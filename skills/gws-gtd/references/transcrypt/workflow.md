# Workflow

## 1) Bootstrap

1. Confirm clean working tree.
2. Run transcrypt with agreed cipher and password.
3. Add encrypted patterns to `.gitattributes`.
4. Stage and commit encrypted files and attributes.
5. Share credentials through a secure out-of-band channel.

## 2) Add Pattern

1. Add a new `.gitattributes` pattern with `filter=crypt diff=crypt merge=crypt`.
2. Re-stage affected files so filters re-run.
3. Verify with `transcrypt --show-raw <file>`.
4. Commit pattern and file updates together.

## 3) Clone Onboarding

1. Clone repository.
2. Run transcrypt using shared cipher and password.
3. Validate decrypted working tree opens correctly.
4. Run `git status` to confirm clean state.

## 4) Verify

1. List encrypted files with `git ls-crypt`.
2. Check one or more files with `transcrypt --show-raw`.
3. Confirm payload appears encrypted in Git object storage.

## 5) Rekey

1. Ensure clean tree and coordinate timing with collaborators.
2. Run `transcrypt --rekey` with new credentials.
3. Commit immediately.
4. Ask collaborators to flush old credentials, pull, and reinitialize.

## 6) Troubleshoot

1. Capture exact warning or failure text.
2. Confirm `transcrypt --display` and filter config.
3. Apply targeted fixes from `troubleshooting.md`.
4. Re-run verification commands.
