---
id: codex-capture-reusable-content
title: Codex 任务结束时捕捉可复用素材：用 AGENTS.md 规则和 Stop Hook 生成素材候选
seo_title: Codex 任务结束时捕捉素材：AGENTS.md 规则与 Stop Hook
description: 任务刚结束时，步骤、卡点和取舍都还在上下文里。本文给出一条可直接复制的 AGENTS.md 规则，让 Codex 只在有可复用经验时输出素材候选；再用一个 Stop Hook 在任务结束时自动提醒，并说明它和 Memories 的区别、怎么验证。
url: /guides/codex-capture-reusable-content
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 1
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-17
date_modified: 2026-10-26
verified_on: 2026-10-26
tested_cli_version: 0.164.0
official_ref: https://learn.chatgpt.com/docs/hooks
keywords: [Codex AGENTS.md 规则, Codex Stop Hook, Codex hooks, Codex 素材整理, Codex 任务复盘, Codex Memories]
howto: true
faq:
  - q: 只写 AGENTS.md 规则够不够？
    a: 大多数情况够用。AGENTS.md 会在每次任务开始前被读入，规则写清楚触发条件，Codex 就会在收尾时判断。只有发现它经常忘记做这一步时，再加 Stop Hook 兜底。
  - q: Stop Hook 会不会让 Codex 一直停不下来？
    a: 官方文档提供了 stop_hook_active 字段，表示这一轮是否已经被 Stop Hook 续跑过。本文的脚本遇到 true 就直接放行，最多只多跑一轮。
  - q: 这和 Codex Memories 有什么区别？
    a: Memories 是 Codex 自动在后台记住的偏好和经验，默认关闭，用于以后的对话召回；素材候选是任务结束时给你看的结构化记录，由你决定要不要保存和使用。官方建议必须遵守的规则写在 AGENTS.md，不要依赖 Memories。
  - q: 项目里的 Hook 为什么没生效？
    a: 非托管的 Hook 要先在 CLI 里用 /hooks 审核并信任才会运行；项目级 Hook 还要求这个项目的 .codex 目录被信任。Hook 内容改动后需要重新审核。
---

# Codex 任务结束时捕捉可复用素材：用 AGENTS.md 规则和 Stop Hook 生成素材候选

> 本文在线版：[codexguide.io/guides/codex-capture-reusable-content](https://codexguide.io/guides/codex-capture-reusable-content)

> 核对依据：OpenAI 官方文档 [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[Hooks](https://learn.chatgpt.com/docs/hooks) 和 [Memories](https://learn.chatgpt.com/docs/customization/memories)。文中的 Stop Hook 脚本在 Python 3.13.5 下用模拟的 Hook 输入逐个测试过 5 种情况；测试机上的 Codex（CLI 0.164.0）没有登录，所以**没有在真实 Codex 对话里跑过这个 Hook**，接入前请按文末步骤自己验证一次。核对日期 2026-10-26。本次改写删除了旧版的两张示意图，补充了规则放置范围、Stop Hook 和 Memories 的区别。

一个任务刚结束时，操作步骤、失败原因和取舍都还在当前上下文里。等几天后再整理，很多细节就要重新查。可以给 Codex 加一条任务结束规则，只在确实出现可复用经验时生成“素材候选”。

这条规则适合经常用 Codex 做项目维护、工具接入和流程改进的人。它只负责记录线索，不自动发布内容，也不把私密配置写进素材库。

## 哪些任务值得记录

触发条件要具体。否则 Codex 每次简单问答后都来提醒，几天后这条规则就成了干扰。

适合记录的：

- 一条跑通的工具接入流程
- 经过验证的配置取舍
- 有复现步骤的故障处理
- 可以重复执行的发布或检查方法

可以直接跳过的：

- 纯聊天和简单问答
- 没有稳定复现方式的偶发故障
- 只对当前临时环境有效的处理
- 包含账号凭据、客户数据或内部地址，且无法可靠脱敏的内容
- 赶时间结束、你已经明确说不需要额外整理的任务

## 第一步：把规则写进 AGENTS.md

Codex 每次开始工作前都会读 `AGENTS.md`。官方文档说明的读取顺序是：

- **全局**：Codex 主目录（默认 `~/.codex`）下的 `AGENTS.override.md`，没有就读 `AGENTS.md`。
- **项目**：从项目根目录一路往下到当前工作目录，每一层的 `AGENTS.override.md` 或 `AGENTS.md`。离当前目录越近的文件越晚读入，内容会覆盖前面的规则。
- 文件按从根目录到当前目录的顺序拼接；合计大小达到上限（`project_doc_max_bytes`，默认 32 KiB）后，后面的文件不再加入。

放哪里：

- 只服务一个仓库的规则，写在项目根目录的 `AGENTS.md`。
- 多个项目都要用，写在全局的 `~/.codex/AGENTS.md`，再让具体项目用更近的规则覆盖。
- 项目规则会随仓库共享。个人内容规划、私有素材路径和账号信息不要提交到公共仓库，放在全局规则里更合适。

`AGENTS.md` 的完整写法和继承关系见 [AGENTS.md 怎么写](../10-配置模型与权限安全/09-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。

### 可以直接复制的规则

```markdown
## 任务结束时捕捉可复用素材

完成主要任务后，检查本次工作是否产生了可复用经验。

满足下列任一条件时，输出一个“素材候选”小节：

- 跑通了可以重复执行的工具接入或自动化流程。
- 找到并验证了一个不明显的故障原因和修复方法。
- 形成了有依据的配置、安全或发布取舍。
- 产出了可公开复用的命令、检查清单或操作顺序。

纯聊天、简单问答、机械性修改和没有复现证据的猜测不触发。

素材候选包含任务场景、实际操作、遇到的卡点、解决方法、
可复用结论和证据路径。不得写入密钥、个人信息、客户数据、
内部域名或未经确认的结论。

只生成候选内容。写入素材文件或发布前先取得用户确认。
```

规则里的“完成主要任务后”很重要：素材整理不能打断原任务，也不能把还没验证的中间结果写成经验。

## 第二步：固定素材候选的格式

格式固定，方便以后筛选，也能避免同一件事被写成好几条空泛总结。

```markdown
素材候选

- 任务场景
- 实际操作
- 卡点与原因
- 解决方法
- 可复用结论
- 证据路径或公开来源
- 需要删除或脱敏的信息
```

证据路径可以是改动的文件、测试命令、公开文档链接或错误日志位置。它是给以后核对用的，不代表这些内部路径可以直接公开。

## 第三步（可选）：用 Stop Hook 在结束时提醒

规则写在 `AGENTS.md` 里，Codex 大多数时候会照做。但任务很长时，它可能在收尾时忘了这一步。这时可以加一个 **Stop Hook**：每轮回复结束时运行一段脚本，判断要不要让 Codex 再做一次检查。

官方文档对 `Stop` 事件的说明：

- Hook 脚本从标准输入收到一个 JSON，除了通用字段（`session_id`、`cwd`、`hook_event_name`、`model` 等），还有 `turn_id`、`stop_hook_active`（这一轮是否已经被 Stop Hook 续跑过）和 `last_assistant_message`（最后一条回复的文字）。
- 脚本以退出码 0 结束、没有输出，表示正常结束。
- 输出 `{"decision": "block", "reason": "..."}` 时，Codex 不会结束，而是把 `reason` 当成一条新的用户提示继续做。也可以用退出码 2，把原因写到标准错误输出。
- 退出码为 0 时，标准输出只能是 JSON，纯文本无效。
- `Stop` 事件不使用 `matcher`。

### Hook 脚本

保存为项目里的 `.codex/hooks/capture_candidate.py`：

```python
#!/usr/bin/env python3
"""Stop hook：任务结束时提醒 Codex 判断是否输出「素材候选」。"""
import json
import subprocess
import sys
from pathlib import Path

data = json.load(sys.stdin)

# 已经因为本 hook 续跑过一次，直接放行，避免循环
if data.get("stop_hook_active"):
    sys.exit(0)

cwd = data.get("cwd") or "."
try:
    root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd, capture_output=True, text=True, check=True,
    ).stdout.strip()
except (subprocess.CalledProcessError, FileNotFoundError):
    root = cwd

# 没有开关文件就不检查
if not (Path(root) / ".codex" / "capture-on").exists():
    sys.exit(0)

# 本轮回复里已经有判断结果，就不再追加
last = data.get("last_assistant_message") or ""
if "素材候选" in last:
    sys.exit(0)

print(json.dumps({
    "decision": "block",
    "reason": (
        "按 AGENTS.md 的「任务结束时捕捉可复用素材」规则检查本轮工作："
        "符合触发条件就输出「素材候选」小节；不符合就只回复一行"
        "「素材候选：本次不触发」并说明原因。不要修改任何文件。"
    ),
}, ensure_ascii=False))
```

这个脚本做了三层限制，避免变成干扰：

1. **开关文件**：只有项目里存在 `.codex/capture-on` 这个空文件时才检查。不想用时删掉它，不用改配置。
2. **只续跑一次**：`stop_hook_active` 为 `true` 时直接放行，Codex 最多多跑一轮。
3. **已经判断过就跳过**：最后一条回复里已经出现“素材候选”，说明 Codex 按规则做过了，不再追加。

注意 Stop Hook 在**每一轮**回复结束时都会运行，不只是整个任务结束时。所以开关文件适合在做一段集中的工作时打开，平时关掉。

### 注册 Hook

在项目里新建 `.codex/hooks.json`：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/capture_candidate.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

然后创建开关文件：

```bash
touch .codex/capture-on
```

几点说明（来自官方 Hooks 文档）：

- Hook 可以放在 `~/.codex/hooks.json`、`~/.codex/config.toml`、`<项目>/.codex/hooks.json` 或 `<项目>/.codex/config.toml` 里。
- `timeout` 的单位是秒，不写时默认 600 秒。
- 命令在会话的工作目录下运行。Codex 可能从子目录启动，所以官方建议像上面这样从 Git 根目录拼出脚本路径，不要写 `.codex/hooks/...` 这样的相对路径。
- `/usr/bin/python3` 沿用官方示例的写法。你的 Python 不在这个位置（例如 Windows）时，改成本机实际路径。
- Hook 功能默认开启。在 `config.toml` 的 `[features]` 里写 `hooks = false` 可以整体关闭。

### 审核并信任 Hook

非托管的 Hook 必须经过你审核、信任后才会运行。在 Codex CLI 里输入 `/hooks`，可以查看 Hook 来源、审核新增或改动过的 Hook、信任或单独停用某个 Hook。

Codex 按 Hook 当前内容的哈希值记录信任状态，Hook 改动后会重新标记为待审核，审核前不会运行。项目级 Hook 还要求项目的 `.codex/` 目录本身被信任；在未信任的项目里，Codex 只加载用户级和系统级的 Hook。

### 脚本自测结果

把 Hook 接入 Codex 之前，可以先用模拟输入测一下脚本。以下是在一个 Git 仓库里的实测结果：

| 情况 | 输入 | 结果 |
|---|---|---|
| 没有开关文件 | `stop_hook_active: false` | 退出码 0，无输出，正常结束 |
| 有开关文件，回复里没有“素材候选” | `stop_hook_active: false` | 输出 `{"decision": "block", ...}`，Codex 会继续一轮 |
| 已经续跑过一次 | `stop_hook_active: true` | 退出码 0，无输出 |
| 回复里已经有“素材候选” | `last_assistant_message` 含“素材候选” | 退出码 0，无输出 |
| 不在 Git 仓库里 | `cwd` 指向非 Git 目录 | 退出码 0，无输出 |

测试命令示例：

```bash
echo '{"cwd":"'"$PWD"'","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"已修复登录跳转，测试通过。"}' \
  | python3 .codex/hooks/capture_candidate.py
```

有开关文件时的实际输出：

```text
{"decision": "block", "reason": "按 AGENTS.md 的「任务结束时捕捉可复用素材」规则检查本轮工作：符合触发条件就输出「素材候选」小节；不符合就只回复一行「素材候选：本次不触发」并说明原因。不要修改任何文件。"}
```

## 需要落盘时再加保存规则

素材候选先显示在任务结果里最稳妥。确定要长期保存后，可以加一个本机目录，例如 `notes/materials/`，并规定文件名和状态字段：

```markdown
---
title: Codex 任务素材标题
status: candidate
created: 2026-10-26
source_task: 任务名称或本机记录
privacy_review: pending
---
```

公共仓库不适合存放个人内容计划。素材目录如果在项目里，先检查 `.gitignore` 和团队约定，避免把本机记录误提交。

## 和 Memories 的区别

Codex 的 Memories 也会“记住”经验，但用途不同：

| | 素材候选 | Memories |
|---|---|---|
| 谁来写 | 任务结束时 Codex 按规则输出，你决定是否保存 | Codex 在对话空闲后在后台自动更新 |
| 存在哪里 | 对话结果里，或你指定的素材目录 | `~/.codex/memories/` |
| 给谁用 | 给你看，用来写文档、复盘、分享 | 给 Codex 以后的对话召回 |
| 默认状态 | 需要你写规则 | 默认关闭，可在 **Settings > Personalization** 打开，或在 `config.toml` 的 `[features]` 里写 `memories = true` |

官方文档建议：必须遵守的规则写在 `AGENTS.md` 或仓库文档里，Memories 只作为辅助召回，不要依赖它执行规则。所以“任务结束时检查素材”这条规则应该写在 `AGENTS.md`，而不是指望 Memories 记住。

## 用一个小任务验证规则

配置完成后，分别测试一次应该触发和不应该触发的任务：

1. 让 Codex 完成一个带验证步骤的小型流程改动，检查结果里是否出现素材候选。
2. 问一个普通概念问题，确认它不会生成无关提醒。
3. 在测试材料里放一个明显的假密钥，确认输出不会复述这个值。
4. 拒绝保存一次，确认 Codex 不会擅自写入素材文件。
5. 用了 Stop Hook 的话，再确认它在一次回复结束后最多只多跑一轮。

触发太频繁就收紧条件。候选内容总是很空，说明规则缺少证据字段，或者任务本身没有足够材料。先把触发和记录做好，再考虑自动分类、定时复盘或发布流程。

## 小结

- 先在 `AGENTS.md` 里写清楚触发条件、跳过条件和素材候选格式，大多数情况这就够了。
- Codex 经常忘记收尾检查时，再加一个带开关文件、只续跑一次的 Stop Hook，并用 `/hooks` 审核信任。
- 素材候选是给你看的记录，Memories 是给 Codex 召回用的，规则不要交给 Memories。

想把收尾检查扩展成包含验证、记录和交接的完整流程，见 [Codex 任务收尾系统](./04-Codex任务收尾系统.md)；想把跑通的流程直接变成可复用的 Skill，见 [Codex 用 Record and Replay 生成可复用 Skill](../07-Skills实战/05-Codex用Record-and-Replay生成可复用Skill.md)。
