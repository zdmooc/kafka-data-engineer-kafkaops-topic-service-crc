#!/usr/bin/env bash
set -euo pipefail

echo "[prereqs] Checking CRC and oc..."
command -v crc >/dev/null || { echo "crc not found"; exit 1; }
command -v oc >/dev/null || { echo "oc not found"; exit 1; }

crc status || true

echo "[prereqs] oc whoami:"
oc whoami

echo "[prereqs] oc version:"
oc version --client || true
oc version || true

echo "[prereqs] Checking cluster-admin (best effort):"
if oc auth can-i '*' '*' --all-namespaces | grep -qi yes; then
  echo "OK: cluster-admin-like permissions detected."
else
  echo "WARN: you may not have cluster-admin. Operator install may fail."
fi

echo "[prereqs] Done."
