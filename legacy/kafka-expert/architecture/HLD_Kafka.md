# High Level Design (HLD) - Plateforme Kafka

**Auteur:** Zidane Djamal (Architect HLD/DDL Kafka)
**Date:** Avril 2026
**Équipe:** Data Analytics

## 1. Introduction

Ce document d'Architecture de Haut Niveau (HLD) décrit la conception globale de la plateforme Apache Kafka mise en place pour l'équipe Data Analytics. Cette plateforme est conçue pour répondre aux besoins internes de l'entreprise en matière de streaming de données, de traitement en temps réel et d'intégration avec des solutions d'analyse comme OpenSearch et l'Elastic Stack.

## 2. Objectifs de l'Architecture

L'architecture Kafka vise à atteindre les objectifs suivants :
*   **Haute Disponibilité (HA) :** Tolérance aux pannes pour garantir un fonctionnement continu, même en cas de défaillance matérielle ou logicielle d'un ou plusieurs nœuds.
*   **Scalabilité Horizontale :** Capacité d'ajouter facilement de nouveaux nœuds (brokers) au cluster pour gérer une augmentation du volume de données ou du nombre de clients.
*   **Faible Latence :** Traitement des événements en temps réel ou quasi-temps réel pour des applications réactives.
*   **Durabilité des Données :** Conservation fiable des messages sur disque avec réplication pour éviter toute perte de données.
*   **Sécurité :** Chiffrement en transit (TLS), authentification (SASL/SCRAM ou mTLS) et autorisation (ACLs) pour protéger les flux de données sensibles.
*   **Observabilité :** Intégration complète avec des outils de monitoring (JMX, Prometheus, Grafana) pour surveiller la santé et les performances du cluster.

## 3. Composants de l'Architecture

### 3.1. Apache Kafka Cluster

Le cœur du système est le cluster Kafka, responsable de la réception, du stockage et de la distribution des messages.

*   **Brokers Kafka :** Nœuds de traitement qui reçoivent les messages des producteurs, les stockent sur disque et les servent aux consommateurs. Le cluster est composé de plusieurs brokers (ex: 3, 5 ou plus selon la charge) répartis sur différentes zones de disponibilité (AZ) pour la résilience.
*   **Gestion du Quorum (KRaft) :** Kafka utilise le protocole KRaft (Kafka Raft metadata mode) pour la gestion du quorum et des métadonnées, remplaçant ainsi ZooKeeper. Cela simplifie l'architecture et améliore la scalabilité. Les nœuds peuvent être configurés comme *brokers*, *controllers* (pour KRaft), ou les deux (*combined mode*). Dans un environnement de production, il est recommandé de séparer les rôles.

### 3.2. Producteurs (Producers)

Les producteurs sont les applications ou les systèmes qui génèrent des données et les envoient vers des *topics* spécifiques dans Kafka.
*   **Sources de Données :** Applications métiers, bases de données (via Change Data Capture - CDC), logs systèmes, capteurs IoT, etc.
*   **Intégration :** L'équipe Data Analytics développe des producteurs en Python et utilise des connecteurs (Kafka Connect) pour ingérer des données depuis diverses sources.

### 3.3. Consommateurs (Consumers)

Les consommateurs lisent les données à partir des *topics* Kafka pour les traiter, les analyser ou les stocker.
*   **Applications de Traitement :** Applications Python, services de traitement de flux (ex: Kafka Streams, Flink).
*   **Destinations :** L'architecture intègre fortement Kafka avec :
    *   **OpenSearch :** Pour la recherche et l'analyse de données.
    *   **Elastic Stack (Elasticsearch, Logstash) :** Pour l'indexation, la recherche et la visualisation des logs et des métriques. Logstash agit souvent comme un consommateur Kafka pour acheminer les données vers Elasticsearch.

### 3.4. Kafka Connect (Optionnel mais recommandé)

Kafka Connect est un framework pour connecter Kafka de manière scalable et fiable avec des systèmes externes (bases de données, systèmes de fichiers, etc.).
*   **Source Connectors :** Ingestion de données depuis des systèmes externes vers Kafka (ex: Debezium pour le CDC).
*   **Sink Connectors :** Exportation de données depuis Kafka vers des systèmes externes (ex: Elasticsearch Sink Connector).

### 3.5. Automatisation et Gestion

L'infrastructure est gérée selon le principe de l'Infrastructure as Code (IaC).
*   **Ansible :** Utilisé pour l'approvisionnement, la configuration et le déploiement automatisé des clusters Kafka et des composants associés (Elastic Stack).
*   **Git/Bitbucket :** Dépôt central pour stocker les playbooks Ansible, les configurations Kafka et le code source Python.

## 4. Flux de Données (Data Flow)

1.  **Ingestion :** Les producteurs (applications, Beats, Logstash) publient des messages vers les brokers Kafka sur des topics spécifiques.
2.  **Stockage et Réplication :** Les brokers Kafka reçoivent les messages, les écrivent sur disque (commit log) et les répliquent vers d'autres brokers selon le facteur de réplication configuré (ex: `replication.factor=3`).
3.  **Consommation :** Les consommateurs (applications Python, Logstash, OpenSearch Sink Connectors) lisent les messages à partir des partitions des topics. Les groupes de consommateurs (Consumer Groups) permettent de répartir la charge de lecture.
4.  **Traitement et Indexation :** Les données consommées sont traitées et envoyées vers OpenSearch ou Elasticsearch pour indexation, recherche et visualisation via Kibana.

## 5. Déploiement Physique (Physical Deployment)

Le déploiement typique implique une répartition sur plusieurs machines virtuelles (VMs) ou conteneurs.

*   **Cluster Kafka (KRaft) :**
    *   3 Nœuds Controllers dédiés (pour le quorum KRaft).
    *   N (ex: 3 à 5) Nœuds Brokers dédiés.
*   **Elastic Stack / OpenSearch :**
    *   Cluster Elasticsearch/OpenSearch (Nœuds Master, Data, Ingest).
    *   Instances Logstash.
    *   Instance Kibana/OpenSearch Dashboards.

*Note : Les détails spécifiques de dimensionnement (CPU, RAM, Disque) seront définis dans le document DDL (Detailed Design).*
