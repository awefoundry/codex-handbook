---
id: codex-modern-web-guidance
title: Codex 安装 Modern Web Guidance 插件：Chrome 团队出品，让 Codex 写前端时用现代 Web API，不再堆旧 JavaScript
seo_title: Codex 安装 Modern Web Guidance：现代 Web API 指南插件实测
description: Modern Web Guidance 是 Chrome、Edge、Firefox 和 MDN 团队维护的 Skill 和命令行工具，让 Codex 写前端时先查现代 Web API 的写法，少用过时的 JavaScript 和重型库。本文用 Codex CLI 实测安装步骤，说明它怎么触发、search、retrieve、legacy-scan 怎么用，以及沙箱联网和遥测要注意什么。
lede: 两条命令装好；它靠 npx 拉取指南，所以在 Codex 沙箱里第一次运行要放行网络。
url: /guides/codex-modern-web-guidance
status: published
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI, IDE]
difficulty: 进阶
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-11
date_modified: 2026-11-11
verified_on: 2026-11-11
official_ref: https://github.com/GoogleChrome/modern-web-guidance
keywords: [Codex Modern Web Guidance, codex plugin marketplace add, modern-web-guidance@googlechrome, legacy-scan, 前端 Skill, Baseline]
related: [create-codex-skill, codex-chrome-devtools-mcp, codex-network-permissions-proxy]
faq:
  - q: 装了插件以后，要每次手动点名才会用吗？
    a: 不用。插件里的 modern-web-guidance Skill 的 description 写明，遇到 HTML、CSS 和浏览器端 JavaScript 任务时要先运行它，后端、CI、构建配置类任务不触发。想强制使用，也可以在提示里写 $modern-web-guidance。
  - q: 它会把我的代码上传吗？
    a: 项目 README 写明，search 用本地的嵌入模型和 BM25 检索，不调用网络 API、不需要 API Key。但它默认收集匿名使用数据，包括调用它的代理名称、取了哪些指南、代理生成的搜索词，不收集原始提示词。不想上报，设环境变量 DISABLE_TELEMETRY=1。
  - q: 为什么 Codex 跑 npx 时卡住或要求审批？
    a: Skill 是通过 npx -y modern-web-guidance@latest 拉取和运行的，需要访问 npm。Codex 默认沙箱不给命令联网，所以第一次运行会要求审批。可以只放行这一条命令，或者用网络权限 profile 只允许 registry.npmjs.org。
  - q: README 里的评测数字可信吗？
    a: 那是项目自己公布的评测结果（例如 11-08 一轮里 codex_cli 用 gpt-6.1-sol 从 54% 提到 82%），本站没有复现。可以把它当作项目方的自报数据参考。
---

# Codex 安装 Modern Web Guidance 插件：Chrome 团队出品，让 Codex 写前端时用现代 Web API，不再堆旧 JavaScript

> 本文在线版：[codexguide.io/guides/codex-modern-web-guidance](https://codexguide.io/guides/codex-modern-web-guidance)

> 核对依据：GitHub 仓库 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)（Apache-2.0）、官方文档页 [developer.chrome.com/docs/modern-web-guidance](https://developer.chrome.com/docs/modern-web-guidance)、npm 包 modern-web-guidance 1.0.0，以及 Hacker News 讨论（[Show HN，252 分 / 72 评论](https://news.ycombinator.com/item?id=50443812)，北京时间 11-11 抓取）和 Adrian Roselli 的评测文章。安装和命令输出是 2026-11-11 在 Linux 上用 **Codex CLI 0.165.0** 和临时 `CODEX_HOME` 实测的；写作环境的 Codex 没有登录，**没有在真实对话里测试 Skill 自动触发**。这是 Google Chrome 团队的第三方项目，不是 OpenAI 官方插件。

编码代理写前端时，经常默认用老办法：自己写一堆 JavaScript 管弹窗、手算 tooltip 位置、引入整个库做一个小效果。原因很直接，训练数据里旧代码多。Modern Web Guidance 想解决的就是这个：在 Codex 动手前，先给它一份「现在浏览器原生就能做」的写法。

## 先看结论

- **是什么**：一个 Skill 加一个命令行工具，覆盖 250 个现代 Web 特性，由 Chrome、Edge、Firefox 和 MDN 团队共同维护。
- **怎么装**：`codex plugin marketplace add GoogleChrome/modern-web-guidance`，再 `codex plugin add modern-web-guidance@googlechrome`。实测两条命令都成功。
- **怎么起作用**：Codex 接到前端任务时，按 Skill 说明先运行 `npx modern-web-guidance search`，再 `retrieve` 对应指南，照着写代码。
- **要注意**：它要用 npx 访问 npm，Codex 沙箱里第一次运行需要放行网络；默认有匿名遥测，可以关掉。

## 安装：两条命令

仓库 README 给 Codex 的安装方式：

```bash
codex plugin marketplace add GoogleChrome/modern-web-guidance
codex plugin add modern-web-guidance@googlechrome
```

实测输出（节选）：

```text
Added marketplace `googlechrome` from https://github.com/GoogleChrome/modern-web-guidance.git.
Added plugin `modern-web-guidance` from marketplace `googlechrome`.
```

装完用 `codex plugin list` 确认：

```text
PLUGIN                            STATUS              VERSION  SOURCE
modern-web-guidance@googlechrome  installed, enabled  1.0.0    …/marketplaces/googlechrome
```

这两条命令会在 `config.toml` 里写入两段配置：

```toml
[marketplaces.googlechrome]
source_type = "git"
source = "https://github.com/GoogleChrome/modern-web-guidance.git"

[plugins."modern-web-guidance@googlechrome"]
enabled = true
```

想暂时停用，把 `enabled` 改成 `false` 即可。插件入口和停用、卸载的通用做法，见《[Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)》。

README 还给了一个交互式安装器 `npx modern-web-guidance@latest install`，以及 `npx skills add GoogleChrome/modern-web-guidance` 只装 Skill 的方式。在 Codex 里用插件方式最直接，本文以插件为准。

## 插件里有什么

插件的 `.codex-plugin/plugin.json` 写明版本 1.0.0、开发者 Google Chrome、类别 Developer Tools，带两个 Skill：

| Skill | 管什么 |
|---|---|
| `modern-web-guidance` | HTML、CSS、浏览器端 JavaScript：弹窗和 popover、表格、深色模式、锚点定位、容器查询、视图过渡、表单校验、无障碍、Core Web Vitals、安全等 |
| `chrome-extensions` | 用 Manifest V3 开发和发布 Chrome 扩展 |

`modern-web-guidance` 下面有 17 个分类目录（accessibility、css、forms、html、performance、security、ui-components 等），实测统计共 234 个 Markdown 指南文件。

它的 `description` 写得很明确：前端任务**必须先运行**；后端（SQL、ORM、API 路由）、基础设施（CI/CD、Docker、Actions）、构建配置（Vite、tsconfig、ESLint）**不要触发**。这是一个写得好的 Skill 描述样例：触发词靠前、边界清楚。自己写 Skill 时可以参考，见《[从零创建 Codex Skill](./04-从零创建Codex-Skill.md)》。

## 它怎么工作：search 和 retrieve

Skill 里给 Codex 的流程分三步：

1. **search**：用 2～5 个词描述一个功能点，比如 `"light dismiss dialog"`，不要带框架名。
2. **retrieve**：按返回的 id 取完整指南，可以一次取多个。
3. **核对**：写完后对照指南检查，并在回复末尾加一节 `### Modern Web Guidance`，说明用了哪条指南、避开了什么坑。

你也可以不经过 Codex，直接在终端试：

```bash
npx modern-web-guidance@latest search "animate a dialog modal backdrop"
```

实测返回 10 条，前几条是：

```text
[{"id":"animate-to-from-top-layer","description":"Animate elements such as dialogs, popovers, and tooltips as they're entering/exiting the top layer."},
{"id":"light-dismiss-a-dialog","description":"Create a modal dialog that can be closed via light dismiss ..."},
{"id":"prevent-page-scroll-under-modal-dialog","description":"Prevent the underlying page from scrolling while a modal dialog is open."},
...]
```

`retrieve` 的输出比较长。实测 `retrieve secure-external-subresources` 约 14.5 KB，工具会把它存到临时文件，提示代理完整读取。

README 写明，search 用的是本地的嵌入模型加 BM25，不调网络 API、不需要 API Key；用 npx 是为了让指南保持最新。

## 实测：用 legacy-scan 扫一个旧页面

如果你想整体看看项目里有哪些旧写法，用 `legacy-scan`。我准备了一个故意写旧的页面（用 CDN 引 jQuery、手写弹窗显示、手算 tooltip 位置），运行：

```bash
npx modern-web-guidance@latest legacy-scan site
```

实测输出：

```text
Modern Web Guidance Analyzer — site
Found 1 modernization opportunity across 1 guide (scanned 33 guides with deterministic rules; ~20% of the guidance corpus):

* secure-external-subresources (1 finding)
  Add Subresource Integrity (integrity="sha384-..."), crossorigin="anonymous", and referrerpolicy="no-referrer" to versioned third-party CDN <script> and <link rel="stylesheet"> elements.
  - index.html:5
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script></head>
```

怎么看这个结果：

- 它只扫了 33 个有确定规则的指南，约占全部指南的 20%。手写弹窗、手算定位这类问题这次没报出来。**扫描结果为空不等于没有旧写法**。
- 每条结果带「什么时候保留／什么时候丢弃」的判断标准，Skill 要求 Codex 逐条核对、去掉误报。
- Skill 说明里写着：只有你要求「整体现代化」或「扫旧写法」时才跑 legacy-scan；具体做某个功能时不跑。

在 Codex 里可以这样提：

```text
用 $modern-web-guidance 扫一下 src/ 里的旧 Web 写法，只出报告，先不改代码。每条结果说明你保留还是丢弃，以及理由。
```

## 沙箱与联网：npx 需要访问 npm

这是在 Codex 里用它最容易卡住的地方。Skill 自己的说明写了：拉取 modern-web-guidance 需要出网；在 Codex、Claude Code 这类有沙箱和审批的环境里，**第一次运行前就应该申请联网**；`~/.npm` 只读时设 `NPM_CONFIG_CACHE=/tmp/npm-cache`；放行时只放行 `npx -y modern-web-guidance@latest *`，不要放行所有 `npx`。

对应到 Codex 的做法：

- **按次审批**：第一次弹出审批时只批这一条命令。
- **用网络 profile 只放行 npm**：在 permission profile 里开 `network.enabled`、`features.network_proxy`，域名只允许 `registry.npmjs.org`。写法和实测见《[Codex 网络权限怎么配](../10-配置模型与权限安全/26-Codex网络权限-network_proxy域名白名单与本地服务访问.md)》。
- **离线环境**：Skill 写明可以用 `npx --offline` 重试（前提是本机缓存里已经有这个包）。

## 实验特性开关与 .mwgrc

默认情况下，Origin Trial 阶段的 API 和「易变特性」（只有一个浏览器引擎发布、发布不到 3 个月或还在变化的特性）的指南能搜到，但取不到全文。要打开，用：

```bash
npx modern-web-guidance@latest set-allow-origin-trials
npx modern-web-guidance@latest set-allow-volatile-features
```

这会写进项目根目录的 `.mwgrc`（对应键 `allowOriginTrials`、`allowVolatileFeatures`），可以提交到仓库让团队共用；没有项目级文件时会读 `~/.mwgrc`。

浏览器兼容性方面，Skill 默认认为 **Baseline Widely available** 的特性可以直接用；不是的，按指南写降级方案。如果你的项目有明确的浏览器支持要求，Skill 建议写进 `AGENTS.md`，比如「允许 Newly Available 特性，但降级代码不超过 20 行、不引入外部依赖」。

## 遥测与关闭方法

README 写明，Google 会收集匿名使用数据：安装次数、调用它的代理名称、取了哪些指南、代理生成的搜索词；不收集原始提示词。关闭方法：

```bash
export DISABLE_TELEMETRY=1
```

写进 `.bashrc` 或 `.zshrc`。公司项目对出网有要求的，先确认这一点再装。

## 它的局限：指南不保证被用上

Modern Web Guidance 在 2026 年 5 月作为早期预览发布，11-10 发了 npm 1.0.0。有两点要心里有数：

- **代理不一定会用指南**。无障碍顾问 Adrian Roselli 在《[Maybe Don't Rely on Google's "Modern Web Guidance"](https://adrianroselli.com/2026/05/maybe-dont-rely-on-googles-modern-web-guidance.html)》里，用官网第一个示例提示词（带动画的手风琴组件）实测，结果动画在 Firefox 里不工作，还有不符合 WCAG 的问题。他引用参与项目的专家的话：LLM 的输出不确定，即使有相关指南，也不保证会被取用、被读完。
- **legacy-scan 只覆盖约 20%**，上面实测里已经看到了。

所以它是减少旧写法的辅助，不能代替测试和人工审查。前端改动照常要在多个浏览器里试，并做键盘和读屏检查；团队已有成熟组件库的，继续优先用组件库。

## 常见问题

**和 Chrome DevTools MCP 有什么区别？**
Modern Web Guidance 管「写之前查写法」；Chrome DevTools MCP 管「写完在浏览器里查控制台、网络和性能」。两个可以一起用，见《[Codex 接入 Chrome DevTools MCP](../09-MCP与外部工具/06-Codex接入Chrome-DevTools-MCP-控制台网络与性能排查.md)》。

**用 React、Vue 也能用吗？**
可以。指南用原生 HTML/CSS/JS 写，Skill 里有一段专门讲怎么在框架里保留这些特性（比如 SSR 时判断 `window`、用 ref 调 `showModal()`）。

**怎么更新？**
插件方式安装的，按插件的更新方式处理；用 `npx modern-web-guidance install` 装的，用 `npx modern-web-guidance@latest update`。Skill 每次都用 `@latest` 调 CLI，指南内容本身会跟着 npm 更新。

## 参考资料

- [GoogleChrome/modern-web-guidance（GitHub）](https://github.com/GoogleChrome/modern-web-guidance)
- [Modern Web Guidance 文档（developer.chrome.com）](https://developer.chrome.com/docs/modern-web-guidance)
- [Show HN 讨论](https://news.ycombinator.com/item?id=50443812)
- [Adrian Roselli：Maybe Don't Rely on Google's "Modern Web Guidance"](https://adrianroselli.com/2026/05/maybe-dont-rely-on-googles-modern-web-guidance.html)

本文按 2026-11-11 的仓库内容和 npm 1.0.0 实测。版本更新后，指南数量和命令输出可能不同。
