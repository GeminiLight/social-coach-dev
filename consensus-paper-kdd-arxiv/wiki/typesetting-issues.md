# 排版问题清单：段落末尾短行（Short Trailing Lines）

编译日期：2026-03-12
当前状态：6 pages, 480KB

## 检测方法

用 PyMuPDF 解析 PDF，对每个 text block 的最后一行：
- 词数 ≤ 3 且宽度 < 前一行的 35% → 标记为短尾行

## 不可控（模板/结构性，无需修）

| 页 | 短尾内容 | 原因 |
|----|---------|------|
| P1 | "Consensus Layer" | 标题自动换行 |
| P1 | "XXXXXXX.XXXXXXX" | DOI 占位符 |
| P2/P4/P6 | "Anon." | anonymous 模式页眉 |
| P2 | "tuple (I,C,A,E):" | subsubsection 标题内嵌数学 |
| P4 | "subgraphs" | subsection 标题自然换行 |

## 需要修的（正文段落短尾）

### P1 — introduction.tex

1. **"trol [19]."** (13% fill)
   - 上一行: "maintain and expose the latent structure humans require for con-"
   - 来源: `agents must maintain and expose the latent structure humans require for control~\cite{seah2026memory}`
   - **plan**: 缩短前文，把 "control [19]." 拉回上一行。改 `agents must maintain and expose` → `agents must expose`，省掉 "maintain and" 约 14 字符，足够让 "for control [19]." 回流

### P3 — method.tex

2. **"artifacts."** (13% fill)
   - 上一行: "be first-class and continuously executed, not ad-hoc documentation"
   - 来源: `requires these operators to be first-class and continuously executed, not ad-hoc documentation artifacts.`
   - **plan**: 去掉 "documentation"，改成 `not ad-hoc artifacts`。"documentation" 是冗余修饰——前文已经说了跟 documentation 的对比

3. **"selective prediction."** (30% fill)
   - 上一行: "ical intervention rates, analogous to confidence-based routing in"
   - 来源: `analogous to confidence-based routing in selective~prediction.`
   - **plan**: 去掉 `~`，改 "analogous to" → "as in"。缩短约 8 字符，让 "in selective prediction." 能填满更多宽度，或者直接回流到上一行

4. **"viewable:"** (14% fill)
   - 上一行: "primitive operations that make consensus both executable and re-"
   - 来源: `make consensus both executable and~reviewable:`
   - **plan**: 去掉 "both" 和 `~`，改成 `make consensus executable and reviewable:`。省 5 字符，让 "reviewable:" 不被断词

### P4 — method.tex / casestudies.tex

5. **"and simulation."** (27% fill)
   - 上一行: `"this node, what breaks?") through dependency analysis`
   - 来源: `through dependency analysis and~simulation.`
   - **plan**: 改 `through dependency analysis and~simulation` → `by tracing dependencies and running simulations`。重写让末尾词更长，不容易被甩出

6. **"first-class in C."** (23% fill)
   - 上一行: `schema"), the system should learn to make that relation explicit and`
   - 来源: `the system should learn to make that relation explicit and first-class in $C$.`
   - **plan**: 加 `~` 绑定最后几个词：`explicit and first-class in~$C$.`。如果不够，改 "should learn to make" → "should make"，缩短约 9 字符让末尾回流

7. **"ΔA."** (6% fill) ← 最严重
   - 上一行: `dependency that violates policy), and only then commits the induced`
   - 来源: `and only then commits the induced $\Delta A$.`
   - **plan**: 改 `and only then commits the induced $\Delta A$` → `and only then commits the induced artifact diffs~$\Delta A$`。加 "artifact diffs" 把数学符号推回上一行，或者改 `commits the induced` → `commits induced`，省 4 字符让 $\Delta A$ 回流

8. **"surviving consensus."** (32% fill)
   - 上一行: `and the system proceeds with a minimal fix consistent with the`
   - 来源: `the system proceeds with a minimal fix consistent with the surviving consensus.`
   - **plan**: 改 `proceeds with a minimal fix consistent with the surviving consensus` → `proceeds with the minimal fix consistent with surviving~consensus`。`~` 绑定最后两词

9. **"dence."** (10% fill)
   - 上一行: `sented, alternatives are compared in C, and fixes are gated by evi-`
   - 来源: `fixes are gated by evidence.`
   - **plan**: 改 `and fixes are gated by evidence` → `and all fixes are evidence-gated`。用复合形容词避免 "evidence" 被断词到下一行

10. **"consensus state."** (24% fill)
    - 上一行: `and complexity of human corrections needed to reach a correct`
    - 来源: `the number and complexity of human corrections needed to reach a correct consensus state.`
    - **plan**: 改 `needed to reach a correct consensus state` → `required to reach a correct consensus~state`。"required" 比 "needed to" 少 3 字符，加 `~` 绑定

### P5 — conclusion.tex

11. **"the coming decade."** (29% fill)
    - 上一行: `consequential problems knowledge discovery systems will face over`
    - 来源: `will face over the~coming~decade.`
    - **plan**: 改 `among the most consequential problems knowledge discovery systems will face over the~coming~decade` → `among the most consequential problems knowledge discovery will face in the decade~ahead`。"in the decade ahead" 比 "over the coming decade" 短 3 字符且更紧凑

## 修复策略

每处有两种手段，按优先级：

1. **缩短前文措辞**：减少几个字符让末尾词回流到上一行（首选，不留痕迹）
2. **`~`（non-breaking space）**：绑定最后 2-3 个词不被拆行（备选，快速）

注意：改一处可能影响同页其他段落的排版，需要逐处改完后重新检测。建议从影响范围最大的页面开始改（P4 有 5 处），改完后重新编译检测。
