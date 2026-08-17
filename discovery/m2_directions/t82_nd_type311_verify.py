"""
T82 — Exact nd formula for type (3,1,1) triples.

Type (3,1,1): a = p^k1 * q^k2 * r^k3 (Pa={p,q,r}),
              b = s^m (Pb={s}),
              c = t^n (Pc={t}).
All five primes p,q,r,s,t distinct; gcd(a,b)=1.

Constraint: k1*phi_p + k2*phi_q + k3*phi_r + m*phi_s = n*phi_t
Wronskian:  W = phi_s - (phi_p + phi_q + phi_r) != 0.

5-branch recursive formula:
  B_{p=0}: nd of type-(2,1,1) sub-triple (q^k2*r^k3, s^m, t^n) [Thm nd_type211]
  B_{q=0}: nd of type-(2,1,1) sub-triple (p^k1*r^k3, s^m, t^n) [Thm nd_type211]
  B_{r=0}: nd of type-(2,1,1) sub-triple (p^k1*q^k2, s^m, t^n) [Thm nd_type211]
  N_{t=0}: Pa x Pb homogeneous: k1*phi_p+k2*phi_q+k3*phi_r+m*phi_s=0, phi_s!=phi_p+phi_q+phi_r
  N_{s=0}: Pa x Pc interaction:  k1*phi_p+k2*phi_q+k3*phi_r=n*phi_t, phi_p+phi_q+phi_r!=0
"""

import math
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 300

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = 1
    return f

def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = extended_gcd(b, a % b); return g, y, x - (a // b) * y

# ---- Sub-problem solvers ----

def nd_omega3(k, m, n, p, q, r, search=16):
    """Exact nd for type (1,1,1): W = phi_q - phi_p != 0."""
    best = float('inf')
    gg, u0, v0 = extended_gcd(k, m)
    step_p = m // gg; step_q = k // gg
    denom = p * step_p + q * step_q
    for phi_r in range(-search, search + 1):
        rhs = n * phi_r
        if rhs % gg != 0: continue
        f2 = rhs // gg
        t_opt = (q * v0 * f2 - p * u0 * f2) / denom if denom != 0 else 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_p = u0 * f2 + step_p * t
            phi_q = v0 * f2 - step_q * t
            if phi_q == phi_p: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if phi_p == 0 and phi_q == 0 and phi_r == 0: continue
            if norm > 0 and norm < best: best = norm
    return best

def ns0_min_211(k1, k2, m, p, q, r, search=14):
    """N_{s=0} for type (2,1,1): phi_s=0.
    min max(p|phi_p|,q|phi_q|,r|phi_r|) s.t. k1*phi_p+k2*phi_q+m*phi_r=0, phi_r!=phi_p+phi_q."""
    best = float('inf')
    for phi_r in range(-search, search + 1):
        for phi_p in range(-search, search + 1):
            rhs3 = -(k1 * phi_p) - m * phi_r
            if rhs3 % k2 != 0: continue
            phi_q = rhs3 // k2
            if phi_r == phi_p + phi_q: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r))
            if norm > 0 and norm < best: best = norm
    return best

def nr0_min_211(k1, k2, n, p, q, s, search=14):
    """N_{r=0} for type (2,1,1): phi_r=0.
    min max(p|phi_p|,q|phi_q|,s|phi_s|) s.t. k1*phi_p+k2*phi_q=n*phi_s, phi_s!=0, phi_p+phi_q!=0."""
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
            if phi_p + phi_q == 0: continue
            norm = max(p * abs(phi_p), q * abs(phi_q), s * abs(phi_s))
            if norm < best: best = norm
    return best

def nd_type211(pa1, pa2, pb, pc, k1, k2, m, n, search=14):
    """Exact nd for type (2,1,1): Pa={pa1^k1, pa2^k2}, Pb={pb^m}, Pc={pc^n}.
    Uses 4-branch formula from Theorem thm:nd_type211."""
    return min(
        ns0_min_211(k1, k2, m, pa1, pa2, pb, search),
        nr0_min_211(k1, k2, n, pa1, pa2, pc, search),
        nd_omega3(k1, m, n, pa1, pb, pc, search),
        nd_omega3(k2, m, n, pa2, pb, pc, search),
    )

def nt0_min_311(k1, k2, k3, m, p, q, r, s, search=14):
    """N_{t=0}: phi_t=0. Pa x Pb homogeneous.
    min max(p|phi_p|,q|phi_q|,r|phi_r|,s|phi_s|)
    s.t. k1*phi_p+k2*phi_q+k3*phi_r+m*phi_s=0, phi_s!=phi_p+phi_q+phi_r."""
    best = float('inf')
    for phi_s in range(-search, search + 1):
        for phi_r in range(-search, search + 1):
            for phi_q in range(-search, search + 1):
                rhs = -(k2 * phi_q + k3 * phi_r + m * phi_s)
                if rhs % k1 != 0: continue
                phi_p = rhs // k1
                W = phi_s - (phi_p + phi_q + phi_r)
                if W == 0: continue
                norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r), s * abs(phi_s))
                if norm > 0 and norm < best: best = norm
    return best

def ns0_min_311(k1, k2, k3, n, p, q, r, t, search=14):
    """N_{s=0}: phi_s=0. Pa x Pc interaction.
    min max(p|phi_p|,q|phi_q|,r|phi_r|,t|phi_t|)
    s.t. k1*phi_p+k2*phi_q+k3*phi_r=n*phi_t, phi_p+phi_q+phi_r!=0."""
    best = float('inf')
    for phi_t in range(-search, search + 1):
        for phi_r in range(-search, search + 1):
            for phi_q in range(-search, search + 1):
                rhs = n * phi_t - k2 * phi_q - k3 * phi_r
                if rhs % k1 != 0: continue
                phi_p = rhs // k1
                if phi_p + phi_q + phi_r == 0: continue
                if phi_t == 0 and phi_p + phi_q + phi_r == 0: continue
                norm = max(p * abs(phi_p), q * abs(phi_q), r * abs(phi_r), t * abs(phi_t))
                if norm > 0 and norm < best: best = norm
    return best

def nd_formula_311(p, q, r, s, t, k1, k2, k3, m, n):
    """5-branch formula for type (3,1,1)."""
    return min(
        nd_type211(q, r, s, t, k2, k3, m, n),    # phi_p=0: type (2,1,1)
        nd_type211(p, r, s, t, k1, k3, m, n),    # phi_q=0: type (2,1,1)
        nd_type211(p, q, s, t, k1, k2, m, n),    # phi_r=0: type (2,1,1)
        nt0_min_311(k1, k2, k3, m, p, q, r, s),  # phi_t=0: Pa x Pb homogeneous
        ns0_min_311(k1, k2, k3, n, p, q, r, t),  # phi_s=0: Pa x Pc interaction
    )

def nd_smart_verify_311(p, q, r, s, t, k1, k2, k3, m, n, formula_val):
    """Smart bounded verifier: solve phi_p from constraint, iterate (phi_q,phi_r,phi_s,phi_t)."""
    M = formula_val - 1
    if M <= 0: return True, 0
    bq = M // q; br = M // r; bs = M // s; bt = M // t
    for phi_q in range(-bq, bq + 1):
        for phi_r in range(-br, br + 1):
            for phi_s in range(-bs, bs + 1):
                for phi_t in range(-bt, bt + 1):
                    rhs = n * phi_t - k2 * phi_q - k3 * phi_r - m * phi_s
                    if rhs % k1 != 0: continue
                    phi_p = rhs // k1
                    if p * abs(phi_p) > M: continue
                    if phi_p == 0 and phi_q == 0 and phi_r == 0 and phi_s == 0 and phi_t == 0:
                        continue
                    norm = max(p*abs(phi_p), q*abs(phi_q), r*abs(phi_r),
                               s*abs(phi_s), t*abs(phi_t))
                    if norm > M: continue
                    W = phi_s - (phi_p + phi_q + phi_r)
                    if W != 0:
                        return False, norm
    return True, formula_val

# ---- Build type (3,1,1) triples ----
three_prime_a = {}; prime_powers = {}
for nn in range(2, LIMIT + 1):
    f = factorize(nn)
    if len(f) == 1:
        p2 = list(f.keys())[0]; prime_powers[nn] = (p2, f[p2])
    elif len(f) == 3:
        ps = sorted(f.keys())
        three_prime_a[nn] = (ps[0], ps[1], ps[2], f[ps[0]], f[ps[1]], f[ps[2]])

print(f"T82: type (3,1,1) exact nd verification — smart bounded verifier (LIMIT={LIMIT})")
print("=" * 70)

triples = []; seen = set()
for a, (p, q, r, k1, k2, k3) in three_prime_a.items():
    for b, (s, m) in prime_powers.items():
        if s in (p, q, r): continue
        if math.gcd(a, b) != 1: continue
        c = a + b
        if c not in prime_powers: continue
        t, n = prime_powers[c]
        if t in (p, q, r, s): continue
        key = (a, b)
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, k1, k2, k3, m, n))

print(f"Type (3,1,1) triples found: {len(triples)}")
print()

ok = 0; fail = 0; branch_wins = defaultdict(int)
branch_names = ['B_p0(211)', 'B_q0(211)', 'B_r0(211)', 'N_t0', 'N_s0']

for (a, b, p, q, r, s, t, k1, k2, k3, m, n) in triples:
    fval = nd_formula_311(p, q, r, s, t, k1, k2, k3, m, n)
    tight, found = nd_smart_verify_311(p, q, r, s, t, k1, k2, k3, m, n, fval)

    if tight:
        ok += 1
        bvals = [
            nd_type211(q, r, s, t, k2, k3, m, n),
            nd_type211(p, r, s, t, k1, k3, m, n),
            nd_type211(p, q, s, t, k1, k2, m, n),
            nt0_min_311(k1, k2, k3, m, p, q, r, s),
            ns0_min_311(k1, k2, k3, n, p, q, r, t),
        ]
        for i, v in enumerate(bvals):
            if v == fval: branch_wins[branch_names[i]] += 1
    else:
        fail += 1
        print(f"FAIL: ({a},{b}) p={p}^{k1}*q={q}^{k2}*r={r}^{k3}+s={s}^{m}=t={t}^{n}: "
              f"formula={fval} but found norm={found}")

print(f"Results: {ok} OK, {fail} FAIL")
print()
print("Branch win counts (ties counted in both):")
for nm in branch_names:
    print(f"  {nm:15s}: {branch_wins[nm]:4d}")
print()
if fail == 0:
    print("CANDIDATE FORMULA PASSES: 5-branch formula is exact on all tested triples.")
else:
    print("FORMULA FAILS: needs correction or additional branches.")
