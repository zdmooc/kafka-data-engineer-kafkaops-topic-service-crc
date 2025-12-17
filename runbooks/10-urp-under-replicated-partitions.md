# Under-Replicated Partitions (URP)

## What it means
A partition has fewer in-sync replicas than its replication factor.
Risk: reduced durability and availability.

## Quick checks
- Validate scope:
  - Is it one broker or multiple?
  - Is it a single topic or many?
- Check disk usage and IO latency.
- Check broker logs for replica fetcher errors.

## Immediate actions (safe)
- Reduce load if possible (throttle producers)
- Avoid unplanned broker restarts if disk/network is unstable
- If a broker is down: restore broker or reassign partitions (planned)

## Investigation pointers
- ISR shrink frequency
- Network saturation between brokers
- Disk full / slow disk
- Controller instability

## Verification
- URP returns to 0 for critical topics
- ISR stable
