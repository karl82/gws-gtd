<%*
const weekParsed = window.moment(tp.file.title, "GGGG-[W]WW", true);
const weekAnchor = weekParsed.isValid() ? weekParsed.clone() : window.moment();
const weekLabel = weekAnchor.format("GGGG-[W]WW");
const weekStart = weekAnchor.clone().startOf("isoWeek").format("YYYY-MM-DD");
const weekEnd = weekAnchor.clone().endOf("isoWeek").add(1, "day").format("YYYY-MM-DD");
-%>
# Weekly Review - <% weekLabel %>

Week Window: `<% weekStart %>` to `<% weekAnchor.clone().endOf("isoWeek").format("YYYY-MM-DD") %>`

## 1. Get Clear

### Mind Sweep

- [ ] Mind sweep: capture anything on your mind, open tabs, loose notes, meeting follow-ups as `#task #inbox`.

### Inbox Sweep

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "inbox", file: dv.current().file.path });
```

- [ ] Clarify every inbox item.
- [ ] For every clarified item, remove `#inbox` and either move it to Projects/Areas or keep it in place with `[[Projects/...]]` or `[[Areas/...]]` link.
- [ ] Delete irrelevant captures.

### Loose Ends

- [ ] Capture unresolved thoughts from the week.
- [ ] Add missing `#task` markers where actionability exists.

## 2. Get Current

### Overdue

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "overdue", file: dv.current().file.path });
```

### Due This Week

```dataviewjs
await dv.view("System/Queries/weekly-due", { file: dv.current().file.path });
```

### Waiting

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "waiting", file: dv.current().file.path });
```

### Possible Next Steps

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "next-candidates", file: dv.current().file.path });
```

- [ ] Review ready tasks and promote only a small set to `#next`.
- [ ] For each active project, confirm whether it has a current `#next` action.

### Projects Health

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "project-health", file: dv.current().file.path });
```

### Stalled Projects (>14 Days)

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "stalled-14", file: dv.current().file.path });
```

- [ ] Confirm each active project has at least one open linked `#task`.
- [ ] Re-sequence blocked tasks.

### Orphan Tasks (Needs Context Link)

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "orphan-open", file: dv.current().file.path });
```

- [ ] Resolve all non-`#inbox` orphan tasks by adding `[[Projects/...]]` or `[[Areas/...]]` link, or moving them to the right note.

## 3. Get Creative

### Journal Insights

```dataviewjs
await dv.view("System/Queries/journal-weekly", { file: dv.current().file.path });
```

- Patterns noticed: <% tp.file.cursor(1) %>
- Risks to resolve:
- Opportunities to pursue:

### Someday/Maybe

```dataviewjs
await dv.view("System/Queries/task-list", { preset: "someday", file: dv.current().file.path });
```

- [ ] Scan for items to promote to active `#task` or delete as stale.

### Next Week Focus

- [ ] Top outcome 1:
- [ ] Top outcome 2:
- [ ] Top outcome 3:

### Eliminate / Defer

- [ ] Drop or archive at least one low-value commitment.
