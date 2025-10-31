
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from confluent_kafka.admin import AdminClient, NewTopic, ClusterMetadata
from confluent_kafka import KafkaException


class KafkaAdminPort(ABC):
    """Interface for Kafka admin operations.

    Concrete implementations should provide the ability to create, delete,
    and list Kafka topics.
    """

    @abstractmethod
    def create_topic(
        self,
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
        timeout: int = 10,
    ) -> None:
        """Creates a new Kafka topic.

        Args:
            topic: Name of the topic to create.
            num_partitions: Number of partitions for the topic.
            replication_factor: Replication factor for the topic.
            timeout: Timeout in seconds for the operation.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str], timeout: int = 10) -> None:
        """Deletes one or more Kafka topics.

        Args:
            topics: List of topic names to delete.
            timeout: Timeout in seconds for the operation.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def list_topics(
        self,
        topic: Optional[str] = None,
        timeout: int = 10,
    ) -> ClusterMetadata:
        """Lists Kafka topics.

        Args:
            topic: Specific topic to list. If None, lists all topics.
            timeout: Timeout in seconds for the operation.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass


class ConfluentKafkaAdminPort(KafkaAdminPort):
    """Concrete implementation of KafkaAdminPort using confluent_kafka."""

    def __init__(self, bootstrap_servers: Union[str, List[str]], **config):
        """
        Args:
            bootstrap_servers: Kafka bootstrap servers (comma separated string or list).
            **config: Additional configuration for the AdminClient.
        """
        if isinstance(bootstrap_servers, str):
            bootstrap_servers = [bootstrap_servers]
        client_config = {"bootstrap.servers": ",".join(bootstrap_servers)}
        client_config.update(config)
        self._client = AdminClient(client_config)

    def create_topic(
        self,
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
        timeout: int = 10,
    ) -> None:
        new_topic = NewTopic(
            topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        futures = self._client.create_topics(
            [new_topic], request_timeout=timeout)
        future = futures[topic]
        try:
            future.result()
        except KafkaException as exc:
            raise RuntimeError(
                f"Failed to create topic '{topic}': {exc}") from exc

    def delete_topic(self, topics: List[str], timeout: int = 10) -> None:
        futures = self._client.delete_topics(topics, request_timeout=timeout)
        for topic in topics:
            future = futures[topic]
            try:
                future.result()
            except KafkaException as exc:
                raise RuntimeError(
                    f"Failed to delete topic '{topic}': {exc}") from exc

    def list_topics(
        self,
        topic: Optional[str] = None,
        timeout: int = 10,
    ) -> ClusterMetadata:
        metadata = self._client.list_topics(timeout=timeout)
        if topic is not None:
            if topic not in metadata.topics:
                raise ValueError(f"Topic '{topic}' not found in cluster.")
        return metadata

    def close(self) -> None:
        """Close the underlying AdminClient."""
        self._client.close()

    def __enter__(self) -> "ConfluentKafkaAdminPort":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
