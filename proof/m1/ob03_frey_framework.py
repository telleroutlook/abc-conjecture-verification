"""proof/m1/ob03_frey_framework.py — Exact executable checks for the OB-03 framework.

Source: independent referee review of OB-03, 2026-08-15.
Review document: outsource/reviews/OB-03-review-2026-08-15.md

This module uses only the Python standard library.  It supplies exact integer
computations and regression checks for the corrected OB-03-A through OB-03-D claims.
The accompanying referee report contains the universal mathematical proofs;
doctests here verify specific computations, not the full universal statements.

Non-anticipation: no imports from M2/M3/M4/M5/M6; no abc triples used as
construction inputs; no Szpiro or IUT assumed (barrier B1, B2).

Corrected constants established by the review:
  C  = (1/3)*log(2)   for the discriminant height bound (OB-03-B)
  C2 = 7*log(2)       for the conductor bound (OB-03-C)
  Conductor bound: N_E <= 2^7 * rad(abc)   (not N_E | rad(abc)^2, which is false)
  Discriminant:    Delta = 16*(abc)^2       (exact, no O(1) error)

Basic radical examples:

>>> rad(1), rad(-1), rad(72), rad(-72)
(1, 1, 6, 6)
>>> rad(2 ** 17), rad(3 ** 9)
(2, 3)
>>> rad_coprime_product_holds(-72, 25)
True

The anchor triple:

>>> t = ABCTriple(1, 8, 9)
>>> t.radical
6
>>> quality_gt_one_exact(t)
True
>>> inv = frey_invariants(t)
>>> (inv.b2, inv.b4, inv.b6, inv.b8)
(28, -16, 0, -64)
>>> (inv.c4, inv.c6, inv.delta)
(1168, -38080, 82944)
>>> anchor_1_8_9()["minimal_discriminant"]
82944
>>> anchor_1_8_9()["conductor"]
48

Corrected bounds, expressed without floating-point logarithms:

>>> discriminant_bounds_hold(t, minimization_scale_power=0)
True
>>> conductor_bound_from_f2(t, f2=4)
(48, 768)
>>> exhaustive_rad_checks(120)
True
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from math import gcd, isqrt
from typing import Final


def _require_int(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


def valuation(n: int, p: int) -> int:
    """Return v_p(n) for nonzero n and prime p.

    >>> valuation(82944, 2), valuation(82944, 3)
    (10, 4)
    """

    _require_int(n, "n")
    _require_int(p, "p")
    if n == 0:
        raise ValueError("valuation(0, p) is not finite")
    if not is_prime(p):
        raise ValueError("p must be prime")
    n = abs(n)
    exponent = 0
    while n % p == 0:
        exponent += 1
        n //= p
    return exponent


def is_prime(n: int) -> bool:
    """Deterministic trial-division primality test for a Python integer."""

    _require_int(n, "n")
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = isqrt(n)
    divisor = 3
    while divisor <= limit:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factorization(n: int) -> tuple[tuple[int, int], ...]:
    """Return the certified positive-prime factorization of ``abs(n)``.

    The empty tuple is the factorization of +/-1.

    >>> prime_factorization(-72)
    ((2, 3), (3, 2))
    >>> prime_factorization(1)
    ()
    """

    _require_int(n, "n")
    if n == 0:
        raise ValueError("rad and factorization are undefined at zero")

    remaining = abs(n)
    factors: list[tuple[int, int]] = []

    exponent = 0
    while remaining % 2 == 0:
        remaining //= 2
        exponent += 1
    if exponent:
        factors.append((2, exponent))

    divisor = 3
    while divisor <= remaining // divisor:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 2

    if remaining > 1:
        factors.append((remaining, 1))

    # A factorization certificate checked independently of the loop state.
    reconstructed = 1
    previous = 1
    for prime, power in factors:
        assert prime > previous
        assert is_prime(prime)
        assert power >= 1
        reconstructed *= prime**power
        previous = prime
    assert reconstructed == abs(n)

    return tuple(factors)


def rad(n: int) -> int:
    """Return the product of the distinct positive prime divisors of n."""

    result = 1
    for prime, _power in prime_factorization(n):
        result *= prime
    return result


def rad_prime_power_holds(p: int, k: int) -> bool:
    """Check rad(p**k) == p after validating the quantified premises."""

    _require_int(p, "p")
    _require_int(k, "k")
    if not is_prime(p) or k < 1:
        raise ValueError("requires prime p and k >= 1")
    return rad(p**k) == p


def rad_coprime_product_holds(m: int, n: int) -> bool:
    """Check rad(m*n) == rad(m)*rad(n) for a nonzero coprime pair."""

    _require_int(m, "m")
    _require_int(n, "n")
    if m == 0 or n == 0 or gcd(abs(m), abs(n)) != 1:
        raise ValueError("requires nonzero coprime integers")
    return rad(m * n) == rad(m) * rad(n)


@dataclass(frozen=True)
class ABCTriple:
    """A positive coprime triple with a+b=c."""

    a: int
    b: int
    c: int

    def __post_init__(self) -> None:
        for name, value in (("a", self.a), ("b", self.b), ("c", self.c)):
            _require_int(value, name)
            if value < 1:
                raise ValueError(f"{name} must be positive")
        if self.a + self.b != self.c:
            raise ValueError("requires a + b = c")
        if gcd(self.a, self.b) != 1:
            raise ValueError("requires gcd(a, b) = 1")
        assert gcd(self.a, self.c) == 1
        assert gcd(self.b, self.c) == 1

    @property
    def product(self) -> int:
        return self.a * self.b * self.c

    @property
    def radical(self) -> int:
        return rad(self.product)

    @property
    def has_ob03_parity(self) -> bool:
        return self.a % 2 == 1 and self.b % 2 == 0


@dataclass(frozen=True)
class FreyInvariants:
    a1: int
    a2: int
    a3: int
    a4: int
    a6: int
    b2: int
    b4: int
    b6: int
    b8: int
    c4: int
    c6: int
    delta: int


def frey_invariants(triple: ABCTriple) -> FreyInvariants:
    """Compute the exact invariants of y^2=x(x-a)(x+b)."""

    a, b, c = triple.a, triple.b, triple.c
    a1, a2, a3, a4, a6 = 0, b - a, 0, -a * b, 0
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = (
        a1 * a1 * a6
        - a1 * a3 * a4
        + 4 * a2 * a6
        + a2 * a3 * a3
        - a4 * a4
    )
    c4 = b2 * b2 - 24 * b4
    c6 = -(b2**3) + 36 * b2 * b4 - 216 * b6
    delta = -(b2 * b2 * b8) - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6

    assert b2 == 4 * (b - a)
    assert b4 == -2 * a * b
    assert b6 == 0
    assert b8 == -(a * b) ** 2
    assert c4 == 16 * (a * a + a * b + b * b)
    assert delta == 16 * (a * b * c) ** 2
    assert c4**3 - c6**2 == 1728 * delta

    return FreyInvariants(
        a1, a2, a3, a4, a6, b2, b4, b6, b8, c4, c6, delta
    )


def minimal_discriminant_candidate(
    triple: ABCTriple, minimization_scale_power: int
) -> int:
    """Return 2^(4-12s)*(abc)^2 for the theorem's s in {0,1}."""

    _require_int(minimization_scale_power, "minimization_scale_power")
    if not triple.has_ob03_parity:
        raise ValueError("requires a odd and b even")
    if minimization_scale_power not in (0, 1):
        raise ValueError("the corrected theorem proves s is 0 or 1")
    model_delta = frey_invariants(triple).delta
    divisor = 2 ** (12 * minimization_scale_power)
    if model_delta % divisor != 0:
        raise ValueError("this s cannot yield an integral minimal discriminant")
    return model_delta // divisor


def discriminant_bounds_hold(
    triple: ABCTriple, minimization_scale_power: int
) -> bool:
    """Check the corrected log bounds by exact monotone integer inequalities."""

    delta_min = minimal_discriminant_candidate(triple, minimization_scale_power)
    product_squared = triple.product**2
    # 2^-8 (abc)^2 <= Delta_min <= 2^4 (abc)^2.
    two_sided = product_squared <= 256 * delta_min and delta_min <= 16 * product_squared
    # This is the exponential form of log Delta_min >= 2 log(c) - 8 log(2).
    skeleton_lower = triple.c**2 <= 256 * delta_min
    return two_sided and skeleton_lower


def odd_radical(triple: ABCTriple) -> int:
    """Return the odd part of rad(abc)."""

    result = triple.radical
    if result % 2 == 0:
        result //= 2
    return result


def conductor_bound_from_f2(triple: ABCTriple, f2: int) -> tuple[int, int]:
    """Return (N, 2^7*rad(abc)) under the proven local formula.

    At each odd p|abc the local conductor exponent is one.  Silverman,
    Advanced Topics, Theorem IV.10.4 gives 0 <= f2 <= 8.
    """

    _require_int(f2, "f2")
    if not triple.has_ob03_parity:
        raise ValueError("requires a odd and b even")
    if not 0 <= f2 <= 8:
        raise ValueError("requires the unconditional bound 0 <= f2 <= 8")
    conductor = 2**f2 * odd_radical(triple)
    upper = 2**7 * triple.radical
    assert conductor <= upper
    return conductor, upper


def quality_gt_one_exact(triple: ABCTriple) -> bool:
    """Decide q>1 without floating point, using strict monotonicity of log."""

    assert triple.c > 1 and triple.radical > 1
    return triple.c > triple.radical


_STEIN_WATKINS_TABLE_3: Final[dict[tuple[int, int], int]] = {
    (1, 2): 4,
    (1, 6): 5,
    (1, 10): 5,
    (1, 14): 3,
    (5, 2): 3,
    (5, 6): 2,
    (5, 10): 4,
    (5, 14): 4,
    (9, 2): 5,
    (9, 6): 3,
    (9, 10): 4,
    (9, 14): 5,
    (13, 2): 4,
    (13, 6): 4,
    (13, 10): 3,
    (13, 14): 2,
}


def anchor_1_8_9() -> dict[str, int | str]:
    """Return exact independently checked data for the attachment's anchor.

    The f2 lookup is Stein--Watkins (2002), Section 2.1, Tables 2--3.
    The prerequisites for the Table-3 branch are checked below.
    """

    triple = ABCTriple(1, 8, 9)
    inv = frey_invariants(triple)

    # v_2(Delta)=10<12 and v_3(Delta)=4<12, so the displayed integral
    # equation is already minimal at every prime.
    assert valuation(inv.delta, 2) == 10
    assert valuation(inv.delta, 3) == 4
    minimal_discriminant = inv.delta

    # Stein--Watkins twist-minimality exceptional cases do not apply.
    assert valuation(inv.c4, 2) == 4
    assert valuation(inv.c6, 2) == 6
    assert valuation(inv.c4**3 - inv.c6**2, 2) == 16 < 18

    # Table 2 sends (c4/16 mod 8, c6/32 mod 8)=(1,2) to Table 3.
    assert (inv.c4 // 16) % 8 == 1
    assert (inv.c6 // 32) % 8 == 2
    residue_pair = ((inv.c4 // 16) % 16, (inv.c6 // 32) % 16)
    assert residue_pair == (9, 10)
    f2 = _STEIN_WATKINS_TABLE_3[residue_pair]
    assert f2 == 4

    # The only odd bad prime is 3, and c4 is a 3-adic unit, so f3=1.
    assert inv.delta % 3 == 0 and inv.c4 % 3 != 0
    conductor = 2**f2 * 3
    assert conductor == 48

    return {
        "radical": triple.radical,
        "c4": inv.c4,
        "c6": inv.c6,
        "minimal_discriminant": minimal_discriminant,
        "f2": f2,
        "f3": 1,
        "conductor": conductor,
        "quality_gt_one": str(quality_gt_one_exact(triple)),
    }


def exhaustive_rad_checks(limit: int = 200) -> bool:
    """Finite regression checks; not a substitute for the universal proof."""

    _require_int(limit, "limit")
    if limit < 2:
        raise ValueError("limit must be at least 2")

    if rad(1) != 1 or rad(-1) != 1:
        return False

    for p in range(2, limit + 1):
        if is_prime(p):
            for k in range(1, 7):
                if not rad_prime_power_holds(p, k):
                    return False

    nonzero = [n for n in range(-limit, limit + 1) if n != 0]
    for m in nonzero:
        if rad(m) != rad(abs(m)):
            return False
        for n in nonzero:
            if gcd(abs(m), abs(n)) == 1 and not rad_coprime_product_holds(m, n):
                return False
    return True


def decimal_anchor_report() -> dict[str, str]:
    """Return high-precision decimal values used only as sanity checks."""

    getcontext().prec = 60
    data = anchor_1_8_9()
    delta = Decimal(int(data["minimal_discriminant"]))
    q = Decimal(9).ln() / Decimal(6).ln()
    return {
        "log_minimal_discriminant": str(delta.ln()),
        "discriminant_height": str(delta.ln() / Decimal(12)),
        "quality": str(q),
        "log_conductor": str(Decimal(int(data["conductor"])).ln()),
    }


def _main() -> None:
    import doctest
    import json

    failures, _tests = doctest.testmod()
    if failures:
        raise SystemExit(1)
    if not exhaustive_rad_checks(160):
        raise SystemExit("finite radical regression checks failed")
    payload = {"exact": anchor_1_8_9(), "decimal": decimal_anchor_report()}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    _main()
