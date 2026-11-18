---
id: codex-prompting-gpt-6-2
title: Codex 提示词怎么写给 GPT-6.2：推理强度、子代理并行、视觉参考图和精简 AGENTS.md，照官方指南改
seo_title: Codex 提示词怎么写给 GPT-6.2：推理强度、子代理与 AGENTS.md
description: GPT-6.2 上线后，Codex 的提示写法有几处要调整。本文照 OpenAI 官方指南整理：怎么告诉 Codex 你验收看什么、推理强度按任务深度怎么选、什么时候让它用子代理并行、怎样用参考图做视觉资产，以及 AGENTS.md 为什么要保持精简。
lede: 先告诉 Codex 你验收时看什么。推理强度按调查有多深来选，能拆开的工作写明可以用子代理，视觉任务给参考图并在真实尺寸下检查。
url: /guides/codex-prompting-gpt-6-2
status: published
section: guides
category: B-core-concepts
topic: 核心概念与任务方法
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE, ChatGPT Work]
difficulty: 入门
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-18
date_modified: 2026-11-18
verified_on: 2026-11-18
models: [gpt-6.2-astra, gpt-6.2-sol]
official_ref: https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra
keywords: [Codex GPT-6.2 提示词, Codex 子代理, Codex 推理强度, AGENTS.md 精简, Prompting GPT-6.2 in Codex]
related: [codex-prompting-guide, codex-subagents-parallel-work, agents-md, codex-gpt-6-2-astra-sol]
faq:
  - q: 这篇和《Codex 提示词怎么写》怎么分工？
    a: 那篇按官方 Prompting 文档讲目标、上下文、边界和验收，并整理了 9 个编程任务示例。这篇只整理 Prompting GPT-6.2 in Codex 里新增的几条：验收时看什么、推理强度按调查深度选、子代理、视觉参考图、精简 AGENTS.md，以及多 agent 共用一台电脑。
  - q: 推理强度 Medium、High、Extra High 怎么对应？
    a: 官方指南写：快速摸一遍可以用 Medium；哪怕只追一个可疑原因、但要跨好几个系统，可以用 High；几个原因可能互相影响、调查要逐个顾到时，再考虑 Extra High。
  - q: 要不要每次都写 use subagents as needed？
    a: 任务有几块可以各自往前做时，官方建议写上 use subagents as needed，让 Codex 自己决定什么时候并行、怎么拆。同一类工作会反复出现时，把这句话写进对应 Skill 或 AGENTS.md，并写明什么情况下适用。Ultra 档由 Codex 自己决定何时派子代理，留给能干净拆开的大任务。
  - q: AGENTS.md 应该写多长？
    a: 官方指南要求保持精简：只放 Codex 从代码、测试和文档里推不出来的项目要求和约定，以及项目依赖的工作流。怎么做的日常决定留给 Codex。继承关系和验收标准的写法见 AGENTS.md 专文。
---

# Codex 提示词怎么写给 GPT-6.2：推理强度、子代理并行、视觉参考图和精简 AGENTS.md，照官方指南改

> 核对依据：官方指南 [Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)（2026-11-18 打开），以及它链出的 [推理强度](https://learn.chatgpt.com/docs/models?surface=app#app-pick-a-reasoning-effort)、[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#triggering-subagent-workflows)、[Skills](https://learn.chatgpt.com/docs/build-skills)、[Max 与 Ultra](https://learn.chatgpt.com/docs/models?surface=app#app-know-when-to-use-max-or-ultra)、[Image generation](https://learn.chatgpt.com/docs/image-generation#generate-or-edit-an-image)、[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 和 [Codex Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments#start-a-task-in-codex-cloud)。指南里的「SVG & 3D Design」插件页可以打开。本文没有桌面端，没有跑一轮 GPT-6.2 对话，下面的中文提示是按指南改写的示例，不是官方原文，也不是实测结果。

官方指南说：这些写法适用于整个 GPT-6.2 系列，包括 GPT-6.2 Astra 和 GPT-6.2 Sol。怎么选这两款、谁能用、额度怎么算，见 [Codex 用 GPT-6.2 Astra 和 Sol](../10-配置模型与权限安全/29-Codex使用GPT-6.2-Astra与Sol-怎么选-切换方法-Ultrafast与额度.md)。

目标、上下文、边界和验收四件事，以及读代码、修 bug、写测试这 9 个编程示例，仍以 [Codex 提示词怎么写](./09-Codex提示词怎么写-目标上下文边界与官方示例.md) 为准。这篇不重复那 9 个例子，只补 GPT-6.2 指南里多出来的几条。

## 先说结论：告诉 Codex 你会怎么验收

指南的核心是两句：用你跟熟悉这个项目的同事说话的方式描述需求，然后告诉 Codex，你检查结果时会看什么。

它举的例子很具体：如果一个图标要在 24 像素的工具栏里仍能认出来，就把这句话写进提示。Codex 可以从现有图标里接上风格，并判断这个尺寸下还能留下多少细节。

验收标准仍然放在这一次任务的提示里。项目里长期不变的要求，放到精简的 `AGENTS.md`，不要每轮把整本规范再贴一遍。

下面是**本文按这句话改写的示例**，不是指南原文：

```text
做一组和现有工具栏图标同一风格的「导出」图标。
我验收时会把它缩到 24 像素看：轮廓要能认出来，细线不能糊成一团。
先给出这个尺寸下仍能看清的方案，再导出。
```

## 推理强度怎么配：Medium、High、Extra High 各对应什么调查深度

指南把推理强度和**调查有多深**绑在一起，而不是和「我想让它更聪明」绑在一起。更高的推理强度可以让模型把一个跑很久的任务做到最后的检查，哪怕你最后要的答案只有几行。你要写清怎样算做完，以及哪里必须查完整。

| 档位 | 指南对应的调查深度 |
|---|---|
| Medium | 快速摸一遍情况 |
| High | 哪怕只怀疑一个原因，也要跨好几个系统追下去 |
| Extra High | 几个原因可能互相影响，调查要逐个顾到 |

如果团队要的是一份建议，指南的说法是：沿着一条有希望的线索查到足够深，拿它和互相竞争的解释对过，再下结论。

桌面端、Work 网页和 IDE 扩展里，这一档叫 Light；CLI 里对应 Low。High、Extra High 的名字各端一致。八组起步组合和速度档见 [模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。GPT-6.2 的指南没有要求默认拉到 Extra High。

本文示例：

```text
结账有时会重复扣款。请先做一次快速调查（推理强度用 Medium）：
列出最可能的三个原因，以及各自要看的日志或测试。
先不要改代码。
```

如果这轮已经锁定一个原因，再把调查加深：

```text
就追「支付回调被处理了两次」这一条。
它会经过网关、订单服务和账本，请跨这三个系统核对（用 High）。
做完的标准：指出重复发生的那一次调用，并给出能复现的测试名字。
```

## 子代理并行：写「use subagents as needed」，什么时候用 Ultra

任务里有几块可以各自往前做时，指南让你告诉 Codex：按需要使用子代理。英文就是 **use subagents as needed**。这句话的作用是允许 Codex 自己判断并行有没有帮助、工作怎么分。

同一类工作会反复出现时，把这句话写进对应的 Skill 或 `AGENTS.md`，并写明什么时候适用。指南的例子：一个研究用的 Skill，可以规定「请求里有好几个互相独立的问题时」适用。

**Ultra** 是另一档。开了 Ultra，Codex 自己决定什么时候叫子代理。指南建议把它留给特别大、而且能干净拆开的工作，例如一个开放式研究，里面有好几个问题，每个都值得单独深挖。每个 agent 可以守着自己的上下文，只跟其中一个问题。

子代理怎么派生、沙箱怎么继承、`/subagents` 打开的是什么，这篇不展开，见 [Codex 使用 Subagents 并行处理任务](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)。Skills 的文件格式见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) 和官方 [Build skills](https://learn.chatgpt.com/docs/build-skills)。

本文示例，只在确实能拆开时使用：

```text
这三件事彼此独立：补齐退款 API 的测试、核对发票 PDF 的字段、列出部署文档里过期的命令。
use subagents as needed。
每件事交回：改了什么、怎么验证、还没做的部分。不要互相改同一批文件。
```

## 视觉任务：给参考图、让它在真实显示尺寸下检查

心里已经有一个样子时，指南建议给一张参考图：形状怎么拼、哪种颜色跳出来、眼睛先落到哪里。图可以来自你的设计软件，也可以让 Codex 用 GPT Image 做一张。参考图已经对上你要的样子之后，再让它做出资产、渲染，并对照参考图修改。

然后让 Codex 在**人们真正会看到的尺寸**下检查。大图里好看的细节，放到成品尺寸可能消失。结果是可交互的，就让它把该支持的操作试一遍。

图像生成的入口（App、网页、CLI 的 `$imagegen`、IDE）在官方 [Image generation](https://learn.chatgpt.com/docs/image-generation)。指南还指向 [SVG & 3D Design 插件](https://chatgpt.com/plugins/Plugin_13c5903473e081919917a1070fad1dd1)：这个插件带一个 Skill，用来走可编辑插画和 3D 模型的这套流程。2026-11-18 该链接返回页面，HTML 标题是 ChatGPT，本文没有安装这个插件，也不把它的效果写成实测。

本文示例：

```text
参考我附上的这张图标：圆角、线宽和留白照着它。
请做成可编辑的 SVG，并在 24×24 和 16×16 两种显示尺寸下各看一次。
哪一档细节糊了，就减细节，不要只交一张放大图。
```

截图和参考图仍然只说明视觉要求。路由、组件和不能改的接口，用文字另写。这一点和 [提示词四件事](./09-Codex提示词怎么写-目标上下文边界与官方示例.md) 里的截图说明是同一条边界。

## AGENTS.md 保持精简：只放 Codex 推不出来的要求

指南对 `AGENTS.md` 的范围限制得很窄：

- 放 Codex **从代码、测试或文档里推不出来**的项目要求和约定。
- 项目确实依赖某条工作流时，把这条工作流写进去。
- 日常「这一步怎么做」留给 Codex 自己决定。

文件怎么被发现、项目级和全局级怎么叠、`project_doc_max_bytes` 默认 32 KiB，见官方 [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。仓库里的写法、继承和验收标准见 [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。

一篇会越写越长的 `AGENTS.md`，每轮都进上下文，也更费额度。Pricing 页把「缩小 AGENTS.md」列为让用量更耐用的办法之一：大仓库用嵌套文件控制注入量。那是用量建议；这篇的依据是 GPT-6.2 指南对内容范围的限制。两篇一起看，结论是同一方向：短，而且只写推不出来的要求。

本文示例，适合放进项目 `AGENTS.md` 的只有这种句子：

```text
对外接口以 docs/api-v3.md 为准。Codex 从代码里看不出来哪些字段已经对客户承诺。
改这些字段之前先停下来问。
发布说明用 docs/release-template.md 的小标题，不要自拟结构。
```

「先读代码再改」「跑测试」这类 Codex 可以从仓库里看出来的习惯，不必再写一遍。

## 多个 agent 共用一台电脑时怎么约束资源与收尾

指南把两种环境分开写。

**Codex Cloud**：每个任务有一台自己的虚拟机。你在自己电脑上继续干活、同时让 Codex 工作的时候，用个人目录里的 `~/.codex/AGENTS.md` 把它引向那些不会抢走当前应用焦点的工具。指南的例子：快速查一封邮件时，让它用已经接上的邮件连接器，这样你正在用的应用可以保持焦点。Cloud 任务怎么开，见 [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments#start-a-task-in-codex-cloud)。本文没有 Cloud 环境。

**好几台 agent 共用这一台电脑**时，指南要求每一台都考虑：

- 同时要跑多少构建或测试，并在做得到的地方给其他工作留出 CPU 和内存。
- 一件确实吃满机器的工作，需要整台机器时把空间让给它。
- 收尾时，停掉自己启动的后台任务，并删掉已经不需要的临时文件。

本文示例，可以放进个人 `~/.codex/AGENTS.md`：

```text
这台电脑上可能同时有别的 Codex 任务。
构建和测试不要一次开很多份；只有当前任务必须吃满 CPU 时再独占。
结束前停掉你启动的后台进程，并删掉你创建的临时文件。
查邮件时用已经配置的邮件连接器，不要把我正在用的应用拉到前台。
```

这是按指南写的约束，不是一份已经在多 agent 机器上测过的配置。

## 和提示词四件事怎么搭配

一次 GPT-6.2 任务可以分成两层：

| 放哪里 | 写什么 |
|---|---|
| 这一次的提示 | 要的结果、这次才有的材料、验收时你会看的那一点、调查要多深、能不能用子代理 |
| `AGENTS.md` 或 Skill | 仓库推不出来的长期约定；会反复出现的「use subagents as needed」以及它什么时候适用 |
| 参考图 | 形状、颜色、视线先落到哪里。真实显示尺寸写在提示里 |

[提示词怎么写](./09-Codex提示词怎么写-目标上下文边界与官方示例.md) 负责把目标、上下文、边界和验收说清。[模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md) 负责 Sol、Astra、Terra、Luna 和八组起步组合。这篇只负责 GPT-6.2 指南里那几条新的写法。

## 参考资料

- [Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)
- [Models：推理强度、Max 与 Ultra](https://learn.chatgpt.com/docs/models)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Image generation](https://learn.chatgpt.com/docs/image-generation)
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)
- [SVG & 3D Design 插件](https://chatgpt.com/plugins/Plugin_13c5903473e081919917a1070fad1dd1)（指南中的链接；本文未安装）
- [Codex 提示词怎么写](./09-Codex提示词怎么写-目标上下文边界与官方示例.md)
- [Codex 使用 Subagents 并行处理任务](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)
- [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)
