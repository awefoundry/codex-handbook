# 配图重生成记录（2026-08-19）

用户反馈原三张 AI 配图（墨线跳色风格，codex 内置生成）不好看、不切题，改用 HiAPI `gpt-image-2/text-to-image` 重新生成，风格为现代扁平插画 + 中文标注（薄荷绿 / 雾蓝 / 杏色，#FAF9F5 底）。

| 文件 | HiAPI 任务 ID | 比例 | 大小 |
|---|---|---|---|
| figure-01-slash-menu.png | tk-hiapi-01M0CH4NWKK7QRQ23NF28VYNXM | 1:1 | 946217 B |
| figure-02-task-flow.png | tk-hiapi-01M0CH4RYWER49RXQ4FKHX5EJ1 | 16:9 | 1056144 B |
| figure-03-input-layers.png | tk-hiapi-01M0CH55Q5MN82K959PDAFKY4A | 1:1 | 1102340 B |

- 生成脚本：`generate.mjs`（读取本地 `HIAPI_API_KEY`，提交 `/v1/tasks` 并轮询下载）。
- 旧图已备份到 `旧图备份/`；新图已覆盖部署到 `../02-Codex斜杠命令与快捷键-图片备份-20260818-0552/online/`，文章中的引用路径未变。
- 目检：三张图中文与命令文字无错字，无 Logo / 水印 / 二维码；图二流程顺序（/plan→/goal→/review→/compact）与正文一致。
