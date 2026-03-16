# Workflow

## 1) Bootstrap

1. Back up vault files outside of git.
2. Confirm clean working tree.
3. Discard plaintext history by creating an orphan branch:
   ```bash
   git checkout --orphan fresh
   git add .
   git commit -m "initial commit"
   git branch -D main
   git branch -m main
   ```
4. Run transcrypt with agreed cipher and password:
   ```bash
   transcrypt -c aes-256-cbc -p 'your-strong-password'
   ```
5. Configure `.gitattributes` to encrypt all vault files:
   ```bash
   echo '*' >> .gitattributes
   echo '.gitattributes !filter !diff' >> .gitattributes
   git add .gitattributes && git commit -m "enable transcrypt encryption"
   git add . && git commit -m "encrypted vault"
   ```
6. Force push to remote:
   ```bash
   git push --force origin main
   ```
7. Verify remote stores only ciphertext:
   ```bash
   git clone <remote-url> /tmp/vault-check
   cat /tmp/vault-check/some-note.md  # should show binary ciphertext
   ```
8. Store transcrypt password securely (e.g. 1Password).
9. Share credentials through a secure out-of-band channel.

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
