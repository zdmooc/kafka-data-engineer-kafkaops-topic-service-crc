from __future__ import annotations

from typing import Any, Dict, List, Tuple

from confluent_kafka import Consumer, TopicPartition
from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic


def list_topics(bootstrap: str) -> List[str]:
    c = AdminClient({"bootstrap.servers": bootstrap})
    md = c.list_topics(timeout=10)
    return sorted(list(md.topics.keys()))


def describe_topic(bootstrap: str, name: str) -> Dict[str, Any]:
    c = AdminClient({"bootstrap.servers": bootstrap})
    md = c.list_topics(topic=name, timeout=10)
    if name not in md.topics:
        raise KeyError(name)
    t = md.topics[name]
    partitions = len(t.partitions)
    rf = 0
    if partitions > 0:
        any_p = next(iter(t.partitions.values()))
        rf = len(any_p.replicas)
    return {"name": name, "partitions": partitions, "replication_factor": rf}


def create_topic(bootstrap: str, name: str, partitions: int, rf: int, configs: Dict[str, str]) -> None:
    c = AdminClient({"bootstrap.servers": bootstrap})
    fs = c.create_topics([NewTopic(topic=name, num_partitions=partitions, replication_factor=rf, config=configs)])
    fs[name].result(timeout=30)


def alter_topic_configs(bootstrap: str, name: str, configs: Dict[str, str]) -> None:
    c = AdminClient({"bootstrap.servers": bootstrap})
    res = ConfigResource(ConfigResource.Type.TOPIC, name, set_config=configs)
    fs = c.alter_configs([res])
    fs[res].result(timeout=30)


def get_topic_configs(bootstrap: str, name: str) -> Dict[str, str]:
    c = AdminClient({"bootstrap.servers": bootstrap})
    res = ConfigResource(ConfigResource.Type.TOPIC, name)
    fs = c.describe_configs([res])
    cfg = fs[res].result(timeout=30)
    out: Dict[str, str] = {}
    for k, entry in cfg.items():
        if entry is None or getattr(entry, "value", None) is None:
            continue
        out[str(k)] = str(entry.value)
    return out


def delete_topic(bootstrap: str, name: str) -> None:
    c = AdminClient({"bootstrap.servers": bootstrap})
    fs = c.delete_topics([name])
    fs[name].result(timeout=30)


def compute_lag(bootstrap: str, group: str, topic_prefix: str | None = None) -> Dict[str, Any]:
    # Best-effort lag computation using Consumer group offsets vs end offsets.
    # Requires that the group exists and that the broker supports listing offsets.
    conf = {
        "bootstrap.servers": bootstrap,
        "group.id": group,
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(conf)
    try:
        # Get assignments from committed offsets
        committed = consumer.committed([], timeout=10)  # empty -> current assignment, may be empty
        # Fallback: list topics and build partitions for topics with committed offsets by fetching group offsets is not exposed directly.
        # We'll approximate by reading watermark offsets for all partitions of matching topics and compare to committed=-1001 sentinel.
        md = consumer.list_topics(timeout=10)
        tnames = sorted(md.topics.keys())
        if topic_prefix:
            tnames = [t for t in tnames if t.startswith(topic_prefix)]
        parts: List[TopicPartition] = []
        for t in tnames:
            for pid in md.topics[t].partitions.keys():
                parts.append(TopicPartition(t, int(pid)))
        committed = consumer.committed(parts, timeout=10)

        rows = []
        total_lag = 0
        for tp in committed:
            low, high = consumer.get_watermark_offsets(TopicPartition(tp.topic, tp.partition), timeout=10)
            end = high
            com = tp.offset
            # If offset is invalid, lag unknown
            if com < 0:
                lag = None
            else:
                lag = max(0, end - com)
                total_lag += int(lag)
            rows.append(
                {
                    "topic": tp.topic,
                    "partition": tp.partition,
                    "committed": com,
                    "end": end,
                    "lag": lag,
                }
            )
        return {"group": group, "total_lag": total_lag, "partitions": rows}
    finally:
        consumer.close()
