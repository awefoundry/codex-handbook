---
id: codex-doctor
title: Codex doctor 自检：一条命令排查安装、配置、登录和网络问题
seo_title: Codex doctor 自检：排查安装、配置、登录和网络问题
description: codex doctor 一条命令检查 Codex 的安装、配置、登录、运行环境、Git、终端、网络和后台服务。本文用 Codex CLI 0.164.0 实测完整输出、--summary 和 --json 的用法，逐项解读 ✗ 和 ⚠ 怎么处理，以及反馈问题前该附什么。
url: /guides/codex-doctor
status: published
section: guides
category: K-troubleshooting
topic: 故障排查与恢复
content_type: 排障
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 入门
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-26
date_modified: 2026-10-26
verified_on: 2026-10-26
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/developer-commands?surface=cli
keywords: [codex doctor, Codex 自检, Codex 诊断, Codex 登录失败, Codex WebSocket, Codex 安装问题, Codex 排查]
faq:
  - q: codex doctor 会自动修复问题吗？
    a: 它的用途是生成诊断报告，不会帮你登录，也不会自动修复配置。按输出里的提示自己处理后，再运行一次确认。
  - q: codex doctor 的退出码是什么意思？
    a: 实测 0.164.0 中，有检查项失败（✗）时退出码是 1；只有警告（⚠）没有失败时退出码是 0。脚本里可以用退出码判断是否有阻断问题。
  - q: 提示 Responses WebSocket failed 是不是就用不了？
    a: 不一定。这一项只是警告，提示里写明 HTTPS 回退仍可能可用。先看下面 reachability 一项是否通过，再检查代理、VPN、防火墙和 WebSocket 策略。
  - q: 用 --json 导出的报告可以直接发给别人吗？
    a: 官方帮助称它是脱敏报告，实测接口地址会被替换成 <redacted>，但本地文件路径仍然保留。路径里有用户名时，发出去之前自己再检查一遍。
---

# Codex doctor 自检：一条命令排查安装、配置、登录和网络问题

> 本文在线版：[codexguide.io/guides/codex-doctor](https://codexguide.io/guides/codex-doctor)

> 核对依据：OpenAI 官方文档 [Command line options](https://learn.chatgpt.com/docs/developer-commands?surface=cli) 中的 `codex doctor` 一节、`codex doctor --help`，以及 [Codex 更新日志](https://learn.chatgpt.com/docs/changelog) 中关于 doctor 的条目。实测环境是 Linux（Debian 13）上通过 npm 安装的 `codex-cli 0.164.0`，在**未登录**状态下运行了 `codex doctor`、`--summary`、`--json`，并用一个无效的测试 API key 对比了登录检查的变化。核对日期 2026-10-26。

Codex 打不开、登录不上、一直重连、MCP 不工作时，先别急着重装。`codex doctor` 会把安装、配置、登录、运行环境、Git、终端、网络和后台服务挨个检查一遍，告诉你哪一项有问题、下一步该查什么。官方文档的说法是：在提交问题反馈之前，或排查一个坏掉的 Codex 安装时，用它生成一份本地诊断报告。

## 怎么运行

```bash
codex doctor
```

它的用途是生成诊断报告：告诉你哪里有问题、建议怎么处理，但不会帮你登录，也不会自动修复配置。

常用参数（来自 `codex doctor --help`）：

| 参数 | 作用 |
|---|---|
| `--summary` | 只显示每项检查一行的分组摘要和最后的统计 |
| `--all` | 展开详细输出里被截断的长列表 |
| `--json` | 输出脱敏后的机器可读报告 |
| `--no-color` | 不用彩色输出 |
| `--ascii` | 用 ASCII 字符显示状态和分隔线 |

如果你装了多个 Codex（比如 npm 一份、Homebrew 一份），先用 `which codex` 和 `codex --version` 确认运行的是哪一个，doctor 检查的是当前这一个。

## 先看摘要：codex doctor --summary

下面是在一台**没登录**的 Linux 测试机上用 `--summary --ascii` 运行的真实输出（安装路径较长，省略中间部分）：

```text
Codex Doctor v0.164.0 · linux-x86_64

Notes
   [XX] auth         no Codex credentials were found - Run codex login or provide an API key through a supported auth env var.
   [!!] websocket    Responses WebSocket failed; HTTPS fallback may still work - Check proxy, VPN, firewall, DNS, custom CA, and WebSocket policy support.
   [!!] terminal     TERM=dumb - colors and cursor control are disabled in this non-interactive run
-------------------------------------------------------------

Environment
  [ok] system       C
  [ok] disk         sufficient free disk space (80.9 GiB)
  [ok] security     endpoint protection is not inspected on this platform
  [ok] runtime      npm (package …)
  [ok] install      consistent
  [ok] search       file exists (bundled, `…/codex-path/rg`)
  [ok] git          git executable found; execution not verified
  [!!] terminal     TERM=dumb - colors and cursor control are disabled in this non-interactive run
  [ok] title        default | project tmp
  [ok] state        state paths and databases are inspectable
  [ok] threads      no rollout/state DB inventory to compare

Configuration
  [ok] config       loaded
  [XX] auth         no Codex credentials were found - Run codex login or provide an API key through a supported auth env var.
  [ok] mcp          1 server (1 stdio) · 0 disabled
  [ok] sandbox      restricted fs + restricted network · approval OnRequest
  [ok] sandbox      no explicit filesystem paths to probe

Updates
  [ok] updates      update configuration is locally consistent

Connectivity
  [ok] network      no proxy env vars
  [!!] websocket    Responses WebSocket failed; HTTPS fallback may still work - Check proxy, VPN, firewall, DNS, custom CA, and WebSocket policy support.
  [ok] reachability active provider endpoints are reachable over HTTP

Background Server
  [--] app-server   not running (ephemeral mode)

-------------------------------------------------------------
17 ok | 1 idle | 3 notes | 2 warn | 1 fail failed
```

怎么读：

- **最上面的 Notes** 把所有不是 ok 的项集中列出来，后面的分组里会再出现一次。先看这里就知道要处理什么。
- **状态标记**：默认输出里是 `✓`（正常）、`⚠`（警告）、`✗`（失败）、`○`（空闲，比如后台服务没运行）；加 `--ascii` 后分别显示为 `[ok]`、`[!!]`、`[XX]`、`[--]`。
- **最后一行**是统计。这次是 17 项正常、1 项空闲、2 项警告、1 项失败，`3 notes` 就是 Notes 里列出的 3 条。
- **退出码**：这次有一项失败，退出码是 1。用无效的测试 key 让登录检查通过后（只剩警告），退出码变成 0。

## 每个分组检查什么

| 分组 | 检查项 | 主要看什么 |
|---|---|---|
| Environment | system、disk、security、runtime、install、search、git、terminal、title、state、threads | 系统和语言环境、磁盘剩余空间、安装方式和版本是否一致、自带的 `rg` 搜索工具、Git、终端能力、本地数据库和会话记录 |
| Configuration | config、auth、mcp、sandbox | `config.toml` 能否解析、有没有登录凭据、MCP 服务器数量、沙箱和审批策略 |
| Updates | updates | 更新检查配置、最新版本、更新命令 |
| Connectivity | network、websocket、reachability | 代理环境变量、WebSocket 连接、HTTP 能否访问模型接口 |
| Background Server | app-server | 共享后台服务是否在运行 |

不加 `--summary` 时，每项下面会展开详情。几个排查时最有用的字段（本次实测输出）：

```text
  ✓ disk         sufficient free disk space (80.9 GiB)
      warning threshold        5.0 GiB
      failure threshold        1.0 GiB
...
  ✓ config       loaded
      model                    <default> · openai
      config.toml parse        ok
      MCP servers              1
      feature flags            62 enabled · 0 overridden (full list with --all)
      configured TUI mode      fullscreen
...
  ✓ updates      update configuration is locally consistent
      startup update check     true
      update action            npm install -g @openai/codex
      latest version           0.164.0
      latest version status    current version is not older
```

- 磁盘剩余空间低于 5 GiB 会警告，低于 1 GiB 会判定失败。
- `config.toml parse` 不是 `ok` 时，说明配置文件有语法错误，先修它。字段之间的覆盖关系见 [config.toml 深入配置](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。
- `update action` 会告诉你按当前安装方式该用哪条命令更新，不用猜是 npm 还是 Homebrew。

## 常见警告和失败怎么处理

### ✗ auth：no Codex credentials were found

没有找到登录凭据。按提示运行 `codex login`，或者通过受支持的环境变量提供 API key。登录方式见 [Codex 安装登录常见问题](../01-安装与首次使用/13-安装登录常见问题.md)。

要注意：这一项只检查**有没有**凭据，不验证凭据**能不能用**。实测把 `OPENAI_API_KEY` 设成一个无效的测试值后，auth 一项变成：

```text
auth.credentials  ok  auth is provided by environment
```

所以 auth 显示正常、但 Codex 仍然报 401 或登录失效时，问题可能出在凭据本身（过期、被撤销、选错账号），需要重新登录。

### ⚠ websocket：Responses WebSocket failed; HTTPS fallback may still work

这一项检查 Codex 能否用 WebSocket 连上模型接口。它是警告不是失败：提示里写明 WebSocket 失败时，HTTPS 回退可能仍然可用。

处理顺序：

1. 看同组的 `reachability` 一项。它通过（`active provider endpoints are reachable over HTTP`）说明 HTTP 能连通，Codex 大概率还能用，只是连接方式退回了 HTTPS。
2. 看详情里的 `handshake transport error`。本次实测是 `http 401 Unauthorized`，原因是测试机没登录、请求没带凭据；登录后再测。
3. 如果是超时、TLS 错误或连接被重置，按提示检查代理、VPN、防火墙、DNS、自定义 CA 证书，以及公司网络是否允许 WebSocket。

### ⚠ terminal：TERM=dumb

终端不支持颜色和光标控制。在脚本、CI 或某些编辑器的内置输出面板里运行时常见，对 `codex exec` 这类非交互运行没有影响。如果你是在正常的终端里运行交互界面时看到它，检查 `TERM` 环境变量是否被设成了 `dumb`。

### ○ app-server：not running

共享后台服务没有运行，显示为空闲而不是失败。只用 CLI 时通常不需要它。

### 其他几项

- **install 不是 consistent**：可能装了多份 Codex，或者安装目录不完整。用 `which -a codex` 查看所有安装位置，保留一份。卸载和重装见 [Codex 更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。
- **state 报错**：本地 SQLite 数据库有问题。官方更新日志记录，2026-09-25 起 doctor 会在输出里标出损坏的 SQLite 数据库。
- **network 显示了代理变量**：确认 `HTTPS_PROXY` 等变量指向的代理确实可用。

## 用 --json 做脚本检查

```bash
codex doctor --json > doctor.json
```

报告顶层有 `schemaVersion`、`overallStatus`、`codexVersion` 和 `checks` 等字段。`checks` 里每一项有 `id`、`category`、`status`、`summary`、`details` 和 `remediation`（修复建议）。

只看不正常的项（需要先装 `jq`）：

```bash
jq -r '.checks | to_entries[] | select(.value.status != "ok") | "\(.key)\t\(.value.status)\t\(.value.summary)"' doctor.json
```

本次实测输出：

```text
auth.credentials	fail	no Codex credentials were found
network.websocket_reachability	warning	Responses WebSocket failed; HTTPS fallback may still work
terminal.env	warning	TERM=dumb - colors and cursor control are disabled in this non-interactive run
```

`overallStatus` 这次是 `fail`；用测试 key 让 auth 通过后变成 `warning`。在 CI 里可以据此判断环境能不能跑 Codex。

注意两点：

- JSON 里后台服务一项的状态是 `ok`（摘要是 `background server is not running`），不是人类可读输出里的“空闲”。
- `--json` 会把接口地址替换成 `<redacted>`，但 `CODEX_HOME`、`auth.json` 等本地路径照常保留。路径里有用户名时，贴到公开的 issue 前自己处理一下。

## 反馈问题前附什么

1. `codex --version` 的输出。
2. `codex doctor --summary` 的输出，或者 `--json` 报告（检查过本地路径）。
3. 出问题时你在做什么、在哪个入口（CLI、桌面端、IDE 扩展）。

不要附 `auth.json` 或任何 API key。

## doctor 最近加了哪些检查

根据官方更新日志：

- 0.149.0（2026-08-20）：新增终端安全软件、网络和代理故障、桌面端状态、更新连通性的诊断。
- 2026-09-25：标出损坏的 SQLite 数据库。
- 2026-10-08：报告配置的终端界面模式（就是上面详情里的 `configured TUI mode`）。
- 2026-10-23：存储统计里计入压缩过的会话记录。

不同版本的检查项会有差异。输出和本文不一样时，先运行 `codex update` 或按 `update action` 提示更新，再对照。

## 小结

- 出问题先跑 `codex doctor --summary`，从最上面的 Notes 开始处理，处理完再跑一次确认。
- ✗ 是要先修的问题，⚠ 不一定影响使用；退出码 1 表示有失败项。
- auth 正常不等于凭据有效；websocket 警告要结合 reachability 一起看。
- 想快速查某个子命令怎么写，见 [Codex CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。
