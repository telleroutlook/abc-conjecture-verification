# A Closed Verification Kernel for the abc Conjecture

## A model-independent certificate system for Masser-Oesterlé and Mochizuki's IUT

**Document type:** final mathematical specification
**Scope:** the abc conjecture (Masser–Oesterlé, 1985) and Mochizuki's Inter-universal
Teichmüller Theory (IUT, 2012) as a candidate proof
**Foundational choice:** algebraic number theory, Diophantine geometry, and arithmetic
height functions
**Completion state:** the implication and verification kernel are complete; the required
arithmetic certificate has not been constructed; Mochizuki's IUT proof has not been
independently verified

---

## 0. Logical contract

### 0.1 What this document does

This document defines one mathematical object — a verified abc certificate — and proves
that any accepted instance implies the abc conjecture. It also specifies a machine-checkable
gate structure for evaluating Mochizuki's Inter-universal Teichmüller Theory as one
candidate supplier of that certificate.

The system is **logically closed** in the following precise sense: every accepted
conclusion follows from typed premises by stated theorems, every missing construction is
an explicit proof obligation, and no missing object is treated as if it existed. It is
**not proof-complete**: no accepted certificate for the abc conjecture is supplied here,
and Mochizuki's IUT proof is not verified by this document.

### 0.2 Atomic status grammar

Every item in the claim ledger has exactly one status.

| Status | Meaning | Logical use |
|---|---|---|
| **[DEF]** | Definition fixed by this document | May be unfolded |
| **[BASE]** | Standard theorem admitted as a foundation | May be used with its stated hypotheses |
| **[THM]** | Theorem proved in this document from definitions and base results | May be used downstream |
| **[OBL]** | Proof object or construction still required | May not be used as a theorem |
| **[OUT]** | Deliberately outside the certified profile | Has no downstream force |

Composite labels are forbidden. A conditional result is labelled **[THM]** and lists its
hypotheses; it is not assigned a hybrid status.

### 0.3 One-way dependency rule (non-anticipation barrier)

The construction is split into modules:

| Module | Contents |
|---|---|
| M0 | foundations, height theory, provenance barrier |
| M1 | rad function, Faltings heights, arithmetic geometry setup |
| M2 | key inequality construction (the Szpiro/Mochizuki step) |
| M3 | finiteness argument (counting exceptions) |
| M4 | known results (Faltings theorem, Szpiro equivalence, known abc triples) |
| M5 | comparison and bound verification |
| M6 | abc conclusion |

The only permitted module dependencies are:

```
M0 → M1 → M2 → M3 → M5 → M6
M0 → M4 → M5
```

In particular, M1, M2, M3 may not import M4, M5, M6. This is the formal
non-anticipation barrier: the construction of the key inequality and finiteness argument
may not see known abc triples, the Faltings/Szpiro comparison, or the conclusion.

---

## 1. The abc conjecture

### 1.1 The radical function

**[DEF]** For a positive integer n, the **radical** of n is

```
rad(n) = product of distinct prime factors of n.
```

Equivalently, rad(n) = prod_{p | n} p. For coprime integers a, b, c = a + b, the
**abc radical** is rad(abc) = rad(a) · rad(b) · rad(c) (since a, b, c pairwise coprime
implies their prime factorizations are disjoint).

**[BASE]** The function rad is completely multiplicative on squarefree inputs: rad(mn) =
rad(m) · rad(n) whenever gcd(m, n) = 1 (CL-01).

### 1.2 Quality of an abc triple

**[DEF]** The **quality** of an abc triple (a, b, c) with a + b = c and gcd(a, b) = 1 is

```
q(a, b, c) = log(c) / log(rad(abc)).
```

A triple has quality > 1 + ε if and only if c > rad(abc)^(1+ε).

### 1.3 Statement of the abc conjecture

**[DEF]** The **abc conjecture** (Masser–Oesterlé, 1985) is:

For every ε > 0, there exist only finitely many triples (a, b, c) of coprime positive
integers with a + b = c such that c > rad(abc)^(1+ε).

Equivalently: for all ε > 0, there exists a constant K_ε > 0 such that for all coprime
a + b = c:

```
c ≤ K_ε · rad(abc)^(1+ε).
```

The conjecture asserts the existence of such K_ε for every ε > 0, with no further
constraint on K_ε's dependence on ε.

### 1.4 Known results and context

**[BASE]** (Mason–Stothers) The abc theorem holds over function fields F(t): for
polynomials a(t), b(t), c(t) with a + b = c and gcd(a, b) = 1, deg(c) ≤ deg(rad(abc)) - 1.
This is proved and gives confidence in the integer analogue (CL-06).

**[BASE]** (Faltings, 1983) Every curve of genus ≥ 2 over Q has finitely many rational
points. This is the Mordell conjecture, proved, and is relevant via the Szpiro equivalence
(CL-05).

**[BASE]** (Oesterlé, 1988) The abc conjecture is equivalent to the *modified Szpiro
conjecture*: for every ε > 0 there is C(ε) > 0 such that, for every semi-stable
elliptic curve E over Q with minimal-model invariants c₄(E), c₆(E) and conductor
N_E,

```
max(|c₄(E)|³, |c₆(E)|²) ≤ C(ε) · N_E^(6+ε).
```

This is Oesterlé's Conjecture 4′. Both assertions remain unproved over the
integers (CL-02). The discriminant-only strong Szpiro form is closely related,
but it is not the precise equivalent asserted by CL-02 unless an additional
bridge is supplied.

---

## 2. The abc certificate

### 2.1 Certificate definition

**Definition 1 [DEF].** A **logical abc certificate** is a tuple

```
C = (ε_bound, K_ε, P_height, P_ineq, P_finiteness)
```

with the following fields.

| Field | Exact type |
|---|---|
| ε_bound | a positive rational number ε > 0 for which the bound is claimed |
| K_ε | a computable positive real constant |
| P_height | a proof of the height/rad bound setup and arithmetic geometry framework |
| P_ineq | a proof that c ≤ K_ε · rad(abc)^(1+ε) for all coprime a + b = c |
| P_finiteness | a proof that {(a,b,c) coprime, a+b=c : c > rad(abc)^(1+ε)} is finite |

The inequality in P_ineq is a universal statement over all coprime triples, not agreement
on a finite collection of known examples, and not a bound that holds only for triples
satisfying additional undisclosed hypotheses.

### 2.2 Certificate theorem

**Theorem 2 [THM].** If a logical abc certificate exists, then the abc conjecture holds
for that ε.

**Proof.** P_ineq provides c ≤ K_ε · rad(abc)^(1+ε) for all coprime a + b = c. This
directly gives the quantitative form of the abc conjecture for ε, hence finitely many
exceptions (quality > 1 + ε). P_finiteness gives the finiteness part. □

### 2.3 Exact strength of the certificate

**Theorem 3 [THM] (honesty check).** The existence of a logical abc certificate for every
ε > 0 is equivalent to the abc conjecture.

**Proof.** Forward: Theorem 2 for each ε. Converse: if the abc conjecture holds, then for
every ε > 0 the set of exceptions is finite, so K_ε = max over exceptions of
c / rad(abc)^(1+ε) is finite (the max of a finite set of positive reals, with K_ε = 1 if
the set is empty). This gives the certificate for each ε. □

Theorem 3 is a mandatory honesty check. The certificate is not an easier reformulation
by itself; it becomes a strategy only when K_ε and P_ineq are constructed without using
the abc conjecture as input or an abc-equivalent assertion.

---

## 3. Construction provenance

### 3.1 Admissible certificate

**Definition 4 [DEF].** An **admissible abc certificate** is

```
C_adm = (C, P_src)
```

where P_src is a replayable construction manifest satisfying the rules below. The
manifest is divided into two directed acyclic proof graphs:

1. **Construction graph:** produces P_height, P_ineq, and P_finiteness.
2. **Comparison graph:** imports the frozen output of the construction graph and
   verifies the bound against the known abc framework.

The construction graph is built and content-hashed before the comparison graph is admitted.

### 3.2 Allowed construction leaves

The construction graph may use:

- the definition of rad(n) and its elementary multiplicative properties;
- height functions, Faltings heights, and Arakelov intersection theory defined
  independently of the abc conjecture conclusion;
- local fields, valuations, and p-adic geometry defined independently;
- algebraic geometry and arithmetic geometry whose statements do not depend on the
  conclusion;
- Faltings' theorem and other proved foundational results (listed as [BASE]);
- the Mason–Stothers function-field abc theorem;
- deterministic construction rules fixed before the comparison step;
- formally proved lemmas listed in the immutable assumption manifest.

### 3.3 Forbidden construction leaves (spec §3.3 — auto-reject)

The construction graph may NEVER use:

- the abc conjecture itself as a hypothesis to prove the abc conjecture (circular);
- known abc triples or high-quality examples to fit, calibrate, or derive the constant
  K_ε;
- Szpiro's conjecture or its equivalent without supplying its own proof;
- the finiteness of S-integer solutions assumed without derivation (assumed Thue–Mahler
  theory);
- the Generalized Riemann Hypothesis (GRH) or other unproved hypotheses not explicitly
  declared as conditional hypotheses;
- IUT-specific: using the "identification of objects" across different Hodge theaters
  without an explicit, independently verifiable isomorphism proof — this is the
  Scholze–Stix objection, and any construction relying on it is flagged CIRCULAR
  pending independent verification;
- parameters selected by minimizing error against known abc examples;
- a bound that applies only to S-integers for a fixed finite set S, promoted as a
  universal statement.

### 3.4 What provenance can and cannot prove

The import barrier is syntactic and machine-checkable. It prevents direct fitting, hidden
data flow, and proof-DAG cycles. It does not decide semantic independence: the arithmetic
geometry of M1–M3 already encodes information about rational points, and no general
algorithm can decide whether an arbitrary theorem is secretly equivalent to the abc
conjecture. Therefore:

- machine checking verifies the declared dependency graph;
- the immutable assumption manifest must also receive mathematical review;
- the final proof remains valid only if every imported theorem is valid and none assumes
  the conclusion.

This limitation is explicit; "non-circular" is not treated as an automatic semantic oracle
(CL-08 is [OUT]).

---

## 4. The Mochizuki IUT context

### 4.1 Status of Mochizuki's claimed proof

Shinichi Mochizuki published a claimed proof of the abc conjecture via Inter-universal
Teichmüller Theory (IUT) in 2012 in four papers (IUTT-I through IUTT-IV). The key
quantitative step is **Corollary 3.12** of IUTT-III, which claims to establish the
crucial height inequality from which the abc bound follows.

In 2018, Peter Scholze and Jakob Stix visited Mochizuki in Kyoto and subsequently
published a report (the "Scholze–Stix report") identifying what they believe is a gap in
the proof. The gap concerns the **identification of objects in different Hodge theaters**:
Scholze and Stix argue that Mochizuki conflates objects that live in distinct copies of
mathematical structures (different "theaters") as if they were identical, without
providing an explicit isomorphism that would justify this identification.

Mochizuki disputes this characterization and maintains that the proof is correct. As of
2026, the mathematical community remains divided: the proof has not been accepted by the
broader research community outside of Mochizuki's group, but it has not been
definitively refuted either.

### 4.2 What this framework can adjudicate

This verification kernel can:

1. **Formalize what Corollary 3.12 must establish** (CORE-3): an explicit quantitative
   height inequality c ≤ K_ε · rad(abc)^(1+ε), proved from the IUT construction without
   assuming abc-equivalent inputs, with a machine-checkable provenance.

2. **Make the Scholze–Stix objection a specific gate failure**: CORE-3 includes a
   sub-obligation `core3.iut-corollary-312-independently-verified` which fails until an
   independent, machine-replayed proof of Corollary 3.12 is supplied. The Scholze–Stix
   dispute maps to this gate: the gate fails not because the objection is adjudicated
   but because independent verification has not been completed.

3. **Record both sides as open obligations**: Mochizuki's claim that the identification
   is valid, and Scholze–Stix's claim that it is not, are both recorded. The framework
   does not take sides; it records that the obligation is open.

4. **Accept any correct proof, IUT or not**: If a future proof passes all gates — whether
   via IUT, via a completely different approach, or via a formalized and independently
   verified version of IUT — CORE-5 fires and the conclusion holds.

### 4.3 What this framework cannot adjudicate

This verification kernel **cannot**:

- Decide whether Mochizuki's identification of objects is mathematically valid. That
  requires either a formalization that passes CORE-3's sub-obligation or a published
  refutation that would make the CIRCULAR flag definitive.
- Verify IUT independently without a machine-readable proof term for Corollary 3.12.
- Rule out that the abc conjecture is true and can be proved via IUT, via a different
  approach, or is yet unprovable.

CL-13: "Mochizuki's IUT proof passes all gates" is [OUT] — this is not established
by this document, and it is never to be self-declared established.

### 4.4 Corollary 3.12 gate specification (CORE-3 sub-obligation)

The key sub-obligation `core3.iut-corollary-312-independently-verified` requires:

1. A machine-readable proof term (in any replayable formal backend: Lean, Coq, Isabelle,
   Metamath, or equivalent) of the height inequality c ≤ K_ε · rad(abc)^(1+ε).

2. The proof term does not use abc or any abc-equivalent assertion as a hypothesis.

3. The proof term does not use the "identification of objects" across Hodge theaters
   without an explicitly proved isomorphism in the same formal system.

4. The proof term is independently replayed by the checker without trusting the author's
   claim that it is correct.

Until this sub-obligation is met, CORE-3 fails, and the Scholze–Stix concern is recorded
as the specific blocking obligation.

### 4.5 The honest boundary

The framework's output for Mochizuki's IUT is:

```
CORE-3 [OBL]: key inequality not independently verified.
  Blocking sub-obligation: core3.iut-corollary-312-independently-verified
  Reason: No machine-replayed proof of Corollary 3.12 supplied.
  Scholze-Stix dispute: identification of objects across Hodge theaters
    requires an explicit isomorphism proof; this has not been formalized.
  This is NOT a determination that IUT is wrong.
  This IS a determination that the obligation is open.
```

---

## 5. Gate graph and pass conditions

### 5.1 Core gates

```
CORE-0 (abc def) → CORE-5 (conclusion)
CORE-1 (provenance) → CORE-2 (height framework) → CORE-3 (key inequality) → CORE-5
CORE-4 (finiteness) → CORE-5
```

| Gate | Deliverable | Pass condition | Automatic failure |
|---|---|---|---|
| CORE-0 | formal definition of abc, rad, certificate | rad definition, certificate tuple, Theorem 2, honesty check all available | abc statement is ambiguous or quality function undefined |
| CORE-1 | immutable assumption and dependency manifest | construction modules have no forbidden imports; DAG acyclic; no forbidden leaves | known abc triples, Szpiro assumed, IUT identification-without-isomorphism |
| CORE-2 | height/rad framework (P_height) | Faltings heights, Arakelov setup, rad bound constructed without forbidden inputs | fitted parameters, assumed finiteness, abc-equivalent input |
| CORE-3 | key inequality P_ineq (Mochizuki's Cor. 3.12) | c ≤ K_ε · rad(abc)^(1+ε) proved for all coprime triples; Cor. 3.12 independently verified | identification of objects without isomorphism; abc assumed; bound applies only to finite S |
| CORE-4 | finiteness of exceptions P_finiteness | finitely many (a,b,c) with c > rad(abc)^(1+ε) proved uniformly | finiteness assumed; finiteness proved only for specific families |
| CORE-5 | theorem application | checker derives Theorem 2 from passed CORE-0..4 | any producer-supplied PASS flag is trusted |

CORE-5 has no independent mathematical assumption. It is a deterministic application
of the verified theorem.

### 5.2 CORE-3 sub-obligations (IUT gate)

CORE-3 includes the following sub-obligations:

- `core3.height-inequality-stated`: the inequality c ≤ K_ε · rad(abc)^(1+ε) is stated
  as a formal claim with explicit ε and K_ε.
- `core3.height-inequality-proved`: the inequality is proved from the construction
  without forbidden inputs.
- `core3.iut-corollary-312-independently-verified`: a machine-replayed formal proof of
  Corollary 3.12 (or an equivalent result) is provided and independently checked. This
  sub-obligation is currently OPEN, with the Scholze–Stix concern recorded as the
  blocking reason.

---

## 6. Verification artifact

### 6.1 Normative manifest

A submission contains the following immutable fields:

| Field | Required content |
|---|---|
| schema_version | exact version of this certificate contract |
| target_id | identifier for the abc conjecture statement |
| foundation_hash | proof-kernel and admitted-base manifest |
| source_dag_hash | complete construction dependency graph |
| source_lock_hash | frozen arithmetic inputs and parameter rules |
| rad_function_hash | formal definition of rad(n) |
| height_framework_hash | formal construction of P_height |
| inequality_proof_hash | proof term for P_ineq |
| finiteness_proof_hash | proof term for P_finiteness |
| checker_hash | verifier implementation and theorem library |
| epsilon_bound | the specific ε > 0 being claimed |
| constant_k_epsilon | the explicit constant K_ε |

The status is not an input field. Only the checker may emit a result.

### 6.2 Checker algorithm

The verifier performs the following steps in order:

1. Parse the manifest and reject unknown or missing normative fields.
2. Recompute all artifact hashes.
3. Verify that the source graph is acyclic.
4. Verify the module import policy of Section 0.3.
5. Scan construction files for forbidden construction leaves (Section 3.3).
6. Replay the construction of P_height.
7. Replay P_ineq, verifying no abc-equivalent hypothesis is used.
8. Replay P_finiteness.
9. Verify the IUT sub-obligation (core3.iut-corollary-312-independently-verified).
10. Instantiate Theorem 2.
11. Emit VERIFIED only if every prior step succeeds; otherwise emit REJECTED with the
    first failed predicate.

A candidate generator cannot certify its own inequality, constant, or status. Each is
recomputed or replayed from lower-level witnesses.

---

## 7. Regression and adversarial tests

### 7.1 Document-level tests

| Test ID | Predicate |
|---|---|
| DOC-01 | every claim status matches exactly one token in Section 0.2 |
| DOC-02 | no composite status label occurs |
| DOC-03 | gate identifiers are unique and every referenced gate is defined |
| DOC-04 | Definitions 1 and 4 occur before downstream use |
| DOC-05 | the module graph and core gate graph are acyclic |
| DOC-06 | every field marked [OBL] appears in the gate table |
| DOC-07 | no bibliography or framework-equivalence claim is required by a proof |

### 7.2 Mathematical unit tests

**TEST-ABC1 — CORE-0 definitions.** The checker must accept the abc statement, rad
definition, certificate tuple, and Theorem 2 as structural definitions and theorems.

**TEST-ABC2 — CORE-1 provenance clean.** A construction manifest with no forbidden
imports and no known-triple data must pass.

**TEST-ABC3 — CORE-2 OBL.** In the absence of a supplied height framework, CORE-2
must fail with an open obligation message.

**TEST-ABC4 — CORE-3 OBL with IUT gate.** CORE-3 must fail with two messages:
(a) the key inequality is not supplied, and (b) the IUT Corollary 3.12 sub-obligation
is open with the Scholze–Stix dispute recorded.

**TEST-ABC5 — CORE-4 OBL.** In the absence of a finiteness proof, CORE-4 must fail.

**TEST-ABC6 — circular abc rejection.** A construction that uses known high-quality
abc triples to derive K_ε must fail CORE-1 with the forbidden-leaf scanner.

**TEST-ABC7 — non-anticipation barrier.** A construction module M2 that imports from M4,
M5, or M6 must fail CORE-1.

**TEST-ABC8 — CORE-5 blocked without CORE-4.** CORE-5 must fail when CORE-4 has not
passed.

**TEST-ABC9 — CL-03/04 implication and honesty theorems.** The checker must record
Theorem 2 (CL-03) and Theorem 3 / honesty check (CL-04) as proved [THM] items whose
proofs use no forbidden inputs.

**TEST-ABC10 — CL-07 syntactic provenance theorem.** The checker must confirm that
the import-barrier scan is a decidable syntactic check (CL-07), explicitly not
claiming semantic independence (CL-08 is [OUT]).

---

## 8. Stop conditions

Work must stop, narrow its claim, or create a new formally proved profile if any of
the following occurs:

1. the construction imports known abc triples or high-quality examples before the
   comparison step;
2. K_ε is derived by minimizing error against known examples;
3. Szpiro's conjecture or an abc-equivalent assertion is assumed without proof;
4. the key inequality is proved only for a fixed finite set S of primes, promoted as
   a universal statement;
5. IUT's identification of objects across Hodge theaters is used without a formalized
   isomorphism proof;
6. finiteness of exceptions is assumed rather than derived;
7. a conditional result (assuming GRH or another unproved hypothesis) is promoted
   to an unconditional theorem without declaring the hypothesis;
8. a candidate-generated status is trusted instead of recomputing the pass predicate;
9. an obligation is renamed an axiom and then used to claim completion;
10. "Mochizuki's IUT proof is correct" is asserted without a machine-replayed formal
    proof of Corollary 3.12.

---

## 9. Atomic claim ledger

| Claim ID | Atomic statement | Status |
|---|---|---|
| CL-01 | rad(n) is well-defined and multiplicative for coprime inputs | [DEF] |
| CL-02 | abc conjecture is equivalent to the modified Szpiro conjecture (Oesterlé Conjecture 4′) | [BASE] |
| CL-03 | Certificate (ε_bound, K_ε, P_height, P_ineq, P_finiteness) implies abc | [THM] |
| CL-04 | Certificate existence is equivalent to abc (honesty check) | [THM] |
| CL-05 | Faltings theorem: finitely many rational points on genus ≥ 2 curves | [BASE] |
| CL-06 | Mason–Stothers theorem: abc over function fields (proved) | [BASE] |
| CL-07 | Provenance barrier is syntactically machine-checkable | [THM] |
| CL-08 | Provenance barrier decides all semantic circularity | [OUT] |
| CL-09 | Height/rad framework constructed without forbidden inputs | [OBL] |
| CL-10 | Key inequality c ≤ K_ε · rad(abc)^(1+ε) proved (Cor. 3.12) | [OBL] |
| CL-11 | Finiteness of exceptions proved uniformly in a, b, c | [OBL] |
| CL-12 | abc conjecture is proved | [OUT] |
| CL-13 | Mochizuki's IUT proof passes all gates | [OUT] |

For CL-07, the theorem is only the syntactic statement: a correctly implemented
import checker rejects a graph containing a forbidden dependency. It does not upgrade
to the excluded semantic claim CL-08.

CL-12 and CL-13 are [OUT]: this document does not prove the abc conjecture, and it
does not verify Mochizuki's IUT proof. These outcomes are never to be self-declared.

---

## 10. Final theorem interface

The complete certified interface is:

```
ε > 0 (rational);
K_ε > 0 (computable);
P_height: height/rad framework constructed without forbidden inputs;
P_ineq:   c ≤ K_ε · rad(abc)^(1+ε) for all coprime a + b = c;
P_finiteness: |{(a,b,c) coprime, a+b=c : c > rad(abc)^(1+ε)}| < ∞;
all of the above constructed under the provenance contract
  ⟹  abc conjecture (for this ε)
```

The implication is proved (Theorem 2, [THM]). The construction premises are not
(CL-09, CL-10, CL-11 are [OBL]). The IUT sub-obligation
(core3.iut-corollary-312-independently-verified) is open.

This is the final logical boundary of the system.
