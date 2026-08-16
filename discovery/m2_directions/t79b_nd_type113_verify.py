"""
T79b — Fast exact nd verification for type (1,1,3) triples.

Strategy: instead of O(BOUND^5) brute-force, use a bounded smart verifier:
  - Iterate over (phi_q, phi_r, phi_s, phi_t) up to bound M//prime
  - Solve phi_p from constraint k*phi_p = n1*phi_r + n2*phi_s + n3*phi_t - m*phi_q
  - Only search norm < formula_value (proving the formula is a tight upper bound)

This is O((M/r)*(M/s)*(M/t)*(M/q)) ~ M^4/(r*s*t*q) per triple, where M = formula_value.
For typical small triples (c=2*3*5=30, M~10, q~20), this is < 1000 iterations vs ~4M.
"""

import math
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 250

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

# ---- Exact sub-problem solvers ----

def nd_omega3(k, m, n, p, q, r, search=16):
    """Exact nd for type (1,1,1): p^k + q^m = r^n, W = phi_q - phi_p != 0."""
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

def Bx(x, n1, n2, r, s):
    """min max(r|phi_r|, s|phi_s|) s.t. n1*phi_r + n2*phi_s = x."""
    if x == 0: return 0
    gg, u0, v0 = extended_gcd(n1, n2)
    if x % gg != 0: return float('inf')
    f2 = x // gg
    step_r = n2 // gg; step_s = n1 // gg
    denom = r * step_r + s * step_s
    best = float('inf')
    t_opt = (s * v0 * f2 - r * u0 * f2) / denom if denom != 0 else 0.0
    for t in range(int(t_opt) - 6, int(t_opt) + 7):
        phi_r = u0 * f2 + step_r * t
        phi_s = v0 * f2 - step_s * t
        nm = max(r * abs(phi_r), s * abs(phi_s))
        if nm > 0: best = min(best, nm)
    return best

def nd_omega4_two_c(k, m, n1, n2, p, q, r, s, search=14):
    """Exact nd for type (1,1,2): 4-branch formula."""
    b_s0 = nd_omega3(k, m, n1, p, q, r, search)
    b_r0 = nd_omega3(k, m, n2, p, q, s, search)
    Bm = Bx(m, n1, n2, r, s)
    Bk = Bx(k, n1, n2, r, s)
    b_q0 = max(q, Bm) if Bm < float('inf') else float('inf')
    b_p0 = max(p, Bk) if Bk < float('inf') else float('inf')
    return min(b_s0, b_r0, b_q0, b_p0)

def np0_min_113(m, n1, n2, n3, q, r, s, t, search=14):
    """N_{p=0}: phi_p=0. min max(q|phi_q|,...) s.t. m*phi_q=n1*phi_r+n2*phi_s+n3*phi_t."""
    best = float('inf')
    for phi_r in range(-search, search + 1):
        for phi_s in range(-search, search + 1):
            for phi_t in range(-search, search + 1):
                rhs = n1 * phi_r + n2 * phi_s + n3 * phi_t
                if rhs % m != 0: continue
                phi_q = rhs // m
                if phi_q == 0: continue
                norm = max(q * abs(phi_q), r * abs(phi_r), s * abs(phi_s), t * abs(phi_t))
                if norm > 0 and norm < best: best = norm
    return best

def nq0_min_113(k, n1, n2, n3, p, r, s, t, search=14):
    """N_{q=0}: phi_q=0. min max(p|phi_p|,...) s.t. k*phi_p=n1*phi_r+n2*phi_s+n3*phi_t."""
    best = float('inf')
    for phi_r in range(-search, search + 1):
        for phi_s in range(-search, search + 1):
            for phi_t in range(-search, search + 1):
                rhs = n1 * phi_r + n2 * phi_s + n3 * phi_t
                if rhs % k != 0: continue
                phi_p = rhs // k
                if phi_p == 0: continue
                norm = max(p * abs(phi_p), r * abs(phi_r), s * abs(phi_s), t * abs(phi_t))
                if norm > 0 and norm < best: best = norm
    return best

def nd_formula_113(p, q, r, s, t, k, m, n1, n2, n3):
    """5-branch recursive formula for type (1,1,3)."""
    return min(
        nd_omega4_two_c(k, m, n2, n3, p, q, s, t),   # phi_r=0
        nd_omega4_two_c(k, m, n1, n3, p, q, r, t),   # phi_s=0
        nd_omega4_two_c(k, m, n1, n2, p, q, r, s),   # phi_t=0
        np0_min_113(m, n1, n2, n3, q, r, s, t),      # phi_p=0
        nq0_min_113(k, n1, n2, n3, p, r, s, t),      # phi_q=0
    )

def nd_smart_verify_113(p, q, r, s, t, k, m, n1, n2, n3, formula_val):
    """
    Verify formula_val is exact by searching for any lattice vector with norm < formula_val.
    Returns (True, 0) if formula is tight; (False, found_norm) if a smaller norm exists.

    Iterate (phi_q, phi_r, phi_s, phi_t) up to M//prime bounds.
    Solve phi_p = (n1*phi_r + n2*phi_s + n3*phi_t - m*phi_q) / k.
    Wronskian: phi_q - phi_p != 0.
    """
    M = formula_val - 1
    if M <= 0:
        return True, 0
    bq = M // q
    br = M // r
    bs = M // s
    bt = M // t

    for phi_q in range(-bq, bq + 1):
        for phi_r in range(-br, br + 1):
            for phi_s in range(-bs, bs + 1):
                for phi_t in range(-bt, bt + 1):
                    rhs = n1 * phi_r + n2 * phi_s + n3 * phi_t - m * phi_q
                    if rhs % k != 0: continue
                    phi_p = rhs // k
                    if p * abs(phi_p) > M: continue
                    if phi_p == 0 and phi_q == 0 and phi_r == 0 and phi_s == 0 and phi_t == 0:
                        continue
                    norm = max(p*abs(phi_p), q*abs(phi_q), r*abs(phi_r),
                               s*abs(phi_s), t*abs(phi_t))
                    if norm > M: continue
                    if phi_q != phi_p:  # Wronskian != 0
                        return False, norm
    return True, formula_val

# ---- Build type (1,1,3) triples ----
prime_powers = {}; three_prime_c = {}
for nn in range(2, LIMIT + 1):
    f = factorize(nn)
    if len(f) == 1:
        p2 = list(f.keys())[0]; prime_powers[nn] = (p2, f[p2])
    elif len(f) == 3:
        ps = sorted(f.keys())
        three_prime_c[nn] = (ps[0], ps[1], ps[2], f[ps[0]], f[ps[1]], f[ps[2]])

print(f"T79b: type (1,1,3) exact nd verification — smart bounded verifier (LIMIT={LIMIT})")
print("=" * 70)

triples = []; seen = set()
for a, (p, k) in prime_powers.items():
    for b, (q, m) in prime_powers.items():
        if p == q: continue
        if math.gcd(a, b) != 1: continue
        c = a + b
        if c not in three_prime_c: continue
        r, s, t, n1, n2, n3 = three_prime_c[c]
        if p in (r, s, t) or q in (r, s, t): continue
        key = (min(a,b), max(a,b))
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, t, k, m, n1, n2, n3))

print(f"Type (1,1,3) triples found: {len(triples)}")
print()

ok = 0; fail = 0; branch_wins = defaultdict(int)
branch_names = ['sub_st(r=0)', 'sub_rt(s=0)', 'sub_rs(t=0)', 'N_p0', 'N_q0']

for (a, b, p, q, r, s, t, k, m, n1, n2, n3) in triples:
    fval = nd_formula_113(p, q, r, s, t, k, m, n1, n2, n3)
    tight, found = nd_smart_verify_113(p, q, r, s, t, k, m, n1, n2, n3, fval)

    if tight:
        ok += 1
        bvals = [
            nd_omega4_two_c(k, m, n2, n3, p, q, s, t),
            nd_omega4_two_c(k, m, n1, n3, p, q, r, t),
            nd_omega4_two_c(k, m, n1, n2, p, q, r, s),
            np0_min_113(m, n1, n2, n3, q, r, s, t),
            nq0_min_113(k, n1, n2, n3, p, r, s, t),
        ]
        for i, v in enumerate(bvals):
            if v == fval: branch_wins[branch_names[i]] += 1
    else:
        fail += 1
        print(f"FAIL: ({a},{b}) p={p}^{k} q={q}^{m} c={r}^{n1}*{s}^{n2}*{t}^{n3}: "
              f"formula={fval} but found norm={found}")

print(f"Results: {ok} OK, {fail} FAIL")
print()
print("Branch win counts (ties counted in both):")
for nm in branch_names:
    print(f"  {nm:20s}: {branch_wins[nm]:4d}")
print()
if fail == 0:
    print("CANDIDATE FORMULA PASSES: 5-branch formula is exact on all tested triples.")
else:
    print("FORMULA FAILS: needs correction or additional branches.")
