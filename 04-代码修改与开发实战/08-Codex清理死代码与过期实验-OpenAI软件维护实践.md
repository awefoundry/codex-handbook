---
id: dead-code-cleanup-software-maintenance
title: Codex 清理死代码与过期实验：OpenAI 用 GPT-6 系列合并 1,400+ 个维护 PR 的方法与 Prompt
seo_title: Codex 清理死代码：OpenAI 合并 1,400+ 维护 PR 的方法与 Prompt
description: OpenAI Core Experimentation 用 Codex 合并了 1,400 多个维护 PR，删除 80 万行以上代码。本文拆解清理死代码、审计过期实验、修 flaky 测试和给 CI 提速时用的 prompt，对比 GPT-6 Astra 与 GPT-6.1 Sol 的成本，并说明怎样从自己仓库的一个小任务开始试。
lede: 维护债会跟着交付速度一起涨。OpenAI 用短 prompt + 证据 + 小 PR 的方式，把死代码和过期实验清成可审查的批量维护。
url: /guides/codex-dead-code-cleanup-software-maintenance
status: draft
section: guides
category: D-project-dev
topic: 代码修改与开发实战
content_type: 案例
source_tag: 官方功能
entry_tags: [App, CLI, Cloud]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6-astra, gpt-6.1-sol]
official_ref: https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family
keywords: [Codex 清理死代码, Codex 软件维护, 过期实验清理, flaky 测试, CI 提速, GPT-6.1 Sol 成本]
related: [model-reasoning-effort, goal-mode-long-running-work]
faq:
  - q: 宽泛地说「帮我清死代码」会不会误删线上路径？
    a: 会有风险。官方团队强调每处删除都要有证据（生产剖析、功能开关配置、Slack/历史 PR 等），并保留 kill switch、标为 Permanent 的开关等运维护栏；最终仍靠人工审查。宽泛 prompt 适合 GPT-6 Astra 这类能主动取证的模型，不等于可以跳过 review。
  - q: 过期实验清理时，Codex 可以直接改 Statsig 线上配置吗？
    a: 官方示例的全仓审计 prompt 明确要求：只出报告、不修改线上配置或服务。清理以小草稿 PR + 控制台链接为准，线上开关变更仍走你们原有流程。
  - q: 为了省钱，是否一律用 GPT-6.1 Sol Medium？
    a: 官方同任务对比里，Sol Medium 发现数更少、单条更便宜；Sol Ultra 用约 14% 的 API 成本拿到 Astra Ultra 约 92% 的发现。先在一个子目录上对比模型与 effort，再决定扩到全仓。
---

# Codex 清理死代码与过期实验：OpenAI 用 GPT-6 系列合并 1,400+ 个维护 PR 的方法与 Prompt

> 本文计划路径：[codexguide.io/guides/codex-dead-code-cleanup-software-maintenance](https://codexguide.io/guides/codex-dead-code-cleanup-software-maintenance)

> 核对依据：OpenAI 开发者博客 [Maintaining software with the GPT-6 family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family)（Rodrigo Roim / Core Experimentation，页面日期 2026-10-14）。文中数字与 prompt 结构以该文为准；「我的用法」是落地建议，不是官方规定。

交付越快，维护债涨得也越快：没人碰的路径、已经定胜负却还挂着的实验、时绿时红的 flaky 测试、越跑越慢的 CI。OpenAI Core Experimentation 团队在这篇博客里说明：他们怎样用 **GPT-6 Astra** 和更便宜的 **GPT-6.1 Sol**，把「找清理机会 → 收集证据 → 准备可审查改动」交给 Codex，并在两周兼职节奏里合并了 **1,400+** 个维护 PR。

本文不复述博客全文，只抽出**可复用的方法、可复制的 prompt，以及必须人工守住的风险边界**。

## 这篇官方博客讲了什么

作者 Rodrigo Roim 所在团队负责公司内实验平台相关软件：从前端改动到模型服务效率。博客的主线是三件事：

1. **死代码清理**：从「先告诉模型去哪查」演进到「一句宽泛请求 + 模型自己取证」。
2. **过期实验 / 特性开关**：比死代码更难——代码可能仍在跑，只是配置已成常量；需要对照 Statsig 等线上配置、git 历史，并保留运维护栏。
3. **成本与规模**：同一审计任务上对比 GPT-6 Astra Ultra、GPT-6.1 Sol Ultra、GPT-6.1 Sol Medium；再用短 prompt 修 flaky、压 CI。

博客给出的量级结果（后文逐项对照原文）：合并 **1,400+** 个维护 PR，删除 **800k+** 行代码；某服务容器镜像 **3.31GB → 1.72GB**（约 **48%**）；去掉约 **400** 个视觉快照变体；一批 CI 优化后，中位完成时间约 **10 分钟 → 4.5 分钟**，P90 约 **12.5 分钟 → 6 分钟**。

模型名以博客为准：主推 **GPT-6 Astra**（处理宽泛、跨源取证）与 **GPT-6.1 Sol**（同工作流、更省成本）。文中对比基线曾提到早期用 **GPT-5.6 Sol** 写静态分析脚本；那是历史对照，不是本文推荐你现在去选的型号。

## 清理死代码：从「指定范围」到「宽泛 prompt + 证据」

### 以前为什么难

博客回顾：Agent 编程普及前，团队常靠复杂静态分析 + 运行时日志找死代码。即便如此，误删仍会发生——反射会骗过静态分析；某条「看起来没用」的路径，将来可能被当成事故缓解开关重新打开。

有了较强模型之后，作者先用**更窄**的方式：指定调查区域、写清验收标准，让模型写静态分析并删死代码。这类定向 prompt 比维护一整套静态分析系统更轻，可靠性接近。

### GPT-6 Astra：一句很「糊」的请求也能跑通

拿到 GPT-6 Astra 后，他们想试：模型能不能从**更宽泛**的请求出发，自己决定查哪里、要什么证据。博客原文保留了那段带笔误的英文 prompt（此处按原文结构照录，便于你复制）：

```text
Can you help identify and clean up dead code in the repo please, feel free to check slack,
statsig [a feature flag and experimentation platform we use], or any other source you need to
confirm that things are indeed no longer being used and can be cleaned up or simplified
```

Astra 的做法（博客描述）包括：翻历史 PR、看 Slack 线程、查内部项目跟踪、读生产性能剖析表确认被删行从未被命中，并为每次删除写清理由——审查因此变快。

五个工程师用该 prompt 的变体扫多个仓库，**兼职约两周**（同时做别的项目），合并 **1,400+** 个 PR，删除 **800k+** 行。审查按项目上下文分发给相关团队。可量化收益示例：

| 结果 | 数字（博客） |
|---|---|
| 某服务容器镜像 | 3.31GB → 1.72GB（约 48%） |
| 测试套件视觉快照变体 | 去掉约 400 个 |

**我的用法：** 不要一上来就对整个 monorepo 丢这句。先选一个你熟悉、有监控/开关后台可查的子目录；要求「每个删除附证据链接或命令输出」；合并前按服务 owner 拆小 PR。宽泛 prompt 依赖模型会主动取证——若你用的配置取证能力弱，先改回「指定目录 + 验收标准」。

## 审计过期实验和特性开关：拆解 `/goal` 全仓 prompt

### 为什么比死代码难

过期实验的代码**未必**未执行：它可能仍在生产路径上跑，或依赖随时会变的资格判定。静态分析容易大量漏报。团队过去用确定性静态分析 + 数据库查询，并用当时最强模型改进脚本，仍有很多假阴性。

### 第一步：小范围、带护栏的清理 prompt

作者不确定怎么开场，先和 Astra 头脑风暴，让它写出可在新会话里试的短 prompt（博客原文）：

```text
Find and remove substantial dead code associated with stale, constant Statsig gates/configs or
abandoned experiments in projects {A} and {B}. Verify live Statsig configuration and check git
history and overlapping PRs. Preserve production behavior, operational safeguards and
gates/configs intended as killswitches or similar. Ignore SDK fallbacks and local overrides.
Create one small draft PR per cleanup, linking its Statsig configuration console link in the
summary.
```

要点（中文归纳，结构与原文一致）：

1. **范围**：指定项目 `{A}` / `{B}`，只动「过期、常量、已放弃实验」相关的大块死代码。
2. **取证**：核对**线上** Statsig 配置、git 历史与重叠 PR。
3. **护栏**：保留生产行为、运维保障，以及用作 **kill switch** 一类的开关；忽略 SDK fallback 与本地 override。
4. **交付形态**：每次清理一个**小草稿 PR**，摘要里挂 Statsig 控制台链接。

Astra 会按护栏准备带证据的改动；作者在 PR 上评论，再让它吸收反馈，并写出可扫全仓的新 prompt，同时解决「候选太多、如何排序」的问题。

### 第二步：全仓 `/goal` 审计——只出报告，不改线上

Astra 建议的全仓 prompt 以 `/goal` 开头（博客有所删节，关键骨架如下）：

```text
/goal Find every stale, constant, abandoned, or fully shipped Statsig gate, config, experiment,
and layer present in this entire repository that can safely be removed with no production
changes. Audit all Statsig projects and inventories, not just objects labeled stale.
Find indirect usages through enums, constants, wrappers, aliases, schemas, dynamically assembled
names, and cross-service consumers. Reconcile every production-referenced constant; do not stop
after producing a conservative shortlist.
Consider each object's cloud resource usage, including CPU. Use production telemetry and
profiles where available to identify expensive dead checks.
[Omitted for brevity: detailed instructions, generated by Astra, on verifying production
behavior, prioritizing older objects, preserving intentional safeguards, and interpreting SDK
fallbacks.]
Produce a markdown report grouping all verified candidates into parallelizable ownership/file
workstreams, including production values, evidence, owners, callsites, and observed evaluation
or CPU costs if available.
Do not modify live configurations or services.
```

结构可以记成五层：

| 层 | 作用 |
|---|---|
| 目标 | 找可安全移除、且**不改变生产行为**的过期/常量/已放弃/已全量上线对象 |
| 覆盖面 | 审计**全部** Statsig 项目与清单，不只看被标成 stale 的 |
| 间接引用 | enum、常量、wrapper、别名、schema、动态拼名、跨服务消费 |
| 优先级 | 结合云资源用量与 CPU；用生产遥测/剖析找「昂贵的死检查」 |
| 输出与禁区 | Markdown 报告按 owner/文件分成可并行工作流；**禁止修改线上配置或服务** |

报告出来后，作者用自家埋点核对 CPU 成本：排在前面的几项是多年没人标成 stale、却是明显效率收益的实验。大项人工复核后，再推进全量清理，最终去掉**数百**个实验与特性开关（博客用语：hundreds）。

**我的用法：** 把 `{A}/{B}` 换成你真实的实验平台项目名；没有 Statsig 就改成 LaunchDarkly / Unleash / 自研开关后台，但**保留**「核对线上配置 + 小 PR + 控制台链接 + 不改线上」四条。全仓审计优先用 Goal 类长任务入口（见知识库 Goal 模式文），先拿报告再开刀。

## 成本对比：Astra Ultra、Sol Ultra、Sol Medium

为比较模型在**同一套过期实验清理工作流**上的表现，作者用同一 prompt，让 Codex 审计某仓库中特定子目录（覆盖 **6,000+** 文件、约 **100 万** 行，含 Python / TypeScript / Go / Rust），再人工验收发现。标准 API 计价，费用含研究用 subagent 以及 Codex 为推进 goal 自动跑的后续轮次。

| 组合 | API 成本 | 验收通过的发现数 | 单条成本 |
|---|---|---|---|
| GPT-6 Astra Ultra | $109.06 | 142 | $0.77 |
| GPT-6.1 Sol Ultra | $15.12 | 131 | $0.12 |
| GPT-6.1 Sol Medium | $5.27 | 86 | $0.06 |

博客结论：

- **GPT-6.1 Sol Ultra** 拿到 Astra Ultra **约 92%** 的发现数，API 成本约为其 **14%**。
- **Sol Medium** 通过数更少，但更便宜。
- Ultra 档上，多数差异来自「被其他开关当作依赖的常量特性开关」：Astra 能抓到，Sol 有时漏。识别这类误差模式后，可以**改 prompt 补洞**，让更便宜的配置逼近贵模型；新模型发布后要**重测 prompt**，旧补丁可能过时。

**我的用法：** 先在一个子目录用 Sol Medium 试跑 → 抽样人工验收 → 同一范围用 Sol Ultra / Astra Ultra 各跑一次，只比较「你愿意合并的发现」，不要只比原始条数。成本数字会随定价与自动跟进轮次变化，上表只作博客公布日的对照。

## 另外三段可以照抄的 prompt

博客「Other ideas to try」建议：先用 **GPT-6.1 Sol Medium** 试；若结果有希望，再提高 effort 做更大审计。

### 1）修 flaky 测试

```text
/goal Look at all recent CI runs to find flaky tests. For each flaky test, try a fix and if
successful put up a PR. Your job is to find clear fixes to simple issues, not to exhaustively
fix every flaky test.
```

边界写得很清楚：**只找简单问题的明确修复**，不要求穷尽所有 flaky。

### 2）回放对比一条 AGENTS.md 指令

```text
Look through my recent Codex sessions and find one AGENTS.md instruction that appears to have
misdirected an agent or caused unnecessary work. Choose the original session prompt where that
happened. Replay that same prompt twice from the same repository snapshot and model:
1. With the current AGENTS.md instruction unchanged.
2. With only that one instruction removed or fixed.

Compare task quality, agent behavior, tool calls, token usage, runtime, and cost. Show the
instruction and whether updating it helped.
```

适合排查「仓库说明本身在带偏模型」——改说明前先做对照实验。

### 3）给 CI 降耗点子排序

```text
What ideas do you have to relieve CI load in this repository? List your ideas in a table and
rank all of them by estimated CI minutes saved per day based on this repo's CI run history
```

官方跟进结果：落地约 **30** 个 CI 优化 PR 后，**中位** CI 完成时间约 **10 → 4.5 分钟**，**P90** 约 **12.5 → 6 分钟**。另一次后续修复：补上缺失 mock 后，含 **63** 个测试的 resolver 套件从 **592.6 秒** 降到 **29.8 秒**（约 **95%**），**63** 个测试全部保留。

## 在自己的仓库落地：小任务 → 子目录 → 全仓

博客收尾建议可以直接当清单用：

1. **从一个小维护任务开始**：一段明显未用代码、一个过期特性开关，或一个 flaky 测试。让 Codex 找到实例、收集证据、提出**小草稿 PR**。
2. **同一小任务上对比模型与 effort**：更便宜的配置往往已经够用。
3. **放大到子目录或边界清晰的项目**；每轮把 code review 意见写回下一版 prompt。
4. **确认模型表现稳定后**，再扩到全仓。
5. **用埋点 / 报告做优先级**：大仓库里 GPT-6 系列能找出大量优化点，没有优先级会被淹没；博客强调 instrumentation + 上述 prompt 技巧帮助排序。有些提案的复杂度高于预期收益，**优先级与度量**仍是工作流的一部分。

**我的用法（最小闭环）：**

1. 选一个有 owner、有开关后台或监控的服务目录。  
2. 先跑「只读报告」版（全仓 `/goal` 那种禁改线上的骨架），人工标 P0/P1。  
3. 每个 P0 开独立小 PR，摘要贴证据与控制台链接。  
4. 合并 3～5 个后再决定是否提高 effort 或换 Astra 扫下一层。

## 风险边界：哪些删除必须人工确认

官方案例里最值得单独记住的一条：

几年前有人为方便内测，加了一个 Statsig 特性开关，用**一行 Python** 把该开关映射到**所有**其他新特性相关开关。它埋在几百行类似映射中间，看起来不起眼。Astra 发现它造成显著 CPU 扇出，估算出受影响主服务约 **0.42%** CPU 节省——但因为该开关在管理控制台被标成 **「Permanent」**，且仍可能有运维用途，模型**没有擅自删掉**，而是升级给人工审查。审查后团队才移除。

由此可归纳的硬边界（均来自博客表述，不是额外发挥）：

| 必须人工确认 | 原因 |
|---|---|
| Kill switch / 事故缓解路径 | 「现在没用」≠「出事时不能用」 |
| 控制台标记为 Permanent（或你们的等价标签） | 标记本身就是人为意图信号 |
| 被其他开关依赖的常量 flag | 便宜模型更容易漏；删错会影响整棵依赖树 |
| 仅靠静态分析、没有生产剖析/配置佐证的删除 | 反射、动态拼名、跨服务引用会制造假阳性 |
| 任何改动线上实验平台配置的操作 | 审计 prompt 明确：报告可以，**不要改 live configurations or services** |

合并 1,400+ 个维护 PR 带来了更快测试、更小镜像、更低 CPU 等收益；博客同时承认：部分提案的复杂度高于收益，需要优先级与度量来过滤。

## 接下来读什么

- 模型与推理强度怎么选 → 知识库 `10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md`（`/guides/codex-model-reasoning-effort`）
- 用 Goal 模式跑长审计 → `11-自动化与高级工作流/05-Codex使用Goal模式运行长任务.md`（`/guides/codex-goal-mode-long-running-work`）
- 修复可复现 Bug 的最小补丁习惯 → `04-代码修改与开发实战/04-修复一个可复现Bug-让补丁只解决当前问题.md`（`/guides/codex-xiu-fu-ke-fu-xian-bug`）

## 参考资料

- [Maintaining software with the GPT-6 family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family)（Rodrigo Roim，Core Experimentation，2026-10-14）
- OpenAI Developers 转发讨论：https://x.com/OpenAIDevs/status/2111213093577691337
- 作者原帖：https://x.com/rrroim/status/2111171952849334585

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
