# 做一个批量图片压缩与格式转换 Skill

每次整理文章配图，我都要重复做几件事：把图片缩到合适尺寸、转成 WebP、控制文件大小，再检查原图有没有被覆盖。单独处理一两张不麻烦，图片一多，漏改尺寸或误删原图就很常见。

这篇实战准备把这套流程做成一个可复用的 Skill。先从一个具体任务开始：把指定文件夹中的图片统一缩放到 1200px 宽，转成 WebP，质量设为 85，并保留原文件。

> 当前状态：文章结构已初始化，运行截图、压缩数据和最终 Skill 仓库链接将在实测后补充。

## 一、先确定输入和输出

这次不做一个什么图片都能处理的万能工具，只解决文章配图中最常见的一组需求。

输入是一批 JPG、JPEG、PNG 或 WebP 图片。输出图片放进新的目录，默认不覆盖原文件。宽度超过 1200px 时等比缩小，不足 1200px 时不放大，避免小图被强行拉糊。

第一版先支持这些参数：

| 参数 | 默认值 | 作用 |
| --- | --- | --- |
| 输入目录 | 用户指定 | 读取待处理图片 |
| 输出目录 | `output` | 保存处理后的图片 |
| 最大宽度 | `1200` | 超出后等比缩小 |
| 输出格式 | `webp` | 统一图片格式 |
| 图片质量 | `85` | 平衡清晰度和文件大小 |
| 保留原图 | `true` | 不覆盖、不删除源文件 |

## 二、为什么选 Sharp

这次准备使用 Node.js 和 Sharp。Sharp 可以读取常见图片格式，也能在一次处理中完成缩放、格式转换和质量设置。它在 Windows、macOS 和 Linux 上都能使用，放进 Skill 的脚本里比较省事。

ImageMagick 也能完成同样的任务，适合本机已经装好命令行工具的人。为了让教程步骤更容易复现，第一版只维护 Sharp 脚本，不同时写两套实现。

## 三、规划 Skill 目录

Skill 暂定名为 `batch-image-converter`，目录保持精简：

```text
batch-image-converter/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── convert-images.mjs
```

`SKILL.md` 负责说明何时触发、怎样确认参数和如何检查结果。真正重复执行的图片处理逻辑放在 `scripts/convert-images.mjs`，这样下次不需要临时重写脚本。

## 四、初始化 Skill

使用 `skill-creator` 提供的初始化脚本创建目录，并只生成这次需要的 `scripts` 资源目录。

```powershell
python D:\CodexHome\skills\.system\skill-creator\scripts\init_skill.py batch-image-converter `
  --path D:\CodexHome\skills `
  --resources scripts `
  --interface "display_name=批量图片转换" `
  --interface "short_description=批量缩放、压缩并转换图片格式" `
  --interface "default_prompt=把指定文件夹中的图片缩放到 1200px 宽，转成 WebP，质量设为 85，并保留原文件。"
```

<!-- TODO：补充 Skill 初始化完成后的目录截图。 -->

## 五、写清楚触发条件

Skill 的 `description` 不能只写“处理图片”。它需要说明能做什么，以及用户说出哪些需求时应该调用。

```yaml
---
name: batch-image-converter
description: Batch resize, compress, convert, and rename JPG, PNG, and WebP images while preserving source files. Use when the user asks to optimize images for websites or articles, convert image formats, limit image dimensions, reduce file size, or batch rename image assets.
---
```

正文则只保留执行步骤：确认输入目录和输出规则，运行脚本，核对处理数量、尺寸与文件大小，最后报告失败文件。原图默认只读，除非用户明确要求覆盖。

## 六、实现批处理脚本

脚本需要递归读取图片、跳过不支持的文件，并为输出目录创建对应结构。每张图片处理完成后记录原始尺寸、输出尺寸和文件大小；单张图片失败时继续处理其余文件，最后统一列出错误。

第一版的命令计划写成这样：

```powershell
node scripts/convert-images.mjs `
  --input "D:\images\original" `
  --output "D:\images\output" `
  --width 1200 `
  --format webp `
  --quality 85
```

<!-- TODO：补充 convert-images.mjs 的完整实现与参数说明。 -->

## 七、实际调用一次

安装完成后，可以直接对 Codex 说：

```text
使用 batch-image-converter，把这个文件夹里的图片统一缩放到 1200px 宽，转成 WebP，质量设为 85。输出到新文件夹，保留原文件。处理前先告诉我预计会处理多少张图片。
```

执行结束后，不能只看脚本有没有报错。还要抽查横图、竖图、透明 PNG 和本来就很小的图片，确认比例没有变化，透明背景没有意外变黑，小图也没有被放大。

<!-- TODO：补充处理前后的文件夹截图。 -->

## 八、记录压缩结果

实测时记录处理前后的总大小，方便判断质量 85 是否适合文章配图。

| 项目 | 处理前 | 处理后 |
| --- | ---: | ---: |
| 图片数量 | 待补充 | 待补充 |
| 总文件大小 | 待补充 | 待补充 |
| 最大宽度 | 待补充 | 1200px |
| 输出格式 | JPG/PNG/WebP | WebP |
| 失败数量 | - | 待补充 |

<!-- TODO：补充一组原图与 WebP 的清晰度对比图。 -->

## 九、验证 Skill

内容写完后，先运行官方校验脚本检查目录名和 `SKILL.md` 的 YAML 头部。

```powershell
python D:\CodexHome\skills\.system\skill-creator\scripts\quick_validate.py D:\CodexHome\skills\batch-image-converter
```

接着用一份测试目录检查这些情况：

- JPG、PNG 和 WebP 都能正常处理
- 宽图和竖图保持原始比例
- 小于 1200px 的图片不会被放大
- 输出目录已存在时不会误删旧文件
- 同名文件不会静默覆盖
- 单张图片损坏时，其余图片仍能继续处理
- 原始图片的数量、名称和内容保持不变

## 十、这篇实战还要补什么

下一步会先完成脚本，再用一组真实文章配图跑一遍。文章最终需要补齐三类证据：初始化后的 Skill 目录、Codex 实际调用过程，以及处理前后的尺寸和文件大小对比。

等这些结果都能复现，再决定是否加入批量重命名、AVIF 输出和按文件大小自动调整质量。第一版先把“缩放、转 WebP、保留原图”做稳。
