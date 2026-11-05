---
id: codex-local-thread-memory
title: Codex 本地线程内存优化：长对话不再越跑越占 RAM
seo_title: Codex 本地线程内存过高：公告、核对与仍上涨时的排查
description: 本地线程变长后，即使用户没有再启动其他进程，Codex 的内存占用也会升高。本文根据工程师公告说明问题范围和修复方向，并给出升级后如何确认内存回落、仍在上涨时的排查顺序。公告没有写明修复版本号。
lede: 先看这条本地线程自己占了多少内存。磁盘被崩溃转储塞满、或旁边又拉起一批进程，是另外的问题。
url: /guides/codex-local-thread-memory
status: published
section: guides
category: K-troubleshooting
topic: 故障排查与恢复
content_type: 排障
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 基础
order: 6
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-05
date_modified: 2026-11-05
verified_on: 2026-11-05
official_ref: https://x.com/ajambrosino/status/2118028125707923513
keywords: [Codex 内存占用, Codex local threads, Codex RAM, 长对话卡顿, 本地线程]
related: [desktop-crashpad-disk-space, codex-doctor]
faq:
  - q: 这次修复对应哪个 App 或 CLI 版本？
    a: 2026-11-04 的公告正文和图上都没有版本号。2026-11-05 查询 npm 上 @openai/codex 的 latest 仍是 0.166.0，这份正式版说明里也没有这条内存修复。升级到当前客户端之后，用同一条长本地线程重新看内存，不要用某个猜测的版本号当作已修复的证据。
  - q: 压缩上下文（/compact）能代替这次修复吗？
    a: 不能据此下结论。/compact 处理的是对话窗口里的上下文长度。这篇公告说的是本地线程变长之后的进程内存。两者可以同时存在，本文没有证据表明只做一次 compact 就等于装上了这次修复。
  - q: 云端任务也会按这张图涨内存吗？
    a: 公告点名的是 local threads。图的纵轴是本机整个应用的物理内存。云端任务跑在远端环境里，不在这张图的测量范围内。
---

# Codex 本地线程内存优化：长对话不再越跑越占 RAM

> 本文在线版：[codexguide.io/guides/codex-local-thread-memory](https://codexguide.io/guides/codex-local-thread-memory)

> 核对依据：Codex 工程师 Andrew Ambrosino（@ajambrosino）2026-11-04 17:10 UTC 的帖文 [we're giving you some RAM back](https://x.com/ajambrosino/status/2118028125707923513)，以及 [@OpenAIDevs 对同一条说明的转发](https://x.com/OpenAIDevs/status/2118095428868862153)。帖文附有一张修复前后的内存曲线。本文照着这张图描述坐标和曲线形态，没有在本机复测，也没有从 npm 或 changelog 里找到对应的修复版本号。

适合已经把一条 Codex 本地线程用得很长、并且感觉整机越来越吃内存的人。读完可以分清：这是线程本身变长带来的内存，还是崩溃转储、子进程或云端环境的另一类占用。

## 先看结论

2026-11-04，@ajambrosino 写道：

> we're giving you some RAM back. local threads could grow memory usage as they became long, even without starting other processes. @btraut declared war on the problem.

翻译过来的产品事实是：他们在把内存还给用户。本地线程变长之后，内存占用会上去，即使这些线程没有再去启动其他进程。Brent Traut（@btraut）负责处理这个问题。@OpenAIDevs 转发了同一条说明。

帖文没有写 App 构建号、CLI 版本或操作系统。附图也没有这些信息。因此本文只说「官方已经宣布本地线程的这块内存问题有了修复」，不写一个具体的修复版本。

## 官方图上能读到什么

原帖附图的坐标是：

- 纵轴：**Whole-app physical memory (GiB)**，刻度到 6。
- 横轴：**Replies in one turn**，标出了 0、8,192、16,384、24,576、32,768。

图上有两条曲线：

- **Before**：从不到 2 GiB 爬升，在大约 8,192 条回复附近到达 6 GiB 的刻度后结束。
- **After**：在整段横轴上停在 2 GiB 下方，并一直画到 32,768 条回复。

这是公告作者附上的对比，不是本文的实验室测量。图没有给出机器配置、采样间隔和统计方法。读它时采用的判断是：修复前，单轮回复变多时，整个应用的物理内存会升到数 GiB；修复后的曲线在同样的横轴上保持在 2 GiB 以下。你自己的机器不会复现成同一条线。

帖文正文说的是 local threads 变长；图的横轴写的是 one turn 里的回复数。两者都来自同一条帖，本文不把它们改写成一个更窄的定义。

## 谁会碰到

会碰到的是把**本地线程**越用越长的人。公告强调的触发条件是线程变长本身，即使没有额外启动别的进程，内存也会涨。

下面这些情况要分开看，它们可以同时发生，但不是这条公告测量的对象：

| 你看到的现象 | 更贴近哪一类 | 下一步 |
| --- | --- | --- |
| 一条本地长线程开着，应用内存随回复变多往上走，旁边没有新的编译器、浏览器或 Git 进程 | 公告描述的本地线程问题 | 升级客户端后再量一次 |
| 磁盘突然少掉几十到几百 GB，应用目录里 pending 一类转储很大 | 崩溃转储占磁盘 | [Crashpad 排查](./02-Codex桌面端占满磁盘-Crashpad崩溃转储排查与清理.md) |
| 同时开了很多子进程，风扇和 CPU 一起上去 | 线程之外的进程 | 先看是谁启动的，再决定要不要停 |
| 任务在云端环境里跑 | 远端计算 | 本机活动监视器量不到那台机器的内存 |

仓库很大、索引很重，仍然可能让别的工具吃内存。那是下一节的排除项。这条公告把原因放在本地线程变长，而不是放在「项目文件总体积」上。

## 升级之后怎么确认内存回落

公告没有给出版本号，也没有写「安装某一次 npm 包即可」。2026-11-05 用 `npm view @openai/codex version` 查到的 latest 是 **0.166.0**。[CLI 0.166.0 更新日志](https://learn.chatgpt.com/docs/changelog)（2026-10-29）里有 `codex queue --resume`、`codex doctor --network-only` 等条目，没有这条本地线程内存修复。桌面端的更新通道和 npm 上的 CLI 版本不是同一个号码本。

可以做的核对是：

1. 用你平时的更新入口把 Codex / ChatGPT 桌面端更新到当前提供的版本。更新完成后看「关于」里的版本号，把它记在自己的笔记里，供前后对比。本文不指定该填哪一个号。
2. 完全退出应用后重新打开，避免旧进程还留在内存里。
3. 打开**同一条**此前变长的本地线程。用系统工具看整个应用的物理内存：macOS 活动监视器、Windows 任务管理器，或 Linux 上你用来看进程驻留内存的工具。
4. 让这条线程再走一段回复，记录打开时和又一批回复之后的内存。对照公告图的形态：修复后的曲线不应随着回复数爬到数 GiB。
5. 同时看进程列表。公告说问题发生时可以没有其他新进程。若你这边同时出现大量 `git`、语言服务器、浏览器或 MCP 进程，先把它们记下来，内存变化就不能只算在「线程变长」上。

一次对比就够用来判断「有没有从爬升变成持平」。不要为了凑满图上的 32,768 条回复去制造超长线程。

## 还在涨时，按这个顺序查

内存更新之后仍然明显爬升，按成本从低到高排除。每一步都先观察，再决定要不要删东西。

1. **确认量的是当前这次启动的应用。** 退出残留进程后再读数。多个窗口会叠加内存，把窗口数一并记下。
2. **看有没有新进程。** 公告针对的是「没有启动其他进程也会涨」。有新进程时，先确认这些进程是线程里的命令、MCP，还是系统自己的服务。
3. **查磁盘上的崩溃转储。** 内存高和磁盘满可以同时出现，原因不同。macOS 上 Crashpad pending 的核对方见 [桌面端占满磁盘](./02-Codex桌面端占满磁盘-Crashpad崩溃转储排查与清理.md)。那篇处理的是磁盘上的转储文件，不是这张内存曲线。
4. **跑一次 `codex doctor`。** 它检查安装、配置、登录、网络和后台服务，不会自动把内存改回去。用法见 [Codex doctor 自检](./04-Codex-doctor自检-安装配置登录与网络排查.md)。
5. **把新任务放到新的本地线程。** 这是使用上的隔离：新工作不必继续堆在已经很长的那条线程里。它不能代替第 1 步的客户端更新。长任务怎么拆开，见 [Codex 长任务工作流](../11-自动化与高级工作流/05-Codex长任务工作流.md)。

`/compact` 用来缩短对话里保留的上下文。它可以让后续回合少带一些历史，本文没有把它写成这次内存修复的替代品。

清理会话文件、删掉整个应用目录或结束系统进程，都不在这条公告的处理步骤里。磁盘清理只按 Crashpad 专文里已经写明的范围做。

## 和云端线程的差别

公告和附图都落在本机应用上：local threads，纵轴是整个应用的物理内存。云端线程的计算发生在云端环境，本机活动监视器里的数字对不上那张图。

本地长线程仍然值得单独看，是因为即使用户没有再启动工具进程，客户端自己也会把内存抬上去。修复宣布之后，判断标准是：更新客户端，再打开这条本地线程，看物理内存是否还随回复数爬升。

## 参考资料

- [Andrew Ambrosino：we're giving you some RAM back](https://x.com/ajambrosino/status/2118028125707923513)（2026-11-04）
- [OpenAIDevs 转发](https://x.com/OpenAIDevs/status/2118095428868862153)
- [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog)（对照用：2026-10-29 的 CLI 0.166.0 条目没有这条内存修复）
