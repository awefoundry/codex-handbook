---
id: codex-ide-extension-security-check
title: Codex IDE 扩展安全自查：Cursor 扩展市场出现 Claude Code 后门后，怎么确认你装的是官方 openai.chatgpt
seo_title: Codex IDE 扩展安全自查：确认官方 openai.chatgpt
description: 2026 年 10 月 29 日 Cursor 扩展市场出现被篡改的 Claude Code。本文说明没有证据表明 Codex 扩展受影响，并给出核对 openai.chatgpt、svc-telemetry 自查，以及按 Cursor 通告处理的步骤。
lede: 先确认你装的是不是官方 openai.chatgpt。这次通告点名的是 Claude Code 的两个版本，不是 Codex。
url: /guides/codex-ide-extension-security-check
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 排障
source_tag: 官方功能
entry_tags: [IDE]
difficulty: 基础
order: 19
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-31
date_modified: 2026-10-31
verified_on: 2026-10-31
official_ref: https://cursor.com/blog/claude-code-extension-security-notice
keywords: [Codex IDE 扩展安全, openai.chatgpt, Codex 扩展官方发布者, VS Code 扩展投毒, Cursor 扩展市场 Claude Code 后门]
related: [codex-vscode-install]
howto: false
faq:
  - q: Codex 扩展受这次事件影响了吗？
    a: 没有证据表明受影响。Cursor 通告点名的是 Anthropic.claude-code 2.1.312 和 2.1.313，并写明审计后没有其他扩展被篡改。通告也写明这些发现只涉及被点名的包，没有证据表明该扩展的其他版本或官方分发渠道受影响。
  - q: 卸载扩展就够了吗？
    a: 不够。通告写明，卸载扩展可能清不掉已经落下的持久化脚本。确认中招后，要删掉未授权的 SSH 公钥、持久化项和正在跑的隧道进程，并从可信系统轮换这台机器上能碰到的凭据。
  - q: 要不要关掉 Codex 扩展的自动更新？
    a: 这次事件不是 Codex 扩展中招。VS Code 可以按官方文档关掉单个扩展的自动更新，当作少装到来路不明更新的习惯。官方 openai.chatgpt 仍应从已核对的市场更新。
---

# Codex IDE 扩展安全自查：Cursor 扩展市场出现 Claude Code 后门后，怎么确认你装的是官方 openai.chatgpt

> 本文在线版：[codexguide.io/guides/codex-ide-extension-security-check](https://codexguide.io/guides/codex-ide-extension-security-check)

> 核对依据：Cursor 2026-10-29 安全通告 [Security notice — malicious version of Anthropic.claude-code](https://cursor.com/blog/claude-code-extension-security-notice)（页内更新说明为 2026-10-30 11:30 am PT，更新了失陷指标并澄清受影响版本）。扩展身份核对了 [Visual Studio Marketplace 上的 openai.chatgpt](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)、Gallery API，以及 [Open VSX 的 openai.chatgpt](https://open-vsx.org/api/openai/chatgpt)。安装入口来自 [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)。自动更新来自 [VS Code 扩展市场文档](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)。核对日期 2026-10-31。本文没有登录 Cursor，也没有拆包审计 Codex 扩展。

很多人在 VS Code、Cursor 或 Windsurf 里用 Codex。2026 年 10 月 29 日，Cursor 自己的扩展市场里出现了被篡改的 Claude Code 扩展。先看和 Codex 有关的结论，再做自查。

## 先看结论

- 通告点名的是 **Anthropic.claude-code 2.1.312 和 2.1.313**（Windows、macOS），来源是 Cursor VS Code Extension Marketplace。这些版本不是 Anthropic 发布的。
- **没有证据表明 Codex 扩展受影响。** 通告写明不影响其他扩展，并写明审计后确认没有其他扩展被篡改。失陷指标也只针对被点名的这个包。官方分发渠道没有被通告列入受影响范围。
- Codex 在编辑器里的官方扩展标识符是 `openai.chatgpt`，显示名是 “Codex – OpenAI’s coding agent”。2026-10-31 在 Visual Studio Marketplace 和 Open VSX 上看到的版本都是 `26.51021.22027`。
- 只有在通告给出的时间窗里，从 Cursor 市场安装或更新到那两个 Claude Code 版本，才需要按通告做完整处置。只装了 `openai.chatgpt` 的人，把下面的自查跑一遍即可，不必按“已经中招”去轮换全部凭据。

安装步骤见 [VS Code、Cursor 和 Windsurf 安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md)。

## 事件经过

Cursor 通告日期是 2026 年 10 月 29 日。被篡改的包大约在当天 **2:27am PT 到 1:35pm PT** 之间可下载。换算成北京时间大约是 10 月 29 日 17:27 到 10 月 30 日 04:35（太平洋夏令时比北京时间晚 15 小时）。通告原文用的是 PT。

通告描述这个包会做三件事：

1. 收集并上报主机信息，包括主机名、用户名、操作系统、架构、主目录、环境变量名、工作目录、Git 邮箱和公网 IP。
2. 尝试把攻击者的 SSH 公钥写进 `authorized_keys`，打开本机 SSH 服务，并建立反向 SSH 隧道。通告写明，除了 Cursor 以管理员权限启动这类少见情况，恶意代码自身有错误，这一步会失败。
3. 尝试把反向隧道做成持久化：macOS 用 LaunchAgent，Windows 用计划任务（试图以 SYSTEM 运行），失败则退到启动脚本。后台脚本大约每 60 秒重试一次。

通告同时说明：攻击者的服务器后来已经下线，反向 shell 和主机信息上报不再可用；在多数没有管理员权限的 macOS 和 Windows 上，打开 SSH 服务会失败，攻击者当时不能通过隧道登录。即便如此，扩展仍然可能已经写入公钥、装上持久化，并送出主机信息。通告要求只要中招就按处置步骤做，不要因为隧道没建成就跳过。

Cursor 写明他们已从市场撤下这两个版本、暂时关闭整个市场、审计后确认没有其他扩展被篡改，然后轮换密钥并恢复市场。页末更新时间是 2026-10-30 11:30 am PT。

Hacker News 上有一条讨论，标题是 “Backdoor in Claude Code for VS Code extension on the Cursor Marketplace”（[item 50300683](https://news.ycombinator.com/item?id=50300683)）。2026-10-31 查询 Firebase API 时为 771 分、482 条评论。帖子链到的是第三方分析 [Phorion](https://phorion.io/blog/offical-claude-code-vsx-compromise/)，不是 Cursor 通告本身。下文的失陷指标只引用 Cursor 通告，不采用第三方文章里的额外数字。

## 自查：svc-telemetry

通告给出的快速检查，是看 SSH 授权文件里有没有标记为 `svc-telemetry` 的攻击者公钥。

macOS：

```bash
grep -qs svc-telemetry ~/.ssh/authorized_keys && echo "svc-telemetry key found" || echo "No key found; machine not impacted"
```

Windows PowerShell：

```powershell
$files = "$HOME\.ssh\authorized_keys", "C:\ProgramData\ssh\administrators_authorized_keys" | Where-Object { Test-Path $_ }
if ($files -and (Select-String svc-telemetry $files)) { "svc-telemetry key found" } else { "No key found; machine not impacted" }
```

输出 `No key found; machine not impacted` 表示这两个位置没有这串标记。输出 `svc-telemetry key found` 表示这台机器已受影响，按下一节处置。

通告点名的安装包是 Windows 和 macOS。失陷指标里另外列了 Linux 路径。Linux 上如果没有从 Cursor 市场装过那两个版本，不要把“已经中招”当成默认结论。仍可以在 `~/.ssh/authorized_keys` 里搜索 `svc-telemetry`，这是把通告里的检查字符串用到通告列出的路径上，通告原文没有单独给一条 Linux 命令。

通告里的 SSH 指标还包括：

- 公钥注释：`svc-telemetry`
- 未授权公钥指纹：`SHA256:0Z6R+DF64Do2nwQic8a7kkfDLNNk4IiK+2U2Rci4htk`
- 反向隧道密钥指纹：`SHA256:KOAU57+ZG6u3MG4WwzPzPX2O5YEe9qdOC1Bl+6MVyDQ`
- 公钥全文以 `ssh-ed25519` 开头，注释为 `svc-telemetry`。完整一行以通告页面为准，这里不改写。

文件和持久化路径，按通告原文：

| 系统 | 通告列出的位置 |
|---|---|
| Linux / macOS | `~/.ssh/authorized_keys`，`~/.config/.smt`，`~/.config/.smtk` |
| Linux | `/tmp/.stk_` 后接 10 位十六进制；cron `@reboot` 执行 `~/.config/.smt` |
| macOS | `$TMPDIR/.stk_` 后接 10 位十六进制；`~/Library/LaunchAgents/com.apple.sysmond.plist`（label `com.apple.sysmond`） |
| Windows | `%USERPROFILE%\.ssh\authorized_keys`，`%USERPROFILE%\.config\smt.cmd`，`%USERPROFILE%\.config\smtk`，`%TEMP%\.stk_` 后接 10 位十六进制；计划任务 `SysMon`；回退启动项 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\sysmon.cmd` |

网络指标在通告里写成带方括号的地址 `134[.]209[.]82[.]225`，反向 SSH 用户是 `tunnel`，端口 TCP 22，另有 8099 端口的 beacon。访问 ifconfig.me 或 api.ipify.org 本身不是指标，通告写明这两处是正常的公网 IP 查询。

进程特征包括 `ssh -N -R`、`autossh -M 0`，以及 `schtasks /create /tn SysMon`、`systemsetup -setremotelogin on`。这些是用来辨认的命令行，不是要你执行的修复命令。

包哈希、payload 哈希以通告页面的 “Indicators of compromise” 为准。2.1.312 和 2.1.313 各有 darwin-arm64 与 win32-x64 的 VSIX 哈希。通告没有列出 Linux 安装包。

## 核对 Codex 扩展

官方扩展要同时对上这几项，缺一项就不要装：

| 核对项 | 2026-10-31 看到的官方值 |
|---|---|
| 标识符 | `openai.chatgpt` |
| 显示名 | Codex – OpenAI’s coding agent |
| Visual Studio Marketplace 发布者 | OpenAI，域名 openai.com，Gallery API 里 `isDomainVerified` 为 true |
| 版本 | `26.51021.22027` |
| Marketplace 版本更新时间 | 2026-10-23 21:27 UTC（北京时间 2026-10-24 05:27） |
| 引擎 | `^1.96.2` |

同一天，Marketplace 页面显示 **16,214,174** 次安装，页面说明这个数字不含更新。Gallery API 的 `install` 字段是 **16,181,564**。两个计数不一致，而且都会变。安装量不能用来判断是不是官方扩展，标识符和已验证发布者才可以。

[Open VSX](https://open-vsx.org/extension/openai/chatgpt) 上，命名空间是 `openai`，`verified` 为 true，版本同样是 `26.51021.22027`，时间戳 `2026-10-26T20:54:33Z`（北京时间 2026-10-27 04:54），`downloadCount` 为 **12,919,792**。API 里的 `publishedBy` 是 GitHub 账号 `shijie-oai`，不是页面上再单独写一个公司名 “OpenAI”。核对时看命名空间、verified 和版本，不要只看显示名。

官方 IDE 文档给出的安装入口是：

- VS Code：`vscode:extension/openai.chatgpt`
- Cursor：`cursor:extension/openai.chatgpt`
- Windsurf：`windsurf:extension/openai.chatgpt`
- VS Code Insiders：同一条 Marketplace 页面 `https://marketplace.visualstudio.com/items?itemName=openai.chatgpt`

Marketplace 页面上的快速安装命令是：

```text
ext install openai.chatgpt
```

在 VS Code 里按 Ctrl+P（macOS 为 Cmd+P）打开 Quick Open，粘贴后回车。

搜索 “Codex” 会出现同名或近名的第三方扩展。只安装标识符正好是 `openai.chatgpt`、发布者域名核对通过的那一个。

本次没有打开 Cursor 市场页面，没有核对 Cursor 市场里 `openai.chatgpt` 的实时版本号。Cursor 通告的审计结论是没有其他扩展被篡改。这不能代替你自己看本机已装扩展的标识符。

## 用命令列出已装扩展

VS Code 文档中的命令：

```bash
code --list-extensions --show-versions
```

在输出里找 `openai.chatgpt`。2026-10-31 的市场版本是 `26.51021.22027`。之后市场还会更新，本机版本可以比这个新，但不能是另一个标识符。

Cursor 和 Windsurf 如果带了兼容的命令行，常见写法是 `cursor --list-extensions --show-versions`、`windsurf --list-extensions --show-versions`。本文没有在这两款编辑器里执行这两条命令。编辑器里也可以打开扩展详情，看标识符和版本。

命令面板里打开侧栏的命令，官方 IDE 文档写的是 `Codex: Open Codex Sidebar`。

## 自动更新要不要关

VS Code 默认会更新扩展。文档写明：

- 可以用命令 **Disable Auto Update for Extensions** 关掉全部自动更新，再用 **Enable Auto Update for Extensions** 打开。
- 也可以在某个扩展上右键，切换 **Auto Update**。
- 设置项 `extensions.autoUpdate` 控制这个行为，组织策略可以覆盖它。
- `extensions.autoUpdateDelay` 的默认值是 12 小时。自动更新开启时，VS Code 会等这段时间再装。设为 `0` 会在发布后尽快安装。扩展页上的 **Update** 按钮不受这个延迟限制。

这次事件发生在 Cursor 市场里的 Claude Code 包，不是 VS Code 市场上的 `openai.chatgpt`。关掉自动更新不能清除已经写入的公钥或持久化文件。它只减少以后自动装上未核对更新的机会。官方扩展仍应在核对标识符之后更新。

## 中招后怎么处理

通告的适用条件是：2026-10-29 的上述时间窗内，在 macOS 或 Windows 上，从 Cursor 市场安装或更新到 Anthropic.claude-code 2.1.312 或 2.1.313。

通告要求的顺序是：

1. 用上面的命令，或通告页面附带的检查脚本，确认是否受影响。
2. 在终端、网络和扩展安装记录里搜索通告列出的指标。
3. 把有载荷执行或后门安装痕迹的主隔离。
4. 删除未授权 SSH 公钥、持久化项和正在运行的隧道进程，并评估这台机器要不要重装。通告写明卸载扩展可能不够，因为载荷会留下独立的持久化脚本。
5. 从一台可信的系统，轮换受影响主机能够访问的凭据和会话。通告写明，当时收集的环境变量范围有限，但不能排除后来通过后门再取凭据。

通告提供两个处置脚本，要从通告页面下载，不要用别处转载的副本：

- macOS：以受影响的用户身份运行 `bash remediate-macos.sh`，不要用 root。
- Windows：用“以管理员身份运行”的 PowerShell，执行 `powershell -ExecutionPolicy Bypass -File .\remediate-windows.ps1`。

通告写明脚本会删除恶意扩展、持久化、正在运行的隧道进程和攻击者公钥；若仍有残留，脚本以非零状态退出。脚本正文以通告页面当时提供的文件为准，本文不转载。

进一步问题，通告写的联系地址是 security@cursor.com。

## 日常防护

- 安装前看标识符 `openai.chatgpt` 和已验证发布者，不按搜索结果里的名字“Codex”点击。
- 扩展详情里的版本，和 Marketplace 或 Open VSX 上的当前版本对一下。对不上就先不要启用。
- 本机用 `code --list-extensions --show-versions` 留一份记录，更新后再对一次。
- 第三方 Skill、插件和 MCP 另有权限边界。扩展市场事件不会把沙箱风险一起解释完，见 [Codex 沙箱与主机权限](./08-Codex沙箱与主机权限风险.md) 和 [用 HOL Guard 做插件安全检查](../13-社区生态与项目评测/01-Codex插件安全检查-HOL-Guard.md)。
- 密钥、令牌不要放进 Codex 对话。自查时也不要把 `authorized_keys` 全文贴到聊天里。

## 常见问题

**只在 VS Code 官方市场装过 Codex，要按通告轮换密钥吗？** 通告的处置对象是装过那两个 Claude Code 版本的机器。自查没有 `svc-telemetry`，也没有通告里的持久化文件时，不需要按中招流程轮换。标识符仍然要核对。

**Open VSX 上的发布账号不是 “OpenAI” 三个字，还能装吗？** 2026-10-31 的 API 显示命名空间 `openai`、`verified: true`、版本与 Marketplace 相同，发布记录挂在 GitHub 用户 `shijie-oai`。这和 Marketplace 上的公司发布者展示不一样。安装前同时看命名空间、verified 和版本。对不上就停。

**Linux 需要跑 Windows 那段 PowerShell 吗？** 不需要。通告的 PowerShell 是给 Windows 的。Linux 只在失陷指标里出现路径，没有单独的受影响 VSIX 版本号。

## 下一步

装或重装编辑器扩展时，按 [VS Code、Cursor 和 Windsurf 安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md) 做，每一步都核对 `openai.chatgpt`。

## 参考资料

- [Cursor：Claude Code 扩展安全通告](https://cursor.com/blog/claude-code-extension-security-notice)
- [OpenAI：Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [Visual Studio Marketplace：openai.chatgpt](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)
- [Open VSX API：openai/chatgpt](https://open-vsx.org/api/openai/chatgpt)
- [VS Code：Extension Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)
- [Hacker News 讨论 50300683](https://news.ycombinator.com/item?id=50300683)（第三方帖，链到 Phorion 的分析；指标不以该文为准）
