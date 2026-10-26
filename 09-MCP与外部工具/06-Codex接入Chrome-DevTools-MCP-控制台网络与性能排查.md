---
id: codex-chrome-devtools-mcp
title: Codex 接入 Chrome DevTools MCP：让 Codex 读控制台、网络请求和性能轨迹（1.12.0 实测）
seo_title: Codex 接入 Chrome DevTools MCP：控制台、网络与性能排查
description: Chrome DevTools MCP 让 Codex 直接打开 Chrome，读取控制台报错、网络请求和性能轨迹。本文用 Codex CLI 0.164.0 和 chrome-devtools-mcp 1.12.0 实测安装、常用工具、无头与隔离模式、连接已打开的 Chrome，以及隐私和权限设置。
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
date_modified: 2026-10-26
verified_on: 2026-10-26
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex Chrome DevTools MCP, chrome-devtools-mcp, codex mcp add chrome-devtools, Codex 前端调试, Codex 性能分析, Codex 控制台报错]
howto: true
faq:
  - q: Codex 怎么安装 Chrome DevTools MCP？
    a: 在终端运行 codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest，它会写入 ~/.codex/config.toml。需要本机有 Node.js LTS、npm 和当前稳定版 Chrome。CLI、IDE 扩展和桌面端共用这份配置。
  - q: 它和 Codex 内置浏览器的 Developer mode 有什么区别？
    a: Developer mode 是 ChatGPT 桌面端自带的功能，在 Settings > Browser 打开，配合内置浏览器或 Chrome 扩展使用，只能在桌面端用。Chrome DevTools MCP 是 Google Chrome DevTools 团队开源的 MCP 服务器，通过 config.toml 接入，CLI 和 IDE 扩展里也能用，参数可以自己控制。
  - q: Chrome DevTools MCP 会上传数据吗？
    a: 默认会向 Google 发送用量统计，可以用 --no-usage-statistics 关闭；性能工具默认会把被测 URL 发给 CrUX API 获取真实用户数据，可以用 --no-performance-crux 关闭。
  - q: Windows 上启动超时怎么办？
    a: 上游文档建议在 config.toml 里用 cmd /c npx 启动，补上 SystemRoot 和 PROGRAMFILES 环境变量，并把启动超时调到 20 秒（startup_timeout_ms = 20_000）。
---

# Codex 接入 Chrome DevTools MCP：让 Codex 读控制台、网络请求和性能轨迹（1.12.0 实测）

> 本文在线版：[codexguide.io/guides/codex-chrome-devtools-mcp](https://codexguide.io/guides/codex-chrome-devtools-mcp)

> 核对依据：[ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) 仓库的 README、[配置文档](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md)、[客户端配置文档](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/client-configurations.md)、[高级用法](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md) 和 [v1.12.0 发布说明](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.12.0)，以及 OpenAI 官方文档 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp) 和 [Browser](https://learn.chatgpt.com/docs/browser)。实测环境是 Linux 上的 `codex-cli 0.164.0`、`chrome-devtools-mcp 1.12.0` 和 Google Chrome 156，验证了 `codex mcp add/list/get`，并用 MCP 客户端直接调用服务器工具，对一个故意出错的本地页面读取控制台、网络请求、页面快照和性能轨迹。**测试机上的 Codex 没有登录**，所以下文没有 Codex 对话截图，工具输出是服务器的真实返回。核对日期 2026-10-26。

前端问题经常只在浏览器里出现：按钮点了没反应、接口返回 404、首屏很慢。以前要你打开开发者工具，把报错和请求复制给 Codex。接入 Chrome DevTools MCP 以后，Codex 可以自己打开页面、点按钮、读控制台和网络面板、录性能轨迹，再回到代码里改。

Chrome DevTools MCP 是 Google Chrome DevTools 团队维护的开源 MCP 服务器（Apache-2.0）。2026-10-26 查询时仓库有 54,142 个星标，最新版本 1.12.0 在 2026-10-22 21:47（北京时间）发布。OpenAI 的 MCP 文档也把它列在常用 MCP 服务器里。

## 它能让 Codex 做什么

服务器启动后会给 Codex 提供一组浏览器工具。1.12.0 默认启用 32 个，按用途大致分成五类：

| 用途 | 代表工具 |
|---|---|
| 打开和切换页面 | `new_page`、`navigate_page`、`list_pages`、`select_page`、`close_page` |
| 操作页面 | `click`、`fill`、`fill_form`、`type_text`、`press_key`、`hover`、`drag`、`upload_file`、`handle_dialog`、`wait_for` |
| 看页面 | `take_snapshot`（无障碍树快照）、`take_screenshot`、`get_css_styles`、`evaluate_script` |
| 调试 | `list_console_messages`、`get_console_message`、`list_network_requests`、`get_network_request` |
| 性能和环境 | `performance_start_trace`、`performance_stop_trace`、`performance_analyze_insight`、`lighthouse_audit`、`emulate`、`resize_page`、`take_heapsnapshot` |

另外还有 `screencast_start` / `screencast_stop`。完整说明见上游的 [工具参考](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)。

### 和 Codex 自带的浏览器能力怎么分

| 方式 | 在哪里用 | 适合 |
|---|---|---|
| 内置浏览器 `@Browser` | ChatGPT 桌面端 | 预览本地页面、在页面上批注、让 Codex 操作网页 |
| Developer mode（内置浏览器或 `@Chrome`） | ChatGPT 桌面端，Settings > Browser 打开 **Enable full CDP access** | 在桌面端里看控制台、网络、性能，使用完整 CDP 前会请你明确批准 |
| 浏览器扩展 `@Chrome` | ChatGPT 桌面端 + 你自己的 Chrome | 需要你已登录账号的网站 |
| Chrome DevTools MCP | CLI、IDE 扩展、桌面端，写在 `config.toml` 里 | 终端或编辑器里的前端调试，需要自己控制启动参数（无头、隔离、只连某个 Chrome） |

官方 [Browser 文档](https://learn.chatgpt.com/docs/browser) 写明，内置浏览器在 Codex CLI 和 IDE 扩展里不可用。如果你主要在终端里工作，Chrome DevTools MCP 是让 Codex 读到浏览器调试信息的直接办法。三种桌面端入口的区别见 [Codex 浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md)。

## 步骤 1：安装

运行前确认本机有：

- Node.js LTS 版本和 npm（服务器用 `npx` 启动）
- Google Chrome 当前稳定版或更新版本

上游 README 写明，官方只支持 Google Chrome 和 Chrome for Testing，其他 Chromium 内核浏览器不保证可用。

用 Codex CLI 添加：

```bash
codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

实测输出：

```text
Added global MCP server 'chrome-devtools'.
```

这条命令会在 `~/.codex/config.toml` 里写入：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest"]
```

CLI、IDE 扩展和桌面端读的是同一份配置，在 CLI 里加一次就行。

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

Codex 默认只等 MCP 服务器启动 10 秒（`startup_timeout_sec` 默认 `10`）。第一次运行时 `npx` 要下载包，容易超时，所以这里调到 20 秒。

## 步骤 2：确认 Codex 读到了配置

```bash
codex mcp list
```

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

进入 Codex 的终端界面后，输入 `/mcp` 可以看到正在运行的 MCP 服务器和工具。

## 步骤 3：实测，Codex 能从一个出错页面拿到什么

为了看清工具返回什么，我写了一个故意出错的本地页面：加载时打一条警告、请求一个不存在的 `/api/cart` 接口，点击 **Pay** 按钮时调用一个没定义的函数。

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

测试页很小，所以 LCP 只有几十毫秒（同一页面两次实测分别是 56 ms 和 74 ms）。真实项目里，可以让 Codex 再调用 `performance_analyze_insight` 展开某个 insight，看具体是哪段脚本或哪个请求拖慢了页面。

`field / real users` 一行显示 `n/a`，是因为本地地址在 CrUX（Chrome 用户体验报告）里没有真实用户数据。对线上公开网址，服务器默认会把网址发给 CrUX API 查询真实用户数据，见下文的隐私设置。

给 Codex 的提示词可以这样写：

```text
用 chrome-devtools 打开 http://localhost:3000/ ，录一次刷新的性能轨迹。
告诉我 LCP、CLS 和最主要的 insight，再在代码里找对应原因。
先给结论和证据，不要直接改代码。
```

## 常用启动参数

参数写在 `args` 里，跟在包名后面。下面是最常用的几个，完整列表见上游 [配置文档](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md)。

| 参数 | 作用 |
|---|---|
| `--headless` | 无界面运行，适合服务器和 CI |
| `--isolated` | 每次用临时用户目录，浏览器关闭后自动清理 |
| `--userDataDir` | 指定用户目录；默认是 `$HOME/.cache/chrome-devtools-mcp/chrome-profile` |
| `--channel` | 选择 Chrome 渠道：`stable`（默认）、`beta`、`dev`、`canary` |
| `--slim` | 只暴露 3 个工具（导航、执行脚本、截图），适合简单任务、节省上下文 |
| `--browserUrl` / `-u` | 连接一个已经打开远程调试端口的 Chrome，例如 `http://127.0.0.1:9222` |
| `--autoConnect` | 自动连接本机正在运行的 Chrome（需要 Chrome 144 及以上） |
| `--viewport` | 初始窗口大小，例如 `1280x720` |
| `--maxNavigationSaved` | 每个页面保留几次导航的控制台和网络记录，1–25，默认 3（1.12.0 新增） |

例如让 Codex 每次都用干净的无头浏览器：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--headless", "--isolated"]
```

实测加上 `--slim` 后，服务器只返回 `evaluate`、`navigate`、`screenshot` 三个工具，读不到控制台和网络请求。本文要做的调试工作不要开 `--slim`。

### 连接你已经打开的 Chrome

服务器默认会启动一个使用独立配置的新 Chrome。需要在你手动操作和 Codex 操作之间共用同一个浏览器状态时，有两种连法：

- **自动连接**（Chrome 144 及以上）：在 Chrome 里打开 `chrome://inspect/#remote-debugging` 开启远程调试，再给服务器加 `--autoConnect`。连接时 Chrome 会弹窗请你确认。上游文档提醒，服务器能访问该配置下所有打开的窗口。
- **手动端口**：用 `--remote-debugging-port=9222` 和一个**非默认**的 `--user-data-dir` 启动 Chrome，再给服务器加 `--browserUrl=http://127.0.0.1:9222`。上游文档提醒，端口开着时本机任何程序都能控制这个浏览器，不要在里面浏览敏感网站。

```bash
# macOS 示例（来自上游高级用法文档）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile-stable
```

## 隐私和权限设置

上游 README 的免责声明写明：服务器会把浏览器里的内容暴露给 MCP 客户端，客户端可以查看、调试和修改浏览器里的任何数据。不要在这个浏览器里放你不想让 Codex 看到的个人信息。

两项默认开启的数据发送：

- **用量统计**：默认开启，Google 收集工具调用成功率、延迟和环境信息。用 `--no-usage-statistics` 关闭；设置了 `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` 或 `CI` 环境变量时也会关闭。
- **CrUX 查询**：性能工具默认把被测网址发给 CrUX API。测内部系统时用 `--no-performance-crux` 关闭。

另外，服务器默认会定期检查 npm 上有没有新版本，设置 `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS` 环境变量可以关闭。

几个收紧范围的参数：

- `--no-javascript-evaluation`：关闭 `evaluate_script` 等执行任意脚本的入口。上游说明它**不是沙箱**，点击、输入触发的页面脚本照样会运行。
- `--blockedUrlPattern` / `--allowedUrlPattern`：按网址模式屏蔽或只允许访问某些地址（`--allowedUrlPattern` 需要 Chrome 149 及以上）。
- `--redactNetworkHeaders`：返回网络请求时隐去部分敏感请求头。实测不加这个参数时，`get_network_request` 会返回完整请求头；如果页面带登录 Cookie，这些内容会进入 Codex 的上下文。

在 Codex 这一侧，也可以用 MCP 配置项限制工具和审批：

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--isolated", "--no-usage-statistics", "--no-performance-crux"]
startup_timeout_sec = 20
tool_timeout_sec = 120
# 只开放调试需要的工具
enabled_tools = [
  "new_page", "navigate_page", "list_pages", "select_page",
  "take_snapshot", "take_screenshot", "click", "wait_for",
  "list_console_messages", "get_console_message",
  "list_network_requests", "get_network_request",
  "performance_start_trace", "performance_stop_trace", "performance_analyze_insight",
]
# 没有标记为只读的工具，调用前都要你确认
default_tools_approval_mode = "writes"
```

这些字段都来自 OpenAI 官方 [MCP 文档](https://learn.chatgpt.com/docs/extend/mcp)：`enabled_tools` / `disabled_tools` 控制可用工具，`default_tools_approval_mode` 可选 `auto`、`prompt`、`writes`、`approve`，`tool_timeout_sec` 默认 60 秒（录性能轨迹可能更久，所以这里调到 120）。不想用时把 `enabled = false` 写进这一节，不用删除配置。更多字段见 [config.toml 深入配置](../10-配置模型与权限安全/08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 常见问题

**Codex 里看不到 chrome-devtools 的工具**

先在终端运行 `codex mcp list`，确认状态是 `enabled`；再进入 Codex 输入 `/mcp` 看服务器有没有启动成功。第一次运行 `npx` 下载包较慢，启动超时就调大 `startup_timeout_sec`。

**提示找不到 Chrome**

服务器默认找稳定版 Chrome。装在非默认位置时，用 `--executablePath` 指定路径；只装了 Beta、Dev 或 Canary 时，用 `--channel` 指定渠道。

**在服务器或容器里跑**

没有图形界面时加 `--headless`。如果运行环境不允许启动新浏览器，用前面的 `--browserUrl` 连接沙箱外已经开好的 Chrome。

**工具太多，占上下文**

用 `enabled_tools` 只留需要的工具，或者在只需要打开网页、截图时使用 `--slim`。

## 小结

- 安装只要一行：`codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest`，CLI、IDE 扩展和桌面端共用。
- 它让 Codex 自己读控制台、网络请求、页面快照和性能轨迹，前端问题不用再手动复制报错。
- 默认会发送用量统计和 CrUX 查询，测内部系统时记得关掉；用 `--isolated` 和 `enabled_tools` 控制浏览器状态和工具范围。

需要做完整的上线前验收（测试用例、断言和截图证据）时，可以接着看 [Codex 做上线前端到端验收](../06-测试调试与质量保障/01-Codex做上线前端到端验收.md)。
