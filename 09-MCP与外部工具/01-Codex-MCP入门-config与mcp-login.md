---
id: mcp-getting-started
title: Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界，补上 OAuth 客户端注册、远程环境、插件自带 MCP 和服务器 instructions
seo_title: Codex MCP 入门：OAuth 客户端、远程环境与插件自带服务器
description: 从零用 Codex 接入 MCP：分清 STDIO 与 Streamable HTTP，用 config.toml 或 codex mcp add 配置并完成 OAuth 登录，实操 Docs MCP。已对照最新官方文档，补上 OAuth 客户端注册、远程环境、插件自带服务器和权限边界。
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
date_modified: 2026-11-21
verified_on: 2026-11-21
tested_cli_version: 0.171.0
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex MCP, codex mcp add --oauth-client-id, environment_id, 插件自带 MCP 服务器, MCP instructions]
related: [mcp-servers-recommended, mcp-troubleshooting, codex-cli-0-170-voice-mcp-reconnect, codex-sandbox-command, serena-codebase-memory-mcp]
faq:
  - q: 桌面端、CLI、IDE 要分别配一遍 MCP 吗？
    a: 一般不用。同一台机器上的 ChatGPT 桌面端、Codex CLI 与 IDE 扩展共用 ~/.codex/config.toml（以及受信任项目下的项目级 .codex/config.toml）。配一次，三个入口都能用。
  - q: Docs MCP 需要登录或 API Key 吗？
    a: 不需要。官方 Docs MCP（https://developers.openai.com/mcp）是只读文档服务，不替你调用 OpenAI API，也不要求 OAuth。配好后重启会话，在对话里明确让它查文档即可。
  - q: codex mcp-server 还能用吗？
    a: 不能。官方已移除 codex mcp-server 与独立的 codex-mcp-server 二进制。要把外部工具接进 Codex，用 codex mcp 管理外部 MCP；若要做深度集成，看 Codex app server，它不是 MCP。
---

# Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界，补上 OAuth 客户端注册、远程环境、插件自带 MCP 和服务器 instructions

> 本文在线版：[codexguide.io/guides/codex-mcp-getting-started](https://codexguide.io/guides/codex-mcp-getting-started)

> 核对依据：2026-11-21 打开的 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)。命令行对照 Codex CLI 0.171.0 的 `codex mcp --help`、`codex mcp add --help` 和 `codex mcp login --help`，没有走完一次 OAuth，没有添加真实服务器。0.169 的未信任目录行为沿用 [Codex CLI 0.169.0](../12-官方工具与集成/25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md) 里已经做过的 `codex exec` 试验，本文没有重跑。0.170、0.171 的 MCP 条目来自对应 Release 和当天的 [更新日志](https://learn.chatgpt.com/codex/changelog)。文中「我的用法」是操作建议，不是官方规定。Docs MCP 与 Context7 的步骤仍是原文里的官方示例，2026-11-21 没有重新执行 `npx`。

Codex 本身能读项目、改文件、跑命令。但很多信息在别处：最新官方文档、设计稿、工单系统、浏览器里的页面。**MCP（Model Context Protocol）** 就是让 Codex 按统一方式调用这些外部工具的协议。

这篇是 09 栏目的入门文：只讲**怎么接上、怎么登录、怎么收紧权限**。常用服务器怎么选，见 [Codex 常用 MCP 推荐](./02-Codex常用MCP服务器推荐-官方示例7个怎么选.md)。连不上、没有工具或 OAuth 失败，见 [Codex MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)。

## MCP 在 Codex 里解决什么（以及不解决什么）

**解决的：**

- 给会话挂上外部工具（查文档、控浏览器、读设计稿、管 GitHub Issue／PR 等）。
- 用同一份配置，在桌面端、CLI、IDE 之间切换，不用反复重配。
- 对需要登录的远程服务走 OAuth 或 Bearer Token，而不是把密钥贴进对话。

**不解决的：**

- 不会自动替你判断「这个第三方服务器值不值得信」。接上就等于把工具能力交给模型调用，恶意服务器可能外泄上下文里的敏感信息。
- 不是把 Codex **自己**托管成 MCP server。`codex mcp-server` 已移除；对外集成请连**外部** MCP，或改用 Codex app server（另一套协议，不是 MCP 替代品）。
- 沙箱和网络代理**管不到** MCP。Permissions 页写明，代理只过滤沙箱里本地命令的流量，不把域名规则用到 MCP、网页搜索、Apps、浏览器或 Codex 自己的请求上。收紧 MCP 用本文后面的工具白名单和审批。给某个 stdio 进程套上 `codex sandbox`，是另一件事，见 [sandbox 命令](../10-配置模型与权限安全/31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)。

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
3. **0.169.0 起，`codex exec` 在未信任目录默认不加载项目配置和 MCP 服务器**，即使加了 `--sandbox workspace-write`。要用 `codex exec --trust` 或 `codex review --trust` 才会保存信任。站内那次试验见 [Codex CLI 0.169.0](../12-官方工具与集成/25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。帮助里的警告还写明：这包括沙箱外的 MCP 命令；已经明确标成不信任的项目，要先改信任设置。后一句本文没有复测。
4. 每个服务器是一张表：`[mcp_servers.<名字>]`。名字要短、好认，方便模型选对服务器。

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

- `/mcp`：查看当前会话里活跃的 MCP 服务器。`/mcp verbose` 带上更细的服务器诊断。
- `/mcp login <server>`：在正在跑的终端会话里对指定服务器做 OAuth（Codex CLI **0.161.0** 起）。

0.171.0 的 `codex mcp` 子命令是 `list`、`get`、`add`、`remove`、`login`、`logout`。`codex mcp add --help` 里有 `--oauth-client-id`、`--oauth-client-secret` 和 `--oauth-client-registration`（`auto`、`cimd`、`dcr`）。`codex mcp login --help` 里有 `--no-browser`、`--scopes` 和同样的 `--oauth-client-registration`。帮助里**没有** `environment_id` 这个参数；它是 `config.toml` 字段，见下文。

0.171.0 的 Release 写：打开 `tui_extensions_statusline` 之后，可以用 `/statusline` 选择和编写自定义 MCP 状态栏。2026-11-21 在空配置上，`codex features list` 里这一项是 `experimental`，有效状态 `false`。同一天的 [Developer commands](https://learn.chatgpt.com/docs/developer-commands) 对 `/statusline` 列的是模型、上下文、用量、Git 分支等内置项，正文没有写 MCP 状态栏。所以：功能在 Release 里，并且默认关着；公开的斜杠命令页还没有把 MCP 那一项写进步骤。本文没有打开 TUI，没有看到这个选择器。

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

若配置了 `auth = "chatgpt"`，受信第一方可先用当前 ChatGPT 会话，再回退到已存 OAuth。0.171.0 修了企业 MCP 登录：有的身份提供者只发 ID token、不发 refresh token（#62129）。企业托管的授权仍可能要求在 Codex 里用账号登录，而不是本地 `mcp login`。以客户端报错文案为准。

### 客户端要预先注册时

授权服务器要求预注册的 OAuth 客户端时，官方写法是在添加时带上 client id。机密客户端再从环境变量读 secret，不要把 secret 写进仓库或示例：

```bash
codex mcp add example --url https://mcp.example.com --oauth-client-id my-client
codex mcp add example --url https://mcp.example.com --oauth-client-id my-client --oauth-client-secret "$MCP_CLIENT_SECRET"
```

0.171.0 的 `codex mcp add --help` 里这两个参数都在。官方写明：secret 不能是空的；Codex 会把它存成 `config.toml` 里的 `mcp_servers.example.oauth.client_secret`。这个文件当机密，不要提交。

已经配了 client id 时，Codex 跳过自动注册。没有配时，默认策略是 `auto`：授权服务器声明支持 Client ID Metadata Documents（CIMD），并且 token 端点接受 `none`、回调又是支持的 loopback 地址时，选用 CIMD；否则在可用时用 Dynamic Client Registration（DCR）。只对这一次登录指定方式：

```bash
codex mcp login <server-name> --oauth-client-registration cimd
codex mcp login <server-name> --oauth-client-registration dcr
```

`codex mcp login --help` 的取值就是 `auto`、`cimd`、`dcr`。官方写明这个选择只作用于本次登录，不写进 `config.toml`。

CIMD 在没有 issuer 绑定响应时，CLI 使用按服务器区分的元数据文档 `https://chatgpt.com/oauth/codex/<callback_id>/client.json`。授权服务器若声明 `authorization_response_iss_parameter_supported: true`、元数据里有合法 `issuer`，并且授权响应里带上匹配的 `iss`，CLI 改用稳定的 `https://chatgpt.com/oauth/codex/client.json`。自定义回调主机、路径或查询参数，需要 DCR 或已经配好的 client id。

### 回调地址（远端／Devbox）

把授权服务器里登记的回调，写成和 `codex mcp add` 打印出来的**完全一致**。发行者支持且提供了元数据 `issuer` 时，CLI 可以打印：

```text
OAuth callback URL: http://127.0.0.1/callback
```

新加的预注册客户端，只有在授权服务器声明 `authorization_response_iss_parameter_supported: true` 并给出 `issuer` 时，才使用这个稳定回调。没有声明时，Codex 会在后面加上按服务器算出来的 callback id，例如 `http://127.0.0.1/callback/XuuuHAzzHOni`。已经存在、又没有保存回调的客户端，继续用带 callback id 的地址。

官方用一张表区分「配置了 `callback_url` 没有 `client_id`」「两者都有」「只有 `client_id`」以及发行者支不支持。这里只记会改行为的几条：

- 配了 `client_id` 和 `callback_url`，并且发行者支持：复用配置里的回调，授权响应必须带上匹配的 `iss`。
- 配了 `client_id`，但 `callback_url` 没有带上正确的 callback id，发行者又不支持：配置里的回调被忽略。Codex 改用 `mcp_oauth_callback_url`，没设则用 `http://127.0.0.1/callback`，再附上 callback id。已经存下来的 `callback_url` 不会被改写。
- `iss` 对不上一定拒绝。发行者声明支持、响应里却没有 `iss`，也拒绝。这两种都不会拿授权码去交换，也不会再换一个回调。

在远程开发机或需要固定入口时，可在用户级 `config.toml` 设置：

```toml
mcp_oauth_callback_port = 5555
mcp_oauth_callback_url = "https://devbox.example.internal/callback"
```

也可用单服务器的 `[mcp_servers.<name>.oauth]`（`client_id`、`callback_url`、`callback_port`、`client_secret`）。`mcp_oauth_callback_port` 固定全局监听端口；单服务器的 `oauth.callback_port` 可以覆盖它。回调 URL 里自己写的端口**不会**顺便把监听端口设成同一个数。直接的 loopback 回调，用没有端口的 `http://127.0.0.1`，或让 URL 和监听端口写成同一个。经过代理时，外部 URL 的端口可以和本机监听端口不同。本地回调绑在本机接口；非本地回调绑在 `0.0.0.0`。

对没有写端口的 `http://127.0.0.1`，Codex 在展示和保存的 URL 里省略监听端口，授权时再填上当时的端口。这不适用于 `localhost`、IPv6、HTTPS，或 URL 里已经有端口的情况。授权服务器要按 [RFC 8252 第 7.3 节](https://www.rfc-editor.org/rfc/rfc8252#section-7.3) 接受变化的 loopback 端口。

`scopes` 写在 `mcp_servers.<name>.scopes`。单次登录可以用 `codex mcp login <name> --scopes read,write`，0.171.0 的帮助里参数名是 `--scopes <SCOPE,SCOPE>`。两处都没写时，Codex 用服务器初始 `WWW-Authenticate` 里的 scope；那里也没有，再用受保护资源元数据里广告的 scope。空列表 `scopes = []` 仍会让 OAuth 库自己选；库还可能在服务器支持时加上 `offline_access`。

### 我的用法：OAuth 不通时的短顺序

1. 确认是 HTTP 服务器，不是 STDIO。
2. `codex mcp list` 看名字是否写对；`enabled` 是否为 `false`。
3. 浏览器能否打开授权页；本机防火墙是否拦了回调端口。
4. 远端环境是否漏配 `mcp_oauth_callback_url`／端口。
5. 仍失败：把脱敏后的报错留给 [MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)，不要把 `client_secret` 贴进聊天或 issue。

## 远程环境与同名服务器

官方 MCP 页把 `environment_id` 写成 stdio 和 Streamable HTTP 都能用的字段，默认是 `local`。要经过远程执行器，填那个执行器注册的环境 ID。0.171.0 的 `codex mcp add --help` 没有这个参数，所以它目前是配置文件字段，不是这条子命令的旗标。

环境变量也分本地和远程。`env_vars` 可以是名字，或带来源的对象：

```toml
env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]
```

字符串和 `source = "local"` 从 Codex 本机环境读。`source = "remote"` 从远程执行器的环境读，并且要求远程 MCP stdio。`http_headers_helper` 只用于本机环境发出的 HTTP MCP 连接，不用于 stdio，也不用于经远程执行环境发出的连接。

这和 0.170.0 的实验功能不是同一句话。[rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0) 写了同名 MCP 服务器可以跨环境使用（实验性，#60905）。2026-11-21 在 0.171.0、空配置上，`codex features list` 里 `multi_environment_mcp` 是 `under development`，有效状态 `false`。发布说明没有给出这个开关的配置教程，[0.170 一文](../12-官方工具与集成/29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md) 也不写启用命令。本文同样不写。`environment_id` 按上面的官方页使用；不要把 feature 名和这个字段当成已经文档化的同一套开关。

## 插件自带的 MCP 服务器

已安装插件可以在插件清单里带上 MCP 服务器。这些服务器由插件启动，用户配置不写它们的 `command` 或 `url`。用户仍可以在 `plugins.<plugin>.mcp_servers.<server>` 下开关和设定工具策略。官方示例：

```toml
[plugins."sample@test".mcp_servers.sample]
enabled = true
default_tools_approval_mode = "prompt"
enabled_tools = ["read", "search"]

[plugins."sample@test".mcp_servers.sample.tools.search]
approval_mode = "approve"
```

插件提供的 HTTP MCP 可以在 `.mcp.json` 里声明 OAuth。清单用驼峰字段 `clientId`、`callbackUrl`、`callbackPort`，不是 `config.toml` 里的蛇形字段。回调选择规则和普通 MCP 相同：插件给了 `clientId`，提供者不支持 issuer 绑定回调，而 `callbackUrl` 又没有服务器专用的 callback id 时，登录会忽略那个 URL，改用 `mcp_oauth_callback_url`（没设则 `http://127.0.0.1/callback`）并附上 callback id。配置里的 `callbackUrl` 保持原样。

插件的 `oauth.callbackPort` 覆盖全局 `mcp_oauth_callback_port`。两个都没设时，Codex 选一个临时端口。`callbackUrl` 里嵌着的端口不会选中监听端口。直接的 loopback 若要固定端口，两个值写成一样。远程入口或别的代理上，回调 URL 的端口和本机监听端口可以有意不同。

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

官方还写了 `startup_readiness`。默认 `"connection"` 要求一条活连接。设成 `"catalog"` 时，有效的缓存工具目录可以先满足启动，服务器同时继续连接；真正调用工具仍要活连接。`required = true` 则是：这个已启用的服务器没就绪，启动就失败。

**服务器 instructions。** Codex 会读初始化时返回的 MCP `instructions` 字段，把它和工具一起当作整台服务器的指导。官方建议用它写跨工具的流程、约束和速率限制，并让前 512 个字符本身就能看懂，因为决定要不要用这台服务器时，最重要的话在这一段里。这是服务器作者提供的字段，不是 `config.toml` 里的一项。

插件自带的 MCP 不在用户配置里写 `command`／`url`。开关和审批见上一节。

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

- [Codex 常用 MCP 推荐](./02-Codex常用MCP服务器推荐-官方示例7个怎么选.md)
- [Codex MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)
- [代码智能 MCP：Serena 与 codebase-memory-mcp](./04-Codex代码智能MCP-Serena与codebase-memory-mcp怎么装怎么选.md)
- [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [沙箱与主机权限风险](../10-配置模型与权限安全/05-Codex沙箱与主机权限风险.md)
- [用 sandbox 命令给 MCP 启动过程套沙箱](../10-配置模型与权限安全/31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)

## 参考资料

- [Model Context Protocol（Codex 扩展 MCP）](https://learn.chatgpt.com/docs/extend/mcp)（2026-11-21 核对）
- [Docs MCP](https://developers.openai.com/learn/docs-mcp)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Codex MCP server removal](https://learn.chatgpt.com/docs/mcp-server)
- [rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)
- [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)
- [更新日志](https://learn.chatgpt.com/codex/changelog)
- [RFC 8252 第 7.3 节](https://www.rfc-editor.org/rfc/rfc8252#section-7.3)
- [OAuth Client ID Metadata Document 草案](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
