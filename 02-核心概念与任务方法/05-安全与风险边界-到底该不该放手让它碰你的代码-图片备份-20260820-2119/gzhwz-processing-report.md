# gzhwz 处理报告

处理环境：Windows 11 24H2；Python 3.13.5 + Pillow 12.3.0；Playwright CLI 浏览器核验；2026-08-21。完整工具记录见 [`environment.md`](./environment.md)。

## 本轮处理

按 `gzhwz` 流程检查正文事实边界与阅读顺序，保留作者提供的安全警告、误删复盘、止损建议和 Mac 内存观察；对“高概率封号”等无法核验的概率判断改成风险提示，不承诺解封。第 05 篇继续负责事故与风险判断，第 06 篇负责权限、沙箱和审批实操。

## 配图

正文包含 2 张官方文档截图和 2 张 HIAPI 教学示意图，按首次出现顺序编号。原始浏览器截图保存在 `online/`，HIAPI 原图保存在本目录，处理图保存在文章目录，所有原图仍可追溯。

| 原图 | 处理图 | 内容 | 来源 |
|---|---|---|---|
| `online/01-openai-sandbox-permissions-source.png` | `图一.png` | 沙箱是技术边界，审批是越界前的停顿机制 | https://developers.openai.com/codex/concepts/sandboxing |
| `online/02-openai-windows-sandbox-source.png` | `图二.png` | Full access 可能带来破坏性操作和数据损失 | https://developers.openai.com/codex/windows/windows-sandbox |
| `hiapi-agent-harness-source.png` | `图三.png` | 模型、执行器、沙箱、审批、审核与评测组成多层防线 | HIAPI（AI 生成教学示意） |
| `hiapi-risk-questions-source.png` | `图四.png` | 资产、回退、验证、影响范围四问 | HIAPI（AI 生成教学示意） |

两张处理图均按 imagegzh 一号样式生成：保留原页面内容，增加透明圆角外框、浅灰边框和轻阴影；未改写截图文字或布局。处理图尺寸均为 1721×1309，四角透明，已用本地图片查看器复核。

两张 HIAPI 图改为无人物编辑部插画风重新生成，再按 imagegzh 一号样式输出为新 PNG，保留代码、沙箱、审批、盾牌、回退和影响范围等物件叙事主体，增加透明圆角外框、浅灰边框和轻阴影；图注明确标注“AI 生成/教学示意”，不作为官方界面或事实证据。输出尺寸为 1672×941，四角透明，已人工检查主体完整、无人物、无品牌和无可误认的产品界面。

二维码 `../wechat-qr.png` 使用 gzhwz 默认源文件原样复制，未调用 imagegzh，不参与正文图号。

## 埋点

| event_id | stage | position | intent | target_type | target_title | url | utm_status | verification_status | copy_role | post_publish_metrics |
|---|---|---|---|---|---|---|---|---|---|---|
| `contextual-sandbox-evidence-01` | contextual | “两种警告不要混为一谈”之后 | verify-evidence | 外部资料 | OpenAI Sandbox | https://developers.openai.com/codex/concepts/sandboxing | 不可添加：官方资料保留原 URL | 已核验，浏览器直接打开 | 证据 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `decision-full-access-warning-01` | decision | “误删文件的复盘”中段 | verify-evidence | 外部资料 | Windows sandbox | https://developers.openai.com/codex/windows/windows-sandbox | 不可添加：官方资料保留原 URL | 已核验，浏览器直接打开 | 证据 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-website-01` | closing | 总结之后、微信区块之前 | take-action | 网站 CTA | CodexGuide 进阶教程 | https://codexguide.io/advanced?utm_source=wechat&utm_medium=article&utm_campaign=codex-safety-risk-boundary&utm_content=closing-website-01 | 已添加：`utm_content=closing-website-01` | 已核验 canonical | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | closing | 网站 CTA 之后、全文最后 | ask-or-connect | 微信 CTA | 微信交流 | 不适用 | 不适用：二维码入口 | 已核验，使用默认源文件 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

本篇没有自然的历史文章入口。原因是第 05/06 篇尚未确认已发布标题，未强行加入公众号后台绑定目标。

## 待确认

- 发布前复核 OpenAI 官方页面是否更新了 Full access 和 Windows Sandbox 的措辞。
- 作者仍需补拍真实 Codex 警告、新会话和删除目标核验画面；公开文档截图不能替代这些本机操作证据。
- 微信后台绑定网站链接并检查二维码区块位于全文最后。
