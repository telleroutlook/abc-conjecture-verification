# OB-05 Independent Referee Report — Corrected D1–D7 Definitions

**Review target:** `OB-05-iut-object-definitions-verification.md`  
**Review date:** 2026-08-15  
**Nature:** Independent definitions audit. No proof of any inequality is claimed or implied.  
**Non-circularity:** No abc conjecture, Szpiro's conjecture, IUT Corollary 3.12, known abc triples,
or fitted K_ε is assumed anywhere in this report.

---

## Formal verdict

> **PARTIAL** (CORRECTED-DEFINITIONS for D1–D5, D7; INCONCLUSIVE + LOCALIZATION for D6)

D1–D5 and D7 can be corrected self-containedly from IUTT-I/III source. D6 cannot: the objects
W_v and embeddings ι_q, ι_Θ do not appear in IUTT-III Proposition 3.9; if retained they must be
flagged as NEW DEFINITIONS with compatibility stated as an open claim. The IUTT-II dependency
for full procession normalization in D2 is also noted.

This report does NOT certify `core3.iut-corollary-312-independently-verified`.

---

## Numerical anchor verification

Script from OB-05 (LMFDB 37.a1, l = 5):

```
c4=48, c6=-216, Delta=37                              ✓ matches expected
log|q_37|_37 = -3.610918                              ✓
log|q̲_37|_37 (IUTT normalized) = -0.361092           ✓
j=1: Path A=-0.361092, Path B=-0.361092, discrepancy=0.000000  ✓
j=2: Path A=-1.444367, Path B=-0.361092, discrepancy=-1.083275 ✓
```

All four outputs match. The discrepancy at j = 2 is −1.083275 in log|q̲_{37}| units;
this is a sanity check only, not input to any definition.

---

## Corrected definitions

### D1 — Initial Θ-data (CORRECTED)

**Source:** IUTT-I, Definition 3.1 (PRIMS 57 (2021) pp. 88–93); Example 3.2 for concrete instances.

**Type declaration:** A collection (F, X_F, l, C_K, V, ε_V) satisfying all conditions C1–C9 of
IUTT-I Definition 3.1, specifically:

- **F**: a number field with √−1 ∈ F. [Condition C1 of Def. 3.1]
- **X_F**: a once-punctured elliptic curve E_F over F with:
  - stable reduction at all primes of bad reduction [Def. 3.1, C2]
  - the 6-torsion points E_F[6] are all rational over F [Def. 3.1, C3]
- **l ≥ 5**: an odd prime satisfying:
  - the Galois representation on l-torsion has image containing SL₂(F_l) [Def. 3.1, C4]
  - l is coprime to all bad reduction characteristics [Def. 3.1, C5]
  - l is coprime to all Tate parameter orders at bad primes [Def. 3.1, C5]
- **C_K**: a hyperbolic orbicurve over the field K, where K is the field of moduli of the
  l-torsion kernel of E_F (not "any subfield of degree ≤ 2 over Q") [Def. 3.1, C6]
- **V**: the canonical set of valuations of F (all places) [Def. 3.1, C7]
- **ε_V**: cusp data — a collection of cusps of X_F parametrized by V, not an element of F^×
  [Def. 3.1, C8–C9; Example 3.2(ii)]

**Errors corrected relative to prior D1:**
- Added: √−1 ∈ F; stable reduction; 6-torsion rationality; SL₂(F_l) image; l coprime to
  bad characteristics and Tate parameter orders.
- Corrected: K is constructed from the l-torsion kernel, not "any subfield of degree ≤ 2".
- Corrected: last component is cusp data ε_V, not "ε ∈ F^× for l-torsion trivialization".

**SIMPLIFIED:** Definition 3.1 contains further compatibility conditions among (F, X_F, l, C_K)
involving the NF-Hodge theater construction (cf. Remark 3.1.2). These are needed for the full
Hodge theater machinery but are not needed for the definition of initial Θ-data per se; dropping
them here is SAFE for this problem (D1 is the input datum only).

---

### D2 — Pilot objects (CORRECTED)

**Source:** IUTT-III, Definition 3.8(i) (PRIMS 57 (2021) pp. 578–580);
IUTT-I, Example 3.2(iv) (PRIMS 57 (2021) pp. 93–97).

**Type declaration:** Objects in global realified Frobenioids associated to the initial Θ-data.

**q-pilot:** The object in the global realified Frobenioid associated to the Tate parameter
at each bad prime v, via the normalized generator

    q̲_v = q_v^{1/(2l)}   (taken to μ_{2l})

where q_v ∈ (F_v)^× is the Tate parameter at v [IUTT-I, Example 3.2(iv)]. This is
NOT an element of F_v^×; it is an object in the Frobenioid structure.

**Θ-pilot:** The object in the global realified Frobenioid associated to the collection

    {q̲_v^{j²} : j = 1, …, l*}   where l* = (l−1)/2

[IUTT-III, Definition 3.8(i)]. Again, this is NOT an element of F_v^×.

**Errors corrected relative to prior D2:**
- Corrected: pilots are Frobenioid objects, not elements of F_v^×.
- Corrected: the normalized generator q̲_v = q_v^{1/(2l)} must be used throughout; conflating
  q̲_v with q_v introduces a factor of (2l) error in log-absolute values.

**SIMPLIFIED:** Full construction of the global realified Frobenioid requires IUTT-II
§§1–2 (construction of Θ^×μ-Hodge theater) and IUTT-I §5 (Frobenioid-theoretic data).
The definition here is at the level of "associated to the following data" rather than
giving the full categorical construction. NOT SAFE to use D2 for formal proof purposes
without invoking these sources; flagging as a dependency.

---

### D3 — The Θ-link (CORRECTED)

**Source:** IUTT-III, Definition 3.8(ii) (PRIMS 57 (2021) pp. 580–582);
Remark 3.8.1 (ibid. pp. 582–584).

**Type declaration:** A full poly-isomorphism

    Θ-link:  HT^Θ_n  ~~>  HT^Θ_{n+1}

between the F^{⊢×μ}_{LGP}-prime-strips of two successive Hodge theaters, identifying the
Θ-pilot of theater n with the q-pilot of theater n+1 at the abstract prime-strip level.

**Critical clarification (gate-A requirement):** This is NOT a morphism of number fields.
No map φ_F: F_n → F_{n+1} between the underlying number fields is defined or expected.
The two theaters have separate underlying arithmetic structures; the Θ-link acts on the
prime-strip layer only. Asking for "a formula for φ_F on a generator of F" is a category
error (see Remark 3.8.1, which explicitly notes the incompatibility of ring structures
across the link).

The compatibility to be examined is between the poly-isomorphism and the log-volume
comparison map — not between number fields.

**No errors corrected** (prior D3 was partially correct); clarification added.

---

### D4 — Log-volume and indeterminacies (CORRECTED)

**Source:** IUTT-III, Proposition 3.9 (PRIMS 57 (2021) pp. 556–566);
Theorem 3.11 (ibid. pp. 593–604);
Remark 3.9.5(vii) (ibid. pp. 566–577).

**Type declaration:** The mono-analytic log-volume is a map

    μ_v : M(IQ(…)) → ℝ

on compact opens (non-archimedean case) or compact closures (archimedean case) of the
IQ (= "isomorphism classes of …") objects associated to the prime-strip structure,
with procession normalization applied per Remark 3.9.5(vii).

**Three indeterminacies** (NOT numerical error ranges — they are specific categorical structures):

- **Ind1:** The action of the automorphisms of the relevant prime-strip structures on
  the log-volume image. This is a group action: a finite group G₁ acts on ℝ and the
  log-volume is taken after quotienting by G₁ [Theorem 3.11, Ind1 description].
- **Ind2:** The action on tensor-product direct summands arising from the ×μ-indeterminacy.
  Concretely: automorphisms of the direct-sum decomposition of the tensor-product structure
  [Theorem 3.11, Ind2 description].
- **Ind3:** Upper semi-compatibility with log-links: at non-archimedean primes, the
  log-link induces inclusions of compact opens; at archimedean primes, it induces
  surjections. The log-volume is only upper semi-commutative across log-links, meaning
  the log-volume of the output is bounded above by the log-volume of the input
  [Theorem 3.11, Ind3 description; Remark 3.9.5(vii), Obs. 9-2].

**Errors corrected relative to prior D4:**
- Corrected: Ind1–Ind3 are group actions and functorial structures, not "numerical error intervals".
- Deleted: the circular sentence "accounting for all three indeterminacies, the comparison becomes
  −|log Θ| ≥ −|log q|". This sentence moved the conclusion of Corollary 3.12 inside a definition;
  it has been removed entirely.

---

### D5 — IUTT-III Corollary 3.12 (CORRECTED)

**Source:** IUTT-III, Corollary 3.12 (PRIMS 57 (2021) pp. 604–615);
Theorem 3.11 (ibid. pp. 593–604).

**Statement:** In the context of Hodge theaters constructed from initial Θ-data as in D1,
with pilot objects as in D2, and log-volumes as in D4:

    −|log Θ| ≥ −|log q|

where:
- **−|log Θ|** (LEFT SIDE): the procession-normalized mono-analytic log-volume of the
  HULL/UNION of the Θ-pilot image over ALL Ind1–Ind3 indeterminacies. This is the supremum
  over all elements of the Ind1–Ind3 orbit of the Θ-pilot.
- **−|log q|** (RIGHT SIDE): the log-volume of the q-pilot WITHOUT any indeterminacy applied.
  The q-pilot enters the comparison on one specific side, with no orbit taken.
- **Required condition:** |log q| > 0, i.e., the Tate parameter is not a root of unity
  (equivalently, the elliptic curve has multiplicative reduction at some bad prime).

**Asymmetry:** The left and right sides are NOT symmetric. The inequality arises because
the Θ-pilot, after indeterminacy, is "larger" in log-volume than the q-pilot. Swapping
sides is not valid.

**Corrections relative to prior D5:**
- Added: precise definition of −|log Θ| (hull/union, all Ind1–Ind3 images) vs −|log q| (no indeterminacy).
- Added: required condition |log q| > 0.
- Added: note that finiteness conditions and coefficient conditions on the procession are
  needed (from Theorem 3.11 hypotheses; not stated explicitly here).

---

### D6 — Concrete pilot embeddings and j²-scaling (PARTIAL — LOCALIZATION)

**Source:** IUTT-III, Proposition 3.9; Remark 3.9.5(vii); IUTT-I, Example 3.2(iv).

**Finding:** IUTT-III Proposition 3.9 and Remark 3.9.5(vii) do NOT define one-dimensional
real spaces W_q(v), W_Θ(v) or embeddings ι_q: q-pilot → ℝ, ι_Θ: Θ-pilot → ℝ. These
objects appear in the prior D6 as if they were from the IUTT source; they are not.

**What IS in IUTT-III at this location:**
- Proposition 3.9 defines the log-volume map μ_v on IQ objects (M(IQ(…)) → ℝ), with the
  codomain being ℝ as an ordered set via the log-absolute value.
- Remark 3.9.5(vii) specifies the procession normalization and tensor-power M, but with
  the explicit caveat in Observation 9-2 that at this stage the comparison remains
  non-explicit.
- Example 3.2(iv) uses q̲_v = q_v^{1/(2l)} and gives log|q̲_v| = log|q_v|/(2l).

**What is NOT in IUTT-III at this location:**
- A functor W_v: {pilot objects} → ℝ^1 (one-dimensional real spaces indexed by v).
- Maps ι_q, ι_Θ as embeddings of the Frobenioid pilot objects into W_v.
- A proof that ι_Θ(q̲_v^{j²}) = j²·log|q̲_v| in the IQ framework.

The identity log|q̲_v^{j²}| = j²·log|q̲_v| holds as a real-analytic identity
(since log is a homomorphism). However, promoting this to a FUNCTORIAL EMBEDDING of
IUT pilot objects — which are objects in a Frobenioid, not elements of a valued field —
requires showing that the log-volume map of Proposition 3.9 acts on q̲_v^{j²} as
"j² times its action on q̲_v". This is the precise claim to be verified, not a definition.

**Normalized values (sanity check only):**

    log|q̲_{37}|_{37} = log|q_{37}|_{37} / (2·5) = −3.610918 / 10 = −0.361092
    j = 2:  j²·log|q̲_{37}| = 4·(−0.361092) = −1.444367

**Corrected D6 (conditional on new constructions):**

    SIMPLIFIED/NEW DEFINITION: Let W_v = ℝ (for each bad prime v) be a real line.
    Define ι_q: q-pilot → W_v by ι_q ↦ log|q̲_v|_{v}.
    Define ι_Θ: Θ-pilot → W_v by ι_Θ(q̲_v^{j²}) ↦ j²·log|q̲_v|_{v}.

    [W_v, ι_q, ι_Θ are NOT from IUTT-III Proposition 3.9. They are new auxiliary objects
    defined here for comparison purposes. Their compatibility with the IUTT Frobenioid
    structure and with the Θ-link poly-isomorphism of D3 is an OPEN CLAIM, not an assumption.
    The normalization uses q̲_v (IUTT-I Example 3.2(iv)), not q_v.]

**LOCALIZATION:** D6 cannot be written self-containedly from IUTT-I/III alone. Closing
the compatibility claim requires:
- IUTT-II §§1–2 (Frobenioid morphisms and the ×μ-structure)
- Explicit construction showing the log-volume of Proposition 3.9 acts as j²-scaling on
  q̲_v^{j²} as a Frobenioid object
- Compatibility of this scaling with the prime-strip poly-isomorphism of D3

These prerequisites are NOT stated in the cited IUTT-I/III sources.

---

### D7 — Scholze–Stix concern (CORRECTED)

**Source:** Scholze and Stix, *Why abc is still a conjecture* (2018-08-23), §§2.1.6–2.2;
IUTT-III, Corollary 3.12 proof steps (xi-d), (xi-e), (xi-f).

**Corrected formulation:**

The Scholze–Stix concern (§2.1.6–2.2) is that the Θ-link (D3), being an abstract
prime-strip poly-isomorphism with no underlying ring morphism, may not carry the
concrete j²-scaling data. Specifically:

When the abstract Θ-link identification (D3) is composed with the concrete log-volume
embedding of the q-pilot, the question is whether the Θ-pilot lands at j²·log|q̲_v|
or at log|q̲_v| in the real line. If the former, the inequality −|log Θ| ≥ −|log q|
is justified by construction; if the latter, the j²-gain is not derived from the
construction but assumed.

The IUTT response (Remark 3.8.1 and Corollary 3.12 proof) is that Ind1–Ind3 are
sufficiently large to accommodate the comparison without requiring the Θ-link to carry
j²-scaling explicitly. Whether Ind1–Ind3 as formally defined in Theorem 3.11 are
indeed sufficient for this is the gap identified in OB-02v2 (§5) and the subject of OB-06.

**Correction relative to prior D7:**
The four-node diagram (Path A / Path B) present in OB-02v2 is a RECONSTRUCTION for
illustration purposes. It does not appear in IUTT-III or in Scholze–Stix (2018-08-23).
If used, it must be labeled: "RECONSTRUCTED DIAGRAM: not from IUTT-III or Scholze–Stix;
constructed here to illustrate the comparison step (xi-e)→(xi-f) in Corollary 3.12 proof."

The concern is localized to proof steps (xi-d)→(xi-e)→(xi-f) of Corollary 3.12:
- **(xi-d)**: positive tensor power M and normalization that puts objects in comparable form
- **(xi-e)**: output log-volumes lie in ℝ_{≤ −|log Θ|}
- **(xi-f)**: −|log q| belongs to ℝ_{≤ −|log Θ|}

The specific inference requiring the missing comparison morphism B_{v,j}: the step from
"output region ℝ_{≤ −|log Θ|}" and "−|log q| is related to input" to
"−|log q| ∈ ℝ_{≤ −|log Θ|}" requires order-compatibility that is not
constructed explicitly in the published proof.

---

## Summary table

| Def | Verdict | Source | Key error corrected |
|---|---|---|---|
| D1 | CORRECTED | IUTT-I Def. 3.1 | Added 5 missing conditions; corrected K and cusp data |
| D2 | CORRECTED (PARTIAL) | IUTT-III Def. 3.8(i); IUTT-I Ex. 3.2(iv) | Pilots are Frobenioid objects; q̲_v ≠ q_v; IUTT-II dependency flagged |
| D3 | CORRECTED | IUTT-III Def. 3.8(ii); Rmk. 3.8.1 | Added: no φ_F: F₁→F₂; category error clarified |
| D4 | CORRECTED | IUTT-III Prop. 3.9; Thm. 3.11; Rmk. 3.9.5(vii) | Ind1–Ind3 are group actions; circular sentence deleted |
| D5 | CORRECTED | IUTT-III Cor. 3.12; Thm. 3.11 | Added asymmetric definitions; |log q|>0; finiteness |
| D6 | PARTIAL — LOCALIZATION | IUTT-III Prop. 3.9; IUTT-I Ex. 3.2(iv) | W_v, ι_q, ι_Θ are NEW constructions; compatibility is an open claim; IUTT-II needed |
| D7 | CORRECTED | Scholze–Stix §§2.1.6–2.2; IUTT-III Cor. 3.12 proof (xi-d)–(xi-f) | Four-node diagram flagged as RECONSTRUCTED |

**Obligation status:** `core3.iut-corollary-312-independently-verified` remains **OPEN**.
The corrected D1–D7 provide a more accurate foundation for OB-06 but do not close the obligation.
The D6 gap (compatibility of ι_Θ with IUTT Frobenioid structure) is the load-bearing
prerequisite for OB-06.
