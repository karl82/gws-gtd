# Troubleshooting

## Deprecated Key Derivation Warning

Symptom during Git operations:

```text
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
```

Cause:

- transcrypt relies on legacy OpenSSL KDF parameters for compatibility.
- OpenSSL 3 emits warnings on each clean/smudge invocation.

Mitigation on macOS when LibreSSL is available:

```bash
git config transcrypt.openssl-path /usr/bin/openssl
```

Then verify:

```bash
git status
```

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
