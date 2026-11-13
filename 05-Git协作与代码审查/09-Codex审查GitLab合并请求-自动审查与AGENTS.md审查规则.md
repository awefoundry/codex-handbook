---
id: codex-gitlab-merge-request-review
title: Codex 审查 GitLab 合并请求：@codex review、自动审查、自建 GitLab 服务账号与 AGENTS.md 审查规则
seo_title: Codex 审查 GitLab 合并请求：@codex review 与自动审查设置
description: Codex 可以审查 GitLab 合并请求：在 MR 评论里写 @codex review，或打开自动审查。本文按官方文档讲 GitLab.com 与自建 GitLab 的连接步骤、服务账号和 webhook 要求、AGENTS.md 审查规则、让 Codex 修复问题，以及不回复时怎么排查。
lede: GitLab.com 连账号、建项目环境就能用；自建 GitLab 还要管理员配服务账号，并且实例要在 19.0 以上。
url: /guides/codex-gitlab-merge-request-review
status: published
section: guides
category: E-git-collab
topic: 开发、测试与代码协作
content_type: 教程
source_tag: 官方功能
entry_tags: [Cloud]
difficulty: 进阶
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-12
date_modified: 2026-11-12
verified_on: 2026-11-12
official_ref: https://learn.chatgpt.com/docs/third-party/gitlab
keywords: [Codex GitLab, GitLab 合并请求审查, "@codex review", 自动审查, 自建 GitLab, 服务账号, Code Review Rules]
related: [codex-github-issue-pr-workflow, agents-md, cloud-environments]
faq:
  - q: Codex 审查 GitLab 合并请求要什么套餐？
    a: 官方文档写明 GitLab 代码审查集成目前是 beta，所有 ChatGPT 套餐都可以用。它在 Codex cloud 里运行。
  - q: 自建 GitLab 能用吗？
    a: 能，但要满足几个条件：工作区管理员先发布 GitLab 连接模板，在 Codex Cloud 的 Connectors 里配好服务账号（让 Codex 创建，或填一个带 api 权限的个人访问令牌）；webhook 需要签名，所以 GitLab 要 19.0 或更新；群组级 webhook 还需要 Premium 或 Ultimate。
  - q: 手动 @codex review 和自动审查报的问题一样多吗？
    a: 不一样。官方默认设置是：手动请求的审查可以报 P0、P1、P2，自动审查只关注 P0 和 P1。
  - q: 为什么 @codex fix 没反应，@codex review 却能用？
    a: 修复和其他编码任务需要先给项目配好项目环境。只开了群组级 GitLab activity 时，Codex 只能审查，不能改代码、提交或推送。
---

# Codex 审查 GitLab 合并请求：@codex review、自动审查、自建 GitLab 服务账号与 AGENTS.md 审查规则

> 本文在线版：[codexguide.io/guides/codex-gitlab-merge-request-review](https://codexguide.io/guides/codex-gitlab-merge-request-review)

> 核对依据：官方 [Review GitLab merge requests with Codex](https://learn.chatgpt.com/docs/third-party/gitlab)、[Code review](https://learn.chatgpt.com/docs/code-review)、[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)（2026-11-12 核对）。写作环境没有 GitLab 实例和已连接的 ChatGPT 账号，**本文没有截图**；界面名称按官方英文文档写，中文界面的叫法可能不同。GitLab 集成是 beta，以官方页面为准。

很多团队的代码不在 GitHub，而在 GitLab.com 或公司自建的 GitLab 上。Codex 的云端代码审查现在也支持 GitLab 合并请求（MR）：在 MR 评论里写 `@codex review`，Codex 会读 diff、按仓库里的规则审查，然后像同事一样在 MR 上发讨论。

## 先看结论

- **状态**：GitLab 代码审查集成是 **beta**，**所有 ChatGPT 套餐**可用，在 Codex cloud 里运行。
- **怎么触发**：MR 评论里写 `@codex review`；或者在设置里打开自动审查，选「MR 打开时」「每次推送」或「Smart Trigger（实验）」。
- **报什么**：手动审查默认可以报 P0、P1、P2；自动审查默认只报 P0、P1。
- **GitLab.com**：连接账号 → 为项目建项目环境并打开 **Enable Codex activity from GitLab** → 在审查设置里开审查。
- **自建或 Dedicated GitLab**：多了两步——管理员配**服务账号**，webhook 要**签名**，实例要 **GitLab 19.0 或更新**。
- **审查规则**：写在 `AGENTS.md` 的 `## Code Review Rules` 小节，就近放在被管的代码旁边。
- **让 Codex 改代码**：需要项目环境；只开群组级 activity 只能审查。

## GitLab.com 和自建 GitLab 的区别

| | GitLab.com | 自建（self-managed）或 Dedicated |
|---|---|---|
| 连接方式 | 先在 ChatGPT 里连接 GitLab，再在 Codex 里连接账号 | 工作区管理员先发布 GitLab 连接模板，每个审查者再各自连接 |
| Codex 用什么身份发评论 | 你连接的账号 | 工作区配置的服务账号 |
| 开启审查的前提 | 必须为项目建项目环境 | 项目环境或群组级 activity 都可以 |
| webhook 要求 | 由项目环境安装 | 项目或群组 webhook，需要签名，GitLab 19.0+ |

另外要注意：桌面端那套 GitHub 风格的仓库操作（比如 **Create pull request**）不在这个 beta 里。

## 连接账号和配置服务账号

**GitLab.com**：按 OpenAI 帮助中心的标准流程在 ChatGPT 里连接 GitLab，然后在 Codex 里连接一次账号即可。

**自建或 Dedicated GitLab**：工作区管理员打开 **Codex Cloud → Settings → Connectors**，选中你的 GitLab 实例，然后二选一。

**让 Codex 创建服务账号**：选择 **Set up service account → Create a service account**。

- 完成设置的管理员需要对 GitLab 实例有管理员权限。
- 范围选 **Selected groups**（对选中的群组授予 Developer 权限，下面的项目和子群组继承）或 **Selected projects only**（只对选中的项目授予 Developer 权限）。
- Codex 会创建名为「ChatGPT Codex Connector」的实例服务账号，带一个 `api` 权限的个人访问令牌。

**用已有的服务账号**：

1. 在 GitLab 里创建或选一个服务账号，只在需要 Codex 工作的群组或项目里给 **Developer** 权限。
2. 在 **Service accounts** 页面选中这个账号 → **Manage access tokens** → **Add new token**，创建 `api` 权限的个人访问令牌，**过期时间至少在 30 天以后**。
3. 回到 Codex，选 **Use an existing service account**，粘贴令牌，点 **Save token**。令牌加密保存，之后不会再显示。

令牌的后续管理也在 Connectors 里：Codex 创建的账号可以撤销当前令牌、生成新令牌；已有账号可以在 Codex 里替换或删除令牌，必要时再到 GitLab 里单独撤销。**没有有效令牌时，Codex 不会响应 GitLab 上的任何活动。**

## 打开 GitLab activity：项目 webhook 与群组 webhook

Codex 要收到 MR、评论和 Issue 事件，靠的是 GitLab webhook。有两种装法。

**项目环境（项目 webhook）**

在 **Codex Cloud → Settings → Environments** 里选 GitLab 项目，创建项目环境，打开 **Enable Codex activity from GitLab**，就会安装项目 webhook。以下情况需要项目环境：

- 想让 Codex 写代码、执行命令、提交或推送到 MR 分支；
- 审查依赖项目专属的密钥、网络访问或安装命令；
- **GitLab.com 开启审查本身就必须有项目环境。**

安装项目 webhook 需要 Maintainer 或 Owner、实例管理员，或能管理项目 webhook 的自定义角色。签名的项目和群组 webhook 要求 **GitLab 19.0 或更新**；自建 19.0 要确认 `webhook_signing_token` 功能开关是开的（默认开启，19.1 起这个开关已移除）。

**群组 activity（群组 webhook，仅自建或 Dedicated）**

工作区管理员在 **Environments → GitLab activity → Manage groups** 里为一个群组及其子群组开启审查，Codex 会装一个覆盖整个群组的 webhook。要求：连接的 GitLab 用户是该群组的 **Owner**，GitLab **Premium 或 Ultimate**，19.0 或更新。

群组 activity **只开启审查，不创建项目环境**。要让 Codex 在某个项目里改代码，仍要单独建项目环境。父群组已经开启时，子项目自动继承。

> 知识库旧文 [Codex Cloud 云端环境](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md) 写过「Cloud 环境暂不支持 GitLab」。按 2026-11-12 的官方 Cloud environments 文档，如果仓库选择器里出现 GitLab，就可以选 GitLab.com 的仓库创建可复用环境；自动关联项目仓库这一步仍只支持 GitHub.com。以官方页面为准。

## 手动审查：@codex review

1. 在 MR 的评论里写 `@codex review`。
2. 等 Codex 用 👀 表情回应，然后发出审查。

Codex 会在 MR 上发 GitLab 讨论（discussions）和备注（notes），和同事审查一样。

想让它这次只看某一块，可以把关注点直接写在评论里：

```text
@codex review for issues in the database migration
```

## 自动审查：三种触发方式

在 [Codex 审查设置](https://chatgpt.com/settings/code-review?provider=gitlab) 里选择仓库，在 **Review code** 下打开 **Automatic review**：

- **Review**：选择谁的 MR 会被审查；
- **Trigger**：选择什么时候审查——**On MR open**（MR 打开时）、**On every push**（每次推送）、**Smart Trigger (Experimental)**。

仓库级设置可以覆盖个人默认值。自动审查运行时不需要任何人写 `@codex review`，前提是：

- 项目 webhook 或某个父群组 webhook 已经开启 GitLab activity；
- 自建或 Dedicated GitLab 上，服务账号对这个项目有写回权限；
- MR 符合仓库策略和触发条件。

有项目环境时，Codex 会用它来审查。

## 用 AGENTS.md 写 Code Review Rules

Codex 会在仓库里找 `AGENTS.md`，遵守适用的代码审查规则。写法是加一个 `## Code Review Rules` 小节，可以用 `###` 给规则分组。官方示例（实验报表服务，防止按曝光后的行为筛选对照组）：

```md
## Code Review Rules

### Experiment cohorts

- Do not filter treatment comparisons on post-exposure behavior, including conversion or retention.
  Safe path: build cohorts from assignment or exposure; report conversion as an outcome.
```

放置位置：

- 全仓库通用的规则放根目录 `AGENTS.md`；
- 某个服务专用的规则放在它自己的目录，比如 `services/experiment_reporting/AGENTS.md`。

Codex 对每个改动文件同时应用根目录和更具体目录的规则，所以无关的改动不用背着别的服务的上下文。

官方给的写规则建议：

- **只写和这个仓库相关、后果严重的行为**：兼容性约束、数据边界、危险的副作用，并说明为什么重要；
- **写出安全做法或例外**，让 Codex 能分清真问题和预期行为；
- **规则要有范围、能长期有效**：写结果而不是会改名的函数名，放在被管的代码旁边；
- **机械检查留给 CI**：格式、lint 这类确定性检查不要写进审查规则。

先写两三条最常被人工审查反复解释的规则，开一个有代表性的 MR 用 `@codex review` 试一次，根据结果收窄或删掉产生噪音的规则。官方也提醒：审查规则只是指导 Codex，**不能替代测试、分支保护和必需的审批**。

`AGENTS.md` 的继承关系和写法细节，可以看 [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。

## 让 Codex 修复和处理其他任务

前提：项目配好了**项目环境**。只开群组 activity 时只能审查。

在同一个 MR 里继续评论，让 Codex 修某个问题：

```md
@codex fix the P1 issue
```

`@codex` 后面跟 `review` 以外的内容，Codex 会以这个 MR 为上下文启动一个旧版（legacy）云端对话，有权限时可以把修复推回 MR 分支。例如：

```md
@codex fix the CI failures
```

推回来的改动和任何人的提交一样，要看 diff、等 CI 通过再合并。

## 不回复时怎么查

按官方排障清单，从外到内检查：

1. **选对了 GitLab 应用吗？** 用项目环境的话，确认项目有对应的 Codex cloud 环境。
2. **webhook 送达了吗？** 在 GitLab 项目的 **Webhooks → Recent events** 里，确认 merge request 和 note（评论）事件投递成功。
3. **自建或 Dedicated**：webhook 是否签名、SSL 校验是否开启、实例是否 19.0+；自建 19.0 确认 `webhook_signing_token` 开关已开启；修复因多次失败被 GitLab 自动禁用的 hook。
4. **令牌还有效吗？** 已有服务账号的个人访问令牌是否有效、是否有 `api` 权限；Codex 创建的账号在 [Connectors 设置](https://chatgpt.com/codex/cloud/settings/connectors) 里是否配置正确、项目或群组是否已启用。
5. **服务账号有权限吗？** 是工作区的**服务账号**（而不只是你连接的 GitLab 用户）需要对项目或父群组有 Developer 权限，Codex 才能发审查和表情。成员关系可以继承；activity 和服务账号权限是两件独立的事。
6. **审查开了吗？** 确认 **Code review** 或 **Automatic reviews** 已开启，MR 符合仓库策略和触发条件。
7. 最后，直接在 MR 里写一次 `@codex review` 试试。

## 和 GitHub 审查、本地 /review 的关系

- **GitHub PR**：同样支持 `@codex review` 和自动审查，GitHub 的连接方式和 Security Review 见 [GitHub 插件实战：从 Issue 到 Pull Request](../08-插件工作流/05-GitHub插件实战-从Issue到PullRequest让Codex跑完整流程.md)。
- **桌面端 Code Review 插件**：可以在应用里看 PR 的描述、改动、评论和检查；官方写明 GitHub 代码审查已正式提供，GitLab 合并请求支持目前是预览。
- **本地 `/review`**：审查你本机 Git 工作区里的改动，不需要连接 GitLab，适合提交前自查。

## 参考

- 官方：[Review GitLab merge requests with Codex](https://learn.chatgpt.com/docs/third-party/gitlab)
- 官方：[Code review](https://learn.chatgpt.com/docs/code-review)
- 官方：[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)
- GitLab：[Webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/) · [为服务账号创建个人访问令牌](https://docs.gitlab.com/user/profile/service_accounts/#create-a-personal-access-token-for-a-service-account)
