---
id: codex-image-inputs
title: "Codex 图片输入：截图和设计稿怎么发给 Codex，App、IDE 按住 Shift 拖入，CLI 用 codex -i 一次传多张，提示词怎么围绕图片写"
seo_title: "Codex 图片输入：Shift 拖入、codex -i 与提示词"
description: "报错截图、界面设计和架构图可以附在提示词里，但图片不能单独把任务说完。本文按官方文档说明桌面端、网页、IDE 和 CLI 怎么附图，多张图怎么比较，以及从截图做原型时文字还要补什么。"
lede: "按住 Shift 把图拖进输入框。CLI 用 codex -i 或 --image。看哪一块、要什么结果、有什么约束，写在文字里。"
url: /guides/codex-image-inputs
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App, IDE, CLI]
difficulty: 基础
order: 39
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-28
date_modified: 2026-11-28
verified_on: 2026-11-28
official_ref: https://learn.chatgpt.com/docs/image-inputs
keywords: [Codex 图片输入, Codex 截图, codex -i, codex --image, Codex 设计稿还原, Prototype from a screenshot]
related: [codex-prompting-gpt-6-2, codex-appshots, codex-cli-commands-cheatsheet, codex-images-2-6]
howto: true
faq:
  - q: "IDE 里把图片拖进对话，为什么进了编辑器？"
    a: "官方写明要按住 Shift 再拖。不按 Shift 时，拖放会被编辑器接走，扩展收不到这张图。"
  - q: "CLI 一次怎么传多张图？"
    a: "路径用逗号分隔，或重复 --image。官方示例是 codex --image before.png,after.png，后面跟提示词。提示词里要逐张说明各是什么、怎样比较。"
  - q: "只贴一张图、不写文字，可以吗？"
    a: "不可以当作完整任务。官方要求说明要检查什么、要什么结果。多张图还要标明每一张，并说明怎么比较。图上看不到的悬停、校验和键盘操作要写进文字。"
  - q: "codex exec fork 加了 --image，为什么还要提示词？"
    a: "Developer commands 写明：使用图片时必须提供提示词。不给提示词时，fork 只复制会话，不会开始新的一轮。"
---

# Codex 图片输入：截图和设计稿怎么发给 Codex，App、IDE 按住 Shift 拖入，CLI 用 codex -i 一次传多张，提示词怎么围绕图片写

> 本文在线版：[codexguide.io/guides/codex-image-inputs](https://codexguide.io/guides/codex-image-inputs)

> 核对依据：2026-11-28 打开的 [Image inputs](https://learn.chatgpt.com/docs/image-inputs)、[Prompting](https://learn.chatgpt.com/docs/prompting) 的 Prototype from a screenshot、[Developer commands](https://learn.chatgpt.com/docs/developer-commands) 里 `codex exec fork` 与 `--image`、[Codex CLI](https://learn.chatgpt.com/docs/codex/cli) 的 Bring visual context into the prompt、[Image generation](https://learn.chatgpt.com/docs/image-generation) 和 [Appshots](https://learn.chatgpt.com/docs/appshots)。没有登录桌面端或 IDE，没有在本机执行这些附图命令。文中的命令和英文提示词按这些页面原文引用。

任务取决于一张图时，把图放进提示词：报错截图、界面设计、架构图，或已有的素材。图只提供视觉上下文。要看哪一块、做成什么样、哪些不能动，仍然写在文字里。提示词的其他写法见 [写给 GPT-6.2 的提示词](../02-核心概念与任务方法/10-Codex提示词怎么写给GPT-6.2-推理强度-子代理-视觉参考与精简AGENTS.md.md)。

## 先说结论

按 2026-11-28 的 Image inputs 页：

- 桌面端和 IDE 扩展：按住 Shift，把图片拖进输入框。IDE 不按 Shift，拖放会被编辑器接走。
- 桌面端也可以让它查看本机上的图片，或用截图工具核对其在另一个应用里的结果。
- 网页：附加、粘贴或拖入，并在提示词里说明要检查什么、要什么结果。
- CLI：交互输入框可以粘贴；也可以 `codex -i` 或 `codex --image` 在第一条提示词里带上文件。
- 多张图用逗号分隔路径，或重复 `--image`。常见格式包括 PNG 和 JPEG。这一页没有写文件大小上限，也没有把格式名单列全。
- 不要只靠图片传达任务。

## 各入口怎么附图

### 桌面端

按住 Shift，把图片拖进提示词输入框，作为上下文。官方还写了两种不经过拖放的做法：让 ChatGPT 查看你系统上的一张图片，或用截图工具去核对另一个应用里的工作。

菜单上的按钮名，这一页没有逐项列出。没有打开桌面端，这里不补界面上的点击路径。

### 网页

把图片附加、粘贴或拖进 ChatGPT 网页的输入框。提示词里说明要检查图的哪一部分，以及你要从这张图得到什么结果。

### IDE 扩展

同样是按住 Shift 把图片拖进输入框，让扩展接收这次拖放，而不是把文件交给编辑器。Prompting 页在「从截图做原型」的 IDE 流程里写的是拖放或粘贴。两页合在一起的操作是：在 Codex 对话里附图时按住 Shift；也可以粘贴。

### CLI

两种方式都写在文档里。

交互会话里，把图片粘贴进输入框。Codex CLI 页的说法是：用 `codex --image` 把报错截图、架构图或设计参考和第一条提示词一起传入，或把图片粘贴进交互输入框。

命令行一次传入文件时，Image inputs 页的原文是：

```bash
codex -i screenshot.png "Explain this error and suggest the smallest fix"
codex --image before.png,after.png "Compare these states and list the regressions"
```

第一句是解释这张报错图，并建议最小的修复。第二句是比较前后两个状态，列出回退。引号里的英文是官方示例，可以改成你的任务，路径换成你的文件。

子命令和启动参数的总表见 [CLI 命令速查](../16-图解与速查/01-Codex-CLI命令速查-子命令与启动参数.md)。

## 多张图怎么传、怎么比较

官方写了两种传法：路径用逗号分隔，或重复 `--image`。上面的 `before.png,after.png` 就是逗号写法。重复旗标时，每一张图各跟一个 `--image`。

只把多张图丢进去不够。Image inputs 页要求：附上多于一张图时，标明每一张是什么，并说明应该怎样比较。例如一张是现在的结账页，一张是设计稿，比较的是间距和字体，行为不要改。这个例子的完整提示词在下一节。

图片生成页在「使用多张参考图」里另有一句，针对的是生成或编辑：用顺序标明每一张（Image 1、Image 2），说明它们的关系，合并元素时用前景、背景、左、右这类空间词。那是生成任务的写法。让 Codex 阅读已有截图时，仍以 Image inputs 页为准：点名每一张，并写明比较方式。

## 提示词怎么围绕图片写

Image inputs 页的要求是三件事：说出图上是什么，指出要紧的区域，写明输出和约束。

官方示例：

```text
Compare this checkout screen with the design. Fix spacing and typography only;
do not change behavior. Verify the result with a new screenshot.

```

中文意思是：把这个结账界面和设计稿比较。只修间距和字体，不要改行为。用一张新的截图核对结果。

「只修间距和字体」就是约束。「用新截图核对」是验收，不是再附一张旧图。图上如果同时有布局问题和按钮逻辑问题，而你只想改布局，这句话要写出来，否则模型会按它自己对整张图的理解去改。

## 从截图做原型

Prompting 页的 **Prototype from a screenshot** 用于把设计稿、截图或界面参考做成可运行的原型。

CLI 流程原文是四步：

1. 把截图存在本地，例如 `./specs/ui.png`。
2. 运行 `codex`。
3. 把图片文件拖进终端，附到提示词上。
4. 再用文字补上约束和结构。官方示例：

```text
Create a new dashboard based on this image.

Constraints:
- Use react, vite, and tailwind. Write the code in typescript.
- Match spacing, typography, and layout as closely as possible.

Outputs:
- A new route/page that renders the UI
- Any small components needed
- README.md with instructions to run it locally

```

这段的意思是：按这张图做一个新的仪表盘。约束是 React、Vite、Tailwind，用 TypeScript，并尽量对齐间距、字体和布局。产出是一条新路由或页面、需要的小组件，以及说明如何在本地运行的 README。

官方对这段的说明，原文可以收成三条：

- 图片提供的是视觉要求。框架、路由和组件风格仍然要你用文字写。
- 图上看不到的行为要写进文字，例如悬停、校验规则、键盘交互。
- 验收时让 Codex 启动开发服务器（若权限允许），并告诉你具体看哪里。官方提示词是：

```text
Start the dev server and tell me the local URL/route to view the prototype.

```

IDE 流程是：在 Codex 对话里附上图片（拖放或粘贴），然后使用：

```text
Create a new settings page. Use the attached screenshot as the target UI.
Follow design and visual patterns from other files in this project.

```

意思是：做一个新的设置页，以附图为目标界面，并沿用项目里其他文件的设计和视觉模式。拖进 IDE 时按住 Shift，见上一节。

## 修完怎么验证

图片输入页的结账示例把验收写进了同一句：用一张新的截图核对。原型流程则是让 Codex 启动开发服务器，并报告本地 URL 和路由。

两段都是「改完要有一个你能自己打开的结果」。服务器有没有真的起来、页面是否和设计稿一致，以你打开那个地址看到的为准。文档没有把「Codex 说已经对齐」写成验收。

Prompting 页另有一节 Iterate on UI with live updates：在另一个终端运行 `npm run dev`，再用小步提示词改样式。那是设计稿落地之后的迭代，不是附图本身。命令保持文档原文，项目如果不用 npm 或 Vite，不要照抄这条启动命令。

## 非交互命令里带图

Developer commands 写的是 `codex exec fork`，不是一条单独的 `codex exec --image` 总说明。原文要点：

- `codex exec fork [PROMPT]` 把已保存的会话复制成新会话。会话参数可以是 UUID 或名字。
- 不给提示词时，fork 只建立副本，不开始新的一轮。
- 提示词用 `-` 表示从标准输入读取。
- 加上 `--image` 可以附图。
- **使用图片时必须提供提示词。** 同一句还列出 `--output-schema`、`--output-last-message` 和 `--ephemeral`：用了这些也必须有提示词。

因此非交互地 fork 并附图时，提示词和 `--image` 要一起出现。交互式的 `codex -i` 和 `codex --image` 示例以 Image inputs 页为准，那两行本身已经带了引号里的提示词。

## 图片输入、图片生成与 Appshots 的区别

三件事都和「画面」有关，官方文档把它们分开写。

| | 你给它什么 | 它做什么 | 文档怎么划界 |
| --- | --- | --- | --- |
| 图片输入 | 已有的截图、设计稿、架构图或素材 | 看图，再按文字完成编码或说明 | Image inputs：要它检查视觉参考时用输入 |
| 图片生成 | 文字描述，可选一张或多张参考图 | 生成或编辑一张图 | Image inputs 指向 Image generation：要它创建或编辑图片时用生成。生成页写明可以用 `-i` 或 `--image` 附上已有图作为引导，IDE 里拖参考图同样要按住 Shift |
| Appshots | 不先准备文件。在 macOS 或 Windows 的桌面应用里，同时按两侧 Command 或两侧 Alt | 把最前面的一个窗口发给对话，可以包含窗口图像和能读到的文字 | 只在桌面应用里新拍。恢复一条已经带有 Appshot 的会话时，CLI 能看到历史里的附件，但不能新拍 |

生成 GIF、overlay 圈选编辑，见 [Codex Images 2.6](./19-Codex-Images-2.6-GIF生成与overlay编辑.md)。快捷键、60 秒内的发送目标和 macOS 权限，见 [Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)。本文只整理「把已有图片交给 Codex 看」。

Appshots 在 macOS 上可能要求屏幕与系统音频录制，以及辅助功能，用来拍窗口、读文字。那是拍摄时的权限。[Computer History](../11-自动化与高级工作流/17-Codex-Computer-History怎么用-开启条件-记录什么-本地存储与隐私控制.md) 不需要屏幕录制，也不把截图放进历史。那是活动记录，不是把一张设计稿发给当前对话。

## 常见问题与参考资料

附图之前先写一句文字：这张图是什么、看哪个区域、交付什么、什么不能改。多张图再加一句每张图的角色。原型任务把框架和路由写进 Constraints，把图上没有的交互写进文字，最后让它报告本地地址，由你自己打开。

参考资料：

- [Image inputs](https://learn.chatgpt.com/docs/image-inputs)（2026-11-28）
- [Prompting](https://learn.chatgpt.com/docs/prompting)（2026-11-28，Prototype from a screenshot）
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)（2026-11-28）
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)（2026-11-28）
- [Image generation](https://learn.chatgpt.com/docs/image-generation)（2026-11-28）
- [Appshots](https://learn.chatgpt.com/docs/appshots)（2026-11-28）
