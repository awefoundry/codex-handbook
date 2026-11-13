---
id: codex-subagents-parallel-work
title: Codex 使用 Subagents 并行处理任务（2026-11 更新）：/subagents、继承沙箱，和主会话怎么分工
seo_title: Codex Subagents：/subagents、沙箱继承与主会话分工
description: 并行调查会把主会话冲乱时，把只读或可隔离的工作交给子 agent。本文按 2026-11-06 的官方文档说明 /subagents、沙箱如何继承，以及和主会话、Goal、多任务线怎么分工。
lede: 主会话留下需求和决定。子 agent 拿走中间噪声，并把摘要交回来。沙箱和审批跟父会话走，TOML 改不了。
url: /guides/codex-subagents-parallel-work
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 6
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-19
date_modified: 2026-11-06
verified_on: 2026-11-06
official_ref: https://learn.chatgpt.com/docs/agent-configuration/subagents
keywords: [Codex Subagents, Codex /subagents, Codex 子代理, Codex 并行任务, 沙箱继承]
related: [codex-goal-mode-long-running-work, codex-long-task-collaboration-workflow, cli-manage-multiple-sessions, worktree-parallel-chats, model-reasoning-effort]
howto: true
faq:
  - q: 自定义 Agent 的 TOML 能单独设只读沙箱或换一套 MCP 吗？
    a: 不能。官方写明自定义 Agent 继承父会话的权限、provider 和 MCP 服务器，文件里写 sandbox_mode、approval_policy、model_provider、mcp_servers 不会覆盖父配置。可以在 developer_instructions 里要求「不要改文件」，也可以用 features 关掉部分能力，但不会生成单独的只读沙箱。
  - q: 本地 Codex 会不会自己主动派生子 Agent？
    a: 当前本地发布版一般在你明确要求，或项目／Skill 指令要求委托时才会派生。ChatGPT Work 在部分高档位上可以更主动地委托，那是另一套产品行为，不要和本地 Codex 混为一谈。
  - q: 子 Agent 弹出审批时，我还在主线程，怎么处理？
    a: CLI 交互会话里，非当前线程也可以弹出审批；覆盖层会标出源线程。按 o 打开那个线程，再批准、拒绝或回答。非交互流程里如果需要新审批，该操作会失败，错误回到父工作流。
  - q: /subagents 会新开一个子 agent 吗？
    a: 不会。2026-11-06 的斜杠命令文档写，/subagents 打开选择器，用来切换到一条已有的子线程，以便查看或继续它的工作。派生本身靠你在对话里要求，或靠 AGENTS.md、Skill 里的委托说明。
---

# Codex 使用 Subagents 并行处理任务（2026-11 更新）：/subagents、继承沙箱，和主会话怎么分工

> 本文在线版：[codexguide.io/guides/codex-subagents-parallel-work](https://codexguide.io/guides/codex-subagents-parallel-work)

> 核对依据：learn.chatgpt.com《[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)》和《[Slash commands](https://learn.chatgpt.com/docs/cli/slash-commands)》，核对日期 2026-11-06。配置字段又对照了同一天的 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)。文中「我的用法」是操作建议，不是官方规定。本机未对真实多 Agent 会话逐项实测。

主聊天里一边定需求、一边塞满探索笔记、测试日志和堆栈，时间一长，真正有用的约束会被冲淡。官方把这类问题叫 **上下文污染（context pollution）** 和 **上下文腐烂（context rot）**：中间噪声把主线程占满，后续判断更容易偏。

**Subagents** 的做法是：把可并行、噪声大的工作挪到独立线程，只把摘要交回主 Agent。适合代码库探索、测试／日志排查、安全与可维护性审查这类「读得多、结论可并列」的活；并行写同一组文件时要格外小心。

## 先看结论：什么工作交给子 agent，什么留在主会话

主会话留下三样东西：需求、你做过的决定、最后要交付的结果。子 agent 拿走可以并列、噪声大的中间过程，交回短摘要和文件引用。

| 留在主会话 | 交给子 agent | 不要交给子 agent 硬做 |
| --- | --- | --- |
| 完成标准、不能改的接口、你刚拍板的取舍 | 分目录探索、测试日志、崩溃栈、三类只读审查 | 多个线程同时改同一组文件 |
| 看完摘要之后的方案，以及唯一的写入线程 | 等齐再汇总。提示里写明是否等待全部完成 | 后一步必须等前一步的具体输出才能开工 |
| 父会话的沙箱和审批。子线程会继承它 | 在这个权限之内做只读或你允许的工具调用 | 在自定义 TOML 里另写一套沙箱。官方写明写了也不生效 |

本地 Codex 一般要你开口，或项目／Skill 的指令要求委托，才会派生。不要假设它总会自己拆。ChatGPT Work 在 Ultra 上可以更主动地委托，那是 Work 的行为，不要和本地会话混成一件事。

子 agent 各自做模型调用和工具调用，总 token 通常高于同等的单 agent 跑法。额度紧时，只拆真正独立的几块。

## 2026-10 更新说明：自定义 Agent 不能覆盖沙箱和 MCP

旧版本文曾写：自定义 Agent 的 TOML「也可以覆盖模型、沙箱或 MCP 设置」。**后半句与现行官方文档相反，特此更正。**

官方原文要点：

- 自定义 Agent **可以**改模型相关设置和指令，也可以关掉部分受支持的能力。
- 它们 **继承** 父 Agent 的权限、provider 和 MCP 服务器；**自定义 Agent 文件不能覆盖这些设置**。
- 沙箱与审批跟 **父会话**（含 `/permissions`、`--yolo` 等当前回合设置）。自定义指令可以要求「不要编辑文件」，但 **不会** 因此生成单独的只读沙箱。
- 写在自定义文件里的 `sandbox_mode`、`approval_policy`、`model_provider`、`mcp_servers` **不会**覆盖父配置；服务档位也跟根会话。要用 MCP，在 **父会话** 里配好。

下文按同一文档补全：内置 `default`／`worker`／`explorer`、自定义 TOML 必填字段、`[agents]` 全局项、CLI `/subagents`、审批按 `o`，以及用量与并发。

## 什么时候值得用子 Agent

先问一件事：**这几块活是不是互不依赖、也不会抢同一组写入？**

适合并行的例子：

- 对当前分支做安全／测试缺口／可维护性三类只读审查
- 大仓库里分目录或分模块做探索，再汇总调用链
- 测试日志、构建日志、崩溃栈分线程梳理
- 多份文档或规范的对照摘要

不适合硬并行的例子：

- 多个线程同时改同一组文件（冲突和协调成本高）
- 后一步必须等前一步的具体输出才能开工
- 共享一个正在变化的运行状态（同一端口、同一临时库）

官方建议：起步阶段优先用并行做 **读多写少** 的探索、测试、分拣和摘要；**写多** 的并行要更谨慎。

**我的用法（建议）**：所有子 Agent 先只读；主 Agent 看完摘要再定方案，最后由 **一个** 执行线程（或单独的 Worktree 会话）改代码。需要真正隔离写入时，优先看 Worktree 专文，而不是指望「多个子 Agent 各自改盘却互不打架」。

可以这样开口：

```text
请审查当前分支相对 main 的改动。派生三个子 Agent：
1）安全风险 2）测试缺口 3）可维护性。
全部只读、不改文件。等三个都完成，再按类别汇总，并给出文件引用。
```

更好的提示词会写清三件事：**怎么拆**、**是否等齐再继续**、**要交回什么样的摘要**。

## 怎么触发：明确要求，或写进项目／Skill

本地 Codex（桌面 App 聊天、交互式 CLI、IDE 扩展）在当前发布行为下，一般会在你 **直接要求** 派生子 Agent，或适用的 **`AGENTS.md`／Skill 指令** 要求委托时启动多 Agent 流程。

直接说法例如：「spawn two agents」「用子 Agent 并行」「每个检查点一个 Agent」。不要假设它总会自己拆——多数智能档位下要你说清楚；ChatGPT Work 在部分高档位上可以更主动地委托，那是 Work 侧行为。

子 Agent 各自做模型和工具调用，**总 token 通常高于同等单 Agent 跑法**。额度紧时，先拆「真正独立」的几块，并限制并发（见下文 `[agents]`）。

活动会出现在：ChatGPT 桌面 App、Codex CLI、IDE 扩展。主线程负责编排：派生、转发后续指示、等待结果、关闭线程；多 Agent 跑完后汇总成一次回复。

## 内置 Agent：default、worker、explorer

Codex 自带三个内置 Agent：

| 名称 | 官方定位 |
|---|---|
| `default` | 通用兜底 |
| `worker` | 偏执行：实现与修复 |
| `explorer` | 偏只读：代码库探索 |

调用时可以用名字点名，也可以让主 Agent 按任务挑选。若你自定义的 Agent **`name` 与内置同名**（例如也叫 `explorer`），**以你的自定义为准**。

旧文只写「具体可用角色取决于客户端和版本」。现在文档已明确列出上述三者；客户端界面文案仍以你本机版本为准。

## 自定义 Agent：必填字段、能改什么、改不了什么

个人 Agent 放在 `~/.codex/agents/`，项目级放在 `.codex/agents/`。**每个文件定义一个** Agent，格式为 TOML。

### 必填三项

| 字段 | 作用 |
|---|---|
| `name` | 派生和引用时用的名字（以字段为准；文件名与 `name` 对齐最省事） |
| `description` | 给人看的：什么时候该用它 |
| `developer_instructions` | 行为主指令 |

### 模型和推理强度

可用 `model`、`model_reasoning_effort`，以及 `model_reasoning_summary`、`model_verbosity`（取值见配置参考）。

解析顺序（应用自定义文件 **之前**）：

1. 这次派生时的 **显式指定**
2. 否则用 `[agents]` 里的默认
3. 再否则继承 **父 Agent**

若显式派生或 `[agents]` 默认只指定了模型、没有指定推理强度，则用 **该模型自己的默认强度**。自定义文件里若 **只写了 `model`**，会保留前面已经解析好的推理强度；若该模型不支持这个强度，或你想换一档，请在文件里 **同时写** `model_reasoning_effort`。

官方选型提示（账户／工作区需有权限）：多数吃力的工作从 `gpt-6.1-sol` 起；轻量、范围窄、量大的扫描可用更快的 `gpt-6-luna`。`model_reasoning_effort` 常见档位含 `low`／`medium`／`high`，以及更高档的 `xhigh`／`max`／`ultra`（以所选模型是否支持为准）。界面里推理档位常见中文名是 **轻度、中、高、极高**——和配置键不是同一套字符串，写 TOML 时仍用官方英文枚举。

### 可以减弱的能力

把受支持的 feature 设为 `false`，例如：`features.shell_tool`、`features.apps`、`features.plugins`、`features.memories`、`features.request_permissions_tool`。用 `skills.config` 关掉个别 Skill，或 `skills.bundled.enabled = false`；`skills.include_instructions = false` 可去掉自动附带的 Skills 说明块。托管／管理策略要求仍然生效。

Skill 默认从父级继承；自定义 Agent 可以按上面方式再收窄。

### 明确改不了的（再强调一次）

| 写在自定义文件里也无效（相对父配置） | 说明 |
|---|---|
| `sandbox_mode` | 跟父会话沙箱 |
| `approval_policy` | 跟父会话审批 |
| `model_provider` | 跟父 provider |
| `mcp_servers` | 跟父 MCP；要在父会话配置 |

### 最小可复制示例（PR 审查三人组）

项目 `.codex/config.toml`：

```toml
[agents]
max_concurrent_threads_per_session = 8

[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"
```

`.codex/agents/pr-explorer.toml`：

```toml
name = "pr_explorer"
description = "只读探索：在提改动前收集证据与调用链。"
model = "gpt-6-luna"
model_reasoning_effort = "high"
developer_instructions = """
Stay in exploration mode.
Do not edit files.
Trace the real execution path, cite files and symbols, and avoid proposing fixes unless the parent agent asks for them.
Prefer fast search and targeted file reads over broad scans.
"""
```

`.codex/agents/reviewer.toml`：

```toml
name = "reviewer"
description = "PR 审查：正确性、安全、缺测。"
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
developer_instructions = """
Review code like an owner.
Do not edit files.
Prioritize correctness, security, behavior regressions, and missing test coverage.
Lead with concrete findings, include reproduction steps when possible, and avoid style-only comments unless they hide a real bug.
"""
```

提示词可以点名这些 Agent：

```text
对照 main 审查本分支。让 pr_explorer 摸清受影响路径，
reviewer 找真实风险，docs_researcher（若已配置）核对补丁依赖的框架 API。
等齐后按类别汇总。
```

（`docs_researcher` 的完整 TOML 见官方 Subagents 页「Example custom agents」；要点仍是：只读、用父会话已配的 docs MCP。）

## `[agents]` 全局设置：默认模型、推理强度、并发

全局项仍写在配置的 `[agents]` 段（用户或项目 `config.toml`）：

| 字段 | 类型 | 用途 |
|---|---|---|
| `agents.enabled` | boolean | 是否启用多 Agent 工具；默认 `true`，设 `false` 可关掉 |
| `agents.max_concurrent_threads_per_session` | number | 同一会话里同时打开的 **派生** 线程上限（不含主线程）。未设置时由 Codex 选默认；旧键 `agents.max_threads` 仍可用 |
| `agents.default_subagent_model` | string | 派生 Agent 的默认模型 |
| `agents.default_subagent_reasoning_effort` | string | 派生 Agent 的默认推理强度 |
| `agents.interrupt_message` | boolean | 中断回合时是否写入模型可见的中断说明；默认 `true` |

显式派生时的模型／强度，会覆盖 `default_subagent_*`。

社区里曾有人反馈「主模型是 Sol 时，子 Agent 也全被绑成 Sol、没法指定」（例如 openai/codex#31814）。按现行文档，可用 `agents.default_subagent_model` 或自定义 Agent 文件给子 Agent 单独指定模型——这正是该配置存在的原因之一。

**我的用法**：探索类子任务默认 `gpt-6-luna` + 较高推理强度；最终裁定和复杂实现留在主线程或 `worker`／更强模型上。并发先从 3～6 试，而不是一上来拉满。

## 管理子 Agent：`/subagents`、审批按 `o`

| 入口 | 怎么管 |
|---|---|
| **CLI** | `/subagents` 在活跃 Agent 线程间切换、查看进行中线程 |
| **桌面 App** | 主线程会展示子 Agent 活动；可打开子线程查看 |
| **IDE** | 若有后台 Agent 面板，可展开看状态、停止全部活跃子 Agent，或打开单个线程 |
| **口头** | 直接让 Codex 转向某个子 Agent、停止它，或关掉已完成线程 |

ChatGPT Work 网页侧栏主要是只读活动列表，不提供逐个停止／转向的控件（以官方「Managing subagents」为准）。

### 审批：继承父会话，按 `o` 打开源线程

- 子 Agent **继承当前沙箱策略** 与父回合的权限模式；委托前先在父侧选好权限（composer 下方的权限模式，或 CLI 的 `/permissions` 等）。
- 交互式 CLI 里，**非当前线程** 也可能弹出审批；覆盖层会标源线程。按 **`o`** 打开该线程，再批准、拒绝或回答。
- **非交互** 流程，或无法弹出新审批时：需要新审批的操作会 **失败**，错误回到父工作流。

自定义文件里的「请勿编辑」只是指令约束，**不是**另一套沙箱。真要收紧写入，仍改父会话权限，或把写操作留到单独、可控的执行线程／Worktree。

## 用量和磁盘：为什么更费，怎样控并发

每个子 Agent 独立做模型调用和工具调用，所以：

- **Token／额度** 通常高于「同一个主 Agent 串行做完」；并行审查很爽，账单也更陡（社区亦有多开子 Agent 很快打满 Pro 额度的报告，例如 #9748）。
- **磁盘**：子 Agent 工作产物、日志与会话数据可能堆积（有讨论见 #34061）；长期并行时留意 `CODEX_HOME` 与会话清理习惯。

控制办法：

1. 把 `max_concurrent_threads_per_session` 设成你能审得过来的数。
2. 轻量扫描用更便宜／更快的默认子模型（如 `gpt-6-luna`），重活再升档。
3. 提示词要求 **短摘要 + 文件引用**，避免把整份日志打回主线程。
4. 不需要多 Agent 时设 `agents.enabled = false`。

主 Agent 汇总后，仍把子 Agent 摘要当作 **待核验线索**：必要时打开子线程原文，或自己复查文件与命令输出。

## 权限和冲突控制（实操顺序）

1. **父会话**先定沙箱／审批（子 Agent 会继承）。
2. 提示词写明：子任务 **只读**、输出固定字段（范围、发现与路径、用过的命令、未确认项、一句话建议）。
3. 等齐摘要 → 主 Agent（或你）裁定方案。
4. **单个**执行线程改文件；若要并行改不同模块，用 Worktree／独立工作副本隔离，而不是多个子 Agent 抢同一工作树。

固定输出格式能显著降低汇总成本，例如：

```text
每个子任务返回：
- 检查范围
- 发现的问题与文件位置
- 使用过的命令及结果摘要
- 尚未确认的地方
- 一句话建议
全部只读，不修改文件。
```

## 和主会话、Goal、多任务线怎么分工

`/subagents` 不负责派生，也不负责把完成标准挂在对话上。2026-11-06 的斜杠命令文档写的是：输入 `/subagents` 后回车，从选择器里选一条线程，Codex 切到该线程，便于查看或继续。派生仍然用对话里的明确要求，例如「spawn two agents」「每个检查点一个 agent」，或写进适用的 `AGENTS.md`／Skill。

桌面端从主线程展示的活动里打开子线程。IDE 在有后台 agent 面板时，可以展开看状态、停止全部活跃子 agent，或打开单个线程。你也可以直接说：转向某个子 agent、停掉它，或关掉已经完成的线程。

和旁边几篇的边界：

| 你现在的问题 | 用哪篇 |
|---|---|
| 这一条对话的完成标准、暂停和恢复 | [Goal 模式](./08-Codex使用Goal模式运行长任务.md)。`/goal` 挂在主对话上，不挂在每个子线程上 |
| 主会话定方向，`/side` 插问，子 agent 分担，结束前写交接 | [长任务工作流](./05-Codex长任务工作流.md) |
| 子线程的角色、TOML、继承来的沙箱、`/subagents` 切换 | 本文 |
| 会话的命名、恢复、fork、归档 | [管理多条任务线](./03-CodexCLI管理多条任务线.md) |
| 两条对话要同时改不同目录，需要单独的检出 | [Worktree](./10-Codex用Worktree并行运行多个任务.md) |
| 给子任务选模型和推理档 | [模型与推理强度](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md) |

Worktree 解决的是磁盘上的隔离。Subagents 解决的是同一条父会话里的并行委托和摘要回流。自定义 agent 文件里的「不要改文件」只是指令，不会变成另一套只读沙箱。真要并行写，用 worktree 或单独的任务线，不要让多个子 agent 抢同一棵工作树。

生命周期脚本仍然用 Hooks，包括 `SubagentStart` 和 `SubagentStop`。那是护栏，不是派生开关。

## 参考资料

- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Customization](https://learn.chatgpt.com/docs/customization/overview)
