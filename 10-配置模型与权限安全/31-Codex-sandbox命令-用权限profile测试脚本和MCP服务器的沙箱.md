---
id: codex-sandbox-command
title: Codex sandbox 命令：用权限 profile 在沙箱里试跑任意命令，验证 profile 拦不拦得住，并给 MCP 服务器套上沙箱
seo_title: codex sandbox：用 -P 和 -C 验证权限 profile，并给 MCP 套沙箱
description: codex sandbox 能在你定义的权限 profile 下运行任意命令，用来验证沙箱到底拦不拦得住。本文按官方文章讲清 -P 与 -C 的用法，演示 .vscode 写入被拦的验证方法，并给 stdio MCP 服务器套沙箱。
lede: 先用一条会被拦住的命令证明 profile 生效，再把它套到你自己的脚本或 MCP 启动命令上。
url: /guides/codex-sandbox-command
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 31
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-21
date_modified: 2026-11-21
verified_on: 2026-11-21
tested_cli_version: 0.171.0
official_ref: https://openai.com/index/inside-the-codex-sandbox
keywords: [codex sandbox, Codex 沙箱命令, --permission-profile, Codex 权限 profile 测试, sandbox MCP 服务器]
related: [codex-sandbox-how-it-works, mcp-getting-started, codex-cli-commands-cheatsheet, codex-network-permissions-proxy]
faq:
  - q: 不写 -P 时，codex sandbox 是不是就用 :workspace？
    a: 不是。2026-11-21 在 Codex CLI 0.171.0、空的 config.toml 上，不带 -P 时 echo 能成功，但在当前目录写文件会被 Read-only file system 拒绝，创建 TCP socket 得到 Operation not permitted。显式加上 -P :workspace 之后，工作区里的普通文件可以写。把 default_permissions 写成某个 profile 之后，不带 -P 才会用那一份。
  - q: 为什么加上 -C 就要求必须写 -P？
    a: 0.171.0 的实际行为是这样。只写 codex sandbox -C <目录> -- echo hi 会退出码 2，并提示必须提供 --permission-profile。帮助里的 -C 说明是：这个目录用于解析 profile，也是命令的工作目录。
  - q: --sandbox-state-disable-network 能不能单独关掉网络？
    a: 不能单独加。0.171.0 上如果不带 --sandbox-state-json，命令退出码 2，用法行要求两者一起出现。帮助写明那份 JSON 来自 codex/sandbox-state，是不透明值。本文没有官方样例，没有编造 JSON。
---

# Codex sandbox 命令：用权限 profile 在沙箱里试跑任意命令，验证 profile 拦不拦得住，并给 MCP 服务器套上沙箱

> 核对依据：OpenAI 博客 [Inside the Codex sandbox](https://openai.com/index/inside-the-codex-sandbox) 的 “Using the `codex sandbox` command” 与 “Example: sandboxing an MCP server”（2026-11-21 对照原文 HTML，补上渲染成 Markdown 时丢掉的 `"--"`）。字段名对照 [Permissions](https://learn.chatgpt.com/docs/permissions)。实测：Linux，`codex-cli 0.171.0`，独立的 `CODEX_HOME`，未登录，没有打开 TUI。系统里没有 `bwrap` 命令。macOS 上博客给出的报错原文是 `Operation not permitted`；**本站环境是 Linux**，同一步得到的是 `Read-only file system`。用户名路径已改成 `$LAB` 或 `/home/<用户名>`。

profile 为什么默认这样定、三个系统各自靠什么执行，见 [Codex 沙箱怎么工作](./30-Codex沙箱怎么工作-拆解OpenAI官方文章-workspace权限profile与三系统实现.md)。本文只做一件事：用 `codex sandbox` 把一份 profile 跑出「拦住」和「放行」。

## 先说结论：codex sandbox 是测试 profile 和复用沙箱的入口

`codex sandbox` 在 Codex 配置里的权限 profile 下运行任意命令。博客写了两个用途：确认沙箱真的挡住了你想挡的行为；让你自己的工具借用同一套沙箱，而不必先开一轮智能体会话。

0.171.0 的 `codex sandbox --help` 把命令说成 “Run commands within a Codex-provided sandbox”。和本文有关的参数是：

| 参数 | 帮助里的作用 |
|---|---|
| `-P, --permission-profile <NAME>` | 从当前配置栈里选用这份具名 profile |
| `-C, --cd <DIR>` | 解析 profile 和执行命令时用的工作目录 |
| `-c, --config <key=value>` | 覆盖本来会从 `~/.codex/config.toml` 读到的配置，值按 TOML 解析 |
| `-p, --profile <CONFIG_PROFILE>` | 在基础用户配置之上再叠 `$CODEX_HOME/<name>.config.toml` |
| `--include-managed-config` | 解析一份显式 profile 时把托管要求也算进去 |
| `--enable` / `--disable <FEATURE>` | 等价于 `-c features.<name>=true` 或 `false` |
| `--sandbox-state-json <JSON>` | 直接套用一份来自 `codex/sandbox-state` 的不透明 JSON |
| `--sandbox-state-disable-network` | 在这份 sandbox state 里关闭直接网络 |
| `--sandbox-state-readable-root` | 给这份 sandbox state 再加一个可读根，可重复 |
| `--transparent-tcp` | 把出站 TCP 转到托管的 SOCKS 代理 |

子命令 `uninstall` 的帮助写的是：移除旧版 Windows 沙箱的机器级账号和网络规则。本文在 Linux 上没有运行它。

命令和参数之间写 `--`。`-C` 和 `-P` 要放在 `--` 前面。

## 最小例子：空配置下先看默认行为，再显式使用 :workspace

下面的 `$LAB` 是一块实验目录，里面有 `codex-home` 和 `work`。`work` 里预先放了 `src/a.txt`、`.git/` 和 `.vscode/`。`CODEX_HOME` 不要放在 `/tmp` 下面：本文第一次把 `CODEX_HOME` 放进 `/tmp` 时，Codex 打印 `Refusing to create helper binaries under temporary dir "/tmp"`，然后仍然继续。后面的输出都来自家目录下的 `CODEX_HOME`，没有这条警告。

空的 `config.toml`、不带 `-P`：

```text
$ codex sandbox -- echo hi
hi
```

退出码 0。同一条件下，在当前项目目录里写文件会被拒绝，`codex sandbox` 的退出码是 1：

```text
$ cd "$LAB/work"
$ codex sandbox -- bash -c 'echo def > src/default-nop.txt'
bash: line 1: src/default-nop.txt: Read-only file system
```

创建 TCP socket 同样失败，退出码 1：

```text
$ codex sandbox -- python3 -c 'import socket; s=socket.socket(); s.settimeout(3); s.connect(("1.1.1.1", 443))'
PermissionError: [Errno 1] Operation not permitted
```

沙箱外面，同一条 Python 能连上并打印 `connected`。所以这不是机器本身没有网络。

这**不是** `:workspace`。显式写上 `-P :workspace` 之后，工作区里的普通文件可以写，退出码 0：

```text
$ codex sandbox -C "$LAB/work" -P :workspace -- bash -c 'echo ok > src/from-sandbox.txt'
```

`.git` 仍然只读，退出码 1：

```text
$ codex sandbox -C "$LAB/work" -P :workspace -- bash -c 'echo x > .git/codex-test'
bash: line 1: .git/codex-test: Read-only file system
```

工作区外面的文件也只读。当时的报错是 `Read-only file system`，文件没有被创建。联网仍是 `Operation not permitted`。另外，沙箱外 `curl https://example.com` 返回 200；`-P :workspace` 里的 `curl` 得到 `Could not resolve host: example.com`。本文把 Python 的 `Operation not permitted` 当作「网络被沙箱拒绝」的证据，`curl` 只作旁证。

只写 `-C`、不写 `-P`，0.171.0 直接拒绝，退出码 2：

```text
error: the following required arguments were not provided:
  --permission-profile <NAME>

Usage: codex sandbox --permission-profile <NAME> --cd <DIR> <COMMAND>...
```

速查表里还有一条更早的「默认策略下写 `/etc` 被拒绝」。那是 0.169.0 的记录，见 [CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。本文换了工作区内外和 `.git`，不重复那一条。

## 写一个 dev profile：filesystem 与 network 条目

字段名先对照 Permissions 页，再按博客的 `dev` 示例写。博客用的是 `"~/build-cache" = "write"`。本文实测把这一条换成实验目录里的绝对路径，避免写进真实的家目录缓存。其余条目与博客相同：

```toml
default_permissions = "dev"

[permissions.dev]
description = "Development with extra read-only protections."
extends = ":workspace"

[permissions.dev.filesystem]
"/home/<用户名>/codex-ag3-lab/build-cache" = "write"

[permissions.dev.filesystem.":workspace_roots"]
".devcontainer" = "read"
".vscode" = "read"
"**/*.env" = "deny"
"secrets" = "deny"
```

这份文件放在 `$CODEX_HOME/config.toml`。没有另开 `network.enabled`，所以它继续继承 `:workspace` 的默认：网络关闭。Permissions 页写 `extends = ":workspace"` 时，`.git`、`.agents`、`.codex`、`.aws` 保持只读，除非你覆盖。这里没有覆盖它们。

`read`、`write`、`deny` 的含义以 Permissions 页为准：`read` 不能创建、修改、重命名或删除；`write` 在操作系统允许时可以；`deny` 读和写都拒绝，用来从更宽的授权里挖掉一块。

## 用 -P 和 -C 验证：.vscode 写入被拦，普通文件和 build-cache 可以写

博客的验证命令是往已经存在的 `.vscode/settings.json` 里写入一份会在保存时调用恶意格式化器的配置。原文（macOS）：

```bash
codex sandbox --permission-profile dev -- \
  bash -c 'cat > .vscode/settings.json' <<'JSON'
{
  "prettier.prettierPath": "./node_modules/evil-prettier",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
JSON
```

博客写，macOS 上失败原文是：

```text
bash: .vscode/settings.json: Operation not permitted
```

**这行是官方文章写的。本站是 Linux，没有复现 macOS 的这句英文。** 本文用一条更短的写入，确认同一条规则。`.vscode` 事先存在，里面已有 `settings.json`：

```text
$ codex sandbox -P dev -C "$LAB/work" -- bash -c 'printf "%s\n" "{\"x\":1}" > .vscode/settings.json'
bash: line 1: .vscode/settings.json: Read-only file system
```

退出码 1。文件内容仍是原来的 `old`，没有被改掉。

同一 profile 下，对照结果是：

| 动作 | 结果 | 退出码 |
|---|---|---|
| 写 `src/dev.txt` | 成功 | 0 |
| 写 `.vscode/settings.json` | `Read-only file system` | 1 |
| 写 `.devcontainer/devcontainer.json` | `Read-only file system` | 1 |
| 读 `.devcontainer/devcontainer.json` | 打出原来的内容 | 0 |
| 写 `.env` | `Read-only file system` | 1 |
| 读 `.env` | `Permission denied` | 1 |
| 写 `secrets/token.txt` | `Permission denied` | 1 |
| 读 `secrets/token.txt` | `Permission denied` | 1 |
| 写实验目录里的 `build-cache/a.txt` | 成功 | 0 |
| `socket.connect(("1.1.1.1", 443))` | `Operation not permitted` | 1 |

`.env` 的写入和读取报错不一样。不要据此认为「只读所以还能读」：读取同样失败了。`secrets` 这一条从写入起就是 `Permission denied`。本文只记录 Linux 上看到的字符串，不把差异解释成另一套规则。

配好 `default_permissions = "dev"` 之后，不带 `-P` 也会用到 `dev`：写 `src/via-default.txt` 成功，写 `.vscode/via-default.json` 被 `Read-only file system` 拒绝。`-P` 是点名；默认名字来自配置，不是来自「不写参数就等于 :workspace」。

`--include-managed-config` 在这台没有托管要求的机器上被接受，工作区写入仍然成功，没有额外报错。本文没有一份 `requirements.toml`，不能把这个结果写成「它会收紧策略」或「它什么都不做」。

## 给 stdio MCP 服务器套沙箱：官方 memory 服务器示例

**这一节引自官方文章，本站没有安装 `@modelcontextprotocol/server-memory`，也没有把下面的配置接进一次真实会话。**

博客写得很明确：对 `config.toml` 里的 stdio MCP 服务器，harness **不会**去沙箱化用来启动服务器的那条命令。Codex 无法可靠推断这个服务器需要哪些文件或网络，套一份默认 profile 可能把本来合法的配置弄坏。

官方先给出不套沙箱的写法：

```toml
[mcp_servers.memory]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-memory@1.0.0"]

[mcp_servers.memory.env]
MEMORY_FILE_PATH = "~/mcp-data/memory.jsonl"
```

这条 `npx` 与运行 Codex 的用户权限相同，能写文件，也能联网。博客认为这过宽。收紧的办法是另写一份 `memory-mcp`，再用 `codex sandbox` 包住原来的 `npx`。原文参数里有一个单独的 `"--"`，2026-11-21 对照博客 HTML 确认它在 `"memory-mcp"` 和 `"npx"` 之间：

```toml
[permissions.memory-mcp.filesystem]
":root" = "read"
"~/.npm" = "write"
"~/mcp-data" = "write"

[permissions.memory-mcp.network]
enabled = false

[mcp_servers.memory]
command = "codex"
args = [
  "sandbox",
  "--permission-profile",
  "memory-mcp",
  "--",
  "npx",
  "--offline",
  "@modelcontextprotocol/server-memory@1.0.0"
]

[mcp_servers.memory.env]
MEMORY_FILE_PATH = "~/mcp-data/memory.jsonl"
```

博客要求在启动前先做两件事，因为沙箱可以往数据目录里写，但不能创建这个目录；安装包本身需要网络：

```bash
mkdir -p ~/mcp-data
npx -y --package=@modelcontextprotocol/server-memory@1.0.0 -c true
```

缓存好之后，`npx --offline` 才能在关闭网络的 profile 里启动。写入被限制在 npm 缓存和服务器自己的数据目录。

什么时候值得这么做：这个 stdio 进程的权限其实就是你的用户权限，而它要碰的目录你说得清楚。什么时候先别套：你还不知道它要读哪些路径。博客的理由就是这个——猜一份默认 profile，可能直接把服务器弄坏。MCP 配置本身怎么写，见 [MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 常用参数各自做什么，以及这次没能单独测出的效果

`-P` 和 `-C` 上面已经跑过。`-c` 可以临时覆盖配置，不必先改文件；本文的 profile 写在实验用的 `CODEX_HOME` 里，没有再用 `-c` 叠一层。`-p` 会再加载 `$CODEX_HOME/<名字>.config.toml`。本文没有准备那份文件，没有跑 `-p`。

`--enable` 和 `--disable` 按帮助等价于改 `features.<name>`。本文没有用它们打开 `network_proxy`。要验证域名白名单，仍以 [网络权限](./26-Codex网络权限-network_proxy域名白名单与本地服务访问.md) 里已经做过的 `curl` 为准，不在这里换一组域名重测。

`--sandbox-state-disable-network` 单独使用时，0.171.0 退出码 2：

```text
error: the following required arguments were not provided:
  --sandbox-state-json <JSON>

Usage: codex sandbox --sandbox-state-json <JSON> --sandbox-state-disable-network <COMMAND>...
```

帮助写：JSON 是来自 `codex/sandbox-state` 的不透明值，这个开关在那份 state 里关闭直接网络。官方博客和 Permissions 页都没有给出一份可以抄的 JSON。本文没有编造。把它和 `-P :workspace` 写在一起时，建 socket 仍然是 `Operation not permitted`；因为 `:workspace` 本来就关网络，这个结果不能算作该参数自己的效果。`--sandbox-state-readable-root` 和 `--transparent-tcp` 同样没有官方示例可跟，本文没有跑。

## 三个系统上的差异与常见报错

博客写，`codex sandbox` 默认把当前工作目录当作一个工作区根。所以 `.vscode` 这种相对工作区根的规则，要在那个目录里测，或者用 `-C` 指过去。

| 现象 | 本文在 Linux 0.171.0 上看到的 | 官方文章里的对应说法 |
|---|---|---|
| 写被标成只读的 `.vscode/settings.json` | `Read-only file system`，退出码 1 | macOS 上是 `Operation not permitted`。那句只属于 macOS |
| 空配置、不写 `-P`，写当前目录的文件 | `Read-only file system` | 博客没有把「不写 `-P`」定义成 `:workspace`。本文也不这么写 |
| 只写 `-C` | 退出码 2，要求 `-P` | 博客的示例同时写了 profile 和命令 |
| `PATH` 上没有 `bwrap` | 限制仍然生效 | 博客写 Codex 自带 `bwrap`，`PATH` 上有兼容版本时优先用系统的。本文没有核对实际是哪一个二进制 |
| 需要用户命名空间但系统禁止 | 本文没有碰到这条失败 | 博客写有些发行版默认禁止用户命名空间，只放行系统 `bwrap`。Permissions 页写：主机如果挡住 bubblewrap 需要的操作，这些策略就跑不起来 |

Windows 的 `codex sandbox uninstall` 只按帮助转述：先停掉使用旧沙箱的程序；如果装了 provisioning 服务，也先停掉；再以管理员运行。它移除机器级账号和网络规则，保留 Codex home。本文没有 Windows 机器，没有执行。

Seatbelt、bubblewrap 和 MXC 各自怎么把同一份 profile 变成内核限制，见 [沙箱怎么工作](./30-Codex沙箱怎么工作-拆解OpenAI官方文章-workspace权限profile与三系统实现.md)。那篇里的 macOS 和 Windows 细节同样是引自官方文章。

## 参考资料

- [Inside the Codex sandbox](https://openai.com/index/inside-the-codex-sandbox)（2026-11-18）
- [Permissions](https://learn.chatgpt.com/docs/permissions)
- [Developer commands：`codex sandbox`](https://learn.chatgpt.com/docs/developer-commands)

`@modelcontextprotocol/server-memory` 的包名只按博客原文引用。本文没有安装。npmjs 上的软件包页在脚本访问时返回 403，所以正文不单列那个链接。
