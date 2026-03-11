# Google Docs Review Overview

This workflow is for Markdown-as-source review using Google Docs as the collaborative comment surface.

- Markdown is canonical.
- Google Docs is the review surface.
- Review comments are pulled from Google Docs and Drive.
- Accepted feedback is applied back to the original `.md` file.
- Store the full Google Doc URL in source metadata.
- A directory of related Markdown notes may map to one Google Doc with tabs.

## Why

Some workflows draft designs, specs, and notes in Markdown but still need Google Docs for collaborative review and comments.

This workflow supports that by keeping the original source in Markdown while using one long-lived Google Doc for discussion.

## Required Frontmatter Attributes

Each reviewable Markdown note keeps Google Doc linkage in frontmatter.

Required attributes after bootstrap:

- `gdoc_id`: long-lived Google Doc file ID
- `gdoc_url`: full Google Doc URL
- `gdoc_source_of_truth`: must be `markdown`

Recommended attributes:

- `gdoc_last_published_sha`: content hash or git SHA for the last published source state
- `gdoc_last_published_at`: last publish timestamp in ISO 8601 format
- `gdoc_last_comment_sync`: last comment intake timestamp in ISO 8601 format
- `gdoc_role`: `main` or `tab` when a directory maps to one Google Doc with tabs
- `gdoc_tab_title`: explicit tab title for tab notes when needed

## Directory-to-Tab Bundle Contract

If multiple Markdown files live in the same directory and should publish into one Google Doc, use this rule:

- one file is the `main` note
- sibling `.md` files are published as tabs in that same Google Doc
- the main note owns the review bundle and should be the default bootstrap target
- sibling tab notes keep their own Markdown source but share the same `gdoc_id` and `gdoc_url`

Recommended behavior:

- main note publishes to the first/root tab
- each sibling tab note publishes to a dedicated Google Docs tab
- tab title defaults to the Markdown filename unless explicitly overridden

See `examples/gdoc-source-note.md` for a minimal sample note.

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

## Workflow

1. Add or initialize frontmatter on a Markdown note or note bundle.
2. Create or link a long-lived Google Doc.
3. If sibling `.md` files exist in the same directory, decide whether they should become tabs in the same Doc.
4. Publish Markdown content into the linked Doc and tabs.
5. Review in Google Docs using comments.
6. Pull open comments and map them back to source sections.
7. Update the original Markdown.
8. Reply to and resolve the corresponding Google Docs threads.

## Current Boundaries

- Use Docs `documents.batchUpdate` for structured content writes.
- For tab-aware reads, use `documents.get` with `includeTabsContent=true`.
- For tab-aware writes, target requests to the intended `tabId`.
- Avoid full Doc recreation because it weakens comment continuity.
- This workflow is comment-first; Google Docs suggestions are intentionally out of scope.
