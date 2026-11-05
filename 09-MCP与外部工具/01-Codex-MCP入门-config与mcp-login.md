---
id: mcp-getting-started
title: Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界
seo_title: Codex MCP 入门：config.toml、mcp login、Docs MCP 与工具权限
description: 从零用 Codex 接入 MCP：弄清 STDIO 与 Streamable HTTP，用 config.toml 或 codex mcp add 配置，用 mcp login／Authenticate 完成 OAuth，实操 Docs MCP 与 Context7，并划清工具白名单与审批边界。
lede: MCP 是让 Codex 调用外部工具的协议。先选对传输方式，再配好登录与权限，别一上来就装一堆服务器。
url: /guides/codex-mcp-getting-started
status: published
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 1
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex MCP, mcp login, config.toml, Docs MCP, OAuth, Streamable HTTP, STDIO]
related: [mcp-servers-recommended, mcp-troubleshooting, serena-codebase-memory-mcp]
faq:
  - q: 桌面端、CLI、IDE 要分别配一遍 MCP 吗？
    a: 一般不用。同一台机器上的 ChatGPT 桌面端、Codex CLI 与 IDE 扩展共用 ~/.codex/config.toml（以及受信任项目下的项目级 .codex/config.toml）。配一次，三个入口都能用。
  - q: Docs MCP 需要登录或 API Key 吗？
    a: 不需要。官方 Docs MCP（https://developers.openai.com/mcp）是只读文档服务，不替你调用 OpenAI API，也不要求 OAuth。配好后重启会话，在对话里明确让它查文档即可。
  - q: codex mcp-server 还能用吗？
    a: 不能。官方已移除 codex mcp-server 与独立的 codex-mcp-server 二进制。要把外部工具接进 Codex，用 codex mcp 管理外部 MCP；若要做深度集成，看 Codex app server，它不是 MCP。
---

# Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界

> 本文在线版：[codexguide.io/guides/codex-mcp-getting-started](https://codexguide.io/guides/codex-mcp-getting-started)

> 核对依据：learn.chatgpt.com／developers.openai.com 的 MCP 扩展文档、Docs MCP、Configuration Reference，以及 Codex CLI 0.161.0 changelog（`/mcp login`）。文中「我的用法」是操作建议，不是官方规定。

Codex 本身能读项目、改文件、跑命令。但很多信息在别处：最新官方文档、设计稿、工单系统、浏览器里的页面。**MCP（Model Context Protocol）** 就是让 Codex 按统一方式调用这些外部工具的协议。

这篇是 09 栏目的入门文：只讲**怎么接上、怎么登录、怎么收紧权限**。常用服务器怎么选，见计划中的姊妹篇《Codex 常用 MCP 服务器推荐》；连不上／没有工具／OAuth 失败，见《Codex MCP 排障》。

## MCP 在 Codex 里解决什么（以及不解决什么）

**解决的：**

- 给会话挂上外部工具（查文档、控浏览器、读设计稿、管 GitHub Issue／PR 等）。
- 用同一份配置，在桌面端、CLI、IDE 之间切换，不用反复重配。
- 对需要登录的远程服务走 OAuth 或 Bearer Token，而不是把密钥贴进对话。

**不解决的：**

- 不会自动替你判断「这个第三方服务器值不值得信」。接上就等于把工具能力交给模型调用，恶意服务器可能外泄上下文里的敏感信息。
- 不是把 Codex **自己**托管成 MCP server。`codex mcp-server` 已移除；对外集成请连**外部** MCP，或改用 Codex app server（另一套协议，不是 MCP 替代品）。
- 沙箱里的域名白名单**管不到** MCP／Apps／网页搜索。收紧 MCP 要靠本文后面的工具白名单与审批，不要指望 `features.network_proxy.domains` 挡住 MCP。

**我的用法：** 先只装一个只读、官方或你信任的服务器（例如 Docs MCP），跑通「能看见工具 → 能答对问题」，再加第二个。不要一次塞七八个。

## 两种接入：STDIO 与 Streamable HTTP

| 对比项 | STDIO | Streamable HTTP |
|---|---|---|
| 怎么跑 | 本机起一个进程（常见是 `npx …`） | 访问一个 URL |
| 典型配置 | `command` + `args`（可选 `env`／`cwd`） | `url`（可选认证与头） |
| 适合 | 本地包装器、要读本机环境变量的工具 | 官方托管服务、团队远程 MCP |
| 登录 | 一般靠环境变量／本地凭证 | Bearer Token、OAuth、`auth = "chatgpt"`（受信第一方）等 |
| OAuth | **不支持** `codex mcp login` | **支持**（仅 Streamable HTTP） |

官方文档写明：`codex mcp login` **只适用于 Streamable HTTP 服务器**。STDIO 服务器若需要密钥，用 `env`／`env_vars` 或服务器自己的本地登录流程，不要指望 `mcp login`。

## 配置放哪：全局与项目级

默认写在用户级：

```text
~/.codex/config.toml
```

也可以在**已信任**的项目里放：

```text
.codex/config.toml
```

要点：

1. **桌面端、CLI、IDE 共用**同一份有效配置（同一 Codex 主机）。
2. **项目级配置只在信任该项目时才会加载**。未信任项目会跳过项目级 `.codex/`（含本地 config、hooks、rules）。
3. 每个服务器是一张表：`[mcp_servers.<名字>]`。名字要短、好认，方便模型选对服务器。

桌面端也可以走界面：Settings → MCP servers → Add server → 选 STDIO 或 Streamable HTTP → Save → Restart。IDE 扩展类似（齿轮 → MCP servers → Restart extension）。CLI 更适合脚本化与复制粘贴。

## CLI 与 TUI：add／list／login、/mcp

### 常用命令

```bash
# 查看已配置服务器
codex mcp list

# 看全部子命令
codex mcp --help

# 添加 STDIO 服务器（官方 Context7 示例）
codex mcp add context7 -- npx -y @upstash/context7-mcp

# 添加 Streamable HTTP（官方 Docs MCP）
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp

# 需要 OAuth 的 HTTP 服务器：单独登录
codex mcp login <server-name>
```

`codex mcp add … --env KEY=VALUE -- <命令>` 可在添加时写入环境变量。需要预注册 OAuth client 时，可用 `--oauth-client-id`（机密客户端再加 `--oauth-client-secret`）；密钥会进 `config.toml`，**不要提交到 Git**。

### TUI 斜杠命令

- `/mcp`：查看当前会话里活跃的 MCP 服务器。
- `/mcp login <server>`：在正在跑的终端会话里对指定服务器做 OAuth（Codex CLI **0.161.0** 起）。

桌面端对需要 OAuth 的条目点 **Authenticate**；作曲区也可输入 `/mcp` 查看已连接服务器。

改完配置后，通常要 **Restart** 桌面端／扩展，或新开 CLI 会话，工具列表才会刷新。

## 实操 A：接入 OpenAI Docs MCP

官方托管的文档 MCP，覆盖 `developers.openai.com`、`platform.openai.com`、`learn.chatgpt.com`。

- **URL：** `https://developers.openai.com/mcp`（Streamable HTTP）
- **能力：** 只读——搜索与拉取文档内容；**不会**替你调用 OpenAI API
- **认证：** 不需要

### 用 CLI（推荐）

```bash
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
```

### 或手写 config.toml

```toml
[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"
```

### 让它「真的会被用上」

配上不等于每句都会查。官方建议在项目 `AGENTS.md` 加一段偏好（可按团队改写）：

```text
Always use the OpenAI developer documentation MCP server if you need to work with the OpenAI API, plugins, ChatGPT, Codex,… without me having to explicitly ask.
```

没有这段时，提问里写清楚：「用 Docs MCP 查 Responses API 的 tools 字段，并给出文档链接。」

**我的用法：** 新开一轮短会话，问一句带版本感的问题（例如某配置键的默认值），看它是否真的调了文档工具、答案是否带来源链接。若模型空口答，提醒它「先 MCP 再总结」。

## 实操 B：接入 Context7（官方文档示例）

Context7 是官方 MCP 文档里的 STDIO 示例：用本地 `npx` 拉开发者文档类工具。

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

等价配置：

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

需要把本机环境变量转给该进程时，用 `env`／`env_vars`（详见配置参考）。机器上要有可用的 Node／npx；第一次跑会下载包，`startup_timeout_sec` 默认 10 秒，偏慢时可酌情加大。

**我的用法：** Docs MCP 解决「OpenAI 自家文档」；Context7 更偏「第三方库／框架的现行文档」。两者目的不同，不要当成重复安装。

## OAuth：什么时候要 login，失败先查什么

### 何时需要

仅当服务器是 **Streamable HTTP**，且在配置好 bearer／头之后仍需要 OAuth（或界面显示要 Authenticate）时：

```bash
codex mcp login <server-name>
```

可选：

- `--no-browser`：打印授权 URL，粘贴回调
- `--scopes a,b`：显式 scope
- `--oauth-client-registration auto|cimd|dcr`：仅本次登录的客户端注册策略

登录成功会提示类似：`Successfully logged in to MCP server '<name>'.`

若配置了 `auth = "chatgpt"`，受信第一方可先用当前 ChatGPT 会话，再回退到已存 OAuth。企业托管的 MCP 授权可能要求在 Codex 里用账号登录，而不是本地 `mcp login`——以客户端报错文案为准。

### 回调地址（远端／Devbox）

默认本地回调大致是 `http://127.0.0.1/callback`（端口由监听器决定；官方对 loopback 有特殊规则）。在远程开发机或需要固定入口时，可在用户级 `config.toml` 设置：

```toml
mcp_oauth_callback_port = 5555
mcp_oauth_callback_url = "https://devbox.example.internal/callback"
```

也可用单服务器的 `[mcp_servers.<name>.oauth]`（`client_id`、`callback_url`、`callback_port`、`client_secret`）。**务必把提供商后台登记的回调，与 `codex mcp add`／登录时显示的完整回调写成一致。**

### 我的用法：OAuth 不通时的短顺序

1. 确认是 HTTP 服务器，不是 STDIO。
2. `codex mcp list` 看名字是否写对；`enabled` 是否为 `false`。
3. 浏览器能否打开授权页；本机防火墙是否拦了回调端口。
4. 远端环境是否漏配 `mcp_oauth_callback_url`／端口。
5. 仍失败：把脱敏后的报错留给姊妹篇《MCP 排障》，不要把 `client_secret` 贴进聊天或 issue。

## 权限边界：白名单、审批、超时

接上 MCP 之后，真正决定风险的是**哪些工具可见、调用前要不要点同意**。

常用字段（写在 `[mcp_servers.<name>]` 下）：

| 字段 | 作用 | 默认／注意 |
|---|---|---|
| `enabled` | 临时关掉而不删配置 | `false` 即禁用 |
| `required` | 启用不了则启动／恢复失败 | 关键路径慎开 |
| `enabled_tools` | 只暴露这些工具 | 白名单 |
| `disabled_tools` | 在白名单之后再剔除 | 后应用 |
| `default_tools_approval_mode` | 该服务器工具的默认审批 | `auto`／`prompt`／`writes`／`approve` |
| `tools.<tool>.approval_mode` | 单工具覆盖 | 同上 |
| `tools.<tool>.output_token_limit` | 单次工具输出 token 预算 | 防超大回灌 |
| `startup_timeout_sec` | 启动超时 | 默认 10 |
| `tool_timeout_sec` | 单次工具超时 | 默认 60 |

`writes` 模式：对**未**标成只读的工具会提示审批。另有顶层 `mcp_optional_startup_grace_ms`（默认 1000）：建初始工具目录时，对可选服务器额外等待多久；设为 `0` 则改等各自的 `startup_timeout_sec`。`required` 服务器仍走自己的启动超时。

插件自带的 MCP 不在用户配置里写 `command`／`url`，但可在 `plugins."<plugin@marketplace>".mcp_servers.<name>` 下改 `enabled`、白名单与审批。

配置示例（收紧某个本地浏览器类 MCP）：

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
disabled_tools = ["screenshot"] # 在 enabled_tools 之后再禁
default_tools_approval_mode = "prompt"
startup_timeout_sec = 20
tool_timeout_sec = 45

[mcp_servers.chrome_devtools.tools.open]
approval_mode = "approve"
output_token_limit = 30000
```

**与主机沙箱的关系：** 沙箱／permission profile 主要约束**命令执行与本机文件系统／代理**。MCP 工具走的是另一条通道；官方写明网络代理域名规则**不**限制 web search、Apps 或 MCP。要控 MCP，用本节字段，并配合你对第三方服务器的信任判断。

**我的用法：**

1. 只读文档类（Docs MCP）：可保持较松审批，但仍建议名字短、专机专用。
2. 能改远端数据、发消息、操作仓库的：默认 `prompt` 或 `approve`，并用 `enabled_tools` 砍到最小。
3. 不用的服务器设 `enabled = false`，而不是留着「万一用得上」——每个 MCP 都会抬高会话上下文（用量文也提醒过这一点）。

## 少踩坑

1. **先分清 STDIO／HTTP**，再决定要不要 `mcp login`。
2. **改完要重启／新开会话**，否则还在看旧工具列表。
3. **项目级 `.codex/config.toml` 只对信任项目生效**；同事 clone 下来不等于自动信任。
4. **不要再教 `codex mcp-server`**——已删除；接外部工具用 `codex mcp`。
5. **密钥进 config／环境变量，不进对话、不进公开仓库**；含 `oauth.client_secret` 的文件当机密。
6. **ChatGPT 网页端不走本地 `~/.codex/config.toml`**；网页侧靠插件／托管连接。本地 Codex 客户端才是这篇的主场景。
7. **Local computer access with Work Cloud**：本地执行与云容器策略不同，本地 MCP 未必在云端可用；企业 hooks／托管 `mcp_servers` 要求另查工作区策略。

## 接下来读什么

- 计划中：《Codex 常用 MCP 服务器推荐》（官方示例 7 个怎么选）→ `09-MCP与外部工具/02-…`
- 计划中：《Codex MCP 排障》（连不上、没有工具、OAuth 失败）→ `09-MCP与外部工具/03-…`
- 计划中：《代码智能 MCP：Serena 与 codebase-memory-mcp》→ `09-MCP与外部工具/04-…`
- 权限与沙箱总览：知识库 `02-核心概念与任务方法/06-权限沙箱与审批-…`（网站 `/guides/codex-quan-xian-sha-xiang-yu-shen-pi`）
- 沙箱与主机风险：`10-配置模型与权限安全/05-Codex沙箱与主机权限风险.md`

## 参考资料

- [Model Context Protocol（Codex 扩展 MCP）](https://learn.chatgpt.com/docs/extend/mcp)
- [Docs MCP](https://developers.openai.com/learn/docs-mcp)
- [Configuration Reference（mcp_servers.*）](https://developers.openai.com/codex/config-reference)
- [Codex MCP server removal](https://learn.chatgpt.com/docs/mcp-server)
- [Codex CLI 0.161.0（`/mcp login`）](https://github.com/openai/codex/releases/tag/rust-v0.161.0)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
