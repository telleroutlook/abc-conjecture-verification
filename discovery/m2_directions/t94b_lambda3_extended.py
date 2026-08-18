"""
T94b — Extended verification of thm:f37 up to c=500.
Same logic as T94 but larger range and higher brute-force bound.
"""

import math
import itertools
from sympy import factorint


def squarefree_omega4_type112_triples(max_c=500):
    """Generate squarefree ω*=4 triples of type (1,1,2): |Pa|=|Pb|=1, |Pc|=2."""
    triples = []
    for a in range(1, max_c):
        for b in range(a, max_c - a + 1):
            c = a + b
            if c > max_c:
                break
            if math.gcd(a, b) != 1:
                continue
            fac_a = factorint(a) if a > 1 else {}
            fac_b = factorint(b) if b > 1 else {}
            fac_c = factorint(c) if c > 1 else {}
            # Check squarefree
            abc_fac = {}
            ok = True
            for fac in [fac_a, fac_b, fac_c]:
                for p, e in fac.items():
                    if e > 1:
                        ok = False
                        break
                    if p in abc_fac:
                        ok = False
                        break  # same prime in two groups impossible for coprime
                    abc_fac[p] = 1
                if not ok:
                    break
            if not ok:
                continue
            Pa = sorted(fac_a.keys())
            Pb = sorted(fac_b.keys())
            Pc = sorted(fac_c.keys())
            # Type (1,1,2): |Pa|=1, |Pb|=1, |Pc|=2
            if len(Pa) != 1 or len(Pb) != 1 or len(Pc) != 2:
                continue
            primes = sorted(abc_fac.keys())
            if len(primes) != 4:
                continue
            triples.append((a, b, c, Pa, Pb, Pc, primes))
    return triples


def brute_minima(Pa, Pb, Pc, bound=12):
    all_primes = Pa + Pb + Pc
    na, nb = len(Pa), len(Pb)
    norms = set()
    for vals in itertools.product(range(-bound, bound + 1), repeat=4):
        if all(v == 0 for v in vals):
            continue
        phi_pa = vals[:na]
        phi_pb = vals[na : na + nb]
        phi_pc = vals[na + nb :]
        if sum(phi_pa) + sum(phi_pb) != sum(phi_pc):
            continue
        if sum(phi_pa) == sum(phi_pb):
            continue
        norm = max(p * abs(v) for p, v in zip(all_primes, vals))
        if norm > 0:
            norms.add(norm)
    return sorted(set(norms))[:5]


def formula_f37(p1, p2, p3, p4):
    lam2 = min(2 * p2, p3)
    if p3 < 2 * p2:
        lam3 = min(2 * p2, p4)
    else:
        lam3 = min(3 * p2, p3)
    return lam2, lam3


print("T94b: Extended verify thm:f37 for squarefree ω*=4 type (1,1,2) triples, c≤500")
triples = squarefree_omega4_type112_triples(max_c=500)
print(f"Found {len(triples)} type-(1,1,2) triples")
print()

l2_ok = l2_fail = l3_ok = l3_fail = 0
case1_ok = case1_fail = case2_ok = case2_fail = 0
p4_branch_hits = 0  # Case 1 where p₄ < 2p₂

for a, b, c, Pa, Pb, Pc, primes in triples:
    p1, p2, p3, p4 = primes
    lam2_f, lam3_f = formula_f37(p1, p2, p3, p4)

    minima = brute_minima(Pa, Pb, Pc, bound=12)
    if len(minima) < 3:
        continue

    lam2_b, lam3_b = minima[1], minima[2]

    if lam2_b != lam2_f:
        l2_fail += 1
        if l2_fail <= 3:
            print(
                f"  L2-FAIL ({a},{b},{c}) primes={primes} brute={lam2_b} F36={lam2_f}"
            )
        continue
    l2_ok += 1

    case = 1 if p3 < 2 * p2 else 2
    if lam3_b == lam3_f:
        l3_ok += 1
        if case == 1:
            case1_ok += 1
        else:
            case2_ok += 1
        if case == 1 and p4 < 2 * p2:
            p4_branch_hits += 1
    else:
        l3_fail += 1
        if case == 1:
            case1_fail += 1
        else:
            case2_fail += 1
        print(
            f"  L3-FAIL ({a},{b},{c}) primes={primes} case={case} λ₃_brute={lam3_b} λ₃_F37={lam3_f}"
        )

print(f"λ₂ correct: {l2_ok}, failures: {l2_fail}")
print(f"λ₃ correct: {l3_ok}, failures: {l3_fail}")
print(
    f"  Case 1 (p₃<2p₂): {case1_ok} ok, {case1_fail} fail  (p₄-branch triggered: {p4_branch_hits})"
)
print(f"  Case 2 (p₃≥2p₂): {case2_ok} ok, {case2_fail} fail")

# Check: does p₄<2p₂ ever occur in Case 1 among these?
print()
if p4_branch_hits > 0:
    print("p₄-branch examples (Case 1, p₄<2p₂):")
    shown = 0
    for a, b, c, Pa, Pb, Pc, primes in triples:
        if shown >= 5:
            break
        p1, p2, p3, p4 = primes
        if p3 < 2 * p2 and p4 < 2 * p2:
            lam2_f, lam3_f = formula_f37(p1, p2, p3, p4)
            minima = brute_minima(Pa, Pb, Pc, bound=12)
            if len(minima) < 3:
                continue
            if minima[1] != lam2_f:
                continue
            print(f"  ({a},{b},{c}) primes={primes} λ₃=p₄={p4} (2p₂={2 * p2})")
            shown += 1

print(f"\nTotal type-(1,1,2) verified: {l3_ok}")
