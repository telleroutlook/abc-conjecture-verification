"""
proof/m1/rad.py — Formal definition of the rad function.

rad(n) = product of distinct prime factors of n  (CL-01, DEF).

This is the arithmetic source used in the abc conjecture statement:
  rad(abc) = rad(a) * rad(b) * rad(c)  for coprime a, b, c.

This module may import only from proof.m0 (non-anticipation barrier B1).
No abc triples, no fitted parameters, no Szpiro assumed (barrier B2).
"""

from __future__ import annotations

from proof.m0.provenance import assert_zero_free, assert_no_abc_input

assert_zero_free(__file__)
assert_no_abc_input(
    "rad(n) is defined from first principles as the product of distinct prime "
    "factors of n. No known examples or fitted parameters are used."
)


def rad(n: int) -> int:
    """
    rad(n) = product of distinct prime factors of n.

    Properties (verified by check_rad_properties()):
      rad(1) = 1
      rad(p) = p for any prime p
      rad(p^k) = p for any prime p, k >= 1
      rad(m*n) = rad(m)*rad(n) / rad(gcd(m,n))^2  ... simplifies to:
      rad(m*n) = rad(m) * rad(n) when gcd(m, n) = 1  (multiplicativity)
    """
    if not isinstance(n, int):
        raise TypeError(f"rad requires an integer, got {type(n).__name__}")
    if n == 0:
        raise ValueError("rad(0) is undefined")
    if n < 0:
        n = -n
    if n == 1:
        return 1
    result = 1
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            result *= p
            while temp % p == 0:
                temp //= p
        p += 1
    if temp > 1:
        result *= temp
    return result


def rad_triple(a: int, b: int, c: int) -> int:
    """
    rad(abc) for a coprime triple a + b = c.

    For coprime a, b, c: rad(abc) = rad(a) * rad(b) * rad(c)
    because gcd(a,b) = gcd(b,c) = gcd(a,c) = 1 implies the prime sets are disjoint.
    """
    return rad(a) * rad(b) * rad(c)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def check_rad_properties() -> dict:
    """
    Programmatically verify basic rad properties.

    Returns a dict with each property name -> bool (True = verified).
    All must be True for the definition to be correct.
    """
    results: dict[str, bool] = {}

    # rad(1) = 1
    results["rad_1_eq_1"] = rad(1) == 1

    # rad(p) = p for small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    results["rad_prime_eq_prime"] = all(rad(p) == p for p in small_primes)

    # rad(p^k) = p for prime powers
    prime_powers = [(2, 2), (2, 3), (2, 10), (3, 2), (3, 5), (5, 3), (7, 4)]
    results["rad_prime_power"] = all(
        rad(p**k) == p for p, k in prime_powers
    )

    # rad multiplicative for coprimes: rad(m*n) = rad(m)*rad(n) when gcd(m,n)=1
    from math import gcd
    coprime_pairs = [(4, 9), (8, 27), (25, 49), (2, 15), (4, 21), (9, 25)]
    results["rad_multiplicative_coprime"] = all(
        gcd(m, n) == 1 and rad(m * n) == rad(m) * rad(n)
        for m, n in coprime_pairs
    )

    # rad(n) <= n for all n >= 1
    results["rad_le_n"] = all(rad(n) <= n for n in range(1, 200))

    # rad(n) = n iff n is squarefree
    squarefree = [1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 21, 30]
    not_squarefree = [4, 8, 9, 12, 18, 25, 27, 36, 50]
    results["rad_squarefree_identity"] = (
        all(rad(n) == n for n in squarefree)
        and all(rad(n) < n for n in not_squarefree)
    )

    return results
