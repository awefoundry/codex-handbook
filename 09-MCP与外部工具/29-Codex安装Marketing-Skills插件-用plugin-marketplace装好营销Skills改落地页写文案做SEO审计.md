---
id: codex-marketing-skills
title: "Codex 安装 Marketing Skills 插件：用 codex plugin marketplace add 装好营销 Skills，改落地页、写文案和做 SEO 审计"
seo_title: "Codex 安装 Marketing Skills：marketplace add 与 53 个 Skill"
description: "Marketing Skills 是 Corey Haines 维护的 MIT 开源技能集，不是 OpenAI 官方插件。本文用 Codex CLI 0.172.0 装上 marketing-skills 2.14.28，列出 53 个 Skill，并说明升级、卸载和第三方风险。"
lede: "先看它是谁维护的、会写进哪些目录，再决定要不要让 Codex 按里面的营销流程改页面。装上不等于已经审过你的落地页。"
url: /guides/codex-marketing-skills
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI]
difficulty: 进阶
order: 29
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-24
date_modified: 2026-11-24
verified_on: 2026-11-24
tested_cli_version: 0.172.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex Marketing Skills, marketingskills, codex plugin marketplace add, Codex SEO Skill, Codex 文案 Skill]
related: [plugin-development-marketplace, create-codex-skill, codex-skillspector-skill-security-scan]
howto: true
faq:
  - q: "这是 OpenAI 的官方插件吗？"
    a: "不是。仓库 coreyhaines31/marketingskills 由 Corey Haines 维护，许可证是 MIT。Codex 只是 README 写明可以安装的对象之一。"
  - q: "会话里的 /plugins 和命令行的 plugin add 是一回事吗？"
    a: "README 写的是先 codex plugin marketplace add，再在会话里输入 /plugins 并选择 marketing-skills。0.172.0 的命令行还有 codex plugin add marketing-skills@marketingskills。本文用的是后一条，没有打开交互式 TUI，没有按过 /plugins。"
  - q: "装上之后 Codex 会自动改落地页吗？"
    a: "本文没有登录，也没有把落地页、文案或 SEO 任务发给模型。prompt-input 能列出 53 个带 marketing-skills 前缀的名字，只说明这份安装被放进了技能列表。会不会改文件，要等你自己的会话，并受当前审批和沙箱约束。"
  - q: "安装前要做什么安全检查？"
    a: "这些 SKILL.md 是写给代理执行的说明。装进会改文件的项目之前，先用 SkillSpector 一文里的扫描看提示注入和数据外泄。本文读了 frontmatter，没有按技能正文去改页面、跑脚本或连接第三方账号。"
---

# Codex 安装 Marketing Skills 插件：用 codex plugin marketplace add 装好营销 Skills，改落地页、写文案和做 SEO 审计

> 核对依据：第三方仓库 [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) 的 README、[MIT 许可证](https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE) 和 `.agents/plugins/marketplace.json`。2026-11-24 通过 GitHub API 查询：62,262 star，9,099 fork，许可证 MIT，`pushed_at` 为 `2026-11-23T21:01:10Z`。默认分支最新提交 `8fd2fcade2fd6629026e9dfe6d133b55b36968b9` 的提交时间是 `2026-11-23T21:00:55Z`，说明为 `Methods: outlier scoring, comment sorting, podcasts as a lead source (2.14.28)`。Codex CLI 为 `@openai/codex@0.172.0`，`codex --version` 输出 `codex-cli 0.172.0`。插件命令和 `codex debug prompt-input` 都在未登录的独立 `CODEX_HOME` 里运行。没有打开交互式会话，没有改落地页，没有配图。

这是 **Corey Haines** 维护的营销技能仓库，不是 OpenAI 的内置营销功能。README 把它写成一组给编码代理用的 Skill，适用于 Claude Code、OpenAI Codex、Cursor、Windsurf，以及支持 [Agent Skills 规范](https://agentskills.io) 的代理。Codex 会不会在你的会话里按这些文件改页面，取决于它是否读到对应的 `SKILL.md`、描述是否匹配，以及你有没有允许它改文件。

插件怎么打包和分发，见 [Codex 插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。`SKILL.md` 本身怎么写，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

## 先说结论

2026-11-24 在独立 `CODEX_HOME`、未登录的 Linux 上：

1. `codex plugin marketplace add coreyhaines31/marketingskills` 添加了名为 `marketingskills` 的 Git 市场。
2. `codex plugin add marketing-skills@marketingskills` 装上的插件版本是 **2.14.28**。缓存目录 `skills/` 下有 **53** 个技能目录，每个目录一份 `SKILL.md`。
3. `codex debug prompt-input` 列出了这 53 个名字，前缀是 `marketing-skills:`。

README 的 Partners 区块是赞助商和集成推广。本文不把那些产品写成推荐，也不写购买或注册步骤。

没有在已登录的会话里发送 `$cro`、`$copywriting` 或 `$seo-audit`，也没有让它改任何一个页面。

## 装之前

先确认 CLI 认插件子命令。2026-11-24 的 `codex plugin --help` 列出 `add`、`list`、`marketplace`、`remove`。`codex plugin marketplace --help` 列出 `add`、`list`、`upgrade`、`remove`。

官方 [Plugins](https://learn.chatgpt.com/docs/plugins) 写：Codex CLI 里输入 `/plugins` 打开插件浏览器，从已配置的市场安装，然后新开一轮会话再用它带的技能或工具。同一页写 IDE 扩展不支持插件。本文没有打开 IDE。

[Build skills](https://learn.chatgpt.com/docs/build-skills) 写 Codex 从这些位置读本地技能：`$CWD/.agents/skills`、仓库里更上层的 `.agents/skills`、`$REPO_ROOT/.agents/skills`、`$HOME/.agents/skills`、`/etc/codex/skills`，另外还有随 Codex 附带的系统技能。插件是另一条分发路径。同一页写可以用 `[[skills.config]]` 按路径或名字禁用技能；`allow_implicit_invocation` 为 false 时，Codex 不会按用户提示自动选用该技能，显式的 `$技能名` 仍然可用。本文没有改这些键。

这个仓库的 `.agents/plugins/marketplace.json` 写明：市场名 `marketingskills`，插件名 `marketing-skills`，`source` 为本地 `./`，`installation` 为 `AVAILABLE`，`authentication` 为 `ON_INSTALL`。

## 用 marketplace add 添加市场并安装

README 的 Option 3 是：

```bash
codex plugin marketplace add coreyhaines31/marketingskills
```

然后在 Codex 会话里输入 `/plugins`，选择 **marketing-skills**。以后用 `codex plugin marketplace upgrade` 收取新版本。

2026-11-24 在独立 `CODEX_HOME` 里执行了第一条。输出是：

```text
Added marketplace `marketingskills` from https://github.com/coreyhaines31/marketingskills.git.
```

`codex plugin marketplace list` 把根目录记在这次测试的 `$CODEX_HOME/.tmp/marketplaces/marketingskills`。`config.toml` 写下：

```toml
[marketplaces.marketingskills]
source_type = "git"
source = "https://github.com/coreyhaines31/marketingskills.git"
```

此时 `codex plugin list` 里 `marketing-skills@marketingskills` 的状态是 `not installed`。

会话里的 `/plugins` 没有打开。0.172.0 的命令行可以直接装：

```bash
codex plugin add marketing-skills@marketingskills
```

`--json` 的结果是：`pluginId` 为 `marketing-skills@marketingskills`，`version` 为 `2.14.28`，`authPolicy` 为 `ON_INSTALL`，`installedPath` 在 `$CODEX_HOME/plugins/cache/marketingskills/marketing-skills/2.14.28`。这次没有登录，命令也没有出现交互式认证提示。清单里的 `ON_INSTALL` 被原样印了出来。已登录会话会不会再问一次，本文没有看到。

装完后 `config.toml` 多了：

```toml
[plugins."marketing-skills@marketingskills"]
enabled = true
```

`codex plugin list` 的状态变成 `installed, enabled`，版本 `2.14.28`。缓存里的 Git 提交是 `8fd2fcade2fd6629026e9dfe6d133b55b36968b9`，和上面的 API 记录是同一条。

接着执行 `codex plugin marketplace upgrade`，输出是 “Upgraded 1 marketplace(s)”，根目录仍是同一个市场路径。版本号没有因此变成另一版。

## 装完多了哪些 Skills

缓存里的 `skills/` 有 53 个目录，53 份 `SKILL.md`。名字与 README 的 Available Skills 表一致，按目录名排序是：

`ab-testing`、`ad-creative`、`ads`、`ai-seo`、`analytics`、`aso`、`attribution`、`churn-prevention`、`co-marketing`、`cold-email`、`community-marketing`、`competitor-profiling`、`competitors`、`content-strategy`、`conversion-tracking`、`copy-editing`、`copywriting`、`cro`、`customer-research`、`directory-submissions`、`emails`、`events`、`free-tools`、`image`、`influencer-marketing`、`launch`、`lead-magnets`、`link-building`、`marketing-council`、`marketing-ideas`、`marketing-loops`、`marketing-plan`、`marketing-psychology`、`offers`、`onboarding`、`paywalls`、`popups`、`pricing`、`product-marketing`、`programmatic-seo`、`prospecting`、`public-relations`、`referrals`、`reverse-engineer-marketing`、`revops`、`sales-enablement`、`schema`、`seo-audit`、`signup`、`site-architecture`、`sms`、`social`、`video`。

`.codex-plugin/plugin.json` 的 `version` 也是 `2.14.28`，`skills` 指向 `./skills/`，许可证栏写 MIT。这份清单没有 MCP 服务器字段。

下面七个的 `description` 来自装到磁盘的 `SKILL.md` frontmatter，只说明它声称自己在什么时候被用到：

| 名字 | 版本 | 它写明的用途 |
|---|---|---|
| `product-marketing` | 2.2.3 | 建立或更新 `.agents/product-marketing.md`，记下产品、受众、定位和品牌语气。描述写：新项目上其他营销技能之前先用它 |
| `cro` | 2.0.6 | 看落地页、定价页、表单为什么转化不好，以及先改哪一处 |
| `copywriting` | 2.3.6 | 写或改首页、落地页、定价页、功能页的文案 |
| `seo-audit` | 2.2.10 | 做 SEO 诊断，包括索引、标题、规范链接和 Core Web Vitals |
| `schema` | 2.0.5 | 添加、修正或核对 JSON-LD |
| `analytics` | 2.2.7 | 看分析埋点、事件命名，以及 GA4、GTM、Mixpanel、PostHog |
| `pricing` | 2.1.7 | 讨论定价、套餐和定价页 |

`analytics` 的描述点了第三方分析产品。`ads`、`image`、`ad-creative` 的文件里还有外部工具和 API 密钥的说明。本文没有运行这些文件里的命令，也没有配置任何密钥。

## 在 Codex 里怎么触发

[Build skills](https://learn.chatgpt.com/docs/build-skills) 写了两种启用方式。显式调用：在 Codex CLI 或 IDE 扩展里运行 `/skills`，或输入 `$` 点名技能。隐式调用：任务和技能的 `description` 对上时，Codex 可以自己选用。IDE 扩展不支持插件，所以这条插件安装只覆盖 CLI，以及官方插件页写明可以使用插件的 ChatGPT 桌面应用。本文没有打开桌面应用。

2026-11-24 的 `codex debug prompt-input` 在技能列表里看到了 `marketing-skills:cro`、`marketing-skills:copywriting`、`marketing-skills:seo-audit` 和 `marketing-skills:product-marketing`，一共 53 个带这个前缀的名字。同时还能看到系统技能 `skill-creator`。这次输出把技能目录放在测试用的 `CODEX_HOME` 下面，正文不写那台机器的用户目录。

`product-marketing` 的描述写：新项目上，其他营销技能会先读产品营销上下文。若要先准备那份文档，可以在**你自己的**已登录会话里发送：

```text
请使用 $product-marketing。只在当前项目创建或更新 .agents/product-marketing.md。
材料只有我贴在下面的产品说明。缺的项写成「待补充」，不要搜索网页，不要改其他文件。
```

这是提示词示例，不是本文跑过的会话。下面三个例子同样没有发送。

## 三个可以自己发的例子

例子都假设你已经在要改的项目里打开了 Codex，并且允许它按当前审批规则改文件。范围写进提示里。Codex 的回复以你这次会话为准。

**审一页落地页。** 把页面文件放在当前项目里，发送：

```text
请使用 $cro。只阅读我指定的这一个页面文件，列出你认为会先影响转化的问题。
不要改文件，不要安装依赖，不要打开外部账号。
```

**重写首页文案。** 先有上一节那份产品说明，再发送：

```text
请使用 $copywriting。只改我指定的首页文案段落。
每个判断都要能在我提供的材料里找到依据。不要新增页面，不要改样式文件。
```

**做一次 SEO 审计。** 发送：

```text
请使用 $seo-audit。只根据当前仓库里的页面文件做审计，按问题列出文件和位置。
不要改文件，不要请求 Search Console 或其他需要登录的服务。
```

`schema` 和 `analytics` 会碰到结构化数据和第三方统计。没有账号、也不打算接账号时，不要让会话去配置 GA4、GTM 或广告平台。

## 升级、停用与卸载

升级市场快照用 README 里的命令：

```bash
codex plugin marketplace upgrade
```

2026-11-24 执行后，市场仍是 `marketingskills`，插件列表里的版本仍是 2.14.28。

停用而不删除市场时，官方 Build skills 的办法是在 `config.toml` 里加 `[[skills.config]]`，用 `path` 或 `name` 把 `enabled` 设为 false。本文没有写这条，所以没有验证禁用后 `prompt-input` 是否还列出它们。

卸载插件，0.172.0 的帮助是：

```bash
codex plugin remove marketing-skills@marketingskills
```

2026-11-24 在同一个 `CODEX_HOME` 里执行了这条。输出是 `Removed plugin marketing-skills from marketplace marketingskills`。随后 `plugin list` 回到 `not installed`，`config.toml` 里的 `[plugins."marketing-skills@marketingskills"]` 消失，市场来源还在。缓存里的 `2.14.28` 目录也不在了。

市场来源本身用 `codex plugin marketplace remove`。帮助里有这个子命令。本文没有执行它，所以市场那一节配置还留在测试用的 `CODEX_HOME` 里。这个目录是临时的，不是读者的家目录。

## 安全

这些文件是写给代理的操作说明。仓库里没有搜到 “ignore previous instructions” 这类句子。这只说明这次克隆里没有这句英文，不说明每份技能都适合直接装进客户仓库。

装进真实项目之前，先看 [用 SkillSpector 扫描第三方 Skill](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。扫描看的是提示注入和数据外泄，不能代替你自己读即将改文件的那一份 `SKILL.md`。

这次安装观察到的边界：

- 插件清单只有技能目录，没有在 `plugin.json` 里声明 MCP 服务器。
- README 另有一份工具连接说明和 Partners 名单。那是可选的外部账号和赞助集成。不连接它们，上面的安装命令仍然能完成。
- `authentication: ON_INSTALL` 写在市场清单里。这次未登录安装没有弹出认证。不要据此认为以后每次安装都不会要账号。
- 部分技能的参考文件讨论分析、广告和图像工具的密钥。密钥留在你自己的环境里，不要贴进会话，也不要写进仓库。

官方插件页写：插件若带 hooks，要在信任之后才会按生命周期运行。这份 2.14.28 缓存里没有找到 `hooks.json`。以后升级若带上 hooks，先看 SkillSpector 和官方 [Hooks](https://learn.chatgpt.com/docs/hooks) 页，再决定是否信任。

## 参考资料

- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)（第三方，MIT）
- [LICENSE](https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE)
- 仓库内 `.agents/plugins/marketplace.json`
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- 同库：[Codex 插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)、[从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)、[SkillSpector](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)

资料核对日期：2026-11-24（Asia/Shanghai）。star 数、fork、提交和许可证来自当天的 GitHub API。安装、列表、`prompt-input`、升级和卸载来自 Linux 上未登录的 `codex-cli 0.172.0`。没有打开 `/plugins`，没有配图。
