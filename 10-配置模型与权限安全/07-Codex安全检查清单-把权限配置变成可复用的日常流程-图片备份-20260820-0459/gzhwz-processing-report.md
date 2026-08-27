# gzhwz 处理报告

处理环境：Windows 11 24H2；Python + Pillow（本轮用于无损图片整理与脱敏）；2026-08-26 核验。

## 正文与配图

- 正文已改为面向读者的三节点检查流程，保留原有安全边界、风险分级和事故响应内容。
- 原图保留在 `manual/`；发布图统一输出到 `正文配图/`，按正文首次出现顺序命名。
- `manual/07-01-start-checklist.png` -> `正文配图/图一.png`：保留分支与工作区证据，未延伸解读未显示的权限字段。
- `manual/07-02-approval-check.png` -> `正文配图/图二.png`：遮挡本机路径，保留审批提示与拒绝/允许一次状态。
- `manual/07-03-final-diff-check.png` -> `正文配图/图三.png`：保留 diff、`git diff --check` 结果和未提交状态。
- 三张发布图均使用 imagegzh 一号样式：透明圆角外框、浅灰边框、紧凑留白；逐张检查可打开、文字清晰、主体完整。

## 链接与引流

| event_id | stage | position | intent | target_type | target_title / url | utm_status | verification_status | copy_role | post_publish_metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| closing-site-01 | closing | 总结之后 | take-action | 网站 CTA | https://codexguide.io | 未添加：站内主入口保持原 URL | 已核验 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| closing-wechat-01 | closing | 网站 CTA 之后 | ask-or-connect | 微信 CTA | 不适用 | 不适用：二维码入口 | 已核验 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

默认微信二维码已复制到 `assets/wechat-qr.png`，未经过 imagegzh 改造；正文引用位于网站 CTA 之后。

## 验收

- 正文图片均独占段落，图片与图注之间留有空段，连续配图之间有可见间距。
- 已清除发布正文中的内部来源措辞；原始来源、脱敏位置和处理记录仅保留在本报告与 gzhstart 工作区。
- 待发布前再次在微信公众号编辑器中确认图片缩放、段落间距和二维码可扫码。
