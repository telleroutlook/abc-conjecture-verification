"""
T74 — Exact nd discovery for type (2,1,1) triples. FAST VERSION.

a = p^k1 * q^k2 (exactly 2 distinct primes in Pa), b = r^m, c = s^n (prime powers).
Uses precomputed sets and smaller range.
"""

import math
from itertools import product as iproduct
from collections import defaultdict

LIMIT = 300

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def nd_brute(a, b, bound=15):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ < 3 or np_ > 5: return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound+1), repeat=np_):
        if all(c2 == 0 for c2 in coords): continue
        if sum(alpha[i]*coords[i] for i in range(np_)) != 0: continue
        W = sum(ws[i]*coords[i] for i in range(np_))
        if W == 0: continue
        norm = max(primes[i]*abs(coords[i]) for i in range(np_))
        if norm > 0: best = min(best, norm)
    return best if best < float('inf') else None

def within_group_norm(k1, k2, p, q):
    g = math.gcd(k1, k2)
    return max(p * (k2 // g), q * (k1 // g))

# Precompute: numbers with exactly 2 prime factors up to LIMIT
two_prime = {}  # n -> (p, q, k1, k2) with p < q
prime_powers = {}  # n -> (p, k) prime powers

for n in range(2, LIMIT+1):
    f = factorize(n)
    if len(f) == 2:
        ps = sorted(f.keys())
        two_prime[n] = (ps[0], ps[1], f[ps[0]], f[ps[1]])
    elif len(f) == 1:
        p = list(f.keys())[0]
        prime_powers[n] = (p, f[p])

print(f"T74: type (2,1,1) nd discovery (range ≤ {LIMIT})")
print(f"  Two-prime numbers: {len(two_prime)},  Prime powers: {len(prime_powers)}")
print("=" * 80)

# Collect type (2,1,1) triples
triples = []
seen = set()

for a, (p, q, k1, k2) in two_prime.items():
    for b, (r, m) in prime_powers.items():
        if r in (p, q): continue
        if b >= a + LIMIT: continue
        c = a + b
        if c > 2 * LIMIT: continue
        if c not in prime_powers: continue
        s, nv = prime_powers[c]
        if s in (p, q, r): continue
        if math.gcd(a, b) != 1: continue
        key = (a, b)
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k1, k2, m, nv))

print(f"Found {len(triples)} type (2,1,1) triples")
print()

# Analyze each triple
print(f"{'(a,b)':12s} {'decomp':18s} {'nd':4s} {'Wab':4s} {'nd vs Wab':10s} {'ratio':6s}")
print("-" * 60)

stats = defaultdict(int)
cases = []

for (a, b, p, q, r, s, k1, k2, m, nv) in triples:
    nd = nd_brute(a, b, bound=12)
    if nd is None: continue

    W_ab = within_group_norm(k1, k2, p, q)
    g = math.gcd(k1, k2)

    if nd < W_ab:
        rel = f"nd<Wab"
        stats['nd<Wab'] += 1
    elif nd == W_ab:
        rel = f"nd=Wab"
        stats['nd=Wab'] += 1
    else:
        rel = f"nd>Wab"
        stats['nd>Wab'] += 1

    ratio = nd / W_ab if W_ab > 0 else float('inf')
    cases.append((a, b, p, q, r, s, k1, k2, m, nv, nd, W_ab, g, ratio))
    print(f"  ({a:3d},{b:3d})   {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}   nd={nd:3d}  Wab={W_ab:3d}  {rel}  {ratio:.3f}")

print()
print("=" * 80)
print(f"Total: {len(cases)}, nd<Wab: {stats['nd<Wab']}, nd=Wab: {stats['nd=Wab']}, nd>Wab: {stats['nd>Wab']}")

print()
print("=== Cases where nd < W_ab (pure cross-group wins) ===")
for (a, b, p, q, r, s, k1, k2, m, nv, nd, W_ab, g, ratio) in cases:
    if nd < W_ab:
        print(f"  ({a},{b}) {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}  nd={nd} < Wab={W_ab}")
        # Check what the cross-group structure gives
        # Simplest cross-group: treat as one-prime-per-group variants
        # Val-regime: phi_s=0 → constraint k1*phi_p + k2*phi_q + m*phi_r = 0
        #   Within Pa: gcd(k1,k2) structure. Cross between Pa and Pb:
        # The key observation: if gcd(k1,m) or gcd(k2,m) divides r or s, smaller norm possible
        N_s0_approx = "?"
        # Try: treat (p^k1, r^m) as ω*=2 problem: nd_ω2 = max(p*m/gcd(k1,m), r*k1/gcd(k1,m))
        g1m = math.gcd(k1, m); nd_pair_1 = max(p*m//g1m, r*k1//g1m)
        g2m = math.gcd(k2, m); nd_pair_2 = max(q*m//g2m, r*k2//g2m)
        # Also (p^k1, s^n) pair:
        g1n = math.gcd(k1, nv); nd_pair_3 = max(p*nv//g1n, s*k1//g1n)
        g2n = math.gcd(k2, nv); nd_pair_4 = max(q*nv//g2n, s*k2//g2n)
        # Also (r^m, s^n) pair:
        gmn = math.gcd(m, nv); nd_pair_5 = max(r*nv//gmn, s*m//gmn)
        print(f"    pairwise norms: ({p},{r})={nd_pair_1}, ({q},{r})={nd_pair_2}, "
              f"({p},{s})={nd_pair_3}, ({q},{s})={nd_pair_4}, ({r},{s})={nd_pair_5}")
        print(f"    min_pairwise = {min(nd_pair_1,nd_pair_2,nd_pair_3,nd_pair_4,nd_pair_5)}, nd={nd}")

print()
print("=== Formula candidate: nd = min(W_ab, min_pairwise_cross) ===")
formula_ok = 0; formula_fail = 0
for (a, b, p, q, r, s, k1, k2, m, nv, nd, W_ab, g, ratio) in cases:
    g1m = math.gcd(k1, m); g2m = math.gcd(k2, m)
    g1n = math.gcd(k1, nv); g2n = math.gcd(k2, nv); gmn = math.gcd(m, nv)
    nd_1 = max(p*m//g1m, r*k1//g1m); nd_2 = max(q*m//g2m, r*k2//g2m)
    nd_3 = max(p*nv//g1n, s*k1//g1n); nd_4 = max(q*nv//g2n, s*k2//g2n)
    nd_5 = max(r*nv//gmn, s*m//gmn)
    formula = min(W_ab, nd_1, nd_2, nd_3, nd_4, nd_5)
    if formula == nd:
        formula_ok += 1
    else:
        formula_fail += 1
        print(f"  FAIL: ({a},{b}) nd={nd} formula={formula} "
              f"[Wab={W_ab}, nd_1={nd_1}, nd_2={nd_2}, nd_3={nd_3}, nd_4={nd_4}, nd_5={nd_5}]")

print(f"Formula nd=min(W_ab, min_pairwise): {formula_ok} OK, {formula_fail} FAIL")

# What IS the correct formula?
# The formula should be: nd = min over ALL pairs of primes (zeroing the others)
# For 4 primes {p,q,r,s} with constraint k1*phi_p + k2*phi_q + m*phi_r = n*phi_s:
# The minimum is over ALL witness families, not just 2-prime pairs.

# Let's look at the actual winning witnesses for nd < W_ab cases
print()
print("=== Actual winning witnesses for nd < W_ab cases ===")
for (a, b, p, q, r, s, k1, k2, m, nv, nd, W_ab, g, ratio) in cases:
    if nd < W_ab:
        c = a + b
        fa, fb, fc = factorize(a), factorize(b), factorize(c)
        primes_list = sorted(set(list(fa) + list(fb) + list(fc)))
        alpha = [fa.get(pp, fb.get(pp, -fc.get(pp, 0))) for pp in primes_list]
        ws = [1 if pp in fb else (-1 if pp in fa else 0) for pp in primes_list]
        np_ = len(primes_list)
        bound = 12
        for coords in iproduct(range(-bound, bound+1), repeat=np_):
            if all(c2 == 0 for c2 in coords): continue
            if sum(alpha[i]*coords[i] for i in range(np_)) != 0: continue
            W = sum(ws[i]*coords[i] for i in range(np_))
            if W == 0: continue
            norm = max(primes_list[i]*abs(coords[i]) for i in range(np_))
            if norm == nd:
                print(f"  ({a},{b}) nd={nd}: phi={dict(zip(primes_list,coords))} W={W}")
                break
