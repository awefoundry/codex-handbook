---
id: codex-compound-engineering-plugin
title: "Codex 安装 Compound Engineering 插件：用 codex plugin marketplace add 装好 38 个 Skills，按头脑风暴、计划、实现、审查、沉淀走一轮"
seo_title: "Codex 安装 Compound Engineering：38 个 Skill 与装法"
description: "Compound Engineering 是 Every 维护的第三方 MIT 插件，不是 OpenAI 官方功能。本文用 Codex CLI 0.172.0 在独立 CODEX_HOME 里装上 3.38.3 的 38 个 Skill，并说明哪些会改仓库或开 PR。"
lede: "先看清是谁的仓库、会写进哪些目录，再用独立的 CODEX_HOME 试装。装上不等于已经在你的项目里跑过 ce-work 或 lfg。"
url: /guides/codex-compound-engineering-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI]
difficulty: 进阶
order: 31
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-26
date_modified: 2026-11-26
verified_on: 2026-11-26
tested_cli_version: 0.172.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex Compound Engineering, compound-engineering-plugin, Codex 插件, ce-plan, ce-compound]
related: [codex-superpowers-plugin, codex-mattpocock-skills, codex-skillspector-skill-security-scan]
howto: true
faq:
  - q: "这是 OpenAI 官方插件吗？"
    a: "不是。仓库 EveryInc/compound-engineering-plugin 由 Every 的 Kieran Klaassen 和 Trevin Chow 维护，许可证是 MIT。Codex 只是 README 写明可以安装的对象之一。"
  - q: "装好就是 38 个吗？"
    a: "2026-11-26 装到的 3.38.3 里，skills 目录下有 38 个技能目录，和 README 的数字一致。未登录的 codex debug prompt-input 列出其中 29 个。另外 9 个的 SKILL.md 写了 disable-model-invocation: true，这次没有出现在 prompt-input 里。"
  - q: "装完会自动改我的仓库或开 PR 吗？"
    a: "这次安装只写了独立 CODEX_HOME 里的 config.toml 和插件缓存，没有在业务仓库里发送任何 Skill。ce-commit、ce-commit-push-pr、lfg 等技能的 description 写明会提交、推送或打开 PR。没有在会话里点名之前，不要假定它们已经改过文件。"
  - q: "和 Superpowers、Matt Pocock Skills 怎么分？"
    a: "三套都是第三方工程流程，作者和仓库不同。Compound Engineering 把一轮工作收成头脑风暴、计划、实现，再把教训写回仓库。命令和技能名不要混用。"
---

# Codex 安装 Compound Engineering 插件：用 codex plugin marketplace add 装好 38 个 Skills，按头脑风暴、计划、实现、审查、沉淀走一轮

> 本文在线版：[codexguide.io/guides/codex-compound-engineering-plugin](https://codexguide.io/guides/codex-compound-engineering-plugin)

> 核对依据：第三方仓库 [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) 的 README、[MIT 许可证](https://github.com/EveryInc/compound-engineering-plugin/blob/main/LICENSE)，以及装到磁盘的 `.codex-plugin/plugin.json` 和各 `SKILL.md` 的 frontmatter。2026-11-26 的 GitHub API：26,236 star，2,057 fork，许可证 MIT，`pushed_at` 为 `2026-11-26T01:14:51Z`。commits API 最新一条和装到磁盘的检出都是 `fcb5e3adc1890db34f482f73e2449f3c57a2f423`，提交说明 `chore: release main (#2087)`，提交者时间 `2026-11-23T23:50:38Z`。最新 Release [compound-engineering-v3.38.3](https://github.com/EveryInc/compound-engineering-plugin/releases/tag/compound-engineering-v3.38.3) 的 `published_at` 是 `2026-11-23T23:51:00Z`。Codex CLI 为 `@openai/codex@0.172.0`，`codex --version` 为 `codex-cli 0.172.0`。插件命令在未登录的独立 `CODEX_HOME` 里运行。没有打开交互式会话，没有按 SKILL.md 改仓库，没有配图。

这是 **Every** 维护的一套 Agent Skills，不是 OpenAI 的内置工程流程。README 把它写成 38 个技能的插件，跑在 14 个 Agent 宿主上，其中包括 Claude Code、Cursor 和 Codex。维护者是 Kieran Klaassen 和 Trevin Chow。Codex 会不会按这些文件改你的项目，取决于它有没有读到对应的 `SKILL.md`、当前会话能不能调用它，以及你有没有允许它改文件和访问网络。

另一套「先问需求、再写计划、测试先行」的第三方插件是 [Superpowers](../08-插件工作流/07-Codex安装Superpowers插件-需求计划TDD工作流.md)。小技能、按仓库先跑 setup 的是 [Matt Pocock Skills](./30-Codex安装Matt-Pocock-Skills插件-装好工程Skills先跑setup再用tdd与code-review.md)。作者、仓库和命令都不同，不要混用。装进会改文件的仓库之前，先看 [用 SkillSpector 扫描第三方 Skill](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。

## 先说结论

2026-11-26 在独立 `CODEX_HOME`、未登录的 Linux 上：

1. `codex plugin marketplace add EveryInc/compound-engineering-plugin` 添加了名为 `compound-engineering-plugin` 的 Git 市场，来源是 `https://github.com/EveryInc/compound-engineering-plugin.git`。
2. `codex plugin add compound-engineering@compound-engineering-plugin` 装上的版本是 **3.38.3**。`skills/` 下有 **38** 个技能目录，和 README 的数字一致。
3. 未登录的 `codex debug prompt-input` 列出其中 **29** 个、前缀为 `compound-engineering:` 的名字。另外 9 个的 `SKILL.md` 写了 `disable-model-invocation: true`，没有出现在这次的 prompt-input 里。

`.codex-plugin/plugin.json` 的 `interface.capabilities` 是 `Read` 和 `Write`。`developerName` 是 Kieran Klaassen and Trevin Chow。隐私政策和条款网址都写成 `https://every.to/legal`（2026-11-26 返回 200）。这份清单的字段里没有 `mcpServers` 或 hooks。

README 顶部的订阅徽章和 Every Frontier 链接是作者自己的推广。本文不把它们写成安装步骤，也不放那些链接。

没有在已登录的会话里发送 `$ce-brainstorm`、`$ce-plan`、`$ce-work`、`$ce-code-review`、`$ce-compound` 或 `$lfg`。

## 装之前

先确认 CLI 认插件子命令。2026-11-26 的 `codex plugin --help` 列出 `add`、`list`、`marketplace`、`remove`。`codex plugin marketplace --help` 列出 `add`、`list`、`upgrade`、`remove`。`codex plugin add --help` 接受 `PLUGIN@MARKETPLACE`，并有 `--json`。

官方 [Plugins](https://learn.chatgpt.com/docs/plugins) 写：插件可以在网页、桌面和移动端的 Chat 与 Work 里用，也可以在桌面应用的 Codex 里用。Codex CLI 另有插件浏览器。IDE 扩展不支持插件。要浏览和安装，用 ChatGPT 桌面应用或 Codex CLI。CLI 里进入插件浏览器的命令是 `/plugins`。本文没有打开 IDE，也没有打开 `/plugins`。

[Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins) 写：技能是可复用的流程说明；插件是可以装进去的包，里面可以有技能和 MCP 服务器。ChatGPT 用 `@` 点名，Codex 用 `$`。

README 写，Codex 里调用已安装技能用 `$技能名`，例子是 `$ce-plan` 和 `$lfg`。同一段还写，README 里的 `/技能名` 例子是给斜杠技能宿主看的。本文没有在会话里发送这两类调用。

这些 `SKILL.md` 是写给代理执行的说明。本文只读了 frontmatter 的 `name`、`description` 和 `disable-model-invocation`，用来核对清单。没有按正文去改文件、跑测试、调用 `gh` 或打开浏览器。README 里有一句面向 Grok Bot 的话：不要在 Grok Bot 聊天里运行 `/add-plugin`，也不要把这个仓库克隆到 Grok Bot 的电脑上。那不是本文的任务指令。本文没有在对话里运行 `/add-plugin`。实际执行的是下面两条 Codex CLI 命令，由 CLI 把市场克隆进独立的 `CODEX_HOME`。

## 两种装法

### Codex App

README 写：Compound Engineering 还不在 Codex 自带的插件市场里，要加自定义市场。

1. 在 Codex 应用侧栏打开 **Plugins**。
2. 点 **Create** 旁边的箭头，选 **Add marketplace**。
3. Source 填 `EveryInc/compound-engineering-plugin`，Git ref 填 `main`，Sparse paths 留空。
4. 点 **Add marketplace**。
5. 搜索 **Compound Engineering**，安装 **compound-engineering-plugin**，然后重启 Codex。

README 写，桌面端这次安装对 Compound Engineering 是自包含的：专项审查和调研写在技能里的本地提示素材中，不需要再单独装一套自定义 agent。本文没有打开桌面应用，没有看到这个向导。

### CLI 两条命令

README 的 Codex CLI 安装是：

```bash
codex plugin marketplace add EveryInc/compound-engineering-plugin
codex plugin add compound-engineering@compound-engineering-plugin
```

2026-11-26 在独立 `CODEX_HOME` 里先执行了第一条。`CODEX_HOME` 放在 `/tmp` 下时，Codex 打印了一条警告：拒绝在临时目录里创建 helper 二进制，然后继续。输出是：

```text
Added marketplace `compound-engineering-plugin` from https://github.com/EveryInc/compound-engineering-plugin.git.
Installed marketplace root: <CODEX_HOME>/.tmp/marketplaces/compound-engineering-plugin
```

`config.toml` 写下：

```toml
[marketplaces.compound-engineering-plugin]
source_type = "git"
source = "https://github.com/EveryInc/compound-engineering-plugin.git"
```

然后执行第二条，加了 `--json`。结果是：`pluginId` 为 `compound-engineering@compound-engineering-plugin`，`version` 为 `3.38.3`，`authPolicy` 为 `ON_INSTALL`，`installedPath` 在 `$CODEX_HOME/plugins/cache/compound-engineering-plugin/compound-engineering/3.38.3`。这次没有登录，命令没有出现交互式认证提示。清单里的 `ON_INSTALL` 被原样印了出来。已登录会话会不会再问一次，本文没有看到。

装完后 `config.toml` 多了：

```toml
[plugins."compound-engineering@compound-engineering-plugin"]
enabled = true
```

`codex plugin list` 的状态是 `installed, enabled`，版本 `3.38.3`。市场检出和缓存用的 Git 提交都是 `fcb5e3adc1890db34f482f73e2449f3c57a2f423`。

接着执行 `codex plugin marketplace upgrade`，输出是 “Upgraded 1 marketplace(s)”。版本号没有变成另一版。

`plugin.json`（仓库根和 `.codex-plugin/plugin.json`）的 `name` 是 `compound-engineering`，`version` 是 `3.38.3`，`license` 是 MIT，`author.name` 是 Kieran Klaassen and Trevin Chow。描述是：Brainstorm, plan, debug, review, and compound learnings with AI agents。Codex 这份清单的 `skills` 字段是字符串 `./skills/`，不是一份 38 项的数组。38 这个数来自 `skills/` 目录里的技能文件夹，不是来自一个写死的数组。

官方 Plugins 页写，捆绑的技能在你新开一个对话或 CLI 会话时可用。README 写装完要重启 Codex。本文没有启动交互式 Codex，所以两种说法都没有在会话里观察。

非默认 profile 时，README 要求每条 Codex 命令都带同一个 `CODEX_HOME`。它的例子是：

```bash
CODEX_HOME="$HOME/.codex/profiles/work" codex plugin marketplace add EveryInc/compound-engineering-plugin
CODEX_HOME="$HOME/.codex/profiles/work" codex plugin add compound-engineering@compound-engineering-plugin
```

本文用的是一个临时的 `CODEX_HOME`，不是 `profiles/work`。机制相同：市场和插件写进你指定的那一份配置，不会自动出现在另一个 profile。

## 插件里有哪些 Skills

下面 38 个的用途，译自装到磁盘的 `SKILL.md` frontmatter 里的 `description`。英文名保持原样，方便和 `$` 对照。分组沿用 README 的目录，方便和上游对照；某一项该不该用，以 description 为准，不按名字猜。标了「需点名」的，frontmatter 含 `disable-model-invocation: true`，并且没有出现在这次的 prompt-input 里。

### 主循环，4 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-brainstorm` | 可被模型选用 | 把模糊或很大的想法收成一份只含需求、规模合适的统一计划。用来头脑风暴或划定要做什么。不用于执行已经写清的工作。要判断要不要采用某项外部技术，用 `ce-pov` |
| `ce-plan` | 可被模型选用 | 为多步工作写结构化计划，包括软件和非软件任务。用来计划、拆实现、从需求做计划，或把已有计划写深。探索性的框定优先用 `ce-brainstorm` |
| `ce-work` | 可被模型选用 | 把一份计划或明确的工作提示做到底。从计划文档、规格路径或清楚的构建请求来实现。开放式的 bug 用 `ce-debug`。外层编排只要实现和本地验证、不要发布那一段时也用它 |
| `ce-compound` | 可被模型选用 | 把一次已解决的问题，用最省的耐久形式记下来：测试、lint 规则、编码标准或仓库里的一条学习；也可以对照代码库刷新已有学习。用在验证过的工作纠正了错误看法时。按原计划做成的工作不要自动调用 |

### 围绕主循环，5 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-strategy` | 可被模型选用 | 创建或更新 `STRATEGY.md`。开始一个产品、补策略文档，或改变方向和路线图时用 |
| `ce-product-pulse` | 需点名 | 从已配置的信号生成一个时间窗口的产品脉搏报告 |
| `ce-sweep` | 需点名 | 扫配置好的反馈来源（Slack、GitHub Issues；邮件是实验性的）：在来源处确认，分析记录，核对修复是否已合并到 main，并产出一份可以交给 `lfg` 的计划。第一次运行会设置来源 |
| `ce-retro` | 可被模型选用 | 回顾这个仓库里的一次代理会话，找出环境里哪些东西在让代理多花力气或走错。只留下证据表明值得做的修复，落地已批准的环境修复，其余交给负责人。一次已解决问题的教训用 `ce-compound`，产品代码里的 bug 用 `ce-debug` |
| `ce-compound-refresh` | 可被模型选用 | 刷新学习的旧名字，现在做这件事的是 `ce-compound`。只有提示或常驻说明点名 `ce-compound-refresh` 时才用它 |

### 按需，10 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-ideate` | 可被模型选用 | 产生并评估有依据的想法。要的是改进或没想到的方向，还没选定要展开哪一个。已经有的想法用 `ce-brainstorm` 来收，已经摆在桌上的方案用 `ce-pov` 来判断 |
| `ce-bakeoff` | 可被模型选用 | 对一份已经定义的简报，各自做出互相独立的方案，比较之后合成一个胜出的做法。判断已经写出来的材料用 `ce-pov`，发现机会用 `ce-ideate` |
| `ce-pov` | 可被模型选用 | 按项目里的证据和约束判断一个给定对象。也可以做 oracle 面板：询问其他模型再调和意见。要理解用 `ce-explain`，要审发现用 `ce-doc-review` |
| `ce-debug` | 可被模型选用 | 对 bug 和失败行为做诊断循环。被要求调试，或要修失败、变慢的行为时用 |
| `ce-explain` | 可被模型选用 | 根据证据说明一件事为什么是现在这个样子，或一段工作里发生了什么。要判断或建议用 `ce-pov` |
| `ce-simplify-code` | 可被模型选用 | 在保持行为的前提下简化代码，并删掉没有价值的测试和注释。实现之后、审查之前用；也可以审计仓库里任意部分的测试或注释。bug 用 `ce-debug` |
| `ce-code-review` | 可被模型选用 | 审查指定的 diff 或 PR，看 bug、回归、测试和标准。也可以在被要求时把这次审查的发现应用到本地。PR 上已经留下的反馈用 `ce-resolve-pr-feedback` |
| `ce-doc-review` | 可被模型选用 | 用分角色的视角审查需求、计划或规格。想改进一份已有的计划文档时用 |
| `ce-optimize` | 可被模型选用 | 对一个指名的目标做测量循环：归因开销，或给变体打分并留下胜出的。改动已经知道时用 `ce-work`，要诊断时用 `ce-debug` |
| `ce-prototype` | 可被模型选用 | 做一个用完即弃的原型，用来回答某件事应该怎么工作、怎么感觉或怎么读。不是头脑风暴里的草图，不是决定做什么，也不是把已经能用的功能磨光，更不是实现正式版本 |

### Git 与 PR，5 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-commit` | 可被模型选用 | 用一条说得清价值的信息做 git commit。用户要求提交已暂存或未暂存的改动时用 |
| `ce-commit-push-pr` | 可被模型选用 | 提交、推送并打开 PR。用户要求发布或打开 PR 时用；也可以只写、改写或描述 PR 正文 |
| `ce-babysit-pr` | 可被模型选用 | 照看一个未合并的 GitHub PR，直到可以合并，并先判断一个旧 PR 是否还该留着。用来长时间看着一个 PR，或更新一个旧的。不是一次性处理评论，也不是处理单次 CI 失败。只支持 GitHub（含 Enterprise） |
| `ce-resolve-pr-feedback` | 可被模型选用 | 集中判断 PR 反馈，应用站得住的修复，并在确认发表之后结束审查对话。处理已经留在 PR 上的反馈。代码还没有反馈时用 `ce-code-review` |
| `ce-worktree` | 可被模型选用 | 建隔离的 git worktree：为新工作开分支，或把 worktree 接到已有分支、PR 或提交 |

### 无人值守，1 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `lfg` | 可被模型选用 | 把一个请求按合适的 Compound Engineering 技能做到结束，中途不交人。代码改动的终点是一个已经推送、打开的 pull request。只在用户明确要求端到端自主完成，或直接调用 `lfg` 时用。要一步步看，就用 `ce-plan`、`ce-work`、`ce-debug` 或 `ce-commit-push-pr` |

### 测试与打磨，4 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-test-browser` | 可被模型选用 | 对当前分支或 PR 影响到的页面跑浏览器测试 |
| `ce-test-xcode` | 需点名 | 用 XcodeBuildMCP 在模拟器里测 iOS 应用。iOS 改动在交接前需要模拟器证据时用 |
| `ce-polish` | 需点名 | 通过用户指导的实时浏览器反馈，打磨一个已经能用的功能。功能需要在发布前做聚焦的体验修改时用 |
| `ce-dogfood` | 需点名 | 对当前分支做无人值守、按 diff 范围的浏览器验收：画出用户流程，驱动真实浏览器，用回归测试和提交自动修小破损，按产品角色判断体验，并写一份耐久的 dogfood 报告。只手动调用 |

### 协作，3 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-proof` | 可被模型选用 | 在 Proof 里发布、阅读、评论或编辑 Markdown。用于 Proof 链接、分享规格、计划或草稿。不要理解成校对、数学证明或概念验证 |
| `ce-handoff` | 可被模型选用 | 给另一个代理写会话交接，或恢复、查找并阅读用户选定的延续材料。当前会话历史带不过去时用 |
| `ce-promote` | 需点名 | 为一个已经发布的功能起草发布或推广文案 |

### 工具，6 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ce-help` | 需点名 | 说明 Compound Engineering：把你正在做的事放到这套循环上，并建议下一条命令，但不运行它 |
| `ce-setup` | 可被模型选用 | 检查 Compound Engineering 的工具和仓库配置，并修它发现的问题；用 `pack:<id>` 搭一个 Compound Pack；或从 PR 历史起草、刷新编码标准和审查文档。设置、排障，或创建、更新 `CODING_STANDARDS.md`、`REVIEW.md` 时用 |
| `ce-noslop` | 可被模型选用 | 重写、检查或起草文字，去掉它认定的 AI 写作痕迹，并保留每一条来源事实。渠道文案用 `ce-promote` |
| `wtf` | 需点名 | 用第一遍就能读懂的话解释上一条消息，或一份给定的文件、链接、段落。用户因为没看懂而调用 `wtf` 时用。要调查代码为什么这样工作，用 `ce-explain` |
| `ce-retune` | 需点名 | 为新模型重调一套技能语料，先测量再改。需要能对两份语料做 A/B 的基准工具，没有就不做 |
| `ce-riffrec-feedback-analysis` | 可被模型选用 | 把录下来的产品反馈分析成 bug 和需求的证据。用于 Riffrec 采集，或其他屏幕、语音、笔记材料 |

2026-11-26 的 `codex debug prompt-input` 在一个空目录上列出的 29 个是上表里「可被模型选用」的全部，前缀为 `compound-engineering:`。9 个「需点名」没有出现。这次输出把目录放在测试用的 `CODEX_HOME` 下面，正文不写那台机器的用户路径。没有打开斜杠菜单，所以没有看到 `$` 点名时这 9 个是否出现。

同一份检出的 `skills/` 里还有一份 `CODING_STANDARDS.md`，它不是技能目录，没有算进 38。`.agents/skills/ce-skill-work` 也不在 `skills/` 下，prompt-input 没有列出它。`tests/` 里的示例技能同样没有算进来。

## 一轮小功能怎么走

README 把主循环写成四步：头脑风暴需求，计划实现，按计划做（它写 `ce-work` 会在开 PR 之前简化和审查自己写的 diff），再用 `ce-compound` 把学到的东西记下来。

`ce-work` 的 description 和这句不完全一样。description 写：外层编排只要实现和本地验证、不要发布那一段时，用 `ce-work`。README 写 `/ce-work` 会在打开 PR 之前简化和审查。本文没有在会话里跑它，看不到实际停在本地验证还是会开 PR。要人一步步看，就不要用 `lfg`。`lfg` 的 description 写明：代码改动的终点是一个已经推送、打开的 pull request，而且只在你明确要求端到端自主完成或直接调用它时使用。

README 还写，装好之后在任意项目里跑 `/ce-setup`。它会报告可选工具的能力，缺少时创建仓库里的 `.compound-engineering/config.yaml`，刷新已提交的示例，并把已有的本地覆盖写进 gitignore。装到磁盘的 description 写得更进一步：它会修它发现的问题，并能起草 `CODING_STANDARDS.md` 和 `REVIEW.md`。本文没有跑 `ce-setup`，也没有在任何仓库里创建那份配置。

如果你要在自己的已登录会话里试，把范围写进提示里。下面是提示词示例，不是本文发送过的内容：

```text
请使用 ce-brainstorm。只讨论，不改文件，不提交。
想法：给当前仓库的 README 加一节「本地怎么跑测试」。
先列出你需要我确认的问题。不要调用 ce-work 或 lfg。
```

计划阶段可以接着写：请使用 `ce-plan`，只根据已经确认的需求写计划，仍然不改代码。实现阶段再单独决定要不要使用 `ce-work`，并写明不要推送、不要开 PR。审查用 `ce-code-review` 时，写明只出发现、不要把发现应用到本地，除非你再批一次。沉淀用 `ce-compound` 时，先让它说明准备写到哪个路径，你看过再允许写入。

README 写，`ce-compound` 默认把学习写到 `docs/solutions/`，计划在 `docs/plans/`。项目的 `docs/` 如果已经是被跟踪的内容，可以用 `docs_root` 把这些目录挪到一个仓库相对路径下。本文没有打开配置指南里的字段表，不编 `docs_root` 的写法。

## 更新、停用与卸载

这次测试执行了 `codex plugin marketplace upgrade`，版本仍是 3.38.3。没有执行卸载，所以测试用的 `config.toml` 里市场和 `enabled = true` 都还在。

2026-11-26 的帮助文本里，卸插件是：

```bash
codex plugin remove compound-engineering@compound-engineering-plugin
```

卸市场来源是：

```bash
codex plugin marketplace remove compound-engineering-plugin
```

两条都支持 `--json`。非默认 profile 要带和安装时相同的 `CODEX_HOME`。本文没有跑这两条，所以没有看到它们会不会留下缓存目录。

官方 Plugins 页写，捆绑技能要新开对话或 CLI 会话才会出现。换版本之后，至少新开一次会话再看 `prompt-input` 或 `/plugins`，不要假定旧会话已经换了技能正文。

## 安全

这是第三方技能包。许可证是 MIT，不表示 OpenAI 审查过每一份 `SKILL.md`。Codex 清单写明能力包括 Read 和 Write。装到磁盘之后，下面这些技能的 description 已经写明会动仓库、提交或开 PR：

- `ce-commit` 会做 git commit。
- `ce-commit-push-pr` 会提交、推送并打开 PR。
- `lfg` 把代码改动做到一个已推送的开放 PR，并且写明中途不停下。
- `ce-resolve-pr-feedback` 会应用它认为站得住的修复。
- `ce-dogfood` 写明会用回归测试和提交自动修小破损。它标了只手动调用。
- `ce-setup` 会修它发现的配置问题，并能写标准文档。
- `ce-compound` 会把教训写成测试、lint、标准或仓库里的学习。
- `ce-strategy` 会创建或更新 `STRATEGY.md`。
- `ce-work` 会按计划实现。
- `ce-simplify-code` 会改代码并删测试或注释。
- `ce-worktree` 会建分支或 worktree。
- `ce-retro` 会落地已批准的环境修复。
- `ce-sweep` 会在反馈来源处确认，并产出计划。

没有在会话里点名，这些文件只是躺在插件缓存里。点名之后，它们是否真的执行，还取决于当前沙箱和审批。不要用全文访问或关掉沙箱来「让插件跑通」。

装进日常使用的 `CODEX_HOME` 之前，用 [SkillSpector](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md) 扫一遍这份检出。本文没有跑那次扫描，不能用「已经装上」代替扫描结果。

## 参考资料

- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
- [Release compound-engineering-v3.38.3](https://github.com/EveryInc/compound-engineering-plugin/releases/tag/compound-engineering-v3.38.3)
- [MIT 许可证](https://github.com/EveryInc/compound-engineering-plugin/blob/main/LICENSE)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
