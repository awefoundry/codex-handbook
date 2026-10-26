---
id: codex-webmcp-site-tools
title: Codex Site tools（WebMCP）入门：网站怎么把操作交给内置浏览器里的 Codex，以及怎么给自己的网站加工具
seo_title: Codex Site tools（WebMCP）入门：内置浏览器的网站工具与接入方法
description: Site tools 是 ChatGPT 对 WebMCP 提案的实现，网站可以把操作注册成工具，让桌面端内置浏览器里的 Codex 直接调用。本文讲清它和 MCP 的区别、怎么查看和关闭、安全边界与限制，以及用 registerTool 给自己的网站加一个只读工具。
url: /guides/codex-webmcp-site-tools
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 解释
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-24
date_modified: 2026-10-24
verified_on: 2026-10-24
models: [gpt-6-sol]
official_ref: https://learn.chatgpt.com/docs/webmcp
keywords: [Codex Site tools, WebMCP, document.modelContext, registerTool, Codex 内置浏览器, WebMCP vs MCP]
related: [codex-browser-login-state, codex-browser-e2e-acceptance]
howto: false
faq:
  - q: Site tools 和 MCP 有什么区别？
    a: MCP 把 AI 应用连到本地或远程服务器，工具可以脱离网页独立工作；WebMCP 由网站自己在页面里注册工具，agent 打开页面时发现并使用，不需要另装 MCP 服务器，适合人和 agent 一起看同一个页面的场景。
  - q: 在哪里能用 Site tools？
    a: ChatGPT 桌面端的内置浏览器。ChatGPT Work 和 Codex 在页面提供工具时可以发现并使用。企业工作区需要管理员通过策略允许，Edu 工作区不可用。
  - q: 怎么关闭 Site tools？
    a: 在 Settings > Browser > Permissions 里关闭 Enable site tools。
---

# Codex Site tools（WebMCP）入门：网站怎么把操作交给内置浏览器里的 Codex，以及怎么给自己的网站加工具

> 本文在线版：[codexguide.io/guides/codex-webmcp-site-tools](https://codexguide.io/guides/codex-webmcp-site-tools)

> 核对依据：OpenAI 官方文档 [Site tools](https://learn.chatgpt.com/docs/webmcp)、[WebMCP 规范草案](https://webmachinelearning.github.io/webmcp/) 和 [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp) 仓库，核对日期 2026-10-24。Site tools 只在 ChatGPT 桌面端的内置浏览器里提供，本文**没有**在桌面端实际操作，界面名称均引自官方文档，因此不附截图。

Codex 在内置浏览器里操作网页，通常要像人一样读页面、找按钮、点击、输入。页面一改版，这套操作就可能失效。

WebMCP 换了个思路：**网站自己把能做的操作声明成工具**，比如“搜索文档”“在某一节留评论”“把图表日期范围改成上周”。agent 打开页面时发现这些工具，直接调用，不用再猜按钮在哪。ChatGPT 把它的实现叫 **Site tools**。

## Site tools 是什么

官方文档的定义：Site tools 是 ChatGPT 对 [WebMCP 提案标准](https://webmachinelearning.github.io/webmcp/) 的实现。网站可以在原有界面之外，把有用的操作直接提供给 AI agent；你和 agent 使用同一个实时页面、同一个登录会话。

在 ChatGPT 桌面端的[内置浏览器](https://learn.chatgpt.com/docs/browser)里，页面提供了这些工具时，ChatGPT Work 和 Codex 可以发现并使用它们。

WebMCP 目前还是提案，规范草案在 GitHub 的 [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp) 仓库里讨论和维护。核对时这个仓库有约 4,700 个 Star，最近一次推送在 2026-10-21。仓库 README 的说法是：WebMCP 让开发者把 Web 应用的功能以“工具”的形式暴露出来，也就是带自然语言描述和结构化 schema 的 JavaScript 函数，供 AI agent 调用。

### 使用条件

按官方文档：

- 更新 ChatGPT 桌面端到最新版本。
- 企业（Enterprise）工作区需要管理员通过工作区策略允许 **Site tools**。
- Edu 工作区不提供。
- 能否使用还取决于灰度进度和当前页面有没有提供工具。
- 模型方面，文档原文写的是：「Use GPT-5.6 Sol or GPT-6 Sol for site tools. GPT-5.6 Luna currently has WebMCP disabled.」

> 说明：这句模型要求里的 GPT-5.6 系列名称和当前 Codex 默认模型（GPT-6.1 Sol 等）不一致，可能是文档没有随模型更新同步。本文照原文引用；实际用哪个模型，以你桌面端模型菜单和官方文档的后续更新为准。

## WebMCP 和 MCP 有什么区别

两者名字像，解决的问题不同：

| | MCP | WebMCP（Site tools） |
| --- | --- | --- |
| 工具由谁提供 | 本地或远程的 MCP 服务器 | 网站自己，在页面里注册 |
| 是否依赖打开的网页 | 不依赖，可以独立调用服务或 API | 依赖，工具属于提供它的页面 |
| 需要用户做什么 | 安装或连接 MCP 服务器 | 不需要额外安装，打开页面即可发现 |
| 适合的场景 | 搜索服务、通过 API 管理记录 | 人和 agent 要看同一个画面，如编辑画布、浏览仪表盘 |

一个网站可以同时提供两者：用带 MCP 服务器的插件做脱离页面的集成，再用 WebMCP 做页面内的协作。Codex 里 MCP 的用法见 [MCP 配置指南](https://codexguide.io/advanced/mcp)。

## 在内置浏览器里怎么用

1. 在桌面端的内置浏览器里打开网站，让 ChatGPT Work 或 Codex 帮你完成任务。
2. 页面提供了 Site tools 时，agent 会发现并调用相关操作。官方举的例子：文档编辑器可以让 agent 找到某一节，或者留一条评论给你审阅。
3. 想看网站提供了哪些工具：点地址栏里的 **Site tools**，再选 **Available site tools**，查看每个工具。
4. 想看 agent 最近调用了什么：有近期活动时，选 **Recently used**，打开 **Sources** 查看这些调用。

几个行为要知道：

- 工具属于提供它的页面。关闭页面或跳到别的页面后，工具可能就不可用了。
- 没有合适的工具时，agent 仍可以用普通的浏览器操作能力。
- 浏览器在网站执行每个请求前会先检查；执行后 agent 可以查看页面确认变化。

内置浏览器怎么登录、怎么处理登录态，见 [Codex 浏览器操作与登录态](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md)。

## 例子：用 Site tools 查 OpenAI 文档

官方文档以 ChatGPT Learn 和 OpenAI Developers 为例，这两个站点提供了查找和阅读文档的 Site tools。在文档页点 **Open in ChatGPT**，会在桌面端浏览器里打开文档页，旁边新建一个对话，并预填这样的提示：

```text
Find the documentation for building reusable skills, open the relevant page, and explain when I should turn a skill into a plugin.
```

agent 能用的工具：

| 工具 | 作用 |
| --- | --- |
| `search_openai_docs` | 搜索 OpenAI 文档 |
| `lookup_page` | 按路径或 URL 读取文档页 |
| `lookup_context` | 读取当前文档路由和选中的文字 |
| `navigate_to_page` | 在当前文档站打开匹配的页面 |
| `generate_custom_guide` | 发起生成一份定制的构建或学习指南，返回状态和链接 |

注意最后一个：Docs Agent 是**异步**生成指南的，拿到链接不代表已经生成完。

## 安全边界

官方文档在这部分写得很明确：

- **网站提供的工具定义和返回结果都是不可信内容。** 工具叫什么名字、声称自己“只读”，都不能证明它实际做什么。
- 网站里的说明**不会**授权 agent 分享无关信息或执行敏感操作。
- 内置浏览器里，**每次工具调用前都有安全审查**。网站访问和确认策略照常生效，发消息、购买、删除数据、改权限这类有后果的操作仍需确认。
- 每次调用都绑定到发起它的页面和工具注册。
- 这些检查能降低风险，但**不会让网站或它的输出变得可信**。

想关掉：**Settings > Browser > Permissions**，关闭 **Enable site tools**。

分享敏感信息或依赖某个改动之前，先看清网站、请求的操作和返回结果。

## 目前的限制

ChatGPT 内置浏览器目前只支持 WebMCP API 的一部分，下面两类不支持：

- **声明式 API**：通过 HTML 表单属性定义的工具，不会作为 Site tools 出现。
- **iframe 里的工具**：注册在 iframe 里的工具（同源、跨源都一样）不会被发现。

所以要在**顶层页面**用 JavaScript 注册工具。agent 仍可以用普通浏览器能力操作表单，但那不算 WebMCP 工具调用。

WebMCP 规范和 [Chrome 的开发者指南](https://developer.chrome.com/docs/ai/webmcp) 描述了更多 API，其中一部分内置浏览器暂不支持。

## 给自己的网站加一个工具

两种做法：让 Codex 帮你给正在开发的 Web 应用或 [Site](https://learn.chatgpt.com/docs/sites) 加上 WebMCP 支持，或者自己写。

让 Codex 做时，说清 agent 应该能做什么，并要求它**复用应用现有的逻辑和权限**。官方建议从应用已经支持的操作开始，例如：

- 仪表盘：让 agent 设置日期范围，查看图表背后的数据；
- 文档编辑器：让 agent 找到某一节、建议修改或留评论供你审阅；
- 旅行规划：让 agent 比较选项、更新行程，你在旁边看地图。

自己写的话，在页面的 JavaScript 模块里先检查浏览器支持，再注册工具。官方给的只读示例，返回当前页面标题：

```javascript
if (typeof document.modelContext?.registerTool === "function") {
  await document.modelContext.registerTool({
    name: "get_page_title",
    description: "Read the title of the current page.",
    inputSchema: {
      type: "object",
      properties: {},
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true },
    execute: async () => ({ title: document.title }),
  });
}
```

兼容的 agent 能发现 `get_page_title`，调用后拿到页面标题。需要参数的工具，在 `inputSchema` 里描述参数，在 `execute` 里调用应用已有的逻辑。

官方给的几条设计建议：

- 输入尽量窄，写清副作用；
- 返回足够的信息，方便核对结果；
- 用应用现有的认证、授权和输入校验，不要为工具另开一套；
- 不支持 WebMCP 的人和浏览器，照常使用原来的界面。

做完后，可以在内置浏览器里打开页面，用 **Site tools → Available site tools** 确认工具出现了，再让 Codex 调用一次，在 **Recently used → Sources** 里核对调用记录。用浏览器做端到端验收的方法，见 [Codex 浏览器端到端验收](https://codexguide.io/guides/codex-browser-e2e-acceptance)。

## 延伸阅读

- OpenAI Developers 博客 [Automating repetitive work at OpenAI with Codex](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex)（2026-08-25）介绍了 OpenAI 内部怎么用 Runme 和 WebMCP，把重复的工程任务变成可审阅、可复用的工作流。
- [WebMCP 规范草案](https://webmachinelearning.github.io/webmcp/)
- [Chrome：WebMCP 开发者指南](https://developer.chrome.com/docs/ai/webmcp)

## 参考资料

- [Site tools（OpenAI 官方文档）](https://learn.chatgpt.com/docs/webmcp)
- [Browser（OpenAI 官方文档）](https://learn.chatgpt.com/docs/browser)
- [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp)
