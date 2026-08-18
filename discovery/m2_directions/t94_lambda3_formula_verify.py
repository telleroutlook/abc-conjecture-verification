"""
T94 — Verify corrected λ₃ formula for squarefree ω*=4 triples.

Proposed thm:f37:
  λ₂ = min(2p₂, p₃)           [F36]
  λ₃ = min(2p₂, p₄)           if p₃ < 2p₂   [Case 1: λ₂=p₃]
       min(3p₂, p₃)            if p₃ ≥ 2p₂   [Case 2: λ₂=2p₂]

Equivalent unified form:
  λ₃ = min(max(2p₂, p₃), p₄-branch)
  ... or simply: the "losing" branch of λ₂ + next candidate.

Also fixes nd calculation: use second_smallest{min_Pa, min_Pb, min_Pc} (E_n theorem).
"""

import math
import itertools
from sympy import factorint


def squarefree_omega4_triples(max_val=300):
    triples = []
    for a in range(1, max_val):
        for b in range(a, max_val):
            c = a + b
            if c > max_val:
                break
            if math.gcd(a, b) != 1:
                continue
            abc = a * b * c
            fac = factorint(abc)
            if any(v > 1 for v in fac.values()):
                continue
            primes = sorted(fac.keys())
            if len(primes) != 4:
                continue
            triples.append((a, b, c, primes))
    return triples


def classify_groups(a, b, c):
    def primes_of(n):
        if n <= 1:
            return []
        return sorted(factorint(n).keys())

    return primes_of(a), primes_of(b), primes_of(c)


def brute_minima(Pa, Pb, Pc, bound=12):
    all_primes = Pa + Pb + Pc
    na, nb = len(Pa), len(Pb)
    norms = set()
    for vals in itertools.product(range(-bound, bound + 1), repeat=len(all_primes)):
        if all(v == 0 for v in vals):
            continue
        phi_pa = list(vals[:na])
        phi_pb = list(vals[na : na + nb])
        phi_pc = list(vals[na + nb :])
        # Constraint: sum_Pa + sum_Pb = sum_Pc
        if sum(phi_pa) + sum(phi_pb) != sum(phi_pc):
            continue
        # Non-degeneracy: sum_Pa phi ≠ sum_Pb phi
        if sum(phi_pa) == sum(phi_pb):
            continue
        norm = max(p * abs(v) for p, v in zip(all_primes, vals))
        if norm > 0:
            norms.add(norm)
    return sorted(set(norms))[:6]


def nd_theory(Pa, Pb, Pc):
    """E_n theorem: nd = second smallest group minimum."""
    mins = []
    for grp in [Pa, Pb, Pc]:
        if grp:
            mins.append(min(grp))
    mins.sort()
    return mins[1] if len(mins) >= 2 else None


def formula_f37(p1, p2, p3, p4):
    """Proposed λ₂, λ₃ formulas (F36 + F37)."""
    lam2 = min(2 * p2, p3)
    if p3 < 2 * p2:  # Case 1: λ₂=p₃
        lam3 = min(2 * p2, p4)
    else:  # Case 2: λ₂=2p₂
        lam3 = min(3 * p2, p3)
    return lam2, lam3


print("T94: Verify thm:f37 (corrected λ₃ formula) for squarefree ω*=4 triples")
print("Generating triples up to c=200...")
triples = squarefree_omega4_triples(max_val=200)
print(f"Found {len(triples)} triples")
print()

nd_fail = l2_fail = l3_fail = 0
nd_ok = l2_ok = l3_ok = 0
case1_ok = case1_fail = case2_ok = case2_fail = 0

for a, b, c, primes in triples:
    Pa, Pb, Pc = classify_groups(a, b, c)
    p1, p2, p3, p4 = primes

    nd_t = nd_theory(Pa, Pb, Pc)
    if nd_t is None:
        continue

    minima = brute_minima(Pa, Pb, Pc, bound=10)
    if len(minima) < 3:
        continue

    lam1_b, lam2_b, lam3_b = minima[0], minima[1], minima[2]
    lam2_f, lam3_f = formula_f37(p1, p2, p3, p4)

    # Check nd
    if lam1_b != nd_t:
        nd_fail += 1
        if nd_fail <= 5:
            print(
                f"  ND-FAIL ({a},{b},{c}) Pa={Pa} Pb={Pb} Pc={Pc}: E_n={nd_t} brute={lam1_b}"
            )
        continue
    nd_ok += 1

    # Check λ₂
    if lam2_b != lam2_f:
        l2_fail += 1
        print(f"  L2-FAIL ({a},{b},{c}) primes={primes} brute={lam2_b} F36={lam2_f}")
        continue
    l2_ok += 1

    # Check λ₃
    case = 1 if p3 < 2 * p2 else 2
    if lam3_b == lam3_f:
        l3_ok += 1
        if case == 1:
            case1_ok += 1
        else:
            case2_ok += 1
    else:
        l3_fail += 1
        if case == 1:
            case1_fail += 1
        else:
            case2_fail += 1
        print(
            f"  L3-FAIL ({a},{b},{c}) primes={primes} case={case} "
            f"λ₂={lam2_b} brute_λ₃={lam3_b} F37={lam3_f}"
        )

print()
print(f"nd correct:   {nd_ok}  failures: {nd_fail}")
print(f"λ₂ correct:   {l2_ok}  failures: {l2_fail}")
print(f"λ₃ correct:   {l3_ok}  failures: {l3_fail}")
print(f"  Case 1 (p₃<2p₂): {case1_ok} ok, {case1_fail} fail")
print(f"  Case 2 (p₃≥2p₂): {case2_ok} ok, {case2_fail} fail")

# Additional: break down by prime-structure type
print()
print("=== Case statistics ===")
case1_count = case2_count = 0
for a, b, c, primes in triples:
    p1, p2, p3, p4 = primes
    if p3 < 2 * p2:
        case1_count += 1
    else:
        case2_count += 1
print(f"Case 1 (p₃<2p₂): {case1_count} triples")
print(f"Case 2 (p₃≥2p₂): {case2_count} triples")

# Also print summary table — first 25 with both formulas vs brute
print()
print("=== Sample (first 25 usable) ===")
print(
    f"{'triple':18s} {'primes':16s} {'nd':>4} {'λ₂_b':>5} {'λ₂_f':>5} {'λ₃_b':>6} {'λ₃_f':>6} case"
)
shown = 0
for a, b, c, primes in triples:
    if shown >= 25:
        break
    Pa, Pb, Pc = classify_groups(a, b, c)
    p1, p2, p3, p4 = primes
    nd_t = nd_theory(Pa, Pb, Pc)
    if nd_t is None:
        continue
    minima = brute_minima(Pa, Pb, Pc, bound=10)
    if len(minima) < 3:
        continue
    l1b, l2b, l3b = minima[0], minima[1], minima[2]
    if l1b != nd_t:
        continue
    l2f, l3f = formula_f37(p1, p2, p3, p4)
    if l2b != l2f:
        continue
    case = 1 if p3 < 2 * p2 else 2
    ok3 = "✓" if l3b == l3f else "✗"
    print(
        f"({a},{b},{c}){'':<7} {str(primes):<16} {l1b:>4} {l2b:>5} {l2f:>5} {l3b:>6} {ok3}{l3f:>5}  {case}"
    )
    shown += 1
