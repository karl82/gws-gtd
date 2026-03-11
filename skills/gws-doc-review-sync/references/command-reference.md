## Command Reference

Use these commands as the primary `gws` lookup points for the Google Docs review workflow.

### Auth

```bash
gws auth status
gws auth logout
gws auth login --scopes "https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/drive"
```

Preserve the current broad `gws-gtd` scope set and add Docs/Drive:

```bash
gws auth logout
gws auth login --scopes "email,openid,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts,https://www.googleapis.com/auth/contacts.other.readonly,https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/gmail.compose,https://www.googleapis.com/auth/gmail.insert,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email"
gws auth status
```

### Drive File Lookup

```bash
gws drive files list --params '{"q":"mimeType = \"application/vnd.google-apps.document\" and trashed = false","fields":"files(id,name,mimeType,modifiedTime,webViewLink)"}'
gws drive files get --params '{"fileId":"DOC_ID","fields":"id,name,mimeType,modifiedTime,webViewLink"}'
```

### Create or Inspect Documents

```bash
gws docs documents create --json '{"title":"Review Doc Title"}'
gws docs documents get --params '{"documentId":"DOC_ID"}'
gws schema docs.documents.batchUpdate
```

### Publish Notes

Use raw Docs batch updates for structured content writes.

```bash
gws docs documents batchUpdate --params '{"documentId":"DOC_ID"}' --json '{"requests":[...]}'
```

Avoid this for publish flows:

```bash
gws docs +write --document DOC_ID --text 'Plain text only'
```

### Export Docs To Markdown

Google Drive supports direct Google Docs export to Markdown:

```bash
gws drive files export --params '{"fileId":"DOC_ID","mimeType":"text/markdown"}'
```

Useful fallbacks when Markdown fidelity is poor:

```bash
gws drive files export --params '{"fileId":"DOC_ID","mimeType":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}'
gws drive files export --params '{"fileId":"DOC_ID","mimeType":"application/zip"}'
```

Notes:

- `text/markdown` is the preferred first export target for AI review.
- `application/zip` is HTML/web-page export, not a single `.html` file.
- richer Docs formatting may survive better in DOCX or HTML than in Markdown.

### Bundled Helper

Use the bundled helper when you want stable file naming and provenance frontmatter:

```bash
python3 <installed-gws-doc-review-sync-skill-dir>/scripts/export_gdoc_markdown.py --doc-url 'https://docs.google.com/document/d/DOC_ID/edit' --output .review-context/designs/foo-design.md --force --stdout-manifest
```

Behavior:

- exports the whole Google Doc into one Markdown file
- adds provenance frontmatter for later reference
- strips large embedded image data URIs down to placeholders

### Comments and Replies

Drive comments methods require explicit `fields` selection.

```bash
gws drive comments list --params '{"fileId":"DOC_ID","fields":"comments(id,content,quotedFileContent,anchor,resolved,replies,modifiedTime),nextPageToken"}'
gws drive comments get --params '{"fileId":"DOC_ID","commentId":"COMMENT_ID","fields":"id,content,quotedFileContent,anchor,resolved,replies,modifiedTime"}'
gws drive replies list --params '{"fileId":"DOC_ID","commentId":"COMMENT_ID"}'
gws drive replies create --params '{"fileId":"DOC_ID","commentId":"COMMENT_ID"}' --json '{"content":"Addressed in source Markdown."}'
gws drive replies create --params '{"fileId":"DOC_ID","commentId":"COMMENT_ID"}' --json '{"action":"resolve"}'
```

### Revisions

```bash
gws drive revisions list --params '{"fileId":"DOC_ID","fields":"revisions(id,modifiedTime,keepForever,lastModifyingUser)"}'
```

### Practical Notes

- Prefer one long-lived Doc per Markdown source file.
- For Docs-authored design docs that need to guide code review, prefer exporting a Markdown mirror rather than pasting summaries by hand.
- Prefer explicit `fields` in Drive calls.
- Treat replies and resolution as review bookkeeping after source updates, not as a substitute for source changes.
