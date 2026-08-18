"""
T65 — OB-13B tightness analysis: nd vs v_max * R^{1/(omega-1)} for high-quality triples

Uses the exact nd computation from T64 (lattice SVP via LLL reduction).
Scans all coprime triples a+b=c with c <= C_MAX and quality > QUALITY_MIN.
Reports: nd, bound_B = v_max * R^{1/(omega-1)}, ratio = nd / bound_B.

Goal: assess whether OB-13B is tight, or whether a smaller constant works.
Also: find the triple with the LARGEST ratio nd/bound_B (nearest to OB-13B equality).
"""

import math
from itertools import product as iproduct


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def rad(n):
    f = factorize(n)
    return math.prod(f.keys()) if f else 1


def quality(a, b):
    c = a + b
    R = rad(a * b * c)
    return math.log(c) / math.log(R) if R > 1 else 0


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def lattice_basis_from_constraint(alpha):
    n = len(alpha)
    U = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    a_work = list(alpha)
    for col in range(1, n):
        if a_work[col] == 0:
            continue
        g, x, y = extended_gcd(a_work[0], a_work[col])
        p_coeff = a_work[col] // g
        q_coeff = a_work[0] // g
        new_U_col0 = [x * U[row][0] + y * U[row][col] for row in range(n)]
        new_U_col = [-p_coeff * U[row][0] + q_coeff * U[row][col] for row in range(n)]
        for row in range(n):
            U[row][0] = new_U_col0[row]
            U[row][col] = new_U_col[row]
        a_work[0] = g
        a_work[col] = 0
    return [[U[row][col] for row in range(n)] for col in range(1, n)]


def lll_reduce(basis, primes, delta=0.75):
    n_vecs = len(basis)
    n_dim = len(basis[0])
    B = [list(v) for v in basis]

    def dot(u, v):
        return sum(primes[i] ** 2 * u[i] * v[i] for i in range(n_dim))

    def gram_schmidt_full(vecs):
        gs = []
        mu_mat = [[0.0] * len(vecs) for _ in range(len(vecs))]
        for i, v in enumerate(vecs):
            u = list(v)
            for j in range(i):
                denom = dot(gs[j], gs[j])
                mu_mat[i][j] = dot(v, gs[j]) / denom if denom > 1e-12 else 0
                u = [u[k] - mu_mat[i][j] * gs[j][k] for k in range(n_dim)]
            gs.append(u)
        return gs, mu_mat

    k = 1
    for _ in range(300):
        if k >= n_vecs:
            break
        gs, mu_mat = gram_schmidt_full(B)
        for j in range(k - 1, -1, -1):
            mu = mu_mat[k][j]
            if abs(mu) > 0.5:
                m = round(mu)
                B[k] = [B[k][i] - m * B[j][i] for i in range(n_dim)]
                gs, mu_mat = gram_schmidt_full(B)
        gs, mu_mat = gram_schmidt_full(B)

        def norm2(v):
            return dot(v, v)

        lhs = norm2(gs[k])
        rhs = (delta - mu_mat[k][k - 1] ** 2) * norm2(gs[k - 1])
        if lhs >= rhs:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            k = max(k - 1, 1)
    return B


def nd_svp(a, b, search_radius=20):
    c = a + b
    fa, fb, fc = factorize(a), factorize(b), factorize(c)
    primes = sorted(set(list(fa.keys()) + list(fb.keys()) + list(fc.keys())))
    n = len(primes)
    if n < 2:
        return None
    alpha = []
    for p in primes:
        if p in fa:
            alpha.append(fa[p])
        elif p in fb:
            alpha.append(fb[p])
        else:
            alpha.append(-fc[p])
    w_signs = []
    for p in primes:
        if p in fb:
            w_signs.append(1)
        elif p in fa:
            w_signs.append(-1)
        else:
            w_signs.append(0)
    basis = lattice_basis_from_constraint(alpha)
    rank = len(basis)
    basis_red = lll_reduce(basis, primes)
    best = float("inf")
    for coords in iproduct(range(-search_radius, search_radius + 1), repeat=rank):
        if all(c_k == 0 for c_k in coords):
            continue
        phi = [0] * n
        for k, c_k in enumerate(coords):
            for i in range(n):
                phi[i] += c_k * basis_red[k][i]
        if sum(alpha[i] * phi[i] for i in range(n)) != 0:
            continue
        W = sum(w_signs[i] * phi[i] for i in range(n))
        if W == 0:
            continue
        norm = max(primes[i] * abs(phi[i]) for i in range(n))
        if norm > 0:
            best = min(best, norm)
    return best if best < float("inf") else None


# ── Enumerate high-quality triples ───────────────────────────────────────────
C_MAX = 5000
QUALITY_MIN = 1.15

print(
    f"T65: OB-13B tightness — high-quality triples (quality > {QUALITY_MIN}, c <= {C_MAX})"
)
print("=" * 105)
print(
    f"{'(a,b,c)':<22} {'omega':>5} {'sq':>3} {'qual':>6} {'v_max':>6} {'R':>6} "
    f"{'nd':>5} {'bound_B':>9} {'ratio':>7}"
)
print("-" * 105)

results = []
for c in range(3, C_MAX + 1):
    fc = factorize(c)
    for a in range(1, c // 2 + 1):
        b = c - a
        if b <= 0 or math.gcd(a, b) != 1:
            continue
        # Quick quality check
        R = rad(a * b * c)
        if R == 0:
            continue
        qual = math.log(c) / math.log(R) if R > 1 else 0
        if qual <= QUALITY_MIN:
            continue

        fa = factorize(a)
        fb = factorize(b)
        primes = set(list(fa.keys()) + list(fb.keys()) + list(fc.keys()))
        omega = len(primes)
        if omega < 2 or omega > 6:
            continue

        v_max = max(
            [
                max(fa.values()) if fa else 0,
                max(fb.values()) if fb else 0,
                max(fc.values()) if fc else 0,
            ]
        )
        bound_b = v_max * (R ** (1.0 / (omega - 1)))

        nd = nd_svp(a, b, search_radius=15)
        if nd is None:
            continue

        ratio = nd / bound_b if bound_b > 0 else 0
        sq = all(v == 1 for d in [fa, fb, fc] for v in d.values())

        results.append((a, b, c, omega, sq, qual, v_max, R, nd, bound_b, ratio))

# Sort by ratio descending (tightest = closest to 1)
results.sort(key=lambda x: -x[10])

for a, b, c, omega, sq, qual, v_max, R, nd, bound_b, ratio in results[:40]:
    sq_str = "Y" if sq else "N"
    print(
        f"  ({a},{b},{c}){'':<10} {omega:>5} {sq_str:>3} {qual:>6.3f} {v_max:>6} "
        f"{R:>6} {nd:>5} {bound_b:>9.3f} {ratio:>7.4f}"
    )

print()
print("=" * 105)
print(f"Total high-quality triples found: {len(results)}")
if results:
    max_ratio = max(r[10] for r in results)
    mean_ratio = sum(r[10] for r in results) / len(results)
    print(f"Max ratio nd/bound_B: {max_ratio:.4f}  (nearest to OB-13B equality)")
    print(f"Mean ratio nd/bound_B: {mean_ratio:.4f}")
    non_sq = [r for r in results if not r[4]]
    if non_sq:
        print(
            f"Non-squarefree: {len(non_sq)} triples, max ratio {max(r[10] for r in non_sq):.4f}"
        )
    sq_only = [r for r in results if r[4]]
    if sq_only:
        print(
            f"Squarefree: {len(sq_only)} triples, max ratio {max(r[10] for r in sq_only):.4f}"
        )

print()
print("ANALYSIS:")
print("  OB-13B bound: nd(a,b) <= v_max * R^{1/(omega-1)}")
print("  ratio = nd / (v_max * R^{1/(omega-1)}); max ratio is the tightest case.")
print("  If max ratio << 1 for all tested triples, OB-13B has significant slack.")
