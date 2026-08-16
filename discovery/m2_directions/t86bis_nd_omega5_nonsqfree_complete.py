"""
T86bis — Complete verification of zero-coordinate minimizer property for ALL
omega*=5 non-squarefree coprime triples with a,b <= 150 (2446 triples, 0 skips).

Classifies each triple into one of two sub-cases:

  Sub-case B1 (analytically proved, 82.5%):
    There exist two primes p_i, p_j in {p_1,...,p_4} (all primes except the
    largest p_5) with val(p_i)=val(p_j)=1 (squarefree) and p_i, p_j in
    different groups (Pa, Pb, Pc).  The cross-group Bezout vector
    (phi_{p_i}=1, phi_{p_j}=+-1, all others 0) is in the zero-p5 sub-lattice,
    satisfies W != 0, and has norm max(p_i, p_j) <= p_4 < p_5.
    Hence B_{p_5} <= p_4 < p_5.  Any all-nonzero phi with norm N < min_p B_p
    must have N < p_5 and p_5|phi_{p_5}| <= N < p_5, forcing phi_{p_5}=0 --
    contradiction with all-nonzero.

  Sub-case B2 (computationally verified, 17.5%):
    No squarefree cross-group pair in {p_1,...,p_4}.  Compute B_{p_5} via
    brute force (BB=8).  Verified B_{p_5} <= p_5 for all 427 such triples.
    The same p_5-forcing argument applies.

Result: nd(a,b) = min_p B_p for all 2446 non-squarefree omega*=5 triples,
0 violations, BB=8 for sub-case B2 (0 skips).
"""

import math
from itertools import product as iproduct
from collections import Counter

LIMIT = 150
BB_B2 = 8


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


def nd_sublattice(primes4, alpha4, ws4, bound):
    """Brute-force nd for a 4-prime sub-lattice (zero-p5 branch)."""
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=4):
        if all(x == 0 for x in coords):
            continue
        if sum(alpha4[i] * coords[i] for i in range(4)) != 0:
            continue
        if sum(ws4[i] * coords[i] for i in range(4)) == 0:
            continue
        nrm = max(primes4[i] * abs(coords[i]) for i in range(4))
        if nrm > 0:
            best = min(best, nrm)
    return best if best < float('inf') else None


def find_sqfree_cross_pair(sub4_primes, groups, vals):
    """Return (p_i, p_j) with val=1 each, in different groups, or None."""
    for i in range(4):
        for j in range(i + 1, 4):
            pi, pj = sub4_primes[i], sub4_primes[j]
            if groups[pi] != groups[pj] and vals[pi] == 1 and vals[pj] == 1:
                return (pi, pj)
    return None


# Build triple list
triples = []
seen = set()
for a in range(2, LIMIT + 1):
    fa = factorize(a)
    for b in range(2, LIMIT + 1):
        if math.gcd(a, b) != 1:
            continue
        c = a + b
        fb = factorize(b)
        fc = factorize(c)
        primes = sorted(set(list(fa) + list(fb) + list(fc)))
        if len(primes) != 5:
            continue
        if set(fa) & set(fb) or set(fa) & set(fc) or set(fb) & set(fc):
            continue
        if all(v == 1 for v in list(fa.values()) + list(fb.values()) + list(fc.values())):
            continue  # squarefree: handled analytically by thm:nd_sqfree_support
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
        ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
        vmax = max(list(fa.values()) + list(fb.values()) + list(fc.values()))
        triples.append((a, b, primes, alpha, ws, vmax, fa, fb, fc))

print(f"T86bis: omega*=5 non-squarefree zero-coord property (a,b<={LIMIT})")
print(f"Total triples: {len(triples)}")
print()

case_b1 = 0   # analytically proved via squarefree cross-pair
case_b2_ok = 0  # computationally verified (p5-forcing)
case_b2_viol = 0
case_skip = 0

b2_details = []

for a, b, primes, alpha, ws, vmax, fa, fb, fc in triples:
    p5 = primes[4]
    sub4_primes = primes[:4]

    # Group and valuation for {p1,...,p4}
    groups = {}
    vals = {}
    for p in sub4_primes:
        if p in fa:
            groups[p] = 'a'
            vals[p] = fa[p]
        elif p in fb:
            groups[p] = 'b'
            vals[p] = fb[p]
        else:
            groups[p] = 'c'
            vals[p] = fc[p]

    # Sub-case B1: analytic
    pair = find_sqfree_cross_pair(sub4_primes, groups, vals)
    if pair is not None:
        pi, pj = pair
        claimed_ub = max(pi, pj)
        # Verify: claimed_ub <= p5 (trivially true since pi,pj in {p1,...,p4})
        assert claimed_ub < p5, f"B1 claim failed: max({pi},{pj})={claimed_ub} >= p5={p5}"
        case_b1 += 1
        continue

    # Sub-case B2: compute B_{p5}
    sub_alpha = alpha[:4]
    sub_ws = ws[:4]
    bp5 = nd_sublattice(sub4_primes, sub_alpha, sub_ws, BB_B2)

    if bp5 is None:
        case_skip += 1
        print(f"  SKIP ({a},{b}): B_{{p5={p5}}} not found with BB={BB_B2}, primes={primes}")
        continue

    if bp5 <= p5:
        case_b2_ok += 1
        b2_details.append((a, b, primes, bp5, p5))
    else:
        case_b2_viol += 1
        print(f"  VIOLATION ({a},{b}): B_{{p5={p5}}}={bp5} > p5={p5}, primes={primes}")

total_verified = case_b1 + case_b2_ok
print(f"Results:")
print(f"  Sub-case B1 (analytically proved):      {case_b1:4d}  ({100*case_b1/len(triples):.1f}%)")
print(f"  Sub-case B2 OK (B_{{p5}} <= p5, BB={BB_B2}): {case_b2_ok:4d}  ({100*case_b2_ok/len(triples):.1f}%)")
print(f"  Sub-case B2 VIOLATIONS:                 {case_b2_viol:4d}")
print(f"  Skipped (BB insufficient):              {case_skip:4d}")
print(f"  Total verified: {total_verified}/{len(triples)}, violations: {case_b2_viol}")
print()
if case_b2_viol == 0 and case_skip == 0:
    print("ZERO-COORDINATE PROPERTY FULLY VERIFIED for all omega*=5 non-squarefree")
    print(f"triples with a,b <= {LIMIT}.")
    print()
    print(f"B2 sub-case: B_{{p5}} range = [{min(d[3] for d in b2_details)}, {max(d[3] for d in b2_details)}]")
    print(f"B2 worst margin (B_{{p5}} / p5): {max(d[3]/d[4] for d in b2_details):.3f}")
