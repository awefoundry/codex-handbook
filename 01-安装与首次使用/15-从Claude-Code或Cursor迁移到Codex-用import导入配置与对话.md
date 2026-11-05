---
id: import-from-claude-code-cursor
title: 从 Claude Code 或 Cursor 迁移到 Codex：用 /import 导入 CLAUDE.md、Skills、MCP、Hooks 和最近 30 天对话，导入后要检查什么
seo_title: 从 Claude Code／Cursor 迁移到 Codex：/import 导入配置与对话
description: 从 Claude Code 或 Cursor 换到 Codex，不必从头配置。本文按官方 Import 文档走一遍：桌面端与 CLI 各能导入什么，指令文件、settings、Skills、MCP、Hooks 会落到哪，CLI 的 50 条／30 天对话上限，以及导入后必须复查的五类设置。
lede: 先用 /import（或桌面端 Settings → Import）把能搬的搬过来，再按官方清单把权限、MCP、Hooks 和命令模板核对一遍。
url: /guides/codex-import-from-claude-code-cursor
status: published
section: guides
category: B-install-login
topic: 认识、安装与环境
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 基础
order: 15
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/import
keywords: [Claude Code 迁移 Codex, Codex /import, CLAUDE.md 转 AGENTS.md, Cursor 迁移 Codex, Codex 导入配置]
related: [create-codex-skill, mcp-getting-started, hooks-guide]
howto: true
faq:
  - q: 桌面端和 CLI 能从哪些 agent 导入？
    a: 官方写明：ChatGPT 桌面端可从 Claude Code、Claude Cowork、Cursor 导入；Codex CLI 可从 Claude Code 或 Cursor 导入。CLI 对话发现上限是最近 30 天内最多 50 条。
  - q: 什么时候 /import 不可用？
    a: 官方开发者命令页写明：须在本地 TUI 会话里运行；任务正在执行时、远程会话中、或已连接到本地 app-server daemon 时不可用。可先结束当前任务、断开远程／daemon，再在本地会话输入 /import。
  - q: 导入会不会覆盖或删掉我现有的 Codex 配置？
    a: 不会。官方明确：Importing doesn’t change or delete your existing agent setup。导入只把你勾选的内容带进 Codex／ChatGPT，原 agent 侧配置保持不动。
---

# 从 Claude Code 或 Cursor 迁移到 Codex：用 /import 导入 CLAUDE.md、Skills、MCP、Hooks 和最近 30 天对话，导入后要检查什么

> 本文在线版：[codexguide.io/guides/codex-import-from-claude-code-cursor](https://codexguide.io/guides/codex-import-from-claude-code-cursor)

> 核对依据：learn.chatgpt.com《[Import from another agent](https://learn.chatgpt.com/docs/import)》、同站《[Developer commands](https://learn.chatgpt.com/docs/developer-commands)》中的 `/import` 说明，以及 Codex CLI `0.140.0` release notes（首次加入 `/import`）与 2026-08-11 What’s new（桌面端导入与 Cursor）。文中「我的用法」是操作顺序建议，不是官方强制流程。本文未在本机实装 Claude Code／Cursor 做端到端导入。

已经在 Claude Code 或 Cursor 里攒了一套项目规则、斜杠命令、MCP 和近期对话时，换到 Codex **不必从零重写**。官方提供统一的导入流：桌面端走 **Settings → Import**，CLI 走 **`/import`**。

这篇讲清三件事：**能搬什么、怎么搬、搬完必须查什么**。

## 迁移前先想清楚：哪些值得搬，哪些更适合重写

值得优先勾选的：

- **项目指令**（CLAUDE.md／同类 instruction 文件）→ 导入后落到 `AGENTS.md`，是 Codex 读项目习惯的主入口。
- **MCP 配置**、**Skills**／斜杠命令、**Hooks**——搬过来再按 Codex 语义微调，通常比重配省事。
- **最近仍在跟进的对话**——CLI 有「最近 30 天、最多 50 条」的发现上限；更早的线程不要指望自动带过来。

更适合在 Codex 里重写或后补的：

- 强依赖源 agent **独有工具名／独有审批模型** 的长规则（导入后可能「文件在、行为不对」）。
- **带参数插值、shell 展开、路径占位符** 的命令模板——官方把这类列为导入后必查项。
- 需要 **重新授权** 的插件、marketplace、自定义认证 MCP——导入只会标出「还要 Finish」，不会替你完成登录。

**硬保证（官方）：** 导入**不会**修改或删除你现有的 Codex／ChatGPT agent 配置；原 Claude Code／Cursor 侧文件也保持不动。

**版本线（便于判断客户端够不够新）：**

| 节点 | 内容 |
|---|---|
| Codex CLI **0.140.0**（约 2026-06-16 北京时间发布） | 加入 `/import`，当时面向从 Claude Code 选择性导入配置、项目文件与近期对话 |
| **2026-08-11** What’s new | 桌面端可从 Claude Code、Claude Cowork、Cursor 导入，并可开自动同步；CLI 也可从 Claude Code 与 Cursor 导入 |

以你当前客户端菜单为准；若没有 Import／`/import`，先升级桌面端或 CLI。

## 能导入什么、导入后放在哪：官方对照表

官方《Import from another agent》对照表如下（Destination 为 Codex／ChatGPT 侧落点）：

| 导入项 | 落点 |
|---|---|
| Instruction files（指令文件） | `AGENTS.md` |
| `settings.json` | `config.toml` |
| Skills | Skills |
| Plugins | Plugins |
| Existing project folders | 使用**同一文件夹**的 Projects |
| Project memories from Claude Code | Memories |
| Chats from the last 30 days | ChatGPT chats（桌面／会话侧） |
| MCP server configuration | Codex MCP configuration |
| Hooks | Codex hooks |
| Slash commands | Skills |
| Subagents | Codex subagents |

补充读法：

1. **指令 → `AGENTS.md`**：用户级与项目级都会被扫描；项目级来自你勾选的仓库／文件夹。
2. **`settings.json` → `config.toml`**：键名与语义不会一一等同，导入后要打开 `~/.codex/config.toml`（及项目级 `.codex/config.toml`）核对权限、模型与 MCP。
3. **斜杠命令 → Skills**：不是「在 Codex 里保留同名 `/foo`」，而是变成可被触发的 Skill；触发方式见姊妹篇《从零创建 Codex Skill》。
4. **Hooks → Codex hooks**：事件名与信任模型可能不同；导入后务必按 Hooks 文走 `/hooks` 审核。
5. **对话**：文档写「最近 30 天」；CLI 另写明发现上限 **50** 条。超过窗口的历史不会进自动导入。

桌面端可选范围还包括 Claude **Cowork**；CLI 官方步骤只列 **Claude Code** 与 **Cursor**。

## 在 Codex CLI 里用 `/import`

前置：本地已安装并登录可用的 Codex CLI；本机仍保留 Claude Code 或 Cursor 的用户级／项目级配置文件（导入靠读本机文件，不是读云端账号）。

步骤（与官方 Developer commands／Import 页一致）：

1. 启动**本地** Codex CLI 会话（TUI）。
2. 输入 `/import`。
3. 选择 **Claude Code** 或 **Cursor**。
4. 勾选要导入的 setup、项目文件与近期 chats。
5. 导入结束后，在 Codex 里打开对应项目／配置继续工作。

**CLI 对话上限：** 最多导入最近 **30 天**内的 **50** 条 chats。

### 什么时候 `/import` 不可用

官方写明下列情况**不能**用 `/import`：

- **任务正在运行**（running task）
- **远程会话**（remote session）
- **已连接到本地 app-server daemon**

处理顺序建议：结束或等当前任务完成 → 断开远程／不要挂着 daemon 连线 → 新开本地 TUI → 再 `/import`。

## 在 ChatGPT 桌面端导入

桌面端覆盖面更宽（含 Claude Cowork），并带 **Finish setup** 与可选自动同步。

1. 打开 **Settings → Import**。若还没有独立 Import 分区，到 **General** 里找 **Import other agent setup**。
2. 选 **Import**。
3. 勾选要导入的源 agent（Claude Code／Claude Cowork／Cursor），Continue。
4. 在 **Select items to import** 勾选 Tools & setup、Projects、Chat sessions 等，Continue。
5. 导入完成后，打开已导入的项目或聊天继续。

界面提示会强调：**Your existing agent setup won’t be affected.**

### 自动同步与导入历史

在 **Settings → Import** 可打开 **automatic updates**，让已导入内容与源 agent 保持同步；同一入口可查看 import history。

**我的用法：** 刚迁移的一两周可以开同步，核对稳定后若你已在 Codex 侧大改 `AGENTS.md`／Skills，再评估是否关掉，避免源侧旧规则反复盖回来。以你当前设置文案为准。

### 导入机制（桌面端摘要）

官方流程：

1. 检测支持的 setup 与近期工作（用户级文件 + 你选中的项目文件夹）。
2. 导入你勾选的项。
3. **不改动**现有 agent setup。
4. 检查插件／连接是否仍需收尾。
5. 需要时在左下角显示 **status card**，点 **Finish** 按提示补授权或设置。

## 导入后的检查清单：官方五类

官方「What to review after importing」要求在依赖这套配置前至少复查：

1. **导入的 skills 与 agents 里的工具限制／权限**  
   源侧「能自动做」的，在 Codex 可能要审批或根本没有同名工具。打开相关 Skill／subagent 定义，确认工具白名单与审批是否仍合理。

2. **使用自定义认证、headers、环境变量或传输方式的 MCP**  
   往往需要重新登录（`codex mcp login`、桌面端 Authenticate，或补 `env`）。连不上时先看 MCP 入门／排障文，不要把密钥贴进对话。

3. **导入后行为可能变化的 Hooks**  
   对照 Codex Hooks：事件、matcher、信任哈希。改过定义要在 `/hooks` 里重新信任；项目级 hooks 还依赖项目是否已信任。

4. **需要手动收尾的 Plugins、marketplace 或其他 setup**  
   跟 status card 的 Finish；marketplace 源或插件版本不一致时，按插件文档重装／启用，而不是假定「勾选了就等于可用」。

5. **依赖参数、shell 插值或文件路径占位符的 prompt／命令模板**  
   斜杠命令变成 Skill 后，参数传递方式可能不同。对每条「带 `$…`／路径占位」的模板做一次只读试跑，再用于写操作。

桌面端若弹出 Finish，优先把卡上的项做完，再进入下面的 `AGENTS.md` 润色。

## 把导入的 AGENTS.md 改成 Codex 写法

导入只解决「文件到位」。`AGENTS.md` 仍可能带有源 agent 的口吻、工具名或审批假设。

**我的用法（非官方清单）：**

1. 打开用户级与项目级 `AGENTS.md`，搜一遍源产品专有名词／工具名；改成 Codex 实际有的能力（读文件、改文件、跑命令、MCP、Skills）。
2. 删掉「必须调用某某源侧 UI 工具」这类在 Codex 无法执行的句子；改成可验收的项目约定（测试命令、目录边界、禁止提交的路径）。
3. 权限相关句子与 `config.toml`、Skill 内工具限制对齐，避免「文档说可以自动写、配置却要每次批准」。
4. 新开一轮短会话，让 Codex **复述**它读到的关键规则，再丢一个**只读**任务（例如总结模块职责、列出测试入口）。规则对得上再做写入类任务。

更系统的写法见计划中／站内的 AGENTS.md 专文；Skill 侧见《从零创建 Codex Skill》。

## 两边并用时怎么维护同一套规则

常见两种姿态：

- **Codex 为主：** 以 `AGENTS.md` + `~/.codex/config.toml` 为真源；Claude Code／Cursor 只作对照。桌面端自动同步适合「源侧仍在改、Codex 还在对齐」的过渡期。
- **短期双轨：** 共享的是**项目约定**（测试怎么跑、目录边界），不是两套完全镜像的 hooks／斜杠命令。Hooks 与 MCP 认证按各客户端分别维护，避免以为「导入一次就永远两边一致」。

**不要做的事：** 把源侧密钥文件提交进 Git；把未复查的 hooks 当成安全边界；在远程会话里干等 `/import` 出现。

## 少踩坑

1. **先本地、再导入**——远程／daemon／跑任务中没有 `/import`。
2. **勾选要克制**——先指令 + MCP + 近期对话，Skills／Hooks／插件分批，降低一次排障面。
3. **对话有窗口**——CLI 30 天／50 条；更早的内容请自行归档或在原客户端查阅。
4. **Finish 不是可选装饰**——插件与自定义 MCP 常常卡在授权。
5. **对照表不是行为等价保证**——尤其 Hooks、带插值的命令、工具权限。
6. **升级客户端**——极旧 CLI 可能只有早期 Claude Code 导入能力；Cursor／桌面端能力以 2026-08-11 之后的说明为准。

## 接下来读什么

- 《从零创建 Codex Skill》（斜杠命令导入为 Skills 之后怎么改、怎么测）→ `create-codex-skill`
- 《Codex MCP 入门》（导入的 MCP 如何登录与收紧权限）→ `mcp-getting-started`
- 《Codex Hooks 入门》（导入 hooks 后的信任与 PreToolUse／Stop）→ `hooks-guide`

## 参考资料

- [Import from another agent](https://learn.chatgpt.com/docs/import)
- [Developer commands · `/import`](https://learn.chatgpt.com/docs/developer-commands)
- [What’s new（2026-08-11 导入与同步）](https://learn.chatgpt.com/docs/whats-new)
- [Codex CLI 0.140.0（首次 `/import`）](https://github.com/openai/codex/releases/tag/rust-v0.140.0)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
