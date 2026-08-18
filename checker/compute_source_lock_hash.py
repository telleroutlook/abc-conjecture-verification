"""
checker/compute_source_lock_hash.py — Compute the source lock hash for proof/m1/.

The source lock hash is the SHA-256 of the concatenation of all .py files in
proof/m1/ in lexicographic order by repo-relative path, formatted as:

    path: <relative_path>
    content:
    <file_content>
    ---

This hash is frozen in domain/policy-v2.json as source_lock_hash, certifying
that the M1 arithmetic source was constructed and locked before any comparison
or conclusion module (M4/M5/M6) content is introduced.

Usage:
    python3 checker/compute_source_lock_hash.py
    # prints: sha256:<hex>
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def compute_source_lock_hash(project_root: Path) -> str:
    m1_dir = project_root / "proof" / "m1"
    if not m1_dir.exists():
        return "sha256:" + "0" * 64

    py_files = sorted(
        (p for p in m1_dir.rglob("*.py") if not p.name.startswith("__")),
        key=lambda p: str(p.relative_to(project_root)),
    )

    parts: list[str] = []
    for py in py_files:
        rel = str(py.relative_to(project_root))
        content = py.read_text(encoding="utf-8")
        parts.append(f"path: {rel}\ncontent:\n{content}\n---\n")

    canonical = "".join(parts)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    print(compute_source_lock_hash(root))


if __name__ == "__main__":
    main()
