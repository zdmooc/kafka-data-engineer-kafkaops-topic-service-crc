#!/usr/bin/env bash
set -euo pipefail

APP_NS="${APP_NS:-kafka-platform}"
APP_NAME="${APP_NAME:-topic-as-a-service}"
IMAGE_TAG="${IMAGE_TAG:-0.1.0}"
CLUSTER_NAME="${CLUSTER_NAME:-demo}"

echo "[app] Namespace: $APP_NS"
oc get ns "$APP_NS" >/dev/null 2>&1 || oc new-project "$APP_NS" >/dev/null

echo "[app] Create/Update Secret + ConfigMap"
oc -n "$APP_NS" apply -f ../manifests/topic-service/secret.yaml
oc -n "$APP_NS" apply -f ../manifests/topic-service/configmap.yaml   --dry-run=client -o yaml |   sed "s/{{CLUSTER_NAME}}/$CLUSTER_NAME/g" |   oc -n "$APP_NS" apply -f -

echo "[app] Build image with OpenShift BuildConfig (Docker strategy)"
# BuildConfig + ImageStream + Build
oc -n "$APP_NS" apply -f ../manifests/topic-service/buildconfig.yaml   --dry-run=client -o yaml |   sed "s/{{APP_NAME}}/$APP_NAME/g; s/{{IMAGE_TAG}}/$IMAGE_TAG/g" |   oc -n "$APP_NS" apply -f -

echo "[app] Start build (if none running)"
oc -n "$APP_NS" start-build "$APP_NAME" --from-dir ../../services/topic-as-a-service --follow || true

echo "[app] Deploy app (Deployment/Service/Route)"
oc -n "$APP_NS" apply -f ../manifests/topic-service/deployment.yaml   --dry-run=client -o yaml |   sed "s/{{APP_NAME}}/$APP_NAME/g; s/{{IMAGE_TAG}}/$IMAGE_TAG/g" |   oc -n "$APP_NS" apply -f -

oc -n "$APP_NS" apply -f ../manifests/topic-service/service.yaml   --dry-run=client -o yaml | sed "s/{{APP_NAME}}/$APP_NAME/g" | oc -n "$APP_NS" apply -f -

oc -n "$APP_NS" apply -f ../manifests/topic-service/route.yaml   --dry-run=client -o yaml | sed "s/{{APP_NAME}}/$APP_NAME/g" | oc -n "$APP_NS" apply -f -

echo "[app] Pods:"
oc -n "$APP_NS" get pods -l app="$APP_NAME" -o wide || true

echo "[app] Done."
