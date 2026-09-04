---
name: gzhstart
description: Initialize a WeChat Official Account article workspace before writing. Use when starting a 公众号/微信公众号 article or tutorial and needing a reproducible environment/version baseline, screenshot inbox, multi-platform tutorial research, verified visual sources, user-operated screenshot steps, source manifests, and a backup-material appendix added to the article end. Coordinates research-article-visuals, agent-reach, and Playwright while keeping registration, login, authentication, payment, preview recipients, and final publishing under user control.
---

# gzhstart

Prepare the article workspace and evidence library before drafting. Hand the initialized article to `gzhwz` only after the writing and screenshot collection stages are complete.

## Required Inputs

Accept either an existing Markdown article path or a topic plus destination directory. If only a topic is supplied, create the research workspace but do not invent an article filename unless the user asks.

## Workspace Location

- When an article path exists, create the backup workspace beside the article as `<article-stem>-图片备份-<timestamp>/`. For example, `08-插件工作流/1.notion.md` maps to `08-插件工作流/1.notion-图片备份-20260813-1015/`.
- Before creating it, scan the article directory for `<article-stem>-图片备份-*` and `<article-stem>-图片备份`. If one or more matching directories already exist, reuse the newest name-sorted directory. Do not create another workspace or overwrite its contents. If a reused legacy workspace lacks `environment.md`, add only that missing template and then fill it.
- Never place an article's backup workspace in a repository-level or shared `图片备份/` directory.
- When only a topic is supplied, create the workspace inside the explicitly requested destination directory as `<slug>-图片备份-<timestamp>/`.
- Keep `manual/`, `online/`, manifests, and research notes inside that one workspace.
- Treat the Markdown article's parent directory as the default and exclusive screenshot search scope. Search that directory and its article-specific backup folders first; do not scan repository-level `图片备份/` folders or generic folders such as `gzhstart-公众号初始化截图`.
- Never copy a screenshot from another article's directory merely because it looks similar. Import outside the article directory only when the user explicitly names the source and the image is verified against the current article step.
- Treat `created<TAB><absolute-path>` as a newly initialized workspace and `existing<TAB><absolute-path>` as a reused workspace. Continue research in the returned directory in both cases.

## Workflow

1. Read the article or topic and identify the exact workflow being taught.
2. Run `scripts/init_gzh_workspace.py --article <article.md>` for an existing article. It reuses an existing adjacent backup workspace when found; otherwise it creates one. Use `scripts/init_gzh_workspace.py <destination> --slug <slug>` only for a topic without an article. A new workspace contains `manual/`, `online/`, `environment.md`, `manifest.tsv`, `manual-steps.md`, and `research-log.md`.
3. Scan the article parent directory for existing screenshots and article-specific backup folders. Reject unrelated topic folders before copying anything into `manual/` or `online/`.
4. Collect the tutorial environment and version baseline before researching screenshots. Record the operating system/build, IDE or host application, Codex surface and version, target plugin/app/connector version, and other workflow-critical dependencies. Put one reader-facing `> 测试环境：...` summary near the article beginning and retain the complete acquisition details in `environment.md`.
5. Read and follow `$research-article-visuals`. Create a visual-evidence matrix for every major article step.
6. Read and follow `$agent-reach`. Run `agent-reach doctor --json` before searching X, Xiaohongshu, Bilibili, YouTube, or other multi-backend platforms.
7. Search official sources first, then Bilibili/Xiaohongshu tutorials, then other community sources for current UI or real-world workflows. Use both Chinese and English queries where useful. For this skill, prioritize real computer-operation evidence over promotional material.
8. Use `$playwright` for publicly accessible pages. Snapshot after every navigation and inspect each screenshot. Never retain QR codes, cookies, tokens, private account data, or login-only screenshots as article material.
9. For pages requiring login, registration, identity verification, payment, administrator confirmation, preview recipients, or publishing, stop automation and write numbered user steps in `manual-steps.md`.
10. Download or extract only traceable candidates. Record source, author, date, dimensions, intended section, verification depth, and expiry risk in `manifest.tsv`. A candidate must show a real application, terminal, settings page, editor, or other task-relevant UI state that supports a specific article step.
11. Append the section from [references/article-appendix-template.md](references/article-appendix-template.md) to the article end. Mark it as backup material excluded from published figure numbering.
12. Validate the workspace with `scripts/validate_gzh_workspace.py`. Report the screenshot inbox as an absolute clickable path.

## Environment Baseline

Add one compact blockquote near the beginning of every tutorial. Do not add a heading or a reader-facing environment table. Use this pattern:

```markdown
> 测试环境：Windows 11 24H2；Codex Desktop 26.803.10989.0；Codex CLI 0.146.1；2026-08-14 核验。
```

- Include only components that affect the UI or behavior demonstrated in the tutorial: the relevant operating system when needed, the actual host or execution surface, workflow-critical plugin/app/connector versions, and the verification date.
- Omit acquisition methods, notes, `不适用` entries, background processing tools, and components that the tutorial does not use. Do not list IDE or CLI merely to say that they are not applicable.
- Keep the summary on one Markdown line. If several versions are needed, separate them with Chinese semicolons instead of expanding it into a table or list.
- Prefer locally observed versions from About screens, package metadata, or `--version`; use official release pages when the tutorial is not tied to the local machine.
- For a managed plugin, connector, or continuously deployed web service with no exposed version, name the surface and give the verification date without inventing a semantic version.
- Save the complete baseline, acquisition method, commands, applicability notes, and evidence in `environment.md`. Do not include tokens, account identifiers, license keys, or private workspace names.

## Source Rules

Use this visual-evidence priority:

1. A fresh screenshot of the real operation captured by the author on the target computer or app.
2. A screenshot of the real operation interface from an official tutorial, help center, or official product video.
3. A frame extracted from an original Bilibili or Xiaohongshu tutorial video that visibly shows the operation, with the exact timestamp recorded.
4. A frame extracted from another reputable tutorial only when it shows the required UI state and no higher-priority source is available.
5. A community screenshot with clear authorship and traceable provenance, only as a fallback.

Hard exclusions:

- Do not use video covers, thumbnails, title cards, channel avatars, logos, or promotional banners as article step images.
- Do not add a plain video URL or a video cover to `manifest.tsv` as an image candidate. A URL may be recorded in `research-log.md` as an optional viewing reference.
- Official brand icons are decorative only; they do not prove a workflow step and must not replace an operation screenshot.
- If a frame does not show the relevant menu, dialog, command output, or result state, reject it even when the video itself is authoritative.

For extracted video frames, record platform, video ID, author, publication date, exact timestamp, frame filename, and the single UI fact the frame proves. Prefer Bilibili and Xiaohongshu for Chinese tutorials, and use their active Agent Reach backend or platform-native tooling; never infer the frame content from a title or thumbnail.

Treat old official screenshots as historical references when the source warns that content may be outdated. Require fresh user screenshots for current login-only UI.

## Platform Coverage

Read [references/platform-routing.md](references/platform-routing.md). Record every requested platform as one of:

- `verified-direct`: opened the original source and verified content;
- `verified-index`: verified metadata through an index/API but could not open the platform page;
- `found-unverified`: discovered a lead but could not verify it;
- `unavailable`: no authenticated backend or blocked by platform controls;
- `no-qualified-result`: searched successfully but found nothing suitable.

Never state that X or Xiaohongshu was searched directly when only a public search index was used.

## User-Operated Screenshots

Read [references/manual-capture.md](references/manual-capture.md). Give the user exact navigation, the expected screen, the proposed filename, what to hide, and where to stop. Do not tell the user to expose QR codes, account identifiers, AppSecret, verification codes, reader data, or payment details.

Do not perform final registration, certification, payment, binding, mass send, publishing, deletion, or irreversible settings changes.

## Article Appendix

Append candidates only when an article path exists. Include:

- selected filenames and intended sections;
- tutorial links with author/platform/date, while keeping links separate from image candidates;
- for video frames, exact timestamps and the UI fact each frame proves;
- provenance and time-sensitive warnings;
- platforms attempted and verification depth;
- a separate checklist of screenshots the user still needs to capture.

Do not insert candidates into the main figure sequence. The author chooses and moves them later.

## Handoff

After the user finishes screenshots and the article draft exists, use `gzhwz` for prose refinement, per-image `imagegzh` processing, final numbering, CTA, and publishing checks. Keep `gzhstart` focused on initialization and research.

## Completion Gate

Report completion only when:

- the screenshot inbox and templates exist;
- `environment.md` exists and the article contains a filled one-line `> 测试环境：...` summary;
- versions affecting the workflow have an acquisition method and verification date in `environment.md`; unknown values are labeled honestly and inapplicable components are omitted from the reader-facing summary;
- requested platforms have honest coverage statuses;
- every saved image opens and has a source record;
- every saved article candidate is a real operation screenshot or a verified operation frame; no video cover, thumbnail, or bare video link is accepted as a candidate;
- invalid login/QR/private screenshots are removed;
- user-only steps include filenames and redaction guidance;
- the article appendix is appended when an article path was supplied;
- `validate_gzh_workspace.py` passes.
