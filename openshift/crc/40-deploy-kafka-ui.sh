#!/usr/bin/env bash
set -euo pipefail

APP_NS="${APP_NS:-kafka-platform}"
CLUSTER_NAME="${CLUSTER_NAME:-demo}"

echo "[kafka-ui] Namespace: $APP_NS"
oc get ns "$APP_NS" >/dev/null 2>&1 || oc new-project "$APP_NS" >/dev/null

oc -n "$APP_NS" apply -f ../manifests/kafka-ui/deployment.yaml   --dry-run=client -o yaml |   sed "s/{{CLUSTER_NAME}}/$CLUSTER_NAME/g" |   oc -n "$APP_NS" apply -f -

oc -n "$APP_NS" apply -f ../manifests/kafka-ui/service.yaml
oc -n "$APP_NS" apply -f ../manifests/kafka-ui/route.yaml

echo "[kafka-ui] Pods:"
oc -n "$APP_NS" get pods -l app=kafka-ui -o wide || true
