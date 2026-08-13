# JetBrains 中使用 Codex

JetBrains IDE 通过 AI Chat 提供 Codex 入口。下面的流程适用于 IntelliJ IDEA、PyCharm、WebStorm 等支持该集成的 IDE；不同产品版本的菜单名称可能略有差异。

![JetBrains 官方品牌图](image-11-jetbrains-official-logo.png)
<p align="center">图 1：JetBrains 官方品牌图。来源：<a href="https://www.jetbrains.com/company/brand/">JetBrains Brand Guidelines</a>。</p>

![Codex 官方图标](image-10-codex-official-icon.png)
<p align="center">图 2：Codex 官方图标。来源：<a href="https://marketplace.visualstudio.com/items?itemName=OpenAI.chatgpt">Visual Studio Marketplace 的 Codex 扩展页面</a>。</p>

## 准备工作

- 将项目作为完整目录打开，而不是只打开单个文件。
- 确认项目使用的 JDK、Python、Node.js 或其他运行时已经可用。
- 先提交或保存已有改动，避免把无关 diff 混进第一次任务。

## 打开 AI Chat 并选择 Codex

打开 AI Chat，在代理或模型选择器中选 Codex。第一次使用按提示完成 ChatGPT 登录；如果看不到 Codex，先更新 AI Assistant/相关插件，再重启 IDE 检查。

## 添加上下文并执行小任务

打开目标文件，选中需要解释的代码，先发送：

```text
请只解释这段代码的执行路径，并指出一个可能的边界条件，不要修改文件。
```

确认上下文无误后，再提出只涉及一个文件或一个测试的修改。完成后检查 IDE 的 diff，运行项目已有的最小测试，并确认没有生成临时文件或修改 IDE 配置。

## 参考资料

- [Codex IDE extension](https://developers.openai.com/codex/ide)
- [JetBrains Brand Guidelines](https://www.jetbrains.com/company/brand/)

![B 站 JetBrains Codex 视频封面](image-11-bilibili-BV1Z6zrBCE8U.jpg)
<p align="center">图 3：B 站“Codex in JetBrains IDEs | OpenAI”视频封面，原作者标注为 OpenAI，B 站搬运作者：伸手不见五趾。<a href="https://www.bilibili.com/video/BV1Z6zrBCE8U/">查看原视频</a>。封面仅作延伸观看入口，不代表官方界面。</p>

## 计划覆盖

- 支持的 JetBrains 环境和准备条件。
- 打开 AI Chat 并选择 Codex。
- 使用当前文件和项目上下文发起任务。
- 审查修改并运行项目验证。

## 配图要求

- 官方 JetBrains 集成入口。
- AI Chat、Codex 选择和登录状态。
- 文件上下文、修改内容和验证结果。

## 配图素材备用区（暂不计入正文图号）

以下素材已下载到本文同目录，供正式写作时按章节挑选。优先使用 JetBrains 官方原图；视频抽帧只补充官方博客没有覆盖的真实任务过程。正式采用时再移动到对应段落，并统一重排图号。

### 首选：JetBrains 官方产品截图

1. `image-11-jetbrains-agent-picker.png`（2006×720）：AI Chat 的 Agent 选择器中出现 Codex。适合“打开 AI Chat 并选择 Codex”。来源：[JetBrains 官方博客](https://blog.jetbrains.com/ai/2026/03/codex-in-jetbrains-ides/)。
2. `image-11-jetbrains-ai-first-run.png`（1280×254）：首次打开 JetBrains AI 时的 “Let's Go” 入口。适合“安装或启用 AI Assistant”。来源同上。
3. `image-11-jetbrains-codex-login.png`（1280×720）：JetBrains AI、ChatGPT、API Key 三种 Codex 登录方式。适合“首次登录”。来源同上。
4. `image-11-jetbrains-free-access.png`（1280×450）：JetBrains AI 内的 Codex 限时免费提示。该活动信息可能过期，只有在正文明确标注时效时才使用。来源同上。
5. `image-11-jetbrains-model-choice.png`（1070×654）：Codex 的模型和推理强度选择界面。适合“选择模型与推理预算”。来源同上。

### 补充：OpenAI 官方视频抽帧

1. `image-11-openai-video-task-progress.jpg`（1920×1080，约 03:00）：Codex 读取 Gradle 构建错误、搜索项目文件并执行命令。适合说明真实项目上下文和任务执行状态。
2. `image-11-openai-video-validation.jpg`（1920×1080，约 07:30）：AI Chat 展示多文件修改清单和 IDE diff。适合“审查修改并验证结果”。

两张抽帧均来自 OpenAI 官方 YouTube 视频 [Codex in JetBrains IDEs](https://www.youtube.com/watch?v=1XkVsE9-ZK4)，发布于 2026 年 1 月 22 日。画面内包含演示者小窗，正式发布前可根据版式决定是否保留。

### 延伸观看候选

- `image-11-bilibili-BV1Z6zrBCE8U.jpg`：B 站搬运视频封面，只适合作为延伸观看入口，不用于解释产品界面。
- JetBrains 官方博客内嵌的 OpenAI 官方演示是本轮最完整的视频来源；YouTube 搜索还找到第三方安装教程，但来源级别和界面时效均低于官方素材，本轮不下载。

### 本轮查找记录

- 查询覆盖：OpenAI/JetBrains 官方文档与博客、YouTube、B 站索引、X 与 Reddit 网页索引。
- 成功链路：官方博客原图下载；YouTube 元数据核验、30 秒间隔联系表筛选、关键时间点精确抽帧。
- 受限链路：B 站公开搜索接口返回 412，改用网页索引和已知 BV 链接核验；X、Reddit、小红书、Instagram 当前没有可用登录后端，因此未把未验证结果写入候选。
- 取舍原则：官方产品图优先于社交转载；真实界面优先于封面；来源、用途、时间点不完整的图片不入库。
