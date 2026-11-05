---
id: codex-goal-mode-long-running-work
title: Codex Goal 模式：用 /goal 跑长任务，完成标准怎么写、怎么暂停和并行
seo_title: Codex Goal 模式：/goal 长任务的完成标准、暂停与并行
description: Goal 是附着在当前对话上的持续目标，目标文本同时是第一条提示和完成标准。本文按官方文档讲清 /goal 的命令、怎么用结果、约束、验证三要素写目标、运行中怎么调整和暂停、权限边界，以及用 worktree 并行跑多个 Goal。
url: /guides/codex-goal-mode-long-running-work
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-13
date_modified: 2026-10-24
verified_on: 2026-10-24
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/long-running-work
keywords: [Codex Goal, /goal, Goal 模式, Codex 长任务, 完成标准, Codex 并行任务]
related: [codex-cli-resume-long-task, codex-subagents-parallel-work]
howto: false
faq:
  - q: /goal 的目标最长能写多少？
    a: 官方文档写明目标不能为空，最多 4,000 个字符。更长的说明放进文件，让目标指向那个文件。
  - q: 开了 Goal，Codex 会获得更大的权限吗？
    a: 不会。Goal 沿用当前的沙箱和审批策略，需要你做决定时会暂停。
  - q: 能同时跑多个 Goal 吗？
    a: 能。每个对话有自己的上下文和目标，可以同时运行；但不要让两个对话改同一批文件，并行写代码时用 Git worktree 给每个对话单独的检出目录。
---

# Codex Goal 模式：用 /goal 跑长任务，完成标准怎么写、怎么暂停和并行

> 本文在线版：[codexguide.io/guides/codex-goal-mode-long-running-work](https://codexguide.io/guides/codex-goal-mode-long-running-work)

> 核对依据：OpenAI 官方文档 [Long-running work](https://learn.chatgpt.com/docs/long-running-work)、[Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)，核对日期 2026-10-24。本文没有在登录状态下实际跑一个 Goal，命令和界面说明均引自官方文档。

如果你已经会让 Codex 改代码，但任务一长就容易跑偏，可以试试 Goal 模式。它适合有明确交付物、能持续验证的工作，比如迁移、重构、排错和发布前检查。

Goal 不是一次性提示词，而是**附着在当前对话上的持续目标**。官方文档的说法是：目标文本**既是第一条提示，也是这个任务的完成标准**。Codex 会在同一个对话的上下文里决定下一步做什么、什么时候算做完。

## 在哪里用、怎么开

Goal 在三个入口都可以用：

| 入口 | 怎么开 | 运行中怎么管 |
| --- | --- | --- |
| ChatGPT 桌面端 | 输入框里输入 `/goal` | 输入框上方出现进度条，可以暂停、继续、编辑或清除 |
| Codex CLI | 交互会话里输入 `/goal` | 在同一会话里继续发消息调整，或让它汇报进度 |
| IDE 扩展 | 对话框里输入 `/goal`，作用于当前打开的工作区 | 在同一对话里继续调整；运行期间保持工作区可用 |

网页版 ChatGPT 没有 `/goal`。官方建议在网页里用 ChatGPT Work，把结果、约束和审阅标准直接写进提示词。

Goal 由配置项 `features.goals` 控制，官方配置参考里的描述是「Enable persisted goals and automatic continuation (stable; on by default)」，也就是稳定功能、默认开启，一般不用手动打开。

## /goal 命令

CLI 里的用法（来自官方 Slash commands 文档）：

| 命令 | 作用 |
| --- | --- |
| `/goal <目标>` | 设置目标，例如 `/goal Finish the migration and keep tests green` |
| `/goal` | 查看当前目标 |
| `/goal edit` | 修改目标 |
| `/goal pause` | 暂停 |
| `/goal resume` | 继续 |
| `/goal clear` | 清除目标 |

目标**不能为空，最多 4,000 个字符**。更长的说明，比如背景、检查清单、接口文档，放进项目里的文件，让目标指向这个文件：

```text
/goal 按 docs/migration-plan.md 完成 checkout 模块的错误处理迁移，完成标准见该文件的“验收”一节
```

## 先 /plan，再 /goal

目标还说不清楚时，官方建议先用 `/plan`：让 Codex 来问你问题、找出约束，把讨论结果整理成一个有可衡量成功标准的目标，然后再用 `/goal` 启动。

这一步花几分钟，能省掉 Goal 跑偏后返工的时间。

## 完成标准怎么写：结果、约束、验证

官方建议目标里写清三件事（适用时）：

| 要素 | 写什么 |
| --- | --- |
| **结果（Outcome）** | 你要的结果，而不只是让它做什么动作 |
| **约束（Constraints）** | 必须用的工具、边界、兼容性要求、要避开的做法 |
| **验证（Verification）** | 能证明做完了的测试、指标或审阅标准 |

官方例子：

```text
Migrate this codebase from JavaScript to TypeScript. Preserve existing behavior,
compile in strict mode without explicit `any` types, and make the full test suite pass.
```

拆开看：

- 结果：代码库从 JavaScript 迁到 TypeScript；
- 约束：保持现有行为，不用显式的 `any`；
- 验证：strict 模式编译通过，完整测试套件通过。

一个中文写法示例：

```text
/goal 把 checkout 模块迁移到新的错误处理方式。只改 src/checkout 和对应测试，不改公共 API。完成条件：npm test 和 npm run typecheck 全部通过，最终报告列出没有覆盖到的边界情况。
```

写的时候注意：

- **验证要能由 Codex 自己跑**。“测试通过”“类型检查通过”可以；“看起来没问题”不行。
- 只写“一直做到完成”而没有停止条件，Goal 容易把时间花在低价值的细节上。
- Goal 不会替你补上模糊的产品决策。需求没定的地方，先讨论清楚。

## 运行中怎么调整

- **补充或修改**：在同一个对话里继续发消息，补充上下文、调整约束。也可以 `/goal edit` 直接改目标。
- **看进度**：让 Codex 汇报一下进度，它会先总结再继续。
- **不打断主对话**：桌面端可以开一个侧边对话（side chat）问进度或请它解释，不影响主对话。CLI 里对应的是 `/side`（或 `/btw`），开一个临时的侧边对话。
- **要断网或合上电脑前**：先暂停 Goal，准备好了再继续。

桌面端在本地跑长任务时，可以在设置里打开 **Prevent sleep while running**，让 Mac 不休眠；再配合 Pets 或系统通知，在对话需要你输入或已经可以审阅时提醒你。

## 权限边界：Goal 不会放大权限

官方文档写得很明确：**开启 Goal 不会给 Codex 更大的权限**。

- 它沿用当前的沙箱和审批策略；
- 需要你做决定时会暂停；
- 开了自动审批审查（auto-review）时，由一个单独的审查者评估符合条件的请求，但同样不会扩大边界。

所以涉及生产环境、密钥、付款、删除数据或系统权限的步骤，该有的人工批准仍然会有。Goal 暂停不是失败，看一下进展，补充约束后继续就行。权限怎么设，见[权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 并行跑多个 Goal

每个对话有自己的上下文、消息、结果和目标，所以多个对话可以同时跑，各自带一个 Goal。

唯一要避免的：**两个对话改同一批文件**。并行写代码时，用 [Git worktree](https://learn.chatgpt.com/docs/environments/git-worktrees) 给每个对话一个独立的检出目录。

在一个任务内部拆分并行子任务，是另一种做法，见 [Codex Subagents 并行处理任务](./09-Codex使用Subagents并行处理任务.md)。

## 什么时候不该用 Goal

- 几分钟就能做完的小修改；
- 需求还没定、成功标准没法检查；
- 需要不断做产品判断的任务。

这几种情况先讨论或 `/plan`，不用急着开 Goal。

判断标准很简单：**目标稳定、过程能拆开、结果能验证**。三点都满足，长任务才值得交给 Goal 持续推进。

任务中途断了、想从之前的会话接着做，见 [Codex CLI 恢复长任务](./04-CodexCLI恢复长任务.md)。

## 参考资料

- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Prompting：Goal mode](https://learn.chatgpt.com/docs/prompting#goal-mode)
- [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
