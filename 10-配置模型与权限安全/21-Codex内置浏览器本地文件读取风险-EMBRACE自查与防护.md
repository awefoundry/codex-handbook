---
id: codex-built-in-browser-local-file-risk
title: Codex 内置浏览器本地文件读取风险：EMBRACE 漏洞修复前，别打开不可信的本地 HTML
seo_title: Codex 内置浏览器本地文件读取：修复前别打开不可信 HTML
description: Forever Security 报告 Codex 内置浏览器打开本地 HTML 后可以读取电脑上的其他文件。本文核对研究文章、两篇报道和官方文档，说明触发方式、截至 2026-11-02 的修复状态，以及修复前怎么预览页面。
url: /guides/codex-built-in-browser-local-file-risk
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 21
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-02
date_modified: 2026-11-02
verified_on: 2026-11-02
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/browser
keywords: [Codex 内置浏览器漏洞, Codex EMBRACE, Codex 本地 HTML 读取文件, Codex 浏览器安全, Forever Security Codex]
related: [codex-browser-login-state, permissions-sandbox-approvals, codex-sandbox-host-trust]
howto: false
faq:
  - q: 只用 Codex CLI、从不用桌面端内置浏览器，还会中这条吗？
    a: 官方文档写明，内置浏览器在 Codex CLI 和 IDE 扩展里不可用，要在 ChatGPT 桌面端使用。这条报告针对的是桌面端内置浏览器里打开的本地页面。CLI 本身不提供这个浏览器。
  - q: 让 Codex 用内置浏览器打开 http://localhost 呢？
    a: 官方预览步骤就是先启动开发服务器，再打开本地的 http 地址，例如文档里的 http://localhost:3000/settings。用独立浏览器或本机开发服务器预览，和在内置浏览器里直接打开来源不明的 file:// 页面，不是同一件事。
  - q: 截至 2026-11-02，官方修好了吗？
    a: 截至这一天，Codex 更新日志最新正式版 0.166.0（2026-10-29）的说明里没有这条修复，openai/codex 的安全公告列表里也没有对应条目。不能把「Browser Use 拒绝 agent 自己打开 file://」写成已经修好。
---

# Codex 内置浏览器本地文件读取风险：EMBRACE 漏洞修复前，别打开不可信的本地 HTML

> 本文在线版：[codexguide.io/guides/codex-built-in-browser-local-file-risk](https://codexguide.io/guides/codex-built-in-browser-local-file-risk)

> 核对依据：Forever Security 2026-10-29 的技术文 [EMBRACE](https://forever.security/blog/embrace-hacking-5-ai-assistants-embedded-browsers-technical)，The Register 同日报道，Help Net Security 同日报道，OpenAI 文档 [Browser](https://learn.chatgpt.com/docs/browser) 与 [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)，以及 2026-11-02 再次查看的 [Codex 更新日志](https://learn.chatgpt.com/codex/changelog) 和 [openai/codex 安全公告](https://github.com/openai/codex/security/advisories)。本文不复现读取本地文件的做法，所以没有截图，也不附带可直接运行的页面代码。

在 ChatGPT 桌面端的 Codex 内置浏览器里打开一个本地 HTML 文件之前，先看这个文件从哪来。Forever Security 在 2026-10-29 公开的研究里，Codex 这一侧的问题是：本地 `file://` 页面没有被限制在项目目录内，页面可以直接读到电脑上的其他文件。截至 2026-11-02，公开渠道里还没有看到 OpenAI 写出的修复版本。

## 先看结论

修复说明出现之前，按这几条用：

- 不要在内置浏览器里打开来源不明的本地 HTML，哪怕链接是 Codex 自己给出来的。
- 预览自己的页面时，用独立浏览器，或先起本地开发服务器，再打开 `http://localhost` 或 `http://127.0.0.1`。
- 不要把来源不明的仓库标成信任。已经信任的项目，检查里面的 HTML 文件。
- 沙箱和审批管的是 Codex 执行的命令，管不住你亲手在内置浏览器里点开的页面。主机侧还会执行项目文件的其他情况，见 [Codex 沙箱与主机权限风险](./08-Codex沙箱与主机权限风险.md)。

内置浏览器只在桌面端。官方文档写明，Codex CLI 和 IDE 扩展里没有它。只用 CLI、从不开桌面端内置浏览器的人，不走这条点击路径。

## EMBRACE 研究测了哪五个工具

Forever Security 把这类问题称作 EMBRACE（embedded browser，内置浏览器被当成普通浏览器来信任）。他们测了 Cursor、GitHub Copilot、Codex、VS Code 和 Claude Desktop。五个产品的内置浏览器都比普通浏览器多了一些能力，普通浏览器里不成立的事在这里成立了。影响各不相同，技术文和 The Register 的归纳是：

- Cursor：页面内容可以进到 agent 的输入里，研究中做到了在主机上执行代码。Forever 写明 2026-09-10 报告，2026-10-01 已修复，厂商没有回复。
- GitHub Copilot：页面可以申报自己的地址，地址栏和 agent 看到的地址可以被伪造。他们在 1.1.27 上确认，GitHub 在 2026-10-13 的 1.1.29 里自行修复，Forever 没有发送这份报告。
- Claude Desktop 和 VS Code：本地页面被限制在项目目录，但这个检查没有覆盖 web worker，worker 里可以读到项目以外的文件。
- Codex：没有那层项目目录限制。本地页面自身就可以读任意文件，不需要再绕到 worker。

同一篇技术文写，Claude Desktop 与 VS Code 的目录限制「应该挡住逃出项目目录的读取」，检查跑在顶层页面，worker 里不跑。Codex 被写成例外：顶层页面上就没有这道文件读取围栏。

研究机器上的演示读到了 SSH 密钥、`.env`、npm 令牌、hosts 文件和私人文档。在 macOS 上，他们还用系统留下的 `.DS_Store` 列出目录。这些是影响范围，不是操作步骤。本文不转贴页面代码。

## Codex 的问题：本地页面没有目录限制

普通浏览器给本地文件一个不能随便读其他文件的来源。Forever 的描述是：Claude Desktop、Codex 和 VS Code 把 `file://` 页面的位置解析成可以读取相邻文件，以便预览项目。逃出项目目录本来应该被挡住。

在 Codex 上，他们的结论是这道围栏不存在，所以页面直接读取 `file://` 下的其他路径就能拿到内容。Claude Desktop 和 VS Code 上，同样的读取在顶层页面会被拒绝，只在 worker 里成功。

The Register 2026-10-29 的报道与此一致，并补充了时间线：Forever 于 2026-07-27 向 OpenAI 报告 Codex 的问题，发布文章时没有收到回复；缺陷仍未修复；OpenAI 发言人表示已知晓，正在处理。Help Net Security 同日写道，截至 10 月 29 日，Codex 和 VS Code 没有修复。

官方浏览器文档仍然把页面内容当成不可信上下文，并写明：网站权限只表示 ChatGPT 可以和这个站点交互，不表示页面内容可信，也不表示批准页面上的每一个动作。[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security) 讲的是命令沙箱、审批和网络，没有把「内置浏览器里的本地 HTML 可以读哪些文件」写成一项沙箱规则。

## 这个页面怎么送到你面前

技术文把投递写成一件平常的事：仓库看起来像一份普通的报告页面，恶意的部分是页面里普通的脚本引用。你让助手「按 README 把项目装好」，助手自己渲染出一个可点击的本地 `file://` 链接。需要的那一次点击，出现在助手给出的链接上。

所以风险点是**你在内置浏览器里打开了这个本地页面**，不是 Codex 在沙箱里多跑了一条命令。链接由 Codex 画出来，不表示目标文件已经检查过。

官方「Preview a page」仍包括三种打开方式：本地路由、file-backed 页面、公网页面。文件型预览还在文档里。修复说明出现之前，来源不明的文件不要走 file-backed 这一条。

## 修复前怎么用内置浏览器

内置浏览器怎么选、和扩展以及 Computer Use 的差别，见 [Codex 浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md)。和这次风险直接相关的用法是：

1. 预览自己正在改的页面时，先在终端或本地环境里启动开发服务器。
2. 在内置浏览器里打开 `http://localhost` 或 `http://127.0.0.1` 上的路由。官方举例是 `http://localhost:3000/settings`。
3. 来源不明的 HTML、压缩包里附带的「请用浏览器打开」的本地文件、以及 Codex 在陌生仓库 README 之后给出的 `file://` 链接，不要在内置浏览器里点开。要看内容，用独立浏览器，或先确认文件来源。
4. 页面上的说明、按钮和「安装步骤」都按不可信内容对待。官方写明，页面上的指示可能有误导或恶意。

这几条是使用上的隔离，不是厂商补丁。它们不能把一个已经打开的恶意本地页面变成安全的。

## 检查已经信任的项目

Help Net Security 转述研究者的建议：从每台机器的配置里列出已信任项目，检查这些项目中的 HTML，对照技术文里的利用方式。

Codex 的项目信任写在配置里。官方审批文档给出的例子是在用户配置中写 `[projects."/path/to/project"]`，并把 `trust_level` 设为 `untrusted`，用来收紧命令审批。已经信任、会加载项目本地配置的目录，就是要检查的范围。2026-11-02 的帮助文档没有给一个「导出全部已信任项目」的专用命令，本文不编造这条命令。可以打开 `config.toml` 里的 `projects` 表，再在对应目录中查看 `.html` / `.htm`。

检查时看的是：这个页面会不会在浏览器里去读项目以外的文件，以及它是不是仓库里本来就该存在的页面。发现来源对不上的 HTML，先不要用内置浏览器打开，把项目从信任里拿掉，再决定要不要继续用这个仓库。

## 怎么确认有没有修复

2026-11-02 重新查了两处：

- [更新日志](https://learn.chatgpt.com/codex/changelog) 最新的 Codex CLI 正式版是 0.166.0，日期 2026-10-29。该页能看到的条目里，没有 EMBRACE、内置浏览器本地文件读取或对应补丁的说明。同一天 npm `latest` 也是 0.166.0。预览版不在这里当修复依据。
- GitHub API 返回的 [openai/codex 安全公告](https://github.com/openai/codex/security/advisories) 只有一条：GHSA-w5fx-fh39-j5rw，2025-09-19 发布，标题是 Sandbox bypass due to bug in path configuration logic。那是更早的沙箱路径问题，在 CLI 0.39.0 修复，和这次浏览器报告不是同一件事。详见 [沙箱与主机权限](./08-Codex沙箱与主机权限风险.md)。

因此：**截至 2026-11-02，未见 OpenAI 公布这次本地文件读取的修复版本。** The Register 在 10 月 29 日记下的「已知晓并在处理」仍然只是处理中的表态，不是补丁说明。

仓库里另有用户讨论 Browser Use 会拒绝 agent 自己导航到 `file://`，例如 [openai/codex#42679](https://github.com/openai/codex/issues/42679)。那是 agent 工具的 URL 策略，和「人在内置浏览器里点开本地页面」不是同一条路径。[openai/codex#36552](https://github.com/openai/codex/issues/36552) 记录了另一面：用户打开的 `file://` 页面仍然可以在内置浏览器里显示。这些 issue 是用户报告，不是 OpenAI 的修复公告。在官方写出修复版本之前，不能把它们当成已经修好。

以后要确认，看两处就够：更新日志或安全公告里出现针对这次问题的版本号；届时再把桌面端升到那个版本，并仍不要用内置浏览器打开不可信的本地 HTML。

## 它和沙箱、审批各管什么

[权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) 管的是 Codex 自己跑的命令：能写哪些目录、能不能上网、越界时谁来批准。内置浏览器里已经打开的页面，按 Forever 的结果，读文件发生在浏览器这一侧。把审批调成「每次都问」，不会自动挡住这次点击。

这也和「项目说明文件里的提示注入」或「编辑器扩展被掉包」不是同一条链。那些问题要靠你喂给模型的内容和你安装的扩展来防。这一篇只覆盖内置浏览器打开本地 HTML。

## 常见问题

**官方是不是已经不让打开本地文件了？** 2026-11-02 的浏览器文档仍把 file-backed 页面列在预览步骤里。文档没有写「本地页面不能读取其他文件」。

**只打开自己写的 HTML，可以吗？** 你确认文件内容、并且它不会去读项目以外的路径时，风险和打开陌生仓库不同。来源不明时，改用独立浏览器或本地 http 服务。

**Claude Desktop 和 VS Code 是不是已经安全？** 按 10 月 29 日的研究和报道，二者的 worker 路径当时也没有修复，Microsoft 以 Workspace Trust 为由拒绝了 VS Code 的报告。那两个产品的后续状态以它们自己的公告为准，本文不代报。

**Cursor 和 Copilot 呢？** Forever 写 Cursor 于 2026-10-01 修复，Copilot 于 2026-10-13 在 1.1.29 修复。这不能外推到 Codex。

## 参考资料

- Forever Security，Gal Weizman，2026-10-29：[EMBRACE technical overview](https://forever.security/blog/embrace-hacking-5-ai-assistants-embedded-browsers-technical)
- The Register，2026-10-29：[Researchers find bugs in 5 AI developer tools](https://www.theregister.com/security/2026/10/29/researchers-find-bugs-in-5-ai-developer-tools-with-openai-and-microsoft-flaws-still-unpatched/5306508)
- Help Net Security，2026-10-29：[Researchers broke the browsers built into VS Code, Cursor, Copilot, Codex and Claude Desktop](https://www.helpnetsecurity.com/2026/10/29/research-ai-assistant-browser-vulnerabilities/)
- OpenAI：[Browser](https://learn.chatgpt.com/docs/browser)、[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)、[更新日志](https://learn.chatgpt.com/codex/changelog)
- 公告列表（2026-11-02 查询）：[openai/codex security advisories](https://github.com/openai/codex/security/advisories)
