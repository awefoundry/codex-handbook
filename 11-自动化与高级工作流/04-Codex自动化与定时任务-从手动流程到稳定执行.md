---
id: codex-automation-ci-scheduled-tasks
title: Codex 自动化与 CI：codex exec 非交互模式、GitHub Action 工作流 YAML、--output-schema 结构化输出与 API Key 安全（2026-10 更新）
seo_title: Codex 自动化与 CI：codex exec、GitHub Action 与 API Key 安全
description: codex exec 可以让 Codex 在脚本和 CI 里一次性跑完任务。本文按 2026 年 10 月官方文档更新：可复制的 GitHub Action 工作流 YAML、--full-auto 停用后的写法、API Key 避免 job 级泄露、--json 事件流与 --output-schema，以及 resume 两阶段流水线。
lede: 无人值守用 codex exec；CI 优先 openai/codex-action，密钥只绑 Codex 那一步。
url: /guides/codex-automation-ci-scheduled-tasks
status: published
section: guides
category: H-automation
topic: 自动化与多任务协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 进阶
order: 4
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-21
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/non-interactive-mode
keywords: [codex exec, Codex GitHub Action, Codex CI, openai/codex-action, Codex 非交互模式, CODEX_API_KEY]
related: [codex-automations-scheduled-tasks, codex-github-issue-pr-workflow, codex-rules-prefix-rule]
howto: true
faq:
  - q: 以前脚本里的 --full-auto 还能用吗？
    a: 不能。官方 Non-interactive mode 写明 --full-auto 已不再支持。需要改文件时改用 --sandbox workspace-write；若要让审批请求走自动审查，再用 --approve-for-me（仍配合 workspace-write 沙箱）。
  - q: 能不能把 OPENAI_API_KEY 或 CODEX_API_KEY 写在整个 job 的 env 里？
    a: 不要。官方要求：不要把这些密钥设成会 checkout 或跑仓库可控代码的 job 级环境变量；构建脚本、测试、依赖生命周期钩子或同 job 里被攻破的 action 都能读到。密钥只给调用 Codex 的那一步；GitHub Actions 优先用 openai/codex-action，由它启动 Responses API 代理。
  - q: crontab 定时跑和本文是什么关系？
    a: 本文聚焦 codex exec 与 CI／GitHub Action。桌面／网页 Scheduled tasks（旧称 Automations）见姊妹篇；crontab 与 Scheduled 的分工也以那篇为准，这里不展开 cron 表。
---

# Codex 自动化与 CI：codex exec 非交互模式、GitHub Action 工作流 YAML、--output-schema 结构化输出与 API Key 安全（2026-10 更新）

> 本文在线版：[codexguide.io/guides/codex-automation-ci-scheduled-tasks](https://codexguide.io/guides/codex-automation-ci-scheduled-tasks)

> 核对依据：learn.chatgpt.com《[Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)》《[Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)》与 [openai/codex-action](https://github.com/openai/codex-action)（2026-10-22）。「我的用法」非官方强制流程。未在真实 runner 完整跑通示例，`client_validation_pending: true`。

日常多半是敲 `codex`、在交互界面边聊边改。扫日志、补 changelog、PR 只读审查这类活，不必一直盯着点确认。

**`codex exec`** 是非交互入口：一条命令给任务，规划、执行后退出。进度走 `stderr`，最终答复走 `stdout`，可进 shell、管道和 CI。GitHub 上优先用 `openai/codex-action@v1`：安装 CLI、按需起 Responses API 代理，再按你声明的权限跑 `codex exec`。

## 2026-10 更新说明：`--full-auto` 已停用，补齐 Action YAML 与密钥写法

相对旧版，这次加厚三件事：

1. **`--full-auto` 不再支持** → `--sandbox workspace-write`；需要自动审批再用 `--approve-for-me`（官方：审批走自动审查，并配合 workspace-write）。
2. **可复制的 Actions 示例**：PR 评审，以及「CI 失败后出补丁」双 job（密钥与写权限拆开）。
3. **API Key 安全**：`OPENAI_API_KEY`／`CODEX_API_KEY` 勿写成会跑仓库可控代码的 **job 级** `env`；只绑 Codex 步骤；优先 `openai/codex-action`。

桌面／网页 **Scheduled tasks**（旧称 Automations）见《[定时任务](../12-官方工具与集成/06-Codex-Automations定时任务.md)》；交互式 Issue→PR 见《[GitHub Issue 到 PR](../08-插件工作流/04-GitHub插件实战-从Issue到PullRequest让Codex跑完整流程.md)》。

## 交互模式和 exec 模式差在哪

| | 交互（`codex`） | 非交互（`codex exec`） |
|---|---|---|
| 形态 | 持续会话 | 一次提示，跑完退出 |
| 适合 | 边做边调 | 脚本、CI、管道 |
| 输出 | TUI／对话 | 进度→`stderr`，最终消息→`stdout` |
| 权限 | 可交互审批 | 事先定好沙箱／审批 |

最基础：

```bash
codex exec "summarize the repository structure and list the top 5 risky areas"
```

把最终结果接到文件：

```bash
codex exec "generate release notes for the last 10 commits" | tee release-notes.md
```

**管道：** 若 stdin 有内容且你又写了提示词参数，官方约定是——提示词是指令，管道内容是额外上下文：

```bash
git diff origin/main...HEAD \
  | codex exec --sandbox read-only -o review.md \
    "审查这些改动，列出潜在 bug 和风格问题"
```

整段 stdin 当作提示词时，用显式哨兵 `-`：

```bash
cat prompt.txt | codex exec -
# 或
generate_prompt.sh | codex exec - --json > result.jsonl
```

Codex 要求在 **Git 仓库**里跑，避免误伤非仓库目录；确认环境安全时可加 `--skip-git-repo-check`。


## 常用参数：模型、落盘、短暂会话、干净配置

裸跑一句只是开始。自动化里更常用这些：

**模型与配置覆盖**

```bash
codex exec -m gpt-6-luna \
  -c model_reasoning_effort="low" \
  "把这个文件里的 print 全换成 logging"
```

`-c` 可覆盖 `$CODEX_HOME/config.toml` 里的项（点号写嵌套路径，值按 TOML 解析）。省钱、控时延时常用。

**最终消息落盘：`-o`／`--output-last-message`**

```bash
codex exec -o result.txt "检查依赖有没有已知的安全漏洞"
# 文件里是最终消息；同时仍会打印到 stdout
```

**不落盘会话：`--ephemeral`**

```bash
codex exec --ephemeral "triage this repository and suggest next steps"
```

不需要保留 rollout／会话文件时用它，适合一次性 CI 步骤。

**忽略用户配置与规则（受控环境）**

- `--ignore-user-config`：不加载 `$CODEX_HOME/config.toml`
- `--ignore-rules`：跳过用户与项目的 execpolicy `.rules` 文件

适合 runner 上只要仓库声明行为的场景。Rules 写法见《[Codex Rules（prefix_rule）](./10-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)》。

若启用了 `required = true` 的 MCP 且初始化失败，`codex exec` 会直接退出，不会静默少工具继续。


## 权限：默认只读，`--full-auto` 换成什么

官方写明：`codex exec` **默认只读沙箱**。自动化里按最小权限加码：

```bash
# 允许改工作区
codex exec --sandbox workspace-write "给 src/foo.py 补上类型注解"

# 需要自动处理审批请求时（配合 workspace-write）
codex exec --sandbox workspace-write --approve-for-me "按测试失败最小修复"

# 仅在受控隔离环境（如一次性 CI 容器）才考虑
codex exec --sandbox danger-full-access "…"
```

旧脚本把 `--full-auto` 换成 `--sandbox workspace-write`（需要自动审批再加 `--approve-for-me`）。`danger-full-access` 仅限隔离 runner／容器。

`--dangerously-bypass-approvals-and-sandbox`（`--yolo`）跳过确认与沙箱，只适合已隔离环境；主力机不要图省事开。

**我的用法：** CI 审查默认 `read-only`；要改文件的 autofix 用 `workspace-write`（或 Action 侧等价的权限配置），密钥与 `contents: write` 分到不同 job。

## `--json` 事件流与 `--output-schema`

### JSONL 事件流

```bash
codex exec --json "summarize the repo structure" | jq
```

开启 `--json` 后，`stdout` 为 **JSON Lines**（每事件一行）。类型含 `thread.started`、`turn.started`、`turn.completed`、`turn.failed`、`item.*`、`error`；item 可含消息、命令、文件变更、MCP、搜索等。

示意（每行一个对象；字段以你本机 CLI 为准）：

```json
{"type":"thread.started","thread_id":"…"}
{"type":"item.completed","item":{"id":"item_3","type":"agent_message","text":"…"}}
{"type":"turn.completed","usage":{"input_tokens":24763,"output_tokens":122}}
```

只要最终文本用 `-o`；要稳定字段用 schema。

### `--output-schema` + `-o`

`schema.json` 示例：

```json
{
  "type": "object",
  "properties": {
    "project_name": { "type": "string" },
    "programming_languages": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["project_name", "programming_languages"],
  "additionalProperties": false
}
```

```bash
codex exec "Extract project metadata" \
  --output-schema ./schema.json \
  -o ./project-metadata.json
```

最终答复按 schema 约束；`-o` 写入文件并打印 stdout。Action 可用 `codex-args` 传 `--output-schema`，或用输入 `output-schema`／`output-schema-file`。


## 在 GitHub Actions 里跑：`openai/codex-action@v1`

官方建议：Actions 里不要自己装 CLI 再把密钥塞进普通 shell；改用 [`openai/codex-action`](https://github.com/openai/codex-action)。它会安装 CLI，在有 API key 时启动 Responses API 代理，再按安全策略跑 `codex exec`。

### 前置条件（官方）

Secret 存 `OPENAI_API_KEY`（步骤输入引用）；Linux／macOS runner（**Windows 必须** `safety-strategy: unsafe`）；先 `checkout` 再跑 Action；`prompt` 与 `prompt-file` **二选一**（建议 `.github/codex/prompts/`）。

### 示例：PR 打开／同步时跑审查并回贴评论

以下 YAML 来自官方《Codex GitHub Action》文档（可直接复制后改 prompt 路径）：

```yaml
name: Codex pull request review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  codex:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      final_message: ${{ steps.run_codex.outputs.final-message }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge
          fetch-depth: 0
          persist-credentials: false

      - name: Run Codex
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/review.md
          output-file: codex-output.md

  post_feedback:
    runs-on: ubuntu-latest
    needs: codex
    if: needs.codex.outputs.final_message != ''
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post Codex feedback
        uses: actions/github-script@v7
        with:
          github-token: ${{ github.token }}
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_FINAL_MESSAGE,
            });
        env:
          CODEX_FINAL_MESSAGE: ${{ needs.codex.outputs.final_message }}
```

要点：

- 步骤输出名是 **`final-message`**（连字符），再映射成 job `outputs`
- `codex-args` 可传 JSON 数组（如 `["--ephemeral"]`）或 shell 风格字符串
- `sandbox`：`workspace-write`／`read-only`／`danger-full-access`（与 `codex exec` 对齐）
- `safety-strategy` 默认 **`drop-sudo`**（Linux／macOS 上在跑 Codex 前撤掉 sudo）；Windows 只能 `unsafe`
- README 另推荐新工作流用 `permission-profile: ":workspace"`（与 `sandbox` 互斥；需较新 CLI）。按锁定的 `codex-version` 二选一，勿混用

### 示例：主 CI 失败后由 Codex 生成补丁（密钥与写权限分离）

官方 Non-interactive 文档给出的模式：

1. `workflow_run` 在主 CI **失败**时触发
2. `generate_fix` job 只有 `contents: read`，安装依赖时 **不**暴露 OpenAI key
3. 再跑 `openai/codex-action@v1`
4. 把本地 diff 打成 patch artifact
5. 另一个 `open_pr` job 拿 `contents: write`／`pull-requests: write` 应用补丁开 PR——**该 job 不拿 `OPENAI_API_KEY`**

骨架（Node 示例；按你的栈改 setup／测试命令）：

```yaml
name: Codex auto-fix on CI failure

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  generate_fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      has_patch: ${{ steps.diff.outputs.has_patch }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: |
          if [ -f package-lock.json ]; then npm ci; fi

      - name: Run Codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt: |
            The CI workflow "${{ github.event.workflow_run.name }}" failed for commit
            ${{ github.event.workflow_run.head_sha }}.

            Run `npm test --silent` to reproduce the failure. Identify the minimal
            change needed to make the tests pass, implement only that change, and
            run `npm test --silent` again.

            Do not refactor unrelated files.

      - name: Create patch artifact
        id: diff
        run: |
          git add -N .
          git diff --binary HEAD > codex.patch
          if [ -s codex.patch ]; then
            echo "has_patch=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_patch=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Upload patch artifact
        if: steps.diff.outputs.has_patch == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: codex-fix-patch
          path: codex.patch
          if-no-files-found: error

  open_pr:
    runs-on: ubuntu-latest
    needs: generate_fix
    if: needs.generate_fix.outputs.has_patch == 'true'
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0
      - uses: actions/download-artifact@v4
        with:
          name: codex-fix-patch
      - run: git apply --index codex.patch
      # 随后 git switch -c / commit / push / gh pr create
      # 完整脚本见官方 Non-interactive 文档同名示例
```

`open_pr` 的完整 `gh pr create` 脚本见官方 Non-interactive 同名示例。**我的用法：** autofix 过人审；prompt 写死最小改动；PR／issue 文本先消毒。

## API Key 安全：只给 Codex 那一步

官方 Non-interactive 文档的硬要求：

- **不要**把 `OPENAI_API_KEY` 或 `CODEX_API_KEY` 设成会 checkout／运行仓库可控代码的 **job 级**环境变量。
- 同 job 里的构建脚本、测试、依赖 lifecycle hook，或被攻破的 action，都能读 job `env`。
- 其他自动化环境：只在需要的那次 `codex exec` 上内联设置，例如：

```bash
CODEX_API_KEY=<api-key> codex exec --json "triage open bug reports"
```

`CODEX_API_KEY` 可用于 `codex exec`、`codex review`、TypeScript SDK，以及 `codex exec-server --remote`。

GitHub Actions 优先把 key 交给 Action 的 `openai-api-key` 输入；由代理转发，而不是散落在后续 shell。安全清单还强调：限制触发者、清理 PR／commit／issue 输入、默认 `drop-sudo`、Codex 放在 job **靠后**，怀疑泄露立刻轮换密钥。

用 ChatGPT 账号态（`~/.codex/auth.json`）跑 CI 是进阶路径：默认仍推荐 API key；`auth.json` 按密码对待，不适合公开仓库。细节见官方「Maintain Codex account auth in CI/CD」，本文不展开。

## 两阶段流水线：`codex exec resume --last`

先审查、再修复时，不必把上下文重新糊进第二段提示词：

```bash
codex exec "review the change for race conditions"
codex exec resume --last "fix the race conditions you found"
```

也可 `codex exec resume <SESSION_ID>`。CI 两阶段通常 **不要**对第一段盲目加 `--ephemeral`，否则可能没有可 resume 的会话。

## 本地脚本与定时：链接 Scheduled，不重复 cron 长文

`codex exec` 也能写进本机 shell 循环，例如：

```bash
for f in src/*.py; do
  codex exec --sandbox workspace-write \
    "给 $f 补上文档字符串，风格参考 Google style"
done
```

定时调度（桌面／网页 Scheduled，以及和 crontab／CI 的分工）见《[Codex 定时任务（Scheduled tasks）](../12-官方工具与集成/06-Codex-Automations定时任务.md)》。本篇只保证 exec／CI 的权限、输出、密钥与 Action YAML 写对。


## 快速对照清单

1. 对话 → `codex`；无人值守／CI → `codex exec` 或 `openai/codex-action@v1`
2. 去掉 `--full-auto` → `--sandbox workspace-write`［+ `--approve-for-me`］
3. 最终文本 → `-o`；事件流 → `--json`；稳定字段 → `--output-schema` + `-o`
4. 一次性 CI → `--ephemeral`；干净环境 → `--ignore-user-config`／`--ignore-rules`
5. GitHub：secret 只进 Action；禁止 job 级 API key；写权限与密钥分 job
6. 两阶段 → `resume --last`；定时 → Scheduled 专文

## 参考

- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action) · [openai/codex-action](https://github.com/openai/codex-action)
- 姊妹篇：[Scheduled tasks](https://codexguide.io/guides/codex-automations-scheduled-tasks) · [Issue→PR](https://codexguide.io/guides/codex-github-issue-pr-workflow) · [Rules](https://codexguide.io/guides/codex-rules-prefix-rule)
