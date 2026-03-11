## Export Markdown Procedure

### Scope

Use this procedure to export a Google Doc into one Markdown file so agents can read it locally during design review or PR review.

### Preconditions

- `gdoc_id` and `gdoc_url` are known.
- Drive auth is available.

### Export Rules

- Prefer Google Drive export with `text/markdown`.
- Treat the exported Markdown as a mirror, not as the source of truth.
- Preserve provenance metadata in frontmatter.
- Export the whole Google Doc into one Markdown file.
- Use the bundled `scripts/export_gdoc_markdown.py` helper for repeatable local exports.

### Step 0 - Inspect the Source Doc

1. Read document metadata.
2. Confirm the destination path for the local Markdown mirror.

### Step 1 - Export the Markdown

1. Use Drive export `text/markdown`.
2. Preserve a stable local file path for repeated exports.
3. Prefer one file per design doc.

### Step 2 - Write Mirror Metadata

Record or update frontmatter:

- `gdoc_id`
- `gdoc_url`
- `gdoc_source_of_truth: google-docs`
- `gdoc_revision_id`
- `gdoc_last_exported_at`
- `gdoc_title`

### Step 3 - Report Fidelity Caveats

Call out likely limitations:

- advanced layout may simplify
- comments are not the same as inline source text
- some rich elements may degrade or flatten in Markdown

### Output

Report:

- exported file path
- linked `gdoc_id`
- full `gdoc_url`
- revision or modified-time provenance
- fidelity caveats worth knowing before AI review

### Helper Example

```bash
python3 <installed-gws-doc-review-sync-skill-dir>/scripts/export_gdoc_markdown.py --doc-url 'https://docs.google.com/document/d/DOC_ID/edit' --output DesignDocs/Foo.md --force --stdout-manifest
```
