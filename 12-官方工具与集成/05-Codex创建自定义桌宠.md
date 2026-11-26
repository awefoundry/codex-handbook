---
id: codex-create-custom-pet
title: "Codex 桌宠怎么用：桌面端悬浮宠物、终端宠物和网页宠物怎么选，/pet 开关、状态提示和自制 hatch-pet 宠物"
seo_title: "Codex 桌宠怎么开：启用 Pets 并用参考图自制宠物"
seo_description: "Codex 桌宠（Pets）在桌面端设置的外观里开启，先选一只内置宠物；想要自己的角色，从 Create your own pet 安装 hatch-pet Skill，上传一张参考图生成动画精灵图。附提示词、动作检查和常见问题。"
description: "Codex 桌宠是可选的动画伙伴，选哪一只只改外观，不改任务怎么完成。本文按官方文档说明桌面端、网页和终端三种宠物，/pet 与状态，以及 hatch-pet 和网页上传规格。"
lede: "桌面端可以悬浮在其他窗口上。网页宠物只出现在支持的 ChatGPT Work 对话里。IDE 扩展没有宠物。"
url: /guides/codex-create-custom-pet
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI, Chat]
difficulty: 进阶
order: 5
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-12
date_modified: 2026-11-26
verified_on: 2026-11-26
official_ref: https://learn.chatgpt.com/docs/pets
keywords: [Codex 桌宠, Codex Pets, Codex /pet, hatch-pet, Codex 自定义宠物]
related: [codex-appshots, codex-voice-chatgpt-voice, codex-skills-install-guide]
howto: true
faq:
  - q: "三种宠物能互相代替吗？"
    a: "不能。桌面端（macOS 和 Windows）有悬浮层、活动托盘和 /pet。网页宠物出现在支持的 ChatGPT Work 对话里，没有悬浮层、活动托盘和 /pet。终端宠物只报告当前 CLI 会话，而且要求 iTerm2 3.6 以上或支持 Kitty graphics、Sixel 的终端。IDE 扩展没有宠物。"
  - q: "桌面端现在从哪里打开？"
    a: "官方写：打开应用底部的个人资料菜单选 Pets，或打开 Settings 再进 Pets。再用 /pet，或在命令菜单里选 Show pet。设置页的 Pets 一节还写了 Hide pet 和 Mini。旧文里的「设置 > 外观 > 启用 Pets」和「Create your own pet」与这两页的现行写法不一致。"
  - q: "自制宠物会同步到网页吗？"
    a: "不会自动同步。桌面端创建的自定义宠物存在本机。网页要另外用 Upload pet，文件必须是透明 PNG 或 WebP，恰好 1536 × 1872 像素，不超过 20 MiB。"
  - q: "终端里 tmux 能显示宠物吗？"
    a: "官方写明不能。tmux 和 Zellij 里不可用。"
---

# Codex 桌宠怎么用：桌面端悬浮宠物、终端宠物和网页宠物怎么选，/pet 开关、状态提示和自制 hatch-pet 宠物

> 本文在线版：[codexguide.io/guides/codex-create-custom-pet](https://codexguide.io/guides/codex-create-custom-pet)

> 核对依据：2026-11-26 打开的 [Pets](https://learn.chatgpt.com/docs/pets)，以及 [Settings](https://developers.openai.com/codex/app/settings) 的 Pets 一节。Settings 页写：在 Settings > Pets 里选内置或自定义宠物，再用 `/pet`、Show pet 或 Hide pet 控制悬浮层；选 Mini 可以只留聊天控件、不显示宠物。没有打开桌面应用，没有打开交互式 CLI，没有安装 hatch-pet，没有配图。

Pets 是可选的动画伙伴，用来跟着工作看进度。它出现在哪里、显示什么，取决于你用的界面。选哪一只只改外观，不改 ChatGPT 怎样完成任务。

## 先说结论

三种都能用的时候，按你人在哪个界面选。

**桌面端。** macOS 和 Windows 的 ChatGPT 桌面应用里，宠物可以浮在其他应用窗口上面。控件在它下方，用来打字或说话开对话，并在你使用其他应用时看进度。

**网页。** 账号和工作区可用时，在 **Settings > Personalization > Pet > Select pet** 里选内置宠物，或选 **Default** 不用宠物。网页宠物出现在支持的 ChatGPT Work 对话里面。它没有桌面端的悬浮层、活动托盘和 `/pet`。

**终端。** 在交互式 Codex CLI 会话里用 `/pets`、`/pet`、`/pets <name>` 或 `/pets off`。它只报告当前这一次 CLI 会话，状态名和桌面端相同，但没有多对话的活动托盘。

IDE 扩展没有宠物选择器，也没有悬浮层。要用自己的宠物，打开桌面应用或 Codex CLI。技能怎么装，见 [Codex Skills 怎么安装](../07-Skills实战/11-Codex-Skills怎么安装-三种方式完整流程.md)。

## 桌面端：选宠物、开关和大小

1. 打开应用底部的个人资料菜单，选 **Pets**。也可以打开 [Settings](https://learn.chatgpt.com/docs/reference/settings) 再进 **Pets**。
2. 选一只内置或自定义宠物。选 **Mini** 则只显示聊天控件、不显示宠物。还没有自定义宠物时，先选 **Create pet**。
3. 输入 `/pet`，或打开命令菜单选 **Show pet**。右键宠物可以选 **Hide**。

改大小：在 **Settings > Pets** 里选 **Customize**，调 **Pet size**。**Reset** 恢复默认大小。选中自定义宠物后，它也会出现在 **Profile** 视图里。

桌面应用开着时，用全局快捷键显示控件并聚焦 Quick Chat：

| 系统 | 默认快捷键 |
| --- | --- |
| macOS | Option+Space |
| Windows | Windows+Alt+P |

**Show pet** 可以在 **Settings > Keyboard shortcuts** 里改。再按一次快捷键，控件保持打开，并聚焦 Quick Chat。

隐藏控件：右键宠物选 **Hide**；或在命令菜单、**Settings > Pets** 里选 **Hide pet**；或再输入一次 `/pet`。宠物的选择和位置在重新打开应用后还在。控件不可用时，先更新应用，并看工作区是否允许宠物。

操作系统开了减少动态效果时，宠物用静止帧，不再播放精灵动画。

旧文写的入口是「设置 > 外观 > 启用 Pets」，自制入口写成 `Settings > Pets > Create your own pet`。2026-11-26 的 Pets 页和 Settings 页都没有「外观里启用 Pets」或 “Create your own pet” 这两个字。外观页现在写的是主题、强调色和字体。现行入口是个人资料菜单或 **Settings > Pets**，自制是 **Create pet**。

## 用宠物开新对话

1. 把指针移到宠物下方的控件，选铅笔图标。
2. 输入请求，按 **Enter** 发送。用 `@` 加上下文，用 `$` 选技能。
3. 选铃铛图标，看各对话的进度。选一条对话，在 ChatGPT 里打开完整会话；选 V 形图标收起对话列表。

从这些控件开始的对话不在项目里。要用项目的上下文，回到主应用，从那个项目里开对话。

改说话：选语音图标。可用范围和控件见 [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)，站内说明见 [Codex 语音](./23-Codex语音-ChatGPT-Voice指挥任务与语音听写.md)。本文没有打通过话。

## 宠物状态

| 状态 | 含义 |
| --- | --- |
| **Running** | 有对话正在工作 |
| **Needs input** | 有对话需要你的批准、回答或其他决定 |
| **Ready** | 有对话已经完成，并且有未读活动 |
| **Blocked** | 有对话失败，或遇到系统错误 |

不止一个对话有活动时，宠物按这个顺序优先：需要输入，然后是阻塞，然后是就绪，然后是正在跑。选铃铛看对话列表，再选一条打开。V 形图标收起列表。

这个活动托盘和系统通知不是同一处。通知怎么开，见桌面端任务工作流里的通知一节。

终端宠物使用同样的四个状态名，但只针对当前 CLI 会话，没有桌面端这种多对话托盘。

## Appshot 和 Computer Use

macOS 上，在使用某个应用时同时按两侧 **Command** 键，会拍一张 [Appshot](https://learn.chatgpt.com/docs/appshots)。宠物可见、而且主 ChatGPT 窗口在后台时，这张图会发给宠物并新开一个对话。选了 **Mini** 也同样。用这个快捷键之前，把设置里的 **Appshot destination** 设为 **Automatic**，并在主应用里授权 Appshots 权限。站内步骤见 [Codex Appshots](./18-Codex-Appshots-把当前应用窗口发给对话.md)。

Windows 上，Appshots 在主 ChatGPT 应用里打开，文档没有写它会发给宠物。

macOS 上，[Computer Use](https://learn.chatgpt.com/docs/computer-use) 的画中画窗口可以附在宠物上。移动宠物，窗口跟着走。宠物如果是隐藏的，把画中画发给它会自动把宠物显示出来。

## 自制宠物

桌面端的现行步骤是：

1. 打开 **Settings > Pets**，选 **Create pet**。
2. 应用安装自带的 `hatch-pet` 技能，重新加载技能，并打开一个新对话。
3. 描述你要的宠物，发送提示。
4. 任务结束后回到 **Settings > Pets**，选 **Refresh**，再选中新宠物。

桌面端创建的自定义宠物存在这台电脑上，不会自动同步到 ChatGPT 网页。

本文没有打开桌面应用，没有安装 `hatch-pet`，也没有读到当前技能正文里的帧表。下面这段是旧文留下的提示词示例，不是这次发送过的内容。参考图只负责外观。发送前把名称和要保留的特征改成你的：

```text
请使用 hatch-pet Skill，以我上传的图片为角色参考，制作一只可在 Codex 桌面应用中使用的自定义宠物。

宠物名称为小橘。
保留参考图中的脸型、配色和红色围巾，使用清晰的像素风。
所有状态保持同一个角色，最终背景必须透明。
完成后检查精灵图尺寸、动作连贯性和边缘残留，并告诉我安装路径和启用方法。
```

参考图最好只有一个主体，轮廓清楚，完整身体没有被裁掉。复杂背景、密集文字和水印会让角色更容易走样。真人肖像、公司标志和受版权保护的角色，先确认你有没有上传和使用的权利。这些是旧文的筛选建议，不是 Pets 页上的字段。

旧文记录的动作包括待机、左右移动、招手、跳跃、失败、等待、运行和审查，并要求看四件事：不同动作里的脸、比例、配色和配件是否一致；左右移动方向是否正确、身体有没有被格子裁掉；等待、运行和审查能不能对上 Codex 的状态；透明背景有没有白边、色边、阴影或零散像素。具体动作名和帧数以你机器上当前 `hatch-pet` 的说明为准，不要把这份旧清单当成固定接口。官方现在用来表示对话进度的状态名是 Running、Needs input、Ready、Blocked，和这份动作清单不是同一张表。

旧文记录的精灵图是八列九行，每格 192 × 208 像素，整张 1536 × 1872 像素。这次没有重新生成，不能把八列九行写成当前技能的输出合同。不要在图像软件里拉伸最终文件，也不要把没用到的透明格填上背景色。

## 网页上传和终端要求

网页上选 **Upload pet** 添加自定义精灵图。文件必须是透明 PNG 或 WebP，恰好 1536 × 1872 像素，不超过 20 MiB。同一处设置里可以编辑、下载、刷新或删除已上传的宠物。整张图的像素和旧文记录的 1536 × 1872 一致；网页文档没有再写「八列九行」或「每格 192 × 208」。

终端宠物：

- 输入 `/pets` 或 `/pet` 打开选择器。
- 输入 `/pets <name>` 直接选一只。
- 输入 `/pets off` 关闭终端宠物。

选择器包含内置宠物，以及这台电脑上已安装、并且兼容的自定义宠物。需要 iTerm2 3.6 或更高版本，或者支持 Kitty graphics 或 Sixel 的终端。tmux 和 Zellij 里不可用。本文的环境不是 iTerm2，没有打开选择器。

## 常见问题

**设置里找不到 Pets。** 先更新桌面应用，并看工作区是否允许。官方写的是个人资料菜单和 Settings > Pets，不是外观页里的一个开关。

**新技能没有出现。** 官方步骤是应用自己安装 `hatch-pet`、重新加载技能并打开新对话。本文没有看到失败时的报错文案，不编一条「必须重启」的步骤。

**网页上看不到桌面端刚做的宠物。** 这是文档写明的：桌面端自定义宠物存在本机，不自动同步。网页要按上面的规格另行上传。

**Linux 桌面端有没有悬浮宠物？** Pets 页把悬浮宠物写在 macOS 和 Windows 的 ChatGPT 桌面应用上。没有写 Linux 的悬浮层。本文不补。

## 参考资料

- [Pets](https://learn.chatgpt.com/docs/pets)
- [Settings 的 Pets 一节](https://developers.openai.com/codex/app/settings)
- [Appshots](https://learn.chatgpt.com/docs/appshots)
- [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)
- [Computer Use](https://learn.chatgpt.com/docs/computer-use)
