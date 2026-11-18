---
id: codex-stop-that-shit
title: Codex 安装 Stop That Shit（别再造史了）：用 Skill 和 Hook 拦住 Codex 的范围膨胀、无用防御和越权修改
seo_title: Codex 安装 Stop That Shit：Skill 与 Hook 拦住范围膨胀
description: Stop That Shit 是一个 MIT 许可的 Codex 插件，用 Skill 和 Hook 约束 Codex 不要范围膨胀、不加没用的防御代码、只读审查时不改文件。本文按官方 README 说明怎么固定版本安装、怎么在 /hooks 里审核信任、怎么用 $stss 命令，以及哪些效果数据只是作者自己的说法。
lede: 用 --ref 把插件固定在 0.2.5。装完先读 Hook 要执行的命令，再在 /hooks 里决定信不信任。效果数据按作者的测试条件读。
url: /guides/codex-stop-that-shit-skill-hooks
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 25
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-17
date_modified: 2026-11-17
verified_on: 2026-11-17
tested_cli_version: 0.169.0
official_ref: https://github.com/lennney/stop-that-shit
keywords: [Codex Stop That Shit, Codex Hook 拦截, 范围膨胀, $stss, codex plugin marketplace add --ref]
related: [hooks-guide, codex-plugin-hook-audit]
howto: true
faq:
  - q: 这是 OpenAI 官方插件吗？
    a: 不是。它是 lennney/stop-that-shit，MIT 许可，README 为中文。用 --ref 0.2.5 安装的是 2026-10-15 发布的正式版，不是跟随 main 的浮动版本。
  - q: README 里的 $stss review 存在吗？
    a: 2026-11-17 的 README 没有 $stss review。主 Skill 叫 stop-that-shit，Codex 里写 $stop-that-shit review。$stss 是另一份「别再废话」Skill，文档里的 Codex 用法是 $stss rewrite 和 $stss audit。
  - q: 作者的对照测试能当成省 token 的证据吗？
    a: 不能。EVIDENCE.md 自己写了哪些运行只是诊断、哪些是空效果，并写明不要用单元测试或单次场景发布改进百分比。本文没有复跑这些测试。
  - q: /hooks 的信任界面测过吗？
    a: 没有。安装、列出、核对 hooks/codex-hooks.json 和卸载是在未登录的 Codex CLI 0.169.0 上做的。TUI 里的 /hooks 需要交互，本文未实测。
---

# Codex 安装 Stop That Shit（别再造史了）：用 Skill 和 Hook 拦住 Codex 的范围膨胀、无用防御和越权修改

> 本文在线版：[codexguide.io/guides/codex-stop-that-shit-skill-hooks](https://codexguide.io/guides/codex-stop-that-shit-skill-hooks)

> 核对依据：第三方仓库 [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit) 在 2026-11-17 的中文 README，以及 tag 0.2.5 的 [INSTALL.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/INSTALL.md)、[INSTALL_FOR_AGENTS.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/INSTALL_FOR_AGENTS.md)、[EVIDENCE.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/EVIDENCE.md)、[skills/stop-that-shit/SKILL.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/skills/stop-that-shit/SKILL.md) 和装下来的 `hooks/codex-hooks.json`。GitHub API 当天返回 3,942 star、82 fork，MIT，未归档，`pushed_at` 为 2026-11-16T06:58:17Z。最新正式版是 [0.2.5](https://github.com/lennney/stop-that-shit/releases/tag/0.2.5)，发布于 2026-10-15T12:31:31Z。实测是 Linux，Node.js v22.23.4，`codex-cli 0.169.0`，独立 `CODEX_HOME`，**没有登录**。没有配图。

Stop That Shit（别再造史了）是第三方插件。它想让 Codex 把当前任务做完，同时少做没有用途的额外工作和防御性文字。许可证 MIT。它不是 OpenAI 的功能，安装它也不表示 OpenAI 审核过这些 Hook。

装任何第三方 Hook 之前，先读它会执行什么命令。Codex 的信任审核见[《Codex Hooks 入门》](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)，装完后的记录见[《插件与 Hook 自查》](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)。

## 它想解决什么：四类过度行为

README 把这些行为叫做 SHIT，四类是：

| 字母 | 英文 | README 的意思 |
|---|---|---|
| S | Scope creep，范围膨胀 | 修一个问题，顺手重构无关模块。必要的调用方、数据迁移和测试要一起做；没有当前用途的扩展就停下 |
| H | Hashing & hypothetical hardening，无用防御 | 没人读取的 checksum、为想象中的未来搭的兼容层。能发现问题并触发拒绝、恢复或诊断的防御留下；无用的省掉 |
| I | Intent violation，意图越界 | 说了只读 Review，文件还是被改了。审查就报告问题，修改需要授权 |
| T | Task thrashing，任务打转 | 没有新问题或变化，把读过、测过、审过的又做一遍。证据够回答当前问题就复用；代码或验收条件变了再补 |

README 同时写：**把当前责任承担完整。** 需要多改几个文件、补迁移或跑跨组件测试，就做完整。它用一段导出 `report.csv` 又写 `.sha256` 的例子说明：下游不读校验和时，按它的判断只留下写 csv 的那一行；发布流程会读校验和并在不一致时拒绝使用，就用 `hash=allow` 放行。

一般宿主需要 Node.js 18+。README 写 Pi 0.84.4 自己要求 Node.js 22.19+；Codex 这条安装路径按 18+。本文的 Node 是 v22.23.4。

## 在 Codex 里安装：固定 --ref 版本、重启、/hooks 审核信任

README 和 INSTALL.md 给 Codex 的命令是：

```bash
codex plugin marketplace add lennney/stop-that-shit --ref 0.2.5
codex plugin add stop-that-shit@stop-that-shit
```

`--ref` 把来源固定到 tag 0.2.5，不跟随可变的 `main`。仓库在 2026-11-16 还有推送，最新正式版仍是 0.2.5。要装作者指定的这一版，就保留 `--ref 0.2.5`。

0.169.0 的 `codex plugin marketplace add --help` 确认有 `--ref <REF>`，说明是 “Git ref to fetch for Git marketplace sources”。

然后**重启 Codex**。在新的 CLI TUI 里输入 `/hooks`，对照 [INSTALL.md 的 Hook 清单](https://github.com/lennney/stop-that-shit/blob/0.2.5/INSTALL.md#review-the-packaged-hooks) 检查并信任命令。INSTALL.md 写：Codex 按 Hook 定义的哈希记录信任；有的桌面端会把 `/hooks` 当成普通消息，那时改在 CLI TUI 里完成审核，再重启桌面端。更新后定义变了，可能要再审一次。原文还有一句：Do not bypass Hook trust for ordinary installation。0.169.0 的 `codex --help` 里能看到 `--dangerously-bypass-hook-trust`。普通安装不要用它，本文也不写它的用法。

也可以把 [INSTALL_FOR_AGENTS.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/INSTALL_FOR_AGENTS.md) 交给 Codex，让它做非交互步骤。信任仍然要你自己在 `/hooks` 里确认。官方说明在 [Review and trust hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks)。

2026-11-17 的未登录安装输出是：

```text
Added marketplace `stop-that-shit` from https://github.com/lennney/stop-that-shit.git#0.2.5.
Added plugin `stop-that-shit` from marketplace `stop-that-shit`.
```

`codex plugin list`：

```text
PLUGIN                         STATUS              VERSION  SOURCE
stop-that-shit@stop-that-shit  installed, enabled  0.2.5    <本次的 marketplace 目录>
```

`codex login status` 为 `Not logged in`。`codex mcp list` 为 `No MCP servers configured yet`。插件缓存目录以 `plugins/cache/stop-that-shit/stop-that-shit/0.2.5` 结尾。

**未实测** `/hooks` 的 TUI 信任界面。没有账号，也没有交互会话。

## 装好后怎么确认：插件列表与 Hook 清单

上面的 `plugin list` 只能说明插件装上了，不能说明你已经信任 Hook。

INSTALL.md 写当前 tag 的 Codex 条目覆盖：

- `UserPromptSubmit`：读取任务模式和显式边界
- `PreToolUse`：在支持的动作运行前检查
- `PostToolUse`：读取支持的委托结果
- `SessionEnd`：不能证明还没结束的子任务已经完成

它写明这个 tag **不**为 Codex 注册 `Stop`、`SubagentStart`、`SubagentStop`，也不会在一轮结束后自动续跑。

本次装到的 `hooks/codex-hooks.json` 和 tag 0.2.5 上的文件一致，四个事件是：

| 事件 | matcher | timeout | 命令在做什么 |
|---|---|---|---|
| UserPromptSubmit | 无 | 5 秒 | `node -e`，加载 `PLUGIN_ROOT` 或 `CLAUDE_PLUGIN_ROOT` 下的 `hooks/stop-that-shit.cjs` |
| PostToolUse | `spawn_agent`、`Agent`、`wait_agent` 等一组委托工具名 | 5 秒 | 同上 |
| PreToolUse | `*` | 5 秒 | 同上，`statusMessage` 为 “Checking the Stop Ladder...” |
| SessionEnd | `*` | 3 秒 | 同上 |

四条命令都是用 Node 加载插件自带的 `hooks/stop-that-shit.cjs`，不是一条写死的业务 shell。信任前仍应打开这个 cjs，看它在拒绝、放行时做什么。INSTALL.md 还要求看 `src/adapters/` 和 `src/`。其他插件也会往 `/hooks` 里加行，所以对来源，不对着总行数点头。

`.codex-plugin/plugin.json` 的 `hooks` 字段指向 `./hooks/codex-hooks.json`，`skills` 指向 `./skills/`。里面有两份 Skill：`stop-that-shit` 和 `stss`。

## 怎么用：$stop-that-shit 和 $stss

2026-11-17 的 README **没有** `$stss review`。两份 Skill 的名字不同。

主 Skill 的 Codex 写法是把指令放在消息**第一个非空行**，不要包在引用或代码块里，用 `--` 隔开任务正文：

```text
$stop-that-shit review -- Review 这个 diff，只报告问题，不要修改。
$stop-that-shit change -- 修复配置读取失败，补齐受影响的调用方和检查。
```

README 的指令表还有 `answer`（回答问题）、`monitor`（持续检查和报告）、`watch`（只观察，不阻断）、`status` / `runtime`（看当前状态和本地记录）。需要收紧边界时可以加参数，例如 `files=`、`deps=allow`、`hash=allow`、`agents=1`。还没查清受影响的文件时，README 说先别锁 `files=`。

`$stss` 是另一份 Skill，README 叫 Stop That Shit Slop（别再废话）。它改的是防御性措辞，不负责拦截写文件。Codex 的两句是：

```text
$stss rewrite -- 把这个提案写直接。
$stss audit -- 找出防御性废话。
```

`rewrite` 改写，`audit` 只报告问题和最小修改建议。完整插件里包含它；也可以单独安装、不带 Hook。单独安装的命令在 README 里是 `npx skills add ./skills/stss --global`，那是在仓库根目录执行的。

INSTALL.md 的 Codex 冒烟测试是：在一次性仓库里先发 `$stop-that-shit review -- ...`，被覆盖的写入应被拒绝；再发 `$stop-that-shit change -- ...` 创建指定文件。作者写这只检查安装和合同切换，**不证明模型行为普遍变好**。本文没有跑这个冒烟测试。

刚装上时默认是 `OBSERVING / unconfirmed`。显式用过 `review`、`answer`、`monitor` 或 `change` 之后，Guard 才进入 `ARMED`。`watch` 始终只观察。只装 Skill、不装 Hook，就没有执行拦截。

## 它拦什么、不拦什么：Skill 与 Guard 的分工

README 写：Skill 负责工程判断；Guard 在受支持的工具调用前检查明确边界。Guard 启用后的默认处理是：

| 动作 | 默认 |
|---|---|
| 在 `review`、`answer` 或 `monitor` 里写文件 | 停止 |
| 添加依赖 | 询问；`deps=allow` 放行 |
| 启动 subagent | 超出 `agents=N` 时停止 |
| 添加可识别的 hash 操作 | 停止；`hash=allow` 放行 |
| 写入 `files=` 之外的路径 | 停止 |

README 写 Guard **不会**看见 `cache`、`retry` 或 `migration` 就断定它们多余。红章 `permission_deny_returned` 表示 Guard 返回了拒绝；宿主最后有没有执行，要另外观察，Runtime 把 `hostEffect` 记为 `unobserved`。安全隔离仍由 Codex 的沙箱负责。

SKILL.md 的 description 写它在考虑额外加固、审查过度设计、处理重复验证、遵守明确边界，或用户点名 Stop That Shit 时使用；单独出现校验、重试或依赖，不足以触发。

## 和 AGENTS.md 规则、Codex 自带审批怎么配合

README 的作者说，自己试过在 `AGENTS.md` 里不断补「不要乱改」「别过度设计」，结果规则文件自己也膨胀了。这个插件是另一层：Skill 给判断顺序，Hook 在一部分工具调用前做明确边界。

它不替换 Codex 的审批和沙箱。EVIDENCE.md 记录过一次：只读配置下 Codex 拒绝了编辑和测试命令；换成 workspace-write 并自动批准后才通过。作者据此写 Skill 不能覆盖宿主的沙箱和审批策略。那是作者的记录，不是本文的复测。

项目里该怎么写 `AGENTS.md`，仍按仓库自己的规则。一次审查要看正确性、安全和测试，见[《如何做一次高质量 Code Review》](../05-Git协作与代码审查/06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md)。这个插件的 `review` 只是加上「报告问题、不要改文件」的合同，不代替那篇里的审查清单。

## 作者的对照测试：怎么读，哪些只能写成「作者称」

下面全部是作者在 EVIDENCE.md 和 0.2.5 发布说明里的话，**不是本文的实测**。

作者称，0.2.5 在 Windows x64、Node 24.14.1 上：609 个源码测试通过、0 失败、3 个可选宿主检查跳过；22/22 离线成对用例通过。发布说明写这些宿主检查用的是本地工具或确定的本地响应，**没有调用外部模型 API**，也不能证明模型普遍更有效，也不能证明从 Git 安装一定成功。附件解析仍未证明。

作者称，截至 2026-08-14，自己在本地用过之后没有再看见无用的 SHA-256。EVIDENCE 把这句标成个人观察，不是对照实验，也不是对模型的普遍结论。

作者还写下了不能当成效果的运行，例如 2026-08-13 用 Codex CLI 0.147.0、`gpt-5.6-luna`、medium、workspace-write、approval never 做的四格试验：baseline 已经保持只读审查，插件没有在任务层面上更好；Good 用例两边都完成了授权编辑。作者的结论是没有效果提升，也没有 Good Case 退步。另一段运行因为插件缓存过期被排除。EVIDENCE 的 Claim rule 写明：不要声称它解决了各编程代理的过度设计，也不要从单元测试或单次场景公布改进百分比。

本文没有找到可以引用的、带条件和对照组的「省了多少 token」数字。README 里「token 已经花了一截」是在描述任务跑偏时的体验，不是测量结果。因此这里不写省 token 的比例。

## 升级与卸载

作者要求 Codex 使用固定 tag。升级不是改去跟踪 `main`。换到新 tag 后，按那一版的 INSTALL 重新添加，重启，并在 `/hooks` 里重新审核变化了的 Hook。INSTALL 写 “Checking a version is not an update”。本文没有升级到 0.2.5 以外的版本。

立刻停用 Guard：在 `/hooks` 里禁用。然后：

```bash
codex plugin remove stop-that-shit@stop-that-shit
codex plugin marketplace remove stop-that-shit
```

2026-11-17 在同一个未登录的 `CODEX_HOME` 里执行了这两句，退出码都是 0。随后 `codex plugin list` 输出 `No marketplace plugins found.` 这只证明卸载命令在未登录时可以跑完，不证明已登录桌面端里的信任记录会一起消失。

INSTALL 写 Guard 的会话合同和运行时元数据在宿主提供的数据目录（Codex 为 `PLUGIN_DATA`）。卸载后要不要删那份数据，先看 [PRIVACY.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/PRIVACY.md)。只装了 Skill 时，作者写默认目录是 `$HOME/.codex/skills/stop-that-shit`（若设置了 `CODEX_HOME`，则在其下的 `skills/stop-that-shit`）。删之前先确认路径。本文没有在已登录配置里找到这份运行时数据。

## 常见问题与参考资料

**只想要规则，不想要 Hook？** INSTALL 写可以用内置 Skill Installer，指向 tag 0.2.5 的 `skills/stop-that-shit`。那样没有执行拦截。

**红章是不是绝对没执行？** README 写不是。拒绝响应和宿主是否真的没跑，要分开看。

**会保存代码和对话吗？** README 写 Runtime 事件不保存代码或对话正文；会话状态另存显式路径、关联 ID 和指令错误等控制信息。分享插件数据前先检查会话状态。

参考资料：

- [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit)（MIT，2026-11-17 查询 3,942 star）
- [Release 0.2.5](https://github.com/lennney/stop-that-shit/releases/tag/0.2.5)（2026-10-15）
- [INSTALL.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/INSTALL.md)
- [EVIDENCE.md](https://github.com/lennney/stop-that-shit/blob/0.2.5/EVIDENCE.md)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Codex plugins](https://learn.chatgpt.com/docs/plugins)
