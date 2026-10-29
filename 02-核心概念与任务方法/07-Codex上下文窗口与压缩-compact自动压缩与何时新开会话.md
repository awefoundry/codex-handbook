---
id: codex-context-compaction
title: Codex 上下文窗口与压缩：/compact、自动压缩阈值、/status 查看用量，什么时候该新开会话
seo_title: Codex 上下文窗口与 /compact 自动压缩：阈值、配置与何时新开会话
description: 长任务做到一半，Codex 的上下文会被塞满。本文讲清上下文窗口怎么看、自动压缩在什么时候触发（0.165.0 源码的算法）、/compact 和 /recap 的区别、相关的 config.toml 字段和 Hooks，以及什么时候压缩、什么时候干脆新开会话。
lede: 压缩能让对话继续下去，但它是用摘要换空间，细节会丢。
url: /guides/codex-context-compaction
status: published
section: guides
category: C-cli-app-usage
topic: 任务方法与项目理解
content_type: 解释
source_tag: 官方功能
entry_tags: [CLI, IDE, App]
difficulty: 进阶
order: 7
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-29
date_modified: 2026-10-29
verified_on: 2026-10-29
tested_cli_version: 0.165.0
models: [gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna]
official_ref: https://learn.chatgpt.com/docs/config-file/config-reference
keywords: [Codex 上下文窗口, Codex compact, Codex 自动压缩, model_auto_compact_token_limit, Codex 上下文不够]
faq:
  - q: /compact 和 /recap 有什么区别？
    a: /compact 用一段摘要替换前面的对话，真正腾出上下文空间；/recap 只生成一段对话总结给你看，不压缩上下文。想腾空间用 /compact。
  - q: 自动压缩在什么时候触发？
    a: 按 Codex CLI 0.165.0 源码，阈值取「model_auto_compact_token_limit 配置值」和「上下文窗口的 90%」中较小的一个；没配置时就是窗口的 90%。
  - q: 我的模型上下文窗口到底多大？
    a: 以 Codex 里 /status 显示的为准。官方文档写 GPT-6.1 Sol 在 Codex 默认 50 万 tokens，但 0.165.0 安装包内置的模型目录里 gpt-6.1-sol 是 27.2 万；登录后 Codex 会从服务端刷新模型目录，实际值可能和内置值不同。
  - q: 压缩以后 AGENTS.md 里的规则还在吗？
    a: 压缩针对的是对话历史。如果担心压缩后丢了某些约定，可以用 SessionStart Hook 匹配 source 为 compact 的情况，在压缩后重新注入需要的上下文。
---

# Codex 上下文窗口与压缩：/compact、自动压缩阈值、/status 查看用量，什么时候该新开会话

> 本文在线版：[codexguide.io/guides/codex-context-compaction](https://codexguide.io/guides/codex-context-compaction)

> 核对依据：OpenAI 官方文档 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)、[Hooks](https://learn.chatgpt.com/docs/hooks) 和 [Models](https://learn.chatgpt.com/docs/models)；自动压缩阈值的算法来自 Codex 源码 [`codex-rs/protocol/src/openai_models.rs`（rust-v0.165.0）](https://github.com/openai/codex/blob/rust-v0.165.0/codex-rs/protocol/src/openai_models.rs)。各模型的窗口数值用 Linux 上的 `codex-cli 0.165.0` 运行 `codex debug models --bundled` 读取。本机没有登录，没有跑真实的长对话压缩，也没有 `/status` 截图。核对日期 2026-10-29（北京时间）。

## 一句话结论

- **上下文窗口**是模型一次能「看到」的 token 总量，对话、读过的文件、命令输出都占地方。用 `/status` 看还剩多少。
- **自动压缩**：快满时 Codex 会自动把前面的对话换成摘要。0.165.0 的阈值是「你配置的值」和「窗口的 90%」取小。
- **手动压缩**用 `/compact`；只想看总结、不想压缩，用 `/recap`。
- 压缩是用摘要换空间，细节会丢。**换了一件事做，就新开会话**，别靠压缩硬撑。

## 上下文里装了什么

一次对话里，下面这些都算进上下文：

- 系统指令和 AGENTS.md 等项目规则
- 你发的每条消息
- Codex 的回复和思考过程里需要保留的部分
- 它读过的文件内容、跑过的命令输出、工具调用结果

所以「我才说了几句话就满了」很常见：一次 `cat` 大文件、一次输出很长的测试，都会占掉大量空间。单个工具输出能在历史里保留多少，由 `tool_output_token_limit` 控制（见下文配置表）。

上下文给多少才合适，是另一个问题：窗口装得下，不等于装进去有帮助。见[给 Codex 多大上下文才够用](../03-项目理解与上下文/04-给Codex多大上下文才够用.md)。

## 怎么看还剩多少

**`/status`**：显示当前会话的模型、审批策略、可写目录和 token 用量。官方命令表写明它可以用来确认「剩余的上下文容量」。任务运行中也能用。

**`/statusline`**：把上下文、用量上限、token 等信息固定显示在终端底部的状态栏，选好后写进 `config.toml`。长任务时开着比较方便。状态栏和其他终端界面设置见官方 [CLI customization](https://learn.chatgpt.com/docs/cli-customization)。

## 每个模型的窗口有多大

用 0.165.0 安装包自带的模型目录（不联网刷新）查看：

```bash
codex debug models --bundled
```

摘几个常用模型的字段：

| 模型 | `context_window` | `max_context_window` | 按源码算出的自动压缩阈值（90%） |
|---|---|---|---|
| `gpt-6.1-sol` | 272,000 | 872,000 | 244,800 |
| `gpt-6.1-terra` | 500,000 | 872,000 | 450,000 |
| `gpt-6-luna` | 272,000 | 872,000 | 244,800 |

**注意，这里和官方文档有出入**：官方 [Models](https://learn.chatgpt.com/docs/models) 页写的是「GPT-6.1 Sol 在 Codex 和 ChatGPT Work 中默认上下文窗口为 500,000 tokens」，而 0.165.0 内置目录里 `gpt-6.1-sol` 是 272,000。官方 Developer commands 文档说明，不加 `--bundled` 时 `codex debug models` 会从远程模型接口刷新目录，所以登录后的实际值可能和内置值不同。本文没有登录验证，**请以你自己 `/status` 里显示的为准**。

两个字段的区别：

- `context_window`：默认使用的窗口大小。
- `max_context_window`：允许你在配置里调到的最大值（对应 `model_context_window`）。

## 自动压缩什么时候触发

Codex 0.165.0 源码里的算法（`ModelInfo::auto_compact_token_limit`）：

1. 先取模型的窗口：有 `context_window` 用它，没有就用 `max_context_window`。
2. 算出窗口的 90%。
3. 如果你配置了 `model_auto_compact_token_limit`，取它和这个 90% 中**较小**的一个；没配置就用 90%。

也就是说，**这个配置只能把阈值调低，不能调到超过窗口的 90%**。

还有一个相关的值 `effective_context_window_percent`，0.165.0 内置目录里所有模型都是 95，表示窗口里有 95% 可用于输入，剩下的留给系统提示、工具开销和模型输出。它是模型目录里的字段，官方 Configuration Reference 里没有对应的配置项。

## /compact：手动压缩

官方文档的步骤：

1. 对话进行了很久以后，输入 `/compact`。
2. Codex 提示要总结之前的对话时，确认。

结果：Codex 用一段简洁的摘要替换前面的轮次，腾出上下文，同时保留关键信息。

几点注意：

- **任务运行中不能用**。按 0.165.0 源码，`/compact` 不在「任务进行中可用」的命令里。可以按 `Tab` 把它排进下一轮。
- IDE 扩展里也有 `/compact`（「Compact the current chat's context」）。
- 压缩用的提示词可以换：`compact_prompt` 直接写在配置里，或用 `experimental_compact_prompt_file` 指向一个文件（实验功能）。

## /recap：只总结，不压缩

`/recap` 在 Codex 空闲时生成一段当前对话的总结，**不压缩上下文**。官方文档原话：想腾空间时用 `/compact`。

另外，`tui.auto_recap` 默认是 `true`：终端窗口失去焦点时，Codex 会自动生成对话回顾。不想要可以设为 `false`，`/recap` 仍然能用。

## 相关配置一览

以下字段来自官方 Configuration Reference，写在 `~/.codex/config.toml`（或项目的 `.codex/config.toml`）：

| 字段 | 类型 | 作用 |
|---|---|---|
| `model_context_window` | 数字 | 当前模型可用的上下文窗口 token 数 |
| `model_auto_compact_token_limit` | 数字 | 触发自动压缩的 token 阈值；不设就用模型默认值 |
| `model_auto_compact_token_limit_scope` | `total` \| `body_after_prefix` | 阈值按整个上下文算（`total`，默认），还是只算压缩摘要之后新增的部分（`body_after_prefix`） |
| `compact_prompt` | 字符串 | 直接替换压缩用的提示词 |
| `experimental_compact_prompt_file` | 路径 | 从文件加载压缩提示词（实验功能） |
| `tool_output_token_limit` | 数字 | 单个工具或函数输出在历史里最多保留多少 token |
| `tui.auto_recap` | 布尔 | 终端失焦时自动生成回顾，默认 `true` |
| `model_providers.<id>.capabilities.remote_compaction` | `unsupported` \| `v2` | 自定义模型提供商的压缩方式：`unsupported` 在本地压缩，`v2` 通过 Responses 接口触发压缩 |

一个想更早压缩的例子（数值只是示意，按你的模型窗口调整）：

```toml
# 比默认的 90% 更早触发自动压缩
model_auto_compact_token_limit = 200000
```

按上面的算法，这个值超过窗口 90% 时会被压回 90%，不会生效。配置文件的分层和覆盖关系见[Codex config.toml 深入配置](../10-配置模型与权限安全/08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 用 Hooks 管住压缩

官方 [Hooks](https://learn.chatgpt.com/docs/hooks) 文档提供了三个和压缩有关的时机：

| Hook | 什么时候跑 | 能做什么 |
|---|---|---|
| `PreCompact` | 压缩之前 | `matcher` 匹配 `trigger`（`manual` 或 `auto`）；返回 `continue: false` 时，Codex 在压缩前停下 |
| `PostCompact` | 压缩之后 | 同样按 `manual` / `auto` 匹配；返回 `continue: false` 时，Codex 压缩后停下 |
| `SessionStart`（`source: "compact"`） | 压缩后、下一次请求模型之前 | 用 `additionalContext` 重新注入需要的上下文。任务中途自动压缩时，这段内容会直接交给紧接着的继续执行 |

常见用法：压缩前把当前进度写进一个文件；压缩后用 `SessionStart` 把「项目约定」「当前任务目标」重新塞回去。Hooks 的配置方式和信任机制见[Codex Hooks 入门](../11-自动化与高级工作流/08-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。

## 压缩还是新开会话

压缩适合**同一件事还没做完**的情况。下面几种情况，新开会话通常更好：

| 情况 | 建议 |
|---|---|
| 同一个任务还在做，只是上下文快满了 | 让它自动压缩，或者在一个阶段结束时手动 `/compact` |
| 已经压缩过好几次，Codex 开始忘记前面的约定 | 让它先把当前进度和下一步写成一段交接说明，然后 `/new` 新开对话，把交接说明发过去 |
| 换了一件不相关的事 | 直接 `/new` 或 `/clear`，别把上一件事的历史带过去 |
| 想试另一种做法，又不想丢掉当前进度 | `/fork` 分出一条新对话 |
| 只是想插问一个小问题 | `/side` 开一个临时旁支对话，不影响主对话 |
| 任务很大，可以拆开 | 用 Subagents 把独立的部分交给子 Agent，主对话只收结果 |

多条对话的命名、恢复和交接见[Codex CLI 管理多条任务线](../11-自动化与高级工作流/02-CodexCLI管理多条任务线.md)；拆给子 Agent 的做法见[Codex Subagents 怎么用](../11-自动化与高级工作流/06-Codex使用Subagents并行处理任务.md)。

## 少占上下文的习惯

- 让 Codex 读文件时指明范围（某个函数、某几行），别让它整个读大文件。
- 跑测试时只跑相关的那部分，或者让它只看失败的输出。
- 一个阶段结束时主动 `/compact`，比等到自动压缩更可控：你知道摘要发生在什么位置。
- 重要的约定写进 AGENTS.md 或项目文件，而不是只在对话里说一次。

## 下一步

- 上下文给多少才够用：[给 Codex 多大上下文才够用](../03-项目理解与上下文/04-给Codex多大上下文才够用.md)
- 多条任务线怎么管：[Codex CLI 管理多条任务线](../11-自动化与高级工作流/02-CodexCLI管理多条任务线.md)
- 压缩前后跑脚本：[Codex Hooks 入门](../11-自动化与高级工作流/08-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)
- 斜杠命令速查：[Codex CLI 斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)

## 参考资料

- OpenAI 官方文档：[Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- OpenAI 官方文档：[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- OpenAI 官方文档：[Hooks](https://learn.chatgpt.com/docs/hooks)
- OpenAI 官方文档：[Models](https://learn.chatgpt.com/docs/models)
- Codex 源码：[openai_models.rs（rust-v0.165.0）](https://github.com/openai/codex/blob/rust-v0.165.0/codex-rs/protocol/src/openai_models.rs)
