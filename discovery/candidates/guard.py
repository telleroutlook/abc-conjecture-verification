"""
discovery/candidates/guard.py — Non-anticipation barrier guard for discovery layer.

Discovery candidates MUST call assert_zero_free() at the top of every file.
Constructions that read known abc triples, fit K_epsilon, or use abc-equivalent
assertions fail at import time.

This module is separate from proof/m0/provenance.py (which is in the certified
construction graph). Discovery is UNTRUSTED and never imported by proof/ or checker/.
"""

from __future__ import annotations

import re
from pathlib import Path


FORBIDDEN_PATTERNS = [
    r"abc_triple",
    r"abc_triples",
    r"high_quality_triple",
    r"known_triple",
    r"triple_table",
    r"fitted_k_epsilon",
    r"fit_to_triples",
    r"minimize.*triple",
    r"k_epsilon.*fit",
    r"assume_szpiro",
    r"szpiro_conjecture",
    r"assume_abc",
    r"abc_equivalent",
    r"hodge_theater_identification",
    r"cross_theater_equal",
    r"s_integer_finite",
    r"assume_finiteness",
    r"assume_grh",
    r"grh_assumed",
]


def assert_zero_free(caller_file: str | None = None) -> None:
    """
    Assert that the calling discovery candidate does not use forbidden patterns.

    Call at the top of every file in discovery/candidates/. Raises RuntimeError
    at import time if a forbidden pattern is found.
    """
    if caller_file is None:
        import inspect
        frame = inspect.stack()[1]
        caller_file = frame.filename

    path = Path(caller_file).resolve()
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, src, re.IGNORECASE):
            raise RuntimeError(
                f"Discovery non-circularity guard violated in {caller_file!r}: "
                f"matches forbidden pattern {pat!r}. "
                f"Discovery candidates must not use known abc triples, fitted K_epsilon, "
                f"Szpiro assumed, or abc-equivalent constructions. "
                f"See spec/SPECIFICATION.md §3.3 and CLAUDE.md discovery layer rules."
            )
