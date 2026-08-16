# Problem OB-13 — Minimum non-degenerate norm in the generalised Pasten lattice (non-squarefree extension)

**Type:** Integer lattice geometry / valuation theory / elementary number theory  
**Non-circularity:** The abc conjecture, IUT Corollary 3.12, Szpiro's conjecture, known
abc triples, and any fitted parameter are not assumed.  The problem concerns
lattice geometry of a single coprime triple; it neither uses abc as a hypothesis
nor derives abc as a conclusion.  No external analytic input (GRH, Faltings, etc.)
is assumed or needed.

---

## All definitions (self-contained)

### 1. The generalised Pasten lattice

Let $a, b$ be coprime positive integers and set $c = a + b$.

**Distinct-prime support.**  Let $P = P_a \cup P_b \cup P_c$ be the set of distinct
rational primes dividing $abc$, with $\omega^* = |P|$.

**Signed valuation groups.**  Write
$$
P_a = \{p : p \mid a\}, \quad P_b = \{p : p \mid b\}, \quad P_c = \{p : p \mid c\},
$$
so $P = P_a \cup P_b \cup P_c$ (disjoint, since $\gcd(a,b)=1$ implies
$P_a \cap P_b = \emptyset$, and a prime dividing two of $a,b,c$ divides all three,
which is impossible when $\gcd(a,b)=1$).

**Lattice vectors.**  A vector $\varphi = (\varphi_p)_{p \in P} \in \mathbb{Z}^{\omega^*}$
belongs to the **generalised Pasten lattice** $F(a,b)$ if and only if
$$
\sum_{p \in P_a} v_p(a)\,\varphi_p
\;+\;
\sum_{p \in P_b} v_p(b)\,\varphi_p
\;=\;
\sum_{p \in P_c} v_p(c)\,\varphi_p,  \tag{C}
$$
where $v_p(n)$ denotes the $p$-adic valuation of $n$ (the exponent of $p$ in the
prime factorisation of $n$).

**Note (squarefree special case).**  When $a, b, c$ are all squarefree,
every valuation $v_p(\cdot) \in \{0,1\}$, and constraint~(C) reduces to
$\sum_{P_a}\varphi_p + \sum_{P_b}\varphi_p = \sum_{P_c}\varphi_p$.

### 2. Norm

$$
\|\varphi\| = \max_{p \in P}\; p\,|\varphi_p|.
$$

### 3. Wronskian and non-degeneracy

$$
W(\varphi) = \sum_{p \in P_b} \varphi_p \;-\; \sum_{p \in P_a} \varphi_p.
$$

A non-zero vector $\varphi \in F(a,b)$ is **non-degenerate** if $W(\varphi) \neq 0$.
Otherwise it is **degenerate**.

### 4. Minimum non-degenerate norm

$$
\mathrm{nd}(a,b) = \min\bigl\{\|\varphi\| : \varphi \in F(a,b),\; W(\varphi) \neq 0\bigr\}.
$$

### 5. Radical, quality, and valuation maximum

$$
R = \mathrm{rad}(abc) = \prod_{p \in P} p, \qquad
\mathrm{quality}(a,b,c) = \frac{\log c}{\log R}, \qquad
v_{\max} = \max_{p \in P}\, v_p(abc).
$$

Note: quality $\leq 1$ for all squarefree $c$; quality $> 1$ is possible when $c$
has a prime-power factor.

### 6. Known result for squarefree triples (E_n theorem, proved in this project)

When $a$, $b$, $c$ are all squarefree define the **group minima**
$$
m_a = \min_{p \in P_a} p, \quad m_b = \min_{p \in P_b} p, \quad
m_c = \min_{p \in P_c} p
$$
and let $\mathrm{nd}_{\mathrm{sq}}$ be the second-smallest element of
$\{m_a, m_b, m_c\}$ (i.e.\ the median when all three are distinct).

**Theorem (E_n).**  $\mathrm{nd}(a,b) = \mathrm{nd}_{\mathrm{sq}}$ for all squarefree
coprime triples $a + b = c$.

Moreover, for all squarefree triples $\mathrm{nd}(a,b) \leq R^{1/(\omega^*-1)}$
(the Minkowski bound), so a non-degenerate short vector always exists within the
Minkowski ball.

---

## The theorem / claim to be verified

**Conjecture OB-13A (non-squarefree E_n extension).**
There exist absolute constants $C \geq 1$ and $A \geq 0$ such that for every
coprime triple $a + b = c$ (not necessarily squarefree):
$$
\mathrm{nd}(a,b) \;\leq\; C \cdot v_{\max}^A \cdot R^{1/(\omega^*-1)}.  \tag{OB-13A}
$$

**Minimal version (Conjecture OB-13B).**  The specific bound
$$
\mathrm{nd}(a,b) \;\leq\; v_{\max} \cdot R^{1/(\omega^*-1)}  \tag{OB-13B}
$$
holds for all coprime $a + b = c$ (i.e.\ $C = 1$, $A = 1$).

**Structural sub-question OB-13C.**  Find a closed-form expression for
$\mathrm{nd}(a,b)$ analogous to the squarefree formula $\mathrm{nd}_{\mathrm{sq}}$
above.  In the squarefree case the formula involves only the group minima.
What replaces it when valuations $v_p > 1$?

---

## Proof skeleton to be closed

### Step 1 — Identify the lattice structure for fixed valuation profile

Fix the valuation profile $(v_p(a), v_p(b), v_p(c))_{p \in P}$.
Constraint~(C) defines a hyperplane $H \subset \mathbb{Z}^{\omega^*}$.
The degenerate vectors form the sub-lattice $D = \{\varphi \in H : W(\varphi)=0\}$.

**What to close for Step 1:**  Show that $H \setminus D$ is non-empty (a non-degenerate
vector exists).  In the squarefree case this is trivial (take $\varphi_{m_a}=1$,
$\varphi_{m_c}=1$ and all others zero).  For non-squarefree, the constraint is
weighted; the existence proof must handle arbitrary valuations.

### Step 2 — Lower bound on the non-degenerate minimum (the degenerate sub-lattice fills the short vectors)

For any non-degenerate $\varphi$, constraint~(C) gives
$W(\varphi) = \sum_{P_c} v_p(c)\varphi_p - \sum_{P_a} v_p(a)\varphi_p
- \sum_{P_b} v_p(b)\varphi_p + W(\varphi) = \ldots$.  The shortest non-degenerate
vector must avoid the coset $D + \mathbf{e}$ structure.

**What to close for Step 2:**  Derive a formula or tight bound for
$\mathrm{nd}(a,b)$ in terms of the primes $p \in P$ and the valuations
$v_p(a), v_p(b), v_p(c)$.  Identify whether the squarefree formula
$\mathrm{nd}_{\mathrm{sq}}$ generalises as
$\mathrm{nd}(a,b) = $ (second smallest of $\{m_a' , m_b', m_c'\}$) for
appropriately re-weighted group minima $m_g' = \min_{p \in P_g}\, p / v_p(g)$?
The numerical anchor (Section~6 below) suggests this may not be exact.

### Step 3 — Upper bound $\mathrm{nd}(a,b) \leq v_{\max} \cdot R^{1/(\omega^*-1)}$

The squarefree proof of $\mathrm{nd} \leq R^{1/(\omega^*-1)}$ uses the explicit
optimal vector $\varphi^* = (\varphi_{m_a}=-1, \varphi_{m_c}=-1,
\text{others}=0)$ or similar, whose norm equals $\max(m_a, m_c)
\leq R^{1/(\omega^*-1)}$ by the AM-GM-type inequality on primes.

For non-squarefree, the constraint forces $v_p(c)\varphi_p = \sum \pm v_q(\cdot)\varphi_q$,
which may require larger $\varphi$ values, potentially inflating the norm by a factor
related to $v_{\max}$.

**What to close for Step 3:**  Construct an explicit non-degenerate vector for the
non-squarefree case (generalising the squarefree optimal vector) and bound its norm
by $v_{\max} \cdot R^{1/(\omega^*-1)}$.

---

## Acceptance criteria

An external review is accepted as **CONFIRMED** if it:
1. Proves OB-13B ($\mathrm{nd}(a,b) \leq v_{\max} \cdot R^{1/(\omega^*-1)}$) or
   OB-13A with explicit constants $C, A$, without assuming abc or any abc-equivalent,
   AND provides an explicit non-degenerate vector achieving or bounding the norm; OR
2. Produces a counterexample triple $(a,b,c)$ with
   $\mathrm{nd}(a,b) > v_{\max} \cdot R^{1/(\omega^*-1)}$, verified by explicit
   enumeration of all short lattice vectors; OR
3. Provides a closed-form expression for $\mathrm{nd}(a,b)$ (answering OB-13C)
   that matches all numerical anchors below.

A review is accepted as **PARTIAL** if it:
- Settles OB-13C (closed-form) but not OB-13B, or vice versa.

A review may report **INCONCLUSIVE** with a precise statement of what is missing
(a specific lemma, a gap in the valuation arithmetic, etc.).  This is a valid outcome.

The outcome **REFUTED** requires an explicit counterexample.

---

## Numerical anchors (sanity only — not inputs to any proof)

All values computed by brute-force enumeration (bound $|\varphi_p| \leq 8$) in
`discovery/m2_directions/t57_nonsquarefree.py`.

| $(a, b, c)$ | $\omega^*$ | $R$ | quality | $v_{\max}$ | $\mathrm{nd}(a,b)$ | $R^{1/(\omega^*-1)}$ | $v_{\max}\cdot R^{1/(\omega^*-1)}$ | conj.~B? |
|---|---|---|---|---|---|---|---|---|
| $(2, 3, 5)$ | 3 | 30 | 0.473 | 1 | 3 | 5.48 | 5.48 | ✓ |
| $(3, 5, 8)$ | 3 | 30 | 0.611 | 3 | 5 | 5.48 | 16.4 | ✓ |
| $(5,11,16)$ | 3 | 110 | 0.590 | 4 | 11 | 10.49 | 41.9 | ✓ |
| $(1, 3, 4)$ | 2 | 6 | 0.774 | 2 | 6 | 6.00 | 12.0 | ✓ |
| $(1, 7, 8)$ | 2 | 14 | 0.788 | 3 | 21 | 14.0 | 42.0 | ✓ |
| $(1, 8, 9)$ | 2 | 6 | 1.226 | 3 | 9 | 6.00 | 18.0 | ✓ |
| $(1,48,49)$ | 3 | 42 | 1.041 | 4 | 7 | 6.48 | 25.9 | ✓ |
| $(4, 5, 9)$ | 3 | 30 | 0.646 | 2 | 3 | 5.48 | 10.9 | ✓ |
| $(8, 1, 9)$ | 2 | 6 | 1.226 | 3 | 9 | 6.00 | 18.0 | ✓ |

The key rows are $(1,8,9)$ and $(1,48,49)$ where quality $> 1$ and
$\mathrm{nd} > R^{1/(\omega^*-1)}$ — the squarefree bound fails, but the
conjectured $v_{\max}$-scaled bound holds in all tested cases.

**Verification script.**  A reviewer can independently replicate these values by
running `python3 discovery/m2_directions/t57_nonsquarefree.py` in the repository root.
No external data or prior results are needed.

---

## Significance and scope limit

**Why this matters.**  The E_n theorem (squarefree case) gives $\mathrm{nd}(a,b)
\leq R^{1/(\omega^*-1)}$ as an upper bound, meaning a non-degenerate short vector
always fits inside the Minkowski ball.  For non-squarefree high-quality triples
(the case where abc is non-trivial), the Minkowski ball may contain only degenerate
vectors, with the minimum non-degenerate vector lying just outside.  The bound
OB-13B, if true, would quantify exactly how far outside: at most a $v_{\max}$ factor.
This is a structural lattice-geometry result; it does **not** by itself imply abc.

**Scope limit.**  This problem asks only for an upper bound on $\mathrm{nd}(a,b)$.
A lower bound on $\mathrm{nd}(a,b)$ would be far harder and is **not** requested here.
The problem is bounded in scope and should be resolvable without deep analytic number
theory.
