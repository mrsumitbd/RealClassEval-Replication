
from abc import ABC, abstractmethod
from typing import Optional, Union
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
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
