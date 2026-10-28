---
id: codex-google-cloud-model-garden
title: Codex 接入 Google Cloud Vertex AI（2026-10 更新）：0.165.0 内置 gcp provider，项目、区域、gcloud 凭证怎么配
seo_title: Codex 接入 Google Cloud Vertex AI：model_provider gcp 配置、模型与报错
description: Codex CLI 0.165.0 起内置 Google Cloud Vertex AI provider。本文讲清 model_provider = "gcp" 怎么配、项目和区域怎么设、gcloud 凭证怎么准备、能用哪些模型、常见报错，并保留 Model Garden 预览、计费与治理的官方说明。
lede: 0.165.0 以后，本地 Codex 接 Google Cloud 不用再等文档：设好项目 ID、登录 gcloud，再写一行 model_provider = "gcp"。
url: /guides/codex-google-cloud-model-garden
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 13
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-23
date_modified: 2026-10-28
verified_on: 2026-10-28
tested_cli_version: 0.165.0
models: [gpt-6-astra, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna]
official_ref: https://github.com/openai/codex/releases/tag/rust-v0.165.0
keywords: [Codex Vertex AI, Codex Google Cloud, model_provider gcp, GOOGLE_CLOUD_PROJECT, Codex CLI GCP, Model Garden]
related: [codex-model-reasoning-effort, codex-amazon-bedrock, codex-custom-model-provider]
howto: true
faq:
  - q: 本地 Codex CLI 要怎么配才能走 Google Cloud？
    a: 需要 Codex CLI 0.165.0 或更高版本。先用 gcloud auth application-default login 登录，设置环境变量 GOOGLE_CLOUD_PROJECT（区域 GOOGLE_CLOUD_LOCATION 可不设，默认 global），再在 ~/.codex/config.toml 里写 model_provider = "gcp"。不需要登录 OpenAI 账号。
  - q: 走 Google Cloud 能用哪些模型？
    a: 0.165.0 里 gcp provider 自带的模型列表是 gpt-6-astra、gpt-6.1-sol、gpt-6.1-terra、gpt-6-luna，默认 gpt-6.1-sol。你的项目实际开通了哪些，以 Google Cloud 控制台为准。
  - q: 哪些功能走 Google Cloud 时用不了？
    a: 0.165.0 源码里，gcp provider 关闭了推理摘要、图像生成和网页搜索。
  - q: 现在能自己在 GCP 控制台直接开通吗？
    a: 10-21 的公告写的是向部分企业客户私有预览，需要通过兴趣表单申请；截至 2026-10-28 没有看到正式开放（GA）的公告。Codex 侧的支持已经在 0.165.0 发布，但你的 GCP 项目要有可用的 OpenAI 模型才能真正调用。
  - q: 费用算在哪里？
    a: 通过 Google Cloud Marketplace 交易，出现在 Google Cloud 账单上，可抵扣已有的 GCP 承诺消费；Google 还说会计入跨模型厂商的 Flexible Savings Plans。
---

# Codex 接入 Google Cloud Vertex AI（2026-10 更新）：0.165.0 内置 gcp provider，项目、区域、gcloud 凭证怎么配

> 本文在线版：[codexguide.io/guides/codex-google-cloud-model-garden](https://codexguide.io/guides/codex-google-cloud-model-garden)

> 核对依据：Codex 侧的配置来自 [openai/codex rust-v0.165.0 Release](https://github.com/openai/codex/releases/tag/rust-v0.165.0)（2026-10-28 04:09 北京时间发布）、[PR #56265](https://github.com/openai/codex/pull/56265)、官方 [Changelog](https://learn.chatgpt.com/docs/changelog) 2026-10-27 条目和该版本源码；报错和模型列表在 Linux 上用 `codex-cli 0.165.0` 实测。Model Garden 的预览、计费和治理来自 OpenAI 博文《OpenAI models are coming to Google Cloud》与 Google Cloud 博文《Google Cloud brings OpenAI models to customers》（均发布于 2026-10-21）。**测试机没有 GCP 项目和 gcloud，所以没有跑通真实推理**，文中只写实际看到的输出。核对日期 2026-10-28（北京时间）。

## 更新说明（2026-10-28）

这篇 10-23 首发时，两篇公告都没给 Codex 的配置方法，原文写的是「不猜测，GA 后更新」。10-28 发布的 Codex CLI **0.165.0** 直接内置了 Google Cloud Vertex AI provider（`model_provider = "gcp"`），所以本文补上配置步骤、可用模型、限制和实测报错。原有的预览、计费和治理部分保留。

截至 2026-10-28，OpenAI 官方文档站还没有单独的 Vertex AI 配置页（Amazon Bedrock 有）。下面的配置项来自 Release 说明和源码，官方文档上线后以文档为准。

## 先看结论

- **版本**：Codex CLI 0.165.0 或更高。
- **三步**：`gcloud auth application-default login` → 设 `GOOGLE_CLOUD_PROJECT` → config.toml 写 `model_provider = "gcp"`。
- **不用登录 OpenAI 账号**：凭证走 Google Cloud 的 Application Default Credentials（ADC）。
- **模型**：自带 4 个，GPT-6 Astra、GPT-6.1 Sol（默认）、GPT-6.1 Terra、GPT-6 Luna。
- **限制**：推理摘要、图像生成、网页搜索不可用。
- **前提**：你的 GCP 项目要能用 Model Garden 里的 OpenAI 模型；目前是企业私有预览。

## 配置三步

### 第一步：准备 gcloud 凭证

安装 Google Cloud CLI 后运行：

```bash
gcloud auth application-default login
```

Codex 默认通过下面这条命令拿访问令牌（0.165.0 源码；Windows 上是 `gcloud.cmd`），超时 30 秒，大约每 50 分钟主动刷新一次：

```bash
gcloud auth application-default print-access-token
```

可以先手动跑一次，能打印出令牌说明凭证没问题。

### 第二步：设置项目和区域

```bash
export GOOGLE_CLOUD_PROJECT="你的项目 ID"
export GOOGLE_CLOUD_LOCATION="global"   # 可不设，默认就是 global
```

Codex 用这两个值拼出请求地址：

```text
https://aiplatform.googleapis.com/v1/projects/{GOOGLE_CLOUD_PROJECT}/locations/{GOOGLE_CLOUD_LOCATION}/publishers/openai/v1
```

两个值都只能包含英文字母、数字和连字符。

### 第三步：在 config.toml 里切换 provider

```toml
# ~/.codex/config.toml
model_provider = "gcp"
# model = "gpt-6.1-sol"   # 不写就是 gpt-6.1-sol
```

只想临时试一次：

```bash
codex -c model_provider=gcp
```

启动后 `codex exec` 的摘要里会显示 `provider: gcp`（0.165.0 实测）：

```text
OpenAI Codex v0.165.0
--------
model: gpt-6.1-sol
provider: gcp
```

## 能用的模型和不能用的功能

在 0.165.0 里设 `model_provider = "gcp"` 后，运行 `codex debug models`，模型列表只剩这 4 个：

| 模型 | 内置说明（原文） | 默认推理强度 |
|---|---|---|
| `gpt-6-astra` | Frontier intelligence for the most demanding work. | low |
| `gpt-6.1-sol`（默认） | Latest workhorse model for coding and everyday work. | low |
| `gpt-6.1-terra` | GPT-6.1 Terra Codex model. | low |
| `gpt-6-luna` | Fast and affordable model for easier tasks. | medium |

10-21 的 Google 博文首批只列了 Astra、Sol、Luna 三个；0.165.0 的内置列表多了 Terra。你的项目里实际能调用哪些，以 Google Cloud 控制台为准。各模型怎么选，见 [Codex 模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

0.165.0 源码里 gcp provider 的能力设置：

| 功能 | 走 Google Cloud 时 |
|---|---|
| 推理摘要（reasoning summaries） | 不可用 |
| 图像生成 | 不可用 |
| 网页搜索 | 不可用 |
| 远程上下文压缩 | 可用 |
| OpenAI 账号登录 | 不需要 |

另外，源码里自动审批审核（approval review）和 Memories 提取默认用 `gpt-6-luna`，Memories 整理用 `gpt-6.1-terra`。

## 常见报错（0.165.0 实测）

测试机没有 gcloud 和 GCP 项目，以下是真实看到的输出。

**没设项目 ID：**

```text
ERROR: Missing environment variable: `GOOGLE_CLOUD_PROJECT`. Set GOOGLE_CLOUD_PROJECT to your Google Cloud project ID, or configure model_providers.gcp.base_url.
```

处理：`export GOOGLE_CLOUD_PROJECT=...`，或者在配置里直接写 `base_url`（见下一节）。

**没装 gcloud，或凭证过期：**

```text
ERROR codex_login::auth::manager: Failed to resolve external auth: provider auth command `gcloud` failed to start: No such file or directory (os error 2)
ERROR: Google Cloud credentials are unavailable or expired. Run `gcloud auth application-default login` to reauthenticate.
```

处理：装好 Google Cloud CLI 并确认 `gcloud` 在 PATH 里，再运行 `gcloud auth application-default login`。

**区域写错（例如中间带空格）：**

```text
ERROR: GOOGLE_CLOUD_LOCATION must contain only ASCII letters, digits, and hyphens
```

**改了不支持的字段（例如给 gcp 加 `env_key`）：**

```text
Error: model_providers.gcp only supports changing `base_url`, `auth`, and `http_headers`; other non-default provider fields are not supported
```

## 可以改哪些字段

内置的 `gcp` provider 只允许在 `[model_providers.gcp]` 下改三项：

| 字段 | 用途 |
|---|---|
| `base_url` | 直接指定完整地址，例如走公司网关；设了就不再读 `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` |
| `auth` | 换一个取令牌的命令（`command`、`args`、`timeout_ms`、`refresh_interval_ms`、`cwd`） |
| `http_headers` | 额外的固定请求头 |

例子（用服务账号模拟取令牌，仅示意写法）：

```toml
model_provider = "gcp"

[model_providers.gcp.auth]
command = "gcloud"
args = ["auth", "print-access-token", "--impersonate-service-account=codex@你的项目.iam.gserviceaccount.com"]
```

改其他字段会报上一节最后那条错。因为 `gcp` 这个名字已被内置 provider 占用，自己的自定义 provider 请换个名字。

## Model Garden：公告说了什么

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
- **正式开放**：OpenAI 写的是「General availability is planned in the coming weeks」，没有具体日期。截至 2026-10-28 没有看到 GA 公告。

两篇公告提到的对象都是企业客户，没有提个人开发者的申请途径。

## 企业治理：Google 的承诺

以下内容转述自 Google Cloud 博文，标注「即将」的表示公告时尚未提供：

- **数据边界**：客户的提示、上下文和输出留在客户指定的数据边界内，不会用于训练基础模型；Zero Data Retention（ZDR）选项**即将提供**。
- **隔离访问**：OpenAI 模型运行在专用的 Google Cloud 基础设施上，Confidential Compute **即将提供**；所有请求经过加固、隔离的网关，数据传输留在 Google Cloud 环境内。
- **审计与身份**：每个 agent 和模型交互都在已认证的身份下运行，管理员能获得端到端可见性、VPC Service Controls 保护和统一审计日志。

ZDR 和 Confidential Compute 都还没上线。如果合规要求依赖这两项，现在先别做上线决定。

## 其他官方表述

- OpenAI 说，OpenAI 模型**即将**进入 Google Antigravity 和 Gemini Agent；Google 博文也提到即将进入 Gemini for business 和 Google Antigravity。
- OpenAI 博文最后一句：Microsoft 仍是 OpenAI 的主要云合作伙伴。

## 和 Amazon Bedrock、自定义 provider 的区别

| | Google Cloud（`gcp`） | Amazon Bedrock（`amazon-bedrock`） | 自定义 provider |
|---|---|---|---|
| 怎么开 | `model_provider = "gcp"` | `model_provider = "amazon-bedrock"` | 自己写 `[model_providers.<id>]` |
| 凭证 | gcloud ADC | AWS 凭证链 / profile | `env_key` 或 `auth` 命令 |
| 官方文档页 | 截至 10-28 还没有 | 有 | 有 |
| 能改的字段 | `base_url`、`auth`、`http_headers` | `base_url`、`auth`、`aws`、`http_headers` | 全部 |

详见 [接入 Amazon Bedrock](./16-Codex接入Amazon-Bedrock-登录向导与配置.md) 和 [自定义模型提供商](../10-配置模型与权限安全/13-Codex自定义模型提供商-model_providers与openai_base_url.md)。

## 本文不承诺的事

- 预览期的区域、配额和价格，以 Google Cloud 控制台和获批后的官方文档为准；
- GA 时间以官方公告为准；
- 本站没有 GCP 预览资格，没有跑通真实推理。上面的报错和模型列表是在没有 GCP 项目的机器上实测的；官方 Vertex AI 文档上线后会再核对本文。

## 相关阅读

- [App、CLI、IDE 和 Cloud 怎么选](https://codexguide.io/guides/app-cli-ide-he-cloud-zen-me-xuan)
- [Codex config.toml 常用字段速查](../16-图解与速查/02-Codex-config.toml常用字段与环境变量速查.md)
- [config.toml 深入配置：字段覆盖关系与排查方法](https://codexguide.io/advanced/config-toml)
- [Codex 常用功能清单](./11-Codex常用功能清单.md)

## 参考

- [openai/codex rust-v0.165.0 Release](https://github.com/openai/codex/releases/tag/rust-v0.165.0)、[PR #56265](https://github.com/openai/codex/pull/56265)
- [OpenAI Codex Changelog](https://learn.chatgpt.com/docs/changelog)
- [OpenAI：OpenAI models are coming to Google Cloud](https://openai.com/index/openai-models-google-cloud/)
- [Google Cloud：Google Cloud brings OpenAI models to customers](https://cloud.google.com/blog/products/ai-machine-learning/google-cloud-brings-openai-models-to-customers)
