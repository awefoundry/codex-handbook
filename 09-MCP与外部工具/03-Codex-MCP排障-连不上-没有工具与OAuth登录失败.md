---
id: mcp-troubleshooting
title: Codex MCP 排障：服务器连不上、工具不显示、OAuth 登录失败，按这个顺序查
seo_title: Codex MCP 排障：连不上、没有工具、OAuth 失败排查顺序
description: Codex 接了 MCP 却用不起来？按「进程能否启动 → 工具是否加载 → 认证是否有效 → 调用是否超时」排查，讲清 startup_timeout_sec、enabled_tools、env_vars、OAuth 注册与回调等关键设置，并整理社区常见症状。
lede: MCP 坏了别同时改十处。先分清是哪一层，再对着官方设置逐项查。
url: /guides/codex-mcp-troubleshooting
status: draft
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 排障
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 3
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
client_validation_pending: true
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex MCP 排障, MCP 连不上, startup timeout, mcp login, MCP OAuth, enabled_tools, tool_timeout]
related: [mcp-getting-started, mcp-servers-recommended]
faq:
  - q: codex mcp list 能看见服务器，对话里却没有工具，先查什么？
    a: 先看 enabled 是否为 false、enabled_tools／disabled_tools 是否把工具滤空、审批是否一直在等你点同意，以及是否改完配置却没 Restart／新开会话。插件自带的 MCP 要在 plugins.*.mcp_servers.* 下查，而不是只看顶层 mcp_servers。
  - q: OAuth 登录成功了，当前会话还报 invalid_grant，怎么办？
    a: 社区里有报告（openai/codex #14144）：重新登录成功后，正在跑的会话仍可能用旧的 refresh token。官方文档要求改完配置后 Restart／新开会话；遇到这类症状，优先新开会话或重启客户端，不要把 client_secret 贴进聊天。
  - q: 还能用 codex mcp-server 把 Codex 自己挂成 MCP 吗？
    a: 不能。官方已移除 codex mcp-server 与独立的 codex-mcp-server 二进制。要把外部工具接进 Codex，用 codex mcp；深度集成请看 Codex app server（另一套协议，不是 MCP）。
---

# Codex MCP 排障：服务器连不上、工具不显示、OAuth 登录失败，按这个顺序查

> 本文计划路径：[codexguide.io/guides/codex-mcp-troubleshooting](https://codexguide.io/guides/codex-mcp-troubleshooting)

> 核对依据：learn.chatgpt.com／developers.openai.com 的 MCP 扩展文档与 Configuration Reference（`mcp_servers.*`、`mcp_oauth_*`），以及 Codex MCP server 移除说明。文中「我的用法」是操作建议；社区 issue 只作症状对照，不是官方修复承诺。

这篇接在《Codex MCP 入门》之后：入门讲怎么接，这篇讲**接上却坏了怎么按层查**。推荐装哪些服务器，见姊妹篇《Codex 常用 MCP 服务器推荐》。

## 先分清是哪一层坏了

多数「MCP 用不了」其实是不同层的问题，混在一起改配置只会越改越乱。按这个顺序想：

| 层 | 你感觉到的症状 | 先看什么 |
|---|---|---|
| 1. 配置／状态 | `list` 里没有、名字对不上、`enabled = false` | `codex mcp list`、`config.toml`、项目是否信任 |
| 2. 启动 | 会话起不来、报 startup／初始化失败、可选服务器一直不进目录 | `command`／`url`、`env_vars`、`startup_timeout_sec`、`required` |
| 3. 工具列表 | 服务器在，但对话里看不到／调不到工具 | `enabled_tools`／`disabled_tools`、审批、插件 MCP 路径、是否 Restart |
| 4. 认证 | Authenticate／`mcp login` 失败，或工具一调就 401／invalid_grant | HTTP vs STDIO、OAuth 注册方式、回调、`bearer_token_env_var` |
| 5. 调用 | 工具能看见，但卡住、超时、内存／进程暴涨 | `tool_timeout_sec`、单服务器无法热重启、进程泄漏类症状 |

**我的用法：** 同一时间只动一层。先用 `list`／`/mcp` 钉住「有没有、启没启」，再动手改超时或 OAuth。

## 看状态：`codex mcp list`、`/mcp`、日志在哪

### CLI

```bash
codex mcp list
codex mcp --help
```

`list` 回答的是「配置里登记了哪些服务器」。它不等于当前会话一定已经握手成功；握手结果要进会话后再用 TUI／桌面状态确认。

对需要 OAuth 的 **Streamable HTTP** 服务器：

```bash
codex mcp login <server-name>
```

官方写明：`codex mcp login` **只适用于 Streamable HTTP**。STDIO 服务器不要走这条路，改用 `env`／`env_vars` 或服务器自己的本地登录。

### TUI 与桌面／IDE

- TUI：`/mcp` 查看当前会话里活跃的 MCP 服务器；CLI **0.161.0** 起可用 `/mcp login <server>`。
- 桌面：Settings → MCP servers；列表会标启用与是否需要 OAuth；需要时点 **Authenticate**；作曲区也可输入 `/mcp`。
- IDE：齿轮 → MCP servers；改完后 **Restart extension**。

改完 `config.toml` 或界面配置后，通常要 **Restart** 桌面端／扩展，或**新开** CLI 会话，工具目录才会刷新。

### 日志与会话（求助时用）

官方 Troubleshooting 给出的位置（macOS 桌面端）：

- 应用日志：`~/Library/Logs/com.openai.codex/YYYY/MM/DD`
- 会话：`$CODEX_HOME/sessions`（默认 `~/.codex/sessions`）
- 归档会话：`$CODEX_HOME/archived_sessions`

分享前先脱敏。CLI 侧还可把 `log_dir` 指到自定义目录（见 Configuration Reference）；明文 TUI 日志需显式打开相关选项，不要默认假设一定有。

## 启动失败：命令、PATH、`env_vars`、启动超时

### STDIO：命令根本起不来

典型配置：

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

先在**同一用户、同一 PATH** 的终端里手动跑一遍命令／`npx`。GUI 启动的桌面端 PATH 往往比交互式 shell 短：`node`／`npx` 在终端里有、在 Codex 里没有，是常见坑。

相关字段：

- `command`／`args`／`cwd`：命令、参数、工作目录
- `env`：直接写入的环境变量
- `env_vars`：从 Codex 环境**转发**的变量名（字符串默认 `source = "local"`；`source = "remote"` 仅配合远程 executor 的 STDIO）

```toml
env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]
```

**我的用法：** 密钥用 `env`／`env_vars`／`bearer_token_env_var` 注入，不要写进对话，也不要提交含 `oauth.client_secret` 的 `config.toml`。

### HTTP：URL 与鉴权头

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

- `url` 必填
- `bearer_token_env_var`：从环境变量读 Bearer，放进 `Authorization`
- `http_headers`／`env_http_headers`：静态头或从环境变量取头
- `http_headers_helper`：本地命令打印 JSON 头（仅本地 HTTP；stdio／远程执行路径不支持）
- `auth`：在 bearer／头之后的回退；`oauth`（默认）用已存 OAuth；`chatgpt` 用于受信第一方 ChatGPT 源，再回退 OAuth

没有解析到任何凭证时，Codex **仍可能**无认证连接；需要 OAuth 时再单独 `codex mcp login`。

### 启动超时与「可选服务器」

| 设置 | 默认 | 作用 |
|---|---|---|
| `startup_timeout_sec` | **10** | 单个服务器启动／初始化超时（另有毫秒别名 `startup_timeout_ms`） |
| `mcp_optional_startup_grace_ms` | **1000** | 建初始工具目录时，对**可选**服务器额外等多久；`0` 则改等各自的 `startup_timeout_sec` |
| `required = true` | 关 | 该启用服务器初始化失败则启动／恢复失败；仍走自己的启动超时 |

第一次跑 `npx -y …` 要下包装，10 秒经常不够。官方示例里会把 `startup_timeout_sec` 调到 20 一类数值：

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
startup_timeout_sec = 20
tool_timeout_sec = 45
```

**我的用法：** 慢启动先加大 `startup_timeout_sec`，不要一上来把所有服务器都设 `required = true`——一个挂掉会拖垮整次启动／恢复。

### 别踩：`codex mcp-server` 已移除

`codex mcp-server` 与独立的 `codex-mcp-server` 二进制**已删除**。旧教程若教你「把 Codex 自己挂成 MCP」，升级后会直接失败。正确方向：用 `codex mcp` 接**外部** MCP；需要认证、历史、审批与流式事件的深度集成，看 **Codex app server**（自有 JSON-RPC，**不是** MCP，也不是生产替代品）。

## 有服务器但没有工具：白名单顺序、审批、插件 MCP

服务器「在列表里」≠「模型能看见工具」。

### `enabled_tools`／`disabled_tools` 的顺序

官方写明：`disabled_tools` 在 `enabled_tools` **之后**生效。

```toml
[mcp_servers.chrome_devtools]
enabled_tools = ["open", "screenshot"]
disabled_tools = ["screenshot"]  # 最终只剩 open
```

若白名单写错名字，或黑名单把白名单清空，表现就是「连上了但没有可用工具」。

### 整机关闭与审批

- `enabled = false`：配置保留，服务器不启用
- `default_tools_approval_mode`／`tools.<name>.approval_mode`：`auto`｜`prompt`｜`writes`｜`approve`  
  `writes`：对**未**标成只读的工具会提示审批
- 会话里一直停在审批／你关了审批弹层，也会像「工具没反应」

### 插件自带的 MCP

插件清单里的 MCP **不由**用户 `config.toml` 写 `command`／`url` 启动。开关与工具策略写在：

```toml
[plugins."sample@test".mcp_servers.sample]
enabled = true
enabled_tools = ["read", "search"]
default_tools_approval_mode = "prompt"
```

只翻顶层 `[mcp_servers.*]` 会漏掉这类服务器。

### 项目级配置没加载

项目级 `.codex/config.toml` **仅信任项目**才会加载。未信任项目会跳过项目级 `.codex/`（含本地 config）。同事 clone 了仓库 ≠ 本机已信任。

**我的用法：** 先在无白名单的干净配置下确认工具能列出，再逐步加 `enabled_tools`；改完必 Restart／新会话。

## OAuth 登录失败：注册方式、回调、旧 token

前提再次强调：`codex mcp login` **只对 Streamable HTTP**。报错里若出现 Dynamic registration／callback／`invalid_grant`，先确认你配的是 `url = "..."`，不是 STDIO。

### 客户端注册：CIMD／DCR／预注册

Codex 支持 **CIMD**（Client ID Metadata Documents）与 **DCR**（Dynamic Client Registration）。默认 `auto`：授权服务器广告满足条件时走 CIMD，否则在可用时走 DCR。配置了 `oauth.client_id` 会**跳过**动态注册。

单次登录可强制：

```bash
codex mcp login <server-name> --oauth-client-registration cimd
codex mcp login <server-name> --oauth-client-registration dcr
```

该选择**只作用于本次登录**，不会写入 `config.toml`。

社区症状对照（open issue，非官方修复说明）：

- **#13200**：对 Slack 官方远程 MCP（`https://mcp.slack.com/mcp`）执行 `codex mcp login` 时报 `Dynamic client registration not supported`。  
  **官方可用方向：** 需要预注册 client 时，用 `codex mcp add … --oauth-client-id`（机密客户端再加 `--oauth-client-secret`），或按提供商要求改用支持的注册方式／`--oauth-client-registration`。不要发明「改 hosts／关 HTTPS」一类非官方步骤。

### 回调 URL 与端口

添加预注册客户端时，Codex 会打印完整回调，例如：

```text
OAuth callback URL: http://127.0.0.1/callback
```

全局覆盖（远程 Devbox／固定入口常用）：

```toml
mcp_oauth_callback_port = 5555
mcp_oauth_callback_url = "https://devbox.example.internal/callback"
```

单服务器：`[mcp_servers.<name>.oauth]` 下的 `client_id`、`client_secret`、`callback_url`、`callback_port`。

要点（摘自官方）：

- **务必**把提供商后台登记的回调，与 `codex mcp add`／登录时显示的完整回调写成一致。
- 回调 URL 里的端口**不会**自动变成监听端口；固定监听用 `mcp_oauth_callback_port` 或 `oauth.callback_port`。
- 对 `http://127.0.0.1` 且未写端口的回调，Codex 在展示／存储时可省略监听端口，授权时再插入实际端口（RFC 8252 loopback）；`localhost`、IPv6、HTTPS、已带端口的 URL 不适用这套替换。
- 授权响应里的 `iss` 校验失败会硬失败，不会换回调重试。

### 登录成功但会话仍用旧 token

社区 **#14144**：OAuth 重新登录显示成功，**当前仍在跑的会话**却继续用旧 refresh token，报 `invalid_grant`；**重启应用／新开会话**后恢复。

这与官方「改完要 Restart／新会话」一致。不要假设 `mcp login` 会热替换所有已打开会话的内存凭证。

**我的用法（OAuth 短顺序）：**

1. 确认是 HTTP，不是 STDIO。  
2. `codex mcp list` 核对名字与 `enabled`。  
3. 看报错是「不支持动态注册」还是回调／`iss`／端口——前者考虑预注册或 `--oauth-client-registration`；后者对齐回调与端口。  
4. 登录成功后**新开会话**再试工具。  
5. 仍失败：脱敏后带上 CLI／App 版本、服务器 URL（可打码路径）、注册方式（auto／cimd／dcr／预注册），去 GitHub issue 对照；**不要**贴 `client_secret` 或完整 token。

## 调用超时，以及不能单独重启某个服务器

### `tool_timeout_sec`

默认 **60** 秒。浏览器自动化、大仓库检索等可能不够：

```toml
tool_timeout_sec = 120
```

超时只说明「这一次工具调用超过预算」，不等于服务器进程死了。可配合 `tools.<name>.output_token_limit` 防止超大输出回灌。

### 不能热重启单个 MCP（#4955）

社区 **#4955** 请求「单独重启某个 MCP 服务器」：现状是会话创建连接管理器时拉起服务器，之后不会按名热重启；要刷新通常得**结束并重开整个 CLI／应用会话**（或桌面 Restart）。在官方提供对应能力之前，请把「改了本地 MCP 代码却不生效」当成预期限制，而不是配置写错。

## 进程越积越多、内存上涨（#30408）

社区 **#30408** 描述的症状（桌面／app-server 场景，issue 仍 open）：每个对话／线程拉起一套全局 MCP 进程，关闭或归档线程后**不回收**，RSS 可涨到数 GB。

官方 MCP 文档目前没有「一键清理孤儿 MCP 进程」的设置项。在修复落地前，**临时处理只能来自运维常识与 issue 讨论**，本文不编造官方命令：

**我的用法（临时、非官方）：**

1. 少开并行长会话；不用的服务器设 `enabled = false`，降低每线程拉起的进程数。  
2. 观察到内存异常时，退出 Codex／相关会话后再用系统工具确认是否仍有残留的 `npx`／MCP 子进程（注意不要误杀无关 Node 进程）。  
3. 在 #30408 补充 App／内置 CLI 版本与进程列表摘要，帮助官方复现；不要上传可能含隐私的完整会话日志。

## 求助前收集清单

复制下面填空，能少来回好多轮：

1. 表面：桌面 App／CLI／IDE？版本号（`codex --version`；桌面可用官方文档中的 bundle 路径查内置 CLI）。  
2. 传输：STDIO 还是 Streamable HTTP？`command` 或 `url`（可打码）。  
3. `codex mcp list` 输出（打码 token／路径中的用户名）。  
4. `/mcp` 或 Settings 里该服务器状态：启用？要 Authenticate？  
5. 完整报错原文（Dynamic registration／invalid_grant／timeout 等）。  
6. 改过的字段：`startup_timeout_sec`、`tool_timeout_sec`、`enabled_tools`／`disabled_tools`、`env_vars`、`bearer_token_env_var`、`mcp_oauth_callback_*`、`--oauth-client-registration`。  
7. 是否已 Restart／新开会话。  
8. 是否项目级 `.codex/config.toml`、项目是否已信任；是否插件 MCP。  
9. 相关日志片段（已脱敏）。  

## 一页顺序（可贴在显示器边）

1. `codex mcp list` → 有没有、名字对不对、`enabled`。  
2. STDIO：本机手动跑通 `command`；查 PATH／`env_vars`／`cwd`。HTTP：查 `url`／bearer／头。  
3. 启动超时：默认 10 秒；慢启动加大 `startup_timeout_sec`；慎用 `required`。  
4. 有服无工具：查白名单／黑名单顺序、审批、插件路径、信任项目、Restart。  
5. OAuth：仅 HTTP；注册方式与预注册；回调与端口一致；登录后新会话。  
6. 调用：加大 `tool_timeout_sec`；接受「不能单服热重启」；进程泄漏先减服务器、退出再查进程。  
7. 仍不行：带清单去官方文档与 GitHub issue，不贴密钥。

## 接下来读什么

- 《Codex MCP 入门》→ `/guides/codex-mcp-getting-started`（计划）  
- 《Codex 常用 MCP 服务器推荐》→ 计划 id `mcp-servers-recommended`  
- config 字段覆盖与排查 → `/advanced/config-toml`  
- 新手常见误区（含 MCP 报错一行）→ `/guides/codex-xin-shou-chang-jian-wu-qu`  
- 权限沙箱与审批 → `/guides/codex-quan-xian-sha-xiang-yu-shen-pi`

## 参考资料

- [Model Context Protocol（Codex 扩展 MCP）](https://learn.chatgpt.com/docs/extend/mcp)  
- [Configuration Reference（`mcp_servers.*`／`mcp_oauth_*`）](https://developers.openai.com/codex/config-reference)  
- [Codex MCP server removal](https://learn.chatgpt.com/docs/mcp-server)  
- [Troubleshooting（日志与会话路径）](https://learn.chatgpt.com/docs/reference/troubleshooting)  
- 社区症状：[#13200](https://github.com/openai/codex/issues/13200)、[#14144](https://github.com/openai/codex/issues/14144)、[#30408](https://github.com/openai/codex/issues/30408)、[#4955](https://github.com/openai/codex/issues/4955)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
