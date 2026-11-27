---
id: codex-auto-review
title: "Codex Auto-review 怎么用：哪些审批会交给审阅者、会拦什么、看得到什么，被拒绝后怎么重试，怎么调策略"
seo_title: "Codex Auto-review：哪些审批交给审阅者、被拒后怎么重试"
description: "Auto-review 把仍要交互审批的请求交给独立审阅 agent，不扩大沙箱。本文按官方文档说明何时生效、Approve for me 与 approvals_reviewer 怎么开、会审和会拦什么、被拒绝后如何重试，以及策略怎么替换。"
lede: "换的是谁来审，不是代理能做什么。沙箱、命令规则和工具设置仍然决定哪些动作要停下来问。"
url: /guides/codex-auto-review
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 33
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-27
date_modified: 2026-11-27
verified_on: 2026-11-27
official_ref: https://learn.chatgpt.com/docs/sandboxing/auto-review
keywords: [Codex Auto-review, Codex Approve for me, Codex approvals_reviewer, Codex 自动审批, Codex /approve]
related: [permissions-sandbox-approvals, codex-rules-prefix-rule, codex-persistent-agent-hardening, codex-sandbox-host-trust, codex-sandbox-command]
howto: true
faq:
  - q: "选了 Approve for me，是不是就等于 Full access？"
    a: "不是。Permissions 页写明，换谁来审不会扩大沙箱。Approve for me 和 Ask for approval 用同一套工作区边界，只是把越界请求交给自动审阅。Full access 在 Sandbox 页写成 sandbox_mode = \"danger-full-access\" 再加上 approval_policy = \"never\"。"
  - q: "只把 approval_policy 改成 on-request，Auto-review 会不会自动打开？"
    a: "不会。官方页写明，只改审批策略不会选定审阅者。CLI 或本地配置还要设 approvals_reviewer = \"auto_review\"。桌面端要在当前对话的权限控件里选中 Approve for me。"
  - q: "审阅者拒绝之后，能不能换一条命令绕过去？"
    a: "官方页要求主 agent 不要用变通、间接执行或绕过策略去追求同一个结果。只能改走实质更安全的方案，否则停下问用户。拒绝不当成普通沙箱错误。"
  - q: "审阅超时，是不是说明这个动作不安全？"
    a: "不能这么判断。官方页把超时和明确拒绝分开，并写明主 agent 会被告知：仅凭超时不能证明动作不安全。"
---

# Codex Auto-review 怎么用：哪些审批会交给审阅者、会拦什么、看得到什么，被拒绝后怎么重试，怎么调策略

> 本文在线版：[codexguide.io/guides/codex-auto-review](https://codexguide.io/guides/codex-auto-review)

> 核对依据：2026-11-27 打开的 [Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)、[Permissions](https://learn.chatgpt.com/docs/permission-modes)、[Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)、[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) 里的 Configure Auto-review policy，以及 [Sandbox](https://learn.chatgpt.com/docs/sandboxing)。没有登录桌面端，没有打开 CLI 的交互界面。文中的配置片段都来自 Auto-review 页原文。

沙箱管边界，审批管要不要问人，Auto-review 只换审阅者。权限、沙箱和审批怎么放行或收紧，见 [权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。命令前缀规则见 [Codex Rules](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)。

## 先说结论：换的是谁来审，不是能做什么

Auto-review 把符合条件的审批请求交给一个独立的审阅 agent。审阅者决定这个动作能不能继续，并返回理由。

它不改沙箱能碰什么。Permissions 页写明：换谁来审不会扩大沙箱。**Approve for me** 和 **Ask for approval** 保持同一套工作区边界，差别是越界请求交给自动审阅，而不是停下来等你点。

哪些动作需要审批，仍由沙箱、命令规则和工具设置决定。已经有权限的动作直接执行，不经过审阅。

## 什么时候才生效

Auto-review 只在审批仍然是交互式的时候生效。官方页写的实际情况是：

- `approval_policy = "on-request"`，或
- 细粒度审批策略仍会弹出相应类别的提示。

`approval_policy = "never"` 时，没有可审的请求。

同一页还写：若使用 `approval_policy = "never"`、`:danger-full-access` 或 `--yolo`，动作可以避开审阅所需要的那一次越界审批请求。授权安全工作的示例里，官方要求保持 `on-request` 或另一种仍会交互的审批策略，并保留可执行的沙箱边界。

Sandbox 页把两个常见审批策略写成：`on-request` 时代理默认在沙箱里工作，要越界才问；`never` 时不再为审批停下来。交互式审批下，还可以用 `approvals_reviewer` 选择审阅者：`user` 是默认，提示交给用户；`auto_review` 把符合条件的提示交给审阅 agent。

## 怎么打开

桌面端和 CLI 不是同一个开关。

**ChatGPT 桌面端**：在输入框下方的权限控件里选 **Approve for me**，并确认当前这条对话确实选中了它。Permissions 页写明，某个模式在菜单里出现，不等于当前对话已经用上。组织要求也可以把这个模式关掉或拿掉。看不到或是灰色时，官方把排障指到 permission troubleshooting，本文没有另开那一页。

**CLI 或本地配置**：在仍然交互的审批策略上设置审阅者。官方示例是和 `approval_policy = "on-request"` 一起写：

```toml
approvals_reviewer = "auto_review"
```

只改 approval policy，不会选定审阅者。

**管理员可以强制**。Managed configuration 写：要让 Auto-review 成为默认，在 **Global** > **Defaults** > **Command execution** > **Approval reviewer** 里选。用户仍可以改选另一个被允许的审阅者。要强制使用，或要替换审阅策略，用 **Edit as TOML** 改 Global 的 `requirements.toml`。浏览器动作有单独的 Auto-review 控制，不要和命令执行混成一项。

该页给出的强制示例是：

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]
```

若还要允许人工审批，把 `"user"` 放进 `allowed_approvals_reviewers`。常驻 agent 上怎么把沙箱、网络和 Auto-review 写在一起，见 [常驻 Agent 安全加固](./27-Codex常驻Agent安全加固-照OpenAI的OpenClaw部署配requirements.toml与权限profile.md)。

另外两句只在桌面端、并且只针对获准的安全模型。Auto-review 页写：

- 在 ChatGPT 桌面端选中一个获准的 Daybreak 模型时，如果 **Approve for me** 对这个账号可用、并且组织策略允许，权限控件会自动切到这个模式。桌面端的 `/model` 命令也一样。这个模式不可用时，当前权限模式保持不变。选模型不会覆盖组织的托管要求。
- 为一个获准的安全模型打开 **Full Access** 之前，桌面端会显示针对该模型的危险动作警告，建议改用 **Approve for me**，并链到审阅策略配置。这则警告不会恢复沙箱边界，也不会覆盖组织策略。

本文没有桌面端，没有看过这则警告的界面。

## 哪些请求会交给审阅者

官方页把流程写成五步：

1. 主 agent 提出一个动作，例如要跑一条命令。
2. 如果这个动作需要审批，Codex 创建一条请求。
3. 若 `approvals_reviewer = "auto_review"`，这条请求交给独立的审阅 agent，而不是停下来等人。
4. 审阅者决定该不该执行，并返回理由。
5. 批准则继续执行。拒绝则指示主 agent 去找一条实质更安全的路径，或者停下问用户。

会交给审阅者的，是本来会停下来等人批的那些请求。官方列出的触发场景：

- 提权的 shell 或 exec 工具调用，也就是请求更高的沙箱权限。
- 命中命令规则且 `decision = "prompt"` 的命令，包括已经在沙箱里的命令。规则怎么写，见 [prefix_rule](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)。
- 目的地需要批准的网络请求。显式的网络 deny 规则会直接拦住这次请求。
- 写到允许的可写根目录之外的文件编辑。
- 按工具注解或所配置的审批模式、需要批准的 MCP 或应用工具调用。

已经有权限的动作不审，直接跑。

Computer Use 的应用级访问提示直接问用户。符合条件的 Computer Use 工具调用，仍可以另外触发 Auto-review。这两件事不要合成一句。

## 审阅者会拦什么、看得到什么

官方页用「设计上会拦」来概括四类，不是一份穷尽清单：

- 向不可信目的地发送私密数据、密钥或凭据。
- 探测凭据、令牌、cookie 或会话材料。
- 广泛或持久地削弱安全。
- 有显著不可逆损坏风险的破坏性动作。

具体规则在策略里。怎么换策略见下一节之前的配置说明；默认策略全文不要从本文推断，官方给的是固定版本链接。

审阅者评估的是触发这次审批的那个具体动作。它看得到的是一份精简对话记录，加上这次审批请求本身。官方写，这通常包括用户消息、已经展示出来的助手更新、相关工具调用和工具输出，以及当前提请批准的动作。它还可以做只读检查，例如在批准删除某个目录之前先查看这个目录。

看不到隐藏的助手推理。Auto-review 使用的是保留下来的聊天条目和工具证据，不是私有的思维链。

## 被拒绝之后

明确拒绝不当成普通沙箱错误。Codex 把审阅理由交回主 agent，并加上更强的指示：

- 不要用变通办法、间接执行或绕过策略，去追求同一个结果。
- 只有实质更安全的替代方案才可以继续。
- 否则停下，问用户。

多数模型下，Codex CLI 会在同一轮里中断：连续 3 次拒绝，或最近 50 次审阅里有 10 次拒绝。对网络安全类模型，CLI 在第一次拒绝时就中断这一轮。

任何其他审阅结果都会把「连续拒绝」的计数清掉。达到拒绝上限时，Codex 显示警告并停止这一轮。

超时和明确拒绝是分开的。主 agent 会被告知：仅凭超时不能证明这个动作不安全。

被拒绝之后还有一条显式的覆盖路径，但范围很窄。官方页写，在当前开源 TUI 里运行 `/approve`，会打开 **Auto-review Denials** 选择器，然后选择最近被拒绝的一个动作，批准它重试一次。Codex 每个任务最多记录 10 条最近的拒绝。这次批准只针对被拒绝的那一个动作，不是以后类似的动作；只在同一上下文里记录一次重试；重试仍然要经过 Auto-review。底层做法是为这个精确动作注入一条开发者范围的批准标记。审阅者会把这次明确的用户覆盖当作上下文，但仍然按策略办。如果策略规定用户不能覆盖这一类拒绝，它还可以再拒绝。

## 调整策略

审阅者怎么评估一个动作，由审阅模板规定。官方页把模板放在固定提交上：

- [reviewer template](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/prompts/templates/guardian/policy_template.md)
- 打包的 [policy.md](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/prompts/templates/guardian/policy.md)

这两条都指向 `rust-v0.167.0`。它们是这一版文档里的固定链接，不是「当前默认策略全文」。Codex 把安全策略插进模板，响应格式另外规定。CLI 在审阅模型有自己的默认策略时用那一份；否则用打包的 `policy.md`。本文没有把这两份文件复述成一份现行默认策略。

要替换策略：先复制你打算改编的完整策略。如果从打包默认开始，就复制 `policy.md` 的全文，改你要改的规则，再把全文放进本地的 `[auto_review].policy`，或托管的 `guardian_policy_config`。没写进去的规则就从替换稿里消失。Codex 仍使用审阅者的模板和响应格式。

托管的 `guardian_policy_config` 优先于本地 `[auto_review].policy`。空白的策略值会被忽略。

组织范围的设置见 Managed configuration 的 Configure Auto-review policy。该页写，要用 `guardian_policy_config` 替换整份策略，并指回 Auto-review 页查看默认策略以及怎么准备替换稿。

### 授权安全工作里的配置示例

下面两段是 Auto-review 页原文，页面标明用于授权的安全工作：要有书面的任务范围、最小权限的 permission profile、获准的实验目标，写明允许的动作和时间窗口，并把生产系统、无关主机、凭据和持久变更留在范围外，除非明确授权。不要把它们当成日常写业务代码的推荐配置。

本地 `config.toml` 打开 Auto-review，并选用 workspace 权限档案：

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
default_permissions = ":workspace"
```

托管的 `requirements.toml` 要求 Auto-review，并限制可用的权限档案：

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
# ":danger-full-access" is omitted, so it is denied.
```

官方页对这两段的说明：`allowed_permission_profiles` 管的是当前的权限档案。`allowed_sandbox_modes` 还用来防止仍在使用旧 `sandbox_mode` 的部署进入完整访问。白名单上的网络目的地本身不会触发审阅。如果沙箱内部的动作也必须送到审阅者，要另加 `decision = "prompt"` 的命令规则，或把敏感的 MCP 工具配成需要批准。

权限档案和 `codex sandbox` 怎么试，见 [沙箱与主机权限风险](./05-Codex沙箱与主机权限风险.md) 和 [sandbox 命令](./31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)。模型准入和推荐配置，官方页指向 Models and Trusted Access 与 recommended configuration。自定义 API 或 Agents SDK 的 harness，指向 Guardrails and human review。这三页本文没有展开。

## 减少审批量

官方的做法是先修边界，而不是教审阅者永远放行那些吵闹的提权。沙箱已经覆盖日常安全流程时，Auto-review 最好用。

页面写的两个杠杆最高的改动：

- 为你确实会用的临时目录或相邻仓库，加上窄的 [`writable_roots`](https://learn.chatgpt.com/docs/config-file/config-advanced#approval-policies-and-sandbox-modes)。
- 加上范围很窄的前缀规则。优先用精确前缀，例如 `["cargo", "test"]` 或 `["pnpm", "run", "lint"]`。不要用 `["python"]`、`["curl"]` 这种宽规则。宽规则往往会抹掉 Auto-review 要守的那条边界。对网络安全类模型，CLI 会忽略 `allow` 前缀规则，仍然遵守 `prompt` 和 `forbidden`。

会话记录默认留在 `~/.codex/sessions`。官方建议，在改策略或权限之前，可以让 Codex 分析那里过去的记录。

## 局限与自查清单

Auto-review 改善的是长时间代理工作的默认工作点。它不是确定性的安全保证。官方写了三条限制：

- 它只评估符合条件的审批请求，包括由显式命令规则或工具审批设置触发的请求。
- 它仍会出错，尤其是在对抗性或不寻常的上下文里。
- 它应该补上沙箱设计、监控和组织自己的策略，而不是替换它们。

研究理由和已发表的评估结果，官方页指向 [Alignment Research post on Auto-review](https://alignment.openai.com/auto-review/)。本文不转述那篇文章里的数字。

改完配置后，可以按这张清单自查。每一条都能在上面的官方说明里找到依据：

1. 当前对话的权限控件是不是 **Approve for me**，或配置里是不是已经有 `approvals_reviewer = "auto_review"`。只改了 `approval_policy` 不算。
2. 审批是不是仍会交互。`never`、`:danger-full-access`、`--yolo` 会让越界请求根本不出现。
3. 日常会撞上的目录和命令，是不是已经用窄的 `writable_roots` 和精确前缀收过，而不是靠宽的 `["python"]` 或 `["curl"]`。
4. 被拒绝之后，主会话有没有改去绕过。绕过不符合官方给主 agent 的指示。
5. 若在当前开源 TUI 里用了 `/approve`，这次放行是不是只针对被拒的那一个动作、只重试一次，并且重试仍会再过审阅。
6. 若写了 `[auto_review].policy` 或 `guardian_policy_config`，是不是整份策略。空白值会被忽略；没写上的规则不会保留。托管配置优先。

## 常见问题与参考资料

常见问题见文首的四则问答。

- [Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)（2026-11-27）
- [Permissions](https://learn.chatgpt.com/docs/permission-modes)（2026-11-27）
- [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)（2026-11-27）
- [Sandbox](https://learn.chatgpt.com/docs/sandboxing)（2026-11-27）
- [Managed configuration：Configure Auto-review policy](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-auto-review-policy)（2026-11-27）
- [策略模板，固定在 rust-v0.167.0](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/prompts/templates/guardian/policy_template.md)
- [打包的 policy.md，固定在 rust-v0.167.0](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/prompts/templates/guardian/policy.md)
- [权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [Codex Rules](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)
- [常驻 Agent 安全加固](./27-Codex常驻Agent安全加固-照OpenAI的OpenClaw部署配requirements.toml与权限profile.md)
