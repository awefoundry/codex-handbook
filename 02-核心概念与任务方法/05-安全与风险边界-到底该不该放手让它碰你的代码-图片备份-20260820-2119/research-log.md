# 素材查找记录

## 视觉证据矩阵

| 文章步骤 | 需要证明的事实 | 首选画面 | 当前状态 | 处理 |
|---|---|---|---|---|
| 风险来自哪里 | 工具动作可能越过文件/环境边界 | 权限模式与审批提示 | 待作者截图 | 不用装饰图替代 |
| 四个问题分级 | 资产、回退、验证、影响四维判断 | 风险判断表 | 待作者制作并截图 | 使用模拟任务 |
| 适合直接交给 Codex | 小范围、可回退、可验证 | 测试分支 + 聚焦测试 | 待作者截图 | 只展示脱敏仓库 |
| 必须保留检查点 | 认证/支付/权限等动作需人工批准 | 批准提示前的命令状态 | 待作者截图 | 停在批准前 |
| 不应直接放手 | 生产 DDL、批量删除、敏感数据外发不可逆 | 高风险提示或清单 | 待作者截图 | 不执行真实高风险动作 |
| 可回退工作链 | 差异审查与测试是独立检查点 | `git diff` 与测试输出 | 待作者截图 | 记录实际命令 |
| 看懂最终交付 | 测试通过不等于差异正确 | 差异 + 测试结果并列 | 待作者截图 | 隐藏私人路径 |

## 来源与平台状态

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方文档 | Codex permissions sandbox approvals security | Jina Reader | verified-direct | https://developers.openai.com/codex/permissions；https://developers.openai.com/codex/sandboxing；https://developers.openai.com/codex/agent-approvals-security；页面 UI 可能随版本变化 |
| OpenAI 官方文档 | Codex Windows sandbox and history persistence | Jina Reader | verified-direct | https://developers.openai.com/codex/windows/windows-sandbox；https://developers.openai.com/codex/config-file/config-advanced；用于核对 Windows 隔离、会话历史和本地状态说明 |
| Git 官方文档 | git diff documentation | Jina Reader | verified-direct | https://git-scm.com/docs/git-diff；用于确认差异审查命令语义 |
| OWASP | OWASP Top Ten current release | Jina Reader | verified-direct | https://owasp.org/www-project-top-ten/；安全背景资料，不作为 Codex 功能说明 |
| The Decoder | OpenAI fixes Codex bug that deleted real user files | Exa → Jina Reader | verified-direct | https://the-decoder.com/openai-fixes-codex-bug-that-deleted-real-user-files-without-permission/；媒体转述，交叉核对 `$HOME`、Full access、Auto-review 和修复方向，不替代官方原帖 |
| InfoWorld | OpenAI acknowledges GPT-5.6 may accidentally delete files | Exa → Jina Reader | verified-direct | https://www.infoworld.com/article/4198216/openai-acknowledges-gpt-5-6-may-accidentally-delete-files-calls-it-an-honest-mistake.html；媒体转述，记录公开表述和“少量/极少发生”的限定 |
| YouTube | Codex sandbox approval permissions tutorial | yt-dlp | verified-index | 找到视频 ID `zXTa_7Tc2EY`，未提取帧；封面和缩略图均排除 |
| B 站 | Codex 权限 沙箱 审批 | B 站搜索 API（doctor 报告） | no-qualified-result | 本轮未找到能核验具体 UI 状态的候选；未使用 `yt-dlp` 抓取 B 站 |
| X | Codex permissions sandbox | 无活动后端 | unavailable | 不声称直接检索 |
| 小红书 | Codex 权限 沙箱 | 无活动后端 | unavailable | 不声称直接检索 |
| Reddit | Codex permissions sandbox | 无活动后端 | unavailable | 不声称直接检索 |

## 失败与时效记录

- HIAPI 补充图使用 Codex 内置 image_gen 生成两张原创编辑部插画：Agent harness 多层防线、风险判断四问；未使用第三方截图、Logo 或产品界面，正文图注已标注 AI 生成/教学示意。

- OpenAI 新版开发者文档的安全入口会重定向到权限导航页；因此记录具体子页面链接，不把导航页截图当作操作证据。
- 权限、沙箱和桌面端菜单属于快速变化界面；正文采用“截至核验日”的环境摘要，正式发布前应复拍本地界面。
- 文件删除事故的负责人原始 X 帖子本轮没有可用的直接后端，故正文明确写成“媒体转述的公开表述”，不写成已直接读取原帖。
- “Mac 客户端吃内存”未找到本轮可引用的官方性能承诺或修复公告，正文只保留为待实测的独立运营问题，不与文件删除安全事件合并。
- 用户提供的“删除会话、检查网络、重启 Codex、新开会话”被改写为止损与排查建议，没有写成解封保证；公开资料不足以支持“这样做大概率封号”的概率判断。
