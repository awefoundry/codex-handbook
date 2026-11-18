---
id: codex-context-mode-plugin
title: Codex 安装 context-mode 插件：把大段命令输出挡在上下文之外，附 hooks 信任步骤和 ELv2 许可证说明
seo_title: Codex 安装 context-mode：本地 SQLite 索引、hooks 信任与 ELv2
description: context-mode 是一个免费的本地插件，把大段命令输出和网页内容放进本机 SQLite 索引，只把需要的部分交给 Codex，减少上下文被撑满。本文按官方 README 说明在 Codex 里怎么安装、怎么信任 hooks、怎么检查和卸载，并写清它的 ELv2 许可证和独立收费的 Gateway。
lede: 测试日志和整页抓取会把上下文撑满。这个第三方插件把全文留在本机数据库里，只交回一小段。它不代替 Codex 自己的压缩和 Memories。
url: /guides/codex-context-mode-plugin
status: published
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 22
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-16
date_modified: 2026-11-16
verified_on: 2026-11-16
tested_cli_version: 0.169.0
official_ref: https://learn.chatgpt.com/docs/hooks
keywords: [Codex context-mode, context-mode 插件, ctx-stats, Codex hooks 信任, ELv2, Context Mode Gateway]
related: [codex-context-compaction, hooks-guide, codex-plugin-hook-audit, codex-memories]
howto: true
faq:
  - q: context-mode 是 OpenAI 官方插件吗？
    a: 不是。它是 mksglu/context-mode 维护的第三方项目。插件本身免费，许可证是 Elastic License 2.0，不是 MIT 或 Apache-2.0。GitHub API 对这份许可证显示 SPDX NOASSERTION。
  - q: README 里的 99% 是本文测出来的吗？
    a: 不是。那是 README 作者自己的基准。规则是原始输出不少于 10 KB 的 36 行，每行取 5 次中位数，再用 ctx_bytes 对比 raw_bytes。2026-11-01、插件 2.0.0-next.23、macOS arm64 上，README 称这 36 行的中位数是 99.4% 的字节没有进入上下文。
  - q: 装上插件，hooks 就自动生效了吗？
    a: 不要这样假设。README 把 Codex 的接入写成 hook file，并要求再跑一次 context-mode setup --agents codex 来信任 hooks。2026-11-16 在 Codex CLI 0.169.0 上，plugin add 之后 config.toml 里还没有 hooks.state。没有 TTY 时 setup 退出码是 2；加上帮助里的 --yes 之后，才写入四条插件 hook 的信任记录。装完仍应在 /hooks 里看一眼。
  - q: Context Mode Gateway 要单独付费吗？
    a: README 把 Gateway 写成另一项托管服务，有自己的账号和订阅。免费的是本机插件。本文只讲插件，没有注册 Gateway，也没有核对付款页。
---

# Codex 安装 context-mode 插件：把大段命令输出挡在上下文之外，附 hooks 信任步骤和 ELv2 许可证说明

> 本文在线版：[codexguide.io/guides/codex-context-mode-plugin](https://codexguide.io/guides/codex-context-mode-plugin)

> 核对依据：第三方仓库 [mksglu/context-mode](https://github.com/mksglu/context-mode) 的 README、[LICENSE](https://github.com/mksglu/context-mode/blob/main/LICENSE) 和 [v2.2.0 Release](https://github.com/mksglu/context-mode/releases/tag/v2.2.0)，以及 [contextmode.ai](https://contextmode.ai)。2026-11-16 的 GitHub API：34,146 stars、2,349 forks，`archived` 为 false，`pushed_at` 为 `2026-11-15T22:57:44Z`；许可证对象的 `spdx_id` 是 `NOASSERTION`。最新 Release `v2.2.0` 的 `published_at` 是 `2026-11-14T15:54:28Z`。星数会变，以这次查询为准。安装核对用的是 Linux 上的 `codex-cli 0.169.0` 和一份独立的 `CODEX_HOME`，没有登录，没有配图。

这是 **mksglu** 维护的第三方插件，不是 OpenAI 的内置功能。本文只讲免费的本地插件。Context Mode Gateway 是另一项托管服务，文末单独说明，不要把它的账号和订阅当成安装插件的前提。

适合已经会用 Codex 跑测试、抓网页或调 MCP，并且经常被大段工具输出占满上下文的人。只改几个文件、输出本来就很短时，不必装。

## 它解决什么问题

README 的说法是：编码代理读文件、跑命令、抓页面，每份结果都进上下文窗口。这个插件在本机处理这些输出，把全文放进 SQLite 索引，只把代理要的那一部分交回去。

它帮得上的典型场景，README 的用例表里就有：

- 一整份测试或 lint 输出，例如 Vitest 的 verbose 报告、Biome 的 JSON 报告；
- `curl` 或网页抓取回来的长正文、长 JSON；
- MCP 一次返回的大快照，例如表里的 Chrome DevTools `take_snapshot`。

这些数字都是 README 作者自己的基准，不是本文实测。规则写在 Benchmarks 一节：只统计原始输出不少于 10 KB 的行，每行 5 次运行的中位数，用 `ctx_bytes` 对比 `raw_bytes`；1 KB = 1,024 字节。2026-11-01、插件版本 2.0.0-next.23（commit `16a4bcc5` 加上该基准文件记录的本地修改）、macOS arm64 上，README 称全部 36 行的中位数是 **99.4%** 的输出字节没有进入上下文。分类中位数里，沙箱执行是 99.5%，检索是 77.2%（因为命中的正文要交回去），hook 改道是 99.8%。跟做时以 README 链接的 `bench/results/2026-11-01-darwin-arm64.md` 为准。

不必装的情况：

- 输出本来就短，例如改一个函数、看一条编译错误；
- 你只是想把已经很长的对话收成摘要。那是 Codex 自己的 `/compact` 和自动压缩，见 [上下文窗口与压缩](../02-核心概念与任务方法/07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md)；
- 你想让 Codex 记住以前的对话习惯。那是 [Memories](../11-自动化与高级工作流/12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)，默认关闭，后台生成还可能消耗额度；
- 你不想让第三方 hook 在工具调用前后先看一眼命令。hooks 不是沙箱，见下面的信任一节。

三件事各管一段。压缩管的是对话本身变长。Memories 管的是跨对话的本地回忆。context-mode 管的是单次工具输出太长。README 自己也有一份会话日记和压缩后的 `ctx_resume` 状态块，那是插件的索引，不是 Codex Memories，也不是 `/compact` 生成的摘要。

## 它是怎么做的

README 把一次工具调用写成这条链。下面的阈值都是 README 原文，本文没有在 Codex 会话里复现：

1. 安装时写入 MCP、hooks 和三个 Skill：`ctx-doctor`、`ctx-stats`、`ctx-upgrade`。`context-mode setup` 负责补上原生安装命令没写上的部分。
2. `SessionStart` 打开这个项目的数据库。以前跑过的会话，会提示代理调用 `ctx_resume`。
3. `PreToolUse` 按固定顺序检查：用户拒绝列表、WebFetch、`curl` 和 `wget`、内联 HTTP 和构建命令，然后是超过 `OUTPUT_CAP`（16,384 字节）的整文件读取，以及 `cat`、`tail` 这类单文件输出。带行号范围的读取照常执行。
4. 命中之后，hook 停掉这次调用，并在回复里写明该用哪一个 `ctx_*` 工具。WebFetch 对应的是先 `ctx_index` 再 `ctx_search`。
5. `ctx_execute` 在本机跑代理写的短脚本，只有脚本打印出来的内容回到上下文，并且不超过 `OUTPUT_CAP`。超时是 `EXEC_TIMEOUT_MS`（600,000 毫秒）。README 写明，这里的 sandbox 指的是输出留在外面、不进上下文；脚本仍以你的用户身份跑，能看见你的文件、网络和环境（去掉 `NODE_OPTIONS` 这类预加载变量）。
6. 全文按最多 `MAX_CHUNK_BYTES`（4,096 字节）分块，写入这个项目的 SQLite FTS5。数据库在 `~/.context-mode`，每个项目一个 `context.db`。
7. 有的宿主会先跑完工具。`PostToolUse` 看到输出超过 `REPLACE_TRIGGER_BYTES`（4,096 字节）时，把全文放进索引，只把最匹配的块和一行 `ctx_search` 交回去。
8. hook 出错时仍以退出码 0 结束，并往 `~/.context-mode/hook-errors.log` 写一行，避免把代理卡死。派生 hook 的 `HOOK_TIMEOUT_MS` 是 5,000 毫秒。

Codex 的接入方式，README 的 Codex 块最后一行写的是 **Hooks（hook file）+ MCP + Skills**。同一节说明 hook 有三种到达方式：打进插件包、写成 hook 文件，或做进代理内部的插件。Codex 属于 hook 文件这一类。

## 在 Codex 里安装

README 写插件需要 Node.js 24.15.0 或更新，依据是 `package.json` 的 `engines`。2026-11-16 的 v2.2.0 `package.json` 仍是 `node: >=24.15.0`。Windows 上 README 还要求 Git for Windows，因为 shell 工具走 Git Bash，doctor 会检查它。本文是 Linux，没有做这项检查。

Codex 的安装块是：

```sh
codex plugin marketplace add mksglu/context-mode
codex plugin add context-mode@context-mode
# one-time step: trust the plugin hooks
npm i -g context-mode
context-mode setup --agents codex
```

2026-11-16 在 Codex CLI 0.169.0、独立 `CODEX_HOME`、未登录的前提下，前两步的结果是：

```text
Added marketplace `context-mode` from https://github.com/mksglu/context-mode.git.
Added plugin `context-mode` from marketplace `context-mode`.
```

`codex plugin list` 里这一行是 `context-mode@context-mode`，状态 `installed, enabled`，版本 `2.2.0`。插件缓存里的 `.codex-plugin/plugin.json` 把 `hooks` 指到 `./.codex-plugin/hooks.json`，把 `skills` 指到 `./codex/skills/`，把 `mcpServers` 指到 `./.codex-plugin/mcp.json`。

这时 `config.toml` 里只有 marketplace 和插件的 `enabled = true`，**没有** `hooks.json`，也没有 `[hooks.state]`。只做 `plugin add` 不等于 hooks 已经信任。

### 信任 hooks

README 把 `npm i -g context-mode` 和 `context-mode setup --agents codex` 标成一次性的信任步骤。hooks 的审核规则见 [Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。装完怎么核对信任记录，见 [插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)。

本机先用 Node.js v22.23.4 安装了 npm 包 `context-mode@2.2.0`。npm 打出 `EBADENGINE`，要求 `>=24.15.0`。`context-mode --version` 仍打印 `2.2.0`，但 `context-mode setup --agents codex` 直接拒绝：

```text
context-mode: Context Mode needs Node 24.15.0 or newer; you have v22.23.4. Fix: nvm install 24, or install it from https://nodejs.org.
```

这条的退出码是 0，可是没有写任何文件。跟做时先把 Node 升到 README 要求的版本，不要把退出码 0 当成已经信任。

换成 Node.js v24.22.3 之后，同一条 README 命令在没有 TTY 的环境里退出码是 **2**，并打印它准备写入的四条信任记录。`context-mode setup --help` 写明：`--yes` 是不再询问、直接应用；没有 TTY 又需要回答时，退出码 2。帮助里的例子是 `context-mode setup --yes --agents codex,claude-code`。README 的 Codex 安装块没有写 `--yes`。有终端时它会先给你看计划再问；本文因为没有 TTY，才加上 `--yes`。

`--yes` 的结果是 `codex: PASS`。它列出的检查是 `parse, list, mcp, hook, hook-registered, hook-runs, hook-seen, skills`，并有一条警告：

```text
WARN hook-seen: not seen yet, run one tool call
```

也就是说，安装器自己做了一次 hook 调用检查，但还没有在真实工具调用里看到它。本文没有登录，没有做这通工具调用。

这次写入的不是一份新的用户级 `hooks.json`。`CODEX_HOME/hooks.json` 仍然不存在。信任记录在 `config.toml` 的 `[hooks.state]`，键指向插件自带的 hook 文件，四条事件是：

- `pre_tool_use`
- `post_tool_use`
- `session_start`
- `user_prompt_submit`

每条都有 `trusted_hash` 和 `trusted_content_hash`。本文不贴哈希。插件缓存里的 `.codex-plugin/hooks.json` 与这四条对应：`PreToolUse` 和 `PostToolUse` 的 matcher 是 `^(Bash|apply_patch|mcp__context_mode__ctx_.*)$`，另外还有 `SessionStart` 和 `UserPromptSubmit`。命令是 `node "${PLUGIN_ROOT}/hook.mjs" --agent codex`，`"timeout": 5`。README 的 `HOOK_TIMEOUT_MS` 是 5,000 毫秒。本文没有在一次真实回合里计时。

能写 `config.toml` 的程序也可以自己写入匹配的信任哈希。setup 在你确认之后就是这么做的。PASS 只说明安装器认为检查过了。新开一次 Codex，在 `/hooks` 里再看这四条是不是你预期的插件 hook。

## 装好后怎么确认

README 的检查命令是：

```sh
codex mcp list
```

2026-11-16 信任步骤前后各跑了一次，输出的列是一致的：

| 列 | 值 |
| --- | --- |
| Name | `context-mode` |
| Command | `node` |
| Args | `./server.mjs --agent codex` |
| Status | `enabled` |
| Auth | `Unsupported` |

`mcp.json` 里的 `cwd` 是 `"."`，`codex mcp list` 把它解析成插件缓存目录。`default_tools_approval_mode` 在这份文件里是 `approve`。本文没有登录会话，没有看到审批弹窗，所以不把「每次都会问你」写成已经发生的事。`codex mcp login` 用于需要登录的 HTTP MCP；这次列表里的 Auth 就是 `Unsupported`，本文没有对它做 `mcp login`。

还可以看 `codex plugin list` 是否仍是 `installed, enabled`，以及 `config.toml` 里是否出现上面的四条 `[hooks.state]`。setup 的 `hook-seen` 警告还在，说明还差一次真实工具调用。那一步本文没做。

## 日常怎么用

README 给 Codex 的统计技能是 `$ctx-stats`。插件缓存里的 `codex/skills/ctx-stats/SKILL.md` 名叫 `ctx-stats`，`disable-model-invocation` 为 true，正文要求调用 `mcp__context_mode__ctx_stats`，并把回复原样放进代码块。同一目录还有 `ctx-doctor` 和 `ctx-upgrade`。README 后文用 `/ctx-doctor`、`/ctx-upgrade` 描述「在代理里的命令」，那张按代理分开的表里，Codex 一行只写了 `$ctx-stats`。本文没有在会话里调用任何一个，所以不把斜杠形式写成 Codex 已经验证的入口。

README 建议装完后把下面这类提示贴进代理。这些示例是在 Claude Code 2.1.312 里跑的，模型写的是 `claude-haiku-5-5`，插件版本 2.0.0-next.26，日期 2026-11-02。README 称其他代理用同一套 `ctx_execute`、`ctx_index`、`ctx_search`。本文没有在 Codex 里重跑：

- 打开一篇长文档，只要其中的例子和规则。README 称 React `useEffect` 那一页原始 601,984 字节，进入上下文 20,860 字节，省下 96.5%。
- 抓一份 5,000 条 JSON，在沙箱里算最长标题。README 称原始 1,039,898 字节，进入上下文 393 字节，省下 99.96%，并注明这是四个例子里的最好情况。
- 统计一份 syslog 里的认证失败。README 称省下 99.7%。
- 看 Hacker News 首页前十条。README 称省下 95.7%，并注明首页会变，原始大小每次不同。

代理侧的工具名，README 的工具表是：`ctx_execute`、`ctx_batch`、`ctx_index`、`ctx_search`、`ctx_resume`、`ctx_stats`、`ctx_doctor`、`ctx_upgrade`、`ctx_purge`。要看某次省了多少，用 `$ctx-stats`，不要把 README 里那张「1015.5 KB 变成 3.7 KB」的样例当成你这次的结果。那份样例的说明是 2026-11-03、2.0.0-next.35、在临时 HOME 里通过 MCP 调用 `release-out/server.mjs`。

## 数据和隐私

README 的 Security and privacy 写了这些边界。本文没有抓包核对：

- 插件数据在本机，每个项目一个库，位于 `~/.context-mode`。`ctx_purge` 可以按会话、来源或项目删除。
- README 称零遥测：用量、事件和崩溃报告留在本机。它列出四类会用到网络的调用，每一类都要你或代理先发起：`ctx_index` 去抓你点名的 URL（并挡住私有地址和链路本地地址）、`context-mode doctor` 读 npm dist-tags（失败时改用 `git ls-remote` 看发布标签）、`context-mode upgrade` 或你确认发送调试报告时调用 npm 或 `gh`、以及你自己执行的安装和更新命令。
- 脚本以你的用户身份执行。README 写明要保留 Codex 自己的权限提示。想限制命令能碰到什么，仍用 Codex 的沙箱和审批，不要把这个插件当成权限系统。

官网首页把插件写成 Elastic License 2.0 下可免费使用、源码可见。同一页的注册入口、价格和「1,000 requests free」讲的是 Gateway，不是这个本地插件。

## 许可证与收费

仓库 `LICENSE` 和 README 的 License 一节写的是 **Elastic License 2.0（ELv2）**，source-available。README 称可以免费使用、复制、修改、分享，也可以在工作中免费使用。它给许可方保留三类用途：把软件做成向他人提供大部分功能的托管或托管式服务；改掉、关掉或绕过许可证密钥功能，或去掉密钥所保护的内容；改掉或藏起许可方的许可证、版权和其他声明。README 写明选 ELv2 是为了源码保持公开，同时把托管服务留在项目这边。

这不是 MIT，也不是 Apache-2.0。GitHub 仓库 API 不把这份许可证识别成一个 SPDX 标识，返回的是 `NOASSERTION`。以仓库里的 `LICENSE` 文件为准。

| 产品 | 跑在哪 | README 怎么写收费 |
| --- | --- | --- |
| Context Mode 插件 | 你的机器，一个项目一份 `context.db` | 免费 |
| Context Mode Gateway | 托管服务，跨会话和代理 | 单独订阅，和插件分开 |

README 称 Gateway 用 `npx @context-mode/cli` 登录，会改每个代理的一份配置，请求会经过它的服务器。它的功能名单是 Context Saving、Recall、Memory、Skills、Search、Session resume、Active Context、Instructions、Protect、Prompt caching、Live 和 Analytics。官网首页写 Gateway 有 1,000 次免费请求、不需要信用卡，并写「Your own model account still pays the model」。本文没有注册，没有打开付款页，不转述套餐金额。本地插件不需要这项订阅。

## 升级与卸载

README 的 Codex 更新和卸载：

```sh
codex plugin marketplace upgrade context-mode
codex plugin remove context-mode@context-mode
```

v2.2.0 的 Release 说明里，Codex 一行的更新命令同样是 `codex plugin marketplace upgrade context-mode`，并注明 hook 信任那一步走 npm。本文没有执行 upgrade 或 remove。

如果还全局装过 `context-mode` 这个 npm 包，README 的通用卸载是：

```sh
context-mode setup --remove
npm rm -g context-mode
```

`setup --help` 写 `--remove` 会把每次 setup 动过的文件按字节放回去。本文没有跑 `--remove`。插件自查一文在 Codex CLI 0.166.0 上看到 `codex plugin remove` 不会删掉 `[hooks.state]`。那次不是这个插件，也不是 0.169.0。卸完之后打开 `config.toml`，看 `hooks.state` 还在不在；还在就对照 [插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md) 处理。不要假设卸插件等于卸信任记录。

## 常见问题与参考资料

**Node 版本够，setup 却退出 2。** 帮助写明，没有 TTY 又需要回答时退出码是 2。先 `context-mode setup --agents codex --dry-run` 看计划，确认之后再用帮助里的 `--yes`。不要在没看计划的情况下，把 `--yes` 理解成 README 安装块的原文。

**`codex mcp list` 有这一行，但大输出仍整段进了对话。** 先看 `[hooks.state]` 在不在，再在 `/hooks` 里看这四条是否为已信任。setup 的 `hook-seen` 警告表示还没有一次真实工具调用。输出本来就低于 README 的阈值时，插件也不会改道。

**和压缩、Memories 一起开会不会互相覆盖。** 不会合成一个开关。压缩和 Memories 仍按 Codex 自己的配置工作。插件多出来的是本地索引和 hook。三套可以同时存在，也可以只留压缩。

**Gateway 的省钱数字能当成插件的效果吗。** 不能。README 把 Gateway 的美元对比单独放在 Gateway 一节，并写明插件的数字在 Benchmarks。那些美元数字是作者账号上的 Gateway 对照，不是本文的测量。

下一步：上下文已经很长时，先看 [压缩](../02-核心概念与任务方法/07-Codex上下文窗口与压缩-compact自动压缩与何时新开会话.md) 要不要新开会话。准备信任这份 hook 之前，把 [Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md) 里的信任和超时读一遍。

- [mksglu/context-mode](https://github.com/mksglu/context-mode)
- [v2.2.0 Release](https://github.com/mksglu/context-mode/releases/tag/v2.2.0)
- [LICENSE（Elastic License 2.0）](https://github.com/mksglu/context-mode/blob/main/LICENSE)
- [contextmode.ai](https://contextmode.ai)
- [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
