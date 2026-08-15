"""
T2 — Szpiro equivalence: height ratio and what it implies for M2 (discovery tier)

Uses the OB-04 bounds (proved in Lean 4) to compute, for each coprime triple,
the "Szpiro ratio" log|Δ_min| / log N_E and show what fixed-power bound
this would give if a Szpiro-type inequality could be proved.

KEY INSIGHT: M2 (abc) ↔ Szpiro's conjecture via the Frey curve.
  Szpiro: |Δ_min(E)| ≤ K_ε · N(E)^{6+ε} for all E/Q
  Frey:   |Δ_min| ~ (abc)^2,  N_E ~ rad(abc)
  → (abc)^2 ≤ K · rad(abc)^{6+ε}
  → since c ≤ abc ≤ c^3:  c^2 ≤ (abc)^2 ≤ K · R^{6+ε}
  → c ≤ K^{1/2} · R^{3+ε/2}  (fixed-power A=3)

But abc conjecture says c ≤ K_ε · R^{1+ε}, i.e., A=1.
The gap 3 → 1 is the content of the equivalence: Szpiro with exponent 6
gives A=3, but the EQUIVALENCE shows Szpiro↔abc so both are equally hard.

This toy computes the empirical Szpiro ratio for known triples.

NON-CIRCULARITY: Known triples used for exploration only. No K_ε is fitted.
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


# --- Height bounds from OB-04 (proved in Lean 4) ---
# For Frey curve E_{a,b,c}: a+b=c, gcd(a,b)=1
# |Δ_min| ∈ { 16·(abc)², (abc)²/256 }  [Silverman AEC VIII.11.3(a)]
# N_E = 2^{f2-1} · rad(abc)  with f2 ≤ 8  [Silverman ATEC IV.10.4]
# Bounds (proved in Lean 4):
#   log|Δ_min| ∈ [2 log(abc) - 8 log 2,  2 log(abc) + 4 log 2]
#   log N_E    ≤ log(rad(abc)) + 7 log 2

LOG2 = math.log(2)

print("T2: Szpiro height ratios and implication for M2")
print("=" * 60)
print()
print("PROVED IN OB-04 (Lean 4, zero sorry):")
print("  log|Δ_min| ∈ [2·log(abc) - 8·log2,  2·log(abc) + 4·log2]")
print("  log N_E    ≤  log(rad(abc)) + 7·log2")
print()

# High-quality triples to analyze
TRIPLES = [
    (1, 8, 9),       # q ≈ 1.226
    (1, 80, 81),     # q ≈ 1.292 (81=3^4, 80=2^4·5, rad=30)
    (1, 48, 49),     # 49=7^2, 48=2^4·3, rad=42
    (5, 27, 32),     # q ≈ 1.246
    (1, 2, 3),       # q = 1 exactly (sanity)
    (1, 4374, 4375), # 4374=2·3^7, 4375=5^4·7, rad=210 — high quality
    (2, 6859, 6861), # 6859=19^3, 6861=3·2287? check below
    (1, 728, 729),   # 729=3^6, 728=2^3·7·13, rad=2·3·7·13=546
    (3, 125, 128),   # 128=2^7, 125=5^3, 3 is prime; rad=30
    (32, 49, 81),    # 32=2^5, 49=7^2, 81=3^4; rad=2·3·7=42; q=log81/log42≈1.19
]

print(f"{'triple':>16}  {'R':>6}  {'q':>6}  {'Szpiro_ratio_UB':>16}  {'implied_A':>10}")
print("-" * 70)

for a, b, c in TRIPLES:
    if math.gcd(a, b) != 1:
        print(f"  ({a},{b},{c}): NOT COPRIME, skipping")
        continue
    if a + b != c:
        print(f"  ({a},{b},{c}): a+b≠c, skipping")
        continue

    R = rad(a * b * c)
    abc_prod = a * b * c
    q = math.log(c) / math.log(R)

    # OB-04 bounds:
    log_disc_ub = 2 * math.log(abc_prod) + 4 * LOG2   # upper bound on log|Δ_min|
    log_NE_lb = math.log(R)                             # lower bound on log N_E (no conductor factors)
    log_NE_ub = math.log(R) + 7 * LOG2                 # upper bound on log N_E

    # Szpiro ratio: log|Δ_min| / log N_E
    # Upper bound on ratio:
    szpiro_ratio_ub = log_disc_ub / log_NE_lb

    # What Szpiro exponent A_Szpiro would give:
    # If |Δ| ≤ K · N_E^{A_Szpiro}, then
    # 2·log(abc) ≲ A_Szpiro · log(R) → log(c) ≲ (A_Szpiro/2) · log(R)
    # So implied quality bound = A_Szpiro / 2
    implied_quality_bound = szpiro_ratio_ub / 2

    print(f"  ({a:>4},{b:>5},{c:>5})  "
          f"{R:>6}  {q:>6.3f}  "
          f"{szpiro_ratio_ub:>16.3f}  {implied_quality_bound:>10.3f}")

print()
print("INTERPRETATION:")
print("  'Szpiro_ratio_UB' = upper bound on log|Δ_min|/log N_E for this triple")
print("  'implied_A'       = quality bound this Szpiro ratio would imply if universal")
print()
print("KEY OBSERVATION:")
print("  For high-quality triples (q > 1.2), the empirical Szpiro ratio is ~ 6–8.")
print("  Standard Szpiro conjecture: ratio ≤ 6+ε (conjectured; not proved).")
print("  If Szpiro (exponent 6) were proved: implied quality bound A ≈ 3.")
print("  To reach M2 (A=1+ε): need Szpiro with exponent 2+2ε, or a different route.")
print()
print("CONCLUSION FOR M2:")
print("  The Szpiro route (via Frey curve + OB-04 bounds) gives a strategy:")
print("    PROVE Szpiro(6+ε) → GET  c ≤ K · R^{3+ε/2}  [weaker than M2]")
print("    But Szpiro ↔ abc (equivalence), so Szpiro(6+ε) IS abc in disguise.")
print("  The equivalence (CL-02, [BASE]) shows both conjectures are equally hard.")
print("  No shortcut: proving Szpiro(6) is the SAME difficulty as M2.")
print()
print("HEIGHT RATIO FROM OB-04:")
print("  This is what IS proved (Lean 4, zero sorry):")
print("  log|Δ_min| ≤ 2·log(abc) + 4·log2   (discriminant upper bound)")
print("  log|Δ_min| ≥ 2·log(abc) - 8·log2   (discriminant lower bound)")
print("  log N_E    ≤ log(rad(abc)) + 7·log2 (conductor upper bound)")
print("  These are the HEIGHT FRAMEWORK axioms. They reduce M2 to the Szpiro ratio.")
