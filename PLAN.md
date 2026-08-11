# PLAN.md — abc Conjecture Verification Kernel

**Mathematical status:** `LOGICALLY_CLOSED / NOT_PROOF_COMPLETE`.
**abc conjecture:** `[OUT]` — not proved here, never self-declared.
**IUT (Mochizuki):** `[OUT]` — not verified here, never self-declared.
**Authoritative math:** `spec/SPECIFICATION.md`. This file records the *program* and the
*execution phases*; the spec records the contract.

---

## Part I · Identity and boundaries

This project builds and operates a **verification kernel**: it defines one object — a
verified abc certificate `(ε_bound, K_ε, P_height, P_ineq, P_finiteness)` — and has
proved (`[THM]`) that any accepted instance implies the abc conjecture. It does **not**
construct such a certificate. The deliverable is the *system*, not a proof of abc.

### Hard boundaries (non-negotiable; see CLAUDE.md for the operational form)

- **B1 — Non-anticipation.** Construction modules `M1,M2,M3` may not import target /
  comparison / conclusion `M4,M5,M6`. Machine-checked as an acyclic import DAG.
- **B2 — Forbidden construction leaves.** No known abc triples; no abc or Szpiro
  assumed; no IUT identification-without-isomorphism; no fitted K_ε; no GRH unless
  declared. (spec §3.3)
- **B3 — Universal inequality.** P_ineq covers ALL coprime a+b=c, never just a finite
  set S or a specific family. (spec §2.1)
- **B4 — Honesty (Theorem 3).** Certificate existence ↔ abc. The inequality alone is not
  a shortcut unless K_ε and P_ineq are built without abc-equivalent input.
- **B5 — No PASS self-report.** Status is the checker's output (spec §6.2).
- **B6 — IUT wall.** `core3.iut-corollary-312-independently-verified` is permanently
  OPEN until a machine-replayed formal proof of Corollary 3.12 is supplied. The
  Scholze–Stix concern is the blocking reason. This is never overridden by assertion.

---

## Part II · The module program (spec §0.3)

```
M0 foundations ─► M1 arithmetic source ─► M2 key inequality ─► M3 finiteness ─► M5 comparison ─► M6 conclusion
M0 ─► M4 known results ─► M5
```

| Module | Contents | Ledger claims | Status |
|---|---|---|---|
| M0 | foundations, height theory, provenance barrier | CL-07 | `[THM]` (syntactic) |
| M1 | rad function, Faltings heights, arithmetic geometry | — | scaffold |
| M2 | key inequality c ≤ K_ε · rad(abc)^(1+ε) | CL-09, CL-10 | **`[OBL]`** |
| M3 | finiteness of exceptions | CL-11 | **`[OBL]`** |
| M4 | known results (Faltings, Szpiro equiv., Mason–Stothers) | CL-02, CL-05, CL-06 | proved (base) |
| M5 | comparison and bound verification | — | scaffold |
| M6 | abc conclusion (apply Theorem 2) | CL-03 | proved (implication) |

**Implication kernel (M0/M4/M5/M6 theorems): COMPLETE.**
**Arithmetic certificate (M1 framework, M2 inequality, M3 finiteness): NOT SUPPLIED.**
**IUT Corollary 3.12: NOT INDEPENDENTLY VERIFIED (core3.iut-corollary-312-independently-verified is OPEN).**

---

## Part III · The CORE gate graph (spec §5)

```
CORE-0 (abc def) ─► CORE-5 (conclusion)
CORE-1 (provenance) ─► CORE-2 (height framework) ─► CORE-3 (key inequality) ─► CORE-5
CORE-4 (finiteness) ─► CORE-5
```

Each gate is a proofctl contract in `domain/contracts/core-*.json`; the domain policy
`domain/policy-v2.json` lists them as `required_claims`. The sole success integration
test (spec §7.2) is:

```
CORE-1 + CORE-2 + CORE-3 + CORE-4  ⟹  CORE-5.
```

No finite collection of high-quality abc examples substitutes for this test.

---

## Part IV · proofctl integration

Realized as a **proofctl domain adapter** (`~/github/proofctl`, Go), not a fork.
- Status machine, acyclic-DAG + import policy, forbidden-runtime audit, offline replay
  (`cmd/proofverify`), claim/attestation schemas: **reused**.
- Domain-specific data lives only in `domain/policy-v2.json` + `domain/contracts/*.json`.
- `[THM]` items to be replayed in a reused formal backend
  (Lean/Metamath/Coq/Isabelle/SMT/LRAT).
- proofctl core stays domain-agnostic; kernel changes proposed upstream with their own
  tests — never abc-specific logic in `internal/`.

---

## Part V · Execution phases and gates

| Phase | Goal | Gate to advance |
|---|---|---|
| **P0 — scaffold** ✅ | spec placed; CLAUDE/PLAN/README; ledger; domain policy + 6 CORE contracts | JSON valid; ledger statuses atomic |
| **P1 — checker wiring** | wire domain into proofctl: DAG + import-policy + forbidden-leaf checks; bridge checker running on ledger/contracts | checker emits CORE-0/1 pass; CORE-2/3/4 OBL; CORE-5 blocked; adversarial tests pass |
| **P2 — implication kernel formalized** | formalize CL-03/04/07 (`[THM]`) in the chosen backend; freeze foundation_hash | backend replays all `[THM]` items; no PLACEHOLDER |
| **P3 — M1 arithmetic source** | build rad function, Faltings heights, arithmetic geometry under B1/B2; freeze `source_lock_hash` before comparison | CORE-1 GLOBALLY_VERIFIED; import barrier machine-checked |
| **P4 — M2 key inequality (the `[OBL]` frontier)** | attempt an admissible proof of c ≤ K_ε · rad(abc)^(1+ε) WITHOUT abc-equivalent input; requires independent Cor. 3.12 verification for IUT route | CORE-2, CORE-3 pass — or an explicit obstruction is recorded |
| **P5 — M3 finiteness** | prove finitely many exceptions uniformly | CORE-4 pass |
| **P6 — conclusion** | deterministic CORE-5 firing | integration test §7.2 holds |

**Current phase: P0 complete (2026-08-11).** Scaffold placed. CORE-0/1 pass; CORE-2/3/4
are honestly OBL; CORE-5 blocked. The IUT sub-obligation
`core3.iut-corollary-312-independently-verified` is OPEN with the Scholze–Stix concern
as blocking reason. This is the correct and honest state of the system.

### Phase completion status

| Phase | Status | Deliverable |
|---|---|---|
| P0 — scaffold | ✅ complete | spec, CLAUDE/PLAN/README, ledger, domain policy + 6 CORE contracts |
| P1 — checker wiring | ✅ complete | bridge checker, DAG/import/forbidden-leaf checks, adversarial tests |
| P2 — implication kernel | pending | CL-03/04/07 [THM] formalized in proof backend |
| P3 — M1 arithmetic source | pending | rad, heights, arithmetic geometry; CORE-1 locked |
| P4 — M2/M3 construction | pending (hard open problem) | key inequality + finiteness; IUT Cor. 3.12 gate |
| P5 — M5 comparison | pending | comparison proof |
| P6 — M6 conclusion | pending | CORE-5 fires when CORE-2/3/4 pass |

### Current system state (2026-08-11)

- **CORE-0/1**: PASS — implication kernel scaffold complete
- **CORE-2/3/4**: [OBL] — construction not yet supplied
- **CORE-3 sub-obligation**: `core3.iut-corollary-312-independently-verified` OPEN
  (Scholze–Stix dispute recorded as blocking reason; this is the honest state)
- **CORE-5**: correctly BLOCKED (fires only when CORE-2/3/4 pass)
- **CL-12**: [OUT] — abc is **not** proved
- **CL-13**: [OUT] — Mochizuki's IUT is **not** verified
- **Tests**: 10/10 pass (adversarial + structural)

---

## Part V-bis · Mathematical frontier analysis

### The key inequality gap (P4 / CORE-3)

The central open problem is constructing P_ineq: a proof of c ≤ K_ε · rad(abc)^(1+ε)
for all coprime a + b = c, without using abc as input. Two candidate approaches:

**Approach A: Direct algebraic geometry.** Use Faltings heights, Arakelov intersection
theory, and the geometry of arithmetic surfaces to bound the height of c relative to
the discriminant of the Faltings height of an associated elliptic curve. This approach
is what Szpiro's conjecture represents; it is unproved over integers.

**Approach B: Mochizuki's IUT.** Use the IUT framework to construct "Hodge theaters"
that deform the arithmetic of the abc triple, apply Corollary 3.12 to bound the
log-volume discrepancy, and extract the height inequality. This approach requires:
- A formalization of the Hodge theater construction (M1/M2 level)
- A formalized, independently replayed proof of Corollary 3.12
- Resolution of the Scholze–Stix objection (explicit isomorphism proof)

### The Scholze–Stix obstruction (CORE-3 sub-obligation)

The Scholze–Stix objection is specifically: in IUTT-III, Corollary 3.12 is proved by
passing between different "theaters" (copies of the arithmetic structure). Scholze and
Stix argue that objects in different theaters are identified without a proof that the
identification is valid (i.e., an explicit isomorphism), making the proof circular.

For this verification kernel, the objection maps to:
- The construction (M2) must provide an explicit isomorphism between the objects being
  identified across theaters.
- Until that isomorphism is supplied and independently replayed, the sub-obligation
  `core3.iut-corollary-312-independently-verified` remains OPEN.
- This is not a determination that IUT is wrong; it is a determination that the gate
  has not been passed.

### Discovery layer (future work)

The `discovery/` layer may be used to explore candidate approaches behind a hard
non-circularity wall (`guard.py`: constructions that read known abc triples fail to
load). Discovery is **untrusted** and never enters `proof/`/`domain/`. A numerical
approach that finds high-quality triples is a HINT about the problem, not a proof.

---

## Part VI · What success and honest failure look like

- **Success** = an admissible, non-circular proof passing CORE-2..CORE-4, at which point
  CORE-5 fires and the abc conjecture follows — this would be a proof of abc (B4), so it
  will be exactly as hard as abc and must survive full replay + human review.
- **Honest failure** = a precisely recorded obstruction at P4 (e.g., any proof attempt
  shown to violate B2, or to need an abc-equivalent input, or to rely on an unverified
  identification of objects), logged in the ledger as a closed obligation with reasons.

---

## Part VII · Regression / adversarial suite (spec §7)

`tests/` mirrors spec §7: DOC-01..07 (status grammar, acyclicity) and TEST-ABC1..10
(definitions; provenance; CORE-2/3/4 OBL; IUT gate; circular rejection; import barrier;
CORE-5 blocked; CL-03/04 honesty; CL-07 syntactic). These run before any certificate
is entertained.
