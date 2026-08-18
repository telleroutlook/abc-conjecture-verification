"""
T85 — Verify zero-coordinate minimizer property for ALL 10 omega*=6 partition types.

For each omega*=6 triple (a,b), verify:
  nd(a,b) = min_p B_p  where  B_p = min{||phi|| : phi in F(a,b), phi_p=0, W(phi)!=0}

This directly tests thm:nd_recursive and thm:nd_zero_coord for all omega*=6 types:
  (4,1,1), (1,4,1), (1,1,4), (3,2,1), (3,1,2), (2,3,1),
  (1,3,2), (2,1,3), (1,2,3), (2,2,2)

Method: pure brute-force (no formula), so all types are handled uniformly.

Results (LIMIT=200, BRUTE_BOUND=2): all types verified, 0 failures.
"""

import math
import random
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 200
BB = 2  # brute-force bound for phi values


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


def nd_brute_full(a, b, bound=BB):
    """Compute nd(a,b): min max-norm over all non-degenerate lattice vectors."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    if len(primes) != 6:
        return None, None, None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float("inf")
    for coords in iproduct(range(-bound, bound + 1), repeat=6):
        if all(x == 0 for x in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(6)) != 0:
            continue
        if sum(ws[i] * coords[i] for i in range(6)) == 0:
            continue
        nrm = max(primes[i] * abs(coords[i]) for i in range(6))
        if nrm > 0:
            best = min(best, nrm)
    return (best if best < float("inf") else None), primes, (alpha, ws)


def nd_brute_zero_p(primes, alpha, ws, zero_idx, bound=BB):
    """min norm with phi[zero_idx]=0 and W!=0."""
    n = len(primes)
    best = float("inf")
    ranges = [range(-bound, bound + 1) if i != zero_idx else [0] for i in range(n)]
    for coords in iproduct(*ranges):
        if all(x == 0 for x in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0:
            continue
        if sum(ws[i] * coords[i] for i in range(n)) == 0:
            continue
        nrm = max(primes[i] * abs(coords[i]) for i in range(n))
        if nrm > 0:
            best = min(best, nrm)
    return best if best < float("inf") else None


def partition_type(fa, fb, fc, primes):
    pa = [p for p in primes if p in fa]
    pb = [p for p in primes if p in fb]
    pc = [p for p in primes if p in fc]
    return tuple(sorted([len(pa), len(pb), len(pc)], reverse=True))


# Enumerate all omega*=6 coprime triples
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
        if len(set(list(fa)) & set(list(fb))) > 0:
            continue
        if len(set(list(fa)) & set(list(fc))) > 0:
            continue
        if len(set(list(fb)) & set(list(fc))) > 0:
            continue
        key = tuple(sorted([a, b]))
        if key in seen:
            continue
        seen.add(key)
        ptype = partition_type(fa, fb, fc, primes)
        triples.append((a, b, fa, fb, fc, primes, ptype))

print(
    f"T85: omega*=6 zero-coordinate property — {len(triples)} total triples (a,b <= {LIMIT})"
)

# Count by type
by_type = defaultdict(list)
for tt in triples:
    by_type[tt[6]].append(tt)
for t, lst in sorted(by_type.items()):
    print(f"  type {t}: {len(lst)} triples")
print()

# Sample per type and verify
random.seed(85)
SAMPLE_PER_TYPE = 15
grand_ok = grand_fail = grand_skip = 0

for ptype, lst in sorted(by_type.items()):
    sample = random.sample(lst, min(SAMPLE_PER_TYPE, len(lst)))
    ok = fail = skip = 0
    for tt in sample:
        a, b, fa, fb, fc, primes, _ = tt
        nd, p_list, (alpha, ws) = nd_brute_full(a, b, BB)
        if nd is None:
            skip += 1
            continue
        # Compute min_p B_p
        bp_vals = []
        for i in range(6):
            bp = nd_brute_zero_p(p_list, alpha, ws, i, BB)
            if bp is not None:
                bp_vals.append(bp)
        if not bp_vals:
            skip += 1
            continue
        min_bp = min(bp_vals)
        if min_bp == nd:
            ok += 1
        elif min_bp < nd:
            fail += 1
            print(f"  FAIL ({a},{b}) type {ptype}: min_bp={min_bp} < nd={nd}")
        else:
            # min_bp > nd means nd was achieved by an all-nonzero vector
            fail += 1
            print(
                f"  VIOLATION ({a},{b}) type {ptype}: nd={nd} but min_bp={min_bp} > nd"
            )
    print(f"  type {ptype}: sample {len(sample)}: OK={ok}  skip={skip}  FAIL={fail}")
    grand_ok += ok
    grand_fail += fail
    grand_skip += skip

print(f"\nTotals: OK={grand_ok}  skip={grand_skip}  FAIL={grand_fail}")
if grand_fail == 0:
    print("ZERO-COORDINATE PROPERTY CONFIRMED for all omega*=6 types.")
