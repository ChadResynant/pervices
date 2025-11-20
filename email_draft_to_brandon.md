# Email Draft to Brandon Malatest - Per Vices Crimson TNG Partnership

---

**To:** brandon.m@pervices.com
**Subject:** Crimson TNG for NMR Spectrometer - Partnership Proposal with Detailed Requirements & Phased Milestones
**Attachments:** 7 specification documents (~170 pages)

---

Brandon,

Following our technical discussions over the past months, I'm ready to proceed with a formal partnership to develop a Crimson TNG-based NMR spectrometer platform for Resynant's Harmonyzer product line. This represents a significant strategic opportunity for both companies.

## Business Opportunity

**Immediate:**
- 1 prototype unit (Q1 2026) - funded by Indiana University large order
- 10 production units (2026-2027) - estimated $600K-$850K revenue
- 50-100 units/year ongoing (2027+) - multi-year strategic partnership

**Market Context:**
- We're replacing aging Varian DDR technology across our customer base
- Current customers are waiting for modern NMR solutions
- Time-to-market is critical for competitive positioning

## Comprehensive Technical Specifications Attached

I'm providing complete technical documentation (~170 pages):

1. **executive_summary.md** - Business case, timeline, budget, risk assessment
2. **requirements_summary.md** - Requirements traceability and gap analysis
3. **technical_requirements.md** - Detailed system specifications (24 pages)
4. **use_case_scenarios.md** - NMR operational scenarios and data flow (28 pages)
5. **test_validation_plan.md** - Acceptance testing procedures (34 pages)
6. **nmr_pulse_sequences.md** - FPGA waveform requirements (36 pages)
7. **IMMEDIATE_ACTIONS.md** - Project planning and critical next steps

## Lessons from Previous Approach

**Context you should know:** We previously explored a Tabor Proteus AWG solution with OpenVNMRJ integration (2023-2024). That project stalled due to:
- Unclear vendor capabilities for critical features (GPIO timing, hardware looping, phase cycling)
- Overly complex software architecture (too many translation layers)
- AWG platform not purpose-built for multi-channel phase-coherent applications

**Why Crimson TNG is fundamentally better:**
- Purpose-built SDR with factory-calibrated phase coherency (JESD204B)
- Well-defined PVAN-11 data interface over 10 GbE
- Proven multi-channel synchronization architecture
- Clean software development path (no legacy integration burden)

**What I learned:** Front-load the technical unknowns. Before signing an SOW, I need SPECIFIC confirmation that critical features are achievable, not "we'll investigate."

## Critical Technical Questions - Need Answers by Nov 15

### 1. GPIO Expander Board (HIGHEST PRIORITY)

**Requirements:**
- 8-12 TTL output channels (0-5V logic levels)
- Timing precision: ±100-200 ns, jitter <50 ns
- Programmable trigger patterns synchronized to Tx/Rx events

**Questions:**
- Do you have an existing GPIO expander design or reference implementation?
- What are the detailed electrical specifications (voltage, current drive, impedance)?
- **Can you provide timing test data or oscilloscope measurements demonstrating ±100-200ns precision?**
- What is the cost and delivery timeline if included in prototype delivery (Jan 31)?
- Is this a standard product or custom development?

**Why this matters:** GPIO timing was an "unknown" in the previous project and became a blocker. I need evidence of capability, not just "it should be possible."

### 2. FPGA CIC Decimation Filters (HIGH PRIORITY)

**Requirements:**
- 4-channel CIC decimation (325 MSPS → 10 MHz, 32× decimation factor)
- Needed for dynamic range enhancement (16-bit → 19-20 bit ENOB)

**Questions:**
- Is CIC decimation currently implemented in standard Crimson TNG FPGA firmware?
- If not, can it be developed and included in prototype delivery (Jan 31)?
- What FPGA resources (logic elements, block RAM) are available for this development?
- What is the NRE cost and timeline estimate?
- **Can you provide example code or reference implementations from similar projects?**

**Fallback:** Host-side decimation is acceptable for Phase 1, but FPGA implementation is strongly preferred for Phase 2.

### 3. Performance Specifications (MEDIUM PRIORITY)

**Questions:**
- Rx noise figure across 20-1400 MHz range?
- Tx output power across frequency range?
- **Confirmed frequency tuning range** (we need 20-1400 MHz coverage)
- SFDR (spurious-free dynamic range)?
- Phase noise specification for OCXO and synthesized LOs?

### 4. PVAN-11 Data Format and Multi-Channel Operation (MEDIUM PRIORITY)

**Questions:**
- Can you provide example PVAN-11 packet captures from a 4-channel Rx acquisition?
- What is the maximum sustained data throughput (4 channels × 325 MSPS)?
- How is phase coherency maintained across channels in the PVAN-11 stream?
- What is the latency and jitter for timed command execution?

## Proposed Development Milestones - Incremental Risk Reduction

I'm proposing a **phased milestone approach** that builds complexity incrementally and validates each capability before proceeding. This de-risks the project and provides clear acceptance gates.

### Phase 0: Pre-SOW Technical Validation (Nov 11-29, 2025) ⚠️ CRITICAL

**Before signing SOW, Per Vices provides:**
- Answers to all critical questions above
- GPIO expander specifications with timing validation data
- FPGA CIC decimation feasibility assessment (exists OR NRE estimate)
- Confirmed frequency range specifications
- Example PVAN-11 packet captures or documentation

**Deliverable:** Technical confidence to proceed with SOW approval

**Why this matters:** The previous project failed because critical capabilities were "unknowns" that got deferred. I need specifics BEFORE committing.

### Phase 1: Hardware Validation (Weeks 1-2 after delivery, Feb 1-14, 2026)

**Milestone 1.1: Basic Network and Data Acquisition**
- Connect Crimson TNG to 10 GbE network
- Receive PVAN-11 packets from single Rx channel
- Parse packet format, validate timing, confirm <0.01% packet loss
- Generate simple Tx waveform (CW tone) on single channel
- **Acceptance:** UDP streaming functional, basic Tx/Rx operational

**Milestone 1.2: GPIO Timing Validation** ⭐ DE-RISKS CRITICAL UNKNOWN
- Trigger GPIO outputs programmatically
- Measure timing precision with oscilloscope
- Validate ±100-200ns precision requirement
- Test jitter over 1000 trigger events
- **Acceptance:** GPIO meets ±100-200ns timing specification

**Milestone 1.3: Multi-Channel Phase Coherency**
- Acquire simultaneous data from all 4 Rx channels
- Measure relative phase between channels with common input signal
- Validate <2° standard deviation (factory calibration)
- **Acceptance:** Phase coherency meets NMR requirements

### Phase 2: Basic Pulse Sequence Elements (Weeks 3-4, Feb 15-28, 2026)

**Milestone 2.1: Delay + Pulse + Acquire (Single Channel)**
- Program basic sequence: 10 μs delay → 5 μs Tx pulse → 1 ms Rx acquire
- Validate timing precision (±1 μs)
- Process FID in host software
- **Acceptance:** Basic pulse-acquire sequence functional

**Milestone 2.2: Looping and Time Averaging** ⭐ DE-RISKS CRITICAL UNKNOWN
- Implement scan loop (acquire 100 scans, average in real-time or post-process)
- Validate no data loss, no timing drift across scans
- **Acceptance:** Time-averaged FID with improved SNR

**Milestone 2.3: Tx Gating with GPIO**
- Trigger GPIO during Tx pulse (for amplifier blanking)
- Validate GPIO-to-Tx timing synchronization
- Measure Rx protection during Tx event
- **Acceptance:** GPIO synchronized with RF events (±100-200ns)

**Milestone 2.4: Phase Cycling** ⭐ DE-RISKS CRITICAL UNKNOWN
- Implement 4-step phase cycle (0°, 90°, 180°, 270°)
- Validate phase precision across cycles (<0.1° error)
- Test receiver phase coherence
- **Acceptance:** Phase cycling functional with required precision

### Phase 3: NMR Integration Testing (Weeks 5-6, Mar 1-14, 2026)

**Milestone 3.1: First NMR Signal - Single-Pulse on Adamantane**
- Connect Crimson TNG to NMR magnet and probe
- Tune and match probe to NMR frequency
- Acquire 13C FID on adamantane standard sample
- **Acceptance:** SNR >50:1 (MUST-PASS CRITERION) ✅

**Milestone 3.2: Multi-Channel NMR Acquisition**
- Acquire simultaneous 1H and 13C signals
- Validate inter-channel phase coherency in NMR context
- **Acceptance:** Multi-channel signals properly synchronized (<2° phase error)

### Phase 4: Advanced NMR Sequences (Weeks 7-8, Mar 15-31, 2026)

**Milestone 4.1: Cross-Polarization (CP)**
- Implement ramped CP waveform (1H → 13C magnetization transfer)
- Measure CP enhancement factor
- Optimize contact time
- **Acceptance:** CP functional, enhancement >2× (typical NMR performance)

**Milestone 4.2: Heteronuclear Decoupling**
- Implement continuous-wave or TPPM decoupling sequence
- Measure multiplet collapse and SNR gain during 1H decoupling
- **Acceptance:** Decoupling functional, SNR improvement 2-4×

**Milestone 4.3: Dynamic Range Measurement** (MUST-PASS CRITERION) ✅
- Acquire signals with decimation (FPGA CIC if available, host-side otherwise)
- Measure ENOB at 5 MHz bandwidth
- Test large signal / small signal discrimination
- **Acceptance:** ENOB ≥17 bits @ 5 MHz bandwidth (MUST-PASS)

### Gate: Prototype Acceptance Decision (March 31, 2026)

**Go/No-Go based on:**
- ✅ Phase coherency: <2° standard deviation (all channels)
- ✅ GPIO timing: ±100-200 ns precision, <50 ns jitter
- ✅ Dynamic range: ENOB ≥17 bits @ 5 MHz bandwidth
- ✅ NMR SNR: >50:1 on adamantane standard sample
- ✅ Data throughput: <0.01% packet loss sustained acquisition
- ✅ CP and decoupling: Functional with typical NMR performance

**If all criteria met:**
- Issue Letter of Intent for 10 production units
- Proceed to Phase 2 optimization (FPGA waveform looping, software integration)
- Negotiate volume pricing for 50-100 units/year

**If criteria not met:**
- Identify specific gaps and remediation plan
- Determine if issues are fixable or fundamental limitations

## Why This Milestone Approach Works

**Learned from previous project failure:**
- **Incremental validation** - Build up complexity step-by-step, don't assume everything works
- **Front-load critical unknowns** - GPIO timing, phase cycling, looping validated in Phase 1-2
- **Clear acceptance gates** - Quantitative metrics, not subjective assessments
- **Evidence-based decisions** - Test data drives go/no-go, not vendor promises

**Leverages Crimson TNG strengths:**
- Factory-calibrated phase coherency (Milestone 1.3) - should pass easily
- Well-defined PVAN-11 interface (Milestone 1.1) - low risk
- Purpose-built SDR architecture - not forcing AWG to be NMR console

**De-risks business commitment:**
- 8-week validation period before production commitment
- Multiple decision points to identify issues early
- Fallback options at each phase if problems arise

## Aggressive Timeline - Requires Per Vices Priority Commitment

| Milestone | Target Date | Duration |
|-----------|-------------|----------|
| **Critical Questions Answered** | **Nov 15, 2025** | **4 days** ⏰ |
| **Technical Alignment Call** | **Nov 18-19, 2025** | **1 day** |
| **SOW Draft Delivered** | **Nov 22, 2025** | **1 week** |
| **SOW Approval & PO Issued** | **Nov 29, 2025** | **2 weeks** |
| **Prototype Development** | **Dec 2 - Jan 31, 2026** | **8 weeks** |
| **Phase 1: Hardware Validation** | **Feb 1-14, 2026** | **2 weeks** |
| **Phase 2: Basic Sequences** | **Feb 15-28, 2026** | **2 weeks** |
| **Phase 3: NMR Integration** | **Mar 1-14, 2026** | **2 weeks** |
| **Phase 4: Advanced Sequences** | **Mar 15-31, 2026** | **2 weeks** |
| **Prototype Acceptance Decision** | **Mar 31, 2026** | **End of Phase 4** |
| **Production Release** | **May 31, 2026** | **+8 weeks** |

**Total: 6.5 months from requirements to production**

**This is aggressive.** It requires:
- Per Vices priority treatment and dedicated resources
- Immediate answers to critical questions (by Nov 15)
- Fast SOW turnaround (by Nov 22)
- Prototype delivery commitment (Jan 31)
- Resynant dedicated validation team (Feb-Mar)

## Commercial Terms - Aligned Incentives

**To support this aggressive timeline, I'm prepared to offer:**

**1. Priority Production Commitment:**
- 50% deposit upon SOW approval (Nov 29) to secure priority slot
- Remaining 50% upon prototype delivery (Jan 31)

**2. Performance Incentives:**
- On-time delivery (Jan 31): $5,000 bonus
- Early delivery (Jan 24 or earlier): $7,500 bonus
- All Phase 1-2 milestones passed on first attempt: $2,500 bonus

**3. Production Commitment:**
- Letter of Intent for 10 production units upon prototype acceptance (Mar 31)
- Volume pricing negotiation for 50-100 units/year (2027+)
- Multi-year strategic partnership agreement

**4. Collaboration Commitment:**
- Weekly status calls every Monday 10am EST (Dec 2 onwards)
- Shared documentation repository
- On-site Per Vices engineer support during validation (1 week, Feb 1-7)

## What I Need from Per Vices This Week (Nov 11-15)

**URGENT - By November 15, 2025:**

✅ **Answers to all critical technical questions** (Section above)
- GPIO expander: Specs, timing data, cost, timeline
- FPGA CIC decimation: Feasibility, NRE estimate, timeline
- Frequency range: Confirmed 20-1400 MHz specs
- Performance: Rx NF, Tx power, phase noise

✅ **Evidence of capability for critical unknowns:**
- GPIO timing: Test data or oscilloscope measurements
- FPGA CIC: Example code or reference implementation
- PVAN-11: Sample packet captures or detailed documentation

✅ **Commitment assessment:**
- Can Per Vices commit to Jan 31, 2026 prototype delivery?
- What priority/resource commitment is required?
- What are primary risks to timeline from your perspective?

**Next Step - Technical Alignment Call:**
- **Proposed:** November 18 or 19, 2025
- **Duration:** 60-90 minutes
- **Attendees:** Brandon, Per Vices lead engineer, Chad Rienstra, Resynant technical lead
- **Agenda:**
  - Review answers to critical questions
  - Discuss proposed milestone approach
  - Align on SOW content and deliverables
  - Confirm timeline feasibility

## Why This Partnership Matters

**For Per Vices:**
- Strategic entry into NMR market (tens of thousands of legacy Varian systems worldwide)
- Multi-year production volume (50-100 units/year = $3M-6M annual revenue potential)
- Reference customer for scientific instrumentation applications
- Funded R&D for FPGA enhancements (CIC decimation, waveform looping)

**For Resynant:**
- Phase out dependence on aging, unsupportable legacy Varian technology
- Modern NMR capabilities and improved customer support
- Competitive differentiation with superior specifications
- Growth enabler for 2026-2027 market expansion

**Together:**
- We both succeed by delivering on-time, on-spec, and avoiding the complexity traps that killed the previous approach
- Clean technical architecture, clear milestones, aligned incentives

## Closing Thoughts

I've learned from the previous project attempt that **specificity is critical**. Vague commitments like "we'll investigate" or "it should be possible" lead to expensive failures.

The milestone structure I'm proposing de-risks the project for both of us:
- Per Vices gets clear acceptance criteria and incremental validation
- Resynant gets confidence that critical features actually work before production commitment
- Both companies avoid the "unknown unknowns" trap

The Crimson TNG platform is an excellent architectural fit for NMR. With clear milestones, specific commitments, and aligned incentives, this project should succeed.

I'm ready to move quickly if Per Vices can commit to this timeline. Week of Nov 11-15 is CRITICAL - actions taken this week determine project success.

Can we schedule a call this week (Nov 11-15) to discuss your responses and align on timeline commitment?

Best regards,

**Chad M. Rienstra, Ph.D.**
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932

---

## Attachments (7 files, ~170 pages):

1. executive_summary.md
2. requirements_summary.md
3. technical_requirements.md
4. use_case_scenarios.md
5. test_validation_plan.md
6. nmr_pulse_sequences.md
7. IMMEDIATE_ACTIONS.md
