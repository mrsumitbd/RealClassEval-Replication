
from abc import ABC, abstractmethod
from typing import Optional
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from kafka.cluster import ClusterMetadata


class KafkaAdminPort(ABC):
    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass

    @abstractmethod
    def delete_topic(self, topics: list[str]) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        pass


class KafkaAdminImpl(KafkaAdminPort):
    def __init__(self, bootstrap_servers: str):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        try:
            new_topic = NewTopic(topic, num_partitions, replication_factor)
            self.admin_client.create_topics([new_topic])
        except TopicAlreadyExistsError:
            print(f"Topic {topic} already exists.")

    def delete_topic(self, topics: list[str]) -> None:
        try:
            self.admin_client.delete_topics(topics)
        except UnknownTopicOrPartitionError:
            print(f"One or more topics {topics} do not exist.")

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        return self.admin_client.list_topics(topic, timeout)


# Example usage
if __name__ == "__main__":
    kafka_admin = KafkaAdminImpl('localhost:9092')
    kafka_admin.create_topic('test_topic', 3, 1)
    kafka_admin.list_topics()
    kafka_admin.delete_topic(['test_topic'])
