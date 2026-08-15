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
| OB-01 | [OB-01-algebraic-geometry-height-bound.md](OB-01-algebraic-geometry-height-bound.md) | Prove or give explicit obstruction for h_F(E_{a,b,c}) ≤ C_ε·(1+ε)·log rad(abc) via Arakelov/Faltings — without Szpiro or IUT | READY — A1-A7 pass |
| OB-02 | [OB-02-iut-corollary-312-isomorphism.md](OB-02-iut-corollary-312-isomorphism.md) | Supply explicit isomorphism φ: Θ₁ → Θ₂ (volume-preserving) resolving Scholze–Stix; machine-replayable proof of IUT Cor. 3.12 | READY — A1-A7 pass |
| OB-03 | [OB-03-p-height-framework.md](OB-03-p-height-framework.md) | Construct formally-verified rad/height/discriminant/conductor framework (CORE-2 / CL-09 prerequisite) — no abc-equivalent input | READY — A1-A7 pass |

## File naming

`OB-NN-<short-topic>.md` — sequential number, short camel-case topic slug.
