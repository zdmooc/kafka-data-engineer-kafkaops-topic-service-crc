# Expert Kafka - Architecture et Data Engineering

**Auteur :** Zidane Djamal (Architect HLD/DDL Kafka)  
**Équipe :** Data Analytics  
**Environnement :** Anglophone

Bienvenue dans le dépôt de référence pour l'expertise Kafka au sein de l'équipe Data Analytics. Ce dépôt centralise l'architecture, l'automatisation, le code et la documentation nécessaires pour le support, la mise en œuvre et le maintien en conditions opérationnelles des plateformes Kafka.

## Contexte de la Mission

Dans le cadre de l'équipe Data Analytics, nous créons et maintenons des architectures Big Data pour les besoins internes de l’entreprise. Ce dépôt vise à renforcer notre équipe support avec une mission spécifique de **Data Engineering sur Kafka**.

### Objectifs Principaux
1. **Mise en œuvre de l'expertise sur Kafka** : Conception et déploiement d'architectures robustes (HLD/DDL).
2. **Support et MCO** : Automatisation et maintien en conditions opérationnelles des plateformes Kafka.
3. **Topic As a Service** : Participation aux développements de l'équipe Data Analytics et du projet Topic As a Service.
4. **Support Plateforme WWW** : Assurer la stabilité et la performance des flux de données critiques.

## Technologies Utilisées

### Cœur de l'Architecture Data
* **Apache Kafka** : Épine dorsale de notre architecture de streaming d'événements.
* **Open Search** : Moteur de recherche et d'analyse distribué.
* **Elastic Stack** : 
  * Elasticsearch
  * Logstash
  * Kibana
  * Beats

### Automatisation et Développement
L'équipe met en avant une approche d'automatisation forte ("Infrastructure as Code").
* **Ansible** : Automatisation du déploiement et de la configuration des clusters Kafka et de l'Elastic Stack.
* **Git/Bitbucket** : Gestion de versions et CI/CD.
* **Python** : Développement de scripts de gestion, de producteurs/consommateurs Kafka et de REST APIs.

## Structure du Dépôt

* `/architecture/` : Documents d'Architecture de Haut Niveau (HLD) et de Conception Détaillée (DDL) pour Kafka.
* `/ansible/` : Playbooks et rôles Ansible pour le déploiement automatisé de Kafka, Zookeeper/KRaft, et de l'Elastic Stack.
* `/python/` : Code source Python incluant les APIs REST pour le "Topic As a Service" et les scripts de gestion.
* `/elastic_stack/` : Configurations pour Elasticsearch, Logstash, Kibana et Beats (intégration avec Kafka).
* `/docs/` : Documentation détaillée, procédures de support, runbooks pour le maintien en conditions opérationnelles (MCO).
* `/scripts/` : Scripts utilitaires bash pour les opérations courantes de support.

## Contribution

Ce dépôt est maintenu par l'équipe Data Analytics. Toute contribution doit suivre le processus de revue de code via Pull Request.

---
*Dépôt créé et maintenu pour https://github.com/zdmooc/*
