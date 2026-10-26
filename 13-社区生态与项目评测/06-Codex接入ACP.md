---
id: codex-acp-integration
title: Codex 接入 ACP：在 Zed 和 JetBrains 里从 ACP Registry 安装 Codex，其他客户端用 codex-acp，以及 ACP 和 MCP 怎么分工
seo_title: Codex 接入 ACP：Registry 安装、codex-acp、与 MCP 分工
description: ACP 让 Zed、JetBrains 等编辑器直接使用 Codex。本文合并站内两篇旧教程，按 2026-10 现状重写：从 ACP Registry 安装，其他客户端用 @agentclientprotocol/codex-acp，登录与审批怎么处理，ACP 与 MCP 怎么分工，以及第一次连接后的验证方法。
lede: 编辑器用 ACP 连上 Codex；认证、计费、沙箱仍由 Codex 自己管。
url: /guides/codex-acp-integration
redirect_from:
  - /guides/codex-zed-acp-integration
status: published
section: guides
category: G-community
topic: 社区生态与编辑器接入
content_type: 指南
source_tag: 社区协议
entry_tags: [CLI, IDE]
difficulty: 进阶
order: 6
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-20
date_modified: 2026-10-22
client_validation_pending: false
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://zed.dev/docs/ai/external-agents
keywords: [Codex ACP, Zed Codex, codex-acp, ACP Registry, Agent Client Protocol, JetBrains Codex]
related: [permissions-sandbox-approvals, advanced-config-toml, advanced-mcp]
faq:
  - q: 给 Zed／JetBrains 配的 OpenAI API Key，能直接给 ACP 里的 Codex 用吗？
    a: 不能默认共用。Zed 官方 External Agents 文档写明：Codex 作为 External Agent 时自己负责认证和计费；给 Zed Agent 配的 OpenAI API Key 不会自动配置 Codex。JetBrains 侧 Registry 安装的 Agent 也走各自的登录／密钥流程。
  - q: zed-industries/codex-acp 还能装吗？
    a: 仓库已归档，README 要求新安装改用 agentclientprotocol/codex-acp（npm：@agentclientprotocol/codex-acp）。Zed／JetBrains 优先从 ACP Registry 装 Codex。
  - q: OpenAI 官方有没有「Codex 原生 ACP」文档？
    a: 截至 2026-10-22，learn.chatgpt.com／developers.openai.com 讲的是 Codex App Server 与 MCP，没有单独的官方 ACP 接入页。编辑器侧通过社区维护的 codex-acp 适配器把 ACP 请求转到 App Server。
---

# Codex 接入 ACP：在 Zed 和 JetBrains 里从 ACP Registry 安装 Codex，其他客户端用 codex-acp，以及 ACP 和 MCP 怎么分工

> 本文在线版：[codexguide.io/guides/codex-acp-integration](https://codexguide.io/guides/codex-acp-integration)

> 核对依据：Zed《[External Agents](https://zed.dev/docs/ai/external-agents)》、JetBrains AI Assistant《[Agent Client Protocol (ACP)](https://www.jetbrains.com/help/ai-assistant/acp.html)》、[ACP Registry](https://agentclientprotocol.com/get-started/registry)、适配器 [agentclientprotocol/codex-acp](https://github.com/agentclientprotocol/codex-acp) README（npm `@agentclientprotocol/codex-acp`）、以及 OpenAI《[Codex App Server](https://learn.chatgpt.com/docs/app-server)》。文中「我的用法」是操作顺序建议。界面文案随客户端变化，以你当前菜单为准。

想在 **Zed** 或 **JetBrains** 里用 Codex 的会话、diff 与审批界面，同时继续用 Codex 自己的登录、模型和沙箱——走的是 **Agent Client Protocol（ACP）**，不是把编辑器里的 OpenAI 模型配置「转成」Codex。

本文把站内两篇旧稿合成一条主线，并按 2026-10 可访问的文档更新安装路径：**ACP Registry**、适配器迁仓、以及 **ACP 与 MCP 的分工**。

合并说明（阅读时可跳过）：

- 主页面 URL 不变：`/guides/codex-acp-integration`（知识库路径仍为 `13-社区生态与项目评测/06-Codex接入ACP.md`）。
- 旧文 `/guides/codex-zed-acp-integration`（原 `13/02`）应 301 到本页；见 frontmatter `redirect_from`。
- 原 `13/06` 里用 Claude Code／OpenClaw 的 `settings.json` 示例、以及「Codex 通过 Zed 自有适配器接入」的过时说法已删除；Zed／JetBrains 实操以 Registry 为准。

## 1. 先认清它是什么

**ACP** 规定编辑器（客户端）和编程 Agent（服务端）怎么对话：开线程、流式输出、展示工具调用、把文件修改与命令执行的审批弹回 UI。协议基于 JSON-RPC；常见跑法是 Agent 作为本地子进程，经 **stdio** 与编辑器通信。

**Codex 侧**仍负责读仓库、跑命令、改文件、沙箱与额度。编辑器只是 ACP 宿主，不会替你「绕过」Codex 的审批策略。

OpenAI 官方给深度嵌入式客户端用的是 **Codex App Server**（见官方 App Server 文档）。社区维护的 **`codex-acp`** 适配器做的事是：以 stdio ACP agent 的身份启动，再对接 Codex App Server，把 ACP 请求／事件与 Codex 操作互译。截至 2026-10-22，官方文档站没有单独的「Codex 原生 ACP」页面；编辑器接入依赖这条适配器路径（或客户端从 Registry 代你装好的同一发行物）。

**我的用法**：日常只从 ACP Registry 装 Codex；只有客户端没有 Registry、或要钉死某个 npm 版本时，再手写 `npx -y @agentclientprotocol/codex-acp`。

## 2. ACP 和 MCP 怎么分工

两者常被混谈，但管的不是同一条边：

| | **ACP** | **MCP** |
|---|---|---|
| 解决什么 | 编辑器 ↔ Agent 的会话、流式输出、审批 UI | Agent ↔ 外部工具／数据（数据库、文档服务、API 等） |
| 谁当客户端 | 编辑器／IDE | Codex（或其他 Agent） |
| 典型入口 | Zed Agent Panel、JetBrains AI Chat 的 Agents | `~/.codex/config.toml`、客户端转发的 MCP 列表、`/mcp` |

一次任务里可以同时用两者：编辑器经 ACP 管 Codex 线程；Codex 再经 MCP 调外部服务。Zed 文档写明：Zed 里配置的 MCP 服务器**可以**经 ACP 转发给 External Agent；Agent 也可能继续读自己的原生 MCP 配置。JetBrains 在 Agents 页提供「Pass custom MCP servers」「Pass IntelliJ MCP server」开关，把 IDE 侧 MCP 暴露给已安装 Agent。

ACP **不会**自动把编辑器里的模型 API Key 变成 Codex 登录态，也**不会**取消 Codex 的沙箱与审批。

## 3. 适配器迁仓：用哪个仓库、哪个包

| 项目 | 状态（2026-10 核对） | 新安装应使用 |
|---|---|---|
| [zed-industries/codex-acp](https://github.com/zed-industries/codex-acp) | 已归档；README 写明开发迁走 | 不要再跟旧 npm `@zed-industries/codex-acp` 做新环境 |
| [agentclientprotocol/codex-acp](https://github.com/agentclientprotocol/codex-acp) | 当前适配器；基于 Codex App Server | npm：`@agentclientprotocol/codex-acp` |
| [ACP Registry](https://agentclientprotocol.com/get-started/registry) | 策展列表；当前列出 **Codex 2.2.2**，仓库指向 agentclientprotocol/codex-acp | Zed／JetBrains 的「Install from Registry」优先 |

适配器 README 写明的安装命令（核对时以仓库为准）：

```bash
npx -y @agentclientprotocol/codex-acp
```

或全局安装后检查版本：

```bash
npm install -g @agentclientprotocol/codex-acp
codex-acp --version
```

包内会带兼容的 `@openai/codex` 依赖。只有当你要指定另一份 Codex 二进制时，才设 `CODEX_PATH`：

```bash
CODEX_PATH=/path/to/codex npx -y @agentclientprotocol/codex-acp
```

认证由适配器在初始化时广告给客户端，README 列出的方式包括：**ChatGPT 登录**、环境变量 **`CODEX_API_KEY` 或 `OPENAI_API_KEY`**，以及客户端若协商了 gateway 能力时的自定义网关。无界面时可设 `NO_BROWSER=1` 隐藏浏览器登录项。密钥放进环境变量或系统密钥环，不要写进可提交的 settings／仓库。

## 4. 在 Zed 里用 Codex（ACP Registry）

按 Zed《External Agents》：

1. 打开 Registry：命令面板运行 `zed: acp registry`；或 **Agent Settings → External Agents → Add Agent → Install from Registry**。  
2. 安装列表中的 **Codex**（与 Registry 上的 Codex 条目对应）。  
3. 在 Agent Panel／Threads Sidebar 的新建线程菜单里选 **Codex**，开一条 Codex 线程。  
4. 用 **Codex 线程自己的登录／登出流程**完成认证。给 Zed Agent 配的 OpenAI API Key **不会**自动变成 Codex 凭证。

Zed 还说明：External Agent 的计费、条款与数据留存在你与 Agent 提供方之间；Zed 不把 External Agents 计入 Zed 自家模型计费。调试可开 `dev: open acp logs`。

若必须手动挂自定义 Agent，Zed 文档给出的是通用 `agent_servers` 形态（`type: custom`、`command`、`args`、`env`），命令指向能讲 ACP 的可执行文件。新环境优先 Registry，避免继续依赖已归档的 zed-industries 发行物。

## 5. 在 JetBrains 里用 Codex（Install From ACP Registry）

按 JetBrains AI Assistant ACP 文档：

1. 打开 **AI Chat**，在聊天模式选择器里选 **Install From ACP Registry**；或到 **Settings → Tools → AI Assistant → Agents**。  
2. 在 Agents 页安装 **Codex**（以 Registry 当时列出的名称为准）。  
3. 按需打开 **Pass custom MCP servers**／**Pass IntelliJ MCP server**，把 IDE 里已配的 MCP 暴露给 Agent。  
4. 首次使用时按提示完成该 Agent 的认证（文档写：Registry Agent 支持认证流程，首次可能要求 API key 等）。  
5. 在 AI Chat 里选中已安装的 Codex，再发提示。

文档还写明：连接 ACP Agent **不要求** JetBrains AI 订阅；**WSL 上目前不支持** ACP Agent；组织若通过 IDE Services／Central 管控，Registry 可见项可能被裁剪。更新／卸载仍在同一 Agents 页。出问题可 **Get ACP Logs**；需要更细请求／响应时再开 Registry 键 `llm.agent.extended.logging`（日志可能含聊天内容，分享前先脱敏）。

Registry 没有你要的 Agent、或要钉死启动命令时，用 **Add Custom Agent**：IDE 会创建／打开 `~/.jetbrains/acp.json`。文档给出的结构是 `agent_servers` 下每个显示名对应 `command`／`args`／`env`。手动跑 Codex 适配器时，把 `command`／`args` 指到本机的 `npx`（或全局 `codex-acp`）以及 README 中的包名即可，**不要**把 API Key 写进可提交文件；多数 Agent 更期望你先在终端完成登录，凭证落在用户配置里。

## 6. 其他 ACP 客户端：手动跑适配器

Zed／JetBrains 之外、且支持自定义 ACP agent 的客户端：用当前适配器作为 stdio 进程，例如：

```bash
npx -y @agentclientprotocol/codex-acp
```

客户端如何填写「命令 + 参数」、工作目录、环境变量，以**该客户端**文档为准，不能把 Zed 菜单步骤原样套过去。模型、审批、沙箱、Skills 仍由 Codex／适配器能力协商决定。

## 7. 第一次连接后怎么验

装好并登录后，先用只读任务确认工作目录，再各试一次拒绝／批准写文件：

```text
读取当前项目的 README，不要修改任何文件。
告诉我主要语言、启动命令和测试命令，并给出对应文件路径。
```

通过后再让它改一个**临时、可丢弃**的文件：看编辑器是否显示 diff；你点拒绝时磁盘是否不变；批准后内容是否真实写入。命令执行类操作同样先拒绝一次、再批准一次。

**我的用法**：验证通过前不要把审批策略放到最松；远程／SSH 项目要单独确认凭证落在哪一侧（Zed 文档提醒：本地钥匙串里的 LLM Key 不等于 External Agent 的凭证）。

## 8. 在 ACP 里能用到哪些 Codex 能力

以适配器 README（2.2.x）为准，常见能力包括：

- 认证：ChatGPT、API Key、（可选）自定义网关  
- 会话配置：模型、推理强度、审批与沙箱相关模式  
- 事件：命令、文件变更、权限请求、MCP 工具调用、终端输出、推理／计划、联网搜索等（具体展示取决于客户端有没有实现对应 UI）  
- 斜杠命令：`/status`、`/mcp`（含 `/mcp reconnect`）、`/skills`、`/goal`、`/review`、`/review-branch`、`/review-commit`、`/compact`、`/logout`，以及已配置的 Skills  
- 客户端经 ACP 提供的 MCP（stdio 命令型与 HTTP）

和原生 Codex App／CLI／官方 IDE 扩展比，ACP 路径多了一层适配器与客户端能力协商：**菜单里能点不等于协议能力齐全**。审查、合并、CI 仍按你的仓库规矩来；编辑器显示「成功」不能代替 Git 与测试验收。

## 9. 常见问题与排查

**登录失败／额度不对**  
先确认走的是 Codex 线程内登录，而不是编辑器全局的 OpenAI／Anthropic 提供方配置。ChatGPT 订阅与 API Key 计费路径不同，以 Codex 账号侧为准。

**装的是旧适配器**  
若 settings 或脚本仍指向 `zed-industries/codex-acp` 或 `@zed-industries/codex-acp`，改为 Registry 安装或 `@agentclientprotocol/codex-acp`。

**MCP 工具在 ACP 线程里看不到**  
分别查：编辑器是否把 MCP 转发给 External Agent；Codex 原生 `config.toml` 是否另有一份；适配器 `/mcp` 状态。Zed／JetBrains 都强调「两边都要看」。

**版本对不齐**  
分别核对：编辑器版本、Registry／npm 上的 Codex／适配器版本、本机 `CODEX_PATH` 是否指向过旧二进制。Zed 用 ACP logs；JetBrains 用 Get ACP Logs。

**官方协议选型**  
要自研深度宿主（认证、历史、审批、事件流）时，读 OpenAI **App Server** 文档。只要在已有 ACP 客户端里用 Codex，走 Registry／`codex-acp` 即可，不必自己实现 App Server 客户端。

## 10. 参考资料

- [Zed External Agents](https://zed.dev/docs/ai/external-agents)  
- [JetBrains AI Assistant · ACP](https://www.jetbrains.com/help/ai-assistant/acp.html)  
- [ACP Registry](https://agentclientprotocol.com/get-started/registry)（Codex 条目）  
- [agentclientprotocol/codex-acp](https://github.com/agentclientprotocol/codex-acp) · npm [`@agentclientprotocol/codex-acp`](https://www.npmjs.com/package/@agentclientprotocol/codex-acp)  
- 归档说明：[zed-industries/codex-acp](https://github.com/zed-industries/codex-acp)  
- OpenAI《[Codex App Server](https://learn.chatgpt.com/docs/app-server)》·《[Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)》  
- 协议站点：[agentclientprotocol.com](https://agentclientprotocol.com/)
