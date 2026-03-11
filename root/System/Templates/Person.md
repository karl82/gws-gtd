---
google_contact_id:
last_contact_sync:
---

## Open Tasks

```dataviewjs
await dv.view("System/Queries/project-linked-open", { file: dv.current().file.path });
```

## Relationship

- Context: <% tp.file.cursor(1) %>
- Contact: 

## Interaction Log

```dataviewjs
await dv.view("System/Queries/person-interactions", { file: dv.current().file.path });
```

## Completed Tasks

```dataviewjs
await dv.view("System/Queries/project-linked-done", { file: dv.current().file.path });
```
