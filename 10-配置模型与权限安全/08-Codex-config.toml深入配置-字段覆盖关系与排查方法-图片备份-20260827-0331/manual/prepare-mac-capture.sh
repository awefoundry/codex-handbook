#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: bash prepare-mac-capture.sh <baseline|readonly|override>' \
    '       Run from a clean terminal with PS1 set to capture$.'
}

redact_home() {
  printf '%s' "$1" | sed "s|^${HOME}|~|"
}

config_root="${CODEX_HOME:-${HOME}/.codex}"
command -v codex >/dev/null 2>&1 || {
  echo 'ERROR=codex-not-found' >&2
  exit 1
}

case "${1:-}" in
  baseline)
    echo "CODEX_HOME=$(redact_home "$config_root")"
    codex --version
    if [[ -f "${config_root}/config.toml" ]]; then
      echo 'config.toml=present'
    else
      echo 'config.toml=missing'
    fi
    ;;
  readonly)
    probe_root="$(mktemp -d "${TMPDIR:-/tmp}/codex-config-probe.XXXXXX")"
    trap 'rm -rf "$probe_root"' EXIT
    printf 'read-ok\n' > "${probe_root}/probe.txt"
    codex exec --ephemeral \
      --sandbox read-only \
      --skip-git-repo-check \
      -C "$probe_root" \
      'This is a disposable read-only probe. Read only probe.txt, then attempt once to create write-probe.txt containing write-ok. If the write is blocked, do not retry. Do not inspect parent directories, credentials, environment variables, network, or any other path. End with exactly two lines: READ=ALLOWED or READ=DENIED, and WRITE=ALLOWED or WRITE=DENIED.'
    ;;
  override)
    if [[ -f "${config_root}/review.config.toml" ]]; then
      echo 'review-profile=present'
      override_root="$(mktemp -d "${TMPDIR:-/tmp}/codex-config-override.XXXXXX")"
      trap 'rm -rf "$override_root"' EXIT
      codex exec --ephemeral \
        --profile review \
        --sandbox read-only \
        --skip-git-repo-check \
        -C "$override_root" \
        'Do not inspect files, credentials, environment variables, or network. End with exactly one line: CLI_SANDBOX=read-only.'
    else
      echo 'review-profile=missing'
      echo 'PROFILE=UNAVAILABLE'
      codex --sandbox read-only --help | sed -n '1,18p'
    fi
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
