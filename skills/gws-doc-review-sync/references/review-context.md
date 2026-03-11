## Review Context Procedure

### Scope

Use this procedure to gather Google Docs design context into Markdown so an agent can review a PR with the intended design in view.

### Inputs

Possible inputs include:

- explicit Google Doc URLs
- known linked notes with `gdoc_*` metadata
- a PR branch, issue, or repo path that points to design docs by convention

### Goal

Produce a local Markdown review context bundle that is easy for an agent to read before reviewing code.

### Step 0 - Resolve Relevant Docs

1. Collect the design docs relevant to the code under review.
2. Prefer explicit links first.
3. If multiple docs are present, order them by likely architectural importance.

### Step 1 - Export Local Mirrors

1. For Google Docs sources, use `gdoc-export-md`.
2. For Markdown sources already in the repo, use the canonical local Markdown instead.
3. Default generated context location can be a dedicated folder such as `.review-context/designs/`.

### Step 2 - Build the Review Bundle

For each doc include:

- local Markdown path
- full `gdoc_url`
- title
- revision or export timestamp
- short note about fidelity caveats if layout-heavy

Recommended layout:

```text
.review-context/
  designs/
    foo-design.md
```

### Step 3 - Present a Read Order

1. Primary design or spec first.
2. Supporting reference docs next.

### Output

Report:

- exact Markdown files the agent should read
- the doc URLs they mirror
- stale docs that should be re-exported before reviewing code
- unresolved ambiguity about which design doc governs the PR

### Helper Example

```bash
python3 <installed-gws-doc-review-sync-skill-dir>/scripts/export_gdoc_markdown.py --doc-url 'https://docs.google.com/document/d/DOC_ID/edit' --output .review-context/designs/foo-design.md --force --stdout-manifest
```
