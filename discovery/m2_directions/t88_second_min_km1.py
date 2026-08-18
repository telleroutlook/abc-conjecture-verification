"""
T88 — Probe second successive minimum for type (k,m,1) triples.

For type (k,m,1): Pa={p^k}, Pb={q^m}, Pc={r}, p<q<r.
Constraint: k*phi_p + m*phi_q = phi_r.
thm:nd_km1: nd = min(r, max(p*m/g, q*k/g)) where g=gcd(k,m).

Goal: find lambda2 empirically and discover the formula.
Focus on pairwise regime: nd = r (i.e., max(pm/g, qk/g) >= r).
"""

import math
from collections import defaultdict


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def nd_and_lambda2_brute(p, q, r, k, m, bound):
    norms = set()
    for xp in range(-bound, bound + 1):
        for xq in range(-bound, bound + 1):
            xr = k * xp + m * xq
            if abs(xr) > bound:
                continue
            if xp == 0 and xq == 0 and xr == 0:
                continue
            # Non-degeneracy: W = phi_q - phi_p != 0 (b-side minus a-side)
            if xq - xp == 0:
                continue
            nrm = max(p * abs(xp), q * abs(xq), r * abs(xr))
            if nrm > 0:
                norms.add(nrm)
    if not norms:
        return None, None
    sn = sorted(norms)
    return sn[0], (sn[1] if len(sn) > 1 else None)


def formula_nd(p, q, r, k, m):
    g = math.gcd(k, m)
    n0 = max(p * (m // g), q * (k // g))
    return min(r, n0)


# Enumerate type (k,m,1) triples
primes = [2, 3, 5, 7, 11, 13]
triples = []
for p in primes:
    for q in primes:
        if q <= p:
            continue
        for k in range(2, 8):
            for m in range(2, 8):
                a = p**k
                b = q**m
                if a > 600 or b > 600:
                    continue
                c = a + b
                if not is_prime(c):
                    continue
                r = c
                if r <= q:
                    continue
                g = math.gcd(k, m)
                n0 = max(p * (m // g), q * (k // g))
                nd_f = min(r, n0)
                regime = "pair" if n0 >= r else "val"
                triples.append((p, q, r, k, m, g, n0, nd_f, regime))

print(f"T88: Second min for type (k,m,1) — {len(triples)} triples")

by_regime = defaultdict(list)
for t in triples:
    by_regime[t[8]].append(t)
for reg, lst in sorted(by_regime.items()):
    print(f"  regime {reg}: {len(lst)} triples")
print()

nd_fail = 0
results = []

for p, q, r, k, m, g, n0, nd_f, regime in triples:
    kp = k // g
    mp = m // g
    bb = max(6, n0 // p + 3, 2 * r // q + 3)
    nd_b, l2_b = nd_and_lambda2_brute(p, q, r, k, m, bb)
    if nd_b is None:
        continue
    if nd_b != nd_f:
        nd_fail += 1
        print(f"  ND-FAIL ({p}^{k},{q}^{m},{r}) g={g}: f={nd_f} b={nd_b}")
        continue
    if l2_b is None:
        continue
    results.append((p, q, r, k, m, g, kp, mp, n0, nd_f, l2_b, regime))

print(f"nd failures: {nd_fail}")
print(f"Usable results: {len(results)}")
print()

# Analyze: for pairwise regime, what is l2?
# Candidates: 2r, n0, q*(k'-1) if>r, p*(m'-1) if>r, combinations
print("=== PAIRWISE regime analysis ===")
pair_results = [r for r in results if r[-1] == "pair"]
print(f"Count: {len(pair_results)}")
print()

# For each result, compute candidate formulas and see which matches
match_stats = defaultdict(int)
for p, q, r, k, m, g, kp, mp, n0, nd, l2, reg in pair_results:
    # Candidates
    c1 = 2 * r  # scale phi_r=1 vector
    c2 = n0  # phi_r=0 branch (always >= r in pairwise)
    c3 = q * (kp - 1) if kp > 1 and q * (kp - 1) > r else None
    c4 = p * (mp - 1) if mp > 1 and p * (mp - 1) > r else None
    c5 = p * mp + q * kp  # sum bound
    c6 = max(p * mp, q * kp)  # same as n0 = max(p*m/g, q*k/g)

    # Build candidate formula: min of all > r candidates
    cands = [c for c in [c1, c2, c3, c4] if c is not None and c > r]
    if not cands:
        match_stats["no_cands"] += 1
        continue
    formula_val = min(cands)

    if formula_val == l2:
        match_stats["MATCH"] += 1
    else:
        match_stats["MISMATCH"] += 1
        print(
            f"  MISMATCH ({p}^{k},{q}^{m},{r}) g={g} k'={kp} m'={mp} "
            f"n0={n0} nd={nd} l2={l2}: formula={formula_val}"
        )
        print(f"    cands={cands} | c1={c1} c2={c2} c3={c3} c4={c4}")

print(f"\nPairwise: MATCH={match_stats['MATCH']} MISMATCH={match_stats['MISMATCH']}")
print()

print("=== VALUATION regime analysis ===")
val_results = [r for r in results if r[-1] == "val"]
print(f"Count: {len(val_results)}")

val_match = val_miss = 0
for p, q, r, k, m, g, kp, mp, n0, nd, l2, reg in val_results:
    # In valuation regime nd=n0, analogous to F34 valuation:
    # candidate: min(r, 2*n0)
    c1 = r
    c2 = 2 * n0
    formula_val = min(c for c in [c1, c2] if c > n0)
    if not formula_val:
        continue
    if formula_val == l2:
        val_match += 1
    else:
        val_miss += 1
        print(
            f"  VAL-MISS ({p}^{k},{q}^{m},{r}) g={g} n0={n0} nd={n0} "
            f"l2={l2}: formula=min(r,2n0)={formula_val}"
        )

print(f"\nValuation: MATCH={val_match} MISMATCH={val_miss}")
print()

# Print sample table for visual inspection
print("=== Sample (pairwise, first 15) ===")
print(
    f"{'triple':20s} {'g':>3} {'k,m':>7} {'nd':>5} {'n0':>5} {'l2':>6} {'winner':15s}"
)
for p, q, r, k, m, g, kp, mp, n0, nd, l2, reg in pair_results[:15]:
    c1, c2 = 2 * r, n0
    c3 = q * (kp - 1) if kp > 1 and q * (kp - 1) > r else None
    c4 = p * (mp - 1) if mp > 1 and p * (mp - 1) > r else None
    cands = {f"2r={c1}": c1, f"n0={c2}": c2}
    if c3:
        cands[f"qk'1={c3}"] = c3
    if c4:
        cands[f"pm'1={c4}"] = c4
    winner = min(cands, key=lambda x: cands[x] if cands[x] > r else float("inf"))
    print(
        f"({p}^{k},{q}^{m},{r:3d})      {g:>3} {k},{m:>5}  {nd:>5} {n0:>5} {l2:>6}  {winner}"
    )
