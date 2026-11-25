---
id: codex-mattpocock-skills
title: "Codex 安装 Matt Pocock Skills 插件：用 codex plugin marketplace add 装好 27 个工程 Skills，先跑 setup 再用 tdd、to-spec 和 code-review"
seo_title: "Codex 安装 Matt Pocock Skills：27 个工程 Skill 与 setup"
description: "Matt Pocock 的 Skills 是第三方 MIT 插件，不是 OpenAI 官方功能。本文用 Codex CLI 0.172.0 装上 1.3.2 的 27 个 Skill，说明先跑 setup，以及 tdd、to-spec、code-review 和第三方风险。"
lede: "先看清是谁的仓库、会写进哪些目录，再用独立的 CODEX_HOME 试装。装上不等于已经在你的项目里跑过 TDD。"
url: /guides/codex-mattpocock-skills
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI]
difficulty: 进阶
order: 30
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-25
date_modified: 2026-11-25
verified_on: 2026-11-25
tested_cli_version: 0.172.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex Matt Pocock Skills, mattpocock skills, Codex 工程 Skills, codex plugin add, Codex TDD Skill]
related: [codex-skills-install-guide, codex-skillspector-skill-security-scan, codex-superpowers-plugin]
howto: true
faq:
  - q: "这是 OpenAI 官方插件吗？"
    a: "不是。仓库 mattpocock/skills 由 Matt Pocock 维护，许可证是 MIT。Codex 只是 README 写明可以安装的对象之一。"
  - q: "插件里是 27 个还是仓库里每一份 SKILL.md？"
    a: "2026-11-25 装到的 1.3.2 里，.claude-plugin/plugin.json 列出 27 个，工程 20 个、效率 7 个。同一份检出里还有 in-progress 8 个和 misc 4 个，不在这份清单里。deprecated 目录的 README 写明目前是空的。"
  - q: "可以和 skills.sh 的安装一起用吗？"
    a: "README 写 Pick one per agent。插件会在启动时自己更新；skills.sh 是把可编辑文件复制进项目、要手动更新。两种都装，每个技能会出现两次。"
  - q: "装完会自动改我的仓库吗？"
    a: "本文没有登录，也没有在会话里发送 setup、tdd 或 code-review。setup 的说明写明它会在你确认后写入 issue tracker 配置和 AGENTS.md 或 CLAUDE.md。没有确认之前，不要假定它已经改过文件。"
---

# Codex 安装 Matt Pocock Skills 插件：用 codex plugin marketplace add 装好 27 个工程 Skills，先跑 setup 再用 tdd、to-spec 和 code-review

> 本文在线版：[codexguide.io/guides/codex-mattpocock-skills](https://codexguide.io/guides/codex-mattpocock-skills)

> 核对依据：第三方仓库 [mattpocock/skills](https://github.com/mattpocock/skills) 的 README、[MIT 许可证](https://github.com/mattpocock/skills/blob/main/LICENSE) 和装到磁盘的 `.claude-plugin/plugin.json`。2026-11-25 的 GitHub API：332,199 star，27,924 fork，许可证 MIT，`pushed_at` 为 `2026-11-24T14:43:16Z`。检出的最新提交是 `d65391149dbb5fe76478e76fa8d5122b2aa5a70e`，时间 `2026-11-24T14:43:03Z`，说明为 `Merge pull request #1474 from mattpocock/chief-of-staff-soften`。Codex CLI 为 `@openai/codex@0.172.0`，`codex --version` 为 `codex-cli 0.172.0`。插件命令在未登录的独立 `CODEX_HOME` 里运行。没有打开交互式会话，没有按 SKILL.md 改仓库，没有配图。

这是 **Matt Pocock** 维护的一套 Agent Skills，不是 OpenAI 的内置工程流程。README 把它写成给日常工程用的小技能，可以组合，而不是由一套总流程把整个开发过程接走。Codex 会不会按这些文件改你的项目，取决于它有没有读到对应的 `SKILL.md`、当前会话能不能调用它，以及你有没有允许它改文件和访问 issue tracker。

三种安装路径的分工，见 [Codex Skills 怎么安装](../07-Skills实战/11-Codex-Skills怎么安装-三种方式完整流程.md)。装进会改文件的仓库之前，先看 [用 SkillSpector 扫描第三方 Skill](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。另一套「先问需求、再写计划、测试先行」的第三方插件是 [Superpowers](../08-插件工作流/07-Codex安装Superpowers插件-需求计划TDD工作流.md)，作者和仓库都不同，不要把两边的命令混用。

## 先说结论

2026-11-25 在独立 `CODEX_HOME`、未登录的 Linux 上：

1. `codex plugin marketplace add mattpocock/skills` 添加了名为 `mattpocock` 的 Git 市场，来源是 `https://github.com/mattpocock/skills.git`。
2. `codex plugin add mattpocock-skills@mattpocock` 装上的版本是 **1.3.2**。`plugin.json` 的 `skills` 数组是 **27** 项：`skills/engineering` 20 个，`skills/productivity` 7 个。
3. 未登录的 `codex debug prompt-input` 只列出其中 **11** 个、前缀为 `mattpocock-skills:` 的名字。这 11 个的 `SKILL.md` 没有写 `disable-model-invocation: true`。另外 16 个写了这个字段，没有出现在这次的 prompt-input 里。

仓库里另外有 `skills/in-progress` 8 份 `SKILL.md` 和 `skills/misc` 4 份，不在 `plugin.json` 里。`skills/deprecated/README.md` 写明这个目录目前是空的：退役的技能会被删掉，而不是留在插件清单中。

README 的 newsletter 报名是作者自己的推广，链接在文末标成推广链接。本文不把它写成安装步骤。

没有在已登录的会话里发送 `/setup-matt-pocock-skills`、`$tdd` 或 `$code-review`。

## 装之前

先确认 CLI 认插件子命令。2026-11-25 的 `codex plugin --help` 列出 `add`、`list`、`marketplace`、`remove`。`codex plugin marketplace --help` 列出 `add`、`list`、`upgrade`、`remove`。

官方 [Plugins](https://learn.chatgpt.com/docs/plugins) 写：IDE 扩展不支持插件。要浏览和安装插件，用 ChatGPT 桌面应用、网页，或 Codex CLI。本文没有打开 IDE，也没有打开桌面应用。

[Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins) 写：技能是可复用的流程说明；插件是可以装进去的包，里面可以有技能和 MCP 服务器。ChatGPT 用 `@` 点名，Codex 用 `$`。这次安装的 `plugin.json` 没有 `mcpServers` 或 hooks 字段。

README 写，插件和 [skills.sh](https://skills.sh/mattpocock/skills) 二选一。插件会在启动时自己更新；skills.sh 把可编辑文件复制进项目，更新要自己来。同一个代理两种都装，每个技能会有两份。本文只走了插件这两条命令，没有运行 `npx skills add`。

这些 `SKILL.md` 是写给代理执行的说明。本文只读了 frontmatter 的 `name`、`description` 和 `disable-model-invocation`，用来核对清单。没有按正文去改文件、跑测试、调用 `gh` 或 `glab`。`diagnosing-bugs` 的正文把 curl 写成一种可以暴露 bug 的命令例子，本文没有执行。

## 两条命令装好插件

README 的 Codex 安装是：

```bash
codex plugin marketplace add mattpocock/skills
codex plugin add mattpocock-skills@mattpocock
```

README 写插件 **Updates itself at startup**。2026-11-25 在独立 `CODEX_HOME` 里先执行了第一条。输出是：

```text
Added marketplace `mattpocock` from https://github.com/mattpocock/skills.git.
Installed marketplace root: <CODEX_HOME>/.tmp/marketplaces/mattpocock
```

`config.toml` 写下：

```toml
[marketplaces.mattpocock]
source_type = "git"
source = "https://github.com/mattpocock/skills.git"
```

然后执行第二条。`--json` 的结果是：`pluginId` 为 `mattpocock-skills@mattpocock`，`version` 为 `1.3.2`，`authPolicy` 为 `ON_INSTALL`，`installedPath` 在 `$CODEX_HOME/plugins/cache/mattpocock/mattpocock-skills/1.3.2`。这次没有登录，命令没有出现交互式认证提示。清单里的 `ON_INSTALL` 被原样印了出来。已登录会话会不会再问一次，本文没有看到。

装完后 `config.toml` 多了：

```toml
[plugins."mattpocock-skills@mattpocock"]
enabled = true
```

`codex plugin list` 的状态是 `installed, enabled`，版本 `1.3.2`。缓存和市场上的 Git 提交都是 `d65391149dbb5fe76478e76fa8d5122b2aa5a70e`。

接着执行 `codex plugin marketplace upgrade`，输出是 “Upgraded 1 marketplace(s)”。版本号没有变成另一版。没有启动交互式 Codex，所以没有观察 README 说的「启动时自动更新」。

`plugin.json` 的 `name` 是 `mattpocock-skills`，`license` 是 MIT，`author.name` 是 Matt Pocock。描述写的是 grilling、规格和工单、TDD、代码审查、领域建模等工程技能。

## 插件里有哪些 Skills

下面 27 个的用途，译自装到磁盘的 `SKILL.md` frontmatter 里的 `description`。英文名保持原样，方便和 `/` 或 `$` 对照。标了「需点名」的，frontmatter 含 `disable-model-invocation: true`。

### 工程，20 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `ask-matt` | 需点名 | 问当前情况该用哪个技能或流程，是这套技能的路由 |
| `grill-with-docs` | 需点名 | 追问计划和设计，并在过程中写下 ADR 和术语表 |
| `triage` | 需点名 | 把 issue 和外部 PR 按分诊角色往下推，分类、核实，必要时追问，写成代理能执行的简报 |
| `improve-codebase-architecture` | 需点名 | 扫描可以加深模块的地方，做成 HTML 报告，再对你选中的一项追问 |
| `setup-matt-pocock-skills` | 需点名 | 配置 issue tracker、分诊标签和领域文档位置。其他工程技能第一次使用前先跑一次 |
| `to-spec` | 需点名 | 把当前对话收成规格，发布到项目的 issue tracker。不再追问，只综合已经讨论过的内容 |
| `to-tickets` | 需点名 | 把计划、规格或当前对话拆成带阻塞关系的工单，写到已配置的 tracker |
| `implement` | 需点名 | 按一份规格或一组工单实现一块工作 |
| `implement-spec` | 需点名 | 把 `/to-spec` 和 `/to-tickets` 的结果实现成代码 |
| `wayfinder` | 需点名 | 把一次会话装不下的大块工作，画成 tracker 上的决策工单，一次解决一个 |
| `retro` | 需点名 | 对一次编码会话做回顾 |
| `prototype` | 可被模型选用 | 做一次性原型，用来检查状态、逻辑或界面方向 |
| `diagnosing-bugs` | 可被模型选用 | 难 bug 和性能回退的诊断循环。用户说 diagnose、debug，或报告失败、变慢时用 |
| `research` | 可被模型选用 | 对照一手来源调查问题，把发现写成仓库里的 Markdown |
| `tdd` | 可被模型选用 | 测试先行。用户要 red-green-refactor，或要集成测试时用 |
| `domain-modeling` | 可被模型选用 | 收紧领域模型。讨论术语、写 `GLOSSARY.md` 或 ADR 时用 |
| `codebase-design` | 可被模型选用 | 设计深模块时用的共用词汇：接口、接缝、可测试性 |
| `code-review` | 可被模型选用 | 从某个提交、分支、标签或 merge-base 起审查。Standards 和 Spec 两条并行 |
| `pr` | 可被模型选用 | 写 PR 正文时用 |
| `wizard` | 可被模型选用 | 生成 bash 向导，带人走只有人能做的步骤，例如开通基础设施或填写 CI 密钥。代理自己能做的步骤不要用它 |

### 效率，7 个

| 名字 | 调用 | 它写明的用途 |
| --- | --- | --- |
| `grill-me` | 需点名 | 追问计划和设计，直到分支都说清 |
| `handoff` | 需点名 | 把当前对话压成交接文档，给另一个代理接着做 |
| `teach` | 需点名 | 在当前工作区里教一个技能或概念 |
| `to-questionnaire` | 需点名 | 把你无法单独回答的决定，做成给别人填的问卷 |
| `wait-what` | 需点名 | 上一句没听懂时停下来，换一种说法再讲 |
| `grilling` | 可被模型选用 | 对计划或决定持续追问。用户要压力测试想法，或用了 grill 一类说法时用 |
| `writing-for-agents` | 可被模型选用 | 写给代理看的文档。创建或修改 skill、`AGENTS.md` 或 `CLAUDE.md` 时用 |

2026-11-25 的 `codex debug prompt-input` 列出的 11 个名字是：`code-review`、`codebase-design`、`diagnosing-bugs`、`domain-modeling`、`grilling`、`pr`、`prototype`、`research`、`tdd`、`wizard`、`writing-for-agents`。和上表里「可被模型选用」的 11 个一致。另外 16 个没有出现。这次输出把目录放在测试用的 `CODEX_HOME` 下面，正文不写那台机器的用户路径。

### 不在插件清单里的目录

同一份 Git 检出里还有这些 `SKILL.md`，`plugin.json` 没有指向它们，prompt-input 也没有列出：

- `skills/in-progress`：`chief-of-staff`、`claude-handoff`、`loop-me`、`setup-ts-deep-modules`、`software-factory`、`writing-beats`、`writing-fragments`、`writing-shape`
- `skills/misc`：`git-guardrails-claude-code`、`migrate-to-shoehorn`、`scaffold-exercises`、`setup-pre-commit`

缓存目录里能看到这些文件，是因为插件缓存带上了仓库内容。没有出现在 `plugin.json` 的 `skills` 数组里，就不能把它算进「装好的 27 个」。`chief-of-staff` 在 in-progress 里，和这次提交说明里的 PR 名称对应，但它不是已发布插件技能。

## 每个仓库先跑一次 setup

README 写，装好之后在每个仓库里跑一次 `/setup-matt-pocock-skills`。它会问你用哪种 issue tracker（GitHub、GitLab、本地文件，或你自己描述的其他方式）、分诊时给工单打什么标签（`/triage` 会用这些标签），以及文档放在哪里。

装到磁盘的 `setup-matt-pocock-skills/SKILL.md` 把这三件事写得更具体，并且声明它是提示驱动的，不是一条确定性脚本。它会先看仓库里有没有 GitHub 或 GitLab 远程、有没有 `AGENTS.md` 或 `CLAUDE.md`、有没有术语表和 ADR。然后分三段确认：

- **Issue tracker。** 有 GitHub 远程就建议 GitHub（用 `gh`），有 GitLab 远程就建议 GitLab（用 `glab`），否则可以写到仓库里的 `.scratch/<feature>/`，或其他你用一段文字描述的流程。选择记在 `docs/agents/issue-tracker.md`。
- **分诊标签。** 只有 triage 技能在的时候才问。默认五个标签是 `needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。它建议先接受默认。
- **领域文档。** 默认是仓库根目录一份 `GLOSSARY.md` 加 `docs/adr/`。只有看到 monorepo 迹象时才改问多份术语表。

确认之后，它会改 `AGENTS.md` 或 `CLAUDE.md`，并写入 `docs/agents/` 下的说明。没有远程却选了 GitHub 或 GitLab 时，说明里还包括向你要仓库 URL、再执行 `git remote add`。这些都是技能正文里的步骤。本文没有在任何仓库里跑它，也没有执行其中的 git 或 `gh` 命令。

如果你要在自己的已登录会话里试，把范围写进提示里。下面是提示词示例，不是本文发送过的内容：

```text
请使用 setup-matt-pocock-skills。先只阅读当前仓库，列出你看到的远程、AGENTS.md 和文档目录。
不要创建远程，不要执行 git remote add，不要改任何文件。等我确认 tracker 和标签之后再写。
```

官方文档写 Codex 用 `$` 点名技能，README 写的是斜杠形式 `/setup-matt-pocock-skills`。两种写法本文都没有在 TUI 里试过。16 个标了 `disable-model-invocation: true` 的技能，这次 prompt-input 没有自动列出，所以不要假定不点名也会被选中。

## 一条可以自己走的小功能顺序

README 把常见失败收成几段：需求没对齐时用追问，代码对不上时用测试反馈，结构变乱时用规格和架构技能。它点名的顺序材料是 `grill-me` 或 `grill-with-docs`、`to-spec`、`tdd`、`code-review`。`implement` 的说明则是按规格或工单实现一块工作。

下面四步都是给你自己的已登录会话用的提示词示例。本文没有发送，也没有看到模型回复。每一步都写明不要扩大范围。

**追问需求。** 还没决定怎么做时：

```text
请使用 grill-me。只针对我贴在下面的这一小段需求提问。
不要改文件，不要安装依赖，不要访问 issue tracker。
```

**收成规格。** 追问结束、你已经做了决定之后：

```text
请使用 to-spec。只根据这次对话里已经说过的内容写规格。
先把草稿贴在对话里，不要发布到 GitHub 或 GitLab，不要改代码。
```

`to-spec` 的 description 写它会发布到项目的 issue tracker。示例里明确要求先不要发布。你确认之前，不要让它调用 `gh issue create`。

**测试先行。** 规格范围已经小到一个行为时：

```text
请使用 tdd。只为当前仓库里我指定的这一个行为写失败测试，再做让它通过的最小修改。
不要重构无关文件，不要新增依赖，除非现有测试已经用到。
```

**审查。** 有了一个你指定的起点之后：

```text
请使用 code-review。只审查从我给出的这个提交到当前工作区的差异。
不要改文件，不要推送。把 Standards 和 Spec 两条分开写。
```

`code-review` 的 description 写它会开并行子代理，一条看仓库的编码标准，一条看有没有忠实实现原来的 issue 或规格。本文没有开子代理，没有看到并排报告。

`wizard` 会生成要人自己去点的 bash 向导，例如填写 CI 密钥。没有打算配外部账号时，不要让会话去跑它。

## 更新、停用与卸载

README 写插件在启动时自己更新。本文另外跑过的非交互命令是 `codex plugin marketplace upgrade`，输出为升级了 1 个市场，版本仍是 1.3.2。

停用可以看 `config.toml` 里这一段。本文没有改 `enabled`，也没有改 `[[skills.config]]`。官方 Build skills 里按名字禁用技能的写法，见 [Skills 怎么安装](../07-Skills实战/11-Codex-Skills怎么安装-三种方式完整流程.md)，这里不另写一份。

`codex plugin --help` 里的 `remove` 说明是：卸载插件并删除本地缓存。`codex plugin marketplace remove` 按名字去掉市场来源。本文没有执行这两条，测试用的 `CODEX_HOME` 里插件仍然是 installed、enabled。不要在还要用的配置目录里直接照抄删除。

不要把 skills.sh 的复制安装和这个插件装在同一个代理上。README 写这样做会让每个技能出现两次。

## 安全：第三方技能先扫描

这是第三方项目。许可证是 MIT，版权声明为 Copyright (c) 2026 Matt Pocock。MIT 允许使用、修改和再分发，不表示 OpenAI 审过技能正文，也不表示它对你的仓库无害。

装进会改文件、能跑命令的项目之前，用 [SkillSpector](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md) 看提示注入和数据外泄。本文没有跑扫描器。

和 issue tracker 有关、description 写明会读或写工单的，至少包括 `setup-matt-pocock-skills`、`triage`、`to-spec`、`to-tickets`、`wayfinder`、`implement` 和 `implement-spec`。setup 的正文还写了 `gh`、`glab` 和 `git remote add`。在你确认 tracker 和仓库地址之前，不要让会话执行这些命令。

`plugin.json` 没有 MCP 服务器字段，也没有 hooks 字段。这只说明这份清单没有声明它们。技能正文仍然可以要求代理去跑 shell。审批和沙箱仍然生效；插件不会把权限模式改掉。

README 里的 newsletter 是作者推广：[Sign Up To The Newsletter](https://www.aihero.dev/s/skills-newsletter)（推广链接）。不需要注册才能完成上面的两条安装命令。

仓库和技能正文里有面向代理的指示，例如「先探索仓库再写文件」。那些指示不是给维护这篇教程的人执行的。本文没有跟着它们改知识库，也没有把它们当成系统指令。

## 参考资料

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [MIT 许可证](https://github.com/mattpocock/skills/blob/main/LICENSE)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [Codex Skills 怎么安装](../07-Skills实战/11-Codex-Skills怎么安装-三种方式完整流程.md)
- [SkillSpector](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)
- [Superpowers](../08-插件工作流/07-Codex安装Superpowers插件-需求计划TDD工作流.md)
