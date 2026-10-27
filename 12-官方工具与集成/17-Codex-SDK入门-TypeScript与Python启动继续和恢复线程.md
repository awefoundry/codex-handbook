---
id: codex-sdk-typescript-python
title: Codex SDK 入门：用 TypeScript 或 Python 在自己的程序里启动、继续和恢复 Codex 线程
seo_title: Codex SDK 入门：TypeScript 与 Python 启动、继续和恢复线程
description: Codex SDK 让你在自己的脚本、内部工具或 CI 里启动 Codex 线程、多轮继续和按 ID 恢复。本文按官方文档和 0.164.0 实测，讲 TypeScript 与 Python 的安装、基本用法、流式事件、结构化输出、沙箱和登录方式。
lede: 命令行里的 codex exec 够用时就用它；要在程序里多轮对话、拿结构化结果、按线程 ID 接着干，再上 SDK。
url: /guides/codex-sdk-typescript-python
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 17
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-27
date_modified: 2026-10-27
verified_on: 2026-10-27
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/codex-sdk
keywords: [Codex SDK, "@openai/codex-sdk", openai-codex Python, Codex 编程调用, Codex 线程恢复, Codex TypeScript]
howto: true
faq:
  - q: Codex SDK 有哪些语言？
    a: 官方提供 TypeScript（npm 包 @openai/codex-sdk，需要 Node.js 18+，只在服务端用）和 Python（PyPI 包 openai-codex，需要 Python 3.10+）。2026-10-27 查询时最新版本分别是 0.164.0 和 0.163.0。
  - q: SDK 和 codex exec 有什么区别？
    a: TypeScript SDK 底层就是启动 codex exec --experimental-json，再把 JSONL 事件转成对象；它帮你管理线程 ID、多轮继续、流式事件和结构化输出。只跑一次命令拿结果，codex exec 就够了。
  - q: 怎么恢复之前的线程？
    a: 线程保存在 ~/.codex/sessions。TypeScript 用 codex.resumeThread(threadId)，Python 用 codex.thread_resume(thread_id)，然后继续 run。
  - q: SDK 用什么登录？
    a: TypeScript SDK 调用本机的 codex CLI，可以沿用本机的登录状态，也可以在 new Codex({ apiKey }) 里传 API Key（SDK 会以 CODEX_API_KEY 传给 CLI）。Python SDK 有 login_api_key、login_chatgpt 和 login_chatgpt_device_code 三个方法。
  - q: 还能用 codex mcp-server 吗？
    a: 不能。官方文档写明 codex mcp-server 命令和独立的 codex-mcp-server 程序已经移除，已有集成请改用 Codex app server。
---

# Codex SDK 入门：用 TypeScript 或 Python 在自己的程序里启动、继续和恢复 Codex 线程

> 本文在线版：[codexguide.io/guides/codex-sdk-typescript-python](https://codexguide.io/guides/codex-sdk-typescript-python)

> 核对依据：OpenAI 官方 [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) 文档、[TypeScript SDK 仓库说明](https://github.com/openai/codex/tree/main/sdk/typescript)、[Python SDK 仓库说明](https://github.com/openai/codex/tree/main/sdk/python)，以及 npm 包 `@openai/codex-sdk` 0.164.0 和 PyPI 包 [openai-codex](https://pypi.org/project/openai-codex/) 0.163.0 的类型定义。实测环境是 Linux、Node.js 和 Python 3：两个包都实际安装并运行了。**测试机上的 Codex 没有登录**，所以没有成功完成的对话结果；文中的事件输出是未登录时的真实输出，用来说明事件流的样子。核对日期 2026-10-27（北京时间）。

你可能已经在用 `codex exec` 跑脚本了。它适合「给一段提示，拿一次结果」。如果你想在自己的程序里做这些事：

- 同一个任务分几轮做：先规划，确认后再实现；
- 拿到 JSON 结构的结果，直接给下一步程序用；
- 程序重启后，按线程 ID 接着之前的任务继续；
- 边跑边看 Codex 执行了什么命令、改了哪些文件；

就该用 Codex SDK 了。

## SDK、codex exec、App Server 分别什么时候用

| 方式 | 适合 | 说明 |
|---|---|---|
| `codex exec` | 脚本、CI 里跑一次任务 | 命令行，输出文本或 JSONL |
| Codex SDK | 在自己的程序里控制 Codex：多轮、恢复、结构化输出 | TypeScript 和 Python 两个包 |
| Codex app server | 自己做一个完整的 Codex 客户端（登录、历史、审批界面、流式事件） | JSON-RPC 协议 |

官方文档的说法是：自动化编码任务（包括 CI 里的任务）用 SDK；要做自定义客户端、自己处理认证、会话历史和审批，用 app server。

另外，`codex mcp-server` 命令和独立的 `codex-mcp-server` 程序**已经移除**，以前用它做集成的，官方建议改用 app server。

## TypeScript：安装和基本用法

### 安装

```bash
npm install @openai/codex-sdk
```

要求 Node.js 18 或更高，只在服务端使用。2026-10-27 查询时 npm 上最新版是 0.164.0（10-23 发布），它依赖同版本的 `@openai/codex`（也就是 Codex CLI）。

TypeScript SDK 的工作方式是：启动本机的 `codex` CLI，通过标准输入输出交换 JSONL 事件。所以 CLI 能用什么配置、什么登录，SDK 就能用什么。

### 启动线程，多轮继续

```ts
import { Codex } from "@openai/codex-sdk";

const codex = new Codex();
const thread = codex.startThread();

const plan = await thread.run("先不要改代码。分析 CI 失败的原因，给出修复计划。");
console.log(plan.finalResponse);

// 同一个线程继续，Codex 记得上一轮的内容
const result = await thread.run("按计划实现修复，然后运行测试。");
console.log(result.finalResponse);
```

`run()` 返回的对象里有三样东西：

- `finalResponse`：最后的回答文本；
- `items`：这一轮里发生的所有条目（消息、推理、执行的命令、改动的文件、MCP 调用、网页搜索、待办清单、错误）；
- `usage`：token 用量。

### 按 ID 恢复线程

线程保存在 `~/.codex/sessions`。程序重启后，用保存下来的线程 ID 恢复：

```ts
const thread = codex.resumeThread(savedThreadId);
await thread.run("从上次停下的地方继续。");
```

线程 ID 在 `thread.id` 里。注意它是在第一轮开始后才有的（实测见下文），所以要在 `run()` 之后再保存。

### 线程选项：工作目录、沙箱、模型

```ts
const thread = codex.startThread({
  workingDirectory: "/path/to/project",
  skipGitRepoCheck: false,
  sandboxMode: "workspace-write",
  approvalPolicy: "never",
  model: "gpt-6.1-sol",
  modelReasoningEffort: "medium",
  networkAccessEnabled: false,
  webSearchMode: "disabled",
});
```

几个要点：

- **工作目录必须是 Git 仓库**，否则会报错。这是为了让改动可以回退。确实不是仓库时，传 `skipGitRepoCheck: true`。
- `sandboxMode` 可选 `read-only`、`workspace-write`、`danger-full-access`。
- `approvalPolicy` 可选 `never`、`on-request`、`on-failure`、`untrusted`。程序里没人点审批，通常配合沙箱用 `never`，靠沙箱限制范围。
- `model` 写你账号能用的模型。模型名见 [Codex 模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。
- `webSearchMode` 可选 `disabled`、`cached`、`live`。

权限和沙箱的含义，参考 [Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 流式事件和结构化输出

### runStreamed：边跑边看

`run()` 要等整轮结束才返回。想实时看到进度，用 `runStreamed()`：

```ts
const { events } = await thread.runStreamed("诊断测试失败的原因并给出修复建议");

for await (const event of events) {
  switch (event.type) {
    case "item.completed":
      console.log("item", event.item.type);
      break;
    case "turn.completed":
      console.log("usage", event.usage);
      break;
    case "turn.failed":
      console.error("failed", event.error.message);
      break;
  }
}
```

事件类型有：`thread.started`、`turn.started`、`turn.completed`、`turn.failed`、`item.started`、`item.updated`、`item.completed` 和 `error`。

### 实测：未登录时事件流长这样

我们在测试机上用 `runStreamed` 跑了一次（只读沙箱，测试机没有登录）。输出里的线程 ID 是本次运行随机生成的，`cf-ray` 和 `request id` 已省略：

```text
EVENT {"type":"thread.started","thread_id":"01a17aee-a80b-7b50-bce7-a3305d43bc64"}
EVENT {"type":"turn.started"}
EVENT {"type":"error","message":"Reconnecting... 2/5 (unexpected status 401 Unauthorized: Missing bearer or basic authentication in header, url: wss://api.openai.com/v1/responses, ...)"}
...
EVENT {"type":"item.completed","item":{"id":"item_0","type":"error","message":"Falling back from WebSockets to HTTPS transport. unexpected status 401 Unauthorized: ..."}}
EVENT {"type":"error","message":"Reconnecting... 1/5 (unexpected status 401 Unauthorized: ..., url: https://api.openai.com/v1/responses, ...)"}
...
EVENT {"type":"turn.failed","error":{"message":"unexpected status 401 Unauthorized: Missing bearer or basic authentication in header, ..."}}
ERROR Error: Codex Exec exited with code 1: ...
thread.id = 01a17aee-a80b-7b50-bce7-a3305d43bc64
```

从这段输出能看出几件事：

1. 第一个事件就是 `thread.started`，带着线程 ID。即使这一轮失败了，`thread.id` 也已经有值。
2. 连接失败时，CLI 先用 WebSocket 重试 5 次，再退回 HTTPS 重试 5 次，期间发出的是 `error` 事件，不是异常。
3. 最后是 `turn.failed`，然后 SDK 抛出异常 `Codex Exec exited with code 1`。所以 `for await` 外面要包 `try/catch`。

看到 `401 Unauthorized`，就是没登录或者 API Key 不对。先在同一台机器上运行 `codex login`，或者给 SDK 传 `apiKey`。

### 结构化输出

给 `run()` 传一个 JSON Schema，Codex 的最终回答会按这个结构返回：

```ts
const schema = {
  type: "object",
  properties: {
    summary: { type: "string" },
    status: { type: "string", enum: ["ok", "action_required"] },
  },
  required: ["summary", "status"],
  additionalProperties: false,
} as const;

const turn = await thread.run("总结仓库当前状态", { outputSchema: schema });
const data = JSON.parse(turn.finalResponse);
```

已经在用 Zod 的项目，可以用 `zod-to-json-schema` 转换，`target` 设为 `"openAi"`。

### 带图片

```ts
const turn = await thread.run([
  { type: "text", text: "描述这两张截图的区别" },
  { type: "local_image", path: "./before.png" },
  { type: "local_image", path: "./after.png" },
]);
```

文字条目会拼成提示词，图片通过 CLI 的 `--image` 传进去。

## TypeScript：登录、环境变量和配置覆盖

### 登录方式

- **沿用本机登录**：SDK 启动的是本机的 `codex` CLI，读同一个 `~/.codex`。在这台机器上 `codex login` 过就能用。
- **传 API Key**：`new Codex({ apiKey: process.env.OPENAI_API_KEY })`。SDK 会把它作为环境变量 `CODEX_API_KEY` 传给 CLI。

### env：不继承环境变量

默认情况下，CLI 继承 Node.js 进程的环境变量。传了 `env` 以后，CLI **只**拿到你给的这些（SDK 自己需要的变量，比如 `CODEX_API_KEY`，会另外加上）：

```ts
const codex = new Codex({
  env: {
    PATH: process.env.PATH!,
    HOME: process.env.HOME!,
  },
});
```

这适合不想把服务进程里的密钥都暴露给 Codex 的场景。忘了带 `PATH` 或 `HOME`，CLI 可能找不到命令或配置。

### 配置覆盖

```ts
const codex = new Codex({
  config: {
    sandbox_workspace_write: { network_access: true },
  },
});
```

`config` 会被展开成多个 `--config key=value` 参数传给 CLI，**不会**改动你的配置文件。不能用点路径表示的键，用 `configOverrides` 直接传 TOML 字符串。

优先级从低到高：`config` < `configOverrides` < `baseUrl` 和线程选项。

`codexPathOverride` 可以指定用哪个 `codex` 可执行文件。

## Python：openai-codex

### 安装

```bash
pip install openai-codex
```

要求 Python 3.10 或更高。2026-10-27 查询时 PyPI 上最新稳定版是 0.163.0（10-16 发布）。发布版会带一个锁定版本的 Codex CLI 运行时（0.163.0 依赖 `openai-codex-cli-bin==0.163.0`），不需要另外装 CLI。想用更新的预发布版，`pip install --pre openai-codex`。

和 TypeScript 不同，Python SDK 是通过 JSON-RPC 控制本机的 Codex **app server**。

### 基本用法

```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(
        model="gpt-6.1-sol",
        sandbox=Sandbox.workspace_write,
    )
    result = thread.run("先不要改代码。分析 CI 失败的原因，给出修复计划。")
    print(result.final_response)

    result = thread.run("按计划实现修复。")
    print(result.final_response)
```

官方示例用的是 GPT-6.1 Sol，账号里没有这个模型时，去掉 `model` 参数，用你配置里的默认模型。

`run()` 返回的 `TurnResult` 有 `id`、`status`、`error`、`started_at`、`completed_at`、`duration_ms`、`final_response`、`items`、`usage` 这些字段。

已经是异步程序的，用 `AsyncCodex`：

```python
import asyncio
from openai_codex import AsyncCodex

async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(model="gpt-6.1-sol")
        result = await thread.run("Implement the plan")
        print(result.final_response)

asyncio.run(main())
```

### 沙箱预设

| 预设 | 作用 |
|---|---|
| `Sandbox.read_only` | 只读，不能写文件 |
| `Sandbox.workspace_write` | 能读，能在工作区和配置的可写目录里写 |
| `Sandbox.full_access` | 不限制文件系统访问 |

不传 `sandbox` 时，用 app server 配置里的默认值。在 `run()` 里传的 `sandbox` 会对这一轮**和之后的轮次**生效：

```python
with Codex() as codex:
    thread = codex.thread_start(sandbox=Sandbox.workspace_write)
    thread.run("Make the requested change.")
    review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
```

### 审批模式

`thread_start` 的 `approval_mode` 默认是 `ApprovalMode.auto_review`，另一个选项是 `ApprovalMode.deny_all`。

### 恢复、分叉和列出线程

```python
with Codex() as codex:
    thread = codex.thread_resume(saved_thread_id)
    thread.run("从上次停下的地方继续。")
```

另外还有 `thread_fork`（从已有线程分出一个新线程）、`thread_list`（按目录、关键词等列出线程）和 `thread_archive`。

### 登录

`Codex` 对象上有三个登录方法：

- `login_api_key(api_key)`：用 API Key；
- `login_chatgpt()`：用 ChatGPT 账号登录；
- `login_chatgpt_device_code()`：设备码登录，适合没有浏览器的服务器。

`account()` 可以查看当前登录状态。测试机上未登录时的真实输出：

```python
from openai_codex import Codex

with Codex() as codex:
    print(codex.account())
```

```text
account=None requires_openai_auth=True
```

同一台测试机上，未登录调用 `codex.models()` 返回的模型 ID 是：`gpt-6.1-sol`、`gpt-6-astra`、`gpt-6-sol`、`gpt-6-luna`、`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`、`gpt-5.5`。这是没有登录时 SDK 自带运行时给出的列表，**不代表你的账号能用哪些模型**。比如 10-26 新上线的 GPT-6.1 Terra 就不在里面，登录后以实际返回为准。

## 排错清单

| 现象 | 原因和处理 |
|---|---|
| `401 Unauthorized`，然后 `turn.failed` | 没登录或 API Key 不对。先在同一台机器 `codex login`，或传 `apiKey` / 调 `login_api_key` |
| 提示不是 Git 仓库 | 工作目录要是 Git 仓库；确实不是时传 `skipGitRepoCheck: true` |
| 传了 `env` 后找不到命令或配置 | `env` 不继承进程环境变量，把 `PATH`、`HOME` 带上 |
| 模型不可用 | 模型名写成账号能用的，或者去掉 `model` 用默认值 |
| 旧代码调用 `codex mcp-server` 失败 | 这个命令已移除，改用 app server |

## 相关阅读

- [Codex CLI 命令速查：codex 子命令与启动参数一览](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)
- [Codex CLI /presets 预设与内联 /model、/permissions](15-Codex-CLI-presets预设与内联model-permissions命令.md)
- [Codex 权限、沙箱与审批：什么时候放行，什么时候收紧](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)

## 参考资料

- [Codex SDK - OpenAI](https://learn.chatgpt.com/docs/codex-sdk)
- [TypeScript SDK - openai/codex](https://github.com/openai/codex/tree/main/sdk/typescript)
- [Python SDK - openai/codex](https://github.com/openai/codex/tree/main/sdk/python)
- [openai-codex - PyPI](https://pypi.org/project/openai-codex/)
- [Codex app server - OpenAI](https://learn.chatgpt.com/docs/app-server)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
