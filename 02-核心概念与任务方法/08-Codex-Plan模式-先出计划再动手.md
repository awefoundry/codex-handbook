---
id: codex-plan-mode
title: Codex Plan 模式：0.169 起「清空上下文后执行」会把完整计划交给新会话，交接失败时原会话保留
seo_title: Codex Plan 模式：/plan、Shift+Tab 与先计划后执行
description: Plan 模式让 Codex 先读代码、问清需求，你确认后再改文件。0.169.0 起「Yes, clear context and implement」会把完整的已批准计划交给新会话；交接失败时留下当前会话。弹窗上的三句英文选项与 0.166.0 相同。
lede: 复杂任务先计划，这是官方 Best practices 里排第一的做法。Plan 模式把「先问清楚」变成一个开关。
url: /guides/codex-plan-mode
status: published
section: guides
category: B-core-concepts
topic: 核心概念与任务方法
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 入门
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-04
date_modified: 2026-11-16
verified_on: 2026-11-16
official_ref: https://learn.chatgpt.com/guides/best-practices
keywords: [Codex Plan 模式, Codex /plan, Codex 计划模式, Codex Shift+Tab, plan_mode_reasoning_effort, Codex 先计划后执行]
related: [permissions-sandbox-approvals, codex-goal-mode-long-running-work, codex-context-compaction, codex-plannotator-plan-review]
faq:
  - q: Plan 模式会不会改我的文件？
    a: 按 Codex rust-v0.169.0 的 plan.md 模板，它只做读文件、搜索、静态分析这类不改动仓库的操作，不编辑文件、不跑会改写文件的格式化工具、不打补丁。这是给模型的规则，官方文档没说 Plan 模式会切换沙箱。需要硬保证，就同时用只读权限。
  - q: 在 Plan 模式里说「直接帮我改」会怎样？
    a: 指令规定，用户在 Plan 模式里要求执行，会被当作「规划这次执行」处理，不会真的去改。要开始实现，就在计划出来后选执行，或者退出 Plan 模式。
  - q: /plan 和 update_plan 是一回事吗？
    a: 不是。Plan 模式是一种协作模式，最后给出一份完整计划。update_plan 是 Codex 在执行任务时更新待办清单的工具，Plan 模式里调用它会报错。
  - q: Plan 模式能单独设推理强度吗？
    a: 能。config.toml 里的 plan_mode_reasoning_effort 只作用于 Plan 模式，不设时用内置的默认值。CLI 里在 Plan 模式下改推理强度时，也可以选只改 Plan 模式，还是同时改全局默认。
---

# Codex Plan 模式：0.169 起「清空上下文后执行」会把完整计划交给新会话，交接失败时原会话保留

> 本文在线版：[codexguide.io/guides/codex-plan-mode](https://codexguide.io/guides/codex-plan-mode)

> 核对依据：OpenAI [Best practices](https://learn.chatgpt.com/guides/best-practices) 的 Plan first 一节、[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 里 `/plan` 的条目、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 里的 `plan_mode_reasoning_effort`（2026-11-16 抓取），[rust-v0.169.0 Release](https://github.com/openai/codex/releases/tag/rust-v0.169.0) 的 Bug Fixes，以及该标签源码里的 `plan.md`、`plan_implementation.rs` 和计划确认弹窗快照。[#60763](https://github.com/openai/codex/pull/60763) 写明交接方式。测试机没有登录 Codex，没有跑一次完整的 Plan 会话，所以本文没有截图。界面上的三句选项照 0.169.0 源码原文写，和 0.166.0 那一版相同。

## 先看结论：什么任务该先 Plan

官方 Best practices 的说法是：任务复杂、需求模糊或者不好描述时，先让 Codex 做计划再写代码。它列了三种做法，排第一的就是 Plan 模式，原话是「For most users, this is the easiest and most effective option」，对大多数用户来说最简单也最有效。

适合先 Plan 的情况：

- 要改好几个模块，或者要动接口、数据结构；
- 你只有一个大概的想法，说不清具体要什么；
- 改错了代价高，比如数据迁移、权限逻辑、对外接口；
- 你想先看 Codex 打算怎么改，再决定交给它，还是自己动手。

改一个错别字、补一个单测这种小事，不必 Plan。

## 怎么进入：/plan、Shift+Tab、App composer

| 入口 | 做法 |
| --- | --- |
| CLI | 输入 `/plan` 回车。这是 Developer commands 写明的步骤 |
| CLI 循环协作模式 | Shift+Tab。0.169.0 源码里这是保留动作 `fixed.cycle_collaboration_mode`，在协作模式之间循环，不是文档里的 `/plan` 专用键 |
| CLI 带提示词 | `/plan 为这个服务写一份迁移方案`，后面的文字会作为第一条规划请求 |
| ChatGPT 桌面端 | composer 里也有 `/plan`，说明是「Toggle plan mode for multi-step planning」 |

带提示词的 `/plan` 也可以粘贴内容、附图片。Codex 正在干活时，`/plan` 暂时用不了，等这一轮结束再切。

## Plan 模式里 Codex 会做什么：三个阶段

rust-v0.169.0 的 Plan 模式指令（`codex-rs/collaboration-mode-templates/templates/plan.md`）仍要求模型分三个阶段，把计划「聊」出来：

1. **先摸清环境。** 能从仓库里查到的事实，先自己查，不问你。比如某个结构体在哪、用的是哪个组件。指令要求问你任何问题之前，至少先做一轮有针对性的只读探索。
2. **再问清意图。** 一直问到能说清楚：目标和完成标准、给谁用、做什么不做什么、约束、现状、取舍偏好。高影响的问题没问清，就不出计划。
3. **最后敲定实现。** 方案、接口、数据流、边界情况和失败处理、测试和验收标准、上线和监控、迁移和兼容问题，都要定下来。

提问时优先用 `request_user_input` 工具，给你几个有意义的选项，并标出推荐项。偏好类的问题你没回答，它就按推荐项继续，并把这个选择写进最终计划的假设里。

最终计划要做到「decision complete」，也就是执行的人不用再做任何决定。计划放在一个 `<proposed_plan>` 块里，客户端会单独渲染。模板建议的结构是 3–5 个短节，一般是 Summary、Key Changes（或 Implementation Changes）、Test Plan、Assumptions。

## 能做什么、不能做什么，以及它不是沙箱

模板把操作分成两类：

| 允许（不改动仓库） | 不允许（改动仓库） |
| --- | --- |
| 读文件、搜索配置、schema、类型、文档 | 编辑或新建文件 |
| 静态分析、浏览仓库 | 跑会改写文件的格式化工具或 linter |
| 不改受版本管理文件的 dry-run 命令 | 打补丁、跑迁移、生成会写入仓库的代码 |
| 测试、构建、检查（写缓存或 `target/` 之类的产物可以） | 目的是「把活干了」而不是「把计划做好」的命令 |

拿不准时的判断标准是：这个操作更像「在干活」还是「在做计划」，像干活就不做。

还有一条：Plan 模式不会因为你的语气改变。你在 Plan 模式里说「直接改吧」，它会把这句话当作「规划这次执行」。

要注意，**这些是给模型的指令，不是权限设置**。官方文档没有说 Plan 模式会改变沙箱或审批策略。测试和构建命令照样会跑，可能写缓存目录，也可能访问网络（看你的权限设置）。想确保一个文件都不会被改，就在 Plan 之前把权限设成只读，见 [权限沙箱与审批](./06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 计划出来以后：三种执行方式

在 CLI 里确认计划后，会弹出「Implement this plan?」。rust-v0.169.0 的 `plan_implementation.rs` 和弹窗快照里，三个选项的英文没有改：

| 选项 | 说明 | 0.169.0 源码里的动作 |
| --- | --- | --- |
| Yes, implement this plan | Switch to Default and start coding | 切回默认模式，在同一个会话里提交「Implement the plan.」 |
| Yes, clear context and implement | Fresh thread with this plan | 把完整的已批准计划交给一个新会话。交接成功之后才清空界面并换到新会话 |
| No, stay in Plan mode | Continue planning with the model | 留在 Plan 模式，继续改计划 |

第二个选项有上下文用量时，说明变成「Start a fresh thread (current context: 89% used)」这种句子。快照里的 `89% used` 是测试文案，不是固定百分比。

0.166.0 会把整份计划连同一段固定前言，当作新会话的第一条用户消息。那段前言（「A previous agent produced the plan below…」）在 0.169.0 的 `plan_implementation.rs` 里已经删掉。Release 的 Bug Fixes 写明：**Yes, clear context and implement** 现在把完整的已批准计划交给新会话；交接失败时保留当前会话（[#60763](https://github.com/openai/codex/pull/60763)）。

该 PR 和 0.169.0 源码把交接写成这几步：

1. 先准备一个新会话，来源标记是 `ThreadStartSource::Clear`。准备失败就在当前会话报错，不切走。
2. 把已批准计划写成附件 `approved-plan.md`，放在 Codex 家目录下的 `attachments/<随机目录>/`。写失败只记一条调试日志，交接仍继续。
3. 调用 `thread/prepareApprovedPlan`。新会话的执行器能读到这份文件、内容与计划一致时，交给模型的用户消息是 `Read the approved plan at <路径> and implement it.` 测试快照把路径写成 `<PLAN_FILE>`。
4. 附件写不了或读不到时，改把完整计划作为 `proposed_plan` 的工具输出放进模型上下文，用户消息是 `Implement the plan.` 源码里的回退上限是 10,000 token、最多 32 段，并且不超过该模型可用窗口的四分之一。
5. 完整计划放不进这个上限时，请求失败，错误原文是：`The executor could not read the plan attachment and the complete plan is too large to send as context. Implement it in the original thread.` 界面上的句子是 `Failed to hand off the approved plan:` 加上这个原因。当前会话保留，不清空。
6. 只有准备成功，才清空终端界面并换到新会话。

本文没有登录，没有走通一次真实交接，所以上面是源码和 PR 说明，不是一次会话记录。

怎么选：

- 规划过程很短，上下文还很空：选第一个，省事。
- 规划时读了大量文件、聊了很多轮，上下文快满了：选第二个。新会话带的是这份已批准计划，不带前面的探索过程。上下文怎么看，见 [上下文窗口与压缩](./07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md)。
- 计划还有你不满意的地方：选第三个，接着说哪里要改。改过之后，新的 `<proposed_plan>` 会完整替换旧的。想在浏览器里划线批注再把意见送回来，用 [Plannotator](../09-MCP与外部工具/23-Codex安装Plannotator-浏览器批注计划与代码审查并回传反馈.md)。那是第三方 Stop hook，不是这个弹窗。

模板仍要求模型在计划末尾不要问 “should I proceed?”。你直接用上面的弹窗，或者退出 Plan 模式再下指令就行。

## 推理强度：plan_mode_reasoning_effort

Plan 模式可以用和平时不同的推理强度。写在 `~/.codex/config.toml`：

```toml
plan_mode_reasoning_effort = "high"
```

配置参考的说明是：这是 Plan 模式专用的推理强度，取值要是当前模型支持的级别；不设时，Plan 模式用内置预设的默认值。

配置键仍在。0.166.0 的界面会在切换推理强度时让你选「Apply to Plan mode override」或「Apply to global default and Plan mode override」。这次对照 rust-v0.169.0 时没有重新定位到这两句文案，所以不把它们写成 0.169.0 的现状。

## Plan 模式、update_plan 和 PLANS.md 的区别

| 名字 | 是什么 |
| --- | --- |
| Plan 模式 | 一种协作模式。先问、先查，最后给出一份完整计划，不动手 |
| `update_plan` | Codex 执行任务时更新待办清单和进度的工具。它不会进入或退出 Plan 模式，在 Plan 模式里调用会报错 |
| `PLANS.md` / 执行计划模板 | 你自己写在仓库里的计划模板，用于更长、步骤更多的任务。见官方 Cookbook 的 [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)（该文已标为归档，模型名可能过时，方法仍可参考） |

Best practices 里的第二种做法是让 Codex「面试你」：你只有模糊想法时，让它先提问、质疑你的假设，把想法变具体。这不需要任何开关，直接在提示词里说就行。

一个任务要连续跑很久、需要明确的完成标准时，可以先在 Plan 模式里把计划定下来，再交给 [Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md) 去跑。上下文已经快满、又要按这份计划开工时，用上面的「清空上下文后执行」，并先看 [压缩与新开会话](./07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md)。

## 写好一次 Plan 请求的例子

```text
/plan 给订单服务加一个按状态批量导出的接口。
背景：现在只能逐条查，运营每周要导一次。
约束：不改现有接口的返回格式；导出要分页，单次最多 5000 条。
完成标准：新接口有测试覆盖，现有测试全部通过。
先告诉我你需要哪些信息，再出计划。
```

这和 Best practices 推荐的提示词结构一致：目标、背景、约束、完成标准。最后一句是让它先问。按指令，Plan 模式本来就会先问，写上这句只是更明确。

## 常见问题

**切不进 Plan 模式。** 官方命令文档写明，Codex 正在运行一轮任务时 `/plan` 暂时不可用，等这一轮结束再试。Shift+Tab 在运行中是否同样受限，文档没有写。

**计划太长了。** 模板要求计划默认简洁，只写执行需要的信息。你可以直接说「压缩到一屏」，它会给出一份完整替换的新计划。

**它一直在问，问个没完。** 指令要求每个问题都必须会实质改变计划、确认一个假设，或者在有意义的取舍之间选择。你觉得够了，就直接说「其余按你的推荐来」，它会把这些写成假设。

**IDE 扩展里能用吗？** 官方命令文档列出了 CLI 和桌面端 composer 的 `/plan`，没有单独写 IDE 扩展。本文没有在 IDE 里验证过。

## 下一步

Plan 出来以后要跑很久的任务，看 [Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md) 和 [长任务工作流](../11-自动化与高级工作流/05-Codex长任务工作流.md)。想让 Plan 阶段一个文件都改不了，先看 [权限沙箱与审批](./06-权限沙箱与审批-什么时候放行什么时候收紧.md)。想在浏览器里批注计划再送回 Codex，看 [Plannotator](../09-MCP与外部工具/23-Codex安装Plannotator-浏览器批注计划与代码审查并回传反馈.md)。

## 参考资料

- [Best practices：Plan first for difficult tasks](https://learn.chatgpt.com/guides/best-practices)
- [Developer commands：Switch to plan mode with /plan](https://learn.chatgpt.com/docs/developer-commands)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)
- [openai/codex rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
- [PR #60763：把已批准计划交给新会话](https://github.com/openai/codex/pull/60763)
