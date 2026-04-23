## GWS Command Reference

Patterns and gotchas for `gws gmail` API calls discovered during live sessions.

### threads.modify — label changes

Use `--json` for the request body, NOT `--params`:

```bash
# Correct — archive a thread (remove INBOX)
gws gmail users threads modify \
  --params '{"userId":"me","id":"<thread_id>"}' \
  --json '{"removeLabelIds":["INBOX"]}'

# Correct — add a label
gws gmail users threads modify \
  --params '{"userId":"me","id":"<thread_id>"}' \
  --json '{"addLabelIds":["<label_id>"]}'
```

Do NOT put `removeLabelIds`/`addLabelIds` inside `--params` — the API will either ignore them or return `"No label add or removes specified"`.

### threads.trash / threads.untrash

Use dedicated endpoints, not `threads.modify` with a TRASH label:

```bash
gws gmail users threads trash \
  --params '{"userId":"me","id":"<thread_id>"}'

gws gmail users threads untrash \
  --params '{"userId":"me","id":"<thread_id>"}'
```

### messages.batchModify

Requires **message IDs**, not thread IDs. Passing thread IDs returns `"No message ids specified"`.

To get message IDs from a thread, use `gws gmail users threads get` or note that single-message threads have `message_id == thread_id`.

```bash
gws gmail users messages batchModify --params '{
  "userId": "me",
  "requestBody": {
    "ids": ["<message_id_1>", "<message_id_2>"],
    "addLabelIds": ["TRASH"],
    "removeLabelIds": ["INBOX"]
  }
}'
```

### +forward

Requires a message ID (not thread ID):

```bash
gws gmail +forward --message-id <message_id> --to plans@tripit.com
```

For single-message threads the message ID equals the thread ID.

### Inbox triage query

Use `in:inbox` (not `is:unread`) to get all inbox threads regardless of read state or age:

```bash
gws gmail +triage --format json --labels --max 250 --query 'in:inbox'
```

For snippet retrieval across all threads in one call:

```bash
gws gmail users threads list --params '{"userId":"me","q":"in:inbox","maxResults":500}' --format json
```

`messages.list` returns IDs only even with `--fields` — use `threads.list` for snippets.
