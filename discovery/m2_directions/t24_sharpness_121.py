"""
T24 — Analytical sharpness proof for type (1,2,1) [F12]

CLAIM: sup_{type (1,2,1)} ratio = 2^{-1/3} (the F7a bound is sharp).

TYPE (1,2,1): a=p (prime), b=q*r (q<r primes), c=s (prime), a ≤ b ≤ c.
  R = p*q*r*s, ω=4, exponent 1/(ω-1) = 1/3.
  F10: nd_norm = second smallest of {min_Pa, min_Pb, min_Pc}
               = second smallest of {p, q, s}  (since min_Pa=p, min_Pb=q, min_Pc=s)

WHEN b = 2*q (so r=2, the smallest prime factor of b):
  nd_norm = second smallest of {p, 2, s}
          = p  (when 2 < p < s, i.e., p ≥ 3 and s > p)
  ratio = p / (2*p*q*s)^{1/3}  with c = s = p + 2*q

ANALYTICAL SUPREMUM:
  Let t = q/p (with q ≥ p/2 so b=2q ≥ p=a, i.e., t ≥ 1/2).
  s = p + 2q = p(1 + 2t), so s/p = 1+2t.
  R = p * 2 * q * s = 2 * t*p * (1+2t)*p * p = 2*t*(1+2t)*p^3  (if q=t*p, approx)

  More precisely: ratio = p / (2*p*q*(p+2q))^{1/3}
                       = p^{1/3} / (2*q*(p+2q))^{1/3}
                       = (p / (2*q*(p+2q)))^{1/3}

  f(p,q) = p / (2*q*(p+2q))  — need to maximize over p prime, q prime, q ≥ p/2

  Set q = p/2 (limit t→1/2):
  f → p / (2*(p/2)*(p+p)) = p / (p * 2p) = 1/(2p) → 0 as p→∞? NO!

  Wait: f(p,q) = p / (2*q*(p+2q)).
  With q = p/2: f = p / (2*(p/2)*(p+p)) = p / (p * 2p) = 1/(2p). That → 0.

  Let me redo: set b = 2q ≈ a = p, so q ≈ p/2 (but q must be prime ≥ p/2).

  Actually the correct formula: let q be MUCH SMALLER than p.
  But b = 2q ≥ p requires q ≥ p/2. So q ≥ p/2.

  f(p,q) = p / (2*q*(p+2q))
  For fixed p, minimize over q ≥ p/2:
    d/dq [2q*(p+2q)] = 2(p+2q) + 2q*2 = 2p + 4q + 4q = 2p + 8q > 0
    So 2q*(p+2q) is increasing in q, so f(p,q) is DECREASING in q.
    Maximum of f over q≥p/2 is at q = p/2 (minimum allowed q).

  So max f = f(p, p/2) = p / (2*(p/2)*(p+p)) = p / (p * 2p) = 1/(2p) → 0.

  Hmm, that gives ratio → 0 not 2^{-1/3}.

  Wait — I have the wrong formula. Let me recheck the F7a proof structure.

  F7a: type (1,2,1) has a=p, b=q1*q2, c=s (all prime or prime products).

  Constraint: a + b = c, i.e., p + q1*q2 = s.

  nd_norm = second_smallest{min_Pa, min_Pb, min_Pc}
          = second_smallest{p, q1, s}  (assuming q1 ≤ q2, min_Pb = q1)

  For ratio to be large: need nd_norm large AND R small.
  nd_norm = max(min(p,q1), ...) — actually second smallest of {p, q1, s}.

  Second smallest of {p, q1, s} where p,q1,s > 0:
  If q1 ≤ p ≤ s: second = p. ratio = p/(p*q1*q2*s)^{1/3}.
  If p ≤ q1 ≤ s: second = q1. ratio = q1/(p*q1*q2*s)^{1/3}.

  Case: q1 = 2 (b = 2*q2):
    nd_norm = second of {p, 2, s} = p (for p > 2).
    ratio = p / (p * 2 * q2 * s)^{1/3} = p / (2*p*q2*(p+2*q2))^{1/3}
          = p^{2/3} / (2*q2*(p+2*q2))^{1/3}

  Now maximize over p, q2 with q2 ≥ 1, p+2*q2 = s prime, p prime, q2 prime, 2*q2 ≥ p.

  Wait: we need b = 2*q2 ≥ a = p (canonical a ≤ b), so q2 ≥ p/2.

  ratio = p^{2/3} / (2*q2*(p+2*q2))^{1/3}

  Maximize: let u = q2/p (u ≥ 1/2):
  ratio = p^{2/3} / (2*u*p*(1+2u)*p)^{1/3} * p^{1/3}
        NO... let me be careful.

  2*q2*(p+2*q2) = 2*u*p*(p+2*u*p) = 2*u*p * p*(1+2u) = 2*u*(1+2u)*p^2

  ratio = p^{2/3} / (2*u*(1+2u)*p^2)^{1/3}
        = p^{2/3} / (2*u*(1+2u))^{1/3} / p^{2/3}
        = 1 / (2*u*(1+2u))^{1/3}

  So ratio = 1 / (2*u*(1+2u))^{1/3} where u = q2/p ≥ 1/2.

  Maximize over u ≥ 1/2: need to minimize g(u) = 2*u*(1+2u) = 2u + 4u^2.
  g'(u) = 2 + 8u > 0 for all u > 0. So g is increasing; min at u = 1/2.
  g(1/2) = 2*(1/2)*(1+1) = 1*2 = 2.

  ratio_max = 1 / 2^{1/3} = 2^{-1/3}.  ✓

  This is achieved in the LIMIT u → 1/2, i.e., q2 → p/2, i.e., b = 2*q2 → p = a.

  Since q2 must be an integer ≥ p/2 (and prime), the supremum is never achieved,
  but is approached as p → ∞ with q2 the smallest prime ≥ p/2.

VERIFICATION: check that ratio = 1/(2u(1+2u))^{1/3} formula matches numerical data.
"""

import math

def factorize(n):
    f = {}; d = 2
    while d*d <= n:
        while n%d == 0: f[d]=f.get(d,0)+1; n//=d
        d += 1
    if n > 1: f[n] = 1
    return f

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

def isprime(n):
    if n<2: return False
    if n==2: return True
    if n%2==0: return False
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True

def is_squarefree(n):
    return all(v==1 for v in factorize(n).values())

print("T24: Sharpness of 2^{-1/3} for type (1,2,1)")
print("="*55)
print()
print("Analytical formula (b=2*q2 subfamily):")
print("  ratio = 1 / (2*u*(1+2*u))^{1/3}  where u = q2/p ≥ 1/2")
print("  Supremum at u = 1/2: ratio_max = 2^{-1/3} =", round(2**(-1/3), 6))
print()

# Verify against numerical data
print("Numerical verification — growing pairs (p, q2) with q2/p → 1/2:")
print(f"  {'p':>6}  {'q2':>6}  {'u=q2/p':>8}  {'ratio_exact':>12}  {'ratio_formula':>13}  {'diff':>10}")
print("  " + "-"*65)

count = 0
for p in range(100, 100000, 100):
    if not isprime(p):
        p += 1
        while not isprime(p): p += 1
    q2 = (p + 1) // 2  # smallest integer ≥ p/2
    while not isprime(q2): q2 += 1
    c = p + 2 * q2
    if not isprime(c): continue
    if 2 * q2 < p: continue  # ensure b ≥ a

    R = p * 2 * q2 * c
    nd = p  # second smallest of {p, 2, c} when p < c
    ratio_exact = nd / R**(1/3)

    u = q2 / p
    ratio_formula = 1.0 / (2*u*(1+2*u))**(1/3)

    print(f"  {p:>6}  {q2:>6}  {u:>8.4f}  {ratio_exact:>12.8f}  {ratio_formula:>13.8f}  {abs(ratio_exact-ratio_formula):>10.2e}")
    count += 1
    if count >= 12: break

print()
print(f"2^{{-1/3}} = {2**(-1/3):.8f}")
print()

# Show the approaching sequence more dramatically
print("Sequence approaching 2^{-1/3} from below (p twin to 2*q2):")
print(f"  {'p':>8}  {'q2':>8}  {'ratio':>12}  {'gap to 2^(-1/3)':>16}")
target = 2**(-1/3)
count = 0
for p in range(3, 500000, 2):
    if not isprime(p): continue
    q2 = (p+1)//2
    while not isprime(q2): q2 += 1
    if 2*q2 < p: continue
    c = p + 2*q2
    if not isprime(c): continue

    R = p * 2 * q2 * c
    ratio = p / R**(1/3)

    print(f"  {p:>8}  {q2:>8}  {ratio:>12.8f}  {target-ratio:>16.10f}")
    count += 1
    if count >= 15: break

print()
print("CONCLUSION F12:")
print("  The F7a upper bound 2^{-1/3} for type (1,2,1) is SHARP (not improvable).")
print("  The sup is approached but never achieved, as p→∞ with q2 = ⌈p/2⌉ (prime).")
print("  The sharp formula: ratio = 1/(2*u*(1+2*u))^{1/3} at u = q2/p → 1/2.")
print()
print("  Implication for P_ineq:")
print("  For type (1,2,1) triples: min_nd_norm ≤ 2^{-1/3} * R^{1/3} < R^{1/3}.")
print("  This gives ψ_nd = O(R^{1/3}) = O(c^{(1+ε)/3}) — useful only if ω ≥ 4.")
print("  But squarefree triples have quality < 1 (R ≥ c), so c ≤ R < R^{1+ε} trivially.")
print()
print("  Key limitation: Pasten lattice analysis for squarefree triples only covers")
print("  quality-< 1 examples. High-quality abc triples (quality > 1) involve prime")
print("  powers and are outside the squarefree setting.")
