# Command Reference

## Inspect Current State

```bash
git status --short
transcrypt --display
git ls-crypt
```

## Bootstrap In Current Repository

```bash
transcrypt -c aes-256-cbc -p '<shared-password>'
```

## Add Encrypted Patterns

Use one line per pattern in `.gitattributes`:

```text
secrets/** filter=crypt diff=crypt merge=crypt
*.env filter=crypt diff=crypt merge=crypt
```

Then stage and commit:

```bash
git add .gitattributes
git add secrets/.env
git commit -m "Enable transcrypt for secret files"
```

## Clone Onboarding

After cloning a repository that already uses transcrypt:

```bash
transcrypt -c aes-256-cbc -p '<shared-password>'
git status
```

## Verify Encryption In Git Object

```bash
transcrypt --show-raw path/to/secret.file
```

Expected encrypted payload usually starts with `U2FsdGVk`.

## Rekey

```bash
transcrypt --rekey -c aes-256-cbc -p '<new-shared-password>'
git status
git commit -m "Rotate transcrypt credentials"
```

## Flush Local Credentials

```bash
transcrypt --flush-credentials
```

## OpenSSL Path Override

```bash
git config transcrypt.openssl-path /usr/bin/openssl
```
