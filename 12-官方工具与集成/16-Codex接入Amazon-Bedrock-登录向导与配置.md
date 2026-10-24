---
id: codex-amazon-bedrock
title: Codex 接入 Amazon Bedrock：CLI 登录向导、Runtime 与 Mantle 怎么选，以及 API Key 和 AWS 凭证怎么配
seo_title: Codex 接入 Amazon Bedrock：登录向导、Runtime/Mantle 与凭证配置
description: Codex CLI 0.164.0 起默认在登录页提供 Amazon Bedrock 选项。本文按官方文档和实测，讲清 Runtime 与 Mantle 两种 provider 的区别、API Key 和 AWS SDK 凭证怎么配、桌面端读取 .env、怎么验证路由，以及 Bedrock 下哪些功能不可用。
url: /guides/codex-amazon-bedrock
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 16
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-24
date_modified: 2026-10-24
verified_on: 2026-10-24
tested_cli_version: 0.164.0
models: [gpt-6-astra, gpt-6-sol, gpt-6-luna, gpt-6.1-sol]
official_ref: https://learn.chatgpt.com/docs/amazon-bedrock
keywords: [Codex Amazon Bedrock, amazon-bedrock-runtime, Bedrock Mantle, AWS_BEARER_TOKEN_BEDROCK, Codex Bedrock 登录]
related: [config-toml-guide, codex-model-reasoning-effort]
howto: false
faq:
  - q: 用 Bedrock 时还需要 ChatGPT 登录或 OPENAI_API_KEY 吗？
    a: 不需要。官方文档写明 Bedrock provider 使用 AWS 原生认证，即 Bedrock API Key 或 AWS IAM 凭证，不使用 ChatGPT 登录或 OPENAI_API_KEY。
  - q: amazon-bedrock 和 amazon-bedrock-runtime 有什么区别？
    a: amazon-bedrock 走 Bedrock Mantle 端点，是同区域推理，支持托管网页搜索；amazon-bedrock-runtime 走 Bedrock Runtime 端点，支持跨区域推理（CRIS），不支持托管网页搜索。官方建议新配置用 Runtime。
  - q: Bedrock 下能用 Fast 模式吗？
    a: 不能。官方文档写明 Fast 模式依赖优先处理，而 Bedrock 首期只支持按需推理。
---

# Codex 接入 Amazon Bedrock：CLI 登录向导、Runtime 与 Mantle 怎么选，以及 API Key 和 AWS 凭证怎么配

> 本文在线版：[codexguide.io/guides/codex-amazon-bedrock](https://codexguide.io/guides/codex-amazon-bedrock)

> 核对依据：OpenAI 官方文档 [Use ChatGPT Work and Codex with Amazon Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock)、Codex CLI 0.164.0 [发布说明](https://github.com/openai/codex/releases/tag/rust-v0.164.0) 及相关 PR。实测环境是 Linux 上的 `codex-cli 0.164.0`，用独立的 `CODEX_HOME` 和**假的** API Key，只验证登录页、配置写入和 `/status` 显示，**没有真实的 AWS 账号，也没有发出成功的 Bedrock 请求**。核对日期 2026-10-24。

如果你的公司把模型访问统一放在 AWS 上，或者希望用 AWS 账号的权限和账单来管 Codex 的用量，可以让 Codex 直接调用 Amazon Bedrock 上的 OpenAI 模型。

这时请求不经过 OpenAI 托管的 Responses API：本地的 Codex 把请求发给 Bedrock，由 Bedrock 提供兼容 OpenAI 的 Responses API。认证也走 AWS：用 Bedrock API Key 或 AWS IAM 凭证，**不用** ChatGPT 登录，也不用 `OPENAI_API_KEY`。

如果你的公司已经有模型网关，官方建议按 [Use API/provider credentials](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) 接网关，而不是直连 Bedrock。

## 0.164.0 的变化：登录页默认出现 Bedrock

Codex CLI 0.164.0 把 Bedrock 登录向导（`bedrock_setup_wizard`）转为稳定功能并默认开启（[#56033](https://github.com/openai/codex/pull/56033)）。在没有登录过的环境里运行 `codex`，实测登录页出现第 4 个选项：

```text
  1. Sign in with ChatGPT
  2. Sign in with Device Code
  3. Provide your own API key
  4. Use Amazon Bedrock
     Connect using your AWS credentials
```

（前三项的说明文字这里省略了。）

不需要这个选项时，可以在 `config.toml` 里关掉：

```toml
[features]
bedrock_setup_wizard = false
```

另一个相关改动是 [#56023](https://github.com/openai/codex/pull/56023)：向导检测到 AWS profile 或环境变量里的凭证时，手动输入 Bedrock API Key 的入口会收进 “Other AWS sign-in methods”；没检测到凭证时，API Key 入口直接显示。

### 实测：向导做了什么

**没有任何 AWS 凭证时**，选 Use Amazon Bedrock 后，向导依次问 AWS profile 名称和 Region：

```text
Enter the name of your AWS profile.
Enter the AWS Region to use with Amazon Bedrock.
```

填了一个本机不存在的 profile，向导报错，没有写入配置：

```text
Unable to set up Amazon Bedrock: account/bedrock/setup failed: failed to load credentials for AWS profile `codex-bedrock`: …
```

**设置了 `AWS_BEARER_TOKEN_BEDROCK` 和 `AWS_REGION=us-east-2` 后**（Key 是随便填的），向导完成配置，`config.toml` 里写入了：

```toml
model_provider = "amazon-bedrock"

[model_providers.amazon-bedrock.aws]
region = "us-east-2"
```

注意这里写的是 `amazon-bedrock`，也就是下文的 **Mantle**，而官方文档建议新配置用 **Runtime**（`amazon-bedrock-runtime`）。用向导完成后，请按下一节决定要不要改 provider。

启动时还看到一行提示：`Running without the shared background server: Bedrock sign-in requires embedded mode.` 字面意思是 Bedrock 登录需要嵌入模式，所以这次没有使用共享的后台服务。本文实测没有发现它影响 `/status` 和配置显示，但没有真实 AWS 账号，未验证对实际请求的影响。

## Runtime 和 Mantle 怎么选

Bedrock 上有两个端点，对应 Codex 里两个内置 provider：

| | Bedrock Runtime | Bedrock Mantle |
| --- | --- | --- |
| `model_provider` | `amazon-bedrock-runtime` | `amazon-bedrock` |
| 推理方式 | 跨区域推理（Global / Geo CRIS） | 同区域推理 |
| 端点 | `https://bedrock-runtime.{region}.amazonaws.com/openai/v1` | `https://bedrock-mantle.{region}.api.aws/openai/v1` |
| 托管网页搜索 | 不支持，需写 `web_search = "disabled"` | 支持，`web_search = "cached"` |
| 模型写法 | 推理配置文件 ID，如 `global.openai.gpt-6-sol` | 模型 ID，如 `openai.gpt-6-sol` |
| 官方建议 | **新配置用这个** | 需要托管网页搜索时用 |

Runtime 配置：

```toml
model_provider = "amazon-bedrock-runtime"
web_search = "disabled"
```

Mantle 配置：

```toml
model_provider = "amazon-bedrock"
web_search = "cached"
```

ChatGPT 桌面端、Codex CLI、IDE 扩展和 SDK 读取同一套本地配置，所以在 `~/.codex/config.toml` 里改一次就行。

### 选模型

`model` 可以不写，内置 provider 有自己的模型目录，`/model` 选择器会列出当前端点支持的模型。要写的话，官方文档列出的 ID 是：

| 模型 | Runtime Global CRIS | Runtime 美国 Geo CRIS | Mantle |
| --- | --- | --- | --- |
| GPT-6 Astra | `global.openai.gpt-6-astra` | `us.openai.gpt-6-astra` | `openai.gpt-6-astra` |
| GPT-6 Sol | `global.openai.gpt-6-sol` | `us.openai.gpt-6-sol` | `openai.gpt-6-sol` |
| GPT-6 Luna | `global.openai.gpt-6-luna` | `us.openai.gpt-6-luna` | `openai.gpt-6-luna` |

几点要注意：

- 切换端点时，provider 和显式写的 `model` 要一起改，Runtime 的 ID 和 Mantle 的 ID 不通用。
- 文档写明 GPT-6 Sol 和 Luna 在 Mantle 上只在 `us-east-1`（弗吉尼亚北部）可用；其他组合以 AWS 的 [Regional availability by models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html#model-regions-openai) 为准。
- 通过 Runtime 用 GPT-6 Sol 时，还需要账号默认 project 上的 `bedrock:InvokeModel` 权限，见 AWS 的 [GPT-6 Sol 说明](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-sol.html)。

**实测和文档不一致的地方**：0.164.0 在不写 `model` 时，`/status` 显示的默认模型是 GPT-6.1 Sol（Mantle 下为 `openai.gpt-6.1-sol`，Runtime 下为 `global.openai.gpt-6.1-sol`），这个 ID 不在上表里。因为实测没有真实 AWS 账号，无法确认它在你的 Region 和账号里能否调用。稳妥的做法是在 `config.toml` 里显式写上表中的 ID，或在 `/model` 里选一个你账号确认可用的模型。

## 认证：API Key 还是 AWS SDK 凭证

Codex 按这个顺序查找凭证：

1. Bedrock API Key；
2. AWS SDK 凭证链。

### 方式一：Bedrock API Key

用 API Key 时**必须**同时指定 Region：

```shell
export AWS_BEARER_TOKEN_BEDROCK=<你的 Bedrock API Key>
export AWS_REGION=us-east-2
```

Windows PowerShell：

```powershell
$env:AWS_BEARER_TOKEN_BEDROCK = "<你的 Bedrock API Key>"
$env:AWS_REGION = "us-east-2"
```

### 方式二：AWS SDK 凭证

公司用 AWS SDK 凭证链管理 Bedrock 访问时用这种方式。支持的来源：

| 来源 | 怎么配 |
| --- | --- |
| 共享配置文件 | `aws configure` |
| 环境变量 | `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN` |
| 控制台登录凭证 | `aws login` |
| SSO 或命名 profile | `aws sso login --profile codex-bedrock`，再 `export AWS_PROFILE=codex-bedrock` |
| 联合身份（企业 SSO / OIDC） | 在 AWS profile 里配置 `credential_process`，浏览器登录、换 token、缓存和刷新都交给这个辅助程序 |

**容易踩的坑**：API Key 排在前面。如果环境里残留了一个过期或不该用的 `AWS_BEARER_TOKEN_BEDROCK`，Codex 会优先用它，你配好的 profile 就不会生效。想用 profile 时，先 `unset AWS_BEARER_TOKEN_BEDROCK`。

### 桌面端和 IDE 扩展：写进 .env

桌面端和 IDE 扩展不一定继承终端里的环境变量。把需要的变量写进 `~/.codex/.env`（Windows 默认是 `%USERPROFILE%\.codex\.env`），然后**重启**应用或扩展：

```shell
export AWS_BEARER_TOKEN_BEDROCK=<你的 Bedrock API Key>
export AWS_REGION=us-east-2
```

`.env` 里是明文密钥，不要提交到任何仓库，也不要放进项目目录。

## 怎么确认请求真的走了 Bedrock

1. CLI 里运行 `/status`，看 Model provider 一行。Mantle 显示 `amazon-bedrock`，Runtime 显示 `amazon-bedrock-runtime`。实测（Mantle）：

   ```text
   Model provider:      amazon-bedrock
   ```

2. 桌面端：重启后选 Work 或 Codex，新建任务。IDE 扩展：重启后新建会话。
3. 在新任务里发一句：

   ```text
   Reply with exactly: bedrock-ok
   ```

   正常应回复 `bedrock-ok`。官方提醒，**光看回复不能判断走的是哪条路由**，要结合客户端里显示的 provider 和模型一起确认。

团队推广前，官方建议用一个可丢弃的目录、只读权限，跑一个无害的本地工具任务和一次追问，确认整条链路正常。

## 哪些功能在 Bedrock 下不能用

Bedrock 配置支持本地的 Codex 工作流，依赖 OpenAI 云服务的功能不可用。按官方的功能表整理：

**可用**：Codex CLI、桌面端里的 Codex 和 Work、IDE 扩展、SDK 和 `codex exec`；本地 `/review`、审批 Auto-review、沙箱和权限控制、定时任务、worktree 和内置 Git 工具；AGENTS.md、Skills、MCP、Subagents；SSH 远程连接；`requirements.toml` 托管配置。

**部分可用**：Plugins（不需要 ChatGPT 认证的本地插件和 OpenAI 精选插件可用）、Memories、Computer Use、Chrome 浏览器控制。

**不可用**：Fast 模式、图像生成和编辑、语音输入、Runtime 上的托管网页搜索；Codex cloud 和网页版 ChatGPT Work；Connectors、插件共享、Sites、手机远程控制；`@codex` GitHub 委派和 GitHub PR 自动审查、Slack 和 Linear 云集成；云端托管策略、分析面板和 Analytics API、Compliance API 等企业管理功能。

Fast 模式不可用的原因，官方写的是：Fast 依赖优先处理，而 Bedrock 首期只支持按需推理。

Codex Security CLI 有自己的 provider 配置，要按它的 [Amazon Bedrock 设置](https://learn.chatgpt.com/docs/security/cli/reference) 单独配，不读上面这些设置。

## 排查清单

设置失败时，按官方清单逐项检查：

- 模型 ID 和支持列表完全一致；
- provider 和端点对应：Runtime 用 `amazon-bedrock-runtime`，Mantle 用 `amazon-bedrock`；
- Region 里有这个模型；
- API Key 或 AWS 凭证有效、没过期；
- AWS 身份有调用该模型的权限；
- `AWS_BEARER_TOKEN_BEDROCK` 不是过期或误设的 Key；
- 桌面端和 IDE：变量写在 `~/.codex/.env` 里，并且重启过。

用 profile 认证时，可以先确认 AWS 身份：

```shell
aws sts get-caller-identity --profile codex-bedrock
```

把 `codex-bedrock` 换成你的 profile 名；用默认凭证链时去掉 `--profile`。这条命令只能确认“你是谁”，**不能**确认你有没有调用 Bedrock 模型的权限。

**找谁支持**：Codex 客户端的安装、配置和本地行为找 OpenAI Support；AWS 凭证、IAM 权限、模型访问、配额、账单、Region、Bedrock 请求失败等问题找公司的 AWS 管理员或 AWS Support。

## 相关阅读

- [Codex config.toml 配置指南](../10-配置模型与权限安全/08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)：provider、`-c` 临时覆盖和配置层级。
- [Codex 模型和推理强度怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [App、CLI、IDE 和 Cloud 怎么选](../00-从这里开始/05-App-CLI-IDE和Cloud怎么选.md)：Bedrock 下 Cloud 不可用，先确认入口。

## 参考资料

- [Use ChatGPT Work and Codex with Amazon Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock)
- [Codex CLI 0.164.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.164.0)
- [#56033 Enable the Bedrock setup wizard by default](https://github.com/openai/codex/pull/56033)
- [#56023 Group Bedrock API key entry with other AWS sign-in methods](https://github.com/openai/codex/pull/56023)
- [AWS：Regional availability by models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html#model-regions-openai)
