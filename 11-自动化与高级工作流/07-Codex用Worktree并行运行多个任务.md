---
id: worktree-parallel-chats
title: Codex Worktree 教程：用 Git worktree 并行跑多个任务，并把结果交回本地（Handoff）
seo_title: Codex Worktree：并行任务、Handoff 与 .worktreeinclude
description: 用 Codex 的 Git worktree 在同一项目里并行开多个聊天，互不踩 Local；学会 Hand off 交回本地、.worktreeinclude 带上忽略文件，以及托管 worktree 的清理规则。
lede: Local 是前台，Worktree 是后台。并行改代码时先隔离，确认后再用 Handoff 交回本地。
url: /guides/codex-worktree-parallel-chats
status: draft
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, ChatGPT Work]
difficulty: 进阶
order: 7
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/environments/git-worktrees
keywords: [Codex worktree, Git worktree 并行, Handoff, .worktreeinclude, Codex 并行任务]
related: []
howto: true
faq:
  - q: 没有 Git 仓库能用 Worktree 吗？
    a: 不能。官方说明 Worktree 只适用于已纳入 Git 的项目，底层就是 Git worktree。没有版本控制时，定时任务会直接在项目目录跑，也不会给你单独的后台 worktree。
  - q: Handoff 之后，被 .gitignore 忽略的文件会一起过来吗？
    a: 默认不会。Handoff 走 Git 操作；忽略文件要进托管 worktree，需在仓库根放 .worktreeinclude 列出路径或 .gitignore 风格模式。被忽略的 AGENTS.override.md 会由 Codex 自动拷进本地托管 worktree，不必写入该文件。
  - q: 为什么在 worktree 建了分支，本地却 checkout 失败？
    a: Git 同一时刻只允许一个 checkout 占用同一分支。worktree 上若已 checkout 该分支，本地再切会报 already used by worktree。打算在 Local 继续时，用 Hand off 把聊天交回 Local，而不是两边同时 checkout 同一分支。
---

# Codex Worktree 教程：用 Git worktree 并行跑多个任务，并把结果交回本地（Handoff）

> 本文计划路径：[codexguide.io/guides/codex-worktree-parallel-chats](https://codexguide.io/guides/codex-worktree-parallel-chats)

> 核对依据：learn.chatgpt.com / developers.openai.com 的 Worktrees、Local environments、Troubleshooting，以及 Developer commands／Slash commands 中与 worktree 相关的条目。文中「我的用法」是工作流建议，不是官方规定。

你已经在 Local 里改到一半：测试服务器占着端口，编辑器停在当前分支。这时又想让 Codex 另开一条线——修旁路 bug、试重构、跑长一点的清理——如果全挤在同一个工作副本里，文件会互相覆盖，分支也会缠在一起。

**Worktree 要解决的就是这件事：** 在同一 Git 项目里，给 Codex 再开一份独立 checkout，让多条聊天并行，而不去搅乱你正在用的 Local。做完后，可以用 **Handoff** 把聊天和代码安全交回 Local，也可以在 worktree 上建分支、推远程、开 PR。

本文按官方文档写清：怎么开、怎么交回、忽略文件怎么带上、磁盘和清理怎么管。截图非必须；界面文案以你当前桌面端为准。

## 三个词先对齐

官方术语可以记成：

| 词 | 含义 |
|---|---|
| **Local checkout（Local）** | 你平时打开的那份仓库；桌面端里常直接叫 Local。 |
| **Worktree** | 从这份 Local 创建出来的 **Git worktree**（另一份工作目录）。 |
| **Handoff** | 在 Local 与 Worktree 之间搬聊天的流程；Codex 负责所需的 Git 操作，让工作能安全换到另一份 checkout。 |

Git 层面：每个 worktree 有自己的文件副本，但共享同一套 `.git` 元数据（提交、分支等），所以才能并行 checkout 不同分支／状态。

**前提：** 项目必须是 Git 仓库。非 Git 项目没有这套 Worktree 流程；官方也写明：无版本控制时，定时任务会直接在项目目录跑。

**入口范围：** 桌面端 ChatGPT App 里的 Codex 是主战场（选择 Worktree、Hand off、Create branch here 等）。手机上的 ChatGPT／Codex **不会在手机本地跑 worktree**；它控制的是已连接电脑（或该电脑上的远程开发环境）里的仓库与 worktree。下面桌面端步骤，发生在那台电脑上。

CLI 也有托管 worktree（`/worktree`、`codex … --worktree`），文末单独一节；**Handoff 的完整 UI 路径以桌面端文档为准。**

## 什么时候该用 Worktree

官方给出的动机可以落成三条日常判断：

1. **不想动当前 Local**——前台还在跑服务、还开着未提交改动，后台另开一条 Codex 聊天。
2. **要排队后台活**——你盯着主任务，旁路修 bug、扫测试、试方案可以丢到 worktree。
3. **先做完再交回前台**——在 worktree 里改到可看，再用 Handoff 拉回 Local，用你习惯的 IDE／唯一能起的那套本地环境验收。

**我的用法（建议，非官方强制）：**

- 需要**改文件**的并行任务 → 优先 Worktree（或 CLI `--worktree`），不要靠「多开几个聊天都写同一份目录」。
- 只要**只读分析**、且你愿意严格不让它写盘 → 有时 Local 旁开只读会话就够；一旦可能写文件，仍隔离更稳。
- 同一端口、同一数据库、同一「只能起一份」的桌面 App → 后台用 worktree 写代码，验收时再 Handoff 回 Local。

定时任务（Scheduled tasks）：在 **Git 仓库**里，官方会让它们跑在**专用后台 worktree**，避免和你手头工作冲突；非 Git 项目则仍在项目目录直接跑。细节留给定时任务专文，这里只记「Worktree 也是自动化隔离的底座」。

## 桌面端：从零开一条 Worktree 聊天

确认当前选中的是 **Codex**，并且项目目录在 Git 仓库内。

1. **选 Worktree**  
   在新聊天视图里，composer 下方／附近选择 **Worktree**（不要停在只会写进 Local 的模式）。  
   可选：再选一个 **local environment**，让创建 worktree 时自动跑 setup 脚本（装依赖、构建等）。本地环境只在桌面端 Codex 配置；配置落在项目根的 `.codex` 目录，可提交进仓库给同事共用。

2. **选起始分支**  
   在 composer 下方选基于哪条 Git 分支创建 worktree：`main`／`master`、功能分支，或**带有未暂存本地改动的当前分支**。  
   官方行为：起始提交是所选分支的 `HEAD`；若你选了带本地改动的分支，Codex **也会把未提交改动应用到**新 worktree。

3. **提交提示词**  
   发送后，Codex 按所选分支创建 Git worktree。默认处在 **detached HEAD**（游离 HEAD），不会立刻污染你的分支列表——这样可以同时开多个 worktree。

4. **决定之后在哪继续**  
   - 继续留在 worktree 上改、测、开分支；或  
   - 用 **Hand off** 把聊天（以及代码侧所需 Git 状态）交到 Local。

托管 worktree 的默认目录在 **`$CODEX_HOME/worktrees`**。若要改位置：桌面端 **Settings → Worktrees**，改 **Worktree root**。

## 两条路：留在 Worktree，或 Handoff 回 Local

可以把 Local 想成**前台**，Worktree 想成**后台**。Handoff 就是在两者之间搬聊天。

底层约束（官方反复强调）：**同一分支同一时刻只能在一个 worktree／checkout 上被 checkout。** 若分支已在 worktree 上 checkout，就不能同时在 Local 再 checkout 它，反之亦然。Handoff 正是为了安全完成这套 Git 切换。

### 路线 A：一直在 Worktree 上做完

适合：依赖和工具已经能在 worktree 里跑通（例如靠 local environment 的 setup 脚本装好了），你可以直接在这份目录里验证。

1. 在聊天标题栏用 **Create branch here**，把当前 worktree 从 detached HEAD 收成真正分支（界面里常见前缀如 `codex/`，可改）。  
2. 在 worktree 上提交、推远程、开 GitHub PR。  
3. 用标题栏 **Open** 用 IDE 打开该 worktree 目录，或用集成终端在该目录操作。

记住：一旦在 worktree 上 checkout 了某分支，**Local 和其他 worktree 就不能再 checkout 同一分支**。若你其实打算马上在 Local 看同一分支，不要硬在两边同时切——改走 Handoff。

### 路线 B：Hand off 到 Local（交回前台）

适合：想在**日常 IDE 窗口**里读 diff、只想起**一份**开发服务器、或验证环境只配在 Local。

1. 在聊天标题栏选 **Hand off**，目标选 **Local**。  
2. Codex 执行把聊天安全迁到 Local checkout 所需的 Git 步骤。  
3. 之后在 Local 继续同一条聊天。

也可以反向：人在 Local 做到一半，想把前台腾出来，就 **Hand off → Worktree**，让 Codex 在后台接着改，你回到 Local 干别的。

**关联关系：** 每条聊天会长期关联**同一个** worktree。你之后再 Hand off 回 Worktree，Codex 会回到**那同一个**后台环境，而不是随便新建一个。

**我的用法：** Hand off 完成后，看一眼环境／侧栏是否已显示 **Local**（或 Worktree），再发下一条会改文件的指令。把「界面提示」和「实际写入目录」对上，再继续大改。

## 忽略文件：`.worktreeinclude` 与自动拷贝

托管 worktree 从 Git checkout 起步，**已跟踪文件**本来就在。但很多本地必需文件在 `.gitignore` 里（`.env`、密钥、本机覆盖配置）。

Handoff／创建托管 worktree 时：**被 ignore 的文件默认不会跟着走**，除非你用 `.worktreeinclude` 让 Codex 在创建**本地托管 worktree** 时拷贝它们。

在**仓库根**新增 `.worktreeinclude`，列出忽略路径或 `.gitignore` 风格模式，例如：

```text
# .worktreeinclude
.env
.env.local
config/secrets.json
```

要点（官方原文约束）：

- **只拷贝「被 ignore 且匹配列表」的文件**；不会把其他未跟踪本地文件一并拷走。  
- **不要**把已跟踪文件写进这个列表。  
- 跳过源端符号链接；目标里已存在的文件**不会覆盖**。  
- 被 ignore 的 **`AGENTS.override.md`** 会**自动**拷进本地托管 worktree，不必写进 `.worktreeinclude`。  
- 该拷贝行为适用于 **ChatGPT 桌面端本地托管 worktree**；**不适用于**远程 worktree，也不适用于你自己在命令行 `git worktree add` 建出来的目录。

Worktree 里代码跑不起来时，官方排障顺序也是同一套：用 **local environment** 跑 setup，或用 `.worktreeinclude` 带上忽略的配置；或者把改动 Handoff／checkout 回你日常的 Local 再跑。

Local environment 的 setup 示例（TypeScript）：

```bash
npm install
npm run build
```

可按 macOS／Windows／Linux 分别覆盖默认脚本。配置放在项目根 `.codex`；单体仓库有多个子项目时，打开**含有这份 `.codex` 的那个项目目录**，否则桌面端可能读不到同事共享的环境。

## 托管 worktree 与永久 worktree

| 类型 | 特点 |
|---|---|
| **Codex-managed（默认）** | 轻量、可丢弃；通常**一条聊天对应一个**；以后 Hand off 回 Worktree 仍回到它。 |
| **Permanent（永久）** | 在侧栏项目上的 **⋯** 菜单创建；会变成**自己的项目条目**；**不会**因归档聊天等规则被自动删掉；可在同一永久 worktree 上开多条聊天。 |

## 清理与磁盘

每个 worktree 自带文件、依赖、构建缓存，磁盘很容易涨。桌面端默认**保留最近 15 个** Codex-managed worktree；可在设置里改上限，或关掉自动删除、改手管。

**不会被自动删**的托管 worktree：

- 钉住（pinned）的聊天还绑着它  
- 聊天仍在进行中  
- 它是永久 worktree  

**会被自动删**的情况包括：

- 你**归档**了关联聊天  
- 数量触及你配置的上限，需要清掉更旧的托管 worktree  

删除托管 worktree **之前**，Codex 会先保存一份工作快照。若以后再打开已删 worktree 关联的聊天，界面会提供**恢复**选项。

聊天记录可以仍在历史里，即使目录已被删；永久 worktree **不会**因为你归档聊天就被自动删掉。

磁盘被 worktree／崩溃转储撑满的专门排障，见计划中的姊妹篇（知识库路径 `15-故障排查与常见问题/02-Codex桌面端占满磁盘-Crashpad崩溃转储排查与清理.md`）。清理前先分清「可自动回收的托管 worktree」和「永久 worktree／仍在进行的任务」。

## 分支占用报错时怎么处理

若在 worktree 上用 Create branch here 建了例如 `feature/a`，再想在 Local `git checkout feature/a`，Git 可能报：

```text
fatal: 'feature/a' is already used by worktree at '<WORKTREE_PATH>'
```

处理思路：

1. **打算在 Local 继续同一条线** → 用 **Hand off → Local**，让 Codex 搬聊天并处理 checkout，而不是强行两边同分支。  
2. **必须留在 worktree** → 先让 worktree 改 checkout 到**别的分支**（或回到 detached），释放 `feature/a`，再在 Local 切换。

这是 Git 的「一分支一工作树」规则，不是 Codex 单独发明的限制。

## CLI：托管 worktree 怎么开（补充）

桌面端 Handoff 是并行＋交回的主叙事；CLI 文档里也有托管 worktree，便于终端党并行：

- 交互里：在本地 Git 仓库输入 **`/worktree`**，选择新开聊天或把**当前对话**继续到新 worktree；也可 Browse worktrees 查看已有 worktree 与所属聊天。任务进行中不可用；需要本地 worktree 支持。  
- 启动／脚本：`codex`／`codex fork <SESSION_ID>`／`codex exec`／`codex exec fork` 可加 **`--worktree`**，在新的托管 Git worktree 里跑。要求**本地执行**；不要与 `resume`、`review`、`--ephemeral`、`--ignore-user-config` 组合。  
- 相关：`/fork`、`/new` 在部分流程里也会让你选当前目录或新 worktree。

CLI 与桌面端共用「托管 worktree」概念，但 **Hand off 按钮、Create branch here、Settings → Worktrees** 等以桌面端为准。需要图形化交回 Local 时，可在 macOS／Windows 用文档中的方式把会话续到桌面端 App（例如 CLI 的 `/app`，以你当前版本帮助为准）。

## 我的用法：一条可复用的并行清单

1. 主线留在 **Local**；并行且要写盘的任务开 **Worktree**。  
2. 仓库根维护 `.worktreeinclude`（环境文件）＋ `.codex` 里的 setup（`npm install` 等）。  
3. 后台跑完：能在 worktree 验证 → Create branch here → push／PR；必须用日常环境验证 → **Hand off → Local**。  
4. 定期看 Settings → Worktrees：上限、根目录；长期不用的聊天归档，让托管 worktree 按规则回收。  
5. 永久 worktree 只留给「长期工位」；日常试探用默认托管，少用手建一堆裸 `git worktree`。

## 小结

- **Worktree = 同一仓库的另一份 Git checkout**，用来并行 Codex 聊天，保护 Local。  
- **Handoff** 在 Local ↔ Worktree 之间搬聊天，并处理「一分支不能双 checkout」。  
- **`.worktreeinclude` + local environment setup** 解决「忽略文件／依赖不在新目录」；`AGENTS.override.md`（被 ignore 时）会自动拷贝。  
- 默认托管 worktree 可回收（默认近 15 个）；永久 worktree 与进行中／钉住的聊天更安全。  
- 手机不本地跑 worktree；CLI 用 `/worktree` 与 `--worktree` 做托管隔离，交回前台优先走桌面端 Handoff。

参考：

- [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)  
- [Local environments](https://learn.chatgpt.com/docs/environments/local-environment)  
- [Troubleshooting（Code doesn't run on a worktree）](https://learn.chatgpt.com/docs/reference/troubleshooting)  
- [Developer commands／Slash：`/worktree`、`--worktree`](https://learn.chatgpt.com/docs/developer-commands)
