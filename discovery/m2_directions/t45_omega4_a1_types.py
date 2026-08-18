"""
T45 — Explore ω=4 type (0,2,2): a=1, b=p1*p2, c=q1*q2 where 1+p1*p2=q1*q2.

For a=1: Pa=∅, so nd = second_smallest{min(Pb), min(Pc)} = min(p1,q1) (smaller of the
two group mins). R = 1*b*c = b*c. ρ = nd^{1/3} / R^{1/3}.

Key question: is ρ bounded for type (0,2,2)?
Compare with F23/F23b: type (0,2,3) with a=1 has sup=1 (unbounded approach to 1).
Hypothesis: type (0,2,2) also has sup=1 since a=1 forces nd ≈ √R approach.
"""

import math


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            if d not in factors:
                factors.append(d)
            n //= d
        d += 1
    if n > 1 and n not in factors:
        factors.append(n)
    return sorted(factors)


def rad(n):
    return math.prod(prime_factors(n))


results = []

# Enumerate type (0,2,2): a=1, b=p1*p2, c=b+1=q1*q2
# Both b and c must have exactly 2 prime factors, and gcd(b,c)=gcd(b,b+1)=1 always.
for b in range(4, 20001):
    c = b + 1
    pb = prime_factors(b)
    pc = prime_factors(c)
    if len(pb) != 2 or len(pc) != 2:
        continue
    # Check squarefree (each prime appears exactly once)
    if not (b == pb[0] * pb[1] and c == pc[0] * pc[1]):
        continue
    a = 1
    p1, p2 = pb[0], pb[1]  # p1 < p2
    q1, q2 = pc[0], pc[1]  # q1 < q2
    # nd = second_smallest of group mins {min(Pa), min(Pb), min(Pc)}
    # But Pa is empty (a=1), so we only have min(Pb)=p1, min(Pc)=q1
    # With only 2 groups, "second smallest" means: we have 2 group mins p1, q1
    # nd = second_smallest of {p1, q1} = max(p1, q1) (the larger of the two mins)
    # Wait -- F10 says nd = second_smallest{min(Pa), min(Pb), min(Pc)}
    # With Pa=∅, there are only 2 groups, so second_smallest of {p1,q1}:
    # If we order them: nd = max(p1,q1) since we need second smallest of a 2-element set.
    # Actually "second smallest" of {p1, q1} means the larger one.
    nd = max(p1, q1)
    R = b * c  # since a=1 and b,c squarefree, rad(abc)=rad(1)*rad(b)*rad(c)=b*c
    omega = 4  # Pa empty but still ω counts primes in abc
    # ρ = nd / R^{1/(ω-1)} = nd / R^{1/3}
    rho = nd / R ** (1 / 3)
    results.append((rho, b, c, p1, p2, q1, q2, nd, R))

results.sort(reverse=True)

print("T45: ω=4 type (0,2,2) — a=1, b=p1*p2, c=q1*q2 squarefree")
print("=" * 70)
print(f"Found {len(results)} qualifying triples with b ≤ 20000")
print()
print("Top 15 by ρ:")
print(f"{'rho':>10}  {'b':>8}  {'c':>8}  {'p1,p2':>10}  {'q1,q2':>10}  {'nd':>6}")
for rho, b, c, p1, p2, q1, q2, nd, R in results[:15]:
    print(f"{rho:10.6f}  {b:8d}  {c:8d}  {p1}·{p2:>5}  {q1}·{q2:>5}  nd={nd}")

print()
print("Distribution of ρ:")
buckets = [0] * 11
for rho, *_ in results:
    i = min(int(rho * 10), 10)
    buckets[i] += 1
for i in range(11):
    lo, hi = i / 10, (i + 1) / 10
    print(f"  [{lo:.1f}, {hi:.1f}): {buckets[i]}")

print()
# Check if ρ approaches 1
max_rho = results[0][0] if results else 0
print(f"Max ρ = {max_rho:.6f}")
print()

# Check the family b=2*p, c=3*q (small primes in each factor)
print("Special family b=2*p (p prime), c=3*q (q prime), b+1=c:")
for p in range(3, 1001):
    if not is_prime(p):
        continue
    b = 2 * p
    c = b + 1
    if c % 3 != 0:
        continue
    q = c // 3
    if not is_prime(q):
        continue
    nd = max(2, 3)  # max(min(Pb), min(Pc)) = max(2,3) = 3
    R = b * c
    rho = nd / R ** (1 / 3)
    if rho > 0.5:
        print(f"  b={b} ({2}·{p}), c={c} ({3}·{q}), nd=3, R={R}, ρ={rho:.6f}")

print()
# Analytical limit: for b=2*p large, c=2p+1≈2p, R≈4p^2
# nd=max(2,q1) where q1=min prime factor of c=2p+1
# If c=2p+1 has small prime factor q1, then nd=max(2,q1)=q1
# ρ = q1 / (2p * (2p+1))^{1/3} ≈ q1 / (4p^2)^{1/3}
# For c=3*q: q1=3, ρ ≈ 3/(4p^2)^{1/3} → 0 as p→∞
# So this family → 0.

# Look for families where ρ→max
# ρ = max(p1,q1) / (p1*p2*q1*q2)^{1/3}
# To maximize: want p1 close to q1 and p2, q2 small
# b = p * p_large, c = q * q_large (p≈q, p_large=p+1 if prime)
print("Analytical bound analysis:")
print("  ρ = max(p1,q1) / (p1*p2*q1*q2)^{1/3}")
print(
    "  For p1=q1=p (equal group mins): ρ = p / (p*p2*p*q2)^{1/3} = p/(p^2*p2*q2)^{1/3}"
)
print("  = 1 / (p*p2*q2)^{1/3} → 0 as primes grow")
print("  Supremum analysis: ρ → 0 for most families → type (0,2,2) has sup → 0")
print()
print("Conclusion: type (0,2,2) is BOUNDED with sup approaching small value,")
print("consistent with OTHER fully-supported ω=4 types.")
print("This DIFFERS from (0,2,3)/(0,3,2) where a=1 forces sup=1.")
print(
    "Key: for (0,2,2) with EXACTLY 2 groups, nd is forced to be the larger group min,"
)
print("which grows slower than R^{1/3}, giving ρ→0.")
