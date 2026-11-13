---
id: codex-jetbrains-ide
title: JetBrains 中使用 Codex（2026-11 更新）：AI Assistant 三种登录、四种操作模式、Plan、Skills 与 MCP
seo_title: JetBrains 中使用 Codex：登录、操作模式、Plan 与 MCP
description: JetBrains 的 AI Assistant 可以在 AI Chat 里使用 Codex。本文按官方文档整理三种登录、操作模式和 Plan、AGENTS.md、Skills、MCP，以及 .aiignore 不生效。没有安装 JetBrains IDE，没有实测。
lede: 在 AI Chat 里选择 Codex，用 JetBrains AI、ChatGPT 账号或 OpenAI 直接签发的 API Key 登录。操作模式决定它能不能改文件和上网。
url: /guides/codex-jetbrains-ide
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [IDE]
difficulty: 进阶
order: 11
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-07-12
date_modified: 2026-11-09
verified_on: 2026-11-09
official_ref: https://www.jetbrains.com/help/ai-assistant/codex-agent.html
keywords: [JetBrains Codex, IntelliJ IDEA Codex, AI Assistant, Codex 操作模式, Plan 模式, .aiignore]
related: [codex-vscode-install, agents-md, permissions-sandbox-approvals, codex-plan-mode]
howto: false
faq:
  - q: 本文在 IDE 里点过这些开关吗？
    a: 没有。写作环境没有 IntelliJ IDEA、PyCharm 或其他 JetBrains IDE。菜单名、模式名和限制都来自 2026-11-09 的 JetBrains 帮助页。2026 年 1 月博客上的界面图已从本文删除，因为它们对不上现在的设备码登录和操作模式说明。
  - q: 操作模式到底叫 Workspace access 还是 Agent？
    a: 两页不一致。Codex 帮助页的操作模式列表是 Read-only、Workspace access、Auto review、Full access；同一页后文又写 Agent 和 Agent (full access)。Agents 总表写成 Read-only、Agent、Agent (full access)。本文把三组名字并列，没有界面可以核对哪一组出现在选择器里。
  - q: .aiignore 能挡住 Codex 吗？
    a: JetBrains 写明不能。Codex 帮助页和 Agents 总表都写 Codex 不遵守 AI Assistant 的 .aiignore，列在里面的文件仍可能被读取。
---

# JetBrains 中使用 Codex（2026-11 更新）：AI Assistant 三种登录、四种操作模式、Plan、Skills 与 MCP

> 本文在线版：[codexguide.io/guides/codex-jetbrains-ide](https://codexguide.io/guides/codex-jetbrains-ide)

> 核对依据：2026-11-09 的 JetBrains 帮助页 [Codex](https://www.jetbrains.com/help/ai-assistant/codex-agent.html)、[Activate agents](https://www.jetbrains.com/help/ai-assistant/activate-agents.html)、[Agents](https://www.jetbrains.com/help/ai-assistant/agents.html) 和 [Install AI Assistant](https://www.jetbrains.com/help/ai-assistant/installation-guide-ai-assistant.html)。2026-01 的博客 [Codex Is Now Integrated Into JetBrains IDEs](https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/) 只用于它写过的「自 2025.3 起」这句话。**本文没有安装 JetBrains IDE，没有登录，没有截图。** 仓库里 2026-01 的配图已删除：品牌图不解释操作，限时免费横幅已过期，认证画面上的 “Use API Key or Local Models” 和当前 BYOK 说明对不上。

Codex 在 JetBrains 里是 AI Assistant 的一个代理，用在 AI Chat 中。帮助页写它可以设计功能、修 bug、回答问题、审查代码。不需要另装一个名叫 Codex 的 IDE 插件。VS Code 系编辑器的扩展是另一条路，见 [VS Code、Cursor 和 Windsurf 安装 Codex](./06-VS-Code和兼容编辑器安装Codex.md)。

## 版本要求以哪一页为准

2026-01 的 JetBrains 博客写：从 IDE v2025.3 起，可以在 AI Chat 里使用 Codex，并安装最新的 AI Assistant 插件。2026-11-09 的 Codex 帮助页没有再写最低 IDE 版本。AI Assistant 的安装页写的是插件本身：商业 IDE 从 2023.3 起，这是插件的前提，不是 Codex 代理的单独说明。本文没有 IDE，不能核对旧版本打开 AI Chat 时会不会拒绝 Codex。跟做时以你本机插件页和 Codex 帮助页为准；博客里的 2025.3 只说明 2026 年 1 月的宣布范围。

## 准备项目

把项目按完整目录打开。Codex 帮助页写，自动附带的上下文只有当前文件和其中的选中文本；其他打开的文件、最近编辑的文件和更广的项目上下文不会自动附上。需要别的文件时，在输入框用 `@` 添加。

输入框里的指示器可以在两种状态之间切换：IDE context enabled 会附上当前文件名和选中文本；IDE context disabled 则不自动附上。本文没有看到这个指示器。

已有改动先提交或暂存，之后的 diff 才分得清哪些来自 Codex。

## 三种登录

[Activate agents](https://www.jetbrains.com/help/ai-assistant/activate-agents.html) 把集成代理的认证分成 JetBrains AI 订阅、API Key（BYOK）和提供商账号（OAuth）。Codex 三种都支持。提供商专用的第四种（文中的例子是 Anthropic Console）没有列在 Codex 名下。

当前认证显示在 **Settings | Tools | AI Assistant | Providers & API keys** 的 Agent Authorization。更换方式要先 Revoke，或在对话开头对 Configured authentication 选择 Reset，然后新开一场聊天。旧聊天保持原来的认证。

### JetBrains AI 订阅

文档步骤：打开 AI Chat，选择用 JetBrains AI 订阅登录，必要时完成 JetBrains 账号登录，再选择 Codex。Codex 需要先发送一条消息才会开始激活。然后 **Install and Continue**，在 Choose authentication method 里选 JetBrains AI。个人订阅显示为 JetBrains；组织分配的许可证显示为 Organization。用 JetBrains AI 激活之后，文档写其他 AI Assistant 功能也可以用。

### ChatGPT 账号，含设备码

文档步骤：在 AI Chat 选择 Codex，发送一条消息触发激活，**Install and Continue**，然后在提示里选 **ChatGPT** 或 **ChatGPT (device code)**，再完成授权。用提供商账号激活时，文档写只有这个代理出现在 AI Chat 里，其他 AI Assistant 功能仍不可用，除非另外打开 JetBrains AI 或配置 API Key。

GitHub Copilot 的小节写了远程开发时浏览器登录会失败。那段写的是 Copilot，不是 Codex。本文没有远程开发会话，不能把这段直接套到 Codex 的设备码上。

### API Key，只认 OpenAI 直接签发的密钥

Codex 帮助页的限制写在最前面：BYOK 时，Codex 只要 OpenAI 直接签发的 API Key。第三方密钥即使能调用 OpenAI 模型，当前也不支持。

Activate agents 里 Codex 的 API Key 步骤是：选择 Codex，发送消息，Install and Continue，选择 API Key，在 Third-party AI providers 里把 Provider 选为 OpenAI，输入密钥，Test Connection，再 OK。密钥只填在这个设置页。不要发到聊天里，也不要写进项目文件。

用 API Key 激活时，文档写该代理和提供商模型能支持的其他 AI Assistant 功能会一起可用，费用由该提供商计算。2026 年 1 月博客里的限时免费，帮助页已不再写成当前政策。价格以 IDE 和账号页为准。

## 四种操作模式，以及两页名字不一致

Codex 帮助页 “Select operation mode” 列出四个：

| 帮助页上的名字 | 同一段的说明 |
| --- | --- |
| Read-only | 改文件和访问互联网前都要批准 |
| Workspace access | 可以改项目工作区里的文件；改到项目外或访问网络之前会询问 |
| Auto review | 只在可能不安全的动作上请求批准 |
| Full access | 可以改这台机器上任何位置的文件，并且网络不受限制。某些敏感动作仍可能要求明确批准 |

选择方式是点操作模式控件，从列表里选。本文没有这个控件的画面。

同一页的 “Approve operations” 又写：可以改成 **Agent** 或 **Agent (full access)** 来调整上述询问行为。这里没有使用 Workspace access、Auto review、Full access 这几个词。

[Agents 总表](https://www.jetbrains.com/help/ai-assistant/agents.html) 把 Codex 的 Operation modes 写成 **Read-only、Agent、Agent (full access)**。总表没有 Workspace access、Auto review 和 Full access。总表把 Plan 放在 Claude Agent 的模式列表里，没有放进 Codex 的操作模式格。

三组名字以 2026-11-09 的原文为准。界面上最终显示哪一组，要在 IDE 里看选择器。不要把它们逐词换成 CLI 里的 Ask for approval、Approve for me 或 Full access。CLI 的审批见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。对照时只比较三件事：会不会改项目里的文件、会不会改项目外的文件、会不会在访问网络前询问。

Read-only 下，文档列出的批准按钮是 Allow Once、Allow for Session、Allow Commands Starting With 和 Reject。Allow Commands Starting With 会放行同一前缀的一组命令。建议的文件改动可以点开 diff；建议的命令可以用 Open in editor 看完整命令。

## Plan 是协作模式

Codex 帮助页把协作模式和操作模式分开：

- **Default**：按当前操作模式做任务。
- **Plan**：分析任务并给出实现计划，此时不做改动，方便你先看计划。

切换位置在操作模式旁边的协作模式选择器。本文没有点开它。

CLI 里的 `/plan`、Shift+Tab 和计划之后的执行方式，见 [Codex Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md)。JetBrains 页没有写 `/plan` 或 Shift+Tab。两边都叫 Plan，本文不能据此说它们是同一次实现。

## 模型、推理强度和 Fast

帮助页写：在模型列表里选择 Codex 使用的模型，并可以另选 Reasoning level。更高的推理档会在回答前做更多分析，复杂任务上可能更好，也可能更慢。模型名单随产品变化，本文不抄一份当前名单。

需要更快的交互时，操作模式旁边有 **Fast mode** 开关。文档写它加快输出，不换成更小的模型；费用会上升；并非所有模型都支持。支持范围以 OpenAI 的说明为准。本文没有打开这个开关，也没有账单。

上下文指示器在第一次回复之后出现，显示本场会话用掉的上下文百分比和 token 数。重新打开会话时保留上次的数字。换模型可能改变数字，因为窗口大小不同。窗口满了之后，文档写代理可能丢掉这场会话较早的内容。

## AGENTS.md、Skills 和 MCP

Codex 帮助页写：它从**项目根目录**的 `AGENTS.md` 读取持久说明，并加到每一项任务上。Agents 总表也把 Codex 的项目说明标成 `AGENTS.md`。CLI 还有从当前目录向上合并多层文件的规则，见 [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。JetBrains 页只写了根目录那一个文件。本文没有在 IDE 里放第二份 `AGENTS.md` 做对照。

Skills 的两种添加方式，按 Codex 页：

- 用 `$skill-installer` 从公开仓库安装，例如 openai/skills。
- 用 `$skill-creator` 按你的描述新建。

装好之后可以自动选用，或在提示词里用 `$` 前缀点名。`/skills` 查看当前有哪些。配置好的 MCP 工具不出现在 `/` 菜单里；代理认为需要时会自己调用，你也可以在提示词里点名。`/` 菜单里还有会话状态、会话管理和查看配置等命令，具体以 [Codex 命令文档](https://learn.chatgpt.com/docs/developer-commands) 为准。本文没有在 AI Chat 里输入 `/`。

把 IDE 里已经配好的 MCP 交给 Codex：

1. 在 **Settings | Tools | AI Assistant | Model Context Protocol (MCP)** 里配好服务器。
2. 打开 **Settings | Tools | AI Assistant | Agents**（Windows 和 Linux 上文档写的快捷键是 Ctrl+Alt+S）。
3. 打开 **Pass custom MCP servers**。
4. 确定。

本文没有 MCP 服务器，没有打开这个复选框。

DataGrip，以及安装了 Database Tools and SQL 插件的 IDE，文档还有一段数据库工具：先在 Settings | Tools | MCP Server 启用 MCP Server，复制 HTTP Stream 配置，再在 AI Assistant 的 MCP 页用 HTTP 粘贴为 `idea-http`。文档里的示例 URL 使用端口 `64344`，并写明端口可能不同，必须和 IDE 里显示的一致。然后在 MCP 页对 Codex 点 Auto-Configure。本文没有 DataGrip，没有这份 JSON 的本机结果。

## .aiignore 不会挡住 Codex

Codex 帮助页写：Codex 不使用 AI Assistant 的 `.aiignore`，列在里面的文件仍可能被处理。Agents 总表在 `.aiignore` 一列把 Codex 标为 Not respected。Junie 的同一列是 Respected。

因此，只把密钥、客户数据和私有配置写进 `.aiignore` 并不能挡住 JetBrains 里的 Codex。这些文件不要放进交给 Codex 的项目目录。自动上下文还有当前打开的文件和选中文本，敏感文件打开着的时候同样会被附上。

## 改完之后怎么看

帮助页写，不满意时可以在改动文件列表里回滚单个文件，或对全部文件点 Rollback。回滚前仍应看 diff。第一次任务先用 Read-only 或 Plan，确认它读到的文件是你以为的那些，再放宽操作模式。

本文没有一次真实的 diff，也没有运行测试。项目自己的测试或最小构建，仍由你在 IDE 里执行。

## 完成前再核对

- [ ] IDE 和 AI Assistant 插件的版本以帮助页和插件页为准，不单凭 2026-01 博客。
- [ ] 知道自己用的是 JetBrains AI、ChatGPT（或设备码）还是 OpenAI 直接签发的 API Key。
- [ ] 操作模式和 Plan 是两个选择器；模式名字在两页文档里不一致，以你 IDE 里的列表为准。
- [ ] 根目录 `AGENTS.md`、`$` 调用的 Skill，以及 Pass custom MCP servers，按需打开。
- [ ] `.aiignore` 没有被当成 Codex 的隔离边界。
- [ ] 聊天和项目文件里没有 API Key。

## 参考资料

- [Codex in AI Assistant](https://www.jetbrains.com/help/ai-assistant/codex-agent.html)
- [Activate agents](https://www.jetbrains.com/help/ai-assistant/activate-agents.html)
- [Agents](https://www.jetbrains.com/help/ai-assistant/agents.html)
- [Install AI Assistant](https://www.jetbrains.com/help/ai-assistant/installation-guide-ai-assistant.html)
- [Codex Is Now Integrated Into JetBrains IDEs](https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/)（2026-01，仅作当时的版本宣布）
- [OpenAI IDE 扩展文档](https://learn.chatgpt.com/docs/codex/ide)
