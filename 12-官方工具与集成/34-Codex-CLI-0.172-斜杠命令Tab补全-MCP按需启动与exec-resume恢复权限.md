---
id: codex-cli-0-172-tab-completion-lazy-mcp-exec-resume
title: "Codex CLI 0.172.0：斜杠命令按 Tab 补全参数，可选 MCP 服务器首次调用才启动，codex exec resume 恢复沙箱权限"
seo_title: "Codex CLI 0.172.0：斜杠命令 Tab 补全与 exec resume"
description: "Codex CLI 0.172.0 已发布。本文按官方更新日志和 GitHub Release 说明怎么升级，斜杠命令 Tab 补全、可选 MCP 首次调用才启动、codex exec resume 恢复沙箱权限，以及连接应用工具的审批人和 code_mode_host_grpc 弃用分别是什么。"
lede: "0.172.0 改的是斜杠命令补全、MCP 何时启动，以及 codex exec resume 会不会把上次的沙箱权限带回来。日常在用 CLI 的人可以升。"
url: /guides/codex-cli-0-172-tab-completion-lazy-mcp-exec-resume
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 34
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-24
date_modified: 2026-11-24
verified_on: 2026-11-24
tested_cli_version: 0.172.0
official_ref: https://learn.chatgpt.com/docs/changelog
keywords: [Codex CLI 0.172.0, Codex 斜杠命令 Tab 补全, codex exec resume, Codex MCP 按需启动, code_mode_host_grpc]
related: [codex-cli-0-171-sol-default-workspace-exec-remote, mcp-getting-started, codex-cli-slash-commands]
howto: false
faq:
  - q: 现在就要升到 0.172.0 吗？
    a: 已经在用 CLI、并且会用斜杠命令、MCP 或 codex exec resume 的人，值得升。更新日志没有把这一版写成必须马上安装的安全公告。
  - q: codex update 会停在 0.172.0 吗？
    a: 不会。0.172.0 的 codex update --help 写的是更新到最新版，帮助里没有指定版本号的参数。要钉住这个正式版，用 npm install -g @openai/codex@0.172.0。
  - q: Tab 补全要自己开开关吗？
    a: 更新日志写的是按 Tab 补全受支持斜杠命令的参数，例子是 /mcp lo 补成 /mcp login。本文没有打开交互式 TUI，没有按过 Tab，也没有在 features list 里看到单独的补全开关。
  - q: code_mode_host_grpc 还要留在配置里吗？
    a: 更新日志写这项设置已弃用。2026-11-24 在 0.172.0 上把 features.code_mode_host_grpc 设为 true 后，程序打印该设置已弃用并被忽略，本地 code-mode host 始终用 gRPC over stdio，并提示从配置里删掉它。
---

# Codex CLI 0.172.0：斜杠命令按 Tab 补全参数，可选 MCP 服务器首次调用才启动，codex exec resume 恢复沙箱权限

> 核对依据：ChatGPT Learn [更新日志](https://learn.chatgpt.com/docs/changelog) 2026-11-24 的 Codex CLI 0.172.0，以及 GitHub Release [rust-v0.172.0](https://github.com/openai/codex/releases/tag/rust-v0.172.0)（发布时间 2026-11-24T00:03:55Z，北京时间 08:03）。两处顶部的 New Features、Bug Fixes、Documentation、Chores 条文一致。npm `dist-tags.latest` 为 `0.172.0`。`npm view @openai/codex@0.172.0 time` 里，该版本的时间是 `2026-11-24T00:09:39.503Z`，包的 `time.modified` 是 `2026-11-24T00:18:06.187Z`。2026-11-24 在 Linux 上安装 `@openai/codex@0.172.0`，`codex --version` 输出 `codex-cli 0.172.0`。完整提交列表见 [rust-v0.171.0...rust-v0.172.0](https://github.com/openai/codex/compare/rust-v0.171.0...rust-v0.172.0)。本文采用 Release 顶部说明，并对照了列表里同号 PR 的标题。列表里的内部重构不写成用户功能。本环境没有登录，没有打开交互式 TUI，没有配图。

这篇给已经在用 Codex CLI、想知道 0.172.0 该不该升的人。上一版的默认模型、终端工作区和 `codex exec --remote` 见 [Codex CLI 0.171.0](./30-Codex-CLI-0.171-默认GPT-6.2-Sol-终端工作区默认开启与exec-remote.md)。MCP 的配置和登录见 [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。斜杠命令分组见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

## 先说结论

0.172.0 是 0.171.0 之后的稳定版。和每天打开终端有关的是这三件：

- 受支持的斜杠命令可以按 Tab 补全参数。更新日志的例子是 `/mcp lo` 补成 `/mcp login`。
- 带有缓存工具列表的可选 stdio MCP 服务器，默认改成第一次调用工具时才启动。
- `codex exec resume` 会恢复已保存的沙箱权限、工作目录和 workspace roots，除非被显式覆盖。

另外知道即可：可以给单个连接应用的工具设审批人；app server 客户端在安装或登录时可以选 Amazon Bedrock Runtime；代理人命令中心用 Shift+Up / Shift+Down 在任务组之间跳；`code_mode_host_grpc` 已弃用。

发布说明没有把 0.172.0 写成必须马上安装的安全公告。

## 怎么升到 0.172.0

更新日志给出的固定版本命令是：

```bash
npm install -g @openai/codex@0.172.0
```

装完新开一个终端，再核对：

```bash
codex --version
```

2026-11-24 在 Linux 上执行了这条 npm 命令。系统默认的 npm 全局目录没有写权限，所以装到了当前用户可写的前缀。装完后的输出是 `codex-cli 0.172.0`。同一天查询的 npm `latest` 也是 `0.172.0`。

`codex update --help` 的说明是 “Update Codex to the latest version”。帮助里出现的参数是配置覆盖、功能开关和 `--help`，没有指定版本号的参数。它按安装来源更新到最新版，不能用来钉住 0.172.0。本文读了这段帮助，没有执行 `codex update`。

[Codex CLI](https://learn.chatgpt.com/docs/codex/cli) 同一天还写了另外两条更新方式。macOS 和 Linux 用安装脚本，Windows 用 PowerShell 脚本，Homebrew 用 `brew upgrade --cask codex`。这些默认都走最新版。渠道判断写在 [Codex 怎么更新和卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。本文今天没有跑安装脚本，也没有用 Homebrew。

要长期停在 0.172.0，用上面的 npm 版本号。以后 `latest` 再往前走时，不带版本号的安装命令会离开这一版。

## 新功能一：斜杠命令参数按 Tab 补全

更新日志和 Release 的原文是：

> Press Tab to complete arguments for supported slash commands. For example, `/mcp lo` completes to `/mcp login`. (#62343)

同号提交的标题是 “Add slash command argument completion to the TUI composer”。

这是终端输入框里的补全，而且写明是受支持的斜杠命令。更新日志只给了 `/mcp` 这一个例子。哪些命令能补、补全列表长什么样，本文没有看到。

2026-11-24 没有打开交互式 TUI，没有按 Tab。`codex features list` 里没有一条名字像 slash completion 的开关。补全是否对当前命令生效，以你打开会话后实际按 Tab 的结果为准。命令本身的分组仍见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

## 新功能二：可选 stdio MCP 服务器首次调用才启动

更新日志和 Release 的原文是：

> Optional stdio MCP servers with cached tool lists now start on their first tool call by default. (#62366)

同号提交的标题是 “Enable lazy startup for stdio MCP servers by default”。

句子里有三个限制：stdio、可选、而且已经有缓存的工具列表。它没有说每一种 MCP 都会推迟启动，也没有说远程 HTTP 服务器改了启动时机。

2026-11-24、独立空 `CODEX_HOME`、未登录时，`codex features list` 里 `mcp_lazy_stdio_startup` 的 stage 是 `stable`，有效状态是 `true`。同一天执行 `codex features disable mcp_lazy_stdio_startup` 之后，`config.toml` 的 `[features]` 写下 `mcp_lazy_stdio_startup = false`，这一行变成 `stable`、有效状态 `false`。

配置参考里和启动相关、而且本机能对上的键是 `mcp_servers.<名称>.startup_readiness`。参考页写：`connection` 是默认，用实时连接判断启动是否就绪；`catalog` 允许用有效的缓存工具目录先满足启动就绪，调用工具时仍要实时连接。0.172.0 上把 `startup_readiness` 设成 `"lazy"`，`--strict-config` 立即拒绝，期望值是 `connection` 或 `catalog`。不要把更新日志里的 “lazy” 填进这个键。

本文没有配置真实的 MCP 服务器，没有测量进程是不是在第一次工具调用时才出现。服务器怎么加、怎么登录，见 [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 新功能三：给单个连接应用工具设审批人

更新日志和 Release 的原文是：

> Set an approval reviewer for individual connected app tools in `config.toml`. (#62360)

同号提交的标题是 “Allow per-tool approval reviewers for Codex apps”。

2026-11-24 打开的 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 写了两级应用审批人，类型都是 `user | auto_review`：

- `apps._default.approvals_reviewer`：应用工具审批的默认审批人。省略时，应用继承顶层的 `approvals_reviewer`。
- `apps.<应用>.approvals_reviewer`：这个应用的工具审批人，覆盖上面的默认值。

同一页还有单个工具的 `apps.<应用>.tools.<工具>.approval_mode`，那是审批行为（`auto`、`prompt`、`writes`、`approve`），参考页没有把它写成审批人。

0.172.0 上，`--strict-config` 遇到 `approvals_reviewer="not-a-reviewer"` 会立即报错，期望值是 `user`、`auto_review`、`guardian_subagent`。把 `apps.example.tools.foo.approvals_reviewer` 设成 `"nope"` 时，报错位置写的是 `in apps`，期望值相同。参考页的类型栏没有列出 `guardian_subagent`，也没有写出「应用里单个工具的 approvals_reviewer」这个键名。本文不提供一份参考页上没有的配置示例。

本文没有连接应用，没有看到审批提示。

## 修复：codex exec resume、远程路径和报错时机

下面按 Release 的 Bug Fixes 转述。除了帮助文本，本文没有复现这些故障，所以不写「升级后某条报错消失了」。

**`codex exec resume`。** 原文是：

> `codex exec resume` restores saved sandbox permissions, the working directory, and workspace roots unless explicitly overridden. (#62194)

同号提交的标题是 “Preserve saved sandbox permissions when resuming `codex exec`”。

2026-11-24 的 `codex exec resume --help` 写的是按会话 id 恢复，或用 `--last` 选最近一次。帮助里还有 `--all`、`--remote`、`--remote-auth-token-env`、`--skip-git-repo-check`、`--trust`、`--ephemeral`。这段帮助没有单独说明沙箱权限从哪里读、怎样算「显式覆盖」。`codex exec --help` 有 `--sandbox`，可选值是 `read-only`、`workspace-write`、`danger-full-access`。本文没有已保存的会话，没有执行 `codex exec resume`。

官方 [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) 仍写：继续上一次非交互运行用 `codex exec resume --last`，也可以把会话 id 放在 `resume` 后面。那一页的例子没有写沙箱恢复。

**远程会话的路径。** 客户端和服务器操作系统不同时，远程会话保留工作目录、workspace roots 和可写路径。（#62375、#62376、#62377）对应标题分别是保留 app-server 线程工作目录、沙箱可写根和 workspace roots。本文没有搭两台不同系统的 app server。

**提供方错误。** 响应流里一出现提供方错误就报告，并标明触达的是哪一项 API 花费限额。（#62329、#62356）本文没有登录，没有看到这类报错界面。同一次未登录的 `codex exec` 在请求模型时以 401 结束，那是缺少认证，不是这条花费限额修复的复现。

**其余三条。** 打断父回合时，子代理已经排队的回复会留给下一回合。（#62348）答案区比终端更高时，用 PageUp 和 PageDown 阅读并提交选项。（#62209）历史加载之后才完成的 Cloud 回复会就地更新，终端记录保持顺序。（#62403）这三件都在交互或 Cloud 会话里。本文没有打开 TUI，也没有 Cloud 任务。

## 其他：线程链接、任务组、Bedrock 和弃用项

**从搜索和记录打开已保存的线程。** 更新日志写：可以从搜索结果和记录里的线程链接，在终端里打开已保存的对话和嵌套代理。（#62332）提交标题是 “Open Codex thread links inside the TUI”。本文没有搜索过历史会话。

**任务组导航。** 在代理人命令中心用 Shift+Up 和 Shift+Down 在任务组之间跳。（#62200）提交标题是 “Add task group navigation to the agent command center”。本文没有打开命令中心。

**Bedrock Runtime。** app server 客户端可以在安装或登录时选择 Amazon Bedrock Runtime。（#62222）提交标题是 “Allow Bedrock Runtime selection during setup and login”。登录向导、Runtime 与 Mantle 的配置见 [Codex 接入 Amazon Bedrock](./16-Codex接入Amazon-Bedrock-登录向导与配置.md)。本文没有走 Bedrock 登录。

**文档技能。** 捆绑的 `openai-docs` 技能现在覆盖迁移到 GPT-6.2 Astra 和 Sol，包括端点选择和工具调用要求。（#62447）本文没有调用这个技能。

**`code_mode_host_grpc`。** Chores 的原文是：

> Code Mode now uses gRPC for all host connections. The `code_mode_host_grpc` setting is deprecated. (#62476)

提交标题是 “Use gRPC for all code-mode host connections”。

2026-11-24 的 `codex features list` 里，`code_mode_host_grpc` 的 stage 是 `removed`，有效状态是 `false`。同一天用 `--strict-config` 传入 `features.code_mode_host_grpc=true`，程序在请求模型之前打印：

```text
deprecated: `[features].code_mode_host_grpc` is deprecated and ignored.
The local code-mode host always uses gRPC over stdio. Remove this setting from your configuration.
```

随后这次未登录请求以 401 结束。更新日志只说明全部主机连接改走 gRPC、这项设置弃用。上面两行是这一版自己打印的弃用说明。

另一条 Chores 是 Python 格式化和 SDK 类型生成会按仓库锁文件核对依赖哈希。（#62346）这是仓库工具，不是终端用户的操作步骤。

## 和 0.171.0 的关系

0.171.0 把 GPT-6.2 Sol 写成模型目录的默认选择，并把终端工作区默认打开。0.172.0 的发布说明没有撤回这两件默认事。

2026-11-24、空配置、未登录的 `codex exec` 在请求模型之前仍打印 `model: gpt-6.2-sol`，沙箱一行是 `sandbox: read-only`。随后因缺少认证以 401 结束，没有模型回复。这只说明这一版空配置下的启动摘要仍是这个模型名，不能代替你自己的 `config.toml`。

可以按这个顺序决定：

1. CLI 是每天都开的：升。升完看 `codex --version`。
2. 只想钉住一个版本做脚本：用 `npm install -g @openai/codex@0.172.0`，不要用 `codex update`。
3. 斜杠命令、MCP 和 Bedrock 的步骤：分别读 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)、[Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) 和 [Amazon Bedrock](./16-Codex接入Amazon-Bedrock-登录向导与配置.md)。

## 参考资料

- [ChatGPT 与 Codex 更新日志](https://learn.chatgpt.com/docs/changelog)（2026-11-24 的 Codex CLI 0.172.0）
- [GitHub Release rust-v0.172.0](https://github.com/openai/codex/releases/tag/rust-v0.172.0)
- [rust-v0.171.0...rust-v0.172.0](https://github.com/openai/codex/compare/rust-v0.171.0...rust-v0.172.0)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- npm：`@openai/codex@0.172.0`
- 同库：[Codex CLI 0.171.0](./30-Codex-CLI-0.171-默认GPT-6.2-Sol-终端工作区默认开启与exec-remote.md)、[Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)、[斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)

官方资料核对日期：2026-11-24（Asia/Shanghai）。依据是更新日志、Release、Configuration Reference、Non-interactive mode、Codex CLI 页、npm 注册表和 Linux 上的 `codex-cli 0.172.0`。没有打开交互式 TUI，没有配图。
