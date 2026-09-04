---
name: research-article-visuals
description: Research, verify, download, extract, and document traceable visual sources for tutorials and articles. Use when an article needs screenshots, social posts, video frames, product UI evidence, source attribution, or a reusable visual-material appendix gathered from official sites, search engines, YouTube, Bilibili, X, Reddit, Xiaohongshu, Instagram, or similar platforms.
---

# Research Article Visuals

Build a source-backed visual library before writing or illustrating an article. Prefer useful evidence over a large pile of loosely related images.

## Workflow

1. Read the target article and list the claims or steps that need visual support.
2. Write a query matrix before searching. Cover official sources, general web search, video platforms, and relevant social/community platforms.
3. Use the available internet-routing skill or platform tools. Run their health check first when a platform depends on login state or multiple backends.
4. Search official sources first, then use social posts and videos for real-world UI, workflows, reactions, or examples not present in official material.
5. Verify each candidate by opening its source or reading structured metadata. Do not accept a result solely from its title or search snippet.
6. For video, inspect metadata and subtitles when useful, make a coarse contact sheet, then extract only precise frames that add information.
7. Inspect every downloaded image. Reject transition frames, illegible UI, misleading crops, generic thumbnails, and duplicates.
8. Append a clearly marked backup section to the article. Keep candidates out of the published figure numbering until selected.
9. Run `scripts/validate_manifest.py` against the tab-separated manifest before reporting completion.

## Source Priority

Use this order unless the article explicitly needs community sentiment:

1. Official documentation, product blog, release notes, or official media account.
2. Original creator or first-party event/video recording.
3. Reputable third-party tutorial with visible, current UI.
4. Community post with a stable URL and clear authorship.
5. Repost, compilation, or search thumbnail only as an annotated viewing link.

Never label a repost, fan upload, or marketplace asset as an official product interface.

## Search And Fallbacks

Read [references/platform-playbook.md](references/platform-playbook.md) before multi-platform work. Record unavailable platforms and the reason. Do not imply coverage when authentication or rate limits prevented verification.

When an API returns anti-bot errors, use the documented fallback chain: platform CLI, indexed web search, then a stable known URL. Do not bypass authentication or scrape private sessions.

## Image Handling

- Preserve PNG for UI screenshots when text clarity matters.
- Use high-quality JPG/WebP for photographic video frames.
- Keep the original aspect ratio and at least 1000 px width for full-width tutorial images when the source permits.
- Name files with the article number, source, and purpose, for example `image-11-jetbrains-agent-picker.png`.
- Store temporary videos, subtitles, and contact sheets outside the repository. Keep only selected output frames.

## Backup Section Format

For each candidate, record filename, dimensions, intended section, what the image proves, source URL, author/account, publication date, and video timestamp if applicable. Add an expiry warning for promotions, pricing, beta labels, or rapidly changing UI.

Use [references/manifest-template.tsv](references/manifest-template.tsv) as the manifest header and field example.

## Completion Gate

Report success only when:

- each saved file opens and is visually legible;
- each item has a stable source URL and intended use;
- official and third-party provenance is labeled accurately;
- unavailable channels and failed fallbacks are recorded;
- the article backup section matches the files on disk;
- the manifest validator passes.
