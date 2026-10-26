---
id: agents-md
title: Codex AGENTS.md 怎么写（2026-10 更新）：项目规则继承、验收标准，以及和 Memories、Skills 怎么分工
seo_title: Codex AGENTS.md 怎么写：继承规则、验收与 Memories/Skills 分工
description: AGENTS.md 用来固定项目约定、目录边界和验收命令。本文按官方文档更新读取与合并规则（override、fallback、32 KiB 上限），说明它和 config.toml、Memories、Skills 的分工，并给出一套能用文件和 diff 证明规则生效的本地验收方法。
lede: 必须遵守的规则写进仓库里的 AGENTS.md；可以忘的偏好交给 Memories；可复用的流程做成 Skill。
url: /advanced/agents-md
status: published
section: advanced
category: F-config-model-security
topic: 配置模型与权限安全
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App, IDE]
difficulty: 进阶
order: 9
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-09-22
date_modified: 2026-10-23
official_ref: https://learn.chatgpt.com/docs/agent-configuration/agents-md
keywords: [Codex AGENTS.md, AGENTS.override.md, project_doc_max_bytes, project_doc_fallback_filenames, Codex 项目规则]
related: [codex-memories, create-codex-skill]
faq:
  - q: 改了 AGENTS.md，当前会话会马上用新规则吗？
    a: 不会。官方说明 Codex 在每次运行开始时建立指令链，TUI 通常是每次启动会话时一次。改完要重新启动 Codex 或开新命令。
  - q: 同一目录同时有 AGENTS.md 和 AGENTS.override.md，会合并吗？
    a: 不会。每个目录最多只取一个文件，顺序是 AGENTS.override.md、AGENTS.md、fallback 文件名，取到第一个非空的就停。
  - q: 团队规则能只放在 Memories 里吗？
    a: 不建议。官方 Memories 文档明确说，必须遵守的团队规则应放在 AGENTS.md 或入库文档里，记忆只是辅助的回忆层。
---

# Codex AGENTS.md 怎么写（2026-10 更新）：项目规则继承、验收标准，以及和 Memories、Skills 怎么分工

> 本文在线版：[codexguide.io/advanced/agents-md](https://codexguide.io/advanced/agents-md)

> 核对依据：learn.chatgpt.com 的《Custom instructions with AGENTS.md》《Memories》《Build skills》，2026-10-23 核对。练习命令沿用上一版（2026-09-23 对照 Codex CLI 0.156.0 帮助文本），没有在本次更新中重新跑模型任务。

**2026-10 更新说明**：补了和 Memories、Skills 的分工表；读取规则按当前官方文档重新核对，加上「空文件会被跳过」「到达上限后停止添加」等细节；验收部分改为优先使用官方给的检查命令。

`AGENTS.md` 存的是要在很多任务里反复用到的项目约定：项目是做什么的、哪些目录能改、怎么验证、哪些动作必须先问人。它能省掉每次开工时的重复交代，但不能替你判断需求，也代替不了沙箱、系统权限、审批和人工验收。

## 它解决什么，不解决什么

适合写进去的：

- 项目用途、主要目录、工作边界；
- 真实存在的构建、检查、测试命令；
- 哪些文件能改，哪些是工具生成的；
- 怎样算完成；删除、部署、写生产数据这类动作要先停下来确认。

它不负责的：

- **安全隔离**。写一句「不要删除文件」挡不住删除命令。能访问什么，是沙箱、系统权限和审批一起决定的。
- **当次任务**。这次要做什么、范围多大，写在当次的请求里。
- **运行配置**。模型、沙箱、审批默认值放在 `config.toml`。
- **验收结果**。Codex 回一句「我读到了」不算证据，要看路径、diff 和命令输出。

## 和提示词、config.toml、Memories、Skills 怎么分工

一条规则该写 AGENTS.md 还是交给 Memories、要不要做成 Skill，可以按下表分。表是本站的分法，依据是官方各自文档的定位。

| 载体 | 管什么 | 适合放 | 不适合放 |
| --- | --- | --- | --- |
| 当次提示词 | 这一次的目标和限制 | 「只改 `index.html`，改完说明检查结果」 | 长期约定 |
| `AGENTS.md` | 项目必须遵守的规则 | 目录边界、真实命令、完成标准、必须先问人的动作 | 密钥、一次性任务、权限隔离 |
| `config.toml` | Codex 自身的运行配置 | 模型、推理强度、审批和沙箱默认值、`project_doc_max_bytes` | 业务规则 |
| Memories | 从过往对话里提炼的本机回忆 | 个人偏好、上次的排查习惯这类可以忘、可以过期的东西 | 团队红线、必须每次都生效的规则 |
| Skills | 可复用的工作流程包 | 有固定步骤、可能带脚本和参考资料的流程，比如「修 CI」「发版检查」 | 每个任务都要遵守的项目约定 |
| 运行权限 | 能访问、能执行什么 | 工作区写入、网络、系统资源 | 判断改得对不对 |

三条判断依据都来自官方文档：

- **Memories**：官方原话是把必须遵守的团队规则放在 `AGENTS.md` 或入库文档里，记忆只当辅助的回忆层。本地 Codex 记忆默认关闭，存在 `~/.codex/memories/`，按机器生效，换台机器就没有了。
- **Skills**：一个 Skill 是带 `SKILL.md` 的目录，Codex 先只看名字和描述，决定要用时才读完整内容。所以 Skill 适合「需要时才调用」的流程，不适合「每次都要遵守」的规则。
- **AGENTS.md**：每次运行开始时都会读进来，适合放始终生效的约定。

一个简单的判断：**这条规则如果某次没生效，会不会出事？** 会出事，写进 AGENTS.md；只是不方便，可以交给 Memories；是一串步骤而不是一条规则，做成 Skill，再在 AGENTS.md 里写一句什么时候该用它。

## 当前官方读取与合并规则

依据官方《Custom instructions with AGENTS.md》，2026-10-23 核对：

1. **何时读取**：Codex 在启动时建立指令链，每次运行一次；TUI 里通常是每次启动会话一次。改了文件要重启或开新命令才生效，没有需要手动清的缓存。
2. **全局层**：在 Codex home 目录（默认 `~/.codex`，设置了 `CODEX_HOME` 则以它为准）读 `AGENTS.override.md`，没有才读 `AGENTS.md`。这一层只用第一个非空文件。
3. **项目层**：从项目根（通常是 Git 根）往下走到当前工作目录；找不到项目根就只看当前目录。每一级按 `AGENTS.override.md` → `AGENTS.md` → `project_doc_fallback_filenames` 里的名字依次找，**每个目录最多取一个文件**。
4. **合并顺序**：从根往下拼接，中间用空行隔开。越靠近当前目录的文件越靠后，所以能覆盖前面的约定。
5. **空文件与上限**：空文件会被跳过；合并后的大小到达 `project_doc_max_bytes`（默认 32 KiB）就停止添加。内容太多时，提高上限或拆到更具体的子目录。
6. **fallback 文件名**：不会自动识别。要在 `config.toml` 里写 `project_doc_fallback_filenames`，例如 `["TEAM_GUIDE.md", ".agents.md"]`；不在列表里的文件名一律忽略。

两个容易踩的点：同一目录里有 `AGENTS.override.md` 时，同目录的 `AGENTS.md` 会被忽略；Codex 只往下走到当前目录为止，所以专用规则要放在离那部分代码最近的地方。

## 最小可维护模板

```markdown
# 项目规则

## 项目是什么
- 一句话说明用途和主要目录。

## 可以改的范围
- 允许修改：`src/`、`docs/`
- 不要手改：`dist/`（构建生成）

## 命令（只写真实存在的）
- 安装依赖：……
- 检查：……
- 测试：……（项目没有测试就写「没有测试脚本，不要声称运行过测试」）

## 怎样算完成
- 相关检查命令通过，并在回复里贴出实际输出。
- 说明改了哪些文件。

## 必须先问人的动作
- 删除文件、改数据库结构、部署、改 CI 配置、新增生产依赖。
```

写的时候注意三点：命令要真实存在，写一个跑不了的 `npm test` 只会让 Codex 白白报错或乱编结果；「完成」要能检查，「代码质量好」不算；必须先问人的动作，同时也要在审批和沙箱里设好，AGENTS.md 只是提醒。

如果项目用 Codex 做 GitHub 代码审查，官方建议在离相关代码最近的 `AGENTS.md` 里加一个 `## Code Review Rules` 小节，格式和 lint 类检查留给 CI。

## 本地验收：用一个网页副本练习

这个练习不依赖 Node 或测试脚本，只在 `/tmp` 下的副本里做，用文件范围和 Git diff 判断规则是否生效。

### 1. 建练习目录和规则

```bash
probe="$(mktemp -d /tmp/codex-agents-probe.XXXXXX)"
cd "$probe"

cat > index.html <<'HTML'
<!doctype html>
<html lang="zh-CN">
  <meta charset="utf-8">
  <title>规则练习页</title>
  <body>
    <h1>第一次修改前</h1>
  </body>
</html>
HTML

cat > AGENTS.md <<'RULES'
# 练习项目规则

- 这是一个只有一个 HTML 文件的练习项目。
- 本次任务只允许修改 `index.html`，不要创建或删除其他文件。
- 修改后运行 `git diff --check`，并说明实际检查了什么。
- 这个项目没有测试脚本，不要运行或声称运行 `npm test`。
RULES

git init -q && git add . && git commit -qm "AGENTS.md 练习基线"
```

### 2. 先让 Codex 说出它读到了什么

官方给的检查方式是：

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

正常情况下，Codex 会按顺序复述全局和项目规则。这只是线索，不是证据。

想看实际加载了哪些文件，官方建议开启明文 TUI 日志：

```bash
codex -c log_dir=./.codex-log
# 然后查看 ./.codex-log/codex-tui.log
```

### 3. 用一个小任务看规则有没有起作用

```bash
codex exec --sandbox workspace-write -C "$probe" \
  "把 index.html 的 h1 改成‘规则已生效’，只修改这个文件。完成后说明实际运行过的检查。"
```

然后自己检查：

```bash
git status --short
git diff --name-only
git diff --check
```

合格的结果：差异里只有 `index.html`，`h1` 改对了，`git diff --check` 没有输出，回复里没有声称跑过 `npm test`。出现别的文件或者检查被跳过，先别认定规则生效，回到下面的排查顺序。

### 4. 练习子目录覆盖

```bash
mkdir -p "$probe/pages"
cat > "$probe/pages/AGENTS.override.md" <<'RULES'
# 子目录规则
- 当前目录的任务只能修改当前目录中的文件。
RULES

codex --cd pages --ask-for-approval never "Show which instruction files are active."
```

预期顺序：全局文件（如果有）在前，根目录 `AGENTS.md` 其次，`pages/AGENTS.override.md` 最后。

练习完删掉 `$probe` 目录即可。不要在真实项目或 `~/.codex` 里直接删规则文件，先看 `git status` 和影响范围。

## 没生效时按这个顺序查

1. **目录**：是不是在目标项目里启动的？可以用 `codex status` 看工作区根目录对不对。
2. **文件名和内容**：是 `AGENTS.md`，不是 `AGENTS.md.txt`；文件不能是空的。
3. **上层的 override**：往上找有没有 `AGENTS.override.md`，包括 Codex home 目录里的。
4. **fallback 名**：`project_doc_fallback_filenames` 有没有拼错；改完配置要重启。
5. **截断**：合并后是否超过 `project_doc_max_bytes`，靠后的规则可能没进来。
6. **CODEX_HOME**：启动前 `echo $CODEX_HOME`。值不是默认的话，Codex 读的可能不是你改的那个目录。
7. **重启**：关掉当前会话，从目标目录重新启动。
8. **证据**：看日志、`git diff --name-only` 和实际命令输出。

## 常见误区

- **把安全隔离写进 AGENTS.md**。「不要访问网络」要靠沙箱设置，规则只是提醒。
- **把一次性任务写进全局规则**。「这周先修登录 bug」放在 `~/.codex/AGENTS.md` 里，下个项目也会读到。
- **规则只放在 Memories 里**。换台机器、关掉记忆、清空记忆以后，规则就没了。
- **把长流程塞进 AGENTS.md**。几十步的发版流程每次都读进上下文，占预算；做成 Skill，在 AGENTS.md 里写一句什么时候用它。
- **写不存在的命令**。Codex 要么报错，要么在回复里含糊带过。

## 相关阅读

- [Codex config.toml 深入配置](./08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
- [权限与安全边界](https://codexguide.io/advanced/permissions-security)
- [从零创建 Codex Skill](https://codexguide.io/guides/create-codex-skill)
- [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)

## 参考

- [OpenAI：Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI：Memories](https://learn.chatgpt.com/docs/customization/memories)
- [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills)
