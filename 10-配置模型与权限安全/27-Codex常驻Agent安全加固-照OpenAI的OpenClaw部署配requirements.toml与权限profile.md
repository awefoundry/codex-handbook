---
id: codex-persistent-agent-hardening
title: Codex 常驻 Agent 怎么上锁：照 OpenAI 内部 OpenClaw 部署配 requirements.toml、权限 profile 与 Auto-review
seo_title: Codex 常驻 Agent 安全加固：OpenClaw 的 requirements.toml 与权限配置
description: OpenAI 公开了内部 500 多个 OpenClaw 常驻 agent 的安全做法和 requirements.toml、config.toml 示例。本文逐行解读网络白名单、权限 profile、环境变量过滤和 Auto-review，并按现行官方文档标出可以再收紧的写法。
lede: 常驻 agent 没人盯着，安全不能靠「每次弹窗问人」。先用配置把能碰的范围锁死，再让 Auto-review 管剩下的审批。
url: /guides/codex-persistent-agent-hardening
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 27
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-13
date_modified: 2026-11-13
verified_on: 2026-11-13
official_ref: https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai
keywords: [Codex 常驻 agent, OpenClaw, requirements.toml, permission profile, Auto-review, network_proxy, experimental_network, shell_environment_policy, Codex 企业安全]
related: [permissions-sandbox-approvals, config-toml-guide, codex-access-tokens-service-accounts]
faq:
  - q: requirements.toml 和 config.toml 有什么区别？
    a: requirements.toml 是管理员下发的限制，规定哪些取值允许用；config.toml 是实际配置，选择具体用哪个值。config.toml 里的值和 requirements 冲突时，Codex 会退回到兼容的值并提示用户。
  - q: requirements.toml 放在哪里？
    a: 系统级文件在 Linux 和 macOS 上是 /etc/codex/requirements.toml，Windows 上是 %ProgramData%\OpenAI\Codex\requirements.toml；企业也可以通过云端 Agent security 或 macOS MDM 下发。
  - q: 博客里的 experimental_network 写法现在还能用吗？
    a: 能。Codex 0.166.0 起 network_proxy 是标准表名，experimental_network 仍被接受，官方文档还建议在所有客户端都支持新名字之前继续用 experimental_network。要注意的是 domains 映射不能和旧的 allowed_domains、denied_domains 列表混用。
  - q: 开了 Auto-review 还需要沙箱吗？
    a: 需要。Auto-review 只审查原本要停下来问人的请求，已经有权限的操作不会经过它。OpenAI 的做法是先用沙箱、网络白名单和凭据代理把边界定死，再对所有需要审批的动作强制 Auto-review。
---

# Codex 常驻 Agent 怎么上锁：照 OpenAI 内部 OpenClaw 部署配 requirements.toml、权限 profile 与 Auto-review

> 本文在线版：[codexguide.io/guides/codex-persistent-agent-hardening](https://codexguide.io/guides/codex-persistent-agent-hardening)

> 核对依据：OpenAI Developers 博客 [Securing persistent agents like OpenClaw at OpenAI](https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai)（2026-11-12）；官方文档 [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)、[Permissions](https://learn.chatgpt.com/docs/permissions)、[Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)。以上均于 2026-11-13 核对。文中 TOML 只做过语法解析检查，没有在受管设备上验证生效；本文没有截图。

2026-11-12，OpenAI 在开发者博客上讲了自己怎么在公司内部跑 OpenClaw 这类**常驻 agent**：它们 7×24 小时在后台运行，目标宽泛，会主动做事，不像普通 Codex 会话那样有固定任务、有人一路看着。博客说公司里已经有**超过 500 个**这样的 agent，在做根据产品反馈自动开 PR、持续跑数据实验之类的工作。

博客最有参考价值的是它附了两份真实配置：一份 `requirements.toml`，一份 `config.toml`。这篇文章逐段解读，再对照现行官方文档，标出哪些地方现在可以写得更规范、更严。

## 先看结论

如果你也要让 Codex 长时间无人值守地跑，按 OpenAI 的思路，至少做到这五件事：

1. **把可信部分和不可信部分分开**：负责网络、身份、沙箱的组件当成可信代码；agent、它的运行环境和它写的代码一律当成不可信。
2. **用 requirements.toml 锁住选项**：禁掉 `danger-full-access`，网页搜索只允许 `cached`，强制走受管网络代理并只放行白名单域名。
3. **用权限 profile 限定文件范围**：只允许写 agent 自己的工作目录，`~/.ssh` 这类目录直接 `deny`。
4. **密钥不进 agent 的视野**：环境变量里删掉 GitHub 令牌等凭据，真正的密钥交给凭据代理（credential broker）管理。
5. **对所有需要审批的动作强制 Auto-review**，并给每个 agent 单独的身份、完整记录日志。

## OpenAI 的五条原则

博客把做法归成五类，下面按原文顺序概括：

| 原则 | 博客里的做法 |
|---|---|
| 分开可信与不可信执行 | 在 OpenClaw 开源项目里实现远程 harness 执行，让 Gateway（负责配置 agent 的组件）和 agent harness 跑在不同容器里，OpenAI 内部甚至放在不同集群 |
| 强制硬性安全边界 | 网络：组织维护的白名单加明确拒绝列表；文件：只允许写 agent 工作目录；进程：用 Codex 的 Linux 沙箱隔离；密钥：通过凭据代理管理，agent 看不到 |
| 加上基于模型的防护 | 对所有 agent 动作强制 Auto-review，让另一个 agent 审查主 agent 的动作，把人的注意力留给高价值的审批 |
| 分开 agent 身份和用户身份 | 每个 agent 有独立身份，关联一个 ChatGPT 服务账号，有自己的推理凭据，可以单独审计、必要时直接停掉推理 |
| 全部可观测 | 控制面的每次配置变更和 agent 的每一轮对话都记日志；因为可能含敏感信息，日志只开放给安全团队里少数人 |

博客还提到一句容易被忽略的话：传统软件的威胁大多来自外部攻击者，而常驻 agent 可以改自己的配置、写任意代码，**风险也会从内部来**，也就是 agent 做出不符合预期的动作。

## requirements.toml：先把选项锁死

`requirements.toml` 是管理员下发的限制，规定 Codex 的哪些取值允许用。用户的 `config.toml`、profile 或命令行参数和它冲突时，Codex 会退回兼容的值并提示用户。系统级文件放在 Linux 和 macOS 的 `/etc/codex/requirements.toml`，Windows 的 `%ProgramData%\OpenAI\Codex\requirements.toml`。

博客里的版本如下（注释译成中文，域名按原文）：

```toml
# 不允许不受限制的 danger-full-access 沙箱模式
allowed_sandbox_modes = ["read-only", "workspace-write"]
# 允许缓存搜索，不允许实时搜索
allowed_web_search_modes = ["cached"]
# 强制使用受管网络代理
experimental_network.enabled = true
# 不允许用户级配置扩大域名白名单
experimental_network.managed_allowed_domains_only = true
# 只放行这些目标；换成你的工作负载实际需要的主机
experimental_network.allowed_domains = [
  "github.com",
  "api.github.com",
  "codeload.github.com",
]
# 明确拦截这些目标，包括云厂商的元数据地址
experimental_network.denied_domains = [
  "pastebin.com",
  "*.pastebin.com",
  "webhook.site",
  "metadata.google.internal",
  "169.254.169.254",
]
```

几处值得注意：

- **拦截云元数据地址**：`169.254.169.254` 和 `metadata.google.internal` 是云服务器上读取实例凭据的常见入口，agent 一旦能访问，就可能拿到机器的云权限。
- **拦截 pastebin、webhook.site**：这类服务常被用来把数据外传。
- **`managed_allowed_domains_only = true`**：用户自己加的允许规则、单次放行都不能扩大白名单。官方文档提醒，开了它就必须写管理员的允许条目，只有拒绝列表时不会放行其他任何网站。

## config.toml：权限 profile、网络和环境变量

博客的 `config.toml` 选了一个名为 `openclaw` 的权限 profile：

```toml
default_permissions = "openclaw"
web_search = "cached"

[permissions.openclaw.filesystem]
# 最小运行环境需要的系统和运行时路径，只读
":minimal" = "read"
# agent 工作目录，可读写
"/home/dev-user/openclaw-workspaces" = "write"
# 受管资料，只读
"/home/dev-user/read-only" = "read"
# 禁止访问 SSH 凭据
"/home/dev-user/.ssh" = "deny"

[permissions.openclaw.network]
enabled = true
allow_upstream_proxy = false
allow_local_binding = false
enable_socks5 = false
enable_socks5_udp = false
dangerously_allow_non_loopback_proxy = false
dangerously_allow_all_unix_sockets = false

[shell_environment_policy]
ignore_default_excludes = false
exclude = [
  "GH_TOKEN",
  "GITHUB_TOKEN",
  "OPENCLAW_GITHUB_BASIC_AUTH",
  "OPENCLAW_GITHUB_READONLY_BASIC_AUTH",
]

[apps._default]
enabled = false
destructive_enabled = false
open_world_enabled = false
```

对照 [Permissions](https://learn.chatgpt.com/docs/permissions) 文档的默认值，就能看出哪几行是在主动收紧：

| 字段 | 文档默认值 | 博客取值 | 作用 |
|---|---|---|---|
| `allow_upstream_proxy` | `true` | `false` | 不继承外部的 `HTTP(S)_PROXY`、`ALL_PROXY`，流量只走 Codex 自己的代理 |
| `enable_socks5` | `true` | `false` | 关掉 SOCKS5 监听 |
| `enable_socks5_udp` | `true` | `false` | 关掉 SOCKS5 UDP |
| `allow_local_binding` | `false` | `false` | 保持本地和内网地址防护，`localhost` 要显式放行，解析到内网 IP 的域名仍被拦 |
| `dangerously_allow_non_loopback_proxy` | `false` | `false` | 代理只监听本机回环地址 |
| `dangerously_allow_all_unix_sockets` | `false` | `false` | 不放开所有 Unix socket |

另外两段：

- **`ignore_default_excludes = false`**：这个字段默认是 `true`，也就是 Codex 默认**不会**自动删掉名字里带 `KEY`、`SECRET`、`TOKEN` 的环境变量。设成 `false` 才会先做这层自动过滤，再执行下面的 `exclude`。博客原文注释也提醒：这只能让命令的环境变量里看不到凭据，**存在 agent 能读到的文件里的凭据照样可见**。
- **`[apps._default]`**：默认关掉所有应用（连接器），并且默认禁止带「破坏性」和「开放世界」标记的应用工具，需要哪个再单独打开。

## 按现行文档，还可以再收紧的四处

博客的配置能直接用，但对照 2026-11-13 的官方文档，有几处可以写得更规范：

**1. 网络表：用 `domains` 映射，但先保留旧表名。** Codex 0.166.0 起，`[network_proxy]` 是 requirements.toml 里受管网络的标准表名，`[experimental_network]` 仍被接受。官方文档建议在所有客户端和策略校验工具都支持新名字之前，**继续发布 `[experimental_network]`**。规则写法上，新的 `domains` 映射是标准写法，不能和旧的 `allowed_domains`、`denied_domains` 列表混用。改写后是这样：

```toml
[experimental_network]
enabled = true
managed_allowed_domains_only = true

[experimental_network.domains]
"github.com" = "allow"
"api.github.com" = "allow"
"codeload.github.com" = "allow"
"**.pastebin.com" = "deny"
"webhook.site" = "deny"
"metadata.google.internal" = "deny"
"169.254.169.254" = "deny"
```

`*.example.com` 只匹配子域名，`**.example.com` 同时匹配主域名和子域名，所以博客里分开写的 `pastebin.com` 和 `*.pastebin.com` 可以合成一条 `**.pastebin.com`。同一个目标同时命中允许和拒绝时，拒绝优先。

**2. 用权限 profile 白名单代替 `allowed_sandbox_modes`。** 官方文档写明，Codex 0.138.0 及以上推荐用 `allowed_permission_profiles` 加受管的 `default_permissions`，`allowed_sandbox_modes` 只留给还在用 `sandbox_mode` 的旧部署。0.137.0 及更早的版本会忽略这两个字段，所以要等所有客户端升级完再切换。自定义 profile 最好也定义在 requirements 里，由管理员统一控制：

```toml
default_permissions = "agent_workspace"

[allowed_permission_profiles]
agent_workspace = true
# 没有列出的 profile（包括 ":danger-full-access"）一律不允许

[permissions.agent_workspace]
description = "常驻 agent：只能写自己的工作目录"
extends = ":workspace"
```

白名单一旦存在，就是允许的完整清单：没写或写成 `false` 的 profile 都不能选，以后新版本新增的内置 profile 也一样。自定义名字不能以 `:` 开头，也不能叫 `filesystem`。

**3. 把 Auto-review 写成强制要求。** 博客说对所有动作强制 Auto-review，但没贴这部分配置。官方文档给的写法是：

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]
```

如果还想保留人工审批，就在 `allowed_approvals_reviewers` 里加上 `"user"`。要整体替换审查规则，用受管的 `guardian_policy_config`，它优先于本地 `[auto_review].policy`。

**4. 环境变量过滤改用 `filters`。** `exclude` 和 `include_only` 数组是旧写法，仍然支持；新配置推荐 `[shell_environment_policy.filters]`，模式不区分大小写，支持 `*` 和 `?`。两种写法**不能放在同一层配置里**，Codex 会直接拒绝：

```toml
[shell_environment_policy]
ignore_default_excludes = false

[shell_environment_policy.filters]
"GH_TOKEN" = "exclude"
"GITHUB_TOKEN" = "exclude"
"OPENCLAW_GITHUB_*" = "exclude"
```

## Auto-review 拦不住的，和网络代理管不到的

两条边界要心里有数：

- **Auto-review 只看原本要停下来问人的请求**：提权的命令、命中 `decision = "prompt"` 规则的命令、需要审批的网络请求、写到可写目录外的文件、需要审批的 MCP 或应用工具调用。已经有权限的操作直接执行，不经过它。所以先用沙箱把权限收窄，Auto-review 才有意义。
- **Auto-review 有停止机制**：大多数模型下，CLI 在同一轮里连续被拒 3 次，或最近 50 次审查里被拒 10 次，就会中断这一轮；网络安全类模型第一次被拒就停。被拒的动作可以在 TUI 里用 `/approve` 选一条放行重试一次，重试仍要再过一遍 Auto-review。
- **受管网络代理只管沙箱里跑的命令**：它不过滤网页搜索、应用和连接器、MCP 服务器、桌面应用自身的流量，也不过滤 Codex 自己的服务请求。这就是博客要另外写 `allowed_web_search_modes = ["cached"]` 和 `[apps._default] enabled = false` 的原因。官方文档还提醒，被批准的完全提权可以绕过受管代理，要单独测试。

## 上线前怎么验证

官方文档对网络规则的建议是：每个执行环境都测一个**应该成功**的请求和一个**应该被拦**的请求。照这个思路，上线前至少确认：

1. 在 agent 里访问白名单域名（如 `api.github.com`）成功，访问 `169.254.169.254` 被拦。
2. 让 agent 尝试读 `~/.ssh` 或写工作目录之外的文件，确认被拒。
3. 在 agent 的命令里打印环境变量，确认 `GH_TOKEN`、`GITHUB_TOKEN` 不在里面。
4. 用户在自己的 `config.toml` 里改 `sandbox_mode = "danger-full-access"` 或开实时搜索，确认 Codex 退回到允许的值并给出提示。
5. Windows 上要特别测：官方文档写明受管网络在 Windows 上的支持有限。

## 关于 OpenClaw Enterprise

博客最后提到，OpenAI 在 DevDay 上发布了 **OpenClaw Enterprise（OCE）**，一个开源、不绑定厂商的 agent 控制面。用 OCE 的标准 Codex 预设启动 agent，就能带上文中的很多防护。博客写明 OCE 还在试点阶段，计划年底前发 1.0。

## 延伸阅读

- [权限、沙箱与审批：什么时候放行，什么时候收紧](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [Codex config.toml 深入配置：字段覆盖关系与排查方法](./04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
- [Codex 访问令牌与服务账号：CI 和定时任务免浏览器登录](../11-自动化与高级工作流/14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)
