# Case Figure Specification

## 整体布局

- **尺寸**：full-width figure*，504pt（7in）宽，渲染源 1440px × 680px
- **结构**：左右两列，各占 50%，中间 1.5px 竖线分隔（带微阴影）
- **每列内部**：上下两半，各占 50%——上半是 vibe coding 失败，下半是 Agentic Consensus 处理
- **列标题**：顶部各一行大标题

```
┌─────────────────────────────┬─────────────────────────────┐
│  ML Training Pipeline       │  A/B Experiment             │
│  Silent Degradation         │  Feature Leakage            │
├─────────────────────────────┼─────────────────────────────┤
│  ① Vibe Coding  [dark]      │  ① Vibe Coding  [dark]      │
│                             │                             │
├ · · · · · · · · · · · · · ·┼· · · · · · · · · · · · · · ┤
│  ② Agentic Consensus [light]│  ② Agentic Consensus [light]│
│                             │                             │
└─────────────────────────────┴─────────────────────────────┘
```

---

## 视觉系统

### 颜色调色板

| 用途 | 颜色 | 背景色 | 形状补充 |
|---|---|---|---|
| 失败 / 错误 | `#dc2626` | `#fef2f2` | ✕ 圆形 pill |
| 成功 / 确认 | `#059669` | `#ecfdf5` | ✓ 圆形 pill |
| 高 entropy / 待定 | `#d97706` | `#fffbeb` | △ 圆形 pill |
| 中性节点填充 | `#f1f5f9` | — | 圆角矩形 |
| 中性节点边框 | `#cbd5e1` | — | — |
| 重要节点边框 | `#1e293b`（2px） | — | — |
| Vibe coding 背景 | `#0f172a` | — | 极细网格纹 1px `#1e293b` |
| Consensus 背景 | `#fafafa` | — | 左侧 2px accent 边线 |
| 分隔线 | `#e2e8f0` | — | 渐变淡出（两端透明） |
| muted 文字 | `#94a3b8` | — | — |

### 字体

- 正文标签：`'Inter', 'Helvetica Neue', sans-serif`
- 代码 / 节点名：`'JetBrains Mono', 'Menlo', monospace`
- 列标题：Inter Bold 14px
- 区块小标签：Inter 500 9px，muted 色
- 节点文字：Mono 11px
- 状态 pill：Inter 600 10px

### 节点样式

- 圆角：8px
- 默认：`fill: #f1f5f9`，`border: 1px solid #cbd5e1`
- 重要节点：`border: 2px solid #1e293b`
- 阴影：`box-shadow: 0 1px 3px rgba(0,0,0,0.08)`（印刷降级为边框）
- 状态 pill：全圆角（`border-radius: 999px`），颜色见上表

### 箭头

- 轻微贝塞尔曲线，`stroke: #94a3b8`，`stroke-width: 1.5`
- 箭头头部：小三角，5px
- 重要路径（confirmed）：`stroke: #059669`，`stroke-width: 2`
- 错误路径：`stroke: #dc2626`，`stroke-dasharray: 4,3`

### 分隔线

- 上下分隔：`border-top: 1px solid`，颜色用 CSS 渐变 `transparent → #e2e8f0 → transparent`
- 左右分隔：`border-right: 1.5px solid #cbd5e1`，右侧加 `box-shadow: 1px 0 4px rgba(0,0,0,0.04)`

---

## Case 1 左列：ML Training Pipeline

### 上半 — Vibe Coding（dark panel，背景 `#0f172a`）

**内容：**
- 顶部小标签：`① Vibe Coding`（muted，8px）
- 4 行 chat 记录（monospace，白色文字）：
  ```
  User  AUC dropped 2 pts — investigate
  Agent  Try lr = 0.0005
  User  No change
  Agent  Roll back features → User: No recovery
  Agent  Add null check → ✕ Day 4: root cause unknown
  ```
- 右侧浮动卡片（blind spots），细线连接：
  - `No snapshot versioning`
  - `No feature distribution record`
  - `Hypotheses only in chat`

**视觉：**
- chat 行背景交替 `#0f172a` / `#1e293b`
- `✕` 用红色 `#dc2626` pill
- blind spot 卡片：`#1e293b` 背景，`#d97706` 左边线，琥珀色文字

### 下半 — Agentic Consensus（light panel，背景 `#fafafa`）

**内容：**
- 顶部小标签：`② Agentic Consensus`（muted，8px）
- 左侧 2px `#059669` accent 边线
- 流水线溯源图（横向）：
  `data_snapshot → feature_pipeline → model → eval_metrics↓`
  `eval_metrics` 节点加红色边框 + `AUC ↓` pill
- 两个竞争假设框（虚线边框，8px 圆角）：
  - `Hyp A  Data Shift` → 右侧 `✕ ELIMINATED` 绿底划线
  - `Hyp B  Feature Drift` → 右侧 `✓ CONFIRMED` + `PR #847` 琥珀 pill
- H(C|I) entropy bar：小横条，`HIGH → RESOLVED`，颜色从红渐变到绿
- 底部结论行：`Window reverted → AUC recovered (same day)` 绿色文字

---

## Case 2 右列：A/B Experiment

### 上半 — Vibe Coding（dark panel）

**内容：**
- 两行对比信息：
  ```
  Treatment  13 features  ✕  user_realtime_signal [LEAKAGE]
  Control    12 features  ✓
  ```
- 分析结果行：`CTR lift: significant` → `Agent: recommend rollout ▶`
- 右侧 blind spot 卡片：
  - `Feature pipelines in separate repo`
  - `Statistical test: correct on invalid inputs`

**视觉：**
- `user_realtime_signal` 用红色 monospace + 红色 `LEAKAGE` pill
- Agent 推荐箭头旁加 `⚠` 琥珀色图标

### 下半 — Agentic Consensus（light panel）

**内容：**
- 左侧 2px `#059669` accent 边线
- 实验因果 DAG（树状，SVG）：
  ```
  experiment_config
      ├── feature_pipeline_ctrl   ✓ 12 features
      └── feature_pipeline_treat  ✕ 13 features
            └── metric_definition
  ```
  `feature_pipeline_treat` 节点红色边框
- Auditor 检查结果 pill：`PARITY CONTRACT: FAILED` 红色
- 分析状态：`BLOCKED` 琥珀色大 pill，横跨节点上方
- 修正后结论：`Re-run → lift not significant` → `✓ False positive avoided` 绿色

---

## 实现规范

- **文件**：单个 HTML 文件，`width: 1440px`，`height: 680px`
- **布局**：CSS grid `1fr 1fr`，两列
- **图形**：inline SVG（节点、箭头、DAG）
- **字体**：系统字体 fallback，无外部依赖
- **离线安全**：无 CDN，无外部图片
- **Caption**：不写在图内，全部在 LaTeX `\caption{}` 里
