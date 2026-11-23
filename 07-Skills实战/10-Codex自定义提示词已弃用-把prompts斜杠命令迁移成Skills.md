---
id: codex-custom-prompts-to-skills
title: "Codex 自定义提示词已弃用：把 ~/.codex/prompts 里的 /prompts 斜杠命令迁移成 Skills"
seo_title: "Codex 自定义提示词已弃用：把 /prompts 迁到 Skills"
description: "Codex 的自定义提示词（~/.codex/prompts 里的 /prompts: 命令）已被官方标为弃用，官方建议改用 Skills。本文说明两者的位置、调用和参数差在哪，并把官方的 draftpr 示例改写成 SKILL.md。0.171.0 上确认了技能能被列出来，以及怎样按名字禁用。"
lede: "旧的提示词文件还在官方文档里，但新的可复用指令应该写成 Skill。占位符不会自动变成 Skill 的参数语法。"
url: /guides/codex-custom-prompts-to-skills
status: published
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, IDE]
difficulty: 进阶
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-23
date_modified: 2026-11-23
verified_on: 2026-11-23
tested_cli_version: 0.171.0
official_ref: https://learn.chatgpt.com/docs/custom-prompts
keywords: [Codex custom prompts, Codex 自定义提示词, "~/.codex/prompts", "/prompts: 斜杠命令", Codex 提示词迁移 Skill]
related: [create-codex-skill, codex-cli-slash-commands, plugin-development-marketplace]
howto: true
faq:
  - q: 自定义提示词是已经不能用了，还是只是不建议再用？
    a: 2026-11-23 的官方页面第一句是 Custom prompts are deprecated，并建议改用 skills。页面仍保留 ~/.codex/prompts 和 /prompts:名字 的写法。文档没有写删除日期，也没有写已经移除。
  - q: Skill 还认 $1 和 $ARGUMENTS 吗？
    a: Build skills 没有写这种占位符。自定义提示词页面才写 $1 到 $9、$ARGUMENTS 和 $FILE 这种命名占位符。迁移时把参数写成自然语言，不要在 SKILL.md 里照抄这套语法并当成还会展开。
  - q: 怎样确认 Codex 看见了新 Skill？
    a: 本文在未登录的 Codex CLI 0.171.0 上用 codex debug prompt-input 看到了仓库 .agents/skills 里的 draft-pr。这不是交互界面的 /skills 菜单，也没有在会话里发送 $draft-pr。
  - q: 旧的 prompts 文件要马上删吗？
    a: 先确认新 Skill 在你自己的会话里能被点名，再删。0.171.0 的 prompt-input 输出里没有出现测试用的 draftpr.md，但这个调试命令展示的是模型可见输入，不能据此判断斜杠命令菜单还加载不加载 prompts。
---

# Codex 自定义提示词已弃用：把 ~/.codex/prompts 里的 /prompts 斜杠命令迁移成 Skills

> 核对依据：2026-11-23 打开的官方文档 [Custom prompts](https://learn.chatgpt.com/docs/custom-prompts) 和 [Build skills](https://learn.chatgpt.com/docs/build-skills)。CLI 行为来自 Linux 上的 `codex-cli 0.171.0`：`codex login status` 为 `Not logged in`，`codex debug prompt-input` 在独立 `CODEX_HOME` 和一个临时 Git 仓库里运行。没有打开 TUI 或 IDE，没有发送 `$draft-pr`，没有配图。

官方页面现在的第一句是：Custom prompts are deprecated. Use skills。自定义提示词还写在文档里，调用方式仍是 `/prompts:` 加上文件名。新的可复用指令按 [Build skills](https://learn.chatgpt.com/docs/build-skills) 写成一个目录里的 `SKILL.md`。

Skill 的文件结构、`$skill-creator` 和打包见 [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)。斜杠命令总表见 [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)。要把 Skill 分发给别人，再看 [插件市场](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)。

## 先说结论

弃用的是 `~/.codex/prompts/` 里的自定义提示词，不是 Skill，也不是 Codex 自带的斜杠命令。官方没有写移除日期。0.171.0 上本文没有打开斜杠菜单，所以不能判断 `/prompts:draftpr` 今天还会不会出现。

应该迁到 Skill 的原因，页面写了两条：提示词只放在本机 Codex 主目录，不会随仓库分享；它们必须显式调用。Skill 可以放进仓库，也可以被隐式选中。

迁移时不要假设 `$1` 到 `$9` 在 `SKILL.md` 里还会展开。Build skills 没有这套语法。

## 自定义提示词和 Skills 的区别

| | 自定义提示词 | Skill |
|---|---|---|
| 官方状态 | deprecated，页面仍保留用法 | 现行的可复用指令格式 |
| 位置 | `~/.codex/prompts/`，只扫这一层的 Markdown | 仓库 `.agents/skills`、`$HOME/.agents/skills`、`/etc/codex/skills`，以及随 Codex 自带的系统技能 |
| 谁能一起用 | 不通过仓库分享 | 仓库里的可以提交；要分发给别人再用插件 |
| 怎么调用 | `/prompts:<文件名>`，例如 `/prompts:draftpr` | Codex CLI 和 IDE 里用 `/skills`，或输入 `$` 点名 |
| 会不会自己选中 | 页面写明需要显式调用 | 默认可以按 `description` 隐式选中；`allow_implicit_invocation: false` 后只接受显式 `$` |
| 参数 | `$1`～`$9`、`$ARGUMENTS`、`$FILE` 这类大写名字、`$$` 表示字面 `$` | 文档要求在 `description` 和正文里写清输入，没有写上述占位符 |
| 改完何时生效 | 重启 Codex，或新开一个对话 | 文档写 Codex 会自动发现技能变化；没出现时再重启。`[[skills.config]]` 改完要重启 |

自定义提示词的 front matter 用 `description` 和 `argument-hint`。Skill 的 `SKILL.md` 必须有 `name` 和 `description`。两边的 `description` 不是同一个加载器。

提示词目录只认顶层 Markdown。`~/.codex/prompts/nested/hidden.md` 和 `notes.txt` 这种文件，按文档不会变成命令。文件名就是命令名：`draftpr.md` 对应 `/prompts:draftpr`。

## 盘点现有 prompts

先看目录里实际有哪些文件：

```bash
find ~/.codex/prompts -maxdepth 1 -type f -name '*.md'
```

官方示例是 `~/.codex/prompts/draftpr.md`：

```markdown
---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---

Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
Commit the staged changes with a clear message.
Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.
```

调用例子是：

```text
/prompts:draftpr FILES="src/pages/index.astro src/lib/api.ts" PR_TITLE="Add hero animation"
```

文档写：Codex 展开文件内容，换掉占位符，再把结果当作一条消息发送。改完文件要重启会话或新开对话。

2026-11-23 在独立 `CODEX_HOME` 里放了这份 `prompts/draftpr.md`，以及一个子目录 Markdown 和一个非 Markdown 文件，然后运行 `codex debug prompt-input`。输出的模型可见输入里没有 `draftpr`、`/prompts:` 或 `prompts/`。同一条命令清楚地列出了 Skill。因此只能说 **这个调试视图没有展示自定义提示词**，不能说 0.171.0 已经停止加载它们。斜杠菜单要在你自己的 CLI 或 IDE 会话里看。

## 把 draftpr.md 改写成 Skill

下面这份 `SKILL.md` 是按官方 `draftpr` 示例改写的，不是 OpenAI 仓库里的文件。`name` 用 `draft-pr`。参数不再写 `$FILES` 和 `$PR_TITLE`，改成正文里的输入说明。

```markdown
---
name: draft-pr
description: Prepare a branch, commit, and open a draft pull request when the user asks to open a draft PR. Do not use for an ordinary commit, a code review, or a PR that should be ready for review immediately.
---

When the user asks to open a draft pull request:

1. Create a branch named `dev/<feature_name>` unless the user already named a branch.
2. If the user names files, stage those files. Otherwise, inspect the working tree and say which files you intend to include before staging.
3. Commit the staged changes with a message that states the change.
4. Open a draft pull request on that branch. If the user supplies a title, use it. Otherwise write a one-line summary from the diff.
5. Stop after you report the branch name and the pull request URL. Do not merge it.
```

描述里写了「什么时候用」和「什么时候不用」。Build skills 要求把触发场景写在 `description` 前面，因为技能很多时描述会被截短。

本文实际放进临时仓库、并被 Codex 列出来的，是更短的一份，用来确认发现机制，而不是上面的完整步骤：

```markdown
---
name: draft-pr
description: Prepare a branch, commit, and open a draft pull request when the user asks to open a draft PR.
---

When asked, describe the steps. Do not run git commands in this test.
```

`codex debug prompt-input` 的可用技能里出现了这一条（路径里的用户目录已换成仓库根的相对写法）：

```text
- draft-pr: Prepare a branch, commit, and open a draft pull request when the user asks to open a draft PR. (file: r1/draft-pr/SKILL.md)
```

这里的 `r1` 是该次输出给仓库 `.agents/skills` 起的标记。同一次列表里还有官方点名的系统技能 `skill-creator` 和 `skill-installer`。另外还看到 `imagegen` 和 `openai-docs`。Build skills 页没有把后两个逐个写进系统技能表，这里只记录出现过，不展开它们做什么。

没有在会话里发送 `$draft-pr`，所以上面的步骤没有被执行，也没有创建分支或 PR。

## 放在哪

| 范围 | 位置 | 这次怎么验证的 |
|---|---|---|
| 当前仓库 | `<仓库>/.agents/skills/draft-pr/SKILL.md` | 临时 Git 仓库里，`prompt-input` 列出了 `draft-pr` |
| 个人、所有仓库 | `$HOME/.agents/skills/<name>/SKILL.md` | 文档如此。本文没有把 `draft-pr` 再复制到用户目录测一次 |
| 机器上的默认技能 | `/etc/codex/skills` | 只按文档，没有写入 |

仓库从当前工作目录一直扫到仓库根。同名技能不合并，选择器里可能同时出现。个人目录适合只有你自己用的提示词；团队要一起用的，放进仓库再审查。

Windows 上的用户目录以你本机 `/skills` 列表里的路径为准。文档写支持符号链接。

## 调用与触发

显式调用按 Build skills：在 Codex CLI 或 IDE 的输入里用 `$` 选中技能，或打开 `/skills`。按本文这份示例，名字是 `$draft-pr`。本文没有在会话里发送这个调用。

不想让它在别人只是提到 “PR” 时就被选中，可以在技能目录里加 `agents/openai.yaml`：

```yaml
policy:
  allow_implicit_invocation: false
```

文档写默认是 `true`。设为 `false` 后，隐式选中停止，显式 `$` 仍然可用。本文没有改这个字段再观察一次会话，所以没有「设成 false 之后还被自动选中」或「不再选中」的运行记录。

暂时停用、但先不删文件，用 `~/.codex/config.toml`：

```toml
[[skills.config]]
name = "draft-pr"
enabled = false
```

文档要求每条只写一个选择器：绝对 `path` 对准一个 `SKILL.md`，或 `name` 匹配所有同名技能。多条匹配时，最后一条生效。改完要重启 Codex。

2026-11-23 在同一个独立 `CODEX_HOME` 里写入上面的 `name = "draft-pr"`、`enabled = false`，再跑一次 `prompt-input`。输出里不再有 `draft-pr`，同一仓库里的其他技能还在。这是新进程重新读取配置的结果，不是在一个已经打开的 TUI 里热更新。

系统自带技能可以用项目里受信任的 `.codex/config.toml` 关掉，文档的键是：

```toml
[skills.bundled]
enabled = false
```

本文没有改这个键。

## 验证与回退

可以按这个顺序检查，做完再删旧文件：

1. `SKILL.md` 在 `.agents/skills/<name>/` 或 `$HOME/.agents/skills/<name>/`，文件名正好是 `SKILL.md`，YAML 能被解析。
2. 新开一个 Codex 进程。本文用的是 `codex debug prompt-input "open a draft PR"`，在未登录时也能打印技能列表。你平时可以用会话里的 `/skills`。两者不要当成同一个界面。
3. 在你自己的会话里显式发送 `$<name>`，看它是否按正文行动。这一步本文没有做。
4. 确认之后，再删除或移走 `~/.codex/prompts/<name>.md`。删之前留一份副本。文档没有说删掉 Skill 之后旧的 `/prompts:` 命令会自动失效；那是两个目录。

如果列表里没有新技能，先看是不是放进了子目录、文件名是不是 `SKILL.md`、`name` 有没有和别的技能冲突，以及 `[[skills.config]]` 是不是把它关了。

0.171.0 没有登录时，`codex exec` 不能完成一次真正的模型回复。本文因此用 `prompt-input` 看发现结果，而不是用 `codex exec` 假装跑通了草稿 PR。

## 参考资料

- [Custom prompts](https://learn.chatgpt.com/docs/custom-prompts)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)
- [斜杠命令与快捷键](../01-安装与首次使用/14-斜杠命令与快捷键.md)
- [用插件分发](../08-插件工作流/06-Codex插件开发入门-用plugin-creator打包并通过marketplace分发.md)

查询日期 2026-11-23。页面若去掉 deprecated 或改掉占位符，以当天的 Custom prompts 和 Build skills 为准。
