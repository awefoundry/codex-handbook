---
id: codex-cross-session-collaboration
title: Codex 跨会话协作：开新会话交接任务、带上下文派生，不再靠复制粘贴
seo_title: Codex 跨会话协作：交接、fork、queue 与 Goal 怎么分工
description: 一条会话塞进讨论、实现和测试，关键决策容易被冲掉。本文说明什么时候开新会话、交接时要写清哪些上下文，以及这和 /fork、queue、Goal 模式各自解决的问题。
lede: 会话之间传递的是你写明的任务和上下文。命令负责复制转录、投递消息或钉住目标，磁盘隔离要另外安排。
url: /guides/codex-cross-session-collaboration
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-17
date_modified: 2026-11-05
verified_on: 2026-08-17
official_ref: https://learn.chatgpt.com/docs/developer-commands
keywords: [Codex 跨会话, Codex 任务交接, Codex fork, Codex queue, Codex 开新会话]
related: [cli-manage-multiple-sessions, codex-goal-mode-long-running-work, codex-subagents-parallel-work, worktree-parallel-chats]
faq:
  - q: 让当前会话「再开一个会话」，和 /fork 是一回事吗？
    a: 不完全是同一条文档命令。/fork 和 codex fork 做的是把已有聊天克隆成一条新 ID 的会话，原转录保持不动。桌面端配图里的「由 ChatGPT 从另一项任务发送」，说明一条任务可以把消息送到另一条任务。2026-11-05 的命令文档没有把这句界面文案写成一个斜杠命令。要投递一段文字到已有会话，文档写明的是 codex queue。
  - q: 两条会话会自动共享还没写出来的记忆吗？
    a: 文档保证的是可恢复的转录、可 fork 的副本、可 queue 的文本，以及子代理派生出来的 descendant 会话会随父会话归档或删除。没有写进消息、转录或文件里的背景，下一条会话看不到。
  - q: 这篇和《Codex CLI 管理多条任务线》为什么都留着？
    a: 地址都还在用。那篇是 /rename、resume、fork、archive、queue 的命令对照。这篇讲什么时候拆开、交接时要带上哪些上下文，以及和 Goal、Plan、Subagent、worktree 怎么配。两边不合并。
---

# Codex 跨会话协作：开新会话交接任务、带上下文派生，不再靠复制粘贴

> 本文在线版：[codexguide.io/guides/codex-cross-session-collaboration](https://codexguide.io/guides/codex-cross-session-collaboration)

> 核对依据：ChatGPT Learn《[Developer commands](https://learn.chatgpt.com/docs/developer-commands)》（`codex queue`、`codex fork`、`codex resume`、`/plan`、`/goal`、归档与删除对 descendant 会话的影响）、[CLI 0.166.0 更新日志](https://learn.chatgpt.com/docs/changelog) 中的 `codex queue --resume`，以及《[Long-running work](https://learn.chatgpt.com/docs/long-running-work)》在 Goal 专文中的用法。配图来自本文上线时的桌面端截图，任务正文已裁掉。2026-11-05 核对了命令文档，没有重新操作一次桌面端交接。界面文案以当前 App 为准。

适合已经能在一个会话里把功能做完，但一长起来就分不清「现在等我决定什么」的人。读完可以决定：继续留在这条会话、fork 一条实验线、用 queue 把一句话交给已有会话，还是把子任务交给 Subagent。

命令本身的标志和选择器，见 [Codex CLI 管理多条任务线](./03-CodexCLI管理多条任务线.md)。本文不重复那张命令表，也不替换它的网址。

## 什么时候该开新会话

一条会话适合装下**一件**从讨论到验收的事。上下文留在同一条转录里，后面的修改才知道前面为什么这样定。

该拆开的信号通常是这些：

- 优先级堆成一串，真正要你拍板的句子被进度刷走。
- 实现已经开始，测试、审查或另一个独立功能需要自己的完成标准。
- 你想试一条会推翻当前方案的路，又不想改写主线转录。
- 两条线都要改文件。这时还要拆工作区，只开新会话不够。

继续留在当前会话的情况同样明确：改动还在同一块代码上，下一步只是收窄范围或补一条验证。中途纠偏可以用即时 Steer，方案还没定可以用 `/side`。这些都不需要新的会话 ID。

## 让当前会话创建并交接

桌面端可以出现这种标记：消息来自另一项任务。下面两张图只保留了这条产品标记，任务正文、仓库名和结果列表已裁掉。

![接收任务的会话顶部显示「由 ChatGPT 从另一项任务发送」](../图片素材/11-自动化与高级工作流/02-Codex跨会话协作功能/01-任务交接.png)

![另一条会话同样标出来源是另一项任务](../图片素材/11-自动化与高级工作流/02-Codex跨会话协作功能/02-派生任务.png)

标记说明接收方能看出：这句话不是用户在这个输入框里新打的，而是从另一项任务送来的。原用法是在实现做完后告诉当前会话：准备测试用例，在某个目录下开一条新会话，把测试交出去，当前会话负责验收。派生任务也是同一类动作：让当前会话开一条新会话，把任务和当时的上下文一起送过去。

2026-11-05 的开发者命令文档**没有**把「由 ChatGPT 从另一项任务发送」写成一个斜杠命令，也没有保证任意两句话都会让两条会话自动对讲。能对上文档的机制是下面几条。菜单若和配图不一致，以你本机为准。

| 你要发生的事 | 文档里的做法 | 对方拿到什么 |
| --- | --- | --- |
| 从现在的聊天分出一条平行实验 | 会话里 `/fork`；或终端 `codex fork` | 一份克隆的转录，新的会话 ID。原转录不动 |
| 给一条已经存在的会话送下一步 | `codex queue --thread <会话 ID 或精确名称> --message "…"` | 一段文本。命令只接受文本，不接受图片附件 |
| 那条会话还没加载，送完就继续跑 | 同一条命令加上 `--resume` | 先入队，再尝试恢复。需要本地 daemon，或用 `--remote` 指定的服务器 |
| 把范围明确的子任务交给子代理 | 当前会话里的 Subagent | 派生出的子会话。归档、恢复、删除父会话时，文档写明会尽量连带处理这些 descendant |
| 人要审阅或另开一条全新会话 | `/export` 导出 Markdown，或自己写一份交接 | 你贴进去的那些文字 |

`/fork` 的预期结果是：克隆当前聊天，新聊天有新的 ID，原转录保持不动，便于并行试另一条路。若出现检出选择，可以留在当前目录，或使用新的 worktree。

`codex queue` 的 `--thread` 接受 UUID 或**精确**会话名。重名时用 UUID。入队消息使用该会话自己的模型。`--resume` 在 CLI 0.166.0 的更新日志里加入：会话尚未加载时，入队后尝试恢复。恢复不了时，Codex 会打印警告，命令仍然成功退出。消息还在队列里，会话不一定已经跑起来。

删除会永久去掉转录，并去掉由它派生的 descendant 会话。只是想从列表里收起时，用归档。`/delete` 在会话仍在运行、或正处在 side chat 时不可用。

## 派生任务时要带走的上下文

新会话、fork 或 queue 的那条消息里，写上对方才能动手的事实。下面这份清单是交接时的写法，不是官方的必填字段：

1. **目标**：这一条线交付什么，到哪一步停。
2. **已确认的事实**：路径、接口、已经否决的方案、失败时怎么复现。
3. **磁盘边界**：能否改文件；若能改，在哪个目录或哪条 worktree；主线是否还在写同一棵工作区。
4. **验证**：跑什么命令，怎样算完成。
5. **不做的事**：生产数据、真实密钥、不能回退的发布。

fork 会把截至当时的转录带过去，所以主线里已经写过的决定会在副本里。queue 只送你写进 `--message` 的文字，之前的转录要靠对方那条会话自己已经有，或靠你在消息里重述。导出的 Markdown 适合人来读，也适合贴进一条全新会话的开头。

两条会话若写同一个工作区，文件会互相覆盖。要并行改代码时，用 worktree 或让其中一条只读。`codex fork --worktree` 需要明确的会话 ID 和本地执行，不能配 `--last`，也不能用会话选择器。细节见 [用 Worktree 并行运行多个任务](./10-Codex用Worktree并行运行多个任务.md)。

## 和 /fork、resume、queue 的关系

三件事经常被说成「接着做」，结果不同：

| 动作 | 会话 ID | 适合 |
| --- | --- | --- |
| `codex resume` 或 `/resume` | 还是原来的 ID | 昨天的线今天继续。`--last` 默认只看当前工作目录，跨目录加 `--all` |
| `/fork` 或 `codex fork` | 新的 ID，原线还在 | 同一问题上试另一条实现，或把测试线从实现线分出去 |
| `codex queue` | 你点名的那条已有 ID | 人不用先打开 TUI，也要把一句话送进那条线 |

`resume` 不接受 `--worktree`。要隔离磁盘，用带会话 ID 的 fork，或在会话里使用 `/worktree`。

子代理派生的会话和一次 `/fork` 也不一样。`/agent` 用来查看或继续一条已经派生的子代理线程。父会话归档或恢复时，Codex 会尝试一并处理它派生的子会话及其后代。范围清楚、最好不要改同一批文件的调查和检查，用 [Subagents](./09-Codex使用Subagents并行处理任务.md)。需要一条以后还能按名字 resume 的长线，用命名过的会话，并在交接消息里写清边界。

## 和 Goal、Plan 怎么配合

拆开之后，每一条还在跑的长线需要自己的完成标准。

- **`/plan`**：把当前聊天切到计划模式，也可以在命令后直接写计划请求，例如 `/plan` 后面跟上要迁移的服务。Codex 正在工作时，`/plan` 暂时不可用。计划模式先把步骤摊开。知识库里 Goal 专文写了「先计划、再开目标」的接法。
- **`/goal`**：目标附在**当前**对话上，同时是第一条提示和完成标准。目标不能为空，最多 4,000 个字符。更长的说明放进文件，让目标指向文件。写法、暂停和并行见 [Codex Goal 模式](./08-Codex使用Goal模式运行长任务.md)。

一条线一个目标。实现线的目标是行为改完且指定测试通过；测试线的目标是用例补齐且命令有结果。不要把两条线的完成标准写进同一句 `/goal`，再指望会话自己分家。

讨论和执行已经缠在一起、只是还没到要新会话的程度时，先看 [长任务工作流](./05-Codex长任务工作流.md)：临时问题、方案讨论、独立子任务和审查可以分开，交接记录仍然要写清当前文件和 Git 状态。

## 一次可以照着做的交接

下面是操作顺序，不是官方向导。2026-11-05 没有在桌面端再走一遍。

1. 给当前实现会话一个能认出来的名字，并用 `/goal` 写上这条线的完成标准。
2. 测试或审查若会冲掉实现上下文，用 `/fork` 分出一条新聊天；两条都要改文件时，fork 到单独的 worktree。
3. 在新会话的第一句里写上目标、已确认事实、可以改的目录和验证命令。若新会话已经存在，用 `codex queue --thread` 把这段话送进去。
4. 实现会话只保留验收：等测试线的结果，再对照验证命令看，而不是把对方的转录默认为已经同步过来。
5. 结束后归档冷却的线。确认不再需要转录时才删除，因为删除会带上 descendant。

## 常见问题

| 现象 | 先看什么 |
| --- | --- |
| 新会话不知道主线已经决定的接口 | 交接消息或 fork 的时间点是否早于那个决定。queue 不会自动附带你没写进消息的句子 |
| fork 之后两个目录的文件乱了 | 是否仍在写同一工作区。补 worktree，或让一条线只读 |
| `queue` 找不到线程 | 名称是否逐字相同。重名时改用 UUID |
| 加了 `--resume` 却没有跑起来 | 本地 daemon 是否在运行，或是否需要 `--remote`。看警告。消息可能已经入队 |
| 删了一条父会话，子任务也不见了 | 删除会去掉 descendant。还要留档时改用归档 |
| 配图里的标记在新版本里换了说法 | 以当前 App 为准。用本节的命令表核对「克隆转录」还是「投递文本」 |

## 参考资料

- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/cli/slash-commands)
- [ChatGPT & Codex changelog · CLI 0.166.0](https://learn.chatgpt.com/docs/changelog)
- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
