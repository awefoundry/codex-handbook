# 素材查找记录

## 证据矩阵

| 文章步骤 | 需要证明的事实 | 首选素材 | 当前状态 | 后续动作 |
|---|---|---|---|---|
| 提交范围 | `git diff --stat`、`git diff --check` 和暂存范围可见 | 作者实拍终端 | 待截图 | 使用 `01-commit-pr-evidence-terminal.png` |
| 提交目的 | 提交摘要能表达单一行为变化 | 作者实拍终端 | 待截图 | 与范围检查放在同一张终端图中 |
| PR 描述 | 改动、动机、验证、风险、回滚和待确认项齐全 | 作者实拍 GitHub PR | 待截图 | 使用 `02-pr-description-scope-risk.png` |
| 诚实验证 | 不把未执行的测试写成已通过 | 作者实拍终端与 PR 文本 | 待截图 | 只展示实际执行过的命令和结果 |
| GitHub 审查入口 | `Files changed`、diff 视图和 `Review changes` 入口可见 | GitHub Docs 官方截图 | 已保存 5 张候选 | 发布前按正文需要选图，并标注官方界面核验日期 |
| 信息脱敏 | 截图无账号、令牌、私有路径和客户数据 | 作者复核后的截图 | 待截图 | 入库前逐张检查 |

## 平台记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| GitHub 官方文档 | pull request reviews；reviewing proposed changes | Web 页面 + 直接下载官方文档图片 | verified-direct | 已保存 5 张真实操作界面截图；未保存 Logo、封面、缩略图或无关图片文件预览 |
| Conventional Commits | specification | Web 官方页面 | verified-direct | 已保留文章中的规范链接；页面没有适合作为本文步骤证据的操作截图 |
| Bilibili | Git commit PR review evidence | `agent-reach doctor --json` 后按路由检查 | no-qualified-result | 未发现已核验且能清楚证明本文步骤的操作帧；没有把搜索结果或封面写入素材清单 |
| YouTube | Git commit pull request code review tutorial | `yt-dlp` 元数据搜索 | verified-index | 找到可观看的教程线索，但未打开并抽取能证明本文步骤的精确帧，因此不作为配图候选；来源仅作研究参考 |
| X / Twitter | commit PR review | 无 active backend | unavailable | 未声称直接搜索 |
| 小红书 | commit PR review | 无 active backend | unavailable | 未声称直接搜索 |

## 已保存官方候选

- `pull-request-tabs-changed-files.png`：1308×122，证明进入 `Files changed`。
- `diff-settings-menu.png`：2288×656，证明可切换 Unified/Split 并隐藏空白差异。
- `review-changes-button.png`：2114×416，证明打开 `Review changes`。
- `abandon-review-button.png`：1316×1078，证明 `Finish your review` 面板中的 Comment/Approve/Request changes 和 Submit review。
- `viewed-checkbox.png`：2150×112，证明用 `Viewed` 标记完成检查的文件。

## 研究说明

- 外部素材只补充 GitHub 审查界面证据；终端命令输出和 PR 描述内容仍必须由作者在本机测试仓库中实拍，避免把第三方教程中的账号、路径或测试结果误当成自己的证据。
- GitHub Docs 页面提供了带橙色标注的操作截图，适合作为界面入口参考；截图中的示例仓库、分支名和计数不应被解释为本文自己的仓库状态。
- 2026-09-04 已逐张打开保存的原图并检查清晰度、尺寸和是否与文章步骤相关。
