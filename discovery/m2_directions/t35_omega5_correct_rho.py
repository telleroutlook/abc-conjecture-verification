"""
T35 — Correct F10 rho for omega=5 types.

F10 nd = second smallest of {min(Pa), min(Pb), min(Pc)}.
For a=1 (Pa empty): nd = max(min(Pb), min(Pc)).

T33/T34 used nd = second smallest of ALL primes — WRONG for multi-prime groups.
"""
import math

def factorize(n):
    f = {}; d = 2
    while d*d <= n:
        while n%d == 0: f[d]=f.get(d,0)+1; n//=d
        d += 1
    if n > 1: f[n] = 1
    return f

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

def f10_nd(a, b, c):
    """F10 nd = second smallest of {min(Pa), min(Pb), min(Pc)}, skipping empty groups."""
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    group_mins = []
    if fa: group_mins.append(min(fa.keys()))
    if fb: group_mins.append(min(fb.keys()))
    if fc: group_mins.append(min(fc.keys()))
    group_mins.sort()
    if len(group_mins) < 2: return None
    return group_mins[1]  # second smallest

C_MAX = 3000
records = {}; total = 0

for c in range(6, C_MAX+1):
    fc = factorize(c)
    if any(v>1 for v in fc.values()): continue
    for a in range(1, (c+1)//2 + 1):
        b = c - a
        if b < a: continue
        if gcd(a,b) != 1: continue
        fa = factorize(a); fb = factorize(b)
        if any(v>1 for v in fa.values()) or any(v>1 for v in fb.values()): continue
        pa=set(fa.keys()); pb=set(fb.keys()); pc=set(fc.keys())
        if pa&pb or pa&pc or pb&pc: continue
        omega = len(pa)+len(pb)+len(pc)
        if omega != 5: continue
        R = math.prod(pa|pb|pc)
        nd = f10_nd(a, b, c)
        if nd is None: continue
        rho = nd / R**0.25
        sa,sb,sc = len(pa),len(pb),len(pc)
        tkey = (sa,sb,sc)
        total += 1
        if tkey not in records or rho > records[tkey][0]:
            records[tkey] = (rho, a, b, c)

print(f"omega=5 triples c<={C_MAX}: {total}")
print()
print("Max rho (CORRECT F10 nd) by type:")
for tkey in sorted(records, key=lambda k: -records[k][0]):
    rho, a, b, c = records[tkey]
    nd = f10_nd(a, b, c)
    R = math.prod(factorize(a).keys()|factorize(b).keys()|factorize(c).keys())
    print(f"  {tkey}: max rho={rho:.5f}  at ({a},{b},{c})  nd={nd}  R={R}")
print()
mx = max(v[0] for v in records.values())
print(f"Global max rho (c<={C_MAX}): {mx:.6f}")
print(f"  Note: (0,2,3) with near-equal b-primes approaches rho->1 (sup=1)")
