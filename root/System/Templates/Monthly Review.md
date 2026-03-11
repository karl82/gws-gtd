<%*
const monthParsed = window.moment(tp.file.title, "YYYY-MM", true);
const monthAnchor = monthParsed.isValid() ? monthParsed.clone() : window.moment();
const monthLabel = monthAnchor.format("YYYY-MM");
const monthStart = monthAnchor.clone().startOf("month").format("YYYY-MM-DD");
const monthEnd = monthAnchor.clone().endOf("month").add(1, "day").format("YYYY-MM-DD");
-%>
# Monthly Review - <% monthLabel %>

Month Window: `<% monthStart %>` to `<% monthAnchor.clone().endOf("month").format("YYYY-MM-DD") %>`

## Portfolio Audit

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "project-health", file: dv.current().file.path });
```

- [ ] Confirm every active project has a measurable outcome.
- [ ] Confirm every active project has at least one open `#task`.

## Area Balance

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "areas-list", file: dv.current().file.path });
```

- Which areas were under-supported?
- Which areas were over-weighted?
- What needs rebalancing next month?

## Stalled & Zombies

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "stalled-30", file: dv.current().file.path });
```

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "next-explicit", file: dv.current().file.path });
```

- [ ] Mark zombie projects for archive or reactivation.

## Pattern Analysis

```dataviewjs
await dv.view("System/Queries/journal-monthly", { file: dv.current().file.path });
```

## Due This Month

```dataviewjs
await dv.view("System/Queries/monthly-due", { file: dv.current().file.path });
```

- Wins pattern: <% tp.file.cursor(1) %>
- Friction pattern:
- Repeated blockers:

## Capacity Check

- Current commitments count:
- Energy reality for next month:
- Constraints (travel, deadlines, obligations):

## Next Month Commitments

- [ ] Priority outcome 1:
- [ ] Priority outcome 2:
- [ ] Priority outcome 3:
- [ ] One commitment to eliminate:
