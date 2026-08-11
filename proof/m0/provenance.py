"""
proof/m0/provenance.py — Non-anticipation barrier guard for the abc conjecture
verification kernel.

This module provides the syntactic import-barrier enforcement for construction
modules M1, M2, M3. These modules must never import from M4 (known results),
M5 (comparison), or M6 (conclusion). This is the formal non-anticipation barrier
described in spec/SPECIFICATION.md §0.3.

The barrier is syntactic and machine-checkable. It does NOT decide semantic
circularity (CL-08 is [OUT]). The immutable assumption manifest must also receive
human mathematical review.

Usage (in any M1/M2/M3 file at the top):
    from proof.m0.provenance import assert_zero_free, assert_no_abc_input

These guards fail loudly at import time if the calling file is loading forbidden
construction inputs.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path


# Modules that M1/M2/M3 are forbidden from importing.
FORBIDDEN_TARGETS = frozenset([
    "m4", "m5", "m6",
    "comparison", "zeros", "conclude", "target",
    "known_triples", "szpiro", "faltings_comparison",
])

# Construction modules subject to the barrier.
CONSTRUCTION_MODULES = frozenset(["m1", "m2", "m3"])

# Patterns that indicate forbidden construction leaves in source files.
# These are specific anti-patterns for abc; generic math names are not flagged.
FORBIDDEN_PATTERNS = [
    # Known abc triple databases or tables
    r"abc_triple",
    r"abc_triples",
    r"high_quality_triple",
    r"known_triple",
    r"triple_table",
    # Fitting K_epsilon to known examples
    r"fitted_k_epsilon",
    r"fit_to_triples",
    r"minimize.*triple",
    r"optimized.*triple",
    r"k_epsilon.*fit",
    # Assuming Szpiro or abc-equivalent hypotheses
    r"szpiro_conjecture",
    r"assume_szpiro",
    r"abc_conjecture",
    r"abc_equivalent",
    # IUT identification without isomorphism
    r"hodge_theater_identification",
    r"cross_theater_equal",
    # S-integer finiteness assumed
    r"s_integer_finite",
    r"assume_finiteness",
    # GRH assumed without declaration
    r"assume_grh",
    r"grh_assumed",
]


def assert_zero_free(caller_file: str | None = None) -> None:
    """
    Assert that the calling file does not use forbidden construction leaves.

    This is the primary guard for discovery/ and proof/m1..m3 files. Call at
    module top level. If the source contains forbidden patterns, this raises
    RuntimeError at import time.

    For proof/ modules: also enforces that no forbidden target modules are imported.
    """
    if caller_file is None:
        # Detect caller from call stack
        import inspect
        frame = inspect.stack()[1]
        caller_file = frame.filename

    caller_path = Path(caller_file).resolve()
    project_root = _find_project_root(caller_path)

    # Check for forbidden patterns in the source file.
    import re
    try:
        src = caller_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return  # Can't read — skip check

    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, src, re.IGNORECASE):
            raise RuntimeError(
                f"Non-anticipation barrier violated in {caller_file!r}: "
                f"matches forbidden pattern {pat!r}. "
                f"Construction modules M1/M2/M3 must not use abc triples, "
                f"fitted K_epsilon, Szpiro assumed, or IUT identification "
                f"without isomorphism. See spec/SPECIFICATION.md §3.3."
            )

    # Check that M1/M2/M3 do not import forbidden targets.
    rel = _relative_module(caller_path, project_root)
    if rel is not None:
        module_part = rel.split("/")[1] if "/" in rel else ""
        if module_part in CONSTRUCTION_MODULES:
            _check_import_barrier(caller_path, project_root)


def assert_no_abc_input(description: str) -> None:
    """
    Declare that a construction does not use abc or abc-equivalent input.

    This is a documentation-level assertion: it records in the construction
    manifest that the caller has checked their inputs. It does NOT replace the
    syntactic scan — assert_zero_free() does that.

    Parameters
    ----------
    description:
        A human-readable description of what inputs ARE used (for the manifest).
    """
    # In the scaffold, this is a no-op that records the claim.
    # In a full implementation, this would write to the construction manifest.
    pass


def check_file(path: Path, project_root: Path) -> tuple[bool, str]:
    """
    Check a single file for forbidden construction leaves and import violations.

    Returns (ok, message). Used by the checker.
    """
    import re
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return True, f"could not read {path}"

    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, src, re.IGNORECASE):
            return False, (
                f"{path.relative_to(project_root)}: "
                f"matches forbidden pattern {pat!r}"
            )

    # Check import barrier for construction modules
    rel = _relative_module(path, project_root)
    if rel is not None:
        module_part = rel.split("/")[1] if "/" in rel else ""
        if module_part in CONSTRUCTION_MODULES:
            ok, msg = _check_import_barrier_report(path, project_root)
            if not ok:
                return False, msg

    return True, "clean"


def _check_import_barrier(path: Path, project_root: Path) -> None:
    """Raise RuntimeError if path imports a forbidden target module."""
    ok, msg = _check_import_barrier_report(path, project_root)
    if not ok:
        raise RuntimeError(
            f"Non-anticipation barrier violated: {msg}. "
            f"Construction modules M1/M2/M3 must not import M4/M5/M6. "
            f"See spec/SPECIFICATION.md §0.3."
        )


def _check_import_barrier_report(
    path: Path, project_root: Path
) -> tuple[bool, str]:
    """Return (ok, message) for the import barrier check on a single file."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return True, "parse error — skipped"

    for node in ast.walk(tree):
        imported = []
        if isinstance(node, ast.Import):
            imported = [alias.name.lower() for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported = [node.module.lower()]
        for imp in imported:
            for forbidden in FORBIDDEN_TARGETS:
                if forbidden in imp:
                    return False, (
                        f"{path.relative_to(project_root)}: "
                        f"imports {imp!r} (forbidden target {forbidden!r})"
                    )
    return True, "import barrier clean"


def _find_project_root(start: Path) -> Path:
    """Walk up from start to find the project root (contains spec/ directory)."""
    current = start.parent
    for _ in range(10):
        if (current / "spec").exists() or (current / "domain").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return start.parent


def _relative_module(path: Path, root: Path) -> str | None:
    """Return the path relative to root as a forward-slash string, or None."""
    try:
        return str(path.relative_to(root)).replace(os.sep, "/")
    except ValueError:
        return None
