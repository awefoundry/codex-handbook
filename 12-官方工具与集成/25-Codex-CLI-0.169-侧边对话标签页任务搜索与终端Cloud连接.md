---
id: codex-cli-0-169-side-chat-cloud-connection
title: Codex CLI 0.169.0：侧边对话多标签页、任务搜索、折叠回合详情，以及在终端连接 Cloud
seo_title: Codex CLI 0.169.0：侧边标签页、任务搜索与终端 Cloud 连接
description: Codex CLI 0.169.0 为可选终端工作区加上多个 side-chat 标签页，并能在 agent 命令中心搜索旧任务、折叠回合详情、在终端添加自定义模型供应商，以及在 macOS 和 Linux 连接 Cloud 会话。本文按官方 changelog 和 GitHub Release 整理升级命令、主要新功能和与 0.167、0.168 的差异。
lede: 同一天先有 0.168.0，再有 0.169.0。要钉住正式版，用 npm 安装 0.169.0；终端里的新界面本文没有拍到。
url: /guides/codex-cli-0-169-side-chat-cloud-connection
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 25
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-14
date_modified: 2026-11-14
verified_on: 2026-11-14
tested_cli_version: 0.169.0
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.169.0
keywords: [Codex CLI 0.169.0, side-chat 标签页, agent 命令中心搜索, Collapse turn details, 自定义模型供应商, Ctrl+S 诊断包, 终端 Cloud 连接, codex exec --trust]
related: [codex-cli-0-167-agent-command-center, codex-update-uninstall, codex-custom-model-provider, codex-terminal-workspace-side-chat]
howto: false
faq:
  - q: 现在就要升到 0.169.0 吗？
    a: 要用多标签 side chat、在命令中心搜索旧任务、折叠回合详情、在终端里改自定义供应商，或在 macOS、Linux 上使用发布说明里的 Cloud 连接，就升。发布说明没有把这一版写成必须安装的安全更新。
  - q: codex update 会停在 0.169.0 吗？
    a: 不会。0.169.0 的 codex update --help 写的是更新到最新版。要固定这个正式版，用 npm install -g @openai/codex@0.169.0。
  - q: 未信任目录里加了 --sandbox workspace-write，项目配置会加载吗？
    a: 0.169.0 实测不会。codex exec 仍提示未信任的项目配置被禁用，启动摘要也不采用项目里的 model。要保存信任，给 codex exec 或 codex review 加上 --trust。
  - q: 终端工作区的标签页在哪？
    a: 0.168 的开关是 features.tui_workspace，0.169 在这个可选工作区里增加多个 side-chat 标签页。0.169.0 的 features list 里该开关是 under development，未写入配置时有效状态是 false。本文没有打开 TUI，没有拍到标签页。
---

# Codex CLI 0.169.0：侧边对话多标签页、任务搜索、折叠回合详情，以及在终端连接 Cloud

> 本文在线版：[codexguide.io/guides/codex-cli-0-169-side-chat-cloud-connection](https://codexguide.io/guides/codex-cli-0-169-side-chat-cloud-connection)

> 核对依据：GitHub Release [rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)（发布时间 2026-11-13T08:37:05Z，北京时间 16:37）和 [rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)（2026-11-13T03:54:29Z，北京时间 11:54）；ChatGPT Learn [更新日志](https://learn.chatgpt.com/docs/changelog) 2026-11-13 的 Codex CLI 0.169.0 条目，与 GitHub Release 的 New Features、Bug Fixes 一致。npm 注册表当天 `latest` 为 `0.169.0`，`0.169.0` 的发布时间为 2026-11-13T08:43:21.818Z（北京时间 16:43）。2026-11-14 在 Linux 上执行 `npm install -g @openai/codex@0.169.0`，`codex --version` 输出 `codex-cli 0.169.0`。下文凡是只来自发布说明、没有在本机界面里点过的行为，都会写明。本环境没有登录，没有打开 TUI，没有 macOS 或 Windows，没有配图。

这篇给已经在用 Codex CLI、想知道 0.169.0 该不该升的人。0.167.0 的命令中心、本机图片预览和 GCP 向导见 [Codex CLI 0.167.0](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)。安装渠道和 `codex update` 怎么按来源更新，见 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。自定义供应商的配置文件写法见 [自定义模型提供商](../10-配置模型与权限安全/11-Codex自定义模型提供商-model_providers与openai_base_url.md)。工作区怎么跟做，见 [终端工作区](./27-Codex终端工作区-并排side-chat多标签页与重启后恢复.md)。

## 先看结论

0.169.0 的更新日志 New Features 是这六条：

- 可选终端工作区支持多个 side-chat 标签页。可以用键盘或鼠标切换，重启后能打开已保存的本地 side chat。
- 在 agent 命令中心按名称、提示预览或工作目录搜索更早的任务。
- 在全屏转录里打开 **Collapse turn details**，把已完成活动收在每条提示下面，同时保留回答可见、工具输出可搜索。
- 在终端添加或编辑自定义模型供应商。开启自定义网关引导后，可以在登录时创建供应商，并在 SSH 或没有本地浏览器时，对支持的网关使用设备码。
- 在终端报告编辑器按 `Ctrl+S`，把诊断 ZIP 存到本地，即使关闭了上传。
- 在 macOS 和 Linux 上开启可选的 Cloud 连接后，可以从终端发图片、选模型和推理强度，并归档或恢复 Cloud 会话。

该不该立刻升：

- 要用上面任意一条：升到 0.169.0。工作区和 Cloud 连接都是 opt-in，升完还要自己打开。
- 人在 Windows，只为了发布说明里的 Cloud 连接：这一条写的是 macOS 和 Linux。Windows 沙箱修复是另一条，见下文。
- 日常还停在 0.167，上面几项都用不到：可以等你平时的更新渠道。这一版的发布说明没有单独列出需要马上安装的安全公告。

同一天稍早的 0.168.0 没有单独成文，速览在下一节之后。

## 怎么升到 0.169.0

更新日志给出的固定版本命令是：

```bash
npm install -g @openai/codex@0.169.0
```

装完新开一个终端，再核对：

```bash
codex --version
```

2026-11-14 在 Linux 上安装后，输出是 `codex-cli 0.169.0`。npm 上 `latest` 当天也指向 0.169.0。

0.169.0 的 `codex update --help` 说明是 “Update Codex to the latest version”。它跟到的是最新版，不是钉死 0.169.0。要固定版本，用上面的 npm 命令。各安装渠道怎么更新，见 [更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。

## 0.168.0 同一天发布了什么

0.168.0 的 New Features，按 Release 原文：

- 在 **Sessions → Model providers** 浏览供应商，并为新对话选择默认供应商。
- 打开 `features.tui_workspace` 后，在主对话旁边看 side conversation。拖动分隔条改宽度，或按 `leader z` 放大当前窗格。
- 使用具备音频能力的模型时可以附加录音。Codex 会在后续回合跳过已确认拒绝的录音，并用片段时长把更多短录音留在上下文里。
- 打开 `features.image_generation_animation` 后，可以生成或编辑动画 GIF，并可设置帧数和时间。
- 全屏 Codex 在 Ghostty 和 Kitty 的 tmux 里显示图片预览和 pets，需要 `allow-passthrough all`。
- 设置 `tui.notification_method = "osc777"` 使用终端通知。审批通知会显示更长的命令预览，并把终端输入请求和网络访问请求区分开。

0.169.0 上用独立的 `CODEX_HOME` 跑了 `codex features list`：`tui_workspace` 和 `image_generation_animation` 都是 under development，未写入配置时有效状态是 false。用 `--strict-config` 加载 `tui.notification_method = "osc777"` 时，没有报未知字段；本机没有会显示 OSC 777 的终端，没有看到通知。Sessions 菜单、录音、GIF 和 tmux 画面都没有打开。

0.168.0 的 Bug Fixes 也只列 Release 里的六条：本地 TUI 历史和 resume 选择器按当前登录的 ChatGPT 账号过滤新建线程；已经打开或恢复的对话，在你改了新对话的默认供应商之后，仍使用自己保存的供应商；被工具调用打断的回复按一条 Markdown 渲染，重放对话时恢复推理摘要；在最终转录保存期间或切回长任务时发出的 steering 消息能到达正在跑的回合；模糊文件搜索提高文件名匹配的权重；Windows 上空闲的本地 MCP 服务器把文件系统 I/O 留给 Codex 的其余部分。

## 侧边对话多标签页

0.168 先提供并排的 side conversation，0.169 在这个可选工作区上增加多个 side-chat 标签页：键盘或鼠标切换，重启 Codex 后可以重新打开已保存的本地 side chat。

打开方式沿用 0.168 的配置键。0.169.0 的 `codex exec --help` 写明 `--enable <FEATURE>` 等价于 `-c features.<name>=true`。一次临时打开可以写成：

```bash
codex --enable tui_workspace
```

写进用户级配置则是：

```toml
[features]
tui_workspace = true
```

2026-11-14 用 `-c features.tui_workspace=true` 启动 `codex exec` 时，终端警告：`Under-development features enabled: tui_workspace`。这只说明配置键被这一版接受，并且开关仍标成开发中。发布说明没有写出切换标签的具体按键，只写了键盘或鼠标；`leader z` 是 0.168 用来放大当前窗格的写法，Release 没有说明 leader 键本身是哪一个键。本文没有进入全屏 TUI，没有看到标签、分隔条或放大后的窗格。跟做步骤见 [终端工作区](./27-Codex终端工作区-并排side-chat多标签页与重启后恢复.md)。

## 在命令中心搜索旧任务

0.167 已经可以用 `codex agents` 打开命令中心。0.169.0 的 `codex agents --help` 仍是：打开 agent command center，用来浏览和切换会话；`--no-daemon` 的说明是用嵌入的 app server 跑这个总览。帮助文本没有写搜索。

搜索能力来自 0.169 的发布说明：在命令中心按名称、提示预览或工作目录搜索更早的任务。本文没有打开命令中心，没有输入过搜索词，也没有拍到结果列表。会话的 resume、fork 和命名仍见 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。

## Collapse turn details

发布说明的位置是全屏转录：打开 **Collapse turn details**，把已完成活动折到每条提示下面，回答保持可见，工具输出仍可搜索。Release 没有写出菜单的上一级叫什么，也没有给出快捷键。本文没有打开全屏转录，没有核对中文界面是否翻译了这个英文名称。使用这个英文名去找开关。

## 终端里添加或编辑模型供应商

0.168 可以在 Sessions → Model providers 里浏览供应商，并为新对话选默认值。已经打开或恢复的对话继续用自己保存的供应商。

0.169 补上：在终端添加或编辑自定义模型供应商；开启自定义网关引导后，登录时可以创建供应商，并在 SSH 或没有本地浏览器时，对支持的网关使用设备码。

发布说明没有写出「自定义网关引导」对应的配置键。0.169.0 的 `codex features list` 里有 `gateway_setup_wizard`，阶段是 stable，未写入配置时有效状态是 false。Release 没有把这个名字写成 custom gateway onboarding，本文没有打开它。设备码、网关 OAuth 和 `config.toml` 的差别见 [自定义模型提供商](../10-配置模型与权限安全/11-Codex自定义模型提供商-model_providers与openai_base_url.md)。本文没有真实网关，没有走设备码。

## Ctrl+S 保存诊断 ZIP

在终端的报告编辑器里按 `Ctrl+S`，把诊断 ZIP 存到本地。发布说明写明：即使关闭了上传，这条保存仍然可用。本文没有打开报告编辑器，没有生成 ZIP，也没有核对文件名和保存目录。不要把对话、密钥或本地用户名打进准备外发的压缩包。

## 在 macOS 和 Linux 从终端连接 Cloud

发布说明限定平台：macOS 和 Linux，而且是 opt-in。打开之后，可以从终端发图片、选择模型和推理强度，并归档或恢复 Cloud 会话。Release 没有写出开关名、菜单路径或快捷键。0.169.0 的 `codex features list` 里没有名称包含 cloud 的功能开关。

同一版的 `codex cloud --help` 是另一条实验子命令，说明文字是 “Browse tasks from Codex Cloud and apply changes locally”，子命令为 `exec`、`status`、`list`、`apply`、`diff`。帮助文本没有写出发图片、选推理强度、归档或恢复会话。本文不把 `codex cloud` 当成 0.169 这条 Cloud 连接。写作环境是 Linux，但没有登录，没有打开 opt-in 连接，没有 Cloud 任务。云端环境本身见 [Codex Cloud 云端环境](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。

## 重要修复

这些行为按 0.169 Release 的 Bug Fixes 书写。带「实测」的句子来自 2026-11-14 的 Linux 命令，其余没有在对应系统上复现。

### 未信任目录里的 `codex exec`

Release：`codex exec` 在未信任目录里不加载项目配置和 MCP，即使加了 `--sandbox workspace-write`。要用 `codex exec` 或 `codex review` 的 `--trust`，才会明确保存项目信任。

0.169.0 的帮助文本与此相符。`codex exec --help` 和 `codex review --help` 里 `--trust` 的说明是：保存这个项目以及以后对话的信任，包括沙箱外的 MCP 命令；即使同时使用 `--ephemeral` 也会持久保存；不会覆盖一个被明确标成不信任的项目。

实测用的是临时 git 仓库和独立 `CODEX_HOME`。项目 `.codex/config.toml` 把 `model` 设成 `project-should-not-load`，并写了一个 MCP 服务器。未加 `--trust`、只加 `--sandbox workspace-write` 时，终端先警告：

```text
warning: Untrusted project-local configuration is disabled. Run `codex exec --trust` to allow project configuration and MCP servers for this and future chats in the project, including MCP commands outside the sandbox. Explicitly untrusted projects must have their trust setting updated first.
```

启动摘要里的 model 仍是这次未设置用户级 model 时打印的 `gpt-6.1-sol`，sandbox 已是 `workspace-write`。加上 `--trust` 之后，这条警告消失，启动摘要里的 model 变成项目文件中的 `project-should-not-load`。两次都没有登录，请求随后因缺少凭证失败。本文没有确认 MCP 进程是否被拉起，只确认了项目配置在未信任时没有改掉 model。

`--trust` 会把信任存下来。只想看一眼项目、还不准备信任其中的 MCP 时，不要随手加上这个参数。

### 计划交接、Windows 沙箱、粘贴图片、MCP 等待和中断的回合

Release 的其余修复：

- **Yes, clear context and implement** 会把完整的已批准计划交给新会话；交接失败时保持当前会话打开。
- Windows 沙箱：修正带引号的 `cmd.exe` 路径，以及工作目录的父目录不可读时的 PowerShell 会话。
- macOS 上粘贴的图片保持预期方向，并在剪贴板有原生 PNG 或 JPEG 时使用这份数据。
- 共享 app server 没有报告的 MCP 服务器，不再让终端一直处于等待。
- 被中断的回合会干净结束；延迟的中止或文件审批取消，不再打断后来的回合。

这五条本文都没有复现。写作环境不是 Windows 或 macOS，也没有走到计划确认按钮。

### 文档和杂项

Release 的 Documentation：`openai-docs` skill 改为聚焦 Codex 与 ChatGPT Work 的问题和首次 API 设置，并有面向团队配置 Codex 的说明；app-server 客户端可以列出模型，或为已配置的供应商授权网关，而不改变默认供应商。

Chores：捆绑的 SQLite 更新到 3.54，以带上 write-ahead log 修复；插件市场升级可以复用磁盘上已有的 Git 对象，减少重复下载。本文没有核对 SQLite 版本号，也没有升级插件市场。

## 和 0.167 比多了什么

| 能力 | 0.167.0 | 0.168.0 | 0.169.0 |
| --- | --- | --- | --- |
| 命令中心 | `codex agents` 打开，并标出未读 | Release 未改这条入口 | 可按名称、提示预览或工作目录搜索旧任务 |
| 并排侧边对话 | 无此开关 | `features.tui_workspace`，分隔条和 `leader z` | 多个 side-chat 标签页，重启后打开已保存的本地 side chat |
| 供应商 | 配置文件和 GCP 向导 | Sessions → Model providers；已打开的对话保留自己的供应商 | 终端里添加或编辑；自定义网关引导与支持网关的设备码 |
| 全屏转录 | 审批未关闭时展开补丁详情 | Ghostty、Kitty 的 tmux 图片预览 | Collapse turn details |
| Cloud | 无 0.169 这条连接 | 无 | macOS、Linux 上的可选连接：图片、模型、推理强度、归档或恢复 |
| 未信任项目 | 见当时的信任规则 | Release 未列这条 | `codex exec` 即使 `workspace-write` 也不加载项目配置和 MCP，需 `--trust` |

0.167 专文里的本机图片预览、Sign in another way、`gcp_setup_wizard` 和 `respect_system_proxy` 没有在 0.169 的 New Features 里被宣布移除。本文没有逐项重测它们是否仍在。

## 常见问题

### 找不到 side-chat 标签

先确认版本是 `codex-cli 0.169.0` 或更新的正式版，并且 `features.tui_workspace` 已打开。0.169.0 上这个开关默认是关的，阶段仍是 under development。发布说明只保证可选工作区支持多个标签，没有写出标签栏的坐标。本文没有拍到界面。

### 重启后标签不见了

Release 写的是重新打开**已保存的本地** side chat。它没有写 Cloud 会话、远程 app server 上的会话，或从未保存的临时窗格也会自动出现。恢复普通主会话仍用 `codex resume`，见 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。

### `--trust` 和交互式里的信任提示是一回事吗

Release 把 `--trust` 写在 `codex exec` 和 `codex review` 上，用来明确保存项目信任。0.169.0 的帮助还写了：它不会覆盖一个已经被明确标成不信任的项目。交互式 TUI 里的信任提示本文没有打开。

### 诊断包会不会自动上传

`Ctrl+S` 的发布说明强调的是存到本地，并且在关闭上传时仍然可以存。本文没有看到上传开关的位置，也没有检查 ZIP 里有哪些文件。外发之前自己打开压缩包，去掉密钥和账号信息。

## 参考资料

- [GitHub Release rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
- [GitHub Release rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)
- [ChatGPT 与 Codex 更新日志](https://learn.chatgpt.com/docs/changelog)（2026-11-13 的 0.169.0 条目）
- [npm @openai/codex](https://www.npmjs.com/package/@openai/codex)
- 同库：[Codex CLI 0.167.0](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)、[终端工作区](./27-Codex终端工作区-并排side-chat多标签页与重启后恢复.md)、[自定义模型提供商](../10-配置模型与权限安全/11-Codex自定义模型提供商-model_providers与openai_base_url.md)、[更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)

官方资料核对日期：2026-11-14（Asia/Shanghai）。终端工作区、命令中心搜索、Collapse turn details、供应商编辑界面和 Cloud 连接都没有截图。
