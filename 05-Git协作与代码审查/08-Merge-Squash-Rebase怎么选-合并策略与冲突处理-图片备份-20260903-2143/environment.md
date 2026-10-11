# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 10 Pro build 26100（系统版本 2009） | PowerShell `Get-ComputerInfo -Property WindowsProductName,WindowsVersion,OsBuildNumber` | 2026-09-03 | Git 命令行与本地终端截图的运行环境 |
| IDE / 宿主应用 | 不适用 | 本教程不依赖 IDE 操作 | 2026-09-03 | 主要在 PowerShell 中复现 |
| Codex | Codex CLI 0.147.0 | `codex --version` | 2026-09-03 | 仅用于文章中的冲突提示词示例，不改变 Git 行为 |
| 目标插件 / App / Connector | 不适用 | 本教程不依赖插件、App 或 Connector | 2026-09-03 | Git 与 GitHub 文档是教程对象，不是运行时插件 |
| 其他关键依赖 | Git 2.47.0.windows.2；Node.js v22.22.3；npm 10.9.8 | `git --version`、`node --version`、`npm --version` | 2026-09-03 | Node/npm 仅用于本机工具链检查，不参与 Git 示例 |

## 采集说明

- 核验时间：2026-09-03 21:43（America/New_York）。
- 版本核验在本机 PowerShell 完成；没有记录账号、令牌、仓库私有名称或其他身份信息。
- 官方网页资料用公开页面核验，GitHub 合并方式是否显示仍受仓库设置、分支保护和权限影响，文章中的界面截图必须由作者使用可公开展示的测试 PR 补拍。
