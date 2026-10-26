---
id: codex-github-issue-pr-workflow
title: Codex 从 GitHub Issue 到 Pull Request：云任务、@codex review、Security Review 与自动审查一篇讲清
seo_title: Codex GitHub Issue 到 PR：云任务、@codex review、Security Review
description: 从一条可验收的 GitHub Issue 开始，用 Codex Cloud 写代码并开 PR，再用 @codex review、Automatic review、Code Review Rules 与 Security Review（research preview）审查，最后用 @codex fix 修复。合并站内三篇旧教程，对照 2026-10 官方 GitHub 文档。
lede: 云任务把 Issue 推进到可审的 PR；审查与合并仍由人定规矩、拍板。
url: /guides/codex-github-issue-pr-workflow
redirect_from:
  - /guides/codex-github-issue-to-pr
status: published
section: guides
category: G-extensions
topic: 插件与 GitHub 协作
content_type: 指南
source_tag: 官方功能
entry_tags: [App, ChatGPT Work, GitHub]
difficulty: 进阶
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-21
date_modified: 2026-10-22
client_validation_pending: false
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/third-party/github
keywords: [Codex GitHub Issue, Codex Pull Request, @codex review, Codex Security Review, Codex 自动代码审查, Code Review Rules]
related: [permissions-sandbox-approvals, cli-manage-multiple-sessions, create-codex-skill]
faq:
  - q: 在 Issue 评论里写 @codex，和在 PR 里写 @codex review 一样吗？
    a: 不一样。官方 GitHub 文档明确写的是：在 Pull Request 评论里用 @codex review（或 @codex security review）触发审查；评论里若是其他 @codex 指令，会以该 PR 为上下文启动 legacy cloud chat。Issue 阶段更稳妥的做法是在已连接仓库的 Codex Cloud 环境里开云任务，并把 Issue 链接写进任务说明。
  - q: Security Review 和普通 Code Review 有什么差别？
    a: Code Review 看 PR diff，按仓库指引标出严重问题（GitHub 上只报 P0／P1）。Security Review 处于 research preview，专门加深安全风险分析，可手动 @codex security review，也可开 Auto security review；完整报告在关联 Codex 任务的 Security Report 页签。两者偶有重叠。
  - q: Codex 会不会自动把 PR 合并进主分支？
    a: 不会替你做最终合并决定。它可以写代码、开 PR、跑审查与（在有权限时）推修复；CI、分支保护、必需审批和按下合并，仍按仓库规则由维护者负责。
---

# Codex 从 GitHub Issue 到 Pull Request：云任务、@codex review、Security Review 与自动审查一篇讲清

> 本文在线版：[codexguide.io/guides/codex-github-issue-pr-workflow](https://codexguide.io/guides/codex-github-issue-pr-workflow)

> 核对依据：OpenAI《[Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github)》（与 developers.openai.com／codex／integrations／github 同页）、以及《[Codex Cloud](https://learn.chatgpt.com/docs/cloud)》。文中「我的用法」是操作顺序建议，不是官方强制流程。界面文案随产品变化，以你当前 Codex 设置页为准。

从一条写清楚的 GitHub Issue，到一个可以请人审、可以合并的 Pull Request，中间有大量机械活：读上下文、改代码、跑测试、开分支、贴审查意见、按意见返工。Codex 接上仓库之后，这些可以放到 **云端隔离任务** 里异步做；**要不要开 PR、要不要合并，仍由你拍板。**

本文把站内三篇旧稿合成一条主线，并按 2026-10 可访问的官方 GitHub 文档补上：**Automatic review／Review trigger**、**`## Code Review Rules`**、**Security Review（research preview）**、以及 **`@codex fix`／legacy cloud chat**。

合并说明（阅读时可跳过）：

- 主页面 URL 不变：`/guides/codex-github-issue-pr-workflow`（知识库路径仍为 `08-插件工作流/04-…`）。
- 旧文 `/guides/codex-github-issue-to-pr`（原 `05/01`）应 301 到本页；见 frontmatter `redirect_from`。
- 原 `05/04`（无线上 URL）的本地 Git／Draft PR／验收清单要点并入下文「本地路径」；仓库侧归档见 factcheck 待办。

## 1. 先认清它是什么

Codex 跟 GitHub 打通之后，更像能进仓库干活的远程同事：在隔离云环境里改代码、给你摘要和 diff，再按你的确认开 PR；在已启用 Code review 的仓库里，还能在 PR 上做高信号审查。

它 **不是**「评论区许个愿就自动合进 main」。官方流程把「写／审」和「合并」分开：审查规则、分支保护、必需审批和最终合并，仍是维护者的责任。

**我的用法**：先只开 Code review，在下一个真实 PR 里试一次 `@codex review`；觉得 P0／P1 靠谱，再往前接云任务开 PR，往后接 Automatic review 或 Security Review。

## 2. 开始前：仓库、审查开关、环境

### 2.1 连接仓库并准备云环境

1. 能登录 ChatGPT／Codex，并访问目标仓库。  
2. 在 Codex 中连接 GitHub 账号或组织，把要用的仓库接到 **Codex Cloud** 环境。  
3. 按《Codex Cloud》走：选仓库 → 让 Codex 检查依赖与安装 → 缺什么再补 → **Publish** 环境。  
4. 确认初始化步骤能装依赖、跑项目和测试——环境可复现，后面的云任务才靠谱。

配置 Automatic review 时，官方要求：仓库已连接，且配置者对该仓库有 GitHub **push 或 admin** 权限。

旧版集成入口见官方文中的 Codex Cloud（Legacy）；新环境优先按当前 Cloud 页操作。

### 2.2 打开 Code review（审查前提）

`@codex review` **不是** GitHub 自带能力。仓库没在 Codex 里打开 Code review，评论里 @ 它也不会审。

1. 打开 [Codex code review 设置](https://chatgpt.com/codex/settings/code-review)（或 Codex Settings 里对应页）。  
2. 选中目标仓库，打开 Code review／按文档开启 Automatic review 相关选项。  
3. 先用一个小 PR 测手动 `@codex review`。  
4. 流程稳定后，再决定是否打开 Automatic review，以及是否配置 Security Review。

需要仓库级审查规矩时，准备根目录（或更靠近代码的）`AGENTS.md`，见第 6 节。

## 3. 把 Issue 写成可验收的任务

只有一句「加个深色模式」，产品和技术选择都没收口，云任务也只能猜。Issue 至少要让执行者看懂：**现象／目标、范围、限制、怎样算完成**。

可执行结构示例（可直接贴进 Issue）：

```md
## 目标

在设置页增加深色模式开关，并记住用户选择。

## 范围

- 只修改前端主题和设置页。
- 不调整账号接口和数据库。

## 验收

- 开关可以在浅色和深色之间切换。
- 刷新页面后保持上一次选择。
- 现有前端测试通过。

## 限制

- 不新增 UI 组件库。
- 不修改其他页面的布局结构。
```

Bug 类也可以写成更短的验收单：

```text
标题：登录失败后按钮一直处于提交状态

现象：输入错误密码并提交后，登录按钮持续显示加载状态。
复现：打开 /login，输入错误密码，提交表单。
预期：保留输入内容，显示现有错误提示，按钮恢复可点击。
范围：只检查登录表单、请求失败处理和对应测试，不改认证接口。
验收：失败路径测试通过；聚焦测试和 lint 通过；diff 没有无关文件。
```

可继续附：已脱敏的日志／截图、相关文件、基线分支、不能动的约束。公开 Issue **不要**写密钥、生产数据或内部地址。

## 4. 两条执行路径：云端开 PR，或本地建分支

### 4.1 路径 A：Codex Cloud 云任务（异步）

适合：任务边界清楚、环境已 Publish、你不必占着本机编辑器。

1. 在已发布的 Cloud 环境里 **Start a new task**。  
2. 把 Issue 链接、目标分支、完成条件写进任务说明。  
3. 任务在独立工作区跑；可并行多个互不抢本地机器的任务。  
4. 结束后先看改动摘要、diff 和测试结果，再决定是否让它 commit／开 PR。

任务说明示例：

```text
请处理这个 GitHub Issue。

仓库已连接到 Codex cloud。先读取 Issue、仓库 AGENTS.md 和相关测试，说明准备修改的范围。完成后运行现有测试并给出 diff 摘要。不要合并，也不要修改 Issue 范围外的文件。

Issue URL
https://github.com/OWNER/REPO/issues/1287
```

检查结果时至少核对：

- 改动是否仍在 Issue 范围内  
- 依赖、配置、生成文件有无意外变化  
- 测试命令是否真的跑过、退出是否成功  
- 日志／提交里有无凭据或内部地址  

方向不对就在同一任务里给具体反馈，让它改完再验。**摘要看起来合理，也不要跳过 diff。**

改动过关后，再让 Codex 创建 Pull Request，或把分支交给维护者创建。PR 描述建议保留 Issue 链接、改动、验证和剩余风险：

```md
## 改动

- …

## 验证

- …

## 关联 Issue

Closes #1287
```

### 4.2 路径 B：本地分支／Worktree 后再开 Draft PR

适合：要亲手看基线、控制暂存文件，或云环境暂时不好用。命令以仓库已有脚本为准；下面用通用 Git 示意。

开始前确认目录与状态：

```bash
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short --branch
git log -1 --oneline
```

有不明未提交改动时，先分清归属；不要随手 `git reset --hard`／`git clean -fd`。干净后再从目标分支拉最新并开任务分支：

```bash
git switch main
git pull --ff-only origin main
git switch -c fix/login-error
```

需要并行多任务时，可用独立 worktree（分支管历史，worktree 管目录隔离）。**不要**让两个目录同时 checkout 同一条正在用的分支。

**先只读调查，再改代码。** 提示词示例：

```text
请根据当前 Issue 先做只读调查，不要修改文件。

请返回：入口与调用链、失败状态如何清理、已有测试与最小回归范围、计划改／不改的文件、基线与验证命令、已知风险。
若工作区已有不属于本 Issue 的改动，先停下说明，不要暂存、提交、切分支或清理文件。
```

实现时把范围和停止条件写死：只改约定文件、不顺手格式化、不升级依赖；完成后看 `git diff --stat`／完整 diff，跑聚焦测试与 lint，**不要自行提交／推送／合并**，除非你明确要求。

确认改动只属于当前 Issue 后，按文件暂存（避免默认 `git add .`），再推送并开 **Draft PR**，在正式求审前自检 `Files changed`。

## 5. 审查：`@codex review`、Automatic review、Review trigger

前提：该仓库已在 Codex 打开 Code review，且 PR 属于已连接仓库。

### 5.1 手动触发

在 Pull Request 评论里精确写：

```text
@codex review
```

Codex 会先用 👀 回应，再发一份标准 GitHub code review。官方说明：在 GitHub 上这类审查 **只标 P0 和 P1**，减少风格类噪声。

一次性收窄范围可以写在同一条评论：

```text
@codex review for issues in the database migration
```

### 5.2 自动审查

在 Codex 设置里：

1. 仓库侧打开与 Code review／Automatic review 相关的选项。  
2. 在 **Personal preferences** 打开 **Automatic review**。  
3. 用 **Review trigger** 选择何时跑（适用于已启用 code review 的仓库；无需每次手写 `@codex review`）。

自动审查跑完后，意见会出现在 GitHub（以及你使用的 Code Review 界面）。它 **不能** 替代分支保护与人工审批。

## 6. 把规矩写进 `AGENTS.md` 的 Code Review Rules

Codex 会查找覆盖改动文件的 `AGENTS.md`，并遵循其中的审查规则。在 **离代码最近** 的那份文件里加 `## Code Review Rules`；需要分组时用 `###`。

仓库级放根目录；某服务的特殊规则放嵌套目录，例如 `services/experiment_reporting/AGENTS.md`。官方行为：对每个改动文件，同时应用根级与更具体的指引，这样无关改动不必背负别的服务上下文。

```md
## Code Review Rules

### Payment safety

- Flag payment capture without an idempotency key.
- Flag amount validation that happens after an external charge.
- Leave formatting and lint checks to CI.
```

写规则时官方建议：

- 盯会造成后果的仓库特有行为（兼容约束、数据边界、危险副作用），并说明为什么重要  
- 写清安全路径或允许例外，方便区分真问题与预期行为  
- 规则要可长期维护：偏结果，少绑易变函数名；放在管辖代码附近  
- 格式化、Lint 等确定性检查留给 CI  

规则 **引导** Codex，**不**替代测试、分支保护或必需审批。写完后拿一个代表性 PR 跑 `@codex review`，按噪声收紧或删掉无效条目。

## 7. Security Review（research preview）

Security Review 面向更关心安全风险的客户：在 PR diff、仓库上下文，以及已配置的威胁模型／安全指引上，做比普通 Code Review **更深** 的安全向审查。普通 Code Review 也可能带出安全相关问题，因此两份结果偶有重叠。

### 7.1 配置自动安全审查

官方概述步骤（更细的选项见官方文中「Security Review」链接；若该专页暂时不可用，以 GitHub 集成页与设置 UI 为准）：

1. 连接 GitHub 仓库。  
2. 打开 Codex 设置，选中仓库。  
3. 在 **Review security vulnerabilities** 下打开 **Auto security review**，用 **Review** 选择审哪些人的 PR；若希望与 Code Review 一起跑，把 **Trigger** 设为 **Whenever code review runs**。

### 7.2 手动触发与阅读报告

在 PR 评论：

```text
@codex security review
```

运行中会有反应，随后把安全发现贴回 PR。打开关联的 Codex 任务，切到 **Security Report** 页签看完整报告。

**我的用法**：鉴权、支付、密钥与数据边界相关的 PR，在普通 `@codex review` 之外再加一次 Security Review；一般文案／样式改动不必每次都开。

## 8. 根据审查意见修复：`@codex fix` 与 legacy cloud chat

审查贴出后，可在同一 PR 再评论：

```text
@codex fix the P1 issue
```

官方说明：这会以当前 Pull Request 为上下文启动 **legacy cloud chat**；在具备分支写入权限时，可以把修复推回该分支。

CI 失败等同理，例如：

```text
@codex fix the CI failures
```

更一般地：在评论里 `@codex` 且内容 **不是** `review`（审查触发语）时，Codex 会以该 PR 为上下文启动 legacy cloud chat。

修复提交仍要过 diff、测试和审批。重要改动应重新 `@codex review`（或等 Automatic review 按 trigger 再跑）。不要把「已处理」当成证据——应留下新提交与验证结果。

## 9. 人和 Codex 各负责什么

| 通常可由 Codex 做 | 仍须维护者负责 |
| --- | --- |
| 读 Issue／仓库上下文，在隔离环境改代码、跑约定测试 | 配置环境、密钥边界与仓库权限 |
| 在你确认后准备／创建 PR | 定义 `AGENTS.md` 审查规矩与合并策略 |
| `@codex review`／Automatic review／Security Review | 核对 diff、业务行为与风险是否可接受 |
| 有权限时按 `@codex fix …` 推修复 | CI、分支保护、必需审批与 **最终合并** |

合并前检查清单：

- [ ] 云环境已连对仓库，初始化可复现（或本地基线／分支已核对）  
- [ ] Issue 写清目标、范围、限制与验收  
- [ ] diff 与测试对应 Issue；无无关文件与敏感信息  
- [ ] PR 描述含真实验证与剩余风险／回滚  
- [ ] `@codex review`（或 Automatic review）结果已看；P0／P1 已处理或记录  
- [ ] 需要时已跑 Security Review，并查看 Security Report  
- [ ] CI、分支保护与必需人工审批满足  
- [ ] 由有权限的维护者执行合并；Issue 关联关闭方式已核对  

## 10. @codex 没反应时怎么查

按官方排查顺序：

1. Codex 设置里该仓库的 **code review** 是否已打开。  
2. 该 PR 是否属于 **已连接到 Codex** 的 GitHub 仓库。  
3. 触发语是否精确为 **`@codex review`**（安全审查则为 **`@codex security review`**）。  
4. 若依赖自动审查：核对仓库设置与 Personal preferences 里的 **Automatic review**，并确认 PR 事件匹配你的 **Review trigger**。

## 11. 常见失误（本地路径尤甚）

- **直接在 main 上改**：缺少清晰对比基线；先建分支或 worktree。  
- **默认 `git add .`**：易把旧改动、生成物、截图或本地配置一起暂存。  
- **测试过了就跳过 diff**：测试只覆盖它测到的行为；无关删除与配置变化仍要人看。  
- **Review 后只改本地不推 PR**：讨论必须和最新提交一致；推送后让 CI／审查对着新提交跑。  
- **让 Codex 自行合并**：代码正确只是条件之一；发布窗口、迁移与回滚责任仍在人。

## 12. 可复制的任务单（给云任务或本地会话）

```text
任务目标：

问题现象：

复现步骤：

预期行为：

相关文件或入口：

修改范围：

明确不修改：

完成条件：

基线命令：

验证命令：

风险与回滚：

请先只读调查并给出计划，不要修改文件。确认计划后再执行。完成后返回修改文件、测试输出、未覆盖项和剩余风险，不要自行提交、推送或合并。
```

## 参考资料

- [Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github)（developers 同源：[integrations/github](https://developers.openai.com/codex/integrations/github)）  
- [Codex Cloud](https://learn.chatgpt.com/docs/cloud)  
- [GitHub Pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)  

延伸阅读（站内）：

- AGENTS.md 怎么写 → https://codexguide.io/advanced/agents-md  
- 读懂 Git status／diff／log／blame → https://codexguide.io/guides/codex-git-status-diff-log-blame  
- 权限沙箱与审批 → https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi  

本文按 2026-10-22（Asia/Shanghai）可访问的官方文档核对。Code review／Security Review 开关名称与入口以你当前 Codex 设置页为准；Security Review 仍为 research preview。
