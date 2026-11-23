---
id: codex-sandbox-how-it-works
title: Codex 沙箱怎么工作：拆解 OpenAI 官方《Inside the Codex sandbox》，:workspace 权限 profile 默认放行什么、拦住什么，三个系统分别怎么执行
seo_title: Codex 沙箱怎么工作：:workspace 默认放行什么、三个系统怎么执行
description: OpenAI 官方拆解了 Codex 沙箱：不靠虚拟机，而用 Seatbelt、bubblewrap 和 MXC 限制命令。本文说明 :workspace 权限 profile 默认放行什么、拦住什么，网络为何默认关闭，以及哪些风险沙箱管不到。
lede: 沙箱限制的是命令能碰哪些文件和网络。它不改变模型本身，也挡不住沙箱外面的程序事后执行那些文件。
url: /guides/codex-sandbox-how-it-works
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 解释
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 30
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-21
date_modified: 2026-11-21
verified_on: 2026-11-21
tested_cli_version: 0.171.0
official_ref: https://openai.com/index/inside-the-codex-sandbox
keywords: [Codex 沙箱, Inside the Codex sandbox, ":workspace 权限 profile", Seatbelt bubblewrap MXC, Codex 默认关闭网络]
related: [codex-sandbox-host-trust, permissions-sandbox-approvals, codex-network-permissions-proxy, codex-sandbox-command, windows-sandbox-mxc]
faq:
  - q: Codex 沙箱是一台虚拟机或一个 Docker 容器吗？
    a: 不是。官方博客写明，Codex 不把计算搬到另一套环境，而是用各系统自带的沙箱机制，限制已经在你现有环境里运行的命令。macOS 用 Seatbelt，Linux 用 bubblewrap 加 seccomp，Windows 正在换到 MXC。
  - q: 默认的 :workspace 会不会把整个家目录都变成只读？
    a: 不会。博客写：以 Git 仓库为工作区根时，:workspace 允许写工作区，但把 .git、.codex 这类目录保持只读，同时允许较宽的读取，并默认关闭网络。读取仍受你现有的操作系统权限约束，所以工作区以外的敏感配置文件仍可能被读到。
  - q: 关掉网络是不是就等于数据出不去？
    a: 只挡住这条命令自己的直接外传。博客举的例子是：命令仍可能改掉本地的 node_modules/prettier；如果编辑器保存时会跑这份 Prettier，那段代码就在沙箱外面执行。网络代理也管不到网页搜索、MCP 和浏览器。
---

# Codex 沙箱怎么工作：拆解 OpenAI 官方《Inside the Codex sandbox》，:workspace 权限 profile 默认放行什么、拦住什么，三个系统分别怎么执行

> 核对依据：OpenAI 博客 [Inside the Codex sandbox](https://openai.com/index/inside-the-codex-sandbox)（2026-11-18，作者 Michael Bolin；2026-11-21 打开原文核对代码块）。权限字段同时对照 [Permissions](https://learn.chatgpt.com/docs/permissions)（页面标注 Beta）。博客发布已经 3 天。[@OpenAIDevs 主帖](https://x.com/OpenAIDevs/status/2123129469447880885)（2026-11-18T19:01:26Z）在 2026-11-21 打开页面时，公开计数是 1,018 赞、69 转发、50 引用、142 回复、418 收藏；展示数没有从页面里再核对。HN [50564390](https://news.ycombinator.com/item?id=50564390) 同一天是 2 分。本文用中文归纳，TOML 示例标明出处。macOS 的 Seatbelt 和 Windows 的 MXC **引自官方文章，未在本站环境实测**。Linux 上只核对了 Codex CLI 0.171.0 的 `codex sandbox` 会真正拦住写入和联网，命令输出写在 [sandbox 命令](./31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)。

## 先说结论：Codex 沙箱限制的是命令，不是模型

Codex 最常做、也最容易出事的一件事，是在你的电脑上跑命令。官方的做法是纵深防御：训练和对齐负责让模型按你的意图用权限；沙箱再给这些命令加上文件系统和网络边界。

所以沙箱回答的是「这条命令能读哪里、写哪里、能不能联网」，不是「模型会不会产生坏主意」。模型拒绝某条指令，也不能代替这道边界。审批是另一根旋钮：它决定什么时候必须先问你，不改变沙箱外面那些程序的权限。整体怎么选，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

用户通过 **permission profile（权限 profile）** 描述这些限制。一次会话用一份具名策略，里面同时写文件系统规则和网络规则。博客把 harness 的公共接口概括成：传入命令和一份 permission profile；如果 profile 只允许有限的网络，调用方还要提供一个网络代理来执行这些限制。子进程继承父进程的沙箱约束，所以整棵进程树都带着同一道边界，包括比原命令活得更久的后代。

## 为什么不用虚拟机或容器：直接在你现有的环境里限制

虚拟机和容器是常见的隔离办法。Codex 不走这条路。博客的理由是：很多开发者的笔记本本身就是一套随手改过的环境，把它再复制进 Docker 要花功夫，而且有些工具必须在宿主机上跑。

例子是在 Mac 上做 iOS 应用。如果把 Codex 放进 Docker，它就跑不了由 Mac 原生可执行文件组成的 iOS 构建工具链，也启动不了 iPhone 模拟器。可以把构建和模拟器委托回 Mac 宿主机，但那些操作已经在容器沙箱外面，还得再单独加限制。Codex 选择把力气花在各系统自己的沙箱上，让命令留在最适合这项任务的环境里。

三个系统对外是同一套接口，对内各自执行。下文第 6 节分开写。

## 默认 :workspace profile：能写哪里、能读哪里、为什么网络默认关

博客以「Git 仓库作为工作区根」说明内置 `:workspace`。默认取舍是：限制从紧，但还要能做日常工作。

**能写哪里。** 允许写工作区内部，同时把 `.git`、`.codex` 这类目录保持只读。这样 Codex 改源码时不必每次都征求许可，也不能直接改 `.codex/config.toml`，也不能改 `.git/hooks` 里的 Git 钩子。

Permissions 页对同一份内置 profile 还有一句补充：`:workspace` 允许写**当前工作区根**和**系统临时目录**。博客展示它从 `:workspace` 继承的工作区规则是：

```toml
[permissions.":workspace".filesystem.":workspace_roots"]
".agents" = "read"
".aws" = "read"
".codex" = "read"
".git" = "read"
```

Permissions 页写明，用 `extends = ":workspace"` 时，工作区根下的 `.git`、`.agents`、`.codex`、`.aws` 会保持只读，除非你明确覆盖。`:workspace_roots` 里的规则会套到每一个工作区根上。博客写：Codex CLI 默认把当前工作目录当作唯一的工作区根；ChatGPT 桌面应用用的是项目的源码文件夹。

**能读哪里。** 允许较宽的文件系统读取，但仍受你现有的操作系统权限约束。编译器、运行时和构建工具依赖仓库外面的 SDK、库和配置；如果把读取收成只限工作区，很多普通流程会断。代价是机器上别处的敏感文件也可能仍然可读，博客举的例子是含有 API key 的配置文件。

**网络为什么默认关。** 博客把网络写成三档，`:workspace` 落在第一档：

- 关闭全部网络（`:workspace` 的默认）
- 打开直接、不受限制的网络（`:danger-full-access` 的默认）
- 只允许连到代理，由代理按 profile 决定放行什么

关掉网络，可以挡住命令把已经读到的数据直接传到外部服务，也会挡住正当操作，比如下载依赖。那些操作需要额外放行。Permissions 页的字段默认值是 `permissions.<name>.network.enabled = false`。写成 `true` 只表示允许联网，**不会**自己启动网络代理；域名规则要等 `features.network_proxy = true`（或管理员托管的网络要求）之后才生效。没有代理时，域名表限制不了直连。域名怎么写，见 [网络权限](./26-Codex网络权限-network_proxy域名白名单与本地服务访问.md)。

Permissions 页还列出另外两个内置 profile：`:read-only` 让本地命令保持只读；`:danger-full-access` 去掉本地沙箱限制，只在你确实要给整台机器时使用。profile 和旧的 `sandbox_mode` / `sandbox_workspace_write` **不能叠用**。配置里只要出现 `sandbox_mode`，或者你传了 `--sandbox`，Codex 就改用那套旧设置，而不是 `default_permissions`。

## 沙箱管不到的事：node_modules 被改、敏感文件仍可读

上面这组默认值挡住一大类坏事，挡不住全部。博客举了两个仍然可能发生的例子。

第一，命令可以往本地已安装的包里注入代码，例如 `node_modules/prettier`。`node_modules` 经常被 Git 忽略，所以 `git status` 未必看得到这次改动。如果用户的编辑器在保存时会跑这份 Prettier，一次保存就会在 Codex 沙箱**外面**执行那段代码。

第二，就是上一节的宽读取：工作区以外、操作系统仍然允许你读的敏感文件，沙箱默认不替你藏起来。

这和 [沙箱与主机权限风险](./05-Codex沙箱与主机权限风险.md) 讲的是同一条缝的两侧。那篇从「沙箱外的程序事后会读、会执行 Codex 写下的文件」复盘；这篇说明官方为什么仍把读取放宽、把 `.git` 收紧。两篇都不把沙箱说成完整隔离。

博客因此把训练、对齐和沙箱放在一起：沙箱限制命令能碰到什么，训练和对齐帮助模型按你的意图使用这些权限。企业环境里怎么把沙箱和其他防护合在一起，博客指向 [Codex security cookbook](https://learn.chatgpt.com/docs/enterprise/security-cookbook)。

## 自己定义 profile：dev 示例、分层配置与 requirements.toml

具名 profile 写在 `config.toml` 的 `[permissions]` 下，同一套文件系统和网络限制可以跨项目复用。下面这份 `dev` **引自博客**「Configuring the sandbox」。它在 `:workspace` 上加规则，不是从零开始：

```toml
default_permissions = "dev"

[permissions.dev]
description = "Development with extra read-only protections."
extends = ":workspace"

[permissions.dev.filesystem]
"~/build-cache" = "write"

[permissions.dev.filesystem.":workspace_roots"]
".devcontainer" = "read"
".vscode" = "read"
"**/*.env" = "deny"
"secrets" = "deny"
```

文件系统条目只有三种值：`read`（只读）、`write`（可读可写）、`deny`（读和写都拒绝）。`:workspace_roots` 里的路径相对于每一个工作区根。所以上面的 `.vscode` 会让每个根下面的 `.vscode` 变成只读。`description` 是 `/permissions` 里给人看的说明；Permissions 页写明，它不会通过 `extends` 从父 profile 继承。

博客给出的网络例子分两步。要给 `dev` 直接联网，在配置顶层写 `permissions.dev.network.enabled = true`；代理没开时，这是完整的直接网络访问。要把访问收成一组域名，需要同时打开代理。博客原文的结构是（`[features]` 在域名表后面）：

```toml
[permissions.dev.network]
enabled = true

[permissions.dev.network.domains]
"*.openai.com" = "allow"
"localhost" = "allow"
"127.0.0.1" = "allow"
"::1" = "allow"
"evil.example" = "deny"

[features]
# 如果本地配置和托管要求都没有打开代理，
# 这个 profile 允许直接联网，域名规则不生效。
network_proxy = true
```

精确域名和通配符都可以写。显式的 `deny` 优先于 `allow`。没有匹配到允许或拒绝规则的域名，按博客的说法会要求批准，或者被拦住；具体走哪条，博客指向后文的网络代理。Permissions 页补充：代理处于活动状态、且一条 `allow` 都没有时，域名请求会被挡住。

**分层。** 个人可以先写跨项目的默认，再在受信任的项目里覆盖。企业管理员也可以写默认，并限制用户能改什么。Codex 合并多层 `config.toml`：表按层递归合并，冲突时高优先级的值赢；数组则整段替换。profile 把路径和域名做成表，就是为了让团队只改自己的几条，其余继续继承组织的底稿。博客的例子是在团队配置里再加：

```toml
[permissions.dev.filesystem.":workspace_roots"]
".idea" = "read"

[permissions.dev.network.domains]
"example.com" = "allow"
```

**requirements.toml。** 管理员用托管要求约束用户能选哪些 profile。博客的云端例子：

```toml
default_permissions = ":read-only"

[allowed_permission_profiles]
":read-only" = true
":danger-full-access" = false
```

博客写：这份云端要求优先于系统文件 `/etc/codex/requirements.toml`，所以那个文件里的条目不能把上面显式的 `":danger-full-access" = false` 翻过来。某一层没写 `:workspace` 时，另一层 requirements 仍可以补上这一项。最终合并表里值为 `false`、或者根本没有的 profile，不可用。

Permissions 页的说法要一起看：一旦出现 `allowed_permission_profiles`，被省略的 profile 会被拒绝，包括被省略的内置 profile 和将来版本新增的 profile。两处并不矛盾，前提是看**合并之后的那张表**，而不是只看其中一层有没有写到这个名字。更完整的托管写法见 [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)，常驻场景的收紧例子见 [常驻 Agent 安全加固](./27-Codex常驻Agent安全加固-照OpenAI的OpenClaw部署配requirements.toml与权限profile.md)。

怎么用 `codex sandbox -P` 把上面的 `dev` 真正跑一遍，不在这里重复，见 [sandbox 命令](./31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)。

## macOS、Linux、Windows 分别靠什么执行

博客先写三边共用的网络代理，再写各系统。代理的请求处理和策略逻辑是同一套；怎么把进程的流量送进代理，是各系统自己的事。

代理由 `codex-network-proxy` 实现。打开之后，它默认同时听一个 HTTP 代理和一个 SOCKS5 代理，再通过环境变量告诉沙箱里的进程，包括 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`，以及一部分工具自己的变量（博客举了 `PIP_PROXY`）。不是每个程序都认这些变量。程序若绕过变量、直接连外部主机，就由操作系统那一层的沙箱挡住。

顺序有意放在 DNS 之前：连主机名里都可以藏信息，所以代理先判定允许或已经批准，再解析这个名字。宽泛的通配符，或者能够访问 DNS 服务，仍然可能让基于 DNS 的外传发生。博客写明了这个剩余风险。

### macOS：Seatbelt

**引自官方文章，未在本站环境实测。**

macOS 上 Codex 使用 Apple 的 Seatbelt，策略用 Sandbox Profile Language（SBPL）写，通过 `/usr/bin/sandbox-exec` 启动。形态和 `codex sandbox` 类似：先写沙箱选项，再写要跑的命令。

```bash
sandbox-exec -p PROFILE [-Dkey=value]* -- PROG ARGS...
```

博客写，Codex 的基础策略从 `(deny default)` 开始，所以出站连接默认拒绝，除非明确允许。网络代理打开时，会注入只允许连到本机代理端口的规则；博客举例是 HTTP 的 `localhost:3128` 和 SOCKS 的 `localhost:8081`。可写目录一类的路径用 `-Dkey=value` 填进 SBPL 的 `(param)`。

`man sandbox-exec` 写着这条命令已弃用，`sandbox_init()` 也是。macOS 仍在 `/usr/share/sandbox` 里带 Seatbelt 策略，Chrome / Chromium 也还在用。博客的结论是：尽管有弃用警告，可预见的将来仍继续用 Seatbelt。Apple 没有把这门语言文档化给第三方，所以生成正确的 SBPL 本身就难。本文不补博客没有写的 SBPL 细节。

### Linux：bubblewrap 与 seccomp

Linux 上是 bubblewrap（`bwrap`）加 seccomp-bpf。内部辅助程序叫 `codex-linux-sandbox`：先接沙箱参数，再接用户命令。需要文件系统隔离或代理转发时，它用 `bwrap` 做出初始环境；`bwrap` 再在里面启动 `codex-linux-sandbox --apply-seccomp-then-exec`，由这一层套上 seccomp，然后才跑用户命令。

文件系统视图用挂载命名空间表达 profile：

- `--bind`：可写的文件或目录
- `--ro-bind`：只读
- `--perms 000 --tmpfs DIR --remount-ro DIR`：拒绝整个目录
- `--perms 000 --ro-bind-data FD FILE`：拒绝单个文件

`deny` 用的通配符会在每次启动前展开成具体路径。命令跑起来之后新出现的匹配路径，不会自动补进这一次的限制。`--unshare-ipc`、`--unshare-pid` 让沙箱碰不到宿主机上的另一些资源，所以 bubblewrap 不只是「少看见几个目录」。

网络关闭，或者连接必须走代理时，Codex 传 `--unshare-net`，给沙箱一个新的网络命名空间，再用 seccomp 限制网络相关系统调用和 socket 类型。网络完全关闭时，会挡住 `connect(2)`、`bind(2)` 等一批调用。代理打开时，允许 IP socket，以便沙箱里的程序连到转发进程；默认则挡住单独创建的 Unix domain socket，避免无意碰到宿主机上的资源。套 seccomp 时会设置 `no_new_privs`，子进程不能靠 setuid 程序再提权。

Codex 自带一份 `bwrap`，免得用户没装；如果 `PATH` 上有兼容的系统 `bwrap`，优先用那一份。博客写，有些发行版默认禁止用户命名空间，但给系统自带的 `bwrap` 开了例外。

**本站环境。** 2026-11-21，Linux，`codex-cli 0.171.0`，`bwrap` 不在 `PATH` 上。空配置下 `codex sandbox -- echo hi` 仍能打出 `hi`；显式 `-P :workspace` 时，工作区里的普通文件可以写，`.git` 和工作区外的写入得到 `Read-only file system`，创建 TCP socket 得到 `PermissionError: [Errno 1] Operation not permitted`。这说明限制确实套上了。本文没有拆进程，不能证明实际执行的是自带的那一份 `bwrap`。完整命令和输出见 sandbox 命令一文。

Linux 上连共享代理的办法也和 macOS 不同。Seatbelt 可以让命令直接连宿主机回环上的指定端口。Linux 在隔离的网络命名空间里放一个回环监听，再由沙箱外的进程转发到代理。命令看到的是自己的网络命名空间，包括单独的回环接口。

### Windows：换到 MXC

**引自官方文章，未在本站环境实测。** 启用步骤、兼容性和 elevated / unelevated 回退见 [Windows 沙箱](./09-Codex-Windows沙箱-启用MXC与elevated-unelevated回退.md)。

博客写，今年早些时候的 Windows 沙箱正在被 Microsoft 的 MXC（Microsoft eXecution Container）替换。Codex 在兼容的 Windows 设备上使用基于 MXC 的沙箱，用原生进程隔离限制命令，命令仍在用户现有环境里。要换掉的旧限制包括：搭建沙箱需要提升权限；ACL 检查和设置又贵又慢；宿主机上会留下持久状态（ACL、防火墙规则、沙箱用户、控制面文件）。

MXC 使用一份 JSON 配置。Codex 用 MXC SDK 填入命令、工作目录、环境和权限。权限覆盖文件系统、网络，以及桌面、剪贴板这类 Windows 资源。博客写了一批固定取舍：允许读注册表；保留 PowerShell 启动时需要的 Win32k 和桌面访问；关闭剪贴板、输入注入，以及桌面和系统设置控制；并且不让 MXC 退回去改宿主机的文件系统权限。

文件系统默认拒绝。为了实现 `:workspace` 那种宽读取，Codex 会给本机各个盘符根加上只读授权，这些授权按递归生效，但仍受用户现有的操作系统权限约束。可写的盘符根授权**不**递归，Codex 会把它展开到该盘已经存在的直接子项。更具体的路径覆盖祖先：`C:\` 只读时，工作区目录仍可写，而工作区里的 `.git` 仍只读。同一路径如果有多种写法或符号链接 / junction，MXC 取更严的那条：`deny` 优先于只读，只读优先于读写。

`deny` 通配符同样只接受展开后的具体路径，启动前展开；命令运行期间新出现的匹配路径不会自动补上。域名规则仍由前面的共享代理执行。MXC 挡住直接的外部连接，但允许连宿主机回环，因此代理可达；其他本机服务也仍然可达。博客把最后这一点单独写出，不要把它理解成「Windows 上连本机服务也会被域名表自动挡住」。

## 怎么自查：该看哪几个设置

1. 你现在用的是 permission profile，还是旧的 `sandbox_mode`。两套同时出现时，Codex 走旧沙箱，`default_permissions` 不生效。
2. `default_permissions` 指向哪一个名字。内置的是 `:read-only`、`:workspace`、`:danger-full-access`。自定义的用 `extends`，优先从 `:workspace` 或 `:read-only` 往下收，而不是从零写一份更宽的。
3. 工作区里的 `.git`、`.codex`、`.agents`、`.aws` 是否仍是只读。要放宽某一条，必须是你明确写上的覆盖。
4. 网络是「全关」「直接全开」还是「代理加域名表」。只写 `network.enabled = true` 而不开 `features.network_proxy`，域名表不生效。
5. 企业机器再看 `requirements.toml` 的 `allowed_permission_profiles`。合并后没有的、或写成 `false` 的 profile 选不了。
6. 用 `codex sandbox` 对你在意的那条路径试一次写入，而不是只看 TOML。见 [sandbox 命令](./31-Codex-sandbox命令-用权限profile测试脚本和MCP服务器的沙箱.md)。

沙箱仍然不管网页搜索、连接器、MCP 服务器、浏览器、Computer Use，以及 Codex 自己的模型和登录请求。那些要各自的开关。MCP 怎么收，见 [MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 参考资料

- [Inside the Codex sandbox](https://openai.com/index/inside-the-codex-sandbox)（2026-11-18，Michael Bolin）
- [@OpenAIDevs 主帖](https://x.com/OpenAIDevs/status/2123129469447880885)（2026-11-18T19:01:26Z）
- [Permissions](https://learn.chatgpt.com/docs/permissions)（Beta）
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [Codex security cookbook](https://learn.chatgpt.com/docs/enterprise/security-cookbook)
- [Hacker News 50564390](https://news.ycombinator.com/item?id=50564390)（2026-11-21 为 2 分，不作热度依据）
