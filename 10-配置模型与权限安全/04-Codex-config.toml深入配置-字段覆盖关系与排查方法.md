---
id: config-toml-guide
title: Codex config.toml 配置指南：配置层级、-c 临时覆盖、Profile 文件和生效检查（0.164.0 实测）
seo_title: Codex config.toml 配置指南：层级、-c 覆盖、Profile 与生效检查
description: Codex 的 config.toml 按 7 个层级解析，CLI 参数、受信任项目、Profile 文件、用户配置依次覆盖。本文用 0.164.0 隔离实测演示怎么看 exec 启动摘要确认生效值、-c 临时覆盖、Profile 单独文件写法、--strict-config 查错，以及不生效时的排查顺序。
url: /advanced/config-toml
status: published
section: advanced
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, IDE, App]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-09-22
date_modified: 2026-10-24
verified_on: 2026-10-24
tested_cli_version: 0.164.0
models: [gpt-6.1-sol]
official_ref: https://learn.chatgpt.com/docs/config-file/config-basic
keywords: [config.toml, Codex 配置, 配置优先级, Codex profile, -c 覆盖, strict-config]
related: [codex-cli-presets-inline-model, codex-amazon-bedrock]
howto: false
faq:
  - q: Codex 的 config.toml 在哪里？
    a: 用户配置在 ~/.codex/config.toml，设置了 CODEX_HOME 时在 $CODEX_HOME/config.toml。项目配置放在仓库里的 .codex/config.toml，只有项目受信任时才加载。
  - q: 0.134.0 以后 Profile 怎么写？
    a: 每个 Profile 是单独的文件 ~/.codex/<名字>.config.toml，用顶层键书写，运行时用 --profile <名字> 选择。config.toml 里的 [profiles.<名字>] 表和 profile = "<名字>" 选择器不再生效。
  - q: 怎么确认某个值最终生效了？
    a: 交互界面用 /status；脚本里看 codex exec 开头打印的启动摘要，里面有 model、provider、approval、sandbox、reasoning effort 等最终值。
---

# Codex config.toml 配置指南：配置层级、-c 临时覆盖、Profile 文件和生效检查（0.164.0 实测）

> 本文在线版：[codexguide.io/advanced/config-toml](https://codexguide.io/advanced/config-toml)

> 核对依据：OpenAI 官方文档 [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)、[Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)、[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 和 [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)。实测环境是 Linux 上的 `codex-cli 0.164.0`，使用独立的 `CODEX_HOME` 和临时项目，**没有登录**，所以只验证到配置解析和启动摘要，没有发出模型请求。核对日期 2026-10-24。

`config.toml` 用来保存稳定的运行偏好：默认模型、推理强度、审批策略、沙箱、MCP 服务器等。它不是“把所有开关抄一遍”的总配置，也不是绕过审批、扩大权限的捷径。

这篇讲三件事：配置从哪几层来、谁覆盖谁；怎么临时覆盖和分场景切换；改完怎么确认真的生效了。

## 什么时候需要写配置

默认设置能完成任务时，不必急着建 `config.toml`。出现下面的情况再写：

- 每次都要重复选同一个审批或沙箱边界；
- 想固定个人默认的模型或推理强度；
- 某个项目需要一份团队共享、经过审查的最低安全基线；
- 想把审查、日常开发、CI 的偏好分开（用 Profile 文件）。

一次性试验用命令行参数或 `-c` 覆盖，确认行为后再写进文件。只想在当前会话里换模型或权限，0.164.0 起可以直接用内联的 `/model`、`/permissions`，见 [Codex CLI /presets 与内联 /model、/permissions](../12-官方工具与集成/15-Codex-CLI-presets预设与内联model-permissions命令.md)。

## 配置从哪里来：7 个层级

官方文档给出的解析顺序，**越靠上优先级越高**：

| 优先级 | 来源 | 说明 |
| --- | --- | --- |
| 1 | CLI 参数和 `-c` / `--config` | 只影响这一次运行 |
| 2 | 项目配置 `.codex/config.toml` | 从项目根目录到当前目录逐层加载，离当前目录最近的优先；**只在项目受信任时加载** |
| 3 | Profile 文件 | 用 `--profile <名字>` 选择，文件是 `~/.codex/<名字>.config.toml` |
| 4 | 用户配置 | `~/.codex/config.toml`（设置了 `CODEX_HOME` 时在该目录下） |
| 5 | 云端托管的 `config.toml` 默认值 | 登录的工作区下发时才有 |
| 6 | 系统配置 | Unix 上是 `/etc/codex/config.toml`（存在时） |
| 7 | 内置默认值 | 前面都没设置时使用 |

几点要注意：

- Codex 是**按键**合并这些层的，不是用高层文件整个替换低层文件。
- 项目被标为不受信任时，项目里的 `.codex/` 层（配置、hooks、规则）全部跳过；用户和系统层照常加载。
- 托管机器上，组织还可以用 `requirements.toml` 限制取值，比如禁止 `approval_policy = "never"` 或 `sandbox_mode = "danger-full-access"`。这是约束，不是默认值，本地配置放宽不了。
- 项目配置里的相对路径（比如 `model_instructions_file`）相对于该 `.codex/` 目录解析。

### 实测：谁覆盖了谁

在一个隔离目录里，用户配置写 `model_reasoning_effort = "medium"`，Profile 文件 `review.config.toml` 写 `"high"`，项目 `.codex/config.toml` 写 `"xhigh"`，再分别运行 `codex exec`，看启动摘要里的 `reasoning effort` 一行：

| 运行方式 | 实测结果 | 说明 |
| --- | --- | --- |
| 只有用户配置 | `medium` | 第 4 层 |
| 加 `--profile review` | `high` | Profile（第 3 层）覆盖用户配置 |
| `--profile review -c model_reasoning_effort="low"` | `low` | `-c`（第 1 层）覆盖 Profile |
| 项目**未受信任**，项目里写了 `xhigh` | `medium` | 项目层被跳过 |
| 项目**受信任**，再加 `--profile review` | `xhigh` | 项目层（第 2 层）覆盖 Profile |

结果和官方顺序一致。

## 一份保守的最小配置

```toml
# ~/.codex/config.toml（或 $CODEX_HOME/config.toml）
approval_policy = "on-request"
sandbox_mode = "read-only"
model_reasoning_effort = "medium"
```

- `approval_policy = "on-request"`：需要时停下来等你确认。它控制**什么时候问**，不额外授予权限。
- `sandbox_mode = "read-only"`：命令只能在只读边界内运行，适合先调查项目。需要改文件时，在这次运行里显式选合适的沙箱。
- `model_reasoning_effort = "medium"`：调整模型的推理投入。官方列出的取值有 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`，但**能用哪些取决于模型和客户端**。

想固定默认模型，加一行 `model = "gpt-6.1-sol"`（需要你的账号能用这个模型）。

### 权限配置（permission profiles）

除了 `sandbox_mode`，Codex 还支持命名的权限配置，用来复用文件系统和网络策略。内置三个：`:read-only`、`:workspace`、`:danger-full-access`。自定义的写在 `[permissions.<名字>]` 表里，并把 `default_permissions` 设成同名。细节见官方 [Permissions](https://learn.chatgpt.com/docs/permissions) 文档和[权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

### 网页搜索

```toml
web_search = "cached"
```

官方列出的 4 个取值：

- `cached`（默认）：从 OpenAI 维护的搜索缓存返回结果，不实时抓网页，能减少来自任意网页的提示注入；
- `indexed`：只有经过搜索索引放行时才访问外部网页；
- `live`：实时抓取最新网页，等同 `--search`；
- `disabled`：关闭网页搜索工具。

搜索结果仍然是外部输入，不能当成可信指令。

### 项目级配置

项目配置只放团队愿意共享的最低边界：

```toml
# <仓库>/.codex/config.toml
sandbox_mode = "read-only"
```

不要把 API Key、代理密码、个人路径、`auth.json` 或账号信息放进仓库。项目配置也不能覆盖改写凭证去向等敏感设置，详见 Advanced Config 的 Project config files 一节。

## -c 临时覆盖

优先用专用参数（比如 `--model`、`--sandbox`），没有专用参数时用 `-c` / `--config`：

```bash
codex --model gpt-6.1-sol
codex --config model='"gpt-6.1-sol"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

规则（来自官方 Advanced Config）：

- 键可以用点号写嵌套值，比如 `mcp_servers.context7.enabled=false`；
- 值按 **TOML** 解析，不是 JSON；拿不准时给整个值加引号，免得 shell 按空格拆开；
- 值解析不成 TOML 时，Codex 当成字符串处理。

`codex exec` 后面同样可以接 `-c`。0.164.0 还修了一个问题：以前 `-c` 同时写在多级命令上时（比如 `codex -c … mcp add -c …`），只有最深一级的值会保留；现在每一级的覆盖都会按顺序收集（[#56022](https://github.com/openai/codex/pull/56022)）。

## Profile 文件：0.134.0 以后的写法

Profile 把一组差异值存成单独的文件，用 `--profile` 切换：

```toml
# ~/.codex/review.config.toml
model_reasoning_effort = "high"
sandbox_mode = "read-only"
```

```bash
codex --profile review
codex exec --profile review "review this change"
```

- 文件名是 `<名字>.config.toml`，名字只能用字母、数字、连字符和下划线；
- 文件里直接写**顶层键**，不要再包一层 `[profiles.review]`；
- Profile 叠加在用户配置之上，所以只写和用户配置不同的值。

**旧写法已失效**：从 Codex 0.134.0 起，`--profile` 不再读取 `config.toml` 里的 `[profiles.<名字>]` 表，顶层的 `profile = "<名字>"` 选择器也不再支持。旧配置要把内容搬到单独的 Profile 文件里，再删掉原来的表和选择器。

## 改完怎么确认生效

### 交互界面：/status

在 CLI 里运行 `/status`，可以看到当前的模型、provider、权限等。注意内联 `/model`、`/permissions` 改的是当前会话，`/status` 显示的是会话里的实际值，不一定等于配置文件。

### 脚本里：看 codex exec 的启动摘要

`codex exec` 每次启动都会先打印一段摘要，里面就是各层合并后的最终值。实测（没有登录，摘要打印完后请求因 401 失败，摘要本身不受影响）：

```text
OpenAI Codex v0.164.0
--------
workdir: ~/codex-probe/project
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: …
--------
```

（workdir 已换成示例路径，session id 已省略。）

这段摘要在“有没有生效”的排查里最有用：改一个值、跑一次，看对应那一行变了没有。

### 关于 exec 里的 approval

上面的配置写的是 `approval_policy = "on-request"`，但 `codex exec` 的摘要显示 `approval: never`。实测把全局参数放到子命令前（`codex --ask-for-approval on-request exec …`），摘要仍然是 `never`。

`exec` 是非交互运行，没有人在旁边点批准。官方 [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) 的建议是：

- `codex exec` 默认在**只读沙箱**里运行；
- 需要改文件时用 `--sandbox workspace-write`，更大的权限只在隔离的 CI 或容器里用；
- `--full-auto` 已不再支持；想让审批请求走自动审查，用 `--approve-for-me`；
- 需要不加载 `$CODEX_HOME/config.toml` 的运行时，用 `--ignore-user-config`。

所以在脚本里控制边界，靠的是**沙箱**，而不是指望 exec 停下来问你。本文旧版曾建议用 `codex --ask-for-approval on-request exec …` 让 exec 按需审批，0.164.0 实测并不能改变摘要里的 `approval: never`，这条建议已删除。

### 用 --strict-config 查拼写错误

实测不加 `--strict-config` 时，配置里的未知字段不会报错，`codex exec` 照常启动，写错的键等于没写。在要运行的子命令上加 `--strict-config`，未知字段会直接报错：

```bash
codex exec --strict-config "只读列出当前目录文件"
```

实测在配置里加一行 `not_a_real_key = 1`：

```text
Error loading config.toml:
~/codex-probe/home/config.toml:4:1: unknown configuration field `not_a_real_key`
  |
4 | not_a_real_key = 1
```

（路径已换成示例路径。）报错给出了文件、行号和字段名。

### 在隔离目录里试

不想动真实的 `~/.codex` 时，建一个临时目录当 `CODEX_HOME`：

```bash
probe_home="$HOME/codex-probe/home"
probe_project="$HOME/codex-probe/project"
mkdir -p "$probe_home" "$probe_project"

cat > "$probe_home/config.toml" <<'TOML'
approval_policy = "on-request"
sandbox_mode = "read-only"
model_reasoning_effort = "medium"
TOML

CODEX_HOME="$probe_home" codex exec --strict-config --ephemeral \
  --skip-git-repo-check -C "$probe_project" \
  "只读列出当前目录文件，不修改任何内容。"
```

- 没有登录时，命令会在打印摘要之后的模型请求阶段失败。这只说明配置解析完成了，**不代表**模型行为验证完成。
- 实测把 `CODEX_HOME` 放在 `/tmp` 下时，会先出现一行 `WARNING: proceeding, even though we could not create PATH aliases: Refusing to create helper binaries under temporary dir "/tmp"`，之后照常继续。放在用户目录下就没有这行。
- 新的隔离目录里没有登录信息，想做真实请求的测试，需要在这个目录里重新登录。

## 改了却没生效：排查顺序

1. **路径**：在运行 Codex 的同一个终端里 `echo "$CODEX_HOME"`；确认文件名是 `config.toml`，不是 `config.toml.txt`。
2. **环境**：Windows、WSL、macOS/Linux 各有自己的用户目录。不要在 Windows 目录里改完，却从 WSL 启动 Codex。
3. **项目信任**：项目不受信任时，项目里的 `.codex/config.toml`、hooks 和规则会一起被跳过。
4. **语法和字段**：检查引号、布尔值、表头和重复键；用 `--strict-config` 抓未知字段。字段对照[官方 Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)。
5. **旧 Profile 写法**：还在用 `[profiles.x]` 或 `profile = "x"`？0.134.0 起不再生效，改成单独文件。
6. **覆盖顺序**：按上面的 7 层表，逐层找是谁给了最终值。跑一次 `codex exec` 看摘要最快。
7. **组织约束**：管理员的 `requirements.toml` 不能被本地配置绕过，被拒绝的值找管理员确认。
8. **重新启动**：配置在每次新运行开始时读取。结束当前会话，从目标目录重新启动再检查。

## 备份与恢复

改真实配置前先备份：

```bash
codex_root="${CODEX_HOME:-$HOME/.codex}"
config_path="$codex_root/config.toml"
backup_path="$config_path.bak.$(date +%Y%m%d-%H%M%S)"
cp "$config_path" "$backup_path"
```

出问题时恢复，再重新启动：

```bash
cp "$backup_path" "$config_path"
```

练习用的隔离目录用完删掉即可：

```bash
rm -rf "$HOME/codex-probe"
```

不要把备份、日志、`auth.json`、环境变量或真实用户路径提交到仓库。`approval_policy = "never"` 和 `danger-full-access` 会去掉重要防线，只适合有外层隔离、经过专门审查的环境，不能当新手默认值。

## 相关阅读

- [Codex 模型和推理强度怎么选](./01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)
- [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [Codex 沙箱与主机权限风险](./05-Codex沙箱与主机权限风险.md)
- [Codex AGENTS.md 教程](./07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)：项目规则写在 AGENTS.md，运行配置写在 config.toml。
- [Codex 接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)：用 `model_provider` 切换模型来源。

## 参考资料

- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Permissions](https://learn.chatgpt.com/docs/permissions)
- [Codex CLI 0.164.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.164.0)
