# gzhwz 处理报告

处理环境：Windows 11 24H2；Python 3.13.5 + Pillow 12.3.0；2026-08-20 核验。完整记录：`03-给Codex写任务-目标范围和验收标准-图片备份-20260818-2147/environment.md`

## 本轮处理

按 `gzhwz` 精简正文至约 3000 字以内，删除重复解释、过长案例说明和多余配图。原稿、原图、旧备份和旧发布目录均保留。

## 配图

正文保留 5 张正文图，按首次出现顺序重新编号；二维码不计入正文图号。

| 原处理图 | 精简发布图 | 内容 |
|---|---|---|
| `公众号配图-发布/图一.png` | `公众号配图-精简发布/图一.png` | 任务说明书与验收证据 |
| `公众号配图-发布/图二.png` | `公众号配图-精简发布/图二.png` | 五步闭环 |
| `公众号配图-发布/图三.png` | `公众号配图-精简发布/图三.png` | 第一版任务 |
| `公众号配图-发布/图六.png` | `公众号配图-精简发布/图四.png` | 第四版完成标准 |
| `公众号配图-发布/图九.png` | `公众号配图-精简发布/图五.png` | 最小 diff 与测试结果 |

5 张正文图均复用已验收的 imagegzh 一号样式；二维码 `公众号配图-精简发布/wechat-qr.png` 保持默认源文件像素不变。

## 埋点

| event_id | stage | 入口 | 方式 | 状态 |
|---|---|---|---|---|
| `opening-prerequisite-01` | opening | 《别再把 Codex 当成“会写代码的 ChatGPT”：一文看懂它到底怎么工作》 | 公众号后台绑定已发表内容 | 待绑定 |
| `contextual-agents-01` | contextual | 《别再重复提醒 Codex：用 AGENTS.md 让它读项目先读规则》 | 公众号后台绑定已发表内容 | 待绑定 |
| `decision-first-task-01` | decision | 《第一次让 Codex 改项目，我建议你先从这个小任务开始》 | 公众号后台绑定已发表内容 | 待绑定 |
| `closing-website-01` | closing | CodexGuide | `https://codexguide.io/?utm_source=wechat&utm_medium=article&utm_campaign=codex-task-card&utm_content=closing-website-01` | 已核验 |
| `closing-wechat-01` | closing | 微信交流二维码 | 无 URL，二维码入口 | 已核验 |

3 条历史文章埋点已放入正文对应阅读阶段；发布时选中标题，使用公众号“已发表内容”绑定。网站 CTA 在微信区块之前，二维码为最后一个引流区块。

## 待确认

- 3 条历史文章需要在公众号后台完成同名绑定。
- 默认二维码不能统计独立扫描来源；如需归因，需替换为专属渠道二维码。
