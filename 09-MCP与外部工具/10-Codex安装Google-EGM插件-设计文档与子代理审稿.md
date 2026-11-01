---
id: codex-google-egm-plugin
title: Codex 安装 Google EGM 插件：先写设计文档，再让零上下文子代理审稿
seo_title: Codex 安装 Google EGM：设计文档与零上下文子代理审稿
description: EGM 是 Google 工程师开源的设计文档插件，不是 Google 官方产品。本文用 Codex CLI 0.166.0 安装 marketplace 里的 egm@egm，核对 7 个 Skill、子代理审稿条件和卸载命令，并说明什么任务值得走这套流程。
lede: Elephant 带着项目上下文写设计，Goldfish 只看文档和它引用的源码。小而明确的 bug 不必走这套流程。
url: /guides/codex-google-egm-plugin-design-review
status: published
section: guides
category: I-ecosystem
topic: 社区生态与编辑器接入
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-01
date_modified: 2026-11-01
verified_on: 2026-11-01
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/codex/skills-and-plugins
keywords: [Codex EGM 插件, elephant-goldfish-model, Codex 设计文档审查, Codex 子代理审稿, codex plugin marketplace add]
related: [codex-superpowers-plugin, codex-subagents-parallel-work, create-codex-skill]
howto: true
faq:
  - q: EGM 是 Google 官方产品吗？
    a: 不是。仓库 README 和插件清单都写着 This is not an officially supported Google product。许可证是 Apache-2.0。
  - q: Codex 里用 /egm: 前缀调用吗？
    a: README 写明，/egm: 前缀用于 Antigravity CLI 和 Claude Code。在 Codex 里从 Skill 选择器选择对应的 EGM Skill。
  - q: 审稿一次花多少额度？
    a: 官方暂未说明。仓库没有给出审稿的 token 或额度数字，本文不估算。
  - q: 会话不能新建子代理时会怎样？
    a: 仓库写明，Goldfish 审稿需要新的子代理上下文。会话没有子代理工具时，EGM 会停止审稿，而不是在同一段上下文里审。
---

# Codex 安装 Google EGM 插件：先写设计文档，再让零上下文子代理审稿

> 本文在线版：[codexguide.io/guides/codex-google-egm-plugin-design-review](https://codexguide.io/guides/codex-google-egm-plugin-design-review)

> 核对依据：[google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) 的 README、`docs/harnesses.md`、`skills/egm-review/SKILL.md` 和 `.codex-plugin/plugin.json`，以及 Codex CLI 0.166.0 在独立 `CODEX_HOME` 里的安装、列表和卸载输出。审稿会消耗的额度没有官方数字。本环境没有登录 Codex，没有跑完 brainstorm → review。

EGM（Elephant-Goldfish Model）解决的是动手写代码之前的设计文档：主代理带着项目上下文起草，另一批看不到先前对话的子代理只根据文档和它引用的源码挑假设。它是第三方插件。README 的许可证一节写着：This is not an officially supported Google product.

## EGM 是什么

2026-11-01 通过 GitHub API 看到的仓库状态：约 7,792 stars、460 forks，Apache-2.0，仓库创建于 2026-09-13，最近推送 2026-10-30 17:33（北京时间）。v0.1.0 发布于 2026-10-27 15:46（北京时间）。官网写在插件清单里，是 [egm.dev](https://egm.dev)。star 数会变，以你打开仓库时的数字为准。

README 把三个角色写成：

| 角色 | 看得到什么 | 负责什么 |
|---|---|---|
| Elephant | 项目、需求和先前的决定 | 把问题想清楚，起草规格 |
| Goldfish | 文档和它引用的源码，没有先前对话 | 找出没说出口的假设、含糊的需求和实现风险 |
| 你 | 真正在意的目标和约束 | 做取舍，批准设计，决定做什么 |

README 还写：Thousands of Google engineers use EGM。这是仓库自述，本文没有另行核实使用人数。

小而明确的 bug 修复，README 建议走平常的编码流程，不必先写这套设计文档。

## 安装

README 和 `docs/harnesses.md` 给 Codex 的命令是：

```bash
codex plugin marketplace add google/elephant-goldfish-model
codex plugin add egm@egm
```

装完要新开一个会话。只复制 `skills/` 目录的安装方式会把插件弄坏，因为技能在运行时要读 `agents/` 和 `resources/document_standards/`。装整包。

2026-11-01，Codex CLI 0.166.0，在一个新建的 `CODEX_HOME` 里实际跑了这两条命令。输出是：

```text
Added marketplace `egm` from https://github.com/google/elephant-goldfish-model.git.
Added plugin `egm` from marketplace `egm`.
```

安装根目录在该 `CODEX_HOME` 下的 `plugins/cache/egm/egm/0.1.0`。`codex plugin list` 里这一行是 `egm@egm`，状态 `installed, enabled`，版本 `0.1.0`。

装好的 `.codex-plugin/plugin.json` 版本是 0.1.0，`requires_local_executor` 为 `true`。界面长说明写着：Reviews require isolated subagents; cloud support remains partial. 同一段也写了 Not an officially supported Google product.

## 验证插件和 Skill 是否可用

新开会话后，在 Codex 的 Skill 选择器里应能看到 EGM 的技能。EGM 的 README 写明：示例里的名字在 Antigravity CLI 和 Claude Code 上要加 `/egm:` 前缀；在 Codex 里从 Skill 选择器调用。OpenAI 的 [Skills 与插件](https://learn.chatgpt.com/codex/skills-and-plugins) 页还写，Codex 可以用 `$` 提及技能。本次没有登录，没有验证 `$egm-brainstorm` 能否触发 EGM。

本次安装落盘的 `skills/` 目录有 7 个技能，和 README 的表一致：

- `egm-brainstorm`
- `egm-draft`
- `egm-review`
- `egm-resolve`
- `egm-bootstrap`
- `egm-review-loop`
- `egm-drift-report`

`docs/harnesses.md` 写：Antigravity、Claude Code 和 Codex 通过了自动安装、审稿隔离和端到端流程夹具。这句话是上游的测试记录。本环境核对的是安装、列表、磁盘上的 7 个 Skill，以及后面的卸载命令。没有登录，所以没有做端到端审稿。

## 7 个 Skill 分别做什么

名字和职责来自 README 的表，以及本次安装的各 `SKILL.md` 开头的 description。不必按顺序全部跑完。

| Skill | 用来做什么 | 技能文件里的产出或范围 |
|---|---|---|
| `egm-brainstorm` | 把一个想法问清楚 | 交互式澄清、审阅和迭代，产出给人看的 RFC 摘要；也可再交给 `egm-draft` |
| `egm-draft` | 把摘要或已有笔记写成设计文档 | 按节起草，用的是 brainstorm 的 concepts brief 或用户笔记 |
| `egm-review` | 用新的子代理审设计 | 五个阶段：Initial Zoom Out Review、Comprehension Review、Design Critique、Intermediate Zoom Out Review、Implementation Readiness |
| `egm-resolve` | 处理审稿意见 | 接收审稿人的缺陷报告，对 PROPOSE FIX 项走选择，并在检查点上协商 |
| `egm-bootstrap` | 给已有代码库补文档 | 在仓库子树里建立或更新目录中的 README.md |
| `egm-review-loop` | 按一组审稿人循环审 | 对照质量标准和结构模板审计文档，并应用已批准的修改 |
| `egm-drift-report` | 看文档和代码是否还一致 | 对设计文档做漂移检查，产出差异报告 |

README 对 brainstorm 和 draft 的文件名写的是 `concepts_brief.md` 和 `design_draft.md`。draft 会逐节停下来等聊天里的反馈。产物默认写在工作目录；也可以在提示或 `AGENTS.md` 里加一行 `EGM artifact directory: .dev/docs`，相对路径相对工作目录。不想提交这些文件时，把该目录写进 `.gitignore`。

## 一次完整流程

上游 Quickstart 的顺序是 brainstorm → draft → review。下面是 README 里的调用内容。Codex 里用 Skill 选择器选中对应技能，再把任务写进对话。本环境没有登录，下面的流程没有在本机跑出 `concepts_brief.md` 或审稿报告。

1. **brainstorm。** 选一个需要设计决定的功能，例如 README 用的例子：给项目加 webhook 投递，失败和重复投递该怎么处理。技能保存商定的方向。
2. **draft。** 把摘要写成设计文档，每节停下来等你的反馈。
3. **review。** 把 draft 给出的文档路径交给 `egm-review`。新的审稿人看设计是否清楚、是否贴合代码、实现计划是否站得住。你决定哪些意见要处理。
4. **resolve。** 逐条处理要采纳的意见。你批准设计之后，再让编码代理去实现。

批准后的规格可以放到 `docs/designs/`，这是上游 getting started 里的目录建议。

## 审稿为什么需要新的子代理

Goldfish 的定义就是不看先前对话。`docs/harnesses.md` 写：Codex 使用原生 spawn/wait 工具；没有具名的 persona 时，技能会启动一个通用子代理，并让它先读 `agents/` 下的 persona 文件。`egm-review` 的技能文件把 Codex 侧的工具写成 `spawn_agent`。

同一页写明：如果环境没有子代理工具，审稿技能会停下来，不会在同一段上下文里充作 Goldfish 审稿。Cloud 支持在插件说明里被写成 partial。

子代理怎么开、审批和用量怎么落，见 [Subagents](../11-自动化与高级工作流/06-Codex使用Subagents并行处理任务.md)。OpenAI 的 [Subagents](https://learn.chatgpt.com/codex/agent-configuration/subagents) 页写明：当前 Codex 版本默认可以跑子代理；每个子代理自己做模型和工具工作，因此比同等的单代理运行消耗更多 token。该页没有给出倍数。EGM 一次审稿实际扣多少额度，仓库和定价页都没有单独的数字，官方暂未说明。

## 什么任务值得用，什么任务不必用

值得用：功能有设计取舍，例如失败策略、重复请求、权限边界，而且你希望有人在不记得「刚才怎么讨论的」的前提下重读文档。

不必用：README 点名的小而明确的 bug 修复。目标、修改点和验证方式都已经清楚时，直接改代码并跑测试更快。

EGM 也不代替测试。harnesses 页写：A review does not replace tests or human judgment.

## 和 Superpowers 怎么选

[Superpowers](../08-插件工作流/06-Codex安装Superpowers插件-需求计划TDD工作流.md) 把需求、计划和测试先行串成一条工作流。EGM 只覆盖「写实现之前的设计文档，以及零上下文审稿」这一段。

已经决定怎么做、缺的是按工程环节拆好的步骤时，用对应的 Skill 或自己写的 Skill，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。还没决定接口和失败行为时，先用 EGM 把设计写下来再审。

## 更新与卸载

更新上游时，重新执行 marketplace 的升级。0.166.0 的子命令是：

```bash
codex plugin marketplace upgrade
```

`codex plugin marketplace --help` 列出的命令是 add、list、upgrade、remove。upgrade 的说明是刷新已配置的 Git marketplace 快照。升级后新开一个会话，再看 `codex plugin list` 里的版本是否仍为你期望的版本。本次核对没有在升级前后对比两个版本号，因为安装到的就是当前的 0.1.0。

卸载在同一个临时 `CODEX_HOME` 里实际执行过：

```bash
codex plugin remove egm@egm
codex plugin marketplace remove egm
```

0.166.0 的输出是 `Removed plugin `egm` from marketplace `egm`.`，随后 `codex plugin list` 里该插件状态变为 `not installed`。再执行 marketplace remove 后，输出 `Removed marketplace `egm`.`，列表变为 No plugin marketplaces in scope。

`codex plugin remove --help` 也接受 `codex plugin remove egm --marketplace egm`。插件说明写明它使用你当前宿主的模型和权限。安装前可以先看仓库的 `skills/`、`agents/` 和 `LICENSE`。

## 常见问题

**装完当前会话里看不到技能？** README 要求安装后新开一个会话。

**可以只装某一个 Skill 吗？** harnesses 页要求装整个插件。只拷贝 `skills/` 会在运行时读不到审稿人和文档标准。

**ChatGPT Work 怎么装？** harnesses 页把 ChatGPT 写成另一条路径：个人测试可以上传插件包，工作区由管理员按仓库 URL 导入 marketplace。那不是本文这条 `codex plugin add`。该页同时写 ChatGPT Work 的云端追踪验证还有缺口。

## 参考资料

- [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model)（README、LICENSE、2026-11-01 的仓库元数据）
- [docs/harnesses.md](https://github.com/google/elephant-goldfish-model/blob/main/docs/harnesses.md)
- [Skills and plugins](https://learn.chatgpt.com/codex/skills-and-plugins)
- [Subagents](https://learn.chatgpt.com/codex/agent-configuration/subagents)
