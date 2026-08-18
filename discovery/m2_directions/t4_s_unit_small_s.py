"""
T4 — S-unit small-S exhaustive enumeration (discovery tier)

For a fixed finite set of primes S, all coprime S-unit solutions to a+b=c
(where a, b, c are S-smooth, i.e., all prime factors in S) are finite
by the S-unit theorem. This toy exhaustively finds all solutions for
small S and checks the quality bound.

PURPOSE:
  - See concretely that solutions are finite (S-unit theorem at work)
  - Measure quality in the finite case: does q ≤ 1+ε hold here?
  - Understand why the S-unit proof (Baker) gives exp(R^{1/3}), not R^{1+ε}

For S = {p_1, ..., p_k}, S-smooth numbers up to bound B are enumerated.
Coprime pairs (a, b) are found with a + b = c where a, b, c all S-smooth.

NON-CIRCULARITY: This is finite enumeration, no fitting of any parameter.
The results are sanity checks only.
"""

import math
from functools import reduce


def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def rad(n):
    return reduce(lambda x, p: x * p, factorize(n).keys(), 1)


def is_S_smooth(n, S):
    """Check if all prime factors of n are in S."""
    if n <= 0:
        return False
    m = n
    for p in S:
        while m % p == 0:
            m //= p
    return m == 1


def generate_S_smooth(S, bound):
    """Generate all S-smooth positive integers up to bound."""
    result = {1}
    for p in S:
        new = set()
        for x in result:
            pk = x
            while pk <= bound:
                new.add(pk)
                pk *= p
        result |= new
    return sorted(result)


def quality(a, b, c):
    R = rad(a * b * c)
    return math.log(c) / math.log(R), R


PRIME_SETS = [
    {2},
    {2, 3},
    {2, 3, 5},
    {2, 3, 5, 7},
    {2, 3, 7},
]

BOUND = 10**8  # search up to this bound for S-smooth numbers

print("T4: S-unit exhaustive enumeration for small S")
print("=" * 60)

for S in PRIME_SETS:
    S_sorted = sorted(S)
    smooth = generate_S_smooth(S, BOUND)
    smooth_set = set(smooth)

    print(f"\nS = {S_sorted},  |S-smooth ≤ {BOUND}| = {len(smooth)}")

    # Find all coprime triples a + b = c with a ≤ b, all S-smooth
    triples = []
    for a in smooth:
        if a > BOUND // 2:
            break
        for b in smooth:
            if b < a:
                continue
            c = a + b
            if c > BOUND:
                break
            if c not in smooth_set:
                continue
            if math.gcd(a, b) != 1:
                continue
            q, R = quality(a, b, c)
            triples.append((a, b, c, q, R))

    triples.sort(key=lambda x: -x[3])
    print(f"  Coprime triples a+b=c (a≤b), all S-smooth: {len(triples)}")

    if triples:
        print("  Top 5 by quality:")
        print(f"  {'a':>10} {'b':>10} {'c':>10}  {'R':>8}  {'q':>8}")
        for a, b, c, q, R in triples[:5]:
            print(f"  {a:>10} {b:>10} {c:>10}  {R:>8}  {q:>8.4f}")

        max_q = triples[0][3]
        print(f"  Max quality: {max_q:.6f}")
        print(f"  M2 requires q ≤ 1+ε for all ε>0: empirical max = {max_q:.4f}")
        if max_q > 1.0:
            a, b, c, q, R = triples[0]
            print(f"  Best witness: ({a},{b},{c}), R={R}, q={q:.4f} > 1")
        else:
            print("  All triples have q ≤ 1 for this S (rare!)")


print()
print("=" * 60)
print("ANALYSIS: Why does the S-unit proof give exp(R^{1/3}), not R^{1+ε}?")
print("""
For S = {p_1,...,p_k}, the solution a + b = c with a = Π p_i^{α_i},
b = Π p_i^{β_i} can be written as:

    Σ_i α_i · log(p_i)  ≈  Σ_i β_i · log(p_i)  +  log(1 - a/c)

Baker's theorem bounds log|Λ| from below (Λ = linear form in logarithms):

    log|Λ| > -C(k, d) · (log B) · Π_i log p_i

where B = max(α_i, β_i) ≤ log(c) / log(p_min).

KEY: B ≤ log(c), NOT B ≤ log(R).
Since c can be >> R (quality > 1), we have B >> log(R),
and the Baker bound gives:

    log c  ≲  C · log c · log R  →  CIRCULAR if C·log R < 1

To close the bound NON-circularly, Stewart-Yu use a prime selection trick:
choose p* ∈ S with p* ~ R^{1/3}, apply Baker to only 3 primes near p*.
This gives B ~ log(c) / log(p*) ~ log(c) / (log(R)/3), and:

    log c  ≲  C · (log c / log R^{1/3}) · log(R^{1/3})
           =  C · log c

Still circular! But the actual argument is more subtle: the prime selection
forces a specific α_i or β_i to be large (~ c^{1/3}/log c), which gives
the c < exp(κ R^{1/3} (log R)^3) bound.

WHAT WOULD GIVE q ≤ 1+ε:
To get c ≤ K_ε · R^{1+ε} from Baker, we need B ≤ O(R^ε log R),
i.e., the exponents α_i are all ≤ R^ε.
But α_i can be as large as log(c)/log(2) ~ q·log(R)/log(2) ~ 3·log(R)/log(2)
for high-quality triples. So B ~ log(R)/log(2), giving Baker only:

    log c ≲ C · log R · log R = C · (log R)^2

which gives c ≤ exp(C (log R)^2) — still super-polynomial in R.

The gap summary:
  PROVED: c < exp(κ · R^{1/3} · (log R)^3)  [Stewart-Yu 2001]
  IMPROVED: c < exp(κ · R^{1/3} · (log R)^3 / log log R)  [Pasten 2024]
  TARGET: c ≤ K_ε · R^{1+ε}  [M2, equivalent to abc]
  GAP: sub-exponential → polynomial; requires fundamentally different method
""")
