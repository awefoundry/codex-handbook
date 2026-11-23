---
id: codex-ui-ux-pro-max-skill
title: "Codex 安装 UI UX Pro Max Skill：用 uipro init --ai codex 装进项目，按产品类型生成设计系统再写界面"
seo_title: "Codex 安装 UI UX Pro Max：uipro init --ai codex"
description: "UI UX Pro Max 是 NextLevelBuilder 维护的开源 Skill，不是 OpenAI 内置功能。本文用 ui-ux-pro-max-cli 2.15.0 执行 uipro init --ai codex，核对写进项目的文件，并在未登录的 Codex CLI 0.171.0 里确认插件市场和技能列表。没有在会话里生成界面。"
lede: "先看它会写进哪些目录，再决定要不要让 Codex 按里面的规则写界面。npm 包和 GitHub main 不是同一份技能正文。"
url: /guides/codex-ui-ux-pro-max-skill
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI]
difficulty: 进阶
order: 28
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-23
date_modified: 2026-11-23
verified_on: 2026-11-23
tested_cli_version: 0.171.0
official_ref: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
keywords: [Codex UI UX Pro Max, ui-ux-pro-max-skill, uipro init --ai codex, Codex 设计 Skill, Codex 前端界面设计]
related: [codex-hallmark-design-skill, create-codex-skill, codex-skillspector-skill-security-scan]
howto: true
faq:
  - q: 这是 OpenAI 的官方 Skill 吗？
    a: 不是。仓库 nextlevelbuilder/ui-ux-pro-max-skill 由 NextLevelBuilder 维护，许可证是 MIT。Codex 只是 README 和 CLI 写明可以安装的对象之一。
  - q: npm 上的 2.15.0 和 GitHub main 是同一份技能吗？
    a: 不是。2026-11-23 的 main 上 SKILL.md 写的是 80 个可搜索样式（51 个在用）、194 套产品配色、141 条 UX 指南。同一天用 ui-ux-pro-max-cli 2.15.0 执行 uipro init --ai codex，写进项目的 SKILL.md 是 79、192 和 119。最新 Release 和 npm 版本都停在 2026-08-13 的 2.15.0。
  - q: 装上之后 Codex 会自动改我的页面吗？
    a: 本文没有登录，也没有在会话里发送界面任务。技能列表里能看到名字，只说明 Codex 读到了 SKILL.md 的 name 和 description。会不会改文件，要等你自己的会话，并受当前审批和沙箱约束。
  - q: README 里的 Premium 要不要跟着装？
    a: 本文不写付费内容。需要知道的是，2.15.0 的 uipro init --ai codex 除了 ui-ux-pro-max，还会写下 brand、design、slides 等另外 6 个技能目录。回答 yes 的卸载会把这 7 个一起删掉。
---

# Codex 安装 UI UX Pro Max Skill：用 uipro init --ai codex 装进项目，按产品类型生成设计系统再写界面

> 核对依据：第三方仓库 [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) 的 README、[MIT 许可证](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE)、`.agents/plugins/marketplace.json`、`skill.json`、`.claude-plugin/plugin.json` 和 main 上的 `.claude/skills/ui-ux-pro-max/SKILL.md`。2026-11-23 通过 GitHub API 查询：152,865 star，许可证 MIT，`pushed_at` 为 `2026-11-22T04:08:27Z`。默认分支最新提交 `6ec2bb58334ca3014573c4cbd4834ee3a40afd9d` 的时间是 `2026-11-22T04:08:26Z`，说明为 `feat(i18n): add Arabic query synonym normalization and RTL-safe HTML preview rendering (#586)`。最新 Release [v2.15.0](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases/tag/v2.15.0) 发布于 `2026-08-13T17:10:40Z`。npm 包 `ui-ux-pro-max-cli` 的 `version` 是 2.15.0，`time.modified` 是 `2026-08-13T17:10:40.157Z`。Codex CLI 为 `@openai/codex@0.171.0`，`codex --version` 输出 `codex-cli 0.171.0`。插件命令和 `codex debug prompt-input` 都在未登录的独立 `CODEX_HOME` 里运行。没有打开桌面应用，没有在会话里生成页面，没有配图。

这是 **NextLevelBuilder** 维护的前端设计技能仓库，不是 OpenAI 的内置设计功能。README 把它写成一个给编码代理用的 Skill：处理界面任务时，先按产品类型检索本地数据，生成配色、字体和布局规则，再写代码。Codex 会不会在你的会话里真的这么做，取决于它是否读到这份 `SKILL.md`、描述是否匹配，以及你有没有允许它改文件。本文只验证安装、文件内容和技能能否被 Codex 列出来。

已经在用另一套设计约束的，可以对照 [Hallmark](../07-Skills实战/08-Codex安装Hallmark设计Skill-让页面少点AI模板味.md)。Skill 文件本身怎么写，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

## 先说结论

2026-11-23 用 npm 上的 `ui-ux-pro-max-cli@2.15.0` 在临时项目里执行 `uipro init --ai codex`，安装器打印 `Installing for: Codex (.agents/skills/)`，并写下 **7 个**技能目录，不只是 `ui-ux-pro-max`。其中 `ui-ux-pro-max/SKILL.md` 的 `name` 是 `ui-ux-pro-max`。把 `HOME` 指到这次全局安装的目录后，`codex debug prompt-input` 能列出这 7 个不带前缀的名字。

另一条路是插件市场。`codex plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` 能读到仓库里的 `.agents/plugins/marketplace.json`。接着 `codex plugin add ui-ux-pro-max@ui-ux-pro-max-skill` 装上的是 **GitHub main 的检出**，版本号显示 2.15.0，但技能正文里的计数和 npm 包写进项目的那份不一样。插件技能在列表里带 `ui-ux-pro-max:` 前缀。

README 把 Brand、Logo、CIP、Banner、Slides 放在付费 Premium 的对比里。本文不写付费档，也不放购买链接。开源 CLI 这次实际写下的目录见下一节。

没有在已登录的 Codex 会话里发送 `$ui-ux-pro-max`，也没有让它改任何一个前端项目。

## 装之前

README 的 Prerequisites 写：搜索脚本需要 **Python 3**，只用标准库，脚本自己不安装依赖、不访问网络。检查命令是 `python3 --version`。

CLI 本身来自 npm，所以还要有 Node.js 和 npm。2026-11-23 这台 Linux 上是 Python 3.12.3、Node.js v22.23.4。

两条安装范围：

| 方式 | 命令 | 2026-11-23 写到哪里 |
|---|---|---|
| 当前项目 | `uipro init --ai codex` | 项目下的 `.agents/skills/` |
| 全局 | `uipro init --ai codex --global` | 当时 `$HOME/.agents/skills/` |

README 的 Global Install 例子里没有 `--ai codex`，只有 `uipro init --ai universal --global`，并注明目标是 `~/.agents/skills/`。2.15.0 的 `uipro init --help` 仍接受 `--ai codex` 和 `--global` 一起用。在隔离的 `HOME` 里实测，安装器打印 `Installing for: Codex (.agents/skills/) (global)`，7 个目录出现在这个 `HOME` 的 `.agents/skills/` 下。

`--global` 会进家目录。不确定要不要给所有项目用时，先装在一个临时项目里。

## 用 uipro init --ai codex 装进项目

README 的推荐安装是：

```bash
npm install -g ui-ux-pro-max-cli
cd /path/to/your/project
uipro init --ai codex
```

`uipro --version` 在 2.15.0 上打印 `2.15.0`。`uipro init --help` 的 `--ai` 列表里有 `codex`。README 现在还列出 kimi、amazonq、openclaw、zcode 等助手，2.15.0 的这份帮助里没有。以你本机的 `uipro init --help` 为准。

README 写了 `uipro init --dry-run`。2.15.0 的实际结果是：

```text
error: unknown option '--dry-run'
```

临时项目里不带 `--dry-run` 的安装输出：

```text
UI/UX Pro Max Installer

info Installing for: Codex (.agents/skills/)
- Installing files...
✔ Generated from templates!

info Installed folders:
  + .agents

success UI/UX Pro Max installed successfully!
```

`.agents/skills/` 下有这 7 个目录：

| 目录 | SKILL.md 的 name | description 在说什么 |
|---|---|---|
| `ui-ux-pro-max` | `ui-ux-pro-max` | 界面设计、审查和修复；本地可搜索的样式、配色、字体、UX 指南、图标、图表和 22 个技术栈 |
| `ui-styling` | `ui-styling` | shadcn/ui、Tailwind 和画布式视觉 |
| `design-system` | `design-system` | 设计令牌、组件规格和幻灯片 |
| `design` | `design` | 品牌、Logo、CIP、幻灯片、横幅、图标；正文里点名了外部图像模型 |
| `brand` | `brand` | 品牌语气、视觉识别和规范 |
| `banner-design` | `banner-design` | 社交、广告和网页横幅 |
| `slides` | `slides` | HTML 演示文稿 |

`ui-ux-pro-max` 这一份有 71 个文件，包括 `scripts/search.py` 和 `data/` 下的 CSV。安装器写的是 **CLI 包里的模板**，不是当场去拉 GitHub main。

同一天 GitHub main 的 `.claude/skills/ui-ux-pro-max/SKILL.md` 开头是：

> Searchable local data: 80 searchable styles (51 active), 194 product palettes and reasoning profiles, 74 font pairings, 141 UX guidelines, 105 icons, 17 GSAP presets, 25 chart types, and 22 stacks.

2.15.0 写进项目的对应句子是 **79** searchable styles（**50** active）、**192** product palettes、**119** UX guidelines，字体、图标、GSAP、图表和技术栈的数字相同。`src/ui-ux-pro-max/templates/platforms/codex.json` 在 main 上的 `skillPath` 只有 `skills/ui-ux-pro-max`，description 计数也是 80 / 51 / 194 / 141。不要把 main 上的计数当成 `uipro init` 已经写进项目的内容。

main 上 `skill.json` 和 `.claude-plugin/plugin.json` 的 `version` 都是 `2.15.0`。同一检出里 `cli/package.json` 的 `version` 是 `2.5.0`。npm 上已发布、并且 `uipro --version` 打印出来的是 **2.15.0**。不要按仓库里那个 `2.5.0` 去装旧包。

`uipro versions` 会联网拉取版本列表。2026-11-23 它把 `v2.15.0 (8/13/2026)` 标成 latest，并提示先更新 CLI 包再执行 `uipro init`。

## 另一条路：从插件市场装

仓库有 [`.agents/plugins/marketplace.json`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.agents/plugins/marketplace.json)。2026-11-23 读到的内容是：市场名 `ui-ux-pro-max-skill`，插件名 `ui-ux-pro-max`，`source` 为 `local`、`path` 为 `./`，`policy.authentication` 为 `ON_INSTALL`。

`codex plugin --help` 里有 `marketplace` 和 `add`。在独立 `CODEX_HOME`、`codex login status` 为 `Not logged in` 时：

```bash
codex plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
```

```text
Added marketplace `ui-ux-pro-max-skill` from https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git.
```

`codex plugin list` 这时显示 `ui-ux-pro-max@ui-ux-pro-max-skill` 的状态是 **not installed**，来源路径指向市场检出里的 `.agents/plugins/marketplace.json`。只加市场不会把技能写进当前项目的 `.agents/skills/`。

README 没有写 Codex 的 `plugin add` 命令。Codex 自己的帮助写的是 `PLUGIN@MARKETPLACE`。继续执行：

```bash
codex plugin add ui-ux-pro-max@ui-ux-pro-max-skill
```

```text
Added plugin `ui-ux-pro-max` from marketplace `ui-ux-pro-max-skill`.
```

再次 `codex plugin list`，状态是 `installed, enabled`，版本 `2.15.0`。没有弹出登录。`policy.authentication` 写成 `ON_INSTALL`，这次 CLI 安装没有再要一次授权；桌面端会不会另外提示，本文没有打开桌面端，不能下结论。

插件缓存是这次克隆的仓库。里面 `.claude/skills/ui-ux-pro-max/SKILL.md` 的计数是 main 的 80 / 51 / 194 / 141，不是 npm 模板的 79 / 50 / 192 / 119。`.claude-plugin/plugin.json` 的 `skills` 字段是 `./.claude/skills/`。

用这个 `CODEX_HOME` 跑 `codex debug prompt-input`，技能根目录指向缓存里的 `.claude/skills`，列表中的名字带插件前缀：

- `ui-ux-pro-max:ui-ux-pro-max`
- `ui-ux-pro-max:ui-styling`
- `ui-ux-pro-max:design-system`
- `ui-ux-pro-max:design`
- `ui-ux-pro-max:brand`
- `ui-ux-pro-max:banner-design`
- `ui-ux-pro-max:slides`

`codex debug prompt-input` 打印的是模型可见输入，不是交互界面里的 `/skills` 菜单。输出里的 `r0`、`r1` 是这一次给技能根目录起的标记，顺序不固定，不是要你创建的文件夹。

## 在 Codex 里怎么触发

官方 [Build skills](https://learn.chatgpt.com/docs/build-skills) 写了两种用法：在 Codex CLI 或 IDE 里用 `/skills`，或输入 `$` 点名；描述匹配时也可能被隐式选中。README 的 Skill Mode 把 Codex CLI 列在自动启用的名单里，例子是直接说 `Build a landing page for my SaaS product`。Workflow Mode 的斜杠命令 `/ui-ux-pro-max` 只写了 Kiro、Roo Code、KiloCode，没有写 Codex。

本文没有登录，没有打开 TUI，没有发送 `$ui-ux-pro-max`，也没有用一句自然语言去改页面。能确认的只有：技能的 `name` 和 `description` 进入了 `prompt-input` 的可用技能列表。

`ui-ux-pro-max/SKILL.md` 是写给代理执行的工作流（何时该用、按优先级查规则、要求跑 `search.py`）。README 还写明：缺 Python 时，使用这个 Skill 的代理应该请人来装，而不是自己在机器上安装软件。本文只执行了教程要核对的安装命令和下面这一次搜索脚本，没有按 `SKILL.md` 去生成界面，也没有运行 `design`、`brand` 等目录里指向外部图像模型的脚本。`SKILL.md` 里没有看到要求忽略既有指令的句子；这只说明扫过这份文件，不能代替你自己读完再装。

装第三方 Skill 之前的扫描步骤见 [SkillSpector](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。本文没有跑 SkillSpector。

## 设计系统命令

README 的示例路径是 `.claude/skills/ui-ux-pro-max/scripts/search.py`。Codex 这次装出来的路径是：

```text
.agents/skills/ui-ux-pro-max/scripts/search.py
```

2.15.0 这份 `search.py --help` 有 `--design-system`、`--persist`、`--page`、`--output-dir`、`--format`、`--stack`、`--domain`，以及 `--variance`、`--motion`、`--density`。帮助里 **没有** README 现在写的 `--tokens`、`--rtl`、`--preview`。不要在 2.15.0 的脚本上照抄这几个新旗标。

在临时目录执行：

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp" --output-dir /path/to/output
```

退出码 0，耗时不到 1 秒。终端开头是：

```text
TARGET: MyApp - RECOMMENDED DESIGN SYSTEM
PATTERN
  Name: Hero + Features + CTA
STYLE
  Name: Glassmorphism
COLORS
  Primary:       #2563EB    (--color-primary)
```

`--persist` 写下 `design-system/myapp/MASTER.md`。文件头是：

```text
Project: MyApp
Generated: 2026-11-23 01:20:23
Category: SaaS (General)
```

色板表里 Primary 是 `#2563EB`，Accent/CTA 是 `#EA580C`，Background 是 `#F8FAFC`。这是查询 `"SaaS dashboard"`、项目名 `MyApp` 的这一次输出，不是所有 SaaS 项目都会得到的配色。README 写脚本不访问网络；这次只看到它写了本地文件，没有抓包。

`MASTER.md` 自己写：某个页面如果有 `design-system/pages/[page-name].md`，以页面文件为准，否则跟随 Master。`--page` 能写页面覆盖文件。本文没有加 `--page`。

这些规则要变成页面，仍然要 Codex 或你自己去改代码。脚本不改现有组件。

## 更新、卸载与常见问题

**更新。** `uipro versions` 在 2026-11-23 仍把 2.15.0 标成 latest，和 npm、GitHub Release 一致。main 在 2026-11-22 还有新提交，但没有新的 Release，也没有更新的 npm 版本。`uipro update` 的帮助写的是用已安装的 CLI 包刷新技能文件，所以它不会把项目里的模板换成比 2.15.0 更新的 main。想要 main 上那份 80 / 194 / 141 的正文，这次是插件市场克隆的仓库，不是 `uipro init`。

**卸载。** 2.15.0 的 `uipro uninstall --ai codex` 在没有交互回答时停在：

```text
Remove UI/UX Pro Max skill for Codex (.agents/skills/) from <项目目录>? (y/N)
```

这次不回答，7 个目录都还在。回答 `yes` 之后，它删掉的是全部 7 个，而不只是 `ui-ux-pro-max`：

```text
Removed:
  - .agents/skills/ui-ux-pro-max
  - .agents/skills/banner-design
  - .agents/skills/brand
  - .agents/skills/design
  - .agents/skills/design-system
  - .agents/skills/slides
  - .agents/skills/ui-styling
```

README 的手动删除例子是：

```bash
rm -rf .agents/skills/ui-ux-pro-max   # Antigravity / Codex
```

这一行只覆盖其中一个目录。如果 `uipro init` 还写下了另外 6 个，只执行这一行会把它们留下。

**Premium。** README 有一节 Basic 与 Premium 的对比，Premium 写了品牌、Logo、CIP、横幅、幻灯片、图标和图像生成，并链到 uupm.cc。本文不介绍付费档。开源安装已经把同名技能目录放进了 `.agents/skills/`，其中 `design` 的 description 提到外部图像服务。用之前先读对应的 `SKILL.md`。

**和 Hallmark 怎么分。** Hallmark 给的是主题文件和浏览器检查脚本。UI UX Pro Max 给的是可搜索的样式、配色和产品类型数据，外加一份设计系统 Markdown。两个都是第三方 Skill，可以都不装。

## 参考资料

- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [Release v2.15.0](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases/tag/v2.15.0)
- [npm ui-ux-pro-max-cli](https://www.npmjs.com/package/ui-ux-pro-max-cli)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)
- [Hallmark](../07-Skills实战/08-Codex安装Hallmark设计Skill-让页面少点AI模板味.md)
- [SkillSpector](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)

查询日期 2026-11-23。星标、main 上的技能正文和 npm 模板会继续变化。安装前再看一次 README 和你本机 `uipro init --help`、`search.py --help`。
