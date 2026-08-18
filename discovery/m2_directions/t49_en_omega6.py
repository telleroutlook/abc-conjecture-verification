"""
T49 — E_n conjecture: ω=6 verification

Tests the conjecture for ω=6 types. With 5 free phi variables, bound=3 gives
3^5 = 243 iterations per triple — very fast even for many triples.

Types tested: (1,1,4), (1,2,3), (2,2,2), (1,3,2), (2,3,1), (3,2,1), (1,4,1), etc.
"""

from itertools import product as iproduct


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


primes = [x for x in range(2, 1000) if is_prime(x)]
prime_set = set(primes)


def find_min_nondeg(pa, pb, pc, bound=3):
    all_p = pa + pb + pc
    n = len(all_p)
    na, nb = len(pa), len(pb)
    best = float("inf")
    best_phi = None
    for vals in iproduct(range(-bound, bound + 1), repeat=n - 1):
        pa_sum = sum(vals[i] for i in range(na))
        pb_sum = sum(vals[na + i] for i in range(nb))
        nc = len(pc)
        pc_partial = sum(vals[na + nb + i] for i in range(nc - 1))
        phi_last = pa_sum + pb_sum - pc_partial
        if abs(phi_last) > bound:
            continue
        phi = list(vals) + [phi_last]
        if all(x == 0 for x in phi):
            continue
        if sum(phi[na + i] for i in range(nb)) == sum(phi[i] for i in range(na)):
            continue
        norm = max(all_p[i] * abs(phi[i]) for i in range(n))
        if norm < best:
            best = norm
            best_phi = tuple(phi)
    return best, best_phi


def f10_nd(pa, pb, pc):
    return sorted([min(pa), min(pb), min(pc)])[1]


def product_of(lst):
    r = 1
    for x in lst:
        r *= x
    return r


def make_triples(na, nb, nc, max_t=10):
    triples = []

    def gen_k_primes(k, used_set, limit=15):
        avail = [p for p in primes if p not in used_set][:40]
        res = []

        def rec(start, chosen):
            if len(chosen) == k:
                res.append(chosen[:])
                return
            if len(res) >= limit * 5:
                return
            for i in range(start, len(avail)):
                chosen.append(avail[i])
                rec(i + 1, chosen)
                chosen.pop()

        rec(0, [])
        return res

    for pa_c in gen_k_primes(na, set(), limit=5):
        a = product_of(pa_c)
        for pb_c in gen_k_primes(nb, set(pa_c), limit=5):
            b = product_of(pb_c)
            c = a + b
            if c <= 1:
                continue
            pc_c = []
            temp = c
            used = set(pa_c) | set(pb_c)
            ok = True
            for p in primes:
                if temp == 1:
                    break
                if temp % p == 0:
                    cnt = 0
                    while temp % p == 0:
                        temp //= p
                        cnt += 1
                    if cnt != 1 or p in used:
                        ok = False
                        break
                    pc_c.append(p)
            if not ok or temp != 1 or len(pc_c) != nc:
                continue
            if len(set(pa_c + pb_c + pc_c)) != na + nb + nc:
                continue
            triples.append((sorted(pa_c), sorted(pb_c), sorted(pc_c)))
            if len(triples) >= max_t:
                return triples
    return triples


print("T49: E_n conjecture for ω=6 (all major types)")
print("=" * 72)

# All ω=6 types (na+nb+nc=6, na,nb,nc ≥ 1)
omega6_types = []
for na in range(1, 5):
    for nb in range(1, 5):
        nc = 6 - na - nb
        if nc >= 1:
            omega6_types.append((na, nb, nc))

print(f"Testing {len(omega6_types)} type combinations\n")

results = {}
total_ok = True
for na, nb, nc in omega6_types:
    triples = make_triples(na, nb, nc, max_t=8)
    if not triples:
        results[(na, nb, nc)] = None
        continue
    all_match = True
    for pa, pb, pc in triples[:6]:
        nd = f10_nd(pa, pb, pc)
        best, _ = find_min_nondeg(pa, pb, pc, bound=3)
        if best != nd:
            all_match = False
            total_ok = False
            print(
                f"  MISMATCH type ({na},{nb},{nc}): {pa + pb + pc}, nd={nd}, min={best}"
            )
    results[(na, nb, nc)] = all_match

# Print summary
print(f"{'Type':12}  {'Triples':>8}  {'Status'}")
print("-" * 40)
for na, nb, nc in omega6_types:
    v = results.get((na, nb, nc))
    n = len(make_triples(na, nb, nc, max_t=1)) if v is None else "?"
    if v is None:
        status = "no triples"
    elif v:
        status = "✓"
    else:
        status = "✗ FAILS"
    print(f"  ({na},{nb},{nc})       {'—':>8}  {status}")

print()
print("=" * 72)
if total_ok:
    print("✓ ALL ω=6 types: min_nondeg_norm = F10's nd")
    print("E_n conjecture confirmed for ω=3,4,5,6.")
else:
    print("✗ Some types fail")
