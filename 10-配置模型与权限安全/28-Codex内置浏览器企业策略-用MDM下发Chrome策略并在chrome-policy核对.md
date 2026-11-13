---
id: codex-desktop-browser-policies
title: Codex 内置浏览器企业策略：用 MDM 下发 Chrome 策略，Windows、macOS、Linux 三种位置与 chrome://policy 核对
seo_title: Codex 内置浏览器企业策略：MDM 下发 Chrome 策略与 chrome://policy 核对
description: ChatGPT 桌面端（含 Codex）的内置浏览器支持 244 项 Chrome 企业策略，只能按设备下发。本文讲清 Windows 注册表、macOS com.openai.codex、Linux 策略目录三种位置，Intune、Jamf、Ansible 示例和 chrome://policy 核对。
lede: 策略内容和 Chrome 完全一样，变的只是放的位置。写到 Chrome 的位置，桌面端读不到。
url: /guides/codex-desktop-browser-policies
status: published
section: guides
category: F-config-model-security
topic: 配置、模型与权限
content_type: 教程
source_tag: 官方功能
entry_tags: [App]
difficulty: 进阶
order: 28
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-11-13
date_modified: 2026-11-13
verified_on: 2026-11-13
official_ref: https://learn.chatgpt.com/docs/enterprise/desktop-browser-policies
keywords: [Codex 内置浏览器策略, ChatGPT 桌面端 MDM, Chrome 企业策略, com.openai.codex, chrome://policy, Intune, Jamf, 浏览器管控]
related: [codex-browser-login-state, codex-built-in-browser-local-file-risk, config-toml-guide]
faq:
  - q: 能用 Google Admin 云端管理这些浏览器策略吗？
    a: 不能。官方文档写明，ChatGPT 桌面端目前只支持通过 MDM、组策略或配置管理工具按设备下发，浏览器策略的云端管理还不可用。
  - q: 已经给 Chrome 下发过策略，桌面端会自动生效吗？
    a: 不会。策略内容和格式相同，但位置不同：Windows 要写到 SOFTWARE\Policies\OpenAI\Codex，macOS 要用 com.openai.codex 偏好域，Linux 要放到 /etc/opt/codex/policies/managed/。针对 Chrome 的配置文件不会作用到桌面端。
  - q: 在 macOS 上用 defaults write 写进去行不行？
    a: 不行。官方文档写明，用 defaults write 写的普通用户偏好不会让策略变成强制，要用 MDM 下发受管偏好（managed preferences）。
  - q: chrome://policy 里看到了策略，就说明生效了吗？
    a: 只能说明策略被读到了。官方建议在那个浏览器里实际测试一次预期行为，有些策略还要完全重启应用才会生效。
---

# Codex 内置浏览器企业策略：用 MDM 下发 Chrome 策略，Windows、macOS、Linux 三种位置与 chrome://policy 核对

> 本文在线版：[codexguide.io/guides/codex-desktop-browser-policies](https://codexguide.io/guides/codex-desktop-browser-policies)

> 核对依据：官方文档 [Desktop browser policies](https://learn.chatgpt.com/docs/enterprise/desktop-browser-policies) 和 [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)，2026-11-13 核对。策略名按官方英文原文写。编辑部没有受管设备和 MDM 环境，文中的脚本和配置文件没有实际下发测试，JSON 示例只做过语法检查；本文没有截图。

Codex 已经并进 ChatGPT 桌面端，桌面端里那个可以让 Codex 打开网页、点按钮、读页面的**内置浏览器**，底层是 Chromium。2026-11 官方新增了一份管理员文档：企业可以像管 Chrome 一样，给这个内置浏览器下发 Chrome 企业策略，比如关掉密码管理器、按网址拦截 Cookie、限制下载。

这篇写给要管一批 Mac、Windows 或 Linux 电脑的 IT 管理员。普通个人用户不需要做任何设置。

## 先看结论

- **能管什么**：内置浏览器支持 **244 项** Chrome 企业策略，每项的含义和取值格式去查 Google 的 [Chrome Enterprise 策略列表](https://chromeenterprise.google/policies/)。
- **怎么下发**：只支持**按设备下发**（MDM、组策略、Ansible 这类配置管理工具），不支持 Google Admin 云端管理。
- **放哪里**：策略内容和格式与 Chrome 相同，只是位置换成桌面端自己的。标识符里仍然是 `Codex` / `codex`，要照抄：

| 平台 | 位置 |
|---|---|
| Windows | 注册表 `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\OpenAI\Codex`（全设备）或 `HKEY_CURRENT_USER` 下同样路径（单个用户） |
| macOS | 受管偏好域 `com.openai.codex` |
| Linux | 强制策略放 `/etc/opt/codex/policies/managed/`，允许用户修改的推荐值放 `/etc/opt/codex/policies/recommended/` |

- **怎么核对**：在桌面端的内置浏览器里打开 `chrome://policy`，点 **Reload policies**，强制策略应显示来源 **Platform**、级别 **Mandatory**，没有报错。

## 浏览器策略和 requirements.toml 管的不是一回事

Codex 的企业管控里还有一套 `requirements.toml`，两者分工不同，容易混：

| | Chrome 浏览器策略（本文） | requirements.toml 里的浏览器相关项 |
|---|---|---|
| 管的对象 | 浏览器本身的行为：密码管理器、Cookie、下载、网址黑白名单、自动填充等 | Codex 在浏览器里能做什么：哪些网站允许 agent 访问、能否上传下载、是否允许完整 CDP 访问、能否读历史记录 |
| 典型字段 | `PasswordManagerEnabled`、`CookiesBlockedForUrls`、`URLBlocklist` | `[browser_use]`、`[browser_use.origins."https://example.com"]` |
| 整体关掉 | 不负责 | `[features]` 里 `in_app_browser = false` 关掉内置浏览器面板，`browser_use = false` 关掉浏览器操作 |
| 下发方式 | MDM、组策略、配置管理工具 | 云端 Agent security 或系统级 requirements 文件 |

要「整个禁用内置浏览器」，用 requirements.toml 的功能开关；要「浏览器可以用，但别存密码、别访问某些网站」，用本文的浏览器策略。

## 官方示例：关掉密码管理器，拦截一个网站的 Cookie

官方三个平台的示例都下发同样两条策略，方便对照：

- `PasswordManagerEnabled` = false：关掉内置浏览器的密码管理器；
- `CookiesBlockedForUrls` = `["https://example.com"]`：拦截这个网址的 Cookie。

实际部署时把它们换成你们自己的策略。

## Windows：Intune 或组策略

用 **Microsoft Intune** 时，官方给的是一段 PowerShell 脚本，加到 **Platform scripts** 里，为设备上所有用户写入强制策略：

```powershell
$ErrorActionPreference = 'Stop'
$policyRoot = 'HKLM:\SOFTWARE\Policies\OpenAI\Codex'
if (-not (Test-Path -LiteralPath $policyRoot)) {
  New-Item -Path $policyRoot -Force | Out-Null
}
New-ItemProperty -Path $policyRoot -Name PasswordManagerEnabled -PropertyType DWord -Value 0 -Force | Out-Null
$cookieKey = "$policyRoot\CookiesBlockedForUrls"
if (-not (Test-Path -LiteralPath $cookieKey)) {
  New-Item -Path $cookieKey -Force | Out-Null
}
New-ItemProperty -Path $cookieKey -Name '1' -PropertyType String -Value 'https://example.com' -Force | Out-Null
```

Intune 里要把 **Run this script using the logged on credentials** 设为 **No**，**Run script in 64-bit PowerShell host** 设为 **Yes**，先分配给试点组。脚本跑完后重启桌面端再核对。

用**组策略**时，按脚本里同样的键、值名、类型和值创建注册表首选项。注意 Chrome 自带的 ADMX 管理模板针对的是 Chrome，管桌面端要用自定义注册表设置。

注册表取值格式：

- **布尔值**：`REG_DWORD`，`0` 是 false，`1` 是 true；
- **字符串列表**：建一个以策略名命名的子键，下面放从 `1` 开始编号的 `REG_SZ` 值；更新列表时要删掉不再需要的编号；
- **结构化策略**：按 Chrome 策略文档里的 Windows 编码，例如 `ExtensionSettings` 是把字典写成 JSON 字符串存进 `REG_SZ`。

两个坑：

- 按用户下发要写 `HKEY_CURRENT_USER`，并且在目标用户的身份下运行。**以 SYSTEM 身份跑的脚本写不到当前登录用户的 `HKEY_CURRENT_USER`**。
- 支持推荐值的策略，放在根键下名为 `Recommended` 的子键里。

## macOS：Jamf 或 Intune 配置描述文件

macOS 要创建一个配置描述文件，在 `com.openai.codex` 偏好域里设置**强制的受管偏好**。官方给的 plist：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PasswordManagerEnabled</key>
  <false/>
  <key>CookiesBlockedForUrls</key>
  <array>
    <string>https://example.com</string>
  </array>
</dict>
</plist>
```

- **Jamf Pro**：先存成 `com.openai.codex.plist`，在电脑配置描述文件的 **Application & Custom Settings** 负载里上传，偏好域填 `com.openai.codex`。
- **Microsoft Intune**：建 macOS 的 **Templates → Preference file** 描述文件，**Preference domain name** 填 `com.openai.codex`。这里只保存最外层 `<dict>` 里面的键值对，去掉 XML 声明、DOCTYPE、`<plist>` 和最外层 `<dict>`，里面嵌套的 `<array>` 保留。
- **其他 MDM**：用它们的自定义受管偏好功能，或者为这个偏好域下发等价的 `.mobileconfig`。

官方特别提醒：**用 `defaults write` 写的普通用户偏好不会让策略变成强制**，必须走受管偏好。给 Chrome 偏好域做的描述文件也不会作用到桌面端。

## Linux：Ansible、Puppet 或 Chef

Linux 上和管 Chrome 一样，用配置管理工具把 JSON 文件放到策略目录：

1. 需要时先创建 `/etc/opt/codex/policies/managed/`；
2. 把 JSON 文件直接放进这个目录；
3. 目录和文件属主设为 `root`，桌面端用户可读，只有可信管理员可写，通常目录 `0755`、文件 `0644`；
4. 重启桌面端再核对。

官方示例 `/etc/opt/codex/policies/managed/browser.json`：

```json
{
  "PasswordManagerEnabled": false,
  "CookiesBlockedForUrls": ["https://example.com"]
}
```

注意三点：JSON 要按各策略要求用布尔值、数字、数组或对象；文件要**直接**放在 `managed/` 下，子目录不会被读取；同一条策略不要写在多个文件里。

## 在 chrome://policy 里核对

官方的核对步骤：

1. 先确认下发工具已经把注册表值、描述文件或 JSON 文件送到试点电脑；
2. 完全退出并重新打开桌面端，**在桌面端的内置浏览器里**新开一个标签页，打开 `chrome://policy`（不是在你电脑上的 Chrome 里打开）；
3. 点 **Reload policies**，逐条看值、来源、作用范围、级别和状态。上面的强制策略示例应显示来源 **Platform**、级别 **Mandatory**，没有错误；
4. 在这个浏览器里实际试一下预期行为。策略出现在这页只说明被读到了，不代表功能已经按预期工作。

有些策略点了重新加载还不够，要完全重启应用。

**排查**：策略没出现，查拼写、下发位置、分配范围和读取权限；策略报错或被忽略，查取值类型、是否支持这个平台和策略级别，以及 `chrome://policy` 上报告的冲突策略。

**修改或删除**：改下发源头，并清掉过时的注册表项或文件里的键。用脚本下发的，要先删掉脚本写进去的值，再取消脚本分配；然后重启桌面端再核对一遍。

## 常用的几项策略

244 项里，和「让 agent 在浏览器里干活」关系比较大的有这些（都在官方支持列表里，取值以 Chrome 策略文档为准）：

| 策略 | 用途 |
|---|---|
| `PasswordManagerEnabled` | 关掉密码管理器，避免内置浏览器保存密码 |
| `AutofillCreditCardEnabled`、`AutofillAddressEnabled` | 关掉信用卡和地址自动填充 |
| `URLBlocklist`、`URLAllowlist` | 按网址禁止或放行访问 |
| `CookiesBlockedForUrls`、`CookiesAllowedForUrls` | 按网址拦截或允许 Cookie |
| `DownloadRestrictions` | 限制下载 |
| `ExtensionInstallBlocklist` | 禁止安装指定扩展 |

完整列表见官方文档的 Support policy reference 一节。

## 上线顺序建议

按官方文档的流程，建议这样推：先选几台试点电脑 → 下发 1～2 条策略 → 在 `chrome://policy` 核对并实际测试 → 确认无误后再扩大范围。同时检查 Codex 的 `requirements.toml` 里 `browser_use` 的网站规则，两边别互相矛盾。

## 延伸阅读

- [Codex 浏览器操作与登录态功能](../12-官方工具与集成/02-Codex浏览器操作与登录态功能.md)
- [Codex 内置浏览器本地文件读取风险：EMBRACE 自查与防护](./21-Codex内置浏览器本地文件读取风险-EMBRACE自查与防护.md)
- [Codex config.toml 深入配置：字段覆盖关系与排查方法](./04-Codex-config.toml深入配置-字段覆盖关系与排查方法.md)
