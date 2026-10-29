---
id: codex-openai-developers-plugin
title: Codex 安装 OpenAI Developers 插件：安全创建 API Key、写入 .env.local 与排查 API 报错
seo_title: Codex OpenAI Developers 插件：创建 API Key 与排查 API 报错
description: OpenAI Developers 是官方 Codex 插件，能在对话里创建 OpenAI 项目 API Key，加密传到本机写进 .env.local，还能判断 API 报错的原因。本文讲安装步骤、Key 的创建流程、本地写入规则和已知问题，并附插件自带测试和假 Key 的本地实测结果。
lede: 想让 Codex 帮你做一个调用 OpenAI API 的应用，又不想把 API Key 贴进对话，就用这个插件。
url: /guides/codex-openai-developers-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-29
date_modified: 2026-10-29
verified_on: 2026-10-29
tested_cli_version: 0.165.0
official_ref: https://developers.openai.com/learn/developers-codex-plugin
keywords: [Codex OpenAI Developers 插件, Codex 创建 API Key, OPENAI_API_KEY .env.local, Codex 插件, OpenAI API 报错排查]
howto: true
faq:
  - q: 插件创建的 API Key 会出现在对话里吗？
    a: 按插件的设计不会。Key 由 OpenAI Platform 连接器用本机生成的公钥加密后返回，本地脚本解密后直接写进你确认的 env 文件，输出里只有文件路径、变量名和是否覆盖了旧值。用假 Key 实测，脚本输出不含明文。
  - q: 默认写到哪个文件？
    a: 没有更明确的项目约定时，默认写到项目根目录的 .env.local，变量名 OPENAI_API_KEY。写之前会请你确认或修改位置。目标文件如果被 Git 跟踪，插件会先停下来再确认一次。
  - q: 用 API Key 登录的 Codex 能用这个插件吗？
    a: 官方文档写，用 API Key 登录时可以安装和使用支持的 OpenAI 官方插件，但有些插件的连接流程需要 API Key 登录不支持的 OAuth 能力。这个插件要连接 OpenAI Platform 应用，本文没有在 API Key 登录下验证。
  - q: 桌面端确认保存位置时直接被拒绝了怎么办？
    a: 这是已知问题 openai/codex#30978（截至 2026-10-29 仍未关闭）：桌面端会自动拒绝插件弹出的保存位置表单。可以改用 Codex CLI 走同样的流程。
  - q: ChatGPT 订阅送的 API 额度能用在这把 Key 上吗？
    a: 可以用在你应用自己的 API 调用上，前提是这把 Key 属于关联了订阅额度的那个 API 组织。但不能用来支付「用 API Key 登录 Codex」的费用。
related: [mcp-getting-started, codex-chatgpt-subscription-api-credits]
---

# Codex 安装 OpenAI Developers 插件：安全创建 API Key、写入 .env.local 与排查 API 报错

> 本文在线版：[codexguide.io/guides/codex-openai-developers-plugin](https://codexguide.io/guides/codex-openai-developers-plugin)

> 核对依据：OpenAI 官方插件页 [OpenAI Developers plugin](https://developers.openai.com/learn/developers-codex-plugin)、官方文档 [Plugins](https://learn.chatgpt.com/docs/plugins) 和 [Authentication](https://learn.chatgpt.com/docs/auth)，以及插件源码 [openai/plugins · plugins/openai-developers](https://github.com/openai/plugins/tree/main/plugins/openai-developers)（版本 1.2.3，提交 `0722921`）。「本地实测」一节在 Linux 上用 Node.js 20.19.2 和一把**假的** Key 跑插件自带的脚本和测试；本机 Codex CLI 0.165.0 没有登录，也没有桌面 App，所以没有在 `/plugins` 里真实安装，也没有截图。核对日期 2026-10-29（北京时间）。

## 这篇适合谁

- 想让 Codex 帮你做一个调用 OpenAI API 的应用、脚本或 Agent 的人。
- 不想把 API Key 复制粘贴进对话或终端的人。
- 刚领了 ChatGPT 订阅送的 API 额度，想把它用起来的人（额度规则见[Codex 与 ChatGPT 订阅 API 额度](../10-配置模型与权限安全/16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)）。

## 一句话结论

- 在 Codex 里运行 `/plugins`，搜 **OpenAI Developers** 安装，再连接它带的 **OpenAI Platform** 应用。
- 之后让 Codex 做「用 OpenAI API 的东西」时，它会先问你：用现有的 Key，还是新建一把。新建的 Key 加密传到本机，默认写进 `.env.local` 的 `OPENAI_API_KEY`，不在对话里出现。
- API 请求报错时，插件会先分清是网络、认证、额度、限流还是权限问题，再给下一步。

## 插件里有什么

插件 1.2.3 包含：

| 组成 | 作用 |
|---|---|
| OpenAI Platform 应用（连接器） | 连接你的 OpenAI API Platform 账号，在指定组织和项目下创建 API Key |
| 本地 MCP 服务器 `openai-api-key-local-confirmation` | 弹出表单，让你确认或修改 Key 的保存位置 |
| Skill `openai-platform-api-key` | API Key 的检查、创建和写入流程 |
| Skill `openai-api-troubleshooting` | API 请求报错的分类和处理 |
| Skill `agents-sdk` | 用 OpenAI Agents SDK 搭建、运行、部署和评估 Agent 应用 |
| Skill `build-chatgpt-app` | 搭建和排查 ChatGPT Apps SDK 项目 |
| Skill `chatgpt-app-submission` | 生成 ChatGPT App 提交用的 `chatgpt-app-submission.json` |

在 Codex 里，它和 Codex 自带的 OpenAI Docs Skill 配合使用，查官方文档。

## 步骤 1：安装插件

官方插件页给出的步骤（Codex CLI）：

1. 在项目目录启动 Codex：

   ```bash
   codex
   ```

2. 打开插件浏览器：

   ```text
   /plugins
   ```

3. 搜索 **OpenAI Developers**，打开后选择 `Install plugin`。
4. 如果 Codex 提示连接插件自带的 **OpenAI Platform** 应用，按提示完成连接。插件要靠它来创建项目 API Key。
5. **新开一个对话**再使用插件。

ChatGPT 桌面端的 Codex 也能装：在插件目录里搜 OpenAI Developers。插件入口和权限的通用说明见[Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)。

关于登录方式：官方文档写，用 API Key 登录 Codex CLI 或桌面端时，可以安装和管理「支持的」OpenAI 官方插件；有些插件的连接流程需要 API Key 登录不支持的 OAuth 能力，因此不可用。这个插件需要连接 OpenAI Platform 应用，本文没有在 API Key 登录下验证，建议用 ChatGPT 账号登录后安装。

## 步骤 2：让 Codex 创建并写入 API Key

装好以后不需要专门调用。当你让 Codex「做一个用 AI 生成 xx 的小工具」「给这个项目接上 OpenAI API」，或者直接说「帮我建一个 OpenAI API Key」时，`openai-platform-api-key` 这个 Skill 会先介入。按 Skill 的规定，流程是这样的：

**1. 先检查，再问你。** Codex 会检查环境变量和 `.env.local`、`.env` 等文件里有没有可用的 `OPENAI_API_KEY`。检查只看「有没有」，不允许用 `cat .env`、`grep OPENAI_API_KEY .env` 这类会把值打出来的命令。然后它会问你：

- 找到了现成的 Key：用这把，还是新建一把？
- 没找到：要不要安全地新建一把？

在你回答之前，它不会建目录、写代码或让你先手动填 Key。如果你一开始就明确说要新 Key，这一问会跳过。

**2. 选 Key 的名称、组织和项目。** 优先用 OpenAI Platform 连接器提供的选择界面，在里面填 Key 名称、选组织和项目。Codex 不会把本地路径发给这个界面。

**3. 确认保存位置。** 本地 MCP 服务器弹出表单，显示推荐的位置（默认项目根目录的 `.env.local`，变量名 `OPENAI_API_KEY`），你可以改。如果这个工具不可用，Codex 会只问一句：

```text
Save the new key to <path>? Reply yes to continue, another workspace-relative env-file path to change it, or decline.
```

如果你选的文件被 Git 跟踪，Codex 会停下来，再确认一次你确实要把密钥写进这个文件。

**4. 加密创建，本地解密写入。** 本地脚本先生成一对临时密钥，只把**公钥**交给连接器；连接器在 OpenAI Platform 上创建 Key，用公钥加密后返回；本地脚本用私钥解密，直接写进你确认的文件。整个过程中，明文 Key 只在本地脚本的内存里出现。

**5. 验证。** 条件允许时，Codex 会跑一下项目的命令确认能用，但不会去读或显示 Key 的值。

如果连接器还没连上，Codex 会请你在 `/apps` 或 `$` 应用选择器里连接 OpenAI Platform，连好后重试。

## 本地实测：插件脚本到底做了什么

本机没有登录 Codex，没法走连接器创建真 Key，所以只测插件自带的本地部分：在插件目录跑自带测试，再用一把假的 `sk-proj-` Key 模拟「连接器返回的密文」，交给插件脚本解密写入。

**插件自带测试**（Node.js 20.19.2）：

```bash
node --test plugins/openai-developers/tests/openai-platform-api-key.test.mjs
```

```text
# tests 30
# pass 28
# fail 0
# skipped 2
```

**第一步 `prepare`**：生成临时密钥对，输出只有请求文件路径、私钥文件路径、公钥（`kty`、`n`、`e` 三个字段）和 Key 名称。

```bash
node scripts/openai-platform-api-key.mjs prepare --name "Codex"
```

**第二步 `decrypt`**：写进一个新的 `.env.local`：

```bash
node scripts/openai-platform-api-key.mjs decrypt \
  --private-key "<prepare 返回的私钥路径>" \
  --ciphertext "<密文>" \
  --target /path/to/demo/.env.local \
  --workspace /path/to/demo \
  --env-name OPENAI_API_KEY
```

```json
{
  "target_path": "/path/to/demo/.env.local",
  "env_name": "OPENAI_API_KEY",
  "existed": false,
  "updated_existing": false,
  "wrote_plaintext_to_stdout": false
}
```

实测结果：

| 情况 | 结果 |
|---|---|
| 写入新的 `.env.local` | 成功；文件权限 `600`（只有自己能读写）；输出里没有 Key |
| 目标 `.env` 已有 `FOO=bar` 和旧的 `OPENAI_API_KEY` | 只替换 `OPENAI_API_KEY` 的值，`FOO=bar` 保留；输出 `"existed": true, "updated_existing": true` |
| 目标在工作区外面 | 拒绝：`Target env file must be inside the workspace. Workspace: … Target: …`，退出码 1 |
| 目标是符号链接 | 拒绝：`Refusing to write API key through symlink target: …`，退出码 1 |

另外两点要自己注意：

- **不会自动加 `.gitignore`**。实测写入后，`git status` 里 `.env.local` 显示为未跟踪文件。项目里没有忽略规则的话，自己把 `.env.local` 加进 `.gitignore`，别把 Key 提交上去。
- **临时私钥文件不会自动删**。`decrypt` 之后，`prepare` 生成的私钥文件（在系统临时目录下）还在。这把私钥只对应这一次请求，但用完删掉更稳妥。

## 步骤 3：API 请求报错时

`openai-api-troubleshooting` Skill 在请求已经发出、出错之后介入，按下面的顺序判断：

| 现象 | 判断 | 下一步 |
|---|---|---|
| DNS 错误、连接超时、连接被重置，没有任何 API 响应 | 网络问题，请求没到 OpenAI | 先修网络。在 Codex 沙箱里跑的，Skill 会申请提权只重跑这一个请求 |
| `401`、`invalid_api_key`、没有 `OPENAI_API_KEY` | 没认证 | 交给 API Key Skill 创建或配置 Key |
| `insufficient_quota`、额度用完 | 账单或额度问题，不是临时限流 | 去 [Billing](https://platform.openai.com/settings/organization/billing) 充值；月度花费上限去 [Limits](https://platform.openai.com/settings/organization/limits) 调 |
| `rate_limit_exceeded`，没有额度用完的字样 | 限流 | 降低并发、批量、指数退避，不要去买额度 |
| `403`、`model_not_found`、组织或项目不匹配 | 请求到了，但没权限 | 检查模型、项目、组织和 Key 的范围 |

Skill 特别提醒：`insufficient_quota` 和普通限流都可能是 `429`，要看具体的错误码。用订阅送的 API 额度时，额度用完返回的是 HTTP `429`、错误码 `credit_balance_exhausted`。

## 已知问题：桌面端确认保存位置被自动拒绝

GitHub issue [openai/codex#30978](https://github.com/openai/codex/issues/30978)（截至 2026-10-29 仍未关闭）：在 macOS 桌面端走这个流程时，插件弹出的「确认保存位置」表单没有显示出来，桌面端直接返回了「拒绝」，插件因此按设计停止创建 Key。报告者的环境是桌面端自带 CLI 0.142.5、插件 1.2.3。

遇到同样的情况，可以先在终端里用 Codex CLI 走一遍。

## 在 Claude Code 和 Cursor 里用

官方也做了这两个工具的版本，包含可移植的 Skill 和公开的 OpenAI Docs MCP，但**没有** Codex 版的 OpenAI Platform 连接器，所以 API Key 部分是引导你在本地设置 `OPENAI_API_KEY`，而不是直接帮你创建。

- Claude Code：

  ```text
  /plugin marketplace add openai/openai-developers-for-claude
  /plugin install openai-developers@openai-developers
  ```

  然后新开一个会话。
- Cursor：在 Settings → Plugins 的搜索框里粘贴 `https://github.com/openai/openai-developers-for-cursor`，找到 OpenAI Developers 后安装。

## 下一步

- MCP 的基本概念和权限边界：[Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)
- 插件的安装、调用和权限：[Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)
- 订阅送的 API 额度怎么领、能用在哪：[Codex 与 ChatGPT 订阅 API 额度](../10-配置模型与权限安全/16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)

## 参考资料

- OpenAI 官方插件页：[OpenAI Developers plugin](https://developers.openai.com/learn/developers-codex-plugin)
- OpenAI 官方文档：[Plugins](https://learn.chatgpt.com/docs/plugins)、[Authentication](https://learn.chatgpt.com/docs/auth)
- 插件源码：[openai/plugins · plugins/openai-developers](https://github.com/openai/plugins/tree/main/plugins/openai-developers)
- 已知问题：[openai/codex#30978](https://github.com/openai/codex/issues/30978)
