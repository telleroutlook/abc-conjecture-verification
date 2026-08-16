"""
T70 — Explore type (k,m,n) one-prime-per-group formula.

Conjecture: nd(a,b) = min(N0, N1, N2) where
  N0 = max(p_a*m/g_km, p_b*k/g_km)  [phi_c=0 branch, g_km=gcd(k,m)]
  N1 = max(p_b*n/g_mn, p_c*m/g_mn)  [phi_a=0 branch, g_mn=gcd(m,n)]
  N2 = max(p_a*n/g_kn, p_c*k/g_kn)  [phi_b=0 branch, g_kn=gcd(k,n)]

This generalises thm:nd_km1 (n=1: N1=max(p_b,p_c*m)>=p_c>N0, N2=max(p_a,p_c*k)>=p_c>N0,
so min=N0=max(pm/g_km, qk/g_km)).
"""

import math
from itertools import product as iproduct

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

def nd_brute(a, b, bound=20):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2 or n > 4:
        return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound + 1), repeat=n):
        if all(c == 0 for c in coords):
            continue
        if sum(alpha[i] * coords[i] for i in range(n)) != 0:
            continue
        W = sum(ws[i] * coords[i] for i in range(n))
        if W == 0:
            continue
        norm = max(primes[i] * abs(coords[i]) for i in range(n))
        if norm > 0:
            best = min(best, norm)
    return best if best < float('inf') else None

def nd_kmn_formula(pa, pb, pc, k, m, n):
    g_km = math.gcd(k, m)
    g_mn = math.gcd(m, n)
    g_kn = math.gcd(k, n)
    N0 = max(pa * m // g_km, pb * k // g_km)  # phi_c=0
    N1 = max(pb * n // g_mn, pc * m // g_mn)  # phi_a=0
    N2 = max(pa * n // g_kn, pc * k // g_kn)  # phi_b=0
    return min(N0, N1, N2), N0, N1, N2

# Triples with one prime per group, n>1
# (a, b, c, pa, pb, pc, k, m, n)
cases = [
    # n=2
    (2,  9,  11, 2, 3, 11, 1, 2, 1),   # covered by km1, n=1
    (4,  5,   9, 2, 5,  3, 2, 1, 2),   # a=4=2^2,b=5,c=9=3^2
    (7,  2,   9, 7, 2,  3, 1, 1, 2),   # a=7,b=2,c=9=3^2
    (4, 21,  25, 2, 7,  5, 2, 1, 2),   # 21=3*7 not single prime, skip
    (4, 45,  49, 2, 3,  7, 2, 2, 2),   # 45=9*5, skip
    (2, 47,  49, 2, 47, 7, 1, 1, 2),   # a=2,b=47,c=49=7^2
    (16, 9,  25, 2, 3,  5, 4, 2, 2),   # a=16=2^4, b=9=3^2, c=25=5^2
    (32, 4,  36, 2, 2,  3, 5, 2, 2),   # 32+4=36: same prime 2, skip
    (25, 4,  29, 5, 2, 29, 2, 2, 1),   # a=25=5^2,b=4=2^2,c=29: n=1 covered
    (4,  5,   9, 2, 5,  3, 2, 1, 2),   # pa=2,pb=5,pc=3 but pa<pb but pc<pb (not monotone)
    # n=3
    (2,  5,   7, 2, 5,  7, 1, 1, 1),   # squarefree
    (8,  19,  27, 2, 19, 3, 3, 1, 3),  # a=8=2^3, b=19, c=27=3^3
    (4,  23,  27, 2, 23, 3, 2, 1, 3),  # a=4=2^2, b=23, c=27=3^3
    (2,  125, 127, 2, 5, 127, 1, 3, 1), # covered km1
    # n=2, all-three-nonzero test
    (4,  5,   9, 2, 5,  3, 2, 1, 2),   # again
]

# Filter valid one-prime-per-group cases
valid = []
seen = set()
for row in cases:
    a, b, c_exp, pa, pb, pc, k, m, n = row
    c = a + b
    if c != c_exp:
        continue
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    if set(fa.keys()) != {pa}: continue
    if set(fb.keys()) != {pb}: continue
    if set(fc.keys()) != {pc}: continue
    if fa[pa] != k: continue
    if fb[pb] != m: continue
    if fc[pc] != n: continue
    key = (a, b)
    if key in seen: continue
    seen.add(key)
    valid.append(row)

# Also add some constructed cases
extra_search = []
# Systematic: find triples a+b=c, one prime per group, n>=2
for a in range(2, 200):
    fa = factorize(a)
    if len(fa) != 1: continue
    pa = list(fa.keys())[0]; k = fa[pa]
    for b in range(1, 200):
        fb = factorize(b)
        if len(fb) != 1: continue
        pb = list(fb.keys())[0]; m = fb[pb]
        if pb == pa: continue
        c = a + b
        fc = factorize(c)
        if len(fc) != 1: continue
        pc = list(fc.keys())[0]; n_val = fc[pc]
        if pc == pa or pc == pb: continue
        if n_val < 2: continue  # only interested in n>=2 cases
        key = (min(a,b), max(a,b))
        if key in seen: continue
        seen.add(key)
        extra_search.append((a, b, c, pa, pb, pc, k, m, n_val))
        if len(extra_search) >= 20: break
    if len(extra_search) >= 20: break

all_cases = valid + extra_search

print("T70: Exploration of type (k,m,n) one-prime-per-group formula")
print("  Conj: nd = min(N0, N1, N2) = min(phi_c=0, phi_a=0, phi_b=0) pure witnesses")
print("=" * 75)

ok_count = 0
fail_count = 0
for row in all_cases:
    a, b, c, pa, pb, pc, k, m, n_val = row
    nd_f, N0, N1, N2 = nd_kmn_formula(pa, pb, pc, k, m, n_val)
    nd_b = nd_brute(a, b, bound=20)
    if nd_b is None:
        continue
    ok = (nd_b == nd_f)
    if ok:
        ok_count += 1
    else:
        fail_count += 1
    winning = "N0" if nd_f == N0 else ("N1" if nd_f == N1 else "N2")
    status = "OK" if ok else f"FAIL(brute={nd_b})"
    print(f"  ({a},{b},{c}): k={k},m={m},n={n_val}  "
          f"N0={N0},N1={N1},N2={N2}  conj={nd_f}[{winning}]  {status}")

print()
print(f"Result: {ok_count} OK, {fail_count} FAIL")
if fail_count == 0:
    print("Conjecture holds on all tested cases.")
else:
    print("COUNTEREXAMPLES FOUND — conjecture needs refinement.")
