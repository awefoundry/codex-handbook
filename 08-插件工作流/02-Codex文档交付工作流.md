---
id: codex-document-delivery-workflow
title: Codex 生成文档、表格、幻灯片和 PDF（2026-11 更新）：桌面端预览与批注、官方用例里的 Skill，以及交付前怎么验收
seo_title: Codex 生成文档、表格、幻灯片和 PDF：预览、批注与交付验收
description: 用 Codex 把同一批材料做成文档、表格、幻灯片和 PDF，稳妥的顺序是先定事实和数据，再逐个生成，最后交叉核对。本文按官方文档讲清桌面端、CLI、IDE 怎么预览和修改文件，$documents、$spreadsheets、@Presentations 怎么用，以及交付清单。
lede: 生成成功不等于内容正确。先把事实和数字定下来，再生成文件；每一步只用上一步已经核对过的结果。
url: /guides/codex-document-delivery-workflow
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-12
date_modified: 2026-11-13
verified_on: 2026-11-13
official_ref: https://learn.chatgpt.com/docs/artifacts-viewer
keywords: [Codex 生成文档, Codex 做 PPT, Codex 表格, Codex PDF, Codex 文件预览, Codex 批注, $documents, $spreadsheets, "@Presentations"]
related: [codex-chajian-rukou-yu-gongzuoliu, create-codex-skill, codex-appshots]
faq:
  - q: CLI 能预览生成的 Word、Excel 或 PPT 吗？
    a: 不能。官方文档写明，Codex CLI 可以在工作目录里创建和修改文件，但没有可视化预览和批注界面，要让 Codex 报告每个输出文件的路径和它做过的检查，再用本地软件打开核对。桌面端可以在对话旁边直接预览。
  - q: 为什么我的 Codex 里没有 $documents 或 @Presentations？
    a: 官方用例页写明，可用的插件、Skill 和连接来源会因套餐和工作区而不同。开始任务前先问 Codex 当前有哪些可用工具，没有的话按插件入口安装或改用其他方式。
  - q: 批注能用在哪些文件上？
    a: 官方文档写明，桌面端的批注可以用在代码、Markdown、网页，以及文档、表格和演示文稿的预览上：选中某个部分，再说要怎么改，ChatGPT 会把选中区域当作上下文。
  - q: 幻灯片做好后想以后照着做，怎么办？
    a: 官方用例里有 $template-creator，可以把现有 PowerPoint 转成可复用的个人模板，保留版式、字体、颜色和品牌元素。官方也提醒，模板匹配和复杂的图表、形状编辑仍可能需要手动调整。
---

# Codex 生成文档、表格、幻灯片和 PDF（2026-11 更新）：桌面端预览与批注、官方用例里的 Skill，以及交付前怎么验收

> 本文在线版：[codexguide.io/guides/codex-document-delivery-workflow](https://codexguide.io/guides/codex-document-delivery-workflow)

> 核对依据：官方文档 [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer)，官方用例 [Create or revise a slide deck](https://learn.chatgpt.com/use-cases/generate-slide-decks)、[Consolidate spreadsheets](https://learn.chatgpt.com/use-cases/consolidate-spreadsheets)、[Draft PRDs from internal context](https://learn.chatgpt.com/use-cases/draft-prds-from-sources)、[Clean and prepare messy data](https://learn.chatgpt.com/use-cases/clean-messy-data)，均于 2026-11-13 核对。Skill 和插件名称按官方用例原文写。编辑部的测试机没有桌面端，没有拍到预览和批注界面，本文没有截图；提示词示例是本站整理的写法。

Codex 不只会写代码，也能把一批材料做成正式文档、带公式的表格、汇报幻灯片和 PDF。常见的翻车方式是：每个文件都「生成成功」了，但文档里的数字和表格对不上，幻灯片又用了另一版数据。

稳定的做法只有一条：**先确定事实和数据，再按顺序生成各类文件，最后交叉核对。**

## 先看结论

| 环节 | 用什么 | 要点 |
|---|---|---|
| 准备材料 | 项目目录 | 原始材料分开放，先让 Codex 列事实、缺口和冲突，不急着出文件 |
| 表格 | `$spreadsheets` | 保留原始表，计算放新表，抽几行手算核对 |
| 文档 | `$documents` | 先出结构再补正文，需求级的说法要标来源 |
| 幻灯片 | `@Presentations`（部分用例写作 `$slides`） | 先列每页要回答的问题，数字只取核对过的表格 |
| PDF | 桌面端预览；`.tex` 可边改边看 PDF | 检查页数、目录、字体、链接、分页 |
| 交付 | 交付清单 | 名称、日期、版本、核心数字在所有文件里一致 |

可用的 Skill 和插件因套餐和工作区而不同，开始前先问 Codex「你现在能用哪些文档类工具」。

## 不同入口怎么看生成的文件

官方 Work with files 文档按入口分别说明了预览和修改方式：

| 入口 | 能做什么 |
|---|---|
| ChatGPT 桌面端 | 在对话旁边预览生成的文档、演示文稿、表格和 PDF；开了自动预览时，任务结束后可以自动打开生成的文件。支持 HTML 预览时，`.html`、`.htm` 可以在渲染效果和源码之间切换。单独打开 `.tex` 文件可以一边改 LaTeX 源码一边看 PDF 预览，内置编译器可用时改完会自动重新编译；编译失败时保留上一次成功的 PDF，源码修改也不会丢 |
| 网页版 ChatGPT Work | 附上源文件或让它生成文档、演示文稿、表格、PDF，在对话里查看，需要时下载，再给出针对性的修改意见 |
| Codex CLI | 能在工作目录里创建和修改文件，但**没有**可视化预览和批注，要让 Codex 报告每个输出路径和做过的检查 |
| IDE 扩展 | 能在工作区里创建和修改文件；文本和代码在编辑器里看，文档、演示文稿、表格和 PDF 要用兼容的查看器打开 |

### 桌面端的批注

桌面端可以在预览里**批注**：选中文件的某一部分，告诉 ChatGPT 要怎么改。官方举的例子：

- 选中网页的导航栏，让它换字体；
- 选中投资分析里的一句结论，问它的来源；
- 圈出幻灯片上的一张图，要求把标签写清楚。

ChatGPT 会把选中的区域当作上下文，只改这一处，不用重新生成整个文件。官方建议在第一稿出来之后用批注做逐处修改。任务进行时，对话侧栏还会显示 agent 的计划、来源、生成的文件和对话摘要。

## 第一步：准备材料和验收标准

把原始材料放进一个项目目录，代码、会议记录、CSV、品牌模板和参考文件分开保存。涉及客户数据、合同和财务信息时，先确认当前工具的上传范围和组织策略。

第一条指令先说清交付对象、事实来源和文件要求，并且**先不生成文件**：

```text
读取 materials 目录里的项目说明、测试结果和 CSV 数据。
先列出可以确认的事实、缺失的信息和互相冲突的数据，不要生成交付文件。
我确认后，再做一份技术报告、一张指标表、一套汇报幻灯片和最终 PDF。
所有数字都必须能对应到原始文件。
```

## 第二步：用 $spreadsheets 整理数据

官方用例里，`$spreadsheets` 用来检查导出的数据、清理关联、写公式，并校验生成的工作簿。几条来自官方用例的做法很实用：

- **保留原文件**：清洗数据时写一份新的副本，原始文件不动；
- **不要编关联键**：多份表合并时，明确告诉它按哪个字段关联，不要擅自合并有冲突的记录；
- **单独列出没对上的记录**：合并不干净的行放进一个复核区，而不是悄悄丢掉；
- **附一份数据质量说明**：哪些行改了、删了、没把握清洗。

示例：

```text
用 $spreadsheets 把附件里的三份导出合并成一个可以更新的工作簿。
按「客户编号」关联，原始数据保留在单独的工作表里，计算结果放新表。
关联不上的记录放进「待复核」表，不要自己猜。
最后说明每个关键公式引用了哪些区域。
```

拿到结果后自己抽几行手算，确认求和范围、日期格式、空值和百分比口径。图表引用的区域也要单独看，避免新增数据后图表没跟着更新。

## 第三步：用 $documents 整理正式文档

官方用例里，`$documents` 用来创建、编辑和校验 DOCX，适合「要交一份正式文件，而不是在对话里给一段文字」的场景，比如根据 Linear、Slack、Notion 或 Google Drive 里的资料写 PRD。

官方 PRD 用例的提示词里有两句很值得照抄：

- 需求级的说法要**标出来源**；来源之间有矛盾时**指出冲突**，不要自己选一个；
- **只出草稿**，在你同意之前不要发帖、不要改 Linear、不要分享文档。

先让 Codex 出结构，再补正文。审阅时重点看事实有没有来源、章节有没有重复、命令和代码有没有被改错。排版好看不等于内容通过验收。

## 第四步：用 @Presentations 做幻灯片

官方「Create or revise a slide deck」用例写明：在桌面端用 `@Presentations` 可以创建或修改 PowerPoint，或从源材料新建演示文稿；连上 Google Drive 可以创建或更新原生 Google 幻灯片；也可以直接附本地文件。部分用例里写的是 `$slides`，作用同样是生成和修改可编辑的演示文稿。

按官方用例的描述，它会先把材料整理成一份简短的幻灯片计划，再生成演示文稿，并在返回前检查渲染后的页面。可以让它照着参考演示文稿或保存的模板做，保留已确认的数字和品牌元素，并标出需要补来源的说法。

几条官方给的后续提示方向：

- **照参考稿改**：保留参考稿的版式、字体、颜色、logo 和章节结构，内容和已确认数字不变；
- **换受众**：把结论、证据和下一步改得适合新受众，删掉多余细节，重要数字不动；
- **补新信息**：先找出哪些页需要改，只改相关的结论和图表，无关页面不动；
- **存成模板**：用 `$template-creator` 把现有 PowerPoint 转成可复用的个人模板，保留版式、字体、颜色和品牌元素。

官方提醒：要看**最终的幻灯片**，不只是大纲；检查故事线是否适合受众、说法和数字是否与源材料一致、页面是否易读；大改之前先复制一份重要的演示文稿，方便回退。模板匹配和复杂的图表、形状、格式编辑仍可能需要手动调整。

## 第五步：PDF 固定版式交付

导出 PDF 之前，先确认文档和幻灯片已经定稿。桌面端可以直接预览生成的 PDF；用 LaTeX 写的文档，打开 `.tex` 文件就能边改源码边看 PDF 预览。

PDF 验收要覆盖页数、目录、字体嵌入、链接、表格分页和图片清晰度。重要文件再提取一次文本，和源文件对比标题、数字和关键条款。

## 串成一条交付流程

推荐顺序：**原始数据 → 表格 → 正式文档 → 幻灯片 → PDF**。每一步只用上一步已经确认的结果；发现数字变了，回到数据源改，再重新生成下游文件。

交付前让 Codex 做一次总检查：

```text
交付前检查所有产物。
核对文档、表格、幻灯片和 PDF 里的项目名称、日期、版本号和核心数字是否一致。
列出每个文件的路径、页数或工作表数量，以及还需要人工确认的地方。
不要用「生成成功」代替内容校验。
```

用 CLI 的话，这一步更重要：CLI 没有预览，要靠 Codex 报告的路径和检查结果，再自己用本地软件打开逐个核对。

## 延伸阅读

- [Codex 插件入口与工作流](./04-Codex插件入口与工作流.md)
- [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)
- [Codex Appshots：把当前应用窗口发给对话](../12-官方工具与集成/18-Codex-Appshots-把当前应用窗口发给对话.md)
