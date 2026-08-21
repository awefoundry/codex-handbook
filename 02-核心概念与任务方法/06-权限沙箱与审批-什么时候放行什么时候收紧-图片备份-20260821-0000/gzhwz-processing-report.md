# gzhwz 处理记录

文章：`06-权限沙箱与审批-什么时候放行什么时候收紧.md`

处理环境：Windows 11；Python + Pillow；2026-08-21 核验。完整环境记录见同目录 `environment.md`。

## 图片处理

| 原图 | 正文处理图 | 正文位置 | 验收 |
| --- | --- | --- | --- |
| `online/01-openai-agent-approvals-security.png` | `online/图一.png` | “1. 先把三个概念分开”概念列表之后 | 官方文档截图，已目检；保留页面文字和导航，未补写 UI 事实 |
| `online/05-ai-permission-sandbox-approval-layers.png` | `online/图二.png` | “1. 先把三个概念分开”贯穿任务说明之后 | 已打开检查，主体完整；油画笔触、边界和审批闸门清晰；圆角、细边框、轻阴影符合 imagegzh 一号样式 |
| `online/02-openai-sandboxing.png` | `online/图三.png` | “2. 常见动作分别需要什么能力”动作列表之后 | OpenAI 官方文档截图，已目检；沙箱边界文字清晰；imagegzh 一号样式验收通过 |
| `online/03-openai-permissions-profiles.png` | `online/图四.png` | “4. 哪些情况可以放行”放行条件之后 | OpenAI 官方文档截图，已目检；权限档位清晰；imagegzh 一号样式验收通过 |
| `online/04-openai-auto-review.png` | `online/图五.png` | “5. 哪些情况应该收紧或拒绝”收紧条件之后 | OpenAI 官方文档截图，已目检；自动审阅说明清晰；imagegzh 一号样式验收通过 |
| `online/05-openai-agent-internet-access.png` | `online/图六.png` | “6. 用最小权限完成一次真实任务”场景说明之后 | OpenAI 官方文档截图，已目检；网络访问说明清晰；imagegzh 一号样式验收通过 |

原图保留在 `online/01-openai-*.png` 至 `05-openai-*.png` 及 `05-ai-permission-sandbox-approval-layers.png` 中，正文仅引用处理后的 `online/图一.png` 至 `online/图六.png`。

2026-08-21 第二轮：发现正文首次出现顺序为官方截图在前、AI 示意图在后，与“按首次出现顺序编号”规则不符，已将 `online/图一.png` 与 `online/图二.png` 经临时文件名安全互换（未覆盖任何文件），同步更新正文引用、图注、alt 文本与本表及 `manifest.tsv`；并修正图四、图五在记录中的小节归属（原误记为第 2、3 节）。互换后 6 张处理图已全部重新打开验收通过。

## 编号与正文验收

- 正文图片总数：6。
- `图一` 至 `图六` 与正文从上到下的首次出现顺序一致，引用文件名与路径可解析、无断链。
- `图二` 为 AI 生成教学示意；`图一`、`图三` 至 `图六` 为 `94bd342` 提供的 OpenAI 官方文档截图，已在图注中区分概念参考与本机实测边界。
- `manual/` 下的 `图一.png` 至 `图五.png` 为未引用的备选素材（含 AI 示意图副本与带完整浏览器框架的官方页面截图），不计入正文编号；作者实拍截图仍按 `manual-steps.md` 待补。

## 链接埋点

- 无自然入口：当前稿仍处于实测补齐阶段，没有可核验的站内 canonical URL、历史文章标题或外部行动入口，未向正文插入猜测链接。
- `opening-summary-01`：未采用；位置为开头；intent `continue-reading`；target_type 历史文章；target_title 待确认；url 由公众号后台绑定；utm_status 不适用：未确认标题；verification_status 未采用；copy_role 承诺；post_publish_metrics 阅读/点击/深读/关注/评论/咨询/转化均待记录。
- `contextual-evidence-01`：未采用；位置为正文配图之后；intent `verify-evidence`；target_type 外部资料；target_title OpenAI Codex approvals & security；url 已在图片清单记录；utm_status 不可添加：官方文档链接用于图片溯源，不作为正文 CTA；verification_status 已核验但未作引流；copy_role 证据；post_publish_metrics 阅读/点击/深读/关注/评论/咨询/转化均待记录。
- `decision-checklist-01`：待确认；位置为总结之后；intent `get-resource`；target_type 站内页；target_title 待确认；url 待确认；utm_status 待确认；verification_status 待确认；copy_role 行动；post_publish_metrics 阅读/点击/深读/关注/评论/咨询/转化均待记录。

## 二维码与待确认项

- 微信二维码未加入：文章仍缺少结论段和网站 CTA，当前不提前插入文末区块。发布前应复制默认二维码源 `D:\CodexHome\skills\gzhwz\assets\wechat-qr.png` 到发布素材目录，保持原像素并放在网站 CTA 之后。
- 上线阻塞项：危险动作的可丢弃测试、作者实拍截图（`manual-steps.md` 中 6 项均未完成）、动作风险对照表、拒绝审批后的替代方案、正文总结，以及可核验的网站 canonical URL。

## 上线闸门

- [x] 正文图片 6 张均有处理副本、来源记录和可解析引用。
- [x] 官方资料来源与 AI 示意图已在图注中区分。
- [ ] 6 项作者实拍与权限实验完成。
- [ ] 4 项正文完成标准完成并复核。
- [ ] 总结、网站 CTA、微信 CTA 和二维码验收完成。
- [ ] 文章状态改为可发布并完成公众号编辑器预览。
