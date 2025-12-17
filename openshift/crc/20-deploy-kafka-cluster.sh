#!/usr/bin/env bash
set -euo pipefail

KAFKA_NS="${KAFKA_NS:-kafka-platform}"
CLUSTER_NAME="${CLUSTER_NAME:-demo}"

echo "[kafka] Creating namespace: $KAFKA_NS"
oc get ns "$KAFKA_NS" >/dev/null 2>&1 || oc new-project "$KAFKA_NS" >/dev/null

echo "[kafka] Applying Kafka cluster (Strimzi CR)"
oc -n "$KAFKA_NS" apply -f ../manifests/kafka/kafka-cluster.yaml   --dry-run=client -o yaml |   sed "s/{{CLUSTER_NAME}}/$CLUSTER_NAME/g" |   oc -n "$KAFKA_NS" apply -f -

echo "[kafka] Waiting for Kafka to be Ready (best effort)..."
oc -n "$KAFKA_NS" wait kafka "$CLUSTER_NAME" --for=condition=Ready=True --timeout=600s || true

echo "[kafka] Services:"
oc -n "$KAFKA_NS" get svc | grep -E "$CLUSTER_NAME|NAME" || true

echo "[kafka] Pods:"
oc -n "$KAFKA_NS" get pods -o wide || true

echo "[kafka] Done."
