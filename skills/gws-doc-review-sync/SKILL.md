---
name: gws-doc-review-sync
---

## Purpose

Use this skill for Markdown-first Google Docs review workflows plus one-way export of Google Docs into Markdown for AI review.

## Supported Modes

- `gdoc-bootstrap`
- `gdoc-publish`
- `gdoc-comment-intake`
- `gdoc-apply-feedback`
- `gdoc-reply-resolve`
- `gdoc-status`
- `gdoc-export-md`
- `gdoc-review-context`

## Router

1. Resolve the review intent.
2. Use the matching reference:
   - `gdoc-bootstrap` -> `references/bootstrap.md`
   - `gdoc-publish` -> `references/publish.md`
   - `gdoc-comment-intake` -> `references/comment-intake.md`
   - `gdoc-apply-feedback` -> `references/apply-feedback.md`
   - `gdoc-reply-resolve` -> `references/resolve.md`
   - `gdoc-status` -> `references/status.md`
   - `gdoc-export-md` -> `references/export-md.md`
   - `gdoc-review-context` -> `references/review-context.md`
3. Treat exported Markdown as a read-only mirror when the source lives in Google Docs.

## Review Contract

- Store both `gdoc_id` and full `gdoc_url` in frontmatter.
- Markdown-authored review bundles may publish sibling `.md` files as tabs in one Google Doc.
- Apply accepted feedback in Markdown, then reply and resolve the corresponding Google Docs threads.
- For Docs-authored reference docs, export the whole Google Doc to one Markdown file with provenance metadata.
- Treat exported Markdown mirrors as read-only reference material.

## Supporting Files

- Overview: `README.md`
- Helper:
  - `scripts/export_gdoc_markdown.py`
- Examples:
  - `examples/gdoc-source-note.md`
  - `examples/gdoc-tab-note.md`
  - `examples/gdoc-reference-note.md`
