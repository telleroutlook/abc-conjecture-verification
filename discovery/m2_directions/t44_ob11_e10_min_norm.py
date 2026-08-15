"""
T44 — Toy verifier for Theorem E10 (OB-11):
For omega=3 squarefree coprime (a,b,c)=( p, q, r=p+q) all prime,
the minimum-norm nonzero vector in the Pasten lattice L is non-degenerate.

Lattice constraint: qr*psi_p + pr*psi_q - pq*psi_r = 0
Wronskian: W(psi) = (p*psi_q - q*psi_p)  [sign, ab/(pq) factor ignored]

KEY CHECK: OB-11 claims min norm = r, but F10 predicts nd = second_smallest{p,q,r} = max(p,q).
           The vector (p,-q,0) is in L, has norm max(p,q) < r, and is non-degenerate.
"""

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def in_lattice(p, q, r, psi):
    return q*r*psi[0] + p*r*psi[1] - p*q*psi[2] == 0

def wronskian(p, q, psi):
    return p*psi[1] - q*psi[0]

def linf(psi):
    return max(abs(x) for x in psi)

print("T44: Verifying min norm and non-degeneracy for omega=3 Pasten lattice")
print("="*70)

# Collect prime triples (p, q, r=p+q)
triples = []
primes = [p for p in range(2, 200) if is_prime(p)]
for p in primes:
    for q in primes:
        if q <= p: continue
        r = p + q
        if is_prime(r):
            triples.append((p, q, r))

print(f"Found {len(triples)} omega=3 squarefree prime triples (p<q, r=p+q prime) up to p,q<200")
print()

# For each triple, find minimum norm vector and check non-degeneracy
issues = []
confirmed = 0

for p, q, r in triples[:20]:  # Show details for first 20
    # Explicit minimum vectors
    v1 = (p, 0, r)   # OB-11 claims this; norm = r
    v2 = (0, q, r)   # OB-11 claims this; norm = r
    v3 = (p, -q, 0)  # F10 candidate; norm = max(p,q) = q
    v4 = (-p, q, 0)  # symmetric; norm = q

    # Verify all are in L
    assert in_lattice(p, q, r, v1), f"v1 not in L for ({p},{q},{r})"
    assert in_lattice(p, q, r, v2), f"v2 not in L for ({p},{q},{r})"
    assert in_lattice(p, q, r, v3), f"v3 not in L for ({p},{q},{r})"
    assert in_lattice(p, q, r, v4), f"v4 not in L for ({p},{q},{r})"

    min_norm_v1 = linf(v1)  # = r
    min_norm_v3 = linf(v3)  # = q = max(p,q)

    w1 = wronskian(p, q, v1)  # = p*0 - q*p = -qp
    w3 = wronskian(p, q, v3)  # = p*(-q) - q*p = -2pq

    # Brute-force: find actual minimum norm in a bounded region
    actual_min = float('inf')
    actual_min_vec = None
    for ap in range(-r, r+1):
        for aq in range(-r, r+1):
            # Constraint: qr*ap + pr*aq = pq*ar => ar = r*(q*ap + p*aq)/(pq)
            num = q*r*ap + p*r*aq
            if num % (p*q) != 0:
                continue
            ar = num // (p*q)
            if ap == 0 and aq == 0 and ar == 0:
                continue
            vec = (ap, aq, ar)
            n = linf(vec)
            if n < actual_min:
                actual_min = n
                actual_min_vec = vec

    # Is the actual min vector non-degenerate?
    w_actual = wronskian(p, q, actual_min_vec)

    ob11_claim = r  # OB-11 says min = r
    f10_pred = q    # F10 says min = max(p,q) = q (since p<q)

    print(f"({p},{q},{r}): OB-11 claims min={ob11_claim}, F10 predicts min={f10_pred}")
    print(f"  v3=({p},-{q},0) in L, norm={min_norm_v3}, W={w3} {'≠0 NON-DEG' if w3 != 0 else 'DEG!'}")
    print(f"  brute-force min norm={actual_min} at {actual_min_vec}, W={w_actual} {'≠0 NON-DEG' if w_actual != 0 else 'DEG!'}")
    print(f"  OB-11 correct? {ob11_claim == actual_min}  |  F10 correct? {f10_pred == actual_min}")
    print()

    if actual_min != f10_pred:
        issues.append((p, q, r, actual_min, f10_pred))
    if w_actual == 0:
        issues.append((p, q, r, "DEGENERATE MIN", actual_min_vec))
    else:
        confirmed += 1

print("="*70)
print(f"Full check over {len(triples)} triples:")
ob11_wrong = 0
for p, q, r in triples:
    # v3=(p,-q,0) is in L with norm q < r
    assert in_lattice(p, q, r, (p,-q,0))
    assert linf((p,-q,0)) == q
    assert wronskian(p, q, (p,-q,0)) != 0  # non-degenerate
    # So min norm <= q < r, contradicting OB-11's claim of r
    ob11_wrong += 1

print(f"  v=(p,-q,0) in L, norm=q<r, non-degenerate: CONFIRMED for all {ob11_wrong} triples")
print(f"  OB-11 Step 1 ('min norm = r') is WRONG for all triples (norm = q = max(p,q) < r)")
print()
print("CORRECTED THEOREM E10:")
print("  Min norm = max(p,q) = q (assuming p<q)")
print("  Achieved by v=(p,-q,0), which is non-degenerate (W = -2pq ≠ 0)")
print("  This is consistent with F10: nd = second_smallest{p,q,r} = q")
print()
print("Proof:")
print("  1. For psi_r=0: qr*psi_p + pr*psi_q = 0 => q*psi_p + p*psi_q = 0")
print("     gcd(p,q)=1 => p|psi_p. Write psi_p=p*t, psi_q=-q*t. Min |t|=1 => norm=max(p,q)=q.")
print("  2. For psi_r≠0: r|psi_r (from gcd(r,pq)=1) => |psi_r|>=r > q.")
print("     So all psi with psi_r≠0 have norm > q.")
print("  3. Global min norm = q, achieved by (p,-q,0). Wronskian = p(-q)-q(p) = -2pq ≠ 0.")
print("     MINIMUM VECTOR IS NON-DEGENERATE. QED.")
