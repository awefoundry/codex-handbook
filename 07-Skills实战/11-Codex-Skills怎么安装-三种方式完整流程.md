---
id: codex-skills-install-guide
title: Codex Skills 怎么安装：$skill-installer、文件目录和 plugin marketplace 三种方式
seo_title: Codex Skills 怎么安装：$skill-installer、文件目录和 plugin marketplace 三种方式
description: Codex Skills 有三种安装方式：$skill-installer 装官方精选，手动放 SKILL.md 文件装个人和项目级 Skill，codex plugin marketplace 命令装第三方 Skill 包。本文按这三条路逐一说明步骤、目录位置、调用方式和常见问题。
lede: 装上之后要新开一次会话，Codex 才能发现新 Skill。
url: /guides/codex-skills-install-guide
status: published
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 11
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-24
date_modified: 2026-11-24
verified_on: 2026-11-24
official_ref: https://learn.chatgpt.com/docs/build-skills
keywords: [Codex Skills 安装, skill-installer, SKILL.md, plugin marketplace, how to install skills in codex, codex skills, .agents/skills]
related: [create-codex-skill, codex-agent-skills-plugin, codex-record-replay-skill, codex-skillspector-skill-security-scan]
faq:
  - q: 装完 Skill 之后为什么还是找不到？
    a: 安装后必须新开一次 Codex 会话。已打开的会话不会重新扫描刚加入的 Skill 文件。
  - q: $skill-installer 和 plugin marketplace 有什么区别？
    a: $skill-installer 是 Codex 自带的 Skill，按名字安装官方精选的单个 Skill；plugin marketplace 安装的是插件，一个插件可以同时带多个 Skill 和 MCP 工具。
  - q: IDE 扩展能用插件里的 Skill 吗？
    a: 官方插件文档写明 IDE 扩展不支持插件，需要用 CLI 或 ChatGPT 应用安装。手动放进 .agents/skills 目录的单个 Skill 不受这条限制。
---

# Codex Skills 怎么安装：$skill-installer、文件目录和 plugin marketplace 三种方式

> 难度　基础
>
> 类型　安装与配置

Codex Skills 是把重复工作保存成可调用说明的机制。装好的 Skill，Codex 可以按名字直接调用，也可以在任务匹配时自动加载。

安装方式有三条：

1. **$skill-installer**：在 Codex 会话里一行命令，装官方精选 Skill。
2. **手动放文件**：把 SKILL.md 文件放进对应目录，适合自己写的和从仓库克隆的 Skill。
3. **codex plugin marketplace**：用 CLI 命令安装第三方打包的 Skill 集合。

三条路的前提都一样：**装完后要新开一次会话，Codex 才会扫描到新 Skill**。

## Skill 和插件是什么关系

Skill 是一个带 `SKILL.md` 的文件夹，包含名称、触发描述和操作说明。插件（Plugin）是把一个或多个 Skill、MCP 工具打包在一起的可安装包。

- 只需要一套说明：直接用 Skill。
- 需要说明加工具，或者要给别人安装：用插件。

这篇文章讲安装，不讲写法。写 Skill 的步骤在[从零创建 Codex Skill](/guides/create-codex-skill)。

## 方式一：$skill-installer（官方精选）

在 Codex 会话里输入：

```text
$skill-installer <skill名称>
```

例如安装 linear：

```text
$skill-installer linear
```

`skill-installer` 是 Codex 自带的系统 Skill。官方文档还写明，可以让它从其他仓库下载 Skill。

安装完成后，新开一次会话，输入 `/skills` 确认 Skill 已经出现在列表中。

> 本文没有在已登录会话里实际运行 `$skill-installer`，Skill 落到哪个目录、输出什么，以你当前界面为准。

## 方式二：手动放文件

这是安装自己写的或从 GitHub 克隆的单个 Skill 时最直接的方式。

Codex 会扫描下面几个目录：

| 目录 | 适用范围 |
|---|---|
| `$CWD/.agents/skills/` | 启动 Codex 的当前目录 |
| `$CWD/../.agents/skills/` | 当前目录的上一级（在 Git 仓库内） |
| `$REPO_ROOT/.agents/skills/` | 仓库根目录，整个仓库共用 |
| `$HOME/.agents/skills/` | 个人，作用于所有仓库 |
| `/etc/codex/skills/` | 管理员级，整台机器共用 |

创建个人目录并放入一个 Skill 的步骤：

```bash
mkdir -p ~/.agents/skills/my-skill
# 把 SKILL.md 放进去
cp /path/to/SKILL.md ~/.agents/skills/my-skill/SKILL.md
```

SKILL.md 的最小格式：

```yaml
---
name: my-skill
description: 一句话说明这个 Skill 做什么，以及什么情况下应该调用它。
---

这里写具体操作说明。
```

`name` 和 `description` 是必须的。`description` 决定 Codex 会不会在合适的时机自动选它，所以要写清楚触发场景。

放好文件之后，新开一次 Codex 会话，输入 `/skills` 验证。

## 方式三：codex plugin marketplace（第三方包）

第三方开发者把多个 Skill 打包成插件，放在 GitHub 仓库里。用 `codex plugin` 命令安装。

### 安装步骤

**第一步：把插件仓库注册为 marketplace**

```bash
codex plugin marketplace add <GitHub仓库路径或URL>
```

例如安装 Addy Osmani 的 agent-skills：

```bash
codex plugin marketplace add addyosmani/agent-skills
```

这一步把这个仓库登记成名为 `agent-skills` 的 marketplace，本地不会立刻下载 Skill 文件。

**第二步：从 marketplace 安装插件**

```bash
codex plugin add <插件名>@<marketplace名>
```

例如：

```bash
codex plugin add agent-skills@agent-skills
```

在 `codex-cli 0.166.0` 上实测，两条命令的输出是：

```text
Added marketplace `agent-skills` from https://github.com/addyosmani/agent-skills.git.
Added plugin `agent-skills` from marketplace `agent-skills`.
```

**第三步：新开会话**

关闭当前会话，重新打开 Codex，新会话里的 Skill 才生效。

### 管理已安装的插件

列出已安装插件：

```bash
codex plugin list
```

输出示例：

```text
PLUGIN                     STATUS              VERSION  SOURCE
agent-skills@agent-skills  installed, enabled  0.6.14   <marketplace 路径>
```

刷新已登记的 Git marketplace 快照：

```bash
codex plugin marketplace upgrade
```

卸载插件：

```bash
codex plugin remove agent-skills@agent-skills
codex plugin marketplace remove agent-skills
```

只删插件保留 marketplace，停在第一条。

### 在 ChatGPT 桌面应用或网页里安装

打开 Plugins 标签，搜索或浏览，点安装。如果插件需要连接 MCP 工具，安装时会提示配置。装完后新开一次对话。

## 安装后怎么调用

安装好的 Skill 有两种调用方式：

**显式调用**：在 Codex CLI 或 IDE 扩展里输入 `$` 加 Skill 名：

```text
$spec-driven-development
```

ChatGPT 里用 `@`：

```text
@spec-driven-development
```

CLI 里也可以输入 `/skills` 打开浏览器，从列表里选。

**隐式调用**：描述任务，不点名 Skill。Codex 读取所有已安装 Skill 的 description，任务匹配时自动加载。

## 验证是否装上

新开会话后在 CLI 里输入：

```text
/skills
```

列表里出现刚装的 Skill 名就说明安装成功。如果列表里没有：

1. 确认已经新开了一次会话，不是在原来的会话里继续。
2. 确认文件路径正确：`~/.agents/skills/<skill名>/SKILL.md`，注意中间的 `.agents` 有前缀点号。
3. 对于 plugin marketplace 安装的，用 `codex plugin list` 确认状态是 `installed, enabled`。

## 安全检查

从第三方 GitHub 仓库安装插件前，建议核查：

- 仓库作者、许可证和最近更新时间。
- 插件根目录的 `plugin.json`，看它会带上哪些 Skill 和 MCP 工具。
- 打算用的那个 `SKILL.md` 的内容，确认步骤和你的项目规则不冲突。

扫描第三方 Skill 有没有提示注入风险，可以用 [SkillSpector](/guides/codex-skillspector-skill-security-scan)。

## 常见问题

**IDE 扩展装不了插件。** 官方插件文档写明 IDE 扩展不支持插件，要用 CLI 或 ChatGPT 应用安装。手动放进 `.agents/skills` 的单个 Skill 不受这条限制。

**连不上 GitHub。** 先把仓库克隆到本地，再把本地路径登记成 marketplace：`codex plugin marketplace add /path/to/local/clone`。

**同名 Skill 有多个。** Codex 会保留所有同名 Skill，不会自动覆盖。用 `config.toml` 的 `[[skills.config]]` 按路径指定启用哪一个，细节见[从零创建 Codex Skill](/guides/create-codex-skill)里的禁用部分。

## 下一步

- 想自己写一个 Skill：[从零创建 Codex Skill](/guides/create-codex-skill)
- 想用 agent-skills 这套 25 个工程 Skill 的包：[Codex 安装 agent-skills 插件](/guides/codex-agent-skills-plugin)
- 想扫描第三方 Skill 的安全风险：[SkillSpector 安全扫描](/guides/codex-skillspector-skill-security-scan)

## 参考资料

- [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI：Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [OpenAI：Plugins](https://learn.chatgpt.com/docs/plugins)
