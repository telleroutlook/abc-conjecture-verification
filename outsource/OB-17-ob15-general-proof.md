# Problem OB-17 — OB-15 for ω*≥4: complete the proof

**Type:** Integer lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter are not assumed. The problem asks to prove a
lattice norm bound for coprime triples satisfying R < c. No abc-equivalent assumption
enters at any point.

---

## Background

**OB-15 (proved for ω*=2 and ω*=3; open for ω*≥4).** For any coprime triple (a,b,c)
with c=a+b and R < c:
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

**ω*=2:** nd ≤ v_max·R (trivial). ✓  
**ω*=3:** Proved by three structural cases — see OB-16 Known cases and Observation 5 in
OB-15. The argument uses: (1) within-group when two same-group primes have unequal vals;
(2) gcd zero-out otherwise. Key: p₂ ≤ p₁·p₃ (p₁≥2, p₃>p₂ distinct primes) ⟹
p₂ ≤ sqrt(p₁·p₂·p₃) = R^{1/2}.  
**ω*≥4:** 53 triples (ω*=4) and 12 triples (ω*=5) verified numerically (c≤5000, 0
violations; max construction ratio 0.28 for ω*=4, 0.54 for ω*=5). Proof incomplete.

---

## All definitions (self-contained)

**Setting.** Coprime a,b>0, c=a+b, gcd(a,b)=1.

**Prime support.** P=Pa∪Pb∪Pc pairwise disjoint: Pa=primes(a), Pb=primes(b), Pc=primes(c).
ω*=|P|.

**Pasten lattice.** F(a,b) = {φ=(φ_p)_{p∈P} ∈ ℤ^P :
Σ_{Pa} v_p(a)φ_p + Σ_{Pb} v_p(b)φ_p = Σ_{Pc} v_p(c)φ_p}.

**Norm.** ‖φ‖ = max_{p∈P} p|φ_p|.

**Wronskian.** W(φ) = Σ_{Pb} φ_p − Σ_{Pa} φ_p.

**Non-degenerate minimum.** nd(a,b) = min{‖φ‖ : φ∈F(a,b), W(φ)≠0}.

**v_max.** v_max = max_{p∈P} v_p(abc). Since R<c implies c non-squarefree (proved in
OB-15 Observation 1'), **v_max ≥ 2** for all R<c triples.

**R = ∏_{p∈P} p** (product of distinct prime factors of abc).

---

## Known structural facts (do not re-derive)

**F1 (v_max≥2).** R<c ⟹ c composite non-squarefree ⟹ v_max≥2.

**F2 (within-group construction).** If group G∈{Pa,Pb,Pc} contains primes p<q with
v_p(g)≠v_q(g): φ_p=v_q/gcd, φ_q=−v_p/gcd (all others 0) is non-degenerate when G≠Pc,
with ‖φ‖ = max(p·v_q, q·v_p)/gcd ≤ v_max·q.

**F3 (zero-out construction).** For any triple with groups Pa={p^α}, Pb={q^β}, Pc={r^γ}
(single prime per group, ω*=3): φ_r=0, φ_p=β/g, φ_q=−α/g gives nd ≤ v_max·q ≤
v_max·R^{1/2} (proved in OB-15 Observation 5, Case A).

**F4 (ω*=3 fully proved).** Theorem: for all R<c triples with ω*=3,
nd(a,b) ≤ v_max·R^{1/2}. Proof covers all three structural types; see OB-15/OB-16.

---

## The claim to be proved

**Theorem OB-17.** For any coprime triple (a,b,c) with R<c and ω*≥4:
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

---

## Proof skeleton to be closed

### Strategy A — Within-group bound (covers ~90% of cases)

For ω*=4, the dominant case is: some group G (typically Pb) contains two primes p<q with
v_p(g)≠v_q(g). By F2, nd ≤ v_max·q. So OB-17 reduces to:

$$q \;\leq\; v_{\max} \cdot R^{1/3} \qquad \Longleftrightarrow \qquad q^3 \leq v_{\max}^3 \cdot p_1 p_2 p_3 p_4 \tag{KEY-4}$$

where {p₁,p₂,p₃,p₄} = P (the 4 distinct primes), and q ≤ p₄ = max prime.

**Case (KEY-4) with single-prime Pc={s^γ}, γ≥2 (dominant sub-case):**

From R < c = s^γ: p₁p₂p₃ < s^{γ−1}.  
For γ=2: s > p₁p₂q (taking p₁p₂p₃ = p₁p₂q for the 3 non-Pc primes).

Using F1 (v_max≥2):  
v_max^3·p₁p₂s > 8·p₁p₂·p₁p₂q = 8(p₁p₂)²q.  
For p₁=2,p₂=3: 8·36q = 288q. So KEY-4 holds when q ≤ 288.

**Open gap:** For q>288 with p₁=2,p₂=3 and γ=2 (s>6q), the bound 288q may fall below
q². Candidates: q∈{293,307,...}. However, for such q, the abc equation
p₁^α + p₂^β·q^δ = s^2 with s>6q imposes strong congruence conditions — either v_max≥3
(from the large exponent needed to make the equation work) or p₁p₂ > 6 (larger base
primes in Pa/Pb). Close KEY-4 by:
(a) Showing no valid R<c triple with q>288 and v_max=2 and p₁p₂=6 exists, OR
(b) Proving v_max ≥ q^{1/3}/C for some absolute constant C in this regime, OR
(c) Finding an alternative construction (cross-group or parameterised) bypassing KEY-4.

### Strategy B — Cross-group for equal-valuation groups (5 ω*=4 triples, c≤5000)

For the 5 ω*=4 triples where some group has equal-valuation primes, within-group is
degenerate and cross-group constructions are used. All 5 are verified numerically (max
ratio 0.27). The general proof for this sub-case follows the method of OB-16 Step 2.

### Strategy C — General ω*≥5

For ω*=5,6,...: the R<c triples always have a group with multiple primes having unequal
valuations (verified for c≤5000; 12 triples at ω*=5 all use within-group). The bound
analogous to KEY-4 is:
q^{ω*−1} ≤ v_max^{ω*−1} · p₁p₂...p_{ω*},
which becomes easier as ω* grows (more primes in R multiply together).

The inductive step: for ω*=k+1, the (k+1)-prime case reduces to a k-prime case by
zeroing one group and using the ω*=k result on the remainder.

---

## Acceptance criteria

1. **CONFIRMED-4:** Complete proof of KEY-4 for all ω*=4 R<c triples.
2. **CONFIRMED-GENERAL:** Proof of OB-17 for all ω*≥4 by induction or uniform argument.
3. **CONDITIONAL-4:** Proof of KEY-4 assuming a named auxiliary hypothesis (prime gap,
   Bertrand-type, or congruence condition).
4. **PARTIAL:** Proof for all ω*=4 triples with p₁p₂≥10 (covers all but p₁=2,p₂=3).
5. **REFUTED:** Explicit R<c triple with ω*≥4 and nd(a,b) > v_max·R^{1/(ω*-1)}.
6. **INCONCLUSIVE:** Precise localization of which sub-case (q-range, group type)
   resists the proof, with the exact numerical threshold.

---

## Numerical anchors (c≤5000, 0 violations across ω*=3,4,5)

**ω*=4 worst-ratio cases (verified, construction-based; ratios << 1):**

| (a,b,c) | fa | fb | fc | ω* | v_max | R | bound | nd_ub | ratio |
|---------|----|----|----|----|-------|---|-------|-------|-------|
| (128,2997,3125) | {2:7} | {3:4,37:1} | {5:5} | 4 | 7 | 1110 | 72.5 | 20 | 0.28 |
| (243,1088,1331) | {3:5} | {2:6,17:1} | {11:3} | 4 | 6 | 1122 | 62.4 | 17 | 0.27 |
| (100,243,343) | {2:2,5:2} | {3:5} | {7:3} | 4 | 5 | 210 | 29.7 | 8 | 0.27 |
| (1024,2187,3211) | {2:10} | {3:7} | {13:2,19:1} | 4 | 10 | 1482 | 114.0 | 30 | 0.26 |

For each: verified nd_ub ≤ bound by explicit construction. No OB-17 violation found.

**KEY-4 check for top ratio case (128,2997,3125):**
q = 37 (within-group pair Pb={3^4,37^1}; within-group norm = max(3·1,37·4)=148, too large).
Actual nd_ub=20 via cross-group: φ_2=0, φ_3=5, φ_37=0, φ_5=4. Constraint: 4·5+0=20=5·4 ✓.
W=φ_3+φ_37=5≠0. ‖φ‖=max(0,15,0,20)=20 ≤ 72.5 ✓.
v_max=7 (from v_2(a)=7); KEY-4 holds: v_max³·p₁p₂s = 7³·2·3·5 = 10,290 > 37²=1,369 ✓.
Note: within-group is not the tightest construction here; the bound is still satisfied.

Script: `discovery/m2_directions/ob15_gap2_power_triples.py`
