---
id: codex-blender-agent-skills
title: Codex 安装 Blender Agent Skills：用 28 个技能做建模、绑定、动画与游戏引擎导出
seo_title: Codex 安装 Blender Agent Skills：28 个技能与安装脚本
description: blender-skills 是一套面向 Blender 5.2 LTS 及以上的开源 Agent Skills，README 列出 28 个技能，覆盖建模、材质、绑定、动画和导出到游戏引擎。本文按仓库 README 和安装脚本说明 Codex 的全局安装、单项目安装和卸载，并标明本文没有 Blender、没有实测。
lede: 用安装脚本把 28 个技能放到 ~/.agents/skills，Codex 会从那里读取。没有 Blender 5.2 就先不要当成已经跑通。
url: /guides/codex-blender-agent-skills
status: published
section: guides
category: G-extensions
topic: Skills 与外部工具
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI]
difficulty: 进阶
order: 17
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-08
date_modified: 2026-11-08
verified_on: 2026-11-08
official_ref: https://github.com/EL4CTEO/blender-skills
keywords: [Codex Blender, Blender Agent Skills, blender-skills, Blender MCP, 3D 建模, 引擎导出]
related: [codex-unity-plugin, create-codex-skill, mcp-getting-started]
faq:
  - q: 这个仓库的发布者是谁？
    a: 作者是 EL4CTEO，许可证是 MIT，仓库创建于 2026-10-14。README 写它适用于 Claude Code、Codex、OpenCode、Gemini CLI、GitHub Copilot 和 Cursor。LICENSE 里的版权人是 EL4CTEO。
  - q: 本文在 Blender 里跑过这些技能吗？
    a: 没有。写作环境没有 Blender 5.2。下文的安装参数来自 README 和安装脚本原文，测试数量来自脚本和文件统计。没有命令输出，也没有视口截图。
  - q: README 写 67 个测试，仓库里是多少？
    a: 2026-11-08 的 README 注释写「67 headless Blender tests」。同一天 main 上，tests/test_*.py 有 26 个文件、69 个以 test_ 开头的函数。本文没有执行 tools/run_tests.py。
  - q: 必须装 Blender MCP 吗？
    a: README 把它写成可选项。有 MCP 时，代理在已经打开的 Blender 里操作；没有时，代理在后台运行 Blender。README 没有给出某一条 MCP 安装命令，本文不补。
---

# Codex 安装 Blender Agent Skills：用 28 个技能做建模、绑定、动画与游戏引擎导出

> 本文在线版：[codexguide.io/guides/codex-blender-agent-skills](https://codexguide.io/guides/codex-blender-agent-skills)

> 核对依据：GitHub 仓库 [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills) 的 README、`install/install.sh`、`install/install.ps1`、`skills/blender-core/SKILL.md`、`tools/run_tests.py` 和 `tests/run_all.py`。2026-11-08 克隆 main，提交 `389f28addc79b87b28764898e38e7bf408d14b77`（2026-11-07 20:16 +0100）。同一天 GitHub API：760 star、77 fork，许可证 MIT，`created_at` 2026-10-14T19:08:14Z，`pushed_at` 2026-11-07T19:16:32Z。Release [v1.2.0](https://github.com/EL4CTEO/blender-skills/releases/tag/v1.2.0) 发布于 2026-10-30T20:35:01Z。`blender-core` 的 `metadata.version` 也是 `1.2.0`。**本文没有安装 Blender，没有执行安装脚本，没有跑 headless 测试，没有截图。**

这是第三方社区项目。作者是 EL4CTEO，许可证是 MIT（版权声明年份 2026）。Blender 本身的文档和 Unity 的官方插件都不是这个仓库。Unity 那条线见 [Codex 安装 Unity 官方插件](./13-Codex安装Unity插件-用Skills辅助Unity开发.md)。

适合已经会用 Codex、并且本机有 Blender 5.2 LTS 或更新版本、希望用固定技能覆盖建模、材质、绑定、动画和引擎导出的人。技能怎么写、怎么触发，见 [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)。

## 先看结论

README 的范围是整条 3D 流程：建模、UV、贴图、烘焙、绑定、动画、服装、毛发、场景、风格化、优化、导出、渲染、视频、天气、模拟和质量检查。它写明面向 **Blender 5.2 LTS+**，并写「每个脚本都在真实的 Blender 里测试过」。这句话是上游对自己仓库的说明。本文没有复现这些测试。

Codex 的安装方式写在 README 的 “Any agent” 一节：克隆仓库，再运行安装脚本。脚本默认会放到 `~/.agents/skills`。README 写 `.agents/skills` 由 Codex、OpenCode、Gemini CLI、Copilot 和 Cursor 读取。可选搭配一个 Blender MCP 服务器；不装的话，代理在后台运行 Blender。

`skills/` 下有 28 个目录，每个目录一个 `SKILL.md`。数量和 README 的技能表一致。

## 准备

README 的要求只有一条硬条件：**Blender 5.2+**。`blender-core` 的 `compatibility` 写的是 Blender 5.2 LTS or newer，并注明 blender-mcp 服务器是可选项。

本文的写作环境没有这个版本，所以下面所有命令都是仓库里的文本，不是一次成功安装的终端记录。有 Blender 的读者先在终端确认 `blender --version` 至少是 5.2，再继续。

## 用安装脚本装到 Codex

README 的步骤：

```bash
git clone https://github.com/EL4CTEO/blender-skills
./blender-skills/install/install.sh          # macOS / Linux
```

```powershell
.\blender-skills\install\install.ps1         # Windows
```

README 写默认会同时装进 `~/.claude/skills` 和 `~/.agents/skills`。2026-11-08 读到的 `install.sh` 头部与此相符：不带参数时，代理列表是 `claude` 和 `agents`。`agents` 和 `codex` 的用户级目录都是 `$HOME/.agents/skills`。因此默认安装已经包含 Codex 要读的那份目录。

只装给 Codex、不装 Claude Code 时，bash 用：

```bash
./blender-skills/install/install.sh --agent codex
```

PowerShell 脚本的参数名是 `-Agent`，不是 bash 的 `--agent`。对应写法是：

```powershell
.\blender-skills\install\install.ps1 -Agent codex
```

README 把选项写成 `--agent claude|codex|opencode|gemini|copilot|cursor|all`、`--project DIR`、`--uninstall`。脚本里还能看到 README 那一行没有展开的参数：

| 脚本 | 还接受的参数 | 作用 |
| --- | --- | --- |
| `install.sh` | `--agent agents` | 与 `--agent codex` 同一目标目录 |
| `install.sh` | `--scope user\|project` | 用户目录或项目目录 |
| `install.sh` | `--copy` | 改成复制；默认是符号链接 |
| `install.sh` | `--skills a,b` | 只处理点名的技能 |
| `install.ps1` | `-Scope user\|project` | 同上 |
| `install.ps1` | `-Link` | 改成目录联接；默认是复制 |
| `install.ps1` | `-Skills a,b` | 只处理点名的技能 |

`--agent all` 在 bash 里展开为 `claude`、`agents`、`opencode`、`gemini`、`copilot`、`cursor`。`codex` 没有单独的目录，它走 `agents` 那一项。PowerShell 的 `-Agent all` 展开的名单相同。

这些参数是阅读 `install.sh` / `install.ps1` 得到的。本文没有执行脚本，没有看到它打印的 `installed N skills`。

符号链接指向克隆下来的 `skills/`。移走或删掉克隆目录后，链接会断。需要一份独立副本时，bash 加 `--copy`，PowerShell 保持默认复制。

## 全局还是单个项目

不带 `--project` / `-Project` 时，范围是当前用户的家目录。

只给一个项目安装时，README 的 `--project DIR` 在两个脚本里都会把范围改成项目：

```bash
./blender-skills/install/install.sh --agent codex --project /path/to/project
```

```powershell
.\blender-skills\install\install.ps1 -Agent codex -Project D:\path\to\project
```

对 `codex`，项目级目录是 `<项目>/.agents/skills`。卸载把同一批目录删掉：

```bash
./blender-skills/install/install.sh --agent codex --uninstall
```

```powershell
.\blender-skills\install\install.ps1 -Agent codex -Uninstall
```

项目级卸载要带上当时的 `--project` 或 `-Project`，否则脚本会按用户级目录处理。这一点来自脚本里「出现 project 参数就把 scope 设为 project」的分支，本文没有跑卸载。

装完之后，新开一个 Codex 会话，再让它做 Blender 任务。本文没有登录后的会话，没有检查斜杠菜单里是否出现这些技能。

## 28 个技能

下表的名字和分工来自 README 的技能表，并与 `skills/` 下的 28 个目录名逐个对过。中文是对 README 那一列的翻译。`blender-core` 里有一张更细的路由表，任务开始时它要求先读这个技能。

| 技能 | README 写的用途 |
| --- | --- |
| `blender-core` | 入口：运行代码、把任务分到其他技能、5.x API 规则 |
| `blender-scene-setup` | 单位、命名、集合、资产库 |
| `blender-hardsurface-modeling` | 倒角、布尔、加权法线 |
| `blender-sculpting` | 有机雕刻 |
| `blender-retopology-uv` | 重拓扑、UV、纹素密度 |
| `blender-pbr-materials` | 由贴图做 PBR 材质 |
| `blender-texturing` | 边缘磨损、污渍、灰尘、贴花、trim sheet |
| `blender-texture-baking` | 法线、AO、曲率、ORM |
| `blender-geometry-nodes` | 用 JSON 做几何节点程序化建模 |
| `blender-character-rigging` | Rigify、蒙皮、游戏骨架 |
| `blender-facial-shapekeys` | ARKit 52 个形态键、视素 |
| `blender-animation` | 动作、动捕重定向、循环检查、根运动 |
| `blender-clothing` | 跟随身体、避免穿插的服装 |
| `blender-hair-grooming` | 毛发、皮毛、游戏发片 |
| `blender-game-optimization` | 面数预算、LOD、绘制调用 |
| `blender-export-pipelines` | 导出到 Roblox、Unity、Unreal、Godot、Web、USD |
| `blender-rendering` | Cycles 与 EEVEE、批量渲染 |
| `blender-lighting-lookdev` | 摄影棚灯光、HDRI、转台 |
| `blender-stylized-npr` | 卡通着色和轮廓 |
| `blender-environment-kits` | 地形、森林、模块化关卡 |
| `blender-video-editing` | 剪辑、摄像机跟踪 |
| `blender-simulation` | 刚体、布料、流体 |
| `blender-time-of-day` | 黄金时刻、夜晚、雾和氛围光 |
| `blender-weather-fx` | 雨、雪、湿地、水坑、闪电 |
| `blender-addon-development` | Blender 扩展 |
| `blender-pipeline-automation` | 批处理和文件转换 |
| `blender-asset-qa` | 检查 z-fighting、浮空、法线、权重和贴图 |
| `blender-workflow-recipes` | 完整资产的操作顺序 |

README 给了五句可以直接试的英文提示，例如为 Unreal 做带烘焙法线和 LOD 的箱子、用 Rigify 绑定并导出到 Unity、检查 z-fighting 后导出到 Roblox。项目站上有一张「有技能 / 没有技能」的对比：[comparison](https://el4cteo.github.io/blender-skills/comparison/)。那是上游页面。本文没有打开对比图，也没有用同一提示各跑一遍。

## 可选的 Blender MCP

README 只写：一个 Blender MCP 服务器可以让代理操作你已经打开的 Blender；没有的话，代理在后台运行 Blender。`blender-core` 把实时路径写成 blender-mcp 的 `execute_blender_code`，并提醒每次调用都在新的 Python 命名空间里，脚本要重新 import。

仓库 README 没有指定某个 MCP 包的安装命令或配置片段。本文不补一条来自别处的安装命令。MCP 在 Codex 里怎么写进配置，见 [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)。接上之后，实时会话改的是你正在用的那份 `.blend`。`blender-core` 写明：不要读工厂设置，不要删除不是这次任务创建的数据，批量破坏性修改前先存一份副本。

## headless 批处理

没有 MCP 时，`blender-core` 给出的后台入口是：

```text
python <skills_dir>/blender-core/scripts/run_in_blender.py --blend in.blend <script.py> -- --objects Chair --save out.blend
python <skills_dir>/blender-core/scripts/run_in_blender.py --expr "import bpy; print(len(bpy.data.objects))"
```

它也写了不经过这个包装脚本的形式：`blender -b in.blend --factory-startup --python-exit-code 1 -P x.py -- args`。技能要求每次会话先跑 `scripts/env_report.py`，看版本、引擎、GPU 和插件。交付前跑 `blender-asset-qa`。这些是技能文件里的步骤。本文没有 Blender 可执行文件，一条都没有跑。

上游的测试入口写在 README：

```bash
python tools/validate_skills.py   # spec + token budget checks
python tools/run_tests.py         # 67 headless Blender tests (BLENDER_EXE to override)
```

`run_tests.py` 会找本机 Blender（可用环境变量 `BLENDER_EXE` 指定），再用 `blender -b` 执行 `tests/run_all.py`。找不到 Blender 时，脚本打印 `Blender not found; set BLENDER_EXE` 并返回退出码 2。这是阅读脚本得到的分支，不是这次的运行输出。

README 注释里的 67，和 2026-11-08 仓库里的函数数量不一致：`tests/test_*.py` 有 26 个文件，其中 `def test_` 共 69 个。`run_all.py` 会执行这些函数。本文没有运行，所以不知道当天在 Blender 5.2 里实际通过多少。

## 卸载与排障

- 卸载用上一节的 `--uninstall` / `-Uninstall`，代理和项目参数与安装时一致。
- bash 默认是符号链接。克隆目录还在，技能才有效。
- PowerShell 默认是复制。更新仓库之后要重新运行安装脚本，复制出去的那份才会变。
- Codex 仍用旧会话时，先新开一个会话再试技能。
- 后台运行找不到 `blender` 时，先把 Blender 5.2+ 放进 `PATH`，或设置技能脚本所认的 `BLENDER_EXE`。具体变量名以 `run_in_blender.py` 里的 `find_blender` 为准；测试脚本明确写了 `BLENDER_EXE`。
- 实时操作没有反应时，先确认你确实另装了一个 Blender MCP，并且 Codex 的 MCP 配置指向它。本文没有一份可用的 MCP 配置。

## 参考资料

- [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills)
- [v1.2.0](https://github.com/EL4CTEO/blender-skills/releases/tag/v1.2.0)
- [MIT License](https://github.com/EL4CTEO/blender-skills/blob/main/LICENSE)
- [上游对比页](https://el4cteo.github.io/blender-skills/comparison/)
- [从零创建 Codex Skill](../07-Skills实战/04-从零创建Codex-Skill.md)
- [Codex MCP 入门](./01-Codex-MCP入门-config与mcp-login.md)
