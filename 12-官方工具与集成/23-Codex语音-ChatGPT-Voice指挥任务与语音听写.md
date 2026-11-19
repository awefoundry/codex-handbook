---
id: codex-voice-chatgpt-voice
title: Codex 语音怎么用：补上 CLI 0.170 的 /voice 与 F8 实时通话，以及 mute、stop 和 settings
seo_title: Codex 语音：/voice、F8、ChatGPT Voice 与听写
description: Codex 的语音有两条路：ChatGPT 桌面应用里的 Voice，以及 CLI 在支持语音的会话里用 /voice 或 F8。本文按官方 Voice 页和 Developer commands 更新：0.170.0 为 TUI 实时语音加入了 WebRTC 协商，并说明 mute、stop、settings 怎么用，以及和语音听写的区别。
lede: 要边说边改任务，用 ChatGPT Voice。只想把话说成一段提示词，用作曲框里的 Dictate。CLI 在构建和会话都支持时，用 /voice 或 F8。
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
date_modified: 2026-11-19
verified_on: 2026-11-19
tested_cli_version: 0.170.0
official_ref: https://learn.chatgpt.com/docs/features/voice
keywords: [Codex 语音, Codex /voice, Codex F8, Codex WebRTC, ChatGPT Voice]
related: [codex-cli-0-170-voice-mcp-reconnect, codex-appshots, usage-limits-credits, codex-desktop-task-workflow]
howto: false
faq:
  - q: 本文打通过语音电话吗？
    a: 没有。写作环境没有 ChatGPT 桌面应用，也没有麦克风，没有打开 TUI。2026-11-19 只在 Linux 上核对了 codex-cli 0.170.0 的版本、帮助文本和可执行文件里的 /voice 字符串。步骤和价格来自当天打开的官方文档。
  - q: 语音听写和 ChatGPT Voice 用的是同一个按钮吗？
    a: 官方把它们写成两件事。Voice 是实时对话。Prompting 页的 Dictate 把语音转写进作曲框，你可以改完再发送。CLI 的 /voice 是第三条入口，只在当前构建和会话支持语音时出现。
  - q: API Key 登录能开桌面语音吗？
    a: 2026-11-19 的 Pricing 页仍写明，ChatGPT Voice in Desktop 不能通过 API Key 使用。功能对照表里 Voice dictation 和 ChatGPT Voice 两行的 API Key 列是破折号。
  - q: /voice mute 和 /voice stop 有什么区别？
    a: Developer commands 写：/voice mute 开关麦克风，/voice stop 结束对话。/voice 或 F8 用来开始或结束一场语音，/voice settings 为以后的对话选择声音。本文没有在 TUI 里执行过这些命令。
---

# Codex 语音怎么用：补上 CLI 0.170 的 /voice 与 F8 实时通话，以及 mute、stop 和 settings

> 本文在线版：[codexguide.io/guides/codex-voice-chatgpt-voice](https://codexguide.io/guides/codex-voice-chatgpt-voice)

> 核对依据：2026-11-19 打开的 [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)、[Pricing](https://learn.chatgpt.com/docs/pricing) 中 “How much does Voice cost?”、[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 的 “Talk to Codex with /voice”、[Prompting](https://learn.chatgpt.com/docs/prompting) 的 “Use voice dictation”，以及 Help Center [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)。CLI 版本差异见 [Codex CLI 0.170.0](./29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md) 和 [rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)。**本文没有 ChatGPT 桌面应用，没有手机，没有麦克风，没有进入 TUI，也没有截图。** 0.170.0 的帮助和可执行文件只能说明命令文本在不在，不能代替一次通话。

## 先分清 Voice 和听写

官方文档把语音分成两条路，CLI 是第二条路上的终端入口。

ChatGPT Voice 是一场实时对话，由 GPT-Live 驱动。你可以开口布置任务、询问进度或改变方向。语音听写只把话说成可编辑的提示词，发送前仍由你确认。

CLI 不替代桌面 Voice。Developer commands 写的是：当前 CLI 构建和这场会话支持语音时，用 `/voice` 或 F8。0.170.0 为 TUI 里的实时语音加上了 WebRTC 协商，命令本身仍是这一节后面的四条。

## 哪些套餐和入口能用

[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) 写明，桌面应用里的 Voice 面向 ChatGPT Plus、Pro、Business、Edu 和 Enterprise。Enterprise 和 Edu 先有两周抢先使用，之后才默认开放。是否真的出现在你的界面上，还取决于发布进度和工作区设置。同一页写：手机上的 Codex 要先和一台桌面主机配对，才能使用 ChatGPT Voice。

Help Center 的 [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) 在 2026-11-19 打开时显示 “Updated: 5 hours ago”，没有给出绝对时间。它另外写：ChatGPT Voice 给网页和手机上的 Work 加上实时语音，也给桌面应用里的 Work 和 Codex 加上实时语音；桌面这一侧点名的是 macOS 和 Windows。网页和手机上，Work 里选 Voice 控件开始一场 Live 对话。需要你批准时，看屏幕上的按钮；口语批准不算数。Voice 功能页这次读到的步骤仍是桌面应用，没有把网页和手机的 Live 写成同一套按钮。两页都打开了，本文分开引用。

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

文档还写：整个桌面应用同一时间只能有一场语音。另一扇窗口里已经有一场时，新的会开不起来。Help Center 也写同一时间只能有一场 Voice。

## 用语音开任务、查进度、换任务

Voice 页写，对话支持打断、追问和改方向。任务已经开始之后，可以继续说，用来查看进度或把工作拉回某个方向。

它还可以为较长的工作另开任务、查看已有任务，并把进度、阻塞和结果说回当前这场语音。文档给的例子是：

- 让它查看当天的发布简报，并总结需要批准的决定。
- 让它开一项 Codex 任务去跑测试，并排查没通过的部分。
- 让它查看进行中的任务，总结什么在挡住进度。

也可以要求改口到另一项 Codex 任务，再说回上一场。文档的例句是 “Let me talk to the task reviewing the tests”，然后 “Take me back to the previous task”。目标任务必须支持语音，并且在一台已连接的主机上。

这些是文档里的说法，不是本文跑出来的结果。语音遵循它在 Chat、Work 和 Codex 里所指挥的那些任务的同一套权限。权限模式见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

Help Center 补了一句边界：网页和手机上，动作需要批准时用屏幕上的控件，口语说「批准」不会生效。桌面端的批准方式以你当前弹窗为准，本文没有桌面应用。

## Screen context 和隐私

仅 macOS：在 **Settings > Voice** 打开 **Screen context**，然后说 “Take a look at this”。文档写，ChatGPT 会拍下最前面窗口的一张 appshot，用作上下文。组织可以关掉这项能力。

这张 appshot 可以包含窗口图像，以及可访问的文字，**包括滚动区域以外的文字**。macOS 可能会请求 Screen & System Audio Recording 和 Accessibility 两项权限。含有密钥、邮件、客户数据或未公开代码的窗口不要拿来做这一步。

快捷键拍摄当前窗口的 Appshots 是另一篇：[Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)。Voice 页把 “Take a look at this” 的结果也叫做 appshot。本文没有桌面应用，没有核对语音设置里的 Screen context 和 Appshots 的快捷键是不是同一个开关。若 Screen context 不可用，Voice 页要求检查 Settings > Voice、Appshots 权限和组织限制。

## 语音听写

[Prompting](https://learn.chatgpt.com/docs/prompting) 在 2026-11-19 的原文仍是：在桌面应用的作曲框选择 **Dictate**，然后说话。ChatGPT 把语音转写进作曲框，你检查、修改之后再发送。

听写不开始一场实时对话，也不替你改任务方向。只想把一段需求说成文字时用它。要让它边听边开工，用上一节的 Voice。

## CLI：0.170.0 的 WebRTC，以及 /voice、F8、mute、stop、settings

[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 的 “Talk to Codex with /voice” 原文是：

> When your CLI build and session support voice, use `/voice` or F8 to start or stop a voice conversation. Use `/voice mute` to turn your microphone on or off and `/voice stop` to end the conversation. Use `/voice settings` to choose a voice for future conversations.

对应关系：

| 命令或按键 | 文档里的作用 |
|---|---|
| `/voice` 或 F8 | 当前构建和会话支持语音时，开始或结束一场语音 |
| `/voice mute` | 开关麦克风 |
| `/voice stop` | 结束对话 |
| `/voice settings` | 为以后的对话选择声音 |

文档没有写出默认声音的名字，也没有写 F8 在哪一种终端模拟器里一定生效。它用了 “when your CLI build and session support voice”，这一节没有最低版本号。

0.170.0 的发布说明新增的是另一句：Added WebRTC negotiation for realtime voice calls in the TUI.（#61172）。协商方式从这一版写进 Release。命令仍是上面四条。升级命令和这条功能在版本说明里的位置，见 [Codex CLI 0.170.0](./29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md)。

2026-11-19 在 Linux 上安装了 npm 的 `@openai/codex@0.170.0`，`codex --version` 为 `codex-cli 0.170.0`。核对到的只有这些：

- `codex --help` 没有列出 `/voice`、F8、mute、stop、settings。斜杠命令属于交互会话。
- 可执行文件里有 `Usage: /voice [settings|mute|stop]`，以及 “When voice is available, use /voice to start or stop a voice conversation, or /voice settings to choose a voice”。字符串只能说明这个构建带有这段说明。
- 独立的空 `CODEX_HOME`、未登录时，`codex features list` 里 `in_app_voice` 是 `stable`，有效状态是 `true`。本文没有对照 0.169 的同一行。有效状态为 true 也不等于本机已经打通麦克风。
- `codex login status` 输出 `Not logged in`，退出码 1。

终端是非交互的，没有 TUI，也没有麦克风，因此没有输入 `/voice`，没有按 F8，也没有打开 `/voice settings`。F8 只按 Developer commands 的原文写入，没有在二进制里把碰巧出现的字节当成键位证据。

桌面 Voice 不能用 API Key，已见 Pricing 页。CLI `/voice` 的登录要求，文档没有在这一节写死。本文没有支持语音的会话，没有该项输出。

## 费用

2026-11-19 的 Pricing 页 “How much does Voice cost?” 原文仍是：

- Voice in Desktop 按每分钟 **0.05 美元** 计入已有的 Codex 用量预算。
- GPT-Live 负责实时对话。处理任务的模型按它自己的 token 价格另外计算。语音和任务共用套餐的用量限制。
- 按 credits 计费的 Business、Edu 和 Enterprise 工作区，桌面语音是每分钟 **1.25 credits**。Plus 和 Pro 在花额外 credits 时也是这个单价。
- ChatGPT Voice in Desktop 不能通过 API Key 使用。

Help Center 对网页和手机写了另一套计量：Work 里的 Voice 使用每日 Voice 分钟额度；由说话或打字开始的 Work 任务，计价方式相同。桌面端在适用灵活定价时，连接中的 Voice 时长另外计算；经 Voice 开始的任务，仍从 Work 和 Codex 共用的用量和 credits 里扣。本文没有把「每日分钟」换算成 0.05 美元。桌面单价以 Pricing 页为准，网页和手机的分钟额度以 Help Center 为准。

用量面板、5 小时窗口和 credits 的读法见 [用量额度怎么看](../10-配置模型与权限安全/08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。本文没有登录，没有 Usage 页面，没有把 0.05 美元换算成某一次任务的 token。

## 开不了时先查什么

Voice 页的排查顺序是：

1. 套餐、发布进度和工作区是否已经打开 ChatGPT Voice。Enterprise / Edu 可能仍在两周抢先期内，默认开关尚未打开。
2. 麦克风权限是否已经授予桌面应用。
3. 是不是已经有另一场语音占着这台桌面应用。
4. 已有任务里没有入口时，更新桌面应用和该任务的 Codex 主机。
5. Screen context 不可用时，检查 Settings > Voice、Appshots 权限和组织策略。
6. 使用 API Key 登录时，桌面 Voice 按 Pricing 页不可用。可以改用文档里仍可用的文本任务。

Help Center 多出来的几条，只适用于它写到的网页和手机 Work：

- 先确认人在 Work，而不是普通 Chat。
- 托管工作区里，Work 的 Voice 同时要求 Voice 和 Work 的权限。
- 批准看屏幕按钮。嘴里说批准不会被当成批准。
- 同一时间只能有一场 Voice。

CLI 侧先确认 `codex --version`。0.170.0 提供的是 WebRTC 协商；会话本身仍要支持语音，`/voice` 或 F8 才会按文档开始。本文的环境到不了输入命令这一步。

## 参考资料

- [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Prompting](https://learn.chatgpt.com/docs/prompting)
- [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
- [GitHub Release rust-v0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)
- [Codex CLI 0.170.0](./29-Codex-CLI-0.170-TUI实时语音-同名MCP与Cloud重连.md)
- [Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)
