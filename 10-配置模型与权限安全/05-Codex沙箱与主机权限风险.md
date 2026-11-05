---
id: codex-sandbox-host-trust
title: Codex 沙箱与主机权限风险（2026-11 更新）：git show 白名单逃逸复盘，和现在怎么用权限、Rules、Hooks 防
seo_title: Codex 沙箱与主机权限：git show 逃逸和现行防护
description: 沙箱只管 Codex 执行的命令，管不住沙箱外的程序事后执行它写下的文件。本文更正旧文把 GHSA-w5fx-fh39-j5rw 当成 git show 编号的错误，并按 0.166.0 的源码和官方文档说明现在的权限、Rules 和 Hooks。
url: /guides/codex-sha-xiang-yu-zhu-ji-quan-feng-xian
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 案例
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-24
date_modified: 2026-11-02
verified_on: 2026-11-02
tested_cli_version: 0.166.0
official_ref: https://learn.chatgpt.com/docs/sandboxing
keywords: [Codex 沙箱逃逸, Codex 主机权限风险, Codex git show 漏洞, Codex 安全命令白名单, Codex 提示注入]
related: [permissions-sandbox-approvals, codex-rules-prefix-rule, hooks-guide, codex-built-in-browser-local-file-risk]
howto: false
faq:
  - q: GHSA-w5fx-fh39-j5rw 是 git show 这次的编号吗？
    a: 不是。它是 2025-09-19 发布的另一条公告，标题是 Sandbox bypass due to bug in path configuration logic，别名 CVE-2025-59532，在 Codex CLI 0.39.0 修复。git show 这次在 2026-11-02 的公告列表里没有单独条目。GHSA 也不是 CVE 编号。
  - q: 升到 0.95.0 之后，git show 还会因为命令名被自动放行吗？
    a: Pillar 记载补丁在 2026-02-04 的 v0.95.0。到 0.149.0（2026-08-20），更新日志的提交列表包含「不再把 Git 命令本身当成已知安全」和「移除 known-safe 命令白名单」。0.166.0 的源码树里已经没有 is_safe_command.rs。本文没有在登录会话里实跑 git show --output，不能把它写成一条实测过的审批结果。
  - q: 自己写一条 allow git show 的 Rules，安全吗？
    a: 不安全。官方写明，decision 为 allow 的 prefix_rule 会让匹配命令在沙箱外运行，并且不再询问。过宽的 git show 前缀会把参数也一起放出去。
---

# Codex 沙箱与主机权限风险（2026-11 更新）：git show 白名单逃逸复盘，和现在怎么用权限、Rules、Hooks 防

> 本文在线版：[codexguide.io/guides/codex-sha-xiang-yu-zhu-ji-quan-feng-xian](https://codexguide.io/guides/codex-sha-xiang-yu-zhu-ji-quan-feng-xian)

> 核对依据：Pillar Security 2026-07-20 的 [GitPwned: Allowlist to RCE](https://www.pillar.security/blog/gitpwned-allowlist-to-rce)；[GHSA-w5fx-fh39-j5rw](https://github.com/openai/codex/security/advisories/GHSA-w5fx-fh39-j5rw)；2026-11-02 查询的 [openai/codex 安全公告列表](https://github.com/openai/codex/security/advisories)（只有这一条）；[更新日志](https://learn.chatgpt.com/codex/changelog) 中 0.149.0 的完整提交列表；标签 `rust-v0.166.0` 的源码树；OpenAI 文档 [Sandbox](https://learn.chatgpt.com/docs/sandboxing)、[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)、[Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)、[Hooks](https://learn.chatgpt.com/docs/hooks)。旧文没有 frontmatter，`date_published` 使用本仓库首次收入该文的提交日期 2026-08-24。旧文四张配图是概念示意图，图注却都叫「操作步骤」，本次全部移除，不另配图。

沙箱限制的是 Codex **正在执行**的命令。它不自动约束沙箱外面的 Git、编辑器任务、钩子和内置浏览器：这些组件事后可以读 Codex 已经写下的文件，并按它们自己的规则执行。2026 年 1 月报告、2 月在 Codex CLI v0.95.0 修复的 git show 白名单问题，就是这条缝。旧文把编号写成了「CVE GHSA-w5fx-fh39-j5rw」。那个编号属于 2025 年 9 月的另一次沙箱绕过，本文改正。

## 先看结论

- 使用 2026-11-02 的正式版 Codex CLI 0.166.0，或任何不低于 v0.95.0 的版本。git show 按命令名跳过沙箱的那次问题，Pillar 记载已在 v0.95.0 修复。0.149.0 起，Git 命令不再被当成天然安全，known-safe 白名单也从当时的审批路径里去掉了。
- 日常用工作区写入加按需审批，不要用 Full access（`danger-full-access` 且不再询问）。怎么选预设，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。
- 不要用一条很短的 Rules 把 `git show` 整体放行到沙箱外。Rules 的 `allow` 会跳过沙箱和询问。
- 模型拒绝执行某条指令，不能当作这道防线还在。
- 内置浏览器打开本地 HTML 的风险在沙箱之外，见 [内置浏览器本地文件读取](./21-Codex内置浏览器本地文件读取风险-EMBRACE自查与防护.md)。

## 沙箱管到哪里

可以把它看成三层。前两层是 Codex 自己的执行；第三层是别的程序。

**直接执行。** 模型发出的命令由 Codex 启动。官方沙箱文档写明：沙箱作用在拉起的命令上，不限于内置的文件操作。`git`、包管理器和测试命令都带上同一道边界。默认的低摩擦模式是 `workspace-write`：可以读文件、在工作区里改、跑工作区里的常规本地命令。`read-only` 更窄。`danger-full-access` 去掉文件系统和网络边界，只在你明确要给它整台机器时使用。

**工作区写入。** 在 `workspace-write` 里，Codex 可以改工作区里的文件。这些文件会留下来，给后面的工具看。

**宿主信任。** 沙箱外面还有 Git、编辑器任务、已安装的钩子和你亲手打开的预览。它们的权限是你的用户权限，不是 Codex 的沙箱权限。Codex 只要写下了一个这些程序会执行的文件，第三层就接上了。

审批是另一根旋钮：`on-request` 在越出沙箱时停下来问；`never` 不问。官方写明，沙箱决定技术边界，审批决定什么时候必须先问。把审批开得很严，不会让沙箱外的 Git 钩子或内置浏览器变得更窄。

## 复盘：git show 白名单逃逸

Pillar Security 在 2026-07-20 公开了 “The Week of Sandbox Escapes” 系列的第 5 篇。他们描述的是当时的 Codex CLI：一份默认开启的安全命令白名单。名单上的命令被认为无论参数如何都不会造成伤害，于是跳过沙箱、跳过用户批准，以用户权限执行。`git show` 在名单上，因为人们把它当成「显示某次提交」。

当时的缝在参数。`git show` 可以带 `--output`，把输出写到文件而不是终端；`--format` 决定写下的文本。两者合在一起，就是按调用者指定的内容写文件。Pillar 的演示把一段 git 配置写进仓库的 `.git/config`：`[diff]` 下面的 `external` 指向攻击者指定的命令。`git diff` 当时也在同一份白名单上。下一次有人在这个仓库运行 `git diff`，git 会调用这个外部 diff 程序，命令以用户权限执行。全程没有审批框。

这不是沙箱被打穿的内存错误。白名单让这条命令根本没进沙箱。Pillar 对比过：同样的 Codex 去跑不在名单上的 `curl` 时会要求批准；跑带 `--output` 的 `git show` 时什么都不问。

他们的披露时间线：

- 2026-01-07：经 Bugcrowd 提交报告
- 2026-01-29：OpenAI 确认 CVSS 8.6
- 2026-02-04：补丁进入 v0.95.0
- 2026-02-17：发放赏金
- 2026-07-20：公开

CVSS 8.6 来自 Pillar 记录的厂商确认，不是下面那条 GHSA 页面上的分数。两条问题的分数碰巧相同。2026-11-02 打开的更新日志没有再单列 v0.95.0 这条旧修复，版本号和时间以 Pillar 的时间线为准。

入口是提示注入，不是用户亲手输入那条 git 命令。场景是让 Codex 读一份外部说明或第三方库的文档，文档里夹了一句指示，模型照做。文档、README、issue 都是不可信输入。

## 编号不要再写成 GHSA-w5fx-fh39-j5rw

旧文写「漏洞编号 CVE GHSA-w5fx-fh39-j5rw」，并把这个号安在 git show 上。两处都错。

GHSA 是 GitHub Security Advisory 的编号，不是 CVE 编号。2026-11-02 用 GitHub API 拉取 `openai/codex` 的安全公告，列表里只有一条：

- 编号：GHSA-w5fx-fh39-j5rw
- 发布：2025-09-19
- 标题：Sandbox bypass due to bug in path configuration logic
- 别名：CVE-2025-59532
- 严重性：High，CVSS 8.6
- 影响：`@openai/codex` 0.2.0 至 0.38.0，修复版本 0.39.0；Codex IDE 扩展 0.4.11 及更早，修复版本 0.4.12

公告正文是：沙箱配置把模型生成的工作目录当成了可写根，从而可以在用户启动会话的文件夹之外写文件、执行命令。网络被禁用的那部分沙箱限制不受这次影响。Pillar 在时间线里把 GHSA-w5fx-fh39-j5rw 称为**先前那次**沙箱逃逸，又在开头用括号把同一个号写进了 git show。旧文沿用了开头那句混写。

git show 这次，截至 2026-11-02，公告列表里没有单独条目，也没有公开的 CVE 编号。能核对的材料是 Pillar 的文章和 Codex 后来的源码变更。不要再把 2025 年 9 月的 GHSA 抄成 2026 年 2 月这次补丁的编号。

## 攻击入口是文档里的提示注入

Pillar 第一次交给分拣时，模型拒绝了注入的指示，对方没能复现。随后用录像说明：同一种提示多跑几次，拒绝和照做都会出现。安全边界要按「模型照做了」来设计。模型这一次拒绝，只说明这一次的采样没有照做。

旧文里的这一点仍然成立，这里保留：命令名本身不决定安全，一次具体的调用才决定。`git show` 加一个提交号，是在读历史。`git show` 再带上能写文件的参数，就是另一次调用。只比较第一个单词的名单，分不开这两次。

## 现在怎么防

按 2026-11-02 能核对到的实现，分四层做，不要只留「把 CLI 升到 0.95.0」。

**版本。** v0.95.0 是 Pillar 写下的补丁版本。此后还有一次明确的收紧：更新日志里 Codex CLI 0.149.0（2026-08-20，对比范围 `rust-v0.148.0...rust-v0.149.0`）的完整列表包含：

- #39524 Stop treating Git commands as inherently safe
- #39630 Retire the untrusted approval policy

#39524 的提交说明写：仓库配置可以让只读的 Git 命令去执行 helper，所以参数本身不足以建立信任；Unix 和 Windows 上把 Git 命令移出 known-safe 分类。#39630 的提交说明写：移除 known-safe 命令白名单。2026-11-02 查看标签 `rust-v0.166.0`（对应 npm 上的 CLI 0.166.0）时，`codex-rs/shell-command/src/command_safety/` 里还有危险命令分类，已经没有 `is_safe_command.rs`。

这能说明「按命令名把 git show 当成已知安全」那条旧路径不在 0.166.0 的源码树里。本文没有登录，也没有让一次真实会话去跑 `git show --output`，所以不写「0.166.0 上这条命令一定会弹出审批」。沙箱仍然允许工作区内的常规命令自己跑；会不会把某次带 `--output` 的调用留在沙箱里，以你当前的权限模式和 Rules 为准。

**权限模式。** 官方现在的低风险组合是 `sandbox_mode = "workspace-write"` 加上 `approval_policy = "on-request"`，或对应的 `--sandbox workspace-write --ask-for-approval on-request`。Full access 是 `danger-full-access` 加 `never`，文件系统和网络边界都去掉。桌面端的 Ask for approval、Approve for me、Full access 怎么选，用 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。Approve for me 只是把符合条件的审批交给自动审阅，不扩大沙箱。

**Rules。** [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules) 控制的是 Codex **在沙箱外**可以跑哪些命令，官方标明为实验功能。`prefix_rule` 的 `allow` 是：在沙箱外运行，并且不询问。因此一条 `pattern` 只写到 `git` 或 `git show` 的 allow 规则，会把后面的参数一起带到沙箱外。不要用这种规则换取少点几次批准。需要收紧时，用 `forbidden` 或 `prompt`，并用 `codex execpolicy check` 看匹配结果。写法见 [Codex Rules](../11-自动化与高级工作流/13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)。

**Hooks。** [Hooks](https://learn.chatgpt.com/docs/hooks) 的 `PreToolUse` 可以在 Bash 等工具运行前拦截，明确的拒绝可以挡住这次调用。同一页也写明：回调报错、超时或格式不对时，这次 hook 会失败，工具调用仍可能继续。Hooks 是额外的检查，不是完整边界。配置和信任步骤见 [Codex Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。

另外两件和这次复盘直接相关的事：让 Codex 读陌生仓库的 README、文档和 issue 之前，把这些内容当成会下命令的输入；不要为了省事把不可信项目标成信任。

## 还有哪些宿主组件会执行项目文件

下面列出的是「沙箱外的程序会读项目文件」这一类，不是说每一项都有一条已公开的漏洞。

- Git 自身的配置和钩子。git show 那次走的就是 `.git/config` 里的外部 diff。仓库里的钩子脚本也在沙箱外运行。
- 编辑器的任务和已安装扩展。它们用你的用户权限读工作区。
- 桌面端内置浏览器。你点开的本地 HTML 不经过命令沙箱。2026-10-29 的 EMBRACE 报告里，Codex 这一侧截至 2026-11-02 还没有修复公告，见 [内置浏览器本地文件读取](./21-Codex内置浏览器本地文件读取风险-EMBRACE自查与防护.md)。

共同的用法是：不可信内容只进一个可丢弃的目录；这个目录不要被本机的自动任务、全局 Git 钩子和内置浏览器当成已经信任的项目。

## 和另外两篇怎么分工

[安全与风险边界](../02-核心概念与任务方法/05-安全与风险边界-到底该不该放手让它碰你的代码.md) 用来判断这次任务该不该放手，以及已经放宽之后怎么止损。[权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md) 讲预设、Auto-review 和 permission profiles 怎么配。本文只讲主机这一层：沙箱外的组件会执行 Codex 写下的文件，以及 2026 年那次白名单是怎么被参数绕开的。

## 常见问题

**只升到 0.95.0 就够了吗？** 那是 git show 这次的补丁版本。2026-11-02 的正式版是 0.166.0。日常保持在当前正式版，并检查自己有没有用 Rules 把 `git` 整体 allow 到沙箱外。

**公告页为什么只有一条？** 2026-11-02 的 API 结果就是一条 GHSA-w5fx-fh39-j5rw。没有第二条，不能解释成 git show 用了这个号。

**Windows 和 macOS 一样吗？** #39524 的说明写 Unix 和 Windows 都把 Git 移出了 known-safe。沙箱的实现仍然按系统不同：macOS 用 Seatbelt，Linux 用 bubblewrap，Windows 另有原生沙箱。边界以 [Sandbox](https://learn.chatgpt.com/docs/sandboxing) 为准。

## 参考资料

- Pillar Security，Ariel Fogel，2026-07-20：[GitPwned: Allowlist to RCE](https://www.pillar.security/blog/gitpwned-allowlist-to-rce)
- GitHub Advisory：[GHSA-w5fx-fh39-j5rw](https://github.com/openai/codex/security/advisories/GHSA-w5fx-fh39-j5rw)（2025-09-19，路径配置导致的沙箱绕过，不是 git show）
- OpenAI：[Sandbox](https://learn.chatgpt.com/docs/sandboxing)、[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)、[Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)、[Hooks](https://learn.chatgpt.com/docs/hooks)、[更新日志](https://learn.chatgpt.com/codex/changelog) 中的 Codex CLI 0.149.0
- 源码标签：`openai/codex` 的 `rust-v0.166.0`，路径 `codex-rs/shell-command/src/command_safety/`（2026-11-02 查看，无 `is_safe_command.rs`）
