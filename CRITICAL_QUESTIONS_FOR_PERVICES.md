# Critical Questions for Per Vices - Quick Reference

**Deadline: November 15, 2025**
**Purpose:** These questions MUST be answered with specifics before SOW approval

---

## 🚨 TIER 1: SHOW-STOPPERS (Must have specific answers, not "we'll investigate")

### GPIO Expander Board

**Background:** GPIO timing was an "unknown" in previous project that became a blocker.

| Question | Why It Matters | Required Answer Type |
|----------|----------------|---------------------|
| Do you have an existing GPIO expander design? | Need proven solution, not R&D project | ✅ "Yes, here's schematic" or ❌ "Custom development required" |
| What is the measured timing precision? | ±100-200ns is critical for NMR | ✅ "Oscilloscope data shows 150±50ns" NOT ❌ "Should be achievable" |
| What is the jitter specification? | <50ns required for precision gating | ✅ "Measured jitter: 30ns over 1000 events" |
| How many GPIO channels available? | Need 8 minimum, 12 preferred | ✅ "12 channels standard" or ✅ "8 channels, expandable to 12" |
| Can it be included in Jan 31 delivery? | Timeline is critical | ✅ "Yes, standard delivery" or ⚠️ "Requires 2 week lead time" |
| What is the cost? | Budget planning | ✅ "$X,XXX per unit" |

**RED FLAGS:**
- ❌ "We'll need to investigate timing precision"
- ❌ "Should be possible to meet 100ns requirement"
- ❌ "We can look into GPIO options"

**GREEN FLAGS:**
- ✅ "Here's test data from previous customer implementation"
- ✅ "We have schematic and gerbers ready"
- ✅ "Timing validated with oscilloscope measurements"

---

### FPGA CIC Decimation Filters

**Background:** Critical for achieving 17-20 bit ENOB dynamic range requirement.

| Question | Why It Matters | Required Answer Type |
|----------|----------------|---------------------|
| Is CIC decimation in current FPGA firmware? | Prefer existing solution | ✅ "Yes, version X.X includes CIC" or ⚠️ "No, custom development" |
| What decimation factors are supported? | Need 32× (325 MSPS → 10 MHz) | ✅ "Configurable up to 64×" |
| How many channels? | Need 4× Rx channels | ✅ "4 channels standard" |
| What FPGA resources does it consume? | Need to fit in Arria V ST | ✅ "~15k LEs, ~700kB block RAM" |
| Can it be included in Jan 31 delivery? | Timeline critical | ✅ "Yes" or ⚠️ "Requires X weeks NRE" |
| What is NRE cost if custom development? | Budget planning | ✅ "$XX,XXX, Y weeks timeline" |

**Fallback Position:**
- Host-side decimation is acceptable for Phase 1
- But FPGA implementation strongly preferred for production

**RED FLAGS:**
- ❌ "We'll investigate CIC implementation"
- ❌ "Decimation should be straightforward"
- ❌ "FPGA has plenty of resources" (without specifics)

**GREEN FLAGS:**
- ✅ "CIC implemented in firmware v2.3, here's example config"
- ✅ "Here's reference code from previous decimation project"
- ✅ "FPGA utilization: 45% LEs, 60% block RAM with CIC"

---

## 🔶 TIER 2: IMPORTANT (Need clear answers for SOW scoping)

### Performance Specifications

| Parameter | Current Spec | Required Clarity |
|-----------|--------------|------------------|
| Frequency range | "To be confirmed" | ✅ "20-1400 MHz confirmed" with tuning steps |
| Rx noise figure | "TBD" | ✅ "NF = X dB @ [frequencies]" |
| Tx output power | "TBD" | ✅ "Pout = X dBm @ [frequencies]" |
| SFDR | Unknown | ✅ "SFDR = X dBc typical" |
| Phase noise | Unknown | ✅ "@10kHz offset: X dBc/Hz" |

**Why this matters:**
- Frequency range determines NMR field coverage
- Noise figure affects SNR with 30dB preamp
- Tx power determines amplifier requirements
- Phase noise affects spectral resolution

---

### PVAN-11 Data Format and Multi-Channel Operation

| Question | Why It Matters | Required Answer Type |
|----------|----------------|---------------------|
| Can you provide example packet captures? | Prove it works for 4 channels | ✅ Sample .pcap file or detailed hex dump |
| What is max sustained throughput? | 4 ch × 325 MSPS = high data rate | ✅ "X Gbps sustained, tested" |
| How is phase coherency encoded? | Need to reconstruct channel relationships | ✅ "Sample timestamp in header field Y" |
| Latency/jitter for timed commands? | Pulse timing precision | ✅ "Command latency: X μs ± Y μs" |

**Documentation required:**
- ✅ PVAN-11 spec (already have link: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/)
- ✅ Example UDP receiver code (Python or C++)
- ✅ Multi-channel synchronization app note

---

## 🟢 TIER 3: NICE-TO-HAVE (For planning, not blockers)

### Multi-Unit Synchronization (Future >4 Channel Systems)

- Architecture for synchronizing multiple Crimson TNG units
- Additional hardware required (clock distribution, etc.)
- Limitations on number of units
- **Not critical for initial 4-channel prototype**

### Waveform Looping / FPGA Buffering

- Hardware looping for decoupling sequences
- FPGA waveform buffer size
- **Acceptable for Phase 2 optimization**

### Advanced Features

- Real-time DSP capabilities
- Custom FPGA development services
- Long-term support model

---

## Decision Matrix: Should We Sign SOW?

### ✅ PROCEED if Per Vices provides:

| Criteria | Threshold |
|----------|-----------|
| GPIO timing | ✅ Specific data showing ±100-200ns (not "should work") |
| FPGA CIC | ✅ Exists in firmware OR detailed NRE estimate |
| Frequency range | ✅ Confirmed 20-1400 MHz coverage |
| PVAN-11 | ✅ Documentation + example code provided |
| Timeline | ✅ Commit to Jan 31, 2026 delivery |
| Cost | ✅ Within $500K budget (prototype + NRE + support) |

### ⚠️ NEGOTIATE if Per Vices provides:

| Red Flag | Mitigation |
|----------|-----------|
| GPIO timing "to be determined" | Request timing validation test BEFORE SOW signature |
| CIC "requires investigation" | Get NRE estimate + timeline, or accept host-side decimation |
| Frequency range "likely covers" | Require datasheet or test report confirmation |
| Cost exceeds $600K | Negotiate scope reduction or phase NRE |

### ❌ DO NOT PROCEED if Per Vices says:

| Show-Stopper | Why |
|--------------|-----|
| "We'll need to investigate GPIO timing" | Tabor failure repeated |
| "SCPI interface recommended" | Wrong architecture, too complex |
| "Frequency range depends on..." | Unclear specs = unclear capability |
| "Timeline depends on FPGA complexity" | Unbounded risk |
| Multiple "we'll look into it" responses | Too many unknowns = high failure risk |

---

## How to Evaluate Responses

### Pattern Recognition

**BAD responses (don't proceed):**
- "We'll investigate..."
- "Should be possible to..."
- "Depends on..."
- "We'll need to..."
- "Can look into..."

**GOOD responses (proceed with confidence):**
- "Here's test data showing..."
- "Implemented in firmware version..."
- "Here's schematic/code/documentation..."
- "Measured performance: [specific numbers]"
- "Delivered this to customer X in 2024"

### Evidence Requirements

| Claim | Acceptable Evidence |
|-------|---------------------|
| GPIO timing ±100ns | Oscilloscope screenshots, test report, previous customer data |
| FPGA CIC exists | Firmware version number, example config file, resource utilization report |
| Frequency range 20-1400 MHz | Datasheet, test report, frequency sweep plot |
| PVAN-11 multi-channel | Sample .pcap file, example receiver code, synchronization app note |
| Jan 31 delivery feasible | Project schedule, resource commitment, similar past delivery |

---

## Email Strategy for Brandon

### Subject Line Options

**Option 1 (Direct):**
"Critical Technical Questions - Need Answers by Nov 15 for SOW"

**Option 2 (Partnership):**
"Crimson TNG Partnership - Requirements & Proposed Milestones"

**Option 3 (Opportunity):**
"$3M-6M Annual NMR Market Opportunity - Technical Validation Questions"

### Opening Strategy

**DO:**
- State business opportunity clearly (1 prototype → 10 units → 50-100/year)
- Mention comprehensive specs attached (170 pages)
- Reference previous technical discussions (establish context)
- Create urgency (week of Nov 11-15 is critical)

**DON'T:**
- Bury critical questions in 10-page email
- Use vague language ("we'd like to understand...")
- Appear desperate or pressured
- Mention Tabor failure in opening (save for context section)

### Question Presentation Strategy

**DO:**
- Group by priority (Tier 1, 2, 3)
- State WHY each question matters
- Give examples of acceptable vs. unacceptable answers
- Provide context from previous project learnings
- Set clear deadline (Nov 15)

**DON'T:**
- Ask open-ended questions ("How does GPIO work?")
- Accept vague promises ("We'll investigate")
- Proceed without specific evidence
- Be afraid to say "this is a deal-breaker"

### Closing Strategy

**DO:**
- Propose technical alignment call (Nov 18-19)
- Offer commercial incentives (deposit, bonuses, LOI)
- Emphasize partnership opportunity
- Create path to yes (not just interrogation)

**DON'T:**
- End with "let me know your thoughts" (too passive)
- Give impression of shopping around
- Undercut negotiating position
- Forget to propose next steps

---

## Follow-Up Strategy

### If Responses Are Excellent (All Tier 1 with evidence)

**Timeline:**
- Nov 15: Receive responses
- Nov 18-19: Technical alignment call
- Nov 22: SOW draft from Per Vices
- Nov 29: SOW approval + PO issuance

**Tone:**
- Enthusiastic partnership
- Fast decision-making
- Clear commitment

### If Responses Are Mixed (Some specifics, some vague)

**Timeline:**
- Nov 15: Receive responses
- Nov 16-17: Internal assessment of gaps
- Nov 18-19: Technical call focused on gap resolution
- Nov 22-25: Request additional evidence for vague items
- Nov 29: Conditional SOW approval OR delay decision

**Tone:**
- Professional but firm
- Specific about what's missing
- Clear about decision criteria

### If Responses Are Vague (Multiple "we'll investigate")

**Timeline:**
- Nov 15: Receive responses
- Nov 16: Internal decision to pause
- Nov 18: Call to discuss concerns and set requirements
- Nov 25: Deadline for specific evidence
- Dec 2: Reassess or pursue alternative vendors

**Tone:**
- Professional and respectful
- Transparent about concerns
- Firm about evidence requirements
- Open to resuming if evidence provided

---

## Success Metrics

**Phase 0 is successful if:**
- ✅ All Tier 1 questions answered with specifics and evidence
- ✅ Per Vices commits to Jan 31, 2026 delivery
- ✅ GPIO timing proven with test data
- ✅ FPGA CIC either exists OR has clear NRE scope
- ✅ Cost within $500K budget
- ✅ Confidence level >80% for project success

**Phase 0 fails if:**
- ❌ Multiple "we'll investigate" responses
- ❌ GPIO timing unclear or unproven
- ❌ FPGA capabilities vague
- ❌ Timeline commitments soft
- ❌ Confidence level <60%

**In that case:**
- Don't sign SOW
- Request specific evidence before proceeding
- Consider alternative vendors (Ettus, Analog Devices, etc.)
- Avoid repeating Tabor failure pattern
