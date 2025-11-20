# PROJECT GANTT CHART
## NMR Spectrometer SDR Development
### Visual Timeline: November 2025 - June 2026

---

## TIMELINE OVERVIEW

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════
PHASE / MILESTONE                          │ NOV │ DEC │ JAN │ FEB │ MAR │ APR │ MAY │ JUN │
                                           │2025 │2025 │2026 │2026 │2026 │2026 │2026 │2026 │
═══════════════════════════════════════════════════════════════════════════════════════════════════════

PHASE 0: REQUIREMENTS & SOW (CRITICAL PATH)
├─ Requirements Complete                   │█████│     │     │     │     │     │     │     │
├─ Per Vices Technical Review              │ ███ │     │     │     │     │     │     │     │
├─ SOW Development                         │  ███│     │     │     │     │     │     │     │
└─ ◆ SOW APPROVAL (Nov 29)                 │   ◆ │     │     │     │     │     │     │     │
───────────────────────────────────────────────────────────────────────────────────────────────────────

PHASE 1: PROTOTYPE DEVELOPMENT (CRITICAL PATH)
Hardware Development
├─ Crimson TNG Assembly                    │     │█████│███  │     │     │     │     │     │
├─ GPIO Expander Design                    │     │████ │     │     │     │     │     │     │
└─ GPIO Fabrication & Integration          │     │ ████│██   │     │     │     │     │     │

FPGA Development  
├─ CIC Decimation Development              │     │█████│████ │     │     │     │     │     │
└─ FPGA Testing & Validation               │     │     │███  │     │     │     │     │     │

Software Development (PARALLEL)
├─ UDP Receiver & Data Pipeline            │     │████ │     │     │     │     │     │     │
├─ Pulse Sequence Compiler                 │     │     │████ │     │     │     │     │     │
└─ Control Interface                       │     │     │████ │     │     │     │     │     │

Factory Testing                            │     │     │███  │     │     │     │     │     │
└─ ◆ PROTOTYPE DELIVERY (Jan 31)           │     │     │  ◆  │     │     │     │     │     │
───────────────────────────────────────────────────────────────────────────────────────────────────────

PHASE 2: PROTOTYPE VALIDATION (CRITICAL PATH)
├─ Bench Testing (Electrical)              │     │     │     │████ │     │     │     │     │
├─ System Integration (First NMR Signal)   │     │     │     │ ████│     │     │     │     │
├─ Multi-Channel Validation                │     │     │     │     │████│     │     │     │
├─ Performance Characterization            │     │     │     │     │ ███│     │     │     │
└─ ◆ VALIDATION COMPLETE (Mar 31)          │     │     │     │     │   ◆│     │     │     │
───────────────────────────────────────────────────────────────────────────────────────────────────────

PHASE 3: PRODUCTION READINESS (CRITICAL PATH)
FPGA Optimization (Conditional)
└─ Waveform Looping Development            │     │     │     │     │     │████ │     │     │

Software Integration (CRITICAL)
├─ Harmonyzer Integration                  │     │     │     │     │█████│█████│     │     │
├─ Advanced Features                       │     │     │     │     │  ███│████ │     │     │
└─ User Interface                          │     │     │     │     │   ██│████ │     │     │

Documentation & Training
├─ System Documentation                    │     │     │     │     │     │ ████│███  │     │
├─ Training Materials                      │     │     │     │     │     │  ███│██   │     │
└─ Production Procedures                   │     │     │     │     │     │   ██│███  │     │

└─ ◆ PRODUCTION RELEASE (May 31)           │     │     │     │     │     │     │  ◆  │     │
───────────────────────────────────────────────────────────────────────────────────────────────────────

PHASE 4: INITIAL PRODUCTION
├─ Units 1-5 Manufacturing                 │     │     │     │     │     │     │     │█████│
├─ Units 6-10 Manufacturing                │     │     │     │     │     │     │     │ ████│
├─ Customer Deployments                    │     │     │     │     │     │     │     │  ███│
└─ ◆ FIRST PRODUCTION UNITS (Jun 30)       │     │     │     │     │     │     │     │   ◆ │
═══════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## CRITICAL MILESTONES

| # | Milestone | Date | Week | Critical? |
|---|-----------|------|------|-----------|
| 1 | SOW Approval & Project Kickoff | Nov 29, 2025 | Week 3 | ✓ YES |
| 2 | Prototype Delivery | Jan 31, 2026 | Week 12 | ✓ YES |
| 3 | First NMR Signal Acquired | Feb 18, 2026 | Week 15 | ✓ YES |
| 4 | Validation Complete & Acceptance | Mar 31, 2026 | Week 20 | ✓ YES |
| 5 | Production Release | May 31, 2026 | Week 29 | ✓ YES |
| 6 | First Production Units Deployed | Jun 30, 2026 | Week 34 | - |

---

## CRITICAL PATH (29 weeks)

**Path:** Requirements → SOW → Prototype Dev → Validation → Production Readiness → Release

**Cannot be delayed without affecting final delivery date.**

Activities NOT on critical path:
- Software development (Dec-Jan) - parallel with prototype
- FPGA optimization (Apr) - optional enhancement
- Documentation (Apr-May) - can overlap with testing

---

## LEGEND

Symbol | Meaning
-------|--------
█████  | Active work period (~1 week per block)
◆      | Major milestone/decision point
✓      | Critical path activity (cannot delay)

---

**For detailed activity breakdown, see WORK_BREAKDOWN_STRUCTURE.md**
**For detailed schedule, see PROJECT_SCHEDULE.md**
**For risk analysis, see RISK_REGISTER.md**

