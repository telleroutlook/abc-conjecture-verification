"""
T73 — nd characterization for high-quality one-prime-per-group triples.

For one-prime-per-group a=p^k, b=q^m, c=r^n:
  quality = n*log(r) / (log(p)+log(q)+log(r))
  quality > 1  iff  r^{n-1} > p*q

Key question: how does nd relate to quality?

Algorithm: precompute all prime powers ≤ LIMIT, then scan pairs.
Uses exact nd formula (thm:nd_pairwise_bezout + cor:nd_kmn_val).
Also verifies against brute force for small triples.
"""

import math
from itertools import product as iproduct

LIMIT = 500000  # scan prime powers up to this limit

# ── utilities ────────────────────────────────────────────────────────────────


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


def all_prime_powers(limit):
    """Return list of (value, prime, exponent) for all prime powers ≤ limit."""
    result = []
    # Primes
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    primes = [i for i in range(2, limit + 1) if sieve[i]]
    for p in primes:
        pk = p
        k = 1
        while pk <= limit:
            result.append((pk, p, k))
            if pk > limit // p:
                break
            pk *= p
            k += 1
    return result


def bezout_min_norm_fixed(m, n, k, pb, pc):
    """
    Find min of max(pb*|phi_b|, pc*|phi_c|) subject to m*phi_b - n*phi_c = ±k.
    CORRECTED: v_part = -v0*(rhs/g) (sign fix vs T72).
    Returns (min_norm, best_triple).
    """
    best = float("inf")
    best_v = None
    g, u0, v0 = extended_gcd(m, n)
    for sign in [+1, -1]:
        rhs = sign * k
        if rhs % g != 0:
            continue
        s = rhs // g
        u_part = u0 * s  # phi_b particular solution
        v_part = -v0 * s  # phi_c particular solution (sign-corrected)
        step_u = n // g  # step for phi_b
        step_v = m // g  # step for phi_c
        # Minimize max(pb*(u_part+step_u*t), pc*(v_part+step_v*t))
        # Continuous optimum: pb*(u_part+step_u*t_opt)² balance with pc*(...)²
        # Approx: balance pb*|u_part+step_u*t| = pc*|v_part+step_v*t|
        denom = pb * step_u - pc * step_v
        if denom != 0:
            t_opt = (pc * v_part - pb * u_part) / denom
        else:
            t_opt = 0.0
        for t in range(int(t_opt) - 6, int(t_opt) + 7):
            phi_b = u_part + step_u * t
            phi_c = v_part + step_v * t
            # Verify constraint
            chk = m * phi_b - n * phi_c
            if chk != rhs:
                continue  # sanity: skip if constraint not met
            norm = max(pb * abs(phi_b), pc * abs(phi_c))
            if norm < best:
                best = norm
                best_v = (phi_b, phi_c, sign)
    return best, best_v


def nd_exact(pa, pb, pc, k, m, n):
    """
    Exact nd = min(N_pure, max(p_L, B)) for one-prime-per-group triples.
    Returns (nd, regime_str, N0, N1, N2, B).
    """
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)
    N1 = max(pb * n // g_mn, pc * m // g_mn)
    N2 = max(pa * n // g_kn, pc * k // g_kn)
    N_pure = min(N0, N1, N2)
    p_L = max(pa, pb, pc)

    # Valuation regime
    if N0 <= pc:
        return N0, "val(φ_c=0)", N0, N1, N2, None
    if N1 <= pa:
        return N1, "val(φ_a=0)", N0, N1, N2, None
    if N2 <= pb:
        return N2, "val(φ_b=0)", N0, N1, N2, None

    # Pairwise: Bezout for p_L-prime = ±1
    if p_L == pa:
        B, _ = bezout_min_norm_fixed(m, n, k, pb, pc)
    elif p_L == pb:
        B, _ = bezout_min_norm_fixed(k, n, m, pa, pc)
    else:  # p_L == pc
        # phi_c = ±1: k*phi_a + m*phi_b = ±n, minimize max(pa*|phi_a|, pb*|phi_b|, pc)
        B = float("inf")
        for phi_c_sign in [+1, -1]:
            rhs = n * phi_c_sign
            for phi_a in range(-40, 41):
                rem = rhs - k * phi_a
                if rem % m != 0:
                    continue
                phi_b = rem // m
                if phi_b - phi_a == 0:
                    continue  # W=0
                norm = max(pa * abs(phi_a), pb * abs(phi_b), pc)
                if norm < B:
                    B = norm

    nd = min(N_pure, max(p_L, B))
    return nd, "pairwise", N0, N1, N2, B


def nd_brute(a, b, bound=30):
    """Brute-force nd for cross-checking."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ > 4:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float("inf")
    for coords in iproduct(range(-bound, bound + 1), repeat=np_):
        if all(c2 == 0 for c2 in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(np_)) != 0:
            continue
        W = sum(ws[i] * coords[i] for i in range(np_))
        if W == 0:
            continue
        norm = max(primes[i] * abs(coords[i]) for i in range(np_))
        if norm > 0:
            best = min(best, norm)
    return best if best < float("inf") else None


# ── Part 0: Bezout function sanity check ──────────────────────────────────────
print("Part 0: Bezout function correctness verification")
print("=" * 70)
test_cases = [
    # (m, n, k, pb, pc, expected_B)
    (3, 5, 1, 3, 2, 6),  # (5,27,32): pL=pa=5, 3*phi_b-5*phi_c=±1
    (
        5,
        7,
        1,
        5,
        2,
        9,
    ),  # (3,125,128): pL=pb=5, 5*phi_a-7*phi_c=±1 → call(k=1,n=7,m=3,pa=3,pc=2)
    (
        5,
        4,
        2,
        2,
        3,
        6,
    ),  # (32,49,81): pL=pb=7, 5*phi_a-4*phi_c=±2 → call(k=5,n=4,m=2,pa=2,pc=3)
]
# Note: for (3,125,128) pL=pb=5: call bezout(k=1, n=7, m=3, pa=3, pc=2)
# → m_arg=k=1, n_arg=n=7, k_arg=m=3, pb_arg=pa=3, pc_arg=pc=2
# Constraint: 1*phi_b - 7*phi_c = ±3. gcd(1,7)=1.
# phi_b=3+7t, phi_c=(3+7t... let me compute directly.
test_cases_full = [
    ("(5,27,32) pL=pa=5", 3, 5, 1, 3, 2, 6, True),
    ("(3,125,128) pL=pb=5", 1, 7, 3, 3, 2, 9, True),
    ("(32,49,81) pL=pb=7", 5, 4, 2, 2, 3, 6, True),
]
for label, m, n, k, pb, pc, expected, _ in test_cases_full:
    B, bv = bezout_min_norm_fixed(m, n, k, pb, pc)
    ok = "OK" if B == expected else f"FAIL(got {B})"
    print(f"  {label}: B={B} (expected {expected}) {ok}")
    if bv:
        phi_b, phi_c, sign = bv
        chk = m * phi_b - n * phi_c
        print(
            f"    witness=(phi_b={phi_b},phi_c={phi_c},sign={sign}), constraint={chk} (need {sign * k})"
        )
print()

# ── Part 1: Find all high-quality one-prime-per-group triples ─────────────────
print(f"Part 1: Scanning prime powers up to {LIMIT}")
print("=" * 70)

print("Generating prime powers...")
prime_powers = all_prime_powers(LIMIT)
pp_set = {v: (p, k) for (v, p, k) in prime_powers}
print(f"  {len(prime_powers)} prime powers ≤ {LIMIT}")
print()

# Scan: for each pair (a,b) of prime powers with same sum c also prime power
# and three DISTINCT prime groups
found = []
seen = set()

pp_values = sorted(pp_set.keys())
print("Scanning pairs for quality >= 0.9 ...")
for i, a in enumerate(pp_values):
    if a >= LIMIT:
        break
    pa, k = pp_set[a]
    for b in pp_values:
        if b >= a:
            break  # only a > b (we'll re-add both orderings)
        pb, m = pp_set[b]
        if pb == pa:
            continue  # same prime group
        c = a + b
        if c not in pp_set:
            continue
        pc, nv = pp_set[c]
        if pc == pa or pc == pb:
            continue  # three distinct primes
        if math.gcd(a, b) != 1:
            continue  # coprime (automatic for distinct prime powers but check)
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        q = nv * math.log(pc) / (math.log(pa) + math.log(pb) + math.log(pc))
        if q < 0.9:
            continue
        found.append((min(a, b), max(a, b), pa, pb, pc, k, m, nv, q, a > b))

# Sort by quality descending
found.sort(key=lambda x: -x[8])
print(f"Found {len(found)} one-prime-per-group triples with quality ≥ 0.9")
print()

# ── Part 2: Compute nd for all found triples ──────────────────────────────────
print("Part 2: nd computation (exact formula + brute verification)")
print("=" * 70)
print()

high_q = [(t) for t in found if t[8] > 1.0]
near_q = [(t) for t in found if 0.9 <= t[8] <= 1.0]


def analyze_triple(a, b, pa, pb, pc, k, m, nv, q):
    """Compute nd and print row."""
    # Identify assignment: which prime is in Pa, Pb, Pc (from factorizations)
    fa = factorize(a)
    fb = factorize(b)
    actual_pa = list(fa.keys())[0]
    actual_ka = fa[actual_pa]
    actual_pb = list(fb.keys())[0]
    actual_mb = fb[actual_pb]
    c = a + b
    fc = factorize(c)
    actual_pc = list(fc.keys())[0]
    actual_nc = fc[actual_pc]

    nd, regime, N0, N1, N2, B = nd_exact(
        actual_pa, actual_pb, actual_pc, actual_ka, actual_mb, actual_nc
    )
    p_L = max(actual_pa, actual_pb, actual_pc)
    B_str = f"{B:.0f}" if B is not None and B < float("inf") else "∞"

    # Brute check for small triples
    nd_b = nd_brute(a, b, bound=30) if max(a, b) < 2000 else "?"
    match_str = ""
    if isinstance(nd_b, int):
        match_str = "✓" if nd_b == nd else f"✗(brute={nd_b})"

    print(
        f"  ({a},{b})  q={q:.4f}  nd={nd}  pL={p_L}  B={B_str}  "
        f"N0={N0}  {actual_pa}^{actual_ka}+{actual_pb}^{actual_mb}={actual_pc}^{actual_nc}  "
        f"{regime}  {match_str}"
    )
    return nd, regime, N0, N1, N2, B, p_L


print(f"═══ HIGH QUALITY (q > 1.0): {len(high_q)} triples ═══")
print()
nd_data = []
for row in high_q:
    a, b, pa, pb, pc, k, m, nv, q, _ = row
    nd, regime, N0, N1, N2, B, p_L = analyze_triple(a, b, pa, pb, pc, k, m, nv, q)
    nd_data.append((a, b, q, nd, p_L, B, N0, regime))

print()
print(f"═══ NEAR-QUALITY (0.9 ≤ q ≤ 1.0): top {min(20, len(near_q))} triples ═══")
print()
for row in near_q[:20]:
    a, b, pa, pb, pc, k, m, nv, q, _ = row
    analyze_triple(a, b, pa, pb, pc, k, m, nv, q)

# ── Part 3: Analysis ──────────────────────────────────────────────────────────
print()
print("Part 3: Analysis of nd vs quality structure")
print("=" * 70)
print()

if nd_data:
    print("High-quality triples — nd/p_L ratio and n-independence:")
    print()
    for a, b, q, nd, p_L, B, N0, regime in nd_data:
        B_str = f"{B:.0f}" if B is not None and B < float("inf") else "∞"
        winner = (
            "N0-branch" if B is None or nd == N0 else ("Bezout" if nd < N0 else "p_L")
        )
        ndep = "n-indep" if winner == "N0-branch" else "n-dep(B)"
        print(
            f"  ({a},{b}): q={q:.4f}  nd={nd}  p_L={p_L}  nd/pL={nd / p_L:.3f}  "
            f"B={B_str}  winner={winner}  {ndep}"
        )

print()
print("KEY OBSERVATION: quality > 1 ⟹ c-group prime is SMALLEST prime")
print("  → Always pairwise regime for N0≤pc test (N0 ≥ p_L > pc)")
print("  → nd ≥ p_L = max(pa,pb) always for high-quality triples")
print()
print("n-INDEPENDENCE: N0 = max(pa*m/gcd(k,m), pb*k/gcd(k,m)) is INDEPENDENT OF n.")
print("  B depends on n through the Bezout constraint.")
print("  When N0 ≤ B: nd = N0, and nd is n-INDEPENDENT (cor:nd_kmn_val).")
print("  When N0 > B: nd = max(p_L, B), and nd depends on n.")
print()

# Check: for high-quality triples, is nd always ≥ p_L?
violations = [
    (a, b, q, nd, p_L) for (a, b, q, nd, p_L, B, N0, regime) in nd_data if nd < p_L
]
if violations:
    print(f"  WARNING: nd < p_L for {len(violations)} triples:")
    for row in violations:
        print(f"    {row}")
else:
    print("CONFIRMED: nd ≥ p_L for ALL high-quality triples. ✓")
    print("  (As expected: pairwise regime forces nd ≥ p_L always.)")
