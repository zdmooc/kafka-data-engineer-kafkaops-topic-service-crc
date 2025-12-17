# Topic naming conventions

Recommended format (example):
- `<domain>.<entity>.<event>.<version>`
- Example: `billing.invoice.created.v1`

Rules:
- lowercase
- dot-separated segments
- version suffix `v1`, `v2`, ...

Special topics:
- DLQ: `<topic>.dlq.<version>`
- Retry: `<topic>.retry.<version>`
- Audit: `audit.<domain>.<version>`
