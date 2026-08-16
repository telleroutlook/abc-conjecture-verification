"""
T85bis — Complete verification of zero-coordinate minimizer property for ALL
omega*=6 non-squarefree coprime triples with a,b <= 200.

Uses the same p6-forcing argument as T86bis does for omega*=5.

Sub-case B1 (analytically proved):
  Two squarefree primes p_i, p_j in {p1,...,p5} in different groups.
  Cross-group Bezout gives B_{p6} <= max(p_i,p_j) <= p5 < p6.
  p6-forcing: any all-nonzero phi with norm N < B_{p6} <= p5 < p6 has
  p6|phi_{p6}| <= N < p6, forcing phi_{p6}=0 — contradiction.

Sub-case B2 (computationally verified):
  No squarefree cross-group pair in {p1,...,p5}.
  Compute B_{p6} via optimized 4-loop brute force on the zero-p6 sub-lattice
  (5 variables, 1 constraint → solve for 5th variable from constraint).
  Verify B_{p6} <= p6 for all such triples.

Key optimization: for the 5-variable constrained sub-lattice, iterate over
(phi1,...,phi4) and compute phi5 = -(sum_{i<5} alpha_i * phi_i) / alpha5.
This reduces cost from (2*BB+1)^5 to (2*BB+1)^4 per B2 triple.
"""

import math
from itertools import product as iproduct

LIMIT = 200
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


def nd_sublattice_5var(primes5, alpha5, ws5, bound):
    """
    Compute B_{p6} = min nd for zero-p6 sub-lattice (5 variables, 1 constraint).
    Uses 4-loop optimization: iterate over (phi1,...,phi4), solve phi5 from constraint.
    Requires alpha5[4] != 0 (always true since it's a valuation >= 1).
    """
    a5 = alpha5[4]  # alpha for the 5th prime (to solve from constraint)
    if a5 == 0:
        return None  # degenerate — shouldn't happen
    best = float('inf')
    for coords4 in iproduct(range(-bound, bound + 1), repeat=4):
        rhs = -sum(alpha5[i] * coords4[i] for i in range(4))
        if rhs % a5 != 0:
            continue
        phi5 = rhs // a5
        if abs(phi5) > bound:
            continue
        coords = list(coords4) + [phi5]
        if all(x == 0 for x in coords):
            continue
        W = sum(ws5[i] * coords[i] for i in range(5))
        if W == 0:
            continue
        nrm = max(primes5[i] * abs(coords[i]) for i in range(5))
        if nrm > 0:
            best = min(best, nrm)
    return best if best < float('inf') else None


def find_sqfree_cross_pair(sub_primes, groups, vals):
    """Return (p_i, p_j) with val=1 each, in different groups, or None."""
    n = len(sub_primes)
    for i in range(n):
        for j in range(i + 1, n):
            pi, pj = sub_primes[i], sub_primes[j]
            if groups[pi] != groups[pj] and vals[pi] == 1 and vals[pj] == 1:
                return (pi, pj)
    return None


# Build non-squarefree omega*=6 triple list
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
        if len(primes) != 6:
            continue
        if set(fa) & set(fb) or set(fa) & set(fc) or set(fb) & set(fc):
            continue
        # Exclude squarefree (all valuations == 1)
        if all(v == 1 for v in list(fa.values()) + list(fb.values()) + list(fc.values())):
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
        ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
        triples.append((a, b, primes, alpha, ws, fa, fb, fc))

print(f"T85bis: omega*=6 non-squarefree zero-coord property (a,b<={LIMIT})")
print(f"Total non-squarefree triples: {len(triples)}")
print()

case_b1 = 0
case_b2_ok = 0
case_b2_viol = 0
case_skip = 0

b2_details = []

for a, b, primes, alpha, ws, fa, fb, fc in triples:
    p6 = primes[5]
    sub5_primes = primes[:5]

    # Group/val lookup for {p1,...,p5}
    groups = {}
    vals = {}
    for p in sub5_primes:
        if p in fa:
            groups[p] = 'a'; vals[p] = fa[p]
        elif p in fb:
            groups[p] = 'b'; vals[p] = fb[p]
        else:
            groups[p] = 'c'; vals[p] = fc[p]

    # Sub-case B1: analytic
    pair = find_sqfree_cross_pair(sub5_primes, groups, vals)
    if pair is not None:
        pi, pj = pair
        assert max(pi, pj) < p6, f"B1 assertion: max({pi},{pj}) >= p6={p6}"
        case_b1 += 1
        continue

    # Sub-case B2: compute B_{p6} on zero-p6 sub-lattice (5 primes)
    sub_alpha = alpha[:5]
    sub_ws = ws[:5]
    bp6 = nd_sublattice_5var(sub5_primes, sub_alpha, sub_ws, BB_B2)

    if bp6 is None:
        case_skip += 1
        print(f"  SKIP ({a},{b}): B_{{p6={p6}}} not found with BB={BB_B2}, primes={primes}")
        continue

    if bp6 <= p6:
        case_b2_ok += 1
        b2_details.append((a, b, primes, bp6, p6))
    else:
        case_b2_viol += 1
        print(f"  VIOLATION ({a},{b}): B_{{p6={p6}}}={bp6} > p6={p6}, primes={primes}")

total_verified = case_b1 + case_b2_ok
print(f"Results:")
print(f"  Sub-case B1 (analytically proved):       {case_b1:5d}  ({100*case_b1/len(triples):.1f}%)")
print(f"  Sub-case B2 OK (B_{{p6}} <= p6, BB={BB_B2}):  {case_b2_ok:5d}  ({100*case_b2_ok/len(triples):.1f}%)")
print(f"  Sub-case B2 VIOLATIONS:                  {case_b2_viol:5d}")
print(f"  Skipped (BB insufficient):               {case_skip:5d}")
print(f"  Total verified: {total_verified}/{len(triples)}, violations: {case_b2_viol}")
print()
if case_b2_viol == 0 and case_skip == 0:
    print("ZERO-COORDINATE PROPERTY FULLY VERIFIED for all omega*=6 non-squarefree")
    print(f"triples with a,b <= {LIMIT}.")
    if b2_details:
        print(f"B2 sub-case: B_{{p6}} range = [{min(d[3] for d in b2_details)}, {max(d[3] for d in b2_details)}]")
        print(f"B2 worst margin (B_{{p6}} / p6): {max(d[3]/d[4] for d in b2_details):.3f}")
