# Git 协作与代码审查

讲清楚 Codex 如何参与版本控制、团队协作和代码审查。

## 内容范围

- 阅读 `git status`、diff 和提交历史。
- 分支、提交、合并和冲突处理。
- Git worktree 的使用场景。
- 从 Issue 到 Pull Request 的完整流程。
- 使用 Codex Review 检查正确性、安全和测试风险。
- 为提交和 PR 写清楚改了什么、为什么修改。

## 推荐阅读顺序

### 一、先把 Git 现场和隔离方式搞清楚

1. [Git 协作前先检查什么：仓库、分支与脏工作区](./01-Git协作前先检查什么-仓库分支与脏工作区.md)
2. [Codex 如何读懂 Git：status、diff、log 与 blame](./02-Codex如何读懂Git-status-diff-log与blame.md)
3. [分支和 Worktree 怎么选：隔离任务、并行工作与恢复现场](./03-分支和Worktree怎么选-隔离任务并行工作与恢复现场.md)

### 二、从 Issue 走到可审查的 PR

4. [从 Issue 到 Pull Request：一次完整的团队协作闭环](./04-从Issue到PullRequest-一次完整团队协作闭环.md)
5. [怎样写出可审查的 Commit 和 PR：范围、证据与风险](./05-怎样写出可审查的Commit和PR-范围验证证据与风险.md)
6. [如何做一次高质量 Code Review：正确性、安全、测试与可维护性](./06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md)
7. [Review 反馈怎么处理：追加提交、修改 PR 与保持讨论清晰](./07-Review反馈怎么处理-追加提交修改PR与保持讨论清晰.md)

### 三、处理合并风险并建立团队门禁

8. [Merge、Squash、Rebase 怎么选：合并策略与冲突处理](./08-Merge-Squash-Rebase怎么选-合并策略与冲突处理.md)
9. [把协作规则自动化：分支保护、Code Owners 与 CI 门禁](./09-把协作规则自动化-分支保护CodeOwners与CI门禁.md)

### 四、让 Codex 进入 Review 环节

10. [让 Codex 参与 Pull Request Review：规则、触发与安全边界](./10-让Codex参与PullRequestReview-Review规则与安全审查.md)
11. [实战复盘：Codex 如何把一个 Bug 修复交付成可审查 PR](./11-实战复盘-Codex如何把Bug修复交付成可审查PR.md)

## 每篇文章的最低交付标准

- 有一个明确的 Git 协作问题，而不是命令罗列。
- 有可复制的命令或 Codex 提示词，并写明哪些操作保持只读。
- 有修改前状态、diff、验证结果和未解决事项。
- 有最小验收清单，必要时说明回滚方式。
- 涉及 GitHub 登录态、仓库设置或 Codex Cloud 时，使用测试仓库并由作者亲自截取脱敏画面。

## 章节边界

第 02 节的斜杠命令表只负责入口速查；第 03 节负责 AGENTS.md 基础概念；第 08 节负责 GitHub 插件的具体连接和 Issue→PR 操作；第 06 节负责测试技术。本文只讲 Git 现场、协作过程、审查判断和交付边界。

## 已上线文章

- [Codex 处理 GitHub Issue 并创建 Pull Request](./01-Codex处理GitHub-Issue并创建PR.md)
