# Problem OB-01 — Algebraic geometry height bound for the Frey curve

**Type:** algebraic geometry / Arakelov theory

**Non-circularity:** This problem does **not** assume the abc conjecture, Szpiro's conjecture (or any of its variants), Mochizuki's IUT Corollary 3.12, any fitted constant K_ε derived from known triples, or any other assertion directly equivalent to abc. The goal is either a proof that avoids all such inputs, or a precise identification of the obstruction showing why the approach cannot be completed without an abc-equivalent hypothesis.

---

## All definitions (self-contained — everything is here)

**Coprime triple.** A triple (a, b, c) of positive integers is *coprime* if gcd(a, b) = gcd(b, c) = gcd(a, c) = 1 and a + b = c.

**rad function.** For a positive integer n, rad(n) = ∏_{p | n, p prime} p (product of distinct prime factors). Convention: rad(1) = 1. For a coprime triple (a, b, c), rad(abc) = rad(a) · rad(b) · rad(c) since gcd(a,b) = gcd(a,c) = gcd(b,c) = 1.

**Frey elliptic curve.** For a coprime triple (a, b, c) with a + b = c, the Frey curve is

    E_{a,b,c} : y² = x(x − a)(x + b)   over Q.

This is an elliptic curve when a, b, c are nonzero (which holds since a, b, c ≥ 1 and gcd(a,b) = 1 implies c ≥ 2).

**Discriminant of E_{a,b,c}.** The discriminant of the Weierstrass model y² = x(x − a)(x + b) is

    Δ = 16 · a² · b² · c²  = 16 · (abc)².

(Here we use the standard formula Δ = −16 · 4p³ − 27q² for y² = x³ + px + q; converting x(x−a)(x+b) = x³ + (b−a)x² − abx to the form y² = x³ + px + q by completing the square, the discriminant of the cubic factor is (b−a)² + 4ab·1... see step 1 for the explicit reduction to minimal model.)

**Minimal discriminant.** For E_{a,b,c} (a, b, c coprime positive integers summing to c), after passing to the global minimal Weierstrass model, the minimal discriminant Δ_min satisfies:

    |Δ_min| = 2^{−8} · (abc)² · (product of local correction factors at 2).

More precisely (Connell 1994 / Silverman AEC, §VII.1): for a, b, c pairwise coprime, the minimal discriminant has

    v_p(Δ_min) = 2 v_p(abc)   for odd primes p,
    v_2(Δ_min) = 2 v_2(abc) − 8   (with possible correction ±6 depending on 2-adic valuation of a, b).

A safe uniform lower bound (sufficient for this problem) is:

    log |Δ_min| ≥ 2 log(abc) − 8 log 2 − 6 log 2 = 2 log(abc) − 14 log 2.

**Conductor of E_{a,b,c}.** The arithmetic conductor N_E is defined by N_E = ∏_p p^{f_p}, where the local exponents f_p are

    f_p = 0            if E has good reduction at p,
    f_p = 1            if E has multiplicative reduction at p,
    f_p = 2 + δ_p      if E has additive reduction at p (δ_p ≥ 0 from wild part).

Key facts:
- E_{a,b,c} has bad reduction exactly at primes p | abc (Frey 1986).
- rad(N_E) = rad(2abc) (all bad-reduction primes divide 2abc).
- For odd primes p | abc: f_p ∈ {1, 2} (multiplicative or tame additive).
- For p = 2: f_2 ≤ 8 (bounded wild part for curves over Q_2).

Therefore:

    log N_E ≤ Σ_{p | abc} f_p log p ≤ Σ_{p | abc} (2 + δ_p) log p ≤ 2 log rad(abc) + Σ_p δ_p log p.

Since δ_p = 0 for odd p (Frey curves are semistable at odd primes — Serre 1987), and δ_2 ≤ 6:

    log N_E ≤ 2 log rad(abc) + 6 log 2.

**Faltings height.** The Faltings height of an elliptic curve E/Q is defined via Arakelov theory as:

    h_F(E) = − (1/[Q:Q]) Σ_{v place of Q} log ‖ω‖_v

where ω is a Néron differential on the minimal model of E, and ‖·‖_v are normalized metrics at each place. An explicit formula for the Faltings height in terms of the minimal discriminant and period is (Silverman, *Advanced Topics in the Arithmetic of Elliptic Curves*, Chapter II, Theorem 1.1):

    h_F(E) = (1/12) log |Δ_min(E)| − (1/2) log(2π) − (1/2) log Ω_E + O(1)

where Ω_E = ∫_{E(C)} |ω ∧ ω̄| is the real period. For comparison purposes, the *naive height* of E relative to its j-invariant satisfies h(j(E)) = h_F(E) + O(1) (bounded constant independent of E).

A simpler equivalent form used in this problem: since the real period Ω_E satisfies 0 < Ω_E ≤ C_0 (bounded above by a universal constant for elliptic curves with |Δ_min| ≥ 1), we have the lower bound

    h_F(E) ≥ (1/12) log |Δ_min(E)| − C_1

for a universal constant C_1 > 0.

**Quality of a coprime triple.** The quality of (a, b, c) is q(a,b,c) = log c / log rad(abc). The abc conjecture (in Masser–Oesterlé form) asserts: for every ε > 0, there exists K_ε > 0 such that c ≤ K_ε · rad(abc)^{1+ε} for all coprime triples — equivalently, q(a,b,c) ≤ 1 + ε except for finitely many triples.

---

## The theorem / claim to be verified

**Claim OB-01.** For every ε > 0 there exists a constant C_ε > 0, computable from ε alone (no abc triples, no fitted parameters), such that for **all** coprime triples (a, b, c) with a + b = c and a, b, c ≥ 1:

    h_F(E_{a,b,c}) ≤ C_ε · (1 + ε) · log rad(abc).

Equivalently (using the lower bound on h_F from the minimal discriminant):

    (1/12) log |Δ_min(E_{a,b,c})| ≤ C_ε · (1 + ε) · log rad(abc) + O(1).

Note: since log |Δ_min| ≥ 2 log c − O(1) (see Step 2), this claim implies the quantitative abc inequality c ≤ exp(C_ε (1+ε) log rad(abc) + O(1)) = K_ε' · rad(abc)^{1+ε}, i.e., the abc conjecture. A proof of Claim OB-01 would therefore constitute a proof of the abc conjecture.

---

## Proof skeleton to be closed

### Step 1 — Minimal discriminant formula

**Draft.** For E_{a,b,c} : y² = x(x−a)(x+b), the model y² = x³ + (b−a)x² − abx has discriminant Δ_Weierstrass = 16a²b²c² = 16(abc)². The global minimal model is obtained by removing p^12-powers (Tate algorithm). For odd p, since a, b, c are pairwise coprime, at most one of a, b, c is divisible by p, so p²‖(abc) means p‖(exactly one of a,b,c), giving v_p(Δ_Weierstrass) = 2. The Tate algorithm at an odd prime p with v_p(Δ) = 2 does NOT reduce the model (the model is already minimal at p), so v_p(Δ_min) = v_p(Δ_Weierstrass) = 2v_p(abc) for odd p.

At p = 2: the analysis depends on the 2-adic residues of a, b, c. Since a + b = c and exactly one of {a,b,c} can be even (gcd(a,b) = 1; if a,b both odd then c is even; if one of a,b is even then the other two are odd), the 2-adic part introduces a correction of at most ±8 in v_2(Δ_min) relative to 2v_2(abc).

**What to close for Step 1:** Provide an exact formula (or a uniform ±O(1) estimate) for log|Δ_min(E_{a,b,c})| valid for ALL coprime triples, handling all 2-adic cases. Specifically: confirm or correct the claim

    2 log(abc) − 14 log 2 ≤ log |Δ_min(E_{a,b,c})| ≤ 2 log(abc) + 8 log 2

and verify the lower bound is tight (or improve it).

---

### Step 2 — Faltings height lower bound in terms of log c

**Draft.** From Step 1, log |Δ_min| ≥ 2 log(abc) − C_2 for a universal constant C_2. Since a, b ≥ 1 and a + b = c, we have abc = a · b · c ≥ 1 · 1 · c = c, so

    log |Δ_min| ≥ 2 log c − C_2.

Combined with h_F ≥ (1/12) log |Δ_min| − C_1:

    h_F(E_{a,b,c}) ≥ (1/6) log c − C_3.

**What to close for Step 2:** Confirm that h_F ≥ (1/6) log c − C_3 for a universal C_3 > 0. This is a LOWER bound on h_F and does not require abc. It tells us h_F grows at least like log c, so bounding h_F from above by log rad(abc) is equivalent to bounding log c by log rad(abc).

---

### Step 3 — Conductor upper bound in terms of rad(abc)

**Draft.** From the definitions: N_E ≤ 2^8 · (rad(abc)/2)² · ... More precisely, for Frey curves E_{a,b,c} with a,b,c pairwise coprime:

    log N_E ≤ 2 log rad(abc) + 6 log 2.

This follows from: (i) bad primes of E are exactly the prime divisors of abc; (ii) E is semistable at all odd primes (Frey 1986, Serre 1987); (iii) f_p ≤ 2 for all p | abc.

**What to close for Step 3:** Verify (or refute) the semistability claim for all odd primes p | abc. Specifically: confirm that for every odd prime p | abc with (a,b,c) any coprime triple, the Frey curve E_{a,b,c} has multiplicative (hence semistable) reduction at p, so f_p = 1 and the conductor contribution is exactly log p (not 2 log p). If this holds, then log N_E ≤ log rad(abc) + O(1) (not 2 log rad(abc)), which would be stronger.

---

### Step 4 — Szpiro-type height-conductor bound (the critical step)

**Draft.** A *Szpiro-type bound* for an elliptic curve E/Q is a bound of the form

    log |Δ_min(E)| ≤ C_Szp · log N_E + O(1)

for some constant C_Szp > 0. Szpiro's conjecture asserts that C_Szp = 6 + ε works for every ε > 0.

If this bound held with some explicit C_Szp, then from Steps 1–3:

    (1/12) log |Δ_min| ≥ (1/6) log c − C_3   (Step 2, lower bound on lhs)
    log |Δ_min| ≤ C_Szp · log N_E + O(1)       (Szpiro-type bound, UNPROVED)
    log N_E ≤ 2 log rad(abc) + O(1)             (Step 3)

Combining: (1/6) log c ≤ (C_Szp/12) · 2 log rad(abc) + O(1), i.e., log c ≤ (C_Szp/6 · 2) log rad(abc) + O(1).

Setting C_ε = C_Szp/3 gives the height bound in Claim OB-01.

**What to close for Step 4:** The Szpiro-type bound log |Δ_min(E)| ≤ C_Szp · log N_E + O(1) is equivalent to Szpiro's conjecture (for Frey curves). Szpiro's conjecture is equivalent to the abc conjecture (Szpiro–Oesterlé–Masser, 1985; see Hindry–Silverman, "Sur le nombre de points de torsion rationnels sur une courbe elliptique", 1988). Therefore, this step CANNOT be closed without an abc-equivalent hypothesis.

---

### Step 5 — Obstruction analysis

**Draft.** The obstruction to completing the proof skeleton is precisely at Step 4.

To demonstrate the obstruction concretely: consider the family of triples (a_n, b_n, c_n) such that c_n / rad(abc_n)^{1+ε} → ∞ (if abc fails — i.e., a family of triples with quality q(a_n,b_n,c_n) → ∞). For such a family, E_{a_n,b_n,c_n} would have

    log |Δ_min(E_{a_n,b_n,c_n})| ≥ 2 log c_n − C_2   →   ∞

while

    log N_{E_{a_n,b_n,c_n}} ≤ 2 log rad(a_n b_n c_n) + O(1)   ≤   (2/(1+ε)) log c_n + O(1).

The ratio log |Δ_min| / log N_E → 2 log c_n / ((2/(1+ε)) log c_n) = (1+ε) → 1+ε as n → ∞. The Szpiro ratio for these curves approaches 1+ε · 6 in the limit (the factor of 6 comes from the Δ_min ↔ N_E relationship for triples with large quality ratio). Any proof of Step 4 that does not use abc as a hypothesis must bound this ratio universally — which IS the abc conjecture.

**What to close for Step 5:** Either (a) exhibit an explicit family of Frey curves where log |Δ_min(E)| / log N_E is unbounded (which would DISPROVE Szpiro's conjecture and hence abc), or (b) provide a proof that log |Δ_min(E)| / log N_E is universally bounded for Frey curves, with an explicit bound, that does NOT assume Szpiro or abc. Either outcome resolves Claim OB-01.

---

## Acceptance criteria

1. **CONFIRMED-PROOF**: A complete proof of h_F(E_{a,b,c}) ≤ C_ε (1+ε) log rad(abc) for ALL coprime triples (a,b,c), with C_ε depending only on ε (no abc triples, no Szpiro assumed, no abc-equivalent hypothesis at any step). Must include an explicit formula for C_ε.

2. **CONFIRMED-OBSTRUCTION**: A precise identification of the step in the proof skeleton where an abc-equivalent hypothesis is unavoidable, together with an explicit family of elliptic curves demonstrating why the Szpiro-type step cannot be closed without such a hypothesis. Acceptable outcome.

3. **PARTIAL**: A complete proof of one or more of Steps 1–3 with a precise statement of what remains open at Step 4 or Step 5.

4. **INCONCLUSIVE**: A clear statement of the current literature state on the Szpiro conjecture for Frey curves, with references, and identification of which sub-problem is the current frontier.

**Not accepted**: "This follows from Szpiro's conjecture" (equivalent to abc — not a proof). "This follows from the abc conjecture" (circular). "This is well-known" without citation and explicit proof sketch.

---

## Numerical anchor (sanity only — not an input to the proof)

For (a, b, c) = (1, 8, 9): these are coprime (gcd(1,8)=gcd(1,9)=gcd(8,9)=1) and 1 + 8 = 9. ✓

- rad(abc) = rad(1 · 8 · 9) = rad(1) · rad(8) · rad(9) = 1 · 2 · 3 = 6.
- log rad(abc) = log 6 ≈ 1.792.
- log c = log 9 ≈ 2.197.
- Quality: q = log 9 / log 6 ≈ 1.226.
- Frey curve: E_{1,8,9} : y² = x(x − 1)(x + 8) = x³ + 7x² − 8x.
- Discriminant of Weierstrass model: Δ_W = 16 · (1·8·9)² = 16 · 5184 = 82944.
- log |Δ_W| = log 82944 ≈ 11.33.
- h_F estimate ≈ (1/12) log |Δ_min| ≈ 0.94.
- (1+ε) log rad(abc) = (1+0.5) · 1.792 ≈ 2.688.

Sanity check: h_F(E_{1,8,9}) ≈ 0.94 ≤ 2.688 ✓ for ε = 0.5.

**Label**: This is a sanity check only — it does not constitute evidence that the bound holds universally, and the (1,8,9) triple is not used anywhere in the proof construction.
