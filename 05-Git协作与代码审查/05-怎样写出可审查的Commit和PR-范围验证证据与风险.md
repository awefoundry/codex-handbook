# 怎样写出可审查的 Commit 和 PR

> 难度：进阶
>
> 类型：方法与模板
>
> 测试环境：Windows 10 Pro 24H2（build 26100.4652）；Codex CLI 0.147.0；Git 2.47.0.windows.2；2026-09-04 核验。

很多代码审查会卡住，因为审查者无法快速回答三个问题。改了什么，为什么这样改，怎么证明它没有带来新的问题。

一份可审查的提交和 PR，需要把这三个问题分别放在合适的位置。提交负责说明一小段行为变化，命令和日志负责提供事实，PR 描述负责把范围、动机、验证和风险串起来。

## 一个提交只回答一个问题

提交信息先写行为，再写范围。`fix(auth): restore login button after failure` 能让人看出这是登录失败后的按钮状态修复。`update files` 只能说明文件被动过，无法帮助审查者判断提交目的。

![单一行为变化从 diff 进入一个聚焦的提交](./05-怎样写出可审查的Commit和PR-范围验证证据与风险-发布素材/正文配图/图一.png)

图一 只把与当前行为有关的差异放进提交，无关修改继续留在工作区。

### 先看工作区，再决定暂存什么

开始提交前，先查看工作区的全部变化。

```powershell
git status --short
git diff --stat
git diff --check
git diff -- README.md login.txt
```

`git diff --stat` 用来确认变化量，`git diff --check` 用来检查空白错误，最后一条命令把注意力收窄到正在判断的文件。它们解决的是不同问题，不能用其中一条代替其他检查。

如果工作区里同时有登录按钮修改和 README 文案修改，先不要把两件事一起提交。使用交互式暂存，只接收属于当前提交的 hunk。

```powershell
git add -p login.txt
```

提示出现后输入 `y` 接受当前 hunk，输入 `n` 保留它，输入 `q` 退出。若一个 hunk 里混有两个主题，可以用 `s` 尝试拆分，再逐块判断。

![git add -p 只暂存 login.txt 的差异块](./05-怎样写出可审查的Commit和PR-范围验证证据与风险-发布素材/正文配图/图二.png)

图二 交互式暂存停在当前 hunk 的选择提示，暂存动作仍然有明确边界。

接着检查暂存区。

```powershell
git diff --cached --stat
git diff --cached --check
git status --short
```

理想结果是，暂存区只包含当前提交需要的文件，其他改动仍显示为未暂存。这里保留工作区的无关修改很正常，也比为了提交方便而顺手格式化整份文件更容易回看。

### 提交后再确认一次

提交信息应该描述一个可以单独验证的动作。

```powershell
git -c user.name='Review Demo' `
    -c user.email='review-demo@example.invalid' `
    commit -m 'fix(auth): restore login button after failure'

git show --stat --oneline --decorate HEAD
git status --short
```

`git show` 用来核对刚刚写入的提交，最后的 `git status --short` 用来确认无关修改还留在工作区。提交后发现范围不对，先停下来检查，不要用新的大提交把问题盖住。

## PR 描述要让审查者少猜

PR 描述不需要写成项目周报。把审查者真正需要的信息放在固定位置即可。

```markdown
## 改了什么
- 修复错误登录后的按钮状态。

## 为什么改
- 请求失败分支没有清理提交状态。

## 如何验证
- git diff --check
- 本地示例仓库检查提交范围。

## 风险与回滚
- 未改变认证接口。需要撤销时，回滚本次提交。

## 待确认
- 未覆盖真实网络超时场景。
```

![PR 描述中的改动、动机、验证、风险与回滚字段](./05-怎样写出可审查的Commit和PR-范围验证证据与风险-发布素材/正文配图/图三.png)

图三 PR 描述把改动范围、动机、验证、风险和待确认项分开写，审查者可以按字段定位问题。

“如何验证”只写实际执行过的命令和结果。没有运行过的测试放进“待确认”，不要为了让 PR 看起来完整而写成通过。

“风险与回滚”也要具体。比如写明没有改变认证接口，回滚时撤销本次提交，审查者就知道影响范围和处理路径。只写“风险可控”没有同样的信息量。

## 用证据检查范围和风险

代码审查时，先进入 PR 的 `Files changed`，再按文件查看 diff。GitHub 的[审查页面](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)支持切换 Unified 和 Split 视图，也可以隐藏空白差异。改动较多时，先把格式噪声排除，再看真正的代码变化。

![GitHub Files changed 中的 diff 视图设置](./05-怎样写出可审查的Commit和PR-范围验证证据与风险-发布素材/正文配图/图四.png)

图四 在 `Files changed` 中选择 Unified 或 Split，并按需要隐藏空白差异。

看完一个文件后勾选 `Viewed`，可以让后续审查者知道哪些范围已经检查过。需要提交意见时，打开 `Review changes`，选择 Comment、Approve 或 Request changes，并在意见中写清文件、代码位置、触发条件和可能后果。

如果你要让 Codex 检查 PR 文本，可以使用只读提示。

```text
请只读检查下面这份 PR 描述。
判断它是否说明了改动范围、动机、验证命令、未验证部分和回滚方式。
缺少信息时直接列出问题，不要替我补写不存在的测试结果。
```

这里的限制很重要。Codex 可以检查文字是否完整，却不能凭空证明测试已经执行，也不能替你判断一个没有提供上下文的业务风险。

## 把风险写成可以执行的动作

风险段落至少回答两个问题。哪一层可能受影响，出了问题以后先做什么。

例如，认证接口没有变化，主要风险落在登录失败后的界面状态。回滚时撤销本次提交，随后重新运行登录失败场景和 `git diff --check`。如果风险涉及数据库迁移，就要写明是否有向后兼容的迁移、回滚脚本能否执行，以及回滚前需要保留什么数据。不要用一句“影响较小”替代这些动作。

审查者看到风险说明后，应该能决定继续审查、补一项验证，还是先暂停合并。风险写得越具体，沟通越少依赖猜测。

## 一份可复核的验收清单

提交和 PR 发出前，可以逐项检查。

- 提交历史能看出每个提交的目的。
- 暂存区只包含当前主题的改动。
- `git diff --check` 和 `git diff --cached --check` 没有空白错误。
- PR 描述写明改动、动机、验证、风险和回滚方式。
- 未执行的测试没有被写成通过。
- 截图和日志没有账号、令牌、私有路径或客户数据。

这份清单的作用是减少遗漏，不是替代代码审查。审查者仍然需要根据 diff 判断正确性、安全性和维护成本。

## 常见失误

把多个主题塞进一个提交，会让失败定位变慢。登录按钮状态、README 文案和依赖升级最好分开处理，各自保留独立的验证依据。

把“测试通过”写进 PR，也不能代替测试结果。命令、输出和测试范围需要一一对应。只运行了空白检查，就只写空白检查；没有覆盖网络超时，就把它保留在待确认项里。

截图也有范围。它适合证明某个界面、命令或状态在某个时刻可见，不适合替代完整测试报告，更不能暴露账号、Token、Cookie 或本机路径。

## 结语

可审查的提交靠的是小范围改动和对应证据。先把一个行为变化独立出来，再用命令确认暂存区和提交结果，最后在 PR 中写清验证边界与回滚动作，审查就有了可以依靠的事实。

如果你准备把这套检查方法放进实际开发任务，可以继续看 [CodexGuide 验证流程](https://codexguide.io/codex/validation?utm_source=wechat&utm_medium=article&utm_campaign=reviewable-commit-pr&utm_content=closing-website-01)，按 diff、测试和最终状态逐项核对。

如果你对提交范围、PR 描述或审查证据有具体问题，可以扫码添加微信，带上脱敏后的命令输出或 PR 文本一起交流。

![微信二维码](./05-怎样写出可审查的Commit和PR-范围验证证据与风险-发布素材/wechat-qr.png)

## 参考资料

- [GitHub 关于 Pull Request 审查](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [GitHub 审查 Pull Request 的改动](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
- [Conventional Commits 规范](https://www.conventionalcommits.org/)
