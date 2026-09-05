# 处理环境记录

- 处理日期：2026-09-04
- 操作系统：Windows 10 Pro，Build 26100（通过 PowerShell `Get-ComputerInfo` 核验）
- Shell：PowerShell（仅用于目录、复制、校验和命令调度）
- 图片处理：Python 3.13.5；Pillow 12.3.0
- 图片处理方式：本地 Pillow 无损读取原始 PNG，按 imagegzh 一号样式处理三张网络截图，添加透明圆角外框、`#d9d9d9` 细边框和轻阴影；未修改截图主体文字与布局。
- 原图检查：使用 Codex `view_image` 检查原图内容、清晰度和敏感信息。
- 输出验收：使用 Codex `view_image` 检查处理图；使用 Pillow 检查尺寸、RGBA 模式和四角透明像素。
- 封面生成：按用户指定使用 HiAPI `https://api.hiapi.ai/v1/tasks` 和 `gpt-image-2/text-to-image`，从本机 `HIAPIAPIKEY`/`HIAPI_API_KEY` 读取认证；任务 `tk-hiapi-01M1N5P7RCT88DENPQFS0JF7F6` 返回 `success`，原始输出 `1280×720 px`，再用 FFmpeg 居中裁切并缩放为 `940×400 px`。
- 封面验收：使用 Codex `view_image` 检查标题、布局、额外文字和敏感信息；使用 System.Drawing 检查最终尺寸和比例，结果为 `940×400`、`2.350000`。
- 正文概念图生成：按用户指定使用 HiAPI `gpt-image-2/text-to-image` 创建图四和图五；任务 `tk-hiapi-01M1NTKN6M3AXRVHWNZDABB7DE` 与 `tk-hiapi-01M1NTKMP8S6X7SE5VKCCQ6CA2` 均返回成功，认证仅读取本机 `HIAPIAPIKEY`/`HIAPI_API_KEY`，密钥值未写入文件、日志或正文。
- 正文概念图处理：图四原始与输出均为 `1280×720 px`；图五原始为 `1672×941 px`，经 Pillow 居中裁切为 `1280×720 px`，均保持 `16:9`。两张图添加轻微阴影、浅灰边框和圆角，并通过 `view_image`、RGBA 模式和四角透明像素检查。
