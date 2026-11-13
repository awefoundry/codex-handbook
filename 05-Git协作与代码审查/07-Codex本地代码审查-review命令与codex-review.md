---
id: codex-local-code-review
title: Codex 本地代码审查：用 /review 与 codex review 审未提交改动、分支和单个 commit
seo_title: Codex 本地代码审查：/review 四个预设与 codex review
description: Codex 的 /review 和 codex review 在本机 Git 仓库里审查未提交改动、相对基准分支的差异或某一个 commit，只报告问题。本文按官方文档整理 CLI 的四个预设、命令行参数和 review_model，并写上 Codex CLI 0.167.0 未登录时的真实报错。
lede: 提交前先让审查读 diff、写问题。审查不改工作区。GitHub 上的 @codex review 是另一条流程。
url: /guides/codex-local-code-review
status: published
section: guides
category: D-project-dev
topic: Git 协作与代码审查
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 基础
order: 7
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-08
date_modified: 2026-11-08
verified_on: 2026-11-08
tested_cli_version: 0.167.0
official_ref: https://learn.chatgpt.com/docs/code-review
keywords: [Codex review, /review, codex review, 本地代码审查, review_model, --uncommitted]
related: [codex-cli-commands-cheatsheet, permissions-sandbox-approvals, codex-github-issue-pr-workflow]
faq:
  - q: /review 会直接改代码或提交吗？
    a: 官方 Code review 和 CLI 文档都写：审查报告问题，不修改工作区。2026-11-08 在未登录的 Codex CLI 0.167.0 上跑完失败的审查后，测试仓库的 git status 仍是原来的未提交修改。这次没有拿到审查结论，也没有看到它自动提交。
  - q: 本地 /review 和 PR 里的 @codex review 是同一个命令吗？
    a: 本地 /review 与 codex review 审的是本机 Git 检出。GitHub 评论里的 @codex review 由仓库是否打开 Code review 决定，见《Codex 处理 GitHub Issue 并创建 Pull Request》。
  - q: 自定义提示词能和 --uncommitted 一起用吗？
    a: 命令文档写 --uncommitted、--base、--commit 和自定义 PROMPT 互相冲突。0.167.0 在参数冲突时，用法行却把 PROMPT 印成可选项。本文没有再跑「带提示词的 --uncommitted」，所以不把这个组合写成已经可用。
  - q: 本文有审查结果截图吗？
    a: 没有。未登录时审查在 401 处中断。没有桌面端，也没有打开 /review 的四个预设菜单。
---

# Codex 本地代码审查：用 /review 与 codex review 审未提交改动、分支和单个 commit

> 本文在线版：[codexguide.io/guides/codex-local-code-review](https://codexguide.io/guides/codex-local-code-review)

> 核对依据：2026-11-08 打开的 [Code review](https://learn.chatgpt.com/docs/code-review)、[Codex CLI](https://learn.chatgpt.com/docs/codex/cli)、[Slash commands](https://learn.chatgpt.com/docs/cli/slash-commands)、[Command line options](https://learn.chatgpt.com/docs/developer-commands) 和 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 里的 `review_model`。同一天在 Linux 上安装 `@openai/codex@0.167.0`，`codex --version` 为 `codex-cli 0.167.0`。审查命令在一个临时 Git 仓库里运行，当时 `codex login status` 输出 `Not logged in`，退出码 1。没有桌面端，没有审查结论，没有截图。

本地审查看的是你电脑上这份 Git 仓库。它适合提交前、开 Pull Request 前，先让 Codex 读一遍差异并列出问题。

GitHub 上由人打开的 Files changed、评论格式和「能不能合并」，仍按 [如何做一次高质量 Code Review](./06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md) 来判断。仓库评论里的 `@codex review` 属于云端审查，见 [Codex 处理 GitHub Issue 并创建 Pull Request](./01-Codex处理GitHub-Issue并创建PR.md)。参数表的短版本在 [CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。

## 先看结论

官方把两件事分开写。

**本地 `/review`**：在 Git 检出上启动一次专门的审查，读你选定的 diff，报告按优先级排列的问题。Code review 文档写：它不修改工作区。CLI 产品页上的预设菜单有四项。桌面应用和 IDE 扩展的文档各写了其中两项。

**非交互 `codex review`**：在脚本或提交前的终端里跑同一种审查。文档要求只选一个目标：`--uncommitted`、`--base <分支>`、`--commit <SHA>`，或一段自定义提示词。

审查用哪个模型，由当前会话的模型决定。要固定成另一个模型，在 `config.toml` 里设置 `review_model`。

人仍然决定哪些意见要改、哪些测试要补。审查结果本身不是合并许可。

## /review 的四个预设

在 Codex CLI 的对话里输入 `/review`。CLI 文档页「Review changes before they ship」展示的菜单是：

1. Review against a base branch（PR Style）
2. Review uncommitted changes
3. Review a commit
4. Custom review instructions

Code review 文档对 CLI 这四项的范围是：

| 预设 | 文档写的审查范围 |
| --- | --- |
| Review against a base branch | 找到 merge base，审查你这条分支相对基准分支的 diff |
| Review uncommitted changes | 已暂存、未暂存和未跟踪的文件 |
| Review a commit | 某一个 commit 引入的那一组改动 |
| Custom review instructions | 按你写的标准来审 |

同一页对桌面应用和 IDE 扩展各只列出前两项：相对基准分支，以及未提交改动。IDE 里 `/review` 只在当前项目位于 Git 仓库中时出现。应用的审查窗格也要求项目在 Git 仓库里；还不是仓库时，应用会提示创建。

本文没有桌面端，也没有在交互 TUI 里打开这个菜单。上表是文档原文的整理，不是一张实拍菜单。

斜杠命令页对 `/review` 的预期结果写的是：总结工作区里的问题，重点是行为变化和缺失的测试；模型用当前会话的，除非配置了 `review_model`。看具体改了哪些行，接着用 `/diff`。`/diff` 的说明是显示 Git diff，包括 Git 尚未跟踪的文件。

审查进行时，`/side` 不可用。这是斜杠命令页对 side 模式的限制。

## 非交互：codex review

`codex review --help` 在 0.167.0 上的用法是 `codex review [OPTIONS] [PROMPT]`。与文档一致的目标参数是：

| 参数 | 0.167.0 帮助里的说明 |
| --- | --- |
| `--uncommitted` | Review staged, unstaged, and untracked changes |
| `--base <BRANCH>` | Review changes against the given base branch |
| `--commit <SHA>` | Review the changes introduced by a commit |
| `--title <TITLE>` | Optional commit title to display in the review summary |
| `--strict-config` | `config.toml` 里有当前版本不认识的字段时直接报错 |
| `PROMPT` | 自定义审查要求。写成 `-` 时从标准输入读 |

命令文档写明：`--uncommitted`、`--base`、`--commit` 和自定义 `PROMPT` 互相冲突。`--title` 只能和 `--commit` 一起用。

0.167.0 上，两个冲突的真实报错是：

```text
error: the argument '--uncommitted' cannot be used with '--base <BRANCH>'
```

退出码 2。只写 `--title`、不写 `--commit` 时：

```text
error: the following required arguments were not provided:
  --commit <SHA>
```

退出码也是 2。

冲突报错附带的用法行是 `codex review --uncommitted [PROMPT]`，缺 `--commit` 时的用法行是 `codex review --commit <SHA> --title <TITLE> [PROMPT]`。方括号表示帮助文本把 PROMPT 印成了可选项。这和命令文档「PROMPT 与这三个目标冲突」并列放在这里。本文没有执行 `codex review --uncommitted "……"` 这种组合，不把方括号写成实测通过。

常用的三种写法：

```bash
codex review --uncommitted
codex review --base main
codex review --commit <SHA> --title "修复登录跳转"
```

自定义要求单独作为目标，或按文档从标准输入读：

```bash
codex review -
```

标准输入示例只说明文档和帮助里有这个读法。本文没有从管道喂入一段提示词。

`codex exec review` 在 0.167.0 的 `codex exec --help` 里是一条子命令，说明文字是 “Run a code review against the current repository”。命令文档把 `codex exec` 的 `--worktree` 写成不能和 `review` 一起用。本文没有跑 `codex exec review`。

## 这次未登录运行实际发生了什么

临时仓库里有一次提交，工作区还有未提交修改。`codex login status` 为 `Not logged in`。

`codex review --uncommitted` 和 `codex review --base main` 都打印了会话头，然后失败。会话头里这次的模型是 `gpt-6.1-sol`，`sandbox` 是 `read-only`，`approval` 是 `never`。这是这台没有登录配置的机器上的启动摘要。你自己的 `config.toml` 会换成别的模型和审批策略。

失败的可见结果是 HTTP 401，以及：

```text
ERROR: unexpected status 401 Unauthorized: Missing bearer or basic authentication in header
Review was interrupted. Please re-run /review and wait for it to complete.
```

两条命令的退出码都是 1。输出里还有 WebSocket 重试和本机缺少 `bubblewrap` 的警告。那些是这台 Linux 的环境信息，不代表审查逻辑本身。

结束后 `git status --short` 仍是原来的 `M app.py`。这次中断的审查没有改文件。官方文档写成功的审查也不改工作区；本文没有一次成功的审查可以对照。

登录方式见 [登录 Codex](../01-安装与首次使用/07-登录Codex.md)。审查要读仓库、有时还会按技能去看测试命令，放行范围见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 用 review_model 单独指定审查模型

配置参考对 `review_model` 的说明是：可选的模型覆盖，供 `/review` 使用；不设置时用当前会话的模型。斜杠命令页的 `/review` 预期结果写的是同一句话。示例配置里有一行注释：

```toml
# review_model = "gpt-6.1-sol"
```

这是示例文件里的注释，不是要求所有人改成这个模型名。模型必须是你的账号实际能用的那个。本文没有改 `config.toml`，没有比较两个模型的审查差异。

IDE 文档另有一项投递方式：默认审查出现在当前对话里；把 `chatgpt.reviewDelivery` 设为 `detached` 时，`/review` 会新开一个审查对话。本文没有改 IDE 设置。

## 审完怎么处理

审查列出问题之后：

1. 用 `/diff` 看它指到的文件和行，确认差异还在。
2. 对照 [高质量 Code Review](./06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md) 里的四件事：位置、触发条件、影响、怎样验证。业务优先级和能不能承担剩余风险，由人判断。
3. 要改代码时，新开一轮修改，或在同一会话里明确说「只改审查里的某一条」。修改仍走你原来的沙箱和审批。Code review 文档写：让 Codex 应用它找到的修复时，平常的沙箱和审批继续生效。
4. 改完再跑你项目自己的测试。审查没有宣称自己已经跑过测试。本文这次的 401 运行也没有跑测试。

应用里的审查窗格还可以按行评论、暂存和还原。那些是桌面应用的 Git 操作，文档写在 “Navigating the review pane” 和 “Staging and reverting files”。本文没有应用截图，不把那组按钮写成 CLI 里的步骤。

## 放进提交前清单

交互会话里，改完代码后输入 `/review`，选未提交改动或相对基准分支。非交互时，在仓库根目录：

```bash
git status --short
codex review --uncommitted
```

退出码不是 0，或输出是 401 / “Review was interrupted” 时，这次没有完成审查。先看 `codex login status`，再重跑。审查完成后自己看意见，再 `git add` 和 `git commit`。`codex review` 的帮助里没有提交参数。

相对 `main` 看整条分支时：

```bash
codex review --base main
```

只复查已经写进历史的某一个提交时，用 `--commit`。需要摘要里带标题时，加上 `--title`。

本文没有把这些命令放进 Git hook，也没有在 CI 里跑。要接进自动化，先在已登录的环境里确认退出码和输出格式，再写进 hook。

## 参考资料

- [Code review](https://learn.chatgpt.com/docs/code-review)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Slash commands](https://learn.chatgpt.com/docs/cli/slash-commands)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands)
- [Configuration Reference：review_model](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Sample Configuration](https://learn.chatgpt.com/docs/config-file/config-sample)
