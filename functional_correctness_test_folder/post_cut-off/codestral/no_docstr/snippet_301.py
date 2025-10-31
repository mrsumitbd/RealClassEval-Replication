
from abc import ABC, abstractmethod
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewTopic
from kafka.cluster import ClusterMetadata


class KafkaAdminPort(ABC):

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass

    @abstractmethod
    def delete_topic(self, topics: list[str]) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        pass


class KafkaAdminClientImpl(KafkaAdminPort):

    def __init__(self, bootstrap_servers: str):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        new_topic = NewTopic(
            name=topic, num_partitions=num_partitions, replication_factor=replication_factor)
        self.admin_client.create_topics([new_topic])

    def delete_topic(self, topics: list[str]) -> None:
        self.admin_client.delete_topics(topics=topics)

    def list_topics(self, topic: str | None = None, timeout: int = 1) -> ClusterMetadata:
        consumer = KafkaConsumer(
            bootstrap_servers=self.admin_client.config['bootstrap_servers'])
        if topic:
            return consumer.topics()[topic]
        else:
            return consumer.topics()
