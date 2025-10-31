
from __future__ import annotations

from typing import List, Optional, Union

try:
    from kafka.admin import AdminClient, NewTopic
    from kafka.cluster import ClusterMetadata
except Exception as exc:  # pragma: no cover
    raise ImportError(
        "kafka-python is required for KafkaAdminPort. "
        "Install it with `pip install kafka-python`."
    ) from exc


class KafkaAdminPort:
    """
    Interface for Kafka admin operations.
    This class provides a simple wrapper around kafka-python's AdminClient
    to create, delete, and list topics.
    """

    def __init__(
        self,
        bootstrap_servers: Union[str, List[str]],
        *,
        client_config: Optional[dict] = None,
    ) -> None:
        """
        Initialize the KafkaAdminPort.

        Args:
            bootstrap_servers: A comma‑separated string or a list of broker
                addresses.
            client_config: Optional dictionary of additional configuration
                options for the AdminClient.
        """
        config = {"bootstrap.servers": bootstrap_servers}
        if client_config:
            config.update(client_config)
        self._client = AdminClient(config)

    def create_topic(
        self,
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
    ) -> None:
        """
        Creates a new Kafka topic.

        Args:
            topic: Name of the topic to create.
            num_partitions: Number of partitions for the topic.
            replication_factor: Replication factor for the topic.

        Raises:
            RuntimeError: If the topic could not be created.
        """
        new_topic = NewTopic(
            name=topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        futures = self._client.create_topics([new_topic])
        try:
            futures[topic].result()
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to create topic {topic!r}") from exc

    def delete_topic(self, topics: List[str]) -> None:
        """
        Deletes one or more Kafka topics.

        Args:
            topics: List of topic names to delete.

        Raises:
            RuntimeError: If any topic could not be deleted.
        """
        futures = self._client.delete_topics(topics)
        for topic in topics:
            try:
                futures[topic].result()
            except Exception as exc:  # pragma: no cover
                raise RuntimeError(
                    f"Failed to delete topic {topic!r}") from exc

    def list_topics(
        self,
        topic:
