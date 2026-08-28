# Codex config.toml 深入配置：字段、覆盖关系与排查方法

> 测试环境：Windows 11 24H2；Codex CLI 0.147.0；PowerShell 7.6.4；2026-08-27 核验。

Codex 的配置问题通常不是“字段不会写”，而是“写在了错误的层级”。同一个 `model`、`sandbox_mode` 或 `approval_policy`，可能同时出现在用户配置、Profile、项目配置和命令行里。只打开某个文件看一眼，不能证明它就是最终生效值。

本文建立一套可复用的判断方法：先定位配置来源，再按优先级推导最终值，最后用一个低风险任务验证运行时行为。文中的字段和值以 [OpenAI 配置参考](https://developers.openai.com/codex/config-file/config-reference) 为准；本机 CLI 为 `0.147.0`，升级后应重新核对。

## 先建立配置心智模型

把配置分成四个问题会更容易排查：

- **来源**：这个值来自哪个文件或参数？
- **覆盖**：是否有更高优先级的同名键？
- **边界**：这个键是否允许在当前层级出现？
- **验证**：运行中的 Codex 是否表现出这个值对应的行为？

### 生效优先级

从高到低，当前 Codex 的常用顺序是：

1. CLI 专用参数和 `--config`/`-c` 临时覆盖。
2. 项目级 `.codex/config.toml`：从项目根目录向当前目录逐层读取，离当前工作目录最近的文件优先；仅对已信任项目加载。
3. `--profile name` 选择的 `$CODEX_HOME/name.config.toml`。
4. 用户级 `$CODEX_HOME/config.toml`。
5. 系统级配置（Unix 常见位置为 `/etc/codex/config.toml`，具体由部署方式决定）。
6. Codex 内置默认值。

这不是“整文件替换”。通常是按键合并：高层定义了 `sandbox_mode`，低层的 `model` 仍然可以保留。表格或数组字段的合并规则要以配置参考中该字段的说明为准，不能自行假设所有嵌套表都是深度合并。

### 三种本地路径

| 场景 | 用户配置 | 项目配置 | 注意事项 |
|---|---|---|---|
| Windows PowerShell | `$env:USERPROFILE\.codex\config.toml` | `<repo>\.codex\config.toml` | `~` 展开到 Windows 用户目录；不要复制 `/home/...` 路径。 |
| macOS/Linux | `$HOME/.codex/config.toml` | `<repo>/.codex/config.toml` | 项目层从根目录向当前目录逐层读取。 |
| WSL2 | WSL 内的 `$HOME/.codex/config.toml` | WSL 项目目录下的 `.codex/config.toml` | WSL 与 Windows 有各自的用户目录；先在实际运行 Codex 的环境中执行 `echo $CODEX_HOME`。 |

如果设置了 `CODEX_HOME`，以上用户级路径都改为 `$CODEX_HOME`。在 PowerShell 中先确认：

```powershell
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
Resolve-Path (Join-Path $codexRoot "config.toml") -ErrorAction SilentlyContinue
```

项目配置只能覆盖它允许覆盖的项目字段。官方当前明确列出的项目层禁用键包括 `model_provider`、`model_providers`、`openai_base_url`、`notify`、`profile`、`profiles`、`otel` 等。看到这些键时，Codex 会忽略它们并在启动时给出警告；提供商、通知、遥测和 Profile 选择应放在用户或受管控层。

## 常用字段怎么分组

不要把所有字段抄进一个“大而全”的模板。按风险和变更频率分组，出错时更容易定位。

| 目的 | 字段 | 当前可用值或形态 | 建议 |
|---|---|---|---|
| 选择模型 | `model` | 字符串，如 `gpt-5.6` | 先确认账号和版本可用，再写入默认值。 |
| 调整推理 | `model_reasoning_effort` | `minimal`、`low`、`medium`、`high`、`xhigh` | 只对支持的模型/Responses API 生效；`xhigh` 是模型相关能力。 |
| 控制审批 | `approval_policy` | `untrusted`、`on-request`、`never`，或 `granular` 表 | `never` 只是“不停下来问”，不是安全保证。 |
| 指定审核者 | `approvals_reviewer` | `user`、`auto_review` | 只改变谁审核符合条件的请求，不扩大沙箱。 |
| 控制沙箱 | `sandbox_mode` | `read-only`、`workspace-write`、`danger-full-access` | 日常开发优先 `workspace-write`；全访问只适合已有外部隔离的环境。 |
| 开放工作区网络 | `[sandbox_workspace_write] network_access` | 布尔值 | 默认关闭；只为明确的安装或 API 任务打开。 |
| 控制 Web 搜索 | `web_search` | `cached`、`indexed`、`live`、`disabled` | Web 搜索开关不等于给 shell 命令开放网络。 |
| 过滤环境变量 | `[shell_environment_policy]` | `inherit`、`set`、`filters` 等 | 新配置使用 `filters`；不要和旧的 `exclude`/`include_only` 同层混用。 |
| Windows 沙箱启动 | `[windows] sandbox` | `elevated`、`unelevated` | 原生 Windows 优先 `elevated`；无管理员权限时再用 `unelevated`。 |

审批和沙箱必须一起看：`approval_policy` 回答“何时询问”，`sandbox_mode` 回答“最多能访问什么”。例如 `approval_policy = "never"` 配上 `sandbox_mode = "read-only"`，仍然是只读边界；反过来，`workspace-write` 也不会自动开放网络。

### 一个保守的起点

下面配置只包含常用且容易验证的键。它适合个人开发起点，不包含凭据、代理密码或真实机器路径。

```toml
model = "gpt-5.6"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

[sandbox_workspace_write]
network_access = false

[windows]
sandbox = "elevated"
```

如果只做代码阅读，把 `sandbox_mode` 改为 `read-only`。如果确实需要联网安装依赖，优先用一次性的 `-c sandbox_workspace_write.network_access=true`，任务完成后不要把网络开关永久留在全局配置中。

## Profile、项目层和临时覆盖

### Profile 是一层，不是另一套账号

`--profile review` 会先加载用户 `config.toml`，再叠加 `$CODEX_HOME/review.config.toml`。Profile 文件只写与默认值不同的键：

```toml
# $CODEX_HOME/review.config.toml
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "read-only"
```

启动时显式选择：

```powershell
codex --profile review
codex exec --ephemeral --profile review "只读检查当前变更并总结风险，不修改文件"
```

从 Codex `0.134.0` 起，`[profiles.review]` 和顶层 `profile = "review"` 不是当前 Profile 读取方式。旧配置应迁移到独立的 `review.config.toml`，否则容易出现“文件存在但没有生效”。

### 项目层只放团队默认值

仓库中的 `.codex/config.toml` 适合放最低安全基线，例如 `sandbox_mode = "read-only"` 或关闭工作区网络。它不适合放 API Key、个人代理、账号路径，也不应借项目层切换提供商或 Profile。陌生仓库的 `.codex` 内容先审查再信任，因为同一层还可能包含 hooks 和规则。

### 临时覆盖优先用于实验

专用参数优先于通用 `-c`：

```powershell
codex --model gpt-5.6-terra --sandbox read-only --ask-for-approval on-request
```

任意键可以用 TOML 值覆盖，值不是 JSON：

```powershell
codex -c 'model="gpt-5.6-terra"'
codex -c sandbox_workspace_write.network_access=true
codex -c 'shell_environment_policy.filters={"PATH"="include"}'
```

PowerShell 会处理引号和空格；先在命令行验证，再决定是否写入文件。`--ignore-user-config` 可用于排除用户层干扰，但它不会跳过认证目录本身。

## 从最小改动开始验证

配置验证要验证“行为”，而不是只验证“文件能打开”。建议每次只改一个字段，并保留一份备份：

```powershell
$configPath = Join-Path $codexRoot "config.toml"
Copy-Item -LiteralPath $configPath -Destination ($configPath + ".bak-20260827")
Get-Content -LiteralPath $configPath
```

### 配置成功：只读边界

在临时目录启动一个只读会话：

```powershell
$probeRoot = Join-Path $env:TEMP "codex-config-probe"
New-Item -ItemType Directory -Force -Path $probeRoot | Out-Null
Set-Content -LiteralPath (Join-Path $probeRoot "probe.txt") -Value "read-ok" -Encoding utf8
codex exec --ephemeral --sandbox read-only --ask-for-approval on-request -C $probeRoot `
  "读取 probe.txt，尝试创建 write-probe.txt；被拒绝时不要重试，并报告 READ、WRITE 结果"
```

预期是 `READ=ALLOWED`、`WRITE=DENIED`。这里验证的是沙箱行为，不代表所有命令都能运行。

### 配置被覆盖：同一字段的高层值

假设用户配置里写了 `sandbox_mode = "read-only"`，但项目 `.codex/config.toml` 写了 `sandbox_mode = "workspace-write"`。在已信任的项目目录执行：

```powershell
codex --sandbox read-only -C .
```

此时 CLI 专用参数优先，最终应回到只读。去掉 `--sandbox read-only` 后，项目层才可能成为最终值。用 `/status` 查看当前工作区和权限边界；交互界面提供 `/debug-config` 时，再用它核对配置来源。若两个入口都不可用，就用上面的读写探针做行为验证，并记录命令行参数、工作目录和项目是否已信任。

## 配置不生效的排查顺序

按下面顺序排查，通常比反复改字段快：

1. **路径错**：打印 `$CODEX_HOME`，确认实际运行环境是 Windows 还是 WSL2，并确认文件名确实是 `config.toml` 而不是 `config.toml.txt`。
2. **项目未信任**：项目层、项目 hooks 和规则会一起被跳过。先在可信的临时仓库复现，不要为了验证而直接信任陌生仓库。
3. **TOML 语法错**：检查引号、布尔值和表头。需要严格失败时加 `--strict-config`，让当前版本遇到未知字段直接退出。
4. **字段不存在或值类型错**：对照配置参考和本机 `codex --help`；不要把旧教程中的 `[profiles.name]`、废弃值或 JSON 对象原样复制。
5. **被更高层覆盖**：记录 CLI 参数、最近的项目 `.codex/config.toml`、Profile 文件和用户文件，逐层删减到最小配置。
6. **受管控约束**：组织可能通过 `requirements.toml` 限制 `approval_policy`、`sandbox_mode`、Profile 或 Web 搜索模式。管理员约束不能由本地配置放宽。
7. **进程未重载**：关闭并重新启动 CLI/桌面会话，再做一次探针；不要在同一个长期会话里假设文件改动已自动加载。

### 一份可复制的排查记录

```text
核验日期：2026-08-27
Codex：codex-cli 0.147.0
工作目录：<脱敏后的临时目录>
CODEX_HOME：<仅记录目录名，不记录用户名>
CLI 覆盖：--sandbox read-only
项目是否信任：是/否
预期：读取允许、写入拒绝
实际：<记录输出或 /status 摘要>
结论：生效 / 被项目层覆盖 / 被受管控要求限制 / 语法或版本错误
```

## 回滚与安全检查

- 修改前复制配置并保留 `git diff --no-index` 或文件哈希；不要直接覆盖唯一副本。
- 先用临时 `-c` 验证，再把确认过的键写回对应层级。
- 全局配置只放个人默认值；项目配置只放团队最低边界；CI 用独立 Profile 和工作流固定命令。
- `.env`、`auth.json`、SSH 密钥、代理密码和真实用户路径不应进入仓库，也不要粘贴到 Issue 或截图中。
- `danger-full-access` 与 `approval_policy = "never"` 组合会移除重要防线。只有外层容器或虚拟机已经承担隔离时才考虑，并在任务结束后恢复默认边界。
- 配置变更后检查 `git status --short`，确认没有把备份、日志或凭据文件带进提交。

## 参考资料与相关教程

- [OpenAI Codex 配置基础](https://developers.openai.com/codex/config-file/config-basic)：位置、层级、项目信任和常见字段。
- [OpenAI Codex 高级配置](https://developers.openai.com/codex/config-file/config-advanced)：Profile、`--config`、项目覆盖、环境变量策略和提供商配置。
- [OpenAI Codex 配置参考](https://developers.openai.com/codex/config-file/config-reference)：字段类型、可选值和受管控要求。
- [OpenAI Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)：沙箱、审批、网络和受管控约束。
- [Codex 配置文件怎么写](./02-Codex配置文件怎么写-config.toml位置优先级与常用字段.md)：先完成基础位置和优先级核对。
- [Codex 权限怎么设](./03-Codex权限怎么设-沙箱审批策略与自动执行边界.md)：理解沙箱、审批与网络边界。
- [Codex 多配置 Profile](./06-Codex多配置Profile-个人项目团队和CI如何隔离.md)：把个人、团队审查和 CI 的配置拆开。

## 结语

遇到“明明改了却没生效”，先不要继续堆字段。打印实际路径，列出优先级，临时覆盖一个键，再用最小读写探针验证。把每次修改和验证结果留下记录，升级 Codex 后也能快速判断是字段变化，还是配置层级发生了变化。

如果你正在整理团队的 Codex 配置、权限和 CI 约束，可以继续查看 [CodexGuide 配置、模型与权限安全专题](https://codexguide.io/guides?utm_source=wechat&utm_medium=article&utm_campaign=codex-config-deep-dive&utm_content=closing-website-01)。

## 配图素材备用区（暂不计入正文图号）

本节是 `gzhstart` 工作区的备份材料索引，发布前如需配图，请将经过核验的素材移动到正文段落并重新编号。

### 官方与可核验操作界面

- `01-openai-config-basics.png`：配置心智模型 / 配置路径；1280×720；证明官方页面展示用户级 `~/.codex/config.toml`、项目 `.codex/config.toml` 与项目信任说明；来源：[OpenAI Config basics](https://developers.openai.com/codex/config-file/config-basic)，OpenAI Developers，2026-08-27；Playwright 真实浏览器截图，`verified-direct`。
- `02-openai-config-advanced.png`：Profile、项目层和临时覆盖；1280×720；证明独立 Profile 文件、`--profile` 选择方式和顶层配置键写法；来源：[OpenAI Advanced Configuration](https://developers.openai.com/codex/config-file/config-advanced)，OpenAI Developers，2026-08-27；Playwright 真实浏览器截图，`verified-direct`。
- `03-openai-config-reference.png`：常用字段与项目层限制；1280×720；证明项目层禁用键、配置参考入口和 `requirements.toml` 关联；来源：[OpenAI Configuration Reference](https://developers.openai.com/codex/config-file/config-reference)，OpenAI Developers，2026-08-27；Playwright 真实浏览器截图，`verified-direct`。
- `04-ai-config-precedence.png`：生效优先级；1672×941；AI 生成的配置层级教学示意图，非官方界面；依据 OpenAI Config basics 绘制，发布时须保留“AI 示意图”标注。
- `05-ai-config-troubleshooting.png`：配置不生效的排查顺序；1774×887；AI 生成的 PATH、TRUST、TOML、OVERRIDE、RELOAD 流程示意图，非官方界面；依据 OpenAI Configuration Reference 绘制，发布时须保留“AI 示意图”标注。

### 视频教程来源（仅作来源，不自动作为配图）

本轮未采用视频截帧。没有把视频封面、缩略图或裸链接列为图片候选。

### 需要作者亲自截图

- [x] `01-config-paths-and-version.png`：当前 Windows Terminal/PowerShell → `.\manual\prepare-windows-capture.ps1 baseline`；证明实际 `CODEX_HOME`、CLI 版本和 `config.toml` 是否存在；隐藏用户名、完整用户路径和账号信息；停在命令输出处。
- [x] `02-status-readonly-probe.png`：当前 Windows Terminal/PowerShell → `.\manual\prepare-windows-capture.ps1 readonly`；证明 `read-only` 下读取允许、写入拒绝；隐藏临时目录、账号、环境变量和令牌；停在探针结果处。

### 查找记录

- 官方网页：配置基础、高级配置、配置参考、审批与安全；Jina Reader `verified-direct`，Playwright 三张截图已保存到 `online/` 并目检通过。
- Bilibili：`Codex config.toml 配置 排查`；B站搜索 API 可用，但本轮未发现需要截取的当前 CLI 操作画面，`no-qualified-result`。
- YouTube：`Codex config.toml configuration troubleshooting`；`yt-dlp` 可用，但本轮未保存视频帧，`no-qualified-result`。
- X / 小红书：doctor 显示无 active backend，未声称直接搜索，`unavailable`。
