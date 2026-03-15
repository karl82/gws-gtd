---
description: Run the weekly GTD review ceremony
agent: gtd-weekly
subtask: true
---

Run the weekly GTD review ceremony for this repository.

Scope and notes: $ARGUMENTS

Requirements:
- Follow `AGENTS.md` and `gws-gtd` in `weekly` and `weekly-reconcile` modes.
- Cover Get Clear, Get Current, and Get Creative.
- Enforce strict weekly behavior: complete `#inbox` Zero in Get Clear before moving on.
- If `#inbox` queue is not zero, stop and report `Get Clear incomplete (#inbox not zero)`.
- Include Google reconciliation checks:
  - configured review-label queue
  - unlabeled inbox emails older than 7 days
  - open `#waiting` loops linked to Gmail
  - calendar load for next 7 days
- Enforce hybrid inbox integrity: non-`#inbox` tasks outside `Projects/` and `Areas/` must include `[[Projects/...]]` or `[[Areas/...]]` links.
- Assume Gmail is the only capture inbox and `GTD Signals` is output-only.
- Incorporate the dedicated weekly template and structure the session around it.
- Ensure the review note path matches `^Journal(?:/.+)?/\d{4}-W\d{2}\.md$` so the weekly template is applied when creating notes.
- Run as an interactive facilitation session.
- Ask one focused question at a time and wait for my response.
- Review possible next-step candidates and intentionally promote only a small set to `#next`.
- Return a concise weekly health snapshot with top 3 outcomes.

Template reference:
@System/Templates/Weekly Review.md
