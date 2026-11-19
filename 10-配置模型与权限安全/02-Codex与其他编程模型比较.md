---
id: codex-vs-claude-code
title: Codex 与 Claude Code 怎么选：按 GPT-6.2 Astra 与 Sol 更新对照，Terra 和 Luna 放在什么位置
seo_title: Codex 与 Claude Code 怎么选：GPT-6.2 Sol、Astra、Terra、Luna
description: 用工作流而不是跑分来选工具。本文按 2026-11-17 之后的官方 Models 页更新：Codex 一侧以 GPT-6.2 Sol 做日常编码、GPT-6.2 Astra 做最难项目，并说明 GPT-6.1 Terra 与 GPT-6 Luna 还适合什么，再和 Claude Code 的入口、上下文与计费边界对照。
lede: 先问任务落在哪条工作流。日常写代码先试 GPT-6.2 Sol，最难的项目再上 GPT-6.2 Astra。
url: /guides/codex-yu-qita-biancheng-moxing-bijiao
status: published
section: guides
category: B-core-concepts
topic: 核心概念与任务方法
content_type: 解释
source_tag: 官方功能
entry_tags: [App, CLI, IDE, Cloud, ChatGPT Work]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-21
date_modified: 2026-11-19
verified_on: 2026-11-19
models: [gpt-6.2-astra, gpt-6.2-sol, gpt-6.1-terra, gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/models
keywords: [Codex 与 Claude Code, GPT-6.2 Sol, GPT-6.2 Astra, GPT-6.1 Terra, 编程助手怎么选]
related: [codex-gpt-6-2-astra-sol, model-reasoning-effort, codex-gpt-6-1-terra, how-codex-works, usage-limits-credits]
faq:
  - q: GPT-6.2 Sol 能在普通 Chat 里用吗？
    a: 2026-11-19 的 Help Center 写，在 Work 的模型选择器或 Codex 的模型选择器里选 GPT-6.2 Astra 或 GPT-6.2 Sol。普通 Chat 保持它原有的模型。GPT-6.1 Sol、GPT-6.1 Terra 和 GPT-6 Luna 也不出现在普通 Chat 的选择器里。能看见哪些模型，还取决于套餐、席位和工作区设置。
  - q: 日常写代码现在先试哪一款？
    a: Model selection 页写，ChatGPT Work 或 Codex 里的多数任务从 GPT-6.2 Sol 开始。修 bug、加功能的示例组合是 GPT-6.2 Sol 加 Medium。最难的项目用 GPT-6.2 Astra。GPT-6.1 Terra 留给看图、操作桌面应用和范围明确的小修复，GPT-6 Luna 留给结果已经清楚的重复工作。
  - q: Codex 和 Claude Code 谁的上下文更大？
    a: 不能直接比成一个数。Models 页写 GPT-6.2 Astra 和 GPT-6.2 Sol 都支持最多 100 万 token，更长窗口要在 config.toml 里设置 model_context_window。Help Center 仍写 GPT-6.1 Sol 在 Work 和 Codex 的默认窗口是 50 万 token。Anthropic Models overview 里，当前的 Fable 5.2、Opus 5.5、Sonnet 5.5、Haiku 5.5 都是 100 万 token 上下文、最高输出 128K token。入口和是否用到这个窗口，以你实际客户端为准。
  - q: 一定要二选一吗？
    a: 不必。可以按任务拆：日常改仓、审 diff、长任务挂云端用 Codex；探索陌生仓库或要试 Claude Code 的实验性 Agent teams 时用另一边。同一任务不要两边各改一半却不合并。
---

# Codex 与 Claude Code 怎么选：按 GPT-6.2 Astra 与 Sol 更新对照，Terra 和 Luna 放在什么位置

> 本文在线版：[codexguide.io/guides/codex-yu-qita-biancheng-moxing-bijiao](https://codexguide.io/guides/codex-yu-qita-biancheng-moxing-bijiao)

> 2026-11-19 更新：Codex 一侧改按 GPT-6.2 Astra 与 GPT-6.2 Sol。谁能用、怎么切换、Ultrafast 和 credits 不在这篇抄表，见 [Codex 用 GPT-6.2 Astra 和 Sol](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。

> 核对依据：2026-11-19 打开的 [Models](https://learn.chatgpt.com/docs/models)、[Model selection](https://learn.chatgpt.com/docs/model-selection)、[Pricing](https://learn.chatgpt.com/docs/pricing)、Help Center [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)，以及 [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/)。Claude Code 一侧同一天打开了 [Model configuration](https://code.claude.com/docs/en/model-config)、[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 和 [Agent teams](https://code.claude.com/docs/en/agent-teams)。发布公告里的基准分数没有写进结论。文中「我的用法」是工作流建议，不是官方排名。

先问任务落在哪条工作流，再选产品和模型。日常写代码先试 **GPT-6.2 Sol**。跨服务排查、要按模板交付的难题，再上 **GPT-6.2 Astra**。看截图、在应用里操作、范围明确的小修复，仍可以先试 **GPT-6.1 Terra**。结果已经写清楚的重复工作，用 **GPT-6 Luna**。

## 1. 先把产品和模型分开

| 层级 | Codex 一侧（OpenAI） | Claude Code 一侧（Anthropic） |
|---|---|---|
| 产品／入口 | Help Center：Chat 做快问快答；Work 做较长的多步交付；Codex 做软件开发。Codex 在桌面应用里是单独的视图。Codex Cloud 在电脑休眠后仍可继续云端编码任务 | 终端 CLI、IDE、桌面和网页入口。模型别名和版本要求以 Model configuration 为准 |
| 编程向模型 | Work／Codex：`gpt-6.2-sol`、`gpt-6.2-astra`，以及仍可能出现的 `gpt-6.1-terra`、`gpt-6.1-sol`、`gpt-6-luna`、`gpt-6-astra`。普通 Chat 不提供 GPT-6.2 这两款 | 别名 `sonnet`、`opus`、`haiku`、`fable`。在 Anthropic API 上，前三个解析到 Sonnet 5.5、Opus 5.5、Haiku 5.5。`fable` 在 Claude apps 网关会话里解析到 Fable 5，其他地方解析到 Fable 5.2，除非设置了 `ANTHROPIC_DEFAULT_FABLE_MODEL` |
| 计费入口 | 用 ChatGPT 登录则走套餐用量与 credits；自备 API Key 则走 API 价。倍率表见 [用量额度](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md) | Claude 订阅或 Anthropic Console／第三方提供商。Fable 在部分套餐上会走 usage credits，并可能弹出确认 |

Help Center 在 2026-11-19 打开时显示 “Updated: 5 hours ago”，没有绝对时间。它写：Codex CLI 使用 GPT-6.2 Astra 或 GPT-6.2 Sol 需要 **0.166.0 或更高**。本文的环境装的是 0.170.0，高于这个下限，但没有登录，没有发出一次模型请求。

发布公告的可用性一段写的是 Plus、Pro、Enterprise 和 Edu，没有提 Business。Changelog、What's new 和 Pricing 写了 Business。这个差别和切换步骤已经记在 [GPT-6.2 一文](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。你的账号能不能用，以模型菜单里有没有这两款为准。

## 2. Codex 这边：GPT-6.2 Sol、Astra，以及 Terra、Luna

按 2026-11-19 的 Models 和 Model selection：

| 模型 | 官方怎么定位 | 更适合的任务感 |
|---|---|---|
| **GPT-6.2 Astra**（`gpt-6.2-astra`） | 最难的项目：跨代码、应用或研究做持续判断。Model selection 的例子包括按模板做幻灯片和表格、分析数据、设计复杂 3D 零件 | 难拆、要强判断、踩坑成本高的长链路 |
| **GPT-6.2 Sol**（`gpt-6.2-sol`） | 日常编码、写作，以及把几份材料收成一份计划。多数 Work／Codex 任务从它开始。credits 单价低于 Astra | **日常写代码、审改、多步骤工作** |
| **GPT-6.1 Terra**（`gpt-6.1-terra`） | 写作、视觉理解和电脑操作。Model selection 的例子是浏览桌面应用、更新记录、做完能核对的小修复 | 看截图和图表、目标明确的电脑操作、范围明确的小修复 |
| **GPT-6 Luna**（`gpt-6-luna`） | 频繁、边界清楚的任务：改已有文件、抽字段、处理常规请求。推理强度最多到 Max，不支持 Ultra | 抽取、分类、改造、结构化摘要 |

Model selection 按工作类型给的顺序，六行都是 GPT-6.2 Astra，GPT-6.2 Sol，GPT-6.1 Terra，GPT-6 Luna。页面说这是高层估计，依据包括基准、独立运行的任务示例和用户反馈。本文不展开分数，也不采用发布公告里的第三方基准。

补充几条当天读到的边界：

1. **推理强度会换速度与用量。** 桌面端和网页 Work 用输入框下方的模型和推理控件。看到 Power 滑杆时，打开 Advanced 再选具体模型。CLI 用 `/model`，或 `codex --model gpt-6.2-sol`、`codex exec -m gpt-6.2-sol`。更高 effort 更慢，也更耗 token。八组起步组合见 [Codex 模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。
2. **Terra 的 credits 单价是 Sol 的一半。** Pricing 页 Standard 速度下，GPT-6.1 Terra 是每百万 token 输入 25、缓存输入 1.25、输出 125 credits；GPT-6.2 Sol 是 50、2.5、250。完整倍率表不在这里抄，见用量一文。Terra 仍需要 Codex CLI 0.159.0 或更高，Models 页的入口说明里没有把 IDE 扩展列进去。
3. **上下文要分入口说。** Models 页写，两款 GPT-6.2 都支持最多 100 万 token；要在 Codex 里用更长的窗口，在 `config.toml` 设置 `model_context_window`。Help Center 写 GPT-6.1 Sol 在 Work 和 Codex 的默认窗口是 50 万 token，套餐内用量没有另加长上下文附加费。默认窗口和 IDE 扩展是否列出 GPT-6.2，以 [GPT-6.2 一文](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md) 对照过的详情卡为准。本文没有改 `model_context_window`。
4. **GPT-6 Astra 和 GPT-6.1 Sol 还在。** Models 页仍把 GPT-6 Astra 和 GPT-6.2 Astra 并列为最难的端到端工作可选模型。新任务的起点按上面四款。菜单里看得到旧款，就可以继续用。
5. **Enterprise／Edu 常要管理员先开。** Help Center 写，模型不见时先确认人在 Work 或 Codex，托管工作区再请管理员检查模型权限。细节不在这篇展开。

CLI 示例（模型名以你账号可用为准；Help Center 要求 CLI 0.166.0+ 才能用这两款 GPT-6.2）：

```bash
codex --model gpt-6.2-sol
codex exec -m gpt-6.2-sol "Review the current changes"
codex -m gpt-6.1-terra
```

配置默认本地模型时，Models 页给 app 或 CLI 的示例是 `model = "gpt-6.2-sol"`。同一份配置还要给 IDE 扩展用时，页面建议改选每个客户端都能用的模型，举例是 `gpt-6.1-sol`。

云端侧：Help Center 写 Codex Cloud 在 OpenAI 托管的电脑上跑编码任务，电脑休眠也能继续。环境要先在桌面或网页创建并发布，才能给手机任务选用。本地文件夹和终端仍主要在桌面 Codex、CLI 和 IDE。

## 3. Claude Code 这边：2026-11-19 核对过的部分

只改当天官方文档里能核对的句子。没有新变化的产品事实保留，并标明核对日期。

| 维度 | 2026-11-19 读到的官方说法 | 和 Codex 对照时怎么读 |
|---|---|---|
| 模型别名 | `sonnet` 日常编码，`opus` 复杂推理，`haiku` 简单快任务，`fable` 最长、最难。另有 `opusplan`：计划用 `opus`，执行换 `sonnet` | 别拿「Opus」和「Sol」硬比名字。比的是任务档位 |
| 别名解析到哪一版 | Anthropic API：Opus 5.5、Sonnet 5.5、Haiku 5.5。其他提供商可以更旧，例如 Amazon Bedrock 与 Google Cloud Agent Platform 上的 `sonnet` 是 Sonnet 4.5、`haiku` 是 Haiku 4.5。整张提供商表在 Model configuration | 云厂商不同，别名不是同一个模型 id |
| 版本下限 | Sonnet 5.5 需要 Claude Code v2.1.284 或更高，Opus 5.5 需要 v2.1.280 或更高，Haiku 5.5 需要 v2.1.293 或更高。Fable 5.2 需要 v2.1.321 或更高，Fable 5.1 需要 v2.1.257 或更高 | 本文没有安装 Claude Code，没有跑 `claude update`，版本号只按文档写 |
| `fable` | 未设置 `ANTHROPIC_DEFAULT_FABLE_MODEL` 时，Claude apps 网关会话解析到 Fable 5，其他地方解析到 Fable 5.2。没有任何套餐把 Fable 设成账号默认，要显式选择 | 10 月 27 日这篇写的是 Fable 5.1。2026-11-19 的文档已经改到上面的解析规则 |
| 上下文 | Models overview 里，Fable 5.2、Opus 5.5、Sonnet 5.5、Haiku 5.5 都是 **100 万 token** 上下文、最高输出 **128K token**。更早的型号不是一律 100 万，例如 Haiku 4.5 是 20 万上下文、64K 输出 | 先确认你用的是哪一版，再和 Codex 的窗口比 |
| 并行 | Agent teams **仍是实验功能，默认关闭**。打开方式是环境变量或 settings.json 里的 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。文档写它明显更耗 token；顺序依赖强或同文件抢改时，单会话或 subagent 更合适。打开之后，Claude 自己命名的 subagent 可能以队友身份启动 | Codex 侧的 Ultra 是子代理并行，机制和开关都不同 |
| 计费 | 部分套餐上，Fable 的用量会计入 usage credits。`/model` 选择器会显示 “Requires usage credits”，交互会话里可能弹出确认 | 这是计费行为。本文没有 Claude 账号，没有看到那个弹窗 |

Agent teams 页在抓取结果顶部附有一段面向文档索引的说明，要求再去取 `llms.txt`。那段没有执行。上面的实验状态和开关来自页面正文。

## 4. 按工作流选，不按一个数字选

| 你的场景 | 更值得先试 | 原因（可核对的产品差异） |
|---|---|---|
| 已在 ChatGPT 付费体系，想本地改仓，偶尔把任务挂到云端 | **Codex + GPT-6.2 Sol** | Model selection 把多数 Work／Codex 任务的起点放在 Sol。Cloud 可在电脑休眠后续跑 |
| 最难的端到端判断 | Codex 上 **GPT-6.2 Astra**（若套餐和工作区已经打开） | Models 页把它放在最难的项目。用量通常高于 Sol，先看 Usage |
| 按材料写说明、看截图和图表、在桌面应用里做目标明确的操作 | **GPT-6.1 Terra** | 官方定位就是写作、视觉理解和电脑操作。credits 单价是 GPT-6.2 Sol 的一半 |
| 大批量、范围清楚的小改或抽取 | Codex **GPT-6 Luna**，或 Claude Code **haiku** | 两边都有「边界清楚、偏快」的一档 |
| 终端或 IDE 里深度阅读陌生大仓 | **Claude Code**，日常用 `sonnet`，难推理用 `opus` | 先确认别名在你的提供商上解析到哪一版 |
| 要多人并行、互相质疑的长研究 | Claude Code **Agent teams**（实验，默认关）或 Codex **Ultra**（任务能拆开时） | 开启方式、默认是否可用、计费都不同 |
| 电脑常关、任务要在云端继续 | Codex Cloud，或 Claude 的网页／移动云会话 | 环境与密钥各自跟官方设置走 |
| 只要写邮件、做幻灯、整理材料 | 先看 **ChatGPT Work** 或 Claude 的通用产品 | Help Center 把 Work 写成多步交付，把 Codex 写成软件开发 |

发布公告里的跑分、以及任何第三方基准，都不放进这张表。

## 5. 我的用法（建议，非官方）

1. **默认编程：Codex + GPT-6.2 Sol。** 新功能、修 bug、跑测试、开 PR 风格的审查，先走这一条。推理从客户端当前档起，不够再加。
2. **判断链很长：同一条工作流里换 GPT-6.2 Astra。** 换之前看 Usage。资格、Enterprise 要管理员先开、Ultrafast 的套餐差异，都看 [GPT-6.2 一文](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)，这里不抄表。
3. **写说明、看截图、目标明确的电脑操作：GPT-6.1 Terra。** 适用任务和切换见 [Terra 一文](./14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md)。
4. **机械、可验收的小批处理：GPT-6 Luna。**
5. **探索陌生仓，或要试 Agent teams：Claude Code。** 输出仍以 Git diff 为准。同一任务不要两边各改一半文件。
6. **权限与密钥两边都按最小权限。** Codex 的沙箱和审批见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

刻意不做的事：不把某一天的基准截图写成「谁赢了」；不把同事的口碑写成产品事实；不假设 API 价目表等于 ChatGPT 套餐体验。

## 6. 60 秒自检

1. **任务要落在本地仓库，还是云端环境？** 决定 Codex 本地或 Cloud，或 Claude Code 的本地或网页会话。
2. **这是难判断的长链路，还是范围清楚的重复活？** GPT-6.2 Astra、GPT-6.2 Sol、GPT-6.1 Terra、GPT-6 Luna，或 Claude Code 的 opus、sonnet、haiku、fable。
3. **账单从哪条走？** ChatGPT 套餐用量、API Key、Claude 订阅，还是 credits。先看 Usage 或账单页，再开长任务。

## 相关阅读

- [Codex 用 GPT-6.2 Astra 和 Sol：怎么选、怎么切换，Ultrafast 与额度怎么算](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)
- [Codex 模型怎么选：GPT-6.2 Astra 与 Sol 上线后，Sol、Terra、Luna、Astra 和推理强度怎么搭配](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [Codex 使用 GPT-6.1 Terra：适合哪些任务、怎么切换，额度比 Sol 多多少](./14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md)

## 参考资料

- [Models](https://learn.chatgpt.com/docs/models)
- [Model selection](https://learn.chatgpt.com/docs/model-selection)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
- [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
