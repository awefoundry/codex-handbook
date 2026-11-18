---
id: codex-custom-model-provider
title: Codex 自定义模型提供商（2026-11 更新）：在终端里添加供应商，登录时用设备码对接网关
seo_title: Codex 自定义模型提供商：model_providers 与 openai_base_url 配置
description: 想让 Codex 走公司网关、代理或第三方模型服务，除了在 config.toml 写 model_providers 或 openai_base_url，现在也可以在终端里添加、编辑供应商，并在 SSH 场景使用设备码。本文按 0.169.0 更新操作入口，并保留请求路径、鉴权头和保留 ID 的说明。
lede: 只改内置 OpenAI 的地址用 openai_base_url。独立服务用自己的 provider ID。0.168 起可以在 Sessions 里为新对话选默认供应商。
url: /guides/codex-custom-model-provider
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, IDE, App]
difficulty: 进阶
order: 13
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-25
date_modified: 2026-11-14
verified_on: 2026-11-14
tested_cli_version: 0.169.0
official_ref: https://learn.chatgpt.com/docs/config-file/config-advanced
keywords: [Codex model_providers, Codex 自定义模型, openai_base_url, Codex 代理, Codex 网关, env_key, wire_api, gateway_setup_wizard]
related: [config-toml-guide, model-reasoning-effort, codex-amazon-bedrock, codex-google-cloud-model-garden, deng-lu-codex]
howto: true
faq:
  - q: 只想让 Codex 走代理或数据驻留地址，需要新建 provider 吗？
    a: 不需要新建。官方建议直接在用户级 config.toml 里设置 openai_base_url，它只改内置 openai provider 的基础地址。
  - q: 能不能写 [model_providers.openai] 覆盖内置的 openai？
    a: 不能。配置参考仍把 openai、ollama、lmstudio 列为不能覆盖的内置 ID。0.169.0 实测这三个 ID 会拒绝加载配置，并提示改名，例如 openai-custom。
  - q: 第三方服务只有 Chat Completions 接口，能接 Codex 吗？
    a: 配置参考里 wire_api 只支持 responses，也是默认值。0.169.0 实测请求发往 base_url 后面的 /responses。服务端需要兼容 Responses 接口。
  - q: 把 model_provider 写进项目里的 .codex/config.toml 会生效吗？
    a: 不会。0.169.0 在已经 --trust 的仓库里仍会提示 Ignored unsupported project-local config keys，provider 保持用户级的值。未信任的仓库则连项目配置一起不加载。
---

# Codex 自定义模型提供商（2026-11 更新）：在终端里添加供应商，登录时用设备码对接网关

> 本文在线版：[codexguide.io/guides/codex-custom-model-provider](https://codexguide.io/guides/codex-custom-model-provider)

> 核对依据：OpenAI 文档 [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)、[Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) 和 [Authentication](https://learn.chatgpt.com/docs/auth)，以及 GitHub Release [rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)、[rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)。请求路径于 2026-11-14 在 Linux 上的 `codex-cli 0.169.0` 复测：每个场景使用独立的 `CODEX_HOME`，模型服务是本机 `127.0.0.1:18081` 上的模拟服务器，它只记录方法、路径和请求头，然后固定返回 401。测试 Key 是假的，没有跑出模型回复。终端里的 Sessions 菜单、添加供应商和网关设备码没有打开。旧链 `sign-in-with-chatgpt-through-a-gateway` 在同一天返回 404，现行入口是 Connect to a gateway。

公司有统一的模型网关，或要走某个代理、某个区域的接口时，Codex 需要知道请求发到哪、用哪一种凭证。0.164 一文只写了 `config.toml`。0.168 和 0.169 增加了终端里的浏览、选择、添加和编辑。配置文件仍然是这些界面背后的那一份用户级配置。

Bedrock 见 [接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)。Vertex AI 见 [接入 Google Cloud Vertex AI](../12-官方工具与集成/13-Codex接入Google-Cloud-Model-Garden.md)。ChatGPT 登录和 `codex login --device-auth` 见 [登录 Codex](../01-安装与首次使用/07-登录Codex.md)。

## 先判断：你需要哪一种

| 你的情况 | 用什么 |
| --- | --- |
| 公司提供了模型网关，并有接入说明 | 按 [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway) 配置；组织级推广见 Roll out a gateway |
| 只是让内置 OpenAI 走代理、路由器或数据驻留地址 | 用户级 `openai_base_url` |
| 接一个独立的模型服务，用它自己的 Key | `[model_providers.<id>]`，ID 不要用保留名 |
| 已有 provider，只想让新对话改用其中某一个 | 0.168 的 Sessions → Model providers |
| 要在终端里新增或修改 provider，或在登录时创建 | 0.169 的终端编辑；自定义网关引导需另行开启 |
| 本机跑 Ollama 或 LM Studio | `--oss` |
| Amazon Bedrock 或 Vertex AI | 内置 provider，见文末专文 |

0.168 还有一条行为要先记住：已经打开或恢复的对话，在你更改「新对话的默认供应商」之后，仍使用自己保存的供应商。改默认值不会把旧会话一起换掉。

## 在终端里浏览和选择默认供应商

0.168.0 的 Release 写明：在 **Sessions → Model providers** 浏览供应商，并为新对话选择默认供应商。本文使用的是 Linux，没有进入交互式 TUI，没有看到这个菜单，也没有截图。菜单名以 Release 的英文为准。

选择结果对应的仍是用户级配置里的 `model_provider`。项目目录里的 `.codex/config.toml` 不能承担这份选择，见下文「写在项目配置里不生效」。

## 在终端添加或编辑供应商

0.169.0 的 Release 写明：可以在终端添加或编辑自定义模型供应商。开启自定义网关引导之后，可以在登录时创建供应商。

Release 没有写出添加供应商的斜杠命令，也没有写出「自定义网关引导」的配置键名。0.169.0 的 `codex features list` 里有 `gateway_setup_wizard`，阶段是 stable，未写入配置时有效状态是 false。Release 没有把这个标志写成 custom gateway onboarding。本文没有执行 `codex features enable gateway_setup_wizard`，没有登录，没有真实网关，因此没有验证打开它之后屏幕上会出现什么。

已经用配置文件接好的 provider 不依赖这个引导。引导是登录过程中的另一条入口。app-server 文档在 0.169 的 Documentation 里还写了：客户端可以列出模型，或为已配置的供应商授权网关，同时不改变默认供应商。本文没有调用 app-server。

## SSH 或没有浏览器时的设备码

这里有三条不同的登录，不要合成一步。

**ChatGPT 账号的设备码**：Authentication 仍把设备码标为 beta。交互界面里选择 Sign in with Device Code，或运行 `codex login --device-auth`。使用前要在个人安全设置或工作区权限里开启设备码登录。0.169.0 的 `codex login --help` 列出了 `--device-auth`，这一行的说明文字是空的。本文没有完成这次登录。细节见 [登录 Codex](../01-安装与首次使用/07-登录Codex.md)。

**0.169 发布说明里的网关设备码**：开启自定义网关引导后，可以在 SSH 或没有本地浏览器时，对支持的网关使用设备码。Release 没有列出哪些网关算 supported，也没有给出设备码的命令行。本文没有网关，没有走这条流程。

**现行网关文档里的 native gateway OAuth**：Connect to a gateway 写的是浏览器登录。它要求浏览器和能够到达的 loopback 回调，并写明没有 device-code fallback。CLI 在 SSH 上时，文档要求在 OAuth 表里设置 `redirect_port`（示例 `43127`），登记对应的 `http://127.0.0.1:43127/callback`，再从有浏览器的机器做本地转发：

```bash
ssh -L 43127:127.0.0.1:43127 user@remote
```

文档接着说：在那个 SSH 会话里启动 `codex`，用本地浏览器打开网关登录 URL。回调无法从浏览器到达时，改用 API Key 或 credential helper。

发布说明中的「支持的网关可以使用设备码」和网关文档中的「native gateway OAuth 没有 device-code fallback」使用的不是同一套措辞。以你的网关管理员给出的认证方式为准。本文没有用端口转发或设备码连上任何网关。

网关 OAuth 的配置表是 `[model_providers.<id>.gateway_oauth]`，字段包括授权 URL、token URL、公开的 client ID，以及可选的 scopes、resource、`redirect_port` 和 `delivery`。它可以在 `requires_openai_auth = false` 时单独使用。`delivery` 用来把令牌放进网关要求的 cookie 或自定义头。完整字段和「同时要 ChatGPT 登录」时怎样把 `Authorization` 留给 OpenAI 凭证，以 Connect to a gateway 为准。0.166.0 及以后，仅网关认证时，CLI 默认把访问令牌放在 `Authorization: Bearer`。本文没有对 `gateway_oauth` 做请求复测。

## 写法一：openai_base_url，只改内置 OpenAI 的地址

Advanced Config 的原意：如果只是把内置的 OpenAI provider 指向 LLM 代理、路由器或开启了数据驻留的项目，直接设置 `openai_base_url`，不必新建 provider。

```toml
# ~/.codex/config.toml
openai_base_url = "https://us.api.openai.com/v1"
```

2026-11-14 把它指向模拟服务器，并指定文档示例里的模型名：

```toml
openai_base_url = "http://127.0.0.1:18081/v1"
model = "gpt-6.1-sol"
```

用假 Key 跑一次 `CODEX_API_KEY=sk-test-not-a-real-key codex exec --skip-git-repo-check "say hi"`。启动摘要里是 `provider: openai`、`model: gpt-6.1-sol`。模拟服务器记录到 7 次带 `Upgrade: websocket` 的 `GET /v1/responses`，然后是 6 次 `POST /v1/responses`。POST 的 `Authorization` 是 `Bearer` 加上假 Key 的前缀，请求体里 `model` 为 `gpt-6.1-sol`，`stream` 为 true。

终端先多次尝试 Responses WebSocket，打印 `Reconnecting... 2/5` 到 `5/5`，再提示 `Falling back from WebSockets to HTTPS transport`，随后 HTTP 也重试，最后报：

```text
ERROR: unexpected status 401 Unauthorized: mock server: request recorded, no model here, url: http://127.0.0.1:18081/v1/responses
```

这和 2026-10-25 在 0.164.0 上看到的顺序一致：地址要写到 `/v1` 这一层，因为客户端会在后面接 `/responses`；内置 OpenAI provider 会先尝试 WebSocket，失败后再走 HTTP POST。代理不支持 WebSocket 时，会先看到重连，再看到 POST。失败会重试，所以模拟服务器收到了多次请求。

## 写法二：model_providers，自定义一个 provider

接独立的模型服务时，在用户级 `config.toml` 里定义 provider，再用 `model_provider` 指向它。2026-11-14 复测用的配置：

```toml
model = "my-gateway-model"
model_provider = "mygateway"

[model_providers.mygateway]
name = "My Gateway"
base_url = "http://127.0.0.1:18081/v1"
env_key = "MYGATEWAY_API_KEY"
http_headers = { "X-Team" = "docs-test" }
request_max_retries = 0
stream_max_retries = 0
wire_api = "responses"
```

各字段的含义以配置参考为准：

| 字段 | 作用 |
| --- | --- |
| `name` | 显示名称 |
| `base_url` | API 基础地址 |
| `env_key` | 从哪个环境变量读 API Key |
| `env_key_instructions` | 可选，给使用者看的 Key 设置说明 |
| `wire_api` | 协议，只支持 `responses`，也是省略时的默认值 |
| `http_headers` | 固定加在请求上的头 |
| `env_http_headers` | 从环境变量取值的请求头，变量存在时才加 |
| `query_params` | 追加的查询参数，例如 Azure 的 `api-version` |
| `request_max_retries` | HTTP 重试次数，默认 4 |
| `stream_max_retries` | 流式中断重试次数，默认 5 |
| `stream_idle_timeout_ms` | 流空闲超时，默认 300000 毫秒 |
| `requires_openai_auth` | 是否使用 OpenAI 鉴权，默认 false |
| `experimental_bearer_token` | 直接写死的 Token；官方不推荐，建议用 `env_key` |
| `supports_standalone_web_search` | 是否声明兼容独立的网页搜索端点，自定义 provider 默认 false。声明为 true 也不会单独把它打开 |
| `model_catalog_url` | Codex 原生模型目录的完整 URL，可省略 |

两个重试次数设成 0，是为了让模拟服务器少收到重复请求。日常使用保持默认即可。

### 没设置环境变量时

```text
warning: Model metadata for `my-gateway-model` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
ERROR: Missing environment variable: `MYGATEWAY_API_KEY`.
```

模拟服务器没有收到请求。第一行表示 Codex 不认识这个模型名，只能用通用的默认参数。2026-11-14 这次运行里，缺少环境变量的 `ERROR` 打印了两遍。

### 设置环境变量后

```bash
MYGATEWAY_API_KEY=sk-test-not-a-real-key codex exec --skip-git-repo-check "say hi"
```

启动摘要里是 `provider: mygateway`、`model: my-gateway-model`。模拟服务器记录到一次请求：

```text
POST /v1/responses
Authorization: Bearer sk-tes…
X-Team: docs-test
Content-Type: application/json
model=my-gateway-model  stream=true
```

这次没有出现 WebSocket 的 `Upgrade` 请求。终端报上面的 401，退出码是 1，同一条 401 打印了两遍，模拟服务器日志里只有一条 POST。

可以确认的仍是这三件事：`env_key` 以 `Authorization: Bearer` 发出；`http_headers` 里的自定义头会带上；地址是 `base_url` 加上 `/responses`，请求体是流式 Responses。只提供 `/chat/completions` 的服务不能按这个写法接入。

## 需要动态 Token 时：用 auth 命令

网关的 Token 要定期刷新时，可以让 Codex 调用外部命令取 Token。示例来自 Advanced Config：

```toml
[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "https://proxy.example.com/v1"
wire_api = "responses"

[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

命令没有标准输入，必须把 Token 打印到标准输出。Codex 去掉首尾空白，空 Token 视为错误。它按 `refresh_interval_ms` 主动刷新；设成 0 则只在鉴权重试后刷新。配置参考写明：`auth` 不能和 `env_key`、`experimental_bearer_token`、`requires_openai_auth` 同时使用。本文没有运行外部取 Token 命令。

Connect to a gateway 还要求：同时使用 ChatGPT 登录时，不要用 `auth` 表去拿网关凭证；网关密钥改走自定义头，把 `Authorization` 留给 OpenAI 凭证。

## 三个仍然有效的限制

### 1. 不能覆盖的内置 ID，和只能改少数字段的内置表

Configuration Reference 的字段表写明：内置 provider ID `openai`、`ollama`、`lmstudio` 被保留，不能覆盖。0.169.0 对这三个 ID 各写了一份带 `name` 和 `base_url` 的表，都在加载配置时失败，原文是：

```text
Error loading config.toml: model_providers contains reserved built-in provider IDs: `openai`. Built-in providers cannot be overridden. Rename your custom provider (for example, `openai-custom`).
```

`ollama` 和 `lmstudio` 的句子相同，只是 ID 不同。只改 OpenAI 的地址时用 `openai_base_url`。

Advanced Config 的 Custom model providers 还把 `amazon-bedrock`、`amazon-bedrock-runtime` 和 `gcp` 写进保留 ID。0.169.0 对这三个 ID 的实测不是上面这句拒绝，而是：表可以存在，但只允许修改列出的字段。多写一个 `name` 时，`gcp` 的报错列出 `base_url`、`auth`、`http_headers`、`project_id`、`location`、`credential_file`；两个 Bedrock ID 列出 `base_url`、`auth`、`http_headers`，以及 `aws.profile`、`aws.region`、`aws.credential_export`、`aws.auth_refresh`。Bedrock 和 Vertex 的正式配法用各自的专文，不要把它们当成可以任意覆盖的自定义 ID。

### 2. 写在项目配置里不生效

provider 相关的键放在用户级 `~/.codex/config.toml`。配置参考列出的、在项目级 `.codex/config.toml` 里会被忽略的键包括 `openai_base_url`、`chatgpt_base_url`、`apps_mcp_product_sku`、`model_provider`、`model_providers`、`notify`、`profile`、`profiles`、`experimental_realtime_ws_base_url` 和 `otel`。

2026-11-14 在临时 git 仓库里写了 `model`、`model_provider` 和 `model_providers`，并用 `codex exec --trust` 保存信任。启动摘要采用了项目里的 `model`，`provider` 仍是 `openai`，并警告：

```text
warning: Ignored unsupported project-local config keys in <项目>/.codex/config.toml: model_provider, model_providers. If you want these settings to apply, manually set them in your user-level config.toml.
```

未加 `--trust` 时，0.169.0 会先禁用整份未信任的项目配置，包括 MCP。那条警告和 `--trust` 的含义见 [Codex CLI 0.169.0](../12-官方工具与集成/25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)。团队要统一 provider 时，写进每人的用户级配置，或由管理员用受管配置下发。

### 3. 配置参考里已经没有的旧字段

一些旧教程里的 `disable_response_storage`、`preferred_auth_method`，在 2026-11-14 的配置参考字段表里仍然查不到。默认情况下 Codex 不会因为未知字段拒绝启动；加上 `--strict-config` 会指出来。0.169.0 把 `disable_response_storage = true` 放进独立的 `CODEX_HOME` 再执行 `codex exec --strict-config`，报错是 `unknown configuration field`。`--strict-config` 的用法见 [config.toml 配置指南](./04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 本地模型与官方内置示例

跑 Ollama 或 LM Studio 用 `--oss`，不必自定义 provider。用 `--local-provider` 选一次，或在配置里设默认值：

```toml
oss_provider = "ollama" # 或 "lmstudio"
```

两者都没设时，交互式 CLI 会让你选，`codex exec` 直接报错。0.164.0 一文记录过的两句报错，本次没有重跑 Ollama：

```text
Error: No default OSS provider configured. Use --local-provider=provider or set oss_provider to one of: lmstudio, ollama in config.toml
```

本机没有 Ollama 进程时，0.164.0 的报错是 `No running Ollama server detected`，并提示 `ollama serve`。这句没有在 0.169.0 上重测。

**Azure** 示例仍在 Advanced Config 里：

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
```

同一节的示例还写了 `request_max_retries`、`stream_max_retries` 和 `stream_idle_timeout_ms`。字段默认值以配置参考的表格为准，示例里的数字是那个示例自己的取值。

**API 组织的数据驻留**：开启了数据驻留的 API 项目，可以建一个 provider，把 `base_url` 换成带区域前缀的地址，例如 `https://us.api.openai.com/v1`。用 ChatGPT 登录的工作区不需要这样做，Codex 会遵循工作区的驻留设置。

**Amazon Bedrock**：`model_provider` 用 `amazon-bedrock`（Mantle）或 `amazon-bedrock-runtime`（Runtime）。Mantle 的区域和 profile 写在 `[model_providers.amazon-bedrock.aws]`。步骤、模型和限制见 [接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)。

**Google Cloud Vertex AI**：`model_provider = "gcp"`，在 `[model_providers.gcp]` 里写 `project_id` 和 `location`。省略时分别读取 `GOOGLE_CLOUD_PROJECT`、`GOOGLE_CLOUD_LOCATION`，location 默认 `global`。见 [接入 Google Cloud Vertex AI](../12-官方工具与集成/13-Codex接入Google-Cloud-Model-Garden.md)。

## 改完怎么确认

1. 跑一次 `codex exec`，看开头启动摘要里的 `provider:` 和 `model:`。0.169.0 的摘要仍会打印这两行。
2. 交互界面里用 `/status`。Connect to a gateway 也把 `/status` 写成核对当前模型和 provider 的步骤。本文没有打开 TUI。
3. 怀疑请求没发到预期地址时，把 `base_url` 临时指向本机一个只记录请求的服务，看路径和请求头，再换回真实地址。不要把真实 Key 写进 `config.toml` 或仓库，用 `env_key` 指向环境变量。
4. 网关是否真的把请求转到了预定的上游，要由网关日志确认。一次模型回复本身不能证明路由。Connect to a gateway 的验证句是让模型只回复 `gateway-ok`，再请管理员核对记录。本文没有真实网关，没有做这一步。

## 参考资料

- [Advanced Config：Custom model providers](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [rust-v0.168.0](https://github.com/openai/codex/releases/tag/rust-v0.168.0)、[rust-v0.169.0](https://github.com/openai/codex/releases/tag/rust-v0.169.0)
- 同库：[登录 Codex](../01-安装与首次使用/07-登录Codex.md)、[接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)、[接入 Google Cloud Vertex AI](../12-官方工具与集成/13-Codex接入Google-Cloud-Model-Garden.md)、[Codex CLI 0.169.0](../12-官方工具与集成/25-Codex-CLI-0.169-侧边对话标签页任务搜索与终端Cloud连接.md)

官方资料与请求路径的核对日期：2026-11-14（Asia/Shanghai）。终端菜单和网关设备码没有实测，也没有截图。
