## Command Reference

Use these commands as the primary `gws` lookup points for the Google Docs review workflow.

### Auth

```bash
gws auth status
gws auth logout
gws auth login --scopes "https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/drive"
```

### Drive File Lookup

```bash
gws drive files list --params '{"q":"mimeType = \"application/vnd.google-apps.document\" and trashed = false","fields":"files(id,name,mimeType,modifiedTime)"}'
gws drive files get --params '{"fileId":"DOC_ID","fields":"id,name,mimeType,modifiedTime,webViewLink"}'
```

### Create or Inspect Documents

```bash
gws docs documents create --json '{"title":"Review Doc Title"}'
gws docs documents get --params '{"documentId":"DOC_ID"}'
gws docs documents get --params '{"documentId":"DOC_ID","includeTabsContent":true}'
gws schema docs.documents.batchUpdate
```

Tab-aware notes:

- use `includeTabsContent=true` when reading a tabbed review document
- use request `tabId` targeting in `documents.batchUpdate` when writing to a specific tab

### Publish Notes

Use raw Docs batch updates for structured content writes.

```bash
gws docs documents batchUpdate --params '{"documentId":"DOC_ID"}' --json '{"requests":[...]}'
```

Avoid this for publish flows:

```bash
gws docs +write --document DOC_ID --text 'Plain text only'
```

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
- When a directory contains one main note plus sibling tab notes, prefer one long-lived Doc with tabs over multiple Docs.
- Prefer explicit `fields` in Drive calls.
- Treat replies and resolution as review bookkeeping after source updates, not as a substitute for source changes.
