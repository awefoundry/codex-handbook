---
id: codex-dotnet-skills
title: Codex 安装 Microsoft 官方 .NET Skills：把 dotnet/skills 加进插件市场，按需安装测试、MSBuild、Blazor 和 MAUI 等插件
seo_title: Codex 安装 Microsoft 官方 .NET Skills：dotnet/skills 的 17 个插件
description: Microsoft .NET 团队的 dotnet/skills 用 Codex 插件市场安装 .NET 技能。2026-11-15 的仓库里有 17 个带 plugin.json 的插件、plugins/ 下 108 个 SKILL.md；README 和市场清单只列出 16 个，不含 dotnet-experimental。Copilot 的 .agent.md 不会装进 Codex。
lede: 先 codex plugin marketplace add dotnet/skills，再在 /plugins 的 dotnet-agent-skills 里按需安装。市场清单是 16 个插件；仓库里多出来的 dotnet-experimental 不在这份清单里。
url: /guides/codex-dotnet-skills
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 21
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-15
date_modified: 2026-11-15
verified_on: 2026-11-15
official_ref: https://github.com/dotnet/skills
keywords: [Codex .NET Skills, dotnet/skills, dotnet-agent-skills, Codex 插件市场, MSBuild, Blazor, MAUI]
related: [codex-chajian-rukou-yu-gongzuoliu, codex-google-skills-plugins, codex-unity-plugin]
faq:
  - q: 这是 OpenAI 内置的 .NET 功能吗？
    a: 不是。仓库在 GitHub 组织 dotnet 下，marketplace.json 的 owner.name 是 “.NET Team at Microsoft”，许可证是 MIT，2026-11-15 未归档。Codex 只是 README 写明的安装对象之一。
  - q: 装完 Codex 插件，就能用仓库里的 GitHub Copilot agent 吗？
    a: 不能。README 写明，plugins 里的 .agent.md 使用 Copilot 自定义 agent 约定，不会作为 Codex 原生 agent 安装。这次克隆的树上没有 .codex/agents/*.toml。Codex 侧用它自己的动态子代理。
  - q: /plugins 里能看到全部 17 个吗？
    a: README 的表格和四份 marketplace.json 都是 16 个，没有 dotnet-experimental。按文档打开 dotnet-agent-skills 这一页，对应的是这 16 个。dotnet-experimental 有自己的 plugin.json 和 2 个 SKILL.md，但没有写进市场清单。本文没有打开 /plugins 界面。
  - q: 本文把 17 个插件都装上并跑过了吗？
    a: 没有。数量来自 2026-11-15 的 GitHub API 和 main 的文件树。没有执行 marketplace add，也没有在 Codex 会话里调用任何一个 Skill。
---

# Codex 安装 Microsoft 官方 .NET Skills：把 dotnet/skills 加进插件市场，按需安装测试、MSBuild、Blazor 和 MAUI 等插件

> 本文在线版：[codexguide.io/guides/codex-dotnet-skills](https://codexguide.io/guides/codex-dotnet-skills)

> 核对依据：GitHub 仓库 [dotnet/skills](https://github.com/dotnet/skills) 的 [README](https://github.com/dotnet/skills/blob/main/README.md)、`.agents/plugins/marketplace.json`，以及每个插件目录下的 `.codex-plugin/plugin.json`。2026-11-15 查询 GitHub API：`stargazers_count` 6181，`forks_count` 488，`license.spdx_id` 为 MIT，`archived` 为 false，`pushed_at` 为 2026-11-13T20:11:12Z（北京时间 2026-11-14 04:11）。同一时刻 `commits/main` 的 tip 是 `2877c712edc20643b72f64e2983b168e6661d607`，这条提交的 committer 时间是 2026-11-12T07:27:26Z。文件计数按这次 tip 的 git tree。技能价值看板 [dotnet.github.io/skills](https://dotnet.github.io/skills/) 返回 HTTP 200，本文没有抄板上的通过率或耗时。没有执行安装命令，没有配图。

这个仓库由 .NET 团队维护，给编码代理提供可移植的 Agent Skills，以及给特定宿主用的自定义 agent。marketplace.json 里的 owner 名称是 “.NET Team at Microsoft”。它和 OpenAI 内置插件是两套来源。

Codex 能安装它，是因为 README 写了 Codex CLI 的 marketplace 命令，仓库里也有 `.agents/plugins/marketplace.json` 和各插件的 `.codex-plugin/plugin.json`。官方插件浏览器的一般用法见 [Plugins](https://developers.openai.com/codex/plugins)：在 Codex CLI 里用 `/plugins` 按市场分页浏览、安装。该页没有单独介绍 dotnet/skills，安装步骤以这个仓库的 README 为准。

适合已经在用 Codex、并且要写 C# / .NET、查测试、看 MSBuild，或做 Blazor、MAUI、ASP.NET Core 的人。只想知道插件目录怎么开，先看 [Codex 插件入口](../08-插件工作流/04-Codex插件入口与工作流.md)。同一栏目里，Google Cloud 的技能仓库见 [google/skills](./16-Codex安装Google官方Skills与插件-google-skills仓库.md)，Unity 见 [Unity 官方插件](./13-Codex安装Unity插件-用Skills辅助Unity开发.md)。

## 先看结论

2026-11-15 这棵树上同时有两套数字，不要合成一个。

**带 `.codex-plugin/plugin.json` 的插件目录是 17 个。** `plugins/` 下面的 `SKILL.md` 是 **108** 个。全仓库的 `SKILL.md` 是 116 个，多出的 8 个不在 `plugins/` 里。

**README 的 “What's Included” 表格是 16 行。** `.agents/plugins/marketplace.json`、`.claude-plugin/marketplace.json`、`.cursor-plugin/marketplace.json`、`.github/plugin/marketplace.json` 的 `plugins` 数组也都是这 16 个名字。四份清单都没有 `dotnet-experimental`。

因此，按 README 的 Codex CLI 步骤注册市场之后，`dotnet-agent-skills` 这一页对应的是表格里的 16 个。`dotnet-experimental` 在仓库里，不在这份市场清单里。

README 还写明：Codex 插件安装带上的是技能，以及插件声明的、Codex 能用的 MCP 服务器。GitHub Copilot 的 `.agent.md`、它们的静态 handoff，以及只给特定宿主用的 LSP 声明，不会跟着装进来。这个仓库目前没有提供 `.codex/agents/*.toml`。这次 tree 里，`plugins/*/agents/*.agent.md` 有 16 个，`.codex/agents/` 下的 toml 是 0 个。

## 仓库身份和三个容易混的数

| 项目 | 2026-11-15 的结果 |
|---|---|
| 仓库 | [dotnet/skills](https://github.com/dotnet/skills)，组织 `dotnet`，说明文字是 “Repository for skills to assist AI coding agents with .NET and C#” |
| 许可证 | MIT。API 的 `license.spdx_id` 为 MIT |
| 状态 | `archived: false` |
| Star / fork | 6181 / 488 |
| 最近 push | `pushed_at` 2026-11-13T20:11:12Z，北京时间 2026-11-14 04:11 |
| main tip | `2877c712edc20643b72f64e2983b168e6661d607`，committer 时间 2026-11-12T07:27:26Z |

`pushed_at` 晚于这条 tip 提交的 committer 时间。计数以 tip 的文件树为准，不以社交帖里的 star 数为准。

| 口径 | 数量 | 怎么数的 |
|---|---:|---|
| `.codex-plugin/plugin.json` | 17 | `plugins/*/.codex-plugin/plugin.json` |
| README “What's Included” 表格 | 16 | 不含 `dotnet-experimental` |
| 每份 `marketplace.json` 的 `plugins` | 16 | 四份文件同一组名字 |
| `plugins/` 下的 `SKILL.md` | 108 | 含 experimental 的 2 个 |
| 全仓库 `SKILL.md` | 116 | 另外 8 个在 `.agents/skills/`（5）、`.github/skills/`（1）和 `eng/skill-validator/tests/fixtures/`（2） |

那 8 个是仓库自己的写作技能和校验夹具，不是下面这张插件表的安装内容。

技能价值看板的入口在 README 顶部，页面说明它按插件、技能、执行模型和评判模型展示 token、耗时、触发和未通过比例。本文只确认页面返回 HTTP 200，没有把看板上的数字写进来。

## 17 个插件：16 个在市场里

版本号来自各目录 `.codex-plugin/plugin.json` 的 `version`。说明文字，市场内的 16 个用 `.agents/plugins/marketplace.json` 的 `description`；`dotnet-experimental` 用它自己的 plugin.json，因为市场文件里没有它。`SKILL.md` 个数按插件目录统计。

说明按当天的市场 `description` 译成中文。`dotnet-experimental` 不在市场文件里，说明译自它的 plugin.json。

| 插件 | 市场清单 | plugin.json 版本 | SKILL.md | 说明 |
|---|---|---:|---:|---|
| dotnet | 有 | 0.2.6 | 5 | 核心 C# 和 .NET 开发技能 |
| dotnet-advanced | 有 | 0.2.3 | 4 | 核心插件不覆盖的专项 .NET / C# 技能 |
| dotnet-ai | 有 | 0.1.6 | 1 | 技术选择、LLM、agent 工作流、RAG、MCP 和 ML.NET |
| dotnet-aspnetcore | 有 | 0.1.2 | 2 | 中间件、端点、实时通信和 API |
| dotnet-blazor | 有 | 0.1.3 | 10 | 组件、交互和 Web 应用 |
| dotnet-data | 有 | 0.1.6 | 2 | 数据访问和 Entity Framework |
| dotnet-diag | 有 | 0.1.3 | 7 | 性能调查、调试和事故分析 |
| dotnet-experimental | 无 | 0.1.2 | 2 | 仍在评估，可能变化，或以后进入稳定插件 |
| dotnet-maui | 有 | 0.1.16 | 8 | 环境、诊断、排障、导航、绑定、依赖注入、布局和主题 |
| dotnet-msbuild | 有 | 0.1.12 | 21 | 失败诊断、性能、代码质量和构建现代化 |
| dotnet-nuget | 有 | 0.1.1 | 1 | 依赖管理和包现代化 |
| dotnet-template-engine | 有 | 0.1.5 | 6 | 模板发现、项目脚手架和模板编写 |
| dotnet-test | 有 | 1.0.1 | 24 | 运行、生成、分析和改进测试，含覆盖率和 MSTest |
| dotnet-test-migration | 有 | 0.1.12 | 6 | MSTest / xUnit 升级、迁到 MSTest、VSTest 迁到 Microsoft.Testing.Platform |
| dotnet-upgrade | 有 | 0.1.1 | 6 | 跨框架版本、语言特性和兼容目标的迁移 |
| dotnet-winforms | 有 | 0.1.0 | 1 | 项目、界面、绑定、无障碍和现行做法 |
| dotnet11 | 有 | 0.1.3 | 2 | .NET 11 的新 API 和语言特性 |

`dotnet-test-migration` 的 plugin.json 比市场说明多写了 NUnit（`xUnit/NUnit-to-MSTest`）。表内按市场说明翻译，没有把 NUnit 算进市场文案。

`dotnet-experimental` 的两个技能目录是 `exp-mock-usage-analysis` 和 `exp-test-maintainability`。plugin.json 把它写成仍在评估、可能变化或毕业到稳定插件的内容。README 表格没有这一行。本文没有找到一条官方命令，能单靠 Codex 市场把它和上面 16 个一起列出来。

市场文件的 `name` 是 `dotnet-agent-skills`，`interface.displayName` 是 “.NET Agent Skills”。升级命令用的就是这个市场名。

## 用 Codex CLI 安装

README 的 Codex CLI 一节要求 **Codex CLI v0.121.0 或更新**。它写的步骤是：

1. 注册市场：

```bash
codex plugin marketplace add dotnet/skills
```

2. 启动 Codex，打开插件浏览器：

```text
/plugins
```

3. 在 `dotnet-agent-skills` 这一页安装需要的插件。
4. 以后升级：

```bash
codex plugin marketplace upgrade dotnet-agent-skills
```

先只装你这次任务会用到的插件，例如 `dotnet-test` 或 `dotnet-msbuild`。108 个技能一次全装，会把很多用不到的说明放进后续会话。装完后新开一段会话，插件自带的技能才会出现。这是 [官方插件文档](https://developers.openai.com/codex/plugins) 对 CLI 的一般说明，不是本文跑出来的结果。

README 另外写了一条按单个技能安装的命令，使用 `skill-installer`，URL 形如：

```bash
skill-installer install https://github.com/dotnet/skills/tree/main/plugins/<plugin>/skills/<skill-name>
```

本文没有运行 `skill-installer`，也没有运行 `codex plugin marketplace add`。写作环境里另有一次 Codex CLI 0.169.0 的安装，用来核对其它文章的命令帮助，没有拿它注册这个市场。

同一份 README 还写了 Copilot CLI、Claude Code、VS Code 和 Cursor 的入口。那些不是本文的步骤。

## 装上 Codex 插件之后没有的东西

README 把这件事写在仓库开头和 Codex CLI 一节，需要单独记住：

- `agents/*.agent.md` 遵循 GitHub Copilot 的自定义 agent 约定。它们不会被安装成 Codex 的原生 agent。
- 原生 Codex agent 用的是 `.codex/agents/*.toml`。README 写明，这个仓库目前不提供这些文件，因为 Codex 的插件安装不会把 agent 文件放到 Codex 的发现位置。这次 tree 搜索的结果是 0 个这样的 toml。
- Codex 插件安装会带上技能，以及插件声明的、Codex 兼容的 MCP 服务器。它不带上 `.agent.md`、那些文件里的静态 handoff，或只给特定宿主的 LSP 声明。
- 需要分工时，用 Codex 内置的动态子代理。仓库指向 [multi-agent 文档](https://developers.openai.com/codex/multi-agent/)。本知识库的用法见 [Subagents](../11-自动化与高级工作流/09-Codex使用Subagents并行处理任务.md)。

`plugins/` 里那 16 个 `.agent.md` 分布在 `dotnet-test`（10）、`dotnet-msbuild`（3）、`dotnet-diag`（1）、`dotnet-template-engine`（1）和 `dotnet-test-migration`（1）。`agentic-workflows/` 和 `.github/workflows/` 里还有别的 `.agent.md`，同样不是 Codex agent 包。

不要把「市场添加成功」理解成 Copilot 那套 planner、tester、MSBuild reviewer 已经出现在 Codex 里。那些名字在仓库里，安装路径不是 Codex 插件。

## 怎么验证、哪里停

本文没有装插件，所以没有成功运行某个 Skill 的输出可以贴。你自己装的时候，可以这样核对：

1. `codex plugin marketplace list` 里出现市场名 `dotnet-agent-skills`。README 的升级命令用的是这个名字。
2. `/plugins` 打开后，进入 `dotnet-agent-skills`，只安装你点名的插件。
3. 新开一段会话，让 Codex 说明它这次能用到的技能名称。名称应来自你安装的那个插件目录，而不是整个 108 的清单。
4. 如果列表里没有 `dotnet-experimental`，这和当前市场文件一致。不要为了把它装上而改市场 JSON，除非你知道自己在改什么。

这些插件会让代理按技能去改项目、跑 `dotnet` 测试或动构建文件。装之前先看 [插件入口](../08-插件工作流/04-Codex插件入口与工作流.md) 里的权限边界。没有 .NET SDK 的机器上，技能里的命令不会凭空变成功。

## 参考资料

- [dotnet/skills](https://github.com/dotnet/skills) 与 [README](https://github.com/dotnet/skills/blob/main/README.md)（MIT，.NET Team at Microsoft）
- [Skill Value dashboard](https://dotnet.github.io/skills/)（2026-11-15，HTTP 200）
- [Codex Plugins](https://developers.openai.com/codex/plugins)（`/plugins` 浏览器；页面本身不介绍这个仓库）
- [Codex multi-agent](https://developers.openai.com/codex/multi-agent/)（README 指向的动态子代理说明）
