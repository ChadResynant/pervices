# Technical Requirements Specification
## Resynant Harmonyzer NMR Spectrometer SDR System
### Per Vices Crimson TNG Prototype

**Document Version:** 1.0
**Date:** November 8, 2025
**Customer:** Resynant, Inc.
**Application:** High-resolution solid-state NMR spectroscopy

---

## 1. System Overview

### 1.1 Purpose
Development of a software-defined radio (SDR) transmitter and receiver system for high-resolution solid-state Nuclear Magnetic Resonance (NMR) spectroscopy using the Per Vices Crimson TNG platform. The system will replace legacy Varian transmitter/receiver technology with modern SDR capabilities.

### 1.2 Application Context
NMR spectroscopy systems operating at static magnetic fields from approximately 1 Tesla to 35 Tesla, corresponding to NMR detection frequencies from 20 MHz to 1.4 GHz. Primary focus on solid-state NMR with multi-channel phase-coherent operation.

### 1.3 Design Philosophy
- Deterministic phase coherency across all channels (critical requirement)
- High dynamic range to support solvent suppression and weak signal detection
- Flexible waveform generation for modern multi-dimensional NMR experiments
- Precise timing control for sub-microsecond pulse sequence execution

---

## 2. Channel Configuration

### 2.1 Receive Channels
- **Quantity:** 4 independent receive channels (Rx A, B, C, D)
- **Phase Coherency:** Deterministic phase relationships factory-calibrated across all channels
- **Purpose:** Simultaneous multi-channel NMR signal acquisition

### 2.2 Transmit Channels
- **Quantity:** 4 independent transmit channels (Tx A, B, C, D)
- **Phase Coherency:** Deterministic phase relationships factory-calibrated across all channels
- **Purpose:** Multi-channel RF excitation and decoupling

### 2.3 Future Expandability
- **Consideration:** 95% of applications use ≤4 channels
- **Extended Use Cases:** Some applications may require >4 channels
- **Strategy:** Explore multi-unit synchronization for >4 channel requirements
  - Secondary channels may have relaxed timing precision requirements
  - GPIO triggers from primary unit could coordinate secondary units
  - Phase coherency may not be required for ancillary channels

---

## 3. Frequency and Bandwidth Specifications

### 3.1 Frequency Range
- **Specified Range:** 0.2 MHz to 1.4 GHz
- **Practical Range:** 20 MHz to 1.4 GHz
  - Lower limit is flexible; rarely operate below 20 MHz in practice
  - Corresponds to static field range from ~0.5T to 35T

### 3.2 Bandwidth Per Channel
- **Maximum Instantaneous Bandwidth:** 20 MHz per radio chain
- **Typical Operating Bandwidth:** 100 kHz to 10 MHz
- **Final Spectral Width:** Typically 100 kHz for acquisition

### 3.3 Tuning and Frequency Control
- **Requirement:** Independent frequency control per channel
- **Stability:** Determined by OCXO reference (5 ppb specified)
- **Phase Noise:** TBD - to be characterized relative to NMR application requirements

---

## 4. Dynamic Range and Resolution

### 4.1 Effective Number of Bits (ENOB)

**Goal:** 20-bit ENOB at 100 kHz final spectral width

**Context:**
- Many NMR experiments involve solvent signals 10^6 times stronger than solutes
- Solvent suppression techniques exist but are not universally applicable
- 20-bit dynamic range would enable detection across full signal range

**Baseline ADC Performance:**
- Crimson TNG: 16-bit ADC (Texas Instruments ADC16DX370)
- Competitor baseline: 16-bit ADC at 240 MSPS

**Strategy for Enhanced Dynamic Range:**

1. **High Sample Rate Acquisition**
   - Initial sampling at 320-325 MSPS (Crimson TNG maximum)
   - Provides oversampling factor relative to final bandwidth

2. **FPGA-Based Decimation**
   - CIC (Cascaded Integrator-Comb) filter implementation on FPGA
   - Decimation from 320 MSPS to 10 MHz (32-fold reduction)
   - Theoretical gain: ~2.5 bits from 32x oversampling

3. **Host-Side Filtering**
   - Additional FIR filtering on Linux host
   - Further decimation to final spectral width
   - Custom filter design for specific bandwidth requirements

**Target Performance:**
- 5 MHz bandwidth: 17-bit ENOB (minimum acceptable)
- 1 MHz bandwidth: 19-bit ENOB (preferred)
- 100 kHz bandwidth: 20-bit ENOB (goal)
- 6 kHz bandwidth: 23-bit ENOB (stretch goal)

**Open Questions:**
- Confirm CIC filter implementation on Crimson TNG FPGA (Altera Arria V ST)
- Verify available FPGA resources for filtering
- Alternative approaches if 16-bit samples with decimation insufficient
  - 32-bit float processing (requires extensive FPGA work per Per Vices)
  - Evaluate cost/benefit of custom FPGA development

### 4.2 ADC/DAC Specifications

**Receive Path:**
- ADC: Texas Instruments ADC16DX370 (dual-channel)
- Resolution: 16-bit I and 16-bit Q samples
- Sample Rate: Up to 325 MSPS
- JESD204B subclass 1 interface

**Transmit Path:**
- DAC: Texas Instruments DAC38J84 (quad-channel)
- Resolution: 16-bit I and 16-bit Q samples
- Sample Rate: Up to 325 MSPS
- JESD204B subclass 1 interface

---

## 5. Receive Chain Specifications

### 5.1 Noise Figure
- **Requirement:** ≤6 dB system noise figure
- **Rationale:**
  - NMR probe includes integrated low-noise preamplifier (~1 dB NF, 30+ dB gain)
  - Optional second-stage 30 dB preamplifier available if needed
  - 6 dB NF from Crimson TNG contributes negligibly to system noise floor

### 5.2 Input Level and Gain Control
- **Expected Input Levels:** TBD
- **AGC Requirements:** TBD
- **Input Protection:** Per Vices standard configuration

### 5.3 Receive Signal Chain
- RFE → ADC → JESD204B → FPGA → 10GbE → Host
- FPGA processing: CIC decimation, preliminary filtering
- Host processing: Final filtering and signal processing

---

## 6. Transmit Chain Specifications

### 6.1 Output Power
- **Maximum Output Power:** +10 dBm per channel
- **Rationale:** Sufficient for driving external high-power RF amplifiers (typically 50W to 2kW)

### 6.2 Attenuation Control

**Coarse Attenuation (Required):**
- Range: 0 to 60 dB
- Step Size: 10 dB (acceptable)
- Preferred: Smaller steps (3 dB or 1 dB) if achievable without significant NRE
- Control: Programmable via software with microsecond-precision timing

**Fine Amplitude Control (Required):**
- Resolution: 0.1% amplitude precision (competitor specification)
- Method: DAC waveform amplitude scaling
- Range: Within each 10 dB attenuation step

**Phase Control:**
- Resolution: 0.1 degree phase precision (competitor specification)
- Method: DAC waveform phase offset
- Range: 0-360 degrees continuous

### 6.3 Transmit Timing and Gating
- **Switching Speed:** Microsecond-scale attenuation changes
- **Blanking:** Precise transmit on/off control via GPIO triggers
- **Minimum Pulse Width:** TBD (typically 1-10 microseconds)

---

## 7. Timing, Triggering, and Synchronization

### 7.1 GPIO Trigger Requirements

**Quantity:**
- Minimum: 8 GPIO trigger outputs (4 for Rx, 4 for Tx)
- Preferred: 12 GPIO trigger outputs (8 + 4 spare lines)
- Assignment: One trigger per channel, plus spares

**Electrical Specifications:**
- Standard: TTL levels (0-5V)
- Note: Crimson TNG FPGA GPIO is 2.5V logic
- **Requirement:** GPIO expander or level shifter board for TTL compatibility
  - Per Vices has indicated capability to provide GPIO expander
  - Provides protected inputs and greater electrical compatibility

**Timing Precision:**
- **Requirement:** ~100 ns precision for GPIO output triggers
- **Purpose:** Ensure consistency in high-power RF amplifier response
- **Rationale:** High-power amplifier settling times and RF level stability
- **Verification:** Per Vices indicated this is achievable with current hardware

**Trigger Functions:**
- **Rx Triggers:** Gate preamplifier protection, enable signal acquisition
- **Tx Triggers:** Gate RF amplifiers, control transmit blanking
- **Spare Triggers:** Future expansion, auxiliary equipment control

### 7.2 Clock and Synchronization

**Reference Clock:**
- Internal: OCXO (Oven-Controlled Crystal Oscillator), 5 ppb stability
- External: 10 MHz reference input (single-ended, default)
- Requirement: Internal OCXO acceptable for prototype

**Phase Coherency:**
- **Critical Requirement:** Factory-calibrated deterministic phase relationships
- All Rx channels must maintain phase coherency
- All Tx channels must maintain phase coherency
- Tx-to-Rx phase relationship must be deterministic

**Sample Clock:**
- Default: 325 MHz (derived from 5 MHz via LMK04828 clock generator)
- JESD204B subclass 1 architecture ensures synchronized sampling

### 7.3 Timed Commands

**Requirement:** Trigger transmission and reception via timed commands
- Commands sent over 10GbE network interface
- Waveforms pre-loaded, execution triggered at precise time
- Latency and jitter specifications: TBD

---

## 8. Waveform Generation and Management

### 8.1 Waveform Types

**Type 1: Fixed Rectangular Pulses**
- Characteristics: Step function, single amplitude and phase
- Duration: 1-1000 microseconds typical
- Usage: Basic excitation pulses, most common in solid-state NMR

**Type 2: Shaped Pulses**
- Waveform Shapes: Gaussian, sinc, tangent, Hermite, etc.
- Length: Typically ~5,000 complex points for 1 ms waveform
- Time Resolution: 200 ns per point (5 MSPS effective)
- Repetition: Typically not repeated; unique per pulse sequence
- Storage: Can be streamed via 10GbE; may not require FPGA storage

**Type 3: Decoupling Waveforms**
- Length: 128-256 complex points per waveform element
- Duration per element: 10s of microseconds
- Repetition: 10s to 100s of repetitions within single scan (<1 second total)
- Storage: **Should be pre-loaded onto FPGA memory for looping**
- Examples: TPPM, SPINAL, XiX, and other phase-modulated decoupling sequences

### 8.2 Waveform Data Flow

**Initial Implementation (Prototype):**
- All waveforms loaded via 10GbE network interface
- Waveforms buffered on Linux host system
- Timed commands trigger waveform transmission
- **Requirements:**
  - Verify latency and timing jitter
  - Ensure no buffer underruns during acquisition
  - Characterize maximum sustainable data rate

**Future Enhancement:**
- Pre-load decoupling waveforms into FPGA block RAM
- Implement hardware looping for repeated waveforms
- Reduces 10GbE bandwidth requirements
- Requires custom FPGA development

### 8.3 FPGA Resource Allocation

**Per Vices Altera Arria V ST FPGA:**
- Current usage: JESD204B, clock distribution, 10GbE interface
- Available resources for custom development: TBD
- **Requirements to evaluate:**
  - CIC decimation filters (4 Rx channels)
  - Waveform buffer memory (Tx channels)
  - Looping and sequencing logic
  - GPIO timing control

**Open Questions:**
- Available FPGA logic elements and block RAM after standard implementation
- Complexity and NRE cost for custom FPGA development
- Alternative: FPGA IP cores vs. custom HDL development

---

## 9. Data Interfaces and Networking

### 9.1 Host Network Interface

**Required:**
- 10GBASE-R NIC (10 Gigabit Ethernet)
- Dual-port 10G NIC recommended for future multi-unit synchronization
- 1 GbE port for command and control

**Data Format:**
- UDP packets per Per Vices specification
- Link: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/

### 9.2 Data Rates and Throughput

**Prototype Configuration (streaming all data):**
- Receive: 320 MSPS × 16-bit I × 16-bit Q × 4 channels = 40.96 Gbps (theoretical)
- With FPGA CIC decimation to 10 MHz: 10 MSPS × 32-bit I/Q × 4 ch = 1.28 Gbps
- After host-side filtering to 100 kHz: ~1 MB/s sustained data rate

**Typical Acquisition:**
- Spectral width: 100 kHz
- Acquisition time: 100 ms
- Dwell time: 10 microseconds
- Points: 10,000 complex points
- File size: 800 kB per scan (8 bytes per complex point, OpenVX "fid" format)

**Requirements:**
- Verify sustainable data rate with CIC decimation
- Characterize latency from trigger to data availability
- Test with real-time OS requirements (if any)

### 9.3 Host System Requirements

**Operating System:**
- Linux (Per Vices standard)
- Real-Time OS: Evaluate requirement based on latency measurements
  - Phoenix NMR engineers raised questions about RTOS needs
  - To be determined based on prototype testing

**Processing:**
- UDP packet reception and buffering
- Final FIR filtering and decimation
- Data conversion to NMR-standard formats
- Pulse sequence timing and coordination

---

## 10. Control and Configuration Interfaces

### 10.1 Per Vices Standard Interfaces
- Web server interface (ARM Cortex-A9 hosted)
- UART serial port for module communication
- Command API over 1 GbE management interface

### 10.2 NMR Spectrometer Integration
- Integration with Resynant Harmonyzer control system
- Pulse sequence programming interface
- Real-time parameter updates (frequency, phase, amplitude)

---

## 11. Power and Environmental

### 11.1 Power Supply
- Input: 120-240 VAC, IEC320 C13 connector
- Internal: 12V, 200W DC power supply
- Overcurrent protection: Included

### 11.2 Environmental Considerations
- **Operating Environment:** NMR laboratory
- **EMI/RFI:** Must coexist with high-field magnets and RF amplifiers
- **Cooling:** Per Vices standard (verify for laboratory environment)

---

## 12. Open Questions and Items for Discussion

### 12.1 Dynamic Range Implementation
1. Confirm available FPGA resources for CIC filter implementation
2. Evaluate 32-bit float processing if 16-bit with decimation insufficient
3. Characterize actual ENOB vs. bandwidth with prototype
4. Define validation methodology using NMR test samples

### 12.2 GPIO and Trigger Interface
1. Confirm GPIO expander board specifications and availability
2. Verify 100 ns timing precision with GPIO expander
3. Define electrical interface (connector type, pinout)
4. Characterize jitter and latency

### 12.3 FPGA Development
1. Assess FPGA resource availability for custom development
2. Estimate NRE costs for:
   - CIC decimation implementation
   - Waveform buffer and looping logic
   - Enhanced GPIO control
3. Timeline for FPGA development and validation

### 12.4 Multi-Unit Synchronization
1. Architecture for >4 channel systems (future)
2. Clock distribution and phase synchronization between units
3. Network infrastructure for multiple Crimson TNG units

### 12.5 Validation and Testing
1. Define acceptance criteria for prototype
2. NMR test samples for dynamic range validation
3. Phase coherency measurement methodology
4. Timing and trigger validation procedures

---

## 13. Project Scope and Timeline

### 13.1 Initial Order
- Quantity: 1 prototype unit
- Purpose: Validation and integration development

### 13.2 Production Forecast
- Near-term: 10 units within 12 months of prototype validation
- Production: 50-99 units per year once in full production (2026-2027)
- Volume pricing: To be negotiated

### 13.3 Current State
- Using refurbished legacy Varian transmitters/receivers
- Orders in hand: 2 customers × 2 units
- Additional orders pending
- Large order from Indiana University provides R&D investment opportunity

---

## 14. Success Criteria

### 14.1 Prototype Acceptance Criteria
1. **Phase Coherency:** Deterministic phase relationships verified across all channels
2. **Dynamic Range:** ENOB ≥17 bits at 5 MHz bandwidth (minimum); ≥19 bits at 1 MHz (goal)
3. **Timing Precision:** GPIO triggers within 100 ns specification
4. **Frequency Coverage:** Validated operation from 20 MHz to 1.4 GHz
5. **Data Throughput:** Sustainable acquisition at required data rates without dropouts
6. **NMR Integration:** Successful acquisition of NMR signals with real samples

### 14.2 Performance Benchmarks
- Meet or exceed legacy Varian DDR specifications
- Competitive with current commercial NMR receiver solutions
- Distinguish Resynant Harmonyzer product in marketplace

---

## 15. References and Supporting Documents

### 15.1 Per Vices Documentation
- Crimson TNG System Architecture: https://support.pervices.com/crimson/sys/
- Data Format Specification: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
- Per Vices case studies (GPS/GNSS, Napatech, Radar, Spectrum)

### 15.2 Email Correspondence
- Initial inquiry: September 26, 2025
- Technical requirements discussion: September 27-29, 2025
- Dynamic range and trigger discussion: October 1-7, 2025
- Follow-up: October 17 - November 8, 2025

### 15.3 Related Documentation
- System block diagram (Screenshot 2025-11-08 at 10.01.06 AM.png)
- Use case scenarios (to be developed)
- NMR pulse sequence specifications (to be developed)

---

**Document Status:** Draft for internal review
**Next Steps:** Review, refine, and submit to Per Vices for SOW development

**Contact Information:**
Chad M. Rienstra, Ph.D.
President & CEO
Resynant, Inc.
chad@resynant.com
(217) 649-8932
