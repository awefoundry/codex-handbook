---
id: codex-dot-custom-instructions
title: Codex 给 dot 设自定义指令：和 ChatGPT 自定义指令分开，还能用自定义规则决定哪些事要先问你
seo_title: Codex 给 dot 设自定义指令：和 ChatGPT 分开，并用自定义规则设边界
description: dot 的自定义指令只对这个 dot 生效，和 ChatGPT 自定义指令不是同一份。本文按官方文档说明怎么在对话里交代长期工作方式、手机上 Behavior 怎么改，以及自定义规则的四种处理方式和它不能越过的安全确认。
lede: 想让 dot 记住你的工作方式，用自定义指令。想限制某件具体的事能不能直接做，用可选的自定义规则。两样都不等于授予 App 或电脑权限。
url: /guides/codex-dot-custom-instructions
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 28
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-15
date_modified: 2026-11-15
verified_on: 2026-11-15
official_ref: https://learn.chatgpt.com/docs/dots/controls
keywords: [Codex dot, dot 自定义指令, dot custom rules, Customize Behavior, How dot handles tasks, dot 数据控制]
related: [codex-dot-ios-notification-reply, codex-dot-multiple-computers, codex-data-controls-training]
faq:
  - q: dot 的自定义指令和 ChatGPT 自定义指令是同一份吗？
    a: 不是同一份。官方 Controls 页写明，自定义指令只属于你的 dot，和 ChatGPT 自定义指令分开。
  - q: 设一条「不用问我直接做」的规则，dot 就能打开 App 或连上电脑吗？
    a: 不能。官方写明，自定义规则不授予 App 或电脑的访问权，也不能取消内置安全要求，或拿掉必须由你确认的步骤，例如使用已保存的登录。连电脑是另一项授权，见连接多台电脑一文。
  - q: 工作区把自定义规则关掉了，已经保存的规则还会生效吗？
    a: 不会。官方写明，工作区关闭自定义规则后，你不能编辑已保存的规则，这些规则也不生效。
  - q: 本文在手机或桌面 App 上点过这些菜单吗？
    a: 没有。写作环境没有 dot，也没有 ChatGPT 桌面端或手机。菜单名按 2026-11-15 的英文文档写，中文界面的叫法可能不同。文中没有截图。
---

# Codex 给 dot 设自定义指令：和 ChatGPT 自定义指令分开，还能用自定义规则决定哪些事要先问你

> 本文在线版：[codexguide.io/guides/codex-dot-custom-instructions](https://codexguide.io/guides/codex-dot-custom-instructions)

> 核对依据：ChatGPT Learn《[What's new](https://learn.chatgpt.com/docs/whats-new)》2026-11-09 至 11-13 的 “Set custom instructions for your dot”，以及《[Control your dot](https://learn.chatgpt.com/docs/dots/controls)》《[Meet dots](https://learn.chatgpt.com/docs/dots)》，2026-11-15 打开。写作环境没有 dot，没有桌面 App，也没有手机。下面的菜单名是英文文档里的原文，中文界面可能用别的译名。本文没有截图。

适合已经有 dot、想规定它长期怎么做事的人。也适合把「ChatGPT 自定义指令」和「这个 dot 的指令」当成同一份设置的人。

在手机通知里回复 dot，见 [iOS 通知回复](./21-Codex与Dot-iOS通知回复与分享继续任务.md)。让 dot 在某一台电脑上跑本地 Codex 任务，见 [连接多台电脑](./24-Codex与dot-连接多台电脑-指定电脑运行本地Codex任务.md)。那两件事都不靠本文的自定义指令完成。

## 先看结论

- **自定义指令只对这个 dot 生效**，和 ChatGPT 自定义指令是两份设置。
- 可以在对话里告诉它要记住的长期工作方式，也可以事后让它改。手机上如果有 Behavior，按下面的路径编辑并保存。
- **自定义规则是可选的**，用来给某类具体动作划边界。桌面和网页在 Settings > Personalization 的 Permissions 下。手机上的 Customize > Custom rules 只在 Behavior 不可用时出现。
- 规则是 dot 会尽量遵守的指示，它可能做错。规则不授予 App 或电脑权限，也不能盖过内置安全要求，或取消必须确认的步骤。
- 工作区如果关闭自定义规则，就不能编辑，规则也不生效。
- ChatGPT 的数据控制同样作用于合格的 dot 对话。本文不写未经官方确认的开关传闻。

dot 按套餐、地区和工作区逐步开放。谁能创建，以 [dots 页的 Access](https://learn.chatgpt.com/docs/dots#access) 为准；套餐表和「2026-11-18 起符合条件的工作区默认开启」已经写在 [连接多台电脑](./24-Codex与dot-连接多台电脑-指定电脑运行本地Codex任务.md) 里，本文不重复。创建入口是 ChatGPT 手机 App、桌面 App 或桌面浏览器。手机网页不支持。

## 自定义指令：只属于这个 dot

2026-11-09 至 11-13 的 What's new 写了一条：告诉 dot 你希望它怎样回应、怎样和你一起工作。你可以在对话里让它更新指令，也可以在 Customize → Behavior 里编辑。

Controls 页把范围说得更具体。自定义指令用来规定这个 dot 怎么工作，例如你偏好的写作风格、它隔多久向你汇报，以及什么时候先问你再行动。**它和你的 ChatGPT 自定义指令分开。** 改其中一份，不会自动改另一份。

官方举的例子是：

```text
When you finish a task, link to the result and tell me what needs my attention.
```

意思是：做完一件事后，给出结果链接，并说明哪些地方要你看。你也可以之后再说「把这条指令改成……」。

写作风格、汇报方式，放在对话或自定义指令里。某一类动作能不能直接做，放到下一节的自定义规则。Controls 页把这两件事分开。

## 在手机上编辑：有 Behavior 时

Controls 页写的逐步操作在手机上，而且有前提：Behavior 可用，并且允许编辑。

1. 打开侧栏，选择 **Customize > Behavior**。
2. 如果看到 ChatGPT 和你的 dot 两个标签，选择 **这个 dot 的名字**。
3. 在 **How [你的 dot 的名字] handles tasks** 下面填写偏好。
4. 点对勾（**Save**）保存。

之后要改，回到 Customize > Behavior，改完再保存。

手机上没有 Behavior 时，文档的说法是：更新 App，或者改用桌面或网页上这个 dot 的对话来改指令。文档没有给出一套桌面端 Settings 里的自定义指令菜单。桌面和网页文档写明的是下一节的自定义规则入口，不要把那一条当成自定义指令的路径。

What's new 用了 Customize → Behavior 这个说法，没有再拆桌面和手机。逐步点击以 Controls 页的手机步骤为准。本文没有打开过这个界面。

## 自定义规则：四种处理方式

自定义规则是可选的。Controls 页写明：先把指示写在对话里就够用，不必为每一次批准都建一条规则。

建规则的位置：

| 入口 | 文档写的路径 |
|---|---|
| 桌面和网页 | **Settings > Personalization**，在 **Permissions** 下选择 **Custom rules** |
| iOS 和 Android | 打开侧栏，选择 **Customize > Custom rules**。这一项在 **Behavior 不可用时**才出现 |

然后选 **Add**，描述这个动作，选择处理方式，再选 **Add rule**。四种处理方式的官方含义是：

| 规则（英文原文） | 预期行为 |
|---|---|
| Take action without asking | 对这条规则描述的动作，不再征求批准 |
| Take action when you say so | 你明确要求时才做；否则在动手前立刻问你 |
| Ask before taking action | 做这个动作之前先征求批准 |
| Hand off to you | 把这件事交给你本人做 |

官方的例子：给客户发消息用 Ask before taking action；删除共享项目文件用 Hand off to you。

已保存的自定义规则作用于同一账号里的这个 dot。它们可以允许某类动作、要求先问你，或阻止它做某件事。文档同时写明：这是 dot 会尽量遵守的指示，它可能出错。

一条规则的菜单可以编辑或删除。选 **Open Plugins** 去看插件权限。插件权限管的是 App 动作，和自定义规则分开。

工作区如果关闭自定义规则，你不能编辑已保存的规则，规则也不生效。管理员侧的设置名，Controls 页指向 Configure dots permissions 和 Set up dots for work。本文没有工作区管理权限，不补一套管理员菜单。

## 规则盖不过的确认

动手之前，文档描述了一层自动审查：可能影响你的账号，或会把信息分享出去的动作，会对照你的指示、权限、自定义规则和内置安全要求来决定。结果是直接做、先问你，或把某一步留给你本人。官方举的例子是改密码必须你自己来。

另外两句边界，Controls 页写在自定义规则下面：

- 规则**不授予**对某个 App 或电脑的访问。让 dot 使用某台电脑的文件和本地 Codex 任务，仍要在那台电脑上单独 Allow，见 [连接多台电脑](./24-Codex与dot-连接多台电脑-指定电脑运行本地Codex任务.md)。
- 规则**不能覆盖**内置安全要求，也不能去掉必须确认的步骤。使用已保存的登录（saved login）仍然要你确认。dots 页也写了：指令和自定义规则都不能覆盖内置安全要求。

「帮我起草回复」不等于允许它把回复发出去。文档的说法是：起草请求不会自动变成发送权限；范围要写清谁参与、要发生什么、什么时候做。落在这个范围里的后续动作可以沿用这条指示，范围外的动作需要另一次决定。

## 插件权限、数据控制、暂停和删除

这三块都在同一页 Controls 里，和自定义指令是不同的开关。

**插件权限。** 选 Open Plugins 查看。它控制 App 动作，和自定义规则分开。dot 只能使用你的账号里已经安装并启用、而且权限允许的插件。连上一个聊天渠道，不会自动连上收件箱、其他 App 或本地电脑。

**数据控制。** Controls 页的原文是：你的 ChatGPT 数据控制同样适用于合格的 dot 对话，以及它执行的工作。OpenAI 不会直接用主动研究（proactive research）或其私人笔记来训练模型。如果这些研究里的信息进入了一段合格的对话或一项任务，就按你的数据设置处理。哪些对话算「合格」，该页没有再列清单，本文不补。

Codex 任务一侧的 Improve the model、Include environments，见 [对话会被用来训练吗](../10-配置模型与权限安全/23-Codex对话会被用来训练吗-数据控制与Include-environments.md)。本文只转述 Controls 页对 dot 的这一段，不把未经 OpenAI 确认的「训练开关被静默打开」写进来。

**暂停和删除是三件不同的事。**

- **Pause** 停的是 dot 当前的主任务。它不停掉每一个已委派的任务，也不取消以后的定时运行。继续用 **Resume**。
- 某一个已委派的任务，到 **Activity** 里打开再停。
- 要结束的重复任务，到 **Scheduled** 里禁用或删除。

停掉工作不会撤销已经完成的动作。删除 dot 用 **Delete**。确认框会说明对话、记忆和定时任务怎么处理。需要留下的结果先保存。删除不能撤销，也不会撤回已经在已连接 App 里做出的修改，或已经发给别人的消息。

## 怎么自己核对

本文没有登录，下面是文档里的核对顺序，不是这次写作的实测结果。

1. 在对话里说一条长期指令，再让 dot 复述它现在记住的工作方式。
2. 手机上如果有 Behavior，打开 Customize > Behavior。有两个标签时，确认选中的是 dot 的名字，而不是 ChatGPT。保存后退出再进一次，看文字还在不在。
3. 在桌面或网页的 Custom rules 里加一条低风险规则，例如对某一类发送使用 Ask before taking action。下一次它要做这件事时，看它是先问你，还是直接做。规则可能被做错，一次没问到，不能当成规则不存在。
4. 工作区账号先问管理员自定义规则是否被关闭。关闭之后，编辑入口和已保存规则都不生效。

没有这些界面，就还没有 dot，或当前客户端版本还没有对应入口。更新 App 之后仍然没有 Behavior 时，按文档改到桌面或网页的对话里设置。

## 下一步

- 通知里回复、从别的 App 分享照片：[Codex 与 Dot：iOS 通知](./21-Codex与Dot-iOS通知回复与分享继续任务.md)
- 指定哪台电脑跑本地 Codex 任务：[连接多台电脑](./24-Codex与dot-连接多台电脑-指定电脑运行本地Codex任务.md)
- Codex 对话和训练开关：[数据控制](../10-配置模型与权限安全/23-Codex对话会被用来训练吗-数据控制与Include-environments.md)

## 参考资料

- [What's new](https://learn.chatgpt.com/docs/whats-new)（2026-11-09 至 11-13：Set custom instructions for your dot）
- [Control your dot](https://learn.chatgpt.com/docs/dots/controls)（自定义指令、自定义规则、数据控制、暂停和删除）
- [Meet dots](https://learn.chatgpt.com/docs/dots)（dot 是什么，在桌面、网页和手机上创建）
