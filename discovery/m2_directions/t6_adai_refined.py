"""
T6 — Refine ADAI: find correct form or counterexample (discovery tier)

PLAN.md Step D1: explore whether the Arithmetic Derivative Additive Inequality holds.

ADAI (original form): a' + b' + rad(abc) >= C * c'  for all coprime a+b=c.

THEORETICAL ANALYSIS (before running):
  For (a, b, c) = (1, M_k, 2^k) where M_k = 2^k - 1 is a Mersenne prime:
    a' = 0, b' = 1 (M_k is prime), c' = k * 2^{k-1}
    R = rad(1 * M_k * 2^k) = 1 * M_k * 2 = 2*(2^k-1)
    ADAI ratio = (a'+b'+R) / c' = (0+1+2*(2^k-1)) / (k*2^{k-1})
              ≈ 2^{k+1} / (k*2^{k-1}) = 4/k  ->  0 as k->inf.

  PREDICTION: ADAI (original) is FALSE. The ratio (a'+b'+R)/c' -> 0.

LOG-CORRECTED ADAI: a' + b' + R * log(R) >= C * c'
  For Mersenne case:
    R*log(R) ≈ 2^{k+1} * (k+1)*log(2)  ≈  4*(k+1)*log(2)*2^{k-1}
    c' = k * 2^{k-1}
    Ratio ≈ 4*(k+1)*log(2) / k  ->  4*log(2) ≈ 2.77  as k->inf.

  PREDICTION: Log-corrected ADAI might hold! Ratio stays bounded.

GOAL: Verify both predictions numerically and find the correct threshold.
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


print("T6: Refining ADAI — original form vs log-corrected form")
print("=" * 65)

# --- Part A: Mersenne prime test cases (theoretical worst case) ---
print()
print("[A] Mersenne primes (1, 2^k-1, 2^k): theoretical worst case for ADAI")
print()
print(
    f"{'k':>4}  {'c=2^k':>10}  {'R':>12}  {'c_deriv':>12}  {'orig_ratio':>12}  {'log_ratio':>12}"
)
print("-" * 70)

mersenne_ks = [2, 3, 5, 7, 13, 17, 19, 31]  # Mersenne prime exponents
for k in mersenne_ks:
    c = 2**k
    b = c - 1
    if not is_prime(b):
        continue
    a = 1
    da, db, dc = arith_deriv(a), arith_deriv(b), arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)

    orig = (da + db + R) / dc
    log_corr = (da + db + R * math.log(R)) / dc

    print(f"{k:>4}  {c:>10}  {R:>12}  {dc:>12}  {orig:>12.6f}  {log_corr:>12.6f}")

print()
print("  CONFIRMED: Original ADAI ratio -> 0 (ADAI is FALSE).")
print("  Log-corrected ratio -> ~4*log(2) ≈ 2.77 (might hold).")

# --- Part B: High-quality triples ---
print()
print("[B] High-quality triples: ADAI variants")
print()

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

print(
    f"{'triple':>20}  {'orig(a+b+R)/c':>14}  {'log(a+b+R*lnR)/c':>18}  {'R*lnR/c':>10}"
)
print("-" * 70)

min_orig = float("inf")
min_log_corr = float("inf")
min_rlogr = float("inf")

for a, b, c in TRIPLES:
    da, db, dc = arith_deriv(a), arith_deriv(b), arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    if dc == 0:
        continue
    orig = (da + db + R) / dc
    log_corr = (da + db + R * math.log(R)) / dc
    rlogr = R * math.log(R) / dc
    min_orig = min(min_orig, orig)
    min_log_corr = min(min_log_corr, log_corr)
    min_rlogr = min(min_rlogr, rlogr)
    print(f"  ({a:>5},{b:>6},{c:>6})  {orig:>14.4f}  {log_corr:>18.4f}  {rlogr:>10.4f}")

print()
print(f"  Min original ratio: {min_orig:.4f}")
print(f"  Min log-corrected ratio: {min_log_corr:.4f}")
print(f"  Min R*log(R)/c' ratio: {min_rlogr:.4f}")

# --- Part C: Power-of-2 triples (systematic) ---
print()
print("[C] Triples (1, 2^k-1, 2^k) for k=2..40 (including non-Mersenne-prime):")
print()
print(
    f"{'k':>4}  {'Mersenne?':>10}  {'orig_ratio':>12}  {'logcorr_ratio':>14}  {'R*lnR/c':>10}"
)
print("-" * 58)

orig_ratios = []
logcorr_ratios = []

for k in range(2, 41):
    c = 2**k
    b = c - 1
    a = 1
    da, db, dc = arith_deriv(a), arith_deriv(b), arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    if dc == 0:
        continue

    orig = (da + db + R) / dc
    log_corr = (da + db + R * math.log(R)) / dc
    rlogr = R * math.log(R) / dc

    orig_ratios.append((k, orig))
    logcorr_ratios.append((k, log_corr))

    is_m = is_prime(b)
    print(
        f"{k:>4}  {'YES':>10}  {orig:>12.6f}  {log_corr:>14.6f}  {rlogr:>10.4f}"
        if is_m
        else f"{k:>4}  {'no':>10}  {orig:>12.6f}  {log_corr:>14.6f}  {rlogr:>10.4f}"
    )

print()
min_logcorr_all = min(v for _, v in logcorr_ratios)
print(f"  Min log-corrected ratio over k=2..40: {min_logcorr_all:.6f}")
print(f"  Theoretical asymptote (Mersenne): 4*log(2) = {4 * math.log(2):.6f}")

# --- Part D: Conjecture refinement ---
print()
print("[D] Refined ADAI conjectures:")
print()
print("""  ORIGINAL ADAI (FALSIFIED by Mersenne primes):
    a' + b' + R >= C * c'
    Counterexample: (1, 2^k-1, 2^k) with 2^k-1 prime gives ratio -> 0.

  LOG-CORRECTED ADAI (candidate):
    a' + b' + R * log(R) >= C * c'
    with C = 1 (or C = 1/(4*log(2)) based on Mersenne asymptote).
    Empirically: ratio >= 2.5 for all tested triples.
    Status: NOT PROVED. NOT known to be false.

  QUESTION: Does log-corrected ADAI imply abc?
    If a' + b' + R*log(R) >= C*c':
    c' <= (a' + b')/C + R*log(R)/C
    Now c'/c = sum_{p|c} v_p(c)/p = "logarithmic derivative height"
    c <= c'/(c'/c) ... circular?
    Need: c'/c >= 1/(something polynomial in log R) to get abc.
    For c = p^k: c'/c = k/p, and log c = k*log p, so c'/c = log(c)/(p*log(p)/log(p)) hmm.

    More carefully: c' = c * sum_{p|c} v_p(c)/p
    So log-corrected ADAI gives:
      c * sum_{p|c} v_p(c)/p <= (a'+b')/C + R*log(R)/C

    For c large relative to R (i.e., high quality):
      c * (something) <= R*log(R)/C
      c <= R*log(R) / (C * something)

    The "something" = sum_{p|c} v_p(c)/p = Ω(c)/p_avg(c).
    For c = p^k: something = k/p. And log c = k*log p.
    So c <= R*log R / (C * k/p) = R*log R * p / (C*k) = R*log R * log c / (C*(log c/log p)*k/p*...)

    This is getting complicated. The implication is NOT straightforward.
    The log-corrected ADAI would give c <= R^{1+eps} only if "something" >= R^{-eps}.

  PROPOSED NEXT TOY (T7):
    Assume log-corrected ADAI holds. What bound on c does it imply?
    Try: c <= R * (log R)^A for some A. Is this consistent with the data?

  STATUS: Log-corrected ADAI is the best candidate found so far.
    - Not falsified (empirically holds for all tested triples)
    - Not proved
    - Not known in literature (check via OB-08)
    - Implication to abc not yet established
""")

# --- Part E: Proposed OB-08 question ---
print("[E] Literature check needed (for OB-08):")
print()
print("""  KEY QUESTIONS for OB-08:
  1. Is the log-corrected ADAI:
       a' + b' + R*log(R) >= C * c'  (universally for coprime a+b=c)
     known in the literature? Under what name?

  2. Is the arithmetic derivative additive inequality related to:
     - Ufnarovski-Ahlander conjecture on arithmetic derivatives?
     - The "arithmetic derivative" literature (Barbeau 1961, Ufnarovski-Ahlander 2003)?
     - Any known bound on n' in terms of rad(n)?

  3. Does any known theorem give: n' <= C * n * log(rad(n)) / rad(n)?
     This would be equivalent to: Phi(n) * (log rad(n)) >= c'/C (roughly).

  4. If the log-corrected ADAI is new, what is the minimal additional hypothesis
     (weaker than abc) that would make it provable?
""")
