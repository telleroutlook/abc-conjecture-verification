# Problem OB-02v2 — IUT Corollary 3.12: compatibility of pilot-object log-volume comparison

**Type:** arithmetic geometry / inter-universal Teichmüller theory  
**Non-circularity:** This problem does **not** assume the abc conjecture, Szpiro's conjecture,
any abc-equivalent hypothesis, known abc triples, or any fitted parameter K_ε. It asks
for a formal verification of one specific compatibility diagram within IUT — the step that
relates abstract pilot-object identification to concrete j²-scaled embeddings in
one-dimensional real vector spaces. No assumption is made that Mochizuki's argument is
correct; the question is whether the specified diagram commutes or whether a precise
obstruction can be exhibited.

**Review status (2026-08-15):** INCONCLUSIVE + LOCALIZATION — independent Gate-A review confirms the gap is precisely localised to IUTT-III Remark 3.9.5(vii) Observations 3-1–3, 9-2 and Corollary 3.12 proof steps (xi-d)–(xi-f): the comparison morphism B_j (from procession-normalised Θ-pilot log-volume to q-pilot log-volume) is not constructed in any cited source. D1–D6 all contain type errors or missing assumptions that must be corrected before re-send (10-item checklist in `reviews/OB-02v2-independent-gate-a-review-2026-08-15.md` §9). obligation `core3.iut-corollary-312-independently-verified` NOT certified.

Source PDFs used for this problem (must be verified against baseline/ before citing):
- IUTT-I: Mochizuki, *IUTT I: Construction of Hodge Theaters*, PRIMS 57 (2021).
- IUTT-III: Mochizuki, *IUTT III: Canonical Splittings of the Log-Theta-Lattice*, PRIMS 57 (2021).
- Scholze–Stix: *Why abc is still a conjecture* (2018-08-23).

---

## All definitions (self-contained — everything is here)

### D1 — Initial Θ-data (IUTT-I Definition 3.1)

**Initial Θ-data** is a collection

    (F, X_F, l, C_K, V, ε)

where:
- **F** is a number field (a finite extension of Q); fix it once for all theaters.
- **X_F** is a once-punctured elliptic curve over F (the base curve).
- **l ≥ 5** is a prime (the "theta level").
- **C_K** is a hyperbolic orbicurve over a subfield K ⊆ F of degree ≤ 2 over Q.
- **V** is a set of valuations of F equipped with a specific bijection with the set of
  all valuations of a certain canonically-chosen subfield; it is **not** an arbitrary
  finite set of places.
- **ε** is an element of F^× used to fix the l-torsion trivialization.

**All Hodge theaters and all links are constructed from this single fixed initial Θ-data.**
The two theaters connected by a Θ-link are not over arbitrary different base fields; they
are both constructed from the same (F, X_F, l, C_K, V, ε).

### D2 — Pilot objects (IUTT-III Definition 3.8(i))

Within a Hodge theater constructed from the initial Θ-data above:

- The **q-pilot object** is the element
      q_v  ∈  (F_v)^×
  for each bad-reduction prime v of X_F. More precisely it lives in a certain
  Frobenioid-theoretic object; for the purposes of log-volume comparison it is
  represented by the formal symbol `q` with local factors q_v at each bad prime v.

- The **Θ-pilot object** is the collection of theta values
      { q_v^{j²} : j = 1, …, l* }
  where l* = (l−1)/2, also living in the Frobenioid; represented by the formal symbol `Θ`.

These are defined within a single Hodge theater; the Θ-link connects the Θ-pilot of one
theater to the q-pilot of the next.

### D3 — The Θ-link (IUTT-III Definition 3.8(ii))

The **Θ-link** is a **full poly-isomorphism**

    HT^{Θ}  ~~>  HT^{Θ}

between the F^{⊢×μ}_{LGP}-prime-strips associated to two successive Hodge theaters
HT^{Θ}_{n} and HT^{Θ}_{n+1} in the log-theta-lattice. Concretely it is the collection
of all isomorphisms between the two prime-strip structures that are compatible with the
given Frobenioid data.

**This is NOT a morphism of function fields or rings.** No map φ_F: F₁→F₂ between
number fields is defined or claimed. In particular, no formula for φ_F on generators
of F^× exists or is expected.

The Θ-link **identifies the Θ-pilot of theater n with the q-pilot of theater n+1** at the
level of abstract prime-strip isomorphisms. The question of this problem is whether that
abstract identification is compatible with the concrete j²-scaling in the log-volume
comparison.

### D4 — Log-volume (IUTT-III Proposition 3.9)

For a Hodge theater constructed from the initial Θ-data, the **log-volume** is defined as
follows. Let IQ(−) denote the ind-pro-object constructed in IUTT-III §1. Let

    𝕄(IQ(…))

denote the set of non-empty compact open subsets (or compact closures at archimedean
places) of the relevant IQ object. The **local log-volume** at a place v is a map

    μ_v : 𝕄(IQ(…)) → ℝ

normalized as specified in Prop 3.9. The **global log-volume** is

    −|log(−)| := Σ_{v} μ_v(−)

summed over all places of the relevant portion of the log-theta-lattice, with the
normalization of Prop 3.9(iv) (log-link compatibility).

For the q-pilot and Θ-pilot, the relevant quantities are:
- **−|log q|**: the global log-volume of the compact region associated to the q-pilot.
- **−|log Θ|**: the global log-volume of the compact region associated to the Θ-pilot.

The three **indeterminacies** that must be accounted for in computing these log-volumes are:
- **Ind1**: indeterminacy arising from the action of the relevant Galois/arithmetic groups.
- **Ind2**: indeterminacy arising from the ×μ-indeterminacy (multiplicative structure).
- **Ind3**: indeterminacy arising from the log-link (upper semi-commutativity).

After accounting for all three indeterminacies, the log-volume comparison becomes an
inequality of the form: −|log Θ| ≥ −|log q| (or equivalently |log Θ| ≤ |log q|),
modulo the specified indeterminacy ranges.

### D5 — IUTT-III Corollary 3.12 (verbatim statement, to be verified against source)

**IUTT-III Corollary 3.12** (*Log-volume Estimates for Θ-Pilot Objects*):

In the context of a collection of Θ±^{ell}NF-Hodge theaters constructed from initial
Θ-data as in D1, with q-pilot and Θ-pilot as in D2:

    −|log Θ|  ≥  −|log q|

That is, the global log-volume of the (procession-normalized) Θ-pilot is greater than or
equal to the global log-volume of the q-pilot (after accounting for indeterminacies
Ind1–Ind3).

**This is NOT the discriminant-conductor inequality** log|Δ| ≤ (1+ε)log N + C.
The arithmetic height bound is a consequence derived in IUTT-IV Theorem 1.10 and
Corollary 2.3 via additional steps not present in Corollary 3.12 itself.

### D6 — Concrete pilot embeddings and j²-scaling

Let v be a bad-reduction prime of X_F. The **concrete q-pilot embedding** places the
q-pilot in a one-dimensional real vector space

    W_q(v) ≅ ℝ

by the map   q_v  ↦  log|q_v|  ∈  ℝ_{< 0}.

The **concrete Θ-pilot embedding** places the Θ-pilot by the collection

    q_v^{j²}  ↦  j² · log|q_v|  ∈  ℝ_{< 0},   j = 1, …, l*.

The **j²-scaling** is the ratio of the Θ-pilot embedding to the q-pilot embedding at
prime v: the Θ values satisfy log|q_v^{j²}| = j² · log|q_v|, so for j ≥ 2 the concrete
Θ-pilot embedding has strictly larger absolute value than the q-pilot embedding.

### D7 — The Scholze–Stix concern (stated as a claim to be checked, not a theorem)

Scholze and Stix (2018) claim that the following is not proved in IUTT-III:

> When the Θ-link identifies the abstract Θ-pilot with the abstract q-pilot, it does NOT
> automatically carry the j²-scaling data from D6. Specifically: in the one-dimensional
> real vector space W_q(v), the abstract identification places the Θ-pilot at the same
> point as the q-pilot (i.e., at log|q_v|, not at j²·log|q_v|). If this is the correct
> interpretation, then the j²-gain that provides the inequality in Corollary 3.12 is not
> justified by the construction.

Mochizuki disputes this interpretation. The unresolved question is whether the precise
categorical construction of the Θ-link in IUTT-III Def 3.8 does or does not preserve
the j²-scaling through the abstract poly-isomorphism.

This document records D7 as the **claim to be verified**, not as an established theorem
in either direction.

---

## The theorem / claim to be verified

**Claim OB-02v2**: In the context of D1–D7, verify or refute the following compatibility
statement for IUTT-III Corollary 3.12 proof steps (xi-e)→(xi-f):

**Diagram to be verified**: The following square must commute (or a precise obstruction
to its commutativity must be exhibited):

```
  Θ-pilot (abstract, theater n)  ---[Θ-link (D3)]--→  q-pilot (abstract, theater n+1)
          |                                                      |
     [concrete                                            [concrete
      embedding D6]                                        embedding D6]
          |                                                      |
          ↓                                                      ↓
  W_Θ(v) ≅ ℝ  [at j²·log|q_v|]    ???    W_q(v) ≅ ℝ  [at log|q_v|]
```

The **top arrow** (Θ-link) is an abstract prime-strip poly-isomorphism (D3).
The **left arrow** (concrete Θ-pilot embedding) maps the Θ-pilot to j²·log|q_v| in ℝ.
The **right arrow** (concrete q-pilot embedding) maps the q-pilot to log|q_v| in ℝ.
The **bottom arrow** (comparison map) must be identified explicitly.

**The question**: Does the bottom arrow take ℝ_{≤ −|log Θ|} into ℝ_{≤ −|log q|}?
Equivalently: is −|log Θ| ≥ −|log q| (Corollary 3.12) a consequence of the commutativity
of this diagram, or does commutativity fail (in which case: what is the obstruction)?

The sub-question at step (xi-e)→(xi-f): step (xi-e) asserts that the output log-volumes
lie in ℝ_{≤ −|log Θ|}; step (xi-f) asserts −|log q| belongs to this region. The
question is whether the concrete identification of −|log q| with the image of the
concrete Θ-pilot embedding is justified, given that the Θ-link is an ABSTRACT
poly-isomorphism that does not explicitly carry j²-scaling.

---

## Proof skeleton to be closed

### Step 1 — Identify the relevant 1D real vector spaces

**What to close**: For each bad prime v of X_F, write down the explicit one-dimensional
real vector space W_v and the maps

    ι_q: q-pilot → W_v   (the concrete q-pilot embedding)
    ι_Θ: Θ-pilot → W_v   (the concrete Θ-pilot embedding)

as defined from the IUTT-III Proposition 3.9 log-volume construction. Verify that ι_q
maps to log|q_v| and ι_Θ maps to Σ_{j=1}^{l*} j² · log|q_v| (or the appropriate
procession normalization thereof).

### Step 2 — Unpack the Θ-link action on pilot objects

**What to close**: In the language of D3 (prime-strip poly-isomorphisms), describe
precisely what the Θ-link does to the abstract Θ-pilot of theater n when it identifies
it with the abstract q-pilot of theater n+1. Specifically: does the poly-isomorphism
respect the structure of the concrete embeddings ι_q and ι_Θ? Cite the specific
morphism in IUTT-III Definition 3.8(ii) that induces the action on pilot objects.

### Step 3 — j²-scaling compatibility

**What to close**: This is the critical step. After the Θ-link identifies (abstract)
Θ-pilot ↔ (abstract) q-pilot, there are two ways to compute the log-volume of the
resulting object:

- Path A (via ι_Θ): use the Θ-pilot embedding → gets j²·log|q_v|.
- Path B (via Θ-link then ι_q): use the identification then q-pilot embedding → gets log|q_v|.

If Path A ≠ Path B (i.e., j²·log|q_v| ≠ log|q_v| for j ≥ 2), then the diagram fails
to commute. The question is whether the indeterminacies Ind1–Ind3 (D4) account for
this discrepancy, or whether the discrepancy is a genuine obstruction.

**Provide one of:**
- A proof that the diagram commutes after accounting for Ind1–Ind3, with explicit
  formulas showing which indeterminacy absorbs the j²-discrepancy.
- An explicit configuration (from IUTT-admissible data — initial Θ-data D1 with
  a specific elliptic curve E/F) where Path A ≠ Path B and the indeterminacies do
  not reconcile the difference.

### Step 4 — Derivation of −|log Θ| ≥ −|log q|

**What to close**: Assuming Step 3 is resolved (in either direction), trace through
how IUTT-III Corollary 3.12 steps (xi-e) and (xi-f) use the pilot log-volume
comparison to conclude −|log Θ| ≥ −|log q|. Specifically:

- What does step (xi-e) produce? (A region ℝ_{≤ −|log Θ|} of possible output values.)
- What does step (xi-f) claim? (That −|log q| lies in this region.)
- Which specific map or identification places −|log q| in ℝ_{≤ −|log Θ|}?

If Step 3 reveals an obstruction, show how it blocks step (xi-f).

---

## Acceptance criteria

1. **CONFIRMED-PROOF**: A machine-checkable proof (Lean, Coq, Isabelle, or Metamath) of
   the commutativity of the diagram in the claim section, showing that −|log Θ| ≥ −|log q|
   follows from the IUT construction without assuming abc, Szpiro, or any abc-equivalent
   hypothesis. This would satisfy the CORE-3 sub-obligation
   `core3.iut-corollary-312-independently-verified` in the verification kernel.

2. **CONFIRMED-OBSTRUCTION**: An explicit IUTT-admissible configuration (specific initial
   Θ-data D1) and a precise computation showing that Path A ≠ Path B (Step 3) in a way
   that the indeterminacies Ind1–Ind3 cannot reconcile, together with the exact place in
   the proof where the j²-scaling is lost. This would confirm a precise version of the
   Scholze–Stix concern.

3. **PARTIAL**: A proof that the diagram commutes conditionally on a precisely-stated
   additional hypothesis H not present in IUTT-III, with H named explicitly and shown to
   be independent of abc and Szpiro.

4. **INCONCLUSIVE + LOCALIZATION**: A precise statement of which morphism in Steps 1–4
   currently lacks a rigorous definition in the sense required, with the exact IUTT-III
   location (section, definition, proposition number) of each gap.

**Reject**: "The identification is standard" or "the objects are the same" without an
explicit formula for the bottom arrow of the diagram.
**Reject**: Any outcome that assumes abc, Szpiro, or Corollary 3.12 itself as a hypothesis.
**Reject**: An inconclusive result that does not localize the gap to a specific step.

---

## Numerical anchor (sanity only — not an input to the proof)

Take initial Θ-data with:
- E: y² + y = x³ − x  (LMFDB label 37.a1, conductor N = 37, |Δ_min| = 37)
  Weierstrass model: [a1,a2,a3,a4,a6] = [0,0,1,−1,0].
- Bad prime: v = 37
- q-parameter at v = 37: q_{37} (the Tate parameter; log|q_{37}|_{37} = −ord_{37}(j(E))·log 37
  for the j-invariant j(E) = c4³/Δ = 48³/37)

Concrete sanity check (does not prove or disprove the diagram):
- log|q_{37}| = log|q-parameter at 37| can be computed from the Tate curve expansion.
- For j = 2: the j²-scaled value is 4·log|q_{37}|; for j = 3: 9·log|q_{37}|.
- The discrepancy between Path A and Path B is (j²−1)·log|q_{37}| per prime per j-value.

This shows concretely that if the j²-scaling is NOT carried by the Θ-link, the
discrepancy at each bad prime v and each j is a nonzero real number — not a formal
indeterminacy that disappears automatically.

**Reproducible script** (verifies j-invariant and q-parameter structure only — not the
IUT diagram; conductor N=37 confirmed via LMFDB):

```python
# Sanity check: Weierstrass invariants of 37.a1 and j²-scaling at v=37
# E: y² + y = x³ − x  →  [a1,a2,a3,a4,a6] = [0,0,1,−1,0]
a1, a2, a3, a4, a6 = 0, 0, 1, -1, 0
b2 = a1**2 + 4*a2
b4 = a1*a3 + 2*a4
b6 = a3**2 + 4*a6
b8 = a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2
c4 = b2**2 - 24*b4
c6 = -b2**3 + 36*b2*b4 - 216*b6
Delta = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6

assert Delta == 37, f"Expected Delta=37, got {Delta}"
assert (c4, c6) == (48, -216), f"Got c4={c4}, c6={c6}"

import math
print(f"Delta = {Delta}")
print(f"c4 = {c4}, c6 = {c6}")
print(f"|Delta| = {abs(Delta)}, log|Delta| = {math.log(abs(Delta)):.6f}")
# j^2-scaling discrepancy at j=2,3:
for j in [1, 2, 3]:
    print(f"j={j}: j^2-scaling factor = {j**2}")
```

Expected output:
```
Delta = 37
c4 = 48, c6 = -216
|Delta| = 37, log|Delta| = 3.610918
j=1: j^2-scaling factor = 1
j=2: j^2-scaling factor = 4
j=3: j^2-scaling factor = 9
```
