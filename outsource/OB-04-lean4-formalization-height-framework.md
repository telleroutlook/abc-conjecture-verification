# Problem OB-04 — Lean 4 formal verification of the P_height framework (CORE-2)

**Type:** formal verification / Lean 4 + Mathlib4
**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
IUT Corollary 3.12, known abc triples, or any fitted parameter K_ε. All four sub-claims
(A–D) are unconditionally provable from standard arithmetic; the goal is machine-verified
proof artifacts, not new mathematics.

**Dependency:** The ordinary mathematical proofs of OB-04-A through OB-04-D are already
closed in `OB-03-p-height-framework.md` (status: PARTIAL-FORMALIZATION, 2026-08-15).
This problem asks only for Lean 4 / Mathlib4 formalizations.

---

## All definitions (self-contained — everything is here)

**The rad function.** For a non-zero integer n:

    rad(n) = ∏_{p prime, p | n} p

(product of distinct prime factors of |n|, ignoring multiplicities).
Conventions: rad(±1) = 1. Required properties:
- (P1) rad(n) = rad(|n|)
- (P2) rad(p^k) = p for any prime p and any k ≥ 1
- (P3) If gcd(|m|, |n|) = 1 then rad(mn) = rad(m) · rad(n)

**Coprime abc-triple.** Positive integers (a, b, c) with a + b = c and gcd(a, b) = 1.
Write R = rad(abc) = rad(a) · rad(b) · rad(c) (coprimeness makes this a product).

**Parity fact (proved in OB-03).** For any coprime abc-triple: exactly one of a, b, c is
even; a² + ab + b² is always odd (covers both the one-odd/one-even and both-odd cases).

**The Frey curve.** For a coprime triple (a, b, c):

    E_{a,b,c} : y² = x(x − a)(x + b)   over Q.

Exact Weierstrass invariants (no approximation):

    a₁ = a₃ = a₆ = 0,   a₂ = b − a,   a₄ = −ab
    c₄ = 16(a² + ab + b²),   Δ_W = 16(abc)²

**Minimal discriminant (Silverman AEC 2nd ed., Lemma VIII.11.3(a)).** The global minimal
discriminant satisfies:

    |Δ_min(E_{a,b,c})| ∈ { 16(abc)², 2⁻⁸(abc)² }

Consequently (the bound used throughout):

    2 log(abc) − 8 log 2  ≤  log|Δ_min|  ≤  2 log(abc) + 4 log 2.   [★]

Upper bound constant C = (1/3) log 2 is tight (achieved by (1,8,9)).

**Discriminant height.** h_Δ(E) = (1/12) log|Δ_min(E)|. This is NOT the Faltings height.
The Faltings height also contains a complex-period / modular-form Archimedean term that
is NOT uniformly bounded over all elliptic curves (Murty–Pasten, J. Number Theory 133
(2013), Theorem 5.1).

**Conductor.** N_E = 2^{f₂} · ∏_{p | abc, p odd} p with 0 ≤ f₂ ≤ 8
(Silverman ATEC 1994, Theorem IV.10.4). Since exactly one of a, b, c is even,
∏_{p | abc, p odd} p = R/2, giving:

    N_E = 2^{f₂−1} · R   and   log N_E ≤ log R + 7 log 2.

**Quality.** q(a, b, c) = log c / log R.

---

## Allowed prior results (closed list — no other unproved results may be used)

1. **Fundamental theorem of arithmetic** (unique factorization in Z).
2. **Silverman, AEC 2nd ed. (2009), Lemma VIII.11.3(a),(b)** — minimal discriminant and
   odd-prime conductor for Frey curves. No parity assumption in the lemma.
   URL: https://www.math.brown.edu/johsilve/AECHome.html
3. **Silverman, ATEC (1994), Theorem IV.10.4** — local conductor exponent f_p ≤ 2 + 3v_p(3) + 6v_p(2),
   giving f₂ ≤ 8 over Q₂.
   URL: https://www.math.brown.edu/johsilve/ATAECHome.html
4. **Mathlib4 library** (any stable version; cite commit hash or release tag in artifact).
   Relevant namespaces: `Nat.factorization`, `Nat.primeFactors`, `Nat.Coprime`,
   `Nat.Squarefree`, `Real.log`, `Int.gcd`.

---

## The theorem / claim to be verified

Produce Lean 4 + Mathlib4 formal proof artifacts for the following sub-claims:

**OB-04-A (rad function).** Formally verify P1–P3 in Lean 4. Suggested approach:

```lean
def rad (n : ℕ) (hn : 0 < n) : ℕ := n.primeFactors.prod id

theorem rad_prime_pow (p : ℕ) (hp : p.Prime) (k : ℕ) (hk : 0 < k) :
    rad (p ^ k) (Nat.pos_pow_of_pos k hp.pos) = p := by ...

theorem rad_mul_coprime (m n : ℕ) (hm : 0 < m) (hn : 0 < n)
    (hcop : Nat.Coprime m n) :
    rad (m * n) (Nat.mul_pos hm hn) = rad m hm * rad n hn := by ...
```

(Exact statement may use Mathlib4 idioms; what is required is a `#check`-able theorem
with no `sorry` that asserts P1–P3.)

**OB-04-B (discriminant height bound).** Formally verify [★] in Lean 4 for the specific
Weierstrass discriminant Δ_W = 16(abc)² and the two-case minimal discriminant:

```lean
theorem frey_disc_ineq (a b : ℕ) (ha : 0 < a) (hb : 0 < b)
    (hcop : Nat.Coprime a b) :
    let c := a + b; let abc := a * b * c
    2 * Real.log abc - 8 * Real.log 2 ≤ Real.log (16 * abc ^ 2)
    ∧ Real.log (16 * abc ^ 2) ≤ 2 * Real.log abc + 4 * Real.log 2 := by ...
```

NOTE: Silverman VIII.11.3(a) may be admitted as a `theorem` citing its exact source
(not proved from first principles in Lean), and the two-case inequality derived from it
algebraically — which is fully formalizable.

**OB-04-C (conductor bound).** Formally verify log N_E ≤ log R + 7 log 2. Since f₂ ≤ 8
requires Tate algorithm analysis (Silverman ATEC IV.10.4, admissible as a cited axiom),
the formal statement is:

```lean
-- Admitted: frey_f2_le_8 : f₂ ≤ 8  (from Silverman ATEC IV.10.4)
-- Proved: odd-prime conductor formula from Silverman VIII.11.3(b)
theorem frey_conductor_log_bound (a b : ℕ) (ha : 0 < a) (hb : 0 < b)
    (hcop : Nat.Coprime a b) (f2 : ℕ) (hf2 : f2 ≤ 8) :
    let R := rad (a * b * (a + b)) ...
    Real.log (2 ^ (f2 - 1) * R) ≤ Real.log R + 7 * Real.log 2 := by ...
```

**OB-04-D (quality above 1).** Formally verify:

```lean
theorem quality_above_one : Real.log 9 / Real.log 6 > 1 := by
  -- 9 > 6 > 1, so log 9 > log 6 > 0
  norm_num [Real.log_lt_log_iff, Real.log_pos]
```

(1, 8, 9) witnesses this: gcd(1,8) = 1, 1+8 = 9, rad(1·8·9) = rad(72) = 6.)

---

## Proof skeleton to be closed

### Step 1 — OB-04-A in Lean 4

**Approach.** In Mathlib4, `Nat.primeFactors n` is `Finset ℕ`. Define rad via
`.prod id`. Use `Nat.primeFactors_mul_of_coprime` and `Finset.prod_union` for P3.
`Nat.primeFactors_pow` handles P2. P1 is `Nat.primeFactors_abs`.

**Mathlib4 lemmas to look up:** `Nat.Coprime.primeFactors_mul`, `Finset.prod_union`,
`Nat.primeFactors_prime_pow`.

### Step 2 — OB-04-B in Lean 4

**Approach.** The bound [★] for the Weierstrass discriminant Δ_W = 16(abc)² follows
algebraically: log(16(abc)²) = 2 log(abc) + 4 log 2 (this IS the upper bound, as
equality). The lower bound 2 log(abc) − 8 log 2 follows from Silverman's two-case
result (admitted or proved). The formal proof of the algebraic step uses `Real.log_mul`,
`Real.log_pow`.

### Step 3 — OB-04-C in Lean 4

**Approach.** Admit f₂ ≤ 8 and the conductor formula N_E = 2^{f₂−1} R. Then
log(2^{f₂−1} R) = (f₂−1) log 2 + log R ≤ 7 log 2 + log R. This is purely real
arithmetic, fully formalizable with `Real.log_pow`, `Real.log_mul`.

### Step 4 — OB-04-D in Lean 4

**Approach.** Reduce to `9 > 6`, hence `Real.log 9 > Real.log 6 > 0`, hence ratio > 1.
`norm_num` or `native_decide` should close this after establishing `Real.log_lt_log`.

---

## Acceptance criteria

1. **COMPLETE-FORMAL**: All four sub-claims proved in Lean 4 with zero `sorry`. Deliverable:
   `.lean` file(s) with theorem names, Mathlib4 version/commit hash, and a `lake build`
   command that succeeds with no errors.

2. **PARTIAL-FORMAL**: Some sub-claims proved; others reduced to admitted axioms with
   exact theorem numbers (Silverman VIII.11.3(a/b), ATEC IV.10.4). Each `sorry` or `axiom`
   must be labeled with exact paper, theorem number, and page.

3. **INCONCLUSIVE + LOCALIZATION**: A precise statement of which Mathlib4 lemma is missing
   or which intermediate step would require formalizing all of Silverman from scratch —
   with the exact missing lemma name.

**Not accepted:** Informal proofs. The ordinary mathematics is already closed in OB-03;
this problem asks only for machine artifacts.

---

## Numerical anchor (sanity only — not an input to the proof)

For (a, b, c) = (1, 8, 9): gcd(1,8) = 1, 1+8 = 9. ✓

- R = rad(1·8·9) = rad(72) = 2·3 = 6.
- Δ_W = 16(72)² = 82944 = 2¹⁰·3⁴. Model globally minimal (v₂ = 10 < 12, v₃(c₄) = 0).
- log|Δ_min| = log(82944). [★] upper bound RHS = 2·log(72) + 4·log(2) = log(82944). Tight. ✓
- h_Δ = (1/12)·log(82944) = 0.943826746689324…  (NOT the Faltings height)
- N_E = 48 = 2⁴·3. log(48) ≤ log(6) + 7·log(2)?  3.871 ≤ 1.792 + 4.852 = 6.644  ✓
- q = log(9)/log(6) = 1.226… > 1.  ✓

```python
import math
a, b, c = 1, 8, 9
abc_val = a * b * c          # 72
R = 6
Delta_min = 82944            # = 16 * 72^2 = 2^10 * 3^4
h_Delta = math.log(Delta_min) / 12
bound_B_rhs = math.log(abc_val) / 6 + math.log(2) / 3
bound_B_lhs = math.log(abc_val) / 6 - 8 * math.log(2) / 12
N_E = 48
conductor_bound_rhs = math.log(R) + 7 * math.log(2)
assert abs(h_Delta - bound_B_rhs) < 1e-12, f"h_Delta={h_Delta} vs rhs={bound_B_rhs}"
assert math.log(N_E) <= conductor_bound_rhs + 1e-12
assert math.log(9) / math.log(6) > 1
print(f"h_Delta = {h_Delta:.15f}")
print(f"[★] upper bound RHS = {bound_B_rhs:.15f}  (tight: equal)")
print(f"[★] lower bound LHS = {bound_B_lhs:.15f}")
print(f"log N_E = {math.log(N_E):.6f} <= log R + 7 log 2 = {conductor_bound_rhs:.6f}")
print(f"q = {math.log(9)/math.log(6):.15f} > 1")
```

Expected output:
```
h_Delta = 0.943826746689324
[★] upper bound RHS = 0.943826746689324  (tight: equal)
[★] lower bound LHS = 0.250679566129379
log N_E = 3.871201 <= log R + 7 log 2 = 6.643790
q = 1.226294385530917 > 1
```
