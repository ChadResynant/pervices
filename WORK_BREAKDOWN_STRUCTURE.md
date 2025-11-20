# WORK BREAKDOWN STRUCTURE (WBS)
## NMR Spectrometer SDR Development Project
### Per Vices Crimson TNG Platform for Resynant Harmonyzer

**Project Duration:** November 2025 - June 2026 (29 weeks to production)
**Total Work Packages:** 102

---

## 1.0 PHASE 0: REQUIREMENTS DEFINITION & SOW DEVELOPMENT

**Duration:** 3 weeks (Nov 8-29, 2025)
**Objective:** Complete requirements documentation and establish Statement of Work with Per Vices

### 1.1 Requirements Documentation & Analysis

#### 1.1.1 Technical Requirements Compilation
Consolidate NMR spectrometer requirements from email correspondence and existing Varian system specifications
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** technical_requirements.md (24 pages)

#### 1.1.2 Use Case Development
Document operational scenarios, pulse sequences, and data flow requirements for NMR applications
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** use_case_scenarios.md, nmr_pulse_sequences.md

#### 1.1.3 Validation Plan Development
Define comprehensive test procedures and acceptance criteria for prototype validation
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** test_validation_plan.md (34 pages)

#### 1.1.4 Gap Analysis
Analyze Crimson TNG capabilities against NMR requirements; identify customization needs
- **Responsible:** Resynant
- **Duration:** 3 days
- **Deliverable:** requirements_summary.md with gap analysis table

#### 1.1.5 Executive Summary Preparation
Create business case summary with timeline, costs, and risk assessment for stakeholder approval
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** executive_summary.md (13 sections, 600+ lines)

### 1.2 Vendor Engagement & Technical Review

#### 1.2.1 Documentation Package Submission
Submit complete requirements package to Per Vices for technical review
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Email with 6 specification documents to Brandon Malatest

#### 1.2.2 Per Vices Technical Assessment
Per Vices engineering team reviews requirements for feasibility and FPGA resource availability
- **Responsible:** Per Vices
- **Duration:** 3-5 business days
- **Deliverable:** Technical feasibility report with responses to critical questions

#### 1.2.3 GPIO Expander Specification
Define electrical specifications, timing precision, and design approach for TTL-compatible GPIO board
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** GPIO expander electrical specs, connector pinout, timing validation data

#### 1.2.4 FPGA Resource Assessment
Evaluate available FPGA logic elements and block RAM for CIC decimation and waveform buffering
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** FPGA resource allocation report with NRE estimates

#### 1.2.5 Technical Alignment Call
Joint Resynant-Per Vices discussion to clarify requirements, confirm feasibility, align on approach
- **Responsible:** Joint
- **Duration:** 60 minutes (Nov 18-19)
- **Deliverable:** Meeting notes with action items and technical decisions

### 1.3 Statement of Work (SOW) Development

#### 1.3.1 SOW Drafting
Per Vices prepares comprehensive SOW including deliverables, timeline, costs, acceptance criteria
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** SOW draft document (target delivery Nov 22)

#### 1.3.2 NRE Cost Estimation
Detailed non-recurring engineering cost breakdown for GPIO expander, FPGA development, factory testing
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** NRE cost breakdown with line-item justification

#### 1.3.3 Prototype Unit Pricing
Fixed price quote for Crimson TNG prototype including all customizations
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Prototype unit pricing with payment terms

#### 1.3.4 Production Volume Pricing
Volume pricing structure for 10-unit and 50-99 unit production quantities
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Tiered pricing table with volume discounts

#### 1.3.5 Timeline & Milestone Definition
Detailed project schedule with phase gates, delivery dates, and dependency mapping
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Project timeline with critical path analysis

### 1.4 SOW Negotiation & Approval

#### 1.4.1 Internal SOW Review
Resynant technical and legal review of Per Vices SOW against requirements and budget
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** SOW review checklist with negotiation points

#### 1.4.2 SOW Negotiation Call
Discuss modifications, finalize terms, agree on bonus/penalty structure for schedule performance
- **Responsible:** Joint
- **Duration:** 90 minutes (Nov 26)
- **Deliverable:** Agreed SOW revisions and final terms

#### 1.4.3 Budget Approval
Executive/board approval for $500K project budget including Per Vices costs and internal resources
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Budget approval authorization and PO authority

#### 1.4.4 SOW Signature & PO Issuance
Execute final SOW and issue purchase order to Per Vices to initiate prototype development
- **Responsible:** Joint
- **Duration:** 1 day (Nov 29 target)
- **Deliverable:** Signed SOW, issued PO, project kickoff scheduled

### 1.5 Project Infrastructure Setup

#### 1.5.1 Team Assignment
Identify and assign Project Manager, NMR Specialist, Software Engineer, Lab Technician roles
- **Responsible:** Resynant
- **Duration:** 3 days
- **Deliverable:** Project roster with confirmed availability

#### 1.5.2 Magnet Time Reservation
Reserve NMR magnet access at NMRFAM or Indiana University for Feb-Mar 2026 validation period
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Confirmed magnet reservation for 8 consecutive weeks

#### 1.5.3 Test Equipment Inventory
Inventory existing test equipment (oscilloscope, spectrum analyzer, signal generator); identify procurement needs
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Equipment inventory with procurement plan and budget

#### 1.5.4 Sample Procurement
Order NMR test samples (adamantane, glycine, alanine, KBr) with 2-4 week lead time
- **Responsible:** Resynant
- **Duration:** 1 day ordering + 3 weeks delivery
- **Deliverable:** Test samples received by mid-December

#### 1.5.5 Communication Infrastructure
Establish weekly status calls, shared document repository, communication channels
- **Responsible:** Resynant (Project Manager)
- **Duration:** 2 days
- **Deliverable:** Recurring meeting scheduled, shared folders created

---

## 2.0 PHASE 1: PROTOTYPE DEVELOPMENT

**Duration:** 8 weeks (Dec 2025 - Jan 31, 2026)
**Objective:** Per Vices develops and delivers customized Crimson TNG prototype

### 2.1 Hardware Platform Assembly

#### 2.1.1 Standard Crimson TNG Configuration
Assemble base Crimson TNG unit with 4 Tx/4 Rx channels, ADC16DX370, DAC38J84, OCXO
- **Responsible:** Per Vices
- **Duration:** 2 weeks
- **Deliverable:** Assembled Crimson TNG base unit

#### 2.1.2 Component Procurement
Order long-lead components (ADCs, DACs, FPGAs) and ensure priority production slot
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** Components in stock, production schedule confirmed

#### 2.1.3 Board-Level Integration
Integrate RF front-end, ADC/DAC boards, FPGA module, power supplies
- **Responsible:** Per Vices
- **Duration:** 2 weeks
- **Deliverable:** Fully integrated hardware assembly

#### 2.1.4 Clock Distribution Setup
Configure LMK04828 clock generator, OCXO reference, JESD204B subclass 1 synchronization
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** Phase-coherent clock distribution validated

#### 2.1.5 10GbE Interface Configuration
Configure SFP+ ports, 10GBASE-R transceivers, network interfaces for data and control
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** 10GbE interfaces tested and operational

### 2.2 GPIO Expander Board Development

#### 2.2.1 GPIO Expander Design
Design PCB for FPGA 2.5V to TTL 0-5V level conversion with 8-12 channels
- **Responsible:** Per Vices
- **Duration:** 2 weeks (Dec 1-15)
- **Deliverable:** GPIO expander schematic and PCB layout

#### 2.2.2 GPIO Board Fabrication
PCB fabrication with expedited turnaround to meet January prototype deadline
- **Responsible:** Per Vices (external fab house)
- **Duration:** 1 week
- **Deliverable:** Fabricated GPIO expander PCBs

#### 2.2.3 GPIO Board Assembly & Testing
Populate components, assemble boards, perform electrical validation
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** Tested GPIO expander boards ready for integration

#### 2.2.4 Timing Precision Validation
Measure GPIO output timing precision, jitter, skew to verify ±100 ns requirement
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Timing validation report with oscilloscope measurements

#### 2.2.5 GPIO Integration with Crimson TNG
Install GPIO expander on Crimson TNG, configure FPGA interface, validate operation
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Integrated GPIO expander with functional testing complete

### 2.3 FPGA Firmware Development

#### 2.3.1 FPGA Resource Allocation
Map available Altera Arria V ST resources; allocate logic elements and block RAM for custom development
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** FPGA resource allocation plan

#### 2.3.2 CIC Decimation Filter Design
Design 4-channel CIC decimation filters (320 MSPS → 10 MHz) for dynamic range enhancement
- **Responsible:** Per Vices
- **Duration:** 2 weeks
- **Deliverable:** CIC filter HDL code with simulation results

#### 2.3.3 CIC Filter Implementation
Implement CIC filters in FPGA, integrate with JESD204B receive datapath
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** Compiled FPGA bitstream with CIC decimation

#### 2.3.4 CIC Filter Validation
Validate filter response, decimation ratio, passband/stopband characteristics using test signals
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** CIC filter validation report with frequency response plots

#### 2.3.5 GPIO Timing Logic
Implement FPGA logic for GPIO trigger generation with microsecond-precision timing control
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** GPIO timing control integrated in FPGA firmware

#### 2.3.6 Waveform Streaming Support (Baseline)
Configure DAC datapath for waveform streaming via 10GbE (defer FPGA buffering to Phase 3)
- **Responsible:** Per Vices
- **Duration:** 3 days
- **Deliverable:** Waveform streaming capability validated

### 2.4 Factory Testing & Validation

#### 2.4.1 Transmit Path Testing
Validate all 4 Tx channels: output power, frequency range, attenuation control, pulsed operation
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Tx test report (spectrum analyzer data, power measurements)

#### 2.4.2 Receive Path Testing
Validate all 4 Rx channels: sensitivity, noise figure, frequency range, gain control
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Rx test report (SNR measurements, noise figure data)

#### 2.4.3 Phase Coherency Verification
Measure inter-channel phase stability and deterministic phase relationships across all Tx/Rx channels
- **Responsible:** Per Vices
- **Duration:** 1 day
- **Deliverable:** Phase coherency report with oscilloscope traces

#### 2.4.4 GPIO Functional Testing
Test all GPIO outputs: voltage levels, timing precision, multi-channel synchronization
- **Responsible:** Per Vices
- **Duration:** 1 day
- **Deliverable:** GPIO test report with timing measurements

#### 2.4.5 Data Streaming Performance
Test sustained data rate, packet loss, buffer management at maximum throughput
- **Responsible:** Per Vices
- **Duration:** 1 day
- **Deliverable:** Data streaming performance report

#### 2.4.6 Frequency Range Characterization
Validate operation across full 20-1400 MHz range at multiple test frequencies
- **Responsible:** Per Vices
- **Duration:** 1 day
- **Deliverable:** Frequency range validation report

### 2.5 Software Development (Resynant - Parallel Track)

#### 2.5.1 Development Environment Setup
Install IDE, libraries (NumPy, SciPy, socket), version control; download PVAN-11 data format spec
- **Responsible:** Resynant
- **Duration:** 2 days (Week 1)
- **Deliverable:** Development environment operational

#### 2.5.2 UDP Packet Receiver Implementation
Develop 10GbE UDP socket listener to receive PVAN-11 formatted data packets
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Basic UDP receiver with packet parsing

#### 2.5.3 I/Q Data Processing Pipeline
Convert UDP packets to complex I/Q samples, implement ring buffer for real-time streaming
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Data processing pipeline from packets to FID format

#### 2.5.4 Control API Development
Develop API for Crimson TNG control: frequency tuning, power/attenuation, timing commands
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Control API with command interface

#### 2.5.5 Pulse Sequence Compiler (Initial)
Develop compiler to generate rectangular pulse waveforms with phase/amplitude control
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Basic pulse sequence compiler for simple experiments

#### 2.5.6 Simulator-Based Testing
Create software simulator for end-to-end testing without hardware (simulated UDP packets)
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Simulator test suite with validation cases

### 2.6 Documentation & Delivery Preparation

#### 2.6.1 System Documentation
Create user manual, technical specifications, API documentation for Crimson TNG NMR configuration
- **Responsible:** Per Vices
- **Duration:** 1 week (parallel with testing)
- **Deliverable:** Documentation package (PDF, 50+ pages)

#### 2.6.2 Factory Test Report Compilation
Consolidate all factory test results into comprehensive validation report
- **Responsible:** Per Vices
- **Duration:** 2 days
- **Deliverable:** Factory test report with pass/fail for all subsystems

#### 2.6.3 Shipping Preparation
Package Crimson TNG unit, GPIO expander, accessories; prepare for shipping to Resynant
- **Responsible:** Per Vices
- **Duration:** 1 day
- **Deliverable:** Packaged system ready for shipment

#### 2.6.4 Prototype Delivery
Ship prototype to Resynant facility with tracking, insurance, expedited delivery
- **Responsible:** Per Vices
- **Duration:** 2-3 days transit
- **Deliverable:** Prototype delivered to Resynant (Jan 31, 2026 target)

---

## 3.0 PHASE 2: PROTOTYPE VALIDATION & TESTING

**Duration:** 8 weeks (Feb 1 - Mar 31, 2026)
**Objective:** Resynant validates prototype against acceptance criteria through progressive testing phases

### 3.1 Phase 1: Bench Testing (No Magnet)

**Duration:** 2 weeks (Feb 1-14, 2026)

#### 3.1.1 Physical Installation & Connectivity
Power on, boot Crimson TNG, verify web interface, configure 10GbE network connection to host
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Operational system with network connectivity

#### 3.1.2 Transmit Path Validation
Test all 4 Tx channels: output power (target +10 dBm), frequency range 20-1400 MHz, attenuation 0-60 dB
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Tx test results (spectrum analyzer measurements)

#### 3.1.3 Receive Path Validation
Test all 4 Rx channels: sensitivity, noise figure (target <6 dB), frequency range
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Rx test results (SNR, noise figure measurements)

#### 3.1.4 GPIO Trigger Timing Validation
Measure trigger-to-Tx delay, jitter (target <50 ns), multi-channel skew (target <100 ns) using oscilloscope
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** GPIO timing validation report (pass/fail vs. ±100 ns spec)

#### 3.1.5 Phase Control & Stability
Validate programmable phase shifts (0°, 90°, 180°, 270°) and measure phase stability over 100 acquisitions
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Phase control validation report

#### 3.1.6 Data Acquisition Testing
Validate UDP packet reception, sustained data rate, packet loss (target <0.01%)
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Data acquisition performance report

#### 3.1.7 FPGA Decimation Validation
Verify CIC decimation (320 MSPS → 10 MHz), measure filter response, compare to theoretical
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** CIC decimation validation report

### 3.2 Phase 2: NMR System Integration

**Duration:** 2 weeks (Feb 15-28, 2026)

#### 3.2.1 NMR Probe Tuning
Tune and match 4mm/3.2mm NMR probe to 13C Larmor frequency (e.g., 100.6 MHz at 9.4T)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Tuned NMR probe ready for experiments

#### 3.2.2 First NMR Signal Acquisition (Adamantane)
Acquire first 13C NMR FID from adamantane standard sample, verify signal detection
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** First NMR spectrum with SNR measurement

#### 3.2.3 Pulse Width Calibration
Perform nutation curve to determine 90° and 180° pulse widths for accurate RF calibration
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Calibrated pulse widths for all Tx channels

#### 3.2.4 Frequency Accuracy Validation
Measure adamantane chemical shift (38.5 ppm), verify frequency accuracy <0.2 ppm error
- **Responsible:** Resynant
- **Duration:** 0.5 days
- **Deliverable:** Frequency accuracy report

#### 3.2.5 Spectral Width & Aliasing Testing
Validate spectral width control, proper digital filtering, absence of aliasing artifacts
- **Responsible:** Resynant
- **Duration:** 0.5 days
- **Deliverable:** Spectral width validation report

#### 3.2.6 Phase Stability Testing
Acquire 100 consecutive FIDs, measure first-point phase, calculate standard deviation (target <1°)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Phase stability report (pass/fail vs. <2° spec)

#### 3.2.7 Timing Precision Validation (NMR)
Hahn echo experiment with variable τ, verify echo position accuracy (target ±1% of 2τ)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Timing precision validation with echo data

#### 3.2.8 Dead Time Characterization
Measure minimum dead time between Tx pulse end and Rx acquisition start (target <100 μs)
- **Responsible:** Resynant
- **Duration:** 0.5 days
- **Deliverable:** Dead time measurement report

### 3.3 Phase 3: Multi-Channel Validation

**Duration:** 2 weeks (Mar 1-15, 2026)

#### 3.3.1 Two-Channel Phase Coherency (13C/1H)
Inject simultaneous signals on two channels, measure inter-channel phase, verify standard deviation <2°
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Multi-channel phase coherency report

#### 3.3.2 Broadband Decoupling Setup (Glycine)
Configure 1H decoupling on Tx B while observing 13C on Tx A/Rx A
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Decoupling configuration validated

#### 3.3.3 Decoupling Performance Testing
Compare glycine 13C spectra with/without 1H TPPM decoupling; measure multiplet collapse and SNR gain
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Decoupling performance report (target 2-4× SNR gain)

#### 3.3.4 Decoupling Power Optimization
Vary decoupling power (-5 to -25 dB), identify optimal power for narrowest linewidth
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Optimized decoupling parameters

#### 3.3.5 Long-Duration Decoupling Stability
Apply continuous decoupling for 10 minutes, monitor stability (SNR/linewidth variation <10%)
- **Responsible:** Resynant
- **Duration:** 0.5 days
- **Deliverable:** Long-duration stability report

#### 3.3.6 Cross-Polarization Optimization (Glycine)
Perform CP Hartmann-Hahn matching, vary 13C amplitude to find matching condition
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** CP matching curve with optimal parameters

#### 3.3.7 CP Contact Time Optimization
Vary CP contact time (0.1-10 ms), measure signal intensity, fit to exponential model
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** CP contact time optimization report

#### 3.3.8 CP Reproducibility Testing
Acquire 100 consecutive CP spectra, measure intensity variation (target CV <5%)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** CP reproducibility report (pass/fail vs. <5% CV)

### 3.4 Phase 4: Performance Characterization

**Duration:** 2 weeks (Mar 16-31, 2026)

#### 3.4.1 Dynamic Range Measurement (SNR Method)
Measure SNR on adamantane at 100 kHz, 1 MHz, 5 MHz bandwidths; calculate ENOB
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** ENOB report (target ≥17 bits @ 5 MHz, ≥19 @ 1 MHz)

#### 3.4.2 Large/Small Signal Coexistence
Acquire spectrum with 1:1000 signal ratio, verify detection of weak signals (20-bit requirement: 10^6:1)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Large signal range validation report

#### 3.4.3 Spurious-Free Dynamic Range (SFDR)
Inject strong CW signal, measure spurious content, calculate SFDR (target >80 dBc)
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** SFDR measurement report

#### 3.4.4 Frequency Stability (24-Hour Test)
Continuous acquisition for 24 hours, measure frequency drift (target <1 ppm/24 hr)
- **Responsible:** Resynant
- **Duration:** 1 day setup + 24 hr acquisition
- **Deliverable:** Long-term frequency stability report

#### 3.4.5 Phase Stability (24-Hour Test)
Measure phase drift over 24 hours from continuous acquisition (target <10°/24 hr)
- **Responsible:** Resynant
- **Duration:** 1 day analysis (uses same data as 3.4.4)
- **Deliverable:** Long-term phase stability report

#### 3.4.6 Shaped Pulse Performance
Generate Gaussian selective pulse, validate frequency-selective excitation profile
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Shaped pulse validation report

#### 3.4.7 Two-Dimensional NMR (13C-13C DARR)
Acquire 2D correlation experiment with t1 incrementation, process 2D dataset
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** 2D NMR spectrum demonstrating advanced capability

#### 3.4.8 Complex Multi-Pulse Sequence
Implement advanced pulse sequence (REDOR/TEDOR/RFDR) requiring multi-channel coordination
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Complex sequence validation report

### 3.5 Test Documentation & Acceptance Decision

#### 3.5.1 Test Data Compilation
Consolidate all raw data files, spectra, oscilloscope screenshots, measurement tables
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Organized test data archive

#### 3.5.2 Acceptance Test Report
Generate comprehensive report comparing measured results to acceptance criteria
- **Responsible:** Resynant
- **Duration:** 3 days
- **Deliverable:** Test report with executive summary and pass/fail determination

#### 3.5.3 Performance Summary Analysis
Create specifications table: measured vs. required for all critical parameters
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Performance summary table

#### 3.5.4 Optimization Recommendations
Identify opportunities for FPGA enhancements, software improvements based on test results
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** Recommendations document for Phase 3 optimization

#### 3.5.5 Acceptance Decision & Feedback
Executive decision on prototype acceptance; provide detailed feedback to Per Vices
- **Responsible:** Resynant
- **Duration:** 2 days
- **Deliverable:** Formal acceptance letter OR deficiency list with remediation plan

---

## 4.0 PHASE 3: PRODUCTION READINESS & OPTIMIZATION

**Duration:** 8 weeks (Apr 1 - May 31, 2026)
**Objective:** Optimize FPGA firmware, complete software integration, prepare for production deployment

### 4.1 FPGA Optimization (Conditional on Phase 2 Results)

#### 4.1.1 Waveform Buffer Implementation
Implement FPGA block RAM buffering for decoupling waveforms (128-256 pts per channel)
- **Responsible:** Per Vices
- **Duration:** 2 weeks
- **Deliverable:** FPGA firmware with waveform buffering capability

#### 4.1.2 Hardware Looping Logic
Develop FPGA logic for waveform looping (10s-100s repetitions) without host intervention
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** Hardware looping feature integrated in firmware

#### 4.1.3 CIC Filter Optimization (If Needed)
Tune CIC filter parameters based on Phase 2 dynamic range measurements
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** Optimized CIC filters with improved ENOB

#### 4.1.4 GPIO Timing Refinement (If Needed)
Optimize FPGA GPIO timing logic if Phase 2 revealed jitter or precision issues
- **Responsible:** Per Vices
- **Duration:** 1 week
- **Deliverable:** Enhanced GPIO timing with reduced jitter

#### 4.1.5 FPGA Firmware Validation
Retest optimized FPGA firmware against original acceptance criteria plus enhancements
- **Responsible:** Per Vices + Resynant
- **Duration:** 1 week
- **Deliverable:** Firmware validation report

### 4.2 Software Integration with Harmonyzer

#### 4.2.1 Pulse Sequence Library Expansion
Expand pulse sequence compiler to support CP, decoupling, shaped pulses, 2D experiments
- **Responsible:** Resynant
- **Duration:** 3 weeks
- **Deliverable:** Comprehensive pulse sequence library

#### 4.2.2 Harmonyzer Control System Integration
Integrate Crimson TNG control API with Resynant Harmonyzer spectrometer control software
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Unified control interface

#### 4.2.3 Data Acquisition Pipeline Refinement
Optimize FIR filtering, decimation, data format conversion for production performance
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Production data acquisition software v1.0

#### 4.2.4 User Interface Development
Create GUI for experiment setup, parameter control, real-time data visualization
- **Responsible:** Resynant
- **Duration:** 3 weeks
- **Deliverable:** Harmonyzer-Crimson TNG user interface

#### 4.2.5 Automated Calibration Routines
Develop software for automated pulse width calibration, probe tuning, phase correction
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Automated calibration software module

#### 4.2.6 Error Handling & Diagnostics
Implement error detection, logging, diagnostic tools for troubleshooting
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Diagnostic and error handling framework

### 4.3 Documentation & Training

#### 4.3.1 System Integration Manual
Document Crimson TNG integration with NMR magnet, probe, amplifiers, peripherals
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Integration manual (PDF, 40+ pages)

#### 4.3.2 User Operating Procedures
Create step-by-step procedures for common NMR experiments and routine operations
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Standard Operating Procedures (SOPs)

#### 4.3.3 Maintenance & Troubleshooting Guide
Document maintenance schedules, common issues, troubleshooting flowcharts
- **Responsible:** Resynant + Per Vices
- **Duration:** 1 week
- **Deliverable:** Maintenance and troubleshooting guide

#### 4.3.4 Software User Documentation
Create user manuals for pulse sequence programming, data processing, GUI operation
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Software user documentation package

#### 4.3.5 Training Materials Development
Develop training presentations, tutorial videos, hands-on exercise materials
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Training materials package

#### 4.3.6 Internal Team Training
Train Resynant engineering and support staff on system operation and customer support
- **Responsible:** Resynant
- **Duration:** 1 week (2-day intensive session)
- **Deliverable:** Certified trained staff

### 4.4 Production Process Development

#### 4.4.1 Production Assembly Procedures
Define step-by-step assembly process for integrating Crimson TNG into Harmonyzer system
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Assembly procedure document with photos/diagrams

#### 4.4.2 Quality Control Checkpoints
Establish QC tests at each assembly stage to ensure production quality
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** QC checklist and acceptance criteria

#### 4.4.3 Factory Acceptance Test Procedure
Define reduced acceptance test for production units (vs. full prototype validation)
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Production FAT procedure (2-3 day test suite)

#### 4.4.4 Supply Chain Setup
Establish ordering process, lead times, inventory management for Crimson TNG units
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Supply chain procedures and vendor agreements

#### 4.4.5 Customer Acceptance Test Protocol
Define standard CAT procedures for customer site acceptance of Harmonyzer systems
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Customer acceptance test protocol

### 4.5 Production Release Preparation

#### 4.5.1 Configuration Management
Establish version control for FPGA firmware, software releases, documentation
- **Responsible:** Resynant + Per Vices
- **Duration:** 1 week
- **Deliverable:** Configuration management plan

#### 4.5.2 Production Bill of Materials (BOM)
Finalize complete BOM including Crimson TNG, accessories, custom components
- **Responsible:** Resynant
- **Duration:** 3 days
- **Deliverable:** Production BOM with part numbers and suppliers

#### 4.5.3 Cost Analysis & Pricing
Calculate total production cost, determine Harmonyzer pricing with Crimson TNG
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Production cost model and pricing strategy

#### 4.5.4 Production Readiness Review
Executive review of production readiness across technical, manufacturing, support dimensions
- **Responsible:** Resynant
- **Duration:** 1 day (meeting)
- **Deliverable:** Production release authorization OR deficiency remediation plan

#### 4.5.5 Production Release Approval
Formal approval to proceed with production orders and customer deployments
- **Responsible:** Resynant (Executive Team)
- **Duration:** 1 day
- **Deliverable:** Production release approval document (May 31, 2026 target)

---

## 5.0 PHASE 4: INITIAL PRODUCTION DEPLOYMENT

**Duration:** 12+ weeks (Jun - Aug 2026 and ongoing)
**Objective:** Deploy first 10 production units to customers, establish support infrastructure

### 5.1 Production Order Placement

#### 5.1.1 Initial Production Order (10 Units)
Place purchase order with Per Vices for first 10 production Crimson TNG units
- **Responsible:** Resynant
- **Duration:** 1 day
- **Deliverable:** PO issued for 10-unit production run

#### 5.1.2 Production Schedule Coordination
Coordinate delivery schedule with Per Vices and customer installation timeline
- **Responsible:** Joint
- **Duration:** 1 week
- **Deliverable:** Confirmed production and delivery schedule

#### 5.1.3 Volume Pricing Negotiation
Negotiate pricing for 50-99 unit/year ongoing production based on Phase 1-3 results
- **Responsible:** Resynant + Per Vices
- **Duration:** 2 weeks
- **Deliverable:** Volume pricing agreement for 2027+ production

### 5.2 Production Unit Assembly & Testing

#### 5.2.1 Crimson TNG Production (Per Vices)
Per Vices manufactures 10 production units per agreed specifications
- **Responsible:** Per Vices
- **Duration:** 6-8 weeks (may be phased delivery)
- **Deliverable:** 10 Crimson TNG units delivered to Resynant

#### 5.2.2 Harmonyzer System Integration
Integrate each Crimson TNG unit into complete Harmonyzer spectrometer system
- **Responsible:** Resynant
- **Duration:** 1 week per unit (10 units total, may overlap)
- **Deliverable:** 10 complete Harmonyzer systems assembled

#### 5.2.3 Factory Acceptance Testing (Production)
Execute streamlined FAT procedure on each production unit (2-3 day test per unit)
- **Responsible:** Resynant
- **Duration:** 3 days per unit × 10 units = 30 days (may overlap)
- **Deliverable:** FAT reports for all 10 units

#### 5.2.4 Software Installation & Configuration
Install production software, configure for customer-specific requirements
- **Responsible:** Resynant
- **Duration:** 1 day per unit
- **Deliverable:** Configured systems ready for shipment

### 5.3 Customer Deployment

#### 5.3.1 Customer Site Preparation
Coordinate with customers on site requirements, magnet specifications, power/cooling
- **Responsible:** Resynant
- **Duration:** 2 weeks per customer (may overlap)
- **Deliverable:** Site readiness confirmation for all customers

#### 5.3.2 System Shipping & Installation
Ship systems to customer sites, perform on-site installation and integration
- **Responsible:** Resynant
- **Duration:** 1 week per installation × 10 = 10 weeks (overlapping)
- **Deliverable:** Installed systems at customer sites

#### 5.3.3 Customer Acceptance Testing
Execute customer acceptance test protocol, demonstrate performance to customer satisfaction
- **Responsible:** Resynant
- **Duration:** 2-3 days per customer
- **Deliverable:** CAT completion certificates from all customers

#### 5.3.4 Customer Training
Train customer personnel on system operation, maintenance, basic troubleshooting
- **Responsible:** Resynant
- **Duration:** 2 days per customer
- **Deliverable:** Trained customer staff with training certificates

#### 5.3.5 System Handoff & Warranty Activation
Complete handoff to customer, activate warranty period, establish support contact
- **Responsible:** Resynant
- **Duration:** 1 day per customer
- **Deliverable:** Signed acceptance documents, warranty registration

### 5.4 Support Infrastructure Establishment

#### 5.4.1 Technical Support Hotline Setup
Establish phone/email support with defined response times and escalation procedures
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Technical support hotline operational

#### 5.4.2 Spare Parts Inventory
Stock critical spare components (GPIO boards, cables, software media) for field support
- **Responsible:** Resynant
- **Duration:** 1 week
- **Deliverable:** Spare parts inventory established

#### 5.4.3 Field Service Training
Train field service engineers on troubleshooting and repair procedures
- **Responsible:** Resynant
- **Duration:** 1 week (intensive training)
- **Deliverable:** Certified field service engineers

#### 5.4.4 Remote Diagnostics Capability
Implement remote access tools for software troubleshooting and diagnostics
- **Responsible:** Resynant
- **Duration:** 2 weeks
- **Deliverable:** Remote diagnostics infrastructure

#### 5.4.5 Knowledge Base Development
Create searchable knowledge base of common issues, solutions, FAQs
- **Responsible:** Resynant
- **Duration:** Ongoing (initial 2 weeks)
- **Deliverable:** Knowledge base portal with initial content

### 5.5 Performance Monitoring & Continuous Improvement

#### 5.5.1 Customer Feedback Collection
Establish systematic feedback mechanism from early customers on performance and issues
- **Responsible:** Resynant
- **Duration:** Ongoing
- **Deliverable:** Customer feedback database

#### 5.5.2 Performance Metrics Tracking
Monitor key metrics: uptime, MTBF, support ticket resolution time, customer satisfaction
- **Responsible:** Resynant
- **Duration:** Ongoing
- **Deliverable:** Monthly performance dashboard

#### 5.5.3 Issue Root Cause Analysis
Analyze field issues to identify systematic problems requiring design/software improvements
- **Responsible:** Resynant + Per Vices
- **Duration:** Ongoing
- **Deliverable:** Root cause analysis reports and corrective actions

#### 5.5.4 Software Updates & Patches
Release software updates to address bugs, add features, improve performance
- **Responsible:** Resynant
- **Duration:** Ongoing (quarterly releases)
- **Deliverable:** Software update packages with release notes

#### 5.5.5 Firmware Optimization (Ongoing)
Work with Per Vices on FPGA firmware improvements based on field experience
- **Responsible:** Per Vices + Resynant
- **Duration:** Ongoing
- **Deliverable:** Firmware updates as needed

---

## PROJECT MANAGEMENT & OVERSIGHT (Ongoing)

### PM.1 Project Management Office

#### PM.1.1 Weekly Status Meetings
Conduct weekly Resynant-Per Vices status calls to track progress, risks, issues
- **Responsible:** Joint (Project Managers)
- **Duration:** 30-60 min weekly, Dec 2025 - May 2026
- **Deliverable:** Weekly status reports

#### PM.1.2 Monthly Executive Reviews
Executive-level progress review with Chad Rienstra and Brandon Malatest
- **Responsible:** Joint (Executives)
- **Duration:** 60 min monthly
- **Deliverable:** Executive summary reports

#### PM.1.3 Risk & Issue Management
Maintain risk register, track mitigation actions, escalate critical issues
- **Responsible:** Resynant (Project Manager)
- **Duration:** Ongoing
- **Deliverable:** Updated risk register (weekly)

#### PM.1.4 Schedule Management
Track progress against timeline, identify delays, adjust resource allocation
- **Responsible:** Joint (Project Managers)
- **Duration:** Ongoing
- **Deliverable:** Updated project schedule (weekly)

#### PM.1.5 Budget Tracking
Monitor spending against approved budget, forecast final costs, manage change requests
- **Responsible:** Resynant (Project Manager)
- **Duration:** Ongoing
- **Deliverable:** Monthly budget reports

### PM.2 Quality Assurance

#### PM.2.1 Design Reviews
Conduct formal design reviews at major milestones (GPIO design, FPGA implementation, software releases)
- **Responsible:** Joint
- **Duration:** 2-3 hour sessions at key gates
- **Deliverable:** Design review reports with approval/action items

#### PM.2.2 Test Plan Compliance
Ensure all validation testing follows documented test plan with objective pass/fail criteria
- **Responsible:** Resynant
- **Duration:** Ongoing during Phase 2-4
- **Deliverable:** Test compliance audit reports

#### PM.2.3 Configuration Control
Maintain version control for all hardware designs, FPGA code, software, documentation
- **Responsible:** Joint
- **Duration:** Ongoing
- **Deliverable:** Configuration management database

#### PM.2.4 Non-Conformance Management
Track and resolve any deviations from specifications or test failures
- **Responsible:** Joint
- **Duration:** Ongoing
- **Deliverable:** Non-conformance reports with corrective actions

---

## SUMMARY STATISTICS

**Total Level 1 Phases:** 5 (Phase 0-4) + 1 (Project Management)

**Total Level 2 Deliverable Categories:** 28
- Phase 0: 5 categories
- Phase 1: 6 categories
- Phase 2: 5 categories
- Phase 3: 5 categories
- Phase 4: 5 categories
- Project Management: 2 categories

**Total Level 3 Work Packages:** 102
- Phase 0: 25 work packages
- Phase 1: 26 work packages
- Phase 2: 24 work packages
- Phase 3: 17 work packages
- Phase 4: 15 work packages
- Project Management: 9 work packages

**Critical Path Duration:** 29 weeks (Nov 8, 2025 - Jun 1, 2026)

**Key Milestones:**
- SOW Approval: November 29, 2025 (Week 3)
- Prototype Delivery: January 31, 2026 (Week 12)
- Validation Complete: March 31, 2026 (Week 20)
- Production Release: May 31, 2026 (Week 29)
- First Deployments: June-August 2026 (Week 32-42)

---

**END OF WORK BREAKDOWN STRUCTURE**
