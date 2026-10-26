---
id: create-codex-skill
title: 从零创建 Codex Skill：$skill-creator 或手写 SKILL.md，测试触发、禁用和打包
seo_title: 从零创建 Codex Skill：skill-creator、触发测试、禁用与插件打包
description: 用 $skill-creator 或手写 SKILL.md 做一个最小可用 Skill，再测显式／隐式触发、用 config.toml 禁用，以及用插件打包分发。步骤对照 OpenAI Build skills 与 Package your plugin。
lede: 先做出一个能触发的 Skill，再谈禁用和打包；描述决定会不会被选中，插件才是对外分发。
url: /guides/create-codex-skill
status: published
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE, ChatGPT Work]
difficulty: 进阶
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-18
date_modified: 2026-10-22
client_validation_pending: false
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://developers.openai.com/codex/skills
keywords: [Codex Skill, skill-creator, SKILL.md, skills.config, 插件打包, 显式调用]
related: [codex-zhuan-shu-skill]
faq:
  - q: $skill-creator 和手写 SKILL.md 哪个更好？
    a: 都能做出可用 Skill。官方把 $skill-creator（ChatGPT Work 里是 @skill-creator）当作「用描述生成」的内置路径；你已经清楚目录与步骤时，手写文件夹同样有效。流程更好「演示」时，优先看 Record & Replay。
  - q: 不想删文件，只想先关掉某个 Skill，怎么做？
    a: 在 ~/.codex/config.toml 里用 [[skills.config]]，写上该 Skill 的 SKILL.md 路径，并设 enabled = false，然后重启 Codex。这是禁用本地 Skill，不是卸载插件。
  - q: 把 Skill 文件夹打成 zip 发给同事算不算官方分发？
    a: 官方推荐的可复用分发是插件：根目录 plugin.json，技能放在 skills/ 下，再通过 marketplace 安装。本地 .agents/skills 更适合本机或仓库内作者创作；跨人安装优先走插件，而不是自创 zip 约定。
---

# 从零创建 Codex Skill：$skill-creator 或手写 SKILL.md，测试触发、禁用和打包

> 本文在线版：[codexguide.io/guides/create-codex-skill](https://codexguide.io/guides/create-codex-skill)

> 核对依据：OpenAI《[Build skills](https://developers.openai.com/codex/skills)》（与 learn.chatgpt.com 同页）、以及《[Package your plugin](https://developers.openai.com/plugins/build/plugins)》。文中「我的用法」是操作顺序建议，不是官方强制流程。界面文案会随客户端变化，以你当前菜单为准。

一段提示词要反复复制，或者同一项工作每次都要重新说明步骤、输入和验收条件——就可以整理成 **Skill**。Skill 是可复用工作流的作者格式；需要给别人安装、或和连接器一起带走时，再打成 **插件（plugin）**。

这篇按一条主线走完：

1. 用 `$skill-creator` **或** 手写最小 `SKILL.md` 做出第一个 Skill  
2. 测显式调用和自动触发  
3. 不删文件地禁用  
4. 需要对外分发时，按官方方式打成插件  

示例只读写文件，不接外部付费服务。Record & Replay（用演示生成 Skill）另有专文，这里只点到入口。

## 1. Skill 适合保存什么

Skill 适合 **边界清楚、会重复出现、结果能检查** 的工作。例如按团队格式写发布说明、检查发布文件、生成固定结构的项目目录，或把一套人工检查步骤交给 Codex 执行。

一次性临时任务通常不需要 Skill。流程还在天天改时，也可以先把提示词跑顺，确认输入、输出和失败条件，再整理——写出来的说明更短，触发范围也更准。

官方建议：一个 Skill 聚焦一件事；能用说明解决的，先不要上脚本；步骤写成祈使句，并写清输入和输出。

## 2. 一个 Skill 目录里有什么

最小形态：一个目录 + 其中的 `SKILL.md`。YAML 元数据必须有 `name` 和 `description`，后面是选中后才加载的操作说明。

```text
my-skill/
└── SKILL.md
```

复杂工作再按需加目录（没有用途就不要提前建空壳）：

```text
my-skill/
├── SKILL.md
├── scripts/          # 可选：需要稳定执行的程序
├── references/       # 可选：较长规范与资料（按需再读）
├── assets/           # 可选：模板等资源
└── agents/
    └── openai.yaml   # 可选：桌面端展示、调用策略、工具依赖
```

可选的 `agents/openai.yaml` 可配置展示名、图标，以及：

- `policy.allow_implicit_invocation`（默认 `true`）：设为 `false` 时，**不会**按用户自然语言隐式选用该 Skill；`$skill-name` 这类显式调用仍然可用。  
- `dependencies.tools`：声明 MCP 等工具依赖。

## 3. 放在哪里：个人、仓库还是系统

Codex 会从仓库、用户、管理员和系统位置加载本地 Skill。对仓库，会从 **当前工作目录一直扫到仓库根** 的每一层 `.agents/skills`。同名 Skill **不会合并**，选择器里可能同时出现多条。

| 范围 | 位置（概念） | 更适合 |
| --- | --- | --- |
| REPO | 从 `$CWD` 到 `$REPO_ROOT` 各层的 `.agents/skills` | 跟模块／仓库一起审查、共享 |
| USER | `$HOME/.agents/skills` | 个人跨仓库复用 |
| ADMIN | `/etc/codex/skills` | 机器／容器级默认 |
| SYSTEM | Codex 内置 | 如 skill-creator、plan 等 |

日常写自己的：个人用 `~/.agents/skills/my-skill/`，团队用仓库里的 `.agents/skills/my-skill/`。Windows 上用户目录随安装方式变化——以 `/skills` 列表里显示的真实路径为准，不要照抄别人的绝对路径。支持符号链接，扫描时会跟随目标。

这些位置是 **作者创作与本地发现**。跨仓库、给别人安装、或和连接器一起分发，官方指向 **插件**，而不是只靠拷贝文件夹。

## 4. 两条创建路径：`$skill-creator` 或手写

### 4.1 用内置 creator（推荐「先说清楚再生成」）

在 Codex CLI／IDE／桌面 Codex 里：

```text
$skill-creator
```

在 ChatGPT Work 里对应入口是 `@skill-creator`。Creator 会问：这个 Skill 做什么、何时该触发、只要说明还是也要脚本。**默认是 instruction-only（纯说明）**。

工作流已经跑顺、更好「演示一遍」时，官方还提供 Record & Replay：录制步骤后起草可复用 Skill。那条线不在本文展开。

### 4.2 手写最小可用 Skill

下面做一个 `release-note`：只根据 **已确认** 的改动写中文发布说明，并禁止编造测试结果。

个人目录示例：

```text
$HOME/.agents/skills/release-note/SKILL.md
```

或项目目录：

```text
.agents/skills/release-note/SKILL.md
```

`SKILL.md` 内容：

```md
---
name: release-note
description: 根据已经确认的代码改动和验证结果生成中文发布说明。用户要求写发布说明、版本说明或 changelog 摘要时使用；缺少真实改动或验证证据时不要猜测。
---

# 发布说明

1. 读取用户提供的改动摘要、提交或 diff。
2. 区分新增、修复和已知限制，只保留有证据的内容。
3. 用简短中文说明用户能感知的变化。
4. 保留版本号、命令、文件名和链接的原始写法。
5. 没有执行过的测试标记为未验证，不得写成已经通过。

输出一段发布摘要和一份变更列表。
```

**`description` 决定隐式匹配能不能选中它。** 要同时写清用途、触发场景和边界。只写「帮助处理发布工作」太宽，容易误触发；把所有例外塞进描述又会让入口过长。详细步骤放正文。关键用例和触发词尽量靠前写——技能很多时，Codex 可能先 **缩短描述**，再必要时从初始列表里省略部分技能并给出警告。

Codex 通常会自动发现变更；列表里看不到时，**重启 Codex** 再查一次。

## 5. 渐进式加载：为什么描述要短而准

ChatGPT／Codex **不会**一上来把所有 Skill 全文塞进上下文。它们先看到名称和描述（Codex 还会带上文件路径），决定使用某个 Skill 后，才读取完整 `SKILL.md`。`references/`、脚本等也只在流程需要时再加载。

在 Codex 里，这份初始技能列表默认最多约占模型上下文窗口的 **2%**；上下文未知时约 **8000 字符**。可用 `skills.max_context_tokens` 调整，上限 **10000 tokens**。该预算 **只约束初始列表**；一旦选中某个 Skill，仍会读它的完整 `SKILL.md`。

因此：主文件保留执行流程和关键边界；大段背景放进 `references/`，并在正文里写清「何时读哪份」；只有需要确定性结果或外部工具时才加 `scripts/`。脚本会在工作环境里跑——涉及删除、网络、凭据或外部计费时，保留明确的审批与失败处理。

## 6. 测试显式调用

激活方式官方写了两种：

1. **显式**：在提示里直接带上 Skill。ChatGPT 里用 `@` 选；Codex CLI／IDE 里用 `/skills`，或输入 `$` 提及。  
2. **隐式**：任务与 `description` 匹配时，由模型选用。

第一次验证用显式更稳：

```text
使用 $release-note，根据当前分支相对 main 的提交写一份发布说明。先读取 diff 和测试结果，不要修改文件。
```

重点看三件事：

1. 是否读取了正确的 `SKILL.md`  
2. 输出是否守住输入与验证边界  
3. 有没有做任务之外的动作  

找不到时：查目录层级、文件名是否正好是 `SKILL.md`、YAML 是否合法，再确认当前入口支持 **Standalone Skill**（桌面 App、CLI、IDE）。插件里的 Skill 还会出现在 Chat／Work 等更广的表面——和「只放在 `.agents/skills`」不是同一分发路径。

## 7. 测试自动触发（以及不该触发）

显式通过后，再用自然语言测 `description`：

```text
根据这个分支的改动写一份中文 changelog 摘要，未运行的检查要标出来。
```

再准备一个 **不应该** 命中的任务：

```text
帮我解释 changelog 这个词是什么意思，不要读取项目文件。
```

前者应倾向命中 `release-note`；后者只需普通回答。两边都测，才能发现描述太窄还是太宽。

若只想允许 `$release-note`、不要自然语言误触，可在该 Skill 的 `agents/openai.yaml` 里设 `allow_implicit_invocation: false`（显式 `$` 仍可用）。

## 8. 禁用：先关，不必删

本地 Skill 不想删文件、只想暂时关掉时，在 `~/.codex/config.toml` 写入：

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

把 `path` 换成你机器上真实的 `SKILL.md` 路径（可从 `/skills` 列表核对）。改完后 **重启 Codex**。

这与「关掉某个已安装插件」不同。插件侧常用 `~/.codex/config.toml` 里形如 `[plugins."name@marketplace"]` 的 `enabled = false`；仓库级本地 marketplace 插件还可在项目 `.codex/config.toml` 里按 `plugin-name@marketplace-name` 开关。本文主线是 **本地 Skill 目录** 的禁用；插件开关按插件文档操作即可。

## 9. 打包分发：本地文件夹 vs 插件

| 目标 | 官方路径 |
| --- | --- |
| 本机／本仓库作者创作 | `.agents/skills/...` 或 `~/.agents/skills/...` |
| 安装社区精选到本机试用 | `$skill-installer`（例如 `$skill-installer linear`）；也可提示从其他仓库下载。发现不了就重启 Codex |
| 给别人安装、捆绑多个 Skill、或带上连接器 | **插件**：`plugin.json` + `skills/`（可选 `mcp.json`、资源等），再经 marketplace／插件目录安装 |

最小可移植插件骨架（官方「先打一个只含 Skill 的包」示例）：

```text
my-first-plugin/
├── plugin.json
└── skills/
    └── hello/
        └── SKILL.md
```

`plugin.json` 使用 Agent Plugins schema，并给出稳定的 kebab-case `name`。技能放在根下 `skills/<skill-name>/SKILL.md`。随后把插件登记进仓库或个人 marketplace（例如 `$REPO_ROOT/.agents/plugins/marketplace.json` 或 `~/.agents/plugins/marketplace.json`），用桌面端插件目录安装验证。也可用 `@plugin-creator`／`$plugin-creator` 脚手架（兼容布局可能含 `.codex-plugin/plugin.json`）。

**我的用法：** 自己先在 `.agents/skills` 里把触发测稳，再拷进插件的 `skills/` 打包；不要一上来就为「也许要分享」建空插件。公开上架、工作区发布、MCP 鉴权等按《Package your plugin》走，本文不展开门户提交流程。

## 10. 什么时候再加脚本和参考资料

纯说明能完成时，先保持纯说明。再考虑脚本的情况：

- 同一条命令必须稳定执行，参数和输出格式清楚  
- 人工复制步骤容易出错，脚本可先做只读检查或 dry run  
- 验证需要解析结构化结果，靠文字判断不够可靠  

参考资料适合字段定义、团队规范和长示例。`SKILL.md` 应写明何时读哪一份，避免一次加载整个 `references/`。

## 11. 发布前检查清单

- `SKILL.md` 含有效的 `name` 和 `description`；描述靠前写清触发词与边界  
- 名称与目录用途一致；步骤有明确输入、动作、输出  
- 没有把 Token、账号、本机绝对路径写进要共享的 Skill  
- 写入／删除／网络／付费操作保留审批与失败处理  
- 测过：显式调用、应自动触发、不应触发  
- 需要时测过：`enabled = false` 禁用后不再出现／不再隐式选用  
- 对外分发走插件 + marketplace，而不是口头约定「解压到某个路径」  
- 项目 Skill／插件里的脚本与引用已纳入 Git 审查  

## 参考资料

- [Build skills](https://developers.openai.com/codex/skills)（[learn 镜像](https://learn.chatgpt.com/docs/build-skills)）  
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)  
- [Plugins（Codex）](https://developers.openai.com/codex/plugins)  
- Agent skills 规范与 openai/skills 示例见官方 Build skills 文末链接  

本文按 2026-10-22 可访问的官方 Skill／插件文档核对。Standalone Skill 与插件 Skill 的可用入口不完全相同；以你当前客户端为准。
