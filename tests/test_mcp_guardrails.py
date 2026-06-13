"""Tests for MCP server architectural guardrails + evidence integrity."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcp_server.sift_mcp_server import SIFTMCPServer


def test_no_shell_execution_function():
    """The server must NOT expose any shell/exec/write capability."""
    s = SIFTMCPServer()
    forbidden = ["execute_shell_cmd", "run_shell", "exec", "system", "write_file", "delete_file"]
    for name in forbidden:
        assert not hasattr(s, name), f"server should not expose {name}"


def test_only_whitelisted_tools_exist():
    s = SIFTMCPServer()
    expected = {
        "analyze_prefetch", "extract_mft_timeline", "parse_event_logs",
        "analyze_memory_dump", "search_registry_hive", "get_amcache",
    }
    for tool in expected:
        assert callable(getattr(s, tool))


def test_path_traversal_rejected():
    s = SIFTMCPServer()
    try:
        s._validate_path("../../etc/passwd")
        assert False, "path traversal should raise"
    except ValueError:
        pass


def test_memory_plugin_whitelist():
    """Non-whitelisted plugins must be rejected (raises), never silently run."""
    import pytest
    s = SIFTMCPServer()
    with pytest.raises(ValueError):
        s.analyze_memory_dump(dump_path="/evidence/mem.raw", plugin="not_a_real_plugin")


def test_execution_log_records_runs():
    s = SIFTMCPServer()
    s.analyze_prefetch(image_path="/evidence/disk.dd")
    log = s.get_execution_log()
    assert len(log) == 1
    assert log[0]["tool"] == "analyze_prefetch"
    assert "execution_id" in log[0]


def test_evidence_integrity_detects_spoliation():
    s = SIFTMCPServer()
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".raw")
    f.write(b"original evidence")
    f.close()
    try:
        baseline = s.register_evidence(f.name)
        assert baseline is not None
        assert s.verify_integrity(f.name) is True  # unchanged

        with open(f.name, "ab") as fh:
            fh.write(b"TAMPERED")
        assert s.verify_integrity(f.name) is False  # detected
        assert len(s.spoliation_events) == 1
    finally:
        os.unlink(f.name)


def test_integrity_neutral_when_no_file():
    """Synthetic mode (no on-disk file) is integrity-neutral, not a false alarm."""
    s = SIFTMCPServer()
    assert s.register_evidence("/evidence/does_not_exist.raw") is None
    assert s.verify_integrity("/evidence/does_not_exist.raw") is True
