---
id: macos-install-codex-cli
title: macOS 安装 Codex CLI：官方脚本、npm、Homebrew 三种方式，登录并跑通第一个只读任务
seo_title: macOS 安装 Codex CLI：脚本、npm、brew --cask 与首次登录
description: 在 macOS 上用官方安装脚本、npm 全局包或 Homebrew Cask 安装 Codex CLI，完成 ChatGPT 或 API Key 登录，并在项目目录跑通第一个只读任务。命令对照 learn.chatgpt.com 现行文档，纠正缺少 --cask 与「必须 Plus」的旧说法。
lede: 三种安装方式选一种即可；装完先登录，再在项目目录发一条明确「不要改文件」的只读任务。
url: /guides/macos-install-codex-cli
status: draft
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 基础
order: 4
howto: true
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
client_validation_pending: true
official_ref: https://learn.chatgpt.com/docs/codex/cli
keywords: [macOS 安装 Codex CLI, Homebrew 安装 Codex, brew install --cask codex, npm @openai/codex, codex login]
related: [windows-wsl-install-codex-cli, deng-lu-codex, install-login-faq]
faq:
  - q: Homebrew 该写 brew install codex 还是带 --cask？
    a: 官方 Codex CLI 文档与 formulae.brew.sh/cask/codex 都要求 `brew install --cask codex`；更新用 `brew upgrade --cask codex`。不要省略 --cask。
  - q: 必须先买 ChatGPT Plus 才能用 CLI 吗？
    a: 不是。ChatGPT 登录可用 Plus、Pro、Business、Edu、Enterprise 等包含 Codex CLI 的套餐；也可以用 API Key 按量计费。Free／Go 的 Codex 能力以官方 Pricing 与你账号界面为准，不要照搬「必须 Plus」。
  - q: 官方脚本、npm、Homebrew 可以同时装吗？
    a: 可以并存，但 PATH 里只会先命中一份。`which -a codex` 若列出多条路径，更新或报错时常是在跑旧的那一份。三种方式选一种，装完再核对路径。
---

# macOS 安装 Codex CLI：官方脚本、npm、Homebrew 三种方式，登录并跑通第一个只读任务

> 本文计划路径：[codexguide.io/guides/macos-install-codex-cli](https://codexguide.io/guides/macos-install-codex-cli)

> 核对依据：learn.chatgpt.com《[Codex CLI](https://learn.chatgpt.com/docs/codex/cli)》《[Authentication](https://learn.chatgpt.com/docs/auth)》《[Pricing](https://learn.chatgpt.com/docs/pricing)》《[Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)》，以及 [Homebrew Cask：codex](https://formulae.brew.sh/cask/codex)、npm 包 `@openai/codex`。文中「我的用法」是操作建议，不是官方强制规定。本篇尚未在真实 Mac 终端逐条截图验证，故 `client_validation_pending: true`；命令以官方文档原文为准。

知识库原稿只是约 190 字的占位大纲。本文按官方现行安装页补全为可跟做教程，并顺带纠正站内旧文常见的两处错误：**Homebrew 漏写 `--cask`**，以及把 ChatGPT 登录说成 **「必须 Plus」**。

## 你要完成什么

在 macOS 上：

1. 用**一种**官方支持的方式装好 `codex` 命令；
2. 用 ChatGPT 登录或 API Key 完成认证；
3. 进入一个本地项目目录，跑通**第一个只读任务**（明确要求不改文件）。

桌面 App、VS Code／兼容编辑器扩展是另一条入口，见同栏目其它文章。本文只覆盖 **Codex CLI**。

## 开始前准备

| 项目 | 说明 |
| --- | --- |
| 系统 | 较新的 macOS；Apple Silicon 与 Intel 都可，安装渠道相同 |
| 终端 | 系统自带「终端」、iTerm2 或 Cursor／VS Code 集成终端均可；提示符是 `zsh` 或 `bash` 都可以 |
| 账号 | **ChatGPT 登录**：官方 Pricing 的功能表把 **Codex CLI** 列在 Plus、Pro、Business、Enterprise／Education，以及 **API Key** 列；npm／GitHub README 也写推荐用 Plus、Pro、Business、Edu 或 Enterprise 计划登录。**不是「只能 Plus」**。也可用 API Key 按 Platform 用量计费 |
| 网络 | 需能访问 ChatGPT／OpenAI 相关域名；公司代理或私有 CA 见文末排障 |

**不要**为了「装全」同时跑官方脚本、npm 和 Homebrew。先选一种；装完用 `which -a codex` 确认实际路径。

**我的用法**：本机已有 Node.js LTS、习惯用 npm 管全局工具 → 用 npm；更想少碰 Node → 用官方 `install.sh` 或已装 Homebrew 时用 `brew install --cask codex`。

## 三种安装方式怎么选

官方 [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) 在 macOS／Linux 下列出四种安装叙述：独立安装脚本、npm、Homebrew，以及（文档结构上并列的）Windows 脚本。macOS 日常用前三种即可。

| 方式 | 命令要点 | 适合 | 更新 |
| --- | --- | --- | --- |
| 官方脚本 | `curl … install.sh \| sh` | 不想依赖 Node／Homebrew | 再跑同一条安装命令 |
| npm | `npm install -g @openai/codex` | 已有 Node.js LTS | 再执行同一条 npm 安装／更新 |
| Homebrew Cask | `brew install --cask codex` | 已用 brew 管图形／CLI 工具 | `brew upgrade --cask codex` |

下面任选一节跟做，做完跳到「验证安装」。

## 方式一：官方安装脚本（推荐默认）

在终端执行（与官方文档一致）：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

这条命令会下载并执行官方安装脚本。默认从 `https://releases.openai.com/codex` 取包，必要时回退到 GitHub Releases。若你对「管道进 shell」敏感，先打开 [Codex CLI 文档](https://learn.chatgpt.com/docs/codex/cli)核对原文，再决定是否执行；也可以先把脚本下载到本地审阅后再 `sh`。

更新时官方写的是**再跑同一条安装命令**，不是另找神秘 `codex update`（是否提供 `update` 子命令以你本机 `codex --help` 为准）。

需要强制走 GitHub Releases 时，官方允许：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false sh
```

普通用户一般不必加这个环境变量。

安装结束后**新开一个终端窗口**，再继续验证。

## 方式二：npm 全局安装

电脑需先安装 [Node.js LTS](https://nodejs.org/)。装好后重新打开终端，确认：

```bash
node -v
npm -v
```

然后安装（官方写法）：

```bash
npm install -g @openai/codex
```

更新同样再执行：

```bash
npm install -g @openai/codex
```

或显式跟 latest：

```bash
npm install -g @openai/codex@latest
```

npm 全局目录因系统与权限而异。若提示权限错误，优先用 Node 官方安装器／nvm／fnm 把全局前缀放到用户目录，**不要**习惯性 `sudo npm install -g`，以免搞乱属主。

国内网络下 npm 注册表慢时，可用你信任的镜像加速，但包名仍必须是 `@openai/codex`，不要改用第三方同名包。

## 方式三：Homebrew（必须带 `--cask`）

先确认本机有 Homebrew：

```bash
brew --version
```

官方文档与 [formulae.brew.sh/cask/codex](https://formulae.brew.sh/cask/codex) 的安装命令是：

```bash
brew install --cask codex
```

更新：

```bash
brew upgrade --cask codex
```

**常见错误**：写成 `brew install codex`（漏掉 `--cask`）。站内旧文《Codex CLI 国内使用与多入口配置》里也曾出现无 `--cask` 的写法；以官方 CLI 页与 Homebrew Cask 页为准。Codex CLI 在 Homebrew 上是 **Cask** 产物，不是随便猜的 formula 名。

## 验证安装

不论用哪种方式，在新终端里执行：

```bash
codex --version
command -v codex
which -a codex
```

- 能打印版本号，说明命令可用；
- `which -a codex` 若出现**多条路径**，记住当前 `command -v codex` 指向的那一条，以后更新要沿同一渠道，避免「明明更新了却还是旧版本」。

当前公开包版本会随发布变化（例如 Homebrew Cask／npm 曾显示 `0.163.0` 一带）；**以你本机 `codex --version` 为准**，不要把文章里的示例版本号背成硬性要求。

## 登录

进入你要使用的项目目录（先 `cd` 进去），再登录。官方交互路径是：直接运行 `codex`，首次选择 Sign in with ChatGPT 或其它可用方式；也可以主动：

```bash
codex login
```

无参数时，CLI 打开浏览器走 ChatGPT OAuth。完成后可用：

```bash
codex login status
```

有凭据时退出码为 `0`，并显示当前认证模式。这只说明登录状态存在，**不等于**已经允许读写任意目录；目录与命令权限仍受沙箱／审批设置约束。

### 无浏览器／远程环境

官方提供设备码流程（beta）：

```bash
codex login --device-auth
```

使用前需在 ChatGPT 安全设置（个人）或工作区权限（管理员）中开启设备码登录。细节见 [Authentication](https://learn.chatgpt.com/docs/auth)。

### API Key（按量计费，可选）

没有 ChatGPT 订阅、或要在脚本／CI 里用 API 计费时：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

把 Key 放进环境变量，再管道传入；**不要**把 Key 写进命令历史、截图、仓库或聊天。API Key 走 Platform 计费，云端类功能会受限，见官方 Pricing「API Key」与 Feature availability。

### 和「必须 Plus」说法的关系

- **错误旧说法**：「要用 Codex CLI 必须先买 Plus。」
- **现行公开说明**：Pricing 写明 ChatGPT Work 与 Codex 包含在 Free、Go、Plus、Pro、Business、Edu、Enterprise 等计划中，但**各档能力不同**；功能表里 **Codex CLI** 明确列在 Plus／Pro／Business／Enterprise／Education 与 API Key。npm README 推荐用 Plus、Pro、Business、Edu 或 Enterprise 做 ChatGPT 登录。
- **正确表述**：用 ChatGPT 登录时，选**包含 Codex CLI 的套餐**（常见是 Plus 及以上个人／团队档，或以你账号实际入口为准）；也可用 API Key。不要写成「只有 Plus 能用」，也不要承诺 Free／Go 一定具备与 Plus 相同的 CLI／模型能力。

## 跑通第一个只读任务

登录成功后，仍在**项目根目录**（有 `README`、`package.json`、`Cargo.toml` 等可识别结构的地方更好）：

```bash
cd ~/path/to/your-project
codex
```

进入交互会话后，发送一条边界清楚的只读请求，例如：

```text
请阅读这个项目的目录结构和 README，不要修改任何文件，也不要运行会改写仓库的命令。用几段话说明：项目用途、主要技术栈、如何安装依赖、如何运行测试。
```

你应看到 Codex 在读文件、归纳结构，而不是开始改代码或提交。若它提出要改文件或执行写入类命令，先拒绝或收紧权限，再把任务重申为只读。

官方入门示例更短：「Tell me about this project」。中文读者用上面这段更不容易被理解成「可以顺手重构」。

**完成标准**：

- `codex --version` 有输出；
- `codex login status` 显示已认证；
- 只读任务返回了项目说明，且工作区文件未被改动（可用 `git status` 核对）。

## 更新时沿用原渠道

| 原安装方式 | 更新 |
| --- | --- |
| 官方脚本 | 再执行同一条 `curl … \| sh` |
| npm | `npm install -g @openai/codex`（或 `@latest`） |
| Homebrew Cask | `brew upgrade --cask codex` |

更新后重新打开终端，再跑 `codex --version` 与 `which -a codex`。卸载、清理 `~/.codex` 等见同栏目《Codex 更新与卸载》；Windows／WSL 命令见《Windows 和 WSL 安装 Codex CLI》。

## 常见问题

### 找不到 `codex` 命令

1. 关掉当前终端，新开一个再试；
2. `which -a codex`；
3. npm 安装时检查 `npm prefix -g` 是否在 `PATH`；
4. Homebrew 确认装的是 cask：`brew list --cask codex`。

### 登录时浏览器没弹出或回调失败

检查默认浏览器、弹窗拦截、代理与公司证书。公司 TLS 拦截时可按官方设置：

```bash
export CODEX_CA_CERTIFICATE=/path/to/corporate-root-ca.pem
codex login
```

未设置时 Codex 会回退到 `SSL_CERT_FILE`。无图形界面优先 `codex login --device-auth`。

### 装了却还是旧版本

多半是 PATH 上还有另一份安装。`which -a codex` 对照后，只保留一种渠道，或调整 PATH 顺序。

### 网络超时

系统代理不一定自动进终端。需要时在当前 shell 设置与你代理软件一致的 `HTTP_PROXY`／`HTTPS_PROXY`，再测：

```bash
curl -I https://learn.chatgpt.com/docs/codex/cli
codex --version
```

不要在网络不通时反复换安装渠道。

## 和桌面 App 的关系

- **CLI**：终端里的 `codex`，本文覆盖。
- **ChatGPT／Codex 桌面 App**：图形界面；macOS App 安装见同栏目对应篇。
- 两者登录凭据在官方说明里可与 IDE 扩展共享缓存；在一端 `codex logout` 可能影响另一端，换账号时先看清再退登。

## 参考资料

- [Codex CLI（安装与入门）](https://learn.chatgpt.com/docs/codex/cli)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Developer commands（含 `codex login`）](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Pricing／Feature availability](https://learn.chatgpt.com/docs/pricing)
- [Homebrew Cask：codex](https://formulae.brew.sh/cask/codex)
- [npm：@openai/codex](https://www.npmjs.com/package/@openai/codex)
- 同栏目：[登录 Codex](./07-登录Codex.md)、[Windows 和 WSL 安装 Codex CLI](./05-Windows和WSL安装Codex-CLI.md)、[安装登录常见问题](./13-安装登录常见问题.md)、[Codex 更新与卸载](./12-Codex更新与卸载.md)

官方资料核对日期：2026-10-22（Asia/Shanghai）。本篇未在真实 Mac 上截取终端／登录界面；上线前建议实机走通三种安装渠道之一并补脱敏截图。
