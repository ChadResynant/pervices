# OpenVNMRJ to Crimson TNG Bridge

Python bridge layer that translates OpenVNMRJ pulse sequence compiler (PSG) output to Per Vices Crimson TNG SDR commands.

## Architecture

```
OpenVNMRJ PSG Compiler
       ↓
Binary Acode Files (/vnmrsystem/acqqueue/exp1.greg.012345.ps.*)
       ↓
Bridge Daemon (monitors psgdone file)
       ↓
Acode Parser (acode_parser.py)
       ↓
Pulse Generator (pulse_generator.py)
       ↓
Crimson TNG API (crimson_api.py - TODO)
       ↓
Per Vices Crimson TNG Hardware
```

## Components

### bridge_daemon.py

Main daemon that monitors OpenVNMRJ experiment directories for PSG compilation completion.

**Features:**
- Watches `{curexp}/psgdone` file for PSG completion signal
- Reads `goid` parameter to locate Acode files
- Loads all controller Acode files (Master1, RF1, RF2, etc.)
- Coordinates multi-channel execution on Crimson TNG

**Usage:**
```bash
# Monitor single experiment
python bridge_daemon.py /vnmr/exp1

# Monitor multiple experiments
python bridge_daemon.py /vnmr/exp1 /vnmr/exp2 /vnmr/exp3

# Dry-run mode (parsing only, no hardware)
python bridge_daemon.py --dry-run /vnmr/exp1

# Debug logging
python bridge_daemon.py --log-level DEBUG /vnmr/exp1
```

### acode_parser.py

Binary parser for OpenVNMRJ Acode files.

**Supported Opcodes:**
- `EVENT1` (46): RF pulse with timing and gate pattern
- `EVENT2` (47): Multi-gate event
- `INITFREQ` (57): Set RF frequency
- `PHASESHIFT` (70): Set RF phase
- `acqstart` (44): Start data acquisition
- `acqend` (45): End data acquisition
- `HALT` (13): End of sequence
- `BRANCH` (various): Looping constructs

**Usage:**
```python
from acode_parser import AcodeParser

parser = AcodeParser('/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1')
opcodes = parser.parse()

for opcode in opcodes:
    print(f"{opcode['opcode']}: {opcode}")
```

### pulse_generator.py

Generate I/Q waveforms from pulse specifications for Crimson TNG DACs.

**Waveform Types:**
- `rectangular_pulse()`: Basic RF pulse with phase control
- `cp_ramp()`: Cross-polarization ramp (linear or tangent)
- `tppm_sequence()`: Two-pulse phase modulation decoupling
- `shaped_pulse()`: Gaussian, sinc, Hermite shaped pulses
- `delay()`: Zero-amplitude delay

**Usage:**
```python
from pulse_generator import PulseGenerator

gen = PulseGenerator(sample_rate=325e6)  # 325 MSPS

# Generate 10 μs rectangular pulse at 90° phase
i_data, q_data = gen.rectangular_pulse(
    duration=10e-6,
    phase=90.0,
    amplitude=1.0
)

# Generate CP ramp (1 ms, linear 0→100%)
i_data, q_data = gen.cp_ramp(
    duration=1e-3,
    start_amplitude=0.0,
    end_amplitude=1.0,
    ramp_type='linear',
    phase=0.0
)
```

### crimson_api.py (TODO)

Wrapper for Crimson TNG hardware control.

**Required Functions:**
- `set_frequency(channel, freq)`: Set RF frequency
- `set_power(channel, power)`: Set output power
- `upload_waveform(channel, i_data, q_data)`: Upload I/Q waveform to FPGA
- `trigger_gpio(channel, state)`: Control GPIO trigger lines
- `start_acquisition(channel)`: Start Rx data acquisition
- `stop_acquisition(channel)`: Stop Rx data acquisition
- `execute_multi_channel(sequences)`: Coordinate multi-channel execution

**Awaiting:** Per Vices Crimson TNG API documentation and Python bindings.

## File Locations

### OpenVNMRJ Directories

| Path | Description |
|------|-------------|
| `/vnmr/exp{N}/` | Experiment directory (N = 1-8) |
| `/vnmr/exp{N}/curpar` | Parameter file (contains goid) |
| `/vnmr/exp{N}/psgdone` | PSG completion signal |
| `/vnmrsystem/acqqueue/` | Acquisition queue directory |

### Acode Files

**Pattern:** `{goid}.{stage}.{controller}`

**Example:**
```
/vnmrsystem/acqqueue/exp1.greg.012345.ps.Master1
/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1
/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF2
```

**Controllers:**
- `Master1`: Master timing and synchronization
- `RF1`, `RF2`, `RF3`, `RF4`: RF transmit channels
- `PFG1`: Pulsed field gradients (if used)
- `DDR1`: Direct digital receiver (legacy)

## Installation

### Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or manually:
pip install watchdog numpy pytest pytest-cov
```

### System Requirements

- Python 3.8+
- OpenVNMRJ installation (for production use)
- Per Vices Crimson TNG (for hardware execution)

### Development Setup

```bash
# Clone repository
cd /home/user/pervices/software/ovj_bridge

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_bridge.py -v
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest test_bridge.py -v

# Run with coverage
pytest test_bridge.py --cov=. --cov-report=html

# Run specific test
pytest test_bridge.py::TestAcodeFileLocator::test_extract_controller_name -v
```

### Integration Testing

**Step 1:** Compile a simple pulse sequence in OpenVNMRJ
```
# In VnmrJ console
cd /vnmr/exp1
go('s2pul')
```

**Step 2:** Start bridge daemon
```bash
python bridge_daemon.py --dry-run /vnmr/exp1
```

**Step 3:** Verify bridge detects PSG completion
```
2025-11-21 14:23:45 - bridge_daemon - INFO - PSG completion detected: /vnmr/exp1/psgdone
2025-11-21 14:23:45 - bridge_daemon - INFO - goid: /vnmrsystem/acqqueue/exp1.greg.012345
2025-11-21 14:23:45 - bridge_daemon - INFO - Found 2 Acode file(s):
2025-11-21 14:23:45 - bridge_daemon - INFO -   Master1: /vnmrsystem/acqqueue/exp1.greg.012345.ps.Master1
2025-11-21 14:23:45 - bridge_daemon - INFO -   RF1: /vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1
```

## Workflow

### Normal Operation

1. **User initiates acquisition in OpenVNMRJ:**
   ```
   go('hX')  # 1H-13C HETCOR experiment
   ```

2. **PSG compiles pulse sequence:**
   - Reads `hX.c` pulse sequence
   - Compiles to binary Acode files
   - Writes completion signal to `/vnmr/exp1/psgdone`

3. **Bridge daemon detects completion:**
   - Watchdog detects `psgdone` file creation
   - Reads `goid` parameter from `curpar`
   - Locates all Acode files matching `{goid}.ps.*`

4. **Bridge parses Acode files:**
   - Loads `Master1`, `RF1`, `RF2` Acode files
   - Parses binary opcodes (EVENT1, INITFREQ, etc.)
   - Extracts timing, frequency, phase, gate patterns

5. **Bridge translates to Crimson TNG:**
   - Maps RF1 → Crimson Tx channel 1
   - Maps RF2 → Crimson Tx channel 2
   - Generates I/Q waveforms for each pulse
   - Configures GPIO triggers for Tx gates

6. **Crimson TNG executes sequence:**
   - Uploads waveforms to FPGA buffers
   - Starts multi-channel synchronized execution
   - Streams Rx data over 10 GbE (PVAN-11 format)

7. **Data returns to OpenVNMRJ:**
   - Bridge receives PVAN-11 packets
   - Converts to VnmrJ FID format
   - Writes FID file to `/vnmr/exp1/acqfil/fid`

## Debugging

### Enable Debug Logging

```bash
python bridge_daemon.py --log-level DEBUG /vnmr/exp1
```

### Manually Trigger Bridge

```python
from bridge_daemon import AcodeBridge

bridge = AcodeBridge(watch_dirs=['/vnmr/exp1'], crimson_api=None)
bridge.on_psg_complete('/vnmr/exp1')  # Manually trigger processing
```

### Examine Acode Files

```bash
# Hexdump first 256 bytes
hexdump -C /vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1 | head -20

# Parse with acode_parser
python -c "
from acode_parser import AcodeParser
parser = AcodeParser('/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1')
opcodes = parser.parse()
for op in opcodes[:10]:
    print(op)
"
```

### Verify Parameter Reading

```bash
# Check goid parameter
python -c "
from bridge_daemon import VnmrJParameterReader
reader = VnmrJParameterReader('/vnmr/exp1')
print(reader.read_parameter('goid'))
"
```

## Known Limitations

1. **Crimson API Not Implemented:** Currently running in dry-run mode only. Awaiting Per Vices API documentation.

2. **No Data Acquisition Return Path:** Bridge can execute sequences but cannot yet return Rx data to OpenVNMRJ FID format.

3. **Limited Opcode Support:** Only core opcodes implemented. Advanced features (shaped pulses, real-time variables) need additional development.

4. **No Error Recovery:** If Crimson TNG execution fails, bridge does not notify OpenVNMRJ console.

## Roadmap

### Phase 1: Prototype (Dec 2025 - Jan 2026)
- ✅ Acode parser implementation
- ✅ Pulse waveform generator
- ✅ Bridge daemon with file monitoring
- ⏳ Crimson TNG API wrapper
- ⏳ Simple pulse (s2pul) end-to-end test

### Phase 2: hX/hXX Support (Feb-Mar 2026)
- Multi-channel CP sequences
- TPPM decoupling integration
- 2D acquisition loops and phase cycling
- FID data return to OpenVNMRJ

### Phase 3: Production (Apr-May 2026)
- Harmonyzer system integration
- Advanced pulse sequences (3D experiments)
- Real-time variable support
- Error handling and logging

## Contributing

**Contact:** Chad Rienstra (chad@resynant.com)

**Documentation:**
- `PSG_ACODE_ANALYSIS.md`: Acode format specification
- `OVJ_CRIMSON_INTEGRATION_ARCHITECTURE.md`: Bridge architecture design
- `ACODE_FILE_LOCATION.md`: File path and interception strategy

---

*Last Updated: November 21, 2025*
*Author: Chad Rienstra / Claude Code*
