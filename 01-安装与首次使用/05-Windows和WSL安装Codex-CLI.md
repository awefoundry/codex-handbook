---
id: windows-wsl-install-codex-cli
title: Windows 和 WSL 安装 Codex CLI（2026-11 更新）：签名 PowerShell 安装脚本、npm 与 WSL2 怎么选
seo_title: Windows 和 WSL 安装 Codex CLI：install.ps1、npm 与 WSL2
description: 在 Windows 上安装 Codex CLI，可以用官方的 PowerShell 安装脚本、npm 全局包，或在 WSL2 里按 Linux 方式安装。本文说明三种方式的命令、下载源回退、安装后怎样验证，以及原生 Windows 和 WSL2 怎么选。
lede: 项目在 Windows 盘上、平时用 PowerShell，就用原生安装。工具链在 Linux 里，就在 WSL2 里安装。两套环境各有各的 codex。
url: /guides/windows-wsl-install-codex-cli
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 基础
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-07-12
date_modified: 2026-11-08
verified_on: 2026-11-08
tested_cli_version: 0.167.0
official_ref: https://github.com/openai/codex/blob/main/README.md
keywords: [Windows 安装 Codex CLI, WSL2, install.ps1, PowerShell 安装脚本, npm @openai/codex]
related: [windows-install-codex-app, windows-sandbox-mxc, codex-doctor, deng-lu-codex]
faq:
  - q: 这篇和 Windows 安装 Codex App 是同一件事吗？
    a: 桌面应用走 Microsoft Store、winget 或离线 MSIX，见《Windows 安装 Codex App》。本文只写终端里的 codex 命令。应用里的 Agent 也可以改到 WSL2，那是应用设置，不是这条 CLI 安装。
  - q: 本文在 Windows 上跑过 install.ps1 吗？
    a: 没有。写作环境是 Linux。2026-11-08 下载并阅读了 https://chatgpt.com/codex/install.ps1 ，确认了下载源回退和文件末尾的签名块，没有执行脚本，也没有运行 Get-AuthenticodeSignature。npm 上的 0.167.0 在这台 Linux 上安装后，codex --version 输出 codex-cli 0.167.0。
  - q: 签名是什么意思？
    a: 0.162.0 的发布说明写 “Publish a signed PowerShell installer with Windows releases”。当天下载的脚本末尾有 PowerShell 签名块。签名是否被 Windows 信任，要在 Windows 上用 Get-AuthenticodeSignature 看 Status。本文没有这项结果。
  - q: 本文的网址是什么？
    a: /guides/windows-wsl-install-codex-cli。本文只写 CLI 的三种安装。是否与现网的 /advanced/windows 互链，留到网站上线时再定。
---

# Windows 和 WSL 安装 Codex CLI（2026-11 更新）：签名 PowerShell 安装脚本、npm 与 WSL2 怎么选

> 本文在线版：[codexguide.io/guides/windows-wsl-install-codex-cli](https://codexguide.io/guides/windows-wsl-install-codex-cli)

> 核对依据：2026-11-08 的 [openai/codex README](https://github.com/openai/codex/blob/main/README.md)、[Codex CLI 文档](https://learn.chatgpt.com/docs/codex/cli)、[rust-v0.162.0](https://github.com/openai/codex/releases/tag/rust-v0.162.0) 发布说明里的 “Publish a signed PowerShell installer with Windows releases”。同一天 `npm view @openai/codex version` 的结果是 `0.167.0`。Linux 上用 npm 安装这个版本后，`codex --version` 输出 `codex-cli 0.167.0`。`install.ps1` 只下载阅读，没有在 Windows 或 WSL 里执行。没有新的终端截图。

Windows 上的桌面应用另有一篇：[Windows 安装 Codex App](./03-Windows安装Codex-App.md)。那篇写 Store、winget、离线 MSIX，以及应用里的 Agent 跑在原生 Windows 还是 WSL2。本文只写终端里的 `codex` 命令怎么装。

## 先看结论

两套环境各装各的，命令、PATH 和登录缓存默认不共用。

- 仓库在 `C:\` 或 `D:\`，工具是 Git for Windows、PowerShell、`npm`：用下面的 PowerShell 脚本或 Windows 上的 npm。
- 仓库和命令一直在 Ubuntu / WSL 里：在 WSL2 里用 Linux 安装脚本或 npm。
- 应用一文写明，WSL1 从 Codex 0.115 起不再支持 Linux 沙箱（`bubblewrap`）。需要 WSL 时安装 WSL2。这句话来自那篇对官方 Windows 应用页的整理，本文没有在 WSL1 上复测。

装完在**同一套**终端里运行 `codex --version`。登录见 [登录 Codex](./07-登录Codex.md)。

## 方式一：PowerShell 安装脚本

[openai/codex README](https://github.com/openai/codex/blob/main/README.md) 给 Windows 的命令是：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

`ByPass` 的大小写与 README 原文一致。这条命令会下载并执行 `https://chatgpt.com/codex/install.ps1`。公司电脑若禁止从网络执行脚本，先打开 [CLI 文档](https://learn.chatgpt.com/docs/codex/cli) 的 Windows 安装说明，再决定是否运行。

0.162.0（发布于 2026-10-08）的发布说明写的是：随 Windows 发布物提供已签名的 PowerShell 安装脚本，对应 PR #51158。2026-11-08 下载的 `install.ps1` 约 71 KB，正文结束后有 `# SIG # Begin signature block` 到 `# SIG # End signature block`。本文在 Linux 上不能代替 Windows 做签名校验。在你自己的 PowerShell 里，下载后可以先看状态再决定是否执行：

```powershell
$script = Join-Path $env:TEMP "codex-install.ps1"
Invoke-WebRequest https://chatgpt.com/codex/install.ps1 -OutFile $script
Get-AuthenticodeSignature $script | Format-List Status, SignerCertificate
```

`Status` 为 `Valid` 时，再按你的安全策略执行。本文没有这份 `Format-List` 的输出。

脚本开头的逻辑（阅读源码，不是运行日志）：

- 未设置 `CODEX_RELEASE` 时，安装 `latest`。
- 环境变量 `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM` 为空时，默认从 `https://releases.openai.com/codex` 取元数据和安装包。
- 该变量匹配 `1`、`true` 或 `yes`（不区分大小写）时，仍走 releases.openai.com。
- README 写：设为 `false` 时强制走 GitHub Releases；`0` 和 `no` 同样接受。这与脚本里「只有 1/true/yes 才为真」的判断一致。
- releases.openai.com 的元数据或安装包下载失败时，脚本会改从 GitHub Releases 解析。源码里的提示是 `releases.openai.com is unavailable; falling back to GitHub Releases.`

README 里强制走 GitHub 的写法是，在已经打开的 PowerShell 中：

```powershell
$env:CODEX_INSTALLER_USE_RELEASES_OPENAI_COM='false'; irm https://chatgpt.com/codex/install.ps1 | iex
```

脚本在成功路径上会打印当前会话可以使用 `codex`，并提示之后新的 PowerShell 窗口再运行 `codex`。这是源码里的 `Write-Step` 文本。本文没有看到它在 Windows 上实际打印出来。

## 方式二：npm

README 同时写了：

```powershell
npm install -g @openai/codex
```

先安装 [Node.js](https://nodejs.org/)（含 npm），关掉终端再开一次，使 `npm` 进入 PATH。两种安装选一种。已经用脚本装过、又用 npm 装一次时，用下一节的 `Get-Command` 看当前窗口实际调用的是哪一个 `codex`。

2026-11-08，`npm view @openai/codex version` 返回 `0.167.0`。在这台 Linux 上安装该版本后，`codex --version` 返回 `codex-cli 0.167.0`。Windows 上的 `npm install -g` 没有执行。npm 的全局目录和脚本安装的 `%LOCALAPPDATA%\Programs\OpenAI\Codex` 可能同时存在，以 `Get-Command` 的 `Source` 为准。

## 方式三：在 WSL2 里安装

还没有 WSL 时，用管理员身份打开 PowerShell。Microsoft 的安装文档给出的命令是：

```powershell
wsl --install
```

按提示重启，在 Ubuntu 里创建 Linux 用户。再检查版本：

```powershell
wsl --list --verbose
```

`VERSION` 一列应为 `2`。本文没有 Windows，没有这份列表的新输出。

在 WSL 的 Linux 终端里，CLI 文档和 README 的 macOS/Linux 命令是：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

没有 `curl` 时先安装它，再执行上面的脚本。也可以：

```bash
npm install -g @openai/codex
```

Linux 脚本同样默认从 releases.openai.com 下载，失败时回退 GitHub。README 里强制 GitHub 的写法是：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false sh
```

本文没有在 WSL 里执行 `install.sh`。

Windows 路径 `D:\work\demo` 在 WSL 里一般是 `/mnt/d/work/demo`。需要频繁编译的 Linux 项目，放在 WSL 自己的家目录（例如 `~/projects`）通常比放在 `/mnt` 上更合适。这条是使用建议，不是安装脚本的输出。

## 安装后验证

在**安装它的那一个**终端里：

```powershell
codex --version
Get-Command codex
```

WSL：

```bash
codex --version
command -v codex
```

能打印版本号，并且路径落在你预期的那一套环境里，安装才算完成。

需要看配置、登录和网络时，运行：

```text
codex doctor
```

`codex doctor` 的检查项、`--summary` 和 `--json` 见 [Codex doctor 自检](../15-故障排查与常见问题/04-Codex-doctor自检-安装配置登录与网络排查.md)。0.167.0 的 `codex doctor --help` 仍包含 `--summary`、`--json`、`--network-only`、`--ascii`。本文没有贴一份新的 doctor 报告。

然后进入项目目录运行 `codex`，按 [登录 Codex](./07-登录Codex.md) 完成 ChatGPT 或 API Key 登录。Windows 原生 CLI 和 WSL 里的 CLI 默认使用各自的家目录，登录状态不自动同步。

## Windows 沙箱

原生 Windows 上，CLI 的文件和网络隔离用 Windows 沙箱，而不是 WSL。MXC、`prefer_mxc`、elevated / unelevated 回退和官方验证命令见 [Codex Windows 沙箱](../10-配置模型与权限安全/09-Codex-Windows沙箱-启用MXC与elevated-unelevated回退.md)。那篇写明写作时没有 Windows 11 真机。本文同样没有。

WSL2 里的 CLI 使用 Linux 沙箱。应用一文记录的边界是：从 0.115 起 Linux 沙箱依赖 `bubblewrap`，WSL1 不在支持范围内。

## 排障

**找不到 `codex`。** 关掉当前窗口，新开一个 PowerShell 或 WSL 终端，再运行 `codex --version`。脚本源码自己也提示要为以后的窗口重新打开终端。

**`irm` 不是内部或外部命令。** 当前窗口是 CMD。打开 PowerShell，或使用 README 那条 `powershell -ExecutionPolicy ByPass -c "..."`，让它自己启动 PowerShell。

**Windows 和 WSL 各有一个版本。** 在 PowerShell 里看 `Get-Command codex -All`，在 WSL 里看 `command -v codex`。升级时升级你正在用的那一个。

**下载中断。** 先确认能打开 `https://chatgpt.com` 和 `https://releases.openai.com`。releases.openai.com 不可用时，脚本会按上一节回退到 GitHub；也可以显式设置 `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false`。重复执行同一条命令之前，先看失败提示是网络、签名还是 PATH。

**代理只配给了 npm。** `npm config set proxy` 不影响已经装好的 `codex` 进程。登录和网络症状的检查顺序见 [安装登录常见问题](./13-安装登录常见问题.md)。

## 参考资料

- [openai/codex README](https://github.com/openai/codex/blob/main/README.md)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [rust-v0.162.0](https://github.com/openai/codex/releases/tag/rust-v0.162.0)
- [Install WSL](https://learn.microsoft.com/windows/wsl/install)
- [Windows 安装 Codex App](./03-Windows安装Codex-App.md)
- [Codex Windows 沙箱](../10-配置模型与权限安全/09-Codex-Windows沙箱-启用MXC与elevated-unelevated回退.md)
- [Codex doctor 自检](../15-故障排查与常见问题/04-Codex-doctor自检-安装配置登录与网络排查.md)
