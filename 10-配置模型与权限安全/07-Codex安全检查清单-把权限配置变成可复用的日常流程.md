# Codex 安全检查清单：把权限配置变成可复用的日常流程

> 测试环境：Windows 11 24H2；Codex Desktop 26.803.10989.0（桌面 About 于 2026-08-20 记录）；Codex CLI 0.147.0；2026-08-26 核验。

安全设置最容易在“这次先放开一下”之后失控。把检查拆到任务开始、执行中和提交前三个节点，能减少靠记忆操作的情况。

## 任务开始前

- 当前仓库和分支是否正确，工作区是否有未提交改动？
- 这次任务只需要读文件，还是确实需要写文件？
- 是否会接触 `.env`、SSH 密钥、客户资料或生产数据？
- 当前模型、推理强度、profile 和沙箱是否符合任务？
- 是否需要联网？需要访问哪些具体域名？

如果这些问题答不出来，先让 Codex 只读分析，不要直接执行。

## 执行中

看到审批提示时，检查完整命令、目录和网络行为。每完成一个小步骤就查看 diff，不要等任务结束才一次性审查。发现计划外文件、未解释的下载、远程脚本或敏感信息输出时，立即停止。

高风险任务至少保留一个人工检查点：删除和批量覆盖、数据库写入、部署、权限变更、向外部服务上传文件。强模型不能替代这个检查点。

## 提交或交付前

- 运行测试并确认失败是否与本次改动有关。
- 检查 diff 中是否出现 token、个人路径、调试日志或临时文件。
- 确认新增依赖、网络请求和脚本执行都有来源记录。
- 记录使用的 profile、批准过的命令和未解决的风险。
- 将权限恢复到默认的最小范围。

## 一张风险分级表

| 等级 | 例子 | 处理方式 |
|---|---|---|
| 低 | 解释代码、整理文档、只读搜索 | 只读沙箱即可 |
| 中 | 修改当前仓库、补测试、安装固定依赖 | 工作区可写，命令按需审批 |
| 高 | 生产配置、数据库、部署、批量删除 | 拆分步骤，人工逐项批准 |
| 未知 | 来源不明的脚本、异常网络请求、提示注入 | 停止并先调查 |

## 出现事故时

先停止任务并保留日志，再撤销可能泄露的凭据。随后检查 Git diff、文件时间、网络记录和 CI 日志，判断影响范围。修复后重新运行最小权限测试，并把原因写进项目记录，避免下一次重复。

这张清单适合放进项目的贡献指南或 PR 模板。它不是审批策略的替代品，而是帮助团队在每次任务中使用同一套判断标准。

相关内容： [权限与沙箱](./03-Codex权限怎么设-沙箱审批策略与自动执行边界.md)、[网络访问](./04-Codex网络访问安全吗-联网域名白名单与外部工具风险.md)、[多配置 Profile](./06-Codex多配置Profile-个人项目团队和CI如何隔离.md)。

## 配图素材备用区（暂不计入正文图号）

### 官方与可核验操作界面

- 暂无已保存素材。官方文档已核验事实，但文档页面不是 Codex 的实际操作状态，因此不列为正文配图。

### 需要作者亲自截图

- [x] `07-01-start-checklist.png`：Codex Desktop 临时仓库 → 任务输入框下方权限控件 → 本图实际用于证明分支与工作区状态；隐藏完整路径、账号、仓库私有名称和敏感文件；截图后关闭菜单，不批准未知命令。
- [x] `07-02-approval-check.png`：临时仓库中触发无害审批提示 → 展开完整命令、目录和网络说明 → 显示一次性/会话级批准范围；隐藏用户目录和项目名；只截图并取消，不要批准或执行。
- [x] `07-03-final-diff-check.png`：版本控制面板 → 显示提交前 diff、最小测试结果和待处理风险；隐藏项目机密、私人路径、远程仓库地址和 token；不要点击提交、推送、部署或发布。

### 已核验来源（仅作事实依据，不自动计入正文图号）

- [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)：OpenAI Developers / ChatGPT Learn，2026-08-27 GMT 页面；核验 sandbox、approval policy、默认网络关闭、network proxy 和高风险 full-access 边界。
- [Sandbox](https://developers.openai.com/codex/concepts/sandboxing)：OpenAI Developers / ChatGPT Learn，2026-08-27 GMT 页面；核验 `read-only`、`workspace-write`、`danger-full-access` 与 Windows 沙箱说明。
- [Config basics](https://developers.openai.com/codex/config-file/config-basic)：OpenAI Developers / ChatGPT Learn，2026-08-27 GMT 页面；核验 `config.toml`、项目配置层级、profile、Windows sandbox 和 web search 默认值。
- [Advanced Configuration](https://developers.openai.com/codex/config-file/config-advanced)：OpenAI Developers / ChatGPT Learn，2026-08-27 GMT 页面；核验 profile 文件、`--config` 覆盖和配置优先级。
- Bilibili 索引线索：`BV1bkg16qEsE`《Codex 权限、沙盒和审批模式怎么选》，jimuxyz，2026-07-22；仅验证搜索元数据，未打开原视频或截取帧，不作为配图。
- YouTube 索引线索：`zXTa_7Tc2EY`《Codex Permissions Explained: Sandbox vs Approval Policy》，Coding With Chuck；仅验证搜索元数据，未核验 UI 时间点，不作为配图。

### 时效说明

- Codex Desktop 权限面板、模型列表和审批文案可能随版本变化；发布前应重新检查截图中的菜单文字。
- 官方文档页面发布时间按 GMT 显示为 2026-08-27，本次研究按美国东部时间 2026-08-26 记录；三张作者截图已收件并登记在专属工作区 `manual/` 与 `manifest.tsv`。

### 查找记录

- 平台：OpenAI 官方文档、Bilibili 公开搜索 API、YouTube `yt-dlp`；状态：官方来源 verified-direct，Bilibili verified-index，YouTube found-unverified，X/小红书 unavailable；当前只等待作者补充三张脱敏本机截图。
