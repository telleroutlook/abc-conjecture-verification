# OB-07 Independent Referee Report — Baker Methods and Fixed-Power Quality Bounds

**Review target:** `OB-07-baker-methods-quality-bound.md`  
**Review date:** 2026-08-15  
**Nature:** Analytic number theory audit. No abc conjecture, Szpiro, IUT Corollary 3.12,
known abc triples as analytic input, or fitted parameter K_ε is assumed.

---

## Formal verdict

> **INCONCLUSIVE + LOCALIZATION**

Baker-type (linear-forms-in-logarithms) methods, as currently developed, cannot give a
fixed-power bound c ≤ K₀·R^A for any fixed A. The obstruction is the circular dependence
B ~ c in the S-unit equation proof, which produces a factor exp(C·log c) rather than a
polynomial in R. Pasten (2024, Inventiones) improves the sub-exponential exponent from
R^{1/3}(log R)^3 by a log log R factor but does not reach polynomial bounds. Whether the
R^{1/3} exponent is a true barrier for linear-forms methods or an artifact of current
technique is an open question; the precise localization is given in Step 2 below.

---

## Numerical anchor verification

```
R = 6
Stewart-Yu bound (kappa=1, illustration): c < 34633.1   ✓ matches expected
Fixed-power bound (A=2, K0=1, example):  c <= 36        ✓
Actual c = 9                                             ✓
Quality q = log(9)/log(6) = 1.226294                    ✓
Gap factor (Stewart-Yu / fixed-power): 962.0x           ✓
```

All outputs match. The 962× gap for (1, 8, 9) illustrates the scale of improvement
needed; this example is a sanity check only and is not input to any proof.

---

## Step 1 — Stewart–Yu bound: tracing the R^{1/3} exponent

**Source:** C. L. Stewart and Kunrui Yu, "On the abc conjecture, II,"
Duke Math. J. 108 (2001), no. 1, 169–181, Theorem 1.

**Theorem 1 (Stewart–Yu 2001):** For all coprime positive integers (a, b, c) with a + b = c:

    c < exp(κ · R^{1/3} · (log R)^3)

for an effectively computable constant κ > 0, where R = rad(abc).

**Derivation of R^{1/3}:**

Given a + b = c with gcd(a, b) = 1, divide by c to get (a/c) + (b/c) = 1.
Both a/c and b/c are S-units for the set S of primes dividing abc (which has |S| = ω(abc)
prime factors, where ω(n) denotes the number of distinct prime divisors of n).

**The linear form:** Apply Baker's theorem to

    Λ = log(a/c) = log a − log c

(or equivalently to the unit equation relation). The linear form in logarithms is:

    Λ = Σ_{p | abc} v_p(a/c) · log p

where v_p denotes the p-adic valuation. The coefficients b_i = v_p(a/c) satisfy

    |b_i| = |v_p(a/c)| ≤ v_p(a) + v_p(c) ≤ log c / log p

so the maximum coefficient is bounded by B ≤ log c (roughly).

**Baker's theorem gives:**

    log|Λ| > −C(|S|, deg) · (log B + 1) · Π_{p ∈ S} log p

where C(|S|, deg) is effectively computable, B ~ log c, and Π_{p ∈ S} log p = log R.
Hence:

    log|Λ| > −C · log c · log R

Since Λ ≠ 0 (otherwise a/c would be a root of unity, contradicting a + b = c with a, b, c
positive integers except for finitely many cases), we get:

    |a/c| ~ |Λ|  ⟹  log c ≲ C · log c · log R  (this is not immediately useful)

**Stewart–Yu's key refinement:** Rather than applying Baker directly to all primes in S,
Stewart and Yu choose a prime p* ∈ S with p* ~ R^{1/3} (such a prime exists by prime
distribution in R = rad(abc) when |S| is of the appropriate size). They apply Baker to
a linear form involving only the primes near p*, which gives a bound where the effective
constant absorbs a factor of R^{1/3}. The three-fold argument (symmetrizing among the
three terms a, b, c and choosing the most favorable prime) yields the R^{1/3} factor
in the exponent rather than R itself.

**Where R^{1/3} enters:** In the Stewart–Yu proof, after the prime-selection argument,
the effective Baker bound on the relevant linear form gives:

    c < exp(κ · p* · (log p*)^3)   with p* ~ R^{1/3}

which produces c < exp(κ · R^{1/3} · (log R^{1/3})^3) = exp(κ' · R^{1/3} · (log R)^3).

**B in terms of R:** The max coefficient B in the linear form satisfies:
- In the direct Baker application: B ~ c, NOT B ~ R.
- Since c can satisfy q(a, b, c) > 1, we have c > R, so B ~ c > R.
- To get a polynomial bound c < R^A, one would need B ~ R^O(1), but B ~ c is circular.

---

## Step 2 — Gap analysis: from exp(R^{1/3}) to R^A

**Key circularity:** To prove c < R^A from a Baker-type argument, one needs:

    log c < A · log R

But Baker's bound, applied to the S-unit equation a + b = c, yields:

    log c ≲ C · B · (log R)^k    for some constants C, k

where B ~ log c (or B ~ c in the direct application). Substituting B ~ log c gives:

    log c ≲ C · log c · (log R)^k

which, when solving for c, gives a sub-exponential bound (as in Stewart–Yu) but NOT
a polynomial bound, because the (log R)^k factor does not absorb the log c on the
right side to give log c ≲ A · log R.

**Formal statement of the circularity:** Define f(c, R) = B (the max coefficient).
In the S-unit equation proof, f(c, R) ≥ C₁ · log c for some constant C₁ > 0
(this follows from the fact that at least one prime p | abc satisfies v_p(a) ≥ log c / (2 log R),
which forces b_i ≥ log c / (2 log R) ~ log c / log R). Then Baker gives:

    log c ≲ C₂ · f(c, R) · log R ≲ C₂ · (log c / log R) · log R = C₂ · log c

This is circular: the bound is trivially satisfied for any c, providing no useful information.
The polynomial bound fails precisely here.

**Is R^{1/3} tight for linear-forms methods?**
This is an open question. There is no theorem in the literature showing that Baker-type
methods provably CANNOT give c ≤ K₀·R^A (a lower bound on what these methods can achieve
would require a matching lower bound construction, which does not exist). The R^{1/3}
exponent is the best current UPPER BOUND from these methods; whether it is a BARRIER
is unknown.

**What would break the R^{1/3} barrier:** To improve from R^{1/3} to R^δ for δ < 1/3,
one would need either:
(a) A Baker-type bound where the effective constant C(n, d) has better dependence on |S|,
    reducing the contribution from the prime selection; or
(b) A way to bound B ~ log c by O(R^ε) for any ε > 0, which is equivalent to bounding
    the quality q(a, b, c) by O(1) — precisely the abc conjecture.
    This makes (b) circular as a strategy.

---

## Step 3 — Pasten 2024: improvement toward polynomial bounds?

**Source:** Héctor Pasten, "The largest prime factor of n²+1 and improvements on
subexponential ABC," Inventiones Mathematicae 236 (2024), 373–385.
DOI: 10.1007/s00222-024-01244-6. arXiv: 2312.03566.

**Theorem 1.4 and bound (1.7) of Pasten (2024):**

Pasten uses Shimura curves (CM points on Shimura curves associated to quaternion algebras)
to improve the sub-exponential bound. His main unconditional result (bound (1.7)) is:

    c < exp(κ · R^{1/3} · (log R)^3 / (log log R))

i.e., an improvement over Stewart–Yu by a factor of 1/(log log R) in the exponent,
for all coprime triples (a, b, c) with c sufficiently large.

**Answers to OB-07 sub-questions:**

(a) **Does Pasten 2024 give δ < 1/3 unconditionally?**
    **NO.** The R^{1/3} exponent is unchanged. The improvement is a log log R factor in
    the denominator of the exponent, not a reduction of the 1/3 power. The bound is still
    super-polynomial in R for any fixed polynomial R^A.

(b) **Does it require additional conditions on abc?**
    The main bound (1.7) applies to ALL coprime triples (unconditionally). However,
    Theorem 1.4 itself concerns n² + 1 and the largest prime factor; the ABC application
    is a consequence. No restriction on which primes divide abc is required for (1.7).

(c) **Does it give polynomial bounds for any subfamily?**
    Not explicitly. The improvement is uniform across all triples; there is no subfamily
    result giving c < R^A for a polynomial family, conditional or unconditional.

**Is (1.7) the best unconditional bound for arbitrary triples?**
As of the OB-07 problem date (2026-08-15), Pasten's bound (1.7) is the best published
unconditional bound for all coprime triples. The improvement is genuinely new (the
log log factor), but the fundamental exponential form c < exp(f(R)) with f(R) → ∞
faster than any polynomial remains unchanged.

---

## Step 4 — Precise gap statement

**Best currently provable unconditional bound (all coprime triples):**

    c < exp(κ · R^{1/3} · (log R)^3 / (log log R))        [Pasten 2024, bound (1.7)]

where κ > 0 is effectively computable.

**Target fixed-power weak abc:** There exist K₀, A > 0 (universal) such that c ≤ K₀·R^A
for all coprime triples. The conjectured exponent A = 1 corresponds to the standard abc
conjecture; any fixed A > 0 gives the weaker form.

**Precise gap:** The gap between the best proven bound and fixed-power weak abc is the
gap between sub-exponential (c < exp(R^{1/3+o(1)})) and polynomial (c < R^A) growth rates.
For any fixed A, the ratio exp(R^{1/3}(log R)^3) / R^A = exp(R^{1/3}(log R)^3 − A log R)
grows without bound as R → ∞. The two bounds are not separated by a finite factor.

**Classification of the gap:**

| Question | Status |
|---|---|
| Is there a theorem showing Baker methods provably cannot give c ≤ K₀·R^A? | **Open.** No impossibility theorem exists. |
| Is R^{1/3} tight for current S-unit / linear-forms techniques? | **Plausibly yes** (see circularity in Step 2), but no lower bound proof. |
| What is the precise open question? | Whether the B ~ c circularity in the Baker application to S-unit equations can be broken without assuming abc. |
| What input would close the gap? | A bound B ≤ R^{O(1)} in the linear form, or an entirely different method (e.g., Arakelov geometry, beyond Baker). |

**Precise formulation of open question (for the number-theory literature):**

Does there exist an effectively computable A > 0 and an unconditional proof (not assuming
abc, Szpiro, or GRH) that for all coprime triples (a, b, c) with a + b = c:

    c < R^A   (R = rad(abc))

No such proof currently exists. The question of whether Baker-type methods can achieve
this is open: it is not known whether the B ~ c circularity is an artifact of the
current proof technique or an intrinsic obstruction to linear-forms methods.

---

## Conclusion

**Verdict: INCONCLUSIVE + LOCALIZATION.**

Baker-type linear-forms methods give the best unconditional bound
c < exp(κ·R^{1/3}·(log R)^3 / (log log R)) but cannot currently be pushed to c < R^A.

The precise obstruction is:
- **Step 1**: B ~ c (max Baker coefficient is ~c, not ~R).
- **Step 2**: Substituting B ~ log c into the Baker bound gives a circular inequality;
  this prevents closing c < R^A without external input bounding c in terms of R.
- **Step 3**: Pasten 2024 improves the constant in the exponent by log log R but does
  not change the R^{1/3} power or bridge the sub-exponential/polynomial gap.

Whether the R^{1/3} exponent is a true barrier for linear-forms methods is the
**open question** that this problem localizes. A proof that B can be bounded polynomially
in R (independent of c) — or a proof that it cannot — would resolve this question.
Neither currently exists in the literature.

**No progress on CORE-3 direct route from Baker methods.** The Baker-to-fixed-power gap
remains open and is not closed by this analysis. The `core3.iut-corollary-312-independently-verified`
obligation is unaffected by this report (Baker methods address a different CORE-3 route).
