#!/usr/bin/env python3
"""
Test harness for Per Vices UDP Receiver
Generates simulated PVAN-11 packets and validates parsing

Author: Resynant, Inc.
Date: November 2025
"""

import struct
import numpy as np
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from udp_receiver import PerVicesUDPReceiver


class PVAN11PacketGenerator:
    """
    Generate simulated PVAN-11 (VITA 49) packets for testing.
    """

    def __init__(self):
        self.packet_counter = 0
        self.timestamp_counter = 0

    def generate_packet(self, num_samples: int = 256, stream_id: int = 1,
                       with_timestamp: bool = True) -> bytes:
        """
        Generate a simulated PVAN-11 packet.

        Args:
            num_samples: Number of I/Q pairs to include
            stream_id: Stream identifier (channel ID)
            with_timestamp: Include fractional timestamp

        Returns:
            Raw packet bytes in PVAN-11 format
        """
        packet_data = bytearray()

        # Calculate packet size (in 32-bit words)
        # Header (1 word) + Stream ID (1 word) + Timestamp (2 words if present) +
        # I/Q data (num_samples words) + Trailer (1 word)
        header_words = 1 + 1  # Header + Stream ID
        timestamp_words = 2 if with_timestamp else 0
        data_words = num_samples  # Each I/Q pair is 1 word (32 bits)
        trailer_words = 1
        total_words = header_words + timestamp_words + data_words + trailer_words

        # Build VITA 49 header (first 32-bit word)
        packet_type = 0x1      # Signal data with Stream ID
        c_bit = 0              # No class identifier
        indicators = 0x5       # Trailer present (bit 2), packet type flags
        tsi = 0x0              # No integer-seconds timestamp
        tsf = 0x3 if with_timestamp else 0x0  # Free-running count or none
        packet_count = self.packet_counter & 0xF  # 4-bit counter
        packet_size = total_words & 0xFFFF  # 16-bit size in words

        header_word = (
            (packet_type << 28) |
            (c_bit << 27) |
            (indicators << 24) |
            (tsi << 22) |
            (tsf << 20) |
            (packet_count << 16) |
            packet_size
        )

        packet_data.extend(struct.pack('>I', header_word))

        # Add Stream Identifier
        packet_data.extend(struct.pack('>I', stream_id))

        # Add Fractional Timestamp if requested
        if with_timestamp:
            packet_data.extend(struct.pack('>Q', self.timestamp_counter))
            self.timestamp_counter += num_samples

        # Generate I/Q data (simulated NMR signal)
        # Create a simple sinusoid for testing
        frequency = 0.05  # Normalized frequency
        amplitude = 10000  # Within int16 range

        for n in range(num_samples):
            phase = 2 * np.pi * frequency * n
            i_val = int(amplitude * np.cos(phase))
            q_val = int(amplitude * np.sin(phase))

            # Clamp to int16 range
            i_val = max(-32768, min(32767, i_val))
            q_val = max(-32768, min(32767, q_val))

            # Pack as big-endian 16-bit signed integers
            packet_data.extend(struct.pack('>hh', i_val, q_val))

        # Add Trailer (all zeros)
        packet_data.extend(struct.pack('>I', 0x00000000))

        self.packet_counter += 1

        return bytes(packet_data)


def test_packet_parsing():
    """
    Test PVAN-11 packet parsing with simulated data.
    """
    print("PVAN-11 Packet Parsing Test")
    print("=" * 60)

    # Create packet generator and receiver
    generator = PVAN11PacketGenerator()
    receiver = PerVicesUDPReceiver()

    # Test 1: Basic packet with timestamp
    print("\nTest 1: Basic packet (256 samples, stream ID = 1, with timestamp)")
    print("-" * 60)

    packet1 = generator.generate_packet(num_samples=256, stream_id=1, with_timestamp=True)
    print(f"Generated packet size: {len(packet1)} bytes")

    parsed1 = receiver.parse_pvan11_packet(packet1)

    print(f"Parsed successfully: {parsed1['parsed']}")
    print(f"Packet type: {parsed1['packet_type']}")
    print(f"Packet count: {parsed1['packet_count']}")
    print(f"Stream ID: {parsed1['stream_id']}")
    print(f"Timestamp: {parsed1['timestamp']}")
    print(f"Sample count: {parsed1['sample_count']}")
    print(f"I data range: [{parsed1['i_data'].min()}, {parsed1['i_data'].max()}]")
    print(f"Q data range: [{parsed1['q_data'].min()}, {parsed1['q_data'].max()}]")

    # Verify sample count
    assert parsed1['sample_count'] == 256, "Sample count mismatch!"
    print("✓ Sample count verified")

    # Test 2: Multiple packets (simulate multi-channel)
    print("\n\nTest 2: Multi-channel simulation (4 channels, 128 samples each)")
    print("-" * 60)

    for channel in range(1, 5):
        packet = generator.generate_packet(num_samples=128, stream_id=channel, with_timestamp=True)
        parsed = receiver.parse_pvan11_packet(packet)

        print(f"Channel {channel}: "
              f"Stream ID={parsed['stream_id']}, "
              f"Samples={parsed['sample_count']}, "
              f"Timestamp={parsed['timestamp']}")

        assert parsed['stream_id'] == channel, f"Stream ID mismatch for channel {channel}"

    print("✓ Multi-channel test passed")

    # Test 3: Packet without timestamp
    print("\n\nTest 3: Packet without timestamp")
    print("-" * 60)

    packet3 = generator.generate_packet(num_samples=512, stream_id=2, with_timestamp=False)
    parsed3 = receiver.parse_pvan11_packet(packet3)

    print(f"Sample count: {parsed3['sample_count']}")
    print(f"Timestamp: {parsed3['timestamp']} (should be 0)")

    assert parsed3['sample_count'] == 512, "Sample count mismatch!"
    assert parsed3['timestamp'] == 0, "Timestamp should be 0 when not present"
    print("✓ No-timestamp test passed")

    # Test 4: I/Q data integrity
    print("\n\nTest 4: I/Q data integrity check")
    print("-" * 60)

    packet4 = generator.generate_packet(num_samples=100, stream_id=1, with_timestamp=True)
    parsed4 = receiver.parse_pvan11_packet(packet4)

    # Convert to complex
    complex_signal = parsed4['i_data'].astype(np.float32) + 1j * parsed4['q_data'].astype(np.float32)

    # Check magnitude
    magnitude = np.abs(complex_signal)
    print(f"Signal magnitude: mean={magnitude.mean():.1f}, std={magnitude.std():.1f}")
    print(f"Expected magnitude: ~10000 (from generator)")

    # Verify magnitude is approximately correct
    assert 9000 < magnitude.mean() < 11000, "Signal magnitude out of expected range!"
    print("✓ I/Q data integrity verified")

    # Test 5: Packet count sequence
    print("\n\nTest 5: Packet count sequence")
    print("-" * 60)

    for i in range(20):
        packet = generator.generate_packet(num_samples=64, stream_id=1, with_timestamp=True)
        parsed = receiver.parse_pvan11_packet(packet)
        print(f"Packet {i+1}: count={parsed['packet_count']}", end="  ")
        if (i+1) % 5 == 0:
            print()  # New line every 5 packets

    print("\n✓ Packet sequence test complete")

    # Summary
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print("\nPVAN-11 packet parser is working correctly!")
    print("Ready for integration with UDP receiver.")


if __name__ == '__main__':
    test_packet_parsing()
