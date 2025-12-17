# SOPs (standard operating procedures)

## Add a topic (production)
1. PR to `catalog/topics/prod.yaml`
2. Review: naming + retention + ownership + partitions strategy
3. Apply with playbook (maintenance window if needed)
4. Evidence capture (before/after)
5. Communicate to worldwide teams (EN update + links)

## Delete a topic (production)
- Prefer deprecate -> retention -> archive -> delete
- Never delete without confirming:
  - consumers migrated
  - data retention requirements met
  - rollback strategy agreed
