---
id: codex-chatgpt-subscription-api-credits
title: Codex 与 ChatGPT 订阅 API 额度：Pro 和 Business 每月最高 500 美元怎么领，能不能用在 Codex
seo_title: ChatGPT Pro/Business 送 API 额度：怎么领、能不能用在 Codex
description: 2026-10 起，ChatGPT Pro 和 Business 订阅可以领 OpenAI API 额度，每月最高 500 美元。本文讲清谁能领、各档金额、在哪里领、额度用完会怎样，以及最容易误会的一点：这笔额度不能支付 Codex 的 API Key 用量，也不增加 Codex 的用量上限。
lede: 订阅送的 API 额度是给你自己写的应用和 Agent 用的，不是 Codex 的额外额度。
url: /guides/codex-chatgpt-subscription-api-credits
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 基础
order: 16
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-29
date_modified: 2026-10-29
verified_on: 2026-10-29
official_ref: https://developers.openai.com/api/docs/guides/chatgpt-api-credits
keywords: [Codex API 额度, ChatGPT Pro API credits, ChatGPT Business API 额度, Codex API Key 计费, credit_balance_exhausted]
faq:
  - q: 领了 API 额度以后，用 API Key 登录 Codex 能花这笔钱吗？
    a: 不能。官方 Help Center 和开发者文档都写明，这项权益不覆盖通过 API Key 使用 Codex 的用量。用 API Key 登录 Codex 时，按标准 API 价格从你的 API 组织扣费。
  - q: 这笔额度会让我在 Codex 里能用得更多吗？
    a: 不会。它不增加 ChatGPT 或用 ChatGPT 账号登录的 Codex 的用量上限，也不增加个人 credits 余额或 Business 工作区的 credits 余额。
  - q: Plus 能领吗？
    a: 不能。符合条件的只有 Pro（100、200、500 美元三档）和有付费 Standard 或 Premium 席位的 Business 工作区。Plus、免费试用、赠送的订阅不符合；Enterprise、Edu 和旧版 Codex 席位也不在范围内。
  - q: 没用完的额度下个月还能用吗？
    a: 不能。每期额度在该订阅计费周期结束时过期，不结转。
  - q: 额度用完以后会自动扣我的钱吗？
    a: 不会自动扣。如果组织里还有自己买的 API 额度，就接着用买的；如果什么额度都没有了，API 请求会返回 HTTP 429，错误码 credit_balance_exhausted。领取和使用这笔额度都不需要绑定 API 付款方式。
related: [usage-limits-credits, codex-openai-developers-plugin, codex-cli-multi-entry-setup]
---

# Codex 与 ChatGPT 订阅 API 额度：Pro 和 Business 每月最高 500 美元怎么领，能不能用在 Codex

> 本文在线版：[codexguide.io/guides/codex-chatgpt-subscription-api-credits](https://codexguide.io/guides/codex-chatgpt-subscription-api-credits)

> 核对依据：OpenAI 官方 Help Center [API credits benefit for eligible ChatGPT subscriptions](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions) 和开发者文档 [API credits for ChatGPT subscribers](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)，以及 @OpenAIDevs 2026-10-29 的[公告](https://x.com/OpenAIDevs/status/2115583698074755078)。Codex 的计费规则来自官方 [Authentication](https://learn.chatgpt.com/docs/auth) 文档。本文没有用真实的 Pro 或 Business 账号领取，领取步骤按官方文档整理。核对日期 2026-10-29（北京时间）。

## 一句话结论

- **谁能领**：付费满 7 天的 ChatGPT Pro（100、200、500 美元三档），以及有付费 Standard 或 Premium 席位的 Business 工作区。Plus 不能领。
- **领多少**：Pro 每月 100、200 或 500 美元；Business 每个 Standard 席位 20 美元、每个 Premium 席位 100 美元，整个工作区每月最多 500 美元。
- **能不能用在 Codex**：**不能**。这笔额度不覆盖用 API Key 跑 Codex 的费用，也不增加 Codex 的用量上限。它是给你调用 OpenAI API 开发自己的应用和 Agent 用的。

## 这是什么

OpenAI 在 2026-10-29 宣布：符合条件的 ChatGPT Pro 和 Business 订阅，可以把订阅关联到一个自己拥有的 **OpenAI API 组织**，然后每个计费周期自动拿到一笔 API 额度。

它和 Codex 里常说的「额度」不是一回事。Codex 里有三种容易混在一起的东西：

| 名称 | 在哪里看 | 用来做什么 | 和这次的 API 额度有没有关系 |
|---|---|---|---|
| Codex 用量上限（5 小时、每周） | Codex 里的 `/status`、`/usage` | 用 ChatGPT 账号登录时，订阅包含的 Codex 用量 | 没有。API 额度不会提高这个上限 |
| ChatGPT credits | ChatGPT 账单页 | 用量上限用完后继续用 Codex | 没有。API 额度不进 credits 余额 |
| **API 额度（本文）** | [API Platform 账单页](https://platform.openai.com/settings/organization/billing/overview) | 调用 OpenAI API（Responses、Agents 等） | 就是它 |

Codex 用量上限和 credits 的细节见[Codex 用量额度怎么看](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

## 谁能领

按官方 Help Center，需要**同时**满足：

1. **订阅类型**：ChatGPT Pro 100、Pro 200、Pro 500，或有付费 Standard 或 Premium 席位的 Business 工作区。
2. **付费满 7 天**：付费订阅至少已经生效 7 天。
3. **两边都是所有者**：
   - Pro：你是这个订阅的所有者，同时是接收额度的 API 组织的 Owner。
   - Business：领取的人必须**既是 ChatGPT 工作区的所有者，又是 API 组织的 Owner**。只是工作区成员或管理员角色不够。
4. **邮箱一致**：ChatGPT 账号和用来关联的 API 账号使用同一个邮箱。
5. **一对一**：一个订阅（或工作区）只能关联一个 API 组织，一个 API 组织也只能有一个这样的有效关联。

不符合条件的：Plus、免费试用、赠送的订阅。Enterprise、Edu 和旧版 Codex 席位也不在这次的范围内。

Help Center 还写了：能不能看到这个入口，还取决于开放批次和所在国家或地区。

## 各档能领多少

| 订阅 | 每个完整计费周期的 API 额度 |
|---|---|
| Pro（100 美元档） | 100 美元 |
| Pro（200 美元档） | 200 美元 |
| Pro（500 美元档） | 500 美元 |
| Business Standard 席位 | 每个付费席位 20 美元，整个工作区合并计算 |
| Business Premium 席位 | 每个付费席位 100 美元，整个工作区合并计算 |
| Business 工作区上限 | 每月合计最多 500 美元；年付最多 6,000 美元 |

Business 的算法是「(20 × Standard 席位数 + 100 × Premium 席位数) 和 500 取小」。官方举的例子：

- 5 个 Standard + 3 个 Premium：100 + 300 = **400 美元**。
- 10 个 Standard + 4 个 Premium：200 + 400 = 600 美元，超过上限，按 **500 美元**。

还有几点：

- **第一期按剩余天数折算**。月中领取，第一笔会少于上表的整月金额，以领取页面显示的数字为准。
- **年付的 Business 工作区一次发一整年**，最多 6,000 美元，在年度计费周期结束时过期。
- 升级 Pro 档位、给 Business 加付费席位或升级席位类型，当期可能补发一笔折算额度（仍受上限约束）。减少席位从下一期开始生效；把已有席位换给另一个人不会多发。

## 在哪里领

两条路，结果一样：都是把订阅关联到你选定的 API 组织。

**从 ChatGPT 领：**

1. 用拥有这个订阅的账号登录 [ChatGPT](https://chatgpt.com/)。Business 要先切到对应的工作区。
2. Pro 打开 [Settings → Billing](https://chatgpt.com/settings/billing)；Business 打开工作区的账单设置，或者 [Admin Console](https://admin.openai.com/)。
3. 找到 API credits 权益，开始领取。
4. 确认接收额度的 API 组织。如果你名下有多个符合条件的组织，选一个。
5. 确认，权益生效。

**从 API Platform 领：**

1. 用订阅所用的同一个邮箱登录 [API Platform](https://platform.openai.com/)。
2. 选中你拥有、要接收额度的 API 组织。
3. 打开 [Billing](https://platform.openai.com/settings/organization/billing/)，找到这项权益。
4. 选择要关联的订阅或 Business 工作区。
5. 确认，权益生效。

没用过 API 也可以领：可以直接关联到你的个人 API 组织（Personal API Organization），不需要先走完 API 的开通流程。

领完以后，到 [API Platform 账单页](https://platform.openai.com/settings/organization/billing/overview) 看额度。Help Center 提醒：「关联成功」和「额度到账」是两步，关联后没看到额度，要先确认选中的是关联的那个组织。

**选组织要谨慎**：换接收组织需要联系客服，而且不保证能转移额度。也不要为了绕过已有关联反复领取。

## 能用在什么地方

额度只能用在**被关联的那个 API 组织**里，调用时要选中这个组织，用它下面项目的 API Key。

官方列出的覆盖范围：

- Responses API（文本、代码、图像理解），以及 Chat Completions
- Agents API，包括 OpenAI 托管沙箱的费用
- Decisions API
- GPT-Live 和 Realtime API
- Images API
- 内置工具（网页搜索、文件搜索、Code Interpreter 等）及其用量和存储费用

**不覆盖**：通过 API Key 使用 Codex 的用量。

## 为什么不能用在 Codex

这是这次最容易误会的地方。官方开发者文档的原话：

> Codex usage through API keys is not supported by this benefit. These API credits also don't increase your ChatGPT or signed-in Codex usage limits.

拆开说就是两层：

1. **用 API Key 登录 Codex**（`codex login --with-api-key`，或在 App、IDE 里选「用 API Key 登录」）：Codex 按标准 API 价格计费，这笔订阅赠送的额度**不能**用来支付。
2. **用 ChatGPT 账号登录 Codex**：用的是订阅自带的 Codex 用量上限和 credits，这笔 API 额度**不会**让上限变高。

所以如果你的目标是「Codex 用得更多」，这项权益帮不上忙。要看的仍然是订阅档位、用量上限和 credits，见[Codex 用量额度怎么看](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。两种登录方式的区别见[Codex CLI 安装、登录与多入口配置](../12-官方工具与集成/09-CodexCLI国内使用与多入口配置.md)。

它适合的场景是：**用 Codex 写一个调用 OpenAI API 的应用**，应用运行时的 API 调用花这笔额度。比如让 Codex 帮你搭一个调用 Responses API 的小工具，工具自己的请求从额度里扣。在 Codex 里创建 API Key、写入项目，可以用官方的 OpenAI Developers 插件，见[Codex 安装 OpenAI Developers 插件](../09-MCP与外部工具/08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md)。

## 续期、过期和用完以后

- **自动续期**：领一次就行。之后每次订阅续费，只要权益还在、订阅仍符合条件，额度会自动发放。
- **当期过期，不结转**：月付的额度在计费周期结束时过期，没用完的不会带到下个月。
- **先扣赠送额度**：组织里同时有赠送额度和自己买的额度时，先扣赠送的。
- **不需要绑卡**：使用有效的赠送额度，不需要给 API 组织添加付款方式。
- **用完以后**：

| 组织余额 | 结果 |
|---|---|
| 还有自己买的 API 额度 | 接着用买的额度 |
| 什么额度都没有了 | API 请求失败，返回 HTTP `429`，错误码 `credit_balance_exhausted` |

要继续用，就在 API 组织的账单设置里购买额度，或开启 Auto Recharge（自动充值）。开启前看清充值阈值、目标余额和每月购买上限。

另外，额度不等于没有限制：请求速率、Token 速率、模型、组织和项目的限制照常生效，可以在 [Limits 页面](https://platform.openai.com/settings/organization/limits) 查看。

## 换订阅、退订会怎样

| 操作 | 结果 |
|---|---|
| 取消订阅 | 新的额度停止发放；已经发的额度不收回，可以用到当期结束 |
| 降级到 Plus、Go 或 Free | 计费周期结束时解除与 API 组织的关联 |
| 从 Pro 换到 Business | Pro 的关联结束；Business 付费满 7 天后，由工作区所有者重新关联 |
| Business 迁到 Enterprise | 计费周期结束时解除关联；Enterprise 不符合条件 |
| 关联 Business 的那位所有者离开工作区 | 关联被解除；当期结束前，订阅和 API 组织都不能重新关联 |
| 订阅全额退款 | 对应的未用完赠送额度会被移除 |

## 常见误会

**「Business 插件 credits」和这个是一回事吗？**
不是。Help Center 专门说明：ChatGPT Business 的插件 credits 促销是另一个活动，加的是工作区 credits；这次的 API 额度放在 API 组织里，规则也不同。

**我是 Business 工作区的管理员，能替团队领吗？**
不能只凭管理员身份。必须是工作区的所有者，同时也是 API 组织的 Owner。另外，ChatGPT 席位不会自动给同事 API 组织或项目的访问权限，要在 API Platform 里单独加。

**看不到领取入口怎么办？**
按 Help Center 的顺序查：订阅是否是 Pro 或 Business、付费是否满 7 天、选中的是不是对的工作区、账号邮箱是否一致。Business 请所有者去工作区账单页看。都没问题还看不到，可以联系客服，附上这些信息。

**截图发给客服时要注意什么？**
Help Center 提醒要去掉截图里的敏感信息，不要发送密码或 API Key。

## 下一步

- 搞清 Codex 自己的用量上限和 credits：[Codex 用量额度怎么看](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)
- 在 Codex 里安全创建 API Key、写进项目：[Codex 安装 OpenAI Developers 插件](../09-MCP与外部工具/08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md)
- 分清 ChatGPT 登录和 API Key 登录：[登录 Codex](../01-安装与首次使用/07-登录Codex.md)

## 参考资料

- OpenAI Help Center：[API credits benefit for eligible ChatGPT subscriptions](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions)
- OpenAI 开发者文档：[API credits for ChatGPT subscribers](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)
- OpenAI 官方文档：[Authentication](https://learn.chatgpt.com/docs/auth)
- @OpenAIDevs 公告（2026-10-29）：[x.com/OpenAIDevs/status/2115583698074755078](https://x.com/OpenAIDevs/status/2115583698074755078)
