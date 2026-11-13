---
id: codex-developers-plugin-showcase-api-credits
title: Codex 用 OpenAI Developers 插件 Showcase：周末 starter 项目，以及 Pro／Business 怎么领取 API 额度
seo_title: Codex Developers 插件 Showcase：remix starter 与领取 API 额度
description: OpenAI Developers 在 2026-11-07 宣布插件里的 Showcase 标签，用来打开 API starter 并在 Codex 里接着做。本文写这个标签和公开 Showcase 站的关系，以及 Pro、Business 在 billing 里领取 API 额度时官方怎么说。金额以 billing 界面和官方文档为准。
lede: Showcase 用来选一个 starter，在 Codex 里接着改。Pro 和 Business 的 API 额度在账单里领，用来支付你的应用调用 API，不增加 Codex 订阅用量。
url: /guides/codex-developers-plugin-showcase-api-credits
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 14
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-07
date_modified: 2026-11-07
verified_on: 2026-11-07
official_ref: https://developers.openai.com/learn/developers-codex-plugin
keywords: [Codex Showcase, OpenAI Developers 插件, API credits, ChatGPT Pro API 额度, Codex remix starter]
related: [codex-openai-developers-plugin, codex-chatgpt-subscription-api-credits, codex-chatgpt-shared-usage-limits]
howto: false
faq:
  - q: Showcase 会自己把 API Key 写进项目吗？
    a: 官方帖子没有这么说。建 Key、写入 .env.local 和 API 报错分类在《Codex 安装 OpenAI Developers 插件》里。本文没有打开 Showcase 标签，也没有创建 Key。
  - q: 领了 API 额度，Codex 的 5 小时或每周用量会变多吗？
    a: 不会。2026-11-07 的官方额度文档写明，这笔权益不支持用 API Key 使用 Codex，也不提高 ChatGPT 或已登录 Codex 的用量上限。它支付的是关联 API 组织上的 API Platform 用量。
  - q: 本文为什么不写每月多少美元？
    a: 官方额度文档有按套餐列出的表格。表格和账号 billing 界面都会变。本文不抄这张表，打开文档和账单时以当时显示的数字为准。
  - q: Plus 能领吗？
    a: 2026-11-07 打开的额度文档把领取资格写成付费至少 7 天的 Pro 或 Business。同一页写明，降到 Plus、Go 或 Free 之后，关联会在计费周期结束时解除。
---

# Codex 用 OpenAI Developers 插件 Showcase：周末 starter 项目，以及 Pro／Business 怎么领取 API 额度

> 本文在线版：[codexguide.io/guides/codex-developers-plugin-showcase-api-credits](https://codexguide.io/guides/codex-developers-plugin-showcase-api-credits)

> 核对依据：[@OpenAIDevs 2026-11-07 00:02 UTC 的帖子](https://x.com/OpenAIDevs/status/2118856544733532452)、插件文档 [OpenAI Developers plugin](https://developers.openai.com/learn/developers-codex-plugin)（同一天的 Markdown 版本）、公开目录 [Showcase](https://developers.openai.com/showcase) 与 [API demos](https://developers.openai.com/showcase/api)，以及 [API credits for ChatGPT subscribers](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)。没有登录 ChatGPT，没有在 Codex 里打开 Showcase 标签，没有点 Open in Codex，没有领取额度，没有截图。金额不在本文抄录。

插件怎么装、怎么建 API Key、API 报错怎么分，已经写在 [Codex 安装 OpenAI Developers 插件](./08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md)。这篇只补两件事：Showcase 用来做什么，以及 Pro／Business 领取 API 额度时官方现在怎么说。

## 先看结论

- 2026-11-07，OpenAI Developers 宣布插件里有新的 **Showcase** 标签，用来开始周末项目。帖子写的范围是 OpenAI API 的 starter，类别为 agents、creative tools、data visualization 和 voice。做法是在 Codex 里打开一个项目，在它上面继续做（open one in Codex and build on it）。
- 同一条帖子写：符合条件的 ChatGPT Pro 和 Business 订阅者可以在 billing settings 里领取 API credits，用来支付应用自己的 API 用量。
- 插件文档页在同一天仍然写的是安装、OpenAI Platform 连接、API Key、Agents SDK 和报错排查。页面正文里没有 Showcase 标签的点击步骤。
- 公开网站 [developers.openai.com/showcase](https://developers.openai.com/showcase) 是另一份目录。API demos 页上能看到 Try demo、Open in Codex 和 Download source。这和插件里的标签是不是逐项相同，本文没有并排打开，不能当成已经核对过的同一份清单。
- 额度数字以你账号的 billing 界面和官方文档当时的表格为准。本文不写死美元金额。

## 这篇和另外两篇怎么分工

| 你要做的事 | 读哪篇 |
|---|---|
| 安装 OpenAI Developers，创建项目 API Key，把 Key 写入 `.env.local`，给 API 报错分类 | [插件安装与排错](./08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md) |
| 知道 Showcase 标签宣布了什么，以及去哪里领 API 额度 | 本文 |
| 看资格、领取后的扣费顺序、额度用完会怎样，以及这笔钱能不能支付「用 API Key 登录 Codex」 | [订阅 API 额度](../10-配置模型与权限安全/16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md) |
| 看 12 月起 ChatGPT 和 Codex 共用的那份订阅用量 | [用量合并](../10-配置模型与权限安全/20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md) |

三份额度不要叠在一起。Showcase 帖子说的 API credits，官方额度文档定义为关联到你拥有的 API 组织、用来调用 API 做应用和 Agent。用量合并文写的是 ChatGPT 与 Codex 的订阅用量。插件排错文解决的是 Key 怎么进项目、请求为什么失败。

## 安装或打开 Developers 插件

官方插件页对 Codex 的安装步骤仍然是：

1. 在项目目录运行 `codex`。
2. 输入 `/plugins`。
3. 搜索 **OpenAI Developers**，打开后选择 `Install plugin`。
4. 如果提示连接自带的 **OpenAI Platform** 应用，按提示完成。插件要靠它创建项目 API Key。
5. 新开一个对话再使用。

桌面端从插件目录搜索同名条目。入口和权限的通用说明见 [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)。

插件文档写明，装好之后，任务涉及 OpenAI Platform 时，ChatGPT 或 Codex 可以自动用这个插件，例如创建 API Key 或排查 API 问题。那部分的逐步规则以插件专文为准，这里不重复。

本文没有在 `/plugins` 里重新安装。插件专文核对的是 1.2.3 的源码和假 Key 脚本，也没有在已登录的 `/plugins` 里点过安装。

## 进入 Showcase，并 remix 一个 starter

帖子原文是两层意思：

1. 用 OpenAI Developers 插件里新的 Showcase 标签，开始周末要做的东西。
2. starter 覆盖 agents、creative tools、data visualization、voice。选一个，在 Codex 里打开，在它上面继续做。帖子把这一步叫 remix，并另有一句 “Find a project to remix”。

帖子没有写标签在插件里的第几屏，也没有写 remix 之后仓库落在本机还是云端。本文没有这个标签的截图，下面不补一套点击顺序。

你可以先做这三件能核对的事：

1. 确认插件已经安装，并且当前对话是安装之后新开的。插件文档把 “Start a new chat” 写成安装后的一步。
2. 在插件界面里找 **Showcase**。找不到时，先把 Codex 或 ChatGPT 桌面端更新到你账号上的当前版本，再新开对话。本文没有验证 “更新之后标签一定出现”。
3. 想先看公开目录，打开 [Showcase](https://developers.openai.com/showcase)。要看带 Open in Codex 的 API 示例，打开 [API demos](https://developers.openai.com/showcase/api)。2026-11-07 这页的项目卡片上有 Try demo、Open in Codex、Download source。项目会增减，以你打开时的页面为准。

Open in Codex 点下去之后 Codex 收到什么提示、会不会新建目录，本文没有点，所以不描述结果。Download source 是网页上的另一条入口，和插件标签里的 remix 是否同一条链路，官方帖子没有写。

帖子列出的四类只说明 starter 的方向。它没有承诺每一类在你的账号里都有项目，也没有写这些项目的模型名或价格。

## Pro／Business 领取 API credits：官方怎么说

2026-11-07 打开的 [API credits for ChatGPT subscribers](https://developers.openai.com/api/docs/guides/chatgpt-api-credits) 写明：符合条件的 ChatGPT Pro 和 Business 订阅可以领取 API credits，作为订阅权益。做法是把订阅关联到一个你拥有的 API 组织，再用这些额度做调用 OpenAI API 的应用和 Agent。

同一页写了这些规则，这里不抄金额表：

- 额度多少取决于 Pro 方案，或 Business 工作区的付费席位。页面上有一张按订阅列出的表，并写了每月上限的说法。数字以这张表和你的 billing 界面为准。
- 激活一次之后，在权益仍然可用、订阅仍然符合条件时，续费会自动发放。
- 没用完的额度在计费周期结束时过期，不结转。
- 有可用的免费额度时，不要求另外绑定 API 付款方式。
- 仍受 API 条款和速率限制约束。

资格，按同一页：

- 有一份已经付费至少 7 天的 ChatGPT Pro 或 Business。免费试用和赠送的订阅不符合。
- 你是这份 ChatGPT 订阅或 Business 工作区的所有者，并且是接收额度的 API 组织的所有者。
- ChatGPT 账号和用来关联的 API 账号使用同一个邮箱。

同一页把降级到 Plus、Go 或 Free 写成不再符合条件的例子：计费周期结束时，API 组织的关联会解除。

领取有两条路，关联的是同一份权益。官方文档的步骤是：

**从 ChatGPT 开始**

1. 用拥有这份订阅的账号登录 [ChatGPT](https://chatgpt.com/)。
2. Pro 打开 [Settings → Billing](https://chatgpt.com/settings/billing)。Business 打开工作区的账单设置，或 [Admin Console](https://admin.openai.com/)。
3. 找到 API credits 权益，开始领取。
4. 核对将要接收额度的 API 组织。名下有多个符合条件的组织时，选要关联的那一个。
5. 确认并激活。

**从 API Platform 开始**

1. 用和符合条件的 ChatGPT 订阅相同的邮箱登录 [API Platform](https://platform.openai.com/)。
2. 选中你拥有的、应该接收额度的 API 组织。
3. 打开 [Billing](https://platform.openai.com/settings/organization/billing/)，找到 API credit 权益。
4. 选中你拥有的那份 ChatGPT 订阅或 Business 工作区。
5. 确认并激活。

激活之后，到 [API Platform 的 billing 概览](https://platform.openai.com/settings/organization/billing/overview) 看额度。本文没有登录，没有看到这笔余额。

官方文档接着写了一句，和 Codex 直接有关：用 API Key 使用 Codex，不在这项权益里。这些 API credits 也不提高 ChatGPT 或已登录 Codex 的用量上限。帖子说的 “cover their app’s API usage”，指的是你的应用调用 API。更细的覆盖范围、用完之后是继续花已购买的额度还是返回 `credit_balance_exhausted`，见 [订阅 API 额度](../10-配置模型与权限安全/16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)。那篇按 2026-10-29 的 Help Center 和开发者文档整理了表格。若它和你今天打开的官方页不一致，以官方页和 billing 界面为准。

## 常见误解

**Showcase 里的项目会用我的 Codex 订阅额度跑完。**

帖子把领取额度的位置放在 billing settings，用途是应用的 API 用量。官方额度文档把 Codex 的 API Key 用量排除在外，也不提高已登录 Codex 的用量上限。在 Codex 里打开 starter 之后，Codex 这一侧的用量仍按你的登录方式计算。应用跑起来之后的 API 调用，才走关联的 API 组织。

**领了额度就不用再读 Key 那篇。**

额度进的是 API 组织。项目里的请求要用这个组织下的项目 Key。Key 怎么创建、怎么避免贴进对话，仍是 [插件专文](./08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md) 的范围。

**这和 12 月的用量合并是同一次改动。**

用量合并写的是 Plus、Pro、Business 的 ChatGPT 和 Codex 从 12 月起共用一份按 token 计算的用量，见 [用量合并](../10-配置模型与权限安全/20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md)。API credits 在 API 组织的账单里。两篇的官方链接不同。

**网页 Showcase 上的每一个演示都能在插件标签里 remix。**

2026-11-07 的公开目录里有很多演示，包括游戏、落地页和 API demos。帖子点名的是插件标签里的 API starter，并给出四类。本文没有打开标签，不能把网站上的每一条都写成插件里已经有的 remix 按钮。

## 怎么判断做到了

- 插件已安装，新对话里能提到 OpenAI Developers。装不上时回到插件专文，而不是在 Showcase 里重试 Key。
- 你能在插件里看到 Showcase，或先在 [API demos](https://developers.openai.com/showcase/api) 上找到准备打开的项目。打开之后的仓库和 diff，以你本机为准。本文没有这一步的结果。
- Pro 或 Business 领取之后，API Platform 的 billing 概览里能看到这笔 credits。看不到入口时，按额度专文核对所有者、满 7 天和邮箱是否一致。不要把密码或 API Key 发给支持人员。

## 参考资料

- [@OpenAIDevs，2026-11-07](https://x.com/OpenAIDevs/status/2118856544733532452)
- [OpenAI Developers plugin](https://developers.openai.com/learn/developers-codex-plugin)
- [Showcase](https://developers.openai.com/showcase)
- [API demos](https://developers.openai.com/showcase/api)
- [API credits for ChatGPT subscribers](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)
