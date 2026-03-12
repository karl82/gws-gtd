---
project_status: active
---

## Outcome

<% tp.file.cursor(1) %>

- Canonical project link: `[[<% tp.file.path(true).replace('.md', '') %>]]`

## Next Actions

```dataviewjs
await dv.view("System/Queries/project-linked-open", { file: dv.current().file.path });
```

- Link related daily tasks with `[[<% tp.file.path(true).replace('.md', '') %>]]`.

## Designs

```dataviewjs
await dv.view("System/Queries/project-designs", { file: dv.current().file.path });
```

## Notes

- Scope:
- Constraints:
- Stakeholders: (use `[[People/Name]]` links)

## Support Folder

- If this project needs deeper material, keep it under `Projects/<Domain>/<Project>/`.
- Put project-owned design notes under `Projects/<Domain>/<Project>/designs/`.

## Completed Tasks

```dataviewjs
await dv.view("System/Queries/project-linked-done", { file: dv.current().file.path });
```
