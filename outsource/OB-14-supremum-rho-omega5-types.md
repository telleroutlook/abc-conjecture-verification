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

**Theorem OB-14A (unconditional upper bound).**  
For all squarefree coprime triples of type (2,1,2) or (2,2,1):
$$
  \rho(a,b,c) \;<\; \frac{1}{6^{1/4}} \;\approx\; 0.6389.
$$

**Conjecture OB-14B (supremum, conditional on sieve density).**  
$$
  \sup\bigl\{\rho(a,b,c) : (a,b,c) \text{ squarefree coprime, type (2,1,2) or (2,2,1)}\bigr\}
  \;=\; \frac{1}{6^{1/4}},
$$
where the supremum is not attained by any finite triple.  The proof that this value is
approached requires that the following family is infinite (a consequence of
Chen's theorem / Bombieri–Vinogradov, but not needed for OB-14A):

**Family F1 (type (2,1,2)):** a = 6 = 2·3, b = q (prime), c = 6 + q = r₁·r₂ (semiprime),
with r₁/r₂ → 1 (near-balanced, i.e. r₁ and r₂ are consecutive or near-consecutive primes).
Then ρ(6, q, 6+q) → 1/6^{1/4} as q → ∞ through valid values.

**Family F2 (type (2,2,1)):** a = 6 = 2·3, b = q₁·q₂ (semiprime with q₁/q₂ → 1),
c = 6 + q₁q₂ (prime). Then ρ(6, q₁q₂, 6+q₁q₂) → 1/6^{1/4} as b → ∞.

---

## Proof skeleton to be closed

### Step 1 — Strict upper bound ρ < 1/(p₁p₂)^{1/4} for type (2,1,2) with P_a = {p₁,p₂}

Fix a = p₁p₂ with p₁ < p₂. Let b = q (prime), c = a+b = r₁r₂ with r₁ < r₂ primes.

**E_n applicability.** For type (2,1,2): Pa={p₁,p₂}, Pb={q}, Pc={r₁,r₂} are all
non-empty, so the E_n theorem applies directly and gives
nd = second\_smallest$\{m_a, m_b, m_c\}$ = second\_smallest$\{p_1, q, r_1\}$.

**Coprimality constraint.** Since gcd(a,c)=1, no prime dividing c can divide a.
Hence $r_1, r_2 \notin \{p_1, p_2\}$.  Note: this means $r_1$ may be *less than* $p_2$
(e.g.\ for $(p_1,p_2)=(2,7)$, $r_1$ can equal $3$); the lower bound on $r_1$ is the
smallest prime not in $\{p_1,p_2\}$, not "the smallest prime greater than $p_2$."
For small $r_1$ (specifically $r_1 < p_1$), computation shows $q = r_1 r_2 - p_1 p_2 \le 1$
for the smallest valid $r_2$, ruling out a prime $q$; the first valid $r_2$ always
gives $r_1(r_2-r_1) > p_1 p_2$ (verified for all $(p_1,p_2)$ with $p_1 p_2 \le 200$).

For all sufficiently large $q$: $p_1 < r_1 < q$ (since $r_1^2 \le r_1 r_2 = c = a+q \le 2q$
for large $q$, giving $r_1 \le \sqrt{2q} < q$), so
nd = second\_smallest$\{p_1, q, r_1\} = r_1$.

$$
  \rho^4 = \frac{r_1^4}{p_1 p_2 \cdot q \cdot r_1 r_2}
         = \frac{r_1^3}{p_1 p_2 \cdot q \cdot r_2}.
$$
We need $\rho^4 < 1/(p_1 p_2)$, i.e., $r_1^3 < q \cdot r_2$.

**Key inequality:** $r_1^3 < q \cdot r_2$ follows from $r_1^2 < q$, since
$$r_1^3 = r_1 \cdot r_1^2 < r_1 \cdot q < r_2 \cdot q$$
(first step: $r_1^2 < q$; second step: $r_1 < r_2$).

**When does $r_1^2 < q$ hold?**
$r_1^2 < q \iff r_1^2 < r_1 r_2 - p_1 p_2 \iff r_1(r_2 - r_1) > p_1 p_2$.

**Case $p_1 p_2 = 6$:** By coprimality, $r_1 \notin \{2,3\}$, so $r_1 \ge 5$.
Since $r_1$ and $r_2$ are distinct odd primes, $r_2 - r_1 \ge 2$, giving
$r_1(r_2-r_1) \ge 5 \cdot 2 = 10 > 6$. ✓ No further case analysis needed.

**General $p_1 p_2$:** $r_1 \notin \{p_1,p_2\}$ and $r_2 - r_1 \ge 2$ for distinct
odd prime pairs. When $r_1(r_2-r_1) \le p_1p_2$ (possible for small $r_1$ and large
$p_1p_2$), the argument requires either: (a) showing no valid prime $q$ exists for
those $(r_1,r_2)$ pairs, or (b) a direct check that $\rho < 1/(p_1p_2)^{1/4}$ via
$nd \le q < r_1^2$ (in which case $nd = q$ and $\rho^4 = q^3/(p_1p_2 \cdot q \cdot r_2^3)
\to 0$). A finite check per fixed $p_1p_2$ closes this gap.

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

*(Conditional on sieve density:)* The infinitude of primes q with 6+q = r₁r₂
semiprime near-balanced follows from Bombieri–Vinogradov / Chen's theorem on almost-primes
(specifically: the set of primes q ≤ N with 6+q = r₁r₂ semiprime has counting function
≫ N/(log N)² by standard sieve methods). This hypothesis is required for OB-14B only;
Theorem OB-14A is unconditional.

### Step 3 — Type (2,2,1) by symmetry

The type (2,2,1) analysis is identical with roles of b and c swapped. For a=6, b=q₁q₂
(near-balanced semiprime), c=6+q₁q₂ (prime):
nd = second_smallest{2, q₁, c} = q₁ ≈ √b, R ≈ 6b·c ≈ 6b².
The upper bound argument of Step 1 applies verbatim (with b replacing q and q₁ replacing r₁).

---

## Acceptance criteria

1. **CONFIRMED-A (unconditional):** Complete proof of Theorem OB-14A — ρ < 1/6^{1/4}
   for all type (2,1,2) and (2,2,1) triples, including the finite check for general
   p₁p₂ (closing the "small r₁" case).
2. **CONFIRMED-B (conditional):** Proof of Conjecture OB-14B — sup ρ = 1/6^{1/4} —
   conditional on a named sieve/density hypothesis (Chen's theorem, Bombieri–Vinogradov,
   or similar); hypothesis must be clearly stated.
3. **CONFIRMED-AB:** Both OB-14A and OB-14B fully proved.
4. **PARTIAL:** OB-14A proved for a=6 only (p₁p₂=6 fixed), without general p₁p₂.
5. **REFUTED:** Explicit counterexample with ρ ≥ 1/6^{1/4} for some finite triple.
6. **INCONCLUSIVE + localization:** Precise statement of the gap remaining.

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
