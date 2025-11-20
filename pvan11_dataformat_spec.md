# PVAN-11 Data Format Specification

**Source:** https://support.pervices.com/application-notes/pvan-11-dataformat-spec/
**Retrieved:** 2025-11-20
**Platform:** Per Vices Crimson TNG / Cyan SDR

## Overview

PVAN-11 is Per Vices' implementation of the **VITA 49 (VRT)** standard for digitized RF data transport over UDP/IP networks. The format provides a complete network stack from Ethernet frames through application-layer VITA 49 packets.

**Key Point:** PVAN-11 = VITA 49 implementation (industry standard for RF data streaming)

## Network Stack Architecture

| Layer | Protocol | Details |
|-------|----------|---------|
| **Link Layer** | Ethernet | Standard Ethernet frames containing all upper protocol layers |
| **Internet Layer** | IPv4 | Protocol number 17 (designates UDP transport) |
| **Transport Layer** | UDP | Standard UDP headers for packet delivery |
| **Application Layer** | VITA 49 | Signal Data Packets with headers + I/Q payload |

## VITA 49 Packet Header Structure (32-bit words)

### Header Fields

| Field | Bit Pattern | Description |
|-------|-------------|-------------|
| **Packet Type** | 0000 or 0001 | Signal Data with/without Stream Identifier |
| **C Bit** | 0 | No Class Identifier field present |
| **Indicators** | (0\|1)01 | Trailer present, VITA indicator, packet type flags |
| **TSI** | 00 | No integer-seconds timestamp |
| **TSF** | 00 or 11 | Timestamp format: None or Free-Running Count |
| **Packet Count** | Variable | Increments with each packet (modulo sequence) |
| **Packet Size** | Variable | Total 32-bit words in entire packet |

### Packet Components

1. **Stream Identifier (optional):** 32-bit number identifying packet stream
2. **Fractional Timestamp:** Free-running counter starting at zero, incrementing per sample
3. **IQ Data Payload:** Complex samples (see format below)
4. **Trailer:** Present in Rx packets, all bits zero

## I/Q Data Format

### Complex Sample Structure (32 bits per I/Q pair)

Each I/Q pair is **32 bits total**, split into two **16-bit signed integers**:

| Bits | Component | Description |
|------|-----------|-------------|
| 31:24 | Real[7:0] | I component, low byte |
| 23:16 | Real[15:8] | I component, high byte |
| 15:8 | Imaginary[7:0] | Q component, low byte |
| 7:0 | Imaginary[15:8] | Q component, high byte |

**Data Type:** `int16_t` for both I and Q
**Byte Order:** Big-endian (network byte order)
**Range:** -32768 to +32767 (16-bit signed)

### Example I/Q Pair Unpacking (C/C++)

```c
// Assume 'data' is uint32_t containing one I/Q pair
int16_t I = (int16_t)((data >> 16) & 0xFFFF);  // Extract Real (I)
int16_t Q = (int16_t)(data & 0xFFFF);          // Extract Imaginary (Q)
```

### Example I/Q Pair Unpacking (Python)

```python
import struct

# Assume 'packet' is bytes containing I/Q data
# Each I/Q pair is 4 bytes (32 bits)
for i in range(0, len(packet), 4):
    iq_pair = packet[i:i+4]
    I, Q = struct.unpack('>hh', iq_pair)  # Big-endian, two signed shorts
    # Now I and Q are int16 values (-32768 to +32767)
```

## Timestamps

**Fractional Timestamp Format:**
- Counter starts at zero when streaming begins
- Increments by 1 for each I/Q sample
- Used to reconstruct sample timing and detect dropped packets

**Example:** If sample rate is 325 MSPS, timestamp increments every 1/325 MHz = 3.077 ns

## UDP Streaming Characteristics

- **Interface:** 10 GbE SFP+ ports
- **Protocol:** UDP (connectionless, low-latency)
- **Packet Loss Handling:** Application must detect via packet count or timestamp gaps
- **Max Throughput:** Limited by 10 GbE (~10 Gbps theoretical, ~9 Gbps practical)

## Practical Implementation Notes

### For NMR Application (Crimson TNG)

**Receive Path (Crimson TNG → Host):**
1. Crimson TNG ADC samples at 325 MSPS (16-bit I/Q)
2. FPGA packetizes I/Q data into VITA 49 packets
3. UDP packets transmitted over 10 GbE to host
4. Host receives UDP packets, parses PVAN-11 headers
5. Extract I/Q samples, reconstruct time-domain signal
6. Apply host-side FIR filtering (decimation to final bandwidth)

**Transmit Path (Host → Crimson TNG):**
1. Host generates I/Q waveform samples (16-bit)
2. Packetize into PVAN-11 format
3. Transmit UDP packets over 10 GbE to Crimson TNG
4. FPGA buffers I/Q data, feeds DAC at 325 MSPS
5. RF output to NMR probe

### Packet Loss Detection

```python
last_packet_count = None

def check_packet_loss(packet_count):
    global last_packet_count
    if last_packet_count is not None:
        expected = (last_packet_count + 1) % 256  # Assuming 8-bit counter
        if packet_count != expected:
            dropped = (packet_count - expected) % 256
            print(f"WARNING: Dropped {dropped} packets")
    last_packet_count = packet_count
```

### Bandwidth Calculation

**Example:** 4 Rx channels @ 325 MSPS, 32 bits per I/Q pair
- Data rate per channel: 325 × 10^6 samples/sec × 4 bytes/sample = 1.3 GB/sec
- Total for 4 channels: 5.2 GB/sec = 41.6 Gbps

**Implication:** Requires decimation in FPGA to stay within 10 GbE bandwidth limits.

For NMR with 5 MHz final bandwidth:
- Decimation factor: 325 / 5 = 65x
- Reduced rate: 41.6 / 65 = 0.64 Gbps (well within 10 GbE capacity)

## Additional Resources

Per Vices provides:
- **Wireshark packet captures:** Example PVAN-11 packets for analysis
- **GNU Radio example scripts:** Reference implementation for VITA 49 parsing

**Documentation URL:** https://support.pervices.com/application-notes/pvan-11-dataformat-spec/

## Relevance to Resynant NMR Project

**Critical for Software Development (Phase 1, Dec 2025 - Jan 2026):**

1. **UDP Data Receiver (Weeks 1-2):**
   - Must parse VITA 49 headers (packet type, count, size)
   - Extract Stream Identifier for multi-channel demultiplexing
   - Unpack I/Q pairs from 32-bit format to int16 arrays

2. **Packet Loss Monitoring:**
   - Track Packet Count field to detect dropped packets
   - Use Fractional Timestamp to verify sample continuity
   - Tolerance: <0.01% packet loss (acceptance criteria)

3. **Multi-Channel Handling:**
   - Each Rx channel (1-4) may use separate Stream Identifier
   - Demultiplex packets by Stream ID before processing
   - Maintain separate buffers per channel

4. **Data Processing Pipeline (Weeks 3-4):**
   - Convert int16 I/Q to float32 for DSP operations
   - Apply host-side FIR filtering (decimation to final BW)
   - FFT for spectral analysis (NMR frequency-domain signal)

**Language Recommendations:**
- **Python:** Initial prototyping (struct module for unpacking, NumPy for DSP)
- **C++:** Production version (performance-critical UDP receiver, real-time constraints)

**Next Steps:**
- Review VITA 49 standard (ANSI/VITA 49.0) for detailed specification
- Download Per Vices Wireshark captures for packet analysis
- Test UDP receiver with Crimson TNG simulator (if available) or packet replays
