---
id: codex-cli-0-171-sol-default-workspace-exec-remote
title: Codex CLI 0.171.0：GPT-6.2 Sol 成为默认模型，终端工作区默认开启，codex exec 也能用 --remote 连已有 app server
seo_title: Codex CLI 0.171.0：默认 GPT-6.2 Sol、终端工作区与 exec --remote
description: Codex CLI 0.171.0 已发布。本文按 GitHub Release 说明怎么升级，GPT-6.2 Sol 成为默认模型、终端工作区默认开启、codex exec --remote、/rc 与 /remote、输入框撤销重做和 MCP 状态栏分别是什么，以及会话草稿保留、权限 profile、审批和终端显示修复对日常使用有什么影响。
lede: 打开 CLI 时的默认模型和默认界面都变了。已经在用 0.170 的人，值得升到 0.171.0 再看自己的配置有没有把工作区关掉。
url: /guides/codex-cli-0-171-sol-default-workspace-exec-remote
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 30
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-20
date_modified: 2026-11-20
verified_on: 2026-11-20
tested_cli_version: 0.171.0
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.171.0
keywords: [Codex CLI 0.171.0, GPT-6.2 Sol 默认模型, Codex 终端工作区, codex exec --remote, /remote 配对码]
related: [codex-cli-0-170-voice-mcp-reconnect, codex-gpt-6-2-astra-sol, codex-update-uninstall, codex-terminal-workspace-side-chat, codex-app-server-remote, codex-cli-slash-commands]
howto: false
faq:
  - q: 现在就要升到 0.171.0 吗？
    a: 已经在用 CLI、并且会看到默认模型或终端工作区的人，值得升。发布说明把 GPT-6.2 Sol 写成模型目录的默认选择，并把终端工作区默认打开。它没有把这一版写成必须马上安装的安全公告。
  - q: codex update 会停在 0.171.0 吗？
    a: 不会。0.171.0 的 codex update --help 写的是更新到最新版，帮助里没有指定版本号的参数。要钉住这个正式版，用 npm install -g @openai/codex@0.171.0。
  - q: 升完是不是每个人打开都是 GPT-6.2 Sol？
    a: 发布说明写的是 Sol 成为模型目录的默认选择。套餐、企业开关和你自己写过的 model 配置仍会改变实际看到的模型。谁能用、额度怎么算，见 GPT-6.2 一文，本文不重抄。
  - q: 终端工作区不想要，怎么关？
    a: 0.171.0 的 --help 里 --disable 等价于 -c features.<name>=false。空配置下 features list 里 tui_workspace 已是 stable、有效状态 true。关掉的写法见终端工作区一文。
---

# Codex CLI 0.171.0：GPT-6.2 Sol 成为默认模型，终端工作区默认开启，codex exec 也能用 --remote 连已有 app server

> 核对依据：GitHub Release [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)（发布时间 2026-11-20T00:44:47Z，北京时间 08:44）。同一天打开的 ChatGPT Learn [更新日志](https://learn.chatgpt.com/codex/changelog) 最新一条 CLI 仍是 2026-11-18 的 Codex CLI 0.170.0，页面上还没有 0.171.0，所以功能条文以 GitHub Release 为准。npm 注册表 `dist-tags.latest` 为 `0.171.0`，该版本的 `time` 为 2026-11-20T00:51:29.762Z（北京时间 08:51）。2026-11-20 在 Linux 上安装 `@openai/codex@0.171.0`，`codex --version` 输出 `codex-cli 0.171.0`。完整提交列表见 [rust-v0.170.0...rust-v0.171.0](https://github.com/openai/codex/compare/rust-v0.170.0...rust-v0.171.0)。本文只采用 Release 顶部的三类说明；列表里的内部重构不写成用户功能。本环境没有登录，没有打开交互式 TUI，没有配图。

这篇给已经在用 Codex CLI、想知道 0.171.0 该不该升的人。上一版的语音协商、同名 MCP 和 Cloud 重连见 [Codex CLI 0.170.0](./29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md)。套餐、额度和切换步骤见 [Codex 用 GPT-6.2 Astra 和 Sol](../10-配置模型与权限安全/29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。安装渠道见 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。

## 先说结论

0.171.0 改的是你打开 CLI 时的两件默认事：模型目录的默认选择，以及终端界面是不是工作区。

已经在用 0.170 这一代的人，值得升，主要因为这三件事：

- 模型目录加入 GPT-6.2 Sol 和 Astra，Sol 是默认选择。
- 终端工作区默认开启。主对话旁边可以搜索预览文档、预览图片、查看子代理记录。
- 切换或恢复会话时，草稿、排队的追问和被打断的输入会留在原来的线程上；切换工作目录时，权限 profile 不再丢掉。

另外三条知道即可，不必单独为它们升级：`codex exec --remote`、TUI 里的 `/rc` 与 `/remote`、以及实验开关打开之后的自定义 MCP 状态栏。前两条的操作放在后面的专文里，这里只说明它们从这一版开始存在。

发布说明没有把 0.171.0 写成必须马上安装的安全公告。Chores 里有一条是把源码构建和发布工具升到 Rust 1.99.1，另一条是更新 XML 依赖并移除过时的安全公告例外。这是仓库构建依赖，不是给终端用户的操作步骤。

## 怎么升到 0.171.0

更新日志和上一版文章用的固定版本命令，这一版同样适用：

```bash
npm install -g @openai/codex@0.171.0
```

装完新开一个终端，再核对：

```bash
codex --version
```

2026-11-20 在 Linux 上执行了这条 npm 命令。系统默认的 npm 全局目录没有写权限，所以装到了当前用户可写的前缀。装完后的输出是 `codex-cli 0.171.0`。同一天查询的 npm `latest` 也是 `0.171.0`。

`codex update --help` 的说明是 “Update Codex to the latest version”。帮助里出现的参数是配置覆盖、功能开关和 `--help`，没有指定版本号的参数。它按安装来源更新到最新版，不能用来钉住 0.171.0。本文读了这段帮助，没有执行 `codex update`。

Homebrew 和官方安装脚本默认也是走最新版。渠道判断、`brew upgrade --cask codex`，以及安装脚本命令，写在 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。本文今天没有跑安装脚本，也没有用 Homebrew。

要长期停在 0.171.0，用上面的 npm 版本号。以后 `latest` 再往前走时，不带版本号的安装命令会离开这一版。

## 新功能一：模型目录加入 GPT-6.2 Sol 和 Astra，Sol 是默认选择

Release 的原文是：

> Added GPT-6.2 Sol and Astra to model catalogs, with Sol as the default catalog selection. (#62106)

提交标题是 “Add GPT-6.2 Sol and Astra to model catalogs”。

这是目录里的默认选择，不是一份新的额度表。哪些套餐能用、Enterprise 和 Edu 要不要管理员先开、Fast 和 Ultrafast 怎么算，仍以 [GPT-6.2 一文](../10-配置模型与权限安全/29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md) 引用的 Models、Pricing 和 What's new 为准。本文不重抄那些表。

2026-11-20 能在这台未登录的 Linux 上核对的，是启动摘要里的模型名。独立空 `CODEX_HOME` 下执行 `codex exec --strict-config -c features.tui_workspace=false --skip-git-repo-check`，进程在请求模型之前打印了 `model: gpt-6.2-sol`。随后请求因缺少认证，以 401 结束，没有模型回复。这只说明这一版在空配置、未登录时把目录默认选成了 `gpt-6.2-sol`。你的 `config.toml` 里如果已经写了 `model`，以你的配置为准。本文没有打开 `/model` 菜单。

[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 同一天对 `/model` 的说明是：如果工作区有权限，日常编码可以选择 GPT-6.2 Sol。这和 Release 的「默认选择」是两句不同的话。菜单里没有 Sol 时，先看套餐和企业开关，不要只靠升级 CLI。

## 新功能二：终端工作区默认开启

Release 的原文是：

> Enabled the TUI workspace by default, with searchable document previews, image previews, and subagent transcripts alongside the main conversation. (#61352, #61888, #61889, #61919, #62157)

0.169 那一版里，`tui_workspace` 还要自己打开，阶段记成 under development。0.171.0 把它默认打开了。

2026-11-20、独立空配置、未登录时，`codex features list` 里 `tui_workspace` 的 stage 是 `stable`，有效状态是 `true`。同一天用 `codex features disable tui_workspace` 之后，这一行变成 `stable`、有效状态 `false`，并且在 `config.toml` 的 `[features]` 里写下 `tui_workspace = false`。

侧栏里文档怎么搜、图片预览长什么样、子代理记录从哪里点开，Release 没有给按键。操作和关闭方式写在 [终端工作区](./27-Codex终端工作区-并排side-chat多标签页与重启后恢复.md)。本文没有进入 TUI，没有看到侧栏。

## 新功能三：codex exec --remote 连已有 app server

Release 的原文是：

> Added `codex exec --remote <ADDR>` to start or resume noninteractive sessions on an existing app server. (#61707)

2026-11-20 的 `codex exec --help` 有这两行：

- `--remote <ADDR>`：Connect to an existing app server
- `--remote-auth-token-env <ENV_VAR>`：Environment variable containing the remote WebSocket bearer token

同一天的 Developer commands 里，`codex exec` 一节还没有写 `--remote`。交互式 TUI 的 `--remote` 那一节是有的。所以「非交互会话也能接到已有 app server」目前以 Release 和本机帮助为准。

地址怎么写、明文 WebSocket 为什么只能走本机或 SSH 转发、token 放在哪个环境变量，见 [远程终端](./31-Codex远程终端-app-server-listen与codex-remote连接.md)。本文不把监听和认证再写一遍。

## 新功能四：/rc、/remote，输入框撤销重做，实验性的 MCP 状态栏

这三条都在 TUI 里。本文没有打开 TUI，只保留 Release 原句，并标出本机能核对的开关状态。

**远程控制。** Release 写：

> Added `/rc` and `/remote` to manage local remote control and display device pairing codes from the TUI. (#62121)

2026-11-20 的 Developer commands 斜杠命令表里还没有 `/rc` 和 `/remote`。命令出现在菜单的哪一项、配对码长什么样，本文不补。分组和边界见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。手机或另一台电脑控制主机，仍是另一条产品路径，见 [远程连接](./01-Codex远程控制另一台Mac.md)。

**撤销和重做。** Release 写：

> Added configurable undo and redo shortcuts to the non-Vim prompt composer, including restoration of attachments and large pastes. (#61954)

这是可配置的快捷键，并且写明不包括 Vim 输入模式。默认键位和 `/keymap` 的关系见斜杠命令一文。本文没有按过这些键。

**MCP 状态栏。** Release 写：

> Added custom MCP status line selection and authoring through `/statusline` when `tui_extensions_statusline` is enabled. (#61979, #61988, #62037)

同一天、空配置下，`codex features list` 里 `tui_extensions_statusline` 的 stage 是 `experimental`，有效状态是 `false`。没打开这个开关时，不要期待 `/statusline` 里出现自定义 MCP 状态栏。官方命令页当天对 `/statusline` 的说明仍是选择和排列页脚项。本文没有开启这个实验开关。

## 和日常使用有关的修复

下面几条按 Release 的 Bug Fixes 原文转述。本文没有复现这些故障，所以不写「升级后某条报错消失了」。

- 切换或恢复会话时，草稿、排队的追问和被打断的输入留在原来的线程上。（#61216）
- 切换工作目录时，权限 profile 保持完整。（#61195）
- 迟到的完成事件不再取消新一轮的审批。（#61801）
- Steer 当前回合时，汇总 diff 保留更早的编辑。（#61820）
- 滚动时插入乱字符、输入框光标跳动、以及按过期的终端尺寸重绘，这三件显示问题有修复。（#62139、#62174、#62175）
- 企业 MCP 登录：身份提供方只发 ID token、不发 refresh token 时，现在可以完成登录。（#62129）

权限 profile 和沙箱边界怎么配，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。本文不展开档案字段。

## 和 0.170.0 的关系

0.170.0 的 WebRTC 语音协商、实验性同名 MCP、Cloud 自动重连，发布说明没有在 0.171.0 里撤回。升到 0.171.0 不是用这一版替换那三件事，而是在那一版之上改了默认模型和默认工作区。

可以按这个顺序决定：

1. CLI 是每天都开的：升。升完看 `codex --version`，再看空配置或你的配置里 `tui_workspace` 是不是你要的状态。
2. 只想钉住一个版本做脚本：用 `npm install -g @openai/codex@0.171.0`，不要用 `codex update`。
3. 工作区、斜杠命令、app server 的步骤：分别读 [终端工作区](./27-Codex终端工作区-并排side-chat多标签页与重启后恢复.md)、[斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md) 和 [远程终端](./31-Codex远程终端-app-server-listen与codex-remote连接.md)。

## 参考资料

- [GitHub Release rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)
- [rust-v0.170.0...rust-v0.171.0](https://github.com/openai/codex/compare/rust-v0.170.0...rust-v0.171.0)
- [ChatGPT 与 Codex 更新日志](https://learn.chatgpt.com/codex/changelog)（2026-11-20 打开时，最新 CLI 条目仍是 0.170.0）
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- npm：`@openai/codex@0.171.0`
- 同库：[Codex CLI 0.170.0](./29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md)、[GPT-6.2 Astra 与 Sol](../10-配置模型与权限安全/29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)、[Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)

官方资料核对日期：2026-11-20（Asia/Shanghai）。依据是 Release、更新日志、Developer commands、npm 注册表和 Linux 上的 `codex-cli 0.171.0`。没有打开交互式 TUI，没有配图。
