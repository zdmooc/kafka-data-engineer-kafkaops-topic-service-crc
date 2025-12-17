# Guide pédagogique bout-en-bout — KafkaOps + Topic-as-a-Service sur OpenShift Local (CRC)

Objectif : disposer d’un **parcours complet** (installation → exploitation → automatisation → troubleshooting) qui simule une mission **Data Engineer Kafka (support/MCO)** sur une plateforme critique.

Ce guide s’appuie sur le dépôt fourni (version CRC) :
- `openshift/crc/*.sh` (déploiement end-to-end)
- `openshift/manifests/**` (YAML OpenShift/Strimzi)
- `services/topic-as-a-service/` (API FastAPI)
- `services/topic-as-a-service/kafkaops_cli/` (CLI KafkaOps)
- `ansible/` (automatisation MCO)
- `runbooks/` et `docs/` (documentation opérationnelle)

---

## 0) Résultat attendu

À la fin, sur **CRC** vous aurez :
- Un cluster Kafka (via **Strimzi Operator**) dans un namespace `kafka-platform`
- Un service **Topic-as-a-Service** exposé par une **Route OpenShift** (`/health`, `/metrics`, `/docs`, `/v1/topics`)
- Une UI Kafka (optionnelle) exposée par Route
- Des scripts d’exploitation (checks, evidence) et des runbooks d’incident

---

## 1) Pré-requis (CRC)

### 1.1 Logiciels
- OpenShift Local (CRC) installé
- `oc` CLI disponible
- Accès cluster-admin (recommandé) pour installer l’opérateur

### 1.2 Démarrer CRC
Commandes usuelles (à adapter à votre machine) :
```bash
crc start
oc login -u kubeadmin -p <password> https://api.crc.testing:6443
```

### 1.3 Vérifier l’état
Depuis la racine du dépôt :
```bash
cd openshift/crc
./00-prereqs.sh
```
Ce script vérifie : présence de `crc`/`oc`, login, et capacité (best effort) d’actions cluster-admin.

---

## 2) Déployer Kafka sur OpenShift (Strimzi)

### 2.1 Installer Strimzi Operator (OperatorHub)
```bash
cd openshift/crc
./10-install-strimzi-operator.sh
```
Ce script :
- crée le namespace `strimzi`
- applique `OperatorGroup` et `Subscription`
- attend le CSV en phase `Succeeded`

Points d’attention :
- Sur CRC, la **source OperatorHub** peut varier (`redhat-operators` vs `community-operators`).
- En cas d’échec : modifier dans le script les variables `SOURCE` / `CHANNEL`.

### 2.2 Déployer un cluster Kafka minimal (CRC)
```bash
./20-deploy-kafka-cluster.sh
```
Ce script :
- crée `kafka-platform`
- déploie un Kafka Strimzi minimal **1 broker** (ephemeral storage) pour CRC
- attend la condition `Ready=True` (best effort)

Vérifications utiles :
```bash
oc -n kafka-platform get kafka
oc -n kafka-platform get pods -o wide
oc -n kafka-platform get svc | grep demo
```

Ce que vous devez voir :
- un service `demo-kafka-bootstrap` (bootstrap interne)
- des pods Kafka/Zookeeper (selon la spec)

---

## 3) Déployer “Topic as a Service” sur CRC

### 3.1 Build de l’image dans OpenShift (BuildConfig)
```bash
./30-deploy-topic-service.sh
```
Ce script :
- crée/configure `Secret` (API_KEY) et `ConfigMap` (KAFKA_BOOTSTRAP_SERVERS, policies)
- crée un `ImageStream` + `BuildConfig`
- lance un `oc start-build --from-dir` depuis `services/topic-as-a-service`
- déploie `Deployment` + `Service` + `Route`

Vérifications utiles :
```bash
oc -n kafka-platform get builds
oc -n kafka-platform logs -f build/topic-as-a-service-1
oc -n kafka-platform get deploy,po,svc,route -l app=topic-as-a-service
```

### 3.2 Auth et gouvernance
Par défaut (CRC) :
- `AUTH_MODE=api_key`
- `API_KEY=change-me` (secret)
- convention de nom : `^[a-z0-9]+(\.[a-z0-9]+)*\.v[0-9]+$`
- labels requis : `owner,env`

Pour changer :
- éditer `openshift/manifests/topic-service/configmap.yaml`
- éditer `openshift/manifests/topic-service/secret.yaml`

---

## 4) Déployer Kafka UI (optionnel)

```bash
./40-deploy-kafka-ui.sh
```
Cela déploie Kafka UI, Service et Route.

---

## 5) Vérifier bout-en-bout

```bash
./50-verify.sh
```
Le script affiche :
- pods/services/routes
- URL du Topic service
- test de `/health`

### 5.1 Tests manuels (depuis votre poste)
Récupérer le host :
```bash
HOST=$(oc -n kafka-platform get route topic-as-a-service -o jsonpath='{.spec.host}')
APIKEY=$(oc -n kafka-platform get secret topic-service-secret -o jsonpath='{.data.API_KEY}' | base64 -d)
```

Health :
```bash
curl -sk "https://$HOST/health" | jq .
```

Lister topics (protégé par API key) :
```bash
curl -sk "https://$HOST/v1/topics" -H "X-API-Key: $APIKEY" | jq .
```

Créer un topic :
```bash
curl -sk -X POST "https://$HOST/v1/topics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $APIKEY" \
  -d '{
    "name": "demo.orders.v1",
    "partitions": 3,
    "replication_factor": 1,
    "configs": {"retention.ms":"86400000","cleanup.policy":"delete"},
    "labels": {"owner":"data-analytics","env":"crc"},
    "description": "Demo topic"
  }' | jq .
```

Mettre à jour des configs :
```bash
curl -sk -X POST "https://$HOST/v1/topics/demo.orders.v1/configs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $APIKEY" \
  -d '{"configs": {"retention.ms":"604800000"}}' | jq .
```

Suppression (protégée) :
```bash
curl -sk -X DELETE "https://$HOST/v1/topics/demo.orders.v1" \
  -H "X-API-Key: $APIKEY" \
  -H "X-Confirm-Delete: true" | jq .
```

---

## 6) Exploitation/MCO : commandes “standard” (support)

### 6.1 Accès au pod et logs
```bash
oc -n kafka-platform get pods
oc -n kafka-platform logs -f deploy/topic-as-a-service
```

### 6.2 Contrôle Kafka (services Strimzi)
```bash
oc -n kafka-platform get svc | grep kafka
```
Bootstrap interne attendu : `demo-kafka-bootstrap:9092`.

### 6.3 Indicateurs d’observabilité (API)
- `/metrics` expose des compteurs/latences (Prometheus client)
- logs JSON (structlog) contiennent les erreurs et événements

---

## 7) Automatisation (Ansible) — version CRC

Le dossier `ansible/` est prévu initialement pour Docker Compose. Pour CRC, on recommande 2 approches :

### Approche A — “oc exec + kafkaops”
- Exécuter le **CLI** dans le pod (ou une image utilitaire) via `oc rsh` / `oc exec`

Exemple (manuel) :
```bash
oc -n kafka-platform rsh deploy/topic-as-a-service kafkaops health --bootstrap demo-kafka-bootstrap:9092
```

### Approche B — adapter les playbooks
- Remplacer `docker compose exec` par `oc exec` dans les playbooks.
- Ajouter une variable `kube_namespace` et `pod_selector`.

Livrables “mission” (future-proof) :
- un rôle Ansible `kafkaops_ocexec` + preuves `evidence/*.json`.

---

## 8) Troubleshooting pédagogique (cas concrets)

### 8.1 L’opérateur Strimzi ne s’installe pas
Symptômes : CSV pas `Succeeded`.
Actions :
```bash
oc -n strimzi get sub,csv
oc -n strimzi describe sub strimzi-kafka-operator
oc -n strimzi get events --sort-by=.lastTimestamp | tail -n 30
```
Corrections fréquentes :
- changer `SOURCE` (`redhat-operators` vs `community-operators`)
- changer `CHANNEL` (stable vs autre)

### 8.2 Kafka CR pas Ready
Actions :
```bash
oc -n kafka-platform describe kafka demo
oc -n kafka-platform get pods -o wide
oc -n kafka-platform get events --sort-by=.lastTimestamp | tail -n 50
```
Sur CRC : ressources limitées, storage ephemeral, timings.

### 8.3 Topic service OK mais création topic échoue
Actions :
```bash
oc -n kafka-platform logs deploy/topic-as-a-service | tail -n 200
```
Causes fréquentes :
- bootstrap mal configuré (`demo-kafka-bootstrap:9092`)
- policy de nommage/labels non respectée

### 8.4 Route OK mais 401 sur /v1/topics
Cause : `AUTH_MODE=api_key`.
Solution : envoyer `X-API-Key`.

---

## 9) Runbooks (incidents) — comment s’en servir

Le dossier `runbooks/` sert à démontrer la posture support :
- **Template incident** : `runbooks/00-incident-template.md`
- URP : `runbooks/10-urp-under-replicated-partitions.md`
- Lag : `runbooks/20-consumer-lag-spike.md`
- Disk : `runbooks/30-broker-disk-full.md`

Exercice pédagogique (simulation) :
1) Créer un topic et produire des messages.
2) Créer un consumer lent → observer lag.
3) Documenter : symptômes, signaux, actions, preuves.

---

## 10) Ce que vous pouvez raconter en entretien (mapping mission)

### Kafka (expertise)
- Mise en place d’un cluster Kafka sur OpenShift via opérateur
- Standardisation d’opérations (health, list/describe/apply)
- Gouvernance topic (naming/labels/retention)

### Support/MCO
- Scripts idempotents d’installation/vérification
- Evidence (logs, metrics, snapshots) et runbooks

### Dév Data Analytics (“Topic as a Service”)
- API REST FastAPI + audit + métriques
- Sécurisation simple (API key), extensible (OIDC plus tard)

### Observabilité (Elastic/OpenSearch)
- Patterns d’intégration et pipelines d’exemple
- KPI opérationnels (latence admin calls, erreurs, health)

---

## 11) Nettoyage / reset (CRC)

Nettoyage minimal (namespaces) :
```bash
oc delete project kafka-platform || true
oc delete project strimzi || true
```

---

## 12) Extensions “avenir” (recommandées)

1) **GitOps Argo CD**
- Utiliser `openshift/gitops/argocd-application-topic-service.yaml` comme base

2) **Sécurité Kafka**
- Ajouter TLS/mTLS, SASL/SCRAM, users Strimzi + ACL

3) **Topic catalog multi-environnements**
- `catalog/topics/dev.yaml`, `preprod.yaml`, `prod.yaml`
- Policies différentes (retention profiles)

4) **Automatisation complète (Ansible)**
- Playbooks “worldwide” multi-inventaires
- Evidence centralisée et reporting hebdo

---

## Check-list finale (à cocher)

- [ ] CRC démarre et `oc whoami` OK
- [ ] Strimzi operator installé (CSV Succeeded)
- [ ] Kafka `demo` Ready
- [ ] Topic-as-a-Service route accessible + `/health` OK
- [ ] Auth API key OK
- [ ] Création topic OK
- [ ] Kafka UI OK
- [ ] Logs + metrics consultables
- [ ] Runbook incident rempli (exercice)

