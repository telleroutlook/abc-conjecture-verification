# baseline/ — source-verified reference literature

This directory stores verified copies of foundational results that appear as `[BASE]`
items in the claim ledger. Every theorem cited as a premise must be traced to a source
file here, by theorem number, before it can support any downstream claim.

## Discipline

**Rule:** "I remember what the theorem says" is not a pass. Before using a base theorem
as a premise, run:
```bash
grep -n 'Theorem <N>' baseline/<file>
```
and confirm the exact statement and hypotheses match what you intend to cite.

A DOI or arXiv number is archival publication, not peer review. The theorem number
must be verified from the actual source, not from a secondary summary.

## Contents

| Source | CL item | Key result | File |
|---|---|---|---|
| Faltings 1983 | CL-05 | Mordell conjecture / finiteness of rational points | `faltings-1983-abelian-varieties.pdf` |
| Mason–Stothers | CL-06 | Polynomial abc theorem | `oesterle-1988-nouvelles-approches-fermat.pdf` (exact published secondary source; original Stothers PDF currently paywalled) |
| Oesterlé 1988 | CL-02 | abc ↔ modified Szpiro/Conjecture 4′ precision record | `oesterle-1988-nouvelles-approches-fermat.pdf` |
| Mochizuki IUTT-III | CORE-3 | Corollary 3.12 (IUT route) | (add when verified) |
| Pasten 2021 (arXiv v3) | Route V | Derivative lattice, SDC, abc equivalence | `pasten-2021-arithmetic-derivatives.pdf` |
| Vaaler 1979 | Route V / determinant bound | Central hyperplane sections and lattice linear forms | `vaaler-1979-geometric-inequality.pdf` |

## Adding a new source

1. Obtain a PDF or tarball of the source.
2. Verify the theorem number and statement directly from the source.
3. Add an entry to the table above with the CL item it supports.
4. Store the file here: `<author>-<year>-<short-title>.<ext>`.
5. Record the exact theorem statement (copied from source) in `REFERENCE_BASELINE.md`.

## REFERENCE_BASELINE.md

Create a `REFERENCE_BASELINE.md` here to record the exact definitions and theorem
statements used from each source — not paraphrases. This is the authoritative record
for what "Faltings Theorem" or "Mason–Stothers" means in this repository.
