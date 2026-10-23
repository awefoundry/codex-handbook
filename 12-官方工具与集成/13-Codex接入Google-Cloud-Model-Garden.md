---
id: codex-google-cloud-model-garden
title: Codex 接入 Google Cloud Model Garden：私有预览申请、Marketplace 计费，以及本地 CLI/Desktop 接 GCP 推理的公开边界
seo_title: Codex × Google Cloud Model Garden：私有预览、计费与本地接入边界
description: OpenAI 模型和 Codex 工作流正在进入 Google Cloud Model Garden，目前是面向部分企业客户的私有预览。本文只整理 OpenAI 与 Google Cloud 两篇官方公告写明的内容：上了哪些模型、怎么申请、账单怎么走、治理承诺，以及本地 Codex CLI/Desktop 接入目前公开到哪一步。
lede: 现在是私有预览，公开信息只到「可以接」。具体怎么接，以获批后的官方指引为准。
url: /guides/codex-google-cloud-model-garden
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 解读
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 13
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-23
date_modified: 2026-10-23
models: [gpt-6-astra, gpt-6.1-sol, gpt-6-luna]
official_ref: https://openai.com/index/openai-models-google-cloud/
keywords: [Codex Google Cloud, Model Garden, OpenAI GCP, Codex CLI GCP, Google Cloud Marketplace]
related: [codex-model-reasoning-effort]
faq:
  - q: 现在能自己在 GCP 控制台直接开通吗？
    a: 公告写的是向部分企业客户私有预览，需要通过兴趣表单申请；OpenAI 说正式开放（GA）计划在未来几周。
  - q: 费用算在哪里？
    a: 通过 Google Cloud Marketplace 交易，出现在 Google Cloud 账单上，可抵扣已有的 GCP 承诺消费；Google 还说会计入跨模型厂商的 Flexible Savings Plans。
  - q: 本地 Codex CLI 要改哪些配置？
    a: 两篇官方公告都没有给出具体配置项、endpoint 或命令。本文不猜测，以获批后 Google Cloud 或 OpenAI 提供的说明为准。
---

# Codex 接入 Google Cloud Model Garden：私有预览申请、Marketplace 计费，以及本地 CLI/Desktop 接 GCP 推理的公开边界

> 本文在线版：[codexguide.io/guides/codex-google-cloud-model-garden](https://codexguide.io/guides/codex-google-cloud-model-garden)

> 核对依据：OpenAI 官方博文《OpenAI models are coming to Google Cloud》与 Google Cloud 博文《Google Cloud brings OpenAI models to customers》，均发布于 2026-10-21，本文于 2026-10-23 核对。**这是私有预览阶段的说明，GA 时细节可能变化。**

10 月 21 日，OpenAI 和 Google Cloud 同时发文：OpenAI 的前沿模型和 Codex 的 agentic 工作流要进入 Google Cloud 的 Model Garden。对已经把预算和数据放在 GCP 的企业来说，这意味着可以在原有的云合同和治理体系里用 OpenAI 模型。

这篇文章只回答一件事：**按目前公开的官方信息，现在能做什么，还不能确定什么。** 两篇公告里没写的配置步骤，本文一概不写。

## 公告说了什么

Google Cloud 博文列出了首批进入 Model Garden 的三个 OpenAI 模型：

| 模型 | Google Cloud 的描述（转述） |
| --- | --- |
| GPT-6 Astra | 面向编码、computer use、专业任务和科研等高要求工作 |
| GPT-6.1 Sol | 接近 Astra 的能力、更低成本，适合 agentic 编码、computer use 和专业工作 |
| GPT-6 Luna | 快速、成本低，适合大规模日常任务 |

博文还说「更多模型即将推出」，但没有列出具体名单。

和 Codex 直接相关的是 Google 博文 Getting started 里的这句话（原文）：

> Starting today, customers can build with these models through our APIs and connect their local Codex CLI and Desktop workflows directly to our Gemini platform for inference.

也就是说，获得预览资格的客户，可以通过 Google Cloud 的 API 使用这些模型，并把本地的 Codex CLI 和桌面端工作流接到 Google 的 Gemini 平台上做推理。

## 和直接用 OpenAI 有什么不同

| 维度 | 通过 Google Cloud Model Garden | 直接用 ChatGPT 账号或 OpenAI API |
| --- | --- | --- |
| 购买方式 | 通过 Google Cloud Marketplace 交易 | 向 OpenAI 购买套餐或 API 用量 |
| 账单 | 出现在同一张 Google Cloud 发票上 | OpenAI 账单 |
| 承诺消费 | 可抵扣已有的 GCP 承诺消费；Google 称还会计入跨模型厂商的 Flexible Savings Plans（FSP） | 不涉及 GCP |
| 推理位置 | Google 称 OpenAI 模型运行在专用的 Google Cloud 基础设施上 | OpenAI 侧 |
| 治理 | 沿用 Google Cloud 的访问控制、审计和 VPC Service Controls（见下节） | 沿用 OpenAI 的组织与工作区设置 |

## 谁现在能用

- **阶段**：Google 博文写的是「rolling out now in private preview to select enterprise customers」，即正在向部分企业客户私有预览。
- **怎么申请**：两篇公告都给了表单入口。OpenAI 博文末尾是 Request access，Google 博文是 express interest 表单。提交表单不等于开通。
- **正式开放**：OpenAI 写的是「General availability is planned in the coming weeks」，没有具体日期。

两篇公告提到的对象都是企业客户，没有提个人开发者的申请途径。

## 本地 Codex 接到 GCP：目前公开到哪一步

这是大家最关心的部分，也是公开信息最少的部分。

已经确定的：

- Google 明确说，客户可以把**本地 Codex CLI 和 Desktop 工作流**接到 Gemini 平台做推理。

公告里**没有**的：

- 具体的 endpoint、认证方式、Codex 配置字段或命令；
- 支持的区域列表；
- 配额、速率限制、价格表；
- Codex 里的哪些功能（例如云端任务、插件）在这种接法下可用。

所以本文不提供配置步骤。拿到预览资格的团队，请以 Google Cloud 或 OpenAI 发来的接入文档为准。如果你在做内部评估，建议把以下几项记下来，方便 GA 时对照：

1. 获批邮件或文档里给出的接入方式和版本要求；
2. 实际可用的模型和区域；
3. 账单在 GCP 里显示在哪个项目、哪个 SKU 下；
4. 和你现在直接用 OpenAI 登录时相比，哪些 Codex 功能表现不同。

## 企业治理：Google 的承诺

以下内容转述自 Google Cloud 博文，标注「即将」的表示公告时尚未提供：

- **数据边界**：客户的提示、上下文和输出留在客户指定的数据边界内，不会用于训练基础模型；Zero Data Retention（ZDR）选项**即将提供**。
- **隔离访问**：OpenAI 模型运行在专用的 Google Cloud 基础设施上，Confidential Compute **即将提供**；所有请求经过加固、隔离的网关，数据传输留在 Google Cloud 环境内。
- **审计与身份**：每个 agent 和模型交互都在已认证的身份下运行，管理员能获得端到端可见性、VPC Service Controls 保护和统一审计日志。

ZDR 和 Confidential Compute 都还没上线。如果合规要求依赖这两项，现在先别做上线决定。

## 其他官方表述

- OpenAI 说，OpenAI 模型**即将**进入 Google Antigravity 和 Gemini Agent；Google 博文也提到即将进入 Gemini for business 和 Google Antigravity。
- OpenAI 博文最后一句：Microsoft 仍是 OpenAI 的主要云合作伙伴。

## 本文不承诺的事

- 预览期的接入方式、区域、配额和价格，以获批后的官方文档为准；
- GA 时间以官方公告为准，「未来几周」不是承诺日期；
- 本站没有预览资格，文中没有任何实测内容。GA 后会更新本文。

## 相关阅读

- [App、CLI、IDE 和 Cloud 怎么选](https://codexguide.io/guides/app-cli-ide-he-cloud-zen-me-xuan)
- [Codex 模型和推理强度怎么选](https://codexguide.io/guides/codex-model-reasoning-effort)
- [Codex 常用功能清单](./11-Codex常用功能清单.md)

## 参考

- [OpenAI：OpenAI models are coming to Google Cloud](https://openai.com/index/openai-models-google-cloud/)
- [Google Cloud：Google Cloud brings OpenAI models to customers](https://cloud.google.com/blog/products/ai-machine-learning/google-cloud-brings-openai-models-to-customers)
