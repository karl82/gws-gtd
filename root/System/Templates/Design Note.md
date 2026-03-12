<%*
const path = tp.file.path(true);
const match = path.match(/^Projects\/([^/]+)\/([^/]+)\/designs\/[^/]+\.md$/);
const projectLink = match ? `[[Projects/${match[1]}/${match[2]}]]` : "";
-%>
---
project: "<% projectLink %>"
gdoc_id:
gdoc_url:
gdoc_source_of_truth: markdown
gdoc_role:
gdoc_tab_title:
gdoc_last_published_sha:
gdoc_last_published_at:
gdoc_last_comment_sync:
gdoc_revision_id:
gdoc_last_exported_at:
---

# <% tp.file.title %>

## Project

- <% projectLink || "Set project to [[Projects/<Domain>/<Project>]]" %>

## Google Doc

- Review surface: add or confirm `gdoc_url`
- Use `gdoc_role` and `gdoc_tab_title` when this note is one tab in a shared review doc

## Problem

<% tp.file.cursor(1) %>

## Approach

- 

## Open Questions

- 
