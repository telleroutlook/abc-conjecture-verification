"""
T71 — General valuation-regime theorem for one-prime-per-group triples.

Key insight from T70 analysis:
  For triple a=p^k, b=q^m, c=r^n (one prime per group), the lattice constraint is:
    k*phi_p + m*phi_q = n*phi_r
  The Wronskian: W = phi_q - phi_p

Three "pure" branches (zeroing one prime coordinate):
  N0 = max(p*m/g_km, q*k/g_km)  [phi_r=0, g_km=gcd(k,m)]
  N1 = max(q*n/g_mn, r*m/g_mn)  [phi_p=0, g_mn=gcd(m,n)]
  N2 = max(p*n/g_kn, r*k/g_kn)  [phi_q=0, g_kn=gcd(k,n)]

Theorem (n-generalized valuation regime):
  If max(p*m/g_km, q*k/g_km) <= r (i.e., N0 <= r), then nd = N0.
  Proof: witness (-m/g_km, k/g_km, 0) satisfies constraint for ANY n. QED.

This extends thm:nd_km1 to general n (removing n=1 restriction).

Similarly by symmetry:
  If N1 <= p, then nd = N1  (phi_p=0 branch wins when p is largest)
  If N2 <= q, then nd = N2  (phi_q=0 branch wins when q is largest)

The unified valuation regime: nd = min(N0,N1,N2) whenever the smallest
  of N0,N1,N2 is <= the prime it "zeros out".

This script:
1. Verifies the n-generalized theorem on all found (k,m,n) triples with n>=2
2. Checks the mixed-witness cases (T70 failures) for a pattern
3. Explores the "mixed witness" formula for p_a largest
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


def nd_brute(a, b, bound=30):
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


def nd_three_pure(pa, pb, pc, k, m, n):
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)  # phi_c=0
    N1 = max(pb * n // g_mn, pc * m // g_mn)  # phi_a=0
    N2 = max(pa * n // g_kn, pc * k // g_kn)  # phi_b=0
    return min(N0, N1, N2), N0, N1, N2


def nd_valuation_regime_formula(pa, pb, pc, k, m, n):
    """
    Returns nd if the triple is in ANY pure valuation regime, else None.
    Valuation regime for phi_r=0 (N0<=pc): nd = N0
    Valuation regime for phi_p=0 (N1<=pa): nd = N1
    Valuation regime for phi_q=0 (N2<=pb): nd = N2
    """
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)
    N1 = max(pb * n // g_mn, pc * m // g_mn)
    N2 = max(pa * n // g_kn, pc * k // g_kn)
    if N0 <= pc:
        return N0, "N0_val(phi_c=0)", N0, N1, N2
    if N1 <= pa:
        return N1, "N1_val(phi_a=0)", N0, N1, N2
    if N2 <= pb:
        return N2, "N2_val(phi_b=0)", N0, N1, N2
    return None, "pairwise/mixed", N0, N1, N2


def nd_mixed_formula_k1(pa, pb, pc, m, n):
    """
    For k=1, tries to find nd via the mixed witness:
    phi_a + m*phi_b = n*phi_c
    W = phi_b - phi_a != 0
    Minimize max(pa*|phi_a|, pb*|phi_b|, pc*|phi_c|)

    Try phi_c in {1,...,10}, phi_b in {-20,...,20}
    """
    best = float("inf")
    best_coords = None
    for phi_c in range(1, 15):
        for phi_b in range(-20, 21):
            # phi_a = n*phi_c - m*phi_b
            num = n * phi_c - m * phi_b
            phi_a = num  # k=1
            W = phi_b - phi_a
            if W == 0:
                continue
            norm = max(pa * abs(phi_a), pb * abs(phi_b), pc * abs(phi_c))
            if norm > 0 and norm < best:
                best = norm
                best_coords = (phi_a, phi_b, phi_c)
    # Also try phi_c negative
    for phi_c in range(-14, 0):
        for phi_b in range(-20, 21):
            num = n * phi_c - m * phi_b
            phi_a = num
            W = phi_b - phi_a
            if W == 0:
                continue
            norm = max(pa * abs(phi_a), pb * abs(phi_b), pc * abs(phi_c))
            if norm > 0 and norm < best:
                best = norm
                best_coords = (phi_a, phi_b, phi_c)
    return best, best_coords


# -------------------------------------------------------------------
# Part 1: Verify n-generalized valuation regime on all (k,m,n) triples with n>=2
# -------------------------------------------------------------------
print("=" * 75)
print("Part 1: n-generalized valuation regime (thm:nd_kmn_val)")
print("  If N0 = max(pa*m/gcd(k,m), pb*k/gcd(k,m)) <= pc, then nd = N0")
print("  (Proof: witness (-m/g, k/g, 0) for any n)")
print("=" * 75)

# Collect all one-prime-per-group triples with n>=2 in range
triples_n2 = []
seen = set()
for a in range(2, 500):
    fa = factorize(a)
    if len(fa) != 1:
        continue
    pa = list(fa.keys())[0]
    k = fa[pa]
    for b in range(1, 500):
        fb = factorize(b)
        if len(fb) != 1:
            continue
        pb = list(fb.keys())[0]
        m = fb[pb]
        if pb == pa:
            continue
        c = a + b
        fc = factorize(c)
        if len(fc) != 1:
            continue
        pc = list(fc.keys())[0]
        nv = fc[pc]
        if pc == pa or pc == pb:
            continue
        if nv < 2:
            continue
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        triples_n2.append((a, b, pa, pb, pc, k, m, nv))

print(f"Found {len(triples_n2)} one-prime-per-group triples with n>=2 in [1,500)")

val_ok = 0
val_formula_ok = 0
val_formula_fail = 0
mixed_cases = []

for a, b, pa, pb, pc, k, m, nv in triples_n2:
    nd_b = nd_brute(a, b, bound=25)
    if nd_b is None:
        continue
    pred, regime, N0, N1, N2 = nd_valuation_regime_formula(pa, pb, pc, k, m, nv)
    if pred is not None:
        if pred == nd_b:
            val_formula_ok += 1
        else:
            val_formula_fail += 1
            print(
                f"  VAL FAIL: ({a},{b}) pa={pa}^{k} pb={pb}^{m} pc={pc}^{nv} "
                f"N0={N0},N1={N1},N2={N2} pred={pred} brute={nd_b} regime={regime}"
            )
    else:
        mixed_cases.append((a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2))

print(f"Valuation-regime cases: {val_formula_ok} correct, {val_formula_fail} fail")
print(f"Pairwise/mixed cases: {len(mixed_cases)}")

# -------------------------------------------------------------------
# Part 2: Analyze mixed-witness cases
# -------------------------------------------------------------------
print()
print("=" * 75)
print("Part 2: Mixed-witness (non-pure) cases — characterizing nd")
print("=" * 75)

for a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2 in mixed_cases:
    pure_min = min(N0, N1, N2)
    print(
        f"  ({a},{b}) pa={pa}^{k} pb={pb}^{m} pc={pc}^{nv}  "
        f"N0={N0} N1={N1} N2={N2} pure_min={pure_min}  nd_brute={nd_b}"
    )
    # Try to find the winning witness
    if k == 1:
        nd_mix, coords = nd_mixed_formula_k1(pa, pb, pc, m, nv)
        if coords:
            phi_a, phi_b, phi_c = coords
            print(
                f"    mixed witness (phi_a={phi_a}, phi_b={phi_b}, phi_c={phi_c}) "
                f"W={phi_b - phi_a} nd_mix={nd_mix}"
            )
    # Check if nd_b matches three-pure or something else
    ratio = nd_b / pure_min
    print(f"    ratio nd/pure_min = {nd_b}/{pure_min} = {ratio:.3f}")

# -------------------------------------------------------------------
# Part 3: Mixed-witness formula analysis for pa-largest cases
# -------------------------------------------------------------------
print()
print("=" * 75)
print("Part 3: Formula for nd when pa is the largest prime (k=1)")
print(
    "  Conjecture: nd = min over phi_c in {1} of min_{phi_b} max(pa|n-m*phi_b|, pb*phi_b, pc)"
)
print("=" * 75)

# Focus on cases where pa > pb > pc (a-prime largest)
pa_largest = [
    (a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2)
    for (a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2) in mixed_cases
    if pa > pb and pa > pc
]

print(f"Cases with pa largest: {len(pa_largest)}")
for a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2 in pa_largest:
    # Formula: for phi_c=1, minimize over phi_b of max(pa|n-m*phi_b|, pb*phi_b, pc)
    if k == 1:
        best_norm = float("inf")
        best_phib = None
        for phi_b in range(0, nv + 5):
            phi_a = nv - m * phi_b  # phi_c=1 case
            W = phi_b - phi_a
            if W == 0:
                continue
            norm = max(pa * abs(phi_a), pb * phi_b, pc)
            if norm < best_norm:
                best_norm = norm
                best_phib = phi_b
        # Continuous optimum: pa*|n-m*phi_b| = pb*phi_b → phi_b* = pa*n/(pb+pa*m)
        phi_b_star = pa * nv / (pb + pa * m)
        print(
            f"  ({a},{b}) pa={pa} pb={pb} pc={pc} k={k} m={m} n={nv}: "
            f"nd={nd_b} formula={best_norm} phi_b*={phi_b_star:.2f} best_phi_b={best_phib}"
        )
        print(f"    N0={N0} [pa*m={pa * m} pa*m/m={pa}; needs N0<=pc={pc}? {N0 <= pc}]")

# -------------------------------------------------------------------
# Part 4: Conjecture for mixed regime — nd = min(N0, 1D_opt, r_term)
# -------------------------------------------------------------------
print()
print("=" * 75)
print("Part 4: Unified formula conjecture")
print(
    "  nd = min over all phi_c>=1: [min_{phi_b} max(pa*|n*phi_c-m*phi_b|, pb*|phi_b|, pc*phi_c)]"
)
print(
    "  and also min over all phi_a>=1: [min_{phi_b} max(pa*phi_a, pb*|m*phi_a-n_like|, pc*|phi_c|)]"
)
print("=" * 75)

# For each mixed case, compute this 2D discrete optimization
for a, b, pa, pb, pc, k, m, nv, nd_b, N0, N1, N2 in mixed_cases[:10]:
    # General k: phi_p*k + phi_q*m = phi_r*n
    # Minimize max(pa*k*|phi_p|, pb*m*|phi_q|, pc*n*|phi_r|) / (k,m,n)?
    # Actually: norm = max(pa*|phi_p|, pb*|phi_q|, pc*|phi_r|)
    # Brute check with larger range to confirm nd_b
    nd_check = nd_brute(a, b, bound=30)
    formula_2d = float("inf")
    best_v = None
    for phi_c in range(-10, 11):
        for phi_b in range(-15, 16):
            # k*phi_a + m*phi_b = n*phi_c
            rhs = nv * phi_c - m * phi_b
            if rhs % k != 0:
                continue
            phi_a = rhs // k
            W = phi_b - phi_a
            if W == 0:
                continue
            norm = max(pa * abs(phi_a), pb * abs(phi_b), pc * abs(phi_c))
            if norm > 0 and norm < formula_2d:
                formula_2d = norm
                best_v = (phi_a, phi_b, phi_c)
    match = "OK" if formula_2d == nd_check else f"FAIL(nd={nd_check})"
    print(
        f"  ({a},{b}) pa={pa}^{k} pb={pb}^{m} pc={pc}^{nv} "
        f"nd={nd_check} 2D_opt={formula_2d} {match} v={best_v}"
    )

print()
print("Summary of Part 4: 2D optimization always recovers nd_brute?")
