"""
T62 — W_psi divisibility structure for non-squarefree triples
         + OB-13C gap: does LP multi-prime match brute nd generally?

Goals:
  1. For each non-squarefree triple, find the brute-force minimum nd vector.
  2. Compute W_phi and W_psi for that optimal vector.
  3. Check divisibility: nd | W_psi?  v_max | W_psi?  R | W_psi?
     Any prime p | W_psi for all triples?
  4. Compare GCD-pair construction norm vs brute nd — gap quantified.
  5. For (a=1, b squarefree, c=q^k): LP formula vs brute (OB-13C verification).
  6. For general non-squarefree: look for W_psi = f(a,b,c,nd,vmax,...).

DEFINITIONS:
  W_phi = sum_{p in Pb} phi_p  -  sum_{p in Pa} phi_p     (phi-Wronskian)
  W_psi = sum_{p in Pb} p*phi_p  -  sum_{p in Pa} p*phi_p  (psi-Wronskian)
  nd    = min{ max_p p*|phi_p| : phi in F(a,b), W_phi != 0 }
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

def brute_nd_full(a, b, bound=10):
    """Return (nd_norm, phi_dict, W_phi, W_psi) for the optimal non-degenerate vector."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    omega = len(all_p)
    if omega == 0 or omega > 6:
        return None
    cc = {p: fa.get(p, 0) + fb.get(p, 0) - fc.get(p, 0) for p in all_p}
    Pb, Pa = list(fb.keys()), list(fa.keys())
    best = {'norm': float('inf'), 'phi': None, 'W_phi': None, 'W_psi': None}
    for vals in iproduct(*[range(-bound, bound + 1)] * omega):
        phi = {all_p[i]: vals[i] for i in range(omega)}
        if all(v == 0 for v in vals):
            continue
        if sum(cc[p] * phi[p] for p in all_p) != 0:
            continue
        W_phi = sum(phi.get(p, 0) for p in Pb) - sum(phi.get(p, 0) for p in Pa)
        if W_phi == 0:
            continue
        norm = max(p * abs(phi[p]) for p in all_p)
        if norm == 0:
            continue
        if norm < best['norm']:
            best['norm'] = norm
            best['phi'] = dict(phi)
            best['W_phi'] = W_phi
            best['W_psi'] = sum(p * phi[p] for p in Pb) - sum(p * phi[p] for p in Pa)
    return best if best['norm'] < float('inf') else None

def gcd_pair_bound(a, b):
    """Min over all cross-group prime pairs with GCD reduction (OB-13B construction)."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    best = float('inf')
    best_label = ''
    def try_pair(p, vp, q, vq, lbl):
        nonlocal best, best_label
        g = math.gcd(vp, vq)
        norm = max(p * (vq // g), q * (vp // g))
        if norm < best:
            best, best_label = norm, lbl
    for p_a, v_a in fa.items():
        for p_c, v_c in fc.items():
            try_pair(p_a, v_a, p_c, v_c, f"AC({p_a},{p_c})")
    for p_b, v_b in fb.items():
        for p_c, v_c in fc.items():
            try_pair(p_b, v_b, p_c, v_c, f"BC({p_b},{p_c})")
    for p_a, v_a in fa.items():
        for p_b, v_b in fb.items():
            try_pair(p_a, v_a, p_b, v_b, f"AB({p_a},{p_b})")
    return best if best < float('inf') else None, best_label

def lp_multiprimer_nd(a, b):
    """For (a=1, b squarefree, c=q^k): LP formula for nd."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    if fa or len(fc) != 1 or any(v != 1 for v in fb.values()):
        return None  # Not the special case
    q = list(fc.keys())[0]
    k = fc[q]
    Pb = list(fb.keys())
    best_int = float('inf')
    for size in range(1, len(Pb) + 1):
        for T in combinations(Pb, size):
            H = sum(1.0 / p for p in T)
            t_star = k / H
            # Integer allocation: brute-force small range
            radius = int(t_star / min(T)) + 3
            for vals in iproduct(*[range(0, radius + 1)] * len(T)):
                if sum(vals) != k:
                    continue
                norm = max(T[i] * vals[i] for i in range(len(T))) if any(v > 0 for v in vals) else 0
                if norm > 0:
                    best_int = min(best_int, norm)
    return max(q, best_int) if best_int < float('inf') else None

# ── Test battery ──────────────────────────────────────────────────────────────
test_cases = [
    # squarefree baselines
    (2, 3), (3, 5), (5, 11), (2, 13),
    # non-squarefree: c = prime^k
    (1, 3), (1, 7), (1, 8), (1, 15), (1, 24), (1, 48), (1, 63), (1, 255),
    # a or b = prime^k
    (4, 5), (8, 1), (9, 16), (4, 21), (25, 2), (27, 5), (8, 3), (4, 25),
    # both non-squarefree
    (4, 9), (8, 9), (4, 45), (9, 25),
    # larger examples
    (1, 2**5 - 1), (1, 2**7 - 1), (16, 9), (32, 3),
]

print("T62: W_psi divisibility + OB-13C gap analysis")
print("=" * 110)
print(f"{'(a,b,c)':<16} {'sq':>3} {'v_max':>6} {'R':>5} {'nd':>5} {'W_phi':>7} {'W_psi':>8} "
      f"{'nd|Wp':>6} {'vm|Wp':>6} {'gap':>6} {'LP':>5}")
print("-" * 110)

divisibility_stats = {'nd_divides_Wpsi': 0, 'vmax_divides_Wpsi': 0, 'total': 0}
gap_cases = []

for (a, b) in test_cases:
    if math.gcd(a, b) != 1:
        continue
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = set(list(fa.keys()) + list(fb.keys()) + list(fc.keys()))
    omega = len(all_p)
    if omega < 2 or omega > 6:
        continue

    v_max = max([max(fa.values()) if fa else 0,
                 max(fb.values()) if fb else 0,
                 max(fc.values()) if fc else 0])
    R = rad(a * b * c)
    sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())

    res = brute_nd_full(a, b, bound=10)
    if res is None:
        continue

    nd = res['norm']
    W_phi = res['W_phi']
    W_psi = res['W_psi']

    nd_div = abs(W_psi) % nd == 0 if nd > 0 else True
    vm_div = abs(W_psi) % v_max == 0 if v_max > 0 else True

    gcd_norm, gcd_label = gcd_pair_bound(a, b)
    gap = (gcd_norm - nd) if gcd_norm is not None else None

    lp_nd = lp_multiprimer_nd(a, b) if not sq else None

    sq_str = 'Y' if sq else 'N'
    gap_str = str(gap) if gap is not None else '?'
    lp_str = str(lp_nd) if lp_nd is not None else '-'

    print(f"  ({a},{b},{c}){'':<5} {sq_str:>3} {v_max:>6} {R:>5} {nd:>5} "
          f"{W_phi:>7} {W_psi:>8} {'Y' if nd_div else 'N':>6} {'Y' if vm_div else 'N':>6} "
          f"{gap_str:>6} {lp_str:>5}")

    if not sq:
        divisibility_stats['total'] += 1
        if nd_div:
            divisibility_stats['nd_divides_Wpsi'] += 1
        if vm_div:
            divisibility_stats['vmax_divides_Wpsi'] += 1
        if gap is not None and gap > 0:
            gap_cases.append((a, b, c, nd, gcd_norm, gap, gcd_label))

print()
print("=" * 110)
print()

# ── Divisibility summary ──────────────────────────────────────────────────────
n = divisibility_stats['total']
print(f"NON-SQUAREFREE DIVISIBILITY (n={n}):")
print(f"  nd  | W_psi : {divisibility_stats['nd_divides_Wpsi']}/{n}  "
      f"({'ALL' if divisibility_stats['nd_divides_Wpsi'] == n else 'NOT ALL'})")
print(f"  v_max | W_psi: {divisibility_stats['vmax_divides_Wpsi']}/{n}  "
      f"({'ALL' if divisibility_stats['vmax_divides_Wpsi'] == n else 'NOT ALL'})")

print()

# ── GCD gap cases ─────────────────────────────────────────────────────────────
if gap_cases:
    print(f"OB-13C GAP CASES (GCD-pair norm > brute nd): {len(gap_cases)} triples")
    print(f"  {'(a,b,c)':<18} {'brute nd':>8} {'GCD norm':>9} {'gap':>5} {'best pair':>16}")
    for (a, b, c, nd, gn, gap, lbl) in sorted(gap_cases, key=lambda x: -x[5]):
        print(f"  ({a},{b},{c}){'':<7} {nd:>8} {gn:>9} {gap:>5} {lbl:>16}")
else:
    print("OB-13C: GCD-pair construction matches brute nd for all tested triples.")

print()

# ── W_psi formula search ──────────────────────────────────────────────────────
print("W_psi FORMULA SEARCH (non-squarefree, W_psi as function of triple invariants):")
print()
pattern_hits = {}
for (a, b) in test_cases:
    if math.gcd(a, b) != 1:
        continue
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())
    if sq:
        continue
    all_p_set = set(list(fa.keys()) + list(fb.keys()) + list(fc.keys()))
    omega = len(all_p_set)
    if omega < 2 or omega > 6:
        continue
    v_max = max([max(fa.values()) if fa else 0,
                 max(fb.values()) if fb else 0,
                 max(fc.values()) if fc else 0])
    R = rad(a * b * c)
    res = brute_nd_full(a, b, bound=10)
    if res is None:
        continue
    nd = res['norm']
    W_psi = res['W_psi']
    W_phi = res['W_phi']

    # Search for W_psi = sign * expr
    candidates = [
        (a, 'a'), (b, 'b'), (c, 'c'), (R, 'R'),
        (nd, 'nd'), (v_max, 'v_max'),
        (nd * v_max, 'nd*vm'), (nd * W_phi, 'nd*Wphi'),
        (R // nd if nd and R % nd == 0 else -1, 'R/nd'),
    ]
    found = False
    for sign in [1, -1]:
        for val, name in candidates:
            if val > 0 and W_psi == sign * val:
                key = f"W_psi={'+'if sign>0 else '-'}{name}"
                pattern_hits[key] = pattern_hits.get(key, 0) + 1
                print(f"  ({a},{b},{c}): W_psi={W_psi}, nd={nd}, W_phi={W_phi} → {key}")
                found = True
                break
        if found:
            break
    if not found:
        print(f"  ({a},{b},{c}): W_psi={W_psi}, nd={nd}, W_phi={W_phi} → [no simple formula]")

print()
print("Pattern frequency:", pattern_hits)
print()

# ── W_psi / nd ratio ──────────────────────────────────────────────────────────
print("W_psi/nd RATIO (non-squarefree only):")
ratios = []
for (a, b) in test_cases:
    if math.gcd(a, b) != 1:
        continue
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())
    if sq:
        continue
    all_p_set = set(list(fa.keys()) + list(fb.keys()) + list(fc.keys()))
    omega = len(all_p_set)
    if omega < 2 or omega > 6:
        continue
    res = brute_nd_full(a, b, bound=10)
    if res is None:
        continue
    nd = res['norm']
    W_psi = res['W_psi']
    if nd > 0:
        r = W_psi / nd
        ratios.append((a, b, c, nd, W_psi, r))
        print(f"  ({a},{b},{c}): W_psi/nd = {W_psi}/{nd} = {r:.4f}")

if ratios:
    vals = [abs(r) for *_, r in ratios]
    print(f"\n  |W_psi/nd| range: [{min(vals):.3f}, {max(vals):.3f}]")
    all_int = all(abs(r) == int(abs(r)) for *_, r in ratios)
    print(f"  W_psi/nd always integer: {'YES' if all_int else 'NO'}")
