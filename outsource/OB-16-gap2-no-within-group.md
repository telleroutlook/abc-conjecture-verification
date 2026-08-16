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

### Case ω* = 3 (power triples p^α + q^β = r^γ, p < q < r)
Zero-out construction: φ_r=0, φ_p=β/g, φ_q=−α/g. Proved above. ✓

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

### Step 1 — General construction for single-prime-per-group (ω* ≥ 3)

For any k groups each containing a single prime p₁<p₂<...<p_k (with valuations
v₁,...,v_k and the respective group signs in constraint):

**Zero-out the largest prime p_k.** Set φ_{p_k}=0 and solve the (k−1)-variable
linear Diophantine equation. The resulting norm is bounded by max(p₁,...,p_{k-1})·v_max.

**What to close:** Show max(p₁,...,p_{k-1})·v_max ≤ v_max·R^{1/(ω*-1)},
i.e., p_{k-1} ≤ R^{1/(ω*-1)}.

The key inequality p_{k-1}^{ω*-1} ≤ R = p₁·p₂·...·p_k follows from:
R < c = p_k^{γ} → p₁·...·p_{k-1} < p_k^{γ-1}.
Then p_{k-1}^{ω*-1} ≤ (p₁·...·p_{k-1})·p_{k-1}^{ω*-1−(k-1)}... 
*(Requires completing the inductive argument for ω*≥4.)*

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

1. **CONFIRMED-3:** Proof of Theorem OB-16 for ω*=3 (already proved, included for
   completeness; verify the zero-out argument is water-tight).
2. **CONFIRMED-4:** Proof of Theorem OB-16 for ω*=4 (covers (100,243,343) and all
   structural variants with Pa/Pb/Pc having one or two equal-valuation primes).
3. **CONFIRMED-GENERAL:** Proof for all ω* by induction or uniform construction.
4. **PARTIAL:** Proof for a restricted class (e.g., all triples with Pa=∅ only).
5. **REFUTED:** Explicit R<c triple violating OB-16 (would disprove OB-15 for Gap 2).
6. **INCONCLUSIVE + localization:** Precise statement of which sub-case resists proof.

---

## Numerical anchors (all verified, sanity only)

| (a,b,c) | structure | ω* | R | v_max | v_max·R^{1/(ω*-1)} | nd | OB-16? |
|---------|-----------|----|----|-------|--------------------|----|--------|
| (1,8,9) | 1,2³,3² | 2 | 6 | 3 | 18.0 | 9 | ✓ |
| (5,27,32) | 5,3³,2⁵ | 3 | 30 | 5 | 27.4 | 6 | ✓ |
| (32,49,81) | 2⁵,7²,3⁴ | 3 | 42 | 5 | 32.4 | 7 | ✓ |
| (4,121,125) | 2²,11²,5³ | 3 | 110 | 3 | 31.5 | 10 | ✓ |
| (3,125,128) | 3,5³,2⁷ | 3 | 30 | 7 | 38.3 | 9 | ✓ |
| (13,243,256) | 13,3⁵,2⁸ | 3 | 78 | 8 | 70.7 | 13 | ✓ |
| (100,243,343) | 2²·5²,3⁵,7³ | 4 | 210 | 5 | 29.7 | 7 | ✓ |
| (169,343,512) | 13²,7³,2⁹ | 3 | 182 | 9 | 121.4 | 21 | ✓ |

Script: `discovery/m2_directions/ob15_gap2_power_triples.py`.
