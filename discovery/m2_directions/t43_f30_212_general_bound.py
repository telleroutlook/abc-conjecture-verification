"""
T43 — F30: General bound rho^4 < 1/6 for ALL type (2,1,2) triples.
Fast version: iterate over b=prime, a=semiprime, compute c=a+b.
"""


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


# Precompute semiprimes up to LIMIT as (a, p1, p2)
LIMIT = 50000

print("Precomputing semiprimes and primes...")
primes = [p for p in range(2, LIMIT + 1) if is_prime(p)]
prime_set = set(primes)

# semiprimes: a = p1*p2 with distinct primes p1 < p2, a <= LIMIT
semiprimes = []
for i, p1 in enumerate(primes):
    if p1 * p1 >= LIMIT:
        break
    for p2 in primes[i + 1 :]:
        a = p1 * p2
        if a > LIMIT:
            break
        semiprimes.append((a, p1, p2))

print(f"  {len(semiprimes)} semiprimes, {len(primes)} primes up to {LIMIT}")

SUP = (1 / 6) ** 0.25
print(f"\nF30: type (2,1,2) bound rho < (1/6)^{{1/4}} = {SUP:.8f}")
print(f"Verifying for b+a=c with b prime, a semiprime, c semiprime, c<={LIMIT}...")

violations = 0
max_rho = 0.0
max_triple = None
count = 0
all_high = []

for q1 in primes:
    for a, p1, p2 in semiprimes:
        c = a + q1
        if c > LIMIT:
            break
        if not (p1 != q1 and p2 != q1):
            continue
        # Check c is squarefree semiprime
        if c % 2 == 0:
            r1 = 2
            rem = c // 2
        else:
            r1 = None
            for r in primes:
                if r >= int(c**0.5) + 2:
                    break
                if c % r == 0:
                    r1 = r
                    rem = c // r
                    break
        if r1 is None:
            continue
        r2 = rem
        if r2 <= r1 or not is_prime(r2):
            continue
        # Check all 5 primes distinct
        if len({p1, p2, q1, r1, r2}) != 5:
            continue

        group_mins = sorted([p1, q1, r1])
        nd = group_mins[1]
        R = p1 * p2 * q1 * r1 * r2
        rho = nd / R**0.25

        count += 1
        if rho >= SUP:
            violations += 1
            print(f"  VIOLATION: ({a},{q1},{c}) rho={rho:.8f}")

        if rho > max_rho:
            max_rho = rho
            max_triple = (a, q1, c, p1, p2, q1, r1, r2)

        if rho > 0.60:
            all_high.append((rho, a, q1, c, p1, p2, q1, r1, r2))

print(f"\nChecked {count} type (2,1,2) triples with c<={LIMIT}")
print(f"Violations: {violations}")
if max_triple:
    a, b, c, p1, p2, q1, r1, r2 = max_triple
    nd = sorted([p1, q1, r1])[1]
    print(f"Max rho = {max_rho:.8f} at ({a},{b},{c})")
    print(f"  a={a}={p1}*{p2}, b={b}={q1}, c={c}={r1}*{r2}")
    print(f"  group mins: {p1}, {q1}, {r1}; nd={nd}")
    print(f"  Gap to sup: {SUP - max_rho:.8f}")

print("\nTop 10 near-extremal (rho>0.60):")
all_high.sort(reverse=True)
for rho, a, b, c, p1, p2, q1, r1, r2 in all_high[:10]:
    nd = sorted([p1, q1, r1])[1]
    if nd == p1:
        grp = "Pa"
    elif nd == q1:
        grp = "Pb"
    else:
        grp = "Pc"
    print(f"  rho={rho:.5f}: a={p1}*{p2}, b={q1}, c={r1}*{r2}; nd={nd}({grp})")
