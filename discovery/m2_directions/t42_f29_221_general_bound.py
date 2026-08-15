"""
T42 — F29: General analytical proof that ALL type (2,2,1) triples have rho < (1/6)^{1/4}.

F24 proved sup=(1/6)^{1/4} using the a=6 extremal subfamily.
F29 proves the UNIVERSAL BOUND rho^4 < 1/6 for ALL (2,2,1) triples analytically.

TYPE (2,2,1): a=p1*p2, b=q1*q2, c=r (prime), all 5 primes distinct, p1<p2, q1<q2.
F10 nd = second_smallest{min(Pa), min(Pb), min(Pc)} = second_smallest{p1, q1, r}.
Since r = p1*p2 + q1*q2 > max(p1,q1), r is always the LARGEST group min.
So nd = max(p1, q1).

THEOREM F29: rho^4 = nd^4/R < 1/6 for ALL type (2,2,1) triples.

PROOF (WLOG nd = q1, i.e., q1 >= p1):
  rho^4 = q1^4/(p1*p2*q1*q2*r) = q1^3/(p1*p2*q2*r).

  STEP 1: r = p1*p2 + q1*q2 >= q1*q2.
    => p1*p2*q2*r >= p1*p2*q2*q1*q2 = p1*p2*q1*q2^2.

  STEP 2: p1*p2 >= 2*3 = 6 (minimum product of 2 distinct primes, using p1 >= 2).
  STEP 3: q2 >= q1 + 1 (distinct primes, q2 > q1).
    => p1*p2*q1*q2^2 >= 6*q1*(q1+1)^2.

  STEP 4: 6*q1*(q1+1)^2 > 6*q1^3 iff (q1+1)^2 > q1^2. ALWAYS TRUE.

  Combining: p1*p2*q2*r > 6*q1^3. So rho^4 < 1/6. QED.

SHARPNESS: As q1 -> q2 -> n and p1=2, p2=3 (a=6 fixed):
  rho^4 = q1^3/(6*q2*(6+q1*q2)) -> n^2/(6*(6+n^2)) -> 1/6 as n->inf.
  Bound is TIGHT: sup = (1/6)^{1/4}. Never achieved.
"""

import math

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

SUP = (1/6) ** 0.25
print(f"F29: type (2,2,1) universal bound rho < (1/6)^{{1/4}} = {SUP:.8f}")
print()

# Verify analytic proof steps numerically
print("PROOF STEP VERIFICATION:")
print("For all (2,2,1) triples, check: p1*p2*q1*q2^2 >= 6*q1*(q1+1)^2 > 6*q1^3")
print()

# Check analytically: q1*(q1+1)^2 > q1^3 for all q1>=2
print("  q1*(q1+1)^2 > q1^3 for q1>=2?")
for q1 in range(2, 20):
    lhs = q1 * (q1+1)**2
    rhs = q1**3
    assert lhs > rhs, f"FAIL q1={q1}"
print("  VERIFIED for q1=2..19 (trivial: (q1+1)^2 > q1^2 always)")
print()

# Full numerical verification
print(f"Verifying rho < (1/6)^{{1/4}} for all type (2,2,1) with c<=20000...")
violations = 0
max_rho = 0.0
max_triple = None
count = 0

for c in range(6, 20001):
    if not all(factorize(c).get(p, 0) == 1 for p in factorize(c)):
        pass
    fc = factorize(c)
    if any(v > 1 for v in fc.values()) or len(fc) != 1:
        continue  # c must be prime (1 factor)

    r = c
    for a in range(1, (c + 1) // 2 + 1):
        b = c - a
        if b < a or gcd(a, b) != 1:
            continue
        fa = factorize(a)
        fb = factorize(b)
        if any(v > 1 for v in fa.values()) or len(fa) != 2:
            continue
        if any(v > 1 for v in fb.values()) or len(fb) != 2:
            continue
        pa = set(fa.keys())
        pb = set(fb.keys())
        pc = set(fc.keys())
        if pa & pb or pa & pc or pb & pc:
            continue

        p1, p2 = sorted(pa)
        q1, q2 = sorted(pb)
        # nd = second_smallest of {p1, q1, r}
        group_mins = sorted([p1, q1, r])
        nd = group_mins[1]

        R = math.prod(pa | pb | pc)
        rho = nd / R ** 0.25

        count += 1
        if rho >= SUP:
            violations += 1
            print(f"  VIOLATION: ({a},{b},{c}) rho={rho:.8f}")

        if rho > max_rho:
            max_rho = rho
            max_triple = (a, b, c, p1, p2, q1, q2, r)

print(f"Checked {count} type (2,2,1) triples with c<=20000")
print(f"Violations: {violations}")
if max_triple:
    a, b, c, p1, p2, q1, q2, r = max_triple
    print(f"Max rho = {max_rho:.8f} at ({a},{b},{c})")
    print(f"  a={a}={p1}*{p2}, b={b}={q1}*{q2}, c={c}, nd=max({p1},{q1})={max(p1,q1)}")
    print(f"  Gap to sup: {SUP - max_rho:.8f}")
print()

# Show the proof works with concrete numbers
print("PROOF STEPS for extremal example (a=6, near-twin b):")
for q1 in [5, 11, 101, 1009]:
    q2 = q1 + 2
    # check q1, q2 prime
    def isp(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    while not isp(q2): q2 += 2
    r_val = 6 + q1 * q2
    # check r prime (may not be)
    for dr in range(0, 200):
        if isp(r_val + dr) and (r_val+dr) not in {2,3,q1,q2}:
            r_val = r_val + dr
            break

    rho4 = q1**3 / (6 * q2 * r_val)
    step1_bound = q1**3 / (6 * q1 * q2**2)  # = q1^2/(6*q2^2)
    print(f"  q1={q1}, q2={q2}, r={r_val}: rho^4={rho4:.6f}, step1_bound={step1_bound:.6f}, 1/6={1/6:.6f}")
    print(f"    6*q1^3={6*q1**3}, p1*p2*q2*r >= 6*q1*q2^2={6*q1*q2**2} > 6*q1^3: {6*q1*q2**2 > 6*q1**3}")

print()
print("F29 THEOREM: For ALL type (2,2,1) triples: rho^4 < 1/6.")
print("  KEY: p1*p2*q2*r >= p1*p2*q1*q2^2 >= 6*q1*(q1+1)^2 > 6*q1^3.")
print(f"  Sup = (1/6)^{{1/4}} = {SUP:.8f} (never achieved).")
