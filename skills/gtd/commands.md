# GWS Commands

Patterns and gotchas for `gws` Gmail / Calendar / People CLI calls discovered during real use.

Always pass `--format json`. Always use `jq` (not `python3 -c`) for JSON parsing in Bash. See `reference.md § Interaction rules`.

When piping `gws ... --format json` into `jq`, redirect stderr: `gws ... --format json 2>/dev/null | jq ...`. The CLI prints `Using keyring backend: ...` and other diagnostics that mix into stdout in some shells and break `jq` parsing. Suppress them.

## Gmail

### `threads.modify` — label changes

Use `--json` for the request body. NOT `--params`.

```bash
# Archive a thread (remove INBOX)
gws gmail users threads modify \
  --params '{"userId":"me","id":"<thread_id>"}' \
  --json '{"removeLabelIds":["INBOX"]}'

# Add a label
gws gmail users threads modify \
  --params '{"userId":"me","id":"<thread_id>"}' \
  --json '{"addLabelIds":["<label_id>"]}'
```

Don't put `removeLabelIds` / `addLabelIds` inside `--params` — the API ignores them or returns `"No label add or removes specified"`.

### `threads.trash` / `threads.untrash`

Dedicated endpoints. Don't use `threads.modify` with a TRASH label.

```bash
gws gmail users threads trash \
  --params '{"userId":"me","id":"<thread_id>"}'

gws gmail users threads untrash \
  --params '{"userId":"me","id":"<thread_id>"}'
```

### `messages.batchModify`

Requires **message IDs**, not thread IDs. Passing thread IDs returns `"No message ids specified"`.

To get message IDs from a thread, use `gws gmail users threads get`. Single-message threads have `message_id == thread_id`.

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

### `+forward`

Requires a message ID, not a thread ID.

```bash
gws gmail +forward --message-id <message_id> --to plans@tripit.com
```

For single-message threads, message ID equals thread ID.

### `+reply` — reply target pitfall

`gws gmail +reply --message-id <ID>` sends the reply to the **sender** of that message. So:

- Pointing at a message **from the other party** → reply goes to them. ✓ Correct for nudges and follow-ups.
- Pointing at **your own outgoing message** → reply goes to **yourself**. ✗ Wrong, and easy to miss because the thread looks correct.

When following up on a stalled thread where your last email got no response, find the last message **from the other party** (often several messages back) and reply to that. Verify with `gws gmail +read --id <reply_id> --headers` after sending — `From` and `To` should both make sense.

```bash
# Find last non-self message in a thread
gws gmail users threads get --params '{"userId":"me","id":"<thread_id>","format":"metadata"}' --format json 2>/dev/null \
  | jq '[.messages[] | {id, from: (.payload.headers[] | select(.name=="From") | .value)}] | map(select(.from | contains("karel.rank") | not)) | last'
```

### Inbox triage query

Use `in:inbox` (not `is:unread`) to get all inbox threads regardless of read state or age.

```bash
gws gmail +triage --format json --labels --max 250 --query 'in:inbox'
```

### Snippet retrieval across all threads

For one round-trip retrieval of `id` + `snippet` across all candidate threads:

```bash
gws gmail users threads list --params '{"userId":"me","q":"in:inbox","maxResults":500}' --format json
```

`messages.list` returns IDs only even with `--fields` — use `threads.list` for snippets.

## Calendar

### Agenda fetch

```bash
gws calendar +agenda --today --format json
gws calendar +agenda --tomorrow --format json
gws calendar +agenda --week --format json
```

Returns events with `summary`, `start`, `end`, `attendees`, `description`, `location`, `id`.

### Event creation

```bash
gws calendar +insert --summary "<title>" --start "<ISO>" --end "<ISO>" --location "<loc>" --format json
```

Used by appointment triage when the email has no matching calendar event.

### Event patch (reschedule)

```bash
gws calendar +patch --id "<event_id>" --start "<ISO>" --end "<ISO>" --format json
```

Used by appointment triage when the email is a reschedule.

### Auth and scope

Calendar operations require the calendar scope in the `gws` auth config. On `insufficientPermissions`, report the setup blocker and proceed without calendar operations.

## People

### Contact lookup

```bash
gws people people searchContacts --params '{"query":"<name-or-email>","readMask":"names,emailAddresses,phoneNumbers"}' --format json
```

Exact-match lookup by email or name.

### Directory search

```bash
gws people people searchDirectoryPeople --params '{"query":"<q>","sources":["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"],"readMask":"names,emailAddresses"}' --format json
```

### Other contacts

```bash
gws people otherContacts search --params '{"query":"<q>","readMask":"names,emailAddresses"}' --format json
```

### Auth and scope

People operations require the contacts scope. On `insufficientPermissions`, report the setup blocker and proceed without people operations.
