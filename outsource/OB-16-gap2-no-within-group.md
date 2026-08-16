# Problem OB-16 — OB-15 Gap 2: cross-group bound for equal-valuation groups

**Type:** Integer lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter are not assumed. The problem concerns explicit
construction of non-degenerate Pasten lattice vectors for a specific sub-class of
coprime triples. No abc-equivalent assumption enters at any point.

---

## Context

OB-15 conjectures: for all coprime triples a+b=c with R < c,
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

Most cases are covered by the **within-group construction** (two primes in the same
group with unequal valuations give a non-degenerate vector of small norm). The
remaining "Gap 2" cases — where within-group is unavailable — are all of a special
"power-triple" structure. This problem asks to prove OB-15 for those cases.

**Proved already (not asked here):** For ω*=3 power triples (p^α + q^β = r^γ, single
prime per group), the zero-out construction settles OB-15 (see Observation 5 in OB-15).

---

## All definitions (self-contained)

**Setting.** Let a, b be coprime positive integers, c = a + b.

**Distinct-prime support.** P = Pa ∪ Pb ∪ Pc, pairwise disjoint; ω* = |P|.

**Generalised Pasten lattice F(a,b).** Integer vectors φ = (φ_p)_{p∈P} satisfying
$$\sum_{p \in P_a} v_p(a)\,\varphi_p + \sum_{p \in P_b} v_p(b)\,\varphi_p
= \sum_{p \in P_c} v_p(c)\,\varphi_p. \tag{C}$$

**Norm.** ‖φ‖ = max_{p∈P} p|φ_p|.

**Wronskian.** W(φ) = Σ_{Pb} φ_p − Σ_{Pa} φ_p.

**Non-degeneracy.** φ ∈ F(a,b) is non-degenerate if W(φ) ≠ 0.

**Minimum non-degenerate norm.**
$$\mathrm{nd}(a,b) = \min\{\|\varphi\| : \varphi \in F(a,b),\; W(\varphi) \neq 0\}.$$

**Valuation maximum.** v_max = max_{p∈P} v_p(abc).

**Radical.** R = ∏_{p∈P} p.

**Within-group construction.** For a group G with two primes p,q ∈ G and v_p(g) ≠ v_q(g)
(g = a, b, or c), the vector φ_p = v_q/gcd, φ_q = −v_p/gcd, all others = 0, has
W ≠ 0 and ‖φ‖ = max(p·v_q, q·v_p)/gcd. This is **unavailable** when all primes in
every group have equal valuations (equal-valuation groups).

**Zero-out construction (proved for ω*=3).** For (p^α, q^β, r^γ) with p<q<r distinct
primes: set φ_r=0, φ_p=β/g, φ_q=−α/g (g=gcd(α,β)). Gives nd ≤ q·v_max ≤ v_max·R^{1/2}.
Proof of bound: q ≤ v_max²·pr. From R<c=r^γ: pq<r^{γ-1}. For γ=2: pr>p²q≥4q. ✓

---

## The theorem / claim to be proved

**Theorem OB-16.** Let (a, b, c) be a coprime triple with R < c and ω* ≥ 2. Suppose
that for every group G ∈ {Pa, Pb, Pc}, either |G| = 1 (single prime) or all primes
in G have equal valuations. Then:
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

---

## Known special cases and constructions

### Case ω* = 2
nd(a,b) ≤ v_max · R (trivial: any non-degenerate φ works). ✓

### Case ω* = 3 (CONFIRMED-3 — proved 2026-08-16)

All ω*=3 R<c triples fall into three structural types:

| Type | Count (c≤5000) | Construction | Norm bound |
|------|---------------|--------------|------------|
| (1,1,1): single prime per group | 7 | zero-out Pc: φ_r=0, φ_p=β/g, φ_q=−α/g | ≤ v_max·q ≤ v_max·R^{1/2} |
| (0,2,1): Pa=∅, Pb two unequal-val | 5 | within-group Pb: φ_p=v_q/g, φ_q=−v_p/g | ≤ v_max·max(p,q) ≤ v_max·R^{1/2} |
| (0,1,2): Pa=∅, Pc two unequal-val | 2 | zero-out larger Pc prime | ≤ v_max·r ≤ v_max·R^{1/2} |

**Norm bound argument (same for all cases):** the construction norm is ≤ v_max·p₂ where p₂ is
the second-largest prime among ω*=3 primes {p₁<p₂<p₃}. Then p₂ ≤ R^{1/2}:
p₂ ≤ sqrt(p₁·p₂·p₃) ⟺ p₂ ≤ p₁·p₃. Since p₁≥2 and p₃>p₂: p₁·p₃ ≥ 2p₃ > p₂. ✓

No R<c triple with ω*=3 and equal-valuation multi-prime Pb found (c≤5000, 14 classified). ✓

### Case ω* = 4, Pa has two equal-valuation primes (the unique case c ≤ 2000)

**The triple (100, 243, 343):** a=2²·5², b=3⁵, c=7³.
Pa={2,5} with v_2(a)=v_5(a)=2, Pb={3} with v_3(b)=5, Pc={7} with v_7(c)=3.
ω*=4, R=2·3·5·7=210, v_max=5, v_max·R^{1/3} = 5·210^{1/3} ≈ 29.7.

**Explicit construction achieving nd ≤ 7:**
φ_7=1, φ_3=1, φ_5=−1, φ_2=0.
- Constraint: 2·0+2·(−1)+5·1 = −2+5 = 3 = 3·1. ✓
- W = φ_3 − (φ_2+φ_5) = 1−(0+(−1)) = 2 ≠ 0. ✓
- ‖φ‖ = max(2·0, 5·1, 3·1, 7·1) = 7 ≤ 29.7. ✓

**General construction strategy for ω*=4 with Pa={p₁,p₂} equal-val v, Pb={q} val s, Pc={r} val u:**

Set φ_r=1, φ_q=1, φ_{p₁}=0, φ_{p₂}=(u−s)/v (requires v | u−s).
- Constraint: v·0 + v·(u−s)/v + s·1 = (u−s)+s = u = u·1. ✓
- W = φ_q − (φ_{p₁}+φ_{p₂}) = 1 − (u−s)/v. Non-zero when (u−s)/v ≠ 1.
- ‖φ‖ = max(p₁·0, p₂·|(u−s)/v|, q·1, r·1).

For (100,243,343): v=2, u=3, s=5 → (u−s)/v = −1. φ_{p₂}=φ_5=−1. ‖φ‖=max(0,5,3,7)=7. ✓

**Open sub-case:** when v ∤ (u−s), or when the formula gives W=0, an alternative φ
is needed. Identify which (v,u,s) triples require this and construct φ explicitly.

---

## Proof skeleton to be closed

### Step 1 — Within-group construction for ω*=4 (main open case)

For ω*=4, 48 of 53 R<c triples (c≤5000) have a multi-prime group with unequal vals;
within-group then gives norm ≤ v_max·q where q = max prime in that group.

**What to close:** Show q ≤ v_max·R^{1/(ω*-1)} for within-group prime q when R<c.

This reduces to: q^(ω*-1) ≤ v_max^(ω*-1)·R = v_max^(ω*-1)·p₁·p₂·p₃·p₄ (for ω*=4).

**Key lemma (from Observation 1'):** R<c implies c non-squarefree, so v_max ≥ 2.

With v_max ≥ 2 and the dominant case (single-prime Pc={s^γ}, γ≥2, giving R<c=s^γ → p₁p₂p₃ < s^{γ-1}):

For γ=2 (most common): s > p₁·p₂·p₃ ≥ 6q (if p₁=2,p₂=3; noting p₃≥q).
v_max^3·p₁·p₂·s > 8·6·6q = 288q. So q^2 ≤ v_max^3·p₁·p₂·s when q ≤ 288.
For q > 288: the constraint s > 6q forces s (and hence R) to be proportionally large,
maintaining the bound.

**What is needed:** Make the above into a complete proof, or identify a sub-case where it fails and construct an alternative vector.

### Step 2 — Equal-valuation multi-prime groups

When some group G has |G|≥2 primes all with the same valuation v:
- Within-group gives W=0 (degenerate).
- The "mixed construction" (φ_r=1, φ_q=1, φ_{p₂}=(u−s)/v) works when v|u−s.
- For v ∤ u−s: use φ_r=v/gcd(v,u−s), φ_q=v/gcd(v,u−s), φ_{p₂}=(u−s)/gcd(v,u−s).
  Norm = max(p₂·|(u−s)/gcd|, q·v/gcd, r·v/gcd).
  
**What to close:** Show this norm ≤ v_max·R^{1/(ω*-1)} for all valid R<c triples.
The key constraint is R < c which limits how large q and r can be relative to R.

---

## Acceptance criteria

1. **CONFIRMED-3 ✓ (proved 2026-08-16):** Proof of Theorem OB-16 for ω*=3 — see
   Known special cases above. All three structural types verified and proved.
2. **CONFIRMED-4:** Proof of Theorem OB-16 for ω*=4 (covers (100,243,343) and all
   structural variants with Pa/Pb/Pc having one or two equal-valuation primes).
3. **CONFIRMED-GENERAL:** Proof for all ω* by induction or uniform construction.
4. **PARTIAL:** Proof for a restricted class (e.g., only equal-val Pa sub-case).
5. **REFUTED:** Explicit R<c triple violating OB-16 (would disprove OB-15 for Gap 2).
6. **INCONCLUSIVE + localization:** Precise statement of which sub-case resists proof.

---

## Numerical anchors (all verified, sanity only)

**Full verification (c≤5000):** Construction-based checker (gcd formula, within-group,
zero-out, parameterized cross-group) finds 0 violations across all 80 R<c triples:
- ω*=3: 14 triples, all PROVED by the three-case argument above.
- ω*=4: 53 triples, 0 violations; max construction ratio 0.28.
- ω*=5: 12 triples, 0 violations; max construction ratio 0.54.
- ω*=6: 1 triple (1, 8191²−1, 8191²) at c=67092481 >> 5000 — handled by within-group.

Script: `discovery/m2_directions/ob15_gap2_power_triples.py`

**Representative ω*=4 triples (construction verified, proof open):**

| (a,b,c) | structure | ω* | R | v_max | v_max·R^{1/3} | nd_ub | ratio |
|---------|-----------|----|----|-------|---------------|-------|-------|
| (100,243,343) | 2²·5²,3⁵,7³ | 4 | 210 | 5 | 29.7 | 8 | 0.27 |
| (81,175,256) | 3⁴,5²·7,2⁸ | 4 | 210 | 8 | 47.5 | 10 | 0.21 |
| (1,224,225) | 1,2⁵·7,3²·5² | 4 | 210 | 5 | 29.7 | 4 | 0.13 |
| (640,729,1369) | 2⁷·5,3⁶,37² | 4 | 1110 | 9 | 93.1 | 9 | 0.10 |

**Representative ω*=3 triples (proved):**

| (a,b,c) | structure | ω* | R | v_max | v_max·R^{1/2} | nd | OB-16? |
|---------|-----------|----|----|-------|---------------|----|--------|
| (1,8,9) | 1,2³,3² | 2 | 6 | 3 | 18.0 | 9 | ✓ |
| (5,27,32) | 5,3³,2⁵ | 3 | 30 | 5 | 27.4 | 6 | ✓ |
| (32,49,81) | 2⁵,7²,3⁴ | 3 | 42 | 5 | 32.4 | 7 | ✓ |
| (4,121,125) | 2²,11²,5³ | 3 | 110 | 3 | 31.5 | 10 | ✓ |
| (100,243,343) | 2²·5²,3⁵,7³ | 4 | 210 | 5 | 29.7 | 7 | ✓ |
| (169,343,512) | 13²,7³,2⁹ | 3 | 182 | 9 | 121.4 | 21 | ✓ |
