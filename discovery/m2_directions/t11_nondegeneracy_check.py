"""
T11 — Non-degeneracy check for Pasten lattice shortest vector (discovery tier)

QUESTION: Is the minimum-norm vector in F(a,b) always non-degenerate (W^psi != 0)?

The Wronskian W^psi(a,b) = ab * (sum_{p|b} v_p(b)/p * psi(p) - sum_{p|a} v_p(a)/p * psi(p))
measures whether psi is "non-degenerate."  A degenerate vector lies in the sublattice
  L_0 = { psi in F(a,b) : W^psi(a,b) = 0 }
which is a rank-(omega-2) sublattice of F(a,b).

SIGNIFICANCE:
- If shortest vector is always non-degenerate: Corollary C (Minkowski bound) gives a
  non-degenerate ψ with ||psi||_inf <= det(L)^{1/(omega-1)} unconditionally.
- If sometimes degenerate: the shortest non-degenerate vector could be larger.
  We measure the gap: ratio ||psi_nondeg||_inf / ||psi_min||_inf.

DISCOVERY TIER: no proof, no abc triples used for construction, pure exploration.
"""


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = 1
    return f


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def gcd_list(lst):
    g = 0
    for x in lst:
        g = gcd(g, abs(x))
    return g


def lcm(a, b):
    return a * b // gcd(a, b)


def rad(n):
    r = 1
    for p in factorize(n):
        r *= p
    return r


def wronskian_val(a, b, psi_map, fa, fb):
    sb = sum(fb[p] * psi_map.get(p, 0) / p for p in fb)
    sa = sum(fa[p] * psi_map.get(p, 0) / p for p in fa)
    return a * b * (sb - sa)


def setup_int_coeffs(a, b, c):
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(fa) | set(fb) | set(fc))
    denom = 1
    for p in primes:
        denom = lcm(denom, p)
    coeff = {}
    for p in fa:
        coeff[p] = coeff.get(p, 0) + fa[p] * (denom // p)
    for p in fb:
        coeff[p] = coeff.get(p, 0) + fb[p] * (denom // p)
    for p in fc:
        coeff[p] = coeff.get(p, 0) - fc[p] * (denom // p)
    return primes, coeff, fa, fb, fc


def find_shortest_vectors(a, b, c, bound=60):
    """
    Returns (norm_all_min, norm_nondeg_min, is_same):
      norm_all_min    = ||psi||_inf of shortest nonzero lattice vector (any)
      norm_nondeg_min = ||psi||_inf of shortest non-degenerate vector (W^psi != 0)
      is_same         = True if shortest vector is non-degenerate
    Returns (None, None, None) if rank > 3 or search is inconclusive.
    """
    primes, coeff, fa, fb, fc = setup_int_coeffs(a, b, c)
    omega = len(primes)
    rank = omega - 1
    items = [(p, coeff[p]) for p in primes]

    if rank == 1:
        (p1, c1), (p2, c2) = items[0], items[1]
        g = gcd(abs(c1), abs(c2))
        fund = {p1: c2 // g, p2: -(c1 // g)}
        norm = max(abs(v) for v in fund.values())
        W = wronskian_val(a, b, fund, fa, fb)
        nondeg = abs(W) > 1e-9
        if not nondeg:
            neg = {p: -v for p, v in fund.items()}
            nondeg = abs(wronskian_val(a, b, neg, fa, fb)) > 1e-9
        return norm, (norm if nondeg else None), nondeg, omega

    if rank == 2:
        dep_idx = max(range(3), key=lambda i: abs(items[i][1]))
        free = [i for i in range(3) if i != dep_idx]
        p_d, c_d = items[dep_idx]
        p1, c1 = items[free[0]]
        p2, c2 = items[free[1]]
        best_all = None
        best_nondeg = None
        for v1 in range(-bound, bound + 1):
            for v2 in range(-bound, bound + 1):
                if v1 == 0 and v2 == 0:
                    continue
                num = -(c1 * v1 + c2 * v2)
                if num % c_d != 0:
                    continue
                vd = num // c_d
                psi = {p1: v1, p2: v2, p_d: vd}
                norm = max(abs(v) for v in psi.values())
                if best_all is None or norm < best_all:
                    best_all = norm
                W = wronskian_val(a, b, psi, fa, fb)
                if abs(W) > 1e-9:
                    if best_nondeg is None or norm < best_nondeg:
                        best_nondeg = norm
        is_same = (
            best_all is not None and best_nondeg is not None and best_all == best_nondeg
        )
        return best_all, best_nondeg, is_same, omega

    if rank == 3:
        dep_idx = max(range(4), key=lambda i: abs(items[i][1]))
        free = [i for i in range(4) if i != dep_idx]
        p_d, c_d = items[dep_idx]
        (p1, c1), (p2, c2), (p3, c3) = [items[i] for i in free]
        best_all = None
        best_nondeg = None
        b3 = min(bound, 20)
        for v1 in range(-b3, b3 + 1):
            for v2 in range(-b3, b3 + 1):
                for v3 in range(-b3, b3 + 1):
                    if v1 == 0 and v2 == 0 and v3 == 0:
                        continue
                    num = -(c1 * v1 + c2 * v2 + c3 * v3)
                    if num % c_d != 0:
                        continue
                    vd = num // c_d
                    psi = {p1: v1, p2: v2, p3: v3, p_d: vd}
                    norm = max(abs(v) for v in psi.values())
                    if best_all is None or norm < best_all:
                        best_all = norm
                    W = wronskian_val(a, b, psi, fa, fb)
                    if abs(W) > 1e-9:
                        if best_nondeg is None or norm < best_nondeg:
                            best_nondeg = norm
        is_same = (
            best_all is not None and best_nondeg is not None and best_all == best_nondeg
        )
        return best_all, best_nondeg, is_same, omega

    return None, None, None, omega


TRIPLES = [
    # omega=2
    (1, 8, 9),
    (1, 3, 4),
    (1, 31, 32),
    (1, 127, 128),
    # omega=3
    (3, 125, 128),
    (1, 80, 81),
    (5, 27, 32),
    (1, 242, 243),
    (1, 48, 49),
    (13, 243, 256),
    (32, 49, 81),
    (7, 25, 32),
    (4, 121, 125),
    (1, 728, 729),
    # omega=4
    (1, 2400, 2401),
    (1, 4374, 4375),
    (8, 343, 351),
    (64, 135, 199),
    (2, 2673, 2675),
    (1, 3024, 3025),
    (5, 1024, 1029),
    # omega=5 (squarefree small)
    (2, 3, 5),
    (4, 5, 9),
    (8, 9, 17),
    (1, 35, 36),
]

print("T11: Non-degeneracy check for Pasten lattice shortest vector")
print("=" * 70)
print()
print("  QUESTION: Is the shortest nonzero lattice vector always non-degenerate?")
print("  W^psi(a,b) = ab*(sum_{p|b} v_p(b)/p*psi_p  -  sum_{p|a} v_p(a)/p*psi_p)")
print()

header = f"  {'(a,b,c)':>22}  {'ω':>2}  {'R':>8}  "
header += f"{'norm_all':>8}  {'norm_nd':>8}  {'gap':>6}  {'same?':>6}  {'note'}"
print(header)
print("  " + "-" * 80)

stats = {2: [], 3: [], 4: [], 5: []}
degenerate_cases = []

for a, b, c in TRIPLES:
    if a + b != c or gcd(a, b) != 1:
        continue
    fa = factorize(a)
    fb = factorize(b)
    fc = factorize(c)
    omega_actual = len(set(fa) | set(fb) | set(fc))
    R = rad(a) * rad(b) * rad(c)

    norm_all, norm_nd, is_same, omega = find_shortest_vectors(a, b, c, bound=60)

    if norm_all is None:
        note = "omega>4 skip"
        print(
            f"  {str((a, b, c)):>22}  {omega:>2}  {R:>8}  {'skip':>8}  {'skip':>8}  {'--':>6}  {'--':>6}  {note}"
        )
        continue

    if norm_nd is None:
        note = "ALL DEGENERATE"
        gap_str = "N/A"
        same_str = "NO"
        degenerate_cases.append((a, b, c))
    else:
        gap = norm_nd / norm_all if norm_all > 0 else 1.0
        gap_str = f"{gap:.2f}"
        same_str = "YES" if is_same else "NO"
        note = "" if is_same else f"gap={gap:.2f}"
        if not is_same:
            degenerate_cases.append((a, b, c))

    nd_str = str(norm_nd) if norm_nd is not None else "N/A"
    print(
        f"  {str((a, b, c)):>22}  {omega:>2}  {R:>8}  "
        f"{str(norm_all):>8}  {nd_str:>8}  {gap_str:>6}  {same_str:>6}  {note}"
    )

    if omega in stats:
        stats[omega].append(
            {
                "norm_all": norm_all,
                "norm_nd": norm_nd,
                "same": is_same,
                "gap": norm_nd / norm_all if norm_nd and norm_all else None,
            }
        )

print()
print("[Summary by omega]")
print()
print(f"  {'ω':>2}  {'n':>3}  {'all_same':>8}  {'max_gap':>8}  {'mean_gap':>9}")
print("  " + "-" * 38)

for omg in [2, 3, 4, 5]:
    data = stats[omg]
    if not data:
        continue
    n_same = sum(1 for d in data if d["same"])
    gaps = [d["gap"] for d in data if d["gap"] is not None]
    max_gap = max(gaps) if gaps else 1.0
    mean_gap = sum(gaps) / len(gaps) if gaps else 1.0
    print(
        f"  {omg:>2}  {len(data):>3}  {n_same:>3}/{len(data):<3}  "
        f"{max_gap:>8.3f}  {mean_gap:>9.3f}"
    )

print()
print("[Non-degenerate cases where shortest vector is degenerate]")
if degenerate_cases:
    for t in degenerate_cases:
        print(f"  {t}")
else:
    print("  NONE — shortest vector is non-degenerate in all tested cases.")

print()
print("[Analysis]")
print()
print("  The Pasten lattice F(a,b) has rank (omega-1).")
print("  The degenerate sublattice L_0 = {psi in F(a,b) : W^psi=0} has rank (omega-2).")
print("  Generically, the complement F(a,b) \\ L_0 is dense: a random vector in F is")
print("  non-degenerate with probability 1 (measure argument).")
print("  The question is whether the SHORTEST vector happens to lie in L_0.")
print()
print("  If L_0 is a 'thin' sublattice (determinant >> det(L)):")
print(
    "    The shortest non-degenerate vector is approximately as short as the shortest vector."
)
print(
    "    det(L_0) / det(L) = ||c_W|| / gcd(c_W) where c_W is the Wronskian constraint vector."
)
print()
print("[Conclusion]")
print()
if not degenerate_cases:
    print("  ALL TESTED CASES: shortest vector is non-degenerate (gap = 1).")
    print("  Empirical evidence supports: for coprime (a,b,c) with omega >= 2,")
    print("  the minimum-norm vector in F(a,b) is always non-degenerate.")
    print()
    print(
        "  SIGNIFICANCE: If this holds universally, Corollary C (OB-09) strengthens to:"
    )
    print(
        "    'There exists a NON-DEGENERATE psi with ||psi||_inf <= det(L)^{1/(omega-1)}'"
    )
    print("  without any additional argument about non-degeneracy.")
    print()
    print("  STATUS: empirical support only; no proof attempted.")
    print("  Next step: E6 (T12) measures det(L)/R for bounded-exponent subfamily.")
else:
    print(f"  {len(degenerate_cases)} triple(s) have a degenerate shortest vector.")
    print("  The gap (norm_nd / norm_all) measures how much longer the shortest")
    print("  non-degenerate vector is relative to the absolute shortest vector.")
    print(
        "  A bounded gap (e.g. gap <= 2) would preserve the O(R^{1/(omega-1)}) bound."
    )
