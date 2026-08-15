# outsource/ — self-contained proof-verification requests

Each file here is a standalone mathematical problem extracted from this abc Conjecture
Verification repository. A reviewer needs **nothing else from this repo** to evaluate
the problem.

## Format contract

- **Self-contained:** all definitions, claims, and proof strategies are in the file.
- **Falsifiable:** if a step is wrong, the reviewer should return an explicit
  counterexample or gap description, not just "cannot prove."
- **Non-circular:** no problem assumes the abc conjecture, Szpiro's conjecture, IUT
  Corollary 3.12, or uses known abc triples as analytic input. Numerical anchors for
  sanity checks are allowed in quantitative steps, labeled as such.

## Lint gate

Run `PROMPT_LINT.md` before every send. When a new defect class is identified in a
returned review, add it to PROMPT_LINT.md and re-scan ALL active prompts.

## Status board

| # | File | Content | Status |
|---|---|---|---|
| (no problems yet) | — | — | — |

## File naming

`OB-NN-<short-topic>.md` — sequential number, short camel-case topic slug.
