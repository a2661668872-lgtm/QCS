# 状态

> 本文件由 `/cheat-status` 维护——每次跑 status 都会更新。手改无意义。

---

**最近更新**: 2026-08-15
**模式**: cold-start
**内容形态**: mixed（AI 案例拆解 / 科普 / 热点 / 测评 / 教程）
**当前 rubric**: v0（暂借教程／知识拆解版，待真实数据校准）
**校准样本**: 0 / 5（解锁第一次 bump 的门槛）

---

## 进度条

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 30 → SQLite 升级建议门槛
[░░░░░░░░░░░░░░░░░░░░] 0 / 5  → 脱离 cold-start 门槛
```

## 🎬 待办

无——你刚初始化，先写第一篇稿子吧。

## 🔥 候选池

已有 Markdown 选题池：`04_选题库/选题池.md`。
- 生成或增量更新选题 → 使用 `shengcai-topic-generator`
- 从现有选题中选择下一篇 → 说“推荐选题”

## 📈 健康度

- `rubric_notes.md`: 已创建（健康，<600 警戒线）
- `hooks_installed`: ❌（Windows Codex 不启用 Claude Code Hook）
- external audit configured: ❌

## 下一步建议

1. 在 `05_内容草稿/` 完成第一篇稿子，并把确认后的最终稿快照放进 `scripts/`
2. 跑 `打分这篇 scripts/<文件名>.md` 看 v0 rubric 的探索评分
3. 准备发布前跑 `启动预测`
4. 发布后说 `已发布 https://...`
5. T+3 天跑 `复盘 path/to/draft.md`

第 5 篇之后会解锁 `/cheat-bump`，rubric 才真正开始校准。

完整工作流见 `WORKFLOW.md`。
