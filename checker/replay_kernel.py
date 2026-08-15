"""
checker/replay_kernel.py — Offline replay verifier for abc proof certificates.

Loads proof certificate JSON files from proof/ and verifies them against the
claim ledger. This is the offline replay component described in PLAN.md §P2.

Protocol:
  - No network access
  - No subprocess execution
  - No trusted PASS fields — verdicts are derived by structural checks
  - No PLACEHOLDER strings allowed in any certificate

Certificate format: abc-proof-term-v1 (JSON, stored in proof/**/*.json)

Usage:
    python3 checker/replay_kernel.py
    # prints: JSON replay report
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

CERT_FORMAT = "abc-proof-term-v1"

# Claims expected as THM in the ledger; must have proof certificates.
THM_CLAIMS = {"CL-03", "CL-04", "CL-07"}

# Where proof certificates live, keyed by claim_id.
CERT_PATHS: dict[str, str] = {
    "CL-03": "proof/m6/cl03_implication.json",
    "CL-04": "proof/m6/cl04_honesty.json",
    "CL-07": "proof/m0/cl07_syntactic.json",
    "source-lock-m1": "proof/m0/source_lock.json",
}

# Status values that are permitted as premise status.
VALID_PREMISE_STATUSES = {"DEF", "BASE", "THM"}


def _digest(msg: str) -> str:
    return "sha256:" + hashlib.sha256(msg.encode("utf-8")).hexdigest()


def _check_no_placeholder(cert: Any, path: str) -> list[str]:
    """Return error messages for any PLACEHOLDER strings in the certificate."""
    raw = json.dumps(cert)
    errors: list[str] = []
    if "PLACEHOLDER" in raw:
        errors.append(f"{path}: contains PLACEHOLDER string")
    return errors


def _check_structure(cert: dict, path: str) -> list[str]:
    """Verify required top-level fields are present and consistent."""
    errors: list[str] = []
    required = [
        "certificate_format",
        "claim_id",
        "statement",
        "module",
        "proof_kind",
        "premises",
        "proof_steps",
        "qed_claim",
        "forbidden_inputs_used",
        "non_circularity",
    ]
    for field in required:
        if field not in cert:
            errors.append(f"{path}: missing required field {field!r}")

    if "certificate_format" in cert and cert["certificate_format"] != CERT_FORMAT:
        errors.append(
            f"{path}: unknown certificate_format {cert['certificate_format']!r}; "
            f"expected {CERT_FORMAT!r}"
        )

    if "claim_id" in cert and "qed_claim" in cert:
        if cert["claim_id"] != cert["qed_claim"]:
            errors.append(
                f"{path}: claim_id {cert['claim_id']!r} != qed_claim {cert['qed_claim']!r}"
            )

    return errors


def _check_proof_steps(cert: dict, path: str) -> list[str]:
    """Verify each proof step has a step number and justification."""
    errors: list[str] = []
    steps = cert.get("proof_steps", [])
    if not steps:
        errors.append(f"{path}: proof_steps is empty")
        return errors

    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"{path}: proof_steps[{i}] is not a dict")
            continue
        if "step" not in step:
            errors.append(f"{path}: proof_steps[{i}] missing 'step' field")
        if "justification" not in step or not step["justification"]:
            errors.append(
                f"{path}: proof_steps[{i}] missing or empty 'justification' field"
            )
        if "label" not in step:
            errors.append(f"{path}: proof_steps[{i}] missing 'label' field")
        if "claim" not in step:
            errors.append(f"{path}: proof_steps[{i}] missing 'claim' field")

    return errors


def _check_premises(cert: dict, ledger: dict, path: str) -> list[str]:
    """Verify declared premises are DEF/BASE/THM in the ledger."""
    errors: list[str] = []
    premises = cert.get("premises", [])
    ledger_index = {c["id"]: c for c in ledger.get("claims", [])}

    for p in premises:
        if not isinstance(p, dict):
            errors.append(f"{path}: invalid premise entry: {p!r}")
            continue
        pid = p.get("claim_id", "")
        declared_status = p.get("status", "")

        # Premises starting with "def-" are definitional axioms not in the ledger;
        # accept them if declared as DEF.
        if pid.startswith("def-"):
            if declared_status != "DEF":
                errors.append(
                    f"{path}: premise {pid!r} declared as {declared_status!r}; "
                    f"definitional premises must be DEF"
                )
            continue

        if pid not in ledger_index:
            errors.append(
                f"{path}: premise {pid!r} not found in claim ledger"
            )
            continue

        ledger_status = ledger_index[pid]["status"]
        if ledger_status not in VALID_PREMISE_STATUSES:
            errors.append(
                f"{path}: premise {pid!r} has status {ledger_status!r} in ledger; "
                f"must be DEF/BASE/THM to be used as a premise"
            )

        if declared_status and declared_status != ledger_status:
            errors.append(
                f"{path}: premise {pid!r} declared as {declared_status!r} but "
                f"ledger says {ledger_status!r}"
            )

    return errors


def _check_forbidden_inputs(cert: dict, path: str) -> list[str]:
    """Verify no forbidden inputs are declared."""
    errors: list[str] = []
    forbidden = cert.get("forbidden_inputs_used", None)
    if forbidden is None:
        errors.append(f"{path}: missing 'forbidden_inputs_used' field")
    elif not isinstance(forbidden, list):
        errors.append(f"{path}: 'forbidden_inputs_used' must be a list")
    elif len(forbidden) > 0:
        errors.append(
            f"{path}: 'forbidden_inputs_used' is non-empty: {forbidden!r}; "
            f"proof certificates must not use forbidden inputs"
        )
    return errors


def verify_certificate(cert_path: Path, ledger: dict) -> dict:
    """
    Verify a single proof certificate file.

    Returns a verdict dict:
      {claim_id, path, verdict ('pass'|'fail'), errors, content_digest}
    """
    path_str = str(cert_path)
    errors: list[str] = []

    try:
        raw = cert_path.read_text(encoding="utf-8")
        cert = json.loads(raw)
    except FileNotFoundError:
        return {
            "claim_id": None,
            "path": path_str,
            "verdict": "fail",
            "errors": [f"{path_str}: file not found"],
            "content_digest": None,
        }
    except json.JSONDecodeError as e:
        return {
            "claim_id": None,
            "path": path_str,
            "verdict": "fail",
            "errors": [f"{path_str}: JSON parse error: {e}"],
            "content_digest": None,
        }

    content_digest = _digest(raw)

    errors += _check_no_placeholder(cert, path_str)
    errors += _check_structure(cert, path_str)
    errors += _check_proof_steps(cert, path_str)
    errors += _check_premises(cert, ledger, path_str)
    errors += _check_forbidden_inputs(cert, path_str)

    claim_id = cert.get("claim_id")
    verdict = "fail" if errors else "pass"
    return {
        "claim_id": claim_id,
        "path": path_str,
        "verdict": verdict,
        "errors": errors,
        "content_digest": content_digest,
    }


def replay_all_thm_certificates(project_root: Path) -> dict:
    """
    Replay all [THM] proof certificates and return a summary report.

    Returns:
      {
        "all_pass": bool,
        "results": [...],     # one per THM claim
        "missing": [...],     # claim_ids with no certificate found
      }
    """
    ledger_path = project_root / "proof" / "claim-ledger.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "all_pass": False,
            "results": [],
            "missing": list(THM_CLAIMS),
            "error": f"Failed to load ledger: {e}",
        }

    results: list[dict] = []
    missing: list[str] = []

    for claim_id, rel_path in CERT_PATHS.items():
        cert_path = project_root / rel_path
        if not cert_path.exists():
            missing.append(claim_id)
            results.append({
                "claim_id": claim_id,
                "path": str(cert_path),
                "verdict": "fail",
                "errors": [f"Certificate file not found: {rel_path}"],
                "content_digest": None,
            })
            continue
        result = verify_certificate(cert_path, ledger)
        if result.get("claim_id") is None:
            result["claim_id"] = claim_id
        results.append(result)

    all_pass = all(r["verdict"] == "pass" for r in results) and not missing
    return {
        "all_pass": all_pass,
        "results": results,
        "missing": missing,
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report = replay_all_thm_certificates(root)
    print(json.dumps(report, indent=2))
    if not report["all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
