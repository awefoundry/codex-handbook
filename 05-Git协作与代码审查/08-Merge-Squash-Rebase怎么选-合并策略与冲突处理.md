# Merge、Squash、Rebase 怎么选：合并策略与冲突处理

> 难度：进阶
>
> 类型：概念与排障

> 测试环境：Windows 10 Pro build 26100；Codex CLI 0.147.0；Git 2.47.0.windows.2；2026-09-03 核验。

## 三种策略解决的是不同问题

Merge 保留分支汇合的历史；Squash 把一个 PR 压成一个提交；Rebase 把提交重新放到新的基线上并改写提交 ID。没有一种策略适合所有团队，规则应写进仓库协作约定。

## 更新自己的功能分支

    git fetch origin
    git switch fix/login-error
    git rebase origin/main

发生冲突时先查看状态和冲突文件，逐个理解两边意图。解决后运行 `git add <file>`，再执行 `git rebase --continue`。如果发现基线选错，使用 `git rebase --abort` 回到开始前状态。

## 合并前的选择

- 需要保留每个提交的演进过程，选择 Merge。
- 团队只关心一个可回滚的主题提交，选择 Squash。
- 个人功能分支需要线性历史，可以在未被他人依赖时 Rebase。

不要对 `main` 或多人共享分支随意 Rebase。GitHub 的线性历史和分支保护设置也会影响可用的合并按钮。

## 给 Codex 的冲突提示词

    请先只读列出冲突文件、双方修改意图和可能受影响的测试。
    不要自动选择 ours/theirs，不要提交或推送。
    给出每个冲突的解决建议，等我确认后再编辑。

## 验收清单

- [ ] 冲突标记全部清除。
- [ ] 解决结果保留了双方必须保留的行为。
- [ ] 受影响的测试、lint 或构建重新运行。
- [ ] 没有对共享分支做未经确认的强制推送。

## 参考资料

- [Atlassian Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [Git rebase documentation](https://git-scm.com/docs/git-rebase)

## 配图素材备用区（暂不计入正文图号）

> 本节用于写作阶段选图，发布前将采用的素材移动到正文段落并重新编号。当前没有已保存的外部图片候选；以下条目是截图计划与来源记录。

### 官方与可核验操作界面

- 暂无合格外部操作截图。官方资料解释了合并方式和冲突命令，但页面中的插图不直接证明本文的本地操作结果，暂不作为正文图。

### 需要作者亲自截图

- [ ] `01-history-strategy-graph.png`：在一次性测试仓库中展示 `git log --graph --oneline --decorate --all`，证明 Merge 保留汇合点、Squash 收敛为主题提交、Rebase 形成线性历史；隐藏本机用户名和真实仓库路径。
- [ ] `02-rebase-conflict-state.png`：在临时分支制造冲突后展示 `git status`、冲突文件和冲突标记；不要推送共享分支，不要截取令牌、账号或私有路径。
- [ ] `03-conflict-resolved-tests-passed.png`：解决冲突后展示 `git add`、`git rebase --continue` 之后的状态以及受影响测试结果；测试命令可使用最小示例仓库。
- [ ] `04-rebase-abort-recovery.png`：执行 `git rebase --abort` 后展示恢复前的分支状态和 `git log --graph`；停在本地恢复完成处，不要执行强制推送。
- [ ] `05-github-merge-methods-dropdown.png`：在可公开展示的测试 PR 中打开合并方式下拉菜单，展示 Merge、Squash、Rebase 选项；隐藏仓库名、用户名、分支名和任何评论内容，停在确认合并之前。

### 查找记录

- 官方资料：Git `git-rebase` 文档（https://git-scm.com/docs/git-rebase），2026-09-03 访问；核验了 `--continue`、`--abort`、冲突标记和提交重放语义。
- 官方资料：GitHub Pull Request merges（https://docs.github.com/en/pull-requests/reference/pull-request-merges），2026-09-03 访问；核验了 Merge commit、Squash and merge、Rebase and merge 的历史结果与适用条件。
- 第三方资料：Atlassian Merging vs. Rebasing（https://www.atlassian.com/git/tutorials/merging-vs-rebasing），2026-09-03 访问；作为概念交叉核验，不作为操作截图来源。
- 平台素材工作区：`08-Merge-Squash-Rebase怎么选-合并策略与冲突处理-图片备份-20260903-2143/`。
- 平台覆盖：B站 `no-qualified-result`（搜索 API 可达，但未发现已打开并核验、能证明本文具体 UI 状态的候选；`bili` CLI 未安装）；YouTube `found-unverified`（可查元数据，未保存任何缩略图或未核验帧）；小红书 `unavailable`（无活动后端）；X `unavailable`（无活动后端）；官方网页 `verified-direct`。
