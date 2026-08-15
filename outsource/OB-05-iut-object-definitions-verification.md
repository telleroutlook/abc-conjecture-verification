# Problem OB-05 — IUT object definitions: verbatim audit and correction (CORE-3 IUT preparatory)

**Type:** arithmetic geometry / inter-universal Teichmüller theory — definitions only, no proof required

**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
IUT Corollary 3.12, known abc triples, or any fitted parameter K_ε. It asks only for
type-correct definitions of the mathematical objects appearing in IUTT-III Corollary 3.12
and its proof — not for a proof of any inequality. No parameter is fitted to examples.

**Purpose:** OB-02v2 (INCONCLUSIVE + LOCALIZATION, 2026-08-15) found that D1–D6 all
contain type errors or missing IUTT-I/III conditions. This preparatory task asks for a
corrected D1–D7 that matches the verbatim IUTT-I/III source. The output of this task
is the foundation for OB-06.

---

## The task (no proof required)

Provide a corrected version of D1–D7 below such that:

1. Each definition uses the **verbatim terminology and type system** of the cited IUTT-I/III
   source — not a simplification or analogy.
2. Each object has an explicit **type declaration** (even if informal: "D1 is a tuple (…)
   satisfying conditions C1–C8 of IUTT-I Definition 3.1").
3. Each definition is labeled with the **exact IUTT source**: paper (I/II/III/IV),
   section, and definition/proposition number.
4. Any simplification relative to the IUTT source is **explicitly flagged** with:
   "SIMPLIFIED: [what was dropped] [why dropping is or is not safe for this problem]".

**What is NOT required:**
- A proof that Corollary 3.12 holds.
- A proof that the Θ-link carries j²-scaling.
- Any new mathematical argument beyond reorganizing and correcting existing IUTT definitions.

---

## All definitions (self-contained — everything is here)

The following D1–D7 appeared in OB-02v2. Each is shown with the known errors identified
by the independent Gate-A review (2026-08-15). Provide a corrected replacement for each.

### D1 — Initial Θ-data

**Current (to be corrected):** A 6-tuple (F, X_F, l, C_K, V, ε) where:
- F is a number field
- X_F is a once-punctured elliptic curve over F
- l ≥ 5 is a prime
- C_K is a hyperbolic orbicurve over a subfield K ⊆ F of degree ≤ 2 over Q
- V is a set of valuations
- ε is an element of F^× for l-torsion trivialization

**Known errors (Gate-A review §3):**
- Missing required conditions: √−1 ∈ F; stable reduction; 6-torsion rationality; mod-l
  image containing SL₂(F_l); l coprime to bad characteristics and to Tate parameter orders.
- "K of degree ≤ 2" is not the correct description; K is constructed from the l-torsion kernel.
- Last component is not "ε ∈ F^× for l-torsion trivialization" — the actual construction
  involves cusp data.

**Source to use:** IUTT-I, Definition 3.1 (and Example 3.2 for concrete instances).

---

### D2 — Pilot objects

**Current (to be corrected):**
- q-pilot: q_v ∈ (F_v)^× for each bad prime v
- Θ-pilot: {q_v^{j²} : j = 1,…,l*} where l* = (l−1)/2

**Known errors (Gate-A review §3):**
- Pilots are objects in **global realified Frobenioids** constructed from the initial Θ-data,
  not elements of F_v^×.
- IUTT uses the normalized generator q̲_v = q_v^{1/(2l)} (to μ_{2l}), where q_v is the Tate
  parameter at bad prime v. The two must not be conflated.

**Source to use:** IUTT-III, Definition 3.8(i); IUTT-I, Example 3.2(iv).

---

### D3 — The Θ-link

**Current formulation:** A full poly-isomorphism HT^Θ ~~> HT^Θ between
F^{⊢×μ}_{LGP}-prime-strips of two successive Hodge theaters.

**Gate-A review finding:** Partially correct: Definition 3.8(ii) and Remark 3.8.1 confirm
this is a prime-strip poly-isomorphism that identifies Θ-pilot with q-pilot at the abstract
level. However, the definition must clarify:
- This is NOT a morphism of number fields or function fields. No map φ_F: F₁→F₂ exists
  or is expected between the two theaters. Asking for a "formula for φ_F on a generator"
  is a category error.
- The full poly-isomorphism is between prime-strip structures; its compatibility with
  log-volumes is what must be examined.

**Source to use:** IUTT-III, Definition 3.8(ii); Remark 3.8.1.

---

### D4 — Log-volume and indeterminacies

**Current (to be corrected):**
- Log-volume: μ_v : M(IQ(…)) → ℝ (local); global log-volume = −|log(−)|
- Ind1: indeterminacy from Galois/arithmetic groups
- Ind2: indeterminacy from ×μ-structure
- Ind3: indeterminacy from the log-link (described as "upper semi-commutativity")

**Known errors (Gate-A review §3):**
- Ind1, Ind2, Ind3 are **specific group actions and functorial structures** (not numerical
  error intervals). Specifically:
  - Ind1: action of automorphisms of the relevant prime-strip structures
  - Ind2: action on tensor-product direct summands
  - Ind3: upper semi-compatibility with log-links (non-archimedean: inclusions; archimedean:
    surjections)
- The current D4 last sentence says "accounting for all three indeterminacies, the
  comparison becomes −|log Θ| ≥ −|log q|" — this puts the conclusion inside a definition
  and is **circular**. It must be deleted.

**Source to use:** IUTT-III, Proposition 3.9 (log-volume definition); Theorem 3.11
(Ind1–Ind3 exact description); Remark 3.9.5(vii) (procession normalization and positive
tensor power M).

---

### D5 — IUTT-III Corollary 3.12

**Current formulation:** −|log Θ| ≥ −|log q|.

**Gate-A review finding:** Inequality direction is correct. But the statement omits:
- Asymmetric definitions: −|log Θ| is the procession-normalized mono-analytic log-volume
  of the Θ-pilot after taking the hull/union over all Ind1–Ind3 images; −|log q| is the
  log-volume of the q-pilot WITHOUT indeterminacy.
- The required condition |log q| > 0.
- Finiteness conditions and coefficient conditions on the procession.

**Source to use:** IUTT-III, Corollary 3.12 (the verbatim published statement in PRIMS 57
(2021)); Theorem 3.11 for the indeterminacy accounting.

---

### D6 — Concrete pilot embeddings and j²-scaling

**Current (to be corrected):**
- ι_q : q-pilot → W_q(v) ≅ ℝ by q_v ↦ log|q_v|
- ι_Θ : Θ-pilot → W_Θ(v) ≅ ℝ by q_v^{j²} ↦ j²·log|q_v|

**Known errors (Gate-A review §3):**
- IUTT-III Proposition 3.9 does **not** define one-dimensional spaces W_q(v), W_Θ(v) or
  the embeddings ι_q, ι_Θ. The elementary identity log|q_v^{j²}| = j²·log|q_v| is
  correct but promoting it to a functorial embedding of IUT pilot objects is the claim
  to be proved, not a definition.
- If W_v, ι_q, ι_Θ are newly constructed objects (not from IUTT-III), they must be
  explicitly flagged as NEW DEFINITIONS and their compatibility with IUTT morphisms stated
  as a claim, not an assumption.
- Normalization: IUTT-I Example 3.2(iv) uses q̲_v = q_v^{1/(2l)}, not q_v; the correct
  log-absolute value is log|q̲_v| = log|q_v|/(2l).

**Source to use:** IUTT-III, Proposition 3.9; Remark 3.9.5(vii); IUTT-I, Example 3.2(iv).

---

### D7 — Scholze–Stix concern

**Current formulation:** When the Θ-link identifies abstract Θ-pilot with abstract q-pilot,
it does not automatically carry j²-scaling data. In W_q(v), the abstract identification
places the Θ-pilot at log|q_v|, not j²·log|q_v|.

**Gate-A review finding:** Reasonable high-level summary. The four-node diagram in OB-02v2
is a reconstruction — not an explicit IUTT or Scholze–Stix definition. An acceptable
correction retains D7 as a high-level description of the dispute, but marks the four-node
diagram as "reconstructed, not from IUTT-III" and explains which aspect of Corollary 3.12
proof step (xi-e)→(xi-f) it is trying to capture.

**Source to use:** Scholze and Stix, *Why abc is still a conjecture* (2018-08-23), §§2.1.6–2.2;
IUTT-III, Corollary 3.12 proof steps (xi-d), (xi-e), (xi-f).

---

## Acceptance criteria

1. **CORRECTED-DEFINITIONS**: A revised D1–D7 where each definition:
   - Quotes the exact IUTT source (paper, section, definition/proposition number)
   - Uses IUTT-native types (Frobenioid, prime-strip, log-link, procession, mono-analytic, etc.)
   - Explicitly flags any simplification as SIMPLIFIED with justification
   - For D3: states clearly that no function-field morphism φ_F: F₁→F₂ is defined or expected
   - For D6: states clearly whether W_v and ι_q, ι_Θ are from IUTT-III or are new constructions

2. **PARTIAL**: Corrected versions of some D_i with precise statements of what is still
   missing for the others.

3. **INCONCLUSIVE + LOCALIZATION**: A finding that some D_i cannot be written
   self-containedly without citing IUTT-II or further prerequisites — with a precise list
   of what those prerequisites are and which definitions require them.

**Not accepted:**
- "The definition is standard in IUT" without a theorem/definition number.
- Any definition that uses a function-field morphism φ_F: F₁→F₂ (A8 violation).
- Any definition that assumes Corollary 3.12 or any abc-equivalent hypothesis.
- D4 containing a sentence that equates "accounting for Ind1–Ind3" with the target
  inequality (circular).

---

## Source PDFs to verify against baseline/ before citing

1. IUTT-I: Mochizuki, PRIMS 57 (2021) 3–207. Author PDF:
   https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20I.pdf
2. IUTT-III: Mochizuki, PRIMS 57 (2021) 403–626. Author PDF:
   https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20III.pdf
3. Scholze–Stix (2018-08-23):
   https://www.math.uni-bonn.de/people/scholze/WhyABCisStillaConjecture.pdf

---

## Numerical anchor (sanity only — not an input to the definitions)

Elliptic curve E: y² + y = x³ − x (LMFDB 37.a1), conductor N = 37, bad prime v = 37.

```python
import math

# Weierstrass invariants of 37.a1: [a1,a2,a3,a4,a6] = [0,0,1,-1,0]
a1, a2, a3, a4, a6 = 0, 0, 1, -1, 0
b2 = a1**2 + 4*a2
b4 = a1*a3 + 2*a4
b6 = a3**2 + 4*a6
b8 = a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2
c4 = b2**2 - 24*b4
c6 = -b2**3 + 36*b2*b4 - 216*b6
Delta = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
assert (c4, c6, Delta) == (48, -216, 37), f"Got {c4},{c6},{Delta}"

# v_37(j(E)) = -1  (j has simple pole at 37, since Delta = 37)
# Tate expansion: j(q) = q^{-1} + 744 + ...  =>  v_37(q_37) = 1
# log|q_37|_37 = -v_37(q_37)*log(37) = -log(37)  (negative: q_37 is 37-adically small)
log_q37 = -math.log(37)

# IUTT-I normalization: q̲_v = q_v^{1/(2*l)}, so log|q̲_37| = log|q_37| / (2*l)
l = 5
log_qbar37 = log_q37 / (2 * l)

# j^2-scaling: Theta-pilot has values q̲_v^{j^2} at j = 1,...,l*=(l-1)/2
lstar = (l - 1) // 2  # = 2
for j in range(1, lstar + 1):
    path_A = j**2 * log_qbar37   # concrete Theta-pilot embedding
    path_B = log_qbar37          # concrete q-pilot embedding
    discrepancy = (j**2 - 1) * log_qbar37
    print(f"j={j}: Path A={path_A:.6f}, Path B={path_B:.6f}, discrepancy={discrepancy:.6f}")
```

Expected output:
```
j=1: Path A=-0.361092, Path B=-0.361092, discrepancy=-0.000000
j=2: Path A=-1.444367, Path B=-0.361092, discrepancy=-1.083275
```

The discrepancy at j=2 is −1.083275 in log|q̲_{37}|_{37} units. This is the quantity
that any correct definition of ι_Θ vs ι_q must account for. It is a sanity check on the
numerical scale of the problem; it does not prove or disprove any IUT claim.
