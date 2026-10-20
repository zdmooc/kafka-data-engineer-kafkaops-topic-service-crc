#!/bin/bash
# =============================================================================
# Script: kafka_healthcheck.sh
# Description: Vérifie la santé du cluster Kafka (KRaft mode)
# Auteur: Zidane Djamal - Équipe Data Analytics
# Usage: ./kafka_healthcheck.sh [BOOTSTRAP_SERVER]
# =============================================================================

set -euo pipefail

KAFKA_HOME="${KAFKA_HOME:-/opt/kafka}"
BOOTSTRAP_SERVER="${1:-localhost:9092}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo " Kafka Cluster Healthcheck"
echo " Bootstrap: ${BOOTSTRAP_SERVER}"
echo " Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"
echo ""

# 1. Check Broker Connectivity
echo -e "${YELLOW}[1/5] Checking Broker Connectivity...${NC}"
if ${KAFKA_HOME}/bin/kafka-broker-api-versions.sh --bootstrap-server ${BOOTSTRAP_SERVER} > /dev/null 2>&1; then
    echo -e "${GREEN}  [OK] Broker is reachable at ${BOOTSTRAP_SERVER}${NC}"
else
    echo -e "${RED}  [FAIL] Cannot connect to broker at ${BOOTSTRAP_SERVER}${NC}"
    exit 1
fi
echo ""

# 2. Check KRaft Quorum Status
echo -e "${YELLOW}[2/5] Checking KRaft Quorum Status...${NC}"
QUORUM_STATUS=$(${KAFKA_HOME}/bin/kafka-metadata-quorum.sh --bootstrap-server ${BOOTSTRAP_SERVER} describe --status 2>&1 || true)
if echo "${QUORUM_STATUS}" | grep -q "LeaderId"; then
    echo -e "${GREEN}  [OK] KRaft quorum is healthy${NC}"
    echo "${QUORUM_STATUS}" | head -5
else
    echo -e "${RED}  [WARN] Could not retrieve KRaft quorum status${NC}"
fi
echo ""

# 3. Check Under-Replicated Partitions (URP)
echo -e "${YELLOW}[3/5] Checking Under-Replicated Partitions (URP)...${NC}"
URP=$(${KAFKA_HOME}/bin/kafka-topics.sh --bootstrap-server ${BOOTSTRAP_SERVER} --describe --under-replicated-partitions 2>&1 || true)
if [ -z "${URP}" ]; then
    echo -e "${GREEN}  [OK] No under-replicated partitions found${NC}"
else
    echo -e "${RED}  [ALERT] Under-replicated partitions detected:${NC}"
    echo "${URP}"
fi
echo ""

# 4. Check Offline Partitions
echo -e "${YELLOW}[4/5] Checking Offline Partitions...${NC}"
OFFLINE=$(${KAFKA_HOME}/bin/kafka-topics.sh --bootstrap-server ${BOOTSTRAP_SERVER} --describe --unavailable-partitions 2>&1 || true)
if [ -z "${OFFLINE}" ]; then
    echo -e "${GREEN}  [OK] No offline partitions found${NC}"
else
    echo -e "${RED}  [CRITICAL] Offline partitions detected:${NC}"
    echo "${OFFLINE}"
fi
echo ""

# 5. List Consumer Groups and their Lag
echo -e "${YELLOW}[5/5] Checking Consumer Group Lag...${NC}"
GROUPS=$(${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${BOOTSTRAP_SERVER} --list 2>&1 || true)
if [ -n "${GROUPS}" ]; then
    for GROUP in ${GROUPS}; do
        echo "  Group: ${GROUP}"
        ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${BOOTSTRAP_SERVER} --describe --group ${GROUP} 2>&1 | head -5 || true
        echo ""
    done
else
    echo "  No consumer groups found."
fi

echo "========================================"
echo " Healthcheck Complete"
echo "========================================"
