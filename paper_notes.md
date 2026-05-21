# SocialCoach: Personalized Social Skill Learning with RL-based Agentic Tutoring and Practice

**会议**: KDD 2026 (August 9-13, Jeju, Korea)
**作者**: Tianfu Wang (HKUST-GZ), Max Xiong (Duke), Shang Qin (Tsinghua/MSRA), Jianxun Lian (MSRA) 等
**机构**: 主要来自 Microsoft Research Asia + HKUST(GZ)
**代码**: https://github.com/GeminiLight/SocialCoach

---

## 1. 研究动机

社交技能（谈判、领导力、冲突解决、情绪调节）对个人和职业发展至关重要，但高质量培训面临专家教练稀缺、难以规模化的瓶颈。现有AI方法存在三个不足：
- 只关注孤立教育环节
- 针对特定技能，缺乏通用性
- 未形成完整教练闭环

需解决三大挑战：
1. **可扩展知识发现与结构化** — 专家知识分散在非结构化来源中
2. **个性化练习课程调度** — 静态课程无法匹配学习者异质性
3. **诊断性教练支架** — 弥合"知道-做到"鸿沟

---

## 2. 框架总览

SocialCoach 是 LLM 驱动的端到端 Agentic 辅导与练习系统，四个核心模块：
- Automated Knowledge Discovery（自动化知识发现）
- User Social Profiling（用户社交画像）
- Adaptive Practice Scheduling via RL（RL优化的自适应练习调度）
- Pedagogical Coaching Scaffolding（教学支架）

---

## 3. 语料获取流程（核心模块一）

### 3.1 知识组织框架：Theory-to-Practice 三层结构

| 类型 | 内容 | 平均字数 | 角色 |
|------|------|----------|------|
| Strategic Theory (K_t) | 抽象社交原则（"为什么"） | 149 词 | 概念理解 |
| Illustrative Case (K_c) | 具体案例（"怎么做"） | 87 词 | 桥接理论与实践 |
| Practical Scenario (K_s) | 模拟场景（"去做"） | 375 词 | 沉浸式练习 |

### 3.2 多维度语义分类

每个知识条目从三个维度标注：
- **Social Competency (CASEL)**: 5大核心能力（Self-Awareness, Self-Management, Social Awareness, Relationship Skills, Responsible Decision-Making）
- **Social Skills**: 34项细粒度技能（Communication, Empathy, Conflict Resolution, Leadership 等）
- **Scenario Context**: 7大类→26小类（Workplace, Family, Friendship, Romantic, Education, Public/Stranger, Party/Social）

### 3.3 LLM驱动的语料构建管线（五阶段）

```
书籍/论文/新闻 (200本书)
       │
       ▼
  ┌─────────────┐
  │ Extraction  │ ← Schema 引导，从非结构化文本抽取结构化条目
  │   Agent     │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ Filtering   │ ← 格式合规 + 字段完整性检查
  │   Agent     │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  Tagging    │ ← CASEL能力 + 社交技能 + 情境类型 三维标注
  │   Agent     │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ Refinement  │ ← 内容/标签修正，解决不一致性
  │   Agent     │
  └──────┬──────┘
         │
         ▼
   Knowledge Corpus K (40K+ entries in Chroma DB)
```

**数据来源**:
- Amazon Books 自助类排行榜
- BookAuthority.org 分类排名
- OpenLibrary 获取电子版
- 最终选定 200 本经典著作（如《Nonviolent Communication》《Emotional Intelligence》）

**技术栈**: Qwen3-235B 做抽取/标注/精炼，Chroma 向量数据库，Qwen3-Embedding-8B 做嵌入

**最终产出**:
- Strategic Theories: 13,298 条
- Illustrative Cases: 22,050 条
- Practical Scenarios: 5,117 条
- 总计 ~40,000+ 条

**核心设计思想**: 不让 LLM 凭空生成知识（避免幻觉），而是从权威来源中抽取和结构化，保证教学可追溯性和可靠性。

---

## 4. 用户社交画像

动态用户画像 U_t 包含：
- **个人信息 U_i**: 人口统计、性格特征、目标技能（onboarding时自报告）
- **历史行为 U_b**: 完成的场景、反思回应、参与度指标
- **能力状态 U_p**: CASEL能力和细粒度技能的 1-5 分评分向量

---

## 5. RL优化的自适应练习调度

### 5.1 Prescription-Retrieval-Adaptation 三阶段

1. **Practice Prescription**: Agent 分析学习者画像，生成练习需求（含自然语言 query + 布尔过滤条件）
2. **Candidate Retrieval**: 标签过滤 + 语义搜索双路检索，渐进式放松策略保证可检索性
3. **Context Adaptation**: 根据学习者画像个性化调整场景（选择最适合的角色等）

### 5.2 学习者模拟器

- 从 SocioVorse（百万级人口统计）和 PersonaHub（十亿级性格描述）获取数据
- Qwen3-Embedding-8B 嵌入 + MMR 采样 top-n 代表性条目
- Hungarian 算法做人口统计-性格的最优一对一匹配
- 生成 1000 个高保真用户画像

### 5.3 One-Shot 奖励估计

- 避免昂贵的多轮对话模拟
- Reward = Engagement + Learning Gain + 过滤惩罚 η
- Qwen3-235B (temperature=0) + rubric-grounded checklists
- 输出有效性瓶颈：非合规/无意义输出直接给 0 分

### 5.4 MDP 建模与训练

- State: 学习者画像 U_t
- Action: 练习处方 a_t
- Reward: 模拟反馈 r_t
- Transition: 能力向量更新（U_p_{t+1} = min(5, U_p_t + α_U · r_gain)）
- 基座模型: Qwen3-8B，用 ROLL (多轮 Agentic RL) 微调
- 硬件: 16x NVIDIA H20 GPUs, lr=1e-6, max_output=2048, batch_size=64

---

## 6. 教学支架（教练闭环）

### Stage 1: 沉浸式场景实践
- 目标驱动的角色扮演模拟
- LLM 驱动的 NPC 动态适应
- 通过语料推断权力动态、情感基调增强角色一致性

### Stage 2: 归因式能力评估
- **行为诊断**: D_b = LLM_diagnosis(U_t, L_t)，识别正/负行为，映射到 CASEL 能力
- **推理驱动归因**: D_c = LLM_attribution(U_t, L_t, D_b)
  - 习得性缺陷（Acquisition Deficit）：缺乏知识
  - 表现性缺陷（Performance Deficit）：知道但做不到
- 更新能力向量: U_p_{t+1} = LLM_profiling(U_t, L_t, D_b, D_c)

### Stage 3: 知识锚定的反思辅导
- 表现性缺陷 → 检索案例 K_c（示范技能应用）
- 习得性缺陷 → 检索理论 K_t（强化概念理解）
- 苏格拉底式提问促进深度反思
- G_t = LLM_guidance(U_t, L_t, D_b, D_c, K_t)

---

## 7. 实验结果

### 7.1 语料库质量
- Shannon Entropy 确认标签分布均匀
- 3位专家评审 Fleiss' Kappa = 0.63
- 标注一致性高（场景最高 4.92），内容教学价值好

### 7.2 练习调度 (Table 3)
200 测试用户画像，10轮学习路径：
- SocialCoach (Qwen3-8B 微调) 全面优于所有基线
- Engagement: 4.38 vs 最强基线 3.95
- Learning Gain: 4.11 vs 3.88
- 关键发现：不了解语料库内容的强 LLM 也会检索失败

### 7.3 辅导指导 (Figure 5)
- 8维度雷达图：SocialCoach 全面领先
- 消融实验证明归因式评估和知识检索都是关键模块

### 7.4 人类评估对齐 (Table 6)
- LLM 评估与专家的 Pearson 相关：Traceability 0.52, Learning Gain 0.51, Diagnosis 0.48 (p<0.01)
- 主观指标（Specificity 0.21）对齐较弱

### 7.5 用户研究（EQoach 产品）
- 50名参与者（25学生 + 25职场新人），至少10次练习
- Reflective Depth: **4.88**（最高！）
- Pedagogical Alignment: 4.66
- Skill Transferability: 4.56
- Agent Realism: 4.40

---

## 8. 技术亮点

| 亮点 | 描述 |
|------|------|
| 端到端框架 | 首次统一知识构建、个性化调度、沉浸式练习、诊断辅导 |
| Theory-to-Practice 知识框架 | 三层结构打通"知道"和"做到" |
| RL 优化的处方 Agent | 模拟器解决冷启动，Agentic RL 让小模型超越大模型 |
| 归因式评估 | 区分习得/表现缺陷，不只说"哪里错"还说"为什么错" |
| 苏格拉底式反思 | 引导自主反思而非填鸭式反馈 |

---

## 9. 局限性

- 用户研究规模较小（50人），产品还在早期 Beta
- 模拟器奖励与人类评估相关性中等（0.37-0.52）
- 主观性指标的 LLM-人类对齐较弱
- 语料主要来自英文书籍，跨文化适用性未充分验证
- RL 训练依赖 16 张 H20 GPU
