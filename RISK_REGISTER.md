# RISK REGISTER
## NMR Spectrometer SDR Development Project
### Per Vices Crimson TNG Platform for Resynant Harmonyzer

**Document Version:** 1.0
**Date:** November 20, 2025
**Project Duration:** November 2025 - June 2026
**Last Updated:** November 20, 2025

---

## EXECUTIVE SUMMARY

**Total Identified Risks:** 35
**Critical Risks (High Impact + High/Medium Probability):** 8
**Overall Project Risk Rating:** MEDIUM

### Risk Distribution by Category
- **Technical Risks:** 12 risks
- **Schedule Risks:** 10 risks
- **Business/Financial Risks:** 7 risks
- **Resource Risks:** 6 risks

### Risk Severity Breakdown
- **Critical (High Impact + High/Medium Prob):** 8 risks (23%)
- **Significant (Medium Impact + Medium Prob):** 12 risks (34%)
- **Moderate (Low-Medium combinations):** 15 risks (43%)

---

## RISK ASSESSMENT MATRIX

### Probability Definitions
- **High (H):** >60% likelihood of occurring
- **Medium (M):** 30-60% likelihood of occurring
- **Low (L):** <30% likelihood of occurring

### Impact Definitions
- **High (H):** >4 weeks schedule delay OR >$100K cost increase OR project failure
- **Medium (M):** 2-4 weeks schedule delay OR $25K-$100K cost increase OR major rework
- **Low (L):** <2 weeks schedule delay OR <$25K cost increase OR minor adjustments

### Risk Priority Matrix

```
                    IMPACT
                LOW     MEDIUM      HIGH
PROBABILITY
    HIGH        M        H          C
    MEDIUM      L        M          H
    LOW         L        L          M

Legend: C = Critical, H = High, M = Moderate, L = Low
```

---

## CRITICAL RISKS (Priority 1)

### CR-01: SOW Negotiation Extends Beyond November 29
**Category:** Schedule
**Probability:** Medium (40%)
**Impact:** High (pushes all downstream activities)
**Risk Score:** 8/10
**Phase:** Phase 0 (Requirements & SOW)

**Description:**
SOW negotiations with Per Vices extend beyond the November 29 deadline due to technical disagreements, pricing disputes, or internal approval delays.

**Impact Analysis:**
- Every week of delay pushes prototype delivery by 1 week
- Pushes validation into April (conflicts with magnet scheduling)
- May miss May 31 production release target
- Potential customer order delays

**Mitigation Strategies:**
1. **Proactive (Before Risk Occurs):**
   - Submit complete documentation package by November 11 (DONE)
   - Pre-negotiate key terms during technical alignment call (Nov 18-19)
   - Prepare fallback positions on non-critical requirements
   - Secure executive approval authority in advance

2. **Reactive (If Risk Occurs):**
   - Daily escalation calls with Per Vices leadership
   - Accept minor compromises on non-critical items
   - Parallel-path: Begin internal software development regardless
   - Compress downstream phases to recover time

**Owner:** CEO (Chad Rienstra)
**Monitoring Trigger:** If SOW not received by Nov 22, escalate immediately
**Contingency Budget:** $0 (schedule compression may cost $20K-$50K later)

---

### CR-02: Prototype Delivery Delayed Beyond January 31
**Category:** Schedule/Technical
**Probability:** Medium (35%)
**Impact:** High (delays validation, production release)
**Risk Score:** 7/10
**Phase:** Phase 1 (Prototype Development)

**Description:**
Per Vices cannot deliver prototype by January 31 due to GPIO expander complexity, FPGA development delays, component shortages, or factory testing issues.

**Impact Analysis:**
- Each week of delay reduces validation time (magnet access fixed Feb-Mar)
- May require compressed validation (higher risk of missing issues)
- Pushes production release beyond May 31
- Delays first customer deployments

**Mitigation Strategies:**
1. **Proactive:**
   - Include delivery date as hard requirement in SOW with penalties
   - Offer schedule performance bonus ($5K on-time, $7.5K early)
   - Request priority production slot at Per Vices
   - Weekly status calls to identify issues early
   - 50% deposit to secure priority treatment

2. **Reactive:**
   - Accept partial delivery (e.g., hardware without GPIO expander)
   - Work with Per Vices to expedite shipping (air freight)
   - Negotiate extended magnet access into April if needed (+$5K cost)
   - Compress validation testing to 6 weeks instead of 8

**Owner:** Project Manager + Per Vices PM
**Monitoring Trigger:** Weekly progress <12.5% per week during Dec-Jan
**Contingency Budget:** $10K (expedited shipping, extended magnet time)

---

### CR-03: GPIO Timing Precision Insufficient (<100ns)
**Category:** Technical
**Probability:** Medium (30%)
**Impact:** High (fails acceptance criteria)
**Risk Score:** 7/10
**Phase:** Phase 1-2 (Development & Validation)

**Description:**
GPIO expander board cannot achieve ±100 ns timing precision required for high-power RF amplifier gating, resulting in timing jitter >50 ns or inter-channel skew >100 ns.

**Impact Analysis:**
- Fails GPIO acceptance criteria (Section 7.1, #3)
- May require hardware redesign (adds 4-6 weeks)
- Could necessitate external timing synchronizer (adds $15K+ cost)
- RF amplifier instability may degrade NMR performance

**Mitigation Strategies:**
1. **Proactive:**
   - Require Per Vices to validate timing precision before delivery
   - Include timing validation data in factory test report
   - Request FPGA timing optimization during development
   - Design review of GPIO expander schematic

2. **Reactive:**
   - Relax requirement to ±200 ns if NMR performance acceptable
   - Implement software timing correction algorithms
   - Use external precision timing board (e.g., SpinCore PulseBlaster)
   - Optimize FPGA clock domain crossing

**Owner:** Per Vices Hardware Engineer (development), Resynant NMR Specialist (validation)
**Monitoring Trigger:** Factory test timing measurements >80 ns jitter
**Contingency Budget:** $20K (external timing board if needed)

---

### CR-04: Dynamic Range Below 17-bit ENOB Target
**Category:** Technical
**Probability:** Medium (35%)
**Impact:** High (fails acceptance criteria)
**Risk Score:** 7/10
**Phase:** Phase 2 (Validation)

**Description:**
Measured ENOB at 5 MHz bandwidth falls below 17-bit minimum requirement due to ADC nonlinearity, CIC filter artifacts, phase noise, or RF interference.

**Impact Analysis:**
- Fails dynamic range acceptance criteria (Section 7.1, #2)
- Cannot detect weak signals in presence of strong solvent peaks
- May require extensive FPGA rework or 32-bit float processing
- Competitive disadvantage vs. existing NMR systems

**Mitigation Strategies:**
1. **Proactive:**
   - Validate CIC filter design in simulation before implementation
   - Request Per Vices ADC linearity specifications
   - Plan for aggressive decimation (320 MSPS → 10 MHz)
   - Optimize FPGA filter coefficients

2. **Reactive:**
   - Accept 16-bit ENOB with plan for FPGA optimization in Phase 3
   - Implement host-side 32-bit float processing (adds latency)
   - Use multiple acquisitions with averaging (increases scan time)
   - Explore hardware modifications (better ADC front-end)

**Owner:** Per Vices FPGA Engineer (development), Resynant NMR Specialist (validation)
**Monitoring Trigger:** SNR measurements during Phase 2 validation
**Contingency Budget:** $30K (32-bit FPGA development if needed)

---

### CR-05: First NMR Signal Acquisition Fails
**Category:** Technical
**Probability:** Low (15%)
**Impact:** Critical (project viability at risk)
**Risk Score:** 6/10
**Phase:** Phase 2 (Validation Week 3)

**Description:**
Cannot acquire meaningful NMR signal from adamantane standard sample during initial system integration testing (Feb 15-20), indicating fundamental system issues.

**Impact Analysis:**
- Indicates critical integration problem (phase coherency, RF chain, data path)
- Requires extensive troubleshooting (may add 2-4 weeks)
- May require Per Vices on-site support (travel costs, schedule)
- Could delay project by 1-2 months if hardware rework needed

**Mitigation Strategies:**
1. **Proactive:**
   - Thorough bench testing before NMR magnet integration (Phase 1 validation)
   - Per Vices factory testing includes loopback RF tests
   - Have backup probe and known-good RF amplifier available
   - Prepare systematic troubleshooting flowchart

2. **Reactive:**
   - Immediate Per Vices engineer call (remote support)
   - Request Per Vices on-site visit if needed (5 days)
   - Parallel troubleshooting: RF chain, data acquisition, timing
   - Fall back to simpler test (just Tx, just Rx, single channel)

**Owner:** Resynant NMR Specialist (lead troubleshooting) + Per Vices Engineer (support)
**Monitoring Trigger:** No signal or SNR <5:1 on adamantane
**Contingency Budget:** $15K (Per Vices on-site support, travel)

---

### CR-06: NMR Magnet Access Unavailable Feb-March
**Category:** Resource/Schedule
**Probability:** Low (20%)
**Impact:** High (cannot validate prototype)
**Risk Score:** 6/10
**Phase:** Phase 2 (Validation)

**Description:**
NMRFAM or Indiana University cannot provide 8 consecutive weeks of magnet access during February-March 2026 validation window due to prior commitments or equipment issues.

**Impact Analysis:**
- Cannot perform NMR validation testing (weeks 13-20)
- Pushes validation to March-April or later
- Delays prototype acceptance decision
- Delays production release (May 31 at risk)

**Mitigation Strategies:**
1. **Proactive:**
   - **CRITICAL: Reserve magnet time by November 15 (Week 1)**
   - Book both primary (NMRFAM) and backup (Indiana U) facilities
   - Flexible scheduling: accept Feb 15-Apr 15 window if needed
   - Negotiate priority access with Indiana U customer (quid pro quo)

2. **Reactive:**
   - Identify tertiary facility (Purdue, Ohio State, other customers)
   - Accept split validation: 4 weeks in Feb + 4 weeks in Apr
   - Compressed validation schedule (6 weeks instead of 8)
   - Transport equipment between facilities if needed

**Owner:** Lab Manager (booking), CEO (customer negotiations)
**Monitoring Trigger:** No confirmed reservation by November 20
**Contingency Budget:** $8K (backup facility rental if needed)

---

### CR-07: Prototype Fails Overall Acceptance Criteria
**Category:** Technical/Business
**Probability:** Low (20%)
**Impact:** Critical (project failure)
**Risk Score:** 6/10
**Phase:** Phase 2 (Validation Conclusion)

**Description:**
Prototype fails to meet minimum acceptance criteria (Section 7.1) on March 31, resulting in rejection and requiring major rework or redesign.

**Impact Analysis:**
- Project delays by 3-6 months (rework cycle)
- Additional NRE costs ($50K-$150K)
- Customer order delays and potential cancellations
- Reputational risk with Per Vices and customers
- May need to continue with legacy Varian systems

**Mitigation Strategies:**
1. **Proactive:**
   - Crystal-clear acceptance criteria in SOW (objective, measurable)
   - Per Vices factory testing validates key specifications
   - Weekly status calls during development to catch issues early
   - Phased validation: pass Phase 1 before Phase 2, etc.

2. **Reactive:**
   - Conditional acceptance with remediation plan (specify fixes)
   - Accept prototype for "must-have" criteria, defer "nice-to-have"
   - Negotiate Phase 3 FPGA optimization to address deficiencies
   - Parallel-path: Continue with Varian while Per Vices remediates

**Owner:** CEO (acceptance decision) + Technical Lead (evaluation)
**Monitoring Trigger:** Any "must-pass" criteria failed during validation
**Contingency Budget:** $100K (rework costs, extended validation)

---

### CR-08: Key Personnel Unavailable During Critical Phases
**Category:** Resource
**Probability:** Low (25%)
**Impact:** High (delays validation, compromises quality)
**Risk Score:** 6/10
**Phase:** All phases (especially Phase 2)

**Description:**
NMR Specialist, Software Engineer, or other key personnel unavailable during critical project phases (illness, resignation, competing priorities).

**Impact Analysis:**
- Validation testing requires expert NMR knowledge (cannot substitute easily)
- Software integration delays if engineer unavailable
- Loss of project knowledge and continuity
- May extend timeline by 2-4 weeks per person

**Mitigation Strategies:**
1. **Proactive:**
   - **Confirm availability commitments in writing (Nov 12)**
   - Cross-train secondary personnel on critical tasks
   - Document all procedures and knowledge (wiki, videos)
   - Identify external consultants as backup (e.g., Phoenix NMR)

2. **Reactive:**
   - Hire contract NMR specialist ($200/hr, 2-week engagement = $16K)
   - Engage external software developer for integration work
   - Request Per Vices extended support during validation
   - Delay non-critical activities to focus resources

**Owner:** Project Manager (resource planning) + CEO (backup approvals)
**Monitoring Trigger:** Key person absence >5 consecutive days
**Contingency Budget:** $25K (contract specialists)

---

## HIGH RISKS (Priority 2)

### HR-01: FPGA CIC Decimation More Complex Than Estimated
**Category:** Technical/Schedule
**Probability:** Medium (40%)
**Impact:** Medium (2-3 week delay, $20K-$40K NRE)
**Risk Score:** 6/10
**Phase:** Phase 1 (FPGA Development)

**Description:**
CIC decimation filter development requires more FPGA resources, development time, or testing than Per Vices estimated in SOW.

**Mitigation:**
- **Proactive:** Confirm FPGA resource availability in SOW, request detailed design plan
- **Reactive:** Fallback to host-side decimation (acceptable for Phase 1), defer FPGA CIC to Phase 3
- **Owner:** Per Vices FPGA Engineer
- **Contingency Budget:** $30K (additional FPGA NRE)

---

### HR-02: Waveform Streaming Latency/Jitter Excessive
**Category:** Technical
**Probability:** Medium (40%)
**Impact:** Medium (degrades decoupling performance)
**Risk Score:** 6/10
**Phase:** Phase 2 (Validation)

**Description:**
10GbE waveform streaming exhibits latency >1 ms or jitter >100 μs, causing decoupling artifacts or timing errors.

**Mitigation:**
- **Proactive:** Characterize streaming performance during bench testing (Phase 1)
- **Reactive:** Implement FPGA waveform buffering in Phase 3 (planned enhancement)
- **Owner:** Software Engineer + Per Vices
- **Contingency Budget:** $15K (FPGA buffering development)

---

### HR-03: Cross-Polarization (CP) Performance Below Target
**Category:** Technical
**Probability:** Medium (35%)
**Impact:** Medium (advanced NMR capability degraded)
**Risk Score:** 5/10
**Phase:** Phase 2 (Multi-Channel Validation)

**Description:**
CP enhancement <2× target due to phase stability issues, power control, or Hartmann-Hahn matching difficulties.

**Mitigation:**
- **Proactive:** Systematic CP optimization procedures, software-assisted matching
- **Reactive:** Accept lower CP performance (not in must-pass criteria), optimize in Phase 3
- **Owner:** NMR Specialist
- **Contingency Budget:** $5K (extended optimization time)

---

### HR-04: Software Integration with Harmonyzer Delays
**Category:** Schedule/Technical
**Probability:** Medium (40%)
**Impact:** Medium (2-3 week delay in Phase 3)
**Risk Score:** 5/10
**Phase:** Phase 3 (Production Readiness)

**Description:**
Integrating Crimson TNG with Harmonyzer control system more complex than anticipated due to API incompatibilities or architectural issues.

**Mitigation:**
- **Proactive:** Modular software architecture, early API testing with simulator
- **Reactive:** Phased integration (core functionality first, advanced features deferred)
- **Owner:** Software Engineer
- **Contingency Budget:** $15K (contract developer if needed)

---

### HR-05: Production Units Quality Issues
**Category:** Technical/Business
**Probability:** Low (25%)
**Impact:** Medium (delays customer deployments)
**Risk Score:** 4/10
**Phase:** Phase 4 (Production)

**Description:**
First production units exhibit quality issues not seen in prototype (manufacturing variations, assembly errors).

**Mitigation:**
- **Proactive:** Detailed production QA procedures, incoming inspection at Resynant
- **Reactive:** Return defective units to Per Vices, delay customer shipments 2-3 weeks
- **Owner:** Resynant QA + Per Vices Production
- **Contingency Budget:** $20K (rework, shipping)

---

### HR-06: Budget Approval Delayed or Reduced
**Category:** Business/Schedule
**Probability:** Low (20%)
**Impact:** Medium (delays project start or limits scope)
**Risk Score:** 4/10
**Phase:** Phase 0 (SOW Approval)

**Description:**
Executive/board approval for $500K budget delayed beyond November 13 or approved at reduced level ($400K).

**Mitigation:**
- **Proactive:** Strong ROI justification, present Indiana U order as funding source
- **Reactive:** Phased budget approval ($200K prototype + $300K production), defer optional features
- **Owner:** CEO
- **Contingency:** Accept reduced scope (no FPGA optimization in Phase 3)

---

### HR-07: Per Vices Resource Constraints
**Category:** Resource/Schedule
**Probability:** Medium (30%)
**Impact:** Medium (2-4 week prototype delay)
**Risk Score:** 5/10
**Phase:** Phase 1 (Prototype Development)

**Description:**
Per Vices engineering team overcommitted, cannot dedicate resources to meet January 31 delivery.

**Mitigation:**
- **Proactive:** SOW includes resource commitment and priority treatment (50% deposit)
- **Reactive:** Escalate to Per Vices COO (Brandon Malatest), offer schedule bonus
- **Owner:** Project Manager + CEO
- **Contingency Budget:** $7.5K (schedule bonus payment)

---

### HR-08: Test Equipment Procurement Delays
**Category:** Resource/Schedule
**Probability:** Low (20%)
**Impact:** Medium (delays bench testing 1-2 weeks)
**Risk Score:** 3/10
**Phase:** Phase 0-1 (Preparation)

**Description:**
Cannot procure or rent oscilloscope, spectrum analyzer, or other test equipment by February 1 validation start.

**Mitigation:**
- **Proactive:** Inventory existing equipment and order missing items by November 15
- **Reactive:** Rent equipment with expedited delivery (+$500-$1,000), borrow from university
- **Owner:** Lab Manager
- **Contingency Budget:** $5K (expedited rental)

---

### HR-09: Customer Site Installation Challenges
**Category:** Business/Schedule
**Probability:** Medium (40%)
**Impact:** Low (delays individual deployments 1-2 weeks)
**Risk Score:** 4/10
**Phase:** Phase 4 (Production Deployment)

**Description:**
Customer sites not ready for installation (power, cooling, magnet integration) or unexpected compatibility issues.

**Mitigation:**
- **Proactive:** Detailed site surveys 4 weeks before installation, pre-ship checklist
- **Reactive:** Delay specific customer installations, prioritize ready sites first
- **Owner:** Installation Team + Production Manager
- **Contingency Budget:** $10K (repeat site visits, extended support)

---

### HR-10: Competitor Releases Superior Product
**Category:** Business/Market
**Probability:** Low (15%)
**Impact:** Medium (market pressure, pricing erosion)
**Risk Score:** 3/10
**Phase:** Ongoing

**Description:**
Competitor releases NMR SDR with superior specifications (better ENOB, lower cost) during development phase.

**Mitigation:**
- **Proactive:** Crimson TNG competitive specs (325 MSPS vs 240 MSPS), rapid deployment timeline
- **Reactive:** Emphasize Resynant support/customization advantage, adjust pricing if needed
- **Owner:** CEO (market strategy)
- **Contingency:** Accept lower margins or accelerate feature development

---

## MODERATE RISKS (Priority 3)

### MR-01: Test Sample Delivery Delays
**Category:** Resource
**Probability:** Low (15%)
**Impact:** Low (1 week validation delay)
**Risk Score:** 2/10
**Phase:** Phase 0-2

**Description:** NMR test samples (adamantane, glycine, alanine) not delivered by January 31.

**Mitigation:**
- Order samples by November 13 (3-week lead time)
- Use alternate samples available in-house if needed
- **Owner:** Lab Manager

---

### MR-02: Documentation Incomplete at Production Release
**Category:** Schedule/Quality
**Probability:** Medium (30%)
**Impact:** Low (delays training, not critical path)
**Risk Score:** 3/10
**Phase:** Phase 3

**Description:** User manuals, SOPs, troubleshooting guides not complete by May 31.

**Mitigation:**
- Parallel documentation development during Phase 2-3
- Accept draft documentation for production release, finalize in Phase 4
- **Owner:** Technical Writer / PM

---

### MR-03: Network Infrastructure Issues
**Category:** Technical
**Probability:** Low (20%)
**Impact:** Low (minor performance degradation)
**Risk Score:** 2/10
**Phase:** Phase 2-3

**Description:** 10GbE network performance issues (dropped packets, latency) due to switch configuration or cabling.

**Mitigation:**
- Use quality Cat6a/Cat7 cables, configure switch for jumbo frames
- Dedicated 10GbE network for Crimson TNG (isolated from other traffic)
- **Owner:** Software Engineer + Lab Technician

---

### MR-04: FPGA Optimization Not Completed in Phase 3
**Category:** Schedule
**Probability:** Medium (35%)
**Impact:** Low (defer to post-production)
**Risk Score:** 3/10
**Phase:** Phase 3

**Description:** FPGA waveform looping or optimization features not completed by May 31.

**Mitigation:**
- Not on critical path; waveform streaming acceptable for production
- Defer optimization to Phase 4 or beyond
- **Owner:** Per Vices FPGA Engineer

---

### MR-05: Training Materials Insufficient
**Category:** Quality
**Probability:** Low (20%)
**Impact:** Low (extended customer training time)
**Risk Score:** 2/10
**Phase:** Phase 3-4

**Description:** Training materials (videos, presentations, hands-on exercises) incomplete or inadequate for customer training.

**Mitigation:**
- On-the-job training during first installations
- Develop materials iteratively based on customer feedback
- **Owner:** Technical Writer + NMR Specialist

---

### MR-06: Volume Pricing Negotiation Unfavorable
**Category:** Business
**Probability:** Low (25%)
**Impact:** Medium (higher unit costs)
**Risk Score:** 3/10
**Phase:** Phase 4

**Description:** Per Vices volume pricing for 50-99 units/year less favorable than expected, impacting Harmonyzer margins.

**Mitigation:**
- Negotiate volume pricing during SOW phase
- Consider alternative suppliers for future generations if pricing unacceptable
- **Owner:** CEO

---

### MR-07: Intellectual Property Concerns
**Category:** Legal/Business
**Probability:** Low (10%)
**Impact:** Medium (licensing costs or restrictions)
**Risk Score:** 2/10
**Phase:** Phase 3-4

**Description:** IP ownership questions regarding custom FPGA firmware or software developed jointly with Per Vices.

**Mitigation:**
- Clarify IP ownership in SOW (Resynant owns software, Per Vices owns FPGA)
- Ensure perpetual license for FPGA firmware with production units
- **Owner:** CEO + Legal

---

### MR-08: Regulatory/Compliance Issues
**Category:** Legal
**Probability:** Low (10%)
**Impact:** Low (documentation, minor delays)
**Risk Score:** 1/10
**Phase:** Phase 4

**Description:** Unexpected FCC, CE, or other regulatory compliance requirements for Crimson TNG in NMR configuration.

**Mitigation:**
- Per Vices Crimson TNG already certified (standard product)
- NMR configuration uses same frequency ranges
- **Owner:** Per Vices (compliance), Resynant (documentation)

---

### MR-09: Currency Exchange Rate Fluctuations
**Category:** Financial
**Probability:** Medium (40% - if Per Vices prices in CAD)
**Impact:** Low (<$10K impact on $500K budget)
**Risk Score:** 3/10
**Phase:** All

**Description:** USD/CAD exchange rate fluctuations impact Per Vices pricing (if quoted in Canadian dollars).

**Mitigation:**
- Request pricing in USD to fix costs
- If CAD pricing, include 10% buffer in budget
- **Owner:** Procurement

---

### MR-10: Shipping Damage or Loss
**Category:** Logistics
**Probability:** Low (5%)
**Impact:** Medium (2-3 week replacement delay)
**Risk Score:** 2/10
**Phase:** Phase 1, Phase 4

**Description:** Prototype or production units damaged or lost during shipping between Per Vices (Canada) and Resynant (USA).

**Mitigation:**
- Insurance on all shipments (included in shipping costs)
- Proper packaging per Per Vices standards
- Expedited replacement if damage occurs
- **Owner:** Per Vices Logistics + Resynant Receiving

---

### MR-11: Per Vices Acquisition or Business Disruption
**Category:** Business Continuity
**Probability:** Low (5%)
**Impact:** High (major project disruption)
**Risk Score:** 3/10
**Phase:** Ongoing

**Description:** Per Vices acquired by competitor, goes out of business, or experiences major disruption affecting support.

**Mitigation:**
- Low probability given Per Vices track record
- SOW includes support commitments through 2027
- Resynant gains knowledge to self-support during Phase 2-3
- **Owner:** CEO (monitoring)

---

### MR-12: Customer Order Cancellations
**Category:** Business
**Probability:** Low (10%)
**Impact:** Medium (reduced production volume)
**Risk Score:** 2/10
**Phase:** Phase 4

**Description:** Anticipated customer orders (10 units in 12 months) do not materialize due to budget cuts or market changes.

**Mitigation:**
- 2 customers × 2 units already committed (4 units secured)
- Indiana U large order provides pipeline
- Flexible production schedule (manufacture on demand)
- **Owner:** CEO (sales pipeline management)

---

### MR-13: Long-Term Phase Stability Issues
**Category:** Technical
**Probability:** Low (15%)
**Impact:** Low (requires recalibration procedures)
**Risk Score:** 2/10
**Phase:** Phase 2 validation, Phase 4 field operations

**Description:** Phase stability degrades over hours/days due to temperature drift or OCXO aging.

**Mitigation:**
- 24-hour stability test during Phase 4 validation (Test 6.2.2)
- Software phase tracking/correction algorithms
- Periodic recalibration procedures in user manual
- **Owner:** NMR Specialist (testing), Software Engineer (correction algorithms)

---

### MR-14: Knowledge Transfer from Validation to Production
**Category:** Process
**Probability:** Low (20%)
**Impact:** Low (inefficiencies, relearning)
**Risk Score:** 2/10
**Phase:** Phase 2 → Phase 3 transition

**Description:** Lessons learned during validation not effectively transferred to production engineering team.

**Mitigation:**
- Comprehensive validation report (includes recommendations)
- Transition meeting in early April (Week 21)
- Production team shadows validation team during Phase 2
- **Owner:** Project Manager

---

### MR-15: Multi-Unit Synchronization Challenges (Future)
**Category:** Technical (Future Risk)
**Probability:** Low (20% if >4 channel systems ordered)
**Impact:** Medium (requires additional development)
**Risk Score:** 2/10
**Phase:** Post-Phase 4 (future orders)

**Description:** Future customers require >4 channels, necessitating multi-unit Crimson TNG synchronization which has not been validated.

**Mitigation:**
- 95% of applications use ≤4 channels (low near-term probability)
- Per Vices has indicated multi-unit sync capability
- Address in future project if orders materialize
- **Owner:** CEO (future business decisions)

---

## RISK MONITORING & REPORTING

### Weekly Risk Review Process
**Frequency:** Weekly during status calls (Mondays, 10:00 AM EST)
**Attendees:** Project Manager, CEO (as needed), Per Vices PM
**Duration:** 10 minutes of each status call

**Agenda:**
1. Review top 5 risks (CR-01 through CR-05)
2. Update probabilities based on current status
3. Identify new risks or escalate emerging issues
4. Verify mitigation actions in progress
5. Update risk register document

### Risk Escalation Triggers

**Immediate Escalation to CEO:**
- Any critical risk probability increases to >50%
- Any new critical risk identified
- Two or more high risks occur simultaneously
- Project delay >2 weeks forecasted
- Cost overrun >$50K forecasted

**Escalation to Per Vices COO:**
- Per Vices delivery date at risk
- Technical issues requiring executive intervention
- Resource constraints impacting timeline

### Monthly Executive Risk Summary
**Frequency:** Last Friday of each month
**Attendees:** CEO (Resynant), COO (Per Vices)
**Format:** 1-page risk summary dashboard

**Contents:**
- Risk distribution by category (chart)
- Top 5 risks with status
- Risks closed since last month
- New risks identified
- Overall project risk rating trend

---

## RISK CONTINGENCY BUDGET

### Allocated Contingency: $60,000 (12% of $500K budget)

**Reserve Allocation by Risk Category:**
- **Technical Risks:** $40,000 (67%)
  - FPGA development overruns: $20K
  - GPIO timing issues: $10K
  - Dynamic range remediation: $10K

- **Schedule Risks:** $10,000 (17%)
  - Expedited shipping: $3K
  - Extended magnet time: $5K
  - Schedule compression: $2K

- **Resource Risks:** $10,000 (17%)
  - Contract specialists: $5K
  - Per Vices on-site support: $3K
  - Equipment rental: $2K

**Contingency Draw Authority:**
- <$5K: Project Manager approval
- $5K-$20K: CEO approval
- >$20K: Executive/board approval

**Contingency Tracking:**
- Monthly report on contingency usage
- Replenish if <$20K remaining
- Release unused contingency at project completion

---

## RISK REGISTER MAINTENANCE

**Update Frequency:**
- Weekly: During status calls (probability updates, new risks)
- Monthly: Full risk register review and re-scoring
- Ad-hoc: When significant events occur

**Document Owner:** Project Manager
**Review Authority:** CEO + Technical Lead
**Distribution:** Project team, Per Vices PM, executive stakeholders

**Version Control:**
- Maintain in git repository: `/pervices/RISK_REGISTER.md`
- Version number increments with each monthly review
- Archive previous versions for audit trail

---

## APPENDIX: RISK IDENTIFICATION METHODOLOGY

**Risk Identification Sources:**
1. Technical requirements analysis (requirements_summary.md)
2. Historical project data (legacy Varian system development)
3. Vendor assessment (Per Vices capabilities and constraints)
4. Expert judgment (NMR specialists, SDR engineers)
5. Schedule analysis (critical path dependencies)
6. Budget analysis (cost estimate uncertainty)

**Risk Categories:**
- **Technical:** Hardware, FPGA, software, integration challenges
- **Schedule:** Timeline delays, dependency failures, resource conflicts
- **Business:** Market, financial, customer, competitive risks
- **Resource:** Personnel, equipment, facilities, vendor capacity
- **External:** Regulatory, supply chain, force majeure

**Risk Scoring Formula:**
- Risk Score = (Probability % / 10) × (Impact / 10) × 10
- Example: 40% probability × High impact (8/10) = 3.2 × 10 = 6/10

---

**END OF RISK REGISTER**

**Next Review Date:** December 2, 2025 (Project Kickoff)
**Document Version:** 1.0
**Approval:** [CEO Signature] _________________ Date: _______
