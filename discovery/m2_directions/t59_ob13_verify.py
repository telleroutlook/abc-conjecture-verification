"""
T59 (revised) — Verify OB-13B with the THREE correct pair constructions.

REVIEWER'S STEP 1 GAP:
  Their construction phi_{p_a} = v_{p_c}(c), phi_{p_c} = v_{p_b}(b) requires
  v_{p_a}(a) = v_{p_b}(b), which is NOT generally true. Constraint FAILS for e.g. (4,5,9).

THREE CORRECT CONSTRUCTIONS for OB-13B:
  Let m_g = min prime in group g, v_g = v_{m_g}(g).

  (A) Pair (Pa, Pc): phi_{m_a} = -v_c,  phi_{m_c} = -v_a,  others = 0
      Constraint: v_a*(-v_c) + 0 = v_c*(-v_a)  =>  -v_a*v_c = -v_a*v_c  ALWAYS OK.
      W = 0 - (-v_c) = v_c  !=  0.
      Norm = max(m_a*v_c, m_c*v_a).

  (B) Pair (Pb, Pc): phi_{m_b} = -v_c,  phi_{m_c} = -v_b,  others = 0
      Constraint: 0 + v_b*(-v_c) = v_c*(-v_b)  =>  -v_b*v_c = -v_b*v_c  ALWAYS OK.
      W = (-v_c) - 0 = -v_c  !=  0.
      Norm = max(m_b*v_c, m_c*v_b).

  (C) Pair (Pa, Pb): phi_{m_a} = v_b,  phi_{m_b} = -v_a,  others = 0
      (and phi_{m_c_chosen} = 0 since constraint gives v_a*v_b + v_b*(-v_a) = 0 = Pc*phi)
      Constraint: v_a*v_b + v_b*(-v_a) = 0 = Pc side  ALWAYS OK.
      W = (-v_a) - (v_b) = -(v_a + v_b)  !=  0.
      Norm = max(m_a*v_b, m_b*v_a).

OB-13B: nd(a,b) <= v_max * R^{1/(omega*-1)}.
Proof: nd <= min(norm_A, norm_B, norm_C)
       = v_max * median(m_a, m_b, m_c)          [since each norm <= v_max*max(m_gi, m_gj)]
       <= v_max * R^{1/(omega*-1)}               [since median^(omega*-1) <= R]

OB-13C: reviewer's formula gives WRONG values for multi-prime groups (e.g. (1,15,16)).
  Correct nd can be smaller due to vectors using >2 primes simultaneously.
  OB-13C REMAINS OPEN.
"""

import math
from itertools import product as iproduct

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return factors

def rad(n):
    return math.prod(factorize(n).keys()) if n > 1 else 1

def brute_nd(a, b, bound=10):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    omega = len(all_p)
    if omega == 0: return None
    cc = {p: fa.get(p,0) + fb.get(p,0) - fc.get(p,0) for p in all_p}
    Pb, Pa = list(fb.keys()), list(fa.keys())
    best = float('inf')
    for vals in iproduct(*[range(-bound, bound+1)]*omega):
        phi = {all_p[i]: vals[i] for i in range(omega)}
        if all(v==0 for v in vals): continue
        if sum(cc[p]*phi[p] for p in all_p) != 0: continue
        W = sum(phi.get(p,0) for p in Pb) - sum(phi.get(p,0) for p in Pa)
        if W == 0: continue
        norm = max(p*abs(phi[p]) for p in all_p)
        if norm == 0: continue
        best = min(best, norm)
    return best if best < float('inf') else None

def three_construction_upper_bound(a, b):
    """
    Compute min over ALL prime pairs from different groups, with GCD reduction.
    For each pair (p, q) from groups (g1, g2):
      phi_p = v_q(g2) / gcd,  phi_q = -v_p(g1) / gcd   (or ± depending on which constraint)
      This satisfies constraint (C) and is non-degenerate.
      Norm = max(p * v_q/gcd, q * v_p/gcd).
    GCD reduction: scale by 1/gcd(v_p(g1), v_q(g2)) to get primitive integer vector.
    """
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    best = float('inf')
    best_label = ''

    def try_pair(p, vp, q, vq, label):
        nonlocal best, best_label
        g = math.gcd(vp, vq)
        norm = max(p * (vq // g), q * (vp // g))
        if norm < best:
            best, best_label = norm, label

    # Pair (Pa, Pc): all p_a in Pa, p_c in Pc
    for p_a, v_a in fa.items():
        for p_c, v_c in fc.items():
            try_pair(p_a, v_a, p_c, v_c, f"A:({p_a},{p_c})")

    # Pair (Pb, Pc): all p_b in Pb, p_c in Pc
    for p_b, v_b in fb.items():
        for p_c, v_c in fc.items():
            try_pair(p_b, v_b, p_c, v_c, f"B:({p_b},{p_c})")

    # Pair (Pa, Pb): all p_a in Pa, p_b in Pb
    for p_a, v_a in fa.items():
        for p_b, v_b in fb.items():
            try_pair(p_a, v_a, p_b, v_b, f"C:({p_a},{p_b})")

    return best if best < float('inf') else None, best_label

# ── Main test ────────────────────────────────────────────────────────────────
test_cases = [
    (2,3),(3,5),(5,11),       # squarefree (1,1,1)
    (2,13),(2,19),            # squarefree (1,1,2)
    (1,3),(1,7),(1,8),(1,15),(1,24),(1,48),  # non-squarefree
    (4,5),(8,1),(2,7),(2,23),
    (4,21),(9,16),(3,5),(5,3),
    (1,2**6-1),(1,2**8-1),   # Mersenne-adjacent
]

print("T59 (revised): Three-construction OB-13B verification")
print("="*100)
print(f"{'(a,b,c)':<16} {'brute':>6} {'3-constr':>9} {'OB13B':>6} {'v_max*R^1/(w-1)':>16} "
      f"{'best':>14} {'OB13C?':>7}")
print("-"*100)

all_b_pass = True

for (a, b) in test_cases:
    if math.gcd(a, b) != 1: continue
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = set(list(fa.keys()) + list(fb.keys()) + list(fc.keys()))
    omega = len(all_p)
    if omega < 2: continue
    v_max = max(max((fa.get(p,0) for p in all_p), default=0),
                max((fb.get(p,0) for p in all_p), default=0),
                max((fc.get(p,0) for p in all_p), default=0))
    R = rad(a * b * c)
    bound_b = v_max * R**(1/(omega-1))

    nd_brute = brute_nd(a, b, bound=8)
    nd_constr, label = three_construction_upper_bound(a, b)

    ob13b = "✓" if nd_brute is not None and nd_brute <= bound_b + 1e-9 else "✗"
    ob13c = "✓" if nd_constr == nd_brute else f"✗({nd_constr})"
    if ob13b == "✗": all_b_pass = False

    print(f"  ({a},{b},{c}){'':<5} {str(nd_brute):>6} {str(nd_constr):>9} {ob13b:>6} "
          f"{bound_b:>16.3f} {label:>14} {ob13c:>7}")

print()
print("="*100)
print(f"OB-13B (nd <= v_max*R^{{1/(omega-1)}}): {'ALL PASS ✓' if all_b_pass else 'SOME FAIL ✗'}")
print()
print("PROOF OF OB-13B (constructive):")
print("  For each triple, at least one of three constructions (A/B/C) gives")
print("  nd <= v_max * median({m_a, m_b, m_c}) <= v_max * R^{1/(omega*-1)}.")
print("  Proof: median(m_a,m_b,m_c)^{omega*-1} <= R  [by: the other omega*-1")
print("  distinct primes are each >= median, so their product >= median^{omega*-1}].")
print()
print("OB-13C STATUS: OPEN.")
print("  Reviewer's formula nd = min_pairs max(m_g1*v_g2, m_g2*v_g1) gives UPPER BOUND")
print("  but is NOT exact when the optimal vector uses >2 primes simultaneously.")
print("  Example: (1,15,16): formula=12, brute nd=9 (via phi_2=1,phi_3=3,phi_5=1).")
