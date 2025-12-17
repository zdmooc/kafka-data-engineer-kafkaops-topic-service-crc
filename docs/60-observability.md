# Observability (Elastic Stack / OpenSearch)

## Kafka signals to monitor
- Under-replicated partitions (URP)
- ISR changes / leader elections
- Request latency / error rates
- Broker disk usage + log dir health
- Controller activity
- Consumer lag (critical groups)
- JVM (GC, heap, threads)

## This repo provides
- Example JMX exporter config: `observability/jmx/kafka-jmx-exporter.yml`
- Example Logstash pipelines:
  - Kafka -> OpenSearch: `observability/logstash/pipeline-kafka-to-opensearch.conf`
  - Kafka -> Elasticsearch: `observability/logstash/pipeline-kafka-to-elastic.conf`

## Recommended approach (future-proof)
- Metrics: Prometheus + Grafana dashboards for Kafka/JVM
- Logs: structured JSON logs -> OpenSearch/Elastic
- Traces: optional (if producers/consumers instrumented)
- Alerting: SLO-based thresholds, not noisy raw metrics
