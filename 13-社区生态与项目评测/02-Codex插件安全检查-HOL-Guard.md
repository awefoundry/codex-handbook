---
id: codex-plugin-security-hol-guard
title: Codex 插件安全检查（2026-11 更新）：HOL Guard 拦截高风险操作，plugin-scanner 发布前扫描
seo_title: Codex 插件安全检查：HOL Guard 与 plugin-scanner 用法
description: HOL Guard 是开源的本地 AI 代理安全工具，接入 Codex 后在执行命令、调用 MCP 前做检查；plugin-scanner 在发布插件前打分。本文按 3.59.0 重写安装、接入、防护档位和审批，附 plugin-scanner 扫 Expo 插件和 command test 的真实输出。
lede: 装插件之前用 plugin-scanner 扫一遍，跑 Codex 时让 HOL Guard 在执行前把关。两者都是第三方开源工具，不能代替你自己看代码。
url: /guides/codex-plugin-security-hol-guard
status: published
section: guides
category: I-ecosystem
topic: 社区生态与编辑器接入
content_type: 教程
source_tag: 第三方服务
entry_tags: [App, CLI]
difficulty: 进阶
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-12
date_modified: 2026-11-10
verified_on: 2026-11-10
official_ref: https://github.com/hashgraph-online/hol-guard
keywords: [Codex 插件安全, HOL Guard, hol-guard install codex, plugin-scanner, PreToolUse hook, MCP 审批]
related: [codex-skillspector-skill-security-scan, codex-plugin-hook-audit, hooks-guide]
faq:
  - q: HOL Guard 是 OpenAI 官方的吗？
    a: 不是。HOL Guard 和 plugin-scanner 由 Hashgraph Online 开源维护，仓库是 hashgraph-online/hol-guard，许可证 Apache-2.0。它通过 Codex 的 Hook 和 MCP 能力接入，不是 Codex 内置功能。
  - q: plugin-scanner 报了 high，是不是说明插件有恶意？
    a: 不一定。high 表示命中了需要人工复核的模式。本文实测 Expo 插件时，唯一的 high 是一个 Skill 里教你用 curl 测试本机开发服务器的示例命令。要打开对应文件看上下文，再决定是否接受。
  - q: 不注册 Guard Cloud 能用吗？
    a: 能。README 写明 Guard Cloud 是可选的；文档也写明本机保护不依赖云端在线，守护进程和 CLI 在本机拦截、记录。云端增加的是共享历史和团队策略。
  - q: 本文在 Codex 里实际跑过 hol-guard install codex 吗？
    a: 没有。写作环境是共享的 Linux 机器，为避免改动它的 Codex 配置，只在临时环境里实测了 plugin-scanner scan 和 hol-guard command test，这两条都不会修改 Codex 配置。接入 Codex 的步骤来自 HOL Guard 的 README 和文档。
---

# Codex 插件安全检查（2026-11 更新）：HOL Guard 拦截高风险操作，plugin-scanner 发布前扫描

> 本文在线版：[codexguide.io/guides/codex-plugin-security-hol-guard](https://codexguide.io/guides/codex-plugin-security-hol-guard)

> 核对依据：GitHub 仓库 [hashgraph-online/hol-guard](https://github.com/hashgraph-online/hol-guard) 的 README、[get-started.md](https://github.com/hashgraph-online/hol-guard/blob/main/docs/guard/get-started.md)、[harness-support.md](https://github.com/hashgraph-online/hol-guard/blob/main/docs/guard/harness-support.md) 和 CHANGELOG，PyPI 上的 [hol-guard](https://pypi.org/project/hol-guard/) 与 [plugin-scanner](https://pypi.org/project/plugin-scanner/)，2026-11-10 核对。当天两个包的最新版本都是 **3.59.0**（2026-11-04 发布），仓库约 1,081 star。**实测范围**：在一台 Linux 机器的临时 Python 环境里装了这两个包，运行了 `plugin-scanner scan` 和 `hol-guard command test`，下文贴的是原始输出；`hol-guard install codex` 会改 Codex 配置，本文没有在写作环境执行。本文 2026-10-12 首发，2026-11-10 按新版本重写。

装一个 Codex 插件越来越容易：一条 `codex plugin add`，它带的 Skills、MCP 服务器和 Hook 就进了你的环境，能读文件、跑命令、连网络。插件本身是谁写的、里面有什么，很多人装之前并没有看。

HOL Guard 是 Hashgraph Online 开源的工具（Apache-2.0），**不是 OpenAI 官方功能**。同一个仓库里有两个包：

- **hol-guard**：装在你的电脑上，Codex 执行命令、调用 MCP 之前先过它这一关，有风险的操作会被拦下来等你批准，并留下记录。
- **plugin-scanner**：给插件、Skill、MCP 包打分，适合插件作者发布前自查，也适合你装别人插件前扫一遍。

## 先看结论

| 你想做的事 | 用什么 | 命令 |
|---|---|---|
| 装插件前扫一遍 | plugin-scanner | `plugin-scanner scan <插件目录>` |
| 让 Codex 跑起来时有人把关 | hol-guard | `hol-guard install codex`，再 `hol-guard run codex` |
| 想知道某条命令会不会被拦 | hol-guard | `hol-guard command test '<命令>'` |
| 在 CI 里卡住不合格的插件 | GitHub Action | `hashgraph-online/ai-plugin-scanner-action` |

## 安装 HOL Guard

README 写的前提：Python 3.10 或更新、pipx，以及匹配的原生运行时。get-started 文档列出的原生 wheel 平台包括 macOS ARM64（macOS 11+）、macOS Intel（macOS 13+，需要从 GitHub release 下载匹配的 wheel）、Linux x86_64 和 Windows x64，Linux ARM64 从 3.58.0 开始提供。

```bash
pipx install hol-guard
hol-guard init
```

`hol-guard init` 是首次设置向导：先列出计划，然后**每一步都先问你**（打开本地面板、安装各个代理的集成、连接可选的 Guard Cloud、桌面通知），你同意一步才做一步。

检查和更新：

```bash
hol-guard --version
hol-guard status
hol-guard update
```

文档提醒：`hol-guard --version` 能输出版本号，不代表原生运行时正常，更不代表代理已被保护。可以先用一条无害命令检查运行时：

```bash
hol-guard command test 'echo guard-install-check'
```

返回 `NO_MATCH` 是正常的；返回 `native_unavailable` 说明安装还没好。

## 接入 Codex

```bash
hol-guard install codex
hol-guard run codex --dry-run
hol-guard run codex
```

按 README 和 [harness-support.md](https://github.com/hashgraph-online/hol-guard/blob/main/docs/guard/harness-support.md)，`install codex` 会做这些事：

- 识别全局和项目的 `config.toml`，解析里面配置的 MCP 服务器；
- 在 `.codex/config.toml` 里安装 Guard 自己的 **`PreToolUse` 和 `PermissionRequest` Hook**，命令在执行前就要经过 Guard，即使 Codex 本身开着完全放行的模式；
- 旧版写在 `.codex/hooks.json` 里的条目会迁移过来，旧的 shell trap 和启动脚本片段会被移除。

`run codex --dry-run` 先记录当前插件、Skill、配置的状态，不真正启动。之后用 `hol-guard run codex` 启动；**如果这些 Hook 缺失或被禁用，Guard 会拒绝用托管方式启动 Codex**，避免你以为有保护其实没有。

Codex 自己的 Hook 机制和信任审核，见 [Codex Hooks 入门](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)。装完后可以按 [Codex 插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md) 的方法，确认 config.toml 里多了哪些条目。

## 被拦下来时怎么审批

文档写明，Codex 有三条路径：

1. **Codex 自带的 Bash 工具调用**：由 `PreToolUse` Hook 检查完整命令，敏感命令在执行前被拒绝，再到 HOL Guard 的审批中心处理。
2. **交互式 Codex CLI 和 Codex App 里的 MCP 工具调用**：Guard 发一个 MCP 审批请求，你**在同一个对话里**批准或拒绝。
3. **`codex exec` 这类无人值守运行**：Codex 不响应审批请求时，Guard 在本机排一个审批请求，并在工具调用的报错里返回请求 ID 和审批链接。

命令行处理审批：

```bash
hol-guard approvals
hol-guard approvals approve <request-id>
hol-guard approvals deny <request-id>
hol-guard receipts
```

`receipts` 是决策记录，事后可以查谁在什么时候放行了什么。

## 防护档位

get-started 文档写明，主控制项是**防护姿态（protection posture）**，三档：**Protected**（默认）、**Extra careful**、**Watch**。默认值对应：

```bash
hol-guard settings set protection protected
```

文档对 Watch 的说明是：**只记录，不拦截**（可以对所有代理或单个代理设置）；被识别为凭据、来自敏感路径的工具输出在 Watch 下仍会对代理隐藏，但动作已经执行。所以 Watch 适合观察一段时间看会命中什么，不适合当作保护。

还可以给「记住的信任」加一道密码或 TOTP，避免被代理或别人随手放行：

```bash
hol-guard settings approval-password enable \
  --new-password '<password>' \
  --confirm-password '<password>' \
  --cooldown-seconds 900
```

默认对放行和大范围信任变更要求密码；加 `--strict-all-decisions` 连拒绝也要求。需要更强时可以用 `hol-guard settings approval-totp enroll` 绑定兼容 Google Authenticator 的 TOTP。

> 本文 2026-10-12 版写的是「四个档位」和「满分 130、七个维度」的评分。3.59.0 的文档改成了上面三档防护姿态，plugin-scanner 的实际输出也按 100 分给出最终分（见下文实测），本次按当前版本改写。

## 先看一条命令会不会被拦：command test

`command test` 和 `command explain` 只检查、不执行，也不会生成审批。2026-11-10 在写作环境里实测（hol-guard 3.59.0）：

```text
$ hol-guard command test 'rm -rf ./build'
╭──────────────────────── HOL Guard command inspection ────────────────────────╮
│ Result       REVIEW                                                          │
│ Action class filesystem destructive command                                  │
│ Extension    command.filesystem                                              │
│ Rule         command.filesystem.recursive-delete                             │
│ Risk classes destructive_shell                                               │
│ Policy       Not evaluated; this inspection creates no approvals or receipts │
╰──────────────────────────────────────────────────────────────────────────────╯
```

（输出后面还有 Why 和 Safer approaches 两栏，这里省略。）对照：`echo guard-install-check` 返回的是 `NO_MATCH`。

想知道 Codex 某条被暂停的命令为什么被拦，就把它放进 `command test` 或 `command explain` 看规则名。

## plugin-scanner：装插件前、发布前扫一遍

```bash
pipx install plugin-scanner
plugin-scanner scan .
plugin-scanner lint .
plugin-scanner verify .
```

它能识别 Codex、Claude Code、DeepSeek Harness、Gemini CLI、Kimi Code、OpenCode 的包格式，`--list-ecosystems` 列出支持的生态，`--ecosystem codex` 指定按 Codex 插件检查。在 Codex marketplace 根目录运行时，会自动找到本地插件条目。CI 里常用：

```bash
plugin-scanner scan . --format sarif --output plugin-scanner.sarif
plugin-scanner scan . --fail-on-severity high
```

GitHub Actions 可以用官方 Action，README 示例里设了 `min_score: 80` 和 `fail_on_severity: high`：

```yaml
- uses: hashgraph-online/ai-plugin-scanner-action@fdb49f9d85321a2ced2933301b395dd3c1ce9c8f # v1.2.631
  with:
    plugin_dir: "."
    min_score: 80
    fail_on_severity: high
```

## 实测：扫一下 Expo 插件

2026-11-10 用 plugin-scanner 3.59.0 扫了 [openai/plugins](https://github.com/openai/plugins) 仓库里的 Expo 插件目录（`plugins/expo`，`.codex-plugin/plugin.json` 版本 1.0.2，仓库最新提交 2026-11-06）：

```bash
plugin-scanner scan plugins/expo --ecosystem codex
```

结果摘要（原始输出节选）：

```text
Ecosystems: codex
Detected packages: 1

── Manifest Validation (28/31) ──
── Security (13/16) ──
  ⚠️ SECURITY.md found                          +0
── Best Practices (12/15) ──
  ⚠️ .codexignore found                         +0
── Skill Security (0/5) ──
  ⚠️ No risky local skill instructions          +0

Findings: critical:0, high:1, medium:0, low:1, info:2

Final Score: 82/100 (B - Good)
```

用 `--format json` 看详情，这几条 finding 分别是：

| 严重程度 | 内容 | 怎么理解 |
|---|---|---|
| high | Risky local skill instruction detected：Skill 里有 `curl http://localhost:8081/api/hello` | 出自 `expo-api-routes` 这个 Skill 的示例：先 `npx expo serve` 起本机服务器，再用 curl 测 API 路由（后面一行是带 `-d` 的 POST）。访问的是本机开发服务器，属于正常示例，但值得知道 Codex 可能照着执行 |
| low | SECURITY.md is missing | 插件没有安全披露说明 |
| info | .codexignore is missing | 建议加，防止把本地产物和密钥打包进去 |
| info | Interface asset or URL "screenshots" is invalid | `plugin.json` 的 screenshots 字段不是 HTTPS 或安全的仓库内路径 |

这个例子说明两件事：分数和 high 都只是**提示你去看哪里**，最后要打开文件看上下文；另一方面，即使是 marketplace 里知名厂商的插件，也会有需要你确认的指令。

同一天也扫了 expo/skills 仓库里的新版插件目录（1.14.3）。这个目录同时带 Claude 格式，扫描器把它识别成了 Claude 插件（94/100），所以没有和上面的 Codex 结果放在一起比较。

## 和 Codex 自带的检查怎么配合

- **装之前**：看插件来源、`plugin.json`、Skills 和 MCP 配置；第三方 Skill 可以再用 [SkillSpector](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md) 扫提示注入和数据外泄。
- **装之后**：按 [Codex 插件与 Hook 自查](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md) 检查 config.toml、Hook 信任记录和插件带的 MCP。
- **运行时**：Codex 自己的权限模式和审批照常保留，HOL Guard 是额外的一层，不是替代。
- **定期**：`hol-guard diff codex` 看启动前有哪些变化，`hol-guard inventory` 列出跟踪的插件和配置，`hol-guard abom --format json` 导出 AI 物料清单。

## 常见问题

**HOL Guard 是 OpenAI 官方的吗？**

不是，由 Hashgraph Online 开源维护（Apache-2.0）。

**plugin-scanner 报了 high，是不是说明插件有恶意？**

不一定。high 表示需要人工复核，要打开文件看上下文。

**不注册 Guard Cloud 能用吗？**

能，本机保护不依赖云端。

**本文在 Codex 里实际跑过 hol-guard install codex 吗？**

没有。只实测了 `plugin-scanner scan` 和 `hol-guard command test`，接入 Codex 的步骤来自官方 README 和文档。

## 相关阅读

- [Codex 用 SkillSpector 扫描第三方 Skill：提示注入与数据外泄检查](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)
- [Codex 插件与 Hook 自查：第三方应用自动安装与信任记录](../10-配置模型与权限安全/22-Codex插件与Hook自查-第三方应用自动安装与信任记录.md)
- [Codex Hooks 入门：hooks.json 配置、信任审核与常用场景](../11-自动化与高级工作流/11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)
