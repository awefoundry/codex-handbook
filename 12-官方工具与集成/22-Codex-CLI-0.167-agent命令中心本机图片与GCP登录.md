---
id: codex-cli-0-167-agent-command-center
title: Codex CLI 0.167.0：用 codex agents 打开命令中心，本机图片预览、跨后端会话切换与 GCP 登录
seo_title: Codex CLI 0.167.0：codex agents 命令中心、图片预览与 GCP 向导
description: Codex CLI 0.167.0 用 codex agents --no-daemon 打开命令中心并标出未读，会话选择器可在已连接后端之间切换并保留草稿。本文按更新日志写本机图片预览、Sign in another way、默认关闭的 GCP 向导，以及 /experimental 里的系统代理。
lede: 0.167.0 把多会话、未读、图片预览和另一条登录入口收进终端。GCP 向导和系统代理都要你自己打开，而且向导本文没有跑过。
url: /guides/codex-cli-0-167-agent-command-center
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 22
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-07
date_modified: 2026-11-07
verified_on: 2026-11-07
tested_cli_version: 0.167.0
official_ref: https://learn.chatgpt.com/docs/changelog
keywords: [Codex CLI 0.167.0, codex agents, gcp_setup_wizard, respect_system_proxy, Sign in another way, Codex 命令中心]
related: [macos-install-codex-cli, codex-cli-presets-inline-model, codex-amazon-bedrock, codex-google-cloud-model-garden]
howto: false
faq:
  - q: 现在就要从 0.166 升到 0.167.0 吗？
    a: 要用命令中心、跨后端切换、本机图片预览，或把 API Key 和云厂商登录收进 Sign in another way，就升。发布说明没有把这一版写成必须安装的安全更新。已经按配置文件接好 Vertex AI 的人，不打开向导也能继续用原来的配置。
  - q: 打开命令中心的命令是什么？
    a: 更新日志写的是 codex agents --no-daemon。0.167.0 的 codex agents --help 把这条子命令说明为打开命令中心，用来浏览和切换会话；--no-daemon 的说明是用嵌入的 app server 跑这个总览。本文没有打开交互界面。
  - q: 不打开 gcp_setup_wizard 还能用 Google Cloud 吗？
    a: 能。向导默认关着。已经按《Codex 接入 Google Cloud Vertex AI》写好 model_provider 的配置继续有效。向导是另一条登录入口，本文没有 GCP 项目，没有走完向导。
  - q: 系统代理默认会跟着 macOS 或 Windows 的设置走吗？
    a: 不会。respect_system_proxy 在 0.167.0 里是 experimental，未写入配置时有效状态是 false。发布说明只把这个选项放在 macOS 或 Windows 的 /experimental。改完后按对应 PR 的说明重启。本文没有验证流量是否走代理。
---

# Codex CLI 0.167.0：用 codex agents 打开命令中心，本机图片预览、跨后端会话切换与 GCP 登录

> 本文在线版：[codexguide.io/guides/codex-cli-0-167-agent-command-center](https://codexguide.io/guides/codex-cli-0-167-agent-command-center)

> 核对依据：ChatGPT Learn [更新日志](https://learn.chatgpt.com/docs/changelog) 2026-11-06 的 Codex CLI 0.167.0 条目，GitHub Release [rust-v0.167.0](https://github.com/openai/codex/releases/tag/rust-v0.167.0)（发布时间 2026-11-06T01:40:00Z），npm 包 [@openai/codex@0.167.0](https://www.npmjs.com/package/@openai/codex/v/0.167.0)（registry 记录的发布时间为 2026-11-06T01:46:01.347Z，当天 `latest` 指向 0.167.0）。2026-11-07 在 Linux 上安装这个 npm 包，`codex --version` 输出 `codex-cli 0.167.0`。功能开关写在一份独立的 `CODEX_HOME` 里，检查完已删除。没有登录，没有打开交互式命令中心，没有 GCP 项目，没有走登录向导，也没有本机图片预览的画面。下文界面行为若只来自发布说明或对应 PR，会写明。

这篇给已经在用 Codex CLI、想知道 0.167.0 该不该升、升完多了哪几条终端能力的人。安装渠道本身见 [macOS 安装 Codex CLI](../01-安装与首次使用/04-macOS安装Codex-CLI.md)。0.164.0 的 `/presets` 和内联 `/model`、`/permissions` 见 [预设与内联命令](./15-Codex-CLI-presets预设与内联model-permissions命令.md)。Bedrock 登录见 [接入 Amazon Bedrock](./16-Codex接入Amazon-Bedrock-登录向导与配置.md)。Vertex AI 的配置文件写法见 [接入 Google Cloud Vertex AI](./13-Codex接入Google-Cloud-Model-Garden.md)。

## 先看结论

0.167.0 的更新日志 New Features 是这六条：

- 用 `codex agents --no-daemon` 打开 agent command center。命令中心和会话选择器会标出未读结果。
- 在终端的会话选择器里切换已经连接的后端，切换时保留草稿。
- 在支持的终端里，编写消息时预览本机图片附件；看过的本机图片可以从记录里的可点击路径打开。
- API Key 和云厂商选项放在 “Sign in another way” 下面。打开 `gcp_setup_wizard` 后，可以用 Application Default Credentials 或凭证文件配置 Google Cloud Vertex AI。
- 从 `/experimental` 选择使用 macOS 或 Windows 的系统代理。
- 审批提示还开着时，可以直接在记录里展开补丁详情。

该不该立刻升，看你用不用上面这些：

- 要在终端里看多条会话、未读、跨后端切换，或要预览本机图片：升到 0.167.0。
- 要在登录页里找 API Key、Bedrock 或 Vertex AI：升。Vertex 向导另外要打开功能开关，默认是关的。
- 人在 macOS 或 Windows，并且 Codex 要跟着系统代理走：升，再在 `/experimental` 里打开。发布说明没有把这项写成 Linux 功能。
- 日常还停在 0.166.0 的斜杠命令和会话上，上面几项都用不到：可以等你平时的更新渠道。这一版的发布说明没有单独列出需要马上安装的安全公告。

已经按 Vertex 专文写好 `model_provider = "gcp"` 的配置，不依赖这次的向导。向导是一条新的登录入口。

## 怎么升到 0.167.0

更新日志给出的固定版本命令是：

```bash
npm install -g @openai/codex@0.167.0
```

装完新开一个终端，再核对：

```bash
codex --version
```

2026-11-07 在 Linux 上安装同一版本后，输出是 `codex-cli 0.167.0`。npm 上 `latest` 当天也指向 0.167.0。0.167.0 的 `codex --help` 里有 `update` 子命令，说明文字是 “Update Codex to the latest version”。它跟到的是最新版，不是 “钉死 0.167.0”。要固定版本，用上面的 npm 命令。

macOS 上如果当初用的是官方脚本或 Homebrew Cask，更新仍走原来的渠道，见 [macOS 安装 Codex CLI](../01-安装与首次使用/04-macOS安装Codex-CLI.md) 和 [Codex 更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。Homebrew 和安装脚本什么时候收到 0.167.0，以更新之后的 `codex --version` 为准。同一台机器上有多份 `codex` 时，先看 `which -a codex` 或 Windows 上的 `Get-Command codex -All`，确认你升的是正在用的那一份。

## codex agents：命令中心和未读

0.167.0 的帮助里，这条子命令是：

```text
agents    Open the agent command center to browse and switch sessions
```

`codex agents --help` 对 `--no-daemon` 的说明是：用嵌入的 app server 跑这个总览（Run the agents overview with an embedded app server）。更新日志要求用的就是带这个参数的形式：

```bash
codex agents --no-daemon
```

未读来自这几条改动：[#58238](https://github.com/openai/codex/pull/58238)、[#58239](https://github.com/openai/codex/pull/58239)、[#58263](https://github.com/openai/codex/pull/58263)、[#58264](https://github.com/openai/codex/pull/58264)。发布说明的原话是：命令中心和会话选择器现在会标出未读结果。#58264 的标题是 Show unread sessions and acknowledge viewed transcripts in the picker。

本文执行了 `--help`，没有进入交互界面，所以没有未读标记的画面，也不知道看过记录之后标记何时消失。低于 0.167.0 时，不要假设本机已经有 `codex agents`。

## 会话选择器里切换后端

发布说明的第二条：从终端的会话选择器切换已经连接的后端，切换时保留草稿（[#58280](https://github.com/openai/codex/pull/58280)、[#58457](https://github.com/openai/codex/pull/58457)）。

PR 58457 写明的行为是：

- 选中的会话由它所属的后端恢复。先准备目标，再换掉当前会话。
- 保留草稿，并恢复目标那边的设置、账号状态、模型目录和工作区服务。
- 当前这一轮还在跑时，不切换后端。
- 目标准备失败时，留下当前会话。

这些是 PR 描述，不是本文点出来的菜单。没有登录，也就没有 “已连接的后端” 可以切换。只接了一个 OpenAI 登录时，这条能力没有额外的后端可换。Bedrock 与 Vertex 的配置方式仍以那两篇专文为准。

同一版的修复还写了：切换模型提供商之后，已保存的聊天仍能看见。某条聊天不能恢复时，可以读它的记录，并准备一段可编辑的提示，到新聊天里继续（[#58202](https://github.com/openai/codex/pull/58202)）。本文没有做这次切换。

## 本机图片预览和可点击路径

发布说明：在支持的终端上，编写消息时预览本机图片附件；看过的本机图片可以从记录里的可点击路径打开（[#58261](https://github.com/openai/codex/pull/58261)、[#58446](https://github.com/openai/codex/pull/58446)）。

PR 58261 补充的范围是：本地工作区、支持的终端、内联视图和全屏视图里按引用顺序显示草稿附件缩略图；放不下的附件显示 `+N`；预览不可用或空间不够时，仍保留可编辑的图片引用。预览会在附件文件变化时刷新。

“支持的终端” 以你本机为准。本文没有粘贴图片，没有缩略图，也没有点开记录里的路径。预览没出现时，先确认 `codex --version` 已经是 0.167.0，再看当前终端是否在发布说明说的支持范围内。本文没有一份失败画面可以对照。

## Sign in another way 和 GCP 向导

发布说明：API Key 和云厂商选项在 “Sign in another way” 下面。打开 `gcp_setup_wizard`，可以用 Application Default Credentials 或凭证文件配置 Google Cloud Vertex AI（[#57857](https://github.com/openai/codex/pull/57857)、[#58427](https://github.com/openai/codex/pull/58427)）。

PR 58427 写明子菜单里有三项：OpenAI API key、Amazon Bedrock、Google Cloud Vertex AI。主菜单保留 ChatGPT 登录和 device code。`Esc` 从子菜单返回。按住 Enter 或数字快捷键时，不会连着跳过多步，也不会在没有新的确认时保存预先填好的 API Key。

PR 57857 写明向导在功能开关 `features.gcp_setup_wizard` 后面，默认关闭。向导收集项目 ID、可选的 location、可选的凭证文件。凭证文件留空时使用 Application Default Credentials。凭证校验和配置写入交给 app-server。

2026-11-07 在独立的 `CODEX_HOME` 里查看 0.167.0 的 `codex features list`：

| 功能 | 阶段 | 未写入配置时的有效状态 |
|---|---|---|
| `gcp_setup_wizard` | stable | false |
| `bedrock_setup_wizard` | stable | true |
| `respect_system_proxy` | experimental | false |

Bedrock 向导在 0.164.0 已经默认开启，和 [Bedrock 专文](./16-Codex接入Amazon-Bedrock-登录向导与配置.md) 一致。GCP 向导的阶段已经是 stable，有效状态仍是关。

在那份临时配置里执行 `codex features enable gcp_setup_wizard` 之后，`config.toml` 变成：

```toml
[features]
gcp_setup_wizard = true
```

命令输出是：Enabled feature `gcp_setup_wizard` in config.toml. 这只证明开关能写入。没有登录页，没有项目 ID，没有凭证文件，没有 Application Default Credentials，向导的每一步都没有跑。临时配置已删除。

要自己打开向导，用上面的功能命令，或把同样的表写进你的 `~/.codex/config.toml`。字段含义、模型和限制仍看 [Vertex AI 专文](./13-Codex接入Google-Cloud-Model-Garden.md)。那篇按 0.165.0 写的是配置文件接法，不是这次的登录向导。

## /experimental 里的系统代理

发布说明：从 `/experimental` 选择使用 macOS 或 Windows 的系统代理（[#58157](https://github.com/openai/codex/pull/58157)）。

PR 58157 写明：

- `/experimental` 里增加 “System proxy”。
- `respect_system_proxy` 默认关闭。
- `codex doctor` 在 macOS 上的代理说明改为指向 `/experimental`，以及 `codex features enable respect_system_proxy`。
- 改完之后重启 Codex。

同一天在临时 `CODEX_HOME` 里执行 `codex features enable respect_system_proxy`，配置里出现 `respect_system_proxy = true`。没有重启一个正在跑的会话，没有发请求，没有核对流量是否走系统代理。

发布说明的系统范围是 macOS 或 Windows。本文的二进制跑在 Linux 上，功能列表里看得到这个开关，这不表示 Linux 桌面代理已经按这条说明接通。

## 和 0.166 比，多了什么

[0.166.0 的更新日志](https://learn.chatgpt.com/docs/changelog)（2026-10-29）里，用户能直接碰到的新增主要是：记录里的键盘选择和搜索、异步问答的 Markdown、模型目录里的 GPT-6.1 Terra、`codex queue --resume`、更清楚的安全拦截说明，以及 `codex doctor --network-only`。这些 0.167.0 没有撤掉。本文没有再装一份 0.166.0 做并排对比。

0.167.0 多出来、并且写在 New Features 里的，就是上面六条。同页 Bug Fixes 还写了这些，本文都没有复现：

- 切换模型提供商后，已保存聊天仍可见；不能恢复的聊天可以读记录，并准备一段提示到新聊天继续。
- `Ctrl+L` 清的是终端显示，更早的消息仍能用 `Ctrl+T` 看到。
- 删掉文字后露出开头的 `!` 时，草稿仍留在聊天模式。
- 网络审批在请求结束后关闭。对同一端点的并发请求，一次只问一个。
- 较长的 realtime V3 对话会把已经完成的语音存进聊天记录。
- 自动压缩上下文时，会计入失败响应里保留的输出，以及缺少 token 用量数据的响应。

发布说明的 Chores 还写了：Linux musl 构建减少 allocator arena，用来降低对话卸载后的空闲内存。这不是一条新的斜杠命令。完整 PR 列表在 [rust-v0.166.0...rust-v0.167.0](https://github.com/openai/codex/compare/rust-v0.166.0...rust-v0.167.0)。没有写进 New Features 或 Bug Fixes 的条目，本文不当成已经可以跟做的功能。

## 怎么确认升到位

1. `codex --version` 显示 `codex-cli 0.167.0`。
2. `codex agents --help` 的第一行说明是打开命令中心。
3. 需要 GCP 向导时，`codex features list` 里 `gcp_setup_wizard` 的有效状态为 true。未打开时，列表里它是 stable，有效状态 false。
4. 需要系统代理时，在 macOS 或 Windows 上打开 `/experimental` 的 System proxy，或写入 `respect_system_proxy = true`，然后重启。再看 doctor 的网络检查是否还提示代理。本文没有做第 4 步的流量验证。

## 常见问题

**命令中心和 `codex resume` 是同一个入口吗？**

`codex --help` 里两行同时存在。`resume` 的说明仍是恢复之前的交互会话，默认打开选择器。`agents` 的说明是打开命令中心，用来浏览和切换会话。更新日志把未读和跨后端切换写在命令中心和会话选择器上。本文没有并排打开这两个界面。

**图片预览会不会把图上传到别处？**

发布说明写的是编写时预览本机附件，以及从记录里的路径打开看过的本机图片。它没有写一条新的上传策略。附件最终是否随消息发给模型，仍按你当时的会话和审批。本文没有附图片。

**打开了 GCP 向导，是不是就不用看 Vertex 专文？**

向导负责收集项目 ID、可选区域和可选凭证文件。模型列表、`model_provider = "gcp"`、以及走 Google Cloud 时哪些功能不可用，仍以 [Vertex 专文](./13-Codex接入Google-Cloud-Model-Garden.md) 和你项目里实际开通的模型为准。本文没有跑向导。

## 参考资料

- [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog)（2026-11-06，Codex CLI 0.167.0；对照 2026-10-29 的 0.166.0）
- [openai/codex rust-v0.167.0](https://github.com/openai/codex/releases/tag/rust-v0.167.0)
- npm：[@openai/codex@0.167.0](https://www.npmjs.com/package/@openai/codex/v/0.167.0)
- [#57857](https://github.com/openai/codex/pull/57857)、[#58157](https://github.com/openai/codex/pull/58157)、[#58427](https://github.com/openai/codex/pull/58427)、[#58457](https://github.com/openai/codex/pull/58457)、[#58261](https://github.com/openai/codex/pull/58261)
