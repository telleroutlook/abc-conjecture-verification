"""
T66 — Lower bound analysis for nd(a,b) in non-squarefree triples.

Key question: what is the best LOWER BOUND on nd(a,b) for non-squarefree triples?

For squarefree triples: E_n theorem gives nd = median(m_a, m_b, m_c) (exact, both sides tight).
For non-squarefree: OB-13B gives nd <= v_max * median(m_a, m_b, m_c) (upper bound).
  But: does nd >= median(m_a, m_b, m_c)?  T65 data suggests NO for multi-prime groups.

EXAMPLE: (1,288,289):
  Pa={}, Pb={2,3} (m_b=2), Pc={17} (m_c=17).
  median(inf, 2, 17) = 17. But nd = 15 < 17!
  Reason: multi-prime Pb allows nd below m_c.

PROGRAM:
  1. For each non-squarefree triple, compute:
     - nd_brute (exact, via T64 algorithm)
     - median(m_a, m_b, m_c) (squarefree formula)
     - second_smallest_prime = min of the (omega-1) smallest primes in P overall
     - GCD-pair lower: min_{cross-pair} max(p,q) (the "F10 formula" for squarefree)
  2. Find: is nd >= second_smallest_prime in P? (global lower bound by smallest primes)
  3. Find: is nd >= min_{g} m_g over non-empty groups? (group-minimum lower bound)
  4. Identify the tightest lower bound from the data.
"""

import math
from itertools import product as iproduct, combinations

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

def rad(n):
    return math.prod(factorize(n).keys()) if n > 1 else 1

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def lattice_basis_from_constraint(alpha):
    n = len(alpha)
    U = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    a_work = list(alpha)
    for col in range(1, n):
        if a_work[col] == 0:
            continue
        g, x, y = extended_gcd(a_work[0], a_work[col])
        p_c = a_work[col] // g
        q_c = a_work[0] // g
        new0 = [x * U[r][0] + y * U[r][col] for r in range(n)]
        newc = [-p_c * U[r][0] + q_c * U[r][col] for r in range(n)]
        for r in range(n):
            U[r][0] = new0[r]
            U[r][col] = newc[r]
        a_work[0] = g
        a_work[col] = 0
    return [[U[r][c] for r in range(n)] for c in range(1, n)]

def lll_reduce(basis, primes, delta=0.75):
    n_v = len(basis)
    n_d = len(basis[0])
    B = [list(v) for v in basis]

    def dot(u, v):
        return sum(primes[i]**2 * u[i] * v[i] for i in range(n_d))

    def gs_full(vecs):
        gs = []
        mu = [[0.0]*len(vecs) for _ in range(len(vecs))]
        for i, v in enumerate(vecs):
            u = list(v)
            for j in range(i):
                d = dot(gs[j], gs[j])
                mu[i][j] = dot(v, gs[j]) / d if d > 1e-12 else 0
                u = [u[k] - mu[i][j]*gs[j][k] for k in range(n_d)]
            gs.append(u)
        return gs, mu

    k = 1
    for _ in range(300):
        if k >= n_v:
            break
        gs, mu = gs_full(B)
        for j in range(k-1, -1, -1):
            if abs(mu[k][j]) > 0.5:
                m = round(mu[k][j])
                B[k] = [B[k][i] - m*B[j][i] for i in range(n_d)]
                gs, mu = gs_full(B)
        gs, mu = gs_full(B)
        lhs = dot(gs[k], gs[k])
        rhs = (delta - mu[k][k-1]**2) * dot(gs[k-1], gs[k-1])
        if lhs >= rhs:
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            k = max(k-1, 1)
    return B

def nd_svp(a, b, R=20):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2 or n > 7:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    basis = lattice_basis_from_constraint(alpha)
    basis_red = lll_reduce(basis, primes)
    rank = len(basis_red)
    best = float('inf')
    for coords in iproduct(range(-R, R+1), repeat=rank):
        if all(c==0 for c in coords):
            continue
        phi = [sum(coords[k]*basis_red[k][i] for k in range(rank)) for i in range(n)]
        if sum(alpha[i]*phi[i] for i in range(n)) != 0:
            continue
        W = sum(ws[i]*phi[i] for i in range(n))
        if W == 0:
            continue
        norm = max(primes[i]*abs(phi[i]) for i in range(n))
        if norm > 0:
            best = min(best, norm)
    return best if best < float('inf') else None

# ── Lower bound candidates ────────────────────────────────────────────────────
def lower_bounds(a, b):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    if not primes:
        return {}
    v_max = max([max(fa.values()) if fa else 0,
                 max(fb.values()) if fb else 0,
                 max(fc.values()) if fc else 0])
    R = rad(a*b*c)
    omega = len(primes)
    # Group minima
    ma = min(fa.keys()) if fa else float('inf')
    mb = min(fb.keys()) if fb else float('inf')
    mc = min(fc.keys()) if fc else float('inf')
    sorted_gm = sorted([x for x in [ma,mb,mc] if x < float('inf')])
    median_gm = sorted_gm[1] if len(sorted_gm) >= 2 else (sorted_gm[0] if sorted_gm else 0)
    min_gm = min(sorted_gm) if sorted_gm else 0
    second_global = primes[1] if omega >= 2 else primes[0]  # 2nd smallest prime in P
    # squarefree E_n formula: second smallest group minimum
    en_sq = median_gm  # holds for squarefree; NOT a lower bound for non-sq
    return {
        'v_max': v_max,
        'R': R,
        'omega': omega,
        'min_gm': min_gm,
        'median_gm': median_gm,
        'second_global': second_global,
        'en_sq': en_sq,
    }

# ── Main analysis ─────────────────────────────────────────────────────────────
print("T66: Lower bound analysis for nd(a,b) in non-squarefree triples")
print("=" * 120)
print(f"{'(a,b,c)':<18} {'omega':>5} {'nd':>5} {'min_gm':>7} {'med_gm':>7} "
      f"{'2nd_glb':>8} {'nd>=mgm':>8} {'nd>=2ng':>8} {'nd/min_gm':>10}")
print("-" * 120)

violations_median = []
violations_2nd_global = []
violations_min_gm = []

C_MAX = 3000
for c in range(3, C_MAX + 1):
    fc = factorize(c)
    sq_c = all(v == 1 for v in fc.values())
    for a in range(1, c // 2 + 1):
        b = c - a
        if b <= 0 or math.gcd(a, b) != 1:
            continue
        fa = factorize(a)
        fb = factorize(b)
        sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())
        if sq:
            continue  # only non-squarefree
        primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
        omega = len(primes)
        if omega < 2 or omega > 5:
            continue
        lb = lower_bounds(a, b)
        nd = nd_svp(a, b, R=15)
        if nd is None:
            continue
        min_gm = lb['min_gm']
        median_gm = lb['median_gm']
        second_global = lb['second_global']
        ok_median = nd >= median_gm
        ok_2nd = nd >= second_global
        ok_min = nd >= min_gm
        if not ok_median:
            violations_median.append((a, b, c, nd, min_gm, median_gm, second_global))
        if not ok_2nd:
            violations_2nd_global.append((a, b, c, nd, min_gm, median_gm, second_global))
        if not ok_min:
            violations_min_gm.append((a, b, c, nd, min_gm, median_gm, second_global))

print(f"\nTotal non-squarefree triples scanned: c <= {C_MAX}, omega in [2,5]")
print()
print(f"nd >= median(m_a, m_b, m_c)  violations: {len(violations_median)}")
if violations_median[:5]:
    print("  (first 5):")
    for (a,b,c,nd,mgm,med,sg) in violations_median[:5]:
        print(f"    ({a},{b},{c}): nd={nd}, median={med}, min_gm={mgm}, 2nd_global={sg}")
print()
print(f"nd >= second_global_prime    violations: {len(violations_2nd_global)}")
if violations_2nd_global[:5]:
    for (a,b,c,nd,mgm,med,sg) in violations_2nd_global[:5]:
        print(f"    ({a},{b},{c}): nd={nd}, 2nd_global={sg}")
print()
print(f"nd >= min_gm                 violations: {len(violations_min_gm)}")
if violations_min_gm[:3]:
    for (a,b,c,nd,mgm,med,sg) in violations_min_gm[:3]:
        print(f"    ({a},{b},{c}): nd={nd}, min_gm={mgm}")
print()

# ── Check specific conjecture: nd >= second_global_prime ─────────────────────
print("CONJECTURE: nd(a,b) >= second-smallest prime in P (= min over cross-group pairs of max(p,q))")
print("  This is the F10 lower bound: nd >= min_{g1!=g2} max(min_g1, min_g2)")
print()

# Direct check of F10 lower bound (from the squarefree proof)
f10_violations = []
for c in range(3, 500 + 1):
    fc = factorize(c)
    for a in range(1, c // 2 + 1):
        b = c - a
        if b <= 0 or math.gcd(a, b) != 1:
            continue
        fa = factorize(a)
        fb = factorize(b)
        sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())
        if sq:
            continue
        primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
        omega = len(primes)
        if omega < 2 or omega > 5:
            continue
        # F10 value: second smallest of group minima
        ma = min(fa.keys()) if fa else float('inf')
        mb = min(fb.keys()) if fb else float('inf')
        mc = min(fc.keys()) if fc else float('inf')
        gm = sorted([x for x in [ma,mb,mc] if x < float('inf')])
        if len(gm) < 2:
            continue
        f10_val = gm[1]  # second smallest group minimum
        nd = nd_svp(a, b, R=12)
        if nd is None:
            continue
        if nd < f10_val:
            f10_violations.append((a,b,c,nd,f10_val,ma,mb,mc))

print(f"F10 lower bound (nd >= second_smallest_group_min) violations in c<=500: {len(f10_violations)}")
if f10_violations[:8]:
    print("  Violations:")
    for (a,b,c,nd,f10v,ma,mb,mc) in f10_violations[:8]:
        print(f"    ({a},{b},{c}): nd={nd} < f10={f10v} (group mins: {ma},{mb},{mc})")
else:
    print("  None found! F10 lower bound holds for all non-squarefree tested triples.")

print()
print("CONCLUSION:")
if not f10_violations:
    print("  CONJECTURE SUPPORTED: nd(a,b) >= second_smallest_group_minimum for all tested non-squarefree.")
    print("  If true, combined with OB-13B: second_smallest_gm <= nd <= v_max * second_smallest_gm.")
    print("  This would EXACTLY extend E_n to non-squarefree, with v_max as the error factor.")
else:
    print(f"  CONJECTURE FAILS: {len(f10_violations)} violations found.")
