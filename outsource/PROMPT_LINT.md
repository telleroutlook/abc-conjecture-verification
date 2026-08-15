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

---

*Add new checks here as referees return findings. Each check is a command or derivation
you actually run — not a prose observation.*
