# gws-doc-review-sync

This workflow supports Markdown-authored review docs and one-way export of Google-Docs-authored reference docs.

- Markdown can remain canonical when Google Docs is only the review surface.
- Google Docs can also be exported into Markdown when you need local AI-readable design context.
- Review comments are pulled from Google Docs and Drive.
- Accepted feedback is applied back to the original `.md` file only in Markdown-authored flows.
- Store the full Google Doc URL in source metadata.

For Markdown-authored review bundles, sibling `.md` files may still publish as tabs in the same Google Doc.

## Why

Some workflows draft specs in Markdown and review them in Google Docs.

Other workflows already keep designs in Google Docs, but still need those docs exported into Markdown so agents can read them during implementation and PR review.

## Required Frontmatter Attributes

Required attributes:

- `gdoc_id`: long-lived Google Doc file ID
- `gdoc_url`: full Google Doc URL

Recommended attributes for Markdown-authored source notes:

- `gdoc_source_of_truth: markdown`
- optional `gdoc_role: main|tab`
- optional `gdoc_tab_title`
- `gdoc_last_published_sha`
- `gdoc_last_published_at`
- `gdoc_last_comment_sync`

Recommended attributes for exported mirrors:

- `gdoc_source_of_truth: google-docs`
- `gdoc_revision_id`
- `gdoc_last_exported_at`

See `examples/gdoc-source-note.md` for a Markdown-authored note and `examples/gdoc-reference-note.md` for an exported mirror.

If you want one Markdown-authored note bundle to publish into one Google Doc with tabs, also see `examples/gdoc-tab-note.md`.

## Required Google Scopes

Minimum practical scopes for this workflow:

- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/drive`

Re-auth example:

```bash
gws auth logout
gws auth login --scopes "https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/drive"
gws auth status
```

If you want to preserve the current broad `gws-gtd` scope set and add Docs/Drive for this skill, use:

```bash
gws auth logout
gws auth login --scopes "email,openid,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts,https://www.googleapis.com/auth/contacts.other.readonly,https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.compose,https://www.googleapis.com/auth/gmail.insert,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email"
gws auth status
```

## Workflow

### Markdown-authored review flow

1. Add or initialize frontmatter on a Markdown note.
2. Create or link a long-lived Google Doc.
3. If sibling `.md` files should live in one review surface, treat one note as `main` and sibling notes as `tab` notes.
4. Publish Markdown content into the linked Doc.
4. Review in Google Docs using comments.
5. Pull open comments and map them back to source sections.
6. Update the original Markdown.
7. Reply to and resolve the corresponding Google Docs threads.

### Docs-authored export flow

1. Link a Google Doc.
2. Export the whole Doc to Markdown using Drive export `text/markdown`.
3. Store the exported Markdown with provenance metadata.
4. Use `gdoc-review-context` to gather current design docs for AI-assisted PR review.

## Current Boundaries

- Use Docs `documents.batchUpdate` for structured content writes in Markdown-authored review flows.
- Markdown-authored publish flows may still target Google Docs tabs.
- Google Drive supports direct Google Docs export to `text/markdown`.
- The export helper currently exports whole docs only, not per-tab bundles.
- Markdown export is the preferred first-pass mirror format for AI review, but fidelity can drop for rich layouts.
- The export helper strips large embedded image data URIs down to placeholders.
- Avoid full Doc recreation because it weakens comment continuity.
- This workflow is comment-first; Google Docs suggestions are intentionally out of scope.
