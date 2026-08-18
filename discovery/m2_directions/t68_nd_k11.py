"""
T68 — Explicit verification of thm:nd_k11 (type (k,1,1) exact formula).

For coprime a+b=c with P_a={p}, P_b={q}, P_c={r}, p<q<r, v_p(a)=k, v_q(b)=v_r(c)=1:
  nd(a,b) = min(r, q*k)

Verification: brute-force enumeration agrees with the formula on named examples.
"""

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


def nd_brute(a, b, bound=15):
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


# Named type (k,1,1) triples: (a, b, c, expected_nd)
# Pa={p^k}, Pb={q^1}, Pc={r^1}, formula: nd = min(r, q*k)
cases = [
    # (a,  b,  c,  p, q,  r, k, nd_formula)
    (4, 3, 7, 2, 3, 7, 2, min(7, 3 * 2)),  # 2^2 + 3 = 7, nd=min(7,6)=6
    (8, 3, 11, 2, 3, 11, 3, min(11, 3 * 3)),  # 2^3 + 3 = 11, nd=min(11,9)=9
    (4, 7, 11, 2, 7, 11, 2, min(11, 7 * 2)),  # 2^2 + 7 = 11, nd=min(11,14)=11
    (16, 3, 19, 2, 3, 19, 4, min(19, 3 * 4)),  # 2^4 + 3 = 19, nd=min(19,12)=12
    (32, 3, 35, 2, 3, 5, 5, None),  # 35=5*7, not type (k,1,1) — skip
    (4, 5, 9, 2, 5, 3, 2, None),  # 9=3^2, not type (k,1,1) — skip
    (8, 5, 13, 2, 5, 13, 3, min(13, 5 * 3)),  # 2^3 + 5 = 13, nd=min(13,15)=13
    (4, 11, 15, 2, 11, 3, 2, None),  # 15=3*5, not single prime — skip
    (9, 2, 11, 3, 2, 11, 2, None),  # p=3>q=2, not p<q — skip
    (9, 4, 13, 3, 2, 13, 2, None),  # p=3>q=2 — skip
    (25, 2, 27, 5, 2, 3, 2, None),  # p=5>q=2 — skip
    # squarefree k=1 examples (nd = min(r,q) = q since q<r)
    (2, 3, 5, 2, 3, 5, 1, min(5, 3 * 1)),  # nd=min(5,3)=3=q
    (2, 5, 7, 2, 5, 7, 1, min(7, 5 * 1)),  # nd=min(7,5)=5=q
    (4, 3, 7, 2, 3, 7, 2, min(7, 6)),  # duplicate: nd=6
]

# Filter to valid type (k,1,1) only
valid_cases = [
    (a, b, c, p, q, r, k, nd_f)
    for (a, b, c, p, q, r, k, nd_f) in cases
    if nd_f is not None
]
# Deduplicate
seen = set()
valid_cases_dedup = []
for row in valid_cases:
    key = (row[0], row[1])
    if key not in seen:
        seen.add(key)
        valid_cases_dedup.append(row)

print("T68: Verification of thm:nd_k11 (type (k,1,1) exact formula)")
print("  nd(a,b) = min(r, q*k)")
print("=" * 65)

all_ok = True
for a, b, c, p, q, r, k, nd_f in valid_cases_dedup:
    nd_b = nd_brute(a, b, bound=15)
    ok = nd_b == nd_f
    if not ok:
        all_ok = False
    regime = "valuation" if nd_f == q * k else "pairwise"
    print(
        f"  ({a},{b},{c}): p={p}^{k}, q={q}, r={r}  "
        f"min({r},{q}*{k})={nd_f}  brute={nd_b}  regime={regime}  "
        f"{'OK' if ok else 'MISMATCH'}"
    )

print()
print(f"Result: {'ALL MATCH — thm:nd_k11 confirmed' if all_ok else 'FAILURES FOUND'}")
print()
print("Crossover observation:")
for a, b, c, p, q, r, k, nd_f in valid_cases_dedup:
    if q * k == r:
        print(f"  ({a},{b},{c}): crossover qk=r={r}")
print("  (crossover triples: both regimes give same nd)")
print()
print("LB-1 check: nd >= p2 = q for all cases:")
lb_ok = True
for a, b, c, p, q, r, k, nd_f in valid_cases_dedup:
    if nd_f < q:
        lb_ok = False
        print(f"  FAIL: ({a},{b},{c}) nd={nd_f} < q={q}")
if lb_ok:
    print("  All satisfy nd >= q = p2 (consistent with thm:nd_lb)")
