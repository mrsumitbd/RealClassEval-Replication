
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
        try:
            new_topic = NewTopic(topic, num_partitions, replication_factor)
            self.admin_client.create_topics([new_topic])
        except Exception as e:
            print(f"Failed to create topic {topic}: {str(e)}")

    def delete_topic(self, topics: list[str]) -> None:
        try:
            self.admin_client.delete_topics(topics)
        except Exception as e:
            print(f"Failed to delete topics {topics}: {str(e)}")

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        try:
            if topic:
                return self.admin_client.describe_topics([topic], timeout_ms=timeout*1000)[0]
            else:
                return self.admin_client.describe_cluster()
        except Exception as e:
            print(f"Failed to list topics: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    kafka_admin = KafkaAdminImpl('localhost:9092')
    kafka_admin.create_topic('test_topic', 3, 1)
    print(kafka_admin.list_topics())
    kafka_admin.delete_topic(['test_topic'])
    print(kafka_admin.list_topics())
