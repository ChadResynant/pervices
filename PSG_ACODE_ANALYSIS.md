# PSG Acode Analysis and Bridge Implementation Plan
## Understanding OpenVNMRJ PSG Output for Crimson TNG Integration

**Document Version:** 1.0
**Date:** November 21, 2025
**Based On:** ResynantOVJ source code analysis + hX pulse sequence examination

---

## 1. PSG Compilation Flow

### 1.1 From Pulse Sequence to Hardware

```
User Pulse Sequence (hX.c)
         ↓
   pulsesequence() function executes
         ↓
   PSG library functions called:
   - rgpulse(), decrgpulse()
   - delay()
   - _cp_() (cross-polarization)
   - _dseqon(), _dseqoff() (decoupling)
   - startacq(), acquire(), endacq()
   - txphase(), decphase()
   - obspwrf(), decpwrf()
         ↓
   Each function generates Acodes (integer opcodes)
         ↓
   Acodes written to binary buffer/file
         ↓
[INTEGRATION POINT] → Crimson Bridge intercepts here
         ↓
   Translated to Crimson TNG commands
         ↓
   Executed on Crimson TNG hardware
```

---

## 2. Acode Format (from nvpsg/acodes.h)

### 2.1 Acode Opcodes

Acodes are **integer opcodes** that represent hardware operations:

| Acode | Value | Description | Bridge Translation |
|-------|-------|-------------|-------------------|
| **EVENT1** | 46 | Output event (pulse) with timing + gate pattern | → Crimson waveform upload + GPIO trigger |
| **EVENT2** | 47 | Two-word timing event (higher precision) | → High-precision Crimson timing |
| **INITFREQ** | 57 | Initialize RF frequency | → `crimson_api.set_frequency()` |
| **INCRFREQ** | 58 | Increment RF frequency | → Frequency sweep support |
| **acqstart** | 44 | Start acquisition | → `crimson_api.start_acquisition()` |
| **acqend** | 45 | End acquisition | → `crimson_api.stop_acquisition()` |
| **HALT** | 4 | Halt sequence | → Sequence termination |
| **BRANCH** | 20 | Branch (loops) | → Loop control for 2D/3D |

**Event Structure (EVENT1):**
```
EVENT1 acode
timing_word (delay duration in hardware ticks)
gate_pattern (which channels/gates active)
```

### 2.2 Example: rgpulse() Translation

**PSG Call (in hX.c):**
```c
decrgpulse(getval("pwH90"), phH90, 0.0, 0.0);
```

**Generates Acodes:**
```
INITFREQ  [decoupler_frequency]
EVENT1    [pulse_duration] [dec_gate_on | rf_on]
EVENT1    [0] [gates_off]
```

**Bridge Translates To:**
```python
crimson_api.set_frequency(channel='H1', freq=400e6)
crimson_api.upload_waveform(channel='H1',
                            i_samples=rectangular_pulse(duration, phase),
                            q_samples=...)
crimson_api.trigger_gpio('H1_TX_GATE', timing)
```

---

## 3. hX Pulse Sequence Analysis

### 3.1 Key PSG Functions Used in hX

**From `/home/user/vnmrj-nmr-tools/vnmrsys/psglib/hX.c`:**

| PSG Function | Purpose | Acode Generated | Crimson Translation |
|--------------|---------|-----------------|-------------------|
| `decrgpulse(pw, ph, r1, r2)` | Decoupler rectangular pulse | EVENT1 + gates | Rectangular waveform on H1 channel |
| `rgpulse(pw, ph, r1, r2)` | Observe pulse | EVENT1 + gates | Rectangular waveform on obs channel |
| `_cp_(hx, phH, phX)` | Cross-polarization | Multiple EVENT1s (ramped) | Linear amplitude ramp waveforms |
| `delay(time)` | Wait | EVENT1 with zero gates | Timing delay in sequence |
| `_dseqon(dec)` | Decoupling on | Continuous EVENT1s (TPPM) | Phase-modulated pulse train |
| `_dseqoff(dec)` | Decoupling off | Stop continuous events | Stop decoupling waveform |
| `startacq(ad)` | Start acquisition | acqstart Acode | Trigger Crimson Rx, start UDP stream |
| `acquire(np, dwell)` | Acquire data | Acquisition loop | Receive PVAN-11 packets |
| `endacq()` | End acquisition | acqend Acode | Stop Rx, close UDP stream |
| `txphase(phase)` | Set transmitter phase | Phase register update | Phase rotation in I/Q waveform |
| `obspwrf(power)` | Set observe power | Amplitude register | Amplitude scaling in waveform |

### 3.2 hX Sequence Structure

**Simplified pseudocode translation:**

```python
# d1 delay (relaxation)
crimson.delay(d1)

# H 90° pulse
crimson.set_phase(channel='H1', phase=phH90)
crimson.rectangular_pulse(channel='H1', duration=pwH90, power=aH90)

# CP (H→X cross-polarization)
crimson.cp_ramp(
    h_channel='H1',
    x_channel='C13',
    duration=tHX,
    h_ramp=(aHhx_start, aHhx_end),
    x_power=aXhx
)

# Decoupling on X
crimson.start_decoupling(channel='H1', seq_type='TPPM', power=aHtppm)

# Optional X flip-back
if flip == 'y':
    crimson.rectangular_pulse(channel='C13', duration=pwX90, phase=phX90flip)

# Optional shaped refocusing pulse
if echo == 'soft':
    crimson.delay(tECHO/2)
    crimson.shaped_pulse(channel='C13', shape='shp1X', phase=phXshp1)
    crimson.delay(tECHO/2)

# Acquisition
crimson.start_acquisition(np, sw)
crimson.acquire(duration=at)
crimson.end_acquisition()

# Stop decoupling
crimson.stop_decoupling(channel='H1')
```

---

## 4. Bridge Architecture Design

### 4.1 Option A: Intercept Acode Binary File (RECOMMENDED)

**Approach:**
1. PSG compiles hX.c → generates Acode file (e.g., `/tmp/acodes`)
2. nvsendproc normally reads this file → sends to Varian hardware
3. **Crimson Bridge** reads same file → translates to Crimson commands

**Benefits:**
- No modifications to PSG compiler
- Clean separation from OVJ codebase
- Can test with pre-compiled Acode files

**Implementation:**
```python
# crimson_bridge.py

class AcodeParser:
    def __init__(self, acode_file_path):
        self.acode_data = self.read_acode_file(acode_file_path)
        self.pc = 0  # Program counter

    def read_acode_file(self, path):
        """Read binary Acode file."""
        with open(path, 'rb') as f:
            return f.read()

    def parse_next_acode(self):
        """Parse next Acode from buffer."""
        if self.pc >= len(self.acode_data):
            return None

        # Read opcode (4 bytes, big-endian int)
        opcode = int.from_bytes(
            self.acode_data[self.pc:self.pc+4],
            byteorder='big'
        )
        self.pc += 4

        # Parse opcode-specific parameters
        if opcode == EVENT1:
            timing = int.from_bytes(self.acode_data[self.pc:self.pc+4], 'big')
            self.pc += 4
            gates = int.from_bytes(self.acode_data[self.pc:self.pc+4], 'big')
            self.pc += 4
            return {'op': 'EVENT1', 'timing': timing, 'gates': gates}

        elif opcode == INITFREQ:
            channel = int.from_bytes(self.acode_data[self.pc:self.pc+4], 'big')
            self.pc += 4
            freq = int.from_bytes(self.acode_data[self.pc:self.pc+8], 'big')
            self.pc += 8
            return {'op': 'INITFREQ', 'channel': channel, 'freq': freq}

        elif opcode == acqstart:
            return {'op': 'acqstart'}

        # ... parse other opcodes

        return {'op': 'UNKNOWN', 'code': opcode}
```

### 4.2 Option B: Hook PSG Library Functions

**Approach:**
1. Recompile PSG with modified library functions
2. rgpulse(), delay(), etc. call Crimson functions directly
3. Bypass Acode generation entirely

**Benefits:**
- Most direct translation
- Real-time execution possible

**Drawbacks:**
- Requires modifying PSG source
- Tightly coupled to OVJ codebase
- Harder to debug

**NOT RECOMMENDED** due to complexity.

---

## 5. Crimson Bridge Implementation Plan

### 5.1 Component Architecture

```
/home/user/pervices/software/
├── ovj_bridge/
│   ├── acode_parser.py         # Parse Acode binary files
│   ├── crimson_bridge.py       # Main bridge logic
│   ├── crimson_api.py          # Crimson TNG API wrapper
│   ├── pulse_generator.py      # Generate I/Q waveforms
│   └── sequence_executor.py    # Execute sequences in real-time
└── src/
    ├── udp_receiver.py          [✅ Already built]
    ├── ring_buffer.py           [✅ Already built]
    ├── data_acquisition.py      [✅ Already built]
    └── signal_processing.py     [✅ Already built]
```

### 5.2 Bridge Workflow

```
1. User runs pulse sequence in OVJ:
   go('hX')  [in vnmrj command line]
   ↓
2. PSG compiles hX.c → generates /tmp/acodes
   ↓
3. Instead of running nvsendproc (Varian):
   Run: crimson_bridge.py /tmp/acodes
   ↓
4. AcodeParser reads binary file:
   opcodes, timing, gates, frequencies
   ↓
5. CrimsonBridge translates Acodes:
   EVENT1 → waveform generation
   INITFREQ → set_frequency()
   acqstart → start_acquisition()
   ↓
6. PulseGenerator creates I/Q waveforms:
   Rectangular pulses, CP ramps, TPPM
   ↓
7. SequenceExecutor uploads to Crimson TNG:
   Upload waveforms to FPGA buffers
   Set GPIO triggers
   Start sequence
   ↓
8. Data acquisition (existing code):
   UDP receiver captures PVAN-11 packets
   Ring buffer stores data
   Save as FID file
   ↓
9. OVJ processes FID:
   Load FID, FFT, phase correction, display
```

---

## 6. Implementation Phases

### Phase 1: Acode Parser (Week 1 - Dec 2-6)

**Tasks:**
1. Locate Acode file output location
2. Parse binary format (opcode + parameters)
3. Create Acode→JSON converter for debugging
4. Test with simple sequence (s2pul)

**Deliverable:** `acode_parser.py` that reads and prints Acodes

### Phase 2: Waveform Generation (Week 2 - Dec 9-13)

**Tasks:**
1. Implement rectangular_pulse() generator
2. Implement cp_ramp() generator (linear)
3. Implement tppm_sequence() generator
4. Test waveform quality (plot I/Q)

**Deliverable:** `pulse_generator.py` with waveform functions

### Phase 3: Crimson API Wrapper (Week 3 - Dec 16-20)

**Tasks:**
1. Research Crimson TNG API (ask Per Vices for docs)
2. Implement set_frequency(), set_power(), set_phase()
3. Implement upload_waveform()
4. Implement GPIO trigger control
5. Implement start/stop acquisition

**Deliverable:** `crimson_api.py` working with Crimson TNG

### Phase 4: Bridge Integration (Week 4 - Jan 6-10)

**Tasks:**
1. Connect AcodeParser → PulseGenerator → CrimsonAPI
2. Execute simple sequence (s2pul) end-to-end
3. Capture FID via UDP receiver
4. Save in OVJ-compatible format
5. Load and process in vnmrj GUI

**Deliverable:** Single-pulse working Resynant→OVJ→Crimson→OVJ

### Phase 5: Multi-Channel CP (Weeks 5-6 - Jan 13-24)

**Tasks:**
1. Parse CP Acodes (_cp_ function)
2. Generate dual-channel CP ramps
3. Implement TPPM decoupling
4. Test hX sequence end-to-end

**Deliverable:** hX (1H-13C HETCOR) working

---

## 7. Critical Questions to Answer

### 7.1 Acode File Location

**Question:** Where does PSG write the compiled Acode file?

**Investigation:**
```bash
cd /home/user/ResynantOVJ
grep -r "acode.*fopen\|acode.*write" src/nvpsg/*.c
```

**Expected:** Something like `/vnmr/acqqueue/acodes` or `/tmp/acodes`

### 7.2 Acode Binary Format

**Question:** What is the exact binary layout?

**Investigation:**
1. Compile simple sequence (s2pul)
2. Hexdump the Acode file
3. Correlate with opcodes in acodes.h

**Expected Format:**
```
[Header: magic number, version, size]
[Opcode 1: 4 bytes]
[Param 1.1: 4-8 bytes]
[Param 1.2: 4-8 bytes]
[Opcode 2: 4 bytes]
...
```

### 7.3 Crimson TNG API

**Question:** What API does Crimson TNG provide?

**Actions:**
1. Ask Per Vices for API documentation
2. Check if Python bindings exist
3. If not, use REST API or custom protocol

**Expected:**
```python
import crimson_tng

crimson = crimson_tng.SDR(ip='192.168.1.100')
crimson.set_tx_frequency(channel=1, freq=400e6)
crimson.upload_tx_waveform(channel=1, i_samples=..., q_samples=...)
crimson.trigger_sequence()
crimson.start_rx()
data = crimson.get_rx_data()
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# test_acode_parser.py
def test_parse_event1():
    parser = AcodeParser('test_data/event1.acode')
    acode = parser.parse_next_acode()
    assert acode['op'] == 'EVENT1'
    assert acode['timing'] > 0
    assert acode['gates'] != 0

def test_parse_simple_sequence():
    parser = AcodeParser('test_data/s2pul.acode')
    acodes = parser.parse_all()
    assert len(acodes) > 0
    assert acodes[0]['op'] == 'INITFREQ'
    assert acodes[-1]['op'] == 'acqend'
```

### 8.2 Integration Tests

**Test 1: Simple Pulse (s2pul)**
- Compile s2pul → Acodes
- Bridge translates → Crimson commands
- Acquire FID
- Verify: FID amplitude, SNR, phase

**Test 2: Cross-Polarization (hX)**
- Compile hX → Acodes
- Bridge translates → dual-channel CP
- Acquire FID
- Verify: CP enhancement (>2×), decoupling effectiveness

**Test 3: 2D Acquisition (hX with t1)**
- Compile hX with ni>1
- Bridge executes 2D loop
- Acquire all t1 points
- Verify: 2D matrix correct, phasing correct

---

## 9. Next Immediate Steps

**Today (Nov 21):**
1. ✅ Clone vnmrj-nmr-tools (hX pulse sequences)
2. ✅ Examine hX.c structure
3. ✅ Identify PSG functions used
4. ✅ Map to Acode opcodes
5. ⏳ **Find Acode file location** (next task)

**Tomorrow (Nov 22):**
1. Compile simple sequence in OVJ
2. Locate and hexdump Acode file
3. Write initial acode_parser.py
4. Test parsing

**Week of Dec 2:**
1. Complete Acode parser
2. Begin waveform generator
3. Design Crimson API (pending Per Vices docs)

---

## 10. Success Criteria

**Phase 1 (Dec):**
- ✅ Acode parser reads and interprets all major opcodes
- ✅ Can print human-readable sequence from Acodes

**Prototype (Feb 2026):**
- ✅ Simple pulse (s2pul) runs end-to-end
- ✅ FID loads in OVJ and processes correctly
- ✅ SNR matches expectations (>50:1 on adamantane)

**Indiana Beta (May 2026):**
- ✅ hX, hXX, hYXX sequences fully working
- ✅ 2D/3D acquisition stable
- ✅ System reliable for 8+ hour experiments

---

**Document Status:** Analysis complete, ready for implementation

**Next Action:** Locate Acode output file and parse first test case (s2pul)
