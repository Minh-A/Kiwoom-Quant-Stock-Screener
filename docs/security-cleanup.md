# Security Cleanup

This repository was cleaned before publication.

## Findings

- `Conditional/Condition3_main.py`: a commented Slack bot token was present in the old notification example.
- `Conditional/Condition4_Beta.py`: the same commented Slack bot token was present in the beta condition file.
- `Conditional/__pycache__/` and `kiwoom/__pycache__/`: compiled Python cache files contained local Windows source paths. These generated files were removed locally and ignored by Git.

## Changes

- Removed the hardcoded Slack token from source code.
- Replaced the old Slack example with `utils/notifier.py`, which reads `SLACK_BOT_TOKEN` and `SLACK_CHANNEL` from local environment variables.
- Added `.env.example` with placeholder environment variables only.
- Ignored runtime output files and generated Python caches in `.gitignore`.

If the old Slack token was still active, it should be revoked and reissued from Slack before any future use.
