# gzhwz 处理报告

处理环境：Windows 11 专业版 24H2；PowerShell 7.6.4；2026-08-27 核验。完整记录：[environment.md](environment.md)。

## 正文与配图

- 正文已按现有材料和官方文档重写，保留 AGENTS.md 的项目规则、继承关系、模板和验收边界。
- 官方页面截图由本机 Chromium 真实渲染后保存，原图位于备份目录 `browser-capture/official-agents-docs.png`。
- 解释型层级示意图由内置 `image_gen` 生成，任务目录为 `01a04222-fb50-77c2-878f-05c7944bb102`，原图位于备份目录 `manual/instruction-layers.png`。
- `browser-capture/official-agents-docs.png` -> `正文配图/图一.png`：保留官方页面标题、规则发现顺序和 32 KiB 说明。
- `manual/instruction-layers.png` -> `正文配图/图二.png`：保留四层英文标签和箭头关系，不增加中文事实或品牌信息。
- 两张发布图均使用 imagegzh 一号样式的本地 Pillow 兜底处理：透明圆角外框、约 4 px 白色边界、`#d9d9d9` 细边框和轻阴影；四角像素已检查为透明。
- 发布前全文搜索已清零“用户提供”“用户素材”“用户截图”“投稿截图”“作者截图”等内部来源措辞。

## 链接与引流

| event_id | stage | position | intent | target_type | target_title / url | utm_status | verification_status | copy_role | post_publish_metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| opening-prerequisite-01 | opening | 导语第 2 段 | continue-reading | 历史文章 | 别再重复提醒 Codex：用 AGENTS.md 让它读项目先读规则；由公众号后台绑定 | 不适用：由公众号后台绑定 | 已核对标题，待作者在后台绑定 | 承诺 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| closing-site-01 | closing | 总结之后、微信区块之前 | take-action | 网站 CTA | https://codexguide.io/advanced/agents-md | 已添加：`utm_content=closing-site-01` | 已核验，canonical 路径来自网站 `advanced.ts` 与页面路由 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| closing-wechat-01 | closing | 网站 CTA 之后、全文最后 | ask-or-connect | 微信 CTA | 不适用 | 不适用：二维码入口 | 已核验：二维码文件可打开且正文引用无断链 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

文首历史文章标题需在公众号编辑器中选中后绑定“已发表内容”。正文网站链接已使用 `utm_source=wechat&utm_medium=article&utm_campaign=agents-md-project-rules&utm_content=closing-site-01`。

## 二维码验收

- 源文件：`D:\CodexHome\skills\gzhwz\assets\wechat-qr.png`
- 发布文件：`wechat-qr.png`
- SHA-256：`E5A625D07A9C5C41F9860060045ECACFFD247A6FCA6D6CC20596383BD9BBE001`，复制前后一致。
- 已用 `view_image` 检查可打开、二维码完整、未加圆角/边框/阴影；区块位于网站 CTA 之后并为最后一个引流区块。

## 验收与待确认

- Markdown 正文图片引用为 `图一.png`、`图二.png`，与 `正文配图/` 文件逐项对应；二维码路径存在且不计入正文配图编号。
- 两张正文配图均可打开，文字清晰，主体完整，样式一致；相邻图片使用独立段落并保留空段间距。
- 正文保留“模板示例”性质，示例命令需要读者按实际项目替换，不应直接视为该项目事实。
- 公众号发布前仍需在后台绑定历史文章标题，并确认网站页面线上可访问。
- 当前未生成封面，已停在公众号标题确认闸门，等待用户选择标题。
