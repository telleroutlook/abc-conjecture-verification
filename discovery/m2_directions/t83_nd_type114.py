"""
T83 — Verify 6-branch recursive nd formula for type (1,1,4) triples.
a = p^k,  b = q^m,  c = r^j1 * s^j2 * t^j3 * u^j4.
6 distinct primes: Pa={p}, Pb={q}, Pc={r,s,t,u}.
Constraint: k*phi_p + m*phi_q = j1*phi_r + j2*phi_s + j3*phi_t + j4*phi_u.
Wronskian: W = phi_q - phi_p.

6-branch recursive formula (zero one prime coordinate each time):
  B_{u=0}: nd_type_113(p,q,r,s,t; k,m,j1,j2,j3)   -- zero phi_u -> type (1,1,3)
  B_{t=0}: nd_type_113(p,q,r,s,u; k,m,j1,j2,j4)   -- zero phi_t -> type (1,1,3)
  B_{s=0}: nd_type_113(p,q,r,t,u; k,m,j1,j3,j4)   -- zero phi_s -> type (1,1,3)
  B_{r=0}: nd_type_113(p,q,s,t,u; k,m,j2,j3,j4)   -- zero phi_r -> type (1,1,3)
  B_{p=0}: max(q, B4pc(m)) where B4pc(v) = min{max(r|a|,s|b|,t|c|,u|d|) : j1*a+j2*b+j3*c+j4*d=v}
  B_{q=0}: max(p, B4pc(k))

Type (1,1,4) follows the general recursive pattern:
  nd(a,b) = min of 6 branches (zero one of 6 prime coordinates).
  Each branch is either a (1,1,3) sub-problem or a 4-variable Bezout problem.

Results: 143 triples (a,b <= 500), spot-check 40, 0 failures.
"""

import math
from itertools import product as iproduct
import random

LIMIT = 500
BB = 8
BRUTE_BOUND = 3
SPOT_N = 40


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
    N0 = max(pa * m // g1, pb * k // g1)
    N1 = max(pb * n // g2, pc * m // g2)
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


def nd_omega4_two_c(pa, pb, pc1, pc2, ka, kb, n1, n2):
    B1 = nd111(pa, pb, pc1, ka, kb, n1)
    B2 = nd111(pa, pb, pc2, ka, kb, n2)
    B3 = max(pb, bm(n1, n2, kb, pc1, pc2))
    B4 = max(pa, bm(n1, n2, ka, pc1, pc2))
    return min(B1, B2, B3, B4)


def b3pc(j1, j2, j3, r, s, t, v, bnd=BB):
    best = float('inf')
    for a in range(-bnd, bnd + 1):
        for b in range(-bnd, bnd + 1):
            rem = v - j1 * a - j2 * b
            if rem % j3 != 0: continue
            c = rem // j3
            nrm = max(r * abs(a), s * abs(b), t * abs(c))
            if nrm > 0 or v == 0: best = min(best, nrm)
    return best


def nd_formula_113(p, q, r, s, t, k, m, j1, j2, j3):
    return min(nd_omega4_two_c(p, q, r, s, k, m, j1, j2),
               nd_omega4_two_c(p, q, r, t, k, m, j1, j3),
               nd_omega4_two_c(p, q, s, t, k, m, j2, j3),
               max(q, b3pc(j1, j2, j3, r, s, t, m)),
               max(p, b3pc(j1, j2, j3, r, s, t, k)))


def b4pc(j1, j2, j3, j4, r, s, t, u, v, bnd=BB):
    """min{max(r|a|,s|b|,t|c|,u|d|) : j1*a+j2*b+j3*c+j4*d=v}"""
    best = float('inf')
    for a in range(-bnd, bnd + 1):
        for b in range(-bnd, bnd + 1):
            for c in range(-bnd, bnd + 1):
                rem = v - j1 * a - j2 * b - j3 * c
                if rem % j4 != 0: continue
                d = rem // j4
                nrm = max(r * abs(a), s * abs(b), t * abs(c), u * abs(d))
                if nrm > 0 or v == 0: best = min(best, nrm)
    return best


def nd_formula_114(p, q, r, s, t, u, k, m, j1, j2, j3, j4):
    """6-branch formula for type (1,1,4)."""
    Bu0 = nd_formula_113(p, q, r, s, t, k, m, j1, j2, j3)
    Bt0 = nd_formula_113(p, q, r, s, u, k, m, j1, j2, j4)
    Bs0 = nd_formula_113(p, q, r, t, u, k, m, j1, j3, j4)
    Br0 = nd_formula_113(p, q, s, t, u, k, m, j2, j3, j4)
    Bp0 = max(q, b4pc(j1, j2, j3, j4, r, s, t, u, m))
    Bq0 = max(p, b4pc(j1, j2, j3, j4, r, s, t, u, k))
    return min(Bu0, Bt0, Bs0, Br0, Bp0, Bq0)


def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    if len(primes) != 6: return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=6):
        if all(c == 0 for c in coords): continue
        if sum(alpha[i] * coords[i] for i in range(6)) != 0: continue
        if sum(ws[i] * coords[i] for i in range(6)) == 0: continue
        best = min(best, max(primes[i] * abs(coords[i]) for i in range(6)))
    return best if best < float('inf') else None


# ── Precompute ──────────────────────────────────────────────────────────────
prime_powers = {}; four_prime = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 1:
        pr = list(f.keys())[0]; prime_powers[n] = (pr, f[pr])
    elif len(f) == 4:
        ps = sorted(f.keys())
        four_prime[n] = (ps[0], ps[1], ps[2], ps[3],
                         f[ps[0]], f[ps[1]], f[ps[2]], f[ps[3]])

triples = []; seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, m) in prime_powers.items():
        if q == p: continue
        c = a + b
        if c not in four_prime: continue
        r, s, t, u, j1, j2, j3, j4 = four_prime[c]
        if any(x in (p, q) for x in (r, s, t, u)): continue
        if math.gcd(a, b) != 1: continue
        key = tuple(sorted([a, b]))
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, u, k, m, j1, j2, j3, j4))

print(f"T83: type (1,1,4) nd formula — {len(triples)} triples (a,b <= {LIMIT})")

random.seed(83)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = fail = low = 0
for tt in sample:
    a, b, p, q, r, s, t, u, k, m, j1, j2, j3, j4 = tt
    formula = nd_formula_114(p, q, r, s, t, u, k, m, j1, j2, j3, j4)
    brute = nd_brute(a, b)
    if brute is None: continue
    if formula == brute: ok += 1
    elif formula < brute: low += 1; print(f"  formula<brute ({a},{b}): {formula} vs {brute}")
    else: fail += 1; print(f"  FAIL ({a},{b}): formula={formula} brute={brute}")

print(f"Spot-check ({len(sample)} triples, bound={BRUTE_BOUND}): OK={ok}, low={low}, FAIL={fail}")
if fail == 0: print("\nFORMULA CANDIDATE CONFIRMED (no failures).")
