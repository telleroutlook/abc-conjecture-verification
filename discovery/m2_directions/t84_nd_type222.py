"""
T84 — Verify 6-branch recursive nd formula for type (2,2,2) triples.
a = p^k1 * q^k2,  b = r^j1 * s^j2,  c = t^n1 * u^n2.
6 distinct primes: Pa={p,q}, Pb={r,s}, Pc={t,u}.
Constraint: k1*phi_p + k2*phi_q + j1*phi_r + j2*phi_s = n1*phi_t + n2*phi_u.
Wronskian: W = (phi_r+phi_s) - (phi_p+phi_q).

6-branch recursive formula (zero one prime coordinate each time):
  B_{p=0}: nd_type122(q, r, s, t, u; k2, j1, j2, n1, n2)  -- zero phi_p -> (1,2,2)
  B_{q=0}: nd_type122(p, r, s, t, u; k1, j1, j2, n1, n2)  -- zero phi_q -> (1,2,2)
  B_{r=0}: nd_type212(p, q, s, t, u; k1, k2, j2, n1, n2)  -- zero phi_r -> (2,1,2)
  B_{s=0}: nd_type212(p, q, r, t, u; k1, k2, j1, n1, n2)  -- zero phi_s -> (2,1,2)
  B_{t=0}: nd_type221(p, q, r, s, u; k1, k2, j1, j2, n2)  -- zero phi_t -> (2,2,1)
  B_{u=0}: nd_type221(p, q, r, s, t; k1, k2, j1, j2, n1)  -- zero phi_u -> (2,2,1)

nd(a,b) = min(B_{p=0}, B_{q=0}, B_{r=0}, B_{s=0}, B_{t=0}, B_{u=0}).

Results: 409 triples (a,b <= 200), spot-check 30, 0 failures.
"""

import math
import random
from itertools import product as iproduct

LIMIT = 200
BB = 8
BRUTE_BOUND = 3


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


def nd4tc(pa, pb, pc1, pc2, ka, kb, n1, n2):
    return min(nd111(pa, pb, pc1, ka, kb, n1), nd111(pa, pb, pc2, ka, kb, n2),
               max(pb, bm(n1, n2, kb, pc1, pc2)), max(pa, bm(n1, n2, ka, pc1, pc2)))


def nd_p0b(q, r, s, j, m, n, bnd=BB):
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
    return min(nd_s0_121(p, q, r, k, j, m), nd_p0b(q, r, s, j, m, n),
               nd111(p, q, s, k, j, n), nd111(p, r, s, k, m, n))


def nd_u0_221(p, q, r, s, k1, k2, j1, j2, bnd=BB):
    best = float('inf')
    for pp in range(-bnd, bnd + 1):
        for pq in range(-bnd, bnd + 1):
            rhs = -(k1 * pp + k2 * pq)
            for pr in range(-bnd, bnd + 1):
                rem = rhs - j1 * pr
                if rem % j2 != 0: continue
                ps = rem // j2
                if (pr + ps) == (pp + pq): continue
                v = max(p * abs(pp), q * abs(pq), r * abs(pr), s * abs(ps))
                if v > 0: best = min(best, v)
    return best


def nd211(p, q, r, s, k1, k2, j, n, bnd=BB):
    def ns0(p_, q_, r_, k_1, k_2, m_, bnd_=BB):
        best_ = float('inf')
        for pp_ in range(-bnd_, bnd_ + 1):
            for pq_ in range(-bnd_, bnd_ + 1):
                rhs_ = -(k_1 * pp_ + k_2 * pq_)
                if rhs_ % m_ != 0: continue
                pr_ = rhs_ // m_
                if pr_ == (pp_ + pq_): continue
                v_ = max(p_ * abs(pp_), q_ * abs(pq_), r_ * abs(pr_))
                if v_ > 0: best_ = min(best_, v_)
        return best_

    def nr0(p_, q_, s_, k_1, k_2, n_, bnd_=BB):
        best_ = float('inf')
        for pp_ in range(-bnd_, bnd_ + 1):
            for pq_ in range(-bnd_, bnd_ + 1):
                rhs_ = k_1 * pp_ + k_2 * pq_
                if n_ == 0 or rhs_ % n_ != 0: continue
                ps_ = rhs_ // n_
                if pp_ + pq_ == 0: continue
                v_ = max(p_ * abs(pp_), q_ * abs(pq_), s_ * abs(ps_))
                if v_ > 0: best_ = min(best_, v_)
        return best_

    return min(ns0(p, q, r, k1, k2, j), nr0(p, q, s, k1, k2, n),
               nd111(p, r, s, k1, j, n), nd111(q, r, s, k2, j, n))


def nd221(p, q, r, s, u, k1, k2, j1, j2, n):
    Bu0 = nd_u0_221(p, q, r, s, k1, k2, j1, j2)
    Bq0 = nd121(p, r, s, u, k1, j1, j2, n)
    Bp0 = nd121(q, r, s, u, k2, j1, j2, n)
    Bs0 = nd211(p, q, r, u, k1, k2, j1, n)
    Br0 = nd211(p, q, s, u, k1, k2, j2, n)
    return min(Bu0, Bq0, Bp0, Bs0, Br0)


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


def nd_p0_122(q, r, s, t, j, m, j1, j2, bnd=BB):
    best = float('inf')
    for pq in range(-bnd, bnd + 1):
        for pr in range(-bnd, bnd + 1):
            rhs = j * pq + m * pr
            for ps in range(-bnd, bnd + 1):
                rem = rhs - j1 * ps
                if rem % j2 != 0: continue
                pt = rem // j2
                if pq + pr == 0: continue
                v = max(q * abs(pq), r * abs(pr), s * abs(ps), t * abs(pt))
                if v > 0: best = min(best, v)
    return best


def nd122(p, q, r, s, t, k, j, m, j1, j2):
    Np0 = nd_p0_122(q, r, s, t, j, m, j1, j2)
    Bq0 = nd4tc(p, r, s, t, k, m, j1, j2)
    Br0 = nd4tc(p, q, s, t, k, j, j1, j2)
    Bt0 = nd121(p, q, r, s, k, j, m, j1)
    Bs0 = nd121(p, q, r, t, k, j, m, j2)
    return min(Np0, Bq0, Br0, Bt0, Bs0)


def nd212(p, q, r, s, t, k1, k2, m, j1, j2):
    return nd122(r, p, q, s, t, m, k1, k2, j1, j2)


def nd222(p, q, r, s, t, u, k1, k2, j1, j2, n1, n2):
    """Pa={p^k1,q^k2}, Pb={r^j1,s^j2}, Pc={t^n1,u^n2}."""
    Bp0 = nd122(q, r, s, t, u, k2, j1, j2, n1, n2)
    Bq0 = nd122(p, r, s, t, u, k1, j1, j2, n1, n2)
    Br0 = nd212(p, q, s, t, u, k1, k2, j2, n1, n2)
    Bs0 = nd212(p, q, r, t, u, k1, k2, j1, n1, n2)
    Bt0 = nd221(p, q, r, s, u, k1, k2, j1, j2, n2)
    Bu0 = nd221(p, q, r, s, t, k1, k2, j1, j2, n1)
    return min(Bp0, Bq0, Br0, Bs0, Bt0, Bu0)


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


two_prime = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 2:
        ps = sorted(f.keys())
        two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])

triples = []; seen = set()
for a, (p, q, k1, k2) in two_prime.items():
    for b, (r, s, j1, j2) in two_prime.items():
        if r in (p, q) or s in (p, q) or r == s: continue
        c = a + b
        if c not in two_prime: continue
        t, u, n1, n2 = two_prime[c]
        if t in (p, q, r, s) or u in (p, q, r, s) or t == u: continue
        if math.gcd(a, b) != 1: continue
        key = tuple(sorted([a, b]))
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, u, k1, k2, j1, j2, n1, n2))

print(f"T84: type (2,2,2) omega*=6: {len(triples)} triples (a,b <= {LIMIT})")

random.seed(84)
sample = random.sample(triples, min(30, len(triples)))
ok = fail = low = 0
for tt in sample:
    a, b, p, q, r, s, t, u, k1, k2, j1, j2, n1, n2 = tt
    f = nd222(p, q, r, s, t, u, k1, k2, j1, j2, n1, n2)
    br = nd_brute(a, b)
    if br is None: continue
    if f == br: ok += 1
    elif f < br: low += 1; print(f"  low ({a},{b}): f={f} br={br}")
    else: fail += 1; print(f"  FAIL ({a},{b}): f={f} br={br}")

print(f"Spot-check ({len(sample)} triples, bound={BRUTE_BOUND}): OK={ok}, low={low}, FAIL={fail}")
if fail == 0: print("\nFORMULA CANDIDATE CONFIRMED (no failures).")
