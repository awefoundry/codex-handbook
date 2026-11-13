---
id: codex-pierre-acquisition-code-storage
title: OpenAI 收购 Pierre：Codex 里的 Trees、Diffs 和即将并入的 Code Storage 意味着什么
seo_title: OpenAI 收购 Pierre：Codex 的 Trees、Diffs 与 Code Storage
description: OpenAI 于 2026-11-04 宣布将收购 Pierre。本文说明 Codex App 里已经用到的 Trees 与 Diffs、交割完成后才准备并入的 Code Storage，以及它和 Pando、GitHub 为什么还不是一回事。
lede: 今天能确定的是审查和浏览代码时用到的两套库。代码托管要等收购交割，而且官方没有给上线日期。
url: /guides/codex-pierre-acquisition-code-storage
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 解释
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 20
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-06
date_modified: 2026-11-06
verified_on: 2026-11-06
official_ref: https://openai.com/index/openai-to-acquire-pierre
keywords: [OpenAI Pierre, Codex Code Storage, Codex Trees, Codex Diffs, Pierre Computer, Pando]
related: [codex-desktop-task-workflow, codex-changyong-gongneng-qingdan]
faq:
  - q: Codex 现在是不是已经自带一套 Git 托管，可以不用 GitHub 了？
    a: 不是。公告写明，交割前 OpenAI 和 Pierre 仍是各自独立的公司。Trees 和 Diffs 已经用在 Codex App 的文件浏览和变更审查里。Code Storage 是交割完成后才准备并入 Codex 的能力，官方没有给出上线日期。
  - q: 现有的 Code Storage 客户会不会在交割当天被停掉？
    a: 公告的说法是，交割完成后客户可以继续使用 Code Storage，与此同时 OpenAI 再把它的功能做进 Codex。公告没有写迁移截止日期。
  - q: Pando 是不是这次收购附带的新产品？
    a: 不是。Pando 是 OpenAI 在 2026-11-02 单独介绍的内部 Git 后端，用来支撑自己的单仓库。它和 Pierre 的 Code Storage 不是同一个产品，公告也没有说读者可以在 Codex 里开通 Pando。
---

# OpenAI 收购 Pierre：Codex 里的 Trees、Diffs 和即将并入的 Code Storage 意味着什么

> 本文在线版：[codexguide.io/guides/codex-pierre-acquisition-code-storage](https://codexguide.io/guides/codex-pierre-acquisition-code-storage)

> 核对依据：OpenAI《[OpenAI to acquire Pierre Computer Company, Inc.](https://openai.com/index/openai-to-acquire-pierre)》（2026-11-04）和《[Scaling Git at OpenAI](https://openai.com/index/scaling-git-at-openai)》（2026-11-02）。本文没有登录 Codex App 核对界面文案，也没有 Code Storage 账号。库和产品的名称以公告为准。

适合已经在 Codex App 里看 diff、也在用 GitHub 或别的 Git 托管的人。读完可以判断：今天多出来的是什么，交割完成之后官方说要做什么，以及哪些说法现在还不能当成产品承诺。

## 先看结论：今天能用什么，交割后可能多什么

2026-11-04，OpenAI 宣布将收购 Pierre Computer Company, Inc.（公告里简称 Pierre）。Pierre 做 Code Storage，也做一批开源的开发者工具。

按公告，可以分成三层，不要混在一起：

| 对象 | 现在的状态 | 你能不能把它当成「Codex 已经内置的 Git 托管」 |
| --- | --- | --- |
| Trees、Diffs | 已经用在 Codex App 里。浏览项目文件、审查一处改动时，用的就是这两套库 | 不能。它们是看代码和看变更的库，不是仓库托管 |
| Code Storage | Pierre 现有的服务：让应用用 Git 存代码、记历史。交割完成后，客户可以继续用；OpenAI 同时准备把它的功能做进 Codex | 不能。收购还没交割，官方没有写上线日期 |
| Pando | OpenAI 自己的 Git 后端，2026-11-02 的文章说它已经支撑 OpenAI 的单仓库 | 不能。那是 OpenAI 内部工程系统，不是这次交给读者开通的托管产品 |

收购交割还要满足惯例条件，包括监管审批。交割之前，两家公司仍然分开、独立经营。所以下面凡是「并入 Codex」的句子，都是公告里的意向，不是已经上线的功能。

## Pierre 是谁：Code Storage、Trees、Diffs、Highlights

公告把 Pierre 的工作分成两类。

一类是已经进了 Codex App 的库：

- **Trees**：用来在项目里快速翻文件。
- **Diffs**：用来看改了什么。公告强调它要在大量代码上仍然保持性能。

另一类是同一团队的其他工作，公告没有说它们已经出现在 Codex 界面里：

- **Diffs 的 Edit mode**：审查时可以在发现问题的那一行直接改。这是公告对 Pierre 这套 Diffs 的描述。公告没有单独说 Codex App 里已经有一个同名按钮。
- **Highlights**：Pierre 近期发布的语法高亮，官方的说法是输入或 agent 输出代码时刷新很快。公告没有说 Highlights 已经并进 Codex。
- **Code Storage**：给应用存代码、并用 Git 跟踪历史的服务。公告把它和前面的开源库并列介绍，但并入 Codex 的时间点写在交割之后。

开源项目在交割完成后继续开源，OpenAI 写明会继续贡献。公告没有在这篇里列出仓库地址或许可证文本，具体仓库以 Pierre 当时公布的项目页为准。

## 你在 Codex App 里已经碰到的部分

公告的原意可以收成一句：如果你在 Codex App 里浏览过文件，或审查过一处改动，你已经用过 Pierre 的 Trees 和 Diffs。

这和「Codex 变成了 Git 主机」不是一件事。今天这几步仍然是原来的工作流：

1. 代码还在你自己的 Git 仓库里，远程可以是 GitHub 或其他托管。
2. Codex 在授权范围内改文件、跑命令。
3. 你在 App 里看文件树和 diff，决定哪些改动可以留下。
4. 提交、开 Pull Request、请人复查，仍然走你原来的 Git 托管。

怎么把一次改动写成别人审得动的提交，见[怎样写出可审查的 Commit 和 PR](../05-Git协作与代码审查/05-怎样写出可审查的Commit和PR-范围验证证据与风险.md)。桌面端里项目、并行对话和审查怎么串起来，见[Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)。

本文没有新的 App 截图。公告没有给出 Trees 或 Diffs 的菜单名称，界面文案以你当前的 Codex App 为准。

## 官方怎么说「并入 Codex」，以及交割条件

公告里和读者直接相关的句子是：

- 交割完成后，客户可以继续使用 Code Storage。
- 与此同时，OpenAI 会把 Code Storage 的功能做进 Codex。
- 更大的意向是：让 Codex 把「公司发出去的代码」和「人做出的决定」连起来，并适应 agent 并行开发的规模。
- 交割取决于惯例条件，包括拿到监管批准。
- 交割前，OpenAI 和 Pierre 保持独立。

这里没有版本号，没有「某月某日在 App 里上线」的句子，也没有写个人账号、团队账号或企业账号谁先得到。把「will acquire」「once the acquisition closes」「our ambition」读成「这个功能今天已经在 Codex 里」，就会把意向写成现状。

交割完成之前，不需要为了这篇公告去改 `config.toml`，也不需要把远程从 GitHub 迁走。

## 开源项目和现有 Code Storage 客户

公告对两类使用者是分开说的。

**开源项目**：继续开源，OpenAI 继续贡献。如果你依赖 Trees、Diffs 或 Highlights 的公开仓库，这篇公告没有要求你立刻换包、换导入路径。仓库以后的维护地址，要等 Pierre 或 OpenAI 另行说明。本文没有逐个打开这些仓库核对最近一次提交。

**Code Storage 的现有客户**：交割完成后可以继续用这项服务，同时 OpenAI 再把它的能力做进 Codex。公告没有写「必须在交割日迁到 Codex」或「旧服务会在某一天关闭」。要做迁移决定，等交割完成之后的客户通知，不要按这篇收购公告提前停掉正在用的存储。

## 和 Pando、GitHub 的关系

同一周早些时候，OpenAI 发了《Scaling Git at OpenAI》（2026-11-02）。收购公告点名了这篇文章里的 Pando：OpenAI 自建的 Git 仓库后端，给工程师和 agent 用。

Pando 文章里和本文有关的范围是：

- 它现在支撑 OpenAI 自己的单仓库开发。
- 它保持 Git 协议和客户端兼容，工程师和 agent 不用改掉现有的 Git 用法。
- 文章给出的生产结果包括：推送延迟的中位数降到将近原来的五分之一，每天送出接近 1 PB 的 Git 数据。

这些数字说明的是 OpenAI 内部单仓库的后端，不是 Codex 产品设置里的一个开关。收购公告把 Pando 和 Pierre 放在同一段，是在解释他们为什么关心「Git 周围的系统」，不是在说读者要在 Codex 里二选一。

可以这样区分预期：

| 你在做的事 | 今天该用什么 | 不要误读成 |
| --- | --- | --- |
| 看文件、看 diff、决定留哪些改动 | Codex App 里已有的 Trees 和 Diffs | 一套新的托管 |
| 把仓库放在 GitHub 或其他 Git 远程上 | 继续用原来的远程和审查流程 | 被 Code Storage 替换 |
| 关心 OpenAI 自己怎么扛 agent 并行推送 | 读 Pando 那篇文章 | 一项已经对客户开放的托管产品 |
| 等代码存储进 Codex | 等交割完成之后的产品说明 | 一个已经承诺日期的功能 |

GitHub 插件、云端环境和本地 worktree 该怎么选，仍然看各自的文章。常用入口见[Codex 常用功能清单](./11-Codex常用功能清单.md)。

## 常见问题

**要不要现在注册 Code Storage，以便交割后自动出现在 Codex 里？**

公告没有这种迁移通道。现有客户可以在交割后继续用 Code Storage。没有账号的人，等 Codex 里真的出现对应功能再评估。

**Trees 和 Diffs 会不会以同一个名字出现在 CLI 里？**

公告点名的界面是 Codex App 的文件浏览和变更审查。它没有写 CLI 或 IDE 扩展的命令名。本文没有在 CLI 里查找同名命令。

**Highlights 能不能在 Codex 里打开？**

公告只说 Pierre 发布了这个高亮组件，没有说它已经是 Codex 的一项设置。

## 参考资料

- [OpenAI to acquire Pierre Computer Company, Inc.](https://openai.com/index/openai-to-acquire-pierre)（2026-11-04）
- [Scaling Git at OpenAI](https://openai.com/index/scaling-git-at-openai)（2026-11-02，Pando）
- [Codex 桌面端任务工作流](./08-Codex桌面端任务工作流.md)
- [怎样写出可审查的 Commit 和 PR](../05-Git协作与代码审查/05-怎样写出可审查的Commit和PR-范围验证证据与风险.md)
