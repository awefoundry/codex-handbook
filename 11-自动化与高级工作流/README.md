# 自动化与高级工作流

面向已经掌握基础使用方法，希望把 Codex 接入稳定流程的读者。

## 内容范围

- 多 Agent 分工与结果汇总。
- 定时任务和长时间运行的任务。
- 非交互模式和批处理。
- Codex SDK、App Server 和 GitHub Action。
- CI 环境中的认证、权限和结果输出。
- Hooks、Rules、Memories 和高级自定义。
- 自动化失败后的恢复和人工检查点。

## 已上线文章

- [Codex 任务结束时捕捉可复用素材：用 AGENTS.md 规则和 Stop Hook 生成素材候选](./01-Codex在任务结束时捕捉可复用素材.md)
- [Codex 跨会话协作：开新会话交接任务、带上下文派生，不再靠复制粘贴](./02-Codex跨会话协作功能.md)
- [Codex CLI 管理多条任务线：resume 恢复长任务、fork 分支、归档与交接](./03-CodexCLI管理多条任务线.md)
- [Codex 长任务工作流：主任务定方向，/side 讨论、Subagents 分担、独立审查，最后留交接记录](./05-Codex长任务工作流.md)
- [Codex 任务收尾怎么做：AGENTS.md、Memories 与 Markdown 交接记录各管什么](./06-Codex任务收尾系统.md)
- [Codex 自动化与 CI：0.169 起未信任目录要加 --trust，否则 exec 不会加载项目配置和 MCP](./07-Codex自动化与定时任务-从手动流程到稳定执行.md)
- [Codex 使用 Goal 模式运行长任务：/goal 启动、暂停恢复，和 Plan、长任务工作流怎么分工](./08-Codex使用Goal模式运行长任务.md)
- [Codex 使用 Subagents 并行处理任务：/subagents、继承沙箱，和主会话怎么分工](./09-Codex使用Subagents并行处理任务.md)
- [Codex Worktree 教程：用 Git worktree 并行跑多个任务，并把结果交回本地](./10-Codex用Worktree并行运行多个任务.md)
- [Codex Hooks 入门：hooks.json 放在哪、怎么用 /hooks 信任](./11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)
- [Codex Memories 记忆功能：开启方式、存储位置（memories 与 memories_v2）、/memories 按对话控制与额度](./12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)
- [Codex Rules 怎么写：用 prefix_rule 设置命令白名单和黑名单](./13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)
- [Codex 访问令牌和服务账号：在 CI 和定时任务里不用浏览器登录运行 codex exec（Business / Enterprise）](./14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)
- [Codex 任务完成通知：0.168 起可选 osc777，审批通知会显示更长的命令预览](./15-Codex任务完成通知-tui.notifications与notify脚本.md)
- [Codex GitHub Action 防提示注入：从 openai/codex 的 Issue 机器人漏洞看 allow-users、safety-strategy 与不可信输入](./16-Codex-GitHub-Action防提示注入-allow-users与safety-strategy.md)
- [Codex Computer History 怎么用：开启条件、记录什么不记录什么、数据存在哪、怎么暂停和清除](./17-Codex-Computer-History怎么用-开启条件-记录什么-本地存储与隐私控制.md)（2026-11-28。按 Computer History 与 Memories 页整理。没有登录桌面端，没有配图）
