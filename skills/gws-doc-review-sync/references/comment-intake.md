## Comment Intake Procedure

### Scope

Use this procedure to read Google Doc review comments and map them back to the canonical Markdown source.

### Required Fields

When using Drive comments APIs, request only the fields needed for review mapping:

- `id`
- `content`
- `quotedFileContent`
- `anchor`
- `resolved`
- `replies`
- `modifiedTime`

### Step 0 - Read Source Context

1. Read the source Markdown file.
2. Parse headings and major sections.
3. Preserve enough local context to map comments back to nearby source text.

### Step 1 - Pull Open Comment Threads

1. Use Drive comments APIs against the linked `gdoc_id`.
2. Exclude resolved comments unless explicitly requested.
3. Keep replies attached to each thread.

### Step 2 - Map Comments to Source

Use this priority order:

1. exact quoted text match
2. normalized text match
3. nearest heading or section match
4. manual review fallback

### Step 3 - Produce Review Queue

For each comment, report:

- comment ID
- comment summary
- source file path
- matched heading or section when available
- confidence (`high`, `medium`, `low`)
- unresolved mapping notes when confidence is low

### Comment Intake Guardrails

- Do not invent exact positions when the anchor is ambiguous.
- Do not silently drop unmapped comments.
- Treat low-confidence mappings as manual review items.

### Output

Report:

- count of open comments
- count mapped with high confidence
- count requiring manual review
- the next set of source edits to consider
