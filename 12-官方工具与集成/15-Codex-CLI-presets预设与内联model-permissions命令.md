---
id: codex-cli-presets-inline-model
title: Codex CLI /presets 预设与内联 /model、/permissions：0.164.0 一条命令切换模型、推理强度和权限
seo_title: Codex CLI /presets 预设与内联 /model、/permissions 用法（0.164.0）
description: Codex CLI 0.164.0 新增 /presets 十个预设槽，/model 和 /permissions 也能直接带参数。本文用实测说明怎么保存常用命令、用 ctrl-x p 和数字键调出，以及内联切换模型、推理强度、速度和权限时哪些只影响当前会话。
url: /guides/codex-cli-presets-inline-model
status: published
section: guides
category: C-cli-app-usage
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 15
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-24
date_modified: 2026-10-24
verified_on: 2026-10-24
tested_cli_version: 0.164.0
models: [gpt-6.1-sol, gpt-6-luna]
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.164.0
keywords: [Codex CLI presets, /presets, /model --reasoning, /permissions :read-only, Codex 0.164.0, tui.presets]
related: [codex-model-reasoning-effort, config-toml-guide]
howto: false
faq:
  - q: 用 /model 带参数切换后，下次启动还会保留吗？
    a: 不会。0.164.0 的内联 /model 只改当前会话，界面会提示 for this session only，config.toml 里保存的默认模型不变。
  - q: /presets 保存在哪里？
    a: 保存在当前用户配置的 tui.presets 下，实测写成 [tui.presets.1] 这样的表，包含 input 和 label 两个字段。
  - q: 打开预设菜单的快捷键是什么？
    a: 默认是 leader p。0.164.0 默认 leader 键是 ctrl-x，所以是 ctrl-x 再按 p；也可以在 tui.keymap.chat.open_presets 里改，用 /keymap 查看当前绑定。
---

# Codex CLI /presets 预设与内联 /model、/permissions：0.164.0 一条命令切换模型、推理强度和权限

> 本文在线版：[codexguide.io/guides/codex-cli-presets-inline-model](https://codexguide.io/guides/codex-cli-presets-inline-model)

> 核对依据：Codex CLI 0.164.0 [发布说明](https://github.com/openai/codex/releases/tag/rust-v0.164.0)（2026-10-23 12:48 北京时间发布）和对应的 4 个 PR；实测环境是 Linux 上的 `codex-cli 0.164.0`，用独立的 `CODEX_HOME`，没有登录 OpenAI 账号，只验证本地命令和配置写入，没有发出真实模型请求。核对日期 2026-10-24。

在 CLI 里换模型、改推理强度、切权限，以前要打开 `/model` 或 `/permissions` 的选择器，一层层选。0.164.0 加了两件事：

- `/model` 和 `/permissions` 可以直接带参数，一条命令完成切换；
- `/presets` 提供 10 个编号槽位，把常用的提示词或斜杠命令存起来，按数字键就能再次运行。

这篇讲这两个功能怎么用、哪些设置只影响当前会话、预设存在哪里。

## 0.164.0 加了什么

发布说明 New Features 的前两条：

- Save reusable prompts and slash commands in ten numbered `/presets` slots, with a keyboard menu for quick access.（[#54380](https://github.com/openai/codex/pull/54380)、[#54381](https://github.com/openai/codex/pull/54381)）
- Set model, reasoning effort, speed, and permission profiles directly with inline `/model` and `/permissions` arguments.（[#54378](https://github.com/openai/codex/pull/54378)、[#54383](https://github.com/openai/codex/pull/54383)）

Codex 负责人 Tibo 在 [10 月 24 日的帖子](https://x.com/thsottiaux/status/2113770862860222611)里也专门提到这几项：「We've added reusable prompt presets, inline model and permission settings…」。

先确认版本：

```bash
codex --version
# codex-cli 0.164.0
```

低于 0.164.0 时，下面的内联参数和 `/presets` 都不可用。截至核对日，官方 [Slash commands 文档](https://learn.chatgpt.com/docs/developer-commands?surface=cli) 还没有写这两个功能，本文的用法来自发布说明、PR 描述和实测。

## 内联 /model：一条命令切换模型、推理强度和速度

格式（来自 PR #54378）：

```text
/model [模型] --reasoning <推理强度> --speed <速度档>
```

- 三个部分都可以省略。不写模型时，设置作用在当前模型上；只输入 `/model` 仍然打开原来的选择器。
- 参数可以用空格写，也可以用等号写：`--reasoning high` 和 `--reasoning=high` 都可以。
- 只改当前会话，不改你保存的默认值。

几个例子：

```text
/model gpt-6.1-sol --reasoning high
/model --reasoning=low
/model gpt-6-luna --speed=standard
```

实测切换成功后，对话里会出现一行提示，结尾是 **for this session only**（下面是把模型切到 high 推理强度时的输出）：

```text
• Model changed to openai.gpt-6.1-sol high standard for this session only
```

（实测环境的模型目录来自 Amazon Bedrock provider，所以模型名带 `openai.` 前缀。用 ChatGPT 登录时，模型名是 `gpt-6.1-sol` 这类写法，以 `/model` 选择器里显示的为准。）

切换后 `config.toml` 没有任何变化。下次启动 Codex，仍然用配置文件里的默认模型。

### 写错了会怎样

PR #54378 写明，Codex 会先校验模型是否可用、推理强度和速度档是否受支持，服务端接受后三项一起生效。写了不支持的值时，会直接报错并列出可用的值。实测输入一个不存在的推理强度：

```text
/model --reasoning=turbo
■ Reasoning level 'turbo' is unavailable for openai.gpt-6.1-sol. Available: low, medium, high, xhigh, max, ultra.
```

可用的推理强度和速度档由模型目录决定，不同模型、不同账号看到的不一样。不确定时故意写错一次，看报错里列出的值就行。官方 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 对 `model_reasoning_effort` 的说明也是「Available levels depend on the model and client」。

PR 里还列出了几种会被拒绝的写法：未知参数、同一参数写两次、参数后面没跟值。

### 速度档

`--speed` 用来选速度档（service tier），可选的档位同样由模型目录决定，用写错一次的办法就能看到。官方 [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) 文档写明，Fast 模式对支持的模型按 Standard 的 2.5 倍消耗订阅额度，购买的 credits 和企业按量付费按 2 倍计费。如果只想开关 Fast，用原来的 `/fast` 也可以。

切换会话（thread）时，每个会话会恢复自己的速度档；新会话使用配置里的默认值，不会沿用当前会话的速度（PR #54378）。

## 内联 /permissions：直接选权限配置

格式（来自 PR #54383）：

```text
/permissions <权限配置 ID>
```

官方 [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) 写明内置的权限配置有三个：`:read-only`、`:workspace`、`:danger-full-access`。你在 `config.toml` 里用 `[permissions.<name>]` 定义的自定义配置也可以直接选。

PR 里还提到两个审批相关的别名：`:ask-for-approval` 和 `:approve-for-me`。

实测切换到只读：

```text
/permissions :read-only
• Permission selection requested: Read Only
```

之后运行 `/status`，Permissions 一行显示：

```text
Permissions:         Read Only (Ask for approval)
```

需要注意的几点：

- 选 `:danger-full-access` 这类完全访问配置时，仍然要你确认，内联写法不会跳过这一步。
- 切换请求还没确认时，排队的输入会先等着；取消或失败后，排队的输入会保留，不会丢（PR #54383）。
- 和 `/model` 一样，实测 `/permissions` 切换后 `config.toml` 没有改动。

权限配置各自允许什么，见[权限、沙箱和审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## /presets：10 个预设槽

`/presets` 可以保存两类内容：普通提示词，或者一条斜杠命令（比如上面的内联 `/model`）。一共 10 个槽，编号 1–9 和 0。

### 打开预设菜单

两种方式：

- 输入 `/presets` 回车；
- 按快捷键 **leader p**。0.164.0 默认的 leader 键是 `ctrl-x`，所以就是先按 `ctrl-x` 再按 `p`。

实测在 `/keymap` 里能看到这一行：

```text
Chat           Open Presets               leader p (ctrl-x p)
```

想换成别的键，在 `config.toml` 里设置 `tui.keymap.chat.open_presets`。如果 `leader p` 和你已有的绑定冲突，或者你显式设置了这个动作，Codex 就不会再自动加 `leader p`。

### 菜单里的按键

第一次打开，菜单是空的：

```text
  Presets
  No presets saved. Press n to create one.
  n · new   s · from settings   e · edit   d · delete   esc · close
```

| 按键 | 作用 |
| --- | --- |
| `0`–`9` | 运行该槽位的预设；槽位为空时新建 |
| `n` | 新建预设 |
| `s` | 从当前设置新建（当前模型、权限、终端标题、状态栏） |
| `e` | 编辑预设 |
| `d` | 删除预设（替换和删除前会确认） |
| `esc` | 关闭菜单 |

### 从当前设置新建

按 `s` 后，Codex 会把当前状态转成对应的斜杠命令，供你选择。实测看到 4 项：

```text
  Start preset from current settings
  Current model           /model openai.gpt-6.1-sol --speed=standard
  Current permissions     /permissions :workspace --approval-policy=… --reviewer=user
  Current terminal title  /title …
  Current status line     /statusline …
```

（审批参数、标题和状态栏的参数较长，这里用 … 省略。）

选 Current model 后进入编辑框，可以继续改。实测在末尾加上 `--reasoning=high`，回车后出现 **Save preset to slot** 列表，从 1–9、0 里选一个槽位。保存后提示：

```text
• Saved preset 1.
```再打开菜单按 `1`，命令立即执行：

```text
• Model changed to openai.gpt-6.1-sol high standard for this session only
```

运行预设时，你在输入框里还没发出去的草稿会保留（PR #54380、#54381）。

## 预设保存在哪

PR #54380 写明预设保存在当前用户配置的 `tui.presets` 下。实测保存 1 号槽后，`$CODEX_HOME/config.toml`（默认 `~/.codex/config.toml`）里多了这一段：

```toml
[tui.presets.1]
input = "/model openai.gpt-6.1-sol --speed=standard --reasoning=high"
label = ""
```

据此可以知道：

- **预设是持久的**，重启后还在；而预设里的 `/model`、`/permissions` 命令执行后只影响当前会话。这两点不冲突：保存的是“命令”，不是“设置”。
- 预设写在用户配置里，不在项目的 `.codex/config.toml` 里。想在团队里共享，可以把命令文本写进项目文档，各自保存。
- 写入失败时，内存里的设置保持不变（PR #54380）。
- 不要把密钥、token 或带个人信息的长提示词存进预设，它们会以明文留在 `config.toml` 里。

## 三个常用组合

下面的命令只是示例，模型名请换成你 `/model` 选择器里能看到的：

| 场景 | 预设内容 | 说明 |
| --- | --- | --- |
| 只读审查 | `/permissions :read-only` | 先看代码、不改文件 |
| 日常开发 | `/model gpt-6.1-sol --reasoning=medium` | 平衡速度和质量 |
| 难题深挖 | `/model gpt-6.1-sol --reasoning=high` | 复杂排错、架构分析 |

还可以存一条常用提示词，比如“检查当前改动并说明每处修改的原因”。推理强度怎么选，见 [Codex 模型和推理强度怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

## 常见问题

**输入 `/presets` 没反应或提示未知命令。** 先运行 `codex --version`，确认是 0.164.0 或更新版本。

**`ctrl-x p` 不起作用。** 打开 `/keymap` 查看 Open Presets 的实际绑定。你可能改过 leader 键，或者别的动作占了这个组合。

**内联 `/model` 提示模型不可用。** 报错以 `is unavailable. Use /model to see available models.` 结尾。模型名必须和 `/model` 选择器里显示的一致，不确定时先只输入 `/model` 打开选择器看一眼。

**想让新会话默认用某个模型。** 内联 `/model` 做不到，要改 `config.toml` 的 `model` 和 `model_reasoning_effort`。见 [config.toml 配置指南](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 参考资料

- [Codex CLI 0.164.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.164.0)
- [#54380 Add `/presets` for reusable prompts and slash commands](https://github.com/openai/codex/pull/54380)
- [#54381 Add a keyboard shortcut menu for presets](https://github.com/openai/codex/pull/54381)
- [#54378 Support inline model, reasoning, and speed selection in `/model`](https://github.com/openai/codex/pull/54378)
- [#54383 Support inline permission profile selection with `/permissions`](https://github.com/openai/codex/pull/54383)
- [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
