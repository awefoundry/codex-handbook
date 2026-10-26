---
id: codex-custom-model-provider
title: Codex 自定义模型提供商：model_providers 和 openai_base_url 怎么配，请求到底发去哪（0.164.0 实测）
seo_title: Codex 自定义模型提供商：model_providers 与 openai_base_url 配置
description: 想让 Codex 走公司网关、代理或第三方模型服务，要配 model_providers 或 openai_base_url。本文用 0.164.0 加本地模拟服务器实测请求路径、鉴权头和常见报错，讲清两种写法怎么选、env_key 与 auth 命令、保留 ID 和只支持 Responses 协议等限制。
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
date_modified: 2026-10-25
verified_on: 2026-10-25
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/config-file/config-advanced
keywords: [Codex model_providers, Codex 自定义模型, openai_base_url, Codex 代理, Codex 网关, env_key, wire_api]
related: [config-toml-guide, codex-model-reasoning-effort]
howto: true
faq:
  - q: 只想让 Codex 走代理或数据驻留地址，需要新建 provider 吗？
    a: 不需要。官方建议直接在 config.toml 里设置 openai_base_url，它只改内置 openai provider 的基础地址，不用另写 model_providers。
  - q: 能不能写 [model_providers.openai] 覆盖内置的 openai？
    a: 不能。openai、ollama、lmstudio 是保留的内置 ID。0.164.0 实测会直接报错拒绝加载配置，提示改名，比如 openai-custom。
  - q: 第三方服务只有 Chat Completions 接口，能接 Codex 吗？
    a: 配置参考里 wire_api 只支持 responses 一个值，也是默认值。实测 Codex 会向 base_url 后面的 /responses 发 POST 请求，所以服务端需要兼容 Responses 接口。
  - q: 把 model_provider 写进项目里的 .codex/config.toml 会生效吗？
    a: 不会。provider 相关的键只能写在用户级配置里。0.164.0 实测会提示 Ignored unsupported project-local config keys，并继续使用用户级的 provider。
---

# Codex 自定义模型提供商：model_providers 和 openai_base_url 怎么配，请求到底发去哪（0.164.0 实测）

> 本文在线版：[codexguide.io/guides/codex-custom-model-provider](https://codexguide.io/guides/codex-custom-model-provider)

> 核对依据：OpenAI 官方文档 [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)。实测环境是 Linux 上的 `codex-cli 0.164.0`，每个场景使用独立的 `CODEX_HOME`，模型服务换成本机 `127.0.0.1:18080` 上的一个**模拟服务器**：它只记录收到的请求方法、路径和请求头，然后固定返回 401。测试用的 Key 是假的，所以**没有真正跑出模型回复**，验证的是配置解析、请求发往哪里、带了哪些头，以及各种报错。核对日期 2026-10-25。

很多人第一次改 Codex 的模型来源，是因为公司有统一的模型网关，或者要走某个代理、某个区域的接口地址。网上的教程写法五花八门，有的字段在当前版本里已经查不到了。

这篇只讲官方文档里有的写法，并用一个本地模拟服务器把请求“拦下来看”：配置写对以后，Codex 到底往哪个地址发请求、带什么头。

## 先判断：你需要哪一种

| 你的情况 | 用什么 |
| --- | --- |
| 公司提供了模型网关，并有接入说明 | 先按官方的网关接入文档配置（见文末参考资料） |
| 只是让内置 OpenAI 走代理、路由器或数据驻留地址 | `openai_base_url`，一行就够 |
| 接一个独立的模型服务，用它自己的 Key | `[model_providers.<id>]` 自定义 provider |
| 本机跑 Ollama 或 LM Studio | `--oss` 本地模式 |
| Amazon Bedrock | 内置的 `amazon-bedrock` provider |

## 写法一：openai_base_url，只改内置 OpenAI 的地址

官方文档的原意：如果你只是想把内置的 OpenAI provider 指向一个 LLM 代理、路由器或开启了数据驻留的项目，**直接设置 `openai_base_url`，不要新建 provider**。

```toml
# ~/.codex/config.toml
openai_base_url = "https://us.api.openai.com/v1"
```

实测把它指向模拟服务器：

```toml
openai_base_url = "http://127.0.0.1:18080/v1"
model = "gpt-5.5"
```

用假 Key 跑一次 `codex exec`（`CODEX_API_KEY=sk-test-... codex exec --skip-git-repo-check "say hi"`），模拟服务器记录到：

```text
GET  /v1/responses   Authorization: Bearer sk-tes…   Upgrade: websocket   （7 次）
POST /v1/responses   Authorization: Bearer sk-tes…   model=gpt-5.5 stream=true   （6 次）
```

终端里先是几行 `Reconnecting... 2/5` 到 `5/5`，最后报：

```text
ERROR: unexpected status 401 Unauthorized: mock server: request recorded, no model here, url: http://127.0.0.1:18080/v1/responses
```

能看出三件事：

1. 请求发往 `openai_base_url` 后面拼上 `/responses`，所以地址要写到 `/v1` 这一层。
2. 内置 OpenAI provider 会先尝试 WebSocket 连接（带 `Upgrade: websocket` 的 GET），失败后改用 HTTP POST 流式请求。你的代理如果不支持 WebSocket，会看到这种先重连、再走 POST 的现象。
3. 失败时会自动重试，所以模拟服务器收到了多次请求。

## 写法二：model_providers，自定义一个 provider

接一个独立的模型服务时，在用户级 `config.toml` 里定义 provider，再用 `model_provider` 指向它。实测用的配置：

```toml
model = "my-gateway-model"
model_provider = "mygateway"

[model_providers.mygateway]
name = "My Gateway"
base_url = "http://127.0.0.1:18080/v1"
env_key = "MYGATEWAY_API_KEY"
http_headers = { "X-Team" = "docs-test" }
request_max_retries = 0
stream_max_retries = 0
```

各字段的含义（摘自配置参考）：

| 字段 | 作用 |
| --- | --- |
| `name` | 显示名称 |
| `base_url` | 模型服务的 API 基础地址 |
| `env_key` | 从哪个环境变量读 API Key |
| `env_key_instructions` | 可选，给使用者看的 Key 设置说明 |
| `wire_api` | 协议，**只支持 `responses`**，也是默认值 |
| `http_headers` | 固定加在请求上的头 |
| `env_http_headers` | 从环境变量取值的请求头，变量存在时才加 |
| `query_params` | 追加到请求上的查询参数，比如 Azure 的 `api-version` |
| `request_max_retries` | HTTP 请求重试次数，默认 4 |
| `stream_max_retries` | 流式中断重试次数，默认 5 |
| `stream_idle_timeout_ms` | 流空闲超时，默认 300000 毫秒 |
| `requires_openai_auth` | 这个 provider 是否使用 OpenAI 鉴权，默认 false |
| `experimental_bearer_token` | 直接写死的 Token，官方不推荐，建议用 `env_key` |

实测把两个重试次数都设成 0，是为了让模拟服务器只收到一次请求，方便观察。日常使用保持默认即可。

### 没设置环境变量时

```text
warning: Model metadata for `my-gateway-model` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
ERROR: Missing environment variable: `MYGATEWAY_API_KEY`.
```

请求根本没有发出，模拟服务器一条记录都没有。第一行警告的意思是 Codex 不认识这个模型名，只能用通用的默认参数，可能影响效果；接非 OpenAI 模型时都会看到。

### 设置环境变量后

```bash
MYGATEWAY_API_KEY=sk-test-not-a-real-key codex exec --skip-git-repo-check "say hi"
```

启动摘要里能看到 `provider: mygateway`、`model: my-gateway-model`。模拟服务器记录到一次请求：

```text
POST /v1/responses
Authorization: Bearer sk-tes…
X-Team: docs-test
Content-Type: application/json
model=my-gateway-model  stream=true
```

终端报错：

```text
ERROR: unexpected status 401 Unauthorized: mock server: request recorded, no model here, url: http://127.0.0.1:18080/v1/responses
```

`codex exec` 的退出码是 1。可以确认：

- `env_key` 里的值以 `Authorization: Bearer <Key>` 的形式发出。
- `http_headers` 里的自定义头原样带上了。
- 请求地址是 `base_url` + `/responses`，请求体是流式的 Responses 请求。

**所以服务端必须兼容 Responses 接口**。只提供 Chat Completions 接口（`/chat/completions`）的服务，不能直接这样接入。

## 需要动态 Token 时：用 auth 命令

如果网关的 Token 要定期刷新，可以让 Codex 调一个外部命令取 Token（示例来自官方文档）：

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

规则：命令没有标准输入，必须把 Token 打印到标准输出；Codex 去掉首尾空白，空 Token 视为错误；按 `refresh_interval_ms` 主动刷新，设成 0 则只在鉴权重试后刷新。**`auth` 不能和 `env_key`、`experimental_bearer_token`、`requires_openai_auth` 同时使用。**

## 三个常见坑

### 1. 不能覆盖保留的内置 ID

`openai`、`ollama`、`lmstudio` 是保留 ID。实测写了 `[model_providers.openai]` 后，Codex 直接拒绝加载配置：

```text
Error loading config.toml: model_providers contains reserved built-in provider IDs: `openai`. Built-in providers cannot be overridden. Rename your custom provider (for example, `openai-custom`).
```

只想改 OpenAI 的地址就用 `openai_base_url`；确实要自定义，就换个名字。

### 2. 写在项目配置里不生效

provider 属于“本机配置”，项目里的 `.codex/config.toml` 不能覆盖。官方配置参考列出的被忽略键包括 `openai_base_url`、`model_provider`、`model_providers` 等。实测在受信任项目里写了 `model_provider` 和 `model_providers`，启动时提示：

```text
warning: Ignored unsupported project-local config keys in /tmp/prov/proj/.codex/config.toml: model_provider, model_providers. If you want these settings to apply, manually set them in your user-level config.toml.
```

启动摘要里 provider 仍是 `openai`，模拟服务器没有收到请求。团队想统一 provider，要么每人写进自己的用户级配置，要么由管理员通过受管配置下发（`requirements.toml` 里可以强制 `model_provider`）。

### 3. 网上教程里的旧字段

一些中文教程的配置里有 `disable_response_storage`、`preferred_auth_method` 等字段。核对日期当天的官方配置参考里**查不到这两个键**。照抄前先到配置参考里搜一下字段名。默认情况下 Codex 不会因为这类未知字段报错；加上 `--strict-config` 可以让它直接指出来。实测把这两个字段写进 `config.toml` 后运行 `codex exec --strict-config`：

```text
Error loading config.toml:
/tmp/prov/ch6/config.toml:1:1: unknown configuration field `disable_response_storage`
```

`--strict-config` 的更多用法见 [config.toml 配置指南](https://codexguide.io/advanced/config-toml)。

## 本地模型：--oss

跑 Ollama 或 LM Studio 不需要自定义 provider，用 `--oss`。官方文档说明：用 `--local-provider` 选一次，或者在配置里设默认值：

```toml
oss_provider = "ollama" # 或 "lmstudio"
```

两者都没设时，交互式 CLI 会让你选，`codex exec` 直接报错。实测：

```text
Error: No default OSS provider configured. Use --local-provider=provider or set oss_provider to one of: lmstudio, ollama in config.toml
```

指定了 `--local-provider ollama` 但本机没跑 Ollama 时：

```text
Error: OSS setup failed: No running Ollama server detected. Start it with: `ollama serve` (after installing). ...
```

## 其他官方示例

**Azure**：

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
```

**API 组织的数据驻留**：开启了数据驻留的 API 项目，可以建一个 provider 把 `base_url` 换成带区域前缀的地址，比如 `https://us.api.openai.com/v1`。用 ChatGPT 登录的工作区不需要这样做，Codex 会遵循工作区的驻留设置。

**Amazon Bedrock**：用内置的 `amazon-bedrock` provider，只支持在 `[model_providers.amazon-bedrock.aws]` 下设置 `profile` 和 `region`。

## 改完怎么确认

1. 跑一次 `codex exec`，看开头启动摘要里的 `provider:` 和 `model:`。
2. 交互界面里用 `/status` 查看。
3. 怀疑请求没发到预期地址时，可以像本文这样，先把 `base_url` 临时指向本机一个只记录请求的小服务，看路径和请求头对不对，再换回真实地址。
4. 不要把真实 Key 写进 `config.toml` 或提交到仓库，用 `env_key` 指向环境变量。

## 参考资料

- [Advanced Config：Custom model providers](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Sign in with ChatGPT through a gateway](https://learn.chatgpt.com/docs/enterprise/sign-in-with-chatgpt-through-a-gateway)
- [Use API/provider credentials](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway)
