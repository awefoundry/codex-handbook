# Windows 安装 Codex App：从下载到确认可用

> 这篇教程介绍如何在 Windows 上安装 ChatGPT 桌面应用，并使用其中的 Codex。目前，Codex 已经集成到 ChatGPT 桌面应用中，没有单独的 Windows 安装包。

## 完成后你可以

完成这篇教程后，你可以：

- 找到官方提供的 Windows 安装入口；
- 安装并启动 ChatGPT Windows 桌面应用。


## 安装前准备

你只需要一台能够正常联网的 Windows 电脑。


## 第一步：打开官方 Windows 下载入口

在浏览器中打开 [ChatGPT Windows 下载页](https://chatgpt.com/zh-Hans-CN/download)。先核对地址栏中的域名，确认进入的是 ChatGPT 官方网站，再点击 **Windows** 下载按钮。

![ChatGPT 官方下载页面中的 Windows 下载入口](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/01-官方下载入口.png)

图 1：官方下载页同时提供 macOS 和 Windows 入口。本文介绍 Windows 版的安装过程。

点击 Windows 后，按页面提示进入安装流程。页面文案可能随版本变化，下载入口应来自官方域名。Microsoft Store 能正常使用时，不必从第三方网站下载安装包。

## 第二步：安装 ChatGPT Windows 应用

### 推荐路线：通过 Microsoft Store 安装

官方 Windows 下载入口通常会跳转到 Microsoft Store。打开商店页面后，先确认应用名称为 **ChatGPT**、发布者为 **OpenAI**，再点击安装。
![alt text](image-1.png)


![Microsoft Store 中的 ChatGPT 应用页面](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/02-Microsoft-Store应用页.png)

图 2：Microsoft Store 已打开 ChatGPT 应用页面。如遇报错，可参考下文的处理方法。

看到“已安装最新版本”和“打开”按钮后，就说明安装完成。

![Microsoft Store 显示 ChatGPT 已安装](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/03-应用安装完成.png)

图 3：安装完成后，点击“打开”即可启动应用。



## Microsoft Store 打不开怎么办

安装时，Microsoft Store 可能出现白屏、初始化失败，或一直停留在“获取”“正在安装”状态。常见原因是 Store 客户端异常或网络连接不稳定。

按下面的顺序处理：

1. 点击 Store 页面上的“刷新页面”，等待几十秒；
2. 关闭 Microsoft Store，再重新打开；
3. 切换网络或代理节点，或临时关闭代理，然后重新打开官方下载页；
4. 按 `Win + I` 打开“设置”，依次进入“时间和语言”>“语言和区域”>“国家或地区”，将“中国”临时改为其他可用地区。关闭并重新打开 Microsoft Store，再尝试搜索并下载应用；
5. 如果仍然失败，可尝试下文的离线安装方法。

![Microsoft Store 初始化或安装失败提示](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/12-真实安装报错.png)

图 4：Microsoft Store 常见的初始化失败提示。

如果 Store 客户端始终无法使用，也可以通过第三方页面解析 Microsoft Store 安装包，手动下载后离线安装。步骤如下：

手动下载安装离线包：
![alt text](../图片素材/01-安装与首次使用/03-Windows安装Codex-App/04-离线安装包下载.png)
1. 打开浏览器，访问 `store.rg-adguard.net`。
2. 在左侧下拉框中选择产品 ID（ProductId），在输入框中粘贴 Codex 的产品 ID `9PLM9XGG6VKS`，然后点击搜索。
3. 页面会列出多个下载链接。找到扩展名为 `.msix`、文件名中包含 `x64` 的版本。大多数 Windows 电脑使用 x64；ARM 设备请按对应架构选择。
4. 点击下载。如果浏览器提示文件存在风险，请先确认来源和文件名无误，再选择“保留”。
5. 下载完成后，双击 `.msix` 文件，按提示完成安装。

安装完成后，继续进行首次启动。

## 第三步：首次启动应用

安装完成后，双击 ChatGPT 应用图标，进入登录界面。
![alt text](image.png)

## 下一步

- [登录 Codex](./07-登录Codex.md)
- [打开第一个本地项目](./08-打开第一个本地项目.md)
