# 教程环境与版本记录

> 正文开头只写一行“测试环境”摘要，仅保留影响教程界面或操作结果的组件与核验日期。本文件保留完整版本、取值位置和核验依据；不要记录账号、密钥或私人工作区名称。

| 项目 | 版本/状态 | 获取方式或来源 | 核验日期 | 适用性/备注 |
|---|---|---|---|---|
| 操作系统 | Windows 10 Pro 24H2；build 26100.4652 | 注册表 `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion`：`ProductName`、`DisplayVersion`、`CurrentBuild`、`UBR` | 2026-09-04 | 影响终端路径、命令行和截图界面 |
| IDE / 宿主应用 | 不适用 | 本教程只演示终端、Git 和 Codex CLI | 2026-09-04 | 不依赖 IDE 图形界面 |
| Codex | Codex CLI 0.147.0 | `codex --version` | 2026-09-04 | 教程中的 Codex 只读检查提示在 CLI 中执行 |
| 目标插件 / App / Connector | 不适用 | 本教程不依赖插件、App 或 Connector | 2026-09-04 | 不记录不存在的版本号 |
| Git | 2.47.0.windows.2 | `git --version` | 2026-09-04 | 影响 `status`、`diff`、`add -p`、`commit` 等命令行为 |
| Node.js / npm | 不适用 | 本教程不执行 Node.js 构建或测试命令 | 2026-09-04 | 仅确认本机 `npx 10.9.8` 可用，但不属于复现前置依赖 |

## 证据范围

- 本文要证明的是：如何拆分提交、如何提供可复核的验证命令、如何在 PR 中写清风险与回滚，以及如何避免把未执行的测试写成已通过。
- 初始化阶段没有复制其他文章目录中的图片，也没有把视频封面、缩略图、Logo 或裸视频链接作为配图候选。
- `manifest.tsv` 已登记本篇使用的 GitHub Docs、终端案例和概念插图候选；未进入正文的候选仍保留在 `online/`。

## 本轮 gzhwz 处理工具

| 工具 | 版本或状态 | 获取方式 | 核验日期 | 用途 |
|---|---|---|---|---|
| Node.js | v22.22.3 | `node --version` | 2026-09-04 | 运行 HiAPI 任务提交与轮询脚本 |
| Python | 3.13.5 | `python --version` | 2026-09-04 | 本地图片处理 |
| Pillow | 12.3.0 | `python -c "from PIL import Image; import PIL; print(PIL.__version__)"` | 2026-09-04 | 生成 PNG 圆角、边框和透明画布 |
| HiAPI Key | 存在，未输出值 | PowerShell 检查环境变量是否存在 | 2026-09-04 | 提交两张入选概念插图任务；另有一张探索图未进入正文 |
| HiAPI | `gpt-image-2/text-to-image`；`1K`；`16:9` | dry-run 请求体检查与实际任务返回 | 2026-09-04 | 生成两张入选概念插图；探索图未用于发布正文 |
| Codex 原生 `image_gen` | 当前会话内置位图生成工具 | 封面生成调用与生成文件 | 2026-09-04 | 生成公众号封面原图；随后仅做尺寸调整 |

## 封面生成证据

- 完整提示词保存在 `发布素材/prompts/01-cover-commit-pr-review.md`。
- 原始生成文件由工具保存为 `D:\CodexHome\generated_images\01a069fa-87e9-7002-ae3f-94c4dd155f77\call_lwS4uepNMbOYtmVkipebTEM7.png`，尺寸为 1922×818。
- 发布封面使用 Pillow 缩放为 940×400；未进行文字重绘、擦除或覆盖。

## 本轮 HiAPI 生成记录

- 2026-09-04 使用已存在的 `HIAPI_API_KEY` 调用 `https://api.hiapi.ai/v1/tasks`，模型为 `gpt-image-2/text-to-image`，输入参数为 `resolution=1K`、`aspect_ratio=16:9`。
- 生成前执行本地 dry-run，仅检查 endpoint、模型、比例、密钥存在状态和提示词长度，未提交任务。
- 任务 `tk-hiapi-01M1PGW7ZARGHX41VFA28N5KA2` 与 `tk-hiapi-01M1PGW7ZQZ5SK449JTT6VR511` 均返回 `success`，原图下载到 `hiapi-source/`；未记录密钥值。
- 原图经 Pillow 12.3.0 处理为 `1600×900` 透明圆角画布，发布图替换为 `发布素材/正文配图/图一.png` 与 `图五.png`；两张成品均用 `view_image` 验收。
