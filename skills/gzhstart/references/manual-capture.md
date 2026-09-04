# Manual Capture Guide

For every user-operated screen, provide:

1. Starting URL.
2. Exact menu path using the labels currently visible to the user.
3. Expected screen and the single fact it should prove.
4. Proposed filename with a numeric prefix.
5. Sensitive fields to hide or leave empty.
6. A stop point before any irreversible action.

## WeChat Official Account Baseline

Use `https://mp.weixin.qq.com/` and ask the user to capture, when relevant:

1. Public homepage and account-type area without the live login QR code.
2. Registration account-type selection.
3. Email activation fields while empty.
4. Subject type selection and required-material labels.
5. Account information fields while empty.
6. Logged-in dashboard navigation with account statistics hidden.
7. New article entry and the full editor layout.
8. Cover selection/crop view without private media.
9. Original/repost and comment settings.
10. Preview entry without recipient identifiers.
11. Publish or mass-send settings before confirmation.
12. Saved draft or completion state.

Never ask the user to capture a usable QR code, verification code, Cookie, AppID/AppSecret, administrator identity, phone, email, payment, recipient, or reader record.

## First Draft Focus

For an article specifically about creating and saving the first draft, reduce the capture set to:

1. `01-dashboard-new-content-entry.png`: dashboard with account identity and metrics hidden.
2. `02-article-editor-empty-layout.png`: empty editor layout.
3. `03-article-editor-sample-content.png`: non-sensitive sample title and body.
4. `04-cover-selection-empty.png`: cover selection using a disposable public test image.
5. `05-article-settings.png`: current original/repost/comment settings.
6. `06-save-draft-action.png`: save-draft action before clicking.
7. `07-draft-saved-state.png`: successful save state; stop before preview, mass send, or publish.
