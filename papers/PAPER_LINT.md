# PAPER_LINT.md — pre-submission self-audit checklist for rigorous mathematical papers

This file is designed to be copied into any project producing a formal mathematics paper.
Project-specific adaptations are confined to `Precedent:` lines and "Domain note:" callouts;
the rules themselves are general.

---

## Architecture: two complementary layers

**Reactive layer (Parts I–IV, items P1–P38).** Specific, automatable or semi-automatable
checks — each item was added after a known defect class was observed.  These checks are
fast, targeted, and will always have gaps: a new defect class will not appear here until
it has already been caught once.

**Proactive layer (Part V, items S1–S5).** Structural completeness questions asked
*once per theorem*, derived from the fundamental invariants of rigorous mathematical
writing.  If you answer S1–S5 honestly for every result, the defects caught by P1–P38
become impossible — not because we enumerated them, but because their underlying cause
was eliminated.

**Recommended workflow:**

1. Run Part I gates (P1–P4): fix compilation errors before reading further.
2. For each new or substantially revised theorem: answer S1–S5 (Part V) in writing.
3. Run Parts II–IV grep sweeps to catch anything S1–S5 missed.
4. Record one-line output for each automatable item before submission.

"Looks fine by eye" is not a pass for any item in this file.

---

## PART I — Compilation and TeX structure (automatable)

These five checks must pass before any manual review.

---

### P1 — No hardcoded cross-references

Every **internally defined** `Theorem A`, `Lemma 2.4`, `Corollary D`, etc. in the body
must be a `\ref{...}`, not a hand-typed letter or number.  Hardcoded refs become stale
when theorem order changes.

**Known false-positive pattern:** references to theorems in *external* sources
(e.g. `Lemma~7.3` from a cited arXiv paper, `Theorem~X.23` from a textbook chapter)
are not `\ref{}` candidates — they should instead be verified via P25 (literature
formula descriptions).  Filter them out by excluding lines that contain `\cite` within
the same sentence.

```bash
# Step 1: find candidates (adapt letter/number patterns to your naming scheme)
grep -n 'Theorem~[A-Z]\|Corollary~[A-Z]\|Lemma~[0-9]\|Proposition~[0-9]' "$TEX" \
  | grep -v '\\ref{'
# Step 2: for each hit, check whether the same line also contains \cite{...}
# Lines with \cite are external theorem references → feed to P25, not P1
grep -n 'Theorem~[A-Z]\|Corollary~[A-Z]\|Lemma~[0-9]\|Proposition~[0-9]' "$TEX" \
  | grep -v '\\ref{' | grep -v '\\cite'
```

**Pass (step 2):** zero lines — all remaining hits are genuine internal hardcoded refs.
Lines filtered out by step 2 (`\cite` present) are external citations; verify those via P25.

---

### P2 — Every `\label` is referenced at least once

```bash
grep -P '\\label\{[^}]+\}' "$TEX" | while IFS= read -r LINE; do
  echo "$LINE" | grep -q 'xref-only' && continue
  L=$(echo "$LINE" | grep -oP '(?<=\\label\{)[^}]+')
  n=$(grep -cE "\\\\(eqref|ref)\{$L\}" "$TEX" 2>/dev/null || true)
  [ "$n" -eq 0 ] && echo "UNUSED: $L"
done
```

**Pass:** zero `UNUSED` lines.  Exception: labels referenced only from a table of
contents or external hyperlink — mark with `% xref-only`.

---

### P3 — Every bibliography entry is cited

```bash
grep -oP '\\bibitem\{[^}]+\}' "$TEX" | sed 's/\\bibitem{//;s/}//' | while read K; do
  n=$(grep -c "\\\\cite[^{]*{[^}]*\\b$K\\b" "$TEX" 2>/dev/null)
  [ "$n" -eq 0 ] && echo "UNCITED: $K"
done
```

**Pass:** zero `UNCITED` lines.

---

### P4 — Clean LaTeX compilation (three passes)

```bash
cd "$(dirname "$TEX")"
for i in 1 2 3; do
  pdflatex -interaction=nonstopmode "$(basename "$TEX")" 2>&1
done | grep -E "undefined|Warning.*ref|Warning.*cite|Error" \
      | grep -v 'Overfull\|Underfull'
```

**Pass:** zero lines (Overfull/Underfull acceptable at draft stage; fix before final
submission).

---

### P5 — Short title semantically matches full title

```bash
grep -n '\\title\[' "$TEX"
```

Manually verify the bracketed short title preserves all load-bearing qualifiers
(e.g. "Formal", "Exact", "Conditional") that distinguish the paper's actual scope
from a broader claim.

---

## PART II — Mathematical content integrity

### Preliminary: preamble inventory (run once before Parts II–IV)

Many checks in Parts II–IV search for specific LaTeX token sequences.  Papers routinely
define custom macros (`\newcommand`) and theorem-like environments (`\newtheorem`) that
expand to those sequences — a grep for `\mathcal{C}` silently misses `\Csub`.

Run these two commands once and keep the output nearby when running subsequent checks:

```bash
# All custom \newtheorem environment names (feed into P6, P30, P35)
grep '\\newtheorem{' "$TEX" | grep -oP '(?<=\\newtheorem\{)[^}]+'

# All custom \newcommand / \DeclareMathOperator definitions (feed into P7, P28, P34, P35)
grep '\\newcommand\|\\DeclareMathOperator\|\\renewcommand' "$TEX" \
  | grep -oP '\\newcommand\{[^}]+\}\{[^}]+\}' | head -40
```

When a subsequent check says "grep for `X`", also grep for every macro that expands to
`X`.  This manual step cannot be automated without a LaTeX expansion engine; be explicit
about it.

---

### P6 — Every lemma / proposition / theorem is used in a later proof

```bash
grep -oP '\\label\{(lem|thm|prop|cor):[^}]+\}' "$TEX" \
  | sed 's/\\label{//;s/}//' | while read L; do
  n=$(grep -c "\\\\ref{$L}" "$TEX")
  [ "$n" -eq 0 ] && echo "UNUSED RESULT: $L"
done
```

For each `UNUSED RESULT`: (a) use it in a proof, (b) remove it, or (c) add a comment
explaining it is background context only.

---

### P7 — Definition consistency: same predicate, same wording throughout

For each formally defined object (predicate, class, map), grep for its name and verify
every occurrence uses identical quantifiers and modifiers.

```bash
# Adapt the grep pattern to your key defined terms
grep -n "<your-key-term>" "$TEX"
```

**Pass:** all occurrences use identical wording, or differences are explicitly flagged
as "informal paraphrase."

---

### P8 — Every *restatement* of a prior result is attributed at first use

This check targets lemmas that restate or directly depend on a known published result.
**Original results proved in this paper legitimately have no citation** and should not
be flagged.

A lemma is a *restatement* candidate if its optional title argument `[...]` contains
an author name, an attribution keyword ("following", "cf.", "after"), or a well-known
theorem name.  Plain descriptive titles ("Quartet Li asymptotics", "Full rank of C")
indicate original results.

```bash
# Flag theorem-like environments whose title suggests prior art attribution
grep -n '\\begin{\(lemma\|proposition\|corollary\)}\[.*\(Bombieri\|Hadamard\|Karamata\|Weyl\|Tauberian\|Ikehara\|Hardy\|Titchmarsh\|Suzuki\|Connes\|Hurwitz\|Montel\|Conway\|Seeley\|BGV\|Gilkey\|following\|cf\.\|after \)' "$TEX"
```

For each hit: verify a `\cite{...}` appears in the environment opener or its first two
lines.  For hits NOT matching the pattern above, no citation is required — skip them.

**Manual supplement:** for any lemma that *uses* (rather than restates) an external
result as a key step, the citation should appear at that step inside the proof
(checked by P16), not necessarily in the lemma statement.

---

### P9 — Asymptotic error orders verified by script

For every displayed asymptotic $f(T) = g(T) + O(T^{-k})$:

1. Point to a script in `checker/` or `discovery/` that independently expands $f$ to
   the stated order.
2. Confirm the remainder is $O(T^{-k})$, not $O(T^{-(k-1)})$.
3. If the order improvement relies on a parity/symmetry cancellation, state the symmetry
   explicitly (see also P19).

```bash
grep -n 'O(T\^{-\|O(T^{-\|o(T\^{-\|o(T^{-' "$TEX"
```

---

### P10 — No informal qualifiers in formal definitions or theorem statements

```bash
grep -n 'nontrivial\|clearly\|obvious\|trivially\|it is easy to see\|well-known' "$TEX"
```

In **formal definitions and theorem statements**: remove or replace with a precise
condition.  In proof text: acceptable only if genuinely self-evident; flag for review.

---

### P11 — All formulas in remarks / footnotes verified

```bash
awk '/\\begin{remark}/,/\\end{remark}/' "$TEX"
```

For each formula in a remark: (a) are the preconditions satisfied for the objects being
discussed, not merely for superficially similar objects? (b) is every claimed identity
or inequality independently verifiable?

---

### P19 — Parity/symmetry arguments proven to sufficient order

When a proof invokes a parity/symmetry argument to cancel an error term, the expansion
must be displayed to **one order beyond** the claimed cancellation.  Show the next real
part is non-zero (or state its sign) — do not leave the cancellation implicit.

```bash
grep -n 'purely imaginary\|purely real\|odd.*order\|even.*order\|imaginary part\|real part.*vanish' "$TEX"
```

---

### P20 — No unsupported strong number-theoretic or analytic assertions

Assertions such as "is transcendental", "is irrational", "cannot be rational", or
"is provably" outside a formal proof require an explicit citation or must be weakened
to a hedged phrasing ("is not currently known to be rational").

```bash
grep -n 'transcendental\|irrational\|cannot be rational\|must be algebraic\|provably\b' "$TEX" \
  | grep -iv '%'
```

**Pass:** every hit either falls inside a `\begin{proof}` block with the claim derived
there, or is immediately followed by `\cite{...}`, or uses a hedge.

---

### P21 — "Analogous argument" claims have no in-paper refutation

```bash
grep -n 'analogous\|same argument\|by the same reasoning\|same proof' "$TEX"
```

For each hit: search the paper for the specific object named in the analogy claim and
verify no other passage adds a restriction that contradicts it.  If a later section
limits the analogy, qualify or remove the earlier claim.

---

## PART III — Formal definition and citation rigor

---

### P22 — External theorem invocations name all substituted parameters

When a proof invokes an external theorem ("By Andersson \cite{...}, Theorem 5"), the
proof text must state what specific objects and parameter values are being substituted
into that theorem's hypotheses.  A bare citation without a parameter-mapping is
insufficient.

```bash
grep -n 'By.*\\cite\|by.*\\cite\|Apply.*\\cite\|Applying.*\\cite\|invoking.*\\cite' "$TEX"
```

For each hit: verify the sentence or the immediately following one names the specific
inputs.

---

### P23 — Operator class definition: formal symmetry precedes self-adjoint extension

When an operator class definition depends on an extension theorem (KLMN / Friedrichs /
Lax–Milgram), the definition must first establish **formal symmetry** and
**semi-boundedness** on a dense domain *before* invoking the extension.
Self-adjointness may not be assumed as a hypothesis and then derived by KLMN: that is
circular.

```bash
grep -n 'KLMN\|Friedrichs\|self-adjoint.*extension\|quadratic form\|form domain' "$TEX"
```

For each hit: verify the surrounding block lists (i) formally symmetric on $C^\infty(M)$
and (ii) semi-bounded on $C^\infty(M)$ as explicit conditions **prior** to the extension
statement.

---

### P24 — Optional theorem-environment titles do not repeat the automatic label

`\begin{theorem}[D]` renders as "Theorem 1 (D)" when automatically numbered 1 — and
as "Theorem D (D)" if the counter already produces "D".  Check the rendered output does
not duplicate the label.

```bash
grep -n '\\begin{.*}\[' "$TEX"
```

---

### P25 — Literature formula descriptions match the cited source exactly

When the text describes a formula from a cited external result, check it against the
source file in `baseline/` (or the arXiv tarball) — not from memory.  Common failure
modes: (a) conflating two normalizations in the same paper; (b) omitting an open step
that the cited paper names explicitly; (c) describing the theorem's conclusion as if
the open step were closed.

```bash
grep -n '\\cite{' "$TEX" | grep -v '\\begin{proof}\|\\end{proof}' | head -30
```

For each hit outside a proof block: open the corresponding source and verify the
displayed formula matches the cited paper's exact statement, and that any open step
named in the source is also flagged as open in this paper's description.

---

### P26 — Reference operator construction: no spurious symbol-class terms

When a proof constructs a reference operator $P = P_0 + bI$ by adding a positive
constant to ensure positivity, the difference $Q = H - P$ contains a $-bI$ term of
order 0.  For $m < 1$ and $\varepsilon < 1-m$, this means $-bI \notin
\Psi^{m-1+\varepsilon}_{1,0}$.  The claim "$Q \in \Psi^{m-1+\varepsilon}$" is then
wrong.

```bash
grep -n 'positive constant\|P\s*:=\|P\s*=.*bI\|ensure.*P.*ge\|P.*\ge.*c' "$TEX"
```

For each hit: verify one of: (a) $P = A^*A + \Pi_{\ker A}$ (no additive constant); or
(b) the constant is split explicitly as a direct form contribution; or (c) the
symbol-class claim is restricted to $\varepsilon > \max(0,1-m)$.

---

### P27 — Tauberian theorems used in both directions are stated as biconditionals

When a Tauberian theorem (Karamata, Wiener–Ikehara, etc.) is invoked in both the
forward direction ($N \Rightarrow Z$) and the inverse direction ($Z \Rightarrow N$),
the cited theorem must be a biconditional ($\iff$).

```bash
grep -n 'Karamata\|Tauberian\|Ikehara\|Wiener.*Ikehara' "$TEX"
```

For each hit: trace the cited theorem and confirm the $\Leftarrow$ direction is stated.
If only $\Rightarrow$ appears, replace "one needs" with "one sufficient condition is."

---

### P28 — Single-letter symbol conflicts resolved

```bash
grep -n '\\begin{definition}' "$TEX" | while IFS=: read lineno rest; do
  window=$(sed -n "${lineno},$((lineno+15))p" "$TEX")
  echo "Line $lineno: $(echo "$window" | grep -o '\$[A-Z]\$' | sort -u | tr '\n' ' ')"
done
```

For each definition block: list the single-letter capitals introduced; verify none
conflicts with a same-letter symbol introduced elsewhere (strip, domain, set, space).

---

### P29 — `\texorpdfstring` bookmark text matches formula's logical meaning

When `\texorpdfstring{$formula$}{bookmark-text}` is used, the bookmark text must express
the *logical content* of the formula under the definitions in force — not just a
literal reading of the symbols.

```bash
grep -n '\\texorpdfstring' "$TEX"
```

For each hit: re-derive what the formula asserts in plain language; compare with the
bookmark text.

**Common failure mode:** a binary relation $R(A,B)$ reads as "$A$ does not $R$ $B$" in
the symbol string, but the defined meaning of $R$ makes $B$ the active agent, so the
correct reading is "$B$ does not [inverse of $R$] $A$".

---

### P30 — Every free variable in a theorem/corollary statement is explicitly bound

Papers often define custom theorem-like environments with `\newtheorem` (e.g.
`mainthm`, `maincor`, `mainthmprime`).  The grep pattern must include these, or the
main theorems — the most important results — will be silently skipped.

```bash
# Step 1: extract all custom \newtheorem environment names from the preamble
ENVS=$(grep '\\newtheorem{' "$TEX" | grep -oP '(?<=\\newtheorem\{)[^}]+' | tr '\n' '\|')
ENVS="theorem|corollary|proposition|${ENVS%|}"   # add standard names
echo "Checking environments: $ENVS"

# Step 2: check each environment for free variables
grep -nP "\\\\begin\\{($ENVS)\\}" "$TEX" | while IFS=: read lineno rest; do
  window=$(sed -n "${lineno},$((lineno+15))p" "$TEX")
  echo "--- Line $lineno ---"; echo "$window"; echo
done
```

For each block: every capital letter and named parameter must be bound by
"Fix $K\ge 1$", "for all $K\ge 1$", "Let $M$ be a…", or as a conclusion variable
in the "there exists" clause.  A parameter appearing only in the conclusion with no
"for some" or "there exists" quantifier is a free variable.

**Known limitation:** `\newtheorem` names inside `\begin{comment}` or conditionally
compiled sections are also extracted — inspect the `ENVS` list before running Step 2.

**Step 3 (new) — "as above" cross-references inside theorem bodies.**
A theorem statement that says "Let $H$ be as above" or "as defined above" is not
self-contained: a reader who encounters the theorem in isolation (e.g. from a citation)
cannot reconstruct the hypotheses.  Flag every occurrence.

```bash
# Detect "as above / as defined above / as before" inside theorem-like environments
ENVS=$(grep '\\newtheorem{' "$TEX" | grep -oP '(?<=\\newtheorem\{)[^}]+' | tr '\n' '\|')
ENVS="theorem|lemma|corollary|proposition|${ENVS%|}"

grep -nP "\\\\begin\\{($ENVS)\\}" "$TEX" | while IFS=: read lineno rest; do
  window=$(sed -n "${lineno},$((lineno+20))p" "$TEX")
  echo "$window" | grep -qiE 'as above|as defined above|as before|notation above' && \
    echo "FINDING P30(step3): Line $lineno — cross-reference phrase inside theorem body"
done
```

Replace every flagged phrase with a brief inline restatement of the relevant hypothesis.

---

### P31 — "Same argument as part (X)" spells out the conclusion for part (Y)

When a multi-part proof abbreviates with "by the same argument as part~(X)", the
*conclusion* of that sub-proof must be stated explicitly for part~(Y).

```bash
grep -n 'same argument\|analogous argument\|as part~\|as in part' "$TEX"
```

For each hit: verify the conclusion of the current part is spelled out, not left
implicit behind the abbreviation.

---

### P32 — Canonical realization identified by name after its construction

When a definition constructs a Friedrichs (or other canonical) realization $H_F$, the
text immediately after `\end{definition}` must state explicitly that $H$ henceforth
denotes $H_F$ and that all spectral objects refer to $H_F$.  Without this, theorems
using $N_H$ or $\operatorname{spec}(H)$ are technically undefined for the formal operator.

```bash
grep -n 'Friedrichs\|H_F\|self-adjoint.*extension\|canonical.*realization' "$TEX"
```

---

### P33 — Statement-proof domain mismatch: statement must cover the full domain used by proof and downstream

When a proof establishes a result for a **broader domain** than the lemma statement
claims (e.g. proof uses only "distinct positive reals", statement restricts to "positive
rationals"), and downstream theorems use the result over the broader domain, the
statement must be upgraded.

Also: if downstream usage relies on **connectivity** of the domain (for analytic
continuation, IFT, or an isolation argument), that connectivity must be an explicit
hypothesis or conclusion of the lemma.

```bash
# Proofs that mention real/positive-real but statements may not
grep -n '\\begin{lemma}\|\\begin{proposition}' "$TEX" | while IFS=: read lineno rest; do
  proof=$(sed -n "${lineno},$((lineno+40))p" "$TEX")
  echo "$proof" | grep -qi 'real\|\\mathbb{R}\|distinct.*real' && \
    echo "Line $lineno: proof mentions real — check statement domain"
done
# Downstream sites using lemma labels
grep -n '\\ref{lem:' "$TEX" | grep -v '\\begin{lemma}' | head -20
```

**Manual check:** for each flagged lemma, (a) record the actual domain used in the
proof; (b) record the claimed domain in the statement; (c) find every downstream `\ref`
site; (d) check the site requires the actual domain; (e) if yes, upgrade the statement.

**Precedent:** Lemma 3.1 (paper-A) stated for positive rationals; proof needed only
distinct positive reals; lines 895–908 used it over the open real set $\Omega$.

---

### P34 — Spectral/counting definition domain covers every operator sub-class that uses it

When formal spectral invariants ($N_H$, $Z_H$, $\operatorname{spec}_\times(H)$, heat
trace, etc.) are defined for a **restricted operator class** (e.g. non-negative,
positive-definite), verify that every operator appearing in a theorem that invokes
those invariants provably belongs to that class — or extend the definition to a broader
class (e.g. lower-semibounded with finitely many negative eigenvalues) and state the
extension explicitly.

**Macro-blindness warning:** papers commonly define shorthand macros for spectral
invariants (e.g. `\newcommand{\Nop}{N_H}`).  The grep below will miss those unless
you also search for the macro names.

```bash
# Step 1: find macro names that expand to spectral invariants
grep '\\newcommand' "$TEX" | grep -iE 'N_H|Z_H|spec|Tr|heat|count' | head -10
# Step 2: find spectral invariant definitions (raw LaTeX and common macro names)
grep -n 'N_H\|Z_H\|\\operatorname{spec}\|\\operatorname{Tr}' "$TEX" | head -20
# Also search inside \begin{definition}...\end{definition} blocks
awk '/\\begin\{definition\}/,/\\end\{definition\}/' "$TEX" \
  | grep -n 'non-negative\|lower.*semi\|positive.*definite\|H\s*\ge\|H\s*>\s*0' | head -20
# Step 3: find operator classes in theorem headers (including custom macro names)
grep -n '\\mathcal{C}\|H_F\|lower.*semibounded\|semi.*bound\|\\lambda_1\le\|\\Csub' "$TEX" | head -20
```

**Manual check:** build a 2-column table — column 1: restrictions in the invariant
definition; column 2: operator classes in theorems using that invariant.  For each pair,
write one sentence confirming the class satisfies the restriction.

**Precedent:** $N_H$, $Z_H$ defined for non-negative $H$; but $H_F \in \mathcal{C}_\mathrm{sub}$
can have finitely many negative eigenvalues (paper-B).  Finite negative spectrum does not
affect the asymptotic but the definition must permit it.

---

### P35 — Parameterized class superscripts re-quantified in dependent theorems; local symbol constants localized

**Part A — parameter re-quantification.**
When a definition introduces a class $\mathcal{C}^{m,K}(M)$ with superscript parameters,
every theorem asserting membership in or properties of that class must either (a)
universally quantify all parameters ("for all $m \ge 1$, $K \ge 1$, compact $M$…") or
(b) reference a fixed previously-named instance.

**Macro-blindness warning:** the class name is often a custom macro (e.g. `\Csub`).
Extract macro names from the preamble and include them in the grep.

```bash
# Step 1: find macros that name the parameterized class
CLASS_MACROS=$(grep '\\newcommand' "$TEX" | grep -oP '\\newcommand\{\\[^}]+\}' \
  | grep -i 'sub\|ell\|logpoly\|class\|Cscr\|Hscr' | grep -oP '(?<=\{\\)[^}]+')
echo "Class macros to check: $CLASS_MACROS"

# Step 2: find custom \newtheorem environment names (so mainthm/maincor are included)
ENVS=$(grep '\\newtheorem{' "$TEX" | grep -oP '(?<=\\newtheorem\{)[^}]+' | tr '\n' '\|')
ENVS="theorem|corollary|${ENVS%|}"

# Step 3: check theorem headers for the class name (raw LaTeX and macros)
grep -nP "\\\\begin\\{($ENVS)\\}" "$TEX" | while IFS=: read L _; do
  window=$(sed -n "${L},$((L+10))p" "$TEX")
  echo "$window" | grep -qE '\\mathcal\{C\}|\\mathcal\{H\}|\^\{m|\\Csub|\\Hscr' && \
    echo "Line $L: check class parameters re-quantified"
done
```

**Part B — local vs global symbol constants.**
Symbol/PDE estimates $|(\partial^\alpha_x\partial^\beta_\xi a)(x,\xi)| \le C_{\alpha\beta}$
are valid only locally when the symbol $a$ is defined on a coordinate patch $U$.  The
constant must be $C_{\alpha\beta,U_0}$ for every $U_0 \Subset U$, not a global constant,
unless the manifold is compact and the operator is globally defined.

```bash
grep -n 'C_.*alpha\|symbol.*estim\|uniform.*bound.*symbol' "$TEX"
```

**Manual check (B):** for each symbol estimate, verify whether $a$ is a patch symbol;
if so, confirm the bound writes $C_{\alpha\beta,U_0}$ and states "$U_0 \Subset U$."

**Part C — notation consistency between a definition's parameter domain and theorem statements.**
When a definition introduces a parameter with a specific type (e.g. $K\in\mathbb{N}_0$,
$m\in\mathbb{Z}_{>0}$, $p\in[1,\infty)$), every theorem that re-quantifies that parameter
must use the **same type notation**, not a weaker or different form (e.g. $K\ge 0$
silently admits non-integer values; $m>0$ allows non-integer orders).

```bash
# Identify parameter-with-type declarations in \begin{definition}...\end{definition}
grep -n '\\in\\mathbb\|\\in\\NN\|\\in\\ZZ\|\\in\[' "$TEX" | head -30

# Then for each parameter name found (e.g. K, m), grep theorem headers for the same
# parameter with a potentially weaker type
PARAM=K    # set to each parameter found above
grep -n "\\\\begin{theorem\|\\\\begin{mainthm\|\\\\begin{lemma" "$TEX" | \
  while IFS=: read L _; do
    window=$(sed -n "${L},$((L+6))p" "$TEX")
    echo "$window" | grep -qP "\b${PARAM}\b" && \
    echo "$window" | grep -vqP "${PARAM}\\\\in\\\\mathbb|${PARAM}\\\\in\\\\NN" && \
      echo "Line $L: $PARAM appears without set-membership type — check consistency"
  done
```

**Manual check (C):** for each flagged line, open the original definition and compare the
declared type.  If the theorem weakens the type (e.g. $K\ge 0$ when definition says
$K\in\mathbb{N}_0$), replace with the definition's type.

**Precedent (paper-B):** Definition used `$K\in\mathbb{N}_0$`; Theorem~D$'$ wrote
`$K\ge 0$` — silently admitting non-integer $K$ where the symbol expansion is undefined.

**Precedent (paper-B):** $\mathcal{C}_\mathrm{sub}$ (macro `\Csub`) used in Theorem D$'$
without re-quantifying $m,K,M$; local symbol estimate wrote $C_{\alpha\beta}$.

### P36 — Existence vs construction: citation qualifier when a specific object is needed

When a theorem has an **existence conclusion** (proved by compactness, contradiction,
or a non-constructive argument) but a downstream proof uses a **specific object**
produced by that theorem, the citation must be qualified:

> By the **construction in the proof of** Theorem~X (equivalently, equation~$(\star)$), …

A bare "By Theorem~X" implies only that some object with the stated properties exists.

```bash
grep -n 'By Theorem\|by Theorem\|By Corollary\|by Corollary' "$TEX" \
  | grep -v 'proof\|construction\|equation\|formula\|explicit' | head -30
```

For each hit: determine whether the downstream argument uses only existence or relies on
a specific construction.  If the latter, add "the construction in the proof of."

**Precedent (paper-A):** line 922 cited "By Theorem~A" but needed the specific
parameters from the construction (equation $(\star)$).

---

### P37 — Degenerate-parameter case convention explicit in counting / combinatorial formulas

When a counting or combinatorial formula admits a **degenerate parameter value** where
the geometric object collapses or a multiplicity changes (e.g. $\sigma_0 = 1/2$ makes
a four-point orbit collapse to two on-line points each with multiplicity 2), the
multiset interpretation and the resulting formula for that special case must be stated
explicitly — either as an additional case or in an immediately adjacent remark.

```bash
# Find counting / orbit formulas and the parameter domain
grep -n 'multiset\|orbit.*multiplicity\|with multiplicity\|degenerate\|special.*case' "$TEX" | head -20
grep -n '\\sigma_0\|\\beta_0\|degenerate\|boundary.*case' "$TEX" | head -20
```

For each counting formula: list all boundary values of each parameter in its domain;
work out what the formula gives at each boundary; confirm it matches the geometric
meaning.

**Precedent (paper-A):** $Q(\sigma_0,T)$ for $\sigma_0=1/2$ gives $Q(1/2,T)=2L(T)$;
this multiset collapse was not stated.

---

### P38 — Self-adjointness inner product named at every invocation

When a theorem asserts, or cites a result asserting, that an operator is **self-adjoint**,
the **inner product** must be named — especially when a non-standard inner product
(Weil quadratic form, Sobolev form, graph inner product) is in play.  A bare "is
self-adjoint on $\mathcal{H}$" is incomplete when $\mathcal{H}$ admits multiple natural
inner products.

```bash
grep -n 'self-adjoint\|self.adjoint\|hermitian\|symmetric.*operator' "$TEX" | head -30
```

For each hit: identify the inner product.  If non-standard, verify the text names it.
For cited results, open the source and confirm the inner product matches.

**Precedent (paper-B):** CCM Theorem 5.10 asserts self-adjointness on
$E_N' \oplus E_N^\perp$ with the Weil quadratic form-induced inner product, not the
standard $L^2$ inner product; the description omitted this.

---

## PART IV — Scope, methodology, and evidence quality

---

### P12 — No-go / impossibility theorem: all five components explicit

A result may be labeled a *barrier*, *no-go theorem*, or *obstruction* only when the
paper explicitly states all five:

1. **Method class** (membership is checkable, not ad hoc)
2. **Ambient object class** (the universe of objects being considered)
3. **Observation map** (what the method can see)
4. **Target predicate** (what the method is trying to decide)
5. **Escape route** (an explicit construction outside the method class, proving
   non-vacuity)

```bash
grep -n 'barrier\|obstruction\|no-go\|impossibility\|cannot prove' "$TEX" | grep -iv '%'
```

For each hit: verify all five components are named in the theorem statement or
immediately adjacent text.

**Why escape route is mandatory:** without it, the theorem is vacuous (the method class
might be empty; the observation map might never be exact).

---

### P13 — No equivalence reformulation claimed as an impossibility result

An equivalence criterion ($C \iff P$) **locates** difficulty; it does not prove
impossibility.  A result may not be labeled "barrier" or "obstruction" solely on the
basis of being equivalent to the target predicate.

```bash
grep -n 'equivalent.*\|iff\b\|if and only if' "$TEX" | grep -iv '%' | head -20
```

For each hit: confirm the result is labeled "equivalent reformulation" or "locates
difficulty," **not** "barrier" or "obstruction."

---

### P14 — Abstract and introduction scope claims bounded to what theorems prove

```bash
sed -n '/\\begin{abstract}/,/\\end{abstract}/p' "$TEX"
sed -n '/\\section{Introduction}/,/\\section{/p' "$TEX" | head -80
```

Manually verify: no sentence implies a stronger conclusion than the theorems prove.
Common over-reach patterns:
- "this suggests [X]" when the theorems only rule out a *sub-class* of approaches to X
- "this is consistent with [conjecture Y]" when the argument does not actually bear on Y
- scope words ("any", "all", "every") not matched by the theorem's quantifiers

---

### P15 — Analogies to other impossibility frameworks labeled motivational

When the paper draws a structural analogy to another impossibility framework (natural
proofs, relativization barriers, information-theoretic lower bounds, etc.):

```bash
grep -n 'natural proof\|Baker.*Gill\|relativiz\|information.*theoretic.*lower\|barrier.*analog' "$TEX"
```

For each hit: confirm the text contains a qualifier such as "structural and motivational,
not a formal reduction."  A bare analogy without this disclaimer overstates the result.

---

### P16 — Evidence level for every imported premise

Every claim imported from the literature that is used as a **premise** in a proof must
carry a verified evidence level.  Recommended two-axis taxonomy:

| Axis | Allowed values |
|---|---|
| Mathematical | `DEFINITION`, `CONJECTURE`, `PROOF-DRAFT`, `INDEPENDENTLY-CHECKED`, `REFEREED` |
| Computational | `NONE`, `EXPLORATORY`, `REPRODUCIBLE`, `INDEPENDENT-CHECKER`, `FORMALIZED` |

- A repository deposit / DOI is **archival publication, not peer review.**
- A finite verification certificate validates only the finite instance replayed, never
  the analytic theorem producing it.
- Status is **derived by the checker**, never self-declared by the generator.

```bash
grep -n '\\cite{' "$TEX" | while IFS=: read lineno rest; do
  context=$(sed -n "$((lineno-3)),$((lineno+3))p" "$TEX")
  echo "$context" | grep -q '\\begin{proof}\|therefore\|hence\|it follows\|by.*,' \
    && echo "Line $lineno: cite in proof context — verify evidence level: $rest"
done | head -30
```

---

### P17 — Invariance under method class transformations

When a quantity is proposed as a "margin", "measure of complexity", or "lower bound" for
a method class, verify it is **invariant** under every transformation the method class
allows (rescaling, congruence, preconditioning, basis change, etc.).

```bash
grep -n 'margin\|complexity.*measure\|lower bound\|Schur\|pivot\|shift.*I\|c_a\|c_L' "$TEX"
```

For each margin-like quantity:
- If it is orthogonally invariant, it factors through the **eigenvalue multiset** (spectral
  theorem) — it cannot detect eigenvector localization.
- If it depends on a basis, it can be reduced to a constant by choosing the eigenbasis —
  it is a representation artifact, not a universal bound.
- A quantity that stays provable while tending to zero is a *diagnostic*, not a barrier.

---

### P18 — Constructive/existential qualifier: definition honors downstream corollaries

When a formal definition contains "explicit", "constructive", "computable", or
"effective", every theorem that claims to produce an instance must satisfy the qualifier.
A non-constructive proof (compactness, contradiction) must either (a) have the definition
allow existential instances, or (b) remove the qualifier.

```bash
grep -n 'explicit\|constructive\|computable\|effective' "$TEX" | grep -v '%'
awk '/\\begin\{definition\}/,/\\end\{definition\}/' "$TEX"
```

---

## PART V — Proactive per-theorem structural audit

**Run this section once for every new or substantially revised theorem / lemma /
corollary before running any grep from Parts I–IV.**  If you answer S1–S5 honestly,
most defects caught by Parts I–IV become impossible by construction.

These five questions derive from the fundamental invariants of rigorous mathematical
writing.  They are *complete* in the sense that their scope covers every defect class
currently in Parts I–IV and any new class of the same structural type.

---

### S1 — Hypothesis shadow test
*Catches: undeclared domain extensions (P33), definition domain gaps (P34), missing
inner-product specifications (P38), and any hidden assumption of any kind.*

**What to do:**
Read the proof body.  For every step of the form "since [property P] holds for [object X]",
ask: **where is P established for X?**

Classify each such use into one of:
- **(H)** — P is an explicit hypothesis of the theorem statement.
- **(D)** — P follows directly from a definition in scope.
- **(L)** — P is proved by a cited lemma (go to S3 for that citation).
- **(GAP)** — P is neither of the above.

Any `(GAP)` is a defect.  Resolution options:
- Add P as an explicit hypothesis.
- Prove P from the existing hypotheses and insert the proof.
- Restructure the proof to avoid needing P.

**Written output required:** a table with columns `[Step]`, `[Property used]`,
`[Object]`, `[Classification]`.  Every row must be `(H)`, `(D)`, or `(L)`.

```bash
# Aid for finding implicit uses: look for "since", "note that", "observe that",
# "clearly", "because" in proof blocks
awk '/\\begin{proof}/,/\\end{proof}/' "$TEX" \
  | grep -n 'since\|note that\|observe\|clearly\|because\|follows from'
```

**Red flags that indicate a gap:**
- "by continuity" — of what function, on what domain, proved where?
- "by the previous lemma" — does the object satisfy the lemma's domain restriction? (→ S2)
- "it suffices to assume" — is this actually sufficient, or is it only necessary?
- "WLOG" — does the reduction preserve every property used later in the proof?
- "analogously" — does the analogy go through for *this* object? (→ P21)

---

### S2 — Definition domain coverage table
*Catches: spectral invariant domain gaps (P34), parameterized class coverage (P35),
citation scope errors (P22), and any use of a tool outside its stated domain.*

**What to do:**
For every formal definition or cited result D used in the paper, build the following
table:

| Definition / Lemma | Domain restriction(s) | Objects in this paper that invoke D | Verification sentence |
|---|---|---|---|
| [name] | [e.g. "H ≥ 0", "t_k distinct positive reals"] | [list] | [one sentence per object] |

**Pass condition:** the Verification sentence column is non-empty for every row, and
every sentence is either a reference to a hypothesis or a short derivation.

**Common coverage failures:**
- A spectral invariant defined for non-negative operators applied to a lower-semibounded one.
- A Weyl-law result stated for second-order differential operators applied to a
  pseudodifferential operator.
- A Hurwitz-type theorem stated for entire functions applied to a meromorphic function.
- A convergence theorem stated for compact sets applied on an unbounded domain.

For any coverage failure: either extend the definition explicitly, or add the restriction
as a hypothesis.

```bash
# Find all definitions and their domain words
awk '/\\begin{definition}/,/\\end{definition}/' "$TEX" \
  | grep -n 'non-negative\|positive\|compact\|distinct\|entire\|meromorphic\|classical' | head -30
# Find all invocations of defined objects outside their definition blocks
grep -n '\\ref{def:\|by Definition\|by the definition of' "$TEX" | head -20
```

---

### S3 — Citation full instantiation record
*Catches: bare citations in proofs (P22), existence-vs-construction errors (P36),
wrong theorem number (P25, L17), and wrong version/normalization (L22).*

**What to do:**
For every `\cite{...}` occurring inside a `\begin{proof}...\end{proof}` block, write
a one-line instantiation record of the form:

> Apply [Author], [Theorem/Lemma N] with: [list of specific substitutions] ↦ [objects in
> current proof].  Conclusion used: [specific conclusion, not the full theorem].

Additionally, for each citation answer these three questions:
1. **Type:** is the conclusion an existence statement or does the proof produce a specific
   construction?  If specific construction, cite "the construction in the proof of Theorem N."
2. **Version:** is the cited theorem from a preprint or a published version?  If both exist,
   record both equation/theorem numbers (preprint vs journal pagination may differ).
3. **Normalization:** does the cited paper use the same normalization convention as this
   paper for every object in the instantiation?  Write the normalization explicitly.

```bash
# Extract all citations inside proof blocks
awk '/\\begin{proof}/,/\\end{proof}/' "$TEX" | grep -n '\\cite{' | head -40
```

**Pass condition:** every proof-internal `\cite` has a written instantiation record.

---

### S4 — Parameter boundary sweep
*Catches: degenerate-case convention gaps (P37), vacuous targets (see PROMPT_LINT L6),
and formula errors at domain boundaries.*

**What to do:**
For every formula, counting function, or asymptotic that involves a **parameter**
$p \in D$ (where $D$ is a stated domain):

1. List all **interior** behavior (what the formula does generically).
2. List all **boundary values** of $D$ (endpoints, zeros, special values where a
   symmetry is gained/lost, or where the geometric object degenerates).
3. For each boundary value, evaluate the formula and verify the result agrees with
   the geometric or mathematical meaning.
4. If the formula collapses or changes character at a boundary (e.g. a quartet becomes
   two double-counted points), state the special-case formula explicitly.

```bash
# Find all parameter-indexed formulas
grep -n '\\sigma_0\|\\beta_0\|\\varepsilon\s*=\|p\s*=\s*[0-9]\|k\s*=\s*0\|m\s*=\s*1\b' "$TEX" | head -20
```

**Common boundary failures:**
- A parity argument that ceases to apply when a parameter equals its symmetry value.
- A counting formula that double-counts when two orbits coincide.
- An error bound that blows up or changes sign at the boundary of the parameter domain.
- A "without loss of generality" reduction that fails at a boundary case.

---

### S5 — Normalization source check
*Catches: formula description mismatches (P25), inner-product errors (P38), conflated
normalizations, and open-step suppression.*

**What to do:**
For every formula, constant, operator, or spectral object borrowed from the literature:

1. Open the **primary source** (arXiv tarball, published PDF, or `baseline/` directory).
2. Locate the **specific theorem or equation** by number.
3. Write its exact statement verbatim or as a close paraphrase.
4. Beside it, write your paper's version.
5. Verify they agree on: (a) normalization constants, (b) inner product, (c) whether any
   step in the cited theorem is itself open/conditional, (d) domain/range of every map.

```bash
# Find every place a formula is attributed to a citation
grep -n '\\cite{' "$TEX" | grep -v '\\begin{proof}' \
  | grep '=\|\\sim\|\\asymp\|\\le\|\\ge\|\\to' | head -30
```

**Common normalization traps:**
- Two results in the same paper that look similar but differ by a factor of 2 from
  distinct symmetrization conventions.
- A cited theorem with a meromorphic target (poles at zeros of a derivative) vs a
  cited theorem with an entire target (all zeros real) — distinct normalizations, never
  interchangeable.
- A self-adjointness result stated with respect to a non-standard inner product induced
  by a quadratic form, described in the paper as simply "self-adjoint."
- Preprint equation numbers shifted by ±1 relative to the published version.

**Pass condition:** for every imported formula, the source check is recorded and every
discrepancy is resolved.

---

### P39 — Open problems / questions sections: all variables defined inline

When a paper includes a section of open problems, questions, or conjectures, each
item is often written informally — but any parameter or object introduced there must
still be defined within that item.  A variable borrowed from the body (e.g. $N$, $K$,
$T$, $h$) without re-introduction becomes undefined if the reader reads the section
standalone, and the question itself may be ill-posed.

Common failure modes:
- "Does there exist $N$ such that…" where $N$ was defined much earlier as a specific
  sequence length, but here appears to be a free integer.
- "For the Weil test $h$…" when the body uses a finite family $h_1,\ldots,h_r$ but the
  question writes only $h$.
- A bound "denominator height $\le T^A$" where $A$ is not defined anywhere in the item.

```bash
# Find open-problem / conjecture / question sections
grep -n '\\section\|\\subsection' "$TEX" \
  | grep -i 'open\|question\|conjecture\|further\|remark' | head -10
# For each such section, extract its content and check for undefined single-letter params
```

**Manual check:** for each open-problem item, list every parameter and object that
appears; verify each is either (a) defined within the item itself ("let $N \ge 1$"),
(b) universally quantified ("for all $h \in \mathcal{H}$"), or (c) a standard
universally understood constant (e.g. $\pi$, $e$).

**Precedent (paper-A):** open problem used $N$ without definition (should be
"$\#\mathcal{Z}_\pm \le T^A$") and wrote $h$ where the body used $h_1,\ldots,h_r$.

---

### P40 — Uniform vs pointwise index quantification in asymptotic expansions

An asymptotic relation $f(j, T) \sim g(j, T)$ as $T\to\infty$ may hold
*for each fixed $j$* (with an error constant that depends on $j$) or
*uniformly in $j$* (with a single error constant). These are different statements:
the first allows $O_j(T^{-k})$; the second requires $O(T^{-k})$ with a $j$-independent
implicit constant. Conflating them is a correctness error: a result that holds "for
fixed $j$" cannot be summed over $j$ unless the dependence on $j$ is made explicit.

```bash
# Grep for asymptotics near an index variable — look for O(...) without O_j or O_n
grep -n 'O(T\|O(T^{-\|\\sim C\|\\asymp' "$TEX" | head -30

# Also grep for "uniformly" near summation contexts
grep -n 'uniformly\|uniform in\|for fixed' "$TEX" | head -20
```

**Manual check:** for each asymptotic line, determine:
1. Does the error constant depend on any free summation index (j, n, k)?
2. If yes: write $O_j(T^{-k})$ and add "for each fixed $j$" to the quantifier.
3. If the result is used in a sum over $j$: also bound the $j$-dependence explicitly.

**Precedent (paper-A):** $q_j(T) = 4j^2/T^2 + O(T^{-4})$ holds for each fixed $j$;
the implicit constant depends on $j$. Text should read
"For each fixed $j \ge 1$, $q_j(T) = 4j^2/T^2 + O_j(T^{-4})$."

---

### P41 — Author count in possessive references ("the author's" vs "the authors'")

When a paper is referenced with a possessive phrase ("the author's refinement",
"the authors' construction"), the grammatical number must match the actual authorship
of the cited work. Citing a solo-authored paper as "the authors'" or a multi-authored
paper as "the author's" is a factual error visible to the cited author.

```bash
# Grep for possessive author phrases near \cite
grep -n "the author" "$TEX" | grep -iv "present author\|this author"
```

**Manual check:** for each match, open the bibliography entry and count the authors.
Confirm singular/plural. For the present paper itself, use "the present author" (not
"we" if single-authored, not "the authors" if solo).

**Precedent (paper-A):** CCM 2025 (arXiv:2511.22755) has three authors; a phrase
"the present author's refinement" in a paper about it should be "the authors'
refinement."  Conversely, if a cited work has a single author, "the authors'" is wrong.

---

### P42 — Checker files referenced in text must exist in the repository

When the text references a file by path (e.g. "`checker/q2_sign_check.py`",
"`pilots/cert.json`"), that file must actually exist at the stated path. A missing
file means the claim "verified by [script]" is unverifiable and the companion
computation is unreproducible.

```bash
# Extract file paths referenced in the TeX source
grep -oE 'checker/[^ $}]+\|pilots/[^ $}]+\|scripts/[^ $}]+' "$TEX"

# For each path found, verify it exists
while IFS= read -r fpath; do
  [ -f "$fpath" ] || echo "MISSING: $fpath"
done < <(grep -oE 'checker/[^ $}]+|pilots/[^ $}]+|scripts/[^ $}]+' "$TEX")
```

**Manual check:** if a referenced file is missing, either (a) add the file to the
repo before submission, or (b) replace the reference with an inline exact value
(e.g. the rational certificate value) so the claim is self-contained without the file.

**Precedent (paper-A):** `checker/q2_sign_check.py` referenced in text but not
included; exact value $q_2(1/10)|_{\sigma_0=3/4} = -380550400/44102881 < 0$ should
be included inline.

---

### P43 — Trace class hypothesis for heat semigroup (operator theory)

The existence of a well-defined heat trace $Z_H(t) = \operatorname{Tr}(e^{-tH}) < \infty$
requires more than lower-semiboundedness with compact resolvent: $e^{-tH}$ must itself
be trace class. A counterexample: $He_n = \log(n+1)e_n$ has compact resolvent yet
$\operatorname{Tr}(e^{-tH}) = \sum_{n\ge 1}(n+1)^{-t}$ diverges for $0 < t \le 1$.

Situations where trace class is guaranteed without extra hypothesis:
- Classical elliptic operators of order $m > d$ on a compact $d$-manifold (by Weyl).
- Operators with explicit eigenvalue growth $e_n \sim C n^\alpha$ with $\alpha > 0$.

```bash
# Flag definitions of Z_H or heat trace near lower-semibounded / compact resolvent
# without an explicit trace class hypothesis
grep -n 'lower.semibounded\|lower semibounded\|semi-bounded\|compact resolvent' "$TEX"
grep -n 'Tr.*e\^{-t\|Z_H\|heat trace\|trace.*class' "$TEX"
```

**Manual check:** for each place where $Z_H(t) < \infty$ is assumed or used:
1. Is there an explicit "assume $e^{-tH}$ is trace class for all $t > 0$" hypothesis?
2. Or is trace class derived from Weyl asymptotics / eigenvalue growth?

If neither holds, add a hypothesis or restrict to operators where it is automatic.

**Precedent (paper-B):** the subsection defined $Z_H(t)$ for lower-semibounded
operators with compact resolvent without stating trace class; an explicit hypothesis
or a proof that the relevant subclass has trace class heat semigroup is required.

---

### P44 — Homogeneous principal symbol vs cutoff extension (spectral geometry / PDE)

In spectral geometry, the Weyl constant is computed from the *homogeneous* principal
symbol $h_m^{\mathrm{hom}}$, defined on $T^*M \setminus 0$ by positive homogeneity of
degree $m$: $h_m^{\mathrm{hom}}(x, r\xi) = r^m h_m^{\mathrm{hom}}(x, \xi)$ for $r > 0$.
Full symbols use a smooth cutoff: $\chi(\xi) h_m^{\mathrm{hom}}(x,\xi)$ (vanishing near zero).

**Two common errors:**
1. Writing the Weyl constant integral $\int\mathbf{1}_{\{h_m \le 1\}}$ without specifying
   whether $h_m$ is the homogeneous part or the cutoff extension — the integral can
   differ on $\{|\xi| \le 1\}$.
2. Using the cutoff symbol in an expansion but then citing a Weyl law whose proof
   requires the homogeneous symbol.

```bash
# Grep for Weyl constant / volume integral near chi or cutoff
grep -n '\\chi\|cutoff\|h_m.*hom\|hom.*h_m\|Weyl.*const\|int.*1_{h_m\|int.*{h_m' "$TEX"
# Grep for homogeneous notation
grep -n 'r\^m\|homogeneous.*degree\|degree.*m\|hom}' "$TEX" | head -20
```

**Manual check:** for each Weyl constant formula:
- Is it written in terms of $h_m^{\mathrm{hom}}$?
- Is the manifold part clearly $\{(x,\xi)\in T^*M: h_m^{\mathrm{hom}}(x,\xi) \le 1\}$?
- Does the proof of the Weyl law cited use the homogeneous or the truncated symbol?

**Precedent (paper-B):** symbol class $\mathcal{C}_{\mathrm{sub}}$ uses a cutoff
$\chi(\xi)$; the Weyl constant formula and the Hörmander/Lesch Weyl law references
must consistently refer to the homogeneous principal symbol $h_m^{\mathrm{hom}}$.

---

### P45 — No forward-referencing `\ref` inside `\begin{definition}` blocks

A definition is an axiomatic construct: it must not rely on a result that will only be
proved later. If a `\begin{definition}` block contains `\ref{thm:X}` (or
`\eqref{eq:Y}`) and `thm:X` (or `eq:Y`) is defined *after* the definition in the
source, this is a forward dependency — the definition implicitly assumes the existence
or truth of a result not yet established.

Common symptom: "The Friedrichs realization $H_F$ (see Theorem~\ref{thm:friedrichs})
is defined as…" where `thm:friedrichs` appears 50 lines later.

```bash
# Extract line numbers of all \begin{definition} and their \end{definition}
grep -n '\\begin{definition}\|\\end{definition}' "$TEX"

# For each definition block, grep for \ref or \eqref
sed -n '/\\begin{definition}/,/\\end{definition}/p' "$TEX" | grep -n '\\ref\|\\eqref'
```

**Manual check:** for each `\ref` / `\eqref` found inside a definition:
1. Locate the referenced label in the file.
2. If it appears *after* the definition, this is a forward dependency.
3. Resolution: either (a) move the referenced result before the definition, (b) state
   the needed property as a hypothesis of the definition, or (c) restructure as a
   "Definition + Proposition" pair where the proposition is proved immediately after.

**Precedent (paper-B):** the definition of $\mathcal{C}_{\mathrm{sub}}$ referenced
the Friedrichs realization (proved later), creating a circular dependency between the
class definition and the theorem that the realization exists.

---

### P46 — Classical operator hypothesis check: log-polyhomogeneous ≠ classical (PDE)

Theorems about classical pseudodifferential operators (Seeley's trace formula,
Atiyah–Singer index theorem, certain Weyl laws) require the operator to have a
*classical* symbol expansion: $\sigma(H) \sim \sum_j h_{m-j}$ with *positively
homogeneous* terms $h_{m-j}$, no logarithmic factors.  A log-polyhomogeneous class
$\mathcal{C}_{\mathrm{sub}}$ (or any class allowing $(\log|\xi|)^\ell$ factors) is
strictly larger than the classical class — adding a constant to a log-poly operator
does not remove the log factors and does not produce a classical operator.

**Common error pattern:**  a paper introduces a class $H\in\mathcal{C}^{\mathrm{logpoly}}$,
then invokes Seeley's trace-class theorem (which requires classical elliptic $H$) by
arguing "shift $H$ to make it positive, then apply Seeley."  The shift does not
eliminate the log terms.

```bash
# Grep for Seeley or classical trace citations near log-poly class usage
grep -n 'Seeley\|classical.*elliptic\|trace.*class\|Tr.*e\^{-t' "$TEX" | head -20
# Grep for log-polyhomogeneous class names / macros
grep -n '\\Csub\|log.poly\|logpoly\|log.*hom\|log.*ell' "$TEX" | head -20
```

**Manual check:** for every invocation of a theorem that requires classical ellipticity
(Seeley, Atiyah–Singer, etc.), verify that the operator in question:
1. Belongs to the *classical* symbol class $S^m_{\mathrm{cl}}$ (no log factors), OR
2. Has an explicit reduction step to a classical operator that actually works.

If the operator is only log-polyhomogeneous, cite an extension of the theorem that
covers that class (e.g., Lesch's log-polyhomogeneous Weyl law), or derive the needed
property (trace class, spectral counting) from first principles.

**Precedent (paper-B):** the trace class argument "$(H+C_0)$ is a positive classical
elliptic operator" for $H\in\mathcal{C}_{\mathrm{sub}}$ is incorrect; $H+C_0$ inherits
the log-polyhomogeneous terms from $H$.  The correct derivation uses the Weyl counting
bound $N_{\widetilde H}(\Lambda)=O(\Lambda^{d/m})$ to deduce $\sum e^{-t\lambda_k}<\infty$.

---

### P47 — Open problem sections must not contain problems already solved in the paper

An "open problem" or "open question" that is fully answered by a result proved earlier
in the same paper is a logical error: it signals to readers that something is unknown
when the paper has already resolved it.  This often happens when the open-problem
section is written independently of the main body, or when a theorem is strengthened
without updating the open questions.

```bash
# Grep for open-problem / conjecture / question sections
grep -n '\\section\|\\subsection' "$TEX" | grep -i 'open\|question\|conjecture\|problem\|further'

# For each open-problem item, extract the mathematical claim and compare with
# theorem statements in the body:
grep -n '\\begin{openproblem}\|\\begin{question}\|\\item.*open\|\\item.*whether' "$TEX" | head -20
```

**Manual check:** for each open-problem item:
1. State the core mathematical assertion the problem is asking about.
2. Search the paper's theorems, lemmas, and corollaries for any result that implies
   or directly answers the assertion.
3. If one exists, the item should be rewritten as a proposition (with the proof
   reference), and the truly open part (if any) stated separately.

Common triggers: injectivity / uniqueness questions answered by the same paper's
main theorems; convergence questions answered in the proof of the main theorem.

**Precedent (paper-A):** Open Problem 3 asked whether the Li-observation sequence
determines the multiset; the paper's own Theorem A + Newton-identity argument shows
$(\Li_j)_{j\ge 1}$ is injective on finite multisets.  The problem should become a
proposition, and the genuinely open part (noisy/bounded reconstruction) stated instead.

---

### P48 — Analytic extension at boundary points: removable singularities must be justified

When a function $f(T)$ is defined via $1/T$ (or $u = 1/T$) and a claim is made about
behavior as $T\to\infty$ (equivalently $u\to 0$), any assertion of analyticity or
uniform remainder in $\sigma$ at $u=0$ requires an explicit argument that:
1. the expression $f(\sigma + i/u) = g(\sigma, u)$ is well-defined at $u=0$
   (the apparent singularity at $T=\infty$ is removable), and
2. $g$ is jointly analytic (or jointly smooth) in $(\sigma, u)$ near $u=0$.

A bare "Taylor-expand $1/s$" argument omits step (1).

```bash
# Grep for 1/T substitutions and Taylor expansion near T -> infty
grep -n '1/T\|u=1/T\|T\to.*infty\|T\to\\infty\|as T\|T\to+\\infty' "$TEX" | head -20
# Grep for joint analyticity / uniform remainder claims
grep -n 'jointly.*anal\|uniform.*remainder\|uniform.*sigma\|uniformly.*sigma_0' "$TEX" | head -10
```

**Manual check:** for each asymptotic expansion in $1/T$:
- Write $u = 1/T$ and rewrite the expression as $g(\sigma, u)$.
- Verify $g$ is defined at $u=0$ (no $1/u$ poles surviving).
- Verify joint analyticity: typically by showing $g(\sigma, u) = h(\sigma u, u)$
  where $h$ is a power series with jointly convergent coefficients.

If not explicitly argued, add a one-sentence proof of the removable singularity
(e.g.\ "$\varphi_j(\sigma+i/u) = 1-(1-u/(i+\sigma u))^j$ extends to a polynomial in $u$
near $u=0$ uniformly in $\sigma\in[0,1]$, so $g$ is jointly analytic").

**Precedent (paper-A):** $\varphi_j(\sigma+iT) = 1-(1-(\sigma+iT)^{-1})^j$ is written
as a function of $T$ with $O_j(T^{-4})$ remainder, but the claim that the remainder
is uniform in $\sigma$ requires the substitution $u=1/T$ and verification that
$1-u/(i+\sigma u)$ is analytic at $u=0$ uniformly in $\sigma\in[0,1]$.

---

### P49 — Rational vs polynomial: verify the algebraic type of analytic functions

When a paper writes "is a polynomial in $u$" to justify that a function is analytic
at $u=0$, verify whether the expression is literally a polynomial (no denominator) or
a rational function that happens to be holomorphic at $u=0$.  The argument is correct
in either case — but stating "polynomial" for a rational function is a factual error
visible to specialists.

**Common pattern:** substituting $u=1/T$ in $\varphi(s_0+i/u)$ yields a rational
expression like $1-(1-u/(a+bu))^j$, which is rational (denominator $a+bu$), not a
polynomial.  The correct description is "rational in $u$, extending holomorphically
to $[0,1]\times\{0\}$" (since the denominator evaluates to $a\ne0$ at $u=0$).

```bash
# Grep for "polynomial in" near rational expressions
grep -n 'polynomial in\|polynomial.*of.*u\|power series in' "$TEX" | head -20
# Inspect each match: does the expression have a denominator depending on u?
```

**Manual check:** for each "polynomial in $u$" claim, substitute $u=0$ in the
denominator and verify it is nonzero.  If the expression has a nontrivial denominator,
replace "polynomial" with "rational function holomorphic at $u=0$" (or "extends
holomorphically to a complex neighbourhood of…").

**Precedent (paper-A):** $F_j(\sigma_0,u)=1-(1-u/(i+\sigma_0 u))^j$ is rational
with denominator $(i+\sigma_0 u)^j$; the correct description is "rational in $u$,
holomorphic on a neighbourhood of $[0,1]\times\{0\}$."

---

### P50 — Counting-function and spectral equalities: state the range of validity

Equalities of the form $N_H(\Lambda)=N_{\widetilde H}(\Lambda)$,
$N_H(\Lambda)=N_{H^{1/m}}(\Lambda^{1/m})$, or similar counting-function identities
arising from spectral manipulations (shifting the kernel, taking fractional powers)
hold only for $\Lambda$ above some threshold ($\Lambda\ge 1$, or $\Lambda > C$), not
for all $\Lambda\ge 0$.  Writing the equality without a domain qualifier is
technically false for small $\Lambda$.

```bash
# Flag counting-function equalities without a domain qualifier
grep -n 'N_H.*=\|N_{\\tilde\|N_{H\^{' "$TEX" | grep -v 'Lambda\\ge\|ge1\|ge 1\|sim\|to.*infty\|asymp' | head -20
```

**Manual check:** for each equality $A(\Lambda)=B(\Lambda)$:
1. Determine at what threshold value of $\Lambda$ the equality becomes exact.
2. Add "$\Lambda\ge C$" or "$\Lambda\ge 1$" (whichever applies) to the statement,
   or change to "$A(\Lambda)=B(\Lambda)+O(1)$" to make it valid for all $\Lambda$.

For Weyl-law purposes the $O(1)$ correction is harmless, but the missing qualifier is
a correctness gap for readers who apply the identity at small $\Lambda$.

**Precedent (paper-B):** after replacing $H$ by $\widetilde H=H+\Pi_{\ker H}$,
the identity $N_H(\Lambda)=N_{\widetilde H^{1/m}}(\Lambda^{1/m})$ holds for $\Lambda\ge 1$
(once the shifted eigenvalues reach $\Lambda=1$), not for all $\Lambda$.

---

### P51 — Unquantified bound variable in definition body

A definition body that uses a symbol like "the $N$th remainder" must bind $N$ with an
explicit quantifier ("for every $N\in\mathbb{N}_0$") before using it.  An unquantified
variable $N$ inside a definition is formally a free variable, making the membership
condition incompletely specified.  This is closely related to P30 (free variables in
theorems) but applies specifically to *definition bodies* and *class descriptions*.

```bash
# Find definition blocks containing "the Nth" or "N-th" without a preceding quantifier
sed -n '/\\begin{definition}/,/\\end{definition}/p' "$TEX" \
  | grep -n 'th remainder\|th order\|N\-th\|Nth\|the.*N\b' | head -20
# Also grep for implicit index variables in definitions
grep -n 'lies in\|belong.*to\|satisfies.*for each' "$TEX" \
  | awk -F: '$1>=(DEFSTART) && $1<=(DEFEND)' | head -10
```

**Manual check:** for each variable appearing in "the $N$th …" or "for $j\le N$" in
a definition body:
1. Is $N$ universally quantified ("for every $N\in\mathbb{N}_0$") before this clause?
2. If not, add the quantifier as the opening of the list item or the sentence.

Including $N=0$ in the quantifier is often important: it gives the base case
($\sigma(H)-h_m\in\bigcap_\varepsilon S^{m-1+\varepsilon}$) that is needed in downstream
form-boundedness proofs.

**Precedent (paper-B):** the $\mathcal{C}_{\mathrm{sub}}$ definition item (ii) wrote
"the $N$th remainder lies in…" without "for every $N\in\mathbb{N}_0$", making the
completeness of the asymptotic expansion formally unquantified.

---

### P52 — Preamble must include `\emergencystretch` and `\tolerance` settings

Long-form mathematics papers routinely contain inline expressions that exceed the text
width unless TeX is given extra line-breaking flexibility.  The default `\tolerance=200`
is appropriate for prose but not for symbol-heavy text; without
`\emergencystretch`, any long inline formula becomes a potential overfull hbox.

Recommended preamble additions (after `\usepackage` declarations):

```latex
%% Typesetting tolerance — prevents most minor overfull hboxes from inline math
\tolerance=1500
\emergencystretch=2em
```

`\tolerance=1500` allows slightly looser word spacing before TeX tries the next
pass; `\emergencystretch=2em` adds up to 2em of extra stretch per line in the
emergency pass.  Together they eliminate overfulls up to ~9pt without manual
intervention.

```bash
grep -n 'emergencystretch\|tolerance' "$TEX" | head -5
```

**Manual check:** if neither `\emergencystretch` nor `\tolerance` appears in the
preamble, add both.  If overfulls larger than 10pt persist after adding them,
those need manual restructuring (P54).

**Precedent (both papers):** adding `\tolerance=1500\emergencystretch=2em` eliminated
six out of eight overfull warnings in paper-A and all small overfulls in paper-B.

---

### P53 — `\begin{thebibliography}` must be wrapped in `{\sloppy ... }` or equivalent

Bibliography entries regularly produce underfull or overfull `\hbox` warnings from
long journal names, arXiv identifiers, DOI strings, and multi-word titles that TeX
cannot hyphenate.  Wrapping the bibliography in `{\sloppy\begin{thebibliography}...
\end{thebibliography}}` suppresses these warnings by relaxing the justification
constraint within the bibliography only.

```bash
# Check whether \sloppy (or \raggedright) precedes \begin{thebibliography}
grep -n 'sloppy\|raggedright' "$TEX" | grep -v '%'
grep -n '\\begin{thebibliography}' "$TEX"
```

**Manual check:** the `\sloppy` (or `{\sloppy ... }` group) must appear *before*
`\begin{thebibliography}`.  If using BibTeX/BibLaTeX, wrap the `\printbibliography`
call similarly.

**Precedent (both papers):** the Andersson arXiv entry and the CCM entry in paper-A
produced underfull hbox warnings (badness 3668 and 6300); wrapping the bibliography
in `{\sloppy ... }` resolved both.

---

### P54 — Long inline operator expressions must be displayed

Inline math containing `\operatorname{foo}(\text{...}, \beta_1,\ldots,\beta_m)` or
similar compound expressions (operator name + text argument + subscripted parameters)
almost always exceeds the line width and produces large overfull hboxes (>10pt) that
`\emergencystretch` alone cannot fix.  These must be moved to a displayed equation.

Common culprits:
- `$R = \operatorname{lcm}(\text{denominators of }\beta_1,\ldots,\beta_m) \ge 1$`
- `$\sigma(H)\colon H^{s_1}(M) \to H^{s_2}(M)$ with $s_1-s_2=m$`
- Long Sobolev mapping: `$Q_0\colon H^{(m-1+\varepsilon)/2}(M)\to H^{-(m-1+\varepsilon)/2}(M)$`

```bash
# Grep for long inline operatorname or Sobolev norm patterns
grep -n '\\operatorname{.*}(\\text\|\\operatorname.*ldots\|H\^{.*varepsilon' "$TEX" | head -20
# Also check for inline \colon mappings between Sobolev spaces
grep -n '\\colon H\^{' "$TEX" | head -10
```

**Manual check:** for each match, estimate the rendered width.  If the expression
contains a text argument (`\text{...}`) inside `\operatorname{...}(...)`, or a
Sobolev mapping with fractional exponents, replace with prose + display:

Instead of:
```latex
Let $R = \operatorname{lcm}(\text{denominators of }\beta_1,\ldots,\beta_m)\ge 1$.
```
Write:
```latex
Let $R\ge 1$ be the least common multiple of the denominators of $\beta_1,\ldots,\beta_m$.
```
or display the definition.

**Precedent (paper-A):** `\operatorname{lcm}(\text{denominators of }\beta_1,\ldots,\beta_m)`
caused a 15.17pt overfull; rewriting as prose eliminated it.

---

## Running order for pre-submission

### Phase 0 — Compilation gate (must pass before any manual review)
1. `pdflatex` three passes → fix errors and undefined-ref warnings (P4)
2. Hardcoded refs → internal `\ref` or external citation check (P1)
3. Unused bibliography → cite or remove (P3)
4. **Preamble inventory** — extract all `\newtheorem` and `\newcommand` names; keep
   the list open for use in P30, P34, P35, P7, P28

### Phase 1 — Per-theorem structural audit (run for each theorem/lemma/corollary)
5. Hypothesis shadow test (S1) — write the table
6. Definition domain coverage table (S2) — write the table
7. Citation full instantiation record (S3) — write one line per proof citation
8. Parameter boundary sweep (S4) — evaluate formula at each domain boundary
9. Normalization source check (S5) — open source, compare verbatim

### Phase 2 — Automated symptom sweeps
10. Unused labels → add `\ref` or remove (P2)
11. Short title check (P5)
12. Unused results (P6)
13. Definition consistency grep for each key term, **including macro names** (P7)
14. Restatement lemma attribution grep (P8)
15. Asymptotics grep → point to verifying scripts (P9)
16. Informal qualifiers grep (P10)
17. Remark formula audit (P11)
18. Parity arguments to sufficient order (P19)
19. Strong analytic/number-theoretic assertions (P20)
20. Analogy refutation check (P21)
21. **Open problem/question section variable binding (P39)**

### Phase 3 — Definition and citation rigor
22. External theorem parameter instantiation (P22)
23. **Statement-proof domain mismatch (P33)** — upgrade statement if proof is stronger
24. Operator definition prerequisite ordering (P23)
25. **Spectral definition domain vs usage (P34)** — search definition blocks + macro names
26. Literature formula descriptions vs source (P25)
27. Optional theorem title duplication (P24)
28. Reference operator symbol class (P26)
29. **Parameterized class superscripts re-quantified (P35)** — use macro names from preamble inventory
30. **Existence vs construction citation qualifier (P36)** — flag bare "By Theorem" in proofs
31. Tauberian theorems used bidirectionally (P27)
32. Single-letter symbol conflicts (P28)
33. `\texorpdfstring` bookmark semantic correctness (P29)
34. **Free variable binding in all theorem environments (P30)** — include custom `\newtheorem` names
35. "Same argument" conclusion completeness (P31)
36. Canonical realization identification after definition (P32)
37. **Degenerate-parameter case convention (P37)**
38. **Self-adjointness inner product named (P38)**

### Phase 4 — Scope and methodology
39. No-go theorem completeness (P12)
40. No equivalence claimed as impossibility (P13)
41. Abstract/intro scope claims (P14)
42. Analogies labeled motivational (P15)
43. Evidence level for imported premises (P16)
44. Invariance under method class transformations (P17)
45. Constructive/existential qualifier consistency (P18)

### Phase 5 — Quantification, reproducibility, and operator hygiene
46. **Uniform vs pointwise index quantification (P40)** — grep `O(` near summation index
47. **Author count in possessive references (P41)** — grep "the author" near `\cite`
48. **Checker/script files referenced must exist (P42)** — grep paths, then `[ -f ]`
49. **Trace class hypothesis for heat semigroup (P43)** — flag lower-semibounded + `Z_H` without trace class statement
50. **Homogeneous vs truncated principal symbol (P44)** — grep `\chi` near Weyl constant integral
51. **No forward `\ref` inside `\begin{definition}` (P45)** — grep `\ref`/`\eqref` in definition blocks

### Phase 6 — Operator class precision and open problem hygiene
52. **Classical vs log-polyhomogeneous class check (P46)** — grep `Seeley` / classical citations near log-poly class usage
53. **Open problems not already solved in paper (P47)** — extract open-problem claims, cross-check theorem list
54. **Removable singularity / joint analyticity at boundary points (P48)** — grep `1/T` or `u=1/T` substitutions; verify $g(\sigma,0)$ defined

### Phase 7 — Algebraic precision and definition completeness
55. **Rational vs polynomial: verify algebraic type of analytic functions (P49)** — grep "polynomial in" near rational/analytic expressions
56. **Counting-function / asymptotic equality domain qualifier (P50)** — grep `N_H\|N_{\|counting function` near `=` without `\Lambda\ge` or `\to\infty`
57. **Unquantified bound variable in definition body (P51)** — grep `\begin{definition}` blocks for free variables (index N, parameter k) without "for every" or "for all" quantifier

### Phase 8 — Typesetting hygiene
58. **Preamble `\emergencystretch` and `\tolerance` (P52)** — grep preamble for these settings
59. **Bibliography wrapped in `{\sloppy}` (P53)** — grep for `\sloppy` before `\begin{thebibliography}`
60. **Long inline operator expressions displayed (P54)** — grep `\operatorname.*\text` and long `\colon H^{` mappings

---

## Notes for project-specific adaptations

When adopting this file for a new project:

1. **P7:** replace the example grep pattern with the key defined terms in your project.
2. **P9:** point to your project's `checker/` or equivalent directory.
3. **P12:** the five components are general; the names "method class / ambient class /
   observation map / target predicate / escape route" may be adapted to your domain's
   terminology.
4. **P16:** the two-axis evidence taxonomy is general; if your project uses a different
   evidence-tracking system, map its levels onto the two axes.
5. **P17:** the specific transforms to check (rescaling, congruence, preconditioning)
   depend on the method class; name them explicitly for your domain.
6. **S2:** the "common coverage failures" list should be extended with domain-specific
   tools (e.g. specific cited theorems that have restricted domains in your field).
7. **S5:** the "common normalization traps" list should be extended with the specific
   pairs of look-alike results in your reference literature.

Remove or rename `Precedent (paper-A/B):` lines when the precedent is not meaningful
outside this project.  The rules themselves remain valid.
