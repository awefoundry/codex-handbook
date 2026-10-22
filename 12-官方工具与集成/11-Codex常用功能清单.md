---
id: codex-changyong-gongneng-qingdan
title: Codex 常用功能清单（2026-10）：/config、即时 Steer、/keymap，以及仍值得每天用的几项
seo_title: Codex 常用功能清单：/config 设置面板、即时 Steer、/keymap
description: 按 2026-10 官方 changelog 与 Developer commands，整理 Codex CLI／TUI 里最值得先学会的功能：可搜索的 /config、回应中即时 Steer、/keymap 与 leader key，以及 /side、/review 等日常入口。
lede: 功能一多，容易只剩「把整件事塞进一个会话」。先学会改设置、中途纠偏、改快捷键这三件事，再补讨论分流与审查。
url: /guides/codex-changyong-gongneng-qingdan
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 清单
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 基础
order: 11
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-09-01
date_modified: 2026-10-22
client_validation_pending: false
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://learn.chatgpt.com/docs/developer-commands
keywords: [/config, Steer, /keymap, Codex 常用功能, leader key, /side, /review]
related: [permissions-sandbox-approvals, usage-limits-credits]
faq:
  - q: Steer 和按 Tab 排队有什么区别？
    a: 官方写明：Codex 正在工作时按 Enter 发送，是把新指令注入当前这一轮（即时 Steer）；按 Tab 则把提示、斜杠命令或本地命令排到下一轮。前者改正在做的事，后者等这一轮结束后再生效。
  - q: /config 改完一定马上生效吗？
    a: 不一定。Codex CLI 0.163.0 起，/config 可搜索偏好、对支持项立即生效，并标明哪些改动需要重启。看到「需重启」提示时，按提示重启后再验证。
  - q: /keymap 的改动保存在哪里？
    a: 官方说明自定义绑定会写入 config.toml 的 tui.keymap。还可配置 leader key（默认 Ctrl+X）；上下文相关绑定优先于 tui.keymap.global，空绑定列表表示取消该动作。
---

# Codex 常用功能清单（2026-10）：/config、即时 Steer、/keymap，以及仍值得每天用的几项

> 本文在线版：[codexguide.io/guides/codex-changyong-gongneng-qingdan](https://codexguide.io/guides/codex-changyong-gongneng-qingdan)

> 核对依据：learn.chatgpt.com 的 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)、[Developer settings](https://learn.chatgpt.com/docs/developer-settings)、[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)，以及 2026-10-15 发布的 [Codex CLI 0.163.0 changelog](https://learn.chatgpt.com/docs/changelog)。文中「我的用法」是建议顺序，不是官方强制流程。界面文案随客户端变化，以你本机菜单为准。

很多人第一次用 Codex，会把讨论、改文件、排错、复查全堆进同一个长会话。功能其实不少，但真正决定「顺不顺手」的，往往是几件小事：

1. **设置能不能快速改对**（不用退出去翻 `config.toml`）。
2. **它还在跑的时候，能不能及时纠偏**（不用干等一轮结束）。
3. **常用操作能不能变成肌肉记忆**（快捷键、侧边讨论、单独审查）。

2026-10 的 CLI 0.163.0，正好把前两件补强了：可搜索的 `/config`、回应中的即时 Steer、以及 `/keymap` 的 leader key。下面按「先学什么」列一张清单；每条都对应官方文档或正式 changelog，不写未核实的第三方技巧。

## 先看一张总表

| 你想做什么 | 先用什么 | 官方要点 |
|---|---|---|
| 搜设置、改偏好 | `/config` | 跨分类搜索；支持项立即生效；标明需重启项（CLI 0.163.0） |
| 它还在输出／跑工具时改方向 | 直接发跟进（Steer） | 回应中发送可立刻纠偏；打断也会停掉活跃的 Code Mode 单元及其嵌套工具调用 |
| 这一轮先别打断，只记下下一句 | `Tab` 排队 | 排队的提示／斜杠／本地命令在**下一轮**才解析执行 |
| 改快捷键、设 leader key | `/keymap` | 写入 `tui.keymap`；leader 默认 `Ctrl+X`；提示保持到选定或取消；语音静音改到 `F9` |
| 重启托管后台服务 | `/daemon` | 会提示可能打断的工作，确认后重启并自动重连 |
| 方案讨论不污染主会话 | `/side`（别名 `/btw`） | 临时侧聊，记录与主会话分开 |
| 改完先看问题再动手修 | `/review` | 审查工作区变更；可用 `/diff` 看具体 diff |
| 确认当前模型／权限／用量 | `/status` | 活跃模型、审批策略、可写根、token 用量等 |

只读工具并行、Daybreak 等也在 0.163.0 里，属于「知道就好」：见文末补充，不必一上来就调。

## 1. `/config`：把设置面板当搜索框用

以前改偏好，多半是记键名、开 `~/.codex/config.toml`，或在零散的斜杠命令之间跳。**从 CLI 0.163.0 起**，在 TUI 输入 `/config` 可以：

- **按分类搜索**偏好；
- 对**支持即时生效**的项直接改；
- 看清哪些改动**需要重启**才生效。

这和 Developer settings 里「部分选择器只影响当前会话、部分可保存为默认」的思路一致：日常先在面板里改；要写成长期默认，再落到 `config.toml`（用户级 `~/.codex/config.toml`，受信任项目可用 `.codex/config.toml`）。

**我的用法**：新环境先打开一次 `/config`，搜 `model`、`approval`、`sandbox`、`tui` 这几个词，把默认模型和审批策略看一眼。需要一次性覆盖时，再用启动参数 `--model`、`--sandbox`、`-c key=value`（命令行优先级最高）。

不确定当前生效的是哪一层配置时，用 `/debug-config` 看层级顺序；会话摘要用 `/status`。

## 2. 即时 Steer：它还在说的时候就能纠偏

官方在 Interactive shortcuts 里写得很清楚：

- **Codex 正在工作时按 Enter**：把新指令**注入当前这一轮**（即时纠偏）。
- **按 Tab**：把跟进提示、斜杠命令或本地 shell 命令**排到下一轮**。
- 前缀 `!`：在当前审批与沙箱策略下跑本地命令。

CLI 0.163.0 进一步写明：在 Codex **正在回应时发送跟进**，可以**立刻 Steer**；打断一轮时，也会停掉活跃的 Code Mode 单元及其嵌套工具调用。桌面端同期修复里也提到次要窗口里的 Steer 恢复——说明「中途改口」已是产品主路径，不是隐藏技巧。

怎么选：

| 场景 | 做法 |
|---|---|
| 发现它跑偏了、改错目录了、范围扩太大了 | 立刻发一句纠正（Steer） |
| 现在这轮想让它做完，下一句再换任务／切模型 | `Tab` 排队，例如先排 `/model` 或下一条提示 |
| 只想停手 | 按客户端的中断快捷键（可用 `/keymap` 查看／改绑） |

**我的用法**：Steer 只写「纠正与边界」，例如「不要改测试以外的文件」「先停在只读调查」。不要把一整段新需求叠上去——那更容易让当前轮上下文更乱；大转弯时宁可打断后开新提示，或用下面的 `/side`。

## 3. `/keymap`：快捷键与 leader key

`/keymap` 用来查看、修改并持久化 TUI 快捷键。官方预期：改完后写入 `config.toml` 的 `tui.keymap`。

键名写法如 `ctrl-a`、`shift-enter`、`page-down`。**上下文相关绑定**优先于 `tui.keymap.global`；某个动作写成**空列表**表示取消绑定。

0.163.0 起还可在 `/keymap` 里配置 **leader key**：

- 默认是 **`Ctrl+X`**；
- 快捷键提示会**一直开着**，直到你选定或取消；
- **语音静音**改到 **`F9`**。

Config basics 里也有 `tui.keymap` 示例（如全局打开 transcript、composer 提交键等）。改之前先在 `/keymap` 里看清当前上下文（global／composer／chat…），避免把「提交」和「打断」绑冲突。

**我的用法**：只改你每周至少用十次的动作（打断、复制最近输出、打开 transcript）。leader key 适合「一组快捷键」；若你几乎不用组合键，保持默认即可。

## 4. `/daemon`：后台服务要重启时走这里

TUI 的 `/daemon` 用于查看与托管后台服务相关的连接与操作。0.163.0 起支持从这里**重启托管后台服务**：Codex 会**警告可能打断的工作**，确认后重启并**自动重连**。

适合：服务版本／功能开关和当前 CLI 不一致、远程控制异常、官方提示需要更新后台组件时。不要把它当成「卡一下就重启」的万能按钮——先看警告里会丢什么。

## 5. `/side`：方案讨论留在侧边

原文强调的 Side Chat，在官方斜杠表里对应 **`/side`（别名 `/btw`）**：开一个**临时侧聊**，记录与主会话分开；也可带一句内联问题，例如 `/side 这个方案有没有明显风险`。

官方限制：

- 已在侧聊里时，不能再开一层 `/side`；
- **审查模式（review）期间不可用**。

主会话还在跑时，侧聊里仍能看到主会话状态，方便判断要不要回去 Steer。

**我的用法**：架构二选一、要不要引入依赖、风险清单——放 `/side`；已经定稿的执行指令，再回到主会话。不要把侧聊当长期档案；需要留档时用 `/export` 或自己的交接笔记。

（桌面端若还有「快速聊天／旁路入口」，以你当前 App 菜单为准；CLI／TUI 以 `/side` 为官方入口。）

## 6. `/review` + `/diff`：改完先审，再决定修

原文「单独开一次 Review」仍然成立，且有正式命令：

1. `/review`：让 Codex 审查工作区变更（行为变化、缺测等）；默认用当前会话模型，也可在 `config.toml` 设 `review_model`。
2. `/diff`：查看 Git diff（含尚未被 Git 跟踪的文件）。

非交互场景还可用终端子命令 `codex review`（例如 `--uncommitted`、`--base`、`--commit`），与 TUI 内 `/review` 是同一类能力的不同入口。

**我的用法**：审查提示里写清「只报告、先不改」。需要修的时候再开新一轮，避免「审查顺手改掉」把证据冲掉。权限更松的环境里尤其重要——审批与沙箱细节见《权限、沙箱与审批》。

## 7. 另外五个高频入口（知道位置就够）

这些不是 0.163.0 新发明，但和上面几项一起构成日常工作台：

| 命令 | 用途 |
|---|---|
| `/model` | 切换当前模型；支持时还可选推理强度。列表以账号／工作区目录为准。 |
| `/permissions` | 会话中调整审批预设（如 Auto／Read Only）；有命名权限档案时也会出现。 |
| `/status` | 核对模型、审批、可写根、用量；远程连接时还会显示远端地址与服务版本。 |
| `/compact` | 长对话后压缩可见上下文，保留要点、腾出窗口。 |
| `/copy`（或 `Ctrl+O`） | 复制**最近一次已完成**的 Codex 输出；进行中的一轮不会当「最新完成」。 |

文件定位继续用 `@` 搜索工作区路径，或 `/mention` 挂上指定文件。需要持久仓库说明时用 `/init` 生成 `AGENTS.md` 草稿，再自己改到可提交。

## 8. 0.163.0 里「知道即可」的两项

- **只读工具并行**：独立的只读工具（含 skill、memory、会话历史查找等）可以并行跑。你通常不用开关；体感是调查类步骤有时更快。不要据此假设「写文件／跑命令也会无脑并行」——并行范围是 changelog 写明的只读类。
- **Daybreak**：对符合条件的账号默认开启；`codex exec` 在服务端提供且使用 API key 时也可选用。是否出现、如何计费以你的账号与模型目录为准，本文不展开资格表。

桌面端另有 **Composer predictions**（回应后在输入框给出下一句草稿，`Tab` 接受为可编辑草稿、不会替你发送）：Beta，年龄与套餐／地区有限制，且限本地与 SSH 线程上的 GPT-6 Astra／GPT-6.1 Sol。不符合条件时看不到是正常的。

## 我建议的启用顺序

不是官方步骤，按这个顺序改，通常第二天就能感到差别：

1. **更新到含 `/config` 的 CLI**（changelog 示例：`npm install -g @openai/codex@0.163.0`，或以你安装渠道的当前稳定版为准）。
2. 打开 **`/config`**，确认默认模型与审批／沙箱相关项；需重启的项记下来。
3. 故意做一次 **Steer**：让它开始改文件后，发一句收窄范围，确认它转向而不是无视。
4. 打开 **`/keymap`**，确认打断与复制键；leader 不熟就保持 `Ctrl+X`。
5. 下一场稍大的任务：方案分歧用 **`/side`**，落地后用 **`/review`**，必要时 **`/diff`**。

若只改两处：先练 **Steer vs Tab 排队**，再练 **`/config`**。前者减少「看它跑错却只能干等」，后者减少「改个设置要退出重来」。

## 参考资料

- [Developer commands（斜杠命令与交互快捷键）](https://learn.chatgpt.com/docs/developer-commands)
- [Developer settings](https://learn.chatgpt.com/docs/developer-settings)
- [Config basics（`config.toml` 与 `tui.keymap`）](https://learn.chatgpt.com/docs/config-file/config-basic)
- [ChatGPT & Codex changelog · CLI 0.163.0（2026-10-15）](https://learn.chatgpt.com/docs/changelog)

想继续系统学习 Codex，可以访问 [CodexGuide 教程网站](https://codexguide.io)。
