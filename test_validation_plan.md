# Test and Validation Plan
## Resynant Harmonyzer NMR Spectrometer SDR System
### Per Vices Crimson TNG Prototype Acceptance Testing

**Document Version:** 1.0
**Date:** November 8, 2025
**Customer:** Resynant, Inc.

---

## 1. Introduction

### 1.1 Purpose
This document defines the test procedures, acceptance criteria, and validation methodology for the Per Vices Crimson TNG-based NMR spectrometer prototype. Testing will be performed in phases, progressing from basic functionality to full system integration.

### 1.2 Testing Philosophy
- **Incremental validation:** Build confidence through progressive complexity
- **Quantitative metrics:** Objective measurements wherever possible
- **NMR-relevant testing:** Ultimate validation with real NMR samples
- **Documentation:** Detailed records for troubleshooting and optimization

### 1.3 Test Environment
- **Location:** Resynant NMR laboratory and/or NMRFAM (National Magnetic Resonance Facility at Madison)
- **Integration:** Crimson TNG connected to existing NMR magnet and probe infrastructure
- **Reference:** Comparison to legacy Varian DDR system where applicable

---

## 2. Test Phases Overview

### Phase 1: Bench Testing (No Magnet Required)
- Electrical and network interface validation
- Basic Tx/Rx functionality
- GPIO trigger timing
- Initial data acquisition

### Phase 2: System Integration Testing (With NMR Magnet)
- Single-channel NMR signal acquisition
- Phase coherency validation
- Timing precision verification

### Phase 3: Multi-Channel Validation
- Multi-channel phase coherency
- Cross-polarization experiments
- Decoupling performance

### Phase 4: Performance Characterization
- Dynamic range measurement
- Long-term stability
- Complex pulse sequences

---

## 3. Phase 1: Bench Testing

### 3.1 Physical Installation and Connectivity

**Test 3.1.1: Power and Boot**
- **Procedure:**
  1. Connect AC power (120/240VAC)
  2. Power on Crimson TNG
  3. Monitor LED indicators
  4. Verify web interface accessibility
- **Expected Result:** Clean boot, web interface accessible within 2 minutes
- **Pass/Fail Criteria:** System boots without errors, web interface responds

**Test 3.1.2: Network Interface**
- **Procedure:**
  1. Connect 10GbE SFP+ to host system
  2. Configure IP addresses per Per Vices documentation
  3. Ping Crimson TNG
  4. Verify data port connectivity
- **Expected Result:** <1 ms ping response, stable connection
- **Pass/Fail Criteria:** Reliable network communication established

**Test 3.1.3: GPIO Expander Interface**
- **Procedure:**
  1. Connect GPIO expander board
  2. Verify TTL voltage levels (expect 0-5V)
  3. Measure output impedance
- **Expected Result:** TTL-compatible outputs, proper electrical characteristics
- **Pass/Fail Criteria:** Voltage levels within TTL specification (0-0.8V low, 2.0-5V high)

---

### 3.2 Transmit Path Validation

**Test 3.2.1: Basic Transmit Output**
- **Equipment:** Spectrum analyzer, 50Ω termination
- **Procedure:**
  1. Set Tx A frequency to 100 MHz
  2. Generate continuous wave (CW) output at +10 dBm
  3. Measure output power and frequency on spectrum analyzer
  4. Repeat for all four Tx channels
- **Expected Result:** +10 dBm ±1 dB at specified frequency
- **Pass/Fail Criteria:** All channels within ±1.5 dB of target, frequency accurate to ±100 Hz

**Test 3.2.2: Frequency Range**
- **Procedure:**
  1. Set Tx A to frequencies: 20, 50, 100, 200, 400, 600, 800, 1000, 1200, 1400 MHz
  2. Verify output power and spectral purity at each frequency
  3. Document any frequency-dependent power variations
- **Expected Result:** Consistent output across frequency range
- **Pass/Fail Criteria:** Output power within ±2 dB across full range, no spurious signals >30 dBc

**Test 3.2.3: Attenuation Control**
- **Procedure:**
  1. Set Tx A to 100 MHz
  2. Program attenuation: 0, -10, -20, -30, -40, -50, -60 dB
  3. Measure output power at each attenuation setting
  4. Calculate actual attenuation vs. programmed
- **Expected Result:** Linear attenuation in 10 dB steps
- **Pass/Fail Criteria:** Attenuation accurate to ±1.5 dB per step

**Test 3.2.4: Pulsed Operation**
- **Equipment:** Oscilloscope (≥1 GHz bandwidth), spectrum analyzer
- **Procedure:**
  1. Generate rectangular pulse: 5 μs duration, 1 ms repetition
  2. Observe pulse on oscilloscope
  3. Measure rise/fall time
  4. Measure pulse width accuracy
- **Expected Result:** Clean pulse shape, <100 ns rise/fall time
- **Pass/Fail Criteria:** Pulse width within ±200 ns, clean on/off transitions

**Test 3.2.5: Phase Control**
- **Equipment:** Oscilloscope, two-channel comparison
- **Procedure:**
  1. Generate CW on Tx A at 100 MHz, phase = 0°
  2. Generate CW on oscilloscope trigger/reference
  3. Change Tx A phase: 0°, 90°, 180°, 270°
  4. Measure phase shift on oscilloscope
- **Expected Result:** Phase shifts as programmed
- **Pass/Fail Criteria:** Phase accurate to ±2° across all settings

---

### 3.3 Receive Path Validation

**Test 3.3.1: Basic Receive Sensitivity**
- **Equipment:** Signal generator (low-noise)
- **Procedure:**
  1. Set Rx A frequency to 100 MHz
  2. Inject -60 dBm signal from signal generator
  3. Acquire data, measure SNR
  4. Repeat with -40, -20, 0 dBm signals
- **Expected Result:** Detectable signal at all input levels
- **Pass/Fail Criteria:** SNR >20 dB for -40 dBm input

**Test 3.3.2: Noise Figure Measurement**
- **Equipment:** Calibrated noise source, spectrum analyzer
- **Procedure:**
  1. Use Y-factor method with noise source
  2. Measure noise figure at 100, 400, 800 MHz
  3. Compare to <6 dB specification
- **Expected Result:** NF <6 dB across frequency range
- **Pass/Fail Criteria:** NF <7 dB (allowing 1 dB margin)

**Test 3.3.3: Frequency Range**
- **Procedure:**
  1. Inject -40 dBm signal at frequencies: 20, 50, 100, 200, 400, 600, 800, 1000, 1200, 1400 MHz
  2. Verify reception at each frequency
  3. Measure SNR variation across frequency range
- **Expected Result:** Consistent sensitivity across range
- **Pass/Fail Criteria:** SNR variation <6 dB across full frequency range

---

### 3.4 GPIO Trigger Timing

**Test 3.4.1: Trigger Output Timing**
- **Equipment:** Oscilloscope (≥1 GHz, ≥4 channels)
- **Procedure:**
  1. Program pulse sequence with Tx pulse and GPIO trigger
  2. Measure time delay from trigger to Tx output
  3. Measure trigger pulse width and jitter
  4. Repeat 100 times, calculate statistics
- **Expected Result:** Consistent trigger-to-Tx delay, low jitter
- **Pass/Fail Criteria:**
  - Trigger-to-Tx delay consistent to ±100 ns (per requirement)
  - Jitter (standard deviation) <50 ns

**Test 3.4.2: Multi-GPIO Synchronization**
- **Procedure:**
  1. Program sequence activating GPIO 0, 1, 2, 3 simultaneously
  2. Measure relative timing on oscilloscope (4-channel)
  3. Repeat 100 times
- **Expected Result:** All triggers fire within 100 ns window
- **Pass/Fail Criteria:** Maximum skew between any two triggers <100 ns

---

### 3.5 Data Acquisition and Streaming

**Test 3.5.1: Basic Data Acquisition**
- **Procedure:**
  1. Inject -40 dBm CW signal at Rx A (100 MHz)
  2. Acquire 10,000 complex points
  3. Verify data reception on host system
  4. Check for dropped packets
- **Expected Result:** Clean data reception, no packet loss
- **Pass/Fail Criteria:** Zero packet loss, correct number of points received

**Test 3.5.2: Sustained Data Rate**
- **Procedure:**
  1. Configure for maximum data rate (320 MSPS, 16-bit I/Q)
  2. Acquire continuously for 10 seconds
  3. Monitor for buffer overruns or dropped packets
  4. Measure actual sustained data rate
- **Expected Result:** Sustained acquisition without data loss
- **Pass/Fail Criteria:** <0.01% packet loss rate

**Test 3.5.3: FPGA Decimation**
- **Procedure:**
  1. Inject known signal at Rx A
  2. Acquire with FPGA decimation (320 MSPS → 10 MHz via CIC filter)
  3. Verify decimated data on host
  4. Compare to expected CIC filter response
- **Expected Result:** Proper decimation, expected filter characteristics
- **Pass/Fail Criteria:** Decimation factor correct, filter response within 10% of ideal CIC

---

## 4. Phase 2: System Integration Testing

### 4.1 Test Sample Preparation

**Standard Test Samples:**
1. **Adamantane (13C NMR):** Sharp singlet, high SNR, known chemical shift
2. **Glycine (13C NMR):** Two peaks (carbonyl and methylene), moderate SNR
3. **Alanine (13C NMR):** Three peaks, known T1 relaxation times
4. **KBr (79Br/81Br NMR):** Broad line, tests wide spectral width

**Sample Requirements:**
- Packed in 4 mm or 3.2 mm rotors
- Known chemical shifts and linewidths
- Sufficient quantity for repeated measurements

---

### 4.2 Single-Channel NMR Validation

**Test 4.2.1: First NMR Signal (Adamantane 13C)**
- **Setup:** 13C Tx/Rx on Tx A/Rx A at appropriate Larmor frequency (e.g., 100.6 MHz at 9.4T)
- **Procedure:**
  1. Tune and match NMR probe to 13C frequency
  2. Calibrate 90° pulse width using nutation curve
  3. Acquire single-pulse FID with optimized parameters
  4. Fourier transform and measure peak height and linewidth
- **Expected Result:**
  - Sharp singlet at 38.5 ppm (adamantane CH peak)
  - Linewidth <50 Hz (under magic-angle spinning)
  - SNR >100:1
- **Pass/Fail Criteria:**
  - Detectable signal at expected chemical shift
  - Linewidth <100 Hz
  - SNR >50:1

**Test 4.2.2: Pulse Width Calibration**
- **Procedure:**
  1. Acquire FID with pulse widths: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 μs
  2. Plot signal intensity vs. pulse width (nutation curve)
  3. Identify 90° (maximum) and 180° (null) pulse widths
- **Expected Result:** Sinusoidal nutation curve
- **Pass/Fail Criteria:**
  - Clear maximum at 90° pulse
  - Clear null at 180° pulse (~2× the 90° pulse width)

**Test 4.2.3: Frequency Accuracy**
- **Procedure:**
  1. Acquire adamantane 13C spectrum
  2. Measure chemical shift of CH peak
  3. Compare to literature value (38.5 ppm relative to TMS)
- **Expected Result:** Peak at 38.5 ±0.1 ppm
- **Pass/Fail Criteria:** Chemical shift within ±0.2 ppm (indicates <2 ppm frequency error)

**Test 4.2.4: Spectral Width and Aliasing**
- **Procedure:**
  1. Set spectral width to 50 kHz
  2. Acquire spectrum, verify no aliasing
  3. Reduce spectral width to 10 kHz
  4. Verify proper folding or absence of signal if outside range
- **Expected Result:** Correct spectral width representation
- **Pass/Fail Criteria:** Spectral width accurate to ±1%, proper handling of signals outside range

---

### 4.3 Phase Stability and Coherency

**Test 4.3.1: Single-Channel Phase Stability**
- **Procedure:**
  1. Acquire adamantane 13C FID with phase = 0°
  2. Repeat 100 times without changing any parameters
  3. Measure first-point phase for each FID
  4. Calculate mean and standard deviation
- **Expected Result:** Consistent phase across all acquisitions
- **Pass/Fail Criteria:** Phase standard deviation <1° across 100 scans

**Test 4.3.2: Programmed Phase Shifts**
- **Procedure:**
  1. Acquire FIDs with transmit phase = 0°, 90°, 180°, 270°
  2. Measure receiver phase for each
  3. Verify 90° increments
- **Expected Result:** Phase shifts as programmed
- **Pass/Fail Criteria:** Measured phase shifts within ±2° of programmed values

**Test 4.3.3: Two-Channel Phase Coherency (13C/1H)**
- **Procedure:**
  1. Tune probe to 1H and 13C frequencies
  2. Inject test signal simultaneously on both channels
  3. Measure relative phase between channels
  4. Repeat 100 times
  5. Calculate phase difference mean and standard deviation
- **Expected Result:** Deterministic phase relationship
- **Pass/Fail Criteria:** Phase difference standard deviation <2° across 100 measurements

---

### 4.4 Timing Precision Validation

**Test 4.4.1: Dead Time Measurement**
- **Procedure:**
  1. Perform single-pulse experiment with minimal dead time
  2. Incrementally reduce delay between Tx pulse end and Rx gate opening
  3. Identify minimum dead time without receiver overload
- **Expected Result:** Dead time <50 μs achievable
- **Pass/Fail Criteria:** Dead time <100 μs without artifacts

**Test 4.4.2: Pulse Spacing Accuracy**
- **Procedure:**
  1. Acquire Hahn echo experiment (90° - τ - 180° - τ - acquire)
  2. Vary τ from 10 μs to 10 ms
  3. Measure echo maximum position
  4. Verify echo maximum occurs at 2τ
- **Expected Result:** Echo position accurate across all τ values
- **Pass/Fail Criteria:** Echo position within ±1% of 2τ

---

## 5. Phase 3: Multi-Channel Validation

### 5.1 Broadband Decoupling Performance

**Test 5.1.1: Single-Pulse with 1H Decoupling (Glycine 13C)**
- **Setup:** 13C observe (Tx A / Rx A), 1H decouple (Tx B)
- **Procedure:**
  1. Acquire 13C spectrum without decoupling
  2. Observe multiplet structure (JCH couplings ~140 Hz)
  3. Acquire 13C spectrum with 1H TPPM decoupling
  4. Observe singlets (collapsed multiplets)
  5. Measure linewidths and SNR
- **Expected Result:**
  - Without decoupling: Multiplets visible
  - With decoupling: Singlets, narrower lines, higher SNR
- **Pass/Fail Criteria:**
  - Decoupling collapses multiplets to singlets
  - SNR improves by factor of 2-4×
  - No decoupling sidebands >5% of signal

**Test 5.1.2: Decoupling Power Optimization**
- **Procedure:**
  1. Acquire glycine 13C with varying 1H decoupling power (-5 to -25 dB)
  2. Measure linewidth and SNR vs. decoupling power
  3. Identify optimal decoupling power
- **Expected Result:** Optimal power gives narrowest lines without sample heating
- **Pass/Fail Criteria:** Achievable linewidth <30 Hz for glycine methylene carbon

**Test 5.1.3: Long-Duration Decoupling Stability**
- **Procedure:**
  1. Apply continuous 1H decoupling for 10 minutes
  2. Monitor sample temperature (if available)
  3. Acquire spectra at 0, 2, 5, 10 minutes
  4. Verify consistent performance
- **Expected Result:** Stable decoupling, no sample heating artifacts
- **Pass/Fail Criteria:** SNR and linewidth variation <10% over 10 minutes

---

### 5.2 Cross-Polarization Performance

**Test 5.2.1: CP Optimization (Glycine 13C)**
- **Procedure:**
  1. Vary 13C CP contact amplitude (Hartmann-Hahn matching)
  2. Fix 1H amplitude, sweep 13C from -30 to -15 dB
  3. Measure signal intensity vs. 13C amplitude
  4. Identify matching condition (maximum signal)
- **Expected Result:** CP matching curve with clear maximum
- **Pass/Fail Criteria:**
  - CP enhancement >2× relative to direct 13C excitation
  - Matching curve shows clear maximum

**Test 5.2.2: CP Contact Time Optimization**
- **Procedure:**
  1. Fix Hartmann-Hahn matching at optimum
  2. Vary CP contact time: 0.1, 0.25, 0.5, 1, 2, 3, 5, 8, 10 ms
  3. Measure signal intensity vs. contact time
  4. Fit to exponential model, extract time constants
- **Expected Result:** Signal grows with contact time, then plateaus/decays
- **Pass/Fail Criteria:**
  - Achievable CP enhancement ≥2× at optimum contact time
  - Time constants consistent with literature values

**Test 5.2.3: CP Reproducibility**
- **Procedure:**
  1. Set CP parameters to optimum values
  2. Acquire 100 consecutive spectra
  3. Measure signal intensity for each
  4. Calculate mean and coefficient of variation (CV)
- **Expected Result:** Consistent CP performance
- **Pass/Fail Criteria:** CV <5% across 100 scans

---

## 6. Phase 4: Performance Characterization

### 6.1 Dynamic Range Measurement

**Test 6.1.1: ENOB Measurement via SNR**
- **Procedure:**
  1. Acquire adamantane 13C spectrum with optimized parameters
  2. Measure signal peak height (S)
  3. Measure RMS noise in empty spectral region (N)
  4. Calculate SNR = S/N
  5. Calculate ENOB = log₂(SNR)
  6. Repeat with different spectral widths: 100 kHz, 1 MHz, 5 MHz
- **Expected Result:** ENOB increases with narrower spectral width (due to decimation)
- **Pass/Fail Criteria:**
  - ENOB ≥17 bits at 5 MHz bandwidth
  - ENOB ≥19 bits at 1 MHz bandwidth (goal)
  - ENOB ≥20 bits at 100 kHz bandwidth (goal)

**Test 6.1.2: Large Signal / Small Signal Coexistence**
- **Sample:** Mixture with 1:1000 signal ratio (e.g., tyrosine with excess solvent)
- **Procedure:**
  1. Acquire 13C spectrum without solvent suppression
  2. Identify strong solvent peak and weak solute peaks
  3. Measure intensity ratio
  4. Verify weak peaks are undistorted and accurately integrated
- **Expected Result:** Both strong and weak signals detected without artifacts
- **Pass/Fail Criteria:** Detectable signals with >10⁶:1 intensity ratio (20-bit requirement)

**Test 6.1.3: Spurious-Free Dynamic Range (SFDR)**
- **Procedure:**
  1. Inject strong CW signal at Rx input (-20 dBm)
  2. Acquire data and Fourier transform
  3. Identify any spurious signals (harmonics, intermodulation)
  4. Calculate SFDR as ratio of main signal to strongest spurious
- **Expected Result:** High SFDR, minimal spurious content
- **Pass/Fail Criteria:** SFDR >80 dBc

---

### 6.2 Long-Term Stability

**Test 6.2.1: Frequency Stability (24-Hour Test)**
- **Procedure:**
  1. Set up continuous acquisition mode (e.g., 1 FID per minute)
  2. Acquire adamantane 13C for 24 hours
  3. Measure peak frequency (chemical shift) for each spectrum
  4. Plot frequency vs. time
  5. Calculate drift rate
- **Expected Result:** Minimal frequency drift, stable over 24 hours
- **Pass/Fail Criteria:**
  - Frequency drift <1 ppm over 24 hours
  - No systematic drift trends (after initial warm-up)

**Test 6.2.2: Phase Stability (24-Hour Test)**
- **Procedure:**
  1. Same acquisition as Test 6.2.1
  2. Measure first-point phase for each FID
  3. Plot phase vs. time
  4. Calculate phase drift rate
- **Expected Result:** Stable phase over 24 hours
- **Pass/Fail Criteria:**
  - Phase drift <10° over 24 hours
  - No systematic drift trends

**Test 6.2.3: Temperature Sensitivity**
- **Procedure:**
  1. If temperature monitoring available, record Crimson TNG and room temperature
  2. Correlate frequency/phase variations with temperature changes
  3. Characterize temperature coefficients
- **Expected Result:** Minimal temperature sensitivity (OCXO should compensate)
- **Pass/Fail Criteria:** Frequency stability <0.1 ppm/°C

---

### 6.3 Complex Pulse Sequence Validation

**Test 6.3.1: Shaped Pulse Performance**
- **Procedure:**
  1. Generate Gaussian-shaped selective pulse (1 ms, selective for 1 kHz bandwidth)
  2. Apply to multi-peak sample (e.g., alanine with 3 peaks spread over 30 kHz)
  3. Observe selective excitation of on-resonance peak only
  4. Measure excitation profile by varying frequency offset
- **Expected Result:** Frequency-selective excitation matching pulse design
- **Pass/Fail Criteria:**
  - Excitation bandwidth within ±20% of design
  - Selectivity >10:1 (on vs. off resonance)

**Test 6.3.2: Two-Dimensional NMR (13C-13C Correlation)**
- **Procedure:**
  1. Acquire 2D 13C-13C DARR experiment (CP-t₁-mixing-t₂)
  2. Increment t₁ from 0 to 10 ms in 100 μs steps (100 increments)
  3. Process 2D dataset
  4. Verify cross-peaks between bonded carbons
- **Expected Result:** 2D correlation spectrum with diagonal and cross-peaks
- **Pass/Fail Criteria:**
  - Clear diagonal peaks for all carbons
  - Detectable cross-peaks between bonded carbons
  - No t₁ noise or phase anomalies

**Test 6.3.3: Complex Multi-Pulse Sequence**
- **Procedure:**
  1. Implement advanced sequence (e.g., REDOR, TEDOR, or RFDR)
  2. Require multiple channels, shaped pulses, and precise timing
  3. Compare results to literature or legacy system
- **Expected Result:** Successful execution of complex sequence
- **Pass/Fail Criteria:** Results comparable to literature values or legacy system

---

## 7. Acceptance Test Summary

### 7.1 Critical Requirements (Must Pass for Acceptance)

| Requirement | Test | Specification | Pass/Fail Criteria |
|------------|------|---------------|-------------------|
| Frequency range | 3.2.2, 4.2.1 | 20-1400 MHz | Validate at 3+ frequencies |
| Phase coherency | 4.3.3 | Deterministic | σ <2° between channels |
| GPIO timing | 3.4.1 | ~100 ns precision | Jitter <50 ns, skew <100 ns |
| Dynamic range | 6.1.1 | ENOB ≥17 @ 5 MHz | Measured ENOB ≥17 bits |
| NMR signal acquisition | 4.2.1 | Detect NMR signal | SNR >50:1 on adamantane |
| Decoupling | 5.1.1 | Collapse multiplets | Singlets with SNR gain 2-4× |
| Cross-polarization | 5.2.1 | CP enhancement ≥2× | Measured enhancement ≥2× |
| Data streaming | 3.5.2 | Sustained rate | <0.01% packet loss |

### 7.2 Performance Goals (Desired but Not Required for Acceptance)

| Goal | Test | Specification | Target |
|------|------|---------------|--------|
| Enhanced dynamic range | 6.1.1 | ENOB @ 1 MHz | ≥19 bits |
| Ultra-high dynamic range | 6.1.1 | ENOB @ 100 kHz | ≥20 bits |
| Wide signal range | 6.1.2 | Simultaneous signals | 10⁶:1 ratio (20-bit) |
| Long-term stability | 6.2.1 | Frequency drift | <0.5 ppm / 24 hr |
| 2D NMR capability | 6.3.2 | Complex sequences | Successful 2D experiment |

---

## 8. Test Documentation and Reporting

### 8.1 Data Collection Requirements

For each test:
1. **Date and time** of test execution
2. **Crimson TNG serial number** and firmware version
3. **Test sample** identification (for NMR tests)
4. **Instrument settings:** Frequency, power levels, timing parameters
5. **Raw data files:** FIDs, spectra, oscilloscope screenshots
6. **Measured results:** SNR, linewidth, ENOB, timing measurements
7. **Pass/Fail determination** with justification
8. **Anomalies or observations**

### 8.2 Test Report Structure

**Executive Summary:**
- Overall pass/fail determination
- Key findings
- Recommended next steps

**Detailed Results:**
- Results for each test in Phases 1-4
- Comparison to acceptance criteria
- Supporting data (plots, tables, spectra)

**Performance Summary:**
- Table of all measured specifications vs. requirements
- Identification of areas meeting/exceeding goals
- Identification of any deficiencies

**Recommendations:**
- Optimization suggestions
- Areas for further development (FPGA enhancements, etc.)
- Readiness for production deployment

---

## 9. Contingency Plans

### 9.1 If Critical Requirements Not Met

**Scenario: GPIO Timing Precision Insufficient**
- **Mitigation:** Work with Per Vices on FPGA timing optimization
- **Alternative:** External timing synchronizer (if available)
- **Timeline:** 2-4 weeks for FPGA modification

**Scenario: Dynamic Range Below Specification**
- **Mitigation:** Optimize FPGA CIC filter parameters
- **Alternative:** Evaluate 32-bit float processing (extensive FPGA work)
- **Timeline:** 1-3 months for FPGA development

**Scenario: Phase Coherency Unstable**
- **Mitigation:** Calibration procedure development
- **Alternative:** Software phase correction algorithms
- **Timeline:** 2-6 weeks

**Scenario: Data Streaming Packet Loss**
- **Mitigation:** Network optimization, FPGA buffer tuning
- **Alternative:** Reduce data rate via more aggressive decimation
- **Timeline:** 1-2 weeks

### 9.2 Risk Mitigation Strategy

For each critical requirement:
1. Early testing in Phase 1 or 2 to identify issues promptly
2. Direct communication with Per Vices engineering for technical support
3. Iterative optimization before final acceptance testing
4. Fallback options identified in advance

---

## 10. Post-Acceptance Activities

### 10.1 Production Readiness Checklist
- [ ] All critical requirements validated
- [ ] Standard operating procedures documented
- [ ] User training completed
- [ ] Integration with Resynant Harmonyzer control software
- [ ] Customer acceptance testing (if applicable)

### 10.2 Ongoing Performance Monitoring
- Quarterly performance validation using standard test samples
- Long-term stability tracking
- Customer feedback integration

### 10.3 Continuous Improvement
- Identify opportunities for FPGA enhancements based on test results
- Evaluate advanced features for future prototypes
- Benchmark against competitor systems

---

## 11. Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Bench Testing | 1-2 weeks | Crimson TNG delivery, test equipment |
| Phase 2: System Integration | 2-3 weeks | NMR magnet access, probe tuning |
| Phase 3: Multi-Channel | 2-4 weeks | Phase 2 completion |
| Phase 4: Performance Characterization | 2-4 weeks | Phases 1-3 completion |
| **Total Estimated Duration** | **7-13 weeks** | Sequential execution |

**Accelerated Timeline (Parallel Testing):** 5-8 weeks if some tests can overlap

---

## 12. Resources Required

### 12.1 Personnel
- **Resynant NMR Specialist:** Lead test execution, NMR expertise
- **Per Vices Engineer:** Remote support, FPGA troubleshooting
- **Resynant Software Engineer:** Data acquisition software integration

### 12.2 Equipment
- Oscilloscope: ≥1 GHz, ≥4 channels
- Spectrum analyzer: 20 MHz - 3 GHz
- Signal generator: Low-noise, 20 MHz - 3 GHz
- Network analyzer: For probe tuning
- NMR magnet: 9.4T or higher (or available field)
- NMR probe: Multi-channel (1H/13C/15N)
- Test samples: Adamantane, glycine, alanine, etc.

### 12.3 Facilities
- Resynant NMR laboratory or NMRFAM
- Bench space for electrical testing
- Network infrastructure: 10GbE switch, host computer

---

## 13. Success Metrics

### 13.1 Quantitative Metrics
- ≥90% of critical requirements met on first prototype
- ≥50% of performance goals achieved
- Zero show-stopper issues requiring hardware redesign

### 13.2 Qualitative Metrics
- NMR spectra quality comparable to legacy Varian system
- Confidence in production deployment
- Positive feedback from test users

### 13.3 Business Metrics
- Timeline to production: <6 months from prototype acceptance
- Cost per unit within budget for production quantities
- Customer satisfaction with Resynant Harmonyzer system

---

**Document Status:** Draft for internal review
**Next Steps:**
1. Review validation plan with Resynant engineering and Per Vices
2. Procure test equipment and prepare test environment
3. Schedule prototype delivery and testing timeline
4. Assign personnel and resources

**Contact Information:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
