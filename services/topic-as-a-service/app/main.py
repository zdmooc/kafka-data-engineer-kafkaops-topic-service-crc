from __future__ import annotations

import time
from typing import Any, Dict, List

import structlog
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from .audit import build_audit_sink
from .auth import require_auth
from .config import settings
from .governance import Governance, GovernanceError
from .kafka_admin import KafkaAdmin
from .logging import setup_logging
from .metrics import KAFKA_ADMIN_CALLS, metrics_endpoint
from .models import TopicConfigUpdateRequest, TopicCreateRequest

setup_logging()
log = structlog.get_logger()

app = FastAPI(title="Topic as a Service", version="0.1.0")

gov = Governance(settings.governance_topic_name_regex, settings.governance_require_labels)
admin = KafkaAdmin(settings.kafka_bootstrap_servers)
audit = build_audit_sink(settings.audit_sink, settings.opensearch_url, settings.opensearch_index)


@app.get("/health")
def health() -> Dict[str, Any]:
    with KAFKA_ADMIN_CALLS.labels(op="health").time():
        return {"status": "ok", "kafka": admin.health()}


@app.get("/metrics")
def metrics():
    return metrics_endpoint()


@app.get("/v1/topics", dependencies=[Depends(require_auth)])
def list_topics() -> Dict[str, Any]:
    with KAFKA_ADMIN_CALLS.labels(op="list_topics").time():
        topics = admin.list_topics()
    return {"count": len(topics), "topics": topics}


@app.get("/v1/topics/{name}", dependencies=[Depends(require_auth)])
def get_topic(name: str) -> Dict[str, Any]:
    try:
        with KAFKA_ADMIN_CALLS.labels(op="describe_topic").time():
            info = admin.describe_topic(name)
        with KAFKA_ADMIN_CALLS.labels(op="get_topic_configs").time():
            cfg = admin.get_topic_configs(name)
        return {"topic": info, "configs": cfg}
    except KeyError:
        raise HTTPException(status_code=404, detail="Topic not found")


@app.post("/v1/topics", status_code=201, dependencies=[Depends(require_auth)])
def create_topic(req: TopicCreateRequest) -> Dict[str, Any]:
    try:
        gov.validate_topic(req.name, req.labels)
    except GovernanceError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with KAFKA_ADMIN_CALLS.labels(op="create_topic").time():
        admin.create_topic(
            name=req.name,
            partitions=req.partitions,
            replication_factor=req.replication_factor,
            configs=req.configs,
        )

    audit.emit(
        "topic_created",
        {
            "topic": req.name,
            "partitions": req.partitions,
            "replication_factor": req.replication_factor,
            "configs": req.configs,
            "labels": req.labels,
            "description": req.description,
        },
    )
    return {"status": "created", "topic": req.name}


@app.post("/v1/topics/{name}/configs", dependencies=[Depends(require_auth)])
def update_configs(name: str, req: TopicConfigUpdateRequest) -> Dict[str, Any]:
    with KAFKA_ADMIN_CALLS.labels(op="alter_topic_configs").time():
        admin.alter_topic_configs(name, req.configs)
    audit.emit("topic_configs_updated", {"topic": name, "configs": req.configs})
    return {"status": "updated", "topic": name}


@app.delete("/v1/topics/{name}", dependencies=[Depends(require_auth)])
def delete_topic(
    name: str,
    x_confirm_delete: str | None = Header(default=None, alias="X-Confirm-Delete"),
) -> Dict[str, Any]:
    if x_confirm_delete != "true":
        raise HTTPException(
            status_code=400,
            detail="Deletion is protected. Add header X-Confirm-Delete: true",
        )
    with KAFKA_ADMIN_CALLS.labels(op="delete_topic").time():
        admin.delete_topic(name)
    audit.emit("topic_deleted", {"topic": name})
    return {"status": "deleted", "topic": name}


@app.exception_handler(Exception)
def unhandled(ex: Exception):
    log.exception("unhandled_error", error=str(ex))
    return JSONResponse(status_code=500, content={"detail": "Internal error"})
