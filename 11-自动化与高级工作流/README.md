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
- [Codex CLI 管理多条任务线：命名、恢复、fork、归档与跨会话交接](./03-CodexCLI管理多条任务线.md)
- [Codex CLI 长任务如何恢复：保存、继续与检查会话](./04-CodexCLI恢复长任务.md)
- [Codex 长任务工作流（2026-11 更新）：主任务定方向，/side 讨论、Subagents 分担、独立审查，最后留交接记录](./05-Codex长任务工作流.md)
- [Codex 任务收尾系统，用 Markdown 保存状态、决策与可复用流程](./06-Codex任务收尾系统.md)
- [Codex 自动化与 CI：codex exec 非交互模式、GitHub Action 工作流 YAML、--output-schema 结构化输出与 API Key 安全（2026-10 更新）](./07-Codex自动化与定时任务-从手动流程到稳定执行.md)
- [Codex Goal 模式：用 /goal 跑长任务，完成标准怎么写、怎么暂停和并行](./08-Codex使用Goal模式运行长任务.md)
- [Codex Subagents 怎么用：内置 Agent、自定义 TOML 与并发设置](./09-Codex使用Subagents并行处理任务.md)
- [Codex Worktree 教程：用 Git worktree 并行跑多个任务，并把结果交回本地](./10-Codex用Worktree并行运行多个任务.md)
- [Codex Hooks 入门：hooks.json 放在哪、怎么用 /hooks 信任](./11-Codex-Hooks入门-hooks.json配置-信任审核与常用场景.md)
- [Codex Memories 记忆功能（2026-10 更新）：开启方式、存储位置（memories 与 memories_v2）、/memories 按对话控制与额度](./12-Codex-Memories记忆功能-开启方式-存储位置与按对话控制.md)
- [Codex Rules 怎么写：用 prefix_rule 设置命令白名单和黑名单](./13-Codex-Rules命令规则-用prefix_rule控制沙箱外命令.md)
- [Codex 访问令牌和服务账号：在 CI 和定时任务里不用浏览器登录运行 codex exec（Business / Enterprise）](./14-Codex访问令牌与服务账号-CI和定时任务免浏览器登录.md)
- [Codex 任务完成通知怎么设置：tui.notifications 终端提醒和 notify 脚本推送](./15-Codex任务完成通知-tui.notifications与notify脚本.md)
