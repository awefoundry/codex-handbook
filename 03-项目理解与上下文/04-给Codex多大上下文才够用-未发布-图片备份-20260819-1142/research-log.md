# 素材查找记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方 | `Codex 上下文选择、文件路径、diff 和任务范围` | Jina Reader | verified-direct | 已读取《How OpenAI uses Codex》，核验定位核心逻辑、模块关系、数据流、故障传播、Ask Mode、文件路径与开发环境等官方建议。 |
| OpenAI 官方 | 同上 | Playwright CLI | unavailable | 原始公开页在当前网络返回 403；已按路由规则回退到 Jina Reader，未保存 403 页面截图。 |
| 全网搜索 | `OpenAI Codex codebase context understand project repository best practices` | Exa via mcporter | verified-index | 找到 OpenAI 官方使用指南、Codex 配置文档与 Codex 仓库 AGENTS.md；仅作写作线索，正式引用前需逐页复核。 |
| YouTube | `OpenAI Codex codebase context tutorial` | yt-dlp | verified-index | 核验 3 条视频元数据；当前未检查正片和精确时间戳，因此不保存封面或视频帧。 |
| Bilibili | `Codex 项目 上下文 代码库 教程` | B站搜索 API | unavailable | Doctor 显示公开搜索 API 可用，但本次请求返回非 JSON 页面；未获得可核验候选，不引用。 |
| X | `Codex 上下文选择、文件路径、diff 和任务范围` | 无可用后端 | unavailable | Agent Reach Doctor 未检测到 Twitter 后端，未直接搜索。 |
| 小红书 | `Codex 上下文选择、文件路径、diff 和任务范围` | 无可用后端 | unavailable | Agent Reach Doctor 未检测到小红书后端，未直接搜索。 |
| Reddit | `Codex 上下文选择、文件路径、diff 和任务范围` | 无可用后端 | unavailable | Agent Reach Doctor 未检测到 Reddit 后端，未直接搜索。 |
| 本地实操 | 上下文不足、过量与最小充分输入 | `computer-use` + TextEdit/Finder | partial | 2026-08-21 已采集输入对照、补充顺序和素材目录 3 张配图；尚未运行三组 Codex 对照任务，因此不记录追问次数或结果差异。 |
