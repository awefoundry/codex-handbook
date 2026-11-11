---
id: codex-network-permissions-proxy
title: Codex 网络权限怎么配：permission profiles 的联网开关、network_proxy 域名白名单与本地服务访问
seo_title: Codex 网络权限：network.enabled、network_proxy 与域名白名单实测
description: Codex 的 permission profiles 可以控制沙箱里的命令能不能联网、能连哪些域名。本文按官方文档和实测，讲 network.enabled 和 network_proxy 的三种组合、域名白名单怎么写、localhost 和 Docker socket 怎么放行，以及这个白名单管不到网页搜索、MCP 和浏览器。
lede: 只写 network.enabled 不够；不开 network_proxy，域名白名单一条都不生效。
url: /guides/codex-network-permissions-proxy
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 26
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-11
date_modified: 2026-11-11
verified_on: 2026-11-11
official_ref: https://learn.chatgpt.com/docs/permissions
keywords: [Codex 网络权限, permission profiles, network.enabled, features.network_proxy, 域名白名单, allow_local_binding, 沙箱联网]
related: [permissions-sandbox-approvals, codex-web-search-settings, codex-rules-prefix-rule]
faq:
  - q: 我在 profile 里写了域名白名单，为什么别的网站还能访问？
    a: 多半是没开 features.network_proxy。官方文档写明，network.enabled = true 只允许联网，不启动代理；没有运行中的代理，域名规则不限制直连。实测关掉代理后，白名单外的 example.com 照样返回 200。
  - q: 开了代理以后，本地的 localhost 服务连不上了，怎么办？
    a: 代理默认拦截本机和内网地址。在 domains 里精确放行 "localhost" 或 "127.0.0.1"；只有当允许的域名会解析到本机或内网地址时，才需要设 allow_local_binding = true。
  - q: 白名单能限制 Codex 的网页搜索和 MCP 吗？
    a: 不能。官方列明，代理只过滤沙箱里本地命令的流量；网页搜索、应用和连接器、MCP 服务器、浏览器和 Computer Use、Codex 自身的模型和登录请求、Codex Cloud 都用各自的设置。
  - q: 代理端口是 3128 吗？
    a: 文档写的默认值是 http://127.0.0.1:3128（SOCKS5 为 127.0.0.1:8081）。但我们在 Linux 上用 codex sandbox 实测时，沙箱里看到的代理是随机端口，所以排查时以命令里实际的 HTTPS_PROXY 等环境变量为准，不要写死端口。
---

# Codex 网络权限怎么配：permission profiles 的联网开关、network_proxy 域名白名单与本地服务访问

> 本文在线版：[codexguide.io/guides/codex-network-permissions-proxy](https://codexguide.io/guides/codex-network-permissions-proxy)

> 核对依据：官方文档 [Permissions](https://learn.chatgpt.com/docs/permissions)（页面标注 Beta，2026-11-11 核对）。实测环境：Linux、**Codex CLI 0.165.0**、临时 `CODEX_HOME`，用 `codex sandbox -- curl …` 在沙箱里发请求，时间为北京时间 2026-11-11 09:00 左右。测试机本身走一个上游代理出网，结果可能和你的网络不同；**macOS 和 Windows 的沙箱没有测试**。

很多人给 Codex 配网络权限的第一步是写 `network.enabled = true`，再写一串允许的域名，然后以为「只能访问这几个网站」。实际上，如果没打开网络代理，这串域名一条都不生效。这篇把联网开关、代理、白名单和本地服务四件事讲清楚，每个结论都附实测结果。

## 先看结论

- **两个开关**：`permissions.<名字>.network.enabled` 决定命令能不能联网；`[features] network_proxy = true` 才会启动代理，让域名规则生效。
- **三种组合**：联网关 = 不能联网；联网开、代理关 = 直连，不受域名规则限制；联网开、代理开 = 按白名单走代理，没有任何 allow 条目就全部拦截。
- **本机服务默认被拦**：代理开着时，`localhost`、`127.0.0.1` 和内网地址默认不能访问，要精确放行。
- **管不到的地方**：网页搜索、MCP、连接器、浏览器和 Computer Use、Codex 自身的请求、Codex Cloud，都不受这个白名单控制。

权限沙箱和审批的整体思路，先看《[权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)》。本文只讲网络这一块。

## 一个最小可用的配置

下面这个 profile 是我实测用的：在内置 `:workspace` 的基础上，只允许命令访问 npm 源。

```toml
default_permissions = "npm-only"

[features]
network_proxy = true

[permissions.npm-only]
extends = ":workspace"

[permissions.npm-only.network]
enabled = true

[permissions.npm-only.network.domains]
"registry.npmjs.org" = "allow"
```

三点说明：

- `default_permissions` 指定默认用哪个 profile。内置的有 `:read-only`、`:workspace` 和 `:danger-full-access`。
- `extends = ":workspace"` 表示继承内置 `:workspace` 的文件规则：工作区可写，`.git/`、`.agents/`、`.codex/` 等目录保持只读。
- 官方文档提醒，permission profiles 和旧的 `sandbox_mode` / `sandbox_workspace_write` 写法**一次只用一种**，不要混用。

## 实测：三种组合的真实效果

我在沙箱里分别请求 npm 源、白名单外的 example.com 和本机服务，结果如下：

| 设置 | registry.npmjs.org | example.com | 本机 127.0.0.1 |
|---|---|---|---|
| 联网开 + 代理开（上面的配置） | 200 | 被拒，`CONNECT tunnel failed, response 403` | 403 |
| 联网开 + 代理关 | — | **200（直连，白名单没生效）** | — |
| 联网关 | — | `Could not resolve host`（连域名都解析不了） | — |
| 联网开 + 代理开 + 放行 `"127.0.0.1"` | — | — | 200 |

「—」表示这一组没测这个地址。

第二行是最容易踩的坑：**只要代理关着，白名单就是摆设**。这和官方文档的说法一致：没有运行中的代理，域名规则不限制直连。

另外，在 `profile` 里写 `domains` 或 `network.enabled = true` 都**不会**自动打开 `features.network_proxy`。企业环境里，管理员也可以在 `requirements.toml` 里用 `[experimental_network]` 启动代理。

## 域名规则怎么写

官方支持四种写法：

```toml
[permissions.npm-only.network.domains]
"registry.npmjs.org" = "allow"   # 精确域名
"*.example.com" = "allow"        # 只匹配子域名，不含 example.com 本身
"**.example.com" = "allow"       # example.com 和所有子域名
"ads.example.com" = "deny"       # deny 优先于 allow
```

规则细节：

- `*` 单独使用表示允许所有公网域名，**只能用于 allow**。官方提醒，只有确实想放开公网时才这么写，可以再加 deny 收窄。
- 域名会被规范化：去掉首尾空格、转小写、去掉末尾的点、去掉端口号和方括号。所以 `"Registry.npmjs.org:443"` 和 `"registry.npmjs.org"` 是一回事。
- 代理开着但一个 allow 都没有，所有外部地址都会被拦。

常见场景的白名单参考（按需要取用，不是官方清单）：

| 场景 | 可以放行的域名 |
|---|---|
| npm 安装 | `registry.npmjs.org` |
| pip 安装 | `pypi.org`、`files.pythonhosted.org` |
| 拉 GitHub 代码和附件 | `github.com`、`*.github.com`、`objects.githubusercontent.com` |

装依赖时到底访问了哪些域名，以实际报错为准：被拦的请求会返回类似上面的 `CONNECT tunnel failed, response 403`，把需要的域名补进来即可。

## 访问本机服务：localhost 与 allow_local_binding

代理开着时，Codex 会默认拦截本机和内网地址，官方说这是为了防 DNS 重绑定和误连本地服务。实测里，白名单只有 npm 时，请求 `127.0.0.1` 直接返回 403。

要让测试脚本访问本机开发服务器，精确放行地址：

```toml
[permissions.npm-only.network.domains]
"registry.npmjs.org" = "allow"
"localhost" = "allow"
"127.0.0.1" = "allow"
```

实测放行 `"127.0.0.1"` 后，本机服务返回 200。

`allow_local_binding = true` 的作用是**关掉**本地和内网防护。只有当你允许的某个域名会解析到本机或内网地址时才需要它（比如公司内网域名）。默认是 `false`，不需要就别开。

## Docker 等 Unix socket

Docker 这类工具通过 Unix socket 通信，要单独放行：

```toml
[permissions.npm-only.network.unix_sockets]
"/var/run/docker.sock" = "allow"
```

官方把它称为「本地逃生口」，提醒尽量少用；开了 Unix socket，代理监听地址要保持在回环地址上。还有一个 `dangerously_allow_all_unix_sockets`，会绕过整个 socket 白名单，日常开发不要用。

本节没有在测试机上实测 Docker。

## 代理端口与上游代理

文档写的默认监听地址：

```toml
[permissions.npm-only.network]
enabled = true
proxy_url = "http://127.0.0.1:3128"
enable_socks5 = true
socks_url = "http://127.0.0.1:8081"
enable_socks5_udp = true
```

官方建议，除非要对接特定运行时，这些保持默认。代理开着时，Codex 会给沙箱里的命令设好 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY` 等环境变量。

实测时我在沙箱里看到的是 `HTTPS_PROXY=http://127.0.0.1:37595`、`all_proxy=socks5h://127.0.0.1:41125`，端口和文档默认值不同，每次运行也可能变。所以：

- 排查问题时，看命令里实际的代理环境变量，不要写死 3128。
- 有些工具不读代理环境变量，会直接连网，这时请求会失败，需要给工具单独配代理。

如果你的电脑本身要通过公司代理上网，`allow_upstream_proxy` 默认是 `true`，Codex 的代理会沿用你设置的上游 `HTTP(S)_PROXY` 和 `ALL_PROXY`。我的测试机就是这种情况。

## 白名单管不到的地方

这一点官方专门列出来了：网络代理**只过滤沙箱里本地命令的流量**。下面这些用各自的设置：

| 能力 | 用什么控制 |
|---|---|
| 网页搜索 | `web_search` 设置；`tools.web_search.allowed_domains` 只过滤搜索结果，不管命令联网。见《[Codex 网页搜索设置](./18-Codex网页搜索设置-cached-indexed-live与allowed_domains.md)》 |
| 应用和连接器 | 服务端连接、工作区权限和应用设置 |
| MCP 服务器 | `mcp_servers` 配置和管理员的服务器白名单 |
| 浏览器和 Computer Use | 各自的功能开关和审批 |
| Codex 自身的模型、登录请求 | 客户端自己的 HTTP 和系统代理设置 |
| Codex Cloud | 云端环境自己的网络设置 |

所以「命令只能访问 npm」不等于「Codex 只能访问 npm」。要收紧哪一项，就去配哪一项。命令本身能不能跑到沙箱外，用 Rules 控制，见《[Codex Rules 命令规则](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)》。

## 常见问题

**团队能统一管吗？**
可以。企业管理员能在 `requirements.toml` 里定义 profile，并用 `allowed_permission_profiles` 限制成员能选哪些；一旦设了这个列表，没列出的 profile（包括内置的）都不能用。

**放行了域名，为什么 git clone 还是失败？**
先看报错是不是 403。有的域名会重定向到另一个域名（比如附件下载），要把重定向后的域名也加进来。

## 参考资料

- [Permissions（Codex 官方文档）](https://learn.chatgpt.com/docs/permissions)
- [Managed configuration：网络要求](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-network-access-requirements)

本文按 2026-11-11 的官方文档和 Codex CLI 0.165.0 实测。Permissions 功能目前是 Beta，键名和默认行为可能变化。
