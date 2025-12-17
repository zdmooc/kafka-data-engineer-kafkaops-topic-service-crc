#!/usr/bin/env bash
set -euo pipefail
BOOTSTRAP="${1:-localhost:9092}"

docker exec -it kafka /opt/bitnami/kafka/bin/kafka-broker-api-versions.sh   --bootstrap-server "$BOOTSTRAP"
