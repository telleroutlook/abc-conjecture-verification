# Problem OB-12 — Analytical sharp bounds for universally-bounded Pasten lattice types

**Type:** Integer lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter K_ε are not used or assumed. The result concerns
structural properties of the Pasten lattice defined by the radical of squarefree coprime
triples. No abc-equivalent assumption enters at any point.

---

## All definitions (self-contained — everything is here)

Let (a, b, c) be a squarefree coprime triple with a + b = c, 1 ≤ a ≤ b ≤ c.

**Prime partition:** Let P_a, P_b, P_c denote the sets of prime factors of a, b, c
respectively. These are pairwise disjoint (since gcd(a,b)=gcd(b,c)=gcd(a,c)=1).

**ω:** Total number of distinct primes, ω = |P_a| + |P_b| + |P_c|.

**R = rad(abc):** Product of all distinct prime factors of abc. For squarefree (a,b,c):
R = a · b · c.

**Partition type (n_a, n_b, n_c):** Tuple of prime-set sizes (|P_a|, |P_b|, |P_c|).

**Optimal non-degenerate norm (F10):**
  min_nd_norm = second smallest of {min(P_a), min(P_b), min(P_c)}
where min(∅) = +∞. This equals the second element in the sorted list of the three
group minima. Proved analytically: every cross-group 2-entry φ-vector is non-degenerate
(Wronskian ≠ 0), and the minimum over all such vectors is second_smallest{·,·,·}.

**Ratio:** ρ(a,b,c) = min_nd_norm / R^{1/(ω−1)}.

**Universally bounded type:** A partition type T is universally bounded if
  sup { ρ(a,b,c) : (a,b,c) squarefree coprime, type = T } < ∞.

---

## Status update (2026-08-16): Claims A and B CONFIRMED; Claim C REVISED

**Claim A — Type (0,2,2):** CONFIRMED (F14). Unique max at (1,14,15); ρ = 3·210^{−1/3}.

**Claim B — Type (1,1,2):** CONFIRMED (F14 + T29). sup ρ = 2^{−1/3} ≈ 0.7937.
  - c-even subfamily (a,b both odd primes): nd = a; ρ³ = a²/(b(a+b)) < 1/2 since b>a.
    Sup = 2^{-1/3} as a/b→1 (never achieved). Verified 0 violations for c ≤ 5000.
  - c-odd subfamily (a=2, b odd prime, c=2+b=r₁r₂): nd = r₁ always (proved: r₁ < b).
    ρ³ ≤ √(2+b)/(2b) → 0. Finite max = 0.4106 at (2,13,15). All < 2^{-1/3}.

**Claim C — REVISED (2026-08-16):**
  - Type (1,2,2): ρ → 0 ✓. nd is bounded (equal to a fixed small prime) while
    R → ∞, so ρ → 0. Finite max ≈ 0.4327 at (2,33,35).
  - Type (2,1,2): **ρ does NOT go to 0.** The family a=6, b=q (prime), c=6+q (near-
    balanced semiprime) gives nd = min(Pc) ≈ √q and R ≈ 6q², so
    ρ ≈ √q / (6q²)^{1/4} = 1/6^{1/4} ≈ 0.6389.
    sup ρ = 1/6^{1/4} (approached, never achieved). Verified: ρ reaches 0.6357 at
    (6, 36857, 36863) = (6, 36857, 191·193).
  - Type (2,2,1): **ρ does NOT go to 0.** The family a=6, b=q₁q₂ (balanced
    semiprime), c=6+q₁q₂ (prime) gives nd = min(Pb) ≈ √b and R ≈ 6b·c ≈ 6b²,
    so ρ → 1/6^{1/4} ≈ 0.6389.
    sup ρ = 1/6^{1/4} (approached, never achieved). Verified: ρ reaches 0.6357 at
    (6, 39203, 39209) = (6, 197·199, 39209).
  **General formula:** for type (2,⋆,⋆) or (⋆,2,⋆) with the 2-prime group having
  product p₁p₂ fixed while b → ∞ via balanced semiprime structure:
    ρ → 1/(p₁p₂)^{1/4}.
  Smallest possible p₁p₂ = 2·3 = 6, giving the universal bound sup ρ ≤ 1/6^{1/4} for
  types (2,1,2) and (2,2,1).

---

## The claims to be proved

From numerical verification (c ≤ 500 for ω≤4; c ≤ 300 for ω=5), seven types are
universally bounded. Type (1,2,1) has an analytical proof (F7a + F12): its supremum
is exactly 2^{−1/3} ≈ 0.7937, sharp. The remaining six types have only numerical bounds:

**Claim A — Type (0,2,2), ω=4:**
  sup ρ = 3 · 210^{−1/3} ≈ 0.5047
achieved uniquely at (a, b, c) = (1, 14, 15).
  
  More precisely: for all squarefree coprime (a,b,c) with type (0,2,2) (a=1, b=p₁p₂,
  c=q₁q₂ with p₁<p₂ and q₁<q₂ primes), we have ρ(a,b,c) ≤ 3·210^{-1/3},
  with equality iff (a,b,c) = (1,14,15).

**Claim B — Type (1,1,2), ω=4:**
  sup ρ ≤ 0.773 (numerical; exact supremum unknown; may be irrational).
  Characterize: does ρ → 0 as the triple grows, and what is the exact supremum?

**Claim C — Types (1,2,2), (2,1,2), (2,2,1), ω=5 (REVISED 2026-08-16):**
  - Type (1,2,2): ρ → 0. Prove analytically. Numerical max ≈ 0.433 at (2,33,35).
  - Type (2,1,2): sup ρ = 1/6^{1/4} ≈ 0.6389 (limit, not achieved). The original claim
    "ρ→0" is **wrong**. Prove: sup ρ = 1/(min(a))^{1/4} where min(a) = p₁p₂ is the
    2-prime group product, minimized at p₁p₂=6. Numerical evidence: ρ reaches 0.6357.
  - Type (2,2,1): sup ρ = 1/6^{1/4} ≈ 0.6389 (limit, not achieved). Same analysis.
    Numerical evidence: ρ reaches 0.6357.

---

## Proof sketch for Claim A (to be closed)

For squarefree type (0,2,2): a=1, b=p₁p₂, c=q₁q₂ (p₁<p₂, q₁<q₂ primes distinct from
p₁,p₂). Constraint: 1 + p₁p₂ = q₁q₂.

By F10: min_nd_norm = second_smallest{+∞, p₁, q₁} = max(p₁, q₁) (since +∞ is largest).

Case p₁ ≤ q₁ (nd = q₁): ρ³ = q₁³/(p₁p₂q₁q₂) = q₁²/(p₁p₂q₂).
  From 1+p₁p₂=q₁q₂: q₂=(1+p₁p₂)/q₁.
  ρ³ = q₁³/(p₁p₂(1+p₁p₂)).

**Step A1:** Bound q₁ ≤ √(q₁q₂) = √(1+p₁p₂).
**Step A2:** So ρ³ ≤ (1+p₁p₂)^{3/2}/(p₁p₂(1+p₁p₂)) = √(1+p₁p₂)/(p₁p₂).
  Let N = p₁p₂: ρ³ ≤ √(1+N)/N = √(1/N + 1/N²).
  For N → ∞: ρ³ → 0. So ρ → 0 for large triples.

**Step A3 (to close):** Find the maximum of √(1+N)/N over valid N = p₁p₂ with
  p₁ < p₂ prime, (1+N) = q₁q₂ squarefree product of two primes, and p₁ ≤ q₁.
  **Claim:** Maximum is at (p₁,p₂) = (2,7), N=14, 1+14=15=3·5.
  Then ρ³ = 27/(14·15) = 27/210, ρ = (27/210)^{1/3} = 3/210^{1/3} ≈ 0.5047. ∎ (if proved)

  Note: This requires checking finitely many small cases (N ≤ C for some C derivable
  from the bound √(1+N)/N ≤ ρ_max) plus showing N→∞ gives ρ→0.

**What to close for Claim A:**
- Verify Step A3: confirm (2,7) is the unique maximizer. This requires either a finite
  computer verification (N ≤ 105, after which √(1+N)/N < (27/210)^{1/3}) or an analytic
  argument showing the first valid N with p₁=2 is N=14 and all larger give smaller ρ.
- Handle the case p₁ > q₁ (nd = p₁): by symmetry/analogous argument.

---

## Proof sketch for Claim C (ρ → 0 for ω=5 balanced types)

For type (1,2,2): a=p, b=q₁q₂, c=r₁r₂ (all distinct primes). Constraint: p+q₁q₂=r₁r₂.
min_nd_norm = second_smallest{p, q₁, r₁} = middle element (after sorting).

**Key:** All three group minima are at most (r₁r₂)^{1/2} ≤ c^{1/2} (since group minima are
single primes ≤ √(their product)). The second smallest is ≤ c^{1/2}.
Meanwhile R = p·q₁q₂·r₁r₂ ≥ p·q₁q₂·r₁r₂. For fixed smallest primes and large triples,
R^{1/4} grows while the second_smallest stays bounded (it's constrained by the primes
already appearing). Show: ρ = nd/R^{1/4} → 0 as triple grows.

**What to close for Claim C:**
- Exhibit an explicit growing subfamily for type (1,2,2) (e.g., a=p, b=2·q, c=3·r with
  p+2q=3r, p prime growing) and show ρ → 0 in this family.
- Show ρ is bounded: no type (1,2,2) squarefree triple with ρ > C for C = 0.5.

---

## Acceptance criteria

1. **CONFIRMED:** Full analytical proof of Claim A (exact supremum 3·210^{-1/3} at (1,14,15)).
2. **CONFIRMED:** Analytical proof that ρ → 0 for types (1,2,2), (2,1,2), (2,2,1) ω=5.
3. **PARTIAL:** Numerical verification of Claims B/C up to c ≤ 10000 with explicit bound.
4. **REFUTED:** Counterexample to any stated bound (a squarefree coprime triple of the stated
   type with ratio exceeding the claimed sup).
5. **INCONCLUSIVE + localization:** Precise characterization of why the proof attempt fails
   and which step requires additional ideas.

---

## Numerical anchor (sanity only, not an input to the proof)

Type (0,2,2) worst case: a=1, b=14, c=15.
  R = 2·3·5·7 = 210, ω=4, nd=3, ρ = 3/210^{1/3} = 3/5.9439... = 0.50468...
  Check: 1 + 14 = 15. ✓ Both b=14=2·7 and c=15=3·5 squarefree with 2 prime factors. ✓
  Second_smallest{+∞, 2, 3} = 3. ✓

Type (1,2,1) sharp case (F12, for reference): a=223, b=226=2·113, c=449 (prime).
  R = 2·113·223·449 = 22,649,758, ω=4, nd=223, ρ = 223/22649758^{1/3} = 0.78841.
  Bound: 2^{-1/3} = 0.79370. Gap = 0.00529. ✓

Script to verify: `discovery/m2_directions/t23_complete_classification.py`
