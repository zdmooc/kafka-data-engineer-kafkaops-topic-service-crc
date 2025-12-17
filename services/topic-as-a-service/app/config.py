from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from typing import List


def _csv(name: str, default: str = "") -> List[str]:
    v = getenv(name, default).strip()
    if not v:
        return []
    return [x.strip() for x in v.split(",") if x.strip()]


@dataclass(frozen=True)
class Settings:
    app_port: int = int(getenv("APP_PORT", "8088"))

    kafka_bootstrap_servers: str = getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    auth_mode: str = getenv("AUTH_MODE", "disabled")  # disabled | api_key
    api_key: str = getenv("API_KEY", "")

    governance_topic_name_regex: str = getenv(
        "GOVERNANCE_TOPIC_NAME_REGEX", r"^[a-z0-9]+(\.[a-z0-9]+)*\.v[0-9]+$"
    )
    governance_require_labels: List[str] = _csv("GOVERNANCE_REQUIRE_LABELS", "owner,env")

    audit_sink: str = getenv("AUDIT_SINK", "stdout")  # stdout | opensearch
    opensearch_url: str = getenv("OPENSEARCH_URL", "")
    opensearch_index: str = getenv("OPENSEARCH_INDEX", "kafka-admin-audit")


settings = Settings()
