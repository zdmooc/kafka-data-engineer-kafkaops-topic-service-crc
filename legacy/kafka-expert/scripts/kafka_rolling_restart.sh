#!/bin/bash
# =============================================================================
# Script: kafka_rolling_restart.sh
# Description: Effectue un rolling restart sécurisé du cluster Kafka
# Auteur: Zidane Djamal - Équipe Data Analytics
# Usage: ./kafka_rolling_restart.sh <broker_list_file>
#   broker_list_file: fichier contenant un hostname de broker par ligne
# =============================================================================

set -euo pipefail

KAFKA_HOME="${KAFKA_HOME:-/opt/kafka}"
BOOTSTRAP_SERVER="${BOOTSTRAP_SERVER:-localhost:9092}"
WAIT_SECONDS=60
MAX_RETRIES=30

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <broker_list_file>"
    echo "  broker_list_file: file containing one broker hostname per line"
    exit 1
fi

BROKER_LIST_FILE="$1"

if [ ! -f "${BROKER_LIST_FILE}" ]; then
    echo "Error: File '${BROKER_LIST_FILE}' not found."
    exit 1
fi

wait_for_isr() {
    echo "  Waiting for all partitions to be in-sync (ISR)..."
    local retries=0
    while [ ${retries} -lt ${MAX_RETRIES} ]; do
        URP=$(${KAFKA_HOME}/bin/kafka-topics.sh --bootstrap-server ${BOOTSTRAP_SERVER} --describe --under-replicated-partitions 2>&1 || true)
        if [ -z "${URP}" ]; then
            echo "  All partitions are in-sync."
            return 0
        fi
        retries=$((retries + 1))
        echo "  Under-replicated partitions still exist. Retry ${retries}/${MAX_RETRIES}. Waiting ${WAIT_SECONDS}s..."
        sleep ${WAIT_SECONDS}
    done
    echo "  WARNING: Timed out waiting for ISR. Proceeding with caution."
    return 1
}

echo "========================================"
echo " Kafka Rolling Restart"
echo " Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"

while IFS= read -r BROKER_HOST; do
    # Skip empty lines and comments
    [[ -z "${BROKER_HOST}" || "${BROKER_HOST}" == \#* ]] && continue

    echo ""
    echo "--- Processing broker: ${BROKER_HOST} ---"

    # Step 1: Verify no URP before restart
    echo "  [Step 1] Checking cluster health before restart..."
    wait_for_isr

    # Step 2: Stop Kafka on the target broker
    echo "  [Step 2] Stopping Kafka on ${BROKER_HOST}..."
    ssh "${BROKER_HOST}" "sudo systemctl stop kafka"
    echo "  Kafka stopped on ${BROKER_HOST}."

    # Step 3: Wait a moment
    echo "  [Step 3] Waiting 10 seconds before restart..."
    sleep 10

    # Step 4: Start Kafka on the target broker
    echo "  [Step 4] Starting Kafka on ${BROKER_HOST}..."
    ssh "${BROKER_HOST}" "sudo systemctl start kafka"
    echo "  Kafka started on ${BROKER_HOST}."

    # Step 5: Wait for ISR to recover
    echo "  [Step 5] Waiting for ISR recovery after restart..."
    sleep 30  # Initial wait for broker to join
    wait_for_isr

    echo "--- Broker ${BROKER_HOST} restarted successfully ---"

done < "${BROKER_LIST_FILE}"

echo ""
echo "========================================"
echo " Rolling Restart Complete"
echo "========================================"
