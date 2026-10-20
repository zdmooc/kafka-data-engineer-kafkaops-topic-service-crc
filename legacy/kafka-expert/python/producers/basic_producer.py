import json
import time
import random
import os
from kafka import KafkaProducer
from datetime import datetime

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = "www-analytics-events"

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def create_producer():
    """
    Crée et retourne un producteur Kafka configuré pour l'équipe Data Analytics.
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=json_serializer,
            acks='all',  # Ensure data durability
            retries=3,
            linger_ms=10, # Batching for better throughput
            compression_type='gzip'
        )
        print(f"Producer connected to {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        print(f"Failed to connect producer: {e}")
        return None

def generate_mock_data():
    """
    Génère des données analytiques fictives pour la plateforme WWW.
    """
    event_types = ['page_view', 'click', 'form_submit', 'purchase']
    users = [f"user_{i}" for i in range(1, 100)]
    pages = ['/home', '/products', '/about', '/checkout']
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": random.choice(event_types),
        "user_id": random.choice(users),
        "page_url": random.choice(pages),
        "session_duration_sec": random.randint(10, 600),
        "source": "www-platform"
    }

if __name__ == "__main__":
    producer = create_producer()
    
    if producer:
        try:
            print(f"Starting to produce messages to topic '{TOPIC_NAME}'...")
            while True:
                data = generate_mock_data()
                
                # Send message asynchronously
                future = producer.send(TOPIC_NAME, value=data)
                
                # Wait for result (optional, but good for debugging)
                record_metadata = future.get(timeout=10)
                print(f"Sent: {data['event_type']} to partition {record_metadata.partition} at offset {record_metadata.offset}")
                
                time.sleep(random.uniform(0.1, 1.0)) # Simulate traffic
                
        except KeyboardInterrupt:
            print("Stopping producer...")
        finally:
            producer.flush()
            producer.close()
            print("Producer closed.")
