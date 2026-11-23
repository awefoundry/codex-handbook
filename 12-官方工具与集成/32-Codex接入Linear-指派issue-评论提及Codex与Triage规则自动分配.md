---
id: codex-linear-integration
title: "Codex 接入 Linear：把 issue 指派给 Codex、在评论里 @Codex，用 Triage 规则自动分配，本地再接 Linear MCP"
seo_title: "Codex 接入 Linear：指派 issue、@Codex 与 Triage 规则"
description: "Codex 可以直接在 Linear 里接活：把 issue 指派给 Codex 或在评论里 @Codex，它会开一个云端任务并把进度和结果回帖。本文按官方文档讲清安装 Codex for Linear、选仓库和环境的规则、Triage 自动指派、常见报错，以及本地用 Linear MCP。"
lede: "指派或在评论里 @Codex，都会开一条 cloud chat，进度回到同一条 issue。这条集成仍走官方写明计划弃用的 Codex Cloud（Legacy），没有弃用日期。"
url: /guides/codex-linear-integration
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [Cloud, CLI]
difficulty: 进阶
order: 32
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-22
date_modified: 2026-11-22
verified_on: 2026-11-22
official_ref: "https://learn.chatgpt.com/docs/third-party/linear"
keywords: [Codex Linear, Codex for Linear, Linear 指派 Codex, "@Codex Linear", Linear MCP Codex]
related: [cloud-environments, mcp-getting-started, codex-github-issue-pr-workflow]
howto: true
faq:
  - q: "Linear 里的 Codex 已经改到新的 Cloud environments 了吗？"
    a: "没有依据这么写。2026-11-22 的 Cloud environments 页写明，Codex Cloud（Legacy）继续支持 Code Review 以及 Linear 和 GitHub 集成，并计划弃用这段体验。页面没有写弃用日期。Linear 文档自己的安装步骤把环境链到 Legacy 环境页。"
  - q: "评论里 @Codex 和把 issue 指派给 Codex 有什么不同？"
    a: "官方写两种都会让 Codex 开始工作并把更新发回 issue。评论适合点名仓库和继续同一条对话；Triage 规则自动指派时，任务用 issue 创建者的账号跑。"
  - q: "本地 CLI 要不要再配一遍 Linear？"
    a: "要。Linear 里的指派走云端 cloud chat。桌面应用、CLI 或 IDE 扩展要在本机读 issue，官方另给 Linear MCP：codex mcp add linear --url https://mcp.linear.app/mcp。"
---

# Codex 接入 Linear：把 issue 指派给 Codex、在评论里 @Codex，用 Triage 规则自动分配，本地再接 Linear MCP

> 核对依据：2026-11-22 打开的 [Use Codex in Linear](https://learn.chatgpt.com/docs/third-party/linear)、[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)、[Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment)、[Codex Cloud 概述](https://learn.chatgpt.com/docs/cloud) 和 [Linear 的 Codex MCP 页](https://linear.app/integrations/codex-mcp)。写作环境没有 Linear 工作区，没有 ChatGPT 付费账号，没有安装 Codex for Linear，没有配图。下面的菜单名只采用这些页面里出现过的英文原文。

适合已经用 Linear 管 issue、并且希望 Codex 在云端改仓库的人。只想在本机对话里读一条 issue，看最后一节的 Linear MCP，不必安装 Codex for Linear。

## 先说结论：Linear 里两种委派方式，结果怎么拿回来

官方 [Use Codex in Linear](https://learn.chatgpt.com/docs/third-party/linear) 写：把 issue 指派给 Codex，或在评论里提到 `@Codex`，Codex 会创建一条 **cloud chat**，再把进度和结果回复到 issue。

两种委派：

- **指派**：安装完成后，像指派同事一样把 issue 指派给 Codex。Codex 开始工作，并把更新发回这条 issue。
- **评论**：在评论线程里 `@Codex`，用来派活或提问。Codex 回复之后，在同一条线程里继续，跟的是同一条 chat。

要钉住仓库，把仓库写进评论，官方例子是 `@Codex fix this in openai/codex`。

进度有两个入口，都写在同一页：

- 打开 issue 上的 **Activity**，看进度更新。
- 打开聊天链接，看更细的过程。

做完后，Codex 会发一段摘要，以及完成那条 chat 的链接，用来创建 pull request。官方同时写明：模型会出错，答案和 diff 都要人看过。

云端环境怎么发布、联网和密钥怎么放，见 [Codex Cloud 云端环境配置](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。从 GitHub issue 走到 pull request 的另一条官方插件路径，见 [GitHub 插件实战](../08-插件工作流/05-GitHub插件实战-从Issue到PullRequest让Codex跑完整流程.md)。

## 准备：付费套餐、GitHub 连接、Cloud 环境

Linear 文档写：Codex in Linear 在付费套餐上可用，并指向 [Pricing](https://learn.chatgpt.com/docs/pricing)。本文没有逐项对照每个套餐按钮，以你账号里能不能安装为准。

Enterprise 要管理员先做两件事，原文是：

- 在 [workspace settings](https://chatgpt.com/admin/settings) 打开 **Codex cloud chats**。
- 在 [connector settings](https://chatgpt.com/admin/ca) 启用 **Codex for Linear**。

安装步骤的第 1 步还要求：在 [Codex](https://chatgpt.com/codex) 连接 GitHub，并为要改的仓库创建一个 environment。这一步的环境链接指向 [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment)，不是新版 Cloud environments 指南。Legacy 页写环境在 Codex settings 里配置，用来决定 cloud chat 安装和运行什么。

### 它现在走的是计划弃用的 Legacy

2026-11-22 的 [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) 页开头写：

> Codex Cloud (Legacy) continues to support Code Review and the Linear and GitHub integrations. We plan to deprecate this experience.

同一天的 [Legacy 环境页](https://learn.chatgpt.com/docs/environments/cloud-environment) 写：Legacy 继续为 Code Review 以及 Linear、GitHub 集成提供环境；网页、手机和桌面的当前体验看 Cloud environments。

两页都没有写弃用日期。本文不补日期，也不把新版 Cloud environments 写成已经接管 Linear。Linear 文档仍把集成叫做创建 cloud chat，安装步骤仍链到 Legacy 环境页。

同一天打开的 [Codex Cloud 概述](https://learn.chatgpt.com/docs/cloud) 正文没有上面那句 “plan to deprecate”。概述页讲的是现行 Cloud：选 **Work in > Cloud**、选已发布环境、任务各自有工作区。Linear 集成不要按概述页的 “Create environment” 流程去理解。

## 安装 Codex for Linear 并关联账号

官方安装顺序：

1. 先按上一节准备 Codex cloud chats：连接 GitHub，并为目标仓库创建环境。
2. 打开 [Codex settings](https://chatgpt.com/codex/settings/connectors)，为工作区安装 **Codex for Linear**。
3. 在一条 Linear issue 的评论线程里提到 `@Codex`，用来关联 Linear 账号。

文档没有写出安装按钮的中文文案，也没有写出关联成功后的提示原文。本文没有点过这个页面。

如果 Codex 确认不了 Linear 连接，它会在 issue 里回复一条带连接链接的消息。这是文档 “Tips and troubleshooting” 里的 **Missing connections**。

## 指派 issue 与评论 @Codex：怎么点名仓库、怎么跟进

指派和评论可以单独用，也可以先指派、再在评论里补充。

点名仓库只用文档里的写法：在评论中写仓库，例如 `@Codex fix this in openai/codex`。文档没有另给一套仓库选择器的字段名。

跟进也只写文档里的规则：Codex 回复之后，在同一条评论线程里继续，这样跟的是同一条 chat。文档没有写换一条评论就会新开 chat。

做完后的交付物是摘要加上完成 chat 的链接，由人从那条链接创建 pull request。本文没有看到真实回帖。

## Codex 怎么选环境和仓库

官方 “How Codex chooses an environment and repo” 是三条：

- Linear 按 issue 上下文建议一个仓库。Codex 选最匹配这个建议的环境。请求含糊时，退回你最近用过的环境。
- chat 跑在该环境 **repo map** 里第一个仓库的默认分支上。要换默认仓库或加入更多仓库，在 Codex 里改 repo map。
- 没有合适的环境或仓库时，Codex 在 Linear 里回复怎么修，然后再试。

选错了环境，文档的处理是在同一条线程里写明要哪个环境，例子是 `@Codex please run this in openai/codex`。改错了代码，就在 issue 里补上下文，或在 `@Codex` 评论里写明确指令。

文档没有写 repo map 的点击路径。本文不编菜单。

## 用 Triage 规则自动指派给 Codex

自动指派用 Linear 的 triage rules。官方步骤：

1. 在 Linear 打开 **Settings**。
2. 在 **Your teams** 下选择团队。
3. 在 workflow settings 里打开 **Triage** 并打开它。
4. 在 **Triage rules** 里建一条规则，选择 **Delegate > Codex**，并设置你还想带上的其他属性。

之后，新进入 triage 的 issue 会自动指派给 Codex。

用 triage 规则时，Codex 用 **issue 创建者的账号**跑 chat。这和你亲手在评论里 `@Codex` 不是同一句说明。创建者没有关联账号、没有 Cloud 环境或没有仓库权限时，任务会停在那个人的权限上。文档没有写可以改成用另一个固定账号跑。

## 本地用：codex mcp add linear 或手写 config.toml

Linear 里的指派是云端。桌面应用、Codex CLI 或 IDE 扩展要在本机访问 Linear issue，官方让你配置 Linear MCP。IDE 扩展和 CLI 共用同一份配置。

官方推荐命令：

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
```

文档写这条命令会提示用 Linear 账号登录，并把它连到 Codex。2026-11-22 在 Linux 的 `codex-cli 0.171.0` 上，`codex mcp add --help` 有 `--url`，说明是给 streamable HTTP MCP 服务器用的。本文没有执行这条 add，因为接下来就是登录，没有 Linear 账号。

手写配置，官方是：

```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

写在 `~/.codex/config.toml`，然后运行 `codex mcp login linear`。

MCP 的通用登录和权限见 [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

Linear 自己的 [Codex MCP 页](https://linear.app/integrations/codex-mcp) 和官方文档有一处不一致：它额外要求第一次使用 MCP 时在 `config.toml` 里写 `rmcp_client = true`。2026-11-22 的 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 没有这个键，`codex features list`（0.171.0）里也没有 `rmcp`。官方 Linear 文档的命令和手写片段都没有这一行。本文不把它写成必做步骤。该页顶部有一句面向 agent 的连接说明，本文没有执行。

## 常见问题：没关联账号、选错环境、改错代码

**没关联账号。** Codex 在 issue 里回一条连接链接。打开链接完成关联后，再在原线程提到 `@Codex`。文档没有写第二次的具体按钮。

**选错环境。** 在原线程回复要使用的环境或仓库，用上一节的 `@Codex please run this in openai/codex` 这种写法。要换默认仓库，改环境的 repo map，而不是只在聊天里说一次。

**改错代码。** 给 issue 补上下文，或在 `@Codex` 评论里写清楚要动的部分。做完后的 diff 仍要人看。

**Legacy 计划弃用。** 影响是：今天的 Linear 集成仍按 Legacy 环境页准备环境，新版 Cloud environments 的 Publish、Connect to services 不能当成 Linear 的安装步骤。弃用日期页面上没有。概述页和 Cloud environments 页对这句弃用声明不一致，以 Cloud environments 页和 Legacy 页为准，因为 Linear 的环境链接指向后者。

**数据。** 提到 `@Codex` 或把 issue 指派给它时，Codex 会收到 issue 内容来建 chat。处理方式指向 OpenAI 的隐私政策、使用条款和 [Codex security](https://learn.chatgpt.com/docs/agent-approvals-security)。不要在 issue 里贴密钥。

## 参考资料

- [Use Codex in Linear](https://learn.chatgpt.com/docs/third-party/linear)
- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)（含 Legacy 计划弃用那一句）
- [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment)
- [Codex Cloud 概述](https://learn.chatgpt.com/docs/cloud)（2026-11-22 的正文没有弃用句）
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Linear MCP for Codex](https://linear.app/integrations/codex-mcp)
- [MCP](https://learn.chatgpt.com/docs/extend/mcp)

Slack 里把仓库任务交给 Codex Cloud，见 [Codex 在 Slack 里怎么用](./33-Codex在Slack里委派仓库任务-提及ChatGPT交给Codex-Cloud与共享环境.md)。
