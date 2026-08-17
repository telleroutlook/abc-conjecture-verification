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
- [ ] Triage the three untracked discovery scripts:
  - [x] `t79_nd_type113_explore.py`: removed; it was superseded by the tracked
    `t79b_nd_type113_verify.py` and was an unresumable >30 s one-off.
  - [x] `t82_nd_type311_verify.py`: retain as mirror-case evidence and reference
    its deterministic replay, or remove it as redundant.
  - [x] `t95_all_successive_minima.py`: record the finite refutation explicitly;
    never promote the merged-multiples spectrum to a theorem.
- [x] Update the outsource status board for OB-01 through OB-17.
- [ ] Decide which untracked baseline PDFs and reference records belong in the
      next commit.
- [x] Record the current branch state (`main` ahead of `origin/main`).
- [ ] Split pending changes into reviewable commits.

## Priority 1 — baseline source verification

- [ ] Correct the CL-02 statement/ledger wording to distinguish the source-backed
      modified Szpiro/Conjecture 4′ form from the discriminant-only strong
      Szpiro form, or supply the missing exact bridge between those forms.
- [x] Obtain and source-verify Faltings 1983 Satz 7 (CL-05).
- [x] Source-verify Mason--Stothers from Oesterlé's exact published secondary
      statement (positive-characteristic derivative hypothesis included).
- [ ] Obtain the original Stothers 1981 publication if an authorized copy becomes
      available; the publisher PDF currently returns HTTP 403.
- [ ] Keep Mochizuki IUTT-III Corollary 3.12 as the object of the OPEN CORE-3
      gate; storing a source is not verification and must not close the gate.
- [x] Verify the newly added Pasten and Vaaler source anchors with local PDF
      extraction.

## Priority 2 — paper and discovery hygiene

- [x] Keep the eleven `Candidate Formula` environments clearly separated from
      theorem-tier results.
- [x] Preserve the conditional status of prime-pattern sharpness and
      unboundedness claims.
- [ ] Close or explicitly retain the OB-13B exceptional-subfamily condition
      beyond `c <= 10^12`.
- [ ] Repair the ten draft-stage underfull boxes before external submission.
- [ ] Add regression/replay wrappers for discovery scripts whose output is cited
      as finite evidence.

## Priority 3 — mathematical frontier (checker-gated, not TODO prose)

These items remain open obligations.  They are listed here only as work
directions; closing them requires checker replay, not manual status edits.

- [ ] CORE-2 / CL-09: construct and replay `P_height`.
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
