# 素材查找记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方文档 | `Codex models reasoning effort`、`Codex model selection reasoning levels` | Exa → Jina Reader → Playwright | verified-direct | 打开 `developers.openai.com/codex/models` 原页，保存并人工检查官方页面截图 |
| YouTube | `OpenAI Codex model reasoning effort tutorial` | yt-dlp | verified-direct | 核验 OpenAI 官方入门视频与 Net Ninja reasoning 教程元数据；只列观看链接，未提取视频帧 |
| Bilibili | `Codex 模型 推理强度` | B 站公开搜索 API | found-unverified | 本机无 `bili` CLI；首次发现索引结果，复核时 HTTP 412，未采用候选 |
| X | `Codex reasoning effort` | 无可用后端 | unavailable | `agent-reach doctor --json` 显示 Twitter CLI/OpenCLI 均不可用；未直接搜索 |
| 小红书 | `Codex 模型 推理强度` | 无可用后端 | unavailable | Doctor 未发现已认证后端；未登录、未读取浏览器 Cookie |
| Reddit | `Codex reasoning effort` | 无可用后端 | unavailable | Doctor 未发现 Reddit 后端；未直接搜索 |

## 可视证据矩阵

| 文章步骤/主张 | 读者需要看到什么 | 首选证据 | 当前状态 |
|---|---|---|---|
| 模型入口在哪里 | 输入框下方的模型与推理强度控件 | 作者桌面端截图 `01-codex-model-control.png` | 待作者截图 |
| 当前有哪些模型 | 当前账号真实模型列表 | 作者桌面端截图 `02-codex-model-list.png` | 待作者截图；官方页面截图可作旁证 |
| Light/Low、Medium、High 的区别 | 档位菜单与官方定义 | 作者桌面端截图 `03-codex-reasoning-levels.png` + 官方 Models 页面 | 官方证据已保存，产品截图待补 |
| 同一任务的实际差异 | 完全相同输入下的可观察结果与耗时/用量 | 作者对比截图 `04-codex-same-task-comparison.png` | 待作者实测 |

## 口径结论

- 官方页面于 2026-08-14 核验：桌面端最低推理档位称为 Light，CLI 称为 Low。
- Medium 是速度与推理深度的平衡起点；更高档位适合多步骤、需要更多分析或检查的任务，但通常更慢且使用更多 token。
- 当前官方推荐模型为 GPT-5.6 Sol、Terra、Luna，属于高时效信息，正式发布前必须复查。
