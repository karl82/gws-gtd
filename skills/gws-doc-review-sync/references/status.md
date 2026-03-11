## Status Procedure

### Scope

Use this procedure to inspect the state between a local Markdown note and its linked Google Doc.

### Step 0 - Read Source Metadata

1. Read source frontmatter.
2. Extract:
   - `gdoc_id`
   - `gdoc_url`
   - `gdoc_source_of_truth`
   - `gdoc_last_published_sha`
   - `gdoc_last_published_at`
   - `gdoc_last_comment_sync`
   - `gdoc_last_exported_at`
   - `gdoc_revision_id`

### Step 1 - Validate Linkage

1. Ensure `gdoc_id` exists.
2. Ensure `gdoc_url` exists and matches the linked doc.
3. Confirm the linked Google Doc is accessible.
4. Report missing metadata or auth blockers.

### Step 2 - Check Drift

1. If `gdoc_source_of_truth` is `markdown`, compare current source content hash to `gdoc_last_published_sha` when present.
2. If `gdoc_source_of_truth` is `google-docs`, compare current remote revision to `gdoc_revision_id` and local `gdoc_last_exported_at`.
3. Inspect Drive or Docs metadata for recent remote modifications.
4. Report whether the local mirror is ahead, the Doc is ahead, or the state is unknown.

### Step 3 - Check Review State

1. Count open comments.
2. Count recently modified comment threads.
3. Surface unresolved comments that are likely stale.

### Output

Report:

- source Markdown path
- linked `gdoc_id`
- full `gdoc_url`
- source-of-truth mode
- metadata completeness
- source or doc drift status
- open comment count
- next recommended mode: `gdoc-publish`, `gdoc-comment-intake`, `gdoc-apply-feedback`, `gdoc-reply-resolve`, or `gdoc-export-md`
