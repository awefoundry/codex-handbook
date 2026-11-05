---
id: hooks-guide
title: Codex Hooks 入门：hooks.json 放在哪、怎么用 /hooks 信任，以及拦截危险命令、回合结束自动检查的写法
seo_title: Codex Hooks 入门：hooks.json、/hooks 信任、PreToolUse 与 Stop
description: Codex Hooks 能在会话开始、命令执行前后、回合结束时自动跑你的脚本。本文讲清 hooks.json 放哪、为何要先在 /hooks 里信任，并给出拦截危险命令与回合结束检查两个可复制例子，以及超时、关闭与常见坑。
lede: Hooks 是生命周期护栏，不是完整安全边界。先放对文件、在 /hooks 里信任，再写 PreToolUse 与 Stop。
url: /guides/codex-hooks-guide
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/hooks
keywords: [Codex Hooks, hooks.json, PreToolUse, Stop hook, /hooks, Codex 生命周期钩子]
related: [plugin-development-marketplace, create-codex-skill]
howto: true
faq:
  - q: 写了 hooks.json 为什么完全不跑？
    a: 先看三件事：1）非托管 hook 是否已在 /hooks 里按当前内容哈希信任；2）项目级 .codex/ 是否仅在项目受信任时加载；3）config.toml 里是否写了 [features] hooks = false。改过 hook 定义后哈希会变，要重新信任。
  - q: timeout 不写是多少秒？
    a: 多数 hook 省略 timeout 时默认 600 秒。SessionEnd 与 Interrupt 默认 1 秒，且最多只能配到 3 秒。
  - q: 插件装上后 hooks 会自动生效吗？
    a: 不会。插件自带 hooks 与用户／项目 hooks 一样，要走审核与信任；安装或启用插件不会自动信任当前 hook 定义。
---

# Codex Hooks 入门：hooks.json 放在哪、怎么用 /hooks 信任，以及拦截危险命令、回合结束自动检查的写法

> 本文在线版：[codexguide.io/guides/codex-hooks-guide](https://codexguide.io/guides/codex-hooks-guide)

> 核对依据：learn.chatgpt.com／developers.openai.com 的 Hooks 文档（2026-10-22 抓取）。文中「我的用法」是操作建议，不是官方规定。社区 issue 只作已知坑对照，不附带未证实的修复步骤。本机未跑通真实 Codex hook 脚本。

你已经会让 Codex 改文件、跑命令。接下来常会想：**危险命令在执行前拦一下**，或**这一回合停下来时自动再跑测试／格式检查**。官方给的扩展点就是 **Hooks**：在智能体循环的固定时机，跑你指定的命令脚本，或调用已连接的 MCP 工具。

这篇按官方 Hooks 页组织：先讲它能做什么、不能代替什么；再讲配置放哪、怎么信任；然后给两个能直接抄的形状（`PreToolUse` 拦截、`Stop` 续跑检查）；最后写超时、关闭、插件与社区常见坑。

## Hooks 能做什么（以及不能代替什么）

官方列出的典型用途包括：

1. 把对话送到自定义日志／分析
2. 扫描团队提示词，挡住误贴的 API Key
3. 汇总对话，辅助持久记忆
4. 在回合停止时跑自定义校验，落实团队标准
5. 在特定目录下定制提示上下文

运行规则（官方原文要点）：

- **多个来源里匹配到的 hooks 都会跑**；高层配置**不会**覆盖／替换低层已加载的 hooks。
- 同一事件上多个匹配的 **command** hook **并发启动**，一个 hook 拦不住另一个开始跑。
- **非托管** hooks 必须先审核并信任，才会执行。

**不能代替什么（务必读）：**

官方在工具覆盖一节写明：把 tool hooks 当作**有用的护栏（guardrail）**，**不是完整的强制执行边界（not a complete enforcement boundary）**。部分专用工具路径可以退出默认 hook 通路；托管工具如 `WebSearch` **不走**本地 function-tool 的 hook 路径。`PostToolUse` 也**不能撤销**已经发生的副作用。

换句话说：Hooks 适合「多一道检查、多一句上下文、拦常见危险命令」；不要当成合规审计或主机级安全产品。

## 事件一览：何时触发、谁认 matcher

| 时机 | 事件 |
|---|---|
| 回合进行中 | `PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、`PostCompact`、`UserPromptSubmit`、`SubagentStop`、`Stop` |
| 你打断正在进行的回合 | `Interrupt`（不对 subagent 跑） |
| 会话或 subagent 开始 | `SessionStart`、`SubagentStart` |
| 主线程结束 | `SessionEnd`（不对 subagent 跑） |

`matcher` 是正则。写成 `"*"`、`""`，或**省略** `matcher`，表示该事件每次都匹配。

| 事件 | matcher 过滤什么 | 备注 |
|---|---|---|
| `PreToolUse`／`PostToolUse`／`PermissionRequest` | 工具名 | 含 `Bash`、`apply_patch`（也可用 `Edit`／`Write`）、MCP 名如 `mcp__filesystem__read_file` |
| `SessionStart` | 启动来源 | `startup`／`resume`／`clear`／`compact`／`fork` |
| `SessionEnd` | 结束原因 | 目前实际只有 `other` |
| `PreCompact`／`PostCompact` | 压缩触发 | `manual`／`auto` |
| `SubagentStart`／`SubagentStop` | subagent 类型 | 取决于实际启动的子代理 |
| `UserPromptSubmit`／`Stop`／`Interrupt` | **不支持** | 配了 matcher 也会被忽略 |

`PreToolUse`／`PostToolUse` 覆盖：Shell（匹配名 `Bash`）、unified exec（`exec_command`，匹配仍为 `Bash`）、`apply_patch`、MCP、其他本地 function tools（如 `update_plan`；`spawn_agent` 也可匹配 `Agent`）。**不含** `WebSearch` 一类托管工具。

## 放在哪：用户级、项目级、内联 TOML

Codex 在**当前生效的配置层旁边**找 hooks，形式可以是：

- `hooks.json`
- `config.toml` 里的内联 `[hooks]`／`[[hooks.…]]`

日常最有用的四个位置：

| 位置 | 作用域 |
|---|---|
| `~/.codex/hooks.json` | 用户级，本机通用 |
| `~/.codex/config.toml` | 用户级内联 |
| `<repo>/.codex/hooks.json` | 项目级 |
| `<repo>/.codex/config.toml` | 项目级内联 |

要点：

1. **多来源同时存在时全部加载匹配项**；不是「只留优先级最高的一份」。
2. **同一层**若既有 `hooks.json` 又有内联 `[hooks]`，Codex 会合并并在启动时警告。**每层只保留一种写法更干净。**
3. **项目级 hooks 只在项目 `.codex/` 层受信任时加载**。未信任项目里，仍会加载用户／系统层 hooks。
4. 已启用插件也可以自带 hooks（见后文）；信任流程与其他非托管 hooks 相同。

配置分三层：事件名 → matcher 组 → 一个或多个 handler。handler 支持 `type: "command"` 与 `type: "mcp_tool"`；`prompt`／`agent` 会被解析但**跳过不跑**。命令的工作目录是会话的 `cwd`。仓库内脚本**优先用 git 根解析绝对路径**（官方示例用 `$(git rev-parse --show-toplevel)`），不要写死相对路径 `.codex/hooks/...`——你可能从子目录启动 Codex。

最小用户级骨架：

```json
{
  "description": "Optional lifecycle hooks for this workspace.",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/pre_tool_use_policy.py",
            "statusMessage": "Checking Bash command",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

等价内联 TOML 片段形状（字段名可用 `command_windows`／`commandWindows`）：

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = 'python3 ~/.codex/hooks/pre_tool_use_policy.py'
timeout = 30
statusMessage = "Checking Bash command"
```

## 第一次运行前：用 `/hooks` 审核与信任

非托管 hook **不会**因为文件存在就自动跑。官方流程：

1. Codex 列出已配置 hooks，再决定哪些能跑。
2. 你必须**审核并信任当前这条 hook 定义**。
3. 信任按 hook **当前内容的哈希**记录；**新建或改过**的 hook 会标成待审，**跳过直到再次信任**。

在 CLI 里用 **`/hooks`**：查看来源、审阅新增／变更、信任，或禁用个别非托管 hook。启动时若有待审，会提示你打开 `/hooks`。

系统／MDM／云／`requirements.toml` 等来源的 **managed** hooks 按策略视为已信任，且不能在用户 hook 浏览器里关掉。

一次性自动化、且你已在 Codex 外审核过来源时，可用：

```bash
codex … --dangerously-bypass-hook-trust
```

这会在**本次调用**跳过「必须已持久化信任」的要求。日常交互仍应走 `/hooks` 信任，而不是默认绕过。

**我的用法：** 项目 hooks 提交进仓库没问题，但每位同事 clone 后仍要自己在 `/hooks` 里审一遍；改脚本或改 `command` 字符串后哈希会变，记得再信任一次。

## 例子一：PreToolUse 拦截危险 Bash

目标：在 Shell 真正执行前读 stdin 里的 JSON，若命令像破坏性操作就拒绝。

`hooks.json`（项目级示例，路径经 git 根解析）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

`.codex/hooks/pre_tool_use_policy.py`（形状按官方字段；按团队规则改黑名单）：

```python
#!/usr/bin/env python3
import json
import re
import sys

event = json.load(sys.stdin)
cmd = ""
tool_input = event.get("tool_input") or {}
if isinstance(tool_input, dict):
    cmd = str(tool_input.get("command") or "")

# 示例：拦常见破坏性模式（请按仓库收紧／放宽）
blocked = re.compile(
    r"(?:rm\s+-rf\s+/|git\s+push\s+--force|mkfs\.|dd\s+if=)",
    re.I,
)

if blocked.search(cmd):
    # 推荐写法
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Destructive command blocked by hook.",
        }
    }
    print(json.dumps(out))
    sys.exit(0)

    # 等价旧写法：{"decision": "block", "reason": "..."}
    # 或：exit 2，并把原因写到 stderr

sys.exit(0)  # 无输出 = 成功并继续
```

输入侧你会常用到：`session_id`、`cwd`、`hook_event_name`、`model`、以及 `tool_name`／`tool_input`（Bash／`apply_patch` 的命令在 `tool_input.command`）。

拦截方式官方认可三种：

1. `permissionDecision: "deny"`（上例）
2. 旧形状 `decision: "block"` + `reason`
3. **退出码 `2`**，原因写在 **stderr**

还可以在不拦截时返回 `additionalContext`，或 `permissionDecision: "allow"` + `updatedInput` 改写命令（Bash／`apply_patch` 的 `updatedInput` 必须含字符串字段 `command`）。`permissionDecision: "ask"`、`continue: false` 等在 `PreToolUse` 上**尚未支持**；返回它们会令该次 hook 记为失败，**工具调用仍会继续**——不要用「失败」当拦截。

若要拦文件编辑，matcher 可用 `apply_patch`、`Edit` 或 `Write`（输入里的 `tool_name` 仍是 `"apply_patch"`）。

## 例子二：Stop 在回合结束时再检查一轮

`Stop` 在主回合将停时触发；**matcher 无效**。退出 `0` 时 stdout **必须是 JSON**（纯文本对该事件无效）。

官方语义要点：`decision: "block"` **不是**拒绝这一回合，而是让 Codex **继续**，并用你的 `reason` 自动生成一条相当于新用户提示的续跑提示。任意匹配的 `Stop` 若返回 `continue: false`，优先于其他 hook 的「继续」决定。

`hooks.json`：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/stop_continue.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

`stop_continue.py`（示意：测失败则续跑；测通过则静默结束）：

```python
#!/usr/bin/env python3
import json
import subprocess
import sys

event = json.load(sys.stdin)
# 已由 Stop 续跑过时，stop_hook_active 为 true——避免死循环
if event.get("stop_hook_active"):
    sys.exit(0)

proc = subprocess.run(
    ["npm", "test", "--silent"],
    cwd=event.get("cwd") or ".",
    capture_output=True,
    text=True,
)
if proc.returncode == 0:
    sys.exit(0)

print(
    json.dumps(
        {
            "decision": "block",
            "reason": "Tests failed. Fix failing tests, then stop again.",
        }
    )
)
sys.exit(0)
# 也可用 exit 2 + stderr 写续跑原因
```

**PostToolUse 补充：** 匹配 `Edit|Write`（或 `apply_patch`）可在改文件后给模型追加 `additionalContext`。`decision: "block"` **不会撤销**已发生的编辑；它会用 hook 反馈替换工具结果并让模型从该反馈继续。同样可用退出码 `2`。

## MCP tool hooks、插件 hooks，以及第三方安装例

### MCP tool hooks

`type: "mcp_tool"` 在生命周期事件里调用**已经连上**的 MCP 服务器工具（不会替你启动／重连服务器）。与 command hook 共用信任与输出约定。错误、缺服务器、工具不可用**不会**因此拦截操作；只有工具返回明确的拦截决策才会拦。`SessionEnd` **不支持** MCP tool hooks。`timeout` 省略时同样默认 **600** 秒。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "scanner",
            "tool": "scan_patch",
            "input": { "patch": "${tool_input.command}" },
            "timeout": 30,
            "statusMessage": "Scanning edited files"
          }
        ]
      }
    ]
  }
}
```

`${field.nested}` 从事件里展开参数；单独占满一个值时保留 JSON 类型。

### 插件自带 hooks

默认找插件根下的 `hooks/hooks.json`；也可在 `.codex-plugin/plugin.json` 用 `hooks` 覆盖（`./` 相对路径、路径数组、或内联对象／数组）。路径必须落在插件根内。插件命令会拿到 `PLUGIN_ROOT`／`PLUGIN_DATA`（以及兼容用的 `CLAUDE_PLUGIN_ROOT`／`CLAUDE_PLUGIN_DATA`）。

**安装或启用插件 ≠ 信任 hooks。** 未审过的插件 hooks 会被跳过。

### 第三方工具怎么装 hooks（Sphinx，仅作安装例）

社区工具有时会往你的 Codex 配置里写入 lifecycle hooks（例如 HN 上讨论过的 Sphinx：在 push 前用测验检查你是否理解 AI 写的代码）。无论来源如何，装完后仍应打开 **`/hooks`**，逐条看清 `command`／`mcp_tool`，再决定是否信任。**本文不推荐具体产品**；只强调：第三方写入的 hooks 与手写 hooks 走同一套信任门闩。

## 超时、关闭，以及已知坑

### 超时默认值

| 情况 | 默认／上限 |
|---|---|
| 多数 hook 省略 `timeout` | **600 秒** |
| `SessionEnd`、`Interrupt` | 默认 **1** 秒，最多 **3** 秒 |
| `async: true` 的 command hook | 仍按秒计时；多数默认 600；`Interrupt` 仍 1～3 秒 |
| 背景 hook 并发 | 每会话最多 **8** 个并发；`SessionEnd` **始终同步** |

需要拦工具／改权限／挡提示／决定是否续跑时，用**同步** hook；`async: true` 只能做事后信息，**不能**控制触发它的那次操作。

### 整机关闭

Hooks 默认开启。在 `config.toml`：

```toml
[features]
hooks = false
```

特性键用 **`hooks`**；`codex_hooks` 仍是已弃用别名。管理员可在 `requirements.toml` 同样关掉，或配合 `allow_managed_hooks_only = true` 等企业策略（细节见官方 Managed hooks 节）。

### 社区已知坑（只列症状与链接，不编修复）

写作时（选题核对）仍 open、适合写进排障意识的 issue：

| Issue | 症状摘要 |
|---|---|
| [openai/codex#21639](https://github.com/openai/codex/issues/21639) | 桌面端更新后 hooks 似乎不跑；多份报告呈「CLI／部分路径有、Desktop／app-server 路径无」的对照 |
| [openai/codex#48500](https://github.com/openai/codex/issues/48500) | app-server 用第一个客户端的 TMUX 相关变量跑 hooks（回归类报告） |
| [openai/codex#16430](https://github.com/openai/codex/issues/16430) | 插件自带 hooks：文档描述与实际行为不一致 |

若你遇到「配置对、也信任了、CLI 能触发但桌面端没有」，先对照 `/hooks` 状态与上述讨论，再决定是否升级／回退客户端；**不要把 issue 评论里的临时绕过当成官方方案。**

排障短清单：

1. `/hooks` 是否显示 trusted，且改文件后是否重新信任  
2. 项目是否 trusted（项目级 `.codex/`）  
3. `[features].hooks` 是否被关掉  
4. matcher 是否匹配实际工具名（Desktop 路径上工具名可能与 CLI 的 `Bash` 观感不同——以会话实际工具名为准）  
5. `PreToolUse` 是否误用了尚不支持的字段导致「hook 失败但工具仍继续」

## 边界小结

- Hooks = 生命周期上的 **command／mcp_tool** 扩展点；多来源叠加、同事件 command 并发。  
- 配置：`~/.codex/hooks.json`、仓库 `.codex/hooks.json`、或 `config.toml` 内联；项目层要项目信任。  
- 非托管必须先 **`/hooks` 按内容哈希信任**；改过要重审。  
- 拦截：`PreToolUse` 用 `permissionDecision: "deny"`（或旧 `decision: "block"`／退出码 2）。  
- 回合结束检查：`Stop` 用 `decision: "block"` **续跑**，不是否决整轮。  
- 默认超时多数 **600s**；`SessionEnd`／`Interrupt` 默认 1s（上限 3s）。  
- 关闭：`[features] hooks = false`。  
- **护栏 ≠ 完整安全边界**；不要替代沙箱、审批与主机策略。

参考：

- [Hooks（learn.chatgpt.com）](https://learn.chatgpt.com/docs/hooks)  
- [Hooks（developers.openai.com/codex/hooks）](https://developers.openai.com/codex/hooks)  
- 姊妹篇计划：[Codex 插件开发入门](https://codexguide.io/guides/codex-plugin-development-marketplace)（`plugin-development-marketplace`）、[从零创建 Codex Skill](https://codexguide.io/guides/create-codex-skill)（`create-codex-skill`）

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
