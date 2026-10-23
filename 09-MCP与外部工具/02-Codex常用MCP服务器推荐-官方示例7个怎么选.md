---
id: mcp-servers-recommended
title: Codex 常用 MCP 推荐：官方列出的 7 个 MCP 服务器（Docs、Context7、Playwright、Chrome DevTools、GitHub、Sentry、Figma）怎么选
seo_title: Codex 常用 MCP 推荐：官方示例 7 个服务器怎么选与怎么装
description: Codex 官方 MCP 文档列出的 7 个示例服务器怎么选：Docs 与 Context7 查文档，Playwright 与 Chrome DevTools 控浏览器，GitHub、Sentry、Figma 做协作与线上排查。附安装命令出处、权限与「别一次装太多」建议。
lede: 官方列了 7 个常用 MCP，不等于要一次全装。先分清 Skill／插件／MCP，再按任务挑一两个。
url: /guides/codex-mcp-servers-recommended
status: draft
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex MCP 推荐, Context7, Playwright MCP, Chrome DevTools MCP, GitHub MCP, Sentry MCP, Figma MCP]
related: [mcp-getting-started, mcp-troubleshooting, serena-codebase-memory-mcp]
faq:
  - q: 官方列的 7 个 MCP 都要装吗？
    a: 不用。官方「Examples of useful MCP servers」只是常见示例。每个启用的 MCP 都会把工具描述塞进会话上下文。我的用法是按当前项目只开 1–2 个，其余 enabled = false 或根本不配。
  - q: Playwright 和 Chrome DevTools 装哪个？
    a: 两者都能控／查浏览器，侧重点不同：Playwright MCP 偏结构化无障碍树自动化；Chrome DevTools MCP 偏 Chrome 调试、网络与性能轨迹。一般二选一，不要两个一起挂满工具。
  - q: Serena 在不在官方清单里？
    a: 不在。Serena 是社区代码智能 MCP，官方 Examples 未列出。需要语义级跳转／重构时再单独评估，见计划中的姊妹篇。
---

# Codex 常用 MCP 推荐：官方列出的 7 个 MCP 服务器（Docs、Context7、Playwright、Chrome DevTools、GitHub、Sentry、Figma）怎么选

> 本文计划路径：[codexguide.io/guides/codex-mcp-servers-recommended](https://codexguide.io/guides/codex-mcp-servers-recommended)

> 核对依据：learn.chatgpt.com／developers.openai.com 的 MCP 扩展文档「Examples of useful MCP servers」、Docs MCP、各服务器官方安装页，以及 Configuration Reference 中的 `mcp_servers.*`。文中「我的用法」是操作建议，不是官方规定。本文**未在本机逐个实测**全部 7 个服务器的安装与登录；安装命令以各官方文档原文为准。

入门篇讲的是怎么配、怎么登录、怎么收紧权限（计划中的姊妹篇《[Codex MCP 入门](/guides/codex-mcp-getting-started)》）。这篇接着讲：**官方示例里那 7 个，该装哪些、各自解决什么问题。**

## 先分清 Skill、插件和 MCP 各管什么

三者经常一起出现，职责不同：

| | 管什么 | 典型形态 |
|---|---|---|
| **Skill** | 可复用的工作流说明（指令、资源、可选脚本） | 本地 `SKILL.md` 或随插件下发；教模型「怎么做」 |
| **插件（Plugin）** | 打包分发：可含 Skill、MCP、浏览器扩展、hooks 等 | ChatGPT／Codex 共用的插件目录；网页侧常靠插件接远程工具 |
| **MCP** | 把外部系统的**工具**接到会话里 | STDIO 本机进程，或 Streamable HTTP URL；可读写远端数据 |

官方 MCP 文档写明：插件可以包装 MCP 连接，也可以附带 Skills。只需要说明文字时用 Skill；需要查文档、控浏览器、管 Issue／设计稿时用 MCP（或带 MCP 的插件）。

配置本身仍落在 `~/.codex/config.toml`（或受信任项目的 `.codex/config.toml`），桌面端／CLI／IDE 共用。细节见《MCP 入门》。

## 官方列出的 7 个 MCP 一览

来源：Codex 扩展文档 [Examples of useful MCP servers](https://learn.chatgpt.com/docs/extend/mcp#examples-of-useful-mcp-servers)。下表「安装／登录」列：**以各官方安装页为准；本文未逐个实测。**

| 服务器 | 官方一句话用途 | 常见接入 | 登录／密钥 | Codex 侧命令出处 |
|---|---|---|---|---|
| OpenAI Docs MCP | 搜索与阅读 OpenAI 开发者文档 | Streamable HTTP | 不需要 | Docs MCP：`codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp` |
| Context7 | 连接较新的开发者文档 | STDIO（官方 Codex 示例） | 可选 API Key（Context7 自述推荐） | Codex MCP 文档：`codex mcp add context7 -- npx -y @upstash/context7-mcp` |
| Playwright | 用 Playwright 控制与检查浏览器 | STDIO（亦可 HTTP） | 一般不需要账号；本机 Node | Playwright MCP：`codex mcp add playwright npx "@playwright/mcp@latest"` |
| Chrome Developer Tools | 控制与检查 Chrome | STDIO | 需本机 Chrome；无第三方账号登录 | Chrome DevTools MCP：`codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` |
| GitHub | 管理 git 之外的 GitHub（如 PR、Issue） | 远程 HTTP 或本地 Docker | PAT／OAuth（视路径） | GitHub 安装指南：远程 `codex mcp add github --url https://api.githubcopilot.com/mcp/ --bearer-token-env-var GITHUB_PAT_TOKEN` |
| Sentry | 访问 Sentry 日志等信息 | Streamable HTTP | OAuth（Sentry 文档：首次连接会授权） | Sentry MCP 端点：`https://mcp.sentry.dev/mcp`（Codex 用 `codex mcp add … --url`；本文未实测 login） |
| Figma Local／Remote | 访问 Figma 设计 | Remote HTTP 或本机桌面服务 | Remote：Figma 账号；Local：桌面 Dev Mode | Figma Remote：`codex mcp add figma --url https://mcp.figma.com/mcp`；Local：`http://127.0.0.1:3845/mcp` |

官方还在 config 示例里给过 Figma 的 Bearer 写法（`bearer_token_env_var = "FIGMA_OAUTH_TOKEN"`）以及本机 `chrome_devtools` 的 HTTP + 工具白名单示例。那是**配置形态示例**，不等于你必须用同一 URL／工具名；以你实际装上的服务器为准。

**我的用法：** 表格当「菜单」而不是「购物车」。先定本周任务（查 OpenAI 文档／跑前端验收／管 PR／对设计稿），再装对应那一行。

## 文档类：OpenAI Docs MCP 和 Context7

### OpenAI Docs MCP

- **URL：** `https://developers.openai.com/mcp`（Streamable HTTP）
- **覆盖：** `developers.openai.com`、`platform.openai.com`、`learn.chatgpt.com`
- **能力：** 只读——搜索与拉取文档；**不会**替你调用 OpenAI API
- **认证：** 不需要

```bash
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
```

或：

```toml
[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"
```

官方建议在 `AGENTS.md` 加偏好片段，提高「主动查 Docs MCP」的概率（无片段时需在提问里显式要求）。完整说明见 [Docs MCP](https://developers.openai.com/learn/docs-mcp)。

### Context7

Codex 官方 MCP 文档把它当作 **STDIO** 示例：

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

需要本机 Node／npx。Context7 上游还提供远程 MCP 与 CLI＋Skills 等路径；在 Codex 里优先跟官方示例走 STDIO，避免和上游其它客户端教程混用。

**我的用法：**

- Docs MCP → OpenAI／ChatGPT／Codex **自家**文档与 API 说明。
- Context7 → **第三方库／框架**的现行文档与示例。
- 两者互补，不是重复安装。

## 浏览器类：Playwright MCP 和 Chrome DevTools MCP 怎么选

两者都在官方 Examples 里，但问题域重叠，**通常选一个**。

### Playwright MCP

- 包：`@playwright/mcp`（Microsoft Playwright）
- 强调：用无障碍树等结构化数据驱动页面，而不是靠截图视觉模型
- Codex 安装（Playwright 文档原文）：

```bash
codex mcp add playwright npx "@playwright/mcp@latest"
```

等价 TOML：

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

要求 Node.js 18+。上游也提到：部分 coding agent 更偏好 CLI＋Skills 以省 token；MCP 仍适合需要持续浏览器状态、反复探查页面结构的场景。详见 [npm @playwright/mcp](https://www.npmjs.com/package/@playwright/mcp)。

### Chrome DevTools MCP

- 包：`chrome-devtools-mcp`
- 强调：在 **Chrome／Chrome for Testing** 上做自动化、调试、性能轨迹等
- Codex 安装（Chrome DevTools 客户端配置原文）：

```bash
codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

需本机 Chrome。上游写明：会把浏览器实例内容暴露给 MCP 客户端；默认有用量统计，可用 `--no-usage-statistics` 等关闭。详见 [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp/)。

### 怎么选（我的用法）

| 更在意… | 更倾向 |
|---|---|
| 多浏览器引擎、无障碍快照、E2E 式操作 | Playwright |
| Chrome 专属调试、网络／控制台／性能分析 | Chrome DevTools |
| 只要「打开页面点几下验收」 | 二选一即可；先装一个跑通再谈第二个 |

Codex 配置参考里用 `enabled_tools`／`disabled_tools`／`default_tools_approval_mode` 收紧浏览器类工具（官方 chrome_devtools 示例即此模式）。浏览器 MCP 能操作页面与本机会话数据，审批建议默认 `prompt` 或更严。

前端到端验收场景，可对照知识库已有文《Codex 做上线前端到端验收》（`/guides/codex-browser-e2e-acceptance`）。

## 协作和线上排查：GitHub、Sentry、Figma

### GitHub MCP Server

官方描述：管理 **git 命令覆盖不到** 的 GitHub 能力（例如 PR、Issue）。

**远程（GitHub Codex 安装指南）：**

```bash
codex mcp add github --url https://api.githubcopilot.com/mcp/ --bearer-token-env-var GITHUB_PAT_TOKEN
```

```toml
[mcp_servers.github]
url = "https://api.githubcopilot.com/mcp/"
bearer_token_env_var = "GITHUB_PAT_TOKEN"
```

PAT 放环境变量，**不要**写进对话或公开仓库。指南建议按最小权限开 scope（如 `repo`，需要时再加 `workflow`／`read:org` 等）。

也可用本地 Docker 镜像 `ghcr.io/github/github-mcp-server`（OAuth 或 `GITHUB_PERSONAL_ACCESS_TOKEN`）。完整步骤见 [Install GitHub MCP Server in OpenAI Codex](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md)。

若你主要靠 GitHub **插件**跑 Issue→PR 工作流，先确认插件是否已带所需 MCP，再决定要不要另加独立 `github` 服务器，避免重复工具撑爆上下文。对照：`/guides/codex-github-issue-pr-workflow`。

### Sentry MCP

官方 Examples 链到 [Sentry MCP](https://docs.sentry.io/product/sentry-mcp/#codex)。要点：

- 基址：`https://mcp.sentry.dev/mcp`
- 可收窄到组织／项目：`…/mcp/{organizationSlug}` 或 `…/mcp/{organizationSlug}/{projectSlug}`
- **所有连接走 OAuth**；首次会触发授权
- 文档给了 Claude／Cursor／VS Code 等示例；「Other clients」可用 HTTP 传输连同一 URL

在 Codex 中可按 HTTP 通用写法添加（**本文未实测**）：

```bash
codex mcp add sentry --url https://mcp.sentry.dev/mcp
# 若界面要求 Authenticate／OAuth：
codex mcp login sentry
```

项目级排查时优先用带 org／project 的 URL，减少无关发现类工具。

### Figma：Remote 与 Local

官方 Examples 写明 **Local 与 Remote** 两条路径。

**Remote（推荐路径之一，Figma 文档）：**

- URL：`https://mcp.figma.com/mcp`
- 不需要 Figma 桌面端；首次用 Figma 账号授权
- Codex CLI：

```bash
codex mcp add figma --url https://mcp.figma.com/mcp
```

Figma 也推荐在 Codex **App** 里装 Figma 插件（含 MCP 与 Skills）。仅 CLI 添加 MCP **不会**自动带上 Figma Skills。详见 [Remote server installation](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)。

**Local（桌面 MCP）：**

- 在 Figma 桌面端 Dev Mode 启用 desktop MCP
- 本机地址：`http://127.0.0.1:3845/mcp`
- 需要桌面端与对应座位／计划；Figma 写明强推 Remote，且 Local **不支持**部分写画布／Send UI 等能力

Codex 扩展文档的 config 示例亦出现过：

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

这是 Bearer／头写法示例；日常也可走 OAuth／插件登录。选一种认证方式，不要把 token 贴进聊天。

## 社区补充：Serena（非官方清单）

**Serena 不在**官方「Examples of useful MCP servers」七项里。它是社区 MCP，面向语义级代码检索、编辑与重构类能力，并通过 MCP 接到包括 Codex 在内的客户端。

若你需要「IDE 式」符号跳转／跨文件重构，可单独评估 Serena，并阅读其官方安装说明（上游强调用 `uv` 安装、**不要**从过时 marketplace 命令装）。本站计划另有姊妹篇《代码智能 MCP：Serena 与 codebase-memory-mcp》（`related: serena-codebase-memory-mcp`）。

**我的用法：** 先把官方七项里与当前任务相关的装稳，再考虑社区 MCP；社区服务器同样适用下文的白名单与安全检查。

## 装多少合适：按项目启用、工具白名单、别撑爆上下文

1. **按项目启用，而不是全局堆满。** 用户级 `~/.codex/config.toml` 适合 Docs 这类通用只读；GitHub／Sentry／Figma／浏览器更适合放进**已信任**项目的 `.codex/config.toml`，或全局配置后对不用的设 `enabled = false`。
2. **用 `enabled_tools`／`disabled_tools` 砍工具面。** `disabled_tools` 在 `enabled_tools` 之后应用。浏览器、GitHub 写操作尤其要收。
3. **审批：** `default_tools_approval_mode` 与单工具 `tools.<name>.approval_mode` 支持 `auto`／`prompt`／`writes`／`approve`。`writes` 会对未标只读的工具提示审批。
4. **超时：** `startup_timeout_sec` 默认 10；`tool_timeout_sec` 默认 60。`npx` 首次拉包偏慢时可加大启动超时。
5. **名字要短。** Docs MCP 文档也提醒：服务器多时，短名字有助于模型选对服务器。

**我的用法：** 同一会话同时开「Docs + 一个任务向 MCP」通常够用。开到 4–5 个还频繁误调工具时，先关一半再排障（计划中的《MCP 排障》）。

## 安装前的安全检查

1. **来源：** 优先官方 Examples 链出的仓库／文档（OpenAI Docs、upstash/context7、Playwright、ChromeDevTools、GitHub、Sentry、Figma）。来路不明的 `npx` 包不要装。
2. **权限范围：** GitHub PAT、Sentry／Figma OAuth 只开当前任务需要的 scope；能项目级收窄（Sentry URL 带 project）就收窄。
3. **密钥放哪：** `bearer_token_env_var`／`env`／系统钥匙串；**不要**写进对话、截图、公开 git。含 `oauth.client_secret` 的 `config.toml` 当机密。
4. **OAuth 只适用于 Streamable HTTP。** STDIO 不要指望 `codex mcp login`（与《MCP 入门》一致）。
5. **浏览器 MCP ≠ 安全边界。** Playwright／Chrome DevTools 上游都提醒：不是安全沙箱；登录态、Cookie、页面内容会对模型可见。
6. **沙箱域名白名单挡不住 MCP。** 收紧靠本节与 `mcp_servers.*` 审批／白名单，不要指望 `features.network_proxy.domains`。
7. **网页 ChatGPT** 不读本地 `~/.codex/config.toml`；网页侧靠插件。本篇主场景是桌面端／CLI／IDE。

## 少踩坑

1. 官方七项是**示例菜单**，不是必装清单。
2. Playwright 与 Chrome DevTools 功能重叠，先装一个。
3. Figma：App 插件路径与纯 CLI `mcp add` 路径能力不同（Skills 是否附带）。
4. GitHub：远程 PAT 与本地 Docker／OAuth 是不同部署，按官方 Codex 安装指南二选一理清。
5. 改完配置要 Restart／新开会话；用 `/mcp` 或 `codex mcp list` 确认。
6. 不要再使用已移除的 `codex mcp-server`。
7. 连不上／没有工具／OAuth 失败 → 计划中的《Codex MCP 排障》。

## 接下来读什么

- 计划中：《Codex MCP 入门》（config.toml、`mcp login`、权限边界）→ `/guides/codex-mcp-getting-started`
- 计划中：《Codex MCP 排障》
- 计划中：《代码智能 MCP：Serena 与 codebase-memory-mcp》
- 上线前端到端验收：`/guides/codex-browser-e2e-acceptance`
- GitHub 插件实战：`/guides/codex-github-issue-pr-workflow`

## 参考资料

- [Model Context Protocol（Examples of useful MCP servers）](https://learn.chatgpt.com/docs/extend/mcp)
- [Docs MCP](https://developers.openai.com/learn/docs-mcp)
- [Configuration Reference（mcp_servers.*）](https://developers.openai.com/codex/config-reference)
- [Context7](https://github.com/upstash/context7)
- [Playwright MCP（npm）](https://www.npmjs.com/package/@playwright/mcp)
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp/)
- [GitHub MCP Server · Codex 安装](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md)
- [Sentry MCP](https://docs.sentry.io/product/sentry-mcp/)
- [Figma MCP Remote](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)／[Local](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/)
- [Build skills](https://developers.openai.com/codex/skills)／[Plugins](https://developers.openai.com/codex/plugins)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
