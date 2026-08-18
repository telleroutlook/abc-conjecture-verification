"""
T29 — OB-12 Claim B complete: type (1,1,2) c-odd subfamily analysis

SETUP: type (1,1,2) means a=p (prime), b=q (prime), c=r₁r₂ (2 primes), p+q=r₁r₂.
Two subfamilies:
  (1) c-even: p,q both odd primes → c=p+q even → 2|c → r₁=2.
      F14 PROVED: sup ρ = 2^{-1/3} (never achieved, approached as p≈q→∞).
  (2) c-odd: p=2, q odd prime → c=2+q odd → r₁,r₂ both odd.
      CLAIM (T29): ρ→0 as q grows; max is finite at small triples.

PROOF for c-odd subfamily:
  For a=2, b=q (odd prime), c=2+q=r₁r₂ (r₁<r₂ odd primes):
  By F10: nd = second_smallest{2, q, r₁}.
  Since r₁ is odd prime ≥3>2 and c=r₁r₂=2+q with r₁≤√c:
    If r₁<q: second_smallest{2, q, r₁} = r₁.  [r₁ is middle element]
    If r₁≥q: r₁r₂ ≥ r₁² ≥ q² and r₁r₂ = 2+q ≤ q+2, so q²≤q+2 → q≤2. Contradiction.
    Therefore r₁ < q ALWAYS, so nd = r₁.

  ρ³ = r₁³/R = r₁³/(2·q·r₁·r₂) = r₁²/(2q·r₂).
  From r₁r₂=2+q: r₂=(2+q)/r₁. So ρ³ = r₁³/(2q(2+q)).
  Since r₁≤√(2+q): ρ³ ≤ (2+q)^{3/2}/(2q(2+q)) = √(2+q)/(2q) → 0 as q→∞.

  The maximum occurs at the smallest valid r₁ (=3) and smallest r₂ prime with q=3r₂-2 prime:
    r₂=5: c=15, q=13, ρ = 3/(2·13·15)^{1/3}. [First case with r₁=3]

CONSEQUENCE: sup ρ (type (1,1,2)) = sup from c-even = 2^{-1/3} ≈ 0.7937.
  The c-odd subfamily contributes a finite maximum < 0.42, much below 2^{-1/3}.
"""


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = 1
    return f


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def isprime(n):
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


def is_squarefree(n):
    return all(v == 1 for v in factorize(n).values())


def partition_type(a, b, c):
    return len(factorize(a)), len(factorize(b)), len(factorize(c))


def nd_norm(a, b, c):
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    Pa = sorted(fa)
    Pb = sorted(fb)
    Pc = sorted(fc)
    mA = Pa[0] if Pa else float("inf")
    mB = Pb[0] if Pb else float("inf")
    mC = Pc[0] if Pc else float("inf")
    cands = []
    if Pa and Pb:
        cands.append(max(mA, mB))
    if Pa and Pc:
        cands.append(max(mA, mC))
    if Pb and Pc:
        cands.append(max(mB, mC))
    return min(cands) if cands else float("inf")


print("T29: OB-12 Claim B — type (1,1,2) c-odd subfamily")
print("=" * 60)
print()

# ── ANALYTICAL PROOF ─────────────────────────────────────────────────────────
print("ANALYTICAL PROOF: c-odd subfamily has ρ → 0")
print()
print("  a=2, b=q (odd prime), c=2+q=r₁r₂ (r₁<r₂ odd primes)")
print("  nd = r₁ always (proved: r₁<q is always true)")
print("  ρ³ = r₁³/(2q(2+q)) ≤ (2+q)^{3/2}/(2q(2+q)) = √(2+q)/(2q) → 0")
print()

# ── GROWING SEQUENCE (verify r₁ < q always) ──────────────────────────────────
print("Growing sequence for r₁=3 (smallest valid): (2, q, 3r₂) with q=3r₂-2")
print()
print(f"  {'(a,b,c)':>25}  {'r₁':>4}  {'nd':>4}  {'ρ':>10}  {'2^{-1/3}':>10}")
count = 0
for r2 in range(5, 200):
    if not isprime(r2) or r2 == 3:
        continue
    c = 3 * r2
    q = c - 2
    if not isprime(q) or q == 3:
        continue
    if gcd(2, q) != 1:
        continue
    R = 2 * q * 3 * r2
    nd = 3
    ratio = nd / R ** (1 / 3)
    print(f"  (2, {q}, {c}={3}·{r2}):  r₁=3  nd=3  ρ={ratio:.8f}  {2 ** (-1 / 3):.8f}")
    count += 1
    if count >= 10:
        break
print()

# ── VERIFY r₁ < q ALWAYS ─────────────────────────────────────────────────────
print("Verifying r₁ < q for ALL type (1,1,2) c-odd triples (c ≤ 3000)...")
r1_ge_q_count = 0
for c in range(6, 3001):
    if c % 2 == 0:
        continue  # c-odd only
    fc = factorize(c)
    if not is_squarefree(c) or len(fc) != 2:
        continue
    r1, r2 = sorted(fc.keys())
    q = c - 2
    if q < 2 or not isprime(q):
        continue
    a = 2
    b = q
    if gcd(a, b) != 1 or gcd(b, c) != 1:
        continue
    if partition_type(a, b, c) != (1, 1, 2):
        continue
    if r1 >= q:
        print(f"  r₁≥q case: ({a},{b},{c}) r₁={r1} q={q}")
        r1_ge_q_count += 1
print(f"  r₁≥q violations: {r1_ge_q_count} (expected: 0)")
print()

# ── FULL NUMERICAL MAX FOR c-ODD ─────────────────────────────────────────────
print("Maximum ρ for type (1,1,2) c-odd triples (c ≤ 5000)...")
max_r = 0
max_t = None
for c in range(6, 5001):
    if c % 2 == 0:
        continue
    fc = factorize(c)
    if not is_squarefree(c) or len(fc) != 2:
        continue
    q = c - 2
    if q < 2 or not isprime(q):
        continue
    if gcd(2, q) != 1 or gcd(q, c) != 1:
        continue
    if partition_type(2, q, c) != (1, 1, 2):
        continue
    R = 2 * q * c
    nd = nd_norm(2, q, c)
    ratio = nd / R ** (1 / 3)
    if ratio > max_r:
        max_r = ratio
        max_t = (2, q, c)
print(f"  Max ρ (c-odd) = {max_r:.10f} at {max_t}")
print()

# ── COMPARE WITH c-EVEN SUPREMUM ─────────────────────────────────────────────
print("COMPARISON:")
print(f"  c-odd max ρ         = {max_r:.6f} at {max_t} (FINITE MAXIMUM)")
print(f"  c-even sup ρ        = {2 ** (-1 / 3):.6f}  (2^{{-1/3}}, never achieved)")
print(f"  Ratio c-odd/c-even  = {max_r / 2 ** (-1 / 3):.4f}")
print()

# ── FULL TYPE (1,1,2) SCAN (both even and odd c) ─────────────────────────────
print("Verifying sup = 2^{-1/3} for ALL type (1,1,2) triples (c ≤ 5000)...")
TARGET = 2 ** (-1 / 3)
violations = 0
max_all = 0
max_all_t = None
for c in range(4, 5001):
    for a in range(1, (c + 1) // 2 + 1):
        b = c - a
        if b < a or gcd(a, b) != 1:
            continue
        if not (is_squarefree(a) and is_squarefree(b) and is_squarefree(c)):
            continue
        if partition_type(a, b, c) != (1, 1, 2):
            continue
        from math import prod as mprod

        R = mprod(set(factorize(a)) | set(factorize(b)) | set(factorize(c)))
        nd = nd_norm(a, b, c)
        ratio = nd / R ** (1 / 3)
        if ratio > max_all:
            max_all = ratio
            max_all_t = (a, b, c)
        if ratio > TARGET + 1e-9:
            violations += 1
            print(f"  VIOLATION: ({a},{b},{c}) ρ={ratio:.6f} > 2^{{-1/3}}")
print(f"  Max ρ overall = {max_all:.10f} at {max_all_t}")
print(f"  2^{{-1/3}}      = {TARGET:.10f}")
print(f"  Gap            = {TARGET - max_all:.10f}")
print(f"  Violations: {violations}")
if violations == 0:
    print("  All type (1,1,2) triples satisfy ρ < 2^{-1/3}. ✓")
print()

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("THEOREM (OB-12 Claim B, CONFIRMED):")
print()
print("  sup ρ for type (1,1,2) = 2^{-1/3} ≈ 0.7937.")
print("  Proof structure:")
print("  (A) c-EVEN subfamily (a,b both odd primes):")
print("      nd = a (= smaller of a,b); ρ³ = a²/(b(a+b)) < 1/2 since b>a.")
print("      Supremum 2^{-1/3} as a/b→1 (proved F14). Never achieved.")
print("  (B) c-ODD subfamily (a=2, b odd prime, c=2+b=r₁r₂):")
print("      nd = r₁ (the smallest prime factor of c, always < b).")
print("      ρ³ = r₁³/(2b(2+b)) ≤ √(2+b)/(2b) → 0 as b→∞.")
print(
    f"      Finite max at (2,13,15): ρ ≈ {3 / (2 * 13 * 15) ** (1 / 3):.6f} ≪ 2^{{-1/3}}."
)
print()
print("  The overall supremum is from the c-even subfamily.")
print("  The c-odd subfamily contributes only a finite maximum < 0.42.")
print()
print("  OB-12 Claim B: CONFIRMED (sup = 2^{-1/3}).")
print("  OB-12 Claim C: CONFIRMED (from T27/F15; explicit growing subfamilies).")
