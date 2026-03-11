## Apply Feedback Procedure

### Scope

Use this procedure to update the canonical Markdown source from accepted Google Docs review comments.

### Preconditions

- A source Markdown file is linked to a Google Doc.
- Relevant review comments were pulled through `gdoc-comment-intake`.
- The user accepted the proposed source changes or asked for an implementation pass.

### Step 0 - Build the Edit Queue

1. Start from mapped review comments only.
2. Group related comments by heading or source section.
3. Separate items into:
   - direct content edits
   - wording clarifications
   - structural follow-ups
   - manual-review items

### Step 1 - Edit the Markdown Source

1. Update the original `.md` file.
2. Preserve heading structure where practical.
3. Keep edits minimal and intentional.
4. If a comment requests a change that should be declined, keep the source unchanged and record the rationale for the reply step.

### Step 2 - Track Comment Outcomes

For each processed comment, assign one outcome:

- `applied`
- `partially-applied`
- `declined`
- `manual-review`

### Step 3 - Prepare Publish and Reply Follow-Up

1. If the source changed, the note is ready for `gdoc-publish`.
2. If comments were fully addressed, the related threads are ready for `gdoc-reply-resolve`.
3. If mapping is uncertain, keep the item open for manual review.

### Guardrails

- Edit Markdown, not the Google Doc body.
- Do not mark feedback handled unless the source actually changed or an explicit decline rationale exists.
- Do not collapse multiple comments into one vague outcome when thread-specific follow-up is needed.

### Output

Report:

- source file updated
- sections changed
- comment IDs by outcome
- any items deferred to manual review
