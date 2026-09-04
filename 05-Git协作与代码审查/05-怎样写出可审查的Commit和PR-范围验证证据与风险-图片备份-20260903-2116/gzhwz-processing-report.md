# gzhwz 处理报告

## 基本信息

- `article_id`：`reviewable-commit-pr`
- 正文：`05-怎样写出可审查的Commit和PR-范围验证证据与风险.md`
- 已确认公众号标题：`Commit 不只写“改了什么”：一份可复核的 PR 审查方法`
- 处理环境：Windows 10 Pro 24H2；PowerShell 5.1；Node.js v22.22.3；Python 3.13.5 + Pillow 12.3.0；Git 2.47.0.windows.2；2026-09-04 核验。完整记录：`environment.md`。
- 正文配图数量：6 张；其中 2 张为 HiAPI 生成概念插图，3 张为终端案例截图，1 张为 GitHub Docs 界面截图；二维码是结尾 CTA 素材，不计入正文图号。
- 三张终端案例原图保留在 `manual/` 作为内部证据备份；发布版图二至图四按正文顺序分别展示初始化与差异统计、差异检查与完整 diff、交互式暂存与提交复核，并用不可逆纯色遮挡个人路径。
- 本轮新增 3 张作者补充终端截图：`manual/05-terminal-followup-initialize.png`、`manual/06-terminal-followup-diff-and-stage.png`、`manual/07-terminal-followup-commit.png`。它们用于补充初始化、diff、交互式暂存和提交复核证据，不进入正文图号；正文继续使用已脱敏验收的图二至图四。

## 正文修改

- 将原稿整理为读者可直接执行的 Git 提交与 PR 审查教程。
- 保留 `git status`、`git diff`、`git add -p`、`git commit`、`git show` 和 PR 描述模板等事实内容。
- 删除素材备用区、内部处理说明、作者来源措辞、本机路径和未完成截图清单。
- 按正文首次出现顺序加入提交范围、交互式暂存、PR 描述和 diff 设置四个视觉节点。
- 文末加入已核验的网站 CTA 和微信交流 CTA，网站链接使用稳定 UTM。

## 图片备份与处理映射

原始生成文件和网络候选保存在备份工作区，发布文件保存在 `发布素材/正文配图/`，未覆盖原图。生成图和裁切图均经过 `imagegzh` 一号样式的本地处理，成品带白色内边距、圆角、`#d9d9d9` 细边框和轻阴影；图二保留证据素材原始比例。

| 正文编号 | 原始素材 | 处理后文件 | 类型 | 尺寸 | 验收 |
|---|---|---|---|---|---|
| 图一 | `hiapi-source/01-hiapi-commit-scope-20260904.png` | `正文配图/图一.png` | HiAPI 生成概念插图 | 1600×900，16:9 | 已用 `view_image` 检查。表达 diff 进入聚焦提交、无关修改留在工作区；无可读账号、路径、Token、Logo、二维码或水印；四角透明、边框和阴影符合一号样式。 |
| 图二 | `manual/02-terminal-initialize.png` | `正文配图/图二.png` | 终端案例截图 | 2016×656，原始比例 | 保留初始化结果、示例文件创建、工作区状态和 `git diff --stat`；本机路径及初始化输出中的完整目录已用不可逆纯色遮挡，命令和结果可读。 |
| 图三 | `manual/03-terminal-diff.png` | `正文配图/图三.png` | 终端案例截图 | 2016×1046，原始比例 | 保留 `git diff --check`、完整 diff、README.md 与 login.txt 的变化；本机路径已遮挡，diff 文字和颜色可读。 |
| 图四 | `manual/04-terminal-commit.png` | `正文配图/图四.png` | 终端案例截图 | 2016×1472，原始比例 | 保留 `git add -p`、暂存区检查、提交、`git show` 和最终状态；本机路径已遮挡，提交信息和范围结果可读。 |
| 图五 | `hiapi-source/02-hiapi-pr-evidence-20260904.png` | `正文配图/图五.png` | HiAPI 生成概念插图 | 1600×900，16:9 | 已用 `view_image` 检查。表达 PR 描述的改动、动机、验证、风险与回滚字段关系；无可读账号、路径、Token、Logo、二维码或水印；四角透明、边框和阴影符合一号样式。 |
| 图六 | `online/diff-settings-menu.png` | `正文配图/图六.png` | GitHub Docs 官方界面截图 | 2304×672，原始比例 | 已用 `view_image` 检查。保留 Files changed、Unified/Split 和 Hide whitespace 设置；示例仓库内容不作为本文测试结果。 |

## 网络素材记录

- GitHub Docs 官方界面截图来源页面为 `https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request`，图六只用于解释 diff 视图设置。
- 其他官方候选保留在 `online/`，未进入正文配图目录；正文没有把示例仓库内容写成本文测试结果。

## HiAPI 概念插图

- 服务：`https://api.hiapi.ai/v1/tasks`
- 模型：`gpt-image-2/text-to-image`
- 参数：`resolution=1K`、`aspect_ratio=16:9`
- 调用前已执行 dry-run，确认模型、比例、运行环境和密钥存在状态；dry-run 未提交生成任务。
- 新图一任务：`tk-hiapi-01M1PGW7ZARGHX41VFA28N5KA2`。
- 新图五任务：`tk-hiapi-01M1PGW7ZQZ5SK449JTT6VR511`。
- 两项任务均成功生成并下载原图，随后由本地 Pillow 处理为 `1600×900` 透明圆角画布；旧版 HiAPI 原图和旧版发布图仍保留在备份工作区，未覆盖。
- 提示词要求无文字、无品牌、无账号、无路径、无 Token、无二维码、无水印；生成后已用 `view_image` 检查。

## 封面生成

- 标题：`Commit 不只写“改了什么”：一份可复核的 PR 审查方法`。
- 技能分工：`baoyu-cover-image` 确定概念型封面方向与标题层级；`banner-design` 核对公众号横版安全区、视觉焦点和尺寸；`design` 复核留白、配色和信息密度；使用 Codex 原生 `image_gen` 生成位图。
- 提示词：`发布素材/prompts/01-cover-commit-pr-review.md`。
- 原始生成图：`online/cover-generated-original.png`；原始尺寸为 1922×818，未覆盖原图。
- 发布封面：`发布素材/cover.png`；最终尺寸 940×400，比例 2.35:1，比例误差为 0。
- 验收：已用 `view_image` 检查标题逐字可读、主体完整、中央安全区无越界；无额外文字、Logo、二维码、水印、账号、路径或凭据。

## 链接与埋点

| event_id | stage | position | intent | target_type | target_title / url | utm_status | verification_status | copy_role | post_publish_metrics |
|---|---|---|---|---|---|---|---|---|---|
| `contextual-review-docs-01` | `contextual` | “用证据检查范围和风险”首段 | `verify-evidence` | 外部资料 | GitHub 审查 Pull Request 的改动；`https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request` | 不可添加：官方资料 URL 保持原样 | 已核验 | 证据 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-website-01` | `closing` | 结语之后、微信 CTA 之前 | `take-action` | 网站 CTA | 修改后如何验证：从 diff 到回归检查；`https://codexguide.io/codex/validation?utm_source=wechat&utm_medium=article&utm_campaign=reviewable-commit-pr&utm_content=closing-website-01` | 已添加：`utm_content=closing-website-01` | 已核验：网站仓库存在对应 canonical 页面 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | `closing` | 网站 CTA 之后、全文最后 | `ask-or-connect` | 微信 CTA | 不适用：二维码入口 | 不适用 | 已核验：二维码文件存在、正文引用无断链、位于最后一个引流区块 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

埋点闸门摘要：

```text
inserted_event_count: 3
required_minimum: 2
gate_status: passed
exception_reason: none
```

## 二维码验收

- 源文件：`D:\CodexHome\skills\gzhwz\assets\wechat-qr.png`
- 发布文件：`发布素材/wechat-qr.png`
- 未调用 `imagegzh`，未裁切、未加边框、未压缩，复制前后像素一致。
- 正文引用无断链，二维码位于网站 CTA 之后的全文最后一个引流区块。

## 封面标题闸门

- 状态：`passed`
- 已选择标题：`Commit 不只写“改了什么”：一份可复核的 PR 审查方法`。
- 正文、配图、埋点、二维码和脱敏检查已完成，封面已生成并验收。

## 验收

- 正文图片引用按首次出现顺序为 `正文配图/图一.png`、`正文配图/图二.png`、`正文配图/图三.png`、`正文配图/图四.png`、`正文配图/图五.png`、`正文配图/图六.png`，与文件逐项对应。
- `正文配图/` 只包含六张正文图，没有原始截图、未采用概念图和二维码。
- 发布正文未出现“用户提供”“用户素材”“用户截图”“投稿截图”“作者截图”、本机绝对路径、内部处理文件名或任务 ID。
- 入选生成概念图均为 16:9，比例误差为 0；图二至图四为终端案例截图，分别为 2016×656、2016×1046、2016×1472，主体和文字可读；未采用的探索图和原始素材均保留在备份目录。
- 正文未出现“用户提供”“用户素材”“用户截图”“投稿截图”“作者截图”、本机绝对路径、内部处理文件名或任务 ID。
- 封面为 940×400、2.35:1，标题和视觉主体已通过 `view_image` 验收；原始生成图保留在 `online/cover-generated-original.png`。
- 仍需确认：GitHub Docs 界面可能随平台更新；网站 CTA 的发布后点击数据待记录。

## 本轮篇幅处理

- 正文压缩并重新排序后约 4712 个文件字符、2338 个中文字符，保留六张正文图、PR 模板、网站 CTA、微信 CTA 和参考资料。
- `check_prose.py` 的硬性规则检查无 AI 黑话、重复段落和重复句，但其固定的中文字符下限为 3000；本篇按用户指定的约 2500 字篇幅保留 2338 个中文字符，过短项属于篇幅目标与脚本阈值冲突，未通过增加重复内容规避。
- 工作区校验：`validate_gzh_workspace.py` 通过；正文图片引用、发布目录、透明角和尺寸检查通过。
