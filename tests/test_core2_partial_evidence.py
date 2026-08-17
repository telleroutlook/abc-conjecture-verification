"""Verify the non-accepting CORE-2 partial-evidence boundary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


from checker.check_certificate import _validate_core2_partial_evidence


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_manifest_declares_non_acceptance() -> None:
    path = REPO_ROOT / "domain" / "evidence" / "core-2-partial-evidence.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["accepted"] is False
    assert data["proofctl_gate"] == "rejected"
    assert data["ledger_status"] == "OBL"
    assert data["forbidden_inputs_used"] == []
    assert "The full P_height Faltings/Arakelov framework is not constructed." in data[
        "blocking_gaps"
    ]


def test_manifest_artifacts_validate() -> None:
    valid, message = _validate_core2_partial_evidence(REPO_ROOT)
    assert valid, message
    assert "does not close CORE-2" in message


def test_core2_remains_rejected_with_partial_evidence() -> None:
    inp = {"claim_id": "core-2-height-framework", "obligation_ids": None}
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "checker" / "check_certificate.py")],
        input=json.dumps(inp),
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        check=True,
    )
    results = json.loads(result.stdout)["obligation_results"]
    assert results
    assert all(result["verdict"] == "fail" for result in results)


def test_silverman_aec_source_anchor_replays() -> None:
    pdf = REPO_ROOT / "baseline" / "silverman-2009-arithmetic-elliptic-curves.pdf"
    text = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout
    assert "Lemma 11.3." in text
    assert "E : y 2 = x(x + A)(x − B)." in text
    assert "|ΔE | = 24 |ABC|2" in text
    assert "multiplicative reduction modulo p for all odd primes" in text
