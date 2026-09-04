# 素材查找记录

## 视觉证据矩阵

| 正文步骤 | 需要证明的事实 | 首选证据 | 当前状态 | 处理决定 |
|---|---|---|---|---|
| 三种策略的历史差异 | Merge 有汇合点，Squash 收敛主题提交，Rebase 形成线性历史 | 一次性测试仓库的 `git log --graph` 实拍 | `manual-required` | 不使用外部示意图，保留 `01-history-strategy-graph.png` 待拍 |
| 更新功能分支与冲突 | `git rebase` 停在冲突处，可用 `--continue` 或 `--abort` | 本地终端实拍 | `manual-required` | 保留 `02-rebase-conflict-state.png`、`03-conflict-resolved-tests-passed.png`、`04-rebase-abort-recovery.png` 待拍 |
| GitHub 合并按钮 | 仓库设置影响 Merge、Squash、Rebase 选项 | 测试 PR 的合并方式下拉菜单 | `manual-required` | 保留 `05-github-merge-methods-dropdown.png` 待拍，停在确认前 |
| Codex 冲突提示词 | 提示词能表达“先只读、不要自动选择、等待确认” | 编辑器或终端中的非敏感示例文本 | `manual-required` | 可与 `02` 或 `03` 合并拍摄，不单独制造外部候选 |

## 来源核验

- Git 官方文档：<https://git-scm.com/docs/git-rebase>；2026-09-03 公开页面直读。核验了冲突后 `git add`、`git rebase --continue`、`git rebase --abort` 的说明，以及 rebase 会逐个重放提交的语义。来源等级：official / verified-direct。
- GitHub 官方文档：<https://docs.github.com/en/pull-requests/reference/pull-request-merges>；2026-09-03 公开页面直读。核验了 Merge commit、Squash and merge、Rebase and merge 的结果、线性历史和长分支注意事项。来源等级：official / verified-direct。
- Atlassian 教程：<https://www.atlassian.com/git/tutorials/merging-vs-rebasing>；2026-09-03 公开页面直读。用于概念交叉核验。来源等级：third-party / verified-direct；不作为图片候选。

## 平台检索记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| 官方网页 | `git rebase conflict continue abort`; `GitHub pull request merge methods` | 公开网页直读 | `verified-direct` | 只记录资料，不把官方页面插图当作本文操作截图 |
| B站 | `Git merge squash rebase 冲突` | Agent Reach doctor：B站搜索 API；`bili` CLI 未安装 | `no-qualified-result` | API 可达但没有保存已打开并核验的具体操作画面；不使用搜索缩略图 |
| YouTube | `git merge squash rebase conflict tutorial` | Agent Reach doctor：`yt-dlp` | `found-unverified` | 仅取得候选元数据，未打开原视频并核验时间戳；不保存封面或缩略图 |
| 小红书 | `Git rebase 冲突` | Agent Reach doctor：无活动后端 | `unavailable` | 未登录、未自动配置，也未声称直接搜索 |
| X | `git rebase conflict` | Agent Reach doctor：无活动后端 | `unavailable` | 未登录、未自动配置，也未声称直接搜索 |

## 版本与时效

- 本地 Git 为 2.47.0.windows.2；官方 `git-rebase` 页面显示文档持续更新，因此截图中的命令输出应以本地核验为准。
- GitHub 合并按钮受仓库设置、分支保护、权限和冲突状态影响；外部页面只能证明概念，不能替代当前测试 PR 的实拍。
- 工作区没有保存图片候选，`online/` 保持为空；`manifest.tsv` 仅保留标准表头，待作者补拍并完成来源记录后再运行校验。
