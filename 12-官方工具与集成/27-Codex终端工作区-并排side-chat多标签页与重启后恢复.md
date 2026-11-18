---
id: codex-terminal-workspace-side-chat
title: Codex 终端工作区：并排 side chat、多标签页，重启之后还能打开
seo_title: Codex 终端工作区：并排 side chat、多标签页与重启后恢复
description: 从 Codex CLI 0.168 起，打开终端工作区可以在主对话旁边开 side chat；0.169 又加上多标签页，并能在重启后打开已保存的本地 side chat。本文按官方 Release 说明怎么启用、怎么切换和缩放窗格，以及和主会话、命令中心的分工。
lede: 工作区是可选的。先打开 features.tui_workspace，再在 0.169 里使用多个本地 side-chat 标签。本文没有拍到 TUI。
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
date_modified: 2026-11-14
verified_on: 2026-11-14
tested_cli_version: 0.169.0
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.169.0
keywords: [Codex 终端工作区, tui_workspace, side chat, 侧边对话标签页, leader z, Collapse turn details]
related: [codex-cli-0-169-side-chat-cloud-connection, codex-cli-0-167-agent-command-center, cli-manage-multiple-sessions]
howto: true
faq:
  - q: 不升级到 0.169，只有 0.168 能用工作区吗？
    a: 0.168 的 Release 已经有 features.tui_workspace、分隔条和 leader z。多个 side-chat 标签页，以及重启后打开已保存的本地 side chat，写在 0.169 的 Release 里。
  - q: 打开工作区的配置键是什么？
    a: Release 写的是 features.tui_workspace。0.169.0 上它位于 codex features list，阶段是 under development，未写入配置时有效状态是 false。可以用 codex --enable tui_workspace，或在 config.toml 的 [features] 里设为 true。
  - q: leader z 的 leader 是哪一个键？
    a: 0.168 的 Release 只写了按 leader z 放大当前获得焦点的窗格，没有写出 leader 键的默认按键。本文不补充 Release 里没有的键位。
  - q: 重启后所有侧边对话都会回来吗？
    a: Release 写的是重新打开已保存的本地 side chat。它没有写未保存的临时窗格、Cloud 会话或另一台机器上的会话会自动出现。
---

# Codex 终端工作区：并排 side chat、多标签页，重启之后还能打开

> 本文在线版：[codexguide.io/guides/codex-terminal-workspace-side-chat](https://codexguide.io/guides/codex-terminal-workspace-side-chat)

> 核对依据：GitHub Release [rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0) 与 [rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)，以及 ChatGPT Learn [更新日志](https://learn.chatgpt.com/docs/changelog) 2026-11-13 的对应条目。2026-11-14 在 Linux 上的 `codex-cli 0.169.0` 核对了 `features.tui_workspace` 的默认状态，并用 `-c features.tui_workspace=true` 确认这一版接受该键。没有登录，没有进入交互式 TUI，没有看到并排窗格、标签或全屏转录，因此没有配图。界面名称以 Release 的英文为准。版本之间还多了哪些命令，见 [Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。

这篇给已经会在终端里跑 Codex、想把一条主对话和旁边的侧边对话放在同一个工作区里的人。0.167 的命令中心见 [Codex CLI 0.167.0](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)。`resume`、`fork` 和 `/side` 见 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。

## 先看结论

普通的一次 `codex` 是一块会话区域。终端工作区是另一层可选布局：主对话还在，旁边可以有 side conversation。

两版 Release 的分工：

- 0.168：打开 `features.tui_workspace` 后，在主对话旁边查看 side conversation。拖动分隔条改变两块窗格的宽度，或按 `leader z` 放大当前获得焦点的窗格。
- 0.169：这个可选工作区支持多个 side-chat 标签页，用键盘或鼠标切换；重启 Codex 之后，可以重新打开已保存的本地 side chat。全屏转录里可以打开 **Collapse turn details**。

工作区默认关着。它不代替 `codex resume`，也不代替命令中心。下面只使用 Release 和 0.169.0 帮助里出现过的名称。

## 怎么打开

先确认版本：

```bash
codex --version
```

多个标签页和重启后恢复写在 0.169。本文核对时的正式版输出是 `codex-cli 0.169.0`。只要 0.168 的并排窗格、还没有标签页时，不要按 0.169 的恢复行为来期待。

0.169.0 的 `codex features list` 把 `tui_workspace` 标为 under development，未写入配置时有效状态是 false。`codex exec --help` 写明 `--enable` 等价于 `-c features.<name>=true`。只想这一次打开：

```bash
codex --enable tui_workspace
```

准备以后都用工作区时，写在用户级 `~/.codex/config.toml`（Windows 上是用户目录下的 `.codex/config.toml`）：

```toml
[features]
tui_workspace = true
```

2026-11-14 用独立的 `CODEX_HOME` 执行 `codex exec --strict-config -c features.tui_workspace=true`，进程接受了这个键，并警告 `Under-development features enabled: tui_workspace`，随后因为没有登录而无法完成模型请求。警告说明开关仍被标成未完成，行为可能变化。这次没有画出 TUI。

发布说明没有给出新建 side chat 的按键或斜杠命令。打开工作区之后，以你屏幕上实际出现的控件为准。对不上 Release 里的 side conversation、分隔条或标签时，先核对 `codex --version`，再对照 Release 原文。

## 主对话和 side chat 分别放什么

Release 只说明了布局：side conversation 在主对话旁边，0.169 还可以有多个本地标签。它没有规定哪些话必须放在侧面。

下面是用法上的划分，不是官方规则。主对话保留你要落地的任务：改哪些文件、怎样验收、做到哪一步。侧面用来问一条不会改写主线结论的问题，例如某个函数的调用方、一条报错的含义，或要不要把范围再缩小。问完把仍然有效的结论用一句话写回主对话，侧面标签就可以关掉。

不要把侧面当成第二个会自动改仓库的隐藏会话来用，除非你在那一块窗格里也看清了它的权限和它正在碰的目录。Release 没有写 side chat 使用另一份沙箱。0.169 的提交说明里有 “Ensure side-chat policy reaches the first model request”，那只说明策略需要传到第一次模型请求，没有公开另一套权限名称。本文没有打开窗格，没有比较两块窗格的审批提示。

[管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md) 里的 `/side`（别名 `/btw`）是会话内的短暂分叉，官方说明是不把这段旁支写进主线转录。0.168 的 side conversation 是工作区里的并排窗格。两份 Release 都没有写它们是不是同一个功能。本文保持两个名字，不把 `/side` 说成打开标签页的命令。

## 切换、拖动分隔条与 leader z

0.168 Release 写了两件事：

- 拖动分隔条，改变窗格宽度。
- 按 `leader z`，放大当前获得焦点的窗格。

0.169 Release 补的是标签之间的移动：用键盘或鼠标在多个 side-chat 标签之间切换。它没有列出方向键、数字键或鼠标单击的具体组合，所以这里不补充。

`leader z` 里的 leader 也没有在 Release 里展开成某一个默认按键。在自己的终端里对不上时，不要改用网上另一套前缀。工作区跟做以你这一版界面上看得到的分隔条和标签为准。本文没有拖过分隔条，也没有按过 `leader z`。

放大的是「当前获得焦点的窗格」。Release 没有写放大之后怎样恢复并排。操作前先确认焦点在你想放大的那一块，避免把主对话放成全屏后找不到侧面。

## 重启后如何打开已保存的本地 side chat

0.169 的原句是：reopen saved local side chats after restarting Codex。拆开是三个条件：已经保存、属于本地 side chat、Codex 重新启动之后可以再打开。

本文能核对的边界只有这句原文：

- 它写的是本地 side chat，不是发布说明同一节里的 Cloud 会话。Cloud 连接是 0.169 的另一条 opt-in 能力，见 [0.169.0 一文](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。
- 它写的是已保存的对话。没有在退出前保存的窗格，不要默认它还会在。
- 它没有写保存文件的路径、数量上限，或卸载 CLI 之后标签是否还在。

重启后如果工作区是空的，先看 `codex --version` 是不是 0.169 或更新的正式版，以及 `features.tui_workspace` 是否仍为 true。主会话本身的恢复用 `codex resume`，不依赖工作区开关。命令中心里按名称、提示预览或工作目录搜索旧任务，是 0.169 的另一项能力，同样没有在本文里打开。

## 和命令中心、resume、fork 的关系

三件事管的不是同一层：

| 你要做的事 | 用什么 | 依据 |
| --- | --- | --- |
| 在当前终端里，主对话旁边看另一段对话 | 打开 `features.tui_workspace` | 0.168 Release |
| 同一工作区里保留多个本地侧面标签，重启后再打开 | 0.169 的 side-chat 标签 | 0.169 Release |
| 离开很久，按目录或名字回到主会话 | `codex resume`、`/resume` | [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md) |
| 从某条会话复制出一条新的聊天记录 | `/fork`、`codex fork` | 同上；fork 不自动隔离磁盘上的文件 |
| 在多条会话之间浏览、切换，并搜索更早的任务 | `codex agents`；搜索是 0.169 的发布说明 | [0.167 命令中心](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)、[0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md) |

0.169.0 的 `codex agents --help` 仍把子命令说明为打开命令中心以浏览和切换会话。帮助文本没有出现 side chat 或 tui_workspace。工作区是当前 TUI 的布局；命令中心是另一条浏览会话的入口。

## Collapse turn details 什么时候有用

0.169 把 **Collapse turn details** 放在全屏转录里：把已经完成的活动折到每条提示下面，回答保持可见，工具输出仍然可以搜索。

适合转录已经很长、你要先看到每轮回答、必要时再展开工具输出的时候。Release 没有把它写成工作区专属，也没有给出快捷键或菜单的上一级。本文没有打开全屏转录。中文界面若没有这句英文，不要猜测另一个翻译；以 Release 里的英文名称为准去对屏幕上的文字。

折叠只影响转录怎么显示。它不删除工具输出，Release 写明工具输出仍可搜索。本文没有输入搜索词去验证。

## 常见问题

### 找不到开关

`codex features list` 里看 `tui_workspace` 这一行。0.169.0 上未配置时是 false，阶段是 under development。配置写在用户级 `config.toml` 的 `[features]` 表，或用 `--enable tui_workspace`。写到项目里的 `.codex/config.toml` 之前，先确认这一版是否接受项目级的 features；本文没有把这个键放进项目配置做试验。改完要重新启动这次 `codex`，正在运行的界面不会因为你在另一个编辑器里保存了文件就自动打开工作区。本文没有验证热加载。

### 标签丢了

先分清丢的是哪一种。Release 只承诺可以重新打开已保存的本地 side chat。临时开的、没有保存的、或属于 Cloud 连接的会话，不在这句之内。主会话还在时，用 `codex resume` 或命令中心找它，而不是只在侧边标签栏里翻。

### 只有本地 side chat

0.169 的恢复句写的是 local side chats。同一版 Release 里的 Cloud 连接可以归档或恢复 Cloud 会话，但那是 macOS 和 Linux 上的另一项 opt-in，Release 没有把它并进 `features.tui_workspace`。本文没有打开 Cloud 连接，没有看到 Cloud 会话出现在侧边标签里。

### 打开之后行为不稳定

0.169.0 在启用这个开关时会警告功能仍在开发中，可能不可预测。遇到窗格打不开、标签无法切换时，先记下 `codex --version` 的原文，再对照 [0.169.0 的发布说明](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。不要为了绕过警告去关 `suppress_unstable_features_warning`，除非你已经知道自己在抑制什么；那条警告文本只说明可以这样关掉提示，不代表功能已经稳定。

## 参考资料

- [GitHub Release rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)
- [GitHub Release rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
- [ChatGPT 与 Codex 更新日志](https://learn.chatgpt.com/docs/changelog)
- 同库：[Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)、[Codex CLI 0.167.0](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)、[管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)

官方资料核对日期：2026-11-14（Asia/Shanghai）。依据是 Release 说明和 0.169.0 的配置键检查，没有拍到终端工作区界面。
