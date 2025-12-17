from __future__ import annotations

from typing import Any, Dict

from confluent_kafka.admin import AdminClient


def cluster_health(bootstrap: str) -> Dict[str, Any]:
    c = AdminClient({"bootstrap.servers": bootstrap})
    md = c.list_topics(timeout=10)
    brokers = [{"id": b.id, "host": b.host, "port": b.port} for b in md.brokers.values()]
    controller = getattr(md, "controller_id", None)
    return {"bootstrap": bootstrap, "broker_count": len(brokers), "brokers": brokers, "controller_id": controller}
