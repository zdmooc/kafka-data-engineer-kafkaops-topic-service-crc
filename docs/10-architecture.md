# Reference architecture

## Logical view

```mermaid
flowchart LR
  subgraph Clients[Internal users / apps]
    Dev[Developers]
    DataTeam[Data Analytics]
    Ops[Support / MCO]
  end

  Dev -->|REST| TaaS[Topic as a Service API]
  Ops -->|Ansible / CLI| TaaS

  TaaS -->|Admin API| Kafka[(Kafka Cluster)]
  Kafka -->|Logs| Obs[Observability]
  TaaS -->|Audit logs| Obs

  subgraph Obs[Observability]
    ES[Elastic Stack]
    OS[OpenSearch]
    Dash[Kibana / Dashboards]
  end

  Obs --> Dash
```

## Key components

- **Kafka Cluster**: high-volume messaging backbone (multi-broker, multi-AZ in prod)
- **Topic-as-a-Service**: standardizes topic creation, naming, retention, configs, ownership
- **KafkaOps CLI**: standardized operational commands (health, topic drift, lag)
- **Ansible automation**: idempotent playbooks for checks, evidence, topic catalog
- **Observability**: logs + metrics + dashboards for proactive operations

## Non-functional targets

- Reliability (SLO, runbooks, incident response)
- Performance (capacity planning, partitions strategy, IO/network tuning)
- Security (TLS/SASL, ACLs, audit)
- Operability (automated checks, reproducible changes, evidence)
