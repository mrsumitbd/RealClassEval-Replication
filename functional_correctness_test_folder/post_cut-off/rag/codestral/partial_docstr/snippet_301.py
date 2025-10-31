
from abc import ABC, abstractmethod
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.cluster import ClusterMetadata


class KafkaAdminPort(ABC):
    '''Interface for Kafka admin operations.
    This interface defines the contract for performing administrative operations on Kafka topics.
    '''

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        '''Creates a new Kafka topic.
        Args:
            topic (str): Name of the topic to create.
            num_partitions (int, optional): Number of partitions for the topic. Defaults to 1.
            replication_factor (int, optional): Replication factor for the topic. Defaults to 1.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass

    @abstractmethod
    def delete_topic(self, topics: list[str]) -> None:
        '''Deletes one or more Kafka topics.
        Args:
            topics (list[str]): List of topic names to delete.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass

    @abstractmethod
    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        '''Lists Kafka topics.
        Args:
            topic (str | None, optional): Specific topic to list. If None, lists all topics.
                Defaults to None.
            timeout (int, optional): Timeout in seconds for the operation. Defaults to 1.
        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass


class KafkaAdminClientImpl(KafkaAdminPort):
    '''Concrete implementation of KafkaAdminPort using KafkaAdminClient.'''

    def __init__(self, bootstrap_servers: str):
        '''Initializes the KafkaAdminClientImpl.
        Args:
            bootstrap_servers (str): Comma-separated list of Kafka broker addresses.
        '''
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        '''Creates a new Kafka topic.
        Args:
            topic (str): Name of the topic to create.
            num_partitions (int, optional): Number of partitions for the topic. Defaults to 1.
            replication_factor (int, optional): Replication factor for the topic. Defaults to 1.
        '''
        new_topic = NewTopic(
            name=topic, num_partitions=num_partitions, replication_factor=replication_factor)
        self.admin_client.create_topics([new_topic])

    def delete_topic(self, topics: list[str]) -> None:
        '''Deletes one or more Kafka topics.
        Args:
            topics (list[str]): List of topic names to delete.
        '''
        self.admin_client.delete_topics(topics)

    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        '''Lists Kafka topics.
        Args:
            topic (str | None, optional): Specific topic to list. If None, lists all topics.
                Defaults to None.
            timeout (int, optional): Timeout in seconds for the operation. Defaults to 1.
        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        '''
        if topic:
            return self.admin_client.describe_topics([topic], timeout_ms=timeout * 1000)
        return self.admin_client.describe_topics(timeout_ms=timeout * 1000)
