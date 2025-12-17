from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml


@dataclass
class TopicSpec:
    name: str
    partitions: int
    replication_factor: int
    configs: Dict[str, str]
    labels: Dict[str, str]
    description: str | None = None


def load_catalog(path: str) -> List[TopicSpec]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    topics = data.get("topics", [])
    out: List[TopicSpec] = []
    for t in topics:
        out.append(
            TopicSpec(
                name=t["name"],
                partitions=int(t.get("partitions", 1)),
                replication_factor=int(t.get("replication_factor", 1)),
                configs=dict(t.get("configs", {}) or {}),
                labels=dict(t.get("labels", {}) or {}),
                description=t.get("description"),
            )
        )
    return out
