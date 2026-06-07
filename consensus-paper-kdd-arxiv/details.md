# 论文逐节详审：Scaling Human-AI Coding Collaboration Requires an Explicit Consensus Layer

**投稿:** KDD 2026 Blue Sky Track | **格式:** ACM sigconf

---

## 0. 标题与摘要

**标题:** Scaling Human-AI Coding Collaboration Requires an Explicit Consensus Layer

**摘要内容:**
- AI 辅助开发能快速生成可执行代码，但生成的系统往往不透明：reviewer 无法确定做了什么假设、改了什么、为什么出现 regression。
- 提出 **Agentic Consensus**：人和 agent 通过一个共享的 consensus layer（typed property graph）协作，该层作为工程的 primary artifact。
- 可执行产物从该结构派生；关联证据使每个结构性声明可审计。
- 使 under-specification 显式化；支持因果 "what-if" 推理；解决 vibe coding 的 **dimension collapse**。
- 概述技术基础：round-trip 同步算子、多 agent 协同流水线、自适应表示学习。
- 评估指标：alignment fidelity、consensus entropy、intervention distance、cognitive load reduction。

---

## 1. Introduction

### 1.1 开场情境 (L1-6)
> 你输入 "speed up feature computation and make it reproducible" → agent 返回 200 行 diff → 测试通过 → 合并 → 3 个月后在某个 demographic slice 出现 regression → 没人能解释原因。

- **论点:** 这就是 **vibe coding** [Karpathy 2025] — 基于表面合理性而非结构性理解来审批。

### 1.2 核心诊断 (L8-11)
> 不是生成失败，是 **控制** 失败：系统在生成的瞬间就变得不透明。

- **论点:** 瓶颈从写代码转向理解和控制代码 [Peng 2023, Vaithilingam 2022]。
- Reviewer 无法确定：假设了什么不变量、引入了什么依赖、正确性的证据是什么。
- 根因：**primary artifact 中没有任何东西编码了这个结构**。

### 1.3 Representation Gap 与 Dimension Collapse (L13-19)
> 系统可以是可执行的、能通过 benchmark，但在认知上不可达。

- **引入术语:** **representation gap**（表示鸿沟）
- 团队的应对方式是加流程开销（ticket、文档、review 仪式）— 但这些是结构缺陷的外部补丁。
- 根因：code + chat history 执行了 **dimension collapse** — 复杂拓扑被压平为低维文本。
- 三个 "does not fix this"：更好的 NL 接口、更强的模型、更丰富的 IDE 功能。
- **论点:** collapse 是 **架构性的** — 流水线中没有地方存放系统结构知识，于是每一步都丢弃了。

### 1.4 提出的方案：Agentic Consensus (L21-26)
> 用 **显式的、可操作的共识** 替代 "希望 AI 理解了 vibe"。

- 核心动作：插入一个 **consensus layer**（typed property graph）作为共享的 primary artifact。
- 可执行产物从中派生；双向对应；证据使声明可审计。
- 编程被重新定义为：协商并验证结构知识。
- 目标：不是 "能编译的代码"，而是 **"我们达成共识的结构"**。
- 假设：下一个接口进步是 **knowledge-first** [Seah 2026]。

### 1.5 贡献 (L28-35)
1. 共享 consensus layer 形式化：结构化世界模型 $C$ 是 primary artifact，$A$ 从中派生 — consensus 作为结构化隐变量，调解模糊意图与具体产物之间。
2. 双向同步算子：realize $\Phi$ 和 rehydrate $\Psi$，带有证据链接和显式不确定性。
3. 评估框架：从生成质量转向 alignment 和 control（alignment fidelity、consensus entropy、intervention distance、cognitive load reduction）。
4. Benchmark 设计：衡量 consensus-based 工作流是否比 chat-driven baseline 改善可审性、减少人工干预。

---

## 2. Related Work

### 2.1 结构化产物与双向视图 (L4-7)
- **文学编程** [Knuth 1984]：程序作为解释，内含可执行子结构。
- **Executable Knowledge Graphs (xKG)** [Luo 2025]：概念节点配对可运行代码片段，实现可验证复制。
- **UML 风格**图表：工程师用图推理，但视图通常是说明性的，不是同步的。
- 需要 **双向一致性** [Czarnecki 2009]。
- **Code property graphs** [Yamaguchi 2014] 桥接到冻结的 LLM [Chen 2025]，带 round-trip 编辑的 typed code DAG [Chivukula 2025] — 显式图表示可度量地改善语义保真度 → 支撑 $\Phi$/$\Psi$ 算子的可行性。

### 2.2 安全、治理与多 agent 协调 (L9-12)
- **形式化方法** [Clarke 1999]：显式状态模型 → 可扩展保证。
- **SAFE-AI** [Navneet 2025]：LLM 辅助 SE 的安全/可审计/可解释性实践。
- **AIDev** [Li 2025]：456K agent PR 的接受率显著低于人类 → **trust-utility gap** [Lee 2004]。
- **经典软件风险** [Brooks 1975]；多 agent SE 框架 [MetaGPT, ChatDev, Agentsway, Guo survey] 通过消息协议维持一致性，而非共享结构产物。

### 2.3 人-AI 编码 Benchmark (L14-16)
- **SWE-bench** [Jimenez 2024]：聚焦单 PR 修复，低估现实复杂性。
- **FeatureBench** [Zhou 2026]：多 commit feature 上仅 11% vs. SWE-bench 上 74% → 需要超越 pass@k 的评估。
- **HAI-Eval** [Luo 2025]："Collaboration-Necessary" 任务，跨干预层级度量人-AI 协同 → 与 intervention-distance 和 cognitive-load 指标兼容。

---

## 3. The Shared Consensus Layer（方法）

### 3.1 结构基础

#### 3.1.1 项目状态 $(I, C, A, E)$
| 符号 | 含义 |
|------|------|
| $I$ | 用户意图 — 可能是局部的、隐式的、随时间变化的 |
| $C$ | Consensus layer — schema + graph + 同步视图 |
| $A$ | 已实现产物 — 代码、数据流、配置 |
| $E$ | 证据 — 测试、检查、trace、provenance |

- 测试 **代码** → $A$（可执行产物）；测试 **结果**（pass/fail、覆盖率、执行 trace）→ $E$。
- **关键设计选择：** $C$ 是人类审查和修改的对象；$A$ 是编译/实现的结果。

#### 3.1.2 Consensus 作为可操作的世界模型
- Agent 在 $C$ 中操纵结构、运行依赖分析、评估反事实 — **在动代码之前**。
- 示例查询："如果我删除这个节点，哪些依赖会断？"
- 不确定性 → consensus entropy 升高（不是静默猜测）。

#### 3.1.3 $C$ 作为多模态 typed property graph
- 不是单一图表 — 是 typed、可查询的 schema，有多个同步投影。
- 节点：模块、接口、数据实体、不变量、实验。
- 边：依赖、合约、因果/时序关系。

**[图 1：Agentic Consensus 架构]**
```
Intent I  ──提议/澄清──▶  Consensus Layer C  ──Φ realize──▶  Artifacts A
   ▲                        (typed property graph,                │
   │                         schema + 同步视图)                    │
   │                               │                              ▼
   └──审查/提交/回滚──◀            │                        Evidence E
                                   ▼                        (测试、检查、
                            多模态投影                        trace、provenance)
                            (拓扑、血缘、                         │
                             实验、合约、                         │
                             因果路径)                   ◀──link──┘

                      ◀──────Ψ rehydrate（虚线）──────────────┘
```
- 区别于 UML/notebook：(i) round-trip $\Phi$/$\Psi$ 算子；(ii) 证据关联的声明；(iii) entropy 驱动的澄清。

#### 关键要求：双向对应
- **结构映射：** 节点 → 代码单元、配置块、数据集定义、流水线阶段。
- **行为映射：** 边 → 显式调用点、API 合约、数据血缘、可测试不变量。
- **Round-trip 完整性：** $C$ 的变更编译为 $A$ 的编辑；$A$ 的变更通过静态分析、运行时 trace、provenance 日志反向灌入 $C$。

#### 上下文感知的视图合成
- 给定用户查询（"为什么这个指标在 slice S 上下降？"），合成任务特定的投影：依赖切面、因果链、实验矩阵、故障模式拓扑。
- 通过保留图结构但仅展示相关的任务特定子流形来防止 dimension collapse。

#### 3.1.4 证据作为一等公民图
- 证据直接链接到 $C$ 中的声明（不只是 PDF/日志）。
- 示例：边 "数据集 D 符合 schema S" 有指向验证作业及其时间戳的指针。
- 分歧变为可行动的："这个声明当前缺乏证据。"

### 3.2 运行动力学

#### 3.2.1 交互动作
两种动作类型交替进行：
1. **Consensus 动作：** 在 $C$ 中提议/修改结构（实体、依赖、不变量、实验图）。
2. **Realization 动作：** 编辑 $A$ 中的产物并将对应结构 rehydrate 回 $C$。

由同步算子耦合；必须保持 round-trip 完整性并更新证据链接。

#### 3.2.2 同步算子 ($\Phi$, $\Psi$)
| 算子 | 签名 | 含义 |
|------|------|------|
| $\Phi$（realize） | $(C, A) \rightarrow A'$ | 给定当前产物基线 $A$，将提议的 consensus 变更编译为增量 diff |
| $\Psi$（rehydrate） | $(A, C) \rightarrow C'$ | 从观察到的产物 diff 推断/更新 consensus 结构 |

- $\Psi$ 实际实现：静态分析 (AST/CFG) [Yamaguchi 2014]、动态不变量检测 [Ernst/Daikon 2007]、数据血缘/provenance、测试结果。
- **Blue Sky 假设：** 健壮的人类控制要求 $\Phi$/$\Psi$ 是一等的、持续执行的算子，不是临时文档产物。

**Round-trip 一致性：**
- 理想：$\Psi(\Phi(C, A)) \approx C$
- 现实：严格相等不可达（$\Phi$ 可能丢弃没有产物对应的结构信息；$\Psi$ 是欠定的）。
- 作为 **软不变量** 处理：持续度量结构漂移 $d(C, \Psi(\Phi(C,A)))$，超过阈值则报警。
- 这种放松对增量采纳至关重要。

**处理 $\Psi$ 中的歧义：**
- 一行代码变更可能隐含 3+ 种不同的 consensus 更新（修改不变量、新增依赖边、变更数据合约）。
- $\Psi$ 应该是 **多假设** 的：产生 $\{\Delta C_1, \Delta C_2, \Delta C_3\}$，附带预测的下游后果和不确定性分数。
- 选择策略：(a) 优先选与 $C$ 和 $E$ 中现有约束一致的候选；(b) 尝试廉价区分性检查；(c) 不确定性仍高 → 提升为显式人类决策。
- 歧义 rehydration 增加 $\mathcal{H}(C|I)$ → 触发澄清，而非静默重新解释。

**对歧义的分级响应：**
| 熵水平 | 系统响应 |
|--------|---------|
| 低 | 自动选择最高置信候选，记录决策 |
| 中 | 暂时提交，在 $C$ 中标记为 under-specified，安排异步审查 |
| 高 | 暂停流水线，请求针对性人类澄清 |

- 阈值按项目从历史干预率校准（类似 selective prediction 中的 confidence-based routing）。

#### 3.2.3 原始 consensus 操作
| 操作 | 描述 |
|------|------|
| **Propose** | Agent 提议变更 $\Delta C$，附带理由和预测的下游 diff $\Delta A$ |
| **Validate** | 附加检查（类型/schema 验证、单元测试、静态分析、数据合约）→ 结果记录为证据 |
| **Commit/Rollback** | 人类在 $C$ 层面接受/拒绝（结构化 diff）；可检查诱导的 $\Delta A$ 用于审计和信任校准 |
| **Explain** | 回答反事实（"如果我删除这个节点，什么会断？"）通过依赖分析和模拟 |

### 3.3 自主 Agentic 编排

#### 3.3.1 协调的多 agent 流水线
| Agent 角色 | 功能 | 映射到原始操作 |
|-----------|------|---------------|
| **Architect** | 意图 → 候选结构 + 不变量 | Propose |
| **Builder** | 与 $C$ 一致的代码/配置变更 | Propose |
| **Auditor** | 生成/运行检查；标记不一致为 $C$ 中的显式冲突 | Validate |
| **Navigator** | 选择最小化当前任务认知负荷的视图和布局 | Explain |

Commit/Rollback 始终是 **人类决策**。

#### Agent 间 consensus 与自演化协议
- Agent 之间用更丰富的内部表示协商（embedding 相似度、执行 trace），但每个协商结果必须在提交前投影回 $C$；面向用户的 source of truth 始终是 $C$。
- 冲突解决：呈现竞争的 $\Delta C$ 备选方案及其预测后果（不是静默合并代码 diff）。
- 原始图 diff 认知代价高 — navigator 必须将每个备选方案精炼为任务相关摘要：自然语言理由、受影响路径、预测测试结果；完整结构 diff 按需可用。
- 长期演化：从交互 trace 中挖掘能减少 **human intervention distance** 的表示（例：如果某类故障反复需要人类画同一条缺失的边，系统应学会将该关系显式化为 $C$ 中的一等公民）。

---

## 4. Case Study Sketches

### 4.1 重构带合约的 feature pipeline

| 步骤 | 类型 | 动作 |
|------|------|------|
| 设置 | — | Pipeline：原始日志 → feature → 与 label join。用户："让它更快、可复现，别破坏隐私策略。" |
| 动作 1 | Consensus | 在 $C$ 中具现化血缘图：sources、transforms、joins、sinks。附加合约：schema 不变量、确定性约束、隐私约束（禁止的 join、保留窗口）。 |
| 动作 1 | Realization | Builder 提议 $\Delta A$（缓存、分区、重新路由 join）+ $\Delta C$（更新血缘图中的新依赖）。 |
| 验证 | Evidence | Auditor 附加 $E$：合约检查、已知 slice 上的回归测试、provenance 断言（"这两次运行在固定 seed 和 snapshot ID 下相同"）。 |
| 决策 | Human | 在 $C$ 层面批准/拒绝（例：否决违反策略的依赖）→ 然后提交诱导的 $\Delta A$。 |

### 4.2 通过竞争因果子图调试 regression

| 步骤 | 类型 | 动作 |
|------|------|------|
| 设置 | — | 模型在某 demographic slice 上性能下降。Agent 能快速生成修复，风险 = 静默错误归因。 |
| 动作 1 | Consensus | 在 $C$ 中生成两个竞争因果子图：(A) 数据偏移解释（schema 漂移 + 缺失值）；(B) 训练配置解释（正则化变更 + 早停）。每个备选列出所需的区分性证据。 |
| 澄清 | Entropy 驱动 | $\mathcal{H}(C|I)$ 高 → agent 请求一条缺失信息："上次正常运行的 dataset snapshot ID 有吗？" |
| 解决 | Evidence | Snapshot 比较测试被附加 → 一个因果子图被否决 → 按存活 consensus 执行最小修复。 |

**这些 case study 展示了什么：**
- 不确定性被显式表示；备选方案在 $C$ 中比较；修复以证据为门控。
- 可度量：alignment fidelity、consensus entropy、intervention distance。

---

## 5. 评估框架

四个互补指标（超越 pass@k）：

### 5.1 Alignment fidelity $\mathcal{F}(I, C, A)$
- 当 $C$ 在正确的抽象层级显式化意图时增加。
- $C$ 是可预测的（reviewer 能预测下游后果）。
- 有关联证据支撑。
- **操作化方式：** 人工标注、反事实问题（"reviewer 能预测什么会断吗？"）、事后归因分析。

### 5.2 Consensus entropy $\mathcal{H}(C | I)$
- 量化给定当前意图下可行 consensus 状态的不确定性。
- 条件熵记号作为结构歧义的 **概念简写**（不是字面的 Shannon 量，因为 $I$ 是非形式化的/局部的）。
- 高 $\mathcal{H}$ = 从执行切换到澄清的信号。

### 5.3 认知负荷与 intervention distance
- 度量：人类通过 $C$ 理解复杂系统是否比阅读原始产物更快？
- 理论基础：认知负荷理论 [Sweller 1988]、common ground [Klein 2005, Siemon 2022, Pokorny 2025]。
- **Intervention distance：** 达到正确 consensus 状态所需的人类修正次数和复杂度。

### 5.4 Benchmark 设计
面向 consensus-based 工作流的任务族：
| 任务族 | 成功标准 |
|--------|---------|
| Refactor-with-invariants | 在保持合约的前提下重构 |
| Failure localization | 用真实因果路径更新 $C$ |
| Experiment design | 在 $C$ 中表示并验证消融实验计划 |
| Governance tasks | 实施策略变更（成功需要正确结构，不仅是测试通过） |

- 外部验证：FeatureBench 多 commit 任务 [Zhou 2026] + HAI-Eval 协作协议 [Luo 2025]。

---

## 6. Discussion

### 6.1 备选观点（反对意见与回应）

#### "更好的模型不需要 consensus layer 就能解决这个问题。"
- **回应：** 问题是 **人类可读性**，不是模型能力。即使一个完美模型静默维护正确的内部世界模型，也无法提供人-AI 协作所需的透明度、可审计性和治理。Consensus layer 是人类行使有意义控制的接口，与模型质量无关。更好的模型 → $C$ 更容易维护，而非不需要。

#### "维护 $C$ 引入了不可承受的开销。"
- **回应：** 开销是 **前置的且可摊销的**。维护 $C$ 的成本每次变更支付一次；从不透明产物重建结构理解的成本反复支付（调试、审计、入职、合规）。"逃生舱" 设计原则处理开销不合理的常规变更。

#### "这就是多了几步的文档。"
- **回应：** 三个区别：(i) $C$ 是 **primary artifact**，不是次要记录；(ii) 通过 $\Phi$/$\Psi$ 双向一致 — 不可能在不被检测的情况下过时；(iii) **可操作的** — agent 在其上推理、模拟、门控变更。区别是：插图 vs. 工具。

#### "基于图的表示对动态、探索性工作来说太脆弱。"
- **回应：** 承认这是真实顾虑。不适用于所有工作流。**增量可采纳：** 从部分的、低置信度结构开始，随项目稳定而收紧。高 consensus entropy = **不要** 施加结构的信号。

### 6.2 局限性

- 开销、设计固化、潜在知识泄露 → 访问控制、脱敏/摘要化、逃生舱。
- Agent 可能 **幻觉结构** → 作为高熵区域可见；被所需证据阻止。
- 证据本身不是无误的（flaky test、noisy trace、false positive）→ 证据链接上的置信权重；矛盾证据在 $C$ 中作为显式不一致浮现。

#### 遗留代码库的引导
- 大型遗留系统的完全 rehydration 不可行。
- **增量路径：** $\Psi$ 先构建覆盖关键模块（入口点、公共 API、已知不变量）的部分、低置信度 $C$ → 随工程师交互逐步扩展覆盖范围。未覆盖区域显式标记为高熵区。

#### 大型代码库的扩展
- $C$ 不需要是单一的整体图。**模块化子图分区**，按包/服务边界切分。
- 每个 agent 操作本地视图；跨模块依赖通过边界接口（公共 API、共享 schema）中介。
- 映射组织所有权模式；减少图查询延迟 + LLM 上下文压力。

#### 更广泛的影响
- 不仅限于编码，泛化到 **任何知识发现系统** — agent 自主发现、可视化、同步隐结构以供人类监督。

---

## 7. Conclusion

- 将系统构建重新定义为在共享的、可验证的结构现实上的协作发现过程。
- 用显式的、可操作的共识替代 "希望 AI 理解了 vibe"。
- **认识论问题：** 当 AI 生成产物的速度超过人类检查速度时，人类监督的正确单位是什么？
- 回答：**结构性声明** — 显式化、链接到证据、与世界保持一致。
- 构建这一基础设施 = 知识发现系统在未来十年面临的最重大问题之一。

---

## 附录：引用地图

| Key | 论文 | 被引位置 |
|-----|------|---------|
| karpathy2025vibecoding | Vibe coding（X 帖子） | Abstract, Intro L5 |
| peng2023copilot | Copilot 生产力 | Intro L10 |
| vaithilingam2022expectation | Copilot 可用性 | Intro L10 |
| seah2026memory | Memory as governance（博客） | Intro L26 |
| knuth1984 | 文学编程 | Related Work §2.1 |
| luo2025xkg | Executable KG | Related Work §2.1 |
| czarnecki2009bidirectional | 双向变换 | Related Work §2.1 |
| yamaguchi2014cpg | Code property graphs | Related Work §2.1, Method §3.2.2 |
| chen2025cgbridge | CGBridge (CPG+LLM) | Related Work §2.1 |
| chivukula2025agint | Agint (code DAG) | Related Work §2.1 |
| clarke1999 | Model checking | Related Work §2.2 |
| navneet2025safeai | SAFE-AI | Related Work §2.2 |
| li2025aidev | AIDev (456K PRs) | Related Work §2.2 |
| lee2004trust | Trust in automation | Related Work §2.2 |
| brooks1975 | Mythical Man-Month | Related Work §2.2 |
| hong2024metagpt | MetaGPT | Related Work §2.2, Method §3.3.1 |
| qian2024chatdev | ChatDev | Related Work §2.2, Method §3.3.1 |
| bandara2025agentsway | Agentsway | Related Work §2.2 |
| guo2025agentsesurvey | Agent SE survey | Related Work §2.2 |
| arxiv2025codingagentse | SE 3.0 | Method §3.3.1 |
| jimenez2024swebench | SWE-bench | Related Work §2.3 |
| zhou2026featurebench | FeatureBench | Related Work §2.3, Eval §5.4 |
| luo2025haieval | HAI-Eval | Related Work §2.3, Eval §5.4 |
| ernst2007daikon | Daikon | Method §3.2.2 |
| sweller1988cognitive | 认知负荷理论 | Eval §5.3 |
| klein2005common | Common ground | Eval §5.3 |
| siemon2022taxonomy | AI 团队角色 | Eval §5.3 |
| pokorny2025human | Human-AI 高风险决策（博士论文） | Eval §5.3 |

### 引用风险标记
- **pokorny2025human：** 博士论文 — institution 未知，在任何学术数据库中均无法验证。**提交前必须确认或替换。**
- **seah2026memory：** 行业博客文章 — URL 返回 HTTP 403。非标准引用。作为 intro 中 "knowledge-first" 假设的唯一引用支撑偏弱。
- **karpathy2025vibecoding：** X（Twitter）帖子。非标准但作为术语溯源可接受。
- **li2025aidev 和 arxiv2025codingagentse：** 同作者（Li, Zhang, Hassan）— 两个 bib entry 指向相同 arXiv ID (2507.15003)，是同一篇论文的重复条目，需要合并。
