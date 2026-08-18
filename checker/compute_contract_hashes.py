"""
checker/compute_contract_hashes.py — Compute and freeze contract digests.

Digest scheme:
  statement_digest  = sha256(note field text, UTF-8)
  checker_digest    = sha256(checker/check_certificate.py bytes)
  schema_digest     = sha256(canonical JSON of obligations list)
  evidence digests:
    CORE-0 abc-definition      = sha256("CL-01: ...\nCL-03: ...\nCL-04: ...\n")
    CORE-1 source-dag          = sha256(canonical JSON of module_import_policy)
    CORE-1 assumption-manifest = foundation_hash from policy-v2.json
    CORE-2/3/4 (OBL)           = sha256("OBL: <claim_id> evidence not yet supplied")
    CORE-5 (BLOCKED)           = sha256("BLOCKED: core-5-conclusion fires only when CORE-2/3/4 pass")
"""

from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path


CONTRACTS = [
    "core-0-abc-definition",
    "core-1-provenance-manifest",
    "core-2-height-framework",
    "core-3-key-inequality",
    "core-4-finiteness",
    "core-5-conclusion",
]


def _h(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def compute_all(root: Path) -> dict:
    policy = json.loads((root / "domain" / "policy-v2.json").read_text())
    ledger = json.loads((root / "proof" / "claim-ledger.json").read_text())
    claims = {c["id"]: c for c in ledger["claims"]}

    checker_digest = _h((root / "checker" / "check_certificate.py").read_bytes())

    abc_def_text = (
        f"CL-01: {claims['CL-01']['statement']}\n"
        f"CL-03: {claims['CL-03']['statement']}\n"
        f"CL-04: {claims['CL-04']['statement']}\n"
    )

    result: dict[str, dict] = {}
    stmt_digests: dict[str, str] = {}

    for cname in CONTRACTS:
        d = json.loads((root / "domain" / "contracts" / f"{cname}.json").read_text())
        stmt_digests[cname] = _h(d["note"])
        result[cname] = {
            "statement_digest": stmt_digests[cname],
            "checker_digest": checker_digest,
            "schema_digest": _h(
                json.dumps(d["obligations"], separators=(",", ":"), sort_keys=True)
            ),
        }

    # evidence digests
    result["core-0-abc-definition"]["evidence_abc-definition"] = _h(abc_def_text)
    result["core-1-provenance-manifest"]["evidence_source-dag"] = _h(
        json.dumps(
            policy["module_import_policy"], separators=(",", ":"), sort_keys=True
        )
    )
    result["core-1-provenance-manifest"]["evidence_assumption-manifest"] = policy[
        "foundation_hash"
    ]
    for cid, msg in [
        (
            "core-2-height-framework",
            "OBL: core-2-height-framework evidence not yet supplied",
        ),
        (
            "core-3-key-inequality",
            "OBL: core-3-key-inequality evidence not yet supplied",
        ),
        ("core-4-finiteness", "OBL: core-4-finiteness evidence not yet supplied"),
        (
            "core-5-conclusion",
            "BLOCKED: core-5-conclusion fires only when CORE-2/3/4 pass",
        ),
    ]:
        result[cid][f"evidence_{cid}"] = _h(msg)

    # cross-reference dependency stmt_digests
    result["_cross_refs"] = {f"stmt:{k}": v for k, v in stmt_digests.items()}
    return result


def freeze_contracts(root: Path) -> None:
    hashes = compute_all(root)

    # cross-ref map: placeholder-name -> real hash
    stmt = {k.replace("stmt:", ""): v for k, v in hashes["_cross_refs"].items()}

    replacements = {
        # statement_digest placeholders
        "sha256:PLACEHOLDER-core0-abc-statement-digest-fill-on-freeze": stmt[
            "core-0-abc-definition"
        ],
        "sha256:PLACEHOLDER-core1-abc-statement-digest-fill-on-freeze": stmt[
            "core-1-provenance-manifest"
        ],
        "sha256:PLACEHOLDER-core2-abc-statement-digest-OBL": stmt[
            "core-2-height-framework"
        ],
        "sha256:PLACEHOLDER-core3-abc-statement-digest-OBL": stmt[
            "core-3-key-inequality"
        ],
        "sha256:PLACEHOLDER-core4-abc-statement-digest-OBL": stmt["core-4-finiteness"],
        "sha256:PLACEHOLDER-core5-abc-statement-digest-fill-on-freeze": stmt[
            "core-5-conclusion"
        ],
        # evidence
        "sha256:PLACEHOLDER-abc-definition": hashes["core-0-abc-definition"][
            "evidence_abc-definition"
        ],
        "sha256:PLACEHOLDER-source-dag": hashes["core-1-provenance-manifest"][
            "evidence_source-dag"
        ],
        "sha256:PLACEHOLDER-assumption-manifest": hashes["core-1-provenance-manifest"][
            "evidence_assumption-manifest"
        ],
        "sha256:PLACEHOLDER-height-framework": hashes["core-2-height-framework"][
            "evidence_core-2-height-framework"
        ],
        "sha256:PLACEHOLDER-inequality-proof": hashes["core-3-key-inequality"][
            "evidence_core-3-key-inequality"
        ],
        "sha256:PLACEHOLDER-finiteness-proof": hashes["core-4-finiteness"][
            "evidence_core-4-finiteness"
        ],
        "sha256:PLACEHOLDER-core5-instantiation": hashes["core-5-conclusion"][
            "evidence_core-5-conclusion"
        ],
        # checker (same for all)
        "sha256:PLACEHOLDER-core0-checker": hashes["core-0-abc-definition"][
            "checker_digest"
        ],
        "sha256:PLACEHOLDER-core1-checker": hashes["core-1-provenance-manifest"][
            "checker_digest"
        ],
        "sha256:PLACEHOLDER-core2-checker": hashes["core-2-height-framework"][
            "checker_digest"
        ],
        "sha256:PLACEHOLDER-core3-checker": hashes["core-3-key-inequality"][
            "checker_digest"
        ],
        "sha256:PLACEHOLDER-core4-checker": hashes["core-4-finiteness"][
            "checker_digest"
        ],
        "sha256:PLACEHOLDER-core5-checker": hashes["core-5-conclusion"][
            "checker_digest"
        ],
        # schema
        "sha256:PLACEHOLDER-core0-schema": hashes["core-0-abc-definition"][
            "schema_digest"
        ],
        "sha256:PLACEHOLDER-core1-schema": hashes["core-1-provenance-manifest"][
            "schema_digest"
        ],
        "sha256:PLACEHOLDER-core2-schema": hashes["core-2-height-framework"][
            "schema_digest"
        ],
        "sha256:PLACEHOLDER-core3-schema": hashes["core-3-key-inequality"][
            "schema_digest"
        ],
        "sha256:PLACEHOLDER-core4-schema": hashes["core-4-finiteness"]["schema_digest"],
        "sha256:PLACEHOLDER-core5-schema": hashes["core-5-conclusion"]["schema_digest"],
    }

    for cname in CONTRACTS:
        path = root / "domain" / "contracts" / f"{cname}.json"
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        # validate JSON
        json.loads(text)

    print("All contracts frozen and valid.")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    hashes = compute_all(root)
    clean = {k: v for k, v in hashes.items() if k != "_cross_refs"}
    clean["_cross_refs"] = hashes["_cross_refs"]
    print(json.dumps(clean, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--freeze":
        freeze_contracts(Path(__file__).resolve().parent.parent)
    else:
        main()
