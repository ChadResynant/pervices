# Crimson TNG API Documentation Summary

**Date:** November 21, 2025
**Purpose:** Implementation guide for Crimson TNG API integration in OpenVNMRJ bridge

---

## Executive Summary

Per Vices Crimson TNG uses the **UHD (USRP Hardware Driver) API**, providing a USRP-compatible Python interface. This is excellent news - the API is well-documented with extensive examples.

**Key Finding:** The Crimson TNG API is not proprietary - it uses the industry-standard UHD framework from Ettus Research, with Per Vices maintaining their own fork.

---

## API Architecture

### Primary Interface: UHD MultiUSRP

**Repository:** https://github.com/pervices/uhd

The Crimson TNG is controlled via the `uhd.usrp.MultiUSRP` Python class, providing:
- Channel configuration (frequency, gain, sample rate)
- Waveform transmission
- Data acquisition
- GPIO control
- Timing/synchronization

### Alternative Interface: PyCrimson

**Repository:** https://github.com/Spinmob/pycrimson
**Installation:** `pip install pycrimson`

Higher-level wrapper providing simplified interface for basic operations.

---

## Installation

### Method 1: Per Vices UHD Package (Recommended)

```bash
# Contact support@pervices.com for package repository access
# Per Vices provides pre-built packages for Ubuntu/Debian:
# - libuhdpv (UHD library)
# - uhdpv-host (Host utilities)
# - python3-uhdpv (Python bindings)

# Installation (once repository is configured):
sudo apt-get update
sudo apt-get install python3-uhdpv
```

### Method 2: Build from Source

```bash
git clone https://github.com/pervices/uhd.git
cd uhd/host
mkdir build && cd build
cmake -DENABLE_PYTHON_API=ON -DENABLE_EXAMPLES=ON ..
make -j4
sudo make install
sudo ldconfig
```

### Method 3: PyCrimson (Quick Prototyping)

```bash
pip install pycrimson
```

---

## Python API Examples

### Basic Connection and Configuration

```python
import uhd
import numpy as np

# Initialize Crimson TNG (replace with your device IP)
usrp = uhd.usrp.MultiUSRP("addr=192.168.10.2")

# Configure RX channel 0
center_freq = 100e6  # 100 MHz
sample_rate = 10e6   # 10 MSPS
rx_gain = 30         # dB

usrp.set_rx_rate(sample_rate, 0)
usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
usrp.set_rx_gain(rx_gain, 0)

# Configure TX channel 0
tx_freq = 100e6
tx_gain = 10

usrp.set_tx_rate(sample_rate, 0)
usrp.set_tx_freq(uhd.libpyuhd.types.tune_request(tx_freq), 0)
usrp.set_tx_gain(tx_gain, 0)
```

### Receiving I/Q Data

```python
# Method 1: High-level receive (finite samples)
num_samples = 1000000
samples = usrp.recv_num_samps(
    num_samps=num_samples,
    freq=center_freq,
    rate=sample_rate,
    channels=[0],
    gain=rx_gain
)

# Method 2: Streaming receive (continuous)
st_args = uhd.usrp.StreamArgs("fc32", "sc16")  # float32 CPU, int16 wire format
st_args.channels = [0]
rx_streamer = usrp.get_rx_stream(st_args)

# Allocate buffer
max_samps_per_packet = rx_streamer.get_max_num_samps()
recv_buffer = np.zeros(max_samps_per_packet, dtype=np.complex64)

# Start streaming
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
stream_cmd.stream_now = True
rx_streamer.issue_stream_cmd(stream_cmd)

# Receive samples
metadata = uhd.types.RXMetadata()
num_rx_samps = rx_streamer.recv(recv_buffer, metadata)
```

### Transmitting I/Q Waveforms

```python
# Generate waveform (example: sine wave)
duration = 1.0  # seconds
waveform = uhd.dsp.signals.get_continuous_tone(
    wave_freq=1e6,      # 1 MHz tone
    amplitude=0.7,
    sample_rate=sample_rate
)

# Method 1: High-level transmit
usrp.send_waveform(
    waveform_proto=waveform,
    duration=duration,
    freq=tx_freq,
    rate=sample_rate,
    channels=[0],
    gain=tx_gain
)

# Method 2: Streaming transmit (for continuous waveforms)
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0]
tx_streamer = usrp.get_tx_stream(st_args)

# Send samples
metadata = uhd.types.TXMetadata()
metadata.has_time_spec = False
tx_streamer.send(waveform, metadata)
```

### GPIO Control (for Tx/Rx Gating)

```python
# Define GPIO configuration
GPIO_BANK = "FP0"  # Front panel GPIO (device-specific - verify with Per Vices)
PIN_MASK = 1 << 6  # Control pin 6

# Set as output
usrp.set_gpio_attr(GPIO_BANK, "DDR", PIN_MASK, PIN_MASK)

# Manual control mode (not ATR)
usrp.set_gpio_attr(GPIO_BANK, "CTRL", 0, PIN_MASK)

# Set output high
usrp.set_gpio_attr(GPIO_BANK, "OUT", PIN_MASK, PIN_MASK)

# Set output low
usrp.set_gpio_attr(GPIO_BANK, "OUT", 0, PIN_MASK)

# ATR mode (automatic Tx/Rx switching)
usrp.set_gpio_attr(GPIO_BANK, "CTRL", PIN_MASK, PIN_MASK)  # Enable ATR
usrp.set_gpio_attr(GPIO_BANK, "ATR_TX", PIN_MASK, PIN_MASK)  # High during TX
usrp.set_gpio_attr(GPIO_BANK, "ATR_RX", 0, PIN_MASK)  # Low during RX
```

---

## State Tree Configuration

Crimson TNG uses a hierarchical "state tree" for low-level configuration access.

### Common State Tree Paths

```python
# Access state tree
tree = usrp.get_tree()

# RX Channel Configuration (A, B, C, D)
rx_freq = tree["/mboards/0/rx_a/rf/freq/val"].get()
tree["/mboards/0/rx_a/rf/freq/val"].set(100e6)

rx_gain = tree["/mboards/0/rx_a/rf/gain/val"].get()
tree["/mboards/0/rx_a/rf/gain/val"].set(30.0)

rx_rate = tree["/mboards/0/rx_a/dsp/rate"].get()
tree["/mboards/0/rx_a/dsp/rate"].set(10e6)

# TX Channel Configuration (A, B, C, D)
tree["/mboards/0/tx_a/rf/freq/val"].set(100e6)
tree["/mboards/0/tx_a/rf/gain/val"].set(10.0)
tree["/mboards/0/tx_a/dsp/rate"].set(10e6)

# Global Settings
tree["/mboards/0/time/clk_pps"].set(...)  # PPS synchronization
tree["/mboards/0/fpga/link_max_payload"].set(...)  # Packet size
```

---

## Multi-Channel Phase Coherency

**Critical for NMR:** All Tx/Rx channels must maintain phase coherency (<2° std dev).

### Channel Synchronization

```python
# Configure multiple TX channels with same sample rate
for ch in range(4):  # 4 Tx channels
    usrp.set_tx_rate(325e6, ch)  # 325 MSPS
    usrp.set_tx_freq(uhd.libpyuhd.types.tune_request(freq), ch)

# Configure multiple RX channels
for ch in range(4):  # 4 Rx channels
    usrp.set_rx_rate(325e6, ch)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(freq), ch)

# Multi-channel transmit
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0, 1, 2, 3]  # All 4 Tx channels
tx_streamer = usrp.get_tx_stream(st_args)

# Waveforms must be synchronized in time
# Use timed commands for deterministic phase relationship
```

### Timed Commands (for Phase-Coherent Execution)

```python
import time

# Set command time (future time for synchronization)
cmd_time = usrp.get_time_now() + uhd.types.TimeSpec(0.1)  # 100 ms in future

# Queue timed frequency change
usrp.set_command_time(cmd_time)
usrp.set_tx_freq(uhd.libpyuhd.types.tune_request(new_freq), 0)
usrp.clear_command_time()

# All channels execute frequency change at exact same time
```

---

## Data Format: PVAN-11 (VITA 49)

Crimson TNG streams data over UDP using PVAN-11 packet format (VITA 49 standard).

**Reference:** https://support.pervices.com/application-notes/pvan-11-dataformat-spec/

**Good News:** We already have this implemented in `/home/user/pervices/software/src/udp_receiver.py`!

The UHD API handles PVAN-11 packet parsing internally when using streaming methods.

---

## Documentation Resources

### Official Per Vices Support Portal

**Base URL:** https://support.pervices.com/

**Key Pages:**
- **Crimson Overview:** https://support.pervices.com/crimson/welcome/
- **System Architecture:** https://support.pervices.com/crimson/sys/
- **Networking Setup:** https://support.pervices.com/crimson/networking/
- **Specifications:** https://support.pervices.com/crimson/specs/

### Application Notes (PVAN Series)

- **PVAN-8:** Frequency Tuning Guide: https://support.pervices.com/application-notes/pvan-8/
- **PVAN-10:** Trigger Functionality: https://support.pervices.com/application-notes/pvan-10-devicetriggers/
- **PVAN-11:** Data Format (VITA 49): https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
- **PVAN-15:** System Time Synchronization: https://support.pervices.com/application-notes/pvan-15-system-time/

### How-To Guides (PVHT Series)

- **PVHT-3:** UHD/GNURadio Setup: https://support.pervices.com/how-to/pvht-3-softwaresetup/
- **PVHT-7:** Plot I/Q Data in Python: https://support.pervices.com/how-to/pvht-7-reading-GRC-data/
- **PVHT-13:** Web UI Guide: https://support.pervices.com/how-to/pvht-13-web-UI/
- **PVHT-15:** Get/Set Tree Paths (May require login)

### Tutorials (PVT Series)

- **PVT-0:** Building Waterfall Plot: https://support.pervices.com/tutorials/pvt-0/
- **PVT-6:** QPSK Modem Demo: https://support.pervices.com/tutorials/pvt-6/

### GitHub Repositories

- **Per Vices UHD Fork:** https://github.com/pervices/uhd
- **Example Programs:** https://github.com/pervices/examples
- **PyCrimson Library:** https://github.com/Spinmob/pycrimson
- **Webserver:** https://github.com/pervices/webserver
- **Releases/Firmware:** https://github.com/pervices/releases

### External UHD Documentation

- **Ettus UHD Manual:** https://files.ettus.com/manual/
- **UHD Python API Reference:** https://files.ettus.com/manual/page_python.html
- **PySDR Tutorial:** https://pysdr.org/content/usrp.html

---

## Implementation Plan for crimson_api.py

### Step 1: Replace Initialization (IMMEDIATE)

```python
import uhd
import numpy as np

class CrimsonAPI:
    def __init__(self, host: str = '192.168.10.2', port: int = None):
        self.host = host
        self.usrp = None
        self.connected = False

        # Connect to Crimson TNG
        self._connect()

    def _connect(self):
        """Establish connection to Crimson TNG via UHD."""
        try:
            addr_str = f"addr={self.host}"
            self.usrp = uhd.usrp.MultiUSRP(addr_str)
            self.connected = True
            logger.info(f"Connected to Crimson TNG at {self.host}")
        except Exception as e:
            raise CrimsonTNGError(f"Failed to connect to Crimson TNG: {e}")
```

### Step 2: Implement Core Methods

```python
def set_frequency(self, channel: int, frequency: float, channel_type: str = 'tx'):
    """Set RF frequency using UHD API."""
    if not self.connected:
        raise CrimsonTNGError("Not connected to Crimson TNG")

    tune_req = uhd.libpyuhd.types.tune_request(frequency)

    if channel_type == 'tx':
        self.usrp.set_tx_freq(tune_req, channel)
    else:
        self.usrp.set_rx_freq(tune_req, channel)

    logger.info(f"Set {channel_type.upper()} channel {channel} to {frequency/1e6:.3f} MHz")

def set_power(self, channel: int, power_dbm: float):
    """Set TX gain (UHD uses gain, not power)."""
    # Convert power to gain (device-specific calibration may be needed)
    self.usrp.set_tx_gain(power_dbm, channel)
    logger.info(f"Set TX channel {channel} gain to {power_dbm:.1f} dB")

def upload_waveform(self, channel: int, i_data: np.ndarray, q_data: np.ndarray):
    """Upload I/Q waveform using UHD streaming."""
    # Combine I/Q into complex array
    waveform = i_data.astype(np.float32) / 30000.0 + 1j * q_data.astype(np.float32) / 30000.0

    # Create TX streamer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [channel]
    tx_streamer = self.usrp.get_tx_stream(st_args)

    # Send waveform
    metadata = uhd.types.TXMetadata()
    metadata.has_time_spec = False
    tx_streamer.send(waveform, metadata)

    logger.info(f"Uploaded {len(waveform)} samples to TX channel {channel}")

def start_acquisition(self, channel: int, duration_ms: Optional[float] = None):
    """Start RX acquisition."""
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [channel]
    rx_streamer = self.usrp.get_rx_stream(st_args)

    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    stream_cmd.stream_now = True
    rx_streamer.issue_stream_cmd(stream_cmd)

    logger.info(f"Started acquisition on RX channel {channel}")
    return rx_streamer
```

### Step 3: GPIO Implementation (REQUIRES PER VICES GUIDANCE)

**CRITICAL QUESTION FOR PER VICES:**
- What is the GPIO bank name for Crimson TNG? ("FP0", "TRIG", etc.?)
- How many GPIO pins available?
- Does custom GPIO expander board have different API?

```python
def trigger_gpio(self, gpio_channel: int, state: bool):
    """Set GPIO trigger line state."""
    # TODO: Verify GPIO bank name with Per Vices
    GPIO_BANK = "FP0"  # PLACEHOLDER - VERIFY WITH PER VICES

    pin_mask = 1 << gpio_channel

    # Set as output
    self.usrp.set_gpio_attr(GPIO_BANK, "DDR", pin_mask, pin_mask)

    # Manual control mode
    self.usrp.set_gpio_attr(GPIO_BANK, "CTRL", 0, pin_mask)

    # Set state
    if state:
        self.usrp.set_gpio_attr(GPIO_BANK, "OUT", pin_mask, pin_mask)
    else:
        self.usrp.set_gpio_attr(GPIO_BANK, "OUT", 0, pin_mask)

    logger.info(f"Set GPIO {gpio_channel} to {'HIGH' if state else 'LOW'}")
```

---

## Outstanding Questions for Per Vices

**Contact:** Brandon Malatest (brandon.m@pervices.com, +1 647-534-9007)

### GPIO Expander Board
1. What is the GPIO bank name for the custom expander board?
2. How many channels available (requirements say 8-12)?
3. What is the API for controlling expander board GPIOs?
4. Can we get ±100ns timing precision with UHD GPIO API, or requires FPGA modification?
5. Cost and delivery timeline for GPIO expander board?

### FPGA CIC Decimation Filters
6. Are CIC decimation filters included in standard Crimson TNG, or custom development?
7. If custom, what is NRE cost and timeline?
8. Can we achieve 17-bit ENOB @ 5 MHz without CIC filters using host-side decimation?

### Phase Coherency
9. Factory calibration for phase coherency - what is measured specification?
10. Does UHD API provide phase calibration coefficients we should apply?
11. How to verify <2° std dev phase coherency across channels?

### Multi-Channel Waveform Buffering
12. Does Crimson TNG support FPGA-based waveform looping (for decoupling sequences)?
13. If not, what is maximum continuous waveform duration via 10 GbE streaming?

### Documentation Access
14. Can we get access to restricted support.pervices.com pages (403 errors)?
15. Are there NMR-specific application notes or example code?

---

## Next Steps

### Immediate (This Week)
1. ✅ Install UHD Python bindings: `pip install pycrimson` (for quick testing)
2. ✅ Clone Per Vices examples: `git clone https://github.com/pervices/examples.git`
3. **Update crimson_api.py** with UHD-based implementation
4. **Contact Per Vices** (Brandon Malatest) with questions above

### Phase 1 (Dec 2025)
5. Test basic UHD API on Crimson TNG simulator or hardware
6. Validate frequency setting, gain control, sample rate
7. Implement waveform upload for rectangular pulses
8. Test GPIO control (once bank name confirmed)

### Phase 2 (Jan 2026)
9. Implement multi-channel synchronization with timed commands
10. Validate phase coherency measurement
11. Integrate with FID writer for data return path
12. End-to-end test: Acode → Waveform → Crimson → UDP → FID → OpenVNMRJ

---

## Summary

**Excellent News:** Crimson TNG uses industry-standard UHD API with extensive documentation and examples. This is far better than a proprietary API.

**Implementation Status:** Can immediately start updating `crimson_api.py` with UHD methods.

**Remaining Gaps:**
- GPIO expander board details (custom hardware, needs Per Vices input)
- FPGA CIC decimation (may be custom development)
- Multi-channel phase synchronization validation

**Risk Assessment:** **LOW** - UHD API is well-proven and documented. Main risks are NMR-specific hardware customizations (GPIO, FPGA).

---

**Document Status:** Complete API research summary
**Next Action:** Update crimson_api.py with UHD implementation
**Contact Per Vices:** For GPIO/FPGA customization details
