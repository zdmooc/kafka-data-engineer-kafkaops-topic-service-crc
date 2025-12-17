from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, Field, constr


class TopicCreateRequest(BaseModel):
    name: constr(min_length=3, max_length=249)  # Kafka max topic name length is 249
    partitions: int = Field(ge=1, le=10000)
    replication_factor: int = Field(ge=1, le=10)
    configs: Dict[str, str] = Field(default_factory=dict)
    labels: Dict[str, str] = Field(default_factory=dict)
    description: Optional[str] = None


class TopicConfigUpdateRequest(BaseModel):
    configs: Dict[str, str]


class TopicInfo(BaseModel):
    name: str
    partitions: int
    replication_factor: int
    configs: Dict[str, str] = Field(default_factory=dict)
    labels: Dict[str, str] = Field(default_factory=dict)
    description: Optional[str] = None
