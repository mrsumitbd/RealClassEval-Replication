
from abc import ABC, abstractmethod
from typing import List, Optional

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.cluster import ClusterMetadata


class KafkaAdminPort(ABC):
    """
    Abstract base class for Kafka administration operations.
    """

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        """Create a new topic in Kafka."""
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str]) -> None:
        """Delete one or more topics from Kafka."""
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        """Return metadata for all topics or a specific topic."""
        pass


class KafkaAdminClientPort(KafkaAdminPort):
    """
    Concrete implementation of KafkaAdminPort using kafka-python's KafkaAdminClient.
    """

    def __init__(self, bootstrap_servers: str | List[str]):
        """
        Initialize the KafkaAdminClientPort.

        :param bootstrap_servers: Kafka bootstrap servers (comma-separated string or list).
        """
        self._admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        """
        Create a new topic in Kafka.

        :param topic: Name of the topic to create.
        :param num_partitions: Number of partitions for the topic.
        :param replication_factor: Replication factor for the topic.
        """
        new_topic = NewTopic(
            name=topic, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self._admin_client.create_topics([new_topic])
        except Exception as exc:
            raise RuntimeError(
                f"Failed to create topic '{topic}': {exc}") from exc

    def delete_topic(self, topics: List[str]) -> None:
        """
        Delete one or more topics from Kafka.

        :param topics: List of topic names to delete.
        """
        try:
            self._admin_client.delete_topics(topics)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to delete topics {topics}: {exc}") from exc

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        """
        Return metadata for all topics or a specific topic.

        :param topic: Optional topic name to filter the metadata.
        :param timeout: Timeout in seconds for the operation (ignored by kafka-python).
        :return: ClusterMetadata object containing topic information.
        """
        try:
            metadata = self._admin_client.describe_cluster()
        except Exception as exc:
            raise RuntimeError(
                f"Failed to retrieve cluster metadata: {exc}") from exc

        if topic is not None:
            # Filter metadata to include only the requested topic
            filtered_topics = {topic: metadata.topics.get(
                topic)} if topic in metadata.topics else {}
            # Create a new ClusterMetadata instance with the filtered topics
            filtered_metadata = ClusterMetadata(
                cluster_id=metadata.cluster_id,
                controller_id=metadata.controller_id,
                brokers=metadata.brokers,
                topics=filtered_topics,
                topic_ids=metadata.topic_ids,
                topic_ids_by_name=metadata.topic_ids_by_name,
            )
            return filtered_metadata

        return metadata
