---
id: codex-long-task-collaboration-workflow
title: Codex 长任务工作流（2026-11 更新）：主任务定方向，/side 讨论、Subagents 分担、独立审查，最后留交接记录
seo_title: Codex 长任务工作流：/side、Subagents、审查与交接
description: 长任务容易越做越乱。本文按官方 Long-running work 的思路，讲清主任务怎么保持方向，临时问题和方案讨论放哪，什么工作交给 Subagents，修改完怎么独立审查，以及结束前留一份能让下一轮接得上的交接记录。
lede: 决定留在主会话。插问用 /side。又吵又可以并行的只读工作交给 Subagents。改完再单独审查，暂停前写交接。
url: /guides/codex-long-task-collaboration-workflow
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-12
date_modified: 2026-11-05
verified_on: 2026-11-05
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/long-running-work
keywords: [Codex 长任务, Codex long-running work, Codex /side, Codex Subagents, Codex 任务交接]
related: [codex-goal-mode-long-running-work, codex-subagents-parallel-work, cli-manage-multiple-sessions, codex-cross-session-collaboration, codex-plan-mode, codex-cli-commands-cheatsheet]
faq:
  - q: 长任务应该一直留在同一个会话，还是经常新开？
    a: 官方 Long-running work 写的是，相关工作留在同一条聊天里，方便它用同一份上下文决定下一步。Subagents 文档同时写，把探索笔记、测试日志这类中间输出堆进主会话，会把要求和决定埋掉。两句一起用：决定留在主会话，噪声放到侧边对话或子 agent。
  - q: /side 和 /fork 有什么区别？
    a: /side（别名 /btw）是临时侧边对话，记录与主会话分开，并且不离开主会话的状态显示。/fork 会克隆出一条有新 ID 的会话，原记录保持不变，用来并行试另一条路。侧边对话不能再套一层 /side，审查模式里也不能用。
  - q: Subagents 会不会用一套更宽的权限？
    a: 不会。官方写子 agent 继承当前沙箱和审批，包括 /permissions 或 --yolo 刚改过的设置。自定义 agent 文件不能换掉这些设置。
  - q: 恢复旧会话时，上次点过的审批还在吗？
    a: CLI 0.166.0 的更新日志写，恢复或分叉时会保留已经确认过的审批和权限设置。同一条还写，推理 token 的计数会跨恢复和分叉保留，避免过早压缩。本文没有拿一条旧会话做恢复实验。
---

# Codex 长任务工作流（2026-11 更新）：主任务定方向，/side 讨论、Subagents 分担、独立审查，最后留交接记录

> 本文在线版：[codexguide.io/guides/codex-long-task-collaboration-workflow](https://codexguide.io/guides/codex-long-task-collaboration-workflow)

> 核对依据：ChatGPT Learn [Long-running work](https://learn.chatgpt.com/docs/long-running-work)、[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)、[Command line options](https://learn.chatgpt.com/docs/developer-commands) 里的 `/side`、`/goal`、`/review`、`codex resume`、`codex fork`（2026-11-05），以及 [更新日志](https://learn.chatgpt.com/docs/changelog) 中 CLI 0.166.0 的两条修复。本机没有登录，没有桌面端，所以没有重拍界面。旧文 6 张桌面截图已从本文撤下，原因写在文末。

这条会话如果又在改需求、又在贴日志、又在试第二种方案，做到后面就分不清哪一句才算数。下面按官方文档把几件事分开：主会话留目标和决定，插问放侧边，可以并行的只读工作交给子 agent，改完再单独审查，暂停前写一份接得上的记录。

`/goal` 的完成标准、暂停和并行，见 [Goal 模式](./08-Codex使用Goal模式运行长任务.md)。子 agent 的 TOML 和并发设置，见 [Subagents](./09-Codex使用Subagents并行处理任务.md)。会话的命名、恢复、fork 和归档，见 [管理多条任务线](./03-CodexCLI管理多条任务线.md)。

## 长任务为什么会越做越乱

Long-running work 的要求是：多步工作要给出结果、约束和完成定义，并且把相关工作留在同一条聊天里。这样 Codex 才能用同一份上下文选择下一步，并判断做完没有。

Subagents 文档写了留在同一条聊天里的代价。主会话本来是在定要求、约束和决定。若把探索笔记、测试日志、堆栈和命令输出都堆进来，有用的信息会被埋住，会话会越来越不可靠。文档用了两个说法：context pollution（有用信息被中间输出盖住）和 context rot（塞进无关细节之后，表现变差）。

所以不是「永远不要新开聊天」，也不是「做着做着就换一条」。相关的决定留在主会话。中间噪声放到侧边对话或子 agent，只把摘要带回来。彼此独立、而且会改同一批文件的任务，不要塞进同一条写入。

## 先定目标和验收标准

Long-running work 把一条目标拆成三样，能用上的都写上：

| 要素 | 写什么 |
|---|---|
| 结果 | 要的结果，而不是只写「去改一改」 |
| 约束 | 必须用的工具、边界、兼容要求，或明确不要的做法 |
| 验证 | 能证明做完的测试、测量或审查标准 |

文档里的例子是：把代码库从 JavaScript 迁到 TypeScript，保持现有行为，严格模式编译且没有显式 `any`，完整测试通过。

目标还说不清时，先用 `/plan` 让它问清约束，再变成带验收标准的目标，然后用 `/goal` 开始。`/goal` 的文本同时是第一条提示和完成标准。进行中要改约束，在同一条会话里追加，而不是默默换一条聊天。启动 goal 不会扩大权限：沙箱和审批政策不变，需要决定时会停下。这些细节以 Goal 那篇为准，这里不重复命令表。

## 临时问题和方案讨论：/side

官方命令表里，临时插问是 `/side`，别名 `/btw`。它从当前聊天开一个临时侧边对话，记录与主会话分开，你也不必离开主会话。侧边模式打开时，终端仍显示主会话的状态，所以能看到主任务还在不在跑。

用法：

1. 输入 `/side` 打开侧边对话。
2. 可以在同一行写上问题，例如 `/side 这个方案有没有明显风险`。
3. 问完回到主会话。只把已经定下来的要求和理由带回去。

限制也是命令文档写明的：已经在侧边对话里时，不能再开一层 `/side`；审查模式里也不能用。

Long-running work 对桌面端的说法是：想要进度复述或解释、又不想打断主聊天时，用 side chat。断网之前先暂停 goal，恢复之后再让它继续。CLI 里对应的是在同一条交互会话里追加消息，或用 `/side` 做这次插问。

旧文把「快速聊天」写成和 Side Chat 并列的入口，并附了桌面端按钮截图。2026-11-05 的 Long-running work 和命令文档没有把 Quick Chat 写成一个步骤。本文不再教那个按钮，也不再引用那些截图。你的桌面端若仍有类似入口，以当前菜单为准；CLI 和 IDE 以 `/side` 为准。

## 能并行的交给 Subagents

子 agent 适合从主会话里拿走上的、可以并行的部分：读代码、跑测试、看日志、做摘要。官方的起点是 read-heavy 的工作。多个子 agent 同时改代码，容易冲突，协调成本也会上去，写多的活要更小心。

每个子 agent 自己做模型和工具调用，所以比单 agent 更费 token。大多数智能档要你明确说「拆给子 agent」。Ultra 可以在并行确有帮助时主动委派。本地 Codex 还会在 `AGENTS.md` 或 Skill 要求委派时照做。

一条说得清的委派要包括：怎么拆、要不要等全部完成、摘要里返回什么。官方示例是让三个子 agent 分别看安全风险、测试缺口和可维护性，等齐之后按类汇总，并附文件位置。CLI 里用 `/subagents` 在运行中的 agent 线程之间查看和切换。

权限跟父会话走。子 agent 继承当前沙箱和审批，包括你用 `/permissions` 或 `--yolo` 刚改过的设置。自定义 agent 文件可以要求它不要改文件，但不能换成另一套只读沙箱，也不能换掉 MCP。交互会话里，没在看的那条 agent 线程仍可能弹出审批。Subagents 文档写明，审批条上会标出来源线程，可以按 `o` 打开那条线程再决定。非交互、或这次运行弹不出新的审批时，需要新审批的动作会失败，错误回到父流程。

内置的 `default`、`worker`、`explorer`，以及 `~/.codex/agents/` 和项目 `.codex/agents/` 里的 TOML，见 [Subagents](./09-Codex使用Subagents并行处理任务.md)。不要为了并行，把一个还在变的需求拆出去。

## 中途恢复和分叉

主会话中断之后，交互式继续用 `codex resume`，非交互用 `codex exec resume`。想保留原会话、另开一条试法，用 `codex fork` 或会话里的 `/fork`。工作目录和保存时不一致时，Codex 会问用哪一个；`tui.resume_cwd` 设为 `"current"` 或 `"session"` 可以不再问。显式的 `-C` 优先。这些开关的细节见 [管理多条任务线](./03-CodexCLI管理多条任务线.md) 和 [恢复长任务](./04-CodexCLI恢复长任务.md)。

和长任务直接相关的，是 CLI 0.166.0 更新日志里的两条修复：

- 恢复或分叉时，保留已经确认过的审批和权限设置（#57227）。
- 推理 token 的计数跨恢复和分叉保留，避免过早压缩（#57839）。

两条都是更新日志的表述。本文没有登录，没有拿一条旧会话做恢复或分叉，所以不写「恢复之后审批弹窗一定和上次相同」。

0.166.0 还加了 `codex queue --resume`：把消息排进已有会话后，尝试在本地 daemon 或 `--remote` 指定的服务器上把这条线程拉起来。拉不起来会警告，命令仍然成功。适合主会话还在、你只是补一句后续，而不是另开一条任务。命令表见 [CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。

彼此独立的任务可以并行，但不要让两条聊天同时写同一批文件。本地并行可以用 worktree 分出单独的检出。见 [Worktree](./10-Codex用Worktree并行运行多个任务.md)。Long-running work 还写：本地并行时可以打开 Prevent sleep while running，并用通知看聊天是否在等输入。通知怎么配，见 [任务完成通知](./15-Codex任务完成通知-tui.notifications与notify脚本.md)。同一页还提到 Pets，本文没有另查这个名称的产品说明，不展开。

## 改完单独审查

实现和审查分开，是为了让「问题被发现时的差异」还在。命令文档里，工作区审查是 `/review`：它按当前会话的模型（除非配置了 `review_model`）总结工作区里的问题，重点是行为变化和缺失的测试。需要看具体改动时再跟 `/diff`。

不在交互会话里时，用 `codex review`，并且只选一个范围，例如 `--uncommitted`、`--base main` 或 `--commit <SHA>`。`codex exec review` 是同一功能在 exec 下的入口。

审查当时先不要让它改代码。确认哪些发现要处理，再回到主会话做下一轮修改。怎么写一份可审查的结论，见 [高质量 Code Review](../05-Git协作与代码审查/06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md)。

## 留交接记录

官方没有规定一个名叫 `HANDOFF.md` 的文件，Codex 也不会自动去读它。暂停前留一份笔记，是为了下一次的人或下一条会话不用从整段记录里翻。笔记至少写清：当前目标、已经完成的、还没解决的、下一步、已知风险。状态分开写，避免「做完了」把提交和上线也包进去：

```markdown
## 当前状态

- 本地修改：已完成
- 测试：已通过指定命令
- 提交：未创建
- 远端：未推送
- 部署：未开始
```

下次继续时，先读这份笔记，再核对文件和 `git status`。笔记和现场不一致的地方，以仓库为准。要换一条会话把上下文交出去，用 [跨会话协作](./02-Codex跨会话协作功能.md) 里的交接方式，而不是只复制这一段。

## 和 Goal、多任务线、Subagents 三篇怎么分工

| 你要解决的事 | 看哪篇 |
|---|---|
| 这一条长任务里，主会话、插问、并行只读、审查、交接各放哪 | 本文 |
| `/goal` 怎么写完成标准、怎么暂停、怎么并行 | [Goal 模式](./08-Codex使用Goal模式运行长任务.md) |
| 子 agent 的内置角色、TOML、并发和审批细节 | [Subagents](./09-Codex使用Subagents并行处理任务.md) |
| `resume`、`fork`、归档、会话命名 | [管理多条任务线](./03-CodexCLI管理多条任务线.md) |
| 目标还模糊，想先出计划 | [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md) |
| 整段上下文已经不值得续，要开新会话交接 | [跨会话协作](./02-Codex跨会话协作功能.md) |

一套可以用的顺序：主会话写上结果、约束和验证；插问用 `/side`；只把边界已经稳定的只读工作交给子 agent；主会话收摘要并完成修改；用 `/review` 或 `codex review` 看差异；暂停前写交接，继续前再对一次 Git 状态。

## 旧截图

改写前，本文有 6 张桌面端截图，放在 `图片素材/11-自动化与高级工作流/05-Codex长任务工作流/`。2026-11-05 逐张对照现行文档后撤下，文件已删除：

- `01-推理强度选项.png`：画面是推理强度多选，不是长任务的步骤。当前 Subagents 文档列出的档位是 Light、Medium、High、Extra High、Max，以及符合条件时的 Ultra。图上框出的「最高」对不上这组名称。
- `02-Quick-Chat入口.png`、`03-Quick-Chat结论回传.png`：按钮是「快速聊天」「添加到聊天」。现行 Long-running work 和命令文档没有把 Quick Chat 写成步骤。
- `04-Side-Chat命令.png`、`06-任务菜单打开Side-Chat.png`：能看出 `/side` 和「打开侧边聊天」。本环境没有桌面端，无法在 2026-11-05 对照菜单文案和快捷键。命令行为改由官方命令文档说明。
- `05-选中文字打开Side-Chat.png`：选中的句子是「残血版 Codex，这 8 个隐藏功能一定要开」，不适合留在知识库正文里。

没有用新图替代。桌面端菜单以你当前的 App 为准。

## 参考资料

- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands)
- [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog)（CLI 0.166.0）
