"""
T78_formula — Verify the 4-branch exact nd formula for type (1,2,1) triples.

Type (1,2,1): a = p^k (Pa = {p}),
              b = q^j * r^m (Pb = {q,r}, q<r),
              c = s^n (Pc = {s}).
All four primes p,q,r,s distinct; gcd(a,b)=1.

By Pa<->Pb symmetry with thm:nd_type211, the 4-branch formula is:
  nd(a,b) = min(N_{s=0}, N_{p=0}, nd3(p^k,q^j,s^n), nd3(p^k,r^m,s^n))

  N_{s=0}: phi_s=0; Pb x Pa interaction
           min{max(p|phi_p|,q|phi_q|,r|phi_r|): k*phi_p+j*phi_q+m*phi_r=0,
               (phi_q+phi_r) != phi_p}
           (subsumes W_b and pairwise pw(k,j,p,q), pw(k,m,p,r))

  N_{p=0}: phi_p=0; Pb x Pc interaction
           min{max(q|phi_q|,r|phi_r|,s|phi_s|): j*phi_q+m*phi_r=n*phi_s,
               phi_q+phi_r != 0}
           (subsumes pairwise pw(j,n,q,s), pw(m,n,r,s))

  nd3_r0:  phi_r=0; omega*=3 sub-problem (p^k, q^j, s^n)
  nd3_q0:  phi_q=0; omega*=3 sub-problem (p^k, r^m, s^n)
"""

import math
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 200
BOUND = 10

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = 1
    return f

def nd_brute(a, b):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ < 3 or np_ > 5: return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-BOUND, BOUND + 1), repeat=np_):
        if all(c2 == 0 for c2 in coords): continue
        if sum(alpha[i] * coords[i] for i in range(np_)) != 0: continue
        W = sum(ws[i] * coords[i] for i in range(np_))
        if W == 0: continue
        norm = max(primes[i] * abs(coords[i]) for i in range(np_))
        if norm > 0: best = min(best, norm)
    return best if best < float('inf') else None

def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = extended_gcd(b, a % b); return g, y, x - (a // b) * y

def ns0_min_121(k, j, m, p, q, r, search=14):
    """
    N_{s=0}: phi_s=0.
    Minimize max(p|phi_p|, q|phi_q|, r|phi_r|)
    subject to k*phi_p + j*phi_q + m*phi_r = 0, (phi_q+phi_r) != phi_p.
    """
    best = float('inf')
    for phi_r in range(-search, search + 1):
        for phi_q in range(-search, search + 1):
            rhs = -(j * phi_q + m * phi_r)
            if rhs % k != 0: continue
            phi_p = rhs // k
            W = (phi_q + phi_r) - phi_p
            if W == 0: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0 and norm < best: best = norm
    return best

def np0_min_121(j, m, n, q, r, s, search=14):
    """
    N_{p=0}: phi_p=0.
    Minimize max(q|phi_q|, r|phi_r|, s|phi_s|)
    subject to j*phi_q + m*phi_r = n*phi_s, phi_q+phi_r != 0.
    """
    best = float('inf')
    gg, u0, v0 = extended_gcd(j, m)
    step_q = m // gg; step_r = j // gg
    denom = q * step_q + r * step_r
    for phi_s in range(-search, search + 1):
        rhs = n * phi_s
        if rhs % gg != 0: continue
        f2 = rhs // gg
        t_opt = (r * v0 * f2 - q * u0 * f2) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_q = u0 * f2 + step_q * t
            phi_r = v0 * f2 - step_r * t
            if phi_q + phi_r == 0: continue
            norm = max(q * abs(phi_q), r * abs(phi_r), s * abs(phi_s))
            if phi_q == 0 and phi_r == 0 and phi_s == 0: continue
            if norm > 0 and norm < best: best = norm
    return best

def nd_omega3_min(k, ek, en, pk, pr, ps, search=14):
    """
    omega*=3 sub-problem: min max(pk|phi_p|, pr|phi_r|, ps|phi_s|)
    subject to k*phi_p + ek*phi_r = en*phi_s, W=phi_r-phi_p != 0.
    (Used for both nd3_r0 and nd3_q0 branches.)
    """
    best = float('inf')
    gg, u0, v0 = extended_gcd(k, ek)
    step_p = ek // gg; step_r = k // gg
    denom = pk * step_p + pr * step_r
    for phi_s in range(-search, search + 1):
        rhs = en * phi_s
        if rhs % gg != 0: continue
        f2 = rhs // gg
        t_opt = (pr * v0 * f2 - pk * u0 * f2) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_p = u0 * f2 + step_p * t
            phi_r = v0 * f2 - step_r * t
            if phi_r - phi_p == 0: continue
            norm = max(pk * abs(phi_p), pr * abs(phi_r), ps * abs(phi_s))
            if phi_p == 0 and phi_r == 0 and phi_s == 0: continue
            if norm > 0 and norm < best: best = norm
    return best

def nd_formula_121(p, q, r, s, k, j, m, n):
    """
    4-branch formula for type (1,2,1).
    Pa={p^k}, Pb={q^j,r^m}, Pc={s^n}, all primes distinct.
    """
    return min(
        ns0_min_121(k, j, m, p, q, r),          # phi_s=0: Pa x Pb interaction
        np0_min_121(j, m, n, q, r, s),           # phi_p=0: Pb x Pc interaction
        nd_omega3_min(k, j, n, p, q, s),         # phi_r=0: omega*=3 (p^k,q^j,s^n)
        nd_omega3_min(k, m, n, p, r, s),         # phi_q=0: omega*=3 (p^k,r^m,s^n)
    )

# ---- Main verification ----
print(f"T78_formula: 4-branch nd formula for type (1,2,1) triples (LIMIT={LIMIT}, BOUND={BOUND})")
print("=" * 75)

prime_powers = {}; two_prime_b = {}
for nn in range(2, LIMIT + 1):
    f = factorize(nn)
    if len(f) == 1:
        p2 = list(f.keys())[0]; prime_powers[nn] = (p2, f[p2])
    elif len(f) == 2:
        ps = sorted(f.keys())
        two_prime_b[nn] = (ps[0], ps[1], f[ps[0]], f[ps[1]])

triples = []; seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, r_p, j, m) in two_prime_b.items():
        r = r_p
        if p in (q, r): continue
        c = a + b
        if c > 2 * LIMIT or c not in prime_powers: continue
        s, n = prime_powers[c]
        if s in (p, q, r): continue
        if math.gcd(a, b) != 1: continue
        key = (a, b)
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k, j, m, n))

print(f"Type (1,2,1) triples found: {len(triples)}")
print()

ok = 0; fail = 0; branch_wins = defaultdict(int)
branch_names = ['N_s0', 'N_p0', 'nd3_r0', 'nd3_q0']

for (a, b, p, q, r, s, k, j, m, n) in triples:
    nd = nd_brute(a, b)
    if nd is None: continue
    f_nd = nd_formula_121(p, q, r, s, k, j, m, n)
    if f_nd == nd:
        ok += 1
        bvals = [
            ns0_min_121(k, j, m, p, q, r),
            np0_min_121(j, m, n, q, r, s),
            nd_omega3_min(k, j, n, p, q, s),
            nd_omega3_min(k, m, n, p, r, s),
        ]
        for i, v in enumerate(bvals):
            if v == nd: branch_wins[branch_names[i]] += 1
    else:
        fail += 1
        print(f"FAIL: ({a},{b}) p={p}^{k} q={q}^{j}*{r}^{m}+{s}^{n}: nd={nd} formula={f_nd}")

print(f"Results: {ok} OK, {fail} FAIL")
print()
print("Branch win counts (ties counted in both):")
for nm in branch_names:
    print(f"  {nm:10s}: {branch_wins[nm]:4d}")

if fail == 0:
    print()
    print("PASS: 4-branch nd_formula_121 is exact on all tested triples.")
