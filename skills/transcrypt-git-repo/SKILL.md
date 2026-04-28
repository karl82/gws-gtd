---
name: transcrypt-git-repo
description: Use when setting up, cloning, verifying, rekeying, or troubleshooting transcrypt transparent encryption in a git repository.
---

# transcrypt-git-repo

## Purpose

Use this skill when a repository needs transparent encryption with transcrypt.

## Supported Modes

- `transcrypt-bootstrap`
- `transcrypt-add-pattern`
- `transcrypt-clone-onboarding`
- `transcrypt-verify`
- `transcrypt-rekey`
- `transcrypt-troubleshoot`

## Router

1. Resolve the transcrypt intent.
2. Use the matching references:
   - overview -> `README.md`
   - workflow -> `references/workflow.md`
   - exact commands -> `references/command-reference.md`
   - warnings or failures -> `references/troubleshooting.md`
3. Prefer non-destructive checks first.

## Guardrails

- Do not expose transcrypt passwords.
- Do not commit plaintext secrets.
- Do not rekey while uncommitted changes are present unless the user explicitly accepts the risk.
- Keep `.gitattributes` committed so encryption rules are shared.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Rekeying with uncommitted changes present | Commit or stash all changes first |
| Passing password via shell argument | Use the interactive prompt or env var — shell args land in history |
| Forgetting to commit `.gitattributes` after adding a pattern | New patterns are local-only until `.gitattributes` is committed and pushed |
| Cloning without running `transcrypt -C` | Run clone onboarding to decrypt; the repo will appear as ciphertext otherwise |
