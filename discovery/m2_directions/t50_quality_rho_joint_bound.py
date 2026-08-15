"""
T50 — Quality-ρ joint bound for squarefree abc triples

Observation: for squarefree coprime (a,b,c) with a+b=c,
  quality q = log(c)/log(rad(abc)) ∈ (0,1) always
  ρ = nd/rad^{1/(ω-1)} (the normalized non-degenerate norm)

Question: Is quality + ρ^{ω-1} bounded by some constant < 1?
         Or: does quality + ρ^{ω-1} → 1 (tight but never exceeds)?

For ω=3 type (1,1,1) with p=2, q prime, r=p+q:
  quality = log(r)/log(2qr)
  ρ² = q/(2r)  [since nd=q, R=rad^{1/2}=(2qr)^{1/2}, ρ²=q²/(2qr)=q/(2r)]

Claim: quality + ρ² < 1 for all type (1,1,1) triples (and → 1 as q → ∞).

Analytical proof sketch for p=2:
  quality + ρ² < 1
  ⟺ log(r)/log(2(r-2)r) + (r-2)/(2r) < 1  [since q=r-2]
  ⟺ log(r)/log(2(r-2)r) < 1 - (r-2)/(2r) = (r+2)/(2r)
  ⟺ 2r·log(r) < (r+2)·log(2(r-2)r)  [where r = 2+q is prime, q prime]
  ⟺ (r-2)·log(r) < (r+2)·log(2(r-2))
  This holds for r≥5 since 2r·log(r) < (r+2)·[log(2)+log(r-2)+log(r)]
  → the sum log(r) term cancels and log(r-2)+log(2) > 0 forces RHS > LHS.
"""

import math

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def rad(n):
    r = 1
    temp = n
    d = 2
    while d*d <= temp:
        if temp % d == 0:
            r *= d
            while temp % d == 0: temp //= d
        d += 1
    if temp > 1: r *= temp
    return r

def quality(a, b, c):
    R = rad(a) * rad(b) * rad(c)  # rad(abc) = rad(a)*rad(b)*rad(c) for squarefree
    return math.log(c) / math.log(R)

def nd_and_rho(pa, pb, pc):
    """F10 nd and ρ for given prime groups"""
    group_mins = sorted([min(pa), min(pb), min(pc)])
    nd = group_mins[1]
    R = 1
    for grp in [pa, pb, pc]:
        for p in grp: R *= p
    omega = len(pa) + len(pb) + len(pc)
    rho_power = nd / R**(1/(omega-1))  # ρ^{ω-1} = nd/R^{1/(ω-1)}... wait
    # Actually ρ = nd / R^{1/(ω-1)}, so ρ^{ω-1} = nd^{ω-1} / R
    rho = nd / R**(1/(omega-1))
    return nd, R, rho, omega

print("T50: Quality vs ρ joint bound for squarefree abc triples")
print("="*70)

# ====== Type (1,1,1): ω=3, p=2 ======
print("\nType (1,1,1): a=p, b=q, c=r=p+q (all prime, p=2)")
print(f"{'(p,q,r)':15}  {'quality':>10}  {'rho^2':>10}  {'q+rho^2':>10}  {'<1?'}")
print("-"*60)

primes = [x for x in range(2, 5000) if is_prime(x)]
results_111 = []
for q in primes:
    if q == 2: continue
    r = 2 + q
    if r not in set(primes): continue
    q_abc = quality(2, q, r)
    nd, R, rho, omega = nd_and_rho([2], [q], [r])
    rho2 = rho**2
    s = q_abc + rho2
    results_111.append((q, r, q_abc, rho2, s))

# Show first 10 and last 5 by q
for q, r, qa, rho2, s in results_111[:10]:
    ok = "✓" if s < 1 else "✗ FAILS"
    print(f"(2,{q},{r}){'':5}  {qa:10.6f}  {rho2:10.6f}  {s:10.6f}  {ok}")

print("...")
for q, r, qa, rho2, s in results_111[-5:]:
    ok = "✓" if s < 1 else "✗ FAILS"
    print(f"(2,{q},{r}){'':5}  {qa:10.6f}  {rho2:10.6f}  {s:10.6f}  {ok}")

max_sum_111 = max(s for _,_,_,_,s in results_111)
all_ok_111 = all(s < 1 for _,_,_,_,s in results_111)
print(f"\nAll quality+rho²<1: {'✓' if all_ok_111 else '✗'}")
print(f"Max quality+rho² = {max_sum_111:.8f} (over {len(results_111)} triples, q≤4999)")
print(f"Limit as q→∞: quality→1/2, rho²→1/2, sum→1 (never achieved)")

# ====== Analytical check ======
print("\n--- Analytical verification for type (1,1,1), p=2 ---")
print("Claim: quality + rho² < 1 iff (r-2)*log(r) < (r+2)*log(2*(r-2))")
print("where r = 2+q, checked for r prime, q=r-2 prime:")
for q in [3, 5, 11, 41, 101, 1009, 5003]:
    if not is_prime(q): continue
    r = 2 + q
    if not is_prime(r): continue
    lhs = (r-2) * math.log(r)
    rhs = (r+2) * math.log(2*(r-2))
    ok = "✓" if lhs < rhs else "✗"
    print(f"  r={r:6d}: LHS={lhs:.4f}  RHS={rhs:.4f}  LHS<RHS: {ok}")

# ====== Type (1,1,2): ω=4 ======
print("\n\nType (1,1,2): a=p, b=q, c=r1*r2 (all prime)")
print(f"{'(p,q,r1,r2)':20}  {'quality':>10}  {'rho^3':>10}  {'q+rho^3':>10}  {'<1?'}")
print("-"*65)

prime_set = set(primes[:200])
results_112 = []
for p in primes[:10]:
    for q in primes:
        if q <= p: continue
        c = p + q
        for r1 in primes:
            if r1 >= c: break
            if c % r1 != 0: continue
            r2 = c // r1
            if r2 <= r1 or r2 not in prime_set: continue
            q_abc = quality(p, q, c)
            nd, R, rho, omega = nd_and_rho([p], [q], [r1, r2])
            rho3 = rho**3
            s = q_abc + rho3
            results_112.append((p, q, r1, r2, q_abc, rho3, s))

for p, q, r1, r2, qa, rho3, s in results_112[:15]:
    ok = "✓" if s < 1 else "✗ FAILS"
    print(f"({p},{q},{r1},{r2}){'':5}  {qa:10.6f}  {rho3:10.6f}  {s:10.6f}  {ok}")

if results_112:
    max_sum_112 = max(s for *_,s in results_112)
    all_ok_112 = all(s < 1 for *_,s in results_112)
    print(f"\nAll quality+rho³<1: {'✓' if all_ok_112 else '✗'}")
    print(f"Max quality+rho³ = {max_sum_112:.8f} (over {len(results_112)} triples)")

# ====== General conjecture ======
print("\n" + "="*70)
print("CONJECTURE (Quality-ρ Joint Bound):")
print("  For any squarefree coprime abc with ω(abc)=ω and quality q=log(c)/log(rad):")
print("  quality + ρ^{ω-1} < 1")
print("  where ρ = nd/rad(abc)^{1/(ω-1)} and nd = F10's minimum non-degenerate norm.")
print()
print("  The bound is TIGHT: quality + ρ^{ω-1} → 1 in the extremal families")
print("  (e.g., ω=3 type (1,1,1) with p=2 and q→∞ along Sophie Germain pairs).")
print()
print("  This is a NEW JOINT BOUND connecting abc quality with Pasten lattice geometry.")
print("  Note: quality < 1 trivially (squarefree); ρ^{ω-1} < 1 from F3/F10.")
print("  The JOINT bound quality+ρ^{ω-1}<1 is stronger than either alone.")
