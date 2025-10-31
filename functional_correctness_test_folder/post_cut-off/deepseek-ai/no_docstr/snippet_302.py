
from abc import ABC, abstractmethod
from typing import Union, Optional
from kafka import KafkaProducer
from kafka.cluster import ClusterMetadata


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
