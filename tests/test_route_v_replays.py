"""Replay the finite evidence scripts cited by the Route V paper."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "discovery" / "m2_directions"


def replay(name: str) -> str:
    path = SCRIPT_DIR / name
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_t30_rho_distribution_replays() -> None:
    output = replay("t30_rho_distribution.py")
    assert "Total squarefree coprime triples" in output
    assert "SUMMARY (F19)" in output


def test_paper_omega_table_matches_t30_replay() -> None:
    output = replay("t30_rho_distribution.py")
    total_match = re.search(
        r"Total squarefree coprime triples \(3 ≤ ω, c ≤ 1000\): ([0-9]+)",
        output,
    )
    assert total_match is not None
    total = int(total_match.group(1))

    statistics = output.split("Statistics by ω:", 1)[1].split(
        "Bounded-type ρ concentration", 1
    )[0]
    script_counts = {
        int(omega): int(count)
        for omega, count in re.findall(
            r"^\s*([0-9]+)\s+([0-9]+)\s+", statistics, re.MULTILINE
        )
    }

    tex = (REPO_ROOT / "papers" / "route-v-pasten" / "route-v-pasten.tex").read_text()
    table = tex.split(r"\label{tab:data}", 1)[0].rsplit(r"\begin{tabular}", 1)[1]
    paper_counts = {
        int(omega): int(count.replace(r"\,", "").replace(",", ""))
        for omega, count in re.findall(
            r"^\s*([0-9]+)\s*&\s*([0-9\\,]+)\s*&", table, re.MULTILINE
        )
    }

    assert paper_counts == script_counts
    assert sum(paper_counts.values()) == total


def test_t82_type311_mirror_case_replays() -> None:
    output = replay("t82_nd_type311_verify.py")
    assert "Type (3,1,1) triples found: 843" in output
    assert "Results: 843 OK, 0 FAIL" in output


def test_t95_merged_minima_conjecture_refutation_replays() -> None:
    output = replay("t95_all_successive_minima.py")
    assert "MISMATCH (2,13,15)" in output
    assert "MISMATCH (3,7,10)" in output
    assert "T95 REFUTATION REPLAYED" in output


def test_t96_edge_case_search_replays() -> None:
    output = replay("t96_edge_case_both_small_in_Pb.py")
    assert "Found 2 edge-case triples" in output
    assert "OB-15 violations: 0" in output
