# 素材查找记录

## 配图证据矩阵

| 文章步骤 | 读者需要看到的证据 | 首选来源 | 当前结果 | 后续动作 |
|---|---|---|---|---|
| 1. 区分权限、沙箱与审批 | 沙箱定义技术边界，审批决定何时停下来询问 | OpenAI 官方文档 | `01-openai-agent-approvals-security.png` | 可直接作为概念证据候选 |
| 2. 常见动作与能力 | Codex Desktop 权限入口及不同模式 | 官方文档 + 本机当前版本 | `02-openai-permissions-menu.png`；仍需本机截图 | 作者按 `manual/01` 补当前版本实拍 |
| 3. 审批窗口检查项 | 完整命令、目标路径、越界理由、审批范围 | 本机可丢弃仓库 | 无合格公开图 | 作者按 `manual/02`、`manual/05`、`manual/06` 补图 |
| 4. 可以放行 | 已知脚本、明确范围、可回退结果 | 原始操作视频 + 本机复现 | `04-youtube-approved-command-scope.png` | 本机复现后优先替换第三方帧 |
| 5. 应该拒绝 | 拒绝后命令未执行、结果未生成、权限未扩大 | 原始操作视频 + 本机复现 | `03-youtube-declined-approval-result.png` | 作者按 `manual/03` 补当前版本实拍 |
| 6. 最小权限真实任务 | 只读、工作区写入、网络访问逐级对照 | 本机可丢弃仓库 | 尚缺三组统一环境截图 | 作者按 `manual/02`、`manual/04`、`manual/05` 补图 |

## 查询记录

| 平台 | 查询词 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| OpenAI 官方文档 | `site:developers.openai.com codex sandbox approvals permissions` | Exa 发现 → Playwright 原页 | `verified-direct` | 打开后跳转至 ChatGPT Learn；保存两张实际文档 UI 截图 |
| 公开网页 | `Codex sandbox approval 权限 审批 教程` | Exa via mcporter | `verified-direct` | 用于发现官方页和原始教程；未使用搜索缩略图 |
| B 站 | `Codex 沙箱 权限 审批` | Agent Reach 报告的 B 站搜索 API；Exa 索引；B 站公开 view API | `verified-index` | `bili-cli` 未安装；核验 BV17e9DB6E6f、作者木子不写代码、2026-04-29，并确认简介含“权限、沙箱与命令确认”；未下载或推断视频帧 |
| 小红书 | `Codex 沙箱 权限 审批` | Agent Reach 无活动后端；Exa 公开索引回退 | `unavailable` | 未直搜小红书；索引返回均不相关，`no-qualified-result`；不保存候选 |
| YouTube | `OpenAI Codex sandbox approval permissions tutorial` | Agent Reach `yt-dlp` | `verified-direct` | 原始视频 zXTa_7Tc2EY 可读取元数据和章节；先生成 30 秒联系表，再核验 00:03:31 与 00:07:42 精确帧 |
| X | 未执行内容查询 | Agent Reach doctor | `unavailable` | Twitter CLI/OpenCLI 无活动后端，不声称已直接搜索 |

## 失败与回退

- 2026-08-21，B 站：`bili` 命令不存在；回退到 B 站搜索 API、公开 view API 与网页索引，仅做元数据级核验。
- 2026-08-21，小红书：无登录后端；回退到公开索引后没有合格结果，未尝试登录或读取浏览器 Cookie。
- 2026-08-21，YouTube：首个 1080p 流下载返回 HTTP 403；按平台流程改用 Android 客户端可公开取得的 360p 格式。来源仅提供该可用格式，因此保留原始 640×360 帧并在清单中如实标注。
- 2026-08-21，Playwright：所有保存截图均已人工打开检查，无 QR 码、Token、Cookie、账号标识或登录遮罩。
