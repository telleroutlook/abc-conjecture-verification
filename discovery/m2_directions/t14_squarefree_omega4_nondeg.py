"""
T14 — Squarefree ω=4 non-degeneracy: complete classification (discovery tier)

Extends T13 (ω=3) to ω=4.  Enumerates ALL squarefree coprime triples (a,b,c)
with a+b=c, ω(abc)=4, c≤300, and classifies:
  - partition type |Pa|, |Pb|, |Pc|
  - minimum all-vector norm λ₁(F)
  - minimum non-degenerate vector norm λ₁^nd(F)
  - ratio λ₁^nd / R^{1/(ω-1)} = λ₁^nd / R^{1/3}

KEY QUESTION: Is the shortest vector always non-degenerate for squarefree ω=4?
If not, how large can the ratio λ₁^nd / R^{1/3} be?

DISCOVERY TIER: no abc triples used for construction.
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


def lcm(a, b):
    return a * b // gcd(a, b)


def is_squarefree(n):
    return all(v == 1 for v in factorize(n).values())


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


def find_both_minima_rank3(a, b, c, bound=30):
    """For rank-3 lattice (omega=4), find min all-vectors and min non-degenerate."""
    primes, coeff, fa, fb, fc = setup_int_coeffs(a, b, c)
    items = [(p, coeff[p]) for p in primes]
    dep_idx = max(range(4), key=lambda i: abs(items[i][1]))
    free = [i for i in range(4) if i != dep_idx]
    p_d, c_d = items[dep_idx]
    (p1, c1), (p2, c2), (p3, c3) = [items[i] for i in free]

    best_all = None
    best_nd = None
    for v1 in range(-bound, bound + 1):
        for v2 in range(-bound, bound + 1):
            for v3 in range(-bound, bound + 1):
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
                    if best_nd is None or norm < best_nd:
                        best_nd = norm
    return best_all, best_nd, primes


print("T14: Squarefree omega=4 non-degeneracy — complete classification (c<=300)")
print("=" * 75)
print()

degenerate_cases = []
all_cases = []
max_ratio = 0.0
max_ratio_triple = None
partition_stats = {}  # (|Pa|,|Pb|,|Pc|) -> (count, degen_count, max_ratio)

count_total = 0
count_degen = 0

for c in range(4, 301):
    for a in range(1, (c + 1) // 2 + 1):
        b = c - a
        if b <= 0 or b < a:
            continue
        if gcd(a, b) != 1:
            continue
        if not (is_squarefree(a) and is_squarefree(b) and is_squarefree(c)):
            continue
        fa = factorize(a)
        fb = factorize(b)
        fc = factorize(c)
        omega = len(set(fa) | set(fb) | set(fc))
        if omega != 4:
            continue

        R = 1
        for p in set(fa) | set(fb) | set(fc):
            R *= p

        pa = sorted(fa.keys())
        pb = sorted(fb.keys())
        pc = sorted(fc.keys())
        ptype = (len(pa), len(pb), len(pc))

        best_all, best_nd, primes = find_both_minima_rank3(a, b, c, bound=25)
        if best_all is None:
            continue

        target = R ** (1.0 / 3)
        ratio_nd = best_nd / target if best_nd else None
        is_degen = best_nd is None or best_all != best_nd

        count_total += 1
        if is_degen:
            count_degen += 1
            degenerate_cases.append((a, b, c, R, ptype, best_all, best_nd, ratio_nd))

        if ratio_nd and ratio_nd > max_ratio:
            max_ratio = ratio_nd
            max_ratio_triple = (a, b, c, ptype)

        key = ptype
        if key not in partition_stats:
            partition_stats[key] = {
                "count": 0,
                "degen": 0,
                "max_ratio": 0.0,
                "max_triple": None,
            }
        partition_stats[key]["count"] += 1
        if is_degen:
            partition_stats[key]["degen"] += 1
        if ratio_nd and ratio_nd > partition_stats[key]["max_ratio"]:
            partition_stats[key]["max_ratio"] = ratio_nd
            partition_stats[key]["max_triple"] = (a, b, c)

        all_cases.append((a, b, c, R, ptype, best_all, best_nd, ratio_nd))

print(f"Total squarefree omega=4 triples (c<=300): {count_total}")
print(f"Degenerate shortest vectors: {count_degen}/{count_total}")
print()
print(f"Max ratio ||psi_nd||/R^{{1/3}}: {max_ratio:.4f} at {max_ratio_triple}")
print()

print("[Partition type breakdown]")
print(f"  {'type':>10}  {'count':>6}  {'degen':>6}  {'max_ratio':>10}  {'max_triple'}")
print("  " + "-" * 60)
for ptype in sorted(partition_stats.keys()):
    s = partition_stats[ptype]
    t = s["max_triple"]
    print(
        f"  {str(ptype):>10}  {s['count']:>6}  {s['degen']:>6}  {s['max_ratio']:>10.4f}  {t}"
    )
print()

print("[Degenerate cases (all)]")
if not degenerate_cases:
    print("  NONE — all shortest vectors are non-degenerate!")
else:
    print(
        f"  {'(a,b,c)':>18}  {'R':>8}  {'type':>10}  {'na':>5}  {'nd':>5}  {'ratio':>8}"
    )
    print("  " + "-" * 65)
    for a, b, c, R, ptype, na, nd, ratio in degenerate_cases:
        ratio_s = f"{ratio:.4f}" if ratio else "N/A"
        print(
            f"  {str((a, b, c)):>18}  {R:>8}  {str(ptype):>10}  {na:>5}  {str(nd) if nd else 'N/A':>5}  {ratio_s:>8}"
        )
print()

print("[Analytical structure for ω=4]")
print()
print("  For squarefree ω=4 triples, rank(F) = 3, rank(L₀) = 2.")
print("  Partition types by |Pa|,|Pb|,|Pc| with |Pa|+|Pb|+|Pc|=4:")
print("  (1,1,2): a prime, b prime, c=pqr — most common")
print("  (1,2,1): a prime, b=pq, c prime")
print("  (2,1,1): a=pq, b prime, c prime")
print("  (2,2,0): not possible (a+b=c, all prime factors of a,b must appear in c)")
print("  (1,3,0): not possible similarly")
print("  (0,2,2): a=1, b=pq, c=rs (checking...)")
print()
print("  EXPECTED: for most partition types, the shortest vector is non-degenerate.")
print("  The ratio bound analogous to ω=3 would be: λ₁^nd / R^{1/3} bounded by")
print("  some explicit constant depending on the partition type.")
print()
print("[Summary]")
print(f"  Total: {count_total}, Degenerate: {count_degen}, Max ratio: {max_ratio:.4f}")
print()
print("  STATUS: empirical survey complete (c<=300).")
if count_degen == 0:
    print("  FINDING: ALL shortest vectors are non-degenerate for squarefree ω=4.")
    print("  Conjecture: same holds for all ω≥3 squarefree triples.")
else:
    print(f"  FINDING: {count_degen} degenerate cases found — see table above.")
