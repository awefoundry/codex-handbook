---
id: codex-obsidian-skills
title: Codex 安装 Obsidian 官方 Skills：让 Codex 读写 Markdown、Bases 和 Canvas，还能调用 Obsidian CLI
seo_title: Codex 安装 Obsidian 官方 Skills：Markdown、Bases、Canvas 与 CLI
description: Obsidian 官方发布的 obsidian-skills 已支持 Codex。本文按 README 说明用 codex plugin marketplace add 装上，介绍 7 个技能各管什么、怎么让 Codex 写出带 wikilink 和 callout 的笔记、编辑 Bases 与 Canvas，以及使用 Obsidian CLI 时要注意的边界。
lede: 先加 marketplace，再装 Obsidian 插件。让 Codex 改笔记库之前先备份，并且只打开它需要的那个库。
url: /guides/codex-obsidian-skills
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 26
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-18
date_modified: 2026-11-18
verified_on: 2026-11-18
tested_cli_version: 0.169.1
official_ref: https://github.com/obsidianmd/obsidian-skills
keywords: [Codex Obsidian, obsidian-skills, Obsidian Skills 安装, Codex 笔记库, Obsidian CLI]
related: [codex-agent-browser, create-codex-skill, mcp-getting-started]
howto: true
faq:
  - q: 这是 OpenAI 的内置功能吗？
    a: 不是。仓库 obsidianmd/obsidian-skills 由 Obsidian 维护，许可证是 MIT。Codex 只是 README 写明支持的安装对象之一。笔记、同步和发布都发生在你自己的库和 Obsidian 账号上。
  - q: 装上之后 Codex 就能改我的库吗？
    a: 插件装上，只是把 7 个技能的说明交给 Codex。obsidian-cli 技能要求本机已经打开 Obsidian，并且 obsidian 命令可用。headless 用的是另一条命令 ob，会改远程同步或发布状态。让它读写库之前先备份，并且只把需要的目录交给当前任务。
  - q: 本文实际改过一篇笔记或一张 Canvas 吗？
    a: 没有。2026-11-18 在未登录的独立 CODEX_HOME 里添加了 marketplace，并用 codex plugin add 装上了 obsidian@obsidian-skills 1.2.0。写作环境没有 Obsidian 桌面端，没有笔记库，没有运行 obsidian、ob、defuddle 或 knap。
  - q: 为什么不要去 npm 上装一个叫 obsidian-cli 的包？
    a: obsidian-cli 技能写明：obsidian 命令随 Obsidian 安装包提供，不要安装无关的 npm 包 obsidian-cli。命令不存在时，按 Obsidian 帮助页打开 CLI，而不是另装一个同名包。
---

# Codex 安装 Obsidian 官方 Skills：让 Codex 读写 Markdown、Bases 和 Canvas，还能调用 Obsidian CLI

> 核对依据：GitHub 仓库 [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) 的 README、[MIT 许可证](https://github.com/obsidianmd/obsidian-skills/blob/main/LICENSE)、`.agents/plugins/marketplace.json`、`plugins/obsidian/plugin.json`，以及 `plugins/obsidian/skills/` 下 7 个 `SKILL.md`。2026-11-18 通过 GitHub API 查询：53,080 star、3,778 fork，`license` 为 MIT，`pushed_at` 为 `2026-11-17T22:37:17Z`，默认分支最新提交 `1c3f6df5683588e39b12462a75d1d0fcf550f955`（提交说明：Plugin: Update the ChatGPT listing for Headless）。Codex CLI 为 `@openai/codex@0.169.1`。插件命令在独立 `CODEX_HOME` 里运行，`codex login status` 为 `Not logged in`（退出码 1）。没有 Obsidian，没有配图。

这是 **Obsidian** 维护的技能仓库，不是 OpenAI 的内置笔记功能。README 写明这些技能遵循 [Agent Skills 规范](https://agentskills.io/specification)，Claude Code、Codex 和 Open Code 都可以用。它教代理使用 Obsidian 的开放格式（Markdown、Bases、JSON Canvas）和两条命令行：控制已打开的桌面端的 `obsidian`，以及不打开桌面端、用来同步和发布的 `ob`。

适合已经有 Obsidian 库、希望 Codex 按官方语法写笔记、改 Bases、画 Canvas 的人。只想了解 Skill 文件怎么写，先看 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

## 这个仓库是什么、7 个技能分别管什么

2026-11-18 的 README 表格和目录里都是这 7 个。触发条件来自各 `SKILL.md` 开头的 `description`。下表后半句是 README 的描述，用来说明它覆盖的格式；两边不一致时，以技能文件为准。

| 技能 | 什么时候会被选中（SKILL.md） | README 里它管什么 |
|---|---|---|
| `obsidian-markdown` | 处理 Obsidian 里的 `.md`，或提到 wikilink、callout、frontmatter、标签、嵌入、Obsidian 笔记 | Obsidian Flavored Markdown：wikilink、嵌入、callout、属性 |
| `obsidian-bases` | 处理 `.base`，或提到 Bases、表格、卡片、看板、过滤器和公式 | Bases：视图、过滤器、公式、汇总 |
| `json-canvas` | 处理 `.canvas`，或提到 Canvas、思维导图、流程图 | JSON Canvas：节点、边、分组 |
| `obsidian-cli` | 要求与库交互、搜笔记、从命令行操作库，或开发插件和主题 | 通过 [Obsidian CLI](https://help.obsidian.md/cli) 操作库，含插件和主题开发 |
| `obsidian-headless` | 要在服务器、CI 或终端里设置、运行 Obsidian Sync 或 Publish，或修改这两项设置 | 用 [Obsidian Headless](https://help.obsidian.md/headless) 同步和发布，不打开桌面端 |
| `defuddle` | 技能文件的 description 只有一句：用 Defuddle CLI 从 HTML 页面抽出干净的 Markdown | 用 [Defuddle](https://github.com/kepano/defuddle) 去掉网页杂讯 |
| `knap` | 要求套用 Knap 模板、把 JSON 或 CSV 变成笔记、批量生成 Markdown，或把 Defuddle 的输出排成笔记 | 用 [Knap](https://github.com/obsidianmd/knap) 按 JSON 或 CSV 渲染模板，含批量生成 |

`plugins/obsidian/plugin.json` 的版本是 **1.2.0**。`author.name` 是 Obsidian。marketplace 里插件名是 `obsidian`，来源是仓库内的 `./plugins/obsidian`。`policy.authentication` 写的是 `ON_INSTALL`。下面的 CLI 安装没有弹出登录，本文不解释这个字段在桌面端还会不会再要一次授权。

插件的长说明写：CLI 技能需要桌面端开着并且打开了 CLI；Headless 技能不需要桌面端；将来会加 MCP，以便在不在这台电脑上时、以及在 ChatGPT 手机端操作库。这是插件清单里的计划，本文没有看到这个 MCP。

## 安装：codex plugin marketplace add，再在插件目录里装 Obsidian

README 给 Codex 的命令只有一条：

```bash
codex plugin marketplace add obsidianmd/obsidian-skills
```

然后在 **Codex 或 ChatGPT 桌面 App 的插件目录**里安装 Obsidian。README 没有写一条对应的 `codex plugin install`。

2026-11-18 在 Linux、Codex CLI 0.169.1、独立 `CODEX_HOME`、未登录的前提下，这条 marketplace 命令的输出是：

```text
Added marketplace `obsidian-skills` from https://github.com/obsidianmd/obsidian-skills.git.
```

`codex plugin marketplace list` 能看到 `obsidian-skills`。此时 `codex plugin list` 里 `obsidian@obsidian-skills` 的状态是 **not installed**。

同一个未登录环境里，再用 CLI 安装（这是 0.169.1 的 `codex plugin add` 能做的事，README 的正文步骤仍然是去插件目录里点安装）：

```bash
codex plugin add obsidian@obsidian-skills
```

输出是 `Added plugin obsidian from marketplace obsidian-skills`，版本 **1.2.0**。再次 `plugin list`，状态为 `installed, enabled`。缓存目录里 7 个 `SKILL.md` 都在。`config.toml` 里出现了 marketplace 的 git 源，以及 `plugins."obsidian@obsidian-skills"` 的 `enabled = true`。

桌面 App 的插件目录没有打开，所以没有安装截图。你本机如果走 README 的图形安装，装完以插件目录里的名字和版本为准。

写作环境把 `CODEX_HOME` 放在 `/tmp` 下时，CLI 会警告它拒绝在临时目录里创建 PATH 辅助程序。marketplace 添加和插件安装仍然成功。这是这次测试目录带来的警告，不是 README 里的步骤。

## 手动安装：复制 skills 目录到 ~/.agents/skills

README 的 Codex 手动安装：把 `plugins/obsidian/skills/` 复制到 Codex 的技能目录，通常是 `~/.agents/skills`。它同时指向 [Agent Skills 规范](https://agentskills.io/specification)。

另一条不限于 Codex 的命令是：

```bash
npx skills add https://github.com/obsidianmd/obsidian-skills
```

已配置 GitHub SSH 密钥时，README 也写了 `npx skills add git@github.com:obsidianmd/obsidian-skills.git`。本文没有运行 `npx skills`，也没有把目录复制到 `~/.agents/skills`。实际装上的是上一节的插件缓存。

OpenCode 和 Claude Code 的复制方式不同。README 特别写了：给 OpenCode 时要克隆整个仓库，不要只复制内层 `skills/`。那是 OpenCode 的说明，Codex 按上一节或 `~/.agents/skills` 即可。

## 三个跟着做的例子

下面三则提示是**本文写法**，用来对准技能文件里的语法。代码块摘自对应 `SKILL.md`，不是 Codex 在本文写作时生成的文件。写作环境没有 Obsidian，没有打开阅读视图或 Bases 视图来验收。

让 Codex 做这些事之前，先看文末的备份和目录范围。

### 写一篇带 wikilink 和 callout 的笔记

`obsidian-markdown` 要求：库内笔记用 `[[wikilink]]`，外部网址才用普通 Markdown 链接。链接按文件名解析，不按 `aliases`。callout 用 `> [!type]`。技能文件里的完整例子以这段开头：

```markdown
---
title: Project Alpha
date: 2024-01-15
tags:
  - project
  - active
status: in-progress
---

# Project Alpha

This project aims to [[improve workflow]] using modern techniques.

> [!important] Key Deadline
> The first milestone is due on ==January 30th==.
```

本文示例，把库名和笔记名换成你自己的：

```text
在库「Research」里新建一篇笔记，使用 Obsidian Flavored Markdown。
用 frontmatter 写 title、date 和 tags。
用 [[wikilink]] 连到已有笔记，不要把库内笔记写成普通 Markdown 链接。
用一条 callout 标出截止日期。
写完后列出你用到的 wikilink，方便我在阅读视图里点开核对。
```

技能还写了：表格里的别名竖线要写成 `[[Note\|Alias]]`；`#1984` 这种纯数字标签无效。这些规则以技能文件为准。官方语法说明在 [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)。该帮助页 2026-11-18 能打开，标题是 Obsidian Flavored Markdown；正文由 Obsidian Publish 在浏览器里渲染，本文没有从页面源码里抽出菜单步骤。

### 改一个 Bases 视图

`obsidian-bases` 写明：`.base` 文件是 YAML。视图类型有 `table`、`cards`、`list`、`map`、`kanban`。排序的 `direction` 必须是大写的 `ASC` 或 `DESC`，写成别的值会被静默忽略。看板需要 `groupBy`，并要求 Obsidian 1.14 或更高。地图视图需要经纬度和 Maps 社区插件。打不开时，技能让你检查 Settings → Core plugins 里的 Bases 是否打开。

技能文件里的表格视图示例：

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

本文示例：

```text
编辑 vault 里的 tasks.base，不要新建第二份。
保留现有的全局 filters。
把名为 Active 的视图改成 table：只显示 status 不是 done 的笔记，
按 due 升序，direction 写成大写 ASC。
order 里依次放 file.name、status、due。
改完用 YAML 解析检查一遍，并说明要在 Obsidian 里打开这个 .base 才能看到视图。
```

完整的 Task Tracker 例子在技能文件的 Complete Examples 里，包含公式和两个表格视图。本文没有把整段抄进来。Bases 语法的帮助页是 [Bases syntax](https://help.obsidian.md/bases/syntax)，2026-11-18 标题可打开。

### 生成一张 Canvas

`json-canvas` 写明：`.canvas` 顶层是 `nodes` 和 `edges` 两个数组，遵循 [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)。节点要有 `id`、`type`、`x`、`y`、`width`、`height`。`type` 是 `text`、`file`、`link` 或 `group`。边用 `fromNode` 和 `toNode` 指向已有节点。id 是 16 位小写十六进制。技能特别写了：**直接写 `.canvas` 文件**，不要用 `obsidian create content=` 来创建，因为那条命令会把 `\n` 换成真换行，JSON 会坏。

技能文件里的最小文本节点：

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

本文示例：

```text
在库里新建 project.canvas，直接写 JSON 文件，不要用 obsidian create。
两个文本节点，用一条带标签的边连起来。
id 用 16 位小写十六进制，并且互不重复。
写完检查：JSON 能解析，每条边的 fromNode 和 toNode 都能在 nodes 里找到。
中文内容的节点宽度按技能里的 CJK 建议，大约是拉丁文建议宽度的 1.5 倍。
```

## obsidian-cli 与 headless：先确认命令可用，哪些操作会改库

两条命令不要混用。`obsidian-headless` 技能写明：`ob` 只做同步和发布；不打开桌面端就改笔记时，直接编辑文件并遵循 `obsidian-markdown`；要控制正在运行的桌面端，用 `obsidian-cli`。

### 先确认 Obsidian CLI

技能要求先跑 `obsidian help`。命令不存在时，向用户说明如何按 [Obsidian CLI 帮助页](https://help.obsidian.md/cli) 打开 CLI。`obsidian` 随 Obsidian 安装包提供。帮助页 2026-11-18 能打开，标题是 Obsidian CLI。本文没有安装 Obsidian，所以没有 `obsidian help` 的输出，也不编写帮助页里没有被技能引用的开关名称。

技能写明的行为，执行前需要知道：

- Obsidian 要处于打开状态。找不到应用时，先打开桌面端再试。沙箱里的同样报错，也可能是沙箱挡住了本地套接字。
- 命令失败时退出码仍可能是 0，要读输出，再决定能不能说成功。
- WSL 上运行安装目录里的 `Obsidian.com`，不要运行 `Obsidian.exe`。技能写 `Obsidian.exe` 会直接退出且不打印输出。
- `vault=` 只有放在第一个参数时才生效。目标库不清楚、而且有好几个库时，先问是哪一个，再改文件。
- 笔记正文放在参数里当字面量，不要当成要执行的 shell。
- `content=` 里的 `\n` 和 `\t` 会被换成换行和制表符，且没有转义。含反斜杠的文本，或长于大约 4 KB 的正文，改为直接写文件。
- 文件名里有点号时，要带上扩展名。
- 不带 `file` 或 `path` 时，操作的是当前活动文件。

会改库的命令，技能原文里包括：

| 命令 | 技能里写的效果 |
|---|---|
| `obsidian create` | 新建笔记。`overwrite` 只在确实要覆盖已有文件时使用。`template=` 会替换 `content=` |
| `obsidian append` | 往笔记末尾加内容 |
| `obsidian rename`、`obsidian move` | 用这两条，不用文件系统的 `mv`，这样 Obsidian 能更新指向该文件的链接。若关闭了自动更新内部链接，Obsidian 会弹出对话框，命令会一直等到有人回答 |
| `obsidian delete` | 把文件移到废纸篓。只有用户明确要求时才加 `permanent` |
| `obsidian property:set` | 改笔记属性 |
| `obsidian daily:append` | 往每日笔记追加内容 |
| `obsidian plugin:reload`、`obsidian eval`、`obsidian dev:*` | 插件和主题开发。写正文优先用 `create` 和 `append`，不要用 `eval` |

`open` 会在 Obsidian 里打开文件，再加上 `newtab` 才用新标签。没有 `silent` 标志。

### Headless：同步和发布

`ob` 不需要桌面端。技能写它处于 open beta，需要 Node.js 22 或更高。命令不存在时，可以 `npm install -g obsidian-headless`。Sync 和 Publish 各自需要账号上的有效订阅。文档在 [Obsidian Headless](https://help.obsidian.md/headless)，2026-11-18 标题可打开。

会改变远程状态的操作，技能要求先从 list 或 status 的输出里确认库、站点和路径：

- `ob sync-setup`、`ob sync`、`ob sync-create-remote`、`ob sync-config` 会建立或修改同步。`--mode pull-only` 会忽略本地修改，`mirror-remote` 会把本地改动退回去，设置前要确认。
- 不要在同一台设备上对同一个库同时用桌面端 Sync 和 Headless Sync，技能写这会造成冲突。第一次同步前备份库文件夹。端到端加密库的密码由用户自己输入，不要替用户输入，也不要加 `--password`。
- `ob login` 在未登录时会要邮箱、密码和双重验证码。让用户在自己的终端里运行。不要向用户索要密码。
- `ob publish` 默认只包含属性里 `publish: true` 的笔记。`--all` 会包含每一个文件，只有用户要求时才用。先 `--dry-run` 并把变更给用户看。用户同意之后，无人值守才加 `--yes`。
- `ob publish-create-site` 会按 slug 建站点。`ob publish-unlink` 和 `ob sync-unlink` 会断开连接。

本文没有运行 `ob`，没有 Obsidian 账号。

### Defuddle 和 Knap

这两个技能调用的是另外的 CLI，不是 `obsidian` 命令。

- Defuddle：先 `defuddle --help`。没有就说明依赖，并可以 `npm install -g defuddle`。抽出 Markdown 用 `defuddle parse <url> --md`。工具不可用或报错时，技能禁止声称抽取成功。仓库链接是 [kepano/defuddle](https://github.com/kepano/defuddle)，那是另一个作者的项目。
- Knap：需要 Node.js 20 或更高。可以 `npm install -g knap` 或 `npx knap`。`knap render` 写文件，`knap batch` 会按 CSV、JSON 数组或一个目录批量生成。已有文件要 `--overwrite` 才会覆盖。`--dry-run` 只列出路径。技能禁止在工具不可用时声称渲染成功。

本文没有安装或运行这两条命令。

## 注意事项：读写笔记库前先备份，只给需要的目录

让 Codex 读取或修改笔记库之前：

1. **先备份**这个库的文件夹。Headless 技能对第一次同步写了同样的要求。
2. **只把这一次任务需要的库或目录交给 Codex**。`obsidian` 不带 `vault=` 时，会先找当前目录所在的库，再找最近聚焦的库。多库时先写清库名。
3. 插件和技能装上之后，Codex 仍要你在对话里提出具体任务才会去改文件。把任务范围写进提示：哪一个库、哪些路径可以改、哪些命令不能用（例如不要加 `permanent`，不要加 `publish --all`）。
4. `delete` 进废纸篓，`permanent` 才是另外一档。`overwrite`、`sync --mode mirror-remote`、`publish --all` 都会扩大改动。这些词没有出现在你的提示里时，不要让它自己加上。
5. 同步和发布花的是你的 Obsidian 订阅，站点会按技能里的 slug 出现在 `publish.obsidian.md` 下。发布前先看 `--dry-run`。
6. 这是第三方技能。装之前如果要做提示注入扫描，可以用仓库里已有的 [SkillSpector 一文](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md) 的方法。本文没有对这 7 个技能跑扫描。

权限和目录边界的通用做法，见 [MCP 与外部工具目录说明](./README.md)。浏览器自动化是另一条工具链，见 [agent-browser](./18-Codex用agent-browser做浏览器自动化-Skill与MCP两种接法.md)，不要和 Obsidian CLI 混成同一个接口。

## 常见问题与参考资料

装完插件，新开一轮对话再让 Codex 处理 `.md`、`.base` 或 `.canvas`。判断是否走对了技能，可以看它有没有遵守上面那些格式：库内链接是 wikilink、`.base` 是合法 YAML、`.canvas` 是合法 JSON 且边都指向存在的节点。最终是否渲染正确，要在 Obsidian 里打开文件看。本文没有这一步。

- [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills)
- [插件清单 plugin.json](https://github.com/obsidianmd/obsidian-skills/blob/main/plugins/obsidian/plugin.json)
- [Obsidian CLI](https://help.obsidian.md/cli)
- [Obsidian Headless](https://help.obsidian.md/headless)
- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Bases syntax](https://help.obsidian.md/bases/syntax)
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [Agent Skills 规范](https://agentskills.io/specification)
- [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)
