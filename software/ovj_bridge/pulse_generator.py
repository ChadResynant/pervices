#!/usr/bin/env python3
"""
Pulse Waveform Generator for Crimson TNG
Generates I/Q waveforms from PSG pulse specifications

Author: Resynant, Inc.
Date: November 2025
"""

import numpy as np
from typing import Tuple


class PulseGenerator:
    """
    Generate I/Q waveforms for NMR pulses.

    Converts PSG pulse descriptions (duration, phase, power) into
    I/Q sample arrays suitable for upload to Crimson TNG DAC.
    """

    def __init__(self, sample_rate: float = 325e6):
        """
        Initialize pulse generator.

        Args:
            sample_rate: DAC sample rate in Hz (default: 325 MHz for Crimson TNG)
        """
        self.sample_rate = sample_rate

    def rectangular_pulse(self,
                         duration: float,
                         phase: float = 0.0,
                         amplitude: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate rectangular RF pulse.

        Args:
            duration: Pulse duration in seconds
            phase: RF phase in degrees (0, 90, 180, 270)
            amplitude: Pulse amplitude (0-1, where 1 = full scale)

        Returns:
            Tuple of (i_samples, q_samples) as int16 arrays
        """
        # Calculate number of samples
        n_samples = int(duration * self.sample_rate)

        # Generate constant amplitude with specified phase
        phase_rad = np.deg2rad(phase)

        # I/Q components (normalized to -1 to +1)
        i_normalized = amplitude * np.cos(phase_rad) * np.ones(n_samples)
        q_normalized = amplitude * np.sin(phase_rad) * np.ones(n_samples)

        # Scale to int16 range (-32767 to +32767, leaving headroom)
        max_amplitude = 30000
        i_samples = (i_normalized * max_amplitude).astype(np.int16)
        q_samples = (q_normalized * max_amplitude).astype(np.int16)

        return i_samples, q_samples

    def cp_ramp(self,
                duration: float,
                start_amplitude: float = 0.5,
                end_amplitude: float = 1.0,
                phase: float = 0.0,
                ramp_type: str = 'linear') -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate cross-polarization ramp waveform.

        Args:
            duration: Ramp duration in seconds
            start_amplitude: Starting amplitude (0-1)
            end_amplitude: Ending amplitude (0-1)
            phase: RF phase in degrees
            ramp_type: 'linear' or 'tangent'

        Returns:
            Tuple of (i_samples, q_samples) as int16 arrays
        """
        n_samples = int(duration * self.sample_rate)
        phase_rad = np.deg2rad(phase)

        # Generate amplitude ramp
        if ramp_type == 'linear':
            amplitude_ramp = np.linspace(start_amplitude, end_amplitude, n_samples)

        elif ramp_type == 'tangent':
            # Tangent ramp (better Hartmann-Hahn matching)
            # tan(x) from -π/4 to +π/4, scaled and shifted
            x = np.linspace(-np.pi/4, np.pi/4, n_samples)
            tan_ramp = np.tan(x)
            # Normalize to 0-1
            tan_norm = (tan_ramp - tan_ramp.min()) / (tan_ramp.max() - tan_ramp.min())
            # Scale to start-end amplitude
            amplitude_ramp = start_amplitude + (end_amplitude - start_amplitude) * tan_norm

        else:
            raise ValueError(f"Unknown ramp type: {ramp_type}")

        # Apply phase
        i_normalized = amplitude_ramp * np.cos(phase_rad)
        q_normalized = amplitude_ramp * np.sin(phase_rad)

        # Scale to int16
        max_amplitude = 30000
        i_samples = (i_normalized * max_amplitude).astype(np.int16)
        q_samples = (q_normalized * max_amplitude).astype(np.int16)

        return i_samples, q_samples

    def tppm_sequence(self,
                     duration: float,
                     pulse_width: float = 5e-6,
                     phase_angle: float = 15.0,
                     amplitude: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate TPPM (Two-Pulse Phase Modulation) decoupling sequence.

        TPPM is a standard decoupling method in solid-state NMR.
        Sequence: [+φ pulse] [−φ pulse] [+φ pulse] [−φ pulse] ...

        Args:
            duration: Total sequence duration in seconds
            pulse_width: Individual pulse width in seconds (typically 5-10 μs)
            phase_angle: Phase modulation angle in degrees (typically 10-20°)
            amplitude: Pulse amplitude (0-1)

        Returns:
            Tuple of (i_samples, q_samples) as int16 arrays
        """
        # Calculate number of pulse pairs
        pulse_pair_duration = 2 * pulse_width
        n_pairs = int(duration / pulse_pair_duration)

        # Samples per pulse
        samples_per_pulse = int(pulse_width * self.sample_rate)

        # Total samples
        total_samples = n_pairs * 2 * samples_per_pulse

        # Preallocate arrays
        i_samples = np.zeros(total_samples, dtype=np.int16)
        q_samples = np.zeros(total_samples, dtype=np.int16)

        # Generate TPPM pattern: +φ, −φ, +φ, −φ, ...
        max_amplitude = 30000 * amplitude

        for pair_idx in range(n_pairs):
            start_idx = pair_idx * 2 * samples_per_pulse

            # +φ pulse
            phase_rad_plus = np.deg2rad(phase_angle)
            i_samples[start_idx:start_idx + samples_per_pulse] = \
                int(max_amplitude * np.cos(phase_rad_plus))
            q_samples[start_idx:start_idx + samples_per_pulse] = \
                int(max_amplitude * np.sin(phase_rad_plus))

            # −φ pulse
            phase_rad_minus = np.deg2rad(-phase_angle)
            i_samples[start_idx + samples_per_pulse:start_idx + 2*samples_per_pulse] = \
                int(max_amplitude * np.cos(phase_rad_minus))
            q_samples[start_idx + samples_per_pulse:start_idx + 2*samples_per_pulse] = \
                int(max_amplitude * np.sin(phase_rad_minus))

        return i_samples, q_samples

    def shaped_pulse(self,
                    duration: float,
                    shape: str = 'gaussian',
                    phase: float = 0.0,
                    amplitude: float = 1.0,
                    truncation: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate shaped RF pulse.

        Args:
            duration: Pulse duration in seconds
            shape: Pulse shape ('gaussian', 'sinc', 'hermite')
            phase: RF phase in degrees
            amplitude: Peak amplitude (0-1)
            truncation: Gaussian truncation level (number of σ)

        Returns:
            Tuple of (i_samples, q_samples) as int16 arrays
        """
        n_samples = int(duration * self.sample_rate)
        phase_rad = np.deg2rad(phase)

        # Time axis centered at zero
        t = np.linspace(-duration/2, duration/2, n_samples)

        # Generate amplitude envelope
        if shape == 'gaussian':
            # Gaussian: exp(-t²/2σ²)
            sigma = duration / (2 * truncation)
            envelope = np.exp(-t**2 / (2 * sigma**2))

        elif shape == 'sinc':
            # Sinc: sin(πt/τ) / (πt/τ)
            x = np.pi * t / (duration/2)
            x[n_samples//2] = 1e-10  # Avoid division by zero at center
            envelope = np.sin(x) / x
            envelope[n_samples//2] = 1.0  # Sinc(0) = 1

        elif shape == 'hermite':
            # Hermite: (1 - t²/σ²) * exp(-t²/2σ²)
            sigma = duration / (2 * truncation)
            envelope = (1 - t**2/sigma**2) * np.exp(-t**2 / (2*sigma**2))

        else:
            raise ValueError(f"Unknown pulse shape: {shape}")

        # Normalize to peak = 1
        envelope = envelope / envelope.max()

        # Apply amplitude and phase
        i_normalized = amplitude * envelope * np.cos(phase_rad)
        q_normalized = amplitude * envelope * np.sin(phase_rad)

        # Scale to int16
        max_amplitude = 30000
        i_samples = (i_normalized * max_amplitude).astype(np.int16)
        q_samples = (q_normalized * max_amplitude).astype(np.int16)

        return i_samples, q_samples

    def delay(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate zero-amplitude delay (silence).

        Args:
            duration: Delay duration in seconds

        Returns:
            Tuple of (i_samples, q_samples) as int16 arrays (all zeros)
        """
        n_samples = int(duration * self.sample_rate)
        i_samples = np.zeros(n_samples, dtype=np.int16)
        q_samples = np.zeros(n_samples, dtype=np.int16)

        return i_samples, q_samples


# Test harness
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    print("Pulse Waveform Generator Test")
    print("=" * 60)

    generator = PulseGenerator(sample_rate=325e6)

    # Test 1: Rectangular pulse
    print("\n1. Rectangular Pulse (90° flip, 10 μs)")
    i_rect, q_rect = generator.rectangular_pulse(
        duration=10e-6,
        phase=90.0,  # +Y axis (90°)
        amplitude=1.0
    )
    print(f"   Generated {len(i_rect)} samples")
    print(f"   I range: [{i_rect.min()}, {i_rect.max()}]")
    print(f"   Q range: [{q_rect.min()}, {q_rect.max()}]")

    # Test 2: CP ramp
    print("\n2. Cross-Polarization Ramp (linear, 1 ms)")
    i_cp, q_cp = generator.cp_ramp(
        duration=1e-3,
        start_amplitude=0.5,
        end_amplitude=1.0,
        phase=0.0,
        ramp_type='linear'
    )
    print(f"   Generated {len(i_cp)} samples")
    print(f"   I range: [{i_cp.min()}, {i_cp.max()}]")

    # Test 3: TPPM decoupling
    print("\n3. TPPM Decoupling (15°, 5 μs pulse width)")
    i_tppm, q_tppm = generator.tppm_sequence(
        duration=100e-6,  # 100 μs
        pulse_width=5e-6,
        phase_angle=15.0,
        amplitude=0.8
    )
    print(f"   Generated {len(i_tppm)} samples")
    print(f"   Number of pulse pairs: {len(i_tppm) // (2 * int(5e-6 * 325e6))}")

    # Test 4: Gaussian shaped pulse
    print("\n4. Gaussian Shaped Pulse (500 μs)")
    i_gauss, q_gauss = generator.shaped_pulse(
        duration=500e-6,
        shape='gaussian',
        phase=0.0,
        amplitude=1.0
    )
    print(f"   Generated {len(i_gauss)} samples")
    print(f"   I range: [{i_gauss.min()}, {i_gauss.max()}]")

    print("\n" + "=" * 60)
    print("All waveforms generated successfully ✓")

    # Optional: Plot waveforms if matplotlib available
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # Plot rectangular pulse
        axes[0, 0].plot(i_rect[:1000], label='I')
        axes[0, 0].plot(q_rect[:1000], label='Q')
        axes[0, 0].set_title('Rectangular Pulse (90°)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Plot CP ramp (downsample for visibility)
        axes[0, 1].plot(i_cp[::1000], label='I')
        axes[0, 1].plot(q_cp[::1000], label='Q')
        axes[0, 1].set_title('CP Linear Ramp')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Plot TPPM (first few pulses)
        axes[1, 0].plot(i_tppm[:5000], label='I')
        axes[1, 0].plot(q_tppm[:5000], label='Q')
        axes[1, 0].set_title('TPPM Decoupling')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        # Plot Gaussian shaped pulse (downsample)
        axes[1, 1].plot(i_gauss[::100], label='I')
        axes[1, 1].plot(q_gauss[::100], label='Q')
        axes[1, 1].set_title('Gaussian Shaped Pulse')
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        plt.tight_layout()
        plt.savefig('/tmp/pulse_waveforms.png')
        print("\nWaveform plots saved to /tmp/pulse_waveforms.png")

    except ImportError:
        print("\nMatplotlib not available - skipping plots")
