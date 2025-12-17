from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic
from tenacity import retry, stop_after_attempt, wait_fixed


@dataclass
class KafkaAdmin:
    bootstrap: str

    def _client(self) -> AdminClient:
        return AdminClient({"bootstrap.servers": self.bootstrap})

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
    def health(self) -> Dict[str, object]:
        c = self._client()
        md = c.list_topics(timeout=5)
        brokers = [{"id": b.id, "host": b.host, "port": b.port} for b in md.brokers.values()]
        controller = getattr(md, "controller_id", None)
        return {
            "bootstrap": self.bootstrap,
            "brokers": brokers,
            "broker_count": len(brokers),
            "controller_id": controller,
        }

    def list_topics(self, timeout: int = 10) -> List[str]:
        c = self._client()
        md = c.list_topics(timeout=timeout)
        return sorted(list(md.topics.keys()))

    def describe_topic(self, name: str, timeout: int = 10) -> Dict[str, object]:
        c = self._client()
        md = c.list_topics(topic=name, timeout=timeout)
        if name not in md.topics:
            raise KeyError(name)
        t = md.topics[name]
        partitions = len(t.partitions)
        rf = None
        if partitions > 0:
            any_p = next(iter(t.partitions.values()))
            rf = len(any_p.replicas)
        return {"name": name, "partitions": partitions, "replication_factor": rf or 0}

    def create_topic(
        self,
        name: str,
        partitions: int,
        replication_factor: int,
        configs: Dict[str, str],
        timeout: int = 30,
    ) -> None:
        c = self._client()
        fs = c.create_topics(
            [NewTopic(topic=name, num_partitions=partitions, replication_factor=replication_factor, config=configs)]
        )
        f = fs[name]
        f.result(timeout=timeout)

    def delete_topic(self, name: str, timeout: int = 30) -> None:
        c = self._client()
        fs = c.delete_topics([name])
        fs[name].result(timeout=timeout)

    def alter_topic_configs(self, name: str, configs: Dict[str, str], timeout: int = 30) -> None:
        c = self._client()
        res = ConfigResource(ConfigResource.Type.TOPIC, name, set_config=configs)
        fs = c.alter_configs([res])
        fs[res].result(timeout=timeout)

    def get_topic_configs(self, name: str, timeout: int = 30) -> Dict[str, str]:
        c = self._client()
        res = ConfigResource(ConfigResource.Type.TOPIC, name)
        fs = c.describe_configs([res])
        cfg = fs[res].result(timeout=timeout)
        # cfg: dict of ConfigEntry
        out: Dict[str, str] = {}
        for k, entry in cfg.items():
            if entry is None:
                continue
            if getattr(entry, "value", None) is None:
                continue
            out[str(k)] = str(entry.value)
        return out
