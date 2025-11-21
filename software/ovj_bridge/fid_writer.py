#!/usr/bin/env python3
"""
OpenVNMRJ FID File Writer

Writes acquired I/Q data to OpenVNMRJ FID file format for display in VnmrJ GUI.

FID File Structure:
    - File header (32 bytes): Global acquisition parameters
    - Block headers (28 bytes each): Per-scan metadata
    - Data blocks: Interleaved float32 I/Q data

This module bridges the gap between Crimson TNG UDP data acquisition
and OpenVNMRJ's FID display format, allowing users to view NMR spectra
acquired from the Crimson TNG SDR in the familiar VnmrJ interface.

File Format Reference:
    OpenVNMRJ Technical Manual, Chapter 7: Data File Formats
    https://openvnmrj.org/docs/datafile.html

Author: Chad Rienstra / Claude Code
Date: November 21, 2025
"""

import os
import struct
import logging
import numpy as np
from typing import Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class FIDWriterError(Exception):
    """Base exception for FID writer errors."""
    pass


class FIDWriter:
    """
    Write OpenVNMRJ FID format files from I/Q acquisition data.

    The FID file format is a binary format consisting of:
    1. File header (32 bytes) - describes overall dataset
    2. Block headers (28 bytes each) - describes each scan/trace
    3. Data blocks (float32 arrays) - interleaved I/Q data

    All binary data is big-endian (network byte order).

    Attributes:
        output_path: Path to output FID file

    Example:
        writer = FIDWriter('/vnmr/exp1/acqfil/fid')
        i_data = np.array([...], dtype=np.float32)
        q_data = np.array([...], dtype=np.float32)
        params = {'np': 2048, 'sw': 50000, 'sfrq': 500.0}
        writer.write_1d_fid(i_data, q_data, params)
    """

    # FID format constants
    BYTES_PER_ELEMENT = 4  # float32
    FILE_VERSION = 0       # Standard FID version
    STATUS_DATA = 0x1      # Status bit: contains data
    NUM_BLOCK_HEADERS = 1  # Number of block headers per block

    def __init__(self, output_path: str):
        """
        Initialize FID writer.

        Args:
            output_path: Full path to output FID file
                        (typically /vnmr/expN/acqfil/fid)

        Raises:
            FIDWriterError: If parent directory cannot be created

        Example:
            writer = FIDWriter('/vnmr/exp1/acqfil/fid')
        """
        self.output_path = Path(output_path)

        # Create parent directory if it doesn't exist
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise FIDWriterError(
                f"Cannot create output directory {self.output_path.parent}: {e}"
            ) from e

        logger.info(f"Initialized FID writer: {output_path}")

    def write_1d_fid(
        self,
        i_data: np.ndarray,
        q_data: np.ndarray,
        params: Dict,
        append: bool = False
    ) -> None:
        """
        Write 1D NMR FID file from I/Q data.

        For simple 1D acquisitions (single scan or averaged scans).
        Creates a file with nblocks=1, ntraces=1.

        Args:
            i_data: In-phase data (real component), shape (np,)
            q_data: Quadrature data (imaginary component), shape (np,)
            params: Acquisition parameters dictionary containing:
                - 'np': Number of points (must match data length)
                - 'sw': Spectral width in Hz (optional, for documentation)
                - 'sfrq': Spectrometer frequency in MHz (optional)
            append: If True, append as additional block to existing file

        Raises:
            FIDWriterError: If data validation fails or write error occurs

        Example:
            # Single scan acquisition
            i_data = np.array([...], dtype=np.float32)
            q_data = np.array([...], dtype=np.float32)
            params = {'np': 2048, 'sw': 50000.0, 'sfrq': 500.0}
            writer.write_1d_fid(i_data, q_data, params)

            # Multiple scans (accumulation)
            for scan in range(4):
                i_data, q_data = acquire_data()
                writer.write_1d_fid(i_data, q_data, params, append=(scan > 0))
        """
        # Validate inputs
        self._validate_iq_data(i_data, q_data)
        np_points = len(i_data)

        # Check that np parameter matches data length
        if 'np' in params and params['np'] != np_points:
            logger.warning(
                f"Parameter np={params['np']} does not match "
                f"data length {np_points}, using data length"
            )
        params['np'] = np_points

        logger.info(f"Writing 1D FID: np={np_points} points")

        try:
            if append:
                if not self.output_path.exists():
                    raise FIDWriterError(
                        f"Cannot append: file does not exist at {self.output_path}"
                    )
                # Append as new block to existing file
                self._append_block(i_data, q_data)
            else:
                # Write new file
                self._write_new_file(i_data, q_data, params, nblocks=1, ntraces=1)

            logger.info(f"Successfully wrote FID file: {self.output_path}")

        except FIDWriterError:
            # Re-raise FIDWriterError as-is
            raise
        except Exception as e:
            raise FIDWriterError(f"Failed to write FID file: {e}") from e

    def write_2d_fid(
        self,
        data_2d: np.ndarray,
        params: Dict
    ) -> None:
        """
        Write 2D NMR FID file from multi-dimensional data.

        For 2D experiments with multiple t1 increments (traces).
        Creates a file with nblocks=1, ntraces=N.

        Args:
            data_2d: Complex 2D data array, shape (ntraces, np)
                    dtype should be complex64 or complex128
            params: Acquisition parameters dictionary containing:
                - 'np': Number of points in direct dimension
                - 'ni': Number of increments in indirect dimension
                - 'sw': Spectral width in Hz (direct dimension)
                - 'sw1': Spectral width in Hz (indirect dimension, optional)

        Raises:
            FIDWriterError: If data validation fails or write error occurs

        Example:
            # 2D HETCOR data (32 t1 increments, 2048 points each)
            data_2d = np.zeros((32, 2048), dtype=np.complex64)
            for t1_idx in range(32):
                data_2d[t1_idx, :] = acquire_fid(t1_idx)

            params = {'np': 2048, 'ni': 32, 'sw': 50000.0, 'sw1': 25000.0}
            writer.write_2d_fid(data_2d, params)
        """
        # Validate 2D data
        if data_2d.ndim != 2:
            raise FIDWriterError(
                f"data_2d must be 2D array, got shape {data_2d.shape}"
            )

        ntraces, np_points = data_2d.shape

        logger.info(f"Writing 2D FID: {ntraces} traces × {np_points} points")

        # Extract I/Q from complex data
        i_data_2d = np.real(data_2d).astype(np.float32)
        q_data_2d = np.imag(data_2d).astype(np.float32)

        # Validate parameters
        if 'np' in params and params['np'] != np_points:
            logger.warning(
                f"Parameter np={params['np']} does not match "
                f"data dimension {np_points}"
            )
        params['np'] = np_points
        params['ni'] = ntraces

        try:
            # For 2D data, write all traces as a single block
            # Each trace gets its own block header
            with open(self.output_path, 'wb') as f:
                # Write file header
                self._write_file_header(f, params, nblocks=ntraces, ntraces=1)

                # Write each trace as a separate block
                for trace_idx in range(ntraces):
                    i_trace = i_data_2d[trace_idx, :]
                    q_trace = q_data_2d[trace_idx, :]

                    # Write block header
                    self._write_block_header(
                        f, params, block_index=trace_idx, ctcount=1
                    )

                    # Write interleaved I/Q data
                    iq_interleaved = self._interleave_iq(i_trace, q_trace)
                    f.write(iq_interleaved.tobytes())

            logger.info(f"Successfully wrote 2D FID file: {self.output_path}")

        except Exception as e:
            raise FIDWriterError(f"Failed to write 2D FID file: {e}") from e

    def _write_new_file(
        self,
        i_data: np.ndarray,
        q_data: np.ndarray,
        params: Dict,
        nblocks: int,
        ntraces: int
    ) -> None:
        """
        Write a new FID file.

        Args:
            i_data: In-phase data
            q_data: Quadrature data
            params: Acquisition parameters
            nblocks: Number of blocks in file
            ntraces: Number of traces per block
        """
        with open(self.output_path, 'wb') as f:
            # Write file header
            self._write_file_header(f, params, nblocks, ntraces)

            # Write single block
            self._write_block_header(f, params, block_index=0, ctcount=1)

            # Write interleaved I/Q data
            iq_interleaved = self._interleave_iq(i_data, q_data)
            f.write(iq_interleaved.tobytes())

    def _append_block(
        self,
        i_data: np.ndarray,
        q_data: np.ndarray
    ) -> None:
        """
        Append a new block to existing FID file.

        This is used for multiple-scan accumulation (e.g., signal averaging).
        Updates the file header nblocks field and appends new block data.

        Args:
            i_data: In-phase data for new block
            q_data: Quadrature data for new block
        """
        if not self.output_path.exists():
            raise FIDWriterError("Cannot append: file does not exist")

        # Read existing file header to get nblocks
        with open(self.output_path, 'rb') as f:
            file_header = self._read_file_header(f)

        old_nblocks = file_header['nblocks']
        new_nblocks = old_nblocks + 1

        logger.info(f"Appending block {new_nblocks} to existing FID file")

        # Update nblocks in file header
        with open(self.output_path, 'r+b') as f:
            # Write new nblocks at offset 0
            f.seek(0)
            f.write(struct.pack('>i', new_nblocks))

            # Seek to end of file to append new block
            f.seek(0, 2)  # SEEK_END

            # Write block header for new block
            self._write_block_header(
                f,
                params={'np': len(i_data)},
                block_index=old_nblocks,
                ctcount=1
            )

            # Write interleaved I/Q data
            iq_interleaved = self._interleave_iq(i_data, q_data)
            f.write(iq_interleaved.tobytes())

    def _write_file_header(
        self,
        f,
        params: Dict,
        nblocks: int,
        ntraces: int
    ) -> None:
        """
        Write FID file header (32 bytes).

        File Header Structure (all big-endian):
            Offset  Size  Type    Field       Description
            0       4     int32   nblocks     Number of blocks (traces)
            4       4     int32   ntraces     Number of traces per block
            8       4     int32   np          Number of points per trace
            12      4     int32   ebytes      Bytes per element (4 for float)
            16      4     int32   tbytes      Bytes per trace
            20      4     int32   bbytes      Bytes per block
            24      2     int16   vers_id     File version (0)
            26      2     int16   status      Status flags (0x1 = data)
            28      4     int32   nbheaders   Number of block headers (1)

        Args:
            f: Open file handle
            params: Parameter dictionary containing 'np'
            nblocks: Number of blocks in file
            ntraces: Number of traces per block
        """
        np_points = params['np']
        ebytes = self.BYTES_PER_ELEMENT

        # Calculate sizes
        # Each trace has np complex points = 2*np float32 values
        tbytes = np_points * 2 * ebytes
        # Each block has ntraces traces + one block header (28 bytes)
        bbytes = ntraces * tbytes + 28

        # Pack file header (big-endian format)
        header = struct.pack(
            '>iiiiiihhi',  # All big-endian
            nblocks,           # Number of blocks
            ntraces,           # Number of traces per block
            np_points,         # Number of points per trace
            ebytes,            # Bytes per element
            tbytes,            # Bytes per trace
            bbytes,            # Bytes per block
            self.FILE_VERSION, # Version ID (0)
            self.STATUS_DATA,  # Status (0x1 = contains data)
            self.NUM_BLOCK_HEADERS  # Number of block headers (1)
        )

        # Verify header size
        assert len(header) == 32, f"File header must be 32 bytes, got {len(header)}"

        f.write(header)

        logger.debug(
            f"Wrote file header: nblocks={nblocks}, ntraces={ntraces}, "
            f"np={np_points}, tbytes={tbytes}, bbytes={bbytes}"
        )

    def _write_block_header(
        self,
        f,
        params: Dict,
        block_index: int,
        ctcount: int
    ) -> None:
        """
        Write block header (28 bytes).

        Block Header Structure (all big-endian):
            Offset  Size  Type     Field      Description
            0       2     int16    scale      Scaling factor (0)
            2       2     int16    status     Block status (1 = valid)
            4       2     int16    index      Block index (0, 1, 2, ...)
            6       2     int16    mode       Mode bits (0)
            8       4     int32    ctcount    Completed transients
            12      4     float32  lpval      Left phase (0.0)
            16      4     float32  rpval      Right phase (0.0)
            20      4     float32  lvl        Level (0.0)
            24      4     float32  tlt        Tilt (0.0)

        Args:
            f: Open file handle
            params: Parameter dictionary (currently unused)
            block_index: Block index (0-based)
            ctcount: Number of completed transients (scans)
        """
        # Pack block header (big-endian format)
        header = struct.pack(
            '>hhhhi4f',  # All big-endian
            0,              # scale (0 = no scaling)
            1,              # status (1 = valid block)
            block_index,    # index (block number)
            0,              # mode (0 = normal)
            ctcount,        # ctcount (completed transients)
            0.0,            # lpval (left phase)
            0.0,            # rpval (right phase)
            0.0,            # lvl (level)
            0.0             # tlt (tilt)
        )

        # Verify header size
        assert len(header) == 28, f"Block header must be 28 bytes, got {len(header)}"

        f.write(header)

        logger.debug(
            f"Wrote block header: index={block_index}, ctcount={ctcount}"
        )

    def _interleave_iq(
        self,
        i_data: np.ndarray,
        q_data: np.ndarray
    ) -> np.ndarray:
        """
        Interleave I and Q data for FID file format.

        OpenVNMRJ expects data as: [I0, Q0, I1, Q1, I2, Q2, ...]
        Data must be in big-endian format for FID files.

        Args:
            i_data: In-phase component (real), shape (n,)
            q_data: Quadrature component (imaginary), shape (n,)

        Returns:
            Interleaved array, shape (2*n,), dtype float32, big-endian

        Example:
            i_data = [1.0, 2.0, 3.0]
            q_data = [4.0, 5.0, 6.0]
            result = [1.0, 4.0, 2.0, 5.0, 3.0, 6.0]
        """
        n = len(i_data)
        # Ensure data is float32
        i_data = i_data.astype(np.float32)
        q_data = q_data.astype(np.float32)

        # Create interleaved array
        interleaved = np.empty(2 * n, dtype=np.float32)
        interleaved[0::2] = i_data  # Even indices: I
        interleaved[1::2] = q_data  # Odd indices: Q

        # Convert to big-endian for FID format
        interleaved = interleaved.astype('>f4')
        return interleaved

    def _validate_iq_data(
        self,
        i_data: np.ndarray,
        q_data: np.ndarray
    ) -> None:
        """
        Validate I/Q data arrays.

        Args:
            i_data: In-phase data
            q_data: Quadrature data

        Raises:
            FIDWriterError: If validation fails
        """
        # Check that arrays are numpy arrays
        if not isinstance(i_data, np.ndarray) or not isinstance(q_data, np.ndarray):
            raise FIDWriterError("i_data and q_data must be numpy arrays")

        # Check dimensions
        if i_data.ndim != 1 or q_data.ndim != 1:
            raise FIDWriterError(
                f"i_data and q_data must be 1D arrays, "
                f"got shapes {i_data.shape}, {q_data.shape}"
            )

        # Check lengths match
        if len(i_data) != len(q_data):
            raise FIDWriterError(
                f"i_data and q_data must have same length, "
                f"got {len(i_data)} and {len(q_data)}"
            )

        # Check not empty
        if len(i_data) == 0:
            raise FIDWriterError("i_data and q_data cannot be empty")

        # Convert to float32 if needed
        if i_data.dtype != np.float32:
            logger.warning(f"Converting i_data from {i_data.dtype} to float32")
        if q_data.dtype != np.float32:
            logger.warning(f"Converting q_data from {q_data.dtype} to float32")

    def _read_file_header(self, f) -> Dict:
        """
        Read and parse FID file header.

        Args:
            f: Open file handle positioned at start of file

        Returns:
            Dictionary with file header fields
        """
        header_bytes = f.read(32)
        if len(header_bytes) != 32:
            raise FIDWriterError("Invalid FID file: header too short")

        # Unpack file header (big-endian)
        header = struct.unpack('>iiiiiihhi', header_bytes)

        return {
            'nblocks': header[0],
            'ntraces': header[1],
            'np': header[2],
            'ebytes': header[3],
            'tbytes': header[4],
            'bbytes': header[5],
            'vers_id': header[6],
            'status': header[7],
            'nbheaders': header[8]
        }


def main():
    """Demo/test FID writer."""
    import tempfile

    logging.basicConfig(level=logging.INFO)

    # Create temporary output directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'fid')

        # Create FID writer
        writer = FIDWriter(output_path)

        # Generate synthetic NMR data (damped sinusoid)
        np_points = 2048
        t = np.arange(np_points) / 50000.0  # 50 kHz sampling

        # Damped sinusoid at 1 kHz with 50 Hz decay
        signal = np.exp(-50 * 2 * np.pi * t) * np.exp(1j * 2 * np.pi * 1000 * t)
        i_data = np.real(signal).astype(np.float32)
        q_data = np.imag(signal).astype(np.float32)

        # Write 1D FID
        params = {
            'np': np_points,
            'sw': 50000.0,  # 50 kHz spectral width
            'sfrq': 500.0    # 500 MHz spectrometer frequency
        }

        writer.write_1d_fid(i_data, q_data, params)

        print(f"\n✓ Successfully wrote FID file: {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        print(f"  Expected: {32 + 28 + 2*np_points*4} bytes")

        # Verify file can be read back
        with open(output_path, 'rb') as f:
            header = writer._read_file_header(f)
            print(f"\nFile header:")
            print(f"  nblocks: {header['nblocks']}")
            print(f"  ntraces: {header['ntraces']}")
            print(f"  np: {header['np']}")
            print(f"  ebytes: {header['ebytes']}")
            print(f"  tbytes: {header['tbytes']}")
            print(f"  bbytes: {header['bbytes']}")


if __name__ == '__main__':
    main()
