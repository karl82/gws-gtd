---
description: One-shot Gmail inbox backlog drain. Iterates /gtd-sweep until trash settles. For backlogged inboxes only.
agent: gtd
subtask: true
---

Drain a backlogged Gmail inbox.

Scope and notes: $ARGUMENTS

Follow `reference.md § Backlog drain`. This wraps `/gtd-sweep` in a ralph-loop. Each iteration runs one sweep and re-evaluates exit conditions.

Use for one-shot backlog cleanup — onboarding a neglected inbox, post-vacation catch-up. Don't use for ongoing maintenance — use `/loop 2h /gtd-sweep` instead.

Recommended invocation:

```
/ralph-loop "Read last 10 lines of System/.gtd-state.jsonl. If any backlog drain exit condition in reference.md is met, emit <promise>TRASH_DRAINED</promise>. Otherwise run one /gtd-sweep pass." --completion-promise TRASH_DRAINED --max-iterations 50
```

After exit, prompt the user to run `/gtd daily` for actionable review.
