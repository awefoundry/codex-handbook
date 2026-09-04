# Platform Routing

## Search Order

1. Official website, help center, developer docs, and platform-owned tutorials.
2. Exa or another configured web index for discovery.
3. YouTube through `yt-dlp` for metadata, subtitles, contact sheets, and precise frames.
4. Bilibili through its configured Agent Reach backend or public metadata endpoint. Do not use `yt-dlp` for Bilibili.
5. X, Xiaohongshu, Reddit, Instagram, or Facebook through the active backend reported by `agent-reach doctor --json`.
6. Public web indexing only when a login backend is unavailable; label this `verified-index` or weaker.

## Playwright

Use the Playwright skill's wrapper when Bash is available. On Windows without Bash, use:

```powershell
npx --yes --package @playwright/cli playwright-cli -s=<session> open <url>
npx --yes --package @playwright/cli playwright-cli -s=<session> snapshot
npx --yes --package @playwright/cli playwright-cli -s=<session> screenshot
```

Always snapshot before interacting and after navigation. Inspect the saved screenshot before accepting it. Delete captures containing login QR codes, tokens, personal details, or irrelevant login overlays.

## Windows Exa Calls

Prefer named arguments to inline JSON, which is fragile under PowerShell quoting:

```powershell
mcporter call exa.web_search_exa query="QUERY" numResults=10 --output json
```

## Failure Log

Record platform, query, backend, timestamp, error class, fallback, verification depth, and citation decision. A 412, login wall, or missing backend is not successful direct coverage.
