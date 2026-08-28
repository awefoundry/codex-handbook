param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('baseline', 'readonly')]
    [string]$Mode
)

$ErrorActionPreference = 'Stop'

$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codexCommand) {
    Write-Error 'ERROR=codex-not-found'
    exit 1
}

$configRoot = if ($env:CODEX_HOME) {
    $env:CODEX_HOME
} else {
    Join-Path $env:USERPROFILE '.codex'
}

$displayRoot = $configRoot
if ($env:USERPROFILE) {
    $displayRoot = $displayRoot.Replace($env:USERPROFILE, '~')
}

switch ($Mode) {
    'baseline' {
        Write-Output "CODEX_HOME=$displayRoot"
        codex --version
        if (Test-Path -LiteralPath (Join-Path $configRoot 'config.toml')) {
            Write-Output 'config.toml=present'
        } else {
            Write-Output 'config.toml=missing'
        }
    }
    'readonly' {
        $probeRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('codex-config-probe-' + [guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $probeRoot | Out-Null
        Set-Content -LiteralPath (Join-Path $probeRoot 'probe.txt') -Value 'read-ok' -NoNewline
        try {
            $previousErrorActionPreference = $ErrorActionPreference
            $ErrorActionPreference = 'Continue'
            try {
                $probeOutput = & codex exec --ephemeral `
                    --sandbox read-only `
                    --skip-git-repo-check `
                    -C $probeRoot `
                    'This is a disposable read-only probe. Read only probe.txt, then attempt once to create write-probe.txt containing write-ok. If the write is blocked, do not retry. Do not inspect parent directories, credentials, environment variables, network, or any other path. End with exactly two lines: READ=ALLOWED or READ=DENIED, and WRITE=ALLOWED or WRITE=DENIED.' 2>&1 | Out-String
            } finally {
                $ErrorActionPreference = $previousErrorActionPreference
            }
            $readResult = if ($probeOutput -match '(?m)^READ=ALLOWED\s*$') { 'ALLOWED' } elseif ($probeOutput -match '(?m)^READ=DENIED\s*$') { 'DENIED' } else { 'UNKNOWN' }
            $writeResult = if ($probeOutput -match '(?m)^WRITE=ALLOWED\s*$') { 'ALLOWED' } elseif ($probeOutput -match '(?m)^WRITE=DENIED\s*$') { 'DENIED' } else { 'UNKNOWN' }
            Write-Output 'sandbox=read-only'
            Write-Output "READ=$readResult"
            Write-Output "WRITE=$writeResult"
        } finally {
            Remove-Item -LiteralPath $probeRoot -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}
