---
id: codex-cli-multi-entry-setup
title: Codex CLI 安装、登录与多入口配置（2026-10 更新）：ChatGPT 登录、API Key 登录、IDE 扩展与第三方模型
seo_title: Codex CLI 安装与登录：ChatGPT 登录、API Key 登录、IDE 扩展怎么配
description: 一篇讲清 Codex CLI 的安装、登录和多入口：四种官方安装方式，ChatGPT 登录和 API Key 登录的区别与命令，远程和无浏览器环境怎么登录，凭证存在哪，IDE 扩展怎么装，以及接第三方模型该用 model_providers。登录命令在 0.165.0 实测。
lede: 先选入口，再选登录方式。两种登录方式的计费完全不同，这是最常踩的坑。
url: /guides/codex-cli-multi-entry-setup
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, IDE, App]
difficulty: 基础
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-20
date_modified: 2026-10-29
verified_on: 2026-10-29
tested_cli_version: 0.165.0
official_ref: https://learn.chatgpt.com/docs/auth
keywords: [Codex CLI 安装, Codex 登录, Codex API Key 登录, codex login, Codex VS Code 扩展]
faq:
  - q: 用 Codex CLI 必须订阅 Plus 吗？
    a: 用 ChatGPT 账号登录的话，按官方 Pricing 页，个人方案里从 Plus 开始包含 CLI 和 IDE 扩展；Free 和 Go 目前只列了桌面端的 GPT-6 Luna，而且是逐步开放。不想订阅也可以用 OpenAI API Key 登录 CLI，按标准 API 价格计费。
  - q: ChatGPT 登录和 API Key 登录有什么区别？
    a: ChatGPT 登录用的是订阅包含的 Codex 用量上限和 credits；API Key 登录按 API 标准价格从你的 API 组织扣费，不占订阅额度，但一些依赖 ChatGPT 工作区或云端服务的功能受限或不可用，Codex cloud 只支持 ChatGPT 登录。
  - q: 远程服务器上没有浏览器，怎么用 ChatGPT 账号登录？
    a: 优先用设备码登录 codex login --device-auth（需要先在 ChatGPT 安全设置里开启）。不行的话，可以用 SSH 把本地 1455 端口转发过去，或者在有浏览器的机器上登录后，把 ~/.codex/auth.json 复制过去。
  - q: 接第三方或自建模型，要手改 auth.json 吗？
    a: 不要。auth.json 是 Codex 自己维护的登录缓存。接其他模型服务应该在 config.toml 里定义 model_providers，用 env_key 指定从哪个环境变量读 Key。
  - q: ChatGPT Pro 送的 API 额度能用来付 API Key 登录的 Codex 费用吗？
    a: 不能。官方写明这项权益不覆盖通过 API Key 使用 Codex 的用量。
related: [macos-install-codex-cli, codex-custom-model-provider, codex-chatgpt-subscription-api-credits, codex-doctor]
---

# Codex CLI 安装、登录与多入口配置（2026-10 更新）：ChatGPT 登录、API Key 登录、IDE 扩展与第三方模型

> 本文在线版：[codexguide.io/guides/codex-cli-multi-entry-setup](https://codexguide.io/guides/codex-cli-multi-entry-setup)

> 核对依据：OpenAI 官方文档 [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)、[Authentication](https://learn.chatgpt.com/docs/auth)、[Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide) 和 [Pricing](https://learn.chatgpt.com/docs/pricing)。「API Key 登录」一节在 Linux 上用 `codex-cli 0.165.0`、一个单独的 `CODEX_HOME` 和一把**假的** Key 实测，命令输出原样贴出；ChatGPT 账号登录和 IDE 步骤按官方文档整理，本机没有浏览器登录和桌面 App，没有截图。核对日期 2026-10-29（北京时间）。
>
> 2026-10-29 改写说明：旧版按个人经验写成，订阅要求没区分登录方式，还有「手写 auth.json 接第三方 API」这类有风险的做法，这一版按官方文档和实测重写。

## 先选入口

Codex 有好几个入口，登录信息大部分是共用的：

| 入口 | 适合 | 安装 |
|---|---|---|
| **Codex CLI**（终端） | 习惯终端、要接脚本和 CI、在远程服务器上干活 | 本文「安装 Codex CLI」 |
| **IDE 扩展**（VS Code、Cursor、Windsurf） | 边看代码边改，想直接用编辑器里打开的文件和选中内容 | 本文「IDE 扩展」 |
| **Xcode、JetBrains** | 用这两类 IDE 的人 | 各自 IDE 自带的集成，见[Xcode 中使用 Codex](../01-安装与首次使用/10-Xcode中使用Codex.md)、[JetBrains 中使用 Codex](../01-安装与首次使用/11-JetBrains中使用Codex.md) |
| **ChatGPT 桌面端** | 想要图形界面、多任务并行 | 见[安装路线总览](../01-安装与首次使用/01-安装路线总览.md) |
| **Codex cloud** | 把任务交给云端跑 | 只支持 ChatGPT 账号登录 |

官方文档写明：CLI 和 IDE 扩展**共用同一份登录缓存**，在其中一个退出登录，另一个下次启动也要重新登录。

## 安装 Codex CLI

官方给了四种方式，任选一种。

**macOS / Linux：官方安装脚本**

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

**Windows：PowerShell 安装脚本**（在新开的 PowerShell 窗口里运行）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

**npm**

```bash
npm install -g @openai/codex
```

**Homebrew**

```bash
brew install --cask codex
```

更新：安装脚本重新运行一遍即可；npm 用同一条命令；Homebrew 用 `brew upgrade --cask codex`。

装好以后确认版本：

```bash
codex --version
```

```text
codex-cli 0.165.0
```

分系统的详细步骤（含 WSL）见[macOS 安装 Codex CLI](../01-安装与首次使用/04-macOS安装Codex-CLI.md)和[Windows 和 WSL 安装 Codex CLI](../01-安装与首次使用/05-Windows和WSL安装Codex-CLI.md)。

## 两种登录方式，计费完全不同

| | ChatGPT 账号登录 | API Key 登录 |
|---|---|---|
| 怎么付费 | 用订阅包含的 Codex 用量上限和 credits | 按 OpenAI API 标准价格，从你的 API 组织扣费 |
| 需要什么 | ChatGPT 账号 | [OpenAI Platform](https://platform.openai.com/api-keys) 上的 API Key |
| 功能 | 完整 | 本地工作可以用；依赖 ChatGPT 工作区或云端服务的功能受限或不可用；Codex cloud 不能用 |
| 数据规则 | 跟随 ChatGPT 工作区的权限和数据设置 | 跟随 API 组织的数据保留和共享设置 |
| 适合 | 日常交互使用 | 脚本、CI/CD 等程序化场景 |

关于「必须订阅 Plus 才能用」：要分登录方式看。按官方 [Pricing](https://learn.chatgpt.com/docs/pricing) 页（2026-10-29 核对）：

- **ChatGPT 账号登录**：个人方案里，Plus 是列出「网页版、CLI、IDE 扩展、iOS」的最低一档；Pro 包含 Plus 的全部内容，分 100、200、500 美元三档；Business、Enterprise、Edu 走团队方案。Free 和 Go 目前只列了「桌面端使用 GPT-6 Luna（标准速度），逐步开放」，没有列 CLI。
- **API Key 登录**：不需要 ChatGPT 订阅，CLI 按 API 标准价格计费，官方定位是 CI 这类共享环境里的自动化。

方案内容会调整，以官方页面为准。

另一个容易混的点：ChatGPT Pro 和 Business 订阅送的 **API 额度**不能用来支付 API Key 登录 Codex 的费用，见[Codex 与 ChatGPT 订阅 API 额度](../10-配置模型与权限安全/16-Codex与ChatGPT订阅API额度-Pro和Business每月额度怎么领能不能用在Codex.md)。

## 登录方式一：ChatGPT 账号

在项目目录运行 `codex`，第一次会让你选登录方式，选 **Sign in with ChatGPT**。也可以直接：

```bash
codex login
```

Codex 会打开浏览器，登录后浏览器把凭证交回终端。登录过程中，Codex 在本机 `localhost:1455` 起一个回调服务接收结果。登录会话在使用中会自动刷新，一般不用反复登录。

图形界面的详细步骤见[登录 Codex](../01-安装与首次使用/07-登录Codex.md)。

## 登录方式二：API Key（0.165.0 实测）

官方推荐的写法是从标准输入读 Key，避免 Key 出现在命令行参数和 shell 历史里：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

下面是用一把**假 Key** 在 0.165.0 上的完整实测输出（Key 尾号是假的）。

登录前：

```text
$ codex login status
Not logged in
```

（退出码 1）

登录：

```text
$ printenv OPENAI_API_KEY | codex login --with-api-key
Reading API key from stdin...
API key saved. Authentication is checked when you send a request.
```

注意最后一句：**保存时不校验 Key 是否有效**，要等第一次真正发请求才知道。

查看状态（Key 中间部分被自动隐藏）：

```text
$ codex login status
API key configured - sk-proj-***00000
Authentication is checked when you send a request.
```

保存位置：默认写进 `$CODEX_HOME/auth.json`（默认 `~/.codex/auth.json`），实测文件权限是 `600`，里面记录的登录方式是 `"auth_mode": "apikey"`。

退出登录：

```text
$ codex logout
Successfully logged out
```

退出后 `auth.json` 被删除，`codex login status` 又回到 `Not logged in`。

在 IDE 扩展里用 Key：未登录界面选 **Use API Key**，输入后点 **OK**。桌面端选 **Sign in another way**，输入 Key 后点 **Continue**。

## 远程服务器、无浏览器环境怎么登录

在 SSH 远程机器、容器里用 ChatGPT 账号登录时，浏览器回调可能走不通。官方给了三种办法，按顺序试：

**1. 设备码登录（beta，首选）**

先在 ChatGPT 的安全设置里开启设备码登录（个人账号自己开；工作区由管理员在权限里开），然后：

```bash
codex login --device-auth
```

在浏览器里打开它给的链接，登录后输入一次性代码。交互界面里也可以选 **Sign in with Device Code**。

**2. SSH 转发回调端口**

在你本地电脑上：

```bash
ssh -L 1455:localhost:1455 user@remote
```

然后在这个 SSH 会话里运行 `codex login`，在本地浏览器打开它打印的地址。

**3. 复制登录缓存**

在有浏览器的机器上 `codex login`，然后把 `~/.codex/auth.json` 复制到远程机器的同一位置：

```bash
ssh user@remote 'mkdir -p ~/.codex'
scp ~/.codex/auth.json user@remote:~/.codex/auth.json
```

**`auth.json` 相当于密码**：里面有访问令牌，不要提交到仓库、贴进工单或发到聊天里。如果你的系统把凭证存在系统凭证库而不是这个文件里，这个办法不适用，见下一节。

脚本和 CI 里，官方仍然推荐默认用 API Key。

## 凭证存在哪

用 `config.toml` 里的 `cli_auth_credentials_store` 控制：

```toml
# file | keyring | auto | ephemeral
cli_auth_credentials_store = "keyring"
```

| 取值 | 行为 |
|---|---|
| `file` | 存在 `CODEX_HOME` 下的 `auth.json`（默认 `~/.codex`） |
| `keyring` | 存在系统凭证库；凭证库不可用时直接失败 |
| `auto` | 有系统凭证库就用，没有就退回 `auth.json` |
| `ephemeral` | 只存在当前进程的内存里 |

公司或团队管理的环境，管理员可能强制了登录方式（`forced_login_method = "chatgpt"` 或 `"api"`）或指定工作区。登录方式不符合时，Codex 会自动退出登录并退出。

登录失败要排查时，直接运行 `codex login` 会在日志目录下写一个 `codex-login.log`。

## 公司网络和证书

如果公司网络用了 TLS 代理或私有根证书，登录前设置 `CODEX_CA_CERTIFICATE` 指向 PEM 证书包：

```bash
export CODEX_CA_CERTIFICATE=/path/to/corporate-root-ca.pem
codex login
```

没设置时 Codex 会读 `SSL_CERT_FILE`。登录、普通 HTTPS 请求和 WebSocket 连接都用这套证书设置。

关于地区：OpenAI 的服务只在支持的国家和地区提供，本文不提供绕过地区限制的方法。连接经常断开、一直 Reconnecting 的排查见[Codex 一直 Reconnecting 排查](../15-故障排查与常见问题/03-Codex一直Reconnecting-stream-disconnected排查.md)；安装、配置、登录和网络的一键自检见[Codex doctor 自检](../15-故障排查与常见问题/04-Codex-doctor自检-安装配置登录与网络排查.md)。

## IDE 扩展

官方文档：VS Code 及其兼容编辑器用 Codex 扩展；Xcode 和 JetBrains 用各自的集成。

1. **安装**：VS Code、Cursor、Windsurf 在扩展市场搜 Codex（扩展 ID `openai.chatgpt`），或从 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt) 安装。
2. **打开**：点侧边栏的 Codex 图标。找不到的话，打开命令面板运行 **Codex: Open Codex Sidebar**。
3. **登录**：选 **Sign in with ChatGPT**，或选 **Use API Key**。已经在 CLI 登录过的，扩展会用同一份登录缓存。

详细步骤见[VS Code 和兼容编辑器安装 Codex](../01-安装与首次使用/06-VS-Code和兼容编辑器安装Codex.md)。

关于 Cursor：在 Cursor 里装的是同一个 Codex 扩展，登录和计费规则跟上面一样。Cursor 自己的模型选择属于 Cursor 的功能，计费走 Cursor 的方案或你在 Cursor 里填的 Key，不在本文范围内。

## 接第三方或自建模型：用 model_providers

如果你要通过公司的模型网关、LLM 代理或其他兼容服务使用 Codex，**不要手改 `auth.json`**。正确做法是在 `config.toml` 里定义一个模型提供商，并选择它的认证方式：

- `requires_openai_auth = true`：仍用 OpenAI 登录（ChatGPT 或 API Key），适合通过代理访问 OpenAI 模型。此时 `env_key` 会被忽略。
- `env_key = "环境变量名"`：从你指定的环境变量读这个服务商的 Key。
- `[model_providers.<id>.gateway_oauth]`：通过公司身份系统在浏览器登录网关。
- `[model_providers.<id>.auth]`：从本机安装的凭证助手命令获取令牌。
- 不需要凭证的本地模型：上面这些认证设置都不写。

```toml
model_provider = "mygateway"

[model_providers.mygateway]
name = "My Gateway"
base_url = "https://gateway.example.com/v1"
env_key = "MYGATEWAY_API_KEY"
```

上面的服务地址和名称只是示意。注意 `wire_api` 目前只支持 `responses`（不写时就是它），也就是说对方服务需要兼容 OpenAI Responses 接口。完整字段、请求到底发去哪、怎么验证，见[Codex 自定义模型提供商](../10-配置模型与权限安全/13-Codex自定义模型提供商-model_providers与openai_base_url.md)。

## 常见问题

| 现象 | 先查什么 |
|---|---|
| `codex: command not found` | 安装脚本或 npm 的安装目录不在 `PATH` 里；新开一个终端再试 |
| `codex login status` 显示已配置 API Key，但请求报认证错误 | 保存时不校验 Key；检查 Key 是否被撤销、是否属于正确的组织和项目 |
| 用 API Key 登录后某些功能不见了 | 正常，部分依赖 ChatGPT 工作区或云端的功能不支持 API Key 登录，见 [Pricing 的功能对比](https://learn.chatgpt.com/docs/pricing#feature-availability) |
| 部分插件用不了 | API Key 登录只支持部分 OpenAI 官方插件，有些插件的连接流程需要 API Key 登录不支持的 OAuth 能力 |
| 登录后被自动退出 | 管理员可能强制了登录方式或工作区，问管理员 |
| 远程机器上浏览器登录卡住 | 用设备码登录，或 SSH 转发 1455 端口 |

更多安装和登录问题见[安装登录常见问题](../01-安装与首次使用/13-安装登录常见问题.md)。

## 下一步

- 分系统安装：[macOS 安装 Codex CLI](../01-安装与首次使用/04-macOS安装Codex-CLI.md)
- 图形界面登录：[登录 Codex](../01-安装与首次使用/07-登录Codex.md)
- 接其他模型服务：[Codex 自定义模型提供商](../10-配置模型与权限安全/13-Codex自定义模型提供商-model_providers与openai_base_url.md)

## 参考资料

- OpenAI 官方文档：[Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- OpenAI 官方文档：[Authentication](https://learn.chatgpt.com/docs/auth)
- OpenAI 官方文档：[Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- OpenAI 官方文档：[Pricing](https://learn.chatgpt.com/docs/pricing)
