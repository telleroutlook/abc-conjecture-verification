"""
T58 — Empirical study: W_ψ vs c, rad, nd across all types

For the minimum non-degenerate vector ψ ∈ F(a,b), study the ratios:
  |W_ψ| / c          — how big is W compared to c?
  |W_ψ| / rad(abc)   — compared to radical?
  |W_ψ| / nd         — compared to minimum non-degen norm?
  c / (ω · nd)       — Minkowski-type bound: how far is c from ω·nd?
  c / rad            — quality (for squarefree = 1/(ω pairwise gcd stuff))

KEY HYPOTHESIS to test:
  H1: |W_ψ| ≤ ω · nd  (from norm bound — should always hold)
  H2: |W_ψ| ≥ 1       (non-degeneracy — always holds)
  H3: For type (1,1,1): W_ψ = -c exactly (proved analytically)
  H4: Any lower bound like |W_ψ| ≥ f(rad) would give abc-type bounds

Look for empirical patterns that might suggest new conjectures.
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

primes = [x for x in range(2, 500) if is_prime(x)]

def omega(n):
    count = 0
    for p in primes:
        if p*p > n: break
        if n % p == 0:
            count += 1
            while n % p == 0: n //= p
    if n > 1: count += 1
    return count

def prime_factors(n):
    factors = []
    for p in primes:
        if p*p > n: break
        if n % p == 0:
            factors.append(p)
            while n % p == 0: n //= p
    if n > 1: factors.append(n)
    return sorted(factors)

def rad(n):
    return math.prod(prime_factors(n)) if n > 1 else 1

def find_min_nondeg(pa, pb, pc, bound=8):
    """Find minimum non-degenerate vector and its W_psi."""
    omega_n = len(pa) + len(pb) + len(pc)
    all_p = pa + pb + pc
    na, nb, nc = len(pa), len(pb), len(pc)
    best_norm = float('inf')
    best_W_psi = None

    ranges = [range(-bound, bound+1)] * (na + nb)
    for coeffs in iproduct(*ranges):
        phi_a = list(coeffs[:na])
        phi_b = list(coeffs[na:na+nb])
        S_a = sum(phi_a)
        S_b = sum(phi_b)
        S_c_needed = S_a + S_b
        W_phi = S_b - S_a
        if W_phi == 0: continue

        # Try phi_c distributions
        if nc == 1:
            phi_c_opts = [[S_c_needed]]
        elif nc == 2:
            phi_c_opts = [[k, S_c_needed-k] for k in range(-bound, bound+1)
                          if abs(S_c_needed-k) <= bound]
        elif nc == 3:
            phi_c_opts = [[k1,k2,S_c_needed-k1-k2]
                          for k1 in range(-bound//2, bound//2+1)
                          for k2 in range(-bound//2, bound//2+1)
                          if abs(S_c_needed-k1-k2) <= bound]
        else:
            phi_c_opts = [[0]*nc] if S_c_needed == 0 else []

        for phi_c in phi_c_opts:
            phi = phi_a + phi_b + phi_c
            norm = max(all_p[i] * abs(phi[i]) for i in range(omega_n))
            if norm == 0: continue
            if norm < best_norm:
                best_norm = norm
                W_psi_a = sum(pa[i]*phi_a[i] for i in range(na))
                W_psi_b = sum(pb[i]*phi_b[i] for i in range(nb))
                best_W_psi = W_psi_b - W_psi_a

    return best_norm, best_W_psi

def nd_value(pa, pb, pc):
    """nd = second smallest of {min(Pa), min(Pb), min(Pc)}."""
    mins = sorted([min(g) for g in [pa, pb, pc] if g])
    return mins[1] if len(mins) >= 2 else mins[0]

# ── Collect data across many squarefree triples ──────────────────────────────
data = []
print("Scanning squarefree coprime triples a+b=c with 2 ≤ a < b and ω(abc) ≤ 6...")

for a in range(2, 120):
    if omega(a) > 3: continue
    for b in range(a+1, 300):
        c = a + b
        if math.gcd(a, b) != 1: continue
        if omega(b) > 3: continue
        if omega(c) > 3: continue
        pa = prime_factors(a)
        pb = prime_factors(b)
        pc = prime_factors(c)
        # Squarefree check
        if math.prod(pa) != a: continue
        if math.prod(pb) != b: continue
        if math.prod(pc) != c: continue
        # No shared primes
        if set(pa) & set(pb) or set(pa) & set(pc) or set(pb) & set(pc): continue
        om = len(pa) + len(pb) + len(pc)
        if om > 6: continue
        nd = nd_value(pa, pb, pc)
        R = rad(a*b*c)
        quality = math.log(c) / math.log(R) if R > 1 else 0
        norm, W_psi = find_min_nondeg(pa, pb, pc, bound=6)
        if W_psi is None: continue
        data.append({
            'a': a, 'b': b, 'c': c,
            'pa': pa, 'pb': pb, 'pc': pc,
            'omega': om, 'nd': nd, 'norm': norm,
            'W_psi': W_psi, 'rad': R, 'quality': quality,
            'type': f"({len(pa)},{len(pb)},{len(pc)})",
        })

print(f"Total triples collected: {len(data)}")
print()

# ── H1 check: |W_ψ| ≤ ω · nd ────────────────────────────────────────────────
h1_fails = [d for d in data if abs(d['W_psi']) > d['omega'] * d['nd']]
print(f"H1 (|W_ψ| ≤ ω·nd): {'PASS' if not h1_fails else f'FAILS for {len(h1_fails)} triples'}")

# ── H3 check: type (1,1,1) → W_ψ = -c ─────────────────────────────────────
type111 = [d for d in data if d['type'] == '(1,1,1)']
# T56 showed W_psi = +c (sign depends on vector orientation); check |W_psi| = c
h3_fails = [d for d in type111 if abs(d['W_psi']) != d['c']]
h3_msg = "PASS" if not h3_fails else f"FAILS for {len(h3_fails)} triples"
print(f"H3 (type (1,1,1): |W_psi|=c): {h3_msg} [{len(type111)} triples tested]")

# ── H3b: type (1,1,k) → W_ψ = +a ─────────────────────────────────────────
type11k = [d for d in data if d['type'] in ('(1,1,2)', '(1,1,3)')]
h3b_fails = [d for d in type11k if d['W_psi'] != d['a']]
if h3b_fails:
    fails_str = str([(d['a'],d['b'],d['c'],d['W_psi']) for d in h3b_fails[:3]])
    h3b_msg = f"FAILS: {fails_str}"
else:
    h3b_msg = "PASS"
print(f"H3b (type (1,1,k>=2): W_psi=+a): {h3b_msg} [{len(type11k)} triples tested]")

print()

# ── Per-type statistics ───────────────────────────────────────────────────────
from collections import defaultdict
by_type = defaultdict(list)
for d in data:
    by_type[d['type']].append(d)

print(f"{'Type':<12} {'count':>6} {'W_ψ/c range':>20} {'|W_ψ|/nd range':>18} {'W_ψ encodes?':>15}")
print("-"*75)
for typ in sorted(by_type.keys()):
    group = by_type[typ]
    wc_vals = set(d['W_psi'] / d['c'] for d in group)
    wnd_vals = [abs(d['W_psi']) / d['nd'] for d in group]
    # Check if W_psi always equals a, b, c, or -c
    wp_vals = [d['W_psi'] for d in group]
    encodes = "?"
    if all(w == -d['c'] for w, d in zip(wp_vals, group)):
        encodes = "-c"
    elif all(w == d['c'] for w, d in zip(wp_vals, group)):
        encodes = "+c"
    elif all(w == d['a'] for w, d in zip(wp_vals, group)):
        encodes = "+a"
    elif all(w == -d['a'] for w, d in zip(wp_vals, group)):
        encodes = "-a"
    elif all(w == d['b'] for w, d in zip(wp_vals, group)):
        encodes = "+b"
    elif all(w == -d['b'] for w, d in zip(wp_vals, group)):
        encodes = "-b"
    wc_str = f"[{min(wc_vals):.3f}, {max(wc_vals):.3f}]"
    wnd_str = f"[{min(wnd_vals):.2f}, {max(wnd_vals):.2f}]"
    print(f"{typ:<12} {len(group):>6} {wc_str:>20} {wnd_str:>18} {encodes:>15}")

print()

# ── Search for lower bound: does |W_ψ| ≥ rad(abc)^α for some α? ─────────────
print("Searching for empirical lower bound |W_ψ| ≥ rad^α ...")
# For type (1,1,1): W_psi = -c, rad = pqr = pq(p+q) ≥ pq²
# So |W_ψ| = c and rad ≥ c² / (p·c/q) ... complex. Just compute empirical ratio.
print(f"{'Type':<12} {'min |W_ψ|/rad':>15} {'max |W_ψ|/rad':>15} {'min |W_ψ|/√rad':>16}")
print("-"*60)
for typ in sorted(by_type.keys()):
    group = by_type[typ]
    ratios1 = [abs(d['W_psi']) / d['rad'] for d in group]
    ratios2 = [abs(d['W_psi']) / d['rad']**0.5 for d in group]
    print(f"{typ:<12} {min(ratios1):>15.6f} {max(ratios1):>15.6f} {min(ratios2):>16.6f}")

print()

# ── Show extreme cases: triples where c/(ω·nd) is largest ───────────────────
print("Top 10 triples by c/(ω·nd) — how close are we to the Minkowski bound?")
data_sorted = sorted(data, key=lambda d: d['c']/(d['omega']*d['nd']), reverse=True)
print(f"{'(a,b,c)':<20} {'type':<10} {'ω·nd':>8} {'c':>8} {'c/(ω·nd)':>10} {'W_ψ':>8}")
for d in data_sorted[:10]:
    print(f"  ({d['a']},{d['b']},{d['c']}){'':<5} {d['type']:<10} "
          f"{d['omega']*d['nd']:>8} {d['c']:>8} {d['c']/(d['omega']*d['nd']):>10.4f} "
          f"{d['W_psi']:>8}")
