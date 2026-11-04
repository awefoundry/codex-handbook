---
id: codex-data-controls-training
title: Codex 对话会被用来训练吗：Improve the model、Include environments 和例外情况
seo_title: Codex 对话会被用来训练吗：数据控制与 Include environments
description: Codex 任务会不会被拿去训练模型，取决于账号类型和几个开关。本文按 OpenAI 帮助中心整理：个人账号在哪里关、Include environments 为什么要单独关、点赞点踩和 Daybreak 会话的例外，以及怎么确认设置没被改回去。
lede: 个人账号默认开着。关掉 Improve the model 还不够，Codex 设置里的 Include environments 要单独看。
url: /guides/codex-data-controls-training
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 社区热点
entry_tags: [App, CLI, Web]
difficulty: 入门
order: 23
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-04
date_modified: 2026-11-04
verified_on: 2026-11-04
official_ref: https://help.openai.com/en/articles/7730893
keywords: [Codex 训练数据, Codex 数据控制, Improve the model for everyone, Codex Include environments, Codex 隐私设置, Codex 关闭训练]
related: [codex-daybreak-blue, permissions-sandbox-approvals, codex-plugin-hook-audit]
faq:
  - q: Plus 和 Pro 用户的 Codex 任务默认会被用来训练吗？
    a: 会。帮助中心写明，Free、Plus、Pro 的个人工作区默认开启数据共享。要关，就在 Settings → Data controls 里关掉 Improve the model for everyone，或者在 Privacy Portal 里选 Do not train on my content，二选一即可。
  - q: 关了 Improve the model 之后，Codex 还要另外设置什么？
    a: Codex 设置里有一个单独的 Include environments，控制 Codex 环境里的额外上下文能不能用于训练。改 ChatGPT 设置或走 Privacy Portal 都不会改到它，要去 Codex 设置里单独确认。
  - q: 有人说开关被偷偷打开了，是真的吗？
    a: 2026-11 和 2026-09 的 Hacker News 上都有用户这么报告，OpenAI 没有确认过设置被重置。本文没法验证，只建议定期去设置页看一眼。
  - q: Business 和 Enterprise 账号呢？
    a: 帮助中心写明，ChatGPT Business、Enterprise、Edu 和 API 的内容默认不用于训练。在这些工作区里点赞点踩，也不会让对应对话进入训练。
---

# Codex 对话会被用来训练吗：Improve the model、Include environments 和例外情况

> 本文在线版：[codexguide.io/guides/codex-data-controls-training](https://codexguide.io/guides/codex-data-controls-training)

> 核对依据：OpenAI 帮助中心 [Data controls in ChatGPT](https://help.openai.com/en/articles/7730893)（2026-11-04 抓取时页面显示当天更新）、[How your data is used to improve model performance](https://help.openai.com/en/articles/5722486) 和 [Advanced Account Security](https://help.openai.com/en/articles/20001221-advanced-account-security)。设置项名称按英文界面原文写。本文没有截图：编辑部的测试机没有登录 ChatGPT 账号，没有拍到设置页。

## 先看结论：按账号类型看默认值

| 账号 | 默认会不会用于训练 | 要做什么 |
| --- | --- | --- |
| Free、Plus、Pro 个人工作区 | 会 | 关 Improve the model for everyone，再查 Codex 的 Include environments |
| ChatGPT Business、Enterprise、Edu | 不会 | 以组织的策略为准 |
| API Key（Platform） | 不会 | 组织所有者开启数据共享时例外 |

个人账号还有两个例外。**点赞或点踩**会让那段对话可以被用于训练，即使你已经关了开关。**Daybreak 等 Trusted Access 会话**里的内容也可能被用于训练。详见下文。

## 这次为什么又有人问

2026-11-03 22:53（北京时间），Hacker News 上出现一帖 [「OpenAI seems to be silently re-enabling model training on Codex chats」](https://news.ycombinator.com/item?id=50352757)，截至 11-04 有 432 分、134 条评论。发帖人说，他和公司同事发现 Codex 的训练开关又被打开了。帖子里还提到 2026-09-10 的一帖 [Tell HN](https://news.ycombinator.com/item?id=49643556)，那次有 487 分、189 条评论，报告的现象差不多。

这些都是**用户报告，OpenAI 没有确认**设置会被自动改回去。本文没法验证。下面只讲官方文档怎么写、开关在哪里，以及怎么定期确认。

## 个人账号：关闭 Improve the model for everyone

帮助中心写明，Free、Plus、Pro 的个人工作区默认开启数据共享。关掉它不会删除聊天记录。

**网页版（已登录）**

1. 打开账号菜单。
2. 选 **Settings**。
3. 选 **Data controls**。
4. 点 **Improve the model for everyone**，关掉，点 **Done**。

**iOS 和 Android**

1. 打开侧边栏。
2. 点头像进入 **Settings**。
3. 选 **Data controls**。
4. 关掉 **Improve the model for everyone**。

登录状态下，这个开关对你账号下的网页和手机端都生效。没登录时用 ChatGPT，选择只保存在当前浏览器里。

## Privacy Portal：两种方式二选一

另一种方式是在 OpenAI 的 Privacy Portal 里选 **Do not train on my content**。帮助中心说：「Either option is sufficient for ChatGPT conversations and Codex tasks. You don't need to do both.」也就是说，对 ChatGPT 对话和 Codex 任务来说，两种方式选一种就够了，不用都做。

关掉之后，**新的**对话和任务不再用于训练。帮助中心没有说关掉会追溯以前的内容。

## Codex 的 Include environments 要单独设置

这是最容易漏掉的一项。两篇帮助文章都写了：

> Codex has a separate Include environments setting in Codex settings that controls whether additional context from your Codex environments can be used to train OpenAI models. Changing your ChatGPT setting or opting out through the Privacy Portal does not change that setting.

意思是：Codex 设置里有一个单独的 **Include environments**，控制 Codex 环境里的额外上下文（另一篇的说法是「完整环境」）能不能用于训练。改 ChatGPT 的设置、走 Privacy Portal，**都不会改到它**。

所以关完 Improve the model for everyone 之后，还要去 Codex 设置里找到 Include environments，确认它是关的。帮助中心只写了「在 Codex 设置里」，没给逐级菜单路径；界面改版时，以你看到的设置页为准。

## 例外：点赞点踩、Daybreak 会话

**点赞或点踩。** 个人账号（Free、Plus、Pro）即使已经关闭训练，只要你对某条回复点了赞或踩，**这条反馈对应的整段对话**都可能被用于训练。不想让某个 Codex 任务进入训练，就别在里面点反馈。

CLI 里的 `/feedback` 是另一回事：按官方命令文档，它把日志或诊断信息发给 Codex 维护者，用来排查问题，发送前会提示你选要附带什么。

**Daybreak 等 Trusted Access 会话。** 帮助中心写明：在个人账号上的 Daybreak 会话里，即使关了 Improve the model for everyone，OpenAI 也可能用这些交互内容改进模型，目的是加强防范网络滥用的安全措施。出了 Trusted Access 会话，你的开关照常生效。Daybreak 怎么申请和开启，见 [Codex Daybreak Blue](./12-Codex-Daybreak-Blue申请开启与排障.md)。

## 不会用于训练的情况

- **临时对话**：保持临时状态时，不进历史、不更新记忆、不用于改进模型，出于安全原因最多保留 30 天。你把它保存下来，它就变成普通对话，按账号设置处理。
- **ChatGPT Business、Enterprise、Edu、ChatGPT for Healthcare 工作区**：默认不用于训练。帮助中心还写明，这些工作区里的点赞点踩也不会让对应对话进入训练，除非组织另外签了允许训练的协议。管理员可以在 Admin Console 的 Workspace settings > Allow response feedback 里开关反馈。
- **API**：通过 API Platform 提交的输入和输出默认不用于训练。API 组织所有者可以开启数据共享，开了以后成员才能选择分享反馈和当前的 Playground 对话。用 API Key 登录 Codex 的情况，按 API 规则处理。

## 开关被改回去了？HN 报告和自查方法

官方没有确认会改回去，但检查一次花不了多少时间：

1. 每隔一段时间，或者账号套餐变动、换设备登录之后，去 **Settings → Data controls** 看一眼 Improve the model for everyone。
2. 同时打开 Codex 设置，看 **Include environments**。
3. 同一个账号有多个工作区（比如个人和公司）的，要分别看。默认值和管理权限按工作区区分。
4. 怀疑设置被改动过，可以在 Privacy Portal 再提交一次 Do not train on my content，作为第二道保险。帮助中心说两种方式都有效。

## 更严的做法：Advanced Account Security

个人账号还可以开启 [Advanced Account Security](https://help.openai.com/en/articles/20001221-advanced-account-security)。帮助中心写明：开启期间，对话不用于训练 OpenAI 模型。

代价不小：

- 至少要准备两种安全登录方式（通行密钥或 FIDO 安全密钥），其中一种能跨设备用。
- 密码登录、邮件和短信验证码、邮件找回账号都会被关闭。
- 设置完成后，所有设备都会退出登录，要用通行密钥或安全密钥重新登录。
- 登录方式和恢复密钥全丢了，可能永久进不了账号，OpenAI 支持也没法帮你恢复。

[OpenAI 的发布文章](https://openai.com/index/advanced-account-security/)（2026-04-30）说明，保护范围包括用同一个登录使用的 Codex。文章还写到，从 2026-06-01 起，Trusted Access for Cyber 的个人成员必须开启它。Daybreak 会话那条例外和这里的「不用于训练」同时出现时以哪条为准，两篇文档都没有说明，本文不做推断。

它在 **Settings → Security → Advanced Account Security** 里开启。企业管理的账号用不了。

## 常见问题

**关掉以后，以前的 Codex 任务会被删掉吗？** 不会。关训练不会删除或隐藏已保存的对话。要删内容，单独删对话或删账号。

**我在 CLI 里用 ChatGPT 账号登录，设置在哪里改？** 训练相关的开关都在账号层面，不在 `config.toml` 里。到网页版或桌面端的 Settings 里改，Codex 的 Include environments 在 Codex 设置里改。

**Business 工作区里，我还要关 Include environments 吗？** 帮助中心说 Business 工作区的内容默认不用于训练，Include environments 在这种工作区里怎么显示，文档没有说。以管理员的策略为准，拿不准就问管理员。

**这和 Codex 的沙箱权限有关系吗？** 没有。沙箱和审批决定 Codex 能在你电脑上做什么，见 [权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。训练开关决定内容会不会被拿去改进模型。两件事要分开管。

## 下一步

本地这边的风险，比如第三方程序改了你的 Codex 配置，见 [Codex 插件和 Hook 自查](./22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)。

## 参考资料

- [Data controls in ChatGPT](https://help.openai.com/en/articles/7730893)
- [How your data is used to improve model performance](https://help.openai.com/en/articles/5722486)
- [Advanced Account Security（帮助中心）](https://help.openai.com/en/articles/20001221-advanced-account-security)
- [Advanced Account Security（OpenAI 发布文章）](https://openai.com/index/advanced-account-security/)
- [Hacker News：OpenAI seems to be silently re-enabling model training on Codex chats](https://news.ycombinator.com/item?id=50352757)
