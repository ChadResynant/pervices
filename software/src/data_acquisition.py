#!/usr/bin/env python3
"""
Real-Time Data Acquisition System
Integrates UDP receiver with ring buffer for continuous NMR data acquisition

Author: Resynant, Inc.
Date: November 2025
"""

import threading
import time
from typing import Optional, Callable
import numpy as np

from udp_receiver import PerVicesUDPReceiver
from ring_buffer import MultiChannelRingBuffer


class NMRDataAcquisition:
    """
    Real-time NMR data acquisition system.
    Receives PVAN-11 UDP packets and streams I/Q data to ring buffers.
    """

    def __init__(self,
                 udp_ip: str = '0.0.0.0',
                 udp_port: int = 28888,
                 num_channels: int = 4,
                 buffer_capacity: int = 10_000_000):
        """
        Initialize acquisition system.

        Args:
            udp_ip: UDP bind address (default: 0.0.0.0 for all interfaces)
            udp_port: UDP port number (default: 28888)
            num_channels: Number of Rx channels (default: 4)
            buffer_capacity: Ring buffer capacity per channel in samples (default: 10M)
        """
        self.receiver = PerVicesUDPReceiver(ip=udp_ip, port=udp_port)
        self.ring_buffer = MultiChannelRingBuffer(num_channels=num_channels,
                                                   capacity_per_channel=buffer_capacity)

        self.num_channels = num_channels
        self.running = False
        self.acquisition_thread: Optional[threading.Thread] = None

        # Statistics
        self.packets_received = 0
        self.packets_dropped = 0
        self.last_packet_count = {}  # Track per stream ID
        self.start_time = 0

        # Callbacks
        self.packet_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None

    def start(self) -> None:
        """Start data acquisition in background thread."""
        if self.running:
            print("Acquisition already running")
            return

        self.receiver.start()
        self.running = True
        self.start_time = time.time()

        self.acquisition_thread = threading.Thread(target=self._acquisition_loop, daemon=True)
        self.acquisition_thread.start()

        print(f"Data acquisition started on {self.receiver.ip}:{self.receiver.port}")

    def stop(self) -> None:
        """Stop data acquisition."""
        if not self.running:
            return

        self.running = False

        if self.acquisition_thread:
            self.acquisition_thread.join(timeout=2.0)

        self.receiver.stop()
        print("Data acquisition stopped")

    def _acquisition_loop(self) -> None:
        """Main acquisition loop (runs in background thread)."""
        while self.running:
            try:
                packet = self.receiver.receive_packet()

                if packet is None:
                    continue

                if not packet.get('parsed', False):
                    if self.error_callback:
                        self.error_callback(f"Failed to parse packet: {packet}")
                    continue

                # Extract stream ID (maps to channel)
                stream_id = packet['stream_id']
                channel = self._stream_id_to_channel(stream_id)

                if channel >= self.num_channels:
                    if self.error_callback:
                        self.error_callback(f"Invalid stream ID {stream_id} (channel {channel})")
                    continue

                # Check for packet loss
                self._check_packet_loss(stream_id, packet['packet_count'])

                # Write I/Q data to ring buffer
                i_data = packet['i_data']
                q_data = packet['q_data']

                if len(i_data) > 0:
                    success = self.ring_buffer.write(channel, i_data, q_data)
                    if not success:
                        # Overflow occurred (logged in ring buffer)
                        pass

                self.packets_received += 1

                # Optional callback for packet processing
                if self.packet_callback:
                    self.packet_callback(packet, channel)

            except KeyboardInterrupt:
                break
            except Exception as e:
                if self.error_callback:
                    self.error_callback(f"Acquisition error: {e}")
                else:
                    print(f"ERROR in acquisition loop: {e}")

    def _stream_id_to_channel(self, stream_id: int) -> int:
        """
        Map PVAN-11 stream ID to channel number.

        Args:
            stream_id: Stream ID from packet

        Returns:
            Channel number (0-3)
        """
        # Simple mapping: stream ID 1-4 -> channel 0-3
        # Adjust based on Crimson TNG configuration
        return (stream_id - 1) % self.num_channels

    def _check_packet_loss(self, stream_id: int, packet_count: int) -> None:
        """
        Detect dropped packets by checking packet count sequence.

        Args:
            stream_id: Stream identifier
            packet_count: Current packet count (4-bit counter, wraps at 16)
        """
        if stream_id in self.last_packet_count:
            expected = (self.last_packet_count[stream_id] + 1) % 16
            if packet_count != expected:
                dropped = (packet_count - expected) % 16
                self.packets_dropped += dropped
                if self.error_callback:
                    self.error_callback(
                        f"Dropped {dropped} packet(s) on stream {stream_id} "
                        f"(expected {expected}, got {packet_count})"
                    )

        self.last_packet_count[stream_id] = packet_count

    def get_channel_data(self, channel: int, n_samples: int) -> Optional[np.ndarray]:
        """
        Read complex I/Q data from specified channel.

        Args:
            channel: Channel number (0-3)
            n_samples: Number of samples to read

        Returns:
            Complex array (I + jQ) or None if insufficient data
        """
        i_data, q_data = self.ring_buffer.read(channel, n_samples)

        if i_data is None:
            return None

        # Convert to complex (float32 for signal processing)
        complex_data = i_data.astype(np.float32) + 1j * q_data.astype(np.float32)

        return complex_data

    def peek_channel_data(self, channel: int, n_samples: int) -> Optional[np.ndarray]:
        """
        Peek at complex I/Q data without consuming (non-destructive read).

        Args:
            channel: Channel number (0-3)
            n_samples: Number of samples to peek

        Returns:
            Complex array (I + jQ) or None if insufficient data
        """
        i_data, q_data = self.ring_buffer.peek(channel, n_samples)

        if i_data is None:
            return None

        complex_data = i_data.astype(np.float32) + 1j * q_data.astype(np.float32)
        return complex_data

    def available(self, channel: int) -> int:
        """Get number of samples available on channel."""
        return self.ring_buffer.available(channel)

    def save_channel_data(self, channel: int, filename: str, n_samples: Optional[int] = None) -> int:
        """
        Save channel data to file.

        Args:
            channel: Channel number (0-3)
            filename: Output filename
            n_samples: Number of samples to save (None = all)

        Returns:
            Number of samples saved
        """
        return self.ring_buffer.save_to_file(channel, filename, n_samples)

    def get_statistics(self) -> dict:
        """
        Get acquisition system statistics.

        Returns:
            Dictionary with overall and per-channel statistics
        """
        elapsed = time.time() - self.start_time if self.start_time > 0 else 0

        stats = {
            'running': self.running,
            'elapsed_time': elapsed,
            'packets_received': self.packets_received,
            'packets_dropped': self.packets_dropped,
            'packet_rate': self.packets_received / max(1, elapsed),
            'drop_rate_percent': 100.0 * self.packets_dropped / max(1, self.packets_received),
            'channels': {}
        }

        for ch in range(self.num_channels):
            stats['channels'][ch] = self.ring_buffer.get_statistics(ch)

        return stats

    def clear_buffers(self) -> None:
        """Clear all channel buffers."""
        self.ring_buffer.clear()


# Example usage and testing
if __name__ == '__main__':
    print("NMR Data Acquisition System - Test Mode")
    print("=" * 60)
    print("\nThis test requires live UDP packets from Crimson TNG.")
    print("For offline testing, use simulated packet generator.\n")

    # Create acquisition system
    acq = NMRDataAcquisition(udp_ip='0.0.0.0', udp_port=28888, num_channels=4)

    # Set up callbacks
    def packet_handler(packet, channel):
        """Process each received packet."""
        if acq.packets_received % 100 == 0:
            print(f"Packet {acq.packets_received}: Channel {channel}, "
                  f"{packet['sample_count']} samples, "
                  f"timestamp={packet['timestamp']}")

    def error_handler(message):
        """Handle errors."""
        print(f"ERROR: {message}")

    acq.packet_callback = packet_handler
    acq.error_callback = error_handler

    # Start acquisition
    try:
        acq.start()

        print("Acquisition running... (Press Ctrl+C to stop)")
        print("Waiting for packets from Crimson TNG...\n")

        # Monitor acquisition
        while True:
            time.sleep(5)

            stats = acq.get_statistics()
            print(f"\n--- Statistics (t={stats['elapsed_time']:.1f}s) ---")
            print(f"Packets: {stats['packets_received']} received, "
                  f"{stats['packets_dropped']} dropped "
                  f"({stats['drop_rate_percent']:.3f}% loss)")
            print(f"Rate: {stats['packet_rate']:.1f} packets/sec")

            for ch in range(4):
                ch_stats = stats['channels'][ch]
                print(f"  Ch {ch}: {ch_stats['available']:,} samples available "
                      f"({ch_stats['fill_percentage']:.1f}% full), "
                      f"overflows={ch_stats['overflow_count']}")

    except KeyboardInterrupt:
        print("\n\nStopping acquisition...")
        acq.stop()

        # Final statistics
        final_stats = acq.get_statistics()
        print("\n" + "=" * 60)
        print("FINAL STATISTICS")
        print("=" * 60)
        print(f"Total packets: {final_stats['packets_received']}")
        print(f"Dropped packets: {final_stats['packets_dropped']}")
        print(f"Drop rate: {final_stats['drop_rate_percent']:.4f}%")
        print(f"Runtime: {final_stats['elapsed_time']:.1f} seconds")

        for ch in range(4):
            ch_stats = final_stats['channels'][ch]
            print(f"\nChannel {ch}:")
            print(f"  Samples captured: {ch_stats['total_written']:,}")
            print(f"  Buffer overflows: {ch_stats['overflow_count']}")
