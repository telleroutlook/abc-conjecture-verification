"""
T51 — Quality-ρ joint bound: all ω=3,4,5,6 types

Extends T50 (which only tested ω=3 type (1,1,1) and ω=4 type (1,1,2)) to ALL
partition types at ω=3,4,5,6.

Conjecture (Quality-ρ Joint Bound):
  For all squarefree coprime (a,b,c): quality + ρ^{ω-1} < 1

where quality = log(c)/log(rad(abc)) and ρ = nd/rad(abc)^{1/(ω-1)}.

F31 proved this for ω=3 (the only type is (1,1,1), all triples have p=2).
This script checks all remaining types numerically.
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

primes = [x for x in range(2, 2000) if is_prime(x)]
prime_set = set(primes)

def rad_of(n):
    r, temp, d = 1, n, 2
    while d*d <= temp:
        if temp % d == 0:
            r *= d
            while temp % d == 0: temp //= d
        d += 1
    if temp > 1: r *= temp
    return r

def quality(c, R):
    return math.log(c) / math.log(R)

def f10_nd(pa, pb, pc):
    return sorted([min(pa), min(pb), min(pc)])[1]

def make_triples(na, nb, nc, max_t=20):
    """Generate squarefree coprime triples of given partition type."""
    results = []
    def gen_k_primes(k, used_set, limit=60):
        avail = [p for p in primes if p not in used_set][:80]
        res = []
        def rec(start, chosen):
            if len(chosen) == k:
                res.append(chosen[:])
                return
            if len(res) >= limit: return
            for i in range(start, len(avail)):
                chosen.append(avail[i])
                rec(i+1, chosen)
                chosen.pop()
        rec(0, [])
        return res

    for pa_c in gen_k_primes(na, set(), limit=8):
        a = 1
        for p in pa_c: a *= p
        for pb_c in gen_k_primes(nb, set(pa_c), limit=8):
            b = 1
            for p in pb_c: b *= p
            c = a + b
            if c <= 1: continue
            # Factorize c, check it's squarefree with exactly nc prime factors
            # from a disjoint prime set
            pc_c = []
            temp = c
            used = set(pa_c) | set(pb_c)
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
                    pc_c.append(p)
            if not ok or temp != 1 or len(pc_c) != nc: continue
            if len(set(pa_c+pb_c+pc_c)) != na+nb+nc: continue
            results.append((sorted(pa_c), sorted(pb_c), sorted(pc_c)))
            if len(results) >= max_t: return results
    return results

print("T51: Quality+rho^{omega-1} joint bound — ALL types ω=3,4,5,6")
print("="*72)

grand_ok = True
grand_max = 0.0
grand_max_info = None

for omega in [3, 4, 5, 6]:
    print(f"\n{'='*30} ω = {omega} {'='*30}")
    # All partition types
    types = []
    for na in range(1, omega):
        for nb in range(1, omega - na):
            nc = omega - na - nb
            if nc >= 1:
                types.append((na, nb, nc))

    for (na, nb, nc) in types:
        triples = make_triples(na, nb, nc, max_t=30)
        if not triples:
            print(f"  type ({na},{nb},{nc}): no triples found")
            continue

        max_sum = 0.0
        all_ok = True
        max_triple = None
        for (pa, pb, pc) in triples:
            a = 1; b = 1; c_val = 1
            for p in pa: a *= p
            for p in pb: b *= p
            for p in pc: c_val *= p
            R = a * b * c_val  # rad(abc) since all squarefree and disjoint
            nd = f10_nd(pa, pb, pc)
            rho = nd / R**(1/(omega-1))
            rho_pow = rho**(omega-1)
            q = quality(c_val, R)
            s = q + rho_pow
            if s >= 1:
                all_ok = False
                grand_ok = False
                print(f"    ✗ FAIL ({na},{nb},{nc}): {pa}+{pb}={pc}, q={q:.4f}, rho^{omega-1}={rho_pow:.4f}, sum={s:.6f}")
            if s > max_sum:
                max_sum = s
                max_triple = (pa, pb, pc, q, rho_pow, s)

        if max_sum > grand_max:
            grand_max = max_sum
            grand_max_info = (omega, na, nb, nc, max_triple)

        status = "✓" if all_ok else "✗ FAILS"
        n = len(triples)
        pa, pb, pc, q, rp, s = max_triple
        print(f"  ({na},{nb},{nc}): {n:3d} triples, max q+ρ^{omega-1} = {max_sum:.6f}  {status}")
        print(f"         argmax: {pa}+{pb}={pc}, q={q:.4f}, ρ^{omega-1}={rp:.4f}")

print("\n" + "="*72)
print("SUMMARY")
print(f"  All quality+rho^{{omega-1}} < 1: {'✓' if grand_ok else '✗ SOME FAIL'}")
print(f"  Global maximum: {grand_max:.8f}")
if grand_max_info:
    omega, na, nb, nc, (pa, pb, pc, q, rp, s) = grand_max_info
    print(f"    Achieved at ω={omega} type ({na},{nb},{nc}): {pa}+{pb}={pc}")
    print(f"    quality={q:.6f}, rho^{omega-1}={rp:.6f}, sum={s:.6f}")
print()
print("Analytical status:")
print("  ω=3 type (1,1,1): PROVED as F31 (2-line proof, Lean-formalized as pasten_F31a)")
print("  All other types: NUMERICAL ONLY (conjecture)")
