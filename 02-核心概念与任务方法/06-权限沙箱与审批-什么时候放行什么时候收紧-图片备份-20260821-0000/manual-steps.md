# 需要作者亲自截图

以下截图请只在可丢弃测试仓库中完成。统一隐藏用户名、主目录、仓库远端、任务正文中的私人信息、Cookie、Token、密钥和账号标识。

1. [ ] `manual/01-codex-permissions-menu.png`：打开 Codex Desktop → 新建本地任务 → 选择可丢弃测试仓库 → 点击输入框下方当前权限模式；画面应同时显示“请求审批/自动审批/完全访问”或当前版本的对应选项，证明权限入口位置；隐藏侧边栏任务名与账号信息；停在菜单展开状态，不切换到“完全访问”。
2. [ ] `manual/02-read-only-write-approval.png`：在同一测试仓库切换为只读模式 → 请求“新建 `sandbox-demo.txt`，内容写 test”；画面应显示写入动作需要审批及完整目标路径；确认路径只指向测试仓库，隐藏用户目录；停在批准或拒绝按钮出现后，不要批准。
3. [ ] `manual/03-rejected-request-alternative.png`：在上一步选择拒绝 → 等待 Codex 给出不写文件的替代方案；画面应证明拒绝不会自动扩大权限，且任务可以退回分析/建议；隐藏会话中的私人文本；停止在替代方案出现后。
4. [ ] `manual/04-workspace-write-success.png`：切换为“请求审批/工作区写入” → 只在测试仓库内创建 `sandbox-demo.txt` → 打开 Git 变更视图；画面应同时显示新文件和限定在当前工作区的路径，证明常规写入可在边界内完成；隐藏远端地址；完成截图后可手动删除测试文件。
5. [ ] `manual/05-network-approval-details.png`：保持工作区写入且网络默认关闭 → 请求读取 `https://developers.openai.com/codex/concepts/sandboxing`；画面应显示网络访问审批、目标域名和理由；确认域名准确，隐藏代理地址与网络配置；停在审批按钮前，不扩大为会话级全网访问。
6. [ ] `manual/06-outside-workspace-path-check.png`：让 Codex 提议把测试文件复制到测试仓库相邻的临时目录；画面应展示工作区外的完整目标路径和越界理由；确保目标不是个人文档、桌面或真实项目；停在审批按钮前，不执行复制。
