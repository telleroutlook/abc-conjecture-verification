"""
T55 — Numerical verification of F33: second minimum for omega=4 type-(1,1,2)

F33 (proved): For type (1,1,2) with a=p, b=q, c=r1*r2 (p < r1 < r2 primes), nd=r1:
  second minimum non-degenerate norm = min(r2, q, 2*r1).

VERIFICATION: brute-force over type-(1,1,2) triples, compare second minimum
against the analytic formula min(r2, q, 2*r1).
"""


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


primes = [x for x in range(2, 300) if is_prime(x)]


def find_norms_sorted(p, q, r1, r2, bound=6, max_n=4):
    norms = set()
    for ap in range(-bound, bound + 1):
        for aq in range(-bound, bound + 1):
            for ar1 in range(-bound, bound + 1):
                phi_r2 = ap + aq - ar1
                if abs(phi_r2) > bound:
                    continue
                if aq == ap:
                    continue  # degenerate
                if ap == 0 and aq == 0 and ar1 == 0:
                    continue
                norm = max(p * abs(ap), q * abs(aq), r1 * abs(ar1), r2 * abs(phi_r2))
                if norm > 0:
                    norms.add(norm)
    return sorted(norms)[:max_n]


def make_112_triples(max_c=300, limit=20):
    results = []
    for p in primes[:8]:  # a = p (single prime)
        for q in primes:  # b = q (single prime)
            if q == p:
                continue
            c = p + q
            if c < 6:
                continue
            # factor c as r1*r2 with r1 < r2 both prime, r1,r2 not in {p,q}
            for r1 in primes:
                if r1 >= c:
                    break
                if c % r1 != 0:
                    continue
                r2 = c // r1
                if r2 <= r1:
                    continue
                if not is_prime(r2):
                    continue
                if r1 in (p, q) or r2 in (p, q):
                    continue
                if len({p, q, r1, r2}) != 4:
                    continue
                if p < r1:  # nd = r1 < q
                    results.append((p, q, r1, r2))
                    if len(results) >= limit:
                        return results
    return results


triples = make_112_triples(limit=20)

print("T55: F33 verification — second minimum nondeg norm for type (1,1,2)")
print("=" * 70)
print("Formula: second min = min(r2, q, 2*r1)")
print()

all_ok = True
for p, q, r1, r2 in triples:
    norms = find_norms_sorted(p, q, r1, r2, bound=8)
    pred = min(r2, q, 2 * r1)
    second = norms[1] if len(norms) > 1 else None
    ok = second == pred
    if not ok:
        all_ok = False
    status = "✓" if ok else "✗"
    dom = (
        "r2"
        if pred == r2 and r2 <= q and r2 <= 2 * r1
        else ("q" if pred == q else "2r1")
    )
    print(
        f"  ({p},{q},{r1}*{r2}): min={norms[0]}=r1, 2nd={second}, "
        f"pred={pred}={dom}, r2={r2},q={q},2r1={2 * r1} {status}"
    )

print()
print("=" * 70)
print(
    f"F33 {'VERIFIED ✓' if all_ok else 'FAILS ✗'} for all tested type-(1,1,2) triples."
)
