#!/usr/bin/env bash
set -euo pipefail

BOOTSTRAP="${1:-localhost:9092}"
TOPIC="${2:-demo.orders.v1}"
COUNT="${3:-100}"

echo "Producing $COUNT JSON messages to $TOPIC on $BOOTSTRAP"

for i in $(seq 1 "$COUNT"); do
  echo "{"id":$i,"ts":"$(date -Is)","amount":$((RANDOM%1000))}" |     docker exec -i kafka /opt/bitnami/kafka/bin/kafka-console-producer.sh       --bootstrap-server "$BOOTSTRAP" --topic "$TOPIC" >/dev/null
done

echo "Done."
