# 素材查找记录

## 证据矩阵

| 文章步骤 | 需要证明的事实 | 首选素材 | 当前状态 | 后续动作 |
|---|---|---|---|---|
| 提交范围 | `git diff --stat`、`git diff --check` 和暂存范围可见 | 作者实拍终端 | 待截图 | 使用 `01-commit-pr-evidence-terminal.png` |
| 提交目的 | 提交摘要能表达单一行为变化 | 作者实拍终端 | 待截图 | 与范围检查放在同一张终端图中 |
| PR 描述 | 改动、动机、验证、风险、回滚和待确认项齐全 | 作者实拍 GitHub PR | 待截图 | 使用 `02-pr-description-scope-risk.png` |
| 诚实验证 | 不把未执行的测试写成已通过 | 终端命令与 PR 文本 | 待截图 | 只展示实际执行过的命令和结果 |
| 信息脱敏 | 截图无账号、令牌、私有路径和客户数据 | 作者复核后的截图 | 待截图 | 入库前逐张检查 |

## 平台记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| GitHub 官方文档 | pull request reviews | Web 官方页面 | verified-direct | 已核对文章中的官方 Review 资料链接；仅作为规则来源，不替代操作截图 |
| Conventional Commits | specification | Web 官方页面 | verified-direct | 已保留文章中的规范链接；不作为 UI 截图候选 |
| Bilibili | Git commit PR review evidence | B站搜索 API | no-qualified-result | 已运行 `agent-reach doctor --json`；未保存无法证明本文步骤的候选帧 |
| YouTube | commit PR review evidence | `yt-dlp` | no-qualified-result | 已确认后端可用，但初始化阶段未发现需要保存的合格操作帧 |
| X / Twitter | commit PR review | 无激活后端 | unavailable | Doctor 显示无 active backend，未声称直接搜索 |
| 小红书 | commit PR review | 无激活后端 | unavailable | Doctor 显示无 active backend，未声称直接搜索 |

## 研究说明

- 外部素材候选保持为空；不复制其他文章的截图目录，避免把相似但未经当前步骤核验的图片混入本篇。
- 公开网页可作为规则和概念来源，真实操作证据优先由作者在当前计算机上实拍。
