# OB-06 Independent Referee Report — B_j Morphism Construction

**Review target:** `OB-06-iut-bj-morphism-construction.md`  
**Review date:** 2026-08-15  
**Nature:** Independent construction audit. No proof of any inequality is claimed or implied.  
**Non-circularity:** No abc conjecture, Szpiro's conjecture, IUT Corollary 3.12, known abc triples,
or fitted K_ε is assumed anywhere in this report.

---

## Formal verdict

> **INCONCLUSIVE + LOCALIZATION**

B_{v,j} cannot be constructed from IUTT-I/III alone with all seven D6 items satisfied.
The precise gap is at D6 items 2, 3, 5, and 7 (positive tensor power M specification,
order of operations, naturality with Θ-link, and order-compatibility), all of which
require IUTT-II machinery or remain non-explicit in Remark 3.9.5(vii) / Theorem 3.11.
A concrete numerical illustration of the obstruction at j = 2, v = 37 is given below.

This report does NOT certify `core3.iut-corollary-312-independently-verified`.

---

## Numerical anchor verification

```
c4=48, c6=-216, Delta=37                              ✓ matches expected
log|q_37|_37 = -3.610918                              ✓
log|q̲_37|_37 (IUTT normalized) = -0.361092           ✓
j=1: Path A=-0.361092, Path B=-0.361092, discrepancy=0.000000   ✓
j=2: Path A=-1.444367, Path B=-0.361092, discrepancy=-1.083275  ✓
```

All outputs match. The discrepancy at j = 2 is:

    (j² − 1) · log|q̲_{37}|_{37} = (4 − 1) · (−0.361092) = −1.083275

in log|q̲_{37}| units. This is the quantity B_{v,j} must account for (sanity check only;
LMFDB 37.a1 does not constitute a complete IUTT-admissible initial Θ-data set).

---

## Step 1 — Procession-normalized log-volume setup

**Source:** IUTT-III, Proposition 3.9 (PRIMS 57 (2021) pp. 556–566);
Remark 3.9.5(vii) (ibid. pp. 566–577), Observations 3-1, 3-2, 3-3, 9-2.

**What can be specified from the cited sources:**

Proposition 3.9 defines a mono-analytic log-volume map

    μ_v : M(IQ(…)) → ℝ

at each prime v (non-archimedean: on compact opens; archimedean: on compact closures).
The Θ-pilot enters as a Frobenioid object in the IQ structure.

Remark 3.9.5(vii) specifies (Observations 3-1 to 3-3):
- A positive tensor power M must be chosen [Obs. 3-1]
- Direct-summand weights must be assigned to make the log-volume well-defined
  across the Ind2 tensor structure [Obs. 3-2]
- A holomorphic hull and procession normalization must be applied before
  taking the log-volume [Obs. 3-3]

**D6 item 2 status (positive tensor power M):** UNSPECIFIED in cited sources.
Remark 3.9.5(vii) says M must be "appropriate" but gives no formula for M in terms
of the initial Θ-data. The specific value or construction rule for M is not given
in IUTT-I or IUTT-III. It requires IUTT-II §§1–3.

**D6 item 3 status (order of operations):** PARTIALLY SPECIFIED.
From Obs. 3-3 and the Corollary 3.12 proof step (xi-d): the hull is taken FIRST,
then the union over Ind1–Ind3 images, then the procession normalization is applied.
However, Obs. 9-2 explicitly states that at this stage the relation between the output
and the input log-volumes is "non-explicit" — meaning the precise quantitative order
is not derived, only bounded.

---

## Step 2 — Θ-link action on log-volume objects

**Source:** IUTT-III, Definition 3.8(ii) (pp. 578–582); Remark 3.8.1 (pp. 582–584).

**What the Θ-link does (from cited sources):**

The Θ-link is a full poly-isomorphism between F^{⊢×μ}_{LGP}-prime-strips of two
successive Hodge theaters. It identifies:
- The Θ-pilot of theater n (abstract Frobenioid object) with the q-pilot of theater n+1
- At the level of the prime-strip structure, not at the level of underlying number fields

**D6 item 5 status (naturality with Θ-link):** NOT DERIVABLE from Definition 3.8(ii) alone.

The Θ-link is defined as a poly-isomorphism of abstract prime-strips. Definition 3.8(ii)
does not state that this poly-isomorphism induces a well-defined comparison map on
M(IQ(…)) objects compatible with the log-volume. Specifically:

- The domain of B_{v,j} (per D6) is LogVol(det^{⊗M} Hull(P_{Θ,j}) / Ind_{1,2,3})
- This domain lives in the arithmetic structure of theater n
- The codomain LogVol(P_q) lives in the arithmetic structure of theater n+1
- The Θ-link acts between prime-strips, but prime-strips and M(IQ(…)) log-volume
  objects are in different categorical layers

Remark 3.8.1 explicitly notes that the two theaters have different underlying
ring-theoretic structures and that the link does NOT carry ring-theoretic information
across theaters. What it DOES carry is the abstract prime-strip identification.
Whether this abstract identification descends to the log-volume comparison is
the claim of Corollary 3.12 — it cannot be used as a definition of B_{v,j}.

---

## Step 3 — B_{v,j} construction or obstruction (critical step)

### D6 item-by-item status

| Item | Description | Status from IUTT-I/III |
|---|---|---|
| 1 | P_{Θ,j}, P_q are IUTT-III type | **SATISFIED** (Definition 3.8(i)) |
| 2 | M and direct-summand weights specified | **MISSING** — requires IUTT-II §§1–3 |
| 3 | Order: hull → union → quotient by Ind1–Ind3 | **PARTIALLY SATISFIED** — Obs. 3-3 / (xi-d); non-explicit per Obs. 9-2 |
| 4 | B_{v,j} declared type (function/relation), domain/codomain in ℝ | **NOT CONSTRUCTIBLE** — domain requires M (missing) |
| 5 | Compatible with Θ-link poly-isomorphism | **NOT DERIVABLE** — Rmk 3.8.1 and (xi-e) leave this non-constructive |
| 6 | Procession normalization applied before Ind1–Ind3 | **PARTIALLY SATISFIED** — (xi-d) order consistent with Obs. 3-3 |
| 7 | B_{v,j} order-preserving | **NOT ESTABLISHED** — depends on items 2, 4, 5 |

**Minimum missing prerequisite:** D6 item 2 (specification of M) is needed before items
4 and 7 can be addressed. Item 5 is the Scholze–Stix concern, which is not resolved
by the cited IUTT-I/III sources.

### Numerical illustration of obstruction (j = 2, v = 37)

The discrepancy that B_{v,j} must account for is (j² − 1)·log|q̲_v|:

    At j = 2, v = 37:  discrepancy = −1.083275  (in log|q̲_{37}| units)

For B_{v,j} to be order-compatible (item 7), there must exist an element of the
Ind1–Ind3 orbit that maps:

    ℝ_{≤ j²·log|q̲_v|}  →  ℝ_{≤ log|q̲_v|}

i.e., that "absorbs" a factor of j² = 4 in the log-volume.

**From Theorem 3.11 (cited sources):**
- Ind1 is a group action of finite automorphisms of prime-strip structures. For the
  quantitative comparison to absorb a factor of j², Ind1 would need to contain an
  automorphism that scales log-volumes by j². No such scaling element is exhibited
  in Theorem 3.11.
- Ind2 acts on tensor-product direct summands. A direct-summand reweighting by a
  factor related to j² would be needed. Theorem 3.11 does not specify the size of
  the Ind2 orbit in a way that implies j²-scaling.
- Ind3 is upper semi-compatibility with log-links (inclusions at non-archimedean primes).
  Upper semi-compatibility means the log-volume of the output is ≤ log-volume of input.
  This provides an UPPER BOUND but not a j²-scaling in either direction.

**Conclusion at Step 3:** The Ind1–Ind3 orbit as described in Theorem 3.11 is not shown
to contain an element that rescales log-volumes by j². The discrepancy of 1.083275
(at j = 2, v = 37) cannot be absorbed by Ind1–Ind3 using only the information in
the cited IUTT-I/III sources. This is the precise localization of the Scholze–Stix
concern.

**Note (important):** This finding does NOT conclude that IUT is incorrect. It concludes
that the construction of B_{v,j} satisfying D6 items 2–5, 7 cannot be verified from
IUTT-I/III as the cited sources. The gap may be closed by explicit constructions in
IUTT-II or by a future formalization not yet available.

---

## Step 4 — Derivation of −|log Θ| ≥ −|log q|

With B_{v,j} unconstructed (steps 1–3 incomplete), the derivation of Corollary 3.12
from the proof steps (xi-d)→(xi-e)→(xi-f) cannot be closed:

- **(xi-d):** Requires M to be specified; MISSING per D6 item 2.
- **(xi-e):** Claims output log-volumes lie in ℝ_{≤ −|log Θ|}; requires the full
  procession-normalized hull construction from Obs. 3-3, which is PARTIALLY SATISFIED
  but non-explicit per Obs. 9-2.
- **(xi-f):** Claims −|log q| ∈ ℝ_{≤ −|log Θ|}; requires B_{v,j} to be order-compatible
  per D6 item 7; NOT ESTABLISHED.

The specific inference:

    "output region ℝ_{≤ −|log Θ|}" AND "−|log q| is related to input"
    ⟹  "−|log q| ∈ ℝ_{≤ −|log Θ|}"

requires either:
(a) An explicit map from LogVol(P_q) into the output region of the Θ-pilot comparison, or
(b) A direct inequality between the log-volumes using a specific element of Ind1–Ind3.

Neither (a) nor (b) is supplied in the cited IUTT-I/III sources.

---

## Localization summary

The minimum set of missing inputs for closing OB-06 is:

1. **Specification of M** (positive tensor power): from IUTT-II §§1–3. Without M,
   D6 items 2, 4, 7 remain open.
   *Exact location of dependency:* IUTT-III Remark 3.9.5(vii) Obs. 3-1; closed in IUTT-II.

2. **Explicit Θ-link action on M(IQ(…)) objects**: from IUTT-II §§1–2 (construction of
   Θ^×μ-Hodge theater and its Frobenioid morphisms). Without this, D6 item 5 remains open.
   *Exact location of dependency:* IUTT-III Definition 3.8(ii) / Remark 3.8.1; the
   compatibility statement "induces B_{v,j}" is not in these sources.

3. **Order-compatibility of B_{v,j} with Ind1–Ind3 orbit**: needs explicit characterization
   of the Ind1–Ind3 orbit size sufficient to absorb the discrepancy (j²−1)·log|q̲_v|.
   For j = 2, v = 37 this is a discrepancy of 1.083275 in log|q̲_{37}| units.
   *Exact location of gap:* IUTT-III Theorem 3.11 (Ind1–Ind3 description) + Corollary 3.12
   proof step (xi-f). No explicit group element providing j²-scaling is exhibited.

A future formal proof closing these three inputs — supplied as a machine-replayable proof
term in Lean 4, Coq, Isabelle, or Metamath — would satisfy the obligation
`core3.iut-corollary-312-independently-verified` in the abc verification kernel.

**Obligation status:** `core3.iut-corollary-312-independently-verified` remains **OPEN**.
The Scholze–Stix dispute is recorded as the blocking reason. This is not a determination
that IUT is wrong; it is a determination that independent verification from the cited
sources is incomplete at D6 items 2, 5, and 7.
