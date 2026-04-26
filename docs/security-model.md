# Security Model

This project is personal-use first, but it still treats secrets and user actions carefully.

## Never Store

- Gmail password
- X password
- Wallet seed phrases
- Wallet private keys
- Raw long-term terminal secrets in logs

## Sensitive Storage

OAuth refresh tokens and API keys should use OS-protected secure storage where practical. SQLite should only store metadata, cached display data, and non-secret settings unless encryption is explicitly added.

## Confirmation Rules

- Email sending requires visible confirmation in v1.
- Permanent email deletion is disabled by default.
- Transaction signing is blocked from the app in v1.
- Terminal commands can run, but dangerous-command warning gates should be added before broad terminal use.

## Audit Events

The backend should log security-relevant events such as email send, wallet connect/disconnect, API key changes, terminal commands, notes export, and settings changes.

