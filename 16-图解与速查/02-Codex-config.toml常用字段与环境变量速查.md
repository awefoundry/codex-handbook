---
id: codex-config-toml-cheatsheet
title: Codex config.toml 常用字段与环境变量速查（0.165.0）
seo_title: Codex config.toml 常用字段速查：模型、沙箱、MCP、界面与环境变量
description: 按用途整理 Codex config.toml 最常用的字段：模型、审批与沙箱、项目信任、MCP、历史与日志、界面、功能开关和模型提供商，以及 CODEX_HOME、CODEX_API_KEY 等环境变量。每项给出写法和官方说明，附一份起步配置。
lede: 想改 Codex 的某个行为，先在这里找到字段名，再去官方 Configuration Reference 看完整说明。
url: /guides/codex-config-toml-cheatsheet
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 参考
source_tag: 官方功能
entry_tags: [CLI, IDE, App]
difficulty: 入门
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-28
date_modified: 2026-10-28
verified_on: 2026-10-28
tested_cli_version: 0.165.0
official_ref: https://learn.chatgpt.com/docs/config-file/config-reference
keywords: [Codex config.toml, Codex 配置速查, config.toml 字段, CODEX_HOME, Codex 环境变量, Codex 配置文件在哪]
faq:
  - q: Codex 的 config.toml 在哪里？
    a: 用户配置在 ~/.codex/config.toml（设置了 CODEX_HOME 就在 $CODEX_HOME/config.toml）。项目里还可以放 .codex/config.toml，但只有项目被信任时才会加载。
  - q: 怎么检查 config.toml 有没有写错字段名？
    a: 用 codex exec --strict-config 或 codex --strict-config 启动。0.165.0 实测，字段名拼错会直接报 unknown configuration field 并指出行号；不加这个参数时，未知字段会被忽略。
  - q: 只想临时改一次配置怎么办？
    a: 启动时加 -c 字段=值，例如 codex -c model_reasoning_effort=high。只影响这一次运行，不改文件。
  - q: approval_policy 还能写 untrusted 吗？
    a: 不能。官方已停用 approval_policy = "untrusted"，交互使用写 on-request，非交互写 never。项目信任用的是另一个字段 projects.<路径>.trust_level。
  - q: CODEX_HOME 指向的目录不存在会怎样？
    a: 官方文档要求目录必须已存在。0.165.0 实测会直接报错退出：CODEX_HOME points to "...", but that path does not exist。
---

# Codex config.toml 常用字段与环境变量速查（0.165.0）

> 本文在线版：[codexguide.io/guides/codex-config-toml-cheatsheet](https://codexguide.io/guides/codex-config-toml-cheatsheet)

> 核对依据：OpenAI 官方文档 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)、[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)、[Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 和 [Environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables)。文末的起步配置和几条报错在 Linux 上用 `codex-cli 0.165.0` 和单独的 Codex home 实测。核对日期 2026-10-28（北京时间）。字段会随版本变化，以官方 Reference 为准。

## 这篇的范围

- **本文**：常用字段叫什么、填什么值、管什么。
- **不在本文**：配置分几层、谁覆盖谁、Profile 文件怎么写、改了不生效怎么查，这些见 [config.toml 配置指南](https://codexguide.io/advanced/config-toml)。
- 官方 Reference 里有 300 多个字段，这里只挑日常会改的。企业管理员用的 `requirements.toml` 不在本文范围。

## 文件在哪、怎么临时改

| 项目 | 说明 |
|---|---|
| 用户配置 | `~/.codex/config.toml`；设置了 `CODEX_HOME` 就是 `$CODEX_HOME/config.toml` |
| 项目配置 | 项目里的 `.codex/config.toml`，**只有项目被信任时才加载** |
| Profile | `~/.codex/<名字>.config.toml`，用 `codex --profile <名字>` 叠加 |
| 临时覆盖 | `codex -c 字段=值`，例如 `codex -c model_reasoning_effort=high` |
| 检查拼写 | `codex --strict-config` 或 `codex exec --strict-config`，遇到不认识的字段直接报错 |

`--strict-config` 的实测效果（故意把 `model_reasoning_effort` 写错）：

```text
Error loading config.toml:
<CODEX_HOME>/config.toml:2:1: unknown configuration field `model_reasoning_efort`
  |
2 | model_reasoning_efort = "medium"
  | ^^^^^^^^^^^^^^^^^^^^^
```

取值写错时，不加 `--strict-config` 也会报错，例如 `codex -c sandbox_mode=bogus`：

```text
Error: unknown variant `bogus`, expected one of `read-only`, `workspace-write`, `danger-full-access`
in `sandbox_mode`
```

## 模型与推理

| 字段 | 写法 / 取值 | 作用 |
|---|---|---|
| `model` | `"gpt-6.1-sol"` 等 | 默认模型 |
| `model_reasoning_effort` | `low`、`medium`、`high`、`xhigh`、`max`、`ultra` | 推理强度，可选档位取决于模型 |
| `plan_mode_reasoning_effort` | 同上 | 只用于 Plan 模式的推理强度；不写就用内置默认 |
| `model_reasoning_summary` | `auto`、`concise`、`detailed`、`none` | 推理摘要的详细程度，`none` 关闭 |
| `model_verbosity` | `low`、`medium`、`high` | 回答的详略 |
| `service_tier` | `"fast"` 等 | 新一轮请求用的服务档位，`fast` 即 Fast 模式 |
| `review_model` | 模型名 | `/review` 代码审查用的模型 |
| `model_context_window` | 数字 | 当前模型可用的上下文窗口 |
| `model_auto_compact_token_limit` | 数字 | 达到多少 token 时自动压缩历史；不写用模型默认 |
| `personality` | `"none"` | 去掉内置的「性格」说明 |

模型怎么选，见 [Codex 模型怎么选](../10-配置模型与权限安全/01-Codex模型怎么选-推理强度Low-Medium-High有什么区别.md)。

## 审批、沙箱与权限

| 字段 | 写法 / 取值 | 作用 |
|---|---|---|
| `approval_policy` | `on-request`、`never`，或 `{ granular = { ... } }` | 什么时候停下来问你。交互用 `on-request`，脚本用 `never`。`untrusted` 已停用，`on-failure` 已弃用 |
| `approvals_reviewer` | `user`（默认）、`auto_review` | 审批请求由你本人看，还是交给自动审核子代理 |
| `sandbox_mode` | `read-only`、`workspace-write`、`danger-full-access` | 执行命令时的文件和网络权限 |
| `sandbox_workspace_write.writable_roots` | 路径数组 | `workspace-write` 下额外可写的目录 |
| `sandbox_workspace_write.network_access` | `true` / `false` | `workspace-write` 下是否允许联网 |
| `default_permissions` | `":workspace"`、`":read-only"` 或自定义名 | 使用命名权限配置（`[permissions.<名字>]`） |
| `web_search` | `cached`（默认）、`indexed`、`live`、`disabled` | 网页搜索模式。用 `--yolo` 等完全放开的设置时默认变成 `live` |
| `windows.sandbox` | `mxc`、`elevated`、`unelevated` | Windows 原生沙箱实现 |

沙箱和审批怎么搭配，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 项目信任与 AGENTS.md

| 字段 | 写法 / 取值 | 作用 |
|---|---|---|
| `projects."<绝对路径>".trust_level` | `"trusted"`、`"untrusted"` | 标记项目是否可信。untrusted 会跳过项目级 `.codex/` 配置、hooks 和 rules |
| `project_root_markers` | 默认相当于 `[".git"]` | 用哪些文件判断项目根；写 `[]` 表示把当前目录当项目根 |
| `project_doc_max_bytes` | 数字，默认 32 KiB | AGENTS.md 合并后最多读多少字节 |
| `project_doc_fallback_filenames` | 文件名数组 | 没有 AGENTS.md 时还找哪些文件名 |
| `developer_instructions` | 字符串 | 每个会话额外注入的开发者说明 |
| `model_instructions_file` | 文件路径 | 用自己的文件替换内置基础指令（慎用） |

信任设置和 AGENTS.md 的安全问题，见 [防范 AGENTS.md 投毒](../10-配置模型与权限安全/15-Codex防范AGENTS.md投毒-Downloads目录风险与config.toml自查.md)；AGENTS.md 本身怎么写，见 [AGENTS.md 怎么写](https://codexguide.io/advanced/agents-md)。

## MCP 服务器

每个服务器一个 `[mcp_servers.<名字>]` 段落：

| 字段 | 作用 |
|---|---|
| `command`、`args`、`env`、`cwd` | 本地（stdio）服务器的启动命令、参数、环境变量、工作目录 |
| `url` | 远程（streamable HTTP）服务器地址 |
| `bearer_token_env_var` | 从哪个环境变量读 Bearer Token |
| `enabled` | `false` 可以先停用，不用删配置 |
| `required` | 启动失败时是否让 Codex 报错 |
| `enabled_tools` / `disabled_tools` | 只开放或屏蔽部分工具 |
| `startup_timeout_sec` | 启动超时，默认 10 秒 |
| `tool_timeout_sec` | 单次工具调用超时，默认 60 秒 |
| `default_tools_approval_mode`、`tools.<工具>.approval_mode` | 工具调用的审批方式 |

新手入门见 [Codex MCP 入门](../09-MCP与外部工具/01-Codex-MCP入门-config与mcp-login.md)。

## 记忆、历史与日志

| 字段 | 写法 / 取值 | 作用 |
|---|---|---|
| `features.memories` | `true` / `false`（默认关） | 开启 Memories |
| `memories.generate_memories` | 默认 `true` | `false` 时新对话不再用于生成记忆 |
| `memories.use_memories` | 默认 `true` | `false` 时不把已有记忆注入新会话 |
| `history.persistence` | `save-all`、`none` | 是否把会话记录写进 `history.jsonl` |
| `history.max_bytes` | 数字 | 历史文件上限，超出删最旧的 |
| `log_dir` | 路径，默认 `$CODEX_HOME/log` | 日志目录；显式设置后还会写纯文本的 `codex-tui.log` |
| `sqlite_home` | 路径 | SQLite 状态库的位置 |

Memories 详见 [Codex Memories 记忆功能](../11-自动化与高级工作流/09-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)。

## 界面（`[tui]`）与其他体验

| 字段 | 作用 |
|---|---|
| `tui.theme` | 语法高亮主题，也可以用 `/theme` 选 |
| `tui.notifications`、`tui.notification_method`、`tui.notification_condition` | 桌面通知开关、方式、条件 |
| `tui.status_line`、`tui.terminal_title` | 底部状态栏、终端窗口标题显示哪些内容 |
| `tui.keymap.<场景>.<动作>` | 改快捷键 |
| `tui.alternate_screen` | `auto`、`always`、`never`，是否用全屏备用屏幕 |
| `file_opener` | 点击引用时用哪个编辑器打开：`vscode`（默认）、`vscode-insiders`、`windsurf`、`cursor`、`none` |
| `hide_agent_reasoning` | 在界面和 `codex exec` 输出里隐藏推理过程 |
| `notify` | 一个命令数组，Codex 有通知时调用它并传入 JSON |
| `check_for_update_on_startup` | 启动时是否检查更新 |

界面相关的完整说明，见 [Codex CLI 终端界面设置速查](./03-Codex-CLI终端界面设置速查-主题补全编辑器状态栏与改键.md)。

## 功能开关（`[features]`）

官方 Config basics 列出的常用开关（值为默认值）：

| 开关 | 默认 | 作用 |
|---|---|---|
| `apps` | 开 | 应用（连接器）集成 |
| `goals` | 开 | 目标持久化和自动继续 |
| `hooks` | 开 | 生命周期 Hooks |
| `fast_mode` | 开 | 允许选 Fast 模式 |
| `memories` | 关 | Memories |
| `multi_agent` | 开 | 子代理协作 |
| `shell_snapshot` | 开 | 缓存 Shell 环境，加快重复命令 |

想看本机版本所有开关和状态，运行 `codex features list`。

## 模型提供商与登录

| 字段 | 作用 |
|---|---|
| `model_provider` | 用哪个提供商，默认 `openai` |
| `openai_base_url` | 只改内置 `openai` 提供商的地址（代理、数据驻留） |
| `model_providers.<id>.*` | 自定义提供商：`base_url`、`env_key`、`wire_api` 等 |
| `chatgpt_base_url` | ChatGPT 登录流程用的地址 |
| `forced_login_method` | 只允许 `chatgpt` 或 `api` 登录 |
| `cli_auth_credentials_store` | 凭证存哪：`file`、`keyring`、`auto`、`ephemeral` |

内置提供商还有 `amazon-bedrock`（Amazon Bedrock）和 0.165.0 新增的 `gcp`（Google Cloud Vertex AI），见 [接入 Google Cloud](../12-官方工具与集成/13-Codex接入Google-Cloud-Model-Garden.md)、[接入 Amazon Bedrock](../12-官方工具与集成/16-Codex接入Amazon-Bedrock-登录向导与配置.md)；自定义提供商见 [model_providers 与 openai_base_url](../10-配置模型与权限安全/13-Codex自定义模型提供商-model_providers与openai_base_url.md)。

## 环境变量

官方 Environment variables 页列出的公开变量：

| 变量 | 作用 |
|---|---|
| `CODEX_HOME` | Codex 状态根目录，默认 `~/.codex`。**目录必须已存在** |
| `CODEX_SQLITE_HOME` | SQLite 状态库位置，默认同 `CODEX_HOME`；配置里的 `sqlite_home` 优先 |
| `CODEX_API_KEY` | 给非交互进程（exec、review、SDK）提供 API Key |
| `CODEX_ACCESS_TOKEN` | 给受信任的自动化提供 ChatGPT / Codex 访问令牌 |
| `OPENAI_FEDERATION_RULE_ID`、`OPENAI_IDENTITY_TOKEN_FILE`、`OPENAI_WORKLOAD_IDENTITY_CONTEXT` | 工作负载身份（Workload identity）认证 |
| `CODEX_CA_CERTIFICATE` | 公司网络做 TLS 拦截时用的 PEM 根证书，优先于 `SSL_CERT_FILE` |
| `SSL_CERT_FILE` | 没设 `CODEX_CA_CERTIFICATE` 时的备用证书路径 |
| `RUST_LOG` | 日志详细程度，如 `debug`、`codex_core=debug` |
| `CODEX_NON_INTERACTIVE` | 官方安装脚本跳过交互提问 |
| `CODEX_INSTALL_DIR` | 官方安装脚本把 `codex` 装到哪 |

`CODEX_HOME` 指向不存在的目录时，0.165.0 实测直接退出：

```text
Error: CODEX_HOME points to "/tmp/does-not-exist-xyz", but that path does not exist
```

自定义提供商的 API Key 变量名由 `env_key` 决定，不是固定的 Codex 变量。

## 一份能直接用的起步配置

下面这份在 0.165.0 上用 `codex exec --strict-config` 检查通过，没有未知字段：

```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
file_opener = "cursor"

[sandbox_workspace_write]
network_access = false

[history]
persistence = "save-all"

[tui]
notifications = true

# 不在下载目录里读 AGENTS.md 和项目配置（路径换成你自己的）
[projects."/Users/你的用户名/Downloads"]
trust_level = "untrusted"
```

启动后 `codex exec` 打印的摘要里能看到生效的值，例如：

```text
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: medium
```

注意 `approval: never`：`codex exec` 是非交互模式，不会弹审批，所以显示的是 never，不代表配置没生效。原因见 [config.toml 配置指南](https://codexguide.io/advanced/config-toml) 里「关于 exec 里的 approval」一节。

## 常见问题

**项目里的 `.codex/config.toml` 为什么没生效？**

项目没被信任。官方规定，只有信任的项目才加载项目级 `.codex/` 配置层。

**`[features]` 里能写哪些开关？**

运行 `codex features list` 看本机版本支持的全部开关、成熟度和当前值。没写的开关保持默认。

**Profile 还能写成 `[profiles.xxx]` 吗？**

新写法是单独一个 `~/.codex/<名字>.config.toml` 文件，里面直接写顶层字段，不要再嵌套在 `[profiles.<名字>]` 下。详见 [config.toml 配置指南](https://codexguide.io/advanced/config-toml)。

## 参考资料

- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables)
