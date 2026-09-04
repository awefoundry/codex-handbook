# 怎样写出可审查的 Commit 和 PR：范围、证据与风险

> 难度：进阶
>
> 类型：方法与模板

> 测试环境：Windows 10 Pro 24H2（build 26100.4652）；Codex CLI 0.147.0；Git 2.47.0.windows.2；2026-09-04 核验。

## 一个提交只回答一个问题

提交信息应该说明行为变化，而不是描述“修改了几个文件”。例如 `fix(auth): restore login button after failure` 比 `update files` 更容易检索和回滚。

    git diff --stat
    git diff --check
    git add -p
    git commit -m "fix(auth): restore login button after failure"

使用 `git add -p` 把无关修改留在工作区。提交前不要为了“看起来整齐”顺手格式化整份文件。

## PR 描述模板

    ## 改了什么
    - 修复错误登录后的按钮状态。

    ## 为什么改
    - 请求失败分支没有清理提交状态。

    ## 如何验证
    - npm run test:login
    - npm run lint

    ## 风险与回滚
    - 未改变认证接口；如需回滚，撤销本 PR 的提交。

    ## 待确认
    - 未覆盖真实网络超时场景。

## 让 Codex 检查 PR 文本

    请只读检查下面这份 PR 描述。
    判断它是否说明了改动范围、动机、验证命令、未验证部分和回滚方式。
    缺少信息时直接列出问题，不要替我补写不存在的测试结果。

## 验收清单

- [ ] 提交历史能看出每个提交的目的。
- [ ] PR 描述没有声称未执行的测试。
- [ ] 改动范围、风险和回滚方式清楚。
- [ ] 截图或日志没有账号、令牌、私有路径和客户数据。

## 常见失误

把“测试通过”写进 PR 不等于测试真的运行过。把多个主题塞进一个大 PR，会让审查者难以判断失败来自哪里。需要拆分时，先保留可独立验证的最小提交。

## 参考资料

- [GitHub About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Conventional Commits](https://www.conventionalcommits.org/)
### 官方与可核验操作界面

- `pull-request-tabs-changed-files.png`（1308×122）：审查 PR 的改动范围；证明进入 `Files changed`。来源：GitHub Docs，`https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request`；作者：GitHub Docs；发布日期未标注；2026-09-04 打开原图核验。GitHub 界面可能更新。
- `diff-settings-menu.png`（2288×656）：审查 PR 的改动范围；证明可切换 Unified/Split 并隐藏 whitespace。来源同上；作者：GitHub Docs；发布日期未标注；2026-09-04 打开原图核验。截图中的仓库内容和计数只是官方示例。
- `review-changes-button.png`（2114×416）：提交审查意见；证明打开 `Review changes`。来源同上；作者：GitHub Docs；发布日期未标注；2026-09-04 打开原图核验。GitHub 界面可能更新。
- `abandon-review-button.png`（1316×1078）：提交审查意见；证明 `Finish your review` 面板提供 Comment、Approve、Request changes 和 Submit review。来源同上；作者：GitHub Docs；发布日期未标注；2026-09-04 打开原图核验。图中示例内容不属于本文测试结果。
- `viewed-checkbox.png`（2150×112）：审查完成后的范围确认；证明可以勾选 `Viewed`。来源同上；作者：GitHub Docs；发布日期未标注；2026-09-04 打开原图核验。GitHub 界面可能更新。

### 视频教程来源（仅作来源，不自动作为配图）

- [How to Review a Pull Request in GitHub the RIGHT Way](https://www.youtube.com/watch?v=lSnbOtw4izI)：CoderDave，YouTube，发布日期未从索引元数据确认；仅通过 `yt-dlp` 获取元数据，未抽取可证明本文步骤的精确帧，因此不列入图片候选。
- [GitHub Crash Course: Creating Code Reviews](https://www.youtube.com/watch?v=GbjI2x0dMK0)：Andrew Dimmer，YouTube，发布日期未从索引元数据确认；仅作观看参考，不使用封面或未经核验的帧。

### 需要作者亲自截图

- [ ] `01-commit-pr-evidence-terminal.png`：PowerShell → 检查 Git 版本 → 创建 `%TEMP%\commit-pr-review-demo` 一次性仓库 → `git diff --stat` → `git diff --check` → `git add -p` → `git diff --cached --stat` → `git show --stat --oneline HEAD`；隐藏用户名、邮箱、远程地址、令牌、客户数据和真实私有路径；停在本地提交摘要之后。
- [ ] `02-pr-description-scope-risk.png`：已登录 GitHub 测试仓库 → `Pull requests` → 测试 PR → `Conversation`；画面包含五个 PR 描述字段；隐藏仓库名、组织名、评论者邮箱、内部链接、客户数据和令牌；停在提交评论、请求审查、合并或关闭之前。

### 查找记录

- 平台：GitHub 官方文档、Conventional Commits、Bilibili、YouTube、X/Twitter、小红书；查询与验证状态详见本文章专属工作区的 `research-log.md`。
- 官方候选文件位于：`05-怎样写出可审查的Commit和PR-范围验证证据与风险-图片备份-20260903-2116/online/`。
- 视频封面、缩略图、Logo、无关图片文件预览和裸视频链接均未作为图片候选。

