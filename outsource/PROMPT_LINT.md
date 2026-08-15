# outsource/PROMPT_LINT.md — standing adversarial checklist for abc outsource prompts

Every recurring defect a referee finds should be listed here as a **check that must
actually be RUN** — a script, a `grep`, or an explicit derivation — never a prose
"looks fine". Run **all applicable** checks on every new or edited prompt before it
ships.

**Re-scan rule (load-bearing).** When a referee surfaces a new defect class: (1) add it
here, (2) re-scan every active prompt AND every relevant `proof/*/` file for the same
error. A defect is never assumed independent.

---

## A1 — K_ε not fitted from known abc triples

CHECK: does the construction read or sample known high-quality abc triples to derive K_ε
or any parameter? If so, it is circular and fails CORE-1 (spec §3.3, forbidden leaf B2).
grep: `rad(abc)`, `best known`, `high-quality triple`, `example triple`, `fit`.

## A2 — Universal scope of the key inequality

The key inequality c ≤ K_ε · rad(abc)^{1+ε} must cover **all** coprime a+b=c.
CHECK: is it proved only for a fixed finite prime set S, for a specific family, or for
"sufficiently large" instances? If so, the scope is insufficient for CORE-3.
grep: `for all primes in S`, `for sufficiently large`, `for this family`, `restricted to`.

## A3 — IUT identification-without-isomorphism

If the proof uses Mochizuki's IUT: CHECK that every step that identifies objects across
Hodge theaters provides an explicit isomorphism proof — not just a claim that the
objects "are the same". This is the Scholze–Stix objection.
grep: `identified with`, `can be identified`, `across theaters`, `same object`.

## A4 — Szpiro or abc-equivalent assumed

CHECK: does the proof assume Szpiro's conjecture, the effective Mordell conjecture, or
any statement directly equivalent to abc? These are forbidden construction leaves.
grep: `Szpiro`, `effective Mordell`, `abc conjecture`, `assuming abc`.

## A5 — Non-anticipation: construction sees comparison

CHECK: do construction modules M1/M2/M3 import or read analytic rank, abc examples
(used for verification, not just exploration), or the Szpiro comparison?
grep (in M1/M2/M3 Python): `from proof.m4`, `from proof.m5`, `from proof.m6`.

## A6 — Finiteness asserted, not derived

CHECK: is the finiteness of exceptions derived from the inequality, or just asserted?
The certificate requires an explicit derivation (spec §2.1, CL-11 is [OBL]).
grep: `it is well-known that there are finitely`, `finiteness follows`, `trivially finite`.

## A7 — Claim not self-contained

CHECK: does the prompt say "see spec §X" or reference another file instead of repeating
the definition inline? Every symbol and formula must appear in the prompt itself.
grep: `see spec`, `as defined in`, `from CLAUDE.md`, `as above`.

## A8 — IUT object type mismatch

When a prompt models IUT structures, verify that each mathematical object has the correct
type as defined in the cited source. Specifically: the Θ-link (IUTT-III Definition 3.8)
is a **full poly-isomorphism of prime-strips**, NOT a function-field morphism φ_F: F₁→F₂.
No formula for φ_F on generators can be requested if the cited definition does not
construct such a morphism — that is a category error, not an open sub-problem.
grep: `φ_F`, `function field morphism`, `morphism φ_F:`, `F_1 → F_2`, `induced morphism on F`.

## A9 — Theorem verbatim check

Every theorem/corollary cited from IUT must be stated exactly as written in its published
source — paraphrasing into a different claim is a reject. Concretely: IUTT-III Corollary
3.12 ("Log-volume Estimates for Θ-Pilot Objects") states −|log Θ| ≥ −|log q|, NOT a
discriminant-conductor bound log|Δ| ≤ (1+ε)log N + C. Run:
`grep -n 'Corollary 3.12' outsource/<file>.md` and verify the stated content against the
source PDF (IUTT-III §3.12 title and statement).
grep: `Corollary 3.12`, `Cor. 3.12`, `log.*Delta.*log.*N`, `discriminant.*conductor.*inequality`.

## A10 — Numerical anchor script self-consistency

Run every inline Python snippet in the prompt and confirm stdout matches the stated
expected output exactly. A mismatch is a reject. Reference failure: OB-02 stated
`2*log(N)=7.1595` but the command had `N=6`, which outputs `2*log(N)=3.5835`.
Run: `python3 -c "<paste snippet>"` and compare against stated expected output character
for character (modulo trailing whitespace).

## A11 — Conductor vs radical conflation

The conductor N(E) of an elliptic curve is NOT equal to rad(abc) or rad(abc)². The
correct statement is: rad(N_E) | rad(2abc), and log N_E ≤ log rad(abc) + 7 log 2
(for Frey curves, a-odd/b-even subfamily). Any stronger divisibility claim must be
verified. Reference failure: for (a,b,c)=(1,8,9) the Frey curve has conductor N=48;
rad(abc)²=36 and 48 ∤ 36, so "N_E | rad(abc)²" and "N_E ≤ rad(abc)²" are both false.
grep: `N_E.*=.*rad`, `N_E.*≤.*rad`, `conductor.*=.*rad`, `N\(E\).*rad`,
      `N_E.*rad(2abc)`, `divides.*rad(2`, `delta.*divides.*rad`.
Verify: for the numerical anchor triple, check N_E ≤ 2⁷ · R manually.

## A12 — Minkowski in a hyperplane requires Vaaler (1979)

When applying Minkowski's theorem to bound coordinates of the shortest lattice vector
in a rank-r sublattice L ⊂ ℤⁿ that sits inside a hyperplane of ℝⁿ (n > r):
Minkowski's theorem alone bounds coordinates in *some* orthonormal basis of the ambient
subspace, NOT the ambient ℤⁿ coordinates. Recovering ‖v‖_∞ ≤ det(L)^{1/r} in the
ambient ℤⁿ coordinates additionally requires **Vaaler's theorem (1979)**:
every central hyperplane section of [−1,1]^n has (n−1)-volume ≥ 2^{n−1}.

CHECK: if a prompt uses Minkowski's theorem to bound ‖ψ‖_∞ for ψ ∈ L ⊂ ℤ^P where
L is defined by a single linear constraint (the Pasten lattice setup), verify the
citation is "Minkowski + Vaaler (1979)", not "Minkowski alone."
Source failure: OB-09 Corollary C stated "Minkowski gives ‖ψ‖_∞ ≤ det(L)^{1/(ω−1)}"
— correct conclusion but incomplete citation; Vaaler (1979) is required.
Reference: Vaaler, J.D. "A geometric inequality with applications to linear forms."
Pacific J. Math. 83 (1979), no. 2, 543–553.
grep (in any outsource or proof file using Minkowski): `Minkowski.*‖ψ‖`, `Minkowski.*ambient`,
     `geometry of numbers.*bound`, `shortest vector.*det`.

## A12 — Discriminant height vs Faltings height conflation

`(1/12) log|Δ_min(E)|` is the *discriminant height* h_Δ, NOT the Faltings height h_F.
The Faltings height also contains a complex-period / modular-form Archimedean term whose
difference from h_Δ is NOT uniformly bounded by a constant independent of the curve
(Löbrich, JTNB 29 (2017), Proposition 3.1). Any prompt that labels `(1/12)log|Δ_min|`
as "Faltings height" or writes `h_F ≈ (1/12)log|Δ_min|` and treats the O(1) as
universally bounded must be corrected. Reference failure: OB-01 and OB-03 both wrote
this equation, leading the referee to flag the citation of Silverman AT as wrong.
grep: `h_F.*1/12.*log`, `Faltings.*1/12`, `naive.*Faltings`, `approximately.*Faltings`,
      `h_F.*≈.*log.*Delta`, `h_F.*=.*log.*Delta`.

## A13 — Discriminant upper bound in log c (not log(abc))

The bound `log|Δ_min(E_{a,b,c})| ≤ 2 log c + C` for a UNIFORM constant C is FALSE.
The correct upper bound is `2 log(abc) + 4 log 2`. When a,b are both large, log(abc)
far exceeds log c. The family (a,b,c)=(1,2n,2n+1) gives log|Δ_min| ≥ 2 log(2n(2n+1))
+ O(1) while 2 log c = 2 log(2n+1), and the gap is unbounded.
CHECK: if a prompt states an upper bound `log|Δ_min| ≤ f(c) + C` with f depending only
on c (not abc), verify this is mathematically correct before shipping. In general the
correct form has log(abc) on the RHS.
grep: `log.*Delta.*≤.*2.*log c`, `≤.*2 log(c)`, `upper.*log c`, `2 log c.*C`.

## A14 — Vacuous quantifier (ε not in conclusion)

If a claim reads `∀ε>0 ∃(something): P(object, ε_free)` where ε does not appear in P,
then the ε is vacuous and the claim is just `∃(something): P(object)`. Two failure modes:
(1) OB-01 style: `h_F ≤ C_ε·(1+ε)·log R` — since C_ε is unconstrained, absorbing (1+ε)
into C_ε makes ε vacuous; this claim is only O(log R), NOT standard abc.
(2) OB-03-D style: `∀ε>0 ∃ triple: q > 1` — ε is absent from the predicate q>1.
CHECK: for every `∀ε>0` quantifier in a claim, confirm ε appears in the conclusion
predicate with a *fixed* leading coefficient (not hidden inside an unconstrained constant).
grep: `forall.*eps.*exists`, `C_\varepsilon.*(1.*varepsilon)`, `∀ε.*∃.*C_`,
      `C_eps.*1.*eps`, `\(1\+\\varepsilon\).*C_`.

## A15 — Parity coverage completeness

If a construction says "assume a odd, b even — possible by permuting a,b", verify this
covers ALL coprime triples. It does NOT: if both a and b are odd (e.g. (1,1,2), (1,3,4)),
permuting still leaves both odd. The claim must either:
(a) explicitly restrict to the a-odd/b-even subfamily, OR
(b) handle the both-odd case separately.
Reference failure: OB-03 wrote "a odd, b even (possible by permuting a,b)" without
qualifying the scope. The both-odd family is a strictly different case.
grep: `permuting a.*b`, `WLOG.*b even`, `odd.*even.*permut`, `by symmetry.*even`,
      `possible by permuting`, `renaming`.

## A10 addendum — Prose numerical computations also require verification

A10 (numerical anchor script self-consistency) only triggers on inline Python snippets.
Any PROSE numerical computation (e.g., "quality = log c / log rad(abc) ≈ X") must also
be verified by hand or by a quick script. Reference failure: OB-03 Step 4 wrote
"quality log 9 / log 72 ≈ 0.514" — the denominator should be log rad(72) = log 6,
not log 72; the correct value is log 9 / log 6 ≈ 1.226.
CHECK: for every "≈" or "=" followed by a floating-point value in any proof step, run
`python3 -c "import math; print(math.log(9)/math.log(6))"` (or equivalent) to confirm.

---

*Add new checks here as referees return findings. Each check is a command or derivation
you actually run — not a prose observation.*
