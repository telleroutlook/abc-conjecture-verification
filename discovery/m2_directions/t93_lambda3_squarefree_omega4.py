"""
T93 — Empirical discovery of λ₃ for squarefree ω*=4 coprime triples.

Context:
  F36 (proved): λ₂(a,b) = min(2p₂, p₃) for squarefree ω*≥3.
  Goal: discover λ₃ = third successive non-degenerate minimum.

Setup (type 1,1,2 = most common ω*=4 case):
  Pa={p}, Pb={q}, Pc={r,s} with p<q<r<s, p+q+rs-form.
  Constraint: φ_p + φ_q = φ_r + φ_s  (integer sum, universal divisibility)
  Norm: max(p|φ_p|, q|φ_q|, r|φ_r|, s|φ_s|)
  Non-degenerate: W = b*Σ_{Pa} φ_p/p - a*Σ_{Pb} φ_p/p ≠ 0  i.e. φ_q - φ_p ≠ 0 for type (1,1,2)
  λ₁ = nd = p₂ = q (from E_n / F36)
  λ₂ = min(2q, r) (from F36)
  λ₃ = ?

Candidate formulas (Minkowski-inspired, working upward from λ₂):
  C1 = 3q          (triple the nd-minimizer)
  C2 = q + r       (nd + p₃)
  C3 = 2r          (double p₃)
  C4 = s           (p₄ itself)
  C5 = 2q + r      (mixed)
  Formula: min(C1, C2, C3, C4) restricted to those > λ₂
"""

import math
from sympy import isprime
from collections import defaultdict


def squarefree_omega4_triples(max_val=300):
    """Generate coprime (a,b,c) with a+b=c, all squarefree, ω*=4 distinct primes."""
    from sympy import factorint
    triples = []
    for a in range(1, max_val):
        for b in range(a, max_val):
            c = a + b
            if c > max_val:
                break
            if math.gcd(a, b) != 1:
                continue
            abc = a * b * c
            fac = factorint(abc)
            primes = sorted(fac.keys())
            # All squarefree?
            if any(v > 1 for v in fac.values()):
                continue
            if len(primes) != 4:
                continue
            triples.append((a, b, c, primes))
    return triples


def classify_groups(a, b, c, primes):
    """Return (Pa, Pb, Pc) as sorted prime lists."""
    from sympy import factorint
    def primes_of(n):
        return sorted(factorint(n).keys())
    Pa = primes_of(a) if a > 1 else []
    Pb = primes_of(b) if b > 1 else []
    Pc = primes_of(c) if c > 1 else []
    return Pa, Pb, Pc


def brute_minima(Pa, Pb, Pc, bound=20):
    """Brute-force first 3 non-degenerate successive minima for squarefree groups."""
    all_primes = Pa + Pb + Pc
    n = len(all_primes)
    # Index: Pa primes first, then Pb, then Pc
    # Constraint: sum_{Pa} φ_p + sum_{Pb} φ_p = sum_{Pc} φ_p  (universal divisibility, squarefree)
    # Non-degeneracy: W = b*sum_{Pa}(φ_p) - a*sum_{Pb}(φ_p) ≠ 0
    # But we don't have a,b here — use the lattice structure directly.
    # For squarefree type (|Pa|,|Pb|,|Pc|): non-degeneracy = at least one of φ_Pa ≠ -φ_Pb sum
    # Actually: W ∝ sum_Pa φ_p - sum_Pb φ_p in ψ coords after universal div.
    # Let's define non-deg: (sum Pa φ) ≠ (sum Pb φ) ... this is W/ab.
    # More precisely for constraint sum_Pa + sum_Pb = sum_Pc:
    # W = 0 iff sum_Pa φ = sum_Pb φ (W = ab*(sum_Pa - sum_Pb)/something).
    # Use: non-degenerate iff NOT (φ_Pa_sum == φ_Pb_sum).
    # This matches F(a,b) definition from OB-09/OB-10.

    norms = []
    ranges = [range(-bound, bound+1)] * n

    import itertools
    for vals in itertools.product(*ranges):
        if all(v == 0 for v in vals):
            continue
        phi = list(vals)
        na = len(Pa); nb = len(Pb); nc = len(Pc)
        phi_pa = phi[:na]
        phi_pb = phi[na:na+nb]
        phi_pc = phi[na+nb:]

        # Constraint: sum_Pa φ + sum_Pb φ = sum_Pc φ
        if sum(phi_pa) + sum(phi_pb) != sum(phi_pc):
            continue

        # Non-degeneracy: sum_Pa φ ≠ sum_Pb φ
        if sum(phi_pa) == sum(phi_pb):
            continue

        norm = max(p * abs(v) for p, v in zip(all_primes, phi))
        if norm > 0:
            norms.append(norm)

    if not norms:
        return []
    unique = sorted(set(norms))
    return unique[:5]  # first 5 distinct values


def formula_lambda3(p1, p2, p3, p4, lam2):
    """Candidate λ₃ formula."""
    c1 = 3 * p2
    c2 = p2 + p3
    c3 = 2 * p3
    c4 = p4
    candidates = [c for c in [c1, c2, c3, c4] if c > lam2]
    if not candidates:
        return None
    return min(candidates)


print("T93: λ₃ discovery for squarefree ω*=4 triples")
print("Generating triples...")
triples = squarefree_omega4_triples(max_val=200)
print(f"Found {len(triples)} squarefree ω*=4 coprime triples with c≤200")
print()

results = []
fail_nd = 0
fail_l2 = 0
fail_l3 = 0
formula_hits = defaultdict(int)

for (a, b, c, primes) in triples[:200]:  # cap for speed
    Pa, Pb, Pc = classify_groups(a, b, c, primes)
    p1, p2, p3, p4 = primes  # sorted

    # Theoretical λ₁ and λ₂
    lam1_theory = p2
    lam2_theory = min(2*p2, p3)

    minima = brute_minima(Pa, Pb, Pc, bound=8)
    if len(minima) < 3:
        continue

    lam1_b, lam2_b, lam3_b = minima[0], minima[1], minima[2]

    if lam1_b != lam1_theory:
        fail_nd += 1
        print(f"  ND-FAIL ({a},{b},{c}) primes={primes}: theory={lam1_theory} brute={lam1_b}")
        continue
    if lam2_b != lam2_theory:
        fail_l2 += 1
        print(f"  L2-FAIL ({a},{b},{c}) primes={primes}: theory={lam2_theory} brute={lam2_b}")
        continue

    lam3_formula = formula_lambda3(p1, p2, p3, p4, lam2_b)

    if lam3_formula == lam3_b:
        formula_hits["MATCH"] += 1
    else:
        fail_l3 += 1
        # Diagnose: which branch wins?
        c1, c2, c3, c4 = 3*p2, p2+p3, 2*p3, p4
        print(f"  L3-MISS ({a},{b},{c}) primes={primes} λ₂={lam2_b} brute_λ₃={lam3_b}")
        print(f"    3p₂={c1} p₂+p₃={c2} 2p₃={c3} p₄={c4} → formula={lam3_formula}")

    results.append((a, b, c, primes, lam1_b, lam2_b, lam3_b, lam3_formula))

print(f"\nnd failures: {fail_nd}")
print(f"λ₂ failures: {fail_l2}")
print(f"λ₃ MATCH: {formula_hits['MATCH']}")
print(f"λ₃ MISS: {fail_l3}")
print(f"Usable: {len(results)}")
print()

# Analyze which candidate wins for λ₃
print("=== λ₃ winner analysis ===")
winner_stats = defaultdict(int)
for (a, b, c, primes, l1, l2, l3, lf) in results:
    p1, p2, p3, p4 = primes
    c1, c2, c3, c4 = 3*p2, p2+p3, 2*p3, p4
    above_l2 = {k: v for k, v in [("3p2",c1),("p2+p3",c2),("2p3",c3),("p4",c4)] if v > l2}
    winner = min(above_l2, key=lambda k: above_l2[k]) if above_l2 else "none"
    winner_stats[winner] += 1

for w, cnt in sorted(winner_stats.items(), key=lambda x: -x[1]):
    print(f"  {w}: {cnt}")

print()
print("=== Sample table (first 20) ===")
print(f"{'triple':18s} {'primes':16s} {'λ₁':>5} {'λ₂':>5} {'λ₃_b':>7} {'λ₃_f':>7} {'ok':>3}")
for (a, b, c, primes, l1, l2, l3, lf) in results[:20]:
    ok = "✓" if l3 == lf else "✗"
    print(f"({a},{b},{c}){'':<7} {str(primes):<16} {l1:>5} {l2:>5} {l3:>7} {str(lf):>7} {ok:>3}")

# Additional: check if a refined formula fixes misses
if fail_l3 > 0:
    print("\n=== Diagnosing λ₃ misses — extended candidates ===")
    for (a, b, c, primes, l1, l2, l3, lf) in results:
        if l3 != lf:
            p1, p2, p3, p4 = primes
            # Extended: also check p2+p4, 2p2+p3, etc.
            ext = {"3p2": 3*p2, "p2+p3": p2+p3, "2p3": 2*p3, "p4": p4,
                   "p2+p4": p2+p4, "2p2+p3": 2*p2+p3, "p3+p4": p3+p4}
            above = {k: v for k, v in ext.items() if v > l2}
            best = min(above, key=lambda k: above[k]) if above else "?"
            print(f"  ({a},{b},{c}) primes={primes} λ₂={l2} brute_λ₃={l3} best_ext={best}={above.get(best,'?')}")
