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

- [Codex 模型怎么选：推理强度 Low、Medium、High 有什么区别](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [Codex 与 Claude Code 怎么选（2026-10）：GPT-6.1 Sol 对照工作流](./02-Codex与其他编程模型比较.md)
- [Codex 桌面端协作设置，从入口到权限与任务纠偏](./02-Codex桌面端协作设置.md)
- [Codex config.toml 配置指南：配置层级、-c 临时覆盖、Profile 文件和生效检查（0.164.0 实测）](./08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
- [Codex 沙箱与主机权限：一次权限边界风险复盘](./08-Codex沙箱与主机权限风险.md)
- [Codex 任务总跑偏？先检查这 5 个设置](./08-Codex设置检查清单-让任务按预期执行.md)
- [Codex AGENTS.md 怎么写（2026-10 更新）：项目规则继承、验收标准，以及和 Memories、Skills 怎么分工](./09-AGENTS.md怎么写-项目规则继承关系与验收标准.md)
- [Codex 用量额度怎么看：5 小时与每周限制、Fast 倍率和 credits](./10-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)
- [Codex Windows 沙箱配置：启用 MXC 原生隔离，以及 elevated / unelevated 回退](./11-Codex-Windows沙箱-启用MXC与elevated-unelevated回退.md)
- [Codex Daybreak Blue 怎么用：申请 Trusted Access、App 开关与 CLI /daybreak，以及审批后仍被拒时怎么查](./12-Codex-Daybreak-Blue申请开启与排障.md)
- [Codex 自定义模型提供商：model_providers 和 openai_base_url 怎么配，请求到底发去哪（0.164.0 实测）](./13-Codex自定义模型提供商-model_providers与openai_base_url.md)
- [Codex 与 ChatGPT 订阅 API 额度：Pro 和 Business 每月最高 500 美元怎么领，能不能用在 Codex](./16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)
