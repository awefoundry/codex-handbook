---
id: codex-cli-tui-customization
title: Codex CLI 终端界面设置速查：补上折叠轮次细节、tmux 里的图片预览和 osc777 通知
seo_title: Codex CLI 界面设置速查：主题、补全、Ctrl+G 编辑器、通知、状态栏与快捷键
description: Codex CLI 的终端界面可以换主题、加 Shell 补全、用 Ctrl+G 写长提示、改状态栏和快捷键。2026-11 补上 0.169.0 的折叠轮次细节、0.168.0 的 osc777 通知、tmux 图片预览，以及 features.tui_workspace 并排侧边对话。osc777 目前和配置参考页不一致。
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
date_modified: 2026-11-16
verified_on: 2026-11-16
tested_cli_version: 0.169.0
official_ref: https://learn.chatgpt.com/docs/cli-customization
keywords: [Codex CLI 主题, Codex 快捷键, Codex 补全, codex completion, tui.keymap, Codex 状态栏, Codex Ctrl+G, tui.collapse_turn_details, osc777, tui_workspace]
related: [codex-notifications-notify, codex-cli-commands-cheatsheet, codex-cli-0-167-agent-command-center]
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

# Codex CLI 终端界面设置速查：补上折叠轮次细节、tmux 里的图片预览和 osc777 通知

> 本文在线版：[codexguide.io/guides/codex-cli-tui-customization](https://codexguide.io/guides/codex-cli-tui-customization)

> 核对依据：OpenAI 官方文档 [CLI customization](https://learn.chatgpt.com/docs/cli-customization)、[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)、[Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)（2026-11-16 抓取），以及 [rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)、[rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0) 的 Release。Shell 补全、keymap 未知字段报错和状态栏项目名仍是 2026-10-28 用 `codex-cli 0.165.0` 核对的记录，这次没有重跑。2026-11-16 用 `codex-cli 0.169.0` 核对了 `tui.notification_method`、`tui.collapse_turn_details` 和 `features.tui_workspace` 能否被配置加载接受。没有登录，没有全屏界面，没有 Ghostty、Kitty 或 tmux，所以没有截图。

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
| 折叠已完成轮次的细节 | 全屏 transcript 里的 **Collapse turn details** | `tui.collapse_turn_details` |
| 并排侧边对话 | — | `features.tui_workspace` |
| tmux 里的图片预览和宠物 | 终端侧设置，不在 config.toml | Ghostty、Kitty 的 tmux：`allow-passthrough all` |
| 通知方式，含 osc777 | — | `tui.notification_method`，取舍见 [任务完成通知](../11-自动化与高级工作流/15-Codex任务完成通知-tui.notifications与notify脚本.md) |

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

Codex 等你审批或者一轮任务结束时，可以发终端通知。开关、事件类型、`notify` 脚本和项目级配置为什么会被忽略，都写在 [任务完成通知](../11-自动化与高级工作流/15-Codex任务完成通知-tui.notifications与notify脚本.md)。这里只留一行配置，以及和官方文档对不上的那一项：

```toml
[tui]
notifications = true
notification_method = "auto" # 配置参考页：auto、osc9、bel。0.169.0 还接受 osc777
notification_condition = "unfocused"
```

2026-11-16 的 Configuration Reference 把 `tui.notification_method` 写成 `auto | osc9 | bel`，没有 `osc777`。rust-v0.168.0 的 Release 已经写了 `tui.notification_method = "osc777"`。同一天用 0.169.0 把非法值 `not-a-method` 放进配置，报错列出的期望值是 `auto`、`osc9`、`osc777`、`bel`。`osc777` 能被这次的 CLI 接受，配置参考页还没有把它列进去。审批通知的预览变长，也放在通知专文里，不在这里展开。

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

项目名以 `/statusline` 里列出的为准，不同版本可能增减。额度相关的项目怎么理解，见 [Codex 用量额度怎么看](../10-配置模型与权限安全/08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

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

主题、状态栏、改键和下面原有界面开关的 TOML，是 0.165.0 上用 `codex exec --strict-config` 检查过的。2026-11-16 没有把这些旧片段在 0.169.0 上重跑。新键的检查见下一节。

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

## 0.168 和 0.169 补上的界面

下面四项来自 Release 和 rust-v0.169.0 的配置 schema。没有登录，没有打开全屏 transcript，也没有 tmux，所以只核对了配置能不能被 0.169.0 接受，没有界面截图。

### 折叠轮次细节

rust-v0.169.0 Release 的原文是：在全屏 transcript 里打开 **Collapse turn details**，把每个提示下面已经完成的活动折起来，答案仍看得见，工具输出仍可搜索。

配置键在该标签的 `config.schema.json` 里是 `tui.collapse_turn_details`，布尔值，默认 `false`。schema 的说明是：在全屏 transcript 里概括工具调用，并折叠已完成的轮次。配置面板上的标签就是 `Collapse turn details`，旁边的短说明是 `Summarize tool calls in the conversation`。2026-11-16 的 Configuration Reference 正文里没有这个键。写进 `config.toml` 的名字以 schema 里的 `tui.collapse_turn_details` 为准。

```toml
[tui]
collapse_turn_details = true
```

0.169.0 上，独立 `CODEX_HOME` 里只写这一项，再执行 `codex exec --strict-config`。进程进入会话后因未登录在 API 返回 401，没有报未知字段。这只说明加载配置时接受了这个键，不说明折叠后的画面。

### osc777

见上一节，细节和排错在 [任务完成通知](../11-自动化与高级工作流/15-Codex任务完成通知-tui.notifications与notify脚本.md)。

### 并排侧边对话

rust-v0.168.0 Release：打开 `features.tui_workspace`，在主对话旁边看一条侧边对话。拖动分隔线改变两栏宽度，或按 `leader z` 放大当前这一栏。rust-v0.169.0 Release 接着写：这个可选的终端工作区支持多个侧边对话标签，可以用键盘或鼠标切换，重启 Codex 之后还能重新打开保存过的本地侧边对话。

0.169.0 源码里，`toggle_pane_zoom` 登记为 leader 和弦 `z`，并且它属于侧栏动作。`features.tui_workspace` 没开时，侧栏动作不会登记，所以这条 `z` 也不会登记。2026-11-16 的 Configuration Reference 没有列出 `features.tui_workspace`。schema 里它是布尔值。

```toml
[features]
tui_workspace = true
```

0.169.0 接受这个键，并在 `codex exec` 里警告：`Under-development features enabled: tui_workspace`。未登录，随后 401。没有看到并排的两栏，也没有按过 `leader z`。leader 键本身是哪一个组合，以你会话里的 `/keymap` 为准；本文不另写一个没有在 0.169.0 帮助里打印出来的默认 leader。

### tmux 里的图片预览和宠物

rust-v0.168.0 Release：在 Ghostty 和 Kitty 里，tmux 设了 `allow-passthrough all` 时，全屏 Codex 会显示图片预览和宠物。这是 tmux 的选项，不是 `config.toml` 的键。本文没有这两款终端，也没有 tmux，没有截图。0.167.0 的本机图片预览和 `codex agents` 见 [命令中心一文](../12-官方工具与集成/22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)。宠物怎么做见 [创建自定义桌宠](../12-官方工具与集成/05-Codex创建自定义桌宠.md)。

子命令本身见 [CLI 命令速查](./01-Codex-CLI命令速查-子命令与启动参数.md)。

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
- [openai/codex rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)
- [openai/codex rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
