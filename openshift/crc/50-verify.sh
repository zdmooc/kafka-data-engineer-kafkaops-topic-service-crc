#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-kafka-platform}"
APP_NAME="${APP_NAME:-topic-as-a-service}"
CLUSTER_NAME="${CLUSTER_NAME:-demo}"

echo "[verify] Resources in $NS"
oc -n "$NS" get pods -o wide
oc -n "$NS" get svc
oc -n "$NS" get route

HOST=$(oc -n "$NS" get route "$APP_NAME" -o jsonpath='{.spec.host}' 2>/dev/null || true)
if [[ -n "$HOST" ]]; then
  echo "[verify] Topic service route: https://$HOST"
  echo "[verify] Health:"
  curl -sk "https://$HOST/health" | head -c 500; echo
  echo "[verify] OpenAPI: https://$HOST/docs"
else
  echo "[verify] WARN: route not found for $APP_NAME"
fi

KUI=$(oc -n "$NS" get route kafka-ui -o jsonpath='{.spec.host}' 2>/dev/null || true)
if [[ -n "$KUI" ]]; then
  echo "[verify] Kafka UI: https://$KUI"
fi

echo "[verify] Done."
