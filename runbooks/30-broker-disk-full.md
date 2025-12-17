# Broker disk full / log dir failure

## Symptoms
- Disk usage near 100%
- Broker log dir warnings/errors
- Partition offline / replication issues

## Immediate actions
- Stop non-critical producers
- Increase retention pressure (temporary reduce retention.ms for non-critical topics)
- Add disk / expand volume if possible (cloud)
- Avoid compaction storms

## Follow-up
- Capacity planning review
- Retention policies governance via Topic-as-a-Service
