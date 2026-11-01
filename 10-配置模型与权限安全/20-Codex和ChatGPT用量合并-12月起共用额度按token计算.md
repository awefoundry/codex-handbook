---
id: codex-chatgpt-shared-usage-limits
title: Codex 和 ChatGPT 用量合并：12 月起 Plus、Pro、Business 共用一份额度，按 token 计算，Instant 不计入
seo_title: Codex 与 ChatGPT 用量合并：12 月起共用额度，Instant 不计
description: OpenAI 宣布从 12 月起，Plus、Pro 和 Business 的 ChatGPT 与 Codex 共用一份用量额度，按 token 计算，Instant 对话不计入。本文按帮助中心原文整理变化、查看位置和用完后的选择，并写明尚未公布的生效日与套餐范围。
lede: 12 月起，Plus、Pro、Business 的 ChatGPT 和 Codex 共用一份额度。具体哪一天、每个套餐多少 token，帮助文章没有写。
url: /guides/codex-chatgpt-shared-usage-limits
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [Chat, App, CLI]
difficulty: 基础
order: 20
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-01
date_modified: 2026-11-01
verified_on: 2026-11-01
official_ref: https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits
keywords: [Codex ChatGPT 用量合并, Codex 共享额度, Codex 用量按 token 计算, ChatGPT Codex usage limits, Codex 12 月用量变化]
related: [usage-limits-credits, model-at-capacity-usage-reset, model-reasoning-effort, codex-switch-multiple-accounts]
faq:
  - q: 12 月几号开始共用额度？
    a: 官方暂未说明。帮助中心写的是 Starting in December。Hacker News 上贴出的邮件写的是 in the coming weeks。两处都没有日历日期。
  - q: Plus、Pro、Business 各有多少 token？
    a: 官方暂未说明。帮助文章只说按 token 计算，消耗多少取决于模型和任务，没有给出各套餐的 token 数。
  - q: Free、Go、Enterprise、Edu 这次一起改吗？
    a: 官方暂未说明。帮助文章点名的是 Plus、Pro、Business。定价页仍写 Codex 包含在 Free、Go、Plus、Pro、Business、Edu、Enterprise 里，但没有把后面这几档写进 12 月的合并说明。
  - q: Instant 对话会计入合并后的额度吗？
    a: 不计入。帮助文章写 Instant chat will not draw from your usage。邮件写 Unlimited Instant is included in your plan and will not draw from your usage。
---

# Codex 和 ChatGPT 用量合并：12 月起 Plus、Pro、Business 共用一份额度，按 token 计算，Instant 不计入

> 本文在线版：[codexguide.io/guides/codex-chatgpt-shared-usage-limits](https://codexguide.io/guides/codex-chatgpt-shared-usage-limits)

> 核对依据：OpenAI 帮助中心《[Understanding ChatGPT and Codex usage limits](https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits)》（2026-11-01 打开），ChatGPT Learn《[Pricing](https://learn.chatgpt.com/codex/pricing)》（同一天打开），以及 [Hacker News 50321622](https://news.ycombinator.com/item?id=50321622) 里贴出的邮件正文。帮助文章里的「9 hours ago」是相对时间，正文不把它写成日历日期。

已经同时用 ChatGPT 和 Codex 的 Plus、Pro、Business 用户，需要知道 12 月以后额度怎么算。Free、Go、Enterprise、Edu 是否进入这次合并，帮助文章没有点名。

这篇只讲帮助文章宣布的合并规则，以及现在能做的准备。现行的 5 小时窗口、每周限制、Fast 倍率和 credits，见 [用量额度怎么看](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

## 先看结论

从 2026 年 12 月起，Plus、Pro、Business 的用量额度由 ChatGPT 和 Codex 共用。用量按 token 计算。模型和任务越重，消耗越多。Instant 对话不计入。

帮助文章给出的原因，是把 Work 的 agentic 能力并进 ChatGPT 的主体验。官方预计大多数用户等待重置的频率不会比现在更高。合并后的剩余额度和重置时间在 Settings → Usage。用完可以等重置、升级套餐，或购买 credits 继续使用符合条件的功能。

具体生效日、各套餐的 token 数、5 小时窗口和每周窗口在合并后是否保留，官方暂未说明。

## 哪些套餐写进了原文

帮助文章的原句是：Starting in December, Plus, Pro, and Business plans’ usage allowance will be shared across ChatGPT and Codex.

点名的是这三档。Free、Go、Enterprise、Edu 是否受这次合并影响，官方暂未说明。

定价页在 2026-11-01 仍写：ChatGPT Work and Codex are included in your ChatGPT Free, Go, Plus, Pro, Business, Edu, or Enterprise plan。同一页还有一句现行说明：ChatGPT Work and Codex share usage。这句说的是现在的 Work 和 Codex 共用用量，页面上没有 Starting in December，也没有把 Instant 排除在这次合并之外的那句话。两页要分开读。

定价页还写：Usage limits are shared with other agentic features once pricing for those features is effective. This currently includes ChatGPT for Excel on Plus and Pro。这是另一条已经生效的共用范围，不是帮助文章里的 12 月变更。

## 按 token 计算是什么意思

帮助文章把 token 定义成模型处理和生成的信息单位。用掉多少额度，取决于所选模型和所做的任务。更高级的模型、更复杂的任务，一般用得更多。

文章没有给出「一次普通任务等于多少 token」或「某套餐一共多少 token」。这些数字官方暂未说明。

定价页仍保留现行估算，而且写明这些估算不是固定的消息条数上限：Plus 和 Standard Business 有一张按模型列出的、每 5 小时本地消息数量区间；Pro 目前没有 5 小时限制；每周限制可能仍然适用。本地消息和云端任务共用套餐额度。这些是定价页上的现行规则。帮助文章没有说 12 月合并之后这张表还在不在，所以不能把表现在的区间写成合并后的 token 配额。

邮件（见下一节）同样只说用量取决于模型和任务，更高级的模型和更复杂的任务用得更多，没有给数字。

## Instant 不计入

帮助文章写：Instant chat will not draw from your usage.

[Hacker News 50321622](https://news.ycombinator.com/item?id=50321622) 在 2026-11-01 贴出一封署名为 The OpenAI team 的邮件，对应的句子是：Unlimited Instant is included in your plan and will not draw from your usage.

两处一致的范围是 Instant 对话不从额度里扣。邮件没有定义 Instant 覆盖哪些入口、有没有公平使用上限以外的例外。帮助文章也没有展开。超出这两句的细节，官方暂未说明。

## 在哪里看合并后的额度和重置时间

帮助文章和那封邮件都写：合并后的剩余额度和重置时间在 Settings → Usage。

2026-11-01 这篇帮助文章描述的是即将发生的界面。本环境没有 ChatGPT 桌面端或手机，打不开合并后的 Usage 页，所以这里不配图。旧的用量页不能用来代表合并之后的画面。

现行额度仍然可以在定价页说的 usage dashboard 里看；Codex CLI 会话里可以用 `/status` 看剩余限制。这两处是现在的入口。合并完成之前，Settings → Usage 里实际显示什么，以你自己账号上的页面为准。

额度已经用完、模型提示容量不足时，排查顺序见 [模型容量不足与额度重置](../15-故障排查与常见问题/01-Codex模型容量不足与额度重置排查.md)。

## 用完以后

帮助文章给出三条路：

1. 等额度重置。
2. 升级套餐。
3. 购买 credits，继续使用符合条件的功能。

邮件用了同一组选择。哪些功能可以用 credits 续上，帮助文章写的是 eligible features，没有在这篇里逐项列表。定价页对现行规则写得更具体：Plus 和 Pro 触达用量上限后可以购买 credits；带灵活定价的 Business、Edu、Enterprise 可以购买工作区 credits；所有用户也可以改用 API key 跑额外的本地会话，按 API 价格计费。这些是定价页上的现行说法。12 月合并之后 credits 的购买入口是否变化，官方暂未说明。

## 现在可以做的准备

帮助文章把消耗和「模型 + 任务」绑在一起。在合并日公布之前，能做的是把现在已经写进定价页的省额度办法用起来，并选适合任务的模型。模型怎么配、推理强度怎么选，见 [模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

定价页《What can I do to make my usage limits last longer?》列出的现行建议是：

- 把提示写精确，去掉不必要的上下文。
- 只提供相关文件，能缩小来源或日期范围时就缩小。
- 写明读者、格式和长度，把必做和可选改进分开。
- 控制 `AGENTS.md` 的体积；大项目可以用嵌套的 `AGENTS.md` 决定注入多少上下文。
- 少挂不需要的 MCP 服务器。每个 MCP 服务器都会给消息增加上下文。

这些是现行定价页的建议，不是帮助文章对 12 月新额度给出的计算公式。

多开账号不会把额度加总。切换账号不合并账单和订阅，见 [多账号切换](../01-安装与首次使用/16-Codex多账号切换-手机端双账号与CLI用CODEX_HOME分开登录.md)。用多个账号轮换来绕过额度，不在官方说明里，本文不写做法。

## 官方还没说明的问题

下面几项，2026-11-01 的帮助文章、定价页和上述邮件都没有给出可以写死的答案。

| 问题 | 现在能引用的原文 | 结论 |
|---|---|---|
| 具体生效日期 | 帮助文章：Starting in December。邮件：in the coming weeks | 官方暂未说明哪一天 |
| 各套餐的 token 总数 | 帮助文章只说按 token 计、取决于模型和任务 | 官方暂未说明 |
| 5 小时窗口、每周窗口是否保留 | 定价页仍按现行规则列出这两类限制；帮助文章没有谈合并后是否保留 | 官方暂未说明 |
| Free、Go、Enterprise、Edu | 帮助文章只列 Plus、Pro、Business | 官方暂未说明是否纳入这次合并 |
| 定价页是否已经改写成 12 月规则 | 2026-11-01 的定价页仍有 5 小时估算表，并写着 Work 与 Codex 现行共用 | 帮助文章的 December 变更还没有以同样的句子出现在定价页 |

Pro 各档用量上调、订阅里附带的 API 额度，是另外的题目，不在这篇里展开，这里也不链接尚未合并的稿件。

## 常见问题

**邮件和帮助文章哪一份算数？** 操作上以帮助中心文章为准。邮件是用户贴到 Hacker News 的文本，2026-11-01 仍可打开，内容和帮助文章大体一致，日期用词不同：邮件是 coming weeks，帮助文章是 Starting in December。

**现在的 5 小时限制是不是当天就取消了？** 帮助文章写的是 12 月起。定价页在核对当天仍描述 5 小时窗口和每周限制。合并完成前，按 [用量额度怎么看](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md) 里的现行规则使用。

**合并以后，ChatGPT 聊天和 Codex 写代码是两个桶还是一个桶？** 对 Plus、Pro、Business，帮助文章写的是一份 usage allowance，ChatGPT 和 Codex 一起用。Instant 对话除外。

## 参考资料

- [Understanding ChatGPT and Codex usage limits](https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits)（OpenAI Help Center，2026-11-01 核对）
- [Pricing](https://learn.chatgpt.com/codex/pricing)（ChatGPT Learn，2026-11-01 核对）
- [Tell HN: ChatGPT and Codex usage will be combined](https://news.ycombinator.com/item?id=50321622)（邮件转贴，2026-11-01 核对）
