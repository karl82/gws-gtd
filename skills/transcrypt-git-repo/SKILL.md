---
name: transcrypt-git-repo
description: Guidance for bootstrapping, operating, verifying, rekeying, and troubleshooting transcrypt-based transparent encryption in a Git repository.
---

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
