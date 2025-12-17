# Consumer lag spike

## Symptoms
- Lag rising for one or more consumer groups
- Throughput drop or processing backlog

## First triage questions
- Is producer rate up?
- Did partitions increase (rebalance impact)?
- Is consumer erroring (auth, schema, downstream dependency)?
- Is broker request latency increasing?

## Immediate actions
- Scale consumers (if safe)
- Investigate downstream dependency saturation
- If rebalancing: prefer cooperative; reduce churn (max.poll.interval, session timeouts)

## Tools
- `kafkaops lag`
- Consumer logs in Elastic/OpenSearch
