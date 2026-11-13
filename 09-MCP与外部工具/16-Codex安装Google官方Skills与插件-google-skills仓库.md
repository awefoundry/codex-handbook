---
id: codex-google-skills-plugins
title: Codex 安装 Google 官方 Skills 与插件：google/skills 仓库的 BigQuery、Cloud SQL、Firestore 等 17 个插件怎么装
seo_title: Codex 安装 Google 官方 Skills：google/skills 与 17 个插件
description: Google 维护的 google/skills 仓库提供 Google Cloud 与数据库相关的 Agent Skills，并带一个 Codex 可用的插件市场。本文说明 npx skills 与 codex plugin marketplace 两条安装路径、约 190 个技能的计数口径、17 个插件各管什么，以及 gcloud 授权、费用和误操作边界。
lede: 技能用 npx skills 安装，插件用 marketplace。仓库 README 列了 187 个技能，全仓库有 192 个 SKILL.md，正文按约 190 个来记，并写明差在哪。
url: /guides/codex-google-skills-plugins
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 16
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-08
date_modified: 2026-11-08
verified_on: 2026-11-08
tested_cli_version: 0.167.0
official_ref: https://github.com/google/skills
keywords: [Codex Google Skills, google/skills, Codex 插件市场, BigQuery, Cloud SQL, Agent Skills]
related: [android-skills-plugin, codex-google-egm-plugin, codex-chajian-rukou-yu-gongzuoliu, mcp-getting-started]
faq:
  - q: 到底是 187 个、192 个，还是约 190 个？
    a: 2026-11-08 克隆的 main 上，README「Available Skills」里指向 ./skills/ 的链接是 187 条，skills/ 目录下的 SKILL.md 也是 187 个。全仓库一共 192 个 SKILL.md，多出的 5 个在 plugins/cloud/google-cloud-developer/skills/，是插件包里的副本。正文因此写约 190 个，并保留这两个口径。
  - q: 这是 OpenAI 和 Google 的合作功能吗？
    a: 仓库由 Google 维护，许可证是 Apache-2.0。Codex 只是它声明支持的安装对象之一。安装、权限和云资源费用都发生在你自己的 Google Cloud 项目上。
  - q: npx skills add 和 codex plugin marketplace add 各装到哪里？
    a: npx skills 把技能装进 agent 的 skills 目录。marketplace 把这个仓库登记成名为 google-plugins 的插件市场，再按插件安装。2026-11-08 只实测了 marketplace add，以及 google-cloud-developer 这一个插件的安装和卸载。
  - q: 本文查询过 BigQuery 或建过数据库吗？
    a: 没有。写作环境没有 GCP 项目，没有 gcloud 登录，也没有配置 Developer Knowledge API Key。bigquery 插件在 Codex CLI 0.167.0 上安装失败，错误原文写在排障一节。
---

# Codex 安装 Google 官方 Skills 与插件：google/skills 仓库的 BigQuery、Cloud SQL、Firestore 等 17 个插件怎么装

> 本文在线版：[codexguide.io/guides/codex-google-skills-plugins](https://codexguide.io/guides/codex-google-skills-plugins)

> 核对依据：GitHub 仓库 [google/skills](https://github.com/google/skills) 的 README、[marketplace.json](https://github.com/google/skills/blob/main/.agents/plugins/marketplace.json)、`plugins/cloud/google-cloud-developer` 的 README 与 `.codex-plugin/plugin.json`、`.mcp.json`。2026-11-08 克隆 main，提交 `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee`（提交时间 2026-11-07 06:41 -0800）。同一天 GitHub API：23,408 star、1,955 fork，`license` 为 Apache-2.0，`created_at` 2026-03-31T19:02:20Z，`pushed_at` 2026-11-07T14:41:39Z。Codex CLI 为 npm 上的 `@openai/codex@0.167.0`，`codex --version` 输出 `codex-cli 0.167.0`。插件命令在独立的 `CODEX_HOME` 里运行，没有使用日常配置目录。没有 GCP 项目，没有配图。

这个仓库由 Google 维护，给编码代理提供 Google 产品（含 Google Cloud）的 [Agent Skills](https://agentskills.io/home)。它同时带一组插件。Codex 能安装它，是因为仓库 README 写了 Codex 的 marketplace 命令，插件包里也有 `.codex-plugin`。这和 OpenAI 内置功能是两套来源。

它和另外两个容易看混的仓库也不同：

- [android/skills](https://github.com/android/skills) 是 Android 开发技能，见 [Codex 安装 Google 官方 Android Skills 插件](../13-社区生态与项目评测/09-Codex安装Google官方Android-Skills插件.md)。
- EGM 是设计文档插件，见 [Codex 安装 Google EGM 插件](./10-Codex安装Google-EGM插件-设计文档与子代理审稿.md)。

适合已经在用 Codex、并且要在自己的 Google Cloud 项目里查 BigQuery、连 Cloud SQL / Firestore / Spanner，或让代理按 gcloud 的现行帮助来写命令的人。只想学 Codex 插件怎么进目录的人，先看 [Codex 插件入口](../08-插件工作流/04-Codex插件入口与工作流.md)。

## 先看结论

2026-11-08 这个仓库同时提供两样东西。

**技能**：README 用 `npx skills add google/skills` 安装。提示里可以选择一部分技能或全部、目标代理，以及项目级还是全局。数量见下一节，正文记为约 190 个。

**插件**：`.agents/plugins/marketplace.json` 的 `name` 是 `google-plugins`，`displayName` 是 Google Plugins，`plugins` 数组有 17 项。README 给 Codex 的步骤是先 `codex plugin marketplace add google/skills`，再在 `/plugins` 里安装。`google-cloud-developer` 的 README 另外写了 `codex plugin add google-cloud-developer@google-plugins`。

这些插件的描述集中在数据库、BigQuery、Dataproc、存储、Looker 和 Cloud 上手。多数条目的 `policy.authentication` 是 `ON_INSTALL`。装上之后，代理会按技能去调用 `gcloud` 和对应产品的 API。资源建在你的 GCP 项目里，费用也记在那个项目上。

## 约 190 个：三个数怎么对上

同一天、同一次克隆里，三个数不一样：

| 口径 | 数量 | 怎么数的 |
| --- | ---: | --- |
| README「Available Skills」里指向 `./skills/` 的链接 | 187 | 链接去重后仍是 187 |
| `skills/` 目录下的 `SKILL.md` | 187 | `find skills -name SKILL.md` |
| 全仓库 `SKILL.md` | 192 | 含插件目录 |

多出来的 5 个文件都在 `plugins/cloud/google-cloud-developer/skills/`：`google-cloud-recipe-auth`、`google-cloud-recipe-onboarding`、`gcloud`、`retrieving-developer-knowledge`、`finding-google-skills`。`skills/` 里已经有同名技能。这 5 个是插件包自带的副本，所以全仓库文件数比 README 清单多 5。

正文用「约 190 个」概括这个仓库的技能规模。安装之后以你本机目录里的 `SKILL.md` 为准，不要把 187 或 192 当成会固定下来的产品规格。

README 在清单之外还指向别的仓库：Cloud Storage 的扩展技能、Agent Development Kit、Android、Dart、Firestore、Flutter、Maps。那些不在这 187 条链接里，本文不把它们算进 google/skills 的数量。

## 方式一：npx skills add google/skills

README 的安装命令是：

```bash
npx skills add google/skills
```

它写明：提示出现后，选择具体技能或全部技能、要配置的代理，以及安装范围（项目或全局）。没有 `npx` 时，先安装带 npm 的 Node.js。更新用：

```bash
npx skills update
```

README 写这条更新命令可以选择删掉过时技能。

本文没有运行 `npx skills`。没有交互式选择的记录，也没有把约 190 个技能装进写作环境。要跟做时，先只选你确实会用的几个（例如 BigQuery 或 Cloud SQL 的基础技能），不要第一次就装全部。

## 方式二：codex plugin marketplace，再装插件

仓库 README 的 Codex 行是：

```bash
codex plugin marketplace add google/skills
```

然后在 `/plugins` 里安装。插件入口的桌面端目录和 CLI `/plugins` 见 [插件入口一文](../08-插件工作流/04-Codex插件入口与工作流.md)。

`google-cloud-developer/README.md` 把 Codex CLI 写成两条命令：

```bash
codex plugin marketplace add google/skills
codex plugin add google-cloud-developer@google-plugins
```

2026-11-08 在 Codex CLI 0.167.0、独立 `CODEX_HOME`、未登录的环境里跑过这两条。`marketplace add` 的输出是：

```text
Added marketplace `google-plugins` from https://github.com/google/skills.git.
```

`codex plugin marketplace list` 里，这个市场的名字是 `google-plugins`。add 之前 `codex plugin list --json` 的 `available` 是空数组。本文没有打开 `/plugins` 界面，所以不知道交互目录是否会把 17 个都列出来。

接着安装本仓库自带的那个插件：

```text
codex plugin add google-cloud-developer@google-plugins --json
```

返回的 `version` 是 `1.1.17`，`authPolicy` 是 `ON_INSTALL`，`pluginId` 是 `google-cloud-developer@google-plugins`。这个版本与当天 `.codex-plugin/plugin.json` 的 `version` 一致。装好的缓存里有 5 个 `SKILL.md`，就是上一节说的那 5 份副本。`config.toml` 里写下了 marketplace 的 git 来源，以及该插件 `enabled = true`。没有写入 API Key。

核对用的移除命令是：

```text
codex plugin remove google-cloud-developer@google-plugins --json
```

这条也成功了。写作环境里没有保留这个插件。

同一个 CLI 上，`codex plugin add bigquery@google-plugins` 失败，原文是：

```text
Error: plugin.json name `bigquery-data-analytics` does not match marketplace plugin name `bigquery`
```

改用包内名字也不行：`bigquery-data-analytics@google-plugins` 的原文是 `plugin bigquery-data-analytics was not found in marketplace google-plugins`。本文只试了 BigQuery 这一个远程插件，没有把其余 15 个逐个安装。仓库 README 写的浏览入口是 `/plugins`。CLI 直接 `plugin add` 遇到名字不一致时，以当天仓库和你本机 CLI 的报错为准。

## 17 个插件各管什么

下表来自 2026-11-08 的 `marketplace.json`。`ref` 是该文件当时钉住的版本，之后会变。描述按该文件的 `description` 压缩，没有改成「已在本文跑通」。

| 插件 | 分类（文件里的 category） | 当时的 ref | 它声明要做的事 |
| --- | --- | --- | --- |
| `alloydb` | Databases | `0.2.0` | 创建、连接并操作 AlloyDB for PostgreSQL |
| `alloydb-omni` | Databases | `0.2.2` | 创建、连接并操作 AlloyDB Omni |
| `bigquery` | Data Warehousing & Data Lakes | `0.2.5` | BigQuery 数据分析技能 |
| `bigtable` | Databases | `v0.4.0` | 连接、查询 Cloud Bigtable |
| `cloud-sql-mysql` | Databases | `0.2.0` | 连接并操作 Cloud SQL for MySQL |
| `cloud-sql-postgresql` | Databases | `0.4.0` | 创建、连接并操作 Cloud SQL for PostgreSQL |
| `cloud-sql-sqlserver` | Databases | `0.2.0` | 连接 Cloud SQL for SQL Server |
| `data-agent-kit` | Databases | `1.0.0` | 数据工程：流水线、dbt、Spark 与 BigQuery SQL、编排 |
| `dataproc` | Data Processing & ETL | `0.1.0` | Dataproc 技能 |
| `db-context-engineering` | 文件里没有 category，也没有 policy | `v0.7.2`（git 子目录 `plugin`） | 维护自然语言转 SQL 用的上下文；支持 AlloyDB、Cloud SQL MySQL/PostgreSQL、Spanner |
| `firestore-native` | Databases | `0.3.4` | 连接并操作 Cloud Firestore |
| `google-cloud-developer` | Cloud Platform | 来源是仓库内路径，不是外部 ref | 上手、认证方式、gcloud 命令校验；带 Developer Knowledge MCP |
| `google-cloud-storage` | Storage | `3.0.1` | Cloud Storage 技能 |
| `knowledge-catalog` | Data Governance & Management | `0.5.4` | Knowledge Catalog |
| `looker` | Business Intelligence & Analytics | `0.3.11` | 连接 Looker |
| `oracledb` | Databases | `0.2.7` | 连接并查询 Oracle 数据库。描述原文写的运行环境是 Gemini CLI |
| `spanner` | Databases | `0.3.6` | 用自然语言连接并操作 Spanner |

除 `db-context-engineering` 外，其余 16 个的 `policy.installation` 都是 `AVAILABLE`，`authentication` 都是 `ON_INSTALL`。`oracledb` 的描述没有写成 Codex 专用，表里保留 Gemini CLI 这句原文。

## gcloud、项目和 IAM

Codex 登录和 Google Cloud 登录是两件事。前者见 [登录 Codex](../01-安装与首次使用/07-登录Codex.md)。后者用的是你机器上的 gcloud 身份、应用默认凭证（ADC）和项目 IAM。

`google-cloud-recipe-auth` 要求先分清四件事：谁在认证（人、本机脚本，还是生产里的应用）、代码跑在哪、要访问哪个 API、用不用客户端库。插件的示例提示里包括新建项目、关联结算，以及为本地开发配置 ADC 和 IAM。本文没有执行这些提示。

`gcloud` 技能把 `gcloud help <叶子命令>` 写成语法的唯一依据，并禁止用网页搜索代替这条帮助。它还要求：带 `--dry-run` 或 `--validate-only` 的命令先预览；删除、更新、移除必须由人明确授权。禁止代理自行执行的操作包括：改 IAM policy、角色或绑定；主动启用 API；主动安装 gcloud；`gcloud * delete`；`gcloud billing *`；组织级变更；`gcloud kms *`；`gcloud infra-manager deployments apply`。这些是技能文件里的限制，不是本文额外加的。

`google-cloud-developer` 的 Codex 安装说明在插件装好之后还有四步，本文都没有做：

1. `gcloud services enable developerknowledge.googleapis.com --project=<YOUR_PROJECT_ID>`
2. 按 [Create and secure the API key](https://developers.google.com/knowledge/quickstart#create-secure-key) 创建 Developer Knowledge API 的密钥。
3. 在 `~/.codex/config.toml` 或项目的 `.codex/config.toml` 里写入该 README 给出的 `mcp_servers.developer-knowledge`，用环境变量名 `DEVELOPERKNOWLEDGE_API_KEY` 提供请求头。
4. 启动 Codex 之前 `export DEVELOPERKNOWLEDGE_API_KEY=...`

`.mcp.json` 里的服务器地址是 `https://developerknowledge.googleapis.com/mcp`。README 写：改完配置后服务器可能显示未登录，这是预期情况，不影响用密钥访问。MCP 的通用配置见 [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。密钥不要写进仓库、截图或聊天记录。

代理真正执行 `gcloud` 时，仍走你在 Codex 里的审批和沙箱。放行范围见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 费用和误操作

marketplace 里多个插件的描述包含「创建」数据库或实例。创建 Cloud SQL、AlloyDB、BigQuery 作业、存储桶或启用 API，都会记到对应 GCP 项目的账单上。本文不写单价。打开 [Google Cloud 定价](https://cloud.google.com/pricing) 和项目账单，以当时的产品页为准。

技能文件已经把结算命令、删除命令和主动启用 API 放进禁止自行执行的列表。让 Codex 做这些事之前，先指定 `--project`，先看 `gcloud help` 里有没有预览开关，再在测试项目里做只读查询。生产项目上的删除和 IAM 变更，由人在终端里确认，不要交给一轮无人值守的对话。

## 怎么验证

在有 GCP 测试项目、并且已经 `gcloud auth` 的机器上：

1. 运行 `codex plugin marketplace add google/skills`，再 `codex plugin marketplace list`，确认有 `google-plugins`。
2. 在 `/plugins` 里安装你要用的那一个，或对名字与 marketplace 一致的插件使用 `codex plugin add <名字>@google-plugins`。
3. 新开一个 Codex 会话。`codex plugin list` 里该项为已安装且启用。
4. 只做一条只读请求，例如让它用 `gcloud help` 解释某个命令，或对测试数据集做一条 `SELECT`。确认项目 ID 是测试项目。
5. 出现创建、删除、改 IAM 或改结算的命令时停下来，自己看完整命令再决定是否执行。

本文完成了第 1 步，以及第 2 步里的 `google-cloud-developer`。第 4 步没有做。BigQuery 的 CLI 安装停在上一节的名字不一致错误。

## 参考资料

- [google/skills](https://github.com/google/skills)
- [marketplace.json](https://github.com/google/skills/blob/main/.agents/plugins/marketplace.json)
- [Google Cloud Developer plugin README](https://github.com/google/skills/blob/main/plugins/cloud/google-cloud-developer/README.md)
- [Apache-2.0](https://github.com/google/skills/blob/main/LICENSE)
- [Agent Skills](https://agentskills.io/home)
- [Create and secure the API key](https://developers.google.com/knowledge/quickstart#create-secure-key)
- [Google Cloud 定价](https://cloud.google.com/pricing)
