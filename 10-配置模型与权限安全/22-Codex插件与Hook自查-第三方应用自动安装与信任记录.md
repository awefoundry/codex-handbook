---
id: codex-plugin-hook-audit
title: Codex 插件和 Hook 自查：第三方应用自动安装后，怎么查 config.toml、信任记录和 MCP
seo_title: Codex 插件和 Hook 自查：config.toml、信任记录与 MCP
description: Postman 桌面端被报告自动给 Codex 装插件，并替自己的启动 Hook 写了信任记录。本文用 Codex CLI 0.166.0 实测，讲怎么查已装插件、marketplace、Hook 信任记录和插件带的 MCP，以及卸载后哪些东西会留下。
lede: 别的程序也能改 ~/.codex/config.toml。五条命令查一遍，卸载以后再看一眼 hooks.state。
url: /guides/codex-plugin-hook-audit
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 社区热点
entry_tags: [CLI, App]
difficulty: 进阶
order: 22
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-04
date_modified: 2026-11-04
verified_on: 2026-11-04
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/hooks
keywords: [Codex 插件自查, Codex Hook 信任, hooks.state, trusted_hash, Postman Codex 插件, codex plugin remove, Codex MCP 检查]
related: [hooks-guide, plugin-development-marketplace, config-toml-guide, mcp-getting-started]
faq:
  - q: Postman 这件事证明它偷了数据吗？
    a: 没有。报告者在 issue 里写明，日志只能证明插件是在没有确认的情况下装上的，并改了 Codex 的启动指令，不能证明数据被发走。The New Stack 发稿时 Postman 也还没有回应。
  - q: 别的程序能直接把 Hook 标成已信任吗？
    a: 能。信任状态存在 config.toml 的 [hooks.state] 里。我们在 0.166.0 上手动写入和当前哈希一致的 trusted_hash 和 trusted_content_hash，hooks/list 立刻显示 trusted。能写你家目录的程序都能这么做。
  - q: codex plugin remove 会把信任记录一起删掉吗？
    a: 不会。实测 plugin remove 和 plugin marketplace remove 之后，[plugins] 和 [marketplaces] 两段都没了，[hooks.state] 那段还在。内容不变时再装回来，Hook 直接是 trusted，不用重新审。
  - q: 只想先停掉，不想卸载怎么办？
    a: 把 config.toml 里该插件的 enabled 改成 false。实测之后 plugin list 显示 installed, disabled，它带的 Hook 和 MCP 都不再加载。要一次停掉所有 Hook，用 [features] hooks = false。
---

# Codex 插件和 Hook 自查：第三方应用自动安装后，怎么查 config.toml、信任记录和 MCP

> 本文在线版：[codexguide.io/guides/codex-plugin-hook-audit](https://codexguide.io/guides/codex-plugin-hook-audit)

> 核对依据：OpenAI 文档 [Hooks](https://learn.chatgpt.com/docs/hooks) 和 [Plugins](https://learn.chatgpt.com/docs/plugins)（2026-11-04 抓取）；事件经过来自 [postmanlabs/postman-app-support#14370](https://github.com/postmanlabs/postman-app-support/issues/14370) 和 [The New Stack](https://thenewstack.io/postman-plugin-coding-agents/) 的报道。下面的命令输出都来自 Linux 上的 Codex CLI 0.166.0：用独立的 `CODEX_HOME`，加一个自建的本地 marketplace 和一个带 SessionStart Hook 和 MCP 的测试插件，没有动真实的用户配置。我们没有安装 Postman，也没有复现它的安装过程。

## 先看结论：五条命令查一遍

| 查什么 | 命令 | 看什么 |
| --- | --- | --- |
| 装了哪些插件 | `codex plugin list` | STATUS 列里的 `installed, enabled` |
| 加了哪些插件来源 | `codex plugin marketplace list` | 你不认识的 MARKETPLACE 名字 |
| 有哪些 Hook、信不信任 | CLI 里输入 `/hooks`；桌面端 composer 里的 **Review hooks** 或 **Settings > Hooks** | 来源是 plugin 的条目 |
| 信任记录写在哪 | `grep -n "hooks.state" ~/.codex/config.toml` | 你没审过却已经存在的记录 |
| 插件带了哪些 MCP | `codex mcp list` | 不是你自己加的服务器 |

用了 `CODEX_HOME` 的话，把 `~/.codex` 换成那个目录。

有一点要注意：`codex doctor` 统计 MCP 时不算插件带来的服务器。实测里 `codex mcp list` 列出了插件的 MCP，`codex doctor` 却报告 0 个 MCP 服务器。查 MCP 要用 `codex mcp list`。

## 事情经过：报告里写了什么、没证明什么

2026-10-26 03:03（北京时间），有人在 Postman 的反馈仓库开了 [#14370](https://github.com/postmanlabs/postman-app-support/issues/14370)。截至 11-04，这个 issue 仍是 open，有 33 条评论、224 个反应，Postman 官方没有在里面回复。11-04 它上了 [Hacker News](https://news.ycombinator.com/item?id=50354960)，有 1,005 分、336 条评论。

报告者用的是 macOS 上的 Postman 桌面端 12.33.4。他贴出的证据有这些：

- Postman 的 `main.log` 里有一条 `auto-existing-upgrade`，同时记录了 `claude-code:installed` 和 `codex:installed`。他说自己没有点过任何安装。
- `~/.codex/config.toml` 里多了三段：

```toml
[marketplaces.postman]
source_type = "git"
source = "https://github.com/postmanlabs/postman-plugin.git"

[plugins."postman@postman"]
enabled = true

[hooks.state."postman@postman:hooks/codex-hooks.json:session_start:0:0"]
trusted_hash = "sha256:..."
trusted_content_hash = "sha256:..."
```

这里的哈希值我们换成了省略号，其余是 issue 里贴出的原文。

- 插件带了一个 SessionStart Hook，匹配 `startup|clear|compact`。它在每次启动时输出一段指令，要求 Codex 在做任何不简单的 API 任务之前，先加载 `postman:api-engineer` 这个 Skill。
- 插件还带了一个远程 MCP：`https://mcp.postman.com/mcp`。报告者那边它连不上，报 `Auth required`。
- 他从安装器源码里找到一个 `approvePostmanHook` 函数，用 app-server 的 `hooks/list` 和 `config/batchWrite` 把这个 Hook 写成已信任。

报告者自己说明，这些证据能证明的是：插件在没有确认的情况下装上了，并且改了 Codex 每次启动时收到的指令。**它们不能证明有数据被发走。** HN 标题里说的「share all API data」没有证据支持。报告者还说，在一台干净的 Mac 上没能复现。[The New Stack 的报道](https://thenewstack.io/postman-plugin-coding-agents/)（11-03）写到，发稿时 Postman 没有回应。

所以本文不评判 Postman，只讲一件事：**任何能写你家目录的程序，都能做同样的改动。** 你要知道去哪里查。

## Hook 信任是怎么存的

官方 [Hooks](https://learn.chatgpt.com/docs/hooks) 文档规定，非托管的 Hook 要先审核、信任才会运行。Codex 按 Hook 当前的哈希记录信任；新加的或改过的 Hook 会被标成待审，在你信任之前直接跳过。插件带来的 Hook 走同一套流程。插件更新时如果改了它打包的脚本，即使 Hook 定义没变，也要重新审核。

信任记录写在 `config.toml` 的 `[hooks.state."<键>"]` 里，有两个字段：`trusted_hash` 和 `trusted_content_hash`。对插件 Hook 来说，键的格式是：

```text
<插件名>@<marketplace名>:<hooks 文件路径>:<事件>:<分组序号>:<Hook序号>
```

Postman 的键是 `postman@postman:hooks/codex-hooks.json:session_start:0:0`。我们的测试插件 `demo-api` 装好以后，`hooks/list` 返回的键是同一种格式：

```json
{"key": "demo-api@demo-mkt:hooks/hooks.json:session_start:0:0", "eventName": "sessionStart", "source": "plugin", "pluginId": "demo-api@demo-mkt", "trustStatus": "untrusted", "currentHash": "sha256:bdabcde55e358093ef5908f575faa9b08191069cbff63c28372a2096a6e2a31a/sha256:949c98ecb510db6fe628ad8591b6095b095a423215b0349f81d97d92aba18429"}
```

刚装上时是 `untrusted`。`currentHash` 是用 `/` 连起来的两个值，分别对应 `trusted_hash` 和 `trusted_content_hash`。

我们没有打开 `/hooks`，而是直接在 `config.toml` 末尾追加了这两个值：

```toml
[hooks.state."demo-api@demo-mkt:hooks/hooks.json:session_start:0:0"]
trusted_hash = "sha256:bdabcde55e358093ef5908f575faa9b08191069cbff63c28372a2096a6e2a31a"
trusted_content_hash = "sha256:949c98ecb510db6fe628ad8591b6095b095a423215b0349f81d97d92aba18429"
```

再查 `hooks/list`，`trustStatus` 变成了 `"trusted"`。也就是说，信任审核挡得住「Hook 自己偷偷变了」，挡不住「别的程序替你写了一条信任记录」。后面这种情况，只能靠你自己去查文件。

## 查插件和 marketplace

`codex plugin list` 会按 marketplace 分组列出插件。实测输出：

```text
$ codex plugin list
Marketplace `demo-mkt`
/workspace/codex-lab/mkt/.agents/plugins/marketplace.json

PLUGIN             STATUS              VERSION  SOURCE
demo-api@demo-mkt  installed, enabled  0.1.0    /workspace/codex-lab/mkt/plugins/demo-api
```

```text
$ codex plugin marketplace list
MARKETPLACE  ROOT
demo-mkt     /workspace/codex-lab/mkt
```

`/workspace/codex-lab` 是实验目录，你那边会是自己的路径。加上 `--json` 能拿到机器可读的结果，适合写进定期检查的脚本。

对应到 `config.toml`，就是两段：

```toml
[marketplaces.demo-mkt]
source_type = "local"
source = "/workspace/codex-lab/mkt"

[plugins."demo-api@demo-mkt"]
enabled = true
```

看到不认识的 `[marketplaces.*]` 或 `[plugins."*@*"]`，先查清楚是谁写的，再决定留不留。插件的文件缓存在 `~/.codex/plugins/cache/<marketplace>/<插件>/<版本>/` 下，可以直接打开它的 `hooks/` 目录和 `.mcp.json` 看内容。

## 查 Hook：/hooks、Review hooks 和 hooks.state

- **CLI**：输入 `/hooks`，能看到每个 Hook 的来源，审核新加或改过的 Hook，或者停用单个非托管 Hook。启动时如果有 Hook 待审，Codex 会打一行警告，提示你去 `/hooks`。
- **ChatGPT 桌面端**：在 composer 里点 **Review hooks**，或者打开 **Settings > Hooks**。
- **直接看文件**：

```bash
grep -n -A2 "hooks.state" ~/.codex/config.toml
```

每条记录的键里都带着插件名和 marketplace 名。对照 `codex plugin list` 的结果：**插件已经不在了，信任记录却还在**，就是下一节要讲的残留。

托管 Hook 来自系统、MDM、云端或 `requirements.toml`，它们由策略信任，在用户的 Hook 浏览器里关不掉。命令行参数 `--dangerously-bypass-hook-trust` 可以让当次运行跳过信任检查。自查时要是在别人的启动脚本或别名里看到这个参数，要当回事。

## 查 MCP：codex mcp list

插件通过 `.mcp.json` 带的 MCP 服务器，会出现在 `codex mcp list` 里：

```text
$ codex mcp list
Name         Url                          Bearer Token Env Var  Status   Auth   
demo-remote  https://example.invalid/mcp  -                     enabled  Unknown
```

`demo-remote` 是测试插件里写的假地址。Postman 那个对应的就是 `https://mcp.postman.com/mcp`。

另外，在 ChatGPT 里单独连接过的 MCP 集成不归本地 CLI 管。官方 Plugins 文档写明：卸载插件只删插件包，**另外连接的 MCP 集成会一直保持连接，直到你在 ChatGPT 里断开它**。

## 实测：卸载以后，信任记录还在

接上面的环境（Hook 已经是 trusted），先卸载插件，再删 marketplace：

```text
$ codex plugin remove demo-api@demo-mkt
Removed plugin `demo-api` from marketplace `demo-mkt`.
$ codex plugin marketplace remove demo-mkt
Removed marketplace `demo-mkt`.
```

这时 `config.toml` 里只剩下：

```toml
[hooks.state."demo-api@demo-mkt:hooks/hooks.json:session_start:0:0"]
trusted_hash = "sha256:bdabcde55e358093ef5908f575faa9b08191069cbff63c28372a2096a6e2a31a"
trusted_content_hash = "sha256:949c98ecb510db6fe628ad8591b6095b095a423215b0349f81d97d92aba18429"
```

`[plugins]` 和 `[marketplaces]` 都删干净了，插件缓存目录 `plugins/cache/demo-mkt/` 也空了，**信任记录却留着**。

然后我们重新执行 `plugin marketplace add` 和 `plugin add`，内容和之前完全一样。`hooks/list` 直接返回 `"trustStatus": "trusted"`，没有要求重新审核。

最后我们改了缓存里 `hooks.json` 的命令，再查一次：

```json
{"key": "demo-api@demo-mkt:hooks/hooks.json:session_start:0:0", "eventName": "sessionStart", "source": "plugin", "pluginId": "demo-api@demo-mkt", "trustStatus": "modified", "currentHash": "sha256:742876a180bae39e29e12ce5eb6b0ff304b44d1f754cc21ecc9c7056c4cd7883/sha256:23faff56be8d7d68ba52cf7bd6b555c2f37d54bfa5f9650cdad8cc9a8c02b056"}
```

状态变成了 `modified`，要重新审核才会运行，和文档一致。

结论：如果一个程序替你写过信任记录，你卸载它的插件之后，这条记录还在。下次它把同样的内容装回来，Hook 会直接运行。

## 清理步骤

1. 先停用，不急着删。把 `config.toml` 里那个插件的 `enabled = true` 改成 `false`。实测之后 `codex plugin list` 显示 `installed, disabled`，`codex mcp list` 里那个插件的 MCP 消失，`hooks/list` 也不再返回它的 Hook。
2. 确认不要了，执行 `codex plugin remove <插件>@<marketplace>`。来源也不要了，再执行 `codex plugin marketplace remove <marketplace>`。也可以在 CLI 的 `/plugins` 浏览器里卸载。
3. 手动删除 `config.toml` 里对应的 `[hooks.state."<插件>@<marketplace>:..."]` 段落。这一步 CLI 不会替你做。
4. 在 ChatGPT 里断开这个插件连过的外部服务。
5. 第三方应用一般还会在别处装东西。Postman 的报告里，同一时段 Claude Code 也被装上了 Postman 插件，`~/.local/bin` 里多了一个 Postman 命令行工具。用了 Claude Code 的话，同样要去它的配置里查。
6. 新开一个 Codex 会话。已经开着的会话不会重新加载配置。

## 预防：关 Hook、只允许托管 Hook、盯住 ~/.codex

- **不用 Hook 就关掉**。Hook 默认是开的。

```toml
[features]
hooks = false
```

`codex_hooks` 是旧写法，现在还能用。

- **企业管理员**可以在 `requirements.toml` 里用 `[features].hooks = false` 强制关闭，或者设 `allow_managed_hooks_only = true`。后者会跳过用户、项目、会话和插件来源的 Hook，只加载托管 Hook。
- **把 `~/.codex/config.toml` 纳入备份或版本管理**。用 git 管起来的话，任何程序改了它，`git diff` 一眼就能看出来。
- **定期跑一遍开头那五条命令**。装了新的桌面应用、命令行工具或 IDE 插件之后，尤其要跑一次。
- **SessionStart Hook 输出的内容会进模型上下文**。审核插件 Hook 的时候，要看它到底打印了什么，不能只看是不是来自熟悉的厂商。

## 常见问题

**`/hooks` 里没有待审条目，是不是就没事？** 不一定。已经被写成 trusted 的 Hook 不会提示你审核。还要看 `config.toml` 里 `[hooks.state]` 的键，是不是都对得上你认识的插件。

**`codex doctor` 说没有 MCP 服务器，可以放心吗？** 不能只看它。实测 doctor 不统计插件带来的 MCP，要用 `codex mcp list` 查。

**我用的是桌面端，不用 CLI，也要查吗？** 要。官方 [Best practices](https://learn.chatgpt.com/guides/best-practices) 写明，CLI、IDE 扩展和 ChatGPT 桌面端共用同一套配置层，按这个说法，`~/.codex/config.toml` 里的插件和 Hook 设置也会影响桌面端里的 Codex。桌面端的入口是 composer 里的 **Review hooks**、**Settings > Hooks**，以及 Plugins 页的 Installed 一栏。本文的实测只在 CLI 上做过。

**插件 Hook 能在 ChatGPT Work 云端运行吗？** 官方 Plugins 文档说明，云端编排的 ChatGPT Work 不支持插件 Hook。本文讨论的都是本地运行的 Codex。

## 下一步

Hook 的写法和 `/hooks` 界面，见 [Codex Hooks 入门](../11-自动化与高级工作流/08-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。插件里到底能打包什么、marketplace 怎么配，见 [Codex 插件开发入门](../08-插件工作流/05-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。正常的安装、停用和卸载，见 [Codex 插件入口](../08-插件工作流/04-Codex插件入口与工作流.md)。`config.toml` 的分层和生效检查，见 [config.toml 深入配置](./08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。MCP 的配置和登录，见 [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 参考资料

- [Hooks](https://learn.chatgpt.com/docs/hooks)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [postmanlabs/postman-app-support#14370](https://github.com/postmanlabs/postman-app-support/issues/14370)
- [The New Stack：Postman plugin and coding agents](https://thenewstack.io/postman-plugin-coding-agents/)
- [Hacker News 讨论](https://news.ycombinator.com/item?id=50354960)
