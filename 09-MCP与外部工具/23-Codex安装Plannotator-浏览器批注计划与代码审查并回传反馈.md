---
id: codex-plannotator-plan-review
title: Codex 安装 Plannotator：在浏览器里批注计划和代码审查，用 Stop hook 把反馈送回 Codex
seo_title: Codex 安装 Plannotator：浏览器批注计划与代码，Stop hook 回传
description: Plannotator 是开源的本地评审界面：计划和代码 diff 在浏览器里划线批注，反馈直接回传给 Codex。本文按官方 README 说明在 Codex 里怎么安装、怎么靠 Stop hook 接管计划评审、怎么用 $plannotator-review 审代码，并写清实验性 hooks 和 curl 安装脚本的风险。
lede: 计划还停在终端里时，可以用浏览器把删改和评论画在原文上，再送回 Codex。Codex 这条链路走的是实验性 Stop hook，安装脚本是远程脚本。
url: /guides/codex-plannotator-plan-review
status: published
section: guides
category: G-extensions
topic: MCP与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 23
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-16
date_modified: 2026-11-16
verified_on: 2026-11-16
official_ref: https://learn.chatgpt.com/docs/hooks
keywords: [Codex Plannotator, plannotator-review, Codex Stop hook, 计划批注, 代码审查批注]
related: [codex-plan-mode, hooks-guide, codex-local-code-review]
howto: true
faq:
  - q: Plannotator 是 Codex 自带的 Plan 模式吗？
    a: 不是。Plan 模式是 Codex 自己的协作模式。Plannotator 是 backnotprop/plannotator 的第三方本地界面，Apache-2.0。它在 Codex 上靠实验性 Stop hook 在回合结束时读计划。
  - q: 可以照着 Claude Code 的 /plugin install 给 Codex 装吗？
    a: 不要。README 的安装表里，Claude Code、Copilot、Pi 各有自己的命令。Codex 一行写的是安装器自动配置 Stop hook，并附上 $plannotator-review、$plannotator-annotate、$plannotator-last。
  - q: 本文跑过安装脚本吗？
    a: 没有。curl 和 PowerShell 那两条都会执行远程脚本。2026-11-16 只下载阅读了 install.sh、install.ps1、仓库 README 和 apps/codex/README.md，没有执行。也没有浏览器评审截图。
  - q: 官方文档是不是写了 Windows 上禁用 Codex hooks？
    a: Plannotator 的 apps/codex/README 有这句。2026-11-16 抓取的 Hooks 文档正文里没有 “experimental”，也没有 “disabled on Windows”。安装脚本自己的注释写 Windows 上的 Codex hooks 仍是上游实验功能。两处不要合成一句官方结论。
---

# Codex 安装 Plannotator：在浏览器里批注计划和代码审查，用 Stop hook 把反馈送回 Codex

> 本文在线版：[codexguide.io/guides/codex-plannotator-plan-review](https://codexguide.io/guides/codex-plannotator-plan-review)

> 核对依据：第三方仓库 [backnotprop/plannotator](https://github.com/backnotprop/plannotator) 的 README、[apps/codex/README.md](https://github.com/backnotprop/plannotator/blob/main/apps/codex/README.md) 和 [v0.28.65 Release](https://github.com/backnotprop/plannotator/releases/tag/v0.28.65)，以及 [plannotator.ai](https://plannotator.ai)。2026-11-16 的 GitHub API：11,847 stars、1,083 forks，许可证 Apache-2.0，`archived` 为 false，`pushed_at` 为 `2026-11-16T01:07:48Z`。Release `v0.28.65` 的 `published_at` 是 `2026-11-15T00:07:22Z`。同一天下载阅读了 `https://plannotator.ai/install.sh` 和 `install.ps1`，**没有执行**。没有桌面端，没有浏览器评审，没有截图。未逐项实测，依据 README 和这两份脚本原文。

这是 **backnotprop** 的第三方项目，不是 OpenAI 功能。Codex 只是它支持的代理之一。README 列出的还有 Claude Code、Copilot CLI、Gemini CLI、OpenCode、Kiro、Droid、Amp、DeepSeek Harness 和 Pi。别的代理的安装步骤不要套到 Codex 上。

## 它解决什么问题

README 把它写成本地的浏览器评审界面：代理给出计划、HTML，或干完一轮时，浏览器打开，你划线、评论，反馈直接回到代理。官网首页的句子是：计划和代码 diff 在你执行或提交之前先过目，反馈送回代理。首页同时写它本地运行、免费且开源。

Codex 能用的三块，以 `apps/codex/README.md` 为准：

- **计划评审。** 不另敲命令。回合结束时，Stop hook 读当前 rollout transcript，取出最新计划，打开计划评审界面。
- **代码审查。** `!plannotator review`，或技能 `$plannotator-review`。
- **文档和上一条回复。** `!plannotator annotate`、`!plannotator last`，对应 `$plannotator-annotate` 和 `$plannotator-last`。

适合计划已经写出来、你想在原文上标「删掉这段」「这里改成那样」，或者想在提交前对 diff 做划线评论的人。只想让 Codex 先问清楚再动手，用 Codex 自己的 Plan 模式就够。只想要一份问题清单、不需要浏览器批注，用本地 `/review`。

## 和 Codex 自带 Plan 模式、/review 的分工

| 做什么 | 用哪个 | 结果去哪 |
| --- | --- | --- |
| 先问清需求，在终端里确认计划再改代码 | [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md) | Codex 自己的计划块和「Implement this plan?」弹窗 |
| 把计划或 diff 画在浏览器里，评论回传给这一轮 | Plannotator | Stop hook 的续写，或审查命令的标准输出 |
| 对未提交改动、分支或某个 commit 要一份问题报告 | [本地 /review](../05-Git协作与代码审查/07-Codex本地代码审查-review命令与codex-review.md) | 审查报告。官方写明审查不改工作区 |

Plannotator 不进入 Plan 模式，也不代替 `/review`。`apps/codex/README.md` 写明：因为用的是 `Stop`，评审发生在 Codex 把这一轮画出来之后，不是在一个专门的 `ExitPlanMode` 拦截点。你拒绝计划时，它返回续写反馈，让 Codex 在同一回合里改计划，并在后续修订之间显示版本历史和 diff。批准则让这一回合保持结束。

README 还写了 Inbox、Obsidian、Bear、GitHub 分享和工作区等产品。那些不是 Codex 计划评审的必经步骤。本文不展开。

## 安装

官方安装命令是管道执行远程脚本：

```bash
# macOS / Linux / WSL
curl -fsSL https://plannotator.ai/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://plannotator.ai/install.ps1 | iex
```

先读脚本再运行，或者按 `apps/codex/README.md` 手工写配置。不要在没读过内容的时候把上面两条直接交给 shell。脚本会从 GitHub Releases 下载二进制。README 写完整安装还可能访问 GitHub、Ataraxy-Labs/sem，以及 npm。本文没有执行任何一条。

2026-11-16 读到的 `install.sh` 在检测到 Codex（PATH 上有 `codex`，或 `CODEX_HOME`、否则 `~/.codex` 里已有用户配置）且没有 `--skip-codex` 时，会自己写两处：

- `config.toml` 里加上 `[features]` 和 `hooks = true`。文件里已经有内联的 `features =` 时，脚本不改文件，只把这两行打印出来让你手工加。
- `hooks.json` 里写一个 `Stop` hook。新建文件时，`command` 是安装目录下的 `plannotator` 绝对路径，`timeout` 是 `345600`。已有文件时，用 node 合并；找不到 node 就不改，并打印要你手工补上的命令和 timeout。

`apps/codex/README.md` 的手工配置是：

```toml
[features]
hooks = true
```

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "plannotator",
            "timeout": 345600
          }
        ]
      }
    ]
  }
}
```

同一页还有三条说明：Codex 会加载当前配置层旁边的 `hooks.json`，全局 `~/.codex` 或仓库里的 `.codex` 都可以；给 Codex 桌面端用时，`command` 最好写成绝对路径，因为桌面端启动的进程不一定继承 shell 的 `PATH`；改完 hooks 后重启 Codex 桌面端。

`345600` 是 README 和 `install.sh` 里的原值。本站 [Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md) 按官方文档把省略时的 timeout 理解成秒。若单位仍是秒，这是一段很长的等待，用来让浏览器评审保持打开。本文没有跑过这个 hook，不把「一定会等到这个上限」写成实测。

只想要二进制、不要它改配置时，README 写了 `--minimal`（或环境变量 `PLANNOTATOR_MINIMAL=1`），装到 `~/.local/bin`，跳过 skills、hooks 和每个代理的配置。那样就没有自动的计划评审，需要再按上面的手工配置补上。

### 原生 Windows

README 的 Codex 行写：macOS、Linux 和 WSL 上，计划评审由实验性 `Stop` hook 自动启用；原生 Windows 上 Codex hooks 仍是实验性的，安装脚本只打印手工步骤。

`install.ps1` 的注释写：在 Windows 安装器里自动改 Codex 家目录之前，上游的 Codex hooks 仍当作实验功能，所以这条路径不自动写入。检测到 Codex 时，它打印的是：

1. 在 `config.toml` 里写 `[features]` 和 `hooks = true`；
2. 在 `hooks.json` 里加一个运行 `plannotator.exe` 的 Stop hook。

这段打印**没有**带上 `timeout: 345600`，也没有给出完整 JSON。完整字段以 `apps/codex/README.md` 为准，并把 `command` 换成脚本打印出来的那个 `plannotator.exe` 路径。`--skip-codex` 会连这段手工说明也不打印。本文没有 Windows 环境，没有运行 `install.ps1`。

`apps/codex/README.md` 还写：「This currently depends on Codex hooks, which are experimental and disabled on Windows in the current official docs.」2026-11-16 抓取的 [Hooks](https://learn.chatgpt.com/docs/hooks) 正文里，检索不到 experimental，也检索不到 disabled on Windows。该页有 Windows 专用的 `commandWindows`。同一天的 [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) 把 `features.hooks` 写成从 `hooks.json` 或内联 `[hooks]` 加载生命周期 hook，`features.codex_hooks` 是已废弃的别名，没有写 Windows 上禁用。因此本文不把「官方文档已在 Windows 上关闭 hooks」当成事实。实验性这个判断，来自 Plannotator 的 README 和它自己的安装脚本。

hooks 写好之后仍要按 Codex 的规则信任。非托管 hook 要在 `/hooks` 里按当前内容审核，见 [Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。安装器如果直接改了 `hooks.json`，哈希会变，旧的信任不会自动沿用。

## 计划评审怎么跑

`apps/codex/README.md` 的顺序是：

1. hooks 已经启用。
2. Codex 某一回合结束，并且这一回合里有计划。
3. Plannotator 读当前 rollout transcript，抽出最新计划，打开平时的计划评审界面。
4. 你批准：这一回合保持完成。你拒绝并写下反馈：Stop hook 返回续写理由，Codex 在同一回合里改计划。修订会留下版本历史和 diff。

它不负责生成计划。计划仍由 [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md) 或你自己的提示产生。Plannotator 接在回合停下来之后。

仓库里有一条本地端到端脚本 `./tests/manual/local/test-codex-plan-review-e2e.sh`。README 写它使用临时 `HOME`、示例 Git 仓库和仓库内的包装命令，避免改你已经装好的 Codex。本文没有克隆后运行这条脚本。

## 代码审查与文档批注

README 的 Commands 一节写明，在 Codex 里把斜杠命令换成 `!plannotator …`（例子是 `!plannotator review`），或使用 `$plannotator-*` 技能。`apps/codex/README.md` 的用法是：

```text
!plannotator review
!plannotator annotate path/to/file.md
!plannotator last
```

`review` 抓取当前 git diff，打开浏览器，等你提交批注，再把反馈打到标准输出。`annotate` 打开指定的 Markdown。`last` 打开代理最近一条回复。根 README 里给其他代理写的 `/plannotator-review <github-pr-url>` 这类斜杠形式，不要原样敲进 Codex。Codex 的对应入口是上面的 `!` 或 `$`。

安装脚本在没有 `--skip-skills` 时，会把三个技能装进 `~/.agents/skills/`，名字是 `$plannotator-review`、`$plannotator-annotate`、`$plannotator-last`。脚本自己的结束语写：Stop hook 不依赖这些技能；跳过技能时，计划评审的 hook 仍可配置，只是没有这三项技能。本文没有安装，所以没有在 `~/.agents/skills` 里看到文件。

本地 `/review` 产出的是 Codex 的审查报告。Plannotator 的代码审查是浏览器里的划线批注，反馈回到当前代理。两件可以先后做，不是同一个命令。

## 数据与安全

README 的 Privacy 一节写：不收集用量遥测或分析；计划、diff、批注、草稿、历史和配置默认留在本地。下面几条是它同时写明的网络行为，本文没有抓包：

- 计划评审、批注、归档、分享页和代码审查界面在加载时会向 GitHub 查最新版本。README 称这次请求不发送计划或审查内容，但 GitHub 会收到一次普通请求，而且目前没有关闭这项检查的设置。
- 本地 Git 审查可能对配置好的 `origin` 做 `git ls-remote`，用来看默认分支和过期的基线，不发送本地 diff。可用 `plannotator review --no-git-remote-check`、`PLANNOTATOR_GIT_REMOTE_CHECK=0`，或 `~/.plannotator/config.json` 里的 `{ "gitRemoteCheck": false }` 关掉。
- 批注一个 URL 时会去抓那个站点。默认经 Jina Reader。
- 分享才把内容送出去。小的 Markdown 放在 URL 片段里，片段不加密。更大的内容和原始 HTML 先用 AES-256-GCM 加密再上传，密钥留在 URL 片段里。拿到完整链接的人可以解密。`PLANNOTATOR_SHARE=disabled` 可以关掉分享。
- Workspaces 是另一个托管产品，不适用「内容只在本地」这句。

`PLANNOTATOR_BROWSER` 设为 `none` 时不打开浏览器，会话 URL 仍会打印。远程会话可以用 `PLANNOTATOR_REMOTE` 和 `PLANNOTATOR_PORT`。这些是 README 的环境变量表，本文没有设过。

Stop hook 会在回合结束时启动本地程序，并读 rollout transcript。这和 `notify` 只是收一条「回合结束了」不同。信任之前先看 hook 的 `command` 是不是你预期的 `plannotator` 路径。

## 限制

- 未逐项实测。没有执行安装脚本，没有打开浏览器评审，没有看到批准或拒绝之后的 Codex 续写。
- 计划评审依赖 Codex 的 Stop hook。Plannotator 把它称为实验性。官方 Hooks 页当天的正文没有使用这个词，也没有写 Windows 上禁用。原生 Windows 的安装器不自动写入配置。
- 评审在回合已经渲染之后，不是在 Plan 模式弹出「Implement this plan?」的那一刻。
- 管道安装会改 `config.toml` 和 `hooks.json`。已有自定义的 Plannotator hook 时，`install.sh` 的合并逻辑会留下含 `plannotator` 字样但不属于它管理的命令，不覆盖。
- README 里 Claude Code 2.1.287 以后「不再让 Claude 等待」的那段，只写给 Claude Code。不要套到 Codex。

## 升级与卸载

README 写更新就是再跑一次安装器，用来更新二进制和斜杠命令。Codex 没有单独的 `codex plugin update` 行。再跑安装器会再次碰到远程脚本，仍应先看 diff 或固定版本。固定版本的写法在 README 里是：

```bash
curl -fsSL https://plannotator.ai/install.sh | bash -s -- --version vX.Y.Z
```

把 `vX.Y.Z` 换成你要的标签，例如当时的 `v0.28.65`。README 称 `--version` 只跳过用 GitHub API 解析「最新版」，不会跳过下载发行包本身。可选的 `--verify-attestation` 需要 `gh`，但不需要登录。本文没有做校验。

卸载：

```bash
plannotator uninstall
plannotator uninstall --purge
```

README 写默认卸载去掉它识别出的已安装组件，保留本地计划、历史、草稿和设置。`--purge` 还要你输入 `purge`，并说明这些数据只在本地，删了不能从 Plannotator 的服务器找回。它也写了覆盖不到的情况：你自己加的文件、装在单个项目里的插件、它不认识的路径。本文没有执行卸载。卸完后看 `hooks.json` 里是否还留着 Stop hook，以及 `/hooks` 里的信任是否还指向已经删掉的二进制。

## 常见问题与参考资料

**装完没有弹出浏览器。** 先确认 Codex 家目录里的 `hooks.json` 有这条 Stop hook，`[features] hooks = true` 没有被关掉，并且 `/hooks` 里这份内容已信任。`apps/codex/README.md` 写只有回合结束且带着计划时才会打开。`PLANNOTATOR_BROWSER=none` 会故意不打开，只打印 URL。这些都还没在本文的环境里走通。

**反馈没有回到 Codex。** 拒绝计划时，README 写的是 Stop 的续写理由，不是一封另开的新会话。批准则不会续写。代码审查的 `!plannotator review` 把反馈打到标准输出，那是另一条路径。

**和 Plan 模式的弹窗叠在一起。** Plan 模式的「Implement this plan?」是 Codex 自己的界面。Plannotator 在回合停止之后才读 transcript。想在浏览器里改计划，就用 Plannotator；想在终端里选「清空上下文后执行」，用 [Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md) 的弹窗。

- [backnotprop/plannotator](https://github.com/backnotprop/plannotator)
- [apps/codex/README.md](https://github.com/backnotprop/plannotator/blob/main/apps/codex/README.md)
- [v0.28.65 Release](https://github.com/backnotprop/plannotator/releases/tag/v0.28.65)
- [plannotator.ai](https://plannotator.ai)
- [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
- [Codex Plan 模式](../02-核心概念与任务方法/08-Codex-Plan模式-先出计划再动手.md)
