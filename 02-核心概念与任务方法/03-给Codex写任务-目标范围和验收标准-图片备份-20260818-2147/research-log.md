# 素材查找记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方文档 | `Codex prompting goal context output boundaries verification` | Jina Reader + Playwright 公开页面 | verified-direct | 核验目标、上下文、输出、边界、验证和 Codex 任务示例；官方文字可引用，界面截图仍需作者实拍。 |
| YouTube | `Codex prompting tasks context verification` | `yt-dlp` | verified-index | 核验 3 个公开视频的标题、作者、日期和时长；未把封面或缩略图作为候选图片。 |
| B站 | `Codex 提示词 任务 上下文 验证` | Agent Reach doctor / B站公开搜索 API | no-qualified-result | 后端可达但本轮没有核验出符合本文案例的操作截图。 |
| 小红书 | `Codex 提示词 写法` | Agent Reach doctor | unavailable | 未检测到可用登录后端，本轮未进行站内搜索。 |
| X | `Codex prompting` | Agent Reach doctor | unavailable | 未检测到可用后端，本轮未进行站内搜索。 |
| 用户指定排重页面 | `https://coding.stormzhang.ai/codex/12-slash-commands` | Jina Reader（仅排重对照） | excluded | 仅识别其“固定数量速查、入口分组、个人踩坑叙事”等表达特征；未引用、未改写其句子、未将其列为参考资料或图片来源。 |

## 本轮查询矩阵与核验结果（2026-08-19）

| 路线 | 查询词/页面 | 后端 | 核验结果 | 文章用途 |
|---|---|---|---|---|
| 官方文档 | `https://developers.openai.com/codex/prompting` | Jina Reader，官方原文 | `verified-direct`；页面明确列出 Goal、Context、Output、Boundaries，并建议重要任务要求 final check | 支撑“四类信息”和最终检查原则 |
| 官方最佳实践 | `https://developers.openai.com/codex/learn/best-practices` | Exa 索引 + Jina Reader | `verified-direct`；建议用 Goal、Context、Constraints、Done when 组织复杂任务，并要求测试、检查和 review | 支撑“完成标准”和 `AGENTS.md`/上下文边界的说明 |
| 官方长任务 | `https://developers.openai.com/codex/long-running-work` | Exa 索引 + Jina Reader | `verified-direct`；Outcome、Constraints、Verification 三项用于形成可验证目标；复杂任务可先 plan 再执行 | 支撑调查先行、验收证据和分阶段推进 |
| 官方已核验工作流 | `https://developers.openai.com/codex/use-cases/verified-operations-workflows` | Exa 索引 + Jina Reader | `verified-direct`；要求输入、批准范围、执行器、验证产物，并记录成功/失败和重试 | 支撑“输出必须带证据”的表格与示例 |
| 官方帮助中心 | `https://help.openai.com/en/articles/11369540-codex-in-chatgpt` | Jina Reader | `verified-direct`；确认 Codex 是写、审查和交付代码的 agent，并覆盖 Desktop、CLI、IDE、Web 入口 | 支撑文章环境和读者入口说明；不作为提示词句式依据 |
| 官方页面浏览器快照 | `https://developers.openai.com/codex/prompting`（实际重定向至 `https://learn.chatgpt.com/docs/prompting`） | Playwright CLI | `verified-direct`；页面标题为 `Prompting | ChatGPT Learn`，快照显示四类信息和 Codex prompting 章节；截图仅作核验留档，不作为本文操作配图 | 核对当前页面结构和链接重定向 |
| 英文网页搜索 | `site:developers.openai.com/codex prompting task goal context constraints verification` | Exa | `verified-index` 后再用 Jina 打开原文 | 用于发现官方页面，最终引用均回到原始官方 URL |
| YouTube | `OpenAI Codex /goal: From Prompt Replies to Verified Work` | `yt-dlp` | `verified-index`；视频 ID `zjGVKNOKOSM`，Fluid Coding & AI，2026-05-08，421 秒；未提取操作帧 | 仅作为延伸观看链接，不作为配图候选 |
| YouTube | `OpenAI Codex Tutorial #6 - Using the AGENTS.md file` | `yt-dlp` | `verified-index`；视频 ID `NlNuoH5PPl4`，Net Ninja，2025-10-04，284 秒；未提取操作帧 | 仅作为上下文规则延伸观看，不作为配图候选 |
| B站 | `Codex 提示词 任务 上下文 验证` | Agent Reach B站搜索 API | `no-qualified-result`；没有核验出显示具体操作状态的合格画面 | 不下载、不引用封面或缩略图 |
| 小红书 | `Codex 提示词 写法` | Agent Reach doctor | `unavailable`；无可用登录后端 | 不声称完成站内搜索 |
| X | `Codex prompting` | Agent Reach doctor | `unavailable`；无可用后端 | 不声称完成站内搜索 |

## 可提取的事实

- 官方文档强调提示词不需要固定语法；复杂任务才补充会改变结果的目标、上下文、输出和边界。
- 官方最佳实践使用 “Done when” 表述完成条件，示例包括测试通过、行为变化、bug 不再复现和 review 完成。
- 官方已核验工作流把验证产物列为输入的一部分，建议记录每项成功/失败、重试和未完成原因；本文将其转译为“对象 + 状态 + 证据”。
- 本文的“验证码按钮”是脱敏教学案例，不来自真实账号、客户项目或生产数据；待补的文章截图必须由作者在临时测试仓库中实拍。
