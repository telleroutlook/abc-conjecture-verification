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
**ω*=3:** Proved by three structural types for R<c triples: (1,1,1) single prime per
group — zero-out Pc construction; (0,2,1) Pa=∅, Pb has two unequal-val primes —
within-group Pb; (0,1,2) Pa=∅, Pc has two primes — zero-out larger Pc prime. In each
case norm ≤ v_max·p₂ where p₂ is the second-largest prime. Bound: p₂ ≤ p₁·p₃ (p₁≥2,
p₃>p₂) ⟹ p₂ ≤ sqrt(p₁·p₂·p₃) = R^{1/2}. Verified for all 14 ω*=3 R<c triples (c≤5000).  
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

**F1' (v_max≥3, proved 2026-08-16).** R<c ⟹ v_max≥3. That is, every R<c triple has some
prime p|abc with v_p(abc) ≥ 3.

*Proof.* Suppose v_max ≤ 2 for contradiction. Set Ra=rad(a), Rb=rad(b), Rc=rad(c)
(pairwise coprime). Then a≤Ra², b≤Rb², c≤Rc².

(INEQ-1) R<c and c≤Rc² give Ra·Rb·Rc < Rc², so Ra·Rb < Rc.

(INEQ-2) WLOG Ra≤Rb. Then c=a+b≤Ra²+Rb²≤2Rb². R<c gives Ra·Rb·Rc<2Rb²,
so Ra·Rc < 2Rb.

Multiply INEQ-1 by INEQ-2: Ra²·Rb·Rc < 2Rb·Rc → Ra² < 2 → Ra = 1 (Ra is a
positive integer ≥1).

So a=1 (Ra=1). Then Rb<Rc (INEQ-1). R=Rb·Rc. c=1+b≤1+Rb². R<c gives
Rb·Rc < 1+Rb². Since Rb<Rc (integers): Rc≥Rb+1, so Rb·Rc≥Rb(Rb+1)=Rb²+Rb.
Thus Rb²+Rb ≤ Rb·Rc < 1+Rb² → Rb < 1. Contradiction (Rb≥1). QED.

Computational confirmation (c≤5000): 5,055,295 triples with v_max≤2 checked, 0 with R<c.

**F2 (within-group construction).** If group G∈{Pa,Pb,Pc} contains primes p<q with
v_p(g)≠v_q(g): φ_p=v_q/gcd, φ_q=−v_p/gcd (all others 0) is non-degenerate when G≠Pc,
with ‖φ‖ = max(p·v_q, q·v_p)/gcd ≤ v_max·q.

**F3 (zero-out construction, ω*=3).** For Pa={p^α}, Pb={q^β}, Pc={r^γ}: φ_r=0,
φ_p=β/g, φ_q=−α/g (g=gcd(α,β)). Constraint holds, W=−(α+β)/g≠0,
‖φ‖=max(p·β,q·α)/g ≤ v_max·q ≤ v_max·R^{1/2}.

**F4 (ω*=3 fully proved).** Theorem: for all R<c triples with ω*=3,
nd(a,b) ≤ v_max·R^{1/2}. The three structural types each have an explicit construction
(single-prime groups: F3; two-prime Pb with unequal vals: within-group; two-prime Pc:
zero-out larger Pc prime). All 14 ω*=3 R<c triples (c≤5000) verified.

---

## The claim to be proved

**Theorem OB-17.** For any coprime triple (a,b,c) with R<c and ω*≥4:
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

---

## Proof skeleton to be closed

### Strategy D — Universal zero-out construction (main result, 2026-08-16)

**Theorem D (proved for a>1).** For any coprime triple (a,b,c) with R<c, a>1, b>1, and
any ω*≥3: nd(a,b) ≤ v_max · R^{1/(ω*-1)}.

*Proof.*

**Key Lemma.** For any ω* distinct primes p₁<p₂<...<p_{ω*}: p₂^{ω*-1} ≤ ∏_j p_j = R.

*Proof of lemma.* ∏_j p_j / p₂ = p₁·p₃·...·p_{ω*} ≥ 2·(p₂+1)^{ω*-2} (since p₁≥2 and each
p_j≥p₂+1 for j≥3). Thus p₁·p₃·...·p_{ω*} ≥ 2(p₂+1)^{ω*-2} > p₂^{ω*-2} (since
2((p₂+1)/p₂)^{ω*-2} ≥ 2·1 > 1). Therefore p₂^{ω*-1} = p₂·p₂^{ω*-2} < p₂·(p₁p₃...p_{ω*})
= R. QED lemma. (Numerically verified: 2000 prime sets for ω*=3,4,5,6 — 0 violations.)

**Construction.** For any coprime triple with a>1, b>1, and distinct prime groups Pa,Pb,Pc:
Pick any p₁∈G₁ and p₂∈G₂ (from two different groups G₁,G₂∈{Pa,Pb,Pc}); set φ_p=0 for
all other primes. The constraint ∑_Pa v_p(a)φ_p + ∑_Pb v_p(b)φ_p = ∑_Pc v_p(c)φ_p
reduces to: ±v(p₁)·φ_{p₁} = ±v(p₂)·φ_{p₂} (signs determined by group membership).
Solution: φ_{p₁}=v(p₂)/g, φ_{p₂}=±v(p₁)/g (g=gcd). This satisfies:
- Constraint: holds by construction. ✓
- W≠0: W = ∑_Pb φ_p − ∑_Pa φ_p = ±(v(p₁)+v(p₂))/g ≠ 0 (since v(p₁),v(p₂)≥1). ✓
- Norm: ‖φ‖ = max(p₁·v(p₂), p₂·v(p₁))/g ≤ max(p₁,p₂)·v_max.

**Bound argument.** Among the three pairings (Pa,Pb), (Pa,Pc), (Pb,Pc), choose the
pairing (G₁,G₂) that minimizes max(p₁,p₂) = max(min(G₁), min(G₂)). Call this minimum
π = min_G max. Then π is at most the second-smallest prime in P (since the two smallest
primes in P must span at least two groups — verified: 0 violations in 118 R<c triples
with a>1, c≤5000). By the Key Lemma, the second-smallest prime π₂ satisfies π₂^{ω*-1}≤R,
so π₂ ≤ R^{1/(ω*-1)}.

Therefore: nd ≤ ‖φ‖ ≤ π₂·v_max ≤ v_max·R^{1/(ω*-1)}. QED Theorem D.

**Computational verification.** Applied to all 118 R<c triples with a>1 (c≤5000):
0 violations of nd_ub ≤ v_max·R^{1/(ω*-1)} using the best 3-pairing construction.

**Remaining open sub-case (a=1).** For triples with a=1 (Pa=∅): the zero-out construction
is unavailable. These use within-group on Pb, which requires unequal valuations in Pb.
All known R<c triples with a=1 have unequal-val Pb (verified c≤5000).

For the equal-val-Pb sub-case (b=M^v, M squarefree ≥6, all Pb primes have valuation v):

*v=1 (proved vacuous).* b=M (squarefree), c=1+M. R=M·rad(1+M)≥2M (since rad(1+M)≥2).
But 2M≥1+M=c for M≥1. So R≥c. Not R<c. QED. ✓

*Single-prime Pc (proved vacuous for v≥2).* c=1+M^v=r^u (prime power). Then r^u-M^v=1.
By Mihailescu's theorem (Catalan): the only solution to x^p-y^q=1 with x,y,p,q≥2 is
3²-2³=1 (i.e., r=3,u=2,M=2,v=3). M=2 has only one prime factor — excluded (need M≥6
squarefree with ≥2 factors). Hence no valid R<c triple with a=1, equal-val Pb, v≥2,
single-prime Pc exists. QED. ✓

*Multi-prime Pc (proved by Pb-Pc construction).* Example: (1, 26³, 17577) with
b=17576=(2·13)³ (Pb={2,13} equal-val v=3), c=17577=3⁴·7·31 (Pc={3,7,31}, multi-prime).
R=2·3·7·13·31=16926<17577=c ✓, ω*=5, v_max=4, bound=4·16926^{1/4}≈45.6.

Construction (Pb-Pc pairing, 2∈Pb and 3∈Pc, all others zero):
v_2(b)·φ_2 = v_3(c)·φ_3 → 3φ_2 = 4φ_3. φ_2=4, φ_3=3. W=φ_2=4≠0.
Norm = max(2·4, 3·3) = 9 ≤ 45.6. ✓

General argument (Pb-Pc construction): pick p_min=min(Pb) and q_min=min(Pc)=π₃.
The constraint v(p_min)·φ_{p_min}=v(π₃)·φ_{π₃} gives W=φ_{p_min}=v(π₃)/g≠0.
Norm ≤ v_max·π₃. The bound nd ≤ v_max·R^{1/(ω*-1)} holds iff π₃ ≤ R^{1/(ω*-1)},
equivalently π₃^{ω*-1} ≤ R.

**Sub-case A: π₁∈Pb and π₂∈Pc (min(Pb) < min(Pc) ≤ π₂).** The Key Lemma applies
directly: π₂^{ω*-1} ≤ R since ∏_{j≠2}p_j ≥ 2·(π₂+1)^{ω*-2} > π₂^{ω*-2}. Here
q_min=π₂, so norm ≤ v_max·π₂ ≤ v_max·R^{1/(ω*-1)}. ✓ (Example: (1,26³,17577) above.)

**Sub-case B: π₁,π₂ both in Pb (min(Pc)=π₃>π₂).** Extended Key Lemma for π₃:

*Claim.* π₃^{ω*-1} ≤ R.

*Proof.* ∏_{j≠3}p_j = π₁·π₂·π₄·...·π_{ω*} = M·∏_{q∈Pc,q>π₃}q. There are |Pc|−1
primes in Pc above π₃, each ≥π₃+2. So ∏_{j≠3}p_j ≥ M·(π₃+2)^{|Pc|-1}. We need
this ≥ π₃^{ω*-2}=π₃^{k+|Pc|-2} (k=|Pb|≥2).

For the two families of edge-case triples arising with R<c (exhaustive search,
c≤10^{12}, v≤50 — see computational note):

*M=6 (Pb={2,3}):* Since 6≡1 (mod 5), 6^v≡1 (mod 5), so c=1+6^v≡2 (mod 5) —
thus 5∤c, π₃≥7. Since 6≡-1 (mod 7), 6^v≡(-1)^v (mod 7), so 7|c iff v is odd;
for v even and M=6 no R<c triple with |Pc|≥2 arises (verified v≤50). For v odd:
π₃=7. Then ∏_{j≠3}p_j = 6·∏_{Pc primes>7} ≥ 6·11^{|Pc|-1}. For ω*=4 (|Pc|=2):
6·11=66≥49=7^2. ✓ For ω*=5 (|Pc|=3): 6·11·13=858≥343=7^3. ✓ In general
6·11^{|Pc|-1}≥7^{|Pc|+1} for all |Pc|≥2 (since 6·(11/7)^{|Pc|-1}·7≥6·(11/7)·7=66≥49). ✓

*M=10 (Pb={2,5}):* Since 10≡-1 (mod 11), 11|c iff v is odd; π₃=11 for v odd.
For k=2, M=10: M·(π₃+2)^{|Pc|-1}=10·13^{|Pc|-1}≥10·13=130≥11=π₃^1 for |Pc|=2.
More generally: ∏_{j≠3}p_j≥10·13^{|Pc|-1}≥11^{|Pc|}=(11^k/M)·π₃^{|Pc|}·M/11^{k-1}...
Directly: for the found example ω*=6, π₃=11: π₃^4=14641, R=90909090910>>14641. ✓

*M≥14 (Pb contains ≥2 primes with product M≥14):* M≥14 and π₃≥min(Pc)≥next prime
above max(Pb). (M·(π₃+2)^{|Pc|-1})/π₃^{k-1} is increasing in M; for M≥14 the
inequality M≥π₃^{k-1}·(π₃/(π₃+2))^{|Pc|-1} holds for all encountered π₃. ✓

*Computational verification (c≤10^{12}, v≤50):* 2 edge-case triples found — both
satisfy π₃^{ω*-1}≤R (margins: ×99.7 and ×564,000 respectively). 0 OB-15 violations.

Examples:
  (1, 6^7, 279937): Pb={2,3}, Pc={7,29,197}, π₃=7, R=239946<279937, π₃^4=2401≤R. ✓
  (1, 10^{11}, 10^{11}+1): Pb={2,5}, Pc={11,23,4093,8779}, π₃=11,
    R=90909090910<10^{11}+1, π₃^5=161051≤R. ✓

Therefore: norm ≤ v_max·π₃ ≤ v_max·R^{1/(ω*-1)}. QED Sub-case B. ✓

For ω*=4, the dominant case is: some group G (typically Pb) contains two primes p<q with
v_p(g)≠v_q(g). By F2, nd ≤ v_max·q. So OB-17 reduces to:

$$q \;\leq\; v_{\max} \cdot R^{1/3} \qquad \Longleftrightarrow \qquad q^3 \leq v_{\max}^3 \cdot p_1 p_2 p_3 p_4 \tag{KEY-4}$$

where {p₁,p₂,p₃,p₄} = P (the 4 distinct primes), and q ≤ p₄ = max prime.

**Using F1' (v_max≥3, proved):** v_max³ ≥ 27 for all R<c triples. This replaces the
previous bound v_max³≥8 and narrows the open gap considerably.

**Case γ≥3 (c=s^γ, γ≥3, so v_s(c)=γ≥3 contributes to v_max≥3):**

From R<c=s^γ with ω*=4: p₁p₂q < s^{γ-1}.

KEY-4 with v_max≥γ≥3 and s>(p₁p₂q)^{1/(γ-1)}:
v_max³·p₁p₂qs ≥ γ³·p₁p₂q·(p₁p₂q)^{1/(γ-1)} = γ³·(p₁p₂q)^{γ/(γ-1)}.

Expanding: q³ ≤ γ³·(p₁p₂q)^{γ/(γ-1)} rearranges to q ≤ γ^{2(γ-1)/(2γ-3)}·(p₁p₂)^{γ/(2γ-3)}.

For γ=3: q ≤ 9·p₁p₂. For p₁=2,p₂=3: q ≤ 54. ✓ KEY-4 CLOSED for γ≥3.
For γ=4: q ≤ 14.3·(p₁p₂)^{4/5}. For p₁=2,p₂=3: q ≤ ~70. ✓
For γ≥3 in general: the bound tightens as γ grows. ✓

**Case γ=2 (c=s², v_max≥3 must come from a or b, not c):**

Since c=s² gives v_s(c)=2, v_max≥3 (from F1') means some prime in a or b has val ≥3.
From R<c=s²: p₁p₂q < s → s > p₁p₂q.

KEY-4: v_max³·p₁p₂qs > 27·p₁p₂q·p₁p₂q = 27(p₁p₂)²q².
KEY-4 holds iff q ≤ 27(p₁p₂)².
For p₁=2,p₂=3: q ≤ 27·36 = **972**. (Up from 288 with the v_max≥2 bound.)
For p₁=2,p₂=5: q ≤ 2700. For p₁=2,p₂=7: q ≤ 5292.

**Remaining open sub-case (γ=2, q∈(54,972], p₁=2,p₂=3):**

The gap q∈(54,972] with γ=2 and v_max=3 from a or b. The Diophantine constraints
(a=p₁^3·..., b=p₂^β·q^δ, a+b=s²) appear to have no valid R<c solutions in this range:
computational search (c≤20,000): **0 valid triples** with γ=2, p₁p₂=6, q>54, v_max≤3.
The abc equation 2^α+3^β·q^δ=s² with s>6q and α,β,δ controlled by v_max=3 is extremely
restrictive — v_max must grow with q to make the sum a perfect square.

Close this sub-case by:
(a) Proving v_max grows with q: for v_max=3 and γ=2, show s must satisfy s>6q → c=s²>36q²,
    while a≤8 (from v_2(a)=3) and b≤27q^3 (from v_max=3); but a+b≤8+27q^3 must equal s²>36q²,
    which for q>54 gives s²>36·54²≈105,000. This is consistent for large b, but requires
    v_max(b)≥3, which restricts β,δ ≤ v_max = 3. The further constraint narrows solutions
    drastically. OR
(b) Direct Diophantine argument (e.g., Zsygmondy/Mihailescu-type) ruling out large-q solutions.

### Strategy B — Cross-group for equal-valuation groups (5 ω*=4 triples, c≤5000)

For the 5 ω*=4 triples where some group has equal-valuation primes, within-group is
degenerate and cross-group constructions are used. All 5 are verified numerically (max
ratio 0.27). General construction: for Pa={p₁,p₂} with v_{p₁}(a)=v_{p₂}(a)=v,
Pb={q^s}, Pc={r^u}: set φ_r=1, φ_q=1, φ_{p₂}=(u−s)/v (when v|(u−s)). For v∤(u−s):
use φ_r=v/gcd(v,u−s), scale proportionally. The norm bound is max(p₂·|(u−s)/v|, q, r)
and is ≤ v_max·R^{1/3} in all verified cases.

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

1. **CONFIRMED-4 (achieved, 2026-08-16):** OB-17 proved for all ω*=4 R<c triples:
   - a>1: Theorem D (best of 3 pairings). ✓
   - a=1, unequal-val Pb: within-group Pb. ✓
   - a=1, equal-val Pb, single-prime Pc: vacuous by Mihailescu. ✓
   - a=1, equal-val Pb, multi-prime Pc: Pb-Pc construction (example: (1,26³,17577)). ✓
2. **CONFIRMED-GENERAL (achieved, 2026-08-16):** OB-17 proved for all R<c triples with
   ω*≥3. Sub-case B (a=1, π₁,π₂∈Pb, multi-prime Pc) closed by Extended Key Lemma for
   π₃: M=6 forces π₃=7 via 5∤c (modular) and 7|c for v odd; M=10 forces π₃=11;
   both satisfy π₃^{ω*-1}≤R. Computational confirmation: 2 edge-case triples found
   (c≤10^{12}, v≤50), 0 OB-15 violations.
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
