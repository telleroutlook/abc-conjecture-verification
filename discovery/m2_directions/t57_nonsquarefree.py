"""
T57 — Pasten lattice for non-squarefree triples (v_p > 1 possible)

The squarefree Pasten lattice has constraint:
  Σ_{p|a} φ_p + Σ_{p|b} φ_p = Σ_{p|c} φ_p

Natural non-squarefree extension (weighted by p-adic valuations):
  Σ_{p|a} v_p(a)·φ_p + Σ_{p|b} v_p(b)·φ_p = Σ_{p|c} v_p(c)·φ_p

KEY QUESTIONS:
1. Does det(F) < rad(abc) still hold for non-squarefree triples?
2. What is the minimum non-degenerate norm? Is it still nd (second-smallest group min)?
3. Does W_ψ still encode c in a useful way?
4. Does quality > 1 become achievable, and how does the lattice behave there?
"""

import math

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def factorize(n):
    """Return list of (prime, exponent) pairs."""
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

def rad(n):
    return math.prod(factorize(n).keys())

def find_min_nondeg_ns(a, b, bound=8):
    """
    Find minimum non-degenerate vector for non-squarefree triple (a, b, c=a+b).
    Constraint: Σ v_p(a)·φ_p + Σ v_p(b)·φ_p = Σ v_p(c)·φ_p
    """
    c = a + b
    if c <= 0: return None
    fa = factorize(a)
    fb = factorize(b)
    fc = factorize(c)
    # All distinct primes
    all_primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    omega = len(all_primes)
    if omega == 0: return None

    # Build constraint: for each prime p, coefficient in phi:
    # v_a(p) * phi_p + v_b(p) * phi_p = v_c(p) * phi_p on the "group" side
    # Actually: sum over p in Pa of v_p(a)*phi_p + ... = sum over p in Pc of v_p(c)*phi_p
    # This is one linear constraint on phi.
    # pa_primes = primes appearing only in a (or in a and c, etc.)
    # Let's just define: the constraint is a single equation with coefficients:
    # coeff[p] = v_a(p) + v_b(p) - v_c(p)  (should sum phi[p]*coeff[p] = 0)
    # Wait: v_a(p) * phi_p + v_b(p) * phi_p - v_c(p) * phi_p = 0  for each p?
    # No -- the constraint is global: Σ_p (v_a(p) - v_c(p)) * phi_p + Σ_p v_b(p)*phi_p = 0
    # i.e., Σ_p (v_a(p) + v_b(p) - v_c(p)) * phi_p = 0

    constraint_coeffs = {}
    for p in all_primes:
        constraint_coeffs[p] = fa.get(p,0) + fb.get(p,0) - fc.get(p,0)

    # Non-degeneracy: S_b = Σ_{p in Pb} phi_p ≠ S_a = Σ_{p in Pa} phi_p
    # where Pa = primes appearing in a, Pb = primes in b (only)
    Pa = list(fa.keys())
    Pb = [p for p in fb.keys() if p not in fa]
    # (Note: for non-squarefree, same prime can appear in a and c, etc.)
    # For Wronskian: use ALL primes in a vs ALL primes in b
    Pa_all = list(fa.keys())
    Pb_all = list(fb.keys())

    best_norm = float('inf')
    best_phi = None
    best_W_phi = None
    best_W_psi = None

    from itertools import product as iproduct
    # Enumerate all phi with |phi_p| <= bound, filter by constraint
    # For small omega, just brute force
    if omega > 5:
        return None  # too large

    ranges = [range(-bound, bound+1)] * omega
    for vals in iproduct(*ranges):
        phi = {all_primes[i]: vals[i] for i in range(omega)}
        if all(v == 0 for v in vals): continue

        # Check constraint
        dot = sum(constraint_coeffs[p] * phi[p] for p in all_primes)
        if dot != 0: continue

        # Wronskian
        S_a = sum(phi[p] for p in Pa_all)
        S_b = sum(phi[p] for p in Pb_all)
        W_phi = S_b - S_a
        if W_phi == 0: continue

        norm = max(p * abs(phi[p]) for p in all_primes)
        if norm == 0: continue
        if norm < best_norm:
            best_norm = norm
            best_phi = dict(phi)
            best_W_phi = W_phi
            W_psi_a = sum(p * phi[p] for p in Pa_all)
            W_psi_b = sum(p * phi[p] for p in Pb_all)
            best_W_psi = W_psi_b - W_psi_a

    return best_norm, best_phi, best_W_phi, best_W_psi, fa, fb, fc, all_primes

# ── Test cases ───────────────────────────────────────────────────────────────
# Mix squarefree and non-squarefree triples
test_triples = [
    # Squarefree (baseline)
    (2, 3),    # 2+3=5, all squarefree
    (2, 5),    # 2+5=7
    (3, 5),    # 3+5=8=2^3 (non-squarefree c!)
    (5, 11),   # 5+11=16=2^4
    (1, 3),    # 1+3=4=2^2
    (1, 7),    # 1+7=8=2^3
    (1, 8),    # 1+8=9=3^2
    (1, 15),   # 1+15=16=2^4
    (1, 24),   # 1+24=25=5^2
    (1, 48),   # 1+48=49=7^2
    (2, 7),    # 2+7=9=3^2
    (2, 23),   # 2+23=25=5^2
    (4, 5),    # 4+5=9 (a=4=2^2 non-squarefree)
    (8, 1),    # 8+1=9 (a=8=2^3)
    (2, 2),    # skip (not coprime)
]

print("T57: Pasten lattice for non-squarefree triples")
print("="*90)
print(f"{'(a,b,c)':<18} {'squarefree':>12} {'rad':>6} {'qual':>5} "
      f"{'nd':>5} {'W_φ':>5} {'W_ψ':>8} {'W_ψ/c':>8} {'W_ψ/rad':>8}")
print("-"*90)

for (a, b) in test_triples:
    import math
    if math.gcd(a, b) != 1: continue
    c = a + b
    r = rad(a * b * c)
    quality = math.log(c) / math.log(r) if r > 1 else 0

    result = find_min_nondeg_ns(a, b, bound=6)
    if result is None:
        print(f"  ({a},{b},{c}): skipped (omega too large or no vector found)")
        continue
    norm, phi, W_phi, W_psi, fa, fb, fc, all_p = result
    if norm is None or norm == float('inf'):
        print(f"  ({a},{b},{c}): no non-degen vector found in bound")
        continue

    sq_a = all(v == 1 for v in fa.values())
    sq_b = all(v == 1 for v in fb.values())
    sq_c = all(v == 1 for v in fc.values())
    sq_label = "yes" if (sq_a and sq_b and sq_c) else "NO"

    Wc_ratio = f"{W_psi}/{c}" if c != 0 else "N/A"
    Wr_ratio = f"{W_psi}/{r}" if r != 0 else "N/A"

    print(f"  ({a},{b},{c}):{'':<5} {sq_label:>12} {r:>6} {quality:>5.3f} "
          f"{norm:>5} {W_phi:>5} {W_psi:>8} {Wc_ratio:>8} {Wr_ratio:>8}")

print()
print("LEGEND: qual = quality = log(c)/log(rad(abc)). qual > 1 means abc bound is non-trivial.")
print("        W_ψ = ψ-Wronskian of minimum non-degenerate vector.")
