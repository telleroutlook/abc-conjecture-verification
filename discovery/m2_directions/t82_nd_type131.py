"""
T82 — Exact nd formula for type (1,3,1) triples.
a = p^k,  b = q^j1 * r^j2 * s^j3,  c = t^n.
5 distinct primes: Pa={p}, Pb={q,r,s}, Pc={t}.
Constraint: k*phi_p + j1*phi_q + j2*phi_r + j3*phi_s = n*phi_t.
Wronskian: W = (phi_q + phi_r + phi_s) - phi_p.

5-branch formula:
  N_{t=0}: Pa x Pb homogeneous: k*phi_p+j1*phi_q+j2*phi_r+j3*phi_s=0, W!=0
  N_{p=0}: Pb x Pc interaction: j1*phi_q+j2*phi_r+j3*phi_s=n*phi_t, W=phi_q+phi_r+phi_s!=0
  B_{q=0}: nd_type121(p^k, r^j2, s^j3, t^n)
  B_{r=0}: nd_type121(p^k, q^j1, s^j3, t^n)
  B_{s=0}: nd_type121(p^k, q^j1, r^j2, t^n)

Type (3,1,1) follows by Pa<->Pb swap:
  Pa={p,q,r}, Pb={s}, Pc={t}: same 5-branch formula with p<->s labelling.
"""

import math
from itertools import product as iproduct
from collections import defaultdict
import random

LIMIT = 150
BB = 15
BRUTE_BOUND = 5
SPOT_N = 50

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b); return g, y, x - (a // b) * y

def bm(m, n, k, pb, pc):
    best = float('inf'); g, u0, v0 = egcd(m, n)
    for sgn in [1, -1]:
        rhs = sgn * k
        if rhs % g != 0: continue
        s = rhs // g; up = u0 * s; vp = -v0 * s; su = n // g; sv = m // g
        D = pb * su - pc * sv; to = (pc * vp - pb * up) / D if D != 0 else 0.0
        for t in range(int(to) - 6, int(to) + 7):
            phi_b = up + su * t; phi_c = vp + sv * t
            if m * phi_b - n * phi_c != rhs: continue
            best = min(best, max(pb * abs(phi_b), pc * abs(phi_c)))
    return best

def nd111(pa, pb, pc, k, m, n):
    g1 = math.gcd(k, m); g2 = math.gcd(m, n); g3 = math.gcd(k, n)
    N0 = max(pa * m // g1, pb * k // g1); N1 = max(pb * n // g2, pc * m // g2)
    N2 = max(pa * n // g3, pc * k // g3)
    if N0 <= pc: return N0
    if N1 <= pa: return N1
    if N2 <= pb: return N2
    pL = max(pa, pb, pc)
    if pL == pa:   B = bm(m, n, k, pb, pc)
    elif pL == pb: B = bm(k, n, m, pa, pc)
    else:
        B = float('inf')
        for ph in [1, -1]:
            for phi_a in range(-40, 41):
                rem = n * ph - k * phi_a
                if rem % m != 0: continue
                phi_b = rem // m
                if phi_b == phi_a: continue
                B = min(B, max(pa * abs(phi_a), pb * abs(phi_b), pc))
    return min(min(N0, N1, N2), max(pL, B))

def nd_p0_b(q, r, s, j, m, n, bnd=BB):
    best = float('inf')
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = j * pq + m * pr
            if n == 0 or rhs % n != 0: continue
            ps = rhs // n
            if pq + pr == 0: continue
            v = max(q * abs(pq), r * abs(pr), s * abs(ps))
            if v > 0: best = min(best, v)
    return best

def nd_s0_121(p, q, r, k, j, m, bnd=BB):
    best = float('inf')
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = -(j * pq + m * pr)
            if rhs % k != 0: continue
            pp = rhs // k
            if (pq + pr) == pp: continue
            v = max(p * abs(pp), q * abs(pq), r * abs(pr))
            if v > 0: best = min(best, v)
    return best

def nd121(p, q, r, s, k, j, m, n):
    return min(nd_s0_121(p, q, r, k, j, m), nd_p0_b(q, r, s, j, m, n),
               nd111(p, q, s, k, j, n), nd111(p, r, s, k, m, n))

def nd_t0_branch(p, q, r, s, k, j1, j2, j3, bnd=BB):
    """Pa x Pb homogeneous: k*phi_p + j1*phi_q + j2*phi_r + j3*phi_s = 0,
    W = (phi_q+phi_r+phi_s) - phi_p != 0."""
    best = float('inf')
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            for ps in range(-bnd, bnd + 1):
                rhs = -(j1 * pq + j2 * pr + j3 * ps)
                if rhs % k != 0: continue
                pp = rhs // k
                W = (pq + pr + ps) - pp
                if W == 0: continue
                v = max(p * abs(pp), q * abs(pq), r * abs(pr), s * abs(ps))
                if v > 0: best = min(best, v)
    return best

def nd_p0_branch(q, r, s, t, j1, j2, j3, n, bnd=BB):
    """Pb x Pc interaction: j1*phi_q+j2*phi_r+j3*phi_s=n*phi_t,
    W = phi_q+phi_r+phi_s != 0."""
    best = float('inf')
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            for ps in range(-bnd, bnd + 1):
                rhs = j1 * pq + j2 * pr + j3 * ps
                if n == 0 or rhs % n != 0: continue
                pt = rhs // n
                if pq + pr + ps == 0: continue
                v = max(q * abs(pq), r * abs(pr), s * abs(ps), t * abs(pt))
                if v > 0: best = min(best, v)
    return best

def nd_formula_131(p, q, r, s, t, k, j1, j2, j3, n):
    """5-branch formula for type (1,3,1)."""
    Nt0 = nd_t0_branch(p, q, r, s, k, j1, j2, j3)      # Pa x Pb homogeneous
    Np0 = nd_p0_branch(q, r, s, t, j1, j2, j3, n)      # Pb x Pc interaction
    Bq0 = nd121(p, r, s, t, k, j2, j3, n)               # phi_q=0: (1,2,1)
    Br0 = nd121(p, q, s, t, k, j1, j3, n)               # phi_r=0: (1,2,1)
    Bs0 = nd121(p, q, r, t, k, j1, j2, n)               # phi_s=0: (1,2,1)
    return min(Nt0, Np0, Bq0, Br0, Bs0), (Nt0, Np0, Bq0, Br0, Bs0)

def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    if len(primes) > 6: return None
    alpha = [fa.get(pr, fb.get(pr, -fc.get(pr, 0))) for pr in primes]
    ws = [1 if pr in fb else (-1 if pr in fa else 0) for pr in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=len(primes)):
        if all(c2 == 0 for c2 in coords): continue
        if sum(alpha[i] * coords[i] for i in range(len(primes))) != 0: continue
        if sum(ws[i] * coords[i] for i in range(len(primes))) == 0: continue
        best = min(best, max(primes[i] * abs(coords[i]) for i in range(len(primes))))
    return best if best < float('inf') else None

# ── Precompute ──────────────────────────────────────────────────────────────
prime_powers = {}; three_prime = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 1:
        pr = list(f.keys())[0]; prime_powers[n] = (pr, f[pr])
    elif len(f) == 3:
        ps = sorted(f.keys())
        three_prime[n] = (ps[0], ps[1], ps[2], f[ps[0]], f[ps[1]], f[ps[2]])

# Type (1,3,1): a=prime_power, b=three_prime, c=prime_power
triples = []; seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, r, s, j1, j2, j3) in three_prime.items():
        if q == p or r == p or s == p: continue
        c = a + b
        if c not in prime_powers: continue
        t, nv = prime_powers[c]
        if t in (p, q, r, s): continue
        if math.gcd(a, b) != 1: continue
        key = tuple(sorted([a, b]))
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, k, j1, j2, j3, nv))

print(f"T82: type (1,3,1) nd formula — {len(triples)} triples (a,b ≤ {LIMIT})")

branch_names = ['N_t0(Pa×Pb)', 'N_p0(Pb×Pc)', 'B_q0(121)', 'B_r0(121)', 'B_s0(121)']
branch_wins = defaultdict(int)
for t in triples:
    a, b, p, q, r, s, tv, k, j1, j2, j3, nv = t
    val, parts = nd_formula_131(p, q, r, s, tv, k, j1, j2, j3, nv)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    print(f"  {br:18s}: {cnt:4d}  ({100 * cnt / len(triples):.1f}%)")
print()

# Spot-check
random.seed(77)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = fail = low = 0
for t in sample:
    a, b, p, q, r, s, tv, k, j1, j2, j3, nv = t
    formula, _ = nd_formula_131(p, q, r, s, tv, k, j1, j2, j3, nv)
    brute = nd_brute(a, b)
    if brute is None: continue
    if formula == brute: ok += 1
    elif formula < brute: low += 1; print(f"  formula<brute ({a},{b}): {formula} vs {brute}")
    else: fail += 1; print(f"  FAIL ({a},{b}): formula={formula} brute={brute}")

print(f"Spot-check ({len(sample)} triples, bound={BRUTE_BOUND}): OK={ok}, low={low}, FAIL={fail}")
if fail == 0: print("\nFORMULA CANDIDATE CONFIRMED (no failures).")
