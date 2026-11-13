# 配置、模型与权限安全

集中说明 Codex 的配置入口、模型选择和执行边界。

## 内容范围

- config.toml 的位置、优先级和常用字段。
- 模型、推理强度、输出详细程度和配置 profile。
- 身份认证和凭据保存方式。
- 沙箱模式、审批策略和目录权限。
- 网络访问、搜索和外部连接。
- Token、密钥和敏感文件保护。
- 个人、项目和团队配置的区别。

## 已上线文章

- [Codex 模型怎么选：GPT-6.1 Sol、Terra、Luna、Astra 和推理强度](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [Codex 与 Claude Code 怎么选（2026-10）：GPT-6.1 Sol、Terra 对照工作流](./02-Codex与其他编程模型比较.md)
- [Codex 桌面端设置怎么调（2026-11 更新）：权限模式、个人指令与 Memories、Follow-up behavior](./03-Codex桌面端协作设置.md)
- [Codex config.toml 配置指南：配置层级、-c 临时覆盖、Profile 文件和生效检查（0.164.0 实测）](./04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
- [Codex 沙箱与主机权限风险（2026-11 更新）：git show 白名单逃逸复盘，和现在怎么用权限、Rules、Hooks 防](./05-Codex沙箱与主机权限风险.md)
- [Codex AGENTS.md 怎么写（2026-10 更新）：项目规则继承、验收标准，以及和 Memories、Skills 怎么分工](./07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)
- [Codex 用量额度怎么看：5 小时与每周限制、Fast 倍率和 credits](./08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)
- [Codex Windows 沙箱配置：启用 MXC 原生隔离，以及 elevated / unelevated 回退](./09-Codex-Windows沙箱-启用MXC与elevated-unelevated回退.md)
- [Codex Daybreak Blue 怎么用：申请 Trusted Access、App 开关与 CLI /daybreak，以及审批后仍被拒时怎么查](./10-Codex-Daybreak-Blue申请开启与排障.md)
- [Codex 自定义模型提供商：model_providers 和 openai_base_url 怎么配，请求到底发去哪（0.164.0 实测）](./11-Codex自定义模型提供商-model_providers与openai_base_url.md)
- [Codex 使用 GPT-6.1 Terra：适合哪些任务、怎么切换，额度比 Sol 多多少](./14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md)
- [Codex 防范 AGENTS.md 投毒：别在 Downloads 目录启动，5 分钟自查 config.toml 和 MCP](./15-Codex防范AGENTS.md投毒-Downloads目录风险与config.toml自查.md)
- [Codex 与 ChatGPT 订阅 API 额度：Pro 和 Business 每月最高 500 美元怎么领，能不能用在 Codex](./16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)
- [Codex 用量上调：Pro 100 和 Pro 500 翻倍、Pro 200 取消降额、Business Premium 也在内，怎么确认你的额度变了](./17-Codex用量上调-Pro100与Pro500翻倍-Pro200取消降额.md)
- [Codex 网页搜索设置：cached、indexed、live、disabled 怎么选，--search 单次联网，allowed_domains 限定站点](./18-Codex网页搜索设置-cached-indexed-live与allowed_domains.md)
- [Codex IDE 扩展安全自查：Cursor 扩展市场出现 Claude Code 后门后，怎么确认你装的是官方 openai.chatgpt](./19-Codex-IDE扩展安全自查-确认官方openai.chatgpt与扩展投毒防范.md)
- [Codex 和 ChatGPT 用量合并：12 月起 Plus、Pro、Business 共用额度](./20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md)
- [Codex 内置浏览器本地文件读取风险：EMBRACE 漏洞修复前，别打开不可信的本地 HTML](./21-Codex内置浏览器本地文件读取风险-EMBRACE自查与防护.md)
- [Codex 插件和 Hook 自查：第三方应用自动安装后，怎么查 config.toml、信任记录和 MCP](./22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)
- [Codex 对话会被用来训练吗：Improve the model、Include environments 和例外情况](./23-Codex对话会被用来训练吗-数据控制与Include-environments.md)
- [Codex 用 GPT-6 Cyber 与 Daybreak Red：准入、和 Astra / Blue 的分工，以及安全研究边界](./24-Codex用GPT-6-Cyber与Daybreak-Red-准入与边界.md)
- [Codex 套餐用在第三方工具：Sign in with ChatGPT 连接 OpenCode、Kilo Code、Warp 等，额度怎么算、怎么限额](./25-Codex套餐用在第三方工具-Sign-in-with-ChatGPT与App-limits.md)
- [Codex 网络权限怎么配：permission profiles 的联网开关、network_proxy 域名白名单与本地服务访问](./26-Codex网络权限-network_proxy域名白名单与本地服务访问.md)
- [Codex 常驻 Agent 怎么上锁：照 OpenAI 内部 OpenClaw 部署配 requirements.toml、权限 profile 与 Auto-review](./27-Codex常驻Agent安全加固-照OpenAI的OpenClaw部署配requirements.toml与权限profile.md)
- [Codex 内置浏览器企业策略：用 MDM 下发 Chrome 策略，Windows、macOS、Linux 三种位置与 chrome://policy 核对](./28-Codex内置浏览器企业策略-用MDM下发Chrome策略并在chrome-policy核对.md)
