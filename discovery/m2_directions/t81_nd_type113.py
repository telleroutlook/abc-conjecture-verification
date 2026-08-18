"""
T81 — Exact nd formula for type (1,1,3) triples.
a = p^k,  b = q^m,  c = r^j1 * s^j2 * t^j3.
5 distinct primes: Pa={p}, Pb={q}, Pc={r,s,t}.
Constraint: k*phi_p + m*phi_q = j1*phi_r + j2*phi_s + j3*phi_t.
Wronskian: W = phi_q - phi_p.

5-branch formula:
  B_{t=0}: nd_omega4_two_c(p,q,r,s; k,m,j1,j2)   [zero phi_t, type (1,1,2)]
  B_{s=0}: nd_omega4_two_c(p,q,r,t; k,m,j1,j3)   [zero phi_s, type (1,1,2)]
  B_{r=0}: nd_omega4_two_c(p,q,s,t; k,m,j2,j3)   [zero phi_r, type (1,1,2)]
  B_{p=0}: max(q, B3pc(m)) where B3pc(v) = min{max(r|phi|,s|phi|,t|phi|) : j1*a+j2*b+j3*c=v}
  B_{q=0}: max(p, B3pc(k))

Note: B_{p=0} generalises the max(q, B_m) branch of nd_omega4_two_c to 3 Pc primes.
"""

import math
from itertools import product as iproduct
from collections import defaultdict
import random

LIMIT = 100
BB = 15
BRUTE_BOUND = 5
SPOT_N = 40


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


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def bm(m, n, k, pb, pc):
    """min{max(pb|phi_b|,pc|phi_c|) : m*phi_b - n*phi_c = ±k}"""
    best = float("inf")
    g, u0, v0 = egcd(m, n)
    for sgn in [1, -1]:
        rhs = sgn * k
        if rhs % g != 0:
            continue
        s = rhs // g
        up = u0 * s
        vp = -v0 * s
        su = n // g
        sv = m // g
        D = pb * su - pc * sv
        to = (pc * vp - pb * up) / D if D != 0 else 0.0
        for t in range(int(to) - 6, int(to) + 7):
            phi_b = up + su * t
            phi_c = vp + sv * t
            if m * phi_b - n * phi_c != rhs:
                continue
            best = min(best, max(pb * abs(phi_b), pc * abs(phi_c)))
    return best


def nd111(pa, pb, pc, k, m, n):
    g1 = math.gcd(k, m)
    g2 = math.gcd(m, n)
    g3 = math.gcd(k, n)
    N0 = max(pa * m // g1, pb * k // g1)
    N1 = max(pb * n // g2, pc * m // g2)
    N2 = max(pa * n // g3, pc * k // g3)
    if N0 <= pc:
        return N0
    if N1 <= pa:
        return N1
    if N2 <= pb:
        return N2
    pL = max(pa, pb, pc)
    if pL == pa:
        B = bm(m, n, k, pb, pc)
    elif pL == pb:
        B = bm(k, n, m, pa, pc)
    else:
        B = float("inf")
        for ph in [1, -1]:
            for phi_a in range(-40, 41):
                rem = n * ph - k * phi_a
                if rem % m != 0:
                    continue
                phi_b = rem // m
                if phi_b == phi_a:
                    continue
                B = min(B, max(pa * abs(phi_a), pb * abs(phi_b), pc))
    return min(min(N0, N1, N2), max(pL, B))


def nd_omega4_two_c(pa, pb, pc1, pc2, ka, kb, n1, n2):
    """Exact nd for type (1,1,2): Pa={pa^ka}, Pb={pb^kb}, Pc={pc1^n1,pc2^n2}."""
    B1 = nd111(pa, pb, pc1, ka, kb, n1)
    B2 = nd111(pa, pb, pc2, ka, kb, n2)
    B3 = max(pb, bm(n1, n2, kb, pc1, pc2))
    B4 = max(pa, bm(n1, n2, ka, pc1, pc2))
    return min(B1, B2, B3, B4)


def b3pc(j1, j2, j3, r, s, t, v, bnd=BB):
    """min{max(r|a|,s|b|,t|c|) : j1*a+j2*b+j3*c=v} — 3-variable unconstrained Bezout."""
    best = float("inf")
    for a in range(-bnd, bnd + 1):
        for b in range(-bnd, bnd + 1):
            rem = v - j1 * a - j2 * b
            if rem % j3 != 0:
                continue
            c = rem // j3
            nrm = max(r * abs(a), s * abs(b), t * abs(c))
            if nrm > 0 or v == 0:
                best = min(best, nrm)
    return best


def nd_formula_113(p, q, r, s, t, k, m, j1, j2, j3):
    """5-branch formula for type (1,1,3)."""
    Bt0 = nd_omega4_two_c(p, q, r, s, k, m, j1, j2)  # phi_t=0: (1,1,2) at p,q,r,s
    Bs0 = nd_omega4_two_c(p, q, r, t, k, m, j1, j3)  # phi_s=0: (1,1,2) at p,q,r,t
    Br0 = nd_omega4_two_c(p, q, s, t, k, m, j2, j3)  # phi_r=0: (1,1,2) at p,q,s,t
    Bp0 = max(q, b3pc(j1, j2, j3, r, s, t, m))  # phi_p=0: type (0,1,3)
    Bq0 = max(p, b3pc(j1, j2, j3, r, s, t, k))  # phi_q=0: type (1,0,3)
    return min(Bt0, Bs0, Br0, Bp0, Bq0), (Bt0, Bs0, Br0, Bp0, Bq0)


def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    if len(primes) > 6:
        return None
    alpha = [fa.get(pr, fb.get(pr, -fc.get(pr, 0))) for pr in primes]
    ws = [1 if pr in fb else (-1 if pr in fa else 0) for pr in primes]
    best = float("inf")
    for coords in iproduct(range(-bound, bound + 1), repeat=len(primes)):
        if all(c2 == 0 for c2 in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(len(primes))) != 0:
            continue
        if sum(ws[i] * coords[i] for i in range(len(primes))) == 0:
            continue
        best = min(best, max(primes[i] * abs(coords[i]) for i in range(len(primes))))
    return best if best < float("inf") else None


# ── Precompute ──────────────────────────────────────────────────────────────
prime_powers = {}
three_prime = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 1:
        pr = list(f.keys())[0]
        prime_powers[n] = (pr, f[pr])
    elif len(f) == 3:
        ps = sorted(f.keys())
        three_prime[n] = (ps[0], ps[1], ps[2], f[ps[0]], f[ps[1]], f[ps[2]])

# Type (1,1,3): a=prime_power, b=prime_power, c=three_prime
triples = []
seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, m) in prime_powers.items():
        if q == p:
            continue
        c = a + b
        if c not in three_prime:
            continue
        r, s, t, j1, j2, j3 = three_prime[c]
        if r in (p, q) or s in (p, q) or t in (p, q):
            continue
        if math.gcd(a, b) != 1:
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, k, m, j1, j2, j3))

print(f"T81: type (1,1,3) nd formula — {len(triples)} triples (a,b ≤ {LIMIT})")

branch_names = ["B_t0(112)", "B_s0(112)", "B_r0(112)", "B_p0(013)", "B_q0(103)"]
branch_wins = defaultdict(int)
for t in triples:
    a, b, p, q, r, s, tv, k, m, j1, j2, j3 = t
    val, parts = nd_formula_113(p, q, r, s, tv, k, m, j1, j2, j3)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    print(f"  {br:15s}: {cnt:4d}  ({100 * cnt / len(triples):.1f}%)")
print()

# Spot-check
random.seed(55)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = fail = low = 0
for t in sample:
    a, b, p, q, r, s, tv, k, m, j1, j2, j3 = t
    formula, _ = nd_formula_113(p, q, r, s, tv, k, m, j1, j2, j3)
    brute = nd_brute(a, b)
    if brute is None:
        continue
    if formula == brute:
        ok += 1
    elif formula < brute:
        low += 1
        print(f"  formula<brute ({a},{b}): {formula} vs {brute}")
    else:
        fail += 1
        print(f"  FAIL ({a},{b}): formula={formula} brute={brute}")

print(
    f"Spot-check ({len(sample)} triples, bound={BRUTE_BOUND}): OK={ok}, low={low}, FAIL={fail}"
)
if fail == 0:
    print("\nFORMULA CANDIDATE CONFIRMED (no failures).")
