# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11，OS Build 26100 | `Get-ComputerInfo -Property WindowsProductName,WindowsVersion,OsBuildNumber` | 2026-08-20 | 本文涉及终端、编辑器和文件系统行为 |
| IDE / 宿主应用 | 不适用 | 本文流程以 Codex Desktop/CLI 和终端为主 | 2026-08-20 | 不把 IDE 作为必需前置条件 |
| Codex Desktop | 26.814.5517.0 | Windows 应用进程路径 `OpenAI.Codex_26.814.5517.0` | 2026-08-20 | 负责对话、任务记录和工作区操作 |
| Codex CLI | 0.147.0 | `codex --version` | 2026-08-20 | 用于命令行示例和测试命令承载 |
| 目标插件 / App / Connector | 不适用 | 本文没有指定插件、连接器或第三方 App | 2026-08-20 | 不猜测不存在的版本号 |
| Node.js / npm | Node.js v22.22.3；npm 10.9.8 | `node --version`、`npm --version` | 2026-08-20 | 仅用于本地工具环境核验，不是文章必需依赖 |
| Python | Python 3.13.5，可直接调用 `python` 与 `python3` | Codex 工作区执行 `Get-Command python,python3` 和 `where.exe python` | 2026-08-21 | 已用于运行 `temp/workflow-demo` 的 `unittest`；此前截图记录的是 2026-08-20 的不可用状态 |
| 图片处理运行时 | Python 3.13.5；Pillow 12.3.0 | 当前处理终端执行 `python --version` 与 `import PIL; PIL.__version__` | 2026-08-20 | 仅用于按 imagegzh 一号样式生成公众号配图，不代表文章项目运行时 |
| HIAPI 配图生成 | `hiapi-icon-skills` 0.2.0；Codex 内置 `image_gen` | `D:\CodexHome\skills\hiapi-icon-skills\package.json`、本轮任务预览与生成记录 | 2026-08-21 | 生成正文开头四类工作流总览图；无账号、密钥或任务凭据写入 |
| 文章仓库 | 本地公开示例仓库，提交号待实操时记录 | 由作者在截图前执行 `git rev-parse --short HEAD` | 2026-08-20 | 不记录私人路径、远程凭据或账号信息 |
