# 登录 Codex：选择账号、完成授权并确认状态

## 这篇文章适合谁

你已经安装了 Codex App、CLI 或编辑器扩展，下一步就是登录。本文会分别介绍这三种入口，并说明 API Key、浏览器授权、Cloud 和退出登录有什么区别。

## 先说结论

第一次在本地使用 Codex，通常直接用 ChatGPT 登录最省事：点击登录按钮后，浏览器会完成授权，再回到 App、CLI 或 IDE。需要按调用量计费、在脚本或自动化环境中运行时，再考虑 API Key。Codex Cloud 必须使用 ChatGPT 登录，不能用 API Key 代替。

登录前，准备好一个可用账号即可。不要把邮箱、验证码、API Key 或 `auth.json` 放进截图、仓库或任务提示中。

## ChatGPT 登录和 API Key 怎么选

OpenAI 的 Authentication 文档列出了两种本地登录方式：使用 ChatGPT 登录时，沿用订阅或工作区权益；使用 API Key 登录时，按 API 用量计费。ChatGPT 桌面应用、Codex CLI 和 IDE 扩展都支持这两种方式，但 Cloud 只能使用 ChatGPT 登录。

![OpenAI Authentication 页面中的登录方式说明](../图片素材/00-从这里开始/06-第一次使用前要准备什么/01-官方Authentication登录方式.png)

图 1：官方 Authentication 页面。来源：[OpenAI Authentication](https://learn.chatgpt.com/docs/auth)。

| 你的情况 | 建议 |
| --- | --- |
| 第一次使用 Codex，已经有 ChatGPT 账号 | 先用 ChatGPT 登录 |
| 想使用 Codex Cloud | 必须用 ChatGPT 登录，并确认账号或工作区已开通 Cloud |
| 在脚本、CI 或可信的自动化环境中按量调用 | 评估 API Key 或组织提供的 Access Token |
| 只是想完成一次本地任务 | 不要为了开始而单独创建 API Key |

API Key 和 ChatGPT 订阅采用不同的计费与权限体系。API Key 需要在 OpenAI Platform 中管理；一旦泄露，应立即撤销并重新生成。账号、额度和功能可能随版本及工作区策略变化。如果实际情况与本文不同，以官方页面和当前客户端的提示为准。

## App：从登录按钮到返回应用

### 1. 打开登录入口

启动 ChatGPT 桌面应用。未登录时会先看到登录页。英文界面的按钮通常写作 **Continue to sign in** 或 **Sign in another way**，中文界面可能略有不同。

![ChatGPT Windows 应用的登录入口](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/05-登录入口.png)

图 2：Windows App 的登录入口。图片可与《Windows 安装 Codex App》复用。

如果需要切换语言或账号，不要连续点击登录按钮。先确认浏览器没有被弹窗拦截，再继续下一步。

### 2. 用 ChatGPT 账号登录

点击 **Continue to sign in**（中文界面为“继续登录”）。应用会打开浏览器，按页面提示完成 ChatGPT 登录和授权。登录方式可能包括邮箱、Google、Microsoft 或 Apple，实际选项以页面显示为准。

![ChatGPT Windows 应用的中文登录界面](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/07-登录界面-中文.png)

图 3：中文登录界面。截图没有包含邮箱或验证码，可以继续复用。

浏览器打开后会进入 ChatGPT 的网页登录页。页面上的登录方式可能随地区、账号和版本变化；只在官方 `chatgpt.com` 域名中输入账号信息。

![ChatGPT 官方网页登录入口](../图片素材/01-安装与首次使用/07-登录Codex/01-ChatGPT网页登录入口-官方.png)

图 4：官方 ChatGPT 网页登录入口。截图来自 [chatgpt.com/auth/login?locale=zh-CN](https://chatgpt.com/auth/login?locale=zh-CN)，画面未包含个人账号信息；这里只用于说明浏览器授权的起点，不代表已经完成登录。

授权完成后，回到刚才的应用窗口。如果浏览器没有自动切回，就手动打开 App，等待页面刷新。授权尚未完成时，不要关闭浏览器或应用。

> 待补截图：浏览器授权完成后的回调页，以及 App 返回后的已登录状态。截图需要隐藏邮箱、头像、工作区名称和通知内容。

### 3. 确认 App 已经登录

看到下面这些状态，说明 App 已经登录：

- 应用不再停留在登录页；
- 账号菜单能显示当前账号或工作区（只核对，不要公开账号信息）；
- 可以进入 Codex 入口，而不是只停留在普通 ChatGPT 页面。

> 待验证：不同版本的 Windows App 可能把账号菜单放在左下角、右上角或设置页。发布前请在当前版本补充准确位置和一张脱敏后的成功状态图。

## CLI：浏览器登录、设备码和 API Key

### 1. 用 ChatGPT 登录

在 PowerShell、Terminal 或 WSL 中进入项目目录，然后启动 Codex：

```powershell
codex
```

第一次启动时，选择 **Continue to sign in**，浏览器会接管登录。也可以先运行：

```text
codex login
```

没有图形界面的机器，如果当前版本支持设备码登录，可以使用：

```text
codex login --device-auth
```

设备码只在当前登录流程中使用，不要把它写进脚本或截图。命令名称和可用选项以 `codex login --help` 为准。

### 2. 用 API Key 登录

不要把 Key 直接写在命令行参数、Shell 历史或文章里。先把 Key 放进当前会话的环境变量，再通过标准输入交给 Codex。

PowerShell：

```powershell
$env:OPENAI_API_KEY | codex login --with-api-key
```

macOS、Linux 或 WSL：

```bash
printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key
```

如果使用组织提供的访问令牌，当前版本也可能支持：

```bash
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
```

本机 CLI 的帮助中列出了这个选项，其他客户端不一定有相同入口。命令执行后，不要把终端历史、环境变量值或认证文件提交到 Git。

### 3. 检查登录状态

CLI 可以直接报告当前认证状态：

```text
codex login status
```

再运行一次 `codex`，发送一条只读请求，例如“请读取当前目录的 README，不要修改文件”，确认登录、项目路径和权限都正常。

> 待补截图：一张裁掉桌面背景、只保留终端的成功证据，至少包含 `codex login status` 的结果和一次只读请求。现有 `03-login-and-project-check.png` 显示的是 PowerShell 启动错误，不作为成功截图。

## IDE：登录入口和返回编辑器

VS Code、Cursor 等兼容编辑器会在 Codex 侧栏中提供登录按钮。打开侧栏，选择 **Continue with ChatGPT** 或类似按钮；浏览器授权完成后，再回到原来的编辑器窗口。

![VS Code 中的 Codex 登录界面](image-10.png)

图 5：VS Code 扩展中的登录界面。图片来自相邻的《VS Code 和兼容编辑器安装 Codex》文章，可复用；按钮文字可能随扩展版本变化。

![VS Code 中的 API Key 登录界面](image-21.png)

图 6：VS Code 扩展中的 API Key 登录界面。

如果浏览器没有自动返回，就手动切回编辑器，再次打开 Codex 侧栏。登录成功后，侧栏不会继续要求登录，账号菜单可以正常打开，当前项目也能添加为上下文。

![VS Code 中登录成功后的对话界面](image-22.png)

图 7：VS Code 扩展登录成功后的对话界面。

> 待补截图：IDE 登录成功后的侧栏和账号菜单。请使用没有邮箱、项目私有路径和客户数据的测试窗口。

## 切换账号和退出登录

切换账号前，先确认当前使用的是哪个客户端、哪种登录方式。App 和 IDE 的账号菜单通常都有退出入口，但菜单名称和位置可能随版本变化。退出后重新选择目标账号即可。不要通过删除配置目录来“强制切换”，这样会连同其他本地设置一起清掉。

CLI 可以使用：

```text
codex logout
codex login
```

退出后用 `codex login status` 确认状态，再进行下一次登录。若多个终端同时使用不同账号，先分别退出，避免把一个终端的认证状态误认为另一个终端的状态。

> 待验证：App 和 IDE 的账号切换按钮位置，以及同一账号在多个本地入口之间是否立即同步。发布前按当前版本各补一张脱敏截图即可，不需要重复截完整登录流程。

## 凭据存储和安全边界

本地登录信息可能保存在操作系统的凭据存储中，也可能写入 `~/.codex/auth.json`。请像保管密码一样保管这些文件：

- 不提交到 Git，不上传到 Issue、网盘或聊天记录；
- 截图前遮住邮箱、头像、工作区、令牌和本地用户名；
- 怀疑泄露 API Key 时，立即到 OpenAI Platform 撤销并重新生成；
- 共享电脑完成任务后退出登录，并检查浏览器是否仍保留账号会话。

第一次使用时，建议从 **Ask for approval** 开始。登录成功并不代表 Codex 可以访问所有文件；项目目录、网络和命令权限仍由当前 App、CLI 或 IDE 的权限设置决定。

## 登录失败时怎么排查

先确认登录卡在哪一步，再收集排查所需的信息：

| 现象 | 先检查什么 |
| --- | --- |
| 点击登录没有浏览器 | 默认浏览器、弹窗拦截、网络和代理 |
| 浏览器登录成功，客户端仍未登录 | 回到原来的 App/IDE 窗口，重新打开登录面板；必要时重启客户端 |
| CLI 找不到登录状态 | 在同一套环境中运行 `codex login status`；Windows 和 WSL 的认证状态彼此独立 |
| API Key 登录失败 | 环境变量是否存在、Key 是否有效、组织和计费是否允许调用 |
| Cloud 无法使用 | 确认使用的是 ChatGPT 登录，而不是 API Key；再检查账号、工作区和 MFA 要求 |

不要反复重试并把错误信息截成一张模糊图片。记录客户端名称、版本、操作系统、登录方式、完整错误文字和发生时间；排查完成后再把敏感字段打码。

## 完成检查

- [ ] 我知道当前入口使用的是 ChatGPT 还是 API Key。
- [ ] 浏览器授权后，我回到了原来的 App、CLI 或 IDE。
- [ ] App 或 IDE 不再显示登录按钮，CLI 的 `codex login status` 状态正常。
- [ ] 我没有在截图、仓库或终端记录中暴露凭据。
- [ ] 如果要使用 Cloud，我确认账号使用 ChatGPT 登录并满足工作区要求。

## 下一步

- [打开第一个本地项目](./08-打开第一个本地项目.md)
- [完成第一次修改并检查结果](./09-完成第一次修改并检查结果.md)
- [安装登录常见问题](./13-安装登录常见问题.md)

## 参考资料

- [OpenAI Authentication](https://learn.chatgpt.com/docs/auth)
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli/)
- [第一次使用 Codex 前要准备什么](../00-从这里开始/06-第一次使用前要准备什么.md)
- [Windows 安装 Codex App](./03-Windows安装Codex-App.md)
- [Windows 和 WSL 安装 Codex CLI](./05-Windows和WSL安装Codex-CLI.md)
- [VS Code 和兼容编辑器安装 Codex](./06-VS-Code和兼容编辑器安装Codex.md)

> 版本提醒：登录按钮、账号菜单、Cloud 权限和 CLI 选项可能随客户端版本、地区及工作区策略变化。发布前请用当前版本完成待补截图和待验证项目。
