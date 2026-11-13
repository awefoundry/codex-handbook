---
id: codex-expo-plugin
title: Codex 安装 Expo 官方插件：Expo Skills 与 Expo MCP 一次装好，开发和发布 React Native 应用
seo_title: Codex 安装 Expo 插件：Expo Skills 与 Expo MCP 设置
description: Expo 官方插件把 Expo Skills 和 Expo MCP Server 打包在一起，Codex 用一条命令就能装好。本文说明安装和登录步骤、23 个 Skills 各管什么、MCP 能查文档、看 EAS 构建和截模拟器图，以及只装 Skills、手动加 MCP 和付费功能的区别。
lede: 一条命令装插件，再用 codex mcp login expo 登录 Expo 账号；框架类 Skills 免费可用，EAS 相关工具要看你的 Expo 套餐。
url: /guides/codex-expo-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI]
difficulty: 进阶
order: 19
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-10
date_modified: 2026-11-10
verified_on: 2026-11-10
official_ref: https://docs.expo.dev/skills
keywords: [Codex Expo 插件, Expo Skills, Expo MCP, codex plugin add expo@openai-curated, React Native, EAS]
related: [codex-mobile-mcp, mcp-getting-started, codex-chajian-rukou-yu-gongzuoliu]
faq:
  - q: 插件名到底是 expo 还是 expo2？
    a: 2026-11-09 Expo 在 X 上的推文里，命令显示为 expo2@openai-curated；Expo 文档（2026-11-02 更新）写的是 expo@openai-curated。本文按文档写。如果安装时提示找不到插件，在 Codex 里打开 /plugins 搜索 Expo，以列表里显示的名字为准。
  - q: 装了插件还要再 codex mcp add 吗？
    a: 不用。Expo 文档写明，Codex 和 Claude Code 的插件会同时注册 Expo MCP Server，只需要运行 codex mcp login expo 登录。没装插件、只想用 MCP 时，才用 codex mcp add expo --url https://mcp.expo.dev/mcp。
  - q: 不登录 Expo 账号能用吗？
    a: Skills 是写给 Codex 的说明文件，装上就能被调用。Expo MCP Server 需要 Expo 账号；部分工具（如 search_documentation）在文档里标注需要 Expo Services 付费套餐，EAS Simulator 和 EAS sandbox 会产生费用。
  - q: 本文实际装过这个插件吗？
    a: 没有。写作环境的 Codex 没有登录账号，codex plugin list --available 返回空列表，无法从 openai-curated 安装。本文的命令和功能来自 Expo 官方文档与 expo/skills 仓库，没有安装截图和运行输出。
---

# Codex 安装 Expo 官方插件：Expo Skills 与 Expo MCP 一次装好，开发和发布 React Native 应用

> 本文在线版：[codexguide.io/guides/codex-expo-plugin](https://codexguide.io/guides/codex-expo-plugin)

> 核对依据：Expo 官方文档 [Expo Skills](https://docs.expo.dev/skills)（页面标注 2026-11-02 更新）与 [Expo MCP Server](https://docs.expo.dev/mcp)，GitHub 仓库 [expo/skills](https://github.com/expo/skills) 的 `plugins/expo/`（2026-11-10 查看，`plugin.json` 版本 1.14.3），以及 Expo 在 X 上的公告（[2026-11-09T15:15Z](https://x.com/expo/status/2119811098928914752)）。**写作环境没有登录 Codex，无法从 openai-curated 安装插件**，本文没有安装截图，也没有运行输出；安装后以你本机 `/plugins` 里的显示为准。

这是 **Expo 团队**维护的插件，不是 OpenAI 编写的内置功能。它把两样东西装进 Codex：

- **Expo Skills**：一组写给 AI 代理的说明文件，告诉 Codex 按 Expo 当前的做法建页面、配路由、升级 SDK、发 App Store 等。
- **Expo MCP Server**：一个远程 MCP 服务器（`https://mcp.expo.dev/mcp`），让 Codex 能查 Expo 文档、看 EAS 构建和工作流、读 TestFlight 崩溃，配合本地开发服务器还能截模拟器的图、点按界面。

适合用 Expo 或 React Native 做 App，想让 Codex 按 Expo 官方写法干活、并直接查 EAS 构建状态的人。

## 先看结论

| 你想要 | 怎么装 |
|---|---|
| Skills 和 MCP 都要（推荐） | `codex plugin add expo@openai-curated`，再 `codex mcp login expo` |
| 只要 Skills | `npx skills add expo/skills` |
| 只要 MCP | `codex mcp add expo --url https://mcp.expo.dev/mcp` |
| 截模拟器图、点按界面 | 在上面基础上，项目里装 `expo-mcp` 并用 `EXPO_UNSTABLE_MCP_SERVER=1 npx expo start` 启动（SDK 54+） |

## 安装：一条命令，或在 /plugins 里装

Expo 文档给 Codex 的安装命令：

```bash
codex plugin add expo@openai-curated
```

也可以在 Codex 里输入 `/plugins`，从 `openai-curated` marketplace 找到 `expo` 安装。桌面 App 用户在 Plugins 页面搜索 Expo。

装完后开一个新对话（CLI 里输入 `/new`），让新会话加载插件里的 Skills。

> 插件名的出入：Expo 在 X 上的公告图里，命令显示为 `expo2@openai-curated`，而文档写的是 `expo@openai-curated`。本文按文档写。如果提示找不到，到 `/plugins` 里搜 Expo，以列表里的名字为准。

另外，OpenAI 公开的 [openai/plugins](https://github.com/openai/plugins) 仓库里，2026-11-10 看到的 `expo` 条目版本还是 1.0.2，而 expo/skills 仓库里的插件已经是 1.14.3。你实际装到哪个版本，取决于 Codex 远端 marketplace 当时提供的版本，装完可以用 `codex plugin list --json` 查看。

## 登录 Expo MCP

Expo 文档写明：**Codex 和 Claude Code 的 expo 插件会同时注册 Expo MCP Server，不需要再单独添加。**装好插件后只需登录：

```bash
codex mcp login expo
```

它会打开 Expo 账号的 OAuth 授权。使用 Expo MCP Server 需要：

- 一个 **Expo 账号**；
- 一个用最新 SDK 的 Expo 项目，新项目可以用 `npx create-expo-app@latest --template default@sdk-58` 创建（文档 2026-11-10 写的是 SDK 58）；
- 支持远程 MCP 的客户端，Codex 属于其中之一。

## 不装插件：只装 Skills，或手动加 MCP

只想要 Skills（比如你同时在用多个代理工具）：

```bash
npx skills add expo/skills
```

文档特别说明：**skills CLI 只装 Skills，不会注册 MCP。**

只想要 MCP：

```bash
codex mcp add expo --url https://mcp.expo.dev/mcp
```

这条命令会把服务器写进 Codex 的配置文件，并提示你登录 Expo 账号。MCP 在 Codex 里的配置和登录方式，见 [Codex MCP 入门：config 与 mcp login](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 23 个 Skills 怎么分

2026-11-10 查看 expo/skills 仓库，`plugins/expo/skills/` 下有 23 个 Skill。命名规则是：`expo-*` 管开源框架，`eas-*` 管 Expo 的云服务（EAS，部分收费）。

**框架类（16 个）**

| Skill | 用来做什么 |
|---|---|
| `expo-overview` | 所有 Expo / EAS 任务的入口，判断你要做什么，再分派给下面的 Skill |
| `expo-project-structure` | 新项目的目录结构（只用于新项目，不重排旧项目） |
| `expo-router` | Expo Router 路由、Stack、Tabs、模态框、页头 |
| `expo-native-ui` | 按 Apple HIG 做原生感界面、语义色、SF Symbols |
| `expo-ui` | 用 `@expo/ui` 写真正的 SwiftUI / Jetpack Compose 组件 |
| `expo-design-system` | 设计令牌和组件规范，修「看起来像 AI 生成」的界面 |
| `expo-animation` | Reanimated、手势、转场和触感反馈 |
| `expo-data-fetching` | 网络请求、React Query、缓存、离线和加载状态 |
| `expo-dom` | 用 DOM 组件在原生里跑 Web 代码 |
| `expo-web-to-native` | 把现有 React Web 项目迁到 iOS / Android |
| `expo-brownfield` | 把 Expo 嵌进已有的原生 App |
| `expo-module` | 用 Expo Modules API 写原生模块 |
| `expo-dev-client` | 构建和分发开发版客户端 |
| `expo-app-clip` | 给 iOS App 加 App Clip |
| `expo-examples` | 从官方约 70 个 `with-*` 示例里找对应的接入写法 |
| `expo-upgrade` | 升级 Expo SDK、修依赖问题 |

**EAS 服务类（7 个）**

| Skill | 用来做什么 |
|---|---|
| `eas-app-stores` | 用 EAS 构建并提交到 TestFlight、App Store、Google Play |
| `eas-hosting` | 部署 Expo 网站和 API 路由到 EAS Hosting |
| `eas-update` | EAS Update 热更新：channel、branch、runtime version |
| `eas-update-insights` | 看热更新的崩溃率、安装量和覆盖比例 |
| `eas-workflows` | 写 `.eas/workflows/` 里的 CI/CD 配置 |
| `eas-observe` | EAS Observe 性能数据 |
| `eas-simulator` | 云端 EAS Simulator，适合没有本地模拟器的机器 |

装好后不用记名字，正常描述需求，Codex 会自动选 Skill。Expo 文档给的示例：

```text
Add tab navigation and a modal to my app
```

```text
Create a CI/CD workflow that builds on every PR
```

```text
Upgrade my project to the latest Expo SDK
```

## Expo MCP 能做什么

文档把 MCP 能力分成两类。

**服务端能力**：只要连上远程 MCP 就能用，不需要本地开发服务器。2026-11-10 的工具表里包括：

- 文档：`read_documentation` 读某一页文档；`search_documentation` 搜文档（文档标注**需要 Expo Services 付费套餐**）。
- EAS 构建：`build_list`、`build_info`、`build_logs`、`build_run`、`build_submit`、`build_cancel`。
- EAS 工作流：`workflow_list`、`workflow_info`、`workflow_logs`、`workflow_run`、`workflow_validate`、`workflow_cancel`。
- 线上反馈：`testflight_crashes`、`testflight_feedback`、`appstore_reviews`、`playstore_crashes`、`playstore_reviews`。
- EAS Observe 性能数据：`observe_*` 系列。
- 云端模拟器和沙箱：`simulator_start`、`sandbox_create` 等。文档写明这两类会**启动计费的环境**。

**本地能力**（SDK 54 及以上）：截模拟器的图、按 testID 找元素并点按、打开 React Native DevTools、生成 expo-router 的路由表。需要在项目里装 `expo-mcp` 并带环境变量启动开发服务器：

```bash
npx expo install expo-mcp --dev
EXPO_UNSTABLE_MCP_SERVER=1 npx expo start
```

每次启动或停止开发服务器后，要在 Codex 里重新连接 MCP，Codex 才能拿到最新的能力列表。文档列出的限制：同一时间只支持一个开发服务器；iOS 的本地能力只支持模拟器，而且只能在 macOS 上用。

如果你只需要操作本地模拟器、不需要 EAS，也可以看 [Codex 接入 Mobile MCP：操作 iOS 模拟器与 Android 设备](../09-MCP与外部工具/11-Codex接入Mobile-MCP-操作iOS模拟器与Android设备.md)。

## 安全和费用要注意的几件事

- **有写操作的工具**：`build_submit` 会把构建提交到商店，`appstore_reply_review` 会发布公开的开发者回复。让 Codex 调这些工具前，保持 Codex 的审批，不要一路放行。
- **会计费的工具**：EAS Simulator、EAS sandbox、EAS 构建都会消耗 Expo 的额度或产生费用。可以先让 Codex 用 `usage_budget_get` 看可用额度。
- **数据流向**：Expo 文档说明它不用发给 MCP 的数据训练模型；本地能力的数据（比如模拟器截图）会经过 Expo MCP Server 再返回给 Codex，之后适用 Codex 和模型提供方的数据政策。
- 第三方插件装之前最好先看一眼内容，方法见 [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)。

## 常见问题

**插件名到底是 expo 还是 expo2？**

推文显示 `expo2@openai-curated`，文档写 `expo@openai-curated`。按文档装；找不到时到 `/plugins` 里搜 Expo，以列表为准。

**装了插件还要再 codex mcp add 吗？**

不用，插件已经注册了 Expo MCP Server，只需要 `codex mcp login expo`。

**不登录 Expo 账号能用吗？**

Skills 装上就能用。Expo MCP 需要 Expo 账号，部分工具需要付费套餐或会计费。

**本文实际装过这个插件吗？**

没有。写作环境的 Codex 没有登录账号，无法从 openai-curated 安装，本文没有安装截图和运行输出。

## 相关阅读

- [Codex 接入 Mobile MCP：操作 iOS 模拟器与 Android 设备](../09-MCP与外部工具/11-Codex接入Mobile-MCP-操作iOS模拟器与Android设备.md)
- [Codex MCP 入门：config 与 mcp login](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)
- [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)
