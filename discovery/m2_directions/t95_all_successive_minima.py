"""
T95 — Probe all successive minima for squarefree type-(1,1,2) triples.

Status: REFUTED by the finite examples below.

Tested conjecture:
  The successive minima spectrum of F(a,b) for type-(1,1,2) ω*=4 triples equals
  the sorted merge of three arithmetic progressions:
    {k·p₂ : k≥1} ∪ {k·p₃ : k≥1} ∪ {k·p₄ : k≥1}

  i.e., λ_m(a,b) = m-th smallest value in this merged set.

The first two non-degenerate successive minima in F36 and the third-minimum
formula in F37 remain unaffected.  The proposed all-minima characterization is
false: the brute-force spectra contain additional valuation combinations that
are absent from the sorted union of single-prime multiples.

This script is discovery-tier evidence.  A zero exit status means that the two
known mismatching triples were replayed exactly; it is not a proof of any
universal positive statement.
"""

import itertools
import math
from sympy import factorint


def brute_minima_all(Pa, Pb, Pc, bound=20, count=10):
    """All successive non-degenerate norms up to given count."""
    all_primes = Pa + Pb + Pc
    na, nb = len(Pa), len(Pb)
    norms = set()
    for vals in itertools.product(range(-bound, bound+1), repeat=4):
        if all(v == 0 for v in vals):
            continue
        phi_pa = vals[:na]
        phi_pb = vals[na:na+nb]
        phi_pc = vals[na+nb:]
        if sum(phi_pa) + sum(phi_pb) != sum(phi_pc):
            continue
        if sum(phi_pa) == sum(phi_pb):
            continue
        norm = max(p * abs(v) for p, v in zip(all_primes, vals))
        if norm > 0:
            norms.add(norm)
    return sorted(norms)[:count]


def merged_multiples(p2, p3, p4, count=10):
    """Sorted merge of {k*p2}, {k*p3}, {k*p4} for k>=1."""
    from heapq import heappush, heappop
    h = [(p2, p2, 1), (p3, p3, 1), (p4, p4, 1)]
    result = []
    seen = set()
    while len(result) < count:
        val, p, k = heappop(h)
        if val not in seen:
            seen.add(val)
            result.append(val)
        heappush(h, (p * (k+1), p, k+1))
    return result


# Test on diverse triples
test_cases = [
    # (a, b, c, Pa, Pb, Pc)
    (1, 14, 15, [2], [7], [3, 5]),     # primes [2,3,5,7]
    (1, 21, 22, [2], [3], [7, 11]),    # primes [2,3,7,11]
    (1, 34, 35, [5], [2], [7, 17]),    # primes [2,5,7,17]  — wait: a=1 Pa=empty
    (2, 13, 15, [2], [13], [3, 5]),    # primes [2,3,5,13]
    (2, 35, 37, [2], [37], [5, 7]),    # primes [2,5,7,37]
    (7, 22, 29, [7], [2], [11, 29]),   # primes [2,7,11,29] — wait need to recalc
    (11, 26, 37, [11], [2], [13, 37]), # wait
]

# Recompute from actual factorization
from sympy import factorint

actual_cases = []
test_abc = [
    (1, 14, 15), (1, 21, 22), (2, 13, 15), (2, 35, 37),
    (3, 7, 10), (7, 22, 29), (11, 26, 37), (13, 46, 59),
    (17, 29, 46), (31, 43, 74),  # p4-branch cases
    (1, 33, 34), (1, 85, 86),    # Case 2 examples
]

for (a, b, c) in test_abc:
    if math.gcd(a, b) != 1: continue
    fac_a = factorint(a) if a > 1 else {}
    fac_b = factorint(b) if b > 1 else {}
    fac_c = factorint(c)
    Pa = sorted(fac_a.keys())
    Pb = sorted(fac_b.keys())
    Pc = sorted(fac_c.keys())
    if len(Pa) != 1 or len(Pb) != 1 or len(Pc) != 2: continue
    primes = sorted(list(fac_a.keys()) + list(fac_b.keys()) + list(fac_c.keys()))
    if len(primes) != 4: continue
    actual_cases.append((a, b, c, Pa, Pb, Pc, primes))

print("T95: All successive minima vs merged-multiples conjecture")
print(f"Testing {len(actual_cases)} type-(1,1,2) triples\n")

all_match = True
mismatched_cases = []
for (a, b, c, Pa, Pb, Pc, primes) in actual_cases:
    p1, p2, p3, p4 = primes
    brute = brute_minima_all(Pa, Pb, Pc, bound=20, count=10)
    conjecture = merged_multiples(p2, p3, p4, count=10)

    # Find first discrepancy
    match_up_to = 0
    for i in range(min(len(brute), len(conjecture))):
        if brute[i] == conjecture[i]:
            match_up_to = i + 1
        else:
            break

    ok = (brute == conjecture)
    if not ok:
        all_match = False
        mismatched_cases.append((a, b, c))
        print(f"MISMATCH ({a},{b},{c}) primes={primes}")
        print(f"  brute:     {brute}")
        print(f"  conjecture:{conjecture}")
        print(f"  match up to λ_{match_up_to}")
    else:
        print(f"✓ ({a},{b},{c}) primes={primes} | {brute[:8]}")

print()
print(f"All matched: {all_match}")

expected_mismatches = {(2, 13, 15), (3, 7, 10)}
actual_mismatches = set(mismatched_cases)
if all_match or actual_mismatches != expected_mismatches:
    print("T95 replay failed: expected exactly the known mismatches "
          f"{sorted(expected_mismatches)}, got {sorted(actual_mismatches)}.")
    raise SystemExit(1)
print("T95 REFUTATION REPLAYED: the merged-multiples spectrum fails at "
      "(2,13,15) and (3,7,10).")

# Show merged-multiples visualization for (1,14,15): [2,3,5,7]
print()
print("=== Merged-multiples structure for primes [2,3,5,7] (p2=3,p3=5,p4=7) ===")
p2, p3, p4 = 3, 5, 7
for v in merged_multiples(p2, p3, p4, count=15):
    sources = []
    if v % p2 == 0: sources.append(f"{v//p2}·{p2}")
    if v % p3 == 0: sources.append(f"{v//p3}·{p3}")
    if v % p4 == 0: sources.append(f"{v//p4}·{p4}")
    print(f"  {v:3d}  =  {', '.join(sources)}")
