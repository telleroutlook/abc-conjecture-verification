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
correct statement is: rad(N_E) | rad(2abc), and log N_E ≤ 2 log rad(abc) + 8 log 2
(for Frey curves). Any stronger divisibility claim must be verified. Reference failure:
for (a,b,c)=(1,8,9) the Frey curve has conductor N=48; rad(abc)²=36 and 48 ∤ 36, so
"N_E | rad(abc)²" and "N_E ≤ rad(abc)²" are both false for this example.
grep: `N_E.*=.*rad`, `N_E.*≤.*rad`, `conductor.*=.*rad`, `N\(E\).*rad`.

---

*Add new checks here as referees return findings. Each check is a command or derivation
you actually run — not a prose observation.*
