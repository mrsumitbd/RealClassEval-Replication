
from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class ClusterMetadata:
    def __init__(self, topics: Dict[str, dict]):
        self.topics = topics

    def __repr__(self):
        return f"ClusterMetadata(topics={self.topics})"


class KafkaAdminPort(ABC):

    def __init__(self):
        # Simulate Kafka topics as a dict: topic_name -> {'partitions': int, 'replication_factor': int}
        self._topics: Dict[str, dict] = {}

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str]) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        pass


class InMemoryKafkaAdminPort(KafkaAdminPort):
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        if topic in self._topics:
            raise ValueError(f"Topic '{topic}' already exists.")
        self._topics[topic] = {
            'partitions': num_partitions,
            'replication_factor': replication_factor
        }

    def delete_topic(self, topics: List[str]) -> None:
        for t in topics:
            if t in self._topics:
                del self._topics[t]

    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        if topic is None:
            return ClusterMetadata(self._topics.copy())
        else:
            if topic in self._topics:
                return ClusterMetadata({topic: self._topics[topic].copy()})
            else:
                return ClusterMetadata({})
