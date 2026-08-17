# TODO — current execution board

This file tracks engineering and documentation work only.  It never changes the
atomic proof status of a ledger item.  Mathematical promotion remains the
exclusive responsibility of the offline checkers and the proof assistant.

## Priority 0 — repository hygiene and replayable evidence

- [x] Re-run the Python regression suite and record the result.
- [x] Re-run `proofctl check --all` and preserve the honest rejected state of
      CORE-2/3/4.
- [x] Re-run the Lean build.
- [x] Re-run the automatable paper checks P1--P4.
- [x] Create this execution board.
- [x] Fix paper lint P2: reference `thm:f3` or mark it explicitly as context.
- [x] Rebuild `papers/route-v-pasten/route-v-pasten.pdf` after the final TeX edit.
- [x] Refresh `PAPER_LINT_REPORT.md` so it describes the current TeX, not an
      earlier revision.
- [x] Triage the three untracked discovery scripts:
  - [x] `t79_nd_type113_explore.py`: removed; it was superseded by the tracked
    `t79b_nd_type113_verify.py` and was an unresumable >30 s one-off.
  - [x] `t82_nd_type311_verify.py`: retain as mirror-case evidence and reference
    its deterministic replay, or remove it as redundant.
  - [x] `t95_all_successive_minima.py`: record the finite refutation explicitly;
    never promote the merged-multiples spectrum to a theorem.
- [x] Update the outsource status board for OB-01 through OB-17.
- [x] Decide which untracked baseline PDFs and reference records belong in the
      next commit.
- [x] Record the current branch state (`main` ahead of `origin/main`).
- [x] Split pending changes into reviewable commits.

## Priority 1 — baseline source verification

- [x] Correct the CL-02 statement/ledger wording to distinguish the source-backed
      modified Szpiro/Conjecture 4′ form from the discriminant-only strong
      Szpiro form, or supply the missing exact bridge between those forms.
- [x] Obtain and source-verify Faltings 1983 Satz 7 (CL-05).
- [x] Source-verify Mason--Stothers from Oesterlé's exact published secondary
      statement (positive-characteristic derivative hypothesis included).
- [ ] Obtain the original Stothers 1981 publication if an authorized copy becomes
      available; the publisher PDF currently returns HTTP 403.
- [x] Source-verify Silverman AEC 2nd ed. Lemma VIII.11.3(a),(b) from the
       local primary-source PDF; correct the page anchor to pp. 257--258.
- [ ] Obtain an authorized primary copy of Silverman ATEC 1994 Theorem IV.10.4.
      Until then `frey_conductor_formula` remains an explicitly admitted premise
      and cannot support CORE-2 acceptance.
- [x] Replace the vacuous existential conductor axiom by an opaque fixed Frey
      conductor plus a nontrivial formula premise; derive the log bound in Lean.
- [x] Replace the vacuous existential minimal-discriminant axiom by an opaque
      fixed Frey minimal discriminant; define and bound \(h_\Delta\) in Lean.
- [x] Anchor Mochizuki IUTT-III Corollary 3.12 to the May 2020 RIMS source
      PDF without closing or weakening the OPEN CORE-3 gate.
- [x] Source-verify Murty--Pasten Theorems 5.1 and 5.4 for the true-Faltings
      height period formula and archimedean lower bound; register the PDF in
      the non-accepting CORE-2 evidence manifest.
- [x] Verify the newly added Pasten and Vaaler source anchors with local PDF
      extraction.

## Priority 2 — paper and discovery hygiene

- [x] Keep the eleven `Candidate Formula` environments clearly separated from
      theorem-tier results.
- [x] Preserve the conditional status of prime-pattern sharpness and
      unboundedness claims.
- [x] Explicitly retain the OB-13B exceptional-subfamily condition
      beyond `c <= 10^12`.
      The remaining Wieferich-type prime-power analysis is a mathematical
      auxiliary obligation, not a lint defect.
- [x] Repair the ten draft-stage underfull boxes before external submission.
- [x] Add regression/replay wrappers for discovery scripts whose output is cited
      as finite evidence.

## Priority 3 — mathematical frontier (checker-gated, not TODO prose)

These items remain open obligations.  They are listed here only as work
directions; closing them requires checker replay, not manual status edits.

- [ ] CORE-2 / CL-09: construct and replay `P_height`.
- [x] Define the Lean target interface `FreyFaltingsHeightTarget` and prove
      only its conditional bounded-quality implication; supply no instance.
- [x] OB-04-A: close the missing Lean P1 artifact for integer absolute-value
      invariance of the radical (P2 and P3 are already formalized).
- [x] OB-04-A: also state P3 over the integers, using coprime absolute values,
      rather than only the natural-number specialization.
- [x] OB-04-B/C: keep the named Silverman imports explicit in a machine-audited
      axiom manifest; do not describe them as fully formalized theorems.
- [ ] OB-04: replace the two admitted Silverman axioms by source-verified
      formal imports, or keep OB-04 at PARTIAL-FORMALIZATION status.
- [x] Register a checker-validated, non-accepting CORE-2 partial-evidence
      manifest with content hashes for the OB-04 artifacts.
- [x] Add adversarial replay tests proving that CORE-2 partial evidence cannot
      tamper its way into acceptance, alter artifact digests, or promote an
      OB-04 component status.
- [x] Add checker-pin regression tests covering both domain and `.proofctl`
      contract/graph mirrors, preventing a future checker edit from silently
      desynchronizing proofctl.
- [ ] CORE-3 / CL-10: prove the universal key inequality without forbidden
      inputs and supply an explicit `K_epsilon`.
- [ ] CORE-3 IUT sub-obligation: provide a machine-replayed proof of
      Corollary 3.12 or an equivalent result, including the required explicit
      isomorphism.
- [ ] CORE-4 / CL-11: prove uniform finiteness of the exception set.
- [ ] Supply release metadata (`epsilon_bound`, `constant_k_epsilon`,
      `provenance_dag_hash`, and related fields) only after the corresponding
      proof artifacts exist.

## Permanent non-goals

- Do not declare abc proved (CL-12 is `[OUT]`).
- Do not declare Mochizuki's IUT proof verified (CL-13 is `[OUT]`).
- Do not use known abc triples, fitted `K_epsilon`, or Szpiro as construction
  inputs.
- Do not turn finite discovery evidence into a universal theorem.
