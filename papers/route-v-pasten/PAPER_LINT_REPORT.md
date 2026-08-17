# Paper lint report — route-v-pasten

Date: 2026-08-17 (refreshed after the `thm:f3` reference repair)  
Target: `route-v-pasten.tex`

This report records the checks run after the repairs described in `PLAN.md`.
“0 findings” means that the displayed checker/grep produced no output lines.

## Part I — compilation and structure

- **P1 hardcoded internal references:** 0 findings.  The external-source
  statement in the bibliography is outside the internal-reference rule.
- **P2 unused labels:** 0 findings among 56 labels.  `thm:f3` is now referenced
  in its following sentence.
- **P3 uncited bibliography entries:** 0 findings among 2 entries.
- **P4 LaTeX compilation:** three `pdflatex -interaction=nonstopmode
  route-v-pasten.tex` passes exited `0, 0, 0`.  The final pass had 0 undefined
  reference/citation/error warnings, 0 overfull boxes, and 0 underfull boxes.
  Long Candidate Formula statements, the formal-verification section, and the
  bibliography use ragged-right typography for unbreakable identifiers and
  source paths.
- **P5 short title:** the optional short-title field is absent, so the full
  scoped title is used; no semantic mismatch.

## Part II — mathematical integrity

- **P6 later use:** all 50 theorem-like/candidate labels are referenced.  Main
  results and finite-verification candidates that are not inputs to a later
  proof are retained explicitly as final results or context, as permitted by
  the checklist's background-context option.
- **P7 definition consistency:** \(F(a,b)\) denotes Pasten's original lattice;
  \(F_{\mathrm{val}}(a,b)\) and \(\mathrm{nd}_{\mathrm{val}}\) are introduced
  before all non-squarefree exact formulas.  The \((1,8,9)\) example separates
  the two invariants.
- **P8 restated prior results:** no theorem environment restates an external
  theorem without attribution.
- **P9 asymptotic error order:** the target `O(T^{-...})`/`o(T^{-...})`
  patterns have 0 occurrences.
- **P10 informal qualifiers in formal statements:** target grep has 0 findings.
- **P11 remark/footnote formulas:** numerical anchors were replayed by script:
  `python3 discovery/m2_directions/t96_edge_case_both_small_in_Pb.py` exited 0
  and reported `OB-15 violations: 0`; the two listed edge cases match the paper.
- **P12 no-go theorem:** not applicable; the paper contains no no-go theorem.
- **P13 equivalence as impossibility:** Pasten's SDC/abc equivalence is used
  only to locate difficulty and is explicitly not promoted to a barrier.
- **P14 abstract/introduction scope:** repaired.  Sharp constants and blanket
  \(\omega\ge6\) unboundedness are now conditional prime-pattern claims.
- **P15 motivational analogy:** no external impossibility-framework analogy is
  used.
- **P16 imported-premise evidence:** Pasten arXiv v3 and Vaaler 1979 primary
  PDFs are stored under `baseline/`; exact statements and instantiations are in
  `baseline/REFERENCE_BASELINE.md`.
- **P17 method-class invariance:** not applicable; no method-class margin is
  defined.
- **P18 constructive qualifier:** OB-13C now claims a finite deterministic
  enumeration with an explicit unconditional witness bound, not polynomial time.

## Part III — theorem/citation rigor

- **P19 parity cancellation:** no target parity/error-cancellation pattern.
- **P20 unsupported strong assertions:** target grep has 0 findings.
- **P21 “same argument” claims:** remaining occurrences are explicit label
  swaps or branch substitutions in the candidate formulas; no in-paper
  counterexample to the claimed symmetry was found.  The E\(_n\) symmetry cases
  are now spelled out.
- **P22 external theorem instantiation:** Vaaler Theorem 2 is instantiated with
  a \(\mathbb Z\)-basis of \(F(a,b)\), ambient coordinate forms, rank
  \(\omega-1\), and common bound \(\det(F)^{1/(\omega-1)}\).
- **P23 operator extensions:** not applicable.
- **P24 optional environment titles:** no optional title duplicates the
  automatic counter label.
- **P25 literature formulas:** source anchors replayed with `pdftotext`:
  Pasten `Conjecture 1.2`, `Lemma 2.4`, and `Corollary 4.6`; Vaaler `THEOREM 2`
  and its geometric corollary.
- **P26 reference operator symbol class:** not applicable.
- **P27 Tauberian biconditional:** not applicable.
- **P28 single-letter conflicts:** the quality abbreviation \(q\) was removed;
  \(F\) versus \(F_{\mathrm{val}}\), and radical \(R\) versus enumeration
  radii \(R_j\), are explicitly distinguished.
- **P29 PDF bookmark text:** the sole bookmark formula is \(\omega=2\), matching
  the bookmark text `omega=2`.
- **P30 free variables:** theorem/candidate domains were audited.  OB-13B now
  defines \(\pi_1<\cdots<\pi_{\omega^*}\); OB-13C excludes the rank-zero
  \(\omega^*=1\) boundary; the undefined `nd111` shorthand was removed.
- **P31 same-argument conclusions:** branch conclusions are stated for each
  target branch; candidate status prevents them from being used as unconditional
  theorem implications.
- **P32 canonical realization:** \(F_{\mathrm{val}}\), its inherited norm, and
  its Wronskian condition are named immediately after construction.
- **P33 statement-proof domain:** the major domain leak is fixed: exact
  non-squarefree formulas apply to \(F_{\mathrm{val}}\), while OB-13B gives only
  an upper bound for the original lattice.
- **P34 spectral definition domain:** not applicable.
- **P35 parameterized class superscripts:** not applicable.
- **P36 existence versus construction:** Vaaler is used only for existence, not
  for an unstated construction.
- **P37 degenerate parameters:** the rank-zero \(\omega^*=1\) case is explicit;
  \(\omega\ge2\) is retained for the lattice theorem.
- **P38 inner product:** the weighted inner product is displayed and named
  before LLL is invoked.

## Part IV — scope and methodology

- **P39 open-problem variables:** there is no standalone open-problem section;
  conditional prime-pattern assumptions state their variables inline.
- **P40 uniform versus pointwise indices:** the F11 criterion is stated for an
  explicit infinite sequence with a uniform comparability condition.
- **P41 author count in possessive citations:** target grep has 0 findings.
- **P42 referenced files:** all explicit repository paths exist.  Shorthand
  script tokens (for example `t47`) resolve to the unique corresponding
  `discovery/m2_directions/t47*.py` file; the mirror-case token
  `T82-type311` resolves specifically to
  `discovery/m2_directions/t82_nd_type311_verify.py`.
- **P43 heat-semigroup trace class:** not applicable.
- **P44 principal-symbol cutoff:** not applicable.
- **P45 forward references in definitions:** 0 findings.
- **P46 classical versus log-polyhomogeneous classes:** not applicable.
- **P47 solved open problems:** conditional prime-pattern infinitudes are not
  claimed to be solved.
- **P48 boundary analytic extension:** not applicable.
- **P49 rational versus polynomial analytic type:** not applicable.
- **P50 counting-function validity range:** the norm-spectrum corollary was
  corrected: the non-degenerate spectrum is a union of two rays and has no
  Frobenius number.
- **P51 unquantified definition variables:** no formal definition block introduces
  an unquantified bound variable.

## Part V — typesetting

- **P52 tolerance/emergency stretch:** present (`\tolerance=1500`,
  `\emergencystretch=2em`).
- **P53 bibliography wrapping:** `thebibliography` is wrapped in `{\sloppy ...}`.
- **P54 long inline operators:** the weighted inner product was moved to a
  display; no remaining target long operator construction was found.

## Proactive audit S1–S5

- **S1 hypothesis shadow:** the valuation-lattice domain, rank-zero boundary,
  conditional prime-pattern assumptions, and finite-verification candidate
  status are explicit.  No proof step silently changes from \(F\) to
  \(F_{\mathrm{val}}\).
- **S2 domain coverage:** Pasten's SDC exceptional family is now stated exactly;
  Vaaler's rank/domain hypotheses are instantiated; original versus valuation
  minima are separated.
- **S3 citation instantiation:** Pasten supplies definitions and the equivalence
  scope; Vaaler Theorem 2 supplies the lattice existence bound with explicit
  substitutions recorded above and in `baseline/REFERENCE_BASELINE.md`.
- **S4 parameter boundaries:** \(\omega=1\), \(\omega=2\), \(q=3\) versus
  \(q\ge5\), and squarefree versus non-squarefree boundaries are handled or
  explicitly excluded.
- **S5 normalization:** Pasten's \(\psi(\xi_p)\), Wronskian, norm, and SDC
  exception are checked against the arXiv v3 source; Vaaler's unit cube and
  scaling to \([-1,1]^\omega\) are recorded.

## Additional verification

- `lake build` in `lean/`: exit `0`, `Build completed successfully (2005 jobs)`.
  Warnings are unused-variable/deprecation lint; no build error.
- `python3 discovery/m2_directions/t30_rho_distribution.py`: exit `0`.
- `python3 discovery/m2_directions/t96_edge_case_both_small_in_Pb.py`: exit `0`,
  `OB-15 violations: 0`.
- `python3 discovery/m2_directions/t82_nd_type311_verify.py`: exit `0`;
  843 type-$(3,1,1)$ triples, `843 OK, 0 FAIL`.
- `python3 discovery/m2_directions/t95_all_successive_minima.py`: exit `0`;
  this is a deterministic replay of a **refutation**.  The all-successive-minima
  merged-multiples candidate fails at $(2,13,15)$ and $(3,7,10)$.

## Remaining honest limitations

1. Eleven higher-dimensional non-squarefree formulas are `Candidate Formula`
   environments, not theorems; their all-nonzero cases have only finite
   verification.
2. Extremal constants and blanket \(\omega\ge6\) unboundedness depend on
   infinite prime-pattern families and remain conditional.
3. OB-13B is conditional outside the checked \(c\le10^{12}\) edge-case search
   for the explicitly listed exceptional subfamilies.
