# OpenVNMRJ - Crimson TNG Integration Architecture
## Integration Strategy for Resynant NMR Spectrometer

**Document Version:** 1.0
**Date:** November 21, 2025
**Purpose:** Define clean architecture for integrating Per Vices Crimson TNG with ResynantOVJ

---

## 1. Current State Analysis

### 1.1 ResynantOVJ Architecture (Based on Repository Exploration)

```
User Interface (ResynantOVJ GUI Enhancements)
           ↓
    OpenVNMRJ Core
           ↓
  Pulse Sequence (.c files in psglib/)
           ↓
    PSG Compiler (nvpsg/)
           ↓
  Hardware Interface Layer (nvsendproc/ + nvrecvproc/)
           ↓
     Hardware (Currently: Varian/Agilent consoles)
```

**Key Findings from Repository:**
- **ResynantOVJ enhancements:** GUI/workflow layer (Java) in `src/vnmrj/src/vnmr/resynant/`
- **Pulse sequences:** C code in `src/psglib/`, `src/biopack/psglib/`
- **PSG compiler:** `src/nvpsg/` - compiles pulse sequences to hardware commands
- **Hardware interface:**
  - `src/nvsendproc/` - Transmit path (RF, gradients, GPIO)
  - `src/nvrecvproc/` - Receive path (data acquisition, FID upload)

### 1.2 Target Architecture (Per Vices Crimson TNG)

```
User Interface (ResynantOVJ GUI)
           ↓
    OpenVNMRJ Core
           ↓
  Pulse Sequence (.c files)
           ↓
    PSG Compiler (nvpsg/)
           ↓
  [NEW] Crimson Bridge Layer (Python/C++)
           ↓
  [NEW] Crimson TNG API + Our UDP Receiver
           ↓
     Crimson TNG SDR Hardware
```

---

## 2. Integration Approach: "Bridge Layer" Strategy

### 2.1 Design Philosophy (Avoiding Tabor Mistakes)

**CRITICAL LESSONS FROM TABOR FAILURE (See CLAUDE.md):**
- ❌ **DON'T:** Create complex translation layers (UCODE → TEproc → SCPI was fatal)
- ❌ **DON'T:** Repurpose Vendor hardware not designed for NMR
- ❌ **DON'T:** Have "unknown unknowns" about critical hardware features
- ✅ **DO:** Keep software architecture simple (maximum 2 layers)
- ✅ **DO:** Use purpose-built SDR (Crimson TNG designed for phase-coherent apps)
- ✅ **DO:** Define clear, documented interfaces

### 2.2 Recommended Architecture

**Two-Layer Approach:**

```
Layer 1: PSG Compiler (nvpsg/) - UNCHANGED
         ↓ (generates intermediate commands)
Layer 2: Crimson Bridge (NEW) - Directly translates to Crimson TNG API
         ↓ (no intermediate formats!)
  Crimson TNG Hardware
```

**Why This Works:**
1. **Preserve existing PSG compiler** - 30+ years of pulse sequence development
2. **Single translation layer** - Bridge directly converts PSG output → Crimson commands
3. **No UCODE/Acode dependency** - Bypass Varian legacy formats entirely
4. **Crimson TNG purpose-built** - Designed for multi-channel phase-coherent apps

---

## 3. Bridge Layer Implementation

### 3.1 Where to Insert the Bridge

**Option A: Replace nvsendproc/nvrecvproc entirely (RECOMMENDED)**

```
PSG Compiler (nvpsg/)
      ↓
   PSG Output (internal data structures in C)
      ↓
[NEW] crimson_bridge.py (Python interface)
      ↓
   Crimson TNG API calls
```

**Benefits:**
- Clean separation from Varian hardware code
- Can reuse our Python UDP receiver (already built!)
- Easier debugging and testing
- Leverage Python for rapid development

**Option B: Modify nvsendproc/nvrecvproc**

```
PSG Compiler (nvpsg/)
      ↓
nvsendproc (MODIFIED to call Crimson instead of Varian)
      ↓
   Crimson TNG API
```

**Benefits:**
- Maintains existing C codebase structure
- Less architectural change
- May be required if PSG outputs binary format

---

### 3.2 Bridge Layer Components

**File Structure:**
```
/home/user/pervices/software/
├── src/
│   ├── udp_receiver.py          [✅ Already built - PVAN-11 parser]
│   ├── ring_buffer.py            [✅ Already built - Multi-channel buffer]
│   ├── data_acquisition.py       [✅ Already built - Real-time streaming]
│   ├── signal_processing.py      [✅ Already built - FIR, FFT, SNR]
│   ├── crimson_bridge.py         [NEW - PSG → Crimson translator]
│   ├── crimson_api.py            [NEW - Crimson TNG API wrapper]
│   └── pulse_sequence_executor.py [NEW - Execute compiled sequences]
└── ovj_interface/
    ├── psg_output_parser.py      [NEW - Parse PSG compiler output]
    └── ovj_crimson_adapter.c     [NEW - C shim if needed for nvsendproc]
```

**Bridge Functions:**

1. **crimson_bridge.py:**
   - Parse PSG compiler output (commands, timing, phases)
   - Translate to Crimson TNG API calls
   - Handle 2D/3D acquisition loops (t1/t2/t3 increments)
   - Phase cycling management

2. **crimson_api.py:**
   - Wrapper for Crimson TNG API
   - Set frequency, power, phase for each channel
   - GPIO trigger control (Tx/Rx gates, blanking)
   - Upload waveform buffers to FPGA
   - Start/stop acquisition

3. **pulse_sequence_executor.py:**
   - Execute compiled pulse sequences in real-time
   - Coordinate Tx waveforms, Rx windows, GPIO timing
   - Feed data to ring buffer via UDP receiver
   - Handle experiment arraying (ni, phase cycling)

---

## 4. Data Flow: Pulse Sequence → NMR Spectrum

### 4.1 Transmit Path (PSG → Crimson TNG)

```
1. User writes pulse sequence:
   hetcor.c (in OVJ psglib/)
   ↓
2. PSG Compiler compiles:
   nvpsg compiles hetcor.c → PSG output (C data structures)
   ↓
3. Bridge parses PSG output:
   crimson_bridge.py reads PSG commands
   ↓
4. Generate waveforms:
   - Rectangular pulses: I/Q arrays for specified duration/phase
   - CP ramps: Linear amplitude ramps for contact pulse
   - TPPM decoupling: Phase-modulated pulse train
   ↓
5. Upload to Crimson TNG:
   crimson_api.set_frequency(channel='H1', freq=400e6)
   crimson_api.upload_waveform(channel='H1', i_samples, q_samples)
   crimson_api.set_gpio_trigger(channel='H1_TX_GATE', timing)
   ↓
6. Trigger execution:
   crimson_api.start_sequence()
   [Crimson TNG FPGA plays out waveforms, triggers GPIO]
```

### 4.2 Receive Path (Crimson TNG → NMR Spectrum)

```
1. Crimson TNG ADC samples:
   4 Rx channels @ 325 MSPS
   ↓
2. FPGA CIC decimation (if available):
   325 MSPS → 10 MHz (65x decimation)
   ↓
3. FPGA packetizes:
   I/Q data → PVAN-11 UDP packets
   ↓
4. Our UDP receiver captures:
   udp_receiver.py receives packets over 10 GbE
   ring_buffer.py stores multi-channel data
   ↓
5. Signal processing:
   signal_processing.py: FIR filtering, FFT
   ↓
6. Export to OVJ format:
   Save as FID files compatible with vnmrj processing
   ↓
7. User processes in OVJ GUI:
   FFT, phase correction, peak picking in ResynantOVJ GUI
```

---

## 5. Implementation Plan

### Phase 1: Minimal Bridge (Feb 2026 - Prototype)

**Goal:** Single-pulse acquisition working end-to-end

**Components:**
1. Parse PSG output for simple pulse sequence (s2pul)
2. Generate rectangular pulse waveforms (I/Q samples)
3. Upload to Crimson TNG, trigger acquisition
4. Receive UDP data, save as FID file
5. Load FID into OVJ for processing

**Deliverables:**
- Single-channel Tx/Rx working
- Basic GPIO control (Tx gate, Rx gate)
- FID file format compatible with OVJ
- Integration test with adamantane (13C single-pulse)

### Phase 2: Multi-Channel CP (Mar-Apr 2026)

**Goal:** Cross-polarization experiments (hCH HETCOR)

**New Features:**
1. Multi-channel waveform generation (1H + 13C simultaneous)
2. CP ramp generation (linear amplitude ramps)
3. TPPM decoupling (phase-modulated pulse train)
4. Phase cycling (4-step, 16-step)

**Deliverables:**
- 1H→13C CP working
- TPPM decoupling implemented
- hCH HETCOR 2D acquisition (basic)

### Phase 3: 2D/3D Framework (May 2026 - Indiana Beta)

**Goal:** Full hX/hXX 2D experiments

**New Features:**
1. 2D acquisition loops (t1/t2 increments, States-TPPI)
2. DARR mixing (CW irradiation during mixing period)
3. RFDR (rotor-synchronized π-pulse train, if time permits)
4. 3D acquisition (NCACX, if time permits)

**Deliverables:**
- hCH HETCOR (1H-13C)
- hNH HETCOR (1H-15N)
- DARR (13C-13C homonuclear)
- System stable for 8-hour acquisitions

---

## 6. Bridge Subroutines (Answering Your Question)

### 6.1 What Are "Bridge Subroutines"?

Based on your query and the codebase, these are the **adapter functions** that translate OVJ PSG commands to Crimson TNG API calls.

**Key Bridge Functions:**

```python
# crimson_bridge.py

class CrimsonBridge:
    """
    Bridge between OpenVNMRJ PSG output and Crimson TNG hardware.
    """

    def __init__(self, crimson_api):
        self.crimson = crimson_api
        self.current_phase = {'H1': 0, 'C13': 0, 'N15': 0}
        self.waveform_buffers = {}

    def translate_pulse(self, channel, duration, phase, power):
        """
        PSG pulse() command → Crimson TNG waveform.

        Args:
            channel: 'H1', 'C13', 'N15', etc.
            duration: Pulse width in seconds
            phase: Phase in degrees (0, 90, 180, 270)
            power: RF power in dBm or relative (0-1)
        """
        # Generate rectangular pulse I/Q waveform
        sample_rate = 325e6  # Crimson TNG sample rate
        n_samples = int(duration * sample_rate)

        # Rectangular pulse with phase
        amplitude = self.power_to_amplitude(power)
        phase_rad = np.deg2rad(phase)

        i_samples = amplitude * np.cos(phase_rad) * np.ones(n_samples)
        q_samples = amplitude * np.sin(phase_rad) * np.ones(n_samples)

        # Upload to Crimson TNG
        self.crimson.upload_waveform(channel, i_samples, q_samples)

        return n_samples

    def translate_cp_ramp(self, channel, duration, start_power, end_power):
        """
        PSG shapedpulse() for CP ramp → Crimson TNG amplitude ramp.
        """
        sample_rate = 325e6
        n_samples = int(duration * sample_rate)

        # Linear ramp from start_power to end_power
        amplitude_ramp = np.linspace(
            self.power_to_amplitude(start_power),
            self.power_to_amplitude(end_power),
            n_samples
        )

        # Constant phase (typically 0° for CP)
        i_samples = amplitude_ramp
        q_samples = np.zeros(n_samples)

        self.crimson.upload_waveform(channel, i_samples, q_samples)

        return n_samples

    def translate_acquire(self, duration, num_points):
        """
        PSG acquire() command → Crimson TNG data acquisition.

        Args:
            duration: Acquisition time in seconds
            num_points: Number of complex points to acquire
        """
        # Set up acquisition
        self.crimson.set_acquisition_params(
            duration=duration,
            num_points=num_points
        )

        # Trigger acquisition via GPIO
        self.crimson.trigger_acquisition()

        # Data will stream via UDP to our receiver

    def translate_delay(self, duration):
        """
        PSG delay() command → Crimson TNG timing.
        """
        # Insert delay in sequence timing
        self.crimson.add_delay(duration)

    def set_frequency(self, channel, frequency):
        """
        Set RF carrier frequency for channel.
        """
        self.crimson.set_frequency(channel, frequency)

    def set_phase(self, channel, phase):
        """
        Set transmitter phase.
        """
        self.current_phase[channel] = phase
        # Will be applied when next waveform is generated
```

---

## 7. Critical Integration Points

### 7.1 Where PSG Output Is Generated

**Need to examine:**
- `/home/user/ResynantOVJ/src/nvpsg/` - PSG compiler source
- Look for output format: binary file, data structures, or function calls
- Identify what nvsendproc expects as input

### 7.2 Where Hardware Commands Are Sent

**Current Varian path:**
- `nvsendproc/sendproc.c` - Main hardware interface
- `nvsendproc/sendfuncs.c` - Send functions

**Replace with:**
- `crimson_bridge.py` intercepts at same point
- Calls Crimson TNG API instead of Varian hardware

### 7.3 Data Format Compatibility

**FID File Format:**
- OVJ expects binary FID files with specific header format
- Our UDP receiver must save data in compatible format
- May need to write FID header translator

---

## 8. Next Steps (Immediate)

### 8.1 Code Exploration Tasks

1. **Find PSG output format:**
   ```bash
   cd /home/user/ResynantOVJ/src/nvpsg
   grep -r "send\|output\|write" *.c | less
   ```

2. **Examine nvsendproc input:**
   ```bash
   cd /home/user/ResynantOVJ/src/nvsendproc
   head -200 sendproc.c > /tmp/sendproc_analysis.txt
   ```

3. **Identify pulse sequence examples:**
   ```bash
   find /home/user/ResynantOVJ -name "*hetcor*.c" -o -name "*darr*.c"
   ```

### 8.2 Design Decisions Needed

**Questions for Chad:**
1. Do you want to **replace nvsendproc entirely** or **modify it** to call Crimson?
2. Is there a PSG output file we can intercept, or do we need C integration?
3. Do you have specific pulse sequences (hetcor.c, darr.c) we should prioritize?
4. Should the bridge be **Python** (faster development) or **C++** (performance)?

### 8.3 Prototype Development

**Week 1 (Dec 2-6):**
- Complete PSG output format analysis
- Design crimson_bridge.py API
- Write crimson_api.py wrapper for Crimson TNG

**Week 2 (Dec 9-13):**
- Implement bridge for simple pulse (s2pul)
- Test with simulated PSG output
- Integrate with our UDP receiver

**Week 3 (Dec 16-20):**
- Add multi-channel support (CP experiments)
- Implement CP ramp generation
- Test with hetcor pulse sequence

---

## 9. Risk Assessment

### 9.1 Known Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PSG output format undocumented | Medium | High | Examine source code, ask OVJ community |
| Binary compatibility issues | Low | Medium | Write robust parser with error handling |
| Timing precision requirements | Low | High | Validate GPIO timing early (±100 ns spec) |
| FID file format incompatibility | Medium | Medium | Reference OVJ source for exact format |

### 9.2 Success Criteria

**Prototype Acceptance (Feb 2026):**
- ✅ Single-pulse (s2pul) runs end-to-end
- ✅ FID loads into OVJ GUI and processes correctly
- ✅ SNR >50:1 on adamantane (matches legacy Varian)

**Indiana Beta Acceptance (May 2026):**
- ✅ hCH HETCOR 2D acquisition complete
- ✅ DARR homonuclear correlation working
- ✅ System stable for 8-hour experiments
- ✅ User finds interface intuitive (ResynantOVJ GUI)

---

## 10. References

**Key Source Files (To Examine):**
- `/home/user/ResynantOVJ/src/nvpsg/cps.c` - PSG core functions
- `/home/user/ResynantOVJ/src/nvsendproc/sendproc.c` - Hardware interface
- `/home/user/ResynantOVJ/src/nvrecvproc/Data_Upload.c` - Data reception
- `/home/user/ResynantOVJ/src/psglib/s2pul.c` - Simple pulse sequence example

**Documentation:**
- PVAN-11 specification: `/home/user/pervices/pvan11_dataformat_spec.md`
- hX/hXX 2D specs: `/home/user/pervices/HX_HXX_2D_SPECIFICATIONS.md`
- Crimson TNG requirements: `/home/user/pervices/technical_requirements.md`

**Our Existing Code:**
- UDP receiver: `/home/user/pervices/software/src/udp_receiver.py`
- Signal processing: `/home/user/pervices/software/src/signal_processing.py`
- Data acquisition: `/home/user/pervices/software/src/data_acquisition.py`

---

**Document Status:** Draft v1.0 - Ready for Chad's review and feedback

**Next Action:** Await Chad's answers to Design Decisions (Section 8.2), then begin prototype development.
