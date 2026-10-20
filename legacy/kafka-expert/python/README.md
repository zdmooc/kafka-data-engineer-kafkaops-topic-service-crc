# Python - APIs et Scripts Kafka

**Auteur :** Zidane Djamal

Ce répertoire contient le code Python pour l'interaction avec le cluster Kafka, incluant l'API REST "Topic As A Service", les producteurs et les consommateurs.

## Structure

```
python/
├── api/
│   └── topic_as_a_service.py   # API REST FastAPI pour la gestion des topics
├── producers/
│   └── basic_producer.py       # Producteur Kafka (événements WWW)
├── consumers/
│   └── basic_consumer.py       # Consommateur Kafka (traitement analytique)
└── requirements.txt            # Dépendances Python
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l'API Topic As A Service

```bash
export KAFKA_BOOTSTRAP_SERVERS="broker1.example.com:9092"
uvicorn python.api.topic_as_a_service:app --host 0.0.0.0 --port 8000
```

Documentation Swagger : `http://localhost:8000/docs`

## Lancer le Producteur

```bash
export KAFKA_BOOTSTRAP_SERVERS="broker1.example.com:9092"
python python/producers/basic_producer.py
```

## Lancer le Consommateur

```bash
export KAFKA_BOOTSTRAP_SERVERS="broker1.example.com:9092"
python python/consumers/basic_consumer.py
```
