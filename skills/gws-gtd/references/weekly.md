## Weekly Procedure

### Scope

Run the weekly GTD review cycle using `references/canonical-vault.md` and `System/Templates/Weekly Review.md`.

Template incorporation:
- Use a review note path that matches `^Journal(?:/.+)?/\d{4}-W\d{2}\.md$`.
- If the weekly note does not exist, create it at a matching path so Templater applies `System/Templates/Weekly Review.md`.
- Use the template sections as the interactive agenda.

### Prerequisites

Before starting the weekly review, check whether a daily journal note exists
for today (`Journal/YYYY/MM/YYYY-MM-DD.md` with today's date substituted). If
it does not exist, invoke the `gtd-daily` agent interactively as a prerequisite
— run the full daily ceremony with the user and wait for it to complete before
proceeding. Do not begin Get Clear until the daily ceremony is done.

### Steps

1. Get Clear
    - Sweep all `#task #inbox` items across the vault to zero. This is a strict gate — Get Clear is not complete until `#inbox` is empty.
    - The `#inbox` queue includes both urgent items from daily intake and deferred review-style tasks (recruiter outreach, ambiguous mail, etc.) that were intentionally left for weekly sweep.
    - For deferred review-style items, use batch decisions: group by type (recruiter, ambiguous, informational), propose outcomes in bulk, and apply after confirmation. Do not review each one individually.
    - For each `#inbox` item decide: clarify (add wikilink, remove `#inbox`, set `#next` or `#waiting`) or delete (task no longer relevant; archive source Gmail thread).
    - If `#inbox` queue is not zero after sweep, stop and report: `Get Clear incomplete (#inbox not zero)`.
    - Also surface unlabeled Gmail inbox threads older than 7 days via `weekly-reconcile.md` Step 1.
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
