# Problem OB-01 — Algebraic geometry height bound for the Frey curve

**Type:** algebraic geometry / Arakelov theory

**Non-circularity:** This problem does **not** assume the abc conjecture, Szpiro's conjecture (or any of its variants), Mochizuki's IUT Corollary 3.12, any fitted constant K_ε derived from known triples, or any other assertion directly equivalent to abc. The goal is either a proof that avoids all such inputs, or a precise identification of the obstruction showing why the approach cannot be completed without an abc-equivalent hypothesis.

**Review status (2026-08-15):** PARTIAL — Steps 1–3 independently verified and strengthened; Claim OB-01 remains open (equivalent to effective fixed-power weak abc). Two load-bearing statements require major correction: the (1/6+ε) height target is false (§ below), and ordinary/modified Szpiro must be distinguished. See `reviews/OB-01-review-2026-08-15.md` for the first referee report and `~/Downloads/OB-01-independent-referee-report-2026-08-15.md` for the independent report.

---

## All definitions (self-contained — everything is here)

**Coprime triple.** A triple (a, b, c) of positive integers is *coprime* if gcd(a, b) = gcd(b, c) = gcd(a, c) = 1 and a + b = c.

**rad function.** For a positive integer n, rad(n) = ∏_{p | n, p prime} p (product of distinct prime factors). Convention: rad(1) = 1. For a coprime triple (a, b, c), rad(abc) = rad(a) · rad(b) · rad(c) since gcd(a,b) = gcd(a,c) = gcd(b,c) = 1. Write R = rad(abc) throughout.

**Frey elliptic curve.** For a coprime triple (a, b, c) with a + b = c, the Frey curve is

    E_{a,b,c} : y² = x(x − a)(x + b)   over Q.

This is an elliptic curve when a, b, c are nonzero (which holds since a, b, c ≥ 1 and gcd(a,b) = 1 implies c ≥ 2).

**Discriminant of E_{a,b,c}.** The Weierstrass model y² = x(x−a)(x+b) has invariants

    c₄ = 16(a² + ab + b²),    Δ_W = 16 a² b² c² = 16(abc)².

**Minimal discriminant.** By Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed. (2009), Lemma VIII.11.3(a), the global minimal discriminant takes exactly one of two values:

    |Δ_min(E_{a,b,c})| ∈ { 16(abc)² , 2⁻⁸(abc)² }.

The two cases correspond to the unique Weierstrass change of variables u ∈ {1, 2} admitted by the minimality condition (u⁴ | 288). Consequently:

    2 log(abc) − 8 log 2  ≤  log |Δ_min|  ≤  2 log(abc) + 4 log 2.   [★]

Both bounds are sharp: (a,b,c) = (1,1,2) achieves the upper bound; (a,b,c) = (16,1,17) achieves the lower bound.

For odd prime p | abc, coprimeness forces v_p(abc) = v_p(exactly one of a,b,c), and one checks p ∤ c₄, so

    v_p(Δ_min) = 2 v_p(abc).          (Silverman, Lemma VIII.11.3(b))

The "p² ‖ abc" shorthand in earlier drafts was imprecise; the valuation can be arbitrarily large.

**Conductor of E_{a,b,c}.** The arithmetic conductor is N_E = ∏_p p^{f_p}. By Silverman Lemma VIII.11.3(b):
- For every odd prime p | abc: reduction is multiplicative, so f_p = 1.
- For odd primes p ∤ abc: good reduction, f_p = 0.
- At p = 2: Barrios–Roy, Theorem 3.7 / Table 7 (taking d=1, since E has a full rational 2-torsion point) gives 0 ≤ f₂ ≤ 5.

Therefore N_E = 2^{f₂} ∏_{p | abc, p odd} p, and since exactly one of a,b,c is even,

    R = 2 · ∏_{p | abc, p odd} p,     so

    N_E = 2^{f₂−1} R,    and    log N_E ≤ log R + 4 log 2.

Note: the bad-reduction set at odd primes is exactly {odd p | abc}; at p = 2 the situation requires separate analysis (e.g. (16,1,17) has good reduction at 2 despite 2 | abc).

**Faltings height.** The Faltings height h_F(E) is defined via Arakelov theory. We use the normalization of Murty–Pasten (*Modular forms and effective Diophantine approximation*, J. Number Theory 133 (2013), Theorems 5.1, 5.4):

    12 h_F(E) = log|Δ_E| − log(|Δ(τ_E)| · (Im τ_E)⁶) + 12 log(2π).

Their Theorem 5.4 gives the unconditional lower bound

    12 h_F(E) > log|Δ_E| + 28.326.

Combined with [★] and abc ≥ c:

    h_F(E_{a,b,c}) > (1/6) log c + (28.326 − 8 log 2) / 12
                   = (1/6) log c + 1.8984….

Under any other standard normalization, this becomes h_F ≥ (1/6) log c − C for a universal constant C.

The comparison h(j(E)) = h_F(E) + O(1) with O(1) uniform over all elliptic curves is **not** valid; the precise comparison contains log(1 + h(j)) terms (Löbrich, JTNB 29 (2017), Proposition 3.1).

For the upper direction: Murty–Pasten Theorem 7.1 gives unconditionally

    h_F(E) < 0.1 N_E log N_E + 11,

which for Frey curves yields h_F = O(R log R), far from the O(log R) target of Claim OB-01.

**Quality of a coprime triple.** The quality is q(a,b,c) = log c / log R. Standard abc asserts: for every ε > 0 there are only finitely many coprime triples with q > 1 + ε. Fixed-power weak abc (open; Pasten Conjectures 1.1–1.2, J. Number Theory 254 (2024)) asserts: there exists a fixed K (existence only; effectivity is a further strengthening not required by Pasten's statement) with q(a,b,c) ≤ K for all coprime triples.

---

## The theorem / claim to be verified

**Claim OB-01.** For every ε > 0 there exists a constant C_ε > 0, computable from ε alone (no abc triples, no fitted parameters), such that for **all** coprime triples (a, b, c) with a + b = c and a, b, c ≥ 1:

    h_F(E_{a,b,c}) ≤ C_ε · (1 + ε) · log R.

**Logical status of Claim OB-01 (corrected).** Since C_ε is unconstrained, the factor (1 + ε) is absorbed: Claim OB-01 is equivalent to the existence of an effective fixed K with h_F(E_{a,b,c}) ≤ K log R for all triples. Via the lower bound h_F > (1/6) log c + 1.898… and the reverse direction (§5.2 of the first referee report; §6 of the independent report), this is equivalent to **effective fixed-power weak abc** (bounded quality q ≤ K₀ for an effective K₀). Note: Pasten Conjectures 1.1–1.2 only assert existence of K, not effectivity; Claim OB-01 requires the effective strengthening. This is an open conjecture but is **strictly weaker** than standard abc.

**The (1/6+ε) log R target is false.** One might think that to target standard abc strength one needs h_F(E_{a,b,c}) ≤ (1/6 + ε) log R + C_ε. This is **unconditionally false**. The family

    (a_n, b_n, c_n) = (1, 2^n − 1, 2^n)

is pairwise coprime with a_n + b_n = c_n, and R_n = 2 rad(2^n − 1) < 2^{n+1}. The Murty–Pasten lower bound gives h_F(E_n) > (2n−1)/6 · log 2 + 1.898…, whose slope in n is (1/3) log 2. But (1/6 + ε)(n+1) log 2 has strictly smaller slope for any ε < 1/6, so the upper bound is eventually violated. The relevant conjecture for standard abc strength uses leading coefficient 1/2 + ε (Javanpeykar, Conjecture (h)), not 1/6 + ε. (See independent referee report §8.)

---

## Proof skeleton to be closed

### Step 1 — Minimal discriminant formula

**Established (unconditionally, by referee).** For E_{a,b,c} : y² = x(x−a)(x+b):

    |Δ_min(E_{a,b,c})| ∈ { 16(abc)², 2⁻⁸(abc)² }.

Hence

    2 log(abc) − 8 log 2  ≤  log|Δ_min|  ≤  2 log(abc) + 4 log 2.

Source: Silverman AEC 2nd ed., Lemma VIII.11.3(a). Both bounds are achieved (see §2.3 of the referee report).

**Remaining for Step 1:** None — this step is closed. The earlier draft's bounds (−14 log 2 lower, +8 log 2 upper) are correct but non-optimal; the above are tight.

---

### Step 2 — Faltings height lower bound in terms of log c

**Established (unconditionally).** By Murty–Pasten Theorems 5.1 and 5.4:

    h_F(E_{a,b,c}) > (1/6) log c + 1.898…

This holds in the Murty–Pasten normalization. In any other standard normalization it reads h_F ≥ (1/6) log c − C for a universal constant C.

**Remaining for Step 2:** None — this step is closed. Citation correction: the earlier draft cited Silverman *Advanced Topics* Ch. II Thm 1.1; that reference does not support the stated formula. Use Murty–Pasten (2013) throughout.

---

### Step 3 — Conductor upper bound in terms of R

**Established (unconditionally).** For Frey curves E_{a,b,c} with a,b,c pairwise coprime:

    N_E = 2^{f₂−1} R,    0 ≤ f₂ ≤ 5,    so    log N_E ≤ log R + 4 log 2.

Source: odd-prime conductor exponents from Silverman, Lemma VIII.11.3(b); the bound f₂ ≤ 5 from Barrios–Roy, Theorem 3.7 / Table 7 (taking d=1, applicable because E has a full rational 2-torsion point).

**Remaining for Step 3:** None — this step is closed. The earlier claim "bad reduction exactly at p | abc" holds for odd p; at p = 2 the bad-reduction membership must be determined separately (see e.g. (16,1,17) which is good at 2 despite 2 | abc).

---

### Step 4 — Szpiro-type height-conductor bound (the critical step)

**Status: OPEN.**

A fixed-constant Szpiro bound log|Δ_min(E)| ≤ C_Szp log N_E + O(1) for Frey curves would, via Steps 1–3, give

    2 log c − O(1)  ≤  C_Szp log R + O(1),    i.e.,    log c ≤ (C_Szp/2) log R + O(1).

This is fixed-power weak abc. Via Steps 1–3 and the reverse direction proved below, it would also give Claim OB-01. But:

- This fixed-constant Szpiro bound is open (Pasten Conjectures 1.1–1.2).
- The ordinary discriminant Szpiro conjecture (|Δ_min| ≤ C_ε N_E^{6+ε}) uses exponent 6+ε, not a fixed constant. Via the Frey-curve construction, ordinary Szpiro applied to this family gives only c ≤ K_ε R^{3/2}, not c ≤ K_ε R^{1+ε}, because |Δ_min| ≫ (abc)² ≫ c⁴ on this family.
- The form equivalent to standard abc is **modified Szpiro**: max{|c₄|³, c₆²} ≤ C_ε N_E^{6+ε}. For this Frey family c₄ = 16(a²+ab+b²) ≥ (3/4)c², so the sixth root of the modified bound directly controls c and yields the 1+ε exponent. (Silverman, Proposition VIII.11.5(a) treats modified Szpiro; the ordinary form does not suffice here.)
- Best unconditional result: Stewart–Yu (Duke Math. J. 108 (2001)) gives log c ≤ κ R^{1/3} (log R)³, far from fixed-power.

**What to close for Step 4:** Prove, without assuming abc or Szpiro, that log|Δ_min(E_{a,b,c})| ≤ C_fixed · log N_E + O(1) for a universal constant C_fixed, for all Frey curves. This is equivalent to fixed-power weak abc and is an open problem in the current literature.

**Proved (reverse direction — effective bounded quality implies Claim).** If there exists an effective constant K₀ with log c ≤ K₀ log R for all coprime triples, then Claim OB-01 holds. Proof: the j-invariant satisfies j(E_{a,b,c}) = 256(a²+ab+b²)³ / (abc)², so h(j(E)) ≤ 6 log c + 8 log 2. The unstable discriminant ideal γ divides 2^12 (all odd primes are semi-stable; the 2-adic contribution is bounded by min(v₂(Δ_min), 3v₂(c₄,min)) ≤ 12). By Löbrich, Proposition 3.1 (in Murty–Pasten normalization, shifting by log 4 + (3/2)log π = 3.1034…), this gives h_F(E_{a,b,c}) ≤ (1/2) log c + 3.5387. Substituting log c ≤ K₀ log R and using R ≥ 2 to absorb the additive constant, yields h_F ≤ ((K₀/2) + 3.5387/log 2) log R, which is Claim OB-01 with effective constant. (Independent referee report §6 for full detail.)

---

### Step 5 — Obstruction analysis

**Status: the earlier draft's argument was incorrect; a weaker correct statement follows.**

The correct structural picture is:

1. Steps 1–3 reduce Claim OB-01 to the existence of an effective K with log c ≤ K log R (fixed-power weak abc / bounded quality).
2. Step 4 is exactly this open conjecture.
3. Claim OB-01 does **not** imply standard abc (the ε-absorption argument, referee §1, shows the formulation with unconstrained C_ε cannot achieve 1+ε exponent).

The earlier Step 5 draft argued: "if standard abc fails, one can find a family with q_n → ∞, and then the Szpiro ratio would be unbounded." This is **wrong**: standard abc failing at some fixed ε means c_n / R_n^{1+ε} → ∞, but this does not imply q_n = log c_n / log R_n → ∞ (the log-ratio need not diverge). The claim q_n → ∞ describes failure of fixed-power weak abc, which is a strictly stronger statement.

**What to close for Step 5:** Either (a) exhibit an explicit family of Frey curves where log|Δ_min(E)| / log N_E is unbounded (which would disprove fixed-power weak Szpiro and hence fixed-power weak abc), or (b) prove log|Δ_min(E)| / log N_E ≤ C universally for Frey curves without assuming Szpiro or abc. Either outcome resolves Claim OB-01.

---

## Acceptance criteria

1. **CONFIRMED-PROOF**: A complete proof of h_F(E_{a,b,c}) ≤ K log R for ALL coprime triples (a,b,c), with effective K depending on no abc triples or fitted parameters. (This would establish fixed-power weak abc, an open conjecture.)

2. **CONFIRMED-OBSTRUCTION**: A precise identification of the step where an abc-equivalent or fixed-power-weak-abc-equivalent hypothesis is unavoidable, together with an explicit family showing the Szpiro-type step cannot be closed.

3. **PARTIAL**: A complete proof of one or more of Steps 1–3 (already achieved) with a precise statement of what remains open at Step 4.

4. **INCONCLUSIVE**: A clear statement of the current literature state with references and identification of the open frontier.

**Not accepted:** "This follows from Szpiro's conjecture." "This follows from the abc conjecture." "This is well-known" without citation and proof sketch. "Claim OB-01 implies standard abc" — this is incorrect (see ε-absorption argument, referee §1).

---

## Numerical anchor (sanity only — not an input to the proof)

For (a, b, c) = (1, 8, 9): coprime, 1 + 8 = 9. ✓

- R = rad(1·8·9) = 1·2·3 = 6.
- log R = 1.79176…,  log c = 2.19722…,  q = 1.22629….
- Weierstrass: Δ_W = 16(1·8·9)² = 82944 = 2¹⁰·3⁴; j = 1556068/81.
- The model is already minimal: v₂(Δ_W) = 10 < 12, v₃(c₄) = 0 (multiplicative at 3). So Δ_min = 82944.
- (1/12) log|Δ_min| = 0.9438… — this is the **finite/non-Archimedean contribution only**, not the Faltings height.
- The actual Faltings height depends on normalization:
  - Murty–Pasten normalization: h_F(E_{1,8,9}) ≈ 3.377.
  - Deligne normalization: h_F(E_{1,8,9}) ≈ 0.274.
  The two differ by a fixed normalization constant; neither equals 0.9438.

**Label**: sanity check only. The triple (1,8,9) is not used anywhere in the proof construction. The "sanity check ✓" in earlier drafts used an incorrect identification of 0.9438 with h_F; under the Murty–Pasten normalization h_F ≈ 3.377 > (1+0.5)·log 6 ≈ 2.688, so the inequality in that draft's check does not hold for ε = 0.5 under that normalization — though this has no bearing on the Claim itself since C_ε is unconstrained.
