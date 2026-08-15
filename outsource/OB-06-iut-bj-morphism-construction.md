# Problem OB-06 — IUT B_j morphism: comparison map for Θ-pilot to q-pilot log-volume (CORE-3)

**Type:** arithmetic geometry / inter-universal Teichmüller theory
**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
any abc-equivalent hypothesis, known abc triples, or any fitted parameter K_ε. It does
not assume that IUTT-III Corollary 3.12 holds; it asks whether a specific comparison
morphism B_j required by the Corollary 3.12 proof can be constructed from IUTT-I/II/III/IV.

**Dependency on OB-05:** This problem uses corrected D1–D7 definitions. D1–D7 below
follow the known-correct types from the OB-02v2 Gate-A review (2026-08-15); a referee
finding further errors in the definitions should report them as a dependency failure and
redirect to OB-05 rather than attempting to close this problem with incorrect objects.

---

## All definitions (self-contained — everything is here)

**D1 — Initial Θ-data** (IUTT-I, Definition 3.1): A collection (F, X_F, l, C_K, V, ε_V)
where F is a number field with √−1 ∈ F; X_F is a once-punctured elliptic curve over F
with stable reduction and 6-torsion rationality; l ≥ 5 is a prime with Galois image
containing SL₂(F_l); l is coprime to bad characteristics and Tate parameter orders; C_K
is a hyperbolic orbicurve over the field K constructed from the l-torsion kernel; V is
the canonical set of valuations; ε_V is cusp data. All Hodge theaters and links are
constructed from this single fixed initial Θ-data.

**D2 — Pilot objects** (IUTT-III, Definition 3.8(i); IUTT-I, Example 3.2(iv)): Objects
in global realified Frobenioids constructed from the initial Θ-data. The q-pilot is
associated to the normalized generator q̲_v = q_v^{1/(2l)} (to μ_{2l}) at each bad prime
v, where q_v is the Tate parameter. The Θ-pilot is associated to the collection
{q̲_v^{j²} : j = 1,…,l*} where l* = (l−1)/2. These are NOT elements of F_v^×.

**D3 — The Θ-link** (IUTT-III, Definition 3.8(ii); Remark 3.8.1): A full poly-isomorphism

    HT^Θ_n  ~~>  HT^Θ_{n+1}

between the F^{⊢×μ}_{LGP}-prime-strips of two successive Hodge theaters. Identifies the
Θ-pilot of theater n with the q-pilot of theater n+1 at the abstract prime-strip level.
This is NOT a morphism of number fields. No map φ_F: F₁→F₂ between number fields is
defined or expected; asking for such a formula is a category error.

**D4 — Log-volume** (IUTT-III, Proposition 3.9; Theorem 3.11): A map

    μ_v : M(IQ(…)) → ℝ

on compact opens (non-archimedean) or compact closures (archimedean) of IQ objects,
with procession normalization per Remark 3.9.5(vii). The three indeterminacies are:
- **Ind1**: action of automorphisms of the relevant prime-strip structures
- **Ind2**: action on tensor-product direct summands (×μ-indeterminacy)
- **Ind3**: upper semi-compatibility with log-links (non-archimedean: inclusions;
  archimedean: surjections)
These are NOT numerical error ranges; they are specific group actions and functorial maps.

**D5 — IUTT-III Corollary 3.12** (verbatim, PRIMS 57 (2021) p. 604): In the context of
Hodge theaters constructed from initial Θ-data as in D1, with pilot objects as in D2:

    −|log Θ| ≥ −|log q|

where −|log Θ| is the procession-normalized mono-analytic log-volume of the Θ-pilot
(hull/union over all Ind1–Ind3 images), and −|log q| is the log-volume of the q-pilot
(no indeterminacy). Required: |log q| > 0.
This is NOT the discriminant-conductor inequality; that follows later in IUTT-IV.

**D6 — Target comparison morphism B_j** (to be constructed — this is the claim): For each
bad prime v and j ∈ {1,…,l*}, a morphism (or relation)

    B_{v,j} : LogVol(det^{⊗M} Hull(P_{Θ,j}) / Ind_{1,2,3}) → LogVol(P_q)

satisfying all seven of the following items (a referee not able to specify all seven
should report which items are missing and cite the exact IUTT location):
1. P_{Θ,j} and P_q are the correct IUTT-III type (procession data, Frobenioid objects).
2. M (positive tensor power) and direct-summand weights are explicitly specified, from
   IUTT-III Remark 3.9.5(vii).
3. The order of operations — hull, union, quotient by Ind1–Ind3 — is specified.
4. B_{v,j} has a declared type (function, correspondence, relation), specified domain
   and codomain in the ordered real line ℝ; it is declared whether B_{v,j} depends on j.
5. B_{v,j} is compatible with the Θ-link poly-isomorphism of D3 (naturality condition).
6. Procession normalization is applied in the correct order relative to Ind1–Ind3.
7. B_{v,j} is order-preserving (or: a proved weaker statement still implying D5).

**D7 — Scholze–Stix concern** (Scholze–Stix 2018-08-23, §§2.1.6–2.2): The unresolved
question of whether the Θ-link's abstract identification of Θ-pilot with q-pilot is
compatible with the concrete j²-scaling in the log-volume comparison.

Specifically: when the abstract identification (D3) is composed with the concrete
log-volume embedding of the q-pilot, does the Θ-pilot land at j²·log|q̲_v| or at
log|q̲_v| in the real line? If the former, no discrepancy; if the latter, the j²-gain
that drives the Corollary 3.12 inequality is not justified by the construction.

---

## The theorem / claim to be verified

**Claim OB-06**: Construct B_{v,j} satisfying all 7 items in D6, using only definitions
from IUTT-I/II/III/IV — without assuming Corollary 3.12 or any abc-equivalent hypothesis.

**Either:**

(A) **Construct B_{v,j}** explicitly: specify all 7 items, and prove that B_{v,j} is
    well-defined and order-compatible so that Corollary 3.12 proof steps (xi-e)→(xi-f) close.

**Or:**

(B) **Exhibit a precise obstruction**: identify which of the 7 items in D6 cannot be
    satisfied from the cited IUTT sources — with the exact paper, section, and definition/
    proposition number where the construction breaks down, and a concrete numerical
    illustration of the discrepancy for j = 2 at v = 37 (using LMFDB 37.a1 data below).

---

## Proof skeleton to be closed

### Step 1 — Procession-normalized log-volume setup

**What to close:** For each bad prime v, write the procession-normalized log-volume of
the Θ-pilot explicitly using IUTT-III Proposition 3.9 and Remark 3.9.5(vii). Specify:
- the positive tensor power M
- the direct-summand weights
- the holomorphic hull and union construction
- the procession normalization

Cite the specific observation numbers from Remark 3.9.5(vii) (Observations 3-1, 3-2, 3-3,
9-2) for each step.

### Step 2 — Θ-link action on log-volume objects

**What to close:** Describe how the Θ-link poly-isomorphism of D3 acts on the log-volume
domain of D4. Specifically: does the prime-strip poly-isomorphism induce a well-defined
morphism on the M(IQ(…)) objects, and if so, is it the type of morphism that B_{v,j}
needs? Cite Definition 3.8(ii), Remark 3.8.1, and the specific compatibility statement.

### Step 3 — B_{v,j} construction or obstruction (the critical step)

**What to close:** Combine Steps 1 and 2. Either:
- Construct B_{v,j} (all 7 items in D6 satisfied), showing that Path A (via Θ-pilot
  embedding) and Path B (via Θ-link then q-pilot embedding) agree after Ind1–Ind3; or
- Show that the discrepancy (j²−1)·log|q̲_v| cannot be absorbed by Ind1–Ind3 as defined
  in Theorem 3.11, citing which Ind_i fails and why.

The specific sub-question per the Scholze–Stix concern: does Ind1–Ind3 contain an
element that maps the region ℝ_{≤ j²·log|q̲_v|} to ℝ_{≤ log|q̲_v|}? If so, give the
explicit group action or inclusion; if not, compute the gap.

### Step 4 — Derivation of −|log Θ| ≥ −|log q|

**What to close:** Given Step 3 (in either direction), trace through Corollary 3.12 proof
steps (xi-d)→(xi-e)→(xi-f):
- (xi-d): which positive tensor power and normalization puts objects in comparable form?
- (xi-e): why do output log-volumes lie in ℝ_{≤ −|log Θ|}?
- (xi-f): why does −|log q| belong to ℝ_{≤ −|log Θ|}?

The specific inference requiring B_{v,j}: "output region ℝ_{≤ −|log Θ|}" + "−|log q|
is related to input" ⟹ "−|log q| ∈ ℝ_{≤ −|log Θ|}". This inference requires the
order-compatibility in D6 item 7.

---

## Acceptance criteria

1. **CONFIRMED-PROOF**: B_{v,j} constructed with all 7 D6 items satisfied and Corollary
   3.12 inequality derived. A machine-replayable formal proof (Lean 4, Coq, Isabelle, or
   Metamath) satisfies obligation `core3.iut-corollary-312-independently-verified` in the
   abc verification kernel.

2. **CONFIRMED-OBSTRUCTION**: Explicit identification of which D6 item fails (with exact
   IUTT source) and a numerical computation showing the discrepancy for j = 2, v = 37.

3. **PARTIAL**: Proof that B_{v,j} exists conditionally on a hypothesis H not present in
   IUTT-I/II/III/IV, with H named explicitly and shown independent of abc and Szpiro.

4. **INCONCLUSIVE + LOCALIZATION**: Precise statement of which D6 item lacks a constructive
   definition in the cited IUTT literature, with the exact IUTT location (paper, section,
   definition number) of the gap.

**Not accepted:**
- "The comparison is standard" without explicit B_{v,j}.
- Any construction that uses Corollary 3.12 itself as a hypothesis.
- Any use of abc, Szpiro, known abc triples, or fitted K_ε.
- A D3 that introduces a function-field morphism φ_F: F₁→F₂ (this is a category error;
  see A8 of the outsource PROMPT_LINT).

---

## Source PDFs to verify against baseline/ before citing

1. IUTT-I: Mochizuki, PRIMS 57 (2021) 3–207.
   Author PDF: https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20I.pdf
2. IUTT-III: Mochizuki, PRIMS 57 (2021) 403–626.
   Author PDF: https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20III.pdf
3. Scholze–Stix (2018-08-23):
   https://www.math.uni-bonn.de/people/scholze/WhyABCisStillaConjecture.pdf

---

## Numerical anchor (sanity only — not an input to the proof)

Elliptic curve E: y² + y = x³ − x (LMFDB 37.a1), conductor N = 37, l = 5, l* = 2.

```python
import math

# Weierstrass invariants of 37.a1
a1, a2, a3, a4, a6 = 0, 0, 1, -1, 0
b2 = a1**2 + 4*a2
b4 = a1*a3 + 2*a4
b6 = a3**2 + 4*a6
b8 = a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2
c4 = b2**2 - 24*b4
c6 = -b2**3 + 36*b2*b4 - 216*b6
Delta = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
assert (c4, c6, Delta) == (48, -216, 37)

l = 5
lstar = (l - 1) // 2  # = 2
# v_37(j(E)) = -1  =>  v_37(q_37) = 1  =>  log|q_37|_37 = -log(37)
log_q37 = -math.log(37)
# IUTT-I normalization: q̲_v = q_v^{1/(2l)}
log_qbar37 = log_q37 / (2 * l)

print(f"c4={c4}, c6={c6}, Delta={Delta}")
print(f"log|q_37|_37 = {log_q37:.6f}")
print(f"log|q̲_37|_37 (IUTT normalized) = {log_qbar37:.6f}")
for j in range(1, lstar + 1):
    path_A = j**2 * log_qbar37   # Theta-pilot: j^2-scaled
    path_B = log_qbar37          # q-pilot: not scaled
    discrepancy = (j**2 - 1) * log_qbar37
    print(f"j={j}: Path A={path_A:.6f}, Path B={path_B:.6f}, discrepancy={discrepancy:.6f}")
```

Expected output:
```
c4=48, c6=-216, Delta=37
log|q_37|_37 = -3.610918
log|q̲_37|_37 (IUTT normalized) = -0.361092
j=1: Path A=-0.361092, Path B=-0.361092, discrepancy=-0.000000
j=2: Path A=-1.444367, Path B=-0.361092, discrepancy=-1.083275
```

The discrepancy at j=2 (−1.083275 in log|q̲_{37}| units) is the quantity that B_{v,j}
must account for. This is a sanity check on the numerical scale; it does NOT prove or
disprove any IUT claim, and LMFDB 37.a1 does NOT constitute complete IUTT-admissible
initial Θ-data (additional conditions from IUTT-I Definition 3.1 must be verified).
