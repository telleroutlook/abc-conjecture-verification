"""
T72 — Bezout characterization of pairwise-regime nd = p_L.

For one-prime-per-group (k,m,n) with p_L = max(pa,pb,pc) in the pairwise regime
(N_{pL=0} > p_L), we ask: when is nd(a,b) = p_L?

Claim: nd = p_L iff there exists a witness with |phi_pL| = gcd_min and
  max(p_other * |phi_other_i|) <= p_L.
where gcd_min is the smallest positive s with gcd(s, lcm(m,n)) | k (for pL=pa).

Key sub-case: k=1, pL=pa, gcd(m,n)=1.
  Constraint: phi_a + m*phi_b = n*phi_c.
  phi_a=+/-1: m*phi_b - n*phi_c = -/+1. Bezout: gcd(m,n)=1 guarantees solutions.
  Minimal Bezout pair (u0,v0) for m*u0 - n*v0 = 1: |u0| <= (n-1)/2+1, |v0| <= (m-1)/2+1.
  nd = pa iff min over Bezout family of max(pb*|phi_b|, pc*|phi_c|) <= pa.

This script:
1. For all pairwise-regime cases from T71, checks if nd = p_L
2. Computes the minimal Bezout norm and checks if <= p_L
3. Identifies the precise boundary condition
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


def nd_brute(a, b, bound=35):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2 or n > 4:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float("inf")
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
    return best if best < float("inf") else None


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def bezout_min_norm(m, n, k, pb, pc):
    """
    Find min over (phi_b, phi_c) of max(pb*|phi_b|, pc*|phi_c|)
    subject to m*phi_b - n*phi_c = -k (i.e., phi_a=+1 case: 1+m*phi_b=n*phi_c).
    Also tries phi_a=-1: m*phi_b - n*phi_c = k.
    Returns (min_norm, best_phi_b, best_phi_c, which_case)
    """
    best = float("inf")
    best_v = None
    for sign in [+1, -1]:
        rhs = sign * k
        g, u0, v0 = extended_gcd(m, n)
        if rhs % g != 0:
            continue
        # Particular solution to m*u - n*v = rhs
        u_part = u0 * (rhs // g)
        v_part = v0 * (rhs // g)
        # General solution: u = u_part + (n/g)*t, v = v_part + (m/g)*t
        step_u = n // g
        step_v = m // g
        # Find t minimizing max(pb*|u_part+step_u*t|, pc*|v_part+step_v*t|)
        # Optimal t: pb*(u_part+step_u*t) = pc*(v_part+step_v*t) (balancing)
        # t = (pc*v_part - pb*u_part) / (pb*step_u - pc*step_v)
        # Search around optimal t
        denom = pb * step_u - pc * step_v
        if denom != 0:
            t_opt = (pc * v_part - pb * u_part) / denom
        else:
            t_opt = 0.0
        for t in range(int(t_opt) - 5, int(t_opt) + 6):
            phi_b = u_part + step_u * t
            phi_c = v_part + step_v * t
            norm = max(pb * abs(phi_b), pc * abs(phi_c))
            if norm < best:
                best = norm
                best_v = (phi_b, phi_c, sign)
    return best, best_v


# Collect all one-prime-per-group triples with n>=1 in range
triples = []
seen = set()
for a in range(2, 600):
    fa = factorize(a)
    if len(fa) != 1:
        continue
    pa = list(fa.keys())[0]
    kval = fa[pa]
    for b in range(1, 600):
        fb = factorize(b)
        if len(fb) != 1:
            continue
        pb = list(fb.keys())[0]
        mval = fb[pb]
        if pb == pa:
            continue
        c = a + b
        fc = factorize(c)
        if len(fc) != 1:
            continue
        pc = list(fc.keys())[0]
        nval = fc[pc]
        if pc == pa or pc == pb:
            continue
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        triples.append((a, b, pa, pb, pc, kval, mval, nval))


def is_pairwise(pa, pb, pc, k, m, n):
    """Check if none of the three pure branches is in valuation regime."""
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)
    N1 = max(pb * n // g_mn, pc * m // g_mn)
    N2 = max(pa * n // g_kn, pc * k // g_kn)
    # valuation regime: N0<=pc or N1<=pa or N2<=pb
    if N0 <= pc:
        return False, N0, N1, N2
    if N1 <= pa:
        return False, N0, N1, N2
    if N2 <= pb:
        return False, N0, N1, N2
    return True, N0, N1, N2


print("T72: Bezout characterization of nd = p_L in pairwise regime")
print("=" * 75)

pairwise_cases = []
for a, b, pa, pb, pc, k, m, n in triples:
    is_pw, N0, N1, N2 = is_pairwise(pa, pb, pc, k, m, n)
    if not is_pw:
        continue
    pairwise_cases.append((a, b, pa, pb, pc, k, m, n, N0, N1, N2))

print(f"Total pairwise-regime cases in [1,600): {len(pairwise_cases)}")
print()

# For each, check nd vs p_L
pl_ok = 0
pl_fail = 0
pure_ok = 0
mixed_other = 0
bezout_condition_verified = 0
bezout_condition_failed = 0

print(
    f"{'Triple':15s} {'p_L':4s} {'nd':4s} {'nd=pL':6s} {'Bez_norm':8s} {'Bez<=pL':7s} {'Regime':15s}"
)
print("-" * 75)

for a, b, pa, pb, pc, k, m, n, N0, N1, N2 in pairwise_cases:
    nd_b = nd_brute(a, b, bound=35)
    if nd_b is None:
        continue

    pL = max(pa, pb, pc)
    pure_min = min(N0, N1, N2)

    nd_equals_pL = nd_b == pL

    # Compute Bezout min norm for the pL-prime = pa case (most common)
    if pL == pa:
        bez_norm, bez_v = bezout_min_norm(m, n, k, pb, pc)
        bez_fits = bez_norm <= pL
        regime = "pL=pa"
    elif pL == pb:
        # phi_b=+/-1: k*phi_a + m = n*phi_c (phi_b=1)
        # Rearrange: k*phi_a - n*phi_c = -m, or k*phi_a - n*phi_c = m (phi_b=-1)
        bez_norm, bez_v = bezout_min_norm(k, n, m, pa, pc)
        bez_fits = bez_norm <= pL
        regime = "pL=pb"
    else:  # pL == pc
        # phi_c=+/-1: k*phi_a + m*phi_b = n (phi_c=1)
        # This is the phi_c-nonzero case
        bez_norm, bez_v = bezout_min_norm(k, m, n, pa, pb)
        # Actually for phi_c=1: k*phi_a + m*phi_b = n
        # This is different from Bezout(k,m)...
        # The norm here: max(pa*|phi_a|, pb*|phi_b|, pc) with constraint k*phi_a+m*phi_b=n
        # Min over (phi_a,phi_b): this is the 2D problem
        bez_best = float("inf")
        for phi_a in range(-20, 21):
            rhs = n - k * phi_a
            if rhs % m != 0:
                continue
            phi_b = rhs // m
            W = phi_b - phi_a
            if W == 0:
                continue
            norm = max(pa * abs(phi_a), pb * abs(phi_b), pc)
            if norm < bez_best:
                bez_best = norm
        bez_norm = bez_best
        bez_fits = bez_norm <= pL
        regime = "pL=pc"

    # Check if Bezout correctly predicts nd=pL
    if bez_fits and nd_equals_pL:
        bezout_condition_verified += 1
    elif not bez_fits and not nd_equals_pL:
        bezout_condition_verified += 1  # consistent: Bez fails → nd>pL
    elif bez_fits and not nd_equals_pL:
        bezout_condition_failed += 1
        print(f"  BEZ_PRED_FAIL: ({a},{b}) pL={pL} nd={nd_b} bez_norm={bez_norm}")
    elif not bez_fits and nd_equals_pL:
        bezout_condition_failed += 1
        print(
            f"  BEZ_PRED_FAIL: ({a},{b}) pL={pL} nd={nd_b} bez_norm={bez_norm} (bez>pL but nd=pL!)"
        )

    if nd_equals_pL:
        pl_ok += 1
    else:
        pl_fail += 1

    # Print concise summary
    tag = "=pL" if nd_equals_pL else f">{pL}"
    print(
        f"  ({a:3d},{b:3d}):  pL={pL:3d}  nd={nd_b:3d}  {tag:5s}  bez={bez_norm:5.0f}  {'fits' if bez_fits else 'NO':4s}  {regime}"
    )

print()
print("=" * 75)
print(f"Cases nd = p_L: {pl_ok}")
print(f"Cases nd > p_L: {pl_fail}")
print(f"Bezout condition consistent: {bezout_condition_verified}")
print(f"Bezout condition FAILED: {bezout_condition_failed}")

if bezout_condition_failed == 0:
    print()
    print("THEOREM CONFIRMED: nd = p_L iff Bezout minimum norm <= p_L")
    print("  (in pairwise regime, for all tested one-prime-per-group triples)")
