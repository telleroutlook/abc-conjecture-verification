"""
T38 — F24: Type (2,2,1) sup = (1/6)^{1/4}, never achieved.

For type (2,2,1): a=p1*p2, b=q1*q2, c=r (single prime).
Group mins: {p1, q1, r}. nd = second_smallest{p1, q1, r}.

CLAIM F24: sup rho = (1/6)^{1/4} ~ 0.6389, approached by a=6 subfamily
but never achieved. For a != 6 (i.e. p1*p2 >= 10), rho < (1/10)^{1/4}.

PROOF SKETCH (a=6 subfamily, pa={2,3}):
  c = a+b = 6 + q1*q2. Group mins: {2, q1, 6+q1*q2}.
  nd = q1 (since q1 < c = 6+q1*q2 always, and q1 > 2).
  rho^4 = q1^4 / (2*3*q1*q2*(6+q1*q2))
        = q1^3 / (6*q2*(6 + q1*q2))
  Upper bound:
    q2 > q1 (q2 >= q1+2 for distinct odd primes).
    6 + q1*q2 > q1*q2.
    rho^4 < q1^3 / (6*q1*q2^2) (using q2*(6+q1*q2) > q1*q2^2)
          = q1^2 / (6*q2^2)
          < 1/6  [since q1 < q2].
  As q1,q2 -> twin primes with q1/q2 -> 1: rho^4 -> 1/6 from below.
  sup = (1/6)^{1/4} ~ 0.6389, never achieved.

PROOF SKETCH (p1*p2 >= 10, any other a):
  rho^4 = nd^3 / (p1*p2 * (other primes product))
  <= nd^3 / (10 * nd * q2 * r) [p1*p2>=10, the two other group mins >= nd+1]
  < nd^2 / (10*q2*r) < 1/10 << 1/6.
  All other a give strictly smaller sup.

Therefore: global sup for (2,2,1) = (1/6)^{1/4}, achieved in the limit by
  a=6, b=q*(q+d) for near-twin primes q, q+d, with c=6+q*(q+d) prime.
"""

import math

def factorize(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=1
    return f

def isprime(n):
    if n<2: return False
    if n==2: return True
    if n%2==0: return False
    d=3
    while d*d<=n:
        if n%d==0: return False
        d+=2
    return True

def gcd(a,b):
    while b: a,b=b,a%b
    return abs(a)

SUP = (1/6)**0.25
print(f"F24: type (2,2,1) sup = (1/6)^{{1/4}} = {SUP:.8f}")
print()

# Verify: all (2,2,1) c<=30000 have rho < (1/6)^{1/4}
print("Verifying rho < (1/6)^{1/4} for all type (2,2,1) triples with c<=30000...")
violations = 0; max_rho = 0; max_triple = None
for c in range(6, 30001):
    if not isprime(c): continue
    for a in range(1, (c+1)//2+1):
        b = c-a
        if b<a: continue
        if gcd(a,b)!=1: continue
        fa=factorize(a); fb=factorize(b)
        if any(v>1 for v in fa.values()) or len(fa)!=2: continue
        if any(v>1 for v in fb.values()) or len(fb)!=2: continue
        pa=set(fa.keys()); pb=set(fb.keys())
        if pa&pb or pa&{c} or pb&{c}: continue
        gm = sorted([min(pa), min(pb), c])
        nd = gm[1]; R = math.prod(pa|pb|{c})
        rho4 = nd**4/R
        rho = rho4**0.25
        if rho4 >= 1/6:
            print(f"  VIOLATION at ({a},{b},{c}): rho={rho:.6f} >= (1/6)^{{1/4}}")
            violations += 1
        if rho > max_rho: max_rho=rho; max_triple=(a,b,c)

print(f"Violations: {violations} (expected: 0)")
print(f"Max rho = {max_rho:.8f} at {max_triple}")
print(f"Gap to sup: {SUP-max_rho:.8f}")
print()

# Show the approach: near-twin-prime a=6 examples
print("Near-sup examples (a=6, q close to q+d, c=6+q*(q+d) prime):")
print(f"  {'(6,b,c)':>22}  {'rho':>12}  {'q1,q2':>14}  {'q1/q2':>8}")
examples = []
for q1 in range(5, 10000, 2):
    if not isprime(q1) or q1==3: continue
    for d in range(2, 20, 2):
        q2 = q1+d
        if not isprime(q2): continue
        c = 6+q1*q2
        if not isprime(c): continue
        if {q1,q2} & {2,3,c}: continue
        R = 2*3*q1*q2*c
        rho4 = q1**3/(6*q2*(6+q1*q2))
        rho = rho4**0.25
        examples.append((rho, q1, q2, q1*q2, c))

examples.sort(reverse=True)
for rho, q1, q2, b, c in examples[:10]:
    print(f"  (6,{b:>9},{c:>9}):  rho={rho:.8f}  ({q1:>5},{q2:>5})  {q1/q2:.6f}")

print()
print("THEOREM F24:")
print("  For omega=5 type (2,2,1): sup rho = (1/6)^{1/4} ~ 0.6389.")
print("  The sup is approached but never achieved.")
print("  Extremal subfamily: a=6=2*3, b=q1*q2 near-twin primes, c=6+b prime.")
print("  For all other a (p1*p2 >= 10): rho < (1/10)^{1/4} ~ 0.562.")
