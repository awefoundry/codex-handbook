---
id: codex-dot-multiple-computers
title: Codex 与 dot 连接多台电脑：指定在哪台电脑上跑本地 Codex 任务
seo_title: Codex 与 dot 连接多台电脑：授权、指定电脑与撤销
description: dot 现在可以连接多台本地电脑，并在任务里指定用哪一台跑本地 Codex 任务，比如让专用机器构建测试、笔记本继续写代码。本文按官方文档说明授权步骤、怎么指定电脑、已有任务为什么不会跟着换、Offline 与撤销的区别，以及套餐和管理员设置。
lede: 每台电脑都要在自己的 ChatGPT App 里授权一次；一个任务同一时间只用一台电脑，换电脑不会把已有任务搬过去。
url: /guides/codex-dot-multiple-computers
status: published
section: guides
category: L-tools-integrations
topic: 官方工具与集成
content_type: 教程
source_tag: 官方功能
entry_tags: [App, Cloud]
difficulty: 进阶
order: 24
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-10
date_modified: 2026-11-10
verified_on: 2026-11-10
official_ref: https://learn.chatgpt.com/docs/dots/computers-and-apps
keywords: [Codex dot, dot 连接多台电脑, 本地 Codex 任务, 指定电脑, Allow access, Revoke access]
related: [codex-remote-control-mac, cloud-environments, codex-desktop-task-workflow]
faq:
  - q: 连接了两台电脑，dot 会自动挑一台吗？
    a: 官方文档没有写自动挑选的规则。文档的说法是可以连接多台电脑，并告诉 dot 某个任务用哪一台。稳妥的做法是在请求里直接写出电脑名，再到 dot 资料页的 Activity 里打开任务，确认它在哪台电脑上运行。
  - q: 我把 dot 的电脑换成另一台，正在跑的任务会跟过去吗？
    a: 不会。官方 Tasks and memory 页写明，改变 dot 选中的电脑不会把已有任务移到那台电脑。已有任务继续用它原来的电脑或云端环境；要在另一台电脑上做，就新建任务。
  - q: 电脑显示 Offline，是不是授权被取消了？
    a: 不是。Offline 只表示这台电脑当前不可用，比如关机、断网或 ChatGPT App 没开。要真正取消访问，需要选择 Revoke access。
  - q: 给 dot 授权了电脑，它能看到我所有的 Codex 对话吗？
    a: 不能。官方文档写明，连接电脑不会让 dot 访问已有的每一段 ChatGPT 或 Codex 对话；新任务只拿到 dot 为这项工作给出的说明和上下文。
---

# Codex 与 dot 连接多台电脑：指定在哪台电脑上跑本地 Codex 任务

> 本文在线版：[codexguide.io/guides/codex-dot-multiple-computers](https://codexguide.io/guides/codex-dot-multiple-computers)

> 核对依据：OpenAI Developers 在 X 上的公告（[2026-11-09T20:01Z，北京时间 11-10 04:01](https://x.com/OpenAIDevs/status/2119883176726409645)），以及官方文档 [dots](https://learn.chatgpt.com/docs/dots)、[Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)、[Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory)、[Controls](https://learn.chatgpt.com/docs/dots/controls) 和管理员文档 [Cloud and local access](https://learn.chatgpt.com/docs/enterprise/cloud-local-access)，2026-11-10 核对。写作环境没有 ChatGPT 桌面 App，也没有可用的 dot，**本文没有截图，也没有实际连接两台电脑**；界面名称按官方英文文档写，中文界面的叫法可能不同。

dot 是 ChatGPT 里一个常驻云端的助手，有自己的云端电脑和浏览器。2026-11-09，OpenAI 宣布 dot 可以连接**多台**本地电脑，并为每个任务选择用哪一台。官方举的例子是：让一台专用机器构建和测试 App，你继续在笔记本上写代码。

## 先看结论

- **每台电脑单独授权**：在那台电脑的 ChatGPT App 里打开 dot 资料页，在 Computers 下选 Allow，再确认 Allow access。要连第二台，就到第二台电脑上重复一遍。
- **一个 thread 同一时间只用一台电脑**：几件互不相关的事，让 dot 在每台电脑上各开一个 thread。
- **换电脑不会搬走已有任务**：已有任务继续在原来的电脑或云端环境里跑。
- **电脑要在线**：电脑开着、联网、ChatGPT App 打开，dot 才能用它。Offline 不等于撤销授权，取消要选 Revoke access。
- **和 Codex 自己的连接是两回事**：给 dot 的本地电脑权限，和你把电脑连到 Codex、开启 Work Sync 是分开的，后两者都不会自动让 dot 访问你的电脑。

## 谁能用

官方 [dots 页](https://learn.chatgpt.com/docs/dots#access)写明，dot 按套餐、地区和工作区设置逐步开放（2026-11-10 核对）：

| 套餐 | 条件 |
|---|---|
| Pro 100、Pro 200、Pro 500 | 18 岁以上，且不在欧洲经济区、英国和瑞士 |
| Business Premium | 受支持的 ChatGPT 地区，视工作区资格而定 |
| Enterprise、Edu、Healthcare | 符合条件的工作区可用；有阿联酋数据或推理驻留的工作区不可用。管理员预览期由管理员按角色开启；**2026-11-18 起默认开启**，除非工作区选择退出 |

用量方面，Pro 和 Business Premium 与 dot 的对话不计入 ChatGPT 用量限制；**dot 在 Work 或 Codex 里启动或管理的任务，照常计入这些产品的用量**。也就是说，让 dot 在你的电脑上开一个本地 Codex 任务，消耗的是 Codex 的额度。

## 第一步：在每台电脑上给 dot 授权

官方 [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps#connect-your-computers) 给出的步骤：

1. 在要连接的那台电脑上，打开 ChatGPT App，进入你的 dot 资料页。
2. 在 **Computers** 下找到当前这台电脑，选择 **Allow**。
3. 看完确认内容后选择 **Allow access**。

要连接另一台电脑，到那台电脑的 ChatGPT App 里重复同样的步骤。授权是在电脑这一侧完成的，不能在笔记本上替另一台机器点 Allow。

连接后，这台电脑上的本地文件、代码和应用可以用于 dot 的工作，无论你在哪里给同一个 dot 发消息，包括手机。连接在任务之间一直保留，不用每次重新授权。

## 给任务指定电脑

官方 [dots 页](https://learn.chatgpt.com/docs/dots)的说法是：可以连接多台电脑，并告诉 dot 某个任务用哪一台。文档没有规定固定的指令格式，直接在请求里写清楚电脑和任务就行，例如：

```text
在「构建机」那台电脑上新开一个 Codex 任务：在 ~/work/my-app 里跑完整测试，失败的用例列出来，先别改代码。
```

```text
继续我在「工作笔记本」上那个修登录页的 Codex 任务，把刚才的报错修掉，改完跑一次 lint。
```

dot 能对已连接的电脑做的事，官方 [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory#assigned-work) 列成了一张表：

| 任务 | dot 能怎么处理 |
|---|---|
| 新的本地 Work 或 Codex 任务 | 在已连接的电脑上创建任务，那台电脑要在线且 ChatGPT App 开着 |
| 已有的本地 Codex 任务 | 在已连接的电脑上继续这个任务。你要说明是哪个任务、想改什么 |
| 新的云端编程任务 | 在你已经建好的 Codex cloud 环境里创建任务，你的电脑可以离线 |
| dot 自己创建的任务 | 用任务原来的电脑或云端环境查看结果、继续追问 |

几点要注意：

- **一个 thread 同一时间只用一台电脑。** 两件独立的事要并行，比如一台跑测试、一台改文档，让 dot 在两台电脑上各开一个 thread。
- **改选中的电脑不会移动已有任务。** 官方原话是 “Changing your dot's selected computer doesn't move an existing task to that computer.” 想让同一件事换到另一台机器上做，就在那台机器上新开任务，并把需要的上下文写进去。
- **新任务不会继承所有对话。** 新任务只拿到 dot 为这项工作给的说明和上下文，不会自动收到你和 dot 的全部对话。连接电脑也不会让 dot 读到这台电脑上已有的每一段 ChatGPT 或 Codex 对话。
- **本地 Codex 任务显示在那台电脑上。** 云端 thread 会出现在桌面、网页和手机 App 里；本地 Codex thread 在对应的电脑上查看。

### 在哪里看任务跑在哪台电脑

在桌面 App 里打开 dot 资料页，选 **Activity**，打开某个任务就能看进度、文件、结果和需要你输入的请求，也可以直接在任务里下指令。dot 指派出去的工作也可以在 Activity 里暂停、停止或删除（见 [Controls](https://learn.chatgpt.com/docs/dots/controls)）。

## 在线、Offline 与 Revoke access

- dot 使用某台电脑时，这台电脑要**在线并开着 ChatGPT App**。
- 资料页里显示 **Offline**，表示这台电脑当前不可用，**授权并没有取消**。电脑重新上线、打开 App 后，dot 还能用它。
- 要真正取消访问，选择 **Revoke access**。

如果网站拦截了 dot 的云端浏览器，你可以让 dot 改用已连接的电脑试一次。官方说明这可能会在那台电脑上新开一个本地任务，**云端浏览器的登录状态不会带过去**，也不保证某个本地浏览器一定受支持。

## 本地电脑、Work Sync 和 Codex cloud 怎么分

| 你想做的事 | 用什么 |
|---|---|
| 电脑关机时也继续写代码 | 先在 Codex 里建好 cloud 环境（仓库和安装配置），dot 可以在里面开云端编程任务 |
| 用本机的文件、工具、已登录的浏览器 | 把这台电脑连到 dot，dot 在这台电脑上开本地任务 |
| 让一台专用机器跑构建、测试 | 把专用机器也连到 dot，任务里写明用这台 |
| 你自己在别的设备上控制这台电脑上的 Codex | 用 Codex 自己的远程连接，见 [Codex 远程控制另一台 Mac](../12-官方工具与集成/01-Codex远程控制另一台Mac.md) |

再强调一次：给 dot 的本地电脑权限，和你把这台电脑连接到 Codex、开启 Work Sync，**是三个独立的开关**，任何一个都不会自动替你打开另外两个。

## 企业管理员：先开 Allow local computer access

Enterprise、Edu、Healthcare 工作区里，员工能不能给 dot 连接本地电脑，取决于管理员设置。官方 [Cloud and local access](https://learn.chatgpt.com/docs/enterprise/cloud-local-access) 的步骤：

1. 工作区所有者打开 **Admin Console** > **Permissions**，为目标用户开启 dots（满足上面的资格要求）。
2. 在 **Use dots** 下打开 **Allow local computer access**，看完确认弹窗后，可以先去 **Agent Security** 检查或设置策略，再确认开启。
3. 让员工把 ChatGPT 桌面 App 更新到 **26.929 或更高版本**，否则本地电脑访问不会生效。
4. 员工按上面的步骤连接电脑，再用一个本地任务测试。

文档还写了两条限制：任何云端策略开启了 `enforce_residency` 时，**Allow local computer access** 对 Work 和 dots 都不可用；使用本地访问时，对话、工具结果和任务上下文仍会经过云端协调，**不会只留在连接的电脑上**。有数据驻留或零留存要求的团队，先看完这份文档再开。

## 动手前的检查清单

- [ ] 套餐和地区在可用范围内，dot 已经创建
- [ ] 每台要用的电脑都在它自己的 ChatGPT App 里点过 Allow access
- [ ] 跑任务的电脑开着、联网、ChatGPT App 打开，不会自动睡眠
- [ ] 请求里写明了电脑名和项目路径
- [ ] 本地 Codex 任务的权限模式符合预期（见 [Codex 桌面端任务工作流](../12-官方工具与集成/08-Codex桌面端任务工作流.md)）
- [ ] 需要电脑关机也能跑的任务，已经在 Codex 里建好 cloud 环境（见 [Codex Cloud 云端环境](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)）

## 常见问题

**连接了两台电脑，dot 会自动挑一台吗？**

官方文档没有写自动挑选的规则，只说可以告诉 dot 某个任务用哪一台。请求里直接写电脑名，再到 Activity 里确认任务在哪台电脑上运行。

**我把 dot 的电脑换成另一台，正在跑的任务会跟过去吗？**

不会。已有任务继续用原来的电脑或云端环境。要在另一台电脑上做，就新建任务。

**电脑显示 Offline，是不是授权被取消了？**

不是。Offline 只表示当前不可用。要取消访问，选 Revoke access。

**给 dot 授权了电脑，它能看到我所有的 Codex 对话吗？**

不能。连接电脑不会让 dot 访问已有的每一段 ChatGPT 或 Codex 对话。

## 相关阅读

- [Codex 远程控制另一台 Mac](../12-官方工具与集成/01-Codex远程控制另一台Mac.md)
- [Codex Cloud 云端环境：创建、发布环境、联网与密钥设置](../12-官方工具与集成/12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)
- [Codex 桌面端任务工作流](../12-官方工具与集成/08-Codex桌面端任务工作流.md)
