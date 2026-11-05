---
id: codex-pro-business-premium-usage-increase
title: Codex 用量上调：Pro 100 和 Pro 500 翻倍、Pro 200 取消降额、Business Premium 也在内，怎么确认你的额度变了
seo_title: Codex 用量上调：Pro 100/500 翻倍，Pro 200 取消降额
description: 2026 年 10 月 29 日起，Codex 在 Pro 100、Pro 500 上的用量翻倍，Pro 200 原定的降额取消，Business Premium 也上调了。本文按官方说明讲清各档位变了什么、Plus 为什么不变、翻倍为什么不等于任务数翻倍，以及在哪确认自己的额度。
lede: 先看帮助中心按档位写的规则，再打开 Settings → Usage。帖文里的 “doubling all” 和 Pro 200 的两种情况要对在一起读。
url: /guides/codex-pro-business-premium-usage-increase
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [App, CLI, ChatGPT Work]
difficulty: 基础
order: 17
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
official_ref: https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers
keywords: [Codex 用量翻倍, Codex usage limits, Pro 200 降额取消, ChatGPT Pro 用量, Business Premium Codex 用量]
related: [usage-limits-credits, model-at-capacity-usage-reset, model-reasoning-effort, codex-chatgpt-shared-usage-limits, codex-chatgpt-subscription-api-credits]
faq:
  - q: Plus 这次一起翻倍了吗？
    a: 没有。About ChatGPT Pro tiers 写明 Plus usage is unchanged。
  - q: 已经在订阅的人要重新付款或取消再订一次吗？
    a: 不用。同一页写 existing subscribers receive it automatically without waiting for renewal。Pro 200 若订阅还在，也不必取消再订来拿到更新后的额度。
  - q: Business Premium 到底翻了几倍？
    a: 帮助中心 10 月 29 日条目只写 Business Premium 的 Work 和 Codex 用量在增加，没有给出倍数。Tibo 的帖文写 doubling。本文不自行换算。
  - q: 额度翻倍以后，能完成的任务是不是也翻倍？
    a: 官方写明不保证。用量仍取决于模型、任务和设置。Fast、Ultrafast 还会按倍率消耗同一份额度。
  - q: 找 Support 能把额度重置或再调高吗？
    a: 不能。Pro 档位说明写 Support cannot reset ChatGPT or Codex limits。他们可以查用量有没有记错，或重置时间过了仍恢复不了。
---

# Codex 用量上调：Pro 100 和 Pro 500 翻倍、Pro 200 取消降额、Business Premium 也在内，怎么确认你的额度变了

> 本文在线版：[codexguide.io/guides/codex-pro-business-premium-usage-increase](https://codexguide.io/guides/codex-pro-business-premium-usage-increase)

> 核对依据：OpenAI 帮助中心 [ChatGPT Business release notes](https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes) 的 2026-10-29 条目、[About ChatGPT Pro tiers](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers)（2026-11-05 打开，页面写 Updated: 2 days ago）、ChatGPT Learn [Pricing](https://learn.chatgpt.com/docs/pricing)（同一天）。公开说明另有 [Tibo 的帖](https://x.com/thsottiaux/status/2115850175868727621)（2026-10-29 16:56 UTC）和 [Andrew Ambrosino 的回复](https://x.com/ajambrosino/status/2115855769665147254)。本文没有登录任何 Pro 或 Business 账号，没有配 Usage 截图，也不引用帖文的点赞和浏览数字。

已经在用 ChatGPT Pro 或 Business Premium 跑 Codex 的人，想确认 10 月 29 日这次调整落在自己哪一档。Plus、以及 12 月才开始的额度合并，不是这一条。

面板上的 5 小时窗、每周窗和 credits 怎么读，见 [用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。模型容量满和重置类型，见 [容量不足与额度重置](../15-故障排查与常见问题/01-Codex模型容量不足与额度重置排查.md)。

## 先看结论

2026 年 10 月 29 日起，Pro 和 Business Premium 里包含的 Work 与 Codex 用量上调。帮助中心把各档写死了，和帖文的总括句要分开看：

| 档位 | 帮助中心怎么写 | 价格 |
|---|---|---|
| Pro 100 | Work 与 Codex 额度变为原来的两倍 | 每月 100 美元 |
| Pro 500 | Work 与 Codex 额度变为原来的两倍 | 每月 500 美元 |
| Pro 200 | 9 月 29 日邮件里通知的降额取消。原来较高的保持不变；原来较低的从 10 月 29 日起翻倍，并对齐到同一上限 | 仍是每月 200 美元 |
| Business Premium | 包含的 Work 与 Codex 用量增加。条目没有写倍数 | 帮助中心这条没有写席位价格 |
| Plus | 用量不变 | 这条调整没有改 Plus |

新订阅和已经在订的人都适用更新后的额度。已经在订的人自动生效，不用等到下次续费，也不用取消再订一次。

帮助中心没有公布各档新的 token 数或「还能发多少条」。确认自己变没变，只能看登录后的用量面板。

## 帖文和帮助中心怎么对在一起读

[Tibo](https://x.com/thsottiaux/status/2115850175868727621)（X 简介为 Codex & ChatGPT）在 2026-10-29 写道：We are doubling all usage limits for all Pro 100/200/500 tiers and Business Premium, effective today. 紧接着写：不会降低 Pro 200 的用量限制，因此你的 Work 和 Codex 用量保持不变。

[Andrew Ambrosino](https://x.com/ajambrosino/status/2115855769665147254)（简介同样是 Codex & ChatGPT）回复的第一点是：usage limits are back to being double. 同一帖的第二点是要改进 App 的简单和性能，和额度规则无关，这里不展开。

帮助中心没有把 “doubling all” 原句写进 Pro 200 和 Business Premium。它的分档是：

- Pro 100、Pro 500：twice their previous Work and Codex allowance。
- Pro 200：降额取消；较高额度保持；较低额度 twice their previous，并 bringing them up to the same limit。Pro 档位页的另一句是：All Pro 200 subscriptions now include the same Work and Codex allowance。若你当时已经是较高额度，帮助中心写的是 keep it，不是在较高额度上再乘一次。
- Business Premium：We’re increasing the Work and Codex usage included in Pro and Business Premium plans。倍数只出现在 Pro 100 和 Pro 500 那一句里。

所以「我的 Pro 200 是不是也翻倍」取决于你 10 月 29 日之前在较高还是较低那一档。帮助中心没有给一个页面让人事后查询自己当时在哪一档。现在能做的是看 Usage 里的剩余和重置，而不是用帖文的总括句倒推一个数字。

同一条帖文还写：会继续提供 dots 的 extended limits，并且 dot 的用量仍与 default usage 分开。10 月 29 日的帮助中心条目没有这段。本文不把这句扩写成产品规则。

## Pro 200 的两种情况

Pro 档位页把已经在订的人分成两句：

- 你已经有较高的 Work 与 Codex 额度：保持这份较高额度。9 月 29 日邮件里说的降额取消。
- 你当时是较低额度：它已经翻倍，并对齐到和其他 Pro 200 相同的上限。

新开通的 Pro 200 也可以再订阅，月费仍是 200 美元，包含的是更新后的这份额度。取消之后再订，得到的也是和其他 Pro 200 相同的额度。订阅如果还有效，不必为了这次调整先取消。

预约取消不会立刻结束订阅。当前计费周期结束前仍可使用，并可以在结束前撤销取消。

Ultrafast 不因为这次额度对齐而出现在 Pro 200 上。Pro 档位页写：Ultrafast 只在 Pro 500。在 Pro 100 或 Pro 200 上购买 credits，页面写 at launch 不会因此解锁 Ultrafast。

## Business Premium 和 Plus

Business 更新日志把 Business Premium 和 Pro 写在同一条标题里：More Work and Codex usage on Pro and Business Premium Plans。正文对 Business Premium 只用了 increasing，没有 twice。本文不把 Tibo 帖文里的 doubling 换算成 Business Premium 的一个倍数。

Plus 的句子在 Pro 档位页：Plus usage is unchanged。这次调整没有写 Free、Go、Enterprise、Edu。

Business Premium 的席位价格、以及增加之后的具体上限，10 月 29 日这条和 Pro 档位页都没有写。

## 额度翻倍不等于能完成的任务翻倍

Pro 档位页的原句是：The amount of work you can complete still depends on the model, task, and settings. A larger allowance does not guarantee twice as many completed tasks.

定价页把原因写得更具体：看起来相似的任务，消耗会因为模型、上下文、推理、工具、检索和缓存而不同。它还给了 Plus 和 Standard Business 的本地消息估算区间，并写明这些估算不是固定的消息条数上限。Pro 目前没有 5 小时限制。这些是定价页上的现行说法，不是 10 月 29 日条目新公布的配额表。本地消息区间见 [用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)，不要把表里的区间当成自己的新上限。

同一份额度还会被速度档放大。定价页 2026-11-05 的倍率表，相对同一模型的 Standard：

| 速度档 | 套餐内含额度 | 已购 credits，以及 Enterprise 按量 |
|---|---|---|
| Fast | 2.5 倍 | 2 倍 |
| GPT-6 Astra Ultrafast | 8 倍 | 6 倍 |
| GPT-6.1 Sol Ultrafast | 8 倍 | 6 倍 |

Pro 档位页对 Ultrafast 的说法与这张表一致：GPT-6 Astra 和 GPT-6.1 Sol 先按 8 倍消耗套餐内含额度，内含用完后按 6 倍消耗 credits。它同时写明这些是消耗倍率，不是更快的性能保证。Fast 对内含额度是 2.5 倍。模型怎么选，见 [模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

## 不要和另外两次额度变更混在一起

10 月 29 日这条，改的是 Pro 与 Business Premium 当前包含的 Work / Codex 用量。

另外两件是不同的说明：

- 12 月起 Plus、Pro、Business 的 ChatGPT 与 Codex 共用额度、按 token 计算、Instant 不计入。见 [用量合并](./20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md)。帮助文章没有把 10 月 29 日的翻倍写进那次合并。
- Pro 和 Business 可以领取的 API 额度，不能用来支付 Codex 的 API Key 用量，也不增加用 ChatGPT 账号登录时的 Codex 上限。见 [订阅 API 额度](./16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)。

还有一条容易看成同一次调整、其实分开写的限制：每周的 GPT-6 Pro 消息上限。Pro 档位页写，这是 Chat 里的消息上限，和 Work / Codex 额度分开。Pro 100 和 Pro 500 保持原来的每周上限。Pro 200 上，较低的每周上限对齐到较高的那一档；原来已经是较高上限的，保持不变。

## 怎么确认自己的额度

官方给出的位置：

- ChatGPT 里打开 **Settings → Usage**。
- Codex 里是 **Usage & Billing**。购买 credits 时，Pro 档位页也指向这两个入口。
- 定价页写：用量仪表板可以看到当前限制和重置时间。CLI 会话进行中，用 `/status` 看剩余限制。

本文没有登录，所以没有截到这些面板，也不引用任何一张「还剩百分之几」的数字。你自己的面板如果和帖文的措辞对不上，以面板上的剩余、重置时间和套餐名称为准。

Support 不能手动重置 ChatGPT 或 Codex 的限制。若你认为计数错了，或重置时间过了仍用不了，可以请他们查。模型到了自己的上限时，界面会在有重置时间时显示出来；换一个还能用的模型，或等到重置。不能靠某个设置绕过上限。

## 已订阅的人要做的事

按 Pro 档位页，已经订阅的人不用操作：

1. 打开 Settings → My Plan，确认档位仍是你以为的 Pro 100、Pro 200 或 Pro 500。
2. 打开 Settings → Usage（Codex 里是 Usage & Billing），看当前剩余和重置时间。
3. CLI 里在一次会话中运行 `/status`，和面板对照。
4. 订阅还在的话，不要为了「领到翻倍」而取消再订。

Business Premium 的管理员同样看工作区的用量页面。帮助中心没有写一个单独的「已翻倍」标记。

## 参考资料

- [ChatGPT Business release notes](https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes)（October 29, 2026）
- [About ChatGPT Pro tiers](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Tibo，2026-10-29](https://x.com/thsottiaux/status/2115850175868727621)
- [Andrew Ambrosino 的回复](https://x.com/ajambrosino/status/2115855769665147254)
