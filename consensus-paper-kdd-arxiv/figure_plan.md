# Figure Plan: Vibe Coding vs. Agentic Consensus 对比图

## Design Context

### Users & Purpose
- **Primary audience**: KDD 2026 Blue Sky Track reviewers and attendees — senior researchers in data mining, ML systems, and applied AI
- **Final deliverable**: ACM sigconf 双栏论文正文插图 (Figure 2, 3, 4)，截图后导入 LaTeX
- **The job**: 让读者在 10 秒内直觉感受到 "vibe coding 的盲区" vs "consensus layer 的结构化可见性"，无需读正文

### Design Principles (Priority Order)

1. **Rigor first, aesthetics second** — 每个 UI 元素必须对应论文中的真实概念（$C$, $A$, $E$, $\Phi$, $\Psi$, $\mathcal{H}$）。不允许纯装饰性元素。如果一个节点出现在图里，它必须在场景描述中有对应。
2. **High-fidelity left, structural right** — 左侧高仿真 Cursor IDE（让读者产生"这就是我每天用的工具"的共鸣），右侧用清晰的结构化图谱（让读者看到"原来可以这样"）。两侧的视觉反差本身就是论证。
3. **Print-safe & ACM-compatible** — 浅色背景为主，确保黑白打印可区分。避免纯靠颜色传递信息，关键状态同时用形状/图标/文字区分。sigconf 双栏宽度 ~504pt (7in)，全宽图用 `figure*`。
4. **English only** — 所有文字全英文，术语与论文正文保持一致。
5. **Minimal honest annotation** — 左侧的盲区标注和右侧的状态标注使用克制的方式（细线、小图标），不用夸张的红色大叉渲染情绪。学术图表应该让读者自己判断，不是广告。

### Anti-references (What NOT to do)
- 不做 marketing landing page 风格的"功能对比表"
- 不做 product demo 截图（我们没有 working system）
- 不用渐变色、投影堆叠、3D 效果
- 不用 emoji 作为正式标注符号（论文打印后可能丢失）

---

## 输出规格

### ACM sigconf 排版约束
- **Full-width figure** (`figure*`): 最大 504pt (7in / 17.8cm) 宽
- **Column figure** (`figure`): 最大 241pt (3.35in / 8.5cm) 宽
- **推荐**: 三张图均用 `figure*` 全宽，左右对比布局自然
- **DPI**: 截图导出 ≥ 300dpi (HTML 渲染宽度 1400-1600px，截图后缩放)
- **字体**: 截图后最小可读字号 ≈ 7pt（对应 HTML 中 ~11px at 1440px 宽度）
- **Caption**: 在 LaTeX 中写，HTML 图内不放 caption

### HTML 渲染规格
- 固定宽度 1440px（截图后缩放到 504pt 约 2.86x，300dpi 友好）
- 高度自适应，每张图预估 600-800px
- 无外部依赖（字体用 system fallback，不加载 Google Fonts）
- 用 inline SVG 画图谱（精确控制、矢量清晰）

---

## 整体设计

- 格式：HTML + CSS，浏览器打开后截图导入 LaTeX
- 三张图覆盖三个领域：软件工程、机器学习、数据科学
- 左侧：**Vibe Coding (Chat + IDE)**，高仿真 Cursor 界面
- 右侧：**Agentic Consensus**，结构化图谱 + 证据面板

---

## Figure A: 微服务 API 升级引发连锁故障（软件工程）

**场景**: 支付服务从 v1 升级到 v2，改了返回结构（嵌套 → 扁平）。Agent 帮你改完了调用方代码，测试全过。上线后订单服务和风控服务相继报错——它们依赖旧结构中的嵌套字段，但没人知道这条隐式依赖。

**为什么需要 consensus layer**: 微服务间的接口契约、隐式依赖、版本兼容性假设——这些东西不在任何一个 repo 的代码里，散落在 API 文档、Slack 对话、和工程师脑子里。IDE 能帮你看一个 repo 的代码，但看不到跨服务的依赖拓扑。

### 左侧 — Vibe Coding

模拟 Cursor 界面，分两个区域：

1. **Chat 面板**
   - 用户："upgrade payment API to v2, flatten the response structure"
   - Agent：输出 diff，修改了 `payment-service` 和直接调用方 `checkout-service`
   - 底部："✓ All 47 tests passed · PR ready to merge"

2. **IDE 代码面板**
   - 打开 `payment-service/api/response.ts`，绿色/红色 diff
   - 文件树只显示当前 repo 的文件
   - 关键盲区标注：
     - ❌ "`order-service` 也消费这个 API？" — Agent 不知道，不在同一个 repo
     - ❌ "`risk-engine` 依赖嵌套字段 `payment.details.risk_score`？" — 没有记录
     - ❌ "v1 → v2 是否需要灰度？兼容期多长？" — chat 里没讨论过

3. **上线后 timeline**
   - T+0: Deploy ✓
   - T+2h: `order-service` 500 errors spike（解析失败）
   - T+6h: `risk-engine` 静默降级（字段缺失被默认值替代，风控规则失效）
   - 红色警告："需要回滚 + 逐个排查下游消费者"

### 右侧 — Agentic Consensus

1. **Consensus Layer C — 服务依赖图**
   - 属性图可视化：
     - 核心节点：`payment-service (v2)` 居中
     - 依赖方节点：`checkout-service`、`order-service`、`risk-engine`、`analytics-pipeline`
     - 边上标注：API version, consumed fields, SLA
   - 变更高亮：
     - `payment-service` 黄色（变更源）
     - `checkout-service` 绿色 ✓（已适配）
     - `order-service` 红色 ⚠（消费 `details.items`，v2 路径变了）
     - `risk-engine` 红色 ⚠（消费 `details.risk_score`，v2 删了嵌套）
     - `analytics-pipeline` 黄色 ?（消费 raw event，可能不受影响，需确认）
   - 不变量标注：`breaking_change: true` → 需要兼容方案

2. **Agent 行为**
   - Architect：识别出 4 个下游消费者，标记 2 个 breaking + 1 个 uncertain
   - Builder：生成适配 diff 只覆盖已确认的服务
   - Auditor：标记 `analytics-pipeline` 为 "证据不足，需人工确认"
   - 熵指示：H(C|I) = MEDIUM → 暂定提交 checkout + order 的适配，analytics 挂起

3. **Evidence E**
   - contract test: checkout ✓, order ✓ (after fix)
   - integration test: risk-engine ✓ (after field mapping)
   - analytics: ⏳ pending confirmation
   - 每条 evidence 连回 C 中对应的服务依赖边

4. **上线后 timeline**
   - T+0: 分批灰度，v1/v2 双版本路由
   - T+24h: 全量切换，零故障
   - 绿色："C 中记录完整的迁移决策，可复盘"

---

## Figure B: ML 训练管道静默退化（机器学习）

**场景**: 推荐模型周迭代训练，某周 AUC 掉了 2 个点。没有报错，没有失败的 job，只是指标默默变差了。团队开始猜：是数据问题？是特征问题？是超参问题？Agent 逐一生成 fix，但每次都是"试一试看"。

**为什么需要 consensus layer**: ML pipeline 的因果链很长（数据采集 → 特征工程 → 训练配置 → 评估 → 部署），任何一环的隐式变更都可能导致下游退化。IDE 能看代码，但看不到"上周和这周的训练 pipeline 到底哪里不同"这个结构性问题。

### 左侧 — Vibe Coding

1. **Chat 面板**
   - 用户："AUC dropped 2 points this week, investigate"
   - Agent Round 1："可能是 learning rate，试试 0.001 → 0.0005" → diff
   - 用户："没用，还是低"
   - Agent Round 2："可能是新特征引入了噪声，我回滚 feature_v3" → diff
   - 用户："回滚了但没恢复"
   - Agent Round 3："检查数据质量？我加个 null check" → diff
   - 越来越长的对话，每一轮都是猜测 → 改代码 → 等训练结果

2. **IDE 面板**
   - 打开 `training/config.yaml` 和 `features/pipeline.py`
   - 开发者在两个文件之间跳转，试图手动 diff 上周 vs 这周的配置
   - 标注：
     - ❌ "上周的 data snapshot 是什么？" — 没有版本化
     - ❌ "哪些特征的分布变了？" — 需要手动写 profiling 脚本
     - ❌ "3 轮尝试中哪些假设被排除了？" — 只在 chat history 里

3. **状态条**
   - "第 4 天，3 轮实验，根因仍不确定" 红色

### 右侧 — Agentic Consensus

1. **Consensus Layer C — 竞争性因果子图**
   - Pipeline lineage 图：`data_snapshot` → `feature_pipeline` → `training_config` → `model` → `eval_metrics`
   - 两个并排的因果假设子图：
     - **Hypothesis A**（数据偏移）：
       - `data_snapshot_week12` vs `week11`：schema 相同，但 `user_activity` 表行数 -15%
       - 原因链：上游采集 job 超时 → 部分分区丢失 → 训练数据不完整
     - **Hypothesis B**（特征漂移）：
       - `feature_v3` 的 `click_rate_7d` 分布偏移（p < 0.01）
       - 原因链：`click_rate` 计算窗口被无意改为 3d（某次 PR 的副作用）
   - 每个假设标注：需要什么判别性证据
   - 熵指示条：H(C|I) = HIGH → 触发 clarification

2. **Clarification Step**
   - Agent 不猜测，而是请求具体信息：
     - "请确认 week12 的 data_snapshot 是否完整（需要分区行数对比）"
     - "请运行 feature drift test 对比 week11 vs week12 的 click_rate_7d 分布"

3. **Resolution**
   - 证据返回：snapshot 完整（排除 Hypothesis A），click_rate 窗口确认被改（确认 Hypothesis B）
   - Hypothesis A 灰色删除线，Hypothesis B 存活
   - 最终 fix：回滚 click_rate 窗口到 7d，从存活的 consensus 派生
   - 熵降低到 LOW，commit

---

## Figure C: A/B 实验中特征泄漏导致错误结论（数据科学）

**场景**: 数据科学团队跑一个推荐策略的 A/B 实验。Agent 帮忙写了实验分析代码，p-value 显著，结论是新策略提升了 CTR 3%。但实际上实验组的特征管道里混入了一个只有实验组才有的用户行为信号（特征泄漏），结论无效。团队基于错误结论全量上线，两周后发现 CTR 并没有提升。

**为什么需要 consensus layer**: 数据科学的核心问题是**实验设计的完整性和因果推断的可靠性**。特征泄漏、样本污染、指标定义不一致——这些不是代码 bug，而是实验逻辑和数据管道之间的结构性矛盾。IDE 能看代码，但看不到"实验组和对照组的特征管道是否真正隔离"这个跨系统的结构性问题。

### 左侧 — Vibe Coding

1. **Chat 面板**
   - 用户："analyze the A/B test results for the new recommendation strategy"
   - Agent：生成分析脚本，输出 "CTR +3.1%, p=0.003, significant"
   - 用户："great, prepare the launch report"
   - Agent：生成漂亮的 report，结论明确："recommend full rollout"

2. **IDE 面板**
   - 打开 `analysis/ab_test_report.py`，看到清晰的分析代码
   - Jupyter notebook 显示 p-value 图和置信区间
   - 标注：
     - ❌ "实验组的特征管道和对照组一致吗？" — 代码里看不出来，特征是上游生成的
     - ❌ "`user_realtime_signal` 特征只对实验组可用？" — 在另一个 repo 的配置里
     - ❌ "指标定义是否排除了 bot traffic？" — 用的是默认 CTR 定义

3. **两周后 timeline**
   - 全量上线后 CTR 并未提升
   - 回查发现特征泄漏：实验组独有的 realtime signal 导致虚假提升
   - 红色："实验结论无效，浪费两周 + 损失用户体验"

### 右侧 — Agentic Consensus

1. **Consensus Layer C — 实验因果图**
   - 实验设计图：
     - 节点：`experiment_config`、`control_group`、`treatment_group`、`feature_pipeline_ctrl`、`feature_pipeline_treat`、`metric_definition`、`analysis`
     - 关键边和契约：
       - `feature_pipeline_ctrl` ↔ `feature_pipeline_treat`：contract: `feature parity`（特征一致性）
       - `metric_definition` → `analysis`：contract: `excludes bot traffic`
   - 冲突检测高亮：
     - `feature_pipeline_treat` 红色 ⚠：包含 `user_realtime_signal`，而 `feature_pipeline_ctrl` 没有
     - `feature parity` 契约标记为 **VIOLATED**
   - Auditor 附注："实验组和对照组特征集不一致，实验结论不可信"

2. **Agent 行为**
   - Architect：构建实验因果 DAG，识别 treatment/control 的特征管道差异
   - Auditor：运行 feature parity check → 发现 `user_realtime_signal` 只存在于 treatment
   - 熵分级：
     - 特征泄漏：HIGH → 暂停实验分析，要求修复特征管道
     - 指标定义：MEDIUM → 标记需确认 bot 过滤逻辑
   - Navigator：向用户展示因果图，高亮泄漏路径

3. **Evidence E**
   - feature parity test: FAILED ❌（`user_realtime_signal` 不对称）
   - metric definition audit: ⚠ bot filter 未启用
   - sample ratio mismatch test: ✓ 通过
   - 每条 evidence 连回 C 中对应的实验设计节点

4. **结果**
   - 实验在提交结论前被拦截
   - 修复后重跑：CTR 差异消失，避免了错误上线
   - 绿色："C 中记录了完整的实验设计审计过程"

---

## 三张图的设计一致性

### 共同模式（每张图都体现）

| 维度 | 左侧 Vibe Coding | 右侧 Agentic Consensus |
|------|-------------------|------------------------|
| Agent 行为 | 接到指令 → 直接生成 diff | 先分析依赖图 → 识别影响范围 → 再生成 |
| 不确定性 | 隐式（agent 猜了就做） | 显式（熵分级：自动/暂定/暂停） |
| 发现问题的时刻 | 上线后（被动） | 提交前（主动） |
| 事后复盘 | 考古 git + chat + Slack | 查询 C 的结构 + evidence |

### 三张图的差异化

| 图 | 领域 | 核心结构 | 关键 insight |
|----|------|---------|-------------|
| A: 微服务升级 | 软件工程 | 服务依赖图 + API 契约 | 跨 repo 的隐式依赖是 IDE 看不到的 |
| B: 训练退化 | 机器学习 | Pipeline lineage + 因果假设图 | 长因果链需要结构化假设对比，不能靠猜 |
| C: A/B 实验泄漏 | 数据科学 | 实验因果 DAG + 特征一致性契约 | 实验逻辑的结构完整性不是代码 bug，IDE 查不出来 |

---

## 视觉风格系统 (Design Tokens)

所有三张图共用同一套视觉语言。设计优先级：**可辨识性（黑白打印）> 语义准确性 > 美观**。

### 色板

```
/* ── 全局 ── */
--bg-page:          #FAFBFC          /* 页面背景，接近白 */
--border-divider:   #C9CDD4          /* 分割线 */
--text-primary:     #1A1D23          /* 正文，接近纯黑 */
--text-secondary:   #5A6270          /* 辅助说明 */
--text-muted:       #8C939E          /* 时间戳、标签 */

/* ── 左侧 Vibe Coding (高仿真 Cursor 深色主题) ── */
--vibe-bg:          #1E1E2E          /* 编辑器背景 */
--vibe-surface:     #252630          /* 侧边栏/面板 */
--vibe-titlebar:    #16161E          /* 标题栏 */
--vibe-tab-active:  #1E1E2E          /* 当前 tab 背景 */
--vibe-tab-inactive:#252630          /* 非活动 tab */
--vibe-chat-user:   #2563EB          /* 用户气泡 */
--vibe-chat-agent:  #30313C          /* Agent 气泡 */
--vibe-text:        #D4D4D8          /* 编辑器文字 */
--vibe-text-dim:    #6B6F7B          /* 行号、注释 */
--vibe-diff-add:    rgba(34,197,94,0.12)
--vibe-diff-del:    rgba(220,38,38,0.12)
--vibe-accent:      #7C3AED          /* Cursor 品牌紫（标题栏 icon） */

/* ── 左侧盲区标注 ── */
/* 注意：不用纯红色渲染恐惧，用中性色+图标让读者自己判断 */
--blind-border:     #94A3B8          /* 盲区虚线框 slate-400 */
--blind-icon:       #DC2626          /* 小圆点/叉号 红 */
--blind-text:       #64748B          /* 说明文字 slate-500 */
--blind-bg:         rgba(148,163,184,0.06)

/* ── 右侧 Agentic Consensus ── */
--ac-bg:            #FFFFFF
--ac-surface:       #F1F5F9          /* slate-100 */

/* 状态色 — 每个状态同时有颜色+形状+文字标签，确保黑白可区分 */
--ac-verified:      #059669          /* emerald-600: 已验证 (配 ✓ 形状) */
--ac-warning:       #D97706          /* amber-600: 需确认 (配 △ 形状) */
--ac-breaking:      #DC2626          /* red-600: 冲突 (配 ✕ 形状) */
--ac-pending:       #6B7280          /* gray-500: 等待 (配 ○ 形状) */

/* 图谱关系色 */
--ac-edge:          #4F46E5          /* indigo-600: 默认依赖边 */
--ac-edge-contract: #7C3AED          /* violet-600: 契约边 */
--ac-evidence:      #7C3AED          /* violet-600: 证据链接 */

/* 熵指示器 — 复用状态色 */
--ac-entropy-low:   var(--ac-verified)
--ac-entropy-mid:   var(--ac-warning)
--ac-entropy-high:  var(--ac-breaking)

/* Timeline */
--tl-fail-bg:       #FEF2F2          /* red-50 */
--tl-fail-border:   #DC2626
--tl-ok-bg:         #F0FDF4          /* green-50 */
--tl-ok-border:     #059669
```

### 字体

```
/* 无外部字体依赖，全部 system fallback */
--font-ui:     -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
--font-mono:   'SF Mono', 'Cascadia Code', 'Consolas', 'Liberation Mono', monospace
--font-label:  var(--font-ui)

/* 字号 — 基于 1440px 渲染宽度，截图缩放到 504pt 后的最终可读性 */
--size-panel-title: 13px    /* 面板标题: "Chat" / "Editor" / "Consensus Layer C" */
--size-body:        12px    /* 气泡文字、代码、图谱标签 */
--size-small:       10.5px  /* 证据条目、状态标签、盲区说明 */
--size-tiny:        9px     /* 行号、时间戳 — 截图后约 7pt，ACM 最小可读 */
```

### 间距与尺寸

```
--width-total:      1440px     /* 截图宽度 → 缩放到 504pt at 300dpi */
--height-estimate:  640-780px  /* 每张图预估高度 */

/* 左右分栏 */
--width-left:       48%        /* Vibe Coding */
--width-divider:    4%         /* VS 分割区 */
--width-right:      48%        /* Agentic Consensus */

/* 面板 */
--radius-panel:     8px
--padding-panel:    14px
--gap-vertical:     10px

/* 气泡 */
--radius-bubble:    12px
--padding-bubble:   8px 12px

/* 图谱节点 */
--radius-node:      6px
--node-min-w:       72px
--node-max-w:       150px
--node-h:           32px       /* 单行 */
--node-h-2:         44px       /* 双行 */
--node-border:      1.5px
--node-shadow:      0 1px 2px rgba(0,0,0,0.06)

/* 图谱边 */
--edge-width:       1.5px
--edge-arrow:       5px        /* 箭头尺寸 */
--edge-contract:    1.5px dashed

/* 状态 badge */
--badge-size:       14px       /* 贴在节点右上角的状态指示 */
```

### Cursor 高仿真规范（左侧）

```
整体布局 (上→下):
  ┌─────────────────────────────────┐
  │ Title Bar (--vibe-titlebar)     │  28px 高
  │  ● ● ●  filename.ts — project  │
  ├──────────┬──────────────────────┤
  │ Activity │ Tab Bar              │  30px 高
  │ Bar      ├──────────────────────┤
  │ (icons)  │ Editor / Chat Area   │  主区域
  │ 40px 宽  │                      │
  │          ├──────────────────────┤
  │          │ Status Bar           │  22px 高
  └──────────┴──────────────────────┘

Title Bar:
  - 背景: var(--vibe-titlebar)
  - 左侧: 三个交通灯圆点 (●●● 8px, #FF5F57 #FEBC2E #28C840)
  - 中间: 当前文件名 (dim text)
  - 字号: var(--size-tiny)

Activity Bar (左侧窄条):
  - 宽度: 40px
  - 背景: var(--vibe-surface)
  - 图标: 用简化的 SVG line icons (Explorer, Search, Git, Chat)
  - 当前活动项: 左边框 2px var(--vibe-accent)

Tab Bar:
  - 活动 tab: var(--vibe-tab-active), 下边框消失, 文字白色
  - 非活动 tab: var(--vibe-tab-inactive), 文字 dim

Editor Area:
  - 背景: var(--vibe-bg)
  - 行号: var(--vibe-text-dim), 右对齐, var(--size-tiny)
  - 代码: var(--vibe-text), var(--font-mono), var(--size-body)
  - 语法高亮 (简化4色):
    keyword:  #C678DD (紫)
    string:   #98C379 (绿)
    function: #61AFEF (蓝)
    comment:  #5C6370 (灰)
  - Diff 高亮: 整行背景 var(--vibe-diff-add/del)

Chat Panel (嵌入编辑器区右侧或底部):
  - 宽度: 约 45% 的编辑器区域
  - 用户气泡: var(--vibe-chat-user), 白色文字, 右对齐, 右下角尖角
  - Agent 气泡: var(--vibe-chat-agent), var(--vibe-text), 左对齐, 左下角尖角
  - Agent 气泡内 code block: 更深的背景 #1A1B26, monospace, 小字号
  - 底部: 输入框样式 (灰色 placeholder "Ask Cursor...")

Status Bar:
  - 背景: var(--vibe-accent) 或 #007ACC
  - 文字: white, var(--size-tiny)
  - 内容: "✓ All 47 tests passed" 或分支名
```

### 盲区标注规范（左侧）

```
设计原则: 克制、学术。不是"产品缺陷展示"，而是"结构知识缺失的客观标注"。

容器:
  - 边框: 1px dashed var(--blind-border)
  - 背景: var(--blind-bg)
  - 圆角: 4px
  - 位于编辑器区右侧或叠加在代码行之上

内容:
  - 小圆点 ● (6px, var(--blind-icon)) + 问题描述 (var(--size-small), var(--blind-text))
  - 可选: 下方更小字的原因说明 (var(--size-tiny))
  - 连接线: 1px dashed var(--blind-border), 从标注指向代码中的对应行

数量控制: 每个 figure 最多 3 个盲区标注，多了会变成控诉而非分析
```

### 图谱节点规范（右侧）

```
节点样式:
  ┌──────────────────┐
  │ icon  Label Text │  ← 单行 32px 高
  └──────────────────┘
  - 圆角矩形, var(--radius-node)
  - 边框: var(--node-border) solid, 颜色随状态
  - 背景: white
  - 阴影: var(--node-shadow)
  - 文字: var(--size-body), var(--font-label)
  - 可选前缀图标: 12px SVG (服务/数据/模型/实验 等)

状态边框色 + badge:
  - Verified:  var(--ac-verified) 边框 + 右上角 ✓ (圆形绿底白勾)
  - Warning:   var(--ac-warning) 边框 + 右上角 △ (三角黄底 !)
  - Breaking:  var(--ac-breaking) 边框 + 右上角 ✕ (圆形红底白叉)
  - Pending:   var(--ac-pending) 虚线边框 + 右上角 ○ (空心灰圈)

  注意: badge 是形状+颜色双编码，黑白打印时靠形状区分

边/连线:
  - 依赖边: var(--edge-width) solid var(--ac-edge), 带箭头
  - 契约边: var(--edge-contract) var(--ac-edge-contract), 带标签 (e.g., "contract: feature parity")
  - Breaking 边: var(--edge-width) solid var(--ac-breaking), 带 ✕ 中点标记
  - 证据链接: var(--edge-width) dotted var(--ac-evidence), 从 Evidence 面板指向节点

标签:
  - 边上标签: var(--size-small), 白底半透明 padding, 居中
  - 节点下方说明: var(--size-tiny), var(--text-secondary)
```

### Evidence 面板规范（右侧）

```
位置: 图谱区下方或右侧，宽度约 30-40% 的右侧面板
背景: var(--ac-surface)
圆角: var(--radius-panel)

条目样式:
  ● label: status_text          ← 一行一条
  - ● 圆点颜色随状态 (verified/warning/breaking/pending)
  - label: var(--size-small), var(--font-mono), var(--text-primary)
  - status_text: var(--size-small), 状态色
  - 连接虚线从 ● 延伸到图谱中对应节点

示例:
  ● contract test: checkout     ✓ passed
  ● integration: risk-engine    ✓ passed
  ● analytics-pipeline          ⏳ pending
```

### 熵指示器规范（右侧）

```
位置: 图谱面板右上角
样式: 紧凑标签，非仪表盘

  ┌─────────────────────┐
  │ H(C|I)  ████░░  MED │
  └─────────────────────┘

  - 外框: 1px solid var(--border-divider), 圆角 4px
  - 标签 "H(C|I)": var(--size-tiny), var(--font-mono)
  - 进度条: 60px 宽, 6px 高, 圆角 3px
    - 填充色: LOW=绿 / MED=黄 / HIGH=红
    - 填充比: LOW=30% / MED=60% / HIGH=90%
  - 状态文字: "LOW"/"MED"/"HIGH", var(--size-tiny), bold, 对应色
```

### Timeline 规范（两侧底部）

```
左侧 (failure):
  - 背景: var(--tl-fail-bg)
  - 左边框: 3px solid var(--tl-fail-border)
  - 圆角: var(--radius-panel)
  - 条目: "T+2h  order-service 500 errors" (var(--size-small))
  - 时间标签: var(--font-mono), var(--size-tiny), bold

右侧 (success):
  - 背景: var(--tl-ok-bg)
  - 左边框: 3px solid var(--tl-ok-border)
  - 条目和字号同左侧
```

### VS 分割区

```
宽度: var(--width-divider)
样式:
  - 竖向虚线: 1px dashed var(--border-divider)
  - 中间: 圆形 badge "VS"
    - 28px 直径
    - 白底, 1px solid var(--border-divider)
    - 文字 "VS", 10px, bold, var(--text-secondary)
```

### 顶部 Banner

```
高度: 40px
背景: var(--bg-page)
布局:
  - 左: Figure 编号 (bold) + 标题
    例: "Figure 2  Microservice API Upgrade"
    字号: 14px, var(--text-primary)
  - 右: 领域标签 badge
    例: "Software Engineering"
    样式: 胶囊形, var(--ac-surface) 背景, 1px solid var(--border-divider), var(--size-small)
底部: 1px solid var(--border-divider)
```

---

## 技术实现

- 单个 HTML 文件 per figure，内嵌 CSS + inline SVG，零外部依赖
- 字体用 system fallback stack（不加载 Google Fonts，避免离线打开失败）
- CSS Grid 做左右分栏 + VS 分割区
- 图谱用 inline SVG（精确控制节点位置和连线路径，矢量清晰）
- Cursor 仿真用 CSS（title bar, tabs, activity bar, editor, status bar）
- 固定 1440px 宽度，高度自适应
- 截图方式：浏览器打开 → DevTools 截取全页 → 得到 1440px+ 宽的 PNG → LaTeX 中 `\includegraphics[width=\textwidth]`

## 文件结构

```
figures/
├── figure-a-microservice.html      # Case 1: Microservice API Upgrade (SE)
├── figure-b-ml-pipeline.html       # Case 2: ML Training Degradation (ML)
└── figure-c-ab-experiment.html     # Case 3: A/B Test Feature Leakage (DS)
```
