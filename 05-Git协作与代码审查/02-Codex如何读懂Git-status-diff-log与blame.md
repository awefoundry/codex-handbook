# Codex 如何读懂 Git，status、diff、log 与 blame

> 难度 基础
>
> 类型 概念与实操

> 测试环境为 Windows build 26100、Codex CLI 0.147.0 和 Git 2.47.0.windows.2，2026-08-30 完成核验。

## 先问对问题

代码审查的第一步是先把比较范围说清楚。不要直接让 Codex 总结“这个提交做了什么”，因为当前工作区、暂存区、某个提交和远程分支可能是四个不同的现场。

四条命令各自回答一个问题。

| 命令 | 它主要回答 | 它不能单独证明 |
| --- | --- | --- |
| `git status` | 当前分支和文件处于什么状态 | 改动的具体行为是否正确 |
| `git diff` | 两个版本之间具体改了哪些内容 | 未跟踪文件是否已经纳入比较 |
| `git log` / `git show` | 提交按什么顺序发生，某次提交改了什么 | 提交信息里的动机一定真实 |
| `git blame` | 某一行最后由哪个提交写入 | 谁应该为问题负责，或这行最初为何存在 |

把它们连起来，才能形成可复核的证据链。`status` 定位现场，`diff` 读取行为，`log` 补历史，`blame` 在有疑问的行上继续追溯。

## 先固定比较基线

在 Codex 读取代码前，先在仓库根目录运行下面的只读命令。

```powershell
Get-Location
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --verify HEAD
git status --short --branch
```

这里要记录当前目录、Git 根目录、分支名和 `HEAD` 的提交号。`HEAD` 是当前检出的提交，不一定是远程分支的最新提交；`status --short --branch` 中的 `ahead` 和 `behind` 只有在已配置跟踪分支、且比较基线明确时才有意义。

如果任务针对某个目标分支，再单独确认它是否存在。

```powershell
git show-ref --verify --quiet refs/remotes/origin/main; $LASTEXITCODE
git rev-parse --verify origin/main
```

命令返回非零只表示本地没有可用的 `origin/main` 引用，不表示应该马上拉取或切换分支。工作区有别人未提交的改动时，先记录现场，再由负责人决定是否同步或隔离。

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

第一行说明当前分支与远程跟踪分支已经分叉。文件名前的两个位置分别代表暂存区（Index）和工作区（Worktree）。

```text
M file.ts       # 只改了工作区
M  file.ts      # 已暂存，工作区没有继续改
MM file.ts      # 暂存后又继续修改
A  file.ts      # 新文件已暂存
D  file.ts      # 删除已暂存
?? file.ts      # 未跟踪文件，尚未进入 Git 比较
```

`git status` 是状态摘要，不会告诉你某个函数具体改了几行。`??` 也不能直接当成临时垃圾，它可能是测试、迁移脚本或需要纳入提交的文档。先确认来源和敏感信息，再决定是否加入版本控制。

需要给脚本或 Codex 稳定解析时，可以使用下面的命令。

```powershell
git status --porcelain=v1 -b
```

不要把“工作区干净”误读成“已经和远程同步”。状态为空只说明相对当前 `HEAD` 没有已识别的工作区和暂存区改动；分支跟踪、远程引用是否最新，还要单独核对。

## 二、`git diff`，先说清楚比较哪两边

最常见的误判是只运行一次 `git diff`。它默认比较“工作区”和“暂存区”，不会显示已经暂存的内容，也不会列出未跟踪文件。

| 命令 | 比较范围 | 适合回答 |
| --- | --- | --- |
| `git diff` | 工作区 vs 暂存区 | 暂存后又改了什么 |
| `git diff --cached` | 暂存区 vs `HEAD` | 下次提交会包含什么 |
| `git diff HEAD` | 工作区和暂存区合计 vs `HEAD` | 当前所有已跟踪改动是什么 |
| `git diff origin/main...HEAD` | 合并基点到当前分支 | 当前分支相对目标分支新增了什么 |
| `git diff <commit>^ <commit>` | 提交的父提交 vs 该提交 | 某次提交实际引入了什么 |

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

命令末尾的 `--` 用来分隔选项和路径。文件名以短横线开头、或路径容易被误识别时，保留这个分隔符。`git diff --check` 只检查空白错误和冲突标记，不能证明逻辑、性能或安全性没有问题。

### 如何读一段 patch

```diff
@@ -18,7 +18,9 @@ function submitLogin() {
-  setSubmitting(true);
+  setSubmitting(true);
+  setError(null);
   return requestLogin(credentials);
```

`@@` 后面的数字是旧文件和新文件的行范围；`-` 是旧内容，`+` 是新内容，没有前缀的是上下文。先问“状态变化是什么”，再问“异常路径、权限边界和调用方是否也变化”。只看到一行 `setError(null)`，不能直接断言用户体验已经修好，还要查看失败分支和对应测试。

重命名和移动可能让文件列表看起来比实际行为复杂。

```powershell
git diff --name-status --find-renames HEAD~1 HEAD
git diff --summary HEAD~1 HEAD
```

Git 的重命名判断是基于相似度的启发式结果，不是文件系统事件。审查时要看内容差异，不能只看 `R` 标记。

## 三、`git log` 与 `git show`，把改动放回时间线

先看分支图和提交摘要。

```powershell
git log --graph --decorate --oneline --all -n 12
git log --format=fuller -n 5
git show --stat --summary <commit>
```

`log` 适合看顺序、分支和合并关系，`show` 适合查看某次提交的正文和 patch。提交信息是线索，不是事实的替代品。真正的行为证据仍然来自 diff、调用方和验证结果。

### 按文件或代码线索查历史

```powershell
git log --follow --oneline -- src/api/login.ts
git log -S'setSubmitting(true)' --oneline -- src/api/login.ts
git log -G'catch|finally' --oneline -- src/api/login.ts
git show <commit> -- src/api/login.ts
```

- `--follow` 在单个文件路径上追踪重命名前的历史；它不适合一次传入多个路径。
- `-S` 查找某段文本出现次数发生变化的提交，适合追踪一行配置或函数调用何时加入、删除。
- `-G` 按正则表达式匹配 diff 中的行，适合查找某类分支或 API 调用的历史变化。

这些选项只能缩小搜索范围。找到提交后，仍要用 `git show` 读完整上下文，尤其要注意后续提交是否改变了原先的假设。

## 四、`git blame`，追踪一行，不追究责任

怀疑某一行的默认值、异常处理或兼容逻辑时，再使用下面的命令。

```powershell
git blame -L 20,45 -- src/api/login.ts
```

输出中的短提交号、作者和日期表示该行最后一次被某个提交写入。下一步通常是打开对应提交并查看文件历史。

```powershell
git show <commit> -- src/api/login.ts
git log --follow --oneline -- src/api/login.ts
```

如果代码经历过格式化、文件移动或复制，可以尝试下面的命令。

```powershell
git blame -w -M -C -C -L 20,45 -- src/api/login.ts
```

`-w` 忽略空白变化，`-M` 检测同一文件内的移动，`-C` 尝试追踪从其他文件复制过来的代码。这些都是启发式判断，可能变慢，也可能在大规模重排后给出不稳定的归属。合并提交、批量格式化和 cherry-pick 也会让“最后修改者”与“最初设计者”不同。

因此，`blame` 能回答“这行最近由哪个提交改动”，不能回答“谁应该为线上问题负责”。把提交放回 Issue、PR、测试和后续修复的上下文，结论才有意义。

## 一次完整的只读阅读流程

假设 `status` 显示实现文件有未暂存修改，测试文件已暂存，还有一个未跟踪的复现说明。可以按下面顺序读取。

1. 记录仓库根目录、分支、`HEAD` 和 `status --short --branch`，把原有改动和本次任务分开。
2. 用 `git diff --stat`、`git diff --cached --stat` 和 `git ls-files --others --exclude-standard` 确认范围，避免漏读暂存文件或未跟踪证据。
3. 分别阅读 `git diff`、`git diff --cached`，最后用 `git diff HEAD` 检查合计效果。
4. 对每个行为变化查看 `git show` 或 `git log -- <path>`，必要时用 `-S` 或 `-G` 找到引入它的提交。
5. 只有某一行的历史仍然不清楚时才用 `git blame`，并打开对应提交的完整 diff。
6. 把结论写成“事实、推断、未知、下一步验证”，不要把历史线索或文件名当成测试结果。

可以把证据整理成下面的表格。

| 项目 | 记录方式 |
| --- | --- |
| 事实 | `src/api/login.ts` 在工作区改变；失败分支新增 `setError(null)` |
| 推断 | 这可能会清理旧错误提示，但还要确认成功分支和组件渲染逻辑 |
| 未知 | 未看到网络超时、重复点击和取消请求的验证 |
| 下一步 | 查看调用方、相关测试，并运行项目已有的登录测试 |

这个表格不替代代码审查，但能防止把“看起来合理”写成“已经证实”。

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
- 工作区差异，git diff
- 暂存区差异，git diff --cached
- 相对 HEAD 的合计差异，git diff HEAD
- 最近提交，git log --graph --decorate --oneline --all -n 12

请按“事实、推断、未知、建议验证”四栏回答。
1. 哪些文件在工作区、暂存区或未跟踪列表中；
2. 每个差异改变了什么输入、状态、输出或错误路径；
3. 哪些判断还需要查看调用方、Issue、历史提交或测试；
4. 哪些文件看起来与任务无关；
5. 如果追踪单行历史，请给出 git blame 的提交号，并用 git show 复核上下文。

不要把未运行的测试写成“通过”，不要把 blame 的作者当成责任人。
```

如果只想追踪一个可疑常量，可以缩小范围。

```text
只读调查 `src/api/login.ts` 第 20 到 45 行的超时默认值。
先给出当前 diff，再用 git blame 和 git show 找到引入该值的提交。
区分这次提交实际改变的内容、提交信息声称的目的和仍然未知的兼容性影响。
不要修改文件，也不要补写不存在的测试结果。
```

拿 Codex 的回答与终端输出逐项对照。它如果漏掉 `git diff --cached`、未跟踪文件或比较基线，结论就不完整。

## 小练习，复现一条证据链

配套的 `git-baseline-demo` 位于第 01 篇文章的备份目录，是一个可丢弃的离线仓库，里面故意同时放了已暂存、未暂存和未跟踪改动。请在教程仓库根目录运行下面的命令。

```powershell
Set-Location -LiteralPath '.\\05-Git协作与代码审查\\01-Git协作前先检查什么-仓库分支与脏工作区-图片备份-20260830-2112\\temp\\git-baseline-demo'
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

这个练习只读，不需要提交、推送或清理现场。若使用自己的测试仓库，先复制一份或创建临时分支，不要在真实项目里故意制造脏改动。

## 截图方案，三张足够

不需要为每条命令单独截图。进入上面的演示仓库后，依次执行三个停点；每个停点截一张终端图，保留命令和完整输出。

### 1. 现场摘要

```powershell
Write-Host '=== 1/3 baseline ==='
git status --short --branch
git diff --stat
git diff --cached --stat
git ls-files --others --exclude-standard
```

这张图证明分支关系、工作区改动、暂存区改动和未跟踪文件。看到 `?? notes/` 时不要展开或上传其中可能含有个人信息的文件。

### 2. 差异范围

```powershell
Write-Host '=== 2/3 diff ==='
git diff --name-status
git diff --cached --name-status
git diff HEAD -- src tests
git diff --check
Write-Host "diff-check exit=$LASTEXITCODE"
```

这张图证明默认 `diff`、暂存区 `diff` 和相对 `HEAD` 的合计差异。`diff-check exit=0` 只表示没有发现空白错误或冲突标记，不代表测试已经通过。

### 3. 历史与单行来源

```powershell
Write-Host '=== 3/3 history ==='
git log --graph --decorate --oneline --all -n 8
git log --follow --oneline -- src/LoginForm.txt
git blame -w -M -C -C -L 1,2 -- src/LoginForm.txt
```

这张图把提交时间线、文件重命名历史和行级归属放在一起。不要截取完整用户名、私有路径或业务数据；如果输出过长，只保留最近 8 次提交和目标行附近的结果，不要删掉命令本身。

## 常见误区与验收清单

- [ ] 能说明 `git diff`、`git diff --cached`、`git diff HEAD` 的比较两端。
- [ ] 能区分工作区、暂存区、未跟踪文件和远程分支关系。
- [ ] 能用 `git show` 把提交摘要还原成具体行为，而不是只复述提交信息。
- [ ] 发现重命名、复制或格式化后，知道 `blame` 结果可能只是启发式归属。
- [ ] 能指出 diff 中没有被现有测试或人工检查覆盖的行为。
- [ ] 没有把 `git blame` 当成责任追究工具，也没有把未运行的测试写成通过。

下面几种说法都不够严谨。

| 说法 | 问题 | 更好的写法 |
| --- | --- | --- |
| “`git status` 没输出，所以可以直接提交。” | 可能漏看远程关系、忽略文件或任务基线 | “相对当前 `HEAD` 没有已跟踪改动；分支同步和提交范围仍需确认。” |
| “`git diff` 为空，所以没有改代码。” | 已暂存改动和未跟踪文件不会出现在默认 diff | “默认 diff 为空；还需要看 `git diff --cached` 和未跟踪列表。” |
| “blame 显示了某人的名字，所以问题是他造成的。” | blame 只记录最后改动这行的提交 | “该行最后在某提交中变更，需结合提交上下文和后续验证判断。” |

## 与其他章节的关系

第 01 节负责进入任务前的仓库、分支和脏工作区检查；本文进一步解释如何阅读四类 Git 证据。第 03 节负责分支和 Worktree 的隔离选择，第 05 节负责可审查的 Commit 与 PR 文本，第 06 节负责 Code Review 的测试和风险判断。本文不替代这些章节，也不把只读检查扩展成自动提交或合并。

## 参考资料

- [Git diff documentation](https://git-scm.com/docs/git-diff)
- [Git log documentation](https://git-scm.com/docs/git-log)
- [Git status documentation](https://git-scm.com/docs/git-status)
- [Git blame documentation](https://git-scm.com/docs/git-blame)
