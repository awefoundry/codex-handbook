# gzhwz 处理报告

## 处理摘要

- 文章：`06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md`
- 处理日期：2026-09-04
- 处理环境：Windows 10 Pro Build 26100；Python 3.13.5 + Pillow 12.3.0；完整记录见同目录 `environment.md`。
- 原文已完成中文人性化润色，保留原有技术判断、官方参考链接和只读 Review 提示词。
- 正文已补充正确性、安全边界、测试覆盖和评论落地说明；按去除 Markdown 标记、图片路径、链接和代码块后的可读字符统计，正文约 2612 字，控制在 2500 字左右。
- 删除发布正文中的测试环境行、备用区说明、待截图说明和查找记录，避免编辑过程进入读者正文。

## 原图与处理图

网络素材均从 GitHub 官方文档页面及其公开图片资源获取，下载后先用 `view_image` 检查，再按 imagegzh 一号样式处理。

| 原图 | 网络来源 | 处理图 | 类型 | 原始尺寸 | 输出尺寸 | 处理与验收 |
| --- | --- | --- | --- | --- | --- | --- |
| `network-source/github-pull-request-tabs-changed-files.png` | `https://docs.github.com/assets/cb-23571/images/help/pull_requests/pull-request-tabs-changed-files.png` | `正文配图/图一.png` | GitHub 界面截图 | 1308×122 | 1334×148，约 8.8784:1 | 展示 `Files changed` 标签；保留文字和布局；透明圆角外框、`#d9d9d9` 细边框和轻阴影；四角透明；未发现账号、路径、令牌、二维码或登录信息；`view_image` 复核通过。 |
| `network-source/github-viewed-checkbox.png` | `https://docs.github.com/assets/cb-37862/images/help/pull_requests/viewed-checkbox.png` | `正文配图/图二.png` | GitHub 界面截图 | 2150×112 | 2176×138，约 15.7681:1 | 展示 `Viewed` 选项；保留文字和布局；透明圆角外框、`#d9d9d9` 细边框和轻阴影；四角透明；未发现账号、路径、令牌、二维码或登录信息；`view_image` 复核通过。 |
| `network-source/github-review-changes-button.png` | `https://docs.github.com/assets/cb-53614/images/help/pull_requests/review-changes-button.png` | `正文配图/图三.png` | GitHub 界面截图 | 2114×416 | 2140×442，约 4.8416:1 | 展示 `Review changes` 按钮；保留文字和布局；透明圆角外框、`#d9d9d9` 细边框和轻阴影；四角透明；未发现账号、路径、令牌、二维码或登录信息；`view_image` 复核通过。 |
| `generated/review-order-raw.png` | HiAPI `gpt-image-2/text-to-image`；任务 `tk-hiapi-01M1NTKN6M3AXRVHWNZDABB7DE` | `正文配图/图四.png` | Code Review 检查顺序概念图 | 1280×720 | 1280×720，16:9 | 展示“目标、范围、正确性 / 安全、测试、结论”五步路径；按 16:9 保持比例；添加轻微阴影、浅灰边框和圆角；四角透明；未发现真实品牌、路径、账号、API Key、Token、二维码或水印；`view_image` 复核通过。 |
| `generated/test-coverage-raw.png` | HiAPI `gpt-image-2/text-to-image`；任务 `tk-hiapi-01M1NTKMP8S6X7SE5VKCCQ6CA2` | `正文配图/图五.png` | 测试覆盖矩阵概念图 | 1672×941 | 1280×720，16:9 | 居中裁切后保持比例，避免拉伸；展示“正常输入、边界值、异常返回、权限不足、兼容旧行为”覆盖矩阵；添加轻微阴影、浅灰边框和圆角；四角透明；未发现真实品牌、路径、账号、API Key、Token、二维码或水印；`view_image` 复核通过。 |

原先使用的本地合成截图不再作为正文配图。三张网络原图保存在本篇 `network-source/` 中，两张 HiAPI 概念图的原始输出保存在 `generated/` 中。正文首次出现顺序对应 `图一.png` 到 `图五.png`。二维码不计入正文图号。

## 配图目录验收

- 正文配图目录：`正文配图/`
- 目录内容：仅有 `图一.png`、`图二.png`、`图三.png`、`图四.png`、`图五.png`
- 正文图片引用：5 张，引用顺序与文件名一致
- 图片独立成段：通过
- 正文配图与二维码、封面、原始截图分离：通过
- 四角透明像素检查：通过

## 链接埋点

| event_id | stage | position | intent | target_type | target_title | url | utm_status | verification_status | copy_role | post_publish_metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `contextual-validation-01` | `contextual` | “先理解目标，再看代码”中，GitHub 界面截图之后 | `get-resource` | 站内页 | CodexGuide 验证流程 | `https://codexguide.io/codex/validation?utm_source=wechat&utm_medium=article&utm_campaign=code-review-quality&utm_content=contextual-validation-01` | 已添加 `utm_content=contextual-validation-01` | 已核验：源码 canonical 为 `https://codexguide.io/codex/validation`，线上 HEAD 返回 HTTP 200 | 补充 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-website-01` | `closing` | “继续实践”段落，微信 CTA 之前 | `take-action` | 网站 CTA | CodexGuide Git 协作与代码审查专题 | `https://codexguide.io/advanced?utm_source=wechat&utm_medium=article&utm_campaign=code-review-quality&utm_content=closing-website-01` | 已添加 `utm_content=closing-website-01` | 已核验：源码 canonical 为 `https://codexguide.io/advanced`，线上 HEAD 返回 HTTP 200 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | `closing` | 网站 CTA 之后，全文最后 | `ask-or-connect` | 微信 CTA | 微信交流 | 不适用 | 不适用 | 已核验：默认二维码文件存在、可打开，正文引用无断链 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

埋点闸门摘要：

- `inserted_event_count`：3
- `required_minimum`：2
- `gate_status`：passed
- `exception_reason`：none

阶段缺省记录：

- `opening`：无自然入口。开头先交代 Review 判断目标，过早放入口会打断主题进入。
- `decision`：无自然入口。正文提供的是通用审查方法，没有单独的案例或工具需要在决策阶段承接。

## 二维码验收

- 源文件：`D:\CodexHome\skills\gzhwz\assets\wechat-qr.png`
- 发布文件：`wechat-qr.png`
- 处理方式：按要求原样复制，不调用 imagegzh，不裁切、不加边框、不加阴影、不重新生成、不压缩。
- 正文位置：网站 CTA 之后，且为最后一个引流区块。
- 文案验收：明确邀请围绕 PR 目标、变更范围和验证结果交流；未虚构微信号、公众号名称、客服身份或回复时效。

## 封面生成记录

- 已选标题：高质量 Code Review 怎么做？从正确性到测试的检查顺序
- baoyu-cover-image：确定为中文、标题-only、conceptual、digital、balanced 方向；项目配置启用 quick mode。
- banner-design：按公众号横版安全区检查，目标比例 2.35:1，目标尺寸 940×400 px；标题位于左侧安全区，视觉主体位于右侧。
- design：采用白色、深石墨色、低饱和绿色与红色、少量暖黄色的技术编辑风格；不使用真实 Logo、网址、二维码或人物身份。
- 图片生成后端：按用户明确要求使用 HiAPI 对外接口，服务为 `https://api.hiapi.ai/v1/tasks`，模型为 `gpt-image-2/text-to-image`，认证仅读取本机 `HIAPIAPIKEY` 或兼容别名 `HIAPI_API_KEY`，不在文件、日志或正文中记录密钥值。
- 封面生成提示词：`prompts/01-cover-code-review.md`；生成请求先通过 dry-run，再提交一次异步任务。
- HiAPI 任务：`tk-hiapi-01M1N5P7RCT88DENPQFS0JF7F6`；任务状态：`success`；原始输出：`cover-candidate/hiapi-cover.png`，`1280×720 px`。
- 最终封面：`cover.png`，从原始输出上下安全留白处居中裁切并等比缩放到 `940×400 px`，比例 `2.35:1`，比例误差为 0；未改写或覆盖标题文字。
- 封面验收：`view_image` 已检查原始输出和最终封面；标题为“高质量 Code Review 怎么做？从正确性到测试的检查顺序”，标题完整可读；未发现额外可发布文字、Logo、二维码、水印、账号、路径或令牌。
- 提示词：`prompts/01-cover-code-review.md`
- dry-run：通过；请求未联网创建任务。
- 此前 ZimaCode 尝试：HTTP 401 Unauthorized；失败发生在创建任务前，未返回 taskId，也没有可验收图片。用户随后明确指定 HiAPI，因此未在该线路盲目重试，改按用户选择使用 HiAPI 完成生成。
- 版权与敏感信息：提示词禁止新增品牌、真实网址、账号、路径、二维码和未核验事实；封面及两张正文概念图均已完成视觉和敏感信息验收。

## 正文概念图生成记录

- 图四：HiAPI 任务 `tk-hiapi-01M1NTKN6M3AXRVHWNZDABB7DE`，原始文件为 `generated/review-order-raw.png`，原始与输出尺寸均为 `1280×720 px`，比例为 `16:9`。
- 图五：HiAPI 任务 `tk-hiapi-01M1NTKMP8S6X7SE5VKCCQ6CA2`，原始文件为 `generated/test-coverage-raw.png`，原始尺寸为 `1672×941 px`，经居中裁切后输出为 `1280×720 px`，比例为 `16:9`。
- 两张图均通过 `view_image` 检查；未发现真实品牌、网址、账号、路径、API Key、Token、二维码或水印。
- 两张图均使用 Pillow 添加轻微阴影、浅灰边框和圆角，并检查 RGBA 模式与四角透明像素；输出文件未进入 `generated/` 以外的中间目录，正文配图目录只保留最终文件。

## 待确认项

- 公众号标题已确定；封面已使用 HiAPI 生成并完成尺寸转换与视觉验收。
- 网站链接已按仓库源码中的 canonical 核验；发布前仍需在公众号编辑器中确认链接可正常打开。
- 历史文章入口：本篇没有采用历史文章标题式链接。

## 最终验收

- 正文与对话隔离扫描：通过，未发现“用户提供”“用户素材”“用户截图”“投稿截图”等内部来源措辞。
- 敏感信息检查：正文配图和二维码均已检查；未发现需遮挡内容。
- 正文图片引用无断链：通过，图一至图五共 5 张。
- 参考链接保留：通过。
- 网站 CTA 在微信 CTA 之前：通过。
- 封面：已生成，使用 HiAPI `gpt-image-2/text-to-image`；最终尺寸 `940×400 px`，比例误差为 0，标题和主体验收通过。
