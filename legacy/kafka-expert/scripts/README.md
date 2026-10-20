# Scripts Utilitaires Kafka

**Auteur :** Zidane Djamal

Ce répertoire contient les scripts bash pour les opérations courantes de support et de maintenance du cluster Kafka.

## Scripts Disponibles

| Script | Description | Usage |
| :--- | :--- | :--- |
| `kafka_healthcheck.sh` | Vérifie la santé globale du cluster Kafka (connectivité, URP, partitions offline, consumer lag). | `./kafka_healthcheck.sh [BOOTSTRAP_SERVER]` |
| `kafka_rolling_restart.sh` | Effectue un rolling restart sécurisé du cluster Kafka en vérifiant l'ISR entre chaque nœud. | `./kafka_rolling_restart.sh <broker_list_file>` |

## Prérequis

Les scripts nécessitent que la variable `KAFKA_HOME` soit définie (par défaut : `/opt/kafka`) et que les outils CLI Kafka soient accessibles.
