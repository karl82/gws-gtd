## Publish Procedure

### Scope

Use this procedure to push canonical Markdown content into an existing linked Google Doc.

### Preconditions

- Source Markdown is canonical.
- Source frontmatter contains `gdoc_id`, `gdoc_url`, and `gdoc_source_of_truth: markdown`.
- Docs and Drive auth is available.

### Publish Rules

- Reuse the linked Google Doc.
- Prefer minimal structural churn.
- Preserve stable headings when possible.
- Do not silently overwrite the Doc if the plan would destroy open comment context.
- If sibling `.md` files in the same directory are part of the same review bundle, publish them as tabs in the same Google Doc.

### Rendering Contract

Initial renderer support should be intentionally narrow:

- headings
- paragraphs
- bullet lists
- numbered lists
- blockquotes
- fenced code blocks
- inline bold, italic, and code when practical

### Step 0 - Drift Check

1. Read source frontmatter.
2. Compute or read a source content hash.
3. If the source hash matches `gdoc_last_published_sha`, report `no publish needed` unless forced.
4. Detect whether sibling `.md` files in the same directory should be included as tabs.

### Step 1 - Comment Safety Check

1. Pull open comments for the linked Doc.
2. If open comments exist and the publish would substantially rewrite structure, warn before proceeding.
3. Prefer section-preserving updates over whole-document replacement.
4. In tabbed bundles, preserve existing tab IDs and titles when possible.

### Step 2 - Build Update Requests

1. Translate Markdown into Docs API requests.
2. If the note is a main note and sibling tab notes exist, build one update plan for the root tab plus sibling tabs.
3. Use `documents.batchUpdate` for structured writes.
4. Target each write request to the intended `tabId`.
5. Avoid plain-text append helpers for publish flows.

### Step 3 - Update Metadata

After successful publish, update frontmatter:

- `gdoc_last_published_sha`
- `gdoc_last_published_at`

If a tabbed bundle was published:

- keep the shared `gdoc_url` on all related notes
- keep one `main` note and sibling `tab` roles stable across republishes

### Publish Output

Report:

- source path
- `gdoc_id`
- full `gdoc_url`
- whether the Doc was updated
- whether sibling notes were published as tabs
- whether open comments were present during publish
- any manual-risk warnings about comment continuity
