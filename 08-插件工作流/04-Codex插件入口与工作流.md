---
id: codex-chajian-rukou-yu-gongzuoliu
title: Codex 插件入口怎么用：桌面端 Plugins 目录、CLI /plugins 与权限边界
seo_title: Codex 插件入口：Plugins 目录、/plugins、安装与卸载
description: Codex 的插件在哪里装、装完怎么调用、卸载会留下什么？按官方 Plugins 文档整理桌面端 Plugins 目录和 CLI /plugins 的用法，附 Codex CLI 0.166.0 的 codex plugin 命令实测输出，并说明 IDE 扩展不支持、API Key 登录的限制和插件 Hook 的信任规则。
lede: 插件把 Skills、MCP 服务和 Hooks 打成一个包。桌面端从 Plugins 目录装，CLI 用 /plugins 或 codex plugin；IDE 扩展里暂时用不了。
url: /guides/codex-chajian-rukou-yu-gongzuoliu
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 入门
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-24
date_modified: 2026-11-04
verified_on: 2026-11-04
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex 插件, Codex Plugins, Codex /plugins, codex plugin add, Codex 插件卸载, Codex 插件权限]
related: [plugin-development-marketplace, codex-plugin-hook-audit, mcp-getting-started, permissions-sandbox-approvals]
faq:
  - q: VS Code 里的 Codex 扩展能装插件吗？
    a: 不能。官方 Plugins 文档写明 IDE 扩展不支持插件，要在 ChatGPT 桌面端的 Codex 或 Codex CLI 里浏览和安装。
  - q: 装完插件为什么当前对话里用不了？
    a: 插件里的 Skills 要在安装后新开对话或新的 CLI 会话才会加载。带 MCP 服务的插件可能还要先完成连接或登录。
  - q: 卸载插件后，它连过的服务也断开了吗？
    a: 不一定。官方说明卸载只移除插件包；单独连接的 MCP 服务集成会留在 ChatGPT 里，要去那边手动断开。实测 CLI 卸载后，config.toml 里插件 Hook 的信任记录也还在。
  - q: 用 API Key 登录 Codex 能用插件吗？
    a: 可以浏览、安装和管理受支持的 OpenAI 精选插件，但部分插件的连接流程需要 API Key 登录不支持的 OAuth 能力，这些插件用不了。
---

# Codex 插件入口怎么用：桌面端 Plugins 目录、CLI /plugins 与权限边界

> 本文在线版：[codexguide.io/guides/codex-chajian-rukou-yu-gongzuoliu](https://codexguide.io/guides/codex-chajian-rukou-yu-gongzuoliu)

> 核对依据：OpenAI 官方 [Plugins 文档](https://learn.chatgpt.com/docs/plugins)（2026-11-04 查看）；命令行部分在 Linux 上用 Codex CLI 0.166.0 实测，用的是本地搭的演示 marketplace 和演示插件，没有登录任何真实服务。桌面端界面以官方文档的文字描述为准，本文没有放桌面端截图。

插件（Plugin）是 Codex 和 ChatGPT 共用的扩展包。一个插件可以带 Skills、MCP 服务、浏览器扩展和 Hooks，装一次就能把一整套工作流带进来，不用自己逐个配置。

这篇讲用户这一侧：入口在哪、怎么装、怎么调用、卸载会留下什么。想自己做插件，看 [Codex 插件开发入门](./05-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。

## 先看结论

| 问题 | 答案 |
| --- | --- |
| 在哪装 | ChatGPT 桌面端的 **Plugins** 标签页，或 Codex CLI 里输入 `/plugins` |
| IDE 扩展 | 不支持插件 |
| 装完怎么用 | 新开对话，直接描述任务，或输入 `@` 点名插件 |
| 权限 | 插件能力在 Codex 里运行时，照样受沙箱和审批策略约束 |
| 卸载 | 只移除插件包；单独连接的 MCP 服务要另外断开 |
| Hooks | 插件带的 Hook 要先审查并信任才会运行 |

## 插件里装了什么

按官方文档，一个插件可以包含这几类东西：

| 组成 | 作用 |
| --- | --- |
| Skills | 某类任务的可复用说明，Codex 需要时加载，按里面的步骤、参考资料和辅助脚本做事 |
| MCP 服务 | 把 Codex 接到 GitHub、Slack、Google Drive 等外部系统，提供工具、处理认证、返回结构化数据 |
| 浏览器扩展 | 插件工作流需要的浏览器能力 |
| Hooks | 在 Codex 运行到特定生命周期节点时执行的命令 |

官方举的例子有：用 Codex Security 插件扫描已授权的代码，用 Gmail、Google Drive、Slack 插件处理邮件、文档和频道消息。

ChatGPT 和 Codex 用同一个公共插件目录，所以在两边能看到同一批公开插件。

## 哪些入口能用插件

| 入口 | 能不能用插件 |
| --- | --- |
| ChatGPT 桌面端里的 Codex | 能，从 **Plugins** 标签页浏览和安装 |
| Codex CLI | 能，用 `/plugins` 插件浏览器或 `codex plugin` 命令 |
| Codex IDE 扩展 | 不能。官方让你改用桌面端或 CLI 安装 |
| ChatGPT 网页版和移动端 | Chat 和 Work 里能用；移动端只能用账号里已有的插件 |

标着 **Desktop only** 的插件必须用 ChatGPT 桌面端。网页上能看到，但要打开桌面端才能安装和使用，移动端用不了。

## 桌面端：从 Plugins 目录安装

桌面端打开 **Plugins** 标签页，目录分成几个标签：

- **OpenAI**：OpenAI 做的插件。
- **你的工作区名称**：工作区提供的插件。
- **Personal**：个人 marketplace 里的插件，有内容时会分 **Created by me** 和 **Shared with me** 两组。

已经装过的插件，在单独的 **Installed** 一行里查看。

安装步骤：

1. 搜索或浏览，打开插件详情。
2. 点加号按钮安装。
3. 插件需要连接 MCP 服务时，按提示连接。有的插件安装时就要登录，有的等第一次用时才要。
4. 装好后新开一个对话，让 Codex 使用这个插件。

部分合作方支持 **Sign in with ChatGPT**（官方写的是 beta 逐步开放），包括 Airtable、GitLab、HubSpot、Notion、Supabase 和 Vercel。用它登录只会把你的姓名、邮箱和头像（如有）分享给对方，**不会**因此让插件读取你的数据，也不会自动批准操作。插件要的权限，还要另外审查和批准。

## CLI：/plugins 插件浏览器

在 Codex CLI 里打开插件浏览器：

```text
codex
/plugins
```

插件按 marketplace 分组，用标签切换来源，打开插件看详情，安装或卸载。对已安装的插件按空格键，可以开启或关闭。

装好后要**新开一个会话**，插件里的 Skills 和工具才会加载。

## CLI：codex plugin 命令（0.166.0 实测）

不想进交互界面，也可以直接用子命令。`codex plugin --help` 列出的命令：

```text
Commands:
  add          Install a plugin from a configured or remote marketplace
  list         List plugins available from configured and remote marketplaces
  marketplace  Add, list, upgrade, or remove configured plugin marketplaces
  remove       Uninstall a plugin and remove its local cache
```

下面用一个本地演示 marketplace（`demo-mkt`）和演示插件（`demo-api`，带一个 MCP 服务和一个 SessionStart Hook）走一遍。路径是实验目录，你的会不一样。

添加 marketplace，再安装插件：

```text
$ codex plugin marketplace add ./mkt
Added marketplace `demo-mkt` from /workspace/codex-lab/mkt.
Installed marketplace root: /workspace/codex-lab/mkt

$ codex plugin add demo-api@demo-mkt
Added plugin `demo-api` from marketplace `demo-mkt`.
Installed plugin root: /workspace/codex-lab/home/plugins/cache/demo-mkt/demo-api/0.1.0
```

查看安装结果：

```text
$ codex plugin list
Marketplace `demo-mkt`
/workspace/codex-lab/mkt/.agents/plugins/marketplace.json

PLUGIN             STATUS              VERSION  SOURCE
demo-api@demo-mkt  installed, enabled  0.1.0    /workspace/codex-lab/mkt/plugins/demo-api
```

插件带的 MCP 服务会直接出现在 `codex mcp list` 里，不用自己再写 `[mcp_servers]`：

```text
$ codex mcp list
Name         Url                          Bearer Token Env Var  Status   Auth
demo-remote  https://example.invalid/mcp  -                     enabled  Unknown
```

安装还会在 `config.toml` 里写下两段：

```toml
[marketplaces.demo-mkt]
source_type = "local"
source = "/workspace/codex-lab/mkt"

[plugins."demo-api@demo-mkt"]
enabled = true
```

实测把 `config.toml` 里的 `enabled` 改成 `false`、关掉插件后，`codex plugin list` 显示 `installed, disabled`，它带的 MCP 服务也从 `codex mcp list` 里消失：

```text
PLUGIN             STATUS               VERSION  SOURCE
demo-api@demo-mkt  installed, disabled  0.1.0    /workspace/codex-lab/mkt/plugins/demo-api

$ codex mcp list
No MCP servers configured yet. Try `codex mcp add my-tool -- my-command`.
```

## 调用插件：直接描述，或用 @ 点名

装好后，在输入框里有两种用法：

- **直接描述任务**，比如「总结今天未读的 Gmail 邮件」。Codex 自己挑合适的已装工具。
- **输入 `@`** 点名某个插件或它带的 Skill。想明确指定用哪个时用这种。

## 权限和数据边界

- 插件能力在 Codex 里运行时，Codex 的[沙箱和审批策略](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)照常生效。装了插件不等于放开权限。
- 连接外部服务时，用的是那个服务自己的认证和访问控制。
- 通过 MCP 服务发出去的数据，适用那个服务的条款和隐私政策。
- 用 OpenAI API Key 登录 Codex 时，可以在 CLI 和桌面端浏览、安装、管理受支持的 OpenAI 精选插件；部分插件的连接流程需要不支持的 OAuth 能力，用不了。用量可以在 Platform 的 Usage 页面查看。

**插件 Hook 要先信任。** 官方要求插件 Hook 运行前先审查并信任。实测刚装好时，演示插件的 Hook 状态是 `untrusted`；写入信任记录后变成 `trusted`；Hook 命令被改动后，状态变成 `modified`，要重新审查。另外，在网页上安装插件不会部署 Hook 脚本，脚本必须在执行环境里存在。

## 卸载插件会留下什么

桌面端在插件详情里选 **Uninstall plugin**。工作区安装或默认安装的插件可能没有这个按钮，由管理员管理。

CLI 用 `codex plugin remove`：

```text
$ codex plugin remove demo-api@demo-mkt
Removed plugin `demo-api` from marketplace `demo-mkt`.

$ codex plugin marketplace remove demo-mkt
Removed marketplace `demo-mkt`.
```

卸载后要知道两件事：

1. 官方说明卸载只移除插件包，**单独连接的 MCP 服务集成会留在 ChatGPT 里**，要去那边手动断开。
2. 实测卸载插件、删掉 marketplace 之后，`config.toml` 里那条 Hook 信任记录还在：

```toml
[hooks.state."demo-api@demo-mkt:hooks/hooks.json:session_start:0:0"]
trusted_hash = "sha256:bdabcde5…"
trusted_content_hash = "sha256:949c98ec…"
```

再装回同样内容的插件，Hook 直接是 `trusted`，不会再问你。想彻底清理，要自己删掉这段。完整的自查方法见 [Codex 插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)。

## 教育插件：插件这个形态的一个例子

2026 年 8 月 4 日，OpenAI 发布了三个面向教育的插件，分别给 K–12 教师、大学教师和大学生，可以在 ChatGPT Work 和 Codex 里用。[公告](https://openai.com/index/learn-teach-chatgpt-work-codex/)把插件描述成「apps、角色专属的 skills、instructions 和常用 workflows 打成的包」，让用户不用自己写复杂的提示词就能开工。

这三个插件只通过 ChatGPT Edu 和 ChatGPT for Teachers 的机构部署提供。公告也强调，机构保留对可用工具和权限的控制。

对普通 Codex 用户来说，这里值得参考的是打包思路：按角色把常用的 Skills、工具连接和工作流放进同一个插件，比一个个零散的 Skill 更好分发和管理。具体怎么打包，见 [Codex 插件开发入门](./05-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。

## 下一步

- 想自己做插件并用 marketplace 分发：[Codex 插件开发入门](./05-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)
- 装过第三方插件，想查它装了什么、信任了什么：[Codex 插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)
- 插件里的 MCP 服务怎么配置和登录：[Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)

## 参考资料

- [Plugins（OpenAI 官方文档）](https://learn.chatgpt.com/docs/plugins)
- [Build plugins（开发者文档）](https://developers.openai.com/plugins/build/plugins)
- [Hooks（OpenAI 官方文档）](https://learn.chatgpt.com/docs/hooks)
- [New ways to learn and teach with ChatGPT Work and Codex（OpenAI，2026-08-04）](https://openai.com/index/learn-teach-chatgpt-work-codex/)
