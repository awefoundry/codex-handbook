---
id: codex-on-cloudflare-durable-objects
title: Codex 在 Cloudflare Durable Objects 上跑：用 ContainerHarness 保持和本机一样的 CLI，会话写进对象存储
seo_title: Codex 在 Cloudflare Durable Objects 上运行：ContainerHarness 与会话持久化
description: Cloudflare 提供实验能力，让 OpenAI Codex 跑在 Durable Objects 上。一条路径用 ContainerHarness 在容器里跑官方 CLI，会话写入对象的 SQLite；另一条把回合处理编成 WebAssembly。本文按 Cloudflare 官方文档整理适用场景、凭据如何放在容器外，以及空闲快照和恢复时要注意的限制。
lede: 这是 Cloudflare 的实验部署。官方 CLI 跑在容器里，会话记在 Durable Object 的 SQLite 中；凭据留在容器外面。
url: /guides/codex-on-cloudflare-durable-objects
status: published
section: guides
category: J-official-tools
topic: 官方工具与集成
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, Cloud]
difficulty: 进阶
order: 26
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-14
date_modified: 2026-11-14
verified_on: 2026-11-14
official_ref: https://developers.cloudflare.com/agents/harnesses/codex/
keywords: [Codex Cloudflare, Durable Objects, ContainerHarness, Codex harness, 会话持久化, ContainerEgress]
related: [cloud-environments, codex-sdk-typescript-python, codex-cli-0-169-side-chat-cloud-connection]
howto: false
faq:
  - q: 这是 OpenAI 托管的 Codex Cloud 吗？
    a: 不是同一套部署。本文写的是 Cloudflare Agents 文档里的实验能力：Durable Object 驱动容器里的官方 CLI，或按 changelog 把回合处理编进 WebAssembly。OpenAI 的云端环境见《Codex Cloud 云端环境》。
  - q: 可以把它当成已经稳定的生产方案吗？
    a: 不可以按 SLA 来用。Cloudflare 把 agents/harness/container 标成 experimental，并写明 API 可能在任一版本改变。本文没有在 Cloudflare 账号里部署。
  - q: API Key 能写进容器或快照吗？
    a: 文档要求凭据留在容器外。CLI 使用占位主机和占位 Key，Worker 里的 ContainerEgress 在请求离开容器后补上真实凭据。setup 步骤用过的 token 会留在快照里，代理可以读到。
  - q: 容器空闲之后，刚写的文件还在吗？
    a: 文档写空闲约 5 分钟后会做文件系统快照并停止容器。下次提示从这份快照恢复。快照之后写入的文件可能丢失。必须留下的文件要放到容器以外的持久存储。
---

# Codex 在 Cloudflare Durable Objects 上跑：用 ContainerHarness 保持和本机一样的 CLI，会话写进对象存储

> 本文在线版：[codexguide.io/guides/codex-on-cloudflare-durable-objects](https://codexguide.io/guides/codex-on-cloudflare-durable-objects)

> 核对依据：Cloudflare Agents 文档 [Codex](https://developers.cloudflare.com/agents/harnesses/codex/)（2026-11-14 打开，HTTP 200）和 changelog [Run the Codex agent loop on Cloudflare Workers](https://developers.cloudflare.com/changelog/post/2026-11-09-codex-harness/)（文内日期 2026-11-09，HTTP 200）。本文没有 Cloudflare 账号，没有安装 `agents`，没有运行 `cf dev` 或 `cf deploy`，没有容器日志，也没有配图。下面的配置片段来自这两页，用来说明两条路径的形状，不能当成已经跑通的结果。

这篇给想把 Codex 放到自己的 Cloudflare Worker 后面、又需要先分清「容器里的官方 CLI」和「Durable Object 里的 WebAssembly 回合循环」的人。OpenAI 托管的云端环境、安装脚本和密钥设置见 [Codex Cloud 云端环境](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。在自己的 Node 或 Python 程序里启动线程，见 [Codex SDK](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md)。本机 CLI 的版本能力见 [Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。

## 先看结论

Cloudflare 现在有两条实验路径，文档没有把它们写成同一次部署：

| | 容器路径（现行 Agents 文档） | Wasm 路径（2026-11-09 changelog） |
| --- | --- | --- |
| 代码跑在哪 | Cloudflare Container 里的官方 Codex CLI | Durable Object 内的 WebAssembly，由 Codex 的 Rust 回合处理改编 |
| 谁驱动它 | Durable Object 上的 `ContainerHarness`（`agents/harness/container`） | 示例里的 `CodexHarness`，接上 Tasks、Sessions、Streams、Workspace |
| CLI 的工具和会话格式 | 文档写明与笔记本电脑上的 CLI 相同 | changelog 写的是回合处理，不是「原样启动官方 CLI」 |
| 凭据 | 不进容器；`ContainerEgress` 在请求离开容器后补上 | changelog 示例走 AI Gateway 的 `createAI`，没有描述 ContainerEgress |
| 文档状态 | 页首标明 experimental，API 可能在任一版本改变 | changelog 写 experimental example |

要和本机一样的 CLI、插件和会话文件，读容器路径。要的是 Durable Object 里面的回合循环、用 Tasks 重放已完成步骤，读 Wasm 路径。两条都不要承诺可用性或时延。

OpenAI 托管的 Codex Cloud 使用的是另一套云端环境。终端里 0.169 的可选 Cloud 连接也是 OpenAI 产品上的能力，见 [0.169.0 一文](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。

## 容器路径：Durable Object、ContainerHarness、ContainerEgress

现行文档的结构是：Codex 跑在 Cloudflare Container 里，Durable Object 用 `ContainerHarness` 驱动它。

- CLI 拥有循环，保留自己的工具、插件、设置和会话格式。
- Durable Object 拥有记录。harness 把会话、操作、转录和 CLI 会话文件放进对象的 SQLite。生命周期任务在对象被驱逐或重新部署后，重新连上仍在运行的容器。
- 凭据留在容器外。CLI 调用占位主机和占位 Key。`ContainerEgress` 是 Worker 里的一个入口，在模型请求离开容器之后补上真实凭据。

不需要自己写 Dockerfile。harness 启动 `cloudflare/debian-trixie`，第一次使用时安装 Codex，并对文件系统做快照，供以后的启动使用。

文档列出的本地前提是 Node.js 24 或更高、Cloudflare CLI，以及一个 OpenAI API Key。本地容器还需要 Docker 在运行。创建项目的命令是：

```bash
cf init codex-agent
cd codex-agent
npm i agents@latest
```

文档用 `cf`，本文没有改写成别的 CLI 名称，也没有执行这三条命令，因此没有核对 `agents@latest` 当天解析到的版本。

`cloudflare.config.ts` 在文档里声明三件事：一个调度策略为 `durable_object` 的容器、带 SQLite 的 Durable Object `CodexAgent`、Worker 入口 `ContainerEgress`，以及密钥 `OPENAI_API_KEY`。文档示例里的 `compatibilityDate` 是 `"2026-11-06"`，`compatibilityFlags` 含 `nodejs_compat`。完整文件以文档页为准。

Agent 一侧，文档从 `agents/harness/container` 引入 `ContainerHarness` 和 `codex`，并再导出 `ContainerEgress`。构造函数把容器、egress 和 `codex({ apiKey })` 接在一起，再用 `Lifecycle.install(this).use(this.harness)`。`onRequest` 里，GET 一类的非 POST 返回 `harness.messages()`，POST 读取 JSON 里的 `prompt`，调用 `harness.prompt(prompt)`，把 `status` 和 `text` 返回给客户端。默认的 `fetch` 示例用 `CodexAgent.getByName("demo")` 把请求送到名为 `demo` 的对象。

`codex()` 在文档中的选项：

| 选项 | 文档中的作用 |
| --- | --- |
| `model` | 新会话起始模型；`session.setModel()` 可以再改 |
| `config` | 额外的 `-c key=value`，传给每一次 `codex exec` |
| `version` | 要安装的 `@openai/codex` 版本 |
| `setup` | 只在第一次启动时运行的命令，结果留在快照里 |

文档建议用 `config` 写单条设置，用 `setup` 写 `~/.codex/config.toml`、`AGENTS.md` 或 MCP。带 `user: "agent"` 的步骤以 Codex 运行时的用户、在它的家目录里执行。每个会话的家目录从这份家目录复制开始。文档同时写明：修改 `setup` 或 `version` 会在容器下次启动时生效；那个容器会从头安装，不使用上一份快照。setup 步骤用过的 token 会留在快照里，代理可以读到它。

要通过 AI Gateway 发模型请求，文档写把网关的 OpenAI URL 作为 `baseUrl`。Unified Billing 时把网关 token 当作 `apiKey`；使用已保存的供应商 Key 时，改放到 `headers` 里的 `cf-aig-authorization`。本文没有 AI Gateway 账号，没有验证这两种计费方式。

本地运行时，文档要求把 Key 放进 `.dev.vars` 并且不要提交这个文件，然后启动 Docker，执行 `cf dev`。示例请求是向 `cf dev` 打印的端口 POST `{"prompt":"Write hello.txt containing hi, then read it back."}`。文档写第一次提示更慢，因为要安装 Codex 并做 setup 快照，之后的容器从快照启动。本文没有执行。

## 凭据为什么留在容器外

文档的安全节把容器本身当作沙箱，并写明两条 CLI 运行时没有自己的权限提示，因此容器里的内容都要当成代理可以读取的。凭据放在容器外，由 egress 补上。每一条会到达 harness 的路由都要先做认证。每条 prompt 都可以在容器里执行命令，并消耗模型额度。

这和「把 Key 写进镜像或 `~/.codex`」是两条路。setup 命令如果把 token 写进家目录，文档已经说明它会进入快照。需要密钥的步骤应放在 Worker 一侧。

部署命令在文档里是：加上认证之后，`cf auth login`，再 `cf deploy --secrets-file .dev.vars`。本文没有登录 Cloudflare，也没有部署。

## 会话、转录和快照存在哪

容器路径里，对象的 SQLite 保存会话、操作、转录和 CLI 会话文件。调用关系按文档：

- `prompt()` 提交工作并等待回答。
- `submit()` 在提示写入后返回；稍后对同一个对象调用 `wait()` 取结果。传入 `operationId` 用来给一次提交去重。
- `harness.sessions.create()` 开始一条独立会话，`harness.sessions.fork(id)` 从已有会话分出分支。
- `session.events()` 先给会话快照，再给实时事件，可以转发给客户端。

`wait()` 的结果在文档示例里看 `status === "done"` 时读取 `text`，否则读取 `reason`。

空闲行为要单独记住：容器空闲五分钟后，harness 对文件系统做快照并停止容器。下一条提示恢复这份快照，并继续 CLI 的会话。容器里的文件来自最后一次快照，快照之后的修改可能丢失。必须保留的文件要放进单独的持久存储，不要只放在容器磁盘上。

## 驱逐、重新部署和容器中途失败

文档按「停在哪」分开写恢复：

- Durable Object 被驱逐或重新部署：生命周期任务重新附着到仍在运行的容器，并重放错过的事件。
- 容器空闲：五分钟后快照并停止；下一次提示从快照恢复。
- 容器在一个回合中途失败：这一回合以 `status: "unanswered"`、`reason: "container_lost"` 结束，会话还在。把 `onContainerLost` 设为 `"retry"` 时，会再跑这一回合；文档要求只在副作用可以安全重复时这样做。

本文没有制造驱逐、空闲或容器崩溃，所以上面三条都是文档行为，不是实测日志。

## Wasm 路径：Tasks、Sessions、Streams、Workspace

2026-11-09 的 changelog 描述的是另一条实验示例：把 Codex 的 Rust 回合处理改编成 WebAssembly，放在 Durable Object 里运行。对话、文件，以及已经完成的模型和工具结果，可以在重启后留下来，以便中断后恢复。

changelog 把持久执行拆成 Agents SDK 的四项能力：

- `Tasks` 记录模型调用和工具执行。已经完成的步骤在重启后复用记录下来的结果；被打断的步骤可以再跑。
- `Sessions` 保存对话历史，并压缩模型上下文。
- `Streams` 按顺序保存事件，供重新连接后重放。
- `Workspace` 提供读写持久文件的工具。

示例类同时持有这四者和一个本地的 `CodexHarness`，模型通过 `createAI` 指向 AI Gateway。changelog 里的模型字符串示例是 `openai/gpt-6.1-sol`。要使用这个模型，文档要求把名为 `default` 的网关配成 Unified Billing，或配上已保存的 OpenAI API Key。changelog 写：安装、模型、工具和恢复行为见 Codex harness guide。2026-11-14 打开的 guide 页内容是上面的 ContainerHarness，不是这份 Wasm 类。按页面各自的代码部署，不要把 `ContainerHarness` 和 `CodexHarness` 拼进同一个构造函数。

本文没有打开 changelog 里的示例仓库，没有编译 WebAssembly，也没有核对 `openai/gpt-6.1-sol` 在某个网关上是否可调用。

## 和 Codex Cloud、本机 CLI、SDK 的差别

| 需求 | 更接近的选择 |
| --- | --- |
| 任务跑在 OpenAI 托管的环境里，用官方的环境发布、联网和密钥 | [Codex Cloud 云端环境](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) |
| 就在自己的终端里用官方 CLI | 本机安装；版本差异见 [0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md) |
| 在自己的服务进程里启动、继续、按 ID 恢复线程 | [Codex SDK](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md) |
| CLI 跑在 Cloudflare 容器里，会话落在 Durable Object 的 SQLite | 本文的 ContainerHarness |
| 回合循环编译进 Durable Object，用 Tasks 重放已完成步骤 | 本文的 Wasm 路径 |

容器路径的文档目标，是让 CLI 的工具、插件、设置和会话格式与笔记本电脑上的那一份相同。SDK 则是在你的程序里包一层 `codex exec`。两者都不是 Codex Cloud 的环境快照。

## 常见问题

### 实验状态意味着什么

文档对 `agents/harness/container` 的表述是 experimental，API 可能在任一版本改变。changelog 的 Wasm 示例同样是实验能力。本文不把任何一条写成已签署的可用性承诺。上线前要用你自己的账号核对当天文档，并在路由前加上认证。

### 文件会丢，密钥不能进容器

空闲快照只覆盖快照当时的文件系统。快照之后的写入可能丢失。密钥、刷新令牌和客户数据不要放进镜像、setup 脚本或容器家目录。ContainerEgress 负责在请求离开容器后附加真实凭据。setup 若必须使用 token，要知道它会留在快照里。

### 本地没有 Docker 时能开发吗

文档把 Docker 写成本地容器开发的前提。本文没有验证缺少 Docker 时 `cf dev` 的报错原文。Wasm 路径的 changelog 没有把 Docker 列进那段示例，但它依赖 Agents SDK 和 AI Gateway，本文同样没有跑过。

## 参考资料

- [Cloudflare Agents：Codex（ContainerHarness）](https://developers.cloudflare.com/agents/harnesses/codex/)
- [Cloudflare changelog：Run the Codex agent loop on Cloudflare Workers（2026-11-09）](https://developers.cloudflare.com/changelog/post/2026-11-09-codex-harness/)
- 同库：[Codex Cloud 云端环境](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)、[Codex SDK](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md)、[Codex CLI 0.169.0](./25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)

官方资料核对日期：2026-11-14（Asia/Shanghai）。没有在真实 Cloudflare 账号中部署，没有容器或 Durable Object 的运行记录。
