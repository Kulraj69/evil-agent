"""Tests for the anti-hallucination evidence validator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence_validator import EvidenceValidator, HallucinationDetector


def make_evidence():
    return {
        "auth_events": {"findings": {"summary": {"failed_logins": 47, "brute_force_detected": True}}},
        "memory_dump": {"findings": {"credential_dumping_indicators": True, "lsass_injection": True}},
    }


def test_supported_finding_passes():
    v = EvidenceValidator()
    r = v.validate_finding(
        "Brute-force authentication attack with 47 failed login attempts",
        ["auth_events"],
        make_evidence(),
    )
    assert r.is_supported is True
    assert r.confidence >= 0.6


def test_missing_citation_rejected():
    v = EvidenceValidator()
    r = v.validate_finding("Some claim", ["does_not_exist"], make_evidence())
    assert r.is_supported is False
    assert "does_not_exist" in r.missing_evidence


def test_no_citations_rejected():
    v = EvidenceValidator()
    r = v.validate_finding("Unsupported claim", [], make_evidence())
    assert r.is_supported is False


def test_fabricated_number_rejected():
    v = EvidenceValidator()
    r = v.validate_finding(
        "Brute-force attack with 999 failed login attempts",
        ["auth_events"],
        make_evidence(),
    )
    assert r.is_supported is False
    assert "999" in r.reason


def test_fabricated_filename_pattern_rejected():
    v = EvidenceValidator()
    r = v.validate_finding("malware.exe was executed", ["auth_events"], make_evidence())
    assert r.is_supported is False
    assert "pattern" in r.reason.lower()


def test_credential_dumping_concept_corroboration():
    v = EvidenceValidator()
    r = v.validate_finding(
        "Credential dumping via LSASS process injection",
        ["memory_dump"],
        make_evidence(),
    )
    assert r.is_supported is True


def test_hallucination_detector_patterns():
    d = HallucinationDetector()
    assert d.detect_hallucination_patterns("found evil.dll on disk")
    assert d.detect_hallucination_patterns("C:\\Malware\\bad.exe")
    assert not d.detect_hallucination_patterns("powershell.exe ran twice")
