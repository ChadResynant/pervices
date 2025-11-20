# Executive Summary
## Resynant Harmonyzer NMR Spectrometer SDR Development
### Per Vices Crimson TNG Platform

**Document Version:** 1.0
**Date:** November 8, 2025
**Prepared by:** Resynant, Inc.
**For:** Per Vices Corporation

---

## 1. Project Overview

### 1.1 Objective

Develop a modern software-defined radio (SDR) transmitter and receiver system for the Resynant Harmonyzer high-resolution solid-state NMR spectrometer platform, replacing legacy refurbished Varian technology with the Per Vices Crimson TNG SDR solution.

### 1.2 Business Context

**Current Situation:**
- Resynant currently fulfills customer orders using refurbished legacy Varian DDR (direct digital receiver) technology
- 2 customers × 2 units currently in hand, several orders pending
- Recent large order from Indiana University provides R&D investment opportunity

**Strategic Importance:**
- Phase out dependence on aging, unsupportable legacy technology
- Enable modern NMR capabilities and improved customer support
- Position Resynant for growth in 2026-2027 market expansion
- Differentiate Harmonyzer product with superior specifications

**Market Opportunity:**
- Initial prototype: 1 unit (Q1 2026)
- Near-term deployment: 10 units within 12 months of validation
- Production volume: 50-99 units per year (2026-2027 onwards)
- Volume pricing to be negotiated with Per Vices

---

## 2. Technical Requirements Summary

### 2.1 Core System Specifications

| Requirement | Specification | Crimson TNG Capability | Status |
|------------|---------------|----------------------|---------|
| **Channels** | 4 Tx + 4 Rx | 4 Tx + 4 Rx | ✅ Met |
| **Frequency Range** | 20-1400 MHz | To be confirmed | ⚠️ Verify |
| **Phase Coherency** | Deterministic, all channels | Factory-calibrated JESD204B | ✅ Met |
| **Dynamic Range** | 17-20 bit ENOB | 16-bit + decimation | ⚠️ To verify |
| **GPIO Triggers** | 8-12 TTL outputs, ~100 ns precision | Via GPIO expander | ⚠️ Custom board |
| **Sample Rate** | 325 MSPS (max) | 325 MSPS | ✅ Met |
| **Data Interface** | 10 GbE | SFP+ 10 GbE | ✅ Met |

### 2.2 Key Technical Challenges

**1. Dynamic Range Enhancement**
- **Goal:** 20-bit ENOB at 100 kHz bandwidth
- **Approach:** FPGA CIC decimation (320 MSPS → 10 MHz) + host FIR filtering
- **Status:** FPGA CIC implementation to be confirmed with Per Vices
- **Risk:** MODERATE - achievable with FPGA development

**2. GPIO Trigger Timing**
- **Requirement:** ~100 ns precision for TTL triggers (8-12 channels)
- **Challenge:** Native FPGA GPIO is 2.5V; requires TTL expander board
- **Status:** Per Vices indicated capability to provide GPIO expander
- **Risk:** LOW - Per Vices has confirmed achievability

**3. Waveform Generation**
- **Requirement:** Complex waveforms for decoupling (looped), shaped pulses
- **Approach:** Phase 1 - streaming via 10GbE; Phase 2 - FPGA buffering/looping
- **Status:** Baseline streaming adequate; FPGA optimization desired
- **Risk:** LOW - streaming works, FPGA looping is optimization

---

## 3. Platform Assessment

### 3.1 Crimson TNG Strengths

✅ **Excellent Architecture Match**
- Multi-channel phase-coherent design with factory calibration
- High-performance ADC/DAC (TI ADC16DX370, DAC38J84)
- Stable OCXO reference (5 ppb) for frequency accuracy
- Flexible Altera Arria V ST FPGA for customization
- Proven SDR platform with established customer base

✅ **Competitive Specifications**
- 325 MSPS sample rate vs. competitor 240 MSPS (35% faster)
- 16-bit resolution matches competitor baseline
- Amplitude precision (0.0015%) exceeds competitor (0.1%) by 100×
- Superior phase control precision

✅ **Scalability and Support**
- Multi-unit synchronization possible for >4 channel future systems
- Established documentation and support infrastructure
- Active development and customer support team

### 3.2 Areas Requiring Customization

⚠️ **GPIO TTL Interface**
- Requires custom GPIO expander board for 0-5V TTL compatibility
- Per Vices has indicated capability to provide
- Cost and timeline to be determined

⚠️ **FPGA Development**
- CIC decimation filters for dynamic range enhancement
- Waveform buffering/looping for decoupling sequences
- Estimated resources: ~700 kB block RAM, ~15k logic elements
- Feasible within Arria V ST capabilities (< 30% of resources)

### 3.3 Overall Platform Fit

**Rating: EXCELLENT**

The Crimson TNG platform aligns exceptionally well with Resyannt Harmonyzer requirements. Core SDR architecture, phase-coherent multi-channel design, and high-performance converters provide a solid foundation. Customization needs (GPIO expander, FPGA development) are well-defined and achievable within platform capabilities.

**Overall Project Risk: LOW to MODERATE**

---

## 4. Project Timeline

### 4.1 Development Phases (ACCELERATED SCHEDULE)

```
Phase 0: Requirements Definition & SOW (ACCELERATED)
├─ November 8, 2025       ✓ Requirements documentation complete
├─ November 11-15, 2025   → Per Vices technical review (EXPEDITED)
├─ November 18-22, 2025   → SOW development and negotiation
└─ November 29, 2025      → SOW approval and project kickoff
    Duration: 3 weeks (vs. 6-8 weeks baseline)
    CRITICAL: Requires immediate Per Vices engagement

Phase 1: Prototype Development (Per Vices) - ACCELERATED
├─ December 2025          → Hardware assembly (standard Crimson TNG)
├─ December 2025          → GPIO expander board (expedited development)
├─ December-January 2026  → FPGA customization (CIC decimation)
└─ January 31, 2026       → Factory testing and delivery
    Duration: 8 weeks (vs. 12-14 weeks baseline)
    Deliverable: Crimson TNG prototype with GPIO expander
    CRITICAL: Requires Per Vices priority commitment

Phase 2: Prototype Validation (Resynant) - ACCELERATED
├─ February 1-14, 2026    → Phase 1 bench testing (electrical, timing)
├─ February 15-28, 2026   → Phase 2 system integration (NMR magnet)
├─ March 1-15, 2026       → Phase 3 multi-channel validation (CP, decoupling)
├─ March 16-25, 2026      → Phase 4 performance characterization
└─ March 31, 2026         → Validation report and acceptance decision
    Duration: 8 weeks (vs. 12-16 weeks baseline)
    Deliverable: Test report with pass/fail determination
    CRITICAL: Requires dedicated Resynant resources and magnet access

Phase 3: Production Readiness (Conditional) - ACCELERATED
├─ April 2026             → FPGA optimization (waveform looping, etc.)
├─ April-May 2026         → Software integration with Harmonyzer
├─ May 2026               → Final documentation and training
└─ May 31, 2026           → Production release
    Duration: 8 weeks (vs. 10-12 weeks baseline)
    Deliverable: Production-ready system
    CRITICAL: Parallel development during Phase 2 validation

Phase 4: Initial Production Deployment
├─ June-August 2026       → First 10 production units
└─ Q4 2026 onwards        → Full production (50-99 units/year)
```

**ACCELERATED TIMELINE SUMMARY:**
- Requirements to Production: **6 months** (vs. 11 months baseline)
- **Time savings: 5 months (45% reduction)**
- **First production units: Q2-Q3 2026** (vs. Q4 2026-Q1 2027)

### 4.2 Summary Timeline (ACCELERATED)

| Milestone | Target Date | Duration from Start | Time Saved |
|-----------|-------------|-------------------|------------|
| Requirements Complete | November 8, 2025 | Week 0 ✓ | — |
| **SOW Approval** | **November 29, 2025** | **Week 3** | **3 weeks** |
| **Prototype Delivery** | **January 31, 2026** | **Week 12** | **8 weeks** |
| **Validation Complete** | **March 31, 2026** | **Week 20** | **12 weeks** |
| **Production Release** | **May 31, 2026** | **Week 29** | **15 weeks** |
| First Production Units | June-August 2026 | Week 32-42 | 10-20 weeks |

**Total Time to Production: ~29 weeks (6.5 months) from requirements complete**
**Time savings vs. baseline: 15 weeks (3.5 months, 45% reduction)**

### 4.3 Critical Path Items (ACCELERATED SCHEDULE)

**WEEK 1-3 (Nov 8-29): SOW Development - HIGHEST PRIORITY**
1. **Immediate Per Vices Engagement** (by Nov 11)
   - Submit complete documentation package TODAY
   - Request expedited technical review (3-5 business days)
   - Schedule technical call by Nov 15
   - **Owner:** Resynant to initiate, Per Vices to commit resources

2. **Rapid SOW Turnaround** (Nov 18-29)
   - Per Vices prepares SOW during week of Nov 18
   - FPGA development NRE estimate (prioritize CIC decimation)
   - GPIO expander specifications and cost (must confirm feasibility)
   - **Target SOW delivery:** November 22
   - **Target SOW approval:** November 29
   - **Risk Mitigation:** Daily check-ins during this period

**WEEK 4-12 (Dec 1 - Jan 31): Prototype Development - CRITICAL PATH**
3. **GPIO Expander Expedited Development** (December 2025)
   - **Must be completed by January 15** to meet prototype deadline
   - Parallel track with main hardware assembly
   - Early prototype for timing validation by January 20
   - **Risk:** Custom board development can slip; need Per Vices commitment

4. **FPGA CIC Decimation** (December-January 2026)
   - **Must be included in prototype delivery** (non-negotiable for schedule)
   - Begin development December 1 (immediately after SOW)
   - Factory validation by January 25
   - **Risk Mitigation:** If CIC unavailable, fall back to host-side decimation (acceptable but not ideal)

5. **Hardware Assembly** (December 2025)
   - Standard Crimson TNG assembly (should be routine)
   - Priority production slot required from Per Vices
   - **Target completion:** January 20 (allows 10 days for integration/testing)

**WEEK 13-20 (Feb 1 - Mar 31): Validation Testing - PARALLEL ACTIVITIES**
6. **Test Environment Preparation** (January 2026, DURING prototype development)
   - **MUST START IMMEDIATELY** - do not wait for prototype delivery
   - Secure NMR magnet access (February-March) - book NOW
   - Prepare test samples (adamantane, glycine, etc.) - order NOW
   - Set up bench test equipment - inventory and procure by December
   - **Owner:** Resynant preparation team

7. **Compressed Validation Schedule** (February-March 2026)
   - Bench testing: 2 weeks (vs. 4 weeks baseline) - focus on critical tests only
   - NMR integration: 2 weeks (vs. 4 weeks) - pre-planned test sequences
   - Multi-channel validation: 2 weeks (vs. 4 weeks) - parallel testing where possible
   - Performance characterization: 2 weeks (vs. 4 weeks) - prioritize must-pass criteria
   - **Risk:** Less time for troubleshooting; may need extended hours

**WEEK 21-29 (Apr 1 - May 31): Production Readiness - OVERLAP WITH VALIDATION**
8. **Parallel Software Development** (Starts December, overlaps with validation)
   - **MUST NOT wait for prototype acceptance**
   - Begin Harmonyzer integration software in December (simulator testing)
   - Pulse sequence compiler development January-February
   - Ready for prototype integration by March
   - **Risk Mitigation:** Parallel path allows recovery time if validation issues arise

9. **FPGA Optimization** (April-May, conditional)
   - Waveform looping implementation (if not in prototype)
   - Performance tuning based on validation results
   - **Can be deferred if needed** - not on critical path for first production units

---

## 5. Cost Considerations

### 5.1 Cost Components (To Be Quoted by Per Vices)

**Non-Recurring Engineering (NRE):**
- GPIO expander board design and fabrication
- FPGA CIC decimation filter development
- FPGA waveform buffering/looping (optional Phase 2)
- Factory testing and validation
- Documentation and training

**Prototype Unit (Quantity 1):**
- Crimson TNG base platform
- GPIO expander board
- Custom FPGA firmware
- Technical support during validation

**Production Units (Quantity 10, then 50-99/year):**
- Per-unit cost with volume pricing
- FPGA firmware licensing (if applicable)
- Ongoing technical support

### 5.2 Resynant Internal Costs (Not in Per Vices SOW)

- Software development (pulse sequence compiler, data acquisition)
- Validation testing labor and magnet time
- Integration with Harmonyzer control system
- Test samples and consumables
- Travel/collaboration expenses (if needed)

### 5.3 Budget Planning

**Estimated Order of Magnitude (Placeholder - Per Vices to Provide Actual Quote):**
- NRE for customization: $XX,XXX - $XXX,XXX
- Prototype unit: $XX,XXX
- Production units (volume pricing): $XX,XXX each

**Decision Point:** SOW review will provide actual costs for budget approval

---

## 6. Risk Assessment

### 6.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Dynamic range below 17-bit target | Low | High | FPGA CIC optimization; 32-bit float processing (extensive NRE) |
| GPIO timing precision insufficient | Low | High | FPGA timing optimization; external timing board (last resort) |
| FPGA resource constraints | Low | Medium | Prioritize CIC (critical), defer waveform looping to Phase 2 |
| Waveform streaming latency issues | Medium | Low | Acceptable for Phase 1; FPGA buffering for production |
| NMR integration challenges | Medium | Medium | Phased software development; vendor collaboration |

### 6.2 Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| SOW negotiation delays | Medium | Medium | Proactive engagement; clear requirements documentation |
| FPGA development complexity | Low | Medium | Phased approach; baseline functionality first |
| Prototype validation extends timeline | Medium | Medium | Detailed test plan; early issue identification |
| Magnet access scheduling | Low | Low | Flexible testing schedule; multiple facility options |

### 6.3 Business Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Prototype fails validation | Low | High | Thorough requirements; Per Vices track record |
| Production costs exceed budget | Low | Medium | Volume pricing negotiation; SOW cost certainty |
| Market demand lower than forecast | Low | Low | Existing orders in hand; conservative estimates |
| Competitor releases superior product | Low | Medium | Crimson TNG specs competitive; rapid deployment |

**Overall Risk Level: LOW to MODERATE**

Project benefits from well-defined requirements, proven SDR platform, and experienced vendors.

---

## 7. Success Criteria

### 7.1 Prototype Acceptance Criteria

**Must-Pass Requirements:**
1. ✅ Phase coherency: <2° standard deviation across all channels
2. ✅ Dynamic range: ENOB ≥17 bits at 5 MHz bandwidth
3. ✅ GPIO timing: ±100 ns precision, jitter <50 ns
4. ✅ Frequency coverage: Validated operation 20-1400 MHz
5. ✅ Data throughput: Sustained acquisition without packet loss (<0.01%)
6. ✅ NMR signal acquisition: SNR >50:1 on adamantane standard sample

**Performance Goals (Desired):**
- Dynamic range: ENOB ≥19 bits at 1 MHz bandwidth
- Large signal range: 10⁶:1 ratio detectable (20-bit)
- Decoupling performance: Multiplet collapse, SNR gain 2-4×
- Cross-polarization: CP enhancement ≥2×

### 7.2 Business Success Metrics

**Near-Term (2026):**
- Prototype validated and accepted: Q2 2026
- First 10 production units deployed: Q4 2026 - Q1 2027
- Phase out legacy Varian technology: 50% by end of 2026

**Long-Term (2027+):**
- Production deployment: 50-99 units per year
- Customer satisfaction: NMR performance meets/exceeds legacy Varian
- Market differentiation: Superior specifications drive Harmonyzer sales

---

## 8. Key Questions for Per Vices

### 8.1 Critical Questions (Required for SOW)

**GPIO Expander:**
1. What are the detailed electrical specifications (voltage levels, current drive, impedance)?
2. What is the timing precision with the expander (verify 100 ns requirement)?
3. How many GPIO lines are available (8 minimum, 12 preferred)?
4. What is the cost and delivery timeline?
5. Is this a standard product or custom development?

**FPGA Development:**
6. Is CIC decimation filter implemented in standard Crimson TNG firmware?
7. What FPGA resources (logic elements, block RAM) are available after standard implementation?
8. What is the NRE cost and timeline for:
   - CIC decimation filters (4× Rx channels)
   - Waveform buffering and hardware looping (for decoupling)
9. Can CIC decimation be delivered with prototype, or is it Phase 2?

**Performance Specifications:**
10. What is the Rx noise figure across 20-1400 MHz?
11. What is the Tx output power across the frequency range?
12. What is the guaranteed frequency tuning range?
13. What is the SFDR (spurious-free dynamic range)?

**Project Planning:**
14. What is the prototype delivery timeline after SOW approval?
15. What is the expected timeline for FPGA development?
16. What technical support is provided during validation?
17. What are unit costs for quantities of 1, 10, 50, 100?

### 8.2 Important Questions (For Planning)

**Timing and Synchronization:**
- What is the latency and jitter for timed command execution?
- What is the phase noise specification for OCXO and synthesized LOs?

**Multi-Unit Sync (Future):**
- What is the architecture for synchronizing multiple Crimson TNG units (>4 channels)?
- What additional hardware is required?
- Are there limitations on the number of units that can be synchronized?

---

## 9. Competitive Positioning

### 9.1 Competitor Comparison

**Legacy Varian DDR (Being Replaced):**
- **Advantages:** Proven NMR performance, well-understood
- **Disadvantages:** Obsolete, unsupportable, no future development
- **Market Position:** End-of-life, refurbished units only

**Current Competitor (Unnamed in Emails):**
- ADC: 240 MSPS, 16-bit
- Dynamic range: 17-19 bit (with decimation)
- Established NMR market presence

**Crimson TNG Advantage:**
- ADC: 325 MSPS (35% faster) → better oversampling for dynamic range
- Amplitude precision: 100× better (0.0015% vs 0.1%)
- Flexible platform: Customization possible
- Modern SDR: Ongoing development and support
- Competitive pricing at volume

### 9.2 Harmonyzer Differentiation Strategy

**Key Differentiators:**
1. **Superior Dynamic Range:** 20-bit ENOB goal exceeds typical competitor specs
2. **Advanced Capabilities:** Modern SDR enables future NMR techniques
3. **Reliability:** New technology vs. refurbished legacy equipment
4. **Support:** Active vendor partnership vs. unsupported obsolete systems
5. **Scalability:** Multi-unit sync for advanced applications (>4 channels)

**Market Message:**
"Resyannt Harmonyzer: Modern SDR technology delivering superior performance, reliability, and support for high-resolution solid-state NMR spectroscopy."

---

## 10. Next Steps and Decision Points

### 10.1 Immediate Actions (This Week - November 2025)

**Resynant:**
1. ✅ Complete requirements documentation (DONE)
2. ⬜ Internal review and approval of specifications
3. ⬜ Submit documentation package to Per Vices (Brandon Malatest)
4. ⬜ Request Per Vices responses to critical questions (Section 8.1)

**Per Vices:**
5. ⬜ Technical review of requirements by engineering team
6. ⬜ Provide responses to critical questions
7. ⬜ Schedule follow-up technical discussion call

### 10.2 Near-Term Actions (2-4 Weeks - December 2025)

**Per Vices:**
1. ⬜ Develop Statement of Work (SOW) with:
   - Detailed technical specifications
   - FPGA development scope and deliverables
   - Validation metrics and acceptance criteria
   - Timeline with milestones
   - Cost breakdown (NRE, prototype, production pricing)
   - Technical support commitment

**Resynant:**
2. ⬜ Review SOW
3. ⬜ Negotiate terms if needed
4. ⬜ Internal budget approval
5. ⬜ **DECISION POINT:** Approve SOW and issue purchase order

### 10.3 Project Kickoff (January 2026)

1. ⬜ Formal project kickoff meeting (Resynant + Per Vices)
2. ⬜ Establish communication channels and regular check-ins
3. ⬜ Confirm technical points of contact
4. ⬜ Begin prototype development (Per Vices)
5. ⬜ Begin software integration development (Resynant)
6. ⬜ Prepare test environment (Resynant)

### 10.4 Key Decision Points

| Decision Point | Timeline | Criteria |
|---------------|----------|----------|
| **SOW Approval** | December 2025 | Cost acceptable; technical feasibility confirmed; timeline reasonable |
| **Prototype Acceptance** | June 2026 | Meets all must-pass validation criteria (Section 7.1) |
| **Production Release** | September 2026 | Software integration complete; production cost confirmed; customer acceptance testing passed |
| **Volume Production** | 2027+ | Market demand validated; unit economics favorable; customer satisfaction metrics met |

---

## 11. Recommendations

### 11.1 Proceed with Per Vices Crimson TNG Development

**Rationale:**
1. ✅ **Excellent technical fit:** Platform architecture aligns with NMR requirements
2. ✅ **Competitive performance:** Meets or exceeds competitor specifications
3. ✅ **Proven platform:** Established SDR with customer base and support
4. ✅ **Manageable risk:** Customization needs well-defined and achievable
5. ✅ **Clear path to production:** Phased approach with validation gates

**Recommendation: PROCEED** with SOW development and prototype program

### 11.2 Phased Implementation Strategy

**Phase 1 (Prototype - Q1-Q2 2026):**
- Baseline Crimson TNG with GPIO expander
- FPGA CIC decimation (if available)
- Waveform streaming via 10GbE
- Validate core functionality and dynamic range
- **Gate:** Prototype acceptance before production commitment

**Phase 2 (Optimization - Q3 2026):**
- FPGA waveform buffering/looping (based on Phase 1 results)
- Advanced features as identified during validation
- Software integration maturity
- **Gate:** Production release approval

**Phase 3 (Production - Q4 2026+):**
- Initial 10-unit deployment
- Customer feedback integration
- Continuous improvement
- Scale to 50-99 units/year

**Rationale:** Phased approach manages risk, allows validation before full commitment, and provides flexibility for optimization.

### 11.3 Resource Commitment

**Resynant Internal:**
- Engineering lead: NMR specialist for validation testing
- Software development: Pulse sequence compiler and data acquisition
- Project management: Timeline and vendor coordination
- Budget: NRE + prototype + initial production units

**Per Vices Partnership:**
- Engineering support: FPGA development and technical troubleshooting
- Documentation: System specifications and user guides
- Validation support: Remote assistance during testing
- Long-term: Ongoing product support and updates

---

## 12. Conclusion

The Per Vices Crimson TNG SDR platform represents an **excellent solution** for modernizing the Resyannt Harmonyzer NMR spectrometer transmitter and receiver systems. The platform's multi-channel phase-coherent architecture, high-performance converters, and flexible FPGA capabilities align exceptionally well with solid-state NMR requirements.

**Key Strengths:**
- Core specifications meet or exceed NMR and competitor benchmarks
- Proven SDR platform with established customer support
- Customization needs are well-defined and achievable
- Clear path from prototype to production deployment

**Areas of Focus:**
- GPIO expander development for TTL compatibility and timing precision
- FPGA CIC decimation for enhanced dynamic range
- Phased validation to confirm performance specifications
- Software integration with Harmonyzer control system

**Timeline:** 11 months from SOW approval to production release (September 2026), with first production units in Q4 2026 - Q1 2027.

**Risk Assessment:** LOW to MODERATE - Well-defined requirements, proven platform, experienced vendors, and phased approach with validation gates.

**Business Impact:** Enables phase-out of legacy Varian technology, positions Resynant for market growth in 2026-2027, and differentiates Harmonyzer product with superior specifications and modern technology.

**Recommendation:** **PROCEED** with Per Vices partnership, SOW development, and prototype program as outlined in this document.

---

## 13. Document Package

This executive summary is supported by detailed technical documentation:

1. **technical_requirements.md** - Comprehensive technical specifications (24 pages)
2. **use_case_scenarios.md** - Operational use cases and data flow (28 pages)
3. **test_validation_plan.md** - Detailed testing procedures and acceptance criteria (34 pages)
4. **requirements_summary.md** - Requirements traceability and gap analysis (22 pages)
5. **nmr_pulse_sequences.md** - Detailed pulse sequence specifications (36 pages)

**Total Documentation:** ~150 pages of comprehensive technical specifications ready for Per Vices engineering review and SOW development.

---

**Prepared by:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

**Date:** November 8, 2025

**Status:** Ready for submission to Per Vices Corporation

**Submitted to:**
Brandon Malatest, COO
Per Vices Corporation
brandon.m@pervices.com
+1 (647) 534-9007

---

## Appendix A: Glossary

**ADC** - Analog-to-Digital Converter
**CP** - Cross-Polarization (magnetization transfer technique)
**CIC** - Cascaded Integrator-Comb (decimation filter)
**DAC** - Digital-to-Analog Converter
**DDR** - Direct Digital Receiver (legacy Varian technology)
**ENOB** - Effective Number of Bits (dynamic range measure)
**FID** - Free Induction Decay (NMR signal)
**FPGA** - Field-Programmable Gate Array
**GPIO** - General Purpose Input/Output
**NF** - Noise Figure
**NMR** - Nuclear Magnetic Resonance
**NRE** - Non-Recurring Engineering (development costs)
**OCXO** - Oven-Controlled Crystal Oscillator
**SDR** - Software-Defined Radio
**SFDR** - Spurious-Free Dynamic Range
**SNR** - Signal-to-Noise Ratio
**SOW** - Statement of Work
**TPPM** - Two-Pulse Phase Modulation (decoupling sequence)
**TTL** - Transistor-Transistor Logic (0-5V digital standard)

---

**End of Executive Summary**
