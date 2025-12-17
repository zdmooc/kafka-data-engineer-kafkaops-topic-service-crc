#!/usr/bin/env bash
set -euo pipefail
BOOTSTRAP="${1:-localhost:9092}"
TOPIC="${2:-demo.orders.v1}"

docker exec -it kafka /opt/bitnami/kafka/bin/kafka-topics.sh   --bootstrap-server "$BOOTSTRAP" --describe --topic "$TOPIC"
