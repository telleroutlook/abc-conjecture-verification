# abc Conjecture Verification Kernel

A machine-checkable verification kernel for the abc conjecture, including a structured
framework for evaluating Mochizuki's Inter-universal Teichmüller Theory (IUT) as a
candidate proof.

**Mathematical status:** `LOGICALLY_CLOSED / NOT_PROOF_COMPLETE`

The implication is proved: any accepted certificate implies the abc conjecture.
The certificate has not been constructed. The abc conjecture is not proved here.

---

## What this repository does

This repository defines a **verification kernel** for the abc conjecture: it specifies
exactly what must be proved, in what order, under what non-circularity constraints, and
how a proposed proof would be machine-checked. The deliverable is the *auditable
boundary*, not a proof of abc.

The system:
- Defines a formal certificate `(ε, K_ε, P_height, P_ineq, P_finiteness)` and proves
  that any accepted certificate implies the abc conjecture (Theorem 2, `[THM]`)
- Proves the honesty check: certificate existence is *equivalent* to abc (Theorem 3, `[THM]`)
- Enforces a syntactic non-anticipation barrier via a directed acyclic import graph
- Provides a machine-checkable gate structure (CORE-0 through CORE-5)
- Includes a dedicated gate for Mochizuki's IUT Corollary 3.12

---

## The Mochizuki / IUT verification angle

Shinichi Mochizuki published a claimed proof of the abc conjecture via Inter-universal
Teichmüller Theory (IUT) in 2012. The key quantitative step is **Corollary 3.12** of
IUTT-III.

In 2018, Peter Scholze and Jakob Stix published a report identifying what they believe
is a gap: the proof identifies objects across different "Hodge theaters" without
providing an explicit isomorphism, which they argue makes the step circular.

**This framework's role:**

| What it does | What it does NOT do |
|---|---|
| Formalizes what Cor. 3.12 must establish (CORE-3) | Adjudicate the Scholze–Stix dispute |
| Makes the dispute machine-checkable: gate `core3.iut-corollary-312-independently-verified` fails until independently verified | Assert that IUT is wrong |
| Records both sides as open obligations | Assert that IUT is correct |
| Accepts any correct proof (IUT or not) that passes all gates | Favor any particular approach |

**Current status of the IUT gate:**

```
CORE-3 sub-obligation: core3.iut-corollary-312-independently-verified
Status: OPEN
Blocking reason: No machine-replayed formal proof of Corollary 3.12 supplied.
Scholze-Stix concern: identification of objects across Hodge theaters requires
  an explicit isomorphism proof; this has not been formalized.
This is NOT a determination that IUT is wrong.
This IS a determination that independent verification is incomplete.
```

---

## Repository structure

```
spec/SPECIFICATION.md          Mathematical specification (authoritative)
CLAUDE.md                      Engineering discipline
PLAN.md                        Execution phases and mathematical frontier analysis
domain/
  policy-v2.json               proofctl domain policy
  contracts/
    core-0-abc-definition.json
    core-1-provenance-manifest.json
    core-2-height-framework.json
    core-3-key-inequality.json     ← includes IUT Corollary 3.12 sub-obligation
    core-4-finiteness.json
    core-5-conclusion.json
proof/
  claim-ledger.json            All 13 CL items with statuses
  m0/provenance.py             Non-anticipation guard
  m1/  m2/  m3/                Construction modules (OBL — not yet built)
  m4/  m5/                     Comparison modules (scaffold)
checker/
  check_certificate.py         Bridge checker (CORE-0/1 pass; CORE-2/3/4 OBL; CORE-5 blocked)
tests/
  test_adversarial.py          10 adversarial tests
discovery/candidates/          Untrusted exploration (never imported by proof/)
```

---

## Gate structure

| Gate | Content | Current status |
|---|---|---|
| CORE-0 | abc statement, rad, certificate def, Theorems 2 & 3 | PASS |
| CORE-1 | Non-anticipation barrier, DAG acyclic, no forbidden leaves | PASS |
| CORE-2 | Height/rad framework (P_height) | [OBL] |
| CORE-3 | Key inequality c ≤ K_ε · rad(abc)^(1+ε) + IUT Cor. 3.12 gate | [OBL] |
| CORE-4 | Finiteness of exceptions (P_finiteness) | [OBL] |
| CORE-5 | abc conclusion (fires only when CORE-2/3/4 pass) | BLOCKED |

---

## Claim ledger summary

| CL | Statement | Status |
|---|---|---|
| CL-01 | rad(n) well-defined and multiplicative | [DEF] |
| CL-02 | abc ↔ Szpiro's conjecture | [BASE] |
| CL-03 | Certificate implies abc | [THM] |
| CL-04 | Certificate existence ↔ abc (honesty) | [THM] |
| CL-05 | Faltings theorem | [BASE] |
| CL-06 | Mason–Stothers theorem | [BASE] |
| CL-07 | Provenance barrier syntactically decidable | [THM] |
| CL-08 | Provenance barrier decides semantic circularity | [OUT] |
| CL-09 | Height/rad framework constructed | [OBL] |
| CL-10 | Key inequality proved (Cor. 3.12) | [OBL] |
| CL-11 | Finiteness proved uniformly | [OBL] |
| CL-12 | abc conjecture proved | [OUT] |
| CL-13 | Mochizuki's IUT proof verified | [OUT] |

---

## Running the tests

```bash
cd ~/github/abc-conjecture-verification
PYTHONPATH=. python3 -m pytest tests/ -v
```

All 10 adversarial tests must pass. They verify:
- CORE-0/1 structural obligations pass
- CORE-2/3/4 are honestly OBL
- CORE-3 IUT gate fails with the Scholze–Stix note
- Circular abc construction is rejected
- Non-anticipation barrier blocks M4/M5/M6 imports from M1/M2/M3
- CORE-5 is blocked without CORE-4
- CL-03/04 implication and honesty theorems are verified
- CL-07 syntactic provenance theorem is verified

---

## Absolute limits

**This repository never claims:**
- The abc conjecture is proved (CL-12 `[OUT]`)
- Mochizuki's IUT proof is correct or verified (CL-13 `[OUT]`)
- Any finite collection of high-quality abc examples constitutes a proof
- The syntactic non-anticipation barrier decides semantic circularity (CL-08 `[OUT]`)

---

## Mathematical background

The abc conjecture (Masser–Oesterlé, 1985): for every ε > 0, there exist only finitely
many coprime triples (a, b, c) with a + b = c such that c > rad(abc)^(1+ε), where
rad(n) is the product of distinct prime factors of n.

The conjecture is equivalent to Szpiro's conjecture for elliptic curves. It implies
Fermat's Last Theorem (for large exponents), Catalan's conjecture, Roth's theorem on
rational approximation, and many other results in Diophantine geometry.

Mochizuki's 2012 IUTT papers claim a proof via a new framework, IUT, that reconstructs
arithmetic structures from the ground up. The key quantitative step is Corollary 3.12 of
IUTT-III. The Scholze–Stix objection (2018) targets the identification of objects in
that step. The dispute remains open as of 2026.
