# hX and hXX 2D NMR Pulse Sequence Specifications
## Indiana Beta Testing Requirements (May-June 2026)

**Document Version:** 1.0
**Date:** November 21, 2025
**Purpose:** Define minimum 2D/3D NMR capabilities for Indiana University beta deployment

---

## 1. Overview

### 1.1 Indiana Beta Testing Objectives

**Timeline:** May 18 - June 30, 2026 (6 weeks)
**Location:** Indiana University Chemistry Department
**Instrument:** Harmonyzer console with Crimson TNG SDR (prototype upgrade from March Varian-based system)

**Success Criteria:**
- Demonstrate 2D heteronuclear correlation (hX) experiments with performance equivalent to legacy Varian system
- Demonstrate 2D homonuclear correlation (hXX) experiments for advanced structural analysis
- Achieve SNR and resolution suitable for publication-quality data
- Prove system reliability for extended multi-hour 2D/3D acquisitions

### 1.2 Pulse Sequence Priorities for Beta

| Sequence Type | Abbreviation | Priority | Rationale |
|---------------|--------------|----------|-----------|
| **1H-13C HETCOR** | hCH | **P0 (Critical)** | Most common 2D experiment in solid-state NMR |
| **1H-15N HETCOR** | hNH | **P1 (High)** | Protein structure determination |
| **13C-13C DARR** | CXX (DARR) | **P1 (High)** | Homonuclear correlation via spin diffusion |
| **13C-13C RFDR** | CXX (RFDR) | **P2 (Medium)** | Improved dipolar recoupling vs. DARR |
| **NCACX** | 3D | **P2 (Medium)** | 3D for sequential assignment (if time permits) |

---

## 2. hX (Heteronuclear Correlation) Experiments

### 2.1 1H-13C HETCOR (Priority: P0 - CRITICAL)

**Purpose:** Correlate 1H and 13C chemical shifts through dipolar couplings
**Application:** Structure determination, assignment, proximity analysis

#### 2.1.1 Pulse Sequence Diagram

```
1H:  [CP] ──────── t1 (evolution) ──────── [Decoupling during t2]
                    ↓
13C: ─────  [Contact] ──── t1 ──────── [Acquisition (t2)]
                                         + 1H decoupling

Phases: φ1 (1H CP), φ2 (13C evolution), φ3 (receiver)
```

#### 2.1.2 Timing Parameters

| Parameter | Symbol | Typical Value | Range | Precision |
|-----------|--------|---------------|-------|-----------|
| **Cross-polarization contact time** | tcp | 1.0 ms | 0.5 - 5.0 ms | ±10 μs |
| **t1 increment (indirect dimension)** | Δt1 | 20 μs | 10 - 100 μs | ±1 μs |
| **t1 evolution time** | t1 | 0 - 10 ms | Variable | ±1 μs |
| **Acquisition time (t2)** | t2 | 10 - 50 ms | Variable | ±10 μs |
| **Recycle delay** | d1 | 2 - 5 s | 1 - 10 s | ±100 ms |

#### 2.1.3 RF Parameters

| Channel | Pulse/Event | Power | Phase | Duration |
|---------|-------------|-------|-------|----------|
| **1H (Tx B)** | CP ramp | 50-100 kHz | φ1 | tcp (1 ms) |
| **1H (Tx B)** | TPPM decoupling | 80-100 kHz | TPPM-15 | During t1 + t2 |
| **13C (Tx A)** | CP contact | 50 kHz | 0° | tcp (1 ms) |
| **13C (Tx A)** | t1 evolution | - | φ2 | t1 (0-10 ms) |
| **13C (Rx A)** | Acquisition | - | φ3 | t2 (10-50 ms) |

#### 2.1.4 Phase Cycling

**Minimum phase cycle (4 steps):**
- φ1 (1H CP): 0°, 180°, 0°, 180°
- φ2 (13C): 0°, 0°, 180°, 180°
- φ3 (receiver): 0°, 180°, 180°, 0°

**Extended phase cycle (16 steps for artifact suppression):** States-TPPI with nested φ1/φ2 cycling

#### 2.1.5 Typical Acquisition Parameters

- **Number of t1 increments:** 128 - 256 (indirect dimension)
- **Number of t2 points:** 1024 - 2048 (direct dimension)
- **Number of scans per t1:** 16 - 128 (depends on sample concentration)
- **Total experiment time:** 1 - 8 hours (depends on scans and d1)

#### 2.1.6 Expected Performance (Adamantane Test Sample)

- **SNR (1D 13C):** >200:1 (single scan)
- **SNR (2D after processing):** >50:1 per cross-peak
- **Resolution:** 1H: <0.5 ppm, 13C: <0.2 ppm
- **Linewidth:** 1H: ~1 kHz, 13C: ~100 Hz (adamantane CH2)

---

### 2.2 1H-15N HETCOR (Priority: P1 - HIGH)

**Purpose:** Correlate 1H and 15N chemical shifts for protein backbone assignment
**Application:** Protein structure determination, dynamics

#### 2.2.1 Differences from 1H-13C HETCOR

- **15N sensitivity:** ~10× lower than 13C → requires more scans
- **CP contact time:** Typically longer (2-3 ms vs. 1 ms for 13C)
- **15N decoupling:** Lower power (30-50 kHz) due to smaller chemical shift range

#### 2.2.2 Timing Parameters

| Parameter | Symbol | Typical Value | Notes |
|-----------|--------|---------------|-------|
| **CP contact time (1H→15N)** | tcp | 2.0 ms | Longer than 1H→13C |
| **t1 increment** | Δt1 | 40 μs | 15N has smaller spectral width |
| **Acquisition time** | t2 | 20 ms | Adequate for 15N resolution |
| **Number of scans** | NS | 64 - 512 | Higher due to low 15N sensitivity |

#### 2.2.3 Test Sample: Glycine or N-acetylvaline

- **Expected SNR:** >20:1 (2D cross-peak after 128 scans)
- **Linewidth:** 1H: ~1 kHz, 15N: ~200 Hz

---

## 3. hXX (Homonuclear Correlation) Experiments

### 3.1 13C-13C DARR (Priority: P1 - HIGH)

**Purpose:** Correlate 13C spins through dipolar-assisted rotational resonance (spin diffusion)
**Application:** Long-range distance constraints, sequential assignment

#### 3.1.1 Pulse Sequence Diagram

```
1H:  [CP] ──── [Dec] ──── t1 ──── [Dec] ──── τmix (DARR) ──── [Dec during t2]
                                                 ↑
                                              CW irradiation
13C: ─── [Contact] ──── t1 ──── τmix ──────── [Acquisition (t2)]

DARR: Continuous-wave (CW) 1H irradiation at n × νr (rotor frequency)
```

#### 3.1.2 Timing Parameters

| Parameter | Symbol | Typical Value | Range | Notes |
|-----------|--------|---------------|-------|-------|
| **CP contact time** | tcp | 1.0 ms | 0.5 - 2.0 ms | Standard 1H→13C |
| **t1 increment** | Δt1 | 20 μs | 10 - 50 μs | 13C indirect dimension |
| **DARR mixing time** | τmix | 20 - 200 ms | Variable | Determines distance range |
| **Acquisition time** | t2 | 15 ms | 10 - 30 ms | 13C direct dimension |
| **Recycle delay** | d1 | 2 s | 1 - 5 s | Sample dependent |

#### 3.1.3 RF Parameters

| Channel | Event | Power | Phase | Duration |
|---------|-------|-------|-------|----------|
| **1H (Tx B)** | CP ramp | 50-100 kHz | φ1 | tcp |
| **1H (Tx B)** | DARR mixing (CW) | νr or 2νr (10-30 kHz) | 0° | τmix |
| **1H (Tx B)** | TPPM decoupling | 80 kHz | TPPM-15 | During t1 + t2 |
| **13C (Tx A)** | CP contact | 50 kHz | 0° | tcp |
| **13C (Tx A)** | t1 evolution | - | φ2 | t1 (0-5 ms) |
| **13C (Rx A)** | Acquisition | - | φ3 | t2 (15 ms) |

**Critical Requirement:** DARR CW irradiation power must match rotor frequency (νr) or its harmonics
- **MAS rate:** 10 kHz → DARR power = 10 kHz or 20 kHz
- **MAS rate:** 20 kHz → DARR power = 20 kHz or 40 kHz

#### 3.1.4 Phase Cycling

**Minimum (4 steps):**
- φ1 (1H CP): 0°, 180°, 0°, 180°
- φ2 (13C t1): 0°, 0°, 180°, 180°
- φ3 (receiver): 0°, 180°, 180°, 0°

**Extended (16 steps):** States-TPPI with nested cycling

#### 3.1.5 Typical Acquisition

- **t1 points:** 128 - 256
- **t2 points:** 1024 - 2048
- **Scans per t1:** 16 - 64
- **Total time:** 2 - 12 hours

#### 3.1.6 Expected Performance (Uniformly 13C-labeled sample)

- **Diagonal peaks SNR:** >100:1
- **Cross-peaks (short mixing):** >20:1 for directly bonded carbons (τmix = 20 ms)
- **Cross-peaks (long mixing):** >10:1 for 5Å distances (τmix = 200 ms)

---

### 3.2 13C-13C RFDR (Priority: P2 - MEDIUM)

**Purpose:** Improved homonuclear recoupling via rotor-synchronized π pulses
**Application:** Better selectivity than DARR, shorter mixing times

#### 3.2.1 Differences from DARR

- **Mixing sequence:** Train of rotor-synchronized 180° pulses on 13C instead of 1H CW
- **Advantages:** Less heating, better recoupling efficiency
- **Implementation complexity:** Requires precise rotor synchronization

#### 3.2.2 RFDR Mixing Block

```
13C: [180°] ── τr ── [180°] ── τr ── [180°] ── ... (N cycles)
     ↑                ↑                ↑
   Rotor-synchronized (τr = 1/νr)
```

- **τr:** Rotor period (e.g., 50 μs for 20 kHz MAS)
- **Number of cycles:** N = τmix / τr (e.g., 100 cycles for 5 ms mixing at 20 kHz)

#### 3.2.3 Timing Requirements

- **180° pulse width:** <10 μs (requires ~25 kHz RF field)
- **Rotor sync precision:** ±1 μs (FPGA GPIO trigger from MAS controller)
- **Phase alternation:** XY-8 or XY-16 for suppressing pulse imperfections

---

## 4. 3D Experiments (Stretch Goal for Indiana Beta)

### 4.1 NCACX (Priority: P2 - MEDIUM)

**Purpose:** 3D correlation 15N → 13CA → 13CX for protein sequential assignment

#### 4.1.1 Pulse Sequence Overview

```
1H → 15N (CP) → t1 (15N evolution) → SPECIFIC CP → 13CA → t2 (13CA evolution)
                                                        ↓
                                                   DARR/RFDR mixing
                                                        ↓
                                                   t3 (13CX acquisition)
```

#### 4.1.2 Acquisition Parameters

- **t1 (15N):** 32 - 64 increments
- **t2 (13CA):** 32 - 64 increments
- **t3 (13CX):** 1024 - 2048 points
- **Scans per (t1, t2) pair:** 32 - 128
- **Total time:** 24 - 72 hours (multi-day acquisition)

**Beta Test Goal:** Acquire partial 3D dataset (reduced resolution) to validate system stability for extended runs

---

## 5. FPGA and Software Requirements

### 5.1 FPGA Capabilities Needed

| Feature | hX (HETCOR) | hXX (DARR) | hXX (RFDR) | 3D (NCACX) |
|---------|-------------|------------|------------|------------|
| **Multi-channel waveform generation** | ✓ (2 Tx) | ✓ (2 Tx) | ✓ (2 Tx) | ✓ (3 Tx) |
| **Phase cycling** | 4-16 steps | 4-16 steps | 4-16 steps | 8-32 steps |
| **t1/t2/t3 incrementation** | 2D | 2D | 2D | 3D |
| **CP ramp generation** | ✓ (linear) | ✓ (linear) | ✓ (linear) | ✓ (linear/tangent) |
| **TPPM decoupling** | ✓ (1H) | ✓ (1H) | ✓ (1H) | ✓ (1H) |
| **Rotor synchronization (RFDR)** | ✗ | ✗ | ✓ (critical) | Optional |
| **GPIO triggers** | ±100 ns | ±100 ns | ±10 ns (rotor sync) | ±100 ns |

### 5.2 Software Requirements (Pulse Sequence Compiler)

**Indiana Beta Minimum:**

1. **2D Acquisition Framework:**
   - t1/t2 nested loop with phase cycling
   - Automatic phase increment (States-TPPI)
   - Real-time data saving (per t1 increment to prevent data loss)

2. **Pulse Sequence Elements:**
   - Rectangular pulses (90°, 180°) with phase control
   - Linear CP ramp generation
   - TPPM decoupling with user-defined parameters (pulse width, phase)
   - DARR CW irradiation (constant amplitude)
   - RFDR π-pulse train (rotor-synchronized, if implemented)

3. **Data Processing:**
   - 2D FFT with States-TPPI processing
   - Apodization (exponential, Gaussian, sine-bell)
   - Phase correction (manual 2D zeroth/first order)
   - Peak picking and integration

4. **User Interface:**
   - Parameter input for hCH, hNH, DARR experiments
   - Real-time SNR monitoring (1D projections during 2D acquisition)
   - Estimated completion time display
   - Abort/resume functionality for long experiments

---

## 6. Validation Tests for Indiana Beta

### 6.1 Test Samples

| Sample | Purpose | Expected Result |
|--------|---------|-----------------|
| **Adamantane (13C natural abundance)** | 1H-13C HETCOR | Single CH2 cross-peak, SNR >50:1 |
| **Glycine (15N-labeled)** | 1H-15N HETCOR | NH3 cross-peak, SNR >20:1 (64 scans) |
| **U-13C,15N-Alanine** | 13C-13C DARR | CA-CB cross-peaks, SNR >30:1 (τmix = 20 ms) |
| **U-13C,15N-Ubiquitin** | Full 2D/3D suite | Publication-quality protein spectra |

### 6.2 Acceptance Criteria

**Critical (Must-Pass for Beta Success):**
- ✓ 1H-13C HETCOR on adamantane: SNR >50:1, resolution <0.5 ppm (1H), <0.2 ppm (13C)
- ✓ 13C-13C DARR on alanine: Observe CA-CB cross-peak, SNR >20:1 (τmix = 20 ms, 32 scans)
- ✓ System stability: Complete 4-hour 2D acquisition without crashes or packet loss >0.01%

**Desirable (Should-Have):**
- ✓ 1H-15N HETCOR on glycine: SNR >20:1 (64 scans)
- ✓ RFDR mixing (if rotor sync implemented): Demonstrate superior efficiency vs. DARR
- ✓ 3D NCACX on ubiquitin: Partial dataset (reduced resolution) to validate 3D framework

---

## 7. Implementation Timeline

### Phase 1: Software Development (Dec 2025 - Jan 2026)

**Weeks 1-2:**
- Implement 2D acquisition framework (t1/t2 loops, phase cycling)
- Test with simulated data

**Weeks 3-4:**
- Implement CP ramp, TPPM decoupling, DARR mixing pulse elements
- Integrate with Crimson TNG API

**Weeks 5-6:**
- 2D FFT processing, States-TPPI
- Phase correction and display

### Phase 2: Hardware Validation (Feb-Mar 2026)

**Feb 2-13:** Bench testing (loopback, GPIO timing)
**Feb 16 - Mar 10:** NMR integration (adamantane 1D, basic CP)
**Mar 13 - Apr 10:** 2D testing (HETCOR on adamantane, glycine)
**Apr 13 - May 8:** Advanced 2D (DARR on alanine)

### Phase 3: Indiana Beta Preparation (May 2026)

**May 1-15:** System optimization, bug fixes, documentation
**May 18:** Ship to Indiana, on-site installation
**May 18 - June 30:** Beta testing with Indiana user (6 weeks)

---

## 8. Risk Mitigation

### 8.1 Known Challenges

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **RFDR rotor sync not ready by May** | Medium | Medium | Focus on DARR (simpler), defer RFDR to production |
| **2D acquisition software bugs** | Low | High | Extensive testing on simulator, early validation Feb-Apr |
| **Long 2D experiments reveal packet loss** | Low | High | Ring buffer overflow handling, real-time monitoring |
| **Indiana user finds UX confusing** | Medium | Medium | On-site training, comprehensive documentation |

### 8.2 Fallback Plan

If Indiana beta reveals critical issues:
- **Option A:** Extend beta testing through July (1-month extension)
- **Option B:** Deploy interim fix, return for full system upgrade in August
- **Option C:** Maintain Varian backup system in parallel until Crimson TNG proven

---

## 9. Success Metrics

**Quantitative:**
- 2D hCH HETCOR: SNR >50:1, <4 hours acquisition time
- 2D DARR: Cross-peak SNR >20:1 for directly bonded 13C pairs
- Packet loss: <0.01% over 8-hour acquisition
- System uptime: >95% during 6-week beta period

**Qualitative:**
- User satisfaction: "System is as good as or better than Varian" (Indiana PI feedback)
- Data quality: Spectra suitable for publication in Journal of Magnetic Resonance
- Reliability: "I trust this system for production research" (Indiana PI endorsement)

---

## 10. References

**NMR Pulse Sequence Literature:**
- Bennett et al., *J. Chem. Phys.* 103, 6951 (1995) - RFDR recoupling
- Takegoshi et al., *Chem. Phys. Lett.* 344, 631 (2001) - DARR mixing
- Baldus et al., *Mol. Phys.* 95, 1197 (1998) - 3D NCACX for proteins

**Resynant Internal Documents:**
- `technical_requirements.md` - Crimson TNG platform specifications
- `nmr_pulse_sequences.md` - General pulse sequence library
- `test_validation_plan.md` - Acceptance testing procedures

---

**Document Prepared By:** Claude Code (AI Assistant)
**Reviewed By:** [To be reviewed by Chad Rienstra and Alex Dreena]
**Next Revision:** After Per Vices SOW review (Dec 2025)
