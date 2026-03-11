---
name: gws-doc-review-sync
---

## Purpose

Use this skill when Markdown is the source of truth and Google Docs is the review surface.

## Supported Modes

- `gdoc-bootstrap`
- `gdoc-publish`
- `gdoc-comment-intake`
- `gdoc-apply-feedback`
- `gdoc-reply-resolve`
- `gdoc-status`

## Router

1. Resolve the review-sync intent.
2. Use the matching reference:
   - `gdoc-bootstrap` -> `references/bootstrap.md`
   - `gdoc-publish` -> `references/publish.md`
   - `gdoc-comment-intake` -> `references/comment-intake.md`
   - `gdoc-apply-feedback` -> `references/apply-feedback.md`
   - `gdoc-reply-resolve` -> `references/resolve.md`
   - `gdoc-status` -> `references/status.md`
3. Treat Markdown as canonical and Google Docs as the review surface.

## Review Contract

- Store both `gdoc_id` and full `gdoc_url` in frontmatter.
- If multiple `.md` files live in one directory, treat one note as `main` and sibling notes as tabs in the same Google Doc.
- Apply accepted feedback in Markdown, then reply and resolve the corresponding Google Docs threads.

## Supporting Files

- Overview: `README.md`
- Examples:
  - `examples/gdoc-source-note.md`
  - `examples/gdoc-tab-note.md`
