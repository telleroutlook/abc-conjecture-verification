"""
proof/m1/heights.py — Faltings height framework scaffold (M1 module).

This module provides the conceptual framework for Weil heights, logarithmic
heights, and Faltings heights as needed for the abc key inequality (CL-09 / CORE-2).

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
    for a coprime triple a + b = c (a, b, c > 0, gcd(a,b) = gcd(b,c) = gcd(a,c) = 1).

    This curve was introduced by Frey (1986) to relate the abc conjecture
    to elliptic curves. The key properties:

      discriminant: Delta = (abc)^2 * 2^4  (up to 6th-power factors from the minimal model)
      j-invariant:  j = 2^8 * (a^2 - ab + b^2)^3 / (abc)^2  (schematic)
      conductor:    N_E | rad(abc)^2  (this is what would need to be proved for the key inequality)

    For the abc conjecture, the relevant bound is:
      log|Delta| ~ 2 log c  (since Delta ~ (abc)^2 and c ~ ab for large c)
      log N_E ~ 2 log rad(abc)
    so the Szpiro ratio ~ log|Delta| / log N_E ~ log c / log rad(abc),
    and bounding this ratio is equivalent to the abc conjecture.

    STATUS: This is a framework scaffold. The conductor bound N_E | rad(abc)^2
    is known (Ogg-Szpiro formula, conditional on semistable reduction), but the
    KEY STEP — bounding log|Delta| / log N_E uniformly — is the content of
    Szpiro's conjecture, which is equivalent to abc and is unproved over the integers.
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
        """Schematic discriminant Δ = 16 * (abc)^2. Not the minimal model discriminant."""
        return 16 * self.a * self.b * self.c

    def log_discriminant_schematic(self) -> float:
        return math.log(self.discriminant_schematic())

    def conductor_upper_bound(self) -> int:
        """
        Conductor upper bound: N_E divides rad(abc)^2.

        This is a structural bound from the theory of elliptic curves
        (the conductor is supported on the primes of bad reduction,
        which are the primes dividing abc, hence dividing rad(abc)).
        The exact exponent in the conductor formula requires the full
        Ogg-Szpiro formula and semistable reduction theory.

        STATUS: structural framework; not a complete proof.
        """
        return self.rad_abc ** 2

    def log_conductor_upper_bound(self) -> float:
        return math.log(self.conductor_upper_bound())

    def schematic_szpiro_ratio(self) -> float:
        """
        Schematic Szpiro ratio: log|Δ| / log N_E  (using upper bounds).

        For the abc conjecture, this ratio needs to be bounded uniformly.
        A bound of (1+ε) on this ratio for all but finitely many curves
        is equivalent to Szpiro's conjecture (and hence abc).

        STATUS: This function computes the ratio using schematic values.
        It is NOT a proof that the ratio is bounded.
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
    Conceptual scaffold for the Faltings height of an elliptic curve.

    The Faltings height h_F(E) is defined via the Arakelov intersection
    pairing on the arithmetic surface associated to the Néron model of E.
    It satisfies the Faltings-Parshin finiteness theorem: for any number
    field K and any bound B, the set
       {E/K : h_F(E) <= B}
    is finite (up to K-isomorphism). This is Faltings theorem (CL-05, BASE).

    For the key inequality, we need a bound of the form:
       h_F(E_{a,b,c}) <= (1+ε) * log rad(abc) + C_ε
    for all but finitely many abc triples. Establishing this bound
    uniformly (for ALL coprime triples, not just a fixed prime set)
    is the content of CORE-2 (P_height, CL-09 [OBL]).

    STATUS: SCAFFOLD. The height is defined conceptually here;
    actual computation of h_F requires Arakelov intersection theory
    and goes beyond the current module.
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
