"""
T23 — Complete classification theorem (F12): sharp universal bounds for bounded types

THEOREM F12 (synthesizing F3–F11):

For squarefree coprime (a,b,c) with a+b=c (canonical a ≤ b ≤ c), let:
  ω = ω(abc), R = rad(abc), partition type (n_a, n_b, n_c).
  m₂ = second smallest of {min(P_a), min(P_b), min(P_c)}  [F10 formula]
  ‖ψ_nd‖ = m₂  [minimum non-degenerate ψ-norm]

UNIVERSALLY BOUNDED TYPES and their sharp ratio bounds:
  ω=3: (1,1,1)  ratio ≤ 1/√2 ≈ 0.7071  (conjectured sharp; proved ≤ √(7/6) ≈ 1.08)
  ω=4: (0,2,2)  ratio → 0,  sup ≤ 0.506
  ω=4: (1,1,2)  ratio → 0,  sup ≤ 0.750
  ω=4: (1,2,1)  ratio ≤ 2^{-1/3} ≈ 0.7937 [F7a: analytical proof]
  ω=5: (1,2,2)  ratio → 0,  sup ≤ 0.500
  ω=5: (2,1,2)  ratio → 0,  sup ≤ 0.595
  ω=5: (2,2,1)  ratio → 0,  sup ≤ 0.582

EVENTUALLY UNBOUNDED TYPES (ratio → ∞ along some growing subfamily):
  All other types at ω ≥ 4, including ALL types at ω ≥ 6.

This script:
1. Verifies the sup bounds numerically for c ≤ 500
2. Attempts to find the sharp constant for each bounded type
3. Checks whether the F7a bound 2^{-1/3} is sharp for (1,2,1)
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

def is_squarefree(n):
    return all(v==1 for v in factorize(n).values())

def optimal_nd_norm(a,b,c):
    fa,fb,fc=factorize(a),factorize(b),factorize(c)
    Pa=sorted(fa); Pb=sorted(fb); Pc=sorted(fc)
    mA=Pa[0] if Pa else float('inf')
    mB=Pb[0] if Pb else float('inf')
    mC=Pc[0] if Pc else float('inf')
    cands=[]
    if Pa and Pb: cands.append(max(mA,mB))
    if Pa and Pc: cands.append(max(mA,mC))
    if Pb and Pc: cands.append(max(mB,mC))
    return min(cands) if cands else float('inf')

def rad(a,b,c):
    ps=set(factorize(a))|set(factorize(b))|set(factorize(c))
    r=1
    for p in ps: r*=p
    return r

def partition_type(a,b,c):
    fa,fb,fc=factorize(a),factorize(b),factorize(c)
    return len(fa),len(fb),len(fc)

# Collect all bounded-type triples up to c=500
bounded_types = {
    3: [(1,1,1)],
    4: [(0,2,2),(1,1,2),(1,2,1)],
    5: [(1,2,2),(2,1,2),(2,2,1)],
}

from collections import defaultdict
data = defaultdict(list)  # (omega, type) -> [(a,b,c,ratio)]

for c in range(4, 501):
    for a in range(1, (c+1)//2+1):
        b = c-a
        if b<=0 or b<a: continue
        if gcd(a,b)!=1: continue
        if not (is_squarefree(a) and is_squarefree(b) and is_squarefree(c)): continue
        pt=partition_type(a,b,c)
        fa,fb,fc=factorize(a),factorize(b),factorize(c)
        omega=len(set(fa)|set(fb)|set(fc))
        if omega not in bounded_types: continue
        if pt not in bounded_types[omega]: continue
        R=rad(a,b,c)
        nd=optimal_nd_norm(a,b,c)
        ratio=nd/R**(1.0/(omega-1))
        data[(omega,pt)].append((a,b,c,ratio,nd))

print("T23: Sharp universal bounds for universally-bounded types")
print("="*65)
print()

KNOWN_BOUNDS = {
    (3,(1,1,1)): math.sqrt(7/6),
    (4,(1,2,1)): 2**(-1/3),
}

for omega in [3,4,5]:
    for pt in bounded_types[omega]:
        key=(omega,pt)
        if key not in data: continue
        entries=data[key]
        ratios=[e[3] for e in entries]
        max_r=max(ratios)
        worst=max(entries,key=lambda x:x[3])
        best=min(entries,key=lambda x:x[3])
        n=len(entries)

        known=KNOWN_BOUNDS.get(key)
        bound_str=f"known={known:.4f}" if known else "conjectured"
        print(f"Type ω={omega} {str(pt):10}: n={n:4}, max_ratio={max_r:.6f}  ({bound_str})")
        print(f"  worst: a={worst[0]}, b={worst[1]}, c={worst[2]}, nd={worst[4]}, ratio={worst[3]:.6f}")
        if known and max_r > known + 1e-9:
            print(f"  *** BOUND VIOLATED: {max_r:.6f} > {known:.6f} ***")
        print()

print()
print("Checking F7a: ratio ≤ 2^{-1/3} for ALL type (1,2,1) triples...")
violations = 0
BOUND = 2**(-1.0/3)
for (a,b,c,ratio,nd) in data.get((4,(1,2,1)),[]):
    if ratio > BOUND + 1e-9:
        print(f"  VIOLATION: ({a},{b},{c}) ratio={ratio:.6f} > 2^(-1/3)={BOUND:.6f}")
        violations += 1
if violations == 0:
    print(f"  All {len(data.get((4,(1,2,1)),[]))} triples satisfy ratio ≤ 2^{{-1/3}} = {BOUND:.6f}. ✓")

print()
print("Approach to the sharp constant for each type:")
print()

# For (1,2,1): check if ratio approaches 2^{-1/3} from below
print("Type (1,2,1): ratio → 2^{-1/3}?")
entries_121 = sorted(data.get((4,(1,2,1)),[]), key=lambda x: -x[3])
print(f"  {'(a,b,c)':>20}  {'ratio':>10}  {'2^(-1/3)-ratio':>14}")
for a,b,c,ratio,nd in entries_121[:10]:
    print(f"  ({a:>4},{b:>4},{c:>4})  {ratio:>10.6f}  {2**(-1/3)-ratio:>14.8f}")

print()
print("Type (0,2,2): ratio → 0 (best subfamily)?")
entries_022 = sorted(data.get((4,(0,2,2)),[]), key=lambda x: x[3])
print(f"  {'(a,b,c)':>20}  {'ratio':>10}  {'trend'}")
for a,b,c,ratio,nd in entries_022[:8]:
    print(f"  ({a:>4},{b:>4},{c:>4})  {ratio:>10.6f}")

print()
print("THEOREM F12 SUMMARY:")
print()
print("  min nd norm = second smallest of {min_Pa, min_Pb, min_Pc}  [F10]")
print()
print("  UNIVERSALLY BOUNDED types (ratio ≤ C for all triples of the type):")
print(f"  ω=3 (1,1,1): ratio ≤ √(7/6)={math.sqrt(7/6):.4f}  (proved F3; conjectured sharp 1/√2)")
print(f"  ω=4 (0,2,2): ratio → 0; sup ≤ {max(e[3] for e in data.get((4,(0,2,2)),[0,0,0,0,0])):.4f}  (numerical)")
print(f"  ω=4 (1,1,2): ratio → 0; sup ≤ {max(e[3] for e in data.get((4,(1,1,2)),[0,0,0,0,0])):.4f}  (numerical)")
print(f"  ω=4 (1,2,1): ratio ≤ 2^(-1/3)={2**(-1/3):.4f}  (proved F7a; sharp? gap={2**(-1/3)-max(e[3] for e in data.get((4,(1,2,1)),[0,0,0,0,0])):.5f})")
print(f"  ω=5 (1,2,2): ratio → 0; sup ≤ {max(e[3] for e in data.get((5,(1,2,2)),[0,0,0,0,0])):.4f}  (numerical)")
print(f"  ω=5 (2,1,2): ratio → 0; sup ≤ {max(e[3] for e in data.get((5,(2,1,2)),[0,0,0,0,0])):.4f}  (numerical)")
print(f"  ω=5 (2,2,1): ratio → 0; sup ≤ {max(e[3] for e in data.get((5,(2,2,1)),[0,0,0,0,0])):.4f}  (numerical)")
print()
print("  All other types (ω≥4): EVENTUALLY UNBOUNDED (ratio → ∞ in some subfamily).")
print()
print("  OPEN: Are the numerical sup bounds for ω=4,5 bounded types sharp?")
print("  OPEN: Does ratio → 0 for all bounded types except (1,2,1)?")
