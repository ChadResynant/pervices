# Milestone Strategy Analysis
## How the Updated Email Merges Best Practices from Both Approaches

**Date:** November 20, 2025
**Purpose:** Document the strategic thinking behind the proposed milestone structure

---

## What We Learned from Tabor/OpenVNMRJ Failure

### The Good: Incremental Validation Approach

The Tabor milestones had an **excellent conceptual framework**:

```
1. Execute delay
2. Execute delay - pulse
3. Implement looping over delay - pulse
4. Execute delay - pulse - acquire
5. Implement time averaging via looping
6. Execute delay - pulse with markers (GPIO)
7. Implement phase cycling
8. Implement arrayed experiments
```

**Why this was smart:**
- Build complexity incrementally
- Validate each capability before proceeding
- Early detection of issues when they're cheap to fix
- Clear acceptance criteria at each step

### The Fatal Flaws: Why It Still Failed

**1. "Unknown Unknowns" Red Flags:**
```
"The biggest unknowns at this first stage include using markers,
looping, phase cycling, data acquisition, and experiment arraying.
We will need assistance from Tabor to resolve these issues."
```
Translation: **We don't know if this will actually work.**

**2. Vendor Dependency:**
- Critical features were "unknowns" that required vendor help
- No evidence of capability before starting
- Assumed vendor would solve problems (they didn't)

**3. Software Complexity:**
- OVJ PSG → UCODE file → TEproc translator → SCPI commands → Proteus
- 4+ abstraction layers between intent and execution
- Each layer = potential failure mode

**4. Wrong Hardware Platform:**
- Proteus is an AWG (Arbitrary Waveform Generator)
- Not designed for multi-channel phase-coherent NMR
- Repurposing tool for wrong job

**5. Legacy Integration Burden:**
- Trying to make OpenVNMRJ work with fundamentally different hardware
- Backward compatibility constrained design choices

---

## How Updated Milestone Strategy Fixes These Issues

### Fix #1: Front-Load the "Unknown Unknowns"

**Tabor Approach (Failed):**
- Deferred critical questions to "we'll need vendor assistance"
- Markers, looping, phase cycling were "biggest unknowns"
- No validation before signing SOW

**Updated Approach (Phase 0):**
```
BEFORE signing SOW, Per Vices must provide:
✅ GPIO expander specs WITH timing test data (not "should work")
✅ FPGA CIC feasibility WITH code examples (not "we'll investigate")
✅ PVAN-11 packet captures (prove it works)
✅ Confirmed frequency range specs (not TBD)
```

**Why this works:**
- No signature until critical capabilities are PROVEN
- Evidence-based decision, not promises
- Vendor demonstrates capability upfront

### Fix #2: De-Risk Critical Features Early (Phase 1-2)

**Tabor Approach:**
- Milestones didn't explicitly validate the "unknowns"
- GPIO timing, phase cycling, looping were assumed

**Updated Approach - Explicitly Test Critical Unknowns:**

**Milestone 1.2: GPIO Timing Validation** ⭐
- Test ±100-200ns precision requirement
- Measure jitter with oscilloscope
- 1000 trigger events to validate consistency
- **PASS/FAIL gate before proceeding**

**Milestone 2.2: Looping and Time Averaging** ⭐
- Validate no data loss across 100 scans
- Prove timing doesn't drift
- **Addresses Tabor "unknown"**

**Milestone 2.4: Phase Cycling** ⭐
- Test 4-step phase cycle precision
- Validate <0.1° error
- **Addresses Tabor "unknown"**

**Why this works:**
- Critical features tested in weeks 1-4 (not deferred)
- Quantitative acceptance criteria
- Fail fast if there are fundamental issues

### Fix #3: Leverage Per Vices Platform Strengths

**Tabor Weakness:**
- AWG repurposed for NMR
- Phase coherency unclear
- Multi-channel sync uncertain

**Per Vices Strengths:**
- Purpose-built SDR for phase-coherent applications
- Factory-calibrated JESD204B synchronization
- Proven 10 GbE streaming interface

**Updated Milestones Leverage This:**

**Milestone 1.3: Multi-Channel Phase Coherency**
- Should PASS easily (factory calibrated)
- But validate anyway (<2° std dev)
- **Confidence builder, not risk item**

**Milestone 1.1: Basic Network Operation**
- PVAN-11 is documented format
- 10 GbE is proven Per Vices strength
- **Low risk, establishes baseline**

### Fix #4: Simpler Software Architecture

**Tabor Architecture (4+ layers):**
```
OVJ PSG → UCODE files → TEproc translator → SCPI commands → Proteus
```

**Updated Architecture (2-3 layers):**
```
Pulse Sequence Compiler → Waveform Buffers + Command API → Crimson TNG
                                                              ↓
                                                         PVAN-11 UDP
                                                              ↓
                                                         Data Processing
```

**Why this works:**
- Fewer translation layers = fewer failure modes
- Direct API to hardware (not SCPI abstraction)
- Fresh software designed for platform (no OpenVNMRJ baggage)

### Fix #5: Clear Acceptance Gates and Go/No-Go Decisions

**Tabor Approach:**
- "First major milestone focuses on RF transmit and receive"
- Vague success criteria
- No clear go/no-go gates

**Updated Approach:**
```
MUST-PASS CRITERIA (March 31, 2026):
✅ Phase coherency: <2° standard deviation
✅ GPIO timing: ±100-200 ns precision, <50 ns jitter
✅ Dynamic range: ENOB ≥17 bits @ 5 MHz
✅ NMR SNR: >50:1 on adamantane
✅ Data throughput: <0.01% packet loss
✅ CP and decoupling: Functional

If ANY must-pass fails → No-Go on production commitment
```

**Why this works:**
- Quantitative, testable criteria
- Clear business decision point (Mar 31)
- No ambiguity about acceptance

---

## Side-by-Side Comparison

| Aspect | Tabor Approach | Updated Per Vices Approach |
|--------|----------------|----------------------------|
| **Incremental validation** | ✅ Good concept | ✅ Adopted and improved |
| **Critical unknowns** | ❌ Deferred to vendor | ✅ Front-loaded in Phase 0 |
| **GPIO timing** | ❌ "Need Tabor assistance" | ✅ Validated in Milestone 1.2 |
| **Phase cycling** | ❌ "Biggest unknown" | ✅ Validated in Milestone 2.4 |
| **Looping** | ❌ "Biggest unknown" | ✅ Validated in Milestone 2.2 |
| **Hardware platform** | ❌ AWG repurposed | ✅ Purpose-built SDR |
| **Software layers** | ❌ 4+ abstraction layers | ✅ 2-3 clean layers |
| **Data interface** | ❌ SCPI (unclear) | ✅ PVAN-11 (documented) |
| **Acceptance criteria** | ❌ Vague | ✅ Quantitative must-pass |
| **Go/No-Go gate** | ❌ Not defined | ✅ March 31, 2026 |
| **Evidence before SOW** | ❌ Trust vendor | ✅ Require proof |

---

## What Makes This Strategy Better

### 1. Risk Reduction Through Early Validation

**Week 1-2 (Phase 1):**
- Test the three "Tabor unknowns": GPIO, phase coherency, basic operation
- If anything fails, only 2 weeks invested (not 6 months)

**Week 3-4 (Phase 2):**
- Test the other "Tabor unknowns": looping, phase cycling
- Still only 1 month invested if we hit a wall

**Week 5-8 (Phase 3-4):**
- Real NMR validation with known-working hardware
- Lower risk because basics are proven

### 2. Evidence-Based Decisions, Not Promises

**Tabor trap:**
- "We will need assistance from Tabor to resolve these issues"
- Proceeded based on vendor promises

**Updated approach:**
- Phase 0: Require evidence BEFORE signing SOW
- Phase 1-4: Test and measure, don't assume
- March 31: Go/No-Go based on quantitative data

### 3. Fail-Fast Philosophy

**If Per Vices can't answer Phase 0 questions with specifics:**
- Don't sign SOW
- Avoid 6-month expensive failure
- Cost: $0 (just time spent on specs)

**If Phase 1 Milestone 1.2 fails (GPIO timing):**
- Only 2 weeks + prototype cost invested
- Identify fix or pivot quickly
- Cost: ~$50K-100K (prototype + 2 weeks labor)

**If Phase 4 Milestone 4.3 fails (dynamic range):**
- 8 weeks + prototype cost invested
- But have validated all other features work
- Know exactly what needs fixing
- Cost: ~$200K (prototype + 8 weeks validation)

vs.

**Tabor approach:**
- 6 months invested before discovering GPIO/looping/phase cycling issues
- Complexity makes root cause unclear
- Sunk cost fallacy drives bad decisions

### 4. Aligned Incentives with Commercial Terms

**Proposed incentives:**
- $5K bonus for on-time delivery (Jan 31)
- $7.5K bonus for early delivery
- $2.5K bonus for Phase 1-2 milestones passed on first attempt

**Why this works:**
- Per Vices rewarded for hitting critical early milestones
- Encourages thorough testing before delivery
- Small enough not to distort business relationship
- Large enough to matter for project manager

**Plus production commitment:**
- 50% deposit secures priority slot
- LOI for 10 units upon acceptance creates partnership incentive
- Multi-year volume creates shared success

---

## Timeline Comparison

### Tabor Estimated Timeline

```
Major Milestone 1: Run ahX experiment from OVJ
Expected: 3-6 months
Reality: Project stalled after ~12-18 months (appears abandoned by mid-2024)
```

### Updated Per Vices Timeline

```
Phase 0: Pre-SOW validation          Nov 11-29  (3 weeks)
Phase 1: Hardware validation         Feb 1-14   (2 weeks)  ← Critical unknowns
Phase 2: Basic sequences             Feb 15-28  (2 weeks)  ← Critical unknowns
Phase 3: NMR integration             Mar 1-14   (2 weeks)
Phase 4: Advanced sequences          Mar 15-31  (2 weeks)
Gate: Acceptance decision            Mar 31     (8 weeks total validation)
Production release                   May 31     (+8 weeks)

Total: 6.5 months from requirements to production
```

**Why this timeline is achievable (unlike Tabor's):**
- Phase 0 eliminates "unknowns" before starting
- Per Vices platform strengths reduce risk
- Simpler software architecture
- Clear acceptance criteria at each phase
- Incremental validation allows parallel work

---

## Key Success Factors

### 1. Phase 0 is Non-Negotiable

**If Per Vices responses to critical questions are vague:**
- "We'll investigate GPIO timing" → ❌ Don't proceed
- "CIC decimation should be possible" → ❌ Not good enough
- "SCPI interface for..." → ❌ Wrong architecture

**Required responses:**
- "Here's oscilloscope data showing 100ns GPIO precision" → ✅
- "CIC decimation exists in firmware version X, here's example code" → ✅
- "PVAN-11 packet format documented at [link], here's sample capture" → ✅

### 2. Milestone Acceptance Criteria Must Be Quantitative

❌ **Bad:** "GPIO timing is acceptable"
✅ **Good:** "GPIO timing measured at 150±50ns over 1000 events, jitter <30ns"

❌ **Bad:** "Phase coherency is good"
✅ **Good:** "4-channel phase std dev = 1.2°, meets <2° requirement"

❌ **Bad:** "NMR signal acquired successfully"
✅ **Good:** "Adamantane SNR = 85:1, exceeds 50:1 requirement"

### 3. Software Architecture Must Stay Simple

**Allow 3 layers maximum:**
1. High-level pulse sequence description
2. Compiler to waveform buffers + API commands
3. Crimson TNG hardware execution

**Red flags:**
- Intermediate file formats (like UCODE)
- Translation programs (like TEproc)
- Abstraction layers for "flexibility"
- Legacy compatibility shims

### 4. Vendor Relationship Based on Evidence, Not Trust

**Trust but verify:**
- Per Vices has excellent SDR platform (trust)
- But require proof for NMR-specific capabilities (verify)
- Evidence before commitment, testing after delivery

**Tabor mistake:**
- Trusted vendor to solve unknowns
- Vendor couldn't deliver
- Project collapsed

---

## Risk Mitigation Summary

| Risk | Tabor Approach | Updated Approach | Mitigation Effectiveness |
|------|----------------|------------------|-------------------------|
| GPIO timing inadequate | Deferred, "need assistance" | Phase 0 + Milestone 1.2 | ✅ HIGH |
| Phase cycling unclear | "Biggest unknown" | Phase 0 + Milestone 2.4 | ✅ HIGH |
| Hardware looping issues | "Biggest unknown" | Milestone 2.2 validation | ✅ HIGH |
| Data acquisition problems | "Need assistance" | Milestone 1.1 + PVAN-11 | ✅ HIGH |
| Software complexity | 4+ layers accepted | 2-3 layer maximum | ✅ HIGH |
| Dynamic range below spec | Not addressed | Milestone 4.3 + CIC FPGA | ⚠️ MEDIUM |
| Vendor capability unclear | Trusted promises | Phase 0 evidence required | ✅ HIGH |
| Cost/schedule overrun | Optimistic 3-6mo | Phased gates with go/no-go | ✅ MEDIUM |

---

## Conclusion: Why This Should Succeed

**The Tabor approach had the right idea** (incremental validation) **but failed on execution:**
- Deferred critical unknowns instead of front-loading them
- Trusted vendor capabilities without evidence
- Complex software architecture with too many layers
- Wrong hardware platform (AWG not designed for NMR)

**The updated Per Vices approach fixes all of these:**
- ✅ Front-loads unknowns in Phase 0 (require evidence before SOW)
- ✅ Validates critical features in Phase 1-2 (fail fast if issues)
- ✅ Simpler software architecture (2-3 layers, not 4+)
- ✅ Purpose-built SDR platform (factory phase coherency)
- ✅ Clear acceptance gates (quantitative must-pass criteria)
- ✅ Aligned incentives (bonuses + production LOI)

**Success probability:**
- Tabor approach: 20-30% (failed)
- Updated approach: 70-80% (if Phase 0 answers are solid)

**The critical gate is Phase 0:**
- If Per Vices provides specific, evidence-based answers → Proceed
- If answers are vague or "we'll investigate" → Don't sign SOW

**The project will succeed or fail in the first 4 weeks of validation:**
- Phase 1-2 tests all the "Tabor unknowns"
- If we pass Phase 2 (by Feb 28), we're 90% likely to succeed
- If Phase 2 reveals issues, we've only invested 1 month + prototype cost

This is how you execute a high-risk technical project: **incremental validation, evidence-based decisions, and fail-fast gates.**
