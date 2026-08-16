"""
T56 — Wronskian pattern for minimum non-degenerate vector across all partition types

For each type (ma, mb, mc) and many triples, find the minimum non-degenerate vector
phi in the Pasten lattice and compute:
  W_phi = S_b(phi) - S_a(phi)   [phi-Wronskian, integer]
  W_psi = S_b(psi) - S_a(psi)   [psi-Wronskian, with psi_p = p*phi_p]

KEY QUESTION: Does W_psi encode a, b, c, rad(abc), or something else?

For type (1,1,1) we proved analytically: W_psi = -(p+q) = -c.
This script checks whether other types have similar "encoding" properties.
"""

from itertools import product as iproduct
import math

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

primes = [x for x in range(2, 300) if is_prime(x)]

def factorize_into_k_primes(n, k, used=set()):
    """Find all ways to write n as product of k distinct primes not in 'used'."""
    if k == 0:
        return [()] if n == 1 else []
    results = []
    for p in primes:
        if p in used: continue
        if p > n: break
        if n % p == 0:
            for rest in factorize_into_k_primes(n // p, k-1, used | {p}):
                results.append((p,) + rest)
    return results

def make_triples_of_type(ma, mb, mc, limit=15):
    """Generate triples (a,b,c) of type (ma,mb,mc): a has ma prime factors, etc."""
    results = []
    for pa_tuple in [primes[i:i+ma] for i in range(0, 30, 1)] if ma > 0 else [()]:
        if len(pa_tuple) != ma: continue
        a = math.prod(pa_tuple) if pa_tuple else 1
        if a > 500: break
        for pb_tuple in [primes[j:j+mb] for j in range(0, 30, 1)] if mb > 0 else [()]:
            if len(pb_tuple) != mb: continue
            if set(pa_tuple) & set(pb_tuple): continue
            b = math.prod(pb_tuple) if pb_tuple else 1
            if b > 500: continue
            c = a + b
            if c <= 1: continue
            pcs = factorize_into_k_primes(c, mc, set(pa_tuple) | set(pb_tuple))
            for pc_tuple in pcs:
                if sorted(pc_tuple) != list(pc_tuple): continue  # ensure sorted
                results.append((a, b, c, sorted(pa_tuple), sorted(pb_tuple), list(pc_tuple)))
                if len(results) >= limit:
                    return results
    return results

def find_min_nondeg_vector(pa, pb, pc, bound=8):
    """Find minimum non-degenerate vector in Pasten lattice for given prime groups."""
    omega = len(pa) + len(pb) + len(pc)
    primes_all = pa + pb + pc
    na, nb, nc = len(pa), len(pb), len(pc)

    best_norm = float('inf')
    best_phi = None
    best_W_phi = None
    best_W_psi = None

    # Enumerate phi over pa, pb; compute phi_pc from constraint
    ranges = [range(-bound, bound+1)] * (na + nb)
    for coeffs in iproduct(*ranges):
        phi_a = list(coeffs[:na])
        phi_b = list(coeffs[na:na+nb])
        S_a = sum(phi_a)
        S_b = sum(phi_b)
        S_c_needed = S_a + S_b  # lattice constraint

        # For nc=1: phi_c[0] = S_c_needed
        # For nc>1: distribute S_c_needed among nc primes (try all with small coeffs)
        if nc == 1:
            phi_c_options = [[S_c_needed]]
        elif nc == 2:
            phi_c_options = [[k, S_c_needed - k] for k in range(-bound, bound+1)
                             if abs(S_c_needed - k) <= bound]
        elif nc == 3:
            phi_c_options = []
            for k1 in range(-bound, bound+1):
                for k2 in range(-bound, bound+1):
                    k3 = S_c_needed - k1 - k2
                    if abs(k3) <= bound:
                        phi_c_options.append([k1, k2, k3])
        else:
            phi_c_options = []  # skip nc>=4

        for phi_c in phi_c_options:
            phi = phi_a + phi_b + phi_c
            if all(x == 0 for x in phi): continue

            W_phi = S_b - S_a
            if W_phi == 0: continue  # degenerate

            norm = max(primes_all[i] * abs(phi[i]) for i in range(omega))
            if norm < best_norm:
                best_norm = norm
                best_phi = phi[:]
                best_W_phi = W_phi
                W_psi_a = sum(pa[i] * phi_a[i] for i in range(na))
                W_psi_b = sum(pb[i] * phi_b[i] for i in range(nb))
                best_W_psi = W_psi_b - W_psi_a

    return best_norm, best_phi, best_W_phi, best_W_psi


# ── Main study ──────────────────────────────────────────────────────────────
types_to_test = [
    (1,1,1, "ω=3 (1,1,1)"),
    (1,1,2, "ω=4 (1,1,2)"),
    (1,2,1, "ω=4 (1,2,1)"),
    (2,1,1, "ω=4 (2,1,1)"),
    (1,1,3, "ω=5 (1,1,3)"),
    (1,2,2, "ω=5 (1,2,2)"),
    (2,1,2, "ω=5 (2,1,2)"),
    (2,2,1, "ω=5 (2,2,1)"),
]

print("T56: Wronskian encoding by partition type")
print("="*80)
print(f"{'Type':<18} {'a':>6} {'b':>6} {'c':>6} {'rad':>8} "
      f"{'nd':>5} {'W_φ':>5} {'W_ψ':>8} {'W_ψ=?':>12}")
print("-"*80)

for (ma, mb, mc, label) in types_to_test:
    triples = make_triples_of_type(ma, mb, mc, limit=12)
    if not triples:
        print(f"{label:<18}  (no triples found)")
        continue
    for (a, b, c, pa, pb, pc) in triples[:6]:
        rad = a * b * c  # squarefree so rad=abc
        nd_val = min_nondeg = None
        norm, phi, W_phi, W_psi = find_min_nondeg_vector(pa, pb, pc, bound=6)

        # Classify W_psi
        def classify(w, a, b, c, rad):
            for sign in [1, -1]:
                for val, name in [(a,'a'), (b,'b'), (c,'c'), (rad,'rad'),
                                  (a+b,'a+b'), (a*b,'ab'), (c-a,'c-a'),
                                  (c-b,'c-b'), (1,'1'), (2,'2')]:
                    if w == sign * val:
                        return f"{'+'if sign>0 else '-'}{name}"
            return f"{w}"

        enc = classify(W_psi, a, b, c, rad)
        print(f"{label:<18} {a:>6} {b:>6} {c:>6} {rad:>8} "
              f"{norm:>5} {W_phi:>5} {W_psi:>8} {enc:>12}")
    print()
