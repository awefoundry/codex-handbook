---
id: codex-glossary
title: Codex 术语表：官方 111 个术语中英对照，按用途分组并附对应中文教程
seo_title: Codex 术语表：官方术语中英对照与名词解释
description: 把 OpenAI 官方 Codex Glossary 的 111 个术语逐条译成中文，按产品入口、对话与上下文、权限沙箱、配置与企业管理、扩展、Git 与 Worktree、自动化、云端与开发接口 8 组整理，每条标注适用范围并附站内对应教程。
lede: 看官方文档或英文界面遇到不认识的词，先在这里查中文意思，再顺着链接去看对应教程。
url: /guides/codex-glossary
status: published
section: guides
category: K-troubleshooting
topic: 认识、安装与环境
content_type: 参考
source_tag: 官方功能
entry_tags: [App, CLI, IDE, Cloud]
difficulty: 入门
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-13
date_modified: 2026-11-13
verified_on: 2026-11-13
official_ref: https://learn.chatgpt.com/docs/glossary
keywords: [Codex 术语表, Codex 名词解释, Codex 中英对照, Codex 概念, sandbox, permission profile, worktree, MCP, Skill]
related: [permissions-sandbox-approvals, codex-config-toml-cheatsheet, codex-cli-commands-cheatsheet]
faq:
  - q: 这份术语表和官方的是什么关系？
    a: 术语、分组前的原始定义和适用范围都来自官方 Glossary 页面（2026-11-13 核对时共 111 条），本文逐条译成中文并按用途重新分组。官方以后增删术语，以官方页面为准。
  - q: Sandbox、Sandbox mode 和 Permission profile 有什么区别？
    a: Sandbox 是限制命令能访问什么的强制边界；Sandbox mode 是旧的配置方式，用 read-only、workspace-write 等档位定义边界；Permission profile 是新的方式，用有名字的 profile 组合文件系统和网络规则，官方推荐 Codex 0.138.0 及以上使用。
  - q: Chat、Conversation、Thread、Turn 都是「对话」吗？
    a: 不完全一样。Chat 是保存下来的对话空间；Conversation 是对话里持续的消息往来；Turn 是其中一次往来（一条提示加一次回复）；Thread 是 app-server 和 SDK 接口里的技术对象，开发集成时才会碰到。
  - q: Skill、Plugin、Connector、MCP server 怎么区分？
    a: Skill 是一套可复用的指令和脚本；Connector 把 Codex 连到外部服务；MCP server 是按 MCP 协议提供工具和上下文的服务；Plugin 是可安装的包，可以把 Skill、连接器、MCP 服务器和 Hook 打包在一起分发。
---

# Codex 术语表：官方 111 个术语中英对照，按用途分组并附对应中文教程

> 本文在线版：[codexguide.io/guides/codex-glossary](https://codexguide.io/guides/codex-glossary)

> 核对依据：OpenAI 官方 [Codex Glossary](https://learn.chatgpt.com/docs/glossary)，2026-11-13 核对，共 111 条。「意思」一列按官方英文定义翻译，「适用」一列按官方标注的适用范围翻译；分组和站内教程链接是本站整理的。纯参考页，没有截图。

Codex 的官方文档和界面大多是英文，同一个意思还常有好几个相近的词：Chat 和 Conversation、Sandbox 和 Sandbox mode、Worktree 和 Git worktree。这页把官方术语表的 111 个词全部译成中文，分成 8 组，每组按英文字母排序。查到词之后，可以点最后一列去看站内对应的中文教程；没有专门教程的标「—」。

## 先看最容易混的几组

| 容易混的词 | 区别 |
|---|---|
| Sandbox / Sandbox mode / Permission profile | Sandbox 是强制边界本身；Sandbox mode 是旧的档位式配置（只读、工作区可写、完全访问）；Permission profile 是新的命名 profile，组合文件和网络规则，官方推荐 0.138.0 及以上使用 |
| Approval policy / Automatic approval review | 前者规定什么时候要审批；后者是让另一个模型代替人审查审批请求（界面上叫 Auto-review） |
| Chat / Conversation / Turn / Thread | Chat 是对话空间，Conversation 是其中的消息往来，Turn 是一次往来，Thread 是 SDK 和 app-server 里的技术对象 |
| Profile / Permission profile | Profile 是 config.toml 里的一套命名配置预设；Permission profile 只管权限 |
| config.toml / requirements.toml | 前者是用户自己的配置；后者是管理员强制下发的限制，冲突时以后者为准 |
| Live web search / Web search cache | 前者实时联网查询；后者用预先索引的搜索结果，不实时浏览 |
| Worktree / Git worktree / Local | Git worktree 是 Git 本身的功能；Worktree 是 Codex 把改动隔离在单独 worktree 里的模式；Local 是直接在你电脑上的项目目录里改 |
| Scheduled task / Heartbeat | 都是定时任务；Heartbeat 是固定回到同一个对话的周期任务 |
| Skill / Plugin / Connector / MCP server | Skill 是指令和脚本；Connector 连外部服务；MCP server 按协议提供工具；Plugin 可以把前面几样打包分发 |

## 1. 产品与入口（12 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| API key sign-in | API Key 登录 | 用 OpenAI API Key 认证登录。 | 桌面端、CLI、IDE | [登录 Codex 并确认入口可用](../01-安装与首次使用/07-登录Codex.md) |
| Appshot | Appshot（应用快照） | 把最前面的应用窗口快照发到 ChatGPT 或 Codex 对话里。 | 桌面端 | [Codex Appshots](../12-官方工具与集成/18-Codex-Appshots-把当前应用窗口发给对话.md) |
| Auth cache | 登录缓存 | Codex 在本地保存并复用的登录凭据。 | 桌面端、CLI、IDE | [登录 Codex 并确认入口可用](../01-安装与首次使用/07-登录Codex.md) |
| ChatGPT desktop app | ChatGPT 桌面端 | 集成 ChatGPT 和 Codex 的桌面应用，包含 Chat 与 Work、项目、文件预览、定时任务和开发者工具。 | 桌面端 | [macOS 安装 Codex App](../01-安装与首次使用/02-macOS安装Codex-App.md) |
| ChatGPT sign-in | ChatGPT 账号登录 | 用 ChatGPT 账号和工作区权限认证登录。 | 桌面端、CLI、IDE、云端 | [登录 Codex 并确认入口可用](../01-安装与首次使用/07-登录Codex.md) |
| ChatGPT Work | ChatGPT Work | ChatGPT 里负责调研、分析，以及生成文档、演示文稿、表格等成品的 agent。 | 桌面端、网页 | [Chat、ChatGPT Work 和 Codex 怎么选](../00-从这里开始/04-Chat-Work和Codex怎么选.md) |
| Codex | Codex | OpenAI 用于软件开发任务的编程 agent。 | 桌面端、CLI、IDE、网页、云端、SDK | [Codex 是什么](../00-从这里开始/01-Codex是什么.md) |
| Codex CLI | Codex 命令行 | 在终端里交互式或用脚本运行 Codex 的客户端。 | 终端 | [macOS 安装 Codex CLI](../01-安装与首次使用/04-macOS安装Codex-CLI.md) |
| Codex IDE extension | Codex IDE 扩展 | 在 VS Code、JetBrains、Cursor、Windsurf 等编辑器里使用 Codex 的集成。 | IDE | [VS Code、Cursor 和 Windsurf 安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md) |
| Computer Use | Computer Use（操作电脑） | 让 ChatGPT 通过界面操作其他应用的桌面能力。 | 桌面端 | [Codex 使用 Computer Use 操作桌面应用](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md) |
| Computer Use in the browser | 在内置浏览器里操作 | 让 ChatGPT 直接操作桌面端内置浏览器的能力。 | 桌面端 | [Codex 浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md) |
| Slash command | 斜杠命令 | 在 CLI 会话里以 / 开头输入、用于控制或查看会话的命令。 | CLI | [Codex CLI 斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md) |

## 2. 对话、任务与上下文（18 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| Agent | 智能体 / agent | Codex 的代理本体：基于上下文推理、调用工具、完成任务。 | 桌面端、CLI、IDE、云端 | [Codex 是如何工作的](../02-核心概念与任务方法/01-Codex是如何工作的.md) |
| Chat | 对话（Chat） | 和 ChatGPT 或 Codex 交流的保存空间，包含共享上下文、结果和操作。Quick chat 可以从 Codex 里发起一个 ChatGPT 对话。 | 桌面端、网页、手机、CLI、IDE、云端 | — |
| Compaction | 压缩（compact） | 把较早的上下文总结压缩，让长时间的工作能继续。 | 桌面端、CLI、IDE、云端 | [Codex 上下文窗口与压缩](../02-核心概念与任务方法/07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md) |
| Computer History | Computer History | macOS 上需主动开启的功能，从允许的应用和网站的交互事件里生成记忆和时间线。 | 桌面端 | — |
| Context | 上下文 | Codex 工作时能用到的信息，比如文件、之前的消息、工具输出和指令。 | 桌面端、CLI、IDE、云端、SDK | [给 Codex 多大上下文才够用](../03-项目理解与上下文/04-给Codex多大上下文才够用.md) |
| Context window | 上下文窗口 | 模型一次能考虑的最大信息量。 | 桌面端、CLI、IDE、云端、SDK | [Codex 上下文窗口与压缩](../02-核心概念与任务方法/07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md) |
| Conversation | 会话内容 | 在一个对话里，人与 ChatGPT 或 Codex 之间持续的消息往来和共享上下文。 | 桌面端、网页、手机、CLI、IDE、云端 | — |
| Fast mode | Fast 模式 | 让支持的模型回复更快、但消耗更多额度的速度设置。 | CLI、IDE | [Codex 用量额度怎么看](../10-配置模型与权限安全/08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md) |
| Local chat | 本地对话 | 在用户自己电脑上运行的 ChatGPT 或 Codex 对话。 | 桌面端、CLI、IDE | — |
| Memories | 记忆（Memories） | Codex 在本地保存、可跨会话复用的上下文。 | 桌面端、CLI、IDE | [Codex Memories 记忆功能](../11-自动化与高级工作流/12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md) |
| Model | 模型 | Codex 用来推理和调用工具的 AI 模型。 | 桌面端、CLI、IDE、云端、SDK | [Codex 模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md) |
| Plan | 计划 | Codex 为完成任务提出或跟踪的步骤。 | 桌面端、CLI、IDE、云端 | [Codex Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md) |
| Project | 项目 | 一组相关对话和共享资料，或用于基于文件工作的本地文件夹。 | 桌面端 | — |
| Prompt | 提示词 | 发给 ChatGPT 或 Codex 的问题、指令或目标。 | 桌面端、CLI、IDE、云端、SDK | — |
| Reasoning effort | 推理强度 | 控制模型使用多少推理预算的设置。 | 桌面端、CLI、IDE、SDK | [Codex 模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md) |
| Standalone task | 独立任务 | 不归属于任何项目的 Codex 任务。 | 桌面端、CLI、IDE、云端 | — |
| Task | 任务 | ChatGPT 或 Codex 要达成的明确结果，比如修一个 bug、写一份文档、调研一个问题。 | 桌面端、网页、手机、CLI、IDE、云端 | — |
| Turn | 轮次（turn） | 对话里的一次往来，通常是一条用户提示加上 agent 的回复和操作。 | 桌面端、CLI、IDE、云端、SDK | [Codex 上下文窗口与压缩](../02-核心概念与任务方法/07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md) |

## 3. 权限、沙箱与审批（16 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| Action | 操作 | 由人、ChatGPT 或 Codex 执行的一次动作，比如改文件、跑命令、使用已连接的服务。 | 桌面端、网页、手机、CLI、IDE、云端 | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Approval policy | 审批策略 | 规定 Codex 什么时候必须先询问再行动的规则。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Approval request | 审批请求 | Codex 请求允许执行一个受限操作。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Automatic approval review | 自动审批审查（Auto-review） | 在审批请求放行前，由模型对符合条件的请求做审查。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Deny-read rule | 禁止读取规则 | 阻止 Codex 读取敏感路径或匹配某个通配模式的文件系统权限规则。 | 桌面端、CLI、IDE、企业 | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Filesystem permission | 文件系统权限 | 权限 profile 里允许或拒绝读写某些路径的规则。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Full access | 完全访问 | Codex 不受常规沙箱限制运行的模式。 | 桌面端、CLI、IDE | [Codex 沙箱与主机权限风险](../10-配置模型与权限安全/05-Codex沙箱与主机权限风险.md) |
| Network access | 网络访问 | 允许命令或环境访问互联网的权限。 | 桌面端、CLI、IDE、云端 | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Network policy | 网络策略 | 按域名允许或拒绝，用来限制沙箱内出站网络流量的规则。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Permission profile | 权限 profile | 有名字的最小权限策略，组合文件系统和网络规则，作用于本地命令执行。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Prefix rule | 前缀规则 | 命令规则里的匹配模式，对匹配的命令前缀允许、询问或禁止。 | 桌面端、CLI、IDE、企业 | [Codex Rules 怎么写](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md) |
| Read-only mode | 只读模式 | Codex 可以查看，但未经批准不能修改的模式。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Rules | 命令规则（Rules） | 允许、询问或拒绝某些命令前缀或权限例外的策略。 | 桌面端、CLI、IDE | [Codex Rules 怎么写](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md) |
| Sandbox | 沙箱 | 限制 Codex 运行的命令能访问或修改什么的强制边界。 | 桌面端、CLI、IDE | [Codex 沙箱与主机权限风险](../10-配置模型与权限安全/05-Codex沙箱与主机权限风险.md) |
| Sandbox mode | 沙箱模式 | 定义 Codex 文件系统和网络限制的配置。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |
| Writable roots | 可写目录 | 允许 Codex 修改的目录。 | 桌面端、CLI、IDE | [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) |

## 4. 配置与企业管理（12 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| `AGENTS.md` | AGENTS.md | 仓库或用户级的说明文件，给 Codex 持久生效的指令。 | 桌面端、CLI、IDE、云端 | [Codex AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md) |
| Analytics dashboard | 分析看板 | 管理员查看 ChatGPT 工作区使用情况和 Codex 报表的中心。 | 企业 | — |
| Compliance API | 合规 API | 导出支持的 ChatGPT 工作区记录和审计元数据的 API。 | 企业 | — |
| `config.toml` | config.toml | Codex 的本地配置文件。 | 桌面端、CLI、IDE | [Codex config.toml 配置指南](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md) |
| Environment variable | 环境变量 | 任务执行时可用的运行时配置值。 | 云端、CLI、IDE | [Codex 读懂配置、环境变量和启动脚本](../03-项目理解与上下文/07-读懂配置环境变量和启动脚本.md) |
| Live web search | 实时网页搜索 | 实时联网查询最新信息。 | 桌面端、CLI、IDE | [Codex 网页搜索设置](../10-配置模型与权限安全/18-Codex网页搜索设置-cached-indexed-live与allowed_domains.md) |
| Managed configuration | 受管配置 | 由组织控制的 Codex 默认值和限制。 | 企业 | [Codex config.toml 配置指南](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md) |
| MDM | MDM（移动设备管理） | 用于分发设备描述文件和受管 Codex 设置的设备管理工具。 | 企业 | — |
| Profile | 配置 profile | Codex 的命名配置预设。 | CLI、IDE | [Codex config.toml 配置指南](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md) |
| RBAC | RBAC（基于角色的访问控制） | 按角色管理工作区权限。 | 企业 | — |
| `requirements.toml` | requirements.toml | 受管部署里由管理员强制执行的要求文件。 | 企业 | [Codex config.toml 配置指南](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md) |
| Web search cache | 网页搜索缓存 | Codex 不必实时浏览就能用的预先索引的搜索结果。 | 桌面端、CLI、IDE | [Codex 网页搜索设置](../10-配置模型与权限安全/18-Codex网页搜索设置-cached-indexed-live与allowed_domains.md) |

## 5. 扩展：Skills、插件、MCP 与 Hooks（18 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| Apps (configuration) | apps（配置字段） | Codex 配置和 app-server 里以 apps 为名保存连接器设置的字段。 | 桌面端、CLI、IDE | [Codex 插件入口怎么用](../08-插件工作流/04-Codex插件入口与工作流.md) |
| Connector | 连接器 | 插件的组成部分，把 ChatGPT 或 Codex 连到外部服务的数据和操作。 | Desktop app (ChatGPT Work、Codex)、网页（Work） | [Codex 插件入口怎么用](../08-插件工作流/04-Codex插件入口与工作流.md) |
| Custom agent | 自定义 agent | 用户定义的 agent 角色，有自己的指令和设置。 | 桌面端、CLI | [Codex Subagents 怎么用](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md) |
| Hook | Hook（钩子） | 匹配到 Codex 事件（如调用工具、请求权限、一轮结束）时运行的生命周期处理程序。 | 桌面端、CLI、IDE | [Codex Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md) |
| Hook event | Hook 事件 | 可以运行已配置 Hook 处理程序的生命周期节点。 | 桌面端、CLI、IDE | [Codex Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md) |
| MCP | MCP（模型上下文协议） | Model Context Protocol，把 Codex 接到外部工具和上下文的标准。 | 桌面端、CLI、IDE | [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) |
| MCP resource | MCP 资源 | MCP 服务器暴露、供 Codex 读取的上下文。 | 桌面端、CLI、IDE | [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) |
| MCP server | MCP 服务器 | 通过 MCP 暴露的外部工具或上下文提供方。 | 桌面端、CLI、IDE | [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) |
| MCP tool | MCP 工具 | MCP 服务器暴露、Codex 在任务中可以调用的操作。 | 桌面端、CLI、IDE | [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) |
| Plugin | 插件 | 可安装的能力包，包含 Skill、连接器和工具等，通过 ChatGPT 和 Codex 共用的目录分发。 | Desktop app (ChatGPT Work、Codex)、网页（Work）、CLI | [Codex 插件入口怎么用](../08-插件工作流/04-Codex插件入口与工作流.md) |
| Plugin manifest | 插件清单 | 标识插件的元数据文件，指向打包的 Skill、连接器映射、MCP 服务器、Hook 和其他元数据。 | 插件开发 | [Codex 插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md) |
| Progressive disclosure | 渐进式加载 | 只在需要时才加载 Skill 的详细内容，以节省上下文。 | 桌面端、网页（Work）、CLI、IDE | [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) |
| Skill | Skill（技能） | 可复用的工作流包，包含指令，以及可选的脚本或参考资料。 | 桌面端、网页（Work）、CLI、IDE | [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) |
| Skill invocation | Skill 调用 | 显式或隐式地启用一个 Skill。 | 桌面端、网页（Work）、CLI、IDE | [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) |
| STDIO MCP server | STDIO MCP 服务器 | 由配置的命令和参数在本地以进程方式启动的 MCP 服务器。 | CLI、IDE | [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md) |
| Streamable HTTP MCP server | Streamable HTTP MCP 服务器 | 通过 HTTP 访问的 MCP 服务器，可选 Bearer token 或 OAuth 认证。 | CLI、IDE | [Codex MCP 排障](../09-MCP与外部工具/03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md) |
| Subagent | 子代理（Subagent） | 被派生出来处理任务一部分的专门子 agent。 | 桌面端、CLI | [Codex Subagents 怎么用](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md) |
| Subagent workflow | 子代理工作流 | Codex 并行运行多个被委派的 agent 并汇总结果的工作流。 | 桌面端、CLI | [Codex Subagents 怎么用](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md) |

## 6. Git、代码审查与 Worktree（12 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| Codex-managed worktree | Codex 管理的 worktree | Codex 为某个对话创建并管理的临时 worktree。 | 桌面端 | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Diff | Diff（差异） | 供查看、评论、暂存或撤销的一组 Git 文件改动。 | 桌面端、Git、审查 | [Codex 如何读懂 Git，status、diff、log 与 blame](../05-Git协作与代码审查/02-Codex如何读懂Git-status-diff-log与blame.md) |
| Environment (local) | 本地环境 | 桌面端的配置，告诉 Codex 怎样为一个项目准备 worktree。 | 桌面端、Worktree | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Git worktree | Git worktree | 同一仓库的第二个检出目录，用于并行处理不同分支。 | 桌面端、Git | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Handoff | 交接（Handoff） | 把一个对话和它的工作在 Local 与 Worktree 之间来回移动。 | 桌面端 | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Hunk | Hunk（改动块） | Diff 里一段连续的改动，可以单独暂存、取消暂存或撤销。 | 桌面端、Git、审查 | [Codex 如何读懂 Git，status、diff、log 与 blame](../05-Git协作与代码审查/02-Codex如何读懂Git-status-diff-log与blame.md) |
| Inline comment | 行内评论 | 附在 Diff 某一行上的反馈。 | 桌面端 | [如何做一次高质量 Code Review](../05-Git协作与代码审查/06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md) |
| Local | Local 模式 | Codex 直接在用户电脑上工作的模式。 | 桌面端、CLI、IDE | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Pull request review | PR 审查 | Codex 审查 PR 里的改动或反馈。 | 桌面端、CLI、GitHub | [如何做一次高质量 Code Review](../05-Git协作与代码审查/06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md) |
| Review pane | 审查面板 | 桌面端里查看 Diff、评论和 Git 改动的视图。 | 桌面端 | [如何做一次高质量 Code Review](../05-Git协作与代码审查/06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md) |
| Setup script | 初始化脚本 | agent 开始工作前运行、用来安装依赖或准备工具的脚本。 | 桌面端 worktree | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |
| Worktree | Worktree 模式 | Codex 把改动隔离在单独 Git worktree 里的模式。 | 桌面端 | [Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md) |

## 7. 自动化与定时任务（11 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| `codex exec` | codex exec | 以非交互方式从脚本或 CI 运行 Codex 的 CLI 命令。 | CLI | [Codex CLI 命令速查](./01-Codex-CLI命令速查-子命令与启动参数.md) |
| Ephemeral session | 临时会话 | 运行结束后不保存会话状态的非交互运行。 | CLI | [Codex CLI 命令速查](./01-Codex-CLI命令速查-子命令与启动参数.md) |
| Finding | 发现（Finding） | 定时任务找出的值得注意的结果或问题。 | 桌面端 | [Codex 定时任务（Scheduled tasks）怎么用](../12-官方工具与集成/06-Codex-Automations定时任务.md) |
| Heartbeat | 心跳任务 | 让 ChatGPT 定期回到同一个对话的周期性定时任务。 | 桌面端 | [Codex 自动化与 CI](../11-自动化与高级工作流/07-Codex自动化与定时任务-从手动流程到稳定执行.md) |
| Non-interactive mode | 非交互模式 | 从脚本或 CI 运行 Codex 的 CLI 模式。 | CLI | [Codex CLI 命令速查](./01-Codex-CLI命令速查-子命令与启动参数.md) |
| Output schema | 输出结构（JSON Schema） | 传给 codex exec 的 JSON Schema，用来约束最终回复的格式。 | CLI | — |
| Schedule | 调度规则 | 定时任务的时间规则。 | 桌面端 | [Codex 定时任务（Scheduled tasks）怎么用](../12-官方工具与集成/06-Codex-Automations定时任务.md) |
| Scheduled run | 定时运行 | 定时任务的一次执行，包括状态和产生的发现。 | 桌面端、网页 | [Codex 定时任务（Scheduled tasks）怎么用](../12-官方工具与集成/06-Codex-Automations定时任务.md) |
| Scheduled task | 定时任务 | ChatGPT 在未来某个时间或按周期运行的提示，有自己的设置和运行历史。 | 桌面端、网页 | [Codex 定时任务（Scheduled tasks）怎么用](../12-官方工具与集成/06-Codex-Automations定时任务.md) |
| Scheduled task in a chat | 对话内定时任务 | 使用某个已有对话的上下文，并把每次运行结果发回该对话的定时任务。 | 桌面端、网页 | [Codex 自动化与 CI](../11-自动化与高级工作流/07-Codex自动化与定时任务-从手动流程到稳定执行.md) |
| Standalone scheduled task | 独立定时任务 | 每次运行都新开一个对话、并在 Triage 里报告发现的定时任务。 | 桌面端、网页 | [Codex 自动化与 CI](../11-自动化与高级工作流/07-Codex自动化与定时任务-从手动流程到稳定执行.md) |

## 8. 云端、远程与开发接口（12 个）

| 英文术语 | 中文叫法 | 意思 | 适用 | 站内教程 |
|---|---|---|---|---|
| Cloud chat | 云端对话 | 在云端环境里远程运行的 Codex 对话。 | 云端 | [Codex Cloud 云端环境配置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| Cloud environment | 云端环境 | Codex Cloud 任务可复用的仓库、依赖、工具和访问设置。 | 云端 | [Codex Cloud 云端环境配置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| Codex app-server | Codex app-server | 本地 JSON-RPC 服务，用来在自定义客户端里嵌入 Codex 的线程、轮次、审批、历史和事件流。 | 桌面端、IDE、SDK | — |
| Codex Cloud | Codex 云端 | 在云端运行的编程任务，有独立的工作区、仓库和工具。 | 桌面端、IDE、网页 | [Codex Cloud 云端环境配置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| Codex SDK | Codex SDK | 用程序构建基于 Codex 的工作流或集成的接口。 | SDK | [Codex SDK 入门](../12-官方工具与集成/17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md) |
| Connected host | 已连接主机 | 通过远程连接打开对话时，提供文件、工具和 shell 的电脑或开发环境。 | 桌面端、手机 | [Codex 远程连接](../12-官方工具与集成/01-Codex远程控制另一台Mac.md) |
| Domain allowlist | 域名白名单 | Codex Cloud 环境网络策略允许访问的域名集合。 | 云端 | [Codex Cloud 云端环境配置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| Network secret | 网络密钥 | 给特定 HTTPS 服务用的凭据。程序拿到的是占位符，代理在访问允许的目标时替换成真实凭据。 | 云端 | [Codex Cloud 云端环境配置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| Remote connection | 远程连接 | 通过一台已连接的主机，在另一台设备上访问 ChatGPT 或 Codex 对话的连接。 | 桌面端、手机 | [Codex 移动端远程协作](../12-官方工具与集成/07-Codex移动端远程协作.md) |
| Sandbox preset | 沙箱预设 | SDK 里常用沙箱策略的简写，比如只读、工作区可写或完全访问。 | SDK | [Codex SDK 入门](../12-官方工具与集成/17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md) |
| Thread | 线程（thread） | Codex app-server API 里的技术对象，包含多个轮次和保存的对话历史。 | app-server、SDK | [Codex SDK 入门](../12-官方工具与集成/17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md) |
| Thread fork | 线程分叉 | 从已有线程的保存历史分出来的新线程。 | app-server、SDK | [Codex SDK 入门](../12-官方工具与集成/17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md) |

## 使用建议

- 读英文文档时把这页开在旁边，遇到词先查「中文叫法」，再看「意思」。
- 「适用」一列说明这个词出现在哪些入口，比如只写「企业」的词（requirements.toml、MDM、RBAC 等）普通个人用户一般碰不到。
- 本站教程标题里尽量沿用这里的中文叫法；同一个词在界面上显示英文时，教程里会同时给出英文原文。

## 延伸阅读

- [Codex 权限、沙箱与审批：什么时候放行，什么时候收紧](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [Codex config.toml 常用字段与环境变量速查](./02-Codex-config.toml常用字段与环境变量速查.md)
- [Codex CLI 命令速查：子命令与启动参数](./01-Codex-CLI命令速查-子命令与启动参数.md)
