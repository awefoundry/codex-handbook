# MCP 与外部工具

讲清楚 Codex 如何连接外部数据和服务，以及连接后产生的权限边界。

## 内容范围

- MCP 的作用和基本工作方式。
- STDIO 与 Streamable HTTP。
- OAuth、Bearer Token 和环境变量。
- 项目级与全局 MCP 配置。
- 工具范围、审批策略和超时设置。
- Notion、GitHub、文档、浏览器等连接实操。
- 连不上、没有工具和认证失败的排查方法。

## 已收入文章

- [Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界](./01-Codex-MCP入门-config与mcp-login.md)
- [Codex 常用 MCP 推荐：官方列出的 7 个 MCP 服务器怎么选](./02-Codex常用MCP服务器推荐-官方示例7个怎么选.md)
- [Codex MCP 排障：服务器连不上、工具不显示、OAuth 登录失败](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)
- [Codex 代码智能 MCP 实测：Serena 和 codebase-memory-mcp 怎么装、怎么选](./04-Codex代码智能MCP-Serena与codebase-memory-mcp怎么装怎么选.md)
- [Codex Site tools（WebMCP）入门：网站怎么把操作交给内置浏览器里的 Codex，以及怎么给自己的网站加工具](./05-Codex-Site-tools-WebMCP网站工具入门.md)

## 已上线文章

- [Codex 接入 Chrome DevTools MCP：让 Codex 读控制台、网络请求和性能轨迹（1.12.0 实测）](./06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)
- [Codex 安装第三方 Skill 前先扫描：用 NVIDIA SkillSpector 查提示注入和数据外泄](./07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)
- [Codex 安装 OpenAI Developers 插件：安全创建 API Key、写入 .env.local 与排查 API 报错](./08-Codex安装OpenAI-Developers插件-创建API-Key与排查API报错.md)
- [Codex 安装 agent-skills 插件：用 codex plugin 装上 Addy Osmani 的 25 个工程 Skill](./09-Codex安装agent-skills插件-25个工程Skill怎么用.md)
- [Codex 安装 Google EGM 插件：先写设计文档，再让零上下文子代理审稿](./10-Codex安装Google-EGM插件-设计文档与子代理审稿.md)
- [Codex 接入 Mobile MCP：让 Codex 操作 iOS 模拟器、Android 模拟器和真机](./11-Codex接入Mobile-MCP-操作iOS模拟器与Android设备.md)（第三方项目 mobile-next/mobile-mcp，不是 OpenAI 官方服务器）
- [Codex 安装 Trail of Bits 安全插件：用 patching-bugs 和 regression-hunt 复现漏洞、写补丁、查回归](./12-Codex安装Trail-of-Bits插件-patching-bugs与regression-hunt.md)
- [Codex 安装 Unity 官方插件：用 Skills 和 unity-cli 辅助开发](./13-Codex安装Unity插件-用Skills辅助Unity开发.md)
- [Codex 用 OpenAI Developers 插件 Showcase：周末 starter 项目，以及 Pro／Business 怎么领取 API 额度](./14-Codex-OpenAI-Developers插件Showcase与领取API额度.md)
- [Codex 安装 Heptabase 插件：在对话里打开白板，读写卡片、Journal 与思维导图](./15-Codex安装Heptabase插件-对话内打开白板与知识卡片.md)（第三方插件，Heptabase 帮助中心；本文没有 Heptabase 账号）
- [Codex 安装 Google 官方 Skills 与插件：google/skills 仓库的 BigQuery、Cloud SQL、Firestore 等 17 个插件怎么装](./16-Codex安装Google官方Skills与插件-google-skills仓库.md)（Google 维护的 google/skills，Apache-2.0。android/skills 与 EGM 各有专文）
- [Codex 安装 Blender Agent Skills：用 28 个技能做建模、绑定、动画与游戏引擎导出](./17-Codex安装Blender-Agent-Skills-建模绑定动画与引擎导出.md)（第三方项目 EL4CTEO/blender-skills，MIT；本文未在 Blender 中实测）
