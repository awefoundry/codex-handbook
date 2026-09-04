# Platform Playbook

## Query Matrix

Create queries for four lanes:

| Lane | Goal | Typical query |
|---|---|---|
| Official | Confirm facts and obtain canonical UI | `site:vendor.com product feature screenshot` |
| Web | Find announcements and indexed social URLs | `product feature IDE UI` |
| Video | Find demonstrations and timestamps | `product feature tutorial official` |
| Community | Find real usage and edge cases | `site:reddit.com product feature`, `site:x.com product feature` |

Use both English and the article language when the audience or ecosystem warrants it.

## Video Procedure

1. Read title, uploader, upload date, duration, description, and thumbnail.
2. Prefer the official upload over a repost.
3. Download a temporary video no larger than 1080p.
4. Generate a contact sheet at 30–60 second intervals.
5. Visually choose useful ranges, then extract exact full-resolution frames.
6. Save the timestamp in the article appendix and manifest.
7. Remove the temporary video after the selected frames are verified.

When mixing images with different aspect ratios in a contact sheet, constrain both width and height and pad the result. Never crop UI merely to make the grid uniform.

## Failure Recording

Record the platform, attempted backend, error class, fallback, and final coverage. Common honest outcomes include:

- login backend unavailable: report not searched directly;
- rate limit or anti-bot response: use indexed results only and label them as such;
- result found but source cannot be opened: do not download or cite it;
- only a repost exists: keep it as an annotated viewing link, not product evidence.

## Selection Rules

Choose an image only if it answers at least one question a reader will have at that point in the article: where to click, what state to expect, what changed, or how success/failure looks. Reject decorative images that do not help complete the workflow.
