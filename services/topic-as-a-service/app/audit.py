from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog
from opensearchpy import OpenSearch


log = structlog.get_logger()


@dataclass
class AuditSink:
    kind: str  # stdout | opensearch
    os_client: Optional[OpenSearch] = None
    os_index: str = "kafka-admin-audit"

    def emit(self, event: str, payload: Dict[str, Any]) -> None:
        record = {"event": event, **payload}
        if self.kind == "opensearch" and self.os_client:
            self.os_client.index(index=self.os_index, body=record)
        else:
            log.info("audit", **record)


def build_audit_sink(kind: str, opensearch_url: str, opensearch_index: str) -> AuditSink:
    if kind == "opensearch" and opensearch_url:
        client = OpenSearch(opensearch_url)
        return AuditSink(kind="opensearch", os_client=client, os_index=opensearch_index)
    return AuditSink(kind="stdout")
