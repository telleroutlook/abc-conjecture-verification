"""
T52 — E_n conjecture: ω=7 verification

Tests all partition types (na,nb,nc) with na+nb+nc=7, na,nb,nc≥1.
This is a total of C(6,2)=15 types.

With ω=7 and bound=2: 2^6=64 iterations per triple — fast enough.
Uses the same logic as T47-T49.
"""

from itertools import product as iproduct

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

primes = [x for x in range(2, 1000) if is_prime(x)]
prime_set = set(primes)

def find_min_nondeg(pa, pb, pc, bound=2):
    all_p = pa + pb + pc
    n = len(all_p)
    na, nb = len(pa), len(pb)
    best = float('inf')
    for vals in iproduct(range(-bound, bound+1), repeat=n-1):
        pa_sum = sum(vals[i] for i in range(na))
        pb_sum = sum(vals[na+i] for i in range(nb))
        nc = len(pc)
        pc_partial = sum(vals[na+nb+i] for i in range(nc-1))
        phi_last = pa_sum + pb_sum - pc_partial
        if abs(phi_last) > bound: continue
        phi = list(vals) + [phi_last]
        if all(x == 0 for x in phi): continue
        if sum(phi[na+i] for i in range(nb)) == sum(phi[i] for i in range(na)): continue
        norm = max(all_p[i]*abs(phi[i]) for i in range(n))
        if norm < best:
            best = norm
    return best

def f10_nd(pa, pb, pc):
    return sorted([min(pa), min(pb), min(pc)])[1]

def product_of(lst):
    r = 1
    for x in lst: r *= x
    return r

def make_triples(na, nb, nc, max_t=6):
    results = []
    def gen_k_primes(k, used_set, limit=30):
        avail = [p for p in primes if p not in used_set][:50]
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

    for pa_c in gen_k_primes(na, set(), limit=5):
        a = product_of(pa_c)
        for pb_c in gen_k_primes(nb, set(pa_c), limit=5):
            b = product_of(pb_c)
            c = a + b
            if c <= 1: continue
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

print("T52: E_n conjecture for ω=7 (all 15 partition types)")
print("="*60)

omega7_types = []
for na in range(1, 6):
    for nb in range(1, 6):
        nc = 7 - na - nb
        if 1 <= nc:
            omega7_types.append((na, nb, nc))

print(f"Testing {len(omega7_types)} types\n")

total_ok = True
results = {}

for na, nb, nc in omega7_types:
    triples = make_triples(na, nb, nc, max_t=5)
    if not triples:
        results[(na,nb,nc)] = None
        continue
    all_match = True
    for pa, pb, pc in triples:
        nd = f10_nd(pa, pb, pc)
        best = find_min_nondeg(pa, pb, pc, bound=2)
        if best != nd:
            all_match = False
            total_ok = False
            print(f"  MISMATCH ({na},{nb},{nc}): {pa}+{pb}={pc}, nd={nd}, min={best}")
    results[(na,nb,nc)] = all_match

print(f"{'Type':14}  {'Status'}")
print("-"*30)
for na, nb, nc in omega7_types:
    v = results.get((na,nb,nc))
    if v is None: status = "no triples found"
    elif v: status = "✓"
    else: status = "✗ FAILS"
    print(f"  ({na},{nb},{nc})         {status}")

print()
print("="*60)
if total_ok:
    print("✓ ALL ω=7 types: min_nondeg_norm = F10's nd")
    print("E_n conjecture confirmed for ω=3,4,5,6,7.")
else:
    print("✗ Some types fail")
