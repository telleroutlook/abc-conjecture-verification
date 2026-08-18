"""
T79 — Exact nd formula for type (2,2,1) triples.
a = p^k1 * q^k2,  b = r^j1 * s^j2,  c = u^n.
5 primes: Pa={p,q}, Pb={r,s}, Pc={u}.
Constraint: k1*phi_p + k2*phi_q + j1*phi_r + j2*phi_s = n*phi_u.
Wronskian: W = (phi_r + phi_s) - (phi_p + phi_q).

Hypothesis: nd = min over 5 "reduce-by-one-prime" branches:
  B_u0  = N_{u=0}: Pa x Pb interaction (phi_u=0, 4-prime problem)
  B_q0  = nd4_type121(p,r,s,u; k1,j1,j2,n): phi_q=0 -> (1,2,1) sub-problem
  B_p0  = nd4_type121(q,r,s,u; k2,j1,j2,n): phi_p=0 -> (1,2,1) sub-problem
  B_s0  = nd4_type211(p,q,r,u; k1,k2,j1,n): phi_s=0 -> (2,1,1) sub-problem
  B_r0  = nd4_type211(p,q,s,u; k1,k2,j2,n): phi_r=0 -> (2,1,1) sub-problem

Note: 2-prime cross-group norms and within-group norms are subsumed by B_u0:
  within-Pa (valid iff k1!=k2): zero phi_r,phi_s,phi_u
  within-Pb (valid iff j1!=j2): zero phi_p,phi_q,phi_u
  All Pa x Pb pairwise norms: zero 3 of {phi_p,phi_q,phi_r,phi_s}
"""

import math
from itertools import product as iproduct
from collections import defaultdict
import random

LIMIT = 100
BRANCH_BOUND = 15
BRUTE_BOUND = 5
SPOT_N = 30


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
            best = min(best, max(pb * abs(phi_b), pc * abs(phi_c)))
    return best


def nd_111(pa, pb, pc, k, m, n):
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
    pL = max(pa, pb, pc)
    if pL == pa:
        B = bezout_min_norm(m, n, k, pb, pc)
    elif pL == pb:
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
    return min(min(N0, N1, N2), max(pL, B))


def nd_zero_s_branch(p, q, r, k1, k2, m, bound=BRANCH_BOUND):
    """phi_s=0 for type (2,1,1): k1*phi_p+k2*phi_q+m*phi_r=0, W=phi_r-(phi_p+phi_q)!=0."""
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


def nd_zero_r_branch(p, q, s, k1, k2, nv, bound=BRANCH_BOUND):
    """phi_r=0 for type (2,1,1): k1*phi_p+k2*phi_q=n*phi_s, -(phi_p+phi_q)!=0."""
    best = float("inf")
    for phi_p in range(-bound, bound + 1):
        for phi_q in range(-bound, bound + 1):
            rhs = k1 * phi_p + k2 * phi_q
            if nv == 0 or rhs % nv != 0:
                continue
            phi_s = rhs // nv
            if phi_p + phi_q == 0:
                continue
            norm = max(p * abs(phi_p), q * abs(phi_q), s * abs(phi_s))
            if norm > 0:
                best = min(best, norm)
    return best


def nd_type211(p, q, r, s, k1, k2, m, n):
    """4-branch nd for type (2,1,1): Pa={p^k1,q^k2}, Pb={r^m}, Pc={s^n}."""
    N_s0 = nd_zero_s_branch(p, q, r, k1, k2, m)
    N_r0 = nd_zero_r_branch(p, q, s, k1, k2, n)
    B3 = nd_111(p, r, s, k1, m, n)
    B4 = nd_111(q, r, s, k2, m, n)
    return min(N_s0, N_r0, B3, B4)


def nd_p0_branch(q, r, s, j, m, n, bound=BRANCH_BOUND):
    """phi_p=0 for type (1,2,1): j*phi_q+m*phi_r=n*phi_s, phi_q+phi_r!=0."""
    best = float("inf")
    for phi_q in range(-bound, bound + 1):
        for phi_r in range(-bound, bound + 1):
            rhs = j * phi_q + m * phi_r
            if n == 0 or rhs % n != 0:
                continue
            phi_s = rhs // n
            if phi_q + phi_r == 0:
                continue
            norm = max(q * abs(phi_q), r * abs(phi_r), s * abs(phi_s))
            if norm > 0:
                best = min(best, norm)
    return best


def nd_s0_121_branch(p, q, r, k, j, m, bound=BRANCH_BOUND):
    """phi_s=0 for type (1,2,1): k*phi_p+j*phi_q+m*phi_r=0, (phi_q+phi_r)-phi_p!=0."""
    best = float("inf")
    for phi_q in range(-bound, bound + 1):
        for phi_r in range(-bound, bound + 1):
            rhs = -(j * phi_q + m * phi_r)
            if rhs % k != 0:
                continue
            phi_p = rhs // k
            if (phi_q + phi_r) == phi_p:
                continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0:
                best = min(best, norm)
    return best


def nd_type121(p, q, r, s, k, j, m, n):
    """4-branch nd for type (1,2,1): Pa={p^k}, Pb={q^j,r^m}, Pc={s^n}."""
    N_s0 = nd_s0_121_branch(p, q, r, k, j, m)
    N_p0 = nd_p0_branch(q, r, s, j, m, n)
    B3 = nd_111(p, q, s, k, j, n)
    B4 = nd_111(p, r, s, k, m, n)
    return min(N_s0, N_p0, B3, B4)


def nd_u0_branch(p, q, r, s, k1, k2, j1, j2, bound=BRANCH_BOUND):
    """phi_u=0: Pa x Pb interaction. k1*phi_p+k2*phi_q+j1*phi_r+j2*phi_s=0,
    W=(phi_r+phi_s)-(phi_p+phi_q)!=0. 4-prime problem."""
    best = float("inf")
    for phi_p in range(-bound, bound + 1):
        for phi_q in range(-bound, bound + 1):
            rhs = -(k1 * phi_p + k2 * phi_q)
            for phi_r in range(-bound, bound + 1):
                rem = rhs - j1 * phi_r
                if rem % j2 != 0:
                    continue
                phi_s = rem // j2
                W = (phi_r + phi_s) - (phi_p + phi_q)
                if W == 0:
                    continue
                norm = max(
                    p * abs(phi_p), q * abs(phi_q), r * abs(phi_r), s * abs(phi_s)
                )
                if norm > 0:
                    best = min(best, norm)
    return best


def nd_formula_221(p, q, r, s, u, k1, k2, j1, j2, n):
    """5-branch formula for type (2,2,1)."""
    B_u0 = nd_u0_branch(p, q, r, s, k1, k2, j1, j2)
    B_q0 = nd_type121(p, r, s, u, k1, j1, j2, n)  # phi_q=0: (1,2,1) Pa=p, Pb={r,s}
    B_p0 = nd_type121(q, r, s, u, k2, j1, j2, n)  # phi_p=0: (1,2,1) Pa=q, Pb={r,s}
    B_s0 = nd_type211(p, q, r, u, k1, k2, j1, n)  # phi_s=0: (2,1,1) Pa={p,q}, Pb=r
    B_r0 = nd_type211(p, q, s, u, k1, k2, j2, n)  # phi_r=0: (2,1,1) Pa={p,q}, Pb=s
    return min(B_u0, B_q0, B_p0, B_s0, B_r0), (B_u0, B_q0, B_p0, B_s0, B_r0)


def nd_brute(a, b, bound=BRUTE_BOUND):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ > 6:
        return None
    alpha = [fa.get(pr, fb.get(pr, -fc.get(pr, 0))) for pr in primes]
    ws = [1 if pr in fb else (-1 if pr in fa else 0) for pr in primes]
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
        pr = list(f.keys())[0]
        prime_powers[n] = (pr, f[pr])

# Type (2,2,1): a=two_prime, b=two_prime, c=prime_power
triples = []
seen = set()
for a, (p, q, k1, k2) in two_prime.items():
    for b, (r, s, j1, j2) in two_prime.items():
        if r in (p, q) or s in (p, q) or r == s:
            continue
        c = a + b
        if c not in prime_powers:
            continue
        u, nv = prime_powers[c]
        if u in (p, q, r, s):
            continue
        if math.gcd(a, b) != 1:
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, u, k1, k2, j1, j2, nv))

print(f"T79: type (2,2,1) nd formula — {len(triples)} triples (a,b ≤ {LIMIT})")

branch_names = ["B_u0", "B_q0(121)", "B_p0(121)", "B_s0(211)", "B_r0(211)"]
branch_wins = defaultdict(int)
for a, b, p, q, r, s, u, k1, k2, j1, j2, nv in triples:
    formula, parts = nd_formula_221(p, q, r, s, u, k1, k2, j1, j2, nv)
    winner_idx = parts.index(min(parts))
    branch_wins[branch_names[winner_idx]] += 1

print("Branch win distribution:")
for br, cnt in sorted(branch_wins.items(), key=lambda x: -x[1]):
    print(f"  {br:16s}: {cnt:4d}  ({100 * cnt / len(triples):.1f}%)")
print()

# Spot-check
random.seed(17)
sample = random.sample(triples, min(SPOT_N, len(triples)))
ok = 0
fail = 0
low = 0
for a, b, p, q, r, s, u, k1, k2, j1, j2, nv in sample:
    formula, _ = nd_formula_221(p, q, r, s, u, k1, k2, j1, j2, nv)
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
