# 需要作者亲自截图

这些截图都在本地 Codex 与终端中完成，不需要登录网页。请使用无隐私内容的测试图片，避免画面出现 Windows 用户名、私人仓库名、npm 令牌、代理地址或真实客户素材。

## 1. 检查仓库中的 Skill

- [ ] 文件名：`01-skill-list-result.png`
- 起始位置：Codex Desktop 当前任务 → 打开终端面板（本地界面，无 URL）。
- 操作：运行 `npx -y skills add https://github.com/dutchbase/img-converter --list`。
- 预期画面：终端显示 `Found 1 skill` 和 `img-convert`，证明仓库可被 Skill 安装器识别。
- 脱敏：隐藏用户主目录、私人项目路径、代理地址；不要显示 npm 配置或令牌。
- 停止位置：只列出 Skill，不执行安装。

## 2. 安装 img-convert Skill

- [ ] 文件名：`02-skill-install-success.png`
- 起始位置：Codex Desktop 当前任务 → 终端面板。
- 操作：运行文章中的 `npx -y skills add ... --skill img-convert --global --yes` 命令。
- 预期画面：终端明确显示 `img-convert` 已安装到 Codex，且没有错误信息。
- 脱敏：隐藏用户名、全局技能目录中的个人路径和任何代理配置。
- 停止位置：安装完成即停止；不要顺带安装其他 Skill 或修改全局配置。

## 3. 安装并检查 CLI

- [ ] 文件名：`03-cli-help-and-version.png`
- 起始位置：Codex Desktop 当前任务 → 终端面板。
- 操作：运行 `npm install -g @dutchbase/img-convert`，随后运行 `node --version`、`img-convert --help`。
- 预期画面：Node.js 版本不低于 18，帮助信息中出现 `--format`、`--quality`、`--width`、`--output`、`--dry-run` 和 `--json`。
- 脱敏：不要打开或输出 `.npmrc`；隐藏私有 registry、令牌、用户名与用户目录。
- 停止位置：确认帮助信息后停止，不启动 MCP 服务或 Web UI。

## 4. 预演批量任务

- [ ] 文件名：`04-dry-run-file-list.png`
- 起始位置：准备 `D:\images\original`，只放可公开的测试 JPG、PNG 和 WebP 副本。
- 操作：运行文章“先预演”一节的 `img-convert ... --dry-run --json` 命令。
- 预期画面：JSON 列出待处理文件和 `output` 路径，`dryRun` 为 `true`；输出目录中尚未写入转换结果。
- 脱敏：使用中性目录 `D:\images`；不要使用客户名称、私人照片或下载目录。
- 停止位置：核对数量与重名冲突后停止，暂不执行正式转换。

## 5. 执行转换并查看结果

- [ ] 文件名：`05-batch-convert-json-result.png`
- 起始位置：继续使用上一步的公开测试图片副本。
- 操作：去掉 `--dry-run` 后执行命令。
- 预期画面：JSON 显示每张图片的输入大小、输出大小、压缩比例、尺寸、格式和保存路径，同时能看见成功数与失败数。
- 脱敏：隐藏个人路径和图片中的个人信息。
- 停止位置：转换完成后停止；不要删除、覆盖或移动原图。

## 6. 对比原图与输出目录

- [ ] 文件名：`06-original-output-folder-comparison.png`
- 起始位置：Windows 文件资源管理器 → `D:\images`。
- 操作：并排显示 `original` 与 `output`，切换到详细信息视图，显示名称、类型、尺寸和文件大小。
- 预期画面：原图仍在，输出均为 WebP；小图没有被放大，大图宽度不超过 1200px。
- 脱敏：只使用公开测试素材，关闭导航栏中的个人云盘和最近使用记录。
- 停止位置：完成截图即停止，不执行删除或覆盖操作。
