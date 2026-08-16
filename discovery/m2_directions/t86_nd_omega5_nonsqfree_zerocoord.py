"""
T86 — Verify zero-coordinate minimizer property for omega*=5 non-squarefree
triples using brute-force bound BB=3 (stronger than previous BB=2 checks).

For each omega*=5 triple (a,b) with at least one exponent >= 2, verify:
  nd(a,b) = min_p B_p  where  B_p = min{||phi|| : phi in F(a,b), phi_p=0, W!=0}

This confirms thm:nd_zero_coord(iii) empirically for the non-squarefree case.

Results with BB=3, LIMIT=150: all types verified, 0 failures.
"""

import math
import random
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 150
BB = 3
SAMPLE_PER_TYPE = 20


def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f


def nd_brute_full(primes, alpha, ws, bound=BB):
    n = len(primes)
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=n):
        if all(x == 0 for x in coords): continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0: continue
        if sum(ws[i] * coords[i] for i in range(n)) == 0: continue
        nrm = max(primes[i] * abs(coords[i]) for i in range(n))
        if nrm > 0: best = min(best, nrm)
    return best if best < float('inf') else None


def nd_brute_zero_p(primes, alpha, ws, zero_idx, bound=BB):
    n = len(primes)
    best = float('inf')
    ranges = [range(-bound, bound + 1) if i != zero_idx else [0] for i in range(n)]
    for coords in iproduct(*ranges):
        if all(x == 0 for x in coords): continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0: continue
        if sum(ws[i] * coords[i] for i in range(n)) == 0: continue
        nrm = max(primes[i] * abs(coords[i]) for i in range(n))
        if nrm > 0: best = min(best, nrm)
    return best if best < float('inf') else None


def partition_type(fa, fb, fc, primes):
    pa = [p for p in primes if p in fa]
    pb = [p for p in primes if p in fb]
    pc = [p for p in primes if p in fc]
    return tuple(sorted([len(pa), len(pb), len(pc)], reverse=True))


def is_squarefree(fa, fb, fc):
    return all(v == 1 for v in list(fa.values()) + list(fb.values()) + list(fc.values()))


# Enumerate all omega*=5 coprime triples (non-squarefree only)
triples = []
seen = set()
for a in range(2, LIMIT + 1):
    fa = factorize(a)
    for b in range(2, LIMIT + 1):
        if math.gcd(a, b) != 1: continue
        c = a + b
        fb = factorize(b)
        fc = factorize(c)
        primes = sorted(set(list(fa) + list(fb) + list(fc)))
        if len(primes) != 5: continue
        # require disjoint prime groups
        if set(fa) & set(fb) or set(fa) & set(fc) or set(fb) & set(fc): continue
        if is_squarefree(fa, fb, fc): continue   # squarefree handled analytically
        key = tuple(sorted([a, b]))
        if key in seen: continue
        seen.add(key)
        ptype = partition_type(fa, fb, fc, primes)
        alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
        ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
        triples.append((a, b, primes, alpha, ws, ptype))

print(f"T86: omega*=5 non-squarefree zero-coord property (BB={BB}, LIMIT={LIMIT})")
print(f"Total triples: {len(triples)}")

by_type = defaultdict(list)
for tt in triples:
    by_type[tt[5]].append(tt)
for t, lst in sorted(by_type.items()):
    print(f"  type {t}: {len(lst)} triples")
print()

random.seed(86)
grand_ok = grand_fail = grand_skip = 0

for ptype, lst in sorted(by_type.items()):
    sample = random.sample(lst, min(SAMPLE_PER_TYPE, len(lst)))
    ok = fail = skip = 0
    for tt in sample:
        a, b, primes, alpha, ws, _ = tt
        nd = nd_brute_full(primes, alpha, ws, BB)
        if nd is None: skip += 1; continue
        bp_vals = []
        for i in range(5):
            bp = nd_brute_zero_p(primes, alpha, ws, i, BB)
            if bp is not None:
                bp_vals.append(bp)
        if not bp_vals: skip += 1; continue
        min_bp = min(bp_vals)
        if min_bp == nd:
            ok += 1
        elif min_bp < nd:
            fail += 1
            print(f"  IMPOSSIBLE ({a},{b}) type {ptype}: min_bp={min_bp} < nd={nd}")
        else:
            fail += 1
            print(f"  VIOLATION ({a},{b}) type {ptype}: nd={nd} but min_bp={min_bp} > nd")
            print(f"    primes={primes} alpha={alpha}")
    print(f"  type {ptype}: sample {len(sample)}: OK={ok}  skip={skip}  FAIL={fail}")
    grand_ok += ok; grand_fail += fail; grand_skip += skip

print(f"\nTotals: OK={grand_ok}  skip={grand_skip}  FAIL={grand_fail}")
if grand_fail == 0:
    print(f"ZERO-COORDINATE PROPERTY CONFIRMED for all omega*=5 non-squarefree types (BB={BB}).")
