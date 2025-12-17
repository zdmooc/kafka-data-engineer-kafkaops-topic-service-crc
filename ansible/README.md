# Ansible usage

## Local demo (Docker Compose)
1) Start stack
```bash
cd ..
make up
```

2) Run healthcheck
```bash
cd ansible
ansible-playbook playbooks/10-kafka-health.yml
```

3) Apply catalog
```bash
ansible-playbook playbooks/20-apply-topic-catalog.yml
```

4) Collect evidence
```bash
ansible-playbook playbooks/30-collect-evidence.yml
```
