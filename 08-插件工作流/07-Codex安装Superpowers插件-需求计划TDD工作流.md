---
id: codex-superpowers-plugin
title: Codex 安装 Superpowers 插件：让 Codex 按“先问需求、再写计划、测试先行”的流程干活（0.164.0 实测）
seo_title: Codex 安装 Superpowers 插件：需求澄清、计划与 TDD 工作流
description: Superpowers 是 GitHub 上很火的开源 Skills 插件，已收录进 Codex 官方插件目录。本文讲官方目录和作者仓库两种装法，用 Codex CLI 0.164.0 实测作者仓库版的安装、查看和卸载，讲清它带来的 15 个 Skills、默认工作流、适合什么任务，以及版本差异和遥测开关。
url: /guides/codex-superpowers-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 入门
order: 6
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-25
date_modified: 2026-10-25
verified_on: 2026-10-25
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Superpowers, Codex Superpowers, Codex 插件, Codex Skills, TDD, brainstorming, codex plugin marketplace]
related: [codex-subagents-parallel-work, config-toml-guide]
howto: true
faq:
  - q: Superpowers 是 OpenAI 官方做的吗？
    a: 不是。它是 Jesse Vincent 和 Prime Radiant 维护的开源项目（MIT 许可），已收录进 Codex 官方插件目录（openai/plugins），可以在 /plugins 里搜索安装。
  - q: 官方目录里的版本和作者仓库的版本一样吗？
    a: 不一定。2026-10-25 核对时，openai/plugins 里收录的是 6.3.0，作者仓库 obra/superpowers 的最新版本是 7.0.1。想用最新版可以把作者仓库添加为插件市场再安装。
  - q: 装了以后要手动调用吗？
    a: 一般不用。Superpowers 的 Skills 会在合适的时候自动触发，比如开始做新功能时先触发 brainstorming。安装后要新开一个对话或 CLI 会话才能用上。
  - q: 怎么卸载？
    a: 在 /plugins 插件浏览器里卸载，或者运行 codex plugin remove superpowers@<市场名>。
---

# Codex 安装 Superpowers 插件：让 Codex 按“先问需求、再写计划、测试先行”的流程干活（0.164.0 实测）

> 本文在线版：[codexguide.io/guides/codex-superpowers-plugin](https://codexguide.io/guides/codex-superpowers-plugin)

> 核对依据：OpenAI 官方文档 [Plugins](https://learn.chatgpt.com/docs/plugins)、Codex 官方插件目录 [openai/plugins](https://github.com/openai/plugins)，以及 Superpowers 仓库 [obra/superpowers](https://github.com/obra/superpowers) 的 README 和发布说明。实测环境是 Linux 上的 `codex-cli 0.164.0`，使用独立的 `CODEX_HOME`，**没有登录**，所以验证了添加插件市场、安装、查看、卸载和安装后的文件，**没有**在对话里实际跑一遍 Superpowers 工作流；工作流说明引自项目 README。核对日期 2026-10-25。

让 Codex 写代码，最常见的问题不是它写不出来，而是它**太快动手**：需求没问清就开写，写完没测试，改着改着偏离了最初的意图。

[Superpowers](https://github.com/obra/superpowers) 是一套开源的 Skills 插件，专门治这个毛病。它给 Codex 装上一组“工作习惯”：先通过提问把需求弄清楚，再拆成小任务写计划，实现时测试先行，完成前必须拿出验证证据。核对时这个仓库在 GitHub 上有 30 多万 star，已经收录进 Codex 官方插件目录。

这篇讲怎么装、装了以后多了什么、它会怎么改变 Codex 的工作方式，以及哪些任务适合用它。

## 它是什么

Superpowers 由 Jesse Vincent 和 Prime Radiant 维护，MIT 许可。插件描述是“一个 agentic skills 框架和软件开发方法论”，覆盖计划、TDD、调试和协作流程。

在 Codex 里，它是一个**只包含 Skills 的插件**：没有 MCP 服务器，也不装钩子（插件清单里 `hooks` 是空对象）。项目的移植文档说明了原因：Codex 原生支持 Skills，不需要会话启动钩子。装好后，Codex 会在合适的时机自动读取对应的 Skill。

## 方式一：从官方插件目录安装（推荐）

Superpowers README 和 OpenAI 插件文档给的路径一致。

**Codex CLI**：

```text
codex
/plugins
```

在插件浏览器里搜索 `superpowers`，选择 **Install Plugin**。插件浏览器按市场分组，可以切换市场标签，打开插件查看详情、安装或卸载；对已安装的插件按空格键可以开关。

**Codex 桌面端**：README 的写法是点击侧边栏的 Plugins，在 Coding 分区里找到 Superpowers 安装。OpenAI 插件文档的通用步骤是：搜索或浏览到插件、打开详情、点加号安装，再新开一个对话使用。

官方文档提醒两点：

- 插件里的 Skills 在**新开对话或新开 CLI 会话**后才可用。
- 插件运行在 Codex 宿主里时，沿用宿主的沙箱和审批策略，不会因为装了插件就获得额外权限。

## 方式二：从作者仓库安装最新版

官方目录里的版本可能落后于作者仓库。2026-10-25 核对时：

| 来源 | 版本 |
| --- | --- |
| Codex 官方插件目录 `openai/plugins` | 6.3.0 |
| 作者仓库 `obra/superpowers` | 7.0.1（10 月 21 日发布） |

想用最新版，可以把作者仓库添加成一个插件市场。`codex plugin` 子命令在 0.164.0 里有 `add`、`list`、`remove` 和 `marketplace`；`marketplace add` 接受 `owner/repo[@ref]` 形式的 GitHub 仓库。

实测（独立 `CODEX_HOME`，未登录）：

```bash
codex plugin marketplace add obra/superpowers
```

```text
Added marketplace `superpowers-dev` ...
```

仓库里的市场名叫 `superpowers-dev`。查看可装的插件：

```bash
codex plugin list
```

```text
PLUGIN                       STATUS         VERSION  SOURCE
superpowers@superpowers-dev  not installed           ...
```

安装：

```bash
codex plugin add superpowers@superpowers-dev
```

```text
Added plugin `superpowers` ...
Installed plugin root .../plugins/cache/superpowers-dev/superpowers/7.0.1
```

再跑 `codex plugin list`，状态变成 `installed, enabled`，版本 `7.0.1`。

同时 `config.toml` 里多了两段：

```toml
[marketplaces.superpowers-dev]
source_type = "git"
source = "https://github.com/obra/superpowers.git"

[plugins."superpowers@superpowers-dev"]
enabled = true
```

以后更新这个市场的快照，用：

```bash
codex plugin marketplace upgrade superpowers-dev
```

> 两种方式选一种就行，不要同时从两个市场装同一个插件，否则会有两套同名 Skills。

## 装完多了什么：15 个 Skills

7.0.1 版本安装后，插件目录下的 `skills/` 里有 15 个 Skill。按 README 的分类：

| 分类 | Skill | 作用 |
| --- | --- | --- |
| 协作 | `brainstorming` | 动手前先通过提问弄清你要什么、为什么要，再把理解复述给你确认 |
| 协作 | `writing-plans` | 把确认过的设计拆成每个 2 到 5 分钟的小任务，写清文件路径和验证步骤 |
| 协作 | `executing-plans` | 在当前会话里自己按计划逐项实现，最后做一次整体审查 |
| 协作 | `subagent-driven-development` | 每个任务派一个新的子 agent 去做，每个任务后审查 |
| 协作 | `dispatching-parallel-agents` | 两个以上互不依赖的任务并行处理 |
| 协作 | `using-git-worktrees` | 开新分支和独立工作区，确认测试基线干净 |
| 协作 | `requesting-code-review` / `receiving-code-review` | 发起审查前自查；收到审查意见时先核实再改 |
| 协作 | `finishing-a-development-branch` | 测试通过后，给出合并、开 PR、保留或丢弃的选项 |
| 测试 | `test-driven-development` | 红-绿-重构：先写失败的测试，看它失败，再写最少的代码让它通过 |
| 调试 | `systematic-debugging` | 四阶段找根因，不先猜修复 |
| 调试 | `verification-before-completion` | 声称“修好了”之前必须跑验证命令、看输出 |
| 调试 | `diagnosing-superpowers` | 会话出问题时，读会话记录分析哪里出了偏差 |
| 元 | `using-superpowers` | 告诉 agent 怎么发现和使用这些 Skills |
| 元 | `writing-skills` | 按项目的方法写新的 Skill 并测试 |

## 它会怎么改变 Codex 的工作方式

README 描述的默认流程是这样的：

1. **brainstorming**：你说要做什么，它不直接写代码，先问问题，把需求理清楚。小改动在对话里确认，大项目会写一份设计文档。
2. **using-git-worktrees**：设计确认后，开新分支和独立工作区。
3. **writing-plans**：把设计拆成小任务，每个任务有确切的文件路径和验证步骤。
4. **subagent-driven-development** 或 **executing-plans**：前者每个任务派一个新的子 agent 并逐个审查，最彻底；后者在当前会话里逐项实现，最后整体审查一次，最省。
5. **test-driven-development**：实现时先写失败的测试。README 甚至写明，测试之前写的代码会被删掉。
6. **requesting-code-review**：任务之间按计划审查，严重问题会阻止继续。
7. **finishing-a-development-branch**：全部完成后验证测试，让你选择合并、开 PR、保留还是丢弃。

README 的原话是：agent 在做任何任务前都会检查有没有相关的 Skill，**这是强制流程，不是建议**。

所以装上之后最直观的变化是：你说“加个功能”，Codex 会先反过来问你一串问题。这对想快速改一行代码的人可能有点啰嗦，但对需求模糊的新功能很有用。

## 适合和不适合的任务

**适合：**

- 需求还不太清楚的新功能，需要先讨论清楚再动手
- 多步骤的实现任务，希望有计划、有测试、可审查
- 反复修不好的 bug，需要按步骤找根因

**不太适合：**

- 改个错别字、调一个配置值这种一句话任务，流程开销比任务本身大
- 你已经写好了详细计划，只需要 Codex 照做

在桌面端想点名用某个 Skill，可以按官方插件文档的说法，在输入框里输入 `@` 选择插件或它的某个 Skill。暂时不想要这套流程时，在 CLI 的 `/plugins` 里选中插件按空格键关掉，或者把 `config.toml` 里对应插件的 `enabled` 改成 `false`。实测改成 `false` 后，`codex plugin list` 显示 `installed, disabled`。

`subagent-driven-development` 和 `dispatching-parallel-agents` 需要子 agent 能力。项目移植文档写明，没有子 agent 工具时，这两个 Skill 会让模型改为在当前会话里完成，或者说明缺少这个能力。Codex 的子 agent 用法见 [Codex Subagents 并行处理任务](https://codexguide.io/guides/codex-subagents-parallel-work)。

## 会话出问题时

如果某个 Skill 该触发没触发、计划被忽略、重复做工或者花费异常，可以直接对 Codex 说：

```text
figure out what went wrong with superpowers in this session
```

它会调用 `diagnosing-superpowers`，读会话记录，给出带行号证据的分析；你同意的话，还能打包一份脱敏后的数据用于提交问题。

## 遥测和卸载

**遥测**：README 说明，brainstorming 的可选“视觉伴侣”功能里，Prime Radiant 的 logo 默认从他们的网站加载，请求里带 Superpowers 的版本号，不包含项目、提示词或 agent 的信息。要关闭，设置环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 为任意真值。

**卸载**：在 `/plugins` 插件浏览器里卸载，或者用命令行。实测：

```bash
codex plugin remove superpowers@superpowers-dev
```

```text
Removed plugin `superpowers` from marketplace `superpowers-dev`.
```

卸载后 `codex plugin list` 显示 `not installed`，`config.toml` 里的 `[plugins."superpowers@superpowers-dev"]` 被删掉，但 `[marketplaces.superpowers-dev]` 还在；不再需要这个市场时，用 `codex plugin marketplace remove superpowers-dev` 移除。

## 参考资料

- [OpenAI 官方文档：Plugins](https://learn.chatgpt.com/docs/plugins)
- [Codex 官方插件目录 openai/plugins](https://github.com/openai/plugins)
- [obra/superpowers](https://github.com/obra/superpowers)
- [Superpowers 发布说明](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md)
