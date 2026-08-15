# CLAUDE.md — abc Conjecture Verification Kernel

## Project identity

This repository implements the **verification kernel** specified in
`spec/SPECIFICATION.md`: *A Closed Verification Kernel for the abc Conjecture —
a model-independent certificate system for Masser-Oesterlé and Mochizuki's IUT.*

**Mathematical status:** the implication kernel and verification system are the
deliverable; the arithmetic certificate (`[OBL]` items) is **not** constructed.
This is **logically closed** but **not proof-complete**. The abc conjecture is `[OUT]`
(CL-12): **not proved by this repository, and never to be self-declared proved.**
Mochizuki's IUT proof is `[OUT]` (CL-13): **not verified here, and never to be
self-declared verified.**

`spec/SPECIFICATION.md` is authoritative. This file records engineering discipline.
Where they conflict, the spec wins on mathematics; this file wins on process.

---

## Status grammar (from spec §0.2) — non-negotiable

Every ledger item has **exactly one** atomic status. Composite labels are forbidden.

| Status | Meaning | Downstream use |
|---|---|---|
| `[DEF]` | Definition fixed by the spec | may be unfolded |
| `[BASE]` | Standard theorem admitted as foundation | usable with stated hypotheses |
| `[THM]` | Theorem proved here from `[DEF]`/`[BASE]` | usable downstream |
| `[OBL]` | Construction/proof still required | **may NOT be used as a theorem** |
| `[OUT]` | Deliberately outside the certified profile | **no downstream force** |

- A conditional result is `[THM]` **with its hypotheses listed** — never a hybrid.
- Status is **derived by the checker**, never self-declared by a generator or a
  human editor. A producer-supplied PASS/status field is ignored (spec §6.2).

---

## The one-way dependency (non-anticipation) barrier — spec §0.3

Modules and their ONLY permitted dependencies:

```
M0 foundations ──► M1 arithmetic source ──► M2 key inequality ──► M3 finiteness ──► M5 comparison ──► M6 conclusion
M0 ──► M4 known results ──► M5
```

- **`M1`, `M2`, `M3` MUST NOT import `M4`, `M5`, `M6`.** This is the formal
  non-anticipation barrier: the construction of the height framework, the key
  inequality, and the finiteness argument may not see known abc triples, the Szpiro
  comparison, or the conclusion.
- The construction graph is **built and content-hashed before** the comparison graph
  is admitted.
- Machine-checkable (syntactic import DAG); it does **not** decide semantic
  circularity (spec §3.4, CL-08 = `[OUT]`).

## Forbidden construction leaves (spec §3.3) — auto-reject

The construction graph (`M1`–`M3`) must NEVER use:
- known abc triples or high-quality examples to fit or derive `K_ε`;
- the abc conjecture itself as a hypothesis;
- Szpiro's conjecture assumed without proof;
- the finiteness of S-integer solutions assumed without derivation;
- GRH or other unproved hypotheses not declared as conditional hypotheses;
- IUT-specific: "identification of objects" across Hodge theaters without an explicit
  isomorphism proof (the Scholze–Stix objection);
- parameters fit by minimizing error against known abc examples;
- a bound proved only for a fixed finite prime set S promoted as universal.

---

## The Mochizuki/IUT discipline — critical

The CORE-3 gate includes a sub-obligation
`core3.iut-corollary-312-independently-verified` that is **always OPEN** until a
machine-replayed formal proof of Corollary 3.12 (IUTT-III) is supplied.

**Rules for this obligation:**
- Never mark it as passed without a machine-replayed proof term.
- Never write "Mochizuki's proof is correct" or "IUT is verified" in any file.
- The Scholze–Stix dispute is recorded as the blocking reason; this is not a
  determination that IUT is wrong — it is a determination that independent
  verification is incomplete.
- A future formalization that passes this gate is welcome via any proof assistant.

---

## proofctl integration (this repo is a proofctl DOMAIN)

This system is realized as a **proofctl domain adapter**, not a fork. proofctl lives
at `~/github/proofctl` (Go, `github.com/telleroutlook/proofctl`); its binary is not on
PATH — build with `go build ./cmd/proofctl` and `./cmd/proofverify` there.

- **Reuse, do not re-implement.** The status state machine, acyclic-DAG check, import
  policy, forbidden-runtime audit, replay verifier (`cmd/proofverify`, offline), and
  claim/attestation schemas already exist in proofctl. Map onto them:
  | spec concept | proofctl mechanism |
  |---|---|
  | status grammar | `derive/` state machine + `schemas/claim.schema.json` |
  | M0–M6 import barrier | `internal/dag` + module import policy JSON |
  | forbidden construction leaves | `policy.ForbiddenRuntimes` / forbidden-input audit |
  | CORE-0..CORE-5 gates | `required_claims` in `domain/policy-v2.json` |
  | `[OBL]` items | OPEN obligations in the claim ledger |
  | replay, no trusted PASS | `cmd/proofverify` (no network, no subprocess) |
- **Domain files live under `domain/`**: a `policy-v2.json` and
  `domain/contracts/*.json` (one per CORE gate / claim).
- **proofctl core stays domain-agnostic.** Per proofctl's own CLAUDE.md: `internal/kernel/`
  imports only stdlib; domain specifics live in policy JSON, never in Go constants.

---

## The certificate (spec §10) — the single logical boundary

```
ε > 0; K_ε > 0; P_height; P_ineq; P_finiteness;
all built under the provenance contract
  ⟹  abc conjecture (for this ε).
```

The implication is `[THM]` (proved). The construction premises are `[OBL]` (not
supplied). The inequality in P_ineq is a **universal statement over all coprime triples**
— NOT agreement on known examples, NOT a bound for a fixed prime set S (spec §2.1).

## Honesty checks you must never delete (spec §2.3, Theorem 3)

Existence of the certificate is *equivalent* to abc. The inequality alone is not an
easier reformulation — it becomes a strategy only when K_ε and P_ineq are constructed
**without** using abc triples, fitting samples, or assuming an abc-equivalent assertion.
Any construction that reads known triples, fits K_ε, or assumes Szpiro is `CIRCULAR`
and fails CORE-1.

The IUT sub-obligation `core3.iut-corollary-312-independently-verified` is **permanently
OPEN** until a machine-replayed proof appears. The Scholze–Stix concern is its blocking
reason. This is the honest state.

---

## Stop conditions (spec §8) — semantic failures, not style

Stop, narrow the claim, or open a new proved profile if any occur:
1. construction imports known abc triples before the comparison step;
2. K_ε is derived by minimizing error against known high-quality examples;
3. Szpiro's conjecture or an abc-equivalent assertion is assumed without proof;
4. the key inequality is proved only for a fixed finite prime set S, promoted universal;
5. IUT identification of objects used without a formalized isomorphism proof;
6. finiteness of exceptions assumed rather than derived;
7. GRH or another unproved hypothesis used without declaring it as a hypothesis;
8. a candidate-generated status is trusted instead of recomputed;
9. an obligation is renamed an axiom and used to claim completion;
10. "Mochizuki's IUT is correct" or "abc is proved" is asserted without gate passage.

---

## Engineering conventions (inherited, hard-won)

- **Long computations (>30s):** observable (`flush=True` progress lines), pausable
  (catch KeyboardInterrupt, checkpoint), resumable (`--resume`). Use
  `~/.local/bin/run_and_wait.sh -t <sec> -- <cmd>` for blocking long runs.
- **Certified bounds:** interval arithmetic with outward rounding
  (`python-flint`/Arb); `mpmath`/floats are discovery-tier only.
- **discovery/ is untrusted** (may read known abc triples for exploration); it is NEVER
  imported by the construction graph or the checker, and its outputs are never promoted
  to `proof/`.
- **Verify load-bearing claims by script, not memory** (identities, bounds, multiplicative
  facts).
- **Commit messages in English.** `git status` before commit. Never stage `discovery/`
  into `proof/`. Certificates go in only after independent replay.
- **No PASS self-report anywhere.** Status is the checker's output.

## What this repository does NOT do

- Does not claim to prove abc (CL-12 `[OUT]`); never write "abc proved".
- Does not verify Mochizuki's IUT (CL-13 `[OUT]`); never write "IUT verified" or
  "Mochizuki's proof is correct".
- Does not treat any finite collection of high-quality abc examples as a proof.
- Does not upgrade the syntactic provenance barrier to a semantic non-circularity oracle
  (CL-07 is syntactic; CL-08 `[OUT]`).
- Does not adjudicate the Scholze–Stix dispute; records it as a blocking open obligation.

---

## Baseline literature discipline (load-bearing — verify from source, never from memory)

Every theorem used as a premise must be checked against its published source before it
supports any claim here. Key foundations that must be source-verified before use:

- **Faltings 1983** (Mordell conjecture / Faltings heights): cited as `[BASE]` in M4/CL-05
- **Mason–Stothers** (polynomial abc): cited as `[BASE]` in M4/CL-06
- **Szpiro equivalence** (abc ↔ Szpiro's conjecture): cited as `[BASE]` in M4/CL-02
- **Mochizuki IUTT-I..IV** (Corollary 3.12 route): cited as the object of the OPEN gate

Store verified source PDFs or tarballs under `baseline/`. For any new base theorem added
to the ledger, run `grep -n 'Theorem X.Y' baseline/<file>` to confirm theorem number and
exact statement before citing it. "I remember what it says" is not a pass.

---

## Outsource-prompt pre-send checklist (mandatory)

Before sending any `outsource/` problem for external review, self-check these failure
modes. Verify load-bearing claims with a quick script, not from memory.

Run `outsource/PROMPT_LINT.md` on every new or edited prompt before it ships.  When a
referee surfaces a new defect class, add it to PROMPT_LINT.md and re-scan every active
prompt AND every `proof/*/` relevant file — defects are never assumed independent.

1. **No circular target.** The goal must not assume abc, Szpiro, or an abc-equivalent
   assertion, directly or through a fitted parameter K_ε derived from known abc triples.
   Grep the prompt for "known triples", "rad(abc)", "best known example", "fit K".

2. **No dropped term.** Any assembly/reduction identity you state must be verified
   end-to-end. Watch: universal quantifier scope (the inequality must cover ALL coprime
   a+b=c, not just a fixed prime set S), and boundary terms in estimates.

3. **Cite only what is proved.** Label each black box with its proof source and theorem
   number (verified). Confirm it actually covers the object used. PLAN.md statuses can
   be stale — trust only verified `checker/` output.

4. **No false dichotomy.** If offering "prove X / prove obstruction", also allow an
   honest "inconclusive + precise partial localization" outcome.

5. **Self-contained.** Every symbol defined in-file. No "see other file". Inline full
   formulas (rad, heights, K_ε, prime sets S). Any numerical anchor labeled
   "sanity only, not an input" and verified by script.

### Minimum outsource file structure

```
# Problem OB-NN — Short title

**Type:** [algebraic geometry / analytic number theory / combinatorics / etc.]
**Non-circularity:** [explicit statement that abc, IUT Corollary 3.12, abc triples,
  fitted K_ε, and Szpiro are not assumed — or why this problem does not touch them]

## All definitions (self-contained — everything is here)
[Every symbol defined, every formula written out in full]

## The theorem / claim to be verified
[Complete statement]

## Proof skeleton to be closed
### Step 1 — [name]
[Draft with "What to close for Step 1:" subsection]
### Step 2 — ...

## Acceptance criteria
[Numbered list; allow CONFIRMED / PARTIAL / REFUTED / inconclusive outcomes]

## Numerical anchor (sanity only, not an input to the proof)
[One concrete computable example the reviewer can sanity-check]
```

---

## Paper pre-submission checklist (mandatory)

Before sending any `papers/*/` file for external review, run all checks in
`papers/PAPER_LINT.md` (items P1–P17 at minimum) against the target `.tex` file.
Record the one-line output of each automatable check next to the item.
Fix every failure before submission. "Looks fine by eye" is not a pass.

```bash
TEX=papers/<id>/<file>.tex  # set this first
# Then run each grep/script from PAPER_LINT.md in order P1 → P17.
```
