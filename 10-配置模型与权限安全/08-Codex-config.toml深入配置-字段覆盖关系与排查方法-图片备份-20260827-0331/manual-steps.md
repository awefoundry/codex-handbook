# Windows 本机截图准备与操作步骤

本文不要求登录、注册或发布。当前电脑只需要一个已经可运行 `codex` 的 PowerShell；脚本不会修改真实 `config.toml`，也不会打印配置内容。

## 先准备终端环境

1. 打开一个新的 Windows Terminal 或 PowerShell 窗口，进入文章工作区：

   ```powershell
   Set-Location 'D:\codexguide_all\教程\10-配置模型与权限安全\08-Codex-config.toml深入配置-字段覆盖关系与排查方法-图片备份-20260827-0331'
   Get-Command codex
   codex --version
   ```

2. 为了不让终端提示符显示用户名或目录，在同一个窗口执行：

   ```powershell
   function prompt { 'capture$ ' }
   ```

3. 若 `Get-Command codex` 或 `codex --version` 失败，停止截图，先确认 Codex CLI 能在该终端运行。不要为了截图临时修改真实配置或复制凭据。

4. Windows 截图方式：每次命令输出完成后按 `Win-Shift-S`，选择矩形截图，只框选终端内容区域；截图后在右下角通知中打开截图并保存到指定文件。不要截取桌面、浏览器登录页、完整用户路径或其他窗口。

## 截图 1：配置路径与 CLI 版本

运行：

```powershell
.\manual\prepare-windows-capture.ps1 baseline
```

截图文件：`manual/01-config-paths-and-version.png`

应保留：`CODEX_HOME=~/.codex`（或脱敏后的自定义目录）、`codex-cli` 版本和 `config.toml=present/missing`。

应隐藏：用户名、完整 home 路径、账号信息、机器名和任何配置文件内容。

停止位置：看到三项结果后停止，不要执行 `Get-Content .codex\config.toml`。

## 截图 2：read-only 沙箱探针

运行：

```powershell
.\manual\prepare-windows-capture.ps1 readonly
```

脚本会在 Windows 临时目录创建一次性目录，写入无敏感内容的 `probe.txt`，随后调用：

```text
codex exec --ephemeral --sandbox read-only --ask-for-approval on-request
```

截图文件：`manual/02-status-readonly-probe.png`

应保留：脚本输出的 `sandbox=read-only`、`READ=ALLOWED` 与 `WRITE=DENIED`。修订后的脚本已把 Codex 的 session ID、临时目录、网络日志和 provider 输出收起，不需要手动截取这些内容。

应隐藏：临时目录完整路径、用户名、账号、环境变量、日志路径和任何令牌。

停止位置：脚本输出两项结果后停止。脚本退出时会清理临时目录，不要手动删除其他目录。

## 截图完成后的本机检查

```powershell
$workspace = 'D:\codexguide_all\教程\10-配置模型与权限安全\08-Codex-config.toml深入配置-字段覆盖关系与排查方法-图片备份-20260827-0331'
python 'D:\CodexHome\skills\gzhstart\scripts\validate_gzh_workspace.py' $workspace
$staging = Join-Path $env:TEMP ('codex-manifest-assets-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $staging | Out-Null
Copy-Item (Join-Path $workspace 'online\*.png') $staging
Copy-Item (Join-Path $workspace 'manual\*.png') $staging
try {
  python 'D:\CodexHome\skills\research-article-visuals\scripts\validate_manifest.py' `
    (Join-Path $workspace 'manifest.tsv') `
    --asset-dir $staging
} finally {
  Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
}
```

当前电脑无需执行 Mac 路径命令。截图完成后只需把两张 PNG 保存在 `manual/`；上面的临时目录只用于合并校验，脚本结束会自动清理。主机端还会检查敏感信息，再登记 `manifest.tsv` 的 `manual` 来源。
