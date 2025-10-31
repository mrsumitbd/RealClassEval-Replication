
from abc import ABC, abstractmethod
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from typing import List, Optional, Union
from kafka.metadata import ClusterMetadata


class KafkaAdminPort(ABC):
    """Interface for Kafka admin operations.
    This interface defines the contract for performing administrative operations on Kafka topics.
    """

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
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
            topics (List[str]): List of topic names to delete.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        """Lists Kafka topics.

        Args:
            topic (Optional[str], optional): Specific topic to list. If None, lists all topics.
                Defaults to None.
            timeout (int, optional): Timeout in seconds for the operation. Defaults to 1.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass


class KafkaAdmin(KafkaAdminPort):
    """Implementation of KafkaAdminPort using KafkaAdminClient."""

    def __init__(self, bootstrap_servers: str):
        """Initializes a KafkaAdmin instance.

        Args:
            bootstrap_servers (str): Bootstrap servers for the Kafka cluster.
        """
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        """Creates a new Kafka topic.

        Args:
            topic (str): Name of the topic to create.
            num_partitions (int, optional): Number of partitions for the topic. Defaults to 1.
            replication_factor (int, optional): Replication factor for the topic. Defaults to 1.
        """
        try:
            new_topic = NewTopic(topic, num_partitions, replication_factor)
            self.admin_client.create_topics([new_topic])
        except TopicAlreadyExistsError:
            print(f"Topic {topic} already exists.")

    def delete_topic(self, topics: List[str]) -> None:
        """Deletes one or more Kafka topics.

        Args:
            topics (List[str]): List of topic names to delete.
        """
        try:
            self.admin_client.delete_topics(topics)
        except UnknownTopicOrPartitionError:
            print(f"One or more topics {topics} do not exist.")

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        """Lists Kafka topics.

        Args:
            topic (Optional[str], optional): Specific topic to list. If None, lists all topics.
                Defaults to None.
            timeout (int, optional): Timeout in seconds for the operation. Defaults to 1.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        """
        return self.admin_client.list_topics(topic, timeout_ms=timeout * 1000)
