"""Search for edge-case triples: a=1, equal-val Pb with BOTH smallest primes in Pb."""

from sympy import factorint


def rad(n):
    return 1 if n == 1 else int(__import__("math").prod(factorint(n)))


def squarefree_with_k_factors(min_primes=2, max_val=200):
    """Generate squarefree M with >= min_primes prime factors, M <= max_val."""
    results = []
    for M in range(6, max_val + 1):
        f = factorint(M)
        if all(e == 1 for e in f.values()) and len(f) >= min_primes:
            results.append(M)
    return results


def analyze_triple(a, b, c):
    """Return (pa, pb, pc, vmax, R, omega) for triple (a,b,c)."""
    fa = factorint(a) if a > 1 else {}
    fb = factorint(b)
    fc = factorint(c)
    Pa = set(fa.keys())
    Pb = set(fb.keys())
    Pc = set(fc.keys())
    assert Pa.isdisjoint(Pb) and Pa.isdisjoint(Pc) and Pb.isdisjoint(Pc)
    P = Pa | Pb | Pc
    omega = len(P)
    vmax = max(
        max((fa.get(p, 0) for p in P), default=0),
        max((fb.get(p, 0) for p in P), default=0),
        max((fc.get(p, 0) for p in P), default=0),
    )
    R = 1
    for p in P:
        R *= p
    return fa, fb, fc, Pa, Pb, Pc, vmax, R, omega


def check_ob15_pb_pc(a, b, c, Pa, Pb, Pc, fb, fc, vmax, R, omega):
    """Try Pb-Pc construction: pick p_min in Pb, q_min in Pc."""
    if not Pb or not Pc:
        return None
    p_min = min(Pb)
    q_min = min(Pc)
    vp = fb[p_min]
    vq = fc[q_min]
    from math import gcd

    g = gcd(vp, vq)
    phi_p = vq // g
    phi_q = vp // g
    W = phi_p  # since a=1, Pa=empty, W = sum_Pb phi_p = phi_p (others 0)
    norm = max(p_min * phi_p, q_min * phi_q)
    bound = vmax * R ** (1 / (omega - 1))
    return norm, bound, norm <= bound, W


def main():
    print("=== Edge-case search: a=1, equal-val Pb, both pi_1,pi_2 in Pb ===")
    print("(i.e., all Pb primes < all Pc primes)")
    print()

    squarefrees = squarefree_with_k_factors(min_primes=2, max_val=100)
    edge_cases = []
    max_v = 50

    for M in squarefrees:
        fm = factorint(M)
        pb_primes = sorted(fm.keys())
        max_pb = max(pb_primes)

        for v in range(3, max_v + 1):
            b = M**v
            c = 1 + b
            if c > 10**12:
                break

            fc = factorint(c)
            pc_primes = sorted(fc.keys())

            # Equal-val Pb check: all primes of b have val v
            # (trivially true since b = M^v and M squarefree)

            # Check: all Pb primes < all Pc primes (edge case condition)
            if not pc_primes:
                continue
            min_pc = min(pc_primes)
            if max_pb >= min_pc:
                continue  # Not the edge case: some Pb prime >= some Pc prime

            # Check R < c
            R = M * rad(c)
            if R >= c:
                continue

            # Found an edge-case triple!
            omega = len(pb_primes) + len(pc_primes)
            vmax = v  # from b = M^v

            # Check v_max could be larger from c
            for p, e in fc.items():
                if e > vmax:
                    vmax = e

            bound = vmax * R ** (1 / (omega - 1))
            pi3 = min_pc  # smallest Pc prime

            # Pb-Pc construction
            p_min = pb_primes[0]
            q_min = pi3
            vp = v
            vq = fc[q_min]
            from math import gcd

            g = gcd(vp, vq)
            phi_p = vq // g
            phi_q = vp // g
            norm_ub = max(p_min * phi_p, q_min * phi_q)
            holds = norm_ub <= bound

            pi3_power_test = pi3 ** (omega - 1)
            pi3_le_R = pi3_power_test <= R

            edge_cases.append(
                {
                    "M": M,
                    "v": v,
                    "c": c,
                    "omega": omega,
                    "vmax": vmax,
                    "R": R,
                    "bound": round(bound, 2),
                    "pi3": pi3,
                    "pi3^(w-1)": pi3_power_test,
                    "R>=pi3^(w-1)": pi3_le_R,
                    "norm_ub": norm_ub,
                    "holds": holds,
                    "pb_primes": pb_primes,
                    "pc_primes": pc_primes,
                    "ratio": round(norm_ub / bound, 4),
                }
            )

    print(f"Found {len(edge_cases)} edge-case triples with c <= 10^12, v <= {max_v}")
    print()

    if edge_cases:
        print(
            f"{'M':>4} {'v':>3} {'pi3':>5} {'omega':>5} {'vmax':>5} {'R':>12} {'c':>14} "
            f"{'pi3^(w-1)':>12} {'R>=':>5} {'norm_ub':>8} {'bound':>8} {'OK':>4} {'ratio':>6}"
        )
        print("-" * 105)
        for e in edge_cases:
            print(
                f"{e['M']:>4} {e['v']:>3} {e['pi3']:>5} {e['omega']:>5} {e['vmax']:>5} "
                f"{e['R']:>12} {e['c']:>14} {e['pi3^(w-1)']:>12} {str(e['R>=pi3^(w-1)']):>5} "
                f"{e['norm_ub']:>8} {e['bound']:>8} {str(e['holds']):>4} {e['ratio']:>6}"
            )
        print()
        violations = [e for e in edge_cases if not e["holds"]]
        print(f"OB-15 violations: {len(violations)}")
        pi3_violations = [e for e in edge_cases if not e["R>=pi3^(w-1)"]]
        print(f"Cases with pi3^(omega-1) > R: {len(pi3_violations)}")
        if pi3_violations:
            print("  (these need alternative proof — Key Lemma fails for pi3):")
            for e in pi3_violations:
                print(
                    f"  M={e['M']}, v={e['v']}, pi3={e['pi3']}, pi3^(w-1)={e['pi3^(w-1)']}, R={e['R']}"
                )

        # Summarize pi3 values seen
        from collections import Counter

        pi3_counts = Counter(e["pi3"] for e in edge_cases)
        print(f"\npi3 distribution: {dict(sorted(pi3_counts.items()))}")

        # Show pb_primes and pc_primes for each
        print("\nDetailed examples:")
        for e in edge_cases[:20]:
            print(
                f"  (1, {e['M']}^{e['v']}, {e['c']}) Pb={e['pb_primes']} Pc={e['pc_primes'][:5]}"
                f" pi3={e['pi3']} R={e['R']} norm_ub={e['norm_ub']} bound={e['bound']}"
            )
    else:
        print("No edge-case triples found.")


if __name__ == "__main__":
    main()
