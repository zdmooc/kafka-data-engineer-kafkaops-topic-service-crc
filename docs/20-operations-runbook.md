# Operations (Day-2) playbook

## Daily checks (baseline)
1. Cluster health (brokers, controller, metadata)
2. Under-Replicated Partitions (URP)
3. ISR shrink events
4. Consumer group lag (critical apps)
5. Disk usage / log segment growth
6. Controller events / leader elections
7. Network errors / request latency spikes

Tools in this repo:
- `kafkaops health`
- `kafkaops lag`
- `kafkaops topics list/describe`
- Runbooks in `runbooks/`

## Change management (safe operations)
- Prefer declarative topic catalog + PR review (`catalog/topics/*.yaml`)
- Use maintenance windows for broker config changes
- Capture evidence before/after (`ansible/playbooks/30-collect-evidence.yml`)
- Post-change validation: URP, ISR, lag, produce/consume smoke tests

## Incident workflow (minimal)
1. Triage (impact + scope)
2. Stabilize (reduce traffic, pause rebalancing, protect brokers)
3. Diagnose (logs/metrics, partition state, request handlers, disk/network)
4. Fix (targeted action)
5. Verify (SLO recovery)
6. Postmortem (timeline + corrective actions)

See `runbooks/00-incident-template.md`.
