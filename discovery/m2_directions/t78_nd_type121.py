"""
T78 — Exact nd formula for type (1,2,1) triples.
a = p^k,  b = q^j * r^m  (q<r, Pb has two primes),  c = s^n.
All four primes p, q, r, s distinct.

By symmetry with thm:nd_type211 (type (2,1,1)), the formula is the Pa<->Pb
swap: replace (p,q,k1,k2) -> (q,r,j,m) as the two-prime group, and p^k as the
single prime. Wronskian: W = (phi_q + phi_r) - phi_p (Pb minus Pa).

Formula: nd = min over 10 branches:
  W_b*            within-group Pb: max(q*m/g, r*j/g), valid iff j != m
  pw(k,j,p,q)     phi_r=phi_s=0
  pw(k,m,p,r)     phi_q=phi_s=0
  pw(k,n,p,s)     phi_q=phi_r=0
  pw(j,n,q,s)     phi_p=phi_r=0
  pw(m,n,r,s)     phi_p=phi_q=0
  N_p0            phi_p=0: min max(q|phi_q|,r|phi_r|,s|phi_s|) s.t. j*phi_q+m*phi_r=n*phi_s, W=(phi_q+phi_r)!=0
  N_s0            phi_s=0: min max(p|phi_p|,q|phi_q|,r|phi_r|) s.t. k*phi_p+j*phi_q+m*phi_r=0, W=(phi_q+phi_r)-phi_p!=0
  nd3_r0          phi_r=0: nd_111(p^k, q^j, s^n)
  nd3_q0          phi_q=0: nd_111(p^k, r^m, s^n)
"""

import math
from itertools import product as iproduct
from collections import defaultdict
import random

LIMIT = 200
BRANCH_BOUND = 20
BRUTE_BOUND = 6
SPOT_N = 60

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def bezout_min_norm(m, n, k, pb, pc):
    best = float('inf')
    g, u0, v0 = extended_gcd(m, n)
    for sign in [+1, -1]:
        rhs = sign * k
        if rhs % g != 0: continue
        s = rhs // g
        u_part = u0 * s; v_part = -v0 * s
        step_u = n // g; step_v = m // g
        denom = pb * step_u - pc * step_v
        t_opt = (pc * v_part - pb * u_part) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 6, int(t_opt) + 7):
            phi_b = u_part + step_u * t
            phi_c = v_part + step_v * t
            if m * phi_b - n * phi_c != rhs: continue
            best = min(best, max(pb * abs(phi_b), pc * abs(phi_c)))
    return best

def nd_111(pa, pb, pc, k, m, n):
    g_km = math.gcd(k, m); g_mn = math.gcd(m, n); g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)
    N1 = max(pb * n // g_mn, pc * m // g_mn)
    N2 = max(pa * n // g_kn, pc * k // g_kn)
    if N0 <= pc: return N0
    if N1 <= pa: return N1
    if N2 <= pb: return N2
    p_L = max(pa, pb, pc)
    if p_L == pa:   B = bezout_min_norm(m, n, k, pb, pc)
    elif p_L == pb: B = bezout_min_norm(k, n, m, pa, pc)
    else:
        B = float('inf')
        for phi_c in [+1, -1]:
            rhs = n * phi_c
            for phi_a in range(-40, 41):
                rem = rhs - k * phi_a
                if rem % m != 0: continue
                phi_b = rem // m
                if phi_b == phi_a: continue
                B = min(B, max(pa * abs(phi_a), pb * abs(phi_b), pc))
    return min(min(N0, N1, N2), max(p_L, B))

def nd_p0_branch(q, r, s, j, m, n, bound=BRANCH_BOUND):
    """phi_p=0: j*phi_q+m*phi_r=n*phi_s, W=(phi_q+phi_r)!=0."""
    best = float('inf')
    for phi_q in range(-bound, bound + 1):
        for phi_r in range(-bound, bound + 1):
            rhs = j * phi_q + m * phi_r
            if n == 0 or rhs % n != 0: continue
            phi_s = rhs // n
            if phi_q + phi_r == 0: continue
            norm = max(q * abs(phi_q), r * abs(phi_r), s * abs(phi_s))
            if norm > 0: best = min(best, norm)
    return best

def nd_s0_branch(p, q, r, k, j, m, bound=BRANCH_BOUND):
    """phi_s=0: k*phi_p+j*phi_q+m*phi_r=0, W=(phi_q+phi_r)-phi_p!=0."""
    best = float('inf')
    for phi_q in range(-bound, bound + 1):
        for phi_r in range(-bound, bound + 1):
            rhs = -(j * phi_q + m * phi_r)
            if rhs % k != 0: continue
            phi_p = rhs // k
            W = (phi_q + phi_r) - phi_p
            if W == 0: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0: best = min(best, norm)
    return best

def nd_formula_121(p, q, r, s, k, j, m, n):
    """Complete nd formula for type (1,2,1): Pa={p^k}, Pb={q^j,r^m}, Pc={s^n}."""
    g = math.gcd(j, m)
    W_b = max(q * (m // g), r * (j // g)) if j != m else float('inf')
    B2 = min(
        max(p * j // math.gcd(k, j), q * k // math.gcd(k, j)),  # pw(k,j,p,q)
        max(p * m // math.gcd(k, m), r * k // math.gcd(k, m)),  # pw(k,m,p,r)
        max(p * n // math.gcd(k, n), s * k // math.gcd(k, n)),  # pw(k,n,p,s)
        max(q * n // math.gcd(j, n), s * j // math.gcd(j, n)),  # pw(j,n,q,s)
        max(r * n // math.gcd(m, n), s * m // math.gcd(m, n)),  # pw(m,n,r,s)
    )
    B3 = nd_111(p, q, s, k, j, n)   # phi_r=0
    B4 = nd_111(p, r, s, k, m, n)   # phi_q=0
    B5 = nd_p0_branch(q, r, s, j, m, n)  # phi_p=0
    B6 = nd_s0_branch(p, q, r, k, j, m)  # phi_s=0
    return min(W_b, B2, B3, B4, B5, B6), (W_b, B2, B3, B4, B5, B6)

def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ > 5: return None
    alpha = [fa.get(pr, fb.get(pr, -fc.get(pr, 0))) for pr in primes]
    ws = [1 if pr in fb else (-1 if pr in fa else 0) for pr in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=np_):
        if all(c2 == 0 for c2 in coords): continue
        if sum(alpha[i] * coords[i] for i in range(np_)) != 0: continue
        if sum(ws[i] * coords[i] for i in range(np_)) == 0: continue
        best = min(best, max(primes[i] * abs(coords[i]) for i in range(np_)))
    return best if best < float('inf') else None

# ── Precompute ────────────────────────────────────────────────────────────────

two_prime = {}; prime_powers = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 2:
        ps = sorted(f.keys()); two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])
    elif len(f) == 1:
        pr = list(f.keys())[0]; prime_powers[n] = (pr, f[pr])

# Type (1,2,1): a = prime power, b = two-prime, c = prime power
triples = []
seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, r, j, m) in two_prime.items():
        if q == p or r == p: continue
        c = a + b
        if c not in prime_powers: continue
        s, nv = prime_powers[c]
        if s in (p, q, r): continue
        if math.gcd(a, b) != 1: continue
        key = tuple(sorted([a, b]))
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k, j, m, nv))

print(f"T78: type (1,2,1) nd formula — {len(triples)} triples with a,b ≤ {LIMIT}")
print()

# ── Formula on all triples ──────────────────────────────────────────────────

branch_names = ['W_b*', 'B2_cross', 'B3_zero_r', 'B4_zero_q', 'B5_zero_p', 'B6_zero_s']
branch_wins = defaultdict(int)

for (a, b, p, q, r, s, k, j, m, nv) in triples:
    formula, parts = nd_formula_121(p, q, r, s, k, j, m, nv)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    pct = 100 * cnt / len(triples)
    print(f"  {br:15s}: {cnt:4d}  ({pct:.1f}%)")
print()

# ── Spot-check ────────────────────────────────────────────────────────────────

random.seed(99)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = 0; fail = 0; low = 0

for (a, b, p, q, r, s, k, j, m, nv) in sample:
    formula, _ = nd_formula_121(p, q, r, s, k, j, m, nv)
    brute = nd_brute(a, b)
    if brute is None: continue
    if formula == brute: ok += 1
    elif formula < brute: low += 1; print(f"  formula<brute ({a},{b}): {formula} vs {brute}")
    else: fail += 1; print(f"  FAIL ({a},{b}): formula={formula} brute={brute}")

print(f"Spot-check ({len(sample)} triples, bound={BRUTE_BOUND}): OK={ok}, low={low}, FAIL={fail}")

if fail == 0:
    print()
    print("THEOREM T78 (candidate): For type (1,2,1) coprime triples")
    print("  a = p^k + q^j*r^m = s^n  (p,q,r,s distinct, q<r),")
    print("  nd(a,b) = min(W_b*, 5 cross-group pw, nd_111(p,q,s), nd_111(p,r,s),")
    print("               N_{p=0}, N_{s=0})")
    print("  where W_b* = max(q*m/g, r*j/g) if j!=m, else +inf.")
    print("  Proof: Pa<->Pb symmetry with thm:nd_type211.")
