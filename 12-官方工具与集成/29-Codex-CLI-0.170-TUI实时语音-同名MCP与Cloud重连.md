---
id: codex-cli-0-170-voice-mcp-reconnect
title: Codex CLI 0.170.0：终端实时语音用上 WebRTC，同名 MCP 可按环境分开，Cloud 断线会自动重连
seo_title: Codex CLI 0.170.0：WebRTC 语音、同名 MCP 与 Cloud 重连
description: Codex CLI 0.170.0 已发布。本文按官方 changelog 和 GitHub Release 说明怎么升级，TUI 实时语音的 WebRTC 协商、实验性同名 MCP、Cloud 自动重连分别是什么，以及 WebSocket 回退、MCP OAuth、子线程沙箱和 Windows 权限修复对日常使用有什么影响。
lede: 已经在用 0.169 的人，为语音协商、Cloud 重连和子线程沙箱修复可以升到 0.170.0。同名 MCP 仍是实验功能，本文不写配置示例。
url: /guides/codex-cli-0-170-voice-mcp-reconnect
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 29
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-19
date_modified: 2026-11-19
verified_on: 2026-11-19
tested_cli_version: 0.170.0
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.170.0
keywords: [Codex CLI 0.170.0, Codex WebRTC 语音, Codex 同名 MCP, Codex Cloud 重连, /voice]
related: [codex-cli-0-169-side-chat-cloud-connection, codex-voice-chatgpt-voice, codex-update-uninstall, reconnecting-network-troubleshooting, permissions-sandbox-approvals]
howto: false
faq:
  - q: 现在就要升到 0.170.0 吗？
    a: 要用 TUI 实时语音的 WebRTC 协商、Cloud 会话断线后的自动重连，或子线程和权限更新不再丢掉已有沙箱限制，就升。发布说明没有把这一版写成必须安装的安全公告。实验性同名 MCP 没有用户配置文档，不要只为这一条去升。
  - q: codex update 会停在 0.170.0 吗？
    a: 不会。0.170.0 的 codex update --help 写的是更新到最新版，帮助里没有指定版本号的参数。要钉住这个正式版，用更新日志里的 npm install -g @openai/codex@0.170.0。
  - q: 升到 0.170.0 就能在终端里打语音电话吗？
    a: 发布说明增加的是 TUI 实时语音的 WebRTC 协商。Developer commands 仍要求当前构建和会话支持语音，再用 /voice 或 F8。本文没有麦克风，没有打开 TUI，没有打通过话。
  - q: 同名 MCP 怎么按环境分开配？
    a: 发布说明只有一句 experimental support，没有独立的用户文档，也没有给出配置字段。0.170.0 的 features list 里 multi_environment_mcp 是 under development，空配置下有效状态是 false。本文不写配置示例。
---

# Codex CLI 0.170.0：终端实时语音用上 WebRTC，同名 MCP 可按环境分开，Cloud 断线会自动重连

> 核对依据：GitHub Release [rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)（发布时间 2026-11-18T03:40:48Z，北京时间 11:40）和 ChatGPT Learn [更新日志](https://learn.chatgpt.com/codex/changelog) 2026-11-18 的 Codex CLI 0.170.0。两处的 New Features、Bug Fixes、Documentation 条文一致。npm 注册表 `dist-tags.latest` 为 `0.170.0`，该版本的 `time` 为 2026-11-18T03:45:45.798Z（北京时间 11:45）。2026-11-19 在 Linux 上安装 `@openai/codex@0.170.0`，`codex --version` 输出 `codex-cli 0.170.0`。完整提交列表见 [rust-v0.169.0...rust-v0.170.0](https://github.com/openai/codex/compare/rust-v0.169.0...rust-v0.170.0)。本文只采用 Release 顶部的三类说明；列表里的内部重构不写成用户功能。本环境没有登录，没有打开 TUI，没有麦克风，没有配图。

这篇给已经在用 Codex CLI、想知道 0.170.0 该不该升的人。上一版的侧边对话、任务搜索和终端 Cloud 连接见 [Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。`/voice`、F8、mute、stop 和 settings 的用法见 [Codex 语音怎么用](./23-Codex语音-ChatGPT-Voice指挥任务与语音听写.md)。安装渠道和 `codex update` 怎么按来源更新，见 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。

## 先说结论

已经在用 0.169 这一代的人，下面三件事值得升到 0.170.0：

- TUI 实时语音加入了 WebRTC 协商。
- Cloud 会话的自动重连有改进，客户端重连时会保留正在进行的恢复回合。
- 权限更新和子线程不再丢掉已有沙箱限制。

另外两条可以知道，但不必单独为它们升级：OpenTelemetry HTTP 导出器会自动刷新认证头；实验性支持在不同环境使用同名 MCP 服务器。后者没有用户配置文档。

发布说明没有把 0.170.0 写成必须马上安装的安全公告。npm 上 `0.169.1` 的发布时间是 2026-11-17T22:26:21.610Z。本文没有打开 0.169.1 的 Release 正文，不把那一版的改动算进 0.170.0。

## 怎么升到 0.170.0

更新日志给出的固定版本命令是：

```bash
npm install -g @openai/codex@0.170.0
```

装完新开一个终端，再核对：

```bash
codex --version
```

2026-11-19 在 Linux 上执行了这条 npm 命令。当时系统默认的 npm 全局目录没有写权限，所以装到了当前用户可写的前缀。装完后的输出是 `codex-cli 0.170.0`。同一天查询的 npm `latest` 也是 `0.170.0`。

`codex update --help` 的说明是 “Update Codex to the latest version”。帮助里出现的参数是配置覆盖、功能开关和 `--help`，没有指定版本号的参数。它按安装来源更新到最新版，不能用来钉住 0.170.0。本文读了这段帮助，没有执行 `codex update`。

Homebrew 和官方安装脚本默认也是走最新版。渠道判断、`brew upgrade --cask codex`，以及 macOS、Linux、Windows 的安装脚本命令，写在 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。本文今天没有跑安装脚本，也没有用 Homebrew。

要长期停在 0.170.0，用上面的 npm 版本号。以后 `latest` 再往前走时，不带版本号的安装命令会离开这一版。

## 新功能一：TUI 实时语音的 WebRTC 协商

Release 和更新日志的原文是：

> Added WebRTC negotiation for realtime voice calls in the TUI. (#61172)

提交标题是 “Negotiate realtime voice calls in the TUI”。

这是协商方式。`/voice`、F8、`/voice mute`、`/voice stop`、`/voice settings` 怎么用，以 [Developer commands](https://learn.chatgpt.com/docs/developer-commands) 为准，步骤写在 [语音一文](./23-Codex语音-ChatGPT-Voice指挥任务与语音听写.md)。本文不把通话过程再写一遍。

2026-11-19 在这台 Linux 上能核对的只有非交互文本：

- `codex --help` 的子命令和选项里没有 `/voice`、F8、mute、stop、settings。斜杠命令不在这条帮助里。
- 可执行文件里有 `Usage: /voice [settings|mute|stop]`，以及 “When voice is available, use /voice to start or stop a voice conversation, or /voice settings to choose a voice”。这只说明构建里带有这些字符串。
- 独立的空 `CODEX_HOME`、未登录时，`codex features list` 里 `in_app_voice` 的 stage 是 `stable`，有效状态是 `true`。本文没有对照 0.169 的同一行，不能说这个开关是 0.170.0 新打开的。
- 同一份二进制里有 `realtime-webrtc` 的源码路径。这和发布说明的 WebRTC 协商一致。本文没有完成一次协商，也没有把二进制里未经文档说明的地址字段写成配置项。

`codex login status` 在这个空目录里输出 `Not logged in`，退出码 1。语音会话是否还要求 ChatGPT 登录，要在支持语音的会话里看。本文没有进入那个会话。

## 新功能二：实验性支持在不同环境使用同名 MCP

Release 和更新日志的原文是：

> Added experimental support for using identically named MCP servers across environments. (#60905)

提交标题是 “Keep same-named MCP servers separate across environments”。

这是实验功能。2026-11-19 没有找到把这句话展开成用户步骤的独立文档，所以这里只保留原句：不同环境里可以使用同名的 MCP 服务器，服务器按环境分开。

同一天、同一台机器、独立空配置且未登录时，`codex features list` 里有 `multi_environment_mcp`，stage 是 `under development`，有效状态是 `false`。发布说明没有写这个开关的名字。本文不把它写成官方配置教程，也不写启用命令或配置字段。

`codex mcp --help` 能打开 MCP 子命令的帮助，但帮助文本没有解释「同名服务器按环境分开」怎么填。没有这份说明之前，不要照着猜测的表去改 `config.toml`。

## 新功能三：OpenTelemetry HTTP 导出器会自动刷新认证头

Release 和更新日志的原文是：

> Added automatically refreshed authentication headers for OpenTelemetry HTTP exporters. (#61028)

提交标题是 “Add refreshable headers for OTLP HTTP exporters”。

如果你已经把追踪导出到一个会轮换认证的 HTTP 收集器，0.170.0 会为这类导出器自动刷新认证头。本文没有收集器，没有导出过追踪，也没有在文档里找到要手写的头字段，所以不给配置示例。

## 和日常使用有关的修复

下面每条都先引 Release 原文，再写它对日常使用的含义。没有在本机复现的，会写明。

**过大的 WebSocket 会立刻回退 HTTP。** 原文：Oversized WebSocket requests now fall back to HTTP without unnecessary retries.（#60840、#60841）。提交标题分别是 “Fall back to HTTP immediately for oversized WebSocket requests” 和 “Honor advertised WebSocket message size limits”。发布说明没有给出字节阈值，也没有说 `stream_max_retries` 的默认次数变了。受影响的是过大的 WebSocket 请求：直接改走 HTTP，不再做多余重试。普通断线是否仍按原来的次数重试，发布说明没有改写。排查顺序见 [一直显示 Reconnecting](../15-故障排查与常见问题/03-Codex一直Reconnecting-stream-disconnected排查.md)。

**Cloud 会话会自动重连，并保留正在恢复的回合。** 原文：Improved automatic reconnection for Cloud conversations and preserved active recovery turns when clients reconnect.（#60969、#61014）。#60969 的标题是 “Reconnect idle Cloud conversations after transient stream loss”，#61014 的标题是 “Preserve active recovery turns when clients reconnect”。短暂断流之后，空闲的 Cloud 会话会重连；客户端重连时，正在进行的恢复回合还在。这是 Cloud 会话上的行为。它不代替本机代理、证书或公司网络的排查。终端里怎么连上 Cloud，仍见 [0.169.0 一文](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。本文没有 Cloud 环境，没有拔过网线做对照。

**MCP OAuth 在取消、登录、退出时不再互相踩凭据。** 原文：Fixed MCP OAuth credential races during cancellation, login, and logout.（#60849、#60981）。标题是 “Protect MCP OAuth persistence from stale credential writes” 和 “Make reactive MCP OAuth refreshes cancellation-safe”。如果你在登录或退出 MCP 时取消过流程，然后看到旧凭据写回去，这一版修的是这条竞态。本文没有走 OAuth。

**权限更新和子线程不再丢掉已有沙箱限制。** 原文：Fixed permission updates and child threads losing existing sandbox restrictions.（#60936、#61134）。怎么理解沙箱和审批，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。发布说明没有写复现步骤。本文没有开子线程。

**Windows 上的文件替换、沙箱权限和运行时注册。** 原文：Fixed Windows file replacement, sandbox permission preservation, and runtime registration recovery.（#60872、#60943、#60944）。标题分别涉及 Windows 原子写入、重复设置沙箱时保留文件权限，以及服务权限出错后恢复运行时注册。写作环境是 Linux，这三条没有实测。

**文件搜索和带空格的线程搜索。** 原文：Removed duplicate file search results and fixed thread search snippets for queries containing whitespace.（#60845、#60846）。搜索结果里的重复文件会去掉；查询里带空格时，线程搜索摘要会按修复后的方式截取。本文没有在 TUI 里搜过。

文档项只有一条：Updated sandbox documentation to explain permission profiles and filesystem rules.（#61133）。当前要对照的页面是 [Permissions](https://learn.chatgpt.com/docs/permissions)。档案和 `sandbox_mode` 怎么分开，写在权限一文，这里不重复档案示例。

## 和 0.169.0 的关系

0.169.0 加上的是可选终端工作区里的多个 side-chat 标签页、命令中心里的任务搜索、折叠回合详情、终端里的自定义供应商，以及 macOS 和 Linux 上的可选 Cloud 连接。那些功能留在 0.169 那篇。0.170.0 没有把它们撤掉，也没有在发布说明里改写它们的开关。

可以按这个顺序决定：

1. 要语音协商、Cloud 断线后的自动重连，或子线程沙箱修复：升到 0.170.0，然后用 `codex --version` 确认输出是 `codex-cli 0.170.0`。
2. 只为同名 MCP：先等有用户文档。本机看到的开关默认是关的。
3. 人在 Windows，而且文件替换或沙箱权限在反复设置后丢过：发布说明写了修复，但本文没有 Windows 环境，不能替你验收。
4. 日常已经稳定、上面几项都碰不到：可以等你平时的更新渠道。钉版本用 npm 的版本号，不要指望 `codex update` 停在 0.170.0。

社交网站上的讨论没有写进上面的结论。功能以 Release 和更新日志为准。

## 参考资料

- [GitHub Release rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)
- [ChatGPT Learn 更新日志](https://learn.chatgpt.com/codex/changelog)
- [rust-v0.169.0...rust-v0.170.0](https://github.com/openai/codex/compare/rust-v0.169.0...rust-v0.170.0)
- [Developer commands：Talk to Codex with /voice](https://learn.chatgpt.com/docs/developer-commands)
- [Permissions](https://learn.chatgpt.com/docs/permissions)
- [Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)
- [Codex 语音怎么用](./23-Codex语音-ChatGPT-Voice指挥任务与语音听写.md)
- [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)
