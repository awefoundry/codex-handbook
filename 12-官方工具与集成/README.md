# 官方工具与集成

整理 OpenAI 官方提供、维护或明确收录的 Codex 工具和集成。

## 内容范围

- GitHub、Slack、Linear 等官方工作流。
- Notion、Figma、Sentry 等官方插件或集成。
- Codex Security 相关能力。
- 官方 Skills、插件和文档工具。
- 安装、认证、权限、适合场景和已知限制。

文章必须附官方来源，并说明适用范围和已知限制。官方未明确认定的项目不能新放入本栏目。已有的飞书一篇是第三方开源桥，正文和条目里已经标明，不把它写成 OpenAI 或飞书官方集成。

## 已上线文章

- [Codex 远程连接：用手机或另一台电脑控制 Mac / Windows，SSH 远程项目和跨设备交接](./01-Codex远程控制另一台Mac.md)
- [Codex 浏览器操作与登录态：内置浏览器、浏览器扩展和 Computer Use 怎么选](./02-Codex浏览器操作与登录态功能.md)
- [Codex 使用 Computer Use 操作桌面应用（2026-10 更新）：安装授权、Win/macOS 差异，以及高风险场景的停手规则](./03-Codex使用Computer-Use操作桌面应用.md)
- [Codex 连接 Sentry 排查线上错误：官方插件、远程 MCP 和自建 Sentry 三种接法（0.164.0 实测）](./04-Codex连接Sentry排查线上错误.md)
- [Codex 创建自定义桌宠，从参考图到动画精灵图](./05-Codex创建自定义桌宠.md)
- [Codex 定时任务（Scheduled tasks）怎么用：创建、查看结果，以及和 codex exec + cron 怎么分工](./06-Codex-Automations定时任务.md)
- [Codex 桌面端任务工作流（2026-10 更新）：在 ChatGPT 桌面应用里用项目、并行对话、审查和定时任务](./08-Codex桌面端任务工作流.md)
- [Codex CLI 安装、登录与多入口配置（2026-10 更新）：ChatGPT 登录、API Key 登录、IDE 扩展与第三方模型](./09-CodexCLI国内使用与多入口配置.md)
- [Codex 接入飞书（2026-11 更新）：用 feishu-codex-bridge 在群里派任务，安装、三档权限和后台服务](./10-Codex飞书集成实战.md)（第三方项目 feishu-codex-bridge，不是 OpenAI 或飞书官方集成；文章保留在本目录）
- [Codex 常用功能清单（2026-11）：补上 Images 2.6、本地线程内存修复，以及仍值得每天用的几项](./11-Codex常用功能清单.md)
- [Codex Cloud 云端环境配置：发布可复用环境、设置联网与网络密钥](./12-Codex-Cloud云端环境-创建发布环境-联网与密钥设置.md)
- [Codex 接入 Google Cloud Vertex AI（2026-10 更新）：0.165.0 内置 gcp provider，项目、区域、gcloud 凭证怎么配](./13-Codex接入Google-Cloud-Model-Garden.md)
- [Codex Composer Predictions 怎么用：桌面端 Tab 接受下一步提示、Settings 开关，以及为什么不占用量额度](./14-Codex-Composer-Predictions桌面端Tab提示.md)
- [Codex CLI /presets 预设与内联 /model、/permissions：0.164.0 一条命令切换模型、推理强度和权限](./15-Codex-CLI-presets预设与内联model-permissions命令.md)
- [Codex 接入 Amazon Bedrock：CLI 登录向导、Runtime 与 Mantle 怎么选，以及 API Key 和 AWS 凭证怎么配](./16-Codex接入Amazon-Bedrock-登录向导与配置.md)
- [Codex SDK 入门：用 TypeScript 或 Python 在自己的程序里启动、继续和恢复 Codex 线程](./17-Codex-SDK入门-TypeScript与Python启动继续和恢复线程.md)
- [Codex Appshots：同时按两侧 Command 或 Alt，把当前应用窗口发给对话，以及权限、发送目标和隐私边界](./18-Codex-Appshots-把当前应用窗口发给对话.md)
- [Codex Images 2.6：在 Codex 里生成 GIF、overlay 圈选编辑，全套餐可用](./19-Codex-Images-2.6-GIF生成与overlay编辑.md)
- [OpenAI 收购 Pierre：Codex 里的 Trees、Diffs 和即将并入的 Code Storage 意味着什么](./20-OpenAI收购Pierre-Codex里的Trees-Diffs与Code-Storage.md)
- [Codex 与 Dot：在 iOS 通知里回复、分享照片，并继续 Codex 任务](./21-Codex与Dot-iOS通知回复与分享继续任务.md)
- [Codex CLI 0.167.0：用 codex agents 打开命令中心，本机图片预览、跨后端会话切换与 GCP 登录](./22-Codex-CLI-0.167-agent命令中心本机图片与GCP登录.md)
- [Codex 语音怎么用：在 ChatGPT 桌面 App 用 Voice 指挥任务、语音听写与 CLI /voice](./23-Codex语音-ChatGPT-Voice指挥任务与语音听写.md)
- [Codex 与 dot 连接多台电脑：指定在哪台电脑上跑本地 Codex 任务](./24-Codex与dot-连接多台电脑-指定电脑运行本地Codex任务.md)
