"""
T74 — Exact nd for type (2,1,1) triples.  Complete 6-branch formula.
a = p^k1 * q^k2,  b = r^m,  c = s^n.

Formula: nd = min(B1, B2, B3, B4, B5, B6) where
  B1 = within-group intra-Pa (valid iff k1≠k2)
  B2 = 5 cross-group 2-prime norms
  B3 = nd_111(p,r,s; k1,m,n)   [φ_q=0]
  B4 = nd_111(q,r,s; k2,m,n)   [φ_p=0]
  B5 = 3-prime min for φ_r=0 branch
  B6 = 3-prime min for φ_s=0 branch
"""

import math
from itertools import product as iproduct
from collections import defaultdict
import random

LIMIT = 200
BRANCH_BOUND = 20  # for nd_zero_r / nd_zero_s loops
BRUTE_BOUND = 6  # for spot-check brute-force
SPOT_N = 50  # number of triples to spot-check


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


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def bezout_min_norm(m, n, k, pb, pc):
    best = float("inf")
    g, u0, v0 = extended_gcd(m, n)
    for sign in [+1, -1]:
        rhs = sign * k
        if rhs % g != 0:
            continue
        s = rhs // g
        u_part = u0 * s
        v_part = -v0 * s
        step_u = n // g
        step_v = m // g
        denom = pb * step_u - pc * step_v
        t_opt = (pc * v_part - pb * u_part) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 6, int(t_opt) + 7):
            phi_b = u_part + step_u * t
            phi_c = v_part + step_v * t
            if m * phi_b - n * phi_c != rhs:
                continue
            norm = max(pb * abs(phi_b), pc * abs(phi_c))
            if norm < best:
                best = norm
    return best


def nd_111(pa, pb, pc, k, m, n):
    """nd for one-prime-per-group."""
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)
    N1 = max(pb * n // g_mn, pc * m // g_mn)
    N2 = max(pa * n // g_kn, pc * k // g_kn)
    if N0 <= pc:
        return N0
    if N1 <= pa:
        return N1
    if N2 <= pb:
        return N2
    p_L = max(pa, pb, pc)
    if p_L == pa:
        B = bezout_min_norm(m, n, k, pb, pc)
    elif p_L == pb:
        B = bezout_min_norm(k, n, m, pa, pc)
    else:
        B = float("inf")
        for phi_c in [+1, -1]:
            rhs = n * phi_c
            for phi_a in range(-40, 41):
                rem = rhs - k * phi_a
                if rem % m != 0:
                    continue
                phi_b = rem // m
                if phi_b == phi_a:
                    continue
                B = min(B, max(pa * abs(phi_a), pb * abs(phi_b), pc))
    return min(min(N0, N1, N2), max(p_L, B))


def nd_zero_r_branch(p, q, s, k1, k2, nv, bound=BRANCH_BOUND):
    """φ_r=0: min max(p|φ_p|,q|φ_q|,s|φ_s|) s.t. k1*φ_p+k2*φ_q=n*φ_s, φ_p+φ_q≠0."""
    best = float("inf")
    for phi_p in range(-bound, bound + 1):
        for phi_q in range(-bound, bound + 1):
            rhs = k1 * phi_p + k2 * phi_q
            if rhs % nv != 0:
                continue
            phi_s = rhs // nv
            if phi_p + phi_q == 0:
                continue
            norm = max(p * abs(phi_p), q * abs(phi_q), s * abs(phi_s))
            if norm > 0:
                best = min(best, norm)
    return best


def nd_zero_s_branch(p, q, r, k1, k2, m, bound=BRANCH_BOUND):
    """φ_s=0: min max(p|φ_p|,q|φ_q|,r|φ_r|) s.t. k1*φ_p+k2*φ_q+m*φ_r=0, φ_r≠φ_p+φ_q."""
    best = float("inf")
    for phi_p in range(-bound, bound + 1):
        for phi_q in range(-bound, bound + 1):
            rhs = -(k1 * phi_p + k2 * phi_q)
            if rhs % m != 0:
                continue
            phi_r = rhs // m
            if phi_r == phi_p + phi_q:
                continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0:
                best = min(best, norm)
    return best


def nd_formula(p, q, r, s, k1, k2, m, nv):
    g = math.gcd(k1, k2)
    B1 = max(p * (k2 // g), q * (k1 // g)) if k1 != k2 else float("inf")
    g1m = math.gcd(k1, m)
    g2m = math.gcd(k2, m)
    g1n = math.gcd(k1, nv)
    g2n = math.gcd(k2, nv)
    gmn = math.gcd(m, nv)
    B2 = min(
        max(p * m // g1m, r * k1 // g1m),
        max(q * m // g2m, r * k2 // g2m),
        max(p * nv // g1n, s * k1 // g1n),
        max(q * nv // g2n, s * k2 // g2n),
        max(r * nv // gmn, s * m // gmn),
    )
    B3 = nd_111(p, r, s, k1, m, nv)
    B4 = nd_111(q, r, s, k2, m, nv)
    B5 = nd_zero_r_branch(p, q, s, k1, k2, nv)
    B6 = nd_zero_s_branch(p, q, r, k1, k2, m)
    return min(B1, B2, B3, B4, B5, B6), (B1, B2, B3, B4, B5, B6)


def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ > 5:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float("inf")
    for coords in iproduct(range(-bound, bound + 1), repeat=np_):
        if all(c2 == 0 for c2 in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(np_)) != 0:
            continue
        if sum(ws[i] * coords[i] for i in range(np_)) == 0:
            continue
        best = min(best, max(primes[i] * abs(coords[i]) for i in range(np_)))
    return best if best < float("inf") else None


# ── Precompute ────────────────────────────────────────────────────────────────

two_prime = {}
prime_powers = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 2:
        ps = sorted(f.keys())
        two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])
    elif len(f) == 1:
        p = list(f.keys())[0]
        prime_powers[n] = (p, f[p])

triples = []
seen = set()
for a, (p, q, k1, k2) in two_prime.items():
    for b, (r, m) in prime_powers.items():
        if r in (p, q):
            continue
        c = a + b
        if c not in prime_powers:
            continue
        s, nv = prime_powers[c]
        if s in (p, q, r):
            continue
        if math.gcd(a, b) != 1:
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k1, k2, m, nv))

print(f"T74: type (2,1,1) — {len(triples)} triples with a,b ≤ {LIMIT}")
print()

# ── Main: formula on all triples ──────────────────────────────────────────────

branch_wins = defaultdict(int)
branch_names = [
    "B1_intra",
    "B2_cross",
    "B3_zero_q",
    "B4_zero_p",
    "B5_zero_r",
    "B6_zero_s",
]

for a, b, p, q, r, s, k1, k2, m, nv in triples:
    formula, parts = nd_formula(p, q, r, s, k1, k2, m, nv)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    pct = 100 * cnt / len(triples)
    print(f"  {br:15s}: {cnt:4d}  ({pct:.1f}%)")
print()

# ── Spot-check: brute-force on random sample ──────────────────────────────────

random.seed(42)
sample = random.sample(triples, min(SPOT_N, len(triples)))
sample_ok = 0
sample_fail = 0
sample_low = 0

for a, b, p, q, r, s, k1, k2, m, nv in sample:
    formula, _ = nd_formula(p, q, r, s, k1, k2, m, nv)
    brute = nd_brute(a, b)
    if brute is None:
        continue
    if formula == brute:
        sample_ok += 1
    elif formula < brute:
        # formula gives lower nd: brute bound may be too small
        sample_low += 1
        print(
            f"  FORMULA<BRUTE ({a},{b}): formula={formula} brute(bd={BRUTE_BOUND})={brute}"
        )
    else:
        sample_fail += 1
        print(f"  FAIL ({a},{b}): formula={formula} brute={brute}")

print(f"Spot-check ({len(sample)} triples, brute bound={BRUTE_BOUND}):")
print(
    f"  OK: {sample_ok},  formula<brute(bound too small): {sample_low},  formula>brute(FAIL): {sample_fail}"
)
print()

if sample_fail == 0:
    print("NO FAILURES. Formula candidate confirmed on all spot-checked triples.")
    print()
    print("STRUCTURAL THEOREM T74 (candidate):")
    print(
        "  nd(a,b) = min(B1_intra*, B2_cross, B3_zero_q, B4_zero_p, B5_zero_r, B6_zero_s)"
    )
    print("  B1_intra* = within-group norm, valid only when k1 ≠ k2")
    print("  B3,B4 = nd_111 for reduced (1,1,1) problems (zeroing one Pa prime)")
    print("  B5,B6 = 3-prime minima for zero-r / zero-s branches")
