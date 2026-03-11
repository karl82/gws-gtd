## Status Procedure

### Scope

Use this procedure to inspect the sync state between a Markdown source note and its linked Google Doc.

### Step 0 - Read Source Metadata

1. Read source frontmatter.
2. Extract:
   - `gdoc_id`
   - `gdoc_url`
   - `gdoc_source_of_truth`
   - `gdoc_role`
   - `gdoc_tab_title`
   - `gdoc_last_published_sha`
   - `gdoc_last_published_at`
   - `gdoc_last_comment_sync`

### Step 1 - Validate Linkage

1. Ensure `gdoc_id` exists.
2. Ensure `gdoc_url` exists and matches the linked doc.
3. Confirm the linked Google Doc is accessible.
4. Report missing metadata or auth blockers.

### Step 2 - Check Drift

1. Compare current source content hash to `gdoc_last_published_sha` when present.
2. Inspect Drive or Docs metadata for recent remote modifications.
3. If the note is part of a directory bundle, inspect sibling `.md` notes and tab metadata.
4. Report whether the source appears ahead, the Doc appears ahead, or the state is unknown.

### Step 3 - Check Review State

1. Count open comments.
2. Count recently modified comment threads.
3. In tabbed bundles, separate counts by tab when possible.
4. Surface unresolved comments that are likely stale.

### Output

Report:

- source Markdown path
- linked `gdoc_id`
- full `gdoc_url`
- metadata completeness
- whether the note is `main` or `tab`
- source or doc drift status
- open comment count
- next recommended mode: `gdoc-publish`, `gdoc-comment-intake`, `gdoc-apply-feedback`, or `gdoc-reply-resolve`
