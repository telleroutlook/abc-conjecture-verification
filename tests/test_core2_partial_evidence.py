"""Verify the non-accepting CORE-2 partial-evidence boundary."""

from __future__ import annotations

import json
import shutil
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


def _copy_partial_evidence_tree(root: Path) -> dict:
    source_manifest = (
        REPO_ROOT / "domain" / "evidence" / "core-2-partial-evidence.json"
    )
    data = json.loads(source_manifest.read_text(encoding="utf-8"))
    for artifact in data["artifacts"]:
        destination = root / artifact["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / artifact["path"], destination)
    manifest = root / "domain" / "evidence" / "core-2-partial-evidence.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def test_partial_evidence_rejects_producer_acceptance_flag(tmp_path: Path) -> None:
    data = _copy_partial_evidence_tree(tmp_path)
    data["accepted"] = True
    data["proofctl_gate"] = "accepted"
    data["ledger_status"] = "THM"
    manifest = tmp_path / "domain" / "evidence" / "core-2-partial-evidence.json"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    valid, message = _validate_core2_partial_evidence(tmp_path)
    assert not valid
    assert "invalid accepted" in message


def test_partial_evidence_rejects_artifact_digest_mismatch(tmp_path: Path) -> None:
    data = _copy_partial_evidence_tree(tmp_path)
    data["artifacts"][0]["sha256"] = "sha256:" + "0" * 64
    manifest = tmp_path / "domain" / "evidence" / "core-2-partial-evidence.json"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    valid, message = _validate_core2_partial_evidence(tmp_path)
    assert not valid
    assert "digest mismatch" in message


def test_partial_evidence_rejects_component_status_tampering(tmp_path: Path) -> None:
    data = _copy_partial_evidence_tree(tmp_path)
    data["components"]["OB-04-B"]["status"] = "MACHINE_PROVED"
    manifest = tmp_path / "domain" / "evidence" / "core-2-partial-evidence.json"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    valid, message = _validate_core2_partial_evidence(tmp_path)
    assert not valid
    assert "OB-04-B" in message
    assert "PARTIAL-FORMALIZATION" in message


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
