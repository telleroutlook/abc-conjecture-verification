"""
T77 — Verification of the exact nd formula for type (2,1,1) triples.

Type (2,1,1): a = p^k1 * q^k2 (Pa has exactly 2 distinct primes p<q),
              b = r^m  (Pb = {r}),
              c = s^n  (Pc = {s}).
All four primes p,q,r,s distinct; gcd(a,b)=1.

The formula has 10 branches:
  1. W_ab        = max(p*k2/g, q*k1/g)  [within-group; valid iff k1/g != k2/g]
  2. pw(k1,m,p,r)                         [phi_q=phi_s=0]
  3. pw(k2,m,q,r)                         [phi_p=phi_s=0]
  4. pw(k1,n,p,s)                         [phi_q=phi_r=0]
  5. pw(k2,n,q,s)                         [phi_p=phi_r=0]
  6. pw(m,n,r,s)                          [phi_p=phi_q=0]
  7. N_r0        [phi_r=0; Pa x Pc interaction]
  8. N_s0        [phi_s=0; Pa x Pb interaction]
  9. nd3_q0      [phi_q=0; omega*=3 sub-problem (p^k1, r^m, s^n)]
 10. nd3_p0      [phi_p=0; omega*=3 sub-problem (q^k2, r^m, s^n)]

Result: formula agrees with brute-force nd on all triples in [4,LIMIT)x[1,LIMIT).
"""

import math
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 150   # a, b, c <= 2*LIMIT
BOUND = 10    # brute-force search bound

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

def pw(v1, v2, p1, p2):
    """Pairwise Bezout norm: max(p1*(v2/g), p2*(v1/g)), g=gcd(v1,v2)."""
    g = math.gcd(v1, v2)
    return max(p1 * (v2 // g), p2 * (v1 // g))

def nr0_min(k1, k2, n, p, q, s, search=14):
    """
    Branch 7: phi_r=0. Minimize max(p|phi_p|, q|phi_q|, s|phi_s|)
    subject to k1*phi_p + k2*phi_q = n*phi_s, phi_p + phi_q != 0.
    """
    best = float('inf')
    gg, u0, v0 = extended_gcd(k1, k2)
    step_p = k2 // gg; step_q = k1 // gg
    denom = p * step_p + q * step_q
    for phi_s in range(-search, search + 1):
        if phi_s == 0: continue
        rhs = n * phi_s
        if rhs % gg != 0: continue
        f2 = rhs // gg
        t_opt = (q * v0 * f2 - p * u0 * f2) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_p = u0 * f2 + step_p * t
            phi_q = v0 * f2 - step_q * t
            if phi_p + phi_q == 0: continue  # Wronskian = 0
            norm = max(p * abs(phi_p), q * abs(phi_q), s * abs(phi_s))
            if norm < best: best = norm
    return best

def ns0_min(k1, k2, m, p, q, r, search=14):
    """
    Branch 8: phi_s=0. Minimize max(p|phi_p|, q|phi_q|, r|phi_r|)
    subject to k1*phi_p + k2*phi_q + m*phi_r = 0, phi_r != phi_p + phi_q.
    """
    best = float('inf')
    for phi_r in range(-search, search + 1):
        for phi_p in range(-search, search + 1):
            rhs3 = -(k1 * phi_p) - m * phi_r
            if rhs3 % k2 != 0: continue
            phi_q = rhs3 // k2
            W = phi_r - (phi_p + phi_q)
            if W == 0: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0 and norm < best: best = norm
    return best

def nd_omega3_min(k, m, n, p, r, s, search=14):
    """
    Branches 9/10: phi_q=0 (or phi_p=0). Minimize max(p|phi_p|, r|phi_r|, s|phi_s|)
    subject to k*phi_p + m*phi_r = n*phi_s, W = phi_r - phi_p != 0.
    This is the exact nd for the omega*=3 sub-problem (p^k, r^m, s^n).
    """
    best = float('inf')
    gg, u0, v0 = extended_gcd(k, m)
    step_p = m // gg; step_r = k // gg
    denom = p * step_p + r * step_r
    for phi_s in range(-search, search + 1):
        rhs = n * phi_s
        if rhs % gg != 0: continue
        f2 = rhs // gg
        t_opt = (r * v0 * f2 - p * u0 * f2) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_p = u0 * f2 + step_p * t
            phi_r = v0 * f2 - step_r * t
            if phi_r - phi_p == 0: continue
            norm = max(p * abs(phi_p), r * abs(phi_r), s * abs(phi_s))
            if phi_p == 0 and phi_r == 0 and phi_s == 0: continue
            if norm > 0 and norm < best: best = norm
    return best

def nd_formula_211(p, q, r, s, k1, k2, m, n):
    """
    10-branch exact nd formula for type (2,1,1) triples.
    Pa={p^k1,q^k2}, Pb={r^m}, Pc={s^n}, all primes distinct.
    """
    g = math.gcd(k1, k2)
    W_ab = max(p * (k2 // g), q * (k1 // g)) if (k2 // g) != (k1 // g) else float('inf')
    branches = [
        W_ab,                           # 1: within-group
        pw(k1, m, p, r),                # 2: phi_q=phi_s=0
        pw(k2, m, q, r),                # 3: phi_p=phi_s=0
        pw(k1, n, p, s),                # 4: phi_q=phi_r=0
        pw(k2, n, q, s),                # 5: phi_p=phi_r=0
        pw(m, n, r, s),                 # 6: phi_p=phi_q=0
        nr0_min(k1, k2, n, p, q, s),   # 7: phi_r=0 (Pa x Pc)
        ns0_min(k1, k2, m, p, q, r),   # 8: phi_s=0 (Pa x Pb)
        nd_omega3_min(k1, m, n, p, r, s),  # 9: phi_q=0
        nd_omega3_min(k2, m, n, q, r, s),  # 10: phi_p=0
    ]
    return min(branches)

# ---- Main verification ----
print(f"T77: Exact nd formula for type (2,1,1) triples (LIMIT={LIMIT}, BOUND={BOUND})")
print("=" * 70)

two_prime = {}; prime_powers = {}
for n in range(2, LIMIT + 1):
    f = factorize(n)
    if len(f) == 2:
        ps = sorted(f.keys())
        two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])
    elif len(f) == 1:
        p2 = list(f.keys())[0]; prime_powers[n] = (p2, f[p2])

triples = []; seen = set()
for a, (p, q, k1, k2) in two_prime.items():
    for b, (r, m) in prime_powers.items():
        if r in (p, q): continue
        c = a + b
        if c > 2 * LIMIT or c not in prime_powers: continue
        s, nv = prime_powers[c]
        if s in (p, q, r): continue
        if math.gcd(a, b) != 1: continue
        key = (a, b)
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k1, k2, m, nv))

print(f"Type (2,1,1) triples found: {len(triples)}")
print()

ok = 0; fail = 0; branch_wins = defaultdict(int)
branch_names = ['W_ab','pw(p,r)','pw(q,r)','pw(p,s)','pw(q,s)','pw(r,s)',
                'N_r0','N_s0','nd3_q0','nd3_p0']

for (a, b, p, q, r, s, k1, k2, m, nv) in triples:
    nd = nd_brute(a, b)
    if nd is None: continue

    f_nd = nd_formula_211(p, q, r, s, k1, k2, m, nv)
    if f_nd == nd:
        ok += 1
        # Track which branches achieve minimum
        g = math.gcd(k1, k2)
        W_ab = max(p*(k2//g),q*(k1//g)) if (k2//g)!=(k1//g) else float('inf')
        bvals = [
            W_ab, pw(k1,m,p,r), pw(k2,m,q,r), pw(k1,nv,p,s), pw(k2,nv,q,s), pw(m,nv,r,s),
            nr0_min(k1,k2,nv,p,q,s), ns0_min(k1,k2,m,p,q,r),
            nd_omega3_min(k1,m,nv,p,r,s), nd_omega3_min(k2,m,nv,q,r,s),
        ]
        for i, v in enumerate(bvals):
            if v == nd: branch_wins[branch_names[i]] += 1
    else:
        fail += 1
        print(f"FAIL: ({a},{b}) {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}: nd={nd} formula={f_nd}")

print(f"Results: {ok} OK, {fail} FAIL")
print()
print("Branch win counts (ties counted in both):")
for nm in branch_names:
    print(f"  {nm:10s}: {branch_wins[nm]:4d}")

if fail == 0:
    print()
    print("PASS: nd_formula_211 is exact on all tested triples.")
