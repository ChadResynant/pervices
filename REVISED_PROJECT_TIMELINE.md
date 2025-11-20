# Revised Project Timeline
## Resynant Harmonyzer NMR Spectrometer Development
### Per Vices Crimson TNG Platform

**Document Version:** 2.0 (Revised)
**Date:** November 21, 2025
**Previous Version:** IMMEDIATE_ACTIONS.md (accelerated timeline)
**Status:** REALISTIC TIMELINE based on current project status

---

## Executive Summary

**Original Timeline:** 29 weeks to production (June 1, 2026)
**Revised Timeline:** 36 weeks to production (August 1, 2026)
**Change:** +7 weeks to accommodate realistic planning and execution pace

**Key Drivers for Revision:**
- Documentation package completion: Added 2 weeks
- Prototype development: Added 4 weeks (Feb 28 vs. Jan 31)
- Beta testing at Indiana: Added opportunity in May-June
- Production release: Moved to August 1 for quality assurance

**Status:** Funding secured ($900K PO + $1M Series A), team assigned, resources ready

---

## Phase 0: Documentation and SOW (3 weeks)
### November 21 - December 13, 2025

**Objective:** Complete technical documentation and finalize Statement of Work

### Week 1: Nov 21-27 (Thanksgiving Week)
**Deliverables:**
- ✅ GPIO specifications document (COMPLETED Nov 21)
- ✅ Email to Per Vices with documentation package (SEND Nov 21)
- ⬜ Technical alignment call with Per Vices (Nov 25-26)
- ⬜ Software development environment setup (Nov 22-24)
- ⬜ UDP receiver skeleton code (Nov 22-24)

**Owner:** Chad Rienstra (NMR Specialist + Software Engineer)
**Support:** Lauren Price (PM), Alex Dreena (R&D)

### Week 2: Dec 2-6
**Deliverables:**
- ⬜ Per Vices SOW draft received (target: Dec 6)
- ⬜ Internal SOW review completed
- ⬜ UDP receiver basic functionality (packet reception)
- ⬜ Indiana March deployment plan drafted

**Owner:** Chad Rienstra + Lauren Price
**Support:** Alex Dreena (lab setup)

### Week 3: Dec 9-13
**Deliverables:**
- ⬜ SOW negotiation and approval (target: Dec 13)
- ⬜ Purchase order issued to Per Vices
- ⬜ Project kickoff call scheduled (Dec 16)
- ⬜ Weekly status call cadence established

**MILESTONE:** 🎯 **SOW APPROVED** (December 13, 2025)

---

## Phase 1: Prototype Development (11 weeks)
### December 16, 2025 - February 28, 2026

**Objective:** Per Vices builds prototype; Resynant prepares validation environment

### Weeks 4-7: Dec 16 - Jan 10 (4 weeks)
**Per Vices Activities:**
- Crimson TNG hardware assembly (standard configuration)
- GPIO expander board design and fabrication
- FPGA CIC decimation filter development (if included)
- Initial factory testing

**Resynant Activities:**
- Software development: UDP receiver and data processing pipeline
- Pulse sequence compiler framework
- Test environment preparation (bench equipment setup)
- Test sample preparation and characterization

**Weekly Status Calls:** Every Monday, 10:00 AM Central
**Owner (Per Vices):** Brandon Malatest + Lead Engineer
**Owner (Resynant):** Chad Rienstra + Lauren Price

### Weeks 8-11: Jan 13 - Feb 7 (4 weeks)
**Per Vices Activities:**
- GPIO expander integration and testing
- FPGA firmware finalization
- Factory validation and burn-in
- Documentation and user manual preparation

**Resynant Activities:**
- Software integration testing (simulated data)
- Validation test procedures finalized
- Bench test equipment calibration
- Magnet scheduling confirmed (400 MHz and 600 MHz)

### Weeks 12-14: Feb 10 - Feb 28 (3 weeks)
**Per Vices Activities:**
- Final factory acceptance testing
- Packaging and shipping preparation
- On-site support planning (1 week during validation)
- Technical documentation delivery

**Resynant Activities:**
- Final software preparation for prototype integration
- Test plan review and refinement
- Lab space preparation for prototype arrival
- Indiana deployment planning (March timeline)

**MILESTONE:** 🎯 **PROTOTYPE DELIVERED** (February 28, 2026)

---

## Phase 2: Prototype Validation (11 weeks)
### March 2 - May 15, 2026

**Objective:** Validate prototype performance against acceptance criteria

### Weeks 15-16: Mar 2-13 (2 weeks) - Bench Testing
**Test Focus:** Electrical and timing validation (no NMR magnet)

**Test Activities:**
- GPIO timing precision validation (±100 ns requirement)
- Frequency range verification (20-1400 MHz)
- Phase coherency measurement (all 4 channels)
- Data throughput testing (10GbE packet reception)
- TX/RX timing coordination verification

**Acceptance Criteria:**
- GPIO timing: ±100 ns precision, <50 ns jitter
- Frequency coverage: Validated at 20, 100, 400, 600, 1000, 1400 MHz
- Phase coherency: <2° standard deviation across channels
- Data throughput: Sustained acquisition without packet loss (<0.01%)

**Owner:** Chad Rienstra + Alex Dreena
**Support:** Per Vices on-site engineer (1 week)

### Weeks 17-20: Mar 16 - Apr 10 (4 weeks) - NMR Integration
**Test Focus:** Basic NMR signal acquisition and characterization

**Test Activities (400 MHz magnet):**
- Initial NMR signal detection (proton, adamantane)
- SNR measurement and comparison to legacy Varian system
- Dynamic range characterization (adamantane, known samples)
- Single-channel optimization (frequency, power, timing)
- Basic pulse sequences (Hahn echo, CPMG, T1/T2 measurements)

**Acceptance Criteria:**
- NMR signal detected: SNR >50:1 on adamantane
- Dynamic range: ENOB ≥17 bits at 5 MHz bandwidth
- Pulse sequence execution: Successful T1, T2 measurements
- Data quality: Comparable to legacy Varian performance

**Owner:** Chad Rienstra (20 hrs/week NMR specialist)
**Support:** Alex Dreena (lab operations)

### Weeks 21-24: Apr 13 - May 8 (4 weeks) - Multi-Channel Validation
**Test Focus:** Advanced NMR techniques (cross-polarization, decoupling)

**Test Activities (600 MHz magnet):**
- Multi-channel phase coherency (CP experiments)
- Decoupling performance (TPPM, SPINAL sequences)
- Shaped pulse validation (Gaussian, sinc waveforms)
- Complex pulse sequences (2D HETCOR, DARR, etc.)
- Stress testing (long acquisitions, thermal stability)

**Acceptance Criteria:**
- Cross-polarization: CP enhancement ≥2× vs. direct excitation
- Decoupling: Multiplet collapse, SNR gain 2-4×
- Multi-channel coordination: Independent phase control verified
- Long-term stability: <1% drift over 8-hour acquisition

**Owner:** Chad Rienstra
**Support:** Alex Dreena, potential external NMR consultant

### Week 25: May 11-15 - Performance Characterization and Report
**Final Validation:**
- Comprehensive performance benchmarking
- Comparison to competitor specifications
- Identification of any issues or optimization opportunities
- Final validation report preparation

**Deliverables:**
- Validation Test Report (pass/fail determination)
- Performance characterization data
- Recommendations for production optimization
- Decision: Proceed to production or request modifications

**MILESTONE:** 🎯 **VALIDATION COMPLETE** (May 15, 2026)

---

## Phase 3: Beta Testing (Indiana University)
### May 18 - June 30, 2026 (6 weeks)

**Objective:** Field testing with beta customer (Indiana University)

**Integration Plan:**
- Indiana receives Resynant 600 MHz console in March 2026 (legacy Varian-based)
- Upgrade console with Per Vices Crimson TNG prototype in May 2026
- Side-by-side comparison: Legacy system vs. Per Vices system
- Beta test period: 6 weeks of real-world usage

**Test Focus:**
- User experience and ease of operation
- Reliability and uptime
- Performance in production research environment
- Software integration with Harmonyzer control system
- Customer feedback on features and capabilities

**Success Metrics:**
- System uptime: >95% during beta period
- User satisfaction: Positive feedback on performance vs. legacy system
- No critical failures requiring prototype return
- Identification of production improvements

**MILESTONE:** 🎯 **BETA TESTING COMPLETE** (June 30, 2026)

---

## Phase 4: Production Readiness (4 weeks)
### July 1 - August 1, 2026

**Objective:** Finalize design for production deployment

**Per Vices Activities:**
- FPGA optimization based on validation results
  - Waveform buffering and looping (if not in prototype)
  - Performance tuning for dynamic range
  - GPIO timing refinement
- Production firmware release
- Final documentation and user manuals
- Production unit cost confirmation

**Resynant Activities:**
- Software integration with Harmonyzer production system
- User interface refinement based on beta feedback
- Production test procedures
- Customer training materials
- First production order placement (10 units)

**MILESTONE:** 🎯 **PRODUCTION RELEASE** (August 1, 2026)

---

## Phase 5: Initial Production Deployment
### August - December 2026

**Objective:** Deploy first 10 production units to customers

**Timeline:**
- **August 2026:** First production order placed (10 units)
- **September-October 2026:** Per Vices production and delivery
- **November-December 2026:** Customer installations and support

**Customers:**
- Indiana University (upgrade existing console)
- Pending orders currently using legacy Varian technology
- New orders secured during beta testing period

**Deliverables:**
- 10 production units installed
- Legacy Varian technology phased out (50% of systems)
- Customer satisfaction metrics collected
- Production process optimized for ongoing deployment

---

## Full Production Deployment (2027+)
### Target: 50-99 units per year

**Volume Production:**
- Quarterly orders to Per Vices (10-25 units per quarter)
- Volume pricing negotiated based on annual commitment
- Continuous improvement based on customer feedback
- Expansion to multi-channel systems (>4 channels) as needed

---

## Summary Timeline Comparison

| Milestone | Original Plan | Revised Plan | Change |
|-----------|--------------|--------------|--------|
| **SOW Approval** | Nov 29, 2025 | Dec 13, 2025 | +2 weeks |
| **Prototype Delivery** | Jan 31, 2026 | Feb 28, 2026 | +4 weeks |
| **Validation Complete** | Mar 31, 2026 | May 15, 2026 | +6 weeks |
| **Beta Testing** | N/A | Jun 30, 2026 | +6 weeks (NEW) |
| **Production Release** | May 31, 2026 | Aug 1, 2026 | +8 weeks |
| **First Production Units** | Jun-Aug 2026 | Sep-Oct 2026 | +2 months |

**Total Time to Production:** 36 weeks (vs. 29 weeks original)
**Time Added:** 7 weeks for realistic execution + beta testing opportunity

---

## Risk Assessment and Mitigation

### Low-Risk Items (High Confidence)
✅ **Funding:** $900K PO + $1M Series A secured
✅ **Team:** Chad (20 hrs/week), Lauren (PM), Alex (full-time) committed
✅ **Equipment:** All test equipment and samples ready
✅ **Magnet Access:** 400 MHz and 600 MHz available 24/7
✅ **Beta Site:** Indiana University committed for March-June testing

### Medium-Risk Items (Require Monitoring)
⚠️ **Per Vices Timeline:** Feb 28 delivery depends on GPIO expander development
⚠️ **Dynamic Range:** ENOB target may require FPGA optimization
⚠️ **Software Development:** Chad's 20 hrs/week may be tight; consider contractor
⚠️ **Validation Duration:** 11 weeks assumes no major issues; add contingency buffer

### Mitigation Strategies
1. **Per Vices Engagement:** Weekly status calls, early issue identification
2. **Software Development:** Identify tasks for contractor delegation (UDP receiver, data processing)
3. **Validation Buffer:** If issues arise, leverage Indiana beta period for extended testing
4. **Fallback:** Legacy Varian technology available for customer orders during development

---

## Critical Path Items

**Week of Nov 21 (THIS WEEK):**
1. Send documentation package to Per Vices (TODAY)
2. Schedule technical alignment call (Nov 25-26)
3. Begin software development environment setup
4. Create UDP receiver skeleton code

**Week of Dec 2:**
5. Review Per Vices SOW draft
6. Negotiate and finalize SOW terms
7. Continue software development (UDP receiver functional)

**Week of Dec 9:**
8. Approve and sign SOW (target: Dec 13)
9. Issue purchase order to Per Vices
10. Schedule project kickoff call (Dec 16)

**December 16 Onwards:**
- Weekly status calls with Per Vices (every Monday)
- Parallel software development (Chad + potential contractor)
- Validation environment preparation

---

## Resource Allocation

### Chad Rienstra (President & CEO)
- **Dec 2025 - Feb 2026:** 20 hrs/week (software development)
- **Mar 2026 - May 2026:** 20+ hrs/week (NMR specialist, validation testing)
- **Jun 2026 onwards:** 10 hrs/week (oversight, beta testing support)

### Lauren Price (Assistant Project Manager)
- **Dec 2025 - Aug 2026:** 8 hrs/week (project coordination, vendor liaison)
- Weekly status calls with Per Vices
- Documentation and timeline tracking
- Customer communication for beta testing

### Alex Dreena (Head of R&D, Lab Technician)
- **Feb 2026 - Jun 2026:** Full-time (validation testing, lab operations)
- Bench testing setup and execution
- NMR magnet operations and sample preparation
- Beta testing support at Indiana

### Potential Software Contractor (TBD)
- **Dec 2025 - Feb 2026:** 10-20 hrs/week (optional)
- UDP receiver development and testing
- Data processing pipeline implementation
- Pulse sequence compiler framework
- **Cost:** ~$15K-$30K (if needed for schedule compression)

---

## Budget Summary (Revised)

| Category | Amount | Notes |
|----------|--------|-------|
| **Per Vices Costs** | $107K-$170K | Prototype + GPIO + FPGA (pending SOW) |
| **Internal Personnel** | $150K-$200K | Revised estimate (Chad, Lauren, Alex) |
| **Equipment & Materials** | $25K | Test equipment, samples (mostly in-house) |
| **Software Contractor** | $0-$30K | Optional, if needed for schedule |
| **Beta Testing (Indiana)** | $10K | Travel, support, contingency |
| **Contingency (10%)** | $30K-$40K | Reduced from 15% given resources ready |
| **TOTAL** | **$322K-$465K** | **Well within $500K approved budget** |

**Funding Available:**
- $900K Indiana University PO
- $1M Series A financing (closing this week)
- **Total:** $1.9M available for R&D and production

**Budget Status:** ✅ LOW RISK - ample funding available

---

## Success Criteria

### Prototype Acceptance (May 15, 2026)
1. ✅ Phase coherency: <2° standard deviation across all channels
2. ✅ Dynamic range: ENOB ≥17 bits at 5 MHz bandwidth
3. ✅ GPIO timing: ±100 ns precision, jitter <50 ns
4. ✅ Frequency coverage: Validated 20-1400 MHz
5. ✅ Data throughput: Sustained acquisition without packet loss (<0.01%)
6. ✅ NMR signal acquisition: SNR >50:1 on adamantane standard

### Beta Testing Success (June 30, 2026)
1. ✅ System uptime: >95% during beta period
2. ✅ User satisfaction: Positive feedback vs. legacy system
3. ✅ No critical failures requiring prototype return
4. ✅ Performance meets/exceeds Varian legacy system

### Production Release (August 1, 2026)
1. ✅ Production firmware finalized and validated
2. ✅ Software integration complete with Harmonyzer
3. ✅ First production order placed (10 units)
4. ✅ Customer training materials prepared
5. ✅ Volume pricing negotiated with Per Vices

---

## Next Steps (Nov 21-27, 2025)

### TODAY (Thursday Nov 21) - 4-6 hours
1. ✅ Review and send email to Brandon Malatest with documentation package
2. ✅ Attach all specification documents (7 files + GPIO spec)
3. ⬜ Download PVAN-11 data format specification
4. ⬜ Set up development environment (Python or C++)
5. ⬜ Create project Git repository for software development

### FRIDAY (Nov 22) - 6 hours
6. ⬜ UDP receiver framework development
7. ⬜ PVAN-11 packet parsing skeleton
8. ⬜ Team kickoff meeting with Lauren and Alex (1 hour)
9. ⬜ Indiana deployment planning discussion

### WEEKEND (Nov 23-24) - 8 hours
10. ⬜ UDP receiver basic functionality (packet reception and validation)
11. ⬜ Data buffering and ring buffer implementation
12. ⬜ Test harness with simulated UDP packets
13. ⬜ Prepare for Per Vices technical call (Nov 25-26)

### MONDAY (Nov 25) - 2 hours
14. ⬜ Technical alignment call with Per Vices
15. ⬜ Review Per Vices feedback on documentation
16. ⬜ Address any clarifications or questions
17. ⬜ Confirm SOW delivery timeline (target: Dec 6)

---

**Document Status:** APPROVED - Ready for execution
**Next Review:** December 2, 2025 (after Per Vices SOW received)

**Contact Information:**

Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

---

**End of Revised Project Timeline**
