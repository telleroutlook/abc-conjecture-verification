"""
proof/m1/arithmetic_geometry.py — Arithmetic geometry setup for the key inequality scaffold (M1).

This module provides the structural setup for the connection between
the abc conjecture and elliptic curve arithmetic geometry. It defines
the Frey curve framework and the relationships needed for the key inequality.

STATUS: SCAFFOLD. This is the setup layer; the actual proof of the
key inequality c <= K_eps * rad(abc)^(1+eps) is CORE-3 ([OBL]).

This module may import only from proof.m0, proof.m1.rad, proof.m1.heights.
Non-anticipation barrier B1 strictly enforced.
No forbidden construction leaves (barrier B2).
"""

from __future__ import annotations

import math
from typing import NamedTuple

from proof.m0.provenance import assert_zero_free, assert_no_abc_input
from proof.m1.rad import rad, rad_triple
from proof.m1.heights import FreyCurveData, FaltingsHeightScaffold, HEIGHT_FRAMEWORK_STATUS

assert_zero_free(__file__)
assert_no_abc_input(
    "Arithmetic geometry framework built from first principles: "
    "Frey curve structure, discriminant formula, conductor divisibility. "
    "No abc examples used as input, no parameters fitted to examples."
)

CONSTRUCTION_STATUS = (
    "SCAFFOLD: The arithmetic geometry framework is in place. "
    "The key inequality c <= K_eps * rad(abc)^(1+eps) is NOT proved here. "
    "CORE-2 (P_height, CL-09) and CORE-3 (P_ineq, CL-10) remain [OBL]. "
    "Two routes to the inequality exist: "
    "(A) Szpiro's conjecture / Arakelov intersection theory — equivalent to abc, unproved over Z; "
    "(B) Mochizuki IUT — requires independent verification of Corollary 3.12 "
    "(OPEN: Scholze-Stix objection)."
)


class FreyCurveInvariants(NamedTuple):
    """
    Arithmetic invariants of the Frey curve E_{a,b,c}: y^2 = x(x-a)(x+b).

    For a coprime triple a + b = c:
      - discriminant: Delta = 16 * (abc)^2  (schematic; minimal model differs by 6th powers)
      - conductor:    N_E | rad(abc)^2  (divisibility; exact exponent from Ogg formula)
      - rad_abc:      rad(a)*rad(b)*rad(c)
    """
    a: int
    b: int
    c: int
    discriminant: int
    conductor_upper_bound: int
    rad_abc: int


def frey_curve_discriminant(a: int, b: int, c: int) -> int:
    """
    Schematic discriminant of the Frey curve y^2 = x(x-a)(x+b).

    Delta = 16 * (abc)^2.

    Note: The minimal model discriminant differs by a 6th power factor
    depending on the 2-adic valuation. For the key inequality, what matters
    is that log|Delta| ~ 2*log(c) + O(log rad(abc)), which is the dominant term.

    This is a framework definition; the precise Arakelov computation
    is required for CORE-2.
    """
    return 16 * a * b * c


def frey_curve_conductor_upper_bound(a: int, b: int, c: int) -> int:
    """
    Upper bound on the conductor N_E of the Frey curve E_{a,b,c}.

    N_E | rad(abc)^2.

    The conductor of E_{a,b,c} is supported on primes dividing abc,
    i.e., the primes in rad(abc). Each such prime contributes at most
    exponent 2 to the conductor (from the Ogg-Szpiro formula for
    semistable reduction). Hence N_E | rad(abc)^2.

    STATUS: This divisibility is structural, not proved as a tight bound here.
    The exact conductor requires the full Ogg-Szpiro formula.
    """
    r = rad_triple(a, b, c)
    return r * r


def compute_frey_invariants(a: int, b: int, c: int) -> FreyCurveInvariants:
    """Compute all key invariants for a Frey curve triple."""
    return FreyCurveInvariants(
        a=a,
        b=b,
        c=c,
        discriminant=frey_curve_discriminant(a, b, c),
        conductor_upper_bound=frey_curve_conductor_upper_bound(a, b, c),
        rad_abc=rad_triple(a, b, c),
    )


def key_inequality_target(a: int, b: int, c: int, epsilon: float, K_eps: float) -> bool:
    """
    Check the KEY INEQUALITY: c <= K_eps * rad(abc)^(1+epsilon).

    This function defines the GOAL of CORE-3 (P_ineq, CL-10 [OBL]).
    It does NOT prove the inequality; it checks whether a given K_eps
    satisfies it for a specific triple.

    Used in:
    - CORE-2 framework: defining what P_height must establish
    - discovery/ layer: exploring candidate K_eps values (untrusted)

    WARNING: Evaluating this on known examples does NOT constitute a proof.
    The inequality must hold for ALL coprime a+b=c (spec B3, §2.1).
    """
    r = rad_triple(a, b, c)
    return c <= K_eps * (r ** (1.0 + epsilon))


def log_height_inequality_gap(a: int, b: int, c: int, epsilon: float) -> float:
    """
    Logarithmic form of the height inequality gap:
      gap = log(c) - (1+epsilon) * log(rad(abc))

    If gap > 0: the triple would require K_eps >= exp(gap) to satisfy the inequality.
    The abc conjecture (for this epsilon) asserts: gap is bounded above for all
    coprime triples (i.e., there exists K_eps such that c <= K_eps * rad(abc)^(1+eps)
    for all but finitely many).

    This function computes the gap — it does NOT prove it is bounded.
    """
    r = rad_triple(a, b, c)
    if r <= 0:
        return float('inf')
    return math.log(c) - (1.0 + epsilon) * math.log(r)


def obstruction_summary() -> str:
    """Return a human-readable summary of the current construction obstruction."""
    return (
        "KEY INEQUALITY OBSTRUCTION (CORE-3, CL-10 [OBL]):\n"
        "\n"
        "Route A: Algebraic geometry / Szpiro.\n"
        "  To prove c <= K_eps * rad(abc)^(1+eps), one approach bounds\n"
        "  the Faltings height h_F(E_{a,b,c}) in terms of the conductor N_E,\n"
        "  then uses N_E | rad(abc)^2 to obtain the abc bound.\n"
        "  OBSTRUCTION: Bounding h_F(E) / log(N_E) uniformly is equivalent to\n"
        "  Szpiro's conjecture over Z, which is equivalent to abc (CL-02, BASE).\n"
        "  This route is CIRCULAR under B2.\n"
        "\n"
        "Route B: Mochizuki IUT.\n"
        "  OBSTRUCTION: core3.iut-corollary-312-independently-verified is OPEN.\n"
        "  Scholze-Stix (2018): objects in different Hodge theaters are identified\n"
        "  without a proved explicit isomorphism. Until a machine-replayed formal\n"
        "  proof of Corollary 3.12 is supplied, this gate remains OPEN.\n"
        "\n"
        "This obstruction is formally recorded in proof/m2/key_inequality_obstruction.json."
    )
