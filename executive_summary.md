# Executive Summary
## Resynant Harmonyzer NMR Spectrometer SDR Development
### Per Vices Crimson TNG Platform

**Document Version:** 2.0
**Date:** November 20, 2025 (Updated from v1.0, Nov 8, 2025)
**Prepared by:** Resynant, Inc.
**For:** Per Vices Corporation

**Project Status:** Requirements complete, ready for SOW development
**Funding Status:** Secured ($900K PO + $1M Series A)
**Timeline:** 36 weeks to production (August 2026)

---

## 0. Historical Context: Lessons from Previous Approach

### 0.1 Why This Is Attempt #2

This project represents Resynant's **second attempt** to modernize the Harmonyzer NMR platform. Understanding why the first approach failed is critical to avoiding similar pitfalls.

**Previous Attempt: Tabor Proteus AWG + OpenVNMRJ (2023-2024)**

**Approach:**
- Platform: Tabor Proteus Arbitrary Waveform Generator (repurposed for NMR)
- Software: Integration with OpenVNMRJ (open-source Varian software fork)
- Architecture: Complex translation layers (OVJ PSG → UCODE → TEproc → SCPI commands)

**Why It Failed:**

1. **Software Complexity Overload:** Multiple abstraction layers between pulse sequence and hardware
2. **"Unknown Unknowns":** Critical gaps in GPIO, hardware looping, phase cycling remained unresolved
3. **AWG Not Designed for NMR:** Proteus lacked native phase-coherent multi-channel architecture
4. **Legacy Software Burden:** Backward compatibility with OpenVNMRJ limited design flexibility
5. **Vendor Dependency Risk:** Key features required Tabor assistance with unclear feasibility

**Project Status:** Appears to have stalled by mid-2024

### 0.2 Why Per Vices Crimson TNG Approach Is Different (and Better)

**1. Purpose-Built SDR vs. Repurposed AWG**
- Crimson TNG designed for multi-channel phase-coherent applications (radar, communications)
- Factory-calibrated JESD204B synchronization, not retrofitted

**2. Simpler Software Architecture**
- Direct UDP streaming (VITA 49/PVAN-11 standard) - no complex translation layers
- Build fresh software optimized for Crimson TNG, not constrained by legacy OpenVNMRJ

**3. Well-Defined Data Interface**
- PVAN-11 = VITA 49 industry standard (documented, proven)
- Established 10 GbE network streaming vs. uncertain SCPI patterns

**4. Established SDR Platform**
- Proven customer base in similar phase-coherent applications
- Per Vices experience with multi-channel synchronization challenges

**5. Clear Customization Scope**
- GPIO expander: Well-defined electrical/timing requirements
- FPGA CIC decimation: Understood signal processing task
- No fundamental architectural "unknowns" like Tabor approach had

### 0.3 Critical Lessons Applied to This Project

**DO:**
- Keep software architecture simple - minimize abstraction layers
- Build fresh software optimized for platform, not forced legacy integration
- Define clear acceptance criteria and validate incrementally
- Front-load the "unknown unknowns" - identify gaps early in SOW

**DON'T:**
- Create complex translation layers (avoid UCODE → TEproc → SCPI pattern)
- Assume vendor will resolve unclear technical challenges - get specifics in SOW
- Underestimate timeline when "unknowns" are mentioned repeatedly
- Proceed without well-defined data interfaces and control mechanisms

**Warning Signs to Watch For:**
- Per Vices saying "we'll need to investigate how to..." for critical features
- Custom FPGA work scope becoming vague or open-ended
- GPIO timing or data acquisition having "unknowns" after SOW
- Software architecture requiring >3 translation/abstraction layers

---

## 1. Project Overview

### 1.1 Objective

Develop a modern software-defined radio (SDR) transmitter and receiver system for the Resynant Harmonyzer high-resolution solid-state NMR spectrometer platform, replacing legacy refurbished Varian technology with the Per Vices Crimson TNG SDR solution.

**This is Resynant's second modernization attempt.** The previous approach (Tabor Proteus AWG + OpenVNMRJ) failed due to software complexity and unclear vendor capabilities. The Crimson TNG approach addresses these lessons with simpler architecture and proven SDR technology.

### 1.2 Business Context

**Current Situation (November 2025):**
- Resynant currently fulfills customer orders using refurbished legacy Varian DDR technology
- **Major Milestone:** $900K purchase order from Indiana University (600 MHz console)
- **Funding Secured:** $1M Series A financing (closed November 2025)
- **Total Available:** $1.9M for R&D and production deployment
- **Team Committed:** Project manager (Lauren Price), head of R&D (Alex Dreena), CEO/NMR specialist (Chad Rienstra)

**Strategic Importance:**
- Phase out dependence on aging, unsupportable legacy Varian technology
- Enable modern NMR capabilities and improved customer support
- Position Resynant for growth in 2026-2027 market expansion
- Differentiate Harmonyzer product with superior specifications
- **Critical:** Avoid repeating Tabor/OpenVNMRJ failure - simpler architecture required

**Market Opportunity:**
- **Prototype:** 1 unit (February 2026 delivery target)
- **Beta Testing:** Indiana University 600 MHz console (May-June 2026)
- **Initial Production:** 10 units (Q3-Q4 2026)
- **Production Volume:** 50-99 units per year (2027+ ongoing)
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
| **Data Interface** | 10 GbE, VITA 49 standard | SFP+ 10 GbE, PVAN-11 (VITA 49) | ✅ Met |

**Data Interface Details (PVAN-11/VITA 49):**
- **Standard:** VITA 49 (industry-standard RF data format, not proprietary)
- **Per Vices Implementation:** PVAN-11 packet format over UDP/IP
- **I/Q Format:** 32 bits per sample (16-bit signed I + 16-bit signed Q)
- **Transport:** UDP streaming over 10 GbE SFP+
- **Bandwidth Constraint:** 4 channels × 325 MSPS = 41.6 Gbps raw → **FPGA decimation required** to fit 10 GbE
- **Documentation:** https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
- **Implication:** CIC decimation is **mandatory** (not optional) for multi-channel operation

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

### 4.1 Development Phases (REVISED REALISTIC SCHEDULE)

**Note:** This timeline reflects lessons learned from the Tabor project failure. Realistic pacing ensures quality over speed, and includes Indiana University beta testing opportunity.

```
Phase 0: Documentation and SOW (3 weeks)
├─ November 8, 2025       ✓ Requirements documentation complete
├─ November 21, 2025      → Documentation package submitted to Per Vices
├─ November 25-26, 2025   → Technical alignment call
├─ December 6, 2025       → SOW draft received from Per Vices
└─ December 13, 2025      → SOW approval and project kickoff
    Duration: 5 weeks (realistic review and negotiation)

Phase 1: Prototype Development (11 weeks)
├─ Dec 16, 2025 - Jan 10  → Hardware assembly + GPIO expander design (4 weeks)
├─ Jan 13 - Feb 7         → FPGA development + integration (4 weeks)
├─ Feb 10 - Feb 28        → Factory testing and delivery prep (3 weeks)
└─ February 28, 2026      → Prototype delivered to Resynant
    Duration: 11 weeks (includes GPIO expander custom board)
    Deliverable: Crimson TNG prototype with GPIO expander + CIC decimation

Phase 2: Prototype Validation (11 weeks)
├─ Mar 2-13, 2026         → Bench testing (electrical, timing) (2 weeks)
├─ Mar 16 - Apr 10        → NMR integration (400 MHz magnet) (4 weeks)
├─ Apr 13 - May 8         → Multi-channel validation (600 MHz) (4 weeks)
└─ May 15, 2026           → Validation complete, acceptance decision
    Duration: 11 weeks (thorough testing, troubleshooting buffer)
    Deliverable: Test report with pass/fail determination

Phase 3: Beta Testing at Indiana University (NEW - 6 weeks)
├─ May 18 - June 30       → Field testing with beta customer
├─ Side-by-side comparison with legacy Varian system
├─ Real-world usage, reliability testing
└─ Customer feedback collection
    Duration: 6 weeks
    Deliverable: Beta test report, production readiness assessment

Phase 4: Production Readiness (4 weeks)
├─ July 1 - August 1      → FPGA optimization based on validation
├─ Software integration with Harmonyzer production system
├─ Final documentation and training materials
└─ August 1, 2026         → Production release
    Duration: 4 weeks
    Deliverable: Production-ready system

Phase 5: Initial Production Deployment
├─ August 2026            → First production order (10 units)
├─ Sep-Oct 2026           → Production and delivery
└─ Nov-Dec 2026           → Customer installations
    First production units: Q3-Q4 2026
```

**REVISED TIMELINE SUMMARY:**
- Requirements to Production: **36 weeks (8.5 months)**
- Prototype delivery: **February 28, 2026** (+4 weeks vs. original)
- Beta testing: **May-June 2026** (NEW - Indiana University opportunity)
- Production release: **August 1, 2026** (+8 weeks vs. original accelerated plan)
- **First production units: Q3-Q4 2026**

### 4.2 Summary Timeline (REVISED)

| Milestone | Original Plan | Revised Plan | Rationale |
|-----------|--------------|--------------|-----------|
| **SOW Approval** | Nov 29, 2025 | Dec 13, 2025 | +2 weeks (realistic review) |
| **Prototype Delivery** | Jan 31, 2026 | Feb 28, 2026 | +4 weeks (GPIO expander complexity) |
| **Validation Complete** | Mar 31, 2026 | May 15, 2026 | +6 weeks (thorough testing) |
| **Beta Testing** | N/A | Jun 30, 2026 | NEW (Indiana opportunity) |
| **Production Release** | May 31, 2026 | Aug 1, 2026 | +8 weeks (beta feedback integration) |
| **First Production Units** | Jun-Aug 2026 | Sep-Oct 2026 | +2 months |

**Total Time to Production: ~36 weeks from requirements complete**
**Trade-off:** Slower but more thorough - avoids Tabor project pitfalls

### 4.3 Critical Path Items (CURRENT SPRINT: Nov 21-25, 2025)

**THIS WEEK (Nov 21-25): Re-engage Per Vices - HIGHEST PRIORITY**

**Status as of Nov 20, 2025:**
- ✅ Requirements documentation complete (~170 pages)
- ✅ GPIO specifications complete (7 pages, detailed TTL interface requirements)
- ✅ PVAN-11 data format specification downloaded and documented
- ✅ Funding secured ($900K PO + $1M Series A)
- ✅ Team assigned (Chad, Lauren, Alex)

**This Week Actions:**
1. **Documentation Package Submission** (Nov 21)
   - Email to Brandon Malatest with 8 specification documents
   - GPIO_SPECIFICATIONS.md (NEW - addresses Per Vices critical question)
   - pvan11_dataformat_spec.md (NEW - VITA 49 standard documented)
   - **Owner:** Chad Rienstra
   - **Status:** Ready to send

2. **Technical Alignment Call** (Nov 25-26)
   - Review GPIO expander feasibility and timeline
   - Confirm FPGA CIC decimation approach (mandatory for bandwidth)
   - SOW development timeline (target Dec 6 draft, Dec 13 approval)
   - **Owner:** Chad + Lauren

3. **Software Development Kickoff** (Nov 21-24)
   - UDP receiver skeleton code (PVAN-11 packet parsing)
   - Development environment setup (Python/C++)
   - Team briefing (Lauren, Alex)
   - **Owner:** Chad (20 hrs/week software development)

**NEXT 3 WEEKS (Nov 25 - Dec 13): SOW Development**
4. **Per Vices SOW Preparation** (Dec 2-6)
   - GPIO expander specifications and NRE estimate
   - FPGA CIC decimation development plan
   - Prototype delivery timeline (target Feb 28, 2026)
   - Production unit pricing (10-unit and volume tiers)

5. **SOW Review and Approval** (Dec 9-13)
   - Internal review by Chad, Lauren, Alex
   - Negotiation if needed (timeline, pricing, deliverables)
   - Final approval and PO issuance (Dec 13)
   - Project kickoff call (Dec 16)

**DEC 16 - FEB 28: Prototype Development (11 weeks)**
6. **Per Vices Hardware Development**
   - GPIO expander board (custom, TTL 0-5V, ±100ns timing)
   - FPGA CIC decimation filters (mandatory for bandwidth)
   - Crimson TNG assembly and integration
   - Factory testing and validation

7. **Resynant Parallel Activities**
   - Software development: UDP receiver, PVAN-11 parsing (Dec-Jan)
   - Pulse sequence compiler framework (Jan-Feb)
   - Test environment preparation (bench equipment, samples)
   - Magnet scheduling (400 MHz, 600 MHz for Mar-May)

**MAR 2 - MAY 15: Validation Testing (11 weeks)**
8. **Bench Testing** (Mar 2-13, 2 weeks)
   - GPIO timing precision validation
   - Frequency range verification
   - Phase coherency measurement
   - Data throughput testing

9. **NMR Integration** (Mar 16 - Apr 10, 4 weeks)
   - 400 MHz magnet: Basic NMR signal acquisition
   - SNR measurement (adamantane standard)
   - Dynamic range characterization
   - Single-channel optimization

10. **Multi-Channel Validation** (Apr 13 - May 8, 4 weeks)
    - 600 MHz magnet: Advanced NMR techniques
    - Cross-polarization experiments
    - Decoupling performance (TPPM sequences)
    - Complex pulse sequences

**MAY 18 - JUN 30: Beta Testing at Indiana (6 weeks) - NEW PHASE**
11. **Field Testing with Beta Customer**
    - Indiana University 600 MHz console upgrade
    - Side-by-side comparison with legacy Varian
    - Real-world usage and reliability testing
    - Customer feedback collection

**JUL 1 - AUG 1: Production Readiness (4 weeks)**
12. **Final Optimization and Release**
    - FPGA tuning based on validation results
    - Software integration with Harmonyzer production
    - Documentation and training materials
    - First production order (10 units)

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

**Estimated Total Project Cost (Per Vices + Internal):**

| Category | Amount | Notes |
|----------|--------|-------|
| **Per Vices Costs** | $107K-$170K | Prototype + GPIO + FPGA CIC (pending SOW) |
| **Internal Personnel** | $150K-$200K | Chad (20 hrs/week), Lauren (PM), Alex (R&D) |
| **Equipment & Materials** | $25K | Test equipment, samples (mostly in-house) |
| **Software Contractor** | $0-$30K | Optional, if needed for schedule |
| **Beta Testing (Indiana)** | $10K | Travel, support, contingency |
| **Contingency (10%)** | $30K-$40K | Buffer for unexpected issues |
| **TOTAL** | **$322K-$465K** | **Estimated project budget** |

**Funding Status (as of November 2025):**
- ✅ **$900K PO from Indiana University** (600 MHz console)
- ✅ **$1M Series A financing** (closed November 2025)
- ✅ **Total Available: $1.9M** for R&D and production deployment
- ✅ **Budget Risk: LOW** - ample funding available (project ~$400K of $1.9M)

**Decision Point:** SOW review (Dec 6-13) will provide Per Vices actual costs for final budget approval

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

### 10.1 Immediate Actions (THIS WEEK - November 21-25, 2025)

**Status as of Nov 20, 2025:**
- ✅ Requirements documentation complete (~170 pages)
- ✅ GPIO specifications complete (GPIO_SPECIFICATIONS.md, 7 pages)
- ✅ PVAN-11 data format documented (pvan11_dataformat_spec.md)
- ✅ Funding secured ($900K PO + $1M Series A = $1.9M available)
- ✅ Team assigned (Chad, Lauren, Alex)

**This Week Actions:**

**Resynant:**
1. ⬜ **Send email to Per Vices** (Nov 21) - Brandon Malatest
   - Attach all 8 specification documents
   - Request technical alignment call (Nov 25-26)
   - Highlight funding secured and team readiness
2. ⬜ **Software development kickoff** (Nov 21-24)
   - UDP receiver skeleton code (PVAN-11 parsing)
   - Development environment setup
3. ⬜ **Technical alignment call** (Nov 25-26)
   - Review GPIO expander feasibility
   - Confirm FPGA CIC decimation plan (mandatory for bandwidth)
   - SOW timeline discussion

**Per Vices:**
4. ⬜ Review technical documentation package
5. ⬜ Provide feedback on GPIO expander and FPGA CIC approach
6. ⬜ Commit to SOW delivery timeline (target Dec 6)

### 10.2 Near-Term Actions (3 Weeks - Nov 25 - Dec 13, 2025)

**Per Vices:**
1. ⬜ **Develop Statement of Work (SOW)** (target Dec 6):
   - GPIO expander specifications and NRE cost
   - FPGA CIC decimation development plan
   - Prototype delivery timeline (target Feb 28, 2026)
   - Production unit pricing (10-unit and volume tiers)
   - Technical support commitment (weekly calls, on-site during validation)

**Resynant:**
2. ⬜ **Review SOW internally** (Dec 9-11)
   - Technical review by Chad
   - Commercial review by Lauren
   - Budget approval confirmation
3. ⬜ **Negotiate if needed** (Dec 11-12)
4. ⬜ **DECISION POINT: Approve SOW and issue PO** (Dec 13)

### 10.3 Project Kickoff (December 16, 2025)

1. ⬜ Formal project kickoff meeting (Resynant + Per Vices)
2. ⬜ Establish weekly status calls (every Monday, 10:00 AM Central)
3. ⬜ Confirm technical points of contact (Per Vices: Lead Engineer, PM)
4. ⬜ Begin prototype development (Per Vices: GPIO expander, FPGA CIC)
5. ⬜ Continue software development (Resynant: UDP receiver, pulse compiler)
6. ⬜ Finalize test environment preparation plan

### 10.4 Key Decision Points (Revised Timeline)

| Decision Point | Timeline | Criteria |
|---------------|----------|----------|
| **SOW Approval** | Dec 13, 2025 | Cost ≤$170K (Per Vices); technical feasibility confirmed; Feb 28 delivery commitment |
| **Prototype Acceptance** | May 15, 2026 | Meets all must-pass validation criteria (Section 7.1) |
| **Beta Testing Approval** | May 18, 2026 | Prototype passes; Indiana customer agrees to beta program |
| **Production Release** | Aug 1, 2026 | Beta testing successful; software integration complete; production cost confirmed |
| **Volume Production** | 2027+ | 10-unit deployment successful; customer satisfaction; unit economics favorable |

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

The Per Vices Crimson TNG SDR platform represents an **excellent solution** for modernizing the Resynant Harmonyzer NMR spectrometer transmitter and receiver systems. **This is Resynant's second modernization attempt** - lessons learned from the failed Tabor Proteus/OpenVNMRJ approach (2023-2024) directly inform this project's simpler, more pragmatic architecture.

**Why This Approach Will Succeed (Unlike Tabor):**
- **Purpose-built SDR** (not repurposed AWG) with native phase-coherent multi-channel design
- **Simpler software architecture:** Direct UDP streaming (VITA 49/PVAN-11) vs. complex translation layers
- **Well-defined data interface:** Industry-standard VITA 49, documented and proven
- **No "unknown unknowns":** GPIO expander and FPGA CIC are understood tasks, not vendor dependencies
- **Clear acceptance criteria:** Defined upfront in SOW, validated incrementally

**Key Strengths:**
- Core specifications meet or exceed NMR and competitor benchmarks
- Proven SDR platform with established customer support (radar, communications applications)
- Customization needs are well-defined and achievable (GPIO expander, FPGA CIC decimation)
- Clear path from prototype to production deployment
- **Funding secured:** $1.9M available ($900K PO + $1M Series A)
- **Team committed:** Chad (NMR specialist + software), Lauren (PM), Alex (R&D)

**Critical Success Factors:**
- **GPIO expander:** Custom board for TTL compatibility (0-5V) and ±100ns timing precision
- **FPGA CIC decimation:** **Mandatory** for bandwidth (41.6 Gbps → 10 GbE requires decimation)
- **Phased validation:** Thorough testing (11 weeks) with troubleshooting buffer
- **Beta testing:** Indiana University field deployment (May-June 2026) before full production
- **Software simplicity:** Avoid complex abstraction layers that killed Tabor project

**Timeline:** **36 weeks (8.5 months)** from requirements complete to production release (August 2026)
- Prototype delivery: February 28, 2026
- Validation complete: May 15, 2026
- Beta testing: May 18 - June 30, 2026
- Production release: August 1, 2026
- First production units: Q3-Q4 2026

**Risk Assessment:** **LOW to MODERATE**
- Well-defined requirements and proven SDR platform
- Adequate funding ($1.9M >> $400K project budget)
- Lessons learned from Tabor failure applied
- Phased approach with validation gates and beta testing
- **Watch for:** Per Vices "unknowns" on critical features, FPGA scope creep, software complexity growth

**Business Impact:**
- Enables phase-out of unsupportable legacy Varian technology
- Positions Resynant for market growth (50-99 units/year production)
- Differentiates Harmonyzer with superior specifications (20-bit ENOB, modern SDR)
- De-risks technology roadmap with proven vendor partnership

**Recommendation:** **PROCEED** with Per Vices partnership, SOW development, and prototype program as outlined in this document.

**Next Action (Nov 21):** Send documentation package to Brandon Malatest (Per Vices COO) to initiate SOW development.

---

## 13. Document Package

This executive summary is supported by detailed technical documentation:

**Core Technical Specifications (~170 pages total):**
1. **executive_summary.md** - This document (business case, timeline, budget, lessons learned)
2. **technical_requirements.md** - Comprehensive technical specifications (24 pages)
3. **requirements_summary.md** - Requirements traceability and gap analysis (22 pages)
4. **use_case_scenarios.md** - Operational use cases and data flow (28 pages)
5. **test_validation_plan.md** - Detailed testing procedures and acceptance criteria (34 pages)
6. **nmr_pulse_sequences.md** - Detailed pulse sequence specifications for FPGA (36 pages)

**New Documents (November 2025):**
7. **GPIO_SPECIFICATIONS.md** - Complete GPIO TTL interface requirements (7 pages)
   - 8-12-16 GPIO configurations
   - Electrical specifications (0-5V TTL, ±100ns timing)
   - Functional requirements (TX/RX gating, external triggers)
8. **pvan11_dataformat_spec.md** - VITA 49 data format specification
   - UDP packet structure (PVAN-11 = VITA 49 standard)
   - I/Q data format (32 bits per sample, 16-bit signed I+Q)
   - Bandwidth constraint analysis (41.6 Gbps → 10 GbE requires FPGA decimation)
9. **REVISED_PROJECT_TIMELINE.md** - Realistic 36-week timeline (Aug 2026 production)
10. **4_DAY_SPRINT_GUIDE.md** - Implementation guide (Nov 21-24 software kickoff)

**Supporting Materials:**
- **IMMEDIATE_ACTIONS.md** - Original accelerated timeline action items (reference)
- **MILESTONE_STRATEGY_ANALYSIS.md** - Analysis of Tabor project failure (lessons learned)
- **email_threads_with_pervices.txt** - Historical communication with Per Vices
- **Case Studies:** GPS/GNSS, Napatech, Radar, Spectrum (Per Vices application examples)

**Total Documentation:** ~200+ pages ready for Per Vices engineering review and SOW development.

**Submission Package (8 core documents to send Nov 21):**
1. executive_summary.md
2. technical_requirements.md
3. requirements_summary.md
4. use_case_scenarios.md
5. test_validation_plan.md
6. nmr_pulse_sequences.md
7. GPIO_SPECIFICATIONS.md (NEW)
8. REVISED_PROJECT_TIMELINE.md

---

**Prepared by:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

**Version History:**
- v1.0: November 8, 2025 - Initial requirements documentation
- v2.0: November 20, 2025 - Updated with historical context, revised timeline, PVAN-11 spec, funding status

**Status:** Ready for submission to Per Vices Corporation (Nov 21, 2025)

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
