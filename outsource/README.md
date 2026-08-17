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

Statuses below describe the *outsource artifact*, not the atomic status of a
claim in `proof/claim-ledger.json`.  A review or prompt note never promotes an
obligation; only the applicable checker/proof assistant can do that.

| # | File | Content | Current artifact status |
|---|---|---|---|
| OB-01 | [OB-01-algebraic-geometry-height-bound.md](OB-01-algebraic-geometry-height-bound.md) | Frey-curve height bound via Arakelov/Faltings | External review: PARTIAL; Steps 1--3 strengthened, main claim remains open |
| OB-02 | [OB-02-iut-corollary-312-isomorphism.md](OB-02-iut-corollary-312-isomorphism.md) | Explicit isomorphism for the IUT Θ-link | READY; no independent review yet; CORE-3 IUT gate remains OPEN |
| OB-02v2 | [OB-02v2-iut-corollary-312-pilot-compatibility.md](OB-02v2-iut-corollary-312-pilot-compatibility.md) | Pilot-object log-volume compatibility | External review: INCONCLUSIVE + LOCALIZATION |
| OB-03 | [OB-03-p-height-framework.md](OB-03-p-height-framework.md) | rad/height/discriminant/conductor framework | Ordinary mathematics corrected and reviewed; formalization PARTIAL. CORE-2 remains `[OBL]` |
| OB-04 | [OB-04-lean4-formalization-height-framework.md](OB-04-lean4-formalization-height-framework.md) | Lean formalization of OB-03 | PARTIAL-FORMALIZATION; OB-04-A complete, Silverman premises explicitly admitted |
| OB-05 | [OB-05-iut-object-definitions-verification.md](OB-05-iut-object-definitions-verification.md) | Verbatim audit of IUT object definitions | External review: PARTIAL (D1--D5, D7 corrected; D6 localized) |
| OB-06 | [OB-06-iut-bj-morphism-construction.md](OB-06-iut-bj-morphism-construction.md) | IUT `B_j` comparison morphism | External review: INCONCLUSIVE + LOCALIZATION; IUT gate remains OPEN |
| OB-07 | [OB-07-baker-methods-quality-bound.md](OB-07-baker-methods-quality-bound.md) | Baker/S-unit route to a fixed-power bound | External review: INCONCLUSIVE + LOCALIZATION; `R^{1/3}` barrier recorded |
| OB-08 | [OB-08-arithmetic-derivative-additive-inequality.md](OB-08-arithmetic-derivative-additive-inequality.md) | Arithmetic-derivative inequality survey | OPEN survey/boundary problem; original ADAI falsified, log-corrected form open |
| OB-09 | [OB-09-pasten-squarefree-det-bound.md](OB-09-pasten-squarefree-det-bound.md) | Pasten lattice determinant bound | External review: CONFIRMED for the stated squarefree theorem |
| OB-10 | [OB-10-squarefree-nondeg-bound.md](OB-10-squarefree-nondeg-bound.md) | Squarefree non-degenerate bound | External review: CONFIRMED |
| OB-11 | [OB-11-pasten-nondeg-a-ge-2.md](OB-11-pasten-nondeg-a-ge-2.md) | Non-degeneracy for `a >= 2` | External review: CONFIRMED after proof correction |
| OB-12 | [OB-12-sharp-bounds-bounded-types.md](OB-12-sharp-bounds-bounded-types.md) | Sharp bounds for bounded Pasten types | External review: Claims A/B CONFIRMED; Claim C refuted as stated and revised |
| OB-13 | [OB-13-nondeg-norm-nonsquarefree.md](OB-13-nondeg-norm-nonsquarefree.md) | Non-squarefree minimum norm | v2 review supersedes v1: minimal OB-13B REFUTED; first inequality and algorithmic OB-13C retained |
| OB-14 | [OB-14-supremum-rho-omega5-types.md](OB-14-supremum-rho-omega5-types.md) | Suprema for `omega=5` types | External review: PARTIAL-CONFIRMED; unconditional upper bound yes, sharpness conditional |
| OB-15 | [OB-15-ob13b-high-quality-triples.md](OB-15-ob13b-high-quality-triples.md) | High-quality `R < c` triples | External review: PARTIAL; subsequent general cases tracked by OB-16/OB-17 |
| OB-16 | [OB-16-gap2-no-within-group.md](OB-16-gap2-no-within-group.md) | Equal-valuation-group gap | Internal closure draft for `omega*=3,4` and general cases; independent replay/review still required |
| OB-17 | [OB-17-ob15-general-proof.md](OB-17-ob15-general-proof.md) | General `R < c` proof | Internal closure draft for `omega*=4` and general `omega*>=3`; independent replay/review still required |

## File naming

`OB-NN-<short-topic>.md` — sequential number, short camel-case topic slug.
