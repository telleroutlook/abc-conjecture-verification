"""
checker/compute_foundation_hash.py — Compute the foundation hash for domain/policy-v2.json.

The foundation hash is the SHA-256 of the concatenated canonical texts of the
admitted BASE statements, in claim-id lexicographic order.

Canonical text format:
    "<claim-id>: <statement>\n"
    (one line per BASE claim, trailing newline)

This is reproducible: given the same BASE claims in the ledger, any independent
implementation produces the same hash.

Usage:
    python3 checker/compute_foundation_hash.py
    # prints: sha256:<hex>
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def canonical_base_text(ledger: dict) -> str:
    base_claims = sorted(
        (c for c in ledger["claims"] if c["status"] == "BASE"),
        key=lambda c: c["id"],
    )
    lines = [f"{c['id']}: {c['statement']}" for c in base_claims]
    return "\n".join(lines) + "\n"


def compute_foundation_hash(ledger_path: Path) -> str:
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    text = canonical_base_text(ledger)
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ledger_path = root / "proof" / "claim-ledger.json"
    if not ledger_path.exists():
        sys.stderr.write(f"Ledger not found: {ledger_path}\n")
        sys.exit(1)
    h = compute_foundation_hash(ledger_path)
    print(h)


if __name__ == "__main__":
    main()
