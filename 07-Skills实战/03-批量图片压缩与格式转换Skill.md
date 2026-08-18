# 用开源 img-convert Skill 批量压缩图片

整理文章配图时，我经常重复做几件事：限制图片宽度、转成 WebP、控制文件大小，再确认原图没有被覆盖。这个流程已经有人做成了开源工具和 Skill，没必要从零写一套。

这篇实战使用 [dutchbase/img-converter](https://github.com/dutchbase/img-converter) 提供的 `img-convert` Skill。目标很具体：把指定文件夹中的图片统一限制在 1200px 宽，转成 WebP，质量设为 85，并把结果放进新目录。

> 测试环境：Windows 11 24H2（26100.4652）；Codex Desktop 26.810.7004.0；Codex CLI 0.147.0；Node.js 22.22.3；skills 1.5.22；img-convert 1.0.4；2026-08-17 核验。

> 当前状态：开源项目、安装方式和单图转换命令已经验证。批量处理截图和完整数据将在实测后补充。

## 一、先看这个开源 Skill 能做什么

`img-convert` 基于 Sharp，仓库使用 MIT 许可证。项目同时提供命令行工具、Node.js API、MCP 服务和一份现成的 `SKILL.md`。这篇只使用最简单的组合：让 Codex 按 Skill 中的规则判断，再调用 CLI 处理本地图片。

它支持 JPEG、PNG、WebP、AVIF、GIF 和 TIFF 输出，也能调整尺寸、压缩质量、旋转、裁边和读取图片信息。批量任务既可以传入 glob 路径，也可以使用 JSON 清单。

安装前可以先让 `skills` 命令读取仓库，确认其中确实有 `img-convert`：

```powershell
npx -y skills add https://github.com/dutchbase/img-converter --list
```

命令应显示一个名为 `img-convert` 的 Skill。不要只凭第三方介绍页安装，仓库中的 [SKILL.md](https://github.com/dutchbase/img-converter/blob/main/SKILL.md) 才是实际内容。

## 二、安装 Skill 和命令行工具

先把 Skill 安装到 Codex 的全局技能目录：

```powershell
npx -y skills add https://github.com/dutchbase/img-converter `
  --skill img-convert `
  --global `
  --yes
```

Skill 只负责告诉 Codex 怎样使用工具，并不会自动安装 `img-convert` 命令。还要安装仓库发布的 npm 包：

```powershell
npm install -g @dutchbase/img-convert
```

这个工具要求 Node.js 18 或更高版本。安装完成后检查命令是否可用：

```powershell
node --version
img-convert --help
img-convert info --help
img-convert batch --help
```

<!-- TODO：补充 Skill 与 CLI 安装成功的截图。 -->

## 三、把处理规则说清楚

这次使用下面这组参数：

| 项目 | 设置 |
| --- | --- |
| 输入 | 指定目录中的 JPG、JPEG、PNG 和 WebP |
| 输出目录 | 新建 `output` 目录 |
| 最大宽度 | 1200px |
| 输出格式 | WebP |
| 图片质量 | 85 |
| 原文件 | 保留，不覆盖、不删除 |

`img-convert` 默认保持宽高比，也默认禁止放大小图。宽度超过 1200px 的图片会等比缩小，小于 1200px 的图片保持原尺寸。

输出目录必须和原图目录分开。这样即使命令参数写错，原文件也还在。

## 四、先预演，不急着写文件

假设原图位于 `D:\images\original`，先运行 `--dry-run` 查看将要处理的文件：

```powershell
img-convert "D:/images/original/**/*.{jpg,jpeg,png,webp}" `
  --format webp `
  --width 1200 `
  --quality 85 `
  --output "D:\images\output" `
  --dry-run `
  --json
```

这里把 glob 路径放在引号中，让 `img-convert` 自己展开文件列表。Windows 下的 glob 要使用正斜杠 `/`，反斜杠会被当成转义符，可能导致一张图片都找不到。预演结果要核对三件事：文件数量是否正确、输出是否都指向新目录、有没有两个不同格式的同名文件最终写成同一个 `.webp`。

## 五、确认后再批量转换

预演没有问题，就去掉 `--dry-run`：

```powershell
img-convert "D:/images/original/**/*.{jpg,jpeg,png,webp}" `
  --format webp `
  --width 1200 `
  --quality 85 `
  --output "D:\images\output" `
  --json
```

`--json` 会返回每张图片的输入大小、输出大小、压缩比例、尺寸和保存路径。文章后面可以直接根据这些结果统计总共节省了多少空间，不需要手工逐张计算。

如果不同图片需要不同尺寸或格式，可以让 Codex 先生成 JSON 清单，再使用：

```powershell
img-convert batch jobs.json --json
```

简单的统一转换用 glob 就够了，不必先做清单。

## 六、直接让 Codex 调用 Skill

安装并重启 Codex 后，可以这样说：

```text
使用 img-convert Skill，先检查 D:\images\original 中会被处理的 JPG、JPEG、PNG 和 WebP 图片。
把宽度限制为 1200px，保持比例，不放大小图，统一转成质量 85 的 WebP，输出到 D:\images\output。
保留所有原文件。先 dry-run 并汇报文件数量和命名冲突，确认没有问题后再执行，最后给出处理成功数、失败数和总压缩比例。
```

这段要求把检查、预演、执行和汇报写在了一起。Skill 还会提醒 Codex 先读取陌生图片的信息，尤其注意透明通道和动画图片。

## 七、用一张小图验证过命令

我先用一张 330×267 的 PNG 截图测试了相同参数。设置宽度为 1200px 后，输出仍是 330×267，说明小图没有被放大。文件从 23,493 字节变为 15,018 字节，减少 36.1%。

```json
{
  "inputBytes": 23493,
  "outputBytes": 15018,
  "reduction": 36.1,
  "width": 330,
  "height": 267,
  "format": "webp",
  "quality": 85
}
```

这只能证明命令可用。正式实测还要加入大尺寸照片、透明 PNG、竖图和已经是 WebP 的图片。

<!-- TODO：补充批量处理前后的文件夹截图。 -->

## 八、记录批量处理结果

| 项目 | 处理前 | 处理后 |
| --- | ---: | ---: |
| 图片数量 | 待补充 | 待补充 |
| 总文件大小 | 待补充 | 待补充 |
| 最大宽度 | 待补充 | 1200px |
| 文件格式 | JPG/PNG/WebP | WebP |
| 失败数量 | - | 待补充 |

<!-- TODO：补充一组原图与 WebP 的清晰度对比图。 -->

## 九、最后检查这些情况

- 原图数量、名称和内容没有变化
- 输出图片都位于单独目录
- 横图和竖图保持原始比例
- 小于 1200px 的图片没有被放大
- 透明区域没有意外变黑
- 动画图片没有在不知情的情况下只保留第一帧
- 同名输入不会静默覆盖同一个 WebP 文件
- 失败文件及原因已经单独列出

## 十、项目链接

- GitHub：[dutchbase/img-converter](https://github.com/dutchbase/img-converter)
- Skill 源文件：[SKILL.md](https://github.com/dutchbase/img-converter/blob/main/SKILL.md)
- npm 包：[`@dutchbase/img-convert`](https://www.npmjs.com/package/@dutchbase/img-convert)
- 许可证：[MIT License](https://github.com/dutchbase/img-converter/blob/main/LICENSE)

## 配图素材备用区（暂不计入正文图号）

> 本节用于写作阶段选图，发布前应将采用的素材移动到对应正文段落并重新编号。旧界面、限时活动和第三方教程必须标注日期与来源。

### 官方与可核验操作界面

- `online/01-github-img-converter-repository.png`：适合“一、先看这个开源 Skill 能做什么”，证明公开仓库的项目定位包含 Sharp、npm、CLI 和 MCP；来源为 [dutchbase/img-converter](https://github.com/dutchbase/img-converter)，作者 dutchbase，仓库创建于 2026-03-10，2026-08-17 直接核验。GitHub 页面和 main 分支可能变化，发布前复核。
- `online/02-github-img-convert-skill-source.png`：适合“一、先看这个开源 Skill 能做什么”，证明仓库根目录存在 `SKILL.md`，名称为 `img-convert`，并列出批处理和格式转换触发词；来源为 [SKILL.md](https://github.com/dutchbase/img-converter/blob/main/SKILL.md)，作者 dutchbase，源文件提交于 2026-03-10，2026-08-17 直接核验。main 分支内容可能变化，发布前复核。

### 视频教程来源（仅作来源，不自动作为配图）

- [使用 Google 的开源工具 libwebp 批量将图像转换为 WebP](https://www.bilibili.com/video/BV1bscteWEBv)：最爱小真寻，B 站，2025-01-14。视频使用 libwebp，不是本文的 `img-convert`，因此未截帧，只作命令行批量转换的延伸阅读。
- [Convert Image Files to WebP From The Command Line](https://www.youtube.com/watch?v=N_N5xPq42Do)：SittingDev，YouTube，2021-02-25。视频使用 libwebp，不是本文工具，未截帧。
- [What's the easiest way to convert multiple images into webP?](https://www.youtube.com/watch?v=lFSE88I3Ggs)：The Vibe Coder，YouTube，2026-03-20。视频展示另一款 GUI 工具，未截帧。

### 需要作者亲自截图

- [ ] `01-skill-list-result.png`：Codex Desktop 当前任务 → 终端 → 运行 `npx ... --list` → 显示 `Found 1 skill` 与 `img-convert`；隐藏用户名、私人路径和代理地址；停在列出结果，不安装。
- [ ] `02-skill-install-success.png`：Codex Desktop 当前任务 → 终端 → 安装 `img-convert` Skill → 显示安装成功；隐藏全局目录中的个人路径；安装完成即停止。
- [ ] `03-cli-help-and-version.png`：Codex Desktop 当前任务 → 终端 → 安装 CLI 并运行版本与帮助命令 → 显示 Node.js >=18 和关键参数；不要输出 `.npmrc`、令牌或私有 registry；不要启动 MCP。
- [ ] `04-dry-run-file-list.png`：`D:\images\original` → 运行 `--dry-run --json` → 显示待处理文件、输出路径和 `dryRun: true`；仅使用公开测试图片副本；停在预演，不转换。
- [ ] `05-batch-convert-json-result.png`：继续使用测试副本 → 去掉 `--dry-run` → 显示输入输出大小、压缩率、尺寸与成功失败数；不得删除或覆盖原图。
- [ ] `06-original-output-folder-comparison.png`：Windows 文件资源管理器 → `D:\images` → 并排查看 `original` 与 `output`；隐藏个人云盘和最近使用记录；截图后不执行删除或覆盖。

### 查找记录

- GitHub：`dutchbase/img-converter`、`SKILL.md`；Playwright、GitHub API、Jina Reader；`verified-direct`；保存两张公开页面截图。
- npm：`@dutchbase/img-convert`；npm registry API；`verified-direct`；网页被 Cloudflare 403 拦截，安全验证页不采用。
- Exa：官方英文查询与中文批量转 WebP 查询；Exa via mcporter；`verified-index`；最终回到 GitHub 原始页面核验。
- B 站：`批量 图片 转 WebP 命令行 Sharp`；B 站搜索 API；`verified-index`；找到 libwebp 教程，但工具不同，不截帧。
- YouTube：`img-convert dutchbase image converter`、`batch convert images webp sharp cli tutorial`；yt-dlp；`verified-index`；结果均非本文工具，不截帧。
- 小红书：`批量图片转 WebP`；无可用后端；`unavailable`；未登录、未绕过平台验证。
