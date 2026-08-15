# Problem OB-10 — Non-degenerate Minkowski bound for Pasten's lattice (squarefree ω=3)

**Type:** Lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter K_ε are not used or assumed anywhere in this
problem. The result concerns structural properties of integer lattices attached to
coprime triples.

---

## All definitions (self-contained — everything is here)

### 1. Setup

Fix a squarefree coprime triple (a, b, c) with a + b = c, and ω(abc) = 3.  
**Squarefree** means every prime appears to the first power in a, b, c.  
**ω(abc) = 3** means abc has exactly three distinct prime factors.  
Write P = {p₁, p₂, p₃} for those primes and R = p₁p₂p₃ = rad(abc).

### 2. The Pasten lattice

For weights ψ: P → ℤ, define d^ψ(n) = n · ∑_{p|n} v_p(n)/p · ψ(p)
(where v_p(n) is the p-adic valuation; = 1 for all p ∈ P since squarefree).

The **Pasten lattice** is:
```
F(a,b) = { ψ ∈ ℤ³  |  d^ψ(a) + d^ψ(b) = d^ψ(c) }
```
This is a sublattice of ℤ³ of rank 2 (since ω − 1 = 2).

The additivity constraint reduces to: ∑_{p ∈ P} c_p · ψ(p) = 0  
where c_p = +R/p for p ∈ P_a ∪ P_b, c_p = −R/p for p ∈ P_c.

### 3. The Wronskian

For ψ ∈ F(a,b), define the **Wronskian**:
```
W^ψ(a,b) = ab · ( ∑_{p|b} ψ(p)/p  −  ∑_{p|a} ψ(p)/p )
```
A nonzero ψ ∈ F(a,b) is **non-degenerate** if W^ψ(a,b) ≠ 0.

### 4. The degenerate sublattice

```
L₀ = { ψ ∈ F(a,b)  |  W^ψ(a,b) = 0 }
```
L₀ is a sublattice of F(a,b) of rank 1 (defined by two constraints in ℤ³).

### 5. Minkowski bound (admitted as axiom in Lean formalization)

For a rank-r integer lattice L with det(L) > 0, there exists a nonzero ψ ∈ L with
‖ψ‖_∞ ≤ det(L)^{1/r}. (Minkowski + Vaaler 1979 for ambient coordinates; see OB-09.)

### 6. Determinant bound (proved in OB-09 and Lean)

For squarefree coprime (a,b,c) with ω = 3:
```
det(F(a,b)) = R · √(∑_{p ∈ P} 1/p²)  <  R.
```

---

## The claims to be verified

### Theorem A — Non-degeneracy for a ≥ 2

For squarefree coprime (a,b,c) with ω = 3 and **a ≥ 2** (equivalently: a, b, c are all prime):

> The generator of L₀ has ‖gen(L₀)‖_∞ = 2c > λ₁(F(a,b)).  
> Consequently, the minimum-norm nonzero vector in F(a,b) is non-degenerate.  
> Combined with det(F(a,b)) < R: there exists a non-degenerate ψ with ‖ψ‖_∞ < R^{1/2}.

### Theorem B — Non-degenerate bound for a = 1

For squarefree coprime (1, b, c) with b = pq (p < q prime) and c = pq+1 prime,
and ω = 3:

> The minimum non-degenerate vector in F(1,b) has ‖ψ‖_∞ = c.  
> Ratio: ‖ψ_nd‖_∞ / R^{1/2} = √(c/(pq)) = √(1 + 1/(pq)) ≤ √(7/6) < 1.09.

### Corollary — Universal squarefree ω=3 bound

For ALL squarefree coprime (a,b,c) with ω = 3:

> ∃ non-degenerate ψ ∈ F(a,b) with ‖ψ‖_∞ ≤ √(7/6) · R^{1/2}.

---

## Proof skeleton to be closed

### Step 1 — Why a ≥ 2 implies a, b, c all prime (for squarefree ω=3)

With ω = 3 and squarefree: P = {p₁,p₂,p₃}, each prime divides exactly one of a,b,c.

If a has two prime factors p₁,p₂ (i.e. a = p₁p₂): then c = p₁p₂ + b, and c must be a product of primes from {p₁,p₂,p₃} only (squarefree). This forces b = 1 (verified by case analysis: all other partitions lead to contradictions). In canonical form a ≤ b: b ≥ p₁p₂ > 1 = a, so a = 1.

Therefore: a ≥ 2 ↔ each of a,b,c is a prime in P.

**What to close:** Confirm the case analysis ruling out |P_a|=2 with b≥2 for squarefree ω=3.

### Step 2 — Compute the generator of L₀ for a ≥ 2

With a, b, c prime and partition P_a={a}, P_b={b}, P_c={c}:

Additivity: (R/a)ψ_a + (R/b)ψ_b = (R/c)ψ_c → bc·ψ_a + ac·ψ_b = ab·ψ_c.  
Wronskian = 0: b·ψ_a − a·ψ_b = 0 → ψ_b = (b/a)·ψ_a.

For integer solutions: a | ψ_a. Set ψ_a = ak, ψ_b = bk.  
Substitute: 2abc·k = ab·ψ_c → ψ_c = 2ck.

**Generator of L₀: (a, b, 2c), with ‖gen‖_∞ = 2c.**

### Step 3 — Prove λ₁(F(a,b)) < 2c

λ₁(F(a,b)) ≤ det(F(a,b))^{1/2} < R^{1/2} = √(abc).

Is √(abc) < 2c?  
⟺ abc < 4c² ⟺ ab < 4c = 4(a+b).

With a = 2 (required by parity: a+b=c prime, so one of a,b must be 2):  
2b < 4(2+b) = 8+4b → 0 < 8+2b. ✓ for all b ≥ 1.

**What to close:** Confirm the arithmetic inequality for all prime pairs (a,b) = (2,b).

### Step 4 — Prove Theorem B for a = 1

With a = 1, b = pq, c = pq+1 = r prime, P_b = {p,q}, P_c = {r}:

Wronskian(1,pq): W = pq·(ψ_p/p + ψ_q/q) = q·ψ_p + p·ψ_q.  
L₀ (W=0): ψ_p = pk, ψ_q = −qk. Substitute in additivity → ψ_r = 0.  
**L₀ generator: (p, −q, 0), ‖gen‖_∞ = q < r.**

So the shortest vector (p,−q,0) with norm q IS in L₀ — degenerate.  
The shortest NON-DEGENERATE vector: try ψ = (0, q, r). W = p·q ≠ 0. ‖ψ‖_∞ = r. ✓  
Is there a shorter non-degenerate vector? Any non-degenerate ψ must have ψ_r ≠ 0 (from the explicit parametrization of F(1,pq)); and the additivity forces |ψ_r| ≥ r/pq · min(pq/p, pq/q)... confirm ‖ψ_nd‖_∞ = r.

**What to close:** Prove that no non-degenerate vector has ‖ψ‖_∞ < r for the (1,pq,r) family.

---

## Acceptance criteria

**CONFIRMED:** Both theorems verified with complete proofs.  
**PARTIAL:** One theorem verified; other needs more work (specify which step).  
**REFUTED:** Explicit counterexample (a squarefree ω=3 triple violating the stated bound).  
**INCONCLUSIVE:** Identify precisely which step is unresolved.

---

## Numerical anchor (sanity only — not an input to the proof)

```python
import math

def gcd(a,b):
    while b: a,b=b,a%b
    return a

# Case a>=2: (2,3,5)
a,b,c = 2,3,5
R = a*b*c  # = 30
print(f"(2,3,5): L0 generator norm = 2c = {2*c}, R^0.5 = {R**0.5:.3f}")
# => L0 generator norm = 10 > sqrt(30) ≈ 5.48. Shortest vector (norm 3) < 10. ✓

# Case a=1: (1,6,7)
a,b,c = 1,6,7
p,q = 2,3  # b = p*q = 6
r = c       # = 7
R = p*q*r   # = 42
ratio = (r/(p*q))**0.5
print(f"(1,6,7): norm_nd = {r}, R^0.5 = {R**0.5:.3f}, ratio = {ratio:.4f}")
# => ratio = sqrt(7/6) ≈ 1.0801

# Universal bound
print(f"Universal upper bound: sqrt(7/6) = {(7/6)**0.5:.4f}")
```

Expected output:
```
(2,3,5): L0 generator norm = 2c = 10, R^0.5 = 5.477
(1,6,7): norm_nd = 7, R^0.5 = 6.481, ratio = 1.0801
Universal upper bound: sqrt(7/6) = 1.0801
```

---

*Prepared 2026-08-15. Non-circularity: no abc triples, no fitted K_ε, no Szpiro.*  
*PROMPT_LINT checks (A1–A5): no abc assumed; universality holds over all squarefree ω=3;*  
*no Wronskian identification-without-proof; no Szpiro; no IUT.*
