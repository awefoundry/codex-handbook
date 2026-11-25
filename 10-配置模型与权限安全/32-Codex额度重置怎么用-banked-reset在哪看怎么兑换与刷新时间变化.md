---
id: codex-banked-reset
title: "Codex 额度重置怎么用：banked reset 在哪看、怎么兑换，80% 门槛和下次刷新时间为什么会变"
seo_title: "Codex banked reset：在哪看、怎么兑换、刷新时间为何变"
description: "banked reset 是存在账户里、由你决定何时使用的一次 Codex 额度重置。本文按帮助中心说明桌面端、网页和 CLI 的 /usage 怎么兑换，以及 80% 门槛和下次刷新时间为什么会变。"
lede: "先看 Usage 里有没有可用的重置、它覆盖哪一档、什么时候过期。剩余还很高时，帮助中心写明兑不出去。"
url: /guides/codex-banked-reset
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 基础
order: 32
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-25
date_modified: 2026-11-25
verified_on: 2026-11-25
tested_cli_version: 0.172.0
official_ref: https://help.openai.com/en/articles/20001498-how-resets-work-in-codex
keywords: [Codex 额度重置, Codex banked reset, Codex Redeem reset, Codex /usage, ChatGPT Business Codex 重置]
related: [usage-limits-credits, model-at-capacity-usage-reset]
howto: true
faq:
  - q: "手机上能兑换 banked reset 吗？"
    a: "不能。帮助中心写明桌面端和网页可以，手机端没有这个入口，也没有重置历史。"
  - q: "为什么点了之后提示 Your usage does not need a reset right now？"
    a: "这次重置要覆盖的额度里，至少有一档剩余低于 80% 才能用。全部都在 80% 或以上时，重置继续留在账户里，直到你以后用掉或它过期。"
  - q: "兑换之后，原来的周五刷新还会发生吗？"
    a: "帮助中心的例子是：原本周五结束的周期如果在周二被重置重启，下一次刷新改到下一周的周二，原来的周五不再适用。订阅扣费日不因此改变。以下次在 Usage 里看到的时间为准。"
---

# Codex 额度重置怎么用：banked reset 在哪看、怎么兑换，80% 门槛和下次刷新时间为什么会变

> 本文在线版：[codexguide.io/guides/codex-banked-reset](https://codexguide.io/guides/codex-banked-reset)

> 核对依据：2026-11-25 打开的帮助中心 [How resets work in Codex](https://help.openai.com/en/articles/20001498-how-resets-work-in-codex)（页面标注 Updated: 28 days ago）和 [Response speed and usage resets in Work and Codex](https://help.openai.com/en/articles/20001596-response-speed-and-usage-resets-in-work-and-codex)（同样标注 28 天前更新）。CLI 斜杠命令对照的是同一天的 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)。Linux 上 `codex-cli 0.172.0` 未登录，`codex --help` 没有列出斜杠命令。没有打开交互式 TUI，没有登录桌面端或网页，没有配图。

5 小时和每周额度怎么读、Fast 倍率怎么算，见 [Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。界面写的是 **Selected model is at capacity**、要先分清容量满还是额度用尽，见 [容量不足与额度重置排查](../15-故障排查与常见问题/01-Codex模型容量不足与额度重置排查.md)。本文只讲重置本身：账户里存着的那一次怎么找、什么条件下能兑换、兑换后刷新时间为什么会变。

## 先说结论

banked reset 是 OpenAI 发给账户、由你自己决定何时使用的一次免费重置。收到它不会立刻刷新用量。它也不是永久提高套餐上限，也不会变成 credits。

划算的用法是：某一档主额度已经用掉一截、而你马上还有一大段要跑的时候再兑换。帮助中心写明，它要覆盖的额度如果全部还剩 80% 或更多，就会提示 **Your usage does not need a reset right now**，这次重置继续留着。

付费的即时重置是另一项购买，不是把 banked reset 用掉。手机端没有兑换入口。

## 三种重置不要混在一起

帮助中心把一次性重置分成三种，并且写明它们和套餐正常的定时刷新是分开的。

| 种类 | 帮助中心怎么说 | 你要不要自己点 |
| --- | --- | --- |
| OpenAI-granted banked reset | 免费、一次性，存进账户以后再用，也包括符合条件的推荐活动换来的重置。收到不等于用量已经刷新 | 要。过期前由你选择何时用 |
| OpenAI-granted automatic reset，有时叫 global reset | 免费，直接作用在这次活动选中的账户和用量限制上。不进 banked 余额。「Global」不是每个账户、每一档额度都会碰到 | 不用兑换 |
| Purchased reset，付费即时重置 | 买来立刻用，而不是存起来。只向部分 Plus 和 Pro 个人账号提供；有这些套餐也不保证买得到 | 购买时即用 |

免费的 banked 和自动重置，帮助中心写成酌情发放的推广福利，没有保证的供应或日程。付费重置的购买细节，该页指向另一篇 Paid weekly Work and Codex rate limit resets，本文没有展开价格。

另一篇帮助中心用更短的话说了同一件事：Automatic reset 不用你操作，也不会显示成一条存好的重置；banked reset 存在账户里，过期前由你自己用。支持团队不能调查某次免费重置该不该发给你、不能补发、不能替换、不能延长，也不为这些免费福利提供补偿。付费重置如果买了却没恢复用量，要用购买时的账户联系支持。

## 在哪里看有没有可用的重置

帮助中心写的入口：

- 桌面端打开 **Settings > Usage & billing**。
- 网页打开 **Usage settings**。
- 手机端没有这个选项。

在用量摘要里找显示还有重置可用的那一栏，例如 **1 reset available** 或 **Full reset**。先看它覆盖哪些用量限制、什么时候到期，再确认要用。

CLI 的说法见下一节。桌面端的 **Use reset** 用的是 **Available** 里已经存着的重置。**Buy an instant reset** 打开的是另一项付费购买。买完付费重置，不会扣你的 banked 余额。

2026-11-25 这台机器没有登录，没有桌面应用，所以上面的菜单名只来自帮助中心，不是这次点出来的界面。

## CLI 里的 /usage

帮助中心写：在 Codex CLI 输入 `/usage`，选择 **Redeem reset**。如果你的 CLI 版本没有这个选项，改用桌面端或网页。

同一天的 [Developer commands](https://learn.chatgpt.com/docs/developer-commands) 把 `/usage` 写成：查看账户 token 用量，或使用一次速率限制重置。步骤是：

1. 输入 `/usage`，打开用量菜单。
2. 选择是显示 token 活动，还是兑换一次可用的已获得重置（redeem an available earned reset）。
3. 要直接打开 token 活动，可以输入 `/usage daily`、`/usage weekly` 或 `/usage cumulative`。

该页的预期结果是：Codex 打开用量操作，或显示所选视图的账户 token 活动。会话如果没有 Codex 服务账号认证，会显示需要登录。

桌面端的 [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands) 是另一张表。那里的 `/usage` 写成：在使用 ChatGPT 登录且该命令可用时，打开用量和账单设置。不要把这两张表里的 `/usage` 当成同一个菜单。

2026-11-25 在 Linux 上核对的是 `codex-cli 0.172.0`。`codex login status` 为 Not logged in。`codex --help` 只列启动参数和子命令，没有列出 `/usage`。没有打开 TUI，所以没有看到菜单上是不是写着 **Redeem reset**。帮助中心用的是这个英文名；Developer commands 用的是「兑换一次可用的已获得重置」。两处都没有写出版本号。0.172.0 的交互菜单里到底显示哪一句，本文没有看到。

## 为什么兑换不了

从 **Usage settings** 使用 banked reset 时，它要覆盖的额度里，至少有一档剩余必须低于 80%。如果覆盖的每一档都还剩 80% 或更多，你会看到：

```text
Your usage does not need a reset right now
```

这次重置继续可用，直到你以后用掉，或者它到期。

也可以在桌面端打开 **Allow your assistant to use resets**，让 Codex 使用 banked reset。帮助中心写明，这个选项要求主 5 小时额度或每周额度剩余在 10% 或以下。

如果一次重置被意外用掉了，帮助中心建议看 History 里的记录，以及最近和 Codex 的对话里有没有要求或确认使用重置。以后只想自己手动点，就把 **Allow your assistant to use resets** 关掉。用量更新可能要等一小会儿。看起来不对时，先刷新或重新打开 Usage settings，确认账户、工作区和看的是哪一档。不要为了试第一次有没有生效，再兑一次或再买一次。

## 兑换后恢复哪些额度

一次 full banked reset 恢复的是当前套餐上的主 Codex 额度：

| 套餐 | 帮助中心写明会恢复的额度 |
| --- | --- |
| Go | 月额度 |
| Plus 和 Business Standard | 5 小时额度和每周额度 |
| Pro 100、Pro 200、Pro 500 | 每周额度 |

使用时，每一档被覆盖且低于 100% 的额度恢复到 100%。已经是 100% 的那一档，不会被这次 banked reset 重新开始计时。

同时有 5 小时和每周两档的套餐，同一份用量会计入两边，但两档的结束时间可以不同。帮助中心的例子是：每周周期中午结束，当前 5 小时周期继续到下午 3 点。在你再次使用之前，可能出现每周还剩 100%、5 小时只剩 10%。这时用一次 banked reset，会恢复 5 小时额度，而不重启每周周期。

只有在至少恢复了一档被覆盖的额度时，这次 banked reset 才算用掉。如果没有任何一档符合条件，重置仍然留着。

「Full」指的是主 Codex 额度。单独的模型或功能额度不受影响，帮助中心点名的是 ChatGPT 的图片生成、文件上传和普通 Chat Voice。

## 下次刷新时间为什么会变

banked、global 和付费重置都可以改变它们影响到的那一档的下次刷新时间，而不改变订阅扣费日。一次重置如果重启了用量周期，新日程替换旧日程。

帮助中心的例子：原本周五结束的每周周期，如果周二被重启，下一次刷新是下一周的周二，原来的周五不再适用。

下次刷新时间要看 **Usage**，不要用你点下重置、完成购买或看到公告的时刻自己推算。新周期开始之前，页面上的时间可能是估计值，还会变。单是这个日期变了，不能说明又用掉了一次 banked reset。

如果 global reset 覆盖的是你刚刚用 banked reset 恢复过的同一档，它会把那一档再次带回 100%，并且可以再改一次下次刷新时间。例子：上午 10:00 用了 banked reset，随后用掉刷新后额度的 5%；上午 10:30 的 global reset 把它从 95% 带回 100%。两次不会加在一起变成 200%。

已经用掉的 banked reset 不会退回来。还没使用的 banked reset 留在余额里，到期日和活动条款保持原样，因为 global reset 不消耗它们。

## 历史、到期和支持能做什么

桌面端在 **Settings > Usage & billing** 里，于 **Usage limit resets** 下选择 **History**，可以看到过去 30 天的 banked reset 记录。手机端目前没有这段历史，也没有重置控件。

| History 里的字 | 帮助中心的意思 |
| --- | --- |
| Reset received | 增加了一次以后再用的 banked reset。不是用量已经刷新 |
| Reset used | 一次 banked reset 被兑换了 |
| Available | 还能用的 banked reset 和它们的到期日 |

History 里一条「已收到」的记录，可能已经用掉或过期，不能用它判断现在还有没有。付费重置和 global 重置不出现在这段历史里。看不到记录，不能说明付费重置失败，也不能说明你错过了一次 global reset。global reset 可以改变额度和下次刷新时间，而不写一条历史。

History 也不显示你为什么符合资格、是谁或什么触发了使用，以及它怎样改了额度和日期。单看额度或日期变了，不能认出是哪一次 global reset。

免费重置的资格和到期由 OpenAI 按每次活动选择：接收人、覆盖的限制、发放时间和到期时间。要看原公告里的套餐、账户、地区限制、资格截止日期和后续更新。别人同套餐收到了，或者你以前的活动收到过，都不保证这次还有。

一次活动可以只有自动重置、只有 banked reset，或两种都有。如果只有自动重置，你不会得到一次可以存起来的 banked reset。banked 活动的发放窗口说的是预计什么时候加到账户上，符合条件的账户可能在窗口内的不同时间收到。

要在账户或活动显示的到期日和时间之前使用，有时区就看那个时区。这是兑换截止时间。用掉之后，刷新出来的额度按它自己的用量周期和下次刷新时间走。

banked reset 不是现金，不是 API credits，也不能当作可转让的余额。推荐活动的条款，帮助中心指向 ChatGPT Desktop Referral Promotions，本文没有改写那一页。

付费重置的收据在桌面端 **Settings > Usage & billing**，或网页 **Settings > Billing**。收据确认的是购买，本身不证明重置已经加上。

免费推广重置的限制，帮助中心写明：支持不审查个人是否符合资格，不调查一次免费重置该不该发放或有没有加上，不改活动条款，也不把某个账户加进活动。支持不提供人工或 courtesy 的推广重置，不延长到期日，也不替换没收到、已过期、误用、或随后又被另一次重置盖过的免费重置。不为这些免费福利提供 credits、退款或其他补偿。付费购买和其他账单另算。

## 怎样确认这次重置已经生效

帮助中心没有给出一个单独的成功动画。可以核对的是：

1. 被覆盖且原本低于 100% 的主额度，回到 100%。已经是 100% 的那一档不会被重新计时。
2. 桌面端 History 里出现 **Reset used**。付费重置和 global 重置不会出现在这里。
3. Usage 上的下次刷新时间可能已经换成新周期。单看日期变了，不能断定用的是哪一种重置。
4. 图片生成、文件上传、普通 Chat Voice 这些单独额度，按帮助中心的说法保持不变。不要用它们来判断主额度有没有被重置。

用量可能要过一小会儿才更新。刷新 Usage settings，并确认账户和工作区。

## 参考资料

- [How resets work in Codex](https://help.openai.com/en/articles/20001498-how-resets-work-in-codex)
- [Response speed and usage resets in Work and Codex](https://help.openai.com/en/articles/20001596-response-speed-and-usage-resets-in-work-and-codex)
- [Developer commands 的 /usage](https://learn.chatgpt.com/docs/developer-commands)
- [Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)
