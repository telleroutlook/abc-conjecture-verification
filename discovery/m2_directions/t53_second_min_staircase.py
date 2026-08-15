"""
T53 — Second minimum non-degenerate norm exploration (F32 open problem)

F10 (proved): min non-degenerate norm = nd = second_smallest{min(Pa), min(Pb), min(Pc)}.
F32 (open): what is the second minimum non-degenerate norm?

FINDINGS:
- For omega=3: second min = q_3 = max prime = p+q < 2q = 2*nd (always). Simple staircase holds.
- For omega>=4 with types (1,1,k), (1,k,1): second min = min(q_3, 2*nd).
  When nd=q_2 (all_sorted[1]) and q_3 < 2*q_2: second min = q_3.
  When 2*q_2 < q_3: second min = 2*q_2.
- For type (2,1,2): nd != all_sorted[1]. The min nondeg norm = nd = min(Pa-group min) !=
  second-smallest prime overall. The second min formula min(q_3, 2*q_2) fails.

CONCLUSION: F32 is an OPEN PROBLEM. The second minimum depends on detailed prime group
structure and is not simply characterized by just the sorted prime list.

CAUTION on T53's predictions:
- 'q_2' here = second smallest prime overall = all_sorted[1] (NOT F10's nd in general!)
- For types (1,1,k) and (1,k,1): nd = all_sorted[1] = q_2, formula works.
- For types (na,nb,nc) with na>1 or nb>1: nd != all_sorted[1], formula breaks.
"""

from itertools import product as iproduct

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

primes = [x for x in range(2, 500) if is_prime(x)]

def find_nondeg_norms_sorted(pa, pb, pc, bound=4, max_norms=5):
    """Find the k smallest non-degenerate norms (distinct values)."""
    all_p = pa + pb + pc
    n = len(all_p)
    na, nb = len(pa), len(pb)
    found_norms = set()
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
        if norm > 0:
            found_norms.add(norm)
    return sorted(found_norms)[:max_norms]

def staircase_prediction(pa, pb, pc):
    """Predict the staircase: q_2, q_3, ..., q_omega (sorted all primes)."""
    all_primes_sorted = sorted(pa + pb + pc)
    return all_primes_sorted[1:]  # q_2, q_3, ..., q_omega


def correct_second_min(pa, pb, pc):
    """Correct second minimum = min(q_3, 2*q_2).
    - Vector using q_1 and q_3 from different groups: norm = q_3.
    - Double of minimum vector: norm = 2*q_2.
    Second minimum = min of these two.
    """
    all_sorted = sorted(pa + pb + pc)
    q2, q3 = all_sorted[1], all_sorted[2]
    return min(q3, 2 * q2)

def make_triples(na, nb, nc, max_t=8):
    results = []
    def gen_k_primes(k, used_set, limit=20):
        avail = [p for p in primes if p not in used_set][:40]
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
        a = 1
        for p in pa_c: a *= p
        for pb_c in gen_k_primes(nb, set(pa_c), limit=5):
            b = 1
            for p in pb_c: b *= p
            c = a + b
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

print("T53: Second minimum non-degenerate norm (F32 conjecture)")
print("="*70)
print()
print("Conjecture F32: second min nondeg norm = min(q_3, 2*q_2)")
print("  (simple staircase q_{k+1} fails for omega>=4 when 2*q_2 < q_3)")
print()

types_to_test = [
    (1,1,1, "omega=3"),
    (1,1,2, "omega=4"),
    (1,2,1, "omega=4"),
    (1,1,3, "omega=5"),
    (1,2,2, "omega=5"),
    (2,1,2, "omega=5"),
]

all_ok = True
for (na, nb, nc, label) in types_to_test:
    triples = make_triples(na, nb, nc, max_t=5)
    if not triples:
        print(f"Type ({na},{nb},{nc}) [{label}]: no triples found")
        continue
    print(f"Type ({na},{nb},{nc}) [{label}]:")
    type_ok = True
    for (pa, pb, pc) in triples[:4]:
        all_sorted = sorted(pa + pb + pc)
        q2, q3 = all_sorted[1], all_sorted[2]
        pred_second = correct_second_min(pa, pb, pc)
        norms = find_nondeg_norms_sorted(pa, pb, pc, bound=4, max_norms=4)
        got_second = norms[1] if len(norms) > 1 else None
        match = (got_second == pred_second)
        if not match:
            type_ok = False
            all_ok = False
        status = "✓" if match else "✗"
        print(f"  {pa}+{pb}={pc}: q2={q2},q3={q3},2q2={2*q2} → pred2nd={pred_second} got2nd={got_second} {status}")
    print()

print("="*70)
if all_ok:
    print("✓ F32: second min nondeg norm = min(q_3, 2*q_2) for all tested types")
    print("  Note: simple staircase (second=q_3) holds iff q_3 < 2*q_2.")
    print("  For omega=3: always q_3=p+q < 2q = 2*q_2 (since p<q), so staircase holds.")
    print("  For omega>=4: can have 2*q_2 < q_3, so second min = 2*q_2.")
else:
    print("✗ Some types fail")
