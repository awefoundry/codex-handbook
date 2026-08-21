# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 24H2，构建 26100 | PowerShell `Get-ComputerInfo -Property WindowsProductName,WindowsVersion,OsBuildNumber`；系统接口将产品名兼容性回报为 Windows 10 Pro，以构建号判定 24H2 | 2026-08-21 | 文章计划演示原生 Windows 上的 Codex Desktop 与 CLI 权限行为 |
| IDE / 宿主应用 | Codex Desktop 26.814.5517.0 | PowerShell `Get-AppxPackage` 查询 `OpenAI.Codex` 包版本 | 2026-08-21 | 影响权限菜单与审批提示界面 |
| Codex | Codex CLI 0.147.0 | 本机执行 `codex --version` | 2026-08-21 | 用于只读、工作区写入和网络审批对照实验 |
| 目标插件 / App / Connector | 无独立插件；官方 OpenAI 文档为持续更新服务 | 直接打开 `https://developers.openai.com/codex/agent-approvals-security` 与 `https://developers.openai.com/codex/concepts/sandboxing`，均跳转至 ChatGPT Learn 当前文档 | 2026-08-21 | 不虚构网页服务版本；页面内容和 UI 可能持续变化 |
| 其他关键依赖 | Playwright CLI（通过 `npx --package @playwright/cli` 临时调用）；Agent Reach 平台路由 | `Get-Command npx`；`agent-reach doctor --json` | 2026-08-21 | 仅用于公开页面核验和素材检索，不进入正文环境摘要 |

## 平台可用性记录

- OpenAI 官方文档：`verified-direct`，Playwright 打开原页、页面快照与截图均已检查。
- YouTube：`verified-direct`，`yt-dlp` 可读取元数据、章节并下载公开 360p 操作视频；逐帧检查后仅保留实际 UI 状态。
- B 站：`verified-index`，B 站搜索 API 可达但 `bili-cli` 未安装；通过公开 API/索引核验原始 BV 号、作者、日期与主题，未把未查看画面当作配图。
- 小红书：`unavailable`，`agent-reach doctor --json` 未发现可用后端；网页索引没有合格结果。
- X：`unavailable`，Twitter CLI/OpenCLI 均无活动后端；本次没有声称直接搜索。
