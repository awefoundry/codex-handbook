---
id: codex-terminal-workspace-side-chat
title: Codex 终端工作区：0.171 起默认开启，侧栏能预览文档和图片、打开子代理记录，并排 side chat 与多标签页照常用
seo_title: Codex 终端工作区：默认开启、文档与图片预览、子代理记录
description: Codex CLI 0.171.0 起终端工作区默认开启：主对话旁可以搜索预览文档、预览图片、打开子代理记录，并排 side chat、多标签页和重启后恢复照常可用。本文按 0.171.0 发布说明和官方命令文档更新开启与关闭方式、侧栏用法和常见问题。
lede: 0.171.0 起工作区默认开着。不想用就把它设成 false。侧栏新增的是可搜索的文档预览、图片预览和子代理记录；本文没有进入 TUI。
url: /guides/codex-terminal-workspace-side-chat
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 27
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-14
date_modified: 2026-11-20
verified_on: 2026-11-20
tested_cli_version: 0.171.0
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.171.0
keywords: [Codex 终端工作区, tui_workspace, Codex 文档预览, Codex 子代理记录, side chat]
related: [codex-cli-0-171-sol-default-workspace-exec-remote, codex-cli-0-169-side-chat-cloud-connection, codex-subagents-parallel-work, cli-manage-multiple-sessions]
howto: true
faq:
  - q: 0.171 还要先打开 features.tui_workspace 吗？
    a: 不用。2026-11-20 在空配置的 codex-cli 0.171.0 上，codex features list 里 tui_workspace 是 stable，有效状态是 true。0.169.0 那时它是 under development，未写入配置时是 false。
  - q: 不想用工作区，怎么关？
    a: 只关这一次，用 codex --disable tui_workspace。0.171.0 的 --help 写明 --disable 等价于 -c features.<name>=false。要写进配置，用 codex features disable tui_workspace，或在 config.toml 的 [features] 里设 tui_workspace = false。本文用 disable 子命令写过，随后 features list 变为 false。
  - q: 侧栏里的文档、图片和子代理记录有快捷键吗？
    a: 0.171.0 的 Release 只写了这三类内容在主对话旁边，没有写出按键或菜单名。本文没有进入 TUI，不补充界面细节。
  - q: 以前手动把 tui_workspace 设成 true，升级后会怎样？
    a: 空配置下默认已经是开。那一行 true 和默认一致，不会变成关。要关，必须写成 false。本文没有热加载配置，改完要重新启动这次 codex。
---

# Codex 终端工作区：0.171 起默认开启，侧栏能预览文档和图片、打开子代理记录，并排 side chat 与多标签页照常用

> 本文在线版：[codexguide.io/guides/codex-terminal-workspace-side-chat](https://codexguide.io/guides/codex-terminal-workspace-side-chat)

> 核对依据：GitHub Release [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)、[rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)、[rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)，以及 2026-11-20 打开的 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)。2026-11-20 在 Linux 的 `codex-cli 0.171.0` 上，空 `CODEX_HOME` 的 `codex features list` 里 `tui_workspace` 为 stable / true；`codex features disable tui_workspace` 之后变为 stable / false，并在 `config.toml` 写下 `[features] tui_workspace = false`。没有登录，没有进入交互式 TUI，没有看到侧栏、标签或全屏转录，因此没有新配图。这一版发布说明和该不该升，见 [Codex CLI 0.171.0](./30-Codex-CLI-0.171-默认GPT-6.2-Sol-终端工作区默认开启与exec-remote.md)。

这篇给已经会在终端里跑 Codex、想知道工作区现在是开还是关、侧栏里多了什么的人。子代理本身怎么派，见 [Subagents](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)。`resume` 和 `fork` 见 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。

## 先说结论

0.171.0 起，终端工作区默认开启。Release 的原文是：

> Enabled the TUI workspace by default, with searchable document previews, image previews, and subagent transcripts alongside the main conversation. (#61352, #61888, #61889, #61919, #62157)

不想用，就把它关掉。0.171.0 的 `codex --help` 写明 `--disable <FEATURE>` 等价于 `-c features.<name>=false`。只影响这一次启动：

```bash
codex --disable tui_workspace
```

要以后都关，Developer commands 写 `codex features` 的 `enable` 和 `disable` 会把改动写入配置，对以后的会话生效。2026-11-20 在独立 `CODEX_HOME` 里执行：

```bash
codex features disable tui_workspace
```

输出是 `Disabled feature tui_workspace in config.toml.` 随后 `codex features list` 里这一行是 `stable`、有效状态 `false`。写出来的配置是：

```toml
[features]
tui_workspace = false
```

同一天用 `codex exec --strict-config -c features.tui_workspace=false` 启动时，进程接受了这个键，没有报未知字段。未登录，模型请求随后 401。这只说明关闭的写法能被这一版加载。

0.168 和 0.169 的布局能力还在，只是不再默认关闭：

- 0.168：主对话旁边可以有 side conversation。拖动分隔条改变两块窗格的宽度，或按 `leader z` 放大当前获得焦点的窗格。
- 0.169：多个 side-chat 标签页，用键盘或鼠标切换；重启之后可以重新打开已保存的本地 side chat。全屏转录里可以打开 **Collapse turn details**。

工作区不代替 `codex resume`，也不代替命令中心。下面凡是界面名称，仍以对应 Release 的英文为准。本文没有进入 TUI。

## 侧栏新增：文档预览、图片预览、子代理记录

0.171.0 的发布说明把三件事放在主对话旁边：可搜索的文档预览、图片预览、子代理记录。对应的提交标题是：

- #61352：把 TUI 工作区标为 stable，并默认开启
- #61888：只读的文档预览
- #61889：文档预览里的搜索、选择和链接导航
- #61919：侧栏图片预览，并在回答之后展示生成的图片
- #62157：在 TUI 侧栏打开子代理记录

这些标题来自该 Release 的提交列表，不是一份界面说明书。Release 顶部那句已经是用户能核对的全部：主对话旁边可以搜索预览文档、预览图片、查看子代理记录。它没有写快捷键、侧栏宽度或菜单的中文名。

子代理和主会话怎么分工，见 [Subagents](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)。那篇讲的是派发和沙箱继承，不是 0.171 的侧栏。本文没有打开过一份子代理记录。

## 并排 side chat 与 /side

0.168 的 Release 说明了布局：side conversation 在主对话旁边。0.169 补了多个本地标签。两版 Release 都没有把 `/side` 写成打开标签页的命令。

2026-11-20 的 Developer commands 把两者接上了，原文是：side chat 默认是临时的；在本地全屏会话里，如果 `features.tui_workspace` 已开启并且有已保存的历史，`/side` 会重新打开已有的 side chat，`/side` 后面带上文字会新开一条。重启 Codex 之后，可以从侧栏重新打开已保存的 side chat。`/side` 在另一条 side chat 里面不可用，review 模式里也不可用。

`/side` 后面可以直接接一句要问的话。Developer commands 的例句是 `/side Check whether this plan has an obvious risk`，带文字的用法以这句为准。

`/side` 的别名仍是 `/btw`。官方对这条命令的用途说明没有变：在主对话继续的时候，另开一段转录分开的侧边对话；侧边模式里仍能看到主对话是否还在跑。

本文没有输入 `/side`，没有比较两块窗格的审批提示。0.169 的提交说明里有 “Ensure side-chat policy reaches the first model request”，那只说明策略需要传到第一次模型请求，没有公开另一套权限名称。不要把侧面当成一份自动换了沙箱的隐藏会话。

## 多标签页、任务搜索与重启后恢复

0.169 Release 写的是：用键盘或鼠标在多个 side-chat 标签之间切换。它没有列出方向键、数字键或鼠标单击的具体组合，所以这里不补充。

`leader z` 仍只来自 0.168 的 Release：放大当前获得焦点的窗格。Release 没有写出 leader 键的默认按键，也没有写放大之后怎样恢复并排。对不上时，不要改用另一套前缀。本文没有拖过分隔条，也没有按过 `leader z`。

重启后的原句仍是 0.169 的：reopen saved local side chats after restarting Codex。2026-11-20 的 Developer commands 用侧栏复述了同一边界：可以从侧栏重新打开已保存的 side chat。拆开是三个条件：已经保存、属于本地 side chat、Codex 重新启动之后可以再打开。

- 它写的是本地 side chat，不是 Cloud 会话。Cloud 连接见 [0.169.0 一文](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。
- 它写的是已保存的对话。没有保存的临时窗格，不要默认它还会在。Developer commands 也写 side chat 默认是临时的，工作区打开并且有已保存历史时才走上面的重新打开。
- 它没有写保存文件的路径、数量上限，或卸载 CLI 之后标签是否还在。

命令中心里按名称、提示预览或工作目录搜索旧任务，是 0.169 的另一项能力，不在 `features.tui_workspace` 这一个开关里。0.171.0 的 `codex agents --help` 仍把子命令说明为打开命令中心以浏览和切换会话。帮助文本没有出现 side chat。本文没有打开命令中心。

0.169 把 **Collapse turn details** 放在全屏转录里：把已经完成的活动折到每条提示下面，回答保持可见，工具输出仍然可以搜索。0.171.0 的 Release 顶部没有再提这一项。本文没有打开全屏转录，不把「没写在 0.171 顶部」理解成已经删除。中文界面若没有这句英文，以 Release 里的英文名称为准去对屏幕上的文字。

## 和 resume、fork 的关系

| 你要做的事 | 用什么 | 依据 |
| --- | --- | --- |
| 主对话旁边的工作区 | 0.171.0 起默认开着；关掉用 `--disable tui_workspace` 或 `[features] tui_workspace = false` | 0.171.0 Release，以及当天的 `--help` |
| 在工作区里重新打开或新开 side chat | `/side`，或 `/side` 后面带上文字 | 2026-11-20 的 Developer commands |
| 多个本地侧面标签，重启后再从侧栏打开已保存的 | 0.169 的 side-chat 标签；命令文档写从侧栏重新打开 | 0.169 Release，Developer commands |
| 离开很久，按目录或名字回到主会话 | `codex resume`、`/resume` | [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md) |
| 从某条会话复制出一条新的聊天记录 | `/fork`、`codex fork` | 同上 |
| 在多条会话之间浏览并搜索更早的任务 | `codex agents` | [0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md) |

## 常见问题

### 终端太窄

0.171.0 的 Release 和当天的 `--help` 都没有写工作区的最小列数，也没有写窄终端时侧栏会不会自动收起。本文没有进入 TUI，看不到窄窗口下的布局。对不上并排时，先把终端拉宽，再核对 `codex --version` 和 `tui_workspace` 的有效状态，不要按一篇文章里没有的列数去调。

### tmux

0.168 的 Release 写过另一件和图片有关的事：在 Ghostty 和 Kitty 里，tmux 设了 `allow-passthrough all` 时，全屏 Codex 会显示图片预览和宠物。那是 tmux 的选项，不是 `config.toml` 的键。说明见 [终端界面设置](../16-图解与速查/03-Codex-CLI终端界面设置速查-主题补全编辑器状态栏与改键.md)。

0.171 的侧栏图片预览是 Release 里的另一句，没有写它是否依赖同一条 tmux 设置。本文没有 tmux，没有 Ghostty 或 Kitty，没有核对这两件事是不是同一个开关。

### 旧配置里手动开过 tui_workspace

0.169.0 上，这个开关未写入配置时是关的，阶段是 under development，启用时会警告功能仍在开发中。0.171.0 的空配置里，阶段已是 `stable`，有效状态是 `true`。这次用 `-c features.tui_workspace=false` 启动时，没有看到以前那种 `Under-development features enabled: tui_workspace`。本文没有再打开 `true` 去对比警告是否还在。

如果你的 `config.toml` 里还有 `tui_workspace = true`，它和现在的默认一致，工作区仍然开着。空目录里没有这一行时，有效状态也是开。本文没有先写成 `true` 再删掉那一行重测。要关，写成 `false`，或执行 `codex features disable tui_workspace`。

改的是文件的话，正在运行的界面不会因为你在另一个编辑器里保存了配置就马上切换。本文没有验证热加载。重新启动这次 `codex` 再看。

### 标签丢了

先分清丢的是哪一种。Release 和命令文档只承诺可以重新打开已保存的本地 side chat。临时开的、没有保存的、或属于 Cloud 连接的会话，不在这句之内。主会话还在时，用 `codex resume` 或命令中心找它。

### 只有本地 side chat

0.169 的恢复句写的是 local side chats。同一版 Release 里的 Cloud 连接是 macOS 和 Linux 上的另一项 opt-in，Release 没有把它并进 `features.tui_workspace`。本文没有打开 Cloud 连接，没有看到 Cloud 会话出现在侧边标签里。

## 参考资料

- [GitHub Release rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)
- [GitHub Release rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
- [GitHub Release rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- 同库：[Codex CLI 0.171.0](./30-Codex-CLI-0.171-默认GPT-6.2-Sol-终端工作区默认开启与exec-remote.md)、[Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)、[Subagents](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)

官方资料核对日期：2026-11-20（Asia/Shanghai）。关闭方式在 0.171.0 的帮助和 `features` 子命令上核对过。没有进入终端工作区，没有新截图。
