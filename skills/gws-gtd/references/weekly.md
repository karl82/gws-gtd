## Weekly Procedure

### Scope

Run the weekly GTD review cycle using `references/canonical-vault.md` and `System/Templates/Weekly Review.md`.

Template incorporation:
- Use a review note path that matches `^Journal(?:/.+)?/\d{4}-W\d{2}\.md$`.
- If the weekly note does not exist, create it at a matching path so Templater applies `System/Templates/Weekly Review.md`.
- Use the template sections as the interactive agenda.

### Prerequisites

Before starting the weekly review, run the daily intake ceremony (`references/daily-intake.md`) to ensure all new Gmail threads and calendar events are imported and processed. The weekly review operates on a current vault — do not skip this step.

### Steps

1. Get Clear
    - Run `#inbox` Zero to completion as a strict gate.
    - Clarify ambiguous captures into explicit outcomes plus either a `#task` next action or a plain local checklist step.
    - If `#inbox` queue is not zero, stop and report: `Get Clear incomplete (#inbox not zero)`.
    - **Drain the `gtd/review` Gmail label queue.** These are emails deferred from daily processing for weekly decision. For each thread: promote to `gtd/import` (becomes a task), move to `gtd/waiting`, `gtd/reference`, or trash. This queue must reach zero before Get Clear is complete.
2. Get Current
   - Review overdue and next-7-day due tasks.
   - Review `#waiting` items.
   - Review possible next-step candidates and promote only a small set to `#next`.
   - Review non-`#inbox` orphan tasks: flag only tasks that have no `[[Projects/...]]` or `[[Areas/...]]` wikilink AND do not live inside a `Projects/` or `Areas/` file. Tasks in `Journal/` or elsewhere that carry a valid wikilink are clean and must not be flagged or relocated.
   - Surface stalled projects (>14 days or no open linked task).
3. Get Creative
   - Review journal patterns from the week.
   - Recommend top 3 outcomes for next week.

### Weekly Guardrails

- Analytical assistant, not decision-maker.
- Keep recommendations tied to due dates, explicit priority markers, and project value.
- Exclude plain checklist items from global task counts; they are local decomposition only.

### Weekly Output

- Weekly health snapshot
- Stalled or stale exceptions
- Proposed top 3 outcomes
