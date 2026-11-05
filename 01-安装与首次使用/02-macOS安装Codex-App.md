---
id: macos-install-codex-app
title: macOS 安装 Codex App：下载、安装、首次登录与进入 Codex 工作区
seo_title: macOS 安装 Codex App：官方下载、拖入应用程序与首次登录
description: 在 Mac 上从 chatgpt.com/download 安装整合了 Codex 的 ChatGPT 桌面端：核对 macOS 14 与芯片、安装到「应用程序」、用 ChatGPT 登录，再切换到 Codex 并打开本地文件夹。本稿未在真机 Mac 复验，配图待补。
lede: Codex 已并入 ChatGPT 桌面端。在 Mac 上只要走官方下载、装进「应用程序」、完成浏览器登录，就能进 Codex 工作区打开本地项目。
url: /guides/macos-install-codex-app
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app
keywords: [macOS 安装 Codex, Codex App 安装, ChatGPT 桌面端 macOS, Codex 首次登录, 打开本地文件夹]
related: [login-codex, open-first-local-project, app-cli-ide-cloud-choice, desktop-crashpad-disk-space]
howto: true
faq:
  - q: 现在还有单独的「Codex App」安装包吗？
    a: 没有必要再找旧的独立 Codex 安装包。自 2026-07-09 起，Codex 已并入 ChatGPT 桌面端（macOS／Windows）。已有 Codex 用户按应用内更新即可；首次安装从 chatgpt.com/download 下载新的 ChatGPT 桌面端，登录后在左上角切到 Codex。
  - q: 必须用付费套餐才能装桌面端吗？
    a: 官方说明更新后的桌面端可在各 ChatGPT 套餐使用（含 Free），但可用模型、额度与部分能力仍随套餐、工作区与 rollout 变化。能打开应用不等于某项 Codex 云功能一定可用。
  - q: 登录要用 API Key 还是 ChatGPT？
    a: 第一次本地练习优先用 ChatGPT 登录（未登录页选 Continue to sign in，走浏览器授权）。需要按量计费时再选 Sign in another way 填 API Key；API Key 路径下部分依赖 ChatGPT 工作区／云服务的功能会受限或不可用。
---

# macOS 安装 Codex App：下载、安装、首次登录与进入 Codex 工作区

> 本文在线版：[codexguide.io/guides/macos-install-codex-app](https://codexguide.io/guides/macos-install-codex-app)

> 核对依据：OpenAI Help Center《[Downloading the ChatGPT macOS app](https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app)》《[Moving to the new ChatGPT desktop app](https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app)》；learn.chatgpt.com《[ChatGPT desktop app](https://learn.chatgpt.com/docs/app)》《[Authentication](https://learn.chatgpt.com/docs/auth)》《[Projects and chats](https://learn.chatgpt.com/docs/projects)》《[Commands](https://learn.chatgpt.com/docs/reference/commands)》；changelog 中 2026-07-09「Use Codex in the ChatGPT desktop app」说明。**本预览在 Linux 箱完成，没有真机 macOS 截图与安装包形态复验**。下文不编造未见于官方文档的菜单文案；安装包若为磁盘映像，按 macOS 常见「拖入应用程序」流程描述，以你本机下载结果为准。

你要在 Mac 上用 Codex 改本地代码，入口已经不是「再找一个叫 Codex 的独立安装包」，而是 **ChatGPT 桌面端里的 Codex 视图**。这篇只覆盖一条线：官方下载 → 装到「应用程序」→ 首次启动与系统提示 → ChatGPT 登录 → 切到 Codex → 打开本地文件夹并确认能开新对话。登录细节、排障清单与「第一次改文件」分别交给同目录的登录文与项目文。

## 完成后你可以

- 从官方域名拿到适合本机芯片的安装包，并装进「应用程序」；
- 用 ChatGPT 账号完成桌面端登录，并进入 Codex 视图；
- 打开（或创建）本地项目文件夹，确认可以开始新对话。

## 安装前检查

对照官方系统要求（Help Center 与系统要求页一致）：

| 项 | 要求 |
|---|---|
| 系统 | **macOS 14** 及以上；官方写明不会为更旧系统出兼容版 |
| 芯片 | **Apple Silicon（M1 或更新）** 或 **Intel** |
| 账号 | 可用的 ChatGPT 账号；公司／学校工作区以管理员开通的权限为准 |
| 网络 | 能访问 `chatgpt.com`（下载与浏览器登录都需要） |
| 磁盘 | 留出足够空间装应用与后续会话／工作区数据；磁盘异常暴涨见 Crashpad 排查文 |

在「关于本机」里确认版本与芯片。下载页会按芯片给出对应安装包，**不要**从网盘、论坛附件或「破解包」安装。

若你以前装过独立 **Codex App**：按应用内更新即可；更新后它会变成带 Chat、Work 与 Codex 的新 ChatGPT 桌面端，既有 Codex 对话与项目应保留，且会为既有 Codex 用户默认打开 Codex。可在设置里继续把 Codex 设为打开时的默认视图，并选用 Codex 应用图标（见《Moving to the new ChatGPT desktop app》）。

若本机已有旧版 **ChatGPT** 桌面端：应用内可能提示下载新版；新旧可能并存——新版叫 **ChatGPT**（含 Chat／Work／Codex），旧版改称 **ChatGPT Classic**，仍获支持，但新的 agent 能力通常只在新版。

## 第一步：只从官方入口下载

1. 用浏览器打开 [https://chatgpt.com/download/](https://chatgpt.com/download/)。
2. **先看地址栏域名**是 `chatgpt.com`（或其官方跳转），再点 macOS 下载。
3. 官方说明：下载页会检测本机是 Apple Silicon 还是 Intel，并提供对应安装包。

同页也会提到：已有 Codex App 的用户可更新到 ChatGPT 并打开 Codex。不要改用第三方「镜像站」或不明 `.dmg`／`.pkg`。

备用说明入口：[Downloading the ChatGPT macOS app](https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app)。桌面端总览与四步上手：[ChatGPT desktop app](https://learn.chatgpt.com/docs/app)。

## 第二步：安装到「应用程序」并首次启动

OpenAI 文档要求「Install the ChatGPT desktop app」，但**没有逐步截图式的 Finder 操作说明**。在 macOS 上，官方下载得到的常见形态是可打开的安装包／磁盘映像；按本机提示完成安装即可。若打开后看到应用图标和「应用程序」文件夹（或等价提示），按 macOS 常规做法：

1. 把 **ChatGPT** 应用拖入 **「应用程序」**（Applications）；
2. 弹出／卸载临时磁盘映像（若有）；
3. 从 **「应用程序」**（或 Launchpad）启动，**不要**长期从「下载」文件夹或未弹出的映像里直接开——否则更新与权限路径容易乱。

首次从「应用程序」打开时，macOS 可能弹出「是否打开从互联网下载的应用」一类确认。这是系统对已下载软件的常规检查，**不是** OpenAI 单独文档里的 Gatekeeper 排障手册。处理原则：

- 确认安装包来自上面的官方下载页，再选择打开；
- **不要**为了「装上」而去关系统完整性保护，或对不明来源执行去隔离属性一类命令；
- 若系统明确拦截且你无法确认来源，删掉文件，重新从 `chatgpt.com/download` 下载。

本预览**未**在真机复验当前安装包扩展名、窗口文案与是否仍为「拖入 Applications」；以你下载到的界面为准。验证通过后可把截图补进知识库图片目录（打码邮箱与本机用户名）。

## 第三步：用 ChatGPT 登录

官方 Authentication 对桌面端写得很短：

1. 打开应用后，在未登录页选择 **Continue to sign in**；
2. 系统浏览器打开 ChatGPT 登录流程；
3. 在浏览器完成登录／授权后，回到原来的桌面应用窗口；
4. 确认应用不再停在登录页。

也可以用 **Sign in another way** 输入 API Key（按 Platform 用量计费）。第一次完成本地练习，优先 ChatGPT 登录，不必为了「能打开」单独建 Key。API Key 可用于本地 Codex，但依赖 ChatGPT 工作区或云服务的能力可能受限；对照 [Authentication](https://learn.chatgpt.com/docs/auth) 与 Feature availability。

登录成功只说明凭据有效。工作区角色、席位、模型开关与额度仍可能挡住部分功能——那是权限／套餐问题，不是「没装上」。

浏览器已成功、应用仍像未登录时：切回原窗口，必要时完全退出再开；不要反复新开登录页，也不要复制地址栏里的回调参数到聊天里。更细的表见[登录 Codex](./07-登录Codex.md)与[安装登录常见问题](./13-安装登录常见问题.md)。

## 第四步：进入 Codex 工作区

桌面端左上角（或产品选择器）在 **ChatGPT** 与 **Codex** 之间切换。官方上手步骤：

1. 选择 **Codex**（软件开发、本地文件、仓库与开发者工具视图）；
2. 在 Codex 里从 **New chat** 开始；需要快捷提问时，指向 New chat 右侧的 **Quick chat**（若界面提供）；
3. 若要做文档／演示／表格等交付物，选 ChatGPT 再在顶部切换到 **Work**；普通问答用 Chat。Codex 历史与 ChatGPT 历史分开。

快捷键参考（以[Commands](https://learn.chatgpt.com/docs/reference/commands) 为准，版本可能调整）：在 Chat／Work／Codex 之间可用 `⌃ + 1`／`2`／`3` 切换；Codex 与 Work 下 **打开文件夹** 为 `⌘ + O`。

已有 Codex 用户更新后，应用可能默认停在 Codex；也可在设置里保持 Codex 为打开时的默认视图。

## 第五步：打开本地文件夹并做一次可用性检查

官方「Choose where to work」：开始对话、创建项目，或 **打开文件夹**。ChatGPT／Codex 会使用你选定位置中的文件与上下文。

在 Codex 侧建议按这个最小验证（只读意图即可，本课不要求真改仓库）：

1. 用 `⌘ + O`（或界面提供的打开文件夹／本地项目入口）选一个你有权访问的目录——练习目录或任意非敏感仓库；
2. 或先建／打开一个 **local project**，在项目菜单里 **Edit project** → **Add folder** 挂上文件夹；需要时把主工作目录设为 **Make primary**（新对话默认目录，也是 Git 与自动发现 `AGENTS.md`、skills、`config.toml` 的默认位置）；
3. 在 Codex 开 **New chat**，发一条不会改文件的确认，例如：「只列出当前工作区顶层目录名，不要修改任何文件」；
4. 能看到回复，且应用能引用该文件夹上下文，即安装＋登录＋工作区这条链路打通。

本地项目可以挂多个相关文件夹；无关仓库请分项目，避免一次授权过大范围。沙箱与审批决定命令实际能读／写／联网的范围——安装完成不等于已开「Full access」。需要改权限时再读权限／沙箱专题，不要在本课为了「验证成功」一把放开。

**Computer Use**（操纵其他 App 的图形界面）是另一步：官方要求在插件里启用，并在 macOS 上按提示授予 **屏幕录制** 与 **辅助功能**。普通「打开文件夹写代码」不依赖这两项；没有提示就不必预先打开系统隐私开关。

## 常见问题（安装阶段）

| 现象 | 先做什么 |
|---|---|
| 找不到「Codex」独立安装包 | 改下 ChatGPT 桌面端；登录后切到 Codex |
| 下载页芯片选错／打不开 | 回官方下载页让其自动检测；确认 macOS ≥ 14 |
| 应用在「下载」里能开、装完却怪 | 挪到「应用程序」再开；清掉旧快捷方式 |
| 浏览器登录成功，桌面仍未登录 | 切回原窗口；退出重开；仍失败见登录文 |
| 能聊天，不能读本地目录 | 是否已 open folder／挂上 local project；看审批与沙箱，不是重装 |
| 同时看到 ChatGPT 与 ChatGPT Classic | 预期行为；新 agent／Codex 整合能力用新版 ChatGPT |
| 磁盘被桌面端撑满 | 先查 Crashpad pending，见磁盘排查文，勿先整目录删除 |

## 和 CLI／IDE 怎么选（一句话）

桌面端适合并行项目、内置审阅与本机文件夹工作区；终端自动化用 CLI；已在编辑器里写代码可用 IDE 扩展。三者登录方式都支持 ChatGPT 与 API Key，但 **CLI 与 IDE 共用一套本地登录缓存**，与桌面端会话管理并不完全同一套 UI。入口对比见[App、CLI、IDE 和 Cloud 怎么选](../00-从这里开始/05-App-CLI-IDE和Cloud怎么选.md)。

## 完成检查

- [ ] 安装包来自 `chatgpt.com/download`，应用位于「应用程序」；
- [ ] 已用 ChatGPT（或你明确需要的 API Key）登录，桌面端离开登录页；
- [ ] 已切换到 **Codex**，并能 **New chat**；
- [ ] 已打开或挂载本地文件夹，只读确认任务有回复；
- [ ] 知道下一步是登录排障或「打开第一个本地项目」，而不是反复重装。

## 下一步

- [登录 Codex](./07-登录Codex.md)（`/guides/deng-lu-codex`）
- [打开第一个本地项目](./08-打开第一个本地项目.md)
- [安装登录常见问题](./13-安装登录常见问题.md)
- [Codex 桌面端占满磁盘（Crashpad）](../15-故障排查与常见问题/02-Codex桌面端占满磁盘-Crashpad崩溃转储排查与清理.md)（若存储异常）
- Windows 用户改看同目录《Windows 安装 Codex App》；只要终端可用时，可另装 CLI 作备选入口

## 参考资料

- [Downloading the ChatGPT macOS app](https://help.openai.com/en/articles/9275200-downloading-the-chatgpt-macos-app)
- [Moving to the new ChatGPT desktop app](https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app)
- [ChatGPT desktop app](https://learn.chatgpt.com/docs/app)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Projects and chats](https://learn.chatgpt.com/docs/projects)
- [Commands（含 Open folder ⌘O）](https://learn.chatgpt.com/docs/reference/commands)
- 下载页：[chatgpt.com/download](https://chatgpt.com/download/)

官方资料核对日期：2026-10-22（Asia/Shanghai）。本预览未在真机 macOS 完成下载、拖入「应用程序」、首次权限对话框与登录回调的逐步截图；上线前建议在 macOS 14+ 实机走通并补打码配图。
