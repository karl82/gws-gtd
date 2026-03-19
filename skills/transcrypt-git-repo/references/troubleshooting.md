# Troubleshooting

## Deprecated Key Derivation Warning

Symptom during Git operations:

```text
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
```

Cause:

- Upstream transcrypt uses `-md MD5` which triggers warnings on OpenSSL 3.

Fix:

Use the patched transcrypt from this skill's `scripts/transcrypt`, which replaces
`-md MD5` with `-pbkdf2 -iter 256000 -md sha512`. This eliminates the warning
and uses modern key derivation.

Additionally, on macOS point transcrypt at LibreSSL:

```bash
git config transcrypt.openssl-path /usr/bin/openssl
```

Then verify:

```bash
git status
```

## SHA-512 vs sha512 — LibreSSL Case Sensitivity

Symptom:

- LibreSSL rejects `SHA-512` as an unknown digest.

Cause:

- LibreSSL requires lowercase digest names (`sha512`), while OpenSSL 3 accepts
  both `SHA-512` and `sha512`.

Fix:

- Always use lowercase `sha512` in the `-md` flag, never `SHA-512`.
- The patched transcrypt in `scripts/transcrypt` already uses the correct form.

## File Appears Unencrypted In Index

Symptom:

- pre-commit hook reports that a transcrypt-managed file is not encrypted.

Fix:

```bash
git rm --cached -- path/to/file
git add path/to/file
```

## Clone Does Not Decrypt

Checklist:

- cipher and password match the origin repository
- `transcrypt --display` shows expected values
- `.gitattributes` contains `filter=crypt diff=crypt merge=crypt` for target paths
- file is tracked and matches an encrypted pattern

## Rekey Safety

If rekey is required:

- run only on a clean working tree
- commit rekeyed files immediately
- notify collaborators to refresh credentials before continuing work
