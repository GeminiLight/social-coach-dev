# Final Case Studies

两个场景，展示 vibe coding 静默失败以及 consensus layer 如何介入。

---

## Case 1 — ML Training Pipeline: Silent Degradation

**Setup.**
推荐模型的周度评估 AUC 下降 2 个点。
三天 chat 驱动的调试（调学习率、回滚特征、加 null check）均无效；每次新会话都在不知道前几次已经排除了什么的情况下重新开始。

**What vibe coding misses.**
根因不可见：`click_rate_7d` 的计算窗口被悄悄从 7d 改成了 3d，这是一个无关 PR 的副作用，而且没有任何结构将该特征与使用它的模型关联起来。

**How C responds.**
C 维护流水线溯源图（`data_snapshot → feature_pipeline → model → eval_metrics`），并构造两个竞争假设，各自列出所需的判别证据：(A) 数据漂移；(B) 特征漂移。
由于 H(C|I) 很高，系统请求两个定向检查而不是猜测。
数小时内：(A) 被排除；(B) 被 drift test 确认，并通过 Ψ 追溯到 PR #847。
修复：将窗口回滚为 7d。AUC 当天恢复。

**Outcome.**
Vibe coding：4 天，3 个训练周期浪费，根因未知。
Agentic Consensus：数小时内定位并修复根因；修复路径记录回 C，作为未来变更的历史证据。

---

## Case 2 — A/B Experiment: Feature Leakage

**Setup.**
一个新推荐策略的 A/B 测试产出了统计显著的 CTR lift。
Agent 建议全量上线。

**What vibe coding misses.**
实验组有 13 个特征，对照组有 12 个。多出来的特征 `user_realtime_signal` 只在实验组中存在：lift 衡量的是特征优势，而不是策略优势。Agent 看不到特征流水线，因为它们在另一个 repo 里。

**How C responds.**
C 维护一张实验因果 DAG：`experiment_config` 分别喂给 control 和 treatment 的特征流水线，两者再喂给 `metric_definition`。
在产出任何数字之前，auditor 检查两条流水线的特征一致性合约；检查失败。
分析被阻断。移除 `user_realtime_signal` 后重新跑实验，lift 不显著。该策略无效。

**Outcome.**
没有 C：false positive 进入实验记录，触发全量上线，2--3 周后在生产环境暴露。
有了 C：结构违规在推断开始前就被拦截。
原始结果在统计上是正确的，但在因果上是无效的；更强的模型会产生同样错误的答案。

---

## What these cases demonstrate

第一个 case 展示 C 作为**诊断界面**：假设是显式的，不确定性可测量，证据收缩不确定性而不是对话轮次收缩不确定性。

第二个 case 展示 C 作为**有效性关卡**：结构合约在结果产出之前被检查，捕捉到任何统计复杂度都无法发现的错误。

两种情况下，失败都不是生成性的，而是结构性的。随着 AI 吞吐量扩大，opacity 积累的速度超过人类的检查速度；没有 governable consensus layer，规模化的 AI 辅助工程最终退化为规模化的不透明。
