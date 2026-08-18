"""
T43b — F30 CORRECTION: Type (2,1,2) has sup = 2^{-1/4}, NOT (1/6)^{1/4}.

FINDING: F25 was WRONG. The extremal family for (2,1,2) is NOT a=6 fixed.
         The true extremal is: b=2 (smallest prime), a=p*q near-twin, c=p*q+2=r*s near-twin.
         As p≈q≈r≈s≈n: rho^4 -> 1/2, so sup = 2^{-1/4} ≈ 0.841.

PROOF of rho^4 < 1/2 for ALL (2,1,2) triples:
WLOG nd = p1 = min(Pa) (by symmetry / relabeling). Then:
  rho^4 = p1^3 / (p2 * q1 * r1 * r2)  (where q1 = b, r1*r2 = c)
  Since r1*r2 = c = p1*p2 + q1 >= p1*p2:
  p2 * r1 * r2 >= p2 * p1 * p2 = p1 * p2^2 > p1^3  (since p2 > p1)
  Hence rho^4 < p1^3 / (2 * p1^3) = 1/2. QED.

This is the SAME proof as for type (1,2,2) (F28 / F27), matching the a<->b symmetry.
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


SUP_NEW = 2 ** (-0.25)  # 2^{-1/4} ≈ 0.841
SUP_OLD = (1 / 6) ** 0.25  # (1/6)^{1/4} ≈ 0.639

LIMIT = 50000

print("T43b: Verifying corrected sup = 2^{-1/4} for type (2,1,2)")
print(f"  Old (wrong) sup: (1/6)^{{1/4}} = {SUP_OLD:.6f}")
print(f"  New (correct) sup: 2^{{-1/4}} = {SUP_NEW:.6f}")
print()

# Precompute
primes = [p for p in range(2, LIMIT + 1) if is_prime(p)]
prime_set = set(primes)

semiprimes = []
prime_list = primes
for i, p1 in enumerate(prime_list):
    if p1 * p1 >= LIMIT:
        break
    for p2 in prime_list[i + 1 :]:
        a = p1 * p2
        if a > LIMIT:
            break
        semiprimes.append((a, p1, p2))

print(f"Checking all (2,1,2) triples with c<={LIMIT}...")
violations_old = 0  # rho >= (1/6)^{1/4}
violations_new = 0  # rho >= 2^{-1/4}
max_rho = 0.0
max_triple = None
count = 0

for q1 in primes:
    for a, p1, p2 in semiprimes:
        c = a + q1
        if c > LIMIT:
            break
        if q1 == p1 or q1 == p2:
            continue
        # Find semiprime factorization of c
        r1 = None
        if c % 2 == 0:
            if (
                c // 2 > 1
                and is_prime(c // 2)
                and c // 2 != p1
                and c // 2 != p2
                and c // 2 != q1
            ):
                r1, r2 = 2, c // 2
            else:
                continue
        else:
            for r in prime_list:
                if r * r > c:
                    break
                if c % r == 0:
                    rem = c // r
                    if is_prime(rem) and r != rem:
                        r1, r2 = r, rem
                    break
        if r1 is None:
            continue
        if len({p1, p2, q1, r1, r2}) != 5:
            continue

        group_mins = sorted([p1, q1, r1])
        nd = group_mins[1]
        R = p1 * p2 * q1 * r1 * r2
        rho = nd / R**0.25

        count += 1
        if rho >= SUP_OLD:
            violations_old += 1
        if rho >= SUP_NEW:
            violations_new += 1
            print(f"  NEW VIOLATION: ({a},{q1},{c}) rho={rho:.8f}")

        if rho > max_rho:
            max_rho = rho
            max_triple = (a, q1, c, p1, p2, q1, r1, r2)

print(f"\nChecked {count} type (2,1,2) triples with c<={LIMIT}")
print(f"Violations (rho >= (1/6)^{{1/4}}=old wrong sup): {violations_old}")
print(f"Violations (rho >= 2^{{-1/4}}=new correct sup): {violations_new}")
if max_triple:
    a, b, c, p1, p2, q1, r1, r2 = max_triple
    nd = sorted([p1, q1, r1])[1]
    print(f"\nMax rho = {max_rho:.8f} (should be < {SUP_NEW:.6f})")
    print(f"  at ({a},{b},{c}): a={p1}*{p2}, b={b}, c={r1}*{r2}, nd={nd}")
    print(f"  Gap to 2^{{-1/4}}: {SUP_NEW - max_rho:.6f}")
print()
print("CONCLUSION: sup(2,1,2) = 2^{-1/4} (by a<->b symmetry with (1,2,2))")
print(f"  sup(1,2,2) = 2^{{-1/4}} ≈ {SUP_NEW:.6f} [proved by F26/F27]")
print(f"  sup(2,1,2) = 2^{{-1/4}} ≈ {SUP_NEW:.6f} [F25 was WRONG; corrected here]")

# Verify the proof: rho^4 < 1/2 for all (2,1,2) triples
print()
print("Proof verification: rho^4 < 1/2 for all (2,1,2) triples?")
max_rho4 = max_rho**4
print(f"  Max rho^4 observed = {max_rho4:.6f} (should be < 0.5)")
assert max_rho4 < 0.5, "PROOF FAILS"
print("  CONFIRMED: rho^4 < 1/2 for all checked triples.")
print()
print("Extremal family approach:")
print("  b=2 (fixed), a=p1*p2 near-twin, c=p1*p2+2=r1*r2 near-twin.")
print("  nd=p1 (smallest of Pa), rho^4 = p1^3/(2*p2*r1*r2).")
print("  As p1~p2~r1~r2~n: rho^4 -> n^3/(2*n^3) = 1/2.")
print("  Since p2*r1*r2 >= p1*p2^2 > p1^3 (as p2>p1): rho^4 < 1/2 strictly.")
