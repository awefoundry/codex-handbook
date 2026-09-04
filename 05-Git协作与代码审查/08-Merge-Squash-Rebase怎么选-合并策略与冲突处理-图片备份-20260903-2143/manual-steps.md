# 需要作者亲自截图

这些截图只使用一次性本地测试仓库或可公开展示的测试 PR。不要使用生产仓库，不要推送共享分支，不要截取账号、令牌、邮箱、私有路径、评论内容或 QR 码。

- [ ] `01-history-strategy-graph.png`：PowerShell → 进入一次性测试仓库 → 运行 `git log --graph --oneline --decorate --all`；画面应同时显示分支图和提交标签，证明三种策略造成的历史差异；隐藏用户名和真实路径；截图后停在只读输出。
- [ ] `02-rebase-conflict-state.png`：PowerShell → 测试仓库 → `git switch <feature>` → `git rebase main` → 冲突发生后运行 `git status`；画面应显示 rebase 正在进行、冲突文件列表和冲突文件中的 `<<<<<<<` / `=======` / `>>>>>>>`；隐藏本机路径和身份信息；停在解决冲突之前。
- [ ] `03-conflict-resolved-tests-passed.png`：PowerShell → 编辑冲突文件 → `git add <file>` → `git rebase --continue` → 运行受影响测试；画面应显示 rebase 完成以及测试通过；隐藏提交作者邮箱和真实仓库路径；停在本地验证完成，不要推送。
- [ ] `04-rebase-abort-recovery.png`：PowerShell → 测试仓库 → 在 rebase 暂停状态运行 `git rebase --abort` → `git status` → `git log --graph --oneline --decorate --all`；画面应证明工作树回到 rebase 开始前；隐藏路径和身份信息；停在恢复完成。
- [ ] `05-github-merge-methods-dropdown.png`：浏览器 → 打开可公开展示的测试 PR → 合并区域 → 展开合并方式下拉菜单；画面应显示 Merge commit、Squash and merge、Rebase and merge（实际可见项受仓库设置影响）；遮挡仓库名、用户名、分支名、评论和 issue 内容；停在确认合并之前，绝不点击确认。
