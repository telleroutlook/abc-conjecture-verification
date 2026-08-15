"""
T48 — E_n generalization: ω=5 ALL types, minimum non-degenerate Pasten lattice vector

Tests E_n conjecture for all ω=5 types:
  (1,1,3): a=p,     b=q,     c=r1*r2*r3
  (1,2,2): a=p,     b=q1*q2, c=r1*r2
  (2,1,2): a=p1*p2, b=q,     c=r1*r2
  (2,2,1): a=p1*p2, b=q1*q2, c=r
  (1,3,1): a=p,     b=q1*q2*q3, c=r
  (3,1,1): a=p1*p2*p3, b=q,  c=r

Wronskian: W = a*b*(phi_b_sum - phi_a_sum), non-degenerate <=> phi_b_sum != phi_a_sum.
Constraint: phi_a_sum + phi_b_sum = phi_c_sum.
"""

from itertools import product as iproduct

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

primes = [x for x in range(2, 800) if is_prime(x)]
prime_set = set(primes)

def find_min_nondeg(pa, pb, pc, bound=4):
    all_p = pa + pb + pc
    n = len(all_p)
    na, nb, nc = len(pa), len(pb), len(pc)
    best = float('inf')
    best_phi = None
    for vals in iproduct(range(-bound, bound+1), repeat=n-1):
        pa_sum = sum(vals[i] for i in range(na))
        pb_sum = sum(vals[na+i] for i in range(nb))
        pc_partial = sum(vals[na+nb+i] for i in range(nc-1))
        phi_last = pa_sum + pb_sum - pc_partial
        if abs(phi_last) > bound: continue
        phi = list(vals) + [phi_last]
        if all(x == 0 for x in phi): continue
        if sum(phi[na+i] for i in range(nb)) == sum(phi[i] for i in range(na)): continue
        norm = max(all_p[i]*abs(phi[i]) for i in range(n))
        if norm < best:
            best = norm
            best_phi = tuple(phi)
    return best, best_phi

def f10_nd(pa, pb, pc):
    mins = sorted([min(pa), min(pb), min(pc)])
    return mins[1]

def test_type(label, triples, limit=12):
    print(f"\nType {label}:")
    print("-"*75)
    all_match = True
    for pa, pb, pc in triples[:limit]:
        nd = f10_nd(pa, pb, pc)
        best, phi = find_min_nondeg(pa, pb, pc, bound=4)
        ok = "✓" if best == nd else f"✗(nd={nd})"
        if best != nd: all_match = False
        tag = f"({','.join(str(x) for x in pa+pb+pc)})"
        print(f"  {tag:30s}: nd={nd:3d} min={best:3d} φ={phi}  {ok}")
    status = "ALL ✓" if all_match else "MISMATCH ✗"
    print(f"  → {status}")
    return all_match

# ---- generate triples ----
def gen_squarefree_k_primes(k, used, limit=10):
    """Generate sets of k distinct primes not in `used`."""
    avail = [p for p in primes if p not in used]
    results = []
    def rec(start, chosen):
        if len(chosen) == k:
            results.append(chosen[:])
            return
        if len(results) >= limit * 10: return
        for i in range(start, min(start+30, len(avail))):
            chosen.append(avail[i])
            rec(i+1, chosen)
            chosen.pop()
    rec(0, [])
    return results

def product_of(lst):
    r = 1
    for x in lst: r *= x
    return r

def make_triples(type_sizes, max_triples=20):
    na, nb, nc = type_sizes
    triples = []
    for pa_cands in gen_squarefree_k_primes(na, set(), limit=8):
        a = product_of(pa_cands)
        for pb_cands in gen_squarefree_k_primes(nb, set(pa_cands), limit=8):
            b = product_of(pb_cands)
            c = a + b
            if c <= 1: continue
            # Factor c into nc distinct primes, squarefree
            pc_cands = []
            temp = c
            used = set(pa_cands) | set(pb_cands)
            ok = True
            for p in primes:
                if temp == 1: break
                if temp % p == 0:
                    cnt = 0
                    while temp % p == 0:
                        temp //= p
                        cnt += 1
                    if cnt != 1 or p in used:
                        ok = False; break
                    pc_cands.append(p)
            if not ok or temp != 1 or len(pc_cands) != nc: continue
            if len(set(pa_cands+pb_cands+pc_cands)) != na+nb+nc: continue
            triples.append((sorted(pa_cands), sorted(pb_cands), sorted(pc_cands)))
            if len(triples) >= max_triples: return triples
    return triples

print("T48: E_n conjecture for ω=5 (all types)")
print("="*75)

types = [(1,1,3), (1,2,2), (2,1,2), (2,2,1), (1,3,1), (3,1,1)]
results = {}
for t in types:
    triples = make_triples(t, max_triples=15)
    print(f"\nGenerating type {t}: found {len(triples)} triples", flush=True)
    if triples:
        ok = test_type(str(t), triples, limit=min(8, len(triples)))
        results[t] = ok
    else:
        print(f"  (no triples found)")
        results[t] = None

print("\n" + "="*75)
print("E_n conjecture ω=5 summary:")
for t, ok in results.items():
    if ok is None: status = "no data"
    elif ok: status = "✓ CONFIRMED"
    else: status = "✗ FAILS"
    print(f"  Type {t}: {status}")

all_ok = all(v for v in results.values() if v is not None)
if all_ok:
    print("\n✓ All ω=5 types: min_nondeg_norm = F10's nd")
    print("E_n conjecture holds for ω=3,4,5.")
else:
    print("\n✗ Some types fail — E_n conjecture needs revision for ω=5")
