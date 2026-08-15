"""
T46b — E11：ω=4 类型(1,1,2) Pasten 格最小非退化向量

正确的 Pasten 格（φ坐标 φ_l=ψ_l/l∈Z，F8保证）：
  约束：φ_p + φ_q = φ_r1 + φ_r2

最小非退化向量（理论预测）：
  φ=(1,-1,0,0) → ψ=(p,-q,0,0)，范数=q，Wronskian=p(-q)-q(p)=-2pq≠0

证明：
  1. 非退化 ↔ φ_q≠φ_p（Wronskian=pq(φ_q-φ_p)≠0）
  2. 若φ_r1=φ_r2=0：约束给 φ_p=-φ_q，φ_q≠φ_p → φ_q≠-φ_q → φ_q≠0
     最小|φ_q|=1，给ψ=(p,-q,0,0)，范数=max(p,q)=q
  3. 若φ_r1≠0或φ_r2≠0：范数≥min(r1,r2)=r1>q（因p<q<r1<r2）
  → 全局最小非退化范数=q，与F10一致
"""

import math

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def in_lattice_phi(phi):
    """φ坐标约束: φ_p + φ_q = φ_r1 + φ_r2"""
    return phi[0] + phi[1] == phi[2] + phi[3]

def wronskian_phi(phi):
    """W = pq*(φ_q - φ_p) 的符号部分，即 (φ_q - φ_p)"""
    return phi[1] - phi[0]  # W≠0 ↔ φ_q≠φ_p

def psi_norm(p, q, r1, r2, phi):
    """ψ范数: max(p|φ_p|, q|φ_q|, r1|φ_r1|, r2|φ_r2|)"""
    return max(p*abs(phi[0]), q*abs(phi[1]), r1*abs(phi[2]), r2*abs(phi[3]))

def find_min_nondeg_phi(p, q, r1, r2, bound=5):
    """搜索最小范数非退化向量（φ坐标）"""
    best = float('inf')
    best_phi = None
    for fp in range(-bound, bound+1):
        for fq in range(-bound, bound+1):
            for fr1 in range(-bound, bound+1):
                fr2 = fp + fq - fr1  # 由约束决定
                if abs(fr2) > bound: continue
                phi = (fp, fq, fr1, fr2)
                if fp == fq == fr1 == fr2 == 0: continue
                if wronskian_phi(phi) == 0: continue  # 退化
                n = psi_norm(p, q, r1, r2, phi)
                if n < best:
                    best = n
                    best_phi = phi
    return best, best_phi

print("T46b: ω=4 类型(1,1,2) Pasten格最小非退化向量验证")
print("="*70)

# 生成 ω=4 类型(1,1,2) 三元组
triples = []
primes = [x for x in range(2, 300) if is_prime(x)]
prime_set = set(primes)

for i, p in enumerate(primes[:30]):
    for j, q in enumerate(primes):
        if q <= p: continue
        c = p + q
        # c = r1*r2, squarefree, r1 < r2, both prime, r1 > q
        for k, r1 in enumerate(primes):
            if r1 <= q: continue
            if c % r1 != 0: continue
            r2 = c // r1
            if r2 <= r1: continue
            if r2 not in prime_set: continue
            triples.append((p, q, r1, r2))
            if len(triples) >= 30:
                break
        if len(triples) >= 30:
            break
    if len(triples) >= 30:
        break

print(f"找到 {len(triples)} 个三元组\n")
print(f"{'(p,q,r1,r2)':25}  {'F10 nd':>6}  {'暴力最小':>8}  {'预测ψ=(p,-q,0,0)':>20}  {'匹配':>6}")
print("-"*80)

all_match = True
for p, q, r1, r2 in triples[:20]:
    # F10预测: nd = second_smallest{min(Pa)=p, min(Pb)=q, min(Pc)=r1} = q（因p<q<r1）
    nd_f10 = q

    # 预测向量 φ=(1,-1,0,0), ψ=(p,-q,0,0), 范数=q
    phi_pred = (1, -1, 0, 0)
    assert in_lattice_phi(phi_pred)
    assert wronskian_phi(phi_pred) != 0
    norm_pred = psi_norm(p, q, r1, r2, phi_pred)
    assert norm_pred == q

    # 暴力搜索最小非退化范数
    bound = min(r2 + 2, 15)
    best_norm, best_phi = find_min_nondeg_phi(p, q, r1, r2, bound)

    match = "✓" if best_norm == q else f"✗ 实际={best_norm}"
    if best_norm != q:
        all_match = False

    print(f"({p:2},{q:3},{r1:3},{r2:4})  nd={nd_f10:4d}  "
          f"暴力={best_norm:4d}  ψ=({p},-{q},0,0)范数={norm_pred}  {match}")

print()
print("="*70)
if all_match:
    print("✓ 全部匹配：最小非退化范数=q=F10预测")
    print()
    print("E11 定理（ω=4, 类型(1,1,2)）：")
    print("  设 a=p, b=q, c=r1*r2（p<q<r1<r2 均为素数，p+q=r1*r2）")
    print("  则 Pasten 格的最小非退化向量为 ψ=(p,-q,0,0)")
    print("  范数 ‖ψ‖_∞ = q = F10公式的 nd 值")
    print("  Wronskian W = -2pq ≠ 0")
    print()
    print("证明骨架：")
    print("  (1) ψ=(p,-q,0,0) 在格中：φ=(1,-1,0,0), 1+(-1)=0+0 ✓")
    print("  (2) 非退化：φ_q-φ_p = -1-1 = -2 ≠ 0 ✓")
    print("  (3) 最小性：")
    print("      若φ_r1=φ_r2=0：约束 → φ_p=-φ_q，非退化 → φ_q≠0，min‖ψ‖=q")
    print("      若φ_r1≠0或φ_r2≠0：‖ψ‖≥r1>q（因r1>q）")
    print("      → 全局最小 = q QED")
else:
    print("✗ 存在不匹配！需要进一步分析")

print()
print("="*70)
print("与 E10 (ω=3) 比较：")
print("  E10: ψ=(p,-q,0)，范数=q，Wronskian=-2pq（r-坐标为0）")
print("  E11: ψ=(p,-q,0,0)，范数=q，Wronskian=-2pq（两个r-坐标均为0）")
print("  结构完全相同！说明 F8 的 φ-坐标简化给出了统一的最小向量结构。")
print()
print("推广猜想 E_n（ω=n+2，类型(1,1,n)）：")
print("  最小非退化向量为 ψ=(p,-q,0,...,0)（n个零），范数=q")
