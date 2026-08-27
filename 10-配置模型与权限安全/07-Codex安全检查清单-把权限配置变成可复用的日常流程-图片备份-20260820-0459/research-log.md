# 研究与视觉证据记录

核验日期：2026-08-26（美国东部时间）。本文只接受能证明具体操作状态的截图；官方文档页面用于核对事实，不作为正文操作截图。

## 视觉证据矩阵

| 文章步骤 | 需要证明的事实 | 首选证据 | 当前状态 | 备注 |
|---|---|---|---|---|
| 任务开始前 | 当前仓库/分支与工作区状态可被一次检查 | 作者在 Codex Desktop 的脱敏截图 | 已收到/已核验 | `07-01-start-checklist.png`；画面实际证明分支与干净状态，不延伸证明未显示的 profile、sandbox 或网络开关 |
| 执行中 | 审批提示展示完整命令、目录、网络行为和批准范围 | 作者在临时仓库触发的无害审批提示 | 已收到/已核验 | `07-02-approval-check.png`；只停留在提示并取消，未批准 |
| 提交或交付前 | diff、测试结果、计划外文件和敏感输出已被检查 | 作者在版本控制面板的脱敏截图 | 已收到/已核验 | `07-03-final-diff-check.png`；保持未提交，不推送或部署 |
| 风险分级表 | 低/中/高/未知四级的处理方式 | 文本表格 | 已由正文覆盖 | 不需要装饰图 |
| 事故响应 | 停止、保留日志、撤销凭据、检查影响范围、最小权限复测 | 文本清单 | 已由正文覆盖 | 不需要登录或生产环境截图 |

## 来源检索

| 平台 | 查询词 | 后端 | 结果状态 | 核验与回退说明 |
|---|---|---|---|---|
| OpenAI 官方文档 | `Codex sandbox approval policy network access security` | Exa 发现 + Jina Reader 直读 + Playwright 公开页 | verified-direct | 已核验 [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)、[Sandbox](https://developers.openai.com/codex/concepts/sandboxing)、[Config basics](https://developers.openai.com/codex/config-file/config-basic)、[Advanced Configuration](https://developers.openai.com/codex/config-file/config-advanced)。Playwright 页面实际显示了 sandbox、approval、network access 和 Version control 章节。 |
| Bilibili | `Codex 权限 沙箱` | Agent Reach doctor：B站搜索 API；直接调用公开搜索 API | verified-index | 搜索结果包含权限、沙箱和审批主题的视频，但本轮没有打开原视频或截取帧，因此不保存候选图，也不把封面列入 manifest。 |
| YouTube | `Codex sandbox approval permissions security` | Agent Reach doctor：yt-dlp | found-unverified | 找到第三方教程元数据，但未核验视频中的具体 UI 时间点；仅作为后续选题线索，不作为配图来源。 |
| X / Twitter | `Codex permissions security` | Agent Reach doctor：无 active backend | unavailable | 未直接搜索，不声称有 X 结果。 |
| 小红书 | `Codex 配置 权限 沙箱` | Agent Reach doctor：无 active backend | unavailable | 未直接搜索，不声称有小红书结果。 |
| 其他社区平台 | `Codex security` | 未请求 | not-attempted | 本文不依赖社区观点，优先使用官方文档和作者自截屏。 |

## 失败与时效记录

- B站 `bili` CLI 未安装；公开搜索 API 可用，但只能验证索引元数据，不能替代原视频画面核验。
- 当前 OpenAI 文档显示发布时间为 2026-08-27 GMT，正文核验按本机 2026-08-26 美国东部时间记录；发布前如 UI 或配置键再次变化，应重新核验。
- 未下载任何视频、缩略图或社区图片；三张作者截图已登记到 `manifest.tsv`，没有把无法证明操作的素材混入正文。
