# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 专业版 24H2，版本 10.0.26100，构建 26100 | `Get-CimInstance Win32_OperatingSystem` | 2026-08-20 | 本文涉及本地终端和 Codex 权限/文件操作边界 |
| IDE / 宿主应用 | 不适用 | 文章使用 Codex CLI 与终端，不依赖 IDE | 2026-08-20 | 不写入正文摘要 |
| Codex | Codex CLI 0.147.0 | `codex --version` | 2026-08-20 | 本文以 CLI 的审批、沙箱和差异审查为主；桌面端界面需作者另行截图核验 |
| 目标插件 / App / Connector | 不适用 | 本文不依赖独立插件、App 或 Connector | 2026-08-20 | 不写入正文摘要 |
| 其他关键依赖 | Git（版本未在本次初始化中核验） | 官方 `git diff` 文档作为命令语义来源 | 2026-08-20 | 发布前若正文给出具体 Git 命令，应在作者机器上补跑 `git --version` |
| 图片处理运行时 | Python 3.13.5；Pillow 12.3.0 | `python --version`；`python -c "import PIL; print(PIL.__version__)"` | 2026-08-21 | 用于按 imagegzh 一号样式生成 `图一.png`、`图二.png`，不参与正文事实判断 |
| 浏览器核验 | Playwright CLI（通过 `npx --yes --package @playwright/cli` 调用） | 打开官方 OpenAI Developers 页面、snapshot、screenshot | 2026-08-21 | 用于获取公开页面截图；未使用登录态 |

## 采集说明

- 系统版本来自本机 `Get-CimInstance Win32_OperatingSystem`；Codex 版本来自 `codex --version`。
- 本次只记录影响文章判断的组件，没有记录账号、密钥、私人工作区名称或登录信息。
- OpenAI 权限与安全导航通过 Jina Reader 读取官方页面；Git 命令语义来自 Git 官方文档；OWASP 风险背景来自 OWASP Top Ten 官方页面。
