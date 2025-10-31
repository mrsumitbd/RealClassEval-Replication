
from abc import ABC, abstractmethod
from typing import List, Optional

from kafka.admin import KafkaAdminClient, NewTopic, ClusterMetadata
from kafka.errors import KafkaError


class KafkaAdminPort(ABC):
    """Interface for Kafka admin operations.
    This interface defines the contract for performing administrative operations on Kafka topics.
    """

    @abstractmethod
    def create_topic(
        self, topic: str, num_partitions: int = 1, replication_factor: int = 1
    ) -> None:
        """Creates a new Kafka topic."""
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str]) -> None:
        """Deletes one or more Kafka topics."""
        pass

    @abstractmethod
    def list_topics(
        self, topic: Optional[str] = None, timeout: int = 1
    ) -> ClusterMetadata:
        """Lists Kafka topics."""
        pass


class KafkaAdminPortImpl(KafkaAdminPort):
    """Concrete implementation of KafkaAdminPort using kafka-python."""

    def __init__(self, bootstrap_servers: List[str] | str):
        if isinstance(bootstrap_servers, str):
            bootstrap_servers = [bootstrap_servers]
        self._admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def create_topic(
        self, topic: str, num_partitions: int = 1, replication_factor: int = 1
    ) -> None:
        new_topic = NewTopic(
            name=topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        try:
            self._admin.create_topics([new_topic])
        except KafkaError as exc:
            raise RuntimeError(
                f"Failed to create topic '{topic}': {exc}") from exc

    def delete_topic(self, topics: List[str]) -> None:
        try:
            self._admin.delete_topics(topics)
        except KafkaError as exc:
            raise RuntimeError(
                f"Failed to delete topics {topics}: {exc}") from exc

    def list_topics(
        self, topic: Optional[str] = None, timeout: int = 1
    ) -> ClusterMetadata:
        timeout_ms = timeout * 1000
        try:
            # Get cluster metadata
            cluster_info = self._admin.describe_cluster()
            # Get topic metadata
            if topic:
                topics_meta = self._admin.describe_topics([topic])
            else:
                topic_names = self._admin.list_topics(timeout_ms=timeout_ms)
                topics_meta = self._admin.describe_topics(topic_names)
            # Build ClusterMetadata object
            return ClusterMetadata(
                cluster_id=cluster_info["cluster_id"],
                controller_id=cluster_info["controller_id"],
                brokers=cluster_info["brokers"],
                topics=topics_meta,
            )
        except KafkaError as exc:
            raise RuntimeError(f"Failed to list topics: {exc}") from exc
