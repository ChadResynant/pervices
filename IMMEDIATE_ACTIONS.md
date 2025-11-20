# IMMEDIATE ACTION PLAN
## Critical Actions for Week of November 11-15, 2025

**Project:** Resynant Harmonyzer NMR Spectrometer - Per Vices Crimson TNG
**Timeline:** 29 weeks to production (Jun 1, 2026)
**This Week is CRITICAL:** Actions taken Nov 11-15 determine project success

---

## 🚨 PRIORITY 1: DO TODAY (Monday, November 11)

### Action 1.1: Submit Documentation Package to Per Vices
**Owner:** Chad Rienstra
**Time Required:** 30 minutes
**Deliverable:** Email to Brandon Malatest

**Email Template:**
```
To: brandon.m@pervices.com
Subject: Strategic Partnership Opportunity - Resynant NMR Spectrometer Platform

Brandon,

Following our technical discussions over the past months, I'm pleased to confirm
that the Crimson TNG is an excellent fit for our Harmonyzer NMR spectrometer
platform. I'm ready to proceed with SOW development for our prototype program.

BUSINESS OPPORTUNITY:
• 1 prototype unit (Q1 2026) - SOW to be developed
• 10 production units (2026-2027) - ~$600K-$850K projected revenue
• 50-100 units/year ongoing (2027+) - multi-year strategic partnership
• Indiana University large order provides immediate R&D funding

TECHNICAL REQUIREMENTS:
I'm attaching comprehensive technical specifications (~170 pages):
1. executive_summary.md - Business context and accelerated timeline
2. requirements_summary.md - Requirements traceability and critical action items
3. technical_requirements.md - Detailed system specifications
4. use_case_scenarios.md - NMR operational scenarios
5. test_validation_plan.md - Acceptance criteria
6. nmr_pulse_sequences.md - FPGA waveform requirements
7. README.md - Documentation navigation guide

ACCELERATED TIMELINE REQUIREMENTS:
• Prototype delivery: January 31, 2026 (8 weeks from SOW approval)
• GPIO expander board with TTL compatibility (8-12 channels, ±100ns timing precision)
• FPGA CIC decimation filters (critical for dynamic range requirement)
• Priority treatment and dedicated engineering resources

IMMEDIATE REQUESTS (URGENT - By November 15):
Please provide responses to the following critical questions:

GPIO EXPANDER:
1. Do you have existing GPIO expander design/reference?
2. Electrical specifications (voltage, current, timing precision)?
3. Can you guarantee ±100ns timing precision?
4. Cost and delivery timeline if included in prototype?

FPGA CIC DECIMATION:
5. Is CIC decimation currently implemented in Crimson TNG?
6. If not, can it be developed and included by Jan 31, 2026?
7. What FPGA resources are available for this development?
8. NRE cost estimate?

PERFORMANCE SPECIFICATIONS:
9. Rx noise figure specification (20-1400 MHz range)?
10. Tx output power specification (across frequency range)?
11. Confirmed frequency tuning range (we need 20-1400 MHz)?

TIMELINE & COMMITMENT:
12. Can Per Vices commit to January 31, 2026 prototype delivery?
13. What priority/resource commitment is required from our side?
14. What are the primary risks to this timeline from your perspective?

NEXT STEPS:
• Technical alignment call: Week of November 18 (propose Nov 18 or 19)
• SOW draft delivery: November 22, 2025
• SOW approval & PO issuance: November 29, 2025

TERMS WE'RE PREPARED TO OFFER:
• 50% deposit upon SOW approval to secure priority production slot
• Schedule performance bonus ($5K for on-time delivery, $7.5K for early)
• Letter of Intent for 10 production units upon prototype acceptance
• Multi-year partnership agreement for ongoing production

This represents a significant strategic opportunity for both companies. Our
customers are actively waiting for modern NMR solutions, and time-to-market
is critical for our competitive positioning.

Can we schedule a call this week (Nov 11-15) to discuss your responses and
align on timeline commitment?

Best regards,

Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932
```

**Attachments:** All 6 specification documents + README.md

---

### Action 1.2: Reserve NMR Magnet Time
**Owner:** Chad Rienstra / Lab Manager
**Time Required:** 1 hour
**Deadline:** TODAY (Nov 11)

**Option A: NMRFAM (Primary)**
- Submit facility request for February 1 - March 31, 2026 (8 consecutive weeks)
- Specify: "Prototype validation for commercial NMR spectrometer development"
- Cost estimate: $8K-$12K for 8 weeks
- Contact: [NMRFAM facility coordinator]
- **ACTION:** Submit online request form or email facility coordinator

**Option B: Indiana University (Backup)**
- Contact recent large customer from Indiana University
- Propose: Early access to prototype in exchange for magnet time
- Cost: Potentially free or reduced (quid pro quo)
- **ACTION:** Email or call Indiana U contact

**Option C: Internal Calendar Block**
- If Resynant has own magnet, block out Feb 1 - Mar 31 NOW
- **ACTION:** Reserve calendar, notify team

**Critical:** Need confirmation of magnet availability by December 15, 2025

---

### Action 1.3: Inventory Test Equipment
**Owner:** Lab Manager / Technical Lead
**Time Required:** 2 hours
**Deadline:** TODAY (Nov 11)

**Equipment Needed for Validation (Feb-Mar 2026):**

| Equipment | Specification | Internal Availability? | Action if Not Available |
|-----------|---------------|----------------------|------------------------|
| Oscilloscope | ≥1 GHz, ≥4 channels | CHECK | Rent: $2K/month × 3 = $6K |
| Spectrum Analyzer | 20 MHz - 3 GHz | CHECK | Rent: $1K/month × 3 = $3K |
| Signal Generator | Low-noise, 20 MHz - 3 GHz | CHECK | Rent: $800/month × 3 = $2.4K |
| Network Analyzer | For probe tuning | CHECK | Borrow from university |
| 10GbE NIC | Dual-port SFP+ | CHECK | Purchase: $500 |
| 10GbE Switch | For future multi-unit | CHECK | Purchase: $1,500 |
| Host Computer | High-performance workstation | CHECK | Purchase: $3K-5K |

**ACTION STEPS:**
1. Inventory all test equipment currently available
2. Identify gaps
3. Create procurement plan with costs
4. If rental needed: Identify vendors and get quotes
5. Budget approval for equipment ($0-$20K depending on availability)

**Deliverable:** Equipment inventory spreadsheet with procurement plan by EOD Nov 11

---

## 📋 PRIORITY 2: Due Tuesday-Wednesday (Nov 12-13)

### Action 2.1: Assign Project Team
**Owner:** Chad Rienstra
**Time Required:** 3 hours
**Deadline:** Nov 12

**Roles to Fill:**

| Role | Time Commitment | Timeline | Candidate | Confirmed? |
|------|----------------|----------|-----------|-----------|
| **Project Manager** | 20% time (8 hrs/week) | Dec 2025 - May 2026 (24 weeks) | [NAME] | ☐ |
| **NMR Specialist (Lead)** | 100% time (40 hrs/week) | Feb-Mar 2026 (8 weeks)<br>25% time other phases | [NAME] | ☐ |
| **Software Engineer** | 50% time (20 hrs/week) | Dec 2025 - May 2026 (24 weeks) | [NAME] | ☐ |
| **Lab Technician** | 25% time (10 hrs/week) | Feb-May 2026 (16 weeks) | [NAME] | ☐ |

**Total Resource Commitment:**
- **NMR Specialist:** ~600 hours (15 weeks FTE)
- **Software Engineer:** ~800 hours (20 weeks FTE)
- **Lab Technician:** ~200 hours (5 weeks FTE)
- **Project Manager:** ~200 hours (5 weeks FTE)
- **Total Cost:** ~$250K internal labor

**ACTION STEPS:**
1. Identify candidates for each role
2. Confirm availability for specified timeline (especially Feb-Mar 2026 for NMR specialist)
3. Brief each team member on project scope and timeline
4. Get written commitment from each person
5. Set up kickoff meeting for week of Nov 18

**Deliverable:** Project team roster with confirmed availability by Nov 12

---

### Action 2.2: Budget Approval
**Owner:** Chad Rienstra
**Time Required:** 2 hours
**Deadline:** Nov 13

**Budget Request: $500,000**

**Breakdown:**
| Category | Amount | Notes |
|----------|--------|-------|
| Per Vices Vendor Costs | $107K-$170K | Prototype + GPIO + FPGA (pending SOW) |
| Internal Personnel | $253K | NMR specialist, software engineer, PM, lab tech |
| Equipment & Materials | $38K | Test equipment rental, magnet time, samples |
| Contingency (15%) | $40K | Overruns, rework, unexpected issues |
| **TOTAL** | **$438K-$501K** | **Request $500K approval** |

**Optional Schedule Compression Budget (if time-critical): +$80K**
- Fast-turn PCB: $1.5K (save 1 week)
- Weekend magnet access: $5K (save 2 weeks)
- 2nd NMR specialist: $20K (save 2 weeks)
- Expedited shipping: $2K (save 3 days)
- Contract software developer: $15K (save 2 weeks)
- **Total compression: +$50K for 4-6 weeks time savings**

**ACTION STEPS:**
1. Prepare budget justification document (use executive_summary.md Section 5)
2. Present to executive team/board
3. Get approval for $500K baseline (or $580K if schedule compression desired)
4. Obtain PO authorization up to approved amount

**Deliverable:** Budget approval and PO authority by Nov 13

---

### Action 2.3: Order Test Samples
**Owner:** Lab Manager
**Time Required:** 1 hour
**Deadline:** Nov 13
**Cost:** ~$1,500

**Samples Needed (Lead Time: 2-4 weeks):**

| Sample | Quantity | Purpose | Supplier | Cost |
|--------|----------|---------|----------|------|
| Adamantane (13C standard) | 5g | Basic NMR signal, SNR, calibration | Sigma-Aldrich | $150 |
| Glycine (13C labeled, 99%) | 5g | Decoupling, multi-peak test | Cambridge Isotope Labs | $300 |
| Alanine (13C labeled, 99%) | 5g | CP optimization, multiple peaks | Cambridge Isotope Labs | $350 |
| KBr (reagent grade) | 100g | Broadline testing (79Br/81Br) | Sigma-Aldrich | $50 |
| Custom sample (TBD) | - | Solvent suppression test (1:1000 ratio) | Internal prep | $500 |
| **TOTAL** | | | | **~$1,350** |

**Additional Lab Supplies:**
- NMR rotors (4mm and 3.2mm): $150
- Rotor caps and spacers: $50
- Chemicals for sample prep: $200
- **Grand Total: ~$1,750**

**ACTION STEPS:**
1. Place orders with Sigma-Aldrich and Cambridge Isotope Labs
2. Expedite shipping if possible (add $50-100)
3. Track delivery (should arrive by mid-December)
4. Prepare internal sample for solvent suppression testing

**Deliverable:** Purchase orders placed, tracking numbers received by Nov 13

---

## 📅 PRIORITY 3: Due Thursday-Friday (Nov 14-15)

### Action 3.1: Set Up Project Infrastructure
**Owner:** Project Manager
**Time Required:** 2 hours
**Deadline:** Nov 15

**Weekly Status Call Setup:**
- **Recurring Meeting:** Every Monday, 10:00 AM EST
- **Duration:** 30 minutes (extend to 60 min if needed)
- **Start Date:** December 2, 2025
- **End Date:** March 31, 2026
- **Participants:**
  - Resynant: Chad Rienstra (or delegate), Project Manager, Technical Lead
  - Per Vices: Brandon Malatest, Lead Engineer, Project Manager
- **Platform:** Zoom, Google Meet, or Microsoft Teams
- **Agenda Template:**
  1. Previous week accomplishments (5 min)
  2. Current week planned activities (5 min)
  3. Risks and blockers (10 min)
  4. Schedule status: on-track / at-risk / delayed (5 min)
  5. Action items and owners (5 min)

**Shared Document Repository:**
- Set up shared folder (Google Drive, Dropbox, or SharePoint)
- Structure:
  ```
  /Resynant-PerVices-Crimson-TNG/
    /00-SOW-and-Contracts/
    /01-Requirements-and-Specs/
    /02-Weekly-Status-Reports/
    /03-Technical-Documentation/
    /04-Test-Results/
    /05-Meeting-Notes/
  ```
- Permissions: Resynant team + Per Vices team
- Upload all specification documents to /01-Requirements-and-Specs/

**Communication Channels:**
- **Email:** Primary communication (brad.m@pervices.com + resynant team)
- **Slack/Teams Channel:** Optional for real-time communication during validation
- **Emergency Phone:** Per Vices lead engineer contact for critical issues
- **Monthly Executive Review:** Last Friday of each month (Chad ↔ Brandon)

**ACTION STEPS:**
1. Send calendar invite for recurring Monday status calls (Dec 2 onwards)
2. Set up shared folder and populate with specification documents
3. Create status report template
4. Set up communication channels (Slack/Teams if desired)

**Deliverable:** Infrastructure ready for SOW approval (Nov 29) by Nov 15

---

### Action 3.2: Initiate Software Development
**Owner:** Software Engineer
**Time Required:** 4 hours (this week); ongoing thereafter
**Deadline:** Start by Nov 15

**Week 1 Tasks (Nov 11-15):**

**Task 1: Download Per Vices Documentation**
- PVAN-11 Data Format Specification
  - URL: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
  - Study UDP packet format for received data
- Crimson TNG API Documentation (request from Per Vices if not public)
- Review technical requirements (technical_requirements.md Section 9)

**Task 2: Set Up Development Environment**
- Programming language: C++ or Python (recommend Python for prototyping)
- Libraries needed:
  - Network: socket, asyncio (Python) or Boost.Asio (C++)
  - Signal processing: NumPy, SciPy (Python) or FFTW (C++)
  - Data visualization: Matplotlib (Python) or Qt (C++)
- Version control: Git repository for project code
- IDE setup: VS Code, PyCharm, or preferred environment

**Task 3: Begin UDP Receiver Development**
- Create basic UDP socket listener on 10GbE interface
- Parse PVAN-11 packet format
- Implement data buffering (ring buffer for real-time streaming)
- Write test harness with simulated UDP packets
- **Goal:** Have basic receiver working by Dec 15 (even without hardware)

**Work Packages (Next 8 Weeks):**

| Week | Dates | Milestone | Deliverable |
|------|-------|-----------|-------------|
| 1-2 | Nov 11-22 | Setup & UDP receiver | Basic packet receiver working |
| 3-4 | Nov 25-Dec 6 | Data processing pipeline | I/Q data → complex samples → FID |
| 5-6 | Dec 9-20 | Pulse sequence compiler | Generate rectangular pulse waveforms |
| 7-8 | Dec 23-Jan 3 | Control interface | API for frequency, power, timing control |
| 9-10 | Jan 6-17 | Integration & testing | Simulator-based end-to-end test |
| 11-12 | Jan 20-31 | Software v1.0 release | Ready for hardware integration Feb 1 |

**ACTION STEPS:**
1. Download PVAN-11 spec and study packet format
2. Set up development environment (Git, IDE, libraries)
3. Begin UDP receiver coding
4. Create project plan and Gantt chart for software development

**Deliverable:** Development environment ready, UDP receiver started by Nov 15

---

## 📊 WEEK OF NOVEMBER 18: SOW Development

### Action 4.1: Technical Alignment Call
**Owner:** Chad Rienstra + Project Manager
**Date:** November 18 or 19, 2025 (schedule after Per Vices responds)
**Duration:** 60 minutes

**Pre-Call Preparation:**
- Review Per Vices responses to critical questions (submitted Nov 11, due Nov 15)
- Identify any gaps or concerns
- Prepare clarifying questions
- Have technical lead available for deep-dive questions

**Call Agenda:**
1. Review Per Vices responses to critical questions (15 min)
2. GPIO expander specifications and timeline (15 min)
3. FPGA CIC decimation: included in prototype or Phase 2? (15 min)
4. SOW content discussion: deliverables, milestones, timeline (10 min)
5. Commercial terms: pricing, payment schedule, incentives (5 min)

**Deliverable:** Alignment on technical approach, SOW content direction

---

### Action 4.2: SOW Review (Internal)
**Owner:** Chad Rienstra + Legal/Procurement
**Date:** Week of November 25
**Duration:** 4 hours

**Assuming Per Vices delivers SOW draft by November 22:**

**Review Checklist:**
- [ ] Fixed delivery date: January 31, 2026 (or acceptable alternative)
- [ ] GPIO expander specifications meet requirements (8-12 channels, ±100-200ns timing)
- [ ] FPGA CIC decimation: included or clear Phase 2 plan with NRE estimate
- [ ] Detailed deliverables list matches requirements
- [ ] Performance guarantees align with acceptance criteria
- [ ] Pricing within approved budget ($500K)
- [ ] Payment terms (propose 50% deposit, 50% on delivery)
- [ ] Weekly status call commitment
- [ ] On-site support (1 week during validation, Feb 2-7)
- [ ] 90-day warranty with FPGA updates
- [ ] Bonus structure for on-time/early delivery (optional but recommended)

**Red Flags (Negotiate or Walk Away):**
- ❌ Delivery date later than February 15, 2026
- ❌ GPIO expander not included or timing precision undefined
- ❌ No commitment to FPGA CIC decimation
- ❌ Total cost exceeds $600K without clear justification
- ❌ No performance guarantees or acceptance criteria
- ❌ Poor communication/support commitments

**Deliverable:** Internal SOW review complete, negotiation points identified by Nov 26

---

### Action 4.3: SOW Negotiation & Approval
**Owner:** Chad Rienstra
**Date:** November 26-29, 2025

**Negotiation Call (Nov 26):**
- Discuss any concerns or modifications needed
- Finalize timeline, deliverables, pricing
- Agree on bonus/penalty structure (if applicable)
- Confirm weekly status call cadence and support commitments

**Internal Approval (Nov 27-28):**
- Circulate final SOW to executive team/board
- Obtain approval signatures
- Prepare PO for issuance

**SOW Signature & PO Issuance (Nov 29):**
- Sign SOW with Per Vices
- Issue purchase order
- Schedule project kickoff call (Dec 2, 10am EST)
- **MILESTONE ACHIEVED:** Project officially launched

---

## 🎯 SUCCESS METRICS FOR THIS WEEK

### By End of Week (Nov 15):
✅ Email sent to Per Vices with all documentation
✅ NMR magnet time reserved (primary + backup)
✅ Test equipment inventory complete, procurement plan ready
✅ Project team assigned and confirmed
✅ Budget approved ($500K)
✅ Test samples ordered
✅ Project infrastructure set up (status calls, shared folders)
✅ Software development initiated

### By End of Nov 22:
✅ Per Vices responses to critical questions received (due Nov 15)
✅ Technical alignment call completed
✅ SOW draft received from Per Vices
✅ Software: Basic UDP receiver working

### By End of Nov 29:
✅ SOW approved and signed
✅ Purchase order issued to Per Vices
✅ Project kickoff call scheduled (Dec 2)

---

## ⚠️ RISK FACTORS THIS WEEK

### Risk 1: Per Vices Non-Responsive
**Indicator:** No response to Nov 11 email within 48 hours
**Action:** Follow-up phone call to Brandon Malatest
**Escalation:** If no response by Nov 14, consider alternative vendors or adjust timeline

### Risk 2: Magnet Access Unavailable
**Indicator:** NMRFAM or Indiana U cannot provide Feb-Mar 2026 access
**Action:** Activate backup plan (find 3rd facility or adjust timeline)
**Escalation:** May need to push validation to March-April (4 week delay)

### Risk 3: Budget Not Approved
**Indicator:** Executive team/board questions $500K budget
**Action:** Present detailed ROI analysis (executive_summary.md Section 5.3)
**Escalation:** Reduce scope (defer FPGA optimization, use cheaper equipment) or delay project

### Risk 4: Key Personnel Unavailable
**Indicator:** NMR specialist or software engineer cannot commit to timeline
**Action:** Identify alternative candidates or hire contractor
**Escalation:** May need external resources (+$50K-$100K budget increase)

---

## 📞 CONTACTS

### Resynant Team
- **Chad Rienstra (CEO):** chad@resynant.com, (217) 649-8932
- **Project Manager:** [TBD]
- **NMR Specialist:** [TBD]
- **Software Engineer:** [TBD]

### Per Vices Team
- **Brandon Malatest (COO):** brandon.m@pervices.com, +1 (647) 534-9007
- **Lead Engineer:** [TBD after SOW]
- **Project Manager:** [TBD after SOW]

### External Resources
- **NMRFAM Facility:** [Coordinator contact]
- **Indiana University Customer:** [Customer contact]
- **Equipment Rental Vendors:** [TBD based on needs]

---

## 📋 CHECKLIST (Print and Track Progress)

**MONDAY NOV 11:**
- [ ] Send email to Per Vices (brandon.m@pervices.com) with all spec documents
- [ ] Submit NMRFAM facility request for Feb 1 - Mar 31, 2026
- [ ] Contact Indiana U customer for backup magnet access
- [ ] Inventory test equipment, create procurement plan

**TUESDAY NOV 12:**
- [ ] Assign project team (PM, NMR specialist, software engineer, lab tech)
- [ ] Confirm team availability for Feb-Mar 2026 intensive phase
- [ ] Prepare budget approval presentation

**WEDNESDAY NOV 13:**
- [ ] Present budget to executive team/board
- [ ] Obtain $500K budget approval
- [ ] Order test samples (adamantane, glycine, alanine, KBr)

**THURSDAY-FRIDAY NOV 14-15:**
- [ ] Set up weekly status call (recurring Monday 10am, starts Dec 2)
- [ ] Create shared document repository
- [ ] Upload specification documents to shared folder
- [ ] Software engineer: Download PVAN-11 spec, set up dev environment
- [ ] Receive Per Vices responses to critical questions (DUE NOV 15)

**WEEK OF NOV 18:**
- [ ] Technical alignment call with Per Vices (Nov 18-19)
- [ ] Receive SOW draft from Per Vices (DUE NOV 22)

**WEEK OF NOV 25:**
- [ ] Internal SOW review (Nov 25-26)
- [ ] SOW negotiation call with Per Vices (Nov 26)
- [ ] Final SOW approval internally (Nov 27-28)
- [ ] Sign SOW and issue PO (NOV 29) ← MILESTONE

---

## 🚀 NEXT PHASE: PROTOTYPE DEVELOPMENT

**Starting Dec 2, 2025:**
- Weekly status calls with Per Vices (every Monday 10am)
- Software development continues (Dec-Jan, 8 weeks)
- Per Vices: GPIO board design, FPGA development, hardware assembly
- Target: Prototype delivery January 31, 2026

**For detailed timeline, see executive_summary.md Section 4**

---

**This document is a living checklist. Update daily with progress.**
**Flag any red/yellow issues immediately to project manager and Chad.**

**Questions? Contact Chad Rienstra: chad@resynant.com / (217) 649-8932**
