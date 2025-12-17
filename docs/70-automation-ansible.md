# Automation (Ansible)

## Why
- repeatability (idempotent playbooks)
- safer operations (standard checks)
- evidence capture (before/after changes)

## What is included
- `playbooks/10-kafka-health.yml` : baseline health
- `playbooks/20-apply-topic-catalog.yml` : apply declarative topics
- `playbooks/30-collect-evidence.yml` : snapshots for audits/postmortems

## Inventory patterns
- `inventories/local/` demonstrates local docker usage
- `inventories/sample-prod/` shows structure for multi-DC / worldwide platforms

Note: adapt connection method (SSH/bastion/Ansible AWX) to your organization.
