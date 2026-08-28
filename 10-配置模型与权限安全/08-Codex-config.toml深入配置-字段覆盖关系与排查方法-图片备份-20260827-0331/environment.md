# 教程环境与版本记录

> 正文摘要核验日期：2026-08-27。仅记录影响教程命令、配置解析或路径示例的组件，不记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 24H2，OS build 26100 | `Get-ComputerInfo`；build 26100 对应 Windows 11 24H2 | 2026-08-27 | 系统 API 的 ProductName 仍可能显示 Windows 10 Pro，本文按 build 记录版本 |
| IDE / 宿主应用 | 不适用 | 本文只演示 CLI 和 PowerShell | 2026-08-27 | 不涉及 IDE 设置界面 |
| Codex | Codex CLI 0.147.0 | `codex --version` | 2026-08-27 | 用于 `config.toml`、Profile、`-c` 和沙箱验证 |
| 目标插件 / App / Connector | 不适用 | 本文不依赖独立插件、App 或 Connector | 2026-08-27 | 不猜测持续部署服务的版本 |
| PowerShell | 7.6.4 | `$PSVersionTable.PSVersion` | 2026-08-27 | 用于 Windows 路径与探针命令 |
| 图片处理 | Python 3.13.5；Pillow 12.3.0 | `python -c "import sys; import PIL; print(sys.version.split()[0]); print(PIL.__version__)"` | 2026-08-28 | 用于按 imagegzh 一号样式生成正文配图，不覆盖原始终端截图 |
| 配置参考 | OpenAI Codex 官方文档（页面于 2026-08-27 读取） | `https://developers.openai.com/codex/config-file/config-reference` | 2026-08-27 | 字段和值随 CLI 版本变化，发布前应重新核对 |
| 封面生成 | ZimaCode GPT Image 2；`engine=web`；`gpt-image-2-text-to-image` | `D:\CodexHome\skills\zimacode-gpt-image-2\scripts\zimacode-gpt-image-2.mjs` | 2026-08-28 | 任务 ID 见处理报告；仅记录服务与模型，不记录 API Key |

## Windows 本机截图基线

本机截图阶段使用 `manual/prepare-windows-capture.ps1 baseline` 记录当前 Windows 电脑上的 `CODEX_HOME`、Codex CLI 版本和 `config.toml` 存在性。当前已在 Windows Terminal 中核验 Codex CLI `0.147.0`，`config.toml` 状态为 `present`；截图命令不会读取配置文件内容，也不修改真实配置。只读探针截图完成后，已补充最终封面：`正文配图/封面.png`，1672 × 941，16:9 目标比例偏差约 0.06%；封面为 ZimaCode 生成原图，未做程序叠字。
