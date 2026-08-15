# OB-02v2 独立 Gate-A 审稿报告

**审稿对象：** `OB-02v2-iut-corollary-312-pilot-compatibility.md`  
**对象 SHA-256：** `ffe55dee4bfee8487275eaf1608f8c3c1206b38c629405d7eaebc79a2adabd8f`  
**审稿日期：** 2026-08-15  
**审稿性质：** 独立核验；不补写作者证明，不预设 IUTT-III Corollary 3.12 成立

## 通用送审头（必附）

> 请对所附问题做独立审稿，而不是替作者完成或默认其结论成立。
>
> 1. 先核对精确陈述：逐一核对附件中定理、命题的精确陈述、所有量词、符号定义，以及“允许引用的前置结果”清单。凡作为前提使用的被引定理，须核对其作者、年份、精确定理编号，并确认其假设确实覆盖此处所用的对象，不能只凭名称或印象。
> 2. 逐步检查，不预设成立：对每一步给出独立判断。凡载荷性的等式、界、符号事实、数值锚点，用脚本或精确算术核验；发现与附件不符时，报告独立算得的精确值。
> 3. 非循环性红线：不得假设 RH、abc、Szpiro、其等价命题或待审结论；不得把 Corollary 3.12 本身改写成某个“indeterminacy range”后再作为前提。

## 1. 正式裁决

> **INCONCLUSIVE + LOCALIZATION**

该裁决严格采用附件 Acceptance criterion 4。OB-02v2 没有给出一个可判定真假的交换方图：底部箭头既无定义域/陪域的来源，也无箭头类别（集合映射、连续映射、实线性映射、序保持映射、商对象上的关系，或 correspondences）。更关键的是，附件的竖直“concrete embeddings”并非 IUTT-III Proposition 3.9 所定义的映射。

在所列文献中，可以定位到的最小缺口是：

1. IUTT-III Remark 3.9.5(vii), Observation 3-1 至 3-3 只说明需要取“合适的”正张量幂及作相应归一化，并把权重匹配细节留给读者；
2. 同一 Remark 的 Observation 9-2 明说到该阶段所得关系仍是非显式的；
3. Corollary 3.12 的证明步骤 (xi-d) 再次调用“合适的”正张量幂与“适当归一化”的 log-volume，才把对象送入可比较的实数量；
4. (xi-e) 只以 multiradial algorithm、SHE 和 prime-strip isomorphisms 的语言说输出与固定输入相关；
5. (xi-f) 从“或许只在某种近似意义下重构输入”跳到
   \[
   -|\log q|\in \mathbb R_{\le -|\log\Theta|},
   \]
   但没有展示一个在 log-volume 上定义、兼容商去 Ind1–Ind3、并保持所需次序的比较映射。

因此，目前不能从附件或其列出的允许来源构造机器可检查的证明；也不能给出附件所要求的 **CONFIRMED-OBSTRUCTION**，因为数值锚点 37.a1 不是一组完整的 IUTT-admissible initial Θ-data，而且 Ind1–Ind3 在附件中没有被定义为可数值穷举或排除的作用范围。

本裁决不认证 verification-kernel obligation `core3.iut-corollary-312-independently-verified`。

## 2. 版本与引用闭包审计

### 2.1 已核对的一手来源

| 来源 | 已核对位置 | 与附件的关系 |
|---|---|---|
| Shinichi Mochizuki, *Inter-universal Teichmüller Theory I: Construction of Hodge Theaters*, PRIMS 57 (2021), 3–207, DOI 10.4171/PRIMS/57-1-1 | Definition 3.1；Example 3.2(iv) | 核对 initial Θ-data 与 \(q_v\)、\(\underline q_v\) 的区别 |
| Shinichi Mochizuki, *Inter-universal Teichmüller Theory III: Canonical Splittings of the Log-Theta-Lattice*, PRIMS 57 (2021), 403–626, DOI 10.4171/PRIMS/57-1-3 | Definition 3.8；Proposition 3.9；Remark 3.9.5(vii)；Theorem 3.11；Corollary 3.12 及证明 (xi-a)–(xi-f) | 核对 pilot、link、log-volume、Ind1–Ind3 和目标推理 |
| Peter Scholze and Jakob Stix, *Why abc is still a conjecture* (2018-08-23 version) | §§2.1.6–2.2 | 核对所谓 \(j^2\)-scaling concern 的原始陈述 |
| LMFDB, elliptic curve 37.a1 | 全局不变量与 \(p=37\) 的局部数据 | 核对数值锚点；不把数据库条目当作 initial Θ-data |

### 2.2 未满足的版本要求

附件称所引 PDF “must be verified against `baseline/` before citing”。交付目录中没有 `baseline/`，只有本附件。因此不能完成附件要求的逐字版本或哈希比对。本报告改用正式 PRIMS 文章页、作者 PDF 及 Scholze–Stix 的 2018-08-23 版本进行内容核对。这个替代足以发现下述陈述差异，但不等于完成附件自己的 baseline 要求。

### 2.3 前置结果清单不闭合

附件列出的来源只有 IUTT-I、IUTT-III 与 Scholze–Stix，却要求从 IUT 构造完整关闭 Corollary 3.12。(xi-a)–(xi-f) 及其邻近论证继续调用 IUTT-II、Earlier/later propositions 以及若干外部系列中的结果；附件没有逐项列出哪些结果允许作为公理、各自的精确版本及假设。故“所有定义 self-contained”与实际依赖不符。

这不是本裁决的唯一理由：即使暂时允许所有交叉引用，OB-02v2 所需的底部实比较映射仍没有在所核对位置出现。

## 3. D1–D7 精确陈述审计

| 项目 | 判断 | 独立核对结果 |
|---|---|---|
| D1 — Initial Θ-data | **不正确，且缺失实质假设** | IUTT-I Definition 3.1 的数据不是附件所写的六元组。原定义还含代数闭包/基域数据、模域、坏约化赋值集合、特定 cusp 等；并要求 \(\sqrt{-1}\in F\)、稳定约化、6-torsion 的有理性、mod-\(\ell\) 像含 \(\mathrm{SL}_2(\mathbf F_\ell)\)、\(\ell\) 与坏特征及 Tate 参数阶互素等。\(K\) 不是附件所称“次数 \(\le2\) 的子域”，末项也不是 \(F^\times\) 中用于固定 \(\ell\)-torsion trivialization 的元素。 |
| D2 — Pilot objects | **类型错误/过度简化** | IUTT-III Definition 3.8(i) 的 pilots 是 global realified Frobenioids 中由 splitting monoids 的生成元（至 torsion）确定的对象/集合；不是逐个坏素点的 \(F_v^\times\) 元素。IUTT 记号还使用 \(\underline q_v=q_v^{1/(2\ell)}\)（至 \(\mu_{2\ell}\)），附件将其与 Tate parameter \(q_v\) 混同。 |
| D3 — Θ-link | **部分正确，但不足以推出竖直映射** | Definition 3.8(ii) 的 \(\Theta^{\times\mu}_{\mathrm{LGP}}\)-link 是相对于 log-link 的 full poly-isomorphism of prime-strips；Remark 3.8.1 确实说明 pilot 对象被送到 q-pilot 对象。它不是函数域/环同态。但该定义没有给出附件所需的 \(W_\Theta(v)\to W_q(v)\) 实线性或序保持映射。 |
| D4 — Log-volume/indeterminacies | **错误归纳且带循环性** | Proposition 3.9 定义的是 compact opens/archimedean compact closures 的局部及全局 log-volume，并说明与 procession、mono-analytic structures、log-links 的兼容性。Theorem 3.11 中 Ind1、Ind2、Ind3 是具体的 automorphism actions、tensor-packet actions 及随纵向移动的 upper semi-compatibility，不是附件所列的三个“数值误差区间”。D4 最后一句直接说“accounting 后 comparison becomes”目标不等式，等于把待证结论放入定义。 |
| D5 — Corollary 3.12 | **不是真正的 verbatim statement** | 不等式方向 \(-|\log\Theta|\ge -|\log q|\) 与原文一致；但原文先分别定义：\(-|\log\Theta|\) 是 Θ-pilot 在 Ind1–Ind3 下所有可能像之并的 holomorphic hull 的 procession-normalized mono-analytic log-volume，而 \(-|\log q|\) 是不受这些 indeterminacies 的 q-pilot log-volume；还断言 \(|\log q|>0\)、Θ 量有限并含系数条件。附件删掉了对判断至关重要的非对称定义。 |
| D6 — Concrete embeddings | **未由所引 Proposition 3.9 定义** | 初等恒等式 \(\log|q_v^{j^2}|=j^2\log|q_v|\) 正确；但 IUTT-III Proposition 3.9 没有定义每个坏素点的 canonical one-dimensional spaces \(W_q(v),W_\Theta(v)\)，也没有定义附件的两条竖直嵌入。把初等取对数公式提升成 IUTT pilot 对象之间的函子性嵌入，正是待证明而不能预设的步骤。 |
| D7 — Scholze–Stix concern | **作为高层摘要基本准确；不是 IUTT 已定义方图** | Scholze–Stix §§2.1.6–2.2 确实区分 abstract pilots 与 concrete copies of \(\mathbb R\)，指出同时保留 \(j^2\) 标度会产生 monodromy/不交换问题，并质疑 indeterminacy 是否足以模糊该差异。附件四节点方图是对此的再构造，而不是他们或 IUTT-III 明确定义的图。 |

结论：OB-02v2 的 “All definitions (self-contained — everything is here)” 不成立。D1、D2、D4、D5、D6 均含会改变问题类型或结论的偏差。

## 4. 方图首先不适定：底部箭头类别决定答案

令
\[
L=\log|q_v|\ne0,
\qquad j\in\{1,\ldots,(\ell-1)/2\}.
\]
附件希望左路得到 \(j^2L\)，右路得到 \(L\)，但把底箭头写成 `???`。

### 4.1 若底箭头是任意集合映射

可以人为定义一个非单射映射 \(b\)，使 \(b(j^2L)=L\) 对所有有限多个 \(j\) 成立。于是这个玩具方图可以“交换”，却不给出任何 log-volume 不等式，也不反映 IUT morphism。

### 4.2 若底箭头是一条统一的实线性同构

写 \(b(x)=cx\)。若顶箭头把每个 Θ-label 都识别到同一个 q-pilot，交换性要求
\[
cj^2L=L.
\]
由于 \(L\ne0\)，\(j=1\) 给出 \(c=1\)，\(j=2\) 给出 \(c=1/4\)。当 \(\ell\ge5\) 时两者矛盾。

这是一条完全初等、可机器形式化的**条件性不交换引理**。但附加假设

> H：底箭头是一条独立于 \(j\) 的统一实线性同构，且顶箭头把所有 Θ-label 送到同一 q-pilot

并不是 Definition 3.8 或 Proposition 3.9 的陈述。因此该引理是诊断工具，不满足附件的 CONFIRMED-OBSTRUCTION：不能用自选的 H 代替 IUTT 中实际的 morphism class。

### 4.3 若底箭头是序保持缩放或商关系

答案又取决于缩放常数、商掉何种作用、半直线的方向，以及 \(-|\log\Theta|\) 是点、上确界、hull 的体积还是所有可能像的界。附件没有指定这些数据。“底箭头把某半直线送入另一半直线”也不是 Corollary 3.12 原文中定义的等价命题。

所以，在识别底箭头的类别以前，OB-02v2 的 Claim 不是一个确定命题。

## 5. Proof skeleton 逐步核验

### Step 1 — Identify the relevant 1D real vector spaces

**判断：FAIL（定义缺失）。**

Proposition 3.9 的输入是 \(\mathbb M(\mathrm{IQ}(\cdots))\) 中的 compact opens/closures，输出是局部或全局实 log-volume。它没有定义
\[
\iota_q:q\text{-pilot}\to W_v,
\qquad
\iota_\Theta:\Theta\text{-pilot}\to W_v,
\]
也没有把 Θ-volume 定义为附件要求的
\(\sum_j j^2\log|q_v|\)。真实 Corollary 3.12 还要先取所有 Ind1–Ind3-images 的并、holomorphic hull、determinant/tensor normalization 与 procession normalization。

因此 Step 1 不能由 D4/D6 或 Proposition 3.9 关闭。

### Step 2 — Unpack the Θ-link action on pilot objects

**判断：PARTIALLY VERIFIED。**

Definition 3.8 与 Remark 3.8.1 支持以下较弱陈述：在 prime-strip/full poly-isomorphism 的抽象层次，Θ-pilot 被送到 q-pilot。它们不支持更强陈述：存在一个被该 link 诱导的逐素点实映射，使附件的两条 concrete embeddings 形成自然方图。

附件要求“cite the specific morphism ... that induces the action on pilot objects”。可引用的 specific morphism 正是 prime-strip poly-isomorphism；但从它到 \(W_v\) 的诱导 morphism 没有给出。类型链在这里中断：
\[
\text{prime-strip poly-isomorphism}
\quad\not\Rightarrow\quad
\text{ordered real-linear map on local log coordinates}.
\]

### Step 3 — \(j^2\)-scaling compatibility

**判断：OPEN，且缺口已定位。**

IUTT-III Theorem 3.11 中：

- Ind1 是 procession/prime-strip 层的 automorphism indeterminacy；
- Ind2 作用于 tensor-product 的各 direct summands；
- Ind3 是随 log-links 的 upper semi-compatibility，在非阿基米德情形涉及 inclusions，在阿基米德情形涉及 surjections。

附件没有从这些作用导出一个实数关系
\[
j^2L\sim L
\quad\text{或}
\quad
(j^2-1)L\in I_{\mathrm{Ind1-3}},
\]
因为原文也没有把 Ind1–Ind3 定义为一个可与 \((j^2-1)L\) 比较的加法误差区间。故不能说某一个 indeterminacy “absorbs” 此差值。

需要补出的精确对象是至少一族比较态射/关系
\[
B_{\mathbf j}:
\operatorname{LogVol}\!\left(
\det{}^{\otimes M}
\operatorname{Hull}(P_{\Theta,\mathbf j})/mathrm{Ind}_{1,2,3}
\right)
\longrightarrow
\operatorname{LogVol}(P_q),
\]
其中必须明示：

1. \(P_{\Theta,\mathbf j}\) 与 \(P_q\) 的实际 IUTT 类型；
2. \(M\) 及各 direct summand 的权重；
3. hull、union 与 quotient/action 的顺序；
4. \(B_{\mathbf j}\) 是函数还是 correspondence，是否序保持；
5. 它对 \(q_v^{j^2}\) 或 \(\underline q_v^{j^2}\) 的作用公式；
6. local-to-global procession normalization；
7. 哪个已证明的命题保证以上构造与 Θ-link 自然兼容。

这些不是“把证明写得更详细”的装饰；缺少任一项，都无法形成附件要求的交换方图。

### Step 4 — Derivation of \(-|\log\Theta|\ge -|\log q|\)

**判断：FAIL at (xi-e) → (xi-f)。**

独立核对原文后的逻辑链为：

1. (xi-d) 先暂时忘掉许多内部结构，只保留抽象算法的性质；只有经过合适的正张量幂、determinant 与适当归一化 log-volume 后，才称所得实对象“完全可比较”。
2. (xi-e) 由 SHE 说：即使固定输入 pilot log-volume 为 \(-|\log q|\)，算法仍有效；possible output log-volumes 构成 \(\mathbb R_{\le -|\log\Theta|}\)，且借 prime-strip isomorphisms 与输入“相关”。
3. (xi-f) 说这个构造至少近似地重构 \(-|\log q|\)，继而断言该输入属于上述区间。

缺失的推理规则是
\[
\begin{aligned}
&\text{“输出与固定输入在 prime-strip/SHE 意义下相关”}\\
&\hspace{20mm}\Longrightarrow
\text{“该输入作为同一有序实坐标中的点属于输出半直线”}.
\end{aligned}
\]

这个蕴含需要 Step 3 所列的 \(B_{\mathbf j}\) 及其序兼容性。Definition 3.8、Proposition 3.9、Theorem 3.11 或 Remark 3.9.5(vii) 的被核对部分均没有提供该蕴含。于是 (xi-f) 的 membership 不能由 (xi-e) 在附件要求的严格意义下推出。

## 6. 数值锚点 37.a1 的独立核验

曲线
\[
E:y^2+y=x^3-x,
\qquad [a_1,a_2,a_3,a_4,a_6]=[0,0,1,-1,0]
\]
的精确不变量为
\[
b_2=0,\quad b_4=-2,\quad b_6=1,\quad b_8=-1,
\]
\[
c_4=48,\qquad c_6=-216,
\qquad \Delta=37,
\qquad j(E)=\frac{48^3}{37}=\frac{110592}{37}.
\]
所以
\[
v_{37}(j(E))=-1.
\]

LMFDB 给出的 conductor 为 37，唯一坏素点为 37，Kodaira symbol 为 \(I_1\)，约化为 nonsplit multiplicative。因而 Tate uniformization 要在未分歧二次扩张后写出；该扩张不改变此处的归一化绝对值结论。

由 Tate 展开
\[
j(q)=q^{-1}+744+196884q+\cdots
\]
得
\[
v_{37}(q_{37})=-v_{37}(j(E))=1.
\]
取标准归一化 \(|37|_{37}=37^{-1}\)，则正确公式是
\[
\boxed{
\log|q_{37}|_{37}
=-v_{37}(q_{37})\log37
=v_{37}(j(E))\log37
=-\log37
}
\]
而附件写成
\[
-v_{37}(j(E))\log37=+\log37,
\]
符号相反，并与其同时声称的 \(\log|q_{37}|_{37}<0\) 冲突。

数值为
\[
\log37=3.610917912644224\ldots,
\qquad
L:=\log|q_{37}|_{37}=-3.610917912644224\ldots.
\]

| \(j\) | Path A 玩具坐标 \(j^2L\) | Path B 玩具坐标 \(L\) | 差值 \((j^2-1)L\) |
|---:|---:|---:|---:|
| 1 | \(-3.610917912644224\ldots\) | \(-3.610917912644224\ldots\) | \(0\) |
| 2 | \(-14.443671650576897\ldots\) | \(-3.610917912644224\ldots\) | \(-10.832753737932673\ldots\) |
| 3 | \(-32.498261213798019\ldots\) | \(-3.610917912644224\ldots\) | \(-28.887343301153795\ldots\) |

附件脚本正确算出 \(c_4,c_6,\Delta\) 和平方因子；它没有实际计算 Tate 参数的绝对值，所以没有捕获上述符号错误。

还有一个独立的 normalization 问题：IUTT-I Example 3.2(iv) 的 q-pilot 记号使用
\[
\underline q_v:=q_v^{1/(2\ell)}
\quad\text{（至 }\mu_{2\ell}\text{）},
\]
故若比较的是 \(\underline q_v\)，其 log absolute value 是 \(L/(2\ell)\)，而不是 \(L\)。OB-02v2 必须先固定它究竟使用 Tate parameter 还是 IUT pilot generator，再谈 \(j^2\) 标度。

## 7. 为什么 37.a1 不能升级为 CONFIRMED-OBSTRUCTION

“给出一条椭圆曲线和一个坏素点”并未给出 IUTT-I Definition 3.1 的 initial Θ-data。至少仍需明确并验证：

- \(\overline F/F\)、模域及其 Galois 条件；
- \(X_F\) 的 puncture 与 stable reduction 条件；
- 符合 mod-\(\ell\) image、坏特征、Tate-order 等约束的具体 \(\ell\ge5\)；
- 由 \(\ell\)-torsion kernel 等构造的 \(K\)；
- orbicurve \(C_K\) 及 core/cusp 条件；
- valuations section \(V\) 与 \(V^{\mathrm{bad}}_{\mathrm{mod}}\)；
- Definition 3.1 的末项 cusp 数据。

即使这些数据补齐，还必须在真实 Frobenioid/tensor-packet 对象上证明不存在任何 Ind1–Ind3-admissible identification；仅证明实数 \(j^2L\ne L\) 不足以排除 IUTT 中尚未显式化的商或 correspondence。

所以 37.a1 是有效的玩具坐标检查，也是附件公式错误的反例；它不是 acceptance criterion 2 所要求的 IUTT-admissible obstruction。

## 8. 非循环性审计

- 本报告未假设 RH，也未使用 ζ 零点位置或任何 RH 等价命题。
- 本报告未假设 abc、Szpiro、其等价形式、已知 abc triples 或 fitted \(K_\varepsilon\)。
- 本报告没有把 IUTT-III Corollary 3.12 当作前提。
- OB-02v2 的 D4 最后一句把 “accounting for all three indeterminacies” 直接解释为目标不等式；若在 Step 3 或 Step 4 使用该句，就构成局部循环。该句必须删除，改为 Theorem 3.11 中 Ind1–Ind3 的实际作用定义。
- 数值锚点只用于类型与符号 sanity check，不用于推导全局结论。

## 9. 达到可重审状态所需的最小补件

下一版本若希望超越 **INCONCLUSIVE + LOCALIZATION**，至少应：

1. 逐字采用 IUTT-I Definition 3.1 的 initial Θ-data，并给出完整的允许前置结果清单；
2. 全文区分 Tate parameter \(q_v\) 与 IUT generator \(\underline q_v\)；
3. 删除“Proposition 3.9 定义 \(W_v\) 和 concrete embeddings”的错误归因；若这些空间是作者自定义的，就显式标为新定义，并证明它们对 IUT morphisms 函子化；
4. 给底箭头声明类别、定义域、陪域、是否依赖 \(j\)、是否单射/线性/序保持；
5. 从 Remark 3.9.5(vii) 把 determinant、正张量幂 \(M\)、各 summand 权重及 normalization 全部写成公式；
6. 把 Ind1–Ind3 写成在上述对象上的实际群作用、包含或满射，而不是“误差范围”；
7. 构造 Step 3 中的 \(B_{\mathbf j}\)，并证明它与 Θ-link、hull、union、determinant、procession normalization 兼容；
8. 给出从 (xi-e) 到 membership in (xi-f) 的独立引理，明确其序结构；
9. 若主张 obstruction，则提供一套逐项验证过 Definition 3.1 的具体 initial Θ-data，并在真实 IUT 对象上排除全部 admissible indeterminacies；
10. 修正 37.a1 的 \(p\)-adic 对数符号，并说明 nonsplit Tate uniformization 与 \(2\ell\)-th-root normalization。

## 10. 最终回答（按附件四选一格式）

> **INCONCLUSIVE + LOCALIZATION**
>
> **缺失 morphism：** 从 IUTT-III Definition 3.8(ii) 的 prime-strip full poly-isomorphism，经 Remark 3.9.5(vii) 所需的 holomorphic hull、determinant/positive tensor power、normalization 与 Theorem 3.11 的 Ind1–Ind3 后，诱导到一个共同有序实 log-volume 坐标的、足以把 (xi-e) 的“related output region”提升为 (xi-f) 的 membership 的比较映射 \(B_{\mathbf j}\)。
>
> **精确位置：** IUTT-III Remark 3.9.5(vii), Observations 3-1–3、9-2；Corollary 3.12 proof (xi-d), (xi-e), (xi-f)；类型入口为 Definition 3.8(ii)，log-volume 入口为 Proposition 3.9，indeterminacy 入口为 Theorem 3.11。
>
> **不能提高为 CONFIRMED-PROOF 的原因：** 竖直 embeddings 与底箭头没有在所引 IUTT 命题中定义，且 D1–D6 多处不等于原文。
>
> **不能提高为 CONFIRMED-OBSTRUCTION 的原因：** 37.a1 不是完整 initial Θ-data，附件也未给出可在真实 IUT 对象上排除 Ind1–Ind3 的计算模型。

## 参考资料

1. Shinichi Mochizuki, [*Inter-universal Teichmüller Theory I: Construction of Hodge Theaters*](https://ems.press/journals/prims/articles/201525), PRIMS 57 (2021), 3–207, DOI 10.4171/PRIMS/57-1-1. [Author PDF](https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20I.pdf).
2. Shinichi Mochizuki, [*Inter-universal Teichmüller Theory III: Canonical Splittings of the Log-Theta-Lattice*](https://ems.press/journals/prims/articles/201527), PRIMS 57 (2021), 403–626, DOI 10.4171/PRIMS/57-1-3. [Author PDF](https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20III.pdf).
3. Peter Scholze and Jakob Stix, [*Why abc is still a conjecture*](https://ncatlab.org/nlab/files/why_abc_is_still_a_conjecture.pdf), version dated 2018-08-23; compare the [authors' hosted copy](https://www.math.uni-bonn.de/people/scholze/WhyABCisStillaConjecture.pdf).
4. LMFDB, [Elliptic curve with LMFDB label 37.a1](https://www.lmfdb.org/EllipticCurve/Q/37/a/1).
