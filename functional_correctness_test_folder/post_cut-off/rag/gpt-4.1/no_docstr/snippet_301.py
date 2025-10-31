from abc import abstractmethod, ABC
from typing import Optional, List
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
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
    def delete_topic(self, topics: List[str]) -> None:
        '''Deletes one or more Kafka topics.
        Args:
            topics (list[str]): List of topic names to delete.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
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


class KafkaAdmin(KafkaAdminPort):
    '''Concrete implementation of KafkaAdminPort using kafka-python.'''

    def __init__(self, bootstrap_servers: str, client_id: str = 'kafka-admin'):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers,
            client_id=client_id
        )

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        new_topic = NewTopic(
            name=topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        try:
            self.admin_client.create_topics([new_topic], validate_only=False)
        except TopicAlreadyExistsError:
            pass

    def delete_topic(self, topics: List[str]) -> None:
        try:
            self.admin_client.delete_topics(topics)
        except UnknownTopicOrPartitionError:
            pass

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        # kafka-python does not expose ClusterMetadata directly, but admin_client._client.cluster is a ClusterMetadata
        # We'll trigger a metadata update and return the cluster object
        if topic:
            self.admin_client._client.poll(timeout_ms=timeout*1000)
            self.admin_client._client.cluster.request_update()
            self.admin_client._client.poll(timeout_ms=timeout*1000)
            # This will ensure metadata is up to date
        else:
            self.admin_client._client.poll(timeout_ms=timeout*1000)
            self.admin_client._client.cluster.request_update()
            self.admin_client._client.poll(timeout_ms=timeout*1000)
        return self.admin_client._client.cluster
