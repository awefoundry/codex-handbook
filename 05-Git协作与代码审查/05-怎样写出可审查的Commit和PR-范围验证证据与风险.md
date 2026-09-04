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

## 配图素材备用区（暂不计入正文图号）

> 本节用于写作阶段选图，发布前应将采用的素材移动到对应正文段落并重新编号。旧界面、限时活动和第三方教程必须标注日期与来源。

### 官方与可核验操作界面

- 暂无合格候选。当前优先使用作者实拍终端和测试 PR；未把其他文章目录中的截图、视频封面、缩略图、Logo 或裸视频链接当作本篇配图。

### 视频教程来源（仅作来源，不自动作为配图）

- 暂无合格视频截帧。Bilibili、YouTube 的初始化检索未产生能直接证明本文步骤的合格画面；X/Twitter 和小红书没有可用的 active backend，未声称直接搜索。

### 需要作者亲自截图

- [ ] `01-commit-pr-evidence-terminal.png`：终端 → `git diff --stat` / `git diff --check` / `git add -p` → 提交摘要；隐藏账号、令牌、客户数据和私有路径；停在推送或其他不可逆操作之前。
- [ ] `02-pr-description-scope-risk.png`：GitHub 测试 PR → `Conversation` → PR 描述；隐藏仓库名、组织名、评论者邮箱、内部链接和客户数据；停在提交评论、合并或关闭 PR 之前。

### 查找记录

- 平台：GitHub 官方文档、Conventional Commits、Bilibili、YouTube、X/Twitter、小红书；查询与验证状态详见本文章专属工作区的 `research-log.md`。
- 工作区：`./05-怎样写出可审查的Commit和PR-范围验证证据与风险-图片备份-20260903-2116/`。
