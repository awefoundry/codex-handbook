# Codex config.toml配置指南：最小配置、生效检查与常见问题

`config.toml` 适合保存稳定的运行偏好，例如默认审批策略、沙箱模式和推理强度。它不应被当成“把所有开关抄一遍”的总配置，也不应成为绕过审批或扩大权限的捷径。

本文保留原文的配置来源、覆盖关系、只读探针和回滚思路，改成一套更小的可操作流程。示例使用独立的 `CODEX_HOME` 和临时项目，不会改写维护者的 `~/.codex`，也不包含凭据。

## 什么时候需要配置

如果默认设置已经能完成任务，可以先不创建或修改 `config.toml`。只有在下面情况出现时，再考虑写配置：

- 每次任务都要重复选择同一个审批或沙箱边界；
- 个人默认模型或推理强度需要固定；
- 某个项目需要一个经过审查的最低安全基线；
- 需要用 Profile 把审查、日常开发和 CI 的偏好分开。

一次性实验优先用命令行参数或 `-c/--config` 覆盖，确认行为后再决定是否落到文件。不要为了“自动化方便”把 `danger-full-access`、`approval_policy = "never"` 或真实密钥写成默认入门配置。

## 配置从哪里来

根据 [OpenAI Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) 和 [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)（核对日期：**2026-09-22**），常见来源如下：

| 层级 | 位置或入口 | 适用范围 |
| --- | --- | --- |
| 命令行 | 专用参数、`-c/--config` | 只影响当前命令，优先级最高 |
| 项目 | 项目根到当前目录的 `.codex/config.toml` | 仅在项目受信任时加载，越靠近当前目录越优先 |
| Profile | `CODEX_HOME/<name>.config.toml`，用 `--profile <name>` 选择 | 在用户配置之上叠加一组差异值 |
| 用户 | `~/.codex/config.toml`，或 `CODEX_HOME` 指定的目录 | 个人默认值 |
| 工作区托管 | 登录工作区下发的配置 | 可能提供组织默认值 |
| 系统 | Unix 常见为 `/etc/codex/config.toml` | 管理员提供的系统默认值 |
| 内置默认 | Codex 自带 | 前面没有值时使用 |

Codex 按键解析这些层级，而不是简单地用高层文件替换低层文件。项目未受信任时，项目级 `.codex/` 层会被跳过；管理员还可以通过 `requirements.toml` 强制限制某些值，本地文件不能把它放宽。

## 一份最小、保守的配置

下面只固定三个容易解释的字段：

```toml
# $CODEX_HOME/config.toml 或 ~/.codex/config.toml
approval_policy = "on-request"
sandbox_mode = "read-only"
model_reasoning_effort = "medium"
```

- `approval_policy = "on-request"`：需要时暂停并等待确认。它控制询问时机，不等于授予额外权限。
- `sandbox_mode = "read-only"`：命令只能在只读边界内工作，适合先调查项目。要修改文件时，在当前命令显式选择合适的工作区策略，并在完成后恢复。
- `model_reasoning_effort = "medium"`：对支持该字段的模型调整推理投入；模型是否支持某个值要以当前入口和官方参考为准。

需要控制网页搜索时，可以单独增加：

```toml
web_search = "cached"
```

`cached` 使用搜索缓存；`indexed`、`live` 和 `disabled` 是其他官方列出的模式。网页结果仍是外部输入，不能把搜索结果当作可信指令。

## exec 与 interactive 怎么选

`exec` 适合一次性命令、脚本和 CI；interactive 适合调查、修改和需要持续确认的任务。两者都要留下完成证据：前者看退出码、输出和测试，后者看 diff、测试和人工检查。入口和参数会随版本变化，先运行当前 `codex --help`，不要把旧教程的选项直接复制进脚本。

## sandbox、permissions 与 approval policy

`sandbox_mode` 规定命令执行时的访问边界，权限配置描述允许触碰的资源，`approval_policy` 决定何时暂停询问。它们不是一个开关。遇到拒绝时先看路径、当前工作目录和实际参数，再决定是否需要批准；不要用扩大权限掩盖路径或配置错误。具体边界可继续查看[权限与安全边界](./08-Codex沙箱与主机权限风险.md)和 [CodexGuide 权限与验证 FAQ](https://codexguide.io/guides/faq#permissions)。

## slash commands 速查

斜杠命令属于交互入口，具体可用项会随当前版本和入口变化。使用前先查看当前帮助；重复且稳定的项目约定沉淀到 `AGENTS.md`，重复流程再考虑 Skill。命令完成后仍要检查 diff 和验证结果。

项目级配置只放团队愿意共享的最低边界，例如：

```toml
# <repo>/.codex/config.toml
sandbox_mode = "read-only"
```

不要把 API Key、代理密码、个人路径、`auth.json` 或账号信息放进仓库。项目配置是否加载还取决于项目是否受信任。

## 用隔离目录检查配置语法

先创建一个临时配置目录，不碰真实用户配置：

```bash
probe_home="$(mktemp -d /tmp/codex-config-home.XXXXXX)"
probe_project="$(mktemp -d /tmp/codex-config-project.XXXXXX)"
mkdir -p "$probe_home" "$probe_project"

cat > "$probe_home/config.toml" <<'TOML'
approval_policy = "on-request"
sandbox_mode = "read-only"
model_reasoning_effort = "medium"
TOML

CODEX_HOME="$probe_home" codex --version
CODEX_HOME="$probe_home" codex exec --help
```

正常应显示当前 CLI 版本和帮助文本；这只能证明文件能被读取到帮助命令，不代表已完成模型调用。本轮（2026-09-23）维护环境实际核对到的是 `codex-cli 0.156.0`。

需要严格检查未知字段时，在真正执行的子命令上加 `--strict-config`：

```bash
CODEX_HOME="$probe_home" codex exec --strict-config --ephemeral \
  --skip-git-repo-check -C "$probe_project" \
  "只读检查当前目录并说明配置来源；不要修改文件。"
```

如果字段名称、类型或 TOML 语法有问题，先修复配置错误；如果随后停在登录、网络或模型连接，则说明配置解析已经走过，但本次行为验证没有完成。不要把网络失败写成“配置生效”。

本轮在 Codex CLI 0.156.0 的隔离探针中，合法配置通过了解析，未知字段被 `--strict-config` 拒绝；发起模型请求前的启动摘要显示 `approval: never`，随后因网络无法连接而中断。因此不能据此确认 `approval_policy = "on-request"` 在 `exec` 入口的最终生效方式。需要对照命令级审批时，把全局参数放在子命令前，例如 `codex --ask-for-approval on-request exec ...`；不要把 `--ask-for-approval` 直接放在 `codex exec` 后面。

## 先用临时覆盖，再写入文件

验证某一个字段时，用 `-c` 临时覆盖：

```bash
CODEX_HOME="$probe_home" codex exec --ephemeral \
  --sandbox read-only -C "$probe_project" \
  -c 'model_reasoning_effort="low"' \
  "只读列出当前目录文件，不修改任何内容。"
```

专用参数和 `-c` 都只影响这次命令。若项目配置中把 `sandbox_mode` 写成 `workspace-write`，上面的 `--sandbox read-only` 仍然明确指定了当前命令的沙箱边界。命令是否能继续运行，还取决于认证、项目受信任状态和组织策略。

## 用最小行为探针检查实际结果

在临时项目写入一份无敏感信息的文件：

```bash
printf 'read-ok\n' > "$probe_project/probe.txt"
CODEX_HOME="$probe_home" codex exec --ephemeral --sandbox read-only \
  --skip-git-repo-check -C "$probe_project" \
  "读取 probe.txt，然后尝试创建 write-probe.txt；被拒绝时不要重试，分别报告读取和写入结果。"
```

你要核对的是实际文件状态和命令输出：

```bash
cat "$probe_project/probe.txt"
if [ -e "$probe_project/write-probe.txt" ]; then echo 'WRITE=CREATED'; else echo 'WRITE=NOT_CREATED'; fi
```

预期是能读取 `probe.txt`，并且 `write-probe.txt` 没有创建。这个探针验证的是当前命令的只读沙箱行为，不证明所有模型、入口或项目配置都相同。没有登录或网络时，命令会在模型请求阶段失败，应把结果记录为“未完成行为验证”。

交互式会话可用当前客户端提供的状态命令或界面信息核对工作目录和权限；命令名会随版本变化，先运行 `codex --help` 或 `codex exec --help`，不要把旧教程中的菜单名称当成固定事实。

## “改了却没生效”的排查顺序

1. **路径**：在实际运行 Codex 的同一个终端中检查 `echo "$CODEX_HOME"`；确认文件名是 `config.toml`，不是 `config.toml.txt`。
2. **环境**：Windows、WSL 和 macOS/Linux 有各自的用户目录；不要在 Windows 文件夹里改完，却从 WSL 启动 Codex。
3. **项目信任**：确认项目已受信任。未受信任时，项目 `.codex/config.toml`、hooks 和规则会一起跳过。
4. **TOML**：检查引号、布尔值、表头和重复键；用 `--strict-config` 的实际执行命令捕获未知字段。
5. **字段和值**：对照[官方配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)和当前 `codex --help`，不要复制旧版本的字段、废弃值或模型名。
6. **覆盖顺序**：记录 CLI 参数、最近的项目配置、Profile、用户配置、托管/系统配置，逐项确认是谁提供了最终值。
7. **受管控约束**：管理员的 `requirements.toml` 不能由本地配置绕过；遇到被拒绝的值，应联系维护者确认允许范围。
8. **重新启动**：配置和项目规则通常在一次新运行开始时读取。结束当前会话，重新从目标目录启动后再做探针。

## 备份、恢复和清理

修改真实用户配置前先做备份；示例只展示命令形式，执行前确认路径：

```bash
codex_root="${CODEX_HOME:-$HOME/.codex}"
config_path="$codex_root/config.toml"
backup_path="$config_path.bak.$(date +%Y%m%d-%H%M%S)"
cp "$config_path" "$backup_path"
```

确认新配置有问题时，用备份恢复：

```bash
cp "$backup_path" "$config_path"
```

恢复后重新启动 Codex，再用只读探针确认行为。清理临时练习目录即可：

```bash
rm -rf "$probe_home" "$probe_project"
```

不要把备份、日志、`auth.json`、环境变量或真实用户路径提交到仓库。`approval_policy = "never"` 与 `danger-full-access` 会移除重要防线，只能在已经有外层隔离并经过专门审查的环境中讨论，不能作为新手默认值。

## 相关阅读与核对边界

- [OpenAI Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [OpenAI Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [OpenAI Config Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [OpenAI Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Codex AGENTS.md教程](./09-AGENTS.md怎么写-项目规则继承关系与验收标准.md)
- [权限、沙箱与审批](../02-核心概念与任务方法/06-权限沙箱与审批-什么时候放行什么时候收紧.md)

官方字段、配置层级和项目受信任条件于 2026-09-22 核对；本轮（2026-09-23）本地 CLI 版本为 0.156.0。实际模型调用、App/IDE 菜单、组织托管配置和浏览器展示没有在本轮完成验证，不能据此宣称已实测。
