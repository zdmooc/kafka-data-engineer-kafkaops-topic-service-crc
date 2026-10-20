# Elastic Stack - Intégration Kafka

**Auteur :** Zidane Djamal

Ce répertoire contient les configurations de l'Elastic Stack (Logstash, Filebeat) pour l'intégration avec le cluster Kafka.

## Structure

```
elastic_stack/
├── logstash/
│   └── kafka-to-opensearch.conf   # Pipeline Logstash : Kafka → OpenSearch/Elasticsearch
└── filebeat/
    └── filebeat.yml               # Configuration Filebeat : Logs → Kafka
```

## Flux de Données

```
[Serveurs] → Filebeat → Kafka → Logstash → OpenSearch/Elasticsearch → Kibana
```

Filebeat collecte les logs sur les serveurs et les envoie vers Kafka (buffer). Logstash consomme les messages depuis Kafka, applique des filtres de transformation, et indexe les données dans OpenSearch ou Elasticsearch pour la visualisation dans Kibana.
