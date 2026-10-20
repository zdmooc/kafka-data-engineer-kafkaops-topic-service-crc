import json
import os
from kafka import KafkaConsumer

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = "www-analytics-events"
GROUP_ID = "data-analytics-consumer-group"

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

def create_consumer():
    """
    Crée et retourne un consommateur Kafka configuré pour l'équipe Data Analytics.
    """
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            value_deserializer=json_deserializer,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=5000,
            max_poll_records=500
        )
        print(f"Consumer connected to {KAFKA_BOOTSTRAP_SERVERS}, subscribed to '{TOPIC_NAME}'")
        return consumer
    except Exception as e:
        print(f"Failed to connect consumer: {e}")
        return None

def process_message(message):
    """
    Traite un message consommé depuis Kafka.
    Peut être étendu pour envoyer les données vers OpenSearch, une base de données, etc.
    """
    event = message.value
    print(f"Received: topic={message.topic}, partition={message.partition}, offset={message.offset}")
    print(f"  Event: type={event.get('event_type')}, user={event.get('user_id')}, page={event.get('page_url')}")
    
    # TODO: Ajouter la logique de traitement (ex: enrichissement, envoi vers OpenSearch)
    return event

if __name__ == "__main__":
    consumer = create_consumer()
    
    if consumer:
        try:
            print(f"Starting to consume messages from topic '{TOPIC_NAME}'...")
            for message in consumer:
                process_message(message)
                
        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            consumer.close()
            print("Consumer closed.")
