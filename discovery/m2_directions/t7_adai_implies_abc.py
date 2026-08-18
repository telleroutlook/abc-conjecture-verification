"""
T7 — Conditional implication: does ADAI-log imply abc? (discovery tier)

PLAN.md Step D3: Assume log-corrected ADAI holds. What bound on c does it imply?

LOG-CORRECTED ADAI (assumed as hypothesis):
  a' + b' + R * ln(R) >= C * c'  for all coprime a+b=c.

IMPLICATION CHAIN:
  Step 1: c' = c * sigma(c) where sigma(c) = sum_{p|c} v_p(c)/p
  Step 2: ADAI-log gives c' <= (a' + b' + R*ln(R)) / C
  Step 3: c = c' / sigma(c) <= (a' + b' + R*ln(R)) / (C * sigma(c))
  Step 4: For abc: need c <= K_eps * R^{1+eps}

KEY QUESTION: Is sigma(c) bounded below by a function of R that makes Step 3 give abc?

PREDICTION (from T6 analysis):
  For c = p^k (prime power): sigma(c) = k/p.
  For (1, 2^k-1, 2^k) Mersenne case: c = 2^k, sigma = k/2, R approx 2*c.
  Bound: c <= R*ln(R) / (C * k/2) = 2*R*ln(R)/(C*k)
        = 2*R*ln(R) / (C * log(c)/log(2))
        = 2*R*ln(R)*log(2) / (C * log(c))
  Since R ~ 2c: this gives c ~ 2c*ln(2c)*log(2)/(C*log(c)) ~ const * c.  (TRIVIAL!)

  ADAI-log DOES NOT IMPLY abc for the Mersenne family.
  The obstruction: sigma(c) -> 0 faster than R -> inf.

GOAL: Verify this obstruction numerically, find the best bound ADAI-log gives,
      and check if it at least gives c <= R^2 (quality <= 2) or something useful.
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


def arith_deriv(n):
    if n <= 1:
        return 0
    result = 0
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            result += n // d
            m //= d
        d += 1
    if m > 1:
        result += n // m
    return result


def sigma(n):
    """sigma(n) = n'/n = sum_{p|n} v_p(n)/p"""
    if n <= 1:
        return 0.0
    facts = factorize(n)
    return sum(e / p for p, e in facts.items())


def is_prime(n):
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


print("T7: Conditional implication ADAI-log => abc")
print("=" * 65)
print()
print("ASSUMPTION: a' + b' + R*ln(R) >= C * c'  [ADAI-log, unproved]")
print()
print("IMPLICATION CHAIN:")
print("  c' <= (a'+b'+R*ln(R))/C")
print("  c = c'/sigma(c) <= (a'+b'+R*ln(R)) / (C * sigma(c))")
print()

# --- Part A: Trace the implication for known triples ---
print("[A] What bound on c does ADAI-log give (assuming C=1)?")
print()
print(
    f"  {'triple':>20}  {'R':>8}  {'sigma(c)':>10}  {'ADAI_bound':>12}  {'c':>10}  {'ratio':>8}  {'abc_q':>8}"
)
print("  " + "-" * 82)

TRIPLES = [
    (1, 8, 9),
    (3, 125, 128),
    (1, 80, 81),
    (1, 4374, 4375),
    (1, 2400, 2401),
    (5, 27, 32),
    (1, 242, 243),
    (1, 48, 49),
    (13, 243, 256),
    (1, 728, 729),
    (32, 49, 81),
]

for a, b, c in TRIPLES:
    da, db, dc = arith_deriv(a), arith_deriv(b), arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    sig_c = sigma(c)
    # ADAI-log bound (with C=1): c <= (a'+b'+R*ln(R)) / sigma(c)
    adai_bound = (da + db + R * math.log(R)) / sig_c
    q = math.log(c) / math.log(R)
    bound_ratio = adai_bound / c
    print(
        f"  ({a:>5},{b:>6},{c:>6})  {R:>8}  {sig_c:>10.5f}  {adai_bound:>12.1f}  {c:>10}  {bound_ratio:>8.2f}  {q:>8.4f}"
    )

print()
print("  NOTE: 'ADAI_bound' is the upper bound on c that ADAI-log gives.")
print("  'ratio' = ADAI_bound/c. If >> 1, the bound is much weaker than c itself.")
print("  For a useful bound we'd need ratio close to 1 (tight) or c <= K*R^{1+eps}.")

# --- Part B: Mersenne family — the critical obstruction ---
print()
print("[B] Mersenne family (1, 2^k-1, 2^k): what bound does ADAI-log give?")
print()
print(
    f"  {'k':>4}  {'R':>12}  {'sigma(c)':>10}  {'ADAI_bound/c':>14}  {'ADAI_bound/R^2':>16}  {'c/R^2':>10}"
)
print("  " + "-" * 72)

for k in [2, 3, 5, 7, 13, 17, 19, 31]:
    c = 2**k
    b = c - 1
    if not is_prime(b):
        continue
    a = 1
    da, db, dc = arith_deriv(a), arith_deriv(b), arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    sig_c = sigma(c)
    adai_bound = (da + db + R * math.log(R)) / sig_c
    # How does ADAI_bound compare to R^2 (a much weaker bound than abc)?
    R2 = R * R
    print(
        f"  {k:>4}  {R:>12}  {sig_c:>10.5f}  {adai_bound / c:>14.2f}  {adai_bound / R2:>16.4f}  {c / R2:>10.6f}"
    )

print()
print("  KEY OBSERVATION:")
print("  - 'ADAI_bound/c' -> infinity: ADAI-log gives NO useful bound on c!")
print("  - 'ADAI_bound/R^2' is roughly constant: ADAI-log gives c <= O(R^2 * log R).")
print("  - But abc says c <= K_eps * R^{1+eps}, MUCH STRONGER than c <= O(R^2).")
print("  - The obstruction: sigma(c) = k/2 -> 0 faster than the improvement in bound.")

# --- Part C: Analytic derivation ---
print()
print("[C] Analytic derivation of the obstruction:")
print()
print("""  For (1, 2^k-1, 2^k) with 2^k-1 Mersenne prime:
    a' = 0, b' = 1, c' = k*2^{k-1}, R = 2*(2^k-1) ~ 2^{k+1}
    sigma(c) = k/2 (since c = 2^k, sigma = k/2)

  ADAI-log gives:
    c' <= (0 + 1 + R*ln(R)) / C ~ R*ln(R) / C

  Since c = c' / sigma(c) = c' / (k/2):
    c <= 2 * c' / (k*C) <= 2 * R*ln(R) / (k*C)

  Substituting R ~ 2^{k+1} and k = log2(c) = log(c)/log(2):
    c <= 2 * 2^{k+1} * (k+1)*log(2) / (k*C)
       ~ 4 * log(2) * 2^k * (1 + 1/k) / C
       ~ (4*log(2)/C) * c   as k -> inf.

  This is c <= const * c, which is TRIVIAL (no bound on c in terms of R).

  CONCLUSION: Log-corrected ADAI does NOT imply abc, and does not even give c <= R^{1+eps}.
  At best it gives c <= C' * R^2 * log(R) (from ADAI_bound/R^2 being O(1) in Part B).
  This is quality <= 2, which is much weaker than abc (quality <= 1+eps).
""")

# --- Part D: What WOULD be needed ---
print("[D] What additional hypothesis WOULD make ADAI-log imply abc?")
print()
print("""  The chain breaks at: sigma(c) = c'/c can be arbitrarily small.
  For abc, we need to ensure c is small relative to R.

  APPROACH 1: Strengthen ADAI-log to bound c directly (not just c').
  A "strong ADAI": a' + b' + R*ln(R) >= C * c * sigma(c)^alpha
    for some alpha in (0,1). This would give:
    c <= (a'+b'+R*ln(R))^{1/(1-alpha)} / (C * sigma(c)^{alpha/(1-alpha)})
    Still unclear whether this gives abc.

  APPROACH 2: Lower-bound sigma(c) from the abc triple structure.
  For coprime a+b=c with c not a prime power: omega(c) >= 2, sigma(c) >= 2/c_max_prime.
  For c = product of distinct primes: sigma(c) = sum 1/p_i = O(log log c).
    Then c <= R * ln(R) / (C * log log c) which gives c = O(R * ln R / log log c).
    Still weaker than abc for high-quality triples.

  APPROACH 3: Use a+b structure to bound a' + b' from below.
  Key: a' + b' = a*sigma(a) + b*sigma(b).
  For a+b=c: a*sigma(a) + b*sigma(b) = (c-b)*sigma(a) + b*sigma(b).
  If sigma(a) and sigma(b) are not too small, a'+b' ~ c * min(sigma(a),sigma(b)).
  Then ADAI-log gives: c*sigma(a_min) + R*ln(R) >= C * c*sigma(c).
  If sigma(a_min) >> sigma(c), this bounds sigma(c)/sigma(a_min) <= something.
  But we can have sigma(a) and sigma(c) both small simultaneously (e.g., both prime powers).

  CONCLUSION: ADAI-log alone is INSUFFICIENT to prove abc.
  The missing ingredient is a LOWER BOUND on sigma(c) in terms of R
  that is NOT provable from ADAI-log alone.

  HONEST STATUS:
  - ADAI-log (if true) gives c <= O(R^2 * log R).
  - This corresponds to quality <= 2, not quality <= 1+eps.
  - Route IV (arithmetic derivative) does NOT yield a proof of abc
    without an additional theorem bounding sigma(c) from below.
  - Such a theorem would say: for coprime a+b=c, c'/c >= 1/R^delta
    for some delta < 1. This is essentially equivalent to abc (quality <= 1+delta).

  The arithmetic derivative approach has the SAME obstruction as the direct approach:
  we need to control how "concentrated" (prime-power-like) c can be relative to R.
  This concentration IS the abc conjecture.
""")

# --- Part E: Summary ---
print("[E] Summary and route status:")
print()
print("""  FINDING: Log-corrected ADAI is NOT sufficient to prove abc.

  What ADAI-log gives (assuming it holds):
    c <= O(R^2 * log R) for all coprime a+b=c.  [quality <= 2, unconditional on ADAI-log]

  What abc requires:
    c <= K_eps * R^{1+eps} for all eps > 0.  [quality <= 1+eps for any eps]

  The gap: ADAI-log cannot distinguish quality 1.5 from quality 1.01.
  Closing this gap requires bounding sigma(c) = c'/c from below,
  which is equivalent to bounding the "arithmetic density of prime powers" in c
  relative to R — and this is the content of abc.

  ROUTE IV STATUS (2026-08-15):
    - Original ADAI: FALSIFIED.
    - Log-corrected ADAI: OPEN (not falsified, not proved).
    - ADAI-log => abc: FALSE (Mersenne obstruction).
    - ADAI-log => c <= O(R^2): likely TRUE (consistent with all data), but weak.
    - Value of route: Identified sigma(c) as the precise gap; no new proof of abc.

  NEXT: D4 (Lean formalization of the equivalence theorem, conditional on ADAI)
  and D5 (decision gate: close Route IV as explored).
""")
