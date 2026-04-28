---
name: journaling
description: Use when logging meetings, 1:1s, design reviews, document shares, or observations to today's daily note in the gws-gtd vault.
---

# journaling

**REQUIRED SUB-SKILL:** Use gws-gtd for vault conventions and task syntax rules (`references/canonical-vault.md`, `references/conventions.md`).

This skill extends the `gws-gtd` workflow with daily note entry creation. It applies `gws-gtd` vault conventions (task syntax, wikilinks, canonical folders) for all formatting.

## How to Use

Describe what happened in natural language. The skill classifies the entry type and formats it correctly.

Examples:
- "Meeting with S Muralidhar about EKS and VPC support, agreed on short-term EKS approach"
- "Lawrence shared the LS dependency closure doc, my task is to make a practical approach"
- "Reviewed Kyle's TPM-Aware AMI proposal, looks good but needs work on image flavors"
- "Vikram wrote good analysis on CPS server setup latency"

## Entry Types

### 1:1 Meeting
When input describes a one-on-one meeting or check-in:
```
- #1_1 [[People/Name]] - [topic]
  - [key point]
  - [key point]
```

### Group Meeting
When input describes a meeting with multiple people:
```
- Meeting with [[People/Name]], [[People/Name]] - [topic]
  - [key point]
  - [optional: link to doc or notes]
```

### Document/Design Review
When input describes reviewing someone's work:
```
- Reviewed [[People/Name]]'s [doc title](URL) - [one-line summary]
  - [feedback point]
  - [feedback point]
```

### Document Share
When someone shared a document or resource:
```
- [[People/Name]] - Shared [doc title](URL) - [one-line summary]
  - [key point]
```

### General Note
For observations, status updates, or context:
```
- [Note text] [[Projects/...]] (if relevant)
```

## People Handling

1. For each person mentioned, check the vault's `People/` directory
2. If a record exists, link with `[[People/Full Name]]`
3. If no record exists, create a stub using the vault's People Template conventions, then link

## Task Extraction

After writing the entry, scan the input for action items. For each one found:
- Ask the user to confirm before creating (one `AskUserQuestion` per action item, not batched)
- If confirmed, add the task immediately after the entry using gws-gtd task syntax

## Daily Note

Entries go under `## Notes` in today's daily note. If the section does not exist, create it. Append — never overwrite existing content.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Batching task confirmations into one question | One `AskUserQuestion` per action item |
| Overwriting existing note content | Always append to `## Notes`; never replace |
| Creating People stubs without checking first | Always check `People/` directory before creating a stub |
| Skipping people resolution | Every person mentioned must be linked with `[[People/Full Name]]` |
