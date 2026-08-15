# Problem OB-07 — Baker-type methods and fixed-power quality bounds for abc (CORE-3 direct route)

**Type:** analytic number theory / Baker theory / S-unit equations
**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
IUT Corollary 3.12, known abc triples as analytic input, or any fitted parameter K_ε.
It asks whether existing unconditional methods (Baker's theorem, S-unit equations, linear
forms in logarithms) can give a fixed-power bound c ≤ K₀ · R^A — and if not, what the
precise obstruction is. No parameter is derived from high-quality examples.

---

## All definitions (self-contained — everything is here)

**Coprime abc-triple.** Positive integers (a, b, c) with a + b = c and gcd(a, b) = 1
(implies gcd(a, c) = gcd(b, c) = 1; a, b, c are pairwise coprime).

**rad function.** rad(n) = ∏_{p | n, p prime} p (distinct prime factors of |n|).

**Radical R.** R = rad(abc) = rad(a) · rad(b) · rad(c).

**Quality.** q(a, b, c) = log c / log R.

**Fixed-power weak abc (open; Pasten, J. Number Theory 254 (2024), Conjectures 1.1–1.2).**
The assertion: there exists a constant K > 0 (universal) such that q(a, b, c) ≤ K for
all coprime abc-triples, i.e., c ≤ K₀ · R^A for effective constants K₀, A > 0.
NOTE: Pasten's stated conjecture only asserts *existence* of K; effectivity is a further
strengthening. This problem asks about the effective version.

**Standard abc conjecture.** For every ε > 0, ∃ C_ε > 0 such that c ≤ C_ε · R^{1+ε}
for all coprime triples. Strictly stronger than fixed-power weak abc (the exponent 1+ε
can approach 1, whereas fixed-power weak abc allows a fixed large exponent A).

**Best unconditional result (Stewart–Yu, Duke Math. J. 108 (2001), Theorem 1):**

    c < exp(κ · R^{1/3} · (log R)^3)

for an effectively computable constant κ > 0. This is a sub-exponential bound: the
exponent is R^{1/3}(log R)^3, which grows faster than any fixed power of log R.

**Baker's theorem (linear forms in logarithms).** Let α₁,…,αₙ ∈ Q* be algebraic, not 0
or 1; b₁,…,bₙ non-zero integers. If Λ = b₁ log α₁ + ··· + bₙ log αₙ ≠ 0, then

    log|Λ| > −C(n, d) · (log B + 1) · ∏ᵢ log max(|αᵢ|, 2)

where B = max|bᵢ|, d = [Q(α₁,…,αₙ):Q], and C(n,d) is an effectively computable constant
depending only on n and d. The key feature: the bound is LINEAR in log B (not polynomial
in B itself).

**S-unit equation connection.** Given a coprime triple a + b = c, divide by c to get
(a/c) + (b/c) = 1. Both a/c and b/c are S-units for S = {primes dividing 2abc}. Baker's
theorem applied to log(a/c) = log a − log c gives a lower bound on |log(a/c)| in terms
of the prime factors.

**Stewart–Yu exponent R^{1/3}.** The R^{1/3} factor in the Stewart–Yu bound arises from
the effective Baker bound on the S-unit equation: the exponent bᵢ in the linear form Λ
can be as large as c itself (roughly), and the Baker bound log|Λ| > −C log B with
B ~ c gives |Λ| > exp(−C log c), hence c > exp(C' · something). The R^{1/3} comes from
the specific prime-distribution argument in Stewart–Yu using the structure of rad(abc).

---

## The theorem / claim to be verified

**Claim OB-07**: Determine whether Baker-type methods can give a fixed-power (polynomial
in R) bound for abc quality.

**Either:**

(A) **Prove a polynomial bound:** There exist effective constants κ > 0 and A > 0 such
    that for all coprime triples (a, b, c):

        c < (some polynomial or polylogarithm in R)

    such that this bound is strictly better than exp(κ · R^{1/3}(log R)^3) for large R
    (in the sense: the exponent of R in the bound is less than 1/3).

**Or:**

(B) **Identify the precise obstruction:** Explain why Baker-type linear-forms methods
    (as currently applied) cannot give c ≤ K₀ · R^A for any fixed A, identifying:
    - Which step in the Stewart–Yu argument produces the R^{1/3} factor
    - Whether the R^{1/3} is tight for linear-forms methods (or just an artifact of
      the current proof technique)
    - What fundamentally different method would be needed to reach a polynomial bound

---

## Proof skeleton to be closed

### Step 1 — Stewart–Yu bound: trace the R^{1/3} exponent

**What to close:** Give the precise derivation of how R^{1/3}(log R)^3 arises in
Stewart–Yu (Theorem 1 of Duke Math. J. 108 (2001)). Specifically:
- What linear form Λ does Baker's theorem apply to?
- What is B (the max coefficient) in terms of a, b, c, R?
- How does B relate to R? (Is B ~ c, ~ log c, ~ R, or something else?)
- Where does the exponent 1/3 enter the bound?

### Step 2 — Gap analysis: from exp(R^{1/3}) to R^A

**What to close:** The gap between c < exp(κ R^{1/3}(log R)^3) and c < K₀ R^A is the
gap between sub-exponential and polynomial growth. Determine:

(a) **Known impossibility:** Is there a theorem showing Baker-type methods provably cannot
    give polynomial bounds for abc (even for fixed A)? If so, cite the theorem and
    explain the obstruction.

(b) **Open question:** Is it an open question whether Baker-type refinements could give
    polynomial bounds? If so, state precisely what is unknown and why.

Key sub-question: in the S-unit equation proof, B (the max coefficient in the linear form)
satisfies B ≤ c. Since c can be much larger than R (e.g., c = R^q with q > 1), the Baker
bound produces a factor depending on log c, not log R. To get a bound c < R^A, one would
need to control log c in terms of log R — which is circular if we use Baker to prove the
bound. Analyze this circularity precisely.

### Step 3 — Pasten 2024: does it improve the exponent toward polynomial?

**What to close:** Pasten's 2024 Inventiones paper (arXiv:2312.03566, DOI:
10.1007/s00222-024-01244-6) improves sub-exponential bounds using Shimura curves. Does it:
(a) Give any bound with exponent less than 1/3 (i.e., c < exp(κ · R^δ) for δ < 1/3)?
(b) Require additional conditions on abc (e.g., a restriction on which primes divide abc)?
(c) Give any polynomial-type bound for any specific subfamilies of abc-triples?

Cite Theorem 1.4 and bound (1.7) from that paper; verify that (1.7) is still the best
unconditional bound for arbitrary triples.

### Step 4 — Conclusion and precise gap statement

**What to close:** Provide a precise statement of:
- The best currently provable unconditional bound of the form c < f(R).
- The precise gap between this bound and fixed-power weak abc c ≤ K₀ · R^A.
- Whether the gap is a known impossibility (with theorem), an open question (with
  precise formulation), or something in between.

---

## Acceptance criteria

1. **PROGRESS**: A bound strictly better than Stewart–Yu, in the sense that the exponent
   of R is reduced below 1/3 unconditionally for all coprime triples. This would be a
   genuine mathematical advance; report the exact new bound.

2. **PRECISE-OBSTRUCTION**: A theorem or precise argument showing that Baker-type
   linear-forms methods provably cannot give c ≤ K₀ · R^A for any fixed A > 0, with the
   exact step where the method fails.

3. **INCONCLUSIVE + LOCALIZATION**: A precise statement of which step in the Baker-to-
   fixed-power gap is currently unknown, with the exact open question in the analytic
   number theory literature and the specific missing input that would close the gap.

4. **NEGATIVE WITH EVIDENCE**: A precise analysis showing that the R^{1/3} exponent
   appears to be essentially tight for S-unit / linear-forms methods, with evidence from
   the structure of the Baker bound (e.g., showing that B ~ c is unavoidable in the
   S-unit approach, and B ~ c gives exp(log c) ~ c which is circular).

**Not accepted:**
- "It is open whether Baker methods can prove abc." That is too vague; the answer must
  localize the obstruction to a specific step or show explicit progress.
- Any argument that assumes abc, Szpiro, IUT Corollary 3.12, or any abc-equivalent
  hypothesis to derive the bound.
- Any parameter K or A derived by fitting to known high-quality abc triples.

---

## References (verify from source before citing)

1. C. L. Stewart and Kunrui Yu, "On the abc conjecture, II," Duke Math. J. 108 (2001),
   no. 1, 169–181, Theorem 1.
   URL: https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/s0012-7094-01-10815-6.pdf
2. Héctor Pasten, "The largest prime factor of n²+1 and improvements on subexponential ABC,"
   Inventiones Mathematicae 236 (2024), 373–385, Theorem 1.4 and bound (1.7).
   arXiv: https://arxiv.org/abs/2312.03566
3. Héctor Pasten, "Shimura curves and the abc conjecture," J. Number Theory 254 (2024),
   Conjectures 1.1–1.2. arXiv: https://arxiv.org/abs/1705.09251
4. A. Baker and G. Wüstholz, "Logarithmic forms and group varieties," J. Reine Angew.
   Math. 442 (1993), 19–62. (Baker's theorem, effective version.)

---

## Numerical anchor (sanity only — not an input to the proof)

For (a, b, c) = (1, 8, 9): R = rad(1·8·9) = rad(72) = 2·3 = 6.

```python
import math
a, b, c = 1, 8, 9
R = 6
# Stewart-Yu bound (kappa=1 for illustration only; actual kappa not specified here)
kappa = 1
stewart_yu_bound = math.exp(kappa * R**(1/3) * math.log(R)**3)
# Fixed-power bound at A=2, K0=1 (example only; not claimed to hold universally):
A, K0 = 2, 1
fixed_power_bound = K0 * R**A
q = math.log(c) / math.log(R)
print(f"R = {R}")
print(f"Stewart-Yu bound (kappa=1, illustration): c < {stewart_yu_bound:.1f}")
print(f"Fixed-power bound (A=2, K0=1, example): c <= {fixed_power_bound}")
print(f"Actual c = {c}")
print(f"Quality q = log({c})/log({R}) = {q:.6f}")
print(f"Gap factor (Stewart-Yu / fixed-power): {stewart_yu_bound / fixed_power_bound:.1f}x")
```

Expected output:
```
R = 6
Stewart-Yu bound (kappa=1, illustration): c < 34633.1
Fixed-power bound (A=2, K0=1, example): c <= 36
Actual c = 9
Quality q = log(9)/log(6) = 1.226294
Gap factor (Stewart-Yu / fixed-power): 962.0x
```

The 962x gap between the two bounds for this tiny example illustrates the magnitude of
the improvement needed to reach a polynomial bound. This is a sanity check only;
(1, 8, 9) is not used as input to any proof, and no K or A is fitted to this or any
other example.
