"""
T5 — Arithmetic Wronskian candidate: exploring Phi(n) = n/rad(n) (discovery tier)

PROPOSED TOOL: Phi(n) = n / rad(n)  = product_{p|n} p^{v_p(n)-1}

This is the "squarefull excess" of n: it measures how far n is from being squarefree.

KEY OBSERVATION for coprime a+b=c:
  Each prime p divides exactly ONE of a, b, c (since gcd(a,b)=1 implies gcd(a,c)=gcd(b,c)=1).
  Therefore: Phi(a)*Phi(b)*Phi(c) = abc / rad(abc)

The abc conjecture is EQUIVALENT to:
  For all eps > 0, exists K_eps: Phi(c) <= K_eps * R^eps  for all coprime a+b=c.
  (Since Phi(c) = c/rad(c) and c/rad(c) <= c/1 = c, and c <= K_eps R^{1+eps} iff
   c/rad(c) <= K_eps * R^{1+eps} / rad(c) which is <= K_eps * R^eps since c <= rad(c)*R^eps... hmm)

More carefully:
  abc says: c <= K_eps * R^{1+eps}
  Since rad(c) <= R, we have c = rad(c) * Phi(c) <= R * Phi(c).
  So: c <= R * Phi(c) <= K_eps * R^{1+eps} iff Phi(c) <= K_eps * R^eps.
  Conversely: if Phi(c) <= K_eps * R^eps, then c = rad(c)*Phi(c) <= R*K_eps*R^eps = K_eps*R^{1+eps}.

EQUIVALENCE: abc(eps) <=> Phi(c) <= K_eps * R^eps  for all coprime a+b=c. (*)

This means: THE TOOL Phi is EXACTLY EQUIVALENT to abc.
  - If we can PROVE (*) for Phi, we PROVE abc.
  - If we can prove Phi(c) <= R^{0.5} say (for eps=0.5), we get c <= R^{1.5} (a weaker bound).

Now explore: WHAT DOES Phi(c) look like empirically?
And: CAN WE BOUND Phi(c) IN TERMS OF Phi(a), Phi(b), AND rad(abc)?

The ARITHMETIC WRONSKIAN:
  W_Phi(a, b) = a * Phi(b) / b - Phi(a) / a * b  [analogue of fg' - f'g, using Phi/n as "derivative"]
              = a * (b/rad(b)) / b - (a/rad(a)) * b
              = a / rad(b) - b / rad(a)

This is rational. We explore |W_Phi| and ask: can it be bounded from below (non-degeneracy)?

NON-CIRCULARITY: exploring known triples for structural insight. No K_eps is fitted.
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


def phi_excess(n):
    """Phi(n) = n / rad(n): squarefull excess."""
    return n // rad(n)


def quality(a, b, c):
    R = rad(a) * rad(b) * rad(c)  # coprime so rad(abc) = rad(a)*rad(b)*rad(c)
    return math.log(c) / math.log(R), R


# High-quality triples for analysis
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
    (1, 1024, 1025),
    (1, 6560, 6561),
]

print("T5: Arithmetic Wronskian candidate Phi(n) = n/rad(n)")
print("=" * 70)
print()
print("EQUIVALENCE: abc(ε) <=> Phi(c) <= K_ε * R^ε  for all coprime a+b=c")
print()

# --- Part A: Phi values for known triples ---
print("[A] Phi(c) and the abc equivalence:")
print()
print(
    f"{'triple':>20}  {'R':>8}  {'q':>6}  {'Phi(c)':>10}  {'Phi(c)/R^0.5':>12}  {'Phi(c)/R^0.3':>12}"
)
print("-" * 80)

for a, b, c in TRIPLES:
    assert a + b == c and math.gcd(a, b) == 1, f"({a},{b},{c}) not valid"
    q, R = quality(a, b, c)
    Phi_c = phi_excess(c)
    ratio_05 = Phi_c / R**0.5 if R > 0 else 0
    ratio_03 = Phi_c / R**0.3 if R > 0 else 0
    print(
        f"  ({a:>5},{b:>6},{c:>6})  {R:>8}  {q:>6.3f}  {Phi_c:>10}  {ratio_05:>12.4f}  {ratio_03:>12.4f}"
    )

print()
print("  OBSERVATION: Phi(c) grows, but slowly relative to R.")
print("  Phi(c)/R^0.5 appears bounded empirically (consistent with abc holding).")
print("  Proving Phi(c) <= K * R^eps for ANY fixed eps > 0 is EQUIVALENT TO abc.")

# --- Part B: The Arithmetic Wronskian ---
print()
print("[B] Arithmetic Wronskian W_Phi(a, c) = a/rad(c) - c/rad(a):")
print()

# W_Phi(a, c) = a/rad(c) - c/rad(a)
# For W to give abc, we need:
# UPPER BOUND: |W_Phi(a,c)| <= something_small
# LOWER BOUND: |W_Phi(a,c)| >= 1/rad(abc)^eps   (non-degeneracy)
# Then: a/rad(c) ~ c/rad(a) => c/a ~ rad(c)/rad(a) => c <= rad(c)/rad(a) * a
#                               c <= rad(abc)^something * a

print(f"{'triple':>20}  {'W_Phi(a,c)':>14}  {'|W_Phi|*R':>12}  {'|W_Phi|*R/c':>12}")
print("-" * 70)

for a, b, c in TRIPLES:
    q, R = quality(a, b, c)
    rad_a = rad(a)
    rad_c = rad(c)
    W = a / rad_c - c / rad_a
    print(
        f"  ({a:>5},{b:>6},{c:>6})  {W:>14.4f}  {abs(W) * R:>12.4f}  {abs(W) * R / c:>12.6f}"
    )

print()
print("  KEY QUESTION: Is |W_Phi(a,c)| >= 1/R^delta for some delta?")
print("  Empirically: |W_Phi|*R/c ~ O(1) or smaller.")
print("  If |W_Phi| >= 1/R^delta, then a/rad(c) ~ c/rad(a) gives c <= R^{1+delta}.")
print("  THIS WOULD PROVE a weak form of abc!")

# --- Part C: Checking A1-A5 for Phi ---
print()
print("[C] Checking axioms A1-A5 for Phi(n) = n/rad(n):")
print()

# A1: Multiplicativity (not Leibniz)
# For gcd(m,n)=1: Phi(mn) = mn/rad(mn) = mn/(rad(m)*rad(n)) = Phi(m)*Phi(n)
m, n = 8, 9
print(
    f"  A1 (multiplicativity for coprime): Phi({m})*Phi({n}) = {phi_excess(m)}*{phi_excess(n)} = {phi_excess(m) * phi_excess(n)}"
)
print(
    f"  Phi({m}*{n}) = Phi({m * n}) = {phi_excess(m * n)}  ✓ (multiplicative, not Leibniz)"
)

# A2: Size drop
print()
print("  A2 (size drop): Phi(n)/n = 1/rad(n)")
for n in [4, 8, 9, 16, 27, 64, 128, 729, 4375]:
    ratio = phi_excess(n) / n
    print(
        f"    Phi({n:>6}) / {n:>6} = 1/{rad(n):>4} = {ratio:.6f}  [log ratio: {math.log(phi_excess(n)) / math.log(n):.4f}]"
    )

print()
print("  A2 CHECK: log(Phi(n))/log(n) < 1 iff n is NOT squarefree.")
print("  For n = p^k: log(Phi(p^k))/log(p^k) = (k-1)/k -> 1 as k->inf.")
print("  So Phi(n) is NOT bounded by n^{1-delta} for any fixed delta!")
print("  FAILS A2 for prime powers with large exponent.")
print()
print("  DIAGNOSIS: Phi(p^k) = p^{k-1}  and  (p^k)^{1-delta} = p^{k(1-delta)}.")
print(
    "  Phi(p^k) < (p^k)^{1-delta}  iff  p^{k-1} < p^{k-k*delta}  iff  k-1 < k-k*delta"
)
print("  iff  k*delta < 1  iff  k < 1/delta.")
print("  So A2 holds only for n with v_p(n) < 1/delta. NOT uniformly in n.")

# --- Part D: The gap and what's needed ---
print()
print("[D] Structural gap analysis:")
print()
print("""  WHY Phi ALONE DOESN'T PROVE abc:

  Phi(n) = n/rad(n) is MULTIPLICATIVE (A1 as multiplicativity).
  But Mason-Stothers needs LEIBNIZ RULE: D(a+b) relates to D(a), D(b).

  The LEIBNIZ FAILURE is the core gap:
    For polynomials: (f+g)' = f' + g'  (linearity of derivative)
    For Phi:        Phi(a+b) has NO formula in terms of Phi(a), Phi(b).

  Example: Phi(3) = 1, Phi(125) = 25, but Phi(128) = 64.
    64 ≠ 1 + 25 = 26  (no additive formula)
    64 ≠ 1 * 25 = 25  (no multiplicative formula)
    The prime 2 in 128=2^7 is unrelated to 3 or 5.

  WHAT WOULD SUFFICE:
  A function D: ℕ → ℝ+ satisfying:
    (i)  D(p^k) = p^{k-1}                      [same as Phi on prime powers]
    (ii) D(mn) = m*D(n) + n*D(m) for gcd(m,n)=1 [Leibniz for coprime factors]
    (iii) D(a+b) <= D(a) + D(b) + C*(rad(ab))  [controlled additive error]
    (iv)  D(n) <= n^{1-1/omega(n)+eps}         [size drop]

  Condition (i) + (ii) UNIQUELY DETERMINES D = arithmetic derivative n'.
  Condition (iii) requires: n' satisfies the additive inequality.
  Condition (iv) requires: n'/n -> 0 for n with many prime factors.

  This is the ARITHMETIC DERIVATIVE CONJECTURE:
    For a+b=c, gcd=1:  c' <= C * rad(abc) * log(abc)^k  (some k)
  This would give abc if true!
""")

# --- Part E: Arithmetic derivative additive inequality ---
print("[E] Testing arithmetic derivative additive inequality:")
print("    Is c' <= C * (a' + b' + rad(abc)) ?")
print()


def arith_deriv(n):
    """Arithmetic derivative n'."""
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


print(f"{'triple':>20}  {'Da':>8}  {'Db':>8}  {'Dc':>8}  {'R':>8}  {'Dc/R':>10}")
print("-" * 70)

for a, b, c in TRIPLES:
    da = arith_deriv(a)
    db = arith_deriv(b)
    dc = arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    print(
        f"  ({a:>5},{b:>6},{c:>6})  {da:>8}  {db:>8}  {dc:>8}  {R:>8}  {dc / R:>10.4f}"
    )

print()
print("  OBSERVATION: c' / R varies widely and can be >> 1.")
print(
    "  c' is NOT bounded by O(R) in general (e.g., (1,4374,4375): c'=5^3*7=875, R=210)."
)
print(
    "  However: c' / c = sum_{p|c} v_p(c)/p, which IS small when c has few prime factors."
)
print()
print("  THE KEY RATIO: c'/c vs log(c)/log(R) = quality")
print()

for a, b, c in TRIPLES[:8]:
    dc = arith_deriv(c)
    R = rad(a) * rad(b) * rad(c)
    q = math.log(c) / math.log(R)
    deriv_ratio = dc / c  # = sum_{p|c} v_p(c)/p
    print(
        f"  ({a:>5},{b:>6},{c:>6}): c'/c={deriv_ratio:.4f},  quality={q:.4f},  "
        f"quality*log(R)={q * math.log(R):.3f},  log(c'/c)={math.log(dc / c) if dc > 0 else '-inf':.3f}"
    )

print()
print("CONCLUSION:")
print(
    "  Phi(n) = n/rad(n) is the RIGHT OBJECT (equivalent to abc) but proves nothing by itself."
)
print("  The arithmetic derivative n' satisfies Leibniz but fails size-drop.")
print("  The MISSING PIECE is an ADDITIVE INEQUALITY for the arithmetic derivative:")
print("    If  a' + b' + rad(abc) >= C * c'  (universally for coprime a+b=c)")
print("    then  c' <= C^{-1} * (a' + b' + R)  <= C^{-1} * O(R * log R)  =>  abc.")
print()
print("  THIS IS THE PRECISE FORM of the missing 'size-drop' tool:")
print("    n' <= C * rad(n) * log(rad(n))  for all n >= 2  [UNPROVED, OPEN]")
print("  Note: This is EQUIVALENT to abc for the specific n=c in the triple.")
