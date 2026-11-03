---
id: codex-trail-of-bits-patching-bugs
title: Codex 安装 Trail of Bits 安全插件：用 patching-bugs 和 regression-hunt 复现漏洞、写补丁、查回归
seo_title: Codex 安装 Trail of Bits 插件：复现漏洞、写补丁、查回归
description: Trail of Bits 开源了 patching-bugs 和 regression-hunt 两个 Codex 插件，用来复现并确认一个已知问题、写本地补丁、证明补丁有效，再检查补丁有没有带来回归。本文讲 marketplace 安装、运行前准备和怎么读报告。
lede: 这两个插件把“复现、写补丁、证明、查回归”拆成固定步骤。它们不会替你 push，也不会替你开 PR。
url: /guides/codex-trail-of-bits-patching-bugs
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 12
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-03
date_modified: 2026-11-03
verified_on: 2026-11-03
tested_cli_version: 0.166.0
models: [gpt-5.6]
official_ref: https://learn.chatgpt.com/docs/plugins
keywords: [Codex Trail of Bits, patching-bugs, regression-hunt, Codex 插件 marketplace, Codex 安全补丁]
related: [codex-security-cli, plugin-development-marketplace]
faq:
  - q: Trail of Bits 用这两个插件修了 149 个内核 CVE 吗？
    a: 不能这么说。2026-11-02 的回移植博客写的是用 Codex 和 GPT-5.6 做回移植，到 10 月 29 日已经把 149 个不同 CVE 的修复送进稳定版内核。博客没有说这些修复来自 patching-bugs 或 regression-hunt。这两个插件是同一团队更早开源的另一套工具。
  - q: 装上以后它会自己 push 或开 PR 吗？
    a: 不会。patching-bugs 的 README 写明它不会 push，也不会开 PR。implement-patch 这一步可以在本地留下一个提交，提交前仍要人看 diff、测试和报告。
  - q: 必须先写 THREAT_MODEL.md 吗？
    a: 不是安装前提。插件在仓库根目录找到 THREAT_MODEL.md、PATCHING_GUIDELINES.md 或 AGENTS.md 就会读；文件可以不存在。作者建议补上这两份说明，让每一步按项目自己的规则判断。
  - q: 本机 Python 低于 3.13 还能装插件吗？
    a: 可以安装。Python 3.13+ 和 uv 是插件里那些校验、证明和渲染脚本的要求，不是 marketplace 安装命令的要求。Codex 真正调用这些脚本时，机器上要有 Python 3.13 或更高版本，并用 uv run --no-project 运行。
---

# Codex 安装 Trail of Bits 安全插件：用 patching-bugs 和 regression-hunt 复现漏洞、写补丁、查回归

> 本文在线版：[codexguide.io/guides/codex-trail-of-bits-patching-bugs](https://codexguide.io/guides/codex-trail-of-bits-patching-bugs)

> 核对依据：第三方仓库 [trailofbits/skills](https://github.com/trailofbits/skills) 的 README、`.claude-plugin/marketplace.json`、[patching-bugs](https://github.com/trailofbits/skills/tree/main/plugins/patching-bugs) 与 [regression-hunt](https://github.com/trailofbits/skills/tree/main/plugins/regression-hunt) 的 README 和技能说明；Trail of Bits 博客 [Backporting security fixes at scale with Codex](https://blog.trailofbits.com/2026/11/02/backporting-security-fixes-at-scale-with-codex/)（2026-11-02）和 [Your AI agent fixed the bug, but what else did it change?](https://blog.trailofbits.com/2026/10/21/your-ai-agent-fixed-the-bug-but-what-else-did-it-change/)（2026-10-21）；OpenAI 页面 [Patch the Planet](https://openai.com/index/patch-the-planet/)（2026-06-22）。安装命令在 Linux 上的 Codex CLI 0.166.0 实测，使用独立的 `CODEX_HOME`，**没有登录**，也**没有**对真实漏洞跑完整条补丁流程。核对日期 2026-11-03。

已经有一份漏洞报告，接下来要做的是把它复现出来、改到最小范围、证明补丁真的对上了这个问题，再看补丁有没有碰坏别的行为。Trail of Bits 把这套步骤做成了两个 Codex 插件：[patching-bugs](https://github.com/trailofbits/skills/tree/main/plugins/patching-bugs) 和 [regression-hunt](https://github.com/trailofbits/skills/tree/main/plugins/regression-hunt)。

它们是第三方项目，许可证是 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)，由 Trail of Bits 维护。2026-11-03 查询 GitHub API 时，[trailofbits/skills](https://github.com/trailofbits/skills) 有 7,965 个 star，最近一次推送是 2026-11-02 20:47 UTC（北京时间 11 月 3 日 04:47）。仓库里的 marketplace 当时列出 46 个插件。本文只讲这两个。

## 先看结论

适合用它们的情况：你已经有一个可以陈述的问题，目标是本地 Git 仓库，而且你准备自己审核结果。

| 插件 | 2026-11-03 的清单版本 | 做什么 |
| --- | --- | --- |
| patching-bugs | 0.5.1 | 针对一个已知问题：复现、独立确认、写补丁、做三端证明，再调用 regression-hunt |
| regression-hunt | 1.2.0 | 针对一批 PR 或提交：找出补丁新引入的回归，用复现、重放和裁决把证据留下来 |

patching-bugs 的预检会确认 regression-hunt 已经安装。两个都装上，第一条流程才能走到回归检查。

和知识库里已有文章的分工：

- 想自己控制一次最小修复，用练习仓库把测试补上，看 [修复一个可复现 Bug](../04-代码修改与开发实战/04-修复一个可复现Bug-让补丁只解决当前问题.md)。
- 想先扫描仓库里可能的问题，看 [Codex Security CLI](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md)。那是 OpenAI 的扫描工具，和这两个插件不是一回事。
- 想自己打包插件，看 [插件开发入门](../08-插件工作流/05-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。

## 回移植案例里的数字，和这两个插件分开看

2026-11-02，Trail of Bits 发了 [Backporting security fixes at scale with Codex](https://blog.trailofbits.com/2026/11/02/backporting-security-fixes-at-scale-with-codex/)。文中的工作流是用 Codex 和 GPT-5.6 做安全补丁回移植：找出还没进稳定分支的修复、改到旧代码上、准备验证材料、跑测试、整理提交包。工程师审核补丁，再提交给维护者。

博客给出的人工投入，不含项目一开始的搭建：简单的回移植大约 30 分钟，复杂的大约 3 小时。到 2026-10-29，这个项目已经把 149 个不同 CVE 的修复送进稳定版 Linux 内核，另外还有 Fedora 和 Ubuntu 软件包的修复。博客写明，这些时间只覆盖补丁准备和审核；回归测试和维护者是否接受，仍然要单独做。

这篇博客没有说上述 149 个 CVE 修复是 patching-bugs 或 regression-hunt 跑出来的。两个插件来自同一团队更早的发布：[PR #471](https://github.com/trailofbits/skills/pull/471) 在 2026-10-20 20:16 UTC 合并，10 月 21 日的博客才公开介绍它们。10 月 21 日的文章说，工程师当时已经在 Patch the Planet 的工作里使用这两个插件，并在继续收集使用数据。那是插件的用途，不是 11 月 2 日那 149 个数字的来源。

背景可以记一笔：2026-06-22，OpenAI 和 Trail of Bits 一起推出 [Patch the Planet](https://openai.com/index/patch-the-planet/)，作为 Daybreak 计划的一部分，给开源维护者提供漏洞验证和补丁支持。6 月那篇公告里的模型和案例，和 11 月这篇回移植博客里的 GPT-5.6 不是同一次说明，不要混成一个版本号。

## 安装：添加 marketplace，再装这两个插件

仓库 README 给的 Codex 装法是：

```bash
codex plugin marketplace add trailofbits/skills
codex plugin list
codex plugin add regression-hunt@trailofbits
codex plugin add patching-bugs@trailofbits
```

`codex plugin marketplace add` 接受 `owner/repo` 这种 GitHub 仓库。2026-11-03 在 Codex CLI 0.166.0 上实测，市场名是 `trailofbits`，来源是 `https://github.com/trailofbits/skills.git`。建议先装 regression-hunt，再装 patching-bugs。安装顺序不影响 `plugin add` 成功；patching-bugs 是在真正开工前的预检里检查另一个插件在不在。

实测输出（独立 `CODEX_HOME`，未登录）：

```text
$ codex --version
codex-cli 0.166.0

$ codex plugin marketplace add trailofbits/skills
Added marketplace `trailofbits` from https://github.com/trailofbits/skills.git.

$ codex plugin add regression-hunt@trailofbits
Added plugin `regression-hunt` from marketplace `trailofbits`.
Installed plugin root: .../plugins/cache/trailofbits/regression-hunt/1.2.0

$ codex plugin add patching-bugs@trailofbits
Added plugin `patching-bugs` from marketplace `trailofbits`.
Installed plugin root: .../plugins/cache/trailofbits/patching-bugs/0.5.1
```

再跑 `codex plugin list`，两行是：

```text
patching-bugs@trailofbits      installed, enabled  0.5.1
regression-hunt@trailofbits    installed, enabled  1.2.0
```

用户级 `config.toml` 里会多出市场和插件开关：

```toml
[marketplaces.trailofbits]
source_type = "git"
source = "https://github.com/trailofbits/skills.git"

[plugins."patching-bugs@trailofbits"]
enabled = true

[plugins."regression-hunt@trailofbits"]
enabled = true
```

版本以插件清单为准。2026-11-03 核对时，`plugins/patching-bugs/.claude-plugin/plugin.json` 和 marketplace 都是 0.5.1；同目录 `pyproject.toml` 里的 `version` 仍是 0.3.0，那是辅助脚本包自己的字段。regression-hunt 的清单和 `pyproject.toml` 都是 1.2.0。

桌面端可以在插件界面里安装。OpenAI 的 [Plugins](https://learn.chatgpt.com/docs/plugins) 文档说，插件里的 Skills 要新开一个对话或新开 CLI 会话才可用，并且沿用宿主的沙箱和审批策略。这次没有登录，所以没有在对话里点选安装。

卸掉用：

```bash
codex plugin remove patching-bugs@trailofbits
codex plugin remove regression-hunt@trailofbits
```

## 运行前准备

README 写的前提，比安装命令多：

1. 目标是一个本地 Git 仓库。patching-bugs 要求工作区干净，并且你知道它平时的构建命令。一次只处理一个可以陈述的问题，不处理远程部署，也不要一次丢进一批漏洞。
2. 运行目录放在目标仓库的跟踪树外面。回归调查的 campaign 目录也放在插件目录和目标仓库外面。
3. 辅助脚本要求 Python 3.13 或更高版本，用 `uv run --no-project` 调用。脚本只做记录校验、三端证明和报告渲染，不负责派发 agent。本机是 Python 3.12.3，没有安装 `uv`，因此没有运行这些脚本。
4. 仓库根目录如果有 `THREAT_MODEL.md`、`PATCHING_GUIDELINES.md` 或 `AGENTS.md`，两个插件都会按对应提交读它们。regression-hunt 的技能说明写明，这些文件可以缺失。10 月 21 日的博客建议维护者自己写前两份：威胁模型说明什么算漏洞或回归；补丁指南说明怎么构建、补丁该多大、改哪里、回归测试要证明什么。`PATCHING_GUIDELINES.md` 也可以写成项目已有的 `AGENTS.md`。

威胁模型写什么，博客列了：哪些资产被破坏才算数、信任边界、访问控制、支持的配置、什么算或不算漏洞、一份有效报告需要什么证据。补丁指南写什么：怎么构建和测试、补丁规模、修改位置、怎么呈现改动、回归测试必须展示什么。

## patching-bugs：复现、确认、写补丁、证明

入口技能是 `patching-bugs`。它自己的说明是：当前本地代码里有一个已知问题，或一个可以证伪的假设，需要一份本地补丁提交和可以审核的证明报告。发现陌生改动里的新问题，应该改用 regression-hunt。

README 里的步骤技能：

| 技能 | 职责 |
| --- | --- |
| patching-bugs | 协调这一次问题、修复尝试、回归检查和报告 |
| reproduce-bug | 在未修改的基线上运行，保留 PoC 和原始回执 |
| validate-bug | 换一个新的 agent，独立重跑同一份 PoC，判断问题是否成立 |
| implement-patch | 在约定范围内修复，并创建一个本地提交 |
| prove-patch | 独立做范围检查和三端证明 |

三端证明来自 10 月 21 日的博客：同一套复现，对三份代码各跑一次。原始代码必须失败，打上补丁的代码必须通过，把补丁完全撤掉之后必须再次失败。博客把这叫做 three-arm proof，用来区分“补丁修好了”和“环境或测试碰巧变了”。

技能说明里的尝试上限是 3 次。某一步得到 `not_reproduced`、`blocked`、`not_confirmed` 或 `inconclusive`，就停下来出报告，不继续写补丁。证明失败会进入下一次修复尝试；三次之后仍没有证明过的补丁，结论是 Not ready。

你可以这样开口，把具体报告换成你自己的文件：

```text
使用 patching-bugs。目标是当前这个干净的 Git 仓库。
问题说明在仓库外的 ISSUE.md，一次只处理这一个问题。
运行目录放在仓库外面。不要 push，不要开 PR。
```

`ISSUE.md` 里写影响、复现步骤、期望行为和实际行为。技能说明要求把用户提供的报告当数据，缺的字段留空，不从补丁或测试里倒推。报告里不要放密码、Token 和客户数据。复现会按报告去跑项目自己的构建和检查，选一个可以丢弃的副本，不要指向生产机器。

## regression-hunt：补丁还改了什么

regression-hunt 调查你给出的 PR 或提交，包括已打开、已关闭、已合并的 PR，以及本地提交和明确的提交范围。它不负责写补丁，也不负责检查“原来的 bug 是不是修好了”。那是 patching-bugs 里 prove-patch 的工作。

| 技能 | 职责 |
| --- | --- |
| regression-hunt | 分派任务、记录进度、支持从保存的进度继续 |
| prepare-regression | 钉住源码和 PR 或提交的上下文 |
| hunt-regressions | 找出从这次改动引入、并且能到达真实接口的候选回归 |
| reproduce-regression | 在改动前、改动后两份部署上运行 PoC |
| replay-regression | 换一个 agent，原样重跑这份 PoC |
| adjudicate-regression | 按定义判断是不是回归，并套用排除项 |
| report-regressions | 校验并渲染已经保存的决定 |

10 月 21 日的博客写了一项初步评估：相对一个只被提示“review the PR for regressions”的 Codex，regression-hunt 的误报少 25%，95% 置信区间是 14% 到 38%。同一篇文章写了代价：证据要求更严，有些已知回归被留在“边界情况”，插件看见了可能的问题，但没有收集到足够证据把它确认下来。这个百分比是他们当时的评估，不是安装之后的保证。

博客里对回归的定义可以当作阅读报告时的尺子：新缺陷打破了改动前正确、且仍被支持的行为，并且真实用户或攻击者能够到达那条路径。他们回顾已合并 PR 时，在 130 多个 PR 里确认了 21 个回归（16 个功能、1 个性能、4 个构建或测试），并写明没有一个破坏安全防护。这些数字描述的是他们自己的补丁回顾，不是你仓库上的预期结果。

## 读报告

patching-bugs 的渲染脚本始终写出 `report.html`，失败和无法下结论的运行也有这份审计报告。只有记录被校验通过、结论是可以交给维护者审核的补丁时，才另外写出 `maintainer-report.html`。技能说明用的词是 READY：验证过的补丁才有这份维护者报告。

regression-hunt 的 `docs/report-definitions.md` 用另一套结论，不要和 READY 混用：

| 结论 | 含义 |
| --- | --- |
| REPRODUCED_REGRESSION | 在改动前后的现场都证明了新缺陷，并且独立重放和裁决都做过 |
| INCOMPLETE_FIX | 预定的修复漏了某个输入来源、调用方或用法 |
| LATENT_BUG | 这次改动把一个已经存在的缺陷暴露出来 |
| PREEXISTING_BUG | 失败在改动前就已经能到达 |
| REJECTED | 引用的证据否定了回归所需的某一条标准 |
| UNRESOLVED | 证据、执行或审核仍然缺失，或互相矛盾 |

只有 `REPRODUCED_REGRESSION` 计入确认数量。覆盖率 `COMPLETE` 表示发现做完了、基线可用、每个候选都有决定。文档写明，Complete 不等于没有 bug。确认项是 agent 的结论，等人审核。哈希能核对证据包没有被改过，不能代替你去看源码、搭建方式和日志。

patching-bugs 把 regression-hunt 的范围定在 `baseline..patch_commit`。任何被复现的回归或未完成的修复，都会让补丁变成 Not ready；没解决的发现或覆盖不全，会变成报告里的 concerns。

## 边界

- 不 push，不开 PR。本地可以出现一个补丁提交。要不要推远程，由你在看完 diff、测试和两份报告之后决定。
- 安装插件不会授予云上花费、导出源码或发布补丁的权限。regression-hunt 的说明写明，云基础设施是可选的，必须另外授权，插件不会自己创建。
- 脚本通过记录校验，只说明材料齐全，不说明结论为真。技能说明把 “The script accepted it” 列成要拒绝的借口。
- 没有独立的第二次复现和裁决时，候选应保持未解决，不能写成“已经确认没有回归”。
- 一次只处理一个问题。范围外的其他 bug 留在报告里，不跟着这一份补丁一起改。

## 常见问题

**Marketplace 加不上去。** 先看网络能不能访问 `https://github.com/trailofbits/skills.git`，再看 `codex plugin marketplace list`。0.166.0 的子命令是 `add`、`list`、`upgrade`、`remove`。

**装上了，新对话里看不到技能。** 官方插件文档要求新开对话或新开 CLI 会话。项目如果不受信任，Codex 不会加载项目级配置；这两个插件装在用户级 `CODEX_HOME`，一般不受这一条影响。

**pyproject 写着 0.3.0，list 却是 0.5.1。** 以 `codex plugin list` 和 `plugin.json` 的 0.5.1 为准。0.3.0 是脚本包字段。

**报告是 INCONCLUSIVE 或 UNRESOLVED。** 这是停下来的信号。补构建、补威胁模型，或把复现步骤写具体，再开一次运行。不要把未完成的证据改写成“没有问题”。

## 下一步

先在一个可以丢弃的仓库上把安装和 `codex plugin list` 跑通。有一份你自己能复现的问题时，再把 patching-bugs 指到那一个问题，并规定运行目录在仓库外。

手工控制最小补丁，继续看 [修复一个可复现 Bug](../04-代码修改与开发实战/04-修复一个可复现Bug-让补丁只解决当前问题.md)。扫描和这两个插件的差别，看 [Codex Security CLI](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md)。

## 参考资料

- [trailofbits/skills](https://github.com/trailofbits/skills)（第三方，CC BY-SA 4.0）
- [patching-bugs](https://github.com/trailofbits/skills/tree/main/plugins/patching-bugs)
- [regression-hunt](https://github.com/trailofbits/skills/tree/main/plugins/regression-hunt)
- [Add regression-hunt and patching-bugs plugins，PR #471](https://github.com/trailofbits/skills/pull/471)
- [Backporting security fixes at scale with Codex](https://blog.trailofbits.com/2026/11/02/backporting-security-fixes-at-scale-with-codex/)
- [Your AI agent fixed the bug, but what else did it change?](https://blog.trailofbits.com/2026/10/21/your-ai-agent-fixed-the-bug-but-what-else-did-it-change/)
- [Patch the Planet](https://openai.com/index/patch-the-planet/)
- [Codex Plugins](https://learn.chatgpt.com/docs/plugins)
