# Ansible - Automatisation Kafka

**Auteur :** Zidane Djamal

Ce répertoire contient les playbooks et rôles Ansible pour le déploiement automatisé et la gestion du cluster Apache Kafka en mode KRaft.

## Structure

```
ansible/
├── inventories/
│   └── production.yml          # Inventaire des serveurs de production
├── playbooks/
│   └── deploy_kafka.yml        # Playbook principal de déploiement
└── roles/
    └── kafka/
        ├── defaults/main.yml   # Variables par défaut
        ├── handlers/main.yml   # Handlers (restart)
        ├── tasks/main.yml      # Tâches de déploiement
        ├── templates/
        │   ├── server.properties.j2  # Configuration Kafka (Jinja2)
        │   └── kafka.service.j2      # Service systemd (Jinja2)
        └── vars/main.yml      # Variables de production
```

## Utilisation

### Déployer le cluster Kafka

```bash
ansible-playbook -i inventories/production.yml playbooks/deploy_kafka.yml
```

### Déployer uniquement les brokers

```bash
ansible-playbook -i inventories/production.yml playbooks/deploy_kafka.yml --limit kafka_brokers
```

### Vérifier sans appliquer (Dry Run)

```bash
ansible-playbook -i inventories/production.yml playbooks/deploy_kafka.yml --check --diff
```
