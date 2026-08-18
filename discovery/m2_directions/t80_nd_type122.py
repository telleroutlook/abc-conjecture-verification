"""
T80 — Exact nd formula for type (1,2,2) triples.
a = p^k,  b = q^j * r^m,  c = s^j1 * t^j2.
5 distinct primes: Pa={p}, Pb={q,r}, Pc={s,t}.
Constraint: k*phi_p + j*phi_q + m*phi_r = j1*phi_s + j2*phi_t.
Wronskian: W = (phi_q + phi_r) - phi_p.

5-branch formula (zero one coordinate each time):
  N_{p=0}: Pb x Pc homogeneous interaction:
           j*phi_q + m*phi_r - j1*phi_s - j2*phi_t = 0, phi_q+phi_r != 0
  B_{q=0}: nd_omega4_two_c(p^k, r^m, s^j1, t^j2)  [type (1,1,2)]
  B_{r=0}: nd_omega4_two_c(p^k, q^j, s^j1, t^j2)  [type (1,1,2)]
  B_{t=0}: nd_type121(p^k, {q^j,r^m}, s^j1)        [type (1,2,1)]
  B_{s=0}: nd_type121(p^k, {q^j,r^m}, t^j2)        [type (1,2,1)]

By Pa<->Pb symmetry with type (2,1,2):
  type (2,1,2): Pa={p,q}, Pb={r}, Pc={s,t} follows by swapping a and b labels.
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


# ── type (1,1,2) nd formula (thm:nd_omega4_two_c) ─────────────────────────
def nd_omega4_two_c(pa, pb, pc1, pc2, ka, kb, n1, n2):
    """Pa={pa^ka}, Pb={pb^kb}, Pc={pc1^n1, pc2^n2}. 4 branches per paper thm.
    branch 1 (phi_pc2=0): nd111(pa,pb,pc1,ka,kb,n1)
    branch 2 (phi_pc1=0): nd111(pa,pb,pc2,ka,kb,n2)
    branch 3 (phi_pa=0):  max(pb, B_kb) where B_kb = bm(n1,n2,kb,pc1,pc2)
    branch 4 (phi_pb=0):  max(pa, B_ka) where B_ka = bm(n1,n2,ka,pc1,pc2)
    """
    B1 = nd111(pa, pb, pc1, ka, kb, n1)
    B2 = nd111(pa, pb, pc2, ka, kb, n2)
    B3 = max(pb, bm(n1, n2, kb, pc1, pc2))
    B4 = max(pa, bm(n1, n2, ka, pc1, pc2))
    return min(B1, B2, B3, B4)


# ── type (1,2,1) nd formula (thm:nd_type121) ──────────────────────────────
def nd_p0_b(q, r, s, j, m, n, bnd=BB):
    best = float("inf")
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = j * pq + m * pr
            if n == 0 or rhs % n != 0:
                continue
            ps = rhs // n
            if pq + pr == 0:
                continue
            v = max(q * abs(pq), r * abs(pr), s * abs(ps))
            if v > 0:
                best = min(best, v)
    return best


def nd_s0_121(p, q, r, k, j, m, bnd=BB):
    best = float("inf")
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = -(j * pq + m * pr)
            if rhs % k != 0:
                continue
            pp = rhs // k
            if (pq + pr) == pp:
                continue
            v = max(p * abs(pp), q * abs(pq), r * abs(pr))
            if v > 0:
                best = min(best, v)
    return best


def nd121(p, q, r, s, k, j, m, n):
    return min(
        nd_s0_121(p, q, r, k, j, m),
        nd_p0_b(q, r, s, j, m, n),
        nd111(p, q, s, k, j, n),
        nd111(p, r, s, k, m, n),
    )


# ── N_{p=0}: Pb x Pc homogeneous interaction ──────────────────────────────
def nd_p0_branch_122(q, r, s, t, j, m, j1, j2, bnd=BB):
    """phi_p=0: j*phi_q + m*phi_r - j1*phi_s - j2*phi_t = 0, W=(phi_q+phi_r)!=0."""
    best = float("inf")
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = j * pq + m * pr
            for ps in range(-bnd, bnd + 1):
                rem = rhs - j1 * ps
                if rem % j2 != 0:
                    continue
                pt = rem // j2
                if pq + pr == 0:
                    continue
                v = max(q * abs(pq), r * abs(pr), s * abs(ps), t * abs(pt))
                if v > 0:
                    best = min(best, v)
    return best


def nd_formula_122(p, q, r, s, t, k, j, m, j1, j2):
    """5-branch formula for type (1,2,2)."""
    Np0 = nd_p0_branch_122(q, r, s, t, j, m, j1, j2)
    Bq0 = nd_omega4_two_c(p, r, s, t, k, m, j1, j2)  # phi_q=0 -> (1,1,2)
    Br0 = nd_omega4_two_c(p, q, s, t, k, j, j1, j2)  # phi_r=0 -> (1,1,2)
    Bt0 = nd121(p, q, r, s, k, j, m, j1)  # phi_t=0 -> (1,2,1)
    Bs0 = nd121(p, q, r, t, k, j, m, j2)  # phi_s=0 -> (1,2,1)
    return min(Np0, Bq0, Br0, Bt0, Bs0), (Np0, Bq0, Br0, Bt0, Bs0)


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
two_prime = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 1:
        pr = list(f.keys())[0]
        prime_powers[n] = (pr, f[pr])
    elif len(f) == 2:
        ps = sorted(f.keys())
        two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])

# Type (1,2,2): a=prime_power, b=two_prime, c=two_prime
triples = []
seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, r, j, m) in two_prime.items():
        if q == p or r == p:
            continue
        c = a + b
        if c not in two_prime:
            continue
        s, t, j1, j2 = two_prime[c]
        if s in (p, q, r) or t in (p, q, r) or s == t:
            continue
        if math.gcd(a, b) != 1:
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, k, j, m, j1, j2))

print(f"T80: type (1,2,2) nd formula — {len(triples)} triples (a,b ≤ {LIMIT})")

branch_names = ["N_{p=0}", "B_q0(112)", "B_r0(112)", "B_t0(121)", "B_s0(121)"]
branch_wins = defaultdict(int)
for t in triples:
    a, b, p, q, r, s, tv, k, j, m, j1, j2 = t
    val, parts = nd_formula_122(p, q, r, s, tv, k, j, m, j1, j2)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    print(f"  {br:15s}: {cnt:4d}  ({100 * cnt / len(triples):.1f}%)")
print()

# Spot-check
random.seed(31)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = fail = low = 0
for t in sample:
    a, b, p, q, r, s, tv, k, j, m, j1, j2 = t
    formula, _ = nd_formula_122(p, q, r, s, tv, k, j, m, j1, j2)
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
