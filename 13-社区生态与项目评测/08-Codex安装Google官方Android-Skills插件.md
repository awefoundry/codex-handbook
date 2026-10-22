---
id: android-skills-plugin
title: Codex 安装 Google 官方 Android Skills 插件：用 codex plugin marketplace 装好 33 个安卓开发技能，再用 AGP 9 升级做一次实测
seo_title: Codex 安装 Google Android Skills：marketplace 与 AGP 9 工作流
description: Google 官方 android/skills 可作为 Codex 插件安装：先 marketplace add，再装 android-skills。本文按官方 README 与 Plugins 文档写清安装、核对技能清单（本稿核对时为 33 个），以及按上游 agp-9-upgrade 技能说明走 AGP 9 升级工作流；本环境无 Android 工程，未伪造实测输出。
lede: 把 Google 维护的 Android Skills 一次装进 Codex，再按官方技能说明驱动 AGP 9 升级，而不是凭记忆硬改 Gradle。
url: /guides/codex-android-skills-plugin
status: draft
section: guides
category: I-ecosystem
topic: 社区生态与编辑器接入
content_type: 教程
source_tag: 社区生态
entry_tags: [App, CLI, Skills]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
client_validation_pending: true
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://github.com/android/skills
keywords: [Codex Android Skills, android/skills, codex plugin marketplace, AGP 9, agp-9-upgrade, Jetpack Compose]
related: [plugin-development-marketplace, create-codex-skill]
howto: true
faq:
  - q: 为什么选题写「约 30 个」，正文却写 33 个？
    a: 2026-10-19 选题笔记按当时清单写约 30。本文按 2026-10-22 抓取的 android/skills 主分支 `.codex-plugin/plugin.json`（version 1.0.16）skills 数组与仓库内 SKILL.md 数量核对，均为 33。技能数会随上游更新变化，安装后以你本机插件包为准。
  - q: 装插件和用 Android CLI 的 android skills add 有什么区别？
    a: Codex 插件路径把整包 Android Skills 作为 marketplace 插件一次装进 Codex。Android CLI 的 `android skills add`／`--all` 把技能装到本机检测到的各 agent 目录（可指定 `--agent=codex`），更适合按技能或按项目粒度安装。两条路径官方 README 都写了。
  - q: 可以拿 agp-9-upgrade 去迁 Kotlin Multiplatform 项目吗？
    a: 不可以。上游 `agp-9-upgrade` 的 description 与 Requirements 明确写：Do not use this skill for migrating Kotlin Multiplatform (KMP) projects。
---

# Codex 安装 Google 官方 Android Skills 插件：用 codex plugin marketplace 装好 33 个安卓开发技能，再用 AGP 9 升级做一次实测

> 本文计划路径：[codexguide.io/guides/codex-android-skills-plugin](https://codexguide.io/guides/codex-android-skills-plugin)

> 核对依据：Google《[android/skills](https://github.com/android/skills)》README 与 `.codex-plugin/plugin.json`、Android Developers《[Overview of Android skills](https://developer.android.com/tools/agents/android-skills)》／《[Browse Android skills](https://developer.android.com/tools/agents/android-skills/browse)》、OpenAI《[Plugins](https://developers.openai.com/codex/plugins)》与 CLI《[Developer commands](https://developers.openai.com/codex/cli/slash-commands)》中的 `codex plugin`／`codex plugin marketplace`，以及上游 `build-system/agp/agp-9-upgrade/SKILL.md`。文中「我的用法」是操作顺序建议。本预览环境无 Android 工程、未登录本机 Codex 实装插件，故不写假终端输出与假截图；`client_validation_pending: true`。

安卓工程里，AGP 升级、edge-to-edge、R8 keep 规则、Navigation 3 这类题，模型「会写 Kotlin」不等于「按 developer.android.com 当前最佳实践走完」。Google 把评测里模型容易翻车的工作流，收成一套遵循 [Agent Skills](https://agentskills.io/home) 开放标准的 `SKILL.md`，仓库是 **[android/skills](https://github.com/android/skills)**，并提供 **Codex 插件**安装方式。

这篇按一条主线：

1. Android Skills 是什么、和自己写 Skill／打包插件的关系  
2. 用 `codex plugin marketplace` 装上官方插件  
3. 怎么列出、核对、触发技能  
4. 按上游 **agp-9-upgrade** 说明，把 AGP 9 升级当成可复查的工作流（不是编造某次构建绿了）  
5. 和 Android CLI 单装技能怎么选  

自己写 Skill、用 `$plugin-creator` 打团队包，见姊妹篇《从零创建 Codex Skill》《Codex 插件开发入门》。

## 1. Android Skills 是什么

按仓库 README 与 Android Developers Overview：

- **内容**：面向 AI agent 的、模块化的 Android 开发指令与配套资源，用来 grounding 模型，让它更贴近 developer.android.com 的模式与流程。  
- **形态**：开放标准 Agent Skills——每个技能一个目录，核心是 `SKILL.md`（可带 `scripts/`、`references/`、`assets/`）。  
- **取舍**：优先覆盖「评测显示大模型表现不好」的用例；不重复模型已经较熟练的基础 Jetpack Compose 写法。  
- **许可**：Apache-2.0；目前 **不接受外部代码贡献**（反馈与请求走 GitHub issue）。  
- **免责**：README 写明 AI 可能出错，结果要人工复核。

官方文档入口：[Android skills](https://developer.android.com/tools/agents/android-skills)、[Android CLI](https://developer.android.com/tools/agents/android-cli)、以及 Studio 侧的 Gemini skills 说明。Browse 页展示了已上线技能的一部分（AGP 9、edge-to-edge、Compose 迁移、R8、Play Billing 等），完整列表以 GitHub 仓库为准。

### 1.1 本稿核对时的技能数量

选题曾写「约 30 个」。**以主键源为准**：2026-10-22 抓取的 `android/skills` 主分支

- `.codex-plugin/plugin.json`：`name` 为 `android-skills`，`version` 为 **1.0.16**，`skills` 数组长度为 **33**  
- 仓库内 `**/SKILL.md` 同样是 **33** 份  

两者一致。数量会随上游发版变化；你安装后请用下一节的核对步骤看本机包，不要死记本文数字。

按顶层目录粗分（路径来自 `plugin.json` 的 `skills` 列表）：

| 分组 | 数量 | 示例技能目录名 |
| --- | --- | --- |
| build-system | 1 | agp-9-upgrade |
| camera / cars / media / profilers / testing / tv / devtools | 各 1 | camerax、android-cli、testing-setup… |
| device-ai | 4 | appfunctions、litert-lm、litert-runtime、ml-kit-genai-prompt-api |
| identity / navigation / performance / security / system / wear / xr | 各 2 | restore-credentials、navigation-3、r8-analyzer、edge-to-edge… |
| jetpack-compose | 4 | adaptive、migrate-xml-views-to-jetpack-compose、styles… |
| play | 3 | engage-sdk-integration、play-billing-library-version-upgrade、play-policy-insights |

插件展示名在 `interface.displayName` 为 **Android Skills**；作者字段为 Google / Android；默认示例提示包含 “Help me upgrade my app to AGP 9.” 与 CameraX 迁移一类句子。

## 2. 在 Codex 里安装：marketplace → 插件

### 2.1 官方推荐的 Codex 命令

`android/skills` README 的 **Install as an agent plugin · Codex** 写的是：

```bash
codex plugin marketplace add android/skills
codex plugin add android-skills@android-skills
```

含义拆开：

1. **`codex plugin marketplace add android/skills`**  
   把 GitHub 简写 `owner/repo` 登记为可浏览的 marketplace 源。OpenAI Developer commands 说明：`marketplace add` 接受 `owner/repo`、`owner/repo@ref`、HTTPS／SSH Git URL、或本地 marketplace 根目录；可用 `--ref` 钉分支／标签，Git 源可重复 `--sparse PATH`。  
2. **`codex plugin add android-skills@android-skills`**  
   从已配置的 marketplace 安装名为 `android-skills` 的插件（`插件名@marketplace名`）。同一页文档里，`codex plugin add`／`list`／`remove` 负责安装、列举、卸载；`--json` 便于脚本。

仓库里还有 `.agents/plugins/marketplace.json`：marketplace 名与插件名都是 `android-skills`，`source` 指向 `https://github.com/android/skills` 的 `main`，`policy.installation` 为 `AVAILABLE`。这与 README 命令一致。

### 2.2 CLI 插件浏览器（另一种装法）

按 OpenAI《Plugins》：

1. 启动 Codex CLI，输入 `/plugins`  
2. 按 **marketplace 页签**切换源，打开插件详情  
3. 选择 **Install plugin**  
4. **新开一个会话** 再使用捆绑的 skills／工具  

桌面端 ChatGPT／Codex 则从 Plugins 目录浏览；**IDE 扩展不支持插件**——要装 Android Skills 这类插件，用桌面端或 CLI。装完后 bundled skills 在 **新开对话／新 CLI session** 后才可用。

**我的用法：** 先跑 README 两行命令把源和插件装上，再用 `codex plugin list`（可加 `--json`）确认 `android-skills` 已安装且 enabled；需要图形浏览时再开 `/plugins`。

### 2.3 装完后建议立刻做的核对

本环境未实跑，下列是**应执行的检查清单**，不是编造的终端抄本：

1. `codex plugin marketplace list` —— 能看到 `android-skills`（或你配置时的名称）及解析到的根路径。  
2. `codex plugin list` —— `android-skills` 出现在已安装列表；需要时加 `--json` 看 `version`／`installedPath`。  
3. **新开** Codex 会话后，用自然语言提一个与技能强相关的任务（README 示例："Make my app UI edge-to-edge."），观察 agent 是否加载对应 skill。  
4. 需要点名时：在支持的表面用 `@`（ChatGPT）或 `$`／`/skills`（Codex CLI／IDE 对 Standalone Skill 的习惯）指向具体技能；插件内技能的精确唤起 UI 以你当前客户端为准。  
5. 升级 marketplace：`codex plugin marketplace upgrade`（或带 marketplace 名），再视需要重装／更新插件，使本地包跟上上游。

若只想给**某一个 Android 仓库**装少量技能、或同时喂给 Gemini／Claude 等，用下一节的 Android CLI，不必强行走整包插件。

## 3. 备选：Android CLI 按技能／按 agent 安装

Android Developers 与仓库 README 推荐用 **Android CLI** 管理技能：

```bash
# 列出可用／已装
android skills list

# 装单个技能到当前项目
android skills add r8-analyzer --project=.

# 装全部官方技能（检测到的各 agent）
android skills add --all

# 只装给 Codex
android skills add --all --agent=codex

# 更新
android skills update --all
android skills update wear-compose-m3
```

要点（官方 skills_add 页）：

- 省略 `--agent` 时，装到本机**已检测到**的全部 agent；若没有任何 agent 目录且未指定 agent，默认落到 Gemini／Antigravity 的 `~/.gemini/antigravity/skills`。  
- 已安装则 `add` 会更新到最新。  
- **若你改过已装技能**，应先改名目录，否则下次 `add`／`update` 会覆盖你的改动。

| 场景 | 更合适的路径 |
| --- | --- |
| 主要在 Codex App／CLI 里做安卓，希望一次拿齐官方包 | `codex plugin marketplace add` + `codex plugin add` |
| 只要一两个技能、或要同时给多个 agent／按项目目录安装 | `android skills add …` |
| 自己写可分发 Skill／团队插件 | 见《从零创建 Codex Skill》《插件开发入门》，不要改官方目录冒充上游 |

## 4. 怎么调用这些技能

官方激活说明（README 与 Overview 一致）：

> 你的 agent 会**自动**激活与任务相关的技能。直接描述相关任务即可，例如 “Make my app UI edge-to-edge.”；若已安装，agent 应自行找到并使用该技能。

补充：

- Android Studio 里还可以在对话中用 `@skill-name` 手动点名（Overview）。  
- Codex／ChatGPT 插件场景：Plugins 文档建议「直接描述目标」或用 `@` 点名插件／捆绑 skill。  
- **不要假设**模型会静默改你的 `gradle.properties` 而不经审批——Codex 仍受你的 sandbox／approval 策略约束；技能只是加长、加准的说明书。

**我的用法：** 任务描述里带上版本与约束（「升级到 AGP 9，非 KMP，先对照 Compatibility 表」），比只说「帮我升一下 Gradle」更容易命中 `agp-9-upgrade` 而不是泛泛改版本号。

## 5. AGP 9 升级：按上游技能走工作流（非本机实测成绩单）

本节**只复述**上游 `build-system/agp/agp-9-upgrade/SKILL.md`（metadata `last-updated: 2026-09-18`，author Google LLC）里的要求与步骤，并说明你在真实工程里应如何配合 Codex 使用。本 box **没有** Android 工程，因此：

- 不贴「某次 `./gradlew build` 已通过」的假日志  
- 不放假 Android Studio 截图  
- frontmatter 已标 `client_validation_pending: true`

### 5.1 技能边界（先读 description）

- 用途：将 Android 工程升级／迁移到 **Android Gradle Plugin 9**。  
- **禁止**：用于 Kotlin Multiplatform（KMP）迁移——description 与 Requirements 均写明 Do not use this skill for KMP。  
- 详细破坏性变更：技能指向 AGP 9 migration guide／release notes（技能包内 `references/`）。

### 5.2 Requirements（升级助理优先）

若用户要求升到 AGP 9，技能要求 agent **先查**工程当前 AGP 版本：

- 若 **低于 9**：先停下，请用户在 Android Studio 用 **AGP Upgrade Assistant** 升到最新稳定 AGP，并确认完成后再继续。  
- 用户若明确要求**跳过**该前置：则在 AGP 9 迁移过程中把 AGP 升到最新稳定版（仍须对照官方 Compatibility：Gradle／JDK／Kotlin 最低版本以对应 release notes 表为准）。

### 5.3 Steps（仅当 AGP 已 ≥ 9）

技能正文步骤摘要：

1. **Update dependencies**  
   - 若用 KSP（`com.google.devtools.ksp`）：确保 **≥ 2.3.6**  
   - 若用 Hilt：确保 **≥ 2.59.2**  
2. **Migrate to built-in Kotlin** —— 按技能引用的官方 migrate-to-built-in-kotlin 指南。  
3. **Migrate to the new AGP DSL** —— 按 AGP 9 release notes；可参考技能包内 `gradle-recipes`。  
4. **Migrate kapt to KSP or legacy-kapt** —— 若项目仍用 KSP 或 kapt，按技能内 `ksp-kapt` 参考迁移。  
5. **BuildConfig** —— 模块若有自定义 BuildConfig 字段，按技能内 BuildConfig 说明处理。  
6. **Update gradle.properties** —— 迁移后删除这些标志（若存在）：  
   - `android.builtInKotlin`  
   - `android.newDsl`  
   - `android.uniquePackageNames`  
   - `android.enableAppCompileTimeRClass`  
   并删除 agent 创建的临时文件。

### 5.4 Guidelines 与 Verification（技能原文约束）

Guidelines 强调：

- 不要编写或运行 Python 脚本  
- 仅在万不得已时、且只在 Gradle 依赖缓存中查看外部依赖  
- **不要**在 `gradle.properties` 加入 `android.disallowKotlinSourceSets=false`  
- 验证时不要跑 `clean`（技能写明浪费时间）

Verification（迁移后应确认）：

1. Gradle IDE sync 成功  
2. `./gradlew help` 成功  
3. `./gradlew build --dry-run` 成功  

Troubleshooting：Paparazzi **v2.0.0-alpha04 及更早** 与 AGP 9 有已知问题，见技能包内 `references/paparazzi-gradle-9.md`。

### 5.5 建议你在本机怎么「实测」这条工作流

把技能当检查表，而不是让模型一次性盲改：

```text
请使用已安装的 agp-9-upgrade 技能。
本仓库不是 KMP。
先报告当前 AGP／Gradle／JDK／Kotlin 版本，对照 Compatibility。
若 AGP < 9：只给出 Upgrade Assistant 步骤，等我确认后再改文件。
若已 ≥ 9：按技能 Step 1–6 逐项改，每步列出将改动的文件；
最后按 Verification 跑 sync、./gradlew help、./gradlew build --dry-run，
不要跑 clean，不要添加 android.disallowKotlinSourceSets=false。
```

你本地通过 Verification 三项后，再考虑去掉 `client_validation_pending`、补打码截图进知识库——那是真机验证，不是本文能伪造的部分。

## 6. 安全与预期管理

1. **官方 Disclaimer**：结果要人工看。AGP 9 有大量 breaking change，技能不能替代阅读 release notes。  
2. **权限**：插件安装不绕过 Codex 审批与沙箱；改 Gradle、执行 `./gradlew` 仍按你的策略确认。  
3. **不要改官方技能目录「打补丁」后还指望 update 保留**——CLI 文档写明会覆盖；要定制就复制改名。  
4. **第三方镜像插件**（把单个上游技能拆成独立 marketplace 插件的社区包装）不是本稿安装路径；内容若来自 Google，仍以 `android/skills` 为准。  
5. **Skills 占上下文**：插件一次捆绑数十个技能描述；若感觉列表过重，可用 Android CLI 只装当前任务相关技能，或查阅 Codex Skills 文档中的上下文预算说明（见 Skill 姊妹篇）。

## 7. 和姊妹篇怎么分工

| 你想做的事 | 去哪篇 |
| --- | --- |
| 安装 Google 这包 Android Skills，并按 agp-9-upgrade 工作流升级 | **本文** |
| 手写／`$skill-creator` 自己的 Skill | 《从零创建 Codex Skill》（id: `create-codex-skill`） |
| 把多个 Skill／MCP 打成可分发插件与 marketplace | 《Codex 插件开发入门》（id: `plugin-development-marketplace`） |

## 8. 检查清单

- [ ] `codex plugin marketplace add android/skills` 成功，`marketplace list` 可见  
- [ ] `codex plugin add android-skills@android-skills` 成功，`plugin list` 可见且已启用  
- [ ] **新开会话** 后，用 edge-to-edge 或 AGP 9 相关提示验证技能会被选用  
- [ ] 需要细粒度控制时，改用 `android skills add --agent=codex …`  
- [ ] AGP 任务：确认非 KMP；AGP&lt;9 时先走 Upgrade Assistant；≥9 时按 Step 1–6；验证三项；注意 Paparazzi 旧版  
- [ ] 对照本机插件 `version` 与 `skills` 数量，不死记本文的 33  

## 9. 参考链接

- https://github.com/android/skills  
- https://developer.android.com/tools/agents/android-skills  
- https://developer.android.com/tools/agents/android-skills/browse  
- https://developer.android.com/tools/agents/android-cli/commands/skills_add  
- https://developers.openai.com/codex/plugins  
- https://developers.openai.com/codex/cli/slash-commands  
- 上游技能：`build-system/agp/agp-9-upgrade/SKILL.md`（随仓库安装，勿依赖过期第三方镜像文）
