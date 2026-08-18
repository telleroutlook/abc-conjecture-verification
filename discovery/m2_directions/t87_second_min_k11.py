"""
T87 — Verify second successive minimum for type (k,1,1) triples.

For type (k,1,1): Pa={p^k}, Pb={q}, Pc={r}, p<q<r, constraint kφ_p+φ_q=φ_r.
thm:nd_k11: nd = min(r, qk).

THEOREM F34:
(i)  Valuation (qk < r):  nd=qk, lambda2 = min(r, 2qk)
(ii) Pairwise (qk >= r):  nd=r,  lambda2 = min{N in {2r, qk, q(k-1)} : N > r}

Achievability vectors (pairwise):
  2r: phi=(0,2,2), W=2-0=2 ≠ 0.  norm=max(0,2q,2r)=2r.
  qk: phi=(1,-k,0), W=-k-1 ≠ 0. norm=max(p,qk,0)=qk.
  q(k-1): phi=(1,1-k,1), W=(1-k)-1=-k ≠ 0. norm=max(p,q(k-1),r)=q(k-1) if q(k-1)>r.

Gap: on the phi_r=±1 line (phi_p=t, phi_q=1-kt), the only t with q|1-kt|<min
     is t=0 (giving norm r=nd). All other t give norm >= min. phi_r=0 gives >=qk.
     phi_r=±j (j>=2) gives >=2r.
"""


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def nd_and_lambda2_brute(p, q, r, k, bound):
    norms = set()
    for xp in range(-bound, bound + 1):
        for xq in range(-bound, bound + 1):
            xr = k * xp + xq
            if abs(xr) > bound:
                continue
            if xp == 0 and xq == 0 and xr == 0:
                continue
            if xq - xp == 0:
                continue
            nrm = max(p * abs(xp), q * abs(xq), r * abs(xr))
            if nrm > 0:
                norms.add(nrm)
    if not norms:
        return None, None
    sn = sorted(norms)
    return sn[0], (sn[1] if len(sn) > 1 else None)


def formula_nd(q, r, k):
    return min(r, q * k)


def formula_lambda2(q, r, k):
    if q * k < r:
        return min(r, 2 * q * k)
    else:
        candidates = [2 * r, q * k]
        qk1 = q * (k - 1)
        if qk1 > r:
            candidates.append(qk1)
        return min(candidates)


triples = []
for p in [2, 3, 5, 7]:
    for q in range(p + 1, 80):
        if not is_prime(q):
            continue
        for k in range(1, 10):
            a = p**k
            if a > 500:
                break
            c = a + q
            if not is_prime(c):
                continue
            r = c
            if r <= q:
                continue
            triples.append((a, q, p, q, r, k))

print(f"T87: Second minimum for type (k,1,1) — {len(triples)} triples")

nd_fail = val_ok = val_fail = pair_ok = pair_fail = 0

for a, b, p, q, r, k in triples:
    nd_f = formula_nd(q, r, k)
    l2_f = formula_lambda2(q, r, k)
    bb = max(5, k + 4, l2_f // max(p, 1) + 2)
    nd_b, l2_b = nd_and_lambda2_brute(p, q, r, k, bb)
    if nd_b is None:
        continue
    if nd_b != nd_f:
        nd_fail += 1
        print(f"  ND-FAIL ({a},{b}): f={nd_f} b={nd_b}")
        continue
    if l2_b is None:
        continue
    regime = "val" if q * k < r else "pair"
    if l2_b == l2_f:
        if regime == "val":
            val_ok += 1
        else:
            pair_ok += 1
    else:
        if regime == "val":
            val_fail += 1
        else:
            pair_fail += 1
        print(
            f"  L2-FAIL ({a},{b}) {regime} k={k} q={q} r={r}: "
            f"nd={nd_f} f_l2={l2_f} b_l2={l2_b}"
        )

print(f"\nnd: {nd_fail} failures")
print(f"Valuation lambda2: OK={val_ok}  FAIL={val_fail}")
print(f"Pairwise  lambda2: OK={pair_ok}  FAIL={pair_fail}")
if nd_fail + val_fail + pair_fail == 0:
    print("\nFORMULA F34 CONFIRMED.")
