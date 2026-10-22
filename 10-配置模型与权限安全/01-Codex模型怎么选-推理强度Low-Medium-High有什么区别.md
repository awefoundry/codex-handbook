---
id: model-reasoning-effort
title: Codex 模型怎么选：推理强度和 GPT-6.1 Sol
seo_title: Codex 模型怎么选：GPT-6.1 Sol、推理强度和速度档
description: 2026 年 10 月 14 日起，ChatGPT 登录的 Codex 不再提供 GPT-5.5。本文按官方文档说明怎么改用 GPT-6.1 Sol、GPT-6 Luna 或 Astra，如何选择推理强度，以及 Fast 和 Ultrafast 怎样影响额度。
lede: 付费套餐优先看 GPT-6.1 Sol，Free 和 Go 用 GPT-6 Luna。推理强度按任务加减，速度档另算。
url: /guides/codex-model-reasoning-effort
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 参考
source_tag: 官方功能
entry_tags: [App, CLI, IDE, Cloud, ChatGPT Work]
difficulty: 进阶
order: 1
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-19
date_modified: 2026-10-22
client_validation_pending: true
models: [gpt-6.1-sol, gpt-6-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/models
keywords: [Codex 模型选择, GPT-6.1 Sol, 推理强度, Ultrafast, model_reasoning_effort]
faq:
  - q: 用 API Key 登录的 Codex 还要换掉 GPT-5.5 吗？
    a: 不用。官方写明 OpenAI API，以及用 API Key 认证的 Codex 会话，不受这次退役影响。
  - q: Ultra 和 Ultrafast 是同一个开关吗？
    a: Ultra 和 Ultrafast 各管一件事。Ultra 是推理强度，会使用子 Agent。Ultrafast 是速度档，按更高倍率消耗额度，而且只对部分套餐开放。
  - q: 把推理强度调高会更快吗？
    a: 通常不会。更高的推理强度花更长时间，也用更多 token。想缩短等待，要看 Fast 或符合资格时的 Ultrafast。
---

# Codex 模型怎么选：推理强度和 GPT-6.1 Sol

> 本文在线版：[codexguide.io/guides/codex-model-reasoning-effort](https://codexguide.io/guides/codex-model-reasoning-effort)

## 2026-10 更新说明

这篇原来按 2026-08 的 GPT-5.6 代来写，默认组合是 Terra + Medium。2026-10-22 对照 [Models](https://learn.chatgpt.com/docs/models)、[Changelog](https://learn.chatgpt.com/docs/changelog)、[Pricing](https://learn.chatgpt.com/docs/pricing)、[Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) 和配置文档改了一版。这次动了这些地方：

- ChatGPT 登录的 Codex 从 2026-10-14 正午 PDT（19:00 UTC，北京时间 10 月 15 日 03:00）起不再提供 GPT-5.5。Plus、Pro、Business、Enterprise、Edu 能选到时改用 GPT-6.1 Sol（`gpt-6.1-sol`）。Free 和 Go 在桌面端改用 GPT-6 Luna（`gpt-6-luna`）。Enterprise 和 Edu 的 GPT-6.1 Sol 默认关闭，要管理员打开。API Key 会话不在这次退役范围内。
- 删掉旧文的 credit 比例、三份第三方跑分，以及 CLI 0.146.1 上 Luna / Terra / Sol 的耗时表。那些数字对不上现在的官方价目，也不能用来判断 GPT-6.1。
- 推理强度的选法留下了。补上官方现在的起步建议：GPT-6.1 Sol 用客户端默认档，Luna 从 High 起步，Astra 从 Light 起步。Light 和 CLI 里的 Low 是同一档，配置值是 `low`。
- 补上 Fast 和 Ultrafast。速度和推理强度是两个开关。
- 2026-08 的桌面端截图还是旧模型菜单，正文先拿掉。下面用 HTML 注释标了需要重拍的画面，本环境没有打开桌面端或 CLI 复核界面。

## 结论

先按任务选，再按结果加减。付费套餐里，复杂编码和要反复跑的长任务用 GPT-6.1 Sol。边界清楚、数量大的抽取和改写用 GPT-6 Luna。最难的端到端工作再考虑 GPT-6 Astra。Free 和 Go 这次启动范围里没有 GPT-6.1 Sol，桌面端用 GPT-6 Luna。

推理强度决定模型在这一题上想多久。官方的说法是：更高档位可能让复杂任务做得更好，同时更慢，token 也更多。任务只是返回得慢，去看速度档，不要顺手把推理强度拉高。

| 任务 | 模型和推理强度 | 依据 |
|---|---|---|
| 摘要、分类、抽取、格式转换、批量改写 | GPT-6 Luna，High | 模型页把这类工作交给 Luna，并写明 Luna 从 High 起步 |
| 解释一小段代码、范围已经写死的机械修改 | 有 GPT-6.1 Sol 时用它，推理放在 Light / Low。账号里只有 Luna 时，仍用 Luna + High | Light / Low 适合边界清楚的小任务。Luna 的起步档是 High，不要套到 Sol 的 Light 上 |
| 日常功能、补测试、常规调试 | GPT-6.1 Sol，先用客户端当前的默认推理强度 | 复杂编码和 agent 工作流优先用 6.1 Sol；默认档的名字以客户端显示为准 |
| 跨模块调试、方案取舍、正确性复核 | GPT-6.1 Sol，High 或 Extra High | 这两档面向多步骤、多来源、需要权衡的工作 |
| 一道很难、暂时拆不开的题 | 当前模型 + Max | Max 把时间花在单个任务上。多数任务用不到。Luna 最高到 Max |
| 可以并行的审查、迁移、调研 | GPT-6.1 Sol + Ultra，或在提示里明确要求子 Agent | Ultra 会使用子 Agent。子 Agent 各自消耗 token |
| 最难的端到端工作 | GPT-6 Astra，从 Light 起步，不够再升 | Astra 能力最强。6.1 Sol 接近它，成本更低。Astra 的 Light 在配置里是 `low` |

这张表里的「默认推理强度」没有一个全球统一的档位名。模型页只说 GPT-6.1 Sol 从你客户端现成的那一档开始。打开菜单或运行 `/status`，看到的才是你的默认值。

<!-- 待实测截图：ChatGPT 桌面端输入框下方的模型和推理控件。画面要能看清当前账号实际列出的模型（对照是否有 GPT-6.1 Sol 或 GPT-6 Luna）以及 Light 到 Ultra 的档位。2026-08 旧图仍是 Sol / Terra / Luna，不能再当现况。 -->

三个开关别拧在一起。

- **模型**：能力、速度和基础消耗的大致区间。换模型不会改变工作区权限，也不会因此获得这个模型的使用权。
- **推理强度**：这一题上投入多少计算。桌面端、ChatGPT Work 网页和 IDE 把最低档显示为 Light，CLI 显示为 Low。配置里写 `low`。
- **速度**：用更多额度换更快的 token。Fast 覆盖多款现役模型。Ultrafast 只支持 GPT-6 Astra 和 GPT-6.1 Sol，而且只对部分套餐开放。

<!-- 待实测截图：同一账号下 Fast 与 Ultrafast 在速度菜单中的位置，注明套餐（Plus、Pro 100/200/500，或 Enterprise/Edu）。没有 Ultrafast 时把套餐和菜单一起拍下来。 -->

### 推理强度怎么加减

配置参考列出的取值包括 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`。某一档是否出现，取决于模型和客户端。

| 界面名称 | CLI | 配置值 | 什么时候用 |
|---|---|---|---|
| Light | Low | `low` | 范围清楚、希望尽快返回的小任务。Astra 的官方起步档 |
| Medium | Medium | `medium` | 需要一些规划，同时还要顾速度 |
| High | High | `high` | 要追查逻辑、核对假设、处理边界。Luna 的官方起步档 |
| Extra High | 以菜单为准 | `xhigh` | 更难的多步骤工作。配置参考有这个值；模型页只写了界面名 Extra High，没有在同一句里写出 `xhigh` |
| Max | `/model` 里的 More reasoning… | `max` | 单题很难，深度比速度和用量重要。桌面端看不到时，检查应用设置 |
| Ultra | 同上 | `ultra` | 工作能拆成几块并行做。多数任务用不到 |

GPT-6 Luna 支持到 Max，不支持 Ultra。桌面端滑杆里没有 Ultra 时，打开 Settings 里的 Configuration，再打开模型选择滑杆中的 Ultra。CLI 里先 `/model` 选模型，再进 More reasoning… 看这个模型有没有 Max 或 Ultra。

不同代的同名档位不能直接对比。熟悉的任务可以先降一档试，看结果再加。

高档位补不上模糊需求。没有验收标准时，先写清目标、不能改什么、怎样算做完。这一步比从 Medium 拉到 High 更有用。长任务如果需要跨很多轮还盯着同一个完成条件，可以另外用 `/goal`。用法见 [Codex Goal 模式](https://codexguide.io/guides/codex-goal-mode-long-running-work)。

### 仍建议把规划和执行分开

省额度的办法还是那条：强模型做少量判断，范围已经写清的步骤交给更便宜的模型。官方对子 Agent 的分工也是这个方向。GPT-6.1 Sol 负责含糊、多步骤、要自己验证的工作；GPT-6 Luna 负责快、窄、可重复的工作。

可以按四步做。

1. 用 GPT-6.1 Sol 做规划。官方说任务需要更多规划时再上调推理强度，这一步放到 High。只读代码，列出要改的文件、顺序、每步验收和回归风险，先不改文件。
2. 人确认计划。边界已经写死的步骤，交给 GPT-6 Luna，推理强度用 High。
3. 批量改名、摘要、变更说明初稿，同样交给 Luna。
4. 改完后，再用 GPT-6.1 Sol 做一次只读复核，看遗漏、回归和测试缺口。

规划时可以用：

```text
先不要修改文件。请分析这个需求涉及的代码路径，列出：
1. 需要修改的文件和原因；
2. 实施顺序；
3. 每一步的验收条件；
4. 可能的回归风险和测试方案。
计划中不要使用“视情况而定”。遇到不确定的信息，写明要先验证什么。
```

执行时把已经确认的计划当成约束：

```text
按下面已经确认的计划执行。只处理第 2、3 步，不扩大范围。
完成后运行计划中指定的测试，并报告实际结果。
如果计划与代码现状冲突，停止修改并说明冲突。
```

一次能用的结果，成本里要算上重试、人工复核和出错以后的返工。Luna 一次做对，就让它继续做这类工作。它连续跑偏，GPT-6.1 Sol 一次通过测试，后者更省。这是用法判断。官方价目表没有这条公式。

子 Agent 各自做模型调用和工具调用，token 会高于同等的单 Agent。能拆开、互不改同一批文件时再用。并行做法见 [Codex 使用 Subagents 并行处理任务](https://codexguide.io/guides/codex-subagents-parallel-work)。

## 配置怎么改

桌面端、CLI 和 IDE 扩展读同一份 `config.toml`。用户配置在 `~/.codex/config.toml`。项目配置是仓库里的 `.codex/config.toml`，只有项目受信任时才加载。不写 `model` 时，这三个入口使用当前的推荐模型。

CLI 0.159.1（更新日志日期 2026-09-29）把 GPT-6.1 Sol 加为 bundled 目录，以及 Amazon Bedrock 的 Mantle 和 Runtime 目录的默认模型。0.161.0（2026-10-07）的发布说明再次写明，它是 bundled 和 Amazon Bedrock 目录的默认模型。0.162.0（2026-10-08）写明，新的 TUI 线程会尊重服务端给出的模型和推理摘要默认值，启动时显式加的参数仍然优先。所以目录里的默认模型，和你这个新会话实际用到的模型，可能不一样，以 `/status` 为准。Free 和 Go 本来就选不到 `gpt-6.1-sol`。

<!-- 待实测截图：CLI 执行 /model 后的列表，以及选中模型后 More reasoning… 的画面。再执行 /status，让模型名和推理强度出现在同一屏。 -->

### 写入默认模型

账号里有 GPT-6.1 Sol 时，可以照官方示例写成：

```toml
# ~/.codex/config.toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
```

`medium` 是配置基础文档里的示例值，用来把档位固定下来。它不等于「所有 GPT-6.1 Sol 用户的出厂默认」。你如果想继续用客户端默认档，就不要写 `model_reasoning_effort`。

Free、Go，或者付费套餐里专门做抽取和批量改写的配置，按 Luna 的起步建议写：

```toml
model = "gpt-6-luna"
model_reasoning_effort = "high"
```

Enterprise 和 Edu 里，GPT-6.1 Sol 默认关闭，要管理员先打开。看不到模型时，先问管理员，不要在配置里写一个菜单里不存在的 slug。

只想对这一次命令生效时，优先用 `--model` / `-m`。其它键用 `--config` 或 `-c`，值按 TOML 解析，字符串要再包一层引号：

```bash
codex --model gpt-6.1-sol
codex exec -m gpt-6.1-sol "Review the current changes"
codex --model gpt-6.1-sol --config model_reasoning_effort='"high"'
```

交互会话里输入 `/model`，选择账号实际列出的模型。官方示例是 `gpt-6-luna` 或 `gpt-6.1-sol`。CLI 会在记录里确认，再用 `/status` 核对。推理强度在这个选择器里一起调；Max 和 Ultra 在 More reasoning… 下面。

开发者命令文档在 IDE 相关的命令表里另外列出了 `/reasoning`，作用是选择当前对话的推理强度。CLI 主表没有单独的 `/reasoning`，写的是 `/model` 在可用时同时选择模型和推理强度。本文没有在本机输入 `/` 核对 CLI 是否也出现 `/reasoning`。待确认。

覆盖关系从高到低是：命令行参数和 `--config`、受信任项目里的 `.codex/config.toml`（离当前目录越近越优先）、`--profile` 选中的 `~/.codex/<name>.config.toml`、用户配置、工作区下发的云端默认、Unix 上的 `/etc/codex/config.toml`、内置默认。Profile 从 Codex 0.134.0 起不再读取 `config.toml` 里的 `[profiles.<name>]`。

托管配置里的 `[models.new_thread]` 只提供默认值。只要用 `--model`、`--config` 或 `--profile` 显式改了模型或推理强度，这一层里的 `model` 和 `model_reasoning_effort` 会一起被忽略。`service_tier` 单独计算。

### Fast 不要写成全局默认

Fast 加快受支持模型的 token 生成，包括 GPT-6.1 Sol、GPT-6 Astra、GPT-6 Sol 和 GPT-6 Luna。CLI 里输入 `/fast` 打开，再输入一次关闭，选择会被保存。当前模型没有公布 Fast 档时，`/fast` 不会出现。

想让新回合默认走 Fast，官方写法是：

```toml
service_tier = "fast"

[features]
fast_mode = true
```

`features.fast_mode` 默认已经是 true，作用是打开 Fast 控件。真正指定档位的是 `service_tier = "fast"`，请求里它对应 `priority`。套餐内用量按 Standard 的 2.5 倍计，已购买的 credits 和企业按量按 2 倍计。建议只在等待时间明显碍事时打开，不要把它留成所有任务的默认值。

Ultrafast 的控件开关是 `features.ultrafast_mode`，默认也是 true。打开开关不等于账号有资格。配置参考只明确写了 `service_tier` 可以填 `fast`，或填当前模型公布的其它档位，没有给出 Ultrafast 的配置字符串。待确认。选这一档时用客户端菜单。

资格写在速度页上：Pro 每月 500 美元，以及符合条件的 Enterprise 和 Edu。其它自助套餐即使买了 credits 也不能用。Enterprise 默认关闭，由工作区所有者打开。Pro 500 美元先用套餐内额度，用完再用 credits。已购 credits 和企业按量按 Standard 的 6 倍计，套餐内用量按 8 倍计。GPT-6 Astra 的 Ultrafast 生成 token 最多比它自己的 Standard 快 8 倍。速度页没有把这句 8 倍速度写到 GPT-6.1 Sol 上。6.1 Sol Ultrafast 的额度倍率是 8 倍和 6 倍，速度倍数待确认。

GPT-5.6 的 Fast 速度提升官方写的是 1.5 倍。GPT-6 这一代的 Fast 只写了「会加快」，没有另一个倍数。

### 自定义 Agent 可以各用各的模型

子 Agent 没有单独写 `model` 和 `model_reasoning_effort` 时，继承父会话。官方示例把读代码的 Agent 放在 `gpt-6-luna` + `high`，审查 Agent 放在 `gpt-6.1-sol` + `medium`。总则里又说审查和安全类适合 `high`。示例和总则差一档，照抄示例可以用 medium；你希望它查得更细，就改成 `high`。

个人 Agent 放在 `~/.codex/agents/`，项目 Agent 放在 `.codex/agents/`。每个 TOML 至少要有 `name`、`description`、`developer_instructions`。文件里写了的 `model` 或 `model_reasoning_effort` 会盖过父会话。文件只写了模型、没写推理强度时，保留先前已经解析好的推理强度。自定义 Agent 不能改掉父会话的沙箱、审批、provider 和 MCP，服务档也跟着根会话。

下面保留官方示例里的键和模型。`pr_explorer` 这个名字也和文档一致。说明文字按同一分工缩短过，完整句子在 Subagents 文档里。不要把自定义 Agent 命名成内置的 `explorer`，同名时会盖过内置 Agent。

```toml
# ~/.codex/agents/pr-explorer.toml
name = "pr_explorer"
description = "只读查看代码，汇总证据。"
model = "gpt-6-luna"
model_reasoning_effort = "high"
developer_instructions = """
不要改文件。
给出文件、符号和调用路径。
不要顺便提出修改方案。
"""
```

```toml
# ~/.codex/agents/reviewer.toml
name = "reviewer"
description = "审查正确性、安全和测试缺口。"
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
developer_instructions = """
不要改文件。
先写会改变行为的问题，再写缺测试的地方。
"""
```

全局默认值写在 `config.toml` 的 `[agents]` 里：`agents.default_subagent_model` 和 `agents.default_subagent_reasoning_effort`。显式指定的模型或推理强度会盖过这两项。完整的三 Agent 示例以 [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) 为准。

### 把写死的 gpt-5.5 找出来

ChatGPT 登录的会话里，下面这些地方如果还写着 `gpt-5.5`，换成当前账号能选到的模型。官方点名的位置是：工作区默认、已保存的模型设置、托管配置、自定义 Agent、定时任务，以及会选择模型的脚本。

本机可以先搜：

- `~/.codex/config.toml`
- `~/.codex/*.config.toml`
- 项目里的 `.codex/config.toml`
- `~/.codex/agents/` 和项目 `.codex/agents/`
- `codex --model`、`codex exec -m`、`--config model=`

定时任务的入口见 [Codex Automations](https://codexguide.io/guides/codex-automations-scheduled-tasks)。改完以后新开一个会话，用 `/status` 或桌面端控件确认模型名，不要只看配置文件已经保存。

用 API Key 认证的会话继续按 API 项目里的模型列表走，GPT-5.5 仍可用，ChatGPT 的 credit 倍率不适用。自定义供应商需要兼容的 Responses API。当前版本不支持 `wire_api = "chat"`，也不能只接 Chat Completions。

更早的 slug 也在模型页的退役说明里：`gpt-5.4` 在 2026-08-31 从 ChatGPT 登录的 Codex 退役，替代是 `gpt-6-sol`；`gpt-5.4-mini` 的替代是 `gpt-6-luna`，Enterprise 和 Edu 要管理员先打开 Luna。`gpt-5.2` 和 `gpt-5.3-codex` 在 ChatGPT 登录下已经弃用。`gpt-5.3-codex-spark` 于 2026-09-14 退役。`gpt-6-sol` 和 `gpt-6.1-sol` 是两个 slug，新的目录默认值是后者。

## 额度和速度

下面两张表都来自 [Pricing](https://learn.chatgpt.com/docs/pricing)，核对日期 2026-10-22。它们回答的是两件不同的事。

第一张是 Standard 速度下，每 100 万 token 的 credit 单价。credit 计费没有单独的缓存写入费。API Key 用量不看这张表。

| 模型 | 输入 | 缓存输入 | 输出 |
|---|---:|---:|---:|
| GPT-6 Astra | 250 | 25 | 1,250 |
| GPT-6.1 Sol | 50 | 2.5 | 250 |
| GPT-6 Sol | 50 | 5 | 250 |
| GPT-6 Luna | 2.5 | 0.25 | 12.5 |
| GPT-5.6 Sol | 100 | 10 | 500 |
| GPT-5.6 Terra | 50 | 5 | 300 |
| GPT-5.6 Luna | 5 | 0.5 | 30 |

GPT-6 Luna 的输入和输出单价都是 GPT-6.1 Sol 的二十分之一，缓存输入是十分之一。旧文里的「Terra 约为 Sol 的一半，Luna 约为五分之一」对不上这张表。GPT-5.6 三款的单价还在价目上，模型页也写明切换期仍然可用。GPT-5.6 Sol 的促销价至少保持到 2026-11-21。单价仍然不能代表一次任务的总消耗，上下文、工具调用、推理强度和重试都会改变结果。

第二张是 Plus 和标准 Business 上，本地消息在每 5 小时里的估算条数。官方写明条数会随任务变化，不能当成固定上限。Pro 目前没有 5 小时限制。云端任务可能更费额度，每周限制也可能另算。看剩余额度以用量面板为准；CLI 里定价页写的是用 `/status`。

| 模型 | Plus 与标准 Business 的本地消息估算 |
|---|---|
| GPT-6 Astra | 5–45 |
| GPT-6.1 Sol | 15–160 |
| GPT-6 Sol | 15–150 |
| GPT-6 Luna | 350–3,000 |

速度档相对同一模型的 Standard，倍率是：

| 速度 | 套餐内用量 | 已购 credits 与企业按量 |
|---|---|---|
| Fast | 2.5 倍 | 2 倍 |
| GPT-6 Astra Ultrafast | 8 倍 | 6 倍 |
| GPT-6.1 Sol Ultrafast | 8 倍 | 6 倍 |

套餐和模型的对应关系，以模型菜单为准。定价页写明的范围是：

- Free（0 美元）和 Go（8 美元/月）：桌面端的 GPT-6 Luna，Standard 速度，受 rollout 影响。
- Plus（20 美元/月）：套餐说明列出 GPT-6.1 Sol 和 GPT-6 Luna。用量估算表里同时有 GPT-6 Astra，是否出现在菜单里仍看账号。
- Pro：100、200 或 500 美元/月。Ultrafast 只在 500 美元这一档。
- Business、Enterprise、Edu：GPT-6.1 Sol 在 Work 和 Codex 里可用，不在 Chat 里。Enterprise 和 Edu 默认关闭，管理员打开后才能用。
- API Key：CLI、SDK、IDE 扩展按 API 价格计费，没有云端功能。

GPT-6.1 Sol Ultrafast 的推理驻留区域是美国和欧洲（EEA 与瑞士）。GPT-6 Astra Ultrafast 只写了美国。

## 常见问题

### 配置改了，新会话还是旧模型

先确认改的是启动 Codex 的那个环境里的 `~/.codex/config.toml`。Windows、WSL 和 macOS 各有自己的用户目录。项目未受信任时，项目级 `.codex/config.toml` 不会加载。命令行如果带了 `--model`、`--config` 或 `--profile`，会盖过 `[models.new_thread]` 里的模型和推理强度。核对时看新会话的 `/status`，不要只看文件。

入口差异见 [App、CLI、IDE 和 Cloud 怎么选](https://codexguide.io/guides/app-cli-ide-he-cloud-zen-me-xuan)。任务老是跑偏时，先过一遍 [设置检查清单](https://codexguide.io/guides/codex-settings-checklist)，再决定要不要换模型。

### 菜单里还有 Terra

那是切换期仍可能出现的 GPT-5.6 Terra，价目表里也还留着它的单价。2026-10 的目录默认和模型页推荐是 GPT-6.1 Sol。付费套餐做日常开发，按模型页改用这一款。Terra 只有在你自己的任务里仍然更合适时再留着，不要把它写成新脚本的默认模型。

### 文档上的六档 Power 和我的菜单不一样

模型页把桌面端和 Work 网页的 Power 预设写成示例：Luna High、GPT-6 Sol Light、GPT-6 Sol Medium、Astra Light、Astra Medium、Astra Extra High。部分付费套餐没有 Astra Extra High。页面同时写明，可选项和默认值随套餐、客户端、工作区设置和 rollout 变化。示例里被选中的是 GPT-6 Sol Light。这一格没有写成 GPT-6.1 Sol。以你自己的 Advanced 菜单为准，那里可以选择具体模型、推理强度和速度。

### 想知道自己的任务该用哪一档

公开价目只能缩小范围。用两个你能验收的旧任务做对照：一个小改动，一个跨文件问题。同一段提示词，GPT-6.1 Sol 和 GPT-6 Luna 各跑一次，都从客户端默认推理强度开始。记下是否一次通过、追问次数和你亲手改了多少。界面如果显示用量就记下来，没有就留空。2026-08 在 CLI 0.146.1 上做过一轮小测，对象是当时的 Luna、Terra 和 Sol，不能用来推断 GPT-6.1。

和其它编程工具怎么分工，见 [Codex 与其他编程模型比较](https://codexguide.io/guides/codex-yu-qita-biancheng-moxing-bijiao)。那篇里的模型代际如果还停在更早的版本，以本文和官方模型页为准。

## 下一步

- 长任务要跨很多轮还保持完成条件：[Goal 模式](https://codexguide.io/guides/codex-goal-mode-long-running-work)
- 审查或调研可以拆开并行：[Subagents](https://codexguide.io/guides/codex-subagents-parallel-work)
- 定时任务里如果写死了模型：[Automations](https://codexguide.io/guides/codex-automations-scheduled-tasks)

## 参考资料

- [Models](https://learn.chatgpt.com/docs/models)，OpenAI，2026-10-22 核对。GPT-5.5 退役、模型分工、推理强度、`model = "gpt-6.1-sol"`
- [Changelog](https://learn.chatgpt.com/docs/changelog)，OpenAI，2026-10-22 核对。2026-10-14 退役、2026-10-08 Ultrafast、CLI 0.159.1 与 0.161.0 的默认模型、CLI 0.162.0 服务端默认值
- [Pricing](https://learn.chatgpt.com/docs/pricing)，OpenAI，2026-10-22 核对。credit 单价、5 小时消息估算、Fast / Ultrafast 倍率、套餐范围
- [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)，OpenAI，2026-10-22 核对。Fast、Ultrafast、`service_tier = "fast"`、`/fast`
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)，OpenAI，2026-10-22 核对。`model`、`model_reasoning_effort = "medium"`、配置优先级、`features.fast_mode`
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)，OpenAI，2026-10-22 核对。推理强度取值、`service_tier`、`features.ultrafast_mode`、`[models.new_thread]`
- [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)，OpenAI，2026-10-22 核对。`--model`、`--config` 的 TOML 引号、profile 文件
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)，OpenAI，2026-10-22 核对。`/model`、`/fast`、`/status`、`/goal`
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)，OpenAI，2026-10-22 核对。子 Agent 的模型和 `model_reasoning_effort`
