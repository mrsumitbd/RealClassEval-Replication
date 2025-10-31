from __future__ import annotations

from typing import Iterable, Optional

from confluent_kafka import AdminClient, NewTopic
from confluent_kafka.cimpl import ClusterMetadata


class KafkaAdminPort:
    def __init__(self, bootstrap_servers: str | Iterable[str], **config) -> None:
        if isinstance(bootstrap_servers, str):
            bs = bootstrap_servers
        else:
            bs = ",".join(bootstrap_servers)
        self._client = AdminClient({"bootstrap.servers": bs, **config})

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        if not isinstance(topic, str) or not topic:
            raise ValueError("topic must be a non-empty string")
        if num_partitions <= 0:
            raise ValueError("num_partitions must be > 0")
        if replication_factor <= 0:
            raise ValueError("replication_factor must be > 0")

        futures = self._client.create_topics(
            [NewTopic(topic=topic, num_partitions=num_partitions,
                      replication_factor=replication_factor)]
        )
        fut = futures.get(topic)
        if fut is None:
            raise RuntimeError("Failed to obtain future for topic creation")
        try:
            fut.result()
        except Exception as e:
            # If topic already exists, swallow; otherwise re-raise
            msg = str(e).lower()
            if "already exists" in msg or "topic_exists" in msg:
                return
            raise

    def delete_topic(self, topics: list[str]) -> None:
        if not isinstance(topics, list) or not topics or not all(isinstance(t, str) and t for t in topics):
            raise ValueError(
                "topics must be a non-empty list of non-empty strings")

        futures = self._client.delete_topics(topics)
        for t, fut in futures.items():
            try:
                fut.result()
            except Exception as e:
                # If topic not found, swallow; otherwise re-raise
                msg = str(e).lower()
                if "unknown topic" in msg or "unknown_topic_or_part" in msg or "not found" in msg:
                    continue
                raise

    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
        return self._client.list_topics(topic=topic, timeout=timeout)
