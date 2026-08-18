"""Keep the bridge checker digest synchronized across proofctl mirrors."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_IDS = [
    "core-0-abc-definition",
    "core-1-provenance-manifest",
    "core-2-height-framework",
    "core-3-key-inequality",
    "core-4-finiteness",
    "core-5-conclusion",
]


def test_domain_and_proofctl_contracts_pin_current_checker() -> None:
    expected = (
        "sha256:"
        + hashlib.sha256(
            (REPO_ROOT / "checker" / "check_certificate.py").read_bytes()
        ).hexdigest()
    )
    for directory in ("domain/contracts", ".proofctl/contracts"):
        for claim_id in CONTRACT_IDS:
            path = REPO_ROOT / directory / f"{claim_id}.json"
            contract = json.loads(path.read_text(encoding="utf-8"))
            actual = contract["checker"]["checker_digest"]
            assert actual == expected, f"{path}: {actual} != {expected}"


def test_domain_and_proofctl_graphs_pin_current_checker() -> None:
    expected = (
        "sha256:"
        + hashlib.sha256(
            (REPO_ROOT / "checker" / "check_certificate.py").read_bytes()
        ).hexdigest()
    )
    for relative in ("graph.json", ".proofctl/graph.json"):
        graph = json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))
        pins = {
            checker["checker_digest"]
            for checker in graph.get("checkers", [])
            if checker.get("id") == "abccv-bridge-v1"
        }
        assert pins == {expected}, f"{relative}: {pins} != {expected}"
