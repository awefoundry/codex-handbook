# 教程环境与版本记录

> 正文摘要：Windows 11 24H2（26100.4652）；Codex Desktop 26.810.7004.0；Codex CLI 0.147.0；Node.js 22.22.3；skills 1.5.22；img-convert 1.0.4；2026-08-17 核验。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 11 Pro 24H2，构建 26100.4652 | 注册表 `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion` 的 `DisplayVersion`、`CurrentBuild` 和 `UBR` | 2026-08-17 | 注册表的旧兼容字段仍显示 Windows 10 Pro，以 24H2 与 26100 构建号判断实际系统 |
| Codex Desktop | 26.810.7004.0 | `Get-AppxPackage`，包名 `OpenAI.Codex` | 2026-08-17 | 用于安装 Skill、发起任务和展示终端操作 |
| Codex CLI | 0.147.0 | `codex --version` | 2026-08-17 | 用于记录当前 Codex 命令行基线 |
| Skill 安装器 | skills 1.5.22 | `npx -y skills --version` | 2026-08-17 | `npx skills add` 的实际命令版本 |
| 目标插件 / Skill | img-convert，来自 `dutchbase/img-converter` | GitHub 公开仓库根目录 `SKILL.md`，Playwright 与 GitHub API 直接核验 | 2026-08-17 | 通过 `npx skills add` 安装到 Codex；初始化阶段未执行全局安装 |
| Node.js | 22.22.3 | `node --version` | 2026-08-17 | `img-convert` 要求 Node.js 18 或更高版本 |
| npm | 10.9.8 | `npm --version` | 2026-08-17 | 用于安装 `@dutchbase/img-convert` |
| img-convert CLI | 1.0.4 | npm registry `@dutchbase/img-convert/latest`；另用 `npx -y @dutchbase/img-convert@1.0.4 --help` 和单图转换实测 | 2026-08-17 | 本机未为初始化阶段执行全局安装；测试通过 npx 运行固定版本 |
| img-convert Skill 源码 | `fbbd16b0e92d888d3eabc3dee505de1892079eb0`（main） | GitHub commits API 与公开仓库页面 | 2026-08-17 | 仓库 main 会变化，发布文章前应再次核验安装命令与参数 |

## 取值说明

- npm 网页被 Cloudflare 返回 403，页面截图只有安全验证提示，未作为文章素材；包版本、许可证与 Node.js 要求改由 npm registry API 核验。
- GitHub 仓库与 `SKILL.md` 均通过 Playwright 打开、快照并截图检查，页面公开，无账号信息、令牌或二维码。
- 本文初始化阶段没有执行 `npm install -g`，也没有把开源 Skill 安装到用户全局目录；这些步骤留给作者按 `manual-steps.md` 操作和截图。
