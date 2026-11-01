---
id: codex-switch-multiple-accounts
title: Codex 多账号切换：手机端最多同时登录 2 个 ChatGPT 账号，CLI 用 CODEX_HOME 把个人号和公司号分开
seo_title: Codex 多账号：手机端双账号切换，CLI 用 CODEX_HOME 分开
description: ChatGPT 网页和手机端最多同时登录 2 个账号，同一时间只有 1 个生效。本文按帮助中心说明添加、切换和退出，并说明 Codex CLI 怎样用 CODEX_HOME 把个人号和公司号的配置与登录分开。
lede: 手机和网页上的账号切换，与 CLI 里用 CODEX_HOME 分开两套登录，是两件不同的事。
url: /guides/codex-switch-multiple-accounts
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [Chat, App, CLI]
difficulty: 基础
order: 16
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-01
date_modified: 2026-11-01
verified_on: 2026-11-01
tested_cli_version: 0.166.0
official_ref: https://help.openai.com/en/articles/20001068-using-multiple-chatgpt-accounts-on-web-and-mobile
keywords: [Codex 多账号, Codex 切换账号, ChatGPT 多账号切换, CODEX_HOME, Codex 个人账号和公司账号]
related: [codex-remote-control-mac, config-toml-guide, codex-chatgpt-shared-usage-limits]
howto: true
faq:
  - q: 最多能同时登录几个 ChatGPT 账号？
    a: 帮助中心写的是最多同时保持登录 2 个，同一时间只有 1 个生效。可以拥有 2 个以上的账号，但已经登录 2 个时，要先退出一个再添加。
  - q: 手机上看不到 Switch account 怎么办？
    a: 帮助文章写明，账号切换正在 iOS 和 Android 上逐步开放。Settings 里还没有 Switch account，可能是还没有推到这台设备。
  - q: 换 CODEX_HOME 会不会只换登录、配置还在原来的目录？
    a: 不会。官方把 CODEX_HOME 定义为 config、auth、logs、sessions、skills 等状态的根目录。换目录之后这些都是另一套。
  - q: 切换账号会把两个套餐的额度加在一起吗？
    a: 不会。帮助文章写明，切换不合并账单或订阅，每个账号保留自己的套餐。
---

# Codex 多账号切换：手机端最多同时登录 2 个 ChatGPT 账号，CLI 用 CODEX_HOME 把个人号和公司号分开

> 本文在线版：[codexguide.io/guides/codex-switch-multiple-accounts](https://codexguide.io/guides/codex-switch-multiple-accounts)

> 核对依据：OpenAI 帮助中心《[Using multiple ChatGPT accounts on web and mobile](https://help.openai.com/en/articles/20001068-using-multiple-chatgpt-accounts-on-web-and-mobile)》（2026-11-01 打开），ChatGPT Learn《[Authentication](https://learn.chatgpt.com/docs/auth)》《[Environment variables](https://learn.chatgpt.com/codex/config-file/environment-variables)》，以及 Codex CLI 0.166.0 的 [发行说明](https://github.com/openai/codex/releases/tag/rust-v0.166.0)。本环境没有手机，Switch account 界面不配图。

个人 ChatGPT 账号和公司工作区账号都要用来跑 Codex 时，先分清两套机制：ChatGPT 网页和手机上的账号切换，以及 Codex CLI 用 `CODEX_HOME` 分开的本地状态。它们不会自动同步。

登录入口本身见 [登录 Codex](./07-登录Codex.md)。

## 先看结论

帮助中心写明：可以同时保持登录最多 2 个 ChatGPT 账号，并在它们之间切换，不必先彻底登出。同一时间只有 1 个账号生效。

可用范围是 ChatGPT 网页，以及 ChatGPT 的 iOS 和 Android 应用。移动端正在逐步开放。桌面端的点击步骤，这篇帮助文章没有写。

Codex CLI 要把个人号和公司号分开，官方提供的办法是给每套状态一个已经存在的 `CODEX_HOME`。`file` 存储模式下，凭据文件 `auth.json` 放在这个目录里。

## 现在哪些端能切换

帮助文章的可用性一节：

- 网页和 ChatGPT iOS、Android 应用可以使用账号切换。
- 网页上，各套餐类型都可以使用；组织可以决定托管工作区是否开放。托管工作区里看不到这个选项时，问工作区管理员。
- iOS 和 Android 正在逐步开放。Settings 里没有 Switch account，可能是还没有推到当前设备。

桌面应用怎么点，帮助文章没有步骤。选题所引的 [2026-10-31 帖](https://x.com/thsottiaux/status/2116405414921384099) 被转述为「手机端已经可以在多个账号之间切换，桌面端即将支持」。2026-11-01 本环境打开该链接返回 403，没有复核帖子原文，也不引用赞和浏览量。在帮助文章写出桌面端步骤之前，本文不写桌面端操作。

## 手机端：添加、切换、退出

帮助文章给出的 iOS / Android 路径如下。本环境没有这些界面的截图。

**添加账号**：

1. 打开 Settings。
2. 选择 Switch account。
3. 选择 Add account。
4. 登录要添加的账号。

已经有 2 个账号处于登录状态时，Add account 会隐藏。先退出其中一个，Add account 才会再出现。

**切换**：打开 Settings，选择 Switch account，再选择另一个账号。

**退出**：

1. 打开 Settings。
2. 选择 Switch account。
3. 打开要退出的那个账号的更多菜单（•••）。
4. 选择 Log out 并确认。

退出当前正在使用的账号后，会打开另一个仍登录的账号。退出最后一个账号后，回到登录画面。退出会把该账号从切换器里移除。

新建第二个账号不需要付款。新账号默认从 Free 套餐开始。

## 网页上的差别

网页同样最多同时登录 2 个账号。帮助文章的网页步骤是：

1. 打开账号菜单。
2. 选择 Add account。
3. 登录或新建账号。

已经登录 2 个时，网页上的入口名称是 Add another account：先选择要退出的账号，再选择 Log out and continue，然后登录想添加的账号。这和手机上「Add account 直接隐藏」不一样，以各自界面为准。

网页上切换：打开账号菜单，选择要使用的账号。

网页上退出：打开账号菜单，选择 Log out；如果有 2 个账号登录，再选择要退出的那一个，并在出现提示时确认。

## 切换后什么跟着走、什么不会合并

帮助文章写明，切换之后，对话、记忆、文件和设置都反映当前选中的账号。有工作区时，工作区也属于该账号。开始对话或购买之前，先看清当前生效的是哪个账号。

切换不会做这些事：

- 把对话从一个账号搬到另一个账号
- 共享记忆或对话历史
- 共享文件或上传内容
- 合并账单或订阅
- 合并账号或工作区

每个账号保留自己的套餐。切换不会把订阅转过去或共享出去。另一个账号要付费套餐，需要单独订阅。购买前先确认订阅挂在哪个账号上，避免重复扣款。

已经付款但看不到订阅时，先检查拥有该订阅的那个 ChatGPT 账号，再决定要不要再次购买。帮助文章把后续的订阅恢复、购买、升降级和购买报错指到 Troubleshooting ChatGPT subscription access and account changes，本文不展开那篇的步骤。

## 切换账号和切换工作区

帮助文章的问答写得很直接：切换账号是换成另一个 ChatGPT 账号；切换工作区是在同一个账号里换工作区。两件事不是一回事。

网页上，如果某个账号关联的工作区被停用，可能会看到说明变化的横幅，并被提示用另一个账号登录或购买新订阅，具体取决于套餐。ChatGPT 不会自动切到另一个账号。

Codex CLI 0.166.0 的发行说明包含一项：Show the selected ChatGPT workspace in `/status`（#57366）。登录之后，可以在 CLI 会话里用 `/status` 看当前选中的 ChatGPT 工作区。本环境没有登录，没有 `/status` 的界面输出。

## 企业管理账号的限制

帮助文章把托管账号单独写成一节，要点是：

- 管理员可以访问并管理绑定在该账号上的数据。
- 在托管账号里产生的数据，适用组织的策略。
- 切换账号不会改变哪些策略继续生效。

不确定自己正在用哪个账号时，看账号菜单里标出的当前账号。组织策略问题找 IT 管理员。

Codex 侧，管理员还可以在配置里限制登录方式和工作区。Authentication 文档给出的字段是：

```toml
forced_login_method = "chatgpt" # 或 "api"
forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"
```

当前凭据不符合这些限制时，Codex 会把用户登出并退出。这两项也可以由托管配置下发。个人电脑上没有这两项时，不必自己填。

## Codex CLI：用 CODEX_HOME 分开两套登录

手机和网页的切换器管的是 ChatGPT 应用里的会话。Codex CLI 的登录缓存在本机。官方 Environment variables 页写明：`CODEX_HOME` 是 Codex 状态的根目录，包括 config、auth、logs、sessions、skills 和独立安装包的元数据，默认是 `~/.codex`。一旦设置，这个目录必须已经存在。

因此，个人号和公司号要各用一个目录，例如 `~/.codex-personal` 和 `~/.codex-work`。换的是整套本地状态，不只是「当前登录的邮箱」。

Authentication 文档把凭据存储分成四种，由 `cli_auth_credentials_store` 控制：

| 值 | 凭据放在哪 |
|---|---|
| `file` | `CODEX_HOME` 下的 `auth.json`（默认目录是 `~/.codex`） |
| `keyring` | 操作系统凭据库；凭据库不可用时失败 |
| `auto` | 有系统凭据库就用它，否则回落到 `auth.json` |
| `ephemeral` | 只留在当前进程的内存里 |

`file` 模式下，两套 `CODEX_HOME` 各有自己的 `auth.json`。`keyring` 模式下，凭据不在 `auth.json` 里。只改 `CODEX_HOME` 不能据此得出「系统凭据库里的两套登录已经分开」。要用文件分开，把对应配置设成 `file`，再分别登录，并确认每个目录里的 `auth.json` 只属于该账号。`auth.json` 里有访问令牌，按密码对待：不要提交进仓库，不要贴到工单或对话里。

2026-11-01 在 Codex CLI 0.166.0 上的核对：先建一个空目录，再把 `CODEX_HOME` 指过去。

```bash
mkdir -p ~/.codex-work
CODEX_HOME=~/.codex-work codex login status
```

输出是：

```text
Not logged in
```

退出码是 1。同一台机器上不设置 `CODEX_HOME` 时，`codex login status` 同样是 `Not logged in`、退出码 1。这次没有「默认目录已经登录、换目录变成未登录」的对照，只能说明新建的空目录处于未登录状态，与官方对 `CODEX_HOME` 的定义一致。

示例不要放在 `/tmp` 一类的临时目录下。本环境如果把 `CODEX_HOME` 指到临时目录，CLI 会提示无法创建 PATH 别名。用家目录下事先建好的目录。

在某个目录里登录：

```bash
CODEX_HOME=~/.codex-work codex login
```

浏览器流程完成后，这套凭据跟该 `CODEX_HOME` 走。结束这套登录用 `codex logout`。Authentication 文档写明：当进程选用 workload identity 时，Codex 会拒绝 `codex login` 和 `codex logout`，因为认证由进程环境控制。那种环境不适合用本文的双目录办法。

CLI 和 IDE 扩展默认共享同一份登录缓存。从其中一边登出后，下次启动 CLI 或扩展都要重新登录。这个共享指的是默认的 `~/.codex`。要让 IDE 扩展也使用另一个目录，需要扩展进程同样拿到那个 `CODEX_HOME`。官方环境变量页写明 IDE 扩展会读 `CODEX_HOME`；桌面应用是否跟随同一次 shell 导出，官方在这篇环境变量页里没有写成操作步骤。

字段放在哪一层、怎样确认生效，见 [config.toml 配置指南](../10-配置模型与权限安全/08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

## 怎么确认当前用的是哪个账号

按表面分开看：

| 表面 | 官方写出的看法 |
|---|---|
| ChatGPT 网页 | 账号菜单里标出的当前账号 |
| 手机 | Settings → Switch account 里当前选中的账号。帮助文章的配图说明用勾号标出生效账号；本环境没有这张图 |
| Codex CLI | `codex login status` 查看当前认证方式；会话里的 `/status` 在 0.166.0 会显示所选 ChatGPT 工作区 |
| 桌面应用 / IDE | Authentication 文档：打开个人资料菜单，查看当前账号或 API key 状态 |

`codex login status` 看的是认证方式，不是手机切换器里的那个勾号。API key 登录和 ChatGPT 登录是两条路。用 API key 时，计费走 API 价格，不走 ChatGPT 套餐里的额度。

## 常见问题

**两个账号的通知会打架吗？** 帮助文章写：移动端两个都登录的账号都可以收到通知，取决于每个账号自己的设置和设备权限。点开另一个账号的通知，会切到那个账号并打开对应内容。

**切换账号能把 12 月以后的共用额度分成两份用吗？** 不能靠切换把同一个订阅拆开。每个账号保留自己的套餐，账单不合并。额度规则见 [用量合并](../10-配置模型与权限安全/20-Codex和ChatGPT用量合并-12月起共用额度按token计算.md)。用多账号轮换绕过额度的做法，官方没有这样的说明，本文不写。

**手机上切了账号，电脑上的 Codex CLI 会跟着切吗？** 帮助文章没有这样写。CLI 用的是本机 `CODEX_HOME` 里的凭据。两边要各自确认。

**远程控制另一台电脑时，账号以哪边为准？** 远程那台机器上的 Codex 用它自己的登录状态。连接方式见 [远程控制另一台 Mac](../12-官方工具与集成/01-Codex远程控制另一台Mac.md)。不要把 `auth.json` 拷到不受信任的机器上。

## 参考资料

- [Using multiple ChatGPT accounts on web and mobile](https://help.openai.com/en/articles/20001068-using-multiple-chatgpt-accounts-on-web-and-mobile)（OpenAI Help Center，2026-11-01 核对）
- [Authentication](https://learn.chatgpt.com/docs/auth)（ChatGPT Learn，2026-11-01 核对）
- [Environment variables](https://learn.chatgpt.com/codex/config-file/environment-variables)（ChatGPT Learn，2026-11-01 核对）
- [Codex CLI rust-v0.166.0](https://github.com/openai/codex/releases/tag/rust-v0.166.0)（`/status` 显示所选工作区，#57366）
