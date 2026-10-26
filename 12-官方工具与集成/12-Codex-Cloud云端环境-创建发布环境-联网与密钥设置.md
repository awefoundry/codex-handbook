---
id: cloud-environments
title: Codex Cloud 云端环境配置：发布可复用环境、设置联网与网络密钥，让任务在电脑休眠时继续运行
seo_title: Codex Cloud 云端环境：创建发布、联网、网络密钥与 codex apply
description: Codex Cloud 在云端跑编程任务，电脑休眠也能继续。本文按 2026 年 10 月官方文档，讲清如何创建并发布可复用环境，如何设置联网、环境变量与网络密钥，以及用 codex cloud／codex apply 把结果拉回本地。
lede: 把装依赖、起服务、联网策略做成可发布的云端环境；新任务从这份快照起步，本地电脑睡着也不耽误。
url: /guides/codex-cloud-environments
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, Cloud, CLI]
difficulty: 进阶
order: 12
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/environments/cloud-environments
keywords: [Codex Cloud, 云端环境, cloud environments, 网络密钥, network secrets, Install script, Start skill, Personal vault, codex cloud, codex apply]
related: [worktree-parallel-chats]
howto: true
faq:
  - q: Codex Cloud（Legacy）和现在的云端环境是一回事吗？
    a: 不是。Legacy 继续支持 Code Review 以及 Linear、GitHub 等集成，官方计划弃用；联网设置见旧页 Internet access。新体验以 Cloud environments 为准，联网走 Connect to services（域名白名单、Package managers 预设、网络密钥等）。
  - q: 环境变量和网络密钥该怎么选？
    a: 程序必须直接读到的值（例如 APP_MODE）用环境变量。只应出现在对某 HTTPS 服务请求里的凭据用网络密钥：进程里是占位符，由代理在允许域名、443 端口的 HTTPS 上替换；保存环境级网络密钥还会把其域名加入受限联网策略。
  - q: 改了已发布环境，旧任务会自动更新吗？
    a: 不会。要 Edit → 让 Codex 准备并测试 → Republish；新任务才用新快照。已有任务保留自己的工作区（含未提交改动与已装工具）。仓库刷新在后台进行，不会重跑安装或启动命令。
---

# Codex Cloud 云端环境配置：发布可复用环境、设置联网与网络密钥，让任务在电脑休眠时继续运行

> 本文在线版：[codexguide.io/guides/codex-cloud-environments](https://codexguide.io/guides/codex-cloud-environments)

> 核对依据：learn.chatgpt.com 的 Cloud environments、DevDay 2026（Reusable cloud environments）、Codex Cloud（Legacy）Internet access、Developer commands（`codex cloud`／`codex apply`）。文中「我的用法」是工作流建议，不是官方规定。本机未登录可用的 Codex Cloud 账户做端到端验证，界面文案以你当前网页／桌面端为准。

本地电脑要睡觉、手机上还想推进改动，或希望同事共用同一套「装好依赖、开好联网」的底座——这就是 **Codex Cloud** 的场景：任务跑在云端 VM 里，网页、手机或桌面端都能开、都能续；电脑休眠也不打断。

**可复用云端环境（cloud environment）** 是任务真正落地的那份配置：仓库、依赖、工具、联网与密钥策略。Codex 会检查仓库、帮你准备并测试；**Publish** 之后，每个新任务从已发布环境的准备好的文件系统起一份**隔离工作区**。这是 DevDay 2026 推出的 Reusable cloud environments 能力。

本文按官方文档写清：创建→发布、Install script／Start skill、联网与密钥、状态怎么更新，以及终端里的 `codex cloud`／`codex apply`。并单独划清 **Legacy 联网页** 与 **新版 Connect to services**，避免照着旧文档配错。

## 先对齐：Cloud、Local、Worktree、远程连接

| 方式 | 代码实际跑在哪 | 典型用途 |
|---|---|---|
| **Local** | 你本机当前 checkout | 日常 IDE、本机服务、立刻改立刻看 |
| **Worktree** | 本机另一份 Git worktree | 本机并行，不踩前台 Local |
| **远程控制** | 另一台已连接的电脑／远程开发环境 | 人在别处，机器在别处，但仍是「那台机器」 |
| **Codex Cloud** | OpenAI 托管的云端 VM | 电脑可休眠；跨网页／手机／桌面续同一任务 |

Cloud **不是**「把本机目录挂到云上」：新任务从**已发布环境**的文件系统起步；仓库访问依赖你连接的 GitHub 与账号权限。仓库里的 Skills 在云端任务可用；**本机个人 Skills 不会同步到云端环境**（官方 Current limitations）。

**入口：** 网页或桌面端：任务里选 **Work in → Cloud**，再选已发布环境。手机：打开 Codex，选可用环境。**新建环境**在网页或桌面端完成（Settings → Codex Cloud → Environments → Create environment 亦可）。Enterprise 管理员可在推广前审查工作区访问权限。

## 新版与 Legacy：别配错联网页

官方并行保留两套体验，容易混：

- **现行 Codex Cloud（本文主体）**：可复用环境、Publish／Republish、Connect to services、环境变量／网络密钥、Personal vault、Tailscale VPN、OIDC 等。文档入口：[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)。
- **Codex Cloud（Legacy）**：继续支持 **Code Review** 以及 **Linear、GitHub** 等集成；官方**计划弃用**。其联网说明在单独页面 [Internet access](https://learn.chatgpt.com/docs/cloud/internet-access)，页首写明：**这些设置只适用于 Legacy**；现行体验请看 Cloud environments 里的 **Connect to services**。

Legacy 联网模型（仅作对照，**不要**当成新版步骤）：

- 默认在 agent 阶段拦外网；**setup 脚本阶段仍可联网**装依赖。
- 可按环境开 agent 联网，用域名白名单与允许的 HTTP 方法收紧；有 Common dependencies 等预设。
- 官方强调风险：提示注入、密钥外泄、恶意依赖等。

新版则是：**Allow Codex to access internet** + **Allow domains**（Package managers／仅自定义／All）+ **Additional allowed domains**，并与 **网络密钥**、Enterprise **Agent Security** 叠加。下文只按新版写操作。

## 创建并发布第一个环境

用 ChatGPT 账号登录网页或桌面端：

1. 新任务里选 **Work in → Cloud**，打开 **Select environment**，选 **Create environment**（或走 Settings → Codex Cloud → Environments）。
2. 选择要 checkout 的 **GitHub 仓库**；未连接则按提示连接 GitHub。
3. 选 **Get started**。Codex 检查仓库、安装依赖与工具，并测试工作流。
4. 缺权限或信息时按提示补上；也可要求特定版本、命令或服务。
5. 查看 **setup report**、配置与文件；处理未完成项，保存更改，选 **Publish**。
6. 出现 **Environment published** 后，选 **Start a new task**，描述要做的事。

官方对保存与发布的区分：

- **Saving** 存配置；部分设置会对**当前正在准备的 setup**立刻生效。
- **Publishing** 固化已准备好的文件系统，供**新任务**使用。
- **Sharing（Privacy → Who can use）** 控制谁能用这份环境，不等于把别人的任务文件共享出去。

**我的用法：** 第一次先用一个小仓库或 monorepo 里真正要跑的子树练手；报告里依赖装绿、关键命令能跑，再 Publish。未发布环境在列表里会带 **Unpublished** 徽章，不能拿来开新任务。

## Install script 与 Start skill

Codex 会从仓库识别运行时、包版本、工具与服务。你可以在对话里 refinement，**不必自己先写一整份安装脚本**。

测通后，官方会把结果记进两个字段：

| 字段 | 作用 |
|---|---|
| **Install script** | 安装依赖、准备开发资源的命令 |
| **Start skill** | 启动服务并检查就绪的说明 |

配置面板里常见「Install script / Start skill：Configured」。之后新任务从发布快照起步；需要改安装或启动逻辑时，走 Edit → 再测 → **Republish**，而不是只在某个旧任务里临时改一改就指望全局生效。

## 联网：Package managers、自定义域名、何时 All

在环境配置里：

1. 打开 **Allow Codex to access internet**。
2. 在 **Allow domains** 选 **Package managers** 或 **Custom domains only**，再在 **Additional allowed domains** 补主机名；工作流确实需要大范围出网时再用 **All（unrestricted）**。
3. 保存，在 setup 期间测服务；Publish／Republish 后，用**新任务**再验一次。

**允许域名 ≠ 有权限。** 白名单只决定 VM 能否连到主机；凭据、仓库权限、云厂商 IAM 仍要另配。

**Package managers 预设**（官方列出的注册表／下载域，节选类别）：npm／Yarn、PyPI／PyTorch、Rust crates、Go proxy、Maven／Gradle、Bazel、Buf、CPAN、Ubuntu／Debian、部分厂商源、GitHub 源码／Release／LFS、以及其他如 `dl.google.com` 等。对已登记的根域，Codex 也会放行对应的 `www`；**其他子域要单独加白**。依赖还访问别的主机时，全部写进 Additional allowed domains。

Enterprise 工作区里，管理员的 **Agent Security** 会与环境级域名策略一并生效；环境页可能提示「由组织策略限制联网，详询管理员」。按 IP 过滤来源的服务，官方要求订阅 **agent egress IP** 源、每天核对并更新对方白名单；这些 IP 段跨客户共享，服务侧鉴权仍要保留。

**我的用法：** 默认 **Package managers** + 私有 registry／API 的精确主机名；只有确认需要随意抓网页或未知 CDN 时才开 All，并接受更大的提示注入与外泄面。

## 环境变量、网络密钥与 Personal vault

Codex 推不出的配置会向你要。在配置里对 **Environment variables** 或 **Network secrets** 点 **Manage**，按用途选择：

| 类型 | 用途 | 交付方式 |
|---|---|---|
| **环境变量** | 程序必须**直接读取**的值 | 原样注入环境进程 |
| **网络密钥** | 发给特定 **HTTPS** 服务的凭据 | 程序只看到**占位符**；代理对**允许域名**替换真值 |

网络密钥要填 **Key、Value、Allowed domains**；Key 不要与直接环境变量撞名。替换在 **setup 与任务期间**生效，且针对 **HTTPS、443**；**不会**把明文写进本地进程环境或文件。

要点：

- **保存环境级网络密钥**会把其目标域**加入**该环境的受限联网策略。
- **直接环境变量**和 **Personal vault 里的个人值**不会因此自动加域名。
- 改完先看已保存的网络策略，再测。

### Personal vault（个人保险库）

用来存**只属于你**的环境变量与网络密钥，供工作区内的云端环境按 Key 取用。

- 共享环境可以声明「需要这些 Key」；**共享的是需求，不是你的凭据**。
- 开任务时若缺个人值，在 **Add personal secrets** 填入后 **Save and start**；可选值可不设。
- 预先管理：Settings → Codex Cloud → **Personal vault** → Add，选类型，填 Key／Value，**Applies to** 选全部或指定环境。
- 保存后值保持隐藏；条目默认都是可选。只有环境**请求到的** Key 才会进任务；**针对某环境的值优先于「全部环境」默认值**。
- 个人网络密钥仍走该环境的允许域名，占位符替换规则与环境级相同。

**我的用法：** `APP_MODE`、功能开关 → 环境变量；私有 npm／PyPI token、只应出现在 HTTPS 请求头里的 registry 密钥 → 网络密钥。若客户端非要把密钥读成「环境里的明文字符串」才能工作，只能改环境变量，并接受落在进程环境中的风险。

## 已保存状态：新任务、旧任务、刷新与 Republish

| 场景 | 从哪开始 |
|---|---|
| **新任务** | 已发布环境准备好的文件系统 |
| **已有任务** | 该任务自己的保存文件（含未提交改动、已装工具） |
| **仓库刷新** | 后台自动进行；保留依赖缓存，**不重跑**安装或启动命令 |

更新可复用底座：Settings → Codex Cloud → Environments → 环境 **⋯ → Edit** → 描述变更 → 让 Codex 准备并测试 → 保存 → **Republish**。然后**开新任务**才用到更新；旧任务仍用自己的状态。

官方提醒：重要工作请 **commit**，或另存你需要的产物；**保存的 VM 状态不能替代版本控制**。默认情况下，任务保存的 VM 状态在你最后一次发回合或恢复后，最多约 **七天**可恢复（以官方 VM specifications 为准）。

未发布环境先完成 Publish；已发布却看不到更新时，确认是否走了 Republish，以及你是否仍在旧任务里操作。

## 终端：`codex cloud` 与 `codex apply`

不必只盯网页。Developer commands 里：

### `codex cloud`（Experimental，别名 `codex cloud-tasks`）

在终端浏览或发起云端任务，不必开 TUI。

- 默认：交互式选择器。
- `codex cloud exec`：直接提交任务；**`--env ENV_ID` 必填**（可用 `codex cloud` 列出）；可选 `--attempts 1-4`（best-of-N）；`QUERY` 可省略（交互追问）。
- `codex cloud list`：列最近云端对话；`--env`、`--limit 1-20`、`--cursor`、`--json`。纯文本会打任务 URL 与状态；JSON 含 `tasks` 与可选 `cursor`，任务字段含 `id`、`url`、`title`、`status`、`environment_id` 等。

认证与主 CLI 相同。提交失败时非零退出。

### `codex apply`（Stable，别名 `codex a`）

把某次 **Codex cloud chat** 的**最新 diff** 打到**本地工作树**。需已登录且对该 chat 有权限；参数为 `TASK_ID`。成功会打印改动文件；`git apply` 冲突等失败时非零退出。

**我的用法：** 云端改完 → 网页或 `codex cloud list` 拿到任务 → 本地仓库 `codex apply <TASK_ID>` → 再本地测／开 PR。Cloud 与 Local 是两份世界，**apply 是桥梁**，不要假设云端未提交改动会自动出现在笔记本上。

桌面端／IDE 斜杠里也可能有 `/cloud`、`/cloud-environment`（以当前客户端帮助为准）；与 CLI 的 Experimental `codex cloud` 互补，不是互相替代。

## 团队共享、Tailscale 与常见问题

### Enterprise 共享环境

环境配置 → **Privacy → Who can use** 选工作区 → 保存；若尚未发布则 Publish。选 **Only me** 则保持私有。

每人任务工作文件隔离；能用环境 ≠ 能看别人的任务，也 ≠ 能编辑该环境。共享前检查准备文件与**环境级**凭据。仓库权限、个人连接仍跟**跑任务的账号**走。角色上：**Use Codex in the cloud** 管任务访问；**Manage workspace environments** 管创建／编辑共享环境（见 Roles and workspace permissions）。

Slack／Microsoft Teams：在启用 Cloud 委派的 Enterprise 工作区，可用 `@ChatGPT` 让其选共享且当前账号可用的环境；可点名偏好环境。RBAC 场景下，部署服务账号与请求用户都需要 Codex Cloud 访问权限。

### VPN（目前：Tailscale）

Advanced → **VPN** → Add，填入提供商凭据；目标域须同时满足 **VPN 访问规则**与**环境联网白名单**。保存后 Publish／Republish，新任务里再测。

官方当前支持 **Tailscale**。创建 auth key 时打开 **Reusable** 与 **Ephemeral**（可复用以便新 VM 加入；临时设备离线后由 Tailscale 清理）。支持私有 IPv4 子网路由、split DNS、MagicDNS。内部 DNS 时在 Tailscale 管理台配 split DNS，使用解析到 **IPv4** 的全限定主机名。共享环境上的任务使用该环境配置的 VPN 身份。其他 VPN 提供商「计划中」。

排障：确认客户端走环境的 HTTP／HTTPS 代理（`curl` 测试时不要乱加 `--noproxy`）；域名同时过环境白名单与 VPN 规则；能 IP 不能域名时查 Tailscale DNS／split DNS。

### 设置失败或缺工具

看 setup 对话里失败命令，让 Codex 诊断并重跑（例如「安装 pnpm 并跑测试」）。初始失败可用 **Try again**（仓库选择保留）。若必须改源码／manifest／lockfile，先在编码任务里改，再回 setup。验证后再 Publish／Republish。

### 包下载或 HTTPS 失败

1. 主机名是否在环境联网设置里（含子域）。  
2. 包管理器 URL 与凭据是否正确（放行域名 ≠ 有权下载）。  
3. 若用网络密钥：Allowed domains 是否含目标，且请求为 **HTTPS:443**。  
4. Enterprise：请管理员对照 Agent Security 与环境设置。

### 缺值或值不可用

环境变量 vs 网络密钥选错是常见原因：需要进程内明文 → 环境变量；只需 HTTPS 出站替换 → 网络密钥。个人值检查 Key 是否匹配、Applies to 是否包含该环境。

### 其他限制（官方 Current limitations）

暂不支持：Computer／browser use；GitLab 与自建 GitHub Enterprise Server。VM 默认可按套餐见文档表格（如 Plus／Edu Plus：2 vCPU／8 GiB／8 GiB；Pro／Business／Enterprise 与 Edu／Edu Pro：4／16／32）。更大规格面向 Enterprise，需联系账户团队。

OIDC（AWS／GCP／Azure 等）可在 Advanced → OIDC 挂短时云凭据；兼容矩阵以官方「OIDC compatibility」表为准（例如部分 Azure／RDS IAM 登录仍为 Not yet supported）。本文不展开逐步云厂商控制台操作；需要时按该节与云控制台文档配置 trust（Issuer／Audience／Subject）。

## 我的用法：一条可复用清单

1. 网页／桌面端创建环境 → 选 GitHub 仓 → Get started → 看 setup report → **Publish**。  
2. 联网：Package managers + 必要额外域；私有 token 优先 **网络密钥**；本机开关类用环境变量；个人凭据进 **Personal vault**。  
3. 改底座：Edit → 测通 → **Republish** → **新任务**验证；不要假设旧任务会换根文件系统。  
4. 电脑可关：任务丢 Cloud；要回本地开发树时用 **`codex apply <TASK_ID>`**（或网页审 diff 再同步）。  
5. 团队只共享环境与「需要哪些 Key」，不共享 Personal vault；VPN 仅 Tailscale 时按 Reusable+Ephemeral 建 key。  
6. 看到 Internet access／Common dependencies 旧文案，先确认是不是还在 **Legacy** 文档或旧 UI。

## 小结

- **Cloud environment** = 可发布的仓库＋依赖＋联网／密钥底座；新任务隔离起步，电脑休眠也能续跑。  
- **Publish／Republish** 决定新任务看到的文件系统；Saving ≠ Publishing。  
- **Install script／Start skill** 固化装依赖与起服务； refinement 用对话即可。  
- **环境变量**直接注入；**网络密钥**占位符＋443 HTTPS 代理替换，且可写入联网策略。  
- **Personal vault** 保个人凭据；共享环境不共享你的密文。  
- **Legacy Internet access** ≠ 新版 **Connect to services**；Code Review 等仍可能在 Legacy。  
- 终端：**`codex cloud`**（Experimental）管云端任务，**`codex apply`**（Stable）把最新 diff 拉回本地。

参考：

- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)  
- [DevDay 2026 · Reusable cloud environments](https://learn.chatgpt.com/docs/whats-new/devday-2026)  
- [Codex Cloud（Legacy）：internet access](https://learn.chatgpt.com/docs/cloud/internet-access)（仅 Legacy）  
- [Developer commands：`codex cloud`／`codex apply`](https://learn.chatgpt.com/docs/developer-commands)
