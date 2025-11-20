# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains comprehensive technical specifications and project documentation for developing a Software-Defined Radio (SDR) transmitter/receiver system for the Resynant Harmonyzer high-resolution solid-state NMR (Nuclear Magnetic Resonance) spectrometer. The system will use the Per Vices Crimson TNG SDR platform to replace legacy Varian DDR technology.

**Project Status:** Requirements complete (Nov 2025); awaiting Per Vices SOW and prototype development
**Target Timeline:** Prototype delivery Jan 2026, production release May 2026

## Business Context

- **Customer:** Resynant, Inc. (NMR spectrometer manufacturer)
- **Vendor:** Per Vices Corporation (Crimson TNG SDR platform)
- **Application:** High-resolution solid-state NMR spectroscopy (20 MHz - 1.4 GHz)
- **Volume:** 1 prototype → 10 initial units → 50-100 units/year production

## Historical Context: Lessons from Failed Previous Approach

**IMPORTANT:** This is the second attempt to modernize Resynant's NMR platform. Understanding why the first attempt failed is critical to avoiding similar pitfalls.

### Previous Attempt: Tabor Proteus + OpenVNMRJ (2023-2024)

**Approach:**
- **Platform:** Tabor Proteus (Arbitrary Waveform Generator repurposed for NMR)
- **Software:** Integration with OpenVNMRJ (open-source Varian software fork)
- **Control:** SCPI commands over TCP/IP
- **Architecture:** OVJ PSG → UCODE intermediate format → TEproc translator → SCPI commands → Proteus AWG
- **Partners:** Open VnmrJ Solutions LLC (Dan Iverson), Tabor Electronics (Mark Elo, Alex Palm)
- **Funding Plan:** NSF SBIR/STTR grant application (June 2024)

**Why It Failed:**

1. **Software Complexity Overload**
   - Required modifying multiple layers of OpenVNMRJ architecture (PSG, procs, Sendproc, Recvproc)
   - Created new translation layer (TEproc) to convert UCODE → SCPI commands
   - Too many abstraction layers between pulse sequence intent and hardware execution

2. **"Unknown Unknowns" Red Flags**
   - Milestone documents repeatedly stated: "The biggest unknowns concern programming the Proteus system"
   - Critical gaps: markers/GPIO, hardware looping, phase cycling, data acquisition, experiment arraying
   - Quote: "We will need assistance from Tabor to resolve these issues" ← vendor dependency risk

3. **AWG Not Designed for NMR**
   - Proteus is an Arbitrary Waveform Generator being repurposed for NMR applications
   - Lacks built-in phase-coherent multi-channel architecture
   - GPIO/marker functionality unclear and not NMR-optimized

4. **Legacy Software Burden**
   - Attempting to integrate modern hardware (Proteus) with legacy architecture (OpenVNMRJ)
   - OpenVNMRJ designed for Varian console architecture, fundamentally different from AWG approach
   - Backward compatibility constraints limited design flexibility

5. **Optimistic Timeline**
   - Estimated 3-6 months to first milestone (ahX experiment)
   - Given the "unknowns" mentioned, timeline was unrealistic
   - Project appears to have stalled by mid-2024

**Documents in Repository:**
- `Milestones.pdf` - Initial milestone planning (incremental SCPI development approach)
- `Milestones2 V1.0-cmr.pdf` - Phase 1 proof of concept milestones
- `Tabor_UWMadison_SBIR_STTR_Planning.docx` - NSF grant planning (June 2024)

### Why Per Vices Crimson TNG Approach Is Different (and Better)

**1. Purpose-Built SDR vs. Repurposed AWG**
- Crimson TNG designed for multi-channel phase-coherent applications (radar, communications)
- Factory-calibrated JESD204B synchronization across all Tx/Rx channels
- Not trying to force an AWG to behave like an NMR console

**2. Simpler Software Architecture**
- Direct UDP streaming over 10 GbE (PVAN-11 format) - no SCPI translation layer
- Build fresh software optimized for Crimson TNG, not constrained by OpenVNMRJ legacy
- Fewer abstraction layers: Pulse Sequence Compiler → Waveform Buffers → Crimson TNG API

**3. Well-Defined Data Interface**
- PVAN-11 packet format documented by Per Vices
- Established network streaming vs. uncertain SCPI command/response patterns
- Proven 10 GbE throughput for high-bandwidth data acquisition

**4. Established SDR Platform**
- Crimson TNG has existing customer base in similar applications
- Per Vices has experience with multi-channel synchronization challenges
- Platform actively developed and supported

**5. Clear Customization Scope**
- GPIO expander board: Well-defined electrical/timing requirements
- FPGA CIC decimation: Understood signal processing task
- No fundamental architectural unknowns like Tabor approach had

**6. Realistic Risk Assessment**
- Current requirements documents explicitly identify gaps and verify status (✅/⚠️/❌)
- Phased approach with validation gates before full production commitment
- Acknowledges moderate FPGA development complexity upfront

### Critical Lessons for This Project

**DO:**
- Keep software architecture as simple as possible - minimize abstraction layers
- Build fresh software optimized for the platform, not forced integration with legacy
- Define clear acceptance criteria and validate incrementally
- Maintain multiple vendor options if Per Vices encounters blockers
- Front-load the "unknown unknowns" - identify gaps early in SOW phase

**DON'T:**
- Create complex translation layers (UCODE → TEproc → SCPI pattern was a trap)
- Assume vendor will resolve unclear technical challenges - get specifics in SOW
- Underestimate timeline when "unknowns" are mentioned repeatedly
- Try to preserve backward compatibility with legacy systems at expense of clean design
- Proceed without well-defined data interfaces and control mechanisms

**Warning Signs to Watch For:**
- If Per Vices starts saying "we'll need to investigate how to..." for critical features
- If custom FPGA work scope becomes vague or open-ended
- If GPIO timing or data acquisition has "unknowns" after SOW
- If software architecture requires >3 translation/abstraction layers

The Tabor project likely collapsed under its own complexity. The Per Vices approach is architecturally cleaner, but vigilance is required to keep it that way.

## Documentation Structure

This repository contains ~170 pages of technical specifications across 7 core documents:

1. **executive_summary.md** - Business case, timeline, budget, risk assessment, next steps
2. **IMMEDIATE_ACTIONS.md** - Critical action plan for project kickoff (week-by-week tasks)
3. **requirements_summary.md** - Requirements traceability matrix and gap analysis
4. **technical_requirements.md** - Detailed system specifications (channels, frequency, dynamic range, GPIO, timing)
5. **use_case_scenarios.md** - Operational scenarios and data flow for NMR pulse sequences
6. **test_validation_plan.md** - Acceptance testing procedures and criteria (4 phases)
7. **nmr_pulse_sequences.md** - Detailed pulse sequence specifications for FPGA waveform generation

**Additional Resources:**
- Case study PDFs: GPS/GNSS, Napatech, Radar, Spectrum applications
- Email thread archive with Per Vices
- Screenshots of technical discussions

## Key Technical Requirements

### Hardware Platform: Per Vices Crimson TNG

**Core Specifications:**
- 4 Tx + 4 Rx channels (phase-coherent, factory-calibrated)
- Frequency range: 20-1400 MHz (verification needed)
- Sample rate: 325 MSPS (ADC16DX370, DAC38J84)
- Data interface: 10 GbE (SFP+)
- Reference: OCXO (5 ppb stability)
- FPGA: Altera Arria V ST

**Critical Customizations Required:**
1. **GPIO Expander Board:** 8-12 TTL channels (0-5V), ±100-200ns timing precision
2. **FPGA CIC Decimation:** 4-channel decimation filters (325 MSPS → 10 MHz) for enhanced dynamic range
3. **FPGA Waveform Buffering:** Hardware looping for decoupling sequences (Phase 2 optimization)

### Performance Requirements

| Parameter | Specification | Status |
|-----------|---------------|---------|
| Channels | 4 Tx + 4 Rx | ✅ Met |
| Frequency | 20-1400 MHz | ⚠️ Verify |
| Phase Coherency | Deterministic, <2° std dev | ✅ Met (JESD204B) |
| Dynamic Range (ENOB) | 17-bit @ 5MHz, 19-bit @ 1MHz, 20-bit @ 100kHz | ⚠️ Requires FPGA CIC |
| GPIO Timing | ±100-200ns precision, <50ns jitter | ⚠️ Custom board |
| Sample Rate | 325 MSPS | ✅ Met |

## Architecture

### Signal Flow (Receive Path)

```
NMR Probe → Preamplifier (+30dB) → Crimson TNG Rx Input
                                          ↓
                                    ADC (16-bit, 325 MSPS)
                                          ↓
                                    FPGA DDC + CIC Decimation
                                          ↓
                                    10 GbE Network (PVAN-11 format)
                                          ↓
                                    Linux Host (UDP receiver)
                                          ↓
                                    Host-side FIR Filtering
                                          ↓
                                    NMR Data Processing
```

### Signal Flow (Transmit Path)

```
Linux Host (Waveform Generation)
       ↓
10 GbE Network → Crimson TNG FPGA Buffers
                         ↓
                   DAC (16-bit, 325 MSPS)
                         ↓
                   RF Output → Power Amplifier → NMR Probe
                         ↓
                   GPIO Trigger (Tx gate, ±100ns precision)
```

### Data Format: PVAN-11 Specification

Crimson TNG uses Per Vices proprietary PVAN-11 UDP packet format:
- Documentation: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
- Packet structure: Header (metadata) + I/Q samples (16-bit complex)
- Streaming: Continuous UDP over 10 GbE SFP+ interface

**Software must:**
- Parse PVAN-11 packets (UDP receiver)
- Extract I/Q data and reconstruct time-domain signal
- Handle real-time streaming without packet loss (<0.01% tolerance)

## NMR-Specific Concepts

### Pulse Sequences

NMR experiments use precise sequences of RF pulses and acquisition windows:

1. **Single-Pulse (Simplest):** One Tx pulse → acquire Rx FID (free induction decay)
2. **Cross-Polarization (CP):** Transfer magnetization between nuclei (e.g., 1H → 13C)
3. **Decoupling:** Continuous Tx on one channel during Rx on another
4. **Multi-dimensional:** Complex sequences with phase cycling and multiple acquisition periods

**Key Requirements:**
- Timing precision: ±1 μs for pulse events, ±100 ns for GPIO triggers
- Phase control: 0.1° precision, deterministic across channels
- Waveform types: Rectangular, Gaussian, WURST, adiabatic ramps

### Critical Terms

- **ENOB:** Effective Number of Bits (dynamic range measure)
- **FID:** Free Induction Decay (NMR signal after RF pulse)
- **CP:** Cross-Polarization (magnetization transfer technique)
- **Decoupling:** RF irradiation to remove spin-spin interactions
- **CIC Filter:** Cascaded Integrator-Comb (efficient decimation filter for FPGA)
- **TPPM/SPINAL:** Advanced decoupling sequences with phase/amplitude modulation

## Software Development

### Phase 1: Prototype Software (Dec 2025 - Jan 2026)

**Components to Develop:**

1. **UDP Data Receiver (Priority 1)**
   - Parse PVAN-11 packet format
   - Real-time I/Q data extraction
   - Ring buffer for streaming acquisition
   - Language: Python (prototyping) or C++ (performance)

2. **Pulse Sequence Compiler**
   - Input: High-level NMR sequence description
   - Output: Timed waveform buffers + GPIO trigger schedule
   - Must support: Rectangular pulses, phase shifts, amplitude modulation

3. **Control Interface**
   - Crimson TNG API wrapper for frequency, power, timing control
   - Timed command execution (trigger pulse sequences)
   - Status monitoring and error handling

4. **Data Processing Pipeline**
   - Host-side FIR filtering (decimation to final bandwidth)
   - FFT for spectral analysis
   - Integration with Harmonyzer control system

**Development Timeline:**
- Weeks 1-2: UDP receiver + packet parsing
- Weeks 3-4: Data processing (I/Q → FID)
- Weeks 5-6: Pulse sequence compiler (basic rectangular pulses)
- Weeks 7-8: Control interface + API integration
- Weeks 9-12: Testing with simulator, ready for hardware (Feb 1)

### Phase 2: Production Software (Apr-May 2026)

- Harmonyzer system integration
- Advanced pulse sequences (shaped pulses, phase cycling)
- Calibration and performance optimization
- User interface and documentation

## Testing and Validation

### 4-Phase Test Plan (Feb-Mar 2026, 8 weeks)

**Phase 1: Bench Testing (No NMR magnet, 2 weeks)**
- Electrical interfaces, network throughput
- GPIO timing precision (oscilloscope measurement)
- Basic Tx/Rx loopback tests

**Phase 2: NMR Integration (With magnet, 2 weeks)**
- Single-channel acquisition (adamantane standard sample)
- SNR measurement, phase coherency validation
- Frequency tuning and stability

**Phase 3: Multi-Channel Validation (2 weeks)**
- CP experiments (1H → 13C magnetization transfer)
- Decoupling performance (TPPM sequence)
- Multi-channel phase coherency

**Phase 4: Performance Characterization (2 weeks)**
- Dynamic range measurement (ENOB @ various bandwidths)
- Long-term stability (temperature, drift)
- Complex pulse sequences (multi-dimensional NMR)

**Acceptance Criteria (Must-Pass):**
- Phase coherency: <2° standard deviation
- Dynamic range: ENOB ≥17 bits @ 5 MHz bandwidth
- GPIO timing: ±100 ns precision, <50 ns jitter
- SNR: >50:1 on adamantane sample
- Data throughput: <0.01% packet loss

## Project Management

### Critical Milestones

| Milestone | Target Date | Status |
|-----------|-------------|---------|
| Requirements Complete | Nov 8, 2025 | ✅ Done |
| SOW from Per Vices | Nov 22, 2025 | ⏳ Pending |
| SOW Approval | Nov 29, 2025 | ⏳ Pending |
| Prototype Delivery | Jan 31, 2026 | ⏳ Pending |
| Validation Complete | Mar 31, 2026 | ⏳ Pending |
| Production Release | May 31, 2026 | ⏳ Pending |

### Immediate Next Steps (See IMMEDIATE_ACTIONS.md)

Week of Nov 11-15, 2025 is CRITICAL:
1. Submit documentation package to Per Vices (Brandon Malatest)
2. Reserve NMR magnet time (Feb-Mar 2026)
3. Inventory test equipment, create procurement plan
4. Assign project team (PM, NMR specialist, software engineer)
5. Obtain budget approval ($500K)
6. Order test samples (adamantane, glycine, alanine)
7. Set up project infrastructure (status calls, shared folders)
8. Begin software development (UDP receiver)

### Key Contacts

**Per Vices Corporation:**
- Brandon Malatest (COO): brandon.m@pervices.com, +1 (647) 534-9007

**Resynant, Inc.:**
- Chad Rienstra (CEO): chad@resynant.com, (217) 649-8932

## Common Development Commands

**No build system yet** - this is a requirements/documentation repository only.

When software development begins (Dec 2025):
- Language: Python (prototyping) or C++ (production)
- Version control: Git (this repository)
- Testing: Unit tests for packet parsing, integration tests with Crimson TNG simulator

## Working with This Repository

### When Adding Documentation

- Maintain markdown format consistency
- Update executive_summary.md for high-level changes
- Use technical_requirements.md for detailed specifications
- Cross-reference related sections across documents

### When Reviewing Requirements

- Check requirements_summary.md for traceability matrix
- Identify gaps with ✅ Met / ⚠️ Verify / ❌ Gap status indicators
- Review use_case_scenarios.md for operational context
- Reference test_validation_plan.md for acceptance criteria

### Understanding Technical Decisions

- Dynamic range strategy: FPGA CIC decimation (see technical_requirements.md Section 4)
- GPIO timing: Custom expander board approach (see technical_requirements.md Section 5)
- Waveform generation: Phase 1 streaming, Phase 2 FPGA buffering (see technical_requirements.md Section 6)

## Risks and Open Questions

### Critical Questions for Per Vices (Pending Responses)

1. GPIO expander: Specifications, cost, delivery timeline?
2. FPGA CIC decimation: Included in prototype or Phase 2?
3. Frequency range: Confirmed 20-1400 MHz coverage?
4. Noise figure: Rx performance specification?
5. Prototype delivery: Can Per Vices commit to Jan 31, 2026?

### Known Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dynamic range below 17-bit target | Low | High | FPGA CIC optimization; 32-bit float (extensive NRE) |
| GPIO timing precision insufficient | Low | High | FPGA timing optimization; external board (last resort) |
| Prototype validation extends timeline | Medium | Medium | Detailed test plan; early issue identification |
| SOW negotiation delays | Medium | Medium | Proactive engagement; clear requirements |

## Notes for Future Claude Instances

- This is a **hardware-software co-design project** for scientific instrumentation
- Requirements are mature and comprehensive (~170 pages) - avoid making assumptions
- NMR spectroscopy has strict phase coherency and timing requirements - precision matters
- The project is time-sensitive (accelerated 6-month timeline) - efficiency is critical
- When uncertain about NMR terminology or requirements, reference the detailed technical documents
- Per Vices Crimson TNG is an established SDR platform - respect vendor architecture and capabilities
