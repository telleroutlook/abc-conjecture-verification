"""
T61 — W_psi encoding for non-squarefree triples

For squarefree type (1,1,1): W_psi = ±c (proved).
For squarefree type (1,1,k): W_psi = ±a (T58).
For non-squarefree: what does W_psi encode?

This script extends T57's study to systematically classify W_psi
for non-squarefree triples across different structural types.

Key question: is there ANY formula W_psi = f(a,b,c,R,v_max,...) that
holds universally for non-squarefree triples?

DEFINITIONS:
  W_phi = Σ_{p∈Pb} φ_p - Σ_{p∈Pa} φ_p  (phi-Wronskian)
  W_psi = Σ_{p∈Pb} p·φ_p - Σ_{p∈Pa} p·φ_p  (psi-Wronskian = phi-Wronskian weighted by p)

CONSTRAINT (non-squarefree): Σ v_p(a)·φ_p + Σ v_p(b)·φ_p = Σ v_p(c)·φ_p
"""

import math
from itertools import product as iproduct

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return factors

def rad(n):
    return math.prod(factorize(n).keys()) if n > 1 else 1

def find_min_nondeg_full(a, b, bound=8):
    """Full brute-force min nondeg for non-squarefree triples."""
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    all_p = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    omega = len(all_p)
    if omega > 5 or omega == 0: return None
    # constraint coefficients: v_a(p) + v_b(p) - v_c(p) for each p
    cc = {p: fa.get(p,0) + fb.get(p,0) - fc.get(p,0) for p in all_p}
    Pa = list(fa.keys())
    Pb = list(fb.keys())
    best = {'norm': float('inf'), 'phi': None, 'W_phi': None, 'W_psi': None}
    for vals in iproduct(*[range(-bound, bound+1)]*omega):
        phi = {all_p[i]: vals[i] for i in range(omega)}
        if all(v==0 for v in vals): continue
        if sum(cc[p]*phi[p] for p in all_p) != 0: continue
        W_phi = sum(phi.get(p,0) for p in Pb) - sum(phi.get(p,0) for p in Pa)
        if W_phi == 0: continue
        norm = max(p*abs(phi[p]) for p in all_p)
        if norm == 0: continue
        if norm < best['norm']:
            best['norm'] = norm
            best['phi'] = dict(phi)
            best['W_phi'] = W_phi
            best['W_psi'] = sum(p*phi[p] for p in Pb) - sum(p*phi[p] for p in Pa)
    return best if best['norm'] < float('inf') else None

def classify(w, a, b, c, R, vmax):
    """Classify W_psi as a function of the triple's invariants."""
    for sign in [1,-1]:
        for val, name in [
            (a,'a'), (b,'b'), (c,'c'), (R,'R'),
            (a+b,'a+b'), (a*b,'a*b'), (c-a,'c-a'), (c-b,'c-b'),
            (vmax,'v_max'), (a*vmax,'a*v'), (b*vmax,'b*v'), (c*vmax,'c*v'),
        ]:
            if val > 0 and w == sign*val:
                return f"{'+'if sign>0 else '-'}{name}"
    return str(w)

# ── Test cases organized by type ─────────────────────────────────────────────
print("T61: W_psi classification for non-squarefree triples")
print("="*95)
print(f"{'(a,b,c)':<18} {'type':<12} {'v_max':>6} {'R':>5} {'qual':>5} "
      f"{'nd':>5} {'W_phi':>7} {'W_psi':>8} {'W_psi=?':>12}")
print("-"*95)

# Squarefree baseline
baseline = [
    (2,3,None,'sq (1,1,1)'), (2,5,None,'sq (1,1,1)'), (3,5,None,'sq (1,1,2)'),
    (2,13,None,'sq (1,1,2)'),
]
# Non-squarefree cases
nonsq = [
    # c = prime^k
    (1,3,None,'ns (0,1,1)'),(1,7,None,'ns (0,1,1)'),(1,8,None,'ns (0,1,1)'),
    (1,15,None,'ns (0,2,1)'),(1,24,None,'ns (0,2,1)'),(1,48,None,'ns (0,2,1)'),
    # a or b = prime^k
    (4,5,None,'ns (1,1,1)'),(8,1,None,'ns (1,0,1)'),(9,16,None,'ns (1,1,1)'),
    (4,21,None,'ns (1,2,1)'),(25,2,None,'ns (1,1,1)'),
    # multiple non-squarefree
    (4,5,None,'ns'),(8,9,None,'ns'),(4,45,None,'ns'),
    (2,7,None,'ns (0,1,1)'),(16,9,None,'ns'),
]

all_cases = baseline + nonsq
seen = set()
for (a,b,_,label) in all_cases:
    if math.gcd(a,b) != 1: continue
    key = (min(a,b), max(a,b))
    if key in seen: continue
    seen.add(key)
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    R = rad(a*b*c)
    qual = math.log(c)/math.log(R) if R > 1 else 0
    vmax = max([max(fa.values()) if fa else 0,
                max(fb.values()) if fb else 0,
                max(fc.values()) if fc else 0])
    res = find_min_nondeg_full(a, b, bound=8)
    if res is None: continue
    enc = classify(res['W_psi'], a, b, c, R, vmax)
    sq = 'sq' if (all(v==1 for v in fa.values()) and
                  all(v==1 for v in fb.values()) and
                  all(v==1 for v in fc.values())) else 'ns'
    print(f"  ({a},{b},{c}){'':<5} [{sq}]{label[3:]:>8} {vmax:>6} {R:>5} {qual:>5.3f} "
          f"{res['norm']:>5} {res['W_phi']:>7} {res['W_psi']:>8} {enc:>12}")

print()
print("ANALYSIS:")
print("  - Squarefree type (1,1,1): W_psi = ±c")
print("  - Squarefree type (1,1,k): W_psi = ±a")
print("  - Non-squarefree: W_psi encodes ??? (see above)")
print()
print("H1 check (|W_psi| <= omega*nd for all cases):")

all_ok = True
for (a,b,_,label) in all_cases:
    if math.gcd(a,b) != 1: continue
    key = (min(a,b), max(a,b))
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    omega = len(set(list(fa.keys())+list(fb.keys())+list(fc.keys())))
    res = find_min_nondeg_full(a, b, bound=8)
    if res is None: continue
    ok = abs(res['W_psi']) <= omega * res['norm']
    if not ok:
        print(f"  FAIL: ({a},{b},{c}): |W_psi|={abs(res['W_psi'])} > omega*nd={omega*res['norm']}")
        all_ok = False
print(f"  {'ALL PASS ✓' if all_ok else 'SOME FAIL ✗'}")
