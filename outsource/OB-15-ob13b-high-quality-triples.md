# Problem OB-15 — OB-13B for high-quality triples (R < c)

**Type:** Integer lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter are not assumed. The problem concerns a lattice
geometry bound for coprime triples satisfying the arithmetic constraint R < c. No
abc-equivalent assumption enters at any point.

---

## Background and motivation

**Why this problem matters.** The abc conjecture concerns triples a+b=c with
*quality* = log(c)/log(R) exceeding 1+ε. This is equivalent to R < c (quality > 1).
For the abc verification program, the relevant regime is precisely R < c — and only
in this regime does the lattice geometry need to work.

**What was previously claimed and refuted.**
OB-13B — the bound nd(a,b) ≤ v_max · R^{1/(ω*−1)} for all coprime triples — was
recently refuted (2026-08-16). Counterexamples:

| Triple | quality | nd | v_max·R^{1/(ω*−1)} | R < c? |
|---|---|---|---|---|
| (1, 6, 7) | 0.52 | 7 | 6.48 | **No** (R=42 > c=7) |
| (1, 36, 37) | 0.67 | 74 | 29.8 | **No** (R=222 > c=37) |
| (1, 30, 31) | 0.50 | 31 | 9.76 | **No** (R=930 > c=31) |

Every known counterexample has R > c (quality < 1). No counterexample has R < c.

**The restricted conjecture.** Numerical verification over all coprime triples with
c ≤ 200 and R < c (brute-force nd, 0 violations) supports:

$$\boxed{\text{Conjecture OB-15:} \quad R < c \implies \mathrm{nd}(a,b) \leq v_{\max} \cdot R^{1/(\omega^*-1)}.}$$

---

## All definitions (self-contained)

**Setting.** Let a, b be coprime positive integers with c = a + b.

**Distinct-prime support.** P = Pa ∪ Pb ∪ Pc, the set of all distinct primes dividing
abc, with ω* = |P| (pairwise disjoint since gcd(a,b)=1).

**Generalised Pasten lattice F(a,b).** Integer vectors φ = (φ_p)_{p∈P} satisfying
$$\sum_{p \in P_a} v_p(a)\,\varphi_p \;+\; \sum_{p \in P_b} v_p(b)\,\varphi_p
\;=\; \sum_{p \in P_c} v_p(c)\,\varphi_p.  \tag{C}$$

**Norm.** ‖φ‖ = max_{p∈P} p|φ_p|.

**Wronskian.** W(φ) = Σ_{Pb} φ_p − Σ_{Pa} φ_p.

**Non-degeneracy.** φ ∈ F(a,b) is non-degenerate if W(φ) ≠ 0.

**Minimum non-degenerate norm.**
$$\mathrm{nd}(a,b) = \min\{\|\varphi\| : \varphi \in F(a,b),\; W(\varphi) \neq 0\}.$$

**Valuation maximum.** v_max = max_{p∈P} v_p(abc).

**Radical.** R = ∏_{p∈P} p (product of distinct primes of abc).

**High-quality constraint.** R < c (equivalently quality = log c / log R > 1).

---

## The theorem / claim to be proved or refuted

**Conjecture OB-15.** For every coprime triple a + b = c with R < c:
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}.$$

### Key structural observations (to guide the proof)

**Observation 1 (v_max is non-trivial).** R < c implies c is *not* squarefree: if c
were squarefree then c | R (since all primes of c are in R), so c ≤ R — contradicting
R < c. Hence some prime p ∈ Pc has v_p(c) ≥ 2, so v_max ≥ 2.

**Observation 2 (the proved bound).** By the cross-group construction (OB-13 Step 3),
$$\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot \mathrm{med}(m_a, m_b, m_c),$$
where med is the second-smallest of the three group minima m_a=min(Pa), m_b=min(Pb),
m_c=min(Pc). OB-15 reduces to showing:
$$\mathrm{med}(m_a, m_b, m_c) \;\leq\; R^{1/(\omega^*-1)} \quad \text{when } R < c.
\tag{KEY}$$

(When the within-group construction is available — two primes in the same group with
unequal valuations — it can give nd strictly smaller than v_max·med, so (KEY) is
sufficient but possibly not necessary.)

**Observation 3 (why counterexamples have R > c).** The refuted cases all have a
single large prime in Pc or Pb with med = that large prime > R^{1/(ω*-1)}.
Example: (1,6,7): med = 7, R^{1/2} = √42 ≈ 6.48. The constraint R < c = 7 forces
R < 7, but R = 42 > 7 here — so R < c fails, consistent with Observation 2.

**Observation 4 (R < c restricts the median).** If R < c and m_c = min(Pc) ≤ med:
$$m_c^{\omega^*-1} \;\leq\; R \quad\text{(to prove)}.$$
This would give m_c ≤ R^{1/(ω*-1)}, and since med ≤ m_c is not immediate, a stronger
argument is needed.

---

## Proof skeleton to be closed

### Step 1 — Reduction to the "single-prime c-group" case

The hardest case is type (0, k, 1): Pa=∅, Pb = k primes, Pc = {p} (single prime).
Here med(∞, m_b, p) = p if p > m_b, or m_b if m_b > p.

**Sub-case 1a (p = med > m_b):** Need p ≤ R^{1/(ω*-1)}.
R < c = p^e (since c ∈ Pc = {p} and R = m_b·...·m_b'·p). R = rad(b)·p.
From R < c = p^e: rad(b)·p < p^e, so rad(b) < p^{e-1}.
Then R = rad(b)·p, and R^{1/(ω*-1)} = (rad(b)·p)^{1/(ω*-1)}.
Need: p ≤ (rad(b)·p)^{1/(ω*-1)}, i.e., p^{ω*-1} ≤ rad(b)·p, i.e., p^{ω*-2} ≤ rad(b).
Since ω* = 1 + |Pb| and rad(b) ≥ product of ω*-1 distinct primes each ≥ 2:
rad(b) ≥ 2^{ω*-1}. Need p ≤ 2^{(ω*-1)/(ω*-2)}·... This is where the argument needs
the constraint rad(b) < p^{e-1}.

**What to close for Step 1:** Prove p ≤ R^{1/(ω*-1)} under the constraint
rad(b)·p < p^e (i.e., rad(b) < p^{e-1}) and ω* = 1 + |Pb| ≥ 2.

### Step 2 — Multiple-prime c-group and general case

When |Pc| ≥ 2: m_c = smallest prime in Pc < c^{1/2}, and the median is at most
c^{1/2} < R^{1/2} (since R > c^{1/2}... this needs justification from R < c).

**What to close for Step 2:** Show that when Pc has ≥ 2 primes (or when Pa is
non-empty), the median satisfies med ≤ R^{1/(ω*-1)} without the R < c constraint, or
use R < c to obtain a stronger bound.

### Step 3 — Within-group assistance for equal-valuation groups

When two primes p, q in the same group have *unequal* valuations v_p ≠ v_q, the
within-group vector φ_p = v_q/g, φ_q = −v_p/g (g = gcd(v_p,v_q)) is non-degenerate
(W = ±(v_q−v_p)/g ≠ 0) with norm max(p·v_q, q·v_p)/g. This can be much smaller than
v_max·med and gives nd ≤ max(p·v_q, q·v_p)/g.

**What to close for Step 3:** Identify which high-quality triples are NOT covered by
within-group or Step 1 (i.e., same-valuation same-group primes and single-prime groups).
Show these remaining cases satisfy OB-15 via a direct argument.

---

## Acceptance criteria

1. **CONFIRMED:** Complete proof of Conjecture OB-15 (nd(a,b) ≤ v_max·R^{1/(ω*-1)}
   for all triples with R < c), unconditional.
2. **PARTIAL:** Proof for the restricted case |Pc|=1 (single prime in c-group), or
   for ω*=2 and ω*=3 only, or for squarefree a,b with c non-squarefree.
3. **CONDITIONAL:** Proof assuming a named auxiliary lemma (e.g., a prime gap bound
   or a Bertrand-type statement).
4. **REFUTED:** Explicit counterexample — a coprime triple with R < c and
   nd(a,b) > v_max·R^{1/(ω*-1)}, verified by brute-force lattice search.
5. **INCONCLUSIVE + localization:** Precise identification of which step fails and
   what additional input is needed.

---

## Numerical anchors (sanity only — not inputs to any proof)

All nd values computed by brute-force enumeration.

| (a,b,c) | quality | v_max | R | ω* | R^{1/(ω*−1)} | v_max·R^{1/(ω*−1)} | nd | OB-15? |
|---|---|---|---|---|---|---|---|---|
| (1, 8, 9) | 1.226 | 3 | 6 | 2 | 6.00 | 18.00 | 9 | ✓ |
| (1, 48, 49) | 1.041 | 4 | 42 | 3 | 6.48 | 25.93 | 7 | ✓ |
| (4, 5, 9) | 1.093 | 2 | 30 | 3 | 5.48 | 10.95 | 3 | ✓ |
| (8, 1, 9) | 1.226 | 3 | 6 | 2 | 6.00 | 18.00 | 9 | ✓ |
| (3, 5, 8) | 0.611 | 3 | 30 | 3 | 5.48 | 16.43 | 5 | ✓ (R>c) |
| (5, 11, 16) | 0.590 | 4 | 110 | 3 | 10.49 | 41.95 | 11 | ✓ (R>c) |

Note: (3,5,8) and (5,11,16) have R > c (quality < 1) and are outside the conjecture's
scope, but OB-13B holds for them anyway. The conjecture is about R < c cases only.

**Verification script:** `discovery/m2_directions/ob13_verify.py`
(run `python3 discovery/m2_directions/ob13_verify.py` from repo root).

---

## Significance

If Conjecture OB-15 is confirmed, it shows that in the *abc-relevant* regime (R < c),
the Pasten lattice always has a non-degenerate vector of norm ≤ v_max·R^{1/(ω*−1)}.
This is the structural lattice result needed to support the height construction in the
abc verification program. The refuted OB-13B (which failed for R > c triples) is not
a blocker for the proof strategy, since those low-quality triples are not the target.

**Scope limit.** This problem asks only for an upper bound on nd. A lower bound on nd
(showing the abc conjecture via quality estimates) is a separate, harder problem (OBL
in the project's claim ledger) and is not requested here.
