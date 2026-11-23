---
id: codex-gpt-6-1-terra
title: "Codex 使用 GPT-6.1 Terra：GPT-6.2 Sol 成为默认后，Terra 还适合哪些任务、怎么切换，额度和 Sol、Astra 怎么比"
seo_title: "Codex 使用 GPT-6.1 Terra：默认已是 GPT-6.2 Sol 后怎么切换"
description: "GPT-6.2 Sol 已是 Codex CLI 的默认模型，GPT-6.1 Terra 还值得用吗？本文按官方模型页和价格页更新：Terra 适合写作、看图和电脑操作，哪些套餐和入口能用，怎么用 codex -m 切换，额度和 credits 与 GPT-6.2 Sol、Astra 怎么比。"
lede: "日常编码留在默认的 GPT-6.2 Sol。Terra 仍然是写作、看图和电脑操作上更快、credits 更低的一档，模型 id 还是 gpt-6.1-terra。"
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
date_modified: 2026-11-22
verified_on: 2026-11-22
tested_cli_version: 0.171.0
models: [gpt-6.1-terra, gpt-6.2-sol, gpt-6.2-astra, gpt-6-luna]
official_ref: "https://learn.chatgpt.com/docs/models"
keywords: [Codex GPT-6.1 Terra, gpt-6.1-terra, Terra 和 GPT-6.2 Sol 区别, Codex Terra 额度, "codex -m gpt-6.1-terra"]
related: [codex-gpt-6-2-astra-sol, model-reasoning-effort, usage-limits-credits]
howto: true
faq:
  - q: "哪些套餐和入口能用 GPT-6.1 Terra？"
    a: "2026-11-22 的 Pricing 写：Work 和 Codex 上的 Plus、Pro、Business、Enterprise、Edu 可用。Chat 里没有。不支持阿联酋推理驻留。Enterprise 还取决于工作区是否提供，以及管理员控制。Models 详情卡片列出桌面端的 Work 和 Codex、Work 网页版、CLI、credits 和 API，没有列出 Codex IDE 扩展。"
  - q: "Codex CLI 怎么切到 Terra？默认不是它吗？"
    a: "0.171.0 起模型目录的默认选择是 GPT-6.2 Sol。Terra 需要 CLI 0.159.0 或更高。启动时用 codex -m gpt-6.1-terra，或 codex --model gpt-6.1-terra。交互会话用 /model。长期默认写在 config.toml 的 model。"
  - q: "Terra 的 Fast 倍率是多少，能开 Ultrafast 吗？"
    a: "2026-11-22 的 Pricing：GPT-6.1 Sol 和 GPT-6.1 Terra 的 Fast，套餐内含是 Standard 的 2.5 倍，credits 和企业按量是 2 倍。Ultrafast 表里没有 Terra。"
  - q: "IDE 扩展能选 Terra 吗？"
    a: "同一天的 Models 详情里，GPT-6.1 Sol 和 GPT-6 Luna 有 Codex IDE extension，GPT-6.1 Terra 的卡片没有这一行。配置示例还写：同一份 config.toml 要给 IDE 扩展用时，选每个客户端都能用的模型，举例是 gpt-6.1-sol。以扩展菜单为准。"
---

# Codex 使用 GPT-6.1 Terra：GPT-6.2 Sol 成为默认后，Terra 还适合哪些任务、怎么切换，额度和 Sol、Astra 怎么比

> 本文在线版：[codexguide.io/guides/codex-gpt-6-1-terra](https://codexguide.io/guides/codex-gpt-6-1-terra)

> 核对依据：2026-11-22 的 [Models](https://learn.chatgpt.com/docs/models) 和 [Pricing](https://learn.chatgpt.com/docs/pricing)，以及 [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)（2026-11-20T00:44:47Z）里「模型目录加入 GPT-6.2 Sol 和 Astra，Sol 是默认选择」。CLI 核对在 Linux、`codex-cli 0.171.0`、独立 `CODEX_HOME`、未登录。没有桌面端，没有配图。GPT-6.2 两款怎么选，见 [Codex 用 GPT-6.2 Astra 和 Sol](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。额度总表见 [用量额度](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。推理档位见 [模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

这篇只回答 Terra 还在什么位置。它不重复 GPT-6.2 的总览。

## 先说结论：GPT-6.2 上线后 Terra 的位置

[Models](https://learn.chatgpt.com/docs/models) 现在的建议是：难的端到端工作选 **GPT-6.2 Astra**，日常编码、写作和跨多份材料的工作选 **GPT-6.2 Sol**。同一页对 Terra 的原句是：GPT-6.1 Terra is a fast, efficient choice for writing, visual understanding, and computer use。后文把它放在「日常写作和视觉工作」：把话说清楚、读图片和屏幕、在支持的应用里把任务做完。例子是起草方案、看视觉材料、按源文件填表。

0.171.0 的发布说明把 GPT-6.2 Sol 写成模型目录的默认选择。2026-11-22 未登录的 `codex exec` 启动摘要里，不指定 `-m` 时打印的是 `model: gpt-6.2-sol`。Terra 不再是对照「当前默认编码模型」时的那一档；默认编码模型是 Sol。

模型显示名仍是 **GPT-6.1 Terra**，CLI 的 id 仍是 `gpt-6.1-terra`。

## 一张表：Astra、Sol、Terra、Luna

数字来自 2026-11-22 的 Pricing。5 小时一列是 Plus 和标准 Business 的**本地消息估算**，两列相同，不是固定条数。credits 是 Standard 速度下每 100 万 token。Fast 是相对同一模型 Standard 的倍率。

| 模型 | CLI id | 官方定位（Models） | Plus / 标准 Business，每 5 小时 | credits：输入 / 缓存输入 / 输出 | Fast：套餐内含 / credits | Ultrafast |
|---|---|---|---|---|---|---|
| GPT-6.2 Astra | `gpt-6.2-astra` | 最难的端到端工作 | 6–50 | 200 / 10 / 1,000 | 2 倍 / 2 倍 | 套餐内含 6 倍；credits 在 2027-02-28 前 3 倍，2027-03-01（太平洋时间）起 6 倍 |
| GPT-6.2 Sol | `gpt-6.2-sol` | 日常编码和写作；CLI 默认 | 17–180 | 50 / 2.5 / 250 | 2 倍 / 2 倍 | 与 Astra 同一行 |
| GPT-6.1 Terra | `gpt-6.1-terra` | 写作、看图、电脑操作 | 35–285 | 25 / 1.25 / 125 | 2.5 倍 / 2 倍 | 表中没有 |
| GPT-6 Luna | `gpt-6-luna` | 目标明确、可重复的大批量任务 | 350–3,000 | 2.5 / 0.25 / 12.5 | 2.5 倍 / 2 倍 | 表中没有 |

同一页上 GPT-6.1 Sol 的 5 小时估算仍是 15–160，credits 与 GPT-6.2 Sol 相同，是 50 / 2.5 / 250。Fast 它和 Terra 在一行。不要把「GPT-6.1 Sol」和「GPT-6.2 Sol」看成同一个默认模型。

Terra 的三列 credits 都是 GPT-6.2 Sol 的一半。GPT-6.2 Astra 的输入是 200 credits，Terra 是 25。Luna 更便宜，Models 把它留给抽取、分类、格式已经清楚的任务。

Pricing 的美元脚注只写了 GPT-6.2 Astra（每百万 token 输入 8 美元、缓存输入 0.40 美元、输出 40 美元）和 GPT-6.2 Sol（2、0.10、10 美元）。脚注没有写 Terra 的美元单价。用 API Key 时，Pricing 写按 [API pricing](https://developers.openai.com/api/docs/pricing) 计费。本文不再沿用 2026-10 那篇里的 Terra 美元单价。

本地消息和云端任务共用套餐额度，还可能有每周限制。Pro 目前没有 5 小时限制。Enterprise / Edu 如果是灵活定价，没有固定速率，按 credits 计。这些句子都在 Pricing 的用量表脚注里。完整算法和「觉得被多扣」的查法在 [用量额度](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。10/29 和 10/08 里 Fast、Ultrafast 和 credits 的对应行，与上表是同一页来源。

## 哪些套餐和入口能用

Pricing 的 Feature availability：

> GPT-6.1 Terra is available in Work and Codex on Plus, Pro, Business, Enterprise, and Edu plans. It does not support UAE inference residency. It isn't available in Chat. Access requires the corresponding surface; Enterprise access also depends on workspace availability and administrator controls.

因此：

| 项目 | 2026-11-22 的写法 |
|---|---|
| 套餐 | Plus、Pro、Business、Enterprise、Edu |
| Chat | 不可用 |
| Work 和 Codex | 可用，而且要有对应入口的权限 |
| 数据驻留 | 不支持阿联酋（UAE）推理驻留 |
| Enterprise | 取决于工作区是否提供，以及管理员控制 |

GPT-6.2 Astra 和 Sol 在 Enterprise、Edu 是另一句：默认关闭，管理员要在工作区模型设置里打开。Terra 这段没有写「默认关闭」。找不到 Terra 时仍要问管理员，但不要把 GPT-6.2 的默认关闭原句套到 Terra 上。

Models 详情卡片给 Terra 标了这些入口：桌面端的 Work 和 Codex、ChatGPT Work 网页版、Codex CLI、ChatGPT Credits、API。卡片上没有 Codex IDE extension。同一页的 GPT-6.1 Sol 和 GPT-6 Luna 有这一行。

CLI 的版本门槛仍在 Models 页：GPT-6.1 Terra requires Codex CLI 0.159.0 or later，命令是 `codex -m gpt-6.1-terra`。

## 怎么切换

### 桌面端和 Work

Models 页写：在 ChatGPT 桌面应用的 Work 或 Codex 里，用输入框下方的模型和推理控件选择可用模型，并调整推理强度。如果看到 Power 滑杆，打开 **Advanced** 再选具体模型。页面举的例子是 GPT-6.2 Astra，不是 Terra 的按钮截图。本文没有桌面应用，没有看到 Terra 在当前菜单里的位置。选得到 GPT-6.1 Terra 再用；选不到就停在套餐、入口和管理员这三件事上。

### Codex CLI

2026-11-22 的版本是 `codex-cli 0.171.0`。未登录、`--sandbox read-only`、`--ephemeral` 时：

```bash
codex exec --skip-git-repo-check --sandbox read-only -m gpt-6.1-terra "Reply with the single word ok"
```

启动摘要里有：

```text
OpenAI Codex v0.171.0
model: gpt-6.1-terra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
```

随后请求因未登录失败，HTTPS 回退的状态是 `401 Unauthorized`。没有模型回复。`approval: never` 和 `sandbox: read-only` 来自这次 `codex exec` 和 `--sandbox`，不是 Terra 自己的权限。`reasoning effort: none` 也只是这次未登录摘要，不能当成登录后的默认推理档。Models 页写 GPT-6.2 从客户端当前档起步；Terra 的档位以 `/model` 里看得到的为准。本文没有打开交互会话，没有执行 `/model`。

同一环境下不写 `-m`，摘要里的模型是 `gpt-6.2-sol`。把 `-m` 换成一个不存在的 id 时，才会出现 `Model metadata for ... not found`。`gpt-6.1-terra` 这次没有这句警告。2026-10-27 在 0.164.0 上，未登录的 Terra 曾经打出过这句警告；0.171.0 的这次运行没有。那次警告不再当作当前行为。

交互会话里，Models 页写用 `/model` 切换模型或推理强度。非交互的官方例子是 `codex exec -m gpt-6.2-sol`。Terra 把模型 id 换成 `gpt-6.1-terra` 即可。

### 写进配置

桌面端、CLI 和 IDE 扩展读同一份 `config.toml`。只想让新的 CLI 或桌面 Codex 会话默认用 Terra：

```toml
model = "gpt-6.1-terra"
```

Models 页的配置示例把 `model = "gpt-6.2-sol"` 标成给 app 或 CLI。如果这份文件还要给 IDE 扩展用，页面要求改选每个客户端都能用的模型，举例是 `gpt-6.1-sol`。Terra 的详情卡片没有 IDE 扩展。主要在 IDE 里工作时，不要把默认模型写成一个菜单里没有的 id。

## 什么时候选 Terra，什么时候留在默认的 Sol

留在 **GPT-6.2 Sol**：改代码、审日常 diff、把几份材料收成计划。这是 Models 给 Sol 的范围，也是 0.171.0 的默认选择。跨服务排错、要按模板交付的难题，换 **GPT-6.2 Astra**，条件见 [GPT-6.2 一文](./29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。

改用 **GPT-6.1 Terra** 的情况，按 Models 页：

- 根据已有材料写清楚：方案、说明、给特定读者的文字。
- 看截图、图表、屏幕，并标出看不清的数字。Models 的例子是让它总结仪表盘截图，引用标签和数值，看不清就直说。
- 在已经配好的浏览器或电脑操作里，完成目标明确的填表、录入。先看 [浏览器](https://learn.chatgpt.com/docs/browser) 和 [Computer Use](https://learn.chatgpt.com/docs/computer-use) 的前提。本站的操作边界在 [使用 Computer Use 操作桌面应用](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md)。

范围很小、有测试能核对的代码修复，可以用 Terra 试一次。连续过不了测试，或改动已经跨出单个函数，回到默认的 GPT-6.2 Sol，而不是继续加长提示。

下面这条只复述 Models 页的例子，不是本文跑出来的结果：

```text
Review these dashboard screenshots and summarize the main changes.
Refer to the chart labels and values, and flag anything you can't read confidently.
```

Fast 会把 Terra 的套餐内含用量按 2.5 倍计。Terra 的 credits 已经是 Sol 的一半；要不要再开 Fast，先看 [用量额度](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md) 里的倍率，而不是假设「快」不额外扣额度。

## 参考资料

- [Models](https://learn.chatgpt.com/docs/models)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)
- [rust-v0.171.0](https://github.com/openai/codex/releases/tag/rust-v0.171.0)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)（`model` 写在同一份 `config.toml`）
