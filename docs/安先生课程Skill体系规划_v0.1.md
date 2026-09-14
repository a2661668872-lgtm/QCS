---
文档类型: Skill 体系建设规划
版本: v0.1
状态: 待确认
创建日期: 2026-09-02
---

# 安先生课程 Skill 体系规划 v0.1

## 一、核心判断：不另起炉灶，补方法层

调研后发现已有资产已覆盖流程层，重复建设会造成冲突。三层分工应为：

| 层 | 现有 / 待建 | 职责 | 已有什么 |
|---|---|---|---|
| **流程层** | 已有 | 决定「下一步做什么、产出什么格式」 | `qcs` / `shengcai-content-writer` / `shengcai-pattern-extractor` / `shengcai-topic-generator` |
| **方法层** | **待建 `qingchushan-*`** | 决定「这一步怎么做得更好」：检查清单、判据、练习动作 | 无。现有 shengcai 为契约型 skill（6–8KB，含 output-contract / schema / protocol），不含方法论 |
| **知识层** | 已有 | 原始素材与完整论述 | `01_学习对象/安先生/`（5.0 共 38 节约 120 万字 + 旧版 91 节 + 结构化笔记 22 份） |
| **预测层** | 已有 | 打分、盲预测、复盘、rubric 升级 | `cheat-on-content`（主入口 + 9 子 skill） |

**关键结论**：`shengcai-*` 是施工流程，安先生课程是施工规范。当前系统状态为 cold-start（样本 0），所有方法均为先验 —— 恰恰需要把先验组织成可调用的形式。这正是 `qingchushan-*` 的价值。

## 二、架构设计

```
an  ──主入口：识别卡点 → 派 1 主 + 最多 2 辅
 │
 ├── 方法层 qingchushan-* × 20（按流程节点组织，非按课程目录）
 │
 └── 知识层：课程资料按需定位，不内嵌进 skill
```

### 为什么按流程节点而非课程目录组织

用户调用时的心智是「我卡在开头」，不是「我要看第 023 节」。dbskill（`dbs-hook` / `dbs-xhs-title` / `dbs-script-flow`）与本地 `cheat-on-content`（`cheat-predict` / `cheat-retro`）均采用此模式。

## 三、Skill 清单（20 个，分四批）

### P0 — 核心五件（先做样板）

| Skill | 流程节点 | 课程来源 |
|---|---|---|
| `qingchushan` | 主入口：卡点识别 + 编排 | 顶层索引 |
| `qingchushan-language` | 文字基本功 | 5.0 基本功篇 011（be→do、专属细节五槽位、擦掉检验法、长短句） |
| `qingchushan-topic` | 选题＝需求＋解决方案 | 5.0 方向篇 008–009 + `03-选题流程和内容思维` |
| `qingchushan-outline` | 大纲与材料组织 | 5.0 基本功篇 015 |
| `qingchushan-hook` | 钩子 | 5.0 进阶篇 020 + `04-结构的精细化处理` |

### P1 — 定位与表达

`qingchushan-account`（定位五要素，方向篇 005–007）、`qingchushan-position`（内容在业务路径中的位置，认知准备篇）、`qingchushan-entry`（人群印记／理解门槛／普世切口／陌生度）、`qingchushan-skeleton`（骨架）、`qingchushan-spike`（情绪刺点）、`qingchushan-scene`（情境化）、`qingchushan-story`（故事性）

### P2 — 影像

`qingchushan-visual`（用画面讲故事）、`qingchushan-shot`（镜头表现力）、`qingchushan-space`（空间调度）、`qingchushan-object`（物品视觉化）、`qingchushan-efficiency`（信息效率）

### P3 — 闭环与边界

`qingchushan-review`（数据复盘）、`qingchushan-ai`（AI 协作边界与指令模板）、`qingchushan-boundary`（发布风险检查）、`qingchushan-learn`（学习路线导航）

## 四、三条设计原则

### 1. 原文不打包进 Skill

三个理由：

- **版权与边界**：`课程总索引.md` 已明确「不照搬课程案例、标题、开头、话术和个人表达；只吸收专业知识、判断框架和练习方法」。Skill 只承载方法论。
- **体积**：120 万字无法装入 skill 上下文。
- **时效性**：逐字稿未逐句校音，未来会修订；skill 内嵌原文会立即过时。

**做法**：Skill 内记录「卡点 → 去读哪个文件的哪一段」，运行时定位原文，而非复制原文。

### 2. 每个 Skill 必须可执行，不能是读书笔记

最小结构：`判断框架` + `检查清单` + `判据` + `练习动作`。

以 `qingchushan-language` 为例（已验证可用的三个可执行件）：

- **擦掉检验法**：文案按逗号拆行，遮住其他句，单看一句能懂即为短句
- **专属细节五槽位**：时间 / 地点 / 职业身份 / 数量 / 专属物品
- **be→do 转换**：把「是什么」改写成动作

### 3. 方法层与流程层通过主入口耦合，不互相内嵌

`qingchushan` 识别卡点后，输出应包含：调用哪个 `qingchushan-*` 方法 + 对应 `shengcai-*` 的哪个流程步骤。两个前缀保持独立，避免后续维护冲突。

## 五、实施路径

1. **先做 `qingchushan-language` 样板**（课程来源最清晰，本轮已提取完整方法），验证「可执行性」与「原文引用方式」两个设计点。
2. **样板确认后铺 P0 其余四个** + `qingchushan` 主入口。
3. **P1/P2/P3 按实际卡点驱动** —— 遇到哪个环节卡住就建哪个，不提前铺完。

### 安装位置（待确认）

- 用户级 `C:\Users\JT\.workbuddy\skills\`（与 dbskill 同级，确定可调用）
- 项目级需创建 `.workbuddy\skills\`（当前 `.workbuddy` 下仅有 memory）
- 注意：项目根 `skills/` 存放 shengcai 与 cheat，但非 WorkBuddy 标准项目级路径，需确认其加载方式后再决定统一方案

**路径硬编码风险**：skill 内应使用相对项目根的路径描述，不写死 `D:\...` 绝对路径（用户有换电脑接续工作的需求）。

## 六、待确认

1. 命名前缀 `qingchushan-` 是否采用（已检查用户级无冲突）
2. 安装位置：用户级 / 项目级
3. 是否先做 `qingchushan-language` 样板
4. 20 个清单是否需要增删（可先只做 P0 五件）
