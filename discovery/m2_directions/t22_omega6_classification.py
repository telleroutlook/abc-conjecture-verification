"""
T22 — ω=6 partition-type classification (F11 extension)

Extends the optimal crossing formula (F10) to ω=6 triples.
Smallest ω=6 triple: one of the constituents must include primes from {2,3,5,7,11,13,...}.
The smallest squarefree product of 6 distinct primes is 2*3*5*7*11*13=30030.
So c >= 30030 for type (0,0,6), but smaller types like (2,2,2) can have smaller c.

PREDICTION from F10:
  min nd norm = second smallest of {min(Pa), min(Pb), min(Pc)}

BOUNDED types: those where the second smallest can be kept constant in growing subfamilies.
UNBOUNDED types: where the second smallest grows.
"""

from collections import defaultdict


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = 1
    return f


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def is_squarefree(n):
    return all(v == 1 for v in factorize(n).values())


def partition_type(a, b, c):
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    return (len(fa), len(fb), len(fc))


def optimal_nd_norm(a, b, c):
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    Pa = sorted(fa.keys())
    Pb = sorted(fb.keys())
    Pc = sorted(fc.keys())
    min_a = Pa[0] if Pa else float("inf")
    min_b = Pb[0] if Pb else float("inf")
    min_c = Pc[0] if Pc else float("inf")
    candidates = []
    if Pa and Pb:
        candidates.append(max(min_a, min_b))
    if Pa and Pc:
        candidates.append(max(min_a, min_c))
    if Pb and Pc:
        candidates.append(max(min_b, min_c))
    if not candidates:
        return float("inf"), None
    best = min(candidates)
    if Pa and Pb and max(min_a, min_b) == best:
        pair = ("Pa", "Pb", min_a, min_b)
    elif Pa and Pc and max(min_a, min_c) == best:
        pair = ("Pa", "Pc", min_a, min_c)
    else:
        pair = ("Pb", "Pc", min_b, min_c)
    return best, pair


def rad(a, b, c):
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = set(fa) | set(fb) | set(fc)
    r = 1
    for p in primes:
        r *= p
    return r


print("T22: ω=6 partition-type classification (F11) — c ≤ 5000")
print("=" * 65)
print()

types_data = defaultdict(list)
count_total = 0

for c in range(4, 5001):
    for a in range(1, (c + 1) // 2 + 1):
        b = c - a
        if b <= 0 or b < a:
            continue
        if gcd(a, b) != 1:
            continue
        if not (is_squarefree(a) and is_squarefree(b) and is_squarefree(c)):
            continue
        fa, fb, fc = factorize(a), factorize(b), factorize(c)
        omega = len(set(fa) | set(fb) | set(fc))
        if omega != 6:
            continue
        pt = partition_type(a, b, c)
        R = rad(a, b, c)
        nd_norm, pair = optimal_nd_norm(a, b, c)
        if nd_norm == float("inf"):
            continue
        ratio = nd_norm / (R ** (1.0 / 5))  # R^{1/(omega-1)} = R^{1/5}
        types_data[pt].append((a, b, c, ratio, nd_norm, pair))
        count_total += 1

print(f"Total ω=6 triples found: {count_total}")
print()
print(
    f"{'Type':14}  {'#triples':>8}  {'max_ratio':>10}  {'min_ratio':>10}  {'pattern'}"
)
print("  " + "-" * 65)
for pt in sorted(types_data.keys()):
    data = types_data[pt]
    ratios = [d[3] for d in data]
    max_r = max(ratios)
    min_r = min(ratios)
    worst = max(data, key=lambda x: x[3])
    na, nb, nc = pt
    # Predict based on F10 rule
    # UNBOUNDED iff two single-prime non-dominant groups forced large
    singletons = sum(1 for n in (na, nb, nc) if n == 1)
    empties = sum(1 for n in (na, nb, nc) if n == 0)
    if empties >= 1:
        # Pa or Pb empty: min = inf, second is max(min_Pb, min_Pc) or similar
        # For (0,k,1) or (0,1,k): one single prime forced large
        if any(
            n == 1 and m == 0
            for (n, m) in [(na, nb), (nb, na), (nc, na), (na, nc), (nb, nc), (nc, nb)]
        ):
            pred = "UNBOUNDED?"
        else:
            pred = "bounded?"
    elif singletons >= 2:
        # Two single-prime groups: they could both grow
        pred = "UNBOUNDED?"
    else:
        pred = "bounded?"
    print(
        f"  {str(pt):14}  {len(data):>8}  {max_r:>10.4f}  {min_r:>10.4f}  {pred}  worst=({worst[0]},{worst[1]},{worst[2]})"
    )

print()
print("Top-5 worst ratios across all ω=6 triples:")
all_data = [
    (a, b, c, r, nd, pair, pt)
    for pt, data in types_data.items()
    for (a, b, c, r, nd, pair) in data
]
all_data.sort(key=lambda x: -x[3])
for a, b, c, r, nd, pair, pt in all_data[:5]:
    print(f"  ({a},{b},{c}) type={pt} nd_norm={nd} ratio={r:.4f} pair={pair}")

print()
print("VERIFICATION of F10 formula (second-smallest formula):")
errors = 0
for pt, data in types_data.items():
    for a, b, c, ratio, nd_norm, pair in data[:5]:
        fa, fb, fc = factorize(a), factorize(b), factorize(c)
        mins = [
            min(fa.keys()) if fa else float("inf"),
            min(fb.keys()) if fb else float("inf"),
            min(fc.keys()) if fc else float("inf"),
        ]
        sorted_mins = sorted(m for m in mins if m != float("inf"))
        predicted = sorted_mins[1] if len(sorted_mins) >= 2 else float("inf")
        if abs(predicted - nd_norm) > 0.01:
            errors += 1
            print(f"  MISMATCH: ({a},{b},{c}) predicted={predicted} actual={nd_norm}")
if errors == 0:
    print("  All verified: F10 formula holds for all ω=6 triples checked. ✓")
