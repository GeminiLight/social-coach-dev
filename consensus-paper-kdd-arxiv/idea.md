# Agentic Consensus: Scaling Human-AI Coding Collaboration Requires an Explicit Consensus Layer

**目标会议:** KDD 2026 Blue Sky Track
**论文类型:** Position / Vision paper
**状态:** 四轮修订完成，编译通过（6页正文 + 参考文献，~484KB）

---

## 核心论点

AI 编程智能体能快速生成可执行代码，但产出的系统是不透明的：审查者无法判断做了哪些假设、改了什么、回归为何发生。瓶颈已从**写代码**转向**理解和控制代码**。我们称之为**表征鸿沟 (representation gap)**——系统可以通过编译和测试，却在认知上不可理解。

我们提出 **Agentic Consensus**：在人与智能体之间插入一个显式的、半结构化的**共识层 (consensus layer)**——一个以类型化属性图表示的可操作世界模型——作为工程的共享主制品。代码、配置、数据流从这个结构**派生**而来，而非反过来。

**核心金句:** "用显式的、可操作的人机共识，取代'希望 AI 理解了 vibe'。"

---

## 关键概念

### 项目状态 $(I, C, A, E)$
- **$I$** — 用户意图（部分的、隐式的、随时间变化的）
- **$C$** — 共识层（类型化属性图：模块、接口、数据实体、不变量、实验；边 = 依赖、契约、因果关系）
- **$A$** — 制品（代码、配置、数据流）—— 从 $C$ **派生**；test code 属于 $A$，test outcomes 属于 $E$
- **$E$** — 证据（测试结果、检查、执行痕迹、溯源）—— 直接链接到 $C$ 中的声明

### 同步算子
- **$\Phi: (C, A) \rightarrow A'$**（realize / 实现）—— 基于当前制品基线 $A$，将共识变更增量编译为制品 diff
- **$\Psi: (A, C) \rightarrow C'$**（rehydrate / 回溯重建）—— 从制品 diff 推断/更新共识结构；歧义时产生多假设候选
- **Round-trip consistency（往返一致性）** — $\Psi(\Phi(C,A)) \approx C$ 作为软约束，持续测量结构漂移，超阈值报警

### 共识熵 $\mathcal{H}(C \mid I)$
量化在模糊意图下可行共识状态的不确定性（概念性记号，非严格 Shannon 熵——$I$ 是非形式化的）。**分级响应机制**：低熵自动处理 → 中熵暂定提交+异步审查 → 高熵暂停请求人类澄清。

### 维度坍缩 (Dimension Collapse)
复杂系统拓扑被压扁为聊天记录和 diff 的过程。这是 Agentic Consensus 要解决的根本问题。

---

## 论文结构

1. **Introduction** — 以第二人称 vibe coding 体验开头（你输入 prompt → agent 返回 200 行 diff → 你凭直觉点 Merge → 三个月后回归无法溯因）。定义 vibe coding（引 Karpathy 2025），识别表征鸿沟和维度坍缩，提出论点，列出四个贡献。

2. **Related Work**（3 段）：
   - 结构化制品与双向视图（Knuth, xKG, CGBridge, Agint [code-level], bx transformations）
   - 安全、治理与多智能体协作（形式化方法, SAFE-AI, AIDev, MetaGPT, ChatDev, Agentsway, survey）
   - 人机协作编程基准（FeatureBench, HAI-Eval）

3. **The Shared Consensus Layer**（核心技术章节）：
   - 结构基础（以 $C$ 为中心）：项目状态元组与 $C$ 的中心地位、$C$ 的表示（类型化属性图 + 证据链接）、$C$ 的性质（可操作世界模型）
   - 操作动力学：交互动作、$\Phi$/$\Psi$ 算子（含往返一致性约束）、歧义分级响应、原语操作（Propose → Validate → Commit/Rollback → Explain）
   - 自主智能体编排：四角色流水线（Architect / Builder / Auditor / Navigator）、agent-agent 共识、专家引导演化（expert-guided evolution）

4. **Case Study Sketches**（精简版，去掉了 baseline 对比段落）：
   - 带契约的特征流水线重构（Setup → Consensus move → Realization move → Validation）
   - 通过竞争性因果子图调试回归（Setup → 多假设 → Clarification → Resolution）

5. **Evaluation Framework**（4 段 prose）：
   - 对齐保真度 $\mathcal{F}(I,C,A)$
   - 共识熵 $\mathcal{H}(C \mid I)$
   - 认知负荷与干预距离
   - 基准设计（任务族 + 外部验证协议）

6. **Discussion**：
   - **Alternative Views**（4 条 steelman 反驳，降为 subsection）
   - **Limitations**：开销、设计僵化、隐私风险；证据 $E$ 的不可靠性（flaky tests, noisy traces）；遗留代码库增量引导；大型 monorepo 子图分治；推广到知识发现系统

7. **Conclusion** — 认识论层面的收尾：当 AI 生成速度超过人类检查速度，正确的监督单元是**结构性声明**，而非代码行。

---

## 四个贡献

1. **共识层形式化** — 结构化世界模型 $C$ 作为主制品；共识作为连接模糊意图与具体制品的结构化潜变量
2. **双向同步算子** — $\Phi$（realize）和 $\Psi$（rehydrate），附带往返一致性软约束、证据链接和显式不确定性
3. **评估框架** — 将关注点从生成质量转向对齐与控制（对齐保真度、共识熵、干预距离、认知负荷）
4. **基准设计** — 共识驱动工作流 vs. 聊天驱动基线；衡量可审查性和人类干预减少程度

---

## 多智能体角色

| 角色 | 职责 |
|------|------|
| **Architect** | 意图 → 结构/不变量 |
| **Builder** | 结构 → 代码/配置 |
| **Auditor** | 运行检查、挂证据、标记冲突 |
| **Navigator** | 选择视图和布局，降低认知负荷；将竞争性 $\Delta C$ 摘要为自然语言+受影响路径+预测测试结果 |

---

## KDD 主题定位

- **知识发现:** 共识层作为软件系统上的结构化知识表示
- **可扩展 AI:** 解决 AI 生成速度超过人类审查速度时的信任-效用鸿沟
- **人机交互:** 将协作重构为协商结构性声明，而非审查 diff

---

## 关键参考文献

| 参考文献 | 定位 |
|---------|------|
| Agint (Chivukula 2025) | code-level typed DAG；本文提升到 full project state $(I,C,A,E)$，加证据链接和不确定性 |
| CGBridge (Chen 2025) | 代码属性图 + LLM → 支持"结构表征提升可控性"的前提 |
| xKG (Luo 2025) | 可执行知识图谱 → 验证"证据作为一等图"原则的可行性 |
| AIDev (Li 2025) | 45.6 万条智能体 PR，接受率更低 → 驱动可审查性指标 |
| SAFE-AI (Navneet 2025) | 分层安全实践 → $C$ 作为策略执行的架构基底 |
| FeatureBench (Zhou 2026) | 多提交特征开发仅 11%（SWE-bench 74%）→ 驱动 beyond-pass@k 评估 |
| HAI-Eval (Luo 2025) | 协作必需型任务 → 与干预距离指标兼容 |
| Agentsway (Bandara 2025) | 智能体生命周期方法论 → 驱动显式 agent-agent 共识 |
| Agentic SE Survey (Guo 2025) | 50+ 基准 → 多智能体协调的全景定位 |

---

## Review 反馈与修订记录

### Review 1（Gemini 3.1 Pro，模拟 ICML 2025 Position Track）
**总评:** 4 Accept | Significance 4/5 | Discussion Potential 4/5 | Argument Clarity 4/5

已修复：
| 弱点 | 修订 |
|------|------|
| W1. $\Phi$/$\Psi$ 形式化不够 | method.tex 新增 "Round-trip consistency" 段：$\Psi(\Phi(C,A)) \approx C$ 作为软约束 |
| W2. 高熵告警疲劳 | method.tex 新增 "Graduated response to ambiguity" 段：三级响应机制 |
| W4. 遗留代码库不适用 | discussion.tex 新增 "Bootstrapping on legacy codebases" 段 |
| W6. 图 diff 对人认知负担大 | method.tex Navigator 角色补充摘要式呈现策略 |

未修复（无需改）：
- W3（缺实证表格）— Position paper 不需要 results table
- W5（缺 3 篇文献）— AI 审稿推荐的论文可能是幻觉，边缘相关

### Review 2（同工具，第二轮）
与 Review 1 大量重叠（round-trip consistency、bootstrapping、缺表格、缺文献），新增两个有价值的点：

已修复：
| 弱点 | 修订 |
|------|------|
| 证据 $E$ 本身不可靠（flaky tests, noisy traces） | discussion.tex Limitations 补充：$E$ 附带置信度权重，矛盾证据作为 $C$ 中显式不一致暴露 |
| 属性图对大型 monorepo 的可扩展性 | discussion.tex 新增 "Scaling to large codebases" 段：模块化子图分治，agent 操作局部视图 |

未修复（无需改）：
- 缺 mock results table — 同 Review 1 W3
- 缺 3 篇文献 — 同 Review 1 W5，AI 推荐文献不可靠

### 第三轮修订（格式与排版）

| 修改项 | 说明 |
|--------|------|
| abstract `\emph{Agentic Consensus}` → `\textbf` | 统一为粗体（系统名首次提出），与 intro 一致 |
| agent role taglines 去掉 | method.tex Architect/Builder 条目末尾的 ``what should exist?'' / ``make it real'' 去掉，角色描述本身已足够 |
| `\emph` 清理 | 全文从 ~30 处减至 ~18 处，仅保留首次术语引入和真正对比强调 |
| 引号 `` '' 清理 | 去掉不必要的双重标记（如 abstract 里 "vibe coding" 已有 `\emph` 又加引号） |
| `\textbf` | 检查全文，均为 list header 标准用法，无需改 |
| microtype | 加 `\PassOptionsToPackage{stretch=10,shrink=25}{microtype}`，改善字间距紧凑度 |
| `\setlist{nosep}` | 全局去掉列表额外间距 |
| 浮动体/caption 间距 | 缩小 `\textfloatsep`、`\intextsep`、`\abovecaptionskip`、`\belowcaptionskip` |
| 短尾行修复 | 用 PyMuPDF 检测段落末尾 ≤3 词且宽度 <35% 的行，通过 `~` 和微调措辞修复多处（详见 `wiki/typesetting-issues.md`，剩余 11 处待修） |
| Intro 重写为第二人称 vibe coding 体验 | 原开头是第三人称 "A user asks..."，太抽象。改为 "You type a prompt... you scan... you click Merge"，让 reviewer 直接代入日常 vibe coding 体验；定义了 vibe coding（"approve based on vibes---surface plausibility rather than structural understanding"）；Karpathy cite 移到场景段 |

### 第四轮修订（逻辑审查修复）

| 修改项 | 说明 |
|--------|------|
| "bi-directional isomorphism" → "correspondence" | method.tex 段落标题与正文矛盾（标题说 isomorphism，正文说 soft invariant），改为 correspondence |
| $\mathcal{H}(C \mid I)$ disclaimer | evaluation.tex 加一句说明：条件熵记号是概念性简写，$I$ 是非形式化的，$\mathcal{H}$ 是设计层面的度量而非严格 Shannon 量 |
| tests ∈ $A$ vs ∈ $E$ 边界澄清 | method.tex 定义段去掉 $A$ 括号里的 "tests"，新增一句区分 test code ∈ $A$ vs test outcomes ∈ $E$ |
| $\Phi$ 输入理由 | method.tex $\Phi$ 定义处加 "given the current artifact baseline $A$"，说明需要 $A$ 是因为增量编译 |
| agent 内部表征约束 | method.tex "higher-bandwidth" → "richer internal representations (e.g., embedding similarities, execution traces)"，加 "must be projected back into $C$ before committed" 堵住绕过 $C$ 的漏洞 |
| abstract 术语对齐 | "adaptive representation learning" → "expert-guided evolution"，与正文语义匹配，不再引发 ML 机制预期 |
| method.tex 段落拆分 | "Agent--agent consensus and self-evolving protocols" 拆为两个独立段落："Agent--agent consensus" + "Expert-guided evolution" |
| related-work.tex 用词 | "retrospective learning" → "iterative refinement"，更直白 |
