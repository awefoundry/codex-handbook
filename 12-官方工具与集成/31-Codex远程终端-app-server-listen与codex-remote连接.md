---
id: codex-app-server-remote
title: Codex 远程终端：在服务器上跑 codex app-server，本机用 codex --remote 连接，0.171 起 codex exec 也能接上
seo_title: Codex 远程终端：app-server --listen 与 codex --remote
description: 想让 Codex 跑在服务器或开发机上、自己在笔记本终端里操作？官方的做法是在远端运行 codex app-server --listen，本机用 codex --remote 连接。本文按官方文档讲清 ws、wss、unix 三种地址、bearer token 怎么放、为什么明文只能走本机或 SSH 转发，以及 0.171 新增的 codex exec --remote。
lede: 代码和环境留在那台机器上，终端留在你面前。用 app-server 听一个地址，再用 --remote 接上去。明文 WebSocket 只走本机或 SSH 转发。
url: /guides/codex-app-server-remote
status: published
section: guides
category: C-cli-app-usage
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 31
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-20
date_modified: 2026-11-20
verified_on: 2026-11-20
tested_cli_version: 0.171.0
official_ref: https://learn.chatgpt.com/docs/app-server
keywords: [Codex app-server, codex --remote, Codex 远程终端, codex exec --remote, remote-auth-token-env]
related: [codex-sdk-typescript-python, cli-manage-multiple-sessions, codex-cli-commands-cheatsheet, codex-cli-0-171-sol-default-workspace-exec-remote, codex-remote-control-mac]
howto: true
faq:
  - q: app-server 能当成生产服务一直开着吗？
    a: 不要。0.171.0 的 codex --help 和 codex app-server --help 都把 app-server 标成 experimental。Developer commands 写它主要用于开发和调试，可能不经通知就变化。App Server 页写 WebSocket 传输是 experimental and unsupported。
  - q: 可以把 ws:// 直接暴露到公网吗？
    a: 不可以。App Server 页写明，明文 WebSocket 只用于本机或 SSH 端口转发。非本机连接要配置 WebSocket 认证，并放在 TLS 后面。同一页还写，非回环的 WebSocket 监听在推出期间默认允许未认证连接，暴露到远端之前要先配认证。
  - q: token 写在命令行里行吗？
    a: 官方示例不这样做。token 放在环境变量里，命令行只传变量名：--remote-auth-token-env CODEX_REMOTE_TOKEN。服务端文档也写，优先用 --ws-token-file，不要把原始 bearer token 放在命令行上。
  - q: codex --remote 和手机远程控制是一回事吗？
    a: 不是。--remote 把本机终端接到一个你自己启动的 app server。手机或另一台电脑控制已配对主机，是远程连接一文里的另一条路径。Developer commands 写，codex remote-control 也不代替你要自己写协议客户端时使用的 codex app-server --listen。
---

# Codex 远程终端：在服务器上跑 codex app-server，本机用 codex --remote 连接，0.171 起 codex exec 也能接上

> 核对依据：2026-11-20 打开的 [Codex App Server](https://learn.chatgpt.com/docs/app-server)「Connect the CLI terminal UI」和 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)，以及 GitHub Release [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)。同一天在 Linux 上，`codex --version` 为 `codex-cli 0.171.0`。本机回环试验用的是独立 `CODEX_HOME`，**没有登录**。`codex app-server --listen ws://127.0.0.1:4500` 能听在该地址；`/readyz` 与不带 `Origin` 的 `/healthz` 返回 200，带 `Origin` 的 `/healthz` 返回 403。`codex exec --remote` 没有报连不上，随后模型请求因 401 结束。`codex --remote` 因当前环境不是 TTY 而拒绝启动交互界面。没有配图。

这篇给「仓库和依赖在一台常开的机器上，自己在笔记本的终端里操作」的人。程序里嵌 Codex 用 [SDK](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md)。本地多条会话的 `resume`、`fork` 见 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。子命令和启动参数的总表见 [命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。

## 先说结论

官方把这件事写成：在一台机器上跑 app-server，从另一台机器用 Codex CLI 的终端界面接上去。

按你要的结果选：

| 你要的结果 | 用什么 | 依据 |
| --- | --- | --- |
| 终端在这台电脑，会话跑在另一台你自己启动了 app server 的机器上 | 远端 `codex app-server --listen`，本机 `codex --remote` | App Server 页「Connect the CLI terminal UI」 |
| 脚本或 CI 式的非交互任务，也跑在那个已经开着的 app server 上 | 0.171.0 起的 `codex exec --remote` | Release #61707，以及 0.171.0 的 `codex exec --help` |
| 在自己的程序里启动、继续、恢复线程 | Codex SDK | App Server 页写明：自动化作业或 CI 用 SDK，而不是把 app-server 当作业系统 |
| 手机或另一台电脑控制一台已配对的 Mac / Windows 主机，或桌面端走 SSH 打开远程项目 | 远程连接一文里的配对和 SSH | [远程连接](./01-Codex远程控制另一台Mac.md)。那篇文章写：远程连接用 SSH 启停远程 app server，不要把 app-server 传输层直接暴露在共享或公网 |
| 任务在 Codex Cloud 的环境里跑，不占用这台开发机 | Cloud 环境 | [云端环境](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。那是另一套托管环境，不是 `--remote` 的地址 |

Developer commands 还写了一条边界：`codex remote-control` 供受管理的远程控制客户端和 SSH 远程流程使用；你要自己做本地协议客户端时，它不能代替 `codex app-server --listen`。

## 准备

**版本。** 本文的命令和报错来自 Linux 上的 `codex-cli 0.171.0`。官方「Connect the CLI terminal UI」没有写两侧必须是同一个版本。跨机器时，先分别执行 `codex --version`，对不上时先不要假设旧客户端能用新的 `--remote` 参数。

**实验功能。** 0.171.0 的 `codex --help` 把子命令写成 `app-server [experimental]`。`codex app-server --help` 的第一行也是 `[experimental]`。Developer commands 写：在本地启动 Codex app server，主要用于开发和调试，可能不经通知就变化。App Server 页写：WebSocket 传输是 experimental and unsupported。本文没有找到「不支持生产负载」这句原话；上面三处已经足够说明不要把它当成长期对外的服务。

**登录在哪一侧。** 「Connect the CLI terminal UI」没有写登录必须放在监听端还是连接端。本文未登录：`codex login status` 在空目录里输出 `Not logged in`，退出码 1。后面的 `codex exec --remote` 能在本机回环上往下走，但模型请求以 401 结束。因此本文只证实「没登录就没有模型回复」，没有证实登录文件该放在哪一台机器。

## 最小可用：本机回环

官方示例是先在一台机器上听：

```bash
codex app-server --listen ws://127.0.0.1:4500
```

再在终端里连接：

```bash
codex --remote ws://127.0.0.1:4500
```

`codex app-server --help` 写明 `--listen` 支持 `stdio://`（默认）、`unix://`、`unix://PATH`、`ws://IP:PORT` 和 `off`。

2026-11-20 在 Linux 上、独立 `CODEX_HOME`、未登录时，执行了上面的监听命令。进程打印：

```text
codex app-server (WebSockets)
  listening on: ws://127.0.0.1:4500
  readyz: http://127.0.0.1:4500/readyz
  healthz: http://127.0.0.1:4500/healthz
  note: binds localhost only (use SSH port-forwarding for remote access)
```

同一进程上，用 HTTP 核对了文档里的健康检查：

- `GET /readyz` 返回 `200 OK`，正文为空。
- 不带 `Origin` 的 `GET /healthz` 返回 `200 OK`，正文为空。
- 带 `Origin: http://example.com` 的 `GET /healthz` 返回 `403 Forbidden`。

这和 App Server 页一致：监听接受新连接之后 `/readyz` 为 200；请求不带 `Origin` 时 `/healthz` 为 200；带 `Origin` 的请求被拒绝。

接着在另一个空 `CODEX_HOME` 里执行 `codex exec --remote ws://127.0.0.1:4500 --skip-git-repo-check`，提示词是一句测试文本。进程没有报地址连不上。它打印了一个 thread id，然后模型请求失败，原文是缺少 bearer 或 basic 认证，对 `https://api.openai.com/v1/responses` 返回 401。没有模型回复。用完后已关掉监听，再次访问 `/readyz` 连不上。

`codex --remote ws://127.0.0.1:4500` 在这个没有 TTY 的环境里没有进入界面。进程退出码 1，原文是：`TERM` 为 `dumb`，因为没有终端可用于确认提示，拒绝启动交互式 TUI。本文因此没有看到远程会话的画面。

## 跨机器：SSH 端口转发，或 wss 加 token

App Server 页写：非本机连接要配置 WebSocket 认证，并把连接放在 TLS 后面。bearer token 放在环境变量里，命令行只传变量名，不要把 token 写进命令行。官方示例是：

```bash
export CODEX_REMOTE_TOKEN="$(cat "$HOME/.codex/app-server-token")"
codex --remote wss://remote-host:4500 \
  --remote-auth-token-env CODEX_REMOTE_TOKEN
```

`$HOME/.codex/app-server-token` 是文档示例里的文件路径。本文没有这个文件，没有设置这个变量，也没有连过 `wss://`。

同一页写明：`--remote` 接受 `ws://`、`wss://`、`unix://` 和 `unix://PATH`。明文 WebSocket 只用于 localhost，或一条 SSH 端口转发。

0.171.0 的 `codex --help` 与此一致：`--remote` 接受 `ws://host:port`、`wss://host:port`、`unix://` 或 `unix://PATH`；`--remote-auth-token-env` 是存放 bearer token 的环境变量名。

监听如果不是回环地址，App Server 页还有一句：非回环 WebSocket 监听在推出期间默认允许未认证连接，所以暴露到远端之前要先配置 WebSocket 认证。文档列出的服务端认证参数是：

- `--ws-auth capability-token --ws-token-file /absolute/path`
- `--ws-auth capability-token --ws-token-sha256 HEX`
- `--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path`

签名 bearer 还可以设置 `--ws-issuer`、`--ws-audience` 和 `--ws-max-clock-skew-seconds`。客户端在 WebSocket 握手时带 `Authorization: Bearer <token>`，app-server 在 JSON-RPC `initialize` 之前执行认证。文档写明优先使用 `--ws-token-file`，不要把原始 bearer token 放在命令行上。`--ws-token-sha256` 只是校验值，客户端仍然需要原来的 token。

0.171.0 的 `codex app-server --help` 里能看到同一组 `--ws-auth`、`--ws-token-file`、`--ws-token-sha256`、`--ws-shared-secret-file`、`--ws-issuer`、`--ws-audience` 和 `--ws-max-clock-skew-seconds`。本文没有生成 token，没有用这些参数启动过带认证的监听。

本机回环那次，进程自己打印了 “binds localhost only (use SSH port-forwarding for remote access)”。这和文档「明文只走本机或 SSH 转发」是同一条边界。本文没有做 SSH 转发，没有从第二台机器连接。

## unix socket

App Server 页写，`--remote unix://` 使用默认 socket，`--remote unix://PATH` 使用明确路径。`--listen` 一侧同样是 `unix://` 或 `unix://PATH`：WebSocket 握手走 Codex 默认的 app-server 控制 socket，或你指定的 Unix socket 路径。

0.171.0 的帮助文本与此相同。Developer commands 还写了带三个斜杠的绝对路径形式：`--listen unix:///absolute/path.sock`。本文没有改用 unix socket 启动，没有验证默认 socket 的实际路径。

## 0.171 起：codex exec --remote

Release 的原文是：

> Added `codex exec --remote <ADDR>` to start or resume noninteractive sessions on an existing app server. (#61707)

0.171.0 的 `codex exec --help` 写的是：

- `--remote <ADDR>`：Connect to an existing app server
- `--remote-auth-token-env <ENV_VAR>`：Environment variable containing the remote WebSocket bearer token

2026-11-20 的 Developer commands 里，`codex exec` 一节还没有这两行。交互式 `codex`、`codex agents` 和 `codex queue` 的 `--remote` 那一节是有的。非交互这一条，目前以 Release 和本机帮助为准。

本机回环上，`codex exec --remote ws://127.0.0.1:4500` 的结果见上面：监听已在，进程没有报连不上，未登录时模型请求 401。本文没有用 `--remote` 恢复一条已有的非交互会话，所以 Release 里的 “resume” 没有实测。

`codex exec-server` 的帮助里也有一个 `--remote <URL>`。那一行写的是把这个 exec-server 注册成远程环境，不是连接已有 app server。不要和 `codex exec --remote` 混用。

## 常见问题与安全边界

**明文 WebSocket。** 只用于 `127.0.0.1` 这种本机地址，或 SSH 已经转发到本机的端口。文档和这次进程的提示都指向 SSH 转发，而不是把 `ws://` 绑到一块公网网卡。

**token 不进命令行。** 连接端用 `--remote-auth-token-env` 传变量名。服务端优先 `--ws-token-file`。本文没有把任何 token 放进 shell 历史。

**哪些命令的帮助里有连 app server 的 `--remote`。** 2026-11-20 在 0.171.0 上核对了帮助文本。下面这些把 `--remote` 写成连接远程 app server：

- `codex`（交互式 TUI）。Developer commands 有同样的说明。
- `codex exec`。Release 和 `codex exec --help` 有；当天的 Developer commands 的 exec 一节还没有。
- `codex agents`、`codex queue`。Developer commands 写了 `--remote`；`queue` 还可以在排队之后，到本地 daemon 或 `--remote` 选定的服务器上尝试恢复线程。
- `codex resume`、`codex fork`、`codex archive`、`codex unarchive`、`codex delete`。这些子命令的 `--help` 里有同样的 `--remote` 和 `--remote-auth-token-env`。当天的 Developer commands 没有在 archive、delete、resume、fork 各节里重复这两行。本文没有用它们连上服务器。

`codex review --help` 和 `codex cloud --help` 里没有这个 `--remote`。

**队列满了会怎样。** App Server 页写，WebSocket 模式下队列有上限。入口满了，服务器用 JSON-RPC 错误码 `-32001` 和 “Server overloaded; retry later.” 拒绝新请求。客户端应以指数增加的延迟加抖动重试。本文没有把队列打满。

## 参考资料

- [Codex App Server](https://learn.chatgpt.com/docs/app-server)
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- [GitHub Release rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)
- 同库：[Codex SDK](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md)、[管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)、[命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)、[Codex CLI 0.171.0](./30-Codex-CLI-0.171-默认GPT-6.2-Sol-终端工作区默认开启与exec-remote.md)、[远程连接](./01-Codex远程控制另一台Mac.md)

官方资料核对日期：2026-11-20（Asia/Shanghai）。本机回环的监听、健康检查和未登录时的 `codex exec --remote` 已做。没有 TTY，没有进入交互式 TUI，没有做 SSH 转发，没有配过 token。
