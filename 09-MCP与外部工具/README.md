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

- [Codex MCP 入门：config.toml、/mcp login、Docs MCP 与权限边界，补上 OAuth 客户端注册、远程环境、插件自带 MCP 和服务器 instructions](./01-Codex-MCP入门-config与mcp-login.md)
- [Codex 常用 MCP 推荐：官方列出的 7 个 MCP 服务器怎么选](./02-Codex常用MCP服务器推荐-官方示例7个怎么选.md)
- [Codex MCP 排障：服务器连不上、工具不显示、OAuth 登录失败](./03-Codex-MCP排障-连不上-没有工具与OAuth登录失败.md)
- [Codex 代码智能 MCP 实测：Serena 和 codebase-memory-mcp 怎么装、怎么选](./04-Codex代码智能MCP-Serena与codebase-memory-mcp怎么装怎么选.md)
- [Codex Site tools（WebMCP）入门：网站怎么把操作交给内置浏览器里的 Codex，以及怎么给自己的网站加工具](./05-Codex-Site-tools-WebMCP网站工具入门.md)

## 已上线文章

- [Codex 接入 Chrome DevTools MCP：读控制台、网络请求和性能轨迹，再装官方 7 个 Skills 和 chrome-devtools CLI](./06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)
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
- [Codex 用 agent-browser 做浏览器自动化：Skill 和 MCP 两种接法，snapshot 引用与常用命令](./18-Codex用agent-browser做浏览器自动化-Skill与MCP两种接法.md)（第三方项目 vercel-labs/agent-browser，不是 OpenAI 官方浏览器）
- [Codex 安装 Expo 官方插件：Expo Skills 与 Expo MCP 一次装好，开发和发布 React Native 应用](./19-Codex安装Expo官方插件-Expo-Skills与Expo-MCP.md)
- [Codex Security 插件教程：在 Security 工作台扫描本地仓库、生成补丁并验证修复](./20-Codex-Security插件-Security工作台扫描本地仓库与修复验证.md)
- [Codex 安装 Microsoft 官方 .NET Skills：把 dotnet/skills 加进插件市场，按需安装测试、MSBuild、Blazor 和 MAUI 等插件](./21-Codex安装Microsoft官方NET-Skills-dotnet-skills仓库.md)（dotnet 组织的 dotnet/skills，MIT；市场清单 16 个，另有未列入的 dotnet-experimental。本文没有执行安装）
- [Codex 安装 context-mode 插件：把大段命令输出挡在上下文之外，附 hooks 信任步骤和 ELv2 许可证说明](./22-Codex安装context-mode插件-把大段工具输出挡在上下文之外.md)（第三方项目 mksglu/context-mode，ELv2。Codex CLI 0.169.0 上装过插件并信任 hooks；没有登录会话，没有配图。21 仍空着）
- [Codex 安装 Plannotator：在浏览器里批注计划和代码审查，用 Stop hook 把反馈送回 Codex](./23-Codex安装Plannotator-浏览器批注计划与代码审查并回传反馈.md)（第三方项目 backnotprop/plannotator，Apache-2.0。没有执行安装脚本，没有配图）
- [Codex 安装 Floorplan 插件：让 Codex 把整个代码库画成可点击的架构地图，还能做密钥与权限健康检查](./24-Codex安装Floorplan插件-把代码库画成可点击的架构地图并做健康检查.md)（第三方项目 haydenschmitty/floorplan，MIT。Codex CLI 0.169.0 上未登录安装了 0.11.0，没有打开地图界面）
- [Codex 安装 Stop That Shit（别再造史了）：用 Skill 和 Hook 拦住 Codex 的范围膨胀、无用防御和越权修改](./25-Codex安装Stop-That-Shit-用Skill和Hook拦住范围膨胀与无用防御.md)（第三方项目 lennney/stop-that-shit，MIT，固定 tag 0.2.5。未登录核对了 Hook 清单，没有打开 /hooks 信任界面）
- [Codex 安装 Obsidian 官方 Skills：让 Codex 读写 Markdown、Bases 和 Canvas，还能调用 Obsidian CLI](./26-Codex安装Obsidian官方Skills-Markdown-Bases-Canvas与Obsidian-CLI.md)（Obsidian 维护的 obsidian-skills，MIT。CLI 0.169.1 上装过插件，没有在 Obsidian 里改过库）
- [Codex 安装 graphify：把代码库变成可查询的知识图谱，用 $graphify 建图，再用 query、path、explain 代替 grep](./27-Codex安装graphify-把代码库变成可查询的知识图谱.md)（第三方项目 Graphify-Labs/graphify，Apache-2.0，PyPI 包名 graphifyy。Linux 上装了 0.9.115，并对一个小例子建过图。没有打开 Codex 会话）
- [Codex 安装 UI UX Pro Max Skill：用 uipro init --ai codex 装进项目，按产品类型生成设计系统再写界面](./28-Codex安装UI-UX-Pro-Max-Skill-按产品类型生成设计系统再写界面.md)（第三方项目 nextlevelbuilder/ui-ux-pro-max-skill，MIT。CLI 0.171.0 上装过 npm 模板和插件市场，没有在会话里生成界面。27 仍空着）
- [Codex 安装 Marketing Skills 插件：用 codex plugin marketplace add 装好营销 Skills，改落地页、写文案和做 SEO 审计](./29-Codex安装Marketing-Skills插件-用plugin-marketplace装好营销Skills改落地页写文案做SEO审计.md)（第三方项目 coreyhaines31/marketingskills，MIT。CLI 0.172.0 上装过 marketing-skills 2.14.28，列出 53 个 Skill。没有在会话里改页面，没有配图）
