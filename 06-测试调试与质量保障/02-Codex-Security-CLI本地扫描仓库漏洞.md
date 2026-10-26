---
id: codex-security-cli
title: Codex Security CLI 上手：用 codex-security 在本地扫描仓库漏洞，并接进 CI（0.6.0 实测）
seo_title: Codex Security CLI 上手：本地扫描仓库漏洞与 CI 接入
description: Codex Security CLI（@openai/codex-security）可在终端扫描整个仓库、目录或 diff，输出报告和结构化结果，并按严重级别控制 CI 退出码。本文用 0.6.0 实测安装、dry-run 预检和常见报错，讲清登录、扫描范围、结果文件和 GitHub Actions 接入。
url: /guides/codex-security-cli
status: published
section: guides
category: D-project-dev
topic: 开发、测试与代码协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI]
difficulty: 进阶
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-25
date_modified: 2026-10-25
verified_on: 2026-10-25
models: [gpt-5.6-sol, gpt-6-sol]
official_ref: https://learn.chatgpt.com/docs/security/cli
keywords: [Codex Security, codex-security, Codex Security CLI, 代码漏洞扫描, fail-on-severity, Codex Security GitHub Actions]
related: [codex-github-issue-to-pr, config-toml-guide]
howto: true
faq:
  - q: Codex Security CLI 和 Codex Security 插件有什么区别？
    a: 官方建议第一次在本地扫描用插件，在 Codex 里交互式处理结果；CLI 适合在终端里重复跑扫描，或者接进 CI。两者都需要 Codex Security 访问权限。
  - q: 运行 codex-security 需要什么环境？
    a: Node.js 24 或 26（也支持 22.13 及以上），以及 Python 3.10 及以上；用 Python 3.10 时还要装 tomli。根据账号和仓库情况，全仓库扫描可能还需要 Trusted Access for Cyber。
  - q: 扫描结果放在哪里？
    a: 不传 --output-dir 时，结果保存在 $CODEX_HOME/state/plugins/codex-security/scans/<仓库名> 下。用 --output-dir 指定时，目录必须在被扫描仓库和它所在的 Git 工作区之外。
  - q: 扫描通过（退出码 0）是不是代表没有漏洞？
    a: 不是。官方文档写明退出码 0 不代表每个文件都审查过，覆盖缺口不会改变退出码，要看 coverage.json 里的排除项、延后项和待确认问题。
---

# Codex Security CLI 上手：用 codex-security 在本地扫描仓库漏洞，并接进 CI（0.6.0 实测）

> 本文在线版：[codexguide.io/guides/codex-security-cli](https://codexguide.io/guides/codex-security-cli)

> 核对依据：OpenAI 官方文档 [Codex Security](https://learn.chatgpt.com/docs/security)、[Codex Security CLI](https://learn.chatgpt.com/docs/security/cli)、[CLI reference](https://learn.chatgpt.com/docs/security/cli/reference)、[Run Codex Security in GitHub Actions](https://learn.chatgpt.com/docs/security/cli/ci/github)，以及 [openai/codex-security](https://github.com/openai/codex-security) 仓库的 0.6.0 发布说明。实测环境是 Linux、Node.js 24.22.1、`@openai/codex-security 0.6.0`，扫描对象是一个自建的演示仓库。实测机器**没有** Codex Security 访问权限，所以只验证到安装、`info`、`--dry-run` 预检和几种输入报错，**没有跑出真实漏洞结果**；结果文件和退出码的说明引自官方文档。核对日期 2026-10-25。

代码改完想做一次安全检查，以前要么等 PR 上的安全审查，要么在 Codex 里装插件慢慢问。Codex Security CLI 把这件事放进终端：一条命令扫描整个仓库、某几个目录或者一段 diff，产出报告和结构化结果，还能按严重级别决定 CI 是否失败。

这篇讲：它和插件、Cloud 怎么选，怎么安装和登录，扫描范围怎么选，dry-run 能帮你提前发现什么问题，结果文件怎么读，以及怎么接进 GitHub Actions。

## 先选对入口：Cloud、插件、CLI、SDK

官方文档把 Codex Security 分成四种用法：

| 用法 | 适合什么时候 |
| --- | --- |
| Codex Security Cloud | 在 Codex cloud 里扫描已连接的 GitHub 仓库，或者持续监控新提交 |
| Codex Security 插件 | 在 Codex 里扫描本地仓库，交互式处理发现的问题 |
| Codex Security CLI | 在终端里重复跑扫描，或者加进 CI |
| Codex Security SDK | 在自己的应用或开发工具里发起扫描、处理结果 |

官方的建议是：**第一次在本地扫描，先用插件**；需要可重复的终端扫描或 CI 检查时再用 CLI。CLI 和 SDK 都在公开的 `@openai/codex-security` 包里。用 OpenAI 推理来扫描，需要 Codex Security 访问权限。

## 安装前检查环境

官方 CLI 文档列出的前提：

- Node.js 24 或 26，也支持 22.13 及以上
- Python 3.10 及以上；用 Python 3.10 时还需要 `tomli`
- 用 OpenAI 推理扫描需要 Codex Security 访问权限；根据账号和仓库情况，全仓库扫描可能还需要 [Trusted Access for Cyber](https://chatgpt.com/cyber)

实测时机器上的 Node.js 是 20，不满足要求，换成 Node.js 24.22.1 后才装上。先确认版本：

```bash
node --version
python3 --version
```

官方文档的写法是直接用 `npx` 运行公开包，先看版本号：

```bash
npx @openai/codex-security --version
```

实测时把包装进了一个本地目录（`npm install @openai/codex-security`），再运行它的 `codex-security` 命令，输出：

```text
0.6.0
```

下文为了简洁都写成 `codex-security`，换成 `npx @openai/codex-security` 效果相同。`info --json` 可以看内置插件版本，各版本改动见 [CLI and SDK releases](https://github.com/openai/codex-security/releases)。

`codex-security --help` 在 0.6.0 里列出的主要命令有：`scan`、`policy`、`validate`、`patch`、`verify-fix`、`scans`、`findings`、`classify-severity`、`dedupe`、`suggest-owners`、`export`、`import`、`publish`、`bulk-scan`、`scan-components`、`install-hook`。日常先用到的是 `scan` 和 `scans`。

## 登录：本机用浏览器，服务器用设备码，CI 用 API Key

本机有浏览器时：

```bash
codex-security login
```

远程或没有浏览器的机器，如果工作区允许设备码登录：

```bash
codex-security login --device-auth
```

CI 里不登录，而是设置环境变量 `OPENAI_API_KEY` 或 `CODEX_API_KEY`。

扫描时用 `--auth` 选凭据：

| 参数 | 含义 |
| --- | --- |
| `--auth auto`（默认） | 自动选择。同时有 ChatGPT 登录和环境变量里的 API Key 时，交互式文本输出会问你用哪个；CI、JSON/JSONL 输出和没有交互终端的扫描用环境变量里的 Key |
| `--auth chatgpt` | 用已保存的登录凭据 |
| `--auth api-key` | 用环境变量里的 API Key |

想让自动模式默认用登录凭据，官方给的做法是先 `unset OPENAI_API_KEY CODEX_API_KEY`。

没有登录、也没有 API Key 时直接扫描，实测会在准备阶段停下，退出码 2：

```text
[00:00] Preparing scan
No credentials were found. Run 'codex-security login'. On a remote or headless machine, use 'codex-security login --device-auth' if your workspace allows it. If device auth is disabled, see 'codex-security login --help' for browser login over SSH. For CI, set OPENAI_API_KEY or CODEX_API_KEY.
```

`codex-security info --json` 可以查看当前运行环境。实测 0.6.0 里能看到 `sdkVersion` 为 0.6.0、内置插件版本 0.1.95、默认模型 `gpt-5.6-sol`、默认推理强度 `xhigh`，以及一条说明：扫描只能通过 CLI 发起，MCP 通道不能取消正在运行的命令（`Scans are CLI-only because the MCP transport cannot cancel active commands.`）。默认值会随版本变化，以你自己机器上的输出为准；需要换模型或强度时用 `--model` 和 `--effort`。

## 选择扫描范围

`scan` 的仓库参数默认是当前目录。每次扫描只能选一种范围：

| 参数 | 扫描什么 |
| --- | --- |
| 不加范围参数 | 整个仓库 |
| `--path PATH` | 仓库里的某个路径，可以重复传多次 |
| `--diff BASE` | 从 `BASE` 到 `--head`（默认 `HEAD`）之间已提交的改动 |
| `--working-tree` | 已暂存和未暂存的改动，对比 `--base`（默认 `HEAD`） |
| `--mode deep` | 深度扫描，只支持整个仓库和指定路径 |

`--path`、`--diff`、`--working-tree` 互斥；`--head` 只能配 `--diff`，`--base` 只能配 `--working-tree`。diff 和 working-tree 扫描要求仓库参数是 Git 工作区根目录，引用的分支或提交必须在当前检出里存在。

常用写法：

```bash
# 整个仓库
codex-security scan .

# 只看两个目录
codex-security scan . --path src --path tests

# 只看这个分支相对 main 的改动
codex-security scan . --diff origin/main --head HEAD

# 只看还没提交的改动
codex-security scan . --working-tree --base HEAD
```

深度扫描会多轮反复审查，`scan --help` 里能看到相关参数，比如 `--workers`（默认 4）、`--subagents`（默认 3）、`--stop-after-no-new`（默认 4）、`--max-discovery-runs`（默认 40）。先用标准模式跑通，再考虑深度扫描。

## 先跑 dry-run：不加载凭据，只检查输入

`--dry-run` 会检查仓库、扫描范围、知识库文件、输出目录和 Codex 配置，**不加载凭据、不启动扫描**。正式扫描前先跑一次，能提前发现路径和参数问题。

实测命令（演示仓库在 `/tmp/demo/shop-api`）：

```bash
codex-security scan /tmp/demo/shop-api --auth chatgpt \
  --output-dir /tmp/demo/cs-results --dry-run
```

输出（退出码 0）：

```text
[00:00] Validating scan inputs
[00:00] Preflight complete
dryRun: true
repository: /tmp/demo/shop-api
target:
  kind: repository
  paths: []
mode: standard
outputDir: /tmp/demo/cs-results
authentication:
  method: stored_credentials
  verified: false
model: gpt-5.6-sol
reasoningEffort: xhigh
```

`verified: false` 说明 dry-run 没有去验证凭据，这和文档描述一致。

dry-run 实测拦下的两类常见错误：

**输出目录放在仓库里面。** 结果目录必须在被扫描目录和它所在的 Git 工作区之外：

```text
[00:00] Validating scan inputs
Scan output directory must be outside the scanned directory and any enclosing Git worktree.
  Resolved path:  /tmp/demo/shop-api/results
  Protected root: /tmp/demo/shop-api
  Reason:         Scan artifacts cannot be written inside the protected scan root.
Re-run with --output-dir /tmp/demo/shop-api-codex-security-scan.
```

**diff 的基准提交不存在。** 演示仓库只有一个提交，`--diff HEAD~1` 会报：

```text
[00:00] Validating scan inputs
unknown Git ref: HEAD~1. ...
```

这两种情况退出码都是 2。CI 里拉代码时如果用了浅克隆，`--diff origin/main` 也可能找不到基准，官方的 PR 工作流示例因此用了 `fetch-depth: 0`。

## 结果放在哪里、怎么读

不传 `--output-dir` 时，结果保存在 `$CODEX_HOME/state/plugins/codex-security/scans/<仓库名>`（`CODEX_HOME` 默认是 `~/.codex`）；设置了 `CODEX_SECURITY_STATE_DIR` 时改放到 `$CODEX_SECURITY_STATE_DIR/scans/<仓库名>`。这些目录里会有源码片段和漏洞细节，官方提醒要管好权限和保留时间。

已保存的扫描用 `scans` 查看。实测在还没有扫描记录时：

```bash
codex-security scans list
```

```text
scans: []
```

官方文档列出的一次完成扫描的目录结构：

```text
<scan-directory>/
├── scan-manifest.json
├── findings.json
├── coverage.json
├── report.md
├── artifacts/
└── exports/
    └── results.sarif       # 生成了才有
```

| 文件 | 内容 |
| --- | --- |
| `report.md` | 给人读的扫描报告 |
| `findings.json` | 每个问题的编号、严重级别、置信度、位置、证据、验证、数据流、可达性和修复建议 |
| `coverage.json` | 审查过的范围、排除项、延后的工作和待确认问题 |
| `scan-manifest.json` | 扫描身份、状态、范围和各结果文件的哈希；`scan.status` 是 `completed`、`failed`、`canceled` 或 `interrupted` |

读结果时别只看 `report.md`。**官方特别说明：退出码 0 不代表每个文件都审查过**，覆盖缺口不会改变退出码，要打开 `coverage.json` 看哪些地方没审到。

想复用同一个输出目录又保留上次结果，加 `--archive-existing`，旧结果会被移到 `DIR.previous-<时间戳>-<id>`。

## 退出码和 CI 策略

扫描默认只出报告，不让命令失败。要在 CI 里卡住高危问题，加 `--fail-on-severity`：

```bash
codex-security scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --json \
  --fail-on-severity high \
  > /path/outside/repository/codex-security.json
```

官方文档的退出码：

| 退出码 | 含义 |
| --- | --- |
| `0` | 扫描完成并通过严重级别策略，或其他命令成功 |
| `1` | 扫描完成，但发现了达到或超过设定级别的问题 |
| `2` | 输入、执行、结果完整性、必需输出或导出失败 |
| `130` | Ctrl-C 中断 |
| `143` | 收到 SIGTERM 被终止 |

费用方面可以加 `--max-cost USD`，扫描的预估模型费用超过这个数就停。官方说明这是**估算值，不是硬上限**，已经在进行中的请求可能略微超出。

## 接进 GitHub Actions

官方提供了 `openai/codex-security` Action，有两种示例工作流：每周定时扫描默认分支，以及扫描 PR 改动。准备步骤是在仓库 **Settings → Secrets and variables → Actions** 里新建名为 `CODEX_SECURITY_API_KEY` 的 secret，填入 OpenAI API Key。

PR 扫描示例的核心部分（摘自官方文档）：

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

permissions:
  contents: read

jobs:
  security:
    if: github.event.pull_request.head.repo.full_name == github.repository && github.actor != 'dependabot[bot]'
    runs-on: ubuntu-24.04
    steps:
      - name: Set up the Ubuntu sandbox
        run: |
          sudo apt-get update
          sudo apt-get install --yes bubblewrap apparmor-profiles
          sudo apparmor_parser -r /usr/share/apparmor/extra-profiles/bwrap-userns-restrict

      - uses: actions/checkout@<官方文档里固定的提交>
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
          persist-credentials: false

      - name: Scan PR changes
        uses: openai/codex-security@<官方文档里固定的提交>
        with:
          scope: diff
          model: gpt-6-sol
          effort: high
          fail-on-severity: none
          upload-artifacts: "true"
        env:
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
```

完整的 YAML 请从[官方文档](https://learn.chatgpt.com/docs/security/cli/ci/github)复制，里面的 Action 用提交哈希固定了版本，上面用尖括号代替了。

几个容易忽略的点：

- 示例从 `fail-on-severity: none` 开始，也就是先只出建议、不拦合并。看过一段时间的结果质量后，再改成 `high`。
- 示例跳过了 fork 来的 PR 和 `dependabot[bot]` 的 PR。**跳过的 job 不代表做过安全审查**，而 GitHub 会把按条件跳过的 job 当成成功，即使它是必需检查。需要更严格时，按官方文档的“Require a successful, completed scan”一节加一个单独的门禁 job。
- 这个 Action 不支持 `pull_request_target` 和 `workflow_run` 触发。
- 只在你信任的仓库和 PR 上运行。扫描用 runner 的本地权限运行，不会停下来等审批；无关的凭据和部署步骤放到别的 job 里。

## 安全提醒：扫描以你的系统权限运行

CLI 扫描用你本机的操作系统权限运行，审批策略固定为 `never`，不会停下来问你。它可以读本地文件系统，写工作区和扫描结果目录。通过 `--codex` 传入的 `approval_policy`、`sandbox_mode` 等设置**不能**替换或收紧这些扫描控制。

扫描进程还会继承你的环境变量，包括和扫描无关的 API Token、云账号凭据。官方建议**扫描前先清掉无关凭据**。在本机跑时，可以开一个只带必要变量的新终端。

## 0.6.0 里新增了什么

根据 [0.6.0 发布说明](https://github.com/openai/codex-security/releases)，这一版主要新增：

- 可以导入 Wiz、Snyk Open Source、Semgrep Code、Endor Labs 的报告：`publish findings --to local` 导入本地，`--to cloud` 发布到云端，本地证据用 `findings imported` 查看
- `classify-severity` 支持 `--runs` 指定独立评估次数（1 到 10 次，默认 3 次）。注意：不带自定义评分标准时，它以前直接沿用扫描器给的级别，现在需要登录和模型访问权限
- `scan --owner-suggestions` 在支持的 Git 扫描完成后单独生成一份负责人建议报告，不会自动分配给任何人
- `patch --host` 和 `verify-fix --host` 提供托管修复；普通的修复和验证命令支持 `--verification-mode static`
- 策略差异预览改用 Node 计算，不再需要 Python

这些是进阶功能，第一次用先把 `scan`、结果文件和 CI 策略跑通。

## 推荐的上手顺序

1. 确认 Node.js 和 Python 版本，安装后跑 `codex-security --version`。
2. 本机 `codex-security login`，CI 用 `CODEX_SECURITY_API_KEY` secret。
3. 先 `--dry-run`，确认范围和输出目录都对。
4. 先扫一个目录（`--path`）或一段 diff，看 `report.md` 和 `coverage.json`。
5. CI 里先用 `fail-on-severity: none` 观察，再改成 `high`。

## 参考资料

- [Codex Security 总览](https://learn.chatgpt.com/docs/security)
- [Codex Security CLI](https://learn.chatgpt.com/docs/security/cli)
- [Codex Security CLI reference](https://learn.chatgpt.com/docs/security/cli/reference)
- [Run Codex Security in GitHub Actions](https://learn.chatgpt.com/docs/security/cli/ci/github)
- [openai/codex-security](https://github.com/openai/codex-security)
