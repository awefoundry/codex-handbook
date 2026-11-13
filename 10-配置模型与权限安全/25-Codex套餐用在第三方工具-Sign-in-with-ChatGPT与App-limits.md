---
id: codex-chatgpt-plan-in-other-apps
title: Codex 套餐用在第三方工具：Sign in with ChatGPT 连接 OpenCode、Kilo Code、Warp 等，额度怎么算、怎么限额
seo_title: Sign in with ChatGPT：把 Codex 套餐用在 OpenCode、Kilo Code、Warp
description: ChatGPT 现在允许在 OpenCode、Kilo Code、Warp、Amp、Notion 等第三方工具里用你的 ChatGPT 套餐发 AI 请求，消耗的是套餐里的 Codex 和 ChatGPT work 用量。本文按官方文档说明哪些工具支持、怎么连接、额度怎么算、怎么用 App limits 限额和断开，以及 Business 管理员要开的两个开关。
lede: 登录和用套餐是两项授权；用套餐不会多给额度，第三方工具花的就是你 Codex 的那一份，所以先设 App limits。
url: /guides/codex-chatgpt-plan-in-other-apps
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 25
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-11
date_modified: 2026-11-11
verified_on: 2026-11-11
official_ref: https://learn.chatgpt.com/docs/sign-in-with-chatgpt
keywords: [Sign in with ChatGPT, ChatGPT 套餐用在第三方工具, Use your ChatGPT plan, App limits, OpenCode, Kilo Code, Business 管理员]
related: [usage-limits-credits, codex-chatgpt-shared-usage-limits, codex-chatgpt-subscription-api-credits]
faq:
  - q: 在第三方工具里用 ChatGPT 套餐，会额外多一份额度吗？
    a: 不会。官方文档写明，应用的用量计入你现有的套餐限制，连接应用不会增加新的额度；它用的是套餐里包含的 Codex / ChatGPT work 用量。第三方工具花得多，你在 Codex 里能用的就少。
  - q: 连接后，第三方工具能看到我的 ChatGPT 对话和记忆吗？
    a: 官方写明「用你的套餐」这项授权不会让应用访问你的 ChatGPT 对话或记忆。应用另外申请的权限（比如姓名、邮箱、头像）要在授权页单独看。
  - q: App limits 设成 30%，是不是给这个工具预留了 30%？
    a: 不是。官方说明应用的限额是上限，不是单独的额度，也不是从套餐里预留出来的部分。它只保证这个工具最多用到你每周总用量的 30%。
  - q: 我是 Business 成员，为什么工具里看不到用套餐的选项？
    a: Business 工作区要先由管理员在 admin.openai.com 的 Tenant settings > External access 里把这个应用的 Use ChatGPT plan 设为 Allowed。另外，官方注明 Devin 不支持 Business 套餐的用量。
---

# Codex 套餐用在第三方工具：Sign in with ChatGPT 连接 OpenCode、Kilo Code、Warp 等，额度怎么算、怎么限额

> 本文在线版：[codexguide.io/guides/codex-chatgpt-plan-in-other-apps](https://codexguide.io/guides/codex-chatgpt-plan-in-other-apps)

> 核对依据：官方文档 [Sign in with ChatGPT](https://learn.chatgpt.com/docs/sign-in-with-chatgpt)（2026-11-11 核对）、开发者文档 [Sign in with ChatGPT](https://developers.openai.com/siwc)，以及 OpenAI Developers 在 X 上的公告（[2026-11-10T17:50Z，北京时间 11-11 01:50](https://x.com/OpenAIDevs/status/2120212596850663712)）。写作环境没有可用的付费 ChatGPT 账号会话，**本文没有截图**；界面名称按官方英文文档写，中文界面的叫法可能不同。合作应用名单会变，以官方页面为准。

2026-11-10，OpenAI 宣布 ChatGPT Business 套餐也可以用在 Notion、v0、Amp、Kilo Code、Warp、Nous Research 的 Hermes、OpenClaw、OpenCode 等工具里，入口叫 **Sign in with ChatGPT**。对 Codex 用户来说，关键一点是：这些工具用的是**你套餐里同一份 Codex / ChatGPT work 用量**。

## 先看结论

- **两项授权分开**：「用 ChatGPT 登录」只是登录；「Use your ChatGPT plan」才是让应用用你的套餐发 AI 请求。授权页会分别列出来。
- **不加额度**：应用的用量计入现有套餐限制，连接应用不会多一份额度；应用自己可能另外收费。
- **不读对话**：用套餐这项授权不会让应用访问你的 ChatGPT 对话和记忆。
- **先设上限**：在 ChatGPT 的 **Settings > Usage > App limits** 给每个应用设「每周用量的百分比上限」，避免某个工具把一周的 Codex 额度花光。
- **随时断开**：**Settings > Security and login > Sign in with ChatGPT** 里选应用 → **Disconnect**。
- **Business 要管理员先开**：Tenant settings > External access 里逐个应用允许，再到 Usage limits 设整体上限。

## 哪些工具支持

官方页面把合作方分成三类（2026-11-11 核对）：

| 类别 | 应用 |
|---|---|
| 可以用 ChatGPT 套餐 | Amp Code、Conductor、Dactyl、Devin（不支持 Business 套餐）、Hermes Agent、Hyperagent、Kilo Code、Lovable（即将支持）、Notion、Vercel、Vorflux、Warp |
| 只能登录，不用套餐 | Airtable、Canva、GitLab、HubSpot、Supabase |
| 开源集成 | OpenClaw、OpenCode、Pi、T3 |

套餐方面，官方写的是 Go、Plus、Pro、Business 中**符合条件**的订阅者可以选择用套餐。官方公告里点名 v0，但 2026-11-11 的官方名单里写的是 Vercel；以你在工具里看到的入口为准。

## 连接步骤

官方给出的登录流程：

1. 在支持的应用或网站里选择 **Continue with ChatGPT**。
2. 登录你要用的 ChatGPT 账号。
3. 看清应用申请的账号信息，比如姓名、邮箱和头像。
4. 继续完成登录。如果你在这个应用里已经有同邮箱的账号，按应用的提示确认并关联。

也可以反过来，先登录应用，再到它的账号或账单设置里找 ChatGPT 选项，把已有账号关联上。

要让应用用你的套餐，应用会额外弹出 **Use your ChatGPT plan** 授权。确认这一项开着，再选 **Continue**。之后，应用的模型菜单里通常会显示正在使用 ChatGPT 套餐，并带有管理用量的入口（官方示意图里叫 **Manage usage**）。

每个工具在哪里放这个入口不一样。OpenCode、OpenClaw 这类开源工具，请看各自仓库的说明；官方页面只给了仓库链接，没有写具体命令，本文也不替它们编命令。

## 额度怎么算：和 Codex 共用一份

官方原话的意思是：一些应用可以用你的 ChatGPT 套餐发符合条件的 AI 请求，**用的是套餐里包含的 Codex / ChatGPT work 用量**。

落到日常使用上：

- 你在 Warp 或 Kilo Code 里跑掉的用量，和你在 Codex App、CLI、IDE 里用的是**同一个池子**，5 小时和每周两档限制照样生效。怎么看这两档，见《[Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)》。
- 12 月起 Codex 和 ChatGPT 共用额度、按 token 计算的变化，见《[Codex 和 ChatGPT 用量合并](./20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md)》。
- 这和 Pro / Business 每月可领的 **API 额度**是两回事。API 额度走 API Key，用套餐走 Sign in with ChatGPT。区别见《[Codex 与 ChatGPT 订阅 API 额度](./16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)》。
- 第三方应用可能有自己的收费，官方页面专门提醒了这一点。

## 用 App limits 给每个工具限额

官方步骤：

1. 在 ChatGPT 打开 **Settings > Usage**，这里能看到已连接应用用了多少。
2. 在 **App limits** 下，打开应用旁边的百分比菜单。
3. 把它的每周上限设成你每周总用量的某个百分比。
4. 选择 **Save**。

两点容易误会：

- **它是上限，不是预留**。设 30% 不代表这 30% 只给这个应用用，你在 Codex 里照样可以先把它用掉。
- **它按周计算**，单位是「每周总用量的百分比」。

我的用法：日常主力在 Codex 里的人，第三方工具先设 10%～20%，跑一周看 Usage 页的实际消耗再调。

## 断开连接

要彻底收回某个工具的访问：**ChatGPT Settings > Security and login > Sign in with ChatGPT** → 选这个应用 → **Disconnect**。

只想暂时不让它花额度，也可以在 Business 账号下到 **Settings > Usage** 关掉这个应用的套餐用量（官方写明 Business 用户可以这样做），或者把 App limits 调低。

## Business 管理员：两个开关

官方文档把管理员设置分成两步。

**第一步：允许用套餐。** 打开 [admin.openai.com](https://admin.openai.com)，进入 **Tenant settings > External access**，选中应用，把 **Use ChatGPT plan** 设为 **Allowed**。每个要放行的应用都要做一次。官方示意图里，Identity（登录）默认是允许的，用套餐要单独打开。

**第二步：设工作区上限（可选）。** 在 admin.openai.com 选中工作区，打开 **Usage limits**，在 **ChatGPT plan** 下找到 **Usage in other services**，选 **Edit**，设置成员套餐额度里最多可以被这些外部服务用掉的百分比，选 **Apply**，再 **Save changes**。

成员自己还能在 **Settings > Usage** 里给单个应用设更低的上限，或者关掉某个已连接应用的套餐用量。OpenAIDevs 的公告也提到，管理员可以给开源工具设用量上限。

## 给开发者

想在自己的应用里加 Sign in with ChatGPT，官方入口是开发者文档 [Sign in with ChatGPT](https://developers.openai.com/siwc)。这部分接入细节不在本文展开。

## 常见问题

**和 Codex CLI 里的「Sign in with ChatGPT」是一回事吗？**
名字一样，场景不同。Codex CLI 首次运行时选 Sign in with ChatGPT，是登录 Codex 本身（见《[登录 Codex](../01-安装与首次使用/07-登录Codex.md)》）；本文讲的是第三方应用借你的 ChatGPT 账号登录，并可选用你的套餐。

**我在多个工具里都连了，用量怎么查？**
都在 ChatGPT 的 **Settings > Usage** 里看已连接应用的用量。

**为什么我在官方名单里找不到某个工具？**
名单会更新。官方公告里点了 v0，名单里写的是 Vercel；Lovable 标着即将支持。以官方页面和工具里实际出现的入口为准。

## 参考资料

- [Sign in with ChatGPT（ChatGPT 文档）](https://learn.chatgpt.com/docs/sign-in-with-chatgpt)
- [Sign in with ChatGPT（开发者文档）](https://developers.openai.com/siwc)
- [OpenAI Developers 公告](https://x.com/OpenAIDevs/status/2120212596850663712) 与[管理员说明](https://x.com/OpenAIDevs/status/2120212598385733732)

本文按 2026-11-11 可访问的官方文档核对。界面截图待补，届时会打码账号、邮箱和工作区名。
