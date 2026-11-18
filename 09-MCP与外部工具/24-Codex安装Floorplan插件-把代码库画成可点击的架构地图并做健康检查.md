---
id: codex-floorplan-plugin
title: Codex 安装 Floorplan 插件：让 Codex 把整个代码库画成可点击的架构地图，还能做密钥与权限健康检查
seo_title: Codex 安装 Floorplan：可点击架构地图与健康检查
description: Floorplan 是一个 MIT 许可的 Codex 插件，让 Codex 读完你的代码库后画出可缩放、可提问的架构地图，并做密钥与权限的健康检查。本文按官方 Codex 文档说明在 App 和终端里怎么安装、怎么生成第一张地图、审批弹窗怎么处理，以及它和 Archify 的取舍。
lede: 两条命令可以装上这个第三方插件。第一张地图用一句话或 $floorplan。Health check 是检查，不是安全审计。
url: /guides/codex-floorplan-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 24
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-17
date_modified: 2026-11-17
verified_on: 2026-11-17
tested_cli_version: 0.169.0
official_ref: https://github.com/haydenschmitty/floorplan/blob/main/docs/codex.md
keywords: [Codex Floorplan, codex plugin marketplace add, 代码库架构图, $floorplan, Health check]
related: [codex-archify-architecture-diagrams, codex-plugin-hook-audit]
howto: true
faq:
  - q: Floorplan 是 OpenAI 官方插件吗？
    a: 不是。它是 Hayden Smith 维护的第三方仓库，MIT 许可。用作者文档里的 marketplace 命令安装，不代表 OpenAI 已审核地图脚本。
  - q: Health check 能代替安全审计吗？
    a: 不能。README 原话是 “A check, not an audit”。它列出的是密钥进了代码或浏览器、Supabase 表谁都能读、Firebase 规则开着、Stripe webhook 可能被伪造、端点没有登录这一类常见问题，每条附一段可以贴回 Codex 的修复提示。
  - q: 本文生成过一张真实地图吗？
    a: 没有。2026-11-17 在 Linux、Codex CLI 0.169.0、独立 CODEX_HOME、未登录的前提下装上了 0.11.0。地图界面、Ask 和审批弹窗需要已登录的 Codex 和浏览器，本文未实测界面。
---

# Codex 安装 Floorplan 插件：让 Codex 把整个代码库画成可点击的架构地图，还能做密钥与权限健康检查

> 本文在线版：[codexguide.io/guides/codex-floorplan-plugin](https://codexguide.io/guides/codex-floorplan-plugin)

> 核对依据：第三方仓库 [haydenschmitty/floorplan](https://github.com/haydenschmitty/floorplan) 的 README、[docs/codex.md](https://github.com/haydenschmitty/floorplan/blob/main/docs/codex.md)、[docs/getting-started.md](https://github.com/haydenschmitty/floorplan/blob/main/docs/getting-started.md)，以及装下来的 `.codex-plugin/plugin.json`。2026-11-17 通过 GitHub API 查询：4,635 star、381 fork，MIT，未归档，`pushed_at` 为 2026-11-16T16:57:59Z。README 版本徽章是 0.11.0。实测环境是 Linux，Node.js v22.23.4，`codex-cli 0.169.0`，`CODEX_HOME` 指向一个新目录，**没有登录**。没有配图。

Floorplan 是第三方 Codex 插件，许可证 MIT，作者 Hayden Smith。Codex 或 Claude Code 读完代码库后，画出一张可以缩放、可以从某个页面点进去、也可以在图上提问的地图。它不是 OpenAI 的官方功能。

这篇写给「用 AI 做出了能跑的应用，但自己没把代码读完」的人。要的是一张给文档、演讲或决策用的图，用[《Codex 使用 Archify 生成架构图》](../13-社区生态与项目评测/04-Codex使用Archify生成架构图.md)。要先摸清仓库再改代码，用[只读调查](../03-项目理解与上下文/05-只读调查怎么做-先让Codex把项目摸清楚.md)。

## 它是什么，适合谁，不适合谁

README 把读者分成三类：想用自己的话看懂 AI 做出来的应用、想让新人从全貌点到具体文件、以及想在每次 AI 改完后看见动了哪一块。

适合：

- 你有一个已经能跑的前端、后端，或并排放着的多个仓库，想看见页面、请求和外部服务怎么连。
- 你愿意让 Codex 读仓库，并在它请求时决定要不要在沙箱外启动本地地图服务器。
- 你想要一份「常见密钥和权限疏漏」的检查清单，并且知道这代替不了审计。

不适合：

- 你要的是序列图、ER 图或一页讲稿。那是 Archify 的题目。
- 你要把 Health check 的结果当成渗透测试或合规结论。
- 你没有 Node.js 18 或更新版本。README 和 Codex 文档都把 Node.js 18+ 写成前提。本文的机器是 v22.23.4。

作者写它不需要单独的 API key，走你已经登录的 ChatGPT。地图、扫描和本地服务器都在你的电脑上。可选的 Floorplan Cloud 等候名单只有在你留下邮箱时才会发出去。

## 在 Codex 里安装：App 里添加 marketplace、终端两条命令

[docs/codex.md](https://github.com/haydenschmitty/floorplan/blob/main/docs/codex.md) 写了两条路，并写明桌面端和 CLI 共用插件，在一边装好后另一边也能用。

**Codex App**（文档写不需要终端）：

1. 打开 **Plugins**，选择 **Add a marketplace**。
2. **Source** 填 `haydenschmitty/floorplan`。**Git ref** 留空，点击 **Add marketplace**。
3. 在列表里找到 **Floorplan**，点 **+** 安装。
4. 新开一个对话。

**终端**：

```bash
codex plugin marketplace add haydenschmitty/floorplan
codex plugin add floorplan@floorplan
```

2026-11-17 在未登录的 Codex CLI 0.169.0 上，这两条命令的退出码都是 0。输出里的关键句是：

```text
Added marketplace `floorplan` from https://github.com/haydenschmitty/floorplan.git.
Added plugin `floorplan` from marketplace `floorplan`.
```

`codex plugin list` 显示：

```text
PLUGIN               STATUS              VERSION  SOURCE
floorplan@floorplan  installed, enabled  0.11.0   <本次的 marketplace 目录>
```

缓存目录名以 `plugins/cache/floorplan/floorplan/0.11.0` 结尾，和 README 徽章、`plugin.json` 的 `"version": "0.11.0"` 一致。`codex login status` 输出 `Not logged in`。`codex mcp list` 输出 `No MCP servers configured yet`。装下来的 `.codex-plugin/plugin.json` 没有 `hooks` 字段。README 的 FAQ 也写 Floorplan 没有 hooks、没有 MCP、没有依赖。这次安装清单和那句话一致；它不能代替你以后升级时再看一遍仓库。

同一份 `plugin.json` 的 `interface.capabilities` 包含 `Read` 和 `Write`。README 写它只添加项目里的 `floorplan/` 目录，不改你的代码、`.gitignore` 或其他已跟踪文件。本次没有登录，没有生成地图，所以没有看到它实际写下哪些文件。

装第三方插件前，先看它会读什么、写什么。检查清单见[《Codex 插件和 Hook 自查》](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)。

## 生成第一张地图：自然语言或 $floorplan

Codex 文档给的第一句是：

> Draw a floorplan of this codebase

也可以输入 `$floorplan`。这个名字来自技能目录：装下来的 `skills/floorplan/SKILL.md` 里 `name: floorplan`。`plugin.json` 的 `defaultPrompt` 第一条就是上面那句，另外两条是 “Update the floorplan with what we just changed” 和 “Show me how the frontend talks to the backend”。

README 的快速开始写的是另一句，Claude Code 和 Codex 通用：

> Make me a floorplan of this app.

前后端分开放在两个仓库时，打开**同时装着这两个仓库的那个文件夹**。文档写它会把仓库都找出来，并把前端请求对上另一边的端点。

文档描述的过程是：先扫描文件、import、端点和网页请求；再由 Codex 给每一块、每个文件和每个请求起一个普通英文名字；然后生成地图并打开。之后说 “update the floorplan” 或 “Update the floorplan”，只会重读有变化的部分。Getting started 还写：小应用大约几分钟，大的更久；扫描本身 “takes seconds and costs no tokens”，给每个文件写说明才走你的 ChatGPT 套餐。这是作者文档里的说法，本文没有计时，也没有看用量。

还没有代码、只有 PRD 或说明时，可以要一张 blueprint。卡片用虚线表示这是计划。那是文档里的第二种用法，本文没有跑过。

**未实测界面。** 打开地图、Start here 导览、缩放和 Ask，都需要已登录的 Codex 和浏览器。本环境没有 Codex 桌面 App，也没有登录。

可以先在浏览器里看作者放出来的示例，不需要安装：[Floorplan live demo](https://haydenschmitty.github.io/floorplan-demo/)（2026-11-17 可以打开）。页面写明右边的 Brewline 地图是真的，旁边的对话是脚本演示。那不是你的仓库。

## 地图怎么看：缩放、从页面出发、Ask 提问

下面是 README 和 getting started 对界面的说明，不是本次点出来的结果。

- **缩放**：从整个应用双击进入一块、一组文件、一个文件和它的端点。每一层显示谁在用它、它又用了谁。
- **从页面出发**：选一个你认识的页面，看它后面的部件、发出的请求、服务端代码、数据和外部服务。
- **Ask**：在地图上提问，例如一次退款怎样回到顾客的卡上。文档写回答会带一张只含相关部分的小图，以及分步说明。
- **Recent work**：刚改过的卡片会以绿色标出，并注明这次改动为什么要做。
- **更新**：已经开着的地图会自己重新加载。

Codex 文档写 Ask 的实现：地图服务器在你的项目目录里跑 `codex exec`，使用 Codex 的**只读沙箱**和你的 ChatGPT 登录。它能读地图和源码，不能改文件。这些运行**不会**写进 Codex 历史；追问时带上最近几轮问答。

服务器默认用「画出这张地图的那个 agent」。要指定 Codex：

```bash
node floorplan/serve.mjs --engine codex
```

`codex` 不在 PATH 上时，用 `--codex /path/to/codex`。`--model` 指定模型；不写就用你的 Codex 设置。本文没有启动这台服务器，这三个参数只按文档列出。

Getting started 还写：服务器默认在本机 `http://127.0.0.1:4378`；直接打开 `floorplan/index.html` 时，除了提问，其他功能仍在；关闭最后一个标签大约两小时后服务器自己停，提前停用 `node floorplan/serve.mjs --stop`。这些同样未经本次运行。

## Health check 能查什么、不能当安全审计

README 对 Health check 的原话是：**A check, not an audit.** 不能把它当成安全审计。

同一段列出的检查项是：

- 密钥写在代码里，或被送到浏览器
- 谁都可以读的 Supabase 表
- 敞开的 Firebase 规则
- 谁都可以伪造的 Stripe webhook
- 没有登录要求的端点

每条附有可以贴回去的修复提示。README 的示例问法是 “Fix the important issues from the floorplan's Health check”。`plugin.json` 的长描述写成 “exposed keys and endpoints anyone can change”，和上面这五条不是同一句。检查项以 README 的列举为准。

它写明不保存、不显示密钥的值，只标出位置。本文没有对任何仓库跑过这项检查，没有发现列表可以引用。

## 审批与沙箱：为什么要在沙箱外起服务器、不想允许时怎么手动起

Codex 文档写：打开地图时，Codex 会请求在沙箱外运行地图服务器。原因是服务器必须在那条命令结束后继续跑，Ask 也要能再调用 Codex。

不想允许这次沙箱外运行时，在项目目录自己起：

```bash
node floorplan/serve.mjs
```

是否点允许，按你对这台机器和这个仓库的信任决定。插件自查一文讲了第三方插件的信任记录该怎么看。

## 和 Archify、Understand Anything 怎么选

下面这张是 **README 自己的对比**，2026-11-17 从 Floorplan README 的 “Floorplan, Archify or Understand Anything?” 转述。本文没有复测 Archify 的出图，也没有安装 Understand Anything，只确认 [Understand Anything 仓库](https://github.com/Egonex-AI/Understand-Anything) 当天可以打开。Archify 的安装和 10 种图以[本库专文](../13-社区生态与项目评测/04-Codex使用Archify生成架构图.md)为准。

| | Floorplan | Archify | Understand Anything |
|---|---|---|---|
| README 说它回答的问题 | 我做出的这个应用实际怎么运转，有什么值得担心 | 怎样把这件事讲清楚 | 这个大代码库一直到函数是怎么工作的 |
| README 说给谁 | 用 AI 做应用、但不读代码的人 | 要解释系统、流程或想法的人 | 要熟悉大型代码库的开发者 |
| README 说你得到什么 | 可缩放的整张应用地图，含页面、跨仓库请求、外部服务，以及 Health check、Recent work | 10 种图之一或单页说明，材料可以是仓库，也可以只是一段描述 | 文件、函数、类的知识图谱，带分层和导览 |

README 的选择句是：要看懂并检查自己的应用，用 Floorplan；要给文档、演讲或决策画一张图，用 Archify；要按函数读一个大仓库，用 Understand Anything。它还写两者可以一起用：Floorplan 画应用，Archify 再画其中一条流程。本文不引用 Trendshift 或其他排行。

## 升级、卸载和数据放在哪

升级，文档写先刷新 marketplace，再装一次插件：

```bash
codex plugin marketplace upgrade floorplan
codex plugin add floorplan@floorplan
```

2026-11-17 在刚装好的那个 `CODEX_HOME` 里执行了第一句，退出码 0。输出是 “Upgraded marketplace floorplan to the latest configured revision.” 插件当时已经是 0.11.0，没有为了升级再执行第二句。

卸载：

```bash
codex plugin remove floorplan@floorplan
codex plugin marketplace remove floorplan
```

卸载这两条本次没有对 Floorplan 执行。文档写地图仍留在每个项目的 `floorplan/` 目录，直到你自己删。Codex 侧不会去改 `AGENTS.md`（作者解释 Codex 没有一份像 `CLAUDE.local.md` 那样只属于你、又不提交的笔记文件）。`floorplan/` 自己忽略自己，不进 git。

## 常见问题与参考资料

**必须登录吗？** 生成地图和 Ask 要 ChatGPT 登录。本次 marketplace 和 plugin 的安装、列出、`mcp list` 在未登录时完成。

**会改我的业务代码吗？** README 写不会；它只写自己的 `floorplan/`。`plugin.json` 仍声明了 Write。以你批准的命令和 git diff 为准。

**语言范围？** README 列出 TypeScript、JavaScript、Python、Go、Rust、Java、Kotlin、Scala、Swift、C#、PHP，以及 Vue、Svelte、Astro 和 Shopify 主题（Liquid），并写其他语言支持更轻。端点和页面框架还有一长串，以 README 的 How it works 为准。

**和 Archify 冲突吗？** 不冲突。一个是可点击的应用地图加健康检查，一个是文档用的图。

参考资料：

- [haydenschmitty/floorplan](https://github.com/haydenschmitty/floorplan)（MIT，2026-11-17 查询 4,635 star）
- [Floorplan in Codex](https://github.com/haydenschmitty/floorplan/blob/main/docs/codex.md)
- [Getting started](https://github.com/haydenschmitty/floorplan/blob/main/docs/getting-started.md)
- [Live demo](https://haydenschmitty.github.io/floorplan-demo/)
- [Is it safe to install?](https://github.com/haydenschmitty/floorplan/blob/main/docs/is-it-safe.md)（作者列出的本机行为；本文没有复跑其中的校验测试）
- [Codex plugins](https://learn.chatgpt.com/docs/plugins)
