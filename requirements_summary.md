# Requirements Summary and Gap Analysis
## Resynant Harmonyzer NMR Spectrometer SDR System
### Per Vices Crimson TNG Platform

**Document Version:** 1.0
**Date:** November 8, 2025
**Customer:** Resynant, Inc.

---

## 1. Executive Summary

This document consolidates all requirements from email correspondence with Per Vices (September-November 2025) and cross-references them with Crimson TNG capabilities. It identifies areas where the platform meets requirements out-of-the-box, areas requiring customization, and gaps requiring further discussion.

### 1.1 Overall Assessment

**Crimson TNG Platform Fit:** EXCELLENT
- Core SDR architecture well-suited for NMR application
- 4 Tx / 4 Rx channels match baseline requirement
- Frequency range and bandwidth appropriate
- Phase-coherent multi-channel operation: factory-calibrated
- Customization required: GPIO expander, FPGA development for enhanced features

**Risk Level:** LOW to MODERATE
- Most requirements achievable with Crimson TNG base platform
- Moderate FPGA development needed for optimal performance
- No fundamental architectural mismatches identified

---

## 2. Requirements Traceability Matrix

### 2.1 Channel Configuration

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Number of Rx channels | Email 9/26 | 4 channels | 4 channels (ADC16DX370 ×2) | ✅ Met | Dual-channel ADCs duplicated 2× |
| Number of Tx channels | Email 9/26 | 4 channels | 4 channels (DAC38J84 ×1) | ✅ Met | Quad-channel DAC |
| Phase coherency | Email 9/26 | Deterministic | Factory-calibrated via LMK04828 | ✅ Met | JESD204B subclass 1 |
| Future expandability | Email 9/27 | >4 channels (rare) | Multi-unit sync possible | ⚠️ Requires planning | Secondary unit for >4 ch |

**Gap Analysis:**
- **No gaps for baseline 4-channel system**
- **Multi-unit synchronization:** Per Vices indicated feasible but requires:
  - Additional dual-port 10G NIC on host
  - Additional 1G port for command/control
  - Clock distribution between units (10 MHz reference)
  - Inter-unit triggering via GPIO or network commands

---

### 2.2 Frequency and Bandwidth

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Frequency range | Email 9/26 | 0.2-1400 MHz (practical: 20-1400 MHz) | Per specs: TBD; likely covers range | ⚠️ Verify | Need confirmation of tuning range |
| Bandwidth per channel | Email 9/26 | 20 MHz max | 325 MSPS → 162.5 MHz Nyquist | ✅ Exceeds | More than adequate |
| Tuning resolution | Implied | <1 Hz (NMR standard) | DDC/DUC frequency control | ✅ Met | Software-defined tuning |

**Gap Analysis:**
- **Frequency range verification needed:** Per Vices documentation excerpt did not specify full frequency range. Need confirmation that 20-1400 MHz is covered.
  - **Action Item:** Request detailed frequency range specifications from Per Vices

---

### 2.3 Dynamic Range and Resolution

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| ADC resolution | Email 9/29 | 16-bit minimum | 16-bit I/Q (ADC16DX370) | ✅ Met | Baseline capability |
| ENOB at 5 MHz BW | Email 9/29 | 17-bit | 16-bit + decimation gain | ⚠️ To verify | Requires FPGA CIC |
| ENOB at 1 MHz BW | Email 9/29 | 19-bit (goal) | 16-bit + decimation gain | ⚠️ To verify | Requires FPGA CIC + FIR |
| ENOB at 100 kHz BW | Email 9/29 | 20-bit (goal) | 16-bit + decimation gain | ⚠️ To verify | Aggressive decimation |
| 32-bit float processing | Email 9/29 | If needed for DR | Possible but extensive FPGA work | ❌ Gap | Per Vices: "extensive FPGA work" |

**Gap Analysis:**
- **CIC Decimation Filter:** Required for ENOB enhancement
  - **Status:** Not confirmed if implemented in standard Crimson TNG FPGA image
  - **Action Item:** Confirm FPGA resources available for CIC filter (4× channels)
  - **Fallback:** Host-side decimation (increases network bandwidth requirements)

- **Dynamic Range Validation:** Must be measured with prototype
  - Theoretical: 16-bit + log₂(decimation factor) ≈ 16 + log₂(32) = 21 bits at 10 MHz
  - Practical: Limited by ADC linearity, noise floor, filtering artifacts
  - **Action Item:** Define NMR-based dynamic range test methodology

- **32-Bit Float Processing:** Only if 16-bit decimation insufficient
  - Per Vices indicated "extensive FPGA work" required
  - **Decision Point:** Test dynamic range with prototype before committing to 32-bit development
  - **Estimate Needed:** NRE cost and timeline for 32-bit implementation if required

---

### 2.4 Receive Chain

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Noise figure | Email 9/27 | ≤6 dB | Per specs: TBD | ⚠️ Verify | Adequate given 30 dB preamp |
| Input protection | Implied | Against Tx leakage | Standard per Per Vices | ✅ Assumed | Verify with spec sheet |

**Gap Analysis:**
- **Noise Figure Specification:** Need confirmation that Crimson TNG Rx NF ≤6 dB
  - With 30 dB preamp at 1 dB NF, 6 dB SDR NF contributes ~0.1 dB to system NF → acceptable
  - **Action Item:** Request Rx noise figure specification from Per Vices

---

### 2.5 Transmit Chain

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Max output power | Email 9/26 | +10 dBm | Per specs: TBD; typical for SDRs | ✅ Likely met | Verify specification |
| Attenuation range | Email 9/26 | 0-60 dB | Programmable attenuation | ✅ Met | Standard SDR feature |
| Attenuation steps | Email 9/26 | 10 dB (acceptable), prefer 3 dB or 1 dB | Depends on implementation | ⚠️ Clarify | Fine steps via DAC amplitude if needed |
| Fine amplitude control | Email 9/27 | 0.1% precision | DAC amplitude scaling | ✅ Met | 16-bit DAC → 0.0015% resolution |
| Phase control | Email 9/27 | 0.1° precision | DAC phase control | ✅ Met | Software-defined |

**Gap Analysis:**
- **Attenuation Implementation:** Clarify whether hardware attenuators (step size?) or DAC-level amplitude scaling
  - Fine control (0.1%) achievable via DAC regardless of hardware attenuator step size
  - **Action Item:** Confirm attenuation control architecture

---

### 2.6 Timing and Triggering

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| GPIO triggers | Email 9/27 | 8 minimum, 12 preferred | FPGA GPIO available | ⚠️ Requires expander | Native GPIO is 2.5V logic |
| TTL compatibility | Email 9/27 | 0-5V TTL | Via GPIO expander board | ⚠️ Custom board | Per Vices indicated capability |
| Timing precision | Email 10/1 | ~100 ns | FPGA-controlled | ✅ Likely met | Per Vices: "within range achievable" |
| Timed commands | Implied | Microsecond precision | Network command API | ⚠️ Verify | Latency/jitter TBD |

**Gap Analysis:**
- **GPIO Expander Board:** Required for TTL compatibility
  - **Status:** Per Vices indicated they can provide "GPIO expander device"
  - **Details Needed:**
    - Electrical specifications (voltage levels, current drive)
    - Connector type and pinout
    - Number of available GPIO lines
    - Timing precision verification (100 ns requirement)
  - **Action Item:** Request GPIO expander board specifications and availability

- **Timing Precision Validation:** Critical requirement
  - Per Vices indicated ~100 ns precision is "within range achievable with current hardware"
  - **Must verify with prototype testing**
  - **Action Item:** Include in Phase 1 bench testing (Test 3.4.1)

- **Timed Command Latency:** Not discussed in emails
  - Timed commands sent over 10GbE network
  - Latency and jitter characteristics unknown
  - **Action Item:** Request specifications for timed command execution precision

---

### 2.7 Waveform Generation

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Rectangular pulses | Email 9/27 | Fixed amplitude/phase, 1-1000 μs | DAC streaming or fixed output | ✅ Met | Simple waveform |
| Shaped pulses | Email 9/27 | ~5000 points, 1 ms duration | DAC playback from buffer | ⚠️ Verify buffer | 5000 pts × 4 bytes = 20 kB per waveform |
| Decoupling waveforms | Email 9/27 | 128-256 pts, looped 10s-100s times | FPGA loop control ideal | ❌ Gap | Requires FPGA development |
| Waveform streaming | Email 9/27 | Alternative to FPGA storage | 10GbE data streaming | ✅ Met | Fallback for Phase 1 |

**Gap Analysis:**
- **FPGA Waveform Buffering:** Desired but not confirmed
  - **Use Case:** Store decoupling waveforms in FPGA block RAM, loop via hardware
  - **Benefit:** Reduces 10GbE bandwidth, eliminates jitter
  - **Resource Requirements:**
    - Block RAM: ~1-4 kB per channel for decoupling waveforms
    - Logic: Loop counter, address generator
  - **Action Items:**
    1. Confirm available FPGA block RAM after standard implementation
    2. Estimate NRE cost and timeline for waveform looping feature
    3. Evaluate necessity: Can Phase 1 operate via streaming?

- **Waveform Streaming Performance:** Fallback approach
  - Bandwidth calculation: 325 MSPS × 4 bytes (16-bit I/Q) × 1 Tx channel = 1.3 GB/s
  - For 100 ms decoupling: 130 MB of data per scan
  - **Concern:** Sustained data rate, latency, jitter
  - **Action Item:** Characterize streaming performance in Phase 1 testing

---

### 2.8 Data Interfaces

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| 10GbE interface | Email 9/27 | 10GBASE-R NIC required | SFP+ ports on front panel | ✅ Met | Standard Crimson TNG |
| Data format | Email 9/27 | UDP packets | Per Vices UDP format | ✅ Met | Documented: PVAN-11 |
| Sustainable data rate | Email 9/27 | After decimation: ~1 MB/s | 10GbE → 1.25 GB/s max | ✅ Exceeds | More than adequate |
| Command interface | Implied | Configuration, control | 1GbE management + API | ✅ Met | Standard Crimson TNG |

**Gap Analysis:**
- **No gaps identified** for data interfaces
- **Integration Requirement:** Resynant software must handle Per Vices UDP packet format
  - **Action Item:** Review PVAN-11 data format specification
  - **Action Item:** Develop packet reception and parsing code (Resynant responsibility)

---

### 2.9 Clock and Synchronization

| Requirement | Source | Specification | Crimson TNG Capability | Status | Notes |
|------------|--------|---------------|----------------------|---------|-------|
| Reference clock | Implied | Stable, low phase noise | OCXO, 5 ppb stability, 10 MHz | ✅ Met | Internal OCXO adequate |
| External reference | Optional | 10 MHz input | Supported (single-ended) | ✅ Met | For future multi-unit sync |
| Sample clock | Implied | 325 MSPS (max) | LMK04828 clock generator | ✅ Met | From 5 MHz internal signal |
| Phase coherency | Email 9/26 | Across all channels | JESD204B subclass 1, factory cal. | ✅ Met | Deterministic phase |

**Gap Analysis:**
- **No gaps identified** for clock and synchronization
- **Excellent match** between OCXO stability (5 ppb) and NMR requirements

---

## 3. Summary of Gaps and Action Items

### 3.1 Critical Gaps Requiring Immediate Clarification

| Gap | Priority | Action Item | Owner |
|-----|----------|-------------|-------|
| GPIO expander specifications | HIGH | Request detailed GPIO expander board specs | Per Vices |
| Frequency range confirmation | HIGH | Confirm 20-1400 MHz tuning range covered | Per Vices |
| FPGA CIC decimation | HIGH | Confirm CIC filter implementation and FPGA resources | Per Vices |
| Timing precision validation | HIGH | Verify 100 ns GPIO timing precision achievable | Per Vices (then test) |

### 3.2 Important Gaps Requiring Discussion

| Gap | Priority | Action Item | Owner |
|-----|----------|-------------|-------|
| FPGA waveform looping | MEDIUM | Estimate NRE cost/timeline for waveform buffering and looping | Per Vices |
| Dynamic range validation | MEDIUM | Define test methodology, plan prototype measurements | Resynant + Per Vices |
| Noise figure specification | MEDIUM | Request Rx noise figure specification | Per Vices |
| Timed command latency | MEDIUM | Request timed command execution precision specs | Per Vices |

### 3.3 Optional Enhancements (Nice-to-Have)

| Enhancement | Priority | Action Item | Owner |
|-------------|----------|-------------|-------|
| Finer attenuation steps | LOW | Discuss 1-3 dB attenuation steps vs. 10 dB | Per Vices |
| 32-bit float processing | LOW | Cost/timeline estimate (only if 16-bit insufficient) | Per Vices |
| Multi-unit synchronization | LOW | Architecture discussion for >4 channel future systems | Per Vices |

---

## 4. Crimson TNG Strengths for NMR Application

### 4.1 Excellent Matches

1. **Phase-Coherent Multi-Channel Architecture**
   - Factory-calibrated deterministic phase relationships
   - JESD204B subclass 1 synchronization
   - Critical for NMR, well-implemented on Crimson TNG

2. **High-Performance ADC/DAC**
   - Texas Instruments ADC16DX370 and DAC38J84
   - 325 MSPS sample rate provides oversampling for dynamic range enhancement
   - 16-bit resolution matches competitor baseline

3. **Flexible FPGA Platform**
   - Altera Arria V ST with ARM Cortex-A9
   - Customization possible for CIC filters, waveform looping
   - Embedded Linux for control and data processing

4. **Stable Reference Clock**
   - OCXO with 5 ppb stability
   - Excellent for NMR frequency stability requirements
   - External reference option for multi-unit sync

5. **High-Speed Data Interface**
   - 10GbE more than adequate for NMR data rates
   - Per Vices documented UDP packet format
   - Network-based control simplifies integration

### 4.2 Areas Requiring Customization (But Feasible)

1. **GPIO TTL Interface**
   - Native FPGA GPIO is 2.5V logic
   - GPIO expander board required for 0-5V TTL compatibility
   - Per Vices indicated capability to provide this

2. **FPGA Signal Processing**
   - CIC decimation filters for dynamic range enhancement
   - Waveform buffering and looping for decoupling sequences
   - Requires custom FPGA development but within platform capabilities

3. **Timing Precision Validation**
   - 100 ns GPIO trigger precision required
   - Per Vices indicated achievable, must verify with testing

---

## 5. Competitor Comparison

### 5.1 Competitor System (from Emails)

**Digital Down Converter (ADC):**
- 240 MSPS, 16-bit

**Dynamic Range (with CIC + FIR):**
- 5 MHz bandwidth: 17-bit
- 1 MHz bandwidth: 19-bit
- 6 kHz bandwidth: 23-bit

**Waveform Control:**
- 0.1% amplitude precision
- 0.1° phase precision

### 5.2 Crimson TNG Comparison

| Specification | Competitor | Crimson TNG | Assessment |
|--------------|------------|-------------|------------|
| ADC sample rate | 240 MSPS | 325 MSPS | ✅ Higher (35% faster) |
| ADC resolution | 16-bit | 16-bit | ✅ Equal |
| Dynamic range (5 MHz) | 17-bit | 17-bit (estimated w/ CIC) | ✅ Competitive |
| Dynamic range (1 MHz) | 19-bit | 19-20 bit (estimated) | ✅ Competitive |
| Amplitude precision | 0.1% | 0.0015% (16-bit DAC) | ✅ Exceeds (100× better) |
| Phase precision | 0.1° | Software-limited | ✅ Exceeds |
| Number of channels | Unknown | 4 Tx + 4 Rx | ? |

**Conclusion:** Crimson TNG competitive or superior on key specifications

---

## 6. Project Timeline and Milestones

### 6.1 Pre-Prototype Phase (Current)

**Objective:** Define comprehensive requirements and SOW

**Deliverables:**
- ✅ Technical requirements specification (this document set)
- ⬜ Per Vices responses to action items (GPIO, FPGA, timing, etc.)
- ⬜ Statement of Work (SOW) from Per Vices
- ⬜ NRE cost estimate for FPGA development
- ⬜ Project timeline and milestones

**Timeline:** November 2025 (in progress)

### 6.2 Prototype Development Phase

**Objective:** Per Vices builds and delivers prototype

**Deliverables:**
- Crimson TNG unit with standard firmware
- GPIO expander board (if available)
- Initial FPGA customizations (CIC decimation, if included)
- Documentation and technical support

**Timeline:** TBD (estimate 3-4 months from SOW approval)

### 6.3 Prototype Validation Phase

**Objective:** Resynant validates prototype against requirements

**Deliverables:**
- Test report covering all validation tests
- Performance characterization data
- Pass/fail determination
- Recommendations for optimization or further development

**Timeline:** TBD (estimate 2-3 months, see test_validation_plan.md)

### 6.4 Production Readiness Phase

**Objective:** Finalize design, prepare for production deployment

**Deliverables:**
- Production-ready firmware with all optimizations
- Final documentation and user manuals
- Integration with Resynant Harmonyzer control software
- Training for Resynant engineering staff

**Timeline:** TBD (estimate 2-3 months after prototype acceptance)

---

## 7. Business Considerations

### 7.1 Order Quantities (from Email)

**Initial Prototype:** 1 unit
**Near-term (12 months):** 10 units
**Production (annual):** 50-99 units per year

**Volume Pricing:** To be negotiated (Per Vices indicated volume discounts available)

### 7.2 Current Market Status (from Email)

**Existing Orders:**
- 2 customers × 2 units using refurbished legacy Varian technology
- Several pending orders
- Large order from Indiana University (provides R&D investment opportunity)

**Business Driver:** Phase out refurbished Varian technology → modern SDR solution

**Market Opportunity:** Growth expected in 2026-2027 with modern product offering

### 7.3 Competitive Positioning

**Differentiation Strategy:**
- Meet or exceed competitor specifications (especially dynamic range)
- Leverage Crimson TNG flexibility for advanced NMR techniques
- Provide superior customer support and customization options

**Risk Mitigation:**
- Early prototype validation reduces deployment risk
- Incremental order quantities align with market growth
- Fallback: Continue with refurbished Varian units if prototype fails validation (but undesirable)

---

## 8. Next Steps

### 8.1 Immediate Actions (This Week)

1. **Resynant Internal Review**
   - Review all specification documents
   - Identify any missing requirements or corrections
   - Prioritize requirements (must-have vs. nice-to-have)

2. **Submit to Per Vices**
   - Send specification documents to Brandon Malatest
   - Request responses to all action items (Section 3)
   - Schedule follow-up call to discuss FPGA development

### 8.2 Near-Term Actions (Next 2-4 Weeks)

1. **Per Vices Response Review**
   - Evaluate GPIO expander specifications
   - Assess FPGA development NRE estimates
   - Review dynamic range achievability

2. **SOW Development**
   - Per Vices prepares Statement of Work
   - Include validation metrics per email 10/31
   - Define deliverables, timeline, costs

3. **Decision Point**
   - Approve SOW and proceed with prototype
   - OR request modifications/clarifications

### 8.3 Long-Term Actions (Post-SOW)

1. **Prototype Development** (Per Vices)
2. **Test Environment Preparation** (Resynant)
3. **Software Integration Development** (Resynant)
4. **Prototype Validation** (Resynant + Per Vices)
5. **Production Deployment**

---

## 9. Open Questions for Per Vices Discussion

### 9.1 Technical Questions

1. **GPIO Expander Board**
   - What are the electrical specifications (voltage, current, impedance)?
   - How many GPIO lines are available?
   - What is the timing precision with the expander (verify 100 ns requirement)?
   - Is this a standard product or custom development?
   - What is the cost and delivery timeline?

2. **FPGA Capabilities and Development**
   - Is CIC decimation filter implemented in standard Crimson TNG firmware?
   - If not, what FPGA resources (logic elements, block RAM) are available for custom development?
   - What is the NRE cost and timeline for developing:
     - CIC decimation filters (4× Rx channels)
     - Waveform buffering and hardware looping (for decoupling sequences)
   - Can these be delivered with the prototype, or is this a Phase 2 enhancement?

3. **Performance Specifications**
   - What is the Rx noise figure across the 20-1400 MHz frequency range?
   - What is the Tx output power across the frequency range?
   - What is the guaranteed frequency tuning range?
   - What is the SFDR (spurious-free dynamic range) specification?

4. **Timing and Synchronization**
   - What is the latency and jitter for timed command execution?
   - How is timing coordinated between multiple Tx/Rx channels?
   - What is the phase noise specification for the OCXO and synthesized LOs?

5. **Attenuation and Amplitude Control**
   - How is Tx attenuation implemented (hardware attenuators, DAC scaling, or both)?
   - What are the attenuation step sizes?
   - What is the precision of fine amplitude control via DAC?
   - What is the switching speed for attenuation changes?

6. **Data Streaming**
   - What is the guaranteed sustained data rate for waveform upload via 10GbE?
   - What buffer sizes are available to prevent underruns?
   - Are there any latency or jitter specifications for real-time streaming?

### 9.2 Business Questions

1. **Pricing**
   - What is the unit cost for the prototype (quantity 1)?
   - What volume pricing is available for quantities of 10, 50, 100 units?
   - What is the cost structure for NRE (FPGA development, GPIO expander, etc.)?

2. **Timeline**
   - What is the delivery timeline for the prototype after SOW approval?
   - What is the expected timeline for FPGA development if required?
   - What lead times are typical for production orders?

3. **Support and Warranty**
   - What technical support is provided during prototype validation?
   - What is the warranty period and coverage?
   - Is on-site support available if needed?

4. **Multi-Unit Synchronization (Future)**
   - For >4 channel applications, what is the architecture for synchronizing multiple Crimson TNG units?
   - What additional hardware is required (cables, clock distribution, etc.)?
   - Are there any limitations on the number of units that can be synchronized?

---

## 10. Risk Assessment

### 10.1 Low-Risk Items (High Confidence)

✅ **Basic SDR Functionality:** Crimson TNG is a proven platform
✅ **Phase Coherency:** Factory-calibrated, standard feature
✅ **Data Interfaces:** 10GbE well-established, documented
✅ **Frequency Range:** Likely covered, pending confirmation
✅ **Amplitude/Phase Control:** 16-bit DAC provides excellent precision

### 10.2 Medium-Risk Items (Require Validation)

⚠️ **Dynamic Range:** Depends on FPGA CIC implementation and measured performance
⚠️ **GPIO Timing Precision:** Per Vices indicated achievable, must verify with testing
⚠️ **Waveform Streaming:** Latency and jitter may require FPGA buffering optimization
⚠️ **NMR Integration:** Software development to interface with Resynant Harmonyzer control system

### 10.3 Low-Probability / High-Impact Items

❗ **FPGA Resource Constraints:** If insufficient resources for CIC + waveform looping
  - Mitigation: Prioritize CIC decimation (critical), defer waveform looping to Phase 2

❗ **Timing Precision Inadequate:** If <100 ns GPIO precision not achievable
  - Mitigation: Work with Per Vices on FPGA timing optimization; external timing synchronizer (last resort)

❗ **Fundamental Architecture Mismatch:** Unlikely at this stage
  - Mitigation: Thorough prototype validation before committing to production

---

## 11. Conclusion

### 11.1 Summary

The Per Vices Crimson TNG platform is an **excellent fit** for the Resyannt Harmonyzer NMR spectrometer application. The core SDR architecture, multi-channel phase-coherent design, and high-performance ADC/DAC subsystems align well with NMR requirements.

**Key Strengths:**
- 4 Tx + 4 Rx channels with factory-calibrated phase coherency
- 325 MSPS sample rate enables oversampling for enhanced dynamic range
- Stable OCXO reference clock for frequency stability
- Flexible FPGA platform for customization
- 10GbE data interface more than adequate for NMR data rates

**Areas Requiring Attention:**
- GPIO expander board for TTL compatibility (Per Vices indicated capability)
- FPGA CIC decimation for dynamic range enhancement (to be confirmed)
- Timing precision validation (100 ns GPIO requirement)
- Waveform buffering and looping for optimal decoupling performance (desired, not critical for Phase 1)

**Overall Risk Level:** LOW to MODERATE

The project is well-positioned for success pending clarification of the action items identified in Section 3 and successful prototype validation.

### 11.2 Recommendation

**Proceed with Per Vices Crimson TNG development** with the following approach:

1. **Near-Term:** Obtain Per Vices responses to critical action items (GPIO expander, FPGA resources, timing precision)

2. **Phase 1 Prototype:** Baseline Crimson TNG with GPIO expander
   - Validate core functionality via streaming (defer FPGA waveform looping)
   - Measure dynamic range with available decimation
   - Verify timing precision

3. **Phase 2 Optimization:** Based on Phase 1 results, proceed with FPGA enhancements
   - CIC decimation (if not included in Phase 1)
   - Waveform buffering and looping
   - Any other optimizations identified during validation

4. **Production Deployment:** Finalize design based on validated prototype

This phased approach manages risk while allowing rapid deployment of initial units.

---

**Document Status:** Draft for internal review and submission to Per Vices
**Next Steps:**
1. Resynant internal review and approval
2. Submit to Per Vices with request for responses to action items
3. Schedule follow-up discussion with Per Vices engineering team

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
