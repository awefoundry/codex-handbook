# 从零创建 Codex Skill

> 难度　进阶
>
> 类型　Skill 编写与调试

如果一段提示词需要反复复制，或者同一项工作每次都要重新说明步骤、输入和验收条件，可以把这套做法整理成 Skill。Codex 会先读取 Skill 的名称和描述，任务匹配后再加载完整说明，需要时继续读取参考资料或运行脚本。

这篇教程会创建一个最小可用的 Skill，并检查显式调用和自动触发是否符合预期。示例只写文件，不连接外部服务，也不会运行付费操作。

![Codex 按 Skill 中的步骤执行重复工作](../图片素材/07-Skills实战/04-从零创建Codex-Skill/01-Codex-Skill工作流示意.png)

> 原稿示意图，非 Codex 产品界面。图中的工作流用来解释 Skill 如何保存重复步骤。

## Skill 适合保存什么

Skill 适合边界清楚、会重复出现、结果能够检查的工作。例如按团队格式创建变更日志、检查发布文件、生成固定结构的项目目录，或者把一套人工检查步骤交给 Codex 执行。

一次性的临时任务通常不需要 Skill。流程还在频繁变化时，也可以先把提示词跑顺，确认输入、输出和失败条件后再整理。这样写出来的说明更短，触发范围也更准确。

## 一个 Skill 目录里有什么

最小 Skill 只需要一个目录和其中的 `SKILL.md`。文件开头的 YAML 元数据必须提供 `name` 和 `description`，后面是 Codex 选中 Skill 后读取的操作说明。

```text
my-skill/
└── SKILL.md
```

复杂工作可以继续加入这些目录。

```text
my-skill/
├── SKILL.md
├── scripts/
├── references/
├── assets/
└── agents/
    └── openai.yaml
```

需要稳定执行的程序放进 `scripts/`，较长的规范和资料收进 `references/`。模板等资源归到 `assets/`，`agents/openai.yaml` 用于补充展示和依赖信息。没有实际用途的目录不要提前创建。

![Skill 的必需文件和可选目录](../图片素材/07-Skills实战/04-从零创建Codex-Skill/02-Skill目录结构.png)

> 原稿示意图，目录结构按 OpenAI 当前 Skill 文档复核。

## 选择个人目录还是项目目录

个人 Skill 放在用户目录下，适合自己在多个项目中复用。项目 Skill 放进仓库，适合团队共享并随代码一起审查。

```text
$HOME/.agents/skills/my-skill/SKILL.md
.agents/skills/my-skill/SKILL.md
```

Windows 环境中的实际用户目录会随安装方式变化。创建前可以先查看当前 Codex 的 Skills 列表和已发现路径，不要照抄别人的绝对路径。

项目 Skill 可以提交到 Git。个人 Skill 通常留在本机，除非你准备把它包装成可以分发的插件。

## 写一个最小可用的 Skill

下面创建一个 `release-note` Skill。它接收一组已经确认的改动，把内容整理成简短发布说明，并明确禁止编造测试结果。

```md
---
name: release-note
description: 根据已经确认的代码改动和验证结果生成中文发布说明。用户要求写发布说明、版本说明或 changelog 摘要时使用；缺少真实改动或验证证据时不要猜测。
---

# 发布说明

1. 读取用户提供的改动摘要、提交或 diff。
2. 区分新增、修复和已知限制，只保留有证据的内容。
3. 使用简短中文说明用户能够感知的变化。
4. 保留版本号、命令、文件名和链接的原始写法。
5. 没有执行过的测试标记为未验证，不得写成已经通过。

输出一段发布摘要和一份变更列表。
```

`description` 决定 Codex 能否发现这个 Skill。它需要同时说明用途、触发场景和边界。只写“帮助处理发布工作”范围太宽，容易误触发；把所有例外都塞进描述又会让入口信息过长。详细步骤留在正文里。

## 渐进式加载怎样节省上下文

Codex 启动时不会把所有 Skill 全文塞进上下文。它先看到名称、描述和路径，选中某个 Skill 后才读取 `SKILL.md`。引用资料和脚本也只在流程需要时加载。

![Codex 先读取 Skill 元数据，选中后再加载完整说明](../图片素材/07-Skills实战/04-从零创建Codex-Skill/03-Skill渐进式加载.png)

> 原稿示意图。图中的比例用于解释渐进式加载，实际上下文占用由已安装 Skill 数量和描述长度共同决定。

因此，主文件应该保留执行流程和关键边界。大段背景资料可以移到 `references/`，稳定且需要精确重复的动作才适合写成脚本。脚本会直接在工作环境里运行，涉及删除、网络、凭据或外部计费时要保留明确的审批步骤。

## 测试显式调用

在 Codex CLI 或 IDE 扩展中，可以运行 `/skills` 查看已经发现的 Skill，也可以在提示中输入 `$` 选择并显式调用。

```text
使用 $release-note，根据当前分支相对 main 的提交写一份发布说明。先读取 diff 和测试结果，不要修改文件。
```

显式调用适合第一次测试。检查结果时重点看三件事。

1. Codex 是否读取了正确的 `SKILL.md`。
2. 输出是否遵守了输入和验证边界。
3. Skill 是否执行了任务之外的动作。

如果找不到 Skill，先检查目录层级、文件名和 YAML 格式，再确认当前入口支持 Standalone Skill。

## 测试自动触发

显式调用通过后，再用自然语言测试 `description`。

```text
根据这个分支的改动写一份中文 changelog 摘要，未运行的检查要标出来。
```

还要准备一个不应该触发的任务。

```text
帮我解释 changelog 这个词是什么意思，不要读取项目文件。
```

第一个任务应该命中 `release-note`，第二个任务只需要普通回答。两边都测试，才能发现描述写得太窄还是太宽。

## 什么时候加入脚本和参考资料

纯说明能完成工作时，先保持纯说明。下面这些情况再考虑加脚本。

- 同一条命令必须稳定执行，并且参数和输出格式清楚。
- 人工复制步骤容易出错，脚本可以先做只读检查或 dry run。
- 验证需要解析结构化结果，靠文字判断不够可靠。

参考资料适合保存字段定义、团队规范和长示例。`SKILL.md` 应当告诉 Codex 何时读取哪份资料，避免把整个参考目录一次加载。

![长提示词被 Skill 取代后的复用方式](../图片素材/07-Skills实战/04-从零创建Codex-Skill/04-重复提示词与Skill复用对比.png)

> 原稿示意图。实际效果取决于 Skill 的边界、材料质量和验证步骤。

## 发布前检查

- `SKILL.md` 包含有效的 `name` 和 `description`。
- 名称与目录用途一致，描述写清触发条件和边界。
- 每一步都有明确输入、动作和输出。
- 没有把 Token、账号和机器绝对路径写进共享 Skill。
- 涉及写入、删除、网络和付费操作时保留审批与失败处理。
- 显式调用、应该自动触发和不应该触发的提示都测试过。
- 项目 Skill 的脚本和引用文件已经纳入 Git 审查。

## 参考资料

- [OpenAI Build skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex customization](https://developers.openai.com/codex/concepts/customization)
- [OpenAI Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [原始公众号文章](https://mp.weixin.qq.com/s?__biz=MzAwMDg5MTAyMw==&mid=2247521461&idx=1&sn=c1991f8612a6443af76cff8df9cc4ad3&chksm=9b5043639049220389dab5485957088b07b83dae4657aa9d47bc2681478d50b24baba1796131#rd)

本文根据 OpenAI 2026 年 8 月 18 日可访问的 Skill 文档核对。不同 Codex 入口对 Standalone Skill 和插件 Skill 的支持范围可能不同。
