# 台账与元数据

## 资料处理台账

台账负责管理处理状态，资料识别卡负责帮助人和 AI 理解资料。

每份资料至少记录：

```yaml
source_id:
source_title:
source_location:
source_type:
processing_status:
purpose_value:
content_fingerprint:
last_scanned_at:
last_processed_at:
generated_materials:
timeliness:
verification_status:
unprocessed_reason:
```

## 处理状态

```text
discovered
→ recognized
→ evaluated
→ processing
→ processed
→ needs-verification / needs-update
```

辅助状态：`indexed-only`、`partial`、`blocked`、`skipped`。

## 内容指纹

优先分别保存：

- 原始资料指纹；
- 标准化内容指纹；
- 素材指纹。

指纹变化时定位变化部分，优先增量整理；结构大幅变化时重新识别和规划。

## 素材最小元数据

```yaml
material_id:
title:
type:
status:
created:
summary:
source_ids:
applicable_scenarios:
related_tools:
target_users:
timeliness:
verification_status:
keywords:
```

元数据用于筛选和追溯，正文用于完整表达。不要为了字段完整而重复正文。

## 稳定 ID

- ID 不随文件改名变化；
- 来源 ID 和素材 ID 必须唯一；
- 聚合多来源结论应使用独立的聚合来源 ID；
- 所有素材来源 ID 必须能在台账找到。

## 时效与验证

### timeliness

- `low`：稳定方法与原则
- `medium`：实践流程和案例
- `high`：工具功能、界面、价格、数据、政策和预测

### verification_status

- `source-supported`
- `multi-source-supported`
- `generalized-from-source`
- `needs-practice`
- `needs-fact-check`
- `time-sensitive-needs-review`
- `sampled`

