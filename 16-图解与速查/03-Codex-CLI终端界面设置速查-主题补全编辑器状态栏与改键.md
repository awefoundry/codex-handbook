---
id: codex-cli-tui-customization
title: Codex CLI 终端界面设置速查：主题、Shell 补全、外部编辑器、通知、状态栏和改键
seo_title: Codex CLI 界面设置速查：主题、补全、Ctrl+G 编辑器、通知、状态栏与快捷键
description: Codex CLI 的终端界面可以换代码高亮主题、加 Shell 补全、用 Ctrl+G 调外部编辑器写长提示、设置通知、定制状态栏和窗口标题，还能改快捷键。本文按官方文档和 0.165.0 实测整理每项怎么设、写在 config.toml 哪里。
lede: 不想每次都在终端里凑合用 Codex？这些设置大多一条斜杠命令就能改，改完会写进 config.toml。
url: /guides/codex-cli-tui-customization
status: published
section: guides
category: K-troubleshooting
topic: 认识、安装与环境
content_type: 参考
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 入门
order: 3
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-28
date_modified: 2026-10-28
verified_on: 2026-10-28
tested_cli_version: 0.165.0
official_ref: https://learn.chatgpt.com/docs/cli-customization
keywords: [Codex CLI 主题, Codex 快捷键, Codex 补全, codex completion, tui.keymap, Codex 状态栏, Codex Ctrl+G]
howto: true
faq:
  - q: Codex CLI 怎么开 Tab 补全？
    a: 运行 codex completion 加 Shell 名生成补全脚本，支持 bash、zsh、fish、powershell、elvish，不写默认 bash。zsh 在 ~/.zshrc 里加 eval "$(codex completion zsh)"；报 command not found compdef 时，先加 autoload -Uz compinit && compinit。
  - q: 提示词很长，能用自己的编辑器写吗？
    a: 能。在输入框里按 Ctrl+G，Codex 会打开 VISUAL 环境变量指定的编辑器，没设 VISUAL 就用 EDITOR。保存并关闭后，文字回到输入框，再按回车发送。
  - q: Codex 跑完任务能提醒我吗？
    a: 能。在 config.toml 的 [tui] 下设 notifications = true。默认只在终端窗口没有焦点时提醒，想一直提醒就设 notification_condition = "always"。
  - q: 怎么改快捷键？
    a: 在会话里输入 /keymap 修改并保存，或者直接在 config.toml 里写 [tui.keymap.<场景>]，例如 [tui.keymap.global] open_transcript = "ctrl-t"。某个动作设成空数组 [] 就是取消绑定。
  - q: 想保留终端的滚动历史，不让 Codex 占满全屏怎么办？
    a: 在 [tui] 下设 alternate_screen = "never"。默认 auto，在 Zellij 里会自动不用全屏备用屏幕。
---

# Codex CLI 终端界面设置速查：主题、Shell 补全、外部编辑器、通知、状态栏和改键

> 本文在线版：[codexguide.io/guides/codex-cli-tui-customization](https://codexguide.io/guides/codex-cli-tui-customization)

> 核对依据：OpenAI 官方文档 [CLI customization](https://learn.chatgpt.com/docs/cli-customization)、[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)、[Advanced Configuration 的 TUI options](https://learn.chatgpt.com/docs/config-file/config-advanced) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 的 `tui.*` 字段。Shell 补全在 Linux 上用 `codex-cli 0.165.0` 实测；斜杠命令说明、默认快捷键和状态栏项目名对照了 [openai/codex](https://github.com/openai/codex) 仓库 `rust-v0.165.0` 版本的源码。测试机上的 Codex 没有登录，所以本文没有界面截图。核对日期 2026-10-28（北京时间）。

## 先看总表

| 想改什么 | 会话里怎么改 | 写在 config.toml 哪里 |
|---|---|---|
| 代码高亮主题 | `/theme` | `tui.theme` |
| Shell 补全 | 运行 `codex completion <shell>` | 写进 Shell 配置文件，不在 config.toml |
| 长提示用外部编辑器 | 输入框里按 `Ctrl+G` | 环境变量 `VISUAL` / `EDITOR` |
| 任务完成提醒 | — | `tui.notifications` 等 |
| 底部状态栏 | `/statusline` | `tui.status_line` |
| 终端窗口标题 | `/title` | `tui.terminal_title` |
| 快捷键 | `/keymap` | `tui.keymap.<场景>.<动作>` |
| Vim 模式 | `/vim` | `tui.vim_mode_default` |
| 方便复制的原始滚动输出 | `/raw` 或 `Alt+R` | `tui.raw_output_mode` |
| 是否占满全屏 | — | `tui.alternate_screen` |

斜杠命令改的设置会保存进 `$CODEX_HOME/config.toml`（默认 `~/.codex/config.toml`）。字段和值的写法，见 [config.toml 常用字段速查](./02-Codex-config.toml常用字段与环境变量速查.md)。

## 主题

- 会话里输入 `/theme`，打开主题选择器，可以预览，选中后保存到 `tui.theme`。
- 也可以直接写：

```toml
[tui]
theme = "dracula"   # 主题名用 kebab-case
```

- 想用自己的主题：把 `.tmTheme` 文件放进 `$CODEX_HOME/themes`（默认 `~/.codex/themes`），再在 `/theme` 里选。

主题只影响代码块和 diff 的语法高亮，不改终端本身的配色。

## Shell 补全

`codex completion` 生成补全脚本。0.165.0 的帮助信息：

```text
Usage: codex completion [OPTIONS] [SHELL]

Arguments:
  [SHELL]
          Shell to generate completions for

          [default: bash]
          [possible values: bash, elvish, fish, powershell, zsh]
```

按你用的 Shell 加到配置文件里：

```bash
# zsh：加到 ~/.zshrc
eval "$(codex completion zsh)"

# 如果 zsh 报 command not found: compdef，改成：
autoload -Uz compinit && compinit
eval "$(codex completion zsh)"

# bash：加到 ~/.bashrc
eval "$(codex completion bash)"

# fish：生成到补全目录
codex completion fish > ~/.config/fish/completions/codex.fish
```

重开终端，输入 `codex ` 后按 `Tab` 验证。在 bash 里实测，加载补全后输入 `codex com` 按 Tab 会补成 `completion`；输入 `codex completion ` 再按 Tab，会列出：

```text
-c -h --config --enable --disable --help bash elvish fish powershell zsh
```

Codex 升级后子命令可能变化，补全脚本用 `eval` 方式每次启动重新生成就不用手动更新；用文件方式的，升级后重新生成一次。

## 外部编辑器（Ctrl+G）

写长提示时，在输入框里按 `Ctrl+G`：

1. Codex 打开 `VISUAL` 环境变量指定的编辑器；没设 `VISUAL` 就用 `EDITOR`。
2. 在编辑器里写完，保存并关闭。
3. 文字回到 Codex 的输入框，确认后按回车发送。

先在 Shell 配置里设好编辑器，例如：

```bash
export VISUAL="code --wait"   # VS Code，需要 --wait 才会等你关闭窗口
# 或
export EDITOR="vim"
```

`Ctrl+G` 对应的快捷键动作是 `tui.keymap.global.open_external_editor`，可以改成别的组合。

## 通知

Codex 等你审批或者一轮任务结束时，可以发终端通知：

```toml
[tui]
notifications = true              # 或只选部分类型，见下
notification_method = "auto"      # auto（默认）、osc9、bel
notification_condition = "unfocused"  # unfocused（默认）、always
```

- `notification_method`：`auto` 会在终端支持时用 OSC 9（很多终端会把它显示成桌面通知），否则退回 BEL 响铃。
- `notification_condition`：默认只在终端窗口没焦点时提醒。
- `notifications` 也可以写成数组，只提醒部分事件。0.165.0 源码里的事件类型名有 `agent-turn-complete`（一轮完成）、`approval-requested`（等你审批）、`plan-mode-prompt`、`async-question`。

想在通知时运行自己的脚本（例如发到手机），用顶层的 `notify` 字段，见官方 [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 的 Notifications 一节。

## 状态栏和窗口标题

- `/statusline`：选择底部状态栏显示哪些项目、按什么顺序。
- `/title`：选择终端窗口或标签页标题显示什么。

写进配置是项目名数组，`null` 表示关闭：

```toml
[tui]
status_line = ["model-with-reasoning", "current-dir", "git-branch", "context-remaining", "five-hour-limit"]
terminal_title = ["spinner", "project"]   # 这是默认值
```

0.165.0 源码里的默认状态栏是 `model-with-reasoning`、`current-dir`、`thread-name`。常用项目名：

| 项目名 | 显示什么 |
|---|---|
| `model`、`model-with-reasoning`、`reasoning` | 模型名、模型加推理强度、推理强度 |
| `current-dir`、`project-name` | 当前目录、项目名 |
| `git-branch`、`pull-request-number`、`branch-changes` | Git 分支、PR 号、分支改动 |
| `run-state` | Ready、Working、Thinking 等运行状态 |
| `permissions`、`approval-mode` | 当前权限 / 沙箱、审批模式 |
| `context-remaining`、`context-used`、`context-window-size` | 上下文剩余、已用、总大小 |
| `five-hour-limit`、`weekly-limit` | 5 小时和每周额度剩余 |
| `used-tokens`、`total-input-tokens`、`total-output-tokens` | 本次会话 token 用量 |
| `fast-mode`、`raw-output` | 是否开了 Fast 模式、原始输出模式 |
| `thread-name`、`thread-id` | 会话名、会话 ID |
| `codex-version`、`hostname` | Codex 版本、主机名 |

项目名以 `/statusline` 里列出的为准，不同版本可能增减。额度相关的项目怎么理解，见 [Codex 用量额度怎么看](../10-配置模型与权限安全/10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

## 改快捷键

两种方式：

- 会话里输入 `/keymap`，查看、修改并保存。
- 直接写 config.toml：

```toml
[tui.keymap.global]
open_transcript = "ctrl-t"
toggle_raw_output = []           # 空数组 = 取消绑定

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]     # 可以绑多个

[tui.keymap.chat]
interrupt_turn = "f12"
```

规则：

- 场景（context）有 `global`、`chat`、`composer`、`editor`、`vim_normal`、`vim_operator`、`vim_text_object`、`pager`、`list`、`approval`。
- 按键名用小写加连字符，例如 `ctrl-a`、`shift-enter`、`page-down`、`minus`。
- 输入框（composer）的部分动作在没单独设置时会沿用 `global` 里的绑定；两边都设了，以具体场景为准。
- 改完在你自己的终端里试一下，有些组合会被终端或系统先拦截。
- 动作名写错时，用 `codex --strict-config` 启动会直接报错。0.165.0 实测：

```text
Error loading config.toml: unknown configuration field `tui.keymap.global.not_an_action` in -c/--config override
```

本文的 TOML 片段（主题、通知、状态栏、改键和下面的界面开关）都在 0.165.0 上用 `codex exec --strict-config` 检查过，没有未知字段。

0.165.0 源码里几个常用动作的默认按键：

| 动作 | 场景 | 默认按键 |
|---|---|---|
| `open_transcript`（打开完整记录） | global | `Ctrl+T` |
| `open_external_editor`（外部编辑器） | global | `Ctrl+G` |
| `copy`（复制最近一条回复） | global | `Ctrl+O` |
| `clear_terminal`（清屏） | global | `Ctrl+L` |
| `toggle_raw_output`（原始输出模式） | global | `Alt+R` |
| `interrupt_turn`（中断当前任务） | chat | `Esc` |
| `increase_reasoning_effort` / `decrease_reasoning_effort` | chat | `Alt+.` 或 `Shift+↑` / `Alt+,` 或 `Shift+↓` |
| `submit`（发送） | composer | `Enter` |
| `queue`（排队下一条） | composer | `Tab` |
| `history_search_previous`（搜历史） | composer | `Ctrl+R` |

斜杠命令和更多日常快捷键，见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

## 其他界面开关

都写在 `[tui]` 下：

| 字段 | 默认 | 作用 |
|---|---|---|
| `alternate_screen` | `auto` | `never` 不占满全屏、保留终端滚动历史；`auto` 在 Zellij 里自动不用 |
| `animations` | `true` | 欢迎页、闪烁效果和转圈动画 |
| `vim_mode_default` | `false` | 输入框默认进入 Vim 普通模式；会话里用 `/vim` 切换 |
| `raw_output_mode` | `false` | 启动就进入原始滚动输出，方便鼠标选中复制 |
| `show_tooltips` | `true` | 欢迎页的新手提示 |
| `auto_recap` | `true` | 终端没焦点时自动生成对话回顾；关掉后仍可手动 `/recap` |
| `disable_paste_burst` | `false` | 关闭「快速粘贴」检测 |
| `resume_cwd` | 不设 | 恢复会话时用当前目录（`current`）还是会话原来的目录（`session`）；不设则每次询问 |

顶层还有两个相关字段：`hide_agent_reasoning`（隐藏推理过程）、`file_opener`（点击引用时用哪个编辑器打开）。

## 常见问题

**`/theme` 选了主题但颜色没变化？**

主题只作用于代码块和 diff 的语法高亮。普通文字的颜色跟终端配色走。

**改了 `tui.keymap` 之后某个键不起作用？**

先在 `/keymap` 里确认绑定已保存；再换一个组合试，很可能是终端或系统先拦截了。

**这些设置对桌面端和 IDE 扩展有效吗？**

`[tui]` 下的设置只作用于 Codex CLI 的终端界面。

## 参考资料

- [CLI customization](https://learn.chatgpt.com/docs/cli-customization)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [openai/codex rust-v0.165.0](https://github.com/openai/codex/releases/tag/rust-v0.165.0)
