---
id: codex-dot-ios-notification-reply
title: Codex 与 Dot：在 iOS 通知里回复、分享照片，并继续 Codex 任务
seo_title: Codex 与 Dot：iOS 通知回复、分享照片、继续任务
description: 有 Dot 资格时，可以在 iOS 通知里长按回复，或从其他 App 把照片分享给 Dot。本文按官方文档整理步骤、1.2026.279 的版本要求，以及 Dot 怎样衔接已有的 Codex 任务。
lede: 通知回复的是 Dot，不是手机里的 Codex 远程控制。Dot 可以接着已有的 Codex 线程，但账号要先有 Dot 资格。
url: /guides/codex-dot-ios-notification-reply
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [Chat]
difficulty: 基础
order: 21
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-06
date_modified: 2026-11-06
verified_on: 2026-11-06
official_ref: https://learn.chatgpt.com/docs/dots/channels
keywords: [Codex Dot, iOS 通知回复 Dot, Dot 分享照片, Dot 继续 Codex, ChatGPT iOS widget]
related: [codex-remote-control-mac, codex-goal-mode-long-running-work]
faq:
  - q: 没有 Dot 的账号，更新 iOS App 之后会出现通知回复吗？
    a: 不会。官方写明这些功能需要 Dot 资格。加上小组件也不会给没有资格的账号开通 Dot。
  - q: 在通知里回复，是不是就等于用手机控制电脑上的 Codex？
    a: 不是。通知回复进入的是 Dot 的对话。用手机控制一台已配对的 Mac 或 Windows，是远程连接，见远程连接一文。
  - q: 本文的步骤在真机上验证过吗？
    a: 没有。作者没有 Dot 资格，也没有 iPhone 上的 ChatGPT 1.2026.279。步骤按 2026-11-06 的官方文档整理。有资格的读者用文末清单自己核对。
---

# Codex 与 Dot：在 iOS 通知里回复、分享照片，并继续 Codex 任务

> 本文在线版：[codexguide.io/guides/codex-dot-ios-notification-reply](https://codexguide.io/guides/codex-dot-ios-notification-reply)

> 核对依据：ChatGPT Learn《[What's new](https://learn.chatgpt.com/docs/whats-new)》中 2026-11-02 至 11-06 的条目、《[Message your dot](https://learn.chatgpt.com/docs/dots/channels)》，以及《[Create your dot in the ChatGPT mobile app](https://learn.chatgpt.com/docs/whats-new/dots-october-9-2026)》（2026-10-05 至 10-09）。需要 Dot 资格。本文按官方文档整理，没有在 iPhone 上长按通知或分享照片。文中没有截图。

适合已经有 Dot、想少打开一次完整 App 的人。也适合把「手机上的 Codex」和「手机上的 Dot」混在一起的人：两件事都能碰到 Codex 任务，但入口和权限不一样。

## 先看结论：什么时候用通知回复

官方在 2026-11-02 至 11-06 的更新里写了一条：可以在 iOS 通知里回复 Dot，也可以从其他 App 把照片分享给它。同一则更新还提到 Windows 上的可靠性改进，以及可以在对话里向主 Dot 反馈问题。后两句没有操作步骤，本文不展开。

通知回复适合这种时刻：Dot 已经推了一条通知过来，你要补一句决定、一个链接或一张图，而不想先把整个 ChatGPT 翻出来。它不适合：

- 账号还没有 Dot。更新 App 不会凭空出现这个入口。
- 你要批准的是电脑上 Codex 的命令。那是远程连接，手机只是那台已配对主机的入口，见[Codex 远程连接](./01-Codex远程控制另一台Mac.md)。旧的移动端远程协作页已经并到那一篇。
- 你要看一整段 diff 或改目标。长任务的完成标准仍然在 Goal 里设置，见[Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md)。

频道文档还有一个前提：你从不同渠道找到的是同一个 Dot。换渠道不会清空它的记忆。Slack 和 Teams 里看到的是那里交换过的消息，不会把其他渠道的每条消息都镜像过来。Dot 可以跨这些对话使用相关上下文；在把私密对话里的信息分享给别人之前，它会先确认你允许。

## 长按通知回复

官方步骤是：

1. 在 iPhone 上按住来自你的 Dot 的那条通知。
2. 输入回复。
3. 点 Send。

预期：这句回复进入 Dot 的对话，而不是新开一个与 Dot 无关的 ChatGPT 聊天。文档没有写通知必须来自哪一种后台任务，也没有写回复的字数上限。

做不到的常见原因，按文档能确定的只有资格和版本：没有 Dot，或者 ChatGPT iOS 还没到下面写的版本。通知本身没出现时，本文没有额外的系统设置可以建议。不要为了试这条功能去打开无关 App 的通知权限。

## 分享照片和其他内容

官方步骤是：

1. 打开要发的照片。
2. 点 Share。
3. 选择你的 Dot。
4. 在输入框里再看一眼这张照片，需要的话补一句说明。
5. 点 Send。

其他使用 iOS 分享面板的 App，也可以把内容分给 Dot。文档没有列出一份 App 白名单。分享之前先看输入框里的预览：账号、对话、文件路径和别人的脸，都不要出现在教学截图或随手转发的图里。本文不放截图。

这和「把电脑屏幕上的窗口发给 Codex」不是同一个功能。窗口截图是 Appshots，分享面板这条是 iOS 上的 Dot。

## Widget、Shortcuts 和 Action Button

这三项和通知回复写在同一份频道文档里，随 ChatGPT iOS **1.2026.279** 推出，并且需要 Dot 资格。官方写的是 rolling out，所以版本号到了，也可能还要等账号开通。

### 主屏幕小组件

1. 按住主屏幕的空白处，选 Edit，再选 Add Widget。
2. 找到 ChatGPT，选择 Your dot，再选 Add Widget。
3. 放好位置，点 Done。

点这个小组件，会打开 Dot 的对话，输入框处于可输入状态。文档举的例子是：开完会之后，把一项决定补进你们已经在做的工作。

小组件上的消息按钮和电话按钮默认关闭。要打开：按住小组件，选 Edit Widget，打开 Show shortcut buttons。消息按钮打开输入框。电话按钮只在通话可用时出现，用来发起通话或回到正在进行的通话。

如果小组件要你登录或先创建 Dot，打开 ChatGPT 做完那一步。加上小组件不会给没有资格的账号发放 Dot。

### 快捷指令

ChatGPT 提供一个动作，名字是 Open your dot，有三种 Mode：

| Mode | 作用 |
| --- | --- |
| Messaging | 打开 Dot 的对话，准备打字。这是默认 |
| Dictation | 用语音转文字，给 Dot 发一条消息。正在通话时不可用 |
| Call | 开始语音通话，或回到正在进行的通话 |

做法：

1. 打开苹果的 Shortcuts。
2. 新建一条快捷指令。
3. 添加动作，搜索 Open your dot，选 ChatGPT 的这个动作。
4. 选中你的 Dot，再选一种 Mode。
5. 命名并保存，然后运行一次，确认 ChatGPT 以该模式打开。

这个动作会打开 ChatGPT，并且需要登录。如果换了账号，快捷指令提示这个 Dot 不再可用，就登录拥有该 Dot 的那个账号。

### Action Button

在有 Action Button 的 iPhone 上：打开 Settings，进入 Action Button，选择 Shortcut，再选 Choose a Shortcut，选中刚保存的那条。也可以从 Shortcuts 自己的主屏幕小组件运行它。

文档没有写 Action Button 能直接回复一条通知。它打开的是你保存的那种模式。

## 和 Codex 任务的关系

通知回复本身，频道文档只说明回复会送到 Dot。Dot 和 Codex 的关系，写在 2026-10-05 至 10-09 的更新里：

- Dot 可以在 Codex 里开始工作，也可以跟进已有线程。
- 它可以搜索你的 ChatGPT 对话，并使用已有 Codex 线程和自动化里的上下文。
- 它会判断应该继续一条已有的 Codex 线程，还是新开一条，以便相关工作留在一起。
- 它也可以阅读和修改 ChatGPT Work 的自动化。你可以让它看现在排了什么，或按变化更新一项重复任务。

这里没有一个官方按钮叫「从通知继续某一条 Codex」。可用的做法是在回复里写清楚：继续哪一条已有线程，还是新开一条。官方说 Dot 会做这个判断，不是说它一定沿用你点名的那一条。本文没有资格验证这句话在 iOS 上打开哪个界面。

长任务如果已经在桌面或 CLI 里用 `/goal` 跑着，通知回复不能代替暂停、恢复和改目标。目标仍在原来的那条对话上。Dot 适合补一句决定或一张图；Goal 适合把完成标准挂住。见[Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md)。

## 和远程连接、短信的区别

| 你想做的事 | 用哪个 | 官方前提 |
| --- | --- | --- |
| 在通知里回 Dot 一句，或丢一张照片 | 本文的通知回复和分享面板 | 有 Dot；iOS App 1.2026.279 起陆续提供 |
| 让 Dot 接着一项 Codex 工作 | 在 Dot 对话里说明继续或新开 | 2026-10-05 至 10-09 的更新；仍要有 Dot |
| 用手机批准家里或公司电脑上的 Codex 命令 | [远程连接](./01-Codex远程控制另一台Mac.md) | 电脑在线并已配对。手机不在本机跑仓库 |
| 用 iMessage 或 Android RCS 给 Dot 发短信 | 频道文档里的 Texting，不是通知回复 | 文档写的是面向美国 ChatGPT Pro 的 beta，一对一，可发文字、照片和语音 |

短信、小组件和通知回复最后到达的是同一个 Dot，但设置位置不同。短信要在 Dot 的资料页里单独打开 Texting 并验证号码。本文不重复那一套验证步骤。

## 资格、版本，以及你自己怎么核对

官方同时写在 What's new 和频道文档里的条件是：

- ChatGPT iOS **1.2026.279** 或该版本开始的推出范围。
- 账号已经有 Dot。文档用的是 dot access。创建 Dot 的入口在 ChatGPT 手机 App 里：起名、改外观、连接插件。没有资格时，这个流程不会因为你安装了小组件而出现。
- 使用的是设过这个 Dot 的那个登录账号。

同一周的 What's new 没有写 Android 通知长按回复。不要把 iOS 的步骤挪到 Android。Android 上文档单独写了 RCS 短信，那是 Texting。

有 Dot 的读者可以这样核对，不需要把画面发给别人：

1. 在 App Store 或 App 的关于页确认版本不低于 1.2026.279。看不到功能时，先区分「版本不够」和「账号还没有资格」。
2. 等一条来自 Dot 的通知，按住，回复一个不含账号和路径的短句，再打开 Dot 的对话，确认这句在里面。
3. 从相册分享一张没有隐私内容的照片，在点 Send 之前看输入框里是不是这张图。
4. 在对话里点名一条已有的 Codex 线程，看 Dot 是继续它还是新开一条。官方只承诺它会做这个判断，并使用 Codex 上下文。不要把某一次的界面当成所有账号的固定菜单。

作者没有完成上面四步。文档和真机不一致时，以你这台手机上的 ChatGPT 为准，并把版本号记下来。

## 参考资料

- [What's new：November 2–6, 2026](https://learn.chatgpt.com/docs/whats-new)
- [Message your dot](https://learn.chatgpt.com/docs/dots/channels)
- [Create your dot in the ChatGPT mobile app](https://learn.chatgpt.com/docs/whats-new/dots-october-9-2026)
- [Codex 远程连接](./01-Codex远程控制另一台Mac.md)
- [Codex Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md)
