---
id: codex-computer-history
title: "Codex Computer History 怎么用：开启条件、记录什么不记录什么、数据存在哪、怎么暂停和清除"
seo_title: "Codex Computer History：开启、记录范围、本地存储与清除"
description: "Computer History 在 macOS 桌面端默认关闭。本文按官方文档说明谁能开、管理员授权和本人 opt in 的差别、记录哪些交互事件、时间线怎么问、排除和暂停、本地文件与发给 OpenAI 的部分，以及清除和排障。"
lede: "默认关闭。管理员授权只是允许你自己开。记的是点击、输入和辅助功能能读到的文本，不是屏幕录像。"
url: /guides/codex-computer-history
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 17
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-28
date_modified: 2026-11-28
verified_on: 2026-11-28
official_ref: https://learn.chatgpt.com/docs/customization/computer-history
keywords: [Codex Computer History, ChatGPT 电脑使用记录, Codex 记忆时间线, Chronicle, Codex 隐私, skysight]
related: [codex-memories, codex-data-controls-training, codex-agents-md-poisoning-downloads, codex-computer-use-desktop-apps]
howto: true
faq:
  - q: "管理员已经授权了，为什么我这边还是关着？"
    a: "授权只表示你的角色可以选择开启。Computer History 默认关闭，Pro、Business、Enterprise 都要本人 opt in，并且还要打开 Memories。工作区角色没有权限时，改本机设置也不能打开。"
  - q: "它会截屏或录音吗？"
    a: "官方写明历史里不包含截图，不录麦克风，不录系统音频。无痕浏览的网页活动也不会进入历史。它记录的是点击、输入、快捷键、切换应用，以及 macOS 辅助功能暴露的文本和其他上下文。"
  - q: "暂停之后，刚才那段摘要还会写完吗？"
    a: "暂停后不再收集新的交互事件。官方同时写明，已经在进行的摘要仍可能继续，直到完成。"
  - q: "清除历史能不能撤销？删 Codex 记忆会怎样？"
    a: "清除最近 10 分钟、1 小时、1 天或全部，会删掉对应的交互事件和由此生成的记忆，不能撤销。Memories 页写明，在本机删除 Codex memories 时，如果提供 Computer History，也会一并清空。"
  - q: "本机上的 Computer History 文件加密了吗？"
    a: "没有。官方在存储说明里写明，这些文件可能包含敏感信息，Computer History 不会加密它们，以同一 macOS 用户身份运行的其他程序可能读取到。要保护好 Mac 账户，并排除不想记录的来源。"
---

# Codex Computer History 怎么用：开启条件、记录什么不记录什么、数据存在哪、怎么暂停和清除

> 本文在线版：[codexguide.io/guides/codex-computer-history](https://codexguide.io/guides/codex-computer-history)

> 核对依据：2026-11-28 打开的 [Computer History](https://learn.chatgpt.com/docs/customization/computer-history) 和 [Memories](https://learn.chatgpt.com/docs/customization/memories)。没有登录 ChatGPT，没有打开 macOS 桌面端，菜单名和路径只按这两页原文转述。

Computer History 把你允许的应用和网站活动整理成记忆，以及一条可以回看的时间线，供 ChatGPT 和 Codex 引用。本地记忆怎么开、文件在哪、`/memories` 怎么按对话控制，见 [Codex Memories](./12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)。它和 [Computer Use](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md) 不是同一项：后者是让 Codex 操作桌面应用；本文只讲活动记录。

## 先说结论

按 2026-11-28 的 Computer History 页：

- 它面向 ChatGPT Pro、Business、Enterprise，只在 macOS 上的 ChatGPT 桌面应用里提供，**默认关闭**。
- Business 和 Enterprise 要管理员先授权。授权不等于开启。每个人自己 opt in，Pro 也要自己开。
- 它依赖 Memories。用 API key 或 Amazon Bedrock 时不可用。
- 它取代更早的 Chronicle 研究预览，但是重做的系统，不是改名。
- 记录交互事件和 macOS 辅助功能能提供的文本。历史里不放截图，不录麦克风和系统音频，无痕浏览不进入。
- 临时事件文件最多留 48 小时。生成的记忆是纯文本 Markdown，不加密，留在本机，直到你删除。
- OpenAI 在服务器上处理事件文件以生成记忆，处理后不保留这些事件文件（法律要求除外），也不用它们训练。之后对话里用到的记忆内容，按你的数据控制，可能用于改进模型。

## 谁能用

官方页的适用范围是：ChatGPT Pro、Business、Enterprise 用户，在 macOS 的 ChatGPT 桌面应用里。Pro 可以自己选择打开。Business 和 Enterprise 工作区里，管理员必须先明确授权，成员才能选择打开。

Enterprise 管理员的入口写在 **Workspace Settings > Permissions & roles** 的 **Enable Computer History**，用来给合适的工作区角色授权。这一页没有单独写出 Business 管理员的菜单路径。工作区角色没有权限时，改本机设置也不能启用。

个人 opt in 和授权是两步。官方原意是：授予工作区访问权，只是让成员可以选择打开，不会替任何人打开。ChatGPT Pro 同样要自己打开。

还要满足两件事：

- **需要 Memories。** 桌面端用 `/memories` 控制某一条对话能不能使用本地记忆，以及能不能贡献给以后的记忆。Memories 的全局开关和目录见 [Memories 一文](./12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)。
- **API key 和 Amazon Bedrock 不可用。** 官方页直接写了这两项。

地区方面，官方写的是 available in supported regions，并点名包括欧洲经济区（EEA）、瑞士和英国。这一页没有给出完整地区名单，也没有写中国大陆是否在内。设置项不出现时，先核对套餐、工作区授权和是否在支持地区，不要根据菜单缺失自行推断原因。

## 怎么开启

历史从你选择打开之后才开始。Business 或 Enterprise 先请管理员授权。管理员批准不会替你 opt in。

官方的五步是：

1. 打开 macOS 上的 ChatGPT 桌面应用。
2. 在 **Settings** 的 **Integrations** 下选择 **Computer history**。
3. 选择 **Turn on**，并阅读隐私、权限和本地存储说明。
4. 如果出现提示，打开 Memories。Computer History 需要 Memories，才能在对话和任务之间使用活动上下文。
5. 选择哪些应用和网站可以贡献历史，然后按 macOS 弹出的权限提示操作。

它**不需要屏幕录制权限**。设置项不出现时，确认套餐支持 Computer History；如果是工作区账号，再确认管理员已经启用。

## 记录什么、不记录什么

它从允许的应用和网站建立一条交互事件流。事件可以包括：

- 点击
- 输入
- 键盘快捷键
- 切换应用
- macOS 辅助功能系统暴露的文本和其他上下文

这些事件会定期变成文字摘要和本地记忆文件。

官方反复写明的边界是：

- 历史里**不包含截图**。
- **不录**麦克风输入，**不录**系统音频。
- **无痕浏览**的网页活动永远不进入。

因此它不是屏幕录像，也不是会议录音。你在允许的应用里打出来的文字、点过的位置，以及辅助功能能读到的界面文本，可以进入事件流。把含有健康、财务或私人内容的应用排除，见后面的控制一节。

它和 Chronicle 的关系也按原文：Computer History 取代更早的 Chronicle 研究预览，但是一套重做的系统，不是把旧预览改个名字。

## 怎么用：时间线和提问

打开 **Settings > Computer history > History**。时间线按天和时间把摘要分组。每一条可以显示：

- 活动的标题和文字摘要
- 贡献了这条摘要的应用
- 当 ChatGPT 认出可重复的工作时，一条建议的 skill 或自动化
- 在 Finder 里显示记忆文件，或删除这一条

选择 **Ask about your history**，用 Computer History 开一段对话。官方给的示例提问是：

- “What was I working on before my last break?”
- “Where can I find the proposal document I was looking for earlier today?”
- “Give me a list of tasks I’ve worked on today and their status.”
- “Prepare a summary of what I did yesterday for standup.”

对应的意思是：休息前我在做什么；今天早些时候找的那份提案在哪；今天做过的任务和状态；把昨天做的事整理成站会摘要。提问可以换成你自己的说法，文档没有要求必须用这四句英文。

官方还写了三类用途。休息之后，可以问自己刚才在做什么，而不必逐个回忆打开过的应用和文档。找最近的工作时，可以按你记得的方式提到一份文档、一段对话或一项任务，让时间线帮你对上来源。发现重复流程时，时间线条目可以建议一个 skill 或自动化；你先看建议，再让 Codex 按记录下来的流程创建。

另一句边界：文件、Slack 对话、Google 文档或其他来源更适合当前任务时，ChatGPT 和 Codex 可以用历史找出那个来源，然后再直接去读它。历史是线索，不是那份文件本身。

## 控制范围：排除、暂停、与他人沟通

应用和网站的权限决定哪些来源可以贡献交互事件。在 **Settings > Computer history > Permissions**：

- **Exclude these apps** 和 **Exclude these websites** 排除你指定的应用或 URL，其他支持的来源仍可进入。
- **Include only these apps** 和 **Include only these websites** 只允许你明确点名的来源。

在时间线某一条上点应用图标，可以把该应用排除出以后的历史，以后也可以再加回来。

改权限只影响以后的历史。已经生成的条目要另外删除或清除。无痕浏览始终不进入，不依赖你怎么配这份名单。

收集可以暂停：

- 点 macOS 菜单栏里的 ChatGPT 图标，展开 Computer History 菜单，查看它在捕获什么，并使用控制项。
- 选 **Pause** 停止收集新的交互事件，准备好再选 **Resume**。
- 关掉 Computer History，停止以后的活动收集。

暂停之后不会收集新事件，但**正在进行的摘要可能继续，直到完成**。

沟通场景官方写得很具体：Computer History 可以包含来自通讯应用和网站的交互事件。和他人沟通时，除非事先得到对方明确同意，否则关掉它。健康、财务或个人信息所在的应用，考虑暂停，或把这些应用排除掉。

## 数据存在哪、哪些会发给 OpenAI

交互事件流先临时存在你的 Mac 上，供 ChatGPT 和 Codex 生成记忆、并整理建议的工作流。事件文件放在 ChatGPT 的 **App Group** 里，官方的说法是：其他应用未经明确许可不能访问这些文件。ChatGPT 和 Codex 在 48 小时后删除这些事件文件。临时事件文件的保留时间是最多 48 小时。

生成出来的记忆和 Codex 的本地记忆是同一类东西：纯文本 Markdown，你可以阅读和修改。路径是 `$CODEX_HOME/memories/extensions/skysight/`，通常解析为 `~/.codex/memories/extensions/skysight/`。这些记忆文件会留到你删除或清除。时间线里可以在 Finder 中显示对应文件。

这些文件可能包含敏感信息，Computer History 不会加密它们，以同一 macOS 用户身份运行的其他程序可能读取到；要保护好 Mac 账户，并排除不想记录的来源。

发给 OpenAI 的部分，按同一页：

1. 事件在本机捕获。
2. 系统会定期开一个临时的 Codex 会话，让它访问交互事件流，把活动摘要成记忆。
3. OpenAI 在服务器上处理临时事件文件，生成记忆，记忆再存回你的 Mac。
4. 处理后不保留这些事件文件，法律要求保留的情况除外。
5. 这些事件文件不用于训练。

之后如果 ChatGPT 或 Codex 在新对话里用到一条记忆，相关的记忆内容和交互事件可能作为上下文放进那次对话。官方写明：若你的 [ChatGPT 数据控制](../10-配置模型与权限安全/23-Codex对话会被用来训练吗-数据控制与Include-environments.md)允许，这些对话内容可能用于改进模型。记忆也遵循和其他 Codex 记忆相同的对话级控制。开关具体在哪一页、个人账号和 Business 有什么差别，以那篇文章和帮助中心为准；Computer History 页本身只写了上面这一句。

## 风险：提示注入、敏感应用、token

官方单列了提示注入：Computer History 会提高来自应用和网站内容的提示注入风险。例如你打开的网页里如果带有恶意指令，ChatGPT 或 Codex 可能照着做。仓库里的 `AGENTS.md` 和下载目录是另一条进入指令的路径，见 [防范 AGENTS.md 投毒](../10-配置模型与权限安全/15-Codex防范AGENTS.md投毒-Downloads目录风险与config.toml自查.md)。两边的表面不同，处理方式相同：不可信文本不要当成必须执行的指令。打开来源不明的页面时，先暂停收集，或把浏览器排除出历史。

敏感应用按上一节处理：与他人沟通时，未事先征得同意就关掉；健康、财务和个人信息考虑暂停或排除。排除只挡住以后的事件。已经写进时间线的内容，用删除或清除去掉。

Token：Computer History 在摘要活动和创建记忆时使用 token。这一页没有写每次摘要的数量或单价。用量怎么读，见 [用量额度](../10-配置模型与权限安全/08-Codex用量额度怎么看-5小时与每周限制-Fast倍率与credits.md)。

## 清除与排障

在 **Settings > Computer history > History** 可以检查摘要、在 Finder 里显示某条摘要的本地记忆文件、删除单条，或清除最近 10 分钟、最近 1 小时、最近 1 天、全部历史。macOS 菜单栏还可以清除某个最近应用的上一段会话。

清除会删除相关的交互事件，以及由它们生成的记忆。**不能撤销。**

Memories 页另有一条：在选中的机器上选择 **Delete Codex memories** 并确认，会重置这台机器的记忆库；本机若提供 Computer History，也会一并清空。这是整库删除，不是只删一条摘要。

如果功能可用但没有开始，官方排障是三步：

1. 确认 Memories 已经打开。
2. 打开 **Settings > Computer history**，按当前状态选择 **Finish setup**、**Resume** 或 **Try again**。
3. 设置仍然不可用时，退出并重新打开 ChatGPT 桌面应用。

## 常见问题与参考资料

上面的问答放在文章信息里。操作顺序可以收成一张表。

| 你要做的事 | 官方入口 |
| --- | --- |
| 打开 | Settings > Integrations > Computer history > Turn on |
| 看时间线、提问、删除单条 | Settings > Computer history > History，或 Ask about your history |
| 排除或只包含某些应用和网站 | Settings > Computer history > Permissions |
| 暂停或恢复收集 | 菜单栏 ChatGPT 图标里的 Computer History，或设置页 |
| 清除一段时间或全部 | History，以及菜单栏里清除最近一个应用的上一段会话 |
| 连同 Codex 记忆一起清空 | Settings > Personalization > Delete Codex memories |

参考资料：

- [Computer History](https://learn.chatgpt.com/docs/customization/computer-history)（2026-11-28）
- [Memories](https://learn.chatgpt.com/docs/customization/memories)（2026-11-28）
- [Codex Memories 记忆功能](./12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)
- [Codex 对话会被用来训练吗](../10-配置模型与权限安全/23-Codex对话会被用来训练吗-数据控制与Include-environments.md)
- [Codex 使用 Computer Use 操作桌面应用](../12-官方工具与集成/03-Codex使用Computer-Use操作桌面应用.md)
