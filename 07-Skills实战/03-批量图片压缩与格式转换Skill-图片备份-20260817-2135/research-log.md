# 素材查找记录

## 教程流程

本文教读者把开源 `dutchbase/img-converter` 仓库中的 `img-convert` Skill 安装到 Codex，再安装配套 npm CLI，对本地图片执行 dry-run、批量转 WebP 和结果核对。登录、注册、付费和发布均不属于本文流程。

## 查询矩阵

| 路线 | 查询词 | 目标 |
|---|---|---|
| 官方 | `site:github.com/dutchbase/img-converter img-convert SKILL.md batch WebP Sharp` | 核验仓库、Skill、CLI 参数、许可证与批处理格式 |
| 通用网页 | `批量 图片 转 WebP Sharp CLI 教程 img-convert` | 查找中文操作案例与可替代证据 |
| YouTube | `img-convert dutchbase image converter`；`batch convert images webp sharp cli tutorial` | 查找同一工具或相近命令行流程 |
| B 站 | `批量 图片 转 WebP 命令行 Sharp` | 查找中文真实终端操作 |
| 小红书 | `批量图片转 WebP` | 查找中文本地操作笔记；后端不可用时只记录不可用 |

## 视觉证据矩阵

| 文章步骤 | 读者需要看到什么 | 首选证据 | 当前状态 |
|---|---|---|---|
| 认识开源项目 | 公开仓库、Sharp/CLI/MCP 说明 | GitHub 仓库公开页面 | 已保存 `online/01-github-img-converter-repository.png` |
| 确认现成 Skill | `SKILL.md`、`img-convert` 名称和触发范围 | GitHub SKILL.md 公开页面 | 已保存 `online/02-github-img-convert-skill-source.png` |
| 检查可安装 Skill | `skills --list` 找到一个 Skill | 作者本机终端 | 待作者截图 `manual/01-skill-list-result.png` |
| 安装 Skill | 安装成功且没有错误 | 作者本机终端 | 待作者截图 `manual/02-skill-install-success.png` |
| 安装 CLI | Node 版本与 CLI 帮助参数 | 作者本机终端 | 待作者截图 `manual/03-cli-help-and-version.png` |
| dry-run | 文件列表、目标路径、未写入状态 | 作者本机终端 | 待作者截图 `manual/04-dry-run-file-list.png` |
| 正式转换 | JSON 输出、压缩率、尺寸、成功失败数 | 作者本机终端 | 待作者截图 `manual/05-batch-convert-json-result.png` |
| 检查产物 | 原图保留、WebP 输出、大小和尺寸变化 | Windows 文件资源管理器 | 待作者截图 `manual/06-original-output-folder-comparison.png` |

## 平台覆盖

| 平台 | 查询词/页面 | 后端 | 结果状态 | 回退/备注 |
|---|---|---|---|---|
| GitHub | `dutchbase/img-converter` 与 `SKILL.md` | Playwright、GitHub REST/raw、Jina Reader | verified-direct | 仓库和源文件已直接打开；保存两张公开 UI 截图，无登录信息 |
| npm registry | `@dutchbase/img-convert/latest` | npm registry API | verified-direct | 核验版本 1.0.4、MIT、Node.js >=18；npm 网页被 Cloudflare 403 拦截 |
| Exa | 官方查询与中文查询 | Exa via mcporter | verified-index | 找到官方仓库和若干其他转换器；最终证据回到 GitHub 原始页面核验 |
| B 站 | `批量 图片 转 WebP 命令行 Sharp` | B 站搜索 API、视频详情 API | verified-index | 找到 BV1bscteWEBv，但使用的是 Google libwebp，不是 img-convert；保留为延伸阅读，不截帧 |
| YouTube | 两组英文查询 | yt-dlp | verified-index | 找到 N_N5xPq42Do 等视频，内容是 libwebp/cwebp 或其他 GUI，不是本文工具；不截帧 |
| 小红书 | `批量图片转 WebP` | 无可用后端 | unavailable | `agent-reach doctor --json` 显示无 OpenCLI、xiaohongshu-mcp 或 xhs-cli；未登录、未绕过验证 |
| X/Twitter | 未继续搜索 | 无可用后端 | unavailable | doctor 显示 twitter-cli 未安装且无 OpenCLI；本文不声称已直接搜索 X |

## 候选与淘汰记录

- 采用：GitHub 仓库页截图。它能证明项目公开、工具定位和 Sharp/CLI/MCP 说明，适合文章第一节。
- 采用：GitHub `SKILL.md` 页面截图。它能证明仓库内确有现成 Skill，并显示名称、描述和触发词。
- 淘汰：npm 网页截图。Playwright 返回 HTTP 403，画面只有 Cloudflare 安全验证，不能证明安装步骤，也不进入 `manifest.tsv`。
- 淘汰：父目录 `image.png`。它属于此前文章素材，和当前 `img-convert` 教程无关，没有复制。
- 淘汰：B 站与 YouTube 视频帧。检索到的视频使用 libwebp/cwebp 或其他产品，不是本文开源 Skill；仅保留可追溯链接，不下载封面、不抽帧。

## 视频元数据

- B 站：[使用 Google 的开源工具 libwebp 批量将图像转换为 WebP](https://www.bilibili.com/video/BV1bscteWEBv)，作者“最爱小真寻”，2025-01-14，4:49。通过 B 站视频详情 API 核验；工具不同，无截帧。
- YouTube：[Convert Image Files to WebP From The Command Line](https://www.youtube.com/watch?v=N_N5xPq42Do)，SittingDev，2021-02-25，8:29。通过 yt-dlp 原始视频元数据核验；使用 libwebp，无截帧。
- YouTube：[What's the easiest way to convert multiple images into webP?](https://www.youtube.com/watch?v=lFSE88I3Ggs)，The Vibe Coder，2026-03-20，2:46。通过 yt-dlp 原始视频元数据核验；为另一款 GUI 工具，无截帧。
