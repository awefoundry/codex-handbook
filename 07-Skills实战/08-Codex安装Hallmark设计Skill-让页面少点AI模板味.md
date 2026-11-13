---
id: codex-hallmark-design-skill
title: Codex 安装 Hallmark 设计 Skill：50 套主题加浏览器检查，让页面少点 AI 模板味
seo_title: Codex 安装 Hallmark：50 套主题、redesign 与 sloplint
description: Hallmark 是 Together AI 的开源设计 Skill，可装进 Codex。本文核对 50 个主题文件、npx skills 的安装路径，以及 redesign、audit 和 sloplint 在技能说明里怎么写。没有在 Codex 里生成页面。
lede: 它交给 Codex 的是一套页面约束和主题文件。装上之后先读 SKILL.md，再决定要不要让它改你的前端。
url: /guides/codex-hallmark-design-skill
status: published
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI]
difficulty: 进阶
order: 8
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-09
date_modified: 2026-11-09
verified_on: 2026-11-09
official_ref: https://github.com/Nutlope/hallmark
keywords: [Codex Hallmark, hallmark skill, npx skills add, sloplint, 前端设计 Skill]
related: [create-codex-skill, codex-skillspector-skill-security-scan, codex-browser-e2e-acceptance]
howto: true
faq:
  - q: 仓库写 50 套主题，文件数对得上吗？
    a: 2026-11-09 查看 main 分支 skills/hallmark/references/themes，除 README.md 外有 50 个 .md，另有 50 个 .jpg 和 index.json。安装到隔离目录后，主题 .md 仍是 50 个。package.json 的 version 是 2.0.0。
  - q: 装完就能用 $hallmark 生成页面吗？
    a: 安装器把文件放到了 Codex 会扫描的 .agents/skills。本文没有启动 Codex，没有发送 $hallmark，也没有改版或审计任何页面。
  - q: 浏览器检查一定会跑吗？
    a: SKILL.md 要求在有 Node 时运行 sloplint.mjs --render。渲染脚本在找不到 puppeteer-core 或 puppeteer 时返回 notRun，找不到 Chrome 时同样不启动浏览器。静态检查和渲染检查是两截。
---

# Codex 安装 Hallmark 设计 Skill：50 套主题加浏览器检查，让页面少点 AI 模板味

> 本文在线版：[codexguide.io/guides/codex-hallmark-design-skill](https://codexguide.io/guides/codex-hallmark-design-skill)

> 核对依据：第三方仓库 [Nutlope/hallmark](https://github.com/Nutlope/hallmark) 的 README、`package.json`、`skills/hallmark/SKILL.md` 和 `references/redesign.md`，许可证为 MIT。README 写明由 Together AI 制作，不是 OpenAI 官方 Skill。2026-11-09 通过 GitHub API 看到 50,978 stars、2,708 forks，最近推送 `2026-11-05T13:16:31Z`，仓库创建于 `2026-04-27T20:47:10Z`。安装使用 `skills` 1.7.6，目录放在隔离的主目录和临时项目里。没有登录 Codex，没有生成或改版页面，没有配图。

Hallmark 是一份给编码代理用的前端设计 Skill。Codex 读到它之后，会按其中的步骤选主题、写页面，并在有条件时用浏览器做检查。它改变的是代理手里的说明书，不是 Codex 的模型。

## 先看结论

它能做的，是把一组写进 `SKILL.md` 的约束交给 Codex：颜色和字体走令牌、不要发明数据、改旧页时先点名 Hallmark。主题文件当天数过是 50 个。它不能替你保证生成结果「看起来不像模板」。本文没有跑过一次真实生成，所以没有页面可以拿来判断。

安装本身在隔离环境里完成了。全局安装落到 `~/.agents/skills/hallmark`，项目安装落到 `./.agents/skills/hallmark`。调用名要等你自己的 Codex 会话确认：README 写 Codex 用 `$hallmark`，`SKILL.md` 的说明文字里又出现 `/hallmark redesign`。

## 安装

README 的命令是：

```bash
npx skills add nutlope/hallmark -g
```

它写明需要 Node.js 18 或更新版本。不加 `-g` 时装进当前项目。只装给 Codex 时加上 `--agent codex`。

2026-11-09 的 `skills` 版本是 1.7.6。为了不写进这台机器的真实主目录，命令使用了隔离的 `HOME`，并加上 `-y` 和 `--copy`：

```bash
npx skills add nutlope/hallmark -g -a codex -y --copy
npx skills add nutlope/hallmark -a codex -y --copy
```

安装器的 JSON 结果：

| 命令 | scope | 路径 | agents |
| --- | --- | --- | --- |
| 带 `-g` | global | `~/.agents/skills/hallmark` | Codex |
| 不带 `-g`，在项目目录里 | project | `./.agents/skills/hallmark` | Codex |

两次的 `SKILL.md` 都在。`version` 字段是 `2.0.0`，与仓库 `package.json` 的 `version` 相同。Codex 怎样扫描这两个位置，见 [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)。

安装器同时打印了安全评估：Gen 为 Med Risk，Socket 为 0 alerts，Snyk 为 Low Risk，详情页是 [skills.sh/nutlope/hallmark](https://skills.sh/nutlope/hallmark)。这是安装器当天的摘要。Skill 正文会让代理执行 `node scripts/theme.mjs` 和 `node scripts/sloplint.mjs`，也会在能连上产品时用 `scripts/capture.mjs` 截图。装之前应自己读完 `SKILL.md`。扫描步骤见 [SkillSpector](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)。本文没有跑 SkillSpector，也没有执行这些脚本。

## 在 Codex 里怎么调用

README 的表把 Codex CLI 的调用写成 `$hallmark <prompt>`，并写也可以用普通句子描述一次新页面。`SKILL.md` 的 `description` 写：用户要做新页面，或点名 Hallmark 时使用；已经存在的设计，除非用户点名 Hallmark（例子是 `` `/hallmark redesign <path>` ``），否则不要用这份 Skill。`argument-hint` 是 `<prompt> | redesign <path> | audit <path>`。

因此仓库里同时出现了 `$hallmark` 和 `/hallmark` 两种写法。Codex 的显式调用惯例是 `$` 前缀，见创建 Skill 一文。本文没有打开会话，没有看到选择器里的实际名字，也没有收到一份生成的 HTML。

跟做时可以先只问它解释自己会读哪些文件，确认触发的是 hallmark，再给一个不连生产数据的小页面。本文没有这一步的输出。

## 50 个主题和 custom

2026-11-09 列出 `skills/hallmark/references/themes`：50 个主题 `.md`、50 张同名 `.jpg`、`index.json`，以及目录里的 `README.md`。安装副本里的主题 `.md` 也是 50 个。README 里的 “fifty themes” 和这个数字一致。本文没有打开 usehallmark.com 上的预览，也不把 README 表格里的示例站点名当作实测页面。

`SKILL.md` 把主题说成材料，而不是版式顺序：调色、字体和组件来自主题文件，页面上有什么则来自任务。选择顺序写的是：

1. 用户点名某个主题，就用那个主题。
2. 用户要求 custom（说明文字里还包括 “no theme” 等说法），就不加载主题文件，改读 `references/direction.md`。Floor 里的约束仍然保留。
3. 其余情况运行 `node <skill-dir>/scripts/theme.mjs deal`，从符合提示词的主题里给出三个，再只加载其中一份 `references/themes/<slug>.md`。

没有 Node 时，说明文字要求改从 `index.json` 里手选，并在标记里写上 `deal: manual`。本文没有运行 `theme.mjs`。

## redesign 和 audit

`references/redesign.md` 写明，只有用户点名 Hallmark 并且使用 redesign 或 audit 时才加载这份说明。一次没点名的改样式、改颜色或小修，按项目原来的样式做。

点名之后，说明文字把默认深度定义为 **full**：留下页面上已有的内容和接线（链接、表单、字段、事件处理、路由、测试用的 id），更换设计系统和版式。同一请求里如果写了 keep the layout、restyle，深度是 **restyle**；如果写了 polish 或只修看起来像生成的部分，深度是 **polish**。三种深度不能混用。

动手前，说明文字要求先跑：

```bash
node <skill-dir>/scripts/sloplint.mjs <target> --genre <genre> --render --before
```

它应记下链接、表单、字段、标题和图片。改完后再跑带 `--kept` 的检查。说明文字写：原先有、改完没有的链接、表单、字段或处理函数记为 `FAIL kept`；标题和图片一类记为 `WARN kept`。本文没有这些命令的输出，也没有 `.hallmark/before.json`。

audit 在 `SKILL.md` 里定义为只出报告。redesign 一文还写：只有线上 URL、手里没有源码时，只能通过 `--url` 做审计，不能当成有源码的改版。

## sloplint 的浏览器检查

`SKILL.md` 的 Floor 第 16 条要求：有 Node 时，交回结果前运行 `node <skill-dir>/scripts/sloplint.mjs <output> --render`，并处理 `FAIL` 和 `REFLEX`。渲染由 `scripts/sloplint-render.mjs` 完成。阅读这份脚本可以看到：

- 它依次寻找 `puppeteer-core` 或 `puppeteer`，查找范围包括当前目录、脚本目录、环境变量 `HALLMARK_PUPPETEER` 和 `npm root -g`。都找不到时，结果标记为 `notRun`，文字是 `no puppeteer-core found locally, globally or via HALLMARK_PUPPETEER`。
- 找到库之后还要找 Chrome 或 Chromium，或 `CHROME_PATH`。找不到时，`notRun` 的文字是 `no Chrome or Chromium found; set CHROME_PATH`。
- 找到之后，脚本用 `puppeteer.launch({ headless: true })` 打开页面。

README 写的准备是 `npm i -g puppeteer-core` 再加本机 Chrome；没有它们时，静态检查仍会跑。这和脚本里「渲染层可以 notRun」一致。本文没有安装 puppeteer，也没有对样例 HTML 跑 sloplint，所以没有八种宽度的截图，也没有 FAIL 列表。

`capture.mjs` 同样依赖 puppeteer 和 Chrome，用来截正在运行的产品。本文没有运行它。

浏览器里的上线验收仍按测试用例做，见 [前端到端验收](../06-测试调试与质量保障/01-Codex做上线前端到端验收.md)。Hallmark 的渲染检查是这份 Skill 自己的门禁，不是那篇验收清单的替代。

## 装上之前先看什么

- 许可证是 MIT。仓库说明由 Together AI 维护。
- `SKILL.md` 允许代理执行仓库里的 Node 脚本，并在能访问应用时截图。
- 安装器给出的是 Med Risk / 0 alerts / Low Risk 这一行摘要，详情以 skills.sh 当天页面为准。
- 照片库在 README 里指向 Wikimedia Commons，并写明不使用 Unsplash、Pexels、Pixabay。本文没有统计 `photos.json` 的条目数，也不引用 README 里的照片数量。

确认目录和触发之后，再在一次性的练习页上试用。不要对还没有提交的生产页面直接做 full redesign。说明文字自己也要求：在 git 项目里从干净工作区开始，由人来提交或暂存，Skill 不去执行提交。

## 参考资料

- [Nutlope/hallmark](https://github.com/Nutlope/hallmark)
- [skills.sh/nutlope/hallmark](https://skills.sh/nutlope/hallmark)
- [从零创建 Codex Skill](./04-从零创建Codex-Skill.md)
- [SkillSpector](../09-MCP与外部工具/07-Codex用SkillSpector扫描第三方Skill-提示注入与数据外泄检查.md)
