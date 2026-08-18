"""
T1 — Quality distribution explorer (discovery tier, UNTRUSTED)

Enumerates coprime triples (a, b, c) with a + b = c up to c < LIMIT
and studies the distribution of quality q = log(c) / log(rad(abc)).

PURPOSE: probe what M2 actually needs to bound.
  - How many triples have q > 1?
  - What is the empirical max quality for small c?
  - How does q_max grow with c_max?

NON-CIRCULARITY: No K_ε is fitted. Known triples are used only for
exploration; none of this output is imported by the construction graph.
"""

import math

LIMIT = 10000


# Sieve to precompute rad(n) for all n up to LIMIT*2
def sieve_rad(N):
    rad_arr = [1] * (N + 1)
    for p in range(2, N + 1):
        if rad_arr[p] == 1:  # p is prime
            for m in range(p, N + 1, p):
                rad_arr[m] *= p
    return rad_arr


rad_arr = sieve_rad(LIMIT * 2)

# Sieve to find coprime pairs quickly: gcd via Euler's totient sieve is complex,
# so we just check gcd for pairs where rad(a*b) = rad(a)*rad(b) (i.e., coprime)
# For speed: use math.gcd which is fast in Python 3.9+


def quality(a, b, c):
    # rad(abc) = rad(a)*rad(b)*rad(c) when gcd(a,b)=1 (since gcd(a,c)=gcd(b,c)=1 follows)
    R = rad_arr[a] * rad_arr[b] // math.gcd(rad_arr[a] * rad_arr[b], 1)
    # Actually for coprime a,b: rad(abc) = lcm(rad(a),rad(b),rad(c))
    # = rad(a)*rad(b)*rad(c) / (common factors)
    # Simplest: rad(a*b*c) via lcm of prime sets
    # Since a+b=c and gcd(a,b)=1, any prime p|a and p|c → p|b, contradiction.
    # So primes of a, b, c are pairwise disjoint: rad(abc) = rad(a)*rad(b)*rad(c)
    # (This only fails if c > LIMIT*2; we check c = a+b ≤ LIMIT*2)
    R = rad_arr[a] * rad_arr[b] * rad_arr[c]
    return math.log(c) / math.log(R), R


print("T1: Quality distribution for coprime triples a+b=c, c ≤ " + str(LIMIT))
print("=" * 60)

# Collect all triples
high_q = []  # q > 1.0
very_high_q = []  # q > 1.2

for a in range(1, LIMIT // 2 + 1):
    for b in range(a, LIMIT - a + 1):
        c = a + b
        if c > LIMIT:
            break
        if math.gcd(a, b) != 1:
            continue
        q, R = quality(a, b, c)
        if q > 1.0:
            high_q.append((a, b, c, q))
        if q > 1.2:
            very_high_q.append((a, b, c, q))

# Sort by quality descending
high_q.sort(key=lambda x: -x[3])
very_high_q.sort(key=lambda x: -x[3])

print(f"\nTriples with q > 1.0: {len(high_q)}")
print(f"Triples with q > 1.2: {len(very_high_q)}")

print(f"\nTop 20 by quality (c ≤ {LIMIT}):")
print(f"{'a':>8} {'b':>8} {'c':>8}  {'R=rad':>12}  {'q':>8}")
print("-" * 55)
for a, b, c, q in high_q[:20]:
    R = rad_arr[a] * rad_arr[b] * rad_arr[c]
    print(f"{a:>8} {b:>8} {c:>8}  {R:>12}  {q:>8.5f}")

# Compute max quality as function of c_max
print("\nEmpirical max quality vs c_max:")
print(f"{'c_max':>8}  {'q_max':>8}  {'triple':>20}")
thresholds = [100, 300, 1000, 3000, 10000]
for thresh in thresholds:
    candidates = [(a, b, c, q) for a, b, c, q in high_q if c <= thresh]
    if candidates:
        best = max(candidates, key=lambda x: x[3])
        print(f"{thresh:>8}  {best[3]:>8.5f}  ({best[0]},{best[1]},{best[2]})")

# Quality histogram
print(f"\nQuality histogram (all triples with q>1, c<{LIMIT}):")
bins = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 2.0, 3.0]
for i in range(len(bins) - 1):
    count = sum(1 for _, _, _, q in high_q if bins[i] <= q < bins[i + 1])
    print(f"  [{bins[i]:.2f}, {bins[i + 1]:.2f}): {count:>5} triples")

print("\nIMPLICATION FOR M2:")
print("  M2 requires: for all ε>0, ∃K_ε: q(a,b,c) ≤ 1+ε for all triples.")
print("  Empirically: q_max appears bounded but grows (slowly) with c_max.")
print("  The PROOF gap: we can observe this but cannot currently bound it universally.")
print("  Best unconditional bound: c < exp(κ·R^{1/3}·(log R)^3) [Stewart-Yu 2001]")
print("  This is far from q ≤ 1+ε.")
