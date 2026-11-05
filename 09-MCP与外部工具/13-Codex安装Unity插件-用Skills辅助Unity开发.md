---
id: codex-unity-plugin
title: Codex 安装 Unity 官方插件：用 Skills 和 unity-cli 辅助开发
seo_title: Codex 安装 Unity 官方插件：两步 marketplace 与 Skills 核对
description: Unity Technologies 为 Codex 提供官方插件，用一套 Skills 覆盖建项目、UI、2D、渲染和变现。本文按 Unity 文档写两步安装和核对方法，并说明技能数量会变、本文未在 Unity Editor 里实测。
lede: 装的是 Unity 自己写的技能说明，让 Codex 按当前引擎的做法检查项目。它不是 Asset Store 里的包。
url: /guides/codex-unity-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI]
difficulty: 进阶
order: 13
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
official_ref: https://docs.unity.com/en-us/ai/unity-plugin/codex
keywords: [Codex Unity 插件, Unity Codex plugin, unity-cli, unity-agent-plugin, Codex Unity Skills]
related: [create-codex-skill, plugin-development-marketplace, mcp-getting-started]
faq:
  - q: 现在到底是 31 个技能还是 33 个？
    a: "2026-09-16 的 Unity 博客写的是起步 31 个，并说明还会继续加。2026-11-05 查看 GitHub 仓库 main 分支的 skills 目录，有 33 个子目录；当天 .codex-plugin/plugin.json 的 version 是 0.1.9-beta。安装后以新会话里的 /unity: 和 codex plugin list 为准。"
  - q: 能在 Unity Package Manager 或 Asset Store 里安装这个插件吗？
    a: 不能。Unity 文档写明它不是 Asset Store 插件或包，也不能通过 Package Manager 安装。Codex 侧用插件目录，或用 marketplace 的两条命令。
  - q: 本文在 Unity 编辑器里跑过这些技能吗？
    a: 没有。写作环境没有 Unity Editor。文中的安装命令、技能目录和版本来自 Unity 文档、博客和 GitHub 仓库，不是一次编辑器里的实测输出。
---

# Codex 安装 Unity 官方插件：用 Skills 和 unity-cli 辅助开发

> 本文在线版：[codexguide.io/guides/codex-unity-plugin](https://codexguide.io/guides/codex-unity-plugin)

> 核对依据：Unity 博客《[The Official Unity Plugin for Codex](https://unity.com/blog/unity-plugin-codex)》（2026-09-16，Christopher Addison）、Unity 文档《[Unity's plugin for Codex](https://docs.unity.com/en-us/ai/unity-plugin/codex)》与《[About Unity's plugin](https://docs.unity.com/en-us/ai/unity-plugin/about-unity-plugin)》，以及 GitHub 仓库 [Unity-Technologies/unity-agent-plugin](https://github.com/Unity-Technologies/unity-agent-plugin)。2026-11-05 通过 GitHub API 核对了仓库元数据、`skills/` 目录和 `.codex-plugin/plugin.json`。**本文未在 Unity Editor 中安装或调用这些技能**，下文没有编辑器截图，也没有假装跑过的命令输出。

这是 **Unity Technologies** 发布的第三方插件，用来给 Codex 增加 Unity 技能。它不是 OpenAI 编写的内置功能。仓库在 Unity Companion License 下授权，见仓库中的 [LICENSE.md](https://github.com/Unity-Technologies/unity-agent-plugin/blob/main/LICENSE.md)。

适合已经在用 Codex、项目是 Unity 6.0 或更高版本，并且希望建项目、UI、2D、渲染、音频或内购按 Unity 当前做法来做的人。

## 先看结论

通用编程助手面对 Unity 项目时，容易按网上重复最多的旧写法回答。Unity 的官方插件把各功能团队写的技能交给 Codex：先看你的项目，再用当前 API，并在交回结果前做核对。博客把这套插件和「自己先做一个 Unity 插件」的准备步骤对照，官方插件省掉的是这一步。

2026-09-16 的博客列出的交付物是：

- 起步 **31** 个技能，覆盖 UI Toolkit 与 uGUI、2D 与 tilemap、URP 与 Shader Graph、音频、导航与物理、IAP 与 LevelPlay、多人、Web 与本地化，并且还会继续增加。
- 终端里两步：添加 marketplace，再添加插件。也可以在 OpenAI 插件目录里一键安装。博客写明不需要按项目配置，换机器时也不用拷贝一份。
- `unity-cli` 技能：在终端里安装 Editor、创建和打开项目、管理包。
- 兼容 **Unity 6+**。文档《About Unity's plugin》写的前提是 **Unity 6.0 或更高**。

2026-11-05 再看仓库时，数量已经不是博文里的 31。当天 `skills/` 下有 **33** 个目录，`plugin.json` 的 `version` 是 **0.1.9-beta**。GitHub API 显示该仓库约 **608** star、**67** fork，`pushed_at` 为 **2026-11-04T19:19:48Z**。这些数字都会变，安装后以本机插件清单为准。

`plugin.json` 还声明 `requires_local_executor` 为 `true`，能力包括 Interactive、Read、Write。技能会指导 Codex 在你的机器上查看和修改 Unity 项目、管理包，并接触 IAP、广告和多人等服务。装之前看清仓库，让它改项目前仍走你平时的审批。

## 安装：插件目录，或终端两步

Unity 文档给出的 Codex 安装步骤是：

```bash
codex plugin marketplace add Unity-Technologies/unity-agent-plugin
codex plugin add unity@unity-agent-plugin
```

第一条把 [Unity-Technologies/unity-agent-plugin](https://github.com/Unity-Technologies/unity-agent-plugin) 加为 marketplace 来源。Codex 的 marketplace 命令接受 `owner/repo` 这种 GitHub 简写。第二条安装名为 `unity`、来自该 marketplace 的插件。

博客同时写了另一条路：在 OpenAI 插件目录里找到 Unity Technologies 名下的条目，一键安装。目录里的显示名以你客户端为准。`plugin.json` 里的 `displayName` 是 Unity，`developerName` 是 Unity Technologies，分类是 Developer Tools。

它**不是** Unity Asset Store 里的插件，也**不能**在编辑器的 Package Manager 里装。装完之后，技能跟随 Codex 的插件安装，而不是跟某个 Unity 工程的 `Packages` 目录走。

更新和移除，文档写的是：

```bash
codex plugin marketplace upgrade unity-agent-plugin
codex plugin remove unity@unity-agent-plugin
```

## 怎么确认装上了

文档要求先**新开一个 Codex 会话**，再做两件检查：

1. 输入 `/unity:`，斜杠菜单里出现技能。
2. 运行 `codex plugin list`，确认 `unity` 显示为已安装并启用。

`codex plugin list --json` 会打印 `installed` 和 `available`。需要记版本时，看其中的 `version` 字段，不要只记本文写过的 `0.1.9-beta`。

本文没有在已登录的 Codex 里执行这两条命令，所以上面没有贴「本机成功输出」。

## 技能按什么用，而不是按什么背

《About Unity's plugin》的用法是：用自然语言描述任务，或在斜杠菜单里点名技能。文档举的例子包括：给玩家做金币包内购、做设置界面、像素画面模糊或相机移动时抖动、用激励视频发金币、做六边形 tile 调色板、TextMeshPro 里中文显示成方框、检查 ScriptableRendererFeature 的 Render Graph。

同一页的实践建议是：

- **点名 UI 框架。** 新项目 Unity 推荐 UI Toolkit；已有项目若在用 uGUI，就写明 uGUI。一开始写明，比让代理猜测更有效。
- **结果看起来不对时，让它去读该技能的 `references/`。** 跳过这些参考文件时，输出经常是错的。
- **它会先提问。** 交互会话里这是预期行为。自动化流水线里，提示要写到不需要追问。
- **没有自动选中技能时，在请求里写上技能名。**

博客强调的差别是：技能来自负责该系统的 Unity 工程师，按引擎的实际行为测试，经过他们的安全审查，并随引擎更新。社区里也有人做了有用的 Unity 技能插件。官方插件额外提供的是：发布者是 Unity Technologies，技能和当前引擎版本放在一起维护。许可证是 Unity Companion License。

博客引用了 Stack Overflow 2025 Developer Survey 的三组数字，用来说明「几乎正确」的挫败感：66% 的人把「AI 方案几乎正确、但还差一点」列为首要挫折；45% 认为调试 AI 生成的代码更花时间；46% 不信任 AI 输出的准确性，信任的占 33%。这是博客对那次调查的引用，不是本文的问卷。

和自己写 Skill、自己打包插件的关系：

- 团队特有的流程，仍然用 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md) 写在仓库里。
- 要把技能、MCP 和 Hooks 打成别人能安装的包，见 [Codex 插件开发入门](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。
- 这个 Unity 插件走的是同一套 marketplace 安装，内容由 Unity 维护。MCP 的配置和登录是另一条线，见 [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。

## 2026-11-05 仓库里的技能目录

下表是当天 `skills/` 的 33 个目录名，按目录名归类，方便浏览。归类是本文为了阅读做的，不是博文原表。博文里的 31 个技能有的已经改名或合并，后来又增加了目录。完整说明以仓库里每个技能的 `SKILL.md` 为准。

| 阅读用分组 | 目录名 |
| --- | --- |
| 开工与工具 | `new-unity-project`、`unity-cli`、`unity-package-management`、`generate-editor-search-query` |
| UI 与文字 | `ui`、`ui-uitk`、`ui-ugui`、`ui-imgui`、`optimize-text-mesh-pro` |
| 2D 与场景物件 | `2d-pixel-perfect`、`sprite-editor`、`sprite-segment-3x3grid`、`manage-sprite-atlas`、`create-tile-palette-or-rule-tiles`、`craft-game-floors`、`create-2d-physics` |
| 渲染 | `urp-postprocessing`、`shader-graph-create-custom-node`、`validate-urp-render-graph-renderer-feature`、`migrate-birp-to-urp`、`asset-transformer-toolkit` |
| 音频 | `audio-setup-mixers`、`optimize-audio`、`setup-vivox-voice-chat` |
| 导航与物理 | `initialize-ai-navigation`、`physics-3d-collision` |
| 变现与线上服务 | `implement-in-app-purchases`、`levelplay-unity-integration`、`build-live-game` |
| 多人 | `setup-multiplayer-services` |
| 平台与本地化 | `optimize-web`、`localization`、`build-gtk` |

`unity-cli` 是其中一项技能，教 Codex 如何驱动 Unity CLI：安装 Editor、创建和打开项目、管理包、许可证与模块，以及构建、测试和读日志。Unity CLI 本身是独立的终端工具。[Unity CLI 文档](https://docs.unity.com/en-us/unity-cli/use-unity-cli)写明：使用 Claude Code、Codex 或 Grok 时，安装对应的 Unity 插件，插件里包含 `unity-cli` 技能和其他 Unity 技能。装上插件，并不等于已经在本机执行过 `unity install`。

博客对部分技能的行为边界仍然有用，例如 `/new-unity-project` 会收集概念、平台和变现方式，并在提问的同时安装 Editor、创建项目、源代码管理和包，**不会**顺便生成玩法代码。UI 路由技能会先判断项目用的是哪套 UI，再交给 UI Toolkit、uGUI 或 IMGUI。

`plugin.json` 里的示例提示包括：为 2D 游戏做带 rule tile 的 tilemap、实现内购并接上 LevelPlay、为游戏做多人 lobby 和网络。这些是插件自带的起步说法。

## 适用版本和权限

- **引擎**：Unity 6.0 或更高。更早的编辑器不在文档的兼容范围内。
- **许可证**：Unity Companion License（Unity 依赖项目）。仓库的 GitHub license 字段是 Other，不是一个 SPDX 标识；以 `LICENSE.md` 为准。软件按「AS IS」提供。
- **本机执行**：插件要求本地执行器，并声明读、写和交互能力。内购、广告、语音和多人技能会碰到账号、密钥和商店后台。这些步骤需要你自己的商店配置，插件不会替你创建开发者账号。
- **提问会挡住无人值守流水线。** 要在 CI 里跑时，把平台、UI 框架、包和验收写进提示，使它不必停下来问。

## 怎么验证

在有 Unity 6.0+ 和已登录 Codex 的机器上：

1. 运行文中的两条安装命令。
2. 新开会话，输入 `/unity:`，确认菜单里出现技能。
3. 运行 `codex plugin list`，确认 `unity@unity-agent-plugin` 为已安装且启用，并记下 `version`。
4. 打开一个 Unity 6 测试工程，用一句点名了 UI 框架的小请求（例如「用 UI Toolkit 做一个只有返回按钮的空设置屏」），再看生成文件是否落在该 UI 系统里。
5. 结果偏离时，让它读取对应技能的 `references/` 后重试。仍偏离就停，不要让它继续改正式工程。

本文的写作环境没有 Unity Editor，第 4 步没有执行。

## 参考资料

- [The Official Unity Plugin for Codex](https://unity.com/blog/unity-plugin-codex)（2026-09-16）
- [Unity's plugin for Codex](https://docs.unity.com/en-us/ai/unity-plugin/codex)
- [About Unity's plugin](https://docs.unity.com/en-us/ai/unity-plugin/about-unity-plugin)
- [Unity-Technologies/unity-agent-plugin](https://github.com/Unity-Technologies/unity-agent-plugin)
- [LICENSE.md](https://github.com/Unity-Technologies/unity-agent-plugin/blob/main/LICENSE.md)
- [Use the Unity CLI](https://docs.unity.com/en-us/unity-cli/use-unity-cli)
