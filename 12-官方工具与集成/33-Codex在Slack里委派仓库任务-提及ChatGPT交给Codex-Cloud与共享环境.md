---
id: codex-slack-cloud-delegation
title: "Codex 在 Slack 里怎么用：@Codex 换成 @ChatGPT，仓库任务交给 Codex Cloud，共享环境、审批卡片和跟进怎么处理"
seo_title: "Codex 在 Slack：@ChatGPT 把仓库任务交给 Cloud"
description: "以前在 Slack 里 @Codex，现在要改成 @ChatGPT。本文按官方文档说明管理员要开什么、为什么只认共享并已发布的 Cloud 环境、私密审批卡片和 Follow along 怎么用、同一帖里怎么继续，以及没回复、找不到环境、任务不启动时怎么排查。"
lede: "频道里提的是 @ChatGPT。仓库任务另开一条 Codex Cloud 任务，结果回到原帖。个人 Cloud 环境不会出现在这份名单里。"
url: /guides/codex-slack-cloud-delegation
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [Cloud]
difficulty: 进阶
order: 33
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-22
date_modified: 2026-11-22
verified_on: 2026-11-22
official_ref: "https://learn.chatgpt.com/docs/third-party/slack"
keywords: [Codex Slack, "@ChatGPT Slack", Slack 委派 Codex Cloud, Codex Cloud 共享环境, Slack Codex 不回复]
related: [cloud-environments, codex-automations-scheduled-tasks, codex-linear-integration]
howto: true
faq:
  - q: "Slack 里还要 @Codex 吗？"
    a: "官方 Move to the ChatGPT app 写：以前用 @Codex 的，管理员启用 ChatGPT 应用之后，新请求改用 @ChatGPT，并按提示完成连接和审批。"
  - q: "为什么我自己的 Cloud 环境在 Slack 里选不到？"
    a: "文档写 ChatGPT 只从你能访问的、已共享给工作区的 Cloud 环境里选，而且要有已发布版本。个人 Cloud 环境不在这个流程里。"
  - q: "审批卡片是私密的，频道里的回复也是私密的吗？"
    a: "不是。Allow / Deny 卡片是私密的。发到频道里的回复，能进这个频道的人都能看。私密卡片不会把回复变成私密。"
---

# Codex 在 Slack 里怎么用：@Codex 换成 @ChatGPT，仓库任务交给 Codex Cloud，共享环境、审批卡片和跟进怎么处理

> 核对依据：2026-11-22 打开的 [Use ChatGPT in Slack](https://learn.chatgpt.com/docs/third-party/slack)、[Set up and manage @ChatGPT in Slack and Microsoft Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams)、[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) 和 [Codex Cloud 概述](https://learn.chatgpt.com/docs/cloud)。写作环境没有 Slack 工作区，没有管理员权限，没有已发布的共享环境，没有配图。后台步骤只写这些页面里有的句子。

适合要在 Slack 频道里让人查仓库、改代码，并把结果留在原帖的人。Linear issue 上的指派是另一条集成，见 [Codex 接入 Linear](./32-Codex接入Linear-指派issue-评论提及Codex与Triage规则自动分配.md)。定时任务里的 Slack 事件触发，见 [Codex 定时任务](./06-Codex-Automations定时任务.md)，不要和下面的 Cloud delegation 混成同一条设置。

## 先说结论：Slack 里谁来接活，代码任务实际跑在哪

在已启用应用的频道里提到 `@ChatGPT`，开始一次请求。工作区开了 **Cloud delegation** 时，ChatGPT 可以把仓库工作交给单独的一条 [Codex Cloud](https://learn.chatgpt.com/docs/cloud) 任务，再把结果回到原来的帖子。

接话的是 `@ChatGPT`。跑代码的是 Codex Cloud，用的是你的账号，而且必须有一份已经发布、并共享给工作区的环境。个人 Cloud 环境不会出现。

频道回复本身不私密。需要授权时，ChatGPT 可以给你一张只有你看的审批卡片，按钮是 **Allow** 和 **Deny**。

什么时候该用 Chat、ChatGPT Work 或 Codex，见 [Chat、ChatGPT Work 和 Codex 怎么选](../00-从这里开始/04-Chat-Work和Codex怎么选.md)。Slack 这条路径解决的是「人在频道里，代码在 Cloud 上」。

## 从 @Codex 换到 @ChatGPT：管理员和个人各要做什么

官方 “Move to the ChatGPT app” 只有两句：以前用 `@Codex` 的，在管理员启用 ChatGPT 应用之后，新请求改用 `@ChatGPT`，并按出现的连接和审批提示做完。

管理员和个人不是同一步。文档把工作区部署和个人账号连接分开写。

**工作区。** ChatGPT 工作区的 owner 或 admin 配置 Slack 部署。能看到哪些开关，取决于工作区已经打开的功能。看不到时，问管理员 Slack 部署是否可用；Slack 自己的应用策略仍然生效。

管理页 [Set up and manage @ChatGPT in Slack and Microsoft Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams) 里，和 Codex 直接相关的是 “Enable Codex Cloud for Slack”。原文五步：

1. 为工作区启用 Codex Cloud。
2. 如果 Codex Cloud 的角色访问控制适用，把权限授给 Slack surface 的服务账号，以及发起请求的用户。
3. 发布一份 cloud environment，并共享给工作区。
4. 核对每个发起请求的用户能否访问这份环境，以及需要认证的仓库。
5. 让一位试点用户在 Slack 里请求做仓库调查，确认编码任务能启动。

同一节还写：服务账号负责找到环境；编码任务以发起请求的用户身份运行。服务账号不需要 GitHub 访问权限。

管理页另外写了连接 Slack、创建 surface、选频道范围。那些是 `@ChatGPT` 这个应用本身的安装，不是 Codex 环境的配置。本文不把帮助中心链接后面的按钮名抄进来，因为 2026-11-22 没有打开那份帮助中心的逐步截图。细节以管理页和它指向的 Help Center 为准。

**个人。** 工作区配好之后，ChatGPT 仍可能要求你连接自己的账号：

1. 点 Slack 消息里的连接链接，需要的话先登录。
2. 把 Slack 连到你发起请求的同一个工作区。
3. 回到原来的帖子，再提一次 `@ChatGPT`。

## 前提：Cloud delegation、已发布并共享的环境、RBAC

Cloud delegation 要在工作区里可用，并且要有一份已经发布、共享给工作区的环境。文档让管理员按上面的锚点启用 Codex Cloud for Slack。

开了 Codex Cloud 的 role-based access control 时，部署用的服务账号和你本人都要有 Codex Cloud 权限。缺一边，任务可以不启动。排查看下一节。

Enterprise 要准备并发布一份测试过的环境，按 [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) 做，再按其中的 [Share within an Enterprise workspace](https://learn.chatgpt.com/docs/environments/cloud-environments#share-within-an-enterprise-workspace) 共享。2026-11-22 该节的步骤是：

1. 打开环境配置。
2. 在 **Privacy > Who can use** 里选择你的工作区。
3. 保存。还没发布的话，发布这份环境。

**Who can use** 选 **Only me** 就是保持私有。Slack 这条流程不使用个人环境，所以只给自己用的环境不会出现在委派名单里。

共享环境不等于共享别人的仓库权限，也不等于共享你的个人凭据值。Cloud environments 写明：每条任务的工作文件是分开的；能用这份环境，不等于能看别人的任务，也不等于能改环境本身。共享前要检查环境自有的凭据和已经准备好的文件，因为用这份环境的人可以碰到这些。仓库访问和个人连接取决于真正跑任务的那个账号。

环境怎么发布、变量和网络密钥怎么分，仍看 [Codex Cloud 云端环境配置](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。

## 发起请求：怎么写才能选对仓库和环境

在应用已启用的频道里：

1. 提到 `@ChatGPT`，写清要的结果。编码工作要带上仓库，以及帖子里相关的上下文。
2. 做完账号连接或审批提示。批准前看请求的工作和访问范围。
3. 相关的后续请求留在同一条帖子里，并再次提到 `@ChatGPT`。

官方例子：

```text
@ChatGPT investigate the failing checkout tests in acme/storefront and propose a fix.
```

同一条帖子里接着写：

```text
@ChatGPT add a regression test for the fix and summarize the checks you ran.
```

环境怎么选，文档是三条：

- ChatGPT 从你能访问的、已共享给工作区的 Cloud 环境里选。用你的账号时，它会先确认你能访问这份环境。个人 Cloud 环境不包括在内。在请求里写出仓库名或共享环境名，帮助它选择。
- 仓库工作跑在单独的任务里，用的是你的账号。你需要能访问选中的环境，以及任何要认证的仓库。
- 同一条 Slack 帖子里的相关请求，如果仍用同一个账号跑，可以继续原来的编码任务和环境。换一个账号的请求可能另开一条编码任务。要换环境，就新开一条对话。

只用本工作区里已启用的公开或私有频道。和其他组织共享的 Slack Connect 频道不支持这个流程。

## 审批卡片、Follow along／Cancel 与同帖跟进

请求需要你授权时，ChatGPT 可以显示一张私密审批卡片，控件是 **Allow** 和 **Deny**。决定前看指派内容，以及卡片上如果有的环境选择。

任务开始时，ChatGPT 可以在原帖发一条消息。**Follow along** 和 **Cancel** 可用时，是给发起请求的人的。**Follow along** 用来打开任务、查看它在做什么。频道里的回复不会让每个频道成员都获得底层任务的访问权。

结果回到帖子之后，先看答案、改动和它报告的检查，再决定用不用、合不合并。要改正或继续，在帖子里再提 `@ChatGPT`。

文档把 **Task controls unavailable** 单独列为一种情况：Follow along 和 Cancel 取决于部署配置，并且是给发起人的。看不到这两个控件，不等于任务没开始。

帖子很长时，官方建议在最新一条请求里自己概括问题、期望结果和仓库，让任务有足够上下文。

## 频道可见性与密钥：哪些内容不要贴进 Slack

发到频道里的回复，能访问这个频道的人都能读。让 ChatGPT 只分享适合这批读者的信息。私密的审批卡片不会把随后的频道回复变成私密。

密钥不要写进 Slack 提示。仓库工作要用环境自己的凭据控制。文档指向 [Agent Security](https://learn.chatgpt.com/docs/environments/cloud-environments#agent-security) 和管理页的 [deployment access boundaries](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams#security-faq)，并要求遵守工作区的数据和应用策略。

管理页对访问的另一句也适用：`@ChatGPT` 使用已配置的连接和对话上下文，不会继承某个人的文件、应用或私有频道权限。个人插件要另外授权。共享回复对会话参与者可见。

## 常见问题

官方排障是这几条，按现象对：

- **没回复。** 确认这个频道启用了 ChatGPT，并且明确提到 `@ChatGPT`。用组织内的频道，不要用 Slack Connect。
- **反复要求连接账号。** 确认 ChatGPT 连的是你正在发言的那个 Slack 工作区，然后在同一条帖子里重试。
- **没有可用环境。** 环境要已发布，并且共享给工作区；跑任务的账号要有相应访问权。个人 Cloud 环境不会出现。
- **编码任务不启动。** 请管理员确认 Cloud delegation 可用，并且工作区启用了 Codex Cloud。开了 RBAC 时，部署的服务账号和你的账号都要有 Codex Cloud 权限。再查你对选中环境和仓库的访问。
- **要换环境。** 新开一条对话，并写上要使用的仓库或共享环境。同一条帖子里的后续请求会尽量沿用同一账号下的原任务和环境。
- **控件不可用。** Follow along 和 Cancel 看部署配置，并且是给发起人的。
- **帖子太长。** 在最新请求里写上问题、期望结果和仓库。

本文没有在真实频道里触发过这些回复，所以没有失败截图。现象对不上时，以你工作区管理员在管理页里看到的开关为准，不要按旧的 `@Codex` 机器人名称继续试。

## 参考资料

- [Use ChatGPT in Slack](https://learn.chatgpt.com/docs/third-party/slack)
- [Set up and manage @ChatGPT in Slack and Microsoft Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams)
- [Codex Cloud 概述](https://learn.chatgpt.com/docs/cloud)
- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)
- [Use Codex in Linear](https://learn.chatgpt.com/docs/third-party/linear)
