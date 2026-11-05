---
id: codex-gpt-6-1-terra
title: Codex 使用 GPT-6.1 Terra：适合哪些任务、怎么切换，额度比 Sol 多多少
seo_title: Codex 使用 GPT-6.1 Terra：适用任务、切换方法与额度
description: GPT-6.1 Terra 已在 Codex 上线。本文按官方文档说明哪些套餐和入口能用、CLI 怎么切换、额度和 credits 比 GPT-6.1 Sol 省多少，以及写作、看图、电脑操作和小范围修复时什么时候选 Terra。
lede: Terra 更快、更省额度，擅长写作、看图和电脑操作；最难的编码任务仍然交给 GPT-6.1 Sol 或 Astra。
url: /guides/codex-gpt-6-1-terra
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [App, CLI, ChatGPT Work]
difficulty: 基础
order: 14
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-27
date_modified: 2026-10-27
verified_on: 2026-10-27
tested_cli_version: 0.164.0
models: [gpt-6.1-terra, gpt-6.1-sol, gpt-6-astra, gpt-6-luna]
official_ref: https://learn.chatgpt.com/docs/models
keywords: [Codex GPT-6.1 Terra, gpt-6.1-terra, Codex Terra 额度, Codex 模型切换, codex -m gpt-6.1-terra]
howto: true
faq:
  - q: 哪些套餐能在 Codex 里用 GPT-6.1 Terra？
    a: 官方 Changelog 和 Pricing 写的是 Plus、Pro、Business、Enterprise 和 Edu 的 Work 与 Codex。Enterprise 还要看工作区是否开放、管理员是否允许。Chat 里没有 Terra，也不支持阿联酋推理驻留。
  - q: Codex CLI 怎么切到 Terra？
    a: 需要 Codex CLI 0.159.0 或更高版本。启动时用 codex -m gpt-6.1-terra，或者在会话里输入 /model 选择；想长期默认就在 ~/.codex/config.toml 里写 model = "gpt-6.1-terra"。
  - q: Terra 比 GPT-6.1 Sol 省多少额度？
    a: 按 Pricing 页，Terra 的 credits 单价是 GPT-6.1 Sol 的一半（每百万 token 输入 25、缓存输入 1.25、输出 125）；Plus 和标准 Business 每 5 小时本地消息估算是 35–285 条，GPT-6.1 Sol 是 15–160 条。实际条数随任务变化。
  - q: IDE 扩展能用 Terra 吗？
    a: 截至 2026-10-27，官方 Models 页给 Terra 列出的入口是桌面端的 Work 和 Codex、Work 网页版、Codex CLI、credits 和 API，没有列 IDE 扩展。以你扩展里的模型菜单为准。
  - q: Terra 能用 Fast 和 Ultrafast 吗？
    a: Fast 支持 Terra，套餐内用量按 Standard 的 2.5 倍计，credits 按 2 倍计。Ultrafast 只支持 GPT-6 Astra 和 GPT-6.1 Sol，不支持 Terra。
---

# Codex 使用 GPT-6.1 Terra：适合哪些任务、怎么切换，额度比 Sol 多多少

> 本文在线版：[codexguide.io/guides/codex-gpt-6-1-terra](https://codexguide.io/guides/codex-gpt-6-1-terra)

> 核对依据：OpenAI 官方 [Changelog（2026-10-26 条目）](https://learn.chatgpt.com/docs/changelog)、[Models](https://learn.chatgpt.com/docs/models)、[Model selection](https://learn.chatgpt.com/docs/model-selection)、[Pricing](https://learn.chatgpt.com/docs/pricing)、[Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)、[API 模型页](https://developers.openai.com/api/docs/models/gpt-6.1-terra) 和 [发布文 Introducing GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra/)。CLI 部分在 Linux 上用 `codex-cli 0.164.0` 实测了 `-m gpt-6.1-terra` 的启动输出；测试机上的 Codex **没有登录**，所以没有 Terra 的对话结果，也没有桌面端截图。核对日期 2026-10-27（北京时间）。

2026 年 10 月 26 日（美国时间），OpenAI 把 GPT-6.1 Terra 加进了 ChatGPT Work 和 Codex。它的定位很明确：快、省额度，擅长写作、看懂图片和屏幕、在应用里操作。

这篇只回答四个问题：谁能用、在哪里切换、比 GPT-6.1 Sol 省多少、什么任务交给它。

## 一句话结论

- **适合交给 Terra**：根据给定材料写说明、邮件、方案初稿；看截图、图表、设计稿后总结或核对；用 Computer Use 或浏览器完成目标明确的操作（填表、录入、整理）；范围很小、有测试能验证的代码修复。
- **仍然交给 GPT-6.1 Sol 或 GPT-6 Astra**：跨模块重构、难排查的 bug、需要长时间规划的端到端编码。发布文原话是：最复杂的编程任务，GPT-6.1 Sol 和 GPT-6 Astra 仍是更好的选择。
- **省额度**：Terra 的 credits 单价是 GPT-6.1 Sol 的一半。

## 谁能用，在哪些入口能用

按官方 Changelog 和 Pricing 页：

| 项目 | 说明 |
|---|---|
| 套餐 | Plus、Pro、Business、Enterprise、Edu |
| 可用的地方 | ChatGPT Work 和 Codex；**Chat 里没有** |
| 桌面端 / Work 网页版 | 在 **Advanced** 的模型列表里选 GPT-6.1 Terra |
| 手机 | Work 支持在手机上用 Terra |
| Codex CLI | 需要 0.159.0 或更高版本 |
| IDE 扩展 | Models 页的入口清单里**没有列出**（Sol、Luna 都列了） |
| Enterprise | 取决于工作区是否开放和管理员设置 |
| 数据驻留 | 不支持阿联酋（UAE）推理驻留 |

有一处官方说法不一致：发布文写的是「Plus、Pro、Enterprise 和 Edu」，没有提 Business；Changelog 和 Pricing 页都写了 Business。本文按 Changelog 和 Pricing 写。你的账号能不能用，以模型菜单里有没有 GPT-6.1 Terra 为准。

Enterprise 和 Edu 用户在菜单里找不到 Terra，先问管理员，不要在配置里硬写一个菜单里没有的模型名。

## 怎么切换到 Terra

### 桌面端和 Work 网页版

在输入框下方的模型控件里打开 **Advanced**，从模型列表里选 **GPT-6.1 Terra**。官方 Models 页说明，桌面端默认显示的是几档 Power 预设，具体模型要在 Advanced 里选。

### Codex CLI

先确认版本不低于 0.159.0：

```bash
codex --version
```

版本太旧就升级：

```bash
npm install -g @openai/codex@latest
```

启动时指定模型：

```bash
codex -m gpt-6.1-terra
```

已经在会话里，就输入 `/model`，选 GPT-6.1 Terra，再选推理强度。

非交互运行也一样：

```bash
codex exec -m gpt-6.1-terra "根据 docs/changelog.md 写一段面向用户的更新说明，只用文件里已有的信息"
```

下面是测试机上 `codex exec -m gpt-6.1-terra` 的实际启动输出（Codex 0.164.0，**未登录**，会话 ID 已省略）。可以看到模型和推理强度都按参数生效了：

```text
OpenAI Codex v0.164.0
--------
model: gpt-6.1-terra
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
--------
warning: Model metadata for `gpt-6.1-terra` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

后面是 401 未认证的重连报错，因为测试机没有登录。那条 `Model metadata ... not found` 警告的意思是：CLI 本地没有这个模型的元数据，只能用默认值。测试机没登录，拿不到线上的模型列表，所以出现这条警告；登录后会不会出现，我们在测试机上没法确认。如果你登录后也看到它，先把 CLI 升到最新版再试。

### 写进配置

想让新会话默认用 Terra，在 `~/.codex/config.toml` 里写：

```toml
model = "gpt-6.1-terra"
model_reasoning_effort = "medium"
```

桌面端、CLI 和 IDE 扩展读同一份 `config.toml`。注意 IDE 扩展的模型清单里官方没有列 Terra，如果你主要在 IDE 里用 Codex，默认模型写 Terra 前先确认扩展菜单里能选到它。

`model_reasoning_effort` 可以写的档位取决于模型和客户端。API 文档给 Terra 列出的推理强度是 `none`、`low`、`medium`（默认）、`high`、`xhigh` 和 `max`；Codex 客户端里实际能选哪几档，以 `/model` 里显示的为准。

## 额度和 credits：和 Sol、Luna、Astra 对比

### 套餐内额度

Pricing 页给出的 Plus 和标准 Business 每 5 小时本地消息估算：

| 模型 | Plus / 标准 Business（每 5 小时） |
|---|---:|
| GPT-6 Astra | 5–45 |
| GPT-6.1 Sol | 15–160 |
| **GPT-6.1 Terra** | **35–285** |
| GPT-6 Sol | 15–150 |
| GPT-6 Luna | 350–3,000 |

这是估算区间，不是固定上限。本地消息和云端任务共用套餐额度，还可能有每周限制。剩余额度看用量面板或 CLI 的 `/status`。Pricing 页也写明，Terra 上线后 Work 和 Codex 的整体套餐限额没有变，只是同样的额度用 Terra 能做更多事。

Codex 团队的 Tibo（@thsottiaux）在 [X 上的说法](https://x.com/thsottiaux/status/2114800277677092936) 是 Terra 在 API 和订阅里的用量是 GPT-6.1 Sol 的 2 倍。这和下面 credits 单价减半的数字一致；Pricing 页的消息条数区间是另一种估算方式，两者不完全对应。

### credits 单价

Standard 速度下，每 100 万 token 的 credits：

| 模型 | 输入 | 缓存输入 | 输出 |
|---|---:|---:|---:|
| GPT-6 Astra | 250 | 25 | 1,250 |
| GPT-6.1 Sol | 50 | 2.5 | 250 |
| **GPT-6.1 Terra** | **25** | **1.25** | **125** |
| GPT-6 Luna | 2.5 | 0.25 | 12.5 |
| GPT-5.6 Terra | 50 | 5 | 300 |

Terra 的输入和输出单价都是 GPT-6.1 Sol 的一半，Astra 的十分之一。Luna 更便宜，但能力明显弱一档，适合格式已经写死的批量工作。

用 API Key 登录的 Codex 按 API 价格计费：Terra 每百万 token 输入 1 美元、缓存输入 0.05 美元、输出 5 美元，上下文窗口 1,050,000 token，最大输出 128,000 token。

### 速度档

- **Fast** 支持 Terra。套餐内用量按 Standard 的 2.5 倍计，已购 credits 和企业按量计费按 2 倍计。
- **Ultrafast** 只支持 GPT-6 Astra 和 GPT-6.1 Sol，**不支持 Terra**。

Terra 本身已经比 Sol 快（发布文说在 Agents' Last Exam 上完成任务的速度是 GPT-6 Astra 和 GPT-6.1 Sol 的三倍多），大多数时候不需要再开 Fast。

## 什么任务交给 Terra

官方 [Model selection](https://learn.chatgpt.com/docs/model-selection) 页建议在这三类任务上试 Terra：

1. **根据给定材料写简洁的文字**：更新说明、PR 描述、方案初稿、邮件。
2. **目标明确的电脑操作**：用 [Computer Use](https://codexguide.io/guides/codex-computer-use-desktop-apps) 或浏览器在应用里填表、录入、整理信息。
3. **范围明确的代码修复**：一个函数的 bug、一处样式问题，并且有回归测试能验证。

前提是给它清楚的输入、要求和验证方法，比如「改完跑 `npm test`」「保存后检查表格里的记录」。

下面几个提示词可以直接改了用：

```text
根据 docs/release-notes-draft.md 和最近 10 个提交，写一段面向用户的更新说明。
只写文件和提交里已有的信息，不确定的地方标出来，不要补充。
```

```text
看 screenshots/ 目录里的三张仪表盘截图，总结主要变化。
引用图表标签和数值；看不清的数字直接说看不清，不要猜。
```

```text
修复 src/utils/date.ts 里 formatRange 在跨年时显示错误的问题。
只改这个函数和它的测试，改完运行 npm test -- date，报告实际结果。
```

### 什么时候换回 Sol 或 Astra

- Terra 连续两轮没有通过测试，或者改动开始波及多个模块。
- 任务需要先读懂大量代码再定方案。
- 你发现自己在反复补充约束，Terra 还是理解偏。

这时直接换 GPT-6.1 Sol，比继续给 Terra 加推理强度更省事。发布文里的一组数字可以参考：Terminal-Bench 4.0 上，Terra 在最高推理强度下解决了 50.3% 的任务，是 GPT-5.6 Terra（21.5%）的两倍多，但官方仍然把最复杂的编程任务留给 Sol 和 Astra。

## 用同一个任务对比 Terra 和 Sol

官方建议的做法是：**同样的输入、同样的推理强度**，分别让 Terra 和 GPT-6.1 Sol 跑一次，再看结果。

1. 挑一个你做过、结果能验证的任务。
2. CLI 里可以这样分别跑：

   ```bash
   codex exec -m gpt-6.1-terra -c model_reasoning_effort='"medium"' "同一段提示词"
   codex exec -m gpt-6.1-sol   -c model_reasoning_effort='"medium"' "同一段提示词"
   ```

3. 写作类任务，除了准确和长度，还要看是否适合读者、语气对不对、有没有有用的细节。
4. 电脑操作类任务，检查实际保存的结果，以及它报告的完成情况是否属实。
5. 记下用了多少额度（`/status`）、花了多久、你自己改了多少。

如果 Terra 在这类任务上稳定达标，就把它设成这类任务的默认模型。

## 常见问题

### 模型菜单里没有 GPT-6.1 Terra

按顺序检查：

1. 套餐是不是 Plus、Pro、Business、Enterprise 或 Edu。
2. 你是不是在 Chat 里找。Terra 只在 Work 和 Codex 里。
3. 桌面端要打开 **Advanced** 才能看到具体模型。
4. Enterprise / Edu：问管理员工作区有没有开放。
5. CLI：`codex --version` 是否低于 0.159.0。

### CLI 提示模型不存在或请求失败

先升级 CLI，再用 `/model` 看列表里有没有 Terra。账号里没有这个模型时，在配置里写 `gpt-6.1-terra` 也用不了。

### 用 API Key 登录能用吗

API 已经提供 `gpt-6.1-terra`。用 API Key 登录的 Codex，模型是否可用取决于你的 API 组织和项目。

## 相关阅读

- [Codex 模型怎么选：GPT-6.1 Sol、Terra、Luna、Astra 和推理强度](01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [Codex 与 Claude Code 怎么选](02-Codex与其他编程模型比较.md)
- [Codex 使用 Computer Use 操作桌面应用](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md)

## 参考资料

- [Changelog - OpenAI Codex](https://learn.chatgpt.com/docs/changelog)
- [Models - OpenAI Codex](https://learn.chatgpt.com/docs/models)
- [Model selection - OpenAI](https://learn.chatgpt.com/docs/model-selection)
- [Pricing - OpenAI Codex](https://learn.chatgpt.com/docs/pricing)
- [Speed - OpenAI Codex](https://learn.chatgpt.com/docs/agent-configuration/speed)
- [GPT-6.1 Terra - OpenAI API](https://developers.openai.com/api/docs/models/gpt-6.1-terra)
- [Introducing GPT-6.1 Terra - OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
