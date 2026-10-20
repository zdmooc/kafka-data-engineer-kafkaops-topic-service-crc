# Detailed Design (DDL) - Plateforme Kafka

**Auteur:** Zidane Djamal (Architect HLD/DDL Kafka)
**Date:** Avril 2026
**Équipe:** Data Analytics

## 1. Introduction

Ce document de Conception Détaillée (DDL) fait suite au document d'Architecture de Haut Niveau (HLD). Il décrit les configurations techniques spécifiques, le dimensionnement matériel, les paramètres de sécurité et les choix d'implémentation pour la plateforme Apache Kafka et son intégration avec l'Elastic Stack/OpenSearch.

## 2. Dimensionnement et Déploiement (Sizing & Deployment)

Le dimensionnement de l'infrastructure est basé sur les exigences de l'équipe Data Analytics en matière de débit, de rétention et de haute disponibilité.

### 2.1. Spécifications Matérielles (Hardware Specifications)

Pour un cluster de production typique gérant un volume moyen à élevé :

| Composant | Rôle | CPU (Cores) | RAM (GB) | Stockage (Disque) | Type de Disque | Quantité (Nœuds) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kafka Controller** | Quorum KRaft | 4 | 8 | 50 GB | SSD (OS) | 3 |
| **Kafka Broker** | Stockage/Traitement | 8-16 | 32-64 | 2 TB - 5 TB | SSD/NVMe (Data) | 3 à 5 (Extensible) |
| **Logstash** | Ingestion/Transformation | 4-8 | 16-32 | 100 GB | SSD (OS/Queue) | 2+ (Scale out) |
| **Elasticsearch Data** | Indexation/Recherche | 16+ | 64 | 2 TB+ | SSD/NVMe | 3+ |

*Note: La RAM allouée à la JVM de Kafka ne doit pas dépasser 6 GB. Le reste de la RAM est utilisé par l'OS pour le cache disque (Page Cache), ce qui est crucial pour les performances de Kafka.*

### 2.2. Configuration Réseau (Network Configuration)

*   **Bande Passante :** 10 Gbps minimum recommandé entre les brokers Kafka pour la réplication.
*   **Ports Ouverts :**
    *   `9092` : Port client Kafka (PLAINTEXT - déconseillé en prod).
    *   `9093` : Port client Kafka sécurisé (SASL_SSL ou mTLS).
    *   `9094` : Port de réplication inter-broker.
    *   `9095` : Port de communication KRaft (Controllers).
    *   `9999` : Port JMX pour le monitoring (Prometheus JMX Exporter).

## 3. Configuration Kafka (server.properties)

Les paramètres suivants sont critiques pour la stabilité et les performances du cluster.

### 3.1. Paramètres de Base et KRaft

```properties
# Rôles du nœud (ex: broker, controller, ou les deux)
process.roles=broker
# ID unique du nœud (ex: 1, 2, 3...)
node.id=1
# Quorum KRaft (liste des controllers)
controller.quorum.voters=1@controller1:9095,2@controller2:9095,3@controller3:9095
# Écouteurs pour les clients et la réplication
listeners=PLAINTEXT://broker1:9092,SSL://broker1:9093
advertised.listeners=PLAINTEXT://broker1.example.com:9092,SSL://broker1.example.com:9093
```

### 3.2. Réplication et Durabilité

```properties
# Facteur de réplication par défaut pour les nouveaux topics
default.replication.factor=3
# Nombre minimum de réplicas synchronisés (In-Sync Replicas - ISR)
min.insync.replicas=2
# Configuration des logs
log.dirs=/var/lib/kafka/data
# Rétention par défaut (ex: 7 jours)
log.retention.hours=168
# Taille maximale d'un segment de log (ex: 1 GB)
log.segment.bytes=1073741824
```

### 3.3. Optimisation des Performances

```properties
# Nombre de threads réseau pour la réception des requêtes
num.network.threads=8
# Nombre de threads d'E/S pour le traitement des requêtes (disque)
num.io.threads=16
# Taille du buffer de réception des sockets
socket.receive.buffer.bytes=102400
# Taille du buffer d'envoi des sockets
socket.send.buffer.bytes=102400
# Taille maximale d'une requête (ex: 10 MB)
message.max.bytes=10485760
```

## 4. Sécurité (Security)

La sécurité est primordiale pour protéger les données sensibles gérées par l'équipe Data Analytics.

### 4.1. Chiffrement (Encryption)

*   **TLS/SSL :** Toutes les communications inter-brokers, entre les clients et les brokers, et entre Kafka et KRaft doivent être chiffrées en utilisant TLS 1.2 ou supérieur.
*   **Certificats :** Utilisation d'une PKI interne ou d'une autorité de certification (CA) reconnue pour générer et gérer les certificats des nœuds Kafka.

### 4.2. Authentification (Authentication)

*   **SASL/SCRAM :** Recommandé pour l'authentification des clients (producteurs/consommateurs). Les identifiants sont stockés de manière sécurisée dans Kafka (SCRAM-SHA-256 ou SCRAM-SHA-512).
*   **mTLS (Mutual TLS) :** Alternative robuste pour l'authentification inter-services, où le client et le serveur vérifient mutuellement leurs certificats.

### 4.3. Autorisation (Authorization)

*   **ACLs (Access Control Lists) :** Kafka fournit un mécanisme d'ACLs natif pour contrôler l'accès aux ressources (Topics, Consumer Groups, Cluster).
*   **Règles :** Principe du moindre privilège. Un producteur ne doit avoir le droit d'écrire (`Write`) que sur les topics qui le concernent. Un consommateur ne doit avoir le droit de lire (`Read`) que sur les topics autorisés.

## 5. Intégration Elastic Stack / OpenSearch

L'architecture s'appuie fortement sur l'Elastic Stack pour le traitement et l'analyse des données issues de Kafka.

### 5.1. Logstash comme Consommateur Kafka

Logstash est configuré avec l'`input` Kafka pour consommer les messages, appliquer des filtres (Grok, Mutate, Date) et les envoyer vers Elasticsearch/OpenSearch via l'`output` correspondant.

**Exemple de configuration Logstash (`logstash.conf`) :**

```logstash
input {
  kafka {
    bootstrap_servers => "broker1.example.com:9093,broker2.example.com:9093"
    topics => ["app-logs", "system-metrics"]
    group_id => "logstash-indexer-group"
    security_protocol => "SSL"
    ssl_truststore_location => "/etc/logstash/kafka.truststore.jks"
    ssl_truststore_password => "password"
    codec => "json"
  }
}

filter {
  # Logique de parsing et d'enrichissement
  if [type] == "nginx_access" {
    grok { ... }
  }
}

output {
  elasticsearch {
    hosts => ["https://es1.example.com:9200", "https://es2.example.com:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
    user => "logstash_internal"
    password => "secure_password"
    ssl_certificate_verification => true
    cacert => "/etc/logstash/es-ca.crt"
  }
}
```

### 5.2. Beats (Filebeat, Metricbeat) comme Producteurs

Les agents Beats collectent les logs et métriques directement sur les serveurs et les envoient vers Kafka (agissant comme un buffer) plutôt que directement vers Logstash ou Elasticsearch, améliorant ainsi la résilience.

**Exemple de configuration Filebeat (`filebeat.yml`) :**

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/nginx/access.log

output.kafka:
  hosts: ["broker1.example.com:9093", "broker2.example.com:9093"]
  topic: 'app-logs'
  partition.round_robin:
    reachable_only: false
  required_acks: 1
  compression: gzip
  max_message_bytes: 1000000
  ssl.certificate_authorities: ["/etc/filebeat/kafka-ca.crt"]
```

## 6. Observabilité et Monitoring

*   **JMX Exporter :** Déployé sur chaque nœud Kafka pour exposer les métriques JMX au format Prometheus.
*   **Prometheus :** Collecte les métriques exposées par JMX Exporter, Node Exporter (métriques OS), et les métriques des clients Kafka.
*   **Grafana :** Tableaux de bord pour visualiser la santé du cluster (Under Replicated Partitions, Offline Partitions, Network Bytes In/Out, Request Latency, etc.).
*   **Alerting :** Alertmanager configuré pour envoyer des notifications (Slack, Email) en cas d'anomalies critiques (ex: `OfflinePartitions > 0`).
