---
id: php2shell-checker-skill
title: Codex 检查 PHP2Shell 漏洞：安装 OpenAI 官方 php2shell-checker Skill，看懂 OK / VULNERABLE / UNKNOWN，再升级到 PHP 8.5.12、8.4.27、8.3.36 或 8.2.35
seo_title: Codex 检查 PHP2Shell：官方 php2shell-checker Skill 与升级版本
description: PHP 于 2026-10-21 披露两个可未认证远程执行代码的严重漏洞（常称 PHP2Shell）。OpenAI 同步发布官方 Codex Skill php2shell-checker。本文按仓库 README 与 SKILL.md，说明如何用 $skill-installer 安装，$phpcheck-url／$phpcheck-server 怎么查，如何理解 OK、VULNERABLE、UNKNOWN，以及应升级到哪些 PHP.net 安全版本。
lede: 先装上 OpenAI 官方检查 Skill，看懂三种结果，再按 PHP.net 公告升级——检查器不做漏洞利用探测。
url: /guides/codex-php2shell-checker-skill
status: draft
section: guides
category: G-skills
topic: Skills 与外部工具
content_type: 教程
source_tag: 官方生态
entry_tags: [App, CLI, Skills]
difficulty: 进阶
order: 7
author: CodexGuide
contributors: [CodexGuide]
date_published: 2026-10-22
date_modified: 2026-10-22
models: [gpt-6.1-sol, gpt-6-luna, gpt-6-astra]
official_ref: https://github.com/openai/php2shell-checker
keywords: [Codex PHP2Shell, php2shell-checker, phpcheck-url, phpcheck-server, CVE-2026-109618, CVE-2026-109619, $skill-installer]
related: [create-codex-skill, codex-github-issue-pr-workflow, permissions-sandbox-approvals]
howto: true
faq:
  - q: UNKNOWN 是不是表示网站已经打过补丁？
    a: 不是。仓库 README 写明：「UNKNOWN does not mean the target is patched!」常见原因是响应头隐藏了 PHP 版本、无法拿到版本，或版本／分支不在检查器内嵌表里。应改用有服务器权限的检查，或对照 PHP／发行版官方公告。
  - q: 检查器会不会对目标做漏洞利用探测？
    a: 不会。phpcheck-url 与 phpcheck-server 的 SKILL.md 都写明「Do not run exploit probes」。URL 检查只读响应头里的 Server／X-Powered-By；服务器侧核对 php -v 与站点实际进程，不做利用探测。
  - q: 没有 Codex 能不能查？
    a: 能。仓库提供独立 CLI：`node phpcheck.js "https://example.com"` 或 `node phpcheck.js --local`，可用 `--json` 接进脚本。退出码与 Skill 一致。
---

# Codex 检查 PHP2Shell 漏洞：安装 OpenAI 官方 php2shell-checker Skill，看懂 OK / VULNERABLE / UNKNOWN，再升级到 PHP 8.5.12、8.4.27、8.3.36 或 8.2.35

> 本文计划路径：[codexguide.io/guides/codex-php2shell-checker-skill](https://codexguide.io/guides/codex-php2shell-checker-skill)

> 核对依据：OpenAI《[php2shell-checker](https://github.com/openai/php2shell-checker)》README 与 `skills/phpcheck-url/SKILL.md`、`skills/phpcheck-server/SKILL.md`、OpenAI《[Patch the Planet: global response coordination as agents uncover critical vulnerabilities](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/)》（2026-10-21）、PHP.net《[Security advisory: Critical remote code execution vulnerabilities, update now](https://www.php.net/archive/2026.php#2026-10-21-5)》及 GHSA 公告页。文中「我的用法」是操作顺序建议。本预览环境**没有**可对真实业务站做检查的授权测试站点，故不写假终端输出、不编造扫描结果、不放假截图；`client_validation_pending: true`。安全事实只引用上述官方来源，**不写利用细节、PoC、payload 或攻击步骤**。

2026 年 10 月 21 日，PHP 项目披露了两个可在**未认证**情况下导致远程代码执行的严重漏洞；社区与安全厂商常用「PHP2Shell」称呼这次事件。同一天，OpenAI 在协调披露文章里说明：他们把 **PHP 版本检查工具做成了 Codex Skill**，方便运维判断该装哪些更新。仓库是 **[openai/php2shell-checker](https://github.com/openai/php2shell-checker)**（Apache-2.0）。

这篇按一条可复查的主线：

1. 官方说了什么、哪些运行方式在风险范围内、已修复版本是哪些  
2. 在 Codex 里用 `$skill-installer` 装上两个 Skill  
3. 只有网址时用 `$phpcheck-url`，有服务器权限时用 `$phpcheck-server`  
4. 看懂 `OK` / `VULNERABLE` / `UNKNOWN` 与退出码  
5. 不用 Codex 时直接跑 `node phpcheck.js`  
6. 查完之后只按 PHP.net（或发行版）升级到安全版本  
7. 安全边界：检查器不做利用探测，也不能替代官方公告  

Skill 目录怎么写、怎么测触发，见姊妹篇《从零创建 Codex Skill》。在服务器上放宽权限前，先读《权限、沙箱与审批》；升级后若要走仓库变更与评审，可接《GitHub Issue 到 Pull Request》。

## 1. 发生了什么（只引用官方公告）

按 [PHP.net 2026-10-21 安全公告](https://www.php.net/archive/2026.php#2026-10-21-5)：

- **已修复版本**：PHP **8.5.12**、**8.4.27**、**8.3.36**、**8.2.35** 修复了两个可未认证远程执行代码的严重漏洞。所有 PHP 用户都被强烈建议立即更新。  
- **CVE／GHSA**（技术细节以公告与 advisory 原文为准，本文不展开利用路径）：  
  - [CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w)（GHSA-w8hw-w9fx-j79w）  
  - [CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)（GHSA-6wmf-4rv5-p3rp）  
- **谁在风险范围内**：所有处理 Web 请求的 PHP 安装，包括 PHP-FPM、Apache mod_php、php-cgi、FrankenPHP、LiteSpeed。PHP 官方认为 **mod_php 风险最高**。  
- **旧分支**：PHP 8.1 及更早版本不再由 PHP 项目更新；部分发行版／LTS 厂商可能提供向后移植补丁。PHP 安全团队为 7.4／8.0／8.1 提供了最小源码回移植，便于自行编译或缺少 LTS 渠道的用户——具体以 PHP.net 公告与厂商说明为准。

OpenAI《[Patch the Planet…](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/)》写明：Calif 用 GPT‑5.6 Sol 在 Patch the Planet 计划中发现了其中一个严重问题，Wiz 也独立发现并报告了两个漏洞；PHP 维护者主导修复与发布，OpenAI 与合作方协助协调。对使用 PHP 的组织，**当前优先事项是应用修复**；文章同时指向作为 Codex Skill 发布的 PHP 版本检查工具。

**我的用法：** 先打开 PHP.net 公告确认「今天」官方推荐的安全版本号，再决定用检查器比对；版本表会随公告更新，不要只记本文写作时的数字。

## 2. 安装官方 Skill：`$skill-installer` 一次装两个

仓库 README 的安装说明是：在 Codex 里让它执行：

```text
$skill-installer install both skills from https://github.com/openai/php2shell-checker
```

装好后会得到两个 Skill（名称来自各自 `SKILL.md` 的 `name` 字段）：

| Skill | 适用场景 | 目录（仓库内） |
| --- | --- | --- |
| **phpcheck-url** | 只有网站 URL／主机名 | `skills/phpcheck-url/` |
| **phpcheck-server** | 有本机或服务器访问权限 | `skills/phpcheck-server/` |

仓库根目录的 `phpcheck.js` 会转调 url Skill 目录下的脚本；两个 Skill 的检查逻辑同源。许可为 Apache-2.0；README 写明 **OpenAI 暂不接受外部代码贡献**，问题与非代码反馈走 GitHub Issues。

装完后**新开一轮对话**再调用 `$phpcheck-url`／`$phpcheck-server`，避免旧会话还看不到刚装的 Skill。`$skill-installer` 与手写 Skill 目录的关系，见《从零创建 Codex Skill》。

**我的用法：** 安装命令直接用 README 原文（含仓库 HTTPS URL），不要改成未核实的镜像或第三方 fork。

## 3. 只有网址时：`$phpcheck-url`

按 `phpcheck-url` 的 SKILL.md，在 Skill 目录下等价于运行：

```sh
node scripts/phpcheck.js "https://example.com" --json
```

在 Codex 对话里，README 示例是：

```text
$phpcheck-url check https://example.com
```

要点（全部来自 README／SKILL.md，不是猜测）：

- 裸主机名用 **HTTPS**。  
- 检查器读取响应头里的 **`Server`** 与 **`X-Powered-By`**。  
- 先发 **HEAD**；仅当状态码为 **405** 或 **501** 时才回退到 **GET**。  
- **不跟随跳转**，**不检查响应体**。  
- 版本被隐藏或拿不到时，报告 **unknown**。  
- **Do not run exploit probes**（不要做漏洞利用探测）。

局限：头可以被改掉或隐藏；发行版向后移植可能让「旧版本号」其实已带补丁。SKILL 明确写：服务器侧的版本与软件包核对是更强证据。

本预览未对真实站点实测，因此这里不贴「某次检查」的 stdout。你授权自己的测试站后，应看到下一节表中的三种结果之一。

## 4. 有服务器权限时：`$phpcheck-server`

对话示例（README）：

```text
$phpcheck-server check the PHP version serving my site
```

`phpcheck-server` 的 SKILL.md 要求：

1. 从 `php -v` 入手，但**核对它是否就是站点实际在用的 PHP-FPM／Apache 等进程**（CLI 与 Web SAPI 可能不是同一套二进制）。  
2. 对照检查器内嵌的受影响范围（**截至 2026-10-20**），并把完整包版本与 PHP／厂商安全公告比对。  
3. 发行版 backports 可能修复「看起来更旧」的版本号；未列入表中的分支先当作 unknown，直到有公告确认。  
4. **仅有配置项不能证明已打补丁**；有用的是运行中的 PHP 构建与厂商包公告。  
5. 无法核实服务版本时报告 unknown。再次强调：**Do not run exploit probes**。

SKILL 给出的受影响范围表（inclusive，与检查器脚本内 `VULNERABLE_THROUGH` 截止补丁号一致；写作时以仓库为准）：

| PHP 分支 | 受影响范围（含端点） |
| --- | --- |
| 5.4～8.1 | 各分支自首个版本至该分支表内终点（见 SKILL 全文） |
| 8.2 | 8.2.0–8.2.34 |
| 8.3 | 8.3.0–8.3.35 |
| 8.4 | 8.4.0–8.4.26 |
| 8.5 | 8.5.0–8.5.11 |

对应地，PHP.net 已发布的安全版本为 **8.2.35／8.3.36／8.4.27／8.5.12**（及公告中的旧分支处理说明）。

在服务器上让 Codex 跑检查前，先收紧沙箱与审批范围，避免「为了查版本」顺手放开远超任务所需的主机权限——见《权限、沙箱与审批》。

## 5. 看懂结果：OK、VULNERABLE、UNKNOWN

README「Results」表：

| 结果 | 退出码 | 含义（按 README 原文意译） |
| --- | --- | --- |
| **OK** | `0` | 所列 major/minor 分支上，稳定补丁版本高于内嵌截止版本。 |
| **VULNERABLE** | `1` | 该分支上版本处于或低于内嵌截止版本。 |
| **UNKNOWN** | `3` | 没有 PHP 版本或响应、无法识别的版本／分支，或较新的预发布构建。 |

另：参数无效时退出码为 **`2`**。加 **`--json`** 时，机器可读字段 `patch_status` 为 `ok`／`vulnerable`／`unknown`。

README「Limitations」里必须记住的三点：

1. **`OK` 是版本比较**，前提是假设所列分支后续稳定补丁包含修复；它**不独立验证**安全修复是否真的打上。请把版本与 [PHP 官方安全发布](https://www.php.net/archive/2026.php#2026-10-21-5) 对照。  
2. 响应头可被隐藏或篡改；**发行版 backports 可能不改上游版本号**。  
3. **`UNKNOWN` 不等于目标已打补丁。**

Skill 侧补充：退出码 `1` 与 `3` 表示 vulnerable／unknown，**不是**脚本执行失败。

**我的用法：**

- 得到 **VULNERABLE** → 按下一节升级（或联系主机商／发行版），不要停留在「先观察」。  
- 得到 **UNKNOWN** → 当作「证据不足」：隐藏头就改用 `$phpcheck-server`／厂商包查询；仍不清楚就按 PHP.net「立即更新」处理。  
- 得到 **OK** → 仍用 `php -v`／包管理器核对一次实际 Web SAPI，并关注后续安全公告。

## 6. 不用 Codex：`node phpcheck.js`

克隆或下载 [openai/php2shell-checker](https://github.com/openai/php2shell-checker) 后，在仓库根目录：

```sh
# 检查网站（读响应头中的 PHP 版本线索）
node phpcheck.js "https://example.com"

# 检查本机 CLI PHP
node phpcheck.js --local

# 指定 php 可执行文件
node phpcheck.js --local --php /usr/bin/php8.3

# 机器可读
node phpcheck.js "https://example.com" --json

# 可选：超时（秒，须 >0 且 ≤60）
node phpcheck.js "https://example.com" --timeout 10
```

需要 Node.js（脚本使用 `fetch`、`node:util` 的 `parseArgs` 等现代 API）。仓库自带测试：

```sh
node --test phpcheck.test.js
```

README 说明：测试对本地 HTTP 服务与假 PHP 可执行文件运行，**不需要**真实 PHP 安装，也**不需要**外网网站。

把 `--json` 接到监控或变更流水线时，仍只应做**版本比对与告警**，不要改成任何形式的利用探测。

## 7. 查完之后：升级到官方安全版本

完整解决方案是**更新 PHP**。按 PHP.net 公告：

1. **升级到** [PHP 8.5.12](https://www.php.net/releases/8_5_12.php)、[8.4.27](https://www.php.net/releases/8_4_27.php)、[8.3.36](https://www.php.net/releases/8_3_36.php) 或 [8.2.35](https://www.php.net/releases/8_2_35.php)（源码与 Windows 二进制见 [downloads](https://www.php.net/downloads)）。各版本发布说明均强调：没有完整缓解措施，**更新是唯一安全选择**。  
2. **Linux 发行版／LTS 厂商**已提前收到补丁——以你的发行版安全公告与包版本为准，不要只看 `php -v` 的上游三元组。  
3. **PHP 8.1 及更早**：项目侧不再更新；向厂商索取 backport，或升级到仍受支持的分支。公告还提到：依赖志愿者维护的 `rpms.remirepo.net` 的用户，应尽快改用发行版包或自行从源码构建以便立即打补丁（该 repo 在公告当日不会有更新）。  
4. **无法立即更新时**：PHP.net 公告列出了若干**降低特定攻击面暴露**的临时措施，并写明它们**不能让安装变得安全**。细节与限制以 [公告原文](https://www.php.net/archive/2026.php#2026-10-21-5) 为准；本文不转述临时配置步骤，避免读者把「临时措施」当成已修复。  
5. **托管／共享主机**：若你无法控制 PHP 包，把 CVE 编号与 PHP.net 链接发给主机商，要求确认已部署安全版本或厂商 backport，并索取可验证的版本／包修订号。

升级后再次运行 `$phpcheck-server` 或 `node phpcheck.js --local`，并确认 **Web 所使用的 SAPI**（而不只是 PATH 里的 CLI）已切换。若变更进了应用仓库，可用 Codex 走 Issue→PR 与安全相关评审流程。

OpenAI 文章与 [Patch the Planet](https://patchtheplanet.org/) 站点也汇总了维护者补丁与合作方指引；**补丁权威来源仍是 PHP 项目与你的发行版／主机商**。

## 8. 安全边界（必读）

1. **检查 ≠ 利用。** 两个 Skill 都写明 **Do not run exploit probes**。本文与知识库不会提供 PoC、payload、攻击步骤或「验证漏洞是否可触发」的操作指南。  
2. **检查 ≠ 公告。** `OK` 只是相对内嵌截止版本的比较；是否修复以 PHP.net／GHSA／发行版公告为准。  
3. **UNKNOWN ≠ 安全。** 隐藏版本头很常见；把它当成需要跟进的信号。  
4. **权限最小化。** 在生产机上跑 `$phpcheck-server` 时，只给读取版本与包信息所需的权限；不要为了「方便」打开无关的网络或写权限。  
5. **来源白名单。** 安装与升级指引只认 [openai/php2shell-checker](https://github.com/openai/php2shell-checker)、[PHP.net 公告](https://www.php.net/archive/2026.php#2026-10-21-5) 与对应 GHSA；不要根据论坛传言或未署名 PoC 做决策。

## 9. 常见问题

**Q：我只看到 UNKNOWN，站点是不是没问题？**  
A：不是。按 README，UNKNOWN 不表示已打补丁。隐藏 `X-Powered-By`／`Server`、检查失败、或不在内嵌分支表内，都会得到 UNKNOWN。请改用服务器侧检查或厂商包公告。

**Q：发行版说已经 backport，但 php -v 仍显示旧三元组，检查器报 VULNERABLE，听谁的？**  
A：听**带安全公告的厂商包修订说明**。README／SKILL 都承认 backports 可能不改上游版本号。把包版本、changelog 与公告 CVE 列表对齐；必要时向发行版安全团队确认，而不是只信检查器的版本比较。

**Q：能不能对公网任意网站批量扫描？**  
A：工具设计是给你**自己有权管理**的站点或本机 PHP 做版本比对。对未授权目标做大规模探测可能违法或违反服务条款；本文只讨论自有资产与已获授权的检查。

## 10. 小结

| 步骤 | 做什么 |
| --- | --- |
| 1 | 读 [PHP.net 安全公告](https://www.php.net/archive/2026.php#2026-10-21-5)，记下当前安全版本 |
| 2 | `$skill-installer install both skills from https://github.com/openai/php2shell-checker` |
| 3 | 有 URL 用 `$phpcheck-url`；有服务器权限用 `$phpcheck-server`（或 `node phpcheck.js`） |
| 4 | 按 OK／VULNERABLE／UNKNOWN 决策；UNKNOWN 继续取证 |
| 5 | 升级到 8.5.12／8.4.27／8.3.36／8.2.35 或厂商等价安全包，再复查 Web SAPI |
| 6 | 全程不做利用探测；有疑问以官方公告为准 |

## 相关阅读

- 从零创建 Codex Skill → https://codexguide.io/guides/create-codex-skill  
- GitHub Issue 到 Pull Request → https://codexguide.io/guides/codex-github-issue-pr-workflow  
- 权限、沙箱与审批 → https://codexguide.io/guides/codex-quan-xian-sha-xiang-yu-shen-pi  

## 参考链接（官方）

- https://github.com/openai/php2shell-checker  
- https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/  
- https://www.php.net/archive/2026.php#2026-10-21-5  
- https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w  
- https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp  
- https://patchtheplanet.org/  
