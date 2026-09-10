# Security

## Current credential policy

This repository must not contain plaintext usernames, passwords, PINs, API keys, private user databases, keystores, or deployment secrets.

Runtime secrets are supplied through environment variables:

- `OPENAI_API_KEY`
- `MEDCARE_ADMIN_USERNAME`
- `MEDCARE_ADMIN_PASSWORD`
- `MEDCARE_ADMIN_PIN`

The `.env` file and Streamlit secrets file are intentionally ignored by Git.

## Important history-remediation note

If a secret was ever committed to Git, removing it from the current branch does **not** make that secret safe again. Rotate/revoke the exposed credential first, then remove the sensitive material from Git history with an approved history-rewriting tool such as `git filter-repo`, and force-push only after reviewing the rewritten history.

This project is a portfolio/demo application and is not a substitute for validated clinical decision support.
