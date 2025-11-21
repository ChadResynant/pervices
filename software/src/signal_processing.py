#!/usr/bin/env python3
"""
NMR Signal Processing Pipeline
FIR filtering, decimation, FFT, and spectral analysis

Author: Resynant, Inc.
Date: November 2025
"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional


class NMRSignalProcessor:
    """
    Signal processing pipeline for NMR data (FID to spectrum).
    Handles decimation, filtering, FFT, and apodization.
    """

    def __init__(self, sample_rate: float = 325e6):
        """
        Initialize signal processor.

        Args:
            sample_rate: ADC sample rate in Hz (default: 325 MHz for Crimson TNG)
        """
        self.sample_rate = sample_rate
        self.decimation_filters = {}  # Cache FIR filter coefficients

    def decimate(self,
                 iq_data: np.ndarray,
                 decimation_factor: int,
                 filter_order: int = 64) -> np.ndarray:
        """
        Decimate I/Q data with anti-aliasing FIR filter.

        Args:
            iq_data: Complex I/Q data (I + jQ)
            decimation_factor: Decimation factor (e.g., 32 for 325 MHz → 10 MHz)
            filter_order: FIR filter order (taps)

        Returns:
            Decimated complex data
        """
        # Cache filter coefficients for reuse
        cache_key = (decimation_factor, filter_order)

        if cache_key not in self.decimation_filters:
            # Design low-pass FIR filter (Hamming window)
            # Cutoff at Nyquist frequency of decimated signal
            cutoff = 1.0 / decimation_factor
            self.decimation_filters[cache_key] = signal.firwin(filter_order, cutoff)

        fir_coeffs = self.decimation_filters[cache_key]

        # Apply filter to I and Q separately
        i_filtered = signal.lfilter(fir_coeffs, 1.0, iq_data.real)
        q_filtered = signal.lfilter(fir_coeffs, 1.0, iq_data.imag)

        # Decimate (downsample)
        i_decimated = i_filtered[::decimation_factor]
        q_decimated = q_filtered[::decimation_factor]

        return i_decimated + 1j * q_decimated

    def fft_spectrum(self,
                     fid_data: np.ndarray,
                     zero_fill_factor: int = 2,
                     line_broadening: float = 50.0,
                     phase_correction: Tuple[float, float] = (0.0, 0.0)) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute NMR spectrum from FID (Free Induction Decay) data.

        Args:
            fid_data: Complex FID data (time domain)
            zero_fill_factor: Zero-filling factor for better resolution (default: 2x)
            line_broadening: Exponential line broadening in Hz (default: 50 Hz)
            phase_correction: Tuple of (zero-order, first-order) phase in degrees

        Returns:
            Tuple of (frequency_axis, spectrum_magnitude)
        """
        n_points = len(fid_data)

        # Apply exponential apodization (line broadening)
        if line_broadening > 0:
            # Assume effective sample rate after decimation
            effective_rate = self.sample_rate  # Will be adjusted in real use
            time_axis = np.arange(n_points) / effective_rate
            apodization = np.exp(-line_broadening * np.pi * time_axis)
            fid_apodized = fid_data * apodization
        else:
            fid_apodized = fid_data.copy()

        # Apply phase correction
        ph0, ph1 = phase_correction
        if ph0 != 0 or ph1 != 0:
            phase_ramp = np.linspace(0, ph1, n_points) + ph0
            phase_correction_factor = np.exp(1j * np.deg2rad(phase_ramp))
            fid_apodized *= phase_correction_factor

        # Zero-fill
        zf_size = n_points * zero_fill_factor
        fid_zf = np.zeros(zf_size, dtype=np.complex64)
        fid_zf[:n_points] = fid_apodized

        # FFT (shift for centered spectrum)
        spectrum_complex = np.fft.fftshift(np.fft.fft(fid_zf))

        # Magnitude spectrum
        spectrum_magnitude = np.abs(spectrum_complex)

        # Frequency axis
        freq_axis = np.fft.fftshift(np.fft.fftfreq(zf_size, d=1/self.sample_rate))

        return freq_axis, spectrum_magnitude

    def extract_spectral_window(self,
                                 freq_axis: np.ndarray,
                                 spectrum: np.ndarray,
                                 center_freq: float,
                                 bandwidth: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract spectral window centered at specific frequency.

        Args:
            freq_axis: Frequency axis from FFT
            spectrum: Spectrum magnitude
            center_freq: Center frequency in Hz
            bandwidth: Bandwidth in Hz

        Returns:
            Tuple of (windowed_freq_axis, windowed_spectrum)
        """
        half_bw = bandwidth / 2.0
        mask = (freq_axis >= center_freq - half_bw) & (freq_axis <= center_freq + half_bw)

        return freq_axis[mask], spectrum[mask]

    def measure_snr(self,
                    spectrum: np.ndarray,
                    signal_region: Tuple[int, int],
                    noise_region: Tuple[int, int]) -> float:
        """
        Measure signal-to-noise ratio.

        Args:
            spectrum: Spectrum magnitude
            signal_region: Tuple of (start_idx, end_idx) for signal peak
            noise_region: Tuple of (start_idx, end_idx) for noise floor

        Returns:
            SNR value
        """
        signal_start, signal_end = signal_region
        noise_start, noise_end = noise_region

        # Signal: maximum in signal region
        signal_peak = np.max(spectrum[signal_start:signal_end])

        # Noise: RMS in noise region
        noise_rms = np.sqrt(np.mean(spectrum[noise_start:noise_end] ** 2))

        snr = signal_peak / noise_rms if noise_rms > 0 else 0.0

        return snr

    def baseline_correction(self,
                            spectrum: np.ndarray,
                            polynomial_order: int = 3) -> np.ndarray:
        """
        Apply polynomial baseline correction.

        Args:
            spectrum: Spectrum magnitude
            polynomial_order: Order of baseline polynomial (default: 3)

        Returns:
            Baseline-corrected spectrum
        """
        x = np.arange(len(spectrum))

        # Fit polynomial to spectrum
        coeffs = np.polyfit(x, spectrum, polynomial_order)
        baseline = np.polyval(coeffs, x)

        # Subtract baseline
        corrected = spectrum - baseline

        return corrected

    def integrate_peak(self,
                       freq_axis: np.ndarray,
                       spectrum: np.ndarray,
                       peak_region: Tuple[float, float]) -> float:
        """
        Integrate spectral peak.

        Args:
            freq_axis: Frequency axis
            spectrum: Spectrum magnitude
            peak_region: Tuple of (start_freq, end_freq) in Hz

        Returns:
            Integrated peak area
        """
        start_freq, end_freq = peak_region

        # Find indices corresponding to frequency range
        mask = (freq_axis >= start_freq) & (freq_axis <= end_freq)

        # Trapezoidal integration
        peak_area = np.trapz(spectrum[mask], freq_axis[mask])

        return peak_area


# Helper functions for common NMR processing tasks

def process_fid_to_spectrum(fid_data: np.ndarray,
                            sample_rate: float = 325e6,
                            decimation: int = 32,
                            line_broadening: float = 50.0,
                            zero_fill: int = 2) -> Tuple[np.ndarray, np.ndarray]:
    """
    Complete processing pipeline: FID → Spectrum.

    Args:
        fid_data: Raw complex FID data
        sample_rate: Sample rate in Hz
        decimation: Decimation factor
        line_broadening: Line broadening in Hz
        zero_fill: Zero-fill factor

    Returns:
        Tuple of (frequency_axis, spectrum)
    """
    processor = NMRSignalProcessor(sample_rate=sample_rate)

    # Decimate if needed
    if decimation > 1:
        fid_decimated = processor.decimate(fid_data, decimation_factor=decimation)
        effective_rate = sample_rate / decimation
    else:
        fid_decimated = fid_data
        effective_rate = sample_rate

    # Update processor sample rate for FFT
    processor.sample_rate = effective_rate

    # Compute spectrum
    freq_axis, spectrum = processor.fft_spectrum(
        fid_decimated,
        zero_fill_factor=zero_fill,
        line_broadening=line_broadening
    )

    return freq_axis, spectrum


# Test harness
if __name__ == '__main__':
    print("NMR Signal Processing Test")
    print("=" * 60)

    # Generate simulated NMR FID (damped sinusoid)
    print("\nGenerating simulated NMR FID...")

    sample_rate = 325e6  # 325 MHz
    duration = 1e-3  # 1 ms acquisition
    n_samples = int(sample_rate * duration)

    time_axis = np.arange(n_samples) / sample_rate

    # Simulate NMR signal: damped cosine at 10 MHz offset
    signal_freq = 10e6  # 10 MHz
    decay_time = 100e-6  # 100 us T2
    amplitude = 1000.0

    fid_signal = amplitude * np.exp(-time_axis / decay_time) * np.exp(1j * 2 * np.pi * signal_freq * time_axis)

    # Add noise
    noise_level = 10.0
    noise = noise_level * (np.random.randn(n_samples) + 1j * np.random.randn(n_samples))
    fid_noisy = fid_signal + noise

    print(f"FID: {n_samples} samples at {sample_rate/1e6:.0f} MHz")
    print(f"Signal: {signal_freq/1e6:.1f} MHz, T2={decay_time*1e6:.0f} us, SNR~{amplitude/noise_level:.0f}")

    # Process FID
    print("\nProcessing FID → Spectrum...")

    processor = NMRSignalProcessor(sample_rate=sample_rate)

    # Test decimation
    decimation_factor = 32
    fid_decimated = processor.decimate(fid_noisy, decimation_factor=decimation_factor)
    print(f"Decimation: {decimation_factor}x → {len(fid_decimated)} samples")

    # Update sample rate for FFT
    processor.sample_rate = sample_rate / decimation_factor

    # Compute spectrum
    freq_axis, spectrum = processor.fft_spectrum(
        fid_decimated,
        zero_fill_factor=4,
        line_broadening=100.0
    )

    print(f"Spectrum: {len(spectrum)} points")
    print(f"Frequency range: {freq_axis[0]/1e6:.2f} to {freq_axis[-1]/1e6:.2f} MHz")

    # Find peak
    peak_idx = np.argmax(spectrum)
    peak_freq = freq_axis[peak_idx]
    peak_amplitude = spectrum[peak_idx]

    print(f"\nPeak detected:")
    print(f"  Frequency: {peak_freq/1e6:.3f} MHz (expected: {signal_freq/1e6:.1f} MHz)")
    print(f"  Amplitude: {peak_amplitude:.1f}")

    # Measure SNR
    signal_region = (peak_idx - 100, peak_idx + 100)
    noise_region = (0, 500)  # Assume noise at edge of spectrum

    snr = processor.measure_snr(spectrum, signal_region, noise_region)
    print(f"  SNR: {snr:.1f}")

    # Integration
    bandwidth = 1e6  # 1 MHz
    peak_area = processor.integrate_peak(freq_axis, spectrum, (peak_freq - bandwidth/2, peak_freq + bandwidth/2))
    print(f"  Integrated area: {peak_area:.2e}")

    print("\n" + "=" * 60)
    print("Signal processing test complete ✓")
    print("\nReady for integration with data acquisition system")
