# GPIO TTL Interface Specifications
## Resynant Harmonyzer NMR Spectrometer
### Per Vices Crimson TNG Platform

**Document Version:** 1.0
**Date:** November 21, 2025
**Author:** Chad M. Rienstra, Ph.D.

---

## 1. Overview

The Resynant Harmonyzer NMR spectrometer requires TTL-level GPIO outputs to control external RF amplifiers, preamplifiers, and other timing-critical peripherals. This document specifies the exact requirements for the GPIO expander interface.

---

## 2. GPIO Quantity Requirements

### 2.1 Minimum Configuration (8 GPIO outputs)
**Required for basic prototype operation:**

| Channel | GPIO 1 | GPIO 2 |
|---------|--------|--------|
| **Channel A** | TX Enable | RX Enable |
| **Channel B** | TX Enable | RX Enable |
| **Channel C** | TX Enable | RX Enable |
| **Channel D** | TX Enable | RX Enable |
| **TOTAL** | **8 GPIO outputs** | |

### 2.2 Preferred Configuration (12 GPIO outputs)
**Recommended for prototyping flexibility:**

| Channel | GPIO 1 | GPIO 2 | GPIO 3 |
|---------|--------|--------|--------|
| **Channel A** | TX Enable | RX Enable | Spare/Future |
| **Channel B** | TX Enable | RX Enable | Spare/Future |
| **Channel C** | TX Enable | RX Enable | Spare/Future |
| **Channel D** | TX Enable | RX Enable | Spare/Future |
| **TOTAL** | **12 GPIO outputs** | | |

### 2.3 Ultimate Configuration (16 GPIO outputs)
**Ideal for future expandability:**

| Channel | GPIO 1 | GPIO 2 | GPIO 3 | GPIO 4 |
|---------|--------|--------|--------|--------|
| **Channel A** | TX Enable | RX Enable | External Trigger | Future Use |
| **Channel B** | TX Enable | RX Enable | External Trigger | Future Use |
| **Channel C** | TX Enable | RX Enable | External Trigger | Future Use |
| **Channel D** | TX Enable | RX Enable | External Trigger | Future Use |
| **TOTAL** | **16 GPIO outputs** | | | |

---

## 3. Electrical Specifications

### 3.1 Voltage Levels
- **Logic Standard:** TTL-compatible (0-5V)
- **Logic LOW:** 0V to 0.8V
- **Logic HIGH:** 2.0V to 5.0V
- **Output Impedance:** 50Ω preferred (or specify actual impedance)

### 3.2 Current Drive Capability
- **Minimum:** 10 mA per output
- **Preferred:** 20 mA per output
- **Load:** Driving 50Ω transmission lines or high-impedance CMOS inputs

### 3.3 Switching Characteristics
- **Rise/Fall Time:** ≤10 ns (10%-90%)
- **Propagation Delay:** TBD (from FPGA command to GPIO output)
- **Maximum Toggle Rate:** ≥1 MHz

---

## 4. Timing Requirements

### 4.1 Timing Precision (CRITICAL)
- **Absolute Precision:** ±100 ns (channel-to-channel synchronization)
- **Jitter:** <50 ns RMS
- **Repeatability:** <20 ns shot-to-shot

**Rationale:** High-power RF amplifiers require consistent gating to ensure:
- Stable RF output power levels
- Amplifier protection during transients
- Synchronization with pulse sequence timing

### 4.2 Timing Control
- **Control Method:** FPGA-based timing engine
- **Time Base:** Derived from Crimson TNG sample clock (325 MHz)
- **Resolution:** Prefer <10 ns steps (or specify achievable resolution)

### 4.3 Latency
- **Command-to-Output Latency:** Specify actual latency from timed command to GPIO assertion
- **Requirement:** Latency must be deterministic and consistent across all channels

---

## 5. Interface and Connectivity

### 5.1 Physical Connector
- **Connector Type:** Please specify (e.g., DB-25, IDC ribbon, SMA array, etc.)
- **Pinout:** Please provide pinout diagram
- **Location:** Specify location on Crimson TNG chassis or GPIO expander board

### 5.2 Cable Requirements
- **Cable Type:** Shielded twisted-pair preferred for noise immunity
- **Maximum Cable Length:** Specify supported cable length (target: 1-2 meters)

---

## 6. Functional Requirements

### 6.1 TX Enable Outputs (4 required, one per channel)
**Function:** Gate external RF power amplifiers

**Timing Sequence:**
1. Assert TX Enable (HIGH) 10-100 µs before RF pulse
2. Maintain HIGH during RF pulse transmission
3. De-assert TX Enable (LOW) immediately after RF pulse ends

**Critical Requirements:**
- Must be synchronized to TX waveform start/stop
- Timing precision ±100 ns relative to waveform
- Fast de-assertion to protect amplifiers

### 6.2 RX Enable Outputs (4 required, one per channel)
**Function:** Gate external preamplifier protection circuits

**Timing Sequence:**
1. Assert RX Enable (HIGH) immediately after TX pulse ends
2. Maintain HIGH during signal acquisition period
3. De-assert RX Enable (LOW) before next TX pulse

**Critical Requirements:**
- Must be synchronized to RX acquisition start/stop
- Timing precision ±100 ns relative to acquisition window
- Prevent RX saturation from TX leakage

### 6.3 External Trigger Outputs (4 preferred, one per channel)
**Function:** Synchronize external equipment (gradients, sample spinners, etc.)

**Requirements:**
- Programmable pulse width (1 µs to continuous)
- Synchronized to pulse sequence events
- Independent control per channel

### 6.4 Future Use Outputs (4 optional, one per channel)
**Function:** Reserved for future NMR techniques or auxiliary equipment

---

## 7. Control and Programming

### 7.1 Programming Interface
- **How are GPIO outputs controlled?** Via Crimson TNG API over 10GbE? FPGA registers? Timed commands?
- **Please specify:** API commands or register map for GPIO control

### 7.2 Timing Coordination
- **Requirement:** GPIO outputs must be coordinated with TX/RX waveform timing
- **Question:** Can GPIO outputs be included in timed command sequences?
- **Question:** Can GPIO timing be specified relative to sample clock edges?

---

## 8. Performance Validation

### 8.1 Bench Testing (Phase 1)
**Tests to be performed during prototype validation:**

1. **Timing Precision Test:** Measure channel-to-channel skew with oscilloscope
2. **Jitter Test:** Measure GPIO output jitter over 1000 repetitions
3. **Rise/Fall Time Test:** Verify <10 ns transition times
4. **Voltage Level Test:** Confirm TTL compatibility (0-5V)

**Acceptance Criteria:**
- All GPIO outputs within ±100 ns of specification
- Jitter <50 ns RMS
- Rise/fall times <10 ns

### 8.2 NMR Integration Testing (Phase 2)
**Tests with actual RF amplifiers and preamplifiers:**

1. **TX Gating Test:** Verify RF amplifier response to TX Enable
2. **RX Gating Test:** Verify preamplifier protection during TX pulses
3. **Multi-Channel Test:** Verify independent control of all 4 channels
4. **Pulse Sequence Test:** Execute complex NMR pulse sequences with GPIO coordination

---

## 9. Open Questions for Per Vices

### 9.1 Technical Questions
1. **GPIO Expander Availability:** Is this a standard product or custom development?
2. **Cost and Timeline:** What is the NRE cost and delivery timeline for GPIO expander?
3. **Electrical Specifications:** Please provide complete electrical specifications (voltage, current, impedance)
4. **Timing Specifications:** Please confirm achievable timing precision (±100 ns target)
5. **Connector Details:** What connector type and pinout will be used?

### 9.2 Integration Questions
6. **Control Method:** How are GPIO outputs programmed and controlled?
7. **Timing Coordination:** How are GPIO outputs synchronized with TX/RX waveforms?
8. **Latency:** What is the command-to-output latency?
9. **API Documentation:** Is there API documentation for GPIO control?

### 9.3 Validation Questions
10. **Factory Testing:** Will GPIO timing be validated at Per Vices before delivery?
11. **Test Report:** Will timing measurements be provided with prototype?
12. **Support:** What level of support is available during validation testing?

---

## 10. Decision Matrix

| Configuration | GPIO Count | Cost Impact | Timeline Impact | Recommendation |
|---------------|------------|-------------|-----------------|----------------|
| **Minimum (8)** | 8 outputs | Lowest | Fastest | ✅ ACCEPTABLE for prototype |
| **Preferred (12)** | 12 outputs | Medium | Medium | ✅ RECOMMENDED for flexibility |
| **Ultimate (16)** | 16 outputs | Highest | Longest | ⚠️ NICE-TO-HAVE, defer if needed |

**Resynant Decision:**
- **Prototype (Phase 1):** Minimum 8 GPIO acceptable to meet February 2026 delivery
- **Production (Phase 2):** Prefer 12 GPIO for customer flexibility
- **Future (Phase 3):** Ultimate 16 GPIO if achievable without significant NRE

---

## 11. Summary and Action Items

### 11.1 Critical Requirements (Must-Have)
✅ **8 TTL outputs** (2 per channel: TX Enable, RX Enable)
✅ **±100 ns timing precision** (channel-to-channel)
✅ **0-5V TTL levels** (via GPIO expander)
✅ **Synchronized to TX/RX timing** (via FPGA control)

### 11.2 Preferred Features (Should-Have)
⚠️ **12 TTL outputs** (3 per channel, adds 1 spare per channel)
⚠️ **Programmable via API** (for flexible pulse sequence control)
⚠️ **<10 ns rise/fall times** (for clean gating)

### 11.3 Future Enhancements (Nice-to-Have)
💡 **16 TTL outputs** (4 per channel, maximum flexibility)
💡 **<50 ns timing precision** (exceeds requirement)
💡 **Bidirectional GPIO** (for future sensor integration)

### 11.4 Action Items for Per Vices
1. **Review this specification** and confirm feasibility
2. **Provide GPIO expander details:** connector, pinout, electrical specs
3. **Confirm timing precision:** Can ±100 ns be achieved?
4. **Estimate NRE cost and timeline** for GPIO expander development
5. **Provide control documentation:** API or register map for GPIO programming

---

**Contact Information:**

Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

Brandon Malatest, COO
Per Vices Corporation
brandon.m@pervices.com
+1 (647) 534-9007

---

**Document Status:** Ready for Per Vices review
**Next Steps:** Include in documentation package to Per Vices, request feedback by Dec 2, 2025
