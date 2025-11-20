# Executive Email to Brandon Malatest - Streamlined Version

---

**To:** brandon.m@pervices.com
**Subject:** $600K-850K Production Order (2026) - Crimson TNG for NMR - Technical Call This Week?
**Attachments:**
- executive_summary.md
- technical_requirements.md
- Technical_Appendix_Full_Milestones.md (detailed version of this email)
- [4 additional technical documents]

---

Brandon,

**I'm ready to issue a purchase order for a Crimson TNG-based NMR spectrometer prototype** (Jan 31, 2026 delivery target) representing the first step in a multi-year partnership:
- **10 production units in 2026:** $600K-850K revenue
- **50-100 units/year thereafter:** $3M-6M annual revenue potential
- **Multi-year strategic partnership** in the NMR instrumentation market

**This week matters:** To finalize the SOW by Nov 22, I need technical validation on three specific Crimson TNG capabilities. **Can we schedule a 60-90 minute technical alignment call Nov 18-19** with your lead engineer?

## Why This Partnership is Strategic for Per Vices

**Market opportunity:** 10,000+ legacy Varian NMR systems worldwide need modern replacements. We're the leading upgrade provider, and our customers are waiting.

**Funded R&D:** We'll pay for FPGA enhancements (CIC decimation filters, GPIO precision timing) that become Per Vices IP for future customers.

**Reference customer:** Scientific instrumentation vertical with predictable multi-year production volume.

**Aligned incentives:**
- 50% deposit secures priority Jan 31 delivery slot
- Performance bonuses for on-time/early delivery
- **Guaranteed production order:** Upon successful March 31 validation, Resynant issues Letter of Intent for 10 units ($600K-850K)

## What I Need from Per Vices by Nov 18

**Three critical technical validations** (I've attached 170 pages of detailed specs, but these are the show-stoppers):

### 1. GPIO Expander Board - Timing Precision Evidence
**Why it matters:** NMR requires ±100-200ns precision for RF amplifier blanking triggers.

**What I need:**
- Do you have an existing GPIO expander design (schematic/reference)?
- **Can you provide oscilloscope measurements showing ±100-200ns timing precision?**
- Electrical specs: 8-12 TTL channels (0-5V), <50ns jitter
- Cost and delivery timeline if included in Jan 31 prototype

**Red flag from previous project:** A vendor said GPIO timing "should be achievable" without proof - it became a blocker. I need evidence, not estimates.

### 2. FPGA CIC Decimation Filters - Feasibility Confirmation
**Why it matters:** Critical for achieving 17-20 bit dynamic range (vs. 16-bit ADC baseline).

**What I need:**
- Is CIC decimation currently in Crimson TNG FPGA firmware?
- If not, what's the NRE cost and timeline? Can it be delivered by Jan 31?
- **Can you provide example code or reference implementation?**
- FPGA resource availability (4-channel decimation, 325 MSPS → 10 MHz)

**Fallback acceptable:** Host-side decimation works for prototype, but FPGA implementation needed for production.

### 3. Multi-Channel Performance - Specifications Across 20-1400 MHz
**Why it matters:** NMR operates across 70:1 frequency range with strict phase coherency requirements.

**What I need:**
- **Confirmed frequency tuning range:** 20-1400 MHz (datasheet or sweep data)
- **Multi-channel phase coherency test data:** Prove <2° std dev across 4 Rx channels
- Rx noise figure, Tx output power across frequency range
- **PVAN-11 packet capture example:** 4-channel streaming with phase synchronization

## Commercial Structure

**Prototype Phase (Nov-Jan):**
- 50% deposit upon SOW approval (Nov 29) - secures Jan 31 delivery slot
- 50% upon prototype delivery (Jan 31)
- Delivery incentive: $5K on-time / $7.5K early

**Production Commitment (March-April):**
- 8-week validation testing (Feb-March) with quantitative acceptance criteria
- **Upon successful validation (March 31):** Letter of Intent for 10 production units
- Volume pricing negotiation for 50-100 units/year begins immediately

**Total Value:**
- Prototype + NRE: ~$150K-250K (depending on FPGA/GPIO scope)
- 10-unit production: $600K-850K
- Multi-year volume: $3M-6M/year at 50-100 units/year

## Why Crimson TNG is the Right Architecture

I evaluated alternatives (including a previous project with a different vendor that stalled). **Crimson TNG is fundamentally better:**

- **Purpose-built SDR** with factory-calibrated phase coherency (JESD204B) - not repurposed AWG
- **Well-defined PVAN-11 interface** over 10 GbE - proven data streaming
- **Established platform** with active customer base and support
- **Multi-channel synchronization** is a core strength, not an afterthought

The attached technical documentation (170 pages) demonstrates we've done our homework:
1. **executive_summary.md** - Business case, timeline, budget analysis
2. **technical_requirements.md** - Detailed specs (24 pages)
3. **use_case_scenarios.md** - NMR operational scenarios (28 pages)
4. **test_validation_plan.md** - Acceptance criteria (34 pages)
5. **Technical_Appendix_Full_Milestones.md** - Detailed milestone breakdown with phased validation approach

## Proposed Timeline

| Milestone | Target Date |
|-----------|-------------|
| **Technical validation call** | **Nov 18-19** |
| **SOW finalized** | **Nov 22** |
| **PO issued (50% deposit)** | **Nov 29** |
| **Prototype delivery** | **Jan 31, 2026** |
| **Validation complete** | **March 31, 2026** |
| **Production order (10 units)** | **April 2026** |

## Next Steps

**Can we schedule a 60-90 minute technical alignment call Nov 18-19?**

**Proposed agenda:**
- Review three validation questions (GPIO, FPGA CIC, multi-channel specs)
- Discuss phased milestone approach (incremental validation, Feb-March)
- Confirm Jan 31 delivery feasibility with your production schedule
- Align on SOW deliverables and acceptance criteria

**Attendees:**
- Per Vices: Brandon, lead engineer, project manager
- Resynant: Chad Rienstra, technical lead

**If the technical fit is confirmed, I'm ready to issue a PO by Nov 29** with 50% deposit to secure your January delivery slot.

I'm confident Crimson TNG is the right platform and Per Vices is the right partner. The attached technical documentation shows we understand the requirements and are serious about this partnership.

Looking forward to discussing this week.

Best regards,

**Chad M. Rienstra, Ph.D.**
President & CEO, Resynant, Inc.
chad@resynant.com
(217) 649-8932

---

## Why I'm Asking for Detailed Evidence

**Context you should know:** I invested significantly in a similar NMR modernization project with another vendor (Tabor Proteus AWG) that stalled due to underestimated technical unknowns. Critical capabilities like GPIO timing precision and phase cycling were assumed to work but weren't validated upfront.

**Lesson learned:** Front-load technical validation before commitment. If you have test data, schematics, or reference implementations, they give us confidence to proceed quickly. If something requires development, we need clear NRE scope and timeline.

**I want to proceed with Per Vices** - these questions help us get there confidently and quickly.

---

**P.S.** The phased milestone approach in the attached Technical_Appendix demonstrates how we'll validate each capability incrementally (Phases 1-4, Feb-March). This de-risks the project for both companies and provides clear acceptance gates.
