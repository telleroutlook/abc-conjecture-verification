"""
T74 — nd exact formula for omega*=4 with two primes in Pc.

Setup: a = p^k, b = q^m, c = r^j * s^n with distinct primes p,q,r,s.
  Groups: Pa={p}, Pb={q}, Pc={r,s}.
  Constraint: k*phi_p + m*phi_q = j*phi_r + n*phi_s
  Wronskian:  W = phi_q - phi_p != 0

The four "pure-one-zero" branches (zero exactly one prime coordinate):

  Branch phi_p=0: m*phi_q = j*phi_r + n*phi_s, W=phi_q!=0.
    Minimum norm: min over phi_q=+/-1 of min_{j*phi_r+n*phi_s=m*phi_q} max(q|phi_q|,r|phi_r|,s|phi_s|)
    = max(q, BEZ2D(j,n,m,r,s))   where BEZ2D is 2D Bezout min.

  Branch phi_q=0: k*phi_p = j*phi_r + n*phi_s, W=-phi_p!=0.
    = max(p, BEZ2D(j,n,k,r,s))

  Branch phi_r=0: k*phi_p + m*phi_q = n*phi_s, W=phi_q-phi_p!=0.
    This is EXACTLY the omega*=3 problem for (p^k, q^m, s^n).
    nd_phir0 = nd_omega3(k, m, n, p, q, s)

  Branch phi_s=0: k*phi_p + m*phi_q = j*phi_r, W=phi_q-phi_p!=0.
    This is EXACTLY the omega*=3 problem for (p^k, q^m, r^j).
    nd_phis0 = nd_omega3(k, m, j, p, q, r)

Conjecture: nd(a,b) = min(max(q,BEZ2D(j,n,m,r,s)), max(p,BEZ2D(j,n,k,r,s)),
                          nd_omega3(k,m,n,p,q,s), nd_omega3(k,m,j,p,q,r))

Key observation: if p<q, then nd_omega3 <= q (E_n theorem), so branch phi_r=0 or phi_s=0
achieves norm <= q. Branch phi_p=0 achieves norm >= q. So the phi_p=0 branch can never
improve over phi_r=0 or phi_s=0. Similarly for phi_q=0 vs phi_r=0/phi_s=0 if p<=q.

Stronger conjecture: nd = min(nd_omega3(k,m,j,p,q,r), nd_omega3(k,m,n,p,q,s))
  i.e., the two "phi_c-prime=0" branches always dominate.

This script verifies both conjectures.
"""

import math
from itertools import product as iproduct

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

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for d in range(3, int(n**0.5)+1, 2):
        if n % d == 0: return False
    return True

def nd_brute(a, b, bound=25):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2 or n > 5:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=n):
        if all(c == 0 for c in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0:
            continue
        W = sum(ws[i] * coords[i] for i in range(n))
        if W == 0:
            continue
        norm = max(primes[i] * abs(coords[i]) for i in range(n))
        if norm > 0:
            best = min(best, norm)
    return best if best < float('inf') else None

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def bezout_min_norm_1d(m, n, k, pb, pc):
    """
    Min over (phi_b, phi_c) of max(pb|phi_b|, pc|phi_c|)
    subject to m*phi_b - n*phi_c = k (and m*phi_b - n*phi_c = -k).
    Returns minimum norm (inf if no solution).
    """
    best = float('inf')
    for sign in [+1, -1]:
        rhs = sign * k
        g, u0, v0 = extended_gcd(m, n)
        if rhs % g != 0:
            continue
        u_part = u0 * (rhs // g)
        v_part = v0 * (rhs // g)
        step_u = n // g
        step_v = m // g
        denom = pb * step_u - pc * step_v
        if denom != 0:
            t_opt = (pc * v_part - pb * u_part) / denom
        else:
            t_opt = 0.0
        for t in range(int(t_opt) - 6, int(t_opt) + 7):
            phi_b = u_part + step_u * t
            phi_c = v_part + step_v * t
            norm = max(pb * abs(phi_b), pc * abs(phi_c))
            best = min(best, norm)
    return best

def bezout_min_2d(j, n, m_rhs, pr, ps):
    """
    Min over (phi_r, phi_s) of max(pr|phi_r|, ps|phi_s|)
    subject to j*phi_r + n*phi_s = m_rhs.
    Tries both m_rhs and -m_rhs (for phi_p=+1 and phi_p=-1 sub-cases).
    """
    best = float('inf')
    for rhs in [m_rhs, -m_rhs]:
        g, u0, v0 = extended_gcd(j, n)
        if rhs % g != 0:
            continue
        # Particular solution: j*u0 + n*v0 = g, scaled
        r_part = u0 * (rhs // g)    # phi_r particular
        s_part = v0 * (rhs // g)    # phi_s particular
        # General solution: phi_r = r_part + (n/g)*t, phi_s = s_part - (j/g)*t
        step_r = n // g
        step_s = j // g   # phi_s decreases as t increases
        # Balance: pr*(r_part+step_r*t) = ps*(s_part-step_s*t)
        # t*(pr*step_r + ps*step_s) = ps*s_part - pr*r_part
        denom = pr * step_r + ps * step_s
        if denom != 0:
            t_opt = (ps * s_part - pr * r_part) / denom
        else:
            t_opt = 0.0
        for t in range(int(t_opt) - 6, int(t_opt) + 7):
            phi_r = r_part + step_r * t
            phi_s = s_part - step_s * t
            norm = max(pr * abs(phi_r), ps * abs(phi_s))
            best = min(best, norm)
    return best

def nd_omega3_exact(k, m, n, p, q, r):
    """
    Exact nd for one-prime-per-group triple a=p^k, b=q^m, c=r^n
    with p,q,r distinct (not necessarily p<q<r).
    Uses thm:nd_pairwise_bezout.
    """
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(p * m // g_km, q * k // g_km)  # phi_r=0 branch
    N1 = max(q * n // g_mn, r * m // g_mn)  # phi_p=0 branch
    N2 = max(p * n // g_kn, r * k // g_kn)  # phi_q=0 branch
    pL = max(p, q, r)
    # Check valuation regime first
    if N0 <= r:  # phi_r=0 wins, N0 is nd
        return N0
    if N1 <= p:
        return N1
    if N2 <= q:
        return N2
    # Pairwise regime: nd >= pL, find Bezout
    # Determine which prime is pL and compute Bezout
    if pL == r:
        # phi_r contribution: use Bezout for phi_r=+/-1
        # Constraint: k*phi_p + m*phi_q = n*phi_r
        # phi_r=+/-1 => k*phi_p + m*phi_q = +/-n
        # Bezout: min over k*phi_p + m*phi_q = n of max(p|phi_p|, q|phi_q|)
        B = bezout_min_norm_1d(k, m, n, p, q)
        N = min(N0, N1, N2)  # best pure branch
        return min(N, max(pL, B))
    elif pL == p:
        # phi_p=+/-1 => m*phi_q - n*phi_r = +/-k
        B = bezout_min_norm_1d(m, n, k, q, r)
        N = min(N0, N1, N2)
        return min(N, max(pL, B))
    else:  # pL == q
        # phi_q=+/-1 => k*phi_p - n*phi_r = +/-m
        # Actually: k*phi_p + m*phi_q = n*phi_r, phi_q=+/-1 => k*phi_p - n*phi_r = -/+m
        # = k*phi_p - n*phi_r = -m (phi_q=1) or k*phi_p - n*phi_r = +m (phi_q=-1)
        B = bezout_min_norm_1d(k, n, m, p, r)
        N = min(N0, N1, N2)
        return min(N, max(pL, B))

# -----------------------------------------------------------------------
# Collect omega*=4 triples with Pa={1 prime}, Pb={1 prime}, Pc={2 primes}
# -----------------------------------------------------------------------
print("T74: nd exact formula for omega*=4 with Pc = {r^j, s^n}")
print("=" * 75)

triples4 = []
seen = set()
RANGE = 120

for a in range(2, RANGE):
    fa = factorize(a)
    if len(fa) != 1: continue
    p = list(fa.keys())[0]; k = fa[p]
    for b in range(1, RANGE):
        fb = factorize(b)
        if len(fb) != 1: continue
        q = list(fb.keys())[0]; m = fb[q]
        if q == p: continue
        c = a + b
        fc = factorize(c)
        if len(fc) != 2: continue  # EXACTLY 2 distinct primes in c
        r_list = sorted(fc.keys())
        r, s = r_list[0], r_list[1]
        j, nv = fc[r], fc[s]
        if r == p or r == q or s == p or s == q: continue
        key = (min(a,b), max(a,b))
        if key in seen: continue
        seen.add(key)
        triples4.append((a, b, p, q, r, s, k, m, j, nv))

print(f"Found {len(triples4)} omega*=4 one-primes-per-Pa-Pb, two-primes-in-Pc triples in [1,{RANGE})")
print()

# -----------------------------------------------------------------------
# Test formula for each triple
# -----------------------------------------------------------------------
formula_ok = 0; formula_fail = 0
strong_formula_ok = 0; strong_formula_fail = 0
branch_wins = {'phi_r0': 0, 'phi_s0': 0, 'phi_p0': 0, 'phi_q0': 0, 'tie': 0}

print(f"{'Triple':18s} {'p,q,r,s':16s} {'nd':4s} {'form':4s} {'phi_r0':6s} {'phi_s0':6s} {'phi_p0':6s} {'phi_q0':6s} {'OK':3s}")
print("-" * 75)

for (a, b, p, q, r, s, k, m, j, nv) in triples4:
    nd_b = nd_brute(a, b, bound=12)
    if nd_b is None: continue

    # Branch phi_r=0: nd_omega3 for (p^k, q^m, s^nv)
    nd_phi_r0 = nd_omega3_exact(k, m, nv, p, q, s)
    # Branch phi_s=0: nd_omega3 for (p^k, q^m, r^j)
    nd_phi_s0 = nd_omega3_exact(k, m, j, p, q, r)
    # Branch phi_p=0: max(q, BEZ2D(j,nv,m,r,s))
    bez_phi_p0 = bezout_min_2d(j, nv, m, r, s)
    nd_phi_p0 = max(q, bez_phi_p0) if bez_phi_p0 < float('inf') else float('inf')
    # Branch phi_q=0: max(p, BEZ2D(j,nv,k,r,s))
    bez_phi_q0 = bezout_min_2d(j, nv, k, r, s)
    nd_phi_q0 = max(p, bez_phi_q0) if bez_phi_q0 < float('inf') else float('inf')

    formula = min(nd_phi_r0, nd_phi_s0, nd_phi_p0, nd_phi_q0)
    formula_match = (formula == nd_b)

    # Strong formula: just min(phi_r0, phi_s0)
    strong_formula = min(nd_phi_r0, nd_phi_s0)
    strong_match = (strong_formula == nd_b)

    ok_str = "OK" if formula_match else "FAIL"
    if formula_match:
        formula_ok += 1
    else:
        formula_fail += 1

    if strong_match:
        strong_formula_ok += 1
    else:
        strong_formula_fail += 1
        # This is a case where phi_p0 or phi_q0 branch beats phi_r0 and phi_s0

    # Track which branch wins
    if formula_match:
        winning = min(nd_phi_r0, nd_phi_s0, nd_phi_p0, nd_phi_q0)
        branches_at_min = []
        if nd_phi_r0 == winning: branches_at_min.append('phi_r0')
        if nd_phi_s0 == winning: branches_at_min.append('phi_s0')
        if nd_phi_p0 == winning: branches_at_min.append('phi_p0')
        if nd_phi_q0 == winning: branches_at_min.append('phi_q0')
        if len(branches_at_min) > 1:
            branch_wins['tie'] += 1
        else:
            branch_wins[branches_at_min[0]] += 1

    pqs_str = f"{p},{q},{r},{s}"
    nd_phi_p0_disp = nd_phi_p0 if nd_phi_p0 < 999 else 999
    nd_phi_q0_disp = nd_phi_q0 if nd_phi_q0 < 999 else 999
    print(f"  ({a:3d},{b:3d}):  {pqs_str:16s} nd={nd_b:3d} f={formula:3d}  "
          f"r0={nd_phi_r0:4d}  s0={nd_phi_s0:4d}  p0={nd_phi_p0_disp:4d}  q0={nd_phi_q0_disp:4d}  {ok_str}")

print()
print("=" * 75)
print(f"Full formula (min of 4 branches): {formula_ok} OK, {formula_fail} FAIL")
print(f"Strong formula (min of phi_r0, phi_s0 only): {strong_formula_ok} OK, {strong_formula_fail} FAIL")
print()
print("Branch that achieves minimum (among formula-OK cases):")
for bname, cnt in branch_wins.items():
    print(f"  {bname}: {cnt}")
print()
if formula_fail == 0:
    print("THEOREM CONFIRMED: nd = min(nd_omega3(k,m,j,p,q,r), nd_omega3(k,m,nv,p,q,s),")
    print("                           max(q,BEZ2D(j,nv,m)), max(p,BEZ2D(j,nv,k)))")
    print("for all omega*=4 one-prime-per-Pa/Pb, two-primes-in-Pc triples tested.")
if strong_formula_fail == 0:
    print()
    print("STRONG THEOREM CONFIRMED: nd = min(nd_omega3_phis0, nd_omega3_phir0)")
    print("  i.e., the two phi_c-branch formulas suffice; phi_p0 and phi_q0 never improve.")
elif strong_formula_fail > 0:
    print(f"STRONG THEOREM FAILS for {strong_formula_fail} cases:")
    # re-scan to print failures
    for (a, b, p, q, r, s, k, m, j, nv) in triples4:
        nd_b = nd_brute(a, b, bound=12)
        if nd_b is None: continue
        nd_phi_r0 = nd_omega3_exact(k, m, nv, p, q, s)
        nd_phi_s0 = nd_omega3_exact(k, m, j, p, q, r)
        strong_formula = min(nd_phi_r0, nd_phi_s0)
        if strong_formula != nd_b:
            bez_phi_p0 = bezout_min_2d(j, nv, m, r, s)
            nd_phi_p0 = max(q, bez_phi_p0) if bez_phi_p0 < float('inf') else float('inf')
            bez_phi_q0 = bezout_min_2d(j, nv, k, r, s)
            nd_phi_q0 = max(p, bez_phi_q0) if bez_phi_q0 < float('inf') else float('inf')
            print(f"  ({a},{b}) p={p}^{k} q={q}^{m} r={r}^{j} s={s}^{nv}: "
                  f"nd={nd_b} strong={strong_formula} "
                  f"phi_r0={nd_phi_r0} phi_s0={nd_phi_s0} phi_p0={nd_phi_p0} phi_q0={nd_phi_q0}")
