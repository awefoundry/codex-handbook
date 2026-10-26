---
id: windows-sandbox-mxc
title: Codex Windows 沙箱配置：启用 MXC 原生隔离、一条命令验证，以及 elevated / unelevated 回退和常见报错
seo_title: Codex Windows 沙箱：启用 MXC、验证命令与 elevated／unelevated 回退
description: 在 Windows 上用原生沙箱跑 Codex，不必先上 WSL。本文按官方 Windows sandbox 文档讲清 mxc、elevated、unelevated 三种实现，桌面端如何自动优先 MXC，CLI 怎样写 prefer_mxc，一条官方验证命令，以及回退与常见报错怎么处理。
lede: 能开 MXC 就开；开不了就优先 elevated，unelevated 只当临时回退——再配上官方那条验证命令。
url: /guides/codex-windows-sandbox-mxc
status: published
section: guides
category: F-config-model-security
topic: 配置模型与权限安全
content_type: 教程
source_tag: 官方功能
entry_tags: [App, CLI]
difficulty: 进阶
order: 11
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
official_ref: https://learn.chatgpt.com/docs/windows/windows-sandbox
keywords: [Codex Windows 沙箱, Codex MXC, prefer_mxc, elevated sandbox, unelevated, Codex PowerShell]
related: [permissions-sandbox-approvals]
howto: true
faq:
  - q: 桌面端要不要手动开 MXC？
    a: 个人（consumer）账户在设备支持时，ChatGPT 桌面端会自动优先 MXC。企业部署或单独用 CLI 时，在 config.toml 写 [features] prefer_mxc = true，与桌面端同一套偏好。
  - q: 验证命令成功了，是不是就等于沙箱永远用 MXC？
    a: 不一定。官方验证命令用 -c windows.sandbox=mxc 只测这一次启动，不改已保存的沙箱选择。日常要靠 prefer_mxc 或明确的 windows.sandbox，并受设备能力与托管策略约束。
  - q: elevated 和 unelevated 该怎么选？
    a: 用不了 MXC 时，官方优先 elevated（需管理员批准的设置，隔离更完整）。unelevated 是次选回退：网络隔离更弱，且不支持禁止读取路径；适合管理员设置被策略挡住时的临时方案。
---

# Codex Windows 沙箱配置：启用 MXC 原生隔离、一条命令验证，以及 elevated / unelevated 回退和常见报错

> 本文在线版：[codexguide.io/guides/codex-windows-sandbox-mxc](https://codexguide.io/guides/codex-windows-sandbox-mxc)

> 核对依据：learn.chatgpt.com《[Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox)》（Configure and troubleshoot the native Codex sandbox on Windows）。文中「我的用法」是操作顺序建议，不是官方强制规定。本文写作环境**没有**可用的 Windows 11 真机做端到端验证，frontmatter 已标 `client_validation_pending: true`；文中命令与版本号均直接来自上述官方页，未另编 PowerShell 探测脚本。

Codex 在 Windows 上可以用 **ChatGPT 桌面端、CLI 或 IDE 扩展**运行。桌面端支持并行聊天、worktree、定时任务、Git、内置浏览器、文件预览、插件与 Skills 等核心流程；更关键的是——**可以原生跑在 PowerShell 里，用 Windows 沙箱约束文件与网络权限，而不必先装 WSL 或虚拟机**。

沙箱本身不替你决定「要不要问人」：它执行的是**当前生效的权限配置文件（permission profile）**所划定的读写与联网边界；**审批策略（approval policy）**另管何时向你要更多权限。概念分工见姊妹篇《[权限、沙箱与审批](https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi)》。

本文只解决 Windows **原生沙箱实现**怎么选、怎么开、怎么验、怎么回退。

## 1. 三种实现：mxc、elevated、unelevated

官方列出三种 Windows 沙箱实现：

| 实现 | 定位 | 要点（按官方表述） |
| --- | --- | --- |
| **`mxc`** | 兼容设备上的**推荐**方案 | 使用原生进程隔离；**不需要**管理员批准的设置、额外的 Windows 账户或本机防火墙规则 |
| **`elevated`** | MXC 不可用或被关掉时的**首选旧版回退** | 需要管理员批准的设置；沙箱内命令**不以管理员权限**运行 |
| **`unelevated`** | elevated 设置不可用、且组织策略允许时的**次选旧版回退** | 网络隔离弱于 `elevated`；**不支持**禁止读取路径（denied read paths） |

官方选型顺序可以记成一句话：

**设备与策略支持时用 MXC；否则优先 elevated；unelevated 只做次选回退。**

两种旧版实现默认还会使用 **private desktop**，以加强 UI 隔离。

## 2. 你的电脑能不能用 MXC

### 系统版本与 MXC 能力

MXC 依赖本机已具备的 **Microsoft Execution Containers（MXC）**能力。官方写明：Microsoft 在 **Windows 11 24H2（build 26100.9278）** 与 **25H2（build 26200.9278）** 引入了 MXC 进程隔离。能力由微软向 Windows 11 设备滚动发布——**版本矩阵里的「Windows 11 推荐」并不自动等于「这台机器已有 MXC」**。

Windows 版本矩阵（官方，与「能不能开 MXC」是两层问题）：

| Windows 版本 | 支持级别 | 说明 |
| --- | --- | --- |
| Windows 11 | 推荐 | 企业标准化部署的最佳基线 |
| 近期、已充分更新的 Windows 10 | 尽力支持 | 不如 Windows 11 可靠；实践上需 **1809 或更新**（依赖现代控制台／ConPTY 等） |
| 更旧的 Windows 10 | 不推荐 | 更容易缺 ConPTY 等组件，企业环境更易失败 |

额外环境假设（官方）：

- 建议本机有 **`winget`**；没有则先更新 Windows 或安装 Windows Package Manager，再设 Codex。
- 旧版 **`elevated`** 依赖管理员批准的设置。
- 部分企业托管设备即使 OS 版本合格，也会挡住必要的设置步骤。
- **MXC 还要额外的原生能力**（见上）；版本矩阵**不能**单独证明某台设备可用 MXC。

在「设置 → 系统 → 关于」里核对 Windows 版本与 OS 内部版本号，对照 **26100.9278 / 26200.9278** 门槛。真正「这台机能不能跑 MXC」以下一节的**官方验证命令**为准，不要只凭版本号口头判断。

### MXC 的兼容性边界（官方）

即便 MXC 能启动，官方还标了几条边界：

1. **托管网络**：需要有效的 `allow_local_binding = true`。MXC 允许与主机 loopback 服务互通；代理域名规则仍作用于经代理流量，但会去掉代理侧对私网目的地的额外检查。
2. **子进程**：前台命令退出后，残留子进程会停下——依赖脱离开发服务器的流程要单独测。
3. **禁止读取的 glob**：每个沙箱进程启动时按当时匹配文件做快照（与 Linux／WSL 相同）；之后新建的匹配文件，对该已在跑的进程仍可能可读。长驻进程在其生命周期内沿用该快照。

显式 `windows.sandbox = "mxc"` 在原生能力不可用或策略禁止时会失败。

## 3. 启用 MXC

### 桌面端（个人账户）

官方写明：**ChatGPT 桌面端对个人（consumer）账户，在设备支持时会自动优先 MXC。** 多数个人用户不必先改配置；装好支持的 Windows 与 Codex 客户端后，用下一节命令确认即可。

### CLI 与企业：同一偏好开关

企业部署或单独使用 CLI 时，在 `config.toml` 写入：

```toml
[features]
prefer_mxc = true
```

`prefer_mxc = true` 时：设备与策略支持则对 Windows 命令使用 MXC；否则走既有的旧版选择与设置流程。

企业若设备能力或策略不一，可继续把 `windows.sandbox` 设为组织允许的旧版实现（`elevated` 或 `unelevated`）作为回退。管理员可以把上述配置作为默认下发，或通过 `requirements.toml` **强制** `features.prefer_mxc = true`；两种做法都**仍允许**旧版回退。默认值与强制要求的差别，见官方 managed configuration 说明。

### 组织要禁用 MXC

在托管的 `requirements.toml` 中：

```toml
[windows]
allow_mxc = false
```

这会同时挡住**自动优先 MXC**与显式 `windows.sandbox = "mxc"`。既有旧版沙箱设置与要求仍然生效。

## 4. 一条命令验证（官方）

**Codex CLI 0.162.0 及以后**，可以在**不改已保存沙箱选择**的前提下，单独测一次 MXC。在项目目录的 PowerShell 中运行（命令原文来自官方文档）：

```powershell
codex -c windows.sandbox=mxc sandbox --include-managed-config --permission-profile :workspace -- cmd.exe /d /c echo MXC_OK
$LASTEXITCODE
```

**预期**：输出 `MXC_OK`，退出码为 `0`。该检查在 **workspace** 权限配置文件与托管要求下验证命令能否启动。

说明：

- `-c windows.sandbox=mxc` 只影响这次探测，**不会**把日常选择永久改成 MXC。
- 探测失败时，先核对 OS 内部版本／更新、企业是否 `allow_mxc = false`、以及 CLI 是否 ≥ 0.162.0；再考虑下一节回退。
- 本文未在真机复跑该命令；你本机以实际输出与 `$LASTEXITCODE` 为准。

## 5. 用不了 MXC 时：elevated / unelevated

在 `config.toml` 选择旧版回退：

```toml
[windows]
sandbox = "elevated" # 或 "unelevated"
```

### elevated（首选旧版）

- 专用较低权限沙箱用户、文件系统边界、防火墙规则，以及所需本地策略变更。
- 禁止读取 glob 同样在每个沙箱进程启动时枚举（见官方 deny-read glob timing）。
- 需要**管理员批准的设置**；无本地管理员权限可由 IT 预配（见下）。

### unelevated（次选旧版）

- 用当前用户派生的受限 token，ACL 划文件边界，环境级离线控制代替 elevated 的专用离线用户防火墙规则。
- **网络隔离弱于 elevated**，且**不支持**禁止读取路径。
- 适合管理员设置被策略挡住时的临时回退，不宜当长期企业默认。

### 企业约束旧版实现

管理员可在 `requirements.toml` 限制 Codex 能用的旧版实现，例如：

```toml
[windows]
allowed_sandbox_implementations = ["elevated"]
```

该例只允许 `elevated`、禁止回退到 `unelevated`；MXC 可用时**不**因此被限制。要允许两种旧版就写上两个值；未选定模式时仍优先 `elevated`。要一并禁 MXC，用单独的 `windows.allow_mxc`。

### IT 代员工预配 elevated

员工没有本地管理员权限时，IT 可在员工开始用 Codex 之前，从**提升权限的部署流程**安装 CLI 并预配 elevated：

```powershell
codex sandbox setup --elevated --user 'DOMAIN\alice' --codex-home 'C:\Users\alice\.codex'
```

把身份与路径换成该员工的 Windows 身份与 `CODEX_HOME`。命令会读取对应用户配置、完成沙箱预配，并保存 `windows.sandbox = "elevated"`。之后员工在普通终端即可使用。

## 6. 沙箱、权限配置文件与审批怎么配合

Windows 沙箱**强制执行**当前对命令及其子进程生效的文件系统与网络权限。权限配置文件决定哪些路径可读可写、是否允许网络；审批策略单独决定何时为「更多权限」打断你。官方指向 sandbox and approvals 文档；站内支柱页是《[权限、沙箱与审批](https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi)》。

**不要**把「完全访问」当默认：官方提醒全权限模式下 Codex 不限于项目目录，可能造成无意破坏。更稳妥的是保留沙箱边界，用窄规则开例外。

CLI 用 **`/status`**、**`/debug-config`** 看生效配置。读不到目录时，先查权限配置文件、托管要求与 Windows 文件权限；有托管限制时请管理员审查，而不是关沙箱。

**我的用法**（非官方）：先跑官方 MXC 验证 → 成功则靠桌面端自动优先或 `prefer_mxc = true` → 失败再用 `elevated`；仅当 elevated 被策略挡住时临时 `unelevated`，并请 IT 跟进。

## 7. 常见报错与排查（仅官方已文档化项）

托管机上先看：**当前沙箱模式、Windows 版本、策略错误**。MXC 查兼容性与网络策略；旧版多查设置、logon rights、文件权限。

### 旧版沙箱设置失败

`elevated` 设不上时，官方常见原因：拒了 UAC／管理员提示；不允许创建本地用户／组；不允许改防火墙；挡住沙箱用户所需 logon rights；或其他企业策略挡住设置。

可再跑一次 elevated 设置并在允许时批准提示；公司本请 IT 确认上述能力；仍失败且策略允许时可暂用 `unelevated`。

### 被切到 unelevated

可能是配置选择，也可能是 elevated 不可用时的回退。仍有 ACL 文件边界，但没有 elevated 的独立沙箱用户边界，网络隔离更弱。企业机先查 MXC；不可用或被禁时请 IT 预配 `elevated`。

### Windows 错误 1385

表示 Windows 拒绝了沙箱用户启动命令所需的登录类型。常见情况是用户已建好，但策略仍禁止启动。请 IT 确认 logon rights；对比组策略／OU；急需继续时可暂用 `unelevated`；反馈附 `CODEX_HOME/.sandbox/sandbox.log`、Windows 版本与简述。

### 警告：部分文件夹对 Everyone 可写

路径权限过宽，沙箱保护不充分。审查警告中的文件夹，环境允许时去掉 `Everyone` 写权限，然后重启 Codex 或重跑沙箱设置；不确定就问 IT。

### 沙箱内命令上不了网

有的会话按权限模式故意关出站网络。先确认是否本就不该联网；若预期应联网，重启再试；持续失败则收集沙箱日志，查是否处于不完整或损坏状态。

### 以前能沙箱，现在不行

常见于移动仓库／工作区、改机器权限、改 Windows 策略等。可重启 Codex；MXC 重跑兼容性探测并查网络策略；elevated 再跑设置；策略允许时临时 `unelevated`；收集沙箱日志。

### 向 OpenAI 发诊断时带什么

发送 `CODEX_HOME/.sandbox/sandbox.log`，并尽量附上：在做什么、所选实现（`mxc`／`elevated`／`unelevated`）、应用错误、是否 `1385` 或其他 Windows／PowerShell 错误、Windows 内部版本号、Win11 还是 Win10。

**不要发送** `CODEX_HOME/.sandbox-secrets/` 的内容。

### IDE 扩展已安装但无响应

可能缺 C++ 工具链。官方提到 Visual Studio Build Tools（C++ 工作负载）、MSVC Redistributable（x64）；也可用 `winget install --id Microsoft.VisualStudio.2022.BuildTools -e`。装完后**完全重启** VS Code。

未列出的报错：仍收集 `sandbox.log` 与版本信息反馈，勿直接关沙箱。

## 8. 什么时候改用 WSL

官方建议：**默认用原生 Windows 沙箱**。需要 Linux 原生工具链、工作流已在 WSL2，或原生实现不够用时再考虑 WSL。WSL 不是权限开关；切过去后仍要单独确认工作区、挂载路径与沙箱／审批。安装见知识库《Windows 和 WSL 安装 Codex CLI》《安装登录常见问题》。

## 9. 检查清单

- [ ] 已在「关于」中看过 Windows 版本；对照 MXC 的 24H2／25H2 内部版本门槛（**26100.9278**／**26200.9278**）。
- [ ] CLI ≥ **0.162.0**，已在项目目录跑过官方验证命令，看到 `MXC_OK` 且退出码 `0`（或已记录失败现象）。
- [ ] 个人桌面端：设备支持时依赖自动优先；CLI／企业：按需设置 `prefer_mxc = true`。
- [ ] 组织若禁用 MXC：已确认 `requirements.toml` 中 `allow_mxc`／`allowed_sandbox_implementations`。
- [ ] MXC 不可用时优先 `elevated`；无管理员权限时走 IT 预配命令；仅临时使用 `unelevated`。
- [ ] 权限边界与审批仍按任务需要配置；未用「完全访问」当默认。
- [ ] 出问题时用 `/status`、`/debug-config`，并按官方清单收集 `sandbox.log`（不发送 `.sandbox-secrets`）。

## 参考

- 官方：[Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox)
- 站内：[权限、沙箱与审批](https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi)（`permissions-sandbox-approvals`）
- 知识库：`01-安装与首次使用/05-Windows和WSL安装Codex-CLI.md`、`01-安装与首次使用/13-安装登录常见问题.md`（错误 1385 等安装期问题可交叉查阅）
