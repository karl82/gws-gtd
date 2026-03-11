# Transcrypt Overview

`transcrypt-git-repo` is a reusable operations skill for enabling transcrypt in any Git repository.

## What It Covers

- bootstrapping transcrypt in an existing repository
- adding or adjusting encrypted file patterns in `.gitattributes`
- onboarding a cloned repository with known credentials
- verifying that encrypted files are actually encrypted in Git history and index
- rekeying safely when credentials must rotate
- troubleshooting common OpenSSL and filter warnings

## Prerequisites

- Git available in `PATH`
- `transcrypt` installed and executable
- `openssl` available (or explicitly configured with `transcrypt.openssl-path`)
- a clean working tree before bootstrap, rekey, or force checkout operations

## Quick Start

1. Initialize transcrypt in a target repository.
2. Add encrypted path patterns in `.gitattributes`.
3. Stage and commit both `.gitattributes` and encrypted files.
4. Share cipher and password securely with collaborators.
5. On each clone, run transcrypt with matching credentials.

See `references/transcrypt/workflow.md` and `references/transcrypt/command-reference.md` for exact commands.

## Important Compatibility Note

If Git operations print:

`*** WARNING : deprecated key derivation used. Using -iter or -pbkdf2 would be better.`

see `references/transcrypt/troubleshooting.md` for the OpenSSL compatibility fix.
