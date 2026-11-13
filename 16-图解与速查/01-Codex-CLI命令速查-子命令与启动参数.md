---
id: codex-cli-commands-cheatsheet
title: Codex CLI 命令速查（0.166.0 更新）：codex 子命令与启动参数一览
seo_title: Codex CLI 命令速查：子命令与启动参数一览
description: 按用途整理 Codex CLI 0.166.0 的子命令和常用启动参数：启动和恢复会话、非交互执行、排队任务、登录（含访问令牌）、MCP 与插件、权限与沙箱、诊断和会话管理。每条都对照 codex --help 和官方命令文档核对过。
lede: 先看 0.166.0 多出来的 queue --resume 和 doctor --network-only，再按要做的事查子命令。Linux 上的 codex --help 列出 26 个。
url: /guides/codex-cli-commands-cheatsheet
status: published
section: guides
category: K-troubleshooting
topic: 认识、安装与环境
content_type: 参考
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 入门
order: 1
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-26
date_modified: 2026-11-08
verified_on: 2026-11-05
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/developer-commands
keywords: [Codex CLI 命令, codex 子命令, Codex CLI 0.166.0, codex queue --resume, codex doctor --network-only, codex login --with-access-token]
related: [codex-doctor, cli-manage-multiple-sessions, codex-access-tokens-service-accounts, codex-web-search-settings]
faq:
  - q: codex 和 codex exec 有什么区别？
    a: 直接运行 codex 会打开交互式终端界面；codex exec（简写 codex e）跑完就退出，适合脚本和 CI。0.166.0 里 --search 写在 codex、resume、fork 的帮助里，codex exec --search 会报 unexpected argument。
  - q: 怎么继续上一次的 Codex 会话？
    a: 用 codex resume --last。它默认只在当前目录的会话里找最近一次，想跨目录找就加 --all。非交互任务用 codex exec resume --last。
  - q: 为什么 codex exec 提示 Not inside a trusted directory？
    a: codex exec 默认要求在 Git 仓库或已信任的目录里运行。确实要在别的目录运行时，加 --skip-git-repo-check。0.166.0 在未信任目录里的原文仍是这句。
  - q: codex mcp-server 命令去哪了？
    a: 官方命令文档写明，codex mcp-server 和单独的 codex-mcp-server 程序已经移除，改用 codex app-server。
---

# Codex CLI 命令速查（0.166.0 更新）：codex 子命令与启动参数一览

> 本文在线版：[codexguide.io/guides/codex-cli-commands-cheatsheet](https://codexguide.io/guides/codex-cli-commands-cheatsheet)

> 核对依据：OpenAI 官方文档 [Command line options](https://learn.chatgpt.com/docs/developer-commands)（2026-11-05 抓取），[更新日志](https://learn.chatgpt.com/docs/changelog) 里的 CLI 0.166.0，以及 Linux 上 npm 安装的 `codex-cli 0.166.0`。同一天 `npm view @openai/codex version` 的 latest 仍是 0.166.0。`codex --help` 和各子命令的 `--help` 都跑过。登录、沙箱、doctor 和非法配置用的是独立 `CODEX_HOME`，没有登录账号。不同版本、不同系统的命令会有差异，以你本机 `codex --help` 为准。

这篇是给已经装好 Codex CLI 的人查命令用的。按要做的事分组，每组只列常用写法。第一次安装和登录请先看 [Codex 安装登录常见问题](../01-安装与首次使用/13-安装登录常见问题.md)。终端里以 `/` 开头的斜杠命令见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。

## 0.166.0 有哪些变化

更新日志里和命令直接相关的新增与修复：

| 变化 | 来源 | 本文怎么用 |
|---|---|---|
| `codex queue --resume`：排队之后尝试把未加载的线程拉起来 | 更新日志 #57232；命令文档和 `--help` 一致 | 见「排队任务」 |
| `codex doctor --network-only`：只跑配置、网络环境和 WebSocket 检查 | 更新日志 #57606；`--help` 写的是 config、network environment、provider HTTP、Responses WebSocket | 见「诊断」 |
| 恢复或分叉时保留已经确认的审批和权限设置 | 更新日志 #57227 | 不是新旗标。长任务里怎么用，见 [长任务工作流](../11-自动化与高级工作流/05-Codex长任务工作流.md) |
| 推理 token 计数跨恢复和分叉保留，避免过早压缩 | 更新日志 #57839 | 同上，本文没有做恢复实验 |
| 安全拦截时，TUI 给出解释，以及可选的更安全后续提示 | 更新日志 #57363、#57365 | 发生在终端界面里，没有对应的新子命令 |
| 内置、Vertex AI 和 Amazon Bedrock 的模型目录加入 GPT-6.1 Terra | 更新日志 #57293 | 模型怎么选见 [GPT-6.1 Terra](../10-配置模型与权限安全/14-Codex使用GPT-6.1-Terra-适用任务-切换方法与额度.md) |

0.164.0 的速查没有写 `codex login --with-access-token`。0.166.0 的 `codex login --help` 有这个旗标。用法见 [访问令牌与服务账号](../11-自动化与高级工作流/14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)。

## 先看全貌：0.166.0 的 26 个子命令

在这台 Linux 上运行 `codex --help`，列出 26 个子命令（另有 `help`）。按用途分组：

| 用途 | 子命令 |
|---|---|
| 开始和继续会话 | （不带子命令）`codex`、`resume`、`fork`、`queue`、`agents` |
| 非交互执行和审查 | `exec`（简写 `e`）、`review`、`apply`（简写 `a`）、`cloud` |
| 登录 | `login`、`logout` |
| 扩展 | `mcp`、`plugin`、`features` |
| 权限与沙箱 | `sandbox` |
| 诊断和维护 | `doctor`、`update`、`completion`、`debug` |
| 会话管理 | `archive`、`unarchive`、`delete`、`migrate-rollouts`、`migrate-nfs-db` |
| 后台服务 | `app-server`、`remote-control`、`exec-server` |

`app-server`、`remote-control`、`migrate-nfs-db` 标着 `[experimental]`，`cloud`、`exec-server` 标着 `[EXPERIMENTAL]`。

官方文档里还有两个命令不在这台 Linux 的 `codex --help` 列表里：

- `codex app`：在 macOS 或 Windows 上从终端打开 ChatGPT 桌面端，没装时会启动安装程序。这台 Linux 上 `codex help app` 的原文是 `unrecognized subcommand 'app'`，退出码 2。
- `codex execpolicy check`：检查 `.rules` 规则文件，文档写明目前是 preview。`codex execpolicy --help` 可以运行，但它不在 `codex --help` 的列表里。

`codex mcp-server` 和单独的 `codex-mcp-server` 程序已经移除，官方文档建议改用 `codex app-server`。

## 开始和继续会话

| 命令 | 作用 |
|---|---|
| `codex` | 打开交互式终端界面 |
| `codex "修复登录页的报错"` | 打开终端界面并直接带上第一条提示词 |
| `codex -i screenshot.png "按这张图改样式"` | 附带图片（可以写多个） |
| `codex resume` | 打开会话列表，选一个继续 |
| `codex resume --last` | 直接继续最近一次会话。默认只看当前目录 |
| `codex resume --all` | 列出所有目录的会话 |
| `codex resume <SESSION_ID>` | 按会话 ID 或会话名继续。帮助写明能解析成 UUID 时，UUID 优先 |
| `codex fork --last` | 把当前目录最近一次会话复制成新会话。原会话不变 |
| `codex fork <SESSION_ID> --worktree` | 把指定会话分叉到新的受管 Git worktree |
| `codex agents` | 浏览本机共享后台服务上的 agent 会话 |

几点以官方文档和 `--help` 为准：

- `codex resume --last` 默认只在当前目录找。加 `--all` 才跨目录。非交互会话要加 `--include-non-interactive` 才会出现在选择器和 `--last` 里。
- 当前目录和会话保存时的目录不一样时，Codex 会问用哪个。`tui.resume_cwd` 设为 `"current"` 或 `"session"` 可以不再问。命令行写了 `-C` 时，以 `-C` 为准。`codex fork` 使用同一套询问。
- **`--worktree` 有两处说法不一致。** 0.166.0 的 `codex resume --help` 列出了 `--worktree`。同一天的命令文档仍写：`codex resume` 接受模型和沙箱覆盖，但不接受 `--worktree`；分叉到 worktree 用 `codex fork --worktree`，必须写明会话 ID，不能用 `--last`，也不能走选择器。本文没有拿已有会话试这两种组合，所以不把帮助里多出来的旗标写成已经可用。`codex exec --worktree` 另有限制：文档写不能和 `resume`、`review`、`--ephemeral`、`--ignore-user-config` 一起用。

长任务中断后怎么接着做，见 [Codex CLI 恢复长任务](../11-自动化与高级工作流/04-CodexCLI恢复长任务.md) 和 [管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)。

## 排队任务：codex queue

`codex queue` 给已有会话排队一条文字消息。`--thread` 是会话 UUID 或精确的会话名，同名时用 UUID。`--message` 只接受文字。排队消息使用这条会话自己的模型。

```bash
codex queue --thread <SESSION_ID> --message "Run the remaining checks"
```

0.166.0 增加 `--resume`：排队之后，若线程还没加载，就尝试在本地 daemon 或 `--remote` 指定的服务器上把它拉起来。拉不起来会打印警告，命令仍然成功。远程服务器需要令牌时，用 `--remote-auth-token-env` 指出环境变量名。

不带 `--thread` 和 `--message` 时，0.166.0 直接报缺少这两个必填参数，退出码 2。本文没有已有会话，没有把一条消息真正排进去。

## 非交互执行：codex exec

`codex exec` 跑完就退出，适合脚本、CI 和定时任务。

| 命令 | 作用 |
|---|---|
| `codex exec "总结这个仓库的目录结构"` | 执行一次 |
| `codex e "..."` | `exec` 的简写 |
| `git diff \| codex exec "审查这段改动"` | 标准输入和提示词同时存在时，标准输入会作为 `<stdin>` 附在后面 |
| `codex exec --json "..."` | 以 JSONL 输出事件，每次状态变化一行 |
| `codex exec -o result.md "..."` | 把最后一条回复写进文件。长旗标是 `--output-last-message` |
| `codex exec --output-schema schema.json "..."` | 用 JSON Schema 约束最终回复的格式 |
| `codex exec --ephemeral "..."` | 不把会话文件保存到磁盘 |
| `codex exec --skip-git-repo-check "..."` | 允许在 Git 仓库外运行 |
| `codex exec resume --last "继续"` | 继续最近一次已记录的会话。默认仍看当前目录，`--all` 才跨目录 |
| `codex exec --worktree "实现下一步"` | 在新的受管 Git worktree 里跑。文档写这要求本地执行 |
| `codex exec fork <SESSION_ID> "试另一种做法"` | 把已保存会话复制成新会话再执行 |

在不是 Git 仓库、也没有被信任的目录里直接运行 `codex exec`，0.166.0 会拒绝，原文是：

```text
Not inside a trusted directory and --skip-git-repo-check was not specified.
```

另外两个开关：`--ignore-user-config` 不加载 `$CODEX_HOME/config.toml`（登录信息仍然从 `CODEX_HOME` 读）；`--ignore-rules` 不加载用户和项目的 `.rules`。

带图片、`--output-schema`、`--output-last-message` 或 `--ephemeral` 时，文档要求必须有提示词。`exec` 还有 `--cyber-access-program`，取值 `standard`、`daybreak_blue`、`daybreak_red`，帮助写明 review 不支持，fork 时还要有提示词。这是实验性 Cyber 计划的入口，说明见 [Daybreak Blue](../10-配置模型与权限安全/10-Codex-Daybreak-Blue申请开启与排障.md)。本文没有申请过。

官方文档建议在 CI 里把 `--json` 和 `--output-last-message` 一起用：前者记录过程，后者拿到最后的文字总结。

## 代码审查：codex review

文档要求只选一个审查目标。

| 命令 | 审查范围 |
|---|---|
| `codex review --uncommitted` | 已暂存、未暂存和未跟踪的改动 |
| `codex review --base main` | 当前分支相对 `main` 的改动 |
| `codex review --commit <SHA>` | 某个提交引入的改动 |
| `codex review --commit <SHA> --title "修复登录跳转"` | 在审查摘要里显示提交标题 |

`codex review` 是非交互的。`codex exec review` 是同一功能在 `exec` 下的入口。提示词写 `-` 时从标准输入读。四个预设、`review_model` 和提交前怎么接，见 [Codex 本地代码审查](../05-Git协作与代码审查/07-Codex本地代码审查-review命令与codex-review.md)。该文在 Codex CLI 0.167.0 上核对了参数冲突和未登录时的报错。

## 登录与账号

| 命令 | 作用 |
|---|---|
| `codex login` | 不带参数时打开浏览器，走 ChatGPT 账号登录。文档写也可以用 API Key 或访问令牌 |
| `codex login --device-auth` | 帮助里有这个旗标，说明文字是空的。本文不补一套设备码步骤 |
| `printenv OPENAI_API_KEY \| codex login --with-api-key` | 从标准输入读 API key。这是帮助里的示例 |
| `printf '%s' "$CODEX_ACCESS_TOKEN" \| codex login --with-access-token` | 从标准输入读访问令牌。文档用 `printf`，帮助示例用 `printenv CODEX_ACCESS_TOKEN` |
| `codex login status` | 查看登录状态。文档写有凭证时退出码为 0 |
| `codex logout` | 删除保存的登录凭证。文档写会同时去掉 API key 和 ChatGPT 登录 |

未登录时，0.166.0 的 `codex login status` 输出 `Not logged in`，退出码 1。把一个明显无效的字符串送进 `--with-access-token`，原文是 `Error logging in with access token: invalid agent identity JWT format`，退出码 1。谁能创建访问令牌，见 [访问令牌与服务账号](../11-自动化与高级工作流/14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)。

`codex logout --help` 仍有通用的 `-c`、`--enable`、`--disable`。命令文档写这个命令没有自己的旗标，意思是没有「只退出某一种登录」的参数。

## MCP、插件与扩展

| 命令 | 作用 |
|---|---|
| `codex mcp add <名称> -- <启动命令>` | 添加本地（stdio）MCP 服务器 |
| `codex mcp add <名称> --url <URL>` | 添加远程（streamable HTTP）MCP 服务器 |
| `codex mcp list` / `codex mcp get <名称>` | 查看已配置的 MCP 服务器 |
| `codex mcp login <名称>` / `codex mcp logout <名称>` | OAuth 登录和退出。文档写只适用于支持 OAuth 的 streamable HTTP 服务器 |
| `codex mcp remove <名称>` | 删除 MCP 服务器配置 |
| `codex plugin list` | 列出可用插件 |
| `codex plugin add <插件>` / `codex plugin remove <插件>` | 安装或卸载插件 |
| `codex plugin marketplace ...` | 添加、列出、升级或删除插件市场 |
| `codex features list` | 列出功能开关、所处阶段和当前是否启用 |
| `codex features enable <名称>` / `disable <名称>` | 把开关写进 `config.toml`。文档写 `features` 不接受 `--profile` |

`codex mcp add` 还有 `--env KEY=VALUE`（只给 stdio 服务器）和 `--bearer-token-env-var`（只给 streamable HTTP）。帮助里另有 `--oauth-client-id`、`--oauth-client-secret`、`--oauth-client-registration`、`--oauth-resource`。本文没有配过 OAuth 客户端。一个接入例子见 [Chrome DevTools MCP](../09-MCP与外部工具/06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)。

`codex features list` 每行三列：功能名、阶段、当前是否启用。0.166.0 实测片段：

```text
hooks                                    stable             true
memories                                 stable             false
standalone_web_search                    under development  false
web_search_cached                        deprecated         false
web_search_request                       deprecated         false
```

`enable` / `disable` 会写进配置，对以后的会话生效。网页搜索的现行写法是顶层 `web_search`，不要再靠这两个 deprecated 开关。见 [网页搜索设置](../10-配置模型与权限安全/18-Codex网页搜索设置-cached-indexed-live与allowed_domains.md)。

插件和市场的 `add`、`list`、`remove`、`upgrade` 可以加 `--json`。字段表以命令文档为准，这里不逐项抄。

## 权限与沙箱参数

下面这些参数可以写在 `codex`、`codex resume`、`codex fork` 等命令上。`codex exec --help` 没有 `--ask-for-approval` 和 `--search`。各子命令以自己的 `--help` 为准。

**模型和配置**

| 参数 | 作用 |
|---|---|
| `-m, --model <MODEL>` | 指定模型 |
| `-c key=value` | 临时覆盖配置。值按 TOML 解析；解析失败时，把原始字符串当作字面量 |
| `-p, --profile <名称>` | 在基础配置上叠加 `$CODEX_HOME/<名称>.config.toml` |
| `--enable <功能>` / `--disable <功能>` | 临时开关，等同于 `-c features.<名称>=true/false` |
| `--strict-config` | 配置里有当前版本不认识的字段时直接报错 |
| `--oss` / `--local-provider lmstudio\|ollama` | 使用本地开源模型 |

**目录和权限**

| 参数 | 作用 |
|---|---|
| `-C, --cd <DIR>` | 指定工作目录 |
| `--add-dir <DIR>` | 额外允许写入的目录 |
| `--worktree` | 在新的受管 Git worktree 里运行。和 `resume` 的组合见上一节的不一致说明 |
| `-s, --sandbox <模式>` | `read-only`、`workspace-write`、`danger-full-access` |
| `-a, --ask-for-approval <策略>` | `on-request`（由模型决定何时请求批准）或 `never`。交互式命令的帮助里有；`exec --help` 没有 |
| `--approve-for-me` | 审批请求交给自动审查，并使用 workspace-write 沙箱 |
| `--dangerously-bypass-approvals-and-sandbox` | 跳过确认、不用沙箱。帮助写明只适合本身已经隔离的环境 |
| `--dangerously-bypass-hook-trust` | 本次运行不检查 Hook 是否被信任。帮助写明只给已经审过 Hook 来源的自动化用 |

沙箱和审批怎么选，见 [权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

**界面和联网**

| 参数 | 作用 |
|---|---|
| `--search` | 这一次运行打开实时网页搜索。帮助写明开启后不再对每一次搜索单独审批。`codex exec` 不接受这个旗标 |
| `--no-alt-screen` | 不用全屏模式，保留终端的滚动历史 |
| `--no-daemon` | 不使用共享后台服务 |
| `--remote ws://host:port` | 把终端界面连接到远程 app server。也支持 `wss://` 和 `unix://` |
| `--remote-auth-token-env <变量名>` | 远程 WebSocket 需要 bearer 时，从哪个环境变量读 |

## 诊断：codex doctor

| 命令 | 作用 |
|---|---|
| `codex --version` | 查看版本。本文环境是 `codex-cli 0.166.0` |
| `codex doctor` | 检查安装、配置、登录、运行环境、Git、终端、后台服务和会话目录 |
| `codex doctor --summary` | 只看每项一行的摘要 |
| `codex doctor --json` | 输出经过打码的 JSON 报告 |
| `codex doctor --network-only` | 只跑配置、网络环境、提供商 HTTP 和 Responses WebSocket |
| `codex doctor --all` | 在详细的人类可读输出里展开长列表 |
| `codex doctor --ascii` | 用 ASCII 状态标签。另有 `--no-color` |
| `codex update` | 检查并安装新版本（需要当前安装方式支持自动更新） |
| `codex completion zsh` | 生成补全脚本。支持 `bash`（默认）、`zsh`、`fish`、`elvish`、`powershell` |
| `codex debug models` | 以 JSON 输出模型目录。文档写 `--bundled` 只看随二进制附带的目录 |
| `codex debug prompt-input` | 把模型能看见的提示输入渲染成 JSON |
| `codex sandbox -- <命令>` | 在 Codex 的沙箱里运行一条命令 |

在独立 `CODEX_HOME`、未登录、`TERM=dumb` 的这台 Linux 上，`codex doctor --network-only --summary --ascii` 的摘要节选是：

```text
Codex Doctor v0.166.0

Configuration
  [ok] config       loaded

Connectivity
  [ok] network      no proxy env vars
  [!!] websocket    Responses WebSocket failed; HTTPS fallback may still work - Check proxy, VPN, firewall, DNS, custom CA, and WebSocket policy support.
  [ok] reachability active provider endpoints are reachable over HTTP

3 ok | 1 notes | 1 warn | 0 fail degraded
```

退出码是 0。WebSocket 那条警告是这台机器当时的网络结果，不是「0.166.0 的 doctor 一定会警告」。完整输出怎么读，见 [Codex doctor 自检](../15-故障排查与常见问题/04-Codex-doctor自检-安装配置登录与网络排查.md)。那篇核对的是 0.164.0，还没有 `--network-only`。

`codex sandbox` 用的是 Codex 内部的沙箱策略。Linux 上实测，默认策略下写系统目录会被拦住：

```text
$ codex sandbox -- echo hi
hi
$ codex sandbox -- touch /etc/zz_codex_test
touch: cannot touch '/etc/zz_codex_test': Read-only file system
```

`sandbox` 还有子命令 `uninstall`，帮助写的是移除旧版 Windows 沙箱的机器级账号和网络规则。本文在 Linux 上没有运行它。升级和卸载见 [Codex 更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。

## 会话管理

| 命令 | 作用 |
|---|---|
| `codex archive <会话>` | 按 ID 或会话名归档 |
| `codex unarchive <会话>` | 取消归档 |
| `codex delete <会话>` | 永久删除。帮助写会先确认 |
| `codex delete --force <UUID>` | 不确认直接删除。帮助写明此时 SESSION 必须是 UUID |
| `codex apply <TASK_ID>` | 把 Codex 云端会话里最近一次改动用 `git apply` 应用到本地。文档写必须已登录且能访问该会话；`git apply` 失败时退出码非 0 |
| `codex cloud list` / `status` / `diff` / `apply` | 查看云端任务、看改动、应用到本地 |
| `codex cloud exec` | 不打开终端界面，提交一个新的云端任务。`cloud` 在帮助里标着实验性 |

`migrate-rollouts` 查看或迁移旧的本地会话。`migrate-nfs-db` 标着实验性，帮助写的是把配置的 SQLite 数据库就地迁到 DELETE 模式。

## 常用组合

```bash
# 在 CI 里只读审查当前改动，输出事件流和最终总结
codex exec --sandbox read-only --json -o review.md "审查本次改动，列出风险" > events.jsonl

# 换个目录、加一个可写目录，开始交互会话
codex -C ~/work/web --add-dir ~/work/shared "把共享组件里的按钮样式同步到 web 项目"

# 临时用高推理强度，不改配置文件
codex -c model_reasoning_effort='"high"' "排查这个偶发的测试失败"

# 给已有会话补一句，并尝试把线程拉起来
codex queue --thread <SESSION_ID> --message "跑剩下的检查" --resume

# 继续另一个目录里最近的一次会话
codex resume --all
```

`-c` 的值按 TOML 解析，字符串要带引号。上面的 `model_reasoning_effort` 没有在已登录会话里核对生效值。

## 小结

- 日常三个入口：`codex`（交互）、`codex exec`（非交互）、`codex resume --last`（继续）。给已经在跑的会话补消息，用 `codex queue`。
- 0.166.0 要单独记住的两个旗标：`codex queue --resume`，`codex doctor --network-only`。
- 权限从严到宽：`-s read-only`，然后 `-s workspace-write` 加 `--add-dir`，再是 `danger-full-access`。带 `dangerously` 的参数只在隔离环境里用。
- 遇到问题先跑 `codex --version` 和 `codex doctor`，再查具体子命令的 `--help`。
