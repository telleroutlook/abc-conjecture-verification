"""
T75 — Exact nd formula discovery for type (2,1,1) triples.

Type (2,1,1): a = p^k1 * q^k2 (two distinct primes in Pa),
              b = r^m  (one prime in Pb),
              c = s^n  (one prime in Pc).
All primes p,q,r,s distinct.

Known: within-group witness (k2/g, -k1/g, 0, 0) where g=gcd(k1,k2) gives
  nd ≤ max(p*k2/g, q*k1/g) = W_ab (within-group norm).

Also cross-group witnesses zeroing different primes.

Goal: find the exact nd formula and identify all regimes.
"""

import math
from itertools import product as iproduct
from collections import defaultdict

def factorize(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def nd_brute(a, b, bound=20):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa) + list(fb) + list(fc)))
    np_ = len(primes)
    if np_ < 3 or np_ > 5: return None
    alpha = [fa.get(p, fb.get(p, -fc.get(p, 0))) for p in primes]
    ws = [1 if p in fb else (-1 if p in fa else 0) for p in primes]
    best = float('inf')
    for coords in iproduct(range(-bound, bound+1), repeat=np_):
        if all(c2 == 0 for c2 in coords): continue
        if sum(alpha[i]*coords[i] for i in range(np_)) != 0: continue
        W = sum(ws[i]*coords[i] for i in range(np_))
        if W == 0: continue
        norm = max(primes[i]*abs(coords[i]) for i in range(np_))
        if norm > 0: best = min(best, norm)
    return best if best < float('inf') else None

def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def within_group_norm(k1, k2, p, q):
    """Norm of within-group witness: max(p*k2/g, q*k1/g), g=gcd(k1,k2)."""
    g = math.gcd(k1, k2)
    return max(p * (k2 // g), q * (k1 // g))

def cross_group_norms_211(p, q, r, s, k1, k2, m, n):
    """
    Compute pure-branch norms for type (2,1,1) triple.
    Primes: p,q ∈ Pa (exponents k1,k2), r ∈ Pb (exponent m), s ∈ Pc (exponent n).
    Constraint: k1*phi_p + k2*phi_q + m*phi_r = n*phi_s.

    Four pure branches (zeroing one coordinate set):
    N_s0: phi_s=0. Constraint: k1*phi_p + k2*phi_q = -m*phi_r.
           This is a 3-variable (2,1) problem: minimize max(p|phi_p|, q|phi_q|, r|phi_r|)
           subject to k1*phi_p + k2*phi_q + m*phi_r = 0.
    N_r0: phi_r=0. Constraint: k1*phi_p + k2*phi_q = n*phi_s.
           3-variable (2,1) problem with s.
    N_q0: phi_q=0. Constraint: k1*phi_p + m*phi_r = n*phi_s.
           3-variable (1,1,1) with cross-group structure.
    N_p0: phi_p=0. Constraint: k2*phi_q + m*phi_r = n*phi_s.
           3-variable (1,1,1).

    Returns dict of {branch_name: norm}.
    """
    results = {}

    # N_s0: phi_s=0, minimize max(p|phi_p|,q|phi_q|,r|phi_r|)
    # Constraint: k1*phi_p + k2*phi_q + m*phi_r = 0
    # W = phi_r - phi_p - phi_q != 0 (CHECK: W = sum_b - sum_a = phi_r - phi_p - phi_q?
    # Actually W = phi_r - (phi_p + phi_q) for Pa={p,q}, Pb={r})
    best_s0 = float('inf')
    for phi_p in range(-15, 16):
        for phi_q in range(-15, 16):
            if k1*phi_p + k2*phi_q == 0:
                phi_r = 0
                W = phi_r - (phi_p + phi_q)
                if W == 0: continue
                norm = max(p*abs(phi_p), q*abs(phi_q), r*abs(phi_r))
                if norm > 0 and norm < best_s0: best_s0 = norm
            else:
                # phi_r = -(k1*phi_p + k2*phi_q) / m
                rhs = -(k1*phi_p + k2*phi_q)
                if rhs % m != 0: continue
                phi_r = rhs // m
                W = phi_r - (phi_p + phi_q)
                if W == 0: continue
                norm = max(p*abs(phi_p), q*abs(phi_q), r*abs(phi_r))
                if norm > 0 and norm < best_s0: best_s0 = norm
    results['N_s0'] = best_s0

    # N_r0: phi_r=0, minimize max(p|phi_p|,q|phi_q|,s|phi_s|)
    best_r0 = float('inf')
    for phi_p in range(-15, 16):
        for phi_q in range(-15, 16):
            rhs = k1*phi_p + k2*phi_q
            if rhs % n != 0: continue
            phi_s = rhs // n
            W = 0 - (phi_p + phi_q)
            if W == 0: continue
            norm = max(p*abs(phi_p), q*abs(phi_q), s*abs(phi_s))
            if norm > 0 and norm < best_r0: best_r0 = norm
    results['N_r0'] = best_r0

    # N_q0: phi_q=0, k1*phi_p + m*phi_r = n*phi_s
    best_q0 = float('inf')
    for phi_p in range(-15, 16):
        for phi_r in range(-15, 16):
            rhs = k1*phi_p + m*phi_r
            if rhs % n != 0: continue
            phi_s = rhs // n
            W = phi_r - phi_p
            if W == 0: continue
            norm = max(p*abs(phi_p), r*abs(phi_r), s*abs(phi_s))
            if norm > 0 and norm < best_q0: best_q0 = norm
    results['N_q0'] = best_q0

    # N_p0: phi_p=0, k2*phi_q + m*phi_r = n*phi_s
    best_p0 = float('inf')
    for phi_q in range(-15, 16):
        for phi_r in range(-15, 16):
            rhs = k2*phi_q + m*phi_r
            if rhs % n != 0: continue
            phi_s = rhs // n
            W = phi_r - phi_q
            if W == 0: continue
            norm = max(q*abs(phi_q), r*abs(phi_r), s*abs(phi_s))
            if norm > 0 and norm < best_p0: best_p0 = norm
    results['N_p0'] = best_p0

    return results

print("T75: Exact nd discovery for type (2,1,1) triples")
print("=" * 75)
print("a = p^k1 * q^k2 (Pa has 2 primes), b = r^m (Pb), c = s^n (Pc)")
print()

# Collect type (2,1,1) triples: a has exactly 2 prime factors, b and c each 1
triples = []
seen = set()

for a in range(4, 500):
    fa = factorize(a)
    if len(fa) != 2: continue  # exactly 2 distinct primes in a
    primes_a = sorted(fa.keys())
    p, q = primes_a[0], primes_a[1]  # p < q
    k1, k2 = fa[p], fa[q]

    for b in range(1, 500):
        fb = factorize(b)
        if len(fb) != 1: continue
        r = list(fb.keys())[0]; m = fb[r]
        if r in (p, q): continue  # r distinct from p,q

        c = a + b
        fc = factorize(c)
        if len(fc) != 1: continue
        s = list(fc.keys())[0]; nv = fc[s]
        if s in (p, q, r): continue  # s distinct

        if math.gcd(a, b) != 1: continue

        key = (a, b)
        if key in seen: continue
        seen.add(key)
        triples.append((a, b, p, q, r, s, k1, k2, m, nv))

print(f"Found {len(triples)} type (2,1,1) triples in [4,500) × [1,500)")
print()

# Analyze each triple
print(f"{'Triple':15s} {'a decomp':15s} {'b':6s} {'c':8s} {'nd':4s} {'W_ab':5s} {'N_pure_min':10s} {'winner':20s}")
print("-" * 90)

stats = defaultdict(int)
cases = []

for (a, b, p, q, r, s, k1, k2, m, nv) in triples:
    nd = nd_brute(a, b, bound=18)
    if nd is None: continue

    W_ab = within_group_norm(k1, k2, p, q)
    branches = cross_group_norms_211(p, q, r, s, k1, k2, m, nv)
    N_pure_min = min(branches.values())
    overall_min = min(W_ab, N_pure_min)

    # Determine what wins
    if nd == W_ab and nd < N_pure_min:
        winner = "within-group"
    elif nd < W_ab:
        winner = f"pure(nd<Wab)"
    elif nd == N_pure_min and nd <= W_ab:
        winner = f"pure(N_pure={N_pure_min})"
    else:
        winner = f"tie(Wab={W_ab},N={N_pure_min})"

    winning_branches = [k for k,v in branches.items() if v == nd]
    formula_ok = "OK" if nd == overall_min else f"FAIL(formula={overall_min})"

    cases.append((a, b, p, q, r, s, k1, k2, m, nv, nd, W_ab, N_pure_min, winner))
    stats[winner.split('(')[0]] += 1

    print(f"  ({a:3d},{b:3d}) {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}  "
          f"nd={nd:3d}  Wab={W_ab:3d}  N_pure={N_pure_min:4d}  {winner}  {formula_ok}")

print()
print("=" * 75)
print(f"Summary: {len(cases)} triples analyzed")
for k,v in sorted(stats.items()): print(f"  {k}: {v}")

print()
print("=== FORMULA INVESTIGATION ===")
print("Candidate: nd = min(W_ab, N_pure_min)?")
errors = [(a,b,nd,overall) for (a,b,p,q,r,s,k1,k2,m,nv,nd,W,N,w) in cases
          for overall in [min(W,N)] if nd != overall]
print(f"  Failures: {len(errors)}")
for row in errors[:10]: print(f"    {row}")

print()
print("=== WITHIN-GROUP DOMINANCE ===")
wg_wins = [(a,b,p,q,k1,k2,nd,W_ab,N_pure_min)
           for (a,b,p,q,r,s,k1,k2,m,nv,nd,W_ab,N_pure_min,w) in cases
           if nd == W_ab and nd < N_pure_min]
print(f"Within-group wins (nd = W_ab < N_pure): {len(wg_wins)} cases")
for row in wg_wins[:8]:
    a,b,p,q,k1,k2,nd,W,N = row
    g = math.gcd(k1,k2)
    print(f"  ({a},{b}) {p}^{k1}*{q}^{k2}: g={g}, k2/g={k2//g}, k1/g={k1//g}  nd={nd}=max({p}*{k2//g},{q}*{k1//g})")

print()
print("=== PURE-BRANCH DOMINANCE ===")
pure_wins = [(a,b,p,q,r,s,k1,k2,m,nv,nd,W_ab,N_pure_min,winner)
             for (a,b,p,q,r,s,k1,k2,m,nv,nd,W_ab,N_pure_min,winner) in cases
             if nd < W_ab]
print(f"Pure branch wins (nd < W_ab): {len(pure_wins)} cases")
for row in pure_wins[:10]:
    a,b,p,q,r,s,k1,k2,m,nv,nd,W,N,w = row
    branches = cross_group_norms_211(p,q,r,s,k1,k2,m,nv)
    winning = [k for k,v in branches.items() if v==nd]
    print(f"  ({a},{b}) {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}: nd={nd}<Wab={W}, winner={winning}, branches={dict(branches)}")

print()
print("=== ANALYSIS: when does within-group lose? ===")
print("Pure branch wins when N_pure_min < W_ab.")
print()

# Analyze ratio W_ab / N_pure_min for within-group losers
for (a,b,p,q,r,s,k1,k2,m,nv,nd,W_ab,N_pure_min,w) in cases:
    if nd < W_ab:
        ratio = W_ab / N_pure_min
        # What determines N_pure_min?
        branches = cross_group_norms_211(p,q,r,s,k1,k2,m,nv)
        best_branch = min(branches, key=branches.get)
        g = math.gcd(k1,k2)
        print(f"  ({a},{b}) Wab={W_ab} N_pure={N_pure_min} ratio={ratio:.2f} best={best_branch}")
        print(f"    {p}^{k1}*{q}^{k2}+{r}^{m}={s}^{nv}, g={g}")
