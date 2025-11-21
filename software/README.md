# Per Vices Crimson TNG - NMR Data Acquisition Software

## Overview

This software package provides UDP data acquisition, signal processing, and control interface for the Per Vices Crimson TNG SDR platform integrated with Resynant Harmonyzer NMR spectrometer.

## Project Structure

```
software/
├── src/                    # Source code
│   ├── udp_receiver.py     # PVAN-11 packet reception and parsing
│   ├── signal_processing.py # I/Q processing, FIR filters, FFT
│   ├── pulse_sequence.py   # Pulse sequence compiler
│   └── crimson_control.py  # Crimson TNG API wrapper
├── tests/                  # Unit and integration tests
├── docs/                   # Additional documentation
├── data/                   # Test data and samples
└── pervices-nmr-env/       # Python virtual environment

```

## Development Setup

### Prerequisites
- Python 3.8+
- NumPy, SciPy, Matplotlib

### Installation

```bash
# Activate virtual environment
source pervices-nmr-env/bin/activate

# Install dependencies
pip install numpy scipy matplotlib

# Run tests (when available)
python -m pytest tests/
```

## Current Development Status

**Sprint: Nov 21-24, 2025**
- [x] Development environment setup
- [ ] UDP receiver skeleton code
- [ ] PVAN-11 packet parsing
- [ ] Signal processing pipeline
- [ ] Test harness

## Key Components

### 1. UDP Receiver (Priority 1)
- Parse PVAN-11 packet format from Crimson TNG
- Real-time I/Q data extraction
- Ring buffer for streaming acquisition

### 2. Signal Processing Pipeline
- I/Q to complex data conversion
- Host-side FIR filtering and decimation
- FFT for spectral analysis

### 3. Pulse Sequence Compiler
- High-level NMR sequence description
- Timed waveform buffer generation
- GPIO trigger scheduling

### 4. Control Interface
- Crimson TNG API wrapper
- Frequency, power, timing control
- Status monitoring

## References

- PVAN-11 Data Format: ../pvan11_dataformat_spec.md
- Technical Requirements: ../technical_requirements.md
- NMR Pulse Sequences: ../nmr_pulse_sequences.md

## Timeline

- **Prototype Software:** Dec 2025 - Jan 2026
- **Hardware Integration:** Feb 2026
- **Validation Testing:** Feb-Mar 2026
- **Production Release:** May 2026
