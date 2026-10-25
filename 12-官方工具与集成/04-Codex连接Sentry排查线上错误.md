---
id: codex-sentry-error-triage
title: Codex 连接 Sentry 排查线上错误：官方插件、远程 MCP 和自建 Sentry 三种接法（0.164.0 实测）
seo_title: Codex 连接 Sentry 排查线上错误：插件、远程 MCP 与自建接入
description: 把 Sentry 接进 Codex，可以让它读取线上错误的 Issue、堆栈和事件，再回到仓库找原因。本文结合官方文档和 Codex CLI 0.164.0 实测，讲清官方插件、远程 MCP、自建 Sentry 三种接法，项目范围、OAuth 权限、工具审批和排查流程。
url: /guides/codex-sentry-error-triage
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-19
date_modified: 2026-10-25
verified_on: 2026-10-25
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex Sentry, Sentry MCP, mcp.sentry.dev, codex mcp add, Sentry 插件, 线上错误排查]
related: [codex-github-issue-to-pr, config-toml-guide]
howto: true
faq:
  - q: Sentry MCP 的地址是什么？
    a: 远程地址是 https://mcp.sentry.dev/mcp。可以在后面加组织和项目把范围收窄，比如 https://mcp.sentry.dev/mcp/{组织}/{项目}，Sentry 官方建议尽量限定到项目。
  - q: 连接 Sentry MCP 要不要自己建 Token？
    a: 远程连接默认走 OAuth，第一次连接时在浏览器里授权即可，不用建 Token。自建 Sentry 用本地 stdio 方式时，才需要建 User Auth Token。
  - q: 旧教程里的 ?agent=1 还能用吗？
    a: 2026-10-25 核对时，Sentry MCP 文档只列出 ?experimental=1 这一个查询参数，没有 ?agent=1。以 mcp.sentry.dev 上的说明为准。
  - q: 能让 Codex 只读、不改 Sentry 里的数据吗？
    a: 可以把 MCP 服务器的 default_tools_approval_mode 设成 writes，让没有标记为只读的工具在调用前都要你确认；也可以用 enabled_tools 或 disabled_tools 限制可用工具。官方 Sentry 插件里的 Skill 本身是只读的。
---

# Codex 连接 Sentry 排查线上错误：官方插件、远程 MCP 和自建 Sentry 三种接法（0.164.0 实测）

> 本文在线版：[codexguide.io/guides/codex-sentry-error-triage](https://codexguide.io/guides/codex-sentry-error-triage)

> 核对依据：Sentry 官方 [Sentry MCP](https://mcp.sentry.dev/) 说明页和 [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) 仓库 README，OpenAI 官方文档 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp) 和 [Plugins](https://learn.chatgpt.com/docs/plugins)，以及 Codex 官方插件目录里的 [Sentry 插件](https://github.com/openai/plugins/tree/main/plugins/sentry)。实测环境是 Linux 上的 `codex-cli 0.164.0`，使用独立的 `CODEX_HOME`，验证了添加远程 MCP、自动发起 OAuth、`codex mcp list/get` 和配置写法；**没有用真实 Sentry 账号完成授权**，所以没有实际读取 Issue，工具清单和返回内容以 Sentry 文档为准。核对日期 2026-10-25。

线上报错进了 Sentry，排查时通常要在 Sentry 页面、日志、代码和测试之间来回切换。把 Sentry 接进 Codex 以后，可以让它直接读取 Issue 详情、堆栈和事件，再结合本地仓库定位原因、补测试、改代码。

Sentry 是外部数据源。接入后 Codex 能看到哪些组织、项目和事件，取决于你授权的账号范围；能执行哪些操作，取决于 Sentry 暴露的工具和你在 Codex 里设置的审批方式。

## 三种接法怎么选

| 接法 | 适合谁 | 鉴权 |
| --- | --- | --- |
| Codex 官方插件目录里的 Sentry 插件 | 用 Codex 桌面端或 CLI，想一键安装 | 插件里的 MCP 走 OAuth；插件里的只读 Skill 用 `SENTRY_AUTH_TOKEN` |
| 远程 MCP：`codex mcp add` | 用 CLI，想自己控制项目范围和工具审批 | OAuth |
| 本地 stdio：`@sentry/mcp-server` | 自建（self-hosted）Sentry | Sentry User Auth Token |

用的是 sentry.io 云服务，优先选前两种。

## 接法一：安装官方 Sentry 插件

Codex 官方插件目录 [openai/plugins](https://github.com/openai/plugins) 收录了 Sentry 插件（核对时版本 0.1.2，简介是“Inspect recent Sentry issues and events”）。它包含两部分：

- 一个 `.mcp.json`，把 MCP 服务器指向 `https://mcp.sentry.dev/mcp`
- 一个只读的 Sentry Skill，用自带的 `scripts/sentry_api.py` 调 Sentry API，查询最近的 Issue、Issue 详情和事件

安装方式：CLI 里输入 `/plugins` 搜索 Sentry；桌面端打开 Plugins 搜索安装。官方插件文档提醒：插件里的 MCP 可能需要额外的连接或授权；Skills 要新开对话或会话后才可用。

插件里的 Skill 需要 `SENTRY_AUTH_TOKEN` 环境变量。Skill 文档建议创建**只读权限**的 Token（例如 `project:read`、`event:read`、`org:read`），在本机设置成环境变量；并明确写着**不要把完整 Token 粘贴到对话里**。

## 接法二：用 codex mcp add 添加远程 MCP

Sentry MCP 的远程地址是 `https://mcp.sentry.dev/mcp`，可以在后面加上组织或项目来收窄范围：

| 地址 | 范围 |
| --- | --- |
| `https://mcp.sentry.dev/mcp` | 你账号能访问的全部 |
| `https://mcp.sentry.dev/mcp/{组织}` | 限定一个组织 |
| `https://mcp.sentry.dev/mcp/{组织}/{项目}` | 限定一个项目 |

限定范围后，工具会默认使用这个组织或项目，不需要的发现类工具会被隐藏。**Sentry 建议能限定到项目就限定到项目。** 另外可以加 `?experimental=1` 启用实验性的工具变体。

> 一些旧教程里的 `?agent=1` 参数，核对时已不在 Sentry MCP 文档里，只列出了 `?experimental=1`。

实测（`my-org` 和 `my-project` 是占位的组织和项目名）：

```bash
codex mcp add sentry --url https://mcp.sentry.dev/mcp/my-org/my-project
```

输出：

```text
Added global MCP server 'sentry'.
Detected OAuth support. Starting OAuth flow…
Authorize `sentry` by opening this URL in your browser:
https://mcp.sentry.dev/oauth/authorize?response_type=code&client_id=...&scope=org%3Aread+project%3Awrite+team%3Awrite+event%3Awrite+alerts%3Awrite&...
```

可以看到两点：

1. Codex 检测到服务器支持 OAuth，**添加后立即发起授权**，在浏览器里打开链接登录 Sentry 并同意即可。
2. 授权链接里请求的权限是 `org:read`、`project:write`、`team:write`、`event:write`、`alerts:write`，包含写权限。这是 Sentry 服务器公布的默认权限。

如果当时没完成授权，之后可以单独运行：

```bash
codex mcp login sentry
```

`codex mcp login` 支持 `--scopes` 指定本次请求的权限；也可以在 `config.toml` 里给这个服务器设置 `scopes`。不设置时，Codex 使用服务器公布的权限。能不能只用更小的权限完成你需要的操作，取决于 Sentry 那边，改之前先确认。

添加后的配置和状态：

```toml
[mcp_servers.sentry]
url = "https://mcp.sentry.dev/mcp/my-org/my-project"
```

```bash
codex mcp list
```

```text
Name    Url                                           Bearer Token Env Var  Status   Auth
sentry  https://mcp.sentry.dev/mcp/my-org/my-project  -                     enabled  Not logged in
```

授权完成前 `Auth` 列显示 `Not logged in`。`codex mcp get sentry` 能看到 `transport: streamable_http`，以及删除命令 `codex mcp remove sentry`。

## 接法三：自建 Sentry 用本地 stdio

自建 Sentry 要用 Sentry 的本地 MCP 服务器 `@sentry/mcp-server`，并在 Sentry 里创建 User Auth Token。README 列出的权限（“截至撰写时”）是：`org:read`、`project:read`、`project:write`、`team:read`、`team:write`、`event:write`。

README 的启动方式是：

```bash
npx @sentry/mcp-server@latest --access-token=<你的 Token> --host=sentry.example.com
```

`--host` 只写主机名。只提供 HTTP 的内网部署再加 `--insecure-http`。

接进 Codex 时，**不要把 Token 写进命令或配置文件**。Codex 的 stdio 服务器支持 `env_vars`，把本机已有的环境变量转发给服务器；README 也说明服务器会读取 `SENTRY_ACCESS_TOKEN` 环境变量。实测可以被 Codex 正确识别的写法：

```toml
[mcp_servers.sentry-selfhosted]
command = "npx"
args = ["@sentry/mcp-server@latest", "--host=sentry.example.com"]
env_vars = ["SENTRY_ACCESS_TOKEN"]
```

`codex mcp list` 显示：

```text
Name               Command  Args                                                 Env                        Cwd  Status   Auth
sentry-selfhosted  npx      @sentry/mcp-server@latest --host=sentry.example.com  SENTRY_ACCESS_TOKEN=*****  -    enabled  Unsupported
```

stdio 服务器不走 OAuth，所以 `Auth` 是 `Unsupported`。启动 Codex 前在终端里设置好 `SENTRY_ACCESS_TOKEN`。

还要注意两点（来自 sentry-mcp README）：

- 自建 Sentry 没有 Seer，所以 `--host` 指向非 sentry.io 的主机时，默认不启用 `seer` 技能组；自建环境确实部署了 Seer，可以用 `--skills=inspect,seer` 打开。不支持的工具组可以用 `--disable-skills` 关掉。
- `search_errors`、`search_issues` 这类 AI 搜索工具需要单独配置一个模型提供方（OpenAI、Azure OpenAI、Anthropic 或 OpenRouter），用 `EMBEDDED_AGENT_PROVIDER` 指定。不配置的话这些工具不可用，其他工具正常。

## 控制 Codex 能做什么

Sentry 里有写操作的工具，事件里也可能带请求参数和用户上下文。建议接入时就把边界设好。Codex 的 MCP 配置支持：

| 配置 | 作用 |
| --- | --- |
| `default_tools_approval_mode` | 这个服务器的工具默认审批方式：`auto`、`prompt`、`writes`、`approve`。`writes` 表示没有标记为只读的工具调用前都要你确认 |
| `enabled_tools` / `disabled_tools` | 工具白名单 / 黑名单（黑名单在白名单之后生效） |
| `tools.<工具名>.approval_mode` | 单个工具的审批方式 |
| `enabled = false` | 暂时停用这个服务器，不删配置 |

例如，让 Sentry 的写操作都先问你：

```toml
[mcp_servers.sentry]
url = "https://mcp.sentry.dev/mcp/my-org/my-project"
default_tools_approval_mode = "writes"
```

另外，sentry-mcp README 在“用显式 Token 直连远程服务器”一节写到，可以在地址后加 `?skills=inspect,triage` 或 `?disable-skills=seer` 按技能组收窄暴露的工具。OAuth 连接是否同样适用，README 没有写明，以 Sentry 文档为准。

## 从一个 Issue 开始排查

接好以后，不要一上来让 Codex 扫整个组织。先给一个 Sentry Issue 链接或 Issue 编号，让它只读、先分析：

```text
请读取这个 Sentry Issue：<Issue 链接>
先不要修改任何文件，也不要修改 Sentry 里的状态。
1. 总结错误信息、首次和最近出现时间、影响的版本或环境。
2. 结合当前仓库，找到堆栈里对应的代码位置。
3. 说明你认为的触发条件，并标出哪些是从事件数据确认的、哪些是推测。
4. 列出复现这个问题需要的测试，以及还缺哪些信息。
```

拿到分析后再进入修复：

1. 先让 Codex 写一个能复现问题的失败测试。
2. 再修改代码，让测试通过。
3. 跑相关的测试集，检查 diff。
4. 对照 Sentry 事件里的触发条件，确认修复覆盖了它。

需要在 Sentry 里改 Issue 状态、分配负责人这类写操作时，单独提出来，在审批时看清楚工具名和参数再同意。

## 排查结束后

- 事件里的请求参数、用户信息可能是敏感数据，不要让 Codex 把它们写进提交信息、PR 描述或公开文档。
- 不再需要时，`codex mcp remove sentry` 删除服务器；只是暂停用，就设 `enabled = false`。
- 通过插件安装的，在插件浏览器里卸载。官方插件文档提醒：卸载插件不会断开在 ChatGPT 里单独连接的 MCP 集成，需要去那边单独断开。

## 参考资料

- [Sentry MCP（mcp.sentry.dev）](https://mcp.sentry.dev/)
- [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)
- [OpenAI 官方文档：Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)
- [OpenAI 官方文档：Plugins](https://learn.chatgpt.com/docs/plugins)
- [Codex 官方插件目录：Sentry 插件](https://github.com/openai/plugins/tree/main/plugins/sentry)
