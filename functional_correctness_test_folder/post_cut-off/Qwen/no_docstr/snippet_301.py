
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ClusterMetadata:
    topics: List[str]
    # Add other necessary fields for ClusterMetadata


class KafkaAdminPort(ABC):

    @abstractmethod
    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass

    @abstractmethod
    def delete_topic(self, topics: List[str]) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str] = None, timeout: int = 1) -> ClusterMetadata:
        pass
