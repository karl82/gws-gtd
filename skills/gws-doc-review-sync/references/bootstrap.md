## Bootstrap Procedure

### Scope

Use this procedure to prepare a Markdown file for Google Docs review sync.

### Preconditions

- The source note is a Markdown file.
- The note is the canonical source.
- The user intends to review in Google Docs via comments.

### Step 0 - Auth Check

1. Run `gws auth status`.
2. Verify Docs and Drive scopes are available.
3. If scopes are missing, stop and report the exact re-auth command.

### Step 1 - Source Note Check

1. Read the source Markdown file.
2. Verify whether frontmatter exists.
3. Ensure required attributes can be set:
   - `gdoc_id`
   - `gdoc_url`
   - `gdoc_source_of_truth: markdown`
4. Inspect the source file's directory for sibling `.md` files when the user wants tabbed publish.
5. If sibling `.md` files should become one review bundle, decide which note is `main` and which notes are `tab` notes.

### Step 2 - Link or Create Google Doc

1. If `gdoc_id` already exists, validate that the file still exists in Drive.
2. Otherwise create a new Google Doc or accept an existing `gdoc_id` supplied by the user.
3. Record both the long-lived `gdoc_id` and the full `gdoc_url` in frontmatter.
4. If the source directory is a tabbed review bundle, make sure sibling tab notes also reference the same `gdoc_id` and `gdoc_url`.

### Step 3 - Initialize Sync Metadata

Set or normalize frontmatter fields:

- `gdoc_id`
- `gdoc_url`
- `gdoc_source_of_truth: markdown`
- optional `gdoc_role: main|tab`
- optional `gdoc_tab_title`
- optional `gdoc_last_published_sha`
- optional `gdoc_last_published_at`
- optional `gdoc_last_comment_sync`

If the source directory is treated as one review bundle:

- mark one note as `gdoc_role: main`
- mark sibling notes as `gdoc_role: tab`
- default tab titles from filenames unless explicitly overridden

### Step 4 - Report Bootstrap Status

Report:

- source Markdown path
- linked `gdoc_id`
- full `gdoc_url`
- missing auth or metadata blockers
- whether sibling `.md` files were detected and configured as tabs
- whether the note is ready for `gdoc-publish`
