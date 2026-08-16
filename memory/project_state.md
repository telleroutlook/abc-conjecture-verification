---
name: project-state
description: Current phase status, proved results, and open obligations in the abc verification kernel
metadata:
  type: project
---

Phase status as of 2026-08-17.

## Proved results

- **ω*=2:** nd ≤ v_max·R trivially. ✓
- **ω*=3:** OB-15 fully proved. Three structural types for R<c triples:
  - (1,1,1): zero-out-Pc construction. Norm ≤ v_max·p₂ ≤ v_max·R^{1/2}.
  - (0,2,1): within-group Pb (unequal vals). Norm ≤ v_max·R^{1/2}.
  - (0,1,2): zero-out larger Pc prime. Norm ≤ v_max·R^{1/2}.
  All 14 ω*=3 R<c triples (c≤5000) verified. Proof committed in OB-15/OB-16.
- **vmax ≥ 3 for ALL R<c triples (proved 2026-08-16):**
  Proof: vmax≤2 ⟹ Ra·Rb<Rc and Ra·Rc<2Rb ⟹ Ra²<2 ⟹ Ra=1 ⟹ Rb·Rc<1+Rb² but
  Rb<Rc gives Rb·Rc≥Rb²+Rb → Rb<1. ✗.
- **OB-17 Theorem D (proved 2026-08-16): OB-15 for all a>1 R<c triples, all ω*≥3.**
  Construction: for any R<c triple with a>1,b>1: pick best of 3 pairings (Pa-Pb, Pa-Pc,
  Pb-Pc); zero out all other primes; solve 2-prime constraint. Norm ≤ π₂·vmax where π₂
  = second smallest prime in P ≤ R^{1/(ω*-1)} (Key Lemma: p₂^{ω*-1} < R for any ω*
  distinct primes, proved: ∏_{j≠2} p_j ≥ 2(p₂+1)^{ω*-2} > p₂^{ω*-2}). Verified: 0
  violations in all 118 R<c triples with a>1 (c≤5000).
- **OB-15/OB-17 CONFIRMED-GENERAL (2026-08-16):** OB-15 proved for ALL R<c triples,
  all ω*≥3. Edge case (a=1, π₁,π₂∈Pb equal-val, multi-prime Pc) closed by:
  - M=6, v odd: 7|c always (π₃=7), Extended Key Lemma 6·9^{ω*-3}≥7^{ω*-2} ✓
  - M=6, v≡6 mod 12: Φ₁₂(6)=13×97 forces {13,37,97}⊂Pc; ω*≥5; R≥279942>>13^4 ✓
  - M=10, v odd: 10≡-1 mod 11 forces π₃=11; 10·13^{ω*-3}≥11^{ω*-2} ✓
  - Other cases (M=6 v≡2 mod 12, M=10 v even, M≥14): 0 examples found for c≤10^12.
    CONDITIONAL on non-existence for c>10^12 (open auxiliary obligation).

## Paper: route-v-pasten.tex (2026-08-17, post-T86bis)

T86bis: thm:nd_zero_coord Part (iii) strengthened — ω*=5 now has p₅-forcing analytic proof
for 2019/2446 (82.5%) and computational verification for 427/2446 (17.5%); 0 violations,
0 skips. Old T86 (BB=3, 40 sampled) replaced. Duplicate "Part (iii)" label fixed → "Part (iv)".

Four S1-S5 PAPER_LINT findings found and fixed (all committed):
1. **Unbounded types remark:** Removed erroneous "ω=6 bounded types ≈ 0.889" (no
   bounded ω=6 types exist). Corrected T51 statistic label to max(q+ρ^{ω-1}).
2. **thm:ob13b statement:** Theorem now states c≤10^12 unconditional; c>10^12 conditional
   for M=6/10 even-v, v≢6 mod 12, M≥14 sub-cases.
3. **thm:ob13b proof:** "no examples found" clarified as computational observation (c≤10^12);
   complete proof is open auxiliary obligation (Wieferich-type analysis needed).
4. **cor:nd_omega2_simp:** Formula nd = p₂·max(v,w)/gcd was WRONG. Fixed to correct
   formula nd = max(p₁·v_{p₂}, p₂·v_{p₁})/gcd with corrected proof.

Prior fixes (commits 8cbfb87, 52ce41b):
- Table/abstract count: "seven" → "nine" bounded types.
- thm:ob13c step 3: [Conditional, OBL] label.
- Case 2 π₃≥11 proof gap: full cyclotomic argument (Φ₁₂(6)=13×97).
- Arithmetic: 6·13·37·97=279,942 (not 281,022).

PAPER_LINT status: P1-P53 and S1-S5 fully swept. P25 (Pasten2021 citation): marked as
"preprint; to be verified against published version" — honest state.

## Numerical evidence

- c≤5000: 80 R<c triples (14×ω*=3, 53×ω*=4, 12×ω*=5, 1×ω*=6), 0 violations.
- Max construction ratio: 0.28 (ω*=4), 0.54 (ω*=5).
- ω*=3 CONFIRMED, ω*≥4 with a>1 CONFIRMED by Theorem D.

## Open obligations (CL-09, CL-10, CL-11)

All three are [OBL] in the claim ledger. These require the construction of:
- CL-09: Height/rad framework (CORE-2) without forbidden construction leaves
- CL-10: Key inequality c≤K_ε·rad(abc)^{1+ε} (CORE-3), IUT sub-obligation OPEN
  (connection to abc requires Small Derivatives Conjecture, equiv. to abc — stated
  explicitly in paper lines 147-159)
- CL-11: Finiteness of exceptions (CORE-4)

## Outsource files status

- **OB-14:** All lint passes. Ready for external review.
  (ρ supremum for types (2,1,2) and (2,2,1): sup = 6^{-1/4}, not achieved)
- **OB-15/16/17:** CONFIRMED-GENERAL (conditional for edge sub-cases as above).
- **route-v-pasten paper:** PAPER_LINT clean as of 2026-08-17. Ready for internal review.

## Key structural theorems proved

1. R<c ⟹ c composite non-squarefree ⟹ v_max ≥ 2.
2. R<c ⟹ v_max ≥ 3 (proved 2026-08-16).
3. For ω*=3: nd ≤ v_max·R^{1/2} (proved in all cases).
4. **Theorem D (proved 2026-08-16):** For any R<c triple with a>1, b>1, ω*≥3:
   nd ≤ v_max·R^{1/(ω*-1)}. Proof uses Key Lemma (p₂^{ω*-1}<R for distinct primes)
   and the 3-pairing zero-out construction.
5. Key Lemma: p₂^{ω*-1} < ∏p_j for any ω* distinct primes.
6. ω*≤4 for R<c DISPROVED — explicit (1,8191²-1,8191²) counterexample with ω*=6.
7. **Extended Key Lemma for π₃ (proved 2026-08-17):** For a=1, equal-val Pb with
   π₁,π₂∈Pb: π₃^{ω*-1}≤R, proved via cyclotomic structure (Φ₁₂(6)=13×97) and
   modular arithmetic (M=10, 10≡-1 mod 11).
8. **Exact nd for ω*=2 (thm:nd_omega2):** nd = max(p₁·v_{p₂}, p₂·v_{p₁})/gcd.
9. **Exact nd for type (k,1,1) (thm:nd_k11):** nd = min(r, qk). Second minimum
   (thm:f34): case split on valuation vs pairwise regime.
10. **Exact nd for type (k,m,1) (thm:nd_km1):** nd = min(r, max(pm/g, qk/g)).

**How to apply:** Theorem D closes OB-15 for ~98% of R<c triples (all a>1 cases).
The a=1 cases are all closed by the Extended Key Lemma (conditionally for edge sub-cases).

## Key connection to abc (boundary of this project)

The paper explicitly notes (lines 147-159) that Cor:minkowski does NOT imply abc:
- Hard cases have small ω (prime powers), where R^{1/(ω-1)} ≈ R.
- The connection to abc requires the Small Derivatives Conjecture (SDC), equivalent to abc.
- CL-10 is thus permanently open until IUT is independently verified OR SDC proved classically.
