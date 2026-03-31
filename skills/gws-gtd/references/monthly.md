## Monthly Procedure

### Scope

Run the monthly GTD review using `references/canonical-vault.md` and `System/Templates/Monthly Review.md`.

Template incorporation:
- Use a review note path that matches `^Journal(?:/.+)?/\d{4}-\d{2}\.md$`.
- If the monthly note does not exist, create it at a matching path so Templater applies `System/Templates/Monthly Review.md`.
- Use the template sections as the interactive agenda.

### Steps

1. Portfolio Audit
    - Confirm each active project has measurable outcome and at least one open `#task`.
    - Treat plain checklist items as local decomposition; they do not satisfy the open `#task` requirement.
2. Area Balance
   - Surface neglected or overloaded areas.
3. Stalled and Stale Detection
   - Projects inactive >30 days.
   - Open tasks stale >30 days without due dates.
4. Pattern and Capacity Analysis
   - Review journal signals and recurring blockers.
   - Detect due-date clustering and constraints.
5. Someday/Maybe Review
   - Review all `#someday` items: promote to active projects/tasks, delete stale ideas, or leave incubated.
   - This is the deeper pass that complements the weekly quick scan.
6. Next Month Commitments
   - Recommend top commitments and elimination candidates.

### Monthly Guardrails

- Do not archive automatically.
- Do not assume calendar availability.

### Monthly Output

- Portfolio exceptions
- Capacity and risk summary
- Proposed commitments for next month
