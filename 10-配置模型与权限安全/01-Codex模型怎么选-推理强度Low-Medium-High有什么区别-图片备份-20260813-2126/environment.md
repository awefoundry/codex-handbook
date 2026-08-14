# 教程环境与版本记录

> 在正文开头填写“本教程环境”表。本文件保留版本取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 24H2（OS Build 26100.4652） | `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion` 的 `DisplayVersion`、`CurrentBuild`、`UBR` | 2026-08-14 | 注册表 `ProductName` 仍显示 Windows 10 Pro；正文采用公开产品名称与精确构建号 |
| IDE / 宿主应用 | Codex Windows 桌面端 26.803.10989.0 | 运行中进程路径 `WindowsApps/OpenAI.Codex_26.803.10989.0_x64...` | 2026-08-14 | 本文以桌面端为主；IDE 不适用 |
| Codex | 桌面端 26.803.10989.0；CLI 0.146.1 | 应用包路径；`codex --version` | 2026-08-14 | 必须区分桌面端 Light 与 CLI Low 的命名 |
| 目标插件 / App / Connector | 不适用 | 文章主题不依赖插件、App 或 Connector | 2026-08-14 | 无第三方认证或独立版本 |
| 其他关键依赖 | OpenAI Codex Models：Web 托管版本 | `https://developers.openai.com/codex/models`，Jina Reader 读取并由 Playwright 打开核验 | 2026-08-14 | 模型列表、默认值和界面均可能变化，发布前复核 |

## 取值命令与证据

```powershell
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' |
  Select-Object ProductName, DisplayVersion, CurrentBuild, UBR

codex --version

Get-Process | Where-Object { $_.ProcessName -match 'Codex' } |
  Select-Object ProcessName, Path
```

- 官方文档直接核验：`https://developers.openai.com/codex/models`
- 核验时官方页面说明：桌面端最低档名为 Light，CLI 为 Low；Medium 为常用平衡起点，高档位会增加耗时与 token 使用。
- 未记录任何账号、密钥、许可证或私人工作区名称。
