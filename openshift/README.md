# OpenShift deployment (CRC)

This folder provides a local OpenShift (CRC) deployment path:
- Kafka via Strimzi operator (Apache Kafka on Kubernetes/OpenShift)
- Topic-as-a-Service API
- Kafka UI (optional)

> Notes:
> - Operator install requires cluster-admin.
> - CRC is a single-node environment; deployments are minimal and non-HA.

## Folder map
- `crc/` : scripts (idempotent-ish) to install operator and deploy stack
- `manifests/` : YAML resources used by scripts
- `gitops/` : (optional) Argo CD Application skeletons
