# Problem OB-09 — Minkowski bound for the Pasten lattice (squarefree subfamily)

**Type:** Lattice geometry / elementary algebraic number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter K_ε are not used or assumed anywhere in this
problem. The result concerns a purely structural property of integer lattices attached
to coprime triples.

---

## All definitions (self-contained — everything is here)

### 1. Setup

Fix a triple of positive coprime integers (a, b, c) with a + b = c.  
Assume (a, b, c) is **squarefree**: every prime appears to the first power in a, b, c.  
Since gcd(a, b) = 1 and a + b = c, the prime supports of a, b, c are pairwise disjoint.

Write P = P_a ∪ P_b ∪ P_c for the set of all primes dividing abc. Set ω = |P| = ω(abc).  
The **radical** of abc is R = rad(abc) = ∏_{p ∈ P} p.  
(For squarefree (a, b, c): R = abc exactly.)

### 2. The Pasten lattice

Following Pasten (2021), arXiv:2106.16165, define the **universal arithmetic derivative**
with weights ψ ∈ ℤ^P by:

    d^ψ(n)  =  n · ∑_{p | n} v_p(n) / p · ψ(p)

where v_p(n) = exponent of p in n.

The **additivity constraint** d^ψ(a) + d^ψ(b) = d^ψ(c) becomes (since P_a, P_b, P_c are
disjoint):

    ∑_{p ∈ P_a} v_p(a)/p · ψ(p)  +  ∑_{p ∈ P_b} v_p(b)/p · ψ(p)
      =  ∑_{p ∈ P_c} v_p(c)/p · ψ(p)

**For squarefree (a, b, c): v_p(n) = 1 for all p | n.** The constraint simplifies to:

    ∑_{p ∈ P_a} ψ(p)/p  +  ∑_{p ∈ P_b} ψ(p)/p  =  ∑_{p ∈ P_c} ψ(p)/p      (*)

The solution set F(a, b) = {ψ ∈ ℤ^P : (*) holds} is a sublattice of ℤ^P of rank ω − 1.

### 3. Integer coefficient form

Multiply (*) by D = lcm(p : p ∈ P) = ∏_{p ∈ P} p = R (squarefree).  
The constraint becomes the single integer linear equation:

    ∑_{p ∈ P} c_p · ψ(p) = 0

where the integer coefficient vector **c** ∈ ℤ^P is:

    c_p  =  +R/p    for p ∈ P_a ∪ P_b   (left-hand side primes)
    c_p  =  −R/p    for p ∈ P_c         (right-hand side primes)

### 4. Lattice determinant

The lattice L = F(a, b) = {ψ ∈ ℤ^P : c · ψ = 0} has rank ω − 1 as a sublattice of ℤ^P.
Its determinant (volume of fundamental domain in the ambient Euclidean subspace) is:

    det(L)  =  ‖c‖₂ / gcd(c_p : p ∈ P)

where ‖c‖₂ = (∑_{p ∈ P} c_p²)^{1/2} is the Euclidean norm.

### 5. Wronskian non-degeneracy

The **Wronskian** W^ψ(a, b) = ab · (∑_{p ∈ P_b} ψ(p)/p − ∑_{p ∈ P_a} ψ(p)/p) must be
nonzero for ψ to be "non-degenerate." A non-degenerate ψ exists whenever the lattice L
is not contained in the hyperplane {W^ψ = 0} — this holds for coprime a, b ≥ 2.

### 6. Minkowski bound (to be cited as [BASE])

Minkowski's theorem (lattice form, ℓ^∞ version): Let L be a lattice of rank r embedded in
ℝ^r with det(L) > 0. Then L contains a nonzero vector v with

    max_i |v_i|  ≤  det(L)^{1/r}.

*(Source: any standard reference on the geometry of numbers, e.g., Cassels "An Introduction
to the Geometry of Numbers," Theorem I.2.)*

---

## The theorems to be verified

### Theorem A (Determinant bound — the core claim)

For squarefree coprime (a, b, c) with a + b = c and ω = ω(abc) ≥ 2:

    det(L) = R · √(∑_{p ∈ P} 1/p²)  <  R.

### Theorem B (GCD claim — supporting lemma)

With c_p = +R/p for p ∈ P_a ∪ P_b and c_p = −R/p for p ∈ P_c (as in Section 3):

    gcd(|c_p| : p ∈ P) = 1.

### Corollary C (Minkowski bound for ‖ψ‖)

Combining Theorems A and B with Minkowski's theorem:  
The lattice L contains a nonzero vector ψ (possibly degenerate) with

    ‖ψ‖_∞  ≤  det(L)^{1/(ω−1)}  <  R^{1/(ω−1)}.

**Note:** Corollary C gives a nonzero vector in L, but not necessarily non-degenerate
(W^ψ ≠ 0). Whether the shortest non-degenerate vector satisfies the same bound is a
separate question — **not part of the acceptance criteria below.** We ask only for
Theorems A and B.

---

## Proof skeleton to be closed

### Step 1 — Evaluate ‖c‖₂

Since c_p = ±R/p, we have c_p² = (R/p)² = R²/p² for all p ∈ P. Therefore:

    ‖c‖₂² = ∑_{p ∈ P} R²/p²  =  R² · ∑_{p ∈ P} 1/p².

So ‖c‖₂ = R · √(∑_{p ∈ P} 1/p²).

**What to close for Step 1:** This is algebraic. Confirm the formula is correct given
the definitions above.

### Step 2 — Prove gcd(|c_p| : p ∈ P) = 1 (Theorem B)

The values |c_p| = R/p range over {R/p : p ∈ P}.  
Since R = ∏_{q ∈ P} q, we have R/p = ∏_{q ∈ P, q ≠ p} q.

A prime ℓ ∈ P divides gcd iff ℓ | R/p for all p ∈ P.  
But ℓ ∤ R/ℓ (since R/ℓ = ∏_{q ≠ ℓ} q, which does not contain ℓ).  
So no prime divides all values → gcd = 1.

**What to close for Step 2:** Check this argument works for any finite set P of distinct
primes. In particular, confirm the edge cases: |P| = 2 (omega = 2) and |P| = 1 
(degenerate, not applicable since ω ≥ 2).

### Step 3 — Prove ∑_{p prime} 1/p² < 1 (key analytic bound)

We need ∑_{p ∈ P} 1/p² < 1 for any finite set P of primes (since ∑_P ≤ ∑_{all primes} 1/p²).

Elementary bound: the prime sum is dominated by the integer sum.

    ∑_{p prime} 1/p²  ≤  1/4 + 1/9 + ∑_{n=5}^{∞} 1/n²

The tail integral: ∑_{n=5}^{∞} 1/n² ≤ ∫_{4}^{∞} 1/x² dx = 1/4.

So ∑_{p prime} 1/p² ≤ 1/4 + 1/9 + 1/4 = 0.25 + 0.111 + 0.25 = 0.611 < 1. ✓

**What to close for Step 3:** Confirm the integral bound is valid (the sum starts at n=5,
and ∑_{n=5}^∞ 1/n² ≤ ∫_4^∞ 1/x² dx = 1/4 by comparison). Give the explicit constant:

    ∑_{p prime} 1/p²  ≤  11/18  <  1.

(Verified: 1/4 + 1/9 + 1/4 = 9/36 + 4/36 + 9/36 = 22/36 = 11/18 ≈ 0.611.)

### Step 4 — Combine: Theorem A

det(L) = ‖c‖₂ / gcd = ‖c‖₂ (by Step 2)
       = R · √(∑_{p ∈ P} 1/p²) (by Step 1)
       ≤ R · √(11/18) (by Step 3)
       < R · √1 = R.

So det(L) < R. ✓

**What to close for Step 4:** Confirm the chain. Note √(11/18) ≈ 0.782, so we also get
the explicit bound det(L) ≤ (√(11/18)) · R < 0.79 · R.

---

## Acceptance criteria

**CONFIRMED:** All four steps verified; Theorems A and B proved with explicit constants.  
Deliverable: a complete proof with no gaps, specifically:
- The formula det(L) = R · √(∑ 1/p²) (Steps 1–2).
- The bound ∑_{p prime} 1/p² ≤ 11/18 with proof (Step 3).
- The conclusion det(L) < R (Step 4).

**PARTIAL:** Steps 1 and 2 verified; Step 3 needs a different or sharper bound.  
Deliverable: state which bound on ∑ 1/p² is achieved and what constant C it gives
in det(L) ≤ C · R.

**REFUTED:** One of the formulas is wrong. Deliverable: explicit counterexample or
error location (which definition, which step).

**INCONCLUSIVE:** The proof sketch is incomplete; identify precisely which sub-claim
is unresolved and whether it is an open problem or merely requires more work.

---

## Numerical anchor (sanity only — not an input to the proof)

Triple (a, b, c) = (2, 3, 5): squarefree, coprime, 2 + 3 = 5. ω = 3, R = 30.

Integer coefficient vector: **c** = (15, 10, −6) for primes (2, 3, 5).
- c_2 = R/2 = 15, c_3 = R/3 = 10, c_5 = −R/5 = −6.

```python
import math
coeffs = [15, 10, -6]
R = 30
det_L = math.sqrt(sum(x**2 for x in coeffs))  # gcd=1 by Theorem B
print(f"det(L) = sqrt({sum(x**2 for x in coeffs)}) = {det_L:.6f}")
print(f"R = {R}, det(L) < R: {det_L < R}")
print(f"det(L)/R = {det_L/R:.6f}")
print(f"Minkowski bound det(L)^{{1/2}} = {det_L**0.5:.4f}")
```

Expected output:
```
det(L) = sqrt(361) = 19.000000
R = 30, det(L) < R: True
det(L)/R = 0.633333
Minkowski bound det(L)^{1/2} = 4.3589
```

Verification: 15² + 10² + 6² = 225 + 100 + 36 = 361 = 19². det(L) = 19 < 30 = R. ✓  
Minkowski bound on ‖ψ‖_∞ for rank-2 lattice: 19^{1/2} ≈ 4.36.  
Actual minimum ‖ψ‖_∞ = 3 (verified computationally), consistent with the bound.

---

*Prepared 2026-08-15. Non-circularity: no abc triples, no fitted K_ε, no Szpiro.*  
*Run outsource/PROMPT_LINT.md before sending; A1–A10 checks below.*
