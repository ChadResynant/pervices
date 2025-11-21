#!/usr/bin/env python3
"""
Test suite for OpenVNMRJ to Crimson TNG bridge daemon.

Tests:
    - VnmrJ parameter reading
    - Acode file location
    - PSG completion handling
    - Multi-file parsing

Author: Chad Rienstra / Claude Code
Date: November 21, 2025
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bridge_daemon import (
    VnmrJParameterReader,
    AcodeFileLocator,
    AcodeBridge
)


class TestVnmrJParameterReader:
    """Test VnmrJ parameter file parsing."""

    def test_read_goid_parameter(self, tmp_path):
        """Test reading goid parameter from curpar file."""
        # Create mock curpar file
        curpar = tmp_path / "curpar"
        curpar.write_text("""experiment 1 1
"s2pul"
goid 1 2
"/vnmrsystem/acqqueue/exp1.greg.012345"
nt 1 1
4.0
""")

        # Read parameter
        reader = VnmrJParameterReader(str(tmp_path))
        goid = reader.read_parameter("goid")

        assert goid == "/vnmrsystem/acqqueue/exp1.greg.012345"

    def test_read_numeric_parameter(self, tmp_path):
        """Test reading numeric parameter."""
        curpar = tmp_path / "curpar"
        curpar.write_text("""nt 1 1
16.0
np 1 1
2048.0
""")

        reader = VnmrJParameterReader(str(tmp_path))
        nt = reader.read_parameter("nt")

        assert nt == "16.0"

    def test_parameter_not_found(self, tmp_path):
        """Test handling of non-existent parameter."""
        curpar = tmp_path / "curpar"
        curpar.write_text("""nt 1 1
16.0
""")

        reader = VnmrJParameterReader(str(tmp_path))
        result = reader.read_parameter("nonexistent")

        assert result is None

    def test_missing_curpar_file(self, tmp_path):
        """Test handling of missing curpar file."""
        reader = VnmrJParameterReader(str(tmp_path))
        result = reader.read_parameter("goid")

        assert result is None


class TestAcodeFileLocator:
    """Test Acode file location and parsing."""

    def test_extract_controller_name(self):
        """Test extracting controller name from file path."""
        test_cases = [
            ("/vnmrsystem/acqqueue/exp1.greg.012345.ps.Master1", "Master1"),
            ("/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF1", "RF1"),
            ("/vnmrsystem/acqqueue/exp1.greg.012345.ps.RF2", "RF2"),
            ("/vnmrsystem/acqqueue/exp1.greg.012345.ps.PFG1", "PFG1"),
        ]

        for filepath, expected_controller in test_cases:
            controller = AcodeFileLocator.extract_controller_name(filepath)
            assert controller == expected_controller

    def test_get_acode_files(self, tmp_path):
        """Test finding Acode files matching goid pattern."""
        # Create mock Acode files
        goid = tmp_path / "exp1.greg.012345"
        acode_files = [
            tmp_path / "exp1.greg.012345.ps.Master1",
            tmp_path / "exp1.greg.012345.ps.RF1",
            tmp_path / "exp1.greg.012345.ps.RF2",
        ]

        for filepath in acode_files:
            filepath.write_bytes(b'\x00\x00\x00\x01')  # Dummy Acode data

        # Find files
        found_files = AcodeFileLocator.get_acode_files(str(goid), stage="ps")

        assert len(found_files) == 3
        assert all(os.path.basename(f).startswith("exp1.greg.012345.ps.") for f in found_files)

    def test_get_acode_files_filters_lock_files(self, tmp_path):
        """Test that .lock files are filtered out."""
        goid = tmp_path / "exp1.greg.012345"

        # Create Acode file and lock file
        (tmp_path / "exp1.greg.012345.ps.RF1").write_bytes(b'\x00\x00\x00\x01')
        (tmp_path / "exp1.greg.012345.ps.RF1.lock").write_bytes(b'')

        found_files = AcodeFileLocator.get_acode_files(str(goid), stage="ps")

        assert len(found_files) == 1
        assert not found_files[0].endswith('.lock')


class TestAcodeBridge:
    """Test bridge daemon functionality."""

    def test_bridge_initialization(self):
        """Test bridge daemon initialization."""
        watch_dirs = ["/vnmr/exp1", "/vnmr/exp2"]
        bridge = AcodeBridge(watch_dirs=watch_dirs, crimson_api=None)

        assert bridge.watch_dirs == watch_dirs
        assert bridge.crimson_api is None
        assert bridge.parsers == {}

    def test_load_sequence_with_mock_files(self, tmp_path):
        """Test loading sequence from mock Acode files."""
        # Create mock Acode files with minimal valid structure
        acode_files = []

        for controller in ["Master1", "RF1", "RF2"]:
            filepath = tmp_path / f"exp1.greg.012345.ps.{controller}"

            # Write minimal Acode file (HALT opcode = 4)
            with open(filepath, 'wb') as f:
                # Write a few opcodes
                f.write((46).to_bytes(4, byteorder='big'))   # EVENT1
                f.write((1000).to_bytes(4, byteorder='big'))  # timing
                f.write((0x01).to_bytes(4, byteorder='big'))  # gates
                f.write((4).to_bytes(4, byteorder='big'))    # HALT

            acode_files.append(str(filepath))

        # Create bridge and load sequence
        bridge = AcodeBridge(watch_dirs=["/vnmr/exp1"], crimson_api=None)
        bridge.load_sequence(acode_files)

        # Verify parsers were created
        assert len(bridge.parsers) == 3
        assert "Master1" in bridge.parsers
        assert "RF1" in bridge.parsers
        assert "RF2" in bridge.parsers


def test_integration_psg_completion(tmp_path):
    """
    Integration test: Simulate PSG completion and verify bridge response.

    This test creates a mock experiment directory with:
        - curpar file (with goid parameter)
        - Mock Acode files
        - psgdone file (created to trigger bridge)
    """
    # Create mock experiment directory
    exp_dir = tmp_path / "exp1"
    exp_dir.mkdir()

    # Create curpar with goid
    curpar = exp_dir / "curpar"
    acqqueue = tmp_path / "acqqueue"
    acqqueue.mkdir()

    goid = acqqueue / "exp1.greg.012345"
    curpar.write_text(f"""goid 1 2
"{str(goid)}"
""")

    # Create mock Acode files
    for controller in ["Master1", "RF1"]:
        filepath = Path(f"{str(goid)}.ps.{controller}")
        with open(filepath, 'wb') as f:
            # Minimal Acode: EVENT1 + HALT
            f.write((46).to_bytes(4, byteorder='big'))   # EVENT1
            f.write((1000).to_bytes(4, byteorder='big'))  # timing
            f.write((0x01).to_bytes(4, byteorder='big'))  # gates
            f.write((4).to_bytes(4, byteorder='big'))    # HALT

    # Create bridge
    bridge = AcodeBridge(watch_dirs=[str(exp_dir)], crimson_api=None)

    # Simulate PSG completion
    bridge.on_psg_complete(str(exp_dir))

    # Verify sequence was loaded
    assert len(bridge.parsers) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
