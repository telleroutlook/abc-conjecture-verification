"""
T46c — E11 正确版：ω=4 类型(1,1,2) Pasten 格最小非退化向量

修正：去除 r1>q 的错误要求。实际三元组（如 2+13=3×5）有 r1<q。

Pasten 格（φ坐标，F8 保证 φ_l=ψ_l/l ∈ Z）：
  约束：φ_p + φ_q = φ_r1 + φ_r2
  ψ 范数：max(p|φ_p|, q|φ_q|, r1|φ_r1|, r2|φ_r2|)
  非退化：W = pq(φ_q - φ_p) ≠ 0 ↔ φ_q ≠ φ_p

F10 预测：nd = second_smallest{ min(Pa), min(Pb), min(Pc) }
                = second_smallest{ p, q, r1 }（按大小排序后取第二小）

E11 猜想（修正版）：最小非退化向量使用 {p,q,r1,r2} 中最小的两个素数，
其余坐标设为零，范数 = 第二小素数 = F10 的 nd。
"""


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_min_nondeg_norm(p, q, r1, r2, bound=8):
    """暴力搜索最小非退化范数（φ坐标）"""
    best = float("inf")
    best_phi = None
    for fp in range(-bound, bound + 1):
        for fq in range(-bound, bound + 1):
            for fr1 in range(-bound, bound + 1):
                fr2 = fp + fq - fr1
                if abs(fr2) > bound:
                    continue
                phi = (fp, fq, fr1, fr2)
                if all(x == 0 for x in phi):
                    continue
                if fq == fp:
                    continue  # 退化（W=pq(fq-fp)=0）
                n = max(p * abs(fp), q * abs(fq), r1 * abs(fr1), r2 * abs(fr2))
                if n < best:
                    best = n
                    best_phi = phi
    return best, best_phi


# 生成 ω=4 类型(1,1,2) 三元组：a=p, b=q (p<q 素数), c=p+q=r1*r2 (r1<r2 素数)
primes = [x for x in range(2, 500) if is_prime(x)]
prime_set = set(primes)
triples = []

for p in primes[:25]:
    for q in primes:
        if q <= p:
            continue
        c = p + q
        # 找 c 的所有两素数分解
        for r1 in primes:
            if r1 >= c:
                break
            if c % r1 != 0:
                continue
            r2 = c // r1
            if r2 <= r1:
                continue
            if r2 not in prime_set:
                continue
            triples.append((p, q, r1, r2))

print(f"找到 {len(triples)} 个三元组\n")

# F10 预测和最小非退化向量分析
print(
    f"{'(p,q,r1,r2)':22}  {'4素数排序':18}  {'nd(F10)':>7}  {'暴力最小':>8}  {'最优φ':>18}  {'匹配'}"
)
print("-" * 100)

all_match = True
mismatches = []

for p, q, r1, r2 in triples[:30]:
    # 四个素数按大小排序
    sorted_primes = sorted([p, q, r1, r2])
    # F10: nd = second_smallest{min(Pa), min(Pb), min(Pc)}
    #      = second_smallest{p, q, r1} （min of each group）
    group_mins = sorted([p, q, r1])  # Pa={p}, Pb={q}, Pc={r1,r2} → min(Pc)=r1（r1<r2）
    nd_f10 = group_mins[1]  # 第二小

    # 暴力搜索
    best_norm, best_phi = find_min_nondeg_norm(p, q, r1, r2, bound=6)

    match = "✓" if best_norm == nd_f10 else f"✗ 实际={best_norm}"
    if best_norm != nd_f10:
        all_match = False
        mismatches.append((p, q, r1, r2, nd_f10, best_norm, best_phi))

    print(
        f"({p:2},{q:3},{r1:2},{r2:3})  "
        f"排序:{sorted_primes}  "
        f"nd={nd_f10:4d}  "
        f"暴力={best_norm:4d}  "
        f"φ={str(best_phi):18}  {match}"
    )

print()
print("=" * 100)
if all_match:
    print("✓ 全部匹配：最小非退化范数 = F10 的 nd")
else:
    print(f"✗ {len(mismatches)} 个不匹配：")
    for item in mismatches:
        print(f"  {item}")

print()
print("最优向量结构分析（前10个）：")
print("-" * 70)
for p, q, r1, r2 in triples[:10]:
    _, phi = find_min_nondeg_norm(p, q, r1, r2, bound=6)
    if phi is None:
        continue
    fp, fq, fr1, fr2 = phi
    # 识别哪两个坐标非零
    nonzero = []
    if fp != 0:
        nonzero.append(f"φ_p={fp}(→ψ_p={p * fp})")
    if fq != 0:
        nonzero.append(f"φ_q={fq}(→ψ_q={q * fq})")
    if fr1 != 0:
        nonzero.append(f"φ_r1={fr1}(→ψ_r1={r1 * fr1})")
    if fr2 != 0:
        nonzero.append(f"φ_r2={fr2}(→ψ_r2={r2 * fr2})")
    sorted4 = sorted([p, q, r1, r2])
    norm = max(p * abs(fp), q * abs(fq), r1 * abs(fr1), r2 * abs(fr2))
    print(f"  ({p},{q},{r1},{r2}): φ={phi}, 非零={nonzero}, 范数={norm}")
    print(
        f"    4素数升序:{sorted4}, 最小两个:{sorted4[:2]}, nd={sorted([p, q, r1])[1]}"
    )

print()
print("=" * 70)
print("E11 定理（修正版）：ω=4 类型(1,1,2)")
print()
print("设 a=p, b=q (p<q 素数), c=r1*r2 (r1<r2 素数), p+q=c。")
print("记 {l_1<l_2<l_3<l_4} = {p,q,r1,r2} 升序排列。")
print()
print("最小非退化向量：使用最小两个素数 l_1, l_2，另两个置零。")
print("具体：令两个非零 φ 坐标对应 l_1 和 l_2，满足约束和非退化条件。")
print("范数 = l_2 = second_smallest{p,q,r1,r2}.")
print()
print("注：F10 给出 nd = second_smallest{min(Pa), min(Pb), min(Pc)}")
print("   = second_smallest{p, q, r1}（三个组各取最小值）")
print("   但 l_2 = second_smallest{p,q,r1,r2} 可能不等于 second_smallest{p,q,r1}。")
print("   需要核查两者是否一致。")

# 检查是否一致
print()
print("一致性检查：")
diff_count = 0
for p, q, r1, r2 in triples[:30]:
    group_nd = sorted([p, q, r1])[1]  # F10: second_smallest of group mins
    all4_nd = sorted([p, q, r1, r2])[1]  # second_smallest of all 4 primes
    if group_nd != all4_nd:
        diff_count += 1
        print(f"  差异：({p},{q},{r1},{r2}): F10 nd={group_nd}, all4 nd={all4_nd}")
if diff_count == 0:
    print(f"  前{min(30, len(triples))}个三元组：F10 nd = all4 second_smallest ✓")
