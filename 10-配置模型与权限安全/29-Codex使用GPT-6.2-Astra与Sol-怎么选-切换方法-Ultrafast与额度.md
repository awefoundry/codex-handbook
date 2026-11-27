---
id: codex-gpt-6-2-astra-sol
title: "Codex 用 GPT-6.2 Astra 和 Sol（更新）：11 月 26 日额度更正后同样的活更吃额度，Astra 约快 40%、Sol 约快 25% 触顶，怎么看用量、怎么省"
seo_title: Codex GPT-6.2 Astra 与 Sol：怎么选、怎么切换、Ultrafast 与额度
description: GPT-6.2 Astra 和 Sol 已在 Codex 上线。本文按官方文档说明两款各适合什么任务、哪些套餐和入口能用、App 与 CLI 怎么切换、Fast 与 Ultrafast 怎么选，以及额度和 credits 怎么算，Enterprise 和 Edu 管理员要先做什么。
lede: 写代码先试 GPT-6.2 Sol。跨服务排查再上 Astra。2026-11-26 的计费更正之后，同样的活比上周更吃套餐用量，5 小时估算以 Usage 为准。
url: /guides/codex-gpt-6-2-astra-sol
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [App, CLI, ChatGPT Work]
difficulty: 基础
order: 29
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-18
date_modified: 2026-11-27
verified_on: 2026-11-27
tested_cli_version: 0.169.1
models: [gpt-6.2-astra, gpt-6.2-sol, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/models
keywords: [Codex GPT-6.2, GPT-6.2 Astra, GPT-6.2 Sol, Ultrafast, gpt-6.2-sol]
related: [model-reasoning-effort, usage-limits-credits, codex-gpt-6-1-terra, codex-prompting-gpt-6-2, codex-banked-reset, model-at-capacity-usage-reset]
howto: true
faq:
  - q: 哪些套餐能在 Codex 里用 GPT-6.2 Astra 和 Sol？
    a: Changelog、What's new 和 Pricing 的 Feature availability 写的是 Plus、Pro、Business、Enterprise 和 Edu，入口是 ChatGPT Work（网页、手机、桌面）以及 Codex app 和 CLI。发布公告的可用性一段没有写 Business。Enterprise 和 Edu 默认关闭，要管理员先打开。普通 Chat 里不选这两款，要到 Work。
  - q: Codex CLI 怎么切到 GPT-6.2 Sol？
    a: 官方 Models 页写 codex --model gpt-6.2-sol，或 codex exec -m gpt-6.2-sol，交互会话里用 /model。2026-11-18 在 Linux 的 codex-cli 0.169.1 上，--help 能看到 -m/--model，看不到 /model。未登录时启动摘要会打印 gpt-6.2-sol，随后请求因 401 结束，没有模型回复。
  - q: Ultrafast 和 Fast 差在哪，谁能开？
    a: 两者都是速度档，比 Standard 更快，也更吃额度。Fast 对两款 GPT-6.2 都可用，套餐内含和 credits 都按 2 倍计。Ultrafast 的公开资格是 Pro 200 美元只用 Sol，Pro 500 美元两款都能用；Enterprise 和 Edu 要工作区另外打开权限，推理驻留只支持美国。
  - q: IDE 扩展能选 GPT-6.2 吗？
    a: 2026-11-18 的 Models 详情和 Pricing Feature availability 把 Codex 入口写成 App 和 CLI，没有把 IDE 扩展列进去。同一页的配置示例 model = "gpt-6.2-sol" 标明是给 app 或 CLI；如果这份配置还要给 IDE 扩展用，页面建议改选每个客户端都能用的模型，举例是 gpt-6.1-sol。以扩展里的模型菜单为准。
---

# Codex 用 GPT-6.2 Astra 和 Sol（更新）：11 月 26 日额度更正后同样的活更吃额度，Astra 约快 40%、Sol 约快 25% 触顶，怎么看用量、怎么省

> 本文在线版：[codexguide.io/guides/codex-gpt-6-2-astra-sol](https://codexguide.io/guides/codex-gpt-6-2-astra-sol)

> 核对依据：模型与额度仍按 [Pricing](https://learn.chatgpt.com/docs/pricing)、[What's new 索引](https://learn.chatgpt.com/docs/whats-new)、[GPT-6.2 What's new](https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol)、[Models](https://learn.chatgpt.com/docs/models)、[Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) 和 [Changelog](https://learn.chatgpt.com/docs/changelog)。2026-11-27 再次打开这几页：Pricing 的 5 小时本地消息估算仍是 Astra 6–50、Sol 17–180（Plus 与 Standard Business），页面没有计费更正的说明。Changelog 的 HTML 能打开，最新日期见到 2026-11-24，没有这次更正；同一地址加 `.md` 返回 404。计费更正只来自 X 上 @thsottiaux 的两则帖子，见下文，那不是官方文档。2026-11-18 在 Linux 上用 `@openai/codex@0.169.1` 核对过 `-m` 的记录仍留在「怎么切换」一节，这次没有重跑 CLI，也没有登录。

2026 年 11 月 17 日，Changelog 把 GPT-6.2 Astra 和 GPT-6.2 Sol 放进 ChatGPT Work 和 Codex。Astra 面向最难的项目，Sol 面向日常编码、写作和多步骤工作。Changelog 同时写：用 GPT-6.2 Sol，同一份付费套餐能比 GPT-6.1 Sol 完成更多任务。这句在 2026-11-27 的 Changelog 里还在。它和下面「比上周更吃额度」不是同一次比较。

下面仍按这几件事组织：谁能用、在哪里切换、两款各交给什么任务、Fast 和 Ultrafast 怎么算、credits 和 5 小时估算怎么读、Enterprise／Edu 管理员要先打开什么。11 月 26 日的计费更正单独成节，不改这几件事的官方分工。模型搭配和推理强度的完整选择表见 [Codex 模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。用量面板怎么读见 [Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

发布公告里还列出了多项基准和安全评估。本文不把那些分数写成结论，需要看分数时直接读 [原文](https://openai.com/index/introducing-gpt-6-2-astra-sol/)。

## 先说结论：写代码先试 Sol，难题再上 Astra

- **日常编码、审 PR、按反馈改代码、把几份材料收成一份计划**：先用 **GPT-6.2 Sol**。API 模型 id 是 `gpt-6.2-sol`。
- **最难的项目**：换 **GPT-6.2 Astra**（`gpt-6.2-astra`）。What's new 的例子是跨服务排查 bug、按模板把报告做成幻灯片、对照多份资料核对结论。
- **写作、看图、在应用里操作、范围很小的修复**：仍可以先试 [GPT-6.1 Terra](./14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md)。
- **Enterprise 和 Edu**：两款默认关闭。成员在菜单里找不到时，先让管理员在工作区模型设置里打开，不要在配置里写一个菜单里没有的模型名。
- **普通 Chat 里没有这两款**。What's new 写明：要在 ChatGPT 里用，请打开 Work。
- **2026-11-26 的计费更正之后**，同样的活会比上周更多消耗套餐用量。文中和 Pricing 页的 5 小时估算可能没有反映这次更正，以设置里的 Usage 为准。细节在下一节。

## 11 月 26 日的额度更正

这一节的事实来自 X 帖子，不是官方文档。2026-11-27 打开的 Pricing、What's new 和 Changelog 都还没有对应说明。

2026-11-26 02:50:10 UTC（页面显示 2:50 AM · Nov 26, 2026，北京时间 10:50），账号 [@thsottiaux](https://x.com/thsottiaux/status/2125784147889393806)（页面显示名为 Tibo，简介是 “Codex & ChatGPT @OpenAI”）发帖。帖子原文的要点是：

- GPT-6.2 上线时出现计费错误，错误地给大多数用户的 GPT-6.2 Astra 和 Sol 用量打了折扣。现已更正。
- 更正之后，同样的活会更多地消耗套餐用量。
- 对比上周，达到限额的速度 GPT-6.2 Astra 快 40%，Sol 快 25%。帖子用的比较基准是 “Comparing to last week”。
- 用量仍应比 6 Astra 和 6.1 Sol 更耐用。帖子写的是 “go further in usage compared to 6 Astra and 6.1 Sol”。
- 其他模型没受影响。
- 不会对过去的用量补收差额。
- 作为道歉，给 Go、Plus、Pro 和 Business 的所有人各补发一次 banked reset。

同一天 07:26:16 UTC（页面显示 7:26 AM · Nov 26, 2026，北京时间 15:26），同一账号另发一帖，正文是 “Banked reset is online”：<https://x.com/thsottiaux/status/2125853628250599730>。打开这页时没有看到它引用前一则的 status id，所以这里只记成同一天的后续说明。banked reset 在设置里怎么看、什么条件下能兑换，见 [额度重置怎么用](./32-Codex额度重置怎么用-banked-reset在哪看怎么兑换与刷新时间变化.md)。那篇按帮助中心整理，帮助中心本身没有写这次道歉补发。

截至 2026-11-27 核对：

- [Pricing](https://learn.chatgpt.com/docs/pricing) 的 5 小时本地消息估算仍是 GPT-6.2 Astra 6–50、GPT-6.2 Sol 17–180，Plus 与 Standard Business 两列相同。页面没有这次更正的说明。
- [What's new](https://learn.chatgpt.com/docs/whats-new) 和 [GPT-6.2 What's new](https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol) 没有这次更正。
- [Changelog](https://learn.chatgpt.com/docs/changelog) 的 HTML 里，日期最新见到 2026-11-24，搜不到这次计费错误。`https://learn.chatgpt.com/docs/changelog.md` 返回 404。
- 帮助中心 [Managing usage with GPT-6 Astra](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) 和 [How resets work in Codex](https://help.openai.com/en/articles/20001498-how-resets-work-in-codex) 也没有这则更正。用帮助中心搜索 “GPT-6.2 billing mistake Astra”，返回页里没有一篇讲这件事的文章。

因此：文中和 Pricing 页的 5 小时估算可能没有反映这次更正，以设置里的 Usage 为准。本文不把 6–50、17–180 按 40% 或 25% 折算成新的条数。帖子里的两个百分比只描述「对比上周、达到限额的速度」，不是本文算出来的消息条数。

用量面板怎么读，见 [Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。界面写的是容量满还是额度用尽，见 [容量不足与额度重置排查](../15-故障排查与常见问题/01-Codex模型容量不足与额度重置排查.md)。

## 谁能用、在哪些入口能用

按 Changelog、What's new 和 Pricing 的 Feature availability：

| 项目 | 说明 |
|---|---|
| 套餐 | Plus、Pro、Business、Enterprise、Edu |
| Work | 网页、手机、桌面 |
| Codex | **App 和 CLI**。Models 详情卡写的也是 App and CLI |
| 普通 Chat | 不在 Chat 里选。打开 Work |
| Enterprise／Edu | **默认关闭**。管理员在工作区模型设置里打开后，成员还要有 Work 或 Codex 的入口权限 |
| API | 模型 id 为 `gpt-6.2-astra`、`gpt-6.2-sol` |

有一处官方说法不一致：发布文的可用性一段写的是 Plus、Pro、Enterprise 和 Edu，没有提 Business。Changelog、What's new 和 Pricing 都写了 Business。本文按后三处写。你的账号能不能用，以模型菜单里有没有这两款为准。

Models 页的详情卡还写了 Codex 里的默认上下文：Astra 是 272,000 token，Sol 是 500,000 token。同一页另写，两款都支持最多 100 万 token 的上下文窗口，更长的窗口要在 `config.toml` 里设置 `model_context_window`。本文没有改过这个字段，也没有一份写好数值的示例配置。

### IDE 扩展先别当成已经支持

Pricing 的 Feature availability 和 Models 详情卡都没有把 IDE 扩展列进 GPT-6.2 的 Codex 入口。Models 页 IDE 面板只说用输入框下方的模型切换器选择**当前可用**的模型，没有点名 GPT-6.2。

配置一节写得更直接：示例 `model = "gpt-6.2-sol"` 是给 **app 或 CLI** 的。如果同一份配置还要给 IDE 扩展用，页面要求改选每个客户端都能用的模型，举例是 `gpt-6.1-sol`。扩展里看不到 GPT-6.2 时，以菜单为准，不要靠本地配置硬切。

### Enterprise 和 Edu 要管理员先开

[Workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability) 的 GPT-6.2 一节写明：

- 两款在发布时**默认关闭**。
- 管理员在工作区模型设置里打开后，成员还要能进入 ChatGPT Work 或 Codex，才能在那边选中模型。
- 工作区里的模型设置**不会自动**作用到桌面端 Codex、CLI、IDE 扩展、Codex cloud 或 API。每个入口单独确认。
- Ultrafast 是**另一项权限**，默认也是关的。符合条件的工作区所有者可以给指定成员或整个工作区打开。细节见下一节。

同一页还写了推理和速度的上限可以按模型设置：打开 Admin Console，进入 Workspace settings，再进入 Models；选工作区默认或某个自定义角色，点支持模型旁边的齿轮，设置该模型的最高推理档和速度。起始默认和最高限制是两件事。本文没有 Enterprise 工作区，没有走过这个界面。

What's new 还写了 Work 新对话的默认值：支持的个人套餐上，新 Work 对话默认是 Sol、推理强度 Light；已经开放模型的 Enterprise 工作区默认是 Sol、Medium。看到 Power 滑杆时，打开 Advanced 再选具体模型和推理强度。这是 **Work 新对话**的默认，不要直接当成 Codex 会话已经帮你选好。

## 怎么切换：App 模型选择器、CLI 的 /model 与 codex -m gpt-6.2-sol

### 桌面端和 Work

Models 页写：在输入框下方的模型和推理控件里选可用模型。如果看到的是 Power 滑杆，打开 **Advanced**，再选具体模型，例如 GPT-6.2 Astra。滑杆往 Smarter 是更深的推理，往 Faster 是更快、更省的工作。

Speed 页写速度档的位置：Work 网页或 Codex 桌面端，点输入框底部模型或推理选择器上的闪电。账号能用 Ultrafast 时，闪电打开速度菜单；如果只有 Standard 和 Fast，点闪电就在两者之间切换。高级选择器里有 **Speed**。手机上的 Work 在模型选择器里调速度。

本文没有桌面 App，没有这些菜单的新截图。

### CLI

官方 Models 页给的命令：

```bash
codex --model gpt-6.2-sol
codex exec -m gpt-6.2-sol "Review the current changes"
```

交互会话里用 `/model` 切换模型或推理强度。想长期默认，同一页的示例是：

```toml
model = "gpt-6.2-sol"
```

这行写在桌面端、CLI 和 IDE 扩展共用的 `config.toml` 里，但页面把这个示例限定为 **app 或 CLI**。要和 IDE 扩展共用时，改成扩展里也能选到的模型。

2026-11-18 在 Linux 上的核对：

- `codex --version` 输出 `codex-cli 0.169.1`。
- `codex --help` 和 `codex exec --help` 都有 `-m, --model <MODEL>`。
- 这两份 help **没有**列出 `/model`、`/fast`、`/ultrafast`。斜杠命令的写法来自 Models 和 Speed 文档。本文没有登录，没有进入交互会话，所以没有亲眼看到 `/` 菜单。
- 独立 `CODEX_HOME`、未登录时，`codex exec -m gpt-6.2-sol` 和 `-m gpt-6.2-astra` 的启动摘要都打印了对应的 `model:`。换成一个不存在的 id 时，CLI 会警告 `Model metadata ... not found`；这两个 id 没有这句警告。
- 两次请求都因 **401 Unauthorized**（缺少认证）结束，**没有模型回复**。启动摘要能打印模型名，只说明 CLI 接受了这个参数，不说明账号已经有资格。

同一天的 Changelog 还有一条 Codex CLI 0.169.1，正文写的是 No verified release highlights。模型上线写在另一条「GPT-6.2 Astra and GPT-6.2 Sol in Work and Codex」里，不要把 0.169.1 的发布说明当成模型功能清单。

登录之后，新开一个会话，用 `/status` 看实际模型。本文没有登录，没有 `/status` 输出。

## Astra 和 Sol 各适合什么任务

What's new 和 Models 页的分工：

| 模型 | 官方定位 | 官方举例 |
|---|---|---|
| GPT-6.2 Astra | 最难的项目、复杂推理 | 跨服务排查：给出失败的流程，让它追原因、改代码、跑受影响的测试。把报告做成符合团队版式和文风的幻灯片。对照多份资料，标出证据不一致的地方 |
| GPT-6.2 Sol | 日常编码、写作、要分几步做的工作 | 审一则 pull request，标出要作者处理的问题。按审稿意见改实现并跑相关测试。把会议记录收成项目简报：决定、下一步、还没定的问题 |

Changelog 用了同一组编码例子：Astra 适合在现有代码库里实现并测试一处跨代码的改动，或把报告做成遵循模板的幻灯片；Sol 适合日常编码、写作和多步骤流程。

这些是官方示例，不是本文跑出来的结果。提示词怎么写给 GPT-6.2，见 [Codex 提示词怎么写给 GPT-6.2](../02-核心概念与任务方法/10-Codex提示词怎么写给GPT-6.2-推理强度-子代理-视觉参考与精简AGENTS.md.md)。

Models 页对推理强度的建议：GPT-6.2 Astra 和 Sol 都从**客户端当前档**起步，再按任务加减。Luna 从 High 起步，GPT-6 Astra 从 Light（配置里写 `low`）起步。八组「模型 + 推理强度」的起步组合在 [模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

## Fast 与 Ultrafast：谁能开、倍率是多少、数据驻留限制

先把三个名字分开：

- **推理强度**（Light／Low、Medium、High、Extra High）决定这一题想多久。
- **Fast／Ultrafast** 是速度档，用更多额度换更快出 token。
- **Ultra** 是另一件事：让子代理并行处理能拆开的工作。它不是 Ultrafast。

下面的倍率来自 Pricing 的 Speed multipliers，相对**同一模型的 Standard**。2026-11-18 抄下这张表，2026-11-27 再打开 Pricing，表内数字没有变。

### Fast

Fast 支持 GPT-6.2 Astra、GPT-6.2 Sol，也支持 GPT-6.1 Sol、GPT-6.1 Terra、GPT-6 Astra、GPT-6 Sol 和 GPT-6 Luna。用 ChatGPT 登录时，CLI 和 IDE 扩展也可以用 Fast。

| 模型 | 套餐内含用量 | credits／企业按量 |
|---|---|---|
| GPT-6.2 Astra、GPT-6.2 Sol | 2 倍 | 2 倍 |
| GPT-6.1 Sol、GPT-6.1 Terra | 2.5 倍 | 2 倍 |
| GPT-6 Astra、GPT-6 Sol、GPT-6 Luna | 2.5 倍 | 2 倍 |

Speed 页另外写了**生成速度**，不要和上表的计费倍率混在一起：对 GPT-6.2 Astra 和 GPT-5.6，Fast 的出 token 速度大约是 Standard 的 1.5 倍。这句没有写 GPT-6.2 Sol。

### Ultrafast

Speed 页写：在 GPT-6.2 Astra 和 Sol 上，Ultrafast 的出 token 速度最多大约是同一模型 Standard 的 4.5 倍。这是速度，不是计费倍率。

谁能开，按 Changelog 和 What's new：

| 套餐或工作区 | Ultrafast |
|---|---|
| Pro，每月 200 美元 | 可以用在 **GPT-6.2 Sol** |
| Pro，每月 500 美元 | **Astra 和 Sol 都可以**。先扣套餐内含，再用 credits |
| Enterprise、Edu | 两款都可以，但工作区要符合条件，并且所有者**另外打开** Ultrafast。默认关闭 |
| GPT-6 Astra、GPT-6.1 Sol 的 Ultrafast | 仍是 Pro 500 美元，以及符合条件的 Enterprise、Edu。Speed 页没有把这两款写成 Pro 200 美元可用 |

Pricing 没有把 Plus、Pro 100 美元、Business 列进 GPT-6.2 的 Ultrafast。本文只按文档点名的资格写。

帮助中心 [Managing usage with GPT-6 Astra](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) 文首已经提到 GPT-6.2 正在推出，但同一页的 Ultrafast 一节仍写：Plus、Pro 100 美元、Pro 200 美元和 Business 在发布时不含 Ultrafast，购买 credits 也不会打开它。这和上面的 Changelog、What's new 冲突。GPT-6.2 的资格以 Changelog、What's new 和 Speed 为准，查询日期 2026-11-18。

Enterprise 工作区要用 Ultrafast，需要 credits 协议或按美元用量计费的协议。Edu 需要 credits 方案。所有者在工作区权限里打开，可以给部分人或整个工作区。按人的花费控制仍然生效。

计费倍率：

| 模型 | 套餐内含用量 | credits／PAYG |
|---|---|---|
| GPT-6.2 Astra、GPT-6.2 Sol | **始终 6 倍** | 到 **2027-02-28** 为 3 倍；**2027-03-01**（太平洋时间）起为 6 倍 |
| GPT-6 Astra | 8 倍 | 6 倍 |
| GPT-6.1 Sol | 8 倍 | 6 倍 |

脚注写的是：用已购买的 credits 支付的超额，以及符合条件的 Enterprise 按量，在 2027 年 2 月 28 日之前按 Standard 的 3 倍计，3 月 1 日起按 6 倍计。套餐内含用量全程都是 6 倍。GPT-6.1 Terra 不在 Ultrafast 表里。

数据驻留：GPT-6.2 Astra、GPT-6.2 Sol 和 GPT-6 Astra 的 Ultrafast **只支持美国**。GPT-6.1 Sol 的 Ultrafast 还支持欧洲（EEA 和瑞士）。What's new 对 API 另写了一句：两款在 Standard、Fast 和 Batch 上支持美国和欧盟数据驻留，Ultrafast 只支持美国。

CLI 里 Speed 页写：输入 `/` 看当前模型有哪些命令，用 `/fast` 或 `/ultrafast` 选速度，再输入一次当前命令回到 Standard。选择会被记住。用 `/statusline` 可以在页脚看到 Fast。0.169.1 的 `--help` 里没有这两条斜杠命令，本文也没有在交互会话里执行它们。

用 API Key 登录时按 API 价格计费，ChatGPT 的 credits 倍率只在 ChatGPT 登录时适用。

## 额度与 credits：5 小时消息估算、credits 单价与 USD 单价

ChatGPT Work 和 Codex **共用**价格、credits 和用量限制。条数不是固定上限。Pricing 写明：下面是 Plus 和 Standard Business 每 5 小时的**本地消息估算**；Pro 目前没有 5 小时限制；云端任务可能比本地消息更吃额度；实际以用量面板为准。

| 模型 | Plus，每 5 小时本地消息估算 | Standard Business |
|---|---|---|
| GPT-6.2 Astra | 6–50 | 6–50 |
| GPT-6.2 Sol | 17–180 | 17–180 |
| GPT-6 Astra | 5–45 | 5–45 |
| GPT-6.1 Sol | 15–160 | 15–160 |

同一页还有 Terra、GPT-6 Sol 和 Luna 的估算，完整表和「觉得被多扣时怎么查」放在 [用量额度](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

2026-11-27 再对过上面这张 5 小时估算，数字仍是表里这些。它可能没有反映 11 月 26 日的计费更正。不要按 40% 或 25% 把这些区间折算成新的条数。以设置里的 Usage 为准。

Standard 速度下，每 100 万 token 的 credits 单价：

| 模型 | 输入 | 缓存输入 | 输出 |
|---|---:|---:|---:|
| GPT-6.2 Astra | 200 | 10 | 1,000 |
| GPT-6 Astra | 250 | 25 | 1,250 |
| GPT-6.2 Sol | 50 | 2.5 | 250 |
| GPT-6.1 Sol | 50 | 2.5 | 250 |

GPT-6.2 Sol 的 credits 单价和 GPT-6.1 Sol 相同。Astra 低于上一代 GPT-6 Astra。credits 单价不等于套餐内含用量，面板仍以 Usage 为准。Codex 的 credits 计费没有单独的 cache-write 费用。

美元单价有两处来源，数字相同、口径要分开：

- Pricing 页把它们写成 **按美元用量计费**、Standard 速度：Astra 每 100 万 token 为输入 8 美元、缓存输入 0.40 美元、输出 40 美元；Sol 为 2 美元、0.10 美元、10 美元。
- 发布文把同一组数字写成 **标准 API 价格**，并写 Astra 的输入和输出比 GPT-6 Astra 低 20%，缓存输入低 60%；Sol 沿用 GPT-6.1 Sol 的 API 价格。

用 API Key 跑 Codex 时走 API 价格，不走 ChatGPT 套餐面板上的倍率。

## 怎么省

这一节只写官方文档已经说过的做法。X 帖子里的 40% 和 25% 不在这里换算成少用多少条。

- **日常编码先用 Sol**。Models 页把 GPT-6.2 Sol 放在 everyday work：改代码、起草、把几份材料收成一份计划。Astra 留给最难的端到端工作。What's new 同样写：难题用 Astra，日常编码和写作用 Sol。
- **推理强度按任务调**。Models 页写，范围清楚的小任务适合 Light，CLI 里对应 Low。Max 用在深度比速度或用量更重要的时候。Pricing 写明：模型选择、上下文、推理、工具使用、检索和缓存都会影响用量。官方文档没有给出「从 High 降到 Light 能省百分之几」。
- **Fast 和 Ultrafast 更吃额度**。Speed 页写，两者都比同一模型的 Standard 生成得更快，也更多使用套餐用量或 credits。倍率以 Pricing 的 Speed multipliers 为准。2026-11-27 核对，两款 GPT-6.2 的 Fast 仍是套餐内含 2 倍、credits 2 倍。Ultrafast 的套餐内含仍是 6 倍；credits 和符合条件的企业按量，到 2027-02-28 为 3 倍，2027-03-01（太平洋时间）起为 6 倍。资格和入口见上面的 Fast 与 Ultrafast 一节，不要为了省额度去开这两档。
- **看 Usage，不看折算**。5 小时估算怎么读、Fast 倍率在面板上怎么理解，见 [用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。收到的 banked reset 能不能兑、80% 门槛是什么，见 [额度重置怎么用](./32-Codex额度重置怎么用-banked-reset在哪看怎么兑换与刷新时间变化.md)。界面写容量满时，先和额度用尽分开，见 [容量不足与额度重置排查](../15-故障排查与常见问题/01-Codex模型容量不足与额度重置排查.md)。

## 和 GPT-6.1 Sol、Terra、Luna 怎么搭配

Model selection 页按工作类型给出的强弱顺序，六类都是同一列：GPT-6.2 Astra，然后 GPT-6.2 Sol，然后 GPT-6.1 Terra，然后 GPT-6 Luna。页面把这张表标成高层估计。GPT-6.1 Sol 和 GPT-6 Astra 不在这张排序里，但定价、速度和模型详情里还有它们。菜单里看得到，就可以继续用。

可以这样搭配，后一半是使用建议，不是官方强制：

- 日常改代码、补测试、审 PR：GPT-6.2 Sol，推理强度用客户端当前档。
- 跨服务排查、要按模板交付的难题：GPT-6.2 Astra。
- 根据材料写作、看截图、目标明确的电脑操作、小范围修复：先试 GPT-6.1 Terra。
- 抽取、分类、格式已经写死的批量改写：GPT-6 Luna。
- 等得太久时再开 Fast。Ultrafast 只在上面的套餐资格里开，不要把它当成推理强度。

GPT-5.5 的退役说明没有被这次上线取消：2026-10-14 中午（太平洋时间）起，用 ChatGPT 登录的 Codex 不再提供 GPT-5.5。API 以及用 API Key 登录的 Codex 会话不受影响。付费套餐的替代模型，Models 页仍写 GPT-6.1 Sol（`gpt-6.1-sol`）；Free 和 Go 在桌面端用 GPT-6 Luna。

## 参考资料

- [Changelog，2026-11-17](https://learn.chatgpt.com/codex/changelog)
- [GPT-6.2 What's new](https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol)
- [Models](https://learn.chatgpt.com/docs/models)
- [Model selection](https://learn.chatgpt.com/docs/model-selection)
- [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability)
- [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/)
- [Changelog](https://learn.chatgpt.com/docs/changelog)（2026-11-27 打开 HTML；`.md` 为 404。最新日期见到 2026-11-24，没有计费更正）
- [@thsottiaux，2026-11-26 02:50 UTC](https://x.com/thsottiaux/status/2125784147889393806)（社交媒体说明，非官方文档）
- [@thsottiaux，2026-11-26 07:26 UTC，“Banked reset is online”](https://x.com/thsottiaux/status/2125853628250599730)（社交媒体说明，非官方文档）
- [Codex 模型怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [Codex 用量额度怎么看](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)
- [Codex 使用 GPT-6.1 Terra](./14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md)
