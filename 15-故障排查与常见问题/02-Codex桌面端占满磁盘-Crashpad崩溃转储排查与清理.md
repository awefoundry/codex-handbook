---
id: desktop-crashpad-disk-space
title: Codex 桌面端占满磁盘怎么办：排查 Crashpad 崩溃转储，并安全清理 worktree 与会话数据（macOS）
seo_title: Codex 占满磁盘：Crashpad pending 排查与安全清理（macOS）
description: Mac 磁盘突然被吃掉几十到几百 GB，可能是 Codex 桌面端的 Crashpad 崩溃转储在后台堆积。本文教你用 du 核对 pending 目录、按社区实践安全清理，并顺带检查 worktree、会话与日志占用；说明官方尚未发布 Crashpad 清理指南。
lede: 应用还能用，磁盘却越来越满时，先量 Crashpad pending，再动刀——而且只动转储，不动整棵应用目录。
url: /guides/codex-desktop-crashpad-disk-space
status: published
section: guides
category: K-troubleshooting
topic: 故障排查与恢复
content_type: 排障
source_tag: 官方功能
entry_tags: [App]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/reference/troubleshooting
keywords: [Codex 占用磁盘, Codex Crashpad, Crashpad pending, Codex 桌面端磁盘空间, Codex worktree 清理]
related: [worktree-parallel-chats, model-at-capacity-usage-reset, cli-manage-multiple-sessions]
faq:
  - q: OpenAI 有没有官方的 Crashpad 清理文档？
    a: 截至本文撰写时没有。官方 Troubleshooting 给出了日志、会话与归档会话路径，以及「定时任务会产生大量 worktree」的提醒，但未单独说明 Crashpad pending。文中清理步骤来自 GitHub issue 社区讨论，须按安全规则操作，并在本机验证后再当作日常流程。
  - q: 能不能直接把整个 Application Support/Codex 目录删掉？
    a: 不建议。那会连带清掉本地配置、缓存与其他应用数据。更窄的做法是先退出应用，只处理 Crashpad 下的 pending（必要时再看 new／completed／attachments），然后重启观察是否继续增长。
  - q: 把 pending 目录改成只读能当长期方案吗？
    a: 只能当紧急刹车。社区里有人用 chmod 阻止继续写入，但这也会挡住真正的崩溃报告，且不是官方建议。优先：退出应用 → 清理 pending → 升级系统／应用 → 向官方反馈；若必须只读，事后要记得改回可写。
---

# Codex 桌面端占满磁盘怎么办：排查 Crashpad 崩溃转储，并安全清理 worktree 与会话数据（macOS）

> 本文在线版：[codexguide.io/guides/codex-desktop-crashpad-disk-space](https://codexguide.io/guides/codex-desktop-crashpad-disk-space)

> 核对依据：learn.chatgpt.com 的 Troubleshooting、Worktrees；openai/codex 上与 Crashpad 相关的 **issue 讨论**（#25921、#36982、#51361 等，标为社区报告，不是官方清理手册）。文中「我的用法」是排查顺序建议，不是官方规定。**OpenAI 尚未发布正式的 Crashpad 清理指南**；下列清理步骤均按社区实践整理，并加上安全边界。

Mac 系统提示存储空间不足，或可用空间一夜之间从几十 GB 掉到只剩一两 GB，但 **Codex／ChatGPT 桌面端看起来还能正常聊天**——这种反差很容易让人以为是「系统缓存」或「Time Machine」，最后才在 `~/Library/Application Support` 里发现成百上千 GB 的 Crashpad 转储。

社区在 [openai/codex#25921](https://github.com/openai/codex/issues/25921) 里多次报告：`Crashpad/pending` 里成对堆积 `.dmp` 与 `_sidecar.json`，应用本身往往仍可用；有人测到一天数 GB，也有人两套目录合计约 **323 GB、约 404 万个文件**，占近 TB 级磁盘的三分之一，且应用没有明显警告。这些数字来自 **issue 评论快照**，不是官方 SLA，用来建立「量级感」即可。

本文只解决三件事：

1. **先确认是不是 Crashpad pending**（以及新旧两套路径）。
2. **按更窄、可回退的方式清理**，避免「整棵目录 chmod 只读」或「删光整个应用数据」当默认操作。
3. **顺带核对**官方文档里点名的日志、会话、归档会话，以及会涨磁盘的 **托管 worktree**（默认保留最近 15 个）。

## 症状：能用，但磁盘越来越满

典型信号（社区描述，非官方诊断标准）：

- 系统设置 → 通用 → 储存空间里，「文稿」或「其他」突然很大；用 `du` 才定位到 `Application Support` 下的 `Crashpad`。
- Codex／统一 ChatGPT 桌面端仍能开窗、发消息；问题更像**后台转储失控**，而不是前台完全崩掉起不来。
- `pending` 里文件数可达数十万到数百万；单文件往往不大（约一百多 KB 量级的 dump 很常见），靠**数量**把磁盘撑满。
- 清理后若根因还在，pending 可能很快又开始涨——所以「删一次」不等于「治好了」。

先别急着清系统缓存或重装整个 App。**先量路径、再决定动哪一层。**

## 先确认是不是它：量两个 Crashpad 目录

历史上社区至少见到过两套应用数据路径（版本迁移／统一桌面端后可能并存）：

| 路径 | 常见叫法 |
|---|---|
| `~/Library/Application Support/com.openai.codex/web/Crashpad` | 偏旧的 `com.openai.codex` 数据根 |
| `~/Library/Application Support/Codex/Crashpad` | 较新的 `Codex` 数据根 |

真正吃磁盘的往往是各自下面的 **`pending`**。在「终端」里（把路径原样粘贴；含空格的目录名要加引号）：

```bash
du -sh \
  "$HOME/Library/Application Support/com.openai.codex/web/Crashpad" \
  "$HOME/Library/Application Support/com.openai.codex/web/Crashpad/pending" \
  "$HOME/Library/Application Support/Codex/Crashpad" \
  "$HOME/Library/Application Support/Codex/Crashpad/pending" \
  2>/dev/null
```

需要文件数量时（目录极大时会慢，属正常）：

```bash
for p in \
  "$HOME/Library/Application Support/com.openai.codex/web/Crashpad/pending" \
  "$HOME/Library/Application Support/Codex/Crashpad/pending"
do
  [ -d "$p" ] || { echo "missing: $p"; continue; }
  echo "== $p =="
  find "$p" -maxdepth 1 -type f 2>/dev/null | wc -l
  find "$p" -maxdepth 1 -type f -name '*.dmp' 2>/dev/null | wc -l
  find "$p" -maxdepth 1 -type f -name '*_sidecar.json' 2>/dev/null | wc -l
done
```

**怎么读结果：**

- `pending` 已经是 **数 GB～数百 GB**，且 `.dmp` 与 `_sidecar.json` 数量接近 → 高度符合本篇讨论的现象。
- 想区分「历史堆积」还是「仍在狂写」：再看最近一两分钟内是否还有新 `.dmp`（例如对 `pending` 做 `-mmin -1` 计数）。持续快速增加，更像活跃循环；只有旧文件、最近不再写入，则更像积压。

官方 Troubleshooting **没有**把 Crashpad 列为条目；它给出的是日志与会话位置（下一节会用到）。因此：**Crashpad 路径与清理动作目前主要来自社区 issue，不是 learn.chatgpt.com 上的逐步手册。**

## 原因（社区结论，非官方根因说明）

综合 [#25921](https://github.com/openai/codex/issues/25921)、[#36982](https://github.com/openai/codex/issues/36982) 等讨论，用户侧反复观察到的模式大致是：

1. 桌面端内嵌的 Chromium／Electron **Crashpad** 会把待上传的崩溃小转储写到 `Crashpad/pending`。
2. 部分环境下，`browser_crashpad_handler` 自己在启动后很快失败（评论里常见 `SIGTRAP`／`mach_port_request_notification` 一类线索），又被反复拉起。
3. 失败被当成新的崩溃 → 再写一对 dump／sidecar → **没有有效上限或清理**时，目录可以线性涨到占满磁盘。
4. 主窗口仍可保持可用，所以用户往往很晚才发现。

另有 [#51361](https://github.com/openai/codex/issues/51361) 一类请求：给 Codex 生成的数据加存储上限与自动清理——说明社区也把「缺上限」当成独立问题，而不只是「某一个崩溃」。

**重要边界：**

- 以上是 **issue 讨论里的复现与推测**，不是 OpenAI 发布的正式故障说明或修复公告。
- 不同 macOS 大版本、不同 ChatGPT／Codex 构建上，是否仍活跃复现，评论并不一致；有人报告升级系统后「自己这边没了」，也有人在较新构建上仍量到巨大 pending。**以你本机 `du` 与是否仍在增长为准。**
- 不要把 HN 标题或第三方博客当成产品真相；它们最多用来对照「有没有人遇到过」。

## 安全清理（社区实践 + 必须遵守的边界）

**再次强调：OpenAI 没有发布官方 Crashpad 清理指南。** 下面步骤整理自 issue 评论中较稳妥的做法，并收紧了安全规则。请在本机验证；本预览环境没有 macOS，无法代你实测。

### 推荐顺序

1. **完全退出** Codex／ChatGPT 桌面端（菜单退出，而不只是关窗口）。必要时在「活动监视器」里确认没有残留的 `browser_crashpad_handler` 仍在写盘。
2. **只动 Crashpad 报告桶**，优先 `pending`；若你清楚自己在做什么，社区也会提到 `new`／`completed`／`attachments` 同属转储相关桶。  
   - 更稳妥：把文件**移到废纸篓**（或移到桌面一个临时文件夹），而不是立刻 `rm -rf` 数百万小文件——移动改名通常更快，也方便后悔。  
   - 不要公开上传 `.dmp`：可能含内存片段、本地路径、会话相关信息。
3. **不要**默认删除整棵：
   - `~/Library/Application Support/Codex`
   - `~/Library/Application Support/com.openai.codex`  
   除非你明确要做「本地全量重置」，并已备份需要的配置。
4. 重新打开应用，再跑一遍上面的 `du`／计数：观察 5～15 分钟，看 `pending` 是否重新快速上涨。
5. 若仍在狂涨：更新到当前最新桌面端；核对本机 macOS 是否过旧；到 [#25921](https://github.com/openai/codex/issues/25921) 等 issue **补充版本号、占用、是否仍增长**（见文末反馈节）。临时止损可以用「定时只清 pending 文件」这类窄脚本；**不要把「整棵目录永久只读」当第一选择。**

### 不建议当「修复」的做法

| 做法 | 为什么不建议当默认 |
|---|---|
| `chmod -R`／`chflags uchg` 作用到**整棵** `Application Support/Codex` 或 `com.openai.codex` | 范围过大，可能影响正常写入与日后升级；社区也有人警告勿把整树锁死 |
| 把只读当成长期「修复」且忘记改回 | 会挡住真实崩溃报告；修好后若忘记解锁，排障信号丢失 |
| 未退出应用就狂删数百万文件 | 可能与仍在写入的 handler 打架；也更难判断「删完是否立刻再生」 |
| 公开贴出 `.dmp` 或完整本地绝对路径含用户名以外的敏感片段 | 隐私风险；issue 作者普遍选择只报元数据 |

若磁盘已经逼近 0、必须立刻止血，社区有人**仅对 `Crashpad/pending` 目录**临时去掉写权限。把它当成**紧急刹车**：记下你改过权限，问题解决或升级后改回可写，并继续走反馈通道。这不是官方推荐，也不是本文的首选步骤。

## 顺带检查：worktree、会话、归档与日志

Crashpad 不是唯一会涨的本地数据。官方 Troubleshooting 写明了这些位置（默认值）：

| 类型 | 默认位置 |
|---|---|
| 应用日志（macOS） | `~/Library/Logs/com.openai.codex/YYYY/MM/DD` |
| 会话记录 | `$CODEX_HOME/sessions`（默认 `~/.codex/sessions`） |
| 归档会话 | `$CODEX_HOME/archived_sessions`（默认 `~/.codex/archived_sessions`） |

快速量一下：

```bash
du -sh \
  "$HOME/Library/Logs/com.openai.codex" \
  "${CODEX_HOME:-$HOME/.codex}/sessions" \
  "${CODEX_HOME:-$HOME/.codex}/archived_sessions" \
  "${CODEX_HOME:-$HOME/.codex}/worktrees" \
  2>/dev/null
```

**Worktree：** 官方 Worktrees 文档写明，每个 worktree 自带文件、依赖、构建缓存，磁盘很容易涨；桌面端默认**保留最近 15 个** Codex 管理的 worktree，可在设置里改上限或改手管。钉住的聊天、进行中的聊天、永久 worktree，不会按同一套「随便删」规则处理。定时任务频繁时，官方也提醒会积累大量 worktree——归档不再需要的定时运行、避免无必要地 pin。

托管 worktree 怎么开、怎么 Handoff、自动清理规则的完整说明，见姊妹篇《[Codex Worktree 教程](../11-自动化与高级工作流/10-Codex用Worktree并行运行多个任务.md)》（知识库 `11-自动化与高级工作流/07-…`，id：`worktree-parallel-chats`）。**本篇只提醒：磁盘告急时，先分清 Crashpad 转储 vs 仍在用的 worktree，不要为了腾空间删掉未交接的工作副本。**

会话／归档体积异常时，优先在客户端里归档或删除**你确认不再需要**的聊天；CLI 多会话命名、恢复与归档见《[Codex CLI 管理多条任务线](../11-自动化与高级工作流/03-CodexCLI管理多条任务线.md)》（id：`cli-manage-multiple-sessions`）。分享日志前，官方要求先检查是否含敏感信息。

额度／容量类「用不了」和「磁盘满了」不是一类问题：前者见《[容量不足与额度重置](./01-Codex模型容量不足与额度重置排查.md)》（id：`model-at-capacity-usage-reset`）。

## 向官方反馈时带什么（不要公开 dump）

官方 Troubleshooting「Feedback and logs」：

1. 在消息输入框输入 `/`，按客户端指引提交反馈；若在已有聊天里触发，可选择是否附带该会话。提交后会得到可分享给团队的会话／反馈标识。
2. 到 [openai/codex](https://github.com/openai/codex) 搜是否已有同类 issue（优先跟帖 [#25921](https://github.com/openai/codex/issues/25921)／[#36982](https://github.com/openai/codex/issues/36982) 等），避免重复开空洞新帖。
3. 公开评论建议只带**元数据**：应用版本与 build、macOS 版本与芯片架构、两个 Crashpad 路径各自 `du` 大小与文件数、oldest／newest 时间戳、清理后是否仍增长。  
4. **不要**把 `.dmp` 直接贴到公开 issue。维护者若提供私密上传通道再按指引处理。

## 一页检查清单

1. `du` 两个 `…/Crashpad` 与各自 `pending`；必要时数 `.dmp`／sidecar。  
2. 确认是历史积压还是仍在写入。  
3. **退出**桌面端 → 只处理 pending（优先移到废纸篓）→ **不要**删整棵 Application Support。  
4. 重启后观察 5～15 分钟；仍狂涨则升级应用／系统，并走 Feedback + issue 元数据跟帖。  
5. 顺带 `du`：`Logs/com.openai.codex`、`~/.codex/sessions`、`archived_sessions`、`worktrees`。  
6. Worktree：看 Settings → Worktrees 上限（默认近 15）；归档无用定时任务与聊天；细节链到 Worktree 专文。  
7. 紧急时才考虑「仅 pending 只读」；事后改回；**永不**把整树只读当正式修复。  
8. 公开反馈不上传 dump。

## 小结

- 桌面端仍可用、磁盘却被吃光时，优先怀疑 **`Crashpad/pending` 无界堆积**；新旧两套 Application Support 路径都要查。  
- **官方尚未给出 Crashpad 专用清理文档**；清理步骤来自社区 issue，核心安全规则是：先退出、只动转储桶、不把整树只读当修复、不公开 dump。  
- 同时用官方路径核对日志、会话、归档与托管 worktree（默认保留最近 15 个）；worktree 管理见姊妹教程。  
- 治本依赖上游修复与合理保留策略；本地清理是止损与取证，不是替代反馈。

参考：

- [Troubleshooting（Feedback and logs；Scheduled tasks create many worktrees）](https://learn.chatgpt.com/docs/reference/troubleshooting)  
- [Worktrees（cleanup：默认保留最近 15 个托管 worktree）](https://learn.chatgpt.com/docs/environments/git-worktrees)  
- 社区讨论（非官方手册）：[openai/codex#25921](https://github.com/openai/codex/issues/25921)、[#36982](https://github.com/openai/codex/issues/36982)、[#51361](https://github.com/openai/codex/issues/51361)
