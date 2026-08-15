# OB-03 / P_height 独立送审报告

**审阅对象：** `OB-03-p-height-framework(1).md`  
**日期：** 2026-08-15  
**性质：** 独立 Gate-A 复核；不把原稿的 `CLOSED` 或 `COMPLETE` 当作前提

## 通用送审头（必附）

本报告对所附问题作独立审稿，而不是替作者完成或默认其结论成立。报告先核对精确陈述、量词、符号和允许引用的结果，再逐步核验承重等式、界、数值锚点和非循环性；普通证明、可执行检查与证明助理形式化核验分开判定。

## 最终裁决

**Gate-A：MAJOR REVISION。**

| 层面 | 独立结论 |
|---|---|
| OB-03-A 至 D 的普通数学内容 | **PASS；修正下列问题后可判 `COMPLETE-MATH`** |
| B、C 的 $a$ 奇、$b$ 偶限制 | **不必要；同一证明覆盖全部正整数互素 abc-triple** |
| abc / Szpiro / IUT 非循环性 | **PASS** |
| RH / ζ 零点非循环性 | **PASS** |
| 数值锚点 | **一处小数错误；一处反例见证不足** |
| “formally verified” | **FAIL / NOT SUBMITTED；附件没有任何机器工件** |

原稿的 `COMPLETE` 要求 A–D 均已形式化核验，当前不满足；`PARTIAL-ABC` 又错误地暗示 B、C 有数学缺口。建议采用新标签 **`PARTIAL-FORMALIZATION`**。若交付目标只是普通数学证明，则可采用 **`COMPLETE-MATH after corrections`**。

## 两处必须更正

### 1. 高度锚点

对 $(a,b,c)=(1,8,9)$，

$$
\frac16\log72=0.712777686502675885\ldots,\qquad
\frac13\log2=0.231049060186648436\ldots,
$$

故

$$
\frac16\log72+\frac13\log2
=0.943826746689324322\ldots,
$$

不是原稿的 $0.9415\ldots$。而且

$$
\frac1{12}\log82944
=\frac16\log72+\frac13\log2
$$

精确成立。定理常数没有错；该例恰好证明 $C=(1/3)\log2$ 为紧常数。

### 2. 两个旧命题需要两个反例

$(1,8,9)$ 给出

$$
N_E=48>36=\operatorname{rad}(144)^2,
$$

所以能反驳 $N_E\mid\operatorname{rad}(2abc)^2$。但该例中
$\operatorname{rad}(N_E)=\operatorname{rad}(2abc)=6$，不能反驳 rad 等式。

后一等式可用 $(3,16,19)$ 反驳。原模型经

$$
x=4x',\qquad y=8y'-12x'
$$

化为

$$
y'^2-3x'y'=x'^3+x'^2-3x',
$$

判别式为 $3249=3^2\cdot19^2$。故 $2$ 处良约化、$3,19$ 处乘法约化，

$$
N_E=57,\qquad
\operatorname{rad}(N_E)=57
\ne114=\operatorname{rad}(2abc).
$$

## 精确陈述与引文

- $\operatorname{rad}$ 的定义域是 $\mathbb Z\setminus\{0\}$；正式规格应同时写 $\operatorname{rad}(\pm1)=1$。
- abc-triple 的量词是 $a,b,c\in\mathbb Z_{>0}$、$a+b=c$、$\gcd(a,b)=1$；由此两两互素，且 $R=\operatorname{rad}(abc)\ge2$。
- D 中若出现“对所有 $\varepsilon>0$”，但 $\varepsilon$ 不在结论谓词中，该量词确实空泛。
- 附件没有单列封闭的“允许引用的前置结果”清单；送审前应补上。

引文核验：

1. **Silverman (2009), `The Arithmetic of Elliptic Curves`, Lemma VIII.11.3(a),(b)：精确匹配。** 引理假设 $A+B=C$、$\gcd(A,B,C)=1$，曲线为 $y^2=x(x+A)(x-B)$。取 $(A,B,C)=(b,a,c)$ 即为本题，且引理没有奇偶假设。[作者书页](https://www.math.brown.edu/johsilve/AECHome.html)；[可检索书稿](https://faculty.kashanu.ac.ir/file/download/course/1666448140-the-arithmetic-of-elliptic-curves-silverman.pdf)。
2. **Silverman (1994), `Advanced Topics`, Theorem IV.10.4：精确匹配。** 对 $K=\mathbb Q_2$，
   $$
   f_2\le2+3v_2(3)+6v_2(2)=8.
   $$
   [作者书页](https://www.math.brown.edu/johsilve/ATAECHome.html)。
3. **Murty–Pasten (2013), Theorem 5.1：精确支持 $h_\Delta\ne h_F$。** 其公式含随曲线变化的 Archimedean 项。[作者预印本](https://people.math.harvard.edu/~hpasten/preprints/modabcJNT.pdf)；[期刊页](https://www.sciencedirect.com/science/article/pii/S0022314X13001583)。
4. **Löbrich (2017), Proposition 3.1：相关但非直接匹配。** 它比较 Faltings 高度、$j$-高度和 unstable discriminant，并不直接陈述 $h_\Delta-h_F$ 无统一界。宜改用 Murty–Pasten 的公式加 cusp 论证。[期刊全文](https://www.numdam.org/articles/10.5802/jtnb.980/)。
5. **Stein–Watkins (2002), Tables 2–3：可用于数值锚点。** 它不替代一般导子界的证明。[原文](https://wstein.org/papers/stein-watkins/ants.pdf)。

## 修正版普通数学证明

### A. rad

令

$$
\operatorname{Supp}(n)=\{p:\ p\text{ 为素数且 }p\mid|n|\},\qquad
\operatorname{rad}(n)=\prod_{p\in\operatorname{Supp}(n)}p.
$$

唯一分解定理表明：符号不改变支集；$\pm1$ 的支集为空；$p^k$ 的支集是 $\{p\}$；互素整数的支集是不交并。因此 rad 的三项性质全部成立。

**普通数学：CLOSED。形式化交付：OPEN。** 附件没有实现、类型规格、终止性证明、证明对象或内核输出。

### B. 判别式高度

对

$$
E:y^2=x(x-a)(x+b)=x^3+(b-a)x^2-abx
$$

有

$$
\begin{aligned}
a_1&=a_3=a_6=0,& a_2&=b-a,& a_4&=-ab,\\
b_2&=4(b-a),& b_4&=-2ab,& b_6&=0,& b_8&=-a^2b^2,\\
c_4&=16(a^2+ab+b^2).
\end{aligned}
$$

并且

$$
\begin{aligned}
\Delta_W
&=-b_2^2b_8-8b_4^3\\
&=16a^2b^2\bigl((b-a)^2+4ab\bigr)\\
&=16(abc)^2.
\end{aligned}
$$

Silverman Lemma VIII.11.3 给出

$$
|\Delta_{\min}|
\in\{16(abc)^2,\;2^{-8}(abc)^2\}.
$$

所以

$$
h_\Delta(E)
\le\frac16\log(abc)+\frac13\log2.
$$

$(1,8,9)$ 的原模型全局最小并取等，故常数紧。

此外，对 $(1,2n,2n+1)$，

$$
\log|\Delta_{\min}|-2\log c
\ge2\log n-6\log2\longrightarrow\infty,
$$

故不存在统一常数 $C$ 使 $\log|\Delta_{\min}|\le2\log c+C$。

### C. 导子

若奇素数 $p\mid abc$，互素性保证 $p$ 只整除 $a,b,c$ 中一个，且

$$
a^2+ab+b^2\not\equiv0\pmod p.
$$

具体地，$p\mid a$、$p\mid b$、$p\mid c$ 三种情形分别余 $b^2$、$a^2$、$a^2$。故这些奇素数处均为乘法约化，$f_p=1$；不整除 $2abc$ 的素数处为良约化。

于是

$$
N_E=2^{f_2}\prod_{\substack{p\mid abc\\p\text{ odd}}}p.
$$

Theorem IV.10.4 给出 $f_2\le8$。又因 $a,b,c$ 中恰有一个偶数，

$$
\prod_{\substack{p\mid abc\\p\text{ odd}}}p=\frac R2.
$$

所以

$$
N_E=2^{f_2}\frac R2\le2^7R,\qquad
\log N_E\le\log R+7\log2.
$$

### D. $q>1$

取 $(1,8,9)$。有 $R=\operatorname{rad}(72)=6$。因 $9>6>1$，

$$
q(1,8,9)=\frac{\log9}{\log6}>1.
$$

### 奇偶限制可删除

若 $a,b$ 一奇一偶，则 $a^2+ab+b^2$ 为奇数；若二者均奇，三个加数均奇，其和仍为奇数。因此所有互素 abc-triple 都有 $v_2(c_4)=4$。Silverman Lemma VIII.11.3 本身也无奇偶假设。导子证明中“$a,b,c$ 恰有一个偶数”同样覆盖 both-odd 情形，此时偶数是 $c$。

**所以 B、C 对全部正整数互素 abc-triple 成立，无须另开 both-odd 分支。**

## 数值锚点

对 $(1,8,9)$：

| 项目 | 独立值 | 判定 |
|---|---:|---|
| $abc$、$R$ | $72=2^3\cdot3^2$，$R=6$ | 正确 |
| $c_4$、$c_6$ | $1168$，$-38080$ | 正确 |
| $\Delta_{\min}$ | $82944=2^{10}\cdot3^4$ | 正确 |
| $h_\Delta$ | $0.943826746689324322\ldots$ | 正确 |
| 高度上界右端 | 同上 | 原稿 $0.9415$ 错；实际取等 |
| $N_E$ | $48=2^4\cdot3$ | 正确 |
| $q$ | $1.226294385530916826\ldots$ | 正确 |
| LMFDB $h_F$ | $-0.2987786957998846\ldots$ | 正确 |

原方程经 $x=X-2$ 变成 [LMFDB 48.a3](https://www.lmfdb.org/EllipticCurve/Q/48.a3/) 的最小方程

$$
y^2=X^3+X^2-24X+36.
$$

Stein–Watkins 表中，$c_4/16=73$、$c_6/32=-1190$ 的模 $8$ 类是 $(1,2)$，Table 2 转入 `e`；模 $16$ 类是 $(9,10)$，Table 3 给出 $f_2=4$。

以下是可重复的算术检查器；它不是形式化证明：

```python
from decimal import Decimal, getcontext
from math import gcd

getcontext().prec = 50
D = Decimal
a, b, c = 1, 8, 9
abc = a*b*c
c4 = 16*(a*a + a*b + b*b)
Delta = 16*abc*abc

assert gcd(a, b) == 1 and a + b == c
assert abc == 72 and c4 == 1168
assert Delta == 82944 == 2**10 * 3**4
lhs = D(Delta).ln()/12
rhs = D(abc).ln()/6 + D(2).ln()/3
assert abs(lhs-rhs) < D("1e-45")
assert D(9).ln()/D(6).ln() > 1
assert 48 > 6**2
assert 3249 == 3**2 * 19**2
assert 57 != 2*3*19
```

## 非循环性

- **abc / Szpiro：PASS。** Silverman Lemma VIII.11.3 虽位于讨论 Szpiro 与 ABC 的章节，但引理本身只用 Weierstrass 不变量、积分变量替换、整除性和互素性；书中是在引理之后才将其用于 Szpiro。
- **IUT：PASS。** 未出现，也未通过等价命题使用。
- **RH / ζ 零点：PASS。** 没有使用 RH、RH 等价命题或 ζ 零点位置。
- **Faltings 高度：PASS。** 只用于术语和数值对比，不是 B、C 的前提。

## 作者修订清单

1. 无机器工件时采用 `PARTIAL-FORMALIZATION`，不要采用原定义的 `COMPLETE`。
2. 修正高度锚点并说明精确取等。
3. 分开两个旧命题的反例：$(1,8,9)$ 反驳整除命题，$(3,16,19)$ 反驳 rad 等式。
4. 新增封闭的“允许引用的前置结果”清单。
5. 若保留 “formally verified”，提交实际工件、版本、运行命令、依赖和期望输出；否则降为 “rigorously proved with executable sanity checks”。
6. 删除 B、C 的不必要奇偶限制。
7. Löbrich Proposition 3.1 不单独承担无界差项结论；改用 Murty–Pasten Theorem 5.1 加 cusp 论证。

> **最终结论：`COMPLETE-MATH` after corrections；`PARTIAL-FORMALIZATION` as submitted；无循环性问题。**
