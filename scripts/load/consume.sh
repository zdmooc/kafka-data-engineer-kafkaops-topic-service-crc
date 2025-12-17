#!/usr/bin/env bash
set -euo pipefail

BOOTSTRAP="${1:-localhost:9092}"
TOPIC="${2:-demo.orders.v1}"

echo "Consuming from $TOPIC on $BOOTSTRAP (Ctrl+C to stop)"

docker exec -it kafka /opt/bitnami/kafka/bin/kafka-console-consumer.sh   --bootstrap-server "$BOOTSTRAP" --topic "$TOPIC" --from-beginning
