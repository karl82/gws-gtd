## Outcome

<% tp.file.cursor(1) %>

## Next Actions

```dataviewjs
await dv.view("System/Queries/project-linked-open", { file: dv.current().file.path });
```

- Link related daily tasks with `[[<% tp.file.path(true).replace('.md', '') %>]]`.

## Notes

- Scope:
- Constraints:
- Stakeholders: (use `[[People/Name]]` links)

## Completed Tasks

```dataviewjs
await dv.view("System/Queries/project-linked-done", { file: dv.current().file.path });
```
