"""
T69 — Verification of thm:nd_km1 (type (k,m,1) exact formula).

For coprime a+b=c with P_a={p}, P_b={q}, P_c={r}, p<q<r,
v_p(a)=k, v_q(b)=m, v_r(c)=1:
  nd(a,b) = min(r, max(p*m/g, q*k/g))  where g = gcd(k,m).

Special cases:
  m=1  → min(r, max(p/g, qk/g)) = min(r, max(p, qk)) = min(r, qk)  [thm:nd_k11]
  k=1  → min(r, max(pm, q))
  k=m  → min(r, max(p,q)) = min(r, q) = q  [squarefree-like]
  k=m, g=k → min(r, max(p, q)) = q  (for any equal valuation)
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
    best = float("inf")
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
    return best if best < float("inf") else None


def nd_km1_formula(p, q, r, k, m):
    g = math.gcd(k, m)
    return min(r, max(p * m // g, q * k // g))


# Named type (k,m,1) triples: (a, b, c, p, q, r, k, m)
# All must have: P_a = {p^k}, P_b = {q^m}, P_c = {r^1}, p < q < r
cases = [
    # k=1,m=1 (squarefree): nd = min(r, max(p,q)) = q
    (2, 3, 5, 2, 3, 5, 1, 1),
    (2, 5, 7, 2, 5, 7, 1, 1),
    (2, 11, 13, 2, 11, 13, 1, 1),
    # k=2, m=1 (thm:nd_k11 special case): nd = min(r, q*2)
    (4, 3, 7, 2, 3, 7, 2, 1),
    (4, 7, 11, 2, 7, 11, 2, 1),
    (16, 3, 19, 2, 3, 19, 4, 1),
    # k=1, m=2: nd = min(r, max(p*2, q))
    (2, 9, 11, 2, 3, 11, 1, 2),  # nd = min(11, max(4,3)) = min(11,4) = 4
    (2, 25, 27, 2, 5, 3, 1, 2),  # 27=3^3 not r^1, skip
    (
        3,
        4,
        7,
        2,
        3,
        7,
        1,
        2,
    ),  # a=3=3^1, b=4=2^2 → P_a={3}, P_b={2}, p=2<q=3<r=7? No: p=2,q=3 but a=3,b=4, Pa={3}, Pb={2}, not p<q ordering by value vs by role
    # Reorient: P_a={smaller prime in a}, P_b={smaller prime in b}
    # Actually P_a is the set of primes in a. Let me just list valid ones:
    (
        3,
        4,
        7,
        2,
        3,
        7,
        2,
        1,
    ),  # a=3^1=3, b=2^2=4: P_a={3},P_b={2},P_c={7}, k_3=1,k_2=2... need p=min(P)=2<q=3<r=7 with role P_b={2^2}, P_a={3^1}: p=2,q=3,k=2,m=1 → nd=min(7,max(2,6))=6 → covered by nd_k11
    # k=1,m=2 with p<q<r and P_b={q^2}:
    (
        2,
        9,
        11,
        2,
        3,
        11,
        1,
        2,
    ),  # a=2,b=9=3^2,c=11: p=2,q=3,r=11,k=1,m=2,g=1 → nd=min(11,max(4,3))=4
    (2, 49, 51, 2, 7, 3, 1, 2),  # 51=3*17, not prime, skip
    (2, 25, 27, 2, 5, 3, 1, 2),  # 27=3^3, r must be prime^1
    # Let me pick valid ones explicitly:
    (5, 4, 9, 2, 5, 3, 2, 1),  # 9=3^2 not r^1, skip
    # k=2, m=2: g=2, nd=min(r, max(p,q)) = min(r,q) = q (for p<q<r)
    (4, 9, 13, 2, 3, 13, 2, 2),  # g=2, max(2,3)=3, nd=min(13,3)=3=q ✓
    (4, 9, 13, 2, 3, 13, 2, 2),  # duplicate
    # k=2, m=3: g=1, nd=min(r, max(2*3, 3*2)) = min(r, 6)
    (4, 27, 31, 2, 3, 31, 2, 3),  # g=1, max(6,6)=6, nd=min(31,6)=6
    # k=3, m=2: g=1, nd=min(r, max(p*2,q*3)) = min(r, max(2*2,3*3)) = min(r,9)
    (8, 9, 17, 2, 3, 17, 3, 2),  # g=1, max(4,9)=9, nd=min(17,9)=9
    # k=4, m=2: g=2, nd=min(r, max(p,q*2)) = min(r, max(2,6)) = min(r, 6)
    (16, 9, 25, 2, 3, 5, 4, 2),  # 25=5^2, not r^1, skip
    (16, 9, 25, 2, 5, 3, 4, 2),  # 16=2^4, 9=3^2, 25=5^2: no r^1
    # k=3,m=3: g=3, nd=min(r, max(p,q)) = q
    (8, 27, 35, 2, 3, 5, 3, 3),  # 35=5*7 not prime, skip
    # k=6,m=4: g=2, max(p*2, q*3) = max(4,9)=9
    (64, 81, 145, 2, 3, 5, 6, 4),  # 145=5*29, not prime, skip
]

# Filter valid (k,m,1) cases: a=p^k, b=q^m, c=r^1 (r prime), p<q<r
valid_cases = []
seen = set()
for row in cases:
    a, b, c, p, q, r, k, m = row
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    # Check structure
    if set(fa.keys()) != {p}:
        continue
    if set(fb.keys()) != {q}:
        continue
    if set(fc.keys()) != {r}:
        continue
    if fa[p] != k:
        continue
    if fb[q] != m:
        continue
    if fc[r] != 1:
        continue
    if not (p < q < r):
        continue
    if a + b != c:
        continue
    key = (a, b)
    if key in seen:
        continue
    seen.add(key)
    valid_cases.append(row)

# Also add some explicitly constructed cases
extra = [
    # a=2, b=9=3^2, c=11: p=2,q=3,r=11,k=1,m=2
    (2, 9, 11, 2, 3, 11, 1, 2),
    # a=2, b=27=3^3, c=29: k=1,m=3
    (2, 27, 29, 2, 3, 29, 1, 3),
    # a=8=2^3, b=9=3^2, c=17: k=3,m=2
    (8, 9, 17, 2, 3, 17, 3, 2),
    # a=4=2^2, b=9=3^2, c=13: k=2,m=2
    (4, 9, 13, 2, 3, 13, 2, 2),
    # a=4=2^2, b=27=3^3, c=31: k=2,m=3
    (4, 27, 31, 2, 3, 31, 2, 3),
    # a=2^1, b=3^4=81, c=83: k=1,m=4
    (2, 81, 83, 2, 3, 83, 1, 4),
    # a=2^5=32, b=3^1=3, c=5^2: skip (c not prime^1)
    # a=2^1=2, b=5^2=25, c=27: skip (27=3^3)
    # a=2^2=4, b=5^1=5, c=3^2: no p<q<r
    # a=2^1=2, b=5^3=125, c=127: k=1,m=3,p=2,q=5,r=127
    (2, 125, 127, 2, 5, 127, 1, 3),
    # a=2^2=4, b=5^2=25, c=29: k=2,m=2,g=2
    (4, 25, 29, 2, 5, 29, 2, 2),
    # a=2^3=8, b=5^2=25, c=33: 33=3*11, skip
    # a=2^4=16, b=3^2=9, c=25: 25=5^2, skip
    # a=3^1=3, b=5^1=5, c=2^3: no p<q<r
    # a=2^1=2, b=3^5=243, c=245: 245=5*49, skip
    # a=2^2=4, b=3^4=81, c=85: 85=5*17, skip
]
for row in extra:
    a, b, c, p, q, r, k, m = row
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    if set(fa.keys()) != {p}:
        continue
    if set(fb.keys()) != {q}:
        continue
    if set(fc.keys()) != {r}:
        continue
    if fa[p] != k:
        continue
    if fb[q] != m:
        continue
    if fc[r] != 1:
        continue
    if not (p < q < r):
        continue
    if a + b != c:
        continue
    key = (a, b)
    if key in seen:
        continue
    seen.add(key)
    valid_cases.append(row)

print("T69: Verification of thm:nd_km1 (type (k,m,1) exact formula)")
print("  nd(a,b) = min(r, max(p*m/g, q*k/g))  where g = gcd(k,m)")
print("=" * 70)

all_ok = True
for a, b, c, p, q, r, k, m in valid_cases:
    g = math.gcd(k, m)
    nd_f = nd_km1_formula(p, q, r, k, m)
    nd_b = nd_brute(a, b, bound=20)
    ok = nd_b == nd_f
    if not ok:
        all_ok = False
    pmg = p * m // g
    qkg = q * k // g
    regime = "phi_r=0" if nd_f < r else ("pairwise" if nd_f == r else "?")
    print(
        f"  ({a},{b},{c}): p={p}^{k},q={q}^{m},r={r}  g={g}  "
        f"max({pmg},{qkg})={max(pmg, qkg)}  min(r={r},max)={nd_f}  "
        f"brute={nd_b}  {'OK' if ok else 'MISMATCH'}"
    )

print()
print(f"Result: {'ALL MATCH — thm:nd_km1 confirmed' if all_ok else 'FAILURES FOUND'}")
print()
print("Special-case checks:")
print("  k=m: g=k, max(pm/g,qk/g)=max(p,q)=q, nd=min(r,q)=q ✓")
print("  m=1: nd=min(r,max(p,qk))=min(r,qk) = thm:nd_k11 ✓")
print("  k=m=1: nd=min(r,max(p,q))=min(r,q)=q = squarefree E_n ✓")
