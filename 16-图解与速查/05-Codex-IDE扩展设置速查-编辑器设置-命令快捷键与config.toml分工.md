---
id: codex-ide-extension-settings
title: "Codex IDE 扩展设置速查：chatgpt.* 编辑器设置、命令快捷键绑定，和 config.toml 各管什么"
seo_title: "Codex IDE 扩展设置速查：chatgpt.* 与 config.toml"
description: "Codex IDE 扩展的设置分两层：模型、权限、MCP 等写在与 CLI 共用的 config.toml，编辑器里的行为用 chatgpt.* 设置。本文按官方页面列出 8 个编辑器设置的默认值和适用场景，并说明怎样给 Codex 命令绑快捷键。"
lede: "改模型、沙箱和 MCP，去 config.toml。改回车发送、排队还是侧边栏，去编辑器设置里搜 chatgpt。"
url: /guides/codex-ide-extension-settings
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 参考
source_tag: 官方功能
entry_tags: [IDE]
difficulty: 入门
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-23
date_modified: 2026-11-23
verified_on: 2026-11-23
official_ref: "https://learn.chatgpt.com/docs/developer-settings?surface=ide"
keywords: [Codex IDE 扩展设置, Codex VS Code 设置, chatgpt.followUpQueueMode, Codex 回车发送, Codex VS Code 快捷键]
related: [codex-vscode-install, codex-cli-slash-commands, codex-config-toml-cheatsheet]
howto: true
faq:
  - q: chatgpt.* 能写进 config.toml 吗？
    a: 不能。Developer settings 写明 chatgpt.* 属于 IDE 扩展，不写入 config.toml。模型、推理强度、权限、沙箱、MCP 和个人化才读 config.toml，并与 CLI 共用。
  - q: 回车是发送还是换行？
    a: 默认 chatgpt.composerEnterBehavior 是 enter，回车发送。要改成多行时用 Cmd/Ctrl+Enter 发送，选 cmdIfMultiline；要每次都用修饰键发送，选 cmdAlways。2026-11-23 的扩展 manifest 里这三项和默认值与文档一致。
  - q: 运行中再发一条消息，会打断当前任务吗？
    a: 默认 followUpQueueMode 是 queue，等下一轮。steer 会引导当前这一轮。文档写旧值 interrupt 会按 steer 处理。扩展 manifest 的可选值里仍然有 interrupt。单条消息可以用 Cmd/Ctrl+Shift+Enter 临时反过来。
  - q: 这篇有没有在 VS Code 里点过这些设置？
    a: 没有。写作环境没有打开 VS Code 或兼容编辑器。8 个键来自官方 Developer settings，并与 Marketplace 上 openai.chatgpt 26.51117.41037 的 manifest 对照过。
---

# Codex IDE 扩展设置速查：chatgpt.* 编辑器设置、命令快捷键绑定，和 config.toml 各管什么

> 核对依据：2026-11-23 打开的 [Developer settings（IDE）](https://learn.chatgpt.com/docs/developer-settings?surface=ide) 和 [Developer commands（IDE）](https://learn.chatgpt.com/docs/developer-commands?surface=ide)。扩展包对照的是 Visual Studio Marketplace 上 `openai.chatgpt` **26.51117.41037**（`lastUpdated` `2026-11-20T23:47:02.413Z`）的 manifest，以及 Open VSX 上同一版本号（`timestamp` `2026-11-20T23:02:48.027681Z`）。没有打开 VS Code、Cursor 或 Windsurf，没有改过本机编辑器设置，没有配图。

Codex 装进编辑器之后，设置不在同一个地方。模型、权限和 MCP 跟 CLI 共用 `config.toml`。侧边栏、回车和审查结果放在哪个对话里，用编辑器自己的 `chatgpt.*`。写错层，改了也不会生效。

扩展怎么安装，见 [VS Code 和兼容编辑器安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md)。`config.toml` 的字段见 [config.toml 常用字段速查](./02-Codex-config.toml常用字段与环境变量速查.md)。命令 ID 的完整表在 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)，本文不重复那张表。

## 两层设置各管什么

[Developer settings](https://learn.chatgpt.com/docs/developer-settings?surface=ide) 把 IDE 扩展分成两层：

| 层 | 存在哪 | 管什么 |
|---|---|---|
| Codex settings | `config.toml` | 模型、推理强度、权限、沙箱、MCP、个人化。与 Codex CLI 共用 |
| Editor settings | 编辑器设置里的 `chatgpt.*` | 扩展在 VS Code 及兼容编辑器里的行为 |

`chatgpt.*` 不要写进 `config.toml`。共享的代理设置用 [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)、[Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 和 [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)。

同一页还写：扩展会沿用 VS Code 内置的聊天字体设置来显示 Codex 的聊天区域。那两项不是 `chatgpt.*`，见下一节表格后面。

## 打开设置的两个入口

**Codex settings。** 官方页面的步骤是：在 Codex 侧边栏点齿轮图标，再选 **Codex Settings**。常用代理选项在这个面板里改；选 **Open config.toml** 会打开当前生效的那一层配置文件。本文没有打开侧边栏，没有看到齿轮的中文译名。界面若是中文，以你编辑器里的实际文字为准，英文名用来和文档对照。

**Editor settings。**

1. 打开编辑器设置。
2. 搜索 `@ext:openai.chatgpt`、`Codex`，或设置名。
3. 改值。

`@ext:openai.chatgpt` 是编辑器用来筛选这个扩展的搜索串，不是 `config.toml` 里的键。

## 8 个编辑器设置

下表的默认值和含义来自 2026-11-23 的 Developer settings。可选值若文档没有写成枚举，表里就不补。

| 设置 | 默认 | 可选或取值 | 什么时候改 |
|---|---|---|---|
| `chatgpt.commentCodeLensEnabled` | `true` | 文档未列其他值 | 不想在 `TODO` 注释上方看到让 Codex 处理的 CodeLens 时关掉 |
| `chatgpt.openOnStartup` | `false` | 文档未列其他值 | 希望扩展启动结束后焦点就在 Codex 侧边栏 |
| `chatgpt.followUpQueueMode` | `queue` | `queue`、`steer`；旧值 `interrupt` 按 `steer` 处理 | 任务还在跑时，新消息是排队（`queue`）还是引导当前这一轮（`steer`） |
| `chatgpt.composerEnterBehavior` | `enter` | `enter`、`cmdIfMultiline`、`cmdAlways` | 回车直接发送，还是多行时才要修饰键，还是每次都要修饰键 |
| `chatgpt.reviewDelivery` | `inline` | `inline`、`detached` | `/review` 尽量留在当前对话，还是另开一个审查对话 |
| `chatgpt.localeOverride` | 空，自动检测。文档表里写 Auto | 文档没有列出语言代码 | 要固定 Codex 界面语言时再填。留空就自动检测 |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | `false` | 仅 Windows，且本机有 WSL | 仓库和工具在 WSL2，或需要 Linux 工具。改它会重新加载 VS Code |
| `chatgpt.cliExecutable` | 未设置 | 一个可执行文件路径 | 只有在开发 Codex CLI 时才设置。文档写手动覆盖自带的可执行文件可能导致扩展的一部分不能工作 |

`followUpQueueMode` 还有一个单次例外：按 `Cmd`/`Ctrl`+`Shift`+`Enter`，这一条消息使用和当前设置相反的行为。

同一张官方表还列了两个 VS Code 聊天字体项，它们不是 `chatgpt.*`：

| 设置 | 默认 | 作用 |
|---|---|---|
| `chat.fontSize` | 编辑器默认 | Codex 侧边栏里的聊天正文和输入框 |
| `chat.editor.fontSize` | 编辑器默认 | 聊天里渲染出来的代码和 diff |

2026-11-23 下载的 `openai.chatgpt` 26.51117.41037 manifest 里，`contributes.configuration` 正好是上面 8 个 `chatgpt.*`。默认值与文档一致：`commentCodeLensEnabled` 为 `true`，`openOnStartup` 为 `false`，`followUpQueueMode` 为 `queue`，`composerEnterBehavior` 为 `enter`，`reviewDelivery` 为 `inline`，`runCodexInWindowsSubsystemForLinux` 为 `false`，`localeOverride` 和 `cliExecutable` 没有默认值。`followUpQueueMode` 的 `enum` 是 `queue`、`steer`、`interrupt`。文档说旧的 `interrupt` 按 `steer` 处理，扩展仍把它留在可选值里。`chat.fontSize` 和 `chat.editor.fontSize` 不在这个扩展的 configuration 里。

manifest 的 `engines.vscode` 是 `^1.96.2`。这是包声明的引擎范围，不是本文在某个 VS Code 版本上打开过的记录。

不一致时以官方 Developer settings 页为准。这次 8 个键的名字和默认值没有对不上。

## 常见需求对照

**回车发送，Shift+Enter 换行。** 保持默认 `chatgpt.composerEnterBehavior = enter`。文档对 `enter` 的说明是回车始终发送。

**回车换行，用 Cmd 或 Ctrl+Enter 发送。** 多行提示才需要修饰键时，选 `cmdIfMultiline`。每次都要修饰键，选 `cmdAlways`。文档没有把「Shift+Enter 换行」写成一个单独的设置项，所以这里不补一个文档里没有的键。

**任务还在跑，新消息不要插进去。** `followUpQueueMode` 用默认 `queue`。希望这条消息改变当前这一轮，用 `steer`，或只对一条消息按 `Cmd`/`Ctrl`+`Shift`+`Enter`。

**`/review` 不要占着当前对话。** `chatgpt.reviewDelivery` 改为 `detached`，文档的说法是另开一个审查对话。默认 `inline` 是尽量在当前对话里跑。审查命令本身见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

**Windows 上仓库在 WSL 里。** 打开 `chatgpt.runCodexInWindowsSubsystemForLinux`。文档写仅 Windows、本机要有 WSL，改完会重新加载 VS Code。本文的环境是 Linux，没有 WSL，没有执行这个开关。

**界面语言。** `chatgpt.localeOverride` 留空则自动检测。文档没有给出 `zh-CN` 这类取值表，本文不编语言代码。manifest 的说明是 “Preferred language for the Codex UI. Leave empty to auto detect.”

## 给 Codex 命令绑快捷键

[Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=ide) 的步骤：

1. 打开命令面板。macOS 是 `Cmd+Shift+P`，Windows 和 Linux 是 `Ctrl+Shift+P`。
2. 运行 **Preferences: Open Keyboard Shortcuts**。
3. 搜索 `Codex` 或命令 ID，例如 `chatgpt.newChat`。
4. 点铅笔图标，输入要绑定的快捷键。

官方表里的命令 ID 是 `chatgpt.addToThread`、`chatgpt.addFileToThread`、`chatgpt.newChat`、`chatgpt.newCodexPanel`、`chatgpt.openCommandMenu`、`chatgpt.openSidebar`。默认快捷键只有 `chatgpt.newChat`：macOS `Cmd+N`，Windows 和 Linux `Ctrl+N`。其余在文档表里是 `-`。完整中文对照在 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

26.51117.41037 的 manifest 里这 6 个 ID 都在。另外还有 `chatgpt.implementTodo`，以及 `chatgpt.dumpNuxState`、`chatgpt.resetNuxState` 两条标题以 Debug 开头的命令。Developer commands 页的表没有写这三条。`chatgpt.newChat` 的键是 `ctrl+n`，mac 是 `cmd+n`，`when` 为 `chatgpt.supportsNewChatKeyShortcut`。文档表没有写这个 when 条件。键位以你快捷键设置里的当前绑定为准；when 条件来自这份 manifest，不是来自文档表。

IDE 里的 `/status`、`/review` 这类斜杠命令是在 Codex 输入框里用的，不是编辑器快捷键。那张表也在 01/14，不在这里重复。

## 改了不生效时查什么

先确认改的是哪一层：

- 模型、审批、沙箱、MCP 没变：看 `config.toml`，不是 `chatgpt.*`。字段怎么写见 [config.toml 速查](./02-Codex-config.toml常用字段与环境变量速查.md)。CLI 和 IDE 扩展读的是同一套 Codex settings。
- 回车、排队、CodeLens、启动时是否聚焦侧边栏没变：在编辑器设置里搜 `@ext:openai.chatgpt`，确认改的是扩展设置，而不是把 `chatgpt.composerEnterBehavior` 写进了 `config.toml`。
- 只在 Windows 上想走 WSL：看 `chatgpt.runCodexInWindowsSubsystemForLinux`。文档写改这个设置会重新加载 VS Code。其他 `chatgpt.*` 页面没有逐项写「必须重启」。
- 扩展行为异常，而且你填过 `chatgpt.cliExecutable`：这是开发 CLI 用的路径。文档写不需要它，除非你正在开发 Codex CLI；手动覆盖自带可执行文件可能让扩展的一部分不能工作。不确定时清空它。
- 快捷键按了没反应：用 Preferences: Open Keyboard Shortcuts 看这个命令 ID 当前绑定，以及有没有别的命令占用同一组键。`chatgpt.newChat` 在这份 manifest 里还带 when 条件。

本文没有在编辑器里逐项切换这些值，所以上面是文档和 manifest 能支持的检查，不是一次「改完立刻看到界面变化」的记录。

## 参考资料

- [Developer settings（IDE）](https://learn.chatgpt.com/docs/developer-settings?surface=ide)
- [Developer commands（IDE）](https://learn.chatgpt.com/docs/developer-commands?surface=ide)
- [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [VS Code 和兼容编辑器安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md)
- [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)
- [config.toml 常用字段速查](./02-Codex-config.toml常用字段与环境变量速查.md)

查询日期 2026-11-23。扩展版本 26.51117.41037 只代表这一天 Marketplace 和 Open VSX 上查到的包。设置名以 Developer settings 页为准。
