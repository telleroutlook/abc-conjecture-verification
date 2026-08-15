# Problem OB-01 独立审稿报告

**审稿对象：** OB-01-algebraic-geometry-height-bound(1).md  
**审稿日期：** 2026-08-15  
**总裁决：** **PARTIAL — major revision required**  
**若以解决 Claim OB-01 为 Gate-A：** **GATE-A BLOCKED**

## 1. 执行摘要

设

\[
a,b,c\in\mathbb Z_{>0},\qquad a+b=c,\qquad
\gcd(a,b)=\gcd(b,c)=\gcd(c,a)=1,
\]

\[
R=\operatorname{rad}(abc),\qquad
E_{a,b,c}:y^2=x(x-a)(x+b).
\]

本次独立核查得到：

| 项目 | 裁决 | 核查结果 |
|---|---|---|
| Step 1：极小判别式 | **CONFIRMED** | 两种可能值均正确，且各有实例达到 |
| Step 2：Faltings 高度下界 | **CONFIRMED / STRENGTHENED** | 附件的 \(\frac16\log c\) 可加强为 \(\frac13\log c+1.782877\ldots\) |
| Step 3：导子界 | **CONFIRMED / CITATIONS REPAIRED** | 原不等式正确；所列两处精确引文不正确；本族可加强为 \(f_2\le5\) |
| Claim 与 weak abc 的关系 | **CONFIRMED WITH QUALIFICATION** | 等价于**有效** fixed-power weak abc；Pasten 的印刷猜想本身未要求有效性 |
| Step 4 | **OPEN FRONTIER** | 不是现成代数几何引理，而正是上述开放猜想 |
| 建议的 \((1/6+\varepsilon)\log R\) 目标 | **REFUTED** | 被显式族 \((1,2^n-1,2^n)\) 无条件否定 |
| 普通 Szpiro 与 abc-equivalent Szpiro 的表述 | **REFUTED AS WRITTEN** | 必须区分 ordinary discriminant Szpiro 与 modified Szpiro |
| 数值锚点 \((1,8,9)\) | **CONFIRMED** | 精确不变量与高精度高度值均复现 |
| 非循环性 | **CONFIRMED** | Steps 1–3 未使用 abc、Szpiro、IUT、RH 或等价假设 |

因此，附件正确识别了一个真实的开放边界，但不能作为 Claim 的证明。另有两个承重陈述必须修改：错误的 \(1/6+\varepsilon\) 高度目标，以及 ordinary/modified Szpiro 的混同。

## 2. 精确量词与基本不变量

Claim OB-01 的量词是

\[
(\forall\varepsilon>0)(\exists C_\varepsilon>0
\text{，且 }C_\varepsilon\text{ 可由 }\varepsilon\text{ 有效计算})
(\forall a,b,c)\quad
h_F(E_{a,b,c})
\le C_\varepsilon(1+\varepsilon)\log R.
\tag{2.1}
\]

由于 \(C_\varepsilon\) 没有预先固定的主项归一化，因子
\(1+\varepsilon\) 可以吸收到常数中。取 \(\varepsilon=1\) 即得到一个统一有效常数；反向也显然。因此附件的“\(\varepsilon\)-absorption”成立。

展开所给模型：

\[
y^2=x^3+(b-a)x^2-abx.
\]

直接由 Weierstrass 不变量公式得

\[
c_4=16(a^2+ab+b^2),\qquad
\Delta_W=16a^2b^2(a+b)^2=16(abc)^2.
\tag{2.2}
\]

三数中恰有一个为偶数，所以

\[
R=2\prod_{\substack{p\mid abc\\p\ \mathrm{odd}}}p.
\tag{2.3}
\]

## 3. Step 1：极小判别式

Silverman, Lemma VIII.11.3(a)，正适用于满足
\(A+B=C\)、\(\gcd(A,B,C)=1\) 的 Frey 曲线。代入
\((A,B,C)=(b,a,a+b)\) 得

\[
|\Delta_{\min}|
\in\left\{16(abc)^2,\;2^{-8}(abc)^2\right\}.
\tag{3.1}
\]

因此

\[
2\log(abc)-8\log2
\le\log|\Delta_{\min}|
\le2\log(abc)+4\log2.
\tag{3.2}
\]

原稿所谓“唯一 change of variables”应改为：极小化尺度只有
\(u\in\{1,2\}\) 两种可能；这不意味着平移参数唯一。

两个端点都能精确达到：

- \((a,b,c)=(1,1,2)\)：模型 \(y^2=x^3-x\) 的
  \(\Delta=64\)，且 \(v_2(\Delta)=6<12\)，故已极小，达到
  \(16(abc)^2\)。
- \((a,b,c)=(16,1,17)\)：作

  \[
  x=4X,\qquad y=8Y+4X,
  \]

  得

  \[
  Y^2+XY=X^3-4X^2-X,
  \]

  其 \(\Delta=17^2=289\)、\(c_4=273\)。它在 \(2\) 处良约化，
  在 \(17\) 处满足 \(v_{17}(c_4)=0\)，故全局极小并达到
  \(2^{-8}(abc)^2\)。

对每个奇素数 \(p\mid abc\)，两两互素性给出
\(p\nmid c_4\)，且极小化尺度只有 \(2\)-幂，故

\[
v_p(\Delta_{\min})=2v_p(abc).
\tag{3.3}
\]

**Step 1 裁决：CONFIRMED。**

## 4. Step 2：高度下界及加强

Murty–Pasten, Theorem 5.1 使用的归一化满足

\[
12h_F(E)=\log|\Delta_E|
-\log\!\left(|\Delta(\tau_E)|(\Im\tau_E)^6\right)
+12\log(2\pi).
\tag{4.1}
\]

其 Theorem 5.4 给出

\[
12h_F(E)>\log|\Delta_E|+28.326.
\tag{4.2}
\]

与 (3.2) 合并：

\[
h_F(E_{a,b,c})>
\frac16\log(abc)+
\frac{28.326-8\log2}{12},
\tag{4.3}
\]

\[
\frac{28.326-8\log2}{12}
=1.898401879626703\ldots.
\]

附件只使用 \(abc\ge c\)，得到 \(\frac16\log c\)。实际上
\(a+b=c\)、\(a,b\ge1\) 给出

\[
ab\ge c-1,\qquad abc\ge c(c-1).
\]

所以对 \(c\ge2\)，

\[
\begin{aligned}
h_F(E_{a,b,c})
&>\frac16\bigl(\log c+\log(c-1)\bigr)
  +1.898401879626703\ldots\\
&\ge\frac13\log c+1.782877349533378\ldots.
\end{aligned}
\tag{4.4}
\]

**Step 2 裁决：CONFIRMED，并由 (4.4) 加强。**

## 5. Step 3：导子与引文修复

Silverman, Lemma VIII.11.3(b) 给出：

- 奇素数 \(p\mid abc\) 处为乘法约化，故 \(f_p=1\)；
- 奇素数 \(p\nmid abc\) 处为良约化，故 \(f_p=0\)。

因此

\[
N_E
=2^{f_2}\prod_{\substack{p\mid abc\\p\ \mathrm{odd}}}p
=2^{f_2-1}R.
\tag{5.1}
\]

附件的两处精确引证需要修复：

1. Silverman, Proposition VIII.11.5 讨论 Szpiro 与 abc 的转换，
   不是 Frey 曲线的导子公式。
2. Barrios–Roy, Lemma 2.2 只说明赋值三元组
   \((v_p(c_4),v_p(c_6),v_p(\Delta))\) 如何限制 Kodaira 型；
   它不是本 Frey 族的导子表。

Barrios–Roy §2 的一般加性界 \(f_2=2+\delta_2\)、\(\delta_2\le6\)
足以证明附件所用的 \(f_2\le8\)。但本曲线有满有理二挠点；
在其 Theorem 3.7 / Table 7 中取 \(d=1\)，逐行可得更强的

\[
0\le f_2\le5.
\tag{5.2}
\]

于是

\[
\boxed{\log N_E\le\log R+4\log2.}
\tag{5.3}
\]

同时 \(f_2\ge0\) 给出

\[
N_E\ge R/2,\qquad
\log R\le\log N_E+\log2.
\tag{5.4}
\]

附件的 \(\log N_E\le\log R+7\log2\) 仍然为真，但不紧；错误在引文定位，不在不等式真值。

**Step 3 裁决：CONFIRMED；应改引 Silverman Lemma VIII.11.3(b) 及 Barrios–Roy Theorem 3.7 / Table 7。**

## 6. Claim 与有效 fixed-power weak abc

### 6.1 Claim 推出有效 bounded quality

取 (2.1) 中 \(\varepsilon=1\)，令 \(H=2C_1\)，则

\[
h_F(E_{a,b,c})\le H\log R.
\]

由 (4.4) 得

\[
\log c<3H\log R.
\]

故质量

\[
q(a,b,c)=\frac{\log c}{\log R}
\]

被一个可有效计算的统一常数控制。

### 6.2 有效 bounded quality 推出 Claim

令

\[
S=a^2+ab+b^2=c^2-ab<c^2.
\]

由 (2.2) 得

\[
j(E)=\frac{256S^3}{(abc)^2}.
\tag{6.1}
\]

约分只会降低分子、分母的最大值，且 \(abc\le c^3\)，故绝对对数 Weil 高度满足

\[
h(j(E))\le6\log c+8\log2.
\tag{6.2}
\]

还需控制 Löbrich, Proposition 3.1 中的不稳定判别式理想
\(\gamma_{E/\mathbb Q}\)。奇素数处只有良约化或乘法约化，所以
\(\gamma\) 没有奇素因子。又因 \(S\) 为奇数：

- 若极小化尺度 \(u=2\)，则 \(v_2(c_{4,\min})=0\)，所以
  \(v_2(\gamma)=0\)；
- 若 \(u=1\)，则 \(v_2(c_{4,\min})=4\)，而

  \[
  v_2(\gamma)
  =\min\{v_2(\Delta_{\min}),3v_2(c_{4,\min})\}
  \le12.
  \]

故

\[
\gamma\mid2^{12}.
\tag{6.3}
\]

Löbrich, Proposition 3.1 的一侧常数可取 \(0.72\)。将其 Deligne
归一化平移到 Murty–Pasten 归一化，两者相差

\[
\log4+\frac32\log\pi
=3.103389189893991\ldots.
\tag{6.4}
\]

由 (6.2)–(6.4) 得到一个显式、无需最优的上界

\[
h_F^{\mathrm{MP}}(E_{a,b,c})
\le\frac12\log c+3.538635.
\tag{6.5}
\]

若存在有效 \(K_0\) 使

\[
\log c\le K_0\log R,
\tag{6.6}
\]

则因 \(R\ge2\)，

\[
h_F(E_{a,b,c})
\le
\left(\frac{K_0}{2}
+\frac{3.538635}{\log2}\right)\log R.
\]

把括号内常数吸收到 \(C_\varepsilon(1+\varepsilon)\) 即得 Claim。

综上，

\[
\boxed{
\text{Claim OB-01}
\iff
\text{有效统一 bounded quality}
\iff
\text{有效 fixed-power weak abc}.
}
\tag{6.7}
\]

重要限定：Pasten, Conjectures 1.1–1.2 的印刷陈述只要求某个常数存在，
没有要求该常数可有效计算。因此 (6.7) 对应的是其**有效加强版**。

## 7. Step 4：真正的开放边界

在本 Frey 族中，若存在有效常数 \(A,B\) 使

\[
\log|\Delta_{\min}(E)|\le A\log N_E+B,
\tag{7.1}
\]

则由 (3.2)、(5.3) 立即得 \(\log c\ll\log R\)。反向，若
\(\log c\le K_0\log R\)，则

\[
\log|\Delta_{\min}|
\le2\log(abc)+4\log2
\le6\log c+4\log2
\ll\log R
\ll\log N_E+1.
\]

故对这个 Frey 族，固定常数的 discriminant–conductor 界与
fixed-power weak abc 双向等价。

这说明 Step 4 不是一个当前已知、尚待查找引文的代数几何引理。
证明它就会证明一个开放的弱 abc 猜想；现有文献不能被当作已知前件调用。

**Step 4 裁决：INCONCLUSIVE / OPEN FRONTIER。**

## 8. \((1/6+\varepsilon)\log R\) 目标的显式反例

附件建议把“标准 abc 强度”写成

\[
h_F(E_{a,b,c})
\le(1/6+\varepsilon)\log R+C_\varepsilon.
\tag{8.1}
\]

该陈述无条件为假。取无限族

\[
(a_n,b_n,c_n)=(1,2^n-1,2^n).
\tag{8.2}
\]

它们两两互素并满足 \(a_n+b_n=c_n\)。而且

\[
R_n=2\operatorname{rad}(2^n-1)<2^{n+1},
\tag{8.3}
\]

\[
a_nb_nc_n
=2^n(2^n-1)
\ge2^{2n-1}.
\tag{8.4}
\]

由 (4.3)，

\[
h_F(E_n)>
\frac{2n-1}{6}\log2+1.898401\ldots.
\tag{8.5}
\]

若 (8.1) 对某个固定 \(\varepsilon<1/6\) 成立，则由 (8.3)

\[
h_F(E_n)
<(1/6+\varepsilon)(n+1)\log2+C_\varepsilon.
\tag{8.6}
\]

(8.5) 的 \(n\)-斜率是 \((1/3)\log2\)，而 (8.6) 的斜率严格更小，
矛盾。取 \(\varepsilon=1/12\) 已足够。

所以这不是常数或归一化问题，而是主系数错误。文献中的精细 Frey
高度猜想在维数 \(1\) 时使用 \(\frac12+\varepsilon\) 作为稳定
Faltings 高度的主系数，见 Javanpeykar, Conjecture (h)。

**附件所提 \(1/6+\varepsilon\) 目标：REFUTED。**

## 9. Ordinary Szpiro 与 modified Szpiro

Silverman, Conjecture VIII.11.1 的 ordinary discriminant Szpiro 是

\[
|\Delta_{\min}(E)|
\le C_\varepsilon N_E^{6+\varepsilon}.
\tag{9.1}
\]

Silverman, Proposition VIII.11.5(a) 对 Frey 曲线从 (9.1) 得到的是
abc 的 \(3/2\) 指数，而不是 \(1+\varepsilon\)。原因在于本族

\[
|\Delta_{\min}|\gg(abc)^2\gg c^4.
\]

与标准 abc 等价的形式是 modified Szpiro：

\[
\max\{|c_4|^3,c_6^2\}
\le C_\varepsilon N_E^{6+\varepsilon}.
\tag{9.2}
\]

本 Frey 曲线上

\[
c_4=16(a^2+ab+b^2),\qquad
a^2+ab+b^2=c^2-ab\ge\frac34c^2.
\]

因而 (9.2) 的六次根直接控制 \(c\)，这才产生标准
\(1+\varepsilon\) 型 abc 指数。

附件应改成：

- ordinary discriminant Szpiro 的指数是 \(6+\varepsilon\)；
  直接用于本族只推出 \(3/2\) 型 abc；
- 与标准 abc 等价的是 modified Szpiro，而不是仅控制
  \(|\Delta_{\min}|\) 的普通形式。

## 10. 失败模式与非循环性

标准 abc 在某个固定 \(\varepsilon>0\) 处失败，只能给出一列三元组满足

\[
\frac{c_n}{R_n^{1+\varepsilon}}\to\infty.
\]

写成质量：

\[
q_n
=1+\varepsilon+
\frac{\log(c_n/R_n^{1+\varepsilon})}{\log R_n}.
\]

分子趋于无穷不迫使该比值趋于无穷。因此不能据此推出
\(q_n\to\infty\)；后者是 fixed-power weak abc 的失败，逻辑上更强。

附件要求的二择一——证明本族 Szpiro 比统一有界，或给出其无界显式族——
分别会解决或否定 fixed-power weak abc；当前文献没有完成其中任何一项。

非循环性核查：

- Steps 1–3 只使用极小模型、局部约化和无条件高度估计；
- abc、ordinary/modified Szpiro、fixed-power weak abc 只作为开放边界出现；
- 未使用 IUT Corollary 3.12、RH、RH 等价命题或 \(\zeta\) 零点位置；
- 数值样本只作 sanity check，不参与证明。

**非循环性裁决：CONFIRMED。**

## 11. 数值锚点 \((1,8,9)\)

精确计算：

\[
R=6,\qquad
\Delta_W=16(72)^2=82944=2^{10}3^4,
\]

\[
c_4=16(1+8+64)=1168,\qquad
j=\frac{c_4^3}{\Delta_W}
=\frac{1556068}{81}.
\]

因 \(v_2(\Delta)=10<12\)，模型在 \(2\) 处已极小；且
\(3\nmid c_4\)，在 \(3\) 处为乘法约化并已极小。所以
\(\Delta_{\min}=82944\)。

独立高精度复算如下：

| 数量 | 数值 |
|---|---:|
| \(\log R\) | \(1.791759469228055\) |
| \(\log c\) | \(2.197224577336220\) |
| \(q=\log9/\log6\) | \(1.226294385530917\) |
| \(\frac1{12}\log|\Delta_{\min}|\) | \(0.943826746689324\) |
| \(h_F\)，Murty–Pasten 归一化 | \(3.376975437018806\) |
| \(h_F\)，Deligne 归一化 | \(0.273586247124815\) |
| \(\frac32\log6\) | \(2.687639203842083\) |

复算使用 Legendre 参数 \(\lambda=8/9\)、AGM 公式

\[
K(m)=\frac{\pi}{2\operatorname{AGM}(1,\sqrt{1-m})},
\]

\[
\tau=i\frac{K(8/9)}{K(1/9)},\qquad
\Im\tau=1.563401922696111\ldots,
\]

以及快速收敛乘积

\[
\Delta(\tau)=q_\tau\prod_{n\ge1}(1-q_\tau^n)^{24},
\qquad q_\tau=e^{2\pi i\tau}.
\]

两种高度归一化之差为

\[
\log4+\frac32\log\pi
=3.103389189893991\ldots.
\]

所以附件的数值结论正确：
\(0.943826\ldots\) 只是有限处贡献，不是完整 Faltings 高度。

**数值锚点裁决：CONFIRMED。**

## 12. 引文逐项核验

| 附件所用结果 | 正确原始位置 | 裁决 |
|---|---|---|
| 两种极小判别式 | Silverman, Lemma VIII.11.3(a) | **CONFIRMED** |
| 奇素数处乘法约化 | Silverman, Lemma VIII.11.3(b) | **CONFIRMED** |
| 高度公式与 \(28.326\) | Murty–Pasten, Theorems 5.1, 5.4 | **CONFIRMED** |
| \(h_F<0.1N\log N+11\) | Murty–Pasten, Theorem 7.1 | **CONFIRMED** |
| \(h(j)\) 与非稳定 Faltings 高度比较 | Löbrich, Proposition 3.1 | **CONFIRMED** |
| 导子公式引 Silverman Proposition VIII.11.5 | 该命题内容不是导子公式 | **REFUTED-CITATION** |
| Barrios–Roy Lemma 2.2 作为本族导子表 | 应用 Theorem 3.7 / Table 7 | **REFUTED-CITATION** |
| Pasten weak abc 的量词 | Conjectures 1.1–1.2 只要求存在性 | **QUALIFICATION REQUIRED** |
| Stewart–Yu 全局无条件界 | Stewart–Yu, Theorem 1 | **CONFIRMED** |

Stewart–Yu 的无条件结果为

\[
c<\exp\!\left(KR^{1/3}(\log R)^3\right)
\]

且 \(K\) 有效。截至审稿日，它仍是这里可对所有三元组统一调用的点态界；
Pasten 的后续改进带有额外大小条件，不能无条件替代它。

## 13. 最小修订清单

1. 删除 Step 3 对 Silverman Proposition VIII.11.5 的导子引用；
   改引 Lemma VIII.11.3(b)。
2. 将 Barrios–Roy Lemma 2.2 改为 Theorem 3.7 / Table 7；
   建议同时把 \(f_2\le8\) 加强为 \(f_2\le5\)。
3. 在 Claim 等价 weak abc 处加入本报告 §6 的反向证明，
   不再依赖未附的 referee report。
4. 明确区分 Pasten 的存在型猜想与 Claim 所要求的有效版本。
5. 删除 \((1/6+\varepsilon)\log R+C_\varepsilon\) 目标；
   至少加入 §8 的显式反例族。
6. 将“abc-equivalent Szpiro”改为 modified Szpiro，
   并说明 ordinary discriminant Szpiro 在本族只给 \(3/2\) 指数。
7. 总状态维持为 **PARTIAL**；不得提升为
   CONFIRMED-PROOF、GATE-A PASS 或已证明 obstruction。

## 14. 原始来源

1. Joseph H. Silverman, The Arithmetic of Elliptic Curves, 2nd ed.,
   Lemma VIII.11.3 and Proposition VIII.11.5:  
   https://www.math.ens.psl.eu/~obenoist/refs/Silverman.pdf
2. M. Ram Murty and Héctor Pasten,
   Modular forms and effective Diophantine approximation,
   Theorems 5.1, 5.4, 7.1:  
   https://people.math.harvard.edu/~hpasten/preprints/modabcJNT.pdf
3. Steffen Löbrich, A Gap in the Spectrum of the Faltings Height,
   Proposition 3.1:  
   https://www.numdam.org/item/JTNB_2017__29_1_289_0.pdf
4. Alexander J. Barrios and Manami Roy,
   Local data of rational elliptic curves with non-trivial torsion,
   Theorem 3.7 / Table 7:  
   https://arxiv.org/pdf/2104.10337
5. Héctor Pasten, Shimura curves and the abc conjecture,
   Conjectures 1.1–1.2 and §3:  
   https://arxiv.org/pdf/1705.09251
6. C. L. Stewart and Kunrui Yu, On the abc conjecture, II,
   Theorem 1:  
   https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/s0012-7094-01-10815-6.pdf
7. Ariyan Javanpeykar, Szpiro’s small points conjecture for cyclic covers,
   Conjecture (h):  
   https://arxiv.org/pdf/1311.0043
8. Alexander J. Barrios, Lower bounds for the modified Szpiro ratio:  
   https://arxiv.org/pdf/2104.10817
9. Héctor Pasten,
   The largest prime factor of \(n^2+1\) and improvements on subexponential ABC:  
   https://arxiv.org/abs/2312.03566

---

**最终独立裁决：PARTIAL — Steps 1–3 confirmed and strengthened; Claim OB-01 remains equivalent to an effective fixed-power weak abc statement and is open. The manuscript additionally requires major correction of the \((1/6+\varepsilon)\) height target and of the ordinary/modified Szpiro distinction.**
