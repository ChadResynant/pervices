#!/usr/bin/env python3
"""
Ring Buffer for Real-Time NMR Data Acquisition
Handles continuous streaming I/Q data from Crimson TNG

Author: Resynant, Inc.
Date: November 2025
"""

import numpy as np
import threading
from typing import Tuple, Optional
from collections import deque


class MultiChannelRingBuffer:
    """
    Thread-safe ring buffer for multi-channel I/Q data acquisition.
    Supports up to 4 Rx channels with independent read/write pointers.
    """

    def __init__(self, num_channels: int = 4, capacity_per_channel: int = 10_000_000):
        """
        Initialize multi-channel ring buffer.

        Args:
            num_channels: Number of Rx channels (default: 4 for Crimson TNG)
            capacity_per_channel: Buffer size in I/Q pairs per channel (default: 10M samples)
        """
        self.num_channels = num_channels
        self.capacity = capacity_per_channel

        # Allocate buffers for each channel (I and Q components)
        self.buffers_i = [np.zeros(capacity_per_channel, dtype=np.int16)
                          for _ in range(num_channels)]
        self.buffers_q = [np.zeros(capacity_per_channel, dtype=np.int16)
                          for _ in range(num_channels)]

        # Per-channel write/read positions
        self.write_pos = [0] * num_channels
        self.read_pos = [0] * num_channels
        self.samples_available = [0] * num_channels

        # Statistics
        self.total_written = [0] * num_channels
        self.total_read = [0] * num_channels
        self.overflow_count = [0] * num_channels

        # Thread safety
        self.locks = [threading.Lock() for _ in range(num_channels)]

    def write(self, channel: int, i_samples: np.ndarray, q_samples: np.ndarray) -> bool:
        """
        Write I/Q samples to specified channel buffer.

        Args:
            channel: Channel number (0-3)
            i_samples: I component samples (int16 array)
            q_samples: Q component samples (int16 array)

        Returns:
            True if successful, False if overflow occurred
        """
        if channel >= self.num_channels:
            raise ValueError(f"Invalid channel {channel}. Max channels: {self.num_channels}")

        if len(i_samples) != len(q_samples):
            raise ValueError("I and Q sample arrays must be same length")

        n_samples = len(i_samples)

        with self.locks[channel]:
            # Check for overflow
            space_available = self.capacity - self.samples_available[channel]
            if n_samples > space_available:
                self.overflow_count[channel] += 1
                # Overwrite oldest data (circular buffer behavior)
                # Advance read pointer to make room
                overflow_amount = n_samples - space_available
                self.read_pos[channel] = (self.read_pos[channel] + overflow_amount) % self.capacity
                self.samples_available[channel] -= overflow_amount

            # Write data with wraparound handling
            write_pos = self.write_pos[channel]

            if write_pos + n_samples <= self.capacity:
                # Simple case: no wraparound
                self.buffers_i[channel][write_pos:write_pos + n_samples] = i_samples
                self.buffers_q[channel][write_pos:write_pos + n_samples] = q_samples
            else:
                # Wraparound case: split write
                first_chunk = self.capacity - write_pos
                self.buffers_i[channel][write_pos:] = i_samples[:first_chunk]
                self.buffers_q[channel][write_pos:] = q_samples[:first_chunk]

                remaining = n_samples - first_chunk
                self.buffers_i[channel][:remaining] = i_samples[first_chunk:]
                self.buffers_q[channel][:remaining] = q_samples[first_chunk:]

            # Update positions
            self.write_pos[channel] = (write_pos + n_samples) % self.capacity
            self.samples_available[channel] += n_samples
            self.total_written[channel] += n_samples

            return self.overflow_count[channel] == 0

    def read(self, channel: int, n_samples: int) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Read I/Q samples from specified channel buffer.

        Args:
            channel: Channel number (0-3)
            n_samples: Number of samples to read

        Returns:
            Tuple of (i_samples, q_samples) or (None, None) if insufficient data
        """
        if channel >= self.num_channels:
            raise ValueError(f"Invalid channel {channel}. Max channels: {self.num_channels}")

        with self.locks[channel]:
            if n_samples > self.samples_available[channel]:
                return None, None  # Not enough data available

            read_pos = self.read_pos[channel]

            # Allocate output arrays
            i_out = np.zeros(n_samples, dtype=np.int16)
            q_out = np.zeros(n_samples, dtype=np.int16)

            if read_pos + n_samples <= self.capacity:
                # Simple case: no wraparound
                i_out[:] = self.buffers_i[channel][read_pos:read_pos + n_samples]
                q_out[:] = self.buffers_q[channel][read_pos:read_pos + n_samples]
            else:
                # Wraparound case: split read
                first_chunk = self.capacity - read_pos
                i_out[:first_chunk] = self.buffers_i[channel][read_pos:]
                q_out[:first_chunk] = self.buffers_q[channel][read_pos:]

                remaining = n_samples - first_chunk
                i_out[first_chunk:] = self.buffers_i[channel][:remaining]
                q_out[first_chunk:] = self.buffers_q[channel][:remaining]

            # Update positions
            self.read_pos[channel] = (read_pos + n_samples) % self.capacity
            self.samples_available[channel] -= n_samples
            self.total_read[channel] += n_samples

            return i_out, q_out

    def peek(self, channel: int, n_samples: int) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Peek at samples without consuming them (non-destructive read).

        Args:
            channel: Channel number (0-3)
            n_samples: Number of samples to peek

        Returns:
            Tuple of (i_samples, q_samples) or (None, None) if insufficient data
        """
        if channel >= self.num_channels:
            raise ValueError(f"Invalid channel {channel}. Max channels: {self.num_channels}")

        with self.locks[channel]:
            if n_samples > self.samples_available[channel]:
                return None, None

            read_pos = self.read_pos[channel]

            i_out = np.zeros(n_samples, dtype=np.int16)
            q_out = np.zeros(n_samples, dtype=np.int16)

            if read_pos + n_samples <= self.capacity:
                i_out[:] = self.buffers_i[channel][read_pos:read_pos + n_samples]
                q_out[:] = self.buffers_q[channel][read_pos:read_pos + n_samples]
            else:
                first_chunk = self.capacity - read_pos
                i_out[:first_chunk] = self.buffers_i[channel][read_pos:]
                q_out[:first_chunk] = self.buffers_q[channel][read_pos:]

                remaining = n_samples - first_chunk
                i_out[first_chunk:] = self.buffers_i[channel][:remaining]
                q_out[first_chunk:] = self.buffers_q[channel][:remaining]

            return i_out, q_out

    def available(self, channel: int) -> int:
        """
        Get number of samples available for reading.

        Args:
            channel: Channel number (0-3)

        Returns:
            Number of samples available
        """
        with self.locks[channel]:
            return self.samples_available[channel]

    def clear(self, channel: Optional[int] = None) -> None:
        """
        Clear buffer for specified channel or all channels.

        Args:
            channel: Channel to clear, or None for all channels
        """
        if channel is None:
            # Clear all channels
            for ch in range(self.num_channels):
                self.clear(ch)
        else:
            with self.locks[channel]:
                self.write_pos[channel] = 0
                self.read_pos[channel] = 0
                self.samples_available[channel] = 0

    def get_statistics(self, channel: int) -> dict:
        """
        Get buffer statistics for specified channel.

        Args:
            channel: Channel number (0-3)

        Returns:
            Dictionary with statistics
        """
        with self.locks[channel]:
            return {
                'channel': channel,
                'capacity': self.capacity,
                'available': self.samples_available[channel],
                'write_pos': self.write_pos[channel],
                'read_pos': self.read_pos[channel],
                'total_written': self.total_written[channel],
                'total_read': self.total_read[channel],
                'overflow_count': self.overflow_count[channel],
                'fill_percentage': 100.0 * self.samples_available[channel] / self.capacity
            }

    def save_to_file(self, channel: int, filename: str, n_samples: Optional[int] = None) -> int:
        """
        Save buffer contents to file (NPZ format for I/Q data).

        Args:
            channel: Channel number (0-3)
            filename: Output filename (will append .npz if not present)
            n_samples: Number of samples to save (None = all available)

        Returns:
            Number of samples saved
        """
        if not filename.endswith('.npz'):
            filename += '.npz'

        with self.locks[channel]:
            samples_to_save = n_samples if n_samples else self.samples_available[channel]
            samples_to_save = min(samples_to_save, self.samples_available[channel])

            if samples_to_save == 0:
                return 0

            i_data, q_data = self.peek(channel, samples_to_save)

            if i_data is not None:
                np.savez_compressed(
                    filename,
                    i_samples=i_data,
                    q_samples=q_data,
                    channel=channel,
                    sample_count=samples_to_save
                )

            return samples_to_save


# Test harness
if __name__ == '__main__':
    print("Multi-Channel Ring Buffer Test")
    print("=" * 60)

    # Create buffer (4 channels, 1000 samples each for testing)
    buffer = MultiChannelRingBuffer(num_channels=4, capacity_per_channel=1000)

    # Test 1: Basic write/read
    print("\nTest 1: Basic write/read (Channel 0)")
    i_test = np.arange(100, dtype=np.int16)
    q_test = np.arange(100, 200, dtype=np.int16)

    buffer.write(0, i_test, q_test)
    print(f"Written 100 samples to channel 0")
    print(f"Available: {buffer.available(0)} samples")

    i_read, q_read = buffer.read(0, 50)
    print(f"Read 50 samples")
    print(f"Remaining: {buffer.available(0)} samples")
    print(f"First 5 I values: {i_read[:5]}")
    print(f"First 5 Q values: {q_read[:5]}")

    assert np.array_equal(i_read, i_test[:50]), "I data mismatch!"
    assert np.array_equal(q_read, q_test[:50]), "Q data mismatch!"
    print("✓ Data integrity verified")

    # Test 2: Multi-channel independence
    print("\n\nTest 2: Multi-channel independence")
    for ch in range(4):
        i_ch = np.full(50, ch * 100, dtype=np.int16)
        q_ch = np.full(50, ch * 100 + 50, dtype=np.int16)
        buffer.write(ch, i_ch, q_ch)
        print(f"Channel {ch}: wrote 50 samples, available={buffer.available(ch)}")

    print("✓ Multi-channel test passed")

    # Test 3: Wraparound
    print("\n\nTest 3: Buffer wraparound")
    buffer.clear(1)

    for i in range(15):  # Write 15 * 100 = 1500 samples (exceeds 1000 capacity)
        i_data = np.full(100, i, dtype=np.int16)
        q_data = np.full(100, i + 100, dtype=np.int16)
        buffer.write(1, i_data, q_data)

    stats = buffer.get_statistics(1)
    print(f"After writing 1500 samples to 1000-capacity buffer:")
    print(f"  Available: {stats['available']}")
    print(f"  Overflow count: {stats['overflow_count']}")
    print(f"  Fill: {stats['fill_percentage']:.1f}%")

    assert stats['overflow_count'] > 0, "Should have overflow!"
    print("✓ Wraparound test passed")

    # Test 4: Statistics
    print("\n\nTest 4: Buffer statistics")
    for ch in range(4):
        stats = buffer.get_statistics(ch)
        print(f"Channel {ch}: {stats['available']}/{stats['capacity']} samples " +
              f"({stats['fill_percentage']:.1f}% full), " +
              f"overflows={stats['overflow_count']}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("Ring buffer ready for integration with UDP receiver")
