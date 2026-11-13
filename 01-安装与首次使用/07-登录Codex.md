---
id: deng-lu-codex
title: 登录 Codex（2026-11 更新）：ChatGPT 账号、API Key、Sign in another way 与凭据存储方式
seo_title: 登录 Codex：ChatGPT 账号、API Key 与凭据存储
description: Codex 可以用 ChatGPT 账号或 API Key 登录。桌面端把 API Key 放在 Sign in another way，IDE 扩展使用 Use API Key。本文说明三端步骤、MFA、cli_auth_credentials_store 的四种存法，以及怎样查看当前账号和工作区。
lede: 先选一个入口登录。ChatGPT 账号走浏览器，API Key 从标准输入或桌面端的另一条入口进入。凭据按密码保管。
url: /guides/deng-lu-codex
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 7
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-07-12
date_modified: 2026-11-08
verified_on: 2026-11-08
tested_cli_version: 0.167.0
official_ref: https://learn.chatgpt.com/docs/auth
keywords: [Codex 登录, Sign in another way, API Key 登录, cli_auth_credentials_store, MFA, 工作区]
related: [codex-switch-multiple-accounts, codex-access-tokens-service-accounts, codex-amazon-bedrock, windows-wsl-install-codex-cli]
faq:
  - q: 第一次本地练习用哪种登录？
    a: 用 ChatGPT 登录即可。Authentication 文档写这种方式使用订阅或工作区里的 Codex 权限。API Key 按 OpenAI Platform 的用量计费，留给你确实要按量付费或写进 CI 的时候。
  - q: CLI 和 IDE 扩展要登录两次吗？
    a: Authentication 文档写 CLI 和扩展共用同一份缓存。从其中一边退出后，下次再开 CLI 或扩展都要重新登录。桌面应用有自己的账号菜单。
  - q: /status 一定会显示工作区名字吗？
    a: CLI 0.166.0 的发布说明包含 #57366：在 /status 里显示当前选中的 ChatGPT 工作区。2026-11-08 的斜杠命令页仍把 /status 的预期输出写成模型、审批策略、可写根和 token 用量。本文没有登录，没有看到工作区那一行。
  - q: 为什么这篇没有登录截图？
    a: 写作环境没有完成 ChatGPT 或 API Key 登录，也没有桌面端。仓库里旧的 IDE 截图显示的是 GPT-5 时期的界面，没有放进这篇更新。
---

# 登录 Codex（2026-11 更新）：ChatGPT 账号、API Key、Sign in another way 与凭据存储方式

> 本文在线版：[codexguide.io/guides/deng-lu-codex](https://codexguide.io/guides/deng-lu-codex)

> 核对依据：2026-11-08 的 [Authentication](https://learn.chatgpt.com/docs/auth)、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)、[Sample Configuration](https://learn.chatgpt.com/docs/config-file/config-sample) 和 [Slash commands](https://learn.chatgpt.com/docs/cli/slash-commands)。CLI 行为来自 Linux 上的 `codex-cli 0.167.0`：`codex login --help` 与 `codex login status`。当时状态命令输出 `Not logged in`，退出码 1。没有打开桌面应用或 IDE，没有完成浏览器登录，没有配图。[0.167.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.167.0) 写了 “Sign in another way”。[0.166.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.166.0) 的 #57366 写了在 `/status` 中显示所选 ChatGPT 工作区。

本课只处理认证：选一个你已经安装好的入口，确认它认得出你的账号或 API Key。打开练习目录、读文件和改代码是下一课。Codex Cloud 的任务仍要 ChatGPT 登录，本课不把 Cloud 当作练习入口。

## 先看结论

Authentication 文档写，使用 OpenAI 模型时有两种个人登录：

- **Sign in with ChatGPT**：使用 ChatGPT 订阅或工作区提供的权限。用量遵守该工作区的权限、角色和 Enterprise 的保留与驻留设置。
- **API Key**：按 OpenAI Platform 的 API 价格计费。用量遵守 API 组织的保留和数据共享设置，不使用 ChatGPT 套餐内的额度。

本地的 ChatGPT 桌面应用、Codex CLI 和 IDE 扩展都支持这两种。Codex Cloud 要求 ChatGPT 登录。

桌面应用在未登录屏幕上，ChatGPT 登录是 **Continue to sign in**。API Key 是 **Sign in another way**，输入密钥后选 Continue。0.167.0 发布说明把 API Key 和云厂商选项放在 “Sign in another way” 下面，并写可以通过启用 `gcp_setup_wizard` 用应用默认凭证或凭证文件配置 Google Cloud Vertex AI。云厂商的具体向导见 [Codex 接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md) 和 [Codex 接入 Google Cloud Vertex AI](../12-官方工具与集成/13-Codex接入Google-Cloud-Model-Garden.md)。本文没有打开这个子菜单。

IDE 扩展的文档用词不同：ChatGPT 登录是 **Sign in with ChatGPT**，API Key 是 **Use API Key**，输入后选 OK。

CLI 不带参数的 `codex login` 打开浏览器。API Key 从标准输入读入，不在命令行参数里出现。

## App：浏览器完成 ChatGPT 登录

文档里的桌面应用步骤：

1. 在未登录屏幕选择 **Continue to sign in**。
2. 在打开的浏览器里完成 ChatGPT 登录。确认地址栏是 chatgpt.com 上的登录页。
3. 浏览器把凭据交回应用。回到原来的窗口。
4. 打开头像或资料菜单，确认当前账号和工作区。

文档写：浏览器登录完成后，凭据回到 Codex。按钮位置会随版本变化。本文没有一张 2026-11 的应用截图。

API Key 登录按文档是同一屏幕上的 **Sign in another way**。密钥从 [OpenAI 仪表板](https://platform.openai.com/api-keys) 获取。不要把密钥拍进截图。

## CLI：codex login

在已经安装 CLI 的终端里：

```bash
codex login
```

不带参数时，这是文档写的默认路径：打开浏览器做 ChatGPT OAuth。0.167.0 的 `codex login --help` 把这条命令写成 “Manage login”，并列出 `status` 子命令。

登录后：

```bash
codex login status
```

命令文档写：有凭据时退出码为 0。2026-11-08 未登录的输出是 `Not logged in`，退出码 1。有凭据只说明这台机器存着登录信息，不说明它已经可以读任意项目目录。

退出：

```bash
codex logout
```

命令文档写这个命令会清掉 API Key 和 ChatGPT 两套已保存凭据，并且没有自己的旗标。当进程改用工作负载身份时，文档写 Codex 会拒绝 `codex login` 和 `codex logout`，因为认证由进程环境决定。本文没有配工作负载身份，没有看到这条拒绝。

### API Key

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

0.167.0 的帮助把 `--with-api-key` 说明为从标准输入读密钥，示例与上面相同。不要把密钥写进命令行历史、仓库、提示词或截图。没有 API Key 需求时跳过这一节。

API Key 登录可以做本地 Codex 流程。依赖 ChatGPT 工作区或云服务的功能会受限或不可用，文档让读者到功能对照表里看套餐差异。CLI 和桌面应用里，API Key 可以使用受支持的 OpenAI 精选插件；有些插件的连接需要 API Key 登录所没有的 OAuth，那些插件不可用。见 [插件入口](../08-插件工作流/04-Codex插件入口与工作流.md)。

### 设备码

远程或无图形界面、或者本机网络挡住登录回调时，文档把设备码认证（beta）写在前面：

1. 在个人账号的 ChatGPT 安全设置，或工作区权限里，打开设备码登录。
2. 在交互登录界面选 **Sign in with Device Code**，或直接运行 `codex login --device-auth`。
3. 在浏览器打开终端给出的链接，登录，再输入一次性代码。

0.167.0 的帮助里有 `--device-auth`，说明文字是空的。步骤以上面的 Authentication 页为准。本文没有走设备码。

文档还写了两条退路：在有浏览器的机器上登录后，把文件形式的 `~/.codex/auth.json` 拷到无界面机器；或者用 SSH 把本机 `localhost:1455` 转发到远程，再在远程跑 `codex login`。凭据若在操作系统钥匙串里，拷贝 `auth.json` 这条不适用。把这个文件当成密码。具体命令以 Authentication 页为准，本文不重复粘贴。

### 企业访问令牌

ChatGPT Enterprise 工作区里，管理员可以授予访问令牌权限。成员创建的 Codex access token 用于受信任的脚本、定时任务和私人 CI，让自动化带着工作区权限运行，而不打开浏览器。普通 OpenAI API 调用仍用 Platform 的 API Key。创建、轮换和撤销见 [Codex 访问令牌与服务账号](../11-自动化与高级工作流/14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)。

已经有令牌时，文档的用法是：

```bash
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```

0.167.0 的帮助包含 `--with-access-token`，示例与此相同。本文没有 Business / Enterprise 工作区，没有创建令牌。

## IDE 扩展

在已安装的扩展里打开 Codex 侧栏：

- ChatGPT：选择 **Sign in with ChatGPT**，完成浏览器授权后回到编辑器。
- API Key：选择 **Use API Key**，输入密钥，选择 OK。

登录之后，侧栏从登录按钮变成可以输入任务的对话，才算这个入口可用。扩展的安装和按钮以 [IDE 扩展文档](https://learn.chatgpt.com/docs/codex/ide) 为准。本文没有打开 VS Code、Cursor 或 Windsurf。

Authentication 文档写：CLI 和 IDE 扩展共用缓存。从其中一边退出，下次启动另一边也要重新登录。

## 凭据存在哪：cli_auth_credentials_store

文档写，用 ChatGPT 或 API Key 登录桌面应用、CLI 或 IDE 扩展后，登录信息会缓存并复用。缓存位置是明文文件 `~/.codex/auth.json`，或操作系统的凭据存储。ChatGPT 会话在使用中会自动刷新令牌，所以持续使用时通常不必再次打开浏览器。

用 `cli_auth_credentials_store` 指定 CLI 的存储位置。Authentication 页的四个值是：

```toml
# file | keyring | auto | ephemeral
cli_auth_credentials_store = "keyring"
```

| 值 | 文档中的行为 |
| --- | --- |
| `file` | 存在 `CODEX_HOME` 下的 `auth.json`。`CODEX_HOME` 默认是 `~/.codex` |
| `keyring` | 存在操作系统凭据存储；存储不可用时失败 |
| `auto` | 有系统凭据存储就用它，否则回到 `auth.json` |
| `ephemeral` | 只留在当前进程的内存里 |

示例配置的注释把 `file` 标成 default，示例值也是 `"file"`。那一行注释只写了 `file | keyring | auto`，没有写 `ephemeral`。`ephemeral` 出现在 Authentication 页和配置参考里。本文没有修改配置，没有对比四种存储的实际文件。

使用 `file` 时，把 `~/.codex/auth.json` 当成密码：里面有访问令牌。不要提交到 Git，不要贴进 Issue 或聊天。怀疑 API Key 泄露时，到 OpenAI Platform 撤销并重新生成。

管理员可以通过本地认证要求强制 `cli_auth_credentials_store` 和 `chatgpt_base_url`。用户不能用 `config.toml` 或 CLI 覆盖这些要求。配置参考里，这条强制项来自本机系统要求文件或 macOS MDM；云托管的值会被忽略。

还可以限制登录方式和工作区：

```toml
forced_login_method = "chatgpt" # 或 "api"
forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"
```

当前凭据不符合时，文档写 Codex 会登出并退出。本文没有设置这两项。

直接运行 `codex login` 时，文档写会在配置的日志目录里写 `codex-login.log`，用来排查浏览器登录和设备码失败。公司代理使用私有根证书时，在登录前设置 `CODEX_CA_CERTIFICATE` 指向 PEM 包；未设置时回退到 `SSL_CERT_FILE`。

个人号和公司号要在 CLI 里完全分开时，用不同的 `CODEX_HOME`，见 [Codex 多账号切换](./16-Codex多账号切换-手机端双账号与CLI用CODEX_HOME分开登录.md)。

## MFA

Authentication 文档把 Codex Cloud 的多因素认证写成单独一节，因为云端会直接接触代码仓库。

- 使用 Google、Microsoft 或 Apple 社交登录时，不要求在 ChatGPT 账号上再开 MFA，可以在该社交登录提供商处设置。
- 通过 SSO 进入时，由组织的 SSO 管理员为所有用户强制 MFA。
- 使用邮箱和密码登录时，必须先在账号上设置 MFA，才能访问 Codex Cloud。
- 账号若同时支持多种登录方式，且其中一种是邮箱和密码，则在访问 Codex 之前必须设置 MFA。文档的原句包括 “even if you sign in another way”。这里的 “another way” 是 MFA 那一节的条件，和桌面端按钮 “Sign in another way” 写在不同的小节里。

本文没有触发 MFA 设置页。

## 查看当前账号和工作区

| 入口 | 文档写的查看方式 |
| --- | --- |
| ChatGPT 网页 | 打开资料菜单，确认账号和工作区；Log out 结束该浏览器里的会话 |
| 桌面应用 | 资料菜单显示当前账号或 API Key 状态；Log out 清除当前凭据 |
| CLI | `codex login status` 显示当前认证方式 |
| IDE 扩展 | 资料菜单显示当前账号或 API Key 状态；Log out 清除当前凭据 |

交互会话里，斜杠命令 `/status` 用来看会话配置。2026-11-08 的斜杠命令页写：查看当前模型、审批策略、可写根和 token 用量；TUI 连到远程时，还会显示远程地址和服务器版本。

0.166.0 发布说明的 #57366 是 “Show the selected ChatGPT workspace in `/status`”。发布说明和斜杠命令页的用词没有并成同一张字段表。本文没有登录，没有 `/status` 的输出，因此不描述工作区名字长什么样。需要换工作区或换账号时，用上面的资料菜单，或按多账号一文分开 `CODEX_HOME`。

## 登录失败时怎么排查

| 现象 | 先检查什么 |
| --- | --- |
| 没有打开浏览器 | 默认浏览器、弹窗拦截、网络和代理 |
| 浏览器成功，客户端仍未登录 | 回到原来的窗口；看 `codex-login.log`；必要时重新打开登录面板 |
| CLI 仍要求登录 | 在运行 Codex 的那个终端里执行 `codex login status`。Windows 原生和 WSL 的家目录默认各有一份配置，见 [Windows 和 WSL 安装 Codex CLI](./05-Windows和WSL安装Codex-CLI.md) |
| 设备码不可用 | 个人安全设置或工作区权限里是否已打开；`--device-auth` 的帮助文字在 0.167.0 上是空的，以 Authentication 页为准 |
| API Key 失败 | 密钥是否有效、组织是否允许调用。把密钥撤销后重发，不要把密钥发给别人排查 |
| 能登录但不能发起任务 | 工作区是否有 Codex 权限、额度是否用完。认证成功不等于产品权限已经打开 |
| 凭据立刻消失 | `cli_auth_credentials_store` 是否为 `ephemeral`；`keyring` 在系统凭据存储不可用时会失败 |

更完整的安装和网络症状见 [安装登录常见问题](./13-安装登录常见问题.md)。切换账号时用客户端的退出，再重新登录。不要为了换账号删掉整个配置目录。

## 完成检查

- [ ] 只登录了准备使用的那一个入口。
- [ ] 浏览器授权后回到了原来的 App、CLI 或 IDE。
- [ ] 资料菜单不再停在登录页，或 `codex login status` 退出码为 0。
- [ ] 知道凭据存在 `auth.json` 还是系统钥匙串，并且没有把令牌提交进 Git。
- [ ] 知道「已登录」和「可以读这个项目目录」是两件事。

完成后进入 [打开第一个本地项目](./08-打开第一个本地项目.md)。

## 参考资料

- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands)
- [IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Sample Configuration](https://learn.chatgpt.com/docs/config-file/config-sample)
- [Slash commands：/status](https://learn.chatgpt.com/docs/cli/slash-commands)
- [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)
- [rust-v0.167.0](https://github.com/openai/codex/releases/tag/rust-v0.167.0)
- [rust-v0.166.0](https://github.com/openai/codex/releases/tag/rust-v0.166.0)
