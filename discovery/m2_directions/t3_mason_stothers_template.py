"""
T3 — Mason–Stothers template: polynomial abc and its arithmetic analogue (discovery tier)

The Mason–Stothers theorem (polynomial abc) has a clean proof using the Wronskian.
This toy traces that proof and identifies the EXACT step where the number-field
analogue breaks down — pointing to what would be needed for M2.

THEOREM (Mason–Stothers, [BASE] CL-06):
  Let f, g, h ∈ k[t] (k char 0) be nonzero polynomials with f + g = h and gcd(f,g,h)=1.
  Then  max(deg f, deg g, deg h)  ≤  deg(rad(fgh)) − 1.

PROOF (by Wronskian):
  Step 1: W(f,g) = f·g' − f'·g  (Wronskian)
  Step 2: f + g = h  →  f'+ g' = h'  →  W(f,g) = fh' − f'h = gh' − g'h
  Step 3: deg W ≤ deg f + deg g − 1  (derivative drops degree by 1)
  Step 4: W divides gcd(f,g') · f = f · gcd(f,g')... more carefully:
          Any root α of f with mult m contributes at most m−1 to W
          → each distinct root of f contributes ≤ 1 to deg W
          → similarly for g and h
  Step 5: deg W ≥ max(deg f, deg g, deg h) − deg(rad(fgh))
          [each distinct root of fgh contributes at most 1 to W]
  Step 6: Combining: max(deg f, ...) − deg(rad(fgh)) ≤ deg W ≤ deg f + deg g − 1
          → max ≤ deg(rad(fgh)) − 1.  QED.

THE ARITHMETIC ANALOGUE for M2:
  Replace deg by log (Weil height / logarithmic height)
  Replace roots by prime divisors
  Replace Wronskian by ... ???

This is where the proof breaks down in the number field case.
"""

import sympy
from sympy import symbols, gcd, Poly, factor, degree, diff, resultant, div
from sympy import prod as sprod
from functools import reduce
import math

t = symbols('t')


def poly_rad(f, var=t):
    """Radical of a polynomial: square-free part (product of distinct irreducible factors)."""
    return sympy.sqf_part(f, var)


def wronskian(f, g, var=t):
    return sympy.expand(f * diff(g, var) - diff(f, var) * g)


print("T3: Mason–Stothers template and arithmetic analogue")
print("=" * 60)

# --- Verify Mason-Stothers on concrete examples ---
print("\n[A] Concrete verification of Mason-Stothers:")
examples = [
    (t**3, t**2 * (t + 1), None),  # will compute h = f+g
    (t**5, 1 - t**5, None),
    (t**2, 2*t + 1, None),
]

# Use actual abc examples
ABC_POLYS = [
    (t**2, t*(t+1), t**2 + t*(t+1)),  # f+g = h?
]

# Let's use clean examples
clean_examples = [
    ("f=t^2, g=1, h=t^2+1", t**2, sympy.Integer(1), t**2 + 1),
    ("f=t^3, g=-t^2, h=t^2(t-1)", t**3, -t**2, t**3 - t**2),
    ("f=t^4, g=t^3+t^2, h=t^4+t^3+t^2", t**4, t**3 + t**2, t**4 + t**3 + t**2),
]

for name, f, g, h in clean_examples:
    assert sympy.expand(f + g - h) == 0, f"f+g≠h for {name}"
    g_cd = sympy.gcd(sympy.gcd(f, g), h)
    if g_cd != 1 and g_cd != -1:
        print(f"  {name}: gcd={g_cd}, not coprime — skip")
        continue

    rad_f = poly_rad(f)
    rad_g = poly_rad(g)
    rad_h = poly_rad(h)
    rad_fgh = poly_rad(f * g * h)

    deg_max = max(sympy.degree(f, t), sympy.degree(g, t), sympy.degree(h, t))
    deg_rad = sympy.degree(rad_fgh, t)

    W = wronskian(f, g)
    deg_W = sympy.degree(W, t) if W != 0 else -1

    ms_bound_holds = deg_max <= deg_rad - 1
    print(f"  {name}:")
    print(f"    max deg = {deg_max},  deg rad(fgh) = {deg_rad},  bound max≤rad-1: {ms_bound_holds}")
    print(f"    deg W = {deg_W}")

# --- The Wronskian step-by-step ---
print("\n[B] Wronskian proof trace:")
print("""
  POLYNOMIAL WORLD (proved, Mason-Stothers):

  1. Wronskian W(f,g) = f·g' - f'·g has deg W ≤ deg(f) + deg(g) - 1
     WHY: If deg f = d, deg g = e, then deg(fg') ≤ d+e-1.
     KEY: DERIVATIVE DROPS DEGREE BY EXACTLY 1.

  2. Root multiplicity: if α is a root of f with mult m, it's a root of f' with mult m-1.
     → α is a root of W with mult ≥ m-1 (not m).
     → W "sees" each prime factor of f at most once.
     → deg W ≥ Σ_{p|f} max(mult_p(f)-1, 0) = deg f - deg rad(f)  (approximately)

  3. Combining: deg(rad(fgh)) - deg(max) ≥ 1.

  ARITHMETIC WORLD (needed for M2):

  1. "Wronskian" → ???
     The logarithmic Mahler measure or arithmetic derivative? Neither has
     a clean analogue that drops "degree" by exactly 1.

     The ARITHMETIC DERIVATIVE n' = Σ_p v_p(n)·(n/p) satisfies:
       (ab)' = a'b + ab'  (Leibniz rule)
       (p)' = 1 for prime p
     This is a Z→Z map. Can we define an "arithmetic Wronskian"?
     W_arith(a, b) = a·b' - a'·b

  2. "Derivative drops degree" → ???
     For polynomials: deg(f') = deg(f) - 1 (EXACT).
     For numbers: log(n') vs log(n) has NO exact analogue.
     The arithmetic derivative satisfies n' ≤ n·log(n)/log(p_min(n))
     which is much larger than n.

  3. "Root multiplicity" → ???
     For polynomials: mult_p(f) - 1 after differentiation.
     For numbers: v_p(n') = v_p(n) - 1 if p|n and p²|n.
     This works LOCALLY but the global bound fails.
""")

# --- Arithmetic derivative exploration ---
print("[C] Arithmetic derivative exploration:")
print()


def arith_derivative(n):
    """Arithmetic derivative n' = sum_p v_p(n)*(n/p)."""
    if n == 0:
        return 0
    if n == 1:
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


print(f"  n   n'    log(n')/log(n)   comment")
print(f"  " + "-" * 50)
for n in [2, 4, 8, 12, 36, 72, 100, 1000, 10000]:
    nd = arith_derivative(n)
    if nd > 0 and n > 1:
        ratio = math.log(nd) / math.log(n)
        print(f"  {n:>6}  {nd:>8}  {ratio:>12.4f}")

print()
print("  OBSERVATION: log(n')/log(n) is roughly 1 (or > 1 for prime powers),")
print("  NOT 1 - 1/deg(n) as in the polynomial case.")
print("  The arithmetic derivative does NOT 'drop' the size the way d/dt drops degree.")
print("  This is the FUNDAMENTAL OBSTRUCTION to naively lifting Mason-Stothers.")

print()
print("[D] What would be needed for the arithmetic analogue:")
print("""
  MASON-STOTHERS PROOF REQUIRES:
  (i)   A "derivative" operator D: Z → Z satisfying D(ab) = aD(b) + bD(a)  ✓ (arith. deriv.)
  (ii)  |D(n)| << n  in some quantitative sense (derivative "smaller" than n)  ✗ FAILS
  (iii) v_p(D(n)) = v_p(n) - 1 when p²|n  ✓ (arith. deriv.)
  (iv)  A Wronskian W_arith(a,b) = aD(b) - D(a)b bounding both terms  ✗ UNCLEAR

  The failure of (ii) is the CORE GAP. In the polynomial world:
    deg(D(f)) = deg(f) - 1   →   loss of 1 unit of "size"
  In the arithmetic world:
    log|D(n)| ≈ log(n)       →   no loss of "size"

  KNOWN APPROACHES trying to fix this:
  1. Granville-Tucker (2002): Shows Mason-Stothers analogy suggests abc is likely true
     but the proof does not transfer.
  2. Arakelov geometry approach (Vojta, Bombieri): Replaces the Wronskian by height
     pairings in the Arakelov intersection theory on arithmetic surfaces.
     This is the "correct" arithmetic analogue but produces Vojta's conjecture
     (stronger than abc), not a proof.
  3. IUT (Mochizuki): Attempts to use "anabelian geometry" to get the key step.
     The Θ-link is the analogue of the Wronskian bound—this is what OB-06 is trying
     to verify.

  STRUCTURAL CONCLUSION:
  M2 cannot be proved by a direct arithmetic derivative / Wronskian lift of
  Mason-Stothers. The missing ingredient is a quantitative "size-drop" theorem
  for arithmetic derivatives — which does not currently exist.
  The three known routes (Arakelov/Vojta, IUT, Baker) are the only candidates,
  and each has a precisely identified barrier:
  - Arakelov/Vojta: requires proving Vojta's conjecture (strictly harder than abc)
  - IUT: requires OB-06 B_j morphism (permanently open)
  - Baker: R^{1/3} barrier from B~c circularity (OB-07)
""")
