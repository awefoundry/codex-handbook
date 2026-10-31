---
id: codex-agent-skills-plugin
title: Codex 安装 agent-skills 插件：用 codex plugin 装上 Addy Osmani 的 25 个工程 Skill
seo_title: Codex 安装 agent-skills：25 个工程 Skill 的装法与调用
description: agent-skills 是 Addy Osmani 维护的第三方工程 Skill 插件。本文用 Codex CLI 0.166.0 实测安装、列出和卸载 0.6.14，说明 25 个 Skill 怎么分、Codex 里用 $ 还是 @，以及为什么不要把元 Skill 写进 AGENTS.md。
lede: 两条命令可以装上这套 Skill。装完要新开一次会话。元 Skill 留在插件里即可，不要再贴进 AGENTS.md。
url: /guides/codex-agent-skills-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-31
date_modified: 2026-10-31
verified_on: 2026-10-31
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex agent-skills, addyosmani agent-skills, codex plugin marketplace add, Codex Skill 插件, Codex 工程 Skill]
related: [codex-superpowers-plugin, create-codex-skill, codex-chrome-devtools-mcp]
howto: false
faq:
  - q: agent-skills 是 OpenAI 官方插件吗？
    a: 不是。它是 Addy Osmani 维护的第三方仓库，MIT 许可。Codex 用作者文档里的 marketplace 命令安装，不代表 OpenAI 已审核全部 Skill 正文。
  - q: 在 Codex 里用 @ 还是 $ 调用？
    a: 官方文档写明 ChatGPT 用 @，Codex CLI 和 IDE 扩展用 $ 或 /skills。作者的 Codex 安装说明写的是 @。本次没有登录，没有在对话里验证哪一种能补全到这些 Skill。
  - q: IDE 扩展里能装这个插件吗？
    a: 官方插件文档写明 IDE 扩展不支持插件。安装和启用请用 Codex CLI，或在 ChatGPT 桌面应用的插件界面里操作。桌面端插件目录是否已经收录同一仓库，本次没有打开桌面应用，不能当成已经上架。
---

# Codex 安装 agent-skills 插件：用 codex plugin 装上 Addy Osmani 的 25 个工程 Skill

> 本文在线版：[codexguide.io/guides/codex-agent-skills-plugin](https://codexguide.io/guides/codex-agent-skills-plugin)

> 核对依据：第三方仓库 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 的 [docs/codex-setup.md](https://github.com/addyosmani/agent-skills/blob/main/docs/codex-setup.md)、根目录 `plugin.json` 和各 `SKILL.md` 的 frontmatter。GitHub API 2026-10-31 返回 112,007 星、MIT、默认分支 `main`，最新提交 `eb07f19` 的说明是 “chore(release): bump plugin manifests to 0.6.14”，提交时间 2026-10-29 05:06 UTC（北京时间 13:06）。官方文档用了 [Plugins](https://learn.chatgpt.com/docs/plugins)、[Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) 和 [Build skills](https://learn.chatgpt.com/docs/build-skills)。实测环境是 Linux 上的 `codex-cli 0.166.0`，`CODEX_HOME` 指向临时目录，**没有登录**。安装、`plugin list` 和卸载的退出码都是 0。没有打开已登录会话，所以没有验证对话里的 `@` 或 `$` 补全。

agent-skills 把软件工程里反复做的一类动作写成 Skill：写规格、拆任务、按测试实现、审查、加固、准备上线。它不是 OpenAI 的产品。作者是 Addy Osmani，许可证是 MIT，仓库简介是 “Production-grade engineering skills for AI coding agents”。

和 [Superpowers](../08-插件工作流/06-Codex安装Superpowers插件-需求计划TDD工作流.md) 的差别在粒度。Superpowers 把“先问清需求、再写计划、测试先行”收成一套流程。agent-skills 按环节拆开，你可以点名其中一个，也可以让 Codex 按描述自己选。

## 安装前先看这几项

| 项目 | 2026-10-31 核对到的值 |
|---|---|
| 仓库 | `addyosmani/agent-skills` |
| 许可 | MIT |
| 星标 | 112,007 |
| 插件版本 | 0.6.14 |
| 作者文档要求的 CLI | v0.122 或更新。更老的版本命令是 `codex marketplace add` |
| 本次 CLI | 0.166.0 |
| `plugin.json` 的 capabilities | Interactive、Read、Write |

`plugin.json` 的 `longDescription` 写的是 25 个工程工作流。安装后的 `skills/` 里确实有 25 个 `SKILL.md`。其中一个是元 Skill `using-agent-skills`，用来决定调用哪一个 Skill。其余 24 个对应具体环节。下文的表按这 25 个文件列出，不把元 Skill 算成普通工程步骤。

作者文档还写了两件不要混用的事：

- `.claude/commands/` 里的斜杠命令只给 Claude Code。在 Codex 里直接调用对应 Skill，例如不要依赖 `/spec` 这种斜杠命令。
- `agents/` 里的 persona 也是 Claude Code 用的。`hooks/` 下的 `SessionStart` 脚本没有接到任一插件清单上。

## 安装

作者文档里的两条命令：

```bash
codex plugin marketplace add addyosmani/agent-skills
codex plugin add agent-skills@agent-skills
```

第一条把这个 Git 仓库登记成名为 `agent-skills` 的 marketplace。第二条从该 marketplace 安装并启用同名插件。本地克隆也可以：

```bash
codex plugin marketplace add /path/to/your/clone
codex plugin add agent-skills@agent-skills
```

### 本次实际输出

`codex-cli 0.166.0`，`CODEX_HOME` 设在临时目录，未登录：

```text
Added marketplace `agent-skills` from https://github.com/addyosmani/agent-skills.git.
Added plugin `agent-skills` from marketplace `agent-skills`.
```

安装根目录是 `plugins/cache/agent-skills/agent-skills/0.6.14`。`codex plugin list` 显示：

```text
PLUGIN                     STATUS              VERSION  SOURCE
agent-skills@agent-skills  installed, enabled  0.6.14   <marketplace 路径>
```

因为 `CODEX_HOME` 放在 `/tmp` 下，CLI 另外打印了一条无法在临时目录创建 PATH 别名的警告。两条安装命令的退出码仍是 0，插件状态是 installed, enabled。默认安装到 `~/.codex` 时不应把这条警告当成失败。

装完之后要新开一个 Codex 会话。作者文档和官方插件文档都写了这一点：已打开的会话不会自动发现刚装上的 Skill。

官方插件文档同时写明，IDE 扩展不支持插件。这条安装路径是 CLI。ChatGPT 桌面应用有自己的插件目录；本次没有打开桌面应用，不能说目录里已经能搜到 `addyosmani/agent-skills`。

## 25 个 Skill

描述取自各 `SKILL.md` 的 `description` 首句，安装版本 0.6.14。

### 需求和规格

| Skill | 做什么 |
|---|---|
| `idea-refine` | 用发散和收敛，把笼统想法收成可执行的概念 |
| `interview-me` | 一次问一个问题，把真实意图问清楚 |
| `spec-driven-development` | 在写代码前先写规格 |
| `planning-and-task-breakdown` | 把规格拆成有顺序、可实施的任务 |
| `source-driven-development` | 先对照官方文档，再做实现决定 |

### 实现

| Skill | 做什么 |
|---|---|
| `incremental-implementation` | 用薄、可验证的切片交付改动 |
| `test-driven-development` | 用红-绿-重构驱动实现和修 bug |
| `constraint-driven-development` | 把质量标准写成约定，避免把标准悄悄降低 |
| `doubt-driven-development` | 对非平凡决策做一次新上下文里的对抗复查 |
| `api-and-interface-design` | 设计稳定的 API、模块边界和类型约定 |
| `frontend-ui-engineering` | 做可访问、响应式的界面 |
| `deprecation-and-migration` | 处理废弃、迁移和线上数据结构变更 |

### 质量和排查

| Skill | 做什么 |
|---|---|
| `code-review-and-quality` | 合并前从多个维度审查改动 |
| `code-simplification` | 不改变行为，只把代码改得更容易读 |
| `debugging-and-error-recovery` | 从失败测试、构建或意外行为追根因 |
| `browser-testing-with-devtools` | 通过 Chrome DevTools MCP 在真实浏览器里看 DOM、控制台、网络和性能 |
| `performance-optimization` | 处理前后端、查询和 Core Web Vitals 一类性能问题 |
| `security-and-hardening` | 检查输入、认证、存储和外部集成 |

`browser-testing-with-devtools` 依赖 Chrome DevTools MCP。接入方法见 [Codex 接入 Chrome DevTools MCP](./06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)。没装那个 MCP 时，不要假定这个 Skill 自己能打开浏览器。

### 交付和工程环境

| Skill | 做什么 |
|---|---|
| `git-workflow-and-versioning` | 规范提交、分支、冲突和原子提交 |
| `ci-cd-and-automation` | 配置流水线、测试门禁和部署 |
| `documentation-and-adrs` | 记录架构决策和需要留下的文档 |
| `observability-and-instrumentation` | 补日志、指标、追踪和告警 |
| `shipping-and-launch` | 做上线前检查、监控和发布步骤 |
| `context-engineering` | 整理会话、规则文件和项目上下文 |

### 元 Skill

| Skill | 做什么 |
|---|---|
| `using-agent-skills` | 判断当前工作该用哪一个 Skill。它是元 Skill，不是一个具体工程环节 |

## 怎么调用

官方 [Build skills](https://learn.chatgpt.com/docs/build-skills) 写明两种触发方式：

- **显式**：ChatGPT 里输入 `@` 选择 Skill。Codex CLI 或 IDE 扩展里用 `/skills`，或输入 `$` 点名，例如 `$spec-driven-development`。
- **隐式**：任务和 Skill 的 `description` 对得上时，Codex 可以自己选。选中之后才加载完整的 `SKILL.md`。

官方 [Plugins](https://learn.chatgpt.com/docs/plugins) 在 ChatGPT 的输入框说明里写的是用 `@` 点名插件或其中的 Skill。[Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) 又写了一句：ChatGPT 用 `@`，Codex 用 `$`。

作者的 `docs/codex-setup.md` 写的是在 Codex 对话里用 `@`，例子是 `@spec-driven-development`，也可以只描述任务，让 Codex 自己选。

两处不一致。本次 CLI 没有登录，插件命令不需要会话就能完成安装和列出，但补全菜单没有在真实对话里看过。以你当前界面为准：先试官方写的 `$` 和 `/skills`。补全里没有这些名字时，再按作者文档试 `@`。不要两套同时堆进同一条系统提示。

定时任务里的写法，官方 Automations 文档另有一句：桌面应用中可以用 `$skill-name`。那是定时任务提示词，不是这条插件的安装步骤。

## 不要把元 Skill 写进 AGENTS.md

作者文档写明：Codex 已经会按 `name` 和 `description` 做渐进加载。不要再把 `using-agent-skills/SKILL.md` 的全文贴进 `AGENTS.md`、系统提示或其他每次都在场的上下文。那样会把这套包自己的路由，叠到 Codex 自己的路由上。

元 Skill 可以留在已安装的插件里。限制的是“预加载全文”，不是“必须删掉这个文件”。

自己写 Skill 的格式见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

## 和 Superpowers 怎么选

| | agent-skills | Superpowers |
|---|---|---|
| 维护者 | Addy Osmani，第三方 | 第三方，见那篇文章 |
| 形态 | 25 个按环节拆开的 Skill | 需求、计划、测试先行的一套流程 |
| 本次安装方式 | `codex plugin marketplace add` 作者仓库 | 那篇文章写了官方目录和作者仓库两种 |

一个具体环节（补观测、写 ADR、做迁移）更接近 agent-skills 里的单个名字。一整段“先问清再计划再测试”的默认顺序，用 Superpowers 那篇里的流程。两套可以都装，但不要让两份总是生效的说明互相覆盖。装第二套之后同样要新开会话。

## 安装第三方 Skill 前的检查

这次安装来自 GitHub 上的公开仓库，不是 OpenAI 插件目录里的已审核条目。`plugin.json` 声明了读和写。装上之后，新会话里的 Codex 可以按描述加载这些说明。

建议在启用前做这几件已经能核对的事：

- 仓库、许可证、作者和版本与上表一致。版本不是 0.6.14 时，先看提交说明再决定要不要更新。
- 打开准备使用的那个 `SKILL.md`，确认步骤和你的仓库规则不冲突。本文没有逐篇审计 25 个文件里有没有提示注入。
- 不要把密钥、客户数据写进 Skill 或 `AGENTS.md`。
- 浏览器类 Skill 会再依赖 MCP。MCP 的权限按那个服务器自己的配置，不因为这个插件是 MIT 就自动安全。

想用扫描工具看第三方 Skill 时，可以先看知识库里已有的 [HOL Guard 插件安全检查](../13-社区生态与项目评测/01-Codex插件安全检查-HOL-Guard.md)。那是另一个第三方项目，不是这次安装的一部分。

## 更新和卸载

作者仓库更新后，官方 CLI 有 marketplace 的 upgrade 子命令。`codex plugin marketplace --help` 在 0.166.0 里列出 `add`、`list`、`upgrade`、`remove`。本次没有在作者发新版本时重跑 `upgrade`，所以不记录升级后的输出。

卸载本次已经执行，退出码 0：

```bash
codex plugin remove agent-skills@agent-skills
codex plugin marketplace remove agent-skills
```

`remove` 之后再 `plugin list`，同一条目的状态变为 `not installed`。接着 `marketplace remove` 的输出是 `Removed marketplace agent-skills`。只删插件、保留 marketplace 时，可以停在第一条。

官方文档还写了在插件浏览器里卸载的界面路径。CLI 未登录时，本文验证的是上面两条命令。

## 常见问题

**装完当前会话里还是看不到 Skill。** 作者文档要求新开一个会话。旧会话不会重新扫描刚安装的插件。

**`/spec` 没有反应。** 那是 Claude Code 的斜杠命令。Codex 里点名 `spec-driven-development`。

**能不能把 25 个 Skill 的全文都写进 AGENTS.md？** 不要。官方机制是按描述按需加载。预加载全文，尤其是元 Skill，和作者文档的警告相反。

## 下一步

想先做一条自己的 Skill，而不是装一整套，从 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) 开始。想要一套固定的需求到测试流程，看 [Superpowers](../08-插件工作流/06-Codex安装Superpowers插件-需求计划TDD工作流.md)。

## 参考资料

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)（第三方，MIT）
- [docs/codex-setup.md](https://github.com/addyosmani/agent-skills/blob/main/docs/codex-setup.md)
- [OpenAI：Plugins](https://learn.chatgpt.com/docs/plugins)
- [OpenAI：Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills)
