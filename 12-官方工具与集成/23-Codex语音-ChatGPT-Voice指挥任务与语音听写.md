---
id: codex-voice-chatgpt-voice
title: Codex 语音怎么用：在 ChatGPT 桌面 App 用 Voice 指挥任务、语音听写与 CLI /voice
seo_title: Codex 语音：ChatGPT Voice、听写与 CLI /voice
description: Codex 有两种语音用法。ChatGPT Voice 可以在桌面应用里开任务、查进度和改方向；语音听写只把语音转成提示词。本文按官方 Voice、Pricing 和命令文档整理入口、Screen context 和计费。没有桌面应用，没有实测。
lede: 要边说边改任务，用 ChatGPT Voice。只想把话说成一段提示词，用作曲框里的 Dictate。两者计费和入口都不一样。
url: /guides/codex-voice-chatgpt-voice
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 基础
order: 23
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-09
date_modified: 2026-11-09
verified_on: 2026-11-09
official_ref: https://learn.chatgpt.com/docs/features/voice
keywords: [Codex 语音, ChatGPT Voice, 语音听写, /voice, Screen context, GPT-Live]
related: [codex-appshots, codex-desktop-task-workflow, usage-limits-credits]
howto: false
faq:
  - q: 本文在桌面应用里用过语音吗？
    a: 没有。写作环境没有 ChatGPT 桌面应用，也没有麦克风会话。步骤、套餐和价格都来自 2026-11-09 打开的官方文档，没有配图。
  - q: 语音听写和 ChatGPT Voice 用的是同一个按钮吗？
    a: 官方把它们写成两件事。Voice 是实时对话。Prompting 页的 Dictate 把语音转写进作曲框，你可以改完再发送。
  - q: API Key 登录能开桌面语音吗？
    a: Pricing 页写明，ChatGPT Voice in Desktop 不能通过 API Key 使用。功能对照表里这两行的 API Key 列是破折号。
---

# Codex 语音怎么用：在 ChatGPT 桌面 App 用 Voice 指挥任务、语音听写与 CLI /voice

> 本文在线版：[codexguide.io/guides/codex-voice-chatgpt-voice](https://codexguide.io/guides/codex-voice-chatgpt-voice)

> 核对依据：2026-11-09 的 [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)、[Pricing](https://learn.chatgpt.com/docs/pricing) 中 “How much does Voice cost?”、[Command line options](https://learn.chatgpt.com/docs/developer-commands) 的 `/voice`，以及 [Prompting](https://learn.chatgpt.com/docs/prompting) 的 “Use voice dictation”。**本文没有 ChatGPT 桌面应用，没有 iPhone，没有麦克风，没有进入 CLI 的语音会话，也没有截图。** 0.167.0 的 `codex` 可执行文件里能搜到 `/voice`、`voice mute` 和 `voice settings` 这几段文字；这只说明该构建带有这些字符串，不能代替一次真实的 `/voice`。

官方文档把语音分成两条路。ChatGPT Voice 是一场实时对话，由 GPT-Live 驱动，可以在 ChatGPT 桌面应用的 Chat、Work 和 Codex 里开口布置任务、询问进度或改变方向。语音听写只把话说成可编辑的提示词，发送前仍由你确认。

## 哪些套餐和入口能用

[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) 写明，桌面应用里的 Voice 面向 ChatGPT Plus、Pro、Business、Edu 和 Enterprise。Enterprise 和 Edu 先有两周抢先使用，之后才默认开放。是否真的出现在你的界面上，还取决于发布进度和工作区设置。同一页写：手机上的 Codex 要先和一台桌面主机配对，才能使用 ChatGPT Voice。

Pricing 页的功能对照表中，ChatGPT Voice 和 Voice dictation 两行的 API Key 列是破折号。前面几列在抓取文本里是空单元格；同页里 Codex CLI 等行也是这种空单元格，勾选标记没有被转成文字。同一页的 Voice 问答写明：桌面语音不能通过 API Key 使用。套餐名单以 Voice 页点名的 Plus、Pro、Business、Edu 和 Enterprise 为准。

桌面应用里的项目、并行对话和任务入口见 [桌面端任务工作流](./08-Codex桌面端任务工作流.md)。本文不重复那篇的界面结构。

## 在桌面应用里开始

Voice 页的步骤是：

1. 在 ChatGPT 桌面应用里打开要讨论的 Codex 任务，或新开一段聊天、一项任务。
2. 已有任务里选择 **Start voice chat**。新的聊天或任务里选择 **Start new voice chat**。
3. 第一次使用时允许麦克风，选择一种声音，并在 macOS 上查看 screen context。
4. 开始说。结束时选择 **Stop voice chat**。

已有任务里的语音仍在分批推出。可用时，语音使用这项任务已有的对话和所选模型，所以可以接着打字开始的任务往下说。若已有任务里没有 Start voice chat，文档要求先更新桌面应用和正在跑这项任务的 Codex 主机。更新之后仍没有时，可以在支持的地方新开一场语音，或改用语音听写。要继续早先的一场语音，打开它再选 Start voice chat。

快捷键在 **Settings > Voice > Voice chat hotkey**。文档没有列出默认键位。本文没有打开这个设置页。

文档还写：整个桌面应用同一时间只能有一场语音。另一扇窗口里已经有一场时，新的会开不起来。

## 用语音开任务、查进度、换任务

Voice 页写，对话支持打断、追问和改方向。任务已经开始之后，可以继续说，用来查看进度或把工作拉回某个方向。

它还可以为较长的工作另开任务、查看已有任务，并把进度、阻塞和结果说回当前这场语音。文档给的例子是：

- 让它查看当天的发布简报，并总结需要批准的决定。
- 让它开一项 Codex 任务去跑测试，并排查没通过的部分。
- 让它查看进行中的任务，总结什么在挡住进度。

也可以要求改口到另一项 Codex 任务，再说回上一场。文档的例句是 “Let me talk to the task reviewing the tests”，然后 “Take me back to the previous task”。目标任务必须支持语音，并且在一台已连接的主机上。

这些是文档里的说法，不是本文跑出来的结果。语音遵循它在 Chat、Work 和 Codex 里所指挥的那些任务的同一套权限。权限模式见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## Screen context 和隐私

仅 macOS：在 **Settings > Voice** 打开 **Screen context**，然后说 “Take a look at this”。文档写，ChatGPT 会拍下最前面窗口的一张 appshot，用作上下文。组织可以关掉这项能力。

这张 appshot 可以包含窗口图像，以及可访问的文字，**包括滚动区域以外的文字**。macOS 可能会请求 Screen & System Audio Recording 和 Accessibility 两项权限。含有密钥、邮件、客户数据或未公开代码的窗口不要拿来做这一步。

快捷键拍摄当前窗口的 Appshots 是另一篇：[Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)。Voice 页把 “Take a look at this” 的结果也叫做 appshot。本文没有桌面应用，没有核对语音设置里的 Screen context 和 Appshots 的快捷键是不是同一个开关。若 Screen context 不可用，Voice 页要求检查 Settings > Voice、Appshots 权限和组织限制。

## 语音听写

[Prompting](https://learn.chatgpt.com/docs/prompting) 写：在桌面应用的作曲框选择 **Dictate**，然后说话。ChatGPT 把语音转写进作曲框，你检查、修改之后再发送。

听写不开始一场实时对话，也不替你改任务方向。只想把一段需求说成文字时用它。要让它边听边开工，用上一节的 Voice。

## CLI 的 /voice

[Command line options](https://learn.chatgpt.com/docs/developer-commands) 写：当所用的 CLI 构建和当前会话支持语音时，用 `/voice` 或 F8 开始或结束一场语音。`/voice mute` 开关麦克风，`/voice stop` 结束对话，`/voice settings` 为以后的对话选择声音。

文档用了 “when your CLI build and session support voice”。它没有在这一节列出最低版本号。本文在 Linux 上安装了 npm 的 `@openai/codex@0.167.0`，`codex --version` 为 `codex-cli 0.167.0`，但终端是非交互的，没有 TUI，也没有麦克风，因此没有输入 `/voice`，没有 F8，也没有 `/voice settings` 的界面。可执行文件里的字符串只能说明这个构建包含相关文字。

0.167.0 的 `codex login status` 在未登录的独立目录里输出 `Not logged in`，退出码 1。语音是否还要求 ChatGPT 登录，本文没有在支持语音的会话里验证。桌面 Voice 不能用 API Key，已见 Pricing 页；CLI `/voice` 的登录要求以你本机的命令表现为准，本文没有该项输出。

## 费用

2026-11-09 的 Pricing 页原文是：

- Voice in Desktop 按每分钟 **0.05 美元** 计入已有的 Codex 用量预算。
- GPT-Live 负责实时对话。处理任务的模型按它自己的 token 价格另外计算。语音和任务共用套餐的用量限制。
- 按 credits 计费的 Business、Edu 和 Enterprise 工作区，桌面语音是每分钟 **1.25 credits**。Plus 和 Pro 在花额外 credits 时也是这个单价。
- ChatGPT Voice in Desktop 不能通过 API Key 使用。

用量面板、5 小时窗口和 credits 的读法见 [用量额度怎么看](../10-配置模型与权限安全/08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。本文没有登录，没有 Usage 页面，没有把 0.05 美元换算成某一次任务的 token。价格以后以 Pricing 页为准。

## 开不了时先查什么

Voice 页的排查顺序是：

1. 套餐、发布进度和工作区是否已经打开 ChatGPT Voice。Enterprise / Edu 可能仍在两周抢先期内，默认开关尚未打开。
2. 麦克风权限是否已经授予桌面应用。
3. 是不是已经有另一场语音占着这台桌面应用。
4. 已有任务里没有入口时，更新桌面应用和该任务的 Codex 主机。
5. Screen context 不可用时，检查 Settings > Voice、Appshots 权限和组织策略。
6. 使用 API Key 登录时，桌面 Voice 按 Pricing 页不可用。可以改用文档里仍可用的文本任务；不要为了开语音去换一把来路不明的密钥。

CLI 侧先确认 `codex --version`，再在交互会话里看 `/voice` 是否存在。本文的环境到不了这一步。

## 参考资料

- [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Command line options](https://learn.chatgpt.com/docs/developer-commands)
- [Prompting](https://learn.chatgpt.com/docs/prompting)
- [Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)
