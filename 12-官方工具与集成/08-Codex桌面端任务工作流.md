---
id: codex-desktop-task-workflow
title: Codex 桌面端任务工作流（2026-10 更新）：在 ChatGPT 桌面应用里用项目、并行对话、审查和定时任务
seo_title: Codex 桌面端任务：项目、并行对话、审查与定时任务
description: Codex 在 ChatGPT 桌面应用里使用，支持 macOS、Windows 和 Linux。本文按官方文档整理选项目或文件夹、并行开对话、Plan 与 Goal、审查改动、通知和定时任务，并说明它和设置篇怎么分工。
lede: 桌面端现在是 ChatGPT 应用里的 Codex。这篇只讲任务怎么往下做；权限、个性和自定义指令放在设置篇。
url: /guides/codex-desktop-task-workflow
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-20
date_modified: 2026-10-31
verified_on: 2026-10-31
models: [gpt-6.1-sol]
official_ref: https://learn.chatgpt.com/docs/app
keywords: [Codex 桌面端, ChatGPT 桌面应用 Codex, Codex 项目与对话, Codex 并行任务, Codex 桌面端工作流]
related: [codex-automations-scheduled-tasks, codex-appshots, codex-goal-mode-long-running-work]
howto: false
faq:
  - q: 还要单独下载一个只含 Codex 的桌面版吗？
    a: 不用。官方文档写的是安装 ChatGPT 桌面应用，登录后在应用里选择 ChatGPT 或 Codex。下载页列出 macOS、Windows 和 Linux。
  - q: 这篇和桌面端协作设置那篇怎么分？
    a: 设置篇讲入口、自定义指令、个性、权限和追问怎么排队。这篇讲选工作位置、并行对话、Plan 和 Goal、审查、通知和定时任务。
  - q: CLI 和 IDE 里能管理定时任务吗？
    a: 官方写明不能。创建和管理在 ChatGPT 网页或桌面应用的 Scheduled 里。CLI 和 IDE 适合先把提示词、Skill 或工作区改动试出来。
---

# Codex 桌面端任务工作流（2026-10 更新）：在 ChatGPT 桌面应用里用项目、并行对话、审查和定时任务

> 本文在线版：[codexguide.io/guides/codex-desktop-task-workflow](https://codexguide.io/guides/codex-desktop-task-workflow)

> 核对依据：2026-10-31 的官方文档 [ChatGPT desktop app](https://learn.chatgpt.com/docs/app)、[Projects and chats](https://learn.chatgpt.com/docs/projects)、[Long-running work](https://learn.chatgpt.com/docs/long-running-work)、[Code review](https://learn.chatgpt.com/docs/code-review)、[Notifications](https://learn.chatgpt.com/docs/notifications)、[Scheduled tasks](https://learn.chatgpt.com/docs/automations)、[Plugins](https://learn.chatgpt.com/docs/plugins)。本文没有运行桌面应用，没有新截图。旧文里 2026 年 8 月独立 Codex 桌面版的截图已经删除，那些界面不能再当作当前步骤。

Codex 的桌面用法，是在 ChatGPT 桌面应用里选 Codex，而不是再装一个单独的 “Codex 桌面版”。官方开始步骤是：安装应用，登录，选择工作位置，发送第一条消息。下载页写的是 macOS、Windows 或 Linux。

应用里可以选择 ChatGPT 或 Codex。选了 ChatGPT 之后，输入框上方还可以在 Chat 和 Work 之间切换。选了 Codex 之后，从 New chat 开始。临时问题可以指向 New chat，再点它右侧的 Quick chat 图标。

权限、个性、自定义指令和追问是排队还是立刻打断，写在 [Codex 桌面端协作设置](../10-配置模型与权限安全/02-Codex桌面端协作设置.md)。这篇不重复那些开关，只讲一件任务从哪里开始、怎么并行、怎么验收。

## 选工作位置

官方把工作位置分成几类。

**ChatGPT 项目。** 适合会持续做、会产出多份结果、或者要共用同一批文件和说明的工作。项目里有 Chats 和 Sources。项目说明对其中的对话都生效。这种项目不能直接读电脑上的文件夹，需要的材料要上传或连接进来。

**本地项目。** 给对话访问电脑上的一个或多个文件夹，例如一份代码库。添加或修改文件夹：打开项目菜单，选 Edit project，用 Add folder 挂上多个文件夹。每个挂上的文件夹，ChatGPT 都可以读和改。把其中一个标成 Make primary，新对话就从主文件夹开始。Codex 也用主文件夹做 Git 操作，并在这里自动发现 `AGENTS.md`、skills 和 `config.toml`。次要文件夹仍可搜索、阅读和编辑，但不会自动发现那些项目文件。远程项目目前只支持一个文件夹。

无关的工作拆成不同项目，避免每个对话都能碰到整个仓库。审查窗可以显示同一项目里多个仓库的改动。Pull request 和 worktree 操作针对主仓库。在 worktree 里开始的对话，其他文件夹仍然挂着。

项目和 worktree 只负责把工作分开。命令能读什么、改什么、能不能上网，仍由沙箱决定。

**不建项目。** 在 Codex 里，Recents 旁边的 New chat 可以不带项目开始。适合一次性、不需要共享项目文件和说明的工作。

**Quick chat。** 打开的是普通 ChatGPT 对话，不会出现在 Codex 侧栏。快捷键是 macOS 的 Cmd+Option+N，Windows 和 Linux 的 Ctrl+Alt+N。

CLI 和 IDE 没有桌面应用这份 Projects 视图。CLI 把启动目录当作项目，也可以用 `codex --cd`。IDE 把当前打开的文件夹或工作区当作项目。

## 并行处理多个任务

官方的做法是：一个明确结果开一个对话。项目负责把相关对话放在一起，每个对话保留自己的记录。

可以同时跑多个对话。不要让两个对话同时改同一批文件。写代码时，用 worktree 给并行对话各自一份检出。Goal 的并行规则相同：每个对话有自己的目标和结果。细节见 [Codex Goal 模式](../11-自动化与高级工作流/05-Codex使用Goal模式运行长任务.md)。

把相关对话留在侧栏里的办法，文档写的是：

- 固定项目，或从 Projects 视图固定。
- 固定经常回去的对话。
- 用结果来命名，例如 “Checkout accessibility review”。
- 在 Projects 视图里搜索项目。从侧栏打开 Search chats，按一句原话或分支名找旧对话。Search chats 没有默认快捷键，可以在 Settings > Keyboard Shortcuts 里指定。
- 做完后归档对话。项目菜单里的 Archive chats 会把该项目的对话一起归档。

固定只改变侧栏位置，不增加上下文，也不改变 Codex 能访问的文件。已归档的对话从 Settings > Archived chats 恢复。同一篇文档的另一段把恢复路径写成 Settings > Data Controls > Archived chats。两处措辞不一样，以你当前版本的设置页为准。

## Plan 模式和 Goal

长任务先写清结果、约束和怎样算做完。相关步骤留在同一个对话里，Codex 才能用同一份上下文决定下一步，以及何时停止。

官方文档写明，在桌面应用、Codex CLI 和 IDE 扩展里都可以输入 `/goal`。目标文本既是第一条提示，也是完成标准。

结果还不清楚时，先用 `/plan`，让它问你问题、列出约束，再收成一条带可检查标准的目标，然后用 `/goal` 开始。

完成标准尽量包含三样：

| 要素 | 写什么 |
|---|---|
| 结果 | 要得到的东西，而不是只写“去改一下” |
| 约束 | 必须用的工具、不能动的边界、兼容要求 |
| 验证 | 测试、测量或审查标准 |

桌面应用里，目标进度条在输入框上方，可以暂停、继续、编辑或清除目标。运行中也可以再发消息补充约束。想看进度解释、又不打断主对话时，用 side chat。预计要断网时先暂停，恢复后再继续。

开始 Goal 不会放宽权限。沙箱和审批策略保持原样，需要决定时会停下来。

本地长任务可以在设置里打开 Prevent sleep while running。文档这句话写的是让 Mac 保持清醒。通知或桌宠用来看对话是否在等输入、是否可以审查。

## 审查改动

本地改动用应用里的审查窗。官方写明，审查窗反映的是 Git 仓库的状态，不限于 Codex 刚改的文件，也包括你自己和其他未提交的改动。项目还不是 Git 仓库时，应用会提示先建仓库。

默认看的是 Unstaged changes。还可以切换：

| 范围 | 看什么 |
|---|---|
| Staged | Git 暂存区 |
| Commit | 某一次提交 |
| Branch | 相对基线分支的差异 |
| Last turn | 最近一轮助手的改动 |

多个文件夹属于不同 Git 仓库时，审查标题栏可以切换仓库。Last turn 可以选择 All repos。Unstaged、Staged、Branch 作用在你选中的那个仓库。

在输入框输入 `/review`，可以选择相对基线分支审查，或审查未提交的改动。Codex 会给出按优先级排列的发现，并且不修改工作区。

行内评论：在审查窗里悬停一行，点出现的加号，写下意见，再发一条消息说明意图，例如要求按这些评论做最小修改。评论本身是审查意见，跟一条消息 Codex 才会去处理。

暂存和还原可以作用在整份 diff、单个文件或单个 hunk。满意的部分暂存，不要的部分还原。同一个文件同时有暂存和未暂存的改动时，审查窗两边都会出现，这是 Git 的正常状态。

点击文件名通常会在你选定的编辑器里打开。按住 Command 再点一行，会打开那一行。默认编辑器在开发者设置里选。

设置里还可以把 `/review` 改成 Detached，让审查另开一个对话。路径是 Settings > General > Code review。

Pull request 用 Code Review 插件，和本地 `/review` 不是同一个入口。插件可以看描述、改动、评论和检查。GitHub 代码审查已正式提供。GitLab 合并请求支持在文档里标为预览。桌面应用自带 Code Review，可以从已安装插件把它固定到侧栏。在对话里审查不会自动在 GitHub 上发评论或合并，要你自己选择提交。

## 通知和长任务跟进

[Notifications](https://learn.chatgpt.com/docs/notifications) 写明，桌面通知在设置里选择：从不提示、只在 ChatGPT 在后台时提示，或总是提示。权限请求和提问可以单独开关。操作系统可能会再要一次通知权限。

Activity 可用时，侧栏的铃铛列出未读、正在跑、或在等你回复的对话。快捷键是 macOS 的 Cmd+Option+U，Windows 的 Ctrl+Alt+U。筛选可以包括 Work、Chat、Pinned 和 Scheduled，视当前界面而定。

macOS 上的浮动桌宠也可以在你使用其他应用时显示 Running、Needs input、Ready 或 Blocked。把窗口拍进对话用的是 Appshots，见 [Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)。

IDE 扩展没有单独的通知开关。要在回合结束时跑外部程序，在连接的 Codex 主机上配置 `notify`。

## 定时任务入口

侧栏里的 Scheduled 是定时任务的收件箱。有发现的运行会出现在这里，未读标记表示需要看。

官方文档现在的名称是 Scheduled tasks。创建和管理在 ChatGPT 网页或桌面应用里。CLI 和 IDE 扩展都没有这份管理界面，只适合先试提示词、Skill 或工作区。

桌面应用里，定时任务可以针对本地项目，跑在项目目录或隔离的 worktree 里。需要读本地文件时，电脑要开着，应用也要开着。Git 仓库可以选择本地目录或新 worktree。worktree 把定时改动和你正在改的文件分开。直接跑在本地项目里时，它可能改到你还在编辑的文件。没有版本控制的项目，任务直接跑在项目目录。

两种用法：

- 独立任务：每次运行新开一个对话，结果进 Scheduled。适合各次互不依赖，或一个任务要扫多个项目。
- 对话内任务：回到同一个对话，带着已有上下文。适合盯住一次还没结束的操作，或按固定节奏继续审查。

自定义周期可以编辑 RFC 5545 的 RRULE，文档举例是 `RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`。

事件触发（Gmail、Slack、GitHub）在网页和移动端的符合条件套餐上提供。文档写明桌面应用、CLI 和 IDE 扩展都不能用事件触发。

定时任务无人值守，使用你的默认沙箱。文档建议从能完成任务的最小权限开始。组织若禁止 `approval_policy = "never"`，任务会退回你所选权限模式的审批行为。

如果已有定时任务还指向 GPT-5.5，官方写明要改成套餐和工作区提供的 `gpt-6.1-sol`（GPT-6.1 Sol）。这条退役适用于用 ChatGPT 登录的 Codex。用 API 密钥的会话不在这条之内。

创建、worktree 和 `codex exec` 的分工，见 [Codex 定时任务](./06-Codex-Automations定时任务.md)。

## 插件和 Skill 从哪里装

官方插件文档写明：插件可以在 ChatGPT 网页、桌面和移动端的 Chat 与 Work 里用，也可以在桌面应用的 Codex 里用。Codex CLI 有插件浏览器，命令是在会话里输入 `/plugins`。IDE 扩展不支持插件。

桌面应用打开 Plugins 标签安装。装完后新开一个对话，插件带上的 Skill 和 MCP 工具才会出现。点名插件或 Skill 时，ChatGPT 的输入框文档写的是 `@`。Codex 里官方 Skills 文档写的是 `$` 或 `/skills`。

第三方 Skill 包要用 CLI 的 marketplace 命令安装时，按那个仓库自己的说明做，并新开会话。一个例子是 [安装 agent-skills 插件](../09-MCP与外部工具/09-Codex安装agent-skills插件-25个工程Skill怎么用.md)。不要把某次旧界面里的 Skill Installer 按钮当成现在的唯一入口。那套截图已经不在本文里。

## 和设置篇的分工

| 你要做的事 | 看哪篇 |
|---|---|
| 选 ChatGPT 还是 Codex、写自定义指令、调个性、收紧权限、决定追问是否排队 | [桌面端协作设置](../10-配置模型与权限安全/02-Codex桌面端协作设置.md) |
| 选项目或文件夹、并行开对话、写 Goal、审查 diff、看通知、建定时任务 | 本文 |
| 把别的应用窗口拍进对话 | [Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md) |
| 定时任务的 RRULE、worktree 和 cron 分工 | [定时任务](./06-Codex-Automations定时任务.md) |

## 常见问题

**Linux 能用这套桌面流程吗？** 官方下载步骤包含 Linux。Appshots 那一页只写了 macOS 和 Windows，不要把 Appshots 的快捷键用到 Linux 上。定时任务需要本地文件时，同样要求电脑和应用保持打开，文档没有把 Linux 排除在桌面应用之外。

**旧文说定时任务只有桌面版才有，CLI 完全不能参与。** 管理界面确实不在 CLI 和 IDE 里。CLI 仍可以先把提示词和 Skill 试出来，也可以用 `codex exec` 配系统的计划任务。两条路的差别见定时任务那篇。

**审查窗里的文件和我自己改的混在一起。** 这是文档里的设计。它显示仓库里的未提交状态，不只显示 Codex 的编辑。用 Last turn 看最近一轮，或先暂存你要保留的部分。

## 下一步

长任务的完成标准写得更细，看 [Codex Goal 模式](../11-自动化与高级工作流/05-Codex使用Goal模式运行长任务.md)。权限开关回到 [桌面端协作设置](../10-配置模型与权限安全/02-Codex桌面端协作设置.md)。

## 参考资料

- [OpenAI：ChatGPT desktop app](https://learn.chatgpt.com/docs/app)
- [OpenAI：Projects and chats](https://learn.chatgpt.com/docs/projects)
- [OpenAI：Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [OpenAI：Code review](https://learn.chatgpt.com/docs/code-review)
- [OpenAI：Notifications](https://learn.chatgpt.com/docs/notifications)
- [OpenAI：Scheduled tasks](https://learn.chatgpt.com/docs/automations)
- [OpenAI：Plugins](https://learn.chatgpt.com/docs/plugins)
