# Runbook : Maintien en Conditions Opérationnelles (MCO) Kafka

**Équipe :** Data Analytics
**Auteur :** Zidane Djamal (Architect HLD/DDL Kafka)
**Date de mise à jour :** Avril 2026

## 1. Introduction

Ce document est le guide de référence pour l'équipe support en charge du Maintien en Conditions Opérationnelles (MCO) de la plateforme Kafka. Il détaille les procédures courantes, les commandes de diagnostic et les actions de remédiation pour assurer la stabilité, la performance et la disponibilité du service.

## 2. Rôles et Responsabilités

L'équipe Data Analytics est responsable du support de niveau 2 et 3 pour l'infrastructure Kafka, OpenSearch et la stack Elastic.

*   **Niveau 1 (Monitoring/NOC) :** Surveillance des alertes Grafana/Prometheus, création de tickets d'incidents, escalade si nécessaire.
*   **Niveau 2 (Support MCO) :** Diagnostic initial, exécution des procédures de ce runbook, redémarrage de services, résolution d'incidents connus.
*   **Niveau 3 (Expertise Kafka) :** Analyse approfondie, optimisation des performances, modification d'architecture, résolution de bugs complexes, développement d'outils d'automatisation (Ansible, Python).

## 3. Outils de Diagnostic

L'équipe support dispose des outils suivants pour analyser l'état du cluster :

1.  **Scripts Kafka (CLI) :** Fournis avec l'installation de Kafka (`/opt/kafka/bin/`).
2.  **Grafana Dashboards :** Visualisation des métriques clés (Prometheus JMX Exporter).
3.  **Kibana / OpenSearch Dashboards :** Analyse des logs applicatifs et systèmes (ingérés via Filebeat/Logstash).
4.  **Ansible :** Pour l'exécution de commandes sur l'ensemble du cluster.

## 4. Procédures Courantes (Day-2 Operations)

### 4.1. Vérification de la Santé du Cluster (Healthcheck)

#### 4.1.1. Vérifier l'état des Brokers (KRaft Mode)

Dans un cluster KRaft, la commande `kafka-metadata-quorum.sh` permet de vérifier l'état du quorum des contrôleurs.

```bash
/opt/kafka/bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status
```
*Attendu : Le statut doit indiquer que le quorum est actif et qu'un leader est élu.*

#### 4.1.2. Vérifier les Partitions Sous-Répliquées (Under-Replicated Partitions - URP)

C'est l'indicateur principal de la santé d'un cluster Kafka. Un URP > 0 indique qu'un ou plusieurs brokers sont lents ou inaccessibles.

```bash
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions
```
*Attendu : La commande ne doit rien retourner (aucun topic sous-répliqué).*

#### 4.1.3. Vérifier l'état des Consumer Groups (Lag)

Le "lag" représente le retard d'un consommateur par rapport à la production de messages. Un lag croissant indique un problème de performance du consommateur.

```bash
# Lister les groupes
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Décrire un groupe spécifique (ex: logstash-indexer)
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group logstash-indexer
```
*Action : Surveiller la colonne `LAG`. Si elle augmente continuellement, il faut investiguer du côté de l'application consommatrice (ex: ajouter des instances Logstash).*

### 4.2. Gestion des Topics

L'équipe support peut être amenée à gérer les topics en dehors du processus automatisé "Topic As A Service" en cas d'urgence.

#### 4.2.1. Créer un Topic (Manuel)

```bash
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-urgent-topic --partitions 3 --replication-factor 3
```

#### 4.2.2. Modifier la Rétention d'un Topic

```bash
# Exemple : Passer la rétention à 1 jour (86400000 ms)
/opt/kafka/bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name my-topic --alter --add-config retention.ms=86400000
```

#### 4.2.3. Augmenter le Nombre de Partitions

*Attention : On ne peut qu'augmenter le nombre de partitions, jamais le diminuer.*

```bash
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic my-topic --partitions 6
```

### 4.3. Gestion des Nœuds (Brokers)

#### 4.3.1. Redémarrer un Broker (Rolling Restart)

Un redémarrage d'un broker doit toujours être effectué de manière contrôlée pour éviter une interruption de service (si le facteur de réplication est > 1).

1.  Vérifier qu'il n'y a pas d'URP (`kafka-topics.sh --under-replicated-partitions`).
2.  Arrêter le service Kafka sur le nœud cible : `sudo systemctl stop kafka`.
3.  Attendre que le service soit complètement arrêté.
4.  Démarrer le service : `sudo systemctl start kafka`.
5.  Vérifier les logs (`/var/log/kafka/server.log`) pour s'assurer du bon démarrage.
6.  **Important :** Attendre que le broker ait fini de synchroniser ses partitions (URP = 0) avant de passer au nœud suivant.

## 5. Résolution d'Incidents (Troubleshooting)

### 5.1. Incident : Broker Inaccessible / Crash

**Symptômes :** Alertes Grafana (Broker Down), augmentation des URP, erreurs de connexion côté clients.

**Actions :**
1.  Vérifier l'état du service OS : `systemctl status kafka`.
2.  Consulter les logs système : `journalctl -u kafka -n 100`.
3.  Consulter les logs Kafka : `tail -n 100 /var/log/kafka/server.log`.
4.  Vérifier l'espace disque : `df -h /var/lib/kafka/data`. Un disque plein (100%) provoque le crash immédiat de Kafka.
5.  Vérifier la consommation mémoire (OOM Killer) : `dmesg -T | grep -i oom`.
6.  Si le disque est plein, réduire temporairement la rétention des topics les plus volumineux (voir 4.2.2) ou purger manuellement des anciens segments (avec précaution).

### 5.2. Incident : Latence Élevée (High Latency)

**Symptômes :** Alertes Grafana (Produce/Fetch Latency), ralentissement global des applications.

**Actions :**
1.  Vérifier l'utilisation CPU et IOPS des brokers (Grafana/Node Exporter).
2.  Identifier s'il y a un pic de trafic anormal (Network Bytes In/Out).
3.  Vérifier les logs de Garbage Collection (GC) de la JVM Kafka. Des pauses GC trop longues (Stop-The-World) peuvent causer de la latence.
4.  Analyser le comportement des clients (producteurs qui envoient de trop petits batchs, ou sans compression).

### 5.3. Incident : Consumer Lag Important

**Symptômes :** Les données mettent du temps à apparaître dans OpenSearch/Kibana, alertes sur le Consumer Lag.

**Actions :**
1.  Identifier le groupe de consommateurs en difficulté (voir 4.1.3).
2.  Vérifier l'état de l'application consommatrice (ex: Logstash est-il surchargé ? CPU à 100% ?).
3.  Vérifier s'il y a des erreurs de parsing ou de connexion dans les logs de Logstash/Filebeat.
4.  Si possible, scaler horizontalement l'application consommatrice (ajouter des instances) pour paralléliser le traitement, à condition que le nombre de partitions du topic le permette (Max instances = Max partitions).

## 6. Support Plateforme WWW

L'équipe Data Analytics assure le support spécifique pour les flux de données provenant de la plateforme web (WWW).

*   **Flux critique :** Ingestion des événements d'analyse web (`www-analytics-events`).
*   **SLA :** La perte de données n'est pas tolérée (Acks=all côté producteur). La latence d'ingestion vers OpenSearch doit être inférieure à 5 minutes.
*   **Action spécifique :** En cas de pic de trafic imprévu (ex: campagne marketing), surveiller attentivement le cluster Kafka et les instances Logstash dédiées à ce flux. Prévoir un scaling proactif si nécessaire.
