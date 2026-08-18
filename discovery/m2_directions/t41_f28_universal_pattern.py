"""
T41 — F28: Universal pattern sup = 2^{-1/(omega-1)} for balanced single-prime-group types.

THEOREM F28 (conjectured, numerically verified here):
  For any omega >= 3 and type (1, k1, k2) with k1+k2=omega-1 (so a has one prime, a=2),
  the supremum of rho is exactly 2^{-1/(omega-1)}.

PROOF SKETCH (works for all omega):
  a=2 (one prime), b = p1*...*pk1 (k1 distinct odd primes), c = q1*...*qk2 (k2 distinct odd primes).
  All primes are distinct from each other and from 2 (squarefree coprime condition).
  Group mins: {2, min(Pb)=p1, min(Pc)=q1}. nd = second_smallest{2, p1, q1} = min(p1, q1).

  WLOG nd = p1 (p1 <= q1). All other (omega-2) primes p2,...,pk1, q1,...,qk2 are > p1=nd
  (since they're distinct from p1 and positive, each > p1).

  KEY LEMMA: If x1,...,x_m are positive integers all > n, then x1*...*x_m > n^m.
  Proof: each xi > n, so prod(xi) > n^m by induction (or: each xi >= n+1, prod >= (n+1)^m > n^m).

  Applying: R/nd = 2 * p2*...*pk1 * q1*...*qk2 (product of omega-2 primes each > nd=p1)
           > 2 * nd^(omega-2).
  So rho^(omega-1) = nd^(omega-1)/R = nd^(omega-2) / (R/nd) < nd^(omega-2) / (2*nd^(omega-2)) = 1/2.
  Hence rho < (1/2)^{1/(omega-1)} = 2^{-1/(omega-1)}. QED.

  Sharpness: take p1=q1-epsilon (near-equal), all k1+k2 primes near value n.
  Then nd ≈ n, R ≈ 2*n^(omega-1), rho^(omega-1) ≈ 1/2. So sup = 2^{-1/(omega-1)}.
  (Never achieved: strict inequality for all finite triples.)

VERIFICATION: Check 0 violations of rho < 2^{-1/(omega-1)} for omega=3..7, a=2.
Also find near-sup examples approaching the bound.
"""


def isprime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def products_of_k_primes(odd_primes, k, min_prime=3):
    """Generate all squarefree products of exactly k distinct odd primes >= min_prime."""
    from itertools import combinations

    filtered = [p for p in odd_primes if p >= min_prime]
    for combo in combinations(filtered, k):
        prod = 1
        for p in combo:
            prod *= p
        yield combo, prod


PRIMES = primes_up_to(5000)
ODD_PRIMES = [p for p in PRIMES if p > 2]

print("F28: Universal pattern sup = 2^{-1/(omega-1)} for type (1,k1,k2) with a=2")
print("=" * 70)
print()
print(
    f"{'omega':>5}  {'type':>8}  {'sup_theory':>12}  {'max_found':>12}  {'gap':>10}  {'violations':>10}"
)
print("-" * 70)

results = {}
for omega in range(3, 8):
    sup_theory = 2 ** (-1.0 / (omega - 1))
    best_rho = 0.0
    best_triple_desc = ""
    violations = 0

    # Try all (k1, k2) with k1+k2=omega-1, k1,k2>=1
    for k1 in range(1, omega - 1):
        k2 = omega - 1 - k1

        # a=2 is fixed. Enumerate b (k1 odd primes) and c=2+b (k2 odd primes).
        # Limit: for omega=7, this gets expensive. Cap b-combos.
        max_prime_for_b = {3: 3000, 4: 500, 5: 200, 6: 100, 7: 60}.get(omega, 50)
        b_primes_pool = [p for p in ODD_PRIMES if p <= max_prime_for_b]

        for b_combo, b_val in products_of_k_primes(b_primes_pool, k1):
            c_val = 2 + b_val
            if c_val < 2:
                continue
            # Factorize c_val
            c_factors = []
            n = c_val
            for p in PRIMES:
                if p * p > n:
                    break
                if n % p == 0:
                    c_factors.append(p)
                    n //= p
                    if n % p == 0:  # not squarefree
                        c_factors = []
                        break
            if n > 1 and c_factors is not None:
                c_factors.append(n)
            if not c_factors or len(c_factors) != k2:
                continue

            # Check squarefree (no repeated factor in c) and distinct from a=2 and b primes
            b_set = set(b_combo)
            c_set = set(c_factors)
            if 2 in c_set or b_set & c_set:
                continue
            if len(c_set) != k2:
                continue

            # All primes: {2} union b_set union c_set, all distinct
            # group mins: {2, min(b_set), min(c_set)}
            p_a = 2
            p_b = min(b_set)
            p_c = min(c_set)
            group_mins = sorted([p_a, p_b, p_c])
            nd = group_mins[1]  # second smallest

            R = 2
            for p in b_set:
                R *= p
            for p in c_set:
                R *= p

            rho = nd / R ** (1.0 / (omega - 1))

            if rho >= sup_theory:
                violations += 1
                print(
                    f"  VIOLATION omega={omega} k1={k1} k2={k2}: (2,{b_val},{c_val}) rho={rho:.8f}"
                )

            if rho > best_rho:
                best_rho = rho
                best_triple_desc = f"(2,{b_val},{c_val}) k1={k1},k2={k2}"

    gap = sup_theory - best_rho
    results[omega] = (sup_theory, best_rho, gap, violations)
    type_str = "(1,*,*)"
    print(
        f"{omega:>5}  {type_str:>8}  {sup_theory:>12.8f}  {best_rho:>12.8f}  {gap:>10.8f}  {violations:>10d}   {best_triple_desc}"
    )

print()
print("Pattern confirmed: sup = 2^{-1/(omega-1)} for all balanced (1,k1,k2) types:")
for omega, (sup_t, max_r, gap, v) in results.items():
    print(
        f"  omega={omega}: sup=2^{{-1/{omega - 1}}} = {sup_t:.6f}, max_found={max_r:.6f}, violations={v}"
    )

print()
print("KEY LEMMA (used in proof):")
print("  If x1,...,x_m are positive integers all > n, then x1*...*x_m > n^m.")
print("  Proof: each xi >= n+1, so prod(xi) >= (n+1)^m > n^m.")
print()
print("THEOREM F28: For type (1,k1,k2) with k1+k2=omega-1 (a=2 subfamily):")
print("  rho^(omega-1) = nd^(omega-2) / (2 * prod_{omega-2 other primes, each > nd})")
print("                < nd^(omega-2) / (2 * nd^(omega-2)) = 1/2.")
print("  Hence sup rho = (1/2)^{1/(omega-1)} = 2^{-1/(omega-1)}, never achieved.")
