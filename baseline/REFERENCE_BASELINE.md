# Verified baseline statements

This file records the exact source statements used as imported premises.  The
PDFs are primary-source copies; the checked version is part of each entry.

## Pasten (2021), arXiv:2106.16165v3

Source file: `pasten-2021-arithmetic-derivatives.pdf`.

### Derivative lattice and rank

Pasten defines, for positive integers $a,b$,

> $T(a,b)=\{\psi\in T:\operatorname{supp}(\psi)\subseteq
> \operatorname{supp}(ab(a+b)) \text{ and } d^\psi(a+b)=d^\psi a+d^\psi b\}$.

His equation (2.1) is the linear constraint

> $a\sum_{p\mid a} v_p(a)\psi(\xi_p)/p+
> b\sum_{p\mid b} v_p(b)\psi(\xi_p)/p=
> (a+b)\sum_{p\mid a+b} v_p(a+b)\psi(\xi_p)/p$.

Lemma 2.4 states:

> Let $a$ and $b$ be positive integers. Then $T(a,b)$ is a saturated
> $\mathbb Z$-submodule of $T$ of rank $\omega(ab(a+b))-1$.

Use in the paper: the additive-weight lattice and its rank.  The paper's
squarefree coordinate reduction is original and is proved locally.

### Wronskian and non-degeneracy

Section 1.3 defines $\psi$-independence by requiring

> $W^\psi(a,b)=ad^\psi b-bd^\psi a\neq 0$.

Use in the paper: the definition of non-degenerate derivative.

### Small Derivatives Conjecture

Conjecture 1.2 states (with the exception recorded verbatim):

> There is an absolute constant $0<\eta<1$ such that for all but finitely many
> triples of coprime positive integers $(a,b,c)$ satisfying $a+b=c$ and not of
> the form $(1,N,q)$ with $q$ prime (up to order), the following holds: There is
> $\psi\in T(a,b)$ such that $a,b$ are $\psi$-independent and
> $\|\psi\|<c^\eta$.

Use in the paper: scope of SDC.  It is a conjecture, not a premise.

### Relation to abc

Corollary 4.6 states:

> The Masser-Oesterlé abc Conjecture 3.1 implies the Small Derivative
> Conjecture 3.9. Conversely, the Small Derivative Conjecture 3.9 implies
> Oesterlé’s abc Conjecture 3.2.

Use in the paper: only the stated equivalence, with its exceptional family and
exponent dependence.  No implication from SDC to abc is used in a proof.

## Vaaler (1979), Pacific J. Math. 83, no. 2, 543–553

Source file: `vaaler-1979-geometric-inequality.pdf`.

### Central-section volume

Vaaler's corollary to Theorem 1 states:

> Let $Q_N$ be as in Theorem 1 and let $P_K$ be a $K$-dimensional subspace of
> $\mathbb R^N$. Then $\mu_K(Q_N\cap P_K)\ge 1$.

For $Q_N=C_N=[-1/2,1/2]^N$, this says that a central section by a
$K$-dimensional subspace has $K$-volume at least $1$.  Scaling by $2$ in the
ambient cube gives volume at least $2^K$ for $[-1,1]^N\cap P_K$.

### Lattice form used

Theorem 2 states in particular:

> If $|\det A^*A|>0$, then there exists a pair of nonzero lattice points
> $\pm v$ such that $|L_j(\pm v)|\le|\det A^*A|^{1/2}$ for each real form
> $j=1,\ldots,r$ (and the corresponding complex bounds hold).

Use in the paper: take the columns of $A$ to be a $\mathbb Z$-basis of the
rank-$(\omega-1)$ lattice $F(a,b)$ and take the ambient coordinate functionals
as $L_j$.  With all coordinate bounds equal to
$\det(F(a,b))^{1/(\omega-1)}$, the theorem gives a nonzero lattice vector with
that $\ell^\infty$-bound.

## Faltings (1983), Inventiones mathematicae 73, 349–366

Source file: `faltings-1983-abelian-varieties.pdf`.

Checked article: G. Faltings, *Endlichkeitssätze für abelsche Varietäten über
Zahlkörpern*, Inventiones mathematicae **73** (1983), 349–366.

### Mordell conjecture

Faltings' Satz 7, on journal page 365, states:

> Satz 7 (Mordell-Vermutung). Sei $X/K$ eine glatte Kurve vom Geschlecht $g>2$.
> Dann ist $X(K)$ endlich.

Translation and use: for a smooth curve $X$ over a number field $K$ with genus
$g>2$, the set $X(K)$ of $K$-rational points is finite.  This exactly supports
CL-05.  It does not supply a uniform effective height bound over the family of
Frey curves, so it does not close CORE-2/CORE-3.

## Oesterlé (1988), Séminaire Bourbaki, exposé 694

Source file: `oesterle-1988-nouvelles-approches-fermat.pdf`.

Checked version: J. Oesterlé, *Nouvelles approches du «théorème» de Fermat*,
Astérisque **161–162** (1988), Séminaire Bourbaki 1987/88, exposé no. 694,
pp. 165–186; Numdam PDF.

### Polynomial/function-field abc

On printed page 169, Théorème 2 states the polynomial abc theorem:

> Soient $k$ un corps et $P,Q,R$ trois polynômes non nuls de $k[X]$, premiers
> entre eux, tels que $P+Q+R=0$, dont l'un au moins a une dérivée $\ne0$.
> Soit $s$ le nombre de racines distinctes de $PQR$ dans une clôture algébrique
> de $k$. On a alors
> $\sup(\deg P,\deg Q,\deg R)<s$.

This supports the Mason--Stothers statement used as CL-06, including the
positive-characteristic hypothesis that at least one polynomial has nonzero
derivative.  Oesterlé's exposition includes a proof.  It is not the 1981/1984
original Stothers/Mason publication; it is recorded here as an exact published
secondary source.  The original Stothers PDF is paywalled and returned HTTP 403
during the 2026-08-17 source search.

### abc and modified Szpiro: source-backed precision

On printed page 169, Conjecture 3 states the abc conjecture:

> Pour tout $\varepsilon>0$, il existe $C(\varepsilon)>0$ tel que
> $\sup(|a|,|b|,|c|)\le C(\varepsilon)\operatorname{rad}(abc)^{1+\varepsilon}$
> pour tout triplet $(a,b,c)$ d'entiers non nuls premiers entre eux vérifiant
> $a+b+c=0$.

Immediately afterward Oesterlé says that he will prove abc equivalent to
Conjectures 4 and $4'$, which bound
$\max(|c_4(E)|^3,|c_6(E)|^2)$ by $C(\varepsilon)N_E^{6+\varepsilon}$ for a
minimal model of $E$ (Conjecture $4'$ restricts to semi-stable elliptic curves
over $\mathbb Q$).  The equivalence proof continues on printed page 170.

**Precision finding:** this source directly supports equivalence between abc
and the modified Szpiro/Conjecture 4′ formulation.  Oesterlé's discriminant
form (strong Szpiro, Conjecture 2) is closely related and implies a weak abc
form, but the source page checked so far does not state verbatim that the
discriminant-only form is equivalent to full abc.  Any ledger use of CL-02 must
therefore name the modified invariant form or supply the missing bridge from
that exact discriminant form.  This is a source-precision issue, not a proof of
abc or Szpiro.

## Mochizuki (May 2020), Inter-universal Teichmüller Theory III

Source file: `mochizuki-2020-iutt-iii.pdf`.

Checked version: Shinichi Mochizuki, *Inter-universal Teichmüller Theory III:
Canonical Splittings of the Log-theta-lattice*, May 2020, RIMS author-hosted
PDF (199 pages).  This is a source anchor only: storing and quoting the paper
does not verify its proof and does not affect the OPEN CORE-3 sub-obligation
`core3.iut-corollary-312-independently-verified`.

### Corollary 3.12

On journal pages 173--174, Corollary 3.12 is titled “Log-volume Estimates for
Θ-Pilot Objects” and begins:

> Suppose that we are in the situation of Theorem 3.11. Write
> $-|\!\log(\Theta)|\in\mathbb R\cup\{+\infty\}$ for the procession-normalized
> mono-analytic log-volume ... of the holomorphic hull ... of the union of the
> possible images of a Θ-pilot object ..., in the multiradial representation of
> Theorem 3.11, (i), which we regard as subject to the indeterminacies
> (Ind1), (Ind2), (Ind3) described in Theorem 3.11, (i), (ii).

It then defines $-|\!\log(q)|$ as the procession-normalized mono-analytic
log-volume of the image of a q-pilot object, *not* regarded as subject to
Ind1--Ind3, and concludes:

> Then it holds that $-|\!\log(\Theta)|\in\mathbb R$, and
> \[
>   -|\!\log(\Theta)| \ge -|\!\log(q)|.
> \]

The hypotheses inherit the full “situation of Theorem 3.11,” including initial
Θ-data, the log-theta-lattice construction, and the cited Kummer/multiradial
representation.  Those hypotheses are not discharged here.  In particular, the
Scholze--Stix concern about identification of objects across theaters remains
a blocking reason; this source quote neither closes nor adjudicates that
dispute.
