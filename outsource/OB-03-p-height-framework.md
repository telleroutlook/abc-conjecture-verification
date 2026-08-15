# Problem OB-03 — P_height: formal height/rad framework construction (CORE-2)

**Type:** algebraic number theory / formal verification
**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
IUT Corollary 3.12, known abc triples, or any fitted parameter K_ε. It asks only for the
construction of a formally-verified height and rad framework as a building block — not for
the key inequality itself.

**Review status (2026-08-15):** PARTIAL-ABC (with corrections). After applying the
corrections below, OB-03-A through OB-03-D are all provable unconditionally. See
`reviews/OB-03-review-2026-08-15.md` for the full referee report.

---

## All definitions (self-contained — everything is here)

**The rad function.** For a non-zero integer n, define:
```
rad(n) = ∏_{p prime, p | n} p
```
(product of distinct prime factors of |n|, ignoring multiplicities). By convention rad(±1) = 1.
Properties required: (1) rad(n) = rad(|n|); (2) rad(p^k) = p for any prime p, k ≥ 1;
(3) for coprime m, n with gcd(|m|,|n|)=1: rad(mn) = rad(m) · rad(n).

**Coprime triple.** A triple (a, b, c) of positive integers is an abc-triple if:
- a + b = c
- gcd(a, b) = 1 (hence gcd(a, c) = gcd(b, c) = 1)
- a, b, c ≥ 1

Write R = rad(abc) throughout.

**Parity restriction.** Steps 2–3 use the Frey curve construction under the assumption
**a odd, b even** (so c is odd). This covers exactly those coprime triples where one of
{a, b} is even; it does NOT cover both-odd triples such as (1, 1, 2). For both-odd triples
(where c = a+b is even), the roles of a and b cannot be exchanged to make b even without
changing the problem. A full treatment of all coprime triples requires handling the both-odd
case separately. Within the a-odd/b-even sub-family, all results below are unconditional.

**The quality of an abc-triple.** q(a, b, c) = log c / log rad(abc).

**The height/rad ratio target.** The key inequality (CORE-3, CL-10 — NOT this problem) asserts:
for all ε > 0 there exists K_ε > 0 such that for all coprime triples (a, b, c):
    c ≤ K_ε · rad(abc)^(1+ε)

This problem (OB-03) asks only for the construction of the formal framework needed to
STATE this inequality rigorously and to verify its premises — NOT to prove it.

**Discriminant height (not Faltings height).** For an elliptic curve E/Q with global
minimal model, define the *discriminant height*:
```
h_Δ(E) := (1/12) log |Δ_min(E)|
```
This is NOT the Faltings height. The Faltings height is an Arakelov-theoretic height that
also involves the Archimedean (complex period / modular form) contribution; see Murty–Pasten
(J. Number Theory 133, 2013), Theorem 5.1 for the precise formula. The two heights agree
only up to a normalization-dependent additive term that is NOT uniformly bounded by a
constant independent of the curve (see Löbrich, JTNB 29 (2017), Proposition 3.1).
For this framework, h_Δ is the object being bounded; it is explicitly NOT claimed to equal h_F.

**The Frey curve.** For a coprime triple (a, b, c) with a + b = c, **a odd, b even**, c odd:
```
E_{a,b,c} : y² = x(x − a)(x + b)
```
The exact Weierstrass invariants are (no approximation):
```
a₁ = a₃ = a₆ = 0,   a₂ = b − a,   a₄ = −ab
b₂ = 4(b−a),   b₄ = −2ab,   b₆ = 0,   b₈ = −a²b²
c₄ = 16(a² + ab + b²),   Δ_W = 16(abc)²
```
Since a is odd and b is even, a²+ab+b² is odd, so v₂(c₄) = 4.
The global minimal discriminant takes exactly one of two values
(Silverman AEC 2nd ed., Lemma VIII.11.3(a)):
```
|Δ_min| ∈ { 16(abc)², 2⁻⁸(abc)² }
```
corresponding to minimization parameter s ∈ {0, 1} with |Δ_min| = 2^{4−12s}(abc)².
Consequently:
```
2 log(abc) − 8 log 2  ≤  log|Δ_min|  ≤  2 log(abc) + 4 log 2     [★]
```
and dividing by 12:
```
(1/6) log(abc) − (2/3) log 2  ≤  h_Δ(E)  ≤  (1/6) log(abc) + (1/3) log 2
```
The upper bound `C = (1/3) log 2` is tight.

**Important correction — upper bound in terms of c only:**
The bound log|Δ_min| ≤ 2 log c + C_uniform for a constant C_uniform independent of (a,b,c)
is **FALSE**. The family (a,b,c) = (1, 2n, 2n+1) for n ≥ 1 satisfies abc = 2n(2n+1) → ∞
while c = 2n+1 grows as n, giving log|Δ_min| ≥ 2 log(2n(2n+1)) − O(1) which grows strictly
faster than 2 log c = 2 log(2n+1). The correct universal upper bound uses log(abc), not log c.

**The framework need (CORE-2 / CL-09).** P_height is a construction that provides:
1. A formally-verified implementation of rad(n) satisfying the three properties above.
2. A formally-verified computation of h_Δ(E_{a,b,c}) for any given abc-triple (a odd, b even).
3. A bound of the form: `log|Δ_min(E_{a,b,c})| ≤ 2 log(abc) + (4 log 2)` — equivalently,
   `h_Δ(E_{a,b,c}) ≤ (1/6) log(abc) + (1/3) log 2`. (The earlier form `2 log c + C` is false.)
4. An upper bound: `log N_E ≤ log R + 7 log 2` (equivalently `log N_E ≤ 2 log R + 7 log 2`
   as a looser valid form). The earlier claim `N_E | rad(2abc)²` is FALSE — see numerical
   anchor below.

These bounds are needed as INPUT to CORE-3 (the key inequality), but they do NOT require
any abc-equivalent hypothesis to establish.

---

## The theorem / claim to be verified

**Claim OB-03**: Construct and formally verify the following framework, which does NOT
assume abc, Szpiro, or any abc-equivalent hypothesis:

**OB-03-A (rad function).** Provide a formally-verified (in Python, Lean, Coq, Isabelle,
or Metamath) proof that for all non-zero integers n:
```
rad(n) = ∏_{p prime, p|n} p
```
satisfies: rad multiplicative for coprimes, rad(p^k) = p, rad(1) = 1.

**OB-03-B (discriminant height bound).** For the Frey curve E_{a,b,c} with a + b = c,
a,b,c ≥ 1 coprime, **a odd, b even**: prove the explicit bound
```
h_Δ(E_{a,b,c}) = (1/12) log|Δ_min(E_{a,b,c})| ≤ (1/6) log(abc) + C
```
for the explicit constant C = (1/3) log 2, with a proof requiring NO abc-equivalent
hypothesis. Note: h_Δ is the discriminant height, not the Faltings height.

**OB-03-C (conductor bound).** For the same Frey curve (a odd, b even): prove the explicit
upper bound
```
log N_E ≤ log R + 7 log 2     (equivalently  N_E ≤ 2⁷ R)
```
for an explicit bound, with a proof requiring NO abc-equivalent hypothesis. The earlier
form `log N_E ≤ 2 log rad(abc) + C_2` with C_2 = 7 log 2 is also valid but weaker.

**OB-03-D (quality above 1).** Prove that there exist coprime triples (a, b, c) with
q(a, b, c) = log c / log rad(abc) > 1. (The ε in "∀ε>0 ∃..." does not appear in the
conclusion predicate and is vacuous; the claim is simply the existence of one such triple.)
This is provable from a single explicit example and does NOT require proving abc.

---

## Proof skeleton to be closed

### Step 1 — rad function verification

**Draft.** The rad function is computed by factoring n and taking the squarefree part.
The three properties follow directly from unique factorization (fundamental theorem of
arithmetic): for gcd(|m|,|n|)=1, the prime-support sets of m and n are disjoint, and
rad(mn) = (product over support(m)) · (product over support(n)) = rad(m)·rad(n).

**Status:** CLOSED unconditionally. See referee report §Five/Step 1 for the full universal
proof.

---

### Step 2 — Frey curve minimal model

**Exact Weierstrass computation.** For y² = x(x−a)(x+b) = x³ + (b−a)x² − abx:
```
a₁=a₃=a₆=0,  a₂=b−a,  a₄=−ab
b₂ = 4(b−a),  b₄ = −2ab,  b₆ = 0,  b₈ = −a²b²
c₄ = b₂² − 24b₄ = 16(a²+ab+b²)
Δ  = −b₂²b₈ − 8b₄³ = 16a²b²(b−a)² + 16a²b²·4ab = 16(abc)²    (exact)
```
No approximation: Δ_W = 16(abc)² exactly.

For odd primes p|abc: coprimeness forces p to divide exactly one of a,b,c, hence
p∤c₄ (checked case by case), so the model is already minimal at p. The minimization
parameter s can only be in {0,1} from v₂(c₄)=4 (since a odd, b even makes a²+ab+b² odd).
This gives |Δ_min| ∈ {16(abc)², 2⁻⁸(abc)²} and bound [★].

**Status:** CLOSED. Exact constants C = (1/3)log2 for the upper bound.

**What to close for Step 2:** None for the (a odd, b even) subfamily. For the both-odd
subfamily, a separate argument is needed.

---

### Step 3 — Conductor upper bound

**Exact formula.** For odd primes p: v_p(c₄)=0 whenever p|abc (proved in Step 2), so Tate
algorithm Step 2 gives multiplicative reduction with f_p=1. For p∤abc: f_p=0 (good
reduction). Therefore:
```
N_E = 2^{f₂} · ∏_{p|abc, p odd} p
```
Silverman, *Advanced Topics*, Theorem IV.10.4 gives 0 ≤ f₂ ≤ 8.
Since b is even and a,c are odd, exactly one of a,b,c is even, so
∏_{p|abc, p odd} p = R/2 and:
```
N_E = 2^{f₂} · (R/2) ≤ 2⁷R,   log N_E ≤ log R + 7 log 2.
```

**Status:** CLOSED. Explicit C_2 = 7 log 2.

**Correction to earlier draft:** The claim `rad(N_E) = rad(2abc)` and `N_E | rad(2abc)²`
are both incorrect. For (1,8,9): N_E = 48, while rad(144)² = 6² = 36 < 48. The correct
bound is the log-inequality above.

---

### Step 4 — Quality lower bound (OB-03-D)

**Witness.** Take (a, b, c) = (1, 8, 9):
- gcd(1,8) = 1, 1+8 = 9. ✓
- rad(1·8·9) = rad(72) = 2·3 = 6.
- q(1,8,9) = log 9 / log 6 = 1.2262…  > 1.  ✓

(Note: the earlier draft computed log 9 / log 72 ≈ 0.514 — this is wrong because the
denominator should be log rad(abc) = log 6, not log abc = log 72.)

The same triple (1,8,9) witnesses OB-03-D for every ε > 0 since ε does not appear in
the conclusion predicate.

**Status:** CLOSED.

---

## Acceptance criteria

1. **COMPLETE**: All four sub-claims (A, B, C, D) formally verified with explicit constants
   C = (1/3) log 2 and C_2 = 7 log 2. Framework ready as input to CORE-3.
2. **PARTIAL-ABC**: Sub-claims A and D complete; B and C partial with explicit gaps.
3. **PARTIAL-D**: Sub-claims A, B, C complete; D requires only a single verified example.
4. **INCONCLUSIVE**: Any sub-claim found to require abc-equivalent input — identify which step.

**Current status after corrections:** All four sub-claims are CLOSED for the (a odd, b even)
sub-family. The both-odd subfamily (e.g. a=b=odd) requires a separate argument for B and C.

---

## Numerical anchor (sanity only, not an input to the proof)

For (a, b, c) = (1, 8, 9) (a odd, b even; gcd(1,8)=1, 1+8=9):

- rad(1·8·9) = rad(72) = 2·3 = 6.   R = 6.
- Exact discriminant: Δ_min = 82944 = 2¹⁰·3⁴.
  (Both v₂=10<12 and v₃=4<12 confirm the model is globally minimal.)
- log|Δ_min| = 11.3259…
- h_Δ = (1/12)·11.3259… = 0.9438…   [discriminant height, NOT Faltings height]
- Faltings height (LMFDB normalization): h_F ≈ −0.2988  [different from h_Δ; this
  illustrates they are not the same quantity]
- Conductor: N_E = 2⁴·3 = 48  (Stein–Watkins Table 3 for f₂=4; f₃=1 from multiplicative reduction)
- Bound check: N_E = 48 ≤ 2⁷·R = 128·6 = 768  ✓
- Earlier claim N_E ≤ rad(144)² = 36 is FALSE: 48 > 36.
- Quality: q = log 9 / log 6 ≈ 1.226 > 1.  ✓  (witnesses OB-03-D)
- h_Δ upper bound check: 0.9438 ≤ (1/6)log(72) + (1/3)log2 ≈ 0.7105 + 0.2310 = 0.9415…
  This is marginally tight; exact integer arithmetic confirms 0.9438… = (1/12)log 82944
  and the bound holds as 82944 = 2⁴·(72)² ≤ 2⁴·(abc)².
