---
id: codex-gpt-6-cyber-daybreak-red
title: Codex 用 GPT-6 Cyber 与 Daybreak Red：准入、和 Astra / Blue 的分工，以及安全研究边界
seo_title: Codex 用 GPT-6 Cyber：Daybreak Red 准入与使用边界
description: GPT-6 Cyber 先向一部分获批的 Daybreak Red 客户在 API 和 Codex 开放。本文只说明谁能用、和 Astra 与 Blue 怎么分工，以及官方要求留在授权范围内。普通订阅默认没有这个模型。
lede: 这不是 Plus 或 Pro 的默认模型。没有 Daybreak Red 资格，就不要在模型列表里找它，也不要把它当成通用编程模型。
url: /guides/codex-gpt-6-cyber-daybreak-red
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 24
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-06
date_modified: 2026-11-06
verified_on: 2026-11-06
official_ref: https://openai.com/index/introducing-gpt-6-cyber
keywords: [GPT-6 Cyber, Daybreak Red, Daybreak Blue, Codex 安全研究, OpenAI Cyber]
related: [codex-daybreak-blue, model-reasoning-effort, codex-security-cli, codex-trail-of-bits-patching-bugs]
faq:
  - q: Plus 或 Pro 订阅里能直接选到 GPT-6 Cyber 吗？
    a: 不能默认拿到。2026-11-05 的官方博文写明，它起初通过 API 和 Codex 提供给一部分已获批的 Daybreak Red 客户，之后再扩大到全部 Daybreak Red 客户。普通 Codex 订阅里的通用模型选择，见模型一文。
  - q: 已经有 Daybreak Blue，是不是就能用 GPT-6 Cyber？
    a: 官方把 Blue 和 Red 分成两层。Blue 面向已验证防御方，减少一部分不必要的拒绝；GPT-6 Cyber 放在 Daybreak Red。Blue 获批不等于 Red 获批。本文作者没有 Red 资格，没有实测模型切换。
  - q: 为什么文里只有数字、没有研究案例的做法？
    a: 博文里的评测和 Linux、Firefox 案例只作为官方结果引用，并链接原文。本文不写利用、复现或绕过方法。授权范围内的代码审查和本地扫描，用主线模型、Codex Security 和已有的防御向文章。
---

# Codex 用 GPT-6 Cyber 与 Daybreak Red：准入、和 Astra / Blue 的分工，以及安全研究边界

> 本文在线版：[codexguide.io/guides/codex-gpt-6-cyber-daybreak-red](https://codexguide.io/guides/codex-gpt-6-cyber-daybreak-red)

> 核对依据：OpenAI《[GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber)》（2026-11-05）和同页指向的系统卡入口。准入对照还参考了知识库里已有的 [Daybreak Blue 一文](./10-Codex-Daybreak-Blue申请开启与排障.md) 所引的帮助中心说明。本文作者没有 Daybreak Red 资格，没有在 API 或 Codex 里切换到 GPT-6 Cyber，也没有看到模型选择器里的实际名称。文中不写漏洞利用、复现条件或绕过方法。

适合要判断「这个模型跟我的 Codex 订阅有没有关系」的人：安全团队、已经在办 Daybreak 的组织管理员，以及只是看到新闻、担心自己的账号被换模型的开发者。

如果你的工作是给自己的仓库做审查、修补和本地扫描，先读[模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)和 [Codex Security CLI](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md)。那两篇覆盖的是普通订阅里就能用的能力。本文不替代它们。

## 先看结论：这不是普通订阅的默认模型

2026-11-05，OpenAI 发布 GPT-6 Cyber。官方对它的定位是：面向安全研究，在研究人员划定的范围内发现并核验漏洞，同时更稳定地留在该范围内。

和 Codex 日常使用直接相关的只有这几句：

- 它起初通过 **API** 和 **Codex**，提供给一部分已经获批的 **Daybreak Red** 客户。
- 官方写明随后会扩大到全部 Daybreak Red 客户，但没有给日期。
- 同一则说明里，**GPT-5.6 Cyber** 改为向全部 Daybreak Red 客户提供。
- Daybreak Blue 一侧，官方在扩大 **GPT-6 Astra** 的 alpha 访问，对象是更多组织和独立安全研究人员。这是 Blue，不是 GPT-6 Cyber。
- 博文没有把它写成 Plus、Pro、Business 或其他套餐的默认可选模型。

因此：模型列表里没有它，是当前政策下的正常情况，不是客户端坏了。本文没有资格做切换实验，不能描述菜单长什么样、配置文件里该写哪个模型 ID。博文使用的是产品名 GPT-6 Cyber，没有给出 `config.toml` 里的模型字符串。不要自己编一个 ID 写进配置。

## 官方发布了什么

下面只保留判断「要不要申请、它和现有工具怎么分工」所需要的产品事实。评测怎么做、案例怎么做，一律留在原文。

官方给出的能力对比，原文是这样说的：

- 在 ExploitGym 上，GPT-6 Cyber 为 48.5%，GPT-5.6 Cyber 为 32.1%。博文同时把这个差距写成大约 16 个百分点，以及 51% 的相对提升。
- 在一项看模型是否越出指定范围的对齐评测里，不带部署提示时，GPT-6 Cyber 在 99.93% 的测试中没有去动范围外的服务；带上该提示时为 100%。对照数字是 GPT-5.6 Cyber 的 94.49%（不带部署提示）。
- 在 Preparedness Framework 的网络安全分级上，官方把 GPT-6 Cyber 标为 Critical，并写明 GPT-5.6 Cyber 此前是 High。

官方研究案例的结果，同样只引用规模，不写做法：

- Firefox：81 个此前未知、被 Mozilla 标为高危的问题；另有 30 个已知问题被判定比原先报告的更严重。博文写 Mozilla 已经发布了其中许多修复。
- Linux：官方研究人员形成了 948 个提权利用；同一套研究流程中，GPT-5.6 Sol 是 166 个。博文还写了复现 1,724 个漏洞，并向维护者披露 304 项严重发现及补丁候选。

这些句子的作用，是说明官方为什么单设这个模型和单独的准入，不是一份可以照做的任务说明。完整设置在博文和它所链接的系统卡里。

博文还提到 Cisco、Calif、CodeRabbit 等团队在用，并引用了 Firefox 工程师的评价。各家内部分数和任务设计不转述到这里。

## Daybreak Blue、Daybreak Red 和主线 Astra

官方在同一篇里把三条线放在一起。结合 Daybreak 帮助中心已经写明的 Blue 范围，分工可以收成这张表：

| 路线 | 官方在 2026-11-05 博文里的分工 | 和普通 Codex 订阅的关系 |
| --- | --- | --- |
| 主线模型，例如 GPT-6 Astra | 已经可以做代码审查、漏洞分级和补丁开发 | 能不能选 Astra，看你的套餐、客户端和工作区，见[模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md) |
| Daybreak Blue | 给已验证的防御方，在核验漏洞和修复时减少不必要的拒绝 | 需要单独获批。个人申请通道、App 开关和 CLI `/daybreak` 见 [Daybreak Blue](./10-Codex-Daybreak-Blue申请开启与排障.md)。Blue 不是 GPT-6 Cyber |
| Daybreak Red 上的 GPT-6 Cyber | 在授权的安全测试里做更深的工作 | 起初只给一部分已获批的 Red 客户，在 API 和 Codex 中提供。不是 Blue 开关打开之后自动出现的模型 |

帮助中心原先写明：Red 需要单独审批，面向获批的企业和组织；个人申请通道申请的是 Blue，Blue 获批不包含 Red。2026-11-05 的博文没有改写这句话。它新增的是：新的使用者可以申请 Daybreak，而 GPT-6 Cyber 先给一部分 Red 客户。两条要一起读。不要把 Blue 申请步骤理解成「做完就能在 Codex 里选中 GPT-6 Cyber」。

博文还提到一个面向关键基础设施防御方的 Red 分组，以及面向资源有限的前线防御团队的 Daybreak 资助项目。分组的具体资格、申请表字段和资助条件，这篇博文没有展开。本文不补写。

## 谁能在 Codex 里用到它，资格从哪里看

按官方文字，同时满足下面几条，才进入「可能用到」的范围：

1. 组织已经是获批的 Daybreak Red 客户，而不只是有一个普通的 ChatGPT 或 Codex 订阅。
2. 在「起初只给一部分 Red 客户」这个阶段，你的组织属于这一部分。博文没有列出名单，也没有写如何查询自己是否在列。
3. 使用的入口是官方点名的 API 或 Codex。博文没有写网页版 ChatGPT 普通对话、也没有写一个公开的模型 ID。

还没有 Daybreak 的人和组织，官方把申请指到 Daybreak 计划。知识库里已经核对过的入口是 [chatgpt.com/cyber](https://chatgpt.com/cyber)。那里的个人流程是 Blue 的流程：付费套餐、高级账户安全、硬件密钥和身份验证。做完这些仍然不表示获得 Red，更不表示获得 GPT-6 Cyber。

已经有 Red、但在 Codex 里看不到这个模型时，本文无法代你排查菜单。作者没有这个资格。可以先确认的只有产品边界：看的是不是获批组织的账号、是不是 Red 而不是 Blue、以及是不是仍处在「一部分客户」的阶段。API 一侧，博文写明 Daybreak Red 的 API 访问默认要求 IP 允许列表，把请求限制在获批网络，例外很少。这是访问控制，不是模型效果开关。

扩大到全部 Daybreak Red 客户的时间，博文用的是 soon，没有日期。在那之前，不要按「所有 Red 客户今天都能选」来写内部文档。

## 和 Codex Security、Trail of Bits 插件怎么分工

三件事经常被摆到一起，覆盖的问题不一样：

| 你要做的事 | 用哪篇 | 不归本文管的部分 |
| --- | --- | --- |
| 在本机用官方扫描器看自己的仓库，并把结果接到 CI | [Codex Security CLI](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md) | 不需要 GPT-6 Cyber |
| 用第三方 Trail of Bits 插件做补丁和回归检查 | [Trail of Bits 插件](../09-MCP与外部工具/12-Codex安装Trail-of-Bits插件-patching-bugs与regression-hunt.md) | 那是社区插件的安装和用法，不是官方模型准入 |
| 判断 GPT-6 Cyber 能不能出现在自己的 Codex 里 | 本文 | 不写研究作业怎么做 |

主线模型加上 Daybreak Blue，官方已经把「审查、分级、补丁、减少防御场景里的误拒」放在这两条线上。多数仓库维护不需要 Red。

## 使用边界：留在授权范围内

官方把「留在研究人员设定的范围内」写成这个模型的产品要求，不是一句口号。博文里和使用者有关的边界是：

- 任务范围由研究人员设定。模型被要求留在这个范围内，遵守限制，并如实报告结果。
- 官方建议对高风险工作流使用沙箱、动作复核和人工监督。这和 Codex 里原有的沙箱、审批是同一类控制：模型变了，不会自动扩大你授予它的权限。
- 官方同时写了误用监测、对高风险行为的拦截，以及关键基础设施场景下的额外限制。这些控制会挡住一部分请求。博文明确说，更高的拦截率并不总是更好，因为正当的防御工作也会用到相邻的技术；他们的目标是拦住有害协助，而不是让正当研究全部失败。
- 使用政策仍然有效。Daybreak 不是「对任意系统都可以做测试」的许可。对象必须是你有权测试的系统。这一点和 Blue 帮助中心的写法一致。

本文到此为止。不提供提示词范例，不描述官方案例的环境、版本和操作，也不讨论怎样让安全检查失效。需要案例细节的人，直接读[官方博文](https://openai.com/index/introducing-gpt-6-cyber)和它链接的系统卡。

如果你在授权工作里被安全策略拦住，Blue 一文写了防御向请求的排查顺序，以及不要把密钥和未授权目标发给支持人员。那个排查不适用于「我想使用 GPT-6 Cyber 但没有 Red」。

## 参考资料

- [GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber)（2026-11-05）
- [Daybreak 申请入口](https://chatgpt.com/cyber)
- [OpenAI Daybreak - Trusted Access for Cyber overview](https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview)
- [Codex Daybreak Blue 怎么用](./10-Codex-Daybreak-Blue申请开启与排障.md)
- [Codex 模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
