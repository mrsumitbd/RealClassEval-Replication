
from abc import ABC, abstractmethod
from typing import Optional
from kafka import KafkaAdminClient, NewTopic, TopicDescription, ClusterMetadata
from kafka.admin import ConfigResource, ConfigResourceType


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


class KafkaAdminImpl(KafkaAdminPort):
    def __init__(self, bootstrap_servers: str):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        new_topic = NewTopic(topic, num_partitions, replication_factor)
        try:
            self.admin_client.create_topics([new_topic])
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")

    def delete_topic(self, topics: list[str]) -> None:
        try:
            self.admin_client.delete_topics(topics)
        except Exception as e:
            print(f"Failed to delete topics {topics}: {e}")

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        try:
            if topic:
                return self.admin_client.describe_topics([topic], timeout_ms=timeout * 1000)
            else:
                return self.admin_client.list_topics(timeout_ms=timeout * 1000)
        except Exception as e:
            print(f"Failed to list topics: {e}")
            return ClusterMetadata({})


# Example usage
if __name__ == "__main__":
    kafka_admin = KafkaAdminImpl("localhost:9092")
    kafka_admin.create_topic(
        "my_topic", num_partitions=3, replication_factor=1)
    metadata = kafka_admin.list_topics()
    print(metadata.topics)
    kafka_admin.delete_topic(["my_topic"])
