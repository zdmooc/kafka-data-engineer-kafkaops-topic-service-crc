# Documentation du Projet : Topic As A Service (TaaS)

**Équipe :** Data Analytics
**Auteur :** Zidane Djamal (Architect HLD/DDL Kafka)
**Version :** 1.0

## 1. Introduction au Projet TaaS

Le projet **Topic As A Service (TaaS)** est une initiative de l'équipe Data Analytics visant à automatiser et à sécuriser le processus de création et de gestion des topics Kafka au sein de l'entreprise. 

L'objectif principal est de fournir aux développeurs, aux data engineers et aux différentes équipes métiers un moyen standardisé, auditable et en libre-service pour demander et obtenir des ressources Kafka (topics, accès, quotas) sans intervention manuelle systématique de l'équipe d'administration.

### 1.1. Pourquoi le TaaS ?

*   **Réduction du Time-to-Market :** Les équipes n'ont plus besoin d'attendre la création manuelle d'un topic via un ticket de support (Jira/ServiceNow).
*   **Standardisation :** Les topics sont créés avec des conventions de nommage strictes, des configurations optimales (partitions, réplication, rétention) définies par l'architecture HLD/DDL.
*   **Sécurité et Gouvernance :** Les créations sont tracées, les propriétaires (owners) sont identifiés, et les ACLs (Access Control Lists) peuvent être gérées de manière programmatique.
*   **Self-Service :** Responsabilisation des équipes productrices et consommatrices.

## 2. Architecture de la Solution TaaS

La solution repose sur une architecture orientée API développée en Python.

### 2.1. Composants

1.  **API REST (Python / FastAPI) :** Le cœur du système. Expose des endpoints HTTP pour la gestion des topics. Elle valide les requêtes, applique les règles métier et interagit avec le cluster Kafka via le client administrateur.
2.  **Kafka Admin Client :** Bibliothèque Python (`kafka-python` ou `confluent-kafka`) utilisée par l'API pour envoyer les commandes de création/modification au cluster Kafka.
3.  **Base de Données (Optionnel mais recommandé) :** Pour stocker les métadonnées des topics (propriétaire, centre de coût, description, date de création) qui ne sont pas gérées nativement par Kafka. (Peut être une base PostgreSQL ou un index OpenSearch).
4.  **Interface Utilisateur (Portail Interne) :** Une interface web simple ou une intégration avec un portail développeur existant (ex: Backstage) appelant l'API REST.

### 2.2. Flux de Création d'un Topic

1.  Un développeur soumet une requête via le portail ou directement via l'API REST.
2.  L'API REST valide la requête (convention de nommage, quotas, paramètres autorisés).
3.  Si la requête est valide, l'API utilise le `KafkaAdminClient` pour créer le topic sur le cluster avec les configurations spécifiées (partitions, facteur de réplication, rétention).
4.  L'API met à jour la base de données de métadonnées.
5.  L'API retourne une réponse de succès au développeur.

## 3. Utilisation de l'API REST (Documentation Technique)

L'API est développée en Python en utilisant le framework FastAPI. Le code source se trouve dans `/python/api/topic_as_a_service.py`.

### 3.1. Démarrer l'API localement

```bash
# Prérequis : Python 3.9+, pip
pip install fastapi uvicorn kafka-python pydantic

# Définir l'adresse du cluster Kafka
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"

# Lancer le serveur uvicorn
uvicorn python.api.topic_as_a_service:app --host 0.0.0.0 --port 8000 --reload
```

Une fois lancée, la documentation interactive Swagger est disponible sur `http://localhost:8000/docs`.

### 3.2. Endpoints Principaux

#### 3.2.1. Créer un Topic (POST `/topics/`)

Permet de créer un nouveau topic. Les valeurs par défaut (partitions=3, replication_factor=3, rétention=7 jours) sont appliquées si elles ne sont pas spécifiées, conformément aux standards de l'équipe Data Analytics.

**Requête (JSON) :**

```json
{
  "name": "www-analytics-events",
  "partitions": 6,
  "replication_factor": 3,
  "retention_ms": 1209600000, 
  "owner": "equipe-marketing"
}
```
*(Note : `1209600000` ms = 14 jours)*

**Réponse de Succès (201 Created) :**

```json
{
  "message": "Topic created successfully",
  "topic_name": "www-analytics-events"
}
```

**Erreurs possibles :**
*   `409 Conflict` : Le topic existe déjà.
*   `422 Unprocessable Entity` : Erreur de validation des données d'entrée.
*   `500 Internal Server Error` : Problème de communication avec le cluster Kafka.

#### 3.2.2. Lister les Topics (GET `/topics/`)

Retourne la liste de tous les topics présents sur le cluster.

**Réponse (200 OK) :**

```json
{
  "topics": [
    "www-analytics-events",
    "app-logs",
    "system-metrics",
    "__consumer_offsets"
  ]
}
```

## 4. Évolutions Futures du TaaS

Pour améliorer la plateforme, les fonctionnalités suivantes sont prévues dans la roadmap de l'équipe Data Analytics :

1.  **Gestion des ACLs :** Automatiser la création des règles d'autorisation (qui peut produire, qui peut consommer) en même temps que la création du topic.
2.  **Validation du Schéma (Schema Registry) :** Intégrer la validation des schémas (Avro, Protobuf, JSON Schema) lors de la création du topic pour garantir la qualité des données.
3.  **Gestion du Cycle de Vie :** Implémenter des endpoints pour modifier la configuration d'un topic existant (ex: augmenter le nombre de partitions, modifier la rétention) ou le supprimer (avec un processus de validation fort).
4.  **Intégration CI/CD :** Permettre la création de topics via des pipelines de déploiement (GitOps) en utilisant des fichiers de déclaration (YAML).
5.  **Quotas et Facturation (Chargeback) :** Mettre en place des quotas d'utilisation par équipe et un système de facturation interne basé sur le volume de données produit/consommé.
