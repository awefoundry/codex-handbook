# gzhwz 处理报告

## 基本信息

- `article_id`：`reviewable-commit-pr`
- 正文：`05-怎样写出可审查的Commit和PR-范围验证证据与风险.md`
- 处理环境：Windows 10 Pro 24H2；PowerShell 5.1；Node.js v22.22.3；Python 3.13.5 + Pillow 12.3.0；Git 2.47.0.windows.2；2026-09-04 核验。完整记录：`environment.md`。
- 正文配图数量：2 张；二维码是结尾 CTA 素材，不计入正文图号。
- 原有终端案例保留在 `manual/` 作为内部证据备份。因画面含本机路径，未放入发布正文。

## 正文修改

- 将原稿整理为读者可直接执行的 Git 提交与 PR 审查教程。
- 保留 `git status`、`git diff`、`git add -p`、`git commit`、`git show` 和 PR 描述模板等事实内容。
- 删除素材备用区、内部处理说明、作者来源措辞、本机路径和未完成截图清单。
- 在“一个提交只回答一个问题”和“用证据检查范围和风险”两个节点加入概念插图。
- 文末加入微信交流 CTA；没有核验到本篇对应的网站 canonical URL，因此未在正文猜写网站链接。

## 图片备份与处理映射

原始生成文件保存在 `online/`，发布文件保存在 `正文配图/`，未覆盖原图。两张生成图均经过 `imagegzh` 一号样式的本地处理，成品四角透明，带白色内边距、圆角、`#d9d9d9` 细边框和轻阴影。

| 正文编号 | 原始素材 | 处理后文件 | 类型 | 尺寸 | 验收 |
|---|---|---|---|---|---|
| 图一 | `online/generated-scope.png` | `正文配图/图一.png` | HiAPI 生成概念插图 | 1600×900，16:9 | 已用 `view_image` 检查。表达 diff 进入聚焦提交、无关改动留在外部的关系；无可读文字、账号、路径、Token、Logo、二维码或水印。 |
| 图二 | `online/generated-evidence.png` | `正文配图/图二.png` | HiAPI 生成概念插图 | 1600×900，16:9 | 已用 `view_image` 检查。表达 diff、终端、清单、风险和回滚组成审查证据链；无可读文字、账号、路径、Token、Logo、二维码或水印。 |

## 网络素材记录

- 已有的 GitHub Docs 官方界面截图继续保存在 `online/`，来源页面为 `https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request`。
- 本轮没有把官方截图直接加入正文配图目录，正文用文字说明 `Files changed`、Unified/Split、`Viewed` 和 `Review changes`，避免让示例界面中的仓库内容被误读为本文实测结果。

## HiAPI 概念插图

- 服务：`https://api.hiapi.ai/v1/tasks`
- 模型：`gpt-image-2/text-to-image`
- 参数：`resolution=1K`、`aspect_ratio=16:9`
- 调用前已执行 dry-run，确认模型、比例、运行环境和密钥存在状态；dry-run 未提交生成任务。
- 图一任务：`tk-hiapi-01M1NB9DKKZRNHA8YSTEMMM3CW`。
- 图二任务：`tk-hiapi-01M1NB9CG3K4ZVAM5PNK1VP818`。
- 两个任务最终状态均为 `success`。生成原图未覆盖，发布图由本地 Pillow 处理。
- 提示词要求无文字、无品牌、无账号、无路径、无 Token、无二维码、无水印；生成后已用 `view_image` 检查。

## 链接与埋点

| event_id | stage | position | intent | target_type | target_title / url | utm_status | verification_status | copy_role | post_publish_metrics |
|---|---|---|---|---|---|---|---|---|---|
| `contextual-review-docs-01` | `contextual` | “用证据检查范围和风险”第二段 | `verify-evidence` | 外部资料 | GitHub 审查 Pull Request 的改动；`https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request` | 不可添加：官方资料 URL 保持原样 | 已核验 | 证据 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | `closing` | 网站入口之后、全文最后 | `ask-or-connect` | 微信 CTA | 不适用：二维码入口 | 不适用 | 已核验：二维码文件存在、正文引用无断链、位于最后一个引流区块 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-website-01` | `closing` | 未插入 | `take-action` | 网站 CTA | 待确认：没有可核验的本篇 canonical URL | 待确认：未插入 | 未采用 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

埋点闸门摘要：

```text
inserted_event_count: 2
required_minimum: 2
gate_status: passed
exception_reason: closing website CTA 未插入，因为本篇 canonical URL 未核验；已保留微信 CTA 和一个正文外部证据入口。
```

## 二维码验收

- 源文件：`D:\CodexHome\skills\gzhwz\assets\wechat-qr.png`
- 发布文件：`wechat-qr.png`
- 未调用 `imagegzh`，未裁切、未加边框、未压缩，复制前后像素一致。
- 正文引用无断链，二维码位于全文最后一个引流区块。

## 封面标题闸门

- 状态：`pending_user_selection`
- 正文、配图、埋点、二维码和脱敏检查已完成。
- 尚未生成封面，等待选择公众号标题。

## 验收

- 正文图片引用按首次出现顺序为 `正文配图/图一.png`、`正文配图/图二.png`，与文件逐项对应。
- `正文配图/` 只包含两张正文图，没有原始截图和二维码。
- 发布正文未出现“用户提供”“用户素材”“用户截图”“投稿截图”“作者截图”、本机绝对路径、内部处理文件名或任务 ID。
- 概念插图均为 1600×900，比例误差为 0；终端案例未进入发布正文，原件保留在备份目录。
- 仍需确认：是否补充一张脱敏后的 PR 描述界面截图；是否提供本篇教程网站 canonical URL。