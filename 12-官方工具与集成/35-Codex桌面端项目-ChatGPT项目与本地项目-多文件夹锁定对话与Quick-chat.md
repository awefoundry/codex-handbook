---
id: codex-desktop-projects
title: "Codex 桌面端项目怎么用：ChatGPT 项目和本地项目的区别，一个项目接多个文件夹、锁定对话与 Quick chat"
seo_title: "Codex 桌面端项目：ChatGPT 项目、本地文件夹与 Quick chat"
description: "ChatGPT 桌面端的 Projects 同时放 ChatGPT 项目和连接本机文件夹的本地项目。本文按官方文档说明两者的区别、多文件夹、锁定对话、Quick chat，以及 CLI 和 IDE 里的项目指什么。"
lede: "会持续做、要共用同一批文件时再建项目。一次性的问题可以直接开对话，或者用 Quick chat。"
url: /guides/codex-desktop-projects
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [Chat, App, CLI, IDE]
difficulty: 基础
order: 35
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-25
date_modified: 2026-11-25
verified_on: 2026-11-25
tested_cli_version: 0.172.0
official_ref: https://learn.chatgpt.com/docs/projects
keywords: [Codex 项目, Codex Projects, Codex 本地项目, Codex 桌面端项目文件夹, Codex Quick chat]
related: [codex-desktop-task-workflow, da-kai-di-yi-ge-ben-di-xiang-mu, worktree-parallel-chats]
howto: true
faq:
  - q: "ChatGPT 项目能直接读我电脑上的文件夹吗？"
    a: "官方文档写不能。ChatGPT 项目要使用的材料，需要上传或连接。能读写本机文件夹的是桌面端的本地项目。"
  - q: "CLI 里有没有 Projects 视图？"
    a: "没有。Codex CLI 把启动它的目录当作这个对话的项目，也可以用 --cd 或 -C 指定。2026-11-25 的 codex-cli 0.172.0 帮助里，-C/--cd 写的是把该目录用作工作根。"
  - q: "锁定对话之后，它还在原来的项目里吗？"
    a: "不在。官方写明，锁定会把对话移出项目，因此不再使用项目说明、项目文件或记忆。Unlock chat 恢复的是普通历史。"
  - q: "一个项目可以挂几个文件夹？"
    a: "桌面端文档写可以用 Add folder 挂多个文件夹，并把其中一个标成 Make primary。远程项目目前只支持一个文件夹。次要文件夹可以读和改，但不会自动发现 AGENTS.md、skills 和 config.toml。"
---

# Codex 桌面端项目怎么用：ChatGPT 项目和本地项目的区别，一个项目接多个文件夹、锁定对话与 Quick chat

> 本文在线版：[codexguide.io/guides/codex-desktop-projects](https://codexguide.io/guides/codex-desktop-projects)

> 核对依据：2026-11-25 打开的官方文档 [Projects and chats](https://learn.chatgpt.com/docs/projects)。CLI 的 `--cd` / `-C` 对照的是同一天 Linux 上 `codex-cli 0.172.0` 的 `codex --help`。没有安装或打开 ChatGPT 桌面应用，没有打开 IDE，没有配图。按钮和菜单名用文档里的英文原文。

桌面端里一次任务怎么并行、怎么审查、怎么做定时任务，见 [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)。第一次把练习目录交给 Codex，见 [第 3 课：打开第一个本地项目](../01-安装与首次使用/08-打开第一个本地项目.md)。几个任务要各自一份检出，见 [用 Worktree 并行运行多个任务](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md)。

## 先说结论

官方文档按入口把「项目」说成不同的东西。

- **桌面应用**里有 **Projects** 视图，同时放 ChatGPT 项目，和连接本机文件夹的本地项目。
- **网页**上的项目把相关对话、文件、说明和来源放在一起。ChatGPT 项目不能直接读电脑上的文件夹。
- **CLI** 把你启动它的目录当作这个对话的项目，不提供 Projects 视图。
- **IDE 扩展**把当前打开的文件夹或工作区根当作本地项目，也不提供网页或桌面端那份 Projects 视图。

会持续一段时间、会产出不止一份结果、或者要反复用同一批文件和来源时，再建项目。工作本身是独立的、不需要共享项目上下文时，直接开一个对话。

## ChatGPT 项目和本地项目

文档把这两类都放在桌面端的 **Projects** 视图里，但它们能碰到的材料不一样。

**ChatGPT 项目**带着项目文件和上下文，跨相关对话使用。网页上的同一篇说明写得更具体：每个项目有 **Chats**，列出项目里的对话；有 **Sources**，放上传的文件和连接进来的上下文。项目说明对其中的对话都生效。同一个项目里可以有用 Chat 开始的对话，也可以有用 ChatGPT Work 开始的对话。ChatGPT 项目不提供对本机文件夹的直接访问，要用的材料需要上传或连接。

**本地项目**让对话访问电脑上的一个或多个文件夹，例如一组源码或一个代码库。文档写，ChatGPT 可以读和改每一个挂上的文件夹。

两边都建议：一个明确的结果开一个单独的对话。这样消息和结果保持集中，项目只负责把相关工作放在一起。

## 新建本地项目，并接上多个文件夹

文档写：项目不是必须有文件夹，但可以按需要挂上。要在已批准的项目文件夹里继续跨设备的 Work，先等工作区打开本地电脑访问，再开始一条新的云端任务，并且让放着文件夹的那台电脑保持在线。同步对话不会把整个本地文件夹上传到另一台电脑。继续任务时，要看它当时能访问哪些来源和工具。Work 的对话历史和 Codex 的历史是分开的。

添加或更换文件夹：打开项目菜单，选择 **Edit project**。选择 **Add folder** 可以挂多个文件夹。要改默认工作目录，指向一个文件夹，再选择 **Make primary**。

新对话从主文件夹开始。Codex 也用这个主文件夹做 Git 操作，并在这里自动发现 `AGENTS.md`、skills 和 `config.toml`。次要文件夹仍然可以搜索、阅读和编辑，但 Codex 不会从次要文件夹自动发现这些项目文件。

多个文件夹适合相关材料本来就不在一个地方，例如一个应用和它的文档，或一个网站和它的后端。不相关的工作，或者每个对话只应该碰到仓库的一部分时，拆成不同的项目，让工作上下文保持集中。远程项目目前只支持一个文件夹。

审查窗可以显示挂在同一项目上的多个仓库的改动。Pull request 和 worktree 操作针对主仓库。在 worktree 里开始的对话，其他文件夹仍然挂着。项目和 worktree 负责把工作组织开；本地命令能读什么、改什么、能不能访问网络，由沙箱决定。

本地环境用来给项目定义准备动作和常用命令。本文没有创建本地环境。

2026-11-25 没有桌面应用，所以上面的 **Edit project**、**Add folder**、**Make primary** 是文档里的菜单名，不是这次点出来的按钮。

## 在项目里工作

文档的做法是一个结果一条对话。

桌面端：ChatGPT 项目跨对话携带文件和上下文；本地项目让对话访问文件夹。每个对话保留自己的消息和结果。

网页：从项目里新开对话，才能用它共享的文件和说明，然后再回到 **Chats** 下面找到它。Chat 适合短对话，ChatGPT Work 适合更大的交付物，两者都出现在项目的 **Chats** 里。

CLI：在应该提供文件上下文的目录里启动 Codex。用 `/new` 为每个不同的结果另开一个对话。Codex 还开着时用 `/resume`，或者在终端运行 `codex resume`，继续一条已保存的对话。对话保留记录和当时记下的工作目录，Codex 读取的是当前工作树里的文件。长期有效的项目说明放在 `AGENTS.md` 或纳入版本管理的文档里，后面的对话才能看到。

IDE：打开应该提供文件上下文的文件夹或工作区。每个不同的结果新开一个对话，之后从 **Recent chats** 里选回来。同一项目里的对话可以使用同一批文件，每条对话保留自己的记录。当前选中的内容和打开的文件，为这一轮提供上下文。长期说明同样放在 `AGENTS.md` 或纳入版本管理的文档里。

## 整理项目和对话

桌面端文档列出的整理动作：

- **Pin a project**：把项目固定在侧栏靠上的位置。也可以从 Projects 视图固定。
- **Pin a chat**：经常要回去的对话可以固定，即使项目里已经有更新的对话。
- **Rename a chat**：用短标题写出结果，文档的例子是 “Q3 launch brief” 和 “Checkout accessibility review”。
- **Search projects**：在 Projects 视图里搜索项目。从侧栏打开 **Search chats**，在记得一句原话或分支名、但不记得标题时找旧对话。Search chats 没有默认快捷键，可以在 **Settings > Keyboard Shortcuts** 里指定。
- **Archive a chat**：做完就归档。从项目菜单选择 **Archive chats**，可以把该项目的对话一起归档。

固定不增加上下文，也不改变 ChatGPT 能访问什么，只改变项目或对话在侧栏里的位置。

桌面端恢复已归档对话的路径是 **Settings > Archived chats**。

网页上的整理动作同样有固定项目、固定对话、重命名和归档。搜索旧对话的快捷键写成 <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>K</kbd>。网页恢复已归档对话的路径是 **Settings > Data Controls > Archived chats**。

这两条恢复路径都写在同一篇 Projects 文档里，分别属于桌面端和网页。不要合成一条。2026-11-25 没有打开这两个设置页。

## 锁定对话

文档把 **Use locked chats** 放在桌面端和网页共用的一节。锁定对话不进入普通历史和搜索。要用时，用账户 PIN 临时打开。

文档举的例子是：还没准备讨论的职业变动、一场难谈的对话、要保密的礼物或庆祝。

可以锁定的是符合条件的云端 Chat 和 Work 对话。本地的 Work 和 Codex 对话不支持。

文档写的步骤：

1. 打开对话的更多菜单（…），选择 **Lock chat**，确认，然后创建或输入账户 PIN。
2. 进入 **Projects > Locked chats**，输入 PIN，获得临时访问。
3. 结束时选择 **Lock now**。共享屏幕之前检查其他设备；在那些设备上刷新 ChatGPT 之前，标题或内容可能仍然可见。

锁定一个项目里的对话，会把它移出项目，因此不再使用项目说明、项目文件或记忆。**Unlock chat** 恢复普通历史。

忘记 PIN 时，重置 PIN 会永久删除由该 PIN 保护的锁定对话和内容。

可用性、分享、文件、记忆和 PIN 设置，文档指向帮助中心 [Using locked chats](https://help.openai.com/en/articles/20001411-using-locked-chats-in-chatgpt)。本文没有打开那一页的全部条款，也没有创建 PIN。

## 不建项目，以及 Quick chat

桌面端：在 Codex 里，**Recents** 旁边选择 **New chat**，可以不带项目开始。适合不需要共享项目文件、说明或文件夹的一次性工作。几个对话都要依赖同一份上下文时，先建项目。

网页：不需要共享项目文件、说明或来源时，从 ChatGPT Home 开始。可以用 Chat，也可以用 ChatGPT Work；在网页上两者都会创建对话。工作变大之后，再移进项目，并用清楚的对话名区分每个结果。一个项目可以并行放研究、起草、审查和跟进，而不必把所有消息塞进同一段上下文。

**Quick chat** 写在桌面端。它打开的是普通 ChatGPT 对话。ChatGPT 对话不出现在 Codex 侧栏里；Codex 侧栏放的是 Codex 对话和项目。

用法：指向 **New chat**，再选择它右侧的 **Quick chat** 图标。也可以按 macOS 的 <kbd>Cmd+Option+N</kbd>，或 Windows 和 Linux 的 <kbd>Ctrl+Alt+N</kbd>。从 **New chat** 还可以打开一条已有的 ChatGPT 对话，并把它加进一条 Codex 对话。

本文没有桌面应用，没有按过这些键。

## CLI 和 IDE 里的项目

Projects 文档对 CLI 的说法是：Codex CLI 把启动它的目录当作这个对话的项目。在要工作的目录里运行 `codex`，或者传入 `--cd <directory>`（`-C`）明确指定。CLI 不提供 ChatGPT 的 Projects 视图。

2026-11-25 的 `codex-cli 0.172.0` 里，`codex --help` 有：

```text
-C, --cd <DIR>
    Tell the agent to use the specified directory as its working root
```

这和文档里的 `--cd` / `-C` 对应。同一份帮助里还有 `--add-dir <DIR>`，说明是「除主工作区之外、也应可写的其他目录」。Projects 文档没有把这个旗标写成桌面端的 **Add folder**。两者都允许碰到主目录以外的路径，但文档没有说 CLI 的 `--add-dir` 会按主文件夹、次要文件夹那一套规则去发现 `AGENTS.md`。本文不把它们写成同一个功能。没有执行 `codex --cd` 去改任何仓库。

IDE 扩展把编辑器里打开的文件夹或工作区当作本地项目。多根工作区里，要为这个对话选择工作区根。扩展不提供网页或桌面端的 Projects 视图。

## 接入其他工具和上下文

文档按入口分开写，不要当成每个入口都有同一组按钮。

桌面端可以：把只和这一次请求有关的文件或图片直接附在对话上；安装插件，从其他服务带进上下文和动作；在组织或开发环境通过 MCP 暴露工具时配置 MCP；在记忆可用时，把过去工作里有用的上下文带到以后的对话。

CLI 的对应列表是图片输入、插件、MCP 和可用时的记忆。没有写「把文件拖进 Projects 视图」，因为 CLI 没有这个视图。

IDE 的对应列表是：引用打开的文件或在编辑器里选中代码，作为这一轮的上下文；配置 MCP；使用所连接 Codex 主机上可用的记忆。插件页写明 IDE 扩展不支持插件，这一节也没有把安装插件写成 IDE 的步骤。

网页上：应该跨对话使用的文件和连接来源，放进项目的 **Sources**；只和这一条对话有关的文件或图片，直接附在对话上；在 ChatGPT Work 里可以安装插件；记忆可用时同样可以使用。

## 怎样确认项目用对了

本文没有桌面应用，不能用截图代替验收。按文档可以自己核对的是：

1. 桌面端要读本机文件夹时，用的是本地项目，不是只有上传文件的 ChatGPT 项目。
2. 挂了多个文件夹时，新对话从 **Make primary** 的那个主文件夹开始。次要文件夹里的 `AGENTS.md` 不要假定会被自动发现。
3. 一个结果一条对话。项目侧栏里看得到这几条对话，不代表它们共用同一段记录。
4. CLI 用 `codex --help` 确认 `-C, --cd <DIR>` 仍在，再在你打算工作的目录启动，或显式传入该目录。
5. 锁定之后，这条对话不再留在原项目里。要它继续使用项目说明和文件时，不要锁定。

## 参考资料

- [Projects and chats](https://learn.chatgpt.com/docs/projects)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Using locked chats](https://help.openai.com/en/articles/20001411-using-locked-chats-in-chatgpt)
- [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)
- [第 3 课：打开第一个本地项目](../01-安装与首次使用/08-打开第一个本地项目.md)
- [用 Worktree 并行](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md)
