# Problem OB-10 — Non-degeneracy theorem for a ≥ 2 in the Pasten lattice

**Type:** Integer lattice geometry / elementary algebraic number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter K_ε are not used or assumed. The result concerns
a structural property of the Pasten lattice for squarefree triples.

---

## All definitions (self-contained)

### 1. Setup

Fix a squarefree coprime triple (a, b, c) with a + b = c, a ≥ 2, and ω(abc) = 3.
Let P = {p, q, r} be the three distinct primes dividing abc.
Since (a, b, c) is squarefree and gcd(a,b) = 1 with a+b=c, the prime supports
P_a, P_b, P_c are pairwise disjoint.

For ω = 3 squarefree and a ≥ 2, there is exactly one prime in each of Pa, Pb, Pc:

    Pa = {p},  Pb = {q},  Pc = {r}

with a = p, b = q (both prime), c = r = p + q (prime). (Other partitions with a ≥ 2
require a to have ≥ 2 prime factors, giving ω ≥ 4; for ω = 3, a ≥ 2 forces a = p prime.)

**Remark on partition.** For ω = 3 squarefree coprime (a,b,c):
- |Pa|=0, |Pb|=2, |Pc|=1 or |Pa|=0, |Pb|=1, |Pc|=2 ↔ a = 1
- |Pa|=1, |Pb|=1, |Pc|=1 ↔ a ≥ 2 (a is prime)

### 2. Integer coefficient form of the Pasten lattice

The additivity constraint D^ψ(a) + D^ψ(b) = D^ψ(c) becomes (for squarefree, v_p=1):

    c_p · ψ_p  +  c_q · ψ_q  +  c_r · ψ_r  =  0

where R = pqr and:

    c_p = +R/p = qr,    c_q = +R/q = pr,    c_r = −R/r = −pq.

So the lattice is:

    L = { ψ = (ψ_p, ψ_q, ψ_r) ∈ ℤ³  |  qr·ψ_p + pr·ψ_q − pq·ψ_r = 0 }

This has rank 2 and det(L) = ‖c‖₂ = √(q²r² + p²r² + p²q²).

### 3. The Wronskian

The Wronskian non-degeneracy condition is:

    W^ψ(a, b) = ab · (ψ_q/q − ψ_p/p)  =  ab/(pq) · (p·ψ_q − q·ψ_p).

Since ab > 0, W^ψ ≠ 0  iff  p·ψ_q ≠ q·ψ_p.

### 4. Degenerate sublattice

The degenerate sublattice L₀ = {ψ ∈ L : W^ψ = 0} consists of:

    ψ ∈ L  with  p·ψ_q − q·ψ_p = 0,
    i.e.,  ψ_p = p·t,  ψ_q = q·t  for some t ∈ ℤ.

Substituting into the lattice constraint:
    qr·(pt) + pr·(qt) − pq·ψ_r = 0
    2pqrt = pq·ψ_r
    ψ_r = 2rt.

Generator of L₀: **v₀ = t·(p, q, 2r)**, norm ‖v₀‖_∞ = max(p, q, 2r) = **2r** (since r = p + q > p, q).

---

## The theorem to be verified

### Theorem E10 (Main claim)

For ω = 3 squarefree coprime (a, b, c) with a + b = c and a ≥ 2 (equivalently, a is prime),
the minimum-norm nonzero vector in L = F(a, b) is non-degenerate.

Equivalently: **the shortest nonzero vector in L has ‖ψ‖_∞ < ‖v₀‖_∞ = 2r**.

---

## Proof skeleton

### Step 1 — Classify all minimum-norm lattice vectors

From qr·ψ_p + pr·ψ_q = pq·ψ_r:
Since gcd(r, pq) = 1, we need r | ψ_r.  Let ψ_r = r·s (s ∈ ℤ, s ≠ 0 for nonzero ψ).

Then: q·ψ_p + p·ψ_q = pq·s.

For s = 1 (smallest positive): q·ψ_p + p·ψ_q = pq.

**Two explicit minimum solutions:**
- v₁ = (p, 0, r):   q·p + p·0 = qp = pq ✓,   ‖v₁‖_∞ = max(p, 0, r) = r.
- v₂ = (0, q, r):   q·0 + p·q = pq     ✓,   ‖v₂‖_∞ = max(0, q, r) = r.

**What to close for Step 1:** Show these are indeed minimum-norm (no vector has norm < r).
Any solution to q·ψ_p + p·ψ_q = pq·s has s ≥ 1 for nonzero ψ, so ψ_r = rs ≥ r. Hence ‖ψ‖_∞ ≥ r.
Minimum norm is exactly r, achieved by v₁ and v₂.

### Step 2 — Verify v₁ and v₂ are non-degenerate

    W^{v₁}(a,b) = ab/(pq) · (p·0 − q·p) = ab/(pq) · (−qp) = −ab ≠ 0.   ✓
    W^{v₂}(a,b) = ab/(pq) · (p·q − q·0) = ab/(pq) · pq   = +ab ≠ 0.   ✓

Both minimum vectors are non-degenerate.

### Step 3 — Compare: minimum norm < degenerate minimum norm

    ‖v_min‖_∞ = r  <  2r = ‖v₀‖_∞ = minimum degenerate norm.

So the shortest vector (norm r) comes before any degenerate vector (norm ≥ 2r).

**What to close for Step 3:** Show the generator of L₀ is (p, q, 2r) and no degenerate
vector has smaller norm. This follows from Step 1: any ψ ∈ L₀ has ψ_r = 2rt (not rs),
so ψ_r ≥ 2r, hence norm ≥ 2r.

---

## Acceptance criteria

**CONFIRMED:** All three steps verified; Theorem E10 proved.  
Deliverable: complete elementary proof showing:
1. Every nonzero ψ ∈ L has ‖ψ‖_∞ ≥ r (minimum is r).
2. The vectors v₁ = (p,0,r) and v₂ = (0,q,r) achieve norm r and are non-degenerate.
3. Every degenerate vector has ‖ψ‖_∞ ≥ 2r > r.

**PARTIAL:** Steps 1 and 2 verified but Step 3 has a gap.  
State whether L₀ minimum could be < 2r for some partition.

**REFUTED:** State the counterexample triple (a,b,c) with a≥2, ω=3, squarefree, where
the shortest lattice vector is degenerate.

**INCONCLUSIVE:** State which sub-claim is unclear.

---

## Corollary (what this gives, combined with OB-09)

Under the hypotheses of OB-09 (squarefree coprime triple, ω ≥ 2) PLUS a ≥ 2 and ω = 3:

> The Pasten lattice L = F(a, b) has a nonzero vector ψ with W^ψ(a,b) ≠ 0 and  
> ‖ψ‖_∞ ≤ det(L)^{1/(ω−1)} = det(L)^{1/2} < R^{1/2} = rad(abc)^{1/2}.

This gives an **unconditional non-degenerate Minkowski bound** for this subfamily,
without any separate argument about non-degeneracy.

**Non-circularity:** No abc conjecture, no Szpiro, no IUT, no known abc triples used.

---

## Numerical anchor (sanity — not an input to the proof)

Triple (a, b, c) = (2, 3, 5): P = {2, 3, 5}, R = 30.

```python
import math

a, b, c = 2, 3, 5
p, q, r = 2, 3, 5
psi_v1 = (p, 0, r)  # = (2, 0, 5)
psi_v2 = (0, q, r)  # = (0, 3, 5)
psi_v0 = (p, q, 2*r)  # = (2, 3, 10)  -- generator of L_0

# Lattice constraint check (qr*psi_p + pr*psi_q - pq*psi_r = 0):
def check(psi):
    return q*r*psi[0] + p*r*psi[1] - p*q*psi[2]

print(f"v1={psi_v1}: constraint={check(psi_v1)}, W={p*psi_v1[1]-q*psi_v1[0]}, norm={max(abs(x) for x in psi_v1)}")
print(f"v2={psi_v2}: constraint={check(psi_v2)}, W={p*psi_v2[1]-q*psi_v2[0]}, norm={max(abs(x) for x in psi_v2)}")
print(f"v0={psi_v0}: constraint={check(psi_v0)}, W={p*psi_v0[1]-q*psi_v0[0]}, norm={max(abs(x) for x in psi_v0)}")
det_L = math.sqrt(sum(x**2 for x in [q*r, p*r, p*q]))
print(f"det(L) = sqrt({q*r}^2+{p*r}^2+{p*q}^2) = {det_L:.4f}")
print(f"R^{{1/2}} = {r**0.5:.4f}")
print(f"min norm (r) = {r} < 2r = {2*r} (degenerate min)")
```

Expected output:
```
v1=(2, 0, 5): constraint=0, W=-6, norm=5
v2=(0, 3, 5): constraint=0, W=6, norm=5
v0=(2, 3, 10): constraint=0, W=0, norm=10
det(L) = sqrt(225+100+36) = 19.0000
R^{1/2} = 2.2361
min norm (r) = 5 < 2r = 10 (degenerate min)
```

---

*Prepared 2026-08-15. Non-circularity: no abc triples, no fitted K_ε, no Szpiro.*  
*Run outsource/PROMPT_LINT.md before sending; A1–A10 checks below.*
