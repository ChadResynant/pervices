#!/usr/bin/env python3
"""
Test Suite for OpenVNMRJ FID Writer

Comprehensive tests for FID file writing functionality:
    - File header structure validation
    - Block header structure validation
    - I/Q data interleaving
    - 1D FID file creation
    - 2D FID file creation
    - Multi-block append functionality
    - Error handling

Author: Chad Rienstra / Claude Code
Date: November 21, 2025
"""

import os
import sys
import struct
import tempfile
import pytest
import numpy as np
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fid_writer import FIDWriter, FIDWriterError


class TestFIDWriterBasics:
    """Test basic FID writer initialization and validation."""

    def test_initialization(self, tmp_path):
        """Test FID writer initialization."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        assert writer.output_path == output_path
        assert writer.BYTES_PER_ELEMENT == 4
        assert writer.FILE_VERSION == 0
        assert writer.STATUS_DATA == 0x1

    def test_creates_parent_directory(self, tmp_path):
        """Test that parent directories are created if needed."""
        output_path = tmp_path / "acqfil" / "fid"
        writer = FIDWriter(str(output_path))

        assert output_path.parent.exists()

    def test_validate_iq_data_success(self, tmp_path):
        """Test successful I/Q data validation."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        q_data = np.array([4.0, 5.0, 6.0], dtype=np.float32)

        # Should not raise exception
        writer._validate_iq_data(i_data, q_data)

    def test_validate_iq_data_length_mismatch(self, tmp_path):
        """Test validation fails on length mismatch."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        q_data = np.array([4.0, 5.0], dtype=np.float32)

        with pytest.raises(FIDWriterError, match="same length"):
            writer._validate_iq_data(i_data, q_data)

    def test_validate_iq_data_wrong_dimensions(self, tmp_path):
        """Test validation fails on wrong dimensions."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        q_data = np.array([[5.0, 6.0], [7.0, 8.0]], dtype=np.float32)

        with pytest.raises(FIDWriterError, match="1D arrays"):
            writer._validate_iq_data(i_data, q_data)

    def test_validate_iq_data_empty(self, tmp_path):
        """Test validation fails on empty arrays."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.array([], dtype=np.float32)
        q_data = np.array([], dtype=np.float32)

        with pytest.raises(FIDWriterError, match="cannot be empty"):
            writer._validate_iq_data(i_data, q_data)


class TestIQInterleaving:
    """Test I/Q data interleaving."""

    def test_interleave_iq_simple(self, tmp_path):
        """Test basic I/Q interleaving."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        q_data = np.array([4.0, 5.0, 6.0], dtype=np.float32)

        result = writer._interleave_iq(i_data, q_data)

        expected = np.array([1.0, 4.0, 2.0, 5.0, 3.0, 6.0], dtype=np.float32)
        np.testing.assert_array_equal(result, expected)

    def test_interleave_iq_length(self, tmp_path):
        """Test interleaved array has correct length."""
        writer = FIDWriter(str(tmp_path / "fid"))

        n = 1024
        i_data = np.random.randn(n).astype(np.float32)
        q_data = np.random.randn(n).astype(np.float32)

        result = writer._interleave_iq(i_data, q_data)

        assert len(result) == 2 * n
        # Result should be big-endian float32
        assert result.dtype == np.dtype('>f4')

    def test_interleave_iq_pattern(self, tmp_path):
        """Test interleaving pattern is correct."""
        writer = FIDWriter(str(tmp_path / "fid"))

        i_data = np.arange(10, dtype=np.float32)
        q_data = np.arange(100, 110, dtype=np.float32)

        result = writer._interleave_iq(i_data, q_data)

        # Check even indices (I data)
        np.testing.assert_array_equal(result[0::2], i_data)
        # Check odd indices (Q data)
        np.testing.assert_array_equal(result[1::2], q_data)


class TestFileHeader:
    """Test FID file header writing and reading."""

    def test_write_file_header_structure(self, tmp_path):
        """Test file header has correct structure."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        with open(output_path, 'wb') as f:
            params = {'np': 2048}
            writer._write_file_header(f, params, nblocks=1, ntraces=1)

        # Verify file size
        assert output_path.stat().st_size == 32

        # Read and verify header
        with open(output_path, 'rb') as f:
            header_bytes = f.read(32)
            header = struct.unpack('>iiiiiihhi', header_bytes)

            nblocks, ntraces, np_points, ebytes, tbytes, bbytes, vers_id, status, nbheaders = header

            assert nblocks == 1
            assert ntraces == 1
            assert np_points == 2048
            assert ebytes == 4  # float32
            assert tbytes == 2048 * 2 * 4  # np * 2 * ebytes
            assert bbytes == tbytes + 28  # tbytes + block header size
            assert vers_id == 0
            assert status == 0x1
            assert nbheaders == 1

    def test_read_file_header(self, tmp_path):
        """Test reading back file header."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        # Write header
        with open(output_path, 'wb') as f:
            params = {'np': 1024}
            writer._write_file_header(f, params, nblocks=2, ntraces=3)

        # Read header back
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)

            assert header['nblocks'] == 2
            assert header['ntraces'] == 3
            assert header['np'] == 1024
            assert header['ebytes'] == 4
            assert header['vers_id'] == 0
            assert header['status'] == 0x1


class TestBlockHeader:
    """Test FID block header writing."""

    def test_write_block_header_structure(self, tmp_path):
        """Test block header has correct structure."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        with open(output_path, 'wb') as f:
            params = {'np': 2048}
            writer._write_block_header(f, params, block_index=0, ctcount=4)

        # Verify file size
        assert output_path.stat().st_size == 28

        # Read and verify header
        with open(output_path, 'rb') as f:
            header_bytes = f.read(28)
            header = struct.unpack('>hhhhi4f', header_bytes)

            scale, status, index, mode, ctcount, lpval, rpval, lvl, tlt = header

            assert scale == 0
            assert status == 1
            assert index == 0
            assert mode == 0
            assert ctcount == 4
            assert lpval == 0.0
            assert rpval == 0.0
            assert lvl == 0.0
            assert tlt == 0.0

    def test_write_multiple_block_headers(self, tmp_path):
        """Test writing multiple block headers with different indices."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        with open(output_path, 'wb') as f:
            params = {'np': 1024}
            for idx in range(5):
                writer._write_block_header(f, params, block_index=idx, ctcount=1)

        # Verify file size (5 block headers)
        assert output_path.stat().st_size == 5 * 28

        # Read and verify each header
        with open(output_path, 'rb') as f:
            for expected_idx in range(5):
                header_bytes = f.read(28)
                header = struct.unpack('>hhhhi4f', header_bytes)
                scale, status, index, mode, ctcount, lpval, rpval, lvl, tlt = header
                assert index == expected_idx


class TestWrite1DFID:
    """Test 1D FID file writing."""

    def test_write_simple_1d_fid(self, tmp_path):
        """Test writing a simple 1D FID file."""
        output_path = tmp_path / "acqfil" / "fid"
        writer = FIDWriter(str(output_path))

        # Generate simple test data
        np_points = 256
        i_data = np.arange(np_points, dtype=np.float32)
        q_data = np.arange(100, 100 + np_points, dtype=np.float32)

        params = {'np': np_points, 'sw': 50000.0, 'sfrq': 500.0}

        # Write FID
        writer.write_1d_fid(i_data, q_data, params)

        # Verify file exists
        assert output_path.exists()

        # Verify file size
        expected_size = 32 + 28 + 2 * np_points * 4  # header + block header + data
        assert output_path.stat().st_size == expected_size

    def test_write_1d_fid_file_header(self, tmp_path):
        """Test 1D FID file header is correct."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 512
        i_data = np.random.randn(np_points).astype(np.float32)
        q_data = np.random.randn(np_points).astype(np.float32)
        params = {'np': np_points}

        writer.write_1d_fid(i_data, q_data, params)

        # Read file header
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)

            assert header['nblocks'] == 1
            assert header['ntraces'] == 1
            assert header['np'] == np_points
            assert header['ebytes'] == 4

    def test_write_1d_fid_data_integrity(self, tmp_path):
        """Test that written data can be read back correctly."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 128
        i_data = np.array([1.0, 2.0, 3.0, 4.0] * (np_points // 4), dtype=np.float32)
        q_data = np.array([5.0, 6.0, 7.0, 8.0] * (np_points // 4), dtype=np.float32)
        params = {'np': np_points}

        writer.write_1d_fid(i_data, q_data, params)

        # Read data back
        with open(output_path, 'rb') as f:
            # Skip file header (32 bytes) and block header (28 bytes)
            f.seek(32 + 28)

            # Read interleaved data
            data_bytes = f.read()
            interleaved = np.frombuffer(data_bytes, dtype='>f4')  # big-endian float32

            # Extract I and Q
            i_read = interleaved[0::2]
            q_read = interleaved[1::2]

            # Verify
            np.testing.assert_array_almost_equal(i_read, i_data)
            np.testing.assert_array_almost_equal(q_read, q_data)

    def test_write_1d_fid_realistic_nmr_signal(self, tmp_path):
        """Test with realistic NMR signal (damped sinusoid)."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        # Generate synthetic NMR FID (damped sinusoid)
        np_points = 2048
        t = np.arange(np_points) / 50000.0  # 50 kHz sampling
        decay = 50.0  # Hz decay rate
        freq = 1000.0  # Hz signal frequency

        signal = np.exp(-decay * 2 * np.pi * t) * np.exp(1j * 2 * np.pi * freq * t)
        i_data = np.real(signal).astype(np.float32)
        q_data = np.imag(signal).astype(np.float32)

        params = {'np': np_points, 'sw': 50000.0, 'sfrq': 500.0}

        writer.write_1d_fid(i_data, q_data, params)

        assert output_path.exists()
        expected_size = 32 + 28 + 2 * np_points * 4
        assert output_path.stat().st_size == expected_size


class TestWrite2DFID:
    """Test 2D FID file writing."""

    def test_write_simple_2d_fid(self, tmp_path):
        """Test writing a simple 2D FID file."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        # Generate 2D test data (8 traces × 256 points)
        ntraces = 8
        np_points = 256
        data_2d = np.random.randn(ntraces, np_points).astype(np.complex64)

        params = {'np': np_points, 'ni': ntraces, 'sw': 50000.0}

        writer.write_2d_fid(data_2d, params)

        # Verify file exists
        assert output_path.exists()

        # Verify file size
        # File header + (ntraces × (block header + data))
        expected_size = 32 + ntraces * (28 + 2 * np_points * 4)
        assert output_path.stat().st_size == expected_size

    def test_write_2d_fid_file_header(self, tmp_path):
        """Test 2D FID file header is correct."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        ntraces = 16
        np_points = 512
        data_2d = np.random.randn(ntraces, np_points).astype(np.complex64)
        params = {'np': np_points, 'ni': ntraces}

        writer.write_2d_fid(data_2d, params)

        # Read file header
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)

            # For 2D data, each trace is written as a separate block
            assert header['nblocks'] == ntraces
            assert header['ntraces'] == 1
            assert header['np'] == np_points

    def test_write_2d_fid_data_integrity(self, tmp_path):
        """Test that 2D data can be read back correctly."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        ntraces = 4
        np_points = 64
        # Create known data pattern
        data_2d = np.zeros((ntraces, np_points), dtype=np.complex64)
        for trace_idx in range(ntraces):
            data_2d[trace_idx, :] = trace_idx + 1j * (trace_idx + 10)

        params = {'np': np_points, 'ni': ntraces}

        writer.write_2d_fid(data_2d, params)

        # Read data back
        with open(output_path, 'rb') as f:
            # Skip file header
            f.seek(32)

            for trace_idx in range(ntraces):
                # Skip block header
                f.seek(32 + trace_idx * (28 + 2 * np_points * 4) + 28)

                # Read interleaved data for this trace
                trace_bytes = f.read(2 * np_points * 4)
                interleaved = np.frombuffer(trace_bytes, dtype='>f4')

                # Extract I and Q
                i_read = interleaved[0::2]
                q_read = interleaved[1::2]

                # Verify
                expected_i = np.real(data_2d[trace_idx, :])
                expected_q = np.imag(data_2d[trace_idx, :])
                np.testing.assert_array_almost_equal(i_read, expected_i)
                np.testing.assert_array_almost_equal(q_read, expected_q)

    def test_write_2d_fid_wrong_dimensions(self, tmp_path):
        """Test that wrong-dimensional data raises error."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        # 1D data (should fail)
        data_1d = np.random.randn(256).astype(np.complex64)
        params = {'np': 256}

        with pytest.raises(FIDWriterError, match="2D array"):
            writer.write_2d_fid(data_1d, params)

        # 3D data (should fail)
        data_3d = np.random.randn(4, 4, 64).astype(np.complex64)
        params = {'np': 64}

        with pytest.raises(FIDWriterError, match="2D array"):
            writer.write_2d_fid(data_3d, params)


class TestMultiBlockAppend:
    """Test appending multiple blocks (scan accumulation)."""

    def test_append_single_block(self, tmp_path):
        """Test appending a single block to existing file."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 128
        params = {'np': np_points}

        # Write first block
        i_data1 = np.ones(np_points, dtype=np.float32)
        q_data1 = np.zeros(np_points, dtype=np.float32)
        writer.write_1d_fid(i_data1, q_data1, params, append=False)

        # Append second block
        i_data2 = np.ones(np_points, dtype=np.float32) * 2.0
        q_data2 = np.ones(np_points, dtype=np.float32) * 2.0
        writer.write_1d_fid(i_data2, q_data2, params, append=True)

        # Read file header
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)
            assert header['nblocks'] == 2

        # Verify file size
        expected_size = 32 + 2 * (28 + 2 * np_points * 4)
        assert output_path.stat().st_size == expected_size

    def test_append_multiple_blocks(self, tmp_path):
        """Test appending multiple blocks (scan averaging)."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 256
        params = {'np': np_points}
        num_scans = 8

        # Write multiple scans
        for scan_idx in range(num_scans):
            i_data = np.random.randn(np_points).astype(np.float32)
            q_data = np.random.randn(np_points).astype(np.float32)
            writer.write_1d_fid(i_data, q_data, params, append=(scan_idx > 0))

        # Read file header
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)
            assert header['nblocks'] == num_scans

    def test_append_to_nonexistent_file_fails(self, tmp_path):
        """Test that appending to non-existent file raises error."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 128
        i_data = np.ones(np_points, dtype=np.float32)
        q_data = np.zeros(np_points, dtype=np.float32)
        params = {'np': np_points}

        with pytest.raises(FIDWriterError, match="Cannot append"):
            writer.write_1d_fid(i_data, q_data, params, append=True)


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_write_with_invalid_path(self):
        """Test writing to invalid path."""
        import os
        # Skip test if running as root (can write anywhere)
        if os.geteuid() == 0:
            pytest.skip("Test skipped when running as root")

        # Try to write to a path that can't be created
        output_path = "/root/nonexistent/deeply/nested/fid"

        # Should raise FIDWriterError during initialization
        with pytest.raises(FIDWriterError, match="Cannot create output directory"):
            writer = FIDWriter(output_path)

    def test_np_parameter_mismatch_warning(self, tmp_path, caplog):
        """Test warning when np parameter doesn't match data length."""
        output_path = tmp_path / "fid"
        writer = FIDWriter(str(output_path))

        np_points = 256
        i_data = np.random.randn(np_points).astype(np.float32)
        q_data = np.random.randn(np_points).astype(np.float32)
        params = {'np': 512}  # Wrong np value

        writer.write_1d_fid(i_data, q_data, params)

        # Check that warning was logged
        assert "does not match data length" in caplog.text


def test_integration_realistic_workflow(tmp_path):
    """
    Integration test: Realistic NMR acquisition workflow.

    Simulates:
    1. Initial acquisition (scan 1)
    2. Multiple scan accumulation (scans 2-4)
    3. Verification of final file
    """
    output_path = tmp_path / "acqfil" / "fid"
    writer = FIDWriter(str(output_path))

    # Acquisition parameters
    np_points = 2048
    sw = 50000.0  # 50 kHz spectral width
    sfrq = 500.0  # 500 MHz spectrometer frequency
    num_scans = 4

    params = {
        'np': np_points,
        'sw': sw,
        'sfrq': sfrq
    }

    # Simulate multiple scan acquisition
    for scan_idx in range(num_scans):
        # Generate synthetic NMR signal with noise
        t = np.arange(np_points) / sw
        signal = np.exp(-50 * 2 * np.pi * t) * np.exp(1j * 2 * np.pi * 1000 * t)
        noise = 0.1 * (np.random.randn(np_points) + 1j * np.random.randn(np_points))
        total_signal = signal + noise

        i_data = np.real(total_signal).astype(np.float32)
        q_data = np.imag(total_signal).astype(np.float32)

        # Write scan
        writer.write_1d_fid(i_data, q_data, params, append=(scan_idx > 0))

    # Verify final file
    assert output_path.exists()

    with open(output_path, 'rb') as f:
        header = writer._read_file_header(f)
        assert header['nblocks'] == num_scans
        assert header['np'] == np_points

    # Verify file size
    expected_size = 32 + num_scans * (28 + 2 * np_points * 4)
    assert output_path.stat().st_size == expected_size


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
