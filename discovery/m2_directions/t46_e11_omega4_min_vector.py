"""
T46 — E11 候选：ω=4 Pasten 格最小非退化向量的显式刻画

E10（ω=3）结论：最小非退化向量为 v=(p,-q,0)，范数=q，Wronskian=-2pq≠0。

本脚本探索 ω=4 类型 (1,1,2) 的情形：
  a=p, b=q, c=r1*r2  (p<q<r1<r2, 均为素数，a+b=c)

Pasten 格约束（标准形式）：
  sum_{prime l | a or b} ψ_l - sum_{prime l | c} ψ_l = 0
即：
  ψ_p + ψ_q - ψ_{r1} - ψ_{r2} = 0

非退化条件（Wronskian ≠ 0）对 ω=4 更复杂，以分量组合表示。

问题：在满足约束的非零整数向量中，无穷范数最小的是哪个？
     它的范数是多少（与 F10 预测 nd=min(p,q)=p 的关系）？
"""

import math

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def wronskian_omega4(p, q, r1, r2, psi):
    """
    对 ω=4 类型 (1,1,2)，Wronskian 定义为 Pa={p}, Pb={q}, Pc={r1,r2}。
    W(ψ) = p*ψ_q - q*ψ_p (按 Pasten 2024, 仅看 a,b 部分)
    非退化 ↔ W ≠ 0。
    """
    return p * psi[1] - q * psi[0]

def in_lattice_omega4(psi):
    """约束: ψ_p + ψ_q - ψ_r1 - ψ_r2 = 0"""
    return psi[0] + psi[1] - psi[2] - psi[3] == 0

def linf(psi):
    return max(abs(x) for x in psi)

def find_min_vector(p, q, r1, r2, search_bound):
    """暴力搜索最小范数向量（受限搜索空间）。"""
    best_norm = float('inf')
    best_vec = None
    best_nondeg = False

    # ψ_r2 = ψ_p + ψ_q - ψ_r1（由约束确定）
    for ap in range(-search_bound, search_bound+1):
        for aq in range(-search_bound, search_bound+1):
            for ar1 in range(-search_bound, search_bound+1):
                ar2 = ap + aq - ar1
                if abs(ar2) > search_bound:
                    continue
                if ap == 0 and aq == 0 and ar1 == 0 and ar2 == 0:
                    continue
                vec = (ap, aq, ar1, ar2)
                n = linf(vec)
                w = wronskian_omega4(p, q, r1, r2, vec)
                is_nd = (w != 0)

                if n < best_norm or (n == best_norm and is_nd and not best_nondeg):
                    best_norm = n
                    best_vec = vec
                    best_nondeg = is_nd
    return best_norm, best_vec, best_nondeg

def find_min_nondeg_vector(p, q, r1, r2, search_bound):
    """搜索最小范数的非退化向量。"""
    best_norm = float('inf')
    best_vec = None

    for ap in range(-search_bound, search_bound+1):
        for aq in range(-search_bound, search_bound+1):
            for ar1 in range(-search_bound, search_bound+1):
                ar2 = ap + aq - ar1
                if abs(ar2) > search_bound:
                    continue
                if ap == 0 and aq == 0 and ar1 == 0 and ar2 == 0:
                    continue
                vec = (ap, aq, ar1, ar2)
                w = wronskian_omega4(p, q, r1, r2, vec)
                if w == 0:
                    continue  # 退化，跳过
                n = linf(vec)
                if n < best_norm:
                    best_norm = n
                    best_vec = vec
    return best_norm, best_vec

print("T46: ω=4 类型 (1,1,2) Pasten 格最小非退化向量")
print("约束: ψ_p + ψ_q = ψ_r1 + ψ_r2")
print("="*70)

# 收集 ω=4 类型 (1,1,2) 三元组
triples = []
primes = [x for x in range(2, 200) if is_prime(x)]
for i, p in enumerate(primes):
    for j, q in enumerate(primes):
        if q <= p: continue
        c = p + q
        # c 必须是两个素数之积（squarefree 且 ω(c)=2）
        for k, r1 in enumerate(primes):
            if r1 <= q: continue
            if c % r1 != 0: continue
            r2 = c // r1
            if r2 <= r1: continue
            if not is_prime(r2): continue
            if r2 * r1 != c: continue
            triples.append((p, q, r1, r2, c))
        if len(triples) >= 20:
            break
    if len(triples) >= 20:
        break

print(f"\n分析前 {len(triples)} 个三元组：\n")
print(f"{'(p,q,r1,r2)':30}  {'F10 nd':>6}  {'min_nondeg_norm':>15}  {'min_vec':>25}  {'Wronskian':>10}")

candidate_norms = []
for (p, q, r1, r2, c) in triples[:15]:
    # F10 预测：nd = second_smallest{min(Pa), min(Pb), min(Pc)} = second_smallest{p, q, r1}
    group_mins = sorted([p, q, r1])
    nd_f10 = group_mins[1]  # 第二小

    bound = max(r1, r2) + 5
    norm, vec = find_min_nondeg_vector(p, q, r1, r2, min(bound, 30))
    w = wronskian_omega4(p, q, r1, r2, vec) if vec else None

    match = "✓" if norm == nd_f10 else f"≠{nd_f10}"
    print(f"({p:2},{q:2},{r1:2},{r2:3})  a={p}+b={q}  nd={nd_f10:4d}  "
          f"min_nd_norm={norm:4d} {match:5}  vec={str(vec):25}  W={w}")
    candidate_norms.append((norm, nd_f10, p, q, r1, r2, vec, w))

print()
# 分析候选向量的模式
print("="*70)
print("模式分析：最小非退化向量的结构\n")

# 按类型分析
for norm, nd_f10, p, q, r1, r2, vec, w in candidate_norms[:10]:
    ap, aq, ar1, ar2 = vec
    print(f"({p},{q},{r1},{r2}): vec=({ap},{aq},{ar1},{ar2}), norm={norm}, W={w}")
    # 尝试识别模式
    if ar1 == 0:
        print(f"  → ar1=0: (ψ_p, ψ_q, 0, ψ_r2) 结构，ψ_r2=ψ_p+ψ_q")
    elif ar2 == 0:
        print(f"  → ar2=0: (ψ_p, ψ_q, ψ_r1, 0) 结构，ψ_r1=ψ_p+ψ_q")
    elif ap == 0:
        print(f"  → ap=0: (0, ψ_q, ψ_r1, ψ_r2) 结构")
    elif aq == 0:
        print(f"  → aq=0: (ψ_p, 0, ψ_r1, ψ_r2) 结构")

print()
print("="*70)
print("关键候选：v = (p, -q, r2, -r1) 是否总在格中并非退化？")
print()
for norm, nd_f10, p, q, r1, r2, vec, w in candidate_norms[:10]:
    # 测试候选向量族
    # v1 = (1, -1, 1, -1)：约束 1-1-1+1=0 ✓ 范数=1 但 Wronskian?
    # v2 = (p, -q, 0, r2-r1) 等变体
    # 显式候选：ar2=0 → ψ_r1=ψ_p+ψ_q：尝试 (1, -1, 0, 0) * gcd
    v_cand = (1, -1, 0, 0)
    # 约束: 1 + (-1) - 0 - 0 = 0 ✓
    w_cand = wronskian_omega4(p, q, r1, r2, v_cand)
    # 范数=1，但 Wronskian = p*(-1) - q*(1) = -p-q = -(p+q) = -c ≠ 0 ✓
    check = "✓ 非退化" if w_cand != 0 else "退化!"
    print(f"  ({p},{q},{r1},{r2}): v=(1,-1,0,0) 在 L 中, 范数=1, W={w_cand} {check}")

print()
print("结论：")
print("  向量 v=(1,-1,0,0) 满足约束 1-1-0-0=0 ✓")
print("  Wronskian W(v) = p*(-1) - q*(1) = -(p+q) = -c ≠ 0 ✓（因为 c = p+q > 0）")
print("  范数 = max(1,1,0,0) = 1")
print()
print("  若 v=(1,-1,0,0) 的范数=1 是最小非退化范数，则 nd=1 而非 F10 预测的 min(p,q)!")
print("  这意味着 F10 公式可能只适用于 ω=3，或需要对 ω>3 作修正！")
