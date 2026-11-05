---
id: codex-notifications-notify
title: Codex 任务完成通知怎么设置：tui.notifications 终端提醒和 notify 脚本推送
seo_title: Codex 任务完成通知：tui.notifications 与 notify 脚本
description: Codex 有两种完成提醒。tui.notifications 由终端发出，notify 在每轮结束时调用你的脚本。本文说明配置写在哪、事件里有哪些字段，以及项目级 config.toml 里的 notify 为什么会被忽略。
lede: 长任务不用一直盯着终端。终端自己的提醒和外部脚本是两条通道，notify 只能写在用户级配置里。
url: /guides/codex-notifications-notify
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 15
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-03
date_modified: 2026-11-03
verified_on: 2026-11-03
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/config-file/config-advanced
keywords: [Codex 通知, Codex notify, tui.notifications, Codex 任务完成提醒, Codex 桌面通知]
related: [config-toml-guide, hooks-guide, codex-goal-mode-long-running-work]
faq:
  - q: notify 现在能收到哪些事件？
    a: 官方高级配置写的是，目前只有 agent-turn-complete。脚本收到一个 JSON 参数，常见字段有 type、thread-id、turn-id、cwd、input-messages 和 last-assistant-message。
  - q: 写在项目的 .codex/config.toml 里为什么没反应？
    a: 官方说明项目级配置不能覆盖 notify。Codex 会忽略项目文件里的这个键，并在启动时警告。要写在用户级 ~/.codex/config.toml。0.166.0 的 doctor 会打出 Ignored unsupported project-local config keys。
  - q: tui.notifications 和 notify 要一起开吗？
    a: 不必。tui.notifications 是终端内建提醒，notify 是外部程序。只想在终端失焦时看一条系统通知，开 tui 即可。要把结果推到 webhook 或自己的脚本，用 notify。
  - q: 这和 Hooks 的 Stop 是一回事吗？
    a: 不是同一套配置。Stop 写在 hooks.json 里，要先在 /hooks 中信任，并且可以让 Codex 继续跑。notify 只在支持的事件上启动外部程序，文档没有说它会改变这一回合。
---

# Codex 任务完成通知怎么设置：tui.notifications 终端提醒和 notify 脚本推送

> 本文在线版：[codexguide.io/guides/codex-notifications-notify](https://codexguide.io/guides/codex-notifications-notify)

> 核对依据：OpenAI 文档 [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 的 Notifications 一节，以及 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 里 `notify`、`tui.notifications`、`tui.notification_method`、`tui.notification_condition` 的条目（2026-11-03 抓取）。配置是否被接受、项目级 `notify` 是否报警，在 Linux 上的 Codex CLI 0.166.0 用 `codex doctor` 看过。本机没有登录，`codex exec` 在请求 API 时返回 401，**notify 脚本没有被调用**，所以下面没有贴一份真实的事件 JSON。ChatGPT 桌面端有没有另一套通知开关，这两篇文档没有写。

一轮任务要跑几分钟甚至更久时，可以让 Codex 在结束时提醒你。配置文件里有两条通道：

| 通道 | 配置键 | 做什么 |
| --- | --- | --- |
| 终端内建提醒 | `tui.notifications` | 由 TUI 按终端能力发通知 |
| 外部程序 | `notify` | 每遇到支持的事件就启动你指定的命令 |

两条都写在用户级 `~/.codex/config.toml`。桌面端是否另有图形界面里的通知设置，官方这两页没有说明，本文不写。

## tui.notifications：开关和事件类型

配置参考给出的类型是布尔值，或一个字符串数组。打开全部：

```toml
[tui]
notifications = true
```

只打开某几类时，高级配置举的例子是 `agent-turn-complete` 和 `approval-requested`：

```toml
[tui]
notifications = ["agent-turn-complete", "approval-requested"]
```

`agent-turn-complete` 是一轮代理结束。`approval-requested` 是 Codex 在等你批准。参考页没有把事件名字穷尽列成一张表，这里只写文档里点名的这两类。

0.166.0 上，把上面的数组和下面两节的 `notification_method`、`notification_condition` 写进用户级配置后，`codex doctor` 没有因为这三个键报警。这次检查时终端是 `TERM=dumb`，没有图形焦点变化，所以没有看到一条真正弹出的 TUI 通知。

## notification_method：OSC 9 和 BEL

```toml
[tui]
notification_method = "auto" # auto、osc9 或 bel
```

默认是 `auto`。auto 时，Codex 优先发 OSC 9。OSC 9 是一段终端转义序列，有的终端会把它显示成桌面通知。终端看起来不支持时，退回 BEL，也就是响铃字符 `\x07`。

想固定方式，把值写成 `osc9` 或 `bel`。终端完全忽略这两种序列时，开着这个键也不会有可见提醒，这时改用下一节的 `notify`。

## notification_condition：什么时候响

```toml
[tui]
notification_condition = "unfocused" # unfocused 或 always
```

默认 `unfocused`：终端不在前台时才提醒。改成 `always` 之后，终端正被看着也会发。人就在这个窗口里看输出时，保持默认即可。

## notify：脚本收到什么

`notify` 是一条命令数组。Codex 发出支持的事件时启动它。高级配置写明，目前只有 `agent-turn-complete`。文档把它用于桌面气泡、聊天 webhook 和 CI 更新，也就是 TUI 内建提醒盖不住的那些旁路。

```toml
notify = ["python3", "/绝对路径/notify.py"]
```

脚本从参数里收到一份 JSON。官方列出的常见字段：

| 字段 | 含义 |
| --- | --- |
| `type` | 目前是 `agent-turn-complete` |
| `thread-id` | 会话标识 |
| `turn-id` | 这一轮的标识 |
| `cwd` | 工作目录，里面通常有本机用户名 |
| `input-messages` | 引出这一轮的用户消息 |
| `last-assistant-message` | 助手最后一条文本 |

文档说的是常见字段，没有说这是完整列表。0.166.0 的程序里，同一组名字旁边还能看到字符串 `client`。本机没有拿到真实 JSON，所以不把 `client` 写成已经确认的字段。日志里如果要留底，先去掉 `cwd`、`thread-id`、`turn-id` 和消息正文。

官方示例是 macOS 上调用 `terminal-notifier` 的 Python。结构是：用 `argparse` 把唯一的参数按 JSON 解析，类型不是 `agent-turn-complete` 就直接返回，再用 `thread-id` 给通知分组。完整脚本在 [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) 的 Notifications 一节，依赖本机已安装的 `terminal-notifier`。

### 示例：Linux 上调用 notify-send

下面这段是按同一份字段写的 Linux 版本，用的是 `libnotify` 的 `notify-send`。本机没有确认通知守护进程把气泡弹出来，把它当成可以抄走再在自己的桌面上试的脚本。

```python
#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notification", type=json.loads)
    note = parser.parse_args().notification
    if note.get("type") != "agent-turn-complete":
        return 0
    if shutil.which("notify-send") is None:
        return 0
    title = "Codex"
    body = note.get("last-assistant-message") or "这一轮结束了"
    subprocess.run(
        ["notify-send", "--app-name=Codex", title, body[:180]],
        check=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`last-assistant-message` 可能很长，也可能含有仓库里的路径。气泡里只放前 180 个字符。不要把整段助手回复发到锁屏界面上。

### 示例：飞书群自定义机器人

飞书开放平台的自定义机器人支持文本消息，请求体是 `{"msg_type":"text","content":{"text":"..."}}`。文档：[自定义机器人](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)。下面的脚本读环境变量 `FEISHU_WEBHOOK_URL`，不把地址写进仓库。

```python
#!/usr/bin/env python3
import argparse
import json
import os
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notification", type=json.loads)
    note = parser.parse_args().notification
    if note.get("type") != "agent-turn-complete":
        return 0
    url = os.environ.get("FEISHU_WEBHOOK_URL", "")
    if not url:
        return 0
    text = note.get("last-assistant-message") or "Codex 这一轮结束了"
    payload = {"msg_type": "text", "content": {"text": text[:500]}}
    data = json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        response.read()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

群机器人如果开了自定义关键词或签名校验，还要按飞书文档补关键词或签名。本机没有向任何飞书地址发送过请求。用一份假的 JSON 在本地只构造请求体、不发网络，得到的是：

```json
{"msg_type": "text", "content": {"text": "示例：这一轮结束了"}}
```

这不是 Codex 打出来的事件。

用户级配置：

```toml
notify = ["python3", "/绝对路径/notify.py"]
```

脚本要能被这个绝对路径找到，并且有执行权限。`cwd` 和消息正文不要写进群里，除非你确认群成员可以看到这些仓库内容。

## 为什么写在项目 .codex/config.toml 里不生效

高级配置写明：项目里的 `.codex/config.toml` 不能覆盖会重定向凭据、改宿主请求、改提供商认证、选择 profile，或在本机运行通知和遥测命令的键。`notify` 在被忽略的名单里。Codex 看到项目文件里的这些键会忽略，并在启动时警告。同名单里还有 `openai_base_url`、`model_provider`、`profiles`、`otel` 等。分层关系见 [config.toml 深入配置](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。

0.166.0 上，在一个已信任的项目里放入：

```toml
notify = ["python3", "/opt/codex-lab/bin/notify.py"]
```

同时用户级配置里也有一份 `notify`。在该项目目录执行 `codex doctor`，警告原文是：

```text
Ignored unsupported project-local config keys in /opt/codex-lab/project/.codex/config.toml: notify. If you want these settings to apply, manually set them in your user-level config.toml.
```

实验目录用的是 `/opt/codex-lab`，里面没有用户名。你自己的家目录路径会不同。警告后半句里的 “user-level config.toml” 就是 `~/.codex/config.toml`，或者你用 `CODEX_HOME` 指到的那个目录下的 `config.toml`。

文档把 `notify` 列为项目级忽略项。`tui.notifications` 不在这张忽略名单里。本文没有另做实验证明项目级 `tui.*` 一定生效，TUI 提醒仍建议写在用户级文件，和 `notify` 放在一起，避免两处各写一半。

未登录时，`codex exec` 完不成一轮，脚本不会被调用。本机的失败停在 API 认证，退出前没有产生 `notify` 记录。要验收脚本，需要一次能正常结束的 `agent-turn-complete`。

## 和 Hooks 的区别

[Hooks](./11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md) 写在 `hooks.json`，改完要在 `/hooks` 里按当前内容信任。`Stop` 在主回合将停时触发，返回 `decision: "block"` 会让 Codex 带着你的理由继续跑。

`notify` 没有这套信任界面，也没有“继续跑”的返回值。它只是在 `agent-turn-complete` 时启动外部命令。审批提醒如果要在终端里出现，用 `tui.notifications` 里的 `approval-requested`，不要指望 `notify` 收到批准事件。

长任务本身怎么写完成标准，见 [Goal 模式](./08-Codex使用Goal模式运行长任务.md)。通知只告诉你一轮停了，不代替完成标准。

## 怎么确认配上了

1. `notify` 和 `[tui]` 写在 `~/.codex/config.toml`，不写在项目的 `.codex/config.toml`。
2. 运行 `codex doctor`，启动警告里不再出现 `project-local config keys` 和 `notify`。
3. 新开一个已经登录的 CLI 会话，让它完成一轮很短的任务。
4. `notification_condition` 保持 `unfocused` 时，把终端切到后台再等结束。
5. 外部脚本先把收到的 JSON 键名写到一个你自己的日志文件。确认有 `type` 之后，再接 `notify-send` 或 webhook。

## 常见问题

**只有响铃，没有桌面气泡。** `notification_method` 处于 auto，当前终端不认 OSC 9，于是退回 BEL。换成 `notify` 加 `notify-send`，或换一个支持 OSC 9 的终端。

**脚本完全没运行。** 看三件事：路径是不是用户级配置里的绝对路径；这一轮是不是真的结束了（认证失败不算 `agent-turn-complete`）；项目文件里的 `notify` 是不是被忽略了。

**webhook 把源码发到群里。** `last-assistant-message` 和 `input-messages` 就是这一轮的对话。群脚本里要自己截断，并避免带上 `cwd`。

**改了配置仍然是旧行为。** 已经打开的 CLI 会话不会重新读配置。退出后新开一次。

## 下一步

配置分层和“哪个文件生效”看 [config.toml 深入配置](../10-配置模型与权限安全/04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)。回合结束时要跑检查并可能续跑，用 [Hooks](./11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)，不要用 `notify` 去拦命令。

## 参考资料

- [Advanced Configuration：Notifications](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
- [飞书自定义机器人](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)
