---
id: codex-mobile-mcp
title: Codex 接入 Mobile MCP：让 Codex 操作 iOS 模拟器、Android 模拟器和真机
seo_title: Codex 接入 Mobile MCP：操作 iOS 模拟器与 Android
description: Mobile MCP 是开源的移动端 MCP 服务器，可让 Codex 操作 iOS 模拟器、Android 模拟器和真机。本文用 Codex CLI 0.166.0 实测安装命令，并按 1.0.15 的 README 核对工具名、前置条件和权限边界。
url: /guides/codex-mobile-mcp
status: published
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 11
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-02
date_modified: 2026-11-02
verified_on: 2026-11-02
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/extend/mcp
keywords: [Codex Mobile MCP, mobile-mcp, Codex 移动端自动化, Codex 操作 iOS 模拟器, Codex Android 测试]
related: [mcp-getting-started, mcp-troubleshooting, android-skills-plugin]
howto: true
faq:
  - q: codex mcp list 里能看到 mobile-mcp，是不是就能点模拟器了？
    a: 不是。list 只说明配置里有这个服务器，而且是启用的。真的列出设备、截图和点击，要在有模拟器或真机的环境里，由已登录的 Codex 会话去调用工具。本文的测试机没有这些设备，也没有登录。
  - q: 和 Google 的 Android Skills 插件是一回事吗？
    a: 不是。Android Skills 是一组开发技能，随插件装进 Codex。Mobile MCP 是一个 MCP 服务器，通过无障碍快照或截图坐标去操作模拟器、真机上的原生 App。
  - q: 可以用它连上手机里正在使用的个人账号吗？
    a: 技术上它能截屏、读剪贴板和设备日志。个人手机上会有私人数据。用模拟器或专用测试机，不要把日常使用的手机交给这个服务器。
---

# Codex 接入 Mobile MCP：让 Codex 操作 iOS 模拟器、Android 模拟器和真机

> 本文在线版：[codexguide.io/guides/codex-mobile-mcp](https://codexguide.io/guides/codex-mobile-mcp)

> 核对依据：第三方仓库 [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp) 的 README 和 LICENSE（Apache-2.0），npm 注册表里的 `@mobilenext/mobile-mcp@1.0.15`，以及 OpenAI 文档 [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)。2026-11-02 在 Linux 上用独立的 `CODEX_HOME` 运行了 `codex-cli 0.166.0` 的 `mcp add`、`mcp list`、`mcp get`，并用 `npx -y @mobilenext/mobile-mcp@1.0.15 --version` 得到 `1.0.15`。测试机没有 iOS 模拟器、Android 模拟器或真机，也没有登录 Codex，所以没有设备画面。

Mobile MCP 是 [mobile-next](https://github.com/mobile-next) 发布的开源 MCP 服务器，不是 OpenAI 或 Apple、Google 的官方组件。它让 MCP 客户端操作 iOS 模拟器、Android 模拟器和对应真机上的原生 App：列设备、装卸 App、截图、按无障碍树或坐标点击、输入文字、看日志。Codex 只是它 README 里写明支持的客户端之一。

2026-11-02 通过 GitHub API 查询：10,202 星，915 个 fork，Apache-2.0，仓库创建于 2025-03-28，默认分支最近一次推送是 2026-11-02 03:51（北京时间）。npm 上 `@mobilenext/mobile-mcp` 的 `latest` 是 1.0.15，发布于 2026-10-31 00:05（北京时间），`engines.node` 为 `>=20`。

## 它是什么，适合做什么

README 写的用途是让 agent 通过结构化的无障碍快照，或基于截图的坐标点击，操作原生 iOS / Android 应用。适合已经能在本机启动的模拟器上做手工回归、填表、复现界面 bug、看设备日志。它不代替模拟器本身，也没有在本文的环境里跑通过任何一条设备操作。

和本知识库里另外两篇的分工：

- [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md) 讲配置文件、传输方式和登录。本文只加这一个服务器。
- [Google 官方 Android Skills 插件](../13-社区生态与项目评测/09-Codex安装Google官方Android-Skills插件.md) 提供的是 Android 开发技能，不驱动一台正在运行的设备。

README 还提到把探索过程写成 [mobilewright](https://github.com/mobile-next/mobilewright) 测试。那是另一个项目，本文不展开。

## 前置条件

README 的 Prerequisites 和平台表如下。本环境只满足其中的 Node.js。

| 目标 | README 写的条件 |
|---|---|
| 所有客户端 | Node.js v20 或更高。2026-11-02 这台机器是 v22.23.4 |
| iOS 模拟器 | Xcode 命令行工具，以及已经启动的模拟器（`xcrun simctl`） |
| iOS 真机 | 设备用 USB 连上，并且已信任这台电脑 |
| Android 模拟器 | Android SDK，以及正在运行的模拟器（`adb`） |
| Android 真机 | `adb`，并开启、授权 USB 调试 |

平台表把四类都标成支持。iOS 模拟器一行写的是 macOS 工具链；后文又写 iOS Simulators on macOS/Linux。以你机器上 `xcrun simctl` 是否真能列出模拟器为准，本文没有在 Linux 上启动过 iOS 模拟器。

## 在 Codex 里安装

官方 MCP 文档的通用形式是 `codex mcp add <名字> -- <命令...>`，例子里 npx 带 `-y`。Mobile MCP 的 README（2026-11-02 的 `main`）给 Codex 的命令不带 `--`，参数里也没有 `-y`。0.166.0 上两种写法都能写入配置。下面记录的是 README 那条，结果和 README 里的 TOML 一致。

在空的 `CODEX_HOME` 里执行：

```bash
codex mcp add mobile-mcp npx "@mobilenext/mobile-mcp@latest"
```

实际输出：

```text
Added global MCP server 'mobile-mcp'.
```

写入的 `config.toml`：

```toml
[mcp_servers.mobile-mcp]
command = "npx"
args = ["@mobilenext/mobile-mcp@latest"]
```

同一天 `@latest` 对应 1.0.15。想固定版本时，把参数改成 `@mobilenext/mobile-mcp@1.0.15`。官方文档那种带 `-y` 的写法是：

```bash
codex mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@1.0.15
```

0.166.0 实测这条会写成 `args = ["-y", "@mobilenext/mobile-mcp@1.0.15"]`。`-y` 让 npx 在包还没缓存时直接安装。README 的片段没有这个参数。

也可以不跑 `codex mcp add`，按 README 手写同一段 TOML。设置了 `CODEX_HOME` 时，文件在 `$CODEX_HOME/config.toml`，否则在用户目录的 `.codex/config.toml`。

README 还有一条自动安装：

```bash
npx @mobilenext/mobile-mcp@latest install
```

`1.0.15` 的 `--help` 写明，`install` 会把 mobile-mcp 加到本机检测到的 MCP 客户端里，`-y` 表示不再询问、全部写入。本文没有运行 `install`，避免改动测试机上的其他客户端。

默认传输是 stdio。要以 HTTP 方式监听时，README 和 `--help` 都有 `--listen`。`npx @mobilenext/mobile-mcp@latest --listen 3000` 绑定在 localhost 的 3000 端口，客户端连接 `http://127.0.0.1:3000/mcp`。这不是本文实测过的监听，只核对了帮助文本。需要鉴权时，README 使用环境变量 `MOBILEMCP_AUTH` 要求 Bearer token。

## 确认配置已经写上

```bash
codex mcp list
```

```text
Name        Command  Args                           Env  Cwd  Status   Auth
mobile-mcp  npx      @mobilenext/mobile-mcp@latest  -    -    enabled  Unsupported
```

```bash
codex mcp get mobile-mcp
```

```text
mobile-mcp
  enabled: true
  transport: stdio
  command: npx
  args: @mobilenext/mobile-mcp@latest
  cwd: -
  env: -
  remove: codex mcp remove mobile-mcp
```

`enabled` 表示配置里启用了这个服务器。`Auth` 为 `Unsupported`，是因为这个 stdio 服务器不走 Codex 的 OAuth 登录，不是安装失败。`codex --version` 输出 `codex-cli 0.166.0`。

这一步没有启动对话，也没有向服务器要工具列表。服务器要等 Codex 会话真正拉起 `npx` 之后才会出现 `mobile_*` 工具。连不上或工具不出现时，按 [MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md) 的顺序看进程、工具加载和超时。改完配置后重新打开会话。

## 工具名单

下面的名字逐条来自 2026-11-02 的 README「Available MCP Tools」，不是从记忆补的。本文没有调用它们。

**设备**

- `mobile_list_available_devices`：列出 iOS 模拟器、Android 模拟器和真机
- `mobile_get_screen_size`：屏幕像素尺寸
- `mobile_get_orientation` / `mobile_set_orientation`：读取或切换横竖屏
- `mobile_fold_device`：折叠屏的折叠与展开
- `mobile_set_location`：覆盖或清除 GPS 位置
- `mobile_clipboard`：读取或替换剪贴板

**云设备（Mobile Next Cloud，见下一节，本文不建议启用）**

- `mobile_login_to_cloud_provider`
- `mobile_list_remote_devices`
- `mobile_allocate_remote_device`
- `mobile_release_remote_device`

**应用**

- `mobile_list_apps`
- `mobile_get_foreground_app`
- `mobile_launch_app`
- `mobile_terminate_app`
- `mobile_install_app`：从 `.apk`、`.ipa`、`.app`、`.zip` 安装
- `mobile_uninstall_app`
- `mobile_clear_app_data`：README 写明用于 Android 和 iOS 模拟器

**屏幕**

- `mobile_take_screenshot`
- `mobile_save_screenshot`
- `mobile_list_elements_on_screen`
- `mobile_click_on_screen_at_coordinates`
- `mobile_double_tap_on_screen`
- `mobile_long_press_on_screen_at_coordinates`
- `mobile_swipe_on_screen`
- `mobile_start_screen_recording` / `mobile_stop_screen_recording`

**输入、链接和日志**

- `mobile_type_keys`
- `mobile_press_button`
- `mobile_open_url`：README 写的是在设备浏览器中打开 http/https。非标准 scheme 默认拒绝，要另设 `MOBILEMCP_ALLOW_UNSAFE_URLS`
- `mobile_get_device_logs`
- `mobile_list_crashes` / `mobile_get_crash`
- `mobile_batch_commands`：一次调用里按顺序跑多条工具

README 的验收方式是让 agent 执行 “list available devices”，返回正在运行的 iOS 模拟器、Android 模拟器和已连接设备。列表为空时，先确认模拟器已经启动。本文没有这条返回。

## 第一次使用时可以让 Codex 做什么

有模拟器之后，任务描述写具体的设备和结果，例如：列出当前设备；启动指定的包名；截一张图；点某个文案；把 logcat 或统一日志里的报错贴出来。坐标点击依赖截图尺寸，无障碍树依赖系统是否暴露控件。README 把这两种都写成可用手段，没有承诺每个 App 都有完整的无障碍树。

这些操作本文都没有跑。不要把上面的句子当成已经看到的界面。

## 真机和云设备

真机按平台表准备：Android 打开 USB 调试并在手机上点授权；iOS 真机用 USB 连接并信任电脑。授权对话框和驱动装法以当时的 Xcode、Android 文档为准，本文不另写一套。

README 用追踪链接推广 Mobile Next Cloud，可以用同一套工具去租云上的真机。那是项目方的云服务。本文不推荐，也不附带那个链接。不需要云设备时，不要调用 `mobile_login_to_cloud_provider` 和 `mobile_allocate_remote_device`。

## 权限和隐私

这个服务器一旦连上设备，工具列表里就包括截图、录屏、剪贴板、GPS 覆盖、应用数据清除和设备日志。日志和截图里可以有账号、通知和私人内容。

建议：

- 用模拟器或专用测试机，不要用日常手机。
- 测试机里不要登录个人账号，不要放真实短信、照片和支付应用。
- MCP 工具调用仍走 Codex 的审批。审批怎么收紧，见 [MCP 入门](./01-Codex-MCP入门-config与mcp-login.md) 里的工具权限一节。审批弹窗不能代替「这台设备上本来就没有私人数据」。
- `--listen` 如果绑到 `0.0.0.0`，局域网里的客户端也能连。README 写本地绑定时会做 Host 头防护；对非本机绑定，设置 `MOBILEMCP_AUTH`。本文没有开放过这个端口。

## 排障

**`codex mcp list` 里没有 mobile-mcp。** 看 `codex mcp add` 是否写进了当前这次使用的配置目录。设置了 `CODEX_HOME` 时，不会写到默认的用户目录。

**list 里有，对话里没有工具。** 新开一次会话。确认 Node.js 至少 v20，`npx` 能打印出 `1.0.15`。再按 MCP 排障看启动超时和 `enabled`。

**工具在，设备列表是空的。** README 的解释是模拟器没有启动，或 adb / `xcrun simctl` 看不见设备。先在终端里用这两个命令确认，再让 Codex 列设备。

**`install` 改错了客户端。** 本文没有跑交互式 `install`。已经跑过的话，用对应客户端自己的 MCP 配置把 `mobile-mcp` 删掉，或在 Codex 里执行 `codex mcp remove mobile-mcp`。

## 常见问题

**必须每次都用 `@latest` 吗？** README 的 Codex 片段用 `@latest`。2026-11-02 它等于 1.0.15。要复现本文的工具名单，把参数固定成 `@mobilenext/mobile-mcp@1.0.15`，以后上游改名时你不会跟着变。

**它和 Chrome DevTools MCP 都能「看屏幕」，用哪个？** Chrome DevTools MCP 看的是桌面 Chrome 里的网页。Mobile MCP 看的是 iOS / Android 上的原生界面。网页用前者。

**Linux 上能测 iOS 吗？** README 的平台表要求 Xcode 命令行工具和已启动的模拟器。本文没有验证 Linux 上的 iOS 模拟器。Android 模拟器取决于本机的 Android SDK 和 `adb`，同样没有在这里启动。

## 参考资料

- 仓库与许可证：[mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)（Apache-2.0，2026-11-02 查询）
- npm：`@mobilenext/mobile-mcp@1.0.15`
- OpenAI：[Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)
- 配置和排障：[Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)、[Codex MCP 排障](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)
