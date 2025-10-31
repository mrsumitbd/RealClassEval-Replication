
from abc import ABC, abstractmethod
from typing import Union, Optional


class ClusterMetadata:
    def __init__(self, topics: list):
        self.topics = topics


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
