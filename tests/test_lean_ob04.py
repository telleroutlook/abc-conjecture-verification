"""Replay and audit the OB-04 Lean formalization boundary."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEAN_ROOT = REPO_ROOT / "lean"
LEAN_FILE = LEAN_ROOT / "AbcHeightKernel.lean"


def test_ob04_source_declares_expected_theorems_and_admitted_premises() -> None:
    source = LEAN_FILE.read_text(encoding="utf-8")
    for declaration in (
        "theorem intRad_abs",
        "theorem rad_prime_pow",
        "theorem rad_mul_coprime",
        "theorem intRad_mul_coprime",
        "theorem rad_pos",
        "theorem frey_disc_height_bound",
        "theorem conductor_log_bound",
        "theorem frey_conductor_log_bound",
        "theorem quality_above_one",
    ):
        assert declaration in source
    assert "axiom silverman_frey_disc_cases" in source
    assert "axiom freyConductor" in source
    assert "axiom frey_conductor_formula" in source
    assert "Silverman AEC 2nd ed. (2009), Lemma VIII.11.3(a)" in source
    assert "Silverman ATEC (1994), Theorem IV.10.4" in source


def test_ob04_axiom_audit_replays() -> None:
    result = subprocess.run(
        [str(Path.home() / ".elan" / "bin" / "lake"), "env", "lean", "AbcHeightKernel.lean"],
        cwd=LEAN_ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = result.stdout + result.stderr
    assert "error:" not in output

    def axioms(name: str) -> set[str]:
        match = re.search(rf"'{name}' depends on axioms: \[([^\]]*)\]", output)
        assert match is not None, f"missing #print axioms output for {name}"
        return {item.strip() for item in match.group(1).split(",")}

    standard = {"propext", "Classical.choice", "Quot.sound"}
    for name in (
        "intRad_abs",
        "rad_prime_pow",
        "rad_mul_coprime",
        "intRad_mul_coprime",
        "rad_pos",
        "conductor_log_bound",
        "quality_above_one",
    ):
        assert axioms(name) == standard, name

    assert axioms("frey_disc_height_bound") == standard | {
        "silverman_frey_disc_cases"
    }
    assert axioms("frey_conductor_log_bound") == standard | {
        "freyConductor",
        "frey_conductor_formula",
    }
    assert "sorryAx" not in output
