---
name: green-series-cover
description: Generate Chinese green-series article covers from a fixed mint-green reference composition, adapting the left information panel to a supplied title and issue number. Use when creating, revising, or batch-generating this publication's green WeChat public-account cover series with HiAPI image2.0.
---

# Green Series Cover

Use the bundled reference image as the visual source of truth. Keep the right-side laptop, floating terminal panels, mint/white background, lighting, perspective, and overall 16:9 composition stable. Rebuild only the left information area for the requested article.

## Required input

Before generating, ask for both values if they were not supplied:

- `title`: the article title, in Chinese when appropriate.
- `issue`: the series issue number, a positive integer.

Do not silently invent either value. Preserve the user's title verbatim in the prompt; do not rewrite its wording. If the title is long, request a shorter display title or use a deliberate two-line layout rather than shrinking it until unreadable.

## Generate

Run the bundled script from the skill directory:

```powershell
node scripts/generate-cover.mjs --title "Windows 安装 Codex" --issue 1 --output .\cover.png
```

The script reads `HIAPI_API_KEY` from the current environment, uses `gpt-image-2/image-to-image` by default, encodes `assets/reference-cover.png` as a data URL, submits an asynchronous HiAPI task, polls it, and downloads the first output. Never print or commit the API key. Override the reference with `--reference <path>` only when the user explicitly supplies a replacement.

The generated prompt must require:

- exact visible issue badge text `系列第 <issue> 篇`;
- the supplied title as the dominant left headline;
- a left-side illustration or motif that reflects the article topic;
- no extra logos, watermark, QR code, invented claims, or unrelated text;
- preservation of the reference's right-side laptop/terminal scene and its mint, white, blue, and teal palette.

If HiAPI returns a task failure, report the returned error and do not present a partial file as final. After success, inspect the downloaded image for title/issue legibility and accidental text or layout drift; retry with a more constrained prompt when necessary.

## Output convention

Prefer a deterministic output path supplied by the user. Otherwise write `green-series-cover-<issue>.png` in the current directory. Keep the original reference asset unchanged. Return the output path and HiAPI task ID, but never expose credentials.
