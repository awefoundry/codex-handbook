---
id: codex-chrome-devtools-mcp
title: "Codex 接入 Chrome DevTools MCP：读控制台、网络请求和性能轨迹，再装官方 7 个 Skills 和 chrome-devtools CLI"
seo_title: "Codex 接入 Chrome DevTools MCP：控制台、网络、Skills 与 CLI"
description: "Chrome DevTools MCP 让 Codex 直接打开 Chrome，读取控制台报错、网络请求和性能轨迹。本次按 1.13.0 更新：补上随包分发的 7 个官方 Skills 怎样复制到 Codex 的 Skills 目录、chrome-devtools CLI 的用法，以及 logpoints 和网络 mock 等新工具。"
url: /guides/codex-chrome-devtools-mcp
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 6
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-26
date_modified: 2026-11-23
verified_on: 2026-11-23
tested_cli_version: 0.171.0
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex Chrome DevTools MCP, chrome-devtools-mcp Skills, chrome-devtools CLI, Codex 前端调试, Chrome DevTools MCP 1.13]
howto: true
related: [mcp-getting-started, mcp-troubleshooting, create-codex-skill]
faq:
  - q: Codex 怎么安装 Chrome DevTools MCP？
    a: 在终端运行 codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest，它会写入 ~/.codex/config.toml。需要本机有 Node.js、npm 和当前稳定版 Chrome。2026-11-23 在 Codex CLI 0.171.0 上重跑，输出与 2026-10-26 的记录相同。
  - q: 1.13.0 的 7 个 Skills 怎样给 Codex 用？
    a: 上游 README 没有写 Codex 的插件安装命令。把 npm 包里 skills 目录下的 7 个文件夹复制到 ~/.agents/skills 或仓库的 .agents/skills。2026-11-23 复制到临时 Git 仓库后，codex debug prompt-input 列出了这 7 个名字。没有在会话里用 $ 调用，升级后要重新复制。
  - q: 什么时候用 chrome-devtools CLI，而不是 MCP？
    a: CLI 是在终端里直接调浏览器工具，不经过 MCP 客户端。1.13.0 上 chrome-devtools --version 打印 1.13.0，chrome-devtools status 在守护进程没启动时打印 chrome-devtools-mcp daemon is not running。文件访问用 --workspace 限制。不要按 main 上的 docs/cli.md 把 1.13.0 理解成默认可以读写任意路径。
  - q: logpoints 和网络 mock 默认就有吗？
    a: 2026-11-23 对 1.13.0 做 tools/list，默认 33 个工具里有 set_logpoints，没有 mock_network。网络 mock 要加 --categoryNetworkMocks。本文没有对页面设置过 logpoint 或 mock。
---

# Codex 接入 Chrome DevTools MCP：读控制台、网络请求和性能轨迹，再装官方 7 个 Skills 和 chrome-devtools CLI

> 本文在线版：[codexguide.io/guides/codex-chrome-devtools-mcp](https://codexguide.io/guides/codex-chrome-devtools-mcp)

> 核对依据：[ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) 的 README、[docs/cli.md](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md)、[v1.13.0 发布说明](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.13.0)，以及 OpenAI 文档 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp) 和 [Browser](https://learn.chatgpt.com/docs/browser)。2026-11-23 通过 GitHub API 查询：58,846 star，许可证 Apache-2.0，`pushed_at` 为 `2026-11-22T01:06:14Z`。默认分支最新提交 `ab911a6dd71ed4960c1c679f831c7b5607bc5505` 的时间是 `2026-11-21T17:42:45Z`，说明为 `fix(config): reject --viewport values with more than two parts (#3577)`。Release [chrome-devtools-mcp-v1.13.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.13.0) 发布于 `2026-11-11T12:40:09Z`（北京时间 20:40）。npm `chrome-devtools-mcp` 为 1.13.0。Codex CLI 为 `codex-cli 0.171.0`。工具列表用 1.13.0 的 stdio `tools/list` 计数。页面点击、控制台和性能轨迹的输出仍是 2026-10-26、`codex-cli 0.164.0`、`chrome-devtools-mcp 1.12.0`、Chrome 156 的记录，没有在 1.13.0 上重做。没有登录 Codex，没有配图。

前端问题经常只在浏览器里出现：按钮点了没反应、接口返回 404、首屏很慢。接入 Chrome DevTools MCP 以后，Codex 可以自己打开页面、读控制台和网络记录、录性能轨迹，再回到代码里改。1.13.0 的包里还带了 7 个官方 Skill 和一条 `chrome-devtools` 命令。

Chrome DevTools MCP 是 Google Chrome DevTools 团队维护的开源 MCP 服务器（Apache-2.0）。2026-11-23 查询时仓库有 58,846 个星标。1.13.0 在 2026-11-11 20:40（北京时间）发布。OpenAI 的 MCP 文档把它列在常用 MCP 服务器里。README 的插件安装只写了 Claude Code、Copilot／VS Code 和 Gemini CLI，没有写 Codex 的插件命令。Codex 这边按「把技能目录复制到你的 agent 的 skills 目录」处理。

## 它能让 Codex 做什么

2026-11-23 用本机安装的 `chrome-devtools-mcp@1.13.0` 做了一次 MCP `initialize` 和 `tools/list`。服务器信息是 `chrome_devtools`，版本 `1.13.0`。没有加额外分类旗标时，返回 **33** 个工具。2026-10-26 这篇文章按 1.12.0 记下的默认数量是 32。这次多出来、并且出现在默认列表里的是 `set_logpoints`。`mock_network` 和 `remove_network_mock` 不在这份默认列表里，见后面的 1.13.0 一节。

| 用途 | 1.13.0 默认列表里的工具 |
|---|---|
| 打开和切换页面 | `new_page`、`navigate_page`、`list_pages`、`select_page`、`close_page` |
| 操作页面 | `click`、`drag`、`fill`、`fill_form`、`hover`、`press_key`、`type_text`、`upload_file`、`handle_dialog`、`wait_for` |
| 看页面 | `take_snapshot`、`take_screenshot`、`get_css_styles`、`evaluate_script` |
| 调试 | `list_console_messages`、`get_console_message`、`list_network_requests`、`get_network_request`、`set_logpoints` |
| 性能和环境 | `performance_start_trace`、`performance_stop_trace`、`performance_analyze_insight`、`lighthouse_audit`、`emulate`、`resize_page`、`take_heapsnapshot`、`screencast_start`、`screencast_stop` |

上面 33 个名字就是这次 `tools/list` 的全部结果。连接服务器本身没有启动 Chrome。完整说明仍见上游 [工具参考](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)。main 上的工具参考可能比 1.13.0 的包更新，数量以你安装的那一版 `tools/list` 为准。

同一天用 `--slim` 再列了一次，仍然只有 `evaluate`、`navigate`、`screenshot` 三个。1.13.0 的 `--help` 也写 slim 是导航、执行脚本和截图。调试不要开 `--slim`。

### 和 Codex 自带的浏览器能力怎么分

| 方式 | 在哪里用 | 适合 |
|---|---|---|
| 内置浏览器 `@Browser` | ChatGPT 桌面端 | 预览本地页面、在页面上批注、让 Codex 操作网页 |
| Developer mode（内置浏览器或 `@Chrome`） | ChatGPT 桌面端，Settings > Browser 打开 **Enable full CDP access** | 在桌面端里看控制台、网络、性能，使用完整 CDP 前会请你明确批准 |
| 浏览器扩展 `@Chrome` | ChatGPT 桌面端 + 你自己的 Chrome | 需要你已登录账号的网站 |
| Chrome DevTools MCP | CLI、IDE 扩展、桌面端，写在 `config.toml` 里 | 终端或编辑器里的前端调试，需要自己控制启动参数 |

官方 [Browser 文档](https://learn.chatgpt.com/docs/browser) 写明，内置浏览器在 Codex CLI 和 IDE 扩展里不可用。如果你主要在终端里工作，Chrome DevTools MCP 是让 Codex 读到浏览器调试信息的直接办法。三种桌面端入口的区别见 [Codex 浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md)。

## 步骤 1：安装

运行前确认本机有 Node.js 和 npm，以及 Google Chrome 当前稳定版或更新版本。上游 README 写明，官方只支持 Google Chrome 和 Chrome for Testing。2026-11-23 这台机器上的 Chrome 是 157.0.8103.50。下面的页面操作记录用的是当时的 Chrome 156，没有在 157 上重做。

用 Codex CLI 添加：

```bash
codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

2026-10-26 在 `codex-cli 0.164.0` 上的输出，2026-11-23 在 `codex-cli 0.171.0`、新建的 `CODEX_HOME`、未登录时重跑，仍然是：

```text
Added global MCP server 'chrome-devtools'.
```

这条命令会在 `~/.codex/config.toml` 里写入：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest"]
```

CLI、IDE 扩展和桌面端读的是同一份配置。MCP 本身怎么配，见 [MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。

### Windows 11 要多写几行

上游客户端配置文档给 Codex 的 Windows 11 写法是用 `cmd /c` 启动，补上 Chrome 安装位置相关的环境变量，并把启动超时调长：

```toml
[mcp_servers.chrome-devtools]
command = "cmd"
args = [
    "/c",
    "npx",
    "-y",
    "chrome-devtools-mcp@latest",
]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000
```

这段沿用 2026-10-26 文章里的上游示例。2026-11-23 没有在 Windows 上重做。Codex 默认只等 MCP 服务器启动 10 秒（`startup_timeout_sec` 默认 `10`）。第一次运行时 `npx` 要下载包，容易超时，所以这里调到 20 秒。

## 步骤 2：确认 Codex 读到了配置

```bash
codex mcp list
```

0.171.0 上重跑的结果与 2026-10-26 相同：

```text
Name             Command  Args                        Env  Cwd  Status   Auth
chrome-devtools  npx      chrome-devtools-mcp@latest  -    -    enabled  Unsupported
```

`Auth` 一栏显示 `Unsupported` 是正常的：这是本地 stdio 服务器，不走 OAuth 登录。

```bash
codex mcp get chrome-devtools
```

```text
chrome-devtools
  enabled: true
  transport: stdio
  command: npx
  args: chrome-devtools-mcp@latest
  cwd: -
  env: -
  remove: codex mcp remove chrome-devtools
```

进入 Codex 的终端界面后，输入 `/mcp` 可以看到正在运行的 MCP 服务器和工具。本文没有打开 TUI。连不上或列表里没有工具时，见 [MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)。

## 步骤 3：实测，Codex 能从一个出错页面拿到什么

这一节的工具输出是 **2026-10-26**、`chrome-devtools-mcp 1.12.0`、Chrome 156 的记录，不是 1.13.0 的复测。

为了看清工具返回什么，当时写了一个故意出错的本地页面：加载时打一条警告、请求一个不存在的 `/api/cart` 接口，点击 **Pay** 按钮时调用一个没定义的函数。

```html
<!doctype html><html><head><meta charset="utf-8"><title>Checkout demo</title></head>
<body><h1>Checkout demo</h1><button id="pay">Pay</button>
<script>
console.warn('demo: legacy price format used');
fetch('/api/cart').then(r=>{ if(!r.ok) console.error('cart load failed: HTTP '+r.status); });
document.getElementById('pay').addEventListener('click',()=>{ undefinedFn(); });
</script></body></html>
```

页面用 `python3 -m http.server 8765` 在本机启动。下面是 MCP 服务器对每次工具调用的真实返回（服务器以 `--headless --isolated` 启动）。在 Codex 里，你只需要说“打开 http://127.0.0.1:8765/ ，点 Pay，告诉我控制台和网络有什么错误”，Codex 会自己选择调用这些工具。

**读控制台**：`list_console_messages`

```text
## Console messages
Showing 1-4 of 4 (Page 1 of 1).
msgid=1 [warn] demo: legacy price format used (1 args)
msgid=2 [error] Failed to load resource: the server responded with a status of 404 (File not found) (0 args)
msgid=3 [error] cart load failed: HTTP 404 (1 args)
msgid=4 [error] Failed to load resource: the server responded with a status of 404 (File not found) (0 args)
```

**读网络请求**：`list_network_requests`

```text
## Network requests
Showing 1-3 of 3 (Page 1 of 1).
reqid=1 GET http://127.0.0.1:8765/ [200]
reqid=2 GET http://127.0.0.1:8765/api/cart [404]
reqid=3 GET http://127.0.0.1:8765/favicon.ico [404]
```

两条 `Failed to load resource` 来自两个返回 404 的请求：`/api/cart` 和浏览器自动请求的 `favicon.ico`。`get_network_request` 还能拿到单个请求的请求头、响应头和响应体，排查接口问题时很有用。

**找到按钮并点击**：`take_snapshot` 返回页面的无障碍树，每个元素有一个 `uid`，后续操作用它定位。

```text
## Latest page snapshot
uid=1_0 RootWebArea "Checkout demo" url="http://127.0.0.1:8765/"
  uid=1_1 heading "Checkout demo" level="1"
  uid=1_2 button "Pay"
```

用 `click` 点击 `uid=1_2` 以后，控制台多了第 5 条消息。用 `get_console_message` 查看详情，可以拿到出错位置：

```text
ID: 5
Message: error> Uncaught ReferenceError: undefinedFn is not defined
### Stack trace
at  ((index):6:63)
Note: line and column numbers use 1-based indexing
```

`(index):6:63` 指向页面第 6 行第 63 列，也就是 `undefinedFn()` 这一处。Codex 拿到这些信息后，就能回到源码定位、修改，再重新打开页面验证。

## 步骤 4：录一段性能轨迹

这一节的数字同样是 2026-10-26、1.12.0 的记录。

`performance_start_trace` 可以刷新页面并自动录制，结束后返回指标和可以深入分析的 insight：

```text
Metrics (lab / observed):
  - LCP: 74 ms, event: (eventKey: r-1565, ts: 62139124756), nodeId: 4
  - LCP breakdown:
    - TTFB: 1 ms, bounds: {min: 62139050462µs, max: 62139051789µs}
    - Render delay: 73 ms, bounds: {min: 62139051789µs, max: 62139124756µs}
  - CLS: 0.00
Metrics (field / real users): n/a – no data for this page in CrUX
Available insights:
  - insight name: LCPBreakdown
```

测试页很小，所以 LCP 只有几十毫秒（同一页面两次实测分别是 56 ms 和 74 ms）。真实项目里，可以让 Codex 再调用 `performance_analyze_insight` 展开某个 insight。

`field / real users` 一行显示 `n/a`，是因为本地地址在 CrUX 里没有真实用户数据。对线上公开网址，服务器默认会把网址发给 CrUX API，见下文的隐私设置。

## 官方 7 个 Skills

1.13.0 的 npm 包里有 `skills/`。README 的表是这 7 个。下面的「做什么」来自各 `SKILL.md` 的 `description`，2026-11-23 从安装好的 1.13.0 包里读的。

| 目录 | description 在说什么 |
|---|---|
| `chrome-devtools` | 用 MCP 工具调试、自动化、看性能和网络。不适用于 `--slim` |
| `chrome-devtools-cli` | 写 shell 脚本或在终端里用 CLI 操作 Chrome DevTools |
| `a11y-debugging` | 按 web.dev 的指南做无障碍检查：语义 HTML、ARIA、焦点、键盘、点击目标和对比度 |
| `cookie-debugging` | Cookie、会话、登录失败、SameSite 和第三方 Cookie |
| `debug-optimize-lcp` | 用 MCP 工具排查和改善 LCP |
| `memory-leak-debugging` | 用堆快照工具查内存泄漏 |
| `troubleshooting` | `list_pages`、`new_page`、`navigate_page` 或服务器初始化失败时的连接问题 |

README 的插件装法只有三条，都不是 Codex：

- Claude Code：`/plugin marketplace add ChromeDevTools/chrome-devtools-mcp`，再 `/plugin install chrome-devtools-mcp@chrome-devtools-plugins`
- Copilot／VS Code：命令 **Chat: Install Plugin From Source**，填 `ChromeDevTools/chrome-devtools-mcp`
- Gemini CLI：`gemini extensions install --auto-update https://github.com/ChromeDevTools/chrome-devtools-mcp`

给 Codex 用时，按 README 的手动复制。官方例子写的是 Claude 的目录，Codex 的技能目录是 `~/.agents/skills` 或仓库里的 `.agents/skills`，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

```bash
npm i chrome-devtools-mcp@latest -g
mkdir -p ~/.agents/skills
cp -R "$(npm root -g)/chrome-devtools-mcp/skills/." ~/.agents/skills/
```

`chrome-devtools-cli` 这一份要求本机已经能运行 `chrome-devtools` 命令，所以要先全局安装这个包。

2026-11-23 把 1.13.0 包里的 7 个目录放进一个临时 Git 仓库的 `.agents/skills/`，用未登录的 `codex-cli 0.171.0` 运行 `codex debug prompt-input`。可用技能列表里出现了 `a11y-debugging`、`chrome-devtools`、`chrome-devtools-cli`、`cookie-debugging`、`debug-optimize-lcp`、`memory-leak-debugging`、`troubleshooting`，文件标记是 `r1/<名字>/SKILL.md`。`r1` 是这次输出给仓库技能根目录起的标记，不是你要创建的文件夹。这只说明 Codex 读到了 `name` 和 `description`。没有打开 `/skills` 菜单，没有发送 `$chrome-devtools`，也没有按技能正文去操作浏览器。

`troubleshooting/SKILL.md` 写着让代理按向导逐步排查连接。这是给代理执行的步骤。本文没有按它操作，也没有在文件里执行任何它指向的命令。

README 写：技能描述的是某一版工具。升级 MCP 或 CLI 之后要重新复制，否则技能可能让代理去调用已经改掉的工具或参数。插件安装用各自插件管理器更新；手动安装就是再复制一次。

## chrome-devtools CLI

包里还有 `chrome-devtools` 命令，用来在终端里调浏览器，不经过 MCP 客户端。官方安装是：

```bash
npm i chrome-devtools-mcp@latest -g
chrome-devtools status
```

2026-11-23 本机 `chrome-devtools --version` 打印 `1.13.0`。守护进程没启动时，`chrome-devtools status` 打印：

```text
chrome-devtools-mcp daemon is not running.
```

`chrome-devtools start --help` 写：headless 默认 **true**；isolated 默认 **true**，除非设置了 `userDataDir`、`autoConnect`、`browserUrl` 或 `wsEndpoint`。这是 CLI 的默认值。MCP 服务器的 `chrome-devtools-mcp --help` 里，`--headless` 和 `--isolated` 默认都是 **false**。同一套旗标，两条命令的默认不一样。

文件工具的范围，以 1.13.0 的 `chrome-devtools start --help` 为准：

- `--workspace`（也叫 `--filesystemRoot`）可以写多次，默认值标明是操作系统的临时目录。
- `--allowUnrestrictedPaths` 默认 false。帮助写：没有协商 MCP roots 时，读写本地文件的工具默认限制在临时目录。这个旗标已标成 deprecated，并写 `Use --workspace=/ instead.`

同一天打开的 main 上 [docs/cli.md](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md) 写的是：CLI 默认不限制文件系统，用 `--workspace` 来收紧；`--allow-unrestricted-paths` 不能和 `--workspace` 一起用。这和 1.13.0 的 `--help` 相反。使用 1.13.0 时按 `--help`，不要按 main 上这几句把默认当成不受限。本文没有启动守护进程，也没有让 CLI 打开网页。

CLI 适合你或脚本要直接调用 `navigate_page`、`take_screenshot` 这类命令的时候。Codex 在对话里调用浏览器，仍然走上面的 MCP 配置。两套可以同时装，它们来自同一个 npm 包。

## 1.13.0 的 logpoints 和网络 mock

[v1.13.0 发布说明](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.13.0) 的新增功能是：基于 DevTools BreakpointManager 的 logpoints、按页面的网络 mock，以及上游网络 mock 响应。

**logpoints。** 默认 `tools/list` 里的工具名是 `set_logpoints`。1.13.0 的工具说明写：它设置所选页面的完整 logpoint 列表，不在列表里的会被移除，空列表表示全部移除。logpoint 在某一行执行时把表达式打到控制台，不暂停，也不改源码，和 DevTools Sources 面板里的 logpoint 同类。`--javascriptEvaluation` 设为 false（命令行上是 `--no-javascript-evaluation`）时，帮助写明 `evaluate_script`、`set_logpoints` 和 slim 的 evaluate 都会关掉。本文没有在页面上设置过 logpoint。

**网络 mock。** 1.13.0 包里有 `mock_network` 和 `remove_network_mock`，类别是 network mocks。`chrome-devtools-mcp --help` 写 `--categoryNetworkMocks` 要设为 true 才会包含这些工具，改这个选项需要重启服务器。默认 `tools/list` 里没有它们。工具说明写：不带动作时列出 mock；提供 `body` 或 `upstream` 会更新对应的 route 和 resourceType；`body` 和 `upstream` 互斥；`upstream` 是服务器端对 GET/HEAD 的抓取；mock 会关掉该页的 HTTP 缓存并拦截请求，服务工作线程可以绕过 mock。本文没有对任何页面下过 mock，也没有打开 `--categoryNetworkMocks` 再列一次工具。

## 常用启动参数

2026-11-23 在 1.13.0 的 `chrome-devtools-mcp --help` 里核对过下表这些旗标仍然存在。除了 `--slim` 的三个工具名又列了一次，没有把每种模式再跑一遍。

| 参数 | 作用 |
|---|---|
| `--headless` | MCP 服务器默认 false。CLI 的 `start` 默认 true |
| `--isolated` | MCP 服务器默认 false。CLI 的 `start` 默认 true，除非指定了用户目录或连接已有浏览器 |
| `--userDataDir` | 指定用户目录。帮助写的默认位置是 `$HOME/.cache/chrome-devtools-mcp/chrome-profile`，非 stable 渠道会加后缀 |
| `--channel` | `stable`（默认）、`beta`、`dev`、`canary` |
| `--slim` | 只暴露 `evaluate`、`navigate`、`screenshot` |
| `--browserUrl` / `-u` | 连接已经打开远程调试端口的 Chrome，例如 `http://127.0.0.1:9222` |
| `--autoConnect` | 自动连接本机正在运行的 Chrome。帮助写需要 Chrome 144 及以上，并要在 `chrome://inspect/#remote-debugging` 打开远程调试 |
| `--viewport` | 例如 `1280x720`。1.13.0 之后的 main 还有一条修复：拒绝多于两段的 viewport 值。1.13.0 的帮助仍写接受 `1280x720` 这种例子 |
| `--maxNavigationSaved` | 每个页面保留几次导航的控制台和网络记录，1–25，默认 3 |

例如让 MCP 每次都用干净的无头浏览器：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--headless", "--isolated"]
```

### 连接你已经打开的 Chrome

服务器默认会启动一个使用独立配置的新 Chrome。需要和你手动开的浏览器共用状态时：

- **自动连接**（帮助写 Chrome 144 及以上）：在 Chrome 里打开 `chrome://inspect/#remote-debugging`，再给服务器加 `--autoConnect`。
- **手动端口**：用 `--remote-debugging-port=9222` 和一个非默认的用户目录启动 Chrome，再给服务器加 `--browserUrl=http://127.0.0.1:9222`。

```bash
# macOS 示例（来自上游高级用法文档，本文没有在 macOS 上执行）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable
```

## 隐私和权限设置

上游 README 的免责声明写明：服务器会把浏览器里的内容暴露给 MCP 客户端。不要在这个浏览器里放你不想让 Codex 看到的个人信息。1.13.0 启动时也会把这段免责声明打到 stderr。

两项默认开启的数据发送，1.13.0 的帮助里仍有对应旗标：

- **用量统计**：`--no-usage-statistics` 关闭。帮助写设置了 `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` 或 `CI` 时也会关闭。
- **CrUX 查询**：`--no-performance-crux` 关闭性能工具里的实地数据。

另外，服务器默认会检查更新。设置 `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS` 可以关掉这次检查。这是 1.13.0 启动代码里的环境变量名；本文用它跳过了列工具时的更新检查。

几个收紧范围的参数，1.13.0 的帮助里仍然有：

- `--no-javascript-evaluation`：关掉 `evaluate_script`、`set_logpoints` 和 slim evaluate。帮助写明这不是沙箱，点击和输入触发的页面脚本仍会运行。
- `--blockedUrlPattern` / `--allowedUrlPattern`：按网址模式拦截或只允许某些地址。`--allowedUrlPattern` 的帮助写需要 Chrome 149 及以上。
- `--redactNetworkHeaders`：默认 false。2026-10-26 不加这个参数时，`get_network_request` 会返回完整请求头。1.13.0 没有重做那一次请求。

在 Codex 这一侧，也可以用 MCP 配置项限制工具和审批：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--isolated", "--no-usage-statistics", "--no-performance-crux"]
startup_timeout_sec = 20
tool_timeout_sec = 120
enabled_tools = [
  "new_page", "navigate_page", "list_pages", "select_page",
  "take_snapshot", "take_screenshot", "click", "wait_for",
  "list_console_messages", "get_console_message",
  "list_network_requests", "get_network_request",
  "performance_start_trace", "performance_stop_trace", "performance_analyze_insight",
]
default_tools_approval_mode = "writes"
```

这些字段来自 OpenAI 官方 [MCP 文档](https://learn.chatgpt.com/docs/extend/mcp)。`default_tools_approval_mode` 可选 `auto`、`prompt`、`writes`、`approve`。不想用时把 `enabled = false` 写进这一节。更多字段见 [config.toml 深入配置](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 常见问题

**Codex 里看不到 chrome-devtools 的工具**

先在终端运行 `codex mcp list`，确认状态是 `enabled`。第一次运行 `npx` 下载包较慢，启动超时就调大 `startup_timeout_sec`。`/mcp` 要在 Codex 会话里看，本文没有打开那个界面。

**提示找不到 Chrome**

服务器默认找稳定版 Chrome。装在非默认位置时，用 `--executablePath` 指定路径。只有 Beta、Dev 或 Canary 时，用 `--channel`。

**在服务器或容器里跑**

MCP 服务器的 `--headless` 默认是 false。没有图形界面时要自己加上 `--headless`。1.13.0 的发布说明里有一条修复：找不到 X server 时提示使用 `--headless`。本文没有制造这个报错。

**工具太多，占上下文**

用 `enabled_tools` 只留需要的工具，或者在只需要打开网页、截图时使用 `--slim`。

**升级之后技能还在让代理调用旧参数**

手动复制的 7 个 Skill 不会跟着 npm 包自己更新。升级 `chrome-devtools-mcp` 之后，再复制一次 `skills/`。

**想用网络 mock，但工具列表里没有**

默认不包含。给服务器加上 `--categoryNetworkMocks`，然后重启这一条 MCP。本文没有用它打过请求。

## 小结

- 安装仍然是 `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest`。0.171.0 上重跑，`mcp list` 和 `mcp get` 的结果与 2026-10-26 相同。
- 1.13.0 默认 `tools/list` 是 33 个工具，其中包含 `set_logpoints`。页面点击和性能数字仍是 1.12.0 的记录。
- 7 个官方 Skill 复制到 `.agents/skills` 后，0.171.0 能在 `prompt-input` 里列出它们。README 没有 Codex 插件命令。
- `chrome-devtools` CLI 和 MCP 的 headless、isolated、文件目录默认值不一样。1.13.0 的 CLI 帮助把文件工具默认限制在临时目录；main 上的 docs/cli.md 仍写默认不受限。

需要做完整的上线前验收时，可以接着看 [Codex 做上线前端到端验收](../06-测试调试与质量保障/01-Codex做上线前端到端验收.md)。
