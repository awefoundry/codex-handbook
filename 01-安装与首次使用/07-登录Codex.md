# 登录 Codex 并确认入口可用

本课只处理认证和入口可用性，不读取练习目录，也不要求你同时操作 App、CLI 和 IDE。选择你在上一课准备好的那个入口即可。

<a id="guide-heading-0"></a>
## 先确认你要用哪种登录方式

OpenAI 当前认证文档说明，本地的 ChatGPT 桌面应用、Codex CLI 和 IDE extension 都支持两种方式：

- **ChatGPT 登录**：使用 ChatGPT 订阅或工作区提供的 Codex 权限；
- **API Key 登录**：按 OpenAI Platform 的 API 用量计费。

第一次完成本地练习时，不需要为了开始单独创建 API Key。Codex Cloud 还需要 ChatGPT 登录，本课不把 Cloud 当作练习入口。

官方依据：[OpenAI Authentication](https://learn.chatgpt.com/docs/auth)。

![OpenAI Authentication 页的登录方式说明](../图片素材/00-从这里开始/06-第一次使用前要准备什么/01-官方Authentication登录方式.png)

图片为此前保存的官方资料截图，来源：[Authentication](https://learn.chatgpt.com/docs/auth)。当前规则以链接页面为准。

<a id="guide-heading-1"></a>
## App：在浏览器完成 ChatGPT 登录

1. 打开 ChatGPT 桌面应用中的 Codex 入口。
2. 在未登录页面选择 **Continue to sign in**，浏览器会打开 ChatGPT 登录流程。
3. 完成浏览器授权后回到原来的应用窗口。
4. 确认应用不再停留在登录页，并且 Codex 入口可以打开。

![此前记录的 Windows 应用中文登录界面](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/07-登录界面-中文.png)

![此前保存的 ChatGPT 官方网页登录入口](../图片素材/01-安装与首次使用/07-登录Codex/01-ChatGPT网页登录入口-官方.png)

以上为历史界面参考，不是本轮重新登录的实测截图。输入账号前确认浏览器域名为 chatgpt.com；浏览器没有自动返回时，手动切回原应用。

<a id="guide-heading-2"></a>
### 应该看到什么

- 浏览器授权已经结束；
- 桌面应用显示已登录状态；
- Codex 页面可以继续输入任务。

账号菜单和按钮位置会随版本调整，以当前界面为准。不要把登录截图当作唯一证据。

<a id="guide-heading-3"></a>
## CLI：用 `codex login` 登录

在你已经安装 Codex CLI 的终端中运行：

```bash
codex login
```

没有参数时，CLI 会打开浏览器完成 ChatGPT OAuth 登录。需要无浏览器流程时，当前 CLI 也提供设备码方式：

```bash
codex login --device-auth
```

这些命令来自当前 [Codex CLI 命令参考](https://learn.chatgpt.com/docs/developer-commands?surface=cli)。如果当前版本或工作区策略不提供某个方式，以 `codex login --help` 的实际输出为准。

登录后检查当前认证状态：

```bash
codex login status
```

<a id="guide-heading-4"></a>
### 输出

`codex login status` 在有凭据时退出码为 0，并显示当前认证模式。它只说明凭据存在，不代表已经允许读取任意项目目录；目录和命令权限在下一课再检查。

<a id="guide-heading-5"></a>
## API Key：需要时再用

如果你确实要使用按量计费的 API 工作流，当前 CLI 参考提供了从标准输入读取 Key 的方式：

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

不要把 Key 直接写进命令历史、提示词、仓库、截图或文章。没有 API Key 需求的读者跳过这一节。

<a id="guide-heading-6"></a>
## IDE extension：回到原来的编辑器

在已安装的 IDE extension 中打开 Codex 侧栏，选择 ChatGPT 登录或当前界面提供的其他方式，完成浏览器授权后切回编辑器。登录按钮变成对话输入框，才算入口可用。

IDE 的具体按钮和支持范围以[官方 IDE 说明](https://learn.chatgpt.com/docs/codex/ide)为准。登录本身不等于已经打开了练习目录。

![此前记录的 IDE 登录入口](image-10.png)

![此前记录的 IDE API Key 输入入口](image-21.png)

![此前记录的 IDE 登录后对话界面](image-22.png)

这三张图保留原文的客户端分支说明，属于历史截图；不同版本的按钮和位置可能不同，不代表本轮完成 IDE 实测。

<a id="guide-heading-7"></a>
## 登录失败时怎么排查

| 现象 | 先检查什么 |
| --- | --- |
| 没有打开浏览器 | 默认浏览器、弹窗拦截、网络和代理 |
| 浏览器成功，客户端仍未登录 | 回到原来的窗口，重新打开登录面板，必要时重启客户端 |
| CLI 仍要求登录 | 在运行 Codex 的同一终端环境检查认证；Windows 和 WSL 的认证状态彼此独立 |
| API Key 失败 | Key 是否有效、组织权限和 API 计费是否允许调用，不要把 Key 发给别人排查 |
| 能登录但不能发起任务 | 检查账号或工作区的 Codex 权限、额度及具体错误；认证不等于产品权限可用 |

仍失败时，保留客户端版本、操作系统、登录方式和脱敏的完整错误。切换账号优先使用客户端退出入口，再重新登录，不要删除整个配置目录。

<a id="guide-heading-8"></a>
## 凭据安全

Codex 可能把登录信息缓存到操作系统凭据存储或 `~/.codex/auth.json`。把它们当作密码处理：

- 不提交到 Git，不粘贴到 Issue 或聊天记录；
- 截图前遮住邮箱、令牌、本地用户名和工作区信息；
- 怀疑 API Key 泄露时，到 OpenAI Platform 撤销并重新生成。

<a id="guide-heading-9"></a>
## 完成检查

- [ ] 我选择了一个入口，没有为了完成课程重复登录所有入口。
- [ ] 浏览器授权后，我回到了原来的 App、CLI 或 IDE。
- [ ] App/IDE 不再显示登录按钮，或 `codex login status` 显示已认证。
- [ ] 我知道凭据有效和项目文件可访问是两件事。

完成后进入[第 3 课：打开练习目录](./08-打开第一个本地项目.md)。登录或权限异常时，查看[安装登录常见问题](./13-安装登录常见问题.md)。

<a id="guide-heading-10"></a>
<a id="guide-heading-11"></a>
<a id="guide-heading-12"></a>
<a id="guide-heading-13"></a>
<a id="guide-heading-14"></a>
<a id="guide-heading-15"></a>
<a id="guide-heading-16"></a>
## 参考资料

- [OpenAI Authentication](https://learn.chatgpt.com/docs/auth)
- [Codex CLI Quickstart](https://learn.chatgpt.com/docs/codex/cli)
- [Codex CLI 命令参考](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)

官方资料核对日期：2026-09-21。本机 Codex CLI 0.154.0 的 `codex login --help` 确认了上述登录参数；命令帮助检查不等于完成登录。本课核对了官方认证页和 CLI 命令参考；没有把此前一次 CLI 非交互测试扩大成 App、交互式 CLI、IDE、安装和登录均已实测。
