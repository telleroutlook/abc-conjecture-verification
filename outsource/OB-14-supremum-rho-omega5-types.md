# Problem OB-14 — Supremum of the nd-ratio for ω=5 types (2,1,2) and (2,2,1)

**Type:** Integer lattice geometry / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter K_ε are not used or assumed. The result concerns
structural properties of the Pasten lattice norm ratio ρ = nd / R^{1/(ω*−1)} defined
purely from the prime factorisation of squarefree coprime triples. No abc-equivalent
assumption enters at any point.

---

## All definitions (self-contained — everything is here)

**Setting.** Let (a, b, c) be a squarefree coprime triple with a + b = c, gcd(a,b)=1,
all of a, b, c squarefree.

**Prime partition.** P_a, P_b, P_c = prime factors of a, b, c (pairwise disjoint).
Partition type = (|P_a|, |P_b|, |P_c|).

**ω* = |P_a| + |P_b| + |P_c|:** total number of distinct prime divisors.

**Minimum non-degenerate norm (nd).** By the E_n theorem (proved in this project):
for squarefree ω*-prime coprime triples,
$$
  \mathrm{nd}(a,b) = \text{second-smallest of } \{m_a, m_b, m_c\},
$$
where m_g = min(P_g) (group minimum), with min(∅) = +∞.

**Radical:** R = product of all distinct prime factors of abc (i.e., R = ∏_{p | abc} p).

**nd-ratio:** ρ(a,b,c) = nd(a,b) / R^{1/(ω*−1)}.

**Type (2,1,2):** |P_a|=2, |P_b|=1, |P_c|=2, ω*=5.  
**Type (2,2,1):** |P_a|=2, |P_b|=2, |P_c|=1, ω*=5.

---

## The theorem to be proved

**Theorem OB-14.**  
For all squarefree coprime triples of type (2,1,2) or (2,2,1):
$$
  \rho(a,b,c) \;<\; \frac{1}{6^{1/4}} \;\approx\; 0.6389,
$$
and
$$
  \sup\bigl\{\rho(a,b,c) : (a,b,c) \text{ squarefree coprime, type (2,1,2) or (2,2,1)}\bigr\}
  \;=\; \frac{1}{6^{1/4}},
$$
where the supremum is not attained by any finite triple but is approached by the
following explicit families:

**Family F1 (type (2,1,2)):** a = 6 = 2·3, b = q (prime), c = 6 + q = r₁·r₂ (semiprime),
with r₁/r₂ → 1 (near-balanced, i.e. r₁ and r₂ are consecutive or near-consecutive primes).
Then ρ(6, q, 6+q) → 1/6^{1/4} as q → ∞ through valid values.

**Family F2 (type (2,2,1)):** a = 6 = 2·3, b = q₁·q₂ (semiprime with q₁/q₂ → 1),
c = 6 + q₁q₂ (prime). Then ρ(6, q₁q₂, 6+q₁q₂) → 1/6^{1/4} as b → ∞.

---

## Proof skeleton to be closed

### Step 1 — Strict upper bound ρ < 1/(p₁p₂)^{1/4} for type (2,1,2) with P_a = {p₁,p₂}

Fix a = p₁p₂ with p₁ < p₂. Let b = q (prime), c = a+b = r₁r₂ with r₁ < r₂ primes.

**Coprimality constraint.** Since gcd(a,c)=1, no prime dividing c can divide a.
Hence $r_1, r_2 \notin \{p_1, p_2\}$, and in particular $r_1 \ge p_3$, the smallest prime
greater than $p_2$.

For all sufficiently large $q$: $p_1 < r_1 < q$ (since $r_1^2 \le r_1 r_2 = c = a+q \le 2q$
for large $q$, giving $r_1 \le \sqrt{2q} < q$), so
nd = second\_smallest$\{p_1, q, r_1\} = r_1$.

$$
  \rho^4 = \frac{r_1^4}{p_1 p_2 \cdot q \cdot r_1 r_2}
         = \frac{r_1^3}{p_1 p_2 \cdot q \cdot r_2}.
$$
We need $\rho^4 < 1/(p_1 p_2)$, i.e., $r_1^3 < q \cdot r_2$.

**Key inequality:** $r_1^3 < q \cdot r_2$ follows from $r_1^2 < q$, since
$r_1^3 = r_1^2 \cdot r_1 < q \cdot r_1 < q \cdot r_2$ (using $r_1 < r_2$).

**When does $r_1^2 < q$ hold?**
$r_1^2 < q \iff r_1^2 < r_1 r_2 - p_1 p_2 \iff r_1(r_2 - r_1) > p_1 p_2$.

**Case $p_1 p_2 = 6$:** By coprimality, $r_1 \notin \{2,3\}$, so $r_1 \ge 5$.
Since $r_1$ and $r_2$ are distinct odd primes, $r_2 - r_1 \ge 2$, giving
$r_1(r_2-r_1) \ge 5 \cdot 2 = 10 > 6$. ✓ No further case analysis needed.

**General $p_1 p_2$:** $r_1 \ge p_3$ (smallest prime $> p_2$), and $r_2 - r_1 \ge 2$
for odd prime pairs, so $r_1(r_2-r_1) \ge 2p_3$. The condition $2p_3 > p_1 p_2$ holds
for $p_1=2, p_2=3$ (giving $p_3=5$, $2\cdot5=10>6$) and may fail for larger $p_1p_2$;
for those cases a finite check over the small-$r_1$ pairs (computable for each fixed $p_1p_2$)
closes the argument.

**Conclusion:** $\rho^4 < 1/(p_1 p_2)$, i.e.\ $\rho < 1/(p_1 p_2)^{1/4}$, for all type (2,1,2)
triples with $a = p_1 p_2$ and $nd = r_1$.  The global bound $\sup \rho \le 1/6^{1/4}$ follows
by minimising over all valid $p_1 p_2 \ge 6$.

### Step 2 — The supremum equals 1/6^{1/4}

Step 1 shows ρ < 1/(p₁p₂)^{1/4} for each fixed a = p₁p₂. The overall sup is:
$$
  \sup_{\text{type (2,1,2)}} \rho \;\leq\; \sup_{a = p_1 p_2} \frac{1}{(p_1 p_2)^{1/4}}
  = \frac{1}{\inf(p_1 p_2)^{1/4}} = \frac{1}{6^{1/4}},
$$
since the infimum of p₁p₂ over distinct primes p₁ < p₂ is 2·3 = 6.

**What to close for Step 2:** Show the supremum 1/6^{1/4} is approached, i.e.
lim sup ρ(6, q, 6+q) = 1/6^{1/4} as q → ∞ through primes with 6+q semiprime.
This requires: (i) the set of such q is infinite (Dirichlet-type density argument:
the density of primes q with 6+q = r₁r₂ semiprime is positive), and (ii)
r₁/(q+6)^{1/2} → 1 for near-balanced semiprimes (r₁ ≈ r₂ ≈ √(q+6) ≈ √q).

For (ii): if r₁ = √q − O(1) (near-balanced), then ρ = r₁/(6q(q+6))^{1/4} ≈ √q/(6q²)^{1/4}
= q^{1/2}/(6^{1/4} q^{1/2}) = 1/6^{1/4}.

**Note:** The infinitude of primes q with 6+q = r₁r₂ semiprime likely follows from
sieve methods (Goldbach-type density: for any fixed even integer 2k, the number of
primes p ≤ N with p+2k semiprime has positive density — a weaker form of Goldbach).
If this sieve estimate is unavailable, the result can be stated conditionally.

### Step 3 — Type (2,2,1) by symmetry

The type (2,2,1) analysis is identical with roles of b and c swapped. For a=6, b=q₁q₂
(near-balanced semiprime), c=6+q₁q₂ (prime):
nd = second_smallest{2, q₁, c} = q₁ ≈ √b, R ≈ 6b·c ≈ 6b².
The upper bound argument of Step 1 applies verbatim (with b replacing q and q₁ replacing r₁).

---

## Acceptance criteria

1. **CONFIRMED:** Complete proof that ρ < 1/6^{1/4} for all type (2,1,2) and (2,2,1)
   triples, AND that sup = 1/6^{1/4} (either unconditional or conditional on a named
   sieve/density hypothesis for the infinitude of qualifying primes).
2. **PARTIAL:** Proof of the strict upper bound ρ < 1/6^{1/4} without the matching
   lower bound (sup = 1/6^{1/4} not established), or vice versa.
3. **PARTIAL-CONDITIONAL:** Complete proof conditional on a stated sieve hypothesis.
4. **REFUTED:** Explicit counterexample with ρ ≥ 1/6^{1/4} for some finite triple.
5. **INCONCLUSIVE + localization:** Precise statement of the gap remaining.

---

## Numerical anchor (sanity only — not an input to the proof)

Type (2,1,2) near-limit examples (a=6, c = twin-prime-like semiprime):

| (a, b, c) | c factors | nd | R | ρ |
|---|---|---|---|---|
| (6, 3593, 3599) | 59·61 | 59 | 2·3·59·61·3593 | 0.6286 |
| (6, 11657, 11663) | 107·109 | 107 | 2·3·107·109·11657 | 0.6331 |
| (6, 19037, 19043) | 137·139 | 137 | 2·3·137·139·19037 | 0.6344 |
| (6, 36857, 36863) | 191·193 | 191 | 2·3·191·193·36857 | 0.6357 |

Theoretical limit: 1/6^{1/4} = 0.638943...

Type (2,2,1) near-limit examples (a=6, c = prime):

| (a, b, c) | b factors | nd | ρ |
|---|---|---|---|
| (6, 5183, 5189) | 71·73 | 71 | 0.6299 |
| (6, 39203, 39209) | 197·199 | 197 | 0.6357 |
| (6, 95477, 95483) | 307·311 | 307 | 0.6348 |

Both families approach 1/6^{1/4} ≈ 0.6389 from below.

Script to verify: `discovery/m2_directions/ob12_claim_c.py` (see discovery directory).
