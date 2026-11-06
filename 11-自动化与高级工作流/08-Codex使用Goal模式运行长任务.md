---
id: codex-goal-mode-long-running-work
title: Codex 使用 Goal 模式运行长任务（2026-11 更新）：/goal 启动、暂停恢复，和 Plan、长任务工作流怎么分工
seo_title: Codex Goal 模式：/goal 启动、暂停恢复，和 Plan 怎么分工
description: 任务要跑很久时，用 /goal 把完成标准挂在当前对话上。本文按 2026-11-06 的官方文档说明怎么启动、暂停、恢复和并行，以及它和 Plan 模式、长任务工作流怎么分工。
lede: Goal 管的是这一条对话的完成标准。计划还没定时用 Plan。主会话、侧边提问和子任务怎么摆，看长任务工作流。
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
date_modified: 2026-11-06
verified_on: 2026-11-06
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/long-running-work
keywords: [Codex Goal 模式, Codex /goal, Codex 长任务, Goal pause resume, Codex Plan]
related: [codex-plan-mode, codex-long-task-collaboration-workflow, codex-subagents-parallel-work]
howto: false
faq:
  - q: /goal 的目标最长能写多少？
    a: 官方斜杠命令文档写明，目标不能为空，最多 4,000 个字符。更长的说明放进文件，让目标指向那个文件。
  - q: 开了 Goal，Codex 会获得更大的权限吗？
    a: 不会。Long-running work 写明它沿用当前的沙箱和审批策略，需要你做决定时会暂停。
  - q: 先 /plan 再 /goal，和直接 /goal 有什么差别？
    a: 结果、约束和验证都已经能写死时，直接 /goal。还要先问清约束时，官方建议先 /plan，整理成可衡量的目标后再 /goal。Codex 已经在干活时，/plan 暂时不可用。
  - q: goals.max_goal_token_budget 要不要填一个数？
    a: 配置参考把它定义成正整数：新 Goal 的默认 token 预算，以及一个 Goal 能请求的上限。不写这项，就是没有配置过的限制。Long-running work 没有要求在目标文本里写预算。本文没有在本机改过这个字段。
---

# Codex 使用 Goal 模式运行长任务（2026-11 更新）：/goal 启动、暂停恢复，和 Plan、长任务工作流怎么分工

> 本文在线版：[codexguide.io/guides/codex-goal-mode-long-running-work](https://codexguide.io/guides/codex-goal-mode-long-running-work)

> 核对依据：OpenAI 官方文档 [Long-running work](https://learn.chatgpt.com/docs/long-running-work)、[Slash commands in Codex CLI](https://learn.chatgpt.com/docs/cli/slash-commands) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)，核对日期 2026-11-06。本文没有在登录状态下跑一个 Goal。命令和字段均引自上述文档。`tested_cli_version` 仍是 2026-10-24 那次文章所记的 0.164.0，这次没有用更新的 CLI 复测。

适合任务会跨很多步、你又怕它跑着跑着改了验收标准的人。短修改不必开 Goal。

## 先看结论：什么时候该开 Goal

Goal 不是另一条对话，也不是更大的权限。官方的定义是：目标文本既是第一条提示，也是这项任务的完成标准。Codex 在同一条对话的上下文里决定下一步，以及什么时候算做完。

用它，当这三件事同时成立：

- 交付物已经能说清；
- 约束已经能写下来，例如只改哪些目录、不能改哪些接口；
- 完成与否可以由测试、类型检查或一份你写明的审阅标准来判断。

先不要开，当：

- 几分钟就能改完；
- 需求还在变，成功标准没法检查；
- 你其实想先看一份计划，再决定做不做。这种情况用 [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md)。

主会话里还要插问、把只读调查分出去、最后留交接记录时，顺序看[长任务工作流](./05-Codex长任务工作流.md)。那篇管整段工作怎么摆，本文只管 `/goal` 这一层。

## 启动：`/goal`，以及先 `/plan` 再转 Goal

三个入口都可以开。网页版 ChatGPT 没有 `/goal`。官方建议网页上的长任务用 ChatGPT Work，把结果、约束和审阅标准直接写进提示词。

| 入口 | 怎么开 | 开了之后怎么管 |
| --- | --- | --- |
| ChatGPT 桌面端 | 输入框输入 `/goal` | 输入框上方出现进度条，可以暂停、继续、编辑或清除 |
| Codex CLI | 交互会话里输入 `/goal` | 同一会话里继续发消息，或用下面的子命令 |
| IDE 扩展 | 对话框输入 `/goal`，作用于当前打开的工作区 | 同一条对话里继续调整。运行期间保持工作区可用 |

CLI 里的子命令（2026-11-06 的斜杠命令文档）：

| 命令 | 作用 |
| --- | --- |
| `/goal <目标>` | 设置目标。文档中的例子是 `/goal Finish the migration and keep tests green` |
| `/goal` | 查看当前目标 |
| `/goal edit` | 修改目标 |
| `/goal pause` | 暂停 |
| `/goal resume` | 继续 |
| `/goal clear` | 清除目标 |

文档写的预期是：目标挂在当前对话上，工作继续时仍然带着它。目标不能为空，最多 4,000 个字符。更长的背景、清单和接口说明放进仓库里的文件，让目标指向这个文件：

```text
/goal 按 docs/migration-plan.md 完成 checkout 模块的错误处理迁移，完成标准见该文件的“验收”一节
```

配置项 `features.goals` 在配置参考里的描述是：Enable persisted goals and automatic continuation (stable; on by default)。也就是稳定功能，默认开启。一般不用为了使用 Goal 去手动打开它。

目标还说不清楚时，官方建议先 `/plan`：让 Codex 问你问题、找出约束，把讨论收成一个带可衡量成功标准的目标，然后再用 `/goal` 启动。斜杠命令文档补充了一点：Codex 已经在干活时，`/plan` 暂时不可用。所以顺序是先计划，再开 Goal，而不是等它跑起来再补一次 `/plan`。

Plan 模式里能做和不能做的事、Shift+Tab，以及计划之后的三种执行方式，都在 [Plan 一文](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md)。本文不重复。

## 定义完成标准：结果、约束、验证

官方建议目标里写清三件事（适用时才写）：

| 要素 | 写什么 |
| --- | --- |
| 结果 | 你要的结果，而不只是让它做什么动作 |
| 约束 | 必须用的工具、边界、兼容性要求、要避开的做法 |
| 验证 | 能证明做完了的测试、指标或审阅标准 |

官方例子：

```text
Migrate this codebase from JavaScript to TypeScript. Preserve existing behavior,
compile in strict mode without explicit `any` types, and make the full test suite pass.
```

拆开看：结果是迁到 TypeScript；约束是保持现有行为，并且不用显式的 `any`；验证是 strict 模式能编译，完整测试套件通过。

一个中文例子：

```text
/goal 把 checkout 模块迁移到新的错误处理方式。只改 src/checkout 和对应测试，不改公共 API。完成条件：npm test 和 npm run typecheck 全部通过，最终报告列出没有覆盖到的边界情况。
```

写的时候注意：

- 验证要能由 Codex 自己跑。「测试通过」「类型检查通过」可以；「看起来没问题」不行。
- 只写「一直做到完成」而没有停止条件，时间会花在低价值的细节上。
- Goal 不会替你补上还没定的产品决定。没定的地方先用 `/plan` 或直接讨论。

配置参考里还有 `goals.max_goal_token_budget`，类型是正整数。官方的说明是：它同时作为新 Goal 的默认 token 预算，以及一个 Goal 能请求的上限。不写这项，Goal 就没有配置过的限制。Long-running work 没有要求你在 `/goal` 的文本里写一个预算数字。本文没有在本机设置过这个字段，也不给一个建议值。

## 运行中：暂停、恢复、编辑、清除

桌面端的进度条在输入框上方。用它暂停、继续、编辑或清除。也可以在 Goal 还在跑的时候再发消息，补充上下文或改约束。

CLI 用上一节的 `/goal pause`、`/goal resume`、`/goal edit`、`/goal clear`。想看进度，就在同一会话里让它先总结再继续。IDE 同样留在原来的对话里调整，并保持工作区可用。

不打断主对话时，桌面端可以开侧边对话，问进度或请它解释。CLI 里对应 `/side`（别名 `/btw`）。侧边对话不能再套一层 `/side`，审查模式里也不能用。侧边对话和主目标怎么配合，长任务工作流一文写得更完整。

预计要断网或合上电脑时，先暂停，准备好了再恢复。桌面端做本地长任务时，可以在设置里打开 Prevent sleep while running，让 Mac 不休眠。CLI 的 `/experimental` 列表里也有这一项。再配合 Pets 或系统通知，在对话需要输入或可以审阅时提醒你。本文没有切换这项设置。

清除目标用 `/goal clear` 或桌面端进度条上的清除。清除之后，这条对话不再带着完成标准。它不会撤销已经改过的文件。文件要不要留，看 Git diff，不看 Goal 还在不在。

## 并行 Goal 与权限

开启 Goal 不会给 Codex 更大的权限。它沿用当前的沙箱和审批，需要你做决定时会暂停。开了自动审批审查时，由单独的审查者评估符合条件的请求，同样不会扩大边界。生产环境、密钥、付款、删除数据和系统权限，该停下来等你的地方仍然会停。权限怎么收，见[权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

每条对话有自己的上下文、消息、结果和目标，所以多条对话可以同时跑，各自带一个 Goal。不要让两条对话改同一批文件。并行写代码时，用 Git worktree 给每条对话单独的检出目录。

一条任务内部的并行只读调查，用子 agent，不需要为每个调查再开一个 Goal。见 [Subagents](./09-Codex使用Subagents并行处理任务.md)。

## 和 Plan、长任务工作流、Subagents 怎么分工

三篇容易叠在一起。按你手里的问题选，不要三篇同时当成操作手册：

| 你现在的问题 | 读哪篇、用哪个命令 |
| --- | --- |
| 还不知道要改哪些文件，想先看计划 | [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md)。`/plan` 或 Shift+Tab。计划可以再转成 Goal |
| 完成标准已经能写死，希望这一条对话一直对着它做 | 本文。`/goal`，需要时暂停、恢复、编辑 |
| 主会话要保持方向，临时问题不想写进主记录，只读调查要分出去，结束前要留交接 | [长任务工作流](./05-Codex长任务工作流.md)。里面会用到 `/side`、子 agent 和审查 |
| 主会话快被日志和探索笔记淹没 | [Subagents](./09-Codex使用Subagents并行处理任务.md)。`/subagents` 只是在子线程之间切换 |
| 会话断了，想从上次的记录接着做 | [恢复长任务](./04-CodexCLI恢复长任务.md)。恢复的是会话，不是自动再创建一个 Goal |

一套能对上官方文档的顺序是：`/plan` 把目标和约束问清；你确认后 `/goal` 把完成标准挂上；跑的过程中用 `/side` 问一句不影响主记录的问题；互不依赖的只读调查交给子 agent；两个 Goal 要同时改代码时，各自用 worktree。本文没有把这套顺序在登录环境里跑通。

## 什么时候不该用 Goal

- 小改动，开 Goal 的说明比改动本身还长。
- 成功标准里还有「等产品决定」的空档。
- 你需要的是手机上回一句，或者让 Dot 跟进一条已有线程。那是另一篇里的通知和 Dot，不改变这条对话的 Goal。

判断标准仍然是：目标稳定、过程能拆开、结果能验证。三条里缺一条，就先 Plan 或先写长任务工作流里的主会话说明，不要先挂上 Goal。

## 参考资料

- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/cli/slash-commands)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)（`features.goals`、`goals.max_goal_token_budget`）
- [Prompting：Goal mode](https://learn.chatgpt.com/docs/prompting#goal-mode)
- [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
