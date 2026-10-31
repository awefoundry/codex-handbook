---
id: codex-appshots
title: Codex Appshots：同时按两侧 Command 或 Alt，把当前应用窗口发给对话，以及权限、发送目标和隐私边界
seo_title: Codex Appshots：快捷键、发送目标、权限与隐私边界
description: Appshots 把最前面的应用窗口和能读到的文字发进 ChatGPT 桌面应用的对话。本文按官方文档说明快捷键、60 秒内的发送目标、macOS 两项权限、哪些应用只有截图，以及 CLI 不能新拍。
lede: 同时按两侧 Command 或 Alt，把当前窗口交给对话。它只拍最前面的一个窗口，而且只在 macOS 和 Windows 的桌面应用里能新拍。
url: /guides/codex-appshots
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 18
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-31
date_modified: 2026-10-31
verified_on: 2026-10-31
official_ref: https://learn.chatgpt.com/docs/appshots
keywords: [Codex Appshots, Appshots 快捷键, Codex 截取应用窗口, ChatGPT 桌面应用 Appshots, Appshots 权限]
related: [codex-computer-use-desktop-apps, codex-desktop-task-workflow]
howto: false
faq:
  - q: CLI 里能新拍一张 Appshot 吗？
    a: 不能。官方写明 CLI 不能创建新的 Appshot。如果恢复的会话里已经有一张，它会作为历史附件留在会话里。
  - q: 拍进去会进哪个对话？
    a: 默认 Automatic：新开一个对话；如果你在过去 60 秒内用过某个对话，就加到那个对话。连续拍摄加在同一对话里。也可以改成 Current chat 或 New chat。
  - q: Linux 桌面应用能用吗？
    a: 官方文档只写了 macOS 和 Windows 的 ChatGPT 桌面应用。本文不把 Linux 写成支持平台。
---

# Codex Appshots：同时按两侧 Command 或 Alt，把当前应用窗口发给对话，以及权限、发送目标和隐私边界

> 本文在线版：[codexguide.io/guides/codex-appshots](https://codexguide.io/guides/codex-appshots)

> 核对依据：OpenAI 官方文档 [Appshots](https://learn.chatgpt.com/docs/appshots)，2026-10-31 核对。本文没有运行 ChatGPT 桌面应用，没有新的界面截图。快捷键、权限名称和限制都来自该页，不以旧版独立 Codex 桌面应用的界面为准。

报错窗口、设置页、设计稿，有时用文字描述不如把窗口本身交给对话。Appshots 做的就是这件事：在 macOS 或 Windows 的 ChatGPT 桌面应用里，把最前面的那个应用窗口发进对话。

官方文档的页面标题是 Appshots，对象是 ChatGPT 桌面应用。同一页写明，在 ChatGPT Work 或 Codex 里，如果装了对应的插件，还可以用插件去读相关应用的内容。它不是一条只存在于 Codex CLI 的命令。桌面应用里选择 Codex 之后，这张窗口仍然是对话附件。任务怎么接下去做，见 [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)。

## 适合什么场景

官方举的例子：

- 把 API 文档页面交给对话，让它写调用脚本。
- 把邮件或日历视图交给对话，让它起草下一步。
- 把图像编辑器、设计或预览窗口交给对话，让它改相关素材或代码。
- 把报错、设置面板或应用状态交给对话。这些用看的比用打字更快。

不适合的情况也写在同一页：你其实需要整份文档，而那个应用只交出可见区域。Google 文档一类就是这样，见下文限制。

## 怎么拍

1. 把要分享的窗口切到最前面。
2. macOS 上同时按左右两个 Command。Windows 上同时按左右两个 Alt。也可以用你在 ChatGPT 设置里改过的自定义快捷键。
3. 如果应用要求授权，先完成权限。
4. 在对话里说明要它做什么。

官方文档没有给 Linux 快捷键。支持范围写的是 macOS 和 Windows。

## 截取范围

一张 Appshot 只包含最前面的窗口。内容可以有两部分：

- 可见窗口的图像。
- 这个窗口能提供的文字，包括看得见的文字，以及应用在滚动区域之外仍然提供的文字。

加进对话之后，它和手动上传的文件、图片一样，是一条附件。官方写明，Appshot 保存在本地会话文件里。

它不会把整块屏幕上的其他窗口一起拍进去。被挡住的窗口不在这张图里。

## 发到哪个对话

默认是 Automatic：

- 新开一个对话来放这张 Appshot。
- 如果你在过去 60 秒内使用过某个对话，就加到那个对话。
- 连续拍摄会加到同一个对话。

设置里可以改 Appshot 的目的地：

| 选项 | 行为 |
|---|---|
| Automatic | 上面这条默认规则 |
| Current chat | 加到当前对话 |
| New chat | 总是新开对话 |

快捷键也在同一处设置里改。

### 桌宠浮窗

macOS 上，浮动的桌宠控件开着、主窗口在后台时，Automatic 会从这些控件新开一个带 Appshot 的对话。选了 Mini 桌宠也适用。权限要先在主应用里完成。Windows 上，Appshots 在主应用里打开。

桌宠本身怎么做，见 [Codex 创建自定义桌宠](./05-Codex创建自定义桌宠.md)。那篇讲的是宠物外观，不是 Appshots 的发送规则。

## macOS 和 Windows 的差别

| | macOS | Windows |
|---|---|---|
| 默认快捷键 | 左右两个 Command | 左右两个 Alt |
| 权限 | 可能要求 Screen & System Audio Recording 和 Accessibility | 文档没有列出这两项同名权限 |
| 桌宠浮窗 | 主窗口在后台时，可以从浮窗新开对话 | Appshots 在主应用里打开 |

排障一节写的是：打开 System Settings > Privacy & Security，检查 **Codex Computer Use** 这一项下面的 Screen & System Audio Recording 和 Accessibility。权限列表里要找的名字是 Codex Computer Use。中文版 macOS 的菜单译名以系统当前版本为准，本文不另写一个未核对的中文项名。

这两项的分工，文档写的是：

- Screen & System Audio Recording：截取最前面窗口的图像。
- Accessibility：读取最前面窗口能提供的文字。

缺了第二项，可能只剩图像，没有窗口里的文字。

## 隐私

拍下去，就会把图像和能读到的文字交给 ChatGPT。官方要求：不是任务必需的敏感内容，不要拍。审查方式和你审查截图、文档上传一样。

尤其不要拍这些，除非当前任务必须用到，并且你接受它们进入会话：

- 密码、令牌、恢复码、私钥。
- 邮箱全页、工资、病历、身份证件。
- 别人的私聊，以及还没公开的客户数据。

本地会话文件里会留下这张附件。换一台电脑或把会话交给别人之前，先想清楚文件里已经有什么。

## 限制

- CLI 不能新拍。恢复一个已经含有 Appshot 的会话时，附件还在历史里。
- Google Docs、Gmail、Google Sheets、Google Slides 这一类，可能只拿到可见截图，拿不到全文或屏幕外的文字。
- 在 ChatGPT Work 或 Codex 里，如果安装了匹配的插件，可以用插件去访问对应应用的内容。插件不是 Appshot 的替代截图，它是另一条读取途径。
- 组织策略可以禁止 Appshots。文档写明，不工作时要更新桌面应用、核对快捷键，并确认组织允许这项功能。

需要 Codex 自己去点按钮、在桌面应用里操作，那是 Computer Use，不是 Appshots。见 [Codex 使用 Computer Use 操作桌面应用](./03-Codex使用Computer-Use操作桌面应用.md)。Appshots 把窗口交给对话；Computer Use 会在获得授权后操作界面。

## 排障

按官方文档的顺序：

1. 更新 ChatGPT 桌面应用。
2. 核对设置里的快捷键没有被改成你没在按的组合。
3. 确认组织允许 Appshots。
4. macOS：打开 System Settings > Privacy & Security，检查 Codex Computer Use 的 Screen & System Audio Recording 和 Accessibility。
5. 改完权限后重启应用再试。

只拿到图、没有文字时，先看 Accessibility 是否打开，再看这个应用是不是文档里点名的 Google 文档类。后者即使权限齐全，也可能只有可见截图。

拍下去进错对话时，看目的地是不是 Automatic，以及你在 60 秒内有没有用过另一个对话。要固定进当前对话，改成 Current chat。

## 常见问题

**和系统自带截图有什么不同？** 系统截图是一张图片文件。Appshot 还尝试带上窗口提供的文字，并按上面的规则放进指定对话，存在本地会话文件里。

**可以拍 Codex 自己的窗口吗？** 文档写的是最前面的窗口。Codex 窗口在最前面时，拍到的就是它。要拍别的应用，先把那个应用切到前面。

**自定义快捷键在哪里？** 在应用设置里，和 Appshot 目的地同一处。文档没有给出菜单的中文名称，以你当前版本的设置页为准。

## 下一步

窗口已经在对话里之后，怎么选项目、并行开对话、审查改动，看 [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)。要让 Codex 操作那个应用，而不是只看一张窗口，看 [Computer Use](./03-Codex使用Computer-Use操作桌面应用.md)。

## 参考资料

- [OpenAI：Appshots](https://learn.chatgpt.com/docs/appshots)
- [OpenAI：Computer Use](https://learn.chatgpt.com/docs/computer-use)
- [OpenAI：ChatGPT desktop app](https://learn.chatgpt.com/docs/app)
