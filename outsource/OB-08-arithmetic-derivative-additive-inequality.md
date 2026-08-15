# Problem OB-08 — Arithmetic Derivative Additive Inequality: Literature Survey and Status

**Type:** Analytic number theory / arithmetic derivatives  
**Non-circularity:** The inequality below involves only the arithmetic derivative n' (defined
unconditionally via the Leibniz rule and n'(p)=1 for primes) and the radical rad(n). It
does NOT assume the abc conjecture, Szpiro's conjecture, IUT, GRH, or any abc-equivalent
hypothesis. No known abc triples are used as inputs.

---

## Background

The **arithmetic derivative** n' : ℕ → ℕ is defined by:
- p' = 1 for every prime p
- (mn)' = m'n + mn' for all m, n ∈ ℕ (Leibniz rule)

Equivalently: n' = n · ∑_{p | n} vₚ(n)/p, where vₚ(n) is the p-adic valuation of n.

The **radical** of n is rad(n) = ∏_{p | n} p (product over distinct primes dividing n).

These are standard, classical objects. Arithmetic derivative references: Barbeau (1961),
Ufnarovski–Åhlander (2003, J. Integer Sequences).

---

## All definitions (self-contained)

- **Coprime abc triple**: positive integers a, b, c with a + b = c and gcd(a, b) = 1.
  (Note: gcd(a,b)=1 implies gcd(a,c)=gcd(b,c)=1 as well.)
- **Arithmetic derivative**: n' = n · ∑_{p|n} vₚ(n)/p. Examples:
  - (p^k)' = k · p^{k-1}  for prime p
  - (2·3)' = 2'·3 + 2·3' = 1·3 + 2·1 = 5
  - 1' = 0, 0' = 0
- **Radical**: rad(n) = ∏_{p|n} p. For coprime a+b=c: rad(abc) = rad(a)·rad(b)·rad(c).
  Write R = rad(abc).

---

## The inequality to be located in the literature

**Arithmetic Derivative Additive Inequality (ADAI, original form):**  
For all coprime positive integers a, b, c with a + b = c:
```
  a' + b' + rad(abc) ≥ C · c'
```
for some universal constant C > 0.

**Falsification evidence (numerical, discovery tier):** For the family (1, 2^k−1, 2^k)
with 2^k−1 prime (Mersenne primes), the ratio (a' + b' + R) / c' → 0 as k → ∞:
- k=7:  ratio ≈ 0.569  (M_7 = 127 prime)
- k=13: ratio ≈ 0.308  (M_13 = 8191 prime)
- k=31: ratio ≈ 0.129  (M_31 prime)
- Asymptotic: ratio ≈ 4/k → 0.

**Conclusion:** ADAI in its original form appears to be FALSE.

---

**Log-corrected ADAI (candidate refinement):**  
For all coprime positive integers a, b, c with a + b = c:
```
  a' + b' + R · log(R) ≥ C · c'
```
for some universal constant C > 0 (where log is the natural logarithm).

**Numerical evidence:**
- For Mersenne-prime families (1, 2^k−1, 2^k): ratio → 4·log(2) ≈ 2.773 as k → ∞.
- For composite-exponent families (k=18,21,36): ratio as low as **0.374** (at k=36).
  The composite-k ratios appear to be decreasing; it is unclear whether the infimum is 0.
- All 12 hand-selected high-quality abc triples tested: minimum ratio = 0.397 (at (3,125,128)).

**Status of log-corrected ADAI:** Not known to be false; not proved; infimum over all
coprime triples is unknown. May depend on whether highly-composite exponents give ratios
converging to 0.

---

## Questions to be answered (acceptance criteria)

**Q1 (primary — literature search).**  
Is either form of ADAI (original or log-corrected) known in the arithmetic derivative
literature? Specifically:

(a) Does any paper by Barbeau (1961), Ufnarovski–Åhlander (2003), Šoberger et al.,
    Haukkanen et al., or others give a bound of the form:
    ```
        (a+b)' ≤ f(a', b', rad(a), rad(b), rad(a+b))
    ```
    for coprime a+b=c?

(b) Is there a known theorem of the form `n' ≤ C · n · log(rad(n)) / rad(n)` (which
    would be essentially the log-corrected bound on c')?

(c) Is the log-corrected ADAI related to the **Arithmetic Derivative Conjecture** of
    Ufnarovski–Åhlander (if such a conjecture exists)?

(d) Is there a connection to known results on `n' / n` (the "arithmetic logarithmic
    derivative") and its distribution or extremal behavior?

**Q2 (boundary analysis).**  
Is the infimum of the ratio `(a' + b' + R·log R) / c'` over all coprime triples equal
to 0? If yes, give a family achieving ratio → 0. If no, give a lower bound proof or
reference.

**Q3 (implication, conditional).**  
Assuming log-corrected ADAI holds with some constant C > 0, does it imply the abc
conjecture? Specifically:

Given: a' + b' + R·log(R) ≥ C·c' for all coprime a+b=c.  
Does this imply: for all ε > 0, ∃ K_ε: c ≤ K_ε · R^{1+ε}?

The key step is bounding c in terms of c'. Note c' = c · ∑_{p|c} vₚ(c)/p, so
c = c' / (∑_{p|c} vₚ(c)/p). The question is whether ∑_{p|c} vₚ(c)/p is bounded
below by a function of R in a way that gives c ≤ R^{1+ε}.

**Q4 (weaker conclusions).**  
If the log-corrected ADAI holds, what is the best unconditional bound on c it implies?
For example: does it give c ≤ R · (log R)^A for some fixed A? For which A?

---

## Proof skeleton to be analyzed

### Step 1 — Reduce c to c'/σ

Write σ(c) = c'/c = ∑_{p|c} vₚ(c)/p ∈ (0, ∞). Then c = c'/σ(c).

**What to close:** Is σ(c) bounded below by a function of R = rad(abc)?  
For c = p^k: σ = k/p. Since p ≤ R and k = log c / log p, we get σ = log c / (p log p).  
For the bound c ≤ R^{1+ε} to follow, need σ(c) ≥ c^{-ε/something}.  
This seems circular: σ depends on c.

### Step 2 — Apply log-corrected ADAI

If ADAI-log holds: c' ≤ (a' + b')/C + R·log(R)/C.  
Together with c = c'/σ: c = c'/(σ) ≤ [(a'+b')/C + R·log(R)/C] / σ.  
For the bound c ≤ R^{1+ε}, need the RHS ≤ R^{1+ε}.  
Since a' ≤ a·log(a)/log p_min(a) and similarly for b', the a'+b' terms are bounded
by c·something. This is NOT obviously helpful — it re-introduces c.

### Step 3 — Iterative or alternative approach

An alternative: use ADAI-log to bound c' from above, then use c'/c = σ as a separate
lower bound. What is the best unconditional lower bound on σ(c) = c'/c?

Known: for c = p^k, σ = k/p; for c with many distinct prime factors, σ ≈ Ω(c)/p_min.
No universal lower bound in terms of R appears obvious.

**What to close for Step 3:** Either prove the implication works for some weaker
conclusion (c ≤ R·(log R)^A) OR exhibit an obstruction showing ADAI-log does not
directly imply abc.

---

## Acceptance criteria

1. **FOUND in literature (full citation + statement):** Provide the reference, theorem
   number, and exact statement. Determine whether it is proved or conjectured.

2. **NOT found but related conjecture identified:** Name the closest known conjecture,
   state the gap, and suggest whether ADAI-log is weaker or stronger.

3. **Infimum analysis (Q2):** Either a family showing inf = 0 (falsifying ADAI-log) or
   a lower bound argument. "Not clear" with a precise localization of the difficulty
   is also acceptable.

4. **Implication (Q3):** Either a proof sketch that ADAI-log → abc, OR a precise
   statement of the obstruction (e.g., "implication requires a lower bound on σ(c)
   that is not provable from ADAI-log alone").

5. **INCONCLUSIVE outcome is acceptable** if accompanied by a precise localization of
   the obstruction (the specific inequality or formula that would need to be proved).

---

## Numerical anchor (sanity only, not an input to any proof)

For (a, b, c) = (1, 2400, 2401) = (1, 2^5·3·5^2, 7^4):
- a' = 0, b' = 2400·(5/2 + 1/3 + 2/5) = 2400·(1/2·5 + 1/3 + 2/5)
  Actually b' = 5·1200 + 1·800 + 2·480 = 6000+800+960 = 7760
- c' = 4·343 = 1372 (since c = 7^4, c' = 4·7^3)
- R = rad(1)·rad(2400)·rad(2401) = 1·(2·3·5)·7 = 210
- Orig ratio: (0+7760+210)/1372 = 7970/1372 ≈ 5.81
- Log-corr ratio: (0+7760+210·log(210))/1372 = (7760+1099)/1372 ≈ 6.46

Both ratios > 1; consistent with ADAI-log holding for this triple.
