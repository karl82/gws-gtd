## Reply and Resolve Procedure

### Scope

Use this procedure after source Markdown has been updated in response to review feedback.

### Preconditions

- The relevant source Markdown change is complete.
- The comment thread was mapped to the source with sufficient confidence.
- The user wants the Google Docs thread updated.

### Step 0 - Verify Source Change

1. Re-read the updated Markdown source.
2. Confirm the requested feedback was addressed or explicitly declined.

### Step 1 - Reply to the Thread

1. Add a concise reply on the comment thread.
2. Prefer source-oriented wording, for example:
   - `Addressed in source Markdown.`
   - `Updated in <path>.`
   - `Kept as-is in source because <reason>.`

### Step 2 - Resolve or Leave Open

1. Resolve when the requested change is complete in the source.
2. Leave open when:
   - the change is partial
   - the mapping is uncertain
   - the user wants follow-up review first

### Guardrails

- Do not resolve threads for changes that were not actually made.
- Do not mark comments handled if source edits are still pending.
- If a comment is rejected, reply with rationale and leave it unresolved unless the user requests closure.

### Output

Report:

- source Markdown path updated
- comment IDs replied to
- comment IDs resolved
- any threads intentionally left open
