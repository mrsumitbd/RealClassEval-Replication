
from abc import ABC, abstractmethod
from typing import List, Optional, Union

try:
    from kafka.admin import KafkaAdminClient, NewTopic
    from kafka.cluster import ClusterMetadata
except ImportError:
    # If kafka-python is not installed, provide minimal stubs for type checking
    KafkaAdminClient = None
    NewTopic = None
    ClusterMetadata = None


class KafkaAdminPort(ABC):
    """Interface for Kafka admin operations.
    This interface defines the contract for performing administrative operations on Kafka topics.
    """

    @abstractmethod
    def create_topic(
        self, topic: str, num_partitions: int = 1, replication_factor: int = 1
    ) -> None:
        """Creates a new Kafka topic.
        Args:
            topic (str): Name of the topic to create.
            num_partitions (int, optional): Number of partitions for the topic. Defaults to 1.
            replication_factor (int, optional): Replication factor for the topic. Defaults to 1.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str]) -> None:
        """Deletes one or more Kafka topics.
        Args:
            topics (list[str]): List of topic names to delete.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def list_topics(
        self, topic: Optional[str] = None, timeout: int = 1
    ) -> ClusterMetadata:
        """Lists Kafka topics.
        Args:
            topic (str | None, optional): Specific topic to list. If None, lists all topics.
                Defaults to None.
            timeout (int, optional): Timeout in seconds for the operation. Defaults to 1.
        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass


class KafkaAdminClientImpl(KafkaAdminPort):
    """Concrete implementation of KafkaAdminPort using kafka-python."""

    def __init__(self, bootstrap_servers: Union[str, List[str]], **kwargs):
        if KafkaAdminClient is None:
            raise ImportError(
                "kafka-python is required for KafkaAdminClientImpl")
        self._admin = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers, **kwargs
        )

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
        except Exception as exc:
            raise RuntimeError(
                f"Failed to create topic '{topic}': {exc}") from exc

    def delete_topic(self, topics: List[str]) -> None:
        try:
            self._admin.delete_topics(topics)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to delete topics {topics}: {exc}") from exc

    def list_topics(
        self, topic: Optional[str] = None, timeout: int = 1
    ) -> ClusterMetadata:
        try:
            # describe_cluster returns ClusterMetadata
            metadata = self._admin.describe_cluster()
            if topic:
                # Filter metadata to include only the requested topic
                if topic not in metadata.topics:
                    raise ValueError(f"Topic '{topic}' not found in cluster")
            return metadata
        except Exception as exc:
            raise RuntimeError(f"Failed to list topics: {exc}") from exc
