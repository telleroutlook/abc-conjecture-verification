"""
proof/m1/heights.py — Height framework scaffold (M1 module).

This module provides the conceptual framework for Weil heights, logarithmic
heights, and the discriminant height of Frey curves, as needed for the abc key
inequality (CL-09 / CORE-2).

NOTE on terminology (established by OB-03 independent review, 2026-08-15):
  h_Delta(E) := (1/12) * log|Delta_min(E)|   is the "discriminant height".
  The true Faltings height (Arakelov-theoretic) also contains an archimedean
  period term; the two are NOT equal and must NOT be conflated.

STATUS: SCAFFOLD. These are definitions and structural descriptions, not
a completed proof of P_height. The CONSTRUCTION_STATUS constant records
the honest state.

This module may import only from proof.m0 and proof.m1.rad (non-anticipation barrier B1).
No forbidden construction leaves (barrier B2).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from proof.m0.provenance import assert_zero_free, assert_no_abc_input
from proof.m1.rad import rad

assert_zero_free(__file__)
assert_no_abc_input(
    "Height framework is defined from first principles. "
    "No known abc examples, no fitted K_epsilon, no Szpiro equivalence assumed as input."
)

HEIGHT_FRAMEWORK_STATUS = "SCAFFOLD"

# ── Weil height (projective) ──────────────────────────────────────────────────


def weil_height_rational(p: int, q: int) -> float:
    """
    Weil height of a rational number p/q (in lowest terms).

    H(p/q) = max(|p|, |q|) for p/q in lowest terms.
    Logarithmic Weil height: h(p/q) = log(max(|p|, |q|)).

    This is the naive height on P^1(Q); the absolute logarithmic Weil height
    is the normalised version used in Arakelov geometry.
    """
    from math import gcd
    if q == 0:
        raise ValueError("denominator must be nonzero")
    g = gcd(abs(p), abs(q))
    p, q = abs(p) // g, abs(q) // g
    return max(p, q)


def log_weil_height_rational(p: int, q: int) -> float:
    """log H(p/q) = log(max(|p_reduced|, |q_reduced|))."""
    return math.log(weil_height_rational(p, q))


# ── Frey curve associated to a coprime triple ─────────────────────────────────


@dataclass
class FreyCurveData:
    """
    Data associated to the Frey curve E_{a,b,c}: y^2 = x(x - a)(x + b)
    for a coprime triple a + b = c with a odd, b even (a, b, c > 0, gcd(a,b)=1).

    Exact Weierstrass invariants (proved in OB-03 independent review, 2026-08-15;
    source: Silverman, AEC 2nd ed., Chapter III §1):
      a1=0, a2=b-a, a3=0, a4=-ab, a6=0
      b2 = 4(b-a),  b4 = -2ab,  b6 = 0,  b8 = -(ab)^2
      c4 = 16(a^2 + ab + b^2)
      Delta = 16(abc)^2          (exact identity, no O(1) error)
      Delta_min = 2^(4-12s) * (abc)^2,  s in {0,1}

    Discriminant height (NOT the Faltings height):
      h_Delta(E) := (1/12) * log|Delta_min|
                 <= (1/6) * log(abc) + (1/3) * log(2)      [OB-03-B, proved]

    Conductor bound (proved in OB-03-C, using Tate algorithm + Silverman ATEC IV.10.4):
      N_E <= 2^7 * rad(abc)
    Equivalently: log N_E <= log(rad(abc)) + 7*log(2).
    The divisibility claim "N_E | rad(abc)^2" is FALSE; (1,8,9) is a counterexample
    (N_E=48, rad(abc)^2=36).

    KEY STEP (unproved — content of Szpiro's conjecture, equivalent to abc):
    Bounding log|Delta| / log N_E uniformly for all coprime triples.
    """
    a: int
    b: int
    c: int
    rad_abc: int

    def __post_init__(self) -> None:
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            raise ValueError("Frey curve requires positive a, b, c")
        if self.a + self.b != self.c:
            raise ValueError(f"Require a + b = c, got {self.a} + {self.b} != {self.c}")

    @classmethod
    def from_triple(cls, a: int, b: int, c: int) -> "FreyCurveData":
        return cls(a=a, b=b, c=c, rad_abc=rad(a) * rad(b) * rad(c))

    def discriminant_schematic(self) -> int:
        """Exact discriminant Delta = 16*(abc)^2 of the displayed integral model."""
        return 16 * (self.a * self.b * self.c) ** 2

    def log_discriminant_schematic(self) -> float:
        return math.log(self.discriminant_schematic())

    def conductor_upper_bound(self) -> int:
        """
        Conductor upper bound: N_E <= 2^7 * rad(abc).

        Proved unconditionally in OB-03-C (Tate algorithm + Silverman ATEC
        Theorem IV.10.4).  The false claim "N_E | rad(abc)^2" has been removed;
        (a,b,c)=(1,8,9) is an explicit counterexample (N_E=48 > rad(abc)^2=36).

        STATUS: structural framework; the bound is proved for a odd, b even triples.
        """
        return (2 ** 7) * self.rad_abc

    def log_conductor_upper_bound(self) -> float:
        return math.log(self.conductor_upper_bound())

    def schematic_szpiro_ratio(self) -> float:
        """
        Schematic Szpiro ratio: log|Delta| / log(conductor_upper_bound).

        STATUS: uses schematic values.  Not a proof that the ratio is bounded.
        Bounding this uniformly for all coprime triples is Szpiro's conjecture (abc).
        """
        log_d = self.log_discriminant_schematic()
        log_n = self.log_conductor_upper_bound()
        if log_n == 0:
            return float('inf')
        return log_d / log_n


# ── Faltings height (conceptual definition) ───────────────────────────────────


@dataclass
class FaltingsHeightScaffold:
    """
    Conceptual scaffold for heights of an elliptic curve.

    TERMINOLOGY (corrected per OB-03 review, 2026-08-15):
      h_Delta(E) := (1/12)*log|Delta_min(E)|  is the DISCRIMINANT height.
      The TRUE Faltings height (Arakelov-theoretic) additionally contains the
      archimedean period term; the two differ and must not be conflated.
      Reference: de Jong–Shokrieh (2022) §1.4, citing Faltings (1984) Thm 7 /
      Silverman (1986) Prop 1.1.

    The Faltings finiteness theorem (CL-05, BASE): for any number field K
    and bound B, {E/K : h_F(E) <= B} is finite up to K-isomorphism.

    For the key inequality, we need a bound of the form:
       h_F(E_{a,b,c}) <= (1+ε) * log rad(abc) + C_ε
    for all coprime triples (not just a fixed prime set S).
    Establishing this uniformly is the content of CORE-2 (P_height, CL-09 [OBL]).

    STATUS: SCAFFOLD. Height defined conceptually; actual computation of h_F
    requires Arakelov intersection theory and goes beyond the current module.
    """
    frey_data: FreyCurveData
    status: str = HEIGHT_FRAMEWORK_STATUS

    def height_upper_bound_schematic(self, epsilon: float) -> Optional[float]:
        """
        Schematic upper bound on h_F(E_{a,b,c}).

        Returns: (1+epsilon) * log(rad_abc) as a target bound.
        This is the GOAL of CORE-2 (CL-09), not a proved result.

        Returns None if the bound cannot be computed (e.g., rad_abc = 1).
        """
        if self.frey_data.rad_abc <= 0:
            return None
        return (1.0 + epsilon) * math.log(self.frey_data.rad_abc)

    def height_framework_complete(self) -> bool:
        """
        Returns False: the Faltings height framework is not yet complete.
        CORE-2 (CL-09) remains [OBL].
        """
        return False
