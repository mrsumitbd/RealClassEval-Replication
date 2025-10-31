
from abc import ABC, abstractmethod
from typing import Optional, Union


class ClusterMetadata:
    def __init__(self, topics: list[str]):
        self.topics = topics

    def __repr__(self):
        return f"ClusterMetadata(topics={self.topics})"


class KafkaProducerPort(ABC):

    @abstractmethod
    def produce(self, message: Union[str, bytes]) -> None:
        pass

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        pass
