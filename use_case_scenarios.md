# Use Case Scenarios
## Resynant Harmonyzer NMR Spectrometer SDR System
### Per Vices Crimson TNG Implementation

**Document Version:** 1.0
**Date:** November 8, 2025
**Customer:** Resynant, Inc.

---

## 1. Introduction

This document describes operational use cases for the Crimson TNG-based NMR spectrometer system, progressing from simple to complex pulse sequences. Each use case details the signal flow, timing requirements, and hardware utilization.

### 1.1 General Operating Principles

**Typical NMR Experiment Workflow:**
1. Pre-load waveforms and pulse sequence parameters to SDR
2. Send timed command to initiate pulse sequence
3. Execute transmit pulses with precise timing
4. Trigger GPIO lines for amplifier gating
5. Acquire receive signals during specified time windows
6. Transfer acquired data to host system
7. Repeat for signal averaging (typically 4-10,000 scans)

**Key Requirements Across All Use Cases:**
- Phase coherency between all Tx and Rx channels
- Microsecond-precision timing for all events
- ~100 ns precision GPIO triggering
- Data streaming without dropouts or buffer underruns

---

## 2. Use Case 1: Single-Pulse Acquisition (Simplest Case)

### 2.1 Description
The most basic NMR experiment: apply a single RF pulse to excite nuclear spins, then acquire the resulting free induction decay (FID) signal. This is the foundation for all NMR spectroscopy.

### 2.2 Sequence Parameters

**Channels Used:**
- Tx A: Observation channel transmitter
- Rx A: Observation channel receiver
- GPIO 0: Tx gate for amplifier control
- GPIO 4: Rx gate for preamplifier protection

**Timing Events:**
```
Time (μs)    Event                    Description
─────────────────────────────────────────────────────────────────
0            Pre-scan delay           System stabilization
5            Tx gate ON (GPIO 0)      Enable transmit amplifier
10           Tx pulse START           Begin RF excitation (90° pulse)
15           Tx pulse END             End RF excitation (5 μs pulse)
20           Tx gate OFF (GPIO 0)     Disable transmit amplifier
25           Dead time                Amplifier ring-down, probe recovery
30           Rx gate ON (GPIO 4)      Enable receiver
35           Acquisition START        Begin data acquisition
100,035      Acquisition END          End data acquisition (100 ms)
100,040      Rx gate OFF (GPIO 4)     Disable receiver
100,050      Sequence END             Return to idle state
```

**Pulse Parameters:**
- **Tx Pulse Width:** 5 μs (typical for solid-state NMR 90° pulse)
- **Tx Frequency:** Set to nuclear Larmor frequency (e.g., 400 MHz for 1H at 9.4T)
- **Tx Power:** +10 dBm from SDR → 50W from power amplifier (typical)
- **Tx Phase:** 0° (reference phase)
- **Tx Amplitude:** 100% (no attenuation)

**Acquisition Parameters:**
- **Rx Frequency:** Same as Tx frequency (on-resonance)
- **Spectral Width:** 100 kHz (typical for solid-state NMR)
- **Dwell Time:** 10 μs (1 / spectral width)
- **Acquisition Time:** 100 ms
- **Number of Points:** 10,000 complex points
- **Data Rate:** ~640 kB per scan (after FPGA decimation)

### 2.3 Data Flow

**Transmit Path:**
```
Host System
  └─> Generate 5 μs rectangular pulse (constant amplitude/phase)
  └─> Send via 10GbE to Crimson TNG
      └─> Buffer in FPGA memory
      └─> Timed command triggers DAC output
          └─> DAC38J84 generates I/Q samples at 325 MSPS
              └─> Upconverter to RF frequency
                  └─> +10 dBm output to external amplifier
```

**Receive Path:**
```
NMR Probe Preamplifier (~30 dB gain, 1 dB NF)
  └─> Crimson TNG RF input
      └─> Downconverter to baseband I/Q
          └─> ADC16DX370 samples at 325 MSPS (16-bit I/Q)
              └─> FPGA CIC decimation to 10 MHz
                  └─> 10GbE streaming to host
                      └─> Host FIR filtering to 100 kHz final bandwidth
                          └─> Store as NMR FID file (10,000 complex points)
```

### 2.4 Success Criteria
- Clean FID signal with exponential decay
- No artifacts from transmit-receive switching
- Signal-to-noise ratio appropriate for sample
- Reproducible phase across repeated scans

### 2.5 Variations
- **Variable pulse width:** 1-20 μs (calibrate 90° and 180° pulses)
- **Phase cycling:** Repeat with 0°, 90°, 180°, 270° phases for artifact suppression
- **Relaxation delay:** Vary pre-scan delay (1-60 seconds) for T1 measurements

---

## 3. Use Case 2: Single-Pulse with Broadband Decoupling

### 3.1 Description
Heteronuclear experiment: observe low-gamma nuclei (e.g., 13C, 15N) while applying high-power RF irradiation on protons (1H) during acquisition to remove heteronuclear couplings. This dramatically simplifies spectra and improves sensitivity.

### 3.2 Sequence Parameters

**Channels Used:**
- Tx A: Observation channel (13C transmitter)
- Tx B: Decoupling channel (1H transmitter)
- Rx A: Observation channel (13C receiver)
- GPIO 0: Tx A gate (13C amplifier)
- GPIO 1: Tx B gate (1H amplifier)
- GPIO 4: Rx A gate (receiver protection)

**Timing Events:**
```
Time (μs)    Event                    Description
─────────────────────────────────────────────────────────────────
0            Pre-scan delay           System stabilization
5            Tx A gate ON (GPIO 0)    Enable 13C transmit amplifier
10           Tx A pulse START         Begin 13C RF excitation (90° pulse)
15           Tx A pulse END           End 13C RF excitation
20           Tx A gate OFF (GPIO 0)   Disable 13C transmit amplifier
25           Dead time                Probe recovery
28           Tx B gate ON (GPIO 1)    Enable 1H decoupling amplifier
30           Rx gate ON (GPIO 4)      Enable receiver
30           Decoupling START         Begin 1H decoupling waveform (Tx B)
35           Acquisition START        Begin 13C data acquisition
100,035      Acquisition END          End 13C data acquisition
100,035      Decoupling END           End 1H decoupling waveform
100,038      Tx B gate OFF (GPIO 1)   Disable 1H decoupling amplifier
100,040      Rx gate OFF (GPIO 4)     Disable receiver
100,050      Sequence END             Return to idle state
```

**13C Observation Pulse (Tx A):**
- Pulse Width: 5 μs (typical 90° pulse)
- Frequency: 100.6 MHz (for 13C at 9.4T)
- Power: +10 dBm → 300W from amplifier
- Phase: 0°
- Amplitude: 100%

**1H Decoupling Waveform (Tx B):**
- Type: TPPM (Two-Pulse Phase Modulation) or SPINAL-64
- Base Frequency: 400 MHz (for 1H at 9.4T)
- Power: +10 dBm → 100W from amplifier
- Waveform Length: 128-256 complex points per element
- Element Duration: ~50 μs (typical)
- Total Duration: 100 ms (continuous during acquisition)
- Repetitions: ~2,000 loops of base waveform

### 3.3 Decoupling Waveform Details

**TPPM Decoupling Example:**
- **Pulse Width:** 6 μs per pulse
- **Pulse Phase:** ±15° from carrier (alternating)
- **RF Amplitude:** Constant (corresponds to ~100 kHz nutation frequency)
- **Pattern:** [+15°, 6μs] → [-15°, 6μs] → repeat

**SPINAL-64 Decoupling Example:**
- **Basic Element:** [φ₁, τ] → [φ₂, τ] → [φ₁, τ] → [φ₂, τ] ... (64 steps)
- **Phases:** Small angle modulation (±10° to ±20°)
- **Pulse Width:** 5-10 μs per element
- **Total Element:** 256 steps → 1.28 ms → repeat ~78 times for 100 ms acquisition

**FPGA Storage Requirement:**
- **Preferred Implementation:** Pre-load waveform into FPGA block RAM
- **Loop Control:** Hardware loop counter repeats waveform
- **Advantage:** Reduces 10GbE bandwidth, ensures no timing jitter
- **Alternative:** Stream from host (requires ~1.28 Gbps sustained)

### 3.4 Data Flow

**Transmit Path A (13C Observation):**
- Same as Use Case 1, single rectangular pulse

**Transmit Path B (1H Decoupling):**
```
Host System
  └─> Generate TPPM/SPINAL decoupling waveform (128-256 points)
  └─> Pre-load into FPGA block RAM (preferred) OR stream via 10GbE
      └─> FPGA loop control repeats waveform for acquisition duration
          └─> DAC38J84 generates I/Q samples at 325 MSPS
              └─> Upconverter to 400 MHz
                  └─> +10 dBm output to 1H amplifier
```

**Receive Path:**
- Same as Use Case 1

### 3.5 Success Criteria
- 13C signal with collapsed multiplets (singlets instead of doublets/quartets)
- Sensitivity enhancement from Nuclear Overhauser Effect (NOE)
- Stable decoupling without sample heating
- No decoupling sidebands or artifacts

### 3.6 Synchronization Requirements
- **Critical:** 13C acquisition (Rx A) and 1H decoupling (Tx B) must be precisely synchronized
- **Timing Jitter:** <1 μs for decoupling waveform loop
- **Phase Coherency:** Not strictly required between 13C and 1H channels (different nuclear species)

---

## 4. Use Case 3: Cross-Polarization (CP) with Decoupling

### 4.1 Description
The workhorse experiment for solid-state NMR: transfer magnetization from abundant spins (1H) to rare spins (13C or 15N) for sensitivity enhancement, then acquire with broadband decoupling. Requires precise amplitude and phase control on both channels simultaneously.

### 4.2 Sequence Parameters

**Channels Used:**
- Tx A: 13C transmitter (observation nucleus)
- Tx B: 1H transmitter (source nucleus)
- Rx A: 13C receiver
- GPIO 0: Tx A gate
- GPIO 1: Tx B gate
- GPIO 4: Rx A gate

**Timing Events:**
```
Time (μs)    Event                    Description
─────────────────────────────────────────────────────────────────
0            Pre-scan delay           System stabilization
5            Tx B gate ON (GPIO 1)    Enable 1H transmit amplifier
10           1H prep pulse START      Begin 1H 90° excitation pulse
15           1H prep pulse END        End 1H 90° pulse
15           1H CP spin-lock START    Begin 1H spin-lock for CP
15           Tx A gate ON (GPIO 0)    Enable 13C transmit amplifier
20           13C CP ramp START        Begin 13C spin-lock ramp for CP
2020         CP contact END           End CP contact period (2 ms)
2020         Tx A gate OFF (GPIO 0)   Disable 13C transmit (briefly)
2020         1H CP spin-lock END      End 1H CP field
2025         Dead time                Brief settling period
2028         Tx A gate ON (GPIO 0)    Re-enable 13C transmit for optional pulse
2030         Rx gate ON (GPIO 4)      Enable receiver
2030         1H decoupling START      Begin 1H decoupling (Tx B)
2035         Acquisition START        Begin 13C acquisition (Rx A)
102,035      Acquisition END          End 13C acquisition
102,035      1H decoupling END        End 1H decoupling
102,038      Tx B gate OFF (GPIO 1)   Disable 1H amplifier
102,040      Rx gate OFF (GPIO 4)     Disable receiver
102,050      Sequence END             Return to idle state
```

### 4.3 Cross-Polarization Contact Period Details

**1H Channel (Tx B) - CP Spin-Lock:**
- Duration: 2 ms (time = 15 to 2015 μs in timeline above)
- RF Amplitude: Constant, corresponds to ~50-83 kHz nutation frequency
- RF Phase: Fixed (e.g., 90° for spin-lock following 90° preparation pulse)
- Power Level: -20 dB attenuation relative to maximum (~+10 dBm - 20 dB = -10 dBm)
- Purpose: Maintain 1H magnetization in transverse plane

**13C Channel (Tx A) - CP Spin-Lock with Ramp:**
- Duration: 2 ms (time = 20 to 2020 μs)
- RF Amplitude: **Variable (ramped)**
  - Start: Corresponds to ~40 kHz nutation frequency
  - End: Corresponds to ~60 kHz nutation frequency
  - Ramp profile: Linear or tangent (to match 1H Hartmann-Hahn condition)
- RF Phase: Fixed (e.g., 0°)
- Power Level: -20 to -25 dB attenuation, modulated during ramp
- Purpose: Match Hartmann-Hahn condition for polarization transfer

**Hartmann-Hahn Matching Condition:**
- Requires: ω₁(1H) = ω₁(13C) [in rotating frame]
- In practice: Sweep 13C amplitude through matching condition (ramp)
- Timing precision: Ramp steps typically 5-10 μs

### 4.4 Waveform Generation Requirements

**1H Preparation Pulse:**
- Type: Rectangular (fixed amplitude/phase)
- Duration: 5 μs
- Generation: Simple, streamed from host

**1H CP Spin-Lock:**
- Type: Rectangular (fixed amplitude/phase)
- Duration: 2000 μs
- Generation: Simple, streamed from host or fixed-value DAC output

**13C CP Ramp:**
- Type: Shaped pulse (amplitude modulated)
- Duration: 2000 μs
- Points: 400 complex points (5 μs per point) OR continuous amplitude control
- Generation Options:
  1. Pre-compute ramp, stream from host
  2. Pre-load ramp waveform into FPGA, trigger playback
  3. Real-time amplitude modulation on FPGA (if supported)

**1H Decoupling During Acquisition:**
- Same as Use Case 2 (TPPM or SPINAL-64)

### 4.5 Amplitude Control Requirements

**Coarse Attenuation:**
- 1H CP spin-lock: -20 dB relative to max power
- 13C CP ramp: -20 to -25 dB range
- 1H decoupling: -10 dB relative to max power
- **Requirement:** Programmable attenuation in 10 dB steps (acceptable), prefer finer steps

**Fine Amplitude Control:**
- 13C ramp: Smooth amplitude sweep over 2 ms
- Resolution: 0.1% amplitude precision (competitor spec)
- **Requirement:** DAC-level amplitude control

### 4.6 Phase Control Requirements

**Phase Stability:**
- All RF fields must maintain stable phase throughout CP contact
- **Requirement:** <1° phase drift over 2 ms contact period

**Phase Coherency:**
- 1H and 13C channels must maintain deterministic phase relationship
- **Critical Requirement:** Factory-calibrated phase relationship

### 4.7 Data Flow

**Complex Waveform Coordination:**
```
Host System
  └─> Generate full pulse sequence with all waveforms
  └─> Upload via 10GbE:
      - 1H: prep pulse + 2ms spin-lock + 100ms decoupling waveform
      - 13C: 2ms ramped CP waveform
  └─> Send timed command to trigger sequence
      └─> FPGA coordinates all channels with microsecond precision
          └─> GPIO triggers gate amplifiers
          └─> DACs output synchronized waveforms
          └─> ADC acquires during specified window
          └─> Data streamed back to host via 10GbE
```

### 4.8 Success Criteria
- 13C signal intensity 2-10× higher than direct excitation (CP enhancement)
- Reproducible signal intensity across scans
- Clean baseline without artifacts
- Successful CP matching across different samples

### 4.9 Variations

**Variable Contact Time:**
- Sweep CP contact time from 100 μs to 10 ms
- Study magnetization transfer dynamics

**Ramped vs. Fixed Amplitude:**
- Compare ramped CP (as described) vs. fixed-amplitude CP
- Optimize for different samples

**Multiple Contact Periods:**
- Advanced: Multiple CP transfers in single sequence
- Requires more complex waveform coordination

---

## 5. Use Case 4: Multi-Dimensional NMR (Future Advanced Scenario)

### 5.1 Description
Two-dimensional correlation experiments (e.g., 2D 13C-13C correlation via proton-driven spin diffusion). Requires variable evolution periods and complex phase cycling. Represents most demanding use case.

### 5.2 Overview

**Sequence Outline:**
1. Cross-polarization (as in Use Case 3)
2. **Variable evolution period (t₁):** Incremented across experiment
3. Mixing period (spin diffusion)
4. Acquisition period (t₂) with decoupling

**Complexity:**
- Sequence repeated hundreds of times with different t₁ values
- Each t₁ increment: 10-50 μs steps
- Full experiment: 4-24 hours of acquisition
- Phase cycling: Multiple scans per t₁ increment

### 5.3 Key Requirements

**Reproducibility:**
- Phase must be identical across all t₁ increments
- Critical for 2D Fourier transform coherence

**Timing Precision:**
- t₁ increment precision: <100 ns
- Total t₁ range: 0-10 ms

**Data Management:**
- Store FIDs for each t₁ increment
- File organization for 2D processing

### 5.4 Implementation Notes
- This use case builds on Use Cases 1-3
- Primarily a software/timing challenge
- Hardware requirements same as CP experiment
- Focus for Phase 2 development after prototype validation

---

## 6. Use Case 5: Shaped Pulse Applications

### 6.1 Description
Use of amplitude- and phase-modulated RF pulses for selective excitation, inversion, or refocusing. Common shapes: Gaussian, sinc, tangent, Hermite.

### 6.2 Shaped Pulse Characteristics

**Gaussian Pulse Example:**
- Duration: 1000 μs (1 ms)
- Shape: Gaussian envelope
- Points: 5000 complex points (200 ns per point)
- Amplitude: Smoothly varying from 0 → max → 0
- Phase: Constant OR linear frequency sweep (for adiabatic pulse)
- Purpose: Selective excitation of narrow frequency range

**Sinc Pulse Example:**
- Duration: 500 μs
- Shape: sin(x)/x envelope with Hamming window
- Points: 2500 complex points
- Purpose: Frequency-selective 180° pulse

### 6.3 Waveform Generation

**Host-Side:**
- Pre-compute pulse shape using NMR software
- Convert to I/Q samples at appropriate rate
- Upload to Crimson TNG via 10GbE

**FPGA Buffering:**
- Option 1: Stream from host in real-time
- Option 2: Pre-load into FPGA buffer memory
- **Requirement:** Verify buffer size and sustained data rate

**DAC Output:**
- Playback at 325 MSPS
- Effective pulse resolution: 200 ns (5 MSPS envelope)
- Fine timing via sample clock

### 6.4 Data Flow

```
Host System
  └─> Pulse shape calculation (Gaussian, sinc, etc.)
  └─> Generate I/Q samples (5000 points for 1 ms pulse)
  └─> Upload via 10GbE
      └─> Buffer in FPGA
          └─> Triggered playback through DAC
              └─> Smooth amplitude/phase modulation
```

### 6.5 Success Criteria
- Smooth pulse envelope without glitches
- Frequency-selective excitation profile as designed
- Reproducible performance across scans

---

## 7. General Data Flow Diagrams

### 7.1 Simplified Transmit Data Flow
```
┌─────────────────────────────────────────────────────────────┐
│ Host System (Linux)                                         │
│  - Pulse sequence programming                               │
│  - Waveform generation                                      │
│  - Timed command sequencing                                 │
└──────────────────┬──────────────────────────────────────────┘
                   │ 10 GbE (waveforms, commands)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ Crimson TNG FPGA (Altera Arria V ST)                       │
│  - Waveform buffering                                       │
│  - Timed command execution                                  │
│  - GPIO trigger generation (~100 ns precision)              │
│  - Tx/Rx coordination                                       │
└──┬──────────────────────────┬───────────────────────────────┘
   │ JESD204B                 │ GPIO (TTL via expander)
   ↓                          ↓
┌──────────────────┐    ┌──────────────────────────┐
│ DAC38J84 (Tx A)  │    │ GPIO Expander Board      │
│ 16-bit I/Q       │    │  - Tx gates (4×)         │
│ 325 MSPS         │    │  - Rx gates (4×)         │
└────┬─────────────┘    │  - Spare triggers (4×)   │
     │                  └──────────┬───────────────┘
     │ I/Q Baseband              │ TTL triggers
     ↓                            ↓
┌──────────────────┐    ┌──────────────────────────┐
│ Upconverter      │    │ RF Amplifiers            │
│ LO: tunable      │    │  1H: 50-300W             │
└────┬─────────────┘    │  13C/15N: 100-500W       │
     │                  └──────────┬───────────────┘
     │ RF output                   │ Gated RF
     │ +10 dBm                     ↓
     └─────────────────────────> ┌──────────────────┐
                                 │ NMR Probe        │
                                 └──────────────────┘
```

### 7.2 Simplified Receive Data Flow
```
┌──────────────────┐
│ NMR Probe        │
│  - RF coil       │
│  - Preamplifier  │
│    (~30 dB gain) │
└────┬─────────────┘
     │ Amplified NMR signal
     ↓
┌─────────────────────────────────────────────────────────────┐
│ Crimson TNG Receiver                                        │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │ Downconverter│──>│ ADC16DX370   │──>│ FPGA           │  │
│  │ LO: tunable  │   │ 16-bit I/Q   │   │  - CIC decim.  │  │
│  └──────────────┘   │ 325 MSPS     │   │  - Filtering   │  │
│                     └──────────────┘   └───────┬────────┘  │
└────────────────────────────────────────────────┼───────────┘
                                                  │ 10 GbE
                                                  ↓
┌─────────────────────────────────────────────────────────────┐
│ Host System (Linux)                                         │
│  - UDP packet reception                                     │
│  - FIR filtering and decimation                             │
│  - Data conversion to NMR format                            │
│  - Storage (FID files)                                      │
│  - Fourier transform and processing                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Summary of Use Case Complexity

| Use Case | Channels | Shaped Pulses | FPGA Looping | GPIO Triggers | Relative Complexity |
|----------|----------|---------------|--------------|---------------|---------------------|
| 1. Single pulse | 1 Tx, 1 Rx | No | No | 2 | ★☆☆☆☆ |
| 2. Pulse + decoupling | 2 Tx, 1 Rx | No | Yes (preferred) | 3 | ★★★☆☆ |
| 3. CP + decoupling | 2 Tx, 1 Rx | Yes (CP ramp) | Yes (decoupling) | 3 | ★★★★☆ |
| 4. 2D correlation | 2 Tx, 1 Rx | Yes | Yes | 3 | ★★★★★ |
| 5. Shaped pulses | 1-2 Tx, 1 Rx | Yes | No | 2-3 | ★★★☆☆ |

---

## 9. Implementation Priority

### 9.1 Phase 1 (Prototype Validation)
1. **Use Case 1:** Single-pulse acquisition
   - Validate basic Tx/Rx operation
   - Test GPIO triggering
   - Verify data flow and acquisition
   - **Success metric:** Clean FID signal

2. **Use Case 2:** Single-pulse with broadband decoupling
   - Validate two-channel operation
   - Test decoupling waveform streaming (10GbE)
   - Assess need for FPGA waveform looping
   - **Success metric:** Decoupled spectrum

### 9.2 Phase 2 (Production Readiness)
3. **Use Case 3:** Cross-polarization with decoupling
   - Validate amplitude ramping
   - Test phase coherency
   - Optimize waveform generation
   - **Success metric:** CP-enhanced signals

4. **Use Case 5:** Shaped pulses
   - Validate arbitrary waveform playback
   - Test frequency-selective pulses
   - **Success metric:** Selective excitation

### 9.3 Phase 3 (Advanced Features)
5. **Use Case 4:** Multi-dimensional NMR
   - Long-term stability testing
   - Phase cycling implementation
   - Data management for large datasets
   - **Success metric:** 2D correlation spectra

### 9.4 FPGA Development Decision Points

**After Phase 1:**
- Evaluate 10GbE streaming performance for decoupling waveforms
- If bandwidth or latency issues → proceed with FPGA waveform looping development

**After Phase 2:**
- Assess dynamic range performance
- If ENOB insufficient → evaluate 32-bit float processing or enhanced filtering

---

## 10. Open Questions for Per Vices

1. **FPGA Waveform Buffering:**
   - Available block RAM for waveform storage per channel?
   - Complexity/NRE for implementing hardware loop control?
   - Maximum waveform length that can be buffered?

2. **Real-Time Waveform Streaming:**
   - Guaranteed sustained data rate for waveform upload via 10GbE?
   - Latency and jitter for timed command execution?
   - Buffer underrun protection mechanisms?

3. **GPIO Expander:**
   - Electrical specifications (voltage levels, current drive)?
   - Timing precision verification (100 ns requirement)?
   - Connector type and pinout?

4. **Amplitude Ramping:**
   - Best method for smooth amplitude modulation (Use Case 3)?
   - Precision of fine amplitude control (0.1% target)?
   - Update rate for amplitude changes?

5. **Multi-Channel Coordination:**
   - Guaranteed synchronization between Tx A and Tx B waveforms?
   - Phase coherency maintenance during long sequences (minutes)?
   - Drift characterization over temperature?

---

**Document Status:** Draft for internal review
**Next Steps:**
1. Review use cases with Resynant engineering team
2. Prioritize use cases for prototype validation
3. Discuss FPGA development requirements with Per Vices
4. Define detailed test procedures for each use case

**Contact Information:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
