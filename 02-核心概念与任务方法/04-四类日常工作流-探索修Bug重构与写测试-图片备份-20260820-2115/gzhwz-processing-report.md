# gzhwz 处理报告

处理环境：Windows 11 24H2；Python 3.13.5 + Pillow 12.3.0（仅用于图片处理）；2026-08-20 核验。文章运行环境另见 `environment.md`，其中记录了当前 Codex 工作区无法直接调用 Python 的事实。

## 正文处理

- 保留文章的教程定位和四类工作流结构，删除写作阶段的“正文计划、配图计划、完成标准”等内部提纲。
- 加入 5 张正文图和简短图注，先放 HIAPI 四类工作流总览，再放探索、Bug 边界、重构与测试状态截图。
- 保留截图拍摄时的环境阻塞证据，并补充 2026-08-21 的实际测试核验结果。
- 历史文章入口使用目录白名单中的准确标题，均需作者在公众号后台用“已发表内容”完成绑定。

## 图片映射与验收

| 原图 | 正文处理图 | 正文位置 | 验收 |
|---|---|---|---|
| `online/hiapi-workflow-overview-source.png` | `04-四类日常工作流-配图/图一.png` | 开头总览 | HIAPI 生成，Pillow 一号样式，四个对象清晰，无文字和 Logo |
| `manual/01-task-start.png` | `04-四类日常工作流-配图/图二.png` | 探索陌生项目 | Pillow 一号样式，文字和布局保留，可打开 |
| `manual/02-project-exploration.png` | `04-四类日常工作流-配图/图三.png` | 探索陌生项目 | Pillow 一号样式，文字和布局保留，可打开 |
| `manual/03-bug-reproduce-and-fix.png` | `04-四类日常工作流-配图/图四.png` | 修 Bug | Pillow 一号样式，保留“Python 不可用”证据 |
| `manual/04-refactor-test-summary.png` | `04-四类日常工作流-配图/图五.png` | 重构与写测试 | Pillow 一号样式，保留“测试未执行”证据 |

原始截图仍保存在本工作区 `manual/`，文章目录里已有其他文章的 `图一.png` 至 `图四.png` 未覆盖。

HIAPI 总览图的任务 manifest：`D:\CodexHome\skills\hiapi-icon-skills\outputs\run-20260821031944-e87c\manifest.json`；状态 `approved`，已完成视觉检查。

## 绿色系列封面

- 章节：第 2 章；篇号：第 4 篇。
- 推荐标题：`接手陌生项目后，Codex 应该先探索、修 Bug，还是先写测试？`
- HIAPI 任务：`tk-hiapi-01M0H8215X5FPQPEBCDYWYGBVM`；状态：`success`。
- 输出文件：`D:\codexguide_all\教程\02-核心概念与任务方法\04-四类日常工作流-探索修Bug重构与写测试-cover-04.png`。
- 视觉验收：通过。封面显示“第 2 章 · 第 4 篇”，主标题与推荐标题一致，使用绿色系列布局，未发现明显乱码或额外 Logo。

## 链接埋点

| event_id | stage | position | intent | target_type | target_title / url | utm_status | verification_status | copy_role | post_publish_metrics |
|---|---|---|---|---|---|---|---|---|---|
| `opening-prerequisite-01` | opening | 导语第 3 段 | continue-reading | 历史文章 | 《别再把 Codex 当成“会写代码的 ChatGPT”：一文看懂它到底怎么工作》；url：由公众号后台绑定 | 不适用：由公众号后台绑定 | 已核验标题，待后台绑定 | 承诺 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `contextual-rules-01` | contextual | 探索章节结尾 | continue-reading | 历史文章 | 《别再重复提醒 Codex：用 AGENTS.md 让它读项目先读规则》；url：由公众号后台绑定 | 不适用：由公众号后台绑定 | 已核验标题，待后台绑定 | 补充 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-website-01` | closing | 总结之后、微信区块之前 | take-action | 网站 CTA | https://codexguide.io/?utm_source=wechat&utm_medium=article&utm_campaign=codex-four-workflows-20260820&utm_content=closing-website-01 | 已添加 | 已核验 | 行动 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |
| `closing-wechat-01` | closing | 网站 CTA 之后、全文最后 | ask-or-connect | 微信 CTA | 微信交流二维码；url：不适用 | 不适用 | 已核验：默认二维码原文件哈希一致 | 关系承接 | 阅读/点击/深读/关注/评论/咨询/转化：待记录 |

## 待确认

- 已完成 Python 环境核验：在 `D:\codexguide_all\temp\workflow-demo` 运行 `python -m unittest discover -s tests -v`，6 项通过、0 项失败、退出码 0。
- 在公众号后台绑定两篇历史文章标题。
- 发布前确认网站链接可访问，二维码仍能打开并扫码。

## 标题

- 归档位置：第二章第 4 篇。
- 推荐引流标题：`接手陌生项目后，Codex 应该先探索、修 Bug，还是先写测试？`
- 其他备选标题已保存到同目录的 `04-四类日常工作流-探索修Bug重构与写测试-引流标题.md`。
- 绿色系列封面已生成，文件见上方“绿色系列封面”记录。
- 发布前测试：`python -m unittest discover -s tests -v`；6 passed，0 failed，exit code 0（2026-08-21）。
