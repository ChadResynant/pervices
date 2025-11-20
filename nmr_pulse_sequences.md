# NMR Pulse Sequence Specifications
## Resynant Harmonyzer NMR Spectrometer
### Detailed Waveform and Timing Requirements

**Document Version:** 1.0
**Date:** November 8, 2025
**Customer:** Resynant, Inc.

---

## 1. Introduction

### 1.1 Purpose
This document provides detailed technical specifications for standard NMR pulse sequences to be implemented on the Per Vices Crimson TNG platform. It includes exact timing parameters, RF amplitudes, phases, and waveform definitions to guide FPGA development and system optimization.

### 1.2 Document Scope
- Standard solid-state NMR pulse sequences
- Waveform definitions with quantitative parameters
- RF channel coordination requirements
- Timing precision and synchronization specifications
- FPGA resource requirements for each sequence type

### 1.3 Notation and Conventions

**RF Pulse Notation:**
- **Flip angle:** 90°, 180°, etc. (nominal)
- **Phase:** 0°, 90°, 180°, 270° (TPPI convention: 0° = +x, 90° = +y, 180° = -x, 270° = -y)
- **Duration:** Typically specified in microseconds (μs)
- **Power:** Specified in dBm or as attenuation relative to maximum

**Channel Notation:**
- **1H:** Proton channel (typically Tx B, high power)
- **13C:** Carbon channel (typically Tx A, medium power)
- **15N:** Nitrogen channel (typically Tx C or D, lower power)

---

## 2. Basic NMR Pulse Sequence: Single Pulse Acquisition

### 2.1 Sequence Overview

**Purpose:** Acquire FID following a single excitation pulse

**Pulse Sequence Diagram:**
```
1H:   [90°x] ─────────────────────────
                ↑
13C:  ─────────────────────── [acquire]
           τdead
```

### 2.2 Detailed Timing Sequence

| Time (μs) | 1H Channel (Tx B) | 13C Channel (Tx A) | Rx A | GPIO |
|-----------|-------------------|-------------------|------|------|
| 0 | Idle | Idle | Off | All low |
| 100 | Idle | **90°x pulse START** | Off | GPIO 0 HIGH (Tx A gate) |
| 105 | Idle | **90°x pulse END** | Off | GPIO 0 remain HIGH |
| 110 | Idle | Idle | Off | GPIO 0 LOW |
| 130 | Idle | Idle | Off | Dead time (probe recovery) |
| 135 | Idle | Idle | **Acquire START** | GPIO 4 HIGH (Rx A gate) |
| 100,135 | Idle | Idle | **Acquire END** | GPIO 4 remain HIGH |
| 100,140 | Idle | Idle | Off | GPIO 4 LOW |
| 100,150 | Idle | Idle | Off | Return to idle |

**Total Sequence Duration:** ~100 ms (dominated by acquisition time)

### 2.3 RF Pulse Parameters

**13C 90° Pulse:**
- **Type:** Rectangular (constant amplitude and phase)
- **Duration:** 5 μs (typical for 50 kHz nutation frequency)
- **Phase:** 0° (x-axis)
- **Frequency:** 13C Larmor frequency (e.g., 100.6 MHz at 9.4T, 150.9 MHz at 14.1T)
- **Power Level:** +10 dBm from SDR → 300W from external amplifier (typical)
- **Nutation Frequency:** 50 kHz (90° in 5 μs)

**Calculation:**
- 90° pulse width = 1 / (4 × nutation frequency)
- For 50 kHz nutation: 90° pulse = 1 / (4 × 50 kHz) = 5 μs

### 2.4 Acquisition Parameters

**13C Acquisition:**
- **Spectral Width:** 100 kHz (typical for solid-state 13C)
- **Dwell Time:** 10 μs (= 1 / spectral width)
- **Number of Points:** 10,000 complex points
- **Acquisition Time:** 100 ms
- **Data Size:** 10,000 points × 8 bytes (16-bit I + 16-bit Q) = 80 kB per FID

**FPGA Processing:**
- ADC sample rate: 325 MSPS
- CIC decimation: 325 MSPS → 10 MHz (32.5× decimation)
- Host FIR decimation: 10 MHz → 100 kHz (100× decimation)
- Total decimation: 3250×

### 2.5 GPIO Timing Requirements

**Tx A Gate (GPIO 0):**
- **Activate:** 5 μs before pulse
- **Hold:** 5 μs after pulse (total ~15 μs HIGH)
- **Purpose:** Gate external 13C power amplifier

**Rx A Gate (GPIO 4):**
- **Activate:** 5 μs before acquisition
- **Hold:** Through entire acquisition + 5 μs
- **Purpose:** Gate preamplifier protection circuitry

**Timing Precision:** ±100 ns for all GPIO edges

### 2.6 Phase Cycling (Optional but Recommended)

**Two-Step Phase Cycle:**
```
Scan 1: 13C pulse = 0°,  Receiver = 0°
Scan 2: 13C pulse = 180°, Receiver = 180°
```
**Purpose:** Suppress DC offset and other artifacts

**Four-Step Phase Cycle (CYCLOPS):**
```
Scan 1: 13C pulse = 0°,   Receiver = 0°
Scan 2: 13C pulse = 90°,  Receiver = 90°
Scan 3: 13C pulse = 180°, Receiver = 180°
Scan 4: 13C pulse = 270°, Receiver = 270°
```
**Purpose:** Suppress quadrature image artifacts

### 2.7 Waveform Generation

**13C 90° Rectangular Pulse:**
```
I(t) = A × cos(2π × 0 × t) = A     for 0 ≤ t ≤ 5 μs
Q(t) = A × sin(2π × 0 × t) = 0     for 0 ≤ t ≤ 5 μs
```
Where A = amplitude (full scale for 0 dB attenuation)

**DAC Output:**
- Sample rate: 325 MSPS
- Number of samples: 325 samples/μs × 5 μs = 1625 samples
- I values: [A, A, A, ... A] (1625 values)
- Q values: [0, 0, 0, ... 0] (1625 values)

**Storage Requirement:** Minimal (constant values)

---

## 3. Single-Pulse with Broadband Decoupling

### 3.1 Sequence Overview

**Purpose:** Acquire 13C FID with 1H decoupling to collapse multiplets

**Pulse Sequence Diagram:**
```
1H:   ──────────── [TPPM decoupling]────
                        (100 ms)
13C:  [90°x] ────── [acquire]──────────
           τdead
```

### 3.2 Detailed Timing Sequence

| Time (μs) | 1H Channel (Tx B) | 13C Channel (Tx A) | Rx A | GPIO |
|-----------|-------------------|-------------------|------|------|
| 0 | Idle | Idle | Off | All low |
| 100 | Idle | **90°x pulse START** | Off | GPIO 0 HIGH |
| 105 | Idle | **90°x pulse END** | Off | GPIO 0 LOW (after delay) |
| 110 | Idle | Idle | Off | Dead time |
| 128 | **TPPM decoupling START** | Idle | Off | GPIO 1 HIGH (1H gate) |
| 135 | TPPM continues | Idle | **Acquire START** | GPIO 4 HIGH |
| 100,135 | **TPPM decoupling END** | Idle | **Acquire END** | GPIO 1, 4 remain HIGH |
| 100,138 | Idle | Idle | Off | GPIO 1 LOW |
| 100,140 | Idle | Idle | Off | GPIO 4 LOW |

**Total Sequence Duration:** ~100 ms

### 3.3 13C Observation Pulse

**Same as Section 2.3** (single 90° rectangular pulse)

### 3.4 1H TPPM Decoupling Waveform

**TPPM = Two-Pulse Phase Modulation**

#### 3.4.1 TPPM Parameters

**Basic Element:**
```
[+φ, τp] → [-φ, τp] → repeat
```

**Standard Parameters:**
- **Pulse width (τp):** 6-8 μs
- **Phase angle (φ):** 10-20° (typically 15°)
- **RF amplitude:** Constant, corresponds to ~83-100 kHz nutation frequency
- **Cycle time:** 2 × τp = 12-16 μs per cycle

**Example: TPPM-15 (τp = 7 μs, φ = 15°)**

| Time Segment | Phase | Duration | Cumulative Time |
|--------------|-------|----------|-----------------|
| Pulse 1 | +15° | 7 μs | 0-7 μs |
| Pulse 2 | -15° | 7 μs | 7-14 μs |
| Pulse 3 | +15° | 7 μs | 14-21 μs |
| Pulse 4 | -15° | 7 μs | 21-28 μs |
| ... | ... | ... | ... |

**For 100 ms acquisition:**
- Number of cycles: 100,000 μs / 14 μs ≈ 7,143 cycles
- Total pulses: ~14,286 alternating phase pulses

#### 3.4.2 TPPM Waveform Generation

**Per-Pulse I/Q Values:**

For phase φ = +15°:
```
I(t) = A × cos(15°) ≈ 0.966 A
Q(t) = A × sin(15°) ≈ 0.259 A
```

For phase φ = -15°:
```
I(t) = A × cos(-15°) ≈ 0.966 A
Q(t) = A × sin(-15°) ≈ -0.259 A
```

**DAC Samples per Pulse:**
- Sample rate: 325 MSPS
- Pulse duration: 7 μs
- Samples per pulse: 325 × 7 = 2275 samples

**Basic TPPM Element (2 pulses, 14 μs):**
- I values: [0.966A × 2275 samples] + [0.966A × 2275 samples] = 4550 samples
- Q values: [0.259A × 2275 samples] + [-0.259A × 2275 samples] = 4550 samples
- Total element size: 4550 complex samples × 4 bytes = 18.2 kB

#### 3.4.3 FPGA Implementation Options

**Option 1: Real-Time Streaming from Host**
- Host generates full 100 ms waveform
- Stream via 10GbE to Crimson TNG
- Data rate: 325 MSPS × 4 bytes × 100 ms = 130 MB
- **Bandwidth:** 1.3 GB/s sustained (within 10GbE capacity)
- **Concern:** Latency, jitter, buffer underruns

**Option 2: FPGA Waveform Looping (Preferred)**
- Store basic TPPM element in FPGA block RAM (18.2 kB)
- Hardware loop counter repeats element 7,143 times
- **Advantage:** Zero jitter, minimal host bandwidth
- **FPGA Resources Required:**
  - Block RAM: ~20 kB per decoupling channel
  - Logic: Loop counter (16-bit), address generator, state machine
  - Estimated: <500 logic elements

**Option 3: Compressed Waveform with FPGA Decompression**
- Store only phase/amplitude changes, decompress on FPGA
- More complex but minimal memory
- **Consideration:** May not be necessary given small waveform size

**Recommendation:** Option 2 (FPGA looping) for production, Option 1 (streaming) acceptable for initial prototype

### 3.5 1H RF Power Requirements

**Decoupling Amplitude:**
- Nutation frequency: 83-100 kHz (typical for 1H decoupling)
- Corresponds to: -10 to -15 dB relative to maximum 1H power
- **Example:** If max 1H power is +10 dBm → 1 kW from amplifier
  - Decoupling at -10 dB → 0 dBm → 100W from amplifier (typical)

**Power Calculation:**
- 90° pulse (maximum power): e.g., 2.5 μs → 100 kHz nutation
- Decoupling (reduced power): 83 kHz nutation
- Power ratio: (83/100)² ≈ 0.69 → -1.6 dB
- Attenuation: -10 dB setting achievable

---

## 4. Cross-Polarization with Decoupling

### 4.1 Sequence Overview

**Purpose:** Transfer magnetization from 1H to 13C, then acquire with 1H decoupling

**Pulse Sequence Diagram:**
```
1H:   [90°x]────[CP spin-lock]──────[TPPM decoupling]────
                    (2 ms)              (100 ms)
13C:  ──────────[CP ramp]─────────[acquire]──────────────
                    (2 ms)              (100 ms)
```

### 4.2 Detailed Timing Sequence

| Time (μs) | 1H Channel (Tx B) | 13C Channel (Tx A) | Rx A | GPIO |
|-----------|-------------------|-------------------|------|------|
| 0 | Idle | Idle | Off | All low |
| 100 | **90°y pulse START** | Idle | Off | GPIO 1 HIGH |
| 102.5 | **90°y pulse END** | Idle | Off | — |
| 102.5 | **CP spin-lock START** (phase +y) | **CP ramp START** (phase +x) | Off | GPIO 0 HIGH |
| 2,102.5 | **CP spin-lock END** | **CP ramp END** | Off | — |
| 2,102.5 | Idle | Idle | Off | GPIO 0, 1 LOW |
| 2,125 | **TPPM decoupling START** | Idle | Off | GPIO 1 HIGH |
| 2,135 | TPPM continues | Idle | **Acquire START** | GPIO 4 HIGH |
| 102,135 | **TPPM END** | Idle | **Acquire END** | — |
| 102,138 | Idle | Idle | Off | GPIO 1 LOW |
| 102,140 | Idle | Idle | Off | GPIO 4 LOW |

**Total Sequence Duration:** ~102 ms (dominated by acquisition)

### 4.3 1H Preparation Pulse (90°)

**Parameters:**
- **Duration:** 2.5 μs (for 100 kHz nutation frequency)
- **Phase:** 90° (y-axis, to prepare for spin-lock along +y)
- **Power:** Maximum (0 dB attenuation) → +10 dBm → 1 kW from amplifier (typical)
- **Frequency:** 1H Larmor frequency (e.g., 400 MHz at 9.4T)

**Waveform:**
```
I(t) = A × cos(90°) = 0
Q(t) = A × sin(90°) = A     for 0 ≤ t ≤ 2.5 μs
```

### 4.4 1H Cross-Polarization Spin-Lock

**Parameters:**
- **Duration:** 2000 μs (2 ms)
- **Phase:** 90° (same as prep pulse, maintains spin-lock along +y)
- **RF Amplitude:** Constant, corresponds to 50-83 kHz nutation frequency
- **Power:** -10 to -15 dB attenuation
- **Purpose:** Maintain 1H magnetization in transverse plane during CP contact

**Waveform:**
```
I(t) = A_CP × cos(90°) = 0
Q(t) = A_CP × sin(90°) = A_CP     for 0 ≤ t ≤ 2000 μs
```

Where A_CP = reduced amplitude (e.g., 50% of maximum for -6 dB)

**DAC Samples:**
- Sample rate: 325 MSPS
- Samples: 325 × 2000 = 650,000 samples
- Storage: 650k samples × 4 bytes = 2.6 MB (if stored)
- **Note:** Constant value waveform, can be generated in real-time on FPGA

### 4.5 13C Cross-Polarization Ramp

**Parameters:**
- **Duration:** 2000 μs (2 ms, same as 1H spin-lock)
- **Phase:** 0° (constant throughout ramp)
- **RF Amplitude:** Variable (ramped)
  - **Start:** Corresponds to 40 kHz nutation frequency
  - **End:** Corresponds to 60 kHz nutation frequency
  - **Ramp Profile:** Linear or tangent (depending on Hartmann-Hahn matching optimization)
- **Power:** -20 to -25 dB attenuation range
- **Purpose:** Sweep through Hartmann-Hahn matching condition

#### 4.5.1 Linear Ramp Specification

**Amplitude Ramp:**
```
A(t) = A_start + (A_end - A_start) × (t / T_ramp)
```

Where:
- A_start = amplitude for 40 kHz nutation (e.g., 0.4 × A_max)
- A_end = amplitude for 60 kHz nutation (e.g., 0.6 × A_max)
- T_ramp = 2000 μs

**Waveform:**
```
I(t) = A(t) × cos(0°) = A(t)
Q(t) = A(t) × sin(0°) = 0     for 0 ≤ t ≤ 2000 μs
```

#### 4.5.2 Waveform Generation for CP Ramp

**Discretization:**
- Update rate: Every 5-10 μs (200-400 amplitude steps)
- **Example:** 400 steps over 2 ms → 5 μs per step

**Amplitude Calculation (400 steps):**
```
For step n = 0 to 399:
  t = n × 5 μs
  A[n] = A_start + (A_end - A_start) × (n / 399)
  I[n] = A[n]
  Q[n] = 0
```

**DAC Samples:**
- 5 μs per step × 325 MSPS = 1625 samples per step
- Total samples: 400 steps × 1625 = 650,000 samples
- For each amplitude step, repeat constant I/Q value 1625 times
- **Storage:** 400 unique amplitude values + interpolation logic

**FPGA Implementation:**
- **Option 1:** Store 400 amplitude values in block RAM, DAC outputs interpolated ramp
- **Option 2:** Real-time amplitude calculation via linear interpolator
- **Memory Required:** 400 × 2 bytes = 800 bytes (minimal)

#### 4.5.3 Tangent Ramp (Alternative)

**Purpose:** Match Hartmann-Hahn condition over broader range

**Amplitude Function:**
```
A(t) = A_center + ΔA × tan((t / T_ramp - 0.5) × π/2)
```

Where:
- A_center = center amplitude (e.g., 0.5 × A_max for 50 kHz)
- ΔA = ramp range (e.g., 0.1 × A_max for ±10 kHz sweep)

**Discretization:** Same as linear ramp (400 steps)

### 4.6 1H Decoupling During Acquisition

**Same as Section 3.4** (TPPM decoupling for 100 ms)

### 4.7 Hartmann-Hahn Matching Condition

**Theory:**
In the rotating frame, CP transfer is efficient when:
```
ω₁(1H) = ω₁(13C)
```

Where ω₁ = γB₁ is the nutation frequency in rad/s.

**In practice:**
- 1H spin-lock: Fixed at ~60-83 kHz nutation
- 13C ramp: Sweep from 40-60 kHz to ensure crossing of matching condition
- Ramp compensates for RF inhomogeneity and sample variations

**Optimization:**
- Acquire CP signal vs. 13C amplitude (Hartmann-Hahn profile)
- Identify matching condition (maximum signal)
- Fine-tune ramp center and width

### 4.8 Timing Synchronization Requirements

**Critical Timing:**
1. **1H 90° → CP spin-lock transition:** Immediate (within 1 sample, <10 ns)
   - Phase must remain coherent (90° throughout)
   - No gap between pulses (continuous RF)

2. **1H CP spin-lock ↔ 13C CP ramp synchronization:**
   - **Must start simultaneously** (within 100 ns)
   - **Must end simultaneously** (within 100 ns)
   - Duration exactly equal (2000 μs ± 100 ns)

3. **CP contact → decoupling/acquisition transition:**
   - Brief gap (20-30 μs) for switching transients
   - Not critical for phase coherency (different experiment phase)

**FPGA Coordination:**
- Single timed command triggers both 1H and 13C CP waveforms
- Hardware state machine ensures synchronized start/stop
- Separate GPIO triggers for each channel amplifier

---

## 5. Advanced Decoupling Sequences

### 5.1 SPINAL-64 Decoupling

**SPINAL = Small Phase Incremental Alternation**

#### 5.1.1 SPINAL-64 Structure

**Basic Element (64 pulses):**
```
[φ₁, τ] [φ₂, τ] [φ₁, τ] [φ₂, τ] ... repeated 32 times
```

Where:
- φ₁ = +α (e.g., +10° to +15°)
- φ₂ = -α (e.g., -10° to -15°)
- τ = pulse width (typically 5-10 μs)

**Variations:**
- **SPINAL-64:** 64-pulse element, α = 10-15°
- **SPINAL-32:** 32-pulse element, faster cycling
- **XiX:** More complex phase pattern for improved performance

#### 5.1.2 SPINAL-64 Parameters

**Example: SPINAL-64 with τ = 8 μs, α = 12°**

| Pulse # | Phase | Duration | Cumulative Time |
|---------|-------|----------|-----------------|
| 1 | +12° | 8 μs | 0-8 μs |
| 2 | -12° | 8 μs | 8-16 μs |
| 3 | +12° | 8 μs | 16-24 μs |
| ... | ... | ... | ... |
| 64 | -12° | 8 μs | 504-512 μs |

**Element Duration:** 64 × 8 μs = 512 μs
**For 100 ms acquisition:** 100,000 / 512 ≈ 195 repetitions

#### 5.1.3 SPINAL-64 Waveform Generation

**I/Q Values:**

For phase +12°:
```
I = A × cos(12°) ≈ 0.978 A
Q = A × sin(12°) ≈ 0.208 A
```

For phase -12°:
```
I = A × cos(-12°) ≈ 0.978 A
Q = A × sin(-12°) ≈ -0.208 A
```

**DAC Samples per Element:**
- Samples per pulse: 325 MSPS × 8 μs = 2600 samples
- Total element: 64 × 2600 = 166,400 samples
- Memory: 166,400 × 4 bytes = 665.6 kB

**FPGA Implementation:**
- Store 64-pulse element in block RAM (~666 kB)
- Hardware loop counter repeats 195 times
- **Memory requirement significant but feasible** for Arria V ST (check available block RAM)

### 5.2 SWf-TPPM (Swept-Frequency TPPM)

**Purpose:** Improved decoupling over broad bandwidth

**Concept:** Sweep 1H carrier frequency during decoupling to average over RF inhomogeneity

**Implementation:**
- Baseband TPPM waveform (as in Section 3.4)
- Modulate carrier frequency by ±5 to ±10 kHz
- Sweep period: 100-500 μs

**Complexity:** Higher; may defer to future development

---

## 6. Shaped Pulses

### 6.1 Gaussian Pulse

**Purpose:** Frequency-selective 90° or 180° pulse

#### 6.1.1 Gaussian Pulse Parameters

**Example: Gaussian 180° Pulse**
- **Duration:** 1000 μs (1 ms)
- **Selectivity:** 1 kHz bandwidth (full width at half maximum)
- **Truncation:** Gaussian truncated at ±3σ

**Gaussian Function:**
```
A(t) = A_max × exp(-((t - t_center) / σ)²)
```

Where:
- t_center = 500 μs (center of pulse)
- σ = 170 μs (for 1 kHz bandwidth: FWHM ≈ 2.355σ)
- A_max = peak amplitude

**Phase:** Constant (0°) for on-resonance pulse

#### 6.1.2 Gaussian Pulse Waveform

**Discretization:**
- Sample interval: 200 ns (5 MHz effective rate)
- Number of points: 1000 μs / 200 ns = 5000 points

**Amplitude Calculation:**
```
For point n = 0 to 4999:
  t[n] = n × 0.2 μs
  A[n] = A_max × exp(-((t[n] - 500) / 170)²)
  I[n] = A[n] × cos(0°) = A[n]
  Q[n] = A[n] × sin(0°) = 0
```

**DAC Samples:**
- DAC rate: 325 MSPS
- Upsample 5000 points to 325 MSPS (65× interpolation)
- Total DAC samples: 1000 μs × 325 MSPS = 325,000 samples
- **Interpolation:** Linear or sinc interpolation on FPGA

**Storage:**
- Baseband waveform: 5000 points × 4 bytes = 20 kB
- **FPGA:** Store baseband, interpolate in real-time to DAC rate

#### 6.1.3 Adiabatic Gaussian Pulse (Frequency Sweep)

**Purpose:** Robust inversion over broad bandwidth

**Modification:** Add linear frequency sweep

**Phase Function:**
```
φ(t) = 2π × Δf × (t - t_center)
```

Where Δf = sweep range (e.g., ±10 kHz over 1 ms)

**I/Q Waveform:**
```
I[n] = A[n] × cos(φ[n])
Q[n] = A[n] × sin(φ[n])
```

**Storage:** Same (5000 points × 4 bytes × 2 channels = 40 kB)

### 6.2 Sinc Pulse

**Purpose:** Frequency-selective excitation with flat excitation profile

#### 6.2.1 Sinc Pulse Parameters

**Example: Sinc 90° Pulse**
- **Duration:** 500 μs
- **Selectivity:** 2 kHz bandwidth
- **Lobes:** Truncated sinc with Hamming window

**Sinc Function:**
```
A(t) = A_max × sinc(2π × BW × (t - t_center)) × Hamming(t)
```

Where:
- BW = bandwidth = 2 kHz
- sinc(x) = sin(x) / x
- Hamming(t) = 0.54 - 0.46 × cos(2π × t / T)

**Phase:** Constant (0°)

#### 6.2.2 Sinc Pulse Waveform

**Discretization:** Same as Gaussian (5000 points over 1 ms, or 2500 points over 500 μs)

**Storage:** 2500 points × 4 bytes = 10 kB

---

## 7. FPGA Resource Summary

### 7.1 Block RAM Requirements

**Per-Channel Waveform Storage:**

| Waveform Type | Size | Channels | Total |
|--------------|------|----------|-------|
| TPPM element | 18 kB | 1 (1H decoupling) | 18 kB |
| SPINAL-64 element | 666 kB | 1 (1H decoupling) | 666 kB |
| CP ramp | 0.8 kB | 1 (13C) | 0.8 kB |
| Gaussian shaped pulse | 20 kB | 1 (as needed) | 20 kB |
| **Total (worst case)** | | | **~700 kB** |

**Arria V ST Block RAM:**
- Typical: 10-20 Mb (1.25-2.5 MB) total on-chip memory
- **Assessment:** 700 kB is feasible (<30% of typical block RAM)

**Recommendation:**
- Prioritize TPPM storage (18 kB) for initial implementation
- Defer SPINAL-64 (666 kB) if block RAM constrained; use streaming

### 7.2 Logic Element Requirements

**Per-Channel Processing:**

| Function | Logic Elements (estimate) |
|----------|--------------------------|
| CIC decimation filter (4-stage, 32× decimation) | 500-1000 per Rx channel |
| Waveform address generator and loop control | 200-500 per Tx channel |
| Interpolator for shaped pulses | 500-1000 per Tx channel |
| GPIO timing controller | 200-500 total |
| **Total (4 Rx + 4 Tx + GPIO)** | **~8,000-15,000 LE** |

**Arria V ST Logic Elements:**
- Typical: 100,000-200,000 logic elements depending on specific model
- **Assessment:** 15,000 LE is <15% of typical resources → feasible

### 7.3 FPGA Development Priority

**Phase 1 (Critical for Prototype):**
1. CIC decimation filters (4× Rx channels) → Dynamic range requirement
2. Basic GPIO timing control → Timing precision requirement
3. Basic waveform playback from host streaming → Functional baseline

**Phase 2 (Optimization):**
4. TPPM waveform buffering and loop control → Reduce bandwidth, improve stability
5. CP ramp waveform storage and playback → Complex sequence support

**Phase 3 (Advanced):**
6. SPINAL-64 buffering (if block RAM available)
7. Shaped pulse interpolation and playback
8. Real-time amplitude/frequency modulation

---

## 8. Pulse Sequence Parameter Tables

### 8.1 Typical NMR Frequencies (at Different Field Strengths)

| Nucleus | 9.4 T | 14.1 T | 18.8 T | 21.1 T |
|---------|-------|--------|--------|--------|
| ¹H | 400 MHz | 600 MHz | 800 MHz | 900 MHz |
| ¹³C | 100.6 MHz | 150.9 MHz | 201.2 MHz | 226.3 MHz |
| ¹⁵N | 40.5 MHz | 60.8 MHz | 81.1 MHz | 91.2 MHz |

**Crimson TNG Frequency Range:** 20-1400 MHz (pending confirmation)
**Assessment:** Covers all nuclei at all relevant field strengths ✓

### 8.2 Typical RF Power Levels

| Application | Nutation Freq. | 90° Pulse Width | Attenuation | Power from SDR | Amplifier Output |
|-------------|---------------|-----------------|-------------|----------------|------------------|
| ¹H 90° pulse | 100 kHz | 2.5 μs | 0 dB | +10 dBm | 1000 W |
| ¹H CP spin-lock | 60-83 kHz | — | -10 dB | 0 dBm | 100 W |
| ¹H decoupling | 83-100 kHz | — | -10 dB | 0 dBm | 100 W |
| ¹³C 90° pulse | 50 kHz | 5 μs | 0 dB | +10 dBm | 300 W |
| ¹³C CP ramp | 40-60 kHz | — | -20 dB | -10 dBm | 30 W |
| ¹⁵N 90° pulse | 50 kHz | 5 μs | 0 dB | +10 dBm | 100 W |

**Note:** Amplifier output powers are representative; actual values depend on probe tuning and sample.

### 8.3 Typical Timing Parameters

| Parameter | Typical Range | Precision Required |
|-----------|--------------|-------------------|
| Pulse width (hard pulse) | 1-10 μs | ±50 ns |
| Pulse width (shaped pulse) | 0.1-10 ms | ±1 μs |
| Dead time (Tx → Rx) | 10-100 μs | ±1 μs |
| CP contact time | 0.1-10 ms | ±1 μs |
| Decoupling duration | 10-500 ms | ±10 μs |
| Acquisition time | 10-500 ms | ±10 μs |
| Recycle delay | 0.1-60 seconds | ±1 ms |

### 8.4 Typical Data Acquisition Parameters

| Parameter | Solid-State NMR | Solution NMR | Notes |
|-----------|----------------|--------------|-------|
| Spectral width | 50-500 kHz | 10-50 kHz | Solid-state broader due to anisotropy |
| Acquisition time | 10-100 ms | 0.5-5 s | Solid-state shorter (faster decay) |
| Number of points | 1,000-20,000 | 16,000-256,000 | Depends on resolution needs |
| Dwell time | 2-20 μs | 20-100 μs | = 1 / spectral width |
| Data size per FID | 8-160 kB | 128 kB-2 MB | 8 bytes per complex point |

**Crimson TNG Match:** Excellent for solid-state NMR (primary target)

---

## 9. Software Interface Requirements

### 9.1 Pulse Sequence Programming Interface

**Required Functionality:**
1. **Waveform Upload:** Send arbitrary I/Q waveforms to Crimson TNG
2. **Timed Command Execution:** Trigger waveform playback at precise times
3. **GPIO Control:** Set GPIO states synchronized with RF events
4. **Phase/Amplitude Control:** Real-time adjustment of RF parameters
5. **Acquisition Control:** Define acquisition windows and data routing

### 9.2 Data Structures

**Pulse Sequence Definition (Conceptual):**
```python
class PulseSequenceEvent:
    time: float          # Event time in microseconds
    channel: str         # 'TxA', 'TxB', 'RxA', etc.
    event_type: str      # 'pulse', 'acquire', 'gpio', etc.
    parameters: dict     # Event-specific parameters

class PulseSequence:
    events: List[PulseSequenceEvent]
    waveforms: Dict[str, Waveform]  # Pre-loaded waveforms

    def compile(self) -> bytes:
        """Compile sequence to Crimson TNG command format"""

    def upload(self, crimson: CrimsonTNG):
        """Upload sequence to hardware"""

    def execute(self):
        """Trigger sequence execution"""
```

**Example: Single-Pulse Sequence**
```python
seq = PulseSequence()

# Upload waveforms
seq.add_waveform('C13_90x', rectangular_pulse(duration_us=5, phase_deg=0))

# Define events
seq.add_event(time_us=100, channel='GPIO_0', event_type='set_high')
seq.add_event(time_us=100, channel='TxA', event_type='pulse', waveform='C13_90x')
seq.add_event(time_us=105, channel='GPIO_0', event_type='set_low')
seq.add_event(time_us=135, channel='GPIO_4', event_type='set_high')
seq.add_event(time_us=135, channel='RxA', event_type='acquire', duration_us=100000, points=10000)
seq.add_event(time_us=100140, channel='GPIO_4', event_type='set_low')

# Compile and execute
seq.compile()
seq.upload(crimson_tng)
seq.execute()
```

### 9.3 Integration with Resynant Harmonyzer Software

**Required Development (Resynant Responsibility):**
1. Pulse sequence compiler (translate high-level NMR sequences → Crimson TNG commands)
2. UDP packet receiver and parser (Per Vices PVAN-11 format)
3. Real-time data processing (decimation, filtering, Fourier transform)
4. User interface for pulse sequence programming
5. Data storage and archival (NMR-standard formats)

**Interfaces to Per Vices Crimson TNG:**
1. 10GbE data interface (UDP packets)
2. 1GbE command interface (configuration, control)
3. Timed command API (precise sequence execution)

---

## 10. Validation and Calibration Procedures

### 10.1 Pulse Width Calibration

**Nutation Curve Measurement:**
1. Vary pulse width from 0 to 20 μs in 1 μs steps
2. Acquire signal intensity for each pulse width
3. Fit to: Signal = A × |sin(θ)|, where θ = ω₁ × t
4. Determine 90° pulse width (maximum signal)
5. Verify 180° pulse width = 2 × 90° pulse width (null)

**Expected Result:**
- Sinusoidal intensity modulation
- 90° pulse: 5 μs (for 50 kHz nutation)
- 180° pulse: 10 μs
- 360° pulse: 20 μs (return to zero)

### 10.2 Phase Calibration

**Phase Increment Test:**
1. Acquire FID with pulse phase = 0°
2. Repeat with phase = 90°, 180°, 270°
3. Measure receiver phase for each
4. Verify 90° increments in receiver phase

**Expected Result:**
- Linear phase relationship between transmit and receive
- Slope = 1.0 (or -1.0 depending on phase convention)

### 10.3 Cross-Polarization Optimization

**Hartmann-Hahn Matching:**
1. Fix 1H CP spin-lock amplitude
2. Vary 13C CP amplitude from -30 dB to -10 dB in 1 dB steps
3. Measure 13C signal intensity vs. 13C amplitude
4. Identify matching condition (maximum signal)

**Contact Time Optimization:**
1. Set 13C amplitude to matching condition
2. Vary CP contact time: 0.1, 0.25, 0.5, 1, 2, 3, 5, 8, 10 ms
3. Measure 13C signal intensity vs. contact time
4. Fit to exponential model: I(t) = I₀(1 - exp(-t/T_CP))
5. Extract T_CP (CP transfer time constant)

**Expected Results:**
- Hartmann-Hahn profile: Bell-shaped curve with clear maximum
- Optimal contact time: 1-3 ms (typical for glycine, alanine)
- CP enhancement: 2-10× relative to direct 13C excitation

---

## 11. Conclusion

This document provides comprehensive technical specifications for implementing standard NMR pulse sequences on the Per Vices Crimson TNG platform. Key requirements include:

1. **Precise timing control:** ~100 ns precision for GPIO triggers, microsecond precision for pulse sequences
2. **Multi-channel coordination:** Synchronized Tx/Rx operation with deterministic phase relationships
3. **Waveform generation:** Support for rectangular pulses, shaped pulses, and complex modulation patterns
4. **FPGA optimization:** CIC decimation for dynamic range, waveform buffering/looping for decoupling
5. **Software integration:** Pulse sequence compiler and data acquisition interface

The specifications presented here represent standard solid-state NMR experiments suitable for prototype validation and production deployment. More advanced sequences can be developed once the baseline functionality is established.

---

**Document Status:** Technical specification for FPGA development and prototype validation

**Next Steps:**
1. Review with Per Vices engineering to assess FPGA resource availability
2. Prioritize FPGA development (CIC filters, waveform looping)
3. Develop pulse sequence software interface
4. Validate with prototype testing per test_validation_plan.md

**Contact Information:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
