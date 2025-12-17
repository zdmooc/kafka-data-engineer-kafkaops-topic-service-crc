# Performance & capacity notes

## Topic design
- Partition count impacts parallelism and overhead
- Rule of thumb: scale partitions with consumer parallelism, not with message volume only
- Keep replication factor aligned with AZ strategy (typically 3 in prod)

## Broker tuning (high-level)
- Disk is usually the bottleneck (IOPS, throughput, latency)
- Control log segment sizes, retention, and compaction policies
- Watch request handler pools, network threads, page cache usage

## Producer tuning
- `acks=all` for durability, tune `linger.ms`, `batch.size`, `compression.type`
- Idempotence for exactly-once-ish delivery semantics at producer level

## Consumer tuning
- Use cooperative rebalancing where possible
- Monitor lag as **symptom**, not a goal: analyze end-to-end throughput

## Benchmark approach
- Define target throughput + latency + error budget
- Run controlled load tests (kcat or custom producer/consumer)
- Capture metrics (request latency, ISR, disk, GC, network)

See `scripts/load/` for examples.
