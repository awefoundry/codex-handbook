---
id: codex-images-2-6
title: Codex Images 2.6：在 Codex 里生成 GIF、overlay 圈选编辑，全套餐可用
seo_title: Codex Images 2.6：GIF、overlay 编辑、用量与 API 模型
description: OpenAI 于 2026-11-04 把 Images 2.6 带到 ChatGPT、Codex 和 API。本文按官方说明整理 Codex 里如何生成与编辑图片、GIF 提示怎么写、overlay 圈选和侧栏有何不同，以及用量与 Flare、Sunburst 怎么分工。
lede: 先分清三件事：在对话里出图、在 API 里选 Flare 或 Sunburst、以及「看当前窗口」和「操作别的桌面应用」。
url: /guides/codex-images-2-6
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, IDE]
difficulty: 基础
order: 19
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
models: [gpt-image-2, gpt-image-2.6-flare, gpt-image-2.6-sunburst]
official_ref: https://openai.com/index/introducing-images-2-6/
keywords: [Codex Images 2.6, Codex GIF, overlay 编辑, gpt-image-2.6-flare, gpt-image-2.6-sunburst, $imagegen]
related: [codex-computer-use-desktop-apps, codex-changyong-gongneng-qingdan]
faq:
  - q: Codex 对话里的内置出图，模型名是 Images 2.6 还是 gpt-image-2？
    a: 2026-11-04 的官方博客写明 Images 2.6 已进入 ChatGPT 与 Codex。同一时期的用法文档仍写内置图像生成使用 gpt-image-2，并计入 Codex 一般用量。API 侧的模型 ID 是 gpt-image-2.6-flare 与 gpt-image-2.6-sunburst。本文没有把这几个名字合并成同一个 ID。
  - q: 做 GIF 时，能在 Codex 对话里直接填 frame_count 吗？
    a: frame_count 和 frame_duration_ms 是 Image API 生成接口的字段。用法文档没有写 Codex 对话里有同名字段。在对话里用自然语言写清主体、动作和循环；要精确控制帧数和每帧时长时，走 API。
  - q: 图像生成为什么额度掉得更快？
    a: 官方写法是：相对不生成图的同类回合，图像生成平均把包含额度用得快 3 到 5 倍，具体取决于图像质量和尺寸。这是用量速度，和博客所说的生成耗时大约快 50% 是两件不同的事。
---

# Codex Images 2.6：在 Codex 里生成 GIF、overlay 圈选编辑，全套餐可用

> 本文在线版：[codexguide.io/guides/codex-images-2-6](https://codexguide.io/guides/codex-images-2-6)

> 核对依据：OpenAI《[Introducing Images 2.6](https://openai.com/index/introducing-images-2-6/)》（2026-11-04）、ChatGPT Learn《[Image generation](https://learn.chatgpt.com/docs/image-generation)》、开发者文档《[Image generation](https://developers.openai.com/api/docs/guides/image-generation)》与《[Image prompting](https://developers.openai.com/api/docs/guides/image-prompting)》，以及 [@OpenAIDevs 2026-11-04 的说明](https://x.com/OpenAIDevs/status/2118124753340756055) 和同线程的 [overlay 编辑帖](https://x.com/OpenAIDevs/status/2118124764413718953)。本文没有在本机生成或编辑图片，也没有截本机对话。界面按钮以你当前的 App、网页或 CLI 为准。

适合已经会在 Codex 里改代码、现在想顺手出一张界面稿、精灵表或循环 GIF 的人。读完可以判断：这句话该在对话里说，还是该改走 API；编辑时该圈一块区域，还是该上传一张标注图。

## 先看结论

2026-11-04，OpenAI 把 Images 2.6 放进 ChatGPT、Codex 和 API。博客写明：ChatGPT 与 Codex 在全部订阅档位上可用，覆盖桌面、移动和网页。同一天，[@OpenAIDevs](https://x.com/OpenAIDevs/status/2118124753340756055) 写道：GPT-Image-2.6 进入 Codex 和 API；API 的两个模型是 Image-2.6 Flare 和 Sunburst，生成速度比此前大约快 50%；质量设为 medium 或 high 时，Sunburst 在连续编辑之间更能保住细节。

Codex 里可以做的事，按官方材料能确定的是这些：

| 你要的结果 | 先走哪条 | 依据 |
| --- | --- | --- |
| 在当前对话里出一张图或改一张已有图 | 自然语言，或显式写 `$imagegen` | [Image generation](https://learn.chatgpt.com/docs/image-generation) |
| 让 Codex 的编辑留在画面上，少开一块侧栏 | overlay 里直接改 | [OpenAIDevs 跟帖](https://x.com/OpenAIDevs/status/2118124764413718953) |
| 要一段循环动画 | 对话里把动作和循环写进提示；要控制帧数时用 API 的 GIF 输出 | 博客与 [Image API](https://developers.openai.com/api/docs/guides/image-generation) |
| 大批量、要单独计价 | 设置 `OPENAI_API_KEY`，让生成走 API | 用法文档 |
| 看当前窗口，或去点别的桌面软件 | 另两条能力，见文末 | 与出图分开 |

用法文档同时写：ChatGPT 网页里图像是否可用、用量上限，仍取决于套餐和工作区设置。网页上找不到入口时，先核对套餐和工作区。

## 在 Codex 里怎么生成

用法文档把几种入口写在同一页上。能直接对应到操作的句子是：

- 在 App 的输入框里描述要生成或要改的图。需要参照已有素材时，附上一张参考图。
- 在交互会话里描述图像，或写上 `$imagegen`，显式调用图像生成技能。已有图片要用 `-i` 或 `--image` 附上，作为结果的视觉引导。
- 在 IDE 扩展的对话里要图。需要 Codex 基于现有素材修改时，按住 Shift 把参考图拖进输入框。

内置图像生成使用的模型名，文档写的是 `gpt-image-2`。它计入 Codex 的一般用量。相对不生成图的同类回合，图像生成平均把包含额度用得快 3 到 5 倍，幅度取决于图像质量和尺寸。

提示词文档给出的有效写法通常是一到三句清楚的话，并覆盖这些点：

1. 这张图给谁用、用来干什么。
2. 主体是谁，正在发生什么。
3. 场景、构图和视觉风格。
4. 需要时再写取景、尺寸、光线、颜色或材质。
5. 必须排除的内容。

具体视觉语言比「好看」「高级」有用。光线从哪边来，比「美丽的光」更能被核对。必须保持不变的要求，要重复写一次。

下面是本文编写的写法示例，用来说明结构。它不是官方样例，也没有在本机跑出结果：

```text
为一份员工入职说明做一张干净的编辑插画。画面里一个人在桌前整理项目，桌上有笔记本电脑、笔记本和一份简单的进度清单。光线是左侧窗户进来的柔和日光，颜色克制，风格现代、好接近。背景保持简单。不要标志、文字或未来感元素。
```

官方页上有英文原例，见 [Write effective image prompts](https://learn.chatgpt.com/docs/image-generation)。

## 编辑：参考图、圈选和 overlay

改图时，文档要求写清两件事：哪一部分要变，哪一部分必须保持原样。一次只动一个要素，构图和其他关键细节才不容易漂。

用法文档还写：可以选中图像的一块区域，再描述这块区域的变化。

2026-11-04，[@OpenAIDevs](https://x.com/OpenAIDevs/status/2118124764413718953) 把 Codex 侧的界面变化说成：编辑现在直接发生在 overlay 里，不再打开侧栏。帖文链回 Images 2.6 博客。本文没有截到这个 overlay，按钮文案以当前客户端为准。能核对的产品变化是：圈选和编辑留在覆盖层上，而不是再开一块侧边面板。

多张参考图时，按顺序说明每张图的角色。一张定内容，另一张定风格或版式。用前景、背景、左、右这类空间词说明怎么合成。

图里要出现的文字保持短，并把原文放进引号，写明大小写、字体感觉、字号、颜色和位置。不常见的名字，必要时逐个字母拼出来。同时写明是否允许其他文字。密集信息图可以起草，但上线用的字要逐词核对，必要时再进设计工具收尾。

API 里的 markup 是另一条路径。开发者文档写：在 `POST /v1/images/edits` 上，用一张透明 PNG 标出要改的位置，并在 `prompt` 里描述改动。这张标注层在方向校正后必须和第一张输入图同宽同高。标注作用在第一张输入图上，其余图片只作参考。第一张图和标注层各自最多 16,777,216 像素，标注文件还有 50 MB 上限。`markup` 不要和 `mask` 或 `prompt_rewriter` 一起用。Responses API 的区域编辑仍用 mask。

所以：Codex 对话里的 overlay 圈选，和 API 请求里的 `markup` 文件，都是在指明「改哪里」。入口不同，字段也不同。

## 做 GIF：把动作和循环写进提示

博客把 GIF 写成 Images 2.6 的新能力：可以让吉祥物、角色或产品画面动起来，并做成循环。范围包括 ChatGPT、Codex 和 API。

API 的控制字段写在生成接口上，编辑接口不产出 GIF：

| 字段 | 取值 | 默认 |
| --- | --- | --- |
| `output_format` | 生成接口可设为 `gif` | — |
| `frame_count` | 2–64 帧 | 9 |
| `frame_duration_ms` | 每帧 20–2000 毫秒，按 10 毫秒取整 | 200 |
| `size` | `auto`，或宽高都是正数且为 16 的倍数 | `auto` |

`size` 描述的是每一帧成品的尺寸。帧数、帧尺寸和动画张数必须落在模型尺寸限制和本次请求的像素预算里。超出时减少 `frame_count`、帧尺寸或 `n`。用 `auto` 时，由 API 在模型限制内选帧尺寸。

响应里是完成的动画。把每条结果的 `b64_json` 按 base64 解码，存成 `.gif`。GIF 输出不支持流式、部分图像、自定义 `output_compression` 或 `prompt_rewriter`。`frame_count` 和 `frame_duration_ms` 只在 GIF 输出时使用。

提示词指南里的官方例子用 `gpt-image-2.6-sunburst`、`size="512x512"`、`quality="high"`，以及默认的 high complexity。`frame_count=9`、`frame_duration_ms=200` 时，这段循环长 1.8 秒。提示本身要写明主体、动作，以及镜头是否移动；要无缝循环，就让主体回到起始姿势。

对话里可以沿用同一套描述，不必假设输入框里有这些 API 字段。本文编写的对话示例：

```text
做一个无缝循环的 GIF。主体是一盏暖色台灯，灯罩轻轻向左再向右晃，然后回到正中。机位固定，背景是浅色桌面。不要文字和标志。动作连续，最后一帧接回第一帧。
```

博客上的精灵表长提示词是第三方创作者的示例，以 [官方博客](https://openai.com/index/introducing-images-2-6/) 原文为准，这里不转载整段。

## 用量：计入 Codex 额度

把「生成变快」和「额度用得更快」分开看。

- **生成耗时**：博客和 OpenAIDevs 的帖都写，Images 2.6 的生成大约比此前快 50%。质量设为 low 时，Flare 最快可以大约 6 秒出图。这是「最快可以」，不是每次请求的承诺。
- **Codex 包含额度**：内置出图计入一般用量，平均比同类非出图回合快 3 到 5 倍耗尽额度，取决于质量和尺寸。
- **大批量**：在环境里设置 `OPENAI_API_KEY`，并让生成走 API，这样按 API 价格计算。具体价目以博客指向的价格页和你账号里的当前表为准，本文不抄一份价格。

组织若要使用 GPT Image 模型，开发者文档写明，可能需要先在开发者控制台完成 API Organization Verification。

## API：Flare、Sunburst、complexity 和 quality

API 模型 ID 是 `gpt-image-2.6-flare` 和 `gpt-image-2.6-sunburst`。提示词指南的分工是：

| 更在意什么 | 先试 |
| --- | --- |
| 响应时间 | `gpt-image-2.6-flare` |
| 细节、版式或编辑准确度 | `gpt-image-2.6-sunburst` |

Sunburst 已经满足要求时，再用同一套提示、参考图、尺寸和质量去试 Flare，比较结果和耗时。博客补充：medium 或 high 质量下，Sunburst 的出图质量和跨编辑一致性更高；Flare 也会改善海报、产品图和其他职业视觉的版式质量。

两个参数分开：

| 参数 | 作用 | 取值 |
| --- | --- | --- |
| `quality` | 视觉细节和保真度，例如纹理或小字 | `auto`、`low`、`medium`、`high`、`xhigh`、`max` |
| `complexity` | 渲染前花多少规划。低档适合快速、范围清楚的编辑；高档适合密集文字、复杂版式和物体关系 | `low`、`medium`、`high` |

省略 `complexity` 时，Flare 和 Sunburst 都用 `high`。调整 complexity 没有单独费用。更高的 complexity 可能增加延迟，也可能带进你不想要的改动，所以要就自己的任务对比。官方建议：多数编辑用 low complexity，再按工作流选 quality；场景元素或约束很多时，试 medium 或 high complexity。

生成接口的 `output_format` 还包括 `png`、`jpeg`、`webp` 和 `svg`。SVG 适合需要可编辑路径的图标和插画。API 会先做一张参考图再产出 SVG，`quality` 控制的是这张参考图。返回的是静态矢量，不支持脚本、外部资源或嵌入的位图。透明背景用 `background: "transparent"`，并配合 `png`、`webp`，或支持透明的 SVG。

开发者文档里的代码示例仍有一部分使用 GPT Image 2.5 的模型名。要用 2.6 时，把 `model` 换成上面的 Flare 或 Sunburst ID，并单独阅读该页的 GPT Image 2.6 小节。

## 和「看窗口」「操作桌面」怎么分工

出一张新图，和下面两件事不是同一条功能：

- **把当前应用窗口发给对话**，是为了让 Codex 看见你正在看的界面。知识库「官方工具与集成」里若已有 Appshots 专文，用那篇处理这件事。
- **让 Codex 去点击、输入别的桌面应用**，走 Computer Use。安装、授权和必须停手的场景见 [Codex 使用 Computer Use 操作桌面应用](./03-Codex使用Computer-Use操作桌面应用.md)。

日常入口的总表见 [Codex 常用功能清单](./11-Codex常用功能清单.md)。

## 怎么验证

本文没有在登录后的 Codex 里实际出图。你本机可以按这个顺序自行核对，每一步都该有可见结果：

1. 用一句短提示加上 `$imagegen`，确认对话返回图像，而不是只返回文字说明。
2. 再发一句只改一个元素的编辑，并写明其余部分保持不变。确认变化落在你点名的部分。
3. 若客户端提供圈选，在 overlay 里选中一块区域再描述改动，确认没有被迫打开侧栏才能编辑。
4. 打开用量或 `/status`，确认这次出图记在 Codex 用量里。3 到 5 倍是官方给出的平均幅度，单次账单不会刚好落在这个倍数上。
5. 需要 GIF 或指定帧数时，用 API 生成一条 `output_format` 为 `gif` 的结果，确认文件能播放，并且编辑接口没有被拿来出 GIF。

人物肖像要有使用许可。要原创处理，避免仿某家品牌、某个艺术家或某件作品。生成图可以不署名 OpenAI；若场景需要，说明素材是怎么来的即可。使用范围同时遵守你所在组织的规定和 OpenAI 的使用政策。博客提到 Images 2.6 有 system card，评测数字以该卡原文为准，本文不转述未单列的分数。

## 常见限制

- 复杂提示的延迟，开发者文档仍写最长大约 2 分钟。50% 更快是相对此前的整体说法。
- 文字渲染和精确排版仍可能出错。小字、多字体和上线文案要人工核对。
- 跨多张图保持同一角色或品牌细节，博客把它列为改进方向；文档仍提醒偶尔会漂。
- 对话里的模型显示名、overlay 的按钮，以及网页端是否对你的工作区开放，以当前客户端和套餐为准。
- 本文没有本机截图。官方博客和 API 指南页上的示例图可以直接打开对照。

## 下一步

生成和编辑的日常说法，先用 `$imagegen` 加一句「改什么、保留什么」。帧数、标注层和 SVG 再进 API。要操作真实桌面软件时，转到 Computer Use 专文，不要用出图代替点击。

## 参考资料

- [Introducing Images 2.6](https://openai.com/index/introducing-images-2-6/)（2026-11-04）
- [Image generation（ChatGPT Learn，含 `$imagegen` 与用量）](https://learn.chatgpt.com/docs/image-generation)
- [Image generation（API）](https://developers.openai.com/api/docs/guides/image-generation)
- [Image prompting（quality、complexity 与 GIF 提示）](https://developers.openai.com/api/docs/guides/image-prompting)
- [OpenAIDevs：GPT-Image-2.6 进入 Codex 与 API](https://x.com/OpenAIDevs/status/2118124753340756055)
- [OpenAIDevs：编辑改在 overlay 中完成](https://x.com/OpenAIDevs/status/2118124764413718953)
