---
id: codex-agent-browser
title: Codex 用 agent-browser 做浏览器自动化：Skill 和 MCP 两种接法，snapshot 引用与常用命令
seo_title: Codex 用 agent-browser：Skill、MCP、snapshot 引用
description: agent-browser 是 Vercel Labs 的浏览器自动化 CLI，可以用 Skill 或 MCP 接到 Codex。本文按 0.41.2 写安装、两种接法、snapshot 的 @ref，以及允许域名。Linux 上打开了 example.com，没有登录网站。
lede: 让 Codex 用短命令打开页面、读可交互元素再点击。Skill 只负责发现这个工具，具体步骤向已安装的 CLI 要。
url: /guides/codex-agent-browser
status: published
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 18
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-09
date_modified: 2026-11-09
verified_on: 2026-11-09
tested_cli_version: 0.167.0
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex agent-browser, agent-browser mcp, snapshot @ref, npx skills add, Vercel Labs]
related: [mcp-getting-started, codex-chrome-devtools-mcp, codex-browser-login-state]
howto: true
faq:
  - q: 装上 Skill 就能点页面了吗？
    a: 不能。2026-11-09 装上的发现型 Skill 只有一份 SKILL.md，它要求先运行 agent-browser skills get core。浏览器命令来自已安装的 agent-browser CLI。
  - q: codex mcp list 里 Auth 是 Unsupported，还要 mcp login 吗？
    a: 这次 stdio 配置的 list 输出就是 Unsupported，并且 enabled 为 true。官方说明 codex mcp login 用于 Streamable HTTP。本文没有对这个服务器运行 mcp login。
  - q: 它和 Codex 内置浏览器是同一个东西吗？
    a: 不是同一个产品。agent-browser 由 Vercel Labs 维护，Apache-2.0。内置浏览器、浏览器扩展和 Computer Use 见浏览器操作一文。
---

# Codex 用 agent-browser 做浏览器自动化：Skill 和 MCP 两种接法，snapshot 引用与常用命令

> 本文在线版：[codexguide.io/guides/codex-agent-browser](https://codexguide.io/guides/codex-agent-browser)

> 核对依据：第三方仓库 [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) 的 README 与 [Apache-2.0 许可证](https://github.com/vercel-labs/agent-browser/blob/main/LICENSE)，文档站 [Skills](https://agent-browser.dev/skills)、[Commands](https://agent-browser.dev/commands) 和 [Security](https://agent-browser.dev/security)，以及 OpenAI 的 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)。2026-11-09 通过 GitHub API 看到 47,621 stars、3,258 forks，最近推送 `2026-11-08T10:03:53Z`；最新 Release `v0.41.2` 发布于 `2026-11-03T23:46:27Z`，npm 上的 `agent-browser` 版本同为 `0.41.2`。仓库创建于 `2026-01-11T05:38:15Z`。下面的命令输出都来自这台 Linux，Node.js 是 v22.23.4。没有把这个工具接到已登录的 Codex 会话，也没有配图。

这是 **Vercel Labs** 的第三方项目，不是 OpenAI 的内置浏览器。它提供一条浏览器 CLI：打开页面，把可交互元素收成带 `@e1` 这类引用的文本，再对引用点击或填写。浏览器在后台通过 Chrome DevTools Protocol 保持打开，所以下一步仍是一条短命令。

## 先看结论

适合用它把「打开这个 URL、读出可点的元素、点一下、再看地址栏」交给 Codex。不适合拿它代替 Codex 自己的内置浏览器登录态，也不适合代替 Chrome DevTools MCP 去读控制台和性能轨迹。

两种接法可以分开用：

- **Skill**：`npx skills add vercel-labs/agent-browser` 装进 `.agents/skills` 或 `~/.agents/skills`。装上的是发现用的薄说明，运行时再执行 `agent-browser skills get core`。
- **MCP**：`codex mcp add agent-browser -- agent-browser mcp`。2026-11-09 在 Codex CLI 0.167.0 的独立 `CODEX_HOME` 里，这条命令写成下面的 TOML。

```toml
[mcp_servers.agent-browser]
command = "agent-browser"
args = ["mcp"]
```

同一天用 CLI 和 `agent-browser mcp call` 都打开了 `https://example.com`。`snapshot -i` 与 MCP 的 `agent_browser_snapshot` 都返回一行 `link "Learn more" [ref=e1]`。点击 `@e1` 之后，`get url` 为 `https://www.iana.org/help/example-domains`。

## 安装 CLI

npm 包的 `engines` 写的是 Node.js `>=24.0.0`、pnpm `>=11.0.0`。这台机器是 Node.js v22.23.4，`npm install agent-browser@0.41.2` 打出了 `EBADENGINE`。后文的 `--version`、`doctor`、`open` 和 `mcp call` 仍然跑完了。跟做时以包声明的 Node 24 为准，不要把这次的警告当成上游放宽了要求。

README 的安装命令是全局安装，然后再下载浏览器：

```bash
npm install -g agent-browser
agent-browser install
```

本文没有改系统的 npm 全局目录，而是在临时目录安装了 `agent-browser@0.41.2`。`agent-browser --version` 输出 `agent-browser 0.41.2`。

`agent-browser install` 下载了 Chrome for Testing `157.0.8103.38`。安装结束时它提示：Linux 上如果启动失败，再运行 `agent-browser install --with-deps`。这台机器没有加 `--with-deps`。随后 `agent-browser doctor` 的汇总是 9 pass、0 warn、0 fail，其中包含一次 headless 打开 `about:blank`。doctor 还看到本机已有一份 Google Chrome；那是环境里原有的浏览器，不是这次安装步骤的前提。

README 还写了 Homebrew：`brew install agent-browser`，然后再 `agent-browser install`。本文没有 macOS，没有跑 Homebrew。不单独安装时，README 给出 `npx agent-browser open example.com`。本文没有用这条 `npx` 路径做后面的点击。

## 接法一：安装发现型 Skill

文档站写明，`npx skills add vercel-labs/agent-browser` 安装的是一份发现型 Skill，让 Cursor、Claude Code 或 Codex 知道有这个 CLI。真正的操作说明由 CLI 按自己的版本提供，避免 Skill 文件和命令行对不上。

2026-11-09 使用 `skills` 1.7.6，在隔离的主目录里安装，并加上 `--agent codex`、`-y` 和 `--copy`：

- 不加 `-g`：复制到当前项目的 `.agents/skills/agent-browser/SKILL.md`，安装结果的 `scope` 是 `project`，`agents` 是 `Codex`。
- 加上 `-g`：复制到 `~/.agents/skills/agent-browser/SKILL.md`，`scope` 是 `global`。

Codex 从仓库里的 `.agents/skills` 和用户目录的 `~/.agents/skills` 加载 Skill，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

装上的 `SKILL.md` 共 50 行。开头写明它是 discovery stub，要求在跑任何 `agent-browser` 命令之前先执行：

```bash
agent-browser skills get core
```

同一文件的 frontmatter 有 `hidden: true`。本文没有打开 Codex 的 `/skills` 列表，不知道这个字段会不会把它从选择器里藏起来。description 里还有一句，让代理优先用 agent-browser，而不是内置的浏览器工具。如果你希望 Codex 继续用自己的内置浏览器，先读完这份 description，再决定要不要全局安装。

这次安装器打印的安全评估是：Gen 为 Safe，Socket 为 0 alerts，Snyk 为 Med Risk，详情页是 [skills.sh/vercel-labs/agent-browser](https://skills.sh/vercel-labs/agent-browser)。这是 `skills` 1.7.6 当天的摘要，不是本知识库的审计结论。安装前的扫描方法见 [用 SkillSpector 扫描第三方 Skill](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。本文没有对这个目录跑 SkillSpector。

`agent-browser skills list` 在 0.41.2 上列出 9 个名字：`agentcore`、`core`、`derive-client`、`dogfood`、`electron`、`protected-vercel-deployments`、`slack`、`vercel-sandbox`、`webmcp-gen`。文档站的说明与此一致。`core` 是日常打开页面、snapshot、表单和会话；其余是 Electron、Slack、云浏览器等专门流程。需要哪一个，再执行 `agent-browser skills get <名字>`。

不想装 Skill 时，README 建议在 `AGENTS.md` 里写：

```markdown
Use `agent-browser` for browser automation. Before the first use, run
`agent-browser skills get core` and follow it.
```

这是上游给的用法约定。项目规则怎么放，见 [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。

## 接法二：把 MCP 写进 config.toml

Commands 文档写：`agent-browser mcp` 在 stdio 上启动 MCP 服务器。默认工具集是 `core`。扩大时用 `--tools all`，或用逗号组合，例如 `--tools core,network,react`。`--config` 指定一份可信配置，子进程只加载这一份，不再沿用户目录和项目目录发现配置。

官方示例是 JSON：

```json
{
  "mcpServers": {
    "agent-browser": {
      "command": "agent-browser",
      "args": ["mcp"]
    }
  }
}
```

Codex 不使用这段 JSON。0.167.0 的 `codex mcp add --help` 要求 stdio 服务器写成 `codex mcp add <名字> -- <命令...>`。在空的 `CODEX_HOME` 里执行：

```bash
codex mcp add agent-browser -- agent-browser mcp
```

输出是 `Added global MCP server 'agent-browser'.` 写入的配置就是上一节那三行 TOML。`codex mcp list` 显示 `enabled`，传输是 stdio，Auth 列是 `Unsupported`。`codex mcp get agent-browser` 显示 `command: agent-browser`、`args: mcp`。

带工具集的一次单独添加：

```bash
codex mcp add agent-browser -- agent-browser mcp --tools core,network,react
```

写入的是：

```toml
[mcp_servers.agent-browser]
command = "agent-browser"
args = ["mcp", "--tools", "core,network,react"]
```

`agent-browser mcp --help` 列出的配置档有 `core`、`network`、`state`、`debug`、`tabs`、`react`、`mobile`、`webmcp` 和 `all`。当天 `mcp call agent_browser_tools_profiles '{}' --tools core` 报告 core 有 29 个工具，all 有 156 个。不带 `--tools` 的 `mcp call` 把活动档报成 `all`；帮助文本写明，`mcp call` 在未限制时可以使用全部工具，而长期驻留的服务器默认仍是 `core`。给 Codex 用时，以 `args` 里有没有 `--tools` 为准。

常用工具名包括 `agent_browser_open`、`agent_browser_snapshot`、`agent_browser_click`、`agent_browser_fill`、`agent_browser_get_url` 和 `agent_browser_close`。本文用 `mcp call` 核对了打开、snapshot、点击和读取 URL，没有在 Codex 对话里让模型自己选工具。

桌面端、CLI 和 IDE 如何共用 `config.toml`，见 [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。本文只在 CLI 里执行了 `mcp add`。

## snapshot、@ref 和这次的命令

README 的核心循环是：

```bash
agent-browser open example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser get url
agent-browser close
```

2026-11-09 的实际输出：

```text
✓ Example Domain
  https://example.com/
```

```text
- link "Learn more" [ref=e1]
```

点击后：

```text
https://www.iana.org/help/example-domains
```

然后 `agent-browser close` 输出 `✓ Browser closed`。

MCP 路径用的是空参数打开 snapshot，点击时传入选择器：

```bash
agent-browser mcp call agent_browser_open '{"url":"https://example.com"}' --tools core
agent-browser mcp call agent_browser_snapshot '{}' --tools core
agent-browser mcp call agent_browser_click '{"selector":"@e1"}' --tools core
agent-browser mcp call agent_browser_get_url '{}' --tools core
```

`open` 的文本结果是 `Example Domain`，`_meta.agentBrowserVersion` 是 `0.41.2`。snapshot 的文本和 CLI 的 `snapshot -i` 相同。点击结果里有 `"clicked": "@e1"`。`get url` 的文本同样是 IANA 的那个地址。example.com 几乎只有一个链接，所以这次不能证明空 JSON 在复杂页面上也等于 `snapshot -i`。

引用只对应当次 snapshot。README 写明：导航或 DOM 变化之后要重新 snapshot，再用新的 `@ref`。点击被挡住、元素隐藏或禁用时，命令会失败，而不是报成功。

`agent-browser --help` 里和这次相关的一组命令还有 `fill`、`type`、`press`、`wait`、`screenshot`、`back`、`reload`，以及 `get url`。完整表在 [Commands](https://agent-browser.dev/commands)。本文没有逐条执行。

## 会话、登录态和允许域名

README 写：每个 `--session` 有自己的后台进程和浏览器；默认情况下，headless 浏览器在一小时没有命令后关闭。登录态、cookie 和 auth vault 在 [Sessions](https://agent-browser.dev/sessions) 与 [Security](https://agent-browser.dev/security)。本文只访问了不需要登录的 example.com，没有保存 cookie，也没有连接已经打开的 Chrome。

Security 页写，`--allowed-domains` 用来限制导航、子资源、WebSocket、EventSource 和 `sendBeacon`。在它支持的 Chromium 会话里还会关掉 WebRTC。允许列表不能和 `--cdp`、`--auto-connect`、`--profile`、`--restore`、`--state` 或某些启动参数一起用，因为那些模式可能在限制生效前就打开了页面。CDN 域名不在列表里时，页面上的脚本和字体也会被拦。环境变量是 `AGENT_BROWSER_ALLOWED_DOMAINS`。本文没有做一次「域名被拒绝」的实验。

给不信任的页面用时，把允许域名写进 MCP 的 `--config` 所指的那份可信配置，而不是只写在对话里。`eval` 能执行页面脚本；Security 页写，若还要收紧 WebSocket 拦截，需要用 `--action-policy` 拒绝 `eval`。本文没有编写 action policy。

## 和内置浏览器、Chrome DevTools MCP 怎么选

| 要做的事 | 先看哪一篇 |
| --- | --- |
| Codex 自己的预览、登录态、浏览器扩展或 Computer Use | [浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md) |
| 读控制台、网络请求和性能轨迹 | [Chrome DevTools MCP](./06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md) |
| 用短命令和 `@ref` 做打开、点击、填写 | 本文 |

三条可以同时装在一台机器上。发现型 Skill 的 description 会要求优先使用 agent-browser。需要内置浏览器时，不要全局安装这份 Skill，或者在任务里写明使用哪一个。

上线前按测试用例取证，仍用 [前端到端验收](../06-测试调试与质量保障/01-Codex做上线前端到端验收.md)。agent-browser 的 `screenshot` 可以留下画面，本文没有跑验收清单。

## 排障

**`agent-browser` 找不到。** 先看安装它的那个终端里的 PATH。本文用的是临时目录里的二进制，不是全局命令。

**Linux 上浏览器起不来。** 安装器自己的提示是再执行 `agent-browser install --with-deps`。先跑 `agent-browser doctor`，看 Chrome 和 Launch test 两段。本文的 Launch test 是通过的。

**MCP 已写入，对话里没有工具。** 新开一次会话。用 `codex mcp list` 确认名字和 `args`。stdio 服务器的 Auth 为 Unsupported 时，按 [MCP 入门](./01-Codex-MCP入门-config与mcp-login.md) 处理，不要对它执行 `codex mcp login`。

**点击报错或点到旧元素。** 重新 `snapshot`，只用新输出里的 `@ref`。

**Node 版本警告。** 0.41.2 的 `package.json` 要求 Node `>=24`。本文在 v22.23.4 上看到了 `EBADENGINE`，命令仍执行成功。这不构成对 Node 22 的支持承诺。

## 参考资料

- [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- [agent-browser.dev/skills](https://agent-browser.dev/skills)
- [agent-browser.dev/commands](https://agent-browser.dev/commands)
- [agent-browser.dev/security](https://agent-browser.dev/security)
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp)
- [v0.41.2](https://github.com/vercel-labs/agent-browser/releases/tag/v0.41.2)
