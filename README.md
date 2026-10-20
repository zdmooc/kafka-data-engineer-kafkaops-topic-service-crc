# KafkaOps + Topic-as-a-Service (portfolio / mission simulator)

Repository designed as a **full delivery** aligned with a Data Engineer (Kafka) support mission (target: **OpenShift Local / CRC** for local lab):
- Kafka expertise (design, config, performance, troubleshooting)
- MCO/support automation (Ansible + CLI tooling)
- Internal dev: **Topic as a Service** (REST API)
- Observability: **OpenSearch** and **Elastic Stack** reference setups
- Documentation / runbooks / best practices (FR/EN)

> Status: project skeleton **ready to run locally** with Docker Compose (Kafka + UI + Topic service).
> Date: 2025-12-17

---

## Quickstart (local)

### Prereqs
- Docker + Docker Compose
- (Optional) Python 3.11+ for local dev
- (Optional) Ansible for automation demos

### Start local stack
```bash
make up
```

### Access
- Kafka UI: http://localhost:8080
- Topic-as-a-Service (API): http://localhost:8088
- OpenAPI: http://localhost:8088/docs

### Create a topic (via API)
```bash
curl -s -X POST http://localhost:8088/v1/topics \
  -H "Content-Type: application/json" \
  -d '{
    "name": "demo.orders.v1",
    "partitions": 3,
    "replication_factor": 1,
    "configs": {
      "retention.ms": "86400000",
      "cleanup.policy": "delete"
    },
    "labels": {
      "owner": "data-analytics",
      "env": "local"
    },
    "description": "Demo topic"
  }' | jq .
```

### Apply a declarative topic catalog (CLI)
```bash
docker compose -f infra/docker-compose/compose.yaml exec topic-service \
  kafkaops topics apply -f /catalog/topics/local.yaml
```

### Stop
```bash
make down
```
## Quickstart (OpenShift Local / CRC)

This repo includes an OpenShift-first local path (CRC), in addition to Docker Compose.

### Prereqs
- OpenShift Local (CRC) installed and running
- `oc` CLI logged in (cluster-admin recommended for operator install)
- Optional: `podman` (or Docker) for local builds

### Deploy on CRC (end-to-end)
```bash
cd openshift/crc
./00-prereqs.sh
./10-install-strimzi-operator.sh
./20-deploy-kafka-cluster.sh
./30-deploy-topic-service.sh
./40-deploy-kafka-ui.sh
./50-verify.sh
```

Artifacts:
- OpenShift manifests: `openshift/manifests/`
- Operational scripts: `openshift/crc/*.sh`



---

## Repository map

- `services/topic-as-a-service/` : FastAPI service + Kafka Admin (Topic as a Service)
- `tools/kafkaops_cli/` : CLI used by ops & automation (health/topics/configs/lag)
- `ansible/` : playbooks + roles (healthcheck, evidence, topic catalog)
- `infra/docker-compose/` : local platform (Kafka, Kafka UI, Topic service)
- `observability/` : example configs (JMX exporter, Logstash pipelines)
- `runbooks/` : incident runbooks (ISR, URP, disk, latency, lag…)
- `docs/` : architecture, security, performance, governance, collaboration (FR/EN)

---

## How this maps to the mission

### Kafka expertise
- Health + metadata checks: `kafkaops health`
- Topic management: API + declarative catalog
- Troubleshooting runbooks: `runbooks/`
- Performance & capacity notes: `docs/40-performance-tuning.md`

### Automation / MCO
- Ansible playbooks for repeatable ops and evidence capture: `ansible/`
- CLI tooling to standardize commands across environments: `tools/kafkaops_cli/`

### Topic as a Service
- REST API (FastAPI), audit, governance rules: `docs/50-topic-as-a-service.md`

### Observability
- Elastic/OpenSearch reference, pipelines and dashboards pointers: `docs/60-observability.md`

---

## Next steps (future-proof)
- Add multi-cluster / multi-region inventory patterns in Ansible
- Package Topic-as-a-Service as Helm chart + GitOps (Argo CD)
- Add SLO-based alerting (Prometheus + Alertmanager) for Kafka KPIs


## Historical Kafka Expert archive — 20/10/2026

The archived [Kafka Expert](legacy/kafka-expert/README.md) is now **fully preserved** under `legacy/kafka-expert/`: **30/30 source files byte-for-byte identical**, including the original [293873-byte HLD PNG](legacy/kafka-expert/architecture/hld_diagram.png), with original Git SHA and executable modes retained. [GitHub Actions validation](https://github.com/zdmooc/kafka-data-engineer-kafkaops-topic-service-crc/actions/runs/39484111012) succeeded; [PR #2](https://github.com/zdmooc/kafka-data-engineer-kafkaops-topic-service-crc/pull/2) merged and the `main` tree passed 30/30 SHA comparisons. See [manifest](legacy/kafka-expert-source-map.json) and [proof report](legacy/KAFKA_EXPERT_2026-10-20.md). The historical source was **deleted manually by its owner on 20 October 2026** (GitHub 404 confirmed, portfolio at 73 repositories). **All 30 files remain byte-identical on `main`**, though its standalone Git history was not transferred. No Kafka runtime proof is claimed.
