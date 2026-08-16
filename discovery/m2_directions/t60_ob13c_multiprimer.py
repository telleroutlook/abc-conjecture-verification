"""
T60 — OB-13C: Multi-prime balanced-load constructions

For (1, b, c=q^k) with b=p1·p2·... (squarefree), the 2-prime formula fails.
The optimal uses a SUBSET T of Pb primes with a balanced allocation:
  phi_q = 1, phi_{pi} solves: Σ_{pi∈T} phi_{pi} = k (squarefree v_pi(b)=1)
  Minimize max(q, max_{pi} pi·|phi_{pi}|)
  Continuous optimum: equal loads pi·phi_{pi} = t → phi_{pi} = t/pi.
  Σ phi_{pi} = t·Σ(1/pi) = k → t = k / H(T) where H(T) = Σ_{pi∈T} 1/pi.
  Integer floor: round phi_{pi} to nearest integers minimizing max.

The formula for the continuous relaxation: t* = k / H(T).
The norm is max(q, t*) when all terms are equal.
In integers, rounding up one component gives norm = ceil_prime_norm.

KEY CLAIM for (1, b, q^k) squarefree b:
  nd(a=1, b) = min_T max(q, ceil_integer_LP(k, T))
where LP optimal (continuous) = k / Σ_{pi∈T} 1/pi.

We verify this for the two remaining cases and check the pattern.
"""

import math
from itertools import combinations, product as iproduct

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

def brute_nd(a, b, bound=10):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    omega = len(all_p)
    cc = {p: fa.get(p,0) + fb.get(p,0) - fc.get(p,0) for p in all_p}
    Pb_keys = list(fb.keys())
    Pa_keys = list(fa.keys())
    best = float('inf')
    for vals in iproduct(*[range(-bound, bound+1)]*omega):
        phi = {all_p[i]: vals[i] for i in range(omega)}
        if all(v==0 for v in vals): continue
        if sum(cc[p]*phi[p] for p in all_p) != 0: continue
        W = sum(phi.get(p,0) for p in Pb_keys) - sum(phi.get(p,0) for p in Pa_keys)
        if W == 0: continue
        norm = max(p*abs(phi[p]) for p in all_p)
        if norm == 0: continue
        best = min(best, norm)
    return best if best < float('inf') else None

def balanced_lp_norm(subset, k):
    """
    Continuous LP norm for distributing k across subset of Pb primes (all v_pi=1).
    t* = k / H(T) = k / Σ 1/pi.
    Returns (t*, integer_norm) where integer_norm is the best integer solution.
    """
    if not subset:
        return float('inf'), float('inf')
    H = sum(1/p for p in subset)
    t_star = k / H
    # Integer search: find integer phi_pi with Σ phi_pi = k, minimize max p*phi_pi
    # Upper bound: phi_pi near t_star/pi
    best_norm = float('inf')
    best_alloc = None
    # For small subsets, brute force integer allocations around LP solution
    n = len(subset)
    radius = max(3, int(t_star/min(subset)) + 2)
    for vals in iproduct(*[range(0, radius+1)]*n):
        if sum(vals) != k: continue
        norm = max(subset[i] * vals[i] for i in range(n)) if any(v > 0 for v in vals) else 0
        if norm < best_norm:
            best_norm = norm
            best_alloc = vals
    return t_star, best_norm, best_alloc

# ── Test cases for OB-13C multi-prime ────────────────────────────────────────
print("T60: OB-13C multi-prime balanced-load analysis")
print("="*90)

# Case 1: (1, 15, 16) — b=3·5, c=2^4
print("\n--- Case: (1, 15, 16) ---")
print("Pb={3,5}, Pc={2}, k=v_2(16)=4")
print("Pairwise best: max(3·4, 2·1)=12 (using pair 3,2)")
print()
for T in [(), (3,), (5,), (3,5)]:
    if not T: continue
    t_star, int_norm, alloc = balanced_lp_norm(list(T), 4)
    full_norm = max(2, int_norm)  # also include q=2 in norm
    print(f"  T={T}: LP t*={t_star:.3f}, integer_best={int_norm}, alloc={alloc}, norm=max(2,{int_norm})={full_norm}")
print(f"  Brute nd = {brute_nd(1,15, bound=8)}")

# Case 2: (1, 255, 256) — b=3·5·17, c=2^8
print("\n--- Case: (1, 255, 256) ---")
print("Pb={3,5,17}, Pc={2}, k=v_2(256)=8")
print("Pairwise best: max(3·8, 2·1)=24 (using pair 3,2)")
print()
for size in range(1, 4):
    for T in combinations([3,5,17], size):
        t_star, int_norm, alloc = balanced_lp_norm(list(T), 8)
        full_norm = max(2, int_norm)
        print(f"  T={T}: LP t*={t_star:.3f}, integer_best={int_norm}, alloc={alloc}, norm={full_norm}")
print(f"  Brute nd = {brute_nd(1,255, bound=10)}")

# General pattern: (1, prod_of_k_primes, power_of_2)
print("\n--- General pattern: (1, p1*p2, 2^k) ---")
print(f"{'triple':<22} {'brute':>7} {'best_T':>20} {'LP_t*':>8} {'formula':>8}")
print("-"*68)
for p1 in [3,5,7,11]:
    for p2 in [5,7,11,13]:
        if p2 <= p1: continue
        b = p1 * p2
        for k in [2,4,6,8]:
            c = 2**k
            if b + 1 != c: continue
            nd = brute_nd(1, b, bound=10)
            # Best subset
            best_lp, best_int, best_T_label = float('inf'), float('inf'), ""
            for size in range(1, 3):
                for T in combinations([p1,p2], size):
                    t_star, int_norm, alloc = balanced_lp_norm(list(T), k)
                    if int_norm < best_int:
                        best_int = int_norm
                        best_lp = t_star
                        best_T_label = str(T)
            formula = max(2, best_int)
            match = "✓" if formula == nd else f"✗(nd={nd})"
            print(f"  (1,{b},{c}){'':<8} {str(nd):>7} {best_T_label:>20} {best_lp:>8.3f} {formula:>8} {match}")

print()
print("CONCLUSION:")
print("  For (1,b,q^k) with b squarefree and q prime:")
print("  nd = max(q, min_T ceil_integer_LP(k,T)) where T⊂Pb.")
print("  LP formula: continuous optimum t* = k / Σ_{pi∈T} 1/pi.")
print("  For |T|=1: t* = k*pi, giving norm max(q,k*pi) — the pairwise formula.")
print("  For |T|=2: t* = k*p1*p2/(p1+p2), always < k*min(p1,p2) — strictly better!")
print("  The 2-prime balanced construction ALWAYS beats the pairwise (1-prime) formula")
print("  when T has ≥2 elements.")
