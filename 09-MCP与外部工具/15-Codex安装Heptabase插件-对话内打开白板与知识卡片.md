---
id: codex-heptabase-plugin-whiteboard
title: Codex 安装 Heptabase 插件：在对话里打开白板，读写卡片、Journal 与思维导图
seo_title: Codex 安装 Heptabase 插件：对话内白板、卡片与 Journal
description: Heptabase 的官方插件让 ChatGPT 和 Codex 搜索、读写卡片和 Journal，并在对话里打开白板。本文按帮助中心整理安装、CLI 与 App 的差别、只读权限和套餐边界。写作时没有 Heptabase 账号。
lede: 从插件目录安装并登录。App 里可以直接打开白板；CLI 要同时开着已登录的 Heptabase 桌面或网页。免费协作账号不要按付费空间的写入能力来预期。
url: /guides/codex-heptabase-plugin-whiteboard
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI]
difficulty: 进阶
order: 15
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-07
date_modified: 2026-11-07
verified_on: 2026-11-07
official_ref: https://support.heptabase.com/en/articles/17120206-use-heptabase-with-chatgpt-and-codex
keywords: [Codex Heptabase 插件, Heptabase 白板, Heptabase Journal, Codex @Heptabase, Heptabase MCP]
related: [codex-chajian-rukou-yu-gongzuoliu, mcp-getting-started]
howto: false
faq:
  - q: 这是 OpenAI 官方插件吗？
    a: 不是。帮助中心写的是 official Heptabase plugin，由 Heptabase 提供，装在 ChatGPT 和 Codex 共用的插件目录里。OpenAI 的插件文档只被 Heptabase 拿来提醒步骤可能随产品更新变化。
  - q: 免费账号能把 Journal 和自己的白板都交给 Codex 改吗？
    a: 不要这样预期。帮助中心的免费方案说明写明，免费协作账号不能使用 Journal、个人白板和卡片库、标签数据库等。插件页没有把写入能力承诺给免费账号。MCP 页写明，连只读的 MCP 也需要 Pro、Premium、Premium+ 或有效试用。
  - q: Codex CLI 里能像 App 一样在对话中嵌一块白板吗？
    a: 帮助中心写的是，在 ChatGPT 和 Codex App 里可以在对话中打开白板。Codex CLI 把结果做成文本，并要求 Heptabase 桌面或网页保持打开且登录同一账号。本文没有 CLI 画面。
  - q: 只想让它搜索、不想让它改卡片，怎么做？
    a: 连接时授予的权限决定能力。帮助中心写明，只读连接可以搜索和阅读，不能创建或编辑。要改内容，需要重新连接并授予写权限。
---

# Codex 安装 Heptabase 插件：在对话里打开白板，读写卡片、Journal 与思维导图

> 本文在线版：[codexguide.io/guides/codex-heptabase-plugin-whiteboard](https://codexguide.io/guides/codex-heptabase-plugin-whiteboard)

> 核对依据：Heptabase 帮助中心 [Use Heptabase with ChatGPT and Codex](https://support.heptabase.com/en/articles/17120206-use-heptabase-with-chatgpt-and-codex)（2026-11-07 打开，页面写着 Updated today）、[Heptabase MCP](https://support.heptabase.com/en/articles/12679581-heptabase-mcp)、[Does Heptabase offer a free plan?](https://support.heptabase.com/en/articles/10519305-does-heptabase-offer-a-free-plan)，以及 [@Heptabase 2026-11-06 13:43 UTC 的帖子](https://x.com/Heptabase/status/2118700918497550395)。这是 **Heptabase** 的第三方插件，不是 OpenAI 编写的内置功能。本文没有 Heptabase 账号，没有安装插件，没有白板截图。步骤按上述文档整理。

适合已经在用 Codex，并且把笔记、Journal 或白板放在 Heptabase 里的人。插件入口的通用规则见 [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)。手动添加 MCP 服务器的一般做法见 [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。Heptabase 这条官方插件路径不要求你自己写 MCP 配置。

## 先看结论

Heptabase 帮助中心写明：用官方插件，就可以从 ChatGPT 或 Codex 使用你的卡片、Journal、白板和标签数据库。不需要打开 Developer mode，不需要自己配置 MCP 服务器，也不需要安装 Heptabase CLI。

2026-11-06 的官方帖子补充的界面能力是：可以在 Claude Code 和 Codex 里直接打开并编辑白板，也可以在 ChatGPT 和 Claude 里这样做。你可以让代理排列卡片、建分区、画连线或做思维导图，并随时自己改。

套餐要分开看：

- 插件帮助页没有写 “免费账号拥有全部写入能力”。
- MCP 帮助页写明：MCP 需要 Heptabase Pro、Premium 或 Premium+，或一份有效的免费试用。只读连接也在这条要求里。同一页让 ChatGPT、Codex、Claude、Claude Code 的用户改用官方插件，把 MCP 页留给其他服务或手动连接。
- 官方帖子写：如果你已经是 Heptabase Pro，不必为了很好的 AI 体验再升到 Premium，可以用现有 Claude Code 和 Codex 订阅里的 token。这句说的是用你自己的订阅，不是免费协作账号的权限清单。
- 免费方案帮助页写明：免费计划只通过协作获得。免费用户可以在有协作权限的空间里编辑白板和卡片；不能使用 Journal、个人白板和卡片库、标签数据库、Tasks、Highlights 和 AI 相关功能。新用户可以点 Upgrade 试 7 天订阅试用。

本文没有账号，不能替你确认插件登录时是否再拦一层套餐。按文档准备时，把 Pro、Premium、Premium+ 或有效试用当作可以使用这套连接的前提，不要把 Journal、个人库和标签库的写入承诺给免费协作账号。

帮助中心的插件文没有给出插件包的 Git 仓库和许可证。本文不把别的 Heptabase CLI 仓库当成这个插件的源码。

## 安装与登录

ChatGPT 和 Codex 共用同一个插件目录。帮助中心的步骤是：

1. 在 ChatGPT 或 Codex 里打开 Plugins Directory。
2. 搜索 Heptabase 并安装。
3. 登录 Heptabase，查看权限，批准连接。
4. 新开一个 ChatGPT 对话或 Codex 任务。让助手使用 Heptabase，或输入 `@Heptabase` 选中它。

Codex CLI 的对应写法是：输入 `/plugins` 安装 Heptabase，然后新开一个会话。

帮助中心提醒，OpenAI 更新应用之后步骤可能变化，并指向 OpenAI 的插件说明。Codex 侧的目录、`/plugins` 和 “装完要新开会话” 与 [插件入口](../08-插件工作流/04-Codex插件入口与工作流.md) 一致。

本文没有在 `/plugins` 里搜索到 Heptabase，也没有完成登录。搜索结果里的发布者名称以你客户端当时的目录为准。

## App 里打开白板，和 CLI 不一样

帮助中心把 “在对话里打开白板” 写在 ChatGPT 和 Codex App 上：助手可以打开你的一块白板，你在对话里浏览和编辑，并看到助手的修改。示例问法是：Open my 'Mindstorms' whiteboard。你可以换白板、打开其中的卡片。你说 “this whiteboard” 或 “this card” 时，助手会先看你当前打开的是哪一块。

Codex CLI 的差别，同一页写了两句：

- 白板编辑和另外几项动作在 Heptabase 应用里执行。CLI 要让 Heptabase 桌面应用或网页保持打开，并登录同一个账号。
- CLI 把结果做成文本，而不是交互式预览。

从电脑上传文件，需要一个能跑命令的助手，帮助中心举的例子是 Codex。在 ChatGPT 里，助手可以从链接保存文件。

所以：

- 想在对话窗口里看着白板改：用 ChatGPT 或 Codex App，按帮助中心的说法。
- 人在终端里：安装插件之后，同时打开已登录的 Heptabase 桌面或网页。不要期待 CLI 里出现一块可拖拽的白板。本文没有这两种界面。

MCP 页还写了：白板编辑、编辑和查询标签数据库、从标签数据库移除卡片、重命名、读取 backlinks，都要在 Heptabase 应用里跑。手机应用不执行这些动作。Heptabase 开着时，助手也会从应用里读，因此能看到还没同步完的编辑。插件页把 “在对话里打开 Heptabase” 写成 ChatGPT 和 Codex App 的做法，用来代替 “自己先打开应用”。两页对 CLI 的要求一致：应用或网页要开着。

## 能做什么

插件页列出的能力：

- 搜索并阅读卡片、Journal、白板、标签数据库、PDF、图片、高亮和 backlinks。
- 创建和编辑笔记卡片与 Journal，包括图片、视频、音频和附件。
- 从文件或链接创建 PDF、图片、音频、视频、网页和 YouTube 卡片。
- 创建和编辑标签数据库，把卡片加进去或移出，设置卡片属性，整理标签，把卡片放进垃圾桶或恢复。
- 阅读和整理 Inbox，阅读或设置 Space Instructions。
- 创建白板、分区、连线和思维导图，并排列上面的对象。
- 在对话里显示卡片；在 ChatGPT 和 Codex App 里打开白板。

帮助中心给的例子是：

- 找出关于 Mindstorms 的卡片，总结主要想法，并显示最相关的卡片。
- 把这次讨论的要点追加到今天的 Journal。
- 把一篇论文链接存成 PDF 卡片，并总结第一节。
- 打开名为 Mindstorms 的白板，按主题把卡片分成区块。

卡片被找到、创建或编辑之后，可以让助手显示这张卡片。选中预览再选 Open in Heptabase，就可以回到 Heptabase 里继续。本文没有这条预览。

官方帖子还写了：用 Web Clipper 存了很多文章和论文时，可以让代理处理 Inbox、把卡片放到合适的白板，并管理标签和属性；外部代理可以读 Space Instructions，按你自己的规则整理知识库。帖子同时写明，这些更新不会在你不想用时把 AI 功能塞进 Heptabase。

## 权限与只读

插件页和 MCP 页都写了同一条边界：助手能做什么，取决于连接时你授予的权限。只读连接可以搜索和阅读，不能创建或编辑。MCP 页补了一句：要让助手修改，就重新连接并授予写权限。

批准之前先看授权页上的账号和权限范围。连错账号时，助手找不到你以为已经同步的内容。帮助中心的排障也把 “检查是不是连对了账号” 写成一步。

只读足够做 “找出并总结”。追加 Journal、改白板、建卡片，都超出只读。免费协作账号即使人可以在受邀空间里编辑白板，也不要把 Journal 和个人卡片库算进插件一定能写的范围。那份清单在免费方案帮助页里是账号不能使用的功能。

## 排障

帮助中心列出的检查顺序：

- 安装之后新开一个对话或 Codex 任务。
- 助手没有用 Heptabase 时，输入 `@Heptabase`。
- 动作像是缺失或过期时，在插件设置里选 Refresh，然后新开对话。
- 找不到内容时，核对连接的是不是那个 Heptabase 账号。
- 连接过期就重新连接。反复过期时，联系 Heptabase 支持，说明你用的应用、出错时间和错误信息。

不要把密码、API Key 或授权 token 发给 Heptabase 支持。这是帮助中心的原话。

白板在 CLI 里没有出现时，先确认 Heptabase 桌面或网页已经打开，并且登录的是同一个账号。帮助中心把交互式白板放在 ChatGPT 和 Codex App，把 CLI 的结果写成文本。

仍想用手动 MCP 或其他客户端时，帮助中心把那条路放在 “Other connection methods”，服务器写在 MCP 页，不在本文展开。那条路需要 Developer mode 或各客户端自己的 MCP 配置，也带有上面的套餐要求。

## 怎么判断连接可用

本文没有账号，下面是文档里的验收，不是一次实测输出：

1. 新会话里用 `@Heptabase` 做一次只读搜索，例如找出某个你知道存在的卡片标题。只读权限下，这一步不应创建卡片。
2. 需要写入时，确认授权不是只读，再用一块测试白板或一条测试 Journal 做小改动，然后在 Heptabase 里打开同一条内容核对。
3. App 路径再试一句 “打开某块白板”。CLI 路径同时确认桌面或网页已登录。对不上时，用上一节的 Refresh 和新会话，而不是反复重装。

## 参考资料

- [Use Heptabase with ChatGPT and Codex](https://support.heptabase.com/en/articles/17120206-use-heptabase-with-chatgpt-and-codex)
- [Heptabase MCP](https://support.heptabase.com/en/articles/12679581-heptabase-mcp)
- [Does Heptabase offer a free plan?](https://support.heptabase.com/en/articles/10519305-does-heptabase-offer-a-free-plan)
- [@Heptabase，2026-11-06](https://x.com/Heptabase/status/2118700918497550395)
- OpenAI 插件步骤会变化时的对照：[Plugins](https://learn.chatgpt.com/docs/plugins)
