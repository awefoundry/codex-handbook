---
id: codex-rules-prefix-rule
title: Codex Rules 怎么写：用 prefix_rule 设置命令白名单和黑名单，看懂 allow / prompt / forbidden，并用 codex execpolicy check 测试
seo_title: Codex Rules：prefix_rule 白名单／黑名单与 execpolicy check
description: Codex 在沙箱外跑命令时，可用 Rules 按前缀决定放行、询问或禁止。本文按官方实验文档讲清 default.rules、prefix_rule、冲突优先级、组合命令拆分，以及用 codex execpolicy check 自测与加载顺序。
lede: Rules 只管沙箱外的命令前缀。先分清它和沙箱／审批的边界，再写白名单与黑名单，并用 execpolicy check 自测。
url: /guides/codex-rules-prefix-rule
status: draft
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
client_validation_pending: true
official_ref: https://learn.chatgpt.com/docs/agent-configuration/rules
keywords: [Codex Rules, prefix_rule, default.rules, execpolicy, 命令白名单, allow prompt forbidden]
related: [permissions-sandbox-approvals, hooks-guide, advanced-config-toml]
howto: true
faq:
  - q: Rules 能不能代替沙箱或审批策略？
    a: 不能。官方写的是 Rules 控制「沙箱外能跑哪些命令」。沙箱管文件／网络边界，审批管越界要不要问人，Rules 再按命令前缀决定 allow／prompt／forbidden。三层要一起看，见权限沙箱与审批一文。
  - q: 为什么写了 allow git add，组合命令 git add . && rm -rf / 仍可能被拦？
    a: 当 bash -lc／-c（及 zsh／sh 等价）脚本只是普通单词用 &&、||、;、| 连接时，Codex 会拆成单条命令分别套规则，取最严结果。rm 单独命中 forbidden 时，整条不会因 git 被允许而放行。
  - q: codex exec 里怎样跳过用户和项目的 .rules？
    a: 非交互文档写明可用 --ignore-rules，在受控自动化环境跳过用户与项目的 execpolicy .rules。这是显式旁路，不要当成日常默认。
---

# Codex Rules 怎么写：用 prefix_rule 设置命令白名单和黑名单，看懂 allow / prompt / forbidden，并用 codex execpolicy check 测试

> 本文计划路径：[codexguide.io/guides/codex-rules-prefix-rule](https://codexguide.io/guides/codex-rules-prefix-rule)

> 核对依据：learn.chatgpt.com《Rules》（developers.openai.com 同页会 308 到该文档）、以及《Non-interactive mode》中的 `--ignore-rules`（2026-10-22 抓取）。**官方标明 Rules 为实验功能，接口与行为可能变化。** 文中「我的用法」是操作建议，不是官方强制规定。本机未在真实 Codex TUI 里点选允许列表或跑完整会话，`client_validation_pending: true`；规则形状与 `execpolicy check` 命令按官方文档编写。

Codex 要在沙箱**外**跑命令时，往往会停下来问你。若同一类只读命令每次都弹窗，或你想**硬性禁止**某些危险前缀，官方提供的机制就是 **Rules**：在配置层旁边的 `rules/` 目录里写 `.rules` 文件，用 `prefix_rule(...)` 按**命令参数前缀**决定 `allow`／`prompt`／`forbidden`。

这篇只讲命令规则这一层：它和沙箱、审批怎么分工；`default.rules` 怎么起手；字段与冲突优先级；组合命令何时拆开；怎样用 `codex execpolicy check` 自测；规则从哪几层加载；以及自动化里的 `--ignore-rules`、Smart approvals 建议规则怎么审。生命周期脚本（Hooks）见姊妹篇，不要和 Rules 混成一套。

## 1. Rules 管什么：和沙箱、审批的边界

先把三层分开（权限总览见《Codex 权限、沙箱与审批》）：

| 层 | 管什么 | 典型配置／界面 |
|---|---|---|
| **沙箱** | 文件、命令、网络在技术上能到哪里 | `sandbox_mode`／权限档案、桌面端 Ask／Full access 等 |
| **审批** | 越界时要不要问人、谁来审 | `approval_policy`、Auto-review／Approve for me |
| **Rules（本文）** | 沙箱**外**请求跑某条命令时，按前缀允许、再问一次、还是直接禁止 | `~/.codex/rules/*.rules` 等 |

官方 Rules 页开宗明义：*Control which commands Codex can run outside the sandbox*。因此：

- 命令仍在沙箱内、本来就不需要提权时，Rules **不是**你日常调的那一层。
- Rules **不会**扩大可写根目录、也不会打开网络；它只影响「已经要出沙箱跑的那条命令」怎么裁决。
- Hooks（`PreToolUse` 等）是生命周期护栏，和前缀白名单／黑名单是另一套机制；需要脚本拦截时看 Hooks 文。

**实验状态：** 官方写明 *Rules are experimental and may change.* 企业／Work Cloud 还有托管侧的 `rules` TOML 与容器策略；本文以本机 Codex 的 `.rules` 文件为主，托管细则不展开。

## 2. 第一条规则：在 `~/.codex/rules/default.rules` 里写 `prefix_rule`

### 放哪里

1. 在**某个已生效的配置层旁边**建 `rules/` 目录，放入 `.rules` 文件。个人最常见的是：

   `~/.codex/rules/default.rules`

   （若设置了 `CODEX_HOME`，则相对该目录，而不是字面量 `~/.codex`。）

2. 写入至少一条 `prefix_rule(...)`。
3. **重启 Codex** 后规则才会在启动扫描时加载。

Codex 启动时会扫描**每个活动配置层**下的 `rules/`，包括 Team Config，以及用户层 `~/.codex/rules/`。仓库内 `<repo>/.codex/rules/` **仅在项目 `.codex/` 层被信任时**加载。

在 TUI 里把某条命令加入允许列表时，官方说明会写入用户层的 `~/.codex/rules/default.rules`，以便以后跳过同类提示。

### 官方示例（询问后再跑 `gh pr view`）

下面直接按官方文档形状抄录，便于对照字段：

```python
# Prompt before running commands with the prefix `gh pr view` outside the sandbox.
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "Viewing PRs is allowed with approval",
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
        "gh pr view 7888 --json title,body,comments",
    ],
    not_match = [
        # Does not match because the `pattern` must be an exact prefix.
        "gh pr --repo openai/codex view 7888",
    ],
)
```

要点：`pattern` 必须是**精确前缀**。`gh pr --repo … view …` 不会匹配 `["gh","pr","view"]`，因为第 3 个参数不是 `view`。

`.rules` 语法是 **Starlark**（像 Python，但设计为无副作用、可安全求值）。文件里不要指望去读写磁盘或调网络——引擎不会当普通脚本跑。

## 3. 字段详解：`pattern`、`decision`、`justification`、`match`／`not_match`

| 字段 | 是否必填 | 含义 |
|---|---|---|
| `pattern` | 必填 | 非空列表，定义命令前缀。每一项是**字面量**（如 `"pr"`），或**字面量联合**（如 `["view","list"]`）匹配该参数位上的多选一。 |
| `decision` | 可选，默认 `"allow"` | 命中后的动作：`allow`／`prompt`／`forbidden`（见下一节）。 |
| `justification` | 可选 | 非空的人读说明；可能出现在审批提示或拒绝文案里。`forbidden` 时，官方建议在合适处写上推荐替代（例如改用 `rg` 而不是 `grep`）。 |
| `match`／`not_match` | 可选，默认 `[]` | **加载时**由 Codex 校验的正／反例，相当于规则的内联单元测试，用来在规则生效前抓写错的前缀。 |

匹配时，Codex 把待执行命令看成参数列表（类似 `execvp(3)` 收到的 argv），再与 `pattern` 比前缀。

**我的用法：** 每条规则都写 `match`／`not_match`，尤其是带联合字面量或多层子命令的前缀；比事后在真实任务里猜「为什么没命中」便宜。

## 4. 多条规则冲突时：`forbidden` > `prompt` > `allow`

官方明确：多条规则同时命中时，取**最严格**的决定：

**`forbidden` > `prompt` > `allow`**

三种决定的语义：

| decision | 行为 |
|---|---|
| `allow` | 在沙箱外直接跑，不再为这条前缀弹窗 |
| `prompt` | 每次匹配调用前都询问 |
| `forbidden` | 直接拦截，不询问 |

因此：用户层写了很宽的 `allow`，项目层或 `requirements.toml` 里若有更严的 `forbidden`／`prompt`，仍以更严者为准（管理员侧强制限制性 `prefix_rule` 的入口，官方点名了 `requirements.toml`）。

不要假设「后写的覆盖先写的」或「项目层总是赢」——裁决键是**决定的严格度**，不是文件名排序玄学。

## 5. 组合命令怎么判断：哪些 `bash -lc` 会拆开

工具常把多条 shell 命令塞进一次调用，例如：

```text
["bash", "-lc", "git add . && rm -rf /"]
```

Codex 对 `bash -lc`、`bash -c`，以及对应的 `zsh`／`sh` 写法做了特殊处理。

### 会拆开的情况

脚本是**线性串联**，且只含：

- 普通单词（无变量展开、无 `VAR=...`、无 `$FOO`、无 `*` 等）
- 用安全连接符接合：`&&`、`||`、`;`、`|`

则 Codex 用 tree-sitter 解析后**拆成单条命令**再分别套规则。上例会变成：

- `["git", "add", "."]`
- `["rm", "-rf", "/"]`

再对每条取最严结果。即便你 `allow` 了 `pattern = ["git", "add"]`，也**不会**因此放行整条 `git add . && rm -rf /`——`rm` 仍单独裁决。官方强调：这是为了防止危险命令夹带在安全前缀后面。

### 不拆开的情况

出现更复杂的 shell 特性时，**整段**当作一次调用匹配规则：

- 重定向：`>`、`>>`、`<`
- 替换：`$(...)`、反引号
- 环境变量：`FOO=bar`
- 通配：`*`、`?`
- 控制流：`if`、`for`，以及带赋值的 `&&` 等

此时 argv 形如 `["bash", "-lc", "<完整脚本>"]`，你的 `prefix_rule` 是在匹配这一整包，而不是包内每一段。

**我的用法：** 白名单尽量写在「拆得开的只读前缀」上；对带重定向／替换的长脚本，宁可 `prompt`，也不要给超宽的 `allow ["bash","-lc"]`。

社区里有 Windows／PowerShell 与 execpolicy 误判相关的讨论（例如 openai/codex#40060）。本篇未在 Windows 上复现；若你在 PowerShell 包装脚本上看到异常放行或误拦，先用下一节的 `execpolicy check` 对**实际 argv** 做对照，再查 issue，不要把评论里的临时绕过写成团队基线。

## 6. 测试规则：`codex execpolicy check`

改完 `.rules` 后，用官方自带的检查命令看裁决，而不要先赌真实会话：

```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body,comments
```

行为要点（官方）：

- 输出 JSON：含**最严决定**、命中的规则，以及规则上的 `justification`（若有）
- 可多次传 `--rules` 合并多个文件
- `--pretty` 便于阅读

**我的用法：** 把 `match`／`not_match` 里的例子，以及你真正担心的组合命令（含 `bash -lc '…&&…'`），都拿去跑一遍；把 JSON 里的 decision 记进 PR／变更说明。本机预览未附着真实 CLI 输出截图；上线前请在你的 Codex 版本上自行跑通同一命令。

## 7. 规则从哪里加载：用户层、项目层、团队与 `requirements.toml`

汇总官方加载说明：

| 来源 | 何时生效 |
|---|---|
| 用户层 `~/.codex/rules/`（含 TUI 写入的 `default.rules`） | 启动扫描活动配置层时加载 |
| 项目 `<repo>/.codex/rules/` | **仅当**项目 `.codex/` 层受信任 |
| Team Config 等活动配置层旁的 `rules/` | 随该层一起扫描 |
| 管理员 `requirements.toml` 中的限制性 `prefix_rule` | 强制收紧（企业策略） |
| Work Cloud／托管 `rules` TOML | 作用于本地执行器等托管路径；**不要假设** Local computer access with Work Cloud 会读你本机 `.rules` 文件 |

配置层、信任与 `CODEX_HOME` 的更完整图景，见《Codex config.toml 深入配置》。Rules 文件跟在「活动配置层」旁边，而不是写进 `config.toml` 正文里的普通键（托管 Work 另有 TOML 字段，与本机 `.rules` 文件是不同入口）。

## 8. 常用规则示例：放行只读 git／gh，拦截破坏性 `rm`，引导 `grep` → `rg`

以下示例用于**教育向的最小白名单／黑名单**，请按仓库收紧；不要复制成「允许一切 git／gh」的万能文件。破坏性命令以**禁止前缀**说明机制，不是攻击教材。

```python
# 只读 git：status / log / diff / show（按需增删子命令）
prefix_rule(
    pattern = ["git", ["status", "log", "diff", "show"]],
    decision = "allow",
    justification = "Read-only git inspection outside the sandbox",
    match = [
        "git status",
        "git log -1 --oneline",
        "git diff HEAD",
        "git show HEAD:README.md",
    ],
    not_match = [
        "git push origin main",
        "git reset --hard",
    ],
)

# 只读 gh：查看 PR／issue（仍建议先 prompt，确认稳定后再改 allow）
prefix_rule(
    pattern = ["gh", ["pr", "issue"], ["view", "list"]],
    decision = "prompt",
    justification = "GitHub read APIs require explicit approval until trusted",
    match = [
        "gh pr view 7888",
        "gh pr list --limit 10",
        "gh issue view 12",
    ],
    not_match = [
        "gh pr create",
        "gh pr merge 7888",
    ],
)

# 禁止常见破坏性删除前缀（示例；按团队政策调整）
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "Destructive recursive delete is blocked; remove files intentionally outside Codex or with a narrower command",
    match = [
        "rm -rf build",
        "rm -rf /tmp/cache",
    ],
    not_match = [
        "rm build/output.o",
    ],
)

# 引导用 rg 替代 grep（官方 justification 示例同思路）
prefix_rule(
    pattern = ["grep"],
    decision = "forbidden",
    justification = "Use `rg` instead of `grep`.",
    match = [
        "grep -R TODO .",
    ],
    not_match = [
        "rg TODO",
    ],
)
```

写入后重启 Codex，并用 §6 的 `execpolicy check` 分别测 `git status`、`gh pr view 1`、`rm -rf build`、`bash -lc 'git status && rm -rf build'`。最后一条应体现「拆分后取最严」：只读 git 被允许，也不应带过 `rm -rf`。

## 9. 自动化里的 `--ignore-rules`，以及 Smart approvals 建议怎么审

### `codex exec` 与 `--ignore-rules`

非交互模式文档写明：在受控自动化环境中，可用 `--ignore-rules` **跳过用户和项目的 execpolicy `.rules` 文件**；另有 `--ignore-user-config` 跳过 `$CODEX_HOME/config.toml`。两者都是为流水线准备的显式旁路，不是日常交互的默认开关。

CI 里若既要用团队强制规则，又要可重复构建，优先让托管／`requirements.toml` 表达硬限制，而不是在开发者笔记本上依赖「偶尔 ignore」。自动化与 CI 的沙箱参数、API Key 写法见《Codex 自动化与 CI》更新文。

### Smart approvals 建议的 `prefix_rule`

官方：Smart approvals **默认开启**时，Codex 可能在提权请求中**提议**一条 `prefix_rule`。接受前务必看清：

- 前缀是否过宽（例如只该允许 `gh pr view`，却建议了整个 `gh`）
- 是否把写操作、推送、删除和只读前缀捆在一起
- `justification` 是否和你真实意图一致

TUI「加入允许列表」写入 `default.rules` 同样要审：文件会留在用户层，影响之后所有会话。

## 边界小结

- Rules = 控制**沙箱外**命令的前缀裁决；实验功能，可能变更。  
- 文件：配置层旁 `rules/*.rules`；个人常用 `~/.codex/rules/default.rules`；改完重启。  
- 字段：`pattern`（可联合字面量）、`decision`、`justification`、`match`／`not_match`。  
- 冲突：`forbidden` > `prompt` > `allow`。  
- `bash`／`zsh`／`sh` 的 `-lc`／`-c`：简单 `&&`／`||`／`;`／`|` 链可拆开逐条裁决；重定向／替换／变量／通配／控制流则整包匹配。  
- 自测：`codex execpolicy check --pretty --rules … -- <命令>`。  
- 加载：用户层；项目层需信任；Team／`requirements.toml` 可强制收紧。  
- 自动化：`--ignore-rules` 显式跳过用户／项目 `.rules`；Smart approvals 建议的前缀要人工审。  
- 与沙箱／审批／Hooks 分工清楚，不要互相替代。

参考：

- [Rules（learn.chatgpt.com）](https://learn.chatgpt.com/docs/agent-configuration/rules)  
- [Non-interactive mode（`--ignore-rules`）](https://learn.chatgpt.com/docs/non-interactive-mode)  
- 姊妹篇：[Codex 权限、沙箱与审批](https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi)（`permissions-sandbox-approvals`）、[Codex Hooks 入门](https://codexguide.io/guides/codex-hooks-guide)（`hooks-guide`）、[Codex config.toml 深入配置](https://codexguide.io/advanced/config-toml)（`advanced-config-toml`）

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
