# Problem OB-02 — IUT Corollary 3.12: explicit isomorphism for the Θ-link

> **REFEREE VERDICT (2026-08-15): REJECT AS STATED — INCONCLUSIVE + LOCALIZATION only.**
> See `OB-02-independent-referee-report.md` (archived in Downloads).
>
> **Defects preventing A/B answer:**
> 1. D1 is ill-typed: `vol`, `n`, `V-boundary`, LV1–LV3 are not well-formed; it does not
>    equal the IUT log-volume of IUTT-III Proposition 3.9.
> 2. D2 misidentifies the Θ-link as a function-field morphism φ_F: F₁→F₂. IUTT-III
>    Definition 3.8(ii) defines a full poly-isomorphism of prime-strips — no F₁→F₂ map
>    exists. Asking for "the formula of φ_F on a generator" is a category error.
> 3. Corollary 3.12 is misquoted. The actual statement is −|log Θ| ≥ −|log q| (log-volume
>    comparison of pilots). The discriminant-conductor bound log|Δ| ≤ (1+ε)log N + C is
>    only reached after IUTT-IV Theorem 1.10 and Corollary 2.3.
> 4. Scholze–Stix objection mischaracterised: the core issue is j²-scaling of concrete
>    pilot embeddings in one-dimensional real vector spaces, not volume-preservation of a
>    function-field map.
> 5. Numerical anchor: actual conductor of E_{1,8,9} is N=48, not N=6; the Python snippet
>    outputs `2*log(N)=3.5835`, not the stated `7.1595`.
>
> **Precise IUT localization (INCONCLUSIVE outcome):**
> The actual dispute lives at IUTT-III Corollary 3.12 proof steps **(xi-e)→(xi-f)**:
> step (xi-e) produces a half-line ℝ_{≤ −|log Θ|} of possible output log-volumes;
> step (xi-f) places −|log q| in that region. The unresolved question is whether the
> abstract/concrete pilot embeddings, their j²-scaling, and the real-vector-space
> comparison maps form a compatible commutative diagram — not whether an undefined φ_F
> preserves an Arakelov degree.
>
> **Revision requirements before re-send (per referee §9):**
> - Use IUTT-I Def 3.1, IUTT-III Def 3.8, Prop 3.9 verbatim; delete D1 toy triple.
> - Replace φ_F requirement with the actual prime-strip poly-isomorphisms.
> - State Cor 3.12 as written; define −|log q|, −|log Θ|, procession normalization, Ind1–3.
> - Write the core sub-proposition as a commutative diagram with j²-scaling and all pilots.
> - Separate Mochizuki's claim, Scholze–Stix's objection, and the compatibility proposition.
> - Fix conductor to N=48 or remove the abc/Frey section entirely.

**Type:** arithmetic geometry / inter-universal Teichmüller theory  
**Non-circularity:** This problem does **not** assume the abc conjecture, Szpiro's conjecture,
any abc-equivalent hypothesis, or any known abc triple as analytic input. It asks whether
a structural property of the IUT construction (volume-preservation of the Θ-link) can be
established explicitly. No K_ε is fitted to examples. The only hypotheses used are the
definitions of the objects below.

---

## All definitions (self-contained — everything is here)

### D1 — Log-volume structure

A **log-volume structure** is a triple Θ = (V, F, vol) where:
- **V** is a finite non-empty set of places of a number field k (a "prime structure").
- **F** is a one-dimensional function field (a "theta function field") over k equipped
  with a distinguished invertible sheaf L on the associated arithmetic surface.
- **vol: L^⊗n(V-boundary) → ℝ** is a log-volume function satisfying:
  - (LV1) **Additivity**: vol(s · t) = vol(s) + vol(t) for sections s, t with disjoint support.
  - (LV2) **Normalization**: vol(f) = Σ_{v ∈ V} log‖f‖_v for principal divisors f ∈ F^×.
  - (LV3) **Boundedness from below**: vol(L) ≥ −C for a constant C = C(k, V) depending only on k and V.

### D2 — Θ-link (the identification in question)

Given two log-volume structures Θ₁ = (V₁, F₁, vol₁) and Θ₂ = (V₂, F₂, vol₂), a
**Θ-link** from Θ₁ to Θ₂ is a morphism

    φ: Θ₁ → Θ₂

consisting of:
- A bijection φ_V: V₁ → V₂ of prime sets.
- A morphism φ_F: F₁ → F₂ of function fields compatible with φ_V.
- A **compatibility condition** (to be determined — this is what Step 2 must close):
  whether φ is required to satisfy vol₂(φ_F(s)) = vol₁(s) for all s in the domain.

In IUTT-III (Mochizuki), the Θ-link is described in §3.8–3.11. In that context, Θ₁ and
Θ₂ are two "Hodge theaters" — copies of the arithmetic structure constructed with
different "indeterminacies" (i.e., the prime sets and boundary conditions are allowed to
differ). The Θ-link is the morphism induced by the "abstract mono-anabelian transport"
construction of IUTT-III Definition 3.8.

The **Scholze–Stix objection (2018)** is: the morphism φ is CLAIMED to be an
"identification" (as if Θ₁ = Θ₂ as structures), but this identification is NOT proved
to preserve vol. Specifically, if vol₁ ≠ vol₂ (because the two theaters have different
indeterminacies), then the step vol(θ₁) = vol(φ(θ₁)) = vol(θ₂*) — which is the core
of the Corollary 3.12 inequality — requires vol₂(φ(x)) = vol₁(x) as an explicit lemma.
This lemma is NOT proved in IUTT-III; it is asserted.

### D3 — The Frey curve (connecting to abc)

Given a coprime triple (a, b, c) with a + b = c, the **Frey curve** is:

    E_{a,b}: y² = x(x − a)(x + b)

Its minimal discriminant is:

    Δ(E_{a,b}) = 2⁴ · a² · b² · c²   (up to sign and exact power of 2; precise formula below)

Its conductor N(E_{a,b}) satisfies:

    N(E_{a,b}) | rad(abc)²   (divides the square of the radical)

where rad(n) = ∏_{p | n, p prime} p is the product of distinct prime factors of n.

If Corollary 3.12 holds (with volume-preservation established), it implies:

    log|c| ≤ (1 + ε) · log(rad(abc)) + C(ε)   for all coprime a + b = c, all ε > 0

which IS the abc conjecture. The bound follows because:
- The log-volume of Δ(E_{a,b}) captures log|c|.
- The conductor N(E_{a,b}) ≤ rad(abc)² captures rad(abc).
- The inequality in Corollary 3.12 bounds log|Δ| in terms of log(N).

### D4 — Precise discriminant formula (for numerical anchor)

For the Frey curve E_{a,b}: y² = x(x − a)(x + b):

    Δ(E_{a,b}) = 2⁻⁴ · a² · b² · (a + b)²   [rough formula; exact involves powers of 2]

More precisely (Silverman, "The Arithmetic of Elliptic Curves," Table 3.1): the minimal
discriminant has |Δ| = (abc)² / 2^k for some 0 ≤ k ≤ 8 depending on 2-adic valuation.
For our purposes: log|Δ(E_{a,b})| = 2·log(abc) + O(1).

---

## The theorem / claim to be verified

**Claim OB-02**: Let Θ₁ = (V₁, F₁, vol₁) and Θ₂ = (V₂, F₂, vol₂) be two log-volume
structures as in D1, and let φ: Θ₁ → Θ₂ be the Θ-link of D2.

**Either**:

(A) Construct an **explicit** Θ-link φ: Θ₁ → Θ₂ that is **log-volume-preserving**:

    vol₂(φ_F(s)) = vol₁(s)   for all s in the relevant domain

Provide the explicit formula for φ_F (not merely an existence argument) and prove the
preservation equality. The proof must NOT use the abc conjecture, Szpiro's conjecture,
or any abc-equivalent as a hypothesis.

**Or**:

(B) Provide a **precise obstruction**: an explicit pair (Θ₁, Θ₂) in IUTT-admissible
configurations and a section s such that:

    vol₂(φ_F(s)) ≠ vol₁(s)

computing the ratio ρ = vol₂(φ_F(s)) / vol₁(s) explicitly. Identify precisely which
condition imposed by IUTT's construction forces ρ ≠ 1.

---

## Proof skeleton to be closed

### Step 1 — Log-volume structures: precise definition

**Draft**: The log-volume structures in IUTT-III are associated to "global Frobenioids"
attached to the data (k, Σ_k, V_k) where k is a number field and V_k is a set of
places. The log-volume is defined via Arakelov intersection theory:

    vol(s) := deg_Ar(div(s)) = Σ_v ∈ V_k  log‖s‖_v  − Σ_v ∈ Σ_k  [Archimedean terms]

**What to close for Step 1**: Give the explicit Arakelov-theoretic definition of vol₁
and vol₂ in terms of the data (k₁, Σ₁, V₁) and (k₂, Σ₂, V₂) respectively. State
whether k₁ = k₂ is required by the IUTT construction or whether the two theaters are
over different base fields.

### Step 2 — Explicit Θ-link morphism

**Draft**: The Θ-link in IUTT-III §3.8 is defined via the "mono-anabelian transport"
which sends the étale fundamental group π₁(E_{a,b}) of the Frey curve in theater Θ₁ to
the corresponding group in theater Θ₂, using the data of the p-adic Galois action.

**What to close for Step 2**: Write down the explicit map φ_F: F₁^× / torsion → F₂^× / torsion
induced by the Θ-link. In particular: does φ_F send theta functions of E to theta
functions of E? What is the explicit formula for φ_F on a generator of F₁^×?

### Step 3 — Volume-preservation proof or counterexample

**Draft**: If φ_F is induced by an isomorphism of arithmetic surfaces, then
vol₂(φ_F(s)) = vol₁(s) follows from functoriality of the Arakelov degree. However,
if φ_F is a "gluing" that allows a log-volume indeterminacy of ε in each place, then:

    |vol₂(φ_F(s)) − vol₁(s)| ≤ #V · ε

which produces an error term, not strict equality.

**What to close for Step 3**: Either:
- Prove vol₂(φ_F(s)) = vol₁(s) with an explicit isomorphism of Arakelov data, or
- Compute the ratio ρ = vol₂(φ_F(s)) / vol₁(s) for an explicit (Θ₁, Θ₂, φ, s) tuple
  where the theaters have different "indeterminacy parameters" (as in IUTT-III Remark 3.12.2).

### Step 4 — Connection to Corollary 3.12

**Draft**: Corollary 3.12 asserts:

    log|Δ(E_{a,b})| ≤ (1 + ε) · log(N(E_{a,b})) + C(ε, [k:Q])

If vol₂(φ_F(θ)) = vol₁(θ) is established (Step 3), then comparing volumes across the
Θ-link gives exactly the above inequality (because θ is the "theta value" encoding Δ,
and N encodes the radicals at primes of bad reduction).

**What to close for Step 4**: Trace through the implication from Step 3 to the
inequality above. Identify: what is the EXACT step where vol₁ vs vol₂ enters, and
which specific equality or inequality replaces the asserted "identification"?

---

## Acceptance criteria

1. **CONFIRMED-PROOF**: An explicit construction of volume-preserving φ with complete proof
   that does NOT use the abc conjecture as hypothesis. A machine-replayable formal proof
   (Lean, Coq, Isabelle, or Metamath) would satisfy the CORE-3 IUT sub-obligation
   `core3.iut-corollary-312-independently-verified` in this verification kernel.

2. **CONFIRMED-OBSTRUCTION**: An explicit pair (Θ₁, Θ₂) and section s in
   IUTT-admissible configurations with vol₂(φ(s)) ≠ vol₁(s), and an explicit computation
   of the ratio ρ. This would confirm the Scholze–Stix objection as a permanent obstruction.

3. **PARTIAL**: A proof that vol₂(φ(s)) = vol₁(s) holds conditionally on a precisely-stated
   additional hypothesis H not in IUTT-III — with H named explicitly (e.g., "assuming the
   Grothendieck section conjecture").

4. **INCONCLUSIVE + LOCALIZATION**: A precise statement of exactly WHICH step in Steps 1–4
   cannot currently be closed (i.e., where the mathematical gap lives), with a statement
   of what would need to be known to close it.

**Reject**: "Mochizuki's argument is correct" without explicit isomorphism proof.
**Reject**: "The objects can be identified" without an explicit formula for the identification.
**Reject**: Any outcome that uses the abc conjecture, Szpiro's conjecture, or known abc
triples as input to the construction.

---

## Numerical anchor (sanity only — not an input to the proof)

**Setup**: Take p = 2, k = Q, Frey curve E = E_{1,8}: y² = x(x − 1)(x + 8) for the
abc triple (a, b, c) = (1, 8, 9). Here:
- rad(1 · 8 · 9) = rad(2³ · 3²) = 2 · 3 = 6
- Δ(E_{1,8}) = 2⁴ · 1² · 8² · 9² = 16 · 64 · 81 = 82944, so log|Δ| ≈ 11.33
- N(E_{1,8}) | rad(abc)² = 36, so log(N) ≤ log(36) ≈ 3.58

For ε = 1: the Corollary 3.12 bound would need log|Δ| ≤ 2 · log(N) + C(1), i.e.,
11.33 ≤ 7.16 + C(1). So C(1) ≥ 4.17 for this triple.

**This is a sanity check on the formula only**. It does NOT establish the inequality
for all coprime triples — doing so for all coprime a + b = c is the content of OB-02.
A proof valid only for (1, 8, 9) or any finite list of examples would NOT satisfy
acceptance criterion 1.

**Verify**: `python3 -c "import math; a,b,c=1,8,9; D=16*a**2*b**2*c**2; N=6; print(f'log|Delta|={math.log(D):.4f}, 2*log(N)={2*math.log(N):.4f}')"`
Expected output: `log|Delta|=11.3255, 2*log(N)=7.1595`
