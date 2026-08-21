# 素材查找记录

本文是 Codex 日常开发工作流教程，首轮视觉素材优先级为作者在公开示例仓库中的新鲜实操截图。没有指定外部文章、视频或社交平台来源，因此不下载在线图片、不把视频封面或宣传图当作候选。

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| 官方网页/文档 | Codex explore bug fix refactor testing workflow | Jina Reader 可用；本轮未发起检索 | no-qualified-result | 文章需要具体仓库操作证据，静态宣传页不能替代 |
| B 站 | Codex 探索 修 Bug 重构 写测试 工作流 | `agent-reach doctor --json`：B站搜索 API | no-qualified-result | 未搜索，未指定视频来源；不使用封面或裸链接 |
| YouTube | Codex explore debug refactor testing workflow | `yt-dlp` 可用 | no-qualified-result | 未搜索，未指定视频来源 |
| 小红书 | Codex 修 Bug 工作流 | 无活动后端 | unavailable | doctor 报告未安装 OpenCLI/xiaohongshu-mcp |
| X | Codex debugging workflow | 无活动后端 | unavailable | doctor 报告未安装 twitter-cli/OpenCLI |
| 本地公开示例仓库 | 四类任务的实操步骤 | 作者手工截图 | pending-manual-capture | 由 `manual-steps.md` 指定截图文件名、脱敏和停止点 |

## 视觉证据矩阵

| 文章步骤 | 要证明的事实 | 首选证据 | 当前状态 |
|---|---|---|---|
| 探索 | 规则、README、依赖和目录入口先于修改 | `01-explore-project-map.png` | 待作者截图 |
| 探索 | 无修改请求时保持只读 | `02-explore-readonly-boundary.png` | 待作者截图 |
| 修 Bug | 先用输入、报错和预期行为稳定复现 | `03-bug-reproduction-failure.png` | 待作者截图 |
| 修 Bug | 原复现用例和回归检查通过 | `04-bug-verification-pass.png` | 待作者截图 |
| 重构 | 先建立行为/性能基线和范围 | `05-refactor-baseline-diff.png` | 待作者截图 |
| 重构 | 小步修改后立即看差异并检查 | `06-refactor-small-step-check.png` | 待作者截图 |
| 写测试 | 测试场景对应风险和行为断言 | `07-test-risk-matrix.png` | 待作者截图 |
| 写测试 | 新增测试与回归测试的实际结果 | `08-test-result-summary.png` | 待作者截图 |
| 混合任务 | 阶段切换和人工决策点 | `09-hybrid-workflow-handoff.png` | 待作者截图 |

## 环境核验

- `agent-reach doctor --json`：2026-08-20 执行。可用后端包括 YouTube `yt-dlp`、B站搜索 API、Jina Reader；小红书、X 无活动后端。
- 未执行登录、注册、支付、预览、发布或不可逆设置操作。
