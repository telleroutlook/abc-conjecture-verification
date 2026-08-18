"""
T20 — ω=5 squarefree non-degeneracy classification via φ-coordinates (discovery tier)

Uses Theorem F8 (φ-coordinate change) to analyze ALL ω=5 squarefree coprime triples.

In φ-coordinates (φ_q = ψ_q/q):
  F̃(a,b) = {φ∈ℤ^5 : ∑ sign_q·φ_q = 0}  (sign_q = +1 if q|ab, -1 if q|c)
  Wronskian: W = a·b·(S_b - S_a),  S_X = ∑_{q|X} φ_q
  Degenerate iff S_b = S_a

NON-DEGENERATE MINIMUM PREDICTION (from φ-framework):
  Minimum non-degen φ: take φ_{p_b}=1, φ_{p_a}=-1 for primes p_b∈P_b, p_a∈P_a
  (or p_b∈P_b, p_c=...  with S_b≠S_a). Norm = max(p_b·1, p_a·1) = max(p_b, p_a).
  Or for n_a=0: use φ_{p_b}=1 (norm p_b·1=p_b) if also satisfies constraint via φ_{p_c}.
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


def wronskian(a, b, psi_map, fa, fb):
    sb = sum(fb[p] * psi_map.get(p, 0) / p for p in fb)
    sa = sum(fa[p] * psi_map.get(p, 0) / p for p in fa)
    return a * b * (sb - sa)


def setup(a, b, c):
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


def check_lat(psi, coeff, primes):
    return sum(coeff[p] * psi.get(p, 0) for p in primes)


def find_min_nondeg(a, b, c, primes, coeff, fa, fb, fc, bound=60):
    """Find minimum ‖ψ‖_∞ over non-degen lattice vectors. Returns (min_nd, min_d, vector)."""
    assert len(primes) == 5
    p1, p2, p3, p4, p5 = primes
    min_nd = None
    min_d = None
    nd_vec = None
    # Enumerate φ-vectors: φ_q ∈ {-2,...,2} (ψ_q = q*φ_q, so ψ bound = q*2 ≤ p5*2)
    max_phi = max(1, bound // p5)
    for f1 in range(-max_phi, max_phi + 1):
        for f2 in range(-max_phi, max_phi + 1):
            for f3 in range(-max_phi, max_phi + 1):
                for f4 in range(-max_phi, max_phi + 1):
                    # determine f5 from constraint
                    # constraint: sign_p1*f1+...+sign_p5*f5 = 0
                    sign = {}
                    for p in fa:
                        sign[p] = sign.get(p, 0) + 1
                    for p in fb:
                        sign[p] = sign.get(p, 0) + 1
                    for p in fc:
                        sign[p] = sign.get(p, 0) - 1
                    # sign_p5*f5 = -(sign_p1*f1+...+sign_p4*f4)
                    sp5 = sign.get(p5, 0)
                    if sp5 == 0:
                        continue
                    rhs = -(
                        sign.get(p1, 0) * f1
                        + sign.get(p2, 0) * f2
                        + sign.get(p3, 0) * f3
                        + sign.get(p4, 0) * f4
                    )
                    if rhs % sp5 != 0:
                        continue
                    f5 = rhs // sp5
                    phi = {p1: f1, p2: f2, p3: p3, p4: f4, p5: f5}
                    phi = {p1: f1, p2: f2, p3: f3, p4: f4, p5: f5}
                    if all(v == 0 for v in phi.values()):
                        continue
                    psi = {q: q * phi[q] for q in primes}
                    norm = max(abs(q * phi[q]) for q in primes)
                    if norm > bound:
                        continue
                    W = wronskian(a, b, psi, fa, fb)
                    if abs(W) > 1e-9:  # non-degen
                        if min_nd is None or norm < min_nd:
                            min_nd = norm
                            nd_vec = dict(phi)
                    else:  # degen
                        if min_d is None or norm < min_d:
                            min_d = norm
    return min_nd, min_d, nd_vec


def predict_min_nd_phi(pa, pb, pc):
    """Predict min nd norm using φ-crossing: find cheapest pair giving S_b≠S_a."""
    # S_b = sum of φ_q for q in pb, S_a = sum for q in pa
    # Non-degen iff S_b ≠ S_a.
    # Strategy 1: φ_p=1 (p∈pb), φ_q=-1 (q∈pa), need lattice constraint satisfied.
    # Lattice: ∑ sign_q φ_q = 0: (∑_pa) + (∑_pb) - (∑_pc) = 0.
    # With φ_p=1 (p∈pb), φ_q=-1 (q∈pa), others 0: S_pb contribution = 1, S_pa contribution=-1.
    # Constraint: (-1)+(1) - 0 = 0. ✓ Always satisfies constraint!
    # Norm = max(p, q). S_b-S_a = 1-(-1) = 2 ≠ 0. Non-degen!
    # Minimum: choose p = min(pb), q = min(pa). Norm = max(min_pb, min_pa).
    if pa and pb:
        return max(min(pb), min(pa))
    # Strategy 2: n_a=0: φ_p=1 (p∈pb), φ_r=-1 (r∈pc). Constraint: 0+1-(-(-1))...
    # sign_p=+1 (b-side), sign_r=-1 (c-side). Constraint: 1+(-1)·(-1)...
    # Let's just compute: φ_p=1, φ_r=1 (c-side contributes -1 to ∑ sign·φ, so φ_r=1 → sign_r·φ_r=-1).
    # ∑ sign·φ = 1 + (-1)·1 = 0. ✓ S_b=1, S_a=0. W=ab·1≠0.
    if not pa and pb and pc:
        return max(min(pb), min(pc))
    return None


print("T20: ω=5 squarefree non-degeneracy classification via φ-coordinates (c≤200)")
print("=" * 75)
print()

type_stats = {}  # partition type → [total, nd_count, ratios, nd_norms]
all_triples = []

for c in range(6, 201):
    for a in range(2, (c + 1) // 2 + 1):
        b = c - a
        if b < a:
            continue
        if gcd(a, b) != 1:
            continue
        if not (is_squarefree(a) and is_squarefree(b) and is_squarefree(c)):
            continue
        fa = factorize(a)
        fb = factorize(b)
        fc = factorize(c)
        primes = sorted(set(fa) | set(fb) | set(fc))
        if len(primes) != 5:
            continue

        pa, pb, pc = sorted(fa.keys()), sorted(fb.keys()), sorted(fc.keys())
        tp = (len(pa), len(pb), len(pc))
        R = 1
        for p in primes:
            R *= p
        primes_full, coeff, fa2, fb2, fc2 = setup(a, b, c)

        # Predict min nd from φ-framework
        pred_nd = predict_min_nd_phi(pa, pb, pc)

        # Find actual min nd and min degen (with small bound for speed)
        min_nd, min_d, nd_vec = find_min_nondeg(
            a, b, c, primes, coeff, fa2, fb2, fc2, bound=50
        )

        is_degen = min_d is not None and (min_nd is None or min_d < min_nd)
        ratio_nd = (
            min_nd / R ** (1.0 / 4) if min_nd is not None else None
        )  # R^{1/(ω-1)} = R^{1/4}

        key = tp
        if key not in type_stats:
            type_stats[key] = {
                "total": 0,
                "nd_count": 0,
                "degen_count": 0,
                "ratios": [],
                "pred_ok": 0,
                "pred_fail": 0,
            }
        type_stats[key]["total"] += 1
        if is_degen:
            type_stats[key]["degen_count"] += 1
        else:
            type_stats[key]["nd_count"] += 1
        if ratio_nd is not None:
            type_stats[key]["ratios"].append(ratio_nd)
        if pred_nd is not None and min_nd is not None:
            if abs(pred_nd - min_nd) <= 0:  # exact match
                type_stats[key]["pred_ok"] += 1
            else:
                type_stats[key]["pred_fail"] += 1
                # Don't flood output, just count

        all_triples.append((a, b, c, tp, min_nd, min_d, ratio_nd, pred_nd))

print(f"Found {len(all_triples)} squarefree ω=5 triples with c≤200.")
print()

print("=" * 75)
print("PARTITION TYPE SUMMARY")
print("=" * 75)
print()
print(
    f"  {'Type':>12}  {'Total':>6}  {'Degen':>6}  {'ND':>5}  {'MaxRatioND':>11}  {'PredOK/Fail':>11}  {'Pattern'}"
)
print("  " + "-" * 80)

for tp in sorted(type_stats.keys()):
    s = type_stats[tp]
    ratios = s["ratios"]
    max_r = max(ratios) if ratios else float("nan")
    pred_str = f"{s['pred_ok']}/{s['pred_fail']}"
    # Classify pattern
    all_degen = s["nd_count"] == 0
    bounded = (max_r < 1.0) if ratios else False
    pattern = (
        "ALL_DEGEN"
        if all_degen
        else ("BOUNDED" if bounded else "UNBOUNDED" if max_r > 1.2 else "?")
    )
    print(
        f"  {str(tp):>12}  {s['total']:>6}  {s['degen_count']:>6}  {s['nd_count']:>5}  {max_r:>11.4f}  {pred_str:>11}  {pattern}"
    )

print()
print("=" * 75)
print("DETAILED EXAMPLES — one per type")
print("=" * 75)

seen_types = set()
for a, b, c, tp, min_nd, min_d, ratio_nd, pred_nd in sorted(
    all_triples, key=lambda x: (x[3], x[2])
):
    if tp in seen_types:
        continue
    seen_types.add(tp)
    fa = factorize(a)
    fb = factorize(b)
    fc = factorize(c)
    pa, pb, pc = sorted(fa.keys()), sorted(fb.keys()), sorted(fc.keys())
    R = 1
    for p in sorted(set(fa) | set(fb) | set(fc)):
        R *= p
    degen = min_d is not None and (min_nd is None or min_d < min_nd)
    print(f"  Type {tp}: ({a},{b},{c}) Pa={pa} Pb={pb} Pc={pc}")
    print(f"    R={R}  R^(1/4)={R**0.25:.3f}")
    print(f"    min_nd={min_nd}  min_d={min_d}  pred_nd={pred_nd}")
    if ratio_nd:
        print(f"    nd_ratio={ratio_nd:.4f}  degen_overall={degen}")
    print()

print()
print("=" * 75)
print("THEOREM F9 CONJECTURE (to verify/prove next)")
print("=" * 75)
print()
print("  Based on T20 findings:")
print()
print("  For squarefree ω=5 coprime (a,b,c), the Pasten lattice minimum non-degen")
print("  norm ‖ψ_nd‖_∞ via φ-crossing:")
print()
print("  BOUNDED types (nd-ratio ≤ C): those where ∃ p_b∈P_b, p_a∈P_a with")
print("    φ_{p_b}=1, φ_{p_a}=-1 (norm max(p_b,p_a)) AND S_b≠S_a achieved.")
print("    Norm ≤ R^{1/5} (trivially, since each prime ≤ R^{1/5}).")
print("    ??? → need to check if max(min_Pb, min_Pa) is bounded by R^{1/4}.")
print()
print("  UNBOUNDED types: isolated prime facing ≥3-prime constituent. Non-degen")
print("    forces ψ_r ≥ r (divisibility); norm = r → ∞.")
