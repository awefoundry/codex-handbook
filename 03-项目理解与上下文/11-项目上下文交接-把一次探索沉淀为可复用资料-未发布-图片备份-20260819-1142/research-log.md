# 素材查找记录

核验日期：2026-08-27。查询矩阵覆盖官方文档、全网索引、视频和社区平台；候选图必须证明“在哪里点、预期状态是什么、结果如何”，因此本轮不把文档封面或视频缩略图当配图。

## 查询与平台状态

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方 | `Codex AGENTS.md project context task handoff` / `Codex customization durable project guidance` | Jina Reader + Playwright CLI | verified-direct | 已打开并核验 https://developers.openai.com/codex/guides/agents-md 与 https://developers.openai.com/codex/concepts/customization；前者展示发现顺序、合并顺序和 32 KiB 上限，后者区分 AGENTS.md、技能、MCP、记忆与任务上下文。Playwright 页面重定向到 ChatGPT Learn，但内容可见；截图仅作研究凭据，不列入 manifest。 |
| 全网搜索 | `OpenAI Codex codebase context understand project repository best practices` | Exa via mcporter | verified-index | 找到 OpenAI 官方 AGENTS.md、Customization、Codex manual 等页面；索引结果用于发现入口，事实以逐页核验的官方页面为准。 |
| YouTube | `OpenAI Codex codebase context tutorial` | yt-dlp | verified-index | 仅核验视频标题、作者、日期和时长，未检查正片与精确时间戳；不保存封面或视频帧。 |
| Bilibili | `Codex 项目 上下文 AGENTS.md 教程` | B站搜索 API（Agent Reach active backend） | unavailable | 请求返回非 JSON 页面，无法验证原始视频或操作时间戳；不引用、不下载缩略图。 |
| X | `Codex 项目上下文 AGENTS.md 任务交接` | 无可用后端 | unavailable | `agent-reach doctor --json` 未检测到 Twitter 后端，未直接搜索。 |
| 小红书 | `Codex 项目上下文 AGENTS.md 任务交接` | 无可用后端 | unavailable | `agent-reach doctor --json` 未检测到小红书后端，未直接搜索。 |
| Reddit | `Codex project context handoff AGENTS.md` | 无可用后端 | unavailable | `agent-reach doctor --json` 未检测到 Reddit 后端，未直接搜索。 |
| 本地实操 | 文章计划中的真实操作步骤 | 作者后续补拍 | pending | 等待 `manual-steps.md` 中 4 张脱敏截图；未使用模拟 UI 或装饰图。 |

## 视觉证据矩阵

| 文章步骤 | 需要证明的 UI 事实 | 首选证据 | 当前状态 | 采用文件 |
|---|---|---|---|---|
| 结果分类 | 调查结果按稳定性与用途分层 | 作者在编辑器中的脱敏草稿截图 | pending | `manual/11-01-调查结果分类.png` |
| AGENTS / README 分工 | 稳定规则与读者入口分别维护 | 作者并排打开两个公开示例文件 | pending | `manual/11-02-AGENTS与README分工.png` |
| 下一轮任务交接 | 任务说明包含路径、未知项、验收和下一步 | Codex Desktop 发送前任务草稿 | pending | `manual/11-03-下一轮任务交接.png` |
| 过期检查 | 更新时间、责任角色、失效条件可被复核 | 编辑器中的维护字段 | pending | `manual/11-04-过期信息检查.png` |

## 研究限制

- 当前 `manifest.tsv` 为空：没有任何已保存图片，因此不存在无来源或不合格候选。
- 公开文档可证明概念与规则，但不能替代本文计划中的真实编辑器、终端和 Codex 操作画面。
- 登录、身份验证、发送、提交、发布等操作不由本流程自动执行；需要时按 `manual-steps.md` 由作者自行截图并在不可逆动作前停止。

## 本轮已保存素材

| 素材 | 状态 | 说明 |
|---|---|---|
| `online/11-web-01-openai-agents-md.png` | verified-direct | OpenAI 官方 AGENTS.md 文档，Playwright 打开并目检，1280×720。 |
| `online/11-web-02-openai-customization.png` | verified-direct | OpenAI 官方 Customization 文档，Playwright 打开并目检，1280×720。 |
| `online/11-generated-context-layers.png` | generated | Codex image_gen 生成的项目上下文分层解释图，1672×941，不代表真实界面。 |
| `online/11-generated-expiry-check.png` | generated | Codex image_gen 生成的过期检查维护闭环图，1672×941，不代表真实界面。 |

本轮未生成或保存作者实拍的编辑器/Codex 任务截图；`manual/` 中的 4 张截图仍需作者后续补拍。文章正文当前不在本机实操截图流程中，以上素材先作为备用区候选。
