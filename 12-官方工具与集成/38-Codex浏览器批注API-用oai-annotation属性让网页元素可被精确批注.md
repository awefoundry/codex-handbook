---
id: codex-browser-annotation-api
title: "Codex 浏览器批注 API：用 oai-annotation 属性让网页里的卡片、文字和 canvas 对象能被精确批注，并带上额外上下文"
seo_title: "Codex 浏览器批注 API：oai-annotation 与精确批注"
description: "Browser Annotation API 让网站规定 Annotation mode 里能选什么、附带什么上下文、发送前预览什么控件。本文按官方文档说明 oai-annotation 属性、document.oai.annotation，以及不改代码也能批注的用法。"
lede: "不改网站时，用浏览器工具栏的 Annotate 就能点选和圈选。要让一张卡片、一段文字或 canvas 里的对象被精确选中，才需要这套 API。"
url: /guides/codex-browser-annotation-api
status: published
section: guides
category: J-official-tools
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 38
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-27
date_modified: 2026-11-27
verified_on: 2026-11-27
official_ref: https://learn.chatgpt.com/docs/annotations-extensibility
keywords: [Codex 浏览器批注, Browser Annotation API, oai-annotatable, document.oai.annotation, Codex Annotation mode]
related: [codex-browser-login-state, codex-webmcp-site-tools, codex-plannotator-plan-review]
howto: true
faq:
  - q: "不改网站代码，能不能在页面上批注？"
    a: "能。Browser 页的 Comment on the page 写明：在内置浏览器工具栏选 Annotate 进入 Annotation mode，点击元素或拖选一块区域，写下评论再保存，然后在对话里请 ChatGPT 处理这些评论。Browser Annotation API 是在这之上，让网站自己规定能选什么、附带什么。"
  - q: "Enterprise 或 Edu 里，自定义批注为什么不出现？"
    a: "官方页写明，ChatGPT Enterprise 和 Edu 工作区里，管理员必须通过工作区策略允许 Site annotation customizations。本文没有企业工作区，没有看过这个开关的界面。"
  - q: "metadata 里可以放令牌或内部 ID 吗？"
    a: "官方要求只放你愿意同时给用户和模型看的上下文。批注会带着这些字段进入对话。无效的 metadata 会被浏览器忽略，这不等于可以拿它藏密钥。"
  - q: "普通 Chrome 里没有 document.oai.annotation，是不是接错了？"
    a: "这套 JavaScript API 通过应用内置浏览器里的 document.oai.annotation 提供，面向 DevDay 2026 版 ChatGPT 桌面端及以后，并且要求安全的顶层页面，例如 HTTPS 或 localhost。官方建议对每个方法做特性检测。检测不到就保持页面原有交互。"
---

# Codex 浏览器批注 API：用 oai-annotation 属性让网页里的卡片、文字和 canvas 对象能被精确批注，并带上额外上下文

> 本文在线版：[codexguide.io/guides/codex-browser-annotation-api](https://codexguide.io/guides/codex-browser-annotation-api)

> 核对依据：2026-11-27 打开的 [Annotations Extensibility](https://learn.chatgpt.com/docs/annotations-extensibility)、[Browser](https://learn.chatgpt.com/docs/browser) 的 Comment on the page，以及 [DevDay 2026](https://learn.chatgpt.com/docs/whats-new/devday-2026) 的 Website annotations。没有登录 ChatGPT 桌面端，没有在内置浏览器里点过 Annotate。下面的属性名、方法名、限制数字和代码片段只来自这些页面的原文。

内置浏览器、浏览器扩展和 Computer Use 怎么选，见 [Codex 浏览器操作与登录态](./02-Codex浏览器操作与登录态功能.md)。批注把人的选择和反馈送进对话；如果还要让代理调用网站自己的能力，那是另一条 [Site tools（WebMCP）](../09-MCP与外部工具/05-Codex-Site-tools-WebMCP网站工具入门.md)。第三方的 [Plannotator](../09-MCP与外部工具/23-Codex安装Plannotator-浏览器批注计划与代码审查并回传反馈.md) 用来批注计划和代码审查，不是这个页面 API。

## 先说结论

Browser Annotation API 让网站自定义三件事：Annotation mode 里能选中什么，选中后附带什么上下文，发送之前用哪些控件预览改动。DevDay 2026 的 What's new 用同一句话概括：选择别人能选中的对象，附上有用的上下文，并加上控件，在把反馈发给 ChatGPT 之前先预览。该页写明，这套 API 用在受支持的桌面应用浏览器里。

不改网站代码，批注已经能用。API 是在默认行为之上，让一张卡片、一段文字，或画在 canvas 里的对象，按你规定的边界被选中。

官方示例用 TypeScript。把抄下来的例子存成 `annotations.ts`，再用页面给出的命令编译：

```bash
npm install --save-dev esbuild
npx esbuild annotations.ts --format=esm --outfile=annotations.js
```

页面上还要有例子里的那些 HTML 元素，然后加载编译结果：

```html
<script type="module" src="./annotations.js"></script>
```

项目如果已经在构建 TypeScript，把例子放进现有构建即可，不必再装一份 esbuild。官方另有一个 Annotations Extensibility 插件安装入口，本文没有安装。

## 使用条件

官方页写，这份指南面向 DevDay 2026 版 ChatGPT 桌面端及以后。JavaScript API 通过应用内置浏览器里的 `document.oai.annotation` 提供。页面必须是安全的顶层页面，例如 HTTPS 或 localhost。启用之后，浏览器会在你的页面脚本运行之前装上它。

对每个方法做特性检测，以便旧版或不支持的浏览器仍能用。DOM 元素就绪后再初始化。不需要就绪事件，也不需要轮询。

API 方法同步返回，注册句柄可以立刻使用。浏览器可以在这之后再把批注编辑器加载完。annotation surface 的 `hitTest` 可以返回一个 promise。

ChatGPT Enterprise 和 Edu 工作区里，管理员必须通过工作区策略允许 **Site annotation customizations**。

从网站自己的按钮发起批注，可能还要用户授权。用户可以在 **Site tools > Annotation features** 里重新打开被拦住的批注功能。

## 先用起来：默认怎么选

默认的 Annotation mode 按页面 DOM 选择元素，偏向文字、图片和控件。这一层不需要 `oai-annotation` 属性。

Browser 页的 Comment on the page 写的步骤是：

1. 在浏览器工具栏选 **Annotate**，进入 **Annotation mode**。
2. 点击一个元素，或拖动选中一块区域。
3. 写下评论并保存。
4. 在对话里发一条消息，请 ChatGPT 处理这些评论。

评论要写明问题和你要的结果。页面给的例子是：这个按钮在移动端溢出，能放进一行就保持一行，否则换行，但不要改卡片高度。

给页面上的一块区域加批注时，可以在文本输入旁边选 **Adjust**，改字体、文字、间距和颜色，先在页面上预览，再把批注发出去，目标会更清楚。官方页写，手动的 **Adjust**、折叠和 **Option-click** 只在 Codex 或 localhost 上可用。托管在 ChatGPT 里的网站上，已注册的自定义控件会自动出现，没有 **Adjust** 或折叠按钮。页面请求的高级模式在那里仍然有效。

内置浏览器和其他入口怎么分工，见 [怎么选浏览器](./02-Codex浏览器操作与登录态功能.md)。

## 让一张卡片整体可选

要让更大的一块成为同一个可选对象，用 `oai-annotation-container` 标出区域，用 `oai-annotatable` 标出其中可选的后代。官方例子把一张图表卡片收成一个对象：

```html
<section oai-annotation-container>
  <article id="chart-card" oai-annotatable="Q3 Revenue">
    <h2>Q3 Revenue</h2>
    <p>$120,000 this quarter</p>
    <button type="button">More info</button>
  </article>
</section>
```

指针停在卡片里的任何位置，都会高亮整张卡片。`oai-annotatable` 的值可选，它是显示给用户和模型的名字。附近有多个对象时，名字要能区分开；也可以不写值。

容器决定这些选择规则用在哪里。单独一个 `oai-annotatable` 不会改变选择行为。容器内部，浏览器选择包含指针下那个元素的、最近的已标记目标。嵌套容器用最近的那一层。容器里没有标记的区域会变成一条网页批注。所有容器之外，保持默认行为。

## 开放文字选择

在一块区域上加 `oai-annotation-container-text`，Annotation mode 里就可以拖选文字。这个属性不需要值：

```html
<article oai-annotation-container-text>
  <h2>Design guidelines</h2>
  <p>Use consistent spacing between related components.</p>
  <p>Leave more space between separate groups.</p>
</article>
```

松开时如果选区不是空的，会打开文字批注编辑器，带上这段范围和它的上下文。只点击、没有选出文字，不会创建批注。**Escape** 或取消的手势会取消这次选择。

最近的文字容器或 DOM 选择容器，决定手势怎么开始。文字容器不用 `oai-annotatable` 做元素拾取。要恢复元素拾取，就在里面再套一层 `oai-annotation-container`；要恢复文字选择，就再套文字容器。同一个元素上两个属性都有时，文字选择优先。

文字选择遵循页面原有的选择规则，可以延伸到起始容器之外。容器不会裁切范围，也不会让 iframe 里面变得可选。文本框仍然可选，但 Annotation mode 期间，普通的页面点击和控件上的原生动作仍然被挡住。显式的 `request()` 保持它原有的行为。

文字选择容器只在 Annotation mode 期间、并且站点批注能力和按站点的设置都已启用时生效。

## 给批注带上看不见的上下文

`oai-annotation-metadata` 加在已标记的目标上，用来带上页面上可能看不见的上下文。官方例子是一行联系人，metadata 里放了一个邮箱，便于起草邮件：

```html
<section oai-annotation-container>
  <div
    id="contact-row"
    oai-annotatable="Alex Morgan"
    oai-annotation-metadata='{"email":"alex@example.com"}'
  >
    <div>Alex Morgan</div>
    <div>Project lead</div>
  </div>
</section>
```

点哪一行都会选中整行。metadata 和批注一起出现，并跟着进入对话。只放你愿意同时给用户和模型看的内容。即便带了邮箱，真正发信仍然需要一个已连接的邮件工具。

必须是一小份扁平的 JSON，限制是：

- 最多 6 个属性。值可以是字符串、有限数字、布尔或 `null`。
- 键最长 64 个字符，字符串值最长 256 个字符。
- 序列化后的对象最多 2,048 字节。
- 键必须以 ASCII 字母开头，只能包含 ASCII 字母、数字、空格、下划线或连字符。词与词之间只用一个空格。
- 不支持嵌套对象和数组。无效的 metadata 会被浏览器忽略。

`request()` 或 surface 的 `hitTest` 结果里也可以提供 metadata。

## 从站内按钮发起批注

在一次用户操作里直接调用 `document.oai.annotation.request(target, options)`，例如按下按钮。目标可以是当前文档可视区域里、已经连上文档的 HTML 元素，或一个 DOM `Range`。不需要批注属性。不支持虚拟对象 ID。

官方示例在一段落款上打开批注。脚本要在两个元素都存在之后再跑。按钮在检测不到 `request` 时保持隐藏：

```html
<p id="delivery-summary">
  Standard delivery takes three to five business days.
</p>
<button id="discuss-delivery" type="button" hidden>Explain more</button>
```

```typescript
const summary = document.getElementById("delivery-summary") as HTMLElement;
const button = document.getElementById("discuss-delivery") as HTMLButtonElement;

button.hidden = typeof document.oai?.annotation?.request !== "function";

button.addEventListener("click", () => {
  const annotation = document.oai?.annotation;
  if (typeof annotation?.request !== "function") return;

  annotation.request(summary, {
    initialComment: "Explain this delivery estimate.",
  });
});
```

点下 **Explain more** 之后，浏览器会打开一条批注：段落被选中，评论可编辑。用户可以改、保存，并随自己的消息发送。打开批注不会把消息发给 ChatGPT，只有用户能提交。

调用要留在当前这次用户交互里。先去等待一次网络请求，可能把这次交互丢掉。

第二个参数里，官方页列出的字段是：

| 选项 | 行为 |
| --- | --- |
| `mode` | `"advanced"` 为元素打开高级控件，`"default"` 用默认编辑器行为。默认是 `"default"`。自定义控件在 `"default"` 下仍可能打开。文本范围只支持 `"default"` |
| `enterAnnotationMode` | 设为 `true` 时进入 Annotation mode，取消或发送这条批注之后仍然留在该模式 |
| `omitScreenshot` | 设为 `true` 时，这条批注不带自动截图。默认 `false`，保持平常的截图行为。对元素请求和文本范围请求都适用 |
| `metadata` | 合法且非空的 metadata 会替换目标上的 HTML metadata，只对这一次请求生效。文本范围，以及目标元素在 shadow DOM 里时，这个选项被忽略 |
| `initialComment` | 一条可编辑的评论，最长 240 个 UTF-16 码元 |

`request()` 返回带 `accepted` 布尔值的对象。要看浏览器是否收下并校验了这次请求，检查 `result.accepted`，不要只看返回对象是否存在。它不表示编辑器已经打开，也不表示用户已经保存或发送。

编辑器还在加载时，浏览器可以暂存一条已接受的请求。已有请求等待中、编辑器开着，或 ChatGPT 正在控制浏览器时，另一条请求可以被拒绝。

### 只请求一段文字

把 DOM `Range` 传给 `request()`，可以不改浏览器当前的文字选择，就对某一小段请求反馈。官方例子只选中 `<mark id="draft-passage">` 里的文字，不需要 `oai-annotation-container-text`。用 `document.createRange()` 和 `range.selectNodeContents(passage)` 做出范围，再 `annotation.request(range, { initialComment: "Explain when this trial ends." })`。完整脚本在官方页的 Request an annotation for a text range。

范围必须包含当前文档里非空的可见文字，并且至少有一部分落在页面可视区域内。最多 20,000 个 UTF-16 码元。折叠的范围、只有空白的文字、被隐藏的选中文字，以及位于已关闭的 shadow root 里的范围，都不支持。

文本范围请求只用默认的文字编辑器。带 `mode: "advanced"` 的请求会被拒绝，请求里的 metadata 也会被忽略。已接受的请求在等编辑器时，目标文字要还在：浏览器打开之前会再检查一次范围。

## 自定义控件、canvas 对象与 Annotation mode 开关

这一节只列官方页写出的接口。每个字段的校验表很长，以 [Annotations Extensibility](https://learn.chatgpt.com/docs/annotations-extensibility) 的 Add custom controls、Make canvas objects selectable 和 Control Annotation mode 为准。

### 编辑器默认模式

通过浏览器自己的选择界面打开批注时，如果要立刻显示高级控件，在页面 `<head>` 里加：

```html
<meta name="oai-annotation-editor-default-mode" content="advanced" />
```

从你自己的界面打开时，给 `request()` 传 `{ mode: "advanced" }`。`mode: "default"` 或不传，用默认编辑器行为。页面上的 meta 不会覆盖这次请求的选项。默认模式不保证只有评论框：带有建议起始值的自定义控件，或省略了 `currentValue` 的控件，可以打开控件编辑器。

### 自定义控件

`registerControls()` 把控件绑到一个或多个 DOM 元素上。控件可以预览应用属性，例如一个间距 token，也可以收集一个选择，例如邮件语气。

`controlsMode: "replace"` 只显示你的控件。`"extend"` 把它们和内置控件放在一起。可选的 `controlsHeading` 是面板标题，浏览器会去掉首尾空白，接受 1 到 80 个字符。没有标题时，面板显示元素的 HTML 标签。标题不会放进发给 ChatGPT 的上下文。

一次注册最多 12 个控件。每个控件都要有 `type`、可见的 `label` 和 `callback`。官方列出的类型：

| 类型 | 值 | 额外字段 |
| --- | --- | --- |
| `color` | 十六进制颜色，例如 `"#2563eb"` | 无 |
| `range` | 数字 | `min`、`max`、`step` |
| `select` | 字符串 | `options`，一组 `{ label, value }` |
| `toggle` | 布尔 | 无 |

`callback` 是字符串标识，不是 JavaScript 函数。同一次注册里必须唯一，以 ASCII 字母开头，只用 ASCII 字母、数字、下划线或连字符。可选的 `reference` 标出正在改的属性，会和标签、值一起进入批注。

`currentValue` 用这个属性当前的普通值，包括还没保存的编辑。不要用预览态或没写完的输入当基线。浏览器用它做前后对比和重置。应用状态变了，用 `registration.update({ controls })` 刷新以后批注的 `currentValue`。已经存在的批注保留当时捕获的值。

`defaultValue` 是建议的起始值，初始状态上优先于 `currentValue`。两个都省略时：颜色从白色开始，range 从最小值开始，select 用第一个选项，toggle 为 `false`。

预览事件是 `oaiannotationcontrolchange`，从被选中的元素冒泡。`detail` 里有 `callback`、`value` 和 `action`。官方列出的 action：

| action | 把给出的值用在 |
| --- | --- |
| `preview` | 显示请求的改动 |
| `preview-original` | 临时显示原来的状态，便于对比 |
| `reset` | 预览被清掉时恢复原来的状态 |

预览不是永久保存。保存仍走应用自己的保存流程。`dispose()` 只去掉控件注册，不会撤销你做的预览改动，清理时要自己把页面画回去。

标签、选项数量、range 的数值范围、颜色写法、目标个数和序列化长度，都有单独上限。写错时 `registerControls()` 和 `registration.update()` 会同步抛出。`dispose()` 之后再 `update()` 也会抛出。被拒绝的更新会保留上一次成功的注册。这些上限的原表在官方页的 Validate controls and registrations，本文不另造一列。

间距预览的完整例子用 `type: "range"`、`callback: "setCardPadding"`，并监听 `oaiannotationcontrolchange` 去改 `--card-padding`。选择语气、不预览页面的例子用 `type: "select"`，省略 `currentValue`，这样即使用户留在初始选项，浏览器也会把选中的语气放进批注。对 select，预览回调收到的是 `option.value`；批注历史和 ChatGPT 收到的是可见的 `option.label`。

### canvas 里的对象

annotation surface 用来识别画在 canvas 里面的单个对象。用 `registerSurface()` 注册宿主元素，并提供 `hitTest`。命中时返回带稳定 `id` 的对象，空白处返回 `null`。

宿主必须是已连接的 HTML 元素，在安全的顶层文档里，并且不在 shadow DOM 中。iframe 里不支持 surface 注册。

`hitTest` 可以返回 promise，并收到一个 `AbortSignal`，参数名是 `signal`，用来取消已被取代的工作。浏览器给 250 毫秒，超时就退回 DOM 选择。出错或结果无效也会退回。成功但没有对象时，要显式返回 `null`。取消了的工作仍然必须 resolve 或 reject。浏览器同时只允许一个 `hitTest` 在飞，在 promise 结束之前都会占着这个名额，即使已经取消或超时。

可选字段：`name` 给用户看，`role` 是一句短的语义说明，`metadata` 只在它提供了页面上还没有的上下文时才加，`rect` 用相对可视页面区域的 CSS 像素，和 `clientX`、`clientY` 同一套坐标。

可选的 `renderSelection` 用来画自己的悬停和选中反馈。对象移动或缩放变了，调用 `surface.invalidate()`。拆掉集成时调用 `surface.dispose()`。两者都同步返回，没有值。

画出来的对象在 API 里叫 virtual objects。自定义控件注册在 surface 的 DOM 元素上。它们用你的自定义控件，内置的 CSS 和文字控件对它们不适用。控件事件的 `detail.virtualTarget` 是 `{ surfaceId, targetId }`。`targetId` 对应 `hitTest` 返回的 `id`。普通 DOM 事件没有 `virtualTarget`。重新打开一条已保存的批注时，不会再跑一次 hit testing 去替换当时捕获的对象或 metadata。

官方页的最小例子只返回 `{ id: "revenue-this-quarter" }`。带上下文的返回是：

```javascript
return {
  id: "revenue-this-quarter",
  name: "Revenue this quarter",
  role: "chart-bar",
  metadata: { metricId: "quarterly-revenue" },
  rect,
};
```

`id` 在同一个 surface 里要保持稳定。

### Annotation mode 开关

用 `toggle()` 请求切换模式，用 `isActive()` 读取已经确认的状态，用文档上的 `oaiannotationmodechange` 让你自己的界面跟上。两个方法都要做特性检测。

`toggle()` 不传参时会把模式反过来。传 `true` 确保打开，传 `false` 确保关闭。同一个布尔值重复请求是幂等的。传 `true` 会保留已经打开的编辑器或尚未完成的激活。传 `false` 会取消尚未完成的激活，并走正常的退出流程。

`toggle()` 要从一次还活着的用户交互里调用。同步返回的 `{ accepted }` 只表示请求被收下，不是模式已经改成那样。浏览器的资格检查仍可能阻止这次切换。状态以 `isActive()` 和事件为准。

`isActive()` 不需要用户手势。浏览器先更新它，再派发 `oaiannotationmodechange`。`event.detail.active` 是布尔值。没有初始事件，强制的空操作也不会再发一条重复事件，所以界面的初始状态要从 getter 读。权限在激活期间被收回时，最后一条事件是 `active: false`，保留的 getter 也返回 `false`。

Annotation mode 会吃掉页面点击。按住 **Space** 才能去点页面控件，包括你自己的退出按钮，也可以从浏览器的批注界面退出。只按住 **Space** 时，`isActive()` 仍是 true。API 不支持 `oai-annotation-ignore`，也没有别的属性可以让点击穿过去。

退出会关掉编辑器，并保留已保存的批注，不会提交它们，也不会把它们移进输入框。

## 怎么测试、哪些情况不生效

官方的 Test your integration 是在桌面应用的内置浏览器里打开你的网站，按你实际加过的功能测。步骤是：

1. 进入 Annotation mode，选择对象和文字。核对高亮、名字、范围和 metadata 是不是你要的目标。
2. 从站内按钮打开一条批注。核对选中的元素或文字范围、初始评论和编辑器模式。
3. 改一个自定义控件，和原状对比，再清掉预览。核对应用把原状恢复了。
4. canvas：测空白处、改变尺寸和场景变化。切换对象，确认控件事件仍更新当时捕获的那个目标。取消一次异步 hit test，确认后面的拾取仍然能用。
5. 从输入框的附件预览里保存、重新打开并编辑一条批注。核对它还保留控件和目标，删掉它时预览也被清掉。
6. 把批注和一条消息一起发送。确认 ChatGPT 收到选中内容、metadata 和请求的值，包括可见的 select 标签，以及省略了 `currentValue` 时那个没改过的选项。
7. 在没有这套 API 的浏览器里打开同一站点，确认普通交互仍然可用。

下面这些情况，按官方页，集成不会按你期望生效：

- 不是安全的顶层页面，或浏览器里没有 `document.oai.annotation`。先做特性检测。
- Enterprise 或 Edu 没有允许 **Site annotation customizations**。
- 只有 `oai-annotatable`，外面没有 `oai-annotation-container`。选择行为不会因此改变。
- metadata 不是扁平 JSON，或超出个数、长度、键名规则。浏览器忽略无效 metadata。
- 文本范围是空的、只有空白、被隐藏、超过 20,000 个 UTF-16 码元，或 `mode` 设成了 `"advanced"`。
- `hitTest` 超过 250 毫秒、抛错或返回无效结果。浏览器退回 DOM 选择。
- surface 放在 iframe 或 shadow DOM 里。
- 调用 `toggle()` 或 `request()` 时，已经不在那一次用户交互里。

要把代理能在网站上执行的动作暴露出来，官方页指向 [Site tools (WebMCP)](https://learn.chatgpt.com/docs/webmcp)。批注负责把人的选择和反馈送进对话；site tools 让代理通过应用已有的能力去用这些上下文。站内说明见 [WebMCP 入门](../09-MCP与外部工具/05-Codex-Site-tools-WebMCP网站工具入门.md)。

## 常见问题与参考资料

常见问题见文首四则问答。

- [Annotations Extensibility](https://learn.chatgpt.com/docs/annotations-extensibility)（2026-11-27）
- [Browser：Comment on the page](https://learn.chatgpt.com/docs/browser#comment-on-the-page)（2026-11-27）
- [DevDay 2026：Website annotations](https://learn.chatgpt.com/docs/whats-new/devday-2026)（2026-11-27）
- [Site tools（WebMCP）官方页](https://learn.chatgpt.com/docs/webmcp)
- [Codex 浏览器操作与登录态](./02-Codex浏览器操作与登录态功能.md)
- [Codex Site tools（WebMCP）入门](../09-MCP与外部工具/05-Codex-Site-tools-WebMCP网站工具入门.md)
- [Plannotator：批注计划与代码审查](../09-MCP与外部工具/23-Codex安装Plannotator-浏览器批注计划与代码审查并回传反馈.md)
