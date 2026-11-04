---
id: codex-plan-mode
title: Codex Plan 模式：先出计划再动手，/plan、Shift+Tab 和三种执行方式
seo_title: Codex Plan 模式：/plan、Shift+Tab 与先计划后执行
description: Plan 模式让 Codex 先读代码、问清需求、写出完整计划，你确认后再改文件。本文讲 /plan 和 Shift+Tab 怎么进入，Plan 模式里能做和不能做的事，计划出来后的三种执行方式，以及怎么单独设置推理强度。
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
date_modified: 2026-11-04
verified_on: 2026-11-04
official_ref: https://learn.chatgpt.com/guides/best-practices
keywords: [Codex Plan 模式, Codex /plan, Codex 计划模式, Codex Shift+Tab, plan_mode_reasoning_effort, Codex 先计划后执行]
related: [permissions-sandbox-approvals, codex-goal-mode-long-running-work]
faq:
  - q: Plan 模式会不会改我的文件？
    a: 按 Codex 0.166.0 源码里的 Plan 模式指令，它只做读文件、搜索、静态分析这类不改动仓库的操作，不编辑文件、不跑会改写文件的格式化工具、不打补丁。这是给模型的规则，官方文档没说 Plan 模式会切换沙箱。需要硬保证，就同时用只读权限。
  - q: 在 Plan 模式里说「直接帮我改」会怎样？
    a: 指令规定，用户在 Plan 模式里要求执行，会被当作「规划这次执行」处理，不会真的去改。要开始实现，就在计划出来后选执行，或者退出 Plan 模式。
  - q: /plan 和 update_plan 是一回事吗？
    a: 不是。Plan 模式是一种协作模式，最后给出一份完整计划。update_plan 是 Codex 在执行任务时更新待办清单的工具，Plan 模式里调用它会报错。
  - q: Plan 模式能单独设推理强度吗？
    a: 能。config.toml 里的 plan_mode_reasoning_effort 只作用于 Plan 模式，不设时用内置的默认值。CLI 里在 Plan 模式下改推理强度时，也可以选只改 Plan 模式，还是同时改全局默认。
---

# Codex Plan 模式：先出计划再动手，/plan、Shift+Tab 和三种执行方式

> 本文在线版：[codexguide.io/guides/codex-plan-mode](https://codexguide.io/guides/codex-plan-mode)

> 核对依据：OpenAI [Best practices](https://learn.chatgpt.com/guides/best-practices) 的 Plan first 一节、[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 里 `/plan` 的条目、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 里的 `plan_mode_reasoning_effort`（2026-11-04 抓取），以及 [openai/codex rust-v0.166.0](https://github.com/openai/codex/tree/rust-v0.166.0/codex-rs) 源码里的 Plan 模式指令模板和计划确认弹窗。编辑部的测试机没有登录 Codex，没有跑一次完整的 Plan 会话，所以本文没有截图，界面文字都照源码原文写。

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
| CLI | 输入 `/plan` 回车；或按 Shift+Tab 切换 |
| CLI 带提示词 | `/plan 为这个服务写一份迁移方案`，后面的文字会作为第一条规划请求 |
| ChatGPT 桌面端 | composer 里也有 `/plan`，说明是「Toggle plan mode for multi-step planning」 |

带提示词的 `/plan` 也可以粘贴内容、附图片。Codex 正在干活时，`/plan` 暂时用不了，等这一轮结束再切。

## Plan 模式里 Codex 会做什么：三个阶段

0.166.0 源码里的 Plan 模式指令（`plan.md` 模板）要求模型分三个阶段，把计划「聊」出来：

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

在 CLI 里确认计划后，会弹出「Implement this plan?」，有三个选项：

| 选项 | 说明 | 实际效果 |
| --- | --- | --- |
| Yes, implement this plan | Switch to Default and start coding | 切回默认模式，在同一个会话里发一句「Implement the plan.」开始实现 |
| Yes, clear context and implement | Fresh thread with this plan | 清空界面，开一个新会话，把计划作为第一条消息发过去 |
| No, stay in Plan mode | Continue planning with the model | 留在 Plan 模式，继续改计划 |

第二个选项的说明里会显示当前上下文用了多少，比如「Start a fresh thread (current context: 89% used)」。新会话收到的消息开头是一段固定说明：

```text
A previous agent produced the plan below to accomplish the user's task. Implement the plan in a fresh context. Treat the plan as the source of user intent, re-read files as needed, and carry the work through implementation and verification.
```

意思是：计划是用户意图的依据，需要时重新读文件，一直做到实现完成并验证过。

怎么选：

- 规划过程很短，上下文还很空：选第一个，省事。
- 规划时读了大量文件、聊了很多轮，上下文快满了：选第二个。新会话只带计划，不带前面的探索过程，空间更宽裕。
- 计划还有你不满意的地方：选第三个，接着说哪里要改。改过之后，新的 `<proposed_plan>` 会完整替换旧的。

模板还要求模型在计划末尾不要问「要我开始吗？」。你直接用上面的弹窗，或者退出 Plan 模式再下指令就行。

## 推理强度：plan_mode_reasoning_effort

Plan 模式可以用和平时不同的推理强度。写在 `~/.codex/config.toml`：

```toml
plan_mode_reasoning_effort = "high"
```

配置参考的说明是：这是 Plan 模式专用的推理强度，取值要是当前模型支持的级别；不设时，Plan 模式用内置预设的默认值。

在 CLI 的 Plan 模式里切换推理强度时，0.166.0 会让你选范围：「Apply to Plan mode override」只改 Plan 模式，「Apply to global default and Plan mode override」同时改全局默认和 Plan 模式。

## Plan 模式、update_plan 和 PLANS.md 的区别

| 名字 | 是什么 |
| --- | --- |
| Plan 模式 | 一种协作模式。先问、先查，最后给出一份完整计划，不动手 |
| `update_plan` | Codex 执行任务时更新待办清单和进度的工具。它不会进入或退出 Plan 模式，在 Plan 模式里调用会报错 |
| `PLANS.md` / 执行计划模板 | 你自己写在仓库里的计划模板，用于更长、步骤更多的任务。见官方 Cookbook 的 [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)（该文已标为归档，模型名可能过时，方法仍可参考） |

Best practices 里的第二种做法是让 Codex「面试你」：你只有模糊想法时，让它先提问、质疑你的假设，把想法变具体。这不需要任何开关，直接在提示词里说就行。

一个任务要连续跑很久、需要明确的完成标准时，可以先在 Plan 模式里把计划定下来，再交给 [Goal 模式](../11-自动化与高级工作流/05-Codex使用Goal模式运行长任务.md) 去跑。

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

Plan 出来以后要跑很久的任务，看 [Goal 模式](../11-自动化与高级工作流/05-Codex使用Goal模式运行长任务.md) 和 [长任务工作流](../11-自动化与高级工作流/03-Codex长任务工作流.md)。想让 Plan 阶段一个文件都改不了，先看 [权限沙箱与审批](./06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 参考资料

- [Best practices：Plan first for difficult tasks](https://learn.chatgpt.com/guides/best-practices)
- [Developer commands：Switch to plan mode with /plan](https://learn.chatgpt.com/docs/developer-commands)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)
- [openai/codex rust-v0.166.0 源码](https://github.com/openai/codex/tree/rust-v0.166.0/codex-rs)
