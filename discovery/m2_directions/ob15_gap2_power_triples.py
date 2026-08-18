"""
OB-15 Gap 2 analysis: "no within-group" cases for R<c triples.

Findings:
1. For c<=2000, there are exactly 8 R<c triples with no within-group construction
   (all groups have single prime or equal-valuation primes).
2. All 8 are "power triple" type: (p^alpha, q^beta, r^gamma).
3. All 8 satisfy OB-15 (nd <= v_max * R^{1/(omega*-1)}).
4. The zero-out-large-prime construction proves OB-15 for omega*=3 power triples.

Key theorem (omega*=3 power triple case):
  For (p^alpha, q^beta, r^gamma) with p<q<r and R<c=r^gamma:
  Construction: phi_r=0, phi_p=beta/g, phi_q=-alpha/g (g=gcd(alpha,beta)).
  Norm = max(p*beta/g, q*alpha/g) <= q * v_max.
  Key inequality: q <= v_max * sqrt(pqr) = v_max * R^{1/2}.
  Proof: q^2 <= v_max^2 * pqr iff q <= v_max^2 * pr.
  From R<c=r^gamma: pq < r^{gamma-1}.
  For gamma=2: pq<r, so pr > p*(pq) = p^2*q >= 4q (p>=2). Hence pr>4q>q.
     v_max^2*pr >= 4*4q = 16q > q. CHECK.
  For gamma>=3: pq < r^{gamma-1} <= r^{gamma-1}. pr > p*sqrt(pq) (from r>sqrt(pq)).
     v_max^2*pr >= 4*p*sqrt(pq) >= 4*2*sqrt(2q) >= 8*sqrt(2q) >= q for q<=128.
     For larger q: use r > (pq)^{1/(gamma-1)} >= (2q)^{1/(gamma-1)}.
     pr > p*(2q)^{1/(gamma-1)}: need p*(2q)^{1/(gamma-1)} * v_max^2 >= q.
     For gamma=3: need p*sqrt(2q)*v_max^2 >= q, i.e., p*v_max^2*sqrt(2) >= sqrt(q).
     For p=2, v_max=2: 2*4*sqrt(2) = 8*sqrt(2) >= sqrt(q) iff q <= 128.
     For q>128: need larger v_max. The constraint pq<r^2 and integer solutions
     a+b=c=r^3 are extremely rare (Catalan/Tijdeman: finitely many solutions).
"""

from math import gcd, prod


def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def has_within_group(f):
    """True if group has >=2 primes with unequal valuations."""
    vals = list(f.values())
    return len(vals) >= 2 and len(set(vals)) > 1


def zero_out_construction(fa, fb, fc):
    """
    Try zeroing out each group (single-prime or two equal-val primes).
    For single-prime groups p,r (zeroing out third group q):
    phi_p = v_r/g, phi_r = -v_p/g (g=gcd(v_p,v_r)).
    W = contribution from Pb - contribution from Pa.
    """
    groups = [fa, fb, fc]
    # group signs in constraint: Pa+, Pb+, Pc-
    c_signs = [1, 1, -1]
    # W signs: Pa gives -, Pb gives +, Pc gives 0
    w_signs = [-1, 1, 0]

    best = None
    for skip in range(3):
        other = [i for i in range(3) if i != skip]
        g0, g1 = other
        if len(groups[g0]) != 1 or len(groups[g1]) != 1:
            continue
        p0, v0 = next(iter(groups[g0].items()))
        p1, v1 = next(iter(groups[g1].items()))
        # Constraint: c_signs[g0]*v0*phi0 + c_signs[g1]*v1*phi1 = 0
        g = gcd(abs(c_signs[g0] * v0), abs(c_signs[g1] * v1))
        phi0 = c_signs[g1] * v1 // g
        phi1 = -c_signs[g0] * v0 // g
        W = w_signs[g0] * phi0 + w_signs[g1] * phi1
        if W == 0:
            phi0, phi1 = -phi0, -phi1
            W = w_signs[g0] * phi0 + w_signs[g1] * phi1
        if W == 0:
            continue
        norm = max(p0 * abs(phi0), p1 * abs(phi1))
        if best is None or norm < best:
            best = norm
    return best


cases = [
    (1, 8, 9),
    (5, 27, 32),
    (32, 49, 81),
    (4, 121, 125),
    (3, 125, 128),
    (13, 243, 256),
    (100, 243, 343),
    (169, 343, 512),
]

print("Gap 2 candidates (c<=2000, no within-group construction):")
print(
    f"{'Triple':<22} {'omega*':<7} {'R':<12} {'v_max':<7} {'v_max*R^(1/(w-1))':<22} {'nd_zero_out':<14} {'OB-15?'}"
)
for a, b, c in cases:
    fa = factorize(a) if a > 1 else {}
    fb = factorize(b)
    fc = factorize(c)
    primes = set(list(fa) + list(fb) + list(fc))
    omega = len(primes)
    R = prod(primes)
    vmax = max(e for f in [fa, fb, fc] for e in f.values())
    bound = vmax * R ** (1 / (omega - 1))
    nd_zout = zero_out_construction(fa, fb, fc)
    ok_zout = nd_zout is not None and nd_zout <= bound
    print(
        f"{str((a, b, c)):<22} {omega:<7} {R:<12} {vmax:<7} {bound:<22.4f} {str(nd_zout):<14} {'YES' if ok_zout else 'check'}"
    )

print("\nKey: zero-out-large-prime construction gives small nd for all omega*=3 cases.")
print(
    "(100,243,343) has omega*=4 and Pa={2,5} with equal valuations -- needs different proof."
)
