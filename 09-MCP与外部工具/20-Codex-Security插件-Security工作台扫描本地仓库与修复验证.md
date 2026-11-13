---
id: codex-security-plugin
title: Codex Security 插件教程：在 Security 工作台扫描本地仓库、生成补丁并验证修复
seo_title: Codex Security 插件：Security 工作台扫描、修复与验证
description: Codex Security 插件在 Codex 里加了一个 Security 工作台，可以扫描整个仓库或只扫最近的改动，再对问题生成补丁、应用并验证。本文按官方文档说明安装方式、三种扫描怎么选、SECURITY.md 怎么提供上下文、输出文件在哪里，以及插件、CLI 和 Cloud 版的分工。
lede: 第一次本地扫描用插件：Security → Scans → + Scan。扫描不改代码；生成补丁也不改代码，点 Apply patch 才会动你的工作区。
url: /guides/codex-security-plugin
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 20
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-10
date_modified: 2026-11-10
verified_on: 2026-11-10
models: [gpt-5.6-sol]
official_ref: https://learn.chatgpt.com/docs/security/plugin
keywords: [Codex Security 插件, Security 工作台, security-scan, security-diff-scan, fix-finding, SECURITY.md]
related: [codex-security-cli, codex-chajian-rukou-yu-gongzuoliu, codex-daybreak-blue]
faq:
  - q: 装了插件就能扫描吗？
    a: 还要有 Codex Security 的访问权限。官方总览页写明，使用 OpenAI 推理的扫描需要 Codex Security 访问权限；工作区里显示 Disabled by admin 时，要让工作区所有者检查插件权限。
  - q: 插件和 npm 上的 @openai/codex-security 是一回事吗？
    a: 不是。官方文档写明两者版本分开：独立的 @openai/codex-security 包自带一份插件，更新这个包不会更新 Codex 里从 marketplace 装的插件。
  - q: Verify fix 通过了，问题会自动关闭吗？
    a: 不会。官方 Fix findings 页写明，验证会记录证据，但不会自动关闭 finding；要你看完命令、结果和剩下的证明缺口后，手动关闭或保持打开。
  - q: 本文跑过一次扫描吗？
    a: 没有。写作环境没有 ChatGPT 桌面 App，也没有 Codex Security 访问权限。文中的步骤、命令和输出文件名都来自官方文档，没有截图和扫描结果。
---

# Codex Security 插件教程：在 Security 工作台扫描本地仓库、生成补丁并验证修复

> 本文在线版：[codexguide.io/guides/codex-security-plugin](https://codexguide.io/guides/codex-security-plugin)

> 核对依据：官方文档 [Codex Security](https://learn.chatgpt.com/docs/security)、[Plugin quickstart](https://learn.chatgpt.com/docs/security/plugin)、[Workbench](https://learn.chatgpt.com/docs/security/plugin/workbench)、[Run a security scan](https://learn.chatgpt.com/docs/security/plugin/scans)、[Deep scans](https://learn.chatgpt.com/docs/security/plugin/deep-scans)、[Review code changes](https://learn.chatgpt.com/docs/security/plugin/code-changes)、[Fix findings](https://learn.chatgpt.com/docs/security/plugin/fix-findings) 和 [Plugin changelog](https://learn.chatgpt.com/docs/security/plugin/changelog)（最新说明为 0.1.32），2026-11-10 核对。写作环境没有 ChatGPT 桌面 App，也没有 Codex Security 访问权限，**本文没有截图，也没有真实的扫描结果**；界面名称按官方英文文档写。

Codex Security 是 OpenAI 的代码安全审查功能，会给出带证据的漏洞报告和修复建议。它有四种用法：Cloud、插件、CLI 和 SDK。这篇讲**插件**：在 Codex 桌面端或 Codex CLI 里扫描本地仓库，然后在 Security 工作台里一条条处理问题。

## 先看结论

| 用法 | 适合 | 本站文章 |
|---|---|---|
| **Codex Security 插件** | 在 Codex 里扫本地仓库，交互式处理问题。官方建议第一次本地扫描用它 | 本文 |
| Codex Security CLI | 在终端里重复扫描，或加进 CI | [Codex Security CLI 本地扫描仓库漏洞](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md) |
| Codex Security SDK | 在自己的应用或开发工具里调用扫描 | 官方 [SDK guide](https://learn.chatgpt.com/docs/security/sdk) |
| Codex Security Cloud | 扫描已连接的 GitHub 仓库、监控新提交（另一个插件，研究预览） | 官方 [Cloud setup](https://learn.chatgpt.com/docs/security/setup) |

插件里有三种扫描：

- **Codebase 标准扫描**：扫整个仓库或某个目录，第一次用这个。
- **Codebase + Deep scan**：对同一范围做多次独立扫描再合并结果，更费时间和 token。
- **Changes**：只审查一组改动（未提交的改动、某个 commit，或一段 base 到 head 的范围），不能开 Deep scan。

## 开始前：访问权限和版本

- **访问权限**：使用 OpenAI 推理的扫描需要 Codex Security 访问权限。插件 0.1.24 起会在扫描前检查 Daybreak 访问权限，没有权限时显示申请链接。管理型工作区里安装时显示 “Disabled by admin”，要让工作区所有者检查插件权限。
- **模型**：官方建议用 `gpt-5.6-sol` 加 `xhigh` 推理强度，扫描质量最好（2026-11-10 文档）。
- **版本**：Codex 和插件的版本是分开的。在 Codex CLI 里查看：

```bash
codex --version
codex plugin list --json
```

在 `installed` 列表里找到 Codex Security，扫描前把两个版本号记下来，出问题时方便反馈。npm 上独立的 `@openai/codex-security` 包自带一份插件，**更新那个包不会更新 Codex 里的插件**。

更新插件后要开一个新对话（CLI 里 `/new`）才会加载新的技能和工具。

## 安装插件

**桌面端**

1. 在 ChatGPT 桌面 App 里切到 **Codex**。
2. 打开 **Plugins**，搜索 **Codex Security** 安装。
3. 确认插件已启用，侧边栏会出现 **Security**。

侧边栏没有 Security 时，先确认选的是 Codex、插件已启用，再更新 App 和插件，最后确认工作区管理员允许这个插件。

**CLI**

1. 在要扫描的仓库目录里启动 `codex`。
2. 输入 `/plugins`，搜索 Codex Security，选择 **Install plugin**。
3. 输入 `/new` 开一个新对话。

在 CI 这类非交互环境里，官方给的安装命令是 `codex plugin add codex-security@openai-curated`。插件和其他插件的管理方式，见 [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)。

## 第一次扫描：Codebase 标准扫描

**桌面端步骤**

1. 侧边栏选 **Security**，打开 **Scans**，点 **+ Scan**。
2. 选一个已有仓库，或选别的文件夹。选 **Codebase**，**Deep scan 保持关闭**。
3. **Scan area** 选整个仓库或某个目录。确认分支和 revision 是你要扫的那份代码。
4. 选模型和推理强度。需要说明攻击入口、敏感区域时，打开 **Additional context** 写进去。
5. 点 **Start scan**。扫描过程中可以点 **View activity** 打开执行扫描的 Codex 任务；要中途停止，打开这次扫描点 **Stop scan**。离开工作台再回来，已保存的扫描不会丢。

monorepo 建议按服务或包选一个目录扫，那样边界和负责人都清楚。

**在对话里扫描（桌面端或 CLI）**

```text
Run a Codex Security scan on this repository.
```

或者直接点名技能，并限定目录：

```text
Use $codex-security:security-scan to scan only services/billing in this repository for security vulnerabilities.
```

扫描本身**不会修改源码**。

## 只扫改动：Changes

改了一批代码、准备提 PR 前，可以只审这组改动。Codex 会看每个改动的源码文件和直接相关的代码，不会扩成整库审计。

1. **Security** → **Scans** → **+ Scan**，选仓库后选 **Changes**。
2. 在 **Changes to review** 里选：`Uncommitted changes`（当前工作区）、最近一个 commit，或一对 base 和 head revision。
3. 确认摘要描述的是你想审的改动，点 **Start scan**。

在对话里也可以：

```text
Use $codex-security:security-diff-scan to review the changes from origin/main to HEAD for security regressions. Focus on authentication, authorization, input handling, filesystem access, network requests, and secrets.
```

Codex 不会替你切分支。要审的 revision 本地没有时，先 fetch。

## 用 SECURITY.md 和 AGENTS.md 提供上下文

- **SECURITY.md**：放在仓库根目录，写威胁模型、安全不变量、哪些算有效问题、哪些排除、严重程度怎么判断。子目录可以放自己的 SECURITY.md，冲突时**离代码最近的文件优先**。Codex Security 把它当作策略上下文，不当作可执行的指令。
- **AGENTS.md**：写构建和验证命令等仓库说明，扫描验证时会用到。写法见 [AGENTS.md 怎么写](../10-配置模型与权限安全/07-AGENTS.md怎么写-项目规则继承关系与验收标准.md)。

一个最小的 SECURITY.md 例子：

```markdown
# Security policy for scanning

- 攻击者可控的输入：所有 /api/* 请求体和查询参数、上传的文件。
- 不变量：普通用户只能读写自己 org_id 下的数据。
- 不报告：tests/ 和 scripts/dev/ 下的代码，只在本地开发时运行。
- 严重程度：能跨租户读数据算 high 以上。
```

## 看结果：按顺序读

扫描完成后，桌面端在 **Scans** 里保留结果；**Findings** 汇总所有仓库和扫描的问题，**Repositories** 看某个仓库的扫描历史。打开一个 finding，**Summary** 看详情，**Patch** 用来修复。

官方建议的阅读顺序：

1. 确认扫描目标、revision 和范围。
2. 看审查过的部分，以及被推迟或需要后续跟进的部分。
3. 对每个 finding，看攻击者怎么到达这段代码、哪个控制失效、证据支持多大的影响，再看验证方法和未解决的问题。
4. 证据不足的继续查；能说明为什么不适用的，就关掉并留下理由。
5. 挑**一个**你认可的 finding 再开始修。

注意：扫描完成不等于覆盖完整，被推迟的区域即使扫描成功也要看。

**输出文件**：CLI 里用对话中给出的扫描目录。`report.md` 是可读报告；`findings/` 下的详细漏洞报告和 `hardening/` 下的加固建议是可选输出，需要时再让它生成；目录里还有 `scan-manifest.json`、`findings.json`、`coverage.json` 给工具和自动化用。分享或归档时把整个目录放一起，报告里的链接才不会断。

## 修复：生成补丁、应用、验证

在桌面工作台里：

1. 打开一个认可的 finding，切到 **Patch**，点 **Generate patch**。Codex 会在可行时复现问题，写出补丁文件，**这一步不改你的工作区**。
2. 审阅补丁：只改了该改的地方，没有顺手重构，也没有削弱安全控制。
3. 点 **Apply patch**，补丁才会应用到工作区。再看一遍工作区 diff。
4. 点 **Verify fix**。Codex 会重跑原来的复现或攻击检查；能跑回归测试时，确认测试在修复前失败、修复后通过；跑不了的会记录验证缺口。
5. **手动关闭**：验证不会自动关闭 finding。看完命令、结果和剩余缺口后，写明理由关闭，或者保持打开。

在对话里修：

```text
Use $codex-security:fix-finding to fix finding <finding-id> from <report-path>. Verify the issue against this checkout, fix it, and test the original failure and legitimate behavior. Record any verification you couldn't complete.
```

这句话等于授权 Codex 改工作区。CI 里非交互地修，官方示例用 `codex exec --sandbox workspace-write` 加同样的提示，并建议每个 finding 用单独的 checkout 或 job。修好的改动照常走代码评审再合并。

## 首次扫描当基线

官方建议把第一次扫描当作基线：记下仓库 revision、插件版本、模型和推理强度。之后代码或安全控制变了，再扫一次对比。如果你拿一个已知问题测试扫描效果，记下有没有提前告诉 Codex。

## 常见问题

**装了插件就能扫描吗？**

还需要 Codex Security 访问权限。工作区里显示 Disabled by admin，找工作区所有者。插件 changelog 写明，从 0.1.24（2026-09-09）起，用 ChatGPT 登录的桌面端和 CLI 会在扫描前检查 Daybreak 访问权限，没有权限时显示申请链接；只用 API key 的会话无法核实账号权限。申请和排障见 [Codex Daybreak Blue 申请开启与排障](../10-配置模型与权限安全/10-Codex-Daybreak-Blue申请开启与排障.md)。

**插件和 npm 上的 @openai/codex-security 是一回事吗？**

不是。两者版本分开，更新 npm 包不会更新 Codex 里的插件。

**Verify fix 通过了，问题会自动关闭吗？**

不会，要手动关闭。

**本文跑过一次扫描吗？**

没有。写作环境没有桌面 App 和 Codex Security 权限，文中内容都来自官方文档。

## 相关阅读

- [Codex Security CLI 本地扫描仓库漏洞](../06-测试调试与质量保障/02-Codex-Security-CLI本地扫描仓库漏洞.md)
- [Codex 插件入口与工作流](../08-插件工作流/04-Codex插件入口与工作流.md)
- [Codex Daybreak Blue 申请开启与排障](../10-配置模型与权限安全/10-Codex-Daybreak-Blue申请开启与排障.md)
