---
id: cli-manage-multiple-sessions
title: Codex CLI 管理多条任务线：命名、恢复、fork、归档与跨会话交接
seo_title: Codex CLI 会话管理：/rename、resume、/fork、归档删除与交接
description: 用 /rename、codex resume、/fork、archive／delete 管好多条 CLI 任务线；并说明 fork 与 Git worktree 的差别，以及跨会话怎么安全交接。
lede: 会话管上下文，Git／worktree 管磁盘。先分清这两层，再决定命名、恢复、分叉还是归档。
url: /guides/codex-cli-manage-multiple-sessions
status: published
section: guides
category: I-automation-workflow
topic: 自动化与高级工作流
content_type: 指南
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-21
date_modified: 2026-10-22
client_validation_pending: false
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://developers.openai.com/codex/cli/reference
keywords: [Codex CLI, 会话管理, resume, fork, rename, archive, 跨会话]
related: [cli-resume-long-tasks, permissions-sandbox-approvals]
faq:
  - q: fork 会不会自动开一条 Git 分支？
    a: 不会。官方写明 /fork 与 codex fork 复制的是聊天转录（上下文）到新会话 ID；原会话保持不变。磁盘上的改动仍落在当前工作区，除非你再配 --worktree 或 /worktree。
  - q: archive 和 delete 有什么差别？
    a: archive／unarchive 只是从常用会话列表收起或恢复，转录还在；delete 会永久删除转录，且会连带删除由其派生的 descendant 会话。能归档就先别删。
  - q: 找不到昨天的会话怎么办？
    a: 默认 picker 与 --last 只看当前工作目录。换过目录时加 --all；若是 codex exec 开的非交互会话，还要加 --include-non-interactive。有名字就用名字或 UUID 直接 resume。
---

# Codex CLI 管理多条任务线：命名、恢复、fork、归档与跨会话交接

> 本文在线版：[codexguide.io/guides/codex-cli-manage-multiple-sessions](https://codexguide.io/guides/codex-cli-manage-multiple-sessions)

> 核对依据：OpenAI Developers / learn.chatgpt.com 的 Developer commands（CLI command reference 与 Slash commands）。文中「我的用法」是操作建议，不是官方强制规定。命令与界面文案随 CLI 版本变化，以你本机 `codex --help` 与当前文档为准。

同时推重构、排错和测试时，不必为每条线开一个终端窗口硬扛。Codex CLI 会把交互会话落盘：你可以命名、按目录或名称恢复、从某一节点 fork 出实验线，也可以归档或删除。

**会话管「说过什么、约定过什么」；工作区与 Git／worktree 管「磁盘上改了什么」。** 两件事别混。fork 一条新聊天，并不会自动隔离文件写入。

本文讲 CLI 侧的日常管理。桌面端／IDE 也有 `/fork`、`/side` 等相近能力，菜单位置不同；企业托管与 app-server 协议细节不展开。

## 1. 先认清几组命令

| 你想做的事 | 会话内（Slash） | 终端（子命令） | 关键事实 |
| --- | --- | --- | --- |
| 给当前会话起名 | `/rename` | （无对等子命令；靠命名后再用名字定位） | 只改显示名，不改转录、不扩权限 |
| 继续旧会话 | `/resume` | `codex resume`、`codex resume --last`、按 ID／名称 | `--last` 默认只看当前工作目录 |
| 分出一条新聊天 | `/fork` | `codex fork`、`codex fork --last`、按 UUID | 新会话新 ID；原转录不动 |
| 临时旁支提问 | `/side`（别名 `/btw`） | — | 短暂 fork，不污染主线转录 |
| 收起但不删 | `/archive` | `codex archive <SESSION>` | 可 `codex unarchive` 找回 |
| 永久删除 | `/delete` | `codex delete <SESSION>` | 删转录；可连带 descendant |
| 给已有会话塞一条消息 | — | `codex queue --thread <ID或精确名> --message "..."` | 跨会话交接的常用出口之一 |
| 隔开磁盘写入 | `/worktree`；fork 时可选 worktree | `codex fork <SESSION_ID> --worktree`；`codex exec --worktree` | 需要显式会话 ID；`--last`／picker 不能配 `--worktree` |

会话参数里：**UUID 优先于同名**。重名时用 UUID，避免误操作。

## 2. 用 `/rename` 让列表可读

UUID 过一周就没法认。进入当前会话后：

1. 输入 `/rename 订单模块重构`，或先 `/rename` 再在提示里填名字。
2. 官方预期：保存的聊天名更新，**转录内容不变**。

之后这些地方都能用名字（与 ID 二选一，ID 优先）：

- `codex resume 订单模块重构`
- `codex archive 订单模块重构` / `codex unarchive …`
- `codex delete 订单模块重构`（仍会确认）
- `codex queue --thread 订单模块重构 --message "…"`（要求**精确**同名；重名请改用 UUID）
- `codex exec resume` / `codex exec fork` 同样接受名称（`codex fork` 终端子命令本身文档写的是 UUID 或 `--last`）

**我的用法**：名字写「对象 + 动作」，例如 `支付重试-实现`、`支付重试-只读排查`，不要只写 `临时`、`test`。名称不会缩小沙箱，也不会自动换模型——那些仍用 `/permissions`、`/model`。

新建时也可以顺带命名：`/new bug bash`、`/clear release prep`（官方文档示例）。

## 3. 用 `codex resume` 接上昨天的线

交互会话默认会写入本地。要继续：

```bash
# 打开当前目录下的会话选择器
codex resume

# 直接继续本目录最近一次交互会话
codex resume --last

# 跨目录找「最近一次」或在 picker 里看到其他目录的会话
codex resume --all

# 把非交互（例如 codex exec）会话也纳入 picker / --last
codex resume --include-non-interactive

# 按 UUID 或已 /rename 的名字恢复
codex resume <SESSION_ID或名称>
```

官方要点：

1. **`--last` 默认限定当前工作目录**；找不到时先想是不是换过 `cwd`，再加 `--all`。
2. **`codex exec` 开的会话**默认不进 picker，也不进 `--last`，除非 `--include-non-interactive`。
3. 当前目录与会话保存目录不一致时，Codex 会问用哪边；可在配置里设 `tui.resume_cwd` 为 `"current"` 或 `"session"`。显式 `--cd` / `-C` 优先于该设置。
4. `codex resume` **接受**模型／沙箱等覆盖，**不接受** `--worktree`（要隔离磁盘，用 fork + `--worktree`，或会话内 `/worktree`）。

会话内也可用 `/resume` 打开已保存列表，效果同类：重载选中会话的转录，从断点继续。

非交互流水线用 `codex exec resume --last "下一步指令"`（或带会话 ID／名称）；这是脚本续跑，不是 TUI 多线并行的主路径。

## 4. 用 `/fork` 试方案，而不是覆盖主线

### 4.1 分叉当前聊天

会话空闲或按文档步骤操作时：

1. 输入 `/fork`。
2. 若提示 checkout，可选**当前目录**或**新建 managed Git worktree**。

官方预期：克隆当前聊天到**新 ID** 的新会话，**原转录保持不动**，方便并行试另一条路。

相关快捷方式（官方 Interactive shortcuts）：作曲栏为空时连按两次 Escape，可编辑上一条用户消息，并从该点 fork。

临时问题不想留在主线：用 `/side`（或 `/btw`）。这是短暂旁支；不可嵌套在另一个 side 里，review 模式也不可用。

### 4.2 从已保存会话分叉

```bash
codex fork                  # 打开 picker
codex fork --last           # 分叉本目录最近会话
codex fork --all            # picker 含其他目录
codex fork <SESSION_UUID>   # 指定会话

# 分叉到 managed Git worktree（必须显式 SESSION_ID；不能 --last / picker）
codex fork <SESSION_ID> --worktree
```

工作目录与会话目录不一致时，`codex fork` 与 `resume` 共用同一套目录确认逻辑和 `tui.resume_cwd`。

非交互：`codex exec fork <SESSION_ID或名称> [PROMPT]`；可加 `--worktree`。无 prompt 时只创建 fork、不立刻开 turn。

### 4.3 必须分清的三件事

| 概念 | 实际复制／改变什么 | 常见误解 |
| --- | --- | --- |
| 会话 fork | 聊天历史 → 新会话 ID | 「等于 git checkout -b」 |
| Git 分支 / worktree | 工作树与提交历史 | 「fork 了就自动隔离文件」 |
| `/side` | 临时旁支转录 | 「和长期 fork 一样可归档管理」 |

**两条会话若写同一工作区，文件改动会打架。** 需要并行改代码时：

- 只让**一条**会话有写权限，另一条只读分析；或
- 用 `/worktree`、`codex fork <ID> --worktree`、`codex exec --worktree` 把写入分到独立 checkout。

fork **不会**自动合并两条线之后的磁盘改动；要合并，仍走你自己的 Git／评审流程。

## 5. 归档与删除：收列表，别误删证据

### 5.1 归档：列表变短，转录还在

```bash
codex archive <SESSION_ID或名称>
codex unarchive <SESSION_ID或名称>
```

会话内：`/archive` → 确认。官方说明：从**活动会话列表**拿掉，**保留转录**；之后用 `codex unarchive` 恢复。连着本地／远程共享 server 时，归档后会回到 command center；没有共享 server 时 CLI 会退出。若当轮还在跑，确认归档会先停掉该 turn。

**适用**：做完的主线、暂时不碰的实验线、只想让 `codex resume` 列表干净。

### 5.2 删除：不可当「再藏一下」

```bash
codex delete <SESSION_ID或名称>
codex delete <SESSION_UUID> --force   # 仅 UUID；名称仍要交互确认
```

会话内：`/delete` → 确认。官方说明：

- **永久删除**转录；
- 会删除由其派生的 **descendant** 会话；
- 聊天仍在跑，或处在 side chat 时，`/delete` 不可用；
- `--force` **只能**配 UUID，避免同名误删。

**我的用法**：默认只 archive。确定无合规／排障价值、且看清 UUID 后再 delete。密钥、客户数据若曾进过转录，删除也替代不了你们自己的数据保留政策——那是流程问题，不是多敲一次 delete。

`codex archive` / `delete` / `unarchive` / `resume` / `fork` 等支持 `--remote`（及按需 `--remote-auth-token-env`），用于连远程 app-server；本地日常可忽略。

## 6. 跨会话交接：交什么、怎么交

「交接」不是魔法同步，而是把**下一会话真正需要的状态**递过去，并写清**谁可以改磁盘**。

### 6.1 官方提供的交接出口

1. **`/fork` / `codex fork`**：把截至当前的上下文整份带到新会话，适合「同一问题换一条实现路径」。
2. **`/side`**：短问短答，结果留在旁支；适合主线正忙时查一个点。
3. **`codex queue`**：向已有会话投递下一条指令，不必先打开 TUI：

   ```bash
   codex queue --thread <UUID或精确名称> --message "跑完剩余检查并把失败用例路径列出来"
   ```

   不支持附件图片。名称必须精确；共享名时用 UUID。
4. **`/export`**：导出完整 Markdown 转录（剪贴板或文件，例如 `/export session.md`）。适合交给人审，或粘进另一条全新会话的开场白。
5. **`/recap`**：生成摘要且**不**压缩上下文；需要腾上下文窗口时用 `/compact`，两者目的不同。
6. **`codex agents` / `/agents`**：在共享 local／remote server 上浏览、切换多个 agent 聊天（需要共享 server；不是单机默认必有）。

### 6.2 一份可执行的交接清单（我的用法）

交给另一条会话（或未来的自己）时，尽量写清：

1. **目标**：这一条线要交付什么，不算什么。
2. **已确认事实**：关键路径、接口约定、失败复现步骤；附 `/export` 或短 recap，避免口口相传。
3. **磁盘边界**：是否允许改文件；若允许，是否已在独立 worktree／分支；主线是否仍在写同一树。
4. **验证方式**：测哪些命令、怎样算完成。
5. **禁止项**：生产库、真实密钥、不可回退操作。

示例分工（仍是建议，不是产品强制角色）：

| 角色 | 会话怎么开 | 权限倾向 |
| --- | --- | --- |
| 主线实现 | 命名清晰的长会话；需要时 `/goal` 钉目标 | 工作区写入 + 按需审批 |
| 只读排查 | `/new` 或从主线 fork 后立刻收紧权限 | 只读／少写 |
| 方案对比 | 主线 `/fork`，必要时 `--worktree` | 每条线一块磁盘 |
| 收尾验证 | `queue` 一条验收指令，或新会话只跑测试 | 能只读就只读 |

不要假设「两个会话会自动互相通话、共享未导出的记忆」。官方保证的是：**可恢复的转录、可 fork 的副本、可 queue 的消息、可 export／recap 的文本**。其余靠你写清楚。

## 7. 一套可落地的多线节奏

1. **开工就 `/rename`**，并（可选）`/goal` 写清完成标准。
2. **主线只做实现与最终验证**；分析日志、对比方案、写测试用例，能分则分到只读或 fork 线。
3. **要并行改代码 → worktree 或分支**，不要两条线共写一个脏工作区。
4. **告一段落 → `/export` 或短交接备忘**，再 `archive` 冷却线；列表只留进行中的。
5. **版本与命令有出入时**，以本机 `codex --help` 与 [Developer commands](https://developers.openai.com/codex/cli/reference) 为准，不要死记第三方博客里的旧 flag。

## 8. 常见卡住点

| 现象 | 先查什么 |
| --- | --- |
| `resume --last` 不是我想要的 | 是否换过目录；试 `--all`；是否其实是 exec 会话（加 `--include-non-interactive`） |
| picker 里没有某条 | 是否已 archive；名称是否记错；用 UUID；`codex unarchive` |
| fork 后文件乱了 | 是否两条线写同一工作区；补 worktree／收权限 |
| delete 误伤 | 是否删到了带 descendant 的父会话；以后先 archive |
| queue 找不到线程 | 名称是否精确；重名时改 UUID；会话是否已删 |

## 最后记住这五句

1. **命名是给未来的自己用的**，不改变权限与目标。
2. **`resume` 默认看当前目录**；跨目录加 `--all`。
3. **fork 复制的是聊天，不是 Git 分支**；并行写入要靠 worktree／纪律。
4. **archive 藏列表，delete 毁转录（含 descendant）**。
5. **跨会话交接靠 fork／queue／export／写清边界**，不要指望隐式同步。

更长的「停下来再接上」流程，可与《Codex CLI 恢复长任务》对照；权限档位见《权限、沙箱与审批》。
