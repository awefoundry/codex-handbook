---
id: plugin-development-marketplace
title: Codex 插件开发入门：用 $plugin-creator 打包 Skills、MCP 与 Hooks，再用 marketplace 分发
seo_title: Codex 插件开发：plugin-creator、plugin.json 与 marketplace 分发
description: 手里攒了几个 Skill 和 MCP 配置，怎样做成团队一键安装的 Codex 插件？按官方 Package your plugin：用 $plugin-creator 生成脚手架，写 plugin.json／mcp.json，弄清 Hooks 限制，再用 marketplace.json 与 codex plugin marketplace 命令分发。
lede: Skill 适合本机创作；要给别人安装、或和 MCP／Hooks 一起带走，就打成插件，再用 marketplace 分发。
url: /guides/codex-plugin-development-marketplace
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://developers.openai.com/codex/plugins/build
keywords: [Codex 插件开发, plugin-creator, plugin.json, mcp.json, marketplace.json, codex plugin marketplace]
related: [create-codex-skill]
faq:
  - q: $plugin-creator 和手写 plugin.json 哪个更好？
    a: @plugin-creator／$plugin-creator 最快，默认出兼容布局并可写本地 marketplace；清楚字段时可手写根目录可移植 plugin.json 与 mcp.json。两者可并存。
  - q: 带 Hooks 的插件能上公开插件目录吗？
    a: 不能。hooks 仅支持 Codex 桌面端手动安装的插件；含 hooks 者不能进公开目录。公开分发请去掉 hooks。
  - q: 个人 marketplace、仓库 marketplace 和公开目录有什么区别？
    a: 公开目录经提交流程上架。仓库级与个人级 marketplace 用于测试／团队分发。CLI 的 marketplace 命令跟踪源；安装本地插件以桌面端为主。
---

# Codex 插件开发入门：用 $plugin-creator 打包 Skills、MCP 与 Hooks，再用 marketplace 分发

> 本文在线版：[codexguide.io/guides/codex-plugin-development-marketplace](https://codexguide.io/guides/codex-plugin-development-marketplace)

> 核对依据：OpenAI《[Package your plugin](https://developers.openai.com/codex/plugins/build)》（与 [plugins/build/plugins](https://developers.openai.com/plugins/build/plugins) 同文）、[Plugins](https://developers.openai.com/codex/plugins)、以及面向对话创建的 [Build plugins](https://learn.chatgpt.com/docs/build-plugins)。文中「我的用法」是操作顺序建议，不是官方强制流程。本机未跑通 `$plugin-creator` 与桌面端安装，界面文案以你当前客户端为准。

Skill 适合本机或仓库里把流程写清楚；要给别人一键安装，或把 **Skills + MCP +（可选）Hooks** 捆在一起带走，官方路径是 **插件（plugin）**，再用 **marketplace** 分发。

这篇按一条主线走完：

1. 弄清插件里装什么  
2. 用 `$plugin-creator`／`@plugin-creator` 生成脚手架（或手写可移植清单）  
3. 写清 `plugin.json`／`mcp.json`，以及和旧版 `.codex-plugin/` 的关系  
4. 加 Hooks 前先看限制  
5. 本地 marketplace 安装验证  
6. 用仓库 marketplace 与 `codex plugin marketplace` 命令给团队用  

Skill 怎么写、怎么测触发，见姊妹篇《从零创建 Codex Skill》。Hooks 事件与信任审查另有专文；本文只写「插件里怎么挂、什么情况下不能上公开目录」。

## 1. 插件里装的是什么

按官方 Plugins／Package your plugin，一个插件可以把若干能力捆成可安装包：

| 组成部分 | 作用 | 常见落点 |
| --- | --- | --- |
| **Skills** | 可复用工作流说明（及可选脚本／参考资料） | 根目录 `skills/<name>/SKILL.md` |
| **MCP 服务器** | 连外部系统的工具与数据 | 可移植包用根目录 `mcp.json`；兼容脚手架可能生成 `.mcp.json` |
| **资源** | 图标、截图、模板等 | 建议 `./assets/` |
| **Hooks** | 在 Codex 运行时生命周期点执行命令 | `hooks/hooks.json` 与脚本；见下文限制 |
| **展示与注册映射** | 显示名、能力说明、已注册 MCP 映射等 | 写在根 `plugin.json` 的 `extensions.com.openai`，或兼容文件 `.codex-plugin/plugin.json` |

还可能出现 **onboarding skill**（`extensions.com.openai.onboardingSkill` 指向包内某份 `SKILL.md`），以及产品侧的浏览器扩展能力——打包细节以提交文档为准。

**公开插件**进入 ChatGPT／Codex **共用通用目录**；**本地／仓库 marketplace** 是测试与团队分发源，和公开目录分开。**IDE 扩展不支持插件**——浏览与安装用桌面端或 CLI 的 `/plugins`。标成 Desktop only 的插件须在桌面端安装。

**我的用法：** 先有至少一个测稳的 Skill（或一个已能连上的 MCP），再打包。空插件只有清单没有内容，安装后也验不出行为。

## 2. 最快路径：`$plugin-creator`／`@plugin-creator`

官方推荐的最快 OpenAI 专用路径是内置 **plugin-creator** skill：

- Codex CLI／桌面 Codex：`$plugin-creator`  
- ChatGPT Work：`@plugin-creator`

它会脚手架出一份 **受支持的兼容清单**（`.codex-plugin/plugin.json`），并可生成 **本地 marketplace 条目** 方便测试。已有插件文件夹时，也可以只用它把文件夹挂进本地 marketplace。

### 2.1 脚手架会生成什么

当前 scaffold 用的是 **Codex 兼容布局**，不是可移植 Agent Plugins 布局。若你请求全部可选组件，大致是：

```text
my-plugin/
├── .codex-plugin/
│   └── plugin.json      # 总会生成
├── .mcp.json            # 可选；初始为空的 mcpServers
├── .app.json            # 可选；初始为空的 apps
├── skills/
├── hooks/               # 可选；只建空目录，不含配置与脚本
├── scripts/
└── assets/
```

要点（对照官方 Plugin creator output）：

1. **只有** `.codex-plugin/plugin.json` 是必生成的。  
2. 清单里会声明 `skills: "./skills/"`；测技能型插件前，先把技能文件夹放进 `skills/`。  
3. 请求 hooks 时 **只创建空的 `hooks/`**，不会自动写出 `hooks.json` 或可执行脚本——要按 Hooks 文档自己补。  
4. **不要**把兼容脚手架的 `.mcp.json` 简单改名为 `mcp.json` 就当可移植包：可移植 MCP 格式还要求为每个服务器声明传输 **`type`**。

### 2.2 示例提示词

在 Work 里可以这样说（把 ID／名称换成你的）：

```text
@plugin-creator 用我的 MCP 服务器为 ChatGPT 和 Codex 创建一个插件。
使用 plugin_asdk_app_……，命名为 Acme Support。
请一并创建个人 marketplace 条目，方便我本地测试。
```

若要带已注册 MCP：先在 ChatGPT Plugins 用「Add custom MCP server」建连接，从 URL 复制 `plugin_asdk_app…` ID 交给 creator。生成后核对 `.app.json` 映射、清单里 `apps → ./.app.json`、`skills/` 内容；有个人 marketplace 则刷新后从本地源安装，**新开对话**再测。本预览环境未实跑 creator（见 `client_validation_pending`）。

## 3. 手写可移植包：`plugin.json` 与 `mcp.json`

新包建议用 **根目录可移植清单**。官方「先打一个只含 Skill 的最小包」：

```bash
mkdir -p my-first-plugin/skills/hello
```

`my-first-plugin/plugin.json`：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "Reusable greeting workflow"
}
```

`name` 用稳定的 **kebab-case**；宿主用它做插件标识与组件命名空间。可移植包从根目录 `skills/` **自动发现**技能，清单里 **不必**再写 `skills` 字段。

`skills/hello/SKILL.md`：

```md
---
name: hello
description: Greet the user with a friendly message.
---

Greet the user warmly and ask how you can help.
```

完整可移植清单还可含 `author`、`homepage`、`repository`、`license`、`keywords` 等——字段以 Agent Plugins schema 与提交说明为准，**不要自造键名**。

### 3.1 OpenAI 专用扩展：`extensions.com.openai`

展示文案、已注册 MCP 映射、hooks、onboarding 等放在根清单的 `extensions.com.openai`。身份字段（`name`／`version`／`description`）留在根上。示意（字段均来自官方示例）：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Reusable skills and MCP servers",
  "extensions": {
    "com.openai": {
      "apps": "./.app.json",
      "hooks": "./hooks/hooks.json",
      "onboardingSkill": "./skills/setup/SKILL.md",
      "interface": {
        "displayName": "My Plugin",
        "shortDescription": "Reusable skills and MCP servers",
        "developerName": "Your team",
        "category": "Productivity",
        "capabilities": ["Read", "Write"],
        "logo": "./assets/logo.png"
      }
    }
  }
}
```

完整 `interface` 还可含 `longDescription`、隐私／条款 URL、`defaultPrompt`、品牌色与截图等——以官方示例为准，不要自造键名。

路径规则：相对插件根，且以 `./` 开头；视觉资源尽量放在 `./assets/`。`apps` 只用于指向 `.app.json` 里的已注册 MCP 映射。

**与 `.codex-plugin/plugin.json` 的关系（官方明确）：**

- 根目录 `plugin.json` 是可移植入口；OpenAI 也接受遗留／Claude 兼容清单，但新包应优先可移植格式。  
- 当 `extensions.com.openai` **作为对象存在**时，它 **整体替换** `.codex-plugin/plugin.json` 作为 OpenAI 专用设置来源，**两者不会合并**。  
- 若根清单里没有该内联对象，才由兼容 overlay 提供那些设置。根上的身份与可移植组件始终以根清单／固定路径为准。  
- 加 Codex overlay 时：**只有**其 `plugin.json` 放在 `.codex-plugin/` 内；hooks、`.app.json` 等仍放在插件根。

### 3.2 捆绑 MCP：`mcp.json`

可移植 MCP 写在根目录 `mcp.json`，带 Agent Plugins MCP schema，并在 `mcpServers` 下命名：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "docs": {
      "type": "streamable-http",
      "url": "https://example.com/mcp"
    }
  }
}
```

认证写在各服务器 `extensions["com.openai"].auth`（`none`／`oauth`／`mixed`／`api_key` 等）。清单 **不写密钥**；`clientSecret` 不进包。公开远程端点须 HTTPS。安装后可用 `plugins."<plugin>".mcp_servers.<name>` 调 `enabled`、白名单与审批，不必改插件文件。

## 4. 加 Hooks 之前必须知道的限制

官方限制：

1. Lifecycle hooks **仅**支持在 **Codex 桌面端手动安装**的插件。  
2. **含 hooks 的插件不能进入公开插件目录。**  
3. 脚本须在执行环境存在；**网页安装不会部署脚本**（企业可用 MDM）。  
4. 安装／启用 **不会自动信任** hooks；审查信任前 Codex 会跳过插件自带（非托管）hooks。  
5. 云端编排的 ChatGPT Work **不支持**插件 hooks（详见官方 Plugins 页）。

未在扩展／兼容清单里定义 `hooks` 时，默认找 `hooks/hooks.json`；`extensions.com.openai.hooks` 的显式值会 **替换** 默认发现（不追加）。遗留包可把 `hooks` 写在 `.codex-plugin/plugin.json`。命令可用 `PLUGIN_ROOT`／`PLUGIN_DATA`（及兼容名 `CLAUDE_*`）。事件与信任见 Hooks 文档／计划中的站内 Hooks 专文。

**我的用法：** 团队内部桌面端自动化可以带 hooks；打算公开上架或给网页／多端用户用时，先拆掉 hooks，只留 Skills／MCP。

## 5. 本地测试：个人 marketplace → 安装 → 新对话

marketplace 是一份 **插件目录 JSON**。可以只挂一个插件做测试，再往同一份目录里继续加条目，变成个人或团队精选列表。

### 5.1 个人 marketplace

常见做法：

1. 把插件文件夹放到例如 `~/.codex/plugins/my-plugin`（路径只是示例，以 marketplace 条目为准）。  
2. 编辑 `~/.agents/plugins/marketplace.json`：

```json
{
  "name": "local-example-plugins",
  "interface": {
    "displayName": "Local Example Plugins"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "source": "local",
        "path": "./plugins/my-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

注意：顶层 `name` 标识 marketplace，`interface.displayName` 是桌面显示名；每条插件都要有 `policy.installation`、`policy.authentication`、`category`。`source.path` **相对 marketplace 根**（不是相对 `.agents/plugins/`），以 `./` 开头且不出该根；本地 `source` 也可写成字符串 `"./plugins/my-plugin"`。`policy.installation` 如 `AVAILABLE`、`INSTALLED_BY_DEFAULT`、`NOT_AVAILABLE`。

3. **重启 ChatGPT 桌面端** → Plugins Directory → 选你的 marketplace → 安装。  
4. **新开对话**（或 CLI 新会话）再测。改完插件文件后更新指向目录并重启桌面端。

桌面端也会读 `$REPO_ROOT/.agents/plugins/marketplace.json`（及遗留 `.claude-plugin/marketplace.json`）。安装缓存约在 `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`；本地版 `$VERSION` 为 `local`。也可用 plugin-creator 直接生成个人 marketplace 条目。

### 5.2 仓库内启用／禁用

发现靠 marketplace；是否对本仓库启用，用项目 `.codex/config.toml`（仅 **信任项目** 会加载）：

```toml
[plugins."my-plugin@local-repo"]
enabled = true
```

键名格式是 `插件名@marketplace顶层name`。`enabled = false` 可先关掉而不卸载；刷新 marketplace 时仍可能安装／刷新文件。这与工作区 Admin 导入的插件策略无关。

## 6. 分发给团队：仓库 marketplace 与 CLI

### 6.1 仓库级 marketplace

适合跟仓库一起走的团队精选：

1. 插件放在例如 `$REPO_ROOT/plugins/my-plugin`  
2. `$REPO_ROOT/.agents/plugins/marketplace.json` 里为每个插件加一条 `source.path`  
3. 同事拉取仓库后，重启桌面端，从该 repo marketplace 安装  

同一份 marketplace 可挂多个本地插件，或用 Git：`"source": "url"`（仓库根）／`"git-subdir"`（子目录 + `url`／`path`／`ref` 或 `sha`）。解析失败则 **跳过该条目**。也支持 `"source": "npm"`（需本机 npm；不跑 lifecycle scripts；`registry` 为无凭据 HTTPS）。

### 6.2 CLI：`codex plugin marketplace`

用 CLI **添加并跟踪** marketplace 源，而不手改 `config.toml`。官方示例：

```bash
codex plugin marketplace add owner/repo
codex plugin marketplace add owner/repo --ref main
codex plugin marketplace add https://github.com/example/plugins.git --sparse .agents/plugins
codex plugin marketplace add ./local-marketplace-root

codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace upgrade marketplace-name
codex plugin marketplace remove marketplace-name
```

来源可以是 GitHub 简写（`owner/repo` 或 `owner/repo@ref`）、HTTP(S)／SSH Git URL，或本地 marketplace 根目录。`--ref` 钉住 Git ref；`--sparse PATH` 仅对 Git 源有效，可重复。`list` 会打印 Codex 正在考虑的各 marketplace 及其解析根（含本地默认与已配置快照）。

**官方分工：** CLI 命令服务作者／目录搭建；**安装测本地插件用 ChatGPT 桌面端**。CLI `/plugins` 可按 marketplace 浏览、安装／卸载，Space 开关已装插件。管理员也可在系统或云管 `config.toml` 定义同格式 marketplace。

### 6.3 工作区发布 ≠ 公开目录

工作区管理员可把个人插件 Publish 到本工作区（选角色可见）；这 **不会** 进入公开目录。公开上架走提交门户。可用 `features.plugin_sharing = false` 关掉工作区分享。对话式创建见 [Build plugins](https://learn.chatgpt.com/docs/build-plugins)，与本篇文件级打包互补。

## 7. 对照官方示例时看什么

公开示例可看官方点名的 Figma、Notion、Build web apps 等包。对照时看：根上是可移植 `plugin.json` 还是 `.codex-plugin/`；`skills/` 与 `mcp.json`（或 `.mcp.json`）如何并列；有无 hooks（有则通常不是公开目录候选）。社区多宿主目录并存的仓库可作参考，但字段与命令仍以 OpenAI Package your plugin 为准，不要按第三方博客洗字段。

## 8. 发布前检查清单

- [ ] kebab-case `name`、版本与描述就绪；Skill 在 `skills/<name>/SKILL.md` 且测过触发  
- [ ] 可移植：`plugin.json` + 需要时的 `mcp.json`（含 `type`）；或明确使用兼容布局  
- [ ] 勿指望 `extensions.com.openai` 与 `.codex-plugin/plugin.json` 合并；路径一律 `./` 且在根内；密钥不进仓  
- [ ] 含 hooks → 仅桌面端手动安装，**不上**公开目录  
- [ ] marketplace 含 `policy`／`category`；`source.path` 相对 marketplace 根；安装后新会话验证  
- [ ] 项目开关用 `plugins."name@marketplace"`（信任项目）；公开／工作区走官方流程，不用自创 zip 约定  

## 参考资料

- [Package your plugin](https://developers.openai.com/codex/plugins/build)（[canonical plugins/build/plugins](https://developers.openai.com/plugins/build/plugins)）  
- [Plugins](https://developers.openai.com/codex/plugins)  
- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)（对话创建／编辑）  
- 姊妹篇：[从零创建 Codex Skill](https://codexguide.io/guides/create-codex-skill)（`create-codex-skill`）  
- Hooks 事件、信任与限制：见官方 Hooks 文档；站内 Hooks 专文计划另发  

本文按 2026-10-22 可访问的官方插件打包文档核对。`$plugin-creator` 与桌面端安装未在本预览环境实操（`client_validation_pending: true`）；命令与字段以你当前 Codex／ChatGPT 客户端及官方文档为准。
