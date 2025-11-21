#!/usr/bin/env python3
"""
UDP Receiver for Per Vices Crimson TNG
Implements PVAN-11 packet format parsing for NMR data acquisition

Author: Resynant, Inc.
Date: November 2025
"""

import socket
import struct
import numpy as np
from typing import Dict, Optional, Tuple


class PerVicesUDPReceiver:
    """
    UDP receiver for Per Vices Crimson TNG SDR platform.
    Receives and parses PVAN-11 format packets containing I/Q data.
    """

    def __init__(self, ip: str = '0.0.0.0', port: int = 28888):
        """
        Initialize UDP receiver.

        Args:
            ip: IP address to bind to (default: 0.0.0.0 for all interfaces)
            port: UDP port number (default: 28888)
        """
        self.ip = ip
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.packet_count = 0
        self.bytes_received = 0

    def start(self) -> None:
        """Initialize and bind UDP socket."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        print(f"UDP receiver listening on {self.ip}:{self.port}")

    def receive_packet(self) -> Optional[Dict]:
        """
        Receive single UDP packet from socket.

        Returns:
            Parsed packet dictionary, or None if error
        """
        if not self.socket:
            raise RuntimeError("Socket not initialized. Call start() first.")

        try:
            # Receive UDP packet (max size 65536 bytes for UDP)
            data, addr = self.socket.recvfrom(65536)
            self.packet_count += 1
            self.bytes_received += len(data)

            # Parse PVAN-11 packet
            return self.parse_pvan11_packet(data)

        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def parse_pvan11_packet(self, data: bytes) -> Dict:
        """
        Parse PVAN-11 packet format (VITA 49 implementation).

        PVAN-11 Format (VITA 49 standard):
        - Header: 32-bit words with packet type, count, size, stream ID, timestamp
        - Payload: I/Q samples (32 bits per pair: 16-bit I + 16-bit Q, big-endian)
        - Trailer: Present in Rx packets (all zeros)

        Reference: https://support.pervices.com/application-notes/pvan-11-dataformat-spec/

        Args:
            data: Raw UDP packet bytes

        Returns:
            Dictionary containing parsed packet data
        """
        if len(data) < 4:
            return {'error': 'Packet too short', 'raw_size': len(data)}

        # Parse VITA 49 header (first 32-bit word)
        header_word = struct.unpack('>I', data[0:4])[0]

        # Extract header fields (VITA 49 format)
        packet_type = (header_word >> 28) & 0xF  # Bits 31:28
        c_bit = (header_word >> 27) & 0x1        # Bit 27
        indicators = (header_word >> 24) & 0x7   # Bits 26:24
        tsi = (header_word >> 22) & 0x3          # Bits 23:22
        tsf = (header_word >> 20) & 0x3          # Bits 21:20
        packet_count = (header_word >> 16) & 0xF # Bits 19:16
        packet_size = header_word & 0xFFFF       # Bits 15:0 (size in 32-bit words)

        # Track current position in packet
        pos = 4  # Start after first header word

        # Parse Stream Identifier if present (packet_type == 0001)
        stream_id = 0
        if packet_type == 0x1:
            stream_id = struct.unpack('>I', data[pos:pos+4])[0]
            pos += 4

        # Parse Fractional Timestamp if present (TSF != 00)
        timestamp = 0
        if tsf == 0x3:  # Free-running count
            timestamp = struct.unpack('>Q', data[pos:pos+8])[0]
            pos += 8

        # Extract I/Q data payload
        # Trailer is present (1 word = 4 bytes at end), subtract from payload
        trailer_size = 4 if (indicators & 0x4) else 0  # Check trailer bit
        payload_end = len(data) - trailer_size

        i_samples, q_samples = self.extract_iq_samples(data[pos:payload_end])

        packet_info = {
            'raw_size': len(data),
            'packet_type': packet_type,
            'packet_count': packet_count,
            'packet_size_words': packet_size,
            'stream_id': stream_id,
            'timestamp': timestamp,
            'i_data': i_samples,
            'q_data': q_samples,
            'sample_count': len(i_samples),
            'parsed': True
        }

        return packet_info

    def parse_header(self, data: bytes) -> Tuple[int, int, int, int]:
        """
        Parse PVAN-11 packet header.

        Args:
            data: Raw packet bytes

        Returns:
            Tuple of (packet_id, channel_id, timestamp, sample_count)
        """
        # TODO: Implement based on PVAN-11 spec
        # This is a placeholder structure
        header_size = 32  # Estimate - verify with spec

        # Example unpacking (adjust based on actual spec)
        # header = struct.unpack('!IIIIIIII', data[:header_size])

        return (0, 0, 0, 0)  # Placeholder

    def extract_iq_samples(self, payload: bytes) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract I/Q samples from packet payload.

        PVAN-11 I/Q Format (32 bits per sample pair):
        - Bits 31:16 = I component (16-bit signed, big-endian)
        - Bits 15:0  = Q component (16-bit signed, big-endian)

        Each I/Q pair = 4 bytes total

        Args:
            payload: Raw I/Q data bytes (after header, before trailer)

        Returns:
            Tuple of (i_samples, q_samples) as numpy int16 arrays
        """
        if len(payload) == 0:
            return np.array([], dtype=np.int16), np.array([], dtype=np.int16)

        # Number of I/Q pairs (each pair is 4 bytes)
        num_pairs = len(payload) // 4

        # Preallocate arrays
        i_samples = np.zeros(num_pairs, dtype=np.int16)
        q_samples = np.zeros(num_pairs, dtype=np.int16)

        # Unpack I/Q pairs (big-endian format)
        for idx in range(num_pairs):
            offset = idx * 4
            iq_pair = payload[offset:offset+4]

            # Unpack as big-endian: two signed 16-bit integers
            i_val, q_val = struct.unpack('>hh', iq_pair)

            i_samples[idx] = i_val
            q_samples[idx] = q_val

        return i_samples, q_samples

    def get_statistics(self) -> Dict:
        """
        Get receiver statistics.

        Returns:
            Dictionary with packet count, bytes received, etc.
        """
        return {
            'packet_count': self.packet_count,
            'bytes_received': self.bytes_received,
            'avg_packet_size': self.bytes_received / max(1, self.packet_count)
        }

    def stop(self) -> None:
        """Close UDP socket and cleanup."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print(f"\nReceiver stopped. Statistics:")
            stats = self.get_statistics()
            for key, value in stats.items():
                print(f"  {key}: {value}")


# Test harness and example usage
if __name__ == '__main__':
    print("Per Vices Crimson TNG UDP Receiver")
    print("=" * 50)

    # Create receiver instance
    receiver = PerVicesUDPReceiver(ip='0.0.0.0', port=28888)

    try:
        receiver.start()
        print("Waiting for packets... (Ctrl+C to stop)\n")

        while True:
            packet = receiver.receive_packet()

            if packet and packet['raw_size'] > 0:
                print(f"Packet {packet['packet_id']}: "
                      f"{packet['raw_size']} bytes, "
                      f"Channel {packet['channel']}, "
                      f"Samples: {packet['sample_count']}")

                # Display every 100th packet to avoid spam
                if packet['packet_id'] % 100 == 0:
                    stats = receiver.get_statistics()
                    print(f"  -> Total: {stats['packet_count']} packets, "
                          f"{stats['bytes_received']/1e6:.2f} MB received")

    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")

    finally:
        receiver.stop()
