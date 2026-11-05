---
id: codex-access-tokens-service-accounts
title: Codex 访问令牌和服务账号：在 CI 和定时任务里不用浏览器登录运行 codex exec（Business / Enterprise）
seo_title: Codex 访问令牌与服务账号：CI 里免浏览器登录
description: Business 和 Enterprise 工作区可以用访问令牌或服务账号，在 CI、定时任务里不用浏览器登录就运行 codex exec。本文讲清它和 API Key 怎么选、管理员要开哪些权限、令牌怎么创建、存放、轮换和撤销，以及常见报错怎么排查。
lede: 需要工作区身份时用访问令牌。只是调用 API 时，继续用 API Key。服务账号只在按量付费方案上，给 CI 一个非个人身份。
url: /guides/codex-access-tokens-service-accounts
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 14
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/enterprise/access-tokens
keywords: [Codex access token, CODEX_ACCESS_TOKEN, codex login --with-access-token, Codex 服务账号, Codex CI 登录]
related: [codex-automation-ci-scheduled-tasks, codex-cli-commands-cheatsheet, codex-config-toml-cheatsheet]
faq:
  - q: Plus 或 Pro 个人账号能创建访问令牌吗？
    a: 官方 Access tokens 页写，目前只支持 ChatGPT Business 和 Enterprise 工作区。个人套餐不在这句范围内。
  - q: 服务账号和访问令牌是什么关系？
    a: 访问令牌是凭证。个人访问令牌代表创建它的那位成员。从服务账号详情页创建的令牌代表这个非个人的工作区身份。服务账号只在按量付费方案上可用。
  - q: 令牌会不会显示第二次？
    a: 不会。官方写明创建后立刻复制，关闭对话框就不能再查看完整令牌。
  - q: CI 里应该把令牌写进 codex login，还是只放环境变量？
    a: 临时或共享的 runner 用 CODEX_ACCESS_TOKEN，不要在机器上保存登录。只有受信任、需要反复使用的本机，才用 codex login --with-access-token 把凭证存下来。
  - q: 把本地 Codex 权限关掉，令牌会怎样？
    a: 官方写：受影响成员名下正在使用的 Codex 令牌会被暂停，不会被撤销。恢复本地 Codex 权限后，这些令牌重新可用。要永久停用，必须在 Access tokens 页撤销。
---

# Codex 访问令牌和服务账号：在 CI 和定时任务里不用浏览器登录运行 codex exec（Business / Enterprise）

> 本文在线版：[codexguide.io/guides/codex-access-tokens-service-accounts](https://codexguide.io/guides/codex-access-tokens-service-accounts)

> 核对依据：ChatGPT Learn [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)、[Service accounts](https://learn.chatgpt.com/docs/enterprise/service-accounts)、[Pricing](https://learn.chatgpt.com/docs/pricing) 的功能表（2026-11-05）。命令是否存在、错误原文，在 Linux 上的 Codex CLI 0.166.0 用独立的 `CODEX_HOME` 看过：未登录时 `codex login status`，以及用一个明显无效的字符串调用 `codex login --with-access-token`。没有 Business 或 Enterprise 工作区，所以没有创建过真实令牌，也没有在 GitHub Actions 上跑过。

脚本、夜间任务和 CI 若每次都弹浏览器，流程就停在登录页。Business 和 Enterprise 可以用工作区访问令牌，让 `codex exec` 带着工作区身份跑。只需要调用模型 API、不需要工作区权限时，官方建议继续用 API Key。API Key 那条路的 GitHub Action 写法见 [自动化与 CI](./07-Codex自动化与定时任务-从手动流程到稳定执行.md)。

## 先选：访问令牌、服务账号，还是 API Key

三样东西解决的不是同一个问题。

| | 访问令牌（个人） | 服务账号上的访问令牌 | API Key |
|---|---|---|---|
| 代表谁 | 创建它的那位 ChatGPT 工作区成员 | 工作区里的一个非个人身份 | API 平台上的密钥，计费走 API 组织 |
| 谁能用 | 文档写目前是 Business 和 Enterprise | 只在按量付费方案上。只有 owner 和 admin 能创建账号 | 定价页把 API Key 写成共享环境（例如 CI）的自动化方式 |
| 适合 | 受信任的本机脚本，用量要记在某个成员名下 | CI、定时任务、共享集成，不想绑在某个人的账号上 | 不需要 ChatGPT 工作区权限、按 API 价格付费的调用 |
| 不能拿来做的事 | 只有 Codex 作用域时，不能触发 Workspace Agent；也不能当作通用 OpenAI API 密钥 | 服务账号令牌不能调用 Admin API | 定价页写 API Key 没有云端功能（例如 GitHub 代码审查、Slack） |

官方的选择顺序是：API Key 已经够用，就继续用 API Key。工作流需要 ChatGPT 工作区权限、工作区管理的权益或企业控制时，再用访问令牌。

定价页功能表有一行 Codex access tokens for trusted automation。2026-11-05 抓到的纯文本里，Plus、Pro 和 API Key 三列是破折号；Business 与 Enterprise / Education 两列没有符号，不能据此判断有没有勾选。范围以 Access tokens 页的原句为准：目前支持 Business 和 Enterprise 工作区。

## 管理员先打开权限

能创建令牌，和能在本地使用 Codex，是两道开关。令牌权限本身不授予桌面端、CLI 或 IDE 扩展的使用权，也不改变席位类型或内置角色。用令牌跑 CLI 或 app-server，这位成员还要有本地 Codex 权限。

工作区 owner 打开 Workspace settings → Permissions & roles。界面有两种写法，用你工作区里看得到的那一种：

1. 若出现 Access tokens 这一节，打开 **Allow users to create personal access tokens**。
2. 若没有这一节，在 Codex and Work Local 或 Codex Local 里打开 **Allow members to use Codex access tokens**。
3. 再给实际跑任务的人打开本地 Codex：Codex and Work Local 里的 **Allow members to use Codex and Work Locally**，或 Codex Local 里的 **Allow members to use Codex locally**。Work Local 若单独成节，Use Work locally 管的是 Work，不是 Codex 令牌的前提。

只让知道令牌放在哪、给哪条自动化用、何时轮换的人来创建。

Owner 还可以限制新令牌的最长有效期。有 Access tokens 节时，在那里设置 Access token expiration limit；否则在 Codex and Work Local 或 Codex Local 里找同名设置。文档界面示例显示为 90 days。这条上限只约束之后新建的令牌，已经发出的令牌保持原来的有效期。

关掉某位成员的本地 Codex 权限，会暂停他名下仍在用的 Codex 令牌，不会撤销。权限加回来，令牌恢复可用。要永久失效，去 Access tokens 页撤销。

## 创建访问令牌

在管理后台的 Access tokens 页创建。官方文档没有把浏览器地址印成一条固定链接，按工作区设置里的 Access tokens 入口进。

1. 打开 Access tokens，选择 Create。
2. 起一个能看出用途的名字，例如 `release-ci` 或 `nightly-docs-check`。
3. 对话框若有 Scopes，Codex 自动化选 **Codex**。只有这条工作流还要触发 Workspace Agent 时，才再选 **Workspace Agents**。没有作用域选择器时，创建出来的是仅 Codex 的令牌。
4. 选一个有限的有效期。文档举例是 7、30、60、90 天。带作用域的个人访问令牌必须过期。更早的「仅 Codex」对话框可能提供 No expiration；除非组织允许、并且有固定轮换日程，否则不要选。自定义有效期最短一天。
5. 创建后立刻复制。关闭对话框就不能再看完整令牌。
6. 放进密钥管理器或 CI 的 secret。不要写进仓库、日志或聊天。

仅 Codex 的令牌不能用来触发已发布的 Workspace Agent。通用 API 调用仍用平台 API Key。作用域只给这条工作流真正需要的。

若创建对话框写了所需的 CLI 版本，先把 CLI 升到那个版本或更高。服务账号令牌另有一条硬性要求，见下一节。

## 两种用法

0.166.0 的 `codex login --help` 有 `--with-access-token`，说明是从标准输入读取访问令牌，示例为 `printenv CODEX_ACCESS_TOKEN | codex login --with-access-token`。

**临时任务用环境变量，不把登录写进本机。** 官方示例：

```bash
export CODEX_ACCESS_TOKEN="<access-token>"
codex exec --json "review this repository and summarize the top risks"
```

**受信任的本机可以保存登录。** 官方用 `printf`，避免把换行符送进令牌：

```bash
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
codex exec "summarize the last release diff"
```

`codex login --with-access-token` 会在 CLI 的登录存储里记下这个身份。不想在机器上留凭证，就只用环境变量。

`codex app-server` 可以用同一个 `CODEX_ACCESS_TOKEN`，或用上面保存的登录，来为自己的 OpenAI 请求认证。这和客户端连接 app-server 时的传输认证不是同一把钥匙。远程 WebSocket 要另配 bearer 或 capability token，不要把 Codex 访问令牌拿去当传输令牌。

本机没有真实令牌。用一个明显无效的字符串调用时，0.166.0 的原文是：

```text
Reading access token from stdin...
Error logging in with access token: invalid agent identity JWT format
```

标准输入为空时：

```text
Reading access token from stdin...
No access token provided via stdin.
```

两条的退出码都是 1。未登录时 `codex login status` 输出 `Not logged in`，退出码也是 1。官方写的是：有凭证时 `codex login status` 退出码为 0。

## 服务账号：给 CI 一个独立身份

服务账号是工作区里的非个人身份，可以有自己的组和角色，用量记在这个身份上，而不是记在创建它的员工身上。它不继承创建者的插件、已连接应用和权限。

官方限制：

- 只有按量付费方案能用。
- 只有工作区 owner 和 admin 能创建、删除或分享账号。
- 用服务账号的访问令牌跑 Codex，CLI 要 **0.142.0 或更高**。0.166.0 满足这条。
- 插件要在服务账号自己的 Plugins 里添加。Configure 和 Manager 可以配插件，User 不行。

创建步骤：打开工作区设置里的 Service accounts，点加号，写一个名字（文档示例是 `release-automation`），再 Create。然后在这个账号的 Access tokens 里 Create token，确认 Codex 作用域和有效期。完整令牌同样只显示一次。可选的有效期受工作区策略限制。

把账号分享给人或组时，共享角色只管「谁来管这个账号」，和工作区赋给服务账号本身的角色不是一回事：

| 共享角色 | 配置账号和插件 | 创建服务账号的访问令牌 |
|---|---|---|
| User | 不能 | 能 |
| Configure | 能 | 不能 |
| Manager | 能 | 能 |

Configure 和 Manager 还可以启用或停用账号。操作的人仍登录自己的 ChatGPT 账号，不是登录成服务账号。

跑法与个人令牌相同：临时 runner 设 `CODEX_ACCESS_TOKEN` 后直接 `codex exec`；要在受信任的机器上保存登录，再用 `printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token`。官方写明，共享或临时的 runner 不要保存登录。

工作区若支持 SCIM，在身份提供商里把 `userType` 设为 `ServiceAccount`，再同步到工作区。这种账号的名字、组成员和生命周期由身份提供商管理，不能在 ChatGPT 里改名或删除。

有 Admin API 的工作区，可以用 ChatGPT Admin API key 管理账号、令牌和分享。读取需要 `chatgpt.enterprise.service_account.read`，变更需要 `chatgpt.enterprise.service_account.write`。服务账号自己的令牌不能调用 Admin API。创建账号的路径是 `POST /v1/manage/workspaces/{workspace_id}/service-accounts`。文档里的令牌示例是一个 30 天的 Codex 令牌，`ttl` 为 `2592000`（秒），`scopes` 为 `chatgpt.workspace.feature.allow-codex-local-access.access`。有限寿命必须短于一年，并符合工作区的过期策略。完整的 `access_token` 只在创建时返回。可用操作以 Admin API 参考为准，本文没有调用过这些接口。

## 在 GitHub Actions 里用

官方没有给出一份 Actions YAML。它写的约束是：令牌只放在受信任的 runner 上；公开 CI、fork 来的 pull request、共享机器都可能把令牌暴露给工作区以外的人。

因此只在你们自己控制的 workflow 上注入 secret，例如默认分支的 push。不要让 fork 的 pull request 读到 `CODEX_ACCESS_TOKEN`。下面只是把文档里的环境变量套进一个步骤，本文没有在 GitHub 上运行：

```yaml
- name: Run Codex
  env:
    CODEX_ACCESS_TOKEN: ${{ secrets.CODEX_ACCESS_TOKEN }}
  run: codex exec --json "review this repository and summarize the top risks"
```

这一步用环境变量，不在 runner 上执行 `codex login --with-access-token`。密钥不要写成会先 checkout、再跑仓库可控代码的整个 job 的 `env`；那部分要求见 [自动化与 CI](./07-Codex自动化与定时任务-从手动流程到稳定执行.md)。访问令牌和 API Key 一样，只给真正调用 Codex 的那一步。

## 轮换和撤销

官方的轮换顺序：

1. 创建一把新令牌。
2. 更新 runner、调度器或密钥管理器里的 secret。
3. 用新令牌做一次冒烟。
4. 在 Access tokens 页撤销旧令牌。

Owner 和 admin 可以撤销工作区里的任何令牌。有创建权限的成员只能撤销自己创建的。已撤销或已过期的令牌不能再用来发起认证运行。

服务账号不用了：在工作区或 Admin API 里停用或删除。两样都会撤销它名下仍有效的令牌。停用之后还可以再启用并签发新令牌；删除不能撤销。

## 安全风险清单

Access tokens 页列出的风险，原意是这些：

- 令牌泄露后，别人可以以创建者的身份，通过 CLI 或 app-server 在本地发起运行。
- 跑在公开 CI、fork 的 pull request 或共享机器上，工作区以外的人可能读到令牌。
- 把同一个人的令牌套到多个不相干的团队，审计时看不清是谁的流程。
- 有效期很长的令牌，会在流程已经改掉之后继续有效。优先用有期限的令牌，不用的立刻撤销。
- 作用域或凭证类型用错：Codex 自动化要 Codex 权限，触发 Workspace Agent 要 Workspace Agents 权限，普通 API 调用要平台 API Key。

服务账号页另要求：只给工作流需要的角色、组、插件和连接；凭证不进日志、聊天和源代码；定期看账号的权限和活动；泄露后立刻撤销并查最近的活动。运行记录记在服务账号上。工作区分析和审计里，还可能看到是谁创建了令牌或改了账号设置。事件覆盖范围以 Admin API 参考为准。

## 常见报错

**Access tokens 页是 404 或 forbidden。** 请 owner 确认你的角色里有 Allow users to create personal access tokens，或 Allow members to use Codex access tokens，看界面上是哪一条。还要确认本地 Codex 权限是开着的。

**`codex login --with-access-token` 失败。** 官方要你核对三件事：贴进去的是刚创建的访问令牌，不是浏览器会话令牌，也不是平台 API Key；令牌仍有效、没过期；令牌所属用户有本地 Codex 权限。0.166.0 在令牌根本不是它期望的格式时，会直接返回上一节里的 `invalid agent identity JWT format`。这只能说明字符串不像一把访问令牌，不能说明工作区权限已经开通。

**`codex exec` 在登录之前就退出。** 在不是 Git 仓库、也没有被信任的目录里，0.166.0 仍会拒绝：`Not inside a trusted directory and --skip-git-repo-check was not specified.` 这和令牌无关。确实要在仓库外跑，才加 `--skip-git-repo-check`。

命令本身的位置见 [CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。浏览器登录见 [登录 Codex](../01-安装与首次使用/07-登录Codex.md)。

## 参考资料

- [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)
- [Service accounts](https://learn.chatgpt.com/docs/enterprise/service-accounts)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands) 中的 `codex login`
