# gzhwz 处理记录

文章：`06-权限沙箱与审批-什么时候放行什么时候收紧.md`

处理环境：Windows 11；Python + Pillow；2026-08-21 核验。完整环境记录见同目录 `environment.md`。

## 图片处理

| 原图 | 正文处理图 | 正文位置 | 验收 |
| --- | --- | --- | --- |
| `online/05-ai-permission-sandbox-approval-layers.png` | `online/图一.png` | “1. 先把三个概念分开”第二段之后 | 已打开检查，主体完整；油画笔触、边界和审批闸门清晰；圆角、细边框、轻阴影符合 imagegzh 一号样式 |
| `online/01-openai-agent-approvals-security.png` | `online/图二.png` | “1. 先把三个概念分开”概念列表之后 | 官方文档截图，已目检；保留页面文字和导航，未补写 UI 事实 |
| `online/02-openai-sandboxing.png` | `online/图三.png` | “2. 常见动作分别需要什么能力”动作列表之后 | OpenAI 官方文档截图，已目检；沙箱边界文字清晰；imagegzh 一号样式验收通过 |
| `online/03-openai-permissions-profiles.png` | `online/图四.png` | “2. 常见动作分别需要什么能力”图三之后 | OpenAI 官方文档截图，已目检；权限档位清晰；imagegzh 一号样式验收通过 |
| `online/04-openai-auto-review.png` | `online/图五.png` | “3. 审批窗口里应该看什么”检查条件之后 | OpenAI 官方文档截图，已目检；自动审阅说明清晰；imagegzh 一号样式验收通过 |
| `online/05-openai-agent-internet-access.png` | `online/图六.png` | “6. 用最小权限完成一次真实任务”场景说明之后 | OpenAI 官方文档截图，已目检；网络访问说明清晰；imagegzh 一号样式验收通过 |

原图保留在 `online/05-ai-permission-sandbox-approval-layers.png` 及 5 张 `01-openai-*.png` 至 `05-openai-*.png` 文件中，正文仅引用处理后的 `online/图一.png` 至 `online/图六.png`。

## 编号与正文验收

- 正文图片总数：6。
- `图一` 至 `图六` 与正文引用文件名一致，路径可解析。
- `图一` 为 AI 生成教学示意；`图二` 至 `图六` 为 `94bd342` 提供的 OpenAI 官方文档截图，已在图注中区分概念参考与本机实测边界。

## 链接埋点

- 无自然入口：当前稿仍处于内容规划与素材处理阶段，尚未形成可核验的站内 CTA、历史文章绑定或外部行动入口。

## 二维码与待确认项

- 微信二维码未加入：当前用户只要求将示意图放入正文，且文章仍是未完成草稿；发布前按 gzhwz 规则复核文末网站 CTA 与微信 CTA。
- 待作者补齐危险动作的可丢弃测试、作者实拍截图，以及正文中的实测结论。
