---
id: xcode-zhong-shi-yong-codex
title: Xcode 中使用 Codex（2026-11 更新）：Coding Assistant 选 Codex、小范围改代码与验证
seo_title: Xcode 中使用 Codex：Coding Assistant 选择 Codex 并核对 diff
description: Xcode 用自带的 coding assistant 选择 Codex，不安装 VS Code 那份扩展。本文按 OpenAI 的 IDE 文档和 Apple 的 Intelligence 设置页整理准备、只读任务、小范围修改和用 Xcode 测试验收。没有 Xcode 实机，截图待补。
lede: 在 coding assistant 里新建对话并选择 Codex。先解释选中的代码，再改一小块，用 Xcode 自己的测试看结果。
url: /guides/xcode-zhong-shi-yong-codex
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [IDE]
difficulty: 基础
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-07-12
date_modified: 2026-11-07
verified_on: 2026-11-07
official_ref: https://learn.chatgpt.com/docs/codex/ide
keywords: [Xcode Codex, Xcode coding assistant, Xcode Intelligence, Codex IDE, Xcode 选择 Codex]
related: [codex-vscode-install, codex-install-path-overview]
howto: false
faq:
  - q: Xcode 里要安装 openai.chatgpt 扩展吗？
    a: 不要。OpenAI 的 IDE 文档写明，VS Code 和兼容编辑器使用 Codex 扩展；Xcode 和 JetBrains 提供各自的集成。
  - q: Apple 文档里的 ChatGPT in Xcode 就是选择 Codex 吗？
    a: 两页写的不是同一句操作。OpenAI 写的是打开 coding assistant，新建对话，选择 Codex 作为 agent。Apple 的 Enable ChatGPT in Xcode 写在 Intelligence 设置的 Chat 分区，步骤是 Turn On。本文没有 Xcode，不能确认这两条在界面上是否汇合到同一次登录。
  - q: 中文菜单和文档对不上怎么办？
    a: 以文档里的英文名称为准，在 Xcode 里寻找 coding assistant、Intelligence、Agents。本地化之后的菜单名以你安装的 Xcode 为准。本文没有中文界面可以对照。
  - q: 本文在 Xcode 里跑过测试吗？
    a: 没有。写作环境没有 Xcode。步骤来自 2026-11-07 打开的 OpenAI IDE 文档和 Apple《Setting up coding intelligence》。截图待补。
---

# Xcode 中使用 Codex（2026-11 更新）：Coding Assistant 选 Codex、小范围改代码与验证

> 本文在线版：[codexguide.io/guides/xcode-zhong-shi-yong-codex](https://codexguide.io/guides/xcode-zhong-shi-yong-codex)

> 核对依据：OpenAI [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)（2026-11-07），以及该页指向的 Apple 文档 [Setting up coding intelligence](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence)。按官方文档整理，截图待补。写作环境没有 Xcode，没有登录，没有改过 Xcode 项目，也没有运行过测试。按钮的中文名以你本机的 Xcode 为准。

先看本栏目的 [安装路线总览](./01-安装路线总览.md)，确认这次要改的是已经在 Xcode 里打开的工程。VS Code、Cursor 和 Windsurf 走扩展，见 [VS Code 和兼容编辑器安装 Codex](./06-VS-Code和兼容编辑器安装Codex.md)。JetBrains 走 AI Chat，见 [JetBrains 中使用 Codex](./11-JetBrains中使用Codex.md)。

## 先看结论

- Xcode 使用编辑器自带的集成。OpenAI 的打开说明是：打开 coding assistant，新建对话，选择 Codex 作为 agent。
- 同一页把 Xcode 的设置文档链到 Apple。Apple 写的启用路径是 Xcode > Settings，侧栏选 Intelligence，或在 coding assistant 侧栏点 “Get Started with Agents”。
- 适合的任务是：用已经打开的文件和选中代码做解释、做范围清楚的修改、就地看 diff。任务变大时，官方 IDE 文档写可以交给 Codex web。
- 验收放在 Xcode 里：看 diff，再跑你项目已有的测试或构建。Apple 写明，在 coding assistant 里选用的 agent 可以使用 Xcode 的能力，例如构建和测试。对话里的一句 “已经通过” 不能代替这次运行。

## Xcode 集成和 VS Code 扩展

官方 IDE 文档把编辑器分成两类：

| 编辑器 | 官方怎么装、怎么开 |
|---|---|
| Visual Studio Code、Cursor、Windsurf、VS Code Insiders | 安装 Codex 扩展。点 Codex 图标；看不到时，命令面板运行 Codex: Open Codex Sidebar |
| Xcode | 自带集成。打开 coding assistant，新建对话，选择 Codex 作为 agent |
| JetBrains IDE | 自带集成。打开 AI Chat，选择 Codex |

扩展的标识符 `openai.chatgpt` 只用于前一类。Xcode 的获取入口在 IDE 文档里是单独的链接，打开的是 Apple 的 Intelligence 设置页，不是 Visual Studio Marketplace。

官方 IDE 页同时描述三类用法，不区分菜单属于哪一个编辑器：用已经打开的上下文、在代码旁边审查改动、任务变大时委托出去。下面的 Xcode 步骤只采用文档里点名 Xcode 的那几句，加上 Apple 设置页里写明的启用和登录。没有点名 Xcode 的界面细节，不写成 Xcode 一定有同名按钮。

## 版本与项目准备

2026-11-07 打开的两份文档都没有在正文里写最低 Xcode 版本号。以你的 Xcode 能否出现 coding assistant，以及能否在 agent 列表里选择 Codex 为准。

开始之前：

- 用 Xcode 打开项目目录，而不是只打开一个脱离工程的源文件。官方 IDE 文档的第一步聊天是 Open a project。
- 确认工程至少能打开目标文件。最好先在本机完成一次你平时用的构建或测试，这样后面的失败更容易和这次修改分开。
- 工作区已有改动时，先提交或另做检查点。官方 IDE 文档写明：任务前后建立 Git 检查点，以便回退。
- 签名证书、私钥、描述文件和配置里的令牌不要放进对话。Apple 写明，你在 coding assistant 里输入提示时，Intelligence 设置中启用的 agent 可能访问项目文件和其他信息。说明在 Intelligence 设置里的 “About Intelligence in Xcode & Privacy…”。

托管设备上，Apple 写明可以用 MDM 键 `CodingAssistantAllowExternalIntegrations` 设为 `false` 来关闭 coding assistant 的外部集成。公司电脑上如果根本没有 Intelligence 或 coding assistant，先问管理员，而不是换一份额扩展安装包。

## 打开 Coding Assistant 并选择 Codex

按 OpenAI 文档，Xcode 里的操作是三步里的第二步：

1. 打开 coding assistant。
2. 新建对话。
3. 选择 Codex 作为 agent。

Apple 文档写的是启用 agent 的设置，不是 “Codex” 这个名字的逐步截图。按那一页操作时：

1. 打开 Intelligence 设置：菜单 **Xcode > Settings**，在侧栏选择 **Intelligence**。也可以在 coding assistant 侧栏点击 **Get Started with Agents**。
2. 在 **Agents** 下面，对要启用的 agent 点 **Get**，在随后的对话框里点 **Install**。Apple 写明，下载安装之后，Xcode 会在可能的情况下自动更新这些下载。
3. 已有账号时，在该 agent 的设置里，**Account** 一行点 **More**（…），按后续窗口和浏览器里的说明登录。隐私政策和条款链接在 Account 下面。

Apple 另有一节 **Enable ChatGPT in Xcode**，位置在 Intelligence 设置的 **Chat** 分区：点 **Turn On**，再在对话框里点 Next 和 **Turn On ChatGPT**。登录是在 ChatGPT in Xcode 设置的 ChatGPT 一行点 **Sign In**。这一节还写了可以不登录使用、可以登录免费或付费账号，以及 “Upgrade to ChatGPT Plus” 的链接。推理强度在对话记录窗格底部的 **Reasoning** 弹出菜单里选择，Apple 把它写在 ChatGPT 这一节。

OpenAI 文档点名的是 “choose Codex as the agent”。Apple 的 ChatGPT 一节没有出现 Codex 这个词。本文把它们保持为文档里的两条路径。没有 Xcode，不能写 “点某一个中文按钮就会同时完成两件事”。你在 Agents 列表里看到 Codex 时，按 OpenAI 的句子选择它。只看到 ChatGPT in Xcode、没有名为 Codex 的 agent 时，以当前 Xcode 的列表为准，并对照 Apple 那一页的 Chat 分区。不要为了补一个扩展，去 Marketplace 搜索 Codex。

登录完成之后，官方 IDE 文档的第三步是：打开项目，让 Codex 解释代码库、做一处集中的修改，或帮助调试。当前打开的文件、选中的代码和最近的对话，可以被写进提示。文档的原意是少重复叙述你正在看的代码。

## 先做只读任务

选中一个函数或一段你能自己读完的代码，发一条不改文件的请求。范围写进句子里：

```text
Explain the selected function: its inputs, outputs, and side effects. Do not edit any file.
```

对照解释和源码。解释对不上选区时，先把文件和选区重新附上，或换一句更短的问题。这一步通过，只说明它读到了你给出的代码。

官方 IDE 文档把 “学习还不熟悉的代码” 写成：询问编辑器里已经打开的文件和符号。只读任务就停在这个范围。

## 小范围修改，并看 diff

只读解释对得上之后，再发一条改动范围写死的请求。例如只给当前函数补失败分支的测试，不改生产代码。一次只交一个结果，避免把重构和测试捆在同一句里。

官方 IDE 文档对 “在代码旁边审查” 的写法是：读简短摘要，查看集中的 diff，在同一条对话里继续追问。只保留你要的改动。它没有把 Xcode 的 diff 控件名称写成一份清单。你在 Xcode 里看到的对比界面，以当前版本为准。

看 diff 时核对三件事：

- 改动是不是停在你点名的文件和函数。
- 有没有顺手改签名、资源或工程设置。
- 测试文件的断言是不是在测你要求的失败分支。

不需要的部分不要留在工作区里。官方文档写的是保留你想要的改动。具体是还原文件还是在对话里要求重做，随 Xcode 当时的控件。本文没有这份控件的截图。

任务明显变大、需要更长时间时，官方 IDE 文档写可以连接 Codex web，再回到编辑器里看可审查的结果。本文没有在 Xcode 里交过云端任务。云端环境的准备见 [Codex Cloud 云端环境](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)。

## 用 Xcode 的测试做验收

Apple 写明：在 coding assistant 里选择的 agent，自动可以使用 Xcode 的能力，例如构建和测试你的 app。这表示它可以发起这些动作。验收仍由你看 Xcode 的结果：

1. 用你平时的 scheme 运行相关测试，或至少构建这次改到的目标。
2. 失败时，把测试输出里的失败断言交给下一次对话，并写明不要扩大修改范围。
3. 通过之后再看一遍 diff，确认没有为了让测试变绿而改掉无关行为。
4. 保留 Git 检查点。需要回退时回到任务前的检查点，而不是只靠对话里的 Undo 描述。

对话里列出的 “Validation passed” 来自官方 IDE 页的示例文案，不是你工程的测试报告。以 Xcode 的 Report 或测试导航器里这次运行的结果为准。

## 敏感内容

- 不要把证书、私钥、描述文件、令牌和客户数据贴进提示，也不要让任务 “顺便把签名配置整理一遍”。
- Apple 写明 agent 处理请求时可能访问项目文件。提交前看 diff，确认这些材料没有被写进源文件或新文件。
- 隐私说明在 Intelligence 设置的 “About Intelligence in Xcode & Privacy…”。账号一行下面有隐私政策和条款链接。
- API Key 如果出现在登录窗口里，只填在那个窗口。不要发到聊天框，也不要写进仓库。密钥从平台控制台获取的说明见 [登录 Codex](./07-登录Codex.md)。

## 常见问题

**侧栏里没有 Codex。**

先按 Apple 的路径打开 Intelligence，看 Agents 下面有没有需要点 Get / Install 的条目，再新开一条 coding assistant 对话并选择 agent。OpenAI 文档没有写 Xcode 的命令面板标题。不要改去安装 `openai.chatgpt`。

**能把整个工程交给它重写吗？**

官方 IDE 文档把编辑器里的 Codex 对应到范围清楚的修改、阅读不熟悉的代码和就地审查。更大的任务可以委托到 Codex web。第一次使用时，停在一个函数和它的测试上。

**JetBrains 的登录方式能直接套用吗？**

不能。JetBrains 的 AI Chat 是另一条集成，见 [JetBrains 中使用 Codex](./11-JetBrains中使用Codex.md)。Xcode 的登录以 Apple 文档的 Account / Sign In 为准。

## 参考资料

- [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [Setting up coding intelligence](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence)（Apple Developer Documentation，由 IDE 文档的 Xcode 链接打开）
- [Authentication](https://learn.chatgpt.com/docs/auth)
