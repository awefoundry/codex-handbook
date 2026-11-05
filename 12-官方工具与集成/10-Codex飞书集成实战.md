---
id: codex-feishu-bridge
title: Codex 接入飞书（2026-11 更新）：用 feishu-codex-bridge 在群里派任务，安装、三档权限和后台服务
seo_title: Codex 接入飞书：feishu-codex-bridge 安装与三档权限
description: feishu-codex-bridge 是把飞书群和本机 Codex 连起来的第三方开源工具，不是 OpenAI 或飞书官方集成。本文按 0.6.14 的 README 和命令帮助更新安装、后台服务、三档权限，以及谁能给机器人发消息。
url: /guides/codex-feishu-ji-cheng-shi-zhan
status: published
section: guides
category: J-official-tools
topic: 官方工具与集成
content_type: 教程
source_tag: 第三方服务
entry_tags: [CLI, App]
difficulty: 进阶
order: 10
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-08-24
date_modified: 2026-11-02
verified_on: 2026-11-02
tested_cli_version: 0.166.0
official_ref: https://github.com/modelzen/feishu-codex-bridge
keywords: [Codex 飞书, Codex 接入飞书, feishu-codex-bridge, 飞书机器人 Codex, Codex 群聊派任务]
related: [permissions-sandbox-approvals, codex-goal-mode-long-running-work, codex-remote-control-mac]
howto: true
faq:
  - q: 这是 OpenAI 或飞书的官方集成吗？
    a: 不是。feishu-codex-bridge 是 modelzen 维护的开源项目，MIT 许可。OpenAI 的远程连接是另一条官方路径，见本站的远程连接文章。
  - q: Linux 上能选「项目内只读」或「项目内读写」吗？
    a: README 写明这两档只在 macOS 和原生 Windows 上由操作系统沙箱强制。Linux 和 WSL 上选择这两档会拒绝启动，不会悄悄降成完全访问。本文在 Linux 上没有启动过后台服务，这条以 README 为准。
  - q: 后台服务可以用 npx 临时跑起来吗？
    a: README 写明不可以。后台服务里写死了 CLI 路径，npx 的临时缓存被清掉之后服务会找不到命令。常驻服务要先 npm i -g。前台的 run 才可以用 npx 跑一次。
---

# Codex 接入飞书（2026-11 更新）：用 feishu-codex-bridge 在群里派任务，安装、三档权限和后台服务

> 本文在线版：[codexguide.io/guides/codex-feishu-ji-cheng-shi-zhan](https://codexguide.io/guides/codex-feishu-ji-cheng-shi-zhan)

> 核对依据：第三方仓库 [modelzen/feishu-codex-bridge](https://github.com/modelzen/feishu-codex-bridge) 的 README 和 LICENSE（MIT），npm 上的 `@modelzen/feishu-codex-bridge@0.6.14`，以及 2026-11-02 在 Linux 上对这个版本执行的 `--help`、`web --help`、`doctor`。没有启动 `web` 或 `start`，避免在测试机上注册系统服务或打开控制台，所以没有飞书界面截图。旧文四张配图是概念示意图，图注都叫「操作步骤」，和真实界面不一致，本次全部移除。`date_published` 使用本仓库首次收入该文的提交日期 2026-08-24。

feishu-codex-bridge 把飞书（或 Lark）群和你电脑上的 Codex 连起来：群里发一句话，本机 Codex 在这个群绑定的目录里干活，过程以卡片回到群里。它是开源的第三方桥，不是 OpenAI 推出的飞书集成，也不是飞书官方的 Codex 机器人。项目 README 文首另有一条给 Mac 用户的产品推荐（项目方推广信息）。本文只写这个桥本身。

2026-11-02 的 GitHub API 数据：95 星，25 个 fork，MIT，默认分支最近一次推送是 2026-10-26 21:43（北京时间）。npm `latest` 是 0.6.14，发布于 2026-09-24 22:12（北京时间），`engines.node` 为 `>=20.0.0`。

想用手机继续指挥**已经配对的那台电脑**上的 Codex，官方路径是远程连接，见 [Codex 远程连接](./01-Codex远程控制另一台Mac.md)。那条不经过飞书，也不使用这个桥。

## 它是什么

README 的对应关系是：

- 一个项目等于一个群，等于一个固定的本地目录。
- 一个话题（thread）等于一条会话（session）。

桥不自己跑模型。它把飞书消息交给本机的 Codex app-server，或交给 Claude Code 的 Agent SDK，再把输出转成飞书里的流式 Markdown 卡片。建项目时选后端。README 写 Codex 一侧包括 goal、steer、compact、resume，以及只读档使用的沙箱；Claude Code 复用本机登录，能力更少。同一台机器可以混用两种后端。

机器人跑 agent 时，README 写的审批策略固定是 `approvalPolicy: never`，没有逐条人工批准。沙箱是唯一的闸门。这个前提放在安装之前：任何能给机器人发消息的人，都在用你这台电脑的身份做事，能做多少取决于下面的三档权限。

## 工作原理

主方向是飞书群到本机 agent。

1. 在私聊或网页控制台里新建项目，绑定一个本地目录，选择 Codex 或 Claude。
2. 机器人建群、置顶命令说明，并把你拉进群。
3. 群里 @ 机器人（话题和单会话群里可以不 @），本机 Codex 在那个目录里执行。
4. 卡片按时间显示思考摘要、进度和工具。卡片上可以终止当前这一轮。

反方向是 README 里的「咖啡一下」：你人在电脑前用 Codex 或 Claude Code，离开时把它「需要审批、需要提问、任务完成」推到飞书私聊。你在手机上点确认或回答，本机继续跑；README 写机器保持不睡，回到电脑后终端交还。本文没有打开过这个开关，也没有飞书私聊截图。

官方的 Codex Goal 是对话里的 `/goal`，完成标准怎么写见 [Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md)。这个桥在群里也提供 `/goal <目标>`，README 的含义是让本机 agent 多轮做到完成。群里的斜杠命令会按后端裁剪，和桌面端里的 `/goal` 是否逐项相同，以你装上的桥和 Codex 版本为准。

## 安装

README 的安装提示写 Node.js ≥ 18。npm 上 0.6.14 的 `engines` 是 `>=20.0.0`。以包声明为准。还需要本机已经能运行 `codex`。2026-11-02 核对时，测试机的 Node 是 v22.23.4，Codex CLI 是 0.166.0。

```bash
npm i -g @modelzen/feishu-codex-bridge
feishu-codex-bridge web
```

第二条打开本机网页控制台。0.6.14 的 `web --help` 写明：只做只读预览的说明是「仅 127.0.0.1 + token」，写操作随 daemon 一起开放；`--port` 的默认值是 51847。README 补充：每次启动使用随机 token，daemon 在跑时控制台可写，没跑时是只读预览，仍可以一键启动 daemon。加好机器人并启动后台之后，这条前台命令可以用 Ctrl+C 结束，后台不受影响。

本文执行了 `web --help`，没有执行 `web`，所以没有看到那个带 token 的地址，也不把端口写成「已经在本机监听」。

0.6.14 的 `feishu-codex-bridge --version` 输出 `0.6.14`。顶层命令和 README 的 CLI 一览一致：`run`、`start`、`stop`、`restart`、`status`、`logs`、`update`、`web`、`bot`、`doctor`。

## 创建机器人和项目群

`bot --help` 的子命令：

```text
init [name]     扫码注册一个飞书机器人并授权（可选短名）
list            列出已注册的飞书机器人
use [names...]  勾选/指定要同时连接的机器人（多选）；无参数弹交互式勾选框
rm <name>       移除一个机器人配置
```

`run --help` 有 `--bot <name>`，只启动指定的一个机器人（名字或 appId）。没有配置时，`run` 会先走扫码 init。本文没有飞书应用，没有扫码。

项目建好之后，README 让你按场景选群：

- **多话题群。** @ 机器人开话题，每个话题是一条独立会话，上下文分开，可以并行。
- **单会话群。** 整个群是一条连续会话，不用每次 @。

README 还写了这些群内能力：图片和文件附件会交给 agent；回答里的本地文件可以变成飞书里的交互文字，点击后由桥把原文件发回当前会话（每轮最多 10 处，单文件不超过 30 MB，并检查身份、项目权限和文件是否变化）；文档评论里 @ 机器人，可以把答复写回同一条评论。这些都来自 README，本文没有在飞书里点过。

## 日常怎么用

群里的基本动作是 @ 机器人并写清目录里要完成的事，看卡片，需要时点终止。`/goal <目标>` 用来多轮执行。卡片上 README 写了两种停法：终止是立刻停，结束目标是本轮跑完再停。斜杠命令包括 `/model`、`/resume`、`/compact`、`/context`，Claude 后端不显示它不支持的项。

私聊里的菜单包括新建项目、设置、用量、诊断、重连。用量数据 README 写明来自 Codex 个人资料页，需要 ChatGPT 登录。本文的 Codex 没有登录，没有看到用量数字。

## 后台服务

```bash
feishu-codex-bridge start
feishu-codex-bridge status
feishu-codex-bridge logs
feishu-codex-bridge logs -f
feishu-codex-bridge restart
feishu-codex-bridge stop
feishu-codex-bridge update
feishu-codex-bridge update --check
```

README 对这些命令的定义是：`start` 安装系统服务、开机或登录自启、崩溃拉起；`status`、`logs`、`restart`、`stop` 管理这个 daemon；`update` 用 `npm i -g` 更新并重启，`--check` 只检查。0.6.14 在 Linux 上的 `start --help` 文案写的是「装 launchd 开机自启」。launchd 是 macOS 的服务管理器。README 则写 macOS、Windows、Linux / WSL 都可以注册后台服务。两处字面不完全一样。本文没有执行 `start`，因此不把 Linux 上的服务安装写成已经成功。以你本机的 `start --help` 和 README 为准，先在不需要自启的情况下用前台 `run` 确认机器人可用。

两条约束来自 README：

- 后台服务必须全局安装。不要用 npx 当常驻进程，服务里写死了 CLI 路径，npx 缓存清理后会找不到命令。前台 `run` 用 npx 跑一次是 README 允许的。
- 要指定 Codex 二进制文件时，在 `start` 时设置 `CODEX_BIN`。服务会保存这个路径，重启后继续用。已经装好的服务要按项目文档重新生成配置。本文没有设置 `CODEX_BIN`，也没有读它的配置文档以外的行为。

本地状态在 `~/.feishu-codex-bridge/`：机器人配置、项目和会话注册表、用 AES-256-GCM 加密的密钥库。卸载时删掉这个目录。新建项目如果留空路径，默认目录是 `~/.feishu-codex-bridge/projects/<项目名>`。要改默认根目录，README 让你编辑当前机器人的 `config.json` 里的 `preferences.projectsRootDir`。这项只影响之后留空创建的项目。

## 三档权限

每个项目单独选择，README 的表是：

| 档位 | 能碰到的范围 | README 写的场景 |
|---|---|---|
| 项目内只读 | 只能读项目目录，不能写 | 外部群、不完全信任的问答 |
| 项目内读写 | 只在项目目录里读写 | 自己的编码项目 |
| 完全访问 | 整台电脑 | 只有你自己掌控、并且完全信任的机器 |

只读和读写靠操作系统沙箱强制，README 写明只有 macOS 和原生 Windows 做得到。在 Linux 或 WSL 上选择这两档，会拒绝启动，不会静默变成完全访问。要在 Linux 上限制目录，README 的建议是把后端放进容器或隔离环境。本文的系统是 Linux，没有启动桥，所以没有看到这条拒绝信息，上面这段是 README 的原文范围。

完全访问的含义，README 写得很直接：任何能给这个机器人发消息的人，都能以你的身份在这台电脑上执行任意命令。只拉你信任的人进群，目录里不要放密钥和私人数据。

沙箱和审批在 Codex 自己的会话里怎么配，见 [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)。桥把审批固定成不再询问之后，你在 Codex 配置里习惯的「每次都问」不会出现在群聊这条路径上。收紧手段是项目档位，加上群成员名单。

它不是多租户托管服务。README 写明这是给自己和信任的小团队用的桥。

## 安全注意事项

把上面几条合成使用前的检查：

1. 确认机器人所在的群里没有你不认识的人，也没有过宽的群可见范围。
2. 在 macOS 或原生 Windows 上，编码项目用「项目内读写」。问答用「项目内只读」。
3. 在 Linux 或 WSL 上，不要指望只读和读写这两档会启动。需要隔离时用容器，而不是改选完全访问来「先跑起来」。
4. 完全访问只放在没有私人数据、只有你能发消息的机器上。
5. `~/.feishu-codex-bridge/` 里有密钥库。备份或拷贝家目录时把它当成凭据。

「咖啡一下」会把本机正在等待的审批推到飞书私聊。私聊对象如果不是你预期的那个账号，就等于把批准权交了出去。本文没有启用它，启用前先在飞书里确认私聊对象。

## 排障

`doctor` 是本地自检。0.6.14 的帮助写的是检查 codex、登录、lark-cli 和当前机器人配置。在一台装了 Codex CLI 0.166.0、但没有登录、也没有初始化桥的 Linux 上，真实输出是：

```text
🩺 feishu-codex-bridge 自检

  ✅ codex CLI    codex-cli 0.166.0 (/tmp/codex-cli/node_modules/.bin/codex)
  ❌ codex 登录     未登录，运行 `codex login`
  ❌ lark-cli     未找到（onboarding 会装到私有目录）
  ❌ bridge 配置    未配置，运行 `feishu-codex-bridge run`（或 `bot init`）扫码创建

3 项需处理
```

路径 `/tmp/codex-cli/...` 是这次测试的临时安装位置，不是推荐的安装目录。Codex 不在 `PATH` 里时，第一项会变成未找到，并提示设置 `CODEX_BIN` 或安装 Codex。登录、lark-cli 和桥配置三项失败，是因为这台机器没有做飞书初始化，不是 0.6.14 的异常崩溃。

继续排查时：

- `feishu-codex-bridge status` 看 daemon 是否在跑。本文没有安装 daemon，没有 status 输出。
- `feishu-codex-bridge logs` 看后台日志。`-f` 持续跟随。
- 控制台打不开时，确认地址是 `127.0.0.1`，端口是你传给 `--port` 的值或默认 51847，并且使用这次启动打印的 token。本文没有拿到这个链接。
- 群里没有回复时，先看机器人是不是 `bot use` 选中的那一个，项目是不是绑到了你以为的目录。

## 常见问题

**Node 18 够不够？** README 的安装提示写 ≥ 18。0.6.14 的 `engines` 要求 `>=20.0.0`。按包的 engines 安装 Node，再安装桥。

**`start --help` 为什么在 Linux 上提到 launchd？** 0.6.14 的帮助文本就是这样写的。README 说 Linux / WSL 也可以注册服务。本文没有执行 `start`，不判断 Linux 上最终调用的是哪一种服务管理器。

**能把公司飞书租户里的所有人一起拉进来吗？** README 反对这种用法。完全访问时，能发消息的人就是能在你电脑上执行命令的人。只读档也只适合你愿意让他们读那个项目目录的人。

**和官方手机远程是什么关系？** 官方远程连接让另一台已配对设备继续使用这台电脑上的 Codex，不经过飞书。这个桥把入口换成飞书群，并固定不再逐条审批。两套不要当成同一个开关。

## 参考资料

- 仓库与许可证：[modelzen/feishu-codex-bridge](https://github.com/modelzen/feishu-codex-bridge)（MIT，2026-11-02 查询的 README 与 0.6.14 命令帮助）
- npm：`@modelzen/feishu-codex-bridge@0.6.14`
- 权限背景：[Codex 权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)
- 群里的 `/goal` 和 Codex 自己的 Goal：[Codex Goal 模式](../11-自动化与高级工作流/08-Codex使用Goal模式运行长任务.md)
- 不经过飞书的官方远程用法：[Codex 远程连接](./01-Codex远程控制另一台Mac.md)
