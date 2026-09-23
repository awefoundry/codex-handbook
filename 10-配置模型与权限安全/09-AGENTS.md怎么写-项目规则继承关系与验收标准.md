# Codex AGENTS.md教程：项目规则、读取范围与生效检查

`AGENTS.md` 用来保存会在多个任务中重复使用的项目约定：项目是什么、哪些目录可以改、怎样验证、哪些动作要先请人确认。它能减少重复提醒，但不能替你决定需求，也不能代替沙箱、操作系统权限、审批或人工验收。

本文沿用原文的项目规则、继承关系和验收思路，补上一个不依赖 Node 或测试脚本的本地网页练习。练习只使用 `/tmp` 下的副本；示例输出是帮助你判断结果的样子，不代表本机已经完成一次模型任务。

## 它解决什么问题

把下面这些稳定约定写进项目规则，Codex 每次进入项目时都能获得同一份上下文：

- 项目的用途、主要目录和工作边界；
- 真实存在的启动、检查或构建命令；
- 哪些文件允许修改，哪些文件由工具生成；
- 什么时候算完成，删除、部署、生产写入等动作何时必须停下来请人确认。

它不解决下面几件事：

- **不等于安全隔离**：写“不要删除文件”不能阻止命令删除文件。能访问什么由沙箱、操作系统权限和审批共同决定；
- **不等于任务提示**：当前任务的目标、范围和交付时间仍应写在本次请求里；
- **不等于 `config.toml`**：配置文件控制模型、沙箱、审批等运行设置，`AGENTS.md` 主要提供项目上下文和协作约定；
- **不等于测试结果**：Codex 说“我已读取”只是一段回复，不能证明读取了预期文件。要用路径、diff、命令输出或页面检查核对。

## 它和提示词、配置、权限怎么分工

| 载体 | 负责什么 | 适合放什么 | 不能代替什么 |
| --- | --- | --- | --- |
| 一次性任务提示 | 当前目标和当前限制 | “只改 `index.html`，完成后说明检查结果” | 长期项目约定 |
| `AGENTS.md` | 项目规则和验收习惯 | 目录边界、真实命令、完成标准 | 沙箱、权限和需求判断 |
| `config.toml` | Codex 的运行配置 | 模型、推理强度、审批和沙箱默认值 | 项目业务规则 |
| 运行权限 | 能访问和执行什么 | 工作区写入、网络、系统资源 | 判断修改是否正确 |

## 当前官方读取规则

下面是依据 [OpenAI 的 AGENTS.md 文档](https://developers.openai.com/codex/agent-configuration/agents-md)整理的规则，核对日期为 **2026-09-22**。具体入口仍可能随 Codex 版本变化，遇到差异应以当前文档和 `codex --help` 为准。

1. **全局层**：默认在 `CODEX_HOME` 指向的目录中查找；没有设置时通常是 `~/.codex`。同一目录优先使用非空的 `AGENTS.override.md`，没有它才使用 `AGENTS.md`。
2. **项目层**：从项目根目录（通常是 Git 根目录）走到当前工作目录；如果找不到项目根，就只检查当前目录。每一级目录按 `AGENTS.override.md`、`AGENTS.md` 和 `project_doc_fallback_filenames` 中的备用文件名查找，每一级最多加入一个文件。
3. **合并顺序**：先加入根目录规则，再加入更靠近当前目录的规则。后加入的具体规则可以补充或覆盖前面的约定。
4. **大小上限**：合并后的项目说明默认受 `project_doc_max_bytes` 限制，官方文档当前给出的默认值是 32 KiB。太长时，应拆到更具体的目录或在确认影响后调整上限。
5. **读取时机**：规则在一次运行开始时建立指令链；修改文件后重启 Codex，再检查新的规则是否进入下一次运行。

如果同一目录同时存在 `AGENTS.override.md` 和 `AGENTS.md`，普通文件不会再被加入这一层。备用文件名不是自动猜出来的，必须通过配置声明。

## 用一个独立网页副本练习

这个例子没有 `package.json`、Node 或测试脚本，所以不会编造 `npm test`。它只检查文件范围、HTML 是否存在和 Git diff 是否干净。

### 1. 创建练习目录和规则

在 macOS 或 Linux 终端输入：

```bash
probe="$(mktemp -d /tmp/codex-agents-probe.XXXXXX)"
mkdir -p "$probe"
cd "$probe"

cat > index.html <<'HTML'
<!doctype html>
<html lang="zh-CN">
  <meta charset="utf-8">
  <title>规则练习页</title>
  <body>
    <h1>第一次修改前</h1>
    <p>这是一份可回滚的本地网页副本。</p>
  </body>
</html>
HTML

cat > AGENTS.md <<'RULES'
# 练习项目规则

- 这是一个只有一个 HTML 文件的练习项目。
- 本次任务只允许修改 `index.html`，不要创建或删除其他文件。
- 修改后检查 `git diff --check`，并说明实际检查了什么。
- 这个项目没有测试脚本，不要运行或声称运行 `npm test`。
RULES

git init -q
git add index.html AGENTS.md
git commit -qm "建立 AGENTS.md 练习基线"
printf '练习目录：%s\n' "$probe"
```

正常应看到一个临时目录路径。先运行 `git status --short --branch`，应只有分支信息，没有未提交改动。路径或权限异常时，先确认 `probe` 变量和当前目录，再继续。

### 2. 让 Codex 先报告规则来源

在同一目录启动一次只读任务：

```bash
codex exec --ephemeral --sandbox read-only -C "$probe" \
  "先不要修改文件。列出你实际读取的 AGENTS.md 路径，说明每条规则如何限制本次任务，并指出项目是否存在可运行的测试命令。最后给出你会检查的文件。"
```

正常回答应至少提到练习目录中的 `AGENTS.md`、只修改 `index.html`、不运行不存在的测试。这里的回答只是线索；把它保存下来或让模型自报路径，都不能单独证明规则已生效。当前环境若未登录或无法连接模型，命令会停在认证或网络错误，这只说明客户端任务未完成。

### 3. 用一个小任务检查实际作用

确认基线没有改动后，再执行一个只改标题的任务：

```bash
codex exec --ephemeral --sandbox workspace-write -C "$probe" \
  "把 index.html 的 h1 改成‘规则已生效’，只修改这个文件。完成后说明实际运行过的检查；不要创建、删除或修改其他文件。"
```

接着由你自己检查：

```bash
git status --short
git diff -- index.html
git diff --name-only
git diff --check
```

正常结果是：只有 `index.html` 出现在差异中，`h1` 改成了目标文字，`git diff --check` 没有输出。若出现其他文件、没有 diff 或检查命令被跳过，先不要宣布规则生效；回到规则路径、当前工作目录和权限设置逐项核对。即使规则写了“不要删除文件”，也仍要把删除动作当作高风险操作单独确认。

## 怎样确认规则来源和覆盖关系

在练习目录逐层查看，而不是只看根目录：

```bash
find "$probe" \( -name 'AGENTS.md' -o -name 'AGENTS.override.md' \) -print
printf '项目根：'; git rev-parse --show-toplevel
printf '当前目录：'; pwd
```

如果要练习子目录覆盖，可以创建 `pages/AGENTS.override.md`，然后从 `pages/` 启动下一次 Codex：

```bash
mkdir -p "$probe/pages"
cat > "$probe/pages/AGENTS.override.md" <<'RULES'
# 子目录规则

- 当前目录的任务只能修改当前目录中的文件。
RULES

cd "$probe/pages"
git rev-parse --show-toplevel
```

正常应仍然返回练习项目根目录；下一次运行时，根目录规则先进入，`pages/AGENTS.override.md` 再补充当前目录限制。若普通 `AGENTS.md` 与 override 同层，先检查是否误以为两份都会合并。

## 没生效时按这个顺序排查

1. **目录**：确认启动目录在目标项目内，`git rev-parse --show-toplevel` 返回了预期根目录。
2. **文件名**：确认是 `AGENTS.md` 或 `AGENTS.override.md`，不是 `AGENTS.md.txt`；文件不能是空的。
3. **同层替代**：检查同一目录是否有 override 文件，或配置是否指定了另一个 fallback 文件名。
4. **范围**：确认规则所在目录确实覆盖当前要改的文件；更具体目录的规则可能改变前面的约定。
5. **大小和语法**：检查规则是否超过 `project_doc_max_bytes`，Markdown 标题和列表是否写完整。
6. **重启**：关闭当前运行，重新从目标目录启动；不要假设改完文件后旧会话会自动重载。
7. **证据**：重新查看模型列出的路径、`git diff --name-only` 和实际检查输出。只凭“我读到了”仍然不够。

## 修改或移除练习规则

先保留回滚点，再修改规则：

```bash
cp AGENTS.md AGENTS.md.bak
$EDITOR AGENTS.md
git diff -- AGENTS.md
```

确认新规则在下一次运行中被读取后，再删除备份：

```bash
rm AGENTS.md.bak
```

要移除规则，先删掉练习目录里的文件，再启动一次只读任务确认没有其他层级的同名规则。不要直接删除真实项目或用户目录中的规则；先查看 `git status`、备份文件和影响范围。

## 相关阅读与资料边界

- [OpenAI：Custom instructions with AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Codex config.toml 配置指南](./08-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
- [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- [从目录到入口](../03-项目理解与上下文/03-从目录到入口-找到真正需要修改的代码.md)

本文的官方读取规则于 2026-09-22 核对。本轮（2026-09-23）核对到 Codex CLI 0.156.0 的版本和帮助文本；没有把隔离环境中的模型调用、App、IDE 或网页展示说成已实测。
