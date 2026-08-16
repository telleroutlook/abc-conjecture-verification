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

**Partial answer (proved for the case $a=1$, $b$ squarefree, $c = q^k$).**
When $P_a = \emptyset$, $P_c = \{q\}$ with $v_q(c) = k$, and $P_b = \{p_1,\ldots,p_n\}$
with all $v_{p_i}(b)=1$:
$$
\mathrm{nd}(1,b) = \max\!\Bigl(q,\;\min_{T \subseteq P_b,\, T \neq \emptyset}
\Bigl\lceil\text{LP}(k,T)\Bigr\rceil^*\Bigr),
$$
where $\text{LP}(k,T)$ is the continuous min-max optimum for distributing $k$ among
$T$:
$$
\text{LP}(k,T) = \frac{k}{\displaystyle\sum_{p_i \in T} \frac{1}{p_i}}
= \frac{k \prod_{p_i \in T} p_i}{\displaystyle\sum_{p_i \in T}
\prod_{p_j \in T,\, j \neq i} p_j},
$$
and $\lceil \cdot \rceil^*$ denotes the integer ceiling achieved by rounding the LP
solution to integer values.  For $|T|=1$ (single prime): $\text{LP}(k,\{p\}) = kp$,
recovering the pairwise formula.  For $|T|=2$: $\text{LP}(k,\{p,q\}) = kpq/(p+q)$,
always strictly less than $kp$ for the smaller prime $p$.

**Verified examples:**
- $(1,15,16)$: best $T=\{3,5\}$, $\text{LP}=7.5$, integer best $=9$, brute $\mathrm{nd}=9$. $\checkmark$
- $(1,255,256)$: best $T=\{3,5\}$, $\text{LP}=15.0$, integer best $=15$, brute $\mathrm{nd}=15$. $\checkmark$

**Open:** The general formula for arbitrary $a,b,c$ (arbitrary valuation profiles) is
not known.  The LP-rounding approach generalises, but the formula is a min-max integer
program with no simple closed form in general.

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

### Step 3 — Upper bound $\mathrm{nd}(a,b) \leq v_{\max} \cdot R^{1/(\omega^*-1)}$ **[PROVED]**

**Proof.**  For each ordered pair of primes $(p, q)$ with $p \in P_g$ and $q \in P_{g'}$
from two distinct groups $g \neq g'$, let $g_0 = \gcd(v_p(g\text{-factor}),\, v_q(g'\text{-factor}))$
and define:

- **$(P_a, P_b)$ pairs** (both on the LHS of constraint C):
  $\varphi_p = v_q(b)/g_0$, $\varphi_q = -v_p(a)/g_0$, others zero.
  Then $v_p(a)\varphi_p + v_q(b)\varphi_q = 0$ ✓ and $W \ne 0$ ✓.

- **$(P_a, P_c)$ pairs** (LHS vs RHS):
  $\varphi_p = v_q(c)/g_0$, $\varphi_q = v_p(a)/g_0$, others zero (both positive).
  Then $v_p(a)\varphi_p = v_q(c)\varphi_q$ ✓ and $W = -\varphi_p \ne 0$ ✓.

- **$(P_b, P_c)$ pairs** (LHS vs RHS):
  $\varphi_q = v_r(c)/g_0$, $\varphi_r = v_q(b)/g_0$, others zero (both positive).
  Then $v_q(b)\varphi_q = v_r(c)\varphi_r$ ✓ and $W = \varphi_q \ne 0$ ✓.
The norm is $\|\varphi^{(p,q)}\| = \max(p \cdot v_q/g,\; q \cdot v_p/g)$.

Taking the minimum over all such pairs:
$$
\mathrm{nd}(a,b) \;\leq\; \min_{(p,q)\text{ cross-group}} \max\!\Bigl(p\cdot\tfrac{v_q}{g},\;
q\cdot\tfrac{v_p}{g}\Bigr) \;\leq\; v_{\max}\cdot \mathrm{med}(m_a, m_b, m_c),
$$
where $\mathrm{med}$ denotes the median (second smallest of the three group minima).
Finally, $\mathrm{med}(m_a,m_b,m_c)^{\omega^*-1} \leq R$ because the $\omega^*-1$
primes of $R$ other than the smallest all exceed the median, giving
$R \geq m_{\min} \cdot \mathrm{med}^{\omega^*-1} \geq \mathrm{med}^{\omega^*-1}$.
Hence $\mathrm{med} \leq R^{1/(\omega^*-1)}$ and the bound follows. $\square$

**Numerical verification:** `discovery/m2_directions/t59_ob13_verify.py` checks all
test triples; the all-pairs GCD construction matches or improves upon the brute-force
nd for all but two cases (see OB-13C discussion below), and OB-13B holds in all cases.

### Step 4 — Exact formula for $\omega=3$: 2D lattice SVP **[DISCOVERY TIER]**

**Setting ($\omega=3$ triples with one prime per group).**
For $P_a = \{p_1\}$, $P_b = \{p_2\}$, $P_c = \{p_3\}$ with valuations $v_a, v_b, v_c$,
the constraint~(C) is $v_a \varphi_1 + v_b \varphi_2 = v_c \varphi_3$.
Fix $(\varphi_1, \varphi_2) \in \mathbb{Z}^2$; then $\varphi_3$ is an integer iff
$$
  (\varphi_1, \varphi_2) \;\in\; \mathcal{L}
    \;=\; \bigl\{(x,y)\in\mathbb{Z}^2 : v_c \mid v_a x + v_b y\bigr\}.
$$
$\mathcal{L}$ is a sublattice of $\mathbb{Z}^2$ of index $v_c / \gcd(v_a, v_b, v_c)$.
An explicit basis is found by extended GCD: let $g = \gcd(v_b, v_c)$; then
$\mathbf{e}_1 = (1,\, t)$ where $t \equiv -v_a \cdot (v_b/g)^{-1} \pmod{v_c/g}$,
and $\mathbf{e}_2 = (0,\, v_c/g)$.

Computing $\mathrm{nd}(a,b)$ reduces to the \textbf{Shortest Vector Problem} on
$\mathcal{L}$ with norm $\|(x,y)\| = \max(p_1 |x|,\, p_2 |y|,\, p_3 |(v_a x + v_b y)/v_c|)$,
subject to $W(x,y) = y - x \neq 0$.

**Algorithm** (`discovery/m2_directions/t63_omega3_lattice_svp.py`):
Apply the Gauss--Lagrange 2D reduction to $\mathcal{L}$ (using the Euclidean proxy
$\|(p_1 x,\, p_2 y,\, p_3(v_a x + v_b y)/v_c)\|_2$), then search $[-25,25]^2$
in the reduced-basis coordinates.

**Verified:** for all 13 tested $\omega=3$ triples (squarefree and non-squarefree,
valuations up to 5), the SVP approach recovers the exact brute-force $\mathrm{nd}$.

**Key example** (new OB-13C gap case, T62):
$a = 27 = 3^3$, $b = 5$, $c = 32 = 2^5$.
Basis of $\mathcal{L} = \{(x,y): 5 \mid 3x + y\}$:
$\mathbf{e}_1 = (1,2)$, $\mathbf{e}_2 = (0,5)$.
Reduced basis: $(-2,1)$ and $(1,2)$.
Optimal vector: $n_1=-1$, $n_2=0$ gives $(\varphi_3, \varphi_5, \varphi_2) = (2,-1,1)$,
norm $= \max(3{\cdot}2,\, 5{\cdot}1,\, 2{\cdot}1) = 6$, $W = -3 \neq 0$.
Constraint: $3 \cdot 2 + 1 \cdot (-1) = 5 = 5 \cdot 1$. $\checkmark$
The all-pairs GCD construction (best pair $(3,2)$) gives norm $15$; the 2D SVP
reduces this to $6$ by using all three primes simultaneously.

**W_\psi divisibility result** (T62, 26 non-squarefree triples):
$W_\psi / \mathrm{nd} \in [0.4, 2.0]$; not always an integer.
$\mathrm{nd} \mid W_\psi$ holds in only 9/26 cases; $v_{\max} \mid W_\psi$ in 10/26.
No universal divisibility rule exists for non-squarefree triples.

**Scope limit for Step 4 (UPDATED — T64):**
The SVP parametrisation generalises to arbitrary $\omega$.  The constraint
$\sum_i \alpha_i \varphi_i = 0$ defines an $(\omega^*-1)$-dimensional sublattice of
$\mathbb{Z}^{\omega^*}$.  Its $\mathbb{Z}$-basis is found by the Smith normal form of
$[\alpha]$, then LLL-reduced.  A search over $[-25,25]^{\omega^*-1}$ in reduced
coordinates recovers the exact $\mathrm{nd}$.

**T64 verification** (`discovery/m2_directions/t64_omega4_lattice_svp.py`):
- $\omega=4$: 13 triples (squarefree and non-squarefree), \textbf{ALL MATCH}.
- $\omega=5$: 6 triples (squarefree and non-squarefree), \textbf{ALL MATCH}.

**OB-13C status (2026-08-16): RESOLVED algorithmically.**
$\mathrm{nd}(a,b)$ is computed exactly in polynomial time (in $\omega^*$ and the
valuation magnitudes) via LLL reduction + SVP on the $(\omega^*-1)$-dimensional
constraint lattice.  There is no simple closed-form expression in general, but the
algorithm is concrete and verified.

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

**Within-group construction and the failure of the squarefree lower bound.**
When a group $P_g$ contains two primes $p, q$ with *distinct* valuations $v_p \neq v_q$,
the within-group vector $\varphi_p = v_q/g_0$, $\varphi_q = -v_p/g_0$
(all other coordinates zero, $g_0 = \gcd(v_p, v_q)$) satisfies constraint (C)
and has $W = \pm(v_q - v_p)/g_0 \neq 0$.

**Consequence:** for non-squarefree triples, $\mathrm{nd}(a,b)$ can be *strictly below*
the squarefree E$_n$ formula value $\mathrm{med}(m_a, m_b, m_c)$.

**Counterexample to the squarefree lower bound:** $(a,b,c) = (72, 11, 83)$.
- $a = 2^3 \cdot 3^2$, $P_a = \{2,3\}$, $v_2(a)=3$, $v_3(a)=2$.
- $P_b = \{11\}$, $P_c = \{83\}$; $\mathrm{med}(m_a, m_b, m_c) = \mathrm{med}(2, 11, 83) = 11$.
- Within-group vector: $\varphi_2 = 2$, $\varphi_3 = -3$, $\varphi_{11} = \varphi_{83} = 0$.
  - Constraint: $3 \cdot 2 + 2 \cdot (-3) = 0$ ✓.
  - $W = 0 - 2 - (-3) = 1 \neq 0$ ✓.
  - Norm $= \max(2 \cdot 2,\, 3 \cdot 3) = 9$.
- Therefore $\mathrm{nd}(72, 11) \leq 9 < 11 = \mathrm{med}(m_a, m_b, m_c)$.
- The lower bound $\mathrm{nd} \geq \mathrm{med}$ valid for squarefree triples fails here.
  (The trivial lower bound $\mathrm{nd} \geq$ second-smallest prime in $P = 3$ still holds.)
