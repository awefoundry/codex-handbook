# 作者亲自截图

以下步骤在 Windows PowerShell 中执行。截图只用于证明本文方法，不要使用真实业务仓库、客户数据或带权限的工作目录。

## 一、准备环境

1. 打开 Windows Terminal 或 PowerShell，复制执行：

```powershell
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$env:WORK = Join-Path $env:TEMP 'commit-pr-review-demo'
$gitVersion = git --version
$psVersion = $PSVersionTable.PSVersion.ToString()
Write-Host "PowerShell $psVersion"
Write-Host $gitVersion
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw '未找到 Git，请先安装 Git for Windows' }
```

2. 预期至少看到 `PowerShell 7.x` 或 Windows PowerShell 版本号，以及 `git version 2.x`。本文核验基线是 Git 2.47.0.windows.2；你的版本不同也可以，但需要把实际版本记在截图说明或记录中。

3. 如果 `$env:WORK` 已存在，先确认它确实是一次性演示目录，再执行：

```powershell
if (Test-Path -LiteralPath $env:WORK) {
    Get-Item -LiteralPath $env:WORK | Select-Object FullName
    Remove-Item -LiteralPath $env:WORK -Recurse -Force
}
New-Item -ItemType Directory -Path $env:WORK | Out-Null
Set-Location -LiteralPath $env:WORK
```

这里的删除只针对 `%TEMP%\commit-pr-review-demo`，不要把变量改成真实仓库路径。

## 二、创建一次性示例仓库

复制执行下面整段：

```powershell
git init -b main
'示例仓库：只用于演示可审查提交' | Set-Content -LiteralPath 'README.md' -Encoding utf8
'login button: idle' | Set-Content -LiteralPath 'login.txt' -Encoding utf8
git add README.md login.txt
git -c user.name='Review Demo' -c user.email='review-demo@example.invalid' commit -m 'chore: initialize review demo'

'login button: ready' | Set-Content -LiteralPath 'login.txt' -Encoding utf8
Add-Content -LiteralPath 'README.md' -Value "`n审查示例仅用于本地演示。"
git status --short
```

预期看到 `README.md` 和 `login.txt` 都有未提交修改。邮箱使用 `.invalid` 保证不会指向真实地址。

## 三、生成范围证据并只暂存一个主题

1. 依次运行下面命令：

```powershell
git diff --stat
git diff --check
git diff -- README.md login.txt
```

2. 使用交互式暂存，只选择 `login.txt` 的改动：

```powershell
git add -p login.txt
```

看到提示时输入 `y` 接受当前 hunk。若出现多个 hunk，只接受与登录按钮状态相关的那一块；输入 `n` 可把无关块留在工作区，输入 `q` 可退出。

3. 再运行：

```powershell
git diff --cached --stat
git diff --cached --check
git status --short
```

预期：暂存区只包含 `login.txt`，`README.md` 仍然是未暂存修改；`git diff --check` 和 `git diff --cached --check` 没有输出表示没有发现空白错误。

4. 用一个只描述单一行为变化的提交信息提交：

```powershell
git -c user.name='Review Demo' -c user.email='review-demo@example.invalid' commit -m 'fix(auth): restore login button after failure'
git show --stat --oneline --decorate HEAD
git status --short
```

预期：提交摘要只对应 `login.txt`，而 `README.md` 的无关修改仍留在工作区。截图停在这里，不要执行 `git push`、合并、删除或强制覆盖。

## 四、终端截图要求

- 文件名：`01-commit-pr-evidence-terminal.png`，放入本工作区的 `manual/`。
- 画面建议包含：版本检查、`git diff --stat`、`git diff --check`、`git add -p` 的选择结果、`git diff --cached --stat`、`git show --stat --oneline HEAD` 和最后的 `git status --short`。
- 如果终端太长，分两张截图也可以，但正文优先选一张信息最完整、文字可读的画面。
- 截图前清理或隐藏真实用户名、邮箱、仓库路径、远程地址、令牌、客户数据和其他工作目录信息；本文示例邮箱保持 `.invalid`。
- 不要把 `git push` 的成功信息写成已执行证据；本步骤明确停在本地提交之后。

## 五、准备 PR 描述截图

1. 在已登录的 GitHub 页面打开一个专门的测试仓库或已存在的脱敏测试 PR，路径为：`Pull requests` → 选择测试 PR → `Conversation`。
2. 在 PR 描述中只放入确实对应测试结果的内容。可以使用下面的脱敏示例，但执行过的命令才可以写成“已验证”：

```markdown
## 改了什么
- 修复登录失败后按钮状态未恢复的问题。

## 为什么改
- 请求失败分支没有清理提交状态。

## 如何验证
- `git diff --check`
- 本地示例仓库检查提交范围。

## 风险与回滚
- 未改变认证接口；可撤销本次提交回滚。

## 待确认
- 未覆盖真实网络超时场景。
```

3. 截图前核对画面能读到“改了什么、为什么改、如何验证、风险与回滚、待确认”五个字段，同时隐藏仓库名、组织名、评论者邮箱、内部链接、客户数据和令牌。
4. 文件名：`02-pr-description-scope-risk.png`，放入本工作区的 `manual/`。停在查看页面，不要提交评论、请求审查、合并或关闭 PR。

## 六、检查截图文件

把两张截图放入 `manual/` 后执行：

```powershell
$manual = 'D:\codexguide_all\教程\05-Git协作与代码审查\05-怎样写出可审查的Commit和PR-范围验证证据与风险-图片备份-20260903-2116\manual'
Get-ChildItem -LiteralPath $manual -File | Select-Object Name,Length
```

图片宽度建议至少 1000 px。打开图片逐张检查：命令和 PR 字段是否清楚，是否有账号、令牌、Cookie、二维码、私有路径或客户数据，是否只展示本文需要证明的状态。

## 七、交回后的入库信息

把截图文件名、像素尺寸、对应章节、证明事实和脱敏检查结果告诉作者；不要把截图直接推送到远程仓库。作者会在确认后补写 `manifest.tsv`，再运行工作区校验器。
