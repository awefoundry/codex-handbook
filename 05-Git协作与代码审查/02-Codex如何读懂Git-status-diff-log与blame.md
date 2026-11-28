---
id: codex-git-status-diff-log-blame
title: "Codex 读懂 Git：status、diff、log、blame 先固定比较基线，再用 /review 和审查面板核对改动范围"
description: "读 Git 先固定比的是哪两边。本文按 git-scm 说明 status、diff、log 和 blame，并对照审查面板的 Unstaged、Staged、Commit、Branch，以及 CLI 的 /review 和 /diff。"
lede: "工作区、暂存区、某次提交和相对基准分支的差异是不同的现场。先记下 HEAD，再决定看哪一份 diff。"
url: /guides/codex-git-status-diff-log-blame
status: published
section: guides
category: E-git-collab
topic: 开发、测试与代码协作
content_type: 教程
source_tag: 官方功能
entry_tags: [CLI, App]
difficulty: 基础
order: 2
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-12
date_modified: 2026-11-28
verified_on: 2026-11-28
official_ref: https://git-scm.com/docs/git-diff
keywords: [git status, git diff, git log, git blame, Codex /review, Codex 审查面板, git diff --cached]
related: [codex-local-code-review, codex-reviewable-commit-pr, permissions-sandbox-approvals]
howto: true
faq:
  - q: "git diff 是空的，是不是没有改代码？"
    a: "默认的 git diff 只比较工作区和暂存区。已经暂存的内容看 git diff --cached（--staged 是同义词）。未跟踪文件不在这两份 diff 里，用 git status 或 git ls-files --others --exclude-standard。"
  - q: "审查面板的 Unstaged 和 git diff 是不是同一份？"
    a: "Code review 页写明，审查面板默认显示 Unstaged。git-scm 写明不带提交参数的 git diff 是工作区相对暂存区的改动。两边都是「还没放进暂存区的已跟踪改动」。未跟踪文件不会出现在 git diff 里。"
  - q: "CLI 的 /review 会改工作区吗？"
    a: "Code review 页写明，/review 报告按优先级排列的发现，不修改工作区。Developer commands 里的 /diff 用来看已暂存、未暂存和尚未跟踪的文件。"
  - q: "blame 上的名字是不是这个 Bug 的责任人？"
    a: "git blame 标注的是最后修改这一行的提交、作者和日期。它不说明谁应该为问题负责，也不说明这行最初为什么存在。合并、格式化和 cherry-pick 都会让最后修改者和最初设计者不同。"
---

# Codex 读懂 Git：status、diff、log、blame 先固定比较基线，再用 /review 和审查面板核对改动范围

> 本文在线版：[codexguide.io/guides/codex-git-status-diff-log-blame](https://codexguide.io/guides/codex-git-status-diff-log-blame)

> 核对依据：2026-11-28 打开的 [git status](https://git-scm.com/docs/git-status)、[git diff](https://git-scm.com/docs/git-diff)、[git log](https://git-scm.com/docs/git-log)、[git blame](https://git-scm.com/docs/git-blame)，以及同一天的 [Code review](https://learn.chatgpt.com/docs/code-review) 和 [Developer commands](https://learn.chatgpt.com/docs/developer-commands)。命令含义按这些页面。早先文稿里的命令输出记录于 Windows build 26100、Codex CLI 0.147.0 和 Git 2.47.0.windows.2，2026-08-30。这次没有重跑那套环境，也没有打开桌面端的审查面板。

## 先问对问题

代码审查的第一步是先把比较范围说清楚。不要直接让 Codex 总结「这个提交做了什么」，因为当前工作区、暂存区、某个提交和远程分支可能是四个不同的现场。

四条命令各自回答一个问题。

| 命令 | 它主要回答 | 它不能单独证明 |
| --- | --- | --- |
| `git status` | 当前分支和文件处于什么状态 | 改动的具体行为是否正确 |
| `git diff` | 两个版本之间具体改了哪些内容 | 未跟踪文件是否已经纳入比较 |
| `git log` / `git show` | 提交按什么顺序发生，某次提交改了什么 | 提交信息里的动机一定真实 |
| `git blame` | 某一行最后由哪个提交写入 | 谁应该为问题负责，或这行最初为何存在 |

把它们连起来，才能形成可复核的证据链。`status` 定位现场，`diff` 读取行为，`log` 补历史，`blame` 在有疑问的行上继续追溯。Codex 的 `/review` 和桌面端审查面板用的也是这些范围，对照关系见后文。本地审查命令的参数见 [本地代码审查](./07-Codex本地代码审查-review命令与codex-review.md)。

## 先固定比较基线

在 Codex 读取代码前，先在仓库根目录运行下面的只读命令。

```powershell
Get-Location
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --verify HEAD
git status --short --branch
```

这里要记录当前目录、Git 根目录、分支名和 `HEAD` 的提交号。`HEAD` 是当前检出的提交，不一定是远程分支的最新提交。`git status` 的 `--short` 给出短格式，`--branch` 即使在短格式里也显示分支和跟踪信息。`ahead` 和 `behind` 是相对上游分支的计数；文档里的 `--ahead-behind` 默认显示这份计数。没有配置上游时，不要把缺了这对数字理解成「已经同步」。

如果任务针对某个目标分支，再单独确认它是否存在。

```powershell
git show-ref --verify --quiet refs/remotes/origin/main; $LASTEXITCODE
git rev-parse --verify origin/main
```

命令返回非零只表示本地没有可用的 `origin/main` 引用，不表示应该马上拉取或切换分支。工作区有别人未提交的改动时，先记录现场，再由负责人决定是否同步或隔离。拉取和切换都不是只读检查。

## 一、`git status`，先读现场，再读内容

### 分支行和文件行

```text
git status --short --branch
```

可能看到下面的输出。

```text
## fix/login-error...origin/main [ahead 1, behind 2]
 M src/components/LoginForm.tsx
M  tests/login-form.test.tsx
MM src/api/login.ts
?? notes/repro.txt
```

第一行是短格式里的分支行：当前分支、跟踪的上游，以及 ahead / behind。文件行是两个字母的 `XY`。不在合并冲突里时，`X` 是暂存区（index），`Y` 是工作区。文档里空格表示 unmodified，`M` 表示 modified，`A` 表示 added，`D` 表示 deleted，`??` 表示未跟踪。忽略文件默认不列出；打开 `--ignored` 时用 `!!`。

短格式里的空格会在排版里看丢。按列来读：

| 你看到的两列 | 含义 |
| --- | --- |
| 左空格、右 `M` | 只改了工作区，还没暂存 |
| 左 `M`、右空格 | 已暂存，工作区没有在此之上再改 |
| `MM` | 暂存之后，工作区又继续改了 |
| 左 `A`、右空格 | 新文件已暂存 |
| 左 `D`、右空格 | 删除已暂存 |
| `??` | 未跟踪，还没有进入 Git 的 diff |

上面示例里，`LoginForm.tsx` 是左空格右 `M`，`login-form.test.tsx` 是左 `M` 右空格，`login.ts` 是 `MM`，`notes/repro.txt` 是未跟踪。

`git status` 是状态摘要。文档写明它列出三类路径：暂存区相对 `HEAD` 的差异（也就是 `git commit` 会提交的）、工作区相对暂存区的差异，以及未跟踪、且没被忽略的路径。它不会告诉你某个函数具体改了几行。`??` 也不能直接当成临时垃圾，它可能是测试、迁移脚本或需要纳入提交的说明。先确认来源。`notes/` 这类未跟踪文件里可能有个人记录，阅读时不要把内容贴到对话或评审说明里，除非已经确认可以公开。

需要给脚本或 Codex 稳定解析时，可以使用：

```powershell
git status --porcelain=v1 -b
```

`--porcelain` 的格式跨 Git 版本、也不跟随用户配置变化，适合解析。版本默认是 `v1`。和短格式相比，v1 不使用 `color.status`，路径始终相对仓库根目录，而不是你当前所在的子目录。`-b` 就是 `--branch`。

不要把「工作区干净」理解成「已经和远程同步」。状态里没有文件行，只说明相对当前 `HEAD` 没有已识别的工作区和暂存区改动，也没有列出未跟踪文件。分支跟踪和远程引用是否最新，还要看分支行，以及你有没有刚刚更新过远程引用。

## 二、`git diff`，先说清楚比较哪两边

最常见的误判是只运行一次 `git diff`。git-scm 写明：不带提交参数的 `git diff` 看的是你相对暂存区做了、但还没放进暂存区的改动。它不显示已经暂存的内容，也不列出未跟踪文件。

| 命令 | 文档里的比较 | 适合回答 |
| --- | --- | --- |
| `git diff` | 工作区相对暂存区 | 还有哪些改动没暂存 |
| `git diff --cached` | 暂存区相对给定提交；不写提交时是 `HEAD` | 下次提交会包含什么 |
| `git diff HEAD` | 工作区相对 `HEAD` | 相对最新提交，工作区里已跟踪文件现在长什么样 |
| `git diff origin/main...HEAD` | 从双方的共同祖先到 `HEAD` | 当前分支从分叉点起新增了什么 |
| `git diff <commit>^ <commit>` | 两个提交之间 | 某次提交相对它的父提交引入了什么 |

`--staged` 是 `--cached` 的同义词。文档里的例子把 `git diff HEAD` 说成「最新提交以来的全部改动」。更精确的定义是工作区相对这个提交。已经暂存、且工作区里仍是那份内容的改动，会包含在这份差异里，因为工作区已经和 `HEAD` 不同。它不是把 `git diff` 和 `git diff --cached` 两段输出拼在一起。未跟踪文件仍然不会出现。

`git diff A...B` 的官方定义是：看包含第二个提交的那一侧、从两个提交的共同祖先算起的变化。`git diff A...B` 等价于 `git diff $(git merge-base A B) B`。因此 `git diff origin/main...HEAD` 是从合并基点到当前 `HEAD`，不是 `origin/main` 上独有、还没进当前分支的那些提交。省略其中一边时，省略的那边按 `HEAD` 处理。两个点的 `git diff A B` 是直接比较两个尖端，和三个点不是同一份差异。

审查前通常先看摘要和文件名。

```powershell
git diff --stat
git diff --name-status
git diff --cached --stat
git diff --cached --name-status
git ls-files --others --exclude-standard
```

再按比较范围展开。

```powershell
git diff -- src/api/login.ts
git diff --cached -- tests/login-form.test.tsx
git diff HEAD -- src/api/login.ts tests/login-form.test.tsx
git diff --check
```

命令末尾的 `--` 用来分隔选项和路径。git-scm 的例子写明：文件名通常可以直接放在最后，`--` 用来避免歧义。`git diff --check` 在改动引入冲突标记或空白错误时发出警告，并在发现问题后以非零状态退出。哪些算空白错误由 `core.whitespace` 决定。退出状态为 0 只表示这次没有发现这类问题，不表示测试、逻辑或安全性已经通过。

### 如何读一段 patch

```diff
@@ -18,7 +18,9 @@ function submitLogin() {
-  setSubmitting(true);
+  setSubmitting(true);
+  setError(null);
   return requestLogin(credentials);
```

`@@` 后面的数字是旧文件和新文件的行范围；`-` 是旧内容，`+` 是新内容，没有前缀的是上下文。先问「状态变化是什么」，再问「异常路径、权限边界和调用方是否也变化」。只看到一行 `setError(null)`，不能直接断言用户体验已经修好，还要查看失败分支和对应测试。

重命名和移动可能让文件列表看起来比实际行为复杂。

```powershell
git diff --name-status --find-renames HEAD~1 HEAD
git diff --summary HEAD~1 HEAD
```

`--find-renames` 按相似度检测重命名。文档写明默认相似度索引是 50%：一对删除和新增里，如果文件有超过一半没有改，就可以被看成重命名。这是启发式结果，不是文件系统事件。审查时要看内容差异，不能只看 `R` 标记。`--summary` 输出扩展头信息的压缩摘要。文档列举的是创建、重命名和模式变化，用来对照 `--name-status`，不代替补丁正文。

## 三、`git log` 与 `git show`，把改动放回时间线

先看分支图和提交摘要。

```powershell
git log --graph --decorate --oneline --all -n 12
git log --format=fuller -n 5
git show --stat --summary <commit>
```

`log` 适合看顺序、分支和合并关系，`show` 适合查看某次提交的正文和 patch。提交信息是线索。行为证据仍然来自 diff、调用方和验证结果。把记录交给别人时，提交里的作者邮箱和本机路径按你们的要求处理，只保留回答问题所需的提交号和路径。

### 按文件或代码线索查历史

```powershell
git log --follow --oneline -- src/api/login.ts
git log -S'setSubmitting(true)' --oneline -- src/api/login.ts
git log -G'catch|finally' --oneline -- src/api/login.ts
git show <commit> -- src/api/login.ts
```

- `--follow` 在重命名之后继续列出这个文件的历史，而且只适用于单个文件。文档同时写明，在非线性历史上它效果不好，除非写成 `--follow=merges`：那样会为合并的每一个父提交分别跟随路径，开销更大。
- `-S` 查找指定字符串出现次数发生变化的差异，也就是这段文本被加进文件或从文件删掉的提交。出现次数没变的修改不会被选中。
- `-G` 查找补丁里新增或删除的行匹配这个正则表达式的差异。官方举的差别是：同一行调用被改了参数、但函数名出现次数不变时，`-G` 能找到这次提交，`-S` 不能。
- 这些选项只能缩小搜索范围。找到提交后，仍要用 `git show` 读完整上下文，尤其要注意后续提交是否改变了原先的假设。

## 四、`git blame`，追踪一行，不追究责任

怀疑某一行的默认值、异常处理或兼容逻辑时，再使用：

```powershell
git blame -L 20,45 -- src/api/login.ts
```

`-L` 把标注限制在给出的行范围，可以写多次。输出里的短提交号、作者和日期表示该行最后一次被某个提交写入。文档的定义就是：用最后修改这一行的修订来标注每一行。下一步通常是打开对应提交并查看文件历史。

```powershell
git show <commit> -- src/api/login.ts
git log --follow --oneline -- src/api/login.ts
```

整文件重命名会自动跟随。要跟踪文件内部的移动，或从其他文件复制过来的行，再用 `-M` 和 `-C`。

```powershell
git blame -w -M -C -C -L 20,45 -- src/api/login.ts
```

- `-w` 在比较父提交和子提交时忽略空白。
- `-M` 检测同一文件里移动或复制的行。
- `-C` 在此之外，检测同一次提交里其他被修改文件中移过来或复制过来的行。再写一个 `-C`，还会在创建该文件的那次提交里查找。写第三个 `-C`，才会到任意提交里查找。上面的命令是两个 `-C`，没有覆盖「任意提交」。

这些都是启发式判断，可能变慢。合并提交、批量格式化和 cherry-pick 也会让「最后修改者」与「最初设计者」不同。

因此，`blame` 能回答「这行最近由哪个提交改动」，不能回答「谁应该为线上问题负责」。把提交放回 Issue、PR、测试和后续修复的上下文，结论才有意义。

## 一次完整的只读阅读流程

假设 `status` 显示实现文件有未暂存修改，测试文件已暂存，还有一个未跟踪的复现说明。可以按下面顺序读取。

1. 记录仓库根目录、分支、`HEAD` 和 `status --short --branch`，把原有改动和本次任务分开。
2. 用 `git diff --stat`、`git diff --cached --stat` 和 `git ls-files --others --exclude-standard` 确认范围，避免漏读暂存文件或未跟踪证据。
3. 分别阅读 `git diff`、`git diff --cached`，最后用 `git diff HEAD` 看工作区相对 `HEAD` 的已跟踪结果。
4. 对每个行为变化查看 `git show` 或 `git log -- <path>`，必要时用 `-S` 或 `-G` 找到引入它的提交。
5. 只有某一行的历史仍然不清楚时才用 `git blame`，并打开对应提交的完整 diff。
6. 把结论写成「事实、推断、未知、下一步验证」，不要把历史线索或文件名当成测试结果。

需要把同一次阅读收成三组命令时，可以用下面的停点。它们仍然是只读的。未跟踪说明里如果可能有个人信息，只记录文件名，不展开内容。

```powershell
git status --short --branch
git diff --stat
git diff --cached --stat
git ls-files --others --exclude-standard
```

```powershell
git diff --name-status
git diff --cached --name-status
git diff HEAD -- src tests
git diff --check
```

```powershell
git log --graph --decorate --oneline --all -n 8
git log --follow --oneline -- src/api/login.ts
git blame -w -M -C -C -L 20,45 -- src/api/login.ts
```

`git diff --check` 的退出状态为 0，只表示没有发现空白错误或冲突标记。历史那一组把提交顺序、单文件的重命名跟随和行级归属放在一起。输出很长时，保留命令本身，提交只留你设定的条数，blame 只留 `-L` 指定的行。

可以把证据整理成下面的表格。

| 项目 | 记录方式 |
| --- | --- |
| 事实 | `src/api/login.ts` 在工作区改变；失败分支新增 `setError(null)` |
| 推断 | 这可能会清理旧错误提示，但还要确认成功分支和组件渲染逻辑 |
| 未知 | 未看到网络超时、重复点击和取消请求的验证 |
| 下一步 | 查看调用方、相关测试，并运行项目已有的登录测试 |

这个表格不替代代码审查，但能防止把「看起来合理」写成「已经证实」。

## 给 Codex 的只读提示词

```text
先只读检查当前 Git 仓库，不要修改、暂存、提交、推送、拉取、切换分支或清理文件。

先运行并记录下面的信息。
- git rev-parse --show-toplevel
- git branch --show-current
- git rev-parse --verify HEAD
- git status --short --branch
- git diff --stat
- git diff --cached --stat
- git ls-files --others --exclude-standard

然后针对本次变更读取下面的内容。
- 工作区相对暂存区，git diff
- 暂存区相对 HEAD，git diff --cached
- 工作区相对 HEAD，git diff HEAD
- 最近提交，git log --graph --decorate --oneline --all -n 12

请按「事实、推断、未知、建议验证」四栏回答。
1. 哪些文件在工作区、暂存区或未跟踪列表中；
2. 每个差异改变了什么输入、状态、输出或错误路径；
3. 哪些判断还需要查看调用方、Issue、历史提交或测试；
4. 哪些文件看起来与任务无关；
5. 如果追踪单行历史，请给出 git blame 的提交号，并用 git show 复核上下文。

不要把未运行的测试写成「通过」，不要把 blame 的作者当成责任人。
```

如果只想追踪一个可疑常量，可以缩小范围。

```text
只读调查 src/api/login.ts 第 20 到 45 行的超时默认值。
先给出当前 diff，再用 git blame 和 git show 找到引入该值的提交。
区分这次提交实际改变的内容、提交信息声称的目的和仍然未知的兼容性影响。
不要修改文件，也不要补写不存在的测试结果。
```

拿 Codex 的回答与终端输出逐项对照。它如果漏掉 `git diff --cached`、未跟踪文件或比较基线，结论就不完整。让它跑这些 Git 命令之前，权限要允许读取仓库。调查阶段怎样收紧，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

## 小练习，复现一条证据链

练习要同时看见已暂存、未暂存和未跟踪三种状态。当前知识库里没有早先提到的 `git-baseline-demo` 备份目录，不要照着那条路径切换目录。在一份可丢弃的临时仓库里自己放上这三种改动，或在已经同时具备这三种状态的测试仓库副本里运行。不要在真实项目里故意制造脏改动。

```powershell
git status --short --branch
git diff --stat
git diff --cached --stat
git diff HEAD -- src tests
git log --graph --decorate --oneline --all -n 8
```

练习时写下四个答案。

- 哪些文件只在工作区，哪些文件已经进入暂存区？
- `git diff` 和 `git diff --cached` 各自遗漏了什么？
- 最近提交的说明与 patch 是否描述了同一个行为？
- 哪一行值得用 `git blame` 继续追踪，追踪后还缺什么验证？

这个练习只读，不需要提交、推送或清理现场。路径和 `src`、`tests` 对不上时，把最后一条 `git diff HEAD --` 后面的路径换成你仓库里真实有改动的目录。

## 在 Codex 里看改动范围

Git 命令把比较的两端写在参数里。Codex 的审查面板和 `/review` 用一组固定的名字指向这些范围。Code review 页写明：审查面板反映的是整个 Git 仓库的状态，不只是 Codex 改过的文件。里面包括 Codex 的改动、你自己的改动，以及仓库里其他未提交的改动。项目还不在 Git 仓库里时，应用会提示你先建仓库。`/review` 只在打开的项目位于 Git 仓库中时出现。

### 审查面板上的五个范围

默认是 **Unstaged**。可以改成：

| 面板上的名字 | 文档怎么说 | 自己用 Git 核对时 |
| --- | --- | --- |
| Unstaged | 默认视图 | `git diff`：工作区相对暂存区 |
| Staged | Git 的 index | `git diff --staged` 或 `git diff --cached`：暂存区相对 `HEAD` |
| Commit | 选定的某次提交 | `git show <commit>`，或 `git diff <commit>^ <commit>` |
| Branch | 相对基准分支的差异 | 见下面关于两个点和三个点的区别 |
| Last turn | 最近一轮助手的改动 | 没有对应的单条 Git 范围。它不是 `HEAD`，也不是分支差异 |

同一个文件可以既有已暂存的改动，又有未暂存的改动。面板可以在两个视图里各显示一次。这是 Git 的正常状态，对应短格式里的 `MM`。

**Branch** 在审查面板上的原文是相对基准分支的差异，没有写明是两个尖端直接比较，还是从合并基点算起。要和终端对齐时，先选定你要的那一种，再跑命令：`git diff <base> HEAD` 是两个尖端；`git diff <base>...HEAD` 是从 `git merge-base` 到 `HEAD`。不要把面板上的 Branch 默认当成其中某一条。

面板可以暂存和还原，粒度是整份差异、单个文件或单个 hunk。头部有 Stage all、Revert all 这类动作。满意的部分暂存，不要的部分还原。这是在改 Git 的 index 和工作区，已经不是只读阅读。只读核对时不要点这些按钮。

一个本地项目如果包含多个文件夹、各自是不同的 Git 仓库，审查头部可以选择仓库，查看另一个仓库里增加和删除的行。**Last turn** 会看助手最近一轮在这些仓库上的改动，仓库选择处显示 All repos。Unstaged、Staged 和 Branch 则作用于你选中的那一个仓库。

在输入框里输入 `/review`，可以选择 **Review against a base branch** 或 **Review uncommitted changes**。Codex 报告按优先级排列的发现，不改变工作区。IDE 扩展里的选项相同，限制也是项目必须在 Git 仓库中。

### CLI 的 `/review` 和 `/diff`

CLI 里输入 `/review` 会打开审查预设。Code review 页列出的范围是：

- **Review against a base branch**：找到合并基点，审查你的分支差异。这一条和 `git diff <base>...HEAD` 的起点一致，都是共同祖先到当前分支，不是两个尖端的直接比较。
- **Review uncommitted changes**：包含已暂存、未暂存和未跟踪文件。它比单独一条 `git diff` 或 `git diff HEAD` 更宽，因为那两条都不列出未跟踪文件。未跟踪部分要和 `git status` 或 `git ls-files --others --exclude-standard` 一起看。
- **Review a commit**：审查选定提交的那一组改动，对应 `git show <commit>`。
- **Custom review instructions**：按你给的标准审查。

Developer commands 里的操作是：输入 `/review`，如果要看具体文件变化，再输入 `/diff`。预期是总结工作区里的问题，关注行为变化和缺失的测试。审查使用当前会话的模型，除非在 `config.toml` 里设置 `review_model`。这里不指定某一个模型名。`/diff` 会显示已暂存的改动、尚未暂存的改动，以及 Git 还没开始跟踪的文件。

Prompting 页的本地审查还可以把焦点写在同一行，例如 `/review Focus on edge cases and security issues`。审查之后若要改代码，仍走你原来的沙箱和审批，审查本身不改工作区。

可审查的提交怎样按主题拆开，见 [可审查的 Commit 和 PR](./05-怎样写出可审查的Commit和PR-范围验证证据与风险.md)。正确性、安全和测试怎么判断，见 [高质量 Code Review](./06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md)。

## 常见误区与验收清单

- [ ] 能说明 `git diff`、`git diff --cached`、`git diff HEAD` 的比较两端。
- [ ] 能区分工作区、暂存区、未跟踪文件和远程分支关系。
- [ ] 能用 `git show` 把提交摘要还原成具体行为，而不是只复述提交信息。
- [ ] 发现重命名、复制或格式化后，知道 `blame` 结果可能只是启发式归属。
- [ ] 能指出 diff 中没有被现有测试或人工检查覆盖的行为。
- [ ] 没有把 `git blame` 当成责任追究工具，也没有把未运行的测试写成通过。
- [ ] 能说出审查面板的 Unstaged、Staged 和 CLI「审查未提交改动」各自对应哪条 Git 命令，以及哪一条还会带上未跟踪文件。

下面几种说法都不够严谨。

| 说法 | 问题 | 更好的写法 |
| --- | --- | --- |
| 「`git status` 没输出，所以可以直接提交。」 | 可能漏看远程关系、忽略文件或任务基线 | 「相对当前 `HEAD` 没有已跟踪改动；分支同步和提交范围仍需确认。」 |
| 「`git diff` 为空，所以没有改代码。」 | 已暂存改动和未跟踪文件不会出现在默认 diff | 「默认 diff 为空；还需要看 `git diff --cached` 和未跟踪列表。」 |
| 「blame 显示了某人的名字，所以问题是他造成的。」 | blame 只记录最后改动这行的提交 | 「该行最后在某提交中变更，需结合提交上下文和后续验证判断。」 |
| 「审查面板的 Branch 就是 `git diff main...HEAD`。」 | 面板只写了相对基准分支；三个点是 CLI「对照基准分支」那条预设写明的合并基点 | 「先确认用的是面板还是 CLI 预设，再选择两个点或三个点的命令去核对。」 |

## 与其他章节的关系

本文解释怎样阅读 `status`、`diff`、`log` 和 `blame`，以及这些范围在审查面板和 `/review` 里叫什么。它不代替下面几篇：

- 报错或需求会牵动哪些文件，先做 [影响范围](../03-项目理解与上下文/06-从报错或需求反推影响范围.md)，再回来看 diff。
- 提交和 PR 怎样按主题拆开、描述里写什么证据，见 [可审查的 Commit 和 PR](./05-怎样写出可审查的Commit和PR-范围验证证据与风险.md)。
- 正确性、安全、测试和可维护性怎么逐项看，见 [高质量 Code Review](./06-如何做一次高质量CodeReview-正确性安全测试与可维护性.md)。
- `/review` 的预设和 `codex review` 的参数，见 [本地代码审查](./07-Codex本地代码审查-review命令与codex-review.md)。
- 让 Codex 执行这些只读命令时，沙箱和审批放在哪一档，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。

只读检查到此为止。暂存、提交和推送是下一步，不在「把比较基线读清楚」这一步里完成。

## 参考资料

- [git status](https://git-scm.com/docs/git-status)（2026-11-28）
- [git diff](https://git-scm.com/docs/git-diff)（2026-11-28）
- [git log](https://git-scm.com/docs/git-log)（2026-11-28）
- [git blame](https://git-scm.com/docs/git-blame)（2026-11-28）
- [Code review](https://learn.chatgpt.com/docs/code-review)（2026-11-28）
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands)（2026-11-28）
- [Prompting](https://learn.chatgpt.com/docs/prompting)（2026-11-28，Do a local code review）
