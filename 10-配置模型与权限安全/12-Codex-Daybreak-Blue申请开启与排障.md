---
id: codex-daybreak-blue
title: Codex Daybreak Blue 怎么用：申请 Trusted Access、App 开关与 CLI /daybreak，以及审批后仍被拒时怎么查
seo_title: Codex Daybreak Blue：申请、App 开关、CLI /daybreak 与排障
description: Daybreak 是 OpenAI 面向授权网络安全工作的 Trusted Access 计划。本文按 Help Center 说明个人申请 Daybreak Blue 要准备什么、在 Codex App 和 CLI 里怎么打开、管理员要开哪些开关，以及审批后仍看到安全提示时怎么逐项排查。
lede: 批下来不等于已经生效。账号、工作区、开关、模型四样对上，Daybreak Blue 才会在请求里起作用。
url: /guides/codex-daybreak-blue
status: draft
section: guides
category: F-config-model-security
topic: 配置模型与权限安全
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 12
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-23
date_modified: 2026-10-23
models: [gpt-6-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview
keywords: [Codex Daybreak, Daybreak Blue, Trusted Access for Cyber, Codex /daybreak, chatgpt.com/cyber]
related: [codex-model-reasoning-effort]
faq:
  - q: 个人能申请 Daybreak Red 吗？
    a: 不能。官方写明 Red 目前只对获批的企业和组织开放，个人申请通道只能申请 Blue，Blue 获批也不包含 Red。
  - q: 批下来之后为什么在 Codex 里没有任何变化？
    a: 审批本身不会打开降拒绝。Codex 用 ChatGPT 登录时，要在高级模型选择器里把 Daybreak 开关打开（默认关）；工作区成员还需要管理员在角色里开启 Daybreak Blue。
  - q: 用 Astra 为什么还是会被拒？
    a: 官方说明 Daybreak Blue 下 Astra 仍走标准防护，降拒绝目前只对 Red 开放。Blue 用户可以换 GPT-6 Sol 或 GPT-6 Luna。
---

# Codex Daybreak Blue 怎么用：申请 Trusted Access、App 开关与 CLI /daybreak，以及审批后仍被拒时怎么查

> 本文计划路径：[codexguide.io/guides/codex-daybreak-blue](https://codexguide.io/guides/codex-daybreak-blue)

> 核对依据：OpenAI Help Center《OpenAI Daybreak - Trusted Access for Cyber overview》和《Troubleshooting OpenAI Daybreak》，2026-10-23 核对。本文只讲授权防御场景下的申请与开关，不涉及 Daybreak Red 的使用，也不讨论任何攻击性操作。

做安全工作的人用 Codex，常碰到一种情况：明明是在审自己公司的代码、分析自己环境里抓到的样本，模型却按通用防护把请求拒了。Daybreak 就是 OpenAI 为这类场景准备的 Trusted Access 计划。

OpenAI 的 Tibo（@thsottiaux）在 10 月 22 日的一条帖子里提醒大家提前申请，原话是「只要 15 分钟，别等到事故当中再弄」。15 分钟是他的个人说法，官方文档没有给出审核时长，只说最终开通时间取决于审核和配置流程。

## Daybreak 是什么

Daybreak 是 OpenAI 的 Trusted Access for Cyber 计划，下面分 Blue 和 Red 两个访问层级。官方的定位是：给通过审核的企业和安全从业者，在**自己拥有、运营或明确获得授权**的系统上做防御工作时，减少不必要的拒绝。使用政策和其他防护仍然有效。

| 层级 | 官方说明（摘要） | 适合 |
| --- | --- | --- |
| 标准（未开启） | 主线模型，标准防护 | 威胁建模、安全代码审查与修补等通用工作 |
| Daybreak Blue | 在 GPT-5.5、GPT-5.6 Sol、GPT-6 Sol、GPT-6 Luna 等主线模型上减少拒绝；Astra 仍走标准防护；不含网络安全专用模型 | 漏洞分级、安全代码审查、恶意软件分析、检测工程、事件响应、补丁验证 |
| Daybreak Red | 需单独审批、更严格的验证和访问控制，仅对获批企业和组织开放 | 本文不展开 |

官方建议多数安全团队从 Blue 开始。下文也只讲 Blue。

还要说明几件 Daybreak **不做**的事（官方原文列出的）：

- 不会去掉全部防护或全部拒绝，也不会默认对所有模型生效；
- 不默认附带 Zero Data Retention；
- 不允许转售、代理、嵌入，或开放给第三方客户和外部用户；
- 不授权你在没有权限的系统上做任何事。

## 谁该申请

适合申请的是在本职工作里做防御安全的人：AppSec、检测工程、应急响应、漏洞管理。对象必须是你自己的系统，或者你有明确书面授权去测试、分析的系统。

不该申请或不该打开的情况：

- 面向客户的应用、下游产品流量、给第三方用的工作流。官方明确不允许把 Daybreak 开给这些场景；
- 想测别人的系统但没有授权；
- 指望买个合同就能拿到。官方写明商业协议或采购本身不保证获得访问。

另外，个人申请者必须年满 18 岁；官方也说明 Daybreak 不是所有地区都提供。

## 个人申请 Blue：准备清单

官方要求个人申请需要**符合条件的付费套餐**、**Advanced Account Security（高级账户安全）**，以及**至少一把兼容的实体 FIDO2 硬件密钥**。软件 passkey 或同步到密码管理器里的 passkey 不算数。已有个人访问的用户需要在 2026-10-01 前满足这些要求才能保留访问。

步骤（按官方流程整理）：

1. 打开 [chatgpt.com/cyber](https://chatgpt.com/cyber)，登录你打算使用的账号，选择 **Set up Daybreak**。
2. 按提示开启 Advanced Account Security：至少登记两种安全登录方式，其中一种要能跨设备使用；为了 Daybreak，至少要有一把实体 FIDO2 硬件密钥。
3. 保存恢复密钥并重新登录。首次开启 Advanced Account Security 会把你从所有设备登出。开启后，密码登录、邮件和短信验证码登录、普通邮件找回都会被停用。
4. 回到 chatgpt.com/cyber，补完剩余的套餐或安全要求，按提示完成身份验证。
5. 进入 **Set up your Daybreak keys**，选择用于 Daybreak 的硬件密钥。这一步和第 2 步登记登录方式是分开的。一把必选，第二把可选。
6. 查看申请状态，按页面提示处理。完成安全设置和身份验证并不保证获批。

开始前读一遍官方的 Advanced Account Security 说明。这个设置会改变你的登录和找回方式，丢了所有登录方式和恢复密钥，账号可能就找不回来了。官方建议另外备一把硬件密钥，恢复密钥放在安全的地方。

几个常见卡点：

- **TrustKey T110 和 T120** 目前不能用于个人 Daybreak。
- 企业托管账号、已验证并认领域名下的账号，不能开启 Advanced Account Security。
- 加入了 Business 或 Team 工作区，不代表可以免除个人的安全和硬件密钥要求。

## 在 Codex App 里打开

审批通过后，Codex 里不会自动出现变化，因为 Daybreak 默认是关的。

用 ChatGPT 登录 Codex App 时：

- 在**高级模型选择器**里找到 **Daybreak 开关**，发请求之前打开。开关关着时，请求按标准防护处理。
- 版本要求：用 ChatGPT 登录需 **26.908.40834** 或更高；用 API Key 登录需 **26.1013.0** 或更高。
- 想确认工作区管理员有没有给你开权限，可以看 **Settings → General** 里的 **Daybreak Access**。

用 API Key 登录 Codex 时情况不同：访问跟着 API 项目走，不会出现专门的 Daybreak 界面，需要显式选择已获批的模型。

## 在 Codex CLI 里打开

- 交互会话里输入 `/daybreak`；
- 无头命令或配置里用 `daybreak=true`；
- CLI 需要升级到 **0.163.0**。

官方还提到，如果工作流固定在更老的 CLI 版本上，Daybreak 对支持的请求默认是开的。升级以后改成显式开启，这一点在自动化脚本里要留意。

用 API Key 登录 CLI 时，官方示例是 `codex -m gpt-6-sol`，并强调 `gpt-` 前缀不能省。

## 管理员要开什么

### ChatGPT 工作区（Codex 用 ChatGPT 登录）

1. 管理员打开 **Roles**，对目标角色选 **Edit override**，或用 **Add role override** 新建一个。
2. 在 **Cybersecurity** 下把 **Daybreak Blue** 设为 On，保存。
3. 生效大约需要 10 分钟。

官方建议在工作区默认设置里保持 Daybreak 关闭，只给需要的角色打开。

### API 项目

1. 由 **API 组织所有者**（项目所有者不够）打开目标项目，注意必须是**非默认项目**，默认项目不支持 Daybreak。
2. 在 **Project settings → General** 的 **Daybreak model access** 里打开获批的层级，保存。
3. 生效大约需要 15 分钟。用该项目的 API Key 发请求。

如果你的组织同时服务面向客户的 API 流量，官方建议只在内部项目上打开。

## 审批后仍被拒：按这个顺序查

1. **工作区和账号**：是不是在获批的组织或工作区里？登录方式是不是批准时指定的那种？
2. **开关**：App 里的 Daybreak 开关打开了吗？CLI 里用了 `/daybreak` 吗？Settings → General 里能看到 Daybreak Access 吗？
3. **管理员配置**：角色 override 或项目设置是否已保存，过了 10～15 分钟没有？
4. **模型**：用的是 Blue 支持降拒绝的模型吗？Astra 和 GPT-6.1-Sol 在 Blue 下仍是标准防护，可以换成 GPT-6 Sol 或 GPT-6 Luna。
5. **版本**：App 和 CLI 是否满足上面的版本要求。
6. **请求本身**：Daybreak 只减少部分拒绝。请求看起来高风险、超出普通防御用途、意图不明确时，仍会看到安全提示，比如请求被限制、被转到备用模型，API 里则是 `cyber_policy` 错误。

确认都没问题、请求明显是防御性质却仍被挡住，再联系 Support。官方建议附上：准确的提示原文、使用的模型、产品界面（ChatGPT、Codex 还是 API）、时间戳和时区、能拿到的 request ID，以及一段打码后的任务描述，并说明目标系统是否归你所有或已获授权。

不要发送密钥、私钥、攻击目标或第三方机密数据。Support 也不能推翻身份验证的结论。

## 小结

| 检查项 | 位置 |
| --- | --- |
| 个人资格 | chatgpt.com/cyber → Your eligibility |
| App 开关 | 高级模型选择器 → Daybreak（默认关） |
| CLI | `/daybreak` 或 `daybreak=true`，CLI ≥ 0.163.0 |
| 工作区权限 | Roles → override → Cybersecurity → Daybreak Blue |
| API 项目 | Project settings → General → Daybreak model access（非默认项目） |
| 模型 | Blue 下用 GPT-6 Sol / GPT-6 Luna；Astra 仍为标准防护 |

## 相关阅读

- [Codex 沙箱与主机权限风险](./08-Codex沙箱与主机权限风险.md)
- [权限、沙箱和审批](https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi)
- [Codex 模型和推理强度怎么选](https://codexguide.io/guides/codex-model-reasoning-effort)

## 参考

- [OpenAI Daybreak - Trusted Access for Cyber overview](https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview)
- [Troubleshooting OpenAI Daybreak](https://help.openai.com/en/articles/20001259-troubleshooting-openai-daybreak)
- [申请入口 chatgpt.com/cyber](https://chatgpt.com/cyber)
- [Tibo 的提醒帖（X）](https://x.com/thsottiaux/status/2113162277688070445)
