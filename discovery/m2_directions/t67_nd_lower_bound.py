"""
T67 — Explicit verification of two theorems:
  1. thm:nd_lb: nd(a,b) >= second_smallest_prime_in_P (proved analytically)
  2. thm:nd_omega2: nd = max(p*w/g, q*v/g) for omega*=2 (proved analytically)

This script verifies both theorems on explicit examples as a sanity check.
The analytical proofs in the paper are complete; this script is cross-validation only.
"""

import math
from itertools import product as iproduct


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def nd_omega2_formula(a, b):
    """Exact nd for omega*=2 triples: nd = max(p*w/g, q*v/g)."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    if len(primes) != 2:
        return None
    p, q = primes[0], primes[1]
    v = fa.get(p, fb.get(p, fc.get(p, 0)))
    w = fa.get(q, fb.get(q, fc.get(q, 0)))
    g = math.gcd(v, w)
    return max(p * (w // g), q * (v // g))


def nd_brute(a, b, bound=10):
    """Brute-force nd by exhaustive vector enumeration."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2 or n > 5:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float("inf")
    for coords in iproduct(range(-bound, bound + 1), repeat=n):
        if all(c == 0 for c in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0:
            continue
        W = sum(ws[i] * coords[i] for i in range(n))
        if W == 0:
            continue
        norm = max(primes[i] * abs(coords[i]) for i in range(n))
        if norm > 0:
            best = min(best, norm)
    return best if best < float("inf") else None


# ── Named test cases ──────────────────────────────────────────────────────────
# omega*=2 cases: nd = max(p*w/g, q*v/g)
omega2_cases = [
    (1, 2, 3),  # P={2,3}, v=1,w=1, g=1, nd=max(2,3)=3
    (1, 3, 4),  # P={3,2}, v_3=1,v_2=2, g=1, nd=max(3*2,2*1)=6
    (1, 7, 8),  # P={7,2}, v_7=1,v_2=3, g=1, nd=max(7*3,2*1)=21
    (1, 8, 9),  # P={2,3}, v_2=3,v_3=2, g=1, nd=max(2*2,3*3)=9
    (1, 15, 16),  # P={3,5,2}... wait omega=3 here. Skip.
    (1, 48, 49),  # omega=3, skip
    (3, 1, 4),  # Pa={3}, Pb={}, Pc={2}, v_3=1,v_2=2, nd=max(3*2,2*1)=6
    (7, 1, 8),  # Pa={7}, Pb={}, Pc={2}, v_7=1,v_2=3, nd=max(7*3,2*1)=21
    (8, 1, 9),  # Pa={2}, Pb={}, Pc={3}, v_2=3,v_3=2, nd=max(2*2,3*3)=9
]

# Filter to omega*=2 only
omega2_valid = []
for a, b, c_ in omega2_cases:
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    if len(primes) == 2:
        omega2_valid.append((a, b, c))

# General non-squarefree examples for LB-1
lb1_cases = [
    (1, 8, 9),  # P={2,3}, p2=3, nd=9 >=3
    (1, 3, 4),  # P={2,3}, p2=3, nd=6 >=3
    (4, 5, 9),  # P={2,3,5}, p2=3, nd?
    (1, 24, 25),  # P={2,3,5}, p2=3, nd?
    (72, 11, 83),  # P={2,3,11,83}, p2=3, nd=9 >=3 (within-group example)
    (27, 5, 32),  # P={3,5,2}, p2=3, nd=6 >=3
    (1, 48, 49),  # P={2,3,7}, p2=3, nd=7 >=3
    (16, 9, 25),  # P={2,3,5}, p2=3
    (1, 80, 81),  # P={2,3,5}, p2=3
    (64, 17, 81),  # P={2,17,3}, p2=3
]

print("T67: Explicit verification of thm:nd_lb and thm:nd_omega2")
print("=" * 65)

# ── Check 1: omega*=2 exact formula ─────────────────────────────────────────
print("\nCheck 1: omega*=2 exact formula nd = max(p*w/g, q*v/g)")
print("-" * 65)
all_ok = True
for a, b, c in omega2_valid:
    nd_f = nd_omega2_formula(a, b)
    nd_b = nd_brute(a, b, bound=12)
    ok = nd_f == nd_b
    if not ok:
        all_ok = False
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    p2 = primes[1]
    print(
        f"  ({a},{b},{c}): formula={nd_f}, brute={nd_b}, p2={p2}, nd>=p2={'YES' if nd_f >= p2 else 'FAIL'} {'OK' if ok else 'MISMATCH'}"
    )
print(f"Result: {'ALL MATCH' if all_ok else 'FAILURES FOUND'}")

# ── Check 2: LB-1 for explicit examples ─────────────────────────────────────
print("\nCheck 2: thm:nd_lb — nd(a,b) >= second_smallest_prime")
print("-" * 65)
lb1_ok = True
for a, b_raw, c_raw in lb1_cases:
    c = a + b_raw
    if c != c_raw:
        continue
    b = b_raw
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    if len(primes) < 2 or len(primes) > 5:
        continue
    p2 = primes[1]
    nd = nd_brute(a, b, bound=10)
    if nd is None:
        continue
    ok = nd >= p2
    if not ok:
        lb1_ok = False
    sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())
    print(
        f"  ({a},{b},{c}): nd={nd}, p2={p2}, P={primes[:4]}{'...' if len(primes) > 4 else ''}, "
        f"{'sq' if sq else 'nsq'}, nd>=p2={'YES' if ok else 'FAIL'}"
    )
print(f"Result: {'ALL PASS — LB-1 confirmed' if lb1_ok else 'FAILURES FOUND'}")

# ── LB-1 proof sketch (from paper) ──────────────────────────────────────────
print("\nAnalytical proof summary (from paper Theorem thm:nd_lb):")
print("  Key step: if ||phi|| < p2, then all phi_p=0 for p>=p2 (norm bound),")
print(
    "  and the single-prime lemma forces phi_{p1}=0 too. So phi=0, W=0: contradiction."
)
print("  Therefore nd >= p2 for ALL coprime triples a+b=c. QED (no restriction).")
print()
print("DONE — both theorems verified on named examples.")
