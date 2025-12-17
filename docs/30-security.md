# Security baseline (Kafka)

## Authentication
- Prefer **mTLS** or **SASL/SCRAM** (or SASL/OAUTHBEARER depending on IAM)
- Keep secrets in Vault / KMS, not in repos

## Authorization
- Use **ACLs** with least privilege
- Separate admin ops from application identities
- Consider prefix-based ACLs for topic naming conventions:
  - `team.domain.*` patterns
  - `dlq.*` patterns

## Network
- Segmentation between producers/consumers and brokers
- Restrict inter-broker communication to broker subnets
- Prefer private endpoints / VPN for worldwide access

## Audit
- Store admin changes (topic create/delete/config changes, ACL changes)
- Index audit events in OpenSearch/Elastic for investigation

Repo support:
- Topic-as-a-Service emits audit records (stdout JSON + optional OpenSearch sink)
- Catalog-based approach provides Git traceability of topic lifecycle
