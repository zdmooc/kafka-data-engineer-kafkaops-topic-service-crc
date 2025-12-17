#!/usr/bin/env bash
set -euo pipefail

# Strimzi operator install via OperatorHub objects (OpenShift way).
# Adjust channel/version according to your cluster OperatorHub catalog.

NS="${NS:-strimzi}"
CHANNEL="${CHANNEL:-stable}"
SOURCE="${SOURCE:-redhat-operators}"        # or "community-operators" depending on CRC catalog
SOURCE_NS="${SOURCE_NS:-openshift-marketplace}"

echo "[strimzi] Creating namespace: $NS"
oc get ns "$NS" >/dev/null 2>&1 || oc new-project "$NS" >/dev/null

echo "[strimzi] Applying OperatorGroup + Subscription (channel=$CHANNEL source=$SOURCE)"
oc -n "$NS" apply -f ../manifests/strimzi/operatorgroup.yaml
oc -n "$NS" apply -f ../manifests/strimzi/subscription.yaml   --dry-run=client -o yaml |   sed "s/{{CHANNEL}}/$CHANNEL/g; s/{{SOURCE}}/$SOURCE/g; s/{{SOURCE_NS}}/$SOURCE_NS/g" |   oc -n "$NS" apply -f -

echo "[strimzi] Waiting for CSV to succeed..."
# Wait for the operator to be installed (best effort; list CSVs)
for i in {1..60}; do
  csv=$(oc -n "$NS" get csv -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)
  phase=$(oc -n "$NS" get csv "$csv" -o jsonpath='{.status.phase}' 2>/dev/null || true)
  if [[ -n "${csv}" && "${phase}" == "Succeeded" ]]; then
    echo "OK: CSV ${csv} is Succeeded"
    break
  fi
  echo "Waiting... (csv=${csv:-none} phase=${phase:-n/a})"
  sleep 5
done

echo "[strimzi] Operator pods:"
oc -n "$NS" get pods -o wide || true

echo "[strimzi] Done."
