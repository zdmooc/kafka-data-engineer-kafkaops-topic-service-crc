from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import logging
import os

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Topic As A Service API",
    description="API REST pour la gestion automatisée des topics Kafka pour l'équipe Data Analytics",
    version="1.0.0"
)

# Models
class TopicCreateRequest(BaseModel):
    name: str
    partitions: int = 3
    replication_factor: int = 3
    retention_ms: int = 604800000  # 7 jours par défaut
    owner: str

class TopicResponse(BaseModel):
    message: str
    topic_name: str

# Dependency to get Kafka Admin Client
def get_admin_client():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id='taas_api_client'
        )
        yield admin_client
    except Exception as e:
        logger.error(f"Failed to connect to Kafka Admin: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Cannot connect to Kafka")
    finally:
        if 'admin_client' in locals():
            admin_client.close()

@app.post("/topics/", response_model=TopicResponse, status_code=201)
def create_topic(request: TopicCreateRequest, admin_client: KafkaAdminClient = Depends(get_admin_client)):
    """
    Crée un nouveau topic Kafka avec les configurations spécifiées.
    """
    logger.info(f"Request to create topic '{request.name}' by owner '{request.owner}'")
    
    topic_config = {
        'retention.ms': str(request.retention_ms)
    }
    
    new_topic = NewTopic(
        name=request.name,
        num_partitions=request.partitions,
        replication_factor=request.replication_factor,
        topic_configs=topic_config
    )
    
    try:
        admin_client.create_topics(new_topics=[new_topic], validate_only=False)
        logger.info(f"Topic '{request.name}' created successfully.")
        return TopicResponse(message="Topic created successfully", topic_name=request.name)
    except TopicAlreadyExistsError:
        logger.warning(f"Topic '{request.name}' already exists.")
        raise HTTPException(status_code=409, detail=f"Topic '{request.name}' already exists.")
    except Exception as e:
        logger.error(f"Failed to create topic '{request.name}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create topic: {str(e)}")

@app.get("/topics/")
def list_topics(admin_client: KafkaAdminClient = Depends(get_admin_client)):
    """
    Liste tous les topics existants dans le cluster.
    """
    try:
        topics = admin_client.list_topics()
        return {"topics": topics}
    except Exception as e:
        logger.error(f"Failed to list topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
