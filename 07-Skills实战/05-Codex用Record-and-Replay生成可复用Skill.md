---
id: codex-record-replay-skill
title: Codex 用 Record & Replay 录制可复用 Skill（2026-11 更新）：官方入口、录制步骤和 macOS 前提
seo_title: Codex Record & Replay：在 Mac 上录一次操作生成 Skill
description: Record & Replay 把你在 Mac 上演示的一次操作整理成可重复使用的 Skill。本文按官方文档更新入口、录制和停止的步骤，说明 macOS 与 Computer Use 两个前提，以及管理员如何关闭。
lede: 步骤稳定、用嘴说不清的桌面流程，可以在 Mac 上录一次。入口在 Plugins 的加号菜单里，不在插件列表中搜索一个叫 Record & Replay 的插件。
url: /guides/codex-record-replay-skill
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-19
date_modified: 2026-11-03
official_ref: https://learn.chatgpt.com/docs/extend/record-and-replay
keywords: [Codex Record and Replay, Codex 录制 Skill, Record a skill, Codex 自动生成 Skill, Codex Computer Use]
related: [create-codex-skill, codex-computer-use-desktop-apps, plugin-development-marketplace]
faq:
  - q: 入口在哪里？
    a: 在 ChatGPT 桌面端选中 ChatGPT 并打开 Work，或者选中 Codex，然后打开 Plugins，点加号菜单，选择 Record a skill。不是在插件列表里搜索一个名为 Record & Replay 的插件。
  - q: Windows 或 Linux 能录吗？
    a: 官方 Record & Replay 页写明目前只在 macOS 上提供，并且 Computer Use 必须可用、已启用。Linux 预览的桌面端文档还写了 Computer Use 尚未在 Linux 上提供。
  - q: 管理员能关掉吗？
    a: 可以。组织用 requirements.toml 管理 Codex 时，把 [features].computer_use 设为 false，Computer Use 和 Record & Replay 会一起不可用。
  - q: 录出来的 Skill 能直接发给同事安装吗？
    a: Record & Replay 适合自己先得到一份草稿。要发给团队、捆绑多个 Skill、带上连接器或 MCP，官方建议按插件来打包。见 Build plugins。
---

# Codex 用 Record & Replay 录制可复用 Skill（2026-11 更新）：官方入口、录制步骤和 macOS 前提

> 本文在线版：[codexguide.io/guides/codex-record-replay-skill](https://codexguide.io/guides/codex-record-replay-skill)

> 核对依据：OpenAI 文档 [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)（2026-11-03 抓取）。旧文把入口写成“在插件列表里找到 Record & Replay”，与这篇文档不一致，这里已改成文档中的加号菜单。旧文配的 6 张仿界面图已删除。本文在 Linux 上编写，没有 macOS，因此没有新的录制截图，也没有在真机上点过 Record a skill。

有一套要反复做、步骤比较稳、但很难一次写成说明的桌面操作，可以让 Codex 看你做一遍，再整理成 Skill。官方把这个功能叫 Record & Replay：在 Mac 上演示一次，ChatGPT 或 Codex 把过程收成一份以后还能用的 Skill。

文档举的例子包括：提交一笔报销、预订停车位、创建配置正确的 Issue、发布一段视频、下载一份定期报表。生成之后，可以交给当前环境里的 Computer Use、浏览器操作、已安装的插件，或几样一起用。

已经知道目录和步骤、想手写 `SKILL.md`，看 [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)。Record & Replay 适合“做一遍比写一遍更快”的情况。

## 适合录什么

文档的前提是：你自己已经会做完这套流程，步骤稳定，成功标准清楚。

录之前先想好三件事，文档也建议在开始前说出来：

- 这次的目标。
- 每次会变的输入，例如要上传的文件、Issue 标题、报表的日期范围。
- 怎样算做完。

用真实但可以公开的输入。密码、Token、客户数据和未公开的账号不要出现在录制里。录制会看到完成流程所需的操作和窗口内容，并且一直持续到你停止。停晚了，后面顺手做的事也会进记录。

## 前提：macOS 和 Computer Use

官方页的第一句是：Record & Replay 在 macOS 上提供，Computer Use 也必须可用并且已经启用。

Computer Use 本身的权限、macOS 上的屏幕录制和辅助功能，见 [Codex 使用 Computer Use 操作桌面应用](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md)。没有这些权限时，录制请求要么不出现，要么批准时失败。本文没有在 Mac 上重试这些系统弹窗。

2026-11-03 的 Record & Replay 页没有写地区限制。旧文里“初期不对欧洲经济区、英国和瑞士开放”没有留在这篇更新里。那句话如果来自更早的发布说明，以当前这页为准：现在的文档只写了 macOS 和 Computer Use。

## 入口：Plugins 的加号菜单

文档里的起点是 ChatGPT 桌面端，不是一条 CLI 命令。

1. 在切换器里选中 ChatGPT 并打开 Work，或者选中 Codex。
2. 打开 Plugins。
3. 打开 **+** 菜单。
4. 选择 **Record a skill**。
5. 看一遍建议的提示词，补上有用的上下文，再提交。
6. 对话请求录制权限时，你准备好演示再批准。

旧文写的是“打开 Plugins，找到 Record & Replay”。那和上面的菜单路径不一致。2026-11-03 的文档没有一个要先搜索、再安装的 Record & Replay 插件条目。

本文没有 macOS 桌面截图。需要界面证据时，应在 Mac 上从 Plugins 的加号菜单截到 **Record a skill** 这一项，并打掉账号、邮箱和对话内容。在补上那张图之前，以文档的六步为准。

## 录制：授权、操作、停止

批准之后，在 Mac 上把流程做完。文档的建议是短，并且做完整。

停止方式有三种，用哪一种都可以：

- 从菜单栏停止。
- 从浮层停止。
- 直接告诉对话你已经做完。

录制在你停止之前不会自己结束。做完目标里的最后一步就停，不要接着去关无关窗口或收拾桌面。

停止之后，ChatGPT 或 Codex 查看抓到的流程并起草 Skill。文档写明，这份 Skill 会说明：什么时候用这套流程、需要哪些输入、按什么步骤做、怎样验证结果。你还可以要求它再改一版。

录制看不出你没说出口的习惯，例如字段默认值、命名规则、某个判断点。草稿出来后把这些补进 Skill，并检查有没有把只属于这一次的文件名、日期写成了固定步骤。

## 重放

新开一个 ChatGPT 或 Codex 对话，让它使用刚生成的 Skill，并给出这一次不同的值：要上传的文件、要创建的 Issue、报表的日期范围。

文档说，产品把 Skill 当作这次任务的可复用上下文，再用当前环境里可用的工具去完成，包括 Computer Use、浏览器操作和已安装的插件。换一台没有这些能力的环境，Skill 文本还在，操作不一定能做完。

重放前先读草稿里的验证标准。和手写 Skill 一样，生成的步骤不是已经测过的保证。第一次重放用无害数据，看它是否停在你写明的完成条件上。

## 管理员怎么关闭

组织用 `requirements.toml` 管理 Codex 时，`[features].computer_use` 同时管着 Record & Replay。文档写明：`computer_use = false` 会让 Computer Use 和 Record & Replay 都不可用。

```toml
[features]
computer_use = false
```

这是管理员的强制配置，和个人在设置里关掉某一项权限不是同一层。个人侧的屏幕录制、辅助功能和允许的应用列表，仍以 [Computer Use](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md) 那篇为准。

## 和手写 Skill、插件的区别

| | Record & Replay | 手写 Skill | 插件 |
| --- | --- | --- | --- |
| 怎么来的 | 在 Mac 上演示一次，由产品起草 | 自己写 `SKILL.md` | 把 Skill、连接器、MCP 打成可安装的包 |
| 适合 | 步骤稳定、更好演示 | 目录和验收已经清楚 | 要分发给别人或长期维护 |
| 官方页面 | [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) | [从零创建](./04-从零创建Codex-Skill.md) | [插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md) |

官方 “When to build another plugin” 一节写的是：Record & Replay 用来从一次演示快速得到 Skill。若要跨团队分发一份稳定的包、捆绑多个 Skill、放入连接器、添加 MCP 服务器，或管理安装元数据，把这套流程打包成自己的插件。演示稿可以当草稿，插件是以后要安装和更新的那一份。

## 常见问题

**菜单里没有 Record a skill。** 先确认是 macOS 上的 ChatGPT 桌面端，并且当前是 ChatGPT 的 Work 或 Codex。再确认 Computer Use 可用。组织下发了 `computer_use = false` 时，文档说两个功能都会消失。

**录出来的步骤太长。** 文档建议演示保持短而完整，并在开始前说明目标和会变化的输入。停晚了，无关动作会留在记录里。可以要求它按你补上的偏好改一版草稿。

**想在 Windows 上录。** 当前这页只写 macOS。Windows 上的 Computer Use 是另一件事，不能从这篇文档推出 Record & Replay 已经支持 Windows。

## 下一步

手写和 `$skill-creator` 的路径见 [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)。录制依赖的桌面操作权限见 [Computer Use](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md)。草稿要变成别人能安装的包时，再看 [插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。

## 参考资料

- [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)
- [Computer Use](https://learn.chatgpt.com/docs/computer-use)
- [Agent Skills](https://learn.chatgpt.com/docs/build-skills)
- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
