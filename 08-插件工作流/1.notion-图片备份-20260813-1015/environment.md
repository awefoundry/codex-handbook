# 教程环境与版本记录

核验日期：2026-08-13

| 项目 | 版本/状态 | 获取方式或来源 | 适用性/备注 |
|---|---|---|---|
| 操作系统 | Windows 11 专业版 64 位；版本 `10.0.26100`；构建 `26100` | PowerShell `Get-CimInstance Win32_OperatingSystem` | 本机实测环境 |
| Codex 桌面端 | `26.803.10989.0` | PowerShell `Get-AppxPackage OpenAI.Codex` | Notion 插件工作流的宿主 |
| Notion 插件 | 目录托管版本；公开页面与当前界面未展示独立语义版本号 | [OpenAI Notion 插件页](https://openai.com/business/plugins/notion/) 与 Plugins 目录 | 不猜测版本；后续截图需保留插件详情状态 |
| Notion App / Connector | Web 托管版本；未展示独立语义版本号 | [OpenAI Notion 同步说明](https://help.openai.com/en/articles/12532955-notion-app-with-sync) 与 OAuth 授权界面 | 权限可能受套餐、地区、角色和管理员策略影响 |
| Codex CLI | `0.146.1` | `codex --version` | 此教程不通过 CLI 操作，仅记录本机环境 |
| IDE | VS Code `1.132.1` | `code --version` | 此教程不通过 IDE 操作，正文明确标记不适用 |

本次调整的可复现命令基线：PowerShell `5.1.26100.4652`，Node.js `v22.22.3`，npm `10.9.8`，Python `3.13.5`。ImageMagick `magick` 未检测到，因此本次没有用它做图片尺寸或透明通道验证。

## 后续复核

- [ ] 正式截图当天重新执行版本命令，并更新正文核验日期。
- [ ] 在 Codex 桌面端记录 About 或 Windows 应用信息中的版本。
- [ ] 打开 Notion 插件详情；若界面仍无独立版本号，保留“目录托管版本”表述。
- [ ] 检查 Plugins 与 Notion 授权页面是否出现套餐、地区或管理员限制。
- [ ] 不记录账号邮箱、设备名、工作区名称、成员、许可证或授权令牌。
