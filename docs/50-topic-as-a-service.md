# Topic as a Service

## Goal
Provide a safe and standardized way to create/manage Kafka topics:
- naming conventions
- retention and cleanup policy templates
- ownership and metadata labels
- approval model (future) and audit trail

## API surface (implemented)
- `GET /health`
- `GET /v1/topics`
- `POST /v1/topics` (create)
- `GET /v1/topics/{name}`
- `POST /v1/topics/{name}/configs` (alter configs)
- `DELETE /v1/topics/{name}` (guarded)

## Governance examples
- Enforce topic name regex
- Enforce mandatory labels: `owner`, `env`
- Restrict destructive operations (delete requires explicit confirmation)
- Offer predefined retention profiles per environment

## Future extensions
- RBAC via IAM (JWT/OIDC)
- Integration with ticketing/approval workflows
- Quotas (max partitions, max retention) by team
- Event-based audit (publish to an audit topic)
