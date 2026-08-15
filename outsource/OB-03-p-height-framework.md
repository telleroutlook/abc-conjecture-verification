# Problem OB-03 — P_height: formal height/rad framework construction (CORE-2)

**Type:** algebraic number theory / formal verification
**Non-circularity:** This problem does not assume the abc conjecture, Szpiro's conjecture,
IUT Corollary 3.12, known abc triples, or any fitted parameter K_ε. It asks only for the
construction of a formally-verified height and rad framework as a building block — not for
the key inequality itself.

---

## All definitions (self-contained — everything is here)

**The rad function.** For a non-zero integer n, define:
```
rad(n) = ∏_{p prime, p | n} p
```
(product of distinct prime factors of n, ignoring multiplicities). By convention rad(±1) = 1.
Properties required: (1) rad(n) = rad(|n|); (2) rad(p^k) = p for any prime p, k ≥ 1;
(3) for coprime m, n: rad(mn) = rad(m) · rad(n).

**Coprime triple.** A triple (a, b, c) of positive integers is an abc-triple if:
- a + b = c
- gcd(a, b) = 1 (hence gcd(a, c) = gcd(b, c) = 1)
- a, b, c ≥ 1

**The quality of an abc-triple.** q(a, b, c) = log c / log rad(abc).

**The height/rad ratio target.** The key inequality (CORE-3, CL-10 — NOT this problem) asserts:
for all ε > 0 there exists K_ε > 0 such that for all coprime triples (a, b, c):
    c ≤ K_ε · rad(abc)^(1+ε)

This problem (OB-03) asks only for the construction of the formal framework needed to
STATE this inequality rigorously and to verify its premises — NOT to prove it.

**Faltings height (minimal Weierstrass form version).** For an elliptic curve E/Q with
minimal Weierstrass equation y² + a₁xy + a₃y = x³ + a₂x² + a₄x + a₆, the minimal
discriminant is:
```
Δ_min(E) = -b₂²b₈ - 8b₄³ - 27b₆² + 9b₂b₄b₆
```
where b₂ = a₁² + 4a₂, b₄ = a₁a₃ + 2a₄, b₆ = a₃² + 4a₆, b₈ = a₁²a₆ - a₁a₃a₄ + 4a₂a₆ + a₂a₃² - a₄².

The (logarithmic naive Faltings) height is approximately:
```
h_F(E) ≈ (1/12) log |Δ_min(E)|
```
(More precisely, the Faltings height is a canonical Arakelov-theoretic height; the above
is a computable approximation via the minimal model. For the purposes of this framework
construction, the naive height (1/12) log |Δ_min| is sufficient.)

**The Frey curve.** For a coprime triple (a, b, c) with a + b = c and a odd, b even
(possible by permuting a, b), the Frey elliptic curve is:
```
E_{a,b,c}: y² = x(x − a)(x + b)
```
Its minimal discriminant satisfies:
```
log |Δ_min(E_{a,b,c})| = log(|abc|²) − 8 log 2 + O(1)
                       = 2(log a + log b + log c) − 8 log 2 + O(1)
```
Its conductor satisfies: N_E = rad(2abc) · δ(a,b,c) where δ divides rad(2abc) (the
exact factor δ depends on 2-adic and p-adic semi-stability conditions).

**The framework need (CORE-2 / CL-09).** P_height is a construction that provides:
1. A formally-verified implementation of rad(n) satisfying the three properties above.
2. A formally-verified computation of h_F(E_{a,b,c}) (or its naive approximation) for
   any given abc-triple.
3. A bound of the form: log |Δ_min(E_{a,b,c})| ≤ 2 log c + C for some explicit C.
4. An upper bound: log N_E ≤ 2 log rad(abc) + C_2 for some explicit C_2.

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
satisfies: rad multiplicative (for coprimes), rad(p^k) = p, rad(1) = 1.

**OB-03-B (discriminant bound).** For the Frey curve E_{a,b,c} with a + b = c, a,b,c ≥ 1
coprime, a odd, b even: prove the explicit bound
```
(1/12) log |Δ_min(E_{a,b,c})| ≤ (1/6) log(abc) + C
```
for an explicit C > 0 (e.g., C = 8/12 · log 2), with a formal proof that requires NO
abc-equivalent hypothesis.

**OB-03-C (conductor bound).** For the same Frey curve: prove the explicit upper bound
```
log N_E ≤ 2 log rad(abc) + C_2
```
for an explicit C_2 > 0, with a formal proof that requires NO abc-equivalent hypothesis.

**OB-03-D (quality bound from below).** Prove that for ANY ε > 0, there exist coprime
triples (a, b, c) with q(a, b, c) = log c / log rad(abc) > 1. (I.e., the quality can
exceed 1, so the key inequality c ≤ K_ε rad(abc)^{1+ε} is not trivially false.)
This is provable from known examples and does NOT require proving abc.

---

## Proof skeleton to be closed

### Step 1 — rad function verification

**Draft**: The rad function is computed by factoring n and taking the squarefree part.
The three properties follow directly from unique factorization (fundamental theorem of
arithmetic).

**What to close for Step 1**: A formally-verified proof (in Python with doctests or in
a proof assistant) that the implementation of rad satisfies: rad(1)=1, rad(p)=p for prime
p, rad(p^k)=p for k≥1, rad(mn)=rad(m)·rad(n) for gcd(m,n)=1. The Python implementation
in proof/m1/rad.py already exists — this step is to produce a formal proof of its
correctness.

### Step 2 — Frey curve minimal model

**Draft**: For a + b = c, a odd, b ≡ 0 (mod 4): the model y² = x(x-a)(x+b) has
b₂ = 0, b₄ = -(ab + ac + bc)/2 (needs care), b₆ = a²bc/4 (approx), and
Δ = 2^4 · (abc)^2 · (1 + O(1/(abc))) (rough; exact formula in Silverman AEC Appendix C).
The exact formula requires 2-adic analysis.

**What to close for Step 2**: A formally-verified derivation of log |Δ_min(E_{a,b,c})|
with explicit remainder O(1) that is independent of a,b,c. Specifically: prove that
log |Δ_min| ≥ 2 log c − C for some computable C.

### Step 3 — Conductor upper bound

**Draft**: For the Frey curve, the conductor N_E is computed via Ogg's formula:
log N_E = Σ_p f_p log p, where f_p is the Artin conductor exponent at p.
For p | abc and p odd: f_p = 1 or 2 depending on additive vs multiplicative reduction.
For p = 2: f_2 can be up to 8 (bounded 2-adic contribution).
Therefore: N_E | rad(2abc)² and log N_E ≤ 2 log rad(abc) + 8 log 2.

**What to close for Step 3**: A formally-verified proof of: log N_E ≤ 2 log rad(abc) + C₂
for C₂ = 8 log 2 + O(1). This uses the theory of Néron models and Ogg's formula — the
key algebraic facts needed are: (1) good/multiplicative reduction at p ∤ 2 gives f_p = 0/1;
(2) the conductor exponent at p is bounded by 2 + val_p(Δ_min); (3) for p odd, f_p ≤ 2.

### Step 4 — Quality lower bound (OB-03-D)

**Draft**: The known triple (a,b,c) = (2, 2^n - 2, 2^n) has quality approaching 1 as
n → ∞. To get quality > 1, note: (1, 8, 9) has quality log 9 / log(1·8·9) = log 9 / log 72
≈ 2.197 / 4.277 ≈ 0.514. A better example: (5, 4·3^5·..., c) where c/rad(abc) > 1.
A simple example with quality > 1: (a,b,c) = (1, 2^5 · 3^2 - 1, 2^5 · 3^2) = (1, 287, 288).
rad(1 · 287 · 288) = rad(287 · 288) = rad(7 · 41 · 2^5 · 3^2) = 2·3·7·41 = 1722.
Quality = log 288 / log 1722 ≈ 5.663 / 7.451 ≈ 0.76 < 1. (Still < 1.)
A high quality example: (a,b,c) = (1, 2^5·3^3 = 864, 865) — no, 865 = 5·173.
rad = 2·3·5·173 = 5190. quality = log 865 / log 5190 ≈ 0.83. Still < 1.
Better: use known high-quality examples from literature (e.g. quality 1.6299 for (2, 3^10·109, ...)).
NOTE: for OB-03-D, a single example with quality > 1 suffices — this IS available in the
literature and can be cited (it is not a proof of abc, just a lower bound on quality).

**What to close for Step 4**: Exhibit ONE explicit coprime triple (a,b,c) with
q(a,b,c) > 1, with explicitly computed rad(abc) and log c / log rad(abc).

---

## Acceptance criteria

1. **COMPLETE**: All four sub-claims (A, B, C, D) are formally verified with explicit
   constants C, C₂. The framework is ready to be used as input to CORE-3 once CORE-3
   (the key inequality) is proved.
2. **PARTIAL-ABC**: Sub-claims A and D complete; B and C partial with explicit gaps
   identified (e.g., "the 2-adic conductor bound requires Ogg's formula for specific
   2-adic types").
3. **PARTIAL-D**: Sub-claims A, B, C complete; D requires only a single high-quality
   example to be verified (can be provided).
4. **INCONCLUSIVE**: Any sub-claim found to require abc-equivalent input — identify
   which step and why. (Note: the current understanding is that all four sub-claims are
   PROVABLE without abc-equivalent input, so an inconclusive result here would be
   surprising and should be fully documented.)

---

## Numerical anchor (sanity only, not an input to the proof)

For (a,b,c) = (1, 8, 9) (coprime: gcd(1,8)=1, 1+8=9):
- rad(1) = 1, rad(8) = 2, rad(9) = 3. So rad(abc) = rad(1·8·9) = rad(72) = 2·3 = 6.
- log |Δ_min(E_{1,8,9})| ≈ 2(log 1 + log 8 + log 9) − 8 log 2 = 0 + 2·2.079 + 2·2.197 − 5.545 ≈ 3.067
- (1/12) · 3.067 ≈ 0.256. This is a sanity check for Step 2; it is NOT an input to the proof.
- N_E ≤ rad(2·1·8·9)² = rad(144)² = 6² = 36. log 36 ≈ 3.58. 2 log rad(9) + C₂: 2 log 6 + C₂ = 3.58 + C₂. ✓
- Quality q(1,8,9) = log 9 / log 6 ≈ 2.197 / 1.792 ≈ 1.226 > 1. This confirms OB-03-D is feasible.
