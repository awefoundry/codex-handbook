# Codex 模型怎么选？推理强度 Low、Medium、High 有什么区别

## 本教程环境

| 项目 | 本教程使用版本 | 获取方式 | 核验日期 | 备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 24H2（OS Build 26100.4652） | Windows 注册表系统版本信息 | 2026-08-14 | Windows 内部产品名仍显示为 Windows 10 Pro，以公开名称与构建号为准 |
| IDE / 宿主应用 | Codex Windows 桌面端 26.803.10989.0 | 已安装应用包路径 | 2026-08-14 | 本文以桌面端为主；IDE 不适用 |
| Codex CLI | codex-cli 0.146.1 | `codex --version` | 2026-08-14 | 用于说明 CLI 中的模型与推理强度名称 |
| 目标插件 / App / Connector | 不适用 | 本教程不依赖插件、App 或 Connector | 2026-08-14 | 无需第三方账号或 API Key |
| 官方模型资料 | Web 托管版本 | OpenAI 官方 Codex Models 页面 | 2026-08-14 | 模型和界面可能更新，写作及发布前应再次核验 |

> 名称提醒：截至核验日期，Codex 桌面端把最低档显示为 **Light**，CLI 显示为 **Low**。本文标题沿用读者更常搜索的 Low，但正文应明确两者所处界面不同。

## 配图素材备用区（暂不计入正文图号）

> 本节用于写作阶段选图，发布前应将采用的素材移动到对应正文段落并重新编号。旧界面、限时活动和第三方教程必须标注日期与来源。

### 官方与可核验素材

- `01-openai-codex-models-page.png`：适合“模型入口与官方推荐”章节，证明 Codex 模型页当前展示 Sol、Terra、Luna 以及桌面端推理强度控件；来源为 [OpenAI Codex Models](https://developers.openai.com/codex/models)，OpenAI，页面于 2026-08-14 核验。该页面为持续更新的 Web 托管内容，发布前应复查。

### 视频与社区教程

- [Getting started with Codex](https://www.youtube.com/watch?v=px7XlbYgk7I)：OpenAI，YouTube，2026-01-12，官方入门演示；适合补看 Codex 整体界面，具体模型画面可能随版本变化。
- [OpenAI Codex Tutorial #8 - Context, Reasoning & TODO's](https://www.youtube.com/watch?v=kbv6Rn7lHkI)：Net Ninja，YouTube，2025-10-07，第三方教程；可辅助理解 reasoning 选项，但界面较旧，不作为当前模型名称的事实依据。

### 需要作者亲自截图

- [ ] `01-codex-model-control.png`：打开 Codex 桌面端任一新任务 → 定位输入框下方模型与推理强度控件 → 截取控件及其上下文；隐藏账号名、任务标题和工作区路径；停在打开选择器之前。
- [ ] `02-codex-model-list.png`：点击模型名称 → 展开当前账号可用的模型列表 → 截取完整列表；隐藏账号或组织信息；不要切换到会影响现有任务的模型。
- [ ] `03-codex-reasoning-levels.png`：点击推理强度控件 → 展开 Light、Medium、High、Extra High 等当前可见档位 → 截取完整菜单；隐藏私人任务内容；停在选择前。
- [ ] `04-codex-same-task-comparison.png`：分别在计划采用的三个档位运行同一条无敏感信息的小任务 → 截取三个完成结果及耗时/用量信息（界面有展示时）；不要使用客户代码、私有仓库或密钥。

### 查找记录

- OpenAI 官方文档：查询 `Codex models reasoning effort`；Exa 发现、Jina Reader 与 Playwright 打开原页核验；`verified-direct`。
- YouTube：查询 `OpenAI Codex model reasoning effort tutorial`；`yt-dlp` 读取公开元数据；`verified-direct`。
- Bilibili：查询 `Codex 模型 推理强度`；公开搜索 API 首次返回索引结果，后续复核触发 HTTP 412；`found-unverified`，未采用素材。
- X：`agent-reach doctor` 未发现可用后端；`unavailable`，未直接搜索。
- 小红书：`agent-reach doctor` 未发现可用后端；`unavailable`，未直接搜索。
- Reddit：`agent-reach doctor` 未发现可用后端；`unavailable`，未直接搜索。
