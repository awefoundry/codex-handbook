---
id: codex-cli-commands-cheatsheet
title: Codex CLI 命令速查：codex 子命令与启动参数一览（0.164.0）
seo_title: Codex CLI 命令速查：子命令与启动参数一览
description: 按用途整理 Codex CLI 0.164.0 的 26 个子命令和常用启动参数：启动与恢复会话、非交互执行与代码审查、登录、MCP 与插件、权限与沙箱、诊断和会话管理。每条都核对过 codex --help 和 OpenAI 官方命令文档，附常用组合。
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
date_modified: 2026-10-26
verified_on: 2026-10-26
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/developer-commands?surface=cli
keywords: [Codex CLI 命令, codex 子命令, codex exec, codex resume, codex --help, Codex CLI 参数, Codex 命令速查]
faq:
  - q: codex 和 codex exec 有什么区别？
    a: 直接运行 codex 会打开交互式终端界面，过程中可以对话和审批；codex exec（简写 codex e）是非交互模式，执行完就退出，适合脚本和 CI。
  - q: 怎么继续上一次的 Codex 会话？
    a: 用 codex resume --last。它默认只在当前目录的会话里找最近一次，想跨目录找就加 --all。非交互任务用 codex exec resume --last。
  - q: 为什么 codex exec 提示 Not inside a trusted directory？
    a: codex exec 默认要求在 Git 仓库或已信任的目录里运行。确实要在别的目录运行时，加 --skip-git-repo-check。
  - q: codex mcp-server 命令去哪了？
    a: OpenAI 官方命令文档写明，codex mcp-server 和单独的 codex-mcp-server 程序已经移除，改用 codex app-server。
---

# Codex CLI 命令速查：codex 子命令与启动参数一览（0.164.0）

> 本文在线版：[codexguide.io/guides/codex-cli-commands-cheatsheet](https://codexguide.io/guides/codex-cli-commands-cheatsheet)

> 核对依据：OpenAI 官方文档 [Command line options](https://learn.chatgpt.com/docs/developer-commands?surface=cli)，以及在 Linux 上安装的 `codex-cli 0.164.0` 逐个运行 `codex --help` 和 26 个子命令的 `--help` 得到的输出。核对日期 2026-10-26。不同版本、不同系统的命令会有差异，以你本机 `codex --help` 为准。

这篇是给已经装好 Codex CLI 的人查命令用的。按“想做什么”分组，每组只列最常用的写法。第一次安装和登录请先看 [Codex 安装登录常见问题](../01-安装与首次使用/13-安装登录常见问题.md)；终端界面里以 `/` 开头的斜杠命令见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)，本文只讲在 shell 里输入的 `codex ...` 命令。

## 先看全貌：0.164.0 的 26 个子命令

在终端运行 `codex --help`，0.164.0 列出 26 个子命令（另有 `help`）。按用途分组如下：

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

`app-server`、`remote-control`、`migrate-nfs-db` 在帮助里标着 `[experimental]`，`cloud`、`exec-server` 标着 `[EXPERIMENTAL]`，用法以后可能变化。

官方文档里还有两个命令不在上面这张 Linux 版列表里：

- `codex app`：在 macOS 或 Windows 上从终端打开 ChatGPT 桌面端，没装时会启动安装程序。
- `codex execpolicy check`：检查 `.rules` 规则文件。实测 Linux 版 0.164.0 能运行 `codex execpolicy --help`，但它不在 `codex --help` 的列表里。

`codex mcp-server` 和单独的 `codex-mcp-server` 程序已经移除，官方文档建议改用 `codex app-server`。

## 开始和继续会话

| 命令 | 作用 |
|---|---|
| `codex` | 打开交互式终端界面 |
| `codex "修复登录页的报错"` | 打开终端界面并直接带上第一条提示词 |
| `codex -i screenshot.png "按这张图改样式"` | 附带图片（可以写多个） |
| `codex resume` | 打开会话列表，选一个继续 |
| `codex resume --last` | 直接继续最近一次会话 |
| `codex resume --all` | 列出所有目录的会话（默认只列当前目录的） |
| `codex resume <SESSION_ID>` | 按会话 ID 继续 |
| `codex fork --last` | 把最近一次会话复制成新会话再继续，原会话不变 |
| `codex queue --thread <THREAD> --message "..."` | 给已有会话排队一条消息 |
| `codex agents` | 浏览本机共享后台服务上的所有 agent 会话 |

几点细节（来自官方文档和 `--help`）：

- `codex resume --last` 默认只在**当前目录**的会话里找最近一次，加 `--all` 才跨目录。
- 非交互的 `codex exec` 会话默认不出现在 `resume` 里，要加 `--include-non-interactive`。
- 当前目录和会话保存时的目录不一样时，Codex 会问你用哪个目录。在 `config.toml` 里把 `tui.resume_cwd` 设为 `"current"` 或 `"session"` 可以不再询问；命令行里显式写 `-C` 时以 `-C` 为准。
- `codex resume` 不接受 `--worktree`。想把会话分叉到新的 Git worktree，用 `codex fork <SESSION_ID> --worktree`，这时必须写明会话 ID，不能用 `--last`。

长任务中断后怎么接着做，见 [Codex CLI 恢复长任务](../11-自动化与高级工作流/04-CodexCLI恢复长任务.md)。

## 非交互执行：codex exec

`codex exec` 跑完就退出，适合脚本、CI 和定时任务。

| 命令 | 作用 |
|---|---|
| `codex exec "总结这个仓库的目录结构"` | 执行一次，结果打印到终端 |
| `codex e "..."` | `exec` 的简写 |
| `git diff \| codex exec "审查这段改动"` | 从标准输入读内容；同时写了提示词时，标准输入会作为 `<stdin>` 附在后面 |
| `codex exec --json "..."` | 以 JSONL 格式输出事件，每次状态变化一行 |
| `codex exec -o result.md "..."` | 把最后一条回复写进文件 |
| `codex exec --output-schema schema.json "..."` | 用 JSON Schema 约束最终回复的格式 |
| `codex exec --ephemeral "..."` | 不把会话文件保存到磁盘 |
| `codex exec --skip-git-repo-check "..."` | 允许在 Git 仓库外运行 |
| `codex exec resume --last "继续"` | 继续当前目录最近一次非交互会话 |

在不是 Git 仓库、也没有被信任的目录里直接运行 `codex exec`，0.164.0 会拒绝执行：

```text
Not inside a trusted directory and --skip-git-repo-check was not specified.
```

另外两个和配置有关的开关：`--ignore-user-config` 不加载 `$CODEX_HOME/config.toml`（登录信息仍然从 `CODEX_HOME` 读）；`--ignore-rules` 不加载用户和项目的 `.rules` 规则文件。

官方文档建议在 CI 里把 `--json` 和 `--output-last-message` 一起用：前者记录过程，后者拿到最后的文字总结。

## 代码审查：codex review

| 命令 | 审查范围 |
|---|---|
| `codex review --uncommitted` | 已暂存、未暂存和未跟踪的改动 |
| `codex review --base main` | 当前分支相对 `main` 的改动 |
| `codex review --commit <SHA>` | 某个提交引入的改动 |
| `codex review --commit <SHA> --title "修复登录跳转"` | 在审查摘要里显示提交标题 |

`codex review` 是非交互的，结果直接打印。`codex exec review` 是同样功能在 `exec` 下的入口。

## 登录

| 命令 | 作用 |
|---|---|
| `codex login` | 不带参数时打开浏览器，走 ChatGPT 账号的 OAuth 登录 |
| `codex login --device-auth` | 用设备码方式登录 |
| `printenv OPENAI_API_KEY \| codex login --with-api-key` | 从标准输入读 API key 登录 |
| `codex login status` | 查看登录状态 |
| `codex logout` | 删除本机保存的登录凭据 |

官方文档写明，有凭据时 `codex login status` 的退出码是 0。实测没登录时它输出 `Not logged in`，退出码是 1，可以在脚本里用来判断。`codex logout` 会同时删除 API key 和 ChatGPT 两种登录凭据。

## 扩展：MCP、插件和功能开关

| 命令 | 作用 |
|---|---|
| `codex mcp add <名称> -- <启动命令>` | 添加本地（stdio）MCP 服务器 |
| `codex mcp add <名称> --url <URL>` | 添加远程（streamable HTTP）MCP 服务器 |
| `codex mcp list` / `codex mcp get <名称>` | 查看已配置的 MCP 服务器 |
| `codex mcp login <名称>` / `codex mcp logout <名称>` | MCP 服务器的 OAuth 登录和退出，只适用于支持 OAuth 的远程（streamable HTTP）服务器 |
| `codex mcp remove <名称>` | 删除 MCP 服务器配置 |
| `codex plugin list` | 列出可用插件 |
| `codex plugin add <插件>` / `codex plugin remove <插件>` | 安装或卸载插件 |
| `codex plugin marketplace ...` | 添加、列出、升级或删除插件市场 |
| `codex features list` | 列出所有功能开关、所处阶段和当前是否启用 |
| `codex features enable <名称>` / `disable <名称>` | 在 `config.toml` 里打开或关闭某个功能 |

`codex mcp add` 还支持 `--env KEY=VALUE`（给本地服务器传环境变量）和 `--bearer-token-env-var`（远程服务器从环境变量读令牌）。一个完整的接入例子见 [Codex 接入 Chrome DevTools MCP](../09-MCP与外部工具/06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)。

`codex features list` 每行三列：功能名、阶段（如 `stable`、`experimental`、`under development`、`removed`）、当前是否启用。0.164.0 实测片段：

```text
browser_use_full_cdp_access              stable             true
hooks                                    stable             true
memories                                 stable             false
```

## 启动参数：所有入口通用的几个

下面这些参数可以写在 `codex`、`codex exec`、`codex resume` 等命令后面（各子命令支持的范围以 `--help` 为准）。

**模型和配置**

| 参数 | 作用 |
|---|---|
| `-m, --model <MODEL>` | 指定模型 |
| `-c key=value` | 临时覆盖 `config.toml` 里的某个值，值按 TOML 解析，例如 `-c model_reasoning_effort="high"` |
| `-p, --profile <名称>` | 在基础配置上叠加 `$CODEX_HOME/<名称>.config.toml` |
| `--enable <功能>` / `--disable <功能>` | 临时开关某个功能，等同于 `-c features.<名称>=true/false` |
| `--strict-config` | `config.toml` 里有当前版本不认识的字段时直接报错 |
| `--oss` / `--local-provider lmstudio\|ollama` | 使用本地开源模型 |

**目录和权限**

| 参数 | 作用 |
|---|---|
| `-C, --cd <DIR>` | 指定工作目录 |
| `--add-dir <DIR>` | 额外允许写入的目录 |
| `--worktree` | 在新的受管 Git worktree 里运行 |
| `-s, --sandbox <模式>` | `read-only`、`workspace-write`、`danger-full-access` |
| `-a, --ask-for-approval <策略>` | `on-request`（由模型决定何时请求批准）或 `never`（从不询问） |
| `--approve-for-me` | 审批请求交给自动审查处理，配合 `workspace-write` 沙箱 |
| `--dangerously-bypass-approvals-and-sandbox` | 跳过所有确认、不用沙箱。帮助里写明只适合本身已经隔离的环境 |
| `--dangerously-bypass-hook-trust` | 本次运行不检查 Hook 是否被信任。帮助里写明只给已经审过 Hook 来源的自动化用 |

官方文档的建议：

- 本地日常开发用 `--sandbox workspace-write --ask-for-approval on-request`。
- 需要写更多目录时优先用 `--add-dir`，不要直接切到 `danger-full-access`。
- `--dangerously-bypass-approvals-and-sandbox` 只在专门的沙箱虚拟机里用。

沙箱和审批怎么选，见 [权限沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

**界面和联网**

| 参数 | 作用 |
|---|---|
| `--search` | 打开实时网页搜索（默认是缓存模式），开启后每次搜索不再单独审批 |
| `--no-alt-screen` | 不用全屏模式，保留终端的滚动历史 |
| `--no-daemon` | 不使用共享后台服务 |
| `--remote ws://host:port` | 把终端界面连接到远程 app server，也支持 `wss://` 和 `unix://` |

## 诊断和维护

| 命令 | 作用 |
|---|---|
| `codex --version` | 查看版本，例如 `codex-cli 0.164.0` |
| `codex doctor` | 检查安装、配置、登录、运行环境、Git、终端和网络 |
| `codex doctor --summary` | 只看每项检查一行的摘要 |
| `codex doctor --json` | 输出 JSON 报告，方便脚本处理或附在问题反馈里 |
| `codex update` | 检查并安装新版本（需要当前安装方式支持自动更新） |
| `codex completion zsh > "${fpath[1]}/_codex"` | 生成 shell 自动补全脚本；支持 `bash`（默认）、`zsh`、`fish`、`elvish`、`powershell` |
| `codex debug models` | 以 JSON 输出模型列表原始数据 |
| `codex sandbox -- <命令>` | 在 Codex 的沙箱里运行一条命令，用来确认沙箱会拦住什么 |

`codex sandbox` 用的是 Codex 内部同样的沙箱策略。在 Linux 上实测，默认策略下写系统目录会被拦住：

```text
$ codex sandbox -- echo hi
hi
$ codex sandbox -- touch /etc/zz_test
touch: cannot touch '/etc/zz_test': Read-only file system
```

`codex doctor` 的完整用法和输出解读见 [Codex doctor 自检](../15-故障排查与常见问题/04-Codex-doctor自检-安装配置登录与网络排查.md)。升级、卸载见 [Codex 更新与卸载](../01-安装与首次使用/12-Codex更新与卸载.md)。

## 会话管理

| 命令 | 作用 |
|---|---|
| `codex archive <会话>` | 按 ID 或会话名归档 |
| `codex unarchive <会话>` | 取消归档 |
| `codex delete <会话>` | 永久删除，会先确认 |
| `codex delete --force <UUID>` | 不确认直接删除，此时必须写会话的 UUID |
| `codex apply <TASK_ID>` | 把 Codex 云端会话里最近一次改动用 `git apply` 应用到本地仓库（需要已登录、能访问该会话） |
| `codex cloud list` / `status` / `diff` / `apply` | 查看 Codex Cloud 任务、看改动、应用到本地 |

## 常用组合

```bash
# 在 CI 里只读审查当前改动，输出事件流和最终总结
codex exec --sandbox read-only --json -o review.md "审查本次改动，列出风险" > events.jsonl

# 换个目录、加一个可写目录，开始交互会话
codex -C ~/work/web --add-dir ~/work/shared "把共享组件里的按钮样式同步到 web 项目"

# 临时用高推理强度，不改配置文件
codex -c model_reasoning_effort="high" "排查这个偶发的测试失败"

# 继续另一个目录里最近的一次会话
codex resume --all
```

## 小结

- 记三个入口就够日常用：`codex`（交互）、`codex exec`（非交互）、`codex resume --last`（继续）。
- 权限相关参数从严到宽：`-s read-only` → `-s workspace-write` + `--add-dir` → `danger-full-access`；带 `dangerously` 的参数只在隔离环境里用。
- 遇到问题先跑 `codex --version` 和 `codex doctor`，再查具体子命令的 `--help`。
