---
description: Drain a Gmail inbox backlog via iterated junk-sweeps. Trash-only. Defers actionable review to /gtd-daily.
agent: gtd-junk-sweep
subtask: true
---

Drain a backlogged Gmail inbox via repeated junk-sweep passes.

Scope and notes: $ARGUMENTS

This command wraps `/gtd-junk-sweep` in a ralph-loop. Each iteration runs one sweep, appends its event to `System/.gtd-coach-state.jsonl`, then re-evaluates exit conditions. Exits when the trash stream settles, the candidate query returns zero, the user disengages, or the sweep cap is reached.

**Trash-only.** Actionable mail (import, waiting, reference, appointment) is deferred. Once this loop exits, run `/gtd-daily` to review what remains.

Use for: onboarding a neglected inbox (>500 unlabeled threads), post-vacation catch-up, recovery after the 2h loop has been offline for weeks.

Do NOT use for ongoing maintenance — use `/loop 2h /gtd-junk-sweep` for that.

See `gmail-intake.md § Backlog Drain` for the loop logic and `§ Backlog Drain Exit Conditions` for the termination criteria.

Recommended invocation:

```
/ralph-loop "Read the last 10 lines of System/.gtd-coach-state.jsonl. Apply gmail-intake.md § Backlog Drain Exit Conditions. If any condition matches, emit <promise>TRASH_DRAINED</promise> and append a loop-exit event. Otherwise run one /gtd-junk-sweep pass." --completion-promise TRASH_DRAINED --max-iterations 50
```

Output: aggregate `{trashed: N, iterations: N, reason: <exit-reason>}` plus a final line reminding the user to run `/gtd-daily` for the actionable review.
