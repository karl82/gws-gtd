## gws Command Reference

Use this reference when you need exact `gws` commands for GTD ceremonies or one-off Google Workspace maintenance.

### Core CLI Pattern

- Generic form: `gws <service> <resource> [sub-resource] <method> [flags]`
- Helper form: `gws <service> +<helper> [flags]`
- Schema lookup: `gws schema <service.resource.method>`

Shared flags:

- `--params '<json>'` for query/path params on GET-style calls
- `--json '<json>'` for request bodies on POST/PATCH/PUT calls
- `--format json|table|yaml|csv` for output shaping
- `--page-all` to auto-paginate list calls
- `--dry-run` to validate a request before sending it

### Safety Order

Prefer the least risky operation that solves the problem:

1. inspect: `+triage`, `threads.list`, `threads.get`, `messages.get`
2. label: `threads.modify`, `messages.batchModify`
3. archive: remove `INBOX` label
4. trash: `threads.trash`, `messages.trash`, `messages.batchModify` with `TRASH`

### Auth and Discovery

- `gws auth status`
  - Use when: verifying the current token and enabled services.
- `gws auth login --scopes "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/contacts.readonly"`
- Preserve current broad scopes and add contacts read access:
  - `gws auth login --scopes "email,openid,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts.readonly,https://www.googleapis.com/auth/gmail.compose,https://www.googleapis.com/auth/gmail.insert,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email"`
  - Use when: re-authing with least privilege for the GTD workflow.
- `gws auth logout`
  - Use when: clearing a stale token before re-auth.
- `gws schema gmail.users.threads.list`
  - Use when: you need the exact request params, scopes, or response shape for a raw method.
- `gws schema calendar.events.list`
  - Use when: building a precise event query.

### Gmail: Fast Inspection

- `gws gmail +triage`
  - Use when: you want a quick unread inbox snapshot.
- `gws gmail +triage --max 10 --query 'label:gtd/import -label:gtd/imported' --format table`
  - Use when: checking the GTD import queue.
- `gws gmail +triage --max 20 --query 'category:promotions older_than:6m' --labels`
  - Use when: scouting old promotional mail before cleanup.
- `gws gmail users labels list --params '{"userId":"me"}'`
  - Use when: checking whether labels already exist or resolving label IDs.
- `gws gmail users threads list --params '{"userId":"me","q":"from:alice@example.com newer_than:30d","maxResults":25}'`
  - Use when: getting candidate thread IDs for a focused review.
- `gws gmail users threads get --params '{"userId":"me","id":"<thread-id>"}'`
  - Use when: inspecting the full conversation before labeling, archiving, or trashing.
- `gws gmail users messages get --params '{"userId":"me","id":"<message-id>","format":"metadata","metadataHeaders":"From,Subject,List-Unsubscribe"}'`
  - Use when: checking sender/subject/unsubscribe metadata without fetching the whole message.

### Gmail: Label and Queue Management

- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd","labelListVisibility":"labelShow","messageListVisibility":"hide"}'`
  - Use when: bootstrapping the GTD parent label before any `gtd/...` children.
- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd/import","labelListVisibility":"labelShow","messageListVisibility":"show"}'`
  - Use when: bootstrapping a missing GTD child label after the `gtd` parent already exists.
- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd/waiting","labelListVisibility":"labelShow","messageListVisibility":"show"}'`
- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd/review","labelListVisibility":"labelShow","messageListVisibility":"show"}'`
- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd/reference","labelListVisibility":"labelShow","messageListVisibility":"show"}'`
- `gws gmail users labels create --params '{"userId":"me"}' --json '{"name":"gtd/imported","labelListVisibility":"labelHide","messageListVisibility":"hide"}'`
  - Use when: completing the full structured GTD label bootstrap on a new account.
- `gws gmail users settings filters create --params '{"userId":"me"}' --json '{"criteria":{"to":"<your-address>+gtd@gmail.com"},"action":{"addLabelIds":["<gtd-import-label-id>"]}}'`
  - Use when: creating the single Gmail capture alias rule.
- `gws gmail users settings filters list --params '{"userId":"me"}'`
  - Use when: verifying that the capture alias filter already exists.
- `gws gmail users labels get --params '{"userId":"me","id":"INBOX"}'`
  - Use when: inspecting a system label or verifying its exact ID/name.
- `gws gmail users threads modify --params '{"userId":"me","id":"<thread-id>"}' --json '{"addLabelIds":["Label_123"],"removeLabelIds":["INBOX"]}'`
  - Use when: applying a user label and archiving the entire conversation in one step.
- `gws gmail users threads modify --params '{"userId":"me","id":"<thread-id>"}' --json '{"addLabelIds":["Label_456"]}'`
  - Use when: routing a whole thread into the waiting queue after resolving the label ID for `gtd/waiting`.
- `gws gmail users messages batchModify --params '{"userId":"me"}' --json '{"ids":["<message-1>","<message-2>"],"removeLabelIds":["UNREAD"]}'`
  - Use when: performing the same label change across many specific messages.
- `gws gmail users messages batchModify --params '{"userId":"me"}' --json '{"ids":["<message-1>","<message-2>"],"addLabelIds":["TRASH"]}'`
  - Use when: moving many specific messages to Trash in one call after review.

Notes:

- Gmail system labels such as `INBOX`, `UNREAD`, and `TRASH` can be used directly.
- `messages.batchModify` with `addLabelIds:["TRASH"]` works in practice for batch trashing specific messages, even though Gmail's docs emphasize the dedicated `trash` methods.
- User-created labels usually need their actual label ID from `users.labels.list`.
- Prefer `threads.modify` when your intent is conversation-level cleanup.

### Gmail: Trash, Restore, and Permanent Removal

- `gws gmail users threads trash --params '{"userId":"me","id":"<thread-id>"}'`
  - Use when: removing an entire conversation while keeping recovery possible.
- `gws gmail users threads untrash --params '{"userId":"me","id":"<thread-id>"}'`
  - Use when: restoring a thread you moved by mistake.
- `gws gmail users messages trash --params '{"userId":"me","id":"<message-id>"}'`
  - Use when: only one message in a thread should be trashed.
- `gws gmail users messages batchModify --params '{"userId":"me"}' --json '{"ids":["<message-1>","<message-2>"],"addLabelIds":["TRASH"]}'`
  - Use when: trashing many exact messages at once while keeping recovery possible.
- Ready-made reviewed-ID snippet:
  ```bash
  gws gmail users messages batchModify \
    --params '{"userId":"me"}' \
    --json '{"ids":["<reviewed-message-1>","<reviewed-message-2>","<reviewed-message-3>"],"addLabelIds":["TRASH"]}'
  ```
  - Use when: the review step already produced the exact message IDs to trash.

### Gmail: Composing and Replying (Mandatory)

Always use these helpers for outbound email. Never construct raw MIME or call `users.messages.send` directly. Always show the user a draft and get explicit confirmation before sending.

- `gws gmail +send --to alice@example.com --subject 'Hello' --body 'Quick note'`
  - Use when: sending a new plain-text message.
  - Do not use for replies to existing threads.
- `gws gmail +reply --message-id '<message-id>' --body 'Quick reply'`
  - Use when: replying inside an existing Gmail thread. Handles `In-Reply-To` and `References` threading automatically.
- `gws gmail +reply-all --message-id '<message-id>' --body 'Quick reply'`
  - Use when: replying to all recipients of an existing thread.
- `gws gmail +forward --message-id '<message-id>' --to 'bob@example.com' --body 'FYI'`
  - Use when: forwarding a message to new recipients.
- `gws gmail +watch --project <gcp-project> --label-ids INBOX --once`
  - Use when: debugging new-mail capture or a watcher workflow.
- `gws gmail users getProfile --params '{"userId":"me"}'`
  - Use when: confirming the authenticated mailbox address.

### Calendar: Read and Review

- `gws calendar +agenda --today --format table`
  - Use when: checking today's meeting load quickly.
- `gws calendar +agenda --days 7 --format json`
  - Use when: comparing upcoming events against due-date pressure in weekly review.
- `gws calendar calendarList list --params '{}' --format table`
  - Use when: discovering available calendar IDs/names.
- `gws calendar events list --params '{"calendarId":"primary","timeMin":"2026-03-09T00:00:00Z","timeMax":"2026-03-16T00:00:00Z","singleEvents":true,"orderBy":"startTime"}'`
  - Use when: pulling a precise date range from one calendar.
- `gws calendar events get --params '{"calendarId":"primary","eventId":"<event-id>"}'`
  - Use when: inspecting one event before creating a note or patching details.

### Calendar: Write and Update

- `gws calendar +insert --summary 'Follow-up block' --start '2026-03-10T14:00:00-05:00' --end '2026-03-10T14:30:00-05:00'`
  - Use when: creating a simple one-off reminder block quickly.
- `gws calendar events patch --params '{"calendarId":"primary","eventId":"<event-id>","sendUpdates":"none"}' --json '{"description":"Updated notes"}'`
  - Use when: making a minimal change without notifying attendees.
- `gws calendar events delete --params '{"calendarId":"primary","eventId":"<event-id>","sendUpdates":"none"}'`
  - Use when: removing an event and suppressing extra attendee mail.

### People: Contacts and Linking

- `gws people people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses,metadata","pageSize":1000}'`
  - Use when: building the People-note matching set.
- `gws people people searchContacts --params '{"query":"Alice","readMask":"names,emailAddresses"}'`
  - Use when: finding a contact quickly by name or email fragment.
- `gws people people get --params '{"resourceName":"people/c123456789","personFields":"names,emailAddresses,phoneNumbers"}'`
  - Use when: inspecting one known contact record.
- `gws people people listDirectoryPeople --params '{"readMask":"names,emailAddresses","sources":"DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"}'`
  - Use when: searching a Workspace directory, not just personal contacts.

### Ad-Hoc Gmail Maintenance Recipes

#### Clean old promotional mail

1. Preview candidates:
   - `gws gmail +triage --max 25 --query 'category:promotions older_than:6m' --labels`
2. Get thread IDs for exact review:
   - `gws gmail users threads list --params '{"userId":"me","q":"category:promotions older_than:6m","maxResults":100}'`
3. Inspect any thread you are unsure about:
   - `gws gmail users threads get --params '{"userId":"me","id":"<thread-id>"}'`
4. Trash reversible candidates:
   - `gws gmail users threads trash --params '{"userId":"me","id":"<thread-id>"}'`

Use when: clearing old newsletters or promotional threads without risking immediate data loss.

#### Archive old automated notifications

1. Find candidates:
   - `gws gmail users threads list --params '{"userId":"me","q":"from:notifications@github.com older_than:90d -is:starred","maxResults":100}'`
2. Archive one reviewed thread:
   - `gws gmail users threads modify --params '{"userId":"me","id":"<thread-id>"}' --json '{"removeLabelIds":["INBOX"]}'`

Use when: messages are worth keeping for search/history but no longer belong in the inbox.

#### Review large old emails before cleanup

- `gws gmail +triage --max 20 --query 'larger:10M older_than:1y has:attachment'`
- `gws gmail users threads list --params '{"userId":"me","q":"larger:10M older_than:1y has:attachment","maxResults":100}'`

Use when: identifying bulky historical mail that may be worth archiving, labeling, or trashing.

#### Check whether a newsletter supports unsubscribe

1. Find candidate mail:
   - `gws gmail users messages list --params '{"userId":"me","q":"category:promotions newer_than:30d","maxResults":20}'`
2. Inspect unsubscribe headers for one message:
   - `gws gmail users messages get --params '{"userId":"me","id":"<message-id>","format":"metadata","metadataHeaders":"From,Subject,List-Unsubscribe,List-Unsubscribe-Post"}'`

Use when: deciding whether cleanup should be one-time trashing or a real unsubscribe follow-up.

#### Sweep stale waiting threads

- `gws gmail +triage --max 25 --query 'label:gtd/waiting older_than:14d' --labels`
- `gws gmail users threads list --params '{"userId":"me","q":"label:gtd/waiting older_than:14d","maxResults":100}'`

Use when: weekly review needs a quick view of external dependencies that may need follow-up.

#### Verify GTD capture queues

- `gws gmail +triage --max 10 --query 'label:gtd/import -label:gtd/imported' --format json`
- `gws gmail +triage --max 10 --query 'label:gtd/waiting' --format json`
- `gws gmail +triage --max 10 --query 'in:inbox newer_than:2d -label:gtd/import -label:gtd/waiting -label:gtd/review -label:gtd/reference -label:gtd/imported' --format json`

Use when: checking whether alias-routed capture is landing correctly and whether unlabeled mail still needs triage.

### Query Design Tips

- Gmail query operators live inside `q`, for example: `older_than:6m`, `newer_than:7d`, `has:attachment`, `category:promotions`, `label:gtd/import`, `-is:starred`.
- Start with the narrowest safe query and a small `maxResults` before widening scope.
- If a cleanup plan feels risky, add a temporary review label first, then decide what to archive or trash.
- Use `threads.list` plus `threads.get` when conversation context matters.
- Use `messages.get` with `format=metadata` when you only need headers like `List-Unsubscribe`.
